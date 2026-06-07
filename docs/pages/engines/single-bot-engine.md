# SingleBotEngine

Handles one configured `Bot`. Every accepted webhook request dispatches to that instance.

## When to use

* One deployed application serves one Telegram bot.
* The webhook URL does not need to identify which bot to use.
* You want the simplest production path.

For several bots identified by URL token, use [TokenEngine](token-engine.md).

## Setup

```python
from aiogram import Bot, Dispatcher

from aiogram_webhook import FastAPIAdapter, SingleBotEngine, WebhookConfig
from aiogram_webhook.route import Route

dispatcher = Dispatcher()
bot = Bot("BOT_TOKEN")

engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=Route(base_url="https://example.com", path="/webhook"),
    webhook_config=WebhookConfig(drop_pending_updates=True),
)
```

Full example with handlers and security: see **Minimal app** on the home page.

## Typical pairing

| Part | Value |
| --- | --- |
| Route | Static path, e.g. `/webhook` |
| Security | `StaticSecretToken` + `IPCheck` in production |
| WebhookConfig | One shared config for the bot |

{% include [Register vs setWebhook](../../_includes/register-vs-set-webhook.md) %}

## Telegram options

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    webhook_config=WebhookConfig(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    ),
)
```

Field reference: [WebhookConfig](../other/webhook-config.md).

## Lifecycle

| Phase | Behavior |
| --- | --- |
| Startup | `emit_startup` with `bot`, `app`, `dispatcher`, `webhook_engine` in workflow data |
| Shutdown | Rejects new requests (`503`), drains background tasks, `emit_shutdown`, closes bot session |

### shutdown_timeout

`shutdown_timeout` controls how long the engine waits for in-flight background tasks to finish before cancelling them. Default: `10.0` seconds.

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    shutdown_timeout=30.0,
)
```

{% note tip %}

Increase `shutdown_timeout` when handlers do slow work such as external API calls or file uploads. Decrease it when fast process exit matters more than draining every in-flight task.

{% endnote %}

Background dispatch and `handle_in_background`: [Dispatch Modes](../dispatch.md).
