"""Snapshot + restore preserves VM filesystem state."""

from __future__ import annotations

import time

from fastvm import FastvmClient
from fastvm.types.vm import Vm


def _wait_ready(client: FastvmClient, snap_id: str, timeout: float = 120) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        for s in client.snapshots.list():
            if s.id == snap_id and s.status in ("ready", "active", "error"):
                return s.status
        time.sleep(2)
    return "timeout"


def test_snapshot_then_restore(client: FastvmClient, vm: Vm) -> None:
    client.vms.run(vm.id, command="echo sentinel > /root/marker")

    snap = client.snapshots.create(vm_id=vm.id, name=f"{vm.name}-snap")
    try:
        assert _wait_ready(client, snap.id) in ("ready", "active")

        restored = client.launch(snapshot_id=snap.id, name=f"{vm.name}-restored")
        try:
            out = client.vms.run(restored.id, command="cat /root/marker")
            assert out.stdout.strip() == "sentinel"
        finally:
            client.vms.delete(restored.id)
    finally:
        client.snapshots.delete(snap.id)
