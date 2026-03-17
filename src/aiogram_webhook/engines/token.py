from __future__ import annotations

import warnings
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from aiogram import Bot, Dispatcher
from aiogram.utils.token import extract_bot_id

from aiogram_webhook.config.bot import BotConfig
from aiogram_webhook.engines.base import WebhookEngine

if TYPE_CHECKING:
    from aiogram_webhook.adapters.base_adapter import BoundRequest, WebAdapter
    from aiogram_webhook.config.webhook import WebhookConfig
    from aiogram_webhook.routing.base import TokenRouting
    from aiogram_webhook.security.security import Security


class TokenEngine(WebhookEngine):
    """
    Multi-bot webhook engine with dynamic bot resolution.

    Resolves Bot instances from request tokens.
    Creates and caches Bot instances on-demand. Suitable for multi-tenant applications.
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        /,
        web_adapter: WebAdapter,
        routing: TokenRouting,
        security: Security | None = None,
        bot_config: BotConfig | None = None,
        webhook_config: WebhookConfig | None = None,
        handle_in_background: bool = True,
    ) -> None:
        super().__init__(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
            webhook_config=webhook_config,
            handle_in_background=handle_in_background,
        )
        self.routing: TokenRouting = routing  # for type checker
        self.bot_config = bot_config or BotConfig()
        self._bots: dict[int, Bot] = {}

    @property
    def bots(self) -> MappingProxyType[int, Bot]:
        return MappingProxyType(self._bots)

    def _get_bot_token_for_request(self, bound_request: BoundRequest) -> str | None:
        return self.routing.extract_token(bound_request)

    def _get_bot_by_token(self, token: str) -> Bot:
        bot_id = extract_bot_id(token)
        existing_bot = self.bots.get(bot_id)

        if existing_bot is None or existing_bot.token != token:
            new_bot = self._build_bot(token)
            self._bots[bot_id] = new_bot
            return new_bot

        return existing_bot

    def _build_bot(self, token: str) -> Bot:
        """Build a new Bot instance from token."""
        return Bot(token=token, session=self.bot_config.session, default=self.bot_config.default)

    async def set_webhook(
        self,
        token: str,
        *,
        max_connections: int | None = None,
        drop_pending_updates: bool | None = None,
        allowed_updates: list[str] | None = None,
        request_timeout: int | None = None,
    ) -> Bot:
        """
        Set the webhook for the Bot instance resolved by token.

        Source: https://core.telegram.org/bots/api#setwebhook

        :param token: The bot token for which to set the webhook.
        :param max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to *40*. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify :code:`["message", "edited_channel_post", "callback_query"]` to only receive updates of these types. See :class:`aiogram.types.update.Update` for a complete list of available update types. Specify an empty list to receive all update types except *chat_member*, *message_reaction*, and *message_reaction_count* (default). If not specified, the previous setting will be used.
        :param drop_pending_updates: Pass :code:`True` to drop all pending updates
        :param request_timeout: Request timeout
        :return: Bot instance
        """

        bot = self._get_bot_by_token(token=token)
        params = self._build_webhook_config(
            max_connections=max_connections,
            drop_pending_updates=drop_pending_updates,
            allowed_updates=allowed_updates,
        ).model_dump(exclude_none=True)

        if self.security is not None:
            secret_token = await self.security.get_secret_token(token=token)
            if secret_token is not None:
                params["secret_token"] = secret_token

        await bot.set_webhook(url=self.routing.webhook_url(bot), request_timeout=request_timeout, **params)
        return bot

    async def on_startup(self, app: Any, *args, bots: set[Bot] | None = None, **kwargs) -> None:  # noqa: ARG002
        all_bots = set(bots) | set(self.bots.values()) if bots else set(self.bots.values())
        workflow_data = self._build_workflow_data(app=app, bots=all_bots, **kwargs)
        await self.dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(self, app: Any, *args, **kwargs) -> None:  # noqa: ARG002
        workflow_data = self._build_workflow_data(app=app, bots=set(self.bots.values()), **kwargs)
        await self.dispatcher.emit_shutdown(**workflow_data)

        for bot in self.bots.values():
            await bot.session.close()
        self._bots.clear()

    def get_bot(self, token: str) -> Bot:
        warnings.warn("get_bot is deprecated, use _get_bot_by_token", DeprecationWarning, stacklevel=2)
        return self._get_bot_by_token(token)
