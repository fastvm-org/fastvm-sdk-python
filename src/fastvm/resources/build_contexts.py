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
from ..types.shared.file_presign_response import FilePresignResponse

__all__ = ["BuildContextsResource", "AsyncBuildContextsResource"]


class BuildContextsResource(SyncAPIResource):
    """Build snapshots from a Docker image ref or Dockerfile"""

    @cached_property
    def with_raw_response(self) -> BuildContextsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BuildContextsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BuildContextsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return BuildContextsResourceWithStreamingResponse(self)

    def presign(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FilePresignResponse:
        """
        Returns a pair of short-lived signed URLs targeting a per-org staging location.
        Tar+gzip your build-context directory, PUT it to `uploadUrl` with
        `Content-Type: application/gzip`, then pass `downloadUrl` as
        `contextDownloadUrl` on `POST /v1/builds`.

        Unlike `/v1/vms/{id}/files/presign`, this endpoint isn't keyed to a specific VM
        — context uploads happen _before_ the build VM exists.
        """
        return self._post(
            "/v1/build-contexts/presign",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FilePresignResponse,
        )


class AsyncBuildContextsResource(AsyncAPIResource):
    """Build snapshots from a Docker image ref or Dockerfile"""

    @cached_property
    def with_raw_response(self) -> AsyncBuildContextsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBuildContextsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBuildContextsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return AsyncBuildContextsResourceWithStreamingResponse(self)

    async def presign(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FilePresignResponse:
        """
        Returns a pair of short-lived signed URLs targeting a per-org staging location.
        Tar+gzip your build-context directory, PUT it to `uploadUrl` with
        `Content-Type: application/gzip`, then pass `downloadUrl` as
        `contextDownloadUrl` on `POST /v1/builds`.

        Unlike `/v1/vms/{id}/files/presign`, this endpoint isn't keyed to a specific VM
        — context uploads happen _before_ the build VM exists.
        """
        return await self._post(
            "/v1/build-contexts/presign",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FilePresignResponse,
        )


class BuildContextsResourceWithRawResponse:
    def __init__(self, build_contexts: BuildContextsResource) -> None:
        self._build_contexts = build_contexts

        self.presign = to_raw_response_wrapper(
            build_contexts.presign,
        )


class AsyncBuildContextsResourceWithRawResponse:
    def __init__(self, build_contexts: AsyncBuildContextsResource) -> None:
        self._build_contexts = build_contexts

        self.presign = async_to_raw_response_wrapper(
            build_contexts.presign,
        )


class BuildContextsResourceWithStreamingResponse:
    def __init__(self, build_contexts: BuildContextsResource) -> None:
        self._build_contexts = build_contexts

        self.presign = to_streamed_response_wrapper(
            build_contexts.presign,
        )


class AsyncBuildContextsResourceWithStreamingResponse:
    def __init__(self, build_contexts: AsyncBuildContextsResource) -> None:
        self._build_contexts = build_contexts

        self.presign = async_to_streamed_response_wrapper(
            build_contexts.presign,
        )
