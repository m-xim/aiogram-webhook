# Secret Token

`StaticSecretToken` verifies Telegram's `X-Telegram-Bot-Api-Secret-Token` header.

```python
from aiogram_webhook.security import Security, StaticSecretToken

security = Security(
    secret_token=StaticSecretToken("webhook-secret"),
)
```

## Token format

Telegram accepts secret tokens with:

* 1 to 256 characters;
* letters;
* digits;
* `_` and `-`.

`StaticSecretToken` validates this format at construction time.

## Incoming request check

The engine compares the incoming header with the configured token using constant-time comparison.

## Outgoing webhook registration

When a secret token provider is configured, the engine also adds `secret_token` to Telegram `setWebhook` arguments. This keeps registration and verification aligned.

