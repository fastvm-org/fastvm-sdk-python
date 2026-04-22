"""Fixtures for live tests. All live tests auto-skip without FASTVM_API_KEY."""

from __future__ import annotations

import os
import random
import string
from typing import Iterator, AsyncIterator

import pytest
import pytest_asyncio

from fastvm import FastvmClient, AsyncFastvmClient
from fastvm.types.vm import Vm


def _name() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f"sdk-test-{suffix}"


def _base_url() -> str:
    return os.environ.get("FASTVM_BASE_URL", "https://api.fastvm.org")


def _require_key() -> str:
    key = os.environ.get("FASTVM_API_KEY")
    if not key:
        pytest.skip("FASTVM_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def client() -> Iterator[FastvmClient]:
    with FastvmClient(api_key=_require_key(), base_url=_base_url()) as c:
        yield c


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_client() -> AsyncIterator[AsyncFastvmClient]:
    async with AsyncFastvmClient(api_key=_require_key(), base_url=_base_url()) as c:
        yield c


@pytest.fixture()
def vm(client: FastvmClient) -> Iterator[Vm]:
    v = client.launch(machine_type="c1m2", name=_name())
    try:
        yield v
    finally:
        try:
            client.vms.delete(v.id)
        except Exception:
            pass


@pytest_asyncio.fixture(loop_scope="session")
async def async_vm(async_client: AsyncFastvmClient) -> AsyncIterator[Vm]:
    v = await async_client.launch(machine_type="c1m2", name=_name())
    try:
        yield v
    finally:
        try:
            await async_client.vms.delete(v.id)
        except Exception:
            pass
