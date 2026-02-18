from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from aiogram.methods import TelegramMethod

from aiogram_webhook.config.webhook import WebhookConfig
from aiogram_webhook.security.security import Security

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher
    from aiogram.methods.base import TelegramType
    from aiogram.types import InputFile

    from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
    from aiogram_webhook.routing.base import BaseRouting


class WebhookEngine(ABC):
    """
    Base webhook engine for processing Telegram bot updates.

    Handles incoming webhook requests, bot resolution, security checks,
    routing, and dispatching updates to the aiogram dispatcher. Supports
    both synchronous and background processing.
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        /,
        web_adapter: WebAdapter,
        routing: BaseRouting,
        security: Security | None = None,
        webhook_config: WebhookConfig | None = None,
        handle_in_background: bool = True,
    ) -> None:
        self.dispatcher = dispatcher
        self.web_adapter = web_adapter
        self.routing = routing
        self.security = security or Security()
        self.webhook_config = webhook_config or WebhookConfig()
        self.handle_in_background = handle_in_background
        self._background_feed_update_tasks: set[asyncio.Task[Any]] = set()

    @abstractmethod
    def _get_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:
        raise NotImplementedError

    @abstractmethod
    async def set_webhook(self, *args, **kwargs) -> Bot:
        raise NotImplementedError

    @abstractmethod
    async def on_startup(self, app: Any, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_shutdown(self, app: Any, *args, **kwargs) -> None:
        raise NotImplementedError

    def _build_workflow_data(self, app: Any, **kwargs) -> dict[str, Any]:
        """Build workflow data for startup/shutdown events."""
        return {
            "app": app,
            "dispatcher": self.dispatcher,
            "webhook_engine": self,
            **self.dispatcher.workflow_data,
            **kwargs,
        }

    async def handle_request(self, bound_request: BoundRequest):
        bot = self._get_bot_from_request(bound_request)
        if bot is None:
            return bound_request.json_response(status=400, payload={"detail": "Bot not found"})

        is_allowed = await self.security.verify(bot=bot, bound_request=bound_request)
        if not is_allowed:
            return bound_request.json_response(status=403, payload={"detail": "Forbidden"})

        if self.handle_in_background:
            return await self._handle_request_background(bot=bot, bound_request=bound_request)

        return await self._handle_request(bot=bot, bound_request=bound_request)

    def register(self, app: Any) -> None:
        self.web_adapter.register(
            app=app,
            path=self.routing.path,
            handler=self.handle_request,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )

    async def _handle_request(self, bot: Bot, bound_request: BoundRequest) -> dict[str, Any]:
        result = await self.dispatcher.feed_webhook_update(bot=bot, update=await bound_request.json())

        if not isinstance(result, TelegramMethod):
            return bound_request.json_response(status=200, payload={})

        payload = self._build_webhook_payload(bot, result)
        if payload is None:
            # Has new files (InputFile) — execute directly via API
            await self.dispatcher.silent_call_request(bot=bot, result=result)
            return bound_request.json_response(status=200, payload={})

        return bound_request.json_response(status=200, payload=payload)

    async def _background_feed_update(self, bot: Bot, update: dict[str, Any]) -> None:
        result = await self.dispatcher.feed_raw_update(bot=bot, update=update)  # **self.data
        if isinstance(result, TelegramMethod):
            await self.dispatcher.silent_call_request(bot=bot, result=result)

    async def _handle_request_background(self, bot: Bot, bound_request: BoundRequest):
        feed_update_task = asyncio.create_task(
            self._background_feed_update(bot=bot, update=await bound_request.json()),
        )
        self._background_feed_update_tasks.add(feed_update_task)
        feed_update_task.add_done_callback(self._background_feed_update_tasks.discard)

        return bound_request.json_response(status=200, payload={})

    @staticmethod
    def _build_webhook_payload(bot: Bot, method: TelegramMethod[TelegramType]) -> dict[str, Any] | None:
        """
        Convert TelegramMethod to webhook response payload.

        See: https://core.telegram.org/bots/faq#how-can-i-make-requests-in-response-to-updates
        """
        files: dict[str, InputFile] = {}
        params: dict[str, Any] = {}
        for k, v in method.model_dump(warnings=False).items():
            pv = bot.session.prepare_value(v, bot=bot, files=files)
            # New files detected — can't use webhook response
            if files:
                return None
            if pv is not None:
                params[k] = pv
        return {"method": method.__api_method__, **params}

    def _build_webhook_config(
        self,
        *,
        max_connections: int | None = None,
        drop_pending_updates: bool | None = None,
        allowed_updates: list[str] | None = None,
    ) -> WebhookConfig:
        overrides = {}
        if max_connections is not None:
            overrides["max_connections"] = max_connections
        if drop_pending_updates is not None:
            overrides["drop_pending_updates"] = drop_pending_updates
        if allowed_updates is not None:
            overrides["allowed_updates"] = allowed_updates
        return self.webhook_config.model_copy(update=overrides) if overrides else self.webhook_config
