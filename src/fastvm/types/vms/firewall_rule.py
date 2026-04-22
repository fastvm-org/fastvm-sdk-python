# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["FirewallRule"]


class FirewallRule(BaseModel):
    """A single allow rule for public IPv6 ingress."""

    port_start: int = FieldInfo(alias="portStart")

    protocol: Literal["tcp", "udp"]

    description: Optional[str] = None

    port_end: Optional[int] = FieldInfo(alias="portEnd", default=None)

    source_cidrs: Optional[List[str]] = FieldInfo(alias="sourceCidrs", default=None)
    """IPv6 CIDRs allowed by this rule.

    If omitted, the backend treats the rule as open to `::/0`.
    """
