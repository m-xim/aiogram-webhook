import pytest

from aiogram_webhook.security.checks.ip import IPCheck
from tests.fixtures import DummyBoundRequest, DummyRequest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ips", "request_ip", "expected"),
    [
        (("8.8.8.8",), "8.8.8.8", True),
        (("8.8.8.8",), "1.1.1.1", False),
        (("8.8.8.8", "1.1.1.1"), "1.1.1.1", True),
        (("192.168.1.0/24",), "192.168.1.42", True),
        (("8.8.8.8",), None, False),
    ],
    ids=[
        "direct-match",
        "direct-no-match",
        "direct-multi-match",
        "direct-network-match",
        "direct-no-ip",
    ],
)
async def test_ip_check_direct(allowed_ips, request_ip, expected, bot):
    req = DummyBoundRequest(DummyRequest(ip=request_ip))
    ip_check = IPCheck(*allowed_ips, include_default=False)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ips", "x_forwarded_for", "expected"),
    [
        (("8.8.8.8",), "8.8.8.8", True),
        (("8.8.8.8",), "1.1.1.1", False),
        (("8.8.8.8", "1.1.1.1"), "8.8.8.8", True),
        (("192.168.1.0/24",), "192.168.1.42", True),
        (("8.8.8.8",), "not-an-ip", False),
        (("8.8.8.8",), "", False),
        (("8.8.8.8",), None, False),
    ],
    ids=[
        "forwarded-match",
        "forwarded-no-match",
        "forwarded-multi-match",
        "forwarded-network-match",
        "forwarded-invalid",
        "forwarded-empty",
        "forwarded-no-header",
    ],
)
async def test_ip_check_forwarded(allowed_ips, x_forwarded_for, expected, bot):
    headers = {"X-Forwarded-For": x_forwarded_for} if x_forwarded_for is not None else None
    req = DummyBoundRequest(DummyRequest(ip="127.0.0.1", headers=headers))
    ip_check = IPCheck(*allowed_ips, include_default=False)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ips", "request_ip", "x_forwarded_for", "expected"),
    [
        (("8.8.8.8",), "8.8.8.8", "1.1.1.1", False),
        (("8.8.8.8",), "1.1.1.1", "8.8.8.8", True),
        (("8.8.8.8",), "8.8.8.8", "not-an-ip", False),
        (("8.8.8.8",), "not-an-ip", "8.8.8.8", True),
        (("8.8.8.8",), "not-an-ip", "not-an-ip", False),
    ],
    ids=[
        "both-priority-no-match",
        "both-priority-match",
        "both-invalid-forwarded",
        "both-invalid-direct",
        "both-both-invalid",
    ],
)
async def test_ip_check_both_priority(allowed_ips, request_ip, x_forwarded_for, expected, bot):
    headers = {"X-Forwarded-For": x_forwarded_for}
    req = DummyBoundRequest(DummyRequest(ip=request_ip, headers=headers))
    ip_check = IPCheck(*allowed_ips, include_default=False)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ips", "request_ip", "x_forwarded_for", "expected"),
    [
        (("8.8.8.8",), "127.0.0.1", "8.8.8.8, not-an-ip", True),
        (("8.8.8.8",), "127.0.0.1", "not-an-ip, 8.8.8.8", False),
    ],
    ids=[
        "edgecase-first-valid",
        "edgecase-first-invalid",
    ],
)
async def test_ip_check_edge_cases(allowed_ips, request_ip, x_forwarded_for, expected, bot):
    headers = {"X-Forwarded-For": x_forwarded_for}
    req = DummyBoundRequest(DummyRequest(ip=request_ip, headers=headers))
    ip_check = IPCheck(*allowed_ips, include_default=False)
    assert await ip_check.verify(bot, req) is expected
