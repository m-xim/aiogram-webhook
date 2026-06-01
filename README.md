# aiogram-webhook

[![PyPI version](https://img.shields.io/pypi/v/aiogram-webhook?color=blue)](https://pypi.org/project/aiogram-webhook)
[![Tests Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![License](https://img.shields.io/github/license/m-xim/aiogram-webhook.svg)](/LICENSE)

`aiogram-webhook` is a small typed library for running aiogram bots through Telegram webhooks.
It provides webhook engines for single-bot and token-based multi-bot applications, route builders, optional request checks, and adapters for FastAPI and aiohttp.

## Install

```bash
pip install aiogram-webhook
pip install "aiogram-webhook[fastapi]"
pip install "aiogram-webhook[aiohttp]"
```

## Quick Start

```python
from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from aiogram_webhook import FastAPIAdapter, SingleBotEngine
from aiogram_webhook.route import Route

dispatcher = Dispatcher()
bot = Bot("BOT_TOKEN")

engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=Route(base_url="https://example.com", path="/webhook"),
)

app = FastAPI()
engine.register(app)
```

Call `await engine.set_webhook()` during your application startup to register the public webhook URL in Telegram.
For production, pass `security=Security(...)` to verify Telegram requests.

## Documentation

The full documentation is in [`docs`](docs). It covers installation, FastAPI and aiohttp setup, routing, security, lifecycle behavior, and the public API.
