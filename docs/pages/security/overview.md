# Security

Security is the request gate between route matching and dispatcher execution. It is optional in code and important in production.

The engine calls `Security.verify()` after a route target is resolved and before the update is dispatched.

{% include [Security warning](../../_includes/security-warning.md) %}

## Built-in checks

| Component | Checks | Best for |
| --- | --- | --- |
| `StaticSecretToken` | Telegram's `X-Telegram-Bot-Api-Secret-Token` header. | Verifying that Telegram knows the shared secret. |
| `IPCheck` | The client IP address or the first address from `X-Forwarded-For`. | Restricting callers to Telegram or trusted proxy networks. |
| `Security` | Runs secret-token verification first, then custom checks in order. | Combining multiple checks behind one engine argument. |

```python
from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

security = Security(
    IPCheck(),
    secret_token=StaticSecretToken("webhook-secret"),
)
```

Pass it to an engine:

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=route,
    security=security,
)
```

## Secret token

`StaticSecretToken` validates Telegram-compatible token format:

* 1 to 256 characters.
* Only letters, digits, `_`, and `-`.

When a secret token is configured, `_build_webhook_kwargs()` also passes it to Telegram's `setWebhook`.
That keeps outgoing registration and incoming verification aligned.

## IP check

`IPCheck()` includes Telegram's default IPv4 networks:

| Network |
| --- |
| `149.154.160.0/20` |
| `91.108.4.0/22` |

Add your reverse proxy or private test addresses when needed:

```python
security = Security(
    IPCheck("10.0.0.0/8", "127.0.0.1"),
    secret_token=StaticSecretToken("webhook-secret"),
)
```

{% note warning "Reverse proxies" %}

`IPCheck` trusts the first `X-Forwarded-For` address when that header is present.
Only rely on it when your proxy overwrites or sanitizes the header before the request reaches the application.

{% endnote %}

## Custom checks

A custom check implements the `SecurityCheck` protocol.

```python
class HeaderCheck:
    async def verify(self, target, request, route_params) -> bool:
        return request.headers.get("X-App-Webhook") == "enabled"
```

```python
security = Security(HeaderCheck())
```

## Combining with engines

Security is passed to the engine, not to the adapter:

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=route,
    security=Security(
        IPCheck(),
        secret_token=StaticSecretToken("webhook-secret"),
    ),
)
```

That keeps the verification policy independent from FastAPI, aiohttp, or any custom framework adapter.
