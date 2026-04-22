# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NoneType, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["LivezResource", "AsyncLivezResource"]


class LivezResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LivezResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#accessing-raw-response-data-eg-headers
        """
        return LivezResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LivezResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#with_streaming_response
        """
        return LivezResourceWithStreamingResponse(self)

    def check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Liveness check"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/livez",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                security={},
            ),
            cast_to=NoneType,
        )


class AsyncLivezResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLivezResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLivezResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLivezResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/fastvm-python#with_streaming_response
        """
        return AsyncLivezResourceWithStreamingResponse(self)

    async def check(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Liveness check"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/livez",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                security={},
            ),
            cast_to=NoneType,
        )


class LivezResourceWithRawResponse:
    def __init__(self, livez: LivezResource) -> None:
        self._livez = livez

        self.check = to_raw_response_wrapper(
            livez.check,
        )


class AsyncLivezResourceWithRawResponse:
    def __init__(self, livez: AsyncLivezResource) -> None:
        self._livez = livez

        self.check = async_to_raw_response_wrapper(
            livez.check,
        )


class LivezResourceWithStreamingResponse:
    def __init__(self, livez: LivezResource) -> None:
        self._livez = livez

        self.check = to_streamed_response_wrapper(
            livez.check,
        )


class AsyncLivezResourceWithStreamingResponse:
    def __init__(self, livez: AsyncLivezResource) -> None:
        self._livez = livez

        self.check = async_to_streamed_response_wrapper(
            livez.check,
        )
