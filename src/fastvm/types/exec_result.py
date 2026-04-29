# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExecResult"]


class ExecResult(BaseModel):
    """
    Buffered response shape for `POST /v1/vms/{id}/exec` under
    `Accept: application/json`. The server collects the streamed events
    and returns this aggregate once the command exits. Per-stream output
    is capped at 4 MiB; overflow bytes are dropped and signalled via
    `stdoutTruncated` / `stderrTruncated`. Streaming clients
    (`Accept: application/x-ndjson`) receive every byte without a cap.
    """

    duration_ms: int = FieldInfo(alias="durationMs")

    exit_code: int = FieldInfo(alias="exitCode")

    stderr: str

    stderr_truncated: bool = FieldInfo(alias="stderrTruncated")
    """True if the collector dropped stderr bytes past the 4 MiB cap."""

    stdout: str

    stdout_truncated: bool = FieldInfo(alias="stdoutTruncated")
    """True if the collector dropped stdout bytes past the 4 MiB cap."""

    timed_out: bool = FieldInfo(alias="timedOut")
