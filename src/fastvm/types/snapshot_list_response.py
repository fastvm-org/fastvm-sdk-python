# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .snapshot_object import SnapshotObject

__all__ = ["SnapshotListResponse"]

SnapshotListResponse: TypeAlias = List[SnapshotObject]
