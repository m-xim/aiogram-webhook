from typing import Generic

from aiogram import Bot

from aiogram_webhook.engines.base import AppT, BaseWebhookEngine, FrameworkResponseT, RawRequestT, logger
from aiogram_webhook.engines.target import Target
from aiogram_webhook.route import Route
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.tasks import TaskTracker
from aiogram_webhook.web.base import WebAdapter, WebRequest


class SingleBotEngine(
    BaseWebhookEngine[AppT, RawRequestT, FrameworkResponseT], Generic[AppT, RawRequestT, FrameworkResponseT]
):
    def __init__(
        self,
        dispatcher,
        bot: Bot,
        /,
        *,
        web: WebAdapter[AppT, RawRequestT, FrameworkResponseT],
        route: Route,
        security=None,
        webhook_config=None,
        handle_in_background: bool = True,
        shutdown_timeout: float = 10.0,
    ) -> None:
        self.bot = bot
        self._task_tracker = TaskTracker()

        super().__init__(
            dispatcher,
            web=web,
            route=route,
            security=security,
            webhook_config=webhook_config,
            handle_in_background=handle_in_background,
            shutdown_timeout=shutdown_timeout,
        )

    async def _resolve_target(self, request: WebRequest[RawRequestT], route_params: RouteParams) -> Target | None:  # noqa: ARG002
        return Target(bot_id=self.bot.id, bot_token=self.bot.token)

    async def _resolve_bot(self, target: Target) -> Bot:  # noqa: ARG002
        return self.bot

    def _get_task_tracker(self, bot: Bot) -> TaskTracker:  # noqa: ARG002
        return self._task_tracker

    async def set_webhook(self) -> bool:
        target = Target(bot_id=self.bot.id, bot_token=self.bot.token)
        webhook_kwargs = await self._build_webhook_kwargs(target=target)
        return await self.bot.set_webhook(url=await self.route.build_url(target=target), **webhook_kwargs)

    async def _on_startup(self, app: AppT, *args, **kwargs) -> None:  # noqa: ARG002
        logger.info("Starting single-bot webhook engine for bot %s", self.bot.id)
        lifecycle_data = self._build_lifecycle_data(app=app, bot=self.bot, **kwargs)
        await self.dispatcher.emit_startup(**lifecycle_data)

    async def _on_shutdown(self, app: AppT, *args, **kwargs) -> None:  # noqa: ARG002
        logger.info("Stopping single-bot webhook engine for bot %s", self.bot.id)
        await self._task_tracker.close(timeout=self.shutdown_timeout)

        lifecycle_data = self._build_lifecycle_data(app=app, bot=self.bot, **kwargs)
        await self.dispatcher.emit_shutdown(**lifecycle_data)

        if self.bot.session is not None:
            await self.bot.session.close()
