# Healthz

Methods:

- <code title="get /healthz">client.healthz.<a href="./src/fastvm/resources/healthz.py">check</a>() -> None</code>

# Livez

Methods:

- <code title="get /livez">client.livez.<a href="./src/fastvm/resources/livez.py">check</a>() -> None</code>

# Readyz

Methods:

- <code title="get /readyz">client.readyz.<a href="./src/fastvm/resources/readyz.py">check</a>() -> None</code>

# Vms

Types:

```python
from fastvm.types import (
    DeleteResponse,
    VmInstance,
    VmListResponse,
    VmExecuteCommandResponse,
    VmIssueConsoleTokenResponse,
)
```

Methods:

- <code title="post /v1/vms">client.vms.<a href="./src/fastvm/resources/vms/vms.py">create</a>(\*\*<a href="src/fastvm/types/vm_create_params.py">params</a>) -> <a href="./src/fastvm/types/vm_instance.py">VmInstance</a></code>
- <code title="get /v1/vms/{id}">client.vms.<a href="./src/fastvm/resources/vms/vms.py">retrieve</a>(id) -> <a href="./src/fastvm/types/vm_instance.py">VmInstance</a></code>
- <code title="get /v1/vms">client.vms.<a href="./src/fastvm/resources/vms/vms.py">list</a>() -> <a href="./src/fastvm/types/vm_list_response.py">VmListResponse</a></code>
- <code title="delete /v1/vms/{id}">client.vms.<a href="./src/fastvm/resources/vms/vms.py">delete</a>(id) -> <a href="./src/fastvm/types/delete_response.py">DeleteResponse</a></code>
- <code title="post /v1/vms/{id}/exec">client.vms.<a href="./src/fastvm/resources/vms/vms.py">execute_command</a>(id, \*\*<a href="src/fastvm/types/vm_execute_command_params.py">params</a>) -> <a href="./src/fastvm/types/vm_execute_command_response.py">VmExecuteCommandResponse</a></code>
- <code title="post /v1/vms/{id}/console-token">client.vms.<a href="./src/fastvm/resources/vms/vms.py">issue_console_token</a>(id) -> <a href="./src/fastvm/types/vm_issue_console_token_response.py">VmIssueConsoleTokenResponse</a></code>
- <code title="patch /v1/vms/{id}">client.vms.<a href="./src/fastvm/resources/vms/vms.py">rename</a>(id, \*\*<a href="src/fastvm/types/vm_rename_params.py">params</a>) -> <a href="./src/fastvm/types/vm_instance.py">VmInstance</a></code>

## Firewall

Types:

```python
from fastvm.types.vms import FirewallPolicy, FirewallRule
```

Methods:

- <code title="patch /v1/vms/{id}/firewall">client.vms.firewall.<a href="./src/fastvm/resources/vms/firewall.py">patch_policy</a>(id, \*\*<a href="src/fastvm/types/vms/firewall_patch_policy_params.py">params</a>) -> <a href="./src/fastvm/types/vm_instance.py">VmInstance</a></code>
- <code title="put /v1/vms/{id}/firewall">client.vms.firewall.<a href="./src/fastvm/resources/vms/firewall.py">replace_policy</a>(id, \*\*<a href="src/fastvm/types/vms/firewall_replace_policy_params.py">params</a>) -> <a href="./src/fastvm/types/vm_instance.py">VmInstance</a></code>

## Console

Methods:

- <code title="get /v1/vms/{id}/console/ws">client.vms.console.<a href="./src/fastvm/resources/vms/console.py">websocket</a>(id, \*\*<a href="src/fastvm/types/vms/console_websocket_params.py">params</a>) -> None</code>

# Snapshots

Types:

```python
from fastvm.types import SnapshotObject, SnapshotListResponse
```

Methods:

- <code title="post /v1/snapshots">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">create</a>(\*\*<a href="src/fastvm/types/snapshot_create_params.py">params</a>) -> <a href="./src/fastvm/types/snapshot_object.py">SnapshotObject</a></code>
- <code title="patch /v1/snapshots/{id}">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">update</a>(id, \*\*<a href="src/fastvm/types/snapshot_update_params.py">params</a>) -> <a href="./src/fastvm/types/snapshot_object.py">SnapshotObject</a></code>
- <code title="get /v1/snapshots">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">list</a>() -> <a href="./src/fastvm/types/snapshot_list_response.py">SnapshotListResponse</a></code>
- <code title="delete /v1/snapshots/{id}">client.snapshots.<a href="./src/fastvm/resources/snapshots.py">delete</a>(id) -> <a href="./src/fastvm/types/delete_response.py">DeleteResponse</a></code>

# Org

Types:

```python
from fastvm.types import OrgQuotaValues, OrgRetrieveQuotasResponse
```

Methods:

- <code title="get /v1/org/quotas">client.org.<a href="./src/fastvm/resources/org.py">retrieve_quotas</a>() -> <a href="./src/fastvm/types/org_retrieve_quotas_response.py">OrgRetrieveQuotasResponse</a></code>
