import asyncio

import pytest
from aiogram import Bot

from aiogram_webhook.engines.single import SingleBotEngine
from tests.fixtures.shutdown import BlockingShutdownDispatcher, TrackableSession
from tests.fixtures.webhook_engine import DummyDispatcher, DummyRoute


@pytest.mark.asyncio
async def test_single_bot_engine_uses_configured_bot_instead_of_route_params(bot, bot_token, adapter, update_request):
    dispatcher = DummyDispatcher()
    engine = SingleBotEngine(
        dispatcher,
        bot,
        web=adapter,
        route=DummyRoute({"bot_token": "100:OTHER"}),  # ty:ignore[invalid-argument-type]
        handle_in_background=False,
    )

    response = await engine.handle_request(update_request)

    assert response["status_code"] == 200
    assert dispatcher.webhook_bot is bot
    assert dispatcher.webhook_bot.token == bot_token
    assert dispatcher.webhook_update == update_request.raw.json_data


@pytest.mark.asyncio
async def test_background_engine_rejects_request_after_shutdown_with_closed_bot_session(adapter, update_request):
    session = TrackableSession()
    bot = Bot("42:TEST", session=session)
    dispatcher = BlockingShutdownDispatcher()
    engine = SingleBotEngine(
        dispatcher,
        bot,
        web=adapter,
        route=DummyRoute({"bot_token": bot.token}),  # ty:ignore[invalid-argument-type]
        handle_in_background=True,
    )

    dispatcher.release_shutdown.set()
    await engine.on_shutdown(None)

    response = await engine.handle_request(update_request)
    await asyncio.sleep(0)
    dispatcher.background_continue.set()
    if engine._task_tracker._tasks:
        await asyncio.wait_for(asyncio.gather(*engine._task_tracker._tasks), timeout=1)

    assert session.closed is True
    assert response["status_code"] == 503
    assert dispatcher.background_updates == []
    assert dispatcher.background_session_closed == []


@pytest.mark.asyncio
async def test_foreground_engine_rejects_request_after_shutdown_with_closed_bot_session(adapter, update_request):
    session = TrackableSession()
    bot = Bot("42:TEST", session=session)
    dispatcher = BlockingShutdownDispatcher()
    engine = SingleBotEngine(
        dispatcher,
        bot,
        web=adapter,
        route=DummyRoute({"bot_token": bot.token}),  # ty:ignore[invalid-argument-type]
        handle_in_background=False,
    )

    dispatcher.release_shutdown.set()
    await engine.on_shutdown(None)

    response = await engine.handle_request(update_request)

    assert session.closed is True
    assert response["status_code"] == 503
    assert dispatcher.foreground_updates == []
    assert dispatcher.foreground_session_closed == []
