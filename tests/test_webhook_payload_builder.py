import pytest
from aiogram.methods import SendDocument, SendMessage
from aiogram.types import BufferedInputFile

from aiogram_webhook.utils._payload import build_webhook_payload
from tests.fixtures.multipart_payload import assert_attached_file, assert_payload_fields


@pytest.mark.asyncio
async def test_webhook_payload_builder_serializes_method_fields(bot):
    method = SendMessage(chat_id=42, text="OK", disable_notification=False)

    payload = build_webhook_payload(bot=bot, method=method)

    await assert_payload_fields(
        payload,
        {
            "method": "sendMessage",
            "chat_id": "42",
            "text": "OK",
            "disable_notification": "false",
        },
    )


@pytest.mark.asyncio
async def test_webhook_payload_builder_serializes_attached_file(bot):
    method = SendDocument(
        chat_id=42,
        document=BufferedInputFile(b"hello", filename="hello.txt"),
    )

    payload = build_webhook_payload(bot=bot, method=method)
    parts = await assert_payload_fields(payload, {"method": "sendDocument", "chat_id": "42"})

    assert_attached_file(parts, field="document", filename="hello.txt", body=b"hello")
