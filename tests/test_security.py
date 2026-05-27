import pytest

from aiogram_webhook.security.errors import SecretTokenError, SecurityCheckError
from aiogram_webhook.security.secret_token import SECRET_TOKEN_HEADER, StaticSecretToken
from aiogram_webhook.security.security import Security
from tests.fixtures.security_checks import RecordingCheck
from tests.fixtures.web_request import DummyRequest, DummyWebRequest


@pytest.mark.asyncio
async def test_security_pipeline_allows_request_without_checks_or_secret_token(target):
    security = Security()

    await security.verify(target=target, request=DummyWebRequest(), route_params={})


@pytest.mark.asyncio
async def test_security_pipeline_stops_at_first_failed_check(target):
    calls: list[str] = []
    security = Security(
        RecordingCheck("first", result=True, calls=calls),
        RecordingCheck("second", result=False, calls=calls),
        RecordingCheck("third", result=True, calls=calls),
    )
    request = DummyWebRequest(DummyRequest(ip="127.0.0.1"))

    with pytest.raises(SecurityCheckError) as exc_info:
        await security.verify(target=target, request=request, route_params={})

    assert calls == ["first", "second"]
    assert exc_info.value.security_check == "RecordingCheck"
    assert exc_info.value.client_ip == "127.0.0.1"


@pytest.mark.asyncio
async def test_security_pipeline_allows_request_when_secret_token_and_checks_pass(target):
    calls: list[str] = []
    security = Security(
        RecordingCheck("check", result=True, calls=calls),
        secret_token=StaticSecretToken("secret"),
    )
    request = DummyWebRequest(DummyRequest(headers={SECRET_TOKEN_HEADER: "secret"}))

    await security.verify(target=target, request=request, route_params={})

    assert calls == ["check"]


@pytest.mark.asyncio
async def test_security_pipeline_runs_checks_after_valid_secret_token(target):
    calls: list[str] = []
    security = Security(
        RecordingCheck("check", result=False, calls=calls),
        secret_token=StaticSecretToken("secret"),
    )
    request = DummyWebRequest(DummyRequest(headers={SECRET_TOKEN_HEADER: "secret"}))

    with pytest.raises(SecurityCheckError):
        await security.verify(target=target, request=request, route_params={})

    assert calls == ["check"]


@pytest.mark.asyncio
async def test_security_pipeline_rejects_bad_secret_token_before_checks(target):
    calls: list[str] = []
    security = Security(
        RecordingCheck("check", result=True, calls=calls),
        secret_token=StaticSecretToken("secret"),
    )
    request = DummyWebRequest(DummyRequest(headers={SECRET_TOKEN_HEADER: "wrong"}))

    with pytest.raises(SecretTokenError) as exc_info:
        await security.verify(target=target, request=request, route_params={})

    assert calls == []
    assert exc_info.value.target_bot_id == target.bot_id
