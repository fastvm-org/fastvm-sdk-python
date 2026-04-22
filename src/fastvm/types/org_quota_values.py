# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OrgQuotaValues"]


class OrgQuotaValues(BaseModel):
    disk_gi_b: int = FieldInfo(alias="diskGiB")

    memory_mi_b: int = FieldInfo(alias="memoryMiB")

    snapshot_count: int = FieldInfo(alias="snapshotCount")

    vcpu: int
