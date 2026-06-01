# Quick Start

This page installs `aiogram-webhook` and shows the shortest useful setup for a single bot.

## Install

`aiogram-webhook` requires Python 3.10 or newer and aiogram 3.14 or newer.

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


## Optional extras

| Extra | Installs | Use it when |
| --- | --- | --- |
| `fastapi` | FastAPI integration dependencies | Your webhook endpoint is served by a FastAPI application. |
| `aiohttp` | aiohttp integration dependencies | Your webhook endpoint is served by an aiohttp application. |
| none | Core aiogram webhook logic | You write your own `WebAdapter` or only use shared route/security helpers. |

{% note info %}

`FastAPIAdapter` is exported from `aiogram_webhook` only when FastAPI is installed.
`AiohttpAdapter` is always importable because aiohttp is already used by aiogram's default HTTP session.

{% endnote %}

## Minimal app

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

## What the engine does

1. Registers a `POST` endpoint in the selected web framework.
2. Matches path and query parameters with `Route`.
3. Resolves the bot target.
4. Runs security checks when configured.
5. Parses Telegram's update JSON.
6. Feeds the update into the aiogram `Dispatcher`.
7. Returns either an empty `200` JSON response or a Telegram method payload.

{% cut "When should I call set_webhook?" %}

Call `set_webhook()` from your application startup code after the public URL is reachable.
For `SingleBotEngine`, this method is available directly on the engine.
For `TokenEngine`, call `add_bot(token)` for every bot you want to register; it creates or reuses a `Bot`, builds its URL, and calls Telegram's `setWebhook`.

{% endcut %}
