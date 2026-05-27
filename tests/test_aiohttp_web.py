import json
from unittest.mock import Mock

from aiogram.methods import SendMessage
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import Application

from aiogram_webhook.utils._payload import build_webhook_payload
from aiogram_webhook.web.aiohttp import AiohttpAdapter


def test_aiohttp_adapter_exposes_framework_request_data():
    transport = Mock()
    transport.get_extra_info.return_value = ("127.0.0.1", 12345)
    raw_request = make_mocked_request(
        "POST",
        "/webhook/42:TEST?tag=first&tag=second",
        headers={"X-Test": "yes"},
        match_info={"bot_token": "42:TEST"},
        transport=transport,
    )

    request = AiohttpAdapter().bind_request(raw_request)

    assert request.raw is raw_request
    assert request.client_ip == "127.0.0.1"
    assert request.headers["X-Test"] == "yes"
    assert request.query_params.getall("tag") == ["first", "second"]
    assert request.path_params["bot_token"] == "42:TEST"


def test_aiohttp_adapter_registers_post_route_and_lifecycle_callbacks():
    adapter = AiohttpAdapter()
    app = Application()

    async def handler(_request):
        return adapter.json_response(status_code=200, data={"ok": "yes"})

    async def on_startup(_app):
        return None

    async def on_shutdown(_app):
        return None

    adapter.register(
        app,
        "/webhook",
        handler,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )

    routes = list(app.router.routes())
    assert len(routes) == 1
    assert routes[0].method == "POST"
    assert routes[0].resource is not None
    assert routes[0].resource.canonical == "/webhook"
    assert app.on_startup[-1] is on_startup
    assert app.on_shutdown[-1] is on_shutdown


def test_aiohttp_adapter_builds_json_response_with_status_and_headers():
    response = AiohttpAdapter().json_response(
        status_code=418,
        data={"detail": "teapot"},
        headers={"X-Test": "yes"},
    )

    assert response.status == 418
    assert response.headers["X-Test"] == "yes"
    assert response.content_type == "application/json"
    assert response.text is not None
    assert json.loads(response.text) == {"detail": "teapot"}


def test_aiohttp_adapter_builds_multipart_payload_response(bot):
    method = SendMessage(chat_id=42, text="OK")
    payload = build_webhook_payload(bot=bot, method=method)

    response = AiohttpAdapter().payload_response(
        status_code=201,
        payload=payload,
        headers={"X-Test": "yes"},
    )

    assert response.status == 201
    assert response.headers["X-Test"] == "yes"
    assert response.body is payload
    assert response.content_type == "multipart/form-data"
