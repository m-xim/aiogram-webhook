# Route

`Route` describes both sides of a webhook URL:

* the framework path registered by the adapter;
* the public URL sent to Telegram through `setWebhook`.

It validates path parameters at construction time and validates incoming request parameters at runtime.

```python
from aiogram_webhook.route import BotTokenParam, Ref, Route

route = Route(
    base_url="https://example.com/api",
    path="/telegram/{bot_token}",
    params={"bot_token": BotTokenParam()},
    query={"token": Ref("bot_token"), "kind": ("telegram", "webhook")},
)
```

The resulting webhook URL contains an encoded path parameter and the configured query string:

```text
https://example.com/api/telegram/123456%3AABCDEF?token=123456:ABCDEF&kind=telegram&kind=webhook
```

## Path parameters

Path parameters are declared explicitly. This keeps URL generation and request parsing symmetric.

| Parameter class | Build value | Parse value | Use with |
| --- | --- | --- | --- |
| `BotIdParam` | `target.bot_id` | `int(value)` | ID-based custom routing. |
| `BotTokenParam` | `target.bot_token` | raw string | `TokenEngine`. |

You can implement your own route parameter by providing async `build(target, params)` and `parse(value, params)` methods.

{% note info "Route validation" %}

Every placeholder in `path` must have a matching declaration in `params`.
Unused declarations and repeated path placeholders are rejected during `Route(...)` construction.

{% endnote %}

## Query parameters

Use constant values for fixed query checks and `Ref("name")` to copy a parsed path parameter.

| Query value | Meaning |
| --- | --- |
| `"telegram"` | A constant string. |
| `42` | A constant integer converted to string. |
| `Ref("bot_token")` | The value parsed from a path parameter. |
| `("telegram", "webhook")` | Repeated query parameter values. |

{% cut "Strict query matching" %}

By default, `Route.match()` ignores extra query parameters after required query values pass.
Set `strict_query=True` to reject unexpected query names.

```python
route = Route(
    base_url="https://example.com",
    path="/webhook/{bot_token}",
    params={"bot_token": BotTokenParam()},
    query={"token": Ref("bot_token")},
    strict_query=True,
)
```

{% endcut %}

## Important path rules

* `path` must be relative.
* Query strings belong in `Route(query=...)`, not in `path`.
* URL fragments are not supported.
* Missing leading slashes are normalized, so `"webhook"` becomes `"/webhook"`.

## Combining with engines

For one bot, the route is usually static:

```python
Route(base_url="https://example.com", path="/webhook")
```

For many bots, the route usually carries the token:

```python
Route(
    base_url="https://example.com",
    path="/webhook/{bot_token}",
    params={"bot_token": BotTokenParam()},
)
```

The adapter registers `path`; the engine uses the full built URL when it calls Telegram.
