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

    def _extract_ip_from_x_forwarded_for(self) -> IPv4Address | IPv6Address | str | None:
        """
        Extract client IP from X-Forwarded-For header.

        Request got through multiple proxy/load balancers
        https://github.com/aiogram/aiogram/issues/672
        """
        header_value = self.header("X-Forwarded-For")
        if not header_value:
            return None
        forwarded_for, *_ = header_value.split(",", maxsplit=1)
        return forwarded_for.strip()

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

    def ip(self) -> IPv4Address | IPv6Address | str | None:
        """Get client IP, first trying X-Forwarded-For header, then direct connection."""
        # Try to resolve client IP over reverse proxy
        if forwarded_for := self._extract_ip_from_x_forwarded_for():
            return forwarded_for

        # Get direct IP from connection (implemented by subclasses)
        return self._get_direct_ip()

    @abstractmethod
    def _get_direct_ip(self) -> IPv4Address | IPv6Address | str | None:
        """Get IP directly from client connection (implementation-specific)."""
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
    def register(
        self,
        app: Any,
        path: str,
        handler: Callable[[BoundRequest], Awaitable[Any]],
        on_startup: Callable[[], Awaitable[Any]] | None = None,
        on_shutdown: Callable[[], Awaitable[Any]] | None = None,
    ) -> None:
        raise NotImplementedError
