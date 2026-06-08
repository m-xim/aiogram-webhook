# Route Query Parameters

Query parameters are declared through `Route(query=...)`. They can be constants, repeated values, or references to parsed path parameters.

```python
from aiogram_webhook.route import BotTokenParam, Ref, Route

route = Route(
    base_url="https://example.com",
    path="/webhook/{bot_token}",
    params={"bot_token": BotTokenParam()},
    query={"token": Ref("bot_token"), "kind": ("telegram", "webhook")},
)
```

## Query values

| Value | Meaning |
| --- | --- |
| `"telegram"` | Constant string. |
| `42` | Constant integer converted to string. |
| `Ref("bot_token")` | Use a parsed path parameter value. |
| `("telegram", "webhook")` | Require repeated query parameter values. |

## Strict matching

By default, `Route.match()` ignores extra query parameters after all required values match. Enable strict mode when query parameters are part of endpoint verification.

```python
route = Route(
    base_url="https://example.com",
    path="/webhook/{bot_token}",
    params={"bot_token": BotTokenParam()},
    query={"token": Ref("bot_token")},
    strict_query=True,
)
```

With `strict_query=True`, unexpected query parameter names are rejected.

