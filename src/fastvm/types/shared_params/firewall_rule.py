# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["FirewallRule"]


class FirewallRule(TypedDict, total=False):
    port_start: Required[Annotated[int, PropertyInfo(alias="portStart")]]
    """Start of port range (inclusive). Required."""

    protocol: Required[str]
    """IP protocol.

    Known values: `tcp`, `udp`. Additional values may be introduced in future server
    versions.
    """

    description: str

    port_end: Annotated[int, PropertyInfo(alias="portEnd")]
    """End of port range (inclusive). Omit for single-port rules."""

    source_cidrs: Annotated[SequenceNotStr[str], PropertyInfo(alias="sourceCidrs")]
    """Allowed source CIDRs in IPv6 notation (e.g.

    `2001:db8::/32`). Omit or empty to allow any source. IPv4 CIDRs are rejected.
    """
