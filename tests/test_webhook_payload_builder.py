import json

import pytest
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import SendDocument, SendMessage
from aiogram.types import BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram_webhook.utils._payload import build_multipart_payload, prepare_webhook_reply
from tests.fixtures.multipart_payload import assert_attached_file, assert_payload_fields


def test_prepare_webhook_reply_returns_json_native_fields_without_files(bot):
    method = SendMessage(chat_id=42, text="OK", disable_notification=False)

    data, files = prepare_webhook_reply(bot=bot, method=method)

    assert files == {}
    assert data == {"method": "sendMessage", "chat_id": 42, "text": "OK", "disable_notification": False}


def test_prepare_webhook_reply_keeps_nested_objects_and_unicode(bot):
    method = SendMessage(
        chat_id=42,
        text="Привет",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="a", callback_data="b")]]),
    )

    data, _ = prepare_webhook_reply(bot=bot, method=method)

    assert data == {
        "method": "sendMessage",
        "chat_id": 42,
        "text": "Привет",
        "reply_markup": {"inline_keyboard": [[{"text": "a", "callback_data": "b"}]]},
    }


def test_prepare_webhook_reply_applies_bot_defaults(bot_token):
    bot = Bot(bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    data, _ = prepare_webhook_reply(bot=bot, method=SendMessage(chat_id=42, text="OK"))

    assert data["parse_mode"] == "HTML"


def test_prepare_webhook_reply_collects_files(bot):
    method = SendDocument(chat_id=42, document=BufferedInputFile(b"hello", filename="hello.txt"))

    data, files = prepare_webhook_reply(bot=bot, method=method)

    assert len(files) == 1
    assert data["document"] == f"attach://{next(iter(files))}"


@pytest.mark.asyncio
async def test_multipart_payload_serializes_attached_file(bot):
    method = SendDocument(
        chat_id=42,
        document=BufferedInputFile(b"hello", filename="hello.txt"),
    )

    data, files = prepare_webhook_reply(bot=bot, method=method)
    payload = build_multipart_payload(bot=bot, data=data, files=files)
    parts = await assert_payload_fields(payload, {"method": "sendDocument", "chat_id": "42"})

    assert_attached_file(parts, field="document", filename="hello.txt", body=b"hello")


@pytest.mark.asyncio
async def test_multipart_payload_serializes_fields_as_strings(bot):
    method = SendDocument(
        chat_id=42,
        document=BufferedInputFile(b"hello", filename="hello.txt"),
        caption="Привет",
        disable_notification=False,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="a", callback_data="b")]]),
    )

    data, files = prepare_webhook_reply(bot=bot, method=method)
    payload = build_multipart_payload(bot=bot, data=data, files=files)
    parts = await assert_payload_fields(
        payload,
        {
            "method": "sendDocument",
            "chat_id": "42",
            "caption": "Привет",
            "disable_notification": "false",
        },
    )

    reply_markup = next(part for part in parts if part.name == "reply_markup")
    assert json.loads(reply_markup.body) == {"inline_keyboard": [[{"text": "a", "callback_data": "b"}]]}
