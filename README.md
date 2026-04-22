# FastVM Python SDK & CLI

[PyPI version](https://pypi.org/project/fastvm/)

Async/sync Python SDK and CLI for the [FastVM](https://fastvm.org) microVM
platform. Launch, snapshot, and exec on Linux microVMs over HTTP/2.

The typed SDK surface is [generated with Stainless](https://www.stainless.com/)
from our [OpenAPI spec](https://github.com/fastvm-org/fastvm-mono/blob/main/api/openapi.yaml);
a thin `[fastvm.lib](src/fastvm/lib/)` module layers on polling, unified file
transfer, HTTP/2, and a `click`-based CLI.

## Installation

```sh
pip install fastvm
# or
uv add fastvm
```

For CLI-only use:

```sh
pipx install fastvm
# or
uv tool install fastvm
```

## Quick start — CLI

```sh
# One-time: authenticate (env var or persisted config)
export FASTVM_API_KEY=your-key
# or:
fastvm config set api_key your-key

# Launch a VM and open an interactive console
fastvm launch --name dev --console

# List, exec, console
fastvm vm ls
fastvm vm exec <vm-id> "uname -a"
fastvm vm console <vm-id>

# Ephemeral: launch → run → destroy
fastvm run "apt update && python3 --version"

# Snapshots + restore
fastvm snapshot create <vm-id> --name my-snap
fastvm snapshot restore <snap-id> --console

# Firewall + quotas
fastvm firewall set <vm-id> --mode restricted -r tcp:22 -r tcp:80
fastvm quota
```

`fastvm --help` has the full reference.

## Quick start — SDK

Two classes ship in the top-level `fastvm` namespace:


| Class                                | What you get                                                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `Fastvm` / `AsyncFastvm`             | Raw generated client — full typed surface, nothing extra.                                                    |
| `FastvmClient` / `AsyncFastvmClient` | Same surface + HTTP/2, `launch()` polling, `upload()`/`download()`, and shell-string auto-wrap on `vms.run`. |


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

Synchronous equivalent:

```python
from fastvm import FastvmClient

with FastvmClient() as client:
    vm = client.launch(machine_type="c1m2")
    result = client.vms.run(vm.id, command="echo hi")
    print(result.stdout)
    client.vms.delete(vm.id)
```

### Environment variables


| Variable          | Purpose                                        |
| ----------------- | ---------------------------------------------- |
| `FASTVM_API_KEY`  | Sent as `X-API-Key` on every request.          |
| `FASTVM_BASE_URL` | Override the default `https://api.fastvm.org`. |


## What `FastvmClient` adds

- **HTTP/2 by default.** Enabled transparently; set `http2=False` in the
constructor or pass your own `http_client=` to override.
- `**launch()` polls.** Wraps `POST /v1/vms` and waits for `status == running`;
raises `VMLaunchError` on terminal failure and `VMNotReadyError` on timeout.
- `**upload(vm_id, local, remote)` / `download(vm_id, remote, local)`.**
Unified file/dir transfer. File vs. directory is detected automatically
(local `isdir` check on upload, VM-side `test -d` on download). Directory
transfers stream a gzipped tar through the presigned storage URL.
- **Shell strings on `vms.run`.** `client.vms.run(id, command="ls -la")` is
auto-wrapped into `["sh", "-c", "ls -la"]` — guards the Python footgun
where a `str` iterates into characters when a `Sequence[str]` is expected.
Passing an argv list is still the recommended form for untrusted input.

Everything else (`client.vms.retrieve`, `client.snapshots.list`, firewall,
quotas, raw `vms.files.presign` / `vms.files.fetch`) is the untouched
generated surface.

## Raw generated client

If you don't want any of the above, use `Fastvm` / `AsyncFastvm` directly. The
full generated reference lives in `[api.md](api.md)`, and all params/response
shapes are fully typed — `pyright` and `mypy` strict both pass against the
library.

## Errors

```python
from fastvm import (
    FastvmClient,
    VMLaunchError, VMNotReadyError, VMExecError, FileTransferError,  # from fastvm.lib
    APIStatusError, BadRequestError, RateLimitError,                  # generated
)
```

HTTP errors raised by the raw client (`APIStatusError` subclasses) are never
re-wrapped by the `fastvm.lib` helpers — you can still `except RateLimitError`
on a `client.launch()` call.

## Retries

The generated client retries idempotent requests (`GET`, `PUT`) by default.
Non-idempotent endpoints (`POST /v1/vms`, `POST /v1/vms/{id}/exec`,
`POST /v1/snapshots`) are configured with **no auto-retry** to avoid duplicate
side effects — retry those explicitly if you need to.

## Custom code + regeneration

Anything under `[src/fastvm/lib/](src/fastvm/lib/)` is hand-written and
survives Stainless regenerations. See `[CUSTOM_CODE.md](CUSTOM_CODE.md)` for
the full list and rationale.

## License

Apache-2.0