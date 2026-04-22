"""``FastvmClient`` / ``AsyncFastvmClient`` — ergonomic wrappers.

Subclasses the generated ``Fastvm`` / ``AsyncFastvm`` clients. Everything here
is additive; the generated resources (``self.vms``, ``self.snapshots``,
``self.quotas``, ``self.health()``) are unchanged.
"""

from __future__ import annotations

import os
import time
import random
import asyncio
from typing import IO, TYPE_CHECKING, Any, BinaryIO, Iterator, Optional, Sequence, AsyncIterator, cast

import httpx

from ._errors import VMExecError, VMLaunchError, VMNotReadyError, FileTransferError
from .._client import Fastvm, AsyncFastvm
from ._tarutil import quote_sh, pack_directory_to_stream, unpack_stream_to_directory
from ..types.vm import Vm
from ..types.exec_result import ExecResult

if TYPE_CHECKING:
    from ..types.vms.presign_response import PresignResponse

__all__ = ["FastvmClient", "AsyncFastvmClient"]


# --------------------------------------------------------------------------- #
#                               Shared constants                              #
# --------------------------------------------------------------------------- #

# VM statuses that mean "give up, won't become runnable".
_TERMINAL_FAILURE = {"error", "stopped", "deleting"}
_RUNNING = "running"

# GCS signed URLs are signed against a specific Content-Type; must match
# exactly on both the client PUT and the VM-side ``curl -T``. Our backend
# presigns with this value.
_PUT_CONTENT_TYPE = "application/octet-stream"

# How long we'll wait for HTTP ops to the storage backend (presigned URLs)
# to complete. Separate from the scheduler client timeout since large
# transfers legitimately take minutes.
_STORAGE_HTTP_TIMEOUT = httpx.Timeout(connect=15.0, read=900.0, write=900.0, pool=15.0)

# Where tarballs land inside the VM during directory transfers.
_VM_STAGE_DIR = "/tmp"


def _stage_tar_path(tag: str) -> str:
    """Unique-per-process tarball path inside the VM."""
    return f"{_VM_STAGE_DIR}/fastvm-{tag}-{os.getpid()}-{random.randrange(1 << 30):x}.tar.gz"


def _poll_delays(interval: float, max_wait: float) -> float:
    """Jittered polling interval so concurrent clients don't stampede."""
    jitter = interval * 0.1
    return max(0.5, min(max_wait, interval + random.uniform(-jitter, jitter)))


def _require_exec_ok(command_preview: str, result: ExecResult) -> ExecResult:
    """Raise ``VMExecError`` if an exec helper returned non-zero / timed out."""
    if result.timed_out or result.exit_code != 0:
        raise VMExecError(command_preview, result)
    return result


# --------------------------------------------------------------------------- #
#                               Sync client                                   #
# --------------------------------------------------------------------------- #


class FastvmClient(Fastvm):
    """Drop-in replacement for :class:`fastvm.Fastvm` with ergonomic helpers.

    Example::

        with FastvmClient() as client:
            client.warmup()
            vm = client.launch(machine_type="c1m2")
            client.upload_file(vm.id, "./main.py", "/root/main.py")
            result = client.run(vm.id, ["python3", "/root/main.py"])
            client.download_file(vm.id, "/root/out.log", "./out.log")
    """

    # --------------------------- Lifecycle ------------------------------- #

    def warmup(self) -> None:
        """Pre-open the HTTP/2 connection to the scheduler.

        Hits ``GET /healthz`` so the connection + TLS handshake are amortized
        before the first real call. Errors propagate — ``warmup`` is a request
        like any other.
        """
        self.health()

    def launch(
        self,
        *,
        wait: bool = True,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        **params: Any,
    ) -> Vm:
        """``POST /v1/vms`` and (by default) wait until the VM is running.

        All other kwargs are forwarded to :meth:`VmsResource.launch`.

        Passing ``wait=False`` returns immediately with the initial VM (may be
        in ``provisioning`` status), matching the raw generated call.

        Raises:
          VMLaunchError: VM transitioned to a terminal failure status.
          VMNotReadyError: VM did not become ``running`` within ``timeout``.
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
            time.sleep(min(_poll_delays(poll_interval, remaining), remaining))

    def run(
        self,
        vm_id: str,
        command: Sequence[str],
        *,
        timeout_sec: Optional[int] = None,
        **kwargs: Any,
    ) -> ExecResult:
        """Short-form alias for ``client.vms.run(vm_id, command=...)``.

        Positional ``command`` matches the old SDK. Under the hood this is the
        same non-idempotent ``POST /v1/vms/{id}/exec`` — no auto-retry.
        """
        if timeout_sec is not None:
            kwargs["timeout_sec"] = timeout_sec
        return self.vms.run(vm_id, command=list(command), **kwargs)

    # --------------------------- File transfer --------------------------- #

    def upload_file(
        self,
        vm_id: str,
        local_path: str,
        remote_path: str,
        *,
        fetch_timeout_sec: int = 300,
    ) -> None:
        """Copy a single local file into the VM at ``remote_path``.

        Flow: ``presign`` → client PUTs the local file to the signed upload URL
        → scheduler asks the VM to ``fetch`` the download URL into ``remote_path``.
        """
        local_path = os.path.abspath(local_path)
        size = _stat_size(local_path)
        presigned = self.vms.files.presign(vm_id, path=remote_path)
        _assert_under_limit(size, presigned)
        with open(local_path, "rb") as f:
            _http_put_stream(presigned.upload_url, f, size=size)
        self.vms.files.fetch(vm_id, url=presigned.download_url, path=remote_path, timeout_sec=fetch_timeout_sec)

    def upload_directory(
        self,
        vm_id: str,
        local_dir: str,
        remote_dir: str,
        *,
        fetch_timeout_sec: int = 600,
        exec_timeout_sec: int = 600,
    ) -> None:
        """Copy a local directory tree into the VM at ``remote_dir``.

        Client-side tars the tree, uploads the tarball to storage, has the VM
        fetch it, then extracts into ``remote_dir`` and removes the staging
        tarball. Tar contents are rooted at ``basename(local_dir)``.
        """
        local_dir = os.path.abspath(local_dir)
        if not os.path.isdir(local_dir):
            raise NotADirectoryError(local_dir)
        stage = _stage_tar_path("upload")
        presigned = self.vms.files.presign(vm_id, path=stage)

        _http_put_stream(presigned.upload_url, pack_directory_to_stream(local_dir))
        self.vms.files.fetch(vm_id, url=presigned.download_url, path=stage, timeout_sec=fetch_timeout_sec)

        extract_cmd = (
            f"set -eu; mkdir -p {quote_sh(remote_dir)}; "
            f"tar xzf {quote_sh(stage)} -C {quote_sh(remote_dir)}; "
            f"rm -f {quote_sh(stage)}"
        )
        _require_exec_ok(
            extract_cmd,
            self.vms.run(vm_id, command=["sh", "-c", extract_cmd], timeout_sec=exec_timeout_sec),
        )

    def download_file(
        self,
        vm_id: str,
        remote_path: str,
        local_path: str,
        *,
        exec_timeout_sec: int = 300,
    ) -> None:
        """Copy a single file from the VM at ``remote_path`` to ``local_path``.

        Flow: ``presign`` → VM ``curl -T <file>`` PUTs bytes to the upload URL
        → client GETs the download URL and streams to ``local_path``.
        """
        presigned = self.vms.files.presign(vm_id, path=remote_path)
        cmd = (
            f"set -eu; curl --fail --silent --show-error -T {quote_sh(remote_path)} "
            f"-H 'Content-Type: {_PUT_CONTENT_TYPE}' {quote_sh(presigned.upload_url)}"
        )
        _require_exec_ok(
            cmd,
            self.vms.run(vm_id, command=["sh", "-c", cmd], timeout_sec=exec_timeout_sec),
        )
        os.makedirs(os.path.dirname(os.path.abspath(local_path)) or ".", exist_ok=True)
        _http_get_to_file(presigned.download_url, local_path)

    def download_directory(
        self,
        vm_id: str,
        remote_dir: str,
        local_dir: str,
        *,
        exec_timeout_sec: int = 600,
    ) -> None:
        """Copy a directory tree from the VM at ``remote_dir`` to ``local_dir``.

        VM-side ``tar czf - -C <parent> <name> | curl -T -`` produces a gzipped
        tarball stream that the client then extracts locally.
        """
        presigned = self.vms.files.presign(vm_id, path=_stage_tar_path("download"))
        cmd = (
            f"set -eu; tar czf - -C {quote_sh(remote_dir)} . | "
            f"curl --fail --silent --show-error -T - -H 'Content-Type: {_PUT_CONTENT_TYPE}' "
            f"{quote_sh(presigned.upload_url)}"
        )
        _require_exec_ok(
            cmd,
            self.vms.run(vm_id, command=["sh", "-c", cmd], timeout_sec=exec_timeout_sec),
        )
        os.makedirs(local_dir, exist_ok=True)
        _http_get_to_tar_extract(presigned.download_url, local_dir)


# --------------------------------------------------------------------------- #
#                               Async client                                  #
# --------------------------------------------------------------------------- #


class AsyncFastvmClient(AsyncFastvm):
    """Async twin of :class:`FastvmClient`."""

    async def warmup(self) -> None:
        await self.health()

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
            await asyncio.sleep(min(_poll_delays(poll_interval, remaining), remaining))

    async def run(
        self,
        vm_id: str,
        command: Sequence[str],
        *,
        timeout_sec: Optional[int] = None,
        **kwargs: Any,
    ) -> ExecResult:
        if timeout_sec is not None:
            kwargs["timeout_sec"] = timeout_sec
        return await self.vms.run(vm_id, command=list(command), **kwargs)

    async def upload_file(
        self,
        vm_id: str,
        local_path: str,
        remote_path: str,
        *,
        fetch_timeout_sec: int = 300,
    ) -> None:
        local_path = os.path.abspath(local_path)
        size = await asyncio.to_thread(_stat_size, local_path)
        presigned = await self.vms.files.presign(vm_id, path=remote_path)
        _assert_under_limit(size, presigned)
        await _ahttp_put_file(presigned.upload_url, local_path, size=size)
        await self.vms.files.fetch(vm_id, url=presigned.download_url, path=remote_path, timeout_sec=fetch_timeout_sec)

    async def upload_directory(
        self,
        vm_id: str,
        local_dir: str,
        remote_dir: str,
        *,
        fetch_timeout_sec: int = 600,
        exec_timeout_sec: int = 600,
    ) -> None:
        local_dir = os.path.abspath(local_dir)
        if not await asyncio.to_thread(os.path.isdir, local_dir):
            raise NotADirectoryError(local_dir)
        stage = _stage_tar_path("upload")
        presigned = await self.vms.files.presign(vm_id, path=stage)

        await _ahttp_put_iter(presigned.upload_url, local_dir)
        await self.vms.files.fetch(vm_id, url=presigned.download_url, path=stage, timeout_sec=fetch_timeout_sec)

        extract_cmd = (
            f"set -eu; mkdir -p {quote_sh(remote_dir)}; "
            f"tar xzf {quote_sh(stage)} -C {quote_sh(remote_dir)}; "
            f"rm -f {quote_sh(stage)}"
        )
        _require_exec_ok(
            extract_cmd,
            await self.vms.run(vm_id, command=["sh", "-c", extract_cmd], timeout_sec=exec_timeout_sec),
        )

    async def download_file(
        self,
        vm_id: str,
        remote_path: str,
        local_path: str,
        *,
        exec_timeout_sec: int = 300,
    ) -> None:
        presigned = await self.vms.files.presign(vm_id, path=remote_path)
        cmd = (
            f"set -eu; curl --fail --silent --show-error -T {quote_sh(remote_path)} "
            f"-H 'Content-Type: {_PUT_CONTENT_TYPE}' {quote_sh(presigned.upload_url)}"
        )
        _require_exec_ok(
            cmd,
            await self.vms.run(vm_id, command=["sh", "-c", cmd], timeout_sec=exec_timeout_sec),
        )
        parent = os.path.dirname(os.path.abspath(local_path)) or "."
        await asyncio.to_thread(os.makedirs, parent, exist_ok=True)
        await _ahttp_get_to_file(presigned.download_url, local_path)

    async def download_directory(
        self,
        vm_id: str,
        remote_dir: str,
        local_dir: str,
        *,
        exec_timeout_sec: int = 600,
    ) -> None:
        presigned = await self.vms.files.presign(vm_id, path=_stage_tar_path("download"))
        cmd = (
            f"set -eu; tar czf - -C {quote_sh(remote_dir)} . | "
            f"curl --fail --silent --show-error -T - -H 'Content-Type: {_PUT_CONTENT_TYPE}' "
            f"{quote_sh(presigned.upload_url)}"
        )
        _require_exec_ok(
            cmd,
            await self.vms.run(vm_id, command=["sh", "-c", cmd], timeout_sec=exec_timeout_sec),
        )
        await asyncio.to_thread(os.makedirs, local_dir, exist_ok=True)
        await _ahttp_get_to_tar_extract(presigned.download_url, local_dir)


# --------------------------------------------------------------------------- #
#                               HTTP helpers                                  #
# --------------------------------------------------------------------------- #
#
# These talk directly to the storage backend via presigned URLs — the
# generated client can't be reused because it injects ``X-API-Key`` on every
# request, and signed URLs reject unexpected headers.
#


def _stat_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except OSError as e:
        raise FileTransferError(f"cannot stat {path!r}: {e}", cause=e) from e


def _assert_under_limit(size: int, presigned: "PresignResponse") -> None:
    if size > presigned.max_upload_bytes:
        raise FileTransferError(f"upload size {size} exceeds VM limit {presigned.max_upload_bytes}")


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
            # ``tarfile`` wants a blocking read API; wrap the byte iterator.
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
    """Turn a sync file handle into an async byte iterator for httpx."""

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

    ``tarfile.open(fileobj=...)`` only touches ``read(n)`` on the object, so
    we don't need a full ``BinaryIO`` — callers ``cast`` us to satisfy type
    checkers.
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
