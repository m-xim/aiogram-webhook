import secrets
from typing import TYPE_CHECKING

from aiogram import Bot
from aiohttp import MultipartWriter, Payload

if TYPE_CHECKING:
    from aiogram.methods import TelegramMethod
    from aiogram.methods.base import TelegramType
    from aiogram.types import InputFile


def build_webhook_payload(bot: Bot, method: "TelegramMethod[TelegramType]") -> Payload:
    """Internal implementation: convert a TelegramMethod to multipart payload."""
    writer = MultipartWriter(
        "form-data",
        boundary=f"webhookBoundary{secrets.token_urlsafe(16)}",
    )

    payload = writer.append(method.__api_method__)
    payload.set_content_disposition("form-data", name="method")

    files: dict[str, InputFile] = {}
    for key, value in method.model_dump(warnings=False).items():
        prepared_value = bot.session.prepare_value(value, bot=bot, files=files)
        if prepared_value is None:
            continue
        payload = writer.append(prepared_value)
        payload.set_content_disposition("form-data", name=key)

    for key, value in files.items():
        file_payload = value.read(bot)
        payload = writer.append(file_payload)
        payload.set_content_disposition("form-data", name=key, filename=value.filename or key)

    return writer
