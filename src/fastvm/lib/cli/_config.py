"""Persistent CLI configuration stored in ``$XDG_CONFIG_HOME/fastvm/config.toml``."""

from __future__ import annotations

import os
from typing import Any
from pathlib import Path

_DEFAULT_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "fastvm"
_CONFIG_FILE = "config.toml"


def _config_path() -> Path:
    return _DEFAULT_DIR / _CONFIG_FILE


def load() -> dict[str, Any]:
    path = _config_path()
    if not path.exists():
        return {}
    # ``tomllib`` only exists on 3.11+; fall back to the ``tomli`` backport.
    try:
        import tomllib  # type: ignore[import-not-found,unused-ignore]
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]
    result: dict[str, Any] = tomllib.loads(path.read_text())
    return result


def _toml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def save(data: dict[str, Any]) -> None:
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for key, value in sorted(data.items()):
        if isinstance(value, bool):
            lines.append(f"{key} = {'true' if value else 'false'}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key} = {value}")
        else:
            lines.append(f'{key} = "{_toml_escape(str(value))}"')
    path.write_text("\n".join(lines) + "\n")


def get(key: str | None = None) -> Any:
    data = load()
    if key is None:
        return data
    return data.get(key)


def set_value(key: str, value: str) -> None:
    data = load()
    data[key] = value
    save(data)
