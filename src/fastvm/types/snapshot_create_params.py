# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SnapshotCreateParams"]


class SnapshotCreateParams(TypedDict, total=False):
    vm_id: Required[Annotated[str, PropertyInfo(alias="vmId")]]

    name: str
    """
    Snapshot name (trimmed + whitespace-collapsed, max 64 runes; longer values are
    truncated server-side). Auto-generated as `snapshot-<8-char-vmId-prefix>` if
    empty.
    """
