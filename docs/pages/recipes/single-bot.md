# Single-bot App

Use this recipe when one deployed service handles one Telegram bot. The component choice is simple: one engine, one route, one adapter, and one bot.

## Component Choices

| Need | Component |
| --- | --- |
| One configured bot | `SingleBotEngine` |
| FastAPI endpoint | `FastAPIAdapter` |
| Public webhook URL | `Route(base_url=..., path=...)` |
| Telegram request verification | `Security` with `StaticSecretToken` |
| Telegram delivery options | `WebhookConfig` |

## Application Layout

```text
app/
  bot.py
  web.py
  settings.py
```

The important part is that the `Bot`, `Dispatcher`, `Route`, `Security`, and adapter are wired once.

{% include [Security warning](../../_includes/security-warning.md) %}

## FastAPI Example

{% include [FastAPI engine](../../_includes/fastapi-engine.md) %}

## Add Webhook Options

```python
from aiogram_webhook import WebhookConfig

webhook_config = WebhookConfig(
    allowed_updates=["message", "callback_query"],
    drop_pending_updates=True,
    max_connections=40,
)
```

| Option | Why it matters |
| --- | --- |
| `allowed_updates` | Limits the update types Telegram sends. |
| `drop_pending_updates` | Drops old queued updates during deployment or first setup. |
| `max_connections` | Controls Telegram delivery concurrency. |

## Shutdown Behavior

During shutdown the engine rejects new webhook requests with `503`.
Background tasks are closed before the bot session is closed.

{% note tip %}

Keep long-running work outside the webhook request path.
Acknowledge Telegram quickly, then use queues or background workers for expensive jobs.

{% endnote %}
