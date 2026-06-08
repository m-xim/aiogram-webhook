# Route Path Parameters

Path parameters are named placeholders in `Route(path=...)`. They let the route build outgoing Telegram URLs and parse incoming framework path values.

```python
from aiogram_webhook.route import BotTokenParam, Route

route = Route(
    base_url="https://example.com",
    path="/webhook/{bot_token}",
    params={"bot_token": BotTokenParam()},
)
```

## Built-in parameters

| Parameter | Build value | Parse value |
| --- | --- | --- |
| `BotIdParam` | `target.bot_id` | `int(value)` |
| `BotTokenParam` | `target.bot_token` | raw string |

## Validation rules

* Every placeholder in `path` must have a matching entry in `params`.
* Unused `params` declarations are rejected.
* Repeated path placeholders are rejected.
* Missing leading slashes are normalized.

## Custom parameter

Implement `RouteParam` when the built-in parameters do not match your target model.

```python
class TenantParam:
    async def build(self, target, params):
        return params["tenant"]

    async def parse(self, value, params):
        return value.lower()
```

