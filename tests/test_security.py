import pytest
from aiogram import Bot

from aiogram_webhook.security.checks.ip import IPCheck
from aiogram_webhook.security.secret_token import StaticSecretToken
from aiogram_webhook.security.security import Security
from tests.conftest import DummyBoundRequest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("secret_token", "request_token", "expected"),
    [
        ("my-secret", "my-secret", True),
        ("my-secret", "wrong", False),
        ("my-secret", None, False),
    ],
)
async def test_static_secret_token_verify(secret_token, request_token, expected):
    checker = StaticSecretToken(secret_token)
    bot = Bot("42:TEST")
    req = DummyBoundRequest(secret_token=request_token)
    assert await checker.verify(bot, req) is expected
    assert checker.secret_token(bot) == secret_token


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("secret_token", "request_token", "expected"),
    [
        ("my-secret", "my-secret", True),
        ("my-secret", "wrong", False),
    ],
)
async def test_security_with_secret_token(secret_token, request_token, expected):
    checker = StaticSecretToken(secret_token)
    sec = Security(secret_token=checker)
    bot = Bot("42:TEST")
    req = DummyBoundRequest(secret_token=request_token)
    assert await sec.verify(bot, req) is expected
    assert await sec.get_secret_token(bot=bot) == secret_token


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("allowed_ip", "request_ip", "expected"),
    [
        ("8.8.8.8", "8.8.8.8", True),
        ("8.8.8.8", "1.2.3.4", False),
    ],
)
async def test_security_with_ip_check(allowed_ip, request_ip, expected):
    ip_check = IPCheck(allowed_ip, include_default=False)
    sec = Security(ip_check)
    bot = Bot("42:TEST")
    req = DummyBoundRequest(ip=request_ip)
    assert await sec.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("network", "request_ip", "expected"),
    [
        ("192.168.1.0/24", "192.168.1.42", True),
        ("192.168.1.0/24", "10.0.0.1", False),
    ],
)
async def test_ip_check_with_network(network, request_ip, expected):
    ip_check = IPCheck(network, include_default=False)
    bot = Bot("42:TEST")
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("request_ip", "expected"),
    [
        ("not-an-ip", False),
        (None, False),
    ],
)
async def test_ip_check_invalid_ip(request_ip, expected):
    ip_check = IPCheck("8.8.8.8", include_default=False)
    bot = Bot("42:TEST")
    req = DummyBoundRequest(ip=request_ip)
    assert await ip_check.verify(bot, req) is expected
