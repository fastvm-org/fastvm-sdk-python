# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .firewall_rule import FirewallRule

__all__ = ["FirewallPolicy"]


class FirewallPolicy(BaseModel):
    """Public IPv6 ingress firewall policy for a VM or snapshot."""

    mode: Literal["open", "restricted"]

    ingress: Optional[List[FirewallRule]] = None
    """Allow rules evaluated only when `mode` is `restricted`.

    If empty, all public IPv6 ports are closed except essential ICMPv6 control
    traffic.
    """
