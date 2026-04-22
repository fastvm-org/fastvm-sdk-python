# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["HealthResponse"]


class HealthResponse(BaseModel):
    status: Optional[str] = None
