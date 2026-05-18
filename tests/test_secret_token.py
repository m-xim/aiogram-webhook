import pytest

from aiogram_webhook.engines.target import Target
from aiogram_webhook.security import Security, StaticSecretToken
from aiogram_webhook.security.errors import SecretTokenError
from aiogram_webhook.security.secret_token import SECRET_TOKEN_HEADER
from tests.fixtures import DummyRequest, dummy_web_request

TARGET = Target(bot_id=42, bot_token="42:TEST")


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
async def test_security_secret_token(secret_token, request_token, expected):
    sec = Security(secret_token=StaticSecretToken(secret_token))
    headers = {SECRET_TOKEN_HEADER: request_token} if request_token is not None else {}
    req = dummy_web_request(DummyRequest(headers=headers))

    if expected:
        await sec.verify(target=TARGET, request=req, route_params={})
    else:
        with pytest.raises(SecretTokenError):
            await sec.verify(target=TARGET, request=req, route_params={})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("secret_token", "expected"),
    [
        (StaticSecretToken("test-secret"), "test-secret"),
        (None, None),
    ],
    ids=["with-secret", "without-secret"],
)
async def test_security_secret_token_getter(secret_token, expected):
    sec = Security(secret_token=secret_token)
    assert await sec.secret_token(target=TARGET) == expected
