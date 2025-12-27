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
        url: Url template.
    """

    def __init__(self, url: str) -> None:
        self.url = URL(url)
        self.base = self.url.origin()
        self.path = self.url.path

    @abstractmethod
    def webhook_point(self, bot: Bot) -> str:
        """Return the webhook URL for the given bot."""
        raise NotImplementedError

    @abstractmethod
    def extract_key(self, bound_request: BoundRequest) -> str | None:
        """Extract the routing key (e.g., token) from the incoming request."""
        raise NotImplementedError
