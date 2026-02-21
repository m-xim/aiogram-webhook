from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession
from pydantic import BaseModel, ConfigDict


class BotConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session: BaseSession | None = None
    """HTTP Client session (For example AiohttpSession). If not specified it will be automatically created."""
    default: DefaultBotProperties | None = None
    """Default bot properties. If specified it will be propagated into the API methods at runtime."""
