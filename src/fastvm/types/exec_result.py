# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExecResult"]


class ExecResult(BaseModel):
    duration_ms: int = FieldInfo(alias="durationMs")

    exit_code: int = FieldInfo(alias="exitCode")

    stderr: str

    stderr_truncated: bool = FieldInfo(alias="stderrTruncated")

    stdout: str

    stdout_truncated: bool = FieldInfo(alias="stdoutTruncated")

    timed_out: bool = FieldInfo(alias="timedOut")
