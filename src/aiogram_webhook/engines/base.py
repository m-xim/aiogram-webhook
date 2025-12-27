import asyncio
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType

from aiogram_webhook.adapters.base import BoundRequest, WebAdapter
from aiogram_webhook.routing.base import BaseRouting
from aiogram_webhook.security.checks.ip import IPCheck
from aiogram_webhook.security.security import Security

if TYPE_CHECKING:
    from aiogram.types import InputFile


class WebhookEngine(ABC):
    """
    Base webhook engine for processing Telegram bot updates.

    Handles incoming webhook requests, bot resolution, security checks,
    routing, and dispatching updates to the aiogram dispatcher. Supports
    both synchronous and background processing.

    Constructor arguments:
        dispatcher: aiogram.Dispatcher instance for update processing.
        web_adapter: Web framework adapter class.
        routing: Webhook routing strategy.
        security: True — protect by IP (IPCheck), False/None — not protect, Security — custom protect.
        handle_in_background: Whether to process updates in background (default: True).
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        /,
        web_adapter: WebAdapter,
        routing: BaseRouting,
        security: Security | bool | None = None,
        handle_in_background: bool = True,
    ) -> None:
        if security is True:
            self.security = Security(IPCheck())
        else:
            self.security = security
        self.dispatcher = dispatcher
        self.web_adapter = web_adapter
        self.routing = routing
        self.handle_in_background = handle_in_background
        self._background_feed_update_tasks: set[asyncio.Task[Any]] = set()

    @abstractmethod
    def resolve_bot_from_request(self, bound_request: BoundRequest) -> Bot | None:
        raise NotImplementedError

    @abstractmethod
    async def on_startup(self, bots: Iterable[Bot] | None = None, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_shutdown(self) -> None:
        raise NotImplementedError

    async def handle_request(self, bound_request: BoundRequest):
        bot = self.resolve_bot_from_request(bound_request)
        if bot is None:
            return bound_request.json_response(status=400, payload={"detail": "Bot not found"})

        if self.security:
            is_allowed = await self.security.verify(bot=bot, bound_request=bound_request)
            if not is_allowed:
                return bound_request.json_response(status=403, payload={"detail": "Forbidden"})

        if self.handle_in_background:
            return await self._handle_request_background(bot=bot, bound_request=bound_request)

        return await self._handle_request(bot=bot, bound_request=bound_request)

    def register(self, app: Any) -> None:
        self.web_adapter.register(app=app, path=self.routing.path, handler=self.handle_request)

    async def _handle_request(self, bot: Bot, bound_request: BoundRequest) -> dict[str, Any]:
        result = await self.dispatcher.feed_webhook_update(bot=bot, update=await bound_request.json())

        if not isinstance(result, TelegramMethod):
            return bound_request.json_response(status=200, payload={})

        if self._has_files(bot, result):
            await self.dispatcher.silent_call_request(bot=bot, result=result)
            return bound_request.json_response(status=200, payload={})

        payload = self._to_webhook_json(bot, result)
        return bound_request.json_response(status=200, payload=payload)

    async def _background_feed_update(self, bot: Bot, update: dict[str, Any]) -> None:
        result = await self.dispatcher.feed_raw_update(bot=bot, update=update)  # **self.data
        if isinstance(result, TelegramMethod):
            await self.dispatcher.silent_call_request(bot=bot, result=result)

    async def _handle_request_background(self, bot: Bot, bound_request: BoundRequest):
        feed_update_task = asyncio.create_task(
            self._background_feed_update(
                bot=bot,
                update=await bound_request.json(),
            ),
        )
        self._background_feed_update_tasks.add(feed_update_task)
        feed_update_task.add_done_callback(self._background_feed_update_tasks.discard)

        return bound_request.json_response(status=200, payload={})

    @staticmethod
    def _has_files(bot: Bot, method: TelegramMethod[TelegramType]) -> bool:
        files: dict[str, InputFile] = {}
        for v in method.model_dump(warnings=False).values():
            bot.session.prepare_value(v, bot=bot, files=files)
        return bool(files)

    @staticmethod
    def _to_webhook_json(bot: Bot, method: TelegramMethod[TelegramType]) -> dict[str, Any]:
        files: dict[str, InputFile] = {}
        params: dict[str, Any] = {}
        for k, v in method.model_dump(warnings=False).items():
            pv = bot.session.prepare_value(v, bot=bot, files=files)
            if pv is not None:
                params[k] = pv
        return {"method": method.__api_method__, **params}
