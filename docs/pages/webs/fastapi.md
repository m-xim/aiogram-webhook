# FastAPI Adapter

`FastAPIAdapter` is the web-framework component for FastAPI applications. It binds a webhook engine to a `FastAPI` app, registers a `POST` route, and composes engine lifecycle callbacks with the application's lifespan.

Use it when the rest of your application already lives in FastAPI or when you want FastAPI's dependency, middleware, and deployment ecosystem around aiogram.

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
    await engine.set_webhook()
    yield


app = FastAPI(lifespan=lifespan)
engine.register(app)
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

FastAPI keeps your application lifespan.
The adapter adds engine startup/shutdown through the included router, so you can keep application setup and webhook registration in the app lifespan.

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
| Lifecycle | Uses router lifespan, so application lifespan can still call `set_webhook()`. |
