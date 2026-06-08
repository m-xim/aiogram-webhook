# FastAPI Adapter

`FastAPIAdapter` is the web-framework component for FastAPI applications. It binds a webhook engine to a `FastAPI` app and registers a `POST` route. Engine lifecycle is managed separately via `engine.lifespan(app)` inside the application's lifespan function.

Use it when the rest of your application already lives in FastAPI or when you want FastAPI's dependency, middleware, and deployment ecosystem around aiogram.

Runnable example with handlers and security: see **Minimal app — FastAPI** on the home page.

```python
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine.register(app)
    async with engine.lifespan(app):
        await engine.set_webhook()
        yield


app = FastAPI(lifespan=lifespan)
```

## Request mapping

| `WebRequest` property | FastAPI source |
| --- | --- |
| `raw` | `fastapi.Request` |
| `client_ip` | `request.client.host` |
| `headers` | Case-insensitive copied headers |
| `query_params` | Multi-value query mapping |
| `path_params` | `request.path_params` |
| `json()` | `await request.json()` |

{% note tip %}

FastAPI does not wire engine lifecycle through `register()`.
Use `engine.lifespan(app)` as an async context manager inside the application lifespan to run engine startup and shutdown in the correct order.

{% endnote %}

## Returning Telegram methods

When `handle_in_background=False`, aiogram may return a `TelegramMethod`.
The adapter streams it as Telegram-compatible multipart payload when needed, including attached files.

## Combining with other components

| Component | What FastAPIAdapter expects |
| --- | --- |
| Engine | Calls `register(app)` with a FastAPI app. |
| Route | Provides the path that becomes a FastAPI `POST` route. |
| Security | Runs inside the engine after the adapter normalizes the request. |
| Lifecycle | Use `engine.lifespan(app)` inside your app lifespan; call `set_webhook()` after entering it. |
