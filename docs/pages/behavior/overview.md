# Webhook Behavior Choices

This page compares behavior choices that affect webhook request handling. It does not define a concrete application setup.

| Topic | Question it answers |
| --- | --- |
| Background handling | Does the engine answer Telegram immediately or wait for handlers? |
| Webhook replies | Can a handler return a Telegram method in the HTTP response? |

## Background vs foreground

`handle_in_background=True` is the default engine behavior. The engine acknowledges Telegram quickly and feeds the update in an internal task.

| Choice | Telegram response | Handler result | Use when |
| --- | --- | --- | --- |
| Background | Returns empty `200` after scheduling work. | A returned Telegram method is sent separately by aiogram. | You want fast acknowledgement and normal bot handlers. |
| Foreground | Waits for `dispatcher.feed_webhook_update()`. | A returned Telegram method can become the webhook HTTP response. | You deliberately use Telegram's webhook reply optimization. |

Use background handling by default. Use foreground handling only when webhook replies are a deliberate design choice.

## Configure the mode

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    handle_in_background=True,
)
```

Set `handle_in_background=False` only when you want handlers to return a Telegram method through the webhook HTTP response.

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    handle_in_background=False,
)
```

## Background mode

In background mode, the engine calls `dispatcher.feed_raw_update()` inside a tracked task. If the handler returns a `TelegramMethod`, the engine sends it through aiogram with `dispatcher.silent_call_request()`.

## Foreground mode

Foreground mode can keep the HTTP request open longer because the engine waits for dispatcher processing. Avoid slow external calls or long-running work in this mode.

Startup and shutdown are engine concerns. See [Engines](../engines/overview.md) and the specific engine page for workflow data and registration details.
