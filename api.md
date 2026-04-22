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

- <code title="get /healthz">client.<a href="./src/fastvm/_client.py">health</a>() -> <a href="./src/fastvm/types/health_response.py">HealthResponse</a></code>

# Vms

Types:

```python
from fastvm.types import ConsoleToken, ExecResult, Vm, VmListResponse, VmDeleteResponse
```

Methods:

- <code title="get /v1/vms/{id}">client.vms.<a href="./src/fastvm/resources/vms/vms.py">retrieve</a>(id) -> <a href="./src/fastvm/types/vm.py">Vm</a></code>
- <code title="patch /v1/vms/{id}">client.vms.<a href="./src/fastvm/resources/vms/vms.py">update</a>(id, \*\*<a href="src/fastvm/types/vm_update_params.py">params</a>) -> <a href="./src/fastvm/types/vm.py">Vm</a></code>
- <code title="get /v1/vms">client.vms.<a href="./src/fastvm/resources/vms/vms.py">list</a>() -> <a href="./src/fastvm/types/vm_list_response.py">VmListResponse</a></code>
- <code title="delete /v1/vms/{id}">client.vms.<a href="./src/fastvm/resources/vms/vms.py">delete</a>(id) -> <a href="./src/fastvm/types/vm_delete_response.py">VmDeleteResponse</a></code>
- <code title="post /v1/vms/{id}/console-token">client.vms.<a href="./src/fastvm/resources/vms/vms.py">console_token</a>(id) -> <a href="./src/fastvm/types/console_token.py">ConsoleToken</a></code>
- <code title="post /v1/vms">client.vms.<a href="./src/fastvm/resources/vms/vms.py">launch</a>(\*\*<a href="src/fastvm/types/vm_launch_params.py">params</a>) -> <a href="./src/fastvm/types/vm.py">Vm</a></code>
- <code title="patch /v1/vms/{id}/firewall">client.vms.<a href="./src/fastvm/resources/vms/vms.py">patch_firewall</a>(id, \*\*<a href="src/fastvm/types/vm_patch_firewall_params.py">params</a>) -> <a href="./src/fastvm/types/vm.py">Vm</a></code>
- <code title="post /v1/vms/{id}/exec">client.vms.<a href="./src/fastvm/resources/vms/vms.py">run</a>(id, \*\*<a href="src/fastvm/types/vm_run_params.py">params</a>) -> <a href="./src/fastvm/types/exec_result.py">ExecResult</a></code>
- <code title="put /v1/vms/{id}/firewall">client.vms.<a href="./src/fastvm/resources/vms/vms.py">set_firewall</a>(id, \*\*<a href="src/fastvm/types/vm_set_firewall_params.py">params</a>) -> <a href="./src/fastvm/types/vm.py">Vm</a></code>

## Files

Types:

```python
from fastvm.types.vms import PresignResponse
```

Methods:

- <code title="post /v1/vms/{id}/files/fetch">client.vms.files.<a href="./src/fastvm/resources/vms/files.py">fetch</a>(id, \*\*<a href="src/fastvm/types/vms/file_fetch_params.py">params</a>) -> <a href="./src/fastvm/types/exec_result.py">ExecResult</a></code>
- <code title="post /v1/vms/{id}/files/presign">client.vms.files.<a href="./src/fastvm/resources/vms/files.py">presign</a>(id, \*\*<a href="src/fastvm/types/vms/file_presign_params.py">params</a>) -> <a href="./src/fastvm/types/vms/presign_response.py">PresignResponse</a></code>

# Snapshots

Types:

```python
from fastvm.types import Snapshot, SnapshotListResponse, SnapshotDeleteResponse
```

Methods:

- <code title="post /v1/snapshots">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">create</a>(\*\*<a href="src/fastvm/types/snapshot_create_params.py">params</a>) -> <a href="./src/fastvm/types/snapshot.py">Snapshot</a></code>
- <code title="patch /v1/snapshots/{id}">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">update</a>(id, \*\*<a href="src/fastvm/types/snapshot_update_params.py">params</a>) -> <a href="./src/fastvm/types/snapshot.py">Snapshot</a></code>
- <code title="get /v1/snapshots">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">list</a>() -> <a href="./src/fastvm/types/snapshot_list_response.py">SnapshotListResponse</a></code>
- <code title="delete /v1/snapshots/{id}">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">delete</a>(id) -> <a href="./src/fastvm/types/snapshot_delete_response.py">SnapshotDeleteResponse</a></code>

# Quotas

Types:

```python
from fastvm.types import OrgQuotaUsage, OrgQuotaValues
```

Methods:

- <code title="get /v1/org/quotas">client.quotas.<a href="./src/fastvm/resources/quotas.py">retrieve</a>() -> <a href="./src/fastvm/types/org_quota_usage.py">OrgQuotaUsage</a></code>
