from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram_webhook.engines.base import WebhookEngine

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

    from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
    from aiogram_webhook.routing.base import BaseRouting
    from aiogram_webhook.security.security import Security


class SimpleEngine(WebhookEngine):
    """
    Simple webhook engine for single-bot applications.

    Uses a single Bot instance for all webhook requests.
    Ideal for applications that handle only one bot.
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
        Initialize the SimpleEngine for a single bot.

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

    def _get_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:  # noqa: ARG002
        """
        Always returns the single Bot instance for any request.

        Args:
            bound_request: The incoming bound request.
        Returns:
            The single Bot instance.
        """
        return self.bot

    async def on_startup(self, app: Any, *args, **kwargs) -> None:  # noqa: ARG002
        """
        Called on application startup. Emits dispatcher startup event.
        """
        workflow_data = self._build_workflow_data(app=app, bot=self.bot, **kwargs)
        await self.dispatcher.emit_startup(**workflow_data)

    async def set_webhook(self, **kwargs) -> Bot:
        """
        Sets the webhook for the single Bot instance.

        Args:
            **kwargs: Additional arguments for set_webhook.
        Returns:
            The Bot instance after setting webhook.
        """
        secret_token = await self.security.get_secret_token(bot=self.bot) if self.security else None

        await self.bot.set_webhook(url=self.routing.webhook_point(self.bot), secret_token=secret_token, **kwargs)
        return self.bot

    async def on_shutdown(self, app: Any, *args, **kwargs) -> None:  # noqa: ARG002
        """
        Called on application shutdown. Emits dispatcher shutdown event and closes bot session.
        """
        workflow_data = self._build_workflow_data(app=app, bot=self.bot, **kwargs)
        await self.dispatcher.emit_shutdown(**workflow_data)
        await self.bot.session.close()
