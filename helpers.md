# FastVM CLI and custom helpers

The auto-generated `README.md` covers the generated SDK surface (every REST
method, authentication, errors, retries, timeouts, logging, pagination, raw
HTTP, versioning). This file documents everything that sits **on top of**
the generated client:

- The `fastvm` command-line tool
- A handful of Python ergonomic helpers (`launch()`, `upload()`, `download()`,
shell-string auto-wrap on `vms.run`)

All of this lives in `[src/fastvm/lib/](src/fastvm/lib/)` and is re-exported
from the top-level `fastvm` package. See
`[fastvm-mono/CUSTOM_CODE.md](https://github.com/fastvm-org/fastvm-mono/blob/main/CUSTOM_CODE.md)`
for the rationale and full inventory.

---

## CLI

```sh
pip install fastvm         # or: uv add fastvm / pipx install fastvm

fastvm config set api_key your-key     # or export FASTVM_API_KEY

fastvm launch --name dev --console     # boot a VM, open a console
fastvm vm ls
fastvm vm exec dev "uname -a"
fastvm run "apt-get update && python3 --version"   # ephemeral one-shot

fastvm snapshot create dev --name my-snap
fastvm snapshot restore my-snap --console

fastvm firewall set dev --mode restricted -r tcp:22 -r tcp:80
fastvm quota
```

VMs and snapshots resolve by full ID, short ID prefix, or name.
`fastvm --help` covers every command.

Shell completion (one-time):

```sh
eval "$(_FASTVM_COMPLETE=bash_source fastvm)"   # or zsh_source
```

---

## Python helpers

Two convenience clients ship alongside the generated `Fastvm` / `AsyncFastvm`:

```python
from fastvm import FastvmClient, AsyncFastvmClient
```

### `client.launch(...)` — create a VM and wait for `status=running`

`POST /v1/vms` returns `201 running` for immediate boots or `202` for queued
VMs. `launch()` wraps `vms.launch(...)` and polls `vms.retrieve()` until the
VM is ready.

```python
vm = client.launch(machine_type="c1m2", poll_interval=2.0, timeout=300)
# raises VMLaunchError on terminal status (error, stopped, deleting)
# raises VMNotReadyError on timeout
# pass wait=False to return the initial (possibly-queued) VM immediately
```

Restore from snapshot: `client.launch(snapshot_id="snp_…")`.

### `client.upload(vm_id, local, remote)` / `client.download(vm_id, remote, local)`

Unified file/directory transfer over the existing GCS-presigned-URL
primitives (`vms.files.presign` + `vms.files.fetch` + `vms.run`).

```python
client.upload(vm.id, "./src", "/root/src")         # dir → tar + presign + VM extract
client.upload(vm.id, "./config.toml", "/etc/app.toml")  # file → presign + PUT + fetch
client.download(vm.id, "/root/out.log", "./out.log")    # file → presign + VM curl
client.download(vm.id, "/var/log", "./logs-back")       # dir → VM tar + download + extract
```

Directory vs file is auto-detected (`isdir` locally, `test -d` VM-side). If
you prefer manual control you can call `vms.files.presign` / `vms.files.fetch`
directly — they're fully documented in the generated `api.md`.

### Shell-string auto-wrap on `vms.run`

Python silently iterates a `str` into characters when a `Sequence[str]` is
expected. `FastvmClient.vms.run(id, command="ls -la")` is auto-wrapped into
`["sh", "-c", "ls -la"]` to guard that footgun. Argv lists pass through
unchanged.

### HTTP/2 by default

`FastvmClient` / `AsyncFastvmClient` configure `httpx.Client(http2=True)` by
default. Override with `http2=False` or pass your own `http_client=`.

### Error types

Every SDK error — generated HTTP errors *and* the three helper errors below —
subclasses the same `fastvm.FastvmError` root, so one `except` catches
everything from the client:

```python
from fastvm import FastvmError  # catches everything
```

The three helper-only errors cover failure modes the generated
`APIStatusError` hierarchy can't model (success HTTP response with a
failure payload, client-side polling deadlines, out-of-band GCS /
local-tar failures):

```python
from fastvm import VMLaunchError, VMNotReadyError, FileTransferError
```

- `VMLaunchError` — VM reached a terminal failure status (`error` /
`stopped` / `deleting`) during `launch()` polling. Not an HTTP error;
`GET /v1/vms/{id}` returned 200 OK with a bad status in the body.
- `VMNotReadyError` — `launch()` polling deadline exceeded. Also subclasses
stdlib `TimeoutError`, so `except TimeoutError` works too.
- `FileTransferError` — any failure during `upload()` / `download()` that
isn't a Fastvm HTTP error: GCS PUT/GET failures, local `tarfile`
errors, size-limit violations, or VM-side `tar`/`curl` exits. When
caused by a VM-side command, the original `ExecResult` is available on
`err.exec_result` for stderr / exit code inspection.

Regular HTTP 4xx/5xx from any method (helpers or generated) still
surfaces as `APIStatusError` (or `NotFoundError`, `RateLimitError`,
`AuthenticationError`, etc.) untouched.