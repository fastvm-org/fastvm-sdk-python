# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["FilePresignResponse"]


class FilePresignResponse(BaseModel):
    """
    Pair of signed URLs scoped to the same per-VM staging object.
    Usable in either direction: either side (client or VM) PUTs bytes
    to `uploadUrl`, and either side GETs them back via `downloadUrl`.
    URLs expire after `expiresInSec` seconds and the staging object
    is auto-deleted after about a day.
    """

    download_url: str = FieldInfo(alias="downloadUrl")
    """Presigned GET URL for the same staging object.

    Used by the VM (via `POST /v1/vms/{id}/files/fetch`) on upload, or by the client
    (via `httpx.stream` / `curl`) on download.
    """

    expires_in_sec: int = FieldInfo(alias="expiresInSec")
    """Lifetime of both URLs in seconds."""

    max_upload_bytes: int = FieldInfo(alias="maxUploadBytes")
    """Upper bound on upload size (equals the VM's disk size in bytes)."""

    upload_url: str = FieldInfo(alias="uploadUrl")
    """Presigned PUT URL for the staging object.

    Accepts `Content-Type: application/octet-stream`. Used by the client on upload,
    or by the VM (via an exec'd `curl -T -`) on download.
    """
