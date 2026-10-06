import asyncio
from unittest.mock import AsyncMock

import pytest
from aiogram.methods import SendDocument, SendMessage
from aiogram.types import BufferedInputFile

from tests.fixtures.multipart_payload import assert_attached_file, assert_payload_fields
from tests.fixtures.web_request import BlockingJsonWebRequest, DummyRequest, DummyWebRequest
from tests.fixtures.webhook_engine import DummyDispatcher, EngineProbe


@pytest.mark.asyncio
async def test_foreground_engine_returns_telegram_method_as_json_reply(bot, target, adapter, update_request):
    dispatcher = DummyDispatcher(result=SendMessage(chat_id=42, text="OK"))
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {
        "kind": "json",
        "status_code": 200,
        "data": {"method": "sendMessage", "chat_id": 42, "text": "OK"},
        "headers": None,
    }
    assert adapter.payload is None
    assert dispatcher.webhook_update == update_request.raw.json_data


@pytest.mark.asyncio
async def test_foreground_engine_returns_telegram_method_with_files_as_multipart_payload(
    bot, target, adapter, update_request
):
    method = SendDocument(chat_id=42, document=BufferedInputFile(b"hello", filename="hello.txt"))
    dispatcher = DummyDispatcher(result=method)
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)

    response = await engine.handle_request(update_request)

    assert response == {"kind": "payload", "status_code": 200, "headers": None}
    assert adapter.payload is not None
    parts = await assert_payload_fields(adapter.payload, {"method": "sendDocument", "chat_id": "42"})
    assert_attached_file(parts, field="document", filename="hello.txt", body=b"hello")


@pytest.mark.asyncio
@pytest.mark.parametrize("result", [None, {"handled": True}], ids=["empty", "non-method"])
async def test_foreground_engine_acknowledges_non_method_dispatcher_result(
    bot, target, adapter, update_request, result
):
    dispatcher = DummyDispatcher(result=result)
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
@pytest.mark.parametrize("payload", [[1, 2], 123, "text", None], ids=["list", "number", "string", "null"])
async def test_engine_returns_bad_request_when_json_payload_is_not_an_object(bot, target, adapter, dispatcher, payload):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)
    request = DummyWebRequest(DummyRequest())
    request.json = AsyncMock(return_value=payload)

    response = await engine.handle_request(request)

    assert response == {"kind": "json", "status_code": 400, "data": {"detail": "Bad request"}, "headers": None}
    assert dispatcher.webhook_update is None


@pytest.mark.asyncio
async def test_engine_rejects_inflight_request_after_shutdown(bot, target, adapter, dispatcher, update_request):
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter, handle_in_background=True)
    request = BlockingJsonWebRequest(update_request.raw)
    request_task = asyncio.create_task(engine.handle_request(request))
    await request.json_started.wait()

    await engine.on_shutdown(None)
    request.json_continue.set()
    response = await request_task
    await asyncio.sleep(0)

    assert response["status_code"] == 503
    assert dispatcher.webhook_update is None
    assert engine.task_tracker._tasks == set()


@pytest.mark.asyncio
async def test_shutdown_waits_for_admitted_request(bot, target, adapter, dispatcher, update_request):
    release = asyncio.Event()
    entered = asyncio.Event()

    async def slow_feed(**_kwargs):
        entered.set()
        await release.wait()

    dispatcher.feed_webhook_update = slow_feed
    engine = EngineProbe(dispatcher, bot, target=target, web=adapter)
    request_task = asyncio.create_task(engine.handle_request(update_request))
    await entered.wait()

    shutdown_task = asyncio.create_task(engine.on_shutdown(None))
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(asyncio.shield(shutdown_task), timeout=0.05)
    assert (await engine.handle_request(update_request))["status_code"] == 503

    release.set()
    assert (await request_task)["status_code"] == 200
    await shutdown_task
