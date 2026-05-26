import pytest

from aiogram_webhook.security.checks.ip import IPCheck
from tests.fixtures.request import DummyRequest, DummyWebRequest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ips", "request_ip", "x_forwarded_for", "expected"),
    [
        (("8.8.8.8",), "8.8.8.8", None, True),
        (("192.168.1.0/24",), "192.168.1.42", None, True),
        (("8.8.8.8", "1.1.1.1"), "1.1.1.1", None, True),
        (("8.8.8.8",), "1.1.1.1", None, False),
        (("8.8.8.8",), None, None, False),
        (("8.8.8.8",), "1.1.1.1", "8.8.8.8", True),
        (("8.8.8.8",), "8.8.8.8", "1.1.1.1", False),
        (("8.8.8.8",), "127.0.0.1", "8.8.8.8, 1.1.1.1", True),
        (("8.8.8.8",), "127.0.0.1", "not-an-ip, 8.8.8.8", False),
        (("8.8.8.8",), "8.8.8.8", "not-an-ip", False),
        (("8.8.8.8",), "8.8.8.8", "", True),
    ],
    ids=[
        "direct-address",
        "direct-network",
        "direct-multiple-allowed",
        "direct-denied",
        "direct-missing",
        "forwarded-overrides-denied-direct",
        "forwarded-overrides-allowed-direct",
        "forwarded-first-address-only",
        "forwarded-invalid-first-address",
        "forwarded-invalid",
        "empty-forwarded-falls-back-to-direct",
    ],
)
async def test_ip_check_matches_allowed_client_ip(target, allowed_ips, request_ip, x_forwarded_for, expected):
    headers = {"X-Forwarded-For": x_forwarded_for} if x_forwarded_for is not None else None
    request = DummyWebRequest(DummyRequest(ip=request_ip, headers=headers))
    ip_check = IPCheck(*allowed_ips, include_default=False)

    assert await ip_check.verify(target=target, request=request, route_params={}) is expected
