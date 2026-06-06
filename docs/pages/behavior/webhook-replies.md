# Webhook Replies

Telegram allows a bot to return one API method directly as the webhook HTTP response. `aiogram-webhook` supports this when foreground handling is enabled.

## Enable foreground handling

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    handle_in_background=False,
)
```

When a handler returns a `TelegramMethod`, the engine asks the web adapter to create a Telegram-compatible payload response.

## Example handler

```python
from aiogram.methods import SendMessage
from aiogram.types import Message


@router.message()
async def echo(message: Message):
    return SendMessage(chat_id=message.chat.id, text=message.text)
```

## When not to use it

Avoid webhook replies when handlers do slow work, call external services, or need predictable background task isolation. Background handling is the safer default for most applications.

