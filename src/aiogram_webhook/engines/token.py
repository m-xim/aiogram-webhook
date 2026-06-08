import asyncio
from typing import TYPE_CHECKING, Generic

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.token import TokenValidationError, extract_bot_id

from aiogram_webhook.configs.bot import BotConfig
from aiogram_webhook.configs.webhook import WebhookConfig
from aiogram_webhook.engines.base import AppT, FrameworkResponseT, RawRequestT, logger
from aiogram_webhook.engines.multi import BaseMultiBotEngine
from aiogram_webhook.engines.target import Target
from aiogram_webhook.route import Route
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.web.base import WebAdapter, WebRequest

if TYPE_CHECKING:
    from aiogram.client.session.base import BaseSession


class TokenEngine(
    BaseMultiBotEngine[AppT, RawRequestT, FrameworkResponseT], Generic[AppT, RawRequestT, FrameworkResponseT]
):
    def __init__(
        self,
        dispatcher,
        web: WebAdapter[AppT, RawRequestT, FrameworkResponseT],
        route: Route,
        security=None,
        bot_config: BotConfig | None = None,
        webhook_config: WebhookConfig | None = None,
        handle_in_background: bool = True,
        shutdown_timeout: float = 10.0,
    ) -> None:
        super().__init__(
            dispatcher=dispatcher,
            web=web,
            route=route,
            security=security,
            webhook_config=webhook_config,
            handle_in_background=handle_in_background,
            shutdown_timeout=shutdown_timeout,
        )

        self.bot_config = bot_config or BotConfig()
        self._owns_session = self.bot_config.session is None
        self._session: BaseSession | None = self.bot_config.session or AiohttpSession()

    async def add_bot(self, token: str, webhook_config: WebhookConfig | None = None) -> Bot:
        target = Target(bot_id=extract_bot_id(token), bot_token=token)
        bot = await self._resolve_bot(target=target)

        webhook_kwargs = await self._build_webhook_kwargs(target=target, webhook_config=webhook_config)
        await bot.set_webhook(url=await self.route.build_url(target=target), **webhook_kwargs)

        logger.info("Added bot %s to token engine and set webhook", bot.id)
        return bot

    async def remove_bot(self, bot_id: int, delete_webhook: bool, drop_pending_updates: bool | None = None) -> bool:
        bot = self._bots.get(bot_id)

        if bot is None:
            return False

        if delete_webhook:
            await bot.delete_webhook(drop_pending_updates=drop_pending_updates)
        elif drop_pending_updates is not None:
            raise ValueError(
                "drop_pending_updates was provided but delete_webhook is False. "
                "Set delete_webhook=True to delete webhook and optionally drop pending updates."
            )

        if (tracker := self._task_trackers.pop(bot_id, None)) is not None:
            await tracker.close(timeout=self.shutdown_timeout)
        self._bots.pop(bot_id, None)

        logger.info("Removed bot %s from token engine", bot_id)

        return True

    async def _resolve_target(self, request: WebRequest[RawRequestT], route_params: RouteParams) -> Target | None:  # noqa: ARG002
        bot_token = route_params.get("bot_token")
        if not bot_token or not isinstance(bot_token, str):
            return None

        try:
            bot_id = extract_bot_id(bot_token)
        except (TokenValidationError, ValueError):
            return None

        return Target(bot_id=bot_id, bot_token=bot_token)

    async def _resolve_bot(self, target: Target) -> Bot:
        existing_bot = self._bots.get(target.bot_id)

        if existing_bot is not None and existing_bot.token == target.bot_token:
            return existing_bot

        session = self._session
        if session is None:
            session = AiohttpSession()
            self._session = session

        bot = Bot(token=target.bot_token, session=session, default=self.bot_config.default)
        self._bots[bot.id] = bot
        return bot

    async def _on_startup(self, app: AppT, *args, **kwargs) -> None:  # noqa: ARG002
        startup_bots = set(self._bots.values())

        logger.info("Starting token-based webhook engine with %s bot(s)", len(startup_bots))
        workflow_data = self._build_lifecycle_data(app=app, bots=startup_bots, **kwargs)
        await self.dispatcher.emit_startup(**workflow_data)

    async def _on_shutdown(self, app: AppT, *args, **kwargs) -> None:  # noqa: ARG002
        logger.info("Stopping token-based webhook engine with %s bot(s)", len(self._bots))
        await asyncio.gather(
            *(tracker.close(timeout=self.shutdown_timeout) for tracker in self._task_trackers.values()),
        )

        self._task_trackers.clear()

        lifecycle_data = self._build_lifecycle_data(app=app, bots=set(self.bots.values()), **kwargs)
        await self.dispatcher.emit_shutdown(**lifecycle_data)

        self._bots.clear()

        session = self._session
        if self._owns_session and session is not None:
            await session.close()
            self._session = None
