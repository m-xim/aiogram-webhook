from ipaddress import IPv4Address, IPv6Address
from typing import TYPE_CHECKING, Any, cast

from aiohttp.web import Application, Request
from aiohttp.web_response import Response, json_response

from aiogram_webhook.adapters.base import BoundRequest, WebAdapter

if TYPE_CHECKING:
    from asyncio import Transport


class AiohttpBoundRequest(BoundRequest):
    adapter: "AiohttpWebAdapter"
    request: Request

    async def json(self) -> dict[str, Any]:
        return await self.request.json()

    def header(self, name: str) -> Any | None:
        return self.request.headers.get(name)

    def query_param(self, name: str) -> Any | None:
        return self.request.query.get(name)

    def path_param(self, name: str) -> Any | None:
        return self.request.match_info.get(name)

    def ip(self) -> IPv4Address | IPv6Address | str | None:
        if peer_name := cast("Transport", self.request.transport).get_extra_info("peername"):
            return peer_name[0]
        return None

    def json_response(self, status: int, payload: dict[str, Any]) -> Response:
        return json_response(status=status, data=payload)


class AiohttpWebAdapter(WebAdapter):
    def bind(self, request: Request) -> AiohttpBoundRequest:
        return AiohttpBoundRequest(adapter=self, request=request)

    def register(self, app: Application, path, handler, on_startup=None, on_shutdown=None) -> None:
        async def endpoint(request: Request):
            return await handler(self.bind(request))

        app.router.add_route(method="POST", path=path, handler=endpoint)
        if on_startup is not None:
            app.on_startup.append(on_startup)
        if on_shutdown is not None:
            app.on_shutdown.append(on_shutdown)
