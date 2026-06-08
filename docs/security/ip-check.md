# IP Check

`IPCheck` allows requests only from configured IP addresses or networks.

```python
from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

security = Security(
    IPCheck(),
    secret_token=StaticSecretToken("webhook-secret"),
)
```

## Default Telegram networks

By default, `IPCheck()` includes Telegram's IPv4 networks:

| Network |
| --- |
| `149.154.160.0/20` |
| `91.108.4.0/22` |

## Add trusted addresses

```python
security = Security(
    IPCheck("10.0.0.0/8", "127.0.0.1"),
)
```

Pass `include_default=False` when you want to provide the whole allowlist yourself.

## Reverse proxies

`IPCheck` reads the first value from `X-Forwarded-For` when the header is present. Only trust this header when your reverse proxy overwrites or sanitizes it before requests reach the application.

