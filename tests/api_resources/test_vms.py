# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import (
    VmInstance,
    DeleteResponse,
    VmListResponse,
    VmExecuteCommandResponse,
    VmIssueConsoleTokenResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVms:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Fastvm) -> None:
        vm = client.vms.create()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.create(
            disk_gi_b=10,
            firewall={
                "mode": "open",
                "ingress": [
                    {
                        "port_start": 1,
                        "protocol": "tcp",
                        "description": "description",
                        "port_end": 1,
                        "source_cidrs": ["string"],
                    }
                ],
            },
            machine_type="c1m2",
            name="name",
            snapshot_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmInstance, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Fastvm) -> None:
        vm = client.vms.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmInstance, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Fastvm) -> None:
        vm = client.vms.list()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmListResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Fastvm) -> None:
        vm = client.vms.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DeleteResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(DeleteResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(DeleteResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_execute_command(self, client: Fastvm) -> None:
        vm = client.vms.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
        )
        assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_execute_command_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
            timeout_sec=1,
        )
        assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_execute_command(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_execute_command(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_execute_command(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.execute_command(
                id="",
                command=["string"],
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_issue_console_token(self, client: Fastvm) -> None:
        vm = client.vms.issue_console_token(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VmIssueConsoleTokenResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_issue_console_token(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.issue_console_token(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmIssueConsoleTokenResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_issue_console_token(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.issue_console_token(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmIssueConsoleTokenResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_issue_console_token(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.issue_console_token(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_rename(self, client: Fastvm) -> None:
        vm = client.vms.rename(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_rename(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.rename(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_rename(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.rename(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmInstance, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_rename(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.rename(
                id="",
                name="name",
            )


class TestAsyncVms:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.create()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.create(
            disk_gi_b=10,
            firewall={
                "mode": "open",
                "ingress": [
                    {
                        "port_start": 1,
                        "protocol": "tcp",
                        "description": "description",
                        "port_end": 1,
                        "source_cidrs": ["string"],
                    }
                ],
            },
            machine_type="c1m2",
            name="name",
            snapshot_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmInstance, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmInstance, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.list()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmListResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DeleteResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(DeleteResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(DeleteResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_execute_command(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
        )
        assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_execute_command_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
            timeout_sec=1,
        )
        assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_execute_command(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_execute_command(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.execute_command(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            command=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmExecuteCommandResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_execute_command(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.execute_command(
                id="",
                command=["string"],
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_issue_console_token(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.issue_console_token(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VmIssueConsoleTokenResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_issue_console_token(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.issue_console_token(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmIssueConsoleTokenResponse, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_issue_console_token(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.issue_console_token(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmIssueConsoleTokenResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_issue_console_token(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.issue_console_token(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_rename(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.rename(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_rename(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.rename(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmInstance, vm, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_rename(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.rename(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmInstance, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_rename(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.rename(
                id="",
                name="name",
            )
