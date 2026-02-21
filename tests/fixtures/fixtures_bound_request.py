from typing import Any

from aiogram_webhook.adapters.base_adapter import BoundRequest, WebAdapter


class DummyAdapter(WebAdapter):
    def bind(self, request):
        raise NotImplementedError("DummyAdapter.bind is not implemented")

    def register(self, app, path, handler, on_startup=None, on_shutdown=None):
        raise NotImplementedError("DummyAdapter.register is not implemented")

    def create_json_response(self, status, payload):
        return status, payload


class DummyRequest:
    def __init__(self, *, path_params=None, query_params=None, headers=None, ip=None):
        self.path_params = path_params or {}
        self.query_params = query_params or {}
        self.headers = headers or {}
        self.ip = ip


class DummyBoundRequest(BoundRequest[DummyRequest]):
    def __init__(self, request: DummyRequest | None = None):
        super().__init__(request or DummyRequest())

    async def json(self) -> dict[str, Any]:
        return {}

    @property
    def client_ip(self) -> str | None:
        return self.request.ip

    @property
    def headers(self):
        return self.request.headers

    @property
    def query_params(self):
        return self.request.query_params

    @property
    def path_params(self):
        return self.request.path_params
