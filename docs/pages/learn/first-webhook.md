# First Webhook

This guide turns a normal aiogram bot into a webhook application.

## 1. Create the dispatcher

```python
from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Webhook is alive")


dispatcher = Dispatcher()
dispatcher.include_router(router)
```

## 2. Choose a framework adapter

{% list tabs group=framework %}

- FastAPI

  {% include [FastAPI engine](../../_includes/fastapi-engine.md) %}

- aiohttp

  {% include [aiohttp engine](../../_includes/aiohttp-engine.md) %}

{% endlist %}

## 3. Expose a public HTTPS URL

Telegram must reach your app over HTTPS.
In development, use a tunnel or a public staging domain.
In production, put your app behind a reverse proxy or platform load balancer.

{% note warning %}

Keep `base_url` equal to the public URL Telegram can call.
Do not use `localhost` in `Route(base_url=...)` unless Telegram can really reach it.

{% endnote %}

## 4. Register the webhook

For one bot:

```python
await engine.set_webhook()
```

For token-based multi-bot applications:

```python
await engine.add_bot("123456:ABCDEF")
```

{% cut "How do I know Telegram accepted it?" %}

Telegram's `setWebhook` returns `True` through aiogram when the registration succeeds.
You can also inspect webhook state with `await bot.get_webhook_info()`.

{% endcut %}
