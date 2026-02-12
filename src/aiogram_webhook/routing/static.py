from aiogram_webhook.routing import BaseRouting


class StaticRouting(BaseRouting):
    """Routing without token, static webhook URL."""

    def __init__(self, url: str) -> None:
        super().__init__(url=url)

    def webhook_point(self, bot) -> str:  # noqa: ARG002
        return self._url_str
