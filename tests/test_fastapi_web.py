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

    adapter.register(
        app,
        "/webhook/{bot_token}",
        handler,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )

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
