# Multi-bot App

Use this recipe when many bots share one application and each webhook URL includes a bot token. The important difference from a single-bot app is that the route selects the bot.

## Component Choices

| Need | Component |
| --- | --- |
| Many token-based bots | `TokenEngine` |
| Token in URL | `Route` with `BotTokenParam` |
| Bot creation defaults | `BotConfig` |
| Shared framework endpoint | `FastAPIAdapter` or `AiohttpAdapter` |
| Shared Telegram defaults | Engine-level `WebhookConfig` |
| Per-bot Telegram options | `add_bot(..., webhook_config=...)` |

## Route Shape

```python
from aiogram_webhook.route import BotTokenParam, Route

route = Route(
    base_url="https://example.com",
    path="/telegram/{bot_token}",
    params={"bot_token": BotTokenParam()},
)
```

The route builds URLs like:

```text
https://example.com/telegram/123456%3AABCDEF
```

## Engine Setup

```python
from aiogram import Dispatcher

from aiogram_webhook import BotConfig, FastAPIAdapter, TokenEngine, WebhookConfig
from aiogram_webhook.security import Security, StaticSecretToken

dispatcher = Dispatcher()

engine = TokenEngine(
    dispatcher,
    web=FastAPIAdapter(),
    route=route,
    bot_config=BotConfig(default=None),
    webhook_config=WebhookConfig(allowed_updates=["message"]),
    security=Security(secret_token=StaticSecretToken("webhook-secret")),
)
```

## Add Bots

```python
await engine.add_bot("123456:ABCDEF")
await engine.add_bot("654321:UVWXYZ")
```

`add_bot()` resolves the bot ID from the token, creates or reuses a `Bot`, builds the public webhook URL, and calls Telegram `setWebhook`.

## Combine Per-bot Options

```python
await engine.add_bot(
    "123456:ABCDEF",
    webhook_config=WebhookConfig(allowed_updates=["message"]),
)
```

Engine-level `WebhookConfig` is the default. Per-bot config is the override.

## Remove Bots

```python
await engine.remove_bot(
    bot_id=123456,
    delete_webhook=True,
    drop_pending_updates=True,
)
```

{% note warning %}

If `delete_webhook=False`, do not pass `drop_pending_updates`.
The engine raises `ValueError` because Telegram accepts `drop_pending_updates` only with webhook deletion.

{% endnote %}

## Operational Notes

| Topic | Recommendation |
| --- | --- |
| Token in path | Treat access logs as sensitive because token values may appear in URLs. |
| Shared session | Provide `BotConfig(session=...)` when you want to own session lifecycle. |
| Startup hooks | Dispatcher startup receives `bots`, the set of bots known at startup. |
| New bots | Bots can be created lazily on incoming requests or explicitly through `add_bot()`. |
