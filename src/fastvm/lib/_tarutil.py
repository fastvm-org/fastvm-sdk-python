"""Streaming tar helpers used by directory upload/download.

These are plain sync functions. The async client runs them via ``anyio.to_thread``
so we don't block the event loop on disk/CPU-bound tar work.
"""

from __future__ import annotations

import os
import shlex
import tarfile
from typing import BinaryIO, Iterator


def pack_directory_to_stream(local_dir: str, *, chunk_size: int = 1 << 20) -> Iterator[bytes]:
    """Stream a gzipped tar of ``local_dir``'s **contents** as byte chunks.

    Equivalent to ``tar czf - -C <local_dir> .`` — the archive is rooted at
    ``.`` so extraction with ``tar xzf ... -C <dest>`` drops the children of
    ``local_dir`` directly into ``dest`` (no intermediate directory). Mirrors
    the VM-side ``tar czf - -C <remote_dir> .`` we use for downloads.
    """
    abs_dir = os.path.abspath(local_dir)
    if not os.path.isdir(abs_dir):
        raise NotADirectoryError(abs_dir)
    arcname = "."

    r, w = os.pipe()

    # tarfile writes into ``w``; we read from ``r`` and yield chunks.
    # We write synchronously in a background thread to decouple the two sides.
    import threading

    def _writer() -> None:
        try:
            with os.fdopen(w, "wb") as wf, tarfile.open(fileobj=wf, mode="w|gz") as tf:
                tf.add(abs_dir, arcname=arcname)
        except BaseException:
            # Close the write end so the reader sees EOF and wakes up.
            try:
                os.close(w)
            except OSError:
                pass
            raise

    t = threading.Thread(target=_writer, daemon=True, name="fastvm-tar-writer")
    t.start()
    try:
        with os.fdopen(r, "rb") as rf:
            while True:
                buf = rf.read(chunk_size)
                if not buf:
                    break
                yield buf
    finally:
        t.join(timeout=30)


def unpack_stream_to_directory(stream: BinaryIO, dest_dir: str) -> None:
    """Extract a gzipped tar stream into ``dest_dir``.

    ``dest_dir`` is created if it doesn't exist. Extraction uses ``tar`` mode
    ``r|gz`` which decodes on the fly — safe for streams without ``seek()``.
    """
    os.makedirs(dest_dir, exist_ok=True)
    with tarfile.open(fileobj=stream, mode="r|gz") as tf:
        # filter="data" rejects special files (devices, setuid) and strips
        # owner/mtime drift — matches tar's own --no-same-owner default.
        # It was added in 3.12; fall back to no filter on older runtimes.
        try:
            tf.extractall(dest_dir, filter="data")  # type: ignore[arg-type]
        except TypeError:
            tf.extractall(dest_dir)


def quote_sh(arg: str) -> str:
    """``shlex.quote`` re-exported so call sites read clearly."""
    return shlex.quote(arg)
