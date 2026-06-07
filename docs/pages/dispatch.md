# Dispatch Modes

How the engine responds to Telegram while handlers run. Wiring (`SingleBotEngine`, adapters, routes) lives in [Quick start](learn/quick-start.md) and the [Engines](engines/overview.md) guide.

## Background vs foreground

`handle_in_background=True` is the default.

| Mode | Telegram gets | Handler returns `TelegramMethod` | Use when |
| --- | --- | --- | --- |
| **Background** | Empty `200` immediately | Sent separately via Bot API | Normal bots; default choice |
| **Foreground** | Waits for handler; may stream method in HTTP body | Streamed as webhook reply | Saving one Bot API round-trip is a deliberate optimization |

## Background mode

Engine spawns `dispatcher.feed_raw_update()` in a tracked background task and immediately returns `200 {}` to Telegram. The HTTP response is sent before the handler runs.

If a handler returns a `TelegramMethod`, the engine sends it via a separate Bot API call (`dispatcher.silent_call_request()`).

{% note warning %}

Webhook replies are not available in background mode. Any `TelegramMethod` returned by a handler becomes a regular Bot API call instead of an in-response reply.

{% endnote %}

## Foreground mode

Engine awaits `dispatcher.feed_webhook_update()` before responding. If a handler returns a `TelegramMethod`, it is streamed back as a Telegram-compatible multipart response — saving one round-trip to the Bot API.

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    handle_in_background=False,
)
```

```python
from aiogram.methods import SendMessage
from aiogram.types import Message


@router.message()
async def echo(message: Message):
    return SendMessage(chat_id=message.chat.id, text=message.text)
```

{% note warning %}

Foreground mode keeps the Telegram HTTP connection open until the handler completes. Avoid long I/O, external API calls, or file uploads inside handlers — use background mode for those cases.

{% endnote %}

| | Background | Foreground |
| --- | --- | --- |
| Response time | Immediate | After handler completes |
| Webhook reply | Not available | Available |
| Extra Bot API call | Yes, if handler returns a method | No |
| Safe for slow handlers | Yes | No |

## Startup and shutdown

Engine lifecycle (workflow data, `503` during shutdown, task draining): [SingleBotEngine](engines/single-bot-engine.md) · [TokenEngine](engines/token-engine.md).
