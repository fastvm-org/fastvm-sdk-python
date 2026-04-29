# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types.shared import FilePresignResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBuildContexts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_presign(self, client: Fastvm) -> None:
        build_context = client.build_contexts.presign()
        assert_matches_type(FilePresignResponse, build_context, path=["response"])

    @parametrize
    def test_raw_response_presign(self, client: Fastvm) -> None:
        response = client.build_contexts.with_raw_response.presign()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build_context = response.parse()
        assert_matches_type(FilePresignResponse, build_context, path=["response"])

    @parametrize
    def test_streaming_response_presign(self, client: Fastvm) -> None:
        with client.build_contexts.with_streaming_response.presign() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build_context = response.parse()
            assert_matches_type(FilePresignResponse, build_context, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBuildContexts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_presign(self, async_client: AsyncFastvm) -> None:
        build_context = await async_client.build_contexts.presign()
        assert_matches_type(FilePresignResponse, build_context, path=["response"])

    @parametrize
    async def test_raw_response_presign(self, async_client: AsyncFastvm) -> None:
        response = await async_client.build_contexts.with_raw_response.presign()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build_context = await response.parse()
        assert_matches_type(FilePresignResponse, build_context, path=["response"])

    @parametrize
    async def test_streaming_response_presign(self, async_client: AsyncFastvm) -> None:
        async with async_client.build_contexts.with_streaming_response.presign() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build_context = await response.parse()
            assert_matches_type(FilePresignResponse, build_context, path=["response"])

        assert cast(Any, response.is_closed) is True
