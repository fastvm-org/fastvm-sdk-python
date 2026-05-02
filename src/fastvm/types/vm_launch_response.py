# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .vm import Vm
from .._models import BaseModel

__all__ = [
    "VmLaunchResponse",
    "VmLaunchResponseSnapshotRestoreWarnings",
    "VmLaunchResponseSnapshotRestoreWarningsUnregisteredService",
]


class VmLaunchResponseSnapshotRestoreWarningsUnregisteredService(BaseModel):
    """
    Captured (name, port, h2c) tuple for a single service
    registration on a snapshotted VM. Carried across snapshot/
    restore by `POST /v1/vms` (snapshot-restore branch) so the
    new VM gets the same service registrations the source VM
    had at snapshot time.
    """

    name: str

    port: int

    h2c: Optional[bool] = None


class VmLaunchResponseSnapshotRestoreWarnings(BaseModel):
    """Reports best-effort failures during the snapshot-restore
    service-replay step.

    Only present when restoring from a
    snapshot AND the post-create bulk service registration failed.
    The VM is created successfully and usable; the user can
    manually re-register the listed services with one
    `POST /v1/vms/{id}/services` per service.

    Bulk service registration is atomic at Redis (one Lua call
    either writes all-N entries or zero), so partial state
    ("5 of 8 registered") is impossible — the response is always
    either a VM with all services registered or a VM with zero
    services and the full list returned here.
    """

    services_registration_failed: bool = FieldInfo(alias="servicesRegistrationFailed")
    """Always `true` when this object is present."""

    reason: Optional[str] = None
    """Operator-facing diagnostic for the failure."""

    unregistered_services: Optional[List[VmLaunchResponseSnapshotRestoreWarningsUnregisteredService]] = FieldInfo(
        alias="unregisteredServices", default=None
    )
    """Services from the snapshot that did not land on the new VM.

    Caller can re-register each via `POST /v1/vms/{id}/services`.
    """


class VmLaunchResponse(Vm):
    """VM object as returned by `POST /v1/vms`.

    On snapshot restore,
    an optional `snapshotRestoreWarnings` field may be present if
    the captured services failed to re-register on the new VM.
    Existing SDK callers that don't know about the field see the
    unchanged VM wire shape (`omitempty` keeps the field absent on
    cold boots and on warning-free restores).
    """

    snapshot_restore_warnings: Optional[VmLaunchResponseSnapshotRestoreWarnings] = FieldInfo(
        alias="snapshotRestoreWarnings", default=None
    )
    """Reports best-effort failures during the snapshot-restore service-replay step.

    Only present when restoring from a snapshot AND the post-create bulk service
    registration failed. The VM is created successfully and usable; the user can
    manually re-register the listed services with one `POST /v1/vms/{id}/services`
    per service.

    Bulk service registration is atomic at Redis (one Lua call either writes all-N
    entries or zero), so partial state ("5 of 8 registered") is impossible — the
    response is always either a VM with all services registered or a VM with zero
    services and the full list returned here.
    """
