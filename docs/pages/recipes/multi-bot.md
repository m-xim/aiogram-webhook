# Multi-bot App

Project shape when many bots share one service and each webhook URL carries a bot token.

Component deep dive: [TokenEngine](../engines/token-engine.md). Runnable pieces: combine [First webhook](../learn/first-webhook.md) wiring with the route and `add_bot()` calls below.

## Components

| Need | Component | Guide |
| --- | --- | --- |
| Many token-based bots | `TokenEngine` | [TokenEngine](../engines/token-engine.md) |
| Token in URL | `Route` + `BotTokenParam` | [Route](../route/overview.md) |
| Bot creation defaults | `BotConfig` | [TokenEngine](../engines/token-engine.md#bot-configuration) |
| Shared Telegram defaults | Engine-level `WebhookConfig` | [WebhookConfig](../other/webhook-config.md) |
| Per-bot overrides | `add_bot(..., webhook_config=...)` | [TokenEngine](../engines/token-engine.md#telegram-options) |

## Route

```python
from aiogram_webhook.route import BotTokenParam, Route

route = Route(
    base_url="https://example.com",
    path="/telegram/{bot_token}",
    params={"bot_token": BotTokenParam()},
)
```

Built URL example: `https://example.com/telegram/123456%3AABCDEF`

## Register bots at startup

```python
async def on_startup(app):
    await engine.add_bot("123456:ABCDEF")
    await engine.add_bot("654321:UVWXYZ")
```

`add_bot()` creates or reuses a `Bot`, builds the public URL, and calls Telegram `setWebhook`.

## Operations

| Topic | Note |
| --- | --- |
| Tokens in paths | Treat access logs and metrics as sensitive. |
| Shared session | Pass `BotConfig(session=...)` to own HTTP client lifecycle. |
| Removing a bot | `remove_bot(bot_id, delete_webhook=True)` — see [TokenEngine](../engines/token-engine.md). |

{% note warning %}

If `delete_webhook=False`, do not pass `drop_pending_updates`. Telegram accepts that flag only when deleting a webhook.

{% endnote %}
