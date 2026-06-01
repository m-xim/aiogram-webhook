# Telegram Options

`WebhookConfig` stores Telegram `setWebhook` options. The route decides where Telegram sends updates; `WebhookConfig` decides how Telegram sends them.

Only explicitly configured fields are sent to Telegram.

```python
from aiogram_webhook import WebhookConfig

config = WebhookConfig(
    allowed_updates=["message", "callback_query"],
    drop_pending_updates=True,
    max_connections=40,
)
```

## Fields

| Field | Telegram meaning | When to set it |
| --- | --- | --- |
| `certificate` | Upload public key certificate for self-signed HTTPS. | Self-signed certificate setups. |
| `ip_address` | Fixed IP address Telegram should use for webhook requests. | DNS is not the source of truth for your endpoint. |
| `max_connections` | Maximum simultaneous HTTPS connections from Telegram. | You want to tune delivery concurrency. |
| `allowed_updates` | Update types Telegram should send. | Production bots that do not need every update type. |
| `drop_pending_updates` | Drop pending updates while setting the webhook. | First deploys, migrations, or deliberate queue resets. |

{% note info %}

If security has a secret-token provider, the engine adds `secret_token` to Telegram `setWebhook` arguments automatically.

{% endnote %}

## Where options are applied

| Engine | How options are used |
| --- | --- |
| `SingleBotEngine` | Pass `webhook_config` to the engine. `set_webhook()` uses it for the single bot. |
| `TokenEngine` | Pass engine defaults through `webhook_config`; override per bot in `add_bot(..., webhook_config=...)`. |

See the engine pages for concrete setup examples.
