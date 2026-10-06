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

{% note warning %}
By default, Starlette does not limit the request body size, so `request.json()` reads the whole body into memory. Always configure [security](../security/overview.md): the body is read only after verification passes. To cap the size, set a limit at your reverse proxy or use Starlette's built-in `RequestBodyLimitMiddleware` (Starlette 1.6+). More details: [starlette#3431](https://github.com/Kludex/starlette/pull/3431), [fastapi#362](https://github.com/fastapi/fastapi/issues/362).
{% endnote %}

## Returning Telegram methods

When `handle_in_background=False`, aiogram may return a `TelegramMethod`.
The adapter streams it as Telegram-compatible multipart payload when needed, including attached files.

{% note warning %}

Call `engine.register(app)` at module level, not inside a `lifespan`. FastAPI does not trigger `on_startup` / `on_shutdown` when a `lifespan` is active, so placing `register` inside one will silently skip engine startup and shutdown.

{% endnote %}

## Combining with other components

| Component | What FastAPIAdapter expects |
| --- | --- |
| Engine | Calls `register(app)` with a FastAPI app. |
| Route | Provides the path that becomes a FastAPI `POST` route. |
| Security | Runs inside the engine after the adapter normalizes the request. |
| Lifecycle | Managed by `engine.register(app)`. |
