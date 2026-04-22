"""Snapshot → restore roundtrip: data survives across VMs."""

from __future__ import annotations

from fastvm import FastvmClient
from fastvm.types.vm import Vm


def test_snapshot_restore(client: FastvmClient, vm: Vm) -> None:
    # Write a sentinel file so we can verify it survives the snapshot.
    assert client.vms.run(vm.id, command="echo sentinel-123 > /root/marker").exit_code == 0

    snap = client.snapshots.create(vm_id=vm.id, name=f"{vm.name}-snap")
    try:
        # Snapshots are created async; poll the list until ours reaches a
        # non-transitional state. (No GET-by-id on /v1/snapshots; list filter is fine.)
        import time

        def _lookup(snap_id: str):
            for s in client.snapshots.list():
                if s.id == snap_id:
                    return s
            return None

        for _ in range(60):
            cur = _lookup(snap.id)
            if cur is not None and cur.status in ("ready", "active", "error"):
                snap = cur
                break
            time.sleep(2)
        assert snap.status in ("ready", "active"), f"snapshot failed: status={snap.status!r}"

        # Restore a new VM from the snapshot.
        restored = client.launch(snapshot_id=snap.id, name=f"{vm.name}-restored")
        try:
            out = client.vms.run(restored.id, command="cat /root/marker")
            assert out.exit_code == 0
            assert out.stdout.strip() == "sentinel-123"
        finally:
            client.vms.delete(restored.id)
    finally:
        try:
            client.snapshots.delete(snap.id)
        except Exception:
            pass
