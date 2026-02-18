from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram_webhook.engines.base import WebhookEngine

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

    from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
    from aiogram_webhook.config.webhook import WebhookConfig
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
        security: Security | None = None,
        webhook_config: WebhookConfig | None = None,
        handle_in_background: bool = True,
    ) -> None:
        self.bot = bot
        super().__init__(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
            webhook_config=webhook_config,
            handle_in_background=handle_in_background,
        )

    def _get_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:  # noqa: ARG002
        """
        Always returns the single Bot instance for any request.

        :param bound_request: The incoming bound request.
        :return: The single Bot instance
        """
        return self.bot

    async def on_startup(self, app: Any, *args, **kwargs) -> None:  # noqa: ARG002
        """
        Called on application startup. Emits dispatcher startup event.
        """
        workflow_data = self._build_workflow_data(app=app, bot=self.bot, **kwargs)
        await self.dispatcher.emit_startup(**workflow_data)

    async def set_webhook(
        self,
        *,
        max_connections: int | None = None,
        drop_pending_updates: bool | None = None,
        allowed_updates: list[str] | None = None,
        request_timeout: int | None = None,
    ) -> Bot:
        """
        Set the webhook for the Bot instance.

        Source: https://core.telegram.org/bots/api#setwebhook

        :param max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to *40*. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify :code:`["message", "edited_channel_post", "callback_query"]` to only receive updates of these types. See :class:`aiogram.types.update.Update` for a complete list of available update types. Specify an empty list to receive all update types except *chat_member*, *message_reaction*, and *message_reaction_count* (default). If not specified, the previous setting will be used.
        :param drop_pending_updates: Pass :code:`True` to drop all pending updates
        :param request_timeout: Request timeout
        :return: Bot
        """
        config = self._build_webhook_config(
            max_connections=max_connections,
            drop_pending_updates=drop_pending_updates,
            allowed_updates=allowed_updates,
        )
        params = config.model_dump(exclude_none=True)

        secret_token = await self.security.get_secret_token(bot=self.bot)
        if secret_token is not None:
            params["secret_token"] = secret_token

        await self.bot.set_webhook(url=self.routing.webhook_point(self.bot), request_timeout=request_timeout, **params)
        return self.bot

    async def on_shutdown(self, app: Any, *args, **kwargs) -> None:  # noqa: ARG002
        """
        Called on application shutdown. Emits dispatcher shutdown event and closes bot session.
        """
        workflow_data = self._build_workflow_data(app=app, bot=self.bot, **kwargs)
        await self.dispatcher.emit_shutdown(**workflow_data)
        await self.bot.session.close()
