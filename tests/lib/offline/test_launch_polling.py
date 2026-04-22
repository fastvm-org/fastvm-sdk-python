"""``launch()`` polling terminates on success, terminal statuses, and timeout."""

from __future__ import annotations

from typing import List, Iterator
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from fastvm import FastvmClient, VMLaunchError, VMNotReadyError
from fastvm.types.vm import Vm


def _vm(status: str) -> Vm:
    # Pydantic wants every required field; we only really care about ``status``.
    return Vm.model_validate(
        {
            "id": "vm_test",
            "cpu": 1,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "diskGiB": 10,
            "memoryMiB": 1024,
            "name": "t",
            "orgId": "org_test",
            "status": status,
        }
    )


@pytest.fixture()
def client() -> Iterator[FastvmClient]:
    c = FastvmClient(api_key="k", base_url="http://example.invalid")
    yield c
    c.close()


def test_running_launch_skips_polling(client: FastvmClient) -> None:
    with patch.object(client.vms, "launch", return_value=_vm("running")):
        vm = client.launch(machine_type="c1m2")
    assert vm.status == "running"


def test_provisioning_polls_then_runs(client: FastvmClient) -> None:
    statuses: List[str] = ["provisioning", "provisioning", "running"]

    def _next(_id: str) -> Vm:
        return _vm(statuses.pop(0))

    with patch.object(client.vms, "launch", return_value=_vm("provisioning")), patch.object(
        client.vms, "retrieve", side_effect=_next
    ), patch("time.sleep"):
        vm = client.launch(machine_type="c1m2", poll_interval=0.01, timeout=5)
    assert vm.status == "running"


def test_terminal_failure_raises(client: FastvmClient) -> None:
    with patch.object(client.vms, "launch", return_value=_vm("provisioning")), patch.object(
        client.vms, "retrieve", return_value=_vm("error")
    ), patch("time.sleep"):
        with pytest.raises(VMLaunchError) as exc_info:
            client.launch(machine_type="c1m2", poll_interval=0.01, timeout=5)
    assert exc_info.value.status == "error"


def test_timeout_raises(client: FastvmClient) -> None:
    with patch.object(client.vms, "launch", return_value=_vm("provisioning")), patch.object(
        client.vms, "retrieve", return_value=_vm("provisioning")
    ), patch("time.sleep"):
        with pytest.raises(VMNotReadyError):
            client.launch(machine_type="c1m2", poll_interval=0.01, timeout=0.0)


def test_wait_false_returns_initial(client: FastvmClient) -> None:
    with patch.object(client.vms, "launch", return_value=_vm("provisioning")):
        vm = client.launch(machine_type="c1m2", wait=False)
    assert vm.status == "provisioning"
