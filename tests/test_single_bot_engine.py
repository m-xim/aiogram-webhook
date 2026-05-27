import pytest

from aiogram_webhook.engines.single import SingleBotEngine
from tests.fixtures.web_request import DummyRequest, DummyWebRequest
from tests.fixtures.webhook_engine import CapturingAdapter, DummyDispatcher, DummyRoute


@pytest.mark.asyncio
async def test_single_bot_engine_uses_configured_bot_instead_of_route_params(bot, bot_token, update_payload):
    adapter = CapturingAdapter()
    dispatcher = DummyDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = SingleBotEngine(
            dispatcher,
            bot,
            web=adapter,
            route=DummyRoute({"bot_token": "100:OTHER"}),
            handle_in_background=False,
        )

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))

    assert response["status_code"] == 200
    assert dispatcher.webhook_bot is bot
    assert dispatcher.webhook_bot.token == bot_token
    assert dispatcher.webhook_update == update_payload
