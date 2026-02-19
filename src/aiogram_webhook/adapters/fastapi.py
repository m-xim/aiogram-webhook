from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
from aiogram_webhook.security.checks.ip import IPAddress


class FastAPIBoundRequest(BoundRequest[Request]):
    async def json(self) -> dict[str, Any]:
        return await self.request.json()

    def header(self, name: str) -> Any | None:
        return self.request.headers.get(name)

    def query_param(self, name: str) -> Any | None:
        return self.request.query_params.get(name)

    def path_param(self, name: str) -> Any | None:
        return self.request.path_params.get(name)

    def ip(self) -> IPAddress | str | None:
        if self.request.client:
            return self.request.client.host
        return None


class FastApiWebAdapter(WebAdapter):
    def bind(self, request: Request) -> FastAPIBoundRequest:
        return FastAPIBoundRequest(request=request)

    def register(self, app: FastAPI, path, handler, on_startup=None, on_shutdown=None) -> None:  # noqa: ARG002
        async def endpoint(request: Request):
            return await handler(self.bind(request))

        app.add_api_route(path=path, endpoint=endpoint, methods=["POST"])

    def create_json_response(self, status: int, payload: dict[str, Any]) -> JSONResponse:
        return JSONResponse(status_code=status, content=payload)
