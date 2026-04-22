# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["VmUpdateParams"]


class VmUpdateParams(TypedDict, total=False):
    metadata: Dict[str, str]
    """Free-form string→string map.

    Server-enforced limits: up to 256 keys, key length 1–256 bytes, value length
    ≤4096 bytes, total JSON encoding ≤65536 bytes.
    """

    name: str
