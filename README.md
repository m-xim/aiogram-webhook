# aiogram-webhook

[![PyPI version](https://img.shields.io/pypi/v/aiogram-webhook?color=blue)](https://pypi.org/project/aiogram-webhook)
[![License](https://img.shields.io/github/license/m-xim/aiogram-webhook.svg)](/LICENSE)
[![Tests Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Release Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/release.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/m-xim/aiogram-webhook)

**aiogram-webhook** is a modular Python library for seamless webhook integration with multiple web frameworks in aiogram. It enables both single and multi-bot operation via webhooks, with flexible routing and security features.

---

## ✨ Features

- 🧱 Modular and extensible webhook engine
- 🔀 Flexible routing (static, tokenized, custom)
- 🤖 Single-bot and multi-bot support
- ⚡ Adapters for FastAPI and aiohttp
- 🔒 Security: secret tokens, IP checks, custom security
- 🧩 Easily extendable with your own adapters, routing, and security

---

## 🚀 Installation

```bash
uv add aiogram-webhook
# or
pip install aiogram-webhook
```

---

## ⚡ Quick Start

### FastAPI
```python
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
bot = Bot("BOT_TOKEN")

engine = SimpleEngine( # or other engine
    dispatcher,
    bot,
    web_adapter=FastApiWebAdapter(),
    routing=PathRouting(url="/webhook"),
    # security=Security(...)
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
```

### Aiohttp
```python
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_webhook import SimpleEngine, FastApiWebAdapter
from aiogram_webhook.routing import PathRouting
from aiohttp import web

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("OK")

dispatcher = Dispatcher()
dispatcher.include_router(router)
bot = Bot("BOT_TOKEN")

engine = SimpleEngine( # or other engine
    dispatcher,
    bot,
    web_adapter=FastApiWebAdapter(),
    routing=PathRouting(url="/webhook"),
    # security=Security(...)
)
app = web.Application()
engine.register(app)
```

---

## 🧩 Engines

In aiogram-webhook, there are two main engines for integrating Telegram bots via webhook:

#### SimpleEngine (Single-bot)

Used for serving a single Telegram bot. Suitable for most standard scenarios when you need to integrate only one bot with your application.

- Connects aiogram `Dispatcher` and `Bot` to the selected web framework (FastAPI, aiohttp, etc.)
- Handles webhook requests for a single bot
- Requires explicit dispatcher, bot, web_adapter, and routing (security is optional)

**Example:**
```python
from aiogram import Bot, Dispatcher
from aiogram_webhook import SimpleEngine, FastApiWebAdapter
from aiogram_webhook.routing import PathRouting

bot = Bot("BOT_TOKEN")
dispatcher = Dispatcher()
engine = SimpleEngine(
    dispatcher,
    bot,
    web_adapter=FastApiWebAdapter(),
    routing=PathRouting(url="/webhook"),
    # security=Security(...)
)
```

#### TokenEngine (Multi-bot)

Allows you to serve multiple Telegram bots in a single application. Useful if you need to dynamically determine which bot the request is for (e.g., by token in the URL).

- Allows serving multiple bots via a single endpoint
- Uses the bot token for request routing
- Requires dispatcher, web_adapter, routing, bot_settings (a dict with bot settings), security (optional)

**Example:**

```python
from aiogram import Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram_webhook import TokenEngine, FastApiWebAdapter
from aiogram_webhook.routing import PathRouting

router = Router()

@router.message(Command("addbot"))
async def add_bot_handler(message: Message, command: CommandObject, webhook_engine: TokenEngine):
    token = command.args
    if not token:
        await message.answer("Use: /addbot <TOKEN>")
        return
    new_bot = await webhook_engine.set_webhook(token)
    await message.answer(f"Bot #{new_bot.id} started!")

dispatcher = Dispatcher()
dispatcher.include_router(router)

engine = TokenEngine(
    dispatcher,
    web_adapter=FastApiWebAdapter(),
    routing=PathRouting(url="/webhook/{bot_token}", param="bot_token"),
    bot_settings={"default": DefaultBotProperties(parse_mode="HTML")},
    # security=Security(...)
)
```

#### Custom Engines

You can create your own engine by inheriting from the base engine class (`BaseEngine`). This allows you to implement custom logic for webhook processing, routing, or bot management.

---

## 🔌 Adapters: FastAPI and aiohttp

Adapters connect the engine to your web framework.

### FastAPI Adapter
- Use `FastApiWebAdapter`
- Register engine in FastAPI lifespan (see Quick Start)

### Aiohttp Adapter
- Use `AiohttpWebAdapter`
- Just call `engine.register(app)`

---

## 🛣️ Routing

- **PathRouting** — static path or path with parameter (e.g. `/webhook/{bot_token}`)
- **QueryRouting** — via query parameters (e.g. `/webhook?bot_token={bot_token}`)
- **CustomRouting** — implement your own routing logic (see [routing examples](/src/aiogram_webhook/routing))

---

## 🛡️ Security

aiogram-webhook provides a flexible and extensible security system for processing webhook requests. You can use built-in mechanisms, combine them, or implement your own checks.

```python
from aiogram_webhook.security import Security, StaticSecretToken, IPCheck

security = Security(
    IPCheck(), # and other checks...
    secret_token=StaticSecretToken("YOUR_SECRET_TOKEN")
)
```

### Main features

- **SecretToken** — verification of the Telegram secret token (e.g., via the `X-Telegram-Bot-Api-Secret-Token` header).
- **IPCheck** — validation of the request source IP address (by default, official Telegram networks are supported, you can add your own addresses/networks).
- **Combining checks** — you can combine several checks (for example, SecretToken and IPCheck simultaneously).
- **Custom checks** — the ability to implement your own verification logic (e.g., by headers, parameters, etc.).

### Using SecretToken

```python
from aiogram_webhook.security import Security, StaticSecretToken

security = Security(secret_token=StaticSecretToken("SECRET_TOKEN"))
```
**StaticSecretToken** is a simple implementation of the `SecretToken` protocol that checks the provided token against a static value.

#### Creating your own SecretToken (e.g., dynamic)
You can implement your own class based on the `SecretToken` protocol. For example, you may want to:
- Store tokens in a database or environment variable
- Use different tokens for different bots
- Rotate tokens dynamically

### Using IPCheck

`IPCheck` is a security check that validates the client's IP address against allowed networks and addresses. It helps ensure that only requests from trusted sources (such as official Telegram servers or your own networks) are accepted.

**Constructor parameters:**
- `*ip_entries`: Any number of IP addresses or networks (as strings or ipaddress objects) to allow. You can specify both IPv4 and IPv6 addresses or networks.
- `include_default` (bool, default: True): If True, includes the official Telegram IP networks in the allowed list. If False, only your custom addresses/networks will be used.

You can combine as many addresses and networks as needed. The check supports both IPv4 and IPv6.

### Using a custom check
You can create your own security check by implementing the `SecurityCheck` protocol. This allows you to define custom logic for validating incoming requests based on your specific requirements.
See [checks examples](/src/aiogram_webhook/security/checks) for more details.



> aiogram-webhook — a modular library for professional Telegram bot integration via webhooks with modern Python frameworks.
