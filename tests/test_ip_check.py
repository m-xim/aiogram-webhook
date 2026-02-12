from ipaddress import IPv4Address, IPv6Address

import pytest

from aiogram_webhook.security.checks.ip import IPCheck
from tests.fixtures import DummyBoundRequest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ip", "request_ip", "expected"),
    [
        # IPv4 single addresses
        ("8.8.8.8", "8.8.8.8", True),
        ("8.8.8.8", "1.2.3.4", False),
        ("1.1.1.1", "1.1.1.1", True),
        ("192.168.1.1", "192.168.1.1", True),
        ("192.168.1.1", "192.168.1.2", False),
        # IPv6 single addresses
        ("2001:4860:4860::8888", "2001:4860:4860::8888", True),
        ("2001:4860:4860::8888", "2001:4860:4860::1", False),
        # IPv4 networks
        ("192.168.1.0/24", "192.168.1.42", True),
        ("192.168.1.0/24", "192.168.1.1", True),
        ("192.168.1.0/24", "192.168.1.255", True),
        ("192.168.1.0/24", "192.168.2.1", False),
        ("10.0.0.0/8", "10.255.255.255", True),
        ("10.0.0.0/8", "11.0.0.0", False),
        # IPv6 networks
        ("2001:4860:4860::/48", "2001:4860:4860::8888", True),
        ("2001:4860:4860::/48", "2001:4860:4861::1", False),
    ],
    ids=[
        "ipv4-match",
        "ipv4-mismatch",
        "ipv4-match2",
        "ipv4-match3",
        "ipv4-mismatch2",
        "ipv6-match",
        "ipv6-mismatch",
        "net-match",
        "net-match1",
        "net-match255",
        "net-mismatch",
        "net-large-match",
        "net-large-mismatch",
        "ipv6-net-match",
        "ipv6-net-mismatch",
    ],
)
async def test_ip_check_verify(allowed_ip, request_ip, expected, bot):
    ip_check = IPCheck(allowed_ip, include_default=False)
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("request_ip", "expected"),
    [
        ("not-an-ip", False),
        ("999.999.999.999", False),
        ("192.168.1", False),
        ("192.168.1.1.1", False),
        ("", False),
        (None, False),
    ],
    ids=["invalid-text", "invalid-octets", "incomplete", "too-many", "empty", "none"],
)
async def test_ip_check_verify_invalid_format(request_ip, expected, bot):
    ip_check = IPCheck("8.8.8.8", include_default=False)
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ips", "request_ip", "expected"),
    [
        (("8.8.8.8", "1.1.1.1", "4.4.4.4"), "8.8.8.8", True),
        (("8.8.8.8", "1.1.1.1", "4.4.4.4"), "1.1.1.1", True),
        (("8.8.8.8", "1.1.1.1", "4.4.4.4"), "4.4.4.4", True),
        (("8.8.8.8", "1.1.1.1", "4.4.4.4"), "2.2.2.2", False),
    ],
    ids=["first-match", "second-match", "third-match", "no-match"],
)
async def test_ip_check_verify_multiple_ips(allowed_ips, request_ip, expected, bot):
    ip_check = IPCheck(*allowed_ips, include_default=False)
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_mixed", "request_ip", "expected"),
    [
        (("8.8.8.8", "192.168.1.0/24", "1.1.1.1"), "8.8.8.8", True),
        (("8.8.8.8", "192.168.1.0/24", "1.1.1.1"), "192.168.1.100", True),
        (("8.8.8.8", "192.168.1.0/24", "1.1.1.1"), "1.1.1.1", True),
        (("8.8.8.8", "192.168.1.0/24", "1.1.1.1"), "2.2.2.2", False),
    ],
    ids=["ip-match", "network-match", "ip-match2", "no-match"],
)
async def test_ip_check_verify_mixed(allowed_mixed, request_ip, expected, bot):
    ip_check = IPCheck(*allowed_mixed, include_default=False)
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("include_default", "request_ip", "expected"),
    [
        # include_default=True - Telegram IPs should pass
        (True, "149.154.160.1", True),
        (True, "91.108.4.0", True),
        (True, "8.8.8.8", False),
        # include_default=False - Telegram IPs should NOT pass
        (False, "149.154.160.1", False),
    ],
    ids=["default-telegram-ip1", "default-telegram-ip2", "default-non-telegram", "exclude-default-telegram"],
)
async def test_ip_check_default_networks(include_default, request_ip, expected, bot):
    ip_check = IPCheck(include_default=include_default)
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("ip_object", "request_ip", "expected"),
    [
        (IPv4Address("8.8.8.8"), "8.8.8.8", True),
        (IPv4Address("8.8.8.8"), "1.1.1.1", False),
        (IPv6Address("2001:4860:4860::8888"), "2001:4860:4860::8888", True),
        (IPv6Address("2001:4860:4860::8888"), "2001:4860:4860::1", False),
    ],
    ids=["ipv4-match", "ipv4-mismatch", "ipv6-match", "ipv6-mismatch"],
)
async def test_ip_check_verify_ipaddress_objects(ip_object, request_ip, expected, bot):
    ip_check = IPCheck(ip_object, include_default=False)
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected
