from aiogram import Bot

from aiogram_webhook.adapters.base_adapter import BoundRequest
from aiogram_webhook.routing.base import TokenRouting


class PathRouting(TokenRouting):
    """
    Path-based routing for webhook requests.

    Extracts the bot token from a path parameter in the URL.
    Example: https://example.com/webhook/{token} will extract the token from the path segment.
    """

    def __init__(self, url: str, param: str = "bot_token") -> None:
        super().__init__(url=url, param=param)
        self.url_template = self.url.human_repr()

        if f"{{{self.param}}}" not in self.url_template:
            raise ValueError(
                f"Parameter '{self.param}' not found in URL template. "
                f"Expected placeholder '{{{self.param}}}' in: {self.url_template}"
            )

    async def webhook_url(self, bot: Bot) -> str:
        return self.url_template.format_map({self.param: bot.token})

    async def resolve_token(self, bound_request: BoundRequest) -> str | None:
        return bound_request.path_params.get(self.param)
