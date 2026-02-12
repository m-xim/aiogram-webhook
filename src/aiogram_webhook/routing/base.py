from abc import ABC, abstractmethod

from aiogram import Bot
from yarl import URL

from aiogram_webhook.adapters.base import BoundRequest


class BaseRouting(ABC):
    """
    Abstract base class for webhook routing strategies.

    Defines how webhook URLs are constructed and how keys (tokens)
    are extracted from incoming requests.

    Attributes:
        url: URL template.
    """

    def __init__(self, url: str) -> None:
        self.url = URL(url)
        self.base = self.url.origin()
        self.path = self.url.path
        self._url_str = self.url.human_repr()

    @abstractmethod
    def webhook_point(self, bot: Bot) -> str:
        """Return the webhook URL for the given bot."""
        raise NotImplementedError


class TokenRouting(BaseRouting, ABC):
    """Routing by token parameter."""

    def __init__(self, url: str, param: str = "bot_token") -> None:
        super().__init__(url)
        self.param = param

        if f"{{{self.param}}}" not in self._url_str:
            raise KeyError(f"Parameter '{self.param}' not found in url template: {self._url_str}")

    def webhook_point(self, bot: Bot) -> str:
        return self._url_str.format_map({self.param: bot.token})

    @abstractmethod
    def extract_token(self, bound_request: BoundRequest) -> str | None:
        """Extract the bot token from the incoming request."""
        raise NotImplementedError
