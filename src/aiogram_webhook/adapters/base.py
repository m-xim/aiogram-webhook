from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from ipaddress import IPv4Address, IPv6Address


@dataclass(slots=True)
class BoundRequest(ABC):
    """
    Abstract base class for a request bound to a web adapter.

    Provides interface for extracting data from incoming requests and generating responses.
    """

    request: Any
    adapter: WebAdapter

    @abstractmethod
    async def json(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def header(self, name: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    def query_param(self, name: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    def path_param(self, name: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    def ip(self) -> IPv4Address | IPv6Address | str | None:
        raise NotImplementedError

    def secret_token(self) -> str | None:
        return self.header(self.adapter.secret_header)

    @abstractmethod
    def json_response(self, status: int, payload: dict[str, Any]) -> Any:
        raise NotImplementedError


@dataclass
class WebAdapter(ABC):
    """
    Abstract base class for web framework adapters.

    Provides interface for binding requests and registering webhook handlers.
    """

    secret_header: str = "x-telegram-bot-api-secret-token"  # noqa: S105

    @abstractmethod
    def bind(self, request: Any) -> BoundRequest:
        raise NotImplementedError

    @abstractmethod
    def register(self, app: Any, path: str, handler: Callable[[BoundRequest], Awaitable[Any]]) -> None:
        raise NotImplementedError
