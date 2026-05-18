import warnings
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from aiogram import Bot
from aiogram.methods import TelegramMethod

from aiogram_webhook.configs.webhook import WebhookConfig
from aiogram_webhook.engines.errors import BotNotFoundError, InvalidJsonError, TargetNotFoundError
from aiogram_webhook.engines.target import Target
from aiogram_webhook.errors import AiogramWebhookError
from aiogram_webhook.logs import get_logger, log_webhook_error
from aiogram_webhook.route import Route
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.security import Security
from aiogram_webhook.tasks import TaskTracker
from aiogram_webhook.utils.config import dataclass_config_to_kwargs
from aiogram_webhook.utils.webhook_payload import build_webhook_payload
from aiogram_webhook.web.base import WebAdapter, WebRequest

logger = get_logger("engines")

AppT = TypeVar("AppT")
RawRequestT = TypeVar("RawRequestT")
FrameworkResponseT = TypeVar("FrameworkResponseT")


class BaseWebhookEngine(ABC, Generic[AppT, RawRequestT, FrameworkResponseT]):
    def __init__(
        self,
        dispatcher,
        /,
        *,
        web: WebAdapter[AppT, RawRequestT, FrameworkResponseT],
        route: Route,
        security: Security | None = None,
        webhook_config: WebhookConfig | None = None,
        handle_in_background: bool = True,
    ) -> None:
        self.dispatcher = dispatcher
        self.web = web
        self.route = route
        self.security = security
        self.webhook_config = webhook_config or WebhookConfig()
        self.handle_in_background = handle_in_background

        if self.security is None:
            warnings.warn("Security is not configured", UserWarning, stacklevel=3)

    def register(self, app: AppT) -> None:
        logger.info("Registering webhook path %s via %s", self.route.path, self.web.__class__.__name__)
        self.web.register(
            app=app,
            path=self.route.path,
            handler=self.handle_request,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )

    async def handle_request(self, request: WebRequest[RawRequestT]) -> FrameworkResponseT:
        try:
            route_params = await self.route.match(request)

            target = await self._resolve_target(request=request, route_params=route_params)
            if target is None:
                raise TargetNotFoundError(route_param_names=route_params.keys())

            if self.security is not None:
                await self.security.verify(target=target, request=request, route_params=route_params)

            bot = await self._resolve_bot(target=target)
            if bot is None:
                raise BotNotFoundError(target_bot_id=target.bot_id, target_type=target.__class__.__name__)

            try:
                update = await request.json()
            except ValueError as exc:
                raise InvalidJsonError(original_error=exc) from exc

            if self.handle_in_background:
                self._get_task_tracker(bot).spawn(self._background_feed(bot, update))

                return self.web.json_response(status_code=200, data={})

            result = await self.dispatcher.feed_webhook_update(bot=bot, update=update)
            if result is None:
                return self.web.json_response(status_code=200, data={})

            payload = build_webhook_payload(bot, result)
            if payload is None:
                await self.dispatcher.silent_call_request(bot=bot, result=result)
                return self.web.json_response(status_code=200, data={})

            return self.web.json_response(status_code=200, data=payload)

        except AiogramWebhookError as exc:
            log_webhook_error(logger, exc)

            return self.web.json_response(status_code=exc.status_code, data=exc.response_payload())

    @abstractmethod
    async def on_startup(self, app: AppT, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_shutdown(self, app: AppT, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _resolve_target(self, request: WebRequest[RawRequestT], route_params: RouteParams) -> Target | None: ...

    @abstractmethod
    async def _resolve_bot(self, target: Target) -> Bot | None: ...

    @abstractmethod
    def _get_task_tracker(self, bot: Bot) -> TaskTracker:
        raise NotImplementedError

    async def _background_feed(self, bot: Bot, update: dict[str, Any]) -> None:
        result = await self.dispatcher.feed_raw_update(bot=bot, update=update)

        if isinstance(result, TelegramMethod):
            await self.dispatcher.silent_call_request(bot=bot, result=result)

    def _build_lifecycle_data(self, *, app: AppT, **kwargs) -> dict[str, Any]:
        return {"app": app, "dispatcher": self.dispatcher, **kwargs}

    async def _build_webhook_kwargs(
        self, target: Target, webhook_config: WebhookConfig | None = None
    ) -> dict[str, Any]:
        webhook_kwargs = dataclass_config_to_kwargs(self.webhook_config, webhook_config)

        if self.security is not None:
            secret_token = await self.security.secret_token(target)
            if secret_token is not None:
                webhook_kwargs["secret_token"] = secret_token

        return webhook_kwargs
