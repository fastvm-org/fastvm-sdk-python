# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConsole:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_websocket(self, client: Fastvm) -> None:
        console = client.vms.console.websocket(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            session="session",
        )
        assert console is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_websocket(self, client: Fastvm) -> None:
        response = client.vms.console.with_raw_response.websocket(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            session="session",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        console = response.parse()
        assert console is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_websocket(self, client: Fastvm) -> None:
        with client.vms.console.with_streaming_response.websocket(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            session="session",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            console = response.parse()
            assert console is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_websocket(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.console.with_raw_response.websocket(
                id="",
                session="session",
            )


class TestAsyncConsole:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_websocket(self, async_client: AsyncFastvm) -> None:
        console = await async_client.vms.console.websocket(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            session="session",
        )
        assert console is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_websocket(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.console.with_raw_response.websocket(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            session="session",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        console = await response.parse()
        assert console is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_websocket(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.console.with_streaming_response.websocket(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            session="session",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            console = await response.parse()
            assert console is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_websocket(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.console.with_raw_response.websocket(
                id="",
                session="session",
            )
