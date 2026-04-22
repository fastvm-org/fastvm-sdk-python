# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.vms import firewall_patch_policy_params, firewall_replace_policy_params
from ..._base_client import make_request_options
from ...types.vm_instance import VmInstance
from ...types.vms.firewall_rule_param import FirewallRuleParam

__all__ = ["FirewallResource", "AsyncFirewallResource"]


class FirewallResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FirewallResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#accessing-raw-response-data-eg-headers
        """
        return FirewallResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FirewallResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#with_streaming_response
        """
        return FirewallResourceWithStreamingResponse(self)

    def patch_policy(
        self,
        id: str,
        *,
        ingress: Iterable[FirewallRuleParam] | Omit = omit,
        mode: Literal["open", "restricted"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """Partially updates the VM's public IPv6 ingress policy.

        This does not affect the
        internal IPv4 path used by platform control and exec.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/v1/vms/{id}/firewall", id=id),
            body=maybe_transform(
                {
                    "ingress": ingress,
                    "mode": mode,
                },
                firewall_patch_policy_params.FirewallPatchPolicyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )

    def replace_policy(
        self,
        id: str,
        *,
        mode: Literal["open", "restricted"],
        ingress: Iterable[FirewallRuleParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """Replaces the VM's public IPv6 ingress policy.

        This does not affect the internal
        IPv4 path used by platform control and exec.

        Args:
          ingress: Allow rules evaluated only when `mode` is `restricted`. If empty, all public
              IPv6 ports are closed except essential ICMPv6 control traffic.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._put(
            path_template("/v1/vms/{id}/firewall", id=id),
            body=maybe_transform(
                {
                    "mode": mode,
                    "ingress": ingress,
                },
                firewall_replace_policy_params.FirewallReplacePolicyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )


class AsyncFirewallResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFirewallResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFirewallResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFirewallResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#with_streaming_response
        """
        return AsyncFirewallResourceWithStreamingResponse(self)

    async def patch_policy(
        self,
        id: str,
        *,
        ingress: Iterable[FirewallRuleParam] | Omit = omit,
        mode: Literal["open", "restricted"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """Partially updates the VM's public IPv6 ingress policy.

        This does not affect the
        internal IPv4 path used by platform control and exec.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/v1/vms/{id}/firewall", id=id),
            body=await async_maybe_transform(
                {
                    "ingress": ingress,
                    "mode": mode,
                },
                firewall_patch_policy_params.FirewallPatchPolicyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )

    async def replace_policy(
        self,
        id: str,
        *,
        mode: Literal["open", "restricted"],
        ingress: Iterable[FirewallRuleParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VmInstance:
        """Replaces the VM's public IPv6 ingress policy.

        This does not affect the internal
        IPv4 path used by platform control and exec.

        Args:
          ingress: Allow rules evaluated only when `mode` is `restricted`. If empty, all public
              IPv6 ports are closed except essential ICMPv6 control traffic.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._put(
            path_template("/v1/vms/{id}/firewall", id=id),
            body=await async_maybe_transform(
                {
                    "mode": mode,
                    "ingress": ingress,
                },
                firewall_replace_policy_params.FirewallReplacePolicyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmInstance,
        )


class FirewallResourceWithRawResponse:
    def __init__(self, firewall: FirewallResource) -> None:
        self._firewall = firewall

        self.patch_policy = to_raw_response_wrapper(
            firewall.patch_policy,
        )
        self.replace_policy = to_raw_response_wrapper(
            firewall.replace_policy,
        )


class AsyncFirewallResourceWithRawResponse:
    def __init__(self, firewall: AsyncFirewallResource) -> None:
        self._firewall = firewall

        self.patch_policy = async_to_raw_response_wrapper(
            firewall.patch_policy,
        )
        self.replace_policy = async_to_raw_response_wrapper(
            firewall.replace_policy,
        )


class FirewallResourceWithStreamingResponse:
    def __init__(self, firewall: FirewallResource) -> None:
        self._firewall = firewall

        self.patch_policy = to_streamed_response_wrapper(
            firewall.patch_policy,
        )
        self.replace_policy = to_streamed_response_wrapper(
            firewall.replace_policy,
        )


class AsyncFirewallResourceWithStreamingResponse:
    def __init__(self, firewall: AsyncFirewallResource) -> None:
        self._firewall = firewall

        self.patch_policy = async_to_streamed_response_wrapper(
            firewall.patch_policy,
        )
        self.replace_policy = async_to_streamed_response_wrapper(
            firewall.replace_policy,
        )
