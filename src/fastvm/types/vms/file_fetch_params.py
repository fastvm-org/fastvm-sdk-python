# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["FileFetchParams"]


class FileFetchParams(TypedDict, total=False):
    path: Required[str]
    """Absolute destination path inside the guest filesystem."""

    url: Required[str]
    """
    Must be the `downloadUrl` previously returned by
    `POST /v1/vms/{id}/files/presign` (URLs from other sources are rejected).
    """

    timeout_sec: Annotated[int, PropertyInfo(alias="timeoutSec")]
    """Per-fetch timeout in seconds."""
