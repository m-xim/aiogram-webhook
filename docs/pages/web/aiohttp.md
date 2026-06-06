# aiohttp Adapter

`AiohttpAdapter` is the web-framework component for `aiohttp.web.Application`. It binds a webhook engine to an aiohttp app, registers a `POST` route, and appends engine lifecycle callbacks to `app.on_startup` and `app.on_shutdown`.

Use it when your service already uses aiohttp or when you prefer aiohttp's lower-level web primitives.

Runnable example with handlers and security: [Quick start — aiohttp](../learn/quick-start.md#minimal-app).

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

## Request mapping

| `WebRequest` property | aiohttp source |
| --- | --- |
| `raw` | `aiohttp.web.Request` |
| `client_ip` | Peer address from the request transport |
| `headers` | `request.headers` |
| `query_params` | `request.query` |
| `path_params` | `request.match_info` |
| `json()` | `await request.json()` |

{% note info %}

The adapter adds lifecycle callbacks in the order it is registered.
Register your own startup callback for `set_webhook()` before or after `engine.register(app)` depending on when you want Telegram registration to happen.

{% endnote %}

## Combining with other components

| Component | What AiohttpAdapter expects |
| --- | --- |
| Engine | Calls `register(app)` with an `aiohttp.web.Application`. |
| Route | Provides the path that becomes an aiohttp `POST` route. |
| Security | Runs inside the engine after the adapter normalizes the request. |
| Lifecycle | Uses aiohttp startup/shutdown callback lists. |
