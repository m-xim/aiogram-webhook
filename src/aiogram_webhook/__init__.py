from aiogram_webhook.adapters.base import WebAdapter
from aiogram_webhook.engines.simple import SimpleEngine
from aiogram_webhook.engines.token import TokenEngine

__all__ = ["SimpleEngine", "TokenEngine", "WebAdapter"]

try:
    from aiogram_webhook.adapters.fastapi import FastApiWebAdapter  # noqa: F401

    __all__.insert(0, "FastApiWebAdapter")
except ImportError:
    pass
