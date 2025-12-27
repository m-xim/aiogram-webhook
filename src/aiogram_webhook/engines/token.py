from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram import Bot, Dispatcher
from aiogram.utils.token import extract_bot_id

from aiogram_webhook.engines.base import WebhookEngine

if TYPE_CHECKING:
    from collections.abc import Iterable

    from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
    from aiogram_webhook.routing.base import BaseRouting
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
        routing: BaseRouting,
        security: Security | bool | None = None,
        bot_settings: dict[str, Any] | None = None,
        handle_in_background: bool = True,
    ) -> None:
        """
        Initialize the TokenEngine for multi-bot applications.

        Args:
            dispatcher: Dispatcher instance for update processing.
            web_adapter: Web framework adapter class.
            routing: Webhook routing strategy.
            security: Security settings and checks.
            bot_settings: Default settings for creating Bot instances.
            handle_in_background: Whether to process updates in background.
        """
        super().__init__(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
            handle_in_background=handle_in_background,
        )
        self.bot_settings = bot_settings
        self._bots: dict[int, Bot] = {}

    def resolve_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:
        token = self.routing.extract_key(bound_request)
        if not token:
            return None
        return self.resolve_bot(token)

    async def on_startup(self, bots: Iterable[Bot] | None = None, **kwargs: Any) -> None:
        """Called on application startup. Emits dispatcher startup event for all bots."""
        all_bots = set(bots) | set(self._bots.values()) if bots else set(self._bots.values())

        await self.dispatcher.emit_startup(
            dispatcher=self.dispatcher,
            bots=all_bots,
            webhook_engine=self,
            **kwargs,
        )

    async def on_shutdown(self) -> None:
        """Called on application shutdown. Emits dispatcher shutdown event and closes all bot sessions."""
        await self.dispatcher.emit_shutdown(
            dispatcher=self.dispatcher,
            bots=set(self._bots.values()),
            webhook_engine=self,
        )

        for bot in self._bots.values():
            await bot.session.close()
        # self._bots.clear()

    async def set_webhook(self, token: str, **kwargs) -> Bot:
        """Sets the webhook for the Bot instance resolved by token."""
        bot = self.resolve_bot(token)

        await bot.set_webhook(url=self.routing.webhook_point(bot), secret_token=None, **kwargs)
        return bot

    def resolve_bot(self, token: str) -> Bot:
        """Resolve or create a Bot instance by token and cache it."""
        bot = self._bots.get(extract_bot_id(token))
        if not bot:
            bot = Bot(token=token, **(self.bot_settings or {}))
            self._bots[bot.id] = bot
        return bot
