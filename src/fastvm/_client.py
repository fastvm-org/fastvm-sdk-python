# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
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
from ._models import SecurityOptions
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import org, vms, livez, readyz, healthz, snapshots
    from .resources.org import OrgResource, AsyncOrgResource
    from .resources.livez import LivezResource, AsyncLivezResource
    from .resources.readyz import ReadyzResource, AsyncReadyzResource
    from .resources.healthz import HealthzResource, AsyncHealthzResource
    from .resources.vms.vms import VmsResource, AsyncVmsResource
    from .resources.snapshots import SnapshotsResource, AsyncSnapshotsResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Fastvm", "AsyncFastvm", "Client", "AsyncClient"]


class Fastvm(SyncAPIClient):
    # client options
    api_key: str | None
    bearer_token: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
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

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `FASTVM_API_KEY`
        - `bearer_token` from `FASTVM_BEARER_TOKEN`
        """
        if api_key is None:
            api_key = os.environ.get("FASTVM_API_KEY")
        self.api_key = api_key

        if bearer_token is None:
            bearer_token = os.environ.get("FASTVM_BEARER_TOKEN")
        self.bearer_token = bearer_token

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
    def healthz(self) -> HealthzResource:
        from .resources.healthz import HealthzResource

        return HealthzResource(self)

    @cached_property
    def livez(self) -> LivezResource:
        from .resources.livez import LivezResource

        return LivezResource(self)

    @cached_property
    def readyz(self) -> ReadyzResource:
        from .resources.readyz import ReadyzResource

        return ReadyzResource(self)

    @cached_property
    def vms(self) -> VmsResource:
        from .resources.vms import VmsResource

        return VmsResource(self)

    @cached_property
    def snapshots(self) -> SnapshotsResource:
        from .resources.snapshots import SnapshotsResource

        return SnapshotsResource(self)

    @cached_property
    def org(self) -> OrgResource:
        from .resources.org import OrgResource

        return OrgResource(self)

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

    @override
    def _auth_headers(self, security: SecurityOptions) -> dict[str, str]:
        return {
            **(self._api_key_auth if security.get("api_key_auth", False) else {}),
            **(self._bearer_auth if security.get("bearer_auth", False) else {}),
        }

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-API-Key": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if headers.get("X-API-Key") or isinstance(custom_headers.get("X-API-Key"), Omit):
            return

        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or bearer_token to be set. Or for one of the `X-API-Key` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
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
            bearer_token=bearer_token or self.bearer_token,
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
    api_key: str | None
    bearer_token: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
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

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `FASTVM_API_KEY`
        - `bearer_token` from `FASTVM_BEARER_TOKEN`
        """
        if api_key is None:
            api_key = os.environ.get("FASTVM_API_KEY")
        self.api_key = api_key

        if bearer_token is None:
            bearer_token = os.environ.get("FASTVM_BEARER_TOKEN")
        self.bearer_token = bearer_token

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
    def healthz(self) -> AsyncHealthzResource:
        from .resources.healthz import AsyncHealthzResource

        return AsyncHealthzResource(self)

    @cached_property
    def livez(self) -> AsyncLivezResource:
        from .resources.livez import AsyncLivezResource

        return AsyncLivezResource(self)

    @cached_property
    def readyz(self) -> AsyncReadyzResource:
        from .resources.readyz import AsyncReadyzResource

        return AsyncReadyzResource(self)

    @cached_property
    def vms(self) -> AsyncVmsResource:
        from .resources.vms import AsyncVmsResource

        return AsyncVmsResource(self)

    @cached_property
    def snapshots(self) -> AsyncSnapshotsResource:
        from .resources.snapshots import AsyncSnapshotsResource

        return AsyncSnapshotsResource(self)

    @cached_property
    def org(self) -> AsyncOrgResource:
        from .resources.org import AsyncOrgResource

        return AsyncOrgResource(self)

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

    @override
    def _auth_headers(self, security: SecurityOptions) -> dict[str, str]:
        return {
            **(self._api_key_auth if security.get("api_key_auth", False) else {}),
            **(self._bearer_auth if security.get("bearer_auth", False) else {}),
        }

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-API-Key": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if headers.get("X-API-Key") or isinstance(custom_headers.get("X-API-Key"), Omit):
            return

        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or bearer_token to be set. Or for one of the `X-API-Key` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
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
            bearer_token=bearer_token or self.bearer_token,
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

    @cached_property
    def healthz(self) -> healthz.HealthzResourceWithRawResponse:
        from .resources.healthz import HealthzResourceWithRawResponse

        return HealthzResourceWithRawResponse(self._client.healthz)

    @cached_property
    def livez(self) -> livez.LivezResourceWithRawResponse:
        from .resources.livez import LivezResourceWithRawResponse

        return LivezResourceWithRawResponse(self._client.livez)

    @cached_property
    def readyz(self) -> readyz.ReadyzResourceWithRawResponse:
        from .resources.readyz import ReadyzResourceWithRawResponse

        return ReadyzResourceWithRawResponse(self._client.readyz)

    @cached_property
    def vms(self) -> vms.VmsResourceWithRawResponse:
        from .resources.vms import VmsResourceWithRawResponse

        return VmsResourceWithRawResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.SnapshotsResourceWithRawResponse:
        from .resources.snapshots import SnapshotsResourceWithRawResponse

        return SnapshotsResourceWithRawResponse(self._client.snapshots)

    @cached_property
    def org(self) -> org.OrgResourceWithRawResponse:
        from .resources.org import OrgResourceWithRawResponse

        return OrgResourceWithRawResponse(self._client.org)


class AsyncFastvmWithRawResponse:
    _client: AsyncFastvm

    def __init__(self, client: AsyncFastvm) -> None:
        self._client = client

    @cached_property
    def healthz(self) -> healthz.AsyncHealthzResourceWithRawResponse:
        from .resources.healthz import AsyncHealthzResourceWithRawResponse

        return AsyncHealthzResourceWithRawResponse(self._client.healthz)

    @cached_property
    def livez(self) -> livez.AsyncLivezResourceWithRawResponse:
        from .resources.livez import AsyncLivezResourceWithRawResponse

        return AsyncLivezResourceWithRawResponse(self._client.livez)

    @cached_property
    def readyz(self) -> readyz.AsyncReadyzResourceWithRawResponse:
        from .resources.readyz import AsyncReadyzResourceWithRawResponse

        return AsyncReadyzResourceWithRawResponse(self._client.readyz)

    @cached_property
    def vms(self) -> vms.AsyncVmsResourceWithRawResponse:
        from .resources.vms import AsyncVmsResourceWithRawResponse

        return AsyncVmsResourceWithRawResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.AsyncSnapshotsResourceWithRawResponse:
        from .resources.snapshots import AsyncSnapshotsResourceWithRawResponse

        return AsyncSnapshotsResourceWithRawResponse(self._client.snapshots)

    @cached_property
    def org(self) -> org.AsyncOrgResourceWithRawResponse:
        from .resources.org import AsyncOrgResourceWithRawResponse

        return AsyncOrgResourceWithRawResponse(self._client.org)


class FastvmWithStreamedResponse:
    _client: Fastvm

    def __init__(self, client: Fastvm) -> None:
        self._client = client

    @cached_property
    def healthz(self) -> healthz.HealthzResourceWithStreamingResponse:
        from .resources.healthz import HealthzResourceWithStreamingResponse

        return HealthzResourceWithStreamingResponse(self._client.healthz)

    @cached_property
    def livez(self) -> livez.LivezResourceWithStreamingResponse:
        from .resources.livez import LivezResourceWithStreamingResponse

        return LivezResourceWithStreamingResponse(self._client.livez)

    @cached_property
    def readyz(self) -> readyz.ReadyzResourceWithStreamingResponse:
        from .resources.readyz import ReadyzResourceWithStreamingResponse

        return ReadyzResourceWithStreamingResponse(self._client.readyz)

    @cached_property
    def vms(self) -> vms.VmsResourceWithStreamingResponse:
        from .resources.vms import VmsResourceWithStreamingResponse

        return VmsResourceWithStreamingResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.SnapshotsResourceWithStreamingResponse:
        from .resources.snapshots import SnapshotsResourceWithStreamingResponse

        return SnapshotsResourceWithStreamingResponse(self._client.snapshots)

    @cached_property
    def org(self) -> org.OrgResourceWithStreamingResponse:
        from .resources.org import OrgResourceWithStreamingResponse

        return OrgResourceWithStreamingResponse(self._client.org)


class AsyncFastvmWithStreamedResponse:
    _client: AsyncFastvm

    def __init__(self, client: AsyncFastvm) -> None:
        self._client = client

    @cached_property
    def healthz(self) -> healthz.AsyncHealthzResourceWithStreamingResponse:
        from .resources.healthz import AsyncHealthzResourceWithStreamingResponse

        return AsyncHealthzResourceWithStreamingResponse(self._client.healthz)

    @cached_property
    def livez(self) -> livez.AsyncLivezResourceWithStreamingResponse:
        from .resources.livez import AsyncLivezResourceWithStreamingResponse

        return AsyncLivezResourceWithStreamingResponse(self._client.livez)

    @cached_property
    def readyz(self) -> readyz.AsyncReadyzResourceWithStreamingResponse:
        from .resources.readyz import AsyncReadyzResourceWithStreamingResponse

        return AsyncReadyzResourceWithStreamingResponse(self._client.readyz)

    @cached_property
    def vms(self) -> vms.AsyncVmsResourceWithStreamingResponse:
        from .resources.vms import AsyncVmsResourceWithStreamingResponse

        return AsyncVmsResourceWithStreamingResponse(self._client.vms)

    @cached_property
    def snapshots(self) -> snapshots.AsyncSnapshotsResourceWithStreamingResponse:
        from .resources.snapshots import AsyncSnapshotsResourceWithStreamingResponse

        return AsyncSnapshotsResourceWithStreamingResponse(self._client.snapshots)

    @cached_property
    def org(self) -> org.AsyncOrgResourceWithStreamingResponse:
        from .resources.org import AsyncOrgResourceWithStreamingResponse

        return AsyncOrgResourceWithStreamingResponse(self._client.org)


Client = Fastvm

AsyncClient = AsyncFastvm
