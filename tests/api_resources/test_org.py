# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import OrgRetrieveQuotasResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrg:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_quotas(self, client: Fastvm) -> None:
        org = client.org.retrieve_quotas()
        assert_matches_type(OrgRetrieveQuotasResponse, org, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve_quotas(self, client: Fastvm) -> None:
        response = client.org.with_raw_response.retrieve_quotas()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = response.parse()
        assert_matches_type(OrgRetrieveQuotasResponse, org, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_quotas(self, client: Fastvm) -> None:
        with client.org.with_streaming_response.retrieve_quotas() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = response.parse()
            assert_matches_type(OrgRetrieveQuotasResponse, org, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOrg:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_quotas(self, async_client: AsyncFastvm) -> None:
        org = await async_client.org.retrieve_quotas()
        assert_matches_type(OrgRetrieveQuotasResponse, org, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_quotas(self, async_client: AsyncFastvm) -> None:
        response = await async_client.org.with_raw_response.retrieve_quotas()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = await response.parse()
        assert_matches_type(OrgRetrieveQuotasResponse, org, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_quotas(self, async_client: AsyncFastvm) -> None:
        async with async_client.org.with_streaming_response.retrieve_quotas() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = await response.parse()
            assert_matches_type(OrgRetrieveQuotasResponse, org, path=["response"])

        assert cast(Any, response.is_closed) is True
