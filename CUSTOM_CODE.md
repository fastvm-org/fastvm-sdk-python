# Custom code in this repo

Everything in `src/fastvm/lib/` and `src/fastvm/cli/` is hand-written and will
not be touched by Stainless on regeneration (per the `lib/` convention
documented in `CONTRIBUTING.md`). The rest of `src/fastvm/` is generated.

This file tracks **what** is custom and **why**, so the next person to open the
repo doesn't have to reverse-engineer it.

## Paths and owners


| Path                             | Purpose                                                                                                                                                                                        |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/fastvm/lib/_client.py`      | `FastvmClient` / `AsyncFastvmClient` — subclass the generated `Fastvm` / `AsyncFastvm` with helper methods.                                                                                    |
| `src/fastvm/lib/_errors.py`      | `VMLaunchError`, `VMNotReadyError`, `VMExecError`, `FileTransferError`. Raised only by helpers — HTTP errors still come through the generated `APIStatusError` hierarchy.                      |
| `src/fastvm/lib/_tarutil.py`     | Streaming gzip-tar pack/unpack for directory upload/download. Pure stdlib `tarfile`; used via `asyncio.to_thread` on the async path.                                                           |
| `src/fastvm/lib/__init__.py`     | Re-exports the classes above.                                                                                                                                                                  |
| `src/fastvm/lib/cli/*.py`        | `click`-based CLI — entry point `fastvm` (see `[project.scripts]`).                                                                                                                            |
| `src/fastvm/__init__.py` (patch) | Adds `FastvmClient`, `AsyncFastvmClient`, and the custom error types to the top-level namespace. Manual edit on top of the generated file; regen merges preserve it (with possible conflicts). |
| `pyproject.toml` (patches)       | Added deps: `click`, `tabulate`, `websockets`, `tomli` (py < 3.11), and the `[http2]` extra on httpx. Added `[project.scripts] fastvm = "fastvm.lib.cli:main"`.                                |
| `tests/offline/`, `tests/live/`  | Workflow-style tests (see `tests/README.md`).                                                                                                                                                  |


## Customizations by category

### HTTP/2 client (sync + async)

Stainless's default client is HTTP/1.1. `FastvmClient.__init__` constructs an
`httpx.Client(http2=True, ...)` (and `AsyncClient` on the async side) with the
same timeout / limits / follow-redirects defaults Stainless uses internally.
Users who pass their own `http_client=` keep control; users who pass
`http2=False` get HTTP/1.1. This matters for multiplexed VM streams (exec +
files) over a warm connection.

Dependency: `httpx[http2]` pulls in `h2` + `hpack`.

### `launch()` polling

`POST /v1/vms` returns `201` (running) or `202` (queued). The raw
`client.vms.launch()` returns the initial VM regardless. `FastvmClient.launch()`
polls `GET /v1/vms/{id}` with jittered backoff until `status == "running"`,
with configurable `poll_interval` (default 2s) and `timeout` (default 300s).

Terminal failure statuses (`error`, `stopped`, `deleting`) raise
`VMLaunchError`; deadline exceeded raises `VMNotReadyError`. Pass `wait=False`
to skip polling entirely and mirror the raw call.

`wait_for_vm_ready(vm_id, ...)` is exposed separately for users who kicked off
a launch via the raw client.

### Unified `upload()` / `download()`

The API exposes only primitives:

- `vms.files.presign(vm_id, path=...)` — mints signed GCS URLs (both upload
and download directions) + a `max_upload_bytes` ceiling.
- `vms.files.fetch(vm_id, url=..., path=..., timeout_sec=...)` — tells the VM
to pull a URL into a guest path.
- `vms.run(vm_id, command=..., timeout_sec=...)` — used for `tar` / `curl`.

`FastvmClient.upload(vm_id, local, remote)` dispatches:

- **File:** `presign` → client PUT → `fetch`.
- **Dir:** `presign` → client streams `tar czf` → `fetch` staging tar → VM
extracts with `tar xzf` → VM removes tar.

`FastvmClient.download(vm_id, remote, local)` runs one VM-side exec first to
classify `remote` (`test -e` + `test -d`); missing paths raise
`FileNotFoundError`. Then:

- **File:** presign → VM `curl -T` to the signed upload URL → client streams
the download URL to disk.
- **Dir:** presign → VM `tar czf - -C <dir> . | curl -T -` → client streams
the download URL into `tarfile.extractall(filter="data")`.

Tar contents are rooted at `./` (not the directory's basename), so upload and
download are symmetric — no `--strip-components` gymnastics.

Signed storage URLs bypass the SDK's configured `X-API-Key` header (GCS
rejects extra headers); `_client.py` spins up short-lived `httpx` clients with
long read/write timeouts for these transfers.

### Shell-string auto-wrap on `vms.run`

Python is one of the few languages where passing a `str` to a `Sequence[str]`
parameter silently iterates into characters instead of raising. The API
requires an argv array (`["sh", "-c", "ls -la"]`), so the common intuitive
call `client.vms.run(id, command="ls -la")` is a silent bug.

`FastvmClient` overrides the `vms` cached property to return `_VmsResourceExt`,
which accepts `str | Sequence[str]` on `run()` and wraps strings into
`["sh", "-c", ...]` before forwarding. Argv-style calls still work unchanged.

This is a Python-only fix; the TypeScript SDK does not need it.

### CLI

`src/fastvm/lib/cli/` ports the old internal CLI to the generated client:

- Top-level shortcuts: `fastvm launch`, `rm`, `exec`, `run`, `console`.
- Subcommand groups: `vm`, `snapshot`, `firewall`, `quota`, `config`.
- Persistent config at `$XDG_CONFIG_HOME/fastvm/config.toml` (API key, base URL).
- Interactive console via WebSocket (`_console.py`), using the generated
`vms.console_token()` call.
- Async-only under the hood — all commands open an `AsyncFastvmClient` and
bridge to click via `asyncio.run`.

CLI is excluded from pyright strict mode (`[tool.pyright]` `exclude` in
`pyproject.toml`) because click + pydantic `model_dump()` interactions are
noisy in strict mode; the core library still type-checks strict.

### Top-level re-export

`src/fastvm/__init__.py` is generated, but we've added:

```python
from .lib import (
    FastvmClient, AsyncFastvmClient,
    VMLaunchError, VMNotReadyError, VMExecError, FileTransferError,
)
```

and appended their names to `__all__`. Stainless preserves manual edits to
generated files across regens, with potential merge conflicts on future
generations — keep an eye on the top of the file on re-sync.

## When adding more custom code

1. Prefer new files in `src/fastvm/lib/` over editing generated ones.
2. If you touch `src/fastvm/__init__.py` or `pyproject.toml`, record it in
  the table above.
3. Keep pyright + mypy strict passing against `src/fastvm/lib/` (CLI dir is
  excluded). Run:

