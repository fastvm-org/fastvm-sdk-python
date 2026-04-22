"""Shared output formatting for the CLI: tables and JSON."""

from __future__ import annotations

import sys
import json
from typing import Any, Sequence
from datetime import datetime, timezone

from tabulate import tabulate  # type: ignore[import-untyped]

# Timestamp-typed fields get humanized formatting in tables / detail output.
# Covers both generated snake_case attrs and the ISO-aliased wire names.
_TIMESTAMP_ATTRS = frozenset({"created_at", "deleted_at", "updated_at"})


def _fmt_ts(value: Any) -> str:
    """Accept a datetime or ISO string; emit a compact local-time rendering."""
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            raw = str(value).rstrip("Z")
            if "." in raw:
                base, frac = raw.split(".", 1)
                raw = f"{base}.{frac[:6]}"
            dt = datetime.fromisoformat(raw)
        except Exception:
            return str(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    local = dt.astimezone()
    hour = local.hour % 12 or 12
    ampm = "am" if local.hour < 12 else "pm"
    return f"{local.day} {local.strftime('%b')} {local.year}, {hour}:{local.strftime('%M')}{ampm}"


def _serialize(obj: Any) -> Any:
    """Convert pydantic models / nested structures to plain JSON-able data."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump(by_alias=True, mode="json")
    if isinstance(obj, list):
        lst: list[Any] = obj
        return [_serialize(x) for x in lst]
    if isinstance(obj, dict):
        d: dict[Any, Any] = obj
        return {k: _serialize(v) for k, v in d.items()}
    return obj


def print_json(data: Any) -> None:
    json.dump(_serialize(data), sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


def print_table(
    rows: Sequence[Any],
    columns: list[tuple[str, str]],
    *,
    short_id: bool = True,
) -> None:
    """Print *rows* (pydantic models) as a human-readable table.

    *columns* is a list of ``(attr_name, header_label)`` pairs. When *short_id*
    is true, any column named ``id`` is truncated git-style to 8 chars.
    """
    table_data: list[list[str]] = []
    headers = [label for _, label in columns]
    for row in rows:
        cells: list[str] = []
        for attr, _ in columns:
            val = getattr(row, attr, "")
            if short_id and attr == "id" and isinstance(val, str) and len(val) > 8:
                val = val[:8]
            if attr in _TIMESTAMP_ATTRS and val:
                val = _fmt_ts(val)
            cells.append("" if val is None else str(val))
        table_data.append(cells)
    click_echo(tabulate(table_data, headers=headers, tablefmt="plain"))


def print_detail(obj: Any, fields_map: list[tuple[str, str]]) -> None:
    """Print a single object as key-value pairs."""
    max_label = max(len(label) for _, label in fields_map) if fields_map else 0
    for attr, label in fields_map:
        val = getattr(obj, attr, "")
        if val is None:
            val = ""
        if attr in _TIMESTAMP_ATTRS and val:
            val = _fmt_ts(val)
        click_echo(f"  {label:<{max_label}}  {val}")


def click_echo(msg: str = "") -> None:
    """Write a line to stdout, swallowing broken-pipe errors."""
    try:
        sys.stdout.write(msg + "\n")
        sys.stdout.flush()
    except BrokenPipeError:
        pass
