from abc import ABC
from collections.abc import Iterable, Mapping
from types import MappingProxyType
from typing import Any, Generic

from aiogram import Bot

from aiogram_webhook import WebhookConfig
from aiogram_webhook.engines.base import AppT, BaseWebhookEngine, FrameworkResponseT, RawRequestT, logger
from aiogram_webhook.engines.target import Target
from aiogram_webhook.route import Route
from aiogram_webhook.security import Security
from aiogram_webhook.tasks import TaskTracker
from aiogram_webhook.utils.config import dataclass_config_to_kwargs
from aiogram_webhook.web.base import WebAdapter


class BaseMultiBotEngine(
    BaseWebhookEngine[AppT, RawRequestT, FrameworkResponseT], ABC, Generic[AppT, RawRequestT, FrameworkResponseT]
):
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
        shutdown_timeout: float = 10.0,
    ) -> None:
        self._task_trackers: dict[int, TaskTracker] = {}
        self._bots: dict[int, Bot] = {}
        self.webhook_config = webhook_config or WebhookConfig()
        super().__init__(
            dispatcher,
            web=web,
            route=route,
            security=security,
            handle_in_background=handle_in_background,
            shutdown_timeout=shutdown_timeout,
        )

    async def _build_webhook_kwargs(
        self, target: Target, webhook_config: WebhookConfig | None = None
    ) -> dict[str, Any]:
        kwargs = dataclass_config_to_kwargs(self.webhook_config, webhook_config)
        if self.security is not None:
            secret_token = await self.security.secret_token(target)
            if secret_token is not None:
                kwargs["secret_token"] = secret_token
        return kwargs

    @property
    def bots(self) -> Mapping[int, Bot]:
        return MappingProxyType(self._bots)

    async def _on_startup(self, app: AppT, *args: Any, bots: Iterable[Bot] | None = None, **kwargs: Any) -> None:  # noqa: ARG002
        all_bots = set(self.bots.values())

        if bots is not None:
            all_bots |= set(bots)

        logger.info("Starting multi-bot webhook engine with %s bot(s)", len(all_bots))
        lifecycle_data = self._build_lifecycle_data(app=app, bots=all_bots, **kwargs)
        await self.dispatcher.emit_startup(**lifecycle_data)

    def _get_task_tracker(self, bot: Bot) -> TaskTracker:
        tracker = self._task_trackers.get(bot.id)

        if tracker is None:
            tracker = TaskTracker()
            self._task_trackers[bot.id] = tracker

        return tracker
