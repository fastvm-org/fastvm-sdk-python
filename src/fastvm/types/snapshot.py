# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.firewall_policy import FirewallPolicy

__all__ = ["Snapshot"]


class Snapshot(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    name: str

    org_id: str = FieldInfo(alias="orgId")

    status: str
    """Snapshot lifecycle status.

    Known values: `creating`, `ready`, `error`. Additional values may be introduced
    in future server versions.
    """

    vm_id: str = FieldInfo(alias="vmId")

    firewall: Optional[FirewallPolicy] = None

    metadata: Optional[Dict[str, str]] = None
    """Free-form string→string map.

    Server-enforced limits: up to 256 keys, key length 1–256 bytes, value length
    ≤4096 bytes, total JSON encoding ≤65536 bytes.
    """
