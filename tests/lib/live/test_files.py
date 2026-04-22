"""Unified upload/download: file + directory, sync + async."""

from __future__ import annotations

from pathlib import Path

import pytest

from fastvm import FastvmClient, AsyncFastvmClient
from fastvm.types.vm import Vm


def _seed_dir(root: Path) -> None:
    (root / "a.txt").write_text("alpha\n")
    (root / "sub").mkdir()
    (root / "sub" / "b.txt").write_text("beta\n")


def test_upload_download_file(client: FastvmClient, vm: Vm, tmp_path: Path) -> None:
    local = tmp_path / "hello.txt"
    payload = "hello from the test\n" * 100
    local.write_text(payload)

    client.upload(vm.id, str(local), "/root/hello.txt")
    # Confirm via exec.
    r = client.vms.run(vm.id, command="cat /root/hello.txt")
    assert r.exit_code == 0
    assert r.stdout == payload

    back = tmp_path / "roundtrip.txt"
    client.download(vm.id, "/root/hello.txt", str(back))
    assert back.read_text() == payload


def test_upload_download_dir(client: FastvmClient, vm: Vm, tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    _seed_dir(src)

    client.upload(vm.id, str(src), "/root/uploaded")
    r = client.vms.run(vm.id, command="cat /root/uploaded/sub/b.txt")
    assert r.exit_code == 0
    assert r.stdout == "beta\n"

    back = tmp_path / "back"
    client.download(vm.id, "/root/uploaded", str(back))
    assert (back / "a.txt").read_text() == "alpha\n"
    assert (back / "sub" / "b.txt").read_text() == "beta\n"


def test_download_missing_raises(client: FastvmClient, vm: Vm, tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        client.download(vm.id, "/root/does-not-exist", str(tmp_path / "out"))


@pytest.mark.asyncio(loop_scope="session")
async def test_async_upload_download_file(async_client: AsyncFastvmClient, async_vm: Vm, tmp_path: Path) -> None:
    local = tmp_path / "async.txt"
    local.write_text("async payload\n")

    await async_client.upload(async_vm.id, str(local), "/root/async.txt")
    r = await async_client.vms.run(async_vm.id, command="cat /root/async.txt")
    assert r.exit_code == 0
    assert r.stdout == "async payload\n"

    back = tmp_path / "async-back.txt"
    await async_client.download(async_vm.id, "/root/async.txt", str(back))
    assert back.read_text() == "async payload\n"
