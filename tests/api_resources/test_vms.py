# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fastvm import Fastvm, AsyncFastvm
from tests.utils import assert_matches_type
from fastvm.types import (
    Vm,
    ExecResult,
    ConsoleToken,
    VmListResponse,
    VmDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVms:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Fastvm) -> None:
        vm = client.vms.retrieve(
            "id",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Fastvm) -> None:
        vm = client.vms.update(
            id="id",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.update(
            id="id",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Fastvm) -> None:
        vm = client.vms.list()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmListResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Fastvm) -> None:
        vm = client.vms.delete(
            "id",
        )
        assert_matches_type(VmDeleteResponse, vm, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(VmDeleteResponse, vm, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(VmDeleteResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_console_token(self, client: Fastvm) -> None:
        vm = client.vms.console_token(
            "id",
        )
        assert_matches_type(ConsoleToken, vm, path=["response"])

    @parametrize
    def test_raw_response_console_token(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.console_token(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(ConsoleToken, vm, path=["response"])

    @parametrize
    def test_streaming_response_console_token(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.console_token(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(ConsoleToken, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_console_token(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.console_token(
                "",
            )

    @parametrize
    def test_method_launch(self, client: Fastvm) -> None:
        vm = client.vms.launch()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_method_launch_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.launch(
            disk_gi_b=0,
            firewall={
                "mode": "mode",
                "ingress": [
                    {
                        "port_start": 0,
                        "protocol": "protocol",
                        "description": "description",
                        "port_end": 0,
                        "source_cidrs": ["string"],
                    }
                ],
            },
            machine_type="machineType",
            metadata={"foo": "string"},
            name="name",
            snapshot_id="snapshotId",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_raw_response_launch(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.launch()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_streaming_response_launch(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.launch() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_patch_firewall(self, client: Fastvm) -> None:
        vm = client.vms.patch_firewall(
            id="id",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_method_patch_firewall_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.patch_firewall(
            id="id",
            ingress=[
                {
                    "port_start": 0,
                    "protocol": "protocol",
                    "description": "description",
                    "port_end": 0,
                    "source_cidrs": ["string"],
                }
            ],
            mode="mode",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_raw_response_patch_firewall(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.patch_firewall(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_streaming_response_patch_firewall(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.patch_firewall(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_patch_firewall(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.patch_firewall(
                id="",
            )

    @parametrize
    def test_method_run(self, client: Fastvm) -> None:
        vm = client.vms.run(
            id="id",
            command=["string"],
        )
        assert_matches_type(ExecResult, vm, path=["response"])

    @parametrize
    def test_method_run_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.run(
            id="id",
            command=["string"],
            timeout_sec=1,
        )
        assert_matches_type(ExecResult, vm, path=["response"])

    @parametrize
    def test_raw_response_run(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.run(
            id="id",
            command=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(ExecResult, vm, path=["response"])

    @parametrize
    def test_streaming_response_run(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.run(
            id="id",
            command=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(ExecResult, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_run(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.run(
                id="",
                command=["string"],
            )

    @parametrize
    def test_method_set_firewall(self, client: Fastvm) -> None:
        vm = client.vms.set_firewall(
            id="id",
            mode="mode",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_method_set_firewall_with_all_params(self, client: Fastvm) -> None:
        vm = client.vms.set_firewall(
            id="id",
            mode="mode",
            ingress=[
                {
                    "port_start": 0,
                    "protocol": "protocol",
                    "description": "description",
                    "port_end": 0,
                    "source_cidrs": ["string"],
                }
            ],
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_raw_response_set_firewall(self, client: Fastvm) -> None:
        response = client.vms.with_raw_response.set_firewall(
            id="id",
            mode="mode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    def test_streaming_response_set_firewall(self, client: Fastvm) -> None:
        with client.vms.with_streaming_response.set_firewall(
            id="id",
            mode="mode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_set_firewall(self, client: Fastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vms.with_raw_response.set_firewall(
                id="",
                mode="mode",
            )


class TestAsyncVms:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.retrieve(
            "id",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.update(
            id="id",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.update(
            id="id",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.list()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmListResponse, vm, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmListResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.delete(
            "id",
        )
        assert_matches_type(VmDeleteResponse, vm, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(VmDeleteResponse, vm, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(VmDeleteResponse, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_console_token(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.console_token(
            "id",
        )
        assert_matches_type(ConsoleToken, vm, path=["response"])

    @parametrize
    async def test_raw_response_console_token(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.console_token(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(ConsoleToken, vm, path=["response"])

    @parametrize
    async def test_streaming_response_console_token(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.console_token(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(ConsoleToken, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_console_token(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.console_token(
                "",
            )

    @parametrize
    async def test_method_launch(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.launch()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_method_launch_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.launch(
            disk_gi_b=0,
            firewall={
                "mode": "mode",
                "ingress": [
                    {
                        "port_start": 0,
                        "protocol": "protocol",
                        "description": "description",
                        "port_end": 0,
                        "source_cidrs": ["string"],
                    }
                ],
            },
            machine_type="machineType",
            metadata={"foo": "string"},
            name="name",
            snapshot_id="snapshotId",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_raw_response_launch(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.launch()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_streaming_response_launch(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.launch() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_patch_firewall(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.patch_firewall(
            id="id",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_method_patch_firewall_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.patch_firewall(
            id="id",
            ingress=[
                {
                    "port_start": 0,
                    "protocol": "protocol",
                    "description": "description",
                    "port_end": 0,
                    "source_cidrs": ["string"],
                }
            ],
            mode="mode",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_raw_response_patch_firewall(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.patch_firewall(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_streaming_response_patch_firewall(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.patch_firewall(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_patch_firewall(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.patch_firewall(
                id="",
            )

    @parametrize
    async def test_method_run(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.run(
            id="id",
            command=["string"],
        )
        assert_matches_type(ExecResult, vm, path=["response"])

    @parametrize
    async def test_method_run_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.run(
            id="id",
            command=["string"],
            timeout_sec=1,
        )
        assert_matches_type(ExecResult, vm, path=["response"])

    @parametrize
    async def test_raw_response_run(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.run(
            id="id",
            command=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(ExecResult, vm, path=["response"])

    @parametrize
    async def test_streaming_response_run(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.run(
            id="id",
            command=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(ExecResult, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_run(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.run(
                id="",
                command=["string"],
            )

    @parametrize
    async def test_method_set_firewall(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.set_firewall(
            id="id",
            mode="mode",
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_method_set_firewall_with_all_params(self, async_client: AsyncFastvm) -> None:
        vm = await async_client.vms.set_firewall(
            id="id",
            mode="mode",
            ingress=[
                {
                    "port_start": 0,
                    "protocol": "protocol",
                    "description": "description",
                    "port_end": 0,
                    "source_cidrs": ["string"],
                }
            ],
        )
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_raw_response_set_firewall(self, async_client: AsyncFastvm) -> None:
        response = await async_client.vms.with_raw_response.set_firewall(
            id="id",
            mode="mode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vm = await response.parse()
        assert_matches_type(Vm, vm, path=["response"])

    @parametrize
    async def test_streaming_response_set_firewall(self, async_client: AsyncFastvm) -> None:
        async with async_client.vms.with_streaming_response.set_firewall(
            id="id",
            mode="mode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vm = await response.parse()
            assert_matches_type(Vm, vm, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_set_firewall(self, async_client: AsyncFastvm) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vms.with_raw_response.set_firewall(
                id="",
                mode="mode",
            )
