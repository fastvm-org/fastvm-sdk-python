# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ...types.vms import file_fetch_params, file_presign_params
from ..._base_client import make_request_options
from ...types.exec_result import ExecResult
from ...types.vms.presign_response import PresignResponse

__all__ = ["FilesResource", "AsyncFilesResource"]


class FilesResource(SyncAPIResource):
    """File upload/download to/from a running VM"""

    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return FilesResourceWithStreamingResponse(self)

    def fetch(
        self,
        id: str,
        *,
        path: str,
        url: str,
        timeout_sec: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExecResult:
        """Scheduler asks the VM worker to download `url` into the guest at `path`.

        `url`
        must be a presigned storage URL previously minted by
        `POST /v1/vms/{id}/files/presign` (URLs from other sources are rejected).

        Response mirrors `/v1/vms/{id}/exec` — the worker runs the fetch via the guest
        agent and reports stdout/stderr/exit code of the underlying download+unpack
        operation.

        Not idempotent; not retried by default.

        Args:
          path: Absolute destination path inside the guest filesystem.

          url: Must be the `downloadUrl` previously returned by
              `POST /v1/vms/{id}/files/presign` (URLs from other sources are rejected).

          timeout_sec: Per-fetch timeout in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/vms/{id}/files/fetch", id=id),
            body=maybe_transform(
                {
                    "path": path,
                    "url": url,
                    "timeout_sec": timeout_sec,
                },
                file_fetch_params.FileFetchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecResult,
        )

    def presign(
        self,
        id: str,
        *,
        path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PresignResponse:
        """
        Returns a pair of short-lived signed URLs targeting a per-VM staging location.
        Upload to `uploadUrl` with PUT (`Content-Type: application/octet-stream`), then
        pass `downloadUrl` to `POST /v1/vms/{id}/files/fetch` to have the worker pull it
        into the guest filesystem.

        Args:
          path: Absolute destination path inside the guest filesystem (where the file will land
              after `fetchFileToVm`). Used only to scope the staging object key; any value
              server-side is accepted here.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/vms/{id}/files/presign", id=id),
            body=maybe_transform({"path": path}, file_presign_params.FilePresignParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PresignResponse,
        )


class AsyncFilesResource(AsyncAPIResource):
    """File upload/download to/from a running VM"""

    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return AsyncFilesResourceWithStreamingResponse(self)

    async def fetch(
        self,
        id: str,
        *,
        path: str,
        url: str,
        timeout_sec: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExecResult:
        """Scheduler asks the VM worker to download `url` into the guest at `path`.

        `url`
        must be a presigned storage URL previously minted by
        `POST /v1/vms/{id}/files/presign` (URLs from other sources are rejected).

        Response mirrors `/v1/vms/{id}/exec` — the worker runs the fetch via the guest
        agent and reports stdout/stderr/exit code of the underlying download+unpack
        operation.

        Not idempotent; not retried by default.

        Args:
          path: Absolute destination path inside the guest filesystem.

          url: Must be the `downloadUrl` previously returned by
              `POST /v1/vms/{id}/files/presign` (URLs from other sources are rejected).

          timeout_sec: Per-fetch timeout in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/vms/{id}/files/fetch", id=id),
            body=await async_maybe_transform(
                {
                    "path": path,
                    "url": url,
                    "timeout_sec": timeout_sec,
                },
                file_fetch_params.FileFetchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecResult,
        )

    async def presign(
        self,
        id: str,
        *,
        path: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PresignResponse:
        """
        Returns a pair of short-lived signed URLs targeting a per-VM staging location.
        Upload to `uploadUrl` with PUT (`Content-Type: application/octet-stream`), then
        pass `downloadUrl` to `POST /v1/vms/{id}/files/fetch` to have the worker pull it
        into the guest filesystem.

        Args:
          path: Absolute destination path inside the guest filesystem (where the file will land
              after `fetchFileToVm`). Used only to scope the staging object key; any value
              server-side is accepted here.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/vms/{id}/files/presign", id=id),
            body=await async_maybe_transform({"path": path}, file_presign_params.FilePresignParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PresignResponse,
        )


class FilesResourceWithRawResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.fetch = to_raw_response_wrapper(
            files.fetch,
        )
        self.presign = to_raw_response_wrapper(
            files.presign,
        )


class AsyncFilesResourceWithRawResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.fetch = async_to_raw_response_wrapper(
            files.fetch,
        )
        self.presign = async_to_raw_response_wrapper(
            files.presign,
        )


class FilesResourceWithStreamingResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.fetch = to_streamed_response_wrapper(
            files.fetch,
        )
        self.presign = to_streamed_response_wrapper(
            files.presign,
        )


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.fetch = async_to_streamed_response_wrapper(
            files.fetch,
        )
        self.presign = async_to_streamed_response_wrapper(
            files.presign,
        )
