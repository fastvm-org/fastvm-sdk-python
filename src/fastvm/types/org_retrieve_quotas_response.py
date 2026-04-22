# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .org_quota_values import OrgQuotaValues

__all__ = ["OrgRetrieveQuotasResponse"]


class OrgRetrieveQuotasResponse(BaseModel):
    limits: OrgQuotaValues

    org_id: str = FieldInfo(alias="orgId")

    usage: OrgQuotaValues
