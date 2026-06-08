# Custom Secret Token

`StaticSecretToken` fits a single bot or one shared secret for every bot on an endpoint. When each bot has its own secret — loaded from a database, vault, or tenant config — implement the `SecretToken` abstract base class.

## Contract

| Method | Role |
| --- | --- |
| `secret_token(target)` | Return the expected secret for this `Target` when registering the webhook. |
| `verify(target, request, route_params)` | Optional override. Default compares `X-Telegram-Bot-Api-Secret-Token` with `secret_token()` using constant-time comparison. |

Token format must follow [Telegram's rules](https://core.telegram.org/bots/api#setwebhook): 1–256 characters, only `A-Z`, `a-z`, `0-9`, `_`, `-`.

## Why subclass instead of many `Security` instances

`Security` is attached once per engine. A `SecretToken` implementation can branch on `target.bot_id` or `target.bot_token` while keeping one `Security(...)` argument and consistent `setWebhook` registration through `_build_webhook_kwargs()`.

## Example: per-bot secrets from storage

```python
from aiogram_webhook.engines.target import Target
from aiogram_webhook.security.secret_token import SecretToken


class StoredSecretToken(SecretToken):
    def __init__(self, store) -> None:
        self._store = store

    async def secret_token(self, target: Target) -> str:
        record = await self._store.get_secret(target.bot_id)
        if record is None:
            raise RuntimeError(f"No webhook secret for bot {target.bot_id}")
        return record
```

```python
from aiogram_webhook.security import IPCheck, Security

security = Security(
    IPCheck(),
    secret_token=StoredSecretToken(store),
)
```

Pass the same `security` to `SingleBotEngine`, `TokenEngine`, or a custom engine. On `set_webhook()` / `add_bot()`, the engine calls `await security.secret_token(target)` and forwards the value to Telegram.

## Verification flow

1. Engine resolves `Target` from the route.
2. `Security.verify()` runs `SecretToken.verify()` first.
3. Incoming header must match `await secret_token(target)`.
4. Custom `SecurityCheck` instances run afterward.

Override `verify()` only when you need non-header validation (for example, a signed query parameter in addition to Telegram's header). Keep constant-time comparison for secrets.

## Static vs dynamic

| Approach | Class | When |
| --- | --- | --- |
| One secret for all requests | `StaticSecretToken` | Single-bot apps, shared gateway secret. |
| Secret depends on `Target` | Custom `SecretToken` | Multi-tenant SaaS, per-bot rows in a database. |

See [Secret token](secret-token.md) for format rules and header name. See [Custom checks](custom-checks.md) for verification that is not secret-token based.
