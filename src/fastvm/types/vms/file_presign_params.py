# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FilePresignParams"]


class FilePresignParams(TypedDict, total=False):
    path: Required[str]
    """
    Absolute destination path inside the guest filesystem (where the file will land
    after `fetchFileToVm`). Used only to scope the staging object key; any value
    server-side is accepted here.
    """
