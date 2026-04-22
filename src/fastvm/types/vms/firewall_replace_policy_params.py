# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .firewall_rule_param import FirewallRuleParam

__all__ = ["FirewallReplacePolicyParams"]


class FirewallReplacePolicyParams(TypedDict, total=False):
    mode: Required[Literal["open", "restricted"]]

    ingress: Iterable[FirewallRuleParam]
    """Allow rules evaluated only when `mode` is `restricted`.

    If empty, all public IPv6 ports are closed except essential ICMPv6 control
    traffic.
    """
