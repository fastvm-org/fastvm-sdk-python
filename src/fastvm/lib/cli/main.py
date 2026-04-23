"""FastVM CLI entry point.

Runs on top of :class:`fastvm.AsyncFastvmClient`. Handles env-var / config-file
auth resolution, asyncio bridging, and pretty ``click.ClickException`` rendering
for SDK errors.
"""

from __future__ import annotations

import sys
import asyncio
from typing import Any, Coroutine, cast

import click
import httpx

from . import _config
from .._client import AsyncFastvmClient
from ..._exceptions import APIStatusError

_DEFAULT_BASE_URL = "https://api.fastvm.org"


def run_async(coro: Coroutine[Any, Any, Any]) -> Any:
    """Run a coroutine and map SDK errors to :class:`click.ClickException`."""
    try:
        return asyncio.run(coro)
    except APIStatusError as exc:
        detail = _extract_api_detail(exc)
        raise click.ClickException(f"{exc.status_code}: {detail}") from None
    except httpx.HTTPStatusError as exc:
        try:
            payload: Any = exc.response.json()
            if isinstance(payload, dict):
                err_val: Any = payload.get("error", exc.response.text)
                detail = str(err_val)
            else:
                detail = exc.response.text
        except Exception:
            detail = exc.response.text
        raise click.ClickException(f"{exc.response.status_code} {exc.response.reason_phrase}: {detail}") from None
    except TimeoutError as exc:
        raise click.ClickException(str(exc) or "Operation timed out") from None
    except (ValueError, RuntimeError) as exc:
        raise click.ClickException(str(exc)) from None


def _extract_api_detail(exc: APIStatusError) -> str:
    body: Any = getattr(exc, "body", None)
    if isinstance(body, dict):
        for k in ("error", "message", "detail"):
            v: Any = body.get(k)
            if isinstance(v, str) and v:
                return v
    return str(exc)


def make_client(ctx: click.Context) -> AsyncFastvmClient:
    """Build an ``AsyncFastvmClient`` from the resolved context settings."""
    obj = cast("dict[str, Any]", ctx.ensure_object(dict))
    return AsyncFastvmClient(api_key=obj["api_key"] or None, base_url=obj["base_url"])


@click.group()
@click.option("--api-key", envvar="FASTVM_API_KEY", default=None, help="API key (or set FASTVM_API_KEY).")
@click.option("--base-url", envvar="FASTVM_BASE_URL", default=None, help="API base URL.")
@click.option("--json", "output_json", is_flag=True, default=False, help="Output raw JSON instead of tables.")
@click.version_option(package_name="fastvm")
@click.pass_context
def main(ctx: click.Context, api_key: str | None, base_url: str | None, output_json: bool) -> None:
    """FastVM — launch and manage Linux microVMs from your terminal."""
    cfg = _config.load()
    resolved_key = api_key or cfg.get("api_key", "")
    resolved_url = base_url or cfg.get("base_url", _DEFAULT_BASE_URL)
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = resolved_key
    ctx.obj["base_url"] = resolved_url
    ctx.obj["output_json"] = output_json


# --- Register subcommand groups (deferred to avoid circular imports) ------- #

from .vm import vm  # noqa: E402
from .quota import quota  # noqa: E402
from .firewall import firewall  # noqa: E402
from .snapshot import snapshot  # noqa: E402
from .config_cmd import config  # noqa: E402

main.add_command(vm)
main.add_command(snapshot)
main.add_command(firewall)
main.add_command(quota)
main.add_command(config)


# --- Top-level shortcuts --------------------------------------------------- #


@main.command("launch")
@click.option("--machine", "-m", "machine_type", default="c1m2", help="Machine type.")
@click.option("--name", "-n", default=None, help="VM name.")
@click.option("--disk-gib", "disk_gi_b", type=int, default=None, help="Disk size in GiB.")
@click.option("--no-console", "no_console", is_flag=True, help="Don't open console after launch.")
@click.pass_context
def launch_shortcut(
    ctx: click.Context,
    machine_type: str,
    name: str | None,
    disk_gi_b: int | None,
    no_console: bool,
) -> None:
    """Launch a new VM and open an interactive console (use --no-console to skip)."""
    from .vm import _do_launch

    _do_launch(ctx, machine_type, name, disk_gi_b, open_console=not no_console)


@main.command("rm")
@click.argument("vm_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
@click.pass_context
def rm_shortcut(ctx: click.Context, vm_id: str, yes: bool) -> None:
    """Delete a VM (shortcut for 'vm rm')."""
    from .vm import _do_rm

    _do_rm(ctx, vm_id, yes)


@main.command("exec", context_settings={"ignore_unknown_options": True})
@click.argument("vm_id")
@click.argument("command", nargs=-1, required=True, type=click.UNPROCESSED)
@click.option("--timeout", "timeout_sec", type=int, default=None, help="Command timeout in seconds (server-side).")
@click.pass_context
def exec_shortcut(
    ctx: click.Context,
    vm_id: str,
    command: tuple[str, ...],
    timeout_sec: int | None,
) -> None:
    """Run a command on a VM (shortcut for 'vm exec')."""
    from .vm import _do_exec

    _do_exec(ctx, vm_id, command, timeout_sec=timeout_sec)


@main.command("console")
@click.argument("vm_id")
@click.pass_context
def console_shortcut(ctx: click.Context, vm_id: str) -> None:
    """Open an interactive console on a VM (shortcut for 'vm console')."""
    from .vm import _do_console

    _do_console(ctx, vm_id)


@main.command("run", context_settings={"ignore_unknown_options": True})
@click.option("--machine", "-m", "machine_type", default="c1m2", help="Machine type.")
@click.option("--name", "-n", default=None, help="VM name.")
@click.option("--timeout", "timeout_sec", type=int, default=None, help="Command timeout in seconds (server-side).")
@click.argument("command", nargs=-1, required=True, type=click.UNPROCESSED)
@click.pass_context
def run_shortcut(
    ctx: click.Context,
    machine_type: str,
    name: str | None,
    timeout_sec: int | None,
    command: tuple[str, ...],
) -> None:
    """Launch a VM, run a command, print output, destroy the VM."""
    from ._output import print_json

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)
    cmd = " ".join(command)
    launched_vm_id: str | None = None

    async def _ephemeral() -> None:
        nonlocal launched_vm_id
        launch_kwargs: dict[str, Any] = {"machine_type": machine_type}
        if name:
            launch_kwargs["name"] = name
        async with client:
            vm = await client.vms.launch(**launch_kwargs)
            launched_vm_id = vm.id
            try:
                run_kwargs: dict[str, Any] = {}
                if timeout_sec is not None:
                    run_kwargs["timeout_sec"] = timeout_sec
                result = await client.vms.run(vm.id, command=cmd, **run_kwargs)
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
            finally:
                await client.vms.delete(vm.id)
                launched_vm_id = None

    async def _cleanup(vm_id: str) -> None:
        async with make_client(ctx) as c:
            await c.vms.delete(vm_id)

    try:
        run_async(_ephemeral())
    except KeyboardInterrupt:
        if launched_vm_id:
            try:
                run_async(_cleanup(launched_vm_id))
            except Exception:
                pass


if __name__ == "__main__":
    main()
