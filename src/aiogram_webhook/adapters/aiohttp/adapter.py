from typing import TYPE_CHECKING, Any, cast

from aiohttp.web import Application, Request
from aiohttp.web_response import Response, json_response

from aiogram_webhook.adapters.aiohttp.mapping import AiohttpHeadersMapping, AiohttpQueryMapping
from aiogram_webhook.adapters.base_adapter import BoundRequest, WebAdapter

if TYPE_CHECKING:
    from asyncio import Transport


class AiohttpBoundRequest(BoundRequest[Request]):
    def __init__(self, request: Request):
        super().__init__(request)
        self._headers = AiohttpHeadersMapping(self.request.headers)
        self._query_params = AiohttpQueryMapping(self.request.query)

    async def json(self):
        return await self.request.json()

    @property
    def client_ip(self):
        if peer_name := cast("Transport", self.request.transport).get_extra_info("peername"):
            return peer_name[0]
        return None

    @property
    def headers(self) -> AiohttpHeadersMapping:
        return self._headers

    @property
    def query_params(self) -> AiohttpQueryMapping:
        return self._query_params

    @property
    def path_params(self):
        return self.request.match_info


class AiohttpWebAdapter(WebAdapter):
    def bind(self, request: Request) -> AiohttpBoundRequest:
        return AiohttpBoundRequest(request=request)

    def register(self, app: Application, path, handler, on_startup=None, on_shutdown=None) -> None:
        async def endpoint(request: Request):
            return await handler(self.bind(request))

        app.router.add_route(method="POST", path=path, handler=endpoint)
        if on_startup is not None:
            app.on_startup.append(on_startup)
        if on_shutdown is not None:
            app.on_shutdown.append(on_shutdown)

    def create_json_response(self, status: int, payload: dict[str, Any]) -> Response:
        return json_response(status=status, data=payload)
