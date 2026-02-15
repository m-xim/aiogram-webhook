from abc import ABC, abstractmethod

from aiogram import Bot
from yarl import URL

from aiogram_webhook.adapters.base import BoundRequest


class BaseRouting(ABC):
    """
    Abstract base class for webhook routing.

    Defines how webhook URLs are constructed and how keys (tokens)
    are extracted from incoming requests.
    """

    def __init__(self, url: str) -> None:
        self.url = URL(url)
        self.base = self.url.origin()
        self.path = self.url.path

    @abstractmethod
    def webhook_point(self, bot: Bot) -> str:
        """Get the webhook URL for the given bot."""
        raise NotImplementedError


class TokenRouting(BaseRouting, ABC):
    """Routing by token parameter."""

    def __init__(self, url: str, param: str = "bot_token") -> None:
        super().__init__(url=url)
        self.param = param

    @abstractmethod
    def extract_token(self, bound_request: BoundRequest) -> str | None:
        """Extract the bot token from the incoming request."""
        raise NotImplementedError
