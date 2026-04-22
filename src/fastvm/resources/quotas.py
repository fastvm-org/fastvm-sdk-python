# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.org_quota_usage import OrgQuotaUsage

__all__ = ["QuotasResource", "AsyncQuotasResource"]


class QuotasResource(SyncAPIResource):
    """Org quotas and usage"""

    @cached_property
    def with_raw_response(self) -> QuotasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return QuotasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuotasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return QuotasResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrgQuotaUsage:
        """Get org quotas and usage"""
        return self._get(
            "/v1/org/quotas",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrgQuotaUsage,
        )


class AsyncQuotasResource(AsyncAPIResource):
    """Org quotas and usage"""

    @cached_property
    def with_raw_response(self) -> AsyncQuotasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncQuotasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuotasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return AsyncQuotasResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrgQuotaUsage:
        """Get org quotas and usage"""
        return await self._get(
            "/v1/org/quotas",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrgQuotaUsage,
        )


class QuotasResourceWithRawResponse:
    def __init__(self, quotas: QuotasResource) -> None:
        self._quotas = quotas

        self.retrieve = to_raw_response_wrapper(
            quotas.retrieve,
        )


class AsyncQuotasResourceWithRawResponse:
    def __init__(self, quotas: AsyncQuotasResource) -> None:
        self._quotas = quotas

        self.retrieve = async_to_raw_response_wrapper(
            quotas.retrieve,
        )


class QuotasResourceWithStreamingResponse:
    def __init__(self, quotas: QuotasResource) -> None:
        self._quotas = quotas

        self.retrieve = to_streamed_response_wrapper(
            quotas.retrieve,
        )


class AsyncQuotasResourceWithStreamingResponse:
    def __init__(self, quotas: AsyncQuotasResource) -> None:
        self._quotas = quotas

        self.retrieve = async_to_streamed_response_wrapper(
            quotas.retrieve,
        )
