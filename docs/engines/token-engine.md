# TokenEngine

`TokenEngine` handles many bots in one application. The incoming route selects the bot, usually through a `{bot_token}` path parameter.

## When to use it

Use `TokenEngine` when:

* one service owns webhook endpoints for many bots;
* bots are added or removed dynamically;
* the bot token is part of the webhook route by design.

## Minimal setup

```python
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from aiogram_webhook import BotConfig, FastAPIAdapter, TokenEngine, WebhookConfig
from aiogram_webhook.route import BotTokenParam, Route

dispatcher = Dispatcher()

route = Route(
    base_url="https://example.com",
    path="/webhook/{bot_token}",
    params={"bot_token": BotTokenParam()},
)

engine = TokenEngine(
    dispatcher,
    web=FastAPIAdapter(),
    route=route,
    bot_config=BotConfig(default=DefaultBotProperties(parse_mode="HTML")),
    webhook_config=WebhookConfig(drop_pending_updates=True),
)
```

## Add a bot

```python
await engine.add_bot("123456:ABCDEF")
```

`add_bot()` resolves the bot ID, builds the public webhook URL, and calls Telegram `setWebhook`.

## How it combines with other parts

| Part | Typical value |
| --- | --- |
| Web | One shared adapter for all bots. |
| Route | Dynamic path with `BotTokenParam`. |
| Security | Shared `Security` policy for all incoming requests. |
| Webhook options | Engine defaults plus per-bot overrides. |

## Bot configuration

`BotConfig` controls how `TokenEngine` creates `Bot` instances for tokens.

| Field | Meaning |
| --- | --- |
| `session` | HTTP client session used by created bots. |
| `default` | Default bot properties propagated into API methods. |

Pass `session` when you want to control HTTP client configuration or share one session between bots created by `TokenEngine`.

```python
engine = TokenEngine(
    dispatcher,
    web=web,
    route=route,
    bot_config=BotConfig(
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML"),
    ),
)
```

## Telegram options

Engine-level `WebhookConfig` is the default for every bot:

```python
engine = TokenEngine(
    dispatcher,
    web=web,
    route=route,
    bot_config=BotConfig(default=None),
    webhook_config=WebhookConfig(allowed_updates=["message"]),
)
```

Override it for one bot when calling `add_bot()`:

```python
await engine.add_bot(
    "123456:ABCDEF",
    webhook_config=WebhookConfig(allowed_updates=["message", "callback_query"]),
)
```

{% note warning %}

Bot tokens may appear in access logs when they are placed in the path. Treat logs, traces, and metrics labels as sensitive.

{% endnote %}

## Startup and shutdown

During engine startup, `TokenEngine` adds known `bots` to dispatcher startup workflow data.

| Hook | What happens |
| --- | --- |
| Startup | Emits dispatcher startup with `bots`, `app`, `dispatcher`, and `webhook_engine`. |
| Shutdown | Rejects late webhook requests, drains all bot task trackers in parallel, emits dispatcher shutdown, and closes bot sessions owned by the engine. |

Register each bot from your own startup flow:

```python
async def set_webhooks(app):
    await engine.add_bot("123456:ABCDEF")
    await engine.add_bot("654321:UVWXYZ")
```

`engine.register(app)` registers the local route (with aiohttp, also wires lifecycle callbacks). For FastAPI, wrap startup in `engine.lifespan(app)` — see [FastAPI adapter](../web/fastapi.md). `engine.add_bot()` resolves the bot and calls Telegram.

### shutdown_timeout

`shutdown_timeout` controls how long the engine waits for each bot's in-flight background tasks to finish before cancelling them. Default: `10.0` seconds.

All bot trackers are drained in parallel, so total shutdown time is bounded by `shutdown_timeout` regardless of the number of bots registered.

```python
engine = TokenEngine(
    dispatcher,
    web=web,
    route=route,
    shutdown_timeout=30.0,
)
```

{% note info %}

The same timeout applies when removing a bot dynamically via `remove_bot()`.

{% endnote %}

End-to-end multi-bot layout: [Multi-bot app](../recipes/multi-bot.md).
