# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import FastvmError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .types.health_response import HealthResponse

if TYPE_CHECKING:
    from .resources import vms, quotas, snapshots
    from .resources.quotas import QuotasResource, AsyncQuotasResource
    from .resources.vms.vms import VmsResource, AsyncVmsResource
    from .resources.snapshots import SnapshotsResource, AsyncSnapshotsResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Fastvm", "AsyncFastvm", "Client", "AsyncClient"]


class Fastvm(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Fastvm client instance.

        This automatically infers the `api_key` argument from the `FASTVM_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("FASTVM_API_KEY")
        if api_key is None:
            raise FastvmError(
                "The api_key client option must be set either by passing api_key to the client or by setting the FASTVM_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("FASTVM_BASE_URL")
        if base_url is None:
            base_url = f"https://api.fastvm.org"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def vms(self) -> VmsResource:
        from .resources.vms import VmsResource

        return VmsResource(self)

    @cached_property
    def snapshots(self) -> SnapshotsResource:
        """Snapshot lifecycle"""
        from .resources.snapshots import SnapshotsResource

        return SnapshotsResource(self)

    @cached_property
    def quotas(self) -> QuotasResource:
        """Org quotas and usage"""
        from .resources.quotas import QuotasResource

        return QuotasResource(self)

    @cached_property
    def with_raw_response(self) -> FastvmWithRawResponse:
        return FastvmWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FastvmWithStreamedResponse:
        return FastvmWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"X-API-Key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HealthResponse:
        """Returns 200 when the API is reachable.

        SDK clients call this on startup to warm
        HTTP/2 connections before the first real request.
        """
        return self.get(
            "/healthz",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HealthResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncFastvm(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncFastvm client instance.

        This automatically infers the `api_key` argument from the `FASTVM_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("FASTVM_API_KEY")
        if api_key is None:
            raise FastvmError(
                "The api_key client option must be set either by passing api_key to the client or by setting the FASTVM_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("FASTVM_BASE_URL")
        if base_url is None:
            base_url = f"https://api.fastvm.org"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def vms(self) -> AsyncVmsResource:
        from .resources.vms import AsyncVmsResource

        return AsyncVmsResource(self)

    @cached_property
    def snapshots(self) -> AsyncSnapshotsResource:
        """Snapshot lifecycle"""
        from .resources.snapshots import AsyncSnapshotsResource

        return AsyncSnapshotsResource(self)

    @cached_property
    def quotas(self) -> AsyncQuotasResource:
        """Org quotas and usage"""
        from .resources.quotas import AsyncQuotasResource

        return AsyncQuotasResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncFastvmWithRawResponse:
        return AsyncFastvmWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFastvmWithStreamedResponse:
        return AsyncFastvmWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"X-API-Key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HealthResponse:
        """Returns 200 when the API is reachable.

        SDK clients call this on startup to warm
        HTTP/2 connections before the first real request.
        """
        return await self.get(
            "/healthz",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HealthResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class FastvmWithRawResponse:
    _client: Fastvm

    def __init__(self, client: Fastvm) -> None:
        self._client = client

        self.health = to_raw_response_wrapper(
            client.health,
        )

    @cached_property
    def vms(self) -> vms.VmsResourceWithRawResponse:
        from .resources.vms import VmsResourceWithRawResponse

        return VmsResourceWithRawResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.SnapshotsResourceWithRawResponse:
        """Snapshot lifecycle"""
        from .resources.snapshots import SnapshotsResourceWithRawResponse

        return SnapshotsResourceWithRawResponse(self._client.snapshots)

    @cached_property
    def quotas(self) -> quotas.QuotasResourceWithRawResponse:
        """Org quotas and usage"""
        from .resources.quotas import QuotasResourceWithRawResponse

        return QuotasResourceWithRawResponse(self._client.quotas)


class AsyncFastvmWithRawResponse:
    _client: AsyncFastvm

    def __init__(self, client: AsyncFastvm) -> None:
        self._client = client

        self.health = async_to_raw_response_wrapper(
            client.health,
        )

    @cached_property
    def vms(self) -> vms.AsyncVmsResourceWithRawResponse:
        from .resources.vms import AsyncVmsResourceWithRawResponse

        return AsyncVmsResourceWithRawResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.AsyncSnapshotsResourceWithRawResponse:
        """Snapshot lifecycle"""
        from .resources.snapshots import AsyncSnapshotsResourceWithRawResponse

        return AsyncSnapshotsResourceWithRawResponse(self._client.snapshots)

    @cached_property
    def quotas(self) -> quotas.AsyncQuotasResourceWithRawResponse:
        """Org quotas and usage"""
        from .resources.quotas import AsyncQuotasResourceWithRawResponse

        return AsyncQuotasResourceWithRawResponse(self._client.quotas)


class FastvmWithStreamedResponse:
    _client: Fastvm

    def __init__(self, client: Fastvm) -> None:
        self._client = client

        self.health = to_streamed_response_wrapper(
            client.health,
        )

    @cached_property
    def vms(self) -> vms.VmsResourceWithStreamingResponse:
        from .resources.vms import VmsResourceWithStreamingResponse

        return VmsResourceWithStreamingResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.SnapshotsResourceWithStreamingResponse:
        """Snapshot lifecycle"""
        from .resources.snapshots import SnapshotsResourceWithStreamingResponse

        return SnapshotsResourceWithStreamingResponse(self._client.snapshots)

    @cached_property
    def quotas(self) -> quotas.QuotasResourceWithStreamingResponse:
        """Org quotas and usage"""
        from .resources.quotas import QuotasResourceWithStreamingResponse

        return QuotasResourceWithStreamingResponse(self._client.quotas)


class AsyncFastvmWithStreamedResponse:
    _client: AsyncFastvm

    def __init__(self, client: AsyncFastvm) -> None:
        self._client = client

        self.health = async_to_streamed_response_wrapper(
            client.health,
        )

    @cached_property
    def vms(self) -> vms.AsyncVmsResourceWithStreamingResponse:
        from .resources.vms import AsyncVmsResourceWithStreamingResponse

        return AsyncVmsResourceWithStreamingResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.AsyncSnapshotsResourceWithStreamingResponse:
        """Snapshot lifecycle"""
        from .resources.snapshots import AsyncSnapshotsResourceWithStreamingResponse

        return AsyncSnapshotsResourceWithStreamingResponse(self._client.snapshots)

    @cached_property
    def quotas(self) -> quotas.AsyncQuotasResourceWithStreamingResponse:
        """Org quotas and usage"""
        from .resources.quotas import AsyncQuotasResourceWithStreamingResponse

        return AsyncQuotasResourceWithStreamingResponse(self._client.quotas)


Client = Fastvm

AsyncClient = AsyncFastvm
