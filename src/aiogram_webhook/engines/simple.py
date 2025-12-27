from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram_webhook.engines.base import WebhookEngine

if TYPE_CHECKING:
    from collections.abc import Iterable

    from aiogram import Bot, Dispatcher

    from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
    from aiogram_webhook.routing.base import BaseRouting
    from aiogram_webhook.security.security import Security


class SimpleEngine(WebhookEngine):
    """
    Simple webhook engine for single-bot applications.

    Uses a single Bot instance for all webhook requests.
    Ideal for applications that handle only one bot.

    Attributes:
        bot: The Bot instance to use for all requests.
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        /,
        web_adapter: WebAdapter,
        routing: BaseRouting,
        security: Security | bool | None = None,
        handle_in_background: bool = True,
    ) -> None:
        """
        Initialize the SimpleEngine for one bot.

        Args:
            dispatcher: Dispatcher instance for update processing.
            bot: The Bot instance to use for all requests.
            web_adapter: Web framework adapter class.
            routing: Webhook routing strategy.
            security: Security settings and checks.
            handle_in_background: Whether to process updates in background.
        """
        self.bot = bot
        super().__init__(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
            handle_in_background=handle_in_background,
        )

    def resolve_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:  # noqa: ARG002
        """
        Always returns the single Bot instance for any request.

        Args:
            bound_request: The incoming bound request.
        Returns:
            The single Bot instance.
        """
        return self.bot

    async def on_startup(self, bots: Iterable[Bot] | None = None, **kwargs: Any) -> None:
        """
        Called on application startup. Emits dispatcher startup event for all bots.

        Args:
            bots: Optional iterable of Bot instances.
            **kwargs: Additional keyword arguments for dispatcher.
        """
        all_bots = set(bots) | {self.bot} if bots else {self.bot}
        await self.dispatcher.emit_startup(
            dispatcher=self.dispatcher,
            bots=all_bots,
            webhook_engine=self,
            **kwargs,
        )

    async def on_shutdown(self) -> None:
        """
        Called on application shutdown. Emits dispatcher shutdown event and closes bot session.
        """
        await self.dispatcher.emit_shutdown(
            dispatcher=self.dispatcher,
            bots={self.bot},
            webhook_engine=self,
        )
        await self.bot.session.close()

    async def set_webhook(self, **kwargs) -> Bot:
        """
        Sets the webhook for the single Bot instance.

        Args:
            **kwargs: Additional arguments for set_webhook.
        Returns:
            The Bot instance after setting webhook.
        """
        await self.bot.set_webhook(url=self.routing.webhook_point(self.bot), secret_token=None, **kwargs)
        return self.bot
