from aiogram_webhook.routing.base import BaseRouting


class StaticRouting(BaseRouting):
    """Routing without token, static webhook URL."""

    def __init__(self, url: str) -> None:
        super().__init__(url=url)
        self.url_template = self.url.human_repr()

    def webhook_point(self, bot) -> str:  # noqa: ARG002
        return self.url_template
