# What is aiogram-webhook?

`aiogram-webhook` is a small typed library for running aiogram bots through Telegram webhooks.

It keeps the HTTP boundary explicit: the web framework receives a request, the route validates it, security checks it, and the engine passes the update to aiogram.

## What you get

| | Feature |
| --- | --- |
| ⚙️ | Engines for single-bot and token-based multi-bot applications. |
| 🌐 | Adapters for FastAPI and aiohttp. |
| 🧭 | Typed route builders for public Telegram webhook URLs. |
| 🔐 | Optional request checks: secret token, IP allowlist, and custom checks. |
| 🚀 | Background update handling by default. |
| ↩️ | Foreground webhook replies when you intentionally need them. |

## Choose the entry point

| If you need | Start with |
| --- | --- |
| One bot and one webhook URL | `SingleBotEngine` |
| Many bots selected by token in the URL | `TokenEngine` |
| FastAPI integration | `FastAPIAdapter` |
| aiohttp integration | `AiohttpAdapter` |
| Telegram request verification | `Security` |
| Telegram `setWebhook` options | `WebhookConfig` |

## What it does not replace

`aiogram-webhook` does not replace aiogram routers, filters, FSM, handlers, or the dispatcher.

It also does not run a web server by itself. You still run FastAPI, aiohttp, or another framework, and call `set_webhook()` or `add_bot()` when your public HTTPS endpoint is ready.

{% note tip %}

If you are new to the library, read [Quick start](quick-start.md), then choose the component pages for your setup: Webs, Engines, Route, and Security.

{% endnote %}
