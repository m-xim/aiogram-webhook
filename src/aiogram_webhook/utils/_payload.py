import secrets
from typing import TYPE_CHECKING, Any

from aiogram import Bot
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiohttp import MultipartWriter

if TYPE_CHECKING:
    from aiogram.types import InputFile


def prepare_webhook_reply(
    bot: Bot, method: TelegramMethod[TelegramType]
) -> tuple[dict[str, Any], dict[str, "InputFile"]]:
    """Convert a TelegramMethod to webhook reply fields with JSON-native values."""

    files: dict[str, InputFile] = {}
    data: dict[str, Any] = {"method": method.__api_method__}
    for key, value in method.model_dump(exclude_none=True, warnings=False).items():
        prepared_value = bot.session.prepare_value(value, bot=bot, files=files, _dumps_json=False)
        if prepared_value is None:
            continue
        data[key] = prepared_value

    return data, files


def build_multipart_payload(bot: Bot, data: dict[str, Any], files: dict[str, "InputFile"]) -> MultipartWriter:
    """Build a multipart/form-data webhook reply: `data` fields plus attached `files`."""
    writer = MultipartWriter(
        "form-data",
        boundary=f"webhookBoundary{secrets.token_urlsafe(16)}",
    )

    for key, value in data.items():
        # multipart fields are strings: same as prepare_value(..., _dumps_json=True) at the top level
        payload = writer.append(value if isinstance(value, str) else bot.session.json_dumps(value))
        payload.set_content_disposition("form-data", name=key)

    for key, value in files.items():
        file_payload = value.read(bot)
        payload = writer.append(file_payload)
        # quote_fields=False keeps non-ASCII filenames as raw UTF-8 instead of percent-encoding them.
        # "All queries must be made using UTF-8" — https://core.telegram.org/bots/api#making-requests
        # Matches aiogram's FormData(quote_fields=False).
        payload.set_content_disposition("form-data", quote_fields=False, name=key, filename=value.filename or key)

    return writer
