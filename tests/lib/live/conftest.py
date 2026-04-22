"""Fixtures for live tests. All live tests auto-skip without FASTVM_API_KEY.

VM fixtures are **session-scoped**: each pytest-xdist worker launches one
``sdk-test-*`` VM up front and reuses it across every test on that worker.
Tests that mutate global state (e.g. renaming the VM) must restore it.
Tests that need their own VM (``launch(wait=False)``, snapshot restore)
create + delete inline.

A ``_stale_vm_sweep`` autouse fixture runs once per worker at session
start and deletes any leftover ``sdk-test-*`` VMs older than 15 minutes —
cleans up after crashed prior runs without racing against concurrent CI
sessions.
"""

from __future__ import annotations

import os
import uuid
import random
import string
from typing import Iterator, AsyncIterator
from datetime import datetime, timezone, timedelta

import pytest
import pytest_asyncio

from fastvm import FastvmClient, AsyncFastvmClient
from fastvm.types.vm import Vm

_NAME_PREFIX = "sdk-test-"
_STALE_AFTER = timedelta(minutes=15)


def _name() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f"{_NAME_PREFIX}{suffix}"


def _base_url() -> str:
    # `.get(..., default)` returns the empty string when the env var is set
    # but empty (e.g. GitHub Actions injects empty `${{ inputs.* }}` on
    # non-workflow_dispatch events). Use `or` to fall through to the default.
    return os.environ.get("FASTVM_BASE_URL") or "https://api.fastvm.org"


def _require_key() -> str:
    key = os.environ.get("FASTVM_API_KEY")
    if not key:
        pytest.skip("FASTVM_API_KEY not set")
    return key


# --------------------------------------------------------------------------- #
#                             Pre-session sweeper                             #
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="session", autouse=True)
def _stale_vm_sweep(client: FastvmClient) -> None:  # pyright: ignore[reportUnusedFunction]
    """Delete leftover ``sdk-test-*`` VMs older than 15 min (once per worker)."""
    cutoff = datetime.now(timezone.utc) - _STALE_AFTER
    for v in client.vms.list():
        if not v.name.startswith(_NAME_PREFIX):
            continue
        if v.status == "deleting":
            continue
        if v.created_at > cutoff:
            continue
        try:
            client.vms.delete(v.id)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
#                                  Clients                                    #
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="session")
def client() -> Iterator[FastvmClient]:
    with FastvmClient(api_key=_require_key(), base_url=_base_url()) as c:
        yield c


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_client() -> AsyncIterator[AsyncFastvmClient]:
    async with AsyncFastvmClient(api_key=_require_key(), base_url=_base_url()) as c:
        yield c


# --------------------------------------------------------------------------- #
#                             Shared session VMs                              #
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="session")
def vm(client: FastvmClient) -> Iterator[Vm]:
    """One VM per pytest-xdist worker, reused across tests."""
    v = client.launch(machine_type="c1m2", name=_name())
    try:
        yield v
    finally:
        try:
            client.vms.delete(v.id)
        except Exception:
            pass


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_vm(async_client: AsyncFastvmClient) -> AsyncIterator[Vm]:
    v = await async_client.launch(machine_type="c1m2", name=_name())
    try:
        yield v
    finally:
        try:
            await async_client.vms.delete(v.id)
        except Exception:
            pass


@pytest.fixture()
def workdir(vm: Vm, client: FastvmClient) -> Iterator[str]:
    """Per-test workspace inside the session VM. Isolates file paths."""
    d = f"/root/work-{uuid.uuid4().hex[:8]}"
    client.vms.run(vm.id, command=["mkdir", "-p", d])
    try:
        yield d
    finally:
        try:
            client.vms.run(vm.id, command=["rm", "-rf", d])
        except Exception:
            pass
