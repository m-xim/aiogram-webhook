from aiogram_webhook.configs.bot import BotConfig
from aiogram_webhook.configs.webhook import WebhookConfig
from aiogram_webhook.engines.single import SingleBotEngine
from aiogram_webhook.engines.token import TokenEngine
from aiogram_webhook.web.aiohttp import AiohttpAdapter

__all__ = ["AiohttpAdapter", "BotConfig", "SingleBotEngine", "TokenEngine", "WebhookConfig"]


try:
    from aiogram_webhook.web.fastapi import FastAPIAdapter  # noqa: F401

    __all__.insert(2, "FastAPIAdapter")
except ModuleNotFoundError as exc:
    if exc.name != "fastapi":
        raise
