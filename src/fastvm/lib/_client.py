"""``FastvmClient`` / ``AsyncFastvmClient`` — ergonomic wrappers over the generated client.

Layers three things on top of the raw Stainless output:

1. **HTTP/2 by default.** The generated ``httpx.Client`` is HTTP/1.1 only; we
   pre-configure an ``http2=True`` client unless the user passes their own.

2. **``launch()`` polling.** ``POST /v1/vms`` can return 201 (already running)
   or 202 (queued). We wait for ``status=running`` with jittered backoff and
   terminal-status detection.

3. **``upload()`` / ``download()``.** Raw file endpoints expose presigned URLs
   + ``fetch`` + ``run``; users think in ``(vm_id, local_path, remote_path)``.
   One call dispatches to file-or-directory based on what's actually there.

4. **Shell-string safety net.** ``client.vms.run(id, command="ls -la")`` in
   Python would iterate the string into characters (silent footgun). We accept
   ``str`` on ``vms.run`` and auto-wrap into ``["sh", "-c", ...]``.
"""

from __future__ import annotations

import os
import time
import shlex
import random
import asyncio
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    List,
    Union,
    BinaryIO,
    Iterator,
    Optional,
    Sequence,
    AsyncIterator,
    cast,
)

import httpx

from ._errors import VMExecError, VMLaunchError, VMNotReadyError, FileTransferError
from .._client import Fastvm, AsyncFastvm
from .._compat import cached_property
from ._tarutil import pack_directory_to_stream, unpack_stream_to_directory
from ..types.vm import Vm
from .._base_client import DEFAULT_TIMEOUT, DEFAULT_CONNECTION_LIMITS
from ..resources.vms.vms import VmsResource, AsyncVmsResource
from ..types.exec_result import ExecResult

if TYPE_CHECKING:
    from ..types.vms.presign_response import PresignResponse

__all__ = ["FastvmClient", "AsyncFastvmClient"]


# --------------------------------------------------------------------------- #
#                                 Constants                                   #
# --------------------------------------------------------------------------- #

# VM statuses that mean "give up, won't become runnable". Any other non-
# ``running`` value is treated as transitional (per spec: unknown statuses
# should be considered in-transition).
_TERMINAL_FAILURE = {"error", "stopped", "deleting"}
_RUNNING = "running"

# GCS signed URLs are signed against a specific Content-Type; the client PUT
# and the VM-side ``curl -T`` must both use this exact value.
_PUT_CONTENT_TYPE = "application/octet-stream"

# Separate timeouts for storage ops — large file transfers legitimately take
# minutes, much longer than the scheduler client's default timeout.
_STORAGE_HTTP_TIMEOUT = httpx.Timeout(connect=15.0, read=900.0, write=900.0, pool=15.0)

# Where tarballs land inside the VM during directory transfers.
_VM_STAGE_DIR = "/tmp"


# --------------------------------------------------------------------------- #
#                          vms.run shell-string patch                         #
# --------------------------------------------------------------------------- #


def _wrap_shell_command(command: Union[str, Sequence[str]]) -> List[str]:
    """Accept either argv or a shell string; emit argv.

    Guards against the Python-only footgun where passing a ``str`` to a
    ``Sequence[str]`` parameter iterates into characters. If the user meant a
    shell command, wrap it in ``["sh", "-c", ...]`` — the explicit form.
    """
    if isinstance(command, str):
        return ["sh", "-c", command]
    return list(command)


class _VmsResourceExt(VmsResource):
    """``VmsResource`` whose ``run()`` accepts ``str`` *or* ``Sequence[str]``."""

    def run(  # type: ignore[override]
        self,
        id: str,
        *,
        command: Union[str, Sequence[str]],
        timeout_sec: Optional[int] = None,
        **kwargs: Any,
    ) -> ExecResult:
        if timeout_sec is not None:
            kwargs["timeout_sec"] = timeout_sec
        return super().run(id, command=_wrap_shell_command(command), **kwargs)


class _AsyncVmsResourceExt(AsyncVmsResource):
    """Async twin of :class:`_VmsResourceExt`."""

    async def run(  # type: ignore[override]
        self,
        id: str,
        *,
        command: Union[str, Sequence[str]],
        timeout_sec: Optional[int] = None,
        **kwargs: Any,
    ) -> ExecResult:
        if timeout_sec is not None:
            kwargs["timeout_sec"] = timeout_sec
        return await super().run(id, command=_wrap_shell_command(command), **kwargs)


# --------------------------------------------------------------------------- #
#                              Sync client                                    #
# --------------------------------------------------------------------------- #


class FastvmClient(Fastvm):
    """Drop-in replacement for :class:`fastvm.Fastvm` with ergonomic helpers.

    Example::

        from fastvm import FastvmClient

        with FastvmClient() as client:
            vm = client.launch(machine_type="c1m2")
            client.upload(vm.id, "./src", "/root/src")
            out = client.vms.run(vm.id, command="ls -la /root")
            client.download(vm.id, "/root/out.log", "./out.log")
    """

    def __init__(
        self,
        *args: Any,
        http_client: Optional[httpx.Client] = None,
        http2: bool = True,
        **kwargs: Any,
    ) -> None:
        # If the user didn't supply their own ``http_client``, build one with
        # HTTP/2 enabled. Stainless's default is HTTP/1.1; HTTP/2 gives us
        # multiplexing + header compression on the amortized TLS connection.
        if http_client is None and http2:
            http_client = httpx.Client(
                http2=True,
                timeout=DEFAULT_TIMEOUT,
                limits=DEFAULT_CONNECTION_LIMITS,
                follow_redirects=True,
            )
        super().__init__(*args, http_client=http_client, **kwargs)

    @cached_property
    def vms(self) -> _VmsResourceExt:  # type: ignore[override]
        # Override Stainless's ``vms`` property so ``client.vms.run`` accepts
        # shell strings in addition to argv arrays.
        return _VmsResourceExt(self)

    # --------------------------- VM lifecycle ---------------------------- #

    def launch(
        self,
        *,
        wait: bool = True,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        **params: Any,
    ) -> Vm:
        """``POST /v1/vms`` and (by default) poll until the VM is running.

        All other kwargs forward to :meth:`VmsResource.launch`.

        ``wait=False`` returns the initial VM even if it's still provisioning —
        matches the raw generated call. ``timeout`` caps the total polling time
        in seconds.

        Raises:
          VMLaunchError: VM reached a terminal failure status.
          VMNotReadyError: did not reach ``running`` within ``timeout``.
        """
        vm = self.vms.launch(**params)
        if not wait or vm.status == _RUNNING:
            return vm
        return self.wait_for_vm_ready(vm.id, poll_interval=poll_interval, timeout=timeout)

    def wait_for_vm_ready(
        self,
        vm_id: str,
        *,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Vm:
        """Poll ``GET /v1/vms/{id}`` until status is ``running`` or terminal."""
        deadline = time.monotonic() + timeout
        last_status = "unknown"
        while True:
            vm = self.vms.retrieve(vm_id)
            last_status = vm.status
            if vm.status == _RUNNING:
                return vm
            if vm.status in _TERMINAL_FAILURE:
                raise VMLaunchError(vm_id, vm.status)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise VMNotReadyError(vm_id, last_status, timeout)
            time.sleep(min(_poll_delay(poll_interval, remaining), remaining))

    # --------------------------- File transfer --------------------------- #

    def upload(
        self,
        vm_id: str,
        local_path: str,
        remote_path: str,
        *,
        fetch_timeout_sec: int = 600,
        exec_timeout_sec: int = 600,
    ) -> None:
        """Copy a file or directory from the client into the VM.

        Dispatches internally: if ``local_path`` is a directory, streams a
        gzipped tar to the VM and extracts into ``remote_path``; otherwise
        fetches the single file to ``remote_path`` directly.
        """
        local_path = os.path.abspath(local_path)
        if not os.path.exists(local_path):
            raise FileNotFoundError(local_path)
        if os.path.isdir(local_path):
            self._upload_dir(vm_id, local_path, remote_path, fetch_timeout_sec, exec_timeout_sec)
        else:
            self._upload_file(vm_id, local_path, remote_path, fetch_timeout_sec)

    def download(
        self,
        vm_id: str,
        remote_path: str,
        local_path: str,
        *,
        exec_timeout_sec: int = 600,
    ) -> None:
        """Copy a file or directory from the VM to the client.

        One extra VM-side ``test -d`` call classifies ``remote_path`` before
        dispatching. Cheap (~one exec round-trip) and avoids surprising the
        user with wrong layout semantics.
        """
        if self._vm_is_dir(vm_id, remote_path, exec_timeout_sec):
            self._download_dir(vm_id, remote_path, local_path, exec_timeout_sec)
        else:
            self._download_file(vm_id, remote_path, local_path, exec_timeout_sec)

    # ---- internal dispatch helpers -------------------------------------- #

    def _vm_is_dir(self, vm_id: str, remote_path: str, exec_timeout_sec: int) -> bool:
        # ``test -d`` exits 0 for dir, 1 for file/missing. ``test -e`` first so
        # we can raise a clear error for missing paths rather than silently
        # treating them as files.
        result = self.vms.run(
            vm_id,
            command=["sh", "-c", f"test -e {shlex.quote(remote_path)} || exit 2; test -d {shlex.quote(remote_path)}"],
            timeout_sec=exec_timeout_sec,
        )
        if result.exit_code == 2:
            raise FileNotFoundError(f"VM path does not exist: {remote_path}")
        return result.exit_code == 0

    def _upload_file(self, vm_id: str, local_path: str, remote_path: str, fetch_timeout_sec: int) -> None:
        size = _stat_size(local_path)
        presigned = self.vms.files.presign(vm_id, path=remote_path)
        _assert_under_limit(size, presigned)
        with open(local_path, "rb") as f:
            _http_put_stream(presigned.upload_url, f, size=size)
        self.vms.files.fetch(vm_id, url=presigned.download_url, path=remote_path, timeout_sec=fetch_timeout_sec)

    def _upload_dir(
        self, vm_id: str, local_dir: str, remote_dir: str, fetch_timeout_sec: int, exec_timeout_sec: int
    ) -> None:
        stage = _stage_tar_path("upload")
        presigned = self.vms.files.presign(vm_id, path=stage)
        _http_put_stream(presigned.upload_url, pack_directory_to_stream(local_dir))
        self.vms.files.fetch(vm_id, url=presigned.download_url, path=stage, timeout_sec=fetch_timeout_sec)
        extract = (
            f"set -eu; mkdir -p {shlex.quote(remote_dir)}; "
            f"tar xzf {shlex.quote(stage)} -C {shlex.quote(remote_dir)}; "
            f"rm -f {shlex.quote(stage)}"
        )
        _require_exec_ok(extract, self.vms.run(vm_id, command=extract, timeout_sec=exec_timeout_sec))

    def _download_file(self, vm_id: str, remote_path: str, local_path: str, exec_timeout_sec: int) -> None:
        presigned = self.vms.files.presign(vm_id, path=remote_path)
        cmd = (
            f"set -eu; curl --fail --silent --show-error -T {shlex.quote(remote_path)} "
            f"-H 'Content-Type: {_PUT_CONTENT_TYPE}' {shlex.quote(presigned.upload_url)}"
        )
        _require_exec_ok(cmd, self.vms.run(vm_id, command=cmd, timeout_sec=exec_timeout_sec))
        parent = os.path.dirname(os.path.abspath(local_path)) or "."
        os.makedirs(parent, exist_ok=True)
        _http_get_to_file(presigned.download_url, local_path)

    def _download_dir(self, vm_id: str, remote_dir: str, local_dir: str, exec_timeout_sec: int) -> None:
        presigned = self.vms.files.presign(vm_id, path=_stage_tar_path("download"))
        cmd = (
            f"set -eu; tar czf - -C {shlex.quote(remote_dir)} . | "
            f"curl --fail --silent --show-error -T - -H 'Content-Type: {_PUT_CONTENT_TYPE}' "
            f"{shlex.quote(presigned.upload_url)}"
        )
        _require_exec_ok(cmd, self.vms.run(vm_id, command=cmd, timeout_sec=exec_timeout_sec))
        os.makedirs(local_dir, exist_ok=True)
        _http_get_to_tar_extract(presigned.download_url, local_dir)


# --------------------------------------------------------------------------- #
#                              Async client                                   #
# --------------------------------------------------------------------------- #


class AsyncFastvmClient(AsyncFastvm):
    """Async twin of :class:`FastvmClient`."""

    def __init__(
        self,
        *args: Any,
        http_client: Optional[httpx.AsyncClient] = None,
        http2: bool = True,
        **kwargs: Any,
    ) -> None:
        if http_client is None and http2:
            http_client = httpx.AsyncClient(
                http2=True,
                timeout=DEFAULT_TIMEOUT,
                limits=DEFAULT_CONNECTION_LIMITS,
                follow_redirects=True,
            )
        super().__init__(*args, http_client=http_client, **kwargs)

    @cached_property
    def vms(self) -> _AsyncVmsResourceExt:  # type: ignore[override]
        return _AsyncVmsResourceExt(self)

    async def launch(
        self,
        *,
        wait: bool = True,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        **params: Any,
    ) -> Vm:
        vm = await self.vms.launch(**params)
        if not wait or vm.status == _RUNNING:
            return vm
        return await self.wait_for_vm_ready(vm.id, poll_interval=poll_interval, timeout=timeout)

    async def wait_for_vm_ready(
        self,
        vm_id: str,
        *,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Vm:
        deadline = time.monotonic() + timeout
        last_status = "unknown"
        while True:
            vm = await self.vms.retrieve(vm_id)
            last_status = vm.status
            if vm.status == _RUNNING:
                return vm
            if vm.status in _TERMINAL_FAILURE:
                raise VMLaunchError(vm_id, vm.status)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise VMNotReadyError(vm_id, last_status, timeout)
            await asyncio.sleep(min(_poll_delay(poll_interval, remaining), remaining))

    async def upload(
        self,
        vm_id: str,
        local_path: str,
        remote_path: str,
        *,
        fetch_timeout_sec: int = 600,
        exec_timeout_sec: int = 600,
    ) -> None:
        local_path = os.path.abspath(local_path)
        if not await asyncio.to_thread(os.path.exists, local_path):
            raise FileNotFoundError(local_path)
        if await asyncio.to_thread(os.path.isdir, local_path):
            await self._upload_dir(vm_id, local_path, remote_path, fetch_timeout_sec, exec_timeout_sec)
        else:
            await self._upload_file(vm_id, local_path, remote_path, fetch_timeout_sec)

    async def download(
        self,
        vm_id: str,
        remote_path: str,
        local_path: str,
        *,
        exec_timeout_sec: int = 600,
    ) -> None:
        if await self._vm_is_dir(vm_id, remote_path, exec_timeout_sec):
            await self._download_dir(vm_id, remote_path, local_path, exec_timeout_sec)
        else:
            await self._download_file(vm_id, remote_path, local_path, exec_timeout_sec)

    async def _vm_is_dir(self, vm_id: str, remote_path: str, exec_timeout_sec: int) -> bool:
        result = await self.vms.run(
            vm_id,
            command=["sh", "-c", f"test -e {shlex.quote(remote_path)} || exit 2; test -d {shlex.quote(remote_path)}"],
            timeout_sec=exec_timeout_sec,
        )
        if result.exit_code == 2:
            raise FileNotFoundError(f"VM path does not exist: {remote_path}")
        return result.exit_code == 0

    async def _upload_file(self, vm_id: str, local_path: str, remote_path: str, fetch_timeout_sec: int) -> None:
        size = await asyncio.to_thread(_stat_size, local_path)
        presigned = await self.vms.files.presign(vm_id, path=remote_path)
        _assert_under_limit(size, presigned)
        await _ahttp_put_file(presigned.upload_url, local_path, size=size)
        await self.vms.files.fetch(vm_id, url=presigned.download_url, path=remote_path, timeout_sec=fetch_timeout_sec)

    async def _upload_dir(
        self, vm_id: str, local_dir: str, remote_dir: str, fetch_timeout_sec: int, exec_timeout_sec: int
    ) -> None:
        stage = _stage_tar_path("upload")
        presigned = await self.vms.files.presign(vm_id, path=stage)
        await _ahttp_put_iter(presigned.upload_url, local_dir)
        await self.vms.files.fetch(vm_id, url=presigned.download_url, path=stage, timeout_sec=fetch_timeout_sec)
        extract = (
            f"set -eu; mkdir -p {shlex.quote(remote_dir)}; "
            f"tar xzf {shlex.quote(stage)} -C {shlex.quote(remote_dir)}; "
            f"rm -f {shlex.quote(stage)}"
        )
        _require_exec_ok(extract, await self.vms.run(vm_id, command=extract, timeout_sec=exec_timeout_sec))

    async def _download_file(self, vm_id: str, remote_path: str, local_path: str, exec_timeout_sec: int) -> None:
        presigned = await self.vms.files.presign(vm_id, path=remote_path)
        cmd = (
            f"set -eu; curl --fail --silent --show-error -T {shlex.quote(remote_path)} "
            f"-H 'Content-Type: {_PUT_CONTENT_TYPE}' {shlex.quote(presigned.upload_url)}"
        )
        _require_exec_ok(cmd, await self.vms.run(vm_id, command=cmd, timeout_sec=exec_timeout_sec))
        parent = os.path.dirname(os.path.abspath(local_path)) or "."
        await asyncio.to_thread(os.makedirs, parent, exist_ok=True)
        await _ahttp_get_to_file(presigned.download_url, local_path)

    async def _download_dir(self, vm_id: str, remote_dir: str, local_dir: str, exec_timeout_sec: int) -> None:
        presigned = await self.vms.files.presign(vm_id, path=_stage_tar_path("download"))
        cmd = (
            f"set -eu; tar czf - -C {shlex.quote(remote_dir)} . | "
            f"curl --fail --silent --show-error -T - -H 'Content-Type: {_PUT_CONTENT_TYPE}' "
            f"{shlex.quote(presigned.upload_url)}"
        )
        _require_exec_ok(cmd, await self.vms.run(vm_id, command=cmd, timeout_sec=exec_timeout_sec))
        await asyncio.to_thread(os.makedirs, local_dir, exist_ok=True)
        await _ahttp_get_to_tar_extract(presigned.download_url, local_dir)


# --------------------------------------------------------------------------- #
#                               Shared helpers                                #
# --------------------------------------------------------------------------- #


def _poll_delay(interval: float, max_wait: float) -> float:
    """Jittered polling interval so concurrent clients don't stampede."""
    jitter = interval * 0.1
    return max(0.5, min(max_wait, interval + random.uniform(-jitter, jitter)))


def _stage_tar_path(tag: str) -> str:
    """Unique-per-process tarball path inside the VM."""
    return f"{_VM_STAGE_DIR}/fastvm-{tag}-{os.getpid()}-{random.randrange(1 << 30):x}.tar.gz"


def _require_exec_ok(preview: str, result: ExecResult) -> ExecResult:
    if result.timed_out or result.exit_code != 0:
        raise VMExecError(preview, result)
    return result


def _stat_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except OSError as e:
        raise FileTransferError(f"cannot stat {path!r}: {e}", cause=e) from e


def _assert_under_limit(size: int, presigned: "PresignResponse") -> None:
    if size > presigned.max_upload_bytes:
        raise FileTransferError(f"upload size {size} exceeds VM limit {presigned.max_upload_bytes}")


# --------------------------------------------------------------------------- #
#                        HTTP helpers — storage backend                       #
# --------------------------------------------------------------------------- #
#
# These bypass the generated client because signed URLs reject extra headers
# (``X-API-Key``) that the Stainless client injects on every request.
#


def _http_put_stream(url: str, body: Any, *, size: Optional[int] = None) -> None:
    headers = {"Content-Type": _PUT_CONTENT_TYPE}
    if size is not None:
        headers["Content-Length"] = str(size)
    with httpx.Client(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        r = c.put(url, content=body, headers=headers)
        _raise_for_storage(r, op="upload")


def _http_get_to_file(url: str, local_path: str) -> None:
    with httpx.Client(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        with c.stream("GET", url) as r:
            _raise_for_storage(r, op="download")
            with open(local_path, "wb") as f:
                for chunk in r.iter_bytes(chunk_size=1 << 20):
                    f.write(chunk)


def _http_get_to_tar_extract(url: str, dest_dir: str) -> None:
    with httpx.Client(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        with c.stream("GET", url) as r:
            _raise_for_storage(r, op="download")
            unpack_stream_to_directory(
                cast(BinaryIO, _IterStream(r.iter_bytes(chunk_size=1 << 20))),
                dest_dir,
            )


async def _ahttp_put_file(url: str, local_path: str, *, size: int) -> None:
    headers = {"Content-Type": _PUT_CONTENT_TYPE, "Content-Length": str(size)}
    async with httpx.AsyncClient(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        with open(local_path, "rb") as f:
            r = await c.put(url, content=_aiter_file(f), headers=headers)
        _raise_for_storage(r, op="upload")


async def _ahttp_put_iter(url: str, local_dir: str) -> None:
    """Stream a directory tar to the upload URL asynchronously.

    ``tarfile`` is blocking, so we pull chunks from the sync iterator on a
    worker thread and pump them through an async generator that httpx can
    consume directly.
    """
    headers = {"Content-Type": _PUT_CONTENT_TYPE}

    async def _chunks() -> AsyncIterator[bytes]:
        it: Iterator[bytes] = iter(pack_directory_to_stream(local_dir))
        while True:
            chunk: Optional[bytes] = await asyncio.to_thread(_next_or_none, it)
            if chunk is None:
                return
            yield chunk

    async with httpx.AsyncClient(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        r = await c.put(url, content=_chunks(), headers=headers)
        _raise_for_storage(r, op="upload")


async def _ahttp_get_to_file(url: str, local_path: str) -> None:
    async with httpx.AsyncClient(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        async with c.stream("GET", url) as r:
            _raise_for_storage(r, op="download")
            with open(local_path, "wb") as f:
                async for chunk in r.aiter_bytes(chunk_size=1 << 20):
                    f.write(chunk)


async def _ahttp_get_to_tar_extract(url: str, dest_dir: str) -> None:
    # Buffer to a temp file on disk, then extract on a worker thread. Avoids
    # bridging async → sync stream reads inside ``tarfile`` (which is blocking).
    import tempfile

    async with httpx.AsyncClient(timeout=_STORAGE_HTTP_TIMEOUT) as c:
        async with c.stream("GET", url) as r:
            _raise_for_storage(r, op="download")
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp_path = tmp.name
            try:
                async for chunk in r.aiter_bytes(chunk_size=1 << 20):
                    tmp.write(chunk)
                tmp.flush()
                tmp.close()
                await asyncio.to_thread(_extract_tar_file, tmp_path, dest_dir)
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass


def _extract_tar_file(tar_path: str, dest_dir: str) -> None:
    with open(tar_path, "rb") as f:
        unpack_stream_to_directory(f, dest_dir)


def _raise_for_storage(r: httpx.Response, *, op: str) -> None:
    if 200 <= r.status_code < 300:
        return
    try:
        body = r.text[:2000]
    except Exception:
        body = ""
    raise FileTransferError(f"storage {op} failed: HTTP {r.status_code}: {body}")


def _aiter_file(f: IO[bytes], chunk_size: int = 1 << 20) -> AsyncIterator[bytes]:
    async def _gen() -> AsyncIterator[bytes]:
        while True:
            chunk: bytes = await asyncio.to_thread(f.read, chunk_size)
            if not chunk:
                return
            yield chunk

    return _gen()


def _next_or_none(it: Iterator[bytes]) -> Optional[bytes]:
    try:
        return next(it)
    except StopIteration:
        return None


class _IterStream:
    """Adapt a byte iterator to a minimal file-like object for ``tarfile``.

    ``tarfile.open(fileobj=...)`` only touches ``read(n)``, so we don't need
    a full ``BinaryIO`` — callers ``cast`` us to satisfy type checkers.
    """

    def __init__(self, it: Iterator[bytes]) -> None:
        self._it = iter(it)
        self._buf = bytearray()
        self._eof = False

    def read(self, n: int = -1) -> bytes:
        if n < 0:
            while not self._eof:
                self._pull()
            out = bytes(self._buf)
            self._buf.clear()
            return out
        while len(self._buf) < n and not self._eof:
            self._pull()
        take = min(n, len(self._buf))
        out = bytes(self._buf[:take])
        del self._buf[:take]
        return out

    def _pull(self) -> None:
        try:
            chunk = next(self._it)
        except StopIteration:
            self._eof = True
            return
        self._buf.extend(chunk)
