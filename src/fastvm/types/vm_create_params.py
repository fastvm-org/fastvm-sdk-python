# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .vms.firewall_policy_param import FirewallPolicyParam

__all__ = ["VmCreateParams"]


class VmCreateParams(TypedDict, total=False):
    disk_gi_b: Annotated[int, PropertyInfo(alias="diskGiB")]
    """Optional grow-only disk size in GiB.

    Must be >= base machine disk (10 GiB) or >= source snapshot VM disk.
    """

    firewall: FirewallPolicyParam
    """
    Public IPv6 ingress firewall policy captured from the source VM at snapshot
    time.
    """

    machine_type: Annotated[Literal["c1m2", "c2m4", "c4m8", "c8m16"], PropertyInfo(alias="machineType")]

    name: str

    snapshot_id: Annotated[str, PropertyInfo(alias="snapshotId")]
