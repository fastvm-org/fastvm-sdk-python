# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NoneType, NotGiven, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.vms import console_websocket_params
from ..._base_client import make_request_options

__all__ = ["ConsoleResource", "AsyncConsoleResource"]


class ConsoleResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConsoleResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ConsoleResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsoleResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return ConsoleResourceWithStreamingResponse(self)

    def websocket(
        self,
        id: str,
        *,
        session: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Upgrade this request to WebSocket and provide `session` query param from
        `/v1/vms/{id}/console-token`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            path_template("/v1/vms/{id}/console/ws", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"session": session}, console_websocket_params.ConsoleWebsocketParams),
                security={},
            ),
            cast_to=NoneType,
        )


class AsyncConsoleResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConsoleResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsoleResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsoleResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return AsyncConsoleResourceWithStreamingResponse(self)

    async def websocket(
        self,
        id: str,
        *,
        session: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Upgrade this request to WebSocket and provide `session` query param from
        `/v1/vms/{id}/console-token`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/vms/{id}/console/ws", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"session": session}, console_websocket_params.ConsoleWebsocketParams
                ),
                security={},
            ),
            cast_to=NoneType,
        )


class ConsoleResourceWithRawResponse:
    def __init__(self, console: ConsoleResource) -> None:
        self._console = console

        self.websocket = to_raw_response_wrapper(
            console.websocket,
        )


class AsyncConsoleResourceWithRawResponse:
    def __init__(self, console: AsyncConsoleResource) -> None:
        self._console = console

        self.websocket = async_to_raw_response_wrapper(
            console.websocket,
        )


class ConsoleResourceWithStreamingResponse:
    def __init__(self, console: ConsoleResource) -> None:
        self._console = console

        self.websocket = to_streamed_response_wrapper(
            console.websocket,
        )


class AsyncConsoleResourceWithStreamingResponse:
    def __init__(self, console: AsyncConsoleResource) -> None:
        self._console = console

        self.websocket = async_to_streamed_response_wrapper(
            console.websocket,
        )
