from aiogram import Bot

from aiogram_webhook.adapters.base import BoundRequest
from aiogram_webhook.routing.base import BaseRouting


class PathRouting(BaseRouting):
    """
    URL path-based routing strategy.

    Extracts bot token from URL path parameters.
    Example: /webhook/{token} -> extracts token from path.
    """

    def __init__(self, url: str, param: str | None = None) -> None:
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
        return bound_request.path_param(self.param)
