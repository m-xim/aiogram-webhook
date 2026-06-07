# Engines

The engine is the runtime coordinator: it receives a normalized request from an adapter, resolves the bot, runs security, feeds the update to aiogram, and manages lifecycle.

{% note info %}

New to the library? [Quick start](../learn/quick-start.md) wires `SingleBotEngine` first. Request flow diagram: [What is aiogram-webhook?](../learn/overview.md#one-update-end-to-end).

{% endnote %}

## Which engine?

| Engine | How the bot is chosen | Guide |
| --- | --- | --- |
| `SingleBotEngine` | Always the `Bot` from the constructor | [SingleBotEngine](single-bot-engine.md) |
| `TokenEngine` | `bot_token` from route parameters | [TokenEngine](token-engine.md) |
| Custom subclass | Your `_resolve_target` / `_resolve_bot` logic | [Custom engine](custom-engine.md) |

Shipped engines are convenience defaults, not the only design. Database lookup or path-based bot IDs need a custom engine.

## Wiring pattern

Every engine takes the same constructor arguments:

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=adapter,
    route=route,
    security=security,  # optional, recommended in production
    webhook_config=webhook_config,  # optional Telegram setWebhook fields
    handle_in_background=True,  # default; see Behavior
)
```

`engine.register(app)` exposes the local route; `set_webhook()` / `add_bot()` register with Telegram. See [First webhook](../learn/first-webhook.md#2-wire-engine-and-adapter).

## Related topics

| Topic | Page |
| --- | --- |
| Background vs foreground dispatch | [Dispatch Modes](../dispatch.md) |
| Telegram `setWebhook` fields | [WebhookConfig](../other/webhook-config.md) |
| Per-bot overrides on `TokenEngine` | [TokenEngine](token-engine.md) |
| HTTP errors during dispatch | [Errors](../other/errors.md) |

{% note tip %}

Keep one `Dispatcher` per engine unless you have a clear reason to split routing. Startup workflow data includes `app`, `webhook_engine`, and `bot` or `bots` for use in aiogram hooks.

{% endnote %}
