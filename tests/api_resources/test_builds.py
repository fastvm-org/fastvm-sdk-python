# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import BuildResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBuilds:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Fastvm) -> None:
        build = client.builds.create()
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Fastvm) -> None:
        build = client.builds.create(
            context_download_url="https://example.com",
            disk_gi_b=1,
            dockerfile_content="dockerfileContent",
            image_ref="imageRef",
            machine_type="machineType",
            name="name",
        )
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Fastvm) -> None:
        response = client.builds.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Fastvm) -> None:
        with client.builds.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(BuildResponse, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Fastvm) -> None:
        build = client.builds.retrieve(
            "id",
        )
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Fastvm) -> None:
        response = client.builds.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Fastvm) -> None:
        with client.builds.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(BuildResponse, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.builds.with_raw_response.retrieve(
                "",
            )


class TestAsyncBuilds:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncFastvm) -> None:
        build = await async_client.builds.create()
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFastvm) -> None:
        build = await async_client.builds.create(
            context_download_url="https://example.com",
            disk_gi_b=1,
            dockerfile_content="dockerfileContent",
            image_ref="imageRef",
            machine_type="machineType",
            name="name",
        )
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFastvm) -> None:
        response = await async_client.builds.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFastvm) -> None:
        async with async_client.builds.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(BuildResponse, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFastvm) -> None:
        build = await async_client.builds.retrieve(
            "id",
        )
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFastvm) -> None:
        response = await async_client.builds.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(BuildResponse, build, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFastvm) -> None:
        async with async_client.builds.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(BuildResponse, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.builds.with_raw_response.retrieve(
                "",
            )
