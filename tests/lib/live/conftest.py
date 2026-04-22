"""Live-test fixtures. Require ``FASTVM_API_KEY``; auto-skip otherwise."""

from __future__ import annotations

import os
import random
import string
from typing import Iterator, AsyncIterator

import pytest
import pytest_asyncio

from fastvm import FastvmClient, AsyncFastvmClient
from fastvm.types.vm import Vm


def _rand_suffix(n: int = 6) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


def _base_url() -> str:
    return os.environ.get("FASTVM_BASE_URL", "https://api.fastvm.org")


def _api_key() -> str | None:
    return os.environ.get("FASTVM_API_KEY") or None


@pytest.fixture(scope="session")
def client() -> Iterator[FastvmClient]:
    key = _api_key()
    if not key:
        pytest.skip("FASTVM_API_KEY not set")
    with FastvmClient(api_key=key, base_url=_base_url()) as c:
        yield c


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_client() -> AsyncIterator[AsyncFastvmClient]:
    key = _api_key()
    if not key:
        pytest.skip("FASTVM_API_KEY not set")
    async with AsyncFastvmClient(api_key=key, base_url=_base_url()) as c:
        yield c


@pytest.fixture()
def vm_name() -> str:
    return f"sdk-test-{_rand_suffix()}"


@pytest.fixture()
def vm(client: FastvmClient, vm_name: str) -> Iterator[Vm]:
    """Launch a VM for one test; delete it on teardown regardless of outcome."""
    v = client.launch(machine_type="c1m2", name=vm_name)
    try:
        yield v
    finally:
        # Best-effort teardown — already-deleted VMs / transient failures don't
        # fail the test that just ran.
        try:
            client.vms.delete(v.id)
        except Exception:
            pass


@pytest_asyncio.fixture(loop_scope="session")
async def async_vm(async_client: AsyncFastvmClient, vm_name: str) -> AsyncIterator[Vm]:
    v = await async_client.launch(machine_type="c1m2", name=vm_name)
    try:
        yield v
    finally:
        try:
            await async_client.vms.delete(v.id)
        except Exception:
            pass
