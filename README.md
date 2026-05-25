# aiogram-webhook

[![PyPI version](https://img.shields.io/pypi/v/aiogram-webhook?color=blue)](https://pypi.org/project/aiogram-webhook)
[![codecov](https://codecov.io/github/m-xim/aiogram-webhook/graph/badge.svg?token=H21MX17Y7D)](https://codecov.io/github/m-xim/aiogram-webhook)
[![Tests Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Release Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/release.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![License](https://img.shields.io/github/license/m-xim/aiogram-webhook.svg)](/LICENSE)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/m-xim/aiogram-webhook)

**aiogram-webhook** is a modular Python library for webhook integration in aiogram.
It supports single-bot and token-based multi-bot setups, with route building, optional request checks, and adapters for FastAPI and aiohttp.

## ✨ Features

- 🤖 Single-bot and token-based multi-bot webhook engines
- ⚡ FastAPI and aiohttp adapters
- 🛣️ Route building with path and query parameters
- 🛡️ Optional secret-token and IP-based request checks
- 🧩 Typed adapter interfaces for web frameworks

## 📦 Installation

```bash
uv add "aiogram-webhook"
# or
pip install "aiogram-webhook"
```

## 🚀 Quick Start

```python
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fastapi import FastAPI

from aiogram_webhook import FastAPIAdapter, SingleBotEngine, WebhookConfig
from aiogram_webhook.route import Route

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
    route=Route(base_url="https://example.com", path="/webhook"),
    webhook_config=WebhookConfig(drop_pending_updates=True),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await engine.set_webhook()
    await engine.on_startup(app)
    try:
        yield
    finally:
        await engine.on_shutdown(app)


app = FastAPI(lifespan=lifespan)
engine.register(app)
```

## 🌐 aiohttp

```python
from aiohttp import web
from aiogram import Bot, Dispatcher

from aiogram_webhook import AiohttpAdapter, SingleBotEngine
from aiogram_webhook.route import Route

dispatcher = Dispatcher()
bot = Bot("BOT_TOKEN")

engine = SingleBotEngine(
    dispatcher,
    bot,
    web=AiohttpAdapter(),
    route=Route(base_url="https://example.com", path="/webhook"),
)


async def set_webhook(app: web.Application) -> None:
    await engine.set_webhook()


app = web.Application()
app.on_startup.append(set_webhook)
engine.register(app)
```

## 🔀 Multi-Bot Webhooks

Use `TokenEngine` when the bot token is part of the webhook route:

```python
from aiogram import Dispatcher

from aiogram_webhook import FastAPIAdapter, TokenEngine
from aiogram_webhook.route import BotTokenParam, Route

dispatcher = Dispatcher()
engine = TokenEngine(
    dispatcher,
    web=FastAPIAdapter(),
    route=Route(
        base_url="https://example.com",
        path="/webhook/{bot_token}",
        params={"bot_token": BotTokenParam()},
    ),
)
```

Then call `await engine.add_bot(token)` to register a bot and set its webhook.

## 🛡️ Security

Security checks are optional. `IPCheck` allows requests from Telegram IP ranges by default:

```python
from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

security = Security(IPCheck(), secret_token=StaticSecretToken("WEBHOOK_SECRET"))
```

Pass it to an engine with `security=security`.
