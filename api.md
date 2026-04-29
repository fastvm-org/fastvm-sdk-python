# Shared Types

```python
from fastvm.types import FilePresignResponse, FirewallPolicy, FirewallRule
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
- <code title="get /v1/snapshots/{id}">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">retrieve</a>(id) -> <a href="./src/fastvm/types/snapshot.py">Snapshot</a></code>
- `client.snapshots.update(id, \*\*params) -> Snapshot`
- `client.snapshots.list() -> SnapshotListResponse`
- `client.snapshots.delete(id) -> SnapshotDeleteResponse`

# Builds

Types:

```python
from fastvm.types import BuildResponse
```

Methods:

- <code title="post /v1/builds">client.builds.<a href="./src/fastvm/resources/builds.py">create</a>(\*\*<a href="src/fastvm/types/build_create_params.py">params</a>) -> <a href="./src/fastvm/types/build_response.py">BuildResponse</a></code>
- <code title="get /v1/builds/{id}">client.builds.<a href="./src/fastvm/resources/builds.py">retrieve</a>(id) -> <a href="./src/fastvm/types/build_response.py">BuildResponse</a></code>

# BuildContexts

Methods:

- <code title="post /v1/build-contexts/presign">client.build_contexts.<a href="./src/fastvm/resources/build_contexts.py">presign</a>() -> <a href="./src/fastvm/types/shared/file_presign_response.py">FilePresignResponse</a></code>

# Quotas

Types:

```python
from fastvm.types import OrgQuotaUsage, OrgQuotaValues
```

Methods:

- `client.quotas.retrieve() -> OrgQuotaUsage`
