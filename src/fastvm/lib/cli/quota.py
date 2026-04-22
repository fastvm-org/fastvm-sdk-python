"""``fastvm quota`` command."""

from __future__ import annotations

import click

from ._output import click_echo, print_json


@click.command()
@click.pass_context
def quota(ctx: click.Context) -> None:
    """Show organization quota limits and current usage."""
    from .main import run_async, make_client

    client = make_client(ctx)
    output_json = ctx.obj.get("output_json", False)

    async def _run() -> None:
        async with client:
            q = await client.quotas.retrieve()
            if output_json:
                print_json(q)
            else:
                click_echo("  Resource      Usage / Limit")
                click_echo("  ─────────────────────────────")
                click_echo(f"  vCPU          {q.usage.vcpu:>5} / {q.limits.vcpu}")
                click_echo(f"  Memory (MiB)  {q.usage.memory_mi_b:>5} / {q.limits.memory_mi_b}")
                click_echo(f"  Disk (GiB)    {q.usage.disk_gi_b:>5} / {q.limits.disk_gi_b}")
                click_echo(f"  Snapshots     {q.usage.snapshot_count:>5} / {q.limits.snapshot_count}")

    run_async(_run())
