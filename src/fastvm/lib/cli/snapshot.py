"""``fastvm snapshot`` subcommands."""

from __future__ import annotations

from typing import Any

import click

from ._output import click_echo, print_json, print_table

_SNAP_LIST_COLS = [
    ("id", "ID"),
    ("name", "NAME"),
    ("vm_id", "VM"),
    ("status", "STATUS"),
    ("created_at", "CREATED"),
]


@click.group()
def snapshot() -> None:
    """Manage snapshots."""


@snapshot.command("create")
@click.argument("vm_id")
@click.option("--name", "-n", default="", help="Snapshot name.")
@click.pass_context
def snap_create(ctx: click.Context, vm_id: str, name: str) -> None:
    """Create a snapshot of a running VM."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            kwargs: dict[str, Any] = {"vm_id": vm_id}
            if name:
                kwargs["name"] = name
            snap = await client.snapshots.create(**kwargs)
            if output_json:
                print_json(snap)
            else:
                click_echo(f"Snapshot {snap.id[:8]} ({snap.name}) — {snap.status}")

    run_async(_run())


@snapshot.command("ls")
@click.pass_context
def snap_ls(ctx: click.Context) -> None:
    """List all snapshots."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            snaps = await client.snapshots.list()
            if output_json:
                print_json(snaps)
            else:
                if not snaps:
                    click_echo("No snapshots.")
                    return
                print_table(list(snaps), _SNAP_LIST_COLS)

    run_async(_run())


@snapshot.command("rm")
@click.argument("snapshot_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
@click.pass_context
def snap_rm(ctx: click.Context, snapshot_id: str, yes: bool) -> None:
    """Delete a snapshot."""
    from .main import run_async, make_client

    client = make_client(ctx)

    async def _run() -> None:
        async with client:
            if not yes:
                click.confirm(f"Delete snapshot {snapshot_id[:8]}?", abort=True)
            await client.snapshots.delete(snapshot_id)
            click_echo(f"Deleted {snapshot_id[:8]}")

    run_async(_run())


@snapshot.command("rename")
@click.argument("snapshot_id")
@click.argument("new_name")
@click.pass_context
def snap_rename(ctx: click.Context, snapshot_id: str, new_name: str) -> None:
    """Rename a snapshot."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            s = await client.snapshots.update(snapshot_id, name=new_name)
            if output_json:
                print_json(s)
            else:
                click_echo(f"Renamed {s.id[:8]} → {s.name}")

    run_async(_run())


@snapshot.command("restore")
@click.argument("snapshot_id")
@click.option("--name", "-n", default=None, help="Name for the restored VM.")
@click.option("--console", "open_console", is_flag=True, help="Open console after restore.")
@click.pass_context
def snap_restore(
    ctx: click.Context,
    snapshot_id: str,
    name: str | None,
    open_console: bool,
) -> None:
    """Restore a VM from a snapshot."""
    from . import _console
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            kwargs: dict[str, Any] = {"snapshot_id": snapshot_id}
            if name:
                kwargs["name"] = name
            # Launch with ``snapshot_id`` set = the old SDK's ``restore(...)``.
            vm = await client.launch(**kwargs)
            if output_json:
                print_json(vm)
            else:
                click_echo(f"VM {vm.id[:8]} ({vm.name}) restored — {vm.status}")
            if open_console:
                click_echo("Connecting to console…")
                await _console.connect(client, vm.id)

    run_async(_run())
