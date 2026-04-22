"""End-to-end VM lifecycle + quotas against the real API."""

from __future__ import annotations

import pytest

from fastvm import FastvmClient, NotFoundError
from fastvm.types.vm import Vm


def test_launch_retrieve_run_rename_delete(client: FastvmClient, vm: Vm) -> None:
    assert vm.status == "running"

    got = client.vms.retrieve(vm.id)
    assert got.id == vm.id and got.name == vm.name

    result = client.vms.run(vm.id, command="echo hi && whoami")
    assert result.exit_code == 0
    assert "hi" in result.stdout

    result = client.vms.run(vm.id, command=["echo", "argv"])
    assert result.stdout.strip() == "argv"

    renamed = client.vms.update(vm.id, name=vm.name + "-renamed")
    assert renamed.name.endswith("-renamed")


def test_list_contains_vm(client: FastvmClient, vm: Vm) -> None:
    assert any(v.id == vm.id for v in client.vms.list())


def test_retrieve_missing_raises_not_found(client: FastvmClient) -> None:
    with pytest.raises(NotFoundError):
        client.vms.retrieve("vm_does_not_exist_000000")


def test_quotas(client: FastvmClient) -> None:
    q = client.quotas.retrieve()
    assert q.limits is not None
    assert q.usage is not None
