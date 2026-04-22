# FastVM Python SDK & CLI

[PyPI version](https://pypi.org/project/fastvm/)

Async/sync Python SDK and CLI for the [FastVM](https://fastvm.org) microVM
platform. Launch, snapshot, and run commands on Linux microVMs over HTTP/2.

## Installation

```sh
pip install fastvm
# or
uv add fastvm
```

CLI-only install (puts `fastvm` on your PATH, isolated from your project env):

```sh
pipx install fastvm
# or
uv tool install fastvm
```

## CLI quick start

```sh
# One-time auth (or export FASTVM_API_KEY)
fastvm config set api_key your-key

# Launch a VM and open an interactive console
fastvm launch --name dev --console

# List, inspect, exec
fastvm vm ls
fastvm vm get dev
fastvm vm exec dev "uname -a"

# Ephemeral one-shot: launch → run → destroy
fastvm run "apt-get update && python3 --version"

# Snapshots
fastvm snapshot create dev --name my-snap
fastvm snapshot restore my-snap --console

# Firewall
fastvm firewall set dev --mode restricted -r tcp:22 -r tcp:80

# Quotas
fastvm quota
```

VMs and snapshots can be referenced by full ID, short ID prefix, or name.
Run `fastvm --help` for the full command reference.

Enable shell completion (one-time):

```sh
# bash
eval "$(_FASTVM_COMPLETE=bash_source fastvm)"
# zsh
eval "$(_FASTVM_COMPLETE=zsh_source fastvm)"
```

## SDK quick start

```python
import asyncio
from fastvm import AsyncFastvmClient

async def main():
    async with AsyncFastvmClient() as client:          # reads FASTVM_API_KEY
        vm = await client.launch(machine_type="c1m2")  # waits until running
        await client.upload(vm.id, "./src", "/root/src")

        result = await client.vms.run(vm.id, command="python3 /root/src/main.py")
        print(result.stdout)

        await client.download(vm.id, "/root/out.log", "./out.log")
        await client.vms.delete(vm.id)

asyncio.run(main())
```

Synchronous client:

```python
from fastvm import FastvmClient

with FastvmClient() as client:
    vm = client.launch(machine_type="c1m2")
    print(client.vms.run(vm.id, command="echo hi").stdout)
    client.vms.delete(vm.id)
```

### Environment variables


| Variable          | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| `FASTVM_API_KEY`  | Sent as `X-API-Key` on every request.           |
| `FASTVM_BASE_URL` | Overrides the default `https://api.fastvm.org`. |


## API overview


| Method                                                              | Description                               |
| ------------------------------------------------------------------- | ----------------------------------------- |
| `client.launch(...)`                                                | Launch a VM and wait for `status=running` |
| `client.vms.retrieve(id)` / `client.vms.list()`                     | Inspect existing VMs                      |
| `client.vms.run(id, command=...)`                                   | Execute a command on a VM                 |
| `client.vms.update(id, name=...)`                                   | Rename a VM                               |
| `client.vms.delete(id)`                                             | Delete a VM                               |
| `client.upload(vm_id, local, remote)`                               | Upload file or directory to a VM          |
| `client.download(vm_id, remote, local)`                             | Download file or directory from a VM      |
| `client.snapshots.create(vm_id=..., name=...)`                      | Create a point-in-time snapshot           |
| `client.snapshots.list()` / `.delete(id)` / `.update(id, name=...)` | Manage snapshots                          |
| `client.vms.set_firewall(id, ...)` / `.patch_firewall(id, ...)`     | Configure IPv6 ingress                    |
| `client.vms.console_token(id)`                                      | Request a WebSocket console session token |
| `client.quotas.retrieve()`                                          | Fetch organization quota usage            |


`launch(snapshot_id=...)` also works — it's how the CLI's `snapshot restore`
is implemented. `client.vms.run(id, command="ls -la")` auto-wraps shell
strings into `["sh", "-c", "ls -la"]`; argv lists are passed through as-is.

Requests retry idempotent failures (connection errors, 408/409/429, 5xx) with
exponential backoff by default. Non-idempotent POSTs (`launch`, `vms.run`,
`snapshots.create`) retry 0 times by default to avoid duplicate side effects;
override per-call with `extra_headers=...` / `timeout=...` / your own retry
loop.

## Errors

```python
from fastvm import (
    FastvmClient,
    VMLaunchError, VMNotReadyError, VMExecError, FileTransferError,
    APIStatusError, NotFoundError, RateLimitError, AuthenticationError,
)
```

`VMLaunchError` / `VMNotReadyError` come from `client.launch(...)` when a VM
enters a terminal failure state or the poll deadline expires. HTTP errors
(`APIStatusError` and friends) surface untouched from any call that hits the
server.

## Documentation

Full API reference: [https://fastvm.org/docs](https://fastvm.org/docs).

## License

Apache-2.0