"""Round-trip pack/unpack: gzip tar stream of a dir extracts identically."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from fastvm.lib._tarutil import pack_directory_to_stream, unpack_stream_to_directory


def _populate(root: Path) -> None:
    (root / "a.txt").write_text("hello\n")
    (root / "subdir").mkdir()
    (root / "subdir" / "b.txt").write_text("world\n")
    (root / "subdir" / "empty").mkdir()


def test_roundtrip_preserves_contents(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    _populate(src)

    buf = io.BytesIO()
    for chunk in pack_directory_to_stream(str(src)):
        buf.write(chunk)
    buf.seek(0)

    dst = tmp_path / "dst"
    unpack_stream_to_directory(buf, str(dst))

    assert (dst / "a.txt").read_text() == "hello\n"
    assert (dst / "subdir" / "b.txt").read_text() == "world\n"
    assert (dst / "subdir" / "empty").is_dir()
    # Archive contents are rooted at ``.``, so no ``src/`` prefix appears.
    assert not (dst / "src").exists()


def test_missing_dir_raises(tmp_path: Path) -> None:
    missing = tmp_path / "nope"
    with pytest.raises(NotADirectoryError):
        list(pack_directory_to_stream(str(missing)))


def test_file_path_raises(tmp_path: Path) -> None:
    f = tmp_path / "f"
    f.write_text("x")
    with pytest.raises(NotADirectoryError):
        list(pack_directory_to_stream(str(f)))
