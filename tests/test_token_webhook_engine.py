import asyncio

import pytest

from aiogram_webhook.configs.bot import BotConfig
from aiogram_webhook.engines.token import TokenEngine
from tests.fixtures.shutdown import BlockingShutdownDispatcher
from tests.fixtures.webhook_engine import DummyDispatcher, DummyRoute


@pytest.mark.asyncio
async def test_token_webhook_engine_dispatches_to_bot_resolved_from_route_token(
    bot, bot_id, bot_token, adapter, update_request
):
    dispatcher = DummyDispatcher()
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute({"bot_token": bot_token}),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=False,
    )

    response = await engine.handle_request(update_request)

    assert response["status_code"] == 200  # ty:ignore[not-subscriptable]
    assert dispatcher.webhook_bot is engine.bots[bot_id]
    assert dispatcher.webhook_bot.token == bot_token
    assert dispatcher.webhook_update == update_request.raw.json_data


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
    bot, adapter, route_params, update_request
):
    dispatcher = DummyDispatcher()
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute(route_params),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=False,
    )

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 404, "data": {"detail": "Not found"}, "headers": None}
    assert dispatcher.webhook_update is None
    assert engine.bots == {}


@pytest.mark.asyncio
async def test_token_background_engine_rejects_request_during_shutdown_without_creating_bot_or_tracker(
    bot, adapter, update_request
):
    dispatcher = BlockingShutdownDispatcher()
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute({"bot_token": bot.token}),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=True,
    )

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))  # ty:ignore[invalid-argument-type]
    await asyncio.wait_for(dispatcher.shutdown_started.wait(), timeout=1)

    try:
        response = await engine.handle_request(update_request)
        await asyncio.sleep(0)
    finally:
        dispatcher.background_continue.set()
        dispatcher.release_shutdown.set()
        await asyncio.wait_for(shutdown_task, timeout=1)
        for tracker in engine._task_trackers.values():
            if tracker._tasks:
                await asyncio.wait_for(asyncio.gather(*tracker._tasks), timeout=1)

    assert response["status_code"] == 503  # ty:ignore[not-subscriptable]
    assert dispatcher.background_updates == []
    assert bot.id not in engine.bots
    assert bot.id not in engine._task_trackers


@pytest.mark.asyncio
async def test_token_foreground_engine_rejects_request_during_shutdown_without_creating_bot(
    bot, adapter, update_request
):
    dispatcher = BlockingShutdownDispatcher()
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute({"bot_token": bot.token}),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=False,
    )

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))  # ty:ignore[invalid-argument-type]
    await asyncio.wait_for(dispatcher.shutdown_started.wait(), timeout=1)

    try:
        response = await engine.handle_request(update_request)
    finally:
        dispatcher.release_shutdown.set()
        await asyncio.wait_for(shutdown_task, timeout=1)

    assert response["status_code"] == 503  # ty:ignore[not-subscriptable]
    assert dispatcher.foreground_updates == []
    assert bot.id not in engine.bots
