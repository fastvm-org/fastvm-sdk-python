# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import ExecResult
from fastvm.types.shared import FilePresignResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_fetch(self, client: Fastvm) -> None:
        file = client.vms.files.fetch(
            id="id",
            path="path",
            url="https://example.com",
        )
        assert_matches_type(ExecResult, file, path=["response"])

    @parametrize
    def test_method_fetch_with_all_params(self, client: Fastvm) -> None:
        file = client.vms.files.fetch(
            id="id",
            path="path",
            url="https://example.com",
            timeout_sec=0,
        )
        assert_matches_type(ExecResult, file, path=["response"])

    @parametrize
    def test_raw_response_fetch(self, client: Fastvm) -> None:
        response = client.vms.files.with_raw_response.fetch(
            id="id",
            path="path",
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(ExecResult, file, path=["response"])

    @parametrize
    def test_streaming_response_fetch(self, client: Fastvm) -> None:
        with client.vms.files.with_streaming_response.fetch(
            id="id",
            path="path",
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(ExecResult, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_fetch(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.files.with_raw_response.fetch(
                id="",
                path="path",
                url="https://example.com",
            )

    @parametrize
    def test_method_presign(self, client: Fastvm) -> None:
        file = client.vms.files.presign(
            id="id",
            path="path",
        )
        assert_matches_type(FilePresignResponse, file, path=["response"])

    @parametrize
    def test_raw_response_presign(self, client: Fastvm) -> None:
        response = client.vms.files.with_raw_response.presign(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FilePresignResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_presign(self, client: Fastvm) -> None:
        with client.vms.files.with_streaming_response.presign(
            id="id",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FilePresignResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_presign(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.files.with_raw_response.presign(
                id="",
                path="path",
            )


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_fetch(self, async_client: AsyncFastvm) -> None:
        file = await async_client.vms.files.fetch(
            id="id",
            path="path",
            url="https://example.com",
        )
        assert_matches_type(ExecResult, file, path=["response"])

    @parametrize
    async def test_method_fetch_with_all_params(self, async_client: AsyncFastvm) -> None:
        file = await async_client.vms.files.fetch(
            id="id",
            path="path",
            url="https://example.com",
            timeout_sec=0,
        )
        assert_matches_type(ExecResult, file, path=["response"])

    @parametrize
    async def test_raw_response_fetch(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.files.with_raw_response.fetch(
            id="id",
            path="path",
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(ExecResult, file, path=["response"])

    @parametrize
    async def test_streaming_response_fetch(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.files.with_streaming_response.fetch(
            id="id",
            path="path",
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(ExecResult, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_fetch(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.files.with_raw_response.fetch(
                id="",
                path="path",
                url="https://example.com",
            )

    @parametrize
    async def test_method_presign(self, async_client: AsyncFastvm) -> None:
        file = await async_client.vms.files.presign(
            id="id",
            path="path",
        )
        assert_matches_type(FilePresignResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_presign(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.files.with_raw_response.presign(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FilePresignResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_presign(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.files.with_streaming_response.presign(
            id="id",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FilePresignResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_presign(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.files.with_raw_response.presign(
                id="",
                path="path",
            )
