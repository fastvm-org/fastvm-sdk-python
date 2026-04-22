"""upload() / download() roundtrip for files and directories."""

from __future__ import annotations

from pathlib import Path

import pytest

from fastvm import FastvmClient, AsyncFastvmClient
from fastvm.types.vm import Vm


def test_file_roundtrip(client: FastvmClient, vm: Vm, tmp_path: Path) -> None:
    src = tmp_path / "hello.txt"
    payload = "hello\n" * 100
    src.write_text(payload)

    client.upload(vm.id, str(src), "/root/hello.txt")
    assert client.vms.run(vm.id, command="cat /root/hello.txt").stdout == payload

    dst = tmp_path / "hello.back.txt"
    client.download(vm.id, "/root/hello.txt", str(dst))
    assert dst.read_text() == payload


def test_directory_roundtrip(client: FastvmClient, vm: Vm, tmp_path: Path) -> None:
    src = tmp_path / "src"
    (src / "sub").mkdir(parents=True)
    (src / "a.txt").write_text("alpha\n")
    (src / "sub" / "b.txt").write_text("beta\n")

    client.upload(vm.id, str(src), "/root/uploaded")
    assert client.vms.run(vm.id, command="cat /root/uploaded/sub/b.txt").stdout == "beta\n"

    dst = tmp_path / "back"
    client.download(vm.id, "/root/uploaded", str(dst))
    assert (dst / "a.txt").read_text() == "alpha\n"
    assert (dst / "sub" / "b.txt").read_text() == "beta\n"


def test_download_missing_raises(client: FastvmClient, vm: Vm, tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        client.download(vm.id, "/root/does-not-exist", str(tmp_path / "out"))


@pytest.mark.asyncio(loop_scope="session")
async def test_async_roundtrip(async_client: AsyncFastvmClient, async_vm: Vm, tmp_path: Path) -> None:
    src = tmp_path / "async.txt"
    src.write_text("async\n")

    await async_client.upload(async_vm.id, str(src), "/root/async.txt")
    out = await async_client.vms.run(async_vm.id, command="cat /root/async.txt")
    assert out.stdout == "async\n"

    dst = tmp_path / "async.back.txt"
    await async_client.download(async_vm.id, "/root/async.txt", str(dst))
    assert dst.read_text() == "async\n"
