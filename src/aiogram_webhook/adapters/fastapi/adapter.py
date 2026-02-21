from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiogram_webhook.adapters.base_adapter import BoundRequest, WebAdapter
from aiogram_webhook.adapters.fastapi.mapping import FastAPIHeadersMapping, FastAPIQueryMapping


class FastAPIBoundRequest(BoundRequest[Request]):
    def __init__(self, request: Request):
        super().__init__(request)
        self._headers = FastAPIHeadersMapping(self.request.headers)
        self._query_params = FastAPIQueryMapping(self.request.query_params)

    async def json(self) -> dict[str, Any]:
        return await self.request.json()

    @property
    def client_ip(self):
        if self.request.client:
            return self.request.client.host
        return None

    @property
    def headers(self) -> FastAPIHeadersMapping:
        return self._headers

    @property
    def query_params(self) -> FastAPIQueryMapping:
        return self._query_params

    @property
    def path_params(self):
        return self.request.path_params


class FastApiWebAdapter(WebAdapter):
    def bind(self, request: Request) -> FastAPIBoundRequest:
        return FastAPIBoundRequest(request=request)

    def register(self, app: FastAPI, path, handler, on_startup=None, on_shutdown=None) -> None:  # noqa: ARG002
        async def endpoint(request: Request):
            return await handler(self.bind(request))

        app.add_api_route(path=path, endpoint=endpoint, methods=["POST"])

    def create_json_response(self, status: int, payload: dict[str, Any]) -> JSONResponse:
        return JSONResponse(status_code=status, content=payload)
