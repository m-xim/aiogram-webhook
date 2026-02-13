from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram import Bot, Dispatcher
from aiogram.utils.token import extract_bot_id

from aiogram_webhook.engines.base import WebhookEngine

if TYPE_CHECKING:
    from collections.abc import Iterable

    from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
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
        self.routing: TokenRouting = routing  # for type checker
        self.bot_settings = bot_settings
        self._bots: dict[int, Bot] = {}

    def _get_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:
        """
        Resolve a Bot instance from the incoming request using the token.

        Args:
            bound_request: The incoming bound request.
        Returns:
            The resolved Bot instance or None if not found.
        """
        token = self.routing.extract_token(bound_request)
        if not token:
            return None
        return self.get_bot(token)

    def get_bot(self, token: str) -> Bot:
        """
        Resolve or create a Bot instance by token and cache it.

        Args:
            token: The bot token.
        Returns:
            The resolved Bot instance.
        """
        bot = self._bots.get(extract_bot_id(token))
        if not bot:
            bot = Bot(token=token, **(self.bot_settings or {}))
            self._bots[bot.id] = bot
        return bot

    async def set_webhook(self, token: str, **kwargs) -> Bot:
        """
        Set the webhook for the Bot instance resolved by token.

        Args:
            token: The bot token.
            **kwargs: Additional arguments for set_webhook.
        Returns:
            The Bot instance after setting webhook.
        """
        bot = self.get_bot(token)
        secret_token = await self.security.get_secret_token(bot=bot) if self.security else None

        await bot.set_webhook(url=self.routing.webhook_point(bot), secret_token=secret_token, **kwargs)
        return bot

    async def on_startup(self, app: Any, *args, bots: Iterable[Bot] | None = None, **kwargs) -> None:  # noqa: ARG002
        """
        Called on application startup. Emits dispatcher startup event for all bots.

        Args:
            *args: Positional arguments (e.g., app from aiohttp).
            app: The web application instance.
            bots: Optional iterable of Bot instances.
            **kwargs: Additional keyword arguments for dispatcher.
        """
        all_bots = set(bots) | set(self._bots.values()) if bots else set(self._bots.values())
        workflow_data = self._build_workflow_data(bots=all_bots, app=app, **kwargs)
        await self.dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(self, app: Any, *args, **kwargs) -> None:  # noqa: ARG002
        """
        Called on application shutdown. Emits dispatcher shutdown event and closes all bot sessions.

        Args:
            *args: Positional arguments (e.g., app from aiohttp).
            app: The web application instance.
            **kwargs: Additional keyword arguments for dispatcher.
        """
        workflow_data = self._build_workflow_data(bots=set(self._bots.values()), app=app, **kwargs)
        await self.dispatcher.emit_shutdown(**workflow_data)

        for bot in self._bots.values():
            await bot.session.close()
        self._bots.clear()
