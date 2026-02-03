from aiogram_webhook.routing.base import TokenRouting


class PathRouting(TokenRouting):
    """
    Routing strategy based on the URL path parameter.

    Extracts the bot token from a path parameter in the URL.
    Example: /webhook/{token} will extract the token from the path segment.
    """

    def extract_token(self, bound_request) -> str | None:
        return bound_request.path_param(self.param)
