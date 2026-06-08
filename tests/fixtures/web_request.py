from collections.abc import Mapping
from typing import Any

from multidict import CIMultiDict, MultiDict


class DummyRequest:
    def __init__(
        self,
        *,
        path_params: Mapping[str, Any] | None = None,
        query: MultiDict[str] | None = None,
        headers: Mapping[str, str | None] | None = None,
        ip: str | None = None,
        json_data: dict[str, Any] | None = None,
        json_error: ValueError | None = None,
    ) -> None:
        self.path_params = dict(path_params or {})
        self.query: MultiDict[str] = query or MultiDict()
        self.headers = dict(headers or {})
        self.ip = ip
        self.json_data = json_data or {}
        self.json_error = json_error


class DummyWebRequest:
    def __init__(self, request: DummyRequest | None = None) -> None:
        self._request = request or DummyRequest()

    @property
    def raw(self) -> DummyRequest:
        return self._request

    @property
    def client_ip(self) -> str | None:
        return self._request.ip

    async def json(self) -> dict[str, Any]:
        if self._request.json_error is not None:
            raise self._request.json_error

        return self._request.json_data

    @property
    def headers(self):
        return CIMultiDict(self._request.headers.items())

    @property
    def query_params(self):
        return self._request.query

    @property
    def path_params(self):
        return self._request.path_params
