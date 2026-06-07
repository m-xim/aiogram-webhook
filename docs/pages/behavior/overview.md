# Webhook Behavior

How the engine responds to Telegram while handlers run. Wiring (`SingleBotEngine`, adapters, routes) lives in [Quick start](../learn/quick-start.md) and the [Engines](../engines/overview.md) guide.

## Background vs foreground

`handle_in_background=True` is the default.

| Mode | Telegram gets | Handler returns `TelegramMethod` | Use when |
| --- | --- | --- | --- |
| **Background** | Empty `200` immediately | Sent separately via Bot API | Normal bots; default choice |
| **Foreground** | Waits for handler; may stream method in HTTP body | Can become the webhook response | Deliberate [webhook reply](webhook-replies.md) optimization |

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    handle_in_background=True,  # default
)
```

Set `handle_in_background=False` only when foreground replies are an intentional design choice.

## What happens inside

**Background:** engine calls `dispatcher.feed_raw_update()` in a tracked task. If a handler returns a `TelegramMethod`, the engine sends it with `dispatcher.silent_call_request()`.

**Foreground:** engine awaits `dispatcher.feed_webhook_update()`. Slow handlers keep the Telegram HTTP connection open — avoid long I/O in this mode.

## Startup and shutdown

Engine lifecycle (workflow data, `503` during shutdown, task draining): [SingleBotEngine](../engines/single-bot-engine.md) · [TokenEngine](../engines/token-engine.md).
