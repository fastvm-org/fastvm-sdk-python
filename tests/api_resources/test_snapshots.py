# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import (
    Snapshot,
    SnapshotListResponse,
    SnapshotDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSnapshots:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Fastvm) -> None:
        snapshot = client.snapshots.create(
            vm_id="vmId",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Fastvm) -> None:
        snapshot = client.snapshots.create(
            vm_id="vmId",
            name="name",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Fastvm) -> None:
        response = client.snapshots.with_raw_response.create(
            vm_id="vmId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Fastvm) -> None:
        with client.snapshots.with_streaming_response.create(
            vm_id="vmId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(Snapshot, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Fastvm) -> None:
        snapshot = client.snapshots.update(
            id="id",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Fastvm) -> None:
        snapshot = client.snapshots.update(
            id="id",
            name="name",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Fastvm) -> None:
        response = client.snapshots.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Fastvm) -> None:
        with client.snapshots.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(Snapshot, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.snapshots.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Fastvm) -> None:
        snapshot = client.snapshots.list()
        assert_matches_type(SnapshotListResponse, snapshot, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Fastvm) -> None:
        response = client.snapshots.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(SnapshotListResponse, snapshot, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Fastvm) -> None:
        with client.snapshots.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(SnapshotListResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Fastvm) -> None:
        snapshot = client.snapshots.delete(
            "id",
        )
        assert_matches_type(SnapshotDeleteResponse, snapshot, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Fastvm) -> None:
        response = client.snapshots.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(SnapshotDeleteResponse, snapshot, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Fastvm) -> None:
        with client.snapshots.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(SnapshotDeleteResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.snapshots.with_raw_response.delete(
                "",
            )


class TestAsyncSnapshots:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncFastvm) -> None:
        snapshot = await async_client.snapshots.create(
            vm_id="vmId",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFastvm) -> None:
        snapshot = await async_client.snapshots.create(
            vm_id="vmId",
            name="name",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFastvm) -> None:
        response = await async_client.snapshots.with_raw_response.create(
            vm_id="vmId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFastvm) -> None:
        async with async_client.snapshots.with_streaming_response.create(
            vm_id="vmId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(Snapshot, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncFastvm) -> None:
        snapshot = await async_client.snapshots.update(
            id="id",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFastvm) -> None:
        snapshot = await async_client.snapshots.update(
            id="id",
            name="name",
        )
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFastvm) -> None:
        response = await async_client.snapshots.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(Snapshot, snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFastvm) -> None:
        async with async_client.snapshots.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(Snapshot, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.snapshots.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncFastvm) -> None:
        snapshot = await async_client.snapshots.list()
        assert_matches_type(SnapshotListResponse, snapshot, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFastvm) -> None:
        response = await async_client.snapshots.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(SnapshotListResponse, snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFastvm) -> None:
        async with async_client.snapshots.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(SnapshotListResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncFastvm) -> None:
        snapshot = await async_client.snapshots.delete(
            "id",
        )
        assert_matches_type(SnapshotDeleteResponse, snapshot, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFastvm) -> None:
        response = await async_client.snapshots.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(SnapshotDeleteResponse, snapshot, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFastvm) -> None:
        async with async_client.snapshots.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(SnapshotDeleteResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.snapshots.with_raw_response.delete(
                "",
            )
