"""``fastvm firewall`` subcommands."""

from __future__ import annotations

import re
from typing import Any, cast

import click

from ._output import click_echo, print_json

_RULE_RE = re.compile(r"^(?P<proto>tcp|udp):(?P<start>\d+)(?:-(?P<end>\d+))?$", re.I)


def _parse_rule(value: str) -> dict[str, Any]:
    """Parse a rule string like ``tcp:80`` or ``udp:5000-5010`` into a dict.

    The generated client accepts dicts with snake_case keys; the wire
    serializer handles alias conversion (``portStart`` / ``portEnd``).
    """
    m = _RULE_RE.match(value)
    if not m:
        raise click.BadParameter(f"Invalid rule '{value}'. Expected format: tcp:80 or udp:5000-5010")
    rule: dict[str, Any] = {
        "protocol": m.group("proto").lower(),
        "portStart": int(m.group("start")),
    }
    if m.group("end"):
        rule["portEnd"] = int(m.group("end"))
    return rule


def _print_policy(vm_id: str, policy: object | None) -> None:
    if policy is None:
        click_echo(f"  {vm_id[:8]}  No firewall policy set")
        return
    click_echo(f"  Mode: {getattr(policy, 'mode', '')}")
    ingress = getattr(policy, "ingress", None)
    if ingress:
        click_echo("  Ingress rules:")
        for r in ingress:
            port = str(r.port_start)
            if r.port_end and r.port_end != r.port_start:
                port += f"-{r.port_end}"
            src = ", ".join(r.source_cidrs) if r.source_cidrs else "any"
            desc = f"  ({r.description})" if r.description else ""
            click_echo(f"    {r.protocol}:{port}  from {src}{desc}")
    else:
        click_echo("  Ingress rules: (none)")


@click.group()
def firewall() -> None:
    """Manage VM firewall rules."""


@firewall.command("get")
@click.argument("vm_id")
@click.pass_context
def fw_get(ctx: click.Context, vm_id: str) -> None:
    """Show the firewall policy for a VM."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            v = await client.vms.retrieve(vm_id)
            if output_json:
                print_json(v.firewall)
            else:
                _print_policy(vm_id, v.firewall)

    run_async(_run())


@firewall.command("set")
@click.argument("vm_id")
@click.option(
    "--mode",
    required=True,
    type=click.Choice(["open", "restricted"], case_sensitive=False),
    help="Firewall mode (open = allow all, restricted = deny by default).",
)
@click.option("--rule", "-r", multiple=True, help="Ingress rule (e.g. tcp:80, udp:5000-5010).")
@click.pass_context
def fw_set(ctx: click.Context, vm_id: str, mode: str, rule: tuple[str, ...]) -> None:
    """Replace the firewall policy for a VM."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)
    rules = [_parse_rule(r) for r in rule]

    async def _run() -> None:
        async with client:
            v = await client.vms.set_firewall(vm_id, mode=mode, ingress=cast(Any, rules))
            if output_json:
                print_json(v.firewall)
            else:
                click_echo(f"Firewall updated for {vm_id[:8]}")
                _print_policy(vm_id, v.firewall)

    run_async(_run())


@firewall.command("patch")
@click.argument("vm_id")
@click.option(
    "--mode",
    type=click.Choice(["open", "restricted"], case_sensitive=False),
    default=None,
    help="Firewall mode (open = allow all, restricted = deny by default).",
)
@click.option("--rule", "-r", multiple=True, help="Ingress rule (e.g. tcp:443).")
@click.pass_context
def fw_patch(ctx: click.Context, vm_id: str, mode: str | None, rule: tuple[str, ...]) -> None:
    """Partially update the firewall policy for a VM."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            kwargs: dict[str, Any] = {}
            if mode is not None:
                kwargs["mode"] = mode
            if rule:
                kwargs["ingress"] = [_parse_rule(r) for r in rule]
            v = await client.vms.patch_firewall(vm_id, **kwargs)
            if output_json:
                print_json(v.firewall)
            else:
                click_echo(f"Firewall patched for {vm_id[:8]}")
                _print_policy(vm_id, v.firewall)

    run_async(_run())
