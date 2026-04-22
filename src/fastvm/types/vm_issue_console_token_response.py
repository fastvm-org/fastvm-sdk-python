# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VmIssueConsoleTokenResponse"]


class VmIssueConsoleTokenResponse(BaseModel):
    token: str

    expires_in_sec: int = FieldInfo(alias="expiresInSec")

    websocket_path: str = FieldInfo(alias="websocketPath")
