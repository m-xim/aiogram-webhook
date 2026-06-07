# Single-bot App

Project shape for one Telegram bot on one service. For the runnable example, start with [Quick start](../learn/quick-start.md); this recipe adds structure and production knobs.

## Components

| Need | Component | Guide |
| --- | --- | --- |
| One bot | `SingleBotEngine` | [SingleBotEngine](../engines/single-bot-engine.md) |
| HTTP framework | `FastAPIAdapter` or `AiohttpAdapter` | [Web adapters](../web/overview.md) |
| Public URL | `Route(base_url=..., path=...)` | [Route](../route/overview.md) |
| Request verification | `Security` | [Security](../security/overview.md) |
| Telegram delivery | `WebhookConfig` | [WebhookConfig](../other/webhook-config.md) |

## Suggested layout

```text
app/
  bot.py        # handlers, Dispatcher, Router
  web.py        # FastAPI/aiohttp app, engine wiring
  settings.py   # tokens, base_url, secrets from env
```

Wire `Bot`, `Dispatcher`, `Route`, `Security`, and the adapter once in `web.py`. Keep handlers free of HTTP details.

{% include [Security warning](../../_includes/security-warning.md) %}

## Webhook options

Add when defaults are not enough:

```python
from aiogram_webhook import WebhookConfig

webhook_config = WebhookConfig(
    allowed_updates=["message", "callback_query"],
    drop_pending_updates=True,
    max_connections=40,
)
```

| Option | Why |
| --- | --- |
| `allowed_updates` | Limits update types Telegram sends. |
| `drop_pending_updates` | Clears stale queue on deploy or first setup. |
| `max_connections` | Caps Telegram delivery concurrency. |

## Shutdown

During shutdown the engine returns `503` for new webhook requests, waits for background tasks, then closes the bot session.

{% note tip %}

Keep expensive work off the webhook path. Acknowledge Telegram quickly; use a queue or worker for long jobs. See [Dispatch Modes](../dispatch.md).

{% endnote %}
