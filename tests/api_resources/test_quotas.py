# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import OrgQuotaUsage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQuotas:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Fastvm) -> None:
        quota = client.quotas.retrieve()
        assert_matches_type(OrgQuotaUsage, quota, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Fastvm) -> None:
        response = client.quotas.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        quota = response.parse()
        assert_matches_type(OrgQuotaUsage, quota, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Fastvm) -> None:
        with client.quotas.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            quota = response.parse()
            assert_matches_type(OrgQuotaUsage, quota, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncQuotas:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFastvm) -> None:
        quota = await async_client.quotas.retrieve()
        assert_matches_type(OrgQuotaUsage, quota, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFastvm) -> None:
        response = await async_client.quotas.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        quota = await response.parse()
        assert_matches_type(OrgQuotaUsage, quota, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFastvm) -> None:
        async with async_client.quotas.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            quota = await response.parse()
            assert_matches_type(OrgQuotaUsage, quota, path=["response"])

        assert cast(Any, response.is_closed) is True
