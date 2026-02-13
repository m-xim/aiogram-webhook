from aiogram import Bot

from aiogram_webhook.routing.base import TokenRouting


class QueryRouting(TokenRouting):
    """
    Routing strategy based on the URL query parameter.

    Extracts the bot token from a query parameter in the URL.
    Example: https://example.com/webhook?token=123:ABC will extract the token from the query string.
    """

    def webhook_point(self, bot: Bot) -> str:
        return self.url.extend_query({self.param: bot.token}).human_repr()

    def extract_token(self, bound_request) -> str | None:
        return bound_request.query_param(self.param)
