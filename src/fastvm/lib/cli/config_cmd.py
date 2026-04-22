"""``fastvm config`` subcommands.

Named ``config_cmd`` to avoid colliding with the ``_config`` module.
"""

from __future__ import annotations

import click

from . import _config
from ._output import click_echo

_VALID_KEYS = {"api_key", "base_url"}


@click.group()
def config() -> None:
    """View and manage CLI configuration."""


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Set a config value (api_key, base_url)."""
    if key not in _VALID_KEYS:
        raise click.ClickException(f"Unknown config key '{key}'. Valid keys: {', '.join(sorted(_VALID_KEYS))}")
    _config.set_value(key, value)
    display = f"{value[:8]}…" if key == "api_key" and len(value) > 12 else value
    click_echo(f"Set {key} = {display}")


@config.command("get")
@click.argument("key", required=False, default=None)
def config_get(key: str | None) -> None:
    """Show a config value, or all config if no key given."""
    data = _config.load()
    if key is not None:
        if key not in _VALID_KEYS:
            raise click.ClickException(f"Unknown config key '{key}'. Valid keys: {', '.join(sorted(_VALID_KEYS))}")
        val = data.get(key, "")
        click_echo(val if val else "(not set)")
    else:
        if not data:
            click_echo("No configuration set. Use 'fastvm config set <key> <value>'.")
            return
        for k, v in sorted(data.items()):
            display = f"{v[:8]}…" if k == "api_key" and isinstance(v, str) and len(v) > 12 else v
            click_echo(f"  {k} = {display}")
