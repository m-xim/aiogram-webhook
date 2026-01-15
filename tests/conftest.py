from aiogram_webhook.adapters.base import BoundRequest, WebAdapter


class DummyAdapter(WebAdapter):
    secret_header = "x-telegram-bot-api-secret-token"

    def bind(self, request):
        raise NotImplementedError

    def register(self, app, path, handler, on_startup=None, on_shutdown=None):
        raise NotImplementedError


class DummyBoundRequest(BoundRequest):
    def __init__(self, path_params=None, query_params=None, secret_token=None, ip=None):
        super().__init__(request=None, adapter=DummyAdapter())
        self._path_params = path_params or {}
        self._query_params = query_params or {}
        self._secret_token = secret_token
        self._ip = ip

    async def json(self):
        return {}

    def header(self, name):
        if name == self.adapter.secret_header:
            return self._secret_token
        return None

    def query_param(self, name):
        return self._query_params.get(name)

    def path_param(self, name):
        return self._path_params.get(name)

    def ip(self):
        return self._ip

    def json_response(self, status, payload):
        return status, payload
