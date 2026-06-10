import asyncio
from typing import Any

import pytest
from aiogram import Bot
from aiogram.methods import SendMessage

from aiogram_webhook.engines.base import BaseWebhookEngine
from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.tasks import TaskTracker
from tests.fixtures.web_request import DummyRequest, DummyWebRequest
from tests.fixtures.webhook_engine import CapturingAdapter, DummyDispatcher, DummyRoute


class EngineProbe(BaseWebhookEngine[Any, Any, dict[str, Any]]):
    def __init__(
        self,
        dispatcher: DummyDispatcher,
        bot: Bot | None,
        *,
        target: Target | None,
        web: CapturingAdapter,
        handle_in_background: bool = False,
    ) -> None:
        self.bot = bot
        self.target = target
        self.task_tracker = TaskTracker()

        super().__init__(
            dispatcher,  # ty:ignore[invalid-argument-type]
            web=web,
            route=DummyRoute({"bot_token": "42:TEST"}),  # ty:ignore[invalid-argument-type]
            handle_in_background=handle_in_background,
        )

    async def _on_startup(self, _app: Any, *args: Any, **kwargs: Any) -> None:
        return None

    async def _on_shutdown(self, _app: Any, *args: Any, **kwargs: Any) -> None:
        return None

    async def _resolve_target(self, request: Any, route_params: RouteParams) -> Target | None:
        return self.target

    async def _resolve_bot(self, target: Target) -> Bot | None:
        return self.bot

    def _get_task_tracker(self, bot: Bot) -> TaskTracker:
        return self.task_tracker


@pytest.mark.asyncio
async def test_foreground_engine_returns_telegram_method_as_webhook_payload(bot, target, adapter, update_request):
    dispatcher = DummyDispatcher(result=SendMessage(chat_id=42, text="OK"))
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "payload", "status_code": 200, "headers": None}
    assert adapter.payload is not None
    assert dispatcher.webhook_update == update_request.raw.json_data


@pytest.mark.asyncio
async def test_foreground_engine_acknowledges_empty_dispatcher_result(bot, target, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 200, "data": {}, "headers": None}
    assert adapter.payload is None


@pytest.mark.asyncio
async def test_foreground_engine_acknowledges_non_method_dispatcher_result(bot, target, adapter, update_request):
    dispatcher = DummyDispatcher(result={"handled": True})
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 200, "data": {}, "headers": None}
    assert adapter.payload is None


@pytest.mark.asyncio
async def test_background_engine_acknowledges_without_webhook_payload(bot, target, adapter, update_request):
    dispatcher = DummyDispatcher(result=SendMessage(chat_id=42, text="OK"))
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter, handle_in_background=True)

    response = await engine.handle_request(update_request)
    await asyncio.sleep(0)

    assert response == {"kind": "json", "status_code": 200, "data": {}, "headers": None}
    assert dispatcher.webhook_update == update_request.raw.json_data
    assert adapter.payload is None


@pytest.mark.asyncio
async def test_engine_stops_accepting_requests_after_shutdown_starts(bot, target, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)
    await engine.on_shutdown(None)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 503, "data": {"detail": "Service unavailable"}, "headers": None}
    assert dispatcher.webhook_update is None


@pytest.mark.asyncio
async def test_engine_accepts_requests_again_after_startup(bot, target, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)
    await engine.on_shutdown(None)
    await engine.on_startup(None)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 200, "data": {}, "headers": None}
    assert dispatcher.webhook_update == update_request.raw.json_data


@pytest.mark.asyncio
async def test_engine_returns_not_found_when_target_cannot_be_resolved(bot, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot, target=None, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 404, "data": {"detail": "Not found"}, "headers": None}
    assert dispatcher.webhook_update is None


@pytest.mark.asyncio
async def test_engine_returns_not_found_when_bot_cannot_be_resolved(target, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot=None, target=target, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "json", "status_code": 404, "data": {"detail": "Not found"}, "headers": None}
    assert dispatcher.webhook_update is None


@pytest.mark.asyncio
async def test_engine_returns_bad_request_when_json_payload_is_invalid(bot, target, adapter, dispatcher):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    response = await engine.handle_request(DummyWebRequest(DummyRequest(json_error=ValueError("invalid json"))))

    assert response == {"kind": "json", "status_code": 400, "data": {"detail": "Bad request"}, "headers": None}
    assert dispatcher.webhook_update is None


@pytest.mark.asyncio
async def test_engine_lifespan_runs_startup_then_shutdown(bot, target, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    await engine.on_startup(None)
    assert not engine._is_shutting_down
    response = await engine.handle_request(update_request)
    assert response["status_code"] == 200
    await engine.on_shutdown(None)

    assert engine._is_shutting_down
    response = await engine.handle_request(update_request)
    assert response["status_code"] == 503
