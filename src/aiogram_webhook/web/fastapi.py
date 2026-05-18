from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy

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

    def register(
        self,
        app: FastAPI,
        path: str,
        handler: WebHandler[Request, Response],
        *,
        on_startup: LifecycleCallback,  # noqa: ARG002
        on_shutdown: LifecycleCallback,  # noqa: ARG002
    ) -> None:
        async def endpoint(request: Request) -> Response:
            return await handler(self.bind_request(request))

        app.add_api_route(path=path, endpoint=endpoint, methods=["POST"])

    def json_response(
        self, status_code: int, data: Mapping[str, str] | None = None, headers: Mapping[str, str] | None = None
    ) -> Response:
        return JSONResponse(status_code=status_code, content=data, headers=headers)
