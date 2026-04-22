# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["VmRunParams"]


class VmRunParams(TypedDict, total=False):
    command: Required[SequenceNotStr[str]]
    """Argv-style command.

    First element must be non-empty. For shell strings, wrap as
    `["sh", "-c", "<string>"]`.
    """

    timeout_sec: Annotated[int, PropertyInfo(alias="timeoutSec")]
    """Server-side execution timeout in seconds.

    Must be positive when provided; omit to use the server default.
    """
