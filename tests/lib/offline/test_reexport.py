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
        "VMExecError",
        "FileTransferError",
    ):
        assert hasattr(fastvm, name), f"fastvm should export {name}"
        assert name in fastvm.__all__, f"{name} missing from fastvm.__all__"
