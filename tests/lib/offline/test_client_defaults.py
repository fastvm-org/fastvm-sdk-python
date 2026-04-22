"""Construction-time behaviors: HTTP/2 on by default, escape hatches work."""

from __future__ import annotations

from typing import Any, Union, cast

import httpx
import pytest

from fastvm import FastvmClient, AsyncFastvmClient
from fastvm.lib._client import _VmsResourceExt, _AsyncVmsResourceExt


def _http2_enabled(hx: Union[httpx.Client, httpx.AsyncClient]) -> bool:
    # httpx has no public ``http2`` attribute; dig into the pool.
    pool = cast(Any, hx._transport)._pool  # type: ignore[attr-defined]
    return bool(pool._http2)


def test_sync_defaults_to_http2():
    client = FastvmClient(api_key="k", base_url="http://example.invalid")
    assert _http2_enabled(client._client) is True
    assert isinstance(client.vms, _VmsResourceExt)
    client.close()


def test_async_defaults_to_http2():
    client = AsyncFastvmClient(api_key="k", base_url="http://example.invalid")
    assert _http2_enabled(client._client) is True
    assert isinstance(client.vms, _AsyncVmsResourceExt)


def test_http2_can_be_disabled():
    client = FastvmClient(api_key="k", base_url="http://example.invalid", http2=False)
    # Stainless's default httpx.Client is HTTP/1.1 only.
    assert _http2_enabled(client._client) is False
    client.close()


def test_user_http_client_wins():
    custom = httpx.Client()
    client = FastvmClient(api_key="k", base_url="http://example.invalid", http_client=custom)
    assert client._client is custom
    client.close()


def test_empty_base_url_env_falls_back_to_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """``FASTVM_BASE_URL=""`` must not produce an empty base URL.

    Upstream Stainless template bug — see openai-python#2927. Our
    ``_normalize_base_url`` shim pre-resolves the env var so the generated
    fallback chain hits the hardcoded production URL.
    """
    monkeypatch.setenv("FASTVM_BASE_URL", "")
    client = FastvmClient(api_key="k")
    try:
        assert str(client.base_url).rstrip("/") == "https://api.fastvm.org"
    finally:
        client.close()


def test_empty_explicit_base_url_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Passing ``base_url=""`` explicitly is also treated as unset."""
    monkeypatch.delenv("FASTVM_BASE_URL", raising=False)
    client = FastvmClient(api_key="k", base_url="")
    try:
        assert str(client.base_url).rstrip("/") == "https://api.fastvm.org"
    finally:
        client.close()
