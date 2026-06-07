# API Reference

This reference lists the public objects users normally import.

## Package exports

| Import | Purpose |
| --- | --- |
| `AiohttpAdapter` | aiohttp web framework adapter. |
| `FastAPIAdapter` | FastAPI adapter, available when FastAPI is installed. |
| `SingleBotEngine` | Engine for one configured `Bot`. |
| `TokenEngine` | Engine for token-based multi-bot webhook routes. |
| `WebhookConfig` | Telegram `setWebhook` options. |
| `BotConfig` | Bot defaults and shared session configuration for `TokenEngine`. |

## Route helpers

| Import | Purpose |
| --- | --- |
| `Route` | Builds public webhook URLs and matches incoming requests. |
| `BotIdParam` | Path parameter mapped to `Target.bot_id`. |
| `BotTokenParam` | Path parameter mapped to `Target.bot_token`. |
| `Const` | Explicit constant query value. |
| `Ref` | Query value copied from a parsed route parameter. |

## Security helpers

| Import | Purpose |
| --- | --- |
| `Security` | Runs secret-token and custom request checks. |
| `StaticSecretToken` | Static Telegram secret-token provider and verifier. |
| `IPCheck` | Allows requests from configured IP addresses and networks. |
| `SecurityCheck` | Protocol for custom checks. |
| `SecretToken` | Base class for custom secret-token providers. See [Custom secret token](../security/custom-secret-token.md). |

## Extension bases (import from submodules)

| Import path | Purpose |
| --- | --- |
| `aiogram_webhook.web.base.WebAdapter` | Custom HTTP framework integration. |
| `aiogram_webhook.engines.base.BaseWebhookEngine` | Custom single-target engine logic. |
| `aiogram_webhook.engines.multi.BaseMultiBotEngine` | Custom multi-bot engine with shared bot cache. |

See [Custom integrations](../custom-integrations.md).
