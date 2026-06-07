# Quick Start

Copy-paste path from zero to a running webhook app. For the mental model and request diagram, read [What is aiogram-webhook?](overview.md) first.

## Before you start

| Requirement | Details |
| --- | --- |
| Python | 3.10 or newer |
| aiogram | 3.14 or newer (installed with the package) |
| Bot token | From [@BotFather](https://t.me/BotFather) |
| Public HTTPS URL | Required before `set_webhook()` — use a tunnel locally |

Pick the framework tab that matches your project.

## Install

{% list tabs group=package-manager %}
- pip
  ```bash
  pip install aiogram-webhook
  pip install "aiogram-webhook[fastapi]"
  pip install "aiogram-webhook[aiohttp]"
  ```

- uv
  ```bash
  uv add aiogram-webhook
  uv add "aiogram-webhook[fastapi]"
  uv add "aiogram-webhook[aiohttp]"
  ```
{% endlist %}

| Extra | Use when |
| --- | --- |
| `fastapi` | Webhook endpoint lives in a FastAPI app. |
| `aiohttp` | Webhook endpoint lives in an aiohttp app. |
| none | You build a [custom adapter](../web/custom.md) or use route/security helpers only. |

{% note info %}

`FastAPIAdapter` imports from `aiogram_webhook` only when FastAPI is installed. `AiohttpAdapter` is always available — aiohttp is already used by aiogram's default HTTP session.

{% endnote %}

## Minimal app

Replace `BOT_TOKEN`, `https://example.com`, and `webhook-secret`. `base_url` must be the HTTPS origin Telegram can reach.

{% include [Security warning](../../_includes/security-warning.md) %}

{% list tabs group=framework %}

- FastAPI

  ```python
  from contextlib import asynccontextmanager

  from aiogram import Bot, Dispatcher, Router
  from aiogram.filters import CommandStart
  from aiogram.types import Message
  from fastapi import FastAPI

  from aiogram_webhook import FastAPIAdapter, SingleBotEngine, WebhookConfig
  from aiogram_webhook.route import Route
  from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

  router = Router()


  @router.message(CommandStart())
  async def start(message: Message) -> None:
      await message.answer("OK")


  dispatcher = Dispatcher()
  dispatcher.include_router(router)

  bot = Bot("BOT_TOKEN")
  engine = SingleBotEngine(
      dispatcher,
      bot,
      web=FastAPIAdapter(),
      route=Route(base_url="https://example.com", path="/telegram/webhook"),
      security=Security(IPCheck(), secret_token=StaticSecretToken("webhook-secret")),
      webhook_config=WebhookConfig(drop_pending_updates=True),
  )


  @asynccontextmanager
  async def lifespan(app: FastAPI):
      await engine.set_webhook()
      yield


  app = FastAPI(lifespan=lifespan)
  engine.register(app)
  ```

- aiohttp

  ```python
  from aiohttp import web
  from aiogram import Bot, Dispatcher, Router
  from aiogram.filters import CommandStart
  from aiogram.types import Message

  from aiogram_webhook import AiohttpAdapter, SingleBotEngine, WebhookConfig
  from aiogram_webhook.route import Route
  from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

  router = Router()


  @router.message(CommandStart())
  async def start(message: Message) -> None:
      await message.answer("OK")


  dispatcher = Dispatcher()
  dispatcher.include_router(router)

  bot = Bot("BOT_TOKEN")
  engine = SingleBotEngine(
      dispatcher,
      bot,
      web=AiohttpAdapter(),
      route=Route(base_url="https://example.com", path="/telegram/webhook"),
      security=Security(IPCheck(), secret_token=StaticSecretToken("webhook-secret")),
      webhook_config=WebhookConfig(drop_pending_updates=True),
  )


  async def set_webhook(app: web.Application) -> None:
      await engine.set_webhook()


  app = web.Application()
  app.on_startup.append(set_webhook)
  engine.register(app)
  ```

{% endlist %}

## What happens at runtime

When a user sends `/start`:

1. Telegram `POST`s JSON to your public URL.
2. Security checks the secret token and source IP.
3. The engine feeds the update to aiogram in the background.
4. Your handler calls `message.answer("OK")` through the Bot API.
5. Telegram gets an empty `200` from the webhook request itself.

Step 4 is a separate HTTP call — normal for [background mode](../dispatch.md). Full sequence diagram: [What is aiogram-webhook?](overview.md#one-update-end-to-end).

{% include [Register vs setWebhook](../../_includes/register-vs-set-webhook.md) %}

## Next steps

| Goal | Page |
| --- | --- |
| Deploy behind HTTPS, verify Telegram accepted the URL | [First webhook](first-webhook.md) |
| Understand one component | [Guide: Web adapters](../web/overview.md), [Engines](../engines/overview.md), [Route](../route/overview.md), [Security](../security/overview.md) |
| Production project layout | [Single-bot app](../recipes/single-bot.md) |
| HTTP `403` / `404` / `503` | [Errors](../other/errors.md) |
