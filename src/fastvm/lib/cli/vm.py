"""``fastvm vm`` subcommands."""

from __future__ import annotations

import sys
from typing import Any

import click

from ._output import click_echo, print_json, print_table, print_detail

_VM_LIST_COLS = [
    ("id", "ID"),
    ("name", "NAME"),
    ("machine_name", "MACHINE"),
    ("status", "STATUS"),
    ("public_ipv6", "IPv6"),
    ("created_at", "CREATED"),
]

# Generated pydantic aliases collapse JSON ``memoryMiB`` → Python
# ``memory_mi_b``; the table/detail attr names here are those snake-cased forms.
_VM_DETAIL_FIELDS = [
    ("id", "ID"),
    ("name", "Name"),
    ("machine_name", "Machine"),
    ("cpu", "vCPU"),
    ("memory_mi_b", "Memory (MiB)"),
    ("disk_gi_b", "Disk (GiB)"),
    ("status", "Status"),
    ("source_name", "Source"),
    ("public_ipv6", "IPv6"),
    ("created_at", "Created"),
]


@click.group()
def vm() -> None:
    """Manage VMs."""


@vm.command("launch")
@click.option("--machine", "-m", "machine_type", default="c1m2", help="Machine type.")
@click.option("--name", "-n", default=None, help="VM name.")
@click.option("--disk-gib", "disk_gi_b", type=int, default=None, help="Disk size in GiB.")
@click.option("--console", "open_console", is_flag=True, help="Open console after launch.")
@click.pass_context
def vm_launch(
    ctx: click.Context,
    machine_type: str,
    name: str | None,
    disk_gi_b: int | None,
    open_console: bool,
) -> None:
    """Launch a new VM and wait until it is ready (use --console to connect)."""
    _do_launch(ctx, machine_type, name, disk_gi_b, open_console)


def _do_launch(
    ctx: click.Context,
    machine_type: str,
    name: str | None,
    disk_gi_b: int | None,
    open_console: bool,
) -> None:
    from . import _console
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            kwargs: dict[str, Any] = {"machine_type": machine_type}
            if name:
                kwargs["name"] = name
            if disk_gi_b is not None:
                kwargs["disk_gi_b"] = disk_gi_b
            new_vm = await client.launch(**kwargs)
            if output_json:
                print_json(new_vm)
            else:
                click_echo(f"VM {new_vm.id[:8]} ({new_vm.name}) is {new_vm.status}")
            if open_console:
                click_echo("Connecting to console…")
                await _console.connect(client, new_vm.id)

    run_async(_run())


@vm.command("ls")
@click.pass_context
def vm_ls(ctx: click.Context) -> None:
    """List all VMs."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            vms = await client.vms.list()
            if output_json:
                print_json(vms)
            else:
                if not vms:
                    click_echo("No VMs.")
                    return
                print_table(list(vms), _VM_LIST_COLS)

    run_async(_run())


@vm.command("get")
@click.argument("vm_id")
@click.pass_context
def vm_get(ctx: click.Context, vm_id: str) -> None:
    """Show details for a VM."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            v = await client.vms.retrieve(vm_id)
            if output_json:
                print_json(v)
            else:
                print_detail(v, _VM_DETAIL_FIELDS)

    run_async(_run())


@vm.command("rm")
@click.argument("vm_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
@click.pass_context
def vm_rm(ctx: click.Context, vm_id: str, yes: bool) -> None:
    """Delete a VM."""
    _do_rm(ctx, vm_id, yes)


def _do_rm(ctx: click.Context, vm_id: str, yes: bool) -> None:
    from .main import run_async, make_client

    client = make_client(ctx)

    async def _run() -> None:
        async with client:
            if not yes:
                v = await client.vms.retrieve(vm_id)
                click.confirm(f"Delete VM {v.id[:8]} ({v.name})?", abort=True)
            await client.vms.delete(vm_id)
            click_echo(f"Deleted {vm_id[:8]}")

    run_async(_run())


@vm.command("rename")
@click.argument("vm_id")
@click.argument("new_name")
@click.pass_context
def vm_rename(ctx: click.Context, vm_id: str, new_name: str) -> None:
    """Rename a VM."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            v = await client.vms.update(vm_id, name=new_name)
            if output_json:
                print_json(v)
            else:
                click_echo(f"Renamed {v.id[:8]} → {v.name}")

    run_async(_run())


@vm.command("exec", context_settings={"ignore_unknown_options": True})
@click.argument("vm_id")
@click.argument("command", nargs=-1, required=True, type=click.UNPROCESSED)
@click.option("--timeout", "timeout_sec", type=int, default=None, help="Command timeout in seconds (server-side).")
@click.pass_context
def vm_exec(ctx: click.Context, vm_id: str, command: tuple[str, ...], timeout_sec: int | None) -> None:
    """Run a command on a VM."""
    _do_exec(ctx, vm_id, command, timeout_sec=timeout_sec)


def _do_exec(
    ctx: click.Context,
    vm_id: str,
    command: tuple[str, ...],
    *,
    timeout_sec: int | None = None,
) -> None:
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)
    # CLI always flattens the argv tail into a single shell string — the
    # ``_VmsResourceExt.run`` override wraps it back into ``sh -c`` for us.
    cmd = " ".join(command)

    async def _run() -> None:
        async with client:
            kwargs: dict[str, Any] = {}
            if timeout_sec is not None:
                kwargs["timeout_sec"] = timeout_sec
            result = await client.vms.run(vm_id, command=cmd, **kwargs)
            if output_json:
                print_json(result)
            else:
                if result.stdout:
                    sys.stdout.write(result.stdout)
                if result.stderr:
                    sys.stderr.write(result.stderr)
                if result.timed_out:
                    sys.stderr.write("Warning: command timed out\n")
                if result.stdout_truncated:
                    sys.stderr.write("Warning: stdout was truncated\n")
                if result.stderr_truncated:
                    sys.stderr.write("Warning: stderr was truncated\n")
                if result.exit_code != 0:
                    sys.exit(result.exit_code)

    run_async(_run())


@vm.command("console")
@click.argument("vm_id")
@click.pass_context
def vm_console(ctx: click.Context, vm_id: str) -> None:
    """Open an interactive console on a VM."""
    _do_console(ctx, vm_id)


def _do_console(ctx: click.Context, vm_id: str) -> None:
    from . import _console
    from .main import run_async, make_client

    client = make_client(ctx)

    async def _run() -> None:
        async with client:
            click_echo(f"Connecting to console for {vm_id[:8]}…")
            click_echo("(Use Ctrl-] to disconnect)\n")
            await _console.connect(client, vm_id)

    run_async(_run())
