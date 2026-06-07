# Web Adapters

Adapters connect the engine to your HTTP framework. They register `POST`, map requests to `WebRequest`, and map engine responses back to framework types.

{% note info %}

First webhook? [First webhook](../learn/first-webhook.md) picks FastAPI or aiohttp for you. Return here to compare options or plan a custom integration.

{% endnote %}

## Choose an adapter

| Adapter | Framework | Guide |
| --- | --- | --- |
| `FastAPIAdapter` | FastAPI | [FastAPI](fastapi.md) |
| `AiohttpAdapter` | `aiohttp.web.Application` | [aiohttp](aiohttp.md) |
| Custom `WebAdapter` | Any async framework | [Custom adapter](custom.md) |

Match the framework your application already uses. If there is no preference, FastAPI is the shortest path.

## Adapter boundary

The adapter handles HTTP types only. It does **not** resolve bots, verify security, or call the dispatcher — that stays in the engine.

| Adapter does | Adapter does not |
| --- | --- |
| Register `POST` on `route.path` | Parse Telegram updates for business logic |
| Expose `client_ip`, headers, path/query params | Call `setWebhook` |
| Build JSON and payload responses | Choose which bot handles the update |

Full layer breakdown: [Dispatch modes](../dispatch.md#what-each-layer-is-responsible-for).

## Custom framework

Shipped adapters are working references, not templates to copy verbatim. See [Custom integrations](../custom-integrations.md).
