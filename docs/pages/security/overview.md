# Security

Security runs **after** route matching and **before** the update reaches aiogram. It is optional in code and important on any public endpoint.

{% include [Security warning](../../_includes/security-warning.md) %}

## Built-in pieces

| Component | What it checks | Details |
| --- | --- | --- |
| `StaticSecretToken` | `X-Telegram-Bot-Api-Secret-Token` header | [Secret token](secret-token.md) |
| `IPCheck` | Client IP (or first `X-Forwarded-For` hop) | [IP check](ip-check.md) |
| `Security` | Secret token first, then custom checks in order | This page |

Custom verification: [Custom checks](custom-checks.md) · per-bot secrets: [Custom secret token](custom-secret-token.md)

## Wire it once on the engine

```python
from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

security = Security(
    IPCheck(),
    secret_token=StaticSecretToken("webhook-secret"),
)

engine = SingleBotEngine(dispatcher, bot, web=adapter, route=route, security=security)
```

Pass `security` to the engine, not the adapter — verification stays independent of FastAPI, aiohttp, or a custom framework.

{% note info %}

When a secret token is configured, the engine also sends it in `setWebhook`. Registration and incoming verification stay aligned without extra configuration.

{% endnote %}

## Production hint

Combine `StaticSecretToken` with `IPCheck()` behind one `Security` instance. Tune `IPCheck` for your reverse proxy — read [IP check — Reverse proxies](ip-check.md) before trusting `X-Forwarded-For`.
