# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["BuildResponse"]


class BuildResponse(BaseModel):
    """Build state snapshot.

    Returned by `POST /v1/builds` (initial
    `pending` state) and `GET /v1/builds/{id}` (current state on
    each poll).
    """

    id: str
    """Build ID (UUID). Use this to poll status."""

    created_at: datetime = FieldInfo(alias="createdAt")

    image_ref: str = FieldInfo(alias="imageRef")

    status: str
    """Current state.

    Known values: `pending` (accepted, not yet started), `running` (worker is
    executing), `completed` (snapshot is ready), `failed` (build did not produce a
    snapshot). Additional values may be introduced in future server versions;
    clients should treat unknown values as "in progress" rather than as hard errors.
    """

    error: Optional[str] = None
    """Set when `status` is `failed`.

    Diagnostic from the worker (truncated to ~4 KiB).
    """

    name: Optional[str] = None

    progress: Optional[str] = None
    """
    Human-readable phase string while the build runs (e.g. `creating build VM`,
    `buildah pull`, `buildah bud`, `applying image`, `settling VM`,
    `creating snapshot`). Not present after a terminal status.
    """

    snapshot_id: Optional[str] = FieldInfo(alias="snapshotId", default=None)
    """Set when `status` is `completed`.

    Fetch the corresponding Snapshot record via `GET /v1/snapshots/{id}`.
    """
