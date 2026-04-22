# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .vms.firewall_policy import FirewallPolicy

__all__ = ["SnapshotObject"]


class SnapshotObject(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    name: str

    org_id: str = FieldInfo(alias="orgId")

    status: Literal["creating", "ready", "error"]

    vm_id: str = FieldInfo(alias="vmId")

    firewall: Optional[FirewallPolicy] = None
    """Public IPv6 ingress firewall policy applied to the VM."""
