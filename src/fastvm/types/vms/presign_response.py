# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PresignResponse"]


class PresignResponse(BaseModel):
    """Pair of signed URLs scoped to the same per-VM staging object.

    Both
    are usable in either direction — the pair supports both uploading a
    file into a VM and downloading a file out of a VM, depending on how
    the SDK wires them up:

      - **Upload (client → VM)**: client PUTs bytes to `uploadUrl`, then
        calls `POST /v1/vms/{id}/files/fetch` with `url: downloadUrl` to
        have the VM pull the object into the guest filesystem.
      - **Download (VM → client)**: SDK issues an exec command inside
        the VM that pipes file contents to `uploadUrl`
        (`tar czf - <path> | curl -T - <uploadUrl>`), then GETs
        `downloadUrl` from the client to stream the bytes back.

    The staging object is auto-deleted ~1 day after creation; the URLs
    themselves expire after `expiresInSec` seconds.
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
