from aiogram_webhook.routing.base import TokenRouting


class QueryRouting(TokenRouting):
    """
    Routing strategy based on the URL query parameter.

    Extracts the bot token from a query parameter in the URL.
    Example: /webhook?token=123:ABC will extract the token from the query string.
    """

    def extract_token(self, bound_request) -> str | None:
        return bound_request.query_param(self.param)
