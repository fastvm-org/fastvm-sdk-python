# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ...types import vm_create_params, vm_rename_params, vm_execute_command_params
from .console import (
    ConsoleResource,
    AsyncConsoleResource,
    ConsoleResourceWithRawResponse,
    AsyncConsoleResourceWithRawResponse,
    ConsoleResourceWithStreamingResponse,
    AsyncConsoleResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from .firewall import (
    FirewallResource,
    AsyncFirewallResource,
    FirewallResourceWithRawResponse,
    AsyncFirewallResourceWithRawResponse,
    FirewallResourceWithStreamingResponse,
    AsyncFirewallResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.vm_instance import VmInstance
from ...types.delete_response import DeleteResponse
from ...types.vm_list_response import VmListResponse
from ...types.vms.firewall_policy_param import FirewallPolicyParam
from ...types.vm_execute_command_response import VmExecuteCommandResponse
from ...types.vm_issue_console_token_response import VmIssueConsoleTokenResponse

__all__ = ["VmsResource", "AsyncVmsResource"]


class VmsResource(SyncAPIResource):
    @cached_property
    def firewall(self) -> FirewallResource:
        return FirewallResource(self._client)

    @cached_property
    def console(self) -> ConsoleResource:
        return ConsoleResource(self._client)

    @cached_property
    def with_raw_response(self) -> VmsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return VmsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VmsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return VmsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        disk_gi_b: int | Omit = omit,
        firewall: FirewallPolicyParam | Omit = omit,
        machine_type: Literal["c1m2", "c2m4", "c4m8", "c8m16"] | Omit = omit,
        name: str | Omit = omit,
        snapshot_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """
        Create VM from a base image or snapshot

        Args:
          disk_gi_b: Optional grow-only disk size in GiB. Must be >= base machine disk (10 GiB) or >=
              source snapshot VM disk.

          firewall: Public IPv6 ingress firewall policy captured from the source VM at snapshot
              time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/vms",
            body=maybe_transform(
                {
                    "disk_gi_b": disk_gi_b,
                    "firewall": firewall,
                    "machine_type": machine_type,
                    "name": name,
                    "snapshot_id": snapshot_id,
                },
                vm_create_params.VmCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """
        Get a single VM by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/vms/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmListResponse:
        """List VMs for the authenticated organization"""
        return self._get(
            "/v1/vms",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete a VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            path_template("/v1/vms/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def execute_command(
        self,
        id: str,
        *,
        command: SequenceNotStr[str],
        timeout_sec: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmExecuteCommandResponse:
        """
        Execute a one-off command inside a running VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/vms/{id}/exec", id=id),
            body=maybe_transform(
                {
                    "command": command,
                    "timeout_sec": timeout_sec,
                },
                vm_execute_command_params.VmExecuteCommandParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmExecuteCommandResponse,
        )

    def issue_console_token(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmIssueConsoleTokenResponse:
        """
        Issue one-time token for websocket console access

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/vms/{id}/console-token", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmIssueConsoleTokenResponse,
        )

    def rename(
        self,
        id: str,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """
        Rename a VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/v1/vms/{id}", id=id),
            body=maybe_transform({"name": name}, vm_rename_params.VmRenameParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )


class AsyncVmsResource(AsyncAPIResource):
    @cached_property
    def firewall(self) -> AsyncFirewallResource:
        return AsyncFirewallResource(self._client)

    @cached_property
    def console(self) -> AsyncConsoleResource:
        return AsyncConsoleResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVmsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVmsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVmsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return AsyncVmsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        disk_gi_b: int | Omit = omit,
        firewall: FirewallPolicyParam | Omit = omit,
        machine_type: Literal["c1m2", "c2m4", "c4m8", "c8m16"] | Omit = omit,
        name: str | Omit = omit,
        snapshot_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """
        Create VM from a base image or snapshot

        Args:
          disk_gi_b: Optional grow-only disk size in GiB. Must be >= base machine disk (10 GiB) or >=
              source snapshot VM disk.

          firewall: Public IPv6 ingress firewall policy captured from the source VM at snapshot
              time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/vms",
            body=await async_maybe_transform(
                {
                    "disk_gi_b": disk_gi_b,
                    "firewall": firewall,
                    "machine_type": machine_type,
                    "name": name,
                    "snapshot_id": snapshot_id,
                },
                vm_create_params.VmCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """
        Get a single VM by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/vms/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmListResponse:
        """List VMs for the authenticated organization"""
        return await self._get(
            "/v1/vms",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteResponse:
        """
        Delete a VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            path_template("/v1/vms/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def execute_command(
        self,
        id: str,
        *,
        command: SequenceNotStr[str],
        timeout_sec: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmExecuteCommandResponse:
        """
        Execute a one-off command inside a running VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/vms/{id}/exec", id=id),
            body=await async_maybe_transform(
                {
                    "command": command,
                    "timeout_sec": timeout_sec,
                },
                vm_execute_command_params.VmExecuteCommandParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmExecuteCommandResponse,
        )

    async def issue_console_token(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmIssueConsoleTokenResponse:
        """
        Issue one-time token for websocket console access

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/vms/{id}/console-token", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmIssueConsoleTokenResponse,
        )

    async def rename(
        self,
        id: str,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """
        Rename a VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/v1/vms/{id}", id=id),
            body=await async_maybe_transform({"name": name}, vm_rename_params.VmRenameParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )


class VmsResourceWithRawResponse:
    def __init__(self, vms: VmsResource) -> None:
        self._vms = vms

        self.create = to_raw_response_wrapper(
            vms.create,
        )
        self.retrieve = to_raw_response_wrapper(
            vms.retrieve,
        )
        self.list = to_raw_response_wrapper(
            vms.list,
        )
        self.delete = to_raw_response_wrapper(
            vms.delete,
        )
        self.execute_command = to_raw_response_wrapper(
            vms.execute_command,
        )
        self.issue_console_token = to_raw_response_wrapper(
            vms.issue_console_token,
        )
        self.rename = to_raw_response_wrapper(
            vms.rename,
        )

    @cached_property
    def firewall(self) -> FirewallResourceWithRawResponse:
        return FirewallResourceWithRawResponse(self._vms.firewall)

    @cached_property
    def console(self) -> ConsoleResourceWithRawResponse:
        return ConsoleResourceWithRawResponse(self._vms.console)


class AsyncVmsResourceWithRawResponse:
    def __init__(self, vms: AsyncVmsResource) -> None:
        self._vms = vms

        self.create = async_to_raw_response_wrapper(
            vms.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            vms.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            vms.list,
        )
        self.delete = async_to_raw_response_wrapper(
            vms.delete,
        )
        self.execute_command = async_to_raw_response_wrapper(
            vms.execute_command,
        )
        self.issue_console_token = async_to_raw_response_wrapper(
            vms.issue_console_token,
        )
        self.rename = async_to_raw_response_wrapper(
            vms.rename,
        )

    @cached_property
    def firewall(self) -> AsyncFirewallResourceWithRawResponse:
        return AsyncFirewallResourceWithRawResponse(self._vms.firewall)

    @cached_property
    def console(self) -> AsyncConsoleResourceWithRawResponse:
        return AsyncConsoleResourceWithRawResponse(self._vms.console)


class VmsResourceWithStreamingResponse:
    def __init__(self, vms: VmsResource) -> None:
        self._vms = vms

        self.create = to_streamed_response_wrapper(
            vms.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            vms.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            vms.list,
        )
        self.delete = to_streamed_response_wrapper(
            vms.delete,
        )
        self.execute_command = to_streamed_response_wrapper(
            vms.execute_command,
        )
        self.issue_console_token = to_streamed_response_wrapper(
            vms.issue_console_token,
        )
        self.rename = to_streamed_response_wrapper(
            vms.rename,
        )

    @cached_property
    def firewall(self) -> FirewallResourceWithStreamingResponse:
        return FirewallResourceWithStreamingResponse(self._vms.firewall)

    @cached_property
    def console(self) -> ConsoleResourceWithStreamingResponse:
        return ConsoleResourceWithStreamingResponse(self._vms.console)


class AsyncVmsResourceWithStreamingResponse:
    def __init__(self, vms: AsyncVmsResource) -> None:
        self._vms = vms

        self.create = async_to_streamed_response_wrapper(
            vms.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            vms.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            vms.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            vms.delete,
        )
        self.execute_command = async_to_streamed_response_wrapper(
            vms.execute_command,
        )
        self.issue_console_token = async_to_streamed_response_wrapper(
            vms.issue_console_token,
        )
        self.rename = async_to_streamed_response_wrapper(
            vms.rename,
        )

    @cached_property
    def firewall(self) -> AsyncFirewallResourceWithStreamingResponse:
        return AsyncFirewallResourceWithStreamingResponse(self._vms.firewall)

    @cached_property
    def console(self) -> AsyncConsoleResourceWithStreamingResponse:
        return AsyncConsoleResourceWithStreamingResponse(self._vms.console)
