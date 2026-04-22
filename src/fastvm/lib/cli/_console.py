"""Interactive WebSocket console for a FastVM VM.

Mirrors the frontend's shell-terminal: fetches a one-shot console token via
``POST /v1/vms/{id}/console-token``, connects over WebSocket, puts the local
terminal in raw mode, and bidirectionally pipes stdin/stdout.

Protocol:
  * Server → client: binary or text frames (raw TTY output)
  * Client → server: text frames (keystrokes)
  * Resize: JSON text frame ``{"type": "resize", "cols": N, "rows": N}``

Works on macOS, Linux, and Windows.
"""

from __future__ import annotations

import os
import re
import sys
import json
import shutil
import asyncio
from typing import TYPE_CHECKING

import websockets
import websockets.asyncio.client

if TYPE_CHECKING:
    from .._client import AsyncFastvmClient

_IS_WINDOWS = sys.platform == "win32"
_WS_SCHEME_RE = re.compile(r"^wss?://", re.I)
_ESCAPE_BYTE = b"\x1d"  # Ctrl-]
_ESCAPE_CHAR = "\x1d"
_CTRL_C_BYTE = b"\x03"
_CTRL_C_CHAR = "\x03"
_HINT = "\r\n(To disconnect, press Ctrl-])\r\n"
# Two Ctrl-C within this window prints the disconnect hint.
_CTRL_C_WINDOW = 1.0


def _build_ws_url(base_url: str, websocket_path: str, token: str) -> str:
    if _WS_SCHEME_RE.match(websocket_path):
        url = websocket_path
    else:
        ws_base = base_url.replace("https://", "wss://").replace("http://", "ws://").rstrip("/")
        sep = "" if websocket_path.startswith("/") else "/"
        url = f"{ws_base}{sep}{websocket_path}"
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}session={token}"


def _terminal_size() -> tuple[int, int]:
    cols, rows = shutil.get_terminal_size((80, 24))
    return cols, rows


# --- Unix raw-mode session ------------------------------------------------- #


class _UnixRawMode:
    """Context manager that puts the terminal in raw mode on Unix."""

    def __init__(self) -> None:
        import termios

        self._old_attrs = termios.tcgetattr(sys.stdin.fileno())

    def __enter__(self) -> None:
        import tty

        tty.setraw(sys.stdin.fileno())

    def __exit__(self, *_: object) -> None:
        import termios

        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self._old_attrs)


async def _unix_session(ws_url: str) -> None:
    import signal

    raw = _UnixRawMode()
    with raw:
        async with websockets.asyncio.client.connect(ws_url, max_size=2**20) as ws:
            cols, rows = _terminal_size()
            await ws.send(json.dumps({"type": "resize", "cols": cols, "rows": rows}))

            loop = asyncio.get_running_loop()
            stdin_fd = sys.stdin.fileno()
            stdout_fd = sys.stdout.fileno()
            queue: asyncio.Queue[bytes | None] = asyncio.Queue()
            last_ctrl_c = 0.0

            def _on_stdin_readable() -> None:
                nonlocal last_ctrl_c
                try:
                    data = os.read(stdin_fd, 4096)
                except OSError:
                    queue.put_nowait(None)
                    return
                if not data:
                    queue.put_nowait(None)
                    return
                if _ESCAPE_BYTE in data:
                    queue.put_nowait(None)
                    return
                if _CTRL_C_BYTE in data:
                    now = loop.time()
                    if now - last_ctrl_c < _CTRL_C_WINDOW:
                        os.write(stdout_fd, _HINT.encode())
                    last_ctrl_c = now
                queue.put_nowait(data)

            def _on_resize(_sig: int, _frame: object) -> None:
                c, r = _terminal_size()
                asyncio.ensure_future(ws.send(json.dumps({"type": "resize", "cols": c, "rows": r})))

            prev_handler = signal.signal(signal.SIGWINCH, _on_resize)
            loop.add_reader(stdin_fd, _on_stdin_readable)
            try:
                await asyncio.gather(_unix_forward_stdin(ws, queue), _read_ws(ws))
            finally:
                loop.remove_reader(stdin_fd)
                signal.signal(signal.SIGWINCH, prev_handler)


async def _unix_forward_stdin(
    ws: websockets.asyncio.client.ClientConnection,
    queue: asyncio.Queue[bytes | None],
) -> None:
    try:
        while True:
            data = await queue.get()
            if data is None:
                await ws.close()
                return
            await ws.send(data.decode("utf-8", errors="replace"))
    except (asyncio.CancelledError, websockets.exceptions.ConnectionClosed):
        pass


# --- Windows session ------------------------------------------------------- #


async def _win_session(ws_url: str) -> None:
    async with websockets.asyncio.client.connect(ws_url, max_size=2**20) as ws:
        cols, rows = _terminal_size()
        await ws.send(json.dumps({"type": "resize", "cols": cols, "rows": rows}))
        await asyncio.gather(_win_read_stdin(ws), _read_ws(ws), _win_poll_resize(ws))


async def _win_read_stdin(ws: websockets.asyncio.client.ClientConnection) -> None:
    import msvcrt

    loop = asyncio.get_running_loop()

    def _blocking_read() -> str | None:
        try:
            ch: str = msvcrt.getwch()  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]
            return ch
        except EOFError:
            return None

    last_ctrl_c = 0.0
    try:
        while True:
            ch = await loop.run_in_executor(None, _blocking_read)
            if ch is None:
                break
            if ch == _ESCAPE_CHAR:
                await ws.close()
                return
            if ch == _CTRL_C_CHAR:
                now = loop.time()
                if now - last_ctrl_c < _CTRL_C_WINDOW:
                    os.write(sys.stdout.fileno(), _HINT.encode())
                last_ctrl_c = now
            await ws.send(ch)
    except (asyncio.CancelledError, websockets.exceptions.ConnectionClosed):
        pass


async def _win_poll_resize(ws: websockets.asyncio.client.ClientConnection) -> None:
    last = _terminal_size()
    try:
        while True:
            await asyncio.sleep(1.0)
            current = _terminal_size()
            if current != last:
                last = current
                await ws.send(json.dumps({"type": "resize", "cols": current[0], "rows": current[1]}))
    except (asyncio.CancelledError, websockets.exceptions.ConnectionClosed):
        pass


async def _read_ws(ws: websockets.asyncio.client.ClientConnection) -> None:
    try:
        async for message in ws:
            if isinstance(message, bytes):
                os.write(sys.stdout.fileno(), message)
            else:
                os.write(sys.stdout.fileno(), message.encode("utf-8"))
    except (asyncio.CancelledError, websockets.exceptions.ConnectionClosed):
        pass


async def connect(client: "AsyncFastvmClient", vm_id: str) -> None:
    """Mint a console session token and run the interactive shell."""
    resp = await client.vms.console_token(vm_id)
    base_url = str(client.base_url).rstrip("/")
    ws_url = _build_ws_url(base_url, resp.websocket_path, resp.token)
    if _IS_WINDOWS:
        await _win_session(ws_url)
    else:
        await _unix_session(ws_url)
