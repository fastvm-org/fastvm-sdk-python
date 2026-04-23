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
