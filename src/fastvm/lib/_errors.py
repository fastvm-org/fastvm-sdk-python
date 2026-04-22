"""Errors raised only by the custom helpers in ``fastvm.lib``.

Regular API errors (4xx/5xx) come through the generated client as
``fastvm.APIStatusError`` subclasses; those aren't re-wrapped here.
"""

from __future__ import annotations

from typing import Optional

from ..types.exec_result import ExecResult


class VMNotReadyError(TimeoutError):
    """``launch()`` polling exceeded its timeout before the VM became ready."""

    def __init__(self, vm_id: str, last_status: str, timeout_s: float) -> None:
        super().__init__(
            f"VM {vm_id} did not reach status=running within {timeout_s:.0f}s (last observed status: {last_status!r})"
        )
        self.vm_id = vm_id
        self.last_status = last_status
        self.timeout_s = timeout_s


class VMLaunchError(RuntimeError):
    """VM entered a terminal failure status during ``launch()`` polling."""

    def __init__(self, vm_id: str, status: str) -> None:
        super().__init__(f"VM {vm_id} failed to launch (status={status!r})")
        self.vm_id = vm_id
        self.status = status


class VMExecError(RuntimeError):
    """A VM-side command (issued by an upload/download helper) exited non-zero."""

    def __init__(self, command: str, result: ExecResult) -> None:
        super().__init__(
            f"VM command failed (exit={result.exit_code}, timedOut={result.timed_out}): {command}\n"
            f"stderr: {result.stderr[:2000] if result.stderr else ''}"
        )
        self.command = command
        self.result = result


class FileTransferError(RuntimeError):
    """Something went wrong during an upload/download helper run."""

    def __init__(self, message: str, *, cause: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.__cause__ = cause
