from collections.abc import Mapping
from typing import Any

from aiogram_webhook.route import Route
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.web.base import WebAdapter


class DummyRoute(Route):
    path = "/webhook"

    def __init__(self, route_params: Mapping[str, str] | None = None) -> None:
        self.route_params = dict(route_params or {})

    async def match(self, request) -> RouteParams:
        return self.route_params


class CapturingAdapter(WebAdapter):
    def __init__(self) -> None:
        self.payload = None

    def bind_request(self, request):
        raise NotImplementedError

    def register(self, app, path, handler, *, on_startup, on_shutdown) -> None:
        raise NotImplementedError

    def json_response(
        self,
        status_code: int,
        data: dict[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ):
        return {"kind": "json", "status_code": status_code, "data": data, "headers": headers}

    def payload_response(self, status_code: int, payload, headers=None):
        self.payload = payload
        return {"kind": "payload", "status_code": status_code, "headers": headers}


class DummyDispatcher:
    def __init__(self, result: Any = None) -> None:
        self.workflow_data = {}
        self.result = result
        self.webhook_bot = None
        self.webhook_update = None

    async def feed_webhook_update(self, bot, update):
        self.webhook_bot = bot
        self.webhook_update = update
        return self.result

    async def feed_raw_update(self, bot, update):
        self.webhook_bot = bot
        self.webhook_update = update
        return self.result

    async def silent_call_request(self, bot, result):
        return None
