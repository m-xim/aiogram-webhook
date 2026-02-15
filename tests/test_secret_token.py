import pytest

from aiogram_webhook.security import Security, StaticSecretToken
from tests.fixtures import DummyBoundRequest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("secret_token", "request_token", "expected"),
    [
        ("my-secret", "my-secret", True),
        ("my-secret", "wrong-secret", False),
        ("my-secret", None, False),
    ],
    ids=["match", "mismatch", "none"],
)
async def test_security_secret_token(secret_token, request_token, expected, bot):
    sec = Security(secret_token=StaticSecretToken(secret_token))
    req = DummyBoundRequest(secret_token=request_token)
    assert await sec.verify(bot, req) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("secret_token", "expected"),
    [
        (StaticSecretToken("test-secret"), "test-secret"),
        (None, None),
    ],
    ids=["with-secret", "without-secret"],
)
async def test_security_get_secret_token(secret_token, expected, bot):
    sec = Security(secret_token=secret_token)
    assert await sec.get_secret_token(bot=bot) == expected
