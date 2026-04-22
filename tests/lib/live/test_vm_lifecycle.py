"""End-to-end: launch → retrieve → run → rename → delete.

One test hits roughly every core endpoint on the VM surface. Each generated
method is covered by Stainless's own API tests; this verifies the composition
works against the real server.
"""

from __future__ import annotations

import pytest

from fastvm import FastvmClient
from fastvm.types.vm import Vm


def test_lifecycle(client: FastvmClient, vm: Vm) -> None:
    # ``launch`` polled to running for us.
    assert vm.status == "running"

    # Readback reflects the name we gave.
    got = client.vms.retrieve(vm.id)
    assert got.id == vm.id
    assert got.name == vm.name

    # Exec with a shell-string (auto-wraps into ``sh -c``).
    result = client.vms.run(vm.id, command="echo hi && whoami")
    assert result.exit_code == 0
    assert "hi" in result.stdout

    # Exec with argv form still works.
    result2 = client.vms.run(vm.id, command=["echo", "argv"])
    assert result2.exit_code == 0
    assert result2.stdout.strip() == "argv"

    # Rename.
    renamed = client.vms.update(vm.id, name=vm.name + "-renamed")
    assert renamed.name.endswith("-renamed")

    # ``vm`` fixture cleans up on teardown.


def test_listing_contains_vm(client: FastvmClient, vm: Vm) -> None:
    vms = client.vms.list()
    assert any(v.id == vm.id for v in vms), "launched VM missing from /v1/vms list"


def test_nonexistent_vm_errors(client: FastvmClient) -> None:
    from fastvm import NotFoundError

    with pytest.raises(NotFoundError):
        client.vms.retrieve("vm_does_not_exist_000000")
