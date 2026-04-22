"""launch() polling: success, terminal failure, timeout, wait=False."""

from __future__ import annotations

from typing import List, Iterator
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from fastvm import FastvmClient, VMLaunchError, VMNotReadyError
from fastvm.types.vm import Vm


def _vm(status: str) -> Vm:
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


def _mock_launch(client: FastvmClient, *, initial: str, transitions: List[str] | None = None):
    """Returns a context manager that mocks vms.launch + vms.retrieve + time.sleep.

    `initial` is the status returned by POST; `transitions` is the sequence of
    statuses returned by each subsequent GET poll.
    """
    from contextlib import ExitStack

    stack = ExitStack()
    stack.enter_context(patch.object(client.vms, "launch", return_value=_vm(initial)))
    if transitions is not None:
        queue = list(transitions)
        last = transitions[-1]

        def _next(_id: str) -> Vm:
            return _vm(queue.pop(0) if queue else last)

        stack.enter_context(patch.object(client.vms, "retrieve", side_effect=_next))
    stack.enter_context(patch("time.sleep"))
    return stack


def test_running_skips_polling(client: FastvmClient) -> None:
    with _mock_launch(client, initial="running"):
        assert client.launch(machine_type="c1m2").status == "running"


def test_polls_until_running(client: FastvmClient) -> None:
    with _mock_launch(client, initial="provisioning", transitions=["provisioning", "provisioning", "running"]):
        vm = client.launch(machine_type="c1m2", poll_interval=0.01, timeout=5)
    assert vm.status == "running"


def test_terminal_status_raises(client: FastvmClient) -> None:
    with _mock_launch(client, initial="provisioning", transitions=["error"]):
        with pytest.raises(VMLaunchError) as exc:
            client.launch(machine_type="c1m2", poll_interval=0.01, timeout=5)
    assert exc.value.status == "error"


def test_timeout_raises(client: FastvmClient) -> None:
    with _mock_launch(client, initial="provisioning", transitions=["provisioning"]):
        with pytest.raises(VMNotReadyError):
            client.launch(machine_type="c1m2", poll_interval=0.01, timeout=0.0)


def test_wait_false_returns_initial(client: FastvmClient) -> None:
    with _mock_launch(client, initial="provisioning"):
        assert client.launch(machine_type="c1m2", wait=False).status == "provisioning"
