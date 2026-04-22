"""Custom FastVM helpers layered on top of the generated Stainless client.

Everything in this directory is out of scope for Stainless code generation, so
files here survive regenerations untouched. Users who want the full ergonomics
of the old hand-written SDK import from here instead of the top-level package:

    from fastvm.lib import FastvmClient, AsyncFastvmClient

Those classes subclass the generated ``Fastvm`` / ``AsyncFastvm`` and add:

  * ``warmup()`` — pre-open HTTP/2 connection via ``GET /healthz``
  * ``launch(...)`` — ``POST /v1/vms`` + poll until status == ``running``
  * ``upload_file`` / ``upload_directory`` — client → VM file transfer
  * ``download_file`` / ``download_directory`` — VM → client file transfer
  * ``run(vm_id, command)`` — short-form alias for ``vms.run(...)``

The raw generated methods (``client.vms.launch``, ``client.vms.files.presign``,
etc.) remain available for escape-hatch use.
"""

from ._client import FastvmClient, AsyncFastvmClient
from ._errors import VMExecError, VMLaunchError, VMNotReadyError, FileTransferError

__all__ = [
    "FastvmClient",
    "AsyncFastvmClient",
    "VMLaunchError",
    "VMExecError",
    "VMNotReadyError",
    "FileTransferError",
]
