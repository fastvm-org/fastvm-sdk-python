"""Read-only smoke tests that don't need a VM."""

from __future__ import annotations

from fastvm import FastvmClient


def test_quotas(client: FastvmClient) -> None:
    q = client.quotas.retrieve()
    assert q.limits is not None
    assert q.usage is not None
