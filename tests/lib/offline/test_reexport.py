"""Top-level ``fastvm`` exposes the custom helpers + error types."""

from __future__ import annotations


def test_top_level_exports() -> None:
    import fastvm

    for name in (
        "Fastvm",
        "AsyncFastvm",
        "FastvmClient",
        "AsyncFastvmClient",
        "VMLaunchError",
        "VMNotReadyError",
        "FileTransferError",
    ):
        assert hasattr(fastvm, name), f"fastvm should export {name}"
        assert name in fastvm.__all__, f"{name} missing from fastvm.__all__"


def test_helper_errors_subclass_fastvm_error() -> None:
    """`except FastvmError` catches helper errors too."""
    from fastvm import FastvmError, VMLaunchError, VMNotReadyError, FileTransferError

    assert issubclass(VMLaunchError, FastvmError)
    assert issubclass(VMNotReadyError, FastvmError)
    assert issubclass(VMNotReadyError, TimeoutError)
    assert issubclass(FileTransferError, FastvmError)
