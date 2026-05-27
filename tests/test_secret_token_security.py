import pytest

from aiogram_webhook.security import Security, StaticSecretToken
from aiogram_webhook.security.secret_token import SECRET_TOKEN_HEADER
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


@pytest.mark.parametrize("secret_token", ["", "has space", "x" * 257])
def test_secret_token_check_rejects_telegram_incompatible_values(secret_token):
    with pytest.raises(ValueError, match="Invalid secret token format"):
        StaticSecretToken(secret_token)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("secret_token", "expected"),
    [
        (StaticSecretToken("my-secret"), "my-secret"),
        (None, None),
    ],
    ids=["with-secret", "without-secret"],
)
async def test_security_resolves_secret_token_from_static_value_or_callable(target, secret_token, expected):
    sec = Security(secret_token=secret_token)
    assert await sec.secret_token(target=target) == expected
