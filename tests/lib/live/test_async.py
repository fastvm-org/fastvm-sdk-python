"""Async smoke test: launch + run + file + directory roundtrip on a single
``AsyncFastvmClient`` + session-scoped VM."""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest

from fastvm import AsyncFastvmClient
from fastvm.types.vm import Vm


@pytest.mark.asyncio(loop_scope="session")
async def test_async_workflow(
    async_client: AsyncFastvmClient,
    async_vm: Vm,
    tmp_path: Path,
) -> None:
    assert async_vm.status == "running"

    # Per-test workspace on the shared async VM.
    workdir = f"/root/async-{uuid.uuid4().hex[:8]}"
    await async_client.vms.run(async_vm.id, command=["mkdir", "-p", workdir])

    try:
        # File roundtrip.
        src = tmp_path / "async.txt"
        src.write_text("async\n", encoding="utf-8")
        await async_client.upload(async_vm.id, str(src), f"{workdir}/async.txt")
        out = await async_client.vms.run(async_vm.id, command=["cat", f"{workdir}/async.txt"])
        assert out.stdout == "async\n"

        dst = tmp_path / "async.back.txt"
        await async_client.download(async_vm.id, f"{workdir}/async.txt", str(dst))
        assert dst.read_text(encoding="utf-8") == "async\n"

        # Directory roundtrip: nested + empty subdir.
        local_tree = tmp_path / "tree"
        (local_tree / "nested").mkdir(parents=True)
        (local_tree / "empty").mkdir()
        (local_tree / "nested" / "x.txt").write_text("x\n")
        await async_client.upload(async_vm.id, str(local_tree), f"{workdir}/tree")
        cat = await async_client.vms.run(
            async_vm.id, command=["cat", f"{workdir}/tree/nested/x.txt"]
        )
        assert cat.stdout == "x\n"

        back = tmp_path / "tree-back"
        await async_client.download(async_vm.id, f"{workdir}/tree", str(back))
        assert (back / "nested" / "x.txt").read_text() == "x\n"
        assert (back / "empty").is_dir()
    finally:
        try:
            await async_client.vms.run(async_vm.id, command=["rm", "-rf", workdir])
        except Exception:
            pass
