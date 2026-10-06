import pytest

from aiogram_webhook.engines.target import Target
from aiogram_webhook.security import Security, StaticSecretToken
from aiogram_webhook.security.errors import SecretTokenError
from aiogram_webhook.security.secret_token import SECRET_TOKEN_HEADER, SecretToken
from tests.fixtures.web_request import DummyRequest, DummyWebRequest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("request_token", "expected"),
    [
        ("my-secret", True),
        ("wrong-secret", False),
        (None, False),
    ],
    ids=["match", "mismatch", "none"],
)
async def test_secret_token_check_verifies_telegram_header(target, request_token, expected):
    secret_token = StaticSecretToken("my-secret")
    headers = {SECRET_TOKEN_HEADER: request_token} if request_token is not None else {}
    req = DummyWebRequest(DummyRequest(headers=headers))

    assert await secret_token.verify(target=target, request=req, route_params={}) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_token",
    ["секрет", "\ud800", "😀"],
    ids=["cyrillic", "surrogate", "surrogate-pair"],
)
async def test_secret_token_check_rejects_non_ascii_header_without_error(target, request_token):
    secret_token = StaticSecretToken("my-secret")
    req = DummyWebRequest(DummyRequest(headers={SECRET_TOKEN_HEADER: request_token}))

    assert await secret_token.verify(target=target, request=req, route_params={}) is False


@pytest.mark.parametrize("secret_token", ["", "has space", "x" * 257])
def test_secret_token_check_rejects_telegram_incompatible_values(secret_token):
    with pytest.raises(ValueError, match="Invalid secret token format"):
        StaticSecretToken(secret_token)


class PerBotSecretToken(SecretToken):
    async def secret_token(self, target: Target) -> str:
        return f"secret-{target.bot_id}"


@pytest.mark.asyncio
async def test_security_returns_none_without_configured_secret_token(target):
    assert await Security().secret_token(target=target) is None


@pytest.mark.asyncio
async def test_security_resolves_and_verifies_secret_token_per_target(target, other_target):
    security = Security(secret_token=PerBotSecretToken())
    request = DummyWebRequest(DummyRequest(headers={SECRET_TOKEN_HEADER: "secret-42"}))

    assert await security.secret_token(target=target) == "secret-42"
    assert await security.secret_token(target=other_target) == "secret-7"
    await security.verify(target=target, request=request, route_params={})
    with pytest.raises(SecretTokenError):
        await security.verify(target=other_target, request=request, route_params={})
