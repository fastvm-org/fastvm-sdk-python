# Shared Types

```python
from fastvm.types import FirewallPolicy, FirewallRule
```

# Fastvm

Types:

```python
from fastvm.types import HealthResponse
```

Methods:

- `client.health() -> HealthResponse`

# Vms

Types:

```python
from fastvm.types import ConsoleToken, ExecResult, Vm, VmListResponse, VmDeleteResponse
```

Methods:

- `client.vms.retrieve(id) -> Vm`
- `client.vms.update(id, \*\*params) -> Vm`
- `client.vms.list() -> VmListResponse`
- `client.vms.delete(id) -> VmDeleteResponse`
- `client.vms.console_token(id) -> ConsoleToken`
- `client.vms.launch(\*\*params) -> Vm`
- `client.vms.patch_firewall(id, \*\*params) -> Vm`
- `client.vms.run(id, \*\*params) -> ExecResult`
- `client.vms.set_firewall(id, \*\*params) -> Vm`

## Files

Types:

```python
from fastvm.types.vms import PresignResponse
```

Methods:

- `client.vms.files.fetch(id, \*\*params) -> ExecResult`
- `client.vms.files.presign(id, \*\*params) -> PresignResponse`

# Snapshots

Types:

```python
from fastvm.types import Snapshot, SnapshotListResponse, SnapshotDeleteResponse
```

Methods:

- `client.snapshots.create(\*\*params) -> Snapshot`
- `client.snapshots.update(id, \*\*params) -> Snapshot`
- `client.snapshots.list() -> SnapshotListResponse`
- `client.snapshots.delete(id) -> SnapshotDeleteResponse`

# Quotas

Types:

```python
from fastvm.types import OrgQuotaUsage, OrgQuotaValues
```

Methods:

- `client.quotas.retrieve() -> OrgQuotaUsage`

# Helpers

Hand-written convenience methods on top of the generated client. Source:
`[src/fastvm/lib/](./src/fastvm/lib/)`. Full docs: `[helpers.md](./helpers.md)`.

Errors (all subclass `fastvm.FastvmError`):

```python
from fastvm import VMLaunchError, VMNotReadyError, FileTransferError
```

Methods:

- `client.wait_for_vm_ready(vm_id, \*args) -> Vm`
- `client.upload(vm_id, local_path, remote_path, \*args) -> None`
- `client.download(vm_id, remote_path, local_path, \*args) -> None`

Signature overrides on generated methods:

- `client.vms.launch(\*, wait: bool = True, poll_interval: float = 2.0, timeout: float = 300.0, \*\*params) -> Vm`
  Polls `GET /v1/vms/{id}` until `status == "running"` before returning. Pass `wait=False` to mirror the raw `POST /v1/vms` behaviour.
- `client.vms.run(id, command: str | Sequence[str], \*\*params) -> ExecResult`
  A shell string is auto-wrapped into `["sh", "-c", ...]`; argv lists pass through unchanged.

