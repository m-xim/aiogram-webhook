from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram_webhook.security.checks.ip import IPAddress


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
        """Parse the request body as JSON and return the resulting dictionary."""
        raise NotImplementedError

    @abstractmethod
    def header(self, name: str) -> Any | None:
        """Get a header value from the request."""
        raise NotImplementedError

    @abstractmethod
    def query_param(self, name: str) -> Any | None:
        """Get a query parameter from the request URL."""
        raise NotImplementedError

    @abstractmethod
    def path_param(self, name: str) -> Any | None:
        """Get a path parameter from the request URL."""
        raise NotImplementedError

    @abstractmethod
    def ip(self) -> IPAddress | str | None:
        """Get IP directly from client connection (implementation-specific)."""
        raise NotImplementedError

    def secret_token(self) -> str | None:
        """Get the secret token from the request header."""
        return self.header(self.adapter.secret_header)

    @abstractmethod
    def json_response(self, status: int, payload: dict[str, Any]) -> Any:
        """Create a JSON response with the given status and payload."""
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
        """Bind a request to a BoundRequest instance."""
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        app: Any,
        path: str,
        handler: Callable[[BoundRequest], Awaitable[Any]],
        on_startup: Callable[..., Awaitable[Any]] | None = None,
        on_shutdown: Callable[..., Awaitable[Any]] | None = None,
    ) -> None:
        """
        Register a webhook handler with the adapter.

        :param app: The web application instance.
        :param path: The path for the webhook endpoint.
        :param handler: The handler function to process incoming requests.
        :param on_startup: Optional startup callback.
        :param on_shutdown: Optional shutdown callback.
        """
        raise NotImplementedError
