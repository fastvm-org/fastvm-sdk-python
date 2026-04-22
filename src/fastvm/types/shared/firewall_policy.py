# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .firewall_rule import FirewallRule

__all__ = ["FirewallPolicy"]


class FirewallPolicy(BaseModel):
    mode: str
    """Firewall mode.

    Known values: `open` (allow all inbound traffic), `restricted` (deny by default;
    only rules listed in `ingress` are allowed). Additional values may be introduced
    in future server versions.
    """

    ingress: Optional[List[FirewallRule]] = None
