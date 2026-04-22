# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

from .shared_params.firewall_rule import FirewallRule

__all__ = ["VmPatchFirewallParams"]


class VmPatchFirewallParams(TypedDict, total=False):
    ingress: Iterable[FirewallRule]

    mode: str
    """Firewall mode.

    Known values: `open` (allow all inbound traffic), `restricted` (deny by default;
    only rules listed in `ingress` are allowed). Additional values may be introduced
    in future server versions.
    """
