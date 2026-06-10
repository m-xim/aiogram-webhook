# FastAPI Adapter

`FastAPIAdapter` is the web-framework component for FastAPI applications. It binds a webhook engine to a `FastAPI` app and registers a `POST` route.

Use it when the rest of your application already lives in FastAPI or when you want FastAPI's dependency, middleware, and deployment ecosystem around aiogram.

Runnable example with handlers and security: see **Minimal app — FastAPI** on the home page.

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

## Request mapping

| `WebRequest` property | FastAPI source |
| --- | --- |
| `raw` | `fastapi.Request` |
| `client_ip` | `request.client.host` |
| `headers` | Case-insensitive copied headers |
| `query_params` | Multi-value query mapping |
| `path_params` | `request.path_params` |
| `json()` | `await request.json()` |

## Returning Telegram methods

When `handle_in_background=False`, aiogram may return a `TelegramMethod`.
The adapter streams it as Telegram-compatible multipart payload when needed, including attached files.

{% note warning %}

`engine.register(app)` wires lifecycle through a `lifespan` context manager on an internal `APIRouter`. Due to FastAPI's behavior, **`app.on_startup` and `app.on_shutdown` handlers are not called when a `lifespan` is in use** — they are mutually exclusive. Use the `lifespan` parameter on `FastAPI(lifespan=...)` for any additional startup or shutdown logic instead.

{% endnote %}

## Combining with other components

| Component | What FastAPIAdapter expects |
| --- | --- |
| Engine | Calls `register(app)` with a FastAPI app. |
| Route | Provides the path that becomes a FastAPI `POST` route. |
| Security | Runs inside the engine after the adapter normalizes the request. |
| Lifecycle | Managed by `engine.register(app)`. |
