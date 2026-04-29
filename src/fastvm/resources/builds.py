# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import build_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.build_response import BuildResponse

__all__ = ["BuildsResource", "AsyncBuildsResource"]


class BuildsResource(SyncAPIResource):
    """Build snapshots from a Docker image ref or Dockerfile"""

    @cached_property
    def with_raw_response(self) -> BuildsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BuildsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BuildsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return BuildsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        context_download_url: str | Omit = omit,
        disk_gi_b: int | Omit = omit,
        dockerfile_content: str | Omit = omit,
        image_ref: str | Omit = omit,
        machine_type: str | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BuildResponse:
        """Submits an asynchronous build.

        The scheduler creates a build VM, runs
        `buildah pull` (image-only path) or `buildah bud` (Dockerfile path) inside it,
        snapshots the result, and tears the VM down.

        At least one of `imageRef` or `dockerfileContent` must be provided. If
        `dockerfileContent` is set, the worker writes it verbatim into
        `/tmp/buildctx/Dockerfile` — buildah handles multi-stage, `SHELL`,
        `RUN --mount`, etc. natively.

        For `COPY` instructions that need files, upload the build context first via
        `POST /v1/build-contexts/presign` and pass the returned download URL as
        `contextDownloadUrl`.

        Response is `202 Accepted` with a build ID; poll `GET /v1/builds/{id}` until
        `status` is `completed` or `failed`.

        Args:
          context_download_url: Presigned GET URL for a `tar.gz` of the build context. The worker downloads and
              extracts this into `/tmp/buildctx` before invoking buildah, so `COPY`
              instructions resolve against the user's files. Obtain via
              `POST /v1/build-contexts/presign`.

          disk_gi_b: Disk size for the build VM. Defaults to 10 GiB if omitted.

          dockerfile_content: Raw Dockerfile content to feed to `buildah bud` inside the build VM.
              Multi-stage, `SHELL`, `RUN --mount`, and every standard Dockerfile feature is
              supported (handled natively by buildah). Container-runtime metadata (`CMD`,
              `ENTRYPOINT`, `EXPOSE`, `LABEL`, `HEALTHCHECK`) is consumed by buildah but does
              not surface on the resulting FastVM snapshot — when the snapshot boots, systemd
              takes over, not the container's CMD.

          image_ref: Docker image reference (e.g. `python:3.13-slim`, `ghcr.io/user/repo:tag`). Used
              directly on the no-Dockerfile path, and as a fallback `FROM` source otherwise.

          machine_type: Machine size identifier (e.g. `c1m2`, `c2m4`). Controls CPU and memory
              allocation. Must be supplied on launch unless restoring from a snapshot.

          name: Optional human-readable name for the resulting snapshot. If omitted, the build
              ID is used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/builds",
            body=maybe_transform(
                {
                    "context_download_url": context_download_url,
                    "disk_gi_b": disk_gi_b,
                    "dockerfile_content": dockerfile_content,
                    "image_ref": image_ref,
                    "machine_type": machine_type,
                    "name": name,
                },
                build_create_params.BuildCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildResponse,
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
    ) -> BuildResponse:
        """Returns the current state of a build.

        While the build is in progress, `status`
        is `pending` or `running` and `progress` contains a human-readable string
        describing the current phase (e.g. `Pulling image`, `Building (3 steps)`,
        `Settling VM`).

        On success, `status` is `completed` and `snapshotId` references a `ready`
        snapshot — fetch it via `GET /v1/snapshots/{id}`. On failure, `status` is
        `failed` and `error` carries the worker's diagnostic.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/builds/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildResponse,
        )


class AsyncBuildsResource(AsyncAPIResource):
    """Build snapshots from a Docker image ref or Dockerfile"""

    @cached_property
    def with_raw_response(self) -> AsyncBuildsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBuildsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBuildsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/fastvm-org/fastvm-sdk-python#with_streaming_response
        """
        return AsyncBuildsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        context_download_url: str | Omit = omit,
        disk_gi_b: int | Omit = omit,
        dockerfile_content: str | Omit = omit,
        image_ref: str | Omit = omit,
        machine_type: str | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BuildResponse:
        """Submits an asynchronous build.

        The scheduler creates a build VM, runs
        `buildah pull` (image-only path) or `buildah bud` (Dockerfile path) inside it,
        snapshots the result, and tears the VM down.

        At least one of `imageRef` or `dockerfileContent` must be provided. If
        `dockerfileContent` is set, the worker writes it verbatim into
        `/tmp/buildctx/Dockerfile` — buildah handles multi-stage, `SHELL`,
        `RUN --mount`, etc. natively.

        For `COPY` instructions that need files, upload the build context first via
        `POST /v1/build-contexts/presign` and pass the returned download URL as
        `contextDownloadUrl`.

        Response is `202 Accepted` with a build ID; poll `GET /v1/builds/{id}` until
        `status` is `completed` or `failed`.

        Args:
          context_download_url: Presigned GET URL for a `tar.gz` of the build context. The worker downloads and
              extracts this into `/tmp/buildctx` before invoking buildah, so `COPY`
              instructions resolve against the user's files. Obtain via
              `POST /v1/build-contexts/presign`.

          disk_gi_b: Disk size for the build VM. Defaults to 10 GiB if omitted.

          dockerfile_content: Raw Dockerfile content to feed to `buildah bud` inside the build VM.
              Multi-stage, `SHELL`, `RUN --mount`, and every standard Dockerfile feature is
              supported (handled natively by buildah). Container-runtime metadata (`CMD`,
              `ENTRYPOINT`, `EXPOSE`, `LABEL`, `HEALTHCHECK`) is consumed by buildah but does
              not surface on the resulting FastVM snapshot — when the snapshot boots, systemd
              takes over, not the container's CMD.

          image_ref: Docker image reference (e.g. `python:3.13-slim`, `ghcr.io/user/repo:tag`). Used
              directly on the no-Dockerfile path, and as a fallback `FROM` source otherwise.

          machine_type: Machine size identifier (e.g. `c1m2`, `c2m4`). Controls CPU and memory
              allocation. Must be supplied on launch unless restoring from a snapshot.

          name: Optional human-readable name for the resulting snapshot. If omitted, the build
              ID is used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/builds",
            body=await async_maybe_transform(
                {
                    "context_download_url": context_download_url,
                    "disk_gi_b": disk_gi_b,
                    "dockerfile_content": dockerfile_content,
                    "image_ref": image_ref,
                    "machine_type": machine_type,
                    "name": name,
                },
                build_create_params.BuildCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildResponse,
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
    ) -> BuildResponse:
        """Returns the current state of a build.

        While the build is in progress, `status`
        is `pending` or `running` and `progress` contains a human-readable string
        describing the current phase (e.g. `Pulling image`, `Building (3 steps)`,
        `Settling VM`).

        On success, `status` is `completed` and `snapshotId` references a `ready`
        snapshot — fetch it via `GET /v1/snapshots/{id}`. On failure, `status` is
        `failed` and `error` carries the worker's diagnostic.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/builds/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildResponse,
        )


class BuildsResourceWithRawResponse:
    def __init__(self, builds: BuildsResource) -> None:
        self._builds = builds

        self.create = to_raw_response_wrapper(
            builds.create,
        )
        self.retrieve = to_raw_response_wrapper(
            builds.retrieve,
        )


class AsyncBuildsResourceWithRawResponse:
    def __init__(self, builds: AsyncBuildsResource) -> None:
        self._builds = builds

        self.create = async_to_raw_response_wrapper(
            builds.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            builds.retrieve,
        )


class BuildsResourceWithStreamingResponse:
    def __init__(self, builds: BuildsResource) -> None:
        self._builds = builds

        self.create = to_streamed_response_wrapper(
            builds.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            builds.retrieve,
        )


class AsyncBuildsResourceWithStreamingResponse:
    def __init__(self, builds: AsyncBuildsResource) -> None:
        self._builds = builds

        self.create = async_to_streamed_response_wrapper(
            builds.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            builds.retrieve,
        )
