# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["FirewallRule"]


class FirewallRule(BaseModel):
    port_start: int = FieldInfo(alias="portStart")
    """Start of port range (inclusive). Required."""

    protocol: str
    """IP protocol.

    Known values: `tcp`, `udp`. Additional values may be introduced in future server
    versions.
    """

    description: Optional[str] = None

    port_end: Optional[int] = FieldInfo(alias="portEnd", default=None)
    """End of port range (inclusive). Omit for single-port rules."""

    source_cidrs: Optional[List[str]] = FieldInfo(alias="sourceCidrs", default=None)
    """Allowed source CIDRs in IPv6 notation (e.g.

    `2001:db8::/32`). Omit or empty to allow any source. IPv4 CIDRs are rejected.
    """
