# Engines

An engine is the runtime coordinator. It receives a normalized web request from an adapter, resolves the target bot, verifies the request, feeds the update into aiogram, and handles startup/shutdown details.

Choose the engine by how the application identifies the bot.

| Engine | Target model | Best for |
| --- | --- | --- |
| `SingleBotEngine` | One configured `Bot` instance | One public webhook endpoint for one Telegram bot. |
| `TokenEngine` | Bot token extracted from the route | Multi-bot systems where each bot has its token in the webhook URL. |

{% note tip %}

Keep one `Dispatcher` per engine unless your application has a clear reason to split update routing. The engine passes lifecycle data into dispatcher startup/shutdown hooks, so routers can still access the app, bot, bots, and engine through workflow data.

{% endnote %}

## SingleBotEngine

`SingleBotEngine` always uses the `Bot` object passed to the constructor.
Path parameters may exist for routing, but they do not select another bot.

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=Route(base_url="https://example.com", path="/webhook"),
)

await engine.set_webhook()
```

Use it with:

| Component | Typical value |
| --- | --- |
| Route | Static path such as `/webhook`. |
| Adapter | `FastAPIAdapter()` or `AiohttpAdapter()`. |
| Security | `StaticSecretToken` and, in production, an IP or proxy-aware check. |
| WebhookConfig | Shared options for one Telegram webhook. |

## TokenEngine

`TokenEngine` extracts the token from route parameters.
The route must expose a `bot_token` parameter, usually with `BotTokenParam`.

```python
from aiogram_webhook import BotConfig, FastAPIAdapter, TokenEngine, WebhookConfig
from aiogram_webhook.route import BotTokenParam, Route

engine = TokenEngine(
    dispatcher,
    web=FastAPIAdapter(),
    route=Route(
        base_url="https://example.com",
        path="/webhook/{bot_token}",
        params={"bot_token": BotTokenParam()},
    ),
    bot_config=BotConfig(default=None),
)

await engine.add_bot("123456:ABCDEF")
```

`add_bot()` sets the webhook for that token.
Incoming requests with a valid token are resolved to a cached `Bot` instance.

Use it with:

| Component | Typical value |
| --- | --- |
| Route | Dynamic path such as `/webhook/{bot_token}`. |
| Route param | `BotTokenParam()` for the token placeholder. |
| Bot configuration | `BotConfig(...)` to control bot creation defaults. |
| WebhookConfig | Engine defaults plus optional per-bot overrides. |

## Telegram options on engines

Pass `webhook_config` to an engine when all bots should share the same Telegram `setWebhook` defaults.

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=route,
    webhook_config=WebhookConfig(drop_pending_updates=True),
)
```

For `TokenEngine`, the engine-level config is the default. `add_bot(..., webhook_config=...)` can override it for one bot.

{% cut "Removing bots" %}

```python
removed = await engine.remove_bot(
    bot_id=123456,
    delete_webhook=True,
    drop_pending_updates=True,
)
```

When `delete_webhook=False`, do not pass `drop_pending_updates`.
The library raises `ValueError` because Telegram only accepts that option while deleting a webhook.

{% endcut %}

## Background handling

`handle_in_background=True` is the default.
The engine acknowledges Telegram quickly and feeds the update in an internal task.
When it is `False`, the engine awaits `dispatcher.feed_webhook_update()`.

| Mode | Response behavior | Use it when |
| --- | --- | --- |
| Background | Always returns an empty `200` JSON response after scheduling work. | You want fast acknowledgement and do not need to return a Telegram method as the HTTP response. |
| Foreground | Can return a Telegram method payload directly. | You deliberately use Telegram's webhook reply optimization. |

## Engine lifecycle

`engine.register(app)` registers the webhook route through the selected web adapter and wires engine startup/shutdown callbacks into the framework.

During startup, the engine emits `dispatcher.emit_startup()` with shared workflow data:

* `dispatcher`
* `dispatcher.workflow_data`
* `app`
* `webhook_engine`

During shutdown, the engine stops accepting new webhook requests, waits for tracked background tasks, and emits dispatcher shutdown.

{% note info %}

Registering the framework route is separate from calling Telegram's API. Call `set_webhook()` or `add_bot()` from application startup when your public URL is ready.

{% endnote %}

## Combining with other components

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=Route(base_url="https://example.com", path="/webhook"),
    security=security,
    webhook_config=WebhookConfig(allowed_updates=["message"]),
)
```

The engine is where the selected adapter, route, security policy, and Telegram webhook options meet.
