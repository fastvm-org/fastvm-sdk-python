"""Custom FastVM helpers layered on top of the generated Stainless client.

Everything in this directory is out of scope for Stainless code generation, so
files here survive regenerations untouched. Users who want the full ergonomics
of the old hand-written SDK import from here (or the top-level package, which
re-exports these symbols):

    from fastvm import FastvmClient, AsyncFastvmClient

``FastvmClient`` / ``AsyncFastvmClient`` subclass the generated ``Fastvm`` /
``AsyncFastvm`` and add:

  * HTTP/2 ``httpx`` client by default (multiplexing + header compression)
  * ``launch(...)`` — ``POST /v1/vms`` + poll until ``status == running``
  * ``upload(vm_id, local, remote)`` / ``download(vm_id, remote, local)``
    — unified file/dir transfers via presigned storage URLs
  * ``client.vms.run(id, command="ls -la")`` — auto-wraps shell strings
    into ``["sh", "-c", ...]`` (Python-only footgun guard)

The raw generated API (``client.vms.files.presign``, etc.) is untouched and
available as an escape hatch.
"""

from ._client import FastvmClient, AsyncFastvmClient
from ._errors import VMLaunchError, VMNotReadyError, FileTransferError

__all__ = [
    "FastvmClient",
    "AsyncFastvmClient",
    "VMLaunchError",
    "VMNotReadyError",
    "FileTransferError",
]
