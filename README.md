![Версия PyPI](docs/_assets/brand/banner.png)

# aiogram-веб-крючок
[![Версия PyPI](https://img.shields.io/pypi/v/aiogram-webhook?color=blue)](https://pypi.org/project/aiogram-webhook)
[![codecov](https://codecov.io/github/m-xim/aiogram-webhook/graph/badge.svg?token=H21MX17Y7D)](https://codecov.io/github/m-xim/aiogram-webhook)
[![Статус тестирования](https://github.com/m-xim/aiogram-webhook/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Статус выпуска](https://github.com/m-xim/aiogram-webhook/actions/workflows/release.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![Лицензия](https://img.shields.io/github/license/m-xim/aiogram-webhook.svg)](/LICENSE)
[![Спросите у DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/m-xim/aiogram-webhook)
[![Ерш](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

`aiogram-webhook` это модульная библиотека Python для интеграции webhook в aiogram.
Он поддерживает настройки с одним ботом и несколькими ботами на основе токенов, с построением маршрута, дополнительной проверкой запросов и адаптерами для FastAPI и aiohttp.

## Устанавливать

```bash
pip install aiogram-webhook
pip install "aiogram-webhook[fastapi]"
pip install "aiogram-webhook[aiohttp]"
```

## быстрый старт

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

Вызов `подождите, пока engine.установит_webhook()` во время запуска вашего приложения зарегистрируйте общедоступный URL-адрес webhook в Telegram.
В процессе работы введите команду `security=Безопасность(...)` для проверки запросов Telegram.

## Документация

Полная документация находится в [`доктора`](https://aiogram-webhook.m-xim.ru). Он охватывает установку, настройку FastAPI и aiohttp, маршрутизацию, безопасность, поведение в течение жизненного цикла и общедоступный API.
