"""End-to-end coverage of ``FastvmClient`` against the real API.

Three dense tests sharing a single session-scoped VM (one per xdist worker):

* ``test_lifecycle`` — retrieve / list / update / run (string + argv) / 404
  / quotas. Exercises every read-mostly VM method + ``run`` auto-wrap.
* ``test_file_transfer`` — ``upload`` + ``download`` for regular files,
  with empty-file, overwrite, unicode filename, and missing-path edge
  cases bundled into a single VM round-trip.
* ``test_directory_transfer`` — ``upload`` + ``download`` for directories,
  including nested files, empty subdirs, and download-into-existing-dir.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fastvm import FastvmClient, NotFoundError
from fastvm.types.vm import Vm


def test_lifecycle(client: FastvmClient, vm: Vm) -> None:
    assert vm.status == "running"

    got = client.vms.retrieve(vm.id)
    assert got.id == vm.id and got.name == vm.name

    assert any(v.id == vm.id for v in client.vms.list())

    # run: string form (auto-wrapped to ["sh", "-c", ...]) + argv form.
    shell = client.vms.run(vm.id, command="echo hi && whoami")
    assert shell.exit_code == 0 and "hi" in shell.stdout

    argv = client.vms.run(vm.id, command=["echo", "argv"])
    assert argv.stdout.strip() == "argv"

    # rename then restore so later tests/fixture teardown see the original name.
    renamed = client.vms.update(vm.id, name=vm.name + "-renamed")
    assert renamed.name.endswith("-renamed")
    client.vms.update(vm.id, name=vm.name)

    with pytest.raises(NotFoundError):
        client.vms.retrieve("vm_does_not_exist_000000")

    q = client.quotas.retrieve()
    assert q.limits is not None and q.usage is not None


def test_file_transfer(client: FastvmClient, vm: Vm, workdir: str, tmp_path: Path) -> None:
    # 1. Regular file: roundtrip preserves content.
    src = tmp_path / "hello.txt"
    payload = "héllo wörld\n" * 100  # unicode payload
    src.write_text(payload, encoding="utf-8")
    client.upload(vm.id, str(src), f"{workdir}/hello.txt")
    assert client.vms.run(vm.id, command=["cat", f"{workdir}/hello.txt"]).stdout == payload

    # 2. Overwrite: second upload to same remote path replaces content.
    src.write_text("v2\n", encoding="utf-8")
    client.upload(vm.id, str(src), f"{workdir}/hello.txt")
    assert client.vms.run(vm.id, command=["cat", f"{workdir}/hello.txt"]).stdout == "v2\n"

    # 3. Empty file: zero-byte content survives the presign/PUT/fetch path.
    empty = tmp_path / "empty.bin"
    empty.write_bytes(b"")
    client.upload(vm.id, str(empty), f"{workdir}/empty.bin")
    wc = client.vms.run(vm.id, command=["wc", "-c", f"{workdir}/empty.bin"])
    assert wc.stdout.split()[0] == "0"

    # 4. Unicode filename: no client-side quoting or path-encoding surprises.
    uni = tmp_path / "ünîçødé fïlé.txt"
    uni.write_text("u\n", encoding="utf-8")
    client.upload(vm.id, str(uni), f"{workdir}/ünîçødé fïlé.txt")

    # 5. Download: full roundtrip + verify unicode payload integrity.
    dst = tmp_path / "hello.back.txt"
    client.download(vm.id, f"{workdir}/hello.txt", str(dst))
    assert dst.read_text(encoding="utf-8") == "v2\n"

    # 6. Missing path on download raises FileNotFoundError (not HTTP 4xx).
    with pytest.raises(FileNotFoundError):
        client.download(vm.id, f"{workdir}/does-not-exist", str(tmp_path / "out"))


def test_directory_transfer(client: FastvmClient, vm: Vm, workdir: str, tmp_path: Path) -> None:
    # Build a local tree: top-level file, nested file, and an empty subdir.
    src = tmp_path / "src"
    (src / "sub").mkdir(parents=True)
    (src / "empty").mkdir()
    (src / "a.txt").write_text("alpha\n")
    (src / "sub" / "b.txt").write_text("beta\n")

    # 1. Upload: all files + empty directory preserved server-side.
    client.upload(vm.id, str(src), f"{workdir}/uploaded")
    assert client.vms.run(vm.id, command=["cat", f"{workdir}/uploaded/a.txt"]).stdout == "alpha\n"
    assert (
        client.vms.run(vm.id, command=["cat", f"{workdir}/uploaded/sub/b.txt"]).stdout == "beta\n"
    )
    empty_check = client.vms.run(vm.id, command=["test", "-d", f"{workdir}/uploaded/empty"])
    assert empty_check.exit_code == 0

    # 2. Download into a pre-existing local dir (merge, not clobber-replace).
    dst = tmp_path / "back"
    dst.mkdir()
    (dst / "preexisting.txt").write_text("keep\n")
    client.download(vm.id, f"{workdir}/uploaded", str(dst))
    assert (dst / "a.txt").read_text() == "alpha\n"
    assert (dst / "sub" / "b.txt").read_text() == "beta\n"
    assert (dst / "empty").is_dir()
    assert (dst / "preexisting.txt").read_text() == "keep\n"
