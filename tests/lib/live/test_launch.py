"""Launch edge cases that can't share the session VM — ``wait=False`` and
snapshot restore. Each test creates + destroys its own VMs inline."""

from __future__ import annotations

import time
import random
import string

from fastvm import FastvmClient
from fastvm.types.vm import Vm


def _name() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f"sdk-test-{suffix}"


def _wait_snapshot_ready(client: FastvmClient, snap_id: str, timeout: float = 180) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        for s in client.snapshots.list():
            if s.id == snap_id:
                if s.status in ("ready", "active", "error"):
                    return s.status
                break
        time.sleep(2)
    return "timeout"


def test_wait_false(client: FastvmClient) -> None:
    """``launch(wait=False)`` returns the initial VM without polling;
    ``wait_for_vm_ready`` drives it the rest of the way."""
    vm = client.vms.launch(machine_type="c1m2", name=_name(), wait=False)
    try:
        assert vm.id and vm.status in {"provisioning", "running", "queued", "pending"}
        ready = client.wait_for_vm_ready(vm.id, timeout=300)
        assert ready.status == "running"
    finally:
        try:
            client.vms.delete(vm.id)
        except Exception:
            pass


def test_snapshot_restore(client: FastvmClient, vm: Vm) -> None:
    """Snapshot the session VM, restore via ``launch(snapshot_id=…)``,
    and verify filesystem state carried over."""
    marker_path = f"/root/snap-marker-{random.randint(0, 1 << 32):08x}"
    client.vms.run(vm.id, command=["sh", "-c", f"echo sentinel > {marker_path}"])

    snap = client.snapshots.create(vm_id=vm.id, name=f"{vm.name}-snap")
    try:
        assert _wait_snapshot_ready(client, snap.id) in ("ready", "active")
        restored = client.vms.launch(snapshot_id=snap.id, name=_name())
        try:
            out = client.vms.run(restored.id, command=["cat", marker_path])
            assert out.stdout.strip() == "sentinel"
        finally:
            client.vms.delete(restored.id)
    finally:
        client.snapshots.delete(snap.id)
        client.vms.run(vm.id, command=["rm", "-f", marker_path])
