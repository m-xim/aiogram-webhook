import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from aiogram import Bot

from aiogram_webhook.configs.bot import BotConfig
from aiogram_webhook.engines.target import Target
from aiogram_webhook.engines.token import TokenEngine
from tests.fixtures.shutdown import BlockingDispatcher, BlockingShutdownDispatcher
from tests.fixtures.web_request import BlockingJsonWebRequest, DummyRequest, DummyWebRequest
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

    assert response["status_code"] == 200
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

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))
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

    assert response["status_code"] == 503
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

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))
    await asyncio.wait_for(dispatcher.shutdown_started.wait(), timeout=1)

    try:
        response = await engine.handle_request(update_request)
    finally:
        dispatcher.release_shutdown.set()
        await asyncio.wait_for(shutdown_task, timeout=1)

    assert response["status_code"] == 503
    assert dispatcher.foreground_updates == []
    assert bot.id not in engine.bots


@pytest.mark.asyncio
async def test_token_engine_does_not_recreate_bot_or_session_when_shutdown_happens_during_body_read(
    bot_token, adapter, update_request
):
    engine = TokenEngine(
        BlockingDispatcher(),
        web=adapter,
        route=DummyRoute({"bot_token": bot_token}),  # ty:ignore[invalid-argument-type]
        handle_in_background=False,
    )
    request = BlockingJsonWebRequest(update_request.raw)
    request_task = asyncio.create_task(engine.handle_request(request))
    await asyncio.wait_for(request.json_started.wait(), timeout=1)

    await engine.on_shutdown(None)
    assert engine._session is None

    request.json_continue.set()
    response = await asyncio.wait_for(request_task, timeout=1)

    assert response["status_code"] == 503
    assert engine.bots == {}
    assert engine._session is None


@pytest.mark.asyncio
async def test_token_engine_does_not_create_bot_when_json_is_invalid(bot, bot_token, adapter):
    dispatcher = DummyDispatcher()
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute({"bot_token": bot_token}),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=False,
    )

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_error=ValueError("invalid json"))))

    assert response["status_code"] == 400
    assert engine.bots == {}


@pytest.mark.asyncio
async def test_token_engine_does_not_create_bot_when_json_is_not_an_object(bot, bot_token, adapter):
    dispatcher = DummyDispatcher()
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute({"bot_token": bot_token}),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=False,
    )
    request = DummyWebRequest(DummyRequest())
    request.json = AsyncMock(return_value=[1, 2])

    response = await engine.handle_request(request)

    assert response["status_code"] == 400
    assert engine.bots == {}


@pytest.mark.asyncio
async def test_token_engine_remove_bot_returns_false_for_unknown_bot(bot, adapter):
    engine = TokenEngine(
        DummyDispatcher(),
        web=adapter,
        route=DummyRoute(),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
    )

    assert await engine.remove_bot(bot.id, delete_webhook=False) is False


@pytest.mark.asyncio
async def test_token_engine_remove_bot_rejects_drop_pending_updates_without_delete_webhook(bot, bot_token, adapter):
    engine = TokenEngine(
        DummyDispatcher(),
        web=adapter,
        route=DummyRoute(),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
    )
    await engine._resolve_bot(Target(bot_id=bot.id, bot_token=bot_token))

    with (
        patch.object(Bot, "delete_webhook", new=AsyncMock()) as delete_webhook,
        pytest.raises(ValueError, match="drop_pending_updates"),
    ):
        await engine.remove_bot(bot.id, delete_webhook=False, drop_pending_updates=True)

    delete_webhook.assert_not_awaited()
    assert bot.id in engine.bots


@pytest.mark.asyncio
async def test_token_engine_remove_bot_deletes_webhook_and_cleans_up(bot, bot_token, adapter):
    engine = TokenEngine(
        DummyDispatcher(),
        web=adapter,
        route=DummyRoute(),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
    )
    resolved = await engine._resolve_bot(Target(bot_id=bot.id, bot_token=bot_token))
    engine._get_task_tracker(resolved)

    with patch.object(Bot, "delete_webhook", new=AsyncMock()) as delete_webhook:
        assert await engine.remove_bot(bot.id, delete_webhook=True, drop_pending_updates=True) is True

    delete_webhook.assert_awaited_once_with(drop_pending_updates=True)
    assert engine.bots == {}
    assert engine._task_trackers == {}


@pytest.mark.asyncio
async def test_token_engine_remove_bot_keeps_state_when_delete_webhook_fails(bot, bot_token, adapter):
    engine = TokenEngine(
        DummyDispatcher(),
        web=adapter,
        route=DummyRoute(),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
    )
    resolved = await engine._resolve_bot(Target(bot_id=bot.id, bot_token=bot_token))
    tracker = engine._get_task_tracker(resolved)

    with (
        patch.object(Bot, "delete_webhook", new=AsyncMock(side_effect=RuntimeError("boom"))),
        pytest.raises(RuntimeError),
    ):
        await engine.remove_bot(bot.id, delete_webhook=True)

    assert engine.bots[bot.id] is resolved
    assert engine._task_trackers[bot.id] is tracker


@pytest.mark.asyncio
async def test_token_engine_remove_bot_drains_tasks_without_leaking_new_ones_into_closing_tracker(
    bot, bot_token, adapter, update_request
):
    engine = TokenEngine(
        DummyDispatcher(),
        web=adapter,
        route=DummyRoute({"bot_token": bot_token}),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
        handle_in_background=True,
    )
    resolved = await engine._resolve_bot(Target(bot_id=bot.id, bot_token=bot_token))
    old_tracker = engine._get_task_tracker(resolved)
    release = asyncio.Event()
    running = old_tracker.spawn(release.wait())

    remove_task = asyncio.create_task(engine.remove_bot(bot.id, delete_webhook=False))
    await asyncio.sleep(0)  # remove_bot is now draining the old tracker

    assert not remove_task.done()
    assert engine.bots == {}
    assert engine._task_trackers == {}

    # A request arriving mid-drain must get a fresh bot/tracker, never the one being closed.
    response = await engine.handle_request(update_request)
    new_tracker = engine._task_trackers[bot.id]

    assert response["status_code"] == 200
    assert new_tracker is not old_tracker
    assert old_tracker._tasks == {running}

    release.set()
    assert await asyncio.wait_for(remove_task, timeout=1) is True
    assert running.done()
    await new_tracker.close()


@pytest.mark.asyncio
async def test_token_engine_startup_merges_extra_bots_with_known_bots(bot, bot_token, adapter):
    dispatcher = SimpleNamespace(workflow_data={}, emit_startup=AsyncMock(), emit_shutdown=AsyncMock())
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute(),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
    )
    known = await engine._resolve_bot(Target(bot_id=bot.id, bot_token=bot_token))
    extra = Bot("7:EXTRA")

    await engine.on_startup(None, bots=[extra])

    assert dispatcher.emit_startup.await_args.kwargs["bots"] == {known, extra}


@pytest.mark.asyncio
async def test_token_engine_shutdown_merges_extra_bots_with_known_bots(bot, bot_token, adapter):
    dispatcher = SimpleNamespace(workflow_data={}, emit_startup=AsyncMock(), emit_shutdown=AsyncMock())
    engine = TokenEngine(
        dispatcher,
        web=adapter,
        route=DummyRoute(),  # ty:ignore[invalid-argument-type]
        bot_config=BotConfig(session=bot.session),
    )
    known = await engine._resolve_bot(Target(bot_id=bot.id, bot_token=bot_token))
    extra = Bot("7:EXTRA")

    await engine.on_shutdown(None, bots=[extra])

    assert dispatcher.emit_shutdown.await_args.kwargs["bots"] == {known, extra}
