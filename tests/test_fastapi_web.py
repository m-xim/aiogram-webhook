from contextlib import asynccontextmanager

from aiogram.methods import SendDocument, SendMessage
from aiogram.types import BufferedInputFile
from fastapi import FastAPI
from fastapi.testclient import TestClient

from aiogram_webhook.utils._payload import build_webhook_payload
from aiogram_webhook.web.fastapi import FastAPIAdapter
from tests.fixtures.multipart_payload import assert_attached_file, assert_multipart_fields


def test_fastapi_adapter_passes_bound_request_to_registered_post_handler():
    adapter = FastAPIAdapter()
    app = FastAPI()
    seen = {}

    async def handler(request):
        seen["raw"] = request.raw
        seen["client_ip"] = request.client_ip
        seen["header"] = request.headers["X-Test"]
        seen["query"] = request.query_params.getall("tag")
        seen["path"] = request.path_params["bot_token"]
        seen["json"] = await request.json()

        return adapter.json_response(
            status_code=202,
            data={"ok": "yes"},
            headers={"X-Reply": "done"},
        )

    async def on_startup(_app):
        return None

    async def on_shutdown(_app):
        return None

    adapter.register(app, "/webhook/{bot_token}", handler, on_startup=on_startup, on_shutdown=on_shutdown)

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


def test_fastapi_adapter_registers_lifecycle_callbacks_with_app_lifespan():
    adapter = FastAPIAdapter()
    events = []

    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        events.append(("app_startup", app))
        try:
            yield
        finally:
            events.append(("app_shutdown", app))

    app = FastAPI(lifespan=app_lifespan)

    async def handler(_request):
        return adapter.json_response(status_code=200, data={"ok": "yes"})

    async def on_startup(app: FastAPI):
        events.append(("adapter_startup", app))

    async def on_shutdown(app: FastAPI):
        events.append(("adapter_shutdown", app))

    adapter.register(app, "/webhook", handler, on_startup=on_startup, on_shutdown=on_shutdown)

    with TestClient(app) as client:
        assert events == [("app_startup", app), ("adapter_startup", app)]
        response = client.post("/webhook", json={"update_id": 1})

    assert response.status_code == 200
    assert response.json() == {"ok": "yes"}
    assert events == [
        ("app_startup", app),
        ("adapter_startup", app),
        ("adapter_shutdown", app),
        ("app_shutdown", app),
    ]


def test_fastapi_adapter_composes_lifecycle_callbacks_for_multiple_registrations():
    adapter = FastAPIAdapter()
    app = FastAPI()
    events = []

    async def first_handler(_request):
        return adapter.json_response(status_code=200, data={"handler": "first"})

    async def second_handler(_request):
        return adapter.json_response(status_code=200, data={"handler": "second"})

    async def first_startup(_app):
        events.append("first_startup")

    async def first_shutdown(_app):
        events.append("first_shutdown")

    async def second_startup(_app):
        events.append("second_startup")

    async def second_shutdown(_app):
        events.append("second_shutdown")

    adapter.register(app, "/first", first_handler, on_startup=first_startup, on_shutdown=first_shutdown)
    adapter.register(app, "/second", second_handler, on_startup=second_startup, on_shutdown=second_shutdown)

    with TestClient(app) as client:
        assert events == ["first_startup", "second_startup"]
        first_response = client.post("/first", json={"update_id": 1})
        second_response = client.post("/second", json={"update_id": 2})

    assert first_response.json() == {"handler": "first"}
    assert second_response.json() == {"handler": "second"}
    assert events == ["first_startup", "second_startup", "second_shutdown", "first_shutdown"]


def test_fastapi_adapter_streams_webhook_method_payload_as_multipart(bot):
    adapter = FastAPIAdapter()
    app = FastAPI()

    @app.post("/webhook")
    async def webhook():
        method = SendMessage(chat_id=42, text="OK", disable_notification=False)
        return adapter.payload_response(status_code=200, payload=build_webhook_payload(bot=bot, method=method))

    with TestClient(app) as client:
        response = client.post("/webhook")

    assert response.status_code == 200
    assert "content-length" not in response.headers
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


def test_fastapi_adapter_streams_webhook_payload_with_attached_file(bot):
    adapter = FastAPIAdapter()
    app = FastAPI()

    @app.post("/webhook")
    async def webhook():
        method = SendDocument(
            chat_id=42,
            document=BufferedInputFile(b"hello", filename="hello.txt"),
        )
        return adapter.payload_response(status_code=200, payload=build_webhook_payload(bot=bot, method=method))

    with TestClient(app) as client:
        response = client.post("/webhook")

    assert response.status_code == 200
    assert "content-length" not in response.headers
    parts = assert_multipart_fields(
        response.headers["content-type"],
        response.content,
        {"method": "sendDocument", "chat_id": "42"},
    )

    assert_attached_file(parts, field="document", filename="hello.txt", body=b"hello")
