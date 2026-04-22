# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from .files import (
    FilesResource,
    AsyncFilesResource,
    FilesResourceWithRawResponse,
    AsyncFilesResourceWithRawResponse,
    FilesResourceWithStreamingResponse,
    AsyncFilesResourceWithStreamingResponse,
)
from ...types import (
    vm_run_params,
    vm_launch_params,
    vm_update_params,
    vm_set_firewall_params,
    vm_patch_firewall_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ...types.vm import Vm
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.exec_result import ExecResult
from ...types.console_token import ConsoleToken
from ...types.vm_list_response import VmListResponse
from ...types.vm_delete_response import VmDeleteResponse
from ...types.shared_params.firewall_rule import FirewallRule
from ...types.shared_params.firewall_policy import FirewallPolicy

__all__ = ["VmsResource", "AsyncVmsResource"]


class VmsResource(SyncAPIResource):
    @cached_property
    def files(self) -> FilesResource:
        """File upload/download to/from a running VM"""
        return FilesResource(self._client)

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
    ) -> Vm:
        """
        Get a VM

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
            cast_to=Vm,
        )

    def update(
        self,
        id: str,
        *,
        metadata: Dict[str, str] | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """Renames a VM and/or replaces its metadata map.

        At least one of `name` or
        `metadata` must be provided. Sending `metadata: {}` clears all metadata;
        omitting `metadata` leaves it unchanged.

        Args:
          metadata: Free-form string→string map. Server-enforced limits: up to 256 keys, key length
              1–256 bytes, value length ≤4096 bytes, total JSON encoding ≤65536 bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/v1/vms/{id}", id=id),
            body=maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                vm_update_params.VmUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
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
        """Lists all non-deleted VMs for the authenticated org.

        Supports metadata-equality
        filtering; callers pass repeated query parameters of the form
        `metadata.<key>=<value>` (e.g. `metadata.env=prod&metadata.role=api`).
        """
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
    ) -> VmDeleteResponse:
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
            cast_to=VmDeleteResponse,
        )

    def console_token(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConsoleToken:
        """Returns a short-lived token and WebSocket path.

        Open a WebSocket to
        `wss://<host><websocketPath>?session=<token>` to attach to the VM's serial
        console. The WebSocket endpoint itself is intentionally not modeled in this spec
        — it uses a capability-URL flow (no API key on upgrade) and a custom binary/text
        protocol. See `src/fastvm/lib/console.py` in the Python SDK for a reference
        client.

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
            cast_to=ConsoleToken,
        )

    def launch(
        self,
        *,
        disk_gi_b: int | Omit = omit,
        firewall: FirewallPolicy | Omit = omit,
        machine_type: str | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: str | Omit = omit,
        snapshot_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """
        Creates a new VM, either from a machineType (fresh boot) or a snapshotId
        (restore from snapshot).

        - Returns **201** when the VM is already running in the response.
        - Returns **202** when the VM is queued; clients must poll `GET /v1/vms/{id}`
          until status transitions to `running`. Terminal failure statuses are `error`
          and `stopped`.

        The SDK's `launch()` helper handles the 201/202 branching and polling
        automatically.

        Args:
          disk_gi_b: Override the default disk size (GiB).

          machine_type: Machine size identifier (e.g. `c1m2`, `c2m4`). Controls CPU and memory
              allocation. Must be supplied on launch unless restoring from a snapshot.

          metadata: Free-form string→string map. Server-enforced limits: up to 256 keys, key length
              1–256 bytes, value length ≤4096 bytes, total JSON encoding ≤65536 bytes.

          name: User-facing name (trimmed + whitespace-collapsed, max 64 runes after
              normalization — longer values are truncated server-side). Auto-generated as
              `vm-<8-char-id-prefix>` if empty.

          snapshot_id: Snapshot ID to restore from.

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
                    "metadata": metadata,
                    "name": name,
                    "snapshot_id": snapshot_id,
                },
                vm_launch_params.VmLaunchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
        )

    def patch_firewall(
        self,
        id: str,
        *,
        ingress: Iterable[FirewallRule] | Omit = omit,
        mode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """Updates `mode` and/or `ingress` on the firewall policy.

        Passing `ingress: []`
        clears all rules; omitting `ingress` leaves rules unchanged.

        Args:
          mode: Firewall mode. Known values: `open` (allow all inbound traffic), `restricted`
              (deny by default; only rules listed in `ingress` are allowed). Additional values
              may be introduced in future server versions.

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
                vm_patch_firewall_params.VmPatchFirewallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
        )

    def run(
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
    ) -> ExecResult:
        """
        Runs a command via the VM's guest agent and returns stdout, stderr, exit code,
        and timing. `timeoutSec` bounds server-side execution; clients should set their
        own HTTP timeout in addition.

        502 responses are transient (worker unreachable, worker-side timeout, or worker
        5xx — all collapsed into 502 at the scheduler). The SDK's `run()` helper does
        NOT auto-retry these by default: exec is **not idempotent** — if a 502 hides a
        successful exec, a retry may run the command twice. Callers opt in with
        `max_retries=N` per call.

        Args:
          command: Argv-style command. First element must be non-empty. For shell strings, wrap as
              `["sh", "-c", "<string>"]`.

          timeout_sec: Server-side execution timeout in seconds. Must be positive when provided; omit
              to use the server default.

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
                vm_run_params.VmRunParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecResult,
        )

    def set_firewall(
        self,
        id: str,
        *,
        mode: str,
        ingress: Iterable[FirewallRule] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """Replaces the full firewall policy on a VM.

        Args:
          mode: Firewall mode.

        Known values: `open` (allow all inbound traffic), `restricted`
              (deny by default; only rules listed in `ingress` are allowed). Additional values
              may be introduced in future server versions.

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
                vm_set_firewall_params.VmSetFirewallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
        )


class AsyncVmsResource(AsyncAPIResource):
    @cached_property
    def files(self) -> AsyncFilesResource:
        """File upload/download to/from a running VM"""
        return AsyncFilesResource(self._client)

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
    ) -> Vm:
        """
        Get a VM

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
            cast_to=Vm,
        )

    async def update(
        self,
        id: str,
        *,
        metadata: Dict[str, str] | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """Renames a VM and/or replaces its metadata map.

        At least one of `name` or
        `metadata` must be provided. Sending `metadata: {}` clears all metadata;
        omitting `metadata` leaves it unchanged.

        Args:
          metadata: Free-form string→string map. Server-enforced limits: up to 256 keys, key length
              1–256 bytes, value length ≤4096 bytes, total JSON encoding ≤65536 bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/v1/vms/{id}", id=id),
            body=await async_maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                vm_update_params.VmUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
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
        """Lists all non-deleted VMs for the authenticated org.

        Supports metadata-equality
        filtering; callers pass repeated query parameters of the form
        `metadata.<key>=<value>` (e.g. `metadata.env=prod&metadata.role=api`).
        """
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
    ) -> VmDeleteResponse:
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
            cast_to=VmDeleteResponse,
        )

    async def console_token(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConsoleToken:
        """Returns a short-lived token and WebSocket path.

        Open a WebSocket to
        `wss://<host><websocketPath>?session=<token>` to attach to the VM's serial
        console. The WebSocket endpoint itself is intentionally not modeled in this spec
        — it uses a capability-URL flow (no API key on upgrade) and a custom binary/text
        protocol. See `src/fastvm/lib/console.py` in the Python SDK for a reference
        client.

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
            cast_to=ConsoleToken,
        )

    async def launch(
        self,
        *,
        disk_gi_b: int | Omit = omit,
        firewall: FirewallPolicy | Omit = omit,
        machine_type: str | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: str | Omit = omit,
        snapshot_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """
        Creates a new VM, either from a machineType (fresh boot) or a snapshotId
        (restore from snapshot).

        - Returns **201** when the VM is already running in the response.
        - Returns **202** when the VM is queued; clients must poll `GET /v1/vms/{id}`
          until status transitions to `running`. Terminal failure statuses are `error`
          and `stopped`.

        The SDK's `launch()` helper handles the 201/202 branching and polling
        automatically.

        Args:
          disk_gi_b: Override the default disk size (GiB).

          machine_type: Machine size identifier (e.g. `c1m2`, `c2m4`). Controls CPU and memory
              allocation. Must be supplied on launch unless restoring from a snapshot.

          metadata: Free-form string→string map. Server-enforced limits: up to 256 keys, key length
              1–256 bytes, value length ≤4096 bytes, total JSON encoding ≤65536 bytes.

          name: User-facing name (trimmed + whitespace-collapsed, max 64 runes after
              normalization — longer values are truncated server-side). Auto-generated as
              `vm-<8-char-id-prefix>` if empty.

          snapshot_id: Snapshot ID to restore from.

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
                    "metadata": metadata,
                    "name": name,
                    "snapshot_id": snapshot_id,
                },
                vm_launch_params.VmLaunchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
        )

    async def patch_firewall(
        self,
        id: str,
        *,
        ingress: Iterable[FirewallRule] | Omit = omit,
        mode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """Updates `mode` and/or `ingress` on the firewall policy.

        Passing `ingress: []`
        clears all rules; omitting `ingress` leaves rules unchanged.

        Args:
          mode: Firewall mode. Known values: `open` (allow all inbound traffic), `restricted`
              (deny by default; only rules listed in `ingress` are allowed). Additional values
              may be introduced in future server versions.

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
                vm_patch_firewall_params.VmPatchFirewallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
        )

    async def run(
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
    ) -> ExecResult:
        """
        Runs a command via the VM's guest agent and returns stdout, stderr, exit code,
        and timing. `timeoutSec` bounds server-side execution; clients should set their
        own HTTP timeout in addition.

        502 responses are transient (worker unreachable, worker-side timeout, or worker
        5xx — all collapsed into 502 at the scheduler). The SDK's `run()` helper does
        NOT auto-retry these by default: exec is **not idempotent** — if a 502 hides a
        successful exec, a retry may run the command twice. Callers opt in with
        `max_retries=N` per call.

        Args:
          command: Argv-style command. First element must be non-empty. For shell strings, wrap as
              `["sh", "-c", "<string>"]`.

          timeout_sec: Server-side execution timeout in seconds. Must be positive when provided; omit
              to use the server default.

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
                vm_run_params.VmRunParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecResult,
        )

    async def set_firewall(
        self,
        id: str,
        *,
        mode: str,
        ingress: Iterable[FirewallRule] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Vm:
        """Replaces the full firewall policy on a VM.

        Args:
          mode: Firewall mode.

        Known values: `open` (allow all inbound traffic), `restricted`
              (deny by default; only rules listed in `ingress` are allowed). Additional values
              may be introduced in future server versions.

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
                vm_set_firewall_params.VmSetFirewallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vm,
        )


class VmsResourceWithRawResponse:
    def __init__(self, vms: VmsResource) -> None:
        self._vms = vms

        self.retrieve = to_raw_response_wrapper(
            vms.retrieve,
        )
        self.update = to_raw_response_wrapper(
            vms.update,
        )
        self.list = to_raw_response_wrapper(
            vms.list,
        )
        self.delete = to_raw_response_wrapper(
            vms.delete,
        )
        self.console_token = to_raw_response_wrapper(
            vms.console_token,
        )
        self.launch = to_raw_response_wrapper(
            vms.launch,
        )
        self.patch_firewall = to_raw_response_wrapper(
            vms.patch_firewall,
        )
        self.run = to_raw_response_wrapper(
            vms.run,
        )
        self.set_firewall = to_raw_response_wrapper(
            vms.set_firewall,
        )

    @cached_property
    def files(self) -> FilesResourceWithRawResponse:
        """File upload/download to/from a running VM"""
        return FilesResourceWithRawResponse(self._vms.files)


class AsyncVmsResourceWithRawResponse:
    def __init__(self, vms: AsyncVmsResource) -> None:
        self._vms = vms

        self.retrieve = async_to_raw_response_wrapper(
            vms.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            vms.update,
        )
        self.list = async_to_raw_response_wrapper(
            vms.list,
        )
        self.delete = async_to_raw_response_wrapper(
            vms.delete,
        )
        self.console_token = async_to_raw_response_wrapper(
            vms.console_token,
        )
        self.launch = async_to_raw_response_wrapper(
            vms.launch,
        )
        self.patch_firewall = async_to_raw_response_wrapper(
            vms.patch_firewall,
        )
        self.run = async_to_raw_response_wrapper(
            vms.run,
        )
        self.set_firewall = async_to_raw_response_wrapper(
            vms.set_firewall,
        )

    @cached_property
    def files(self) -> AsyncFilesResourceWithRawResponse:
        """File upload/download to/from a running VM"""
        return AsyncFilesResourceWithRawResponse(self._vms.files)


class VmsResourceWithStreamingResponse:
    def __init__(self, vms: VmsResource) -> None:
        self._vms = vms

        self.retrieve = to_streamed_response_wrapper(
            vms.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            vms.update,
        )
        self.list = to_streamed_response_wrapper(
            vms.list,
        )
        self.delete = to_streamed_response_wrapper(
            vms.delete,
        )
        self.console_token = to_streamed_response_wrapper(
            vms.console_token,
        )
        self.launch = to_streamed_response_wrapper(
            vms.launch,
        )
        self.patch_firewall = to_streamed_response_wrapper(
            vms.patch_firewall,
        )
        self.run = to_streamed_response_wrapper(
            vms.run,
        )
        self.set_firewall = to_streamed_response_wrapper(
            vms.set_firewall,
        )

    @cached_property
    def files(self) -> FilesResourceWithStreamingResponse:
        """File upload/download to/from a running VM"""
        return FilesResourceWithStreamingResponse(self._vms.files)


class AsyncVmsResourceWithStreamingResponse:
    def __init__(self, vms: AsyncVmsResource) -> None:
        self._vms = vms

        self.retrieve = async_to_streamed_response_wrapper(
            vms.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            vms.update,
        )
        self.list = async_to_streamed_response_wrapper(
            vms.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            vms.delete,
        )
        self.console_token = async_to_streamed_response_wrapper(
            vms.console_token,
        )
        self.launch = async_to_streamed_response_wrapper(
            vms.launch,
        )
        self.patch_firewall = async_to_streamed_response_wrapper(
            vms.patch_firewall,
        )
        self.run = async_to_streamed_response_wrapper(
            vms.run,
        )
        self.set_firewall = async_to_streamed_response_wrapper(
            vms.set_firewall,
        )

    @cached_property
    def files(self) -> AsyncFilesResourceWithStreamingResponse:
        """File upload/download to/from a running VM"""
        return AsyncFilesResourceWithStreamingResponse(self._vms.files)
