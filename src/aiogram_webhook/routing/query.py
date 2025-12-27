from aiogram import Bot

from aiogram_webhook.adapters.base import BoundRequest
from aiogram_webhook.routing.base import BaseRouting


class QueryRouting(BaseRouting):
    """
    URL query parameter-based routing strategy.

    Extracts bot token from query parameters.
    Example: /webhook?token=123:ABC -> extracts token from query.
    """

    def __init__(self, url: str, param: str) -> None:
        """
        Initialize the query parameter-based routing strategy.

        Args:
            url: The URL template for webhook endpoints.
            param: The query parameter name for the bot token.
        """
        super().__init__(url=url)
        self.param = param

    def webhook_point(self, bot: Bot) -> str:
        url = self.url.human_repr()
        if self.param is None:
            return url
        return url.format_map({self.param: bot.token})

    def extract_key(self, bound_request: BoundRequest) -> str | None:
        if self.param is None:
            return None
        return bound_request.query_param(self.param)
