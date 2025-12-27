# aiogram-webhook

[![PyPI version](https://img.shields.io/pypi/v/aiogram-webhook?color=blue)](https://pypi.org/project/aiogram-webhook)
[![License](https://img.shields.io/github/license/m-xim/aiogram-webhook.svg)](/LICENSE)
[![Tests Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Release Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/release.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/m-xim/aiogram-webhook)

**aiogram-webhook** is a Python library for seamless webhook integration with multiple web frameworks in aiogram. It enables both single and multi-bot operation via webhooks, with flexible routing and security features.

<br>

## ✨ Features

- 🧱 Modular and extensible webhook engine
- 🔀 Flexible routing (static and token-based)
- 🤖 Supports single and multi-bot setups
- ⚡ FastAPI adapters out of the box
- 🔒 Security best practices: secret tokens, IP checks
- 🧩 Easy to extend with custom adapters and routing

## 🚀 Installation

```bash
uv add aiogram-webhook
# or
pip install aiogram-webhook
```

## ⚡ Quick Start

### Single Bot Example (FastAPI)
```python
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_webhook import SimpleEngine, FastApiWebAdapter
from aiogram_webhook.routing import PathRouting

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("OK")

dispatcher = Dispatcher()
dispatcher.include_router(router)
bot = Bot("BOT_TOKEN_HERE")

engine = SimpleEngine(
    dispatcher,
    bot,
    web_adapter=FastApiWebAdapter(),
    routing=PathRouting(url="/webhook"),
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine.register(app)
    await engine.set_webhook(
        drop_pending_updates=True,
        allowed_updates=("message", "callback_query"),
    )
    await engine.on_startup()
    yield
    await engine.on_shutdown()

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
```

### Multi-Bot Example (FastAPI)
Each bot is configured in Telegram with its own webhook URL: `https://example.com/webhook/<BOT_TOKEN>`

```python
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_webhook import TokenEngine, FastApiWebAdapter
from aiogram_webhook.routing import PathRouting

dispatcher = Dispatcher()
engine = TokenEngine(
    dispatcher,
    web_adapter=FastApiWebAdapter(),
    routing=PathRouting(url="/webhook/{bot_token}", param="bot_token"),
    bot_settings={
        "default": DefaultBotProperties(parse_mode="HTML"),
    },
)
```

Usage is the same:
```python
engine.register(app)
await engine.set_webhook(...)
await engine.on_startup()
await engine.on_shutdown()
```

## 🛣️ Routing

`PathRouting` defines where Telegram sends updates:

- **Static path:**
    ```python
  PathRouting(url="/webhook")
  ```
- **Token-based path:**
  ```python
  PathRouting(url="/webhook/{bot_token}", param="bot_token")
  ```

## 🛡️ Security
writings...
