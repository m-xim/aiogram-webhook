import asyncio

import pytest

from aiogram_webhook.configs.bot import BotConfig
from aiogram_webhook.engines.token import TokenEngine
from tests.fixtures.shutdown import BlockingShutdownDispatcher
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


@pytest.mark.asyncio
async def test_token_background_engine_rejects_request_during_shutdown_without_creating_bot_or_tracker(
    bot, update_payload
):
    adapter = CapturingAdapter()
    dispatcher = BlockingShutdownDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = TokenEngine(
            dispatcher,
            web=adapter,
            route=DummyRoute({"bot_token": bot.token}),
            bot_config=BotConfig(session=bot.session),
            handle_in_background=True,
        )

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))
    await asyncio.wait_for(dispatcher.shutdown_started.wait(), timeout=1)

    try:
        response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))
        await asyncio.sleep(0)
    finally:
        dispatcher.background_continue.set()
        dispatcher.release_shutdown.set()
        await asyncio.wait_for(shutdown_task, timeout=1)
        for tracker in engine._task_trackers.values():
            if tracker._tasks:
                await asyncio.wait_for(asyncio.gather(*tracker._tasks), timeout=1)

    assert response["status_code"] == 503
    assert dispatcher.background_updates == []
    assert bot.id not in engine.bots
    assert bot.id not in engine._task_trackers


@pytest.mark.asyncio
async def test_token_foreground_engine_rejects_request_during_shutdown_without_creating_bot(bot, update_payload):
    adapter = CapturingAdapter()
    dispatcher = BlockingShutdownDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = TokenEngine(
            dispatcher,
            web=adapter,
            route=DummyRoute({"bot_token": bot.token}),
            bot_config=BotConfig(session=bot.session),
            handle_in_background=False,
        )

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))
    await asyncio.wait_for(dispatcher.shutdown_started.wait(), timeout=1)

    try:
        response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))
    finally:
        dispatcher.release_shutdown.set()
        await asyncio.wait_for(shutdown_task, timeout=1)

    assert response["status_code"] == 503
    assert dispatcher.foreground_updates == []
    assert bot.id not in engine.bots
