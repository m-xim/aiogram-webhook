import asyncio

import pytest
from aiogram import Bot

from aiogram_webhook.engines.single import SingleBotEngine
from tests.fixtures.shutdown import BlockingDispatcher, BlockingShutdownDispatcher, TrackableSession
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


@pytest.mark.asyncio
async def test_single_bot_engine_rejects_new_requests_once_shutdown_has_started(bot, update_payload):
    adapter = CapturingAdapter()
    dispatcher = BlockingDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = SingleBotEngine(
            dispatcher,
            bot,
            web=adapter,
            route=DummyRoute({"bot_token": "100:OTHER"}),
            handle_in_background=True,
        )

    await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))
    await asyncio.sleep(0)
    assert dispatcher.started_updates == 1

    shutdown_task = asyncio.create_task(engine.on_shutdown(app=None))
    await asyncio.sleep(0)

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data={"update_id": 2})))

    dispatcher.release_updates.set()
    await shutdown_task

    assert response["status_code"] == 503
    assert dispatcher.started_updates == 1


@pytest.mark.asyncio
async def test_background_engine_rejects_request_during_shutdown(bot, update_payload):
    adapter = CapturingAdapter()
    dispatcher = BlockingShutdownDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = SingleBotEngine(
            dispatcher,
            bot,
            web=adapter,
            route=DummyRoute({"bot_token": bot.token}),
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
        if engine._task_tracker._tasks:
            await asyncio.wait_for(asyncio.gather(*engine._task_tracker._tasks), timeout=1)

    assert response["status_code"] == 503
    assert dispatcher.background_updates == []
    assert len(engine._task_tracker._tasks) == 0


@pytest.mark.asyncio
async def test_foreground_engine_rejects_request_during_shutdown(bot, update_payload):
    adapter = CapturingAdapter()
    dispatcher = BlockingShutdownDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = SingleBotEngine(
            dispatcher,
            bot,
            web=adapter,
            route=DummyRoute({"bot_token": bot.token}),
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


@pytest.mark.asyncio
async def test_background_engine_rejects_request_after_shutdown_with_closed_bot_session(update_payload):
    session = TrackableSession()
    bot = Bot("42:TEST", session=session)
    adapter = CapturingAdapter()
    dispatcher = BlockingShutdownDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = SingleBotEngine(
            dispatcher,
            bot,
            web=adapter,
            route=DummyRoute({"bot_token": bot.token}),
            handle_in_background=True,
        )

    dispatcher.release_shutdown.set()
    await engine.on_shutdown(None)

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))
    await asyncio.sleep(0)
    dispatcher.background_continue.set()
    if engine._task_tracker._tasks:
        await asyncio.wait_for(asyncio.gather(*engine._task_tracker._tasks), timeout=1)

    assert session.closed is True
    assert response["status_code"] == 503
    assert dispatcher.background_updates == []
    assert dispatcher.background_session_closed == []


@pytest.mark.asyncio
async def test_foreground_engine_rejects_request_after_shutdown_with_closed_bot_session(update_payload):
    session = TrackableSession()
    bot = Bot("42:TEST", session=session)
    adapter = CapturingAdapter()
    dispatcher = BlockingShutdownDispatcher()
    with pytest.warns(UserWarning, match="Security is not configured"):
        engine = SingleBotEngine(
            dispatcher,
            bot,
            web=adapter,
            route=DummyRoute({"bot_token": bot.token}),
            handle_in_background=False,
        )

    dispatcher.release_shutdown.set()
    await engine.on_shutdown(None)

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_data=update_payload)))

    assert session.closed is True
    assert response["status_code"] == 503
    assert dispatcher.foreground_updates == []
    assert dispatcher.foreground_session_closed == []
