# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.firewall_policy import FirewallPolicy

__all__ = ["Vm"]


class Vm(BaseModel):
    id: str

    cpu: int

    created_at: datetime = FieldInfo(alias="createdAt")

    disk_gi_b: int = FieldInfo(alias="diskGiB")

    memory_mi_b: int = FieldInfo(alias="memoryMiB")

    name: str

    org_id: str = FieldInfo(alias="orgId")

    status: str
    """Lifecycle status.

    Known values: `provisioning`, `running`, `stopped`, `deleting`, `error`.
    Terminal failure statuses are `error` and `stopped`; any other non-`running`
    value indicates the VM is still transitioning. Additional values may be
    introduced in future server versions; clients should treat unknown values as "in
    transition" rather than as hard errors.
    """

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)

    firewall: Optional[FirewallPolicy] = None

    machine_name: Optional[str] = FieldInfo(alias="machineName", default=None)

    metadata: Optional[Dict[str, str]] = None
    """Free-form string→string map.

    Server-enforced limits: up to 256 keys, key length 1–256 bytes, value length
    ≤4096 bytes, total JSON encoding ≤65536 bytes.
    """

    public_ipv6: Optional[str] = FieldInfo(alias="publicIpv6", default=None)

    source_name: Optional[str] = FieldInfo(alias="sourceName", default=None)
    """Source snapshot or image name (empty on fresh boot)."""
