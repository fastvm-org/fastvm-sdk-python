# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .vm_instance import VmInstance

__all__ = ["VmListResponse"]

VmListResponse: TypeAlias = List[VmInstance]
