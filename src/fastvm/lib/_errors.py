"""Errors raised only by the custom helpers in ``fastvm.lib``.

Every error here subclasses the generated ``fastvm.FastvmError`` root, so
``except FastvmError`` catches every error raised by any method on
``FastvmClient`` — helpers included. Regular HTTP errors from the generated
client still come through as ``fastvm.APIStatusError`` subclasses; those are
never re-wrapped.

These four cover the failure modes the Stainless error hierarchy *can't*
model:

- ``VMLaunchError`` — ``GET /v1/vms/{id}`` returned 200 OK with
  ``status`` in a terminal failure state (``error`` / ``stopped`` / ``deleting``).
  The HTTP layer succeeded; the failure is in the response payload.
- ``VMNotReadyError`` — client-side polling deadline exceeded. No HTTP
  call timed out, we just stopped polling. Also subclasses the stdlib
  ``TimeoutError`` so ``except TimeoutError`` still works.
- ``FileTransferError`` — anything that went wrong during ``upload()`` /
  ``download()`` that isn't a Fastvm HTTP error: GCS PUT/GET failures
  (different host, different error schema), local ``tarfile`` errors,
  size-limit violations, and VM-side ``tar``/``curl`` commands that
  exited non-zero.
"""

from __future__ import annotations

from typing import Optional

from .._exceptions import FastvmError
from ..types.exec_result import ExecResult


class VMLaunchError(FastvmError, RuntimeError):
    """VM entered a terminal failure status during ``launch()`` polling."""

    def __init__(self, vm_id: str, status: str) -> None:
        super().__init__(f"VM {vm_id} failed to launch (status={status!r})")
        self.vm_id = vm_id
        self.status = status


class VMNotReadyError(FastvmError, TimeoutError):
    """``launch()`` polling exceeded its timeout before the VM became ready."""

    def __init__(self, vm_id: str, last_status: str, timeout_s: float) -> None:
        super().__init__(
            f"VM {vm_id} did not reach status=running within {timeout_s:.0f}s (last observed status: {last_status!r})"
        )
        self.vm_id = vm_id
        self.last_status = last_status
        self.timeout_s = timeout_s


class FileTransferError(FastvmError, RuntimeError):
    """Something went wrong during an ``upload()`` / ``download()`` helper run.

    ``exec_result`` is populated when the failure came from a VM-side
    ``tar`` / ``curl`` exec that exited non-zero — inspect
    ``exec_result.stderr`` / ``exec_result.exit_code`` for details.
    """

    def __init__(
        self,
        message: str,
        *,
        cause: Optional[BaseException] = None,
        exec_result: Optional[ExecResult] = None,
    ) -> None:
        super().__init__(message)
        self.exec_result = exec_result
        if cause is not None:
            self.__cause__ = cause
