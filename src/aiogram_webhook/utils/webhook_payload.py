from typing import TYPE_CHECKING, Any

from aiogram import Bot
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType

if TYPE_CHECKING:
    from aiogram.types import InputFile


def build_webhook_payload(bot: Bot, method: TelegramMethod[TelegramType]) -> dict[str, Any] | None:
    """
    Convert TelegramMethod to webhook response payload.

    See: https://core.telegram.org/bots/faq#how-can-i-make-requests-in-response-to-updates
    """
    files: dict[str, InputFile] = {}
    params: dict[str, Any] = {}
    for k, v in method.model_dump(warnings=False).items():
        pv = bot.session.prepare_value(v, bot=bot, files=files)
        # New files detected — can't use webhook response
        if files:
            return None
        if pv is not None:
            params[k] = pv
    return {"method": method.__api_method__, **params}
