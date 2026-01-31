from aiogram_webhook.adapters.aiohttp import AiohttpWebAdapter
from aiogram_webhook.adapters.base import WebAdapter
from aiogram_webhook.engines.simple import SimpleEngine
from aiogram_webhook.engines.token import TokenEngine

__all__ = ["SimpleEngine", "TokenEngine", "WebAdapter"]


try:
    from aiogram_webhook.adapters.aiohttp import AiohttpWebAdapter  # noqa: F401

    __all__.insert(0, "AiohttpWebAdapter")
except ImportError:
    pass

try:
    from aiogram_webhook.adapters.fastapi import FastApiWebAdapter  # noqa: F401

    __all__.insert(1, "FastApiWebAdapter")
except ImportError:
    pass
