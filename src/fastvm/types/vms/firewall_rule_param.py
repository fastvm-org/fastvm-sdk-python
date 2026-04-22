# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["FirewallRuleParam"]


class FirewallRuleParam(TypedDict, total=False):
    """A single allow rule for public IPv6 ingress."""

    port_start: Required[Annotated[int, PropertyInfo(alias="portStart")]]

    protocol: Required[Literal["tcp", "udp"]]

    description: str

    port_end: Annotated[int, PropertyInfo(alias="portEnd")]

    source_cidrs: Annotated[SequenceNotStr[str], PropertyInfo(alias="sourceCidrs")]
    """IPv6 CIDRs allowed by this rule.

    If omitted, the backend treats the rule as open to `::/0`.
    """
