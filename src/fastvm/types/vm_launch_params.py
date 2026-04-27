# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .shared_params.firewall_policy import FirewallPolicy

__all__ = ["VmLaunchParams"]


class VmLaunchParams(TypedDict, total=False):
    disk_gi_b: Annotated[int, PropertyInfo(alias="diskGiB")]
    """Override the default disk size (GiB)."""

    firewall: FirewallPolicy

    machine_type: Annotated[str, PropertyInfo(alias="machineType")]
    """Machine size identifier (e.g.

    `c1m2`, `c2m4`). Controls CPU and memory allocation. Must be supplied on launch
    unless restoring from a snapshot.
    """

    metadata: Dict[str, str]
    """Free-form string→string map.

    Server-enforced limits: up to 256 keys, key length 1–256 bytes, value length
    ≤4096 bytes, total JSON encoding ≤65536 bytes.
    """

    name: str
    """
    User-facing name (trimmed + whitespace-collapsed, max 64 runes after
    normalization; longer values are truncated server-side). Auto-generated as
    `vm-<8-char-id-prefix>` if empty.
    """

    snapshot_id: Annotated[str, PropertyInfo(alias="snapshotId")]
    """Snapshot ID to restore from."""
