from dataclasses import dataclass

from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession


@dataclass
class BotConfig:
    session: BaseSession | None = None
    """HTTP Client session (For example AiohttpSession). If not specified it will be automatically created."""
    default: DefaultBotProperties | None = None
    """Default bot properties. If specified it will be propagated into the API methods at runtime."""
