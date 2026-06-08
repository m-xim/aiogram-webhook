# Custom integrations

Built-in adapters and engines cover common setups. When one piece does not fit — another framework, database bot lookup, per-bot secrets — replace **only that piece** and keep the rest.

{% note warning %}

Start with [First webhook](learn/first-webhook.md) and shipped components first. Custom code is easier to reason about when the default path already works.

{% endnote %}

## Extension map

| You need to… | Implement | Shipped reference |
| --- | --- | --- |
| Support another web framework | `WebAdapter` + `WebRequest` | [FastAPI](web/fastapi.md), [aiohttp](web/aiohttp.md) — read source, do not copy blindly |
| Resolve bots by id, database, or custom route | `BaseWebhookEngine` / `BaseMultiBotEngine` | [SingleBotEngine](engines/single-bot-engine.md), [TokenEngine](engines/token-engine.md) |
| Different secret per bot | `SecretToken` | [StaticSecretToken](security/secret-token.md) |
| Extra request rules (headers, tenancy) | `SecurityCheck` | [IPCheck](security/ip-check.md) |

| Guide | Open when |
| --- | --- |
| [Custom adapter](web/custom.md) | HTTP stack is not FastAPI or aiohttp. |
| [Custom engine](engines/custom-engine.md) | Bot selection is not fixed `Bot` or URL token. |
| [Custom secret token](security/custom-secret-token.md) | Secrets come from storage at runtime. |
| [Custom checks](security/custom-checks.md) | Verification goes beyond Telegram defaults. |

## Boundaries (do not blur)

| Layer | Owns |
| --- | --- |
| Adapter | Framework types, `POST` registration, response mapping |
| `Route` | Public URL build + path/query match |
| `Security` | Verification before dispatch |
| Engine | Bot resolution, update feeding, lifecycle, `setWebhook` kwargs |
| aiogram | Handlers, filters, FSM |

An adapter that resolves bots, or an engine that parses framework-specific headers, couples layers and makes upgrades harder.

Layer table with examples: [Dispatch modes](dispatch.md#what-each-layer-is-responsible-for).

## Out of scope

Handler design, FSM, and Bot API usage: [aiogram documentation](https://docs.aiogram.dev/en/latest/).
