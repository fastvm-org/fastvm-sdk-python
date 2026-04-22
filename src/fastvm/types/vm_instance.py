# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .vms.firewall_policy import FirewallPolicy

__all__ = ["VmInstance"]


class VmInstance(BaseModel):
    id: str

    cpu: int

    created_at: datetime = FieldInfo(alias="createdAt")

    disk_gi_b: int = FieldInfo(alias="diskGiB")

    machine_name: str = FieldInfo(alias="machineName")

    memory_mi_b: int = FieldInfo(alias="memoryMiB")

    name: str

    org_id: str = FieldInfo(alias="orgId")

    status: Literal["provisioning", "running", "stopped", "deleting", "error"]

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)

    firewall: Optional[FirewallPolicy] = None
    """Public IPv6 ingress firewall policy.

    If omitted for a newly created VM, the default is `restricted` with no ingress
    rules.
    """

    public_ipv6: Optional[str] = FieldInfo(alias="publicIpv6", default=None)

    source_name: Optional[str] = FieldInfo(alias="sourceName", default=None)
