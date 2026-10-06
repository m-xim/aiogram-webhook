import pytest
from aiogram.methods import SendDocument, SendMessage
from aiogram.types import BufferedInputFile
from fastapi import FastAPI
from fastapi.testclient import TestClient

from aiogram_webhook.route import Route
from aiogram_webhook.utils._payload import build_multipart_payload, prepare_webhook_reply
from aiogram_webhook.web.fastapi import FastAPIAdapter
from tests.fixtures.multipart_payload import assert_attached_file, assert_multipart_fields
from tests.fixtures.webhook_engine import DummyDispatcher, EngineProbe


@pytest.fixture
def fastapi_adapter() -> FastAPIAdapter:
    return FastAPIAdapter()


@pytest.fixture
def app() -> FastAPI:
    return FastAPI()


def test_fastapi_adapter_passes_bound_request_to_registered_post_handler(fastapi_adapter, app):
    seen = {}

    async def handler(request):
        seen["raw"] = request.raw
        seen["client_ip"] = request.client_ip
        seen["header"] = request.headers["X-Test"]
        seen["query"] = request.query_params.getall("tag")
        seen["path"] = request.path_params["bot_token"]
        seen["json"] = await request.json()

        return fastapi_adapter.json_response(
            status_code=202,
            data={"ok": "yes"},
            headers={"X-Reply": "done"},
        )

    async def on_startup(_app):
        return None

    async def on_shutdown(_app):
        return None

    fastapi_adapter.register(app, "/webhook/{bot_token}", handler, on_startup=on_startup, on_shutdown=on_shutdown)

    with TestClient(app) as client:
        response = client.post(
            "/webhook/42:TEST?tag=first&tag=second",
            json={"update_id": 1},
            headers={"X-Test": "yes"},
        )

    assert response.status_code == 202
    assert response.headers["X-Reply"] == "done"
    assert response.json() == {"ok": "yes"}
    assert seen["raw"].path_params == {"bot_token": "42:TEST"}
    assert seen["client_ip"] == "testclient"
    assert seen["header"] == "yes"
    assert seen["query"] == ["first", "second"]
    assert seen["path"] == "42:TEST"
    assert seen["json"] == {"update_id": 1}


def test_fastapi_adapter_registers_lifecycle_callbacks_via_router(bot, target, fastapi_adapter, app):
    events = []

    engine = EngineProbe(
        DummyDispatcher(),
        web=fastapi_adapter,
        route=Route(base_url="https://example.com", path="/webhook"),
        handle_in_background=False,
        bot=bot,
        target=target,
        events=events,
    )

    engine.register(app)

    with TestClient(app) as client:
        assert events == [("engine_startup", app)]
        response = client.post("/webhook", json={"update_id": 1})

    assert response.status_code == 200
    assert response.json() == {}
    assert events == [("engine_startup", app), ("engine_shutdown", app)]


def test_fastapi_adapter_streams_webhook_method_payload_as_multipart(bot, fastapi_adapter, app):

    @app.post("/webhook")
    async def webhook():
        method = SendMessage(chat_id=42, text="OK", disable_notification=False)
        data, files = prepare_webhook_reply(bot, method)
        return fastapi_adapter.payload_response(status_code=200, payload=build_multipart_payload(bot, data, files))

    with TestClient(app) as client:
        response = client.post("/webhook")

    assert response.status_code == 200
    assert int(response.headers["content-length"]) == len(response.content)
    assert_multipart_fields(
        response.headers["content-type"],
        response.content,
        {
            "method": "sendMessage",
            "chat_id": "42",
            "text": "OK",
            "disable_notification": "false",
        },
    )


def test_fastapi_adapter_streams_webhook_payload_with_attached_file(bot, fastapi_adapter, app):

    @app.post("/webhook")
    async def webhook():
        method = SendDocument(
            chat_id=42,
            document=BufferedInputFile(b"hello", filename="hello.txt"),
        )
        data, files = prepare_webhook_reply(bot, method)
        return fastapi_adapter.payload_response(status_code=200, payload=build_multipart_payload(bot, data, files))

    with TestClient(app) as client:
        response = client.post("/webhook")

    assert response.status_code == 200
    assert "content-length" not in response.headers  # payload.size is None for file attachments
    parts = assert_multipart_fields(
        response.headers["content-type"],
        response.content,
        {"method": "sendDocument", "chat_id": "42"},
    )

    assert_attached_file(parts, field="document", filename="hello.txt", body=b"hello")
