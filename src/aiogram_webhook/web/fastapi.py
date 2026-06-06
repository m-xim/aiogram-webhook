from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from typing import Any

from aiohttp import Payload
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
from starlette.types import Lifespan

from aiogram_webhook.web._starlette import AiohttpPayloadResponse
from aiogram_webhook.web.base import (
    Headers,
    LifecycleCallback,
    PathParams,
    QueryParams,
    WebAdapter,
    WebHandler,
    WebRequest,
)


class FastAPIWebRequest(WebRequest[Request]):
    __slots__ = ("_headers", "_query_params", "_request")

    def __init__(self, request: Request) -> None:
        self._request = request
        self._headers = CIMultiDictProxy(CIMultiDict(request.headers.items()))
        self._query_params = MultiDictProxy[str](MultiDict(request.query_params.multi_items()))

    @property
    def raw(self) -> Request:
        return self._request

    @property
    def client_ip(self) -> str | None:
        return self._request.client.host if self._request.client is not None else None

    async def json(self) -> dict[str, Any]:
        return await self._request.json()

    @property
    def headers(self) -> Headers:
        return self._headers

    @property
    def query_params(self) -> QueryParams:
        return self._query_params

    @property
    def path_params(self) -> PathParams:
        return self._request.path_params


class FastAPIAdapter(WebAdapter[FastAPI, Request, Response]):
    def bind_request(self, request: Request) -> WebRequest[Request]:
        return FastAPIWebRequest(request)

    @staticmethod
    def _build_lifespan(on_startup: LifecycleCallback, on_shutdown: LifecycleCallback) -> Lifespan[FastAPI]:
        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncIterator[None]:
            await on_startup(app)
            try:
                yield
            finally:
                await on_shutdown(app)

        return lifespan

    def register(
        self,
        app: FastAPI,
        path: str,
        handler: WebHandler[Request, Response],
        *,
        on_startup: LifecycleCallback,
        on_shutdown: LifecycleCallback,
    ) -> None:
        async def endpoint(request: Request) -> Response:
            return await handler(self.bind_request(request))

        router = APIRouter(lifespan=self._build_lifespan(on_startup, on_shutdown))
        router.add_api_route(path=path, endpoint=endpoint, methods=["POST"])
        app.include_router(router)

    def json_response(
        self, status_code: int, data: dict[str, str] | None = None, headers: Mapping[str, str] | None = None
    ) -> Response:
        return JSONResponse(status_code=status_code, content=data, headers=headers)

    def payload_response(
        self, status_code: int, payload: Payload, headers: Mapping[str, str] | None = None
    ) -> Response:
        return AiohttpPayloadResponse(status_code=status_code, payload=payload, headers=headers)
