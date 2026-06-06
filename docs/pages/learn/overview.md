# What is aiogram-webhook?

`aiogram-webhook` is a small typed library for running [aiogram](https://docs.aiogram.dev/en/latest/) bots through Telegram webhooks.

It keeps the HTTP boundary explicit: your web framework receives a request, the route validates it, security checks it, and the engine passes the update to aiogram. Routers, filters, FSM, and handlers stay the same as with long polling — only startup and the HTTP layer change.

{% note tip %}

**New here?** [Quick start](quick-start.md) gives a copy-paste app. Come back to this page when you want the full picture.

{% endnote %}

## How to read the docs

| Track | Pages | When |
| --- | --- | --- |
| **Learn** | This page → Quick start → First webhook | First time setup and deployment. |
| **Guide** | Web adapters, Engines, Route, Security, Behavior | One component at a time, after you have a running app. |
| **Recipes** | Single-bot / Multi-bot | Project layout when basics are clear. |
| **Reference** | WebhookConfig, Errors, API | Lookup while coding. |

Custom frameworks, bot lookup, or per-bot secrets: [Custom integrations](../extending/overview.md) — after the Guide, not before.

## One update, end to end

Telegram sends a `POST` with JSON. The adapter normalizes it; the engine resolves the bot, runs security, and dispatches to aiogram.

{% include [Request flow](../../_includes/request-flow.md) %}

The diagram above is the canonical request flow. Other pages link here instead of repeating it.

{% cut "What each layer is responsible for" %}

| Layer | Responsibility | Does not |
| --- | --- | --- |
| Web framework (FastAPI, aiohttp, …) | TLS, routing, middleware, running the server | Parse Telegram updates or call handlers |
| Web adapter | Register `POST`, map request/response types | Choose bot, verify Telegram, dispatch |
| `Route` | Build the public `setWebhook` URL; match path and query on incoming requests | Run security or handlers |
| `Security` | Verify secret token and optional checks before dispatch | Register routes or call `setWebhook` |
| Engine | Resolve bot, dispatch update, lifecycle, `set_webhook()` / `add_bot()` | Replace aiogram routers |
| aiogram `Dispatcher` | Handlers, filters, FSM, middleware | Expose a public HTTPS endpoint |

{% endcut %}

## Choose the entry point

| If you need | Start with |
| --- | --- |
| One bot and one webhook URL | `SingleBotEngine` — [guide](../engines/single-bot-engine.md) |
| Many bots selected by token in the URL | `TokenEngine` — [guide](../engines/token-engine.md) |
| FastAPI integration | `FastAPIAdapter` — [guide](../web/fastapi.md) |
| aiohttp integration | `AiohttpAdapter` — [guide](../web/aiohttp.md) |
| Telegram request verification | `Security` — [guide](../security/overview.md) |
| Telegram `setWebhook` options | `WebhookConfig` — [reference](../other/webhook-config.md) |

## What it does not replace

`aiogram-webhook` does not replace aiogram routers, filters, FSM, handlers, or the dispatcher.

It also does not run a web server. You run FastAPI, aiohttp, or another framework yourself, and call `set_webhook()` or `add_bot()` when the public HTTPS endpoint is ready.

{% cut "How this relates to aiogram's built-in webhook tools" %}

aiogram can register webhooks with aiohttp helpers (for example `SimpleRequestHandler`). That fits aiohttp-only projects with a fixed setup.

`aiogram-webhook` uses the same dispatch model (`feed_webhook_update` / `feed_raw_update`) and adds a FastAPI adapter, typed `Route`, composable `Security`, and `TokenEngine` for multi-bot lifecycle. If you already know aiogram handlers, you only learn the wiring on this side of the dispatcher.

{% endcut %}
