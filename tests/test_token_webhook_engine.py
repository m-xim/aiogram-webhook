import pytest

from aiogram_webhook.configs.bot import BotConfig
from aiogram_webhook.engines.token import TokenEngine
from tests.fixtures.web_request import DummyRequest, DummyWebRequest
from tests.fixtures.webhook_engine import CapturingAdapter, DummyDispatcher, DummyRoute


@pytest.mark.asyncio
async def test_token_webhook_engine_dispatches_to_bot_resolved_from_route_token(bot, bot_id, bot_token, update_payload):
    adapter = CapturingAdapter()
    dispatcher = DummyDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = TokenEngine(
            dispatcher,
            web=adapter,
            route=DummyRoute({"bot_token": bot_token}),
            bot_config=BotConfig(session=bot.session),
            handle_in_background=False,
        )

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))

    assert response["status_code"] == 200
    assert dispatcher.webhook_bot is engine.bots[bot_id]
    assert dispatcher.webhook_bot.token == bot_token
    assert dispatcher.webhook_update == update_payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "route_params",
    [
        {},
        {"bot_token": ""},
        {"bot_token": "not-a-token"},
    ],
    ids=["missing", "empty", "invalid"],
)
async def test_token_webhook_engine_returns_not_found_when_route_token_is_missing_or_invalid(
    bot, route_params, update_payload
):
    adapter = CapturingAdapter()
    dispatcher = DummyDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = TokenEngine(
            dispatcher,
            web=adapter,
            route=DummyRoute(route_params),
            bot_config=BotConfig(session=bot.session),
            handle_in_background=False,
        )

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))

    assert response == {"kind": "json", "status_code": 404, "data": {"detail": "Not found"}, "headers": None}
    assert dispatcher.webhook_update is None
    assert engine.bots == {}


def test_token_webhook_engine_security_warning_mentions_engine(bot, bot_token):
    adapter = CapturingAdapter()
    dispatcher = DummyDispatcher()

    with pytest.warns(UserWarning, match="Security is not configured for TokenEngine"):
        TokenEngine(
            dispatcher,
            web=adapter,
            route=DummyRoute({"bot_token": bot_token}),
            bot_config=BotConfig(session=bot.session),
        )
