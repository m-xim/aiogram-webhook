# First Webhook

Deployment checklist. This page explains **why** each step matters — copy-paste code is on the [home page](../index.html).

## What changes from polling

| Part | Change |
| --- | --- |
| Handlers, routers, FSM | None — move as-is |
| Process bootstrap | Web framework + engine instead of `start_polling()` |
| Public URL | Telegram must reach HTTPS |
| `set_webhook()` | Registers that URL with Telegram |
| `Security` | Verifies incoming requests at the public endpoint |

{% note tip %}

Develop handlers with long polling locally; switch to webhooks for deployment. Only bootstrap code changes.

{% endnote %}

## 1. Handlers stay ordinary aiogram

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

## 2. Wire engine and adapter

The engine connects dispatcher, bot, adapter, route, and security in one place — copy the minimal app from the home page.

{% include [Register vs setWebhook](../_includes/register-vs-set-webhook.md) %}

Adapter-specific details: [FastAPI](../web/fastapi.md) · [aiohttp](../web/aiohttp.md)

## 3. Expose a public HTTPS URL

Telegram delivers updates only over HTTPS to an internet-reachable host.

| Environment | Typical approach |
| --- | --- |
| Local development | Tunnel (ngrok, cloudflared) or staging server |
| Production | Reverse proxy (nginx, Caddy) or platform load balancer |

`Route(base_url=...)` must match the **public** origin — scheme, host, and port if non-standard.

{% note warning %}

Do not use `http://localhost` in `base_url` unless Telegram can reach it. For local work, put the tunnel's HTTPS URL in `base_url`.

{% endnote %}

{% cut "Checklist before set_webhook()" %}

- [ ] App is running on the expected port.
- [ ] `curl -I https://your-domain/telegram/webhook` reaches the service (`405` on `GET` is fine — Telegram uses `POST`).
- [ ] TLS certificate is valid (or `WebhookConfig.certificate` is set for self-signed setups).
- [ ] `base_url` and `path` in `Route` match the URL you register.
- [ ] `Security` is configured for anything beyond a throwaway test.

{% endcut %}

## 4. Register with Telegram

Call **after** the endpoint is reachable:

```python
await engine.set_webhook()  # SingleBotEngine
await engine.add_bot("123456:ABCDEF")  # TokenEngine
```

The engine forwards `WebhookConfig` fields and the secret from `Security`, so Telegram registration and request verification stay aligned. Details: [WebhookConfig](../reference/webhook-config.md).

{% cut "How do I know Telegram accepted it?" %}

`set_webhook()` returns `True` on success. Inspect live state:

```python
info = await bot.get_webhook_info()
print(info.url, info.last_error_message)
```

Empty `url` or a set `last_error_message` means fix connectivity or TLS before debugging handlers.

{% endcut %}

## 5. Verify end-to-end

1. Send `/start` in Telegram.
2. Confirm the handler reply arrives.
3. On failure, check [Errors](../reference/errors.md) and application logs (`aiogram_webhook` logger).

Request flow diagram: [Dispatch modes](../dispatch.md#one-update-end-to-end).

## Where to go next

| Topic | Page |
| --- | --- |
| Secret token and IP checks | [Security](../security/overview.md) |
| `allowed_updates`, `drop_pending_updates` | [WebhookConfig](../reference/webhook-config.md) |
| Project file layout | [Single-bot app](../recipes/single-bot.md) |
| Several bots on one service | [Multi-bot app](../recipes/multi-bot.md) |
