from collections.abc import Iterable, Mapping
from typing import Any

from multidict import CIMultiDict, MultiDict

from tests.fixtures.fixtures_checks import ConditionalCheck, FailingCheck, PassingCheck


class DummyRequest:
    def __init__(
        self,
        *,
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | Iterable[tuple[str, Any]] | None = None,
        headers: Mapping[str, str | None] | None = None,
        ip: str | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> None:
        self.path_params = dict(path_params or {})
        self.query: Mapping[str, Any] | Iterable[tuple[str, Any]] = query or {}
        self.headers = dict(headers or {})
        self.ip = ip
        self.json_data = json_data or {}


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
        return self._request.json_data

    @property
    def headers(self):
        # Normalize dict to CIMultiDict for headers
        return CIMultiDict(self._request.headers.items())

    @property
    def query_params(self):
        return MultiDict(self._request.query)

    def _get_query_values(self, name: str) -> list[str]:
        query = self._request.query
        if isinstance(query, Mapping):
            for key, value in query.items():
                if key != name:
                    continue
                if isinstance(value, list | tuple):
                    return [str(item) for item in value]
                return [str(value)]
            return []

        return [str(value) for key, value in query if key == name]

    def _get_query_names(self) -> tuple[str, ...]:
        query = self._request.query
        if isinstance(query, Mapping):
            return tuple(str(key) for key in query)

        return tuple(str(key) for key, _ in query)

    @property
    def path_params(self):
        return self._request.path_params


def dummy_web_request(request: DummyRequest | None = None) -> DummyWebRequest:
    return DummyWebRequest(request)


__all__ = (
    "ConditionalCheck",
    "DummyRequest",
    "DummyWebRequest",
    "FailingCheck",
    "PassingCheck",
    "dummy_web_request",
)
