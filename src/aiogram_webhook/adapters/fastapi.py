from collections.abc import Awaitable, Callable
from ipaddress import IPv4Address, IPv6Address
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from aiogram_webhook.adapters.base import BoundRequest, WebAdapter


class FastAPIBoundRequest(BoundRequest):
    request: Request

    async def json(self) -> dict[str, Any]:
        return await self.request.json()

    def header(self, name: str) -> Any | None:
        return self.request.headers.get(name)

    def query_param(self, name: str) -> Any | None:
        return self.request.query_params.get(name)

    def path_param(self, name: str) -> Any | None:
        return self.request.path_params.get(name)

    def ip(self) -> IPv4Address | IPv6Address | str | None:
        return self.request.client.host if self.request.client else None

    def json_response(self, status: int, payload: dict[str, Any]) -> JSONResponse:
        return JSONResponse(status_code=status, content=payload)


class FastApiWebAdapter(WebAdapter):
    def bind(self, request: Request) -> BoundRequest:
        return FastAPIBoundRequest(adapter=self, request=request)

    def register(self, app: Any, path: str, handler: Callable[[BoundRequest], Awaitable[Any]]) -> None:
        async def endpoint(request: Request):
            return await handler(self.bind(request))

        app.add_api_route(path, endpoint, methods=["POST"])
