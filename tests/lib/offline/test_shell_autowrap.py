"""``FastvmClient`` auto-wraps shell strings on ``vms.run``."""

from __future__ import annotations

from fastvm.lib._client import _wrap_shell_command


def test_string_wraps():
    assert _wrap_shell_command("ls -la /root") == ["sh", "-c", "ls -la /root"]


def test_empty_string_wraps():
    # Degenerate but valid input; don't silently drop it.
    assert _wrap_shell_command("") == ["sh", "-c", ""]


def test_sequence_passthrough():
    assert _wrap_shell_command(["python3", "-c", "print(1)"]) == ["python3", "-c", "print(1)"]


def test_tuple_passthrough():
    assert _wrap_shell_command(("a", "b")) == ["a", "b"]
