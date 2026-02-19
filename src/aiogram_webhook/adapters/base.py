from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Protocol, TypeVar

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram_webhook.security.checks.ip import IPAddress


R = TypeVar("R")


class BoundRequest(ABC, Generic[R]):
    """
    Abstract base class for a request bound to a web adapter.

    Provides interface for extracting data from incoming requests and generating responses.
    """

    __slots__ = ("request",)

    def __init__(self, request: R) -> None:
        self.request = request

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


class WebAdapter(Protocol):
    """
    Protocol for web framework adapters using structural subtyping.

    Provides interface for binding requests and registering webhook handlers.
    """

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

    @abstractmethod
    def create_json_response(self, status: int, payload: dict[str, Any]) -> Any:
        """Create a JSON response with the given status and payload."""
        raise NotImplementedError
