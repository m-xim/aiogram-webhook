# SingleBotEngine

`SingleBotEngine` handles one configured `Bot` instance. Every accepted webhook request is dispatched to that bot.

## When to use it

Use `SingleBotEngine` when:

* one deployed application serves one Telegram bot;
* the webhook URL does not need to identify a bot;
* you want the simplest production setup.

## Minimal setup

```python
from aiogram import Bot, Dispatcher

from aiogram_webhook import FastAPIAdapter, SingleBotEngine, WebhookConfig
from aiogram_webhook.route import Route

dispatcher = Dispatcher()
bot = Bot("BOT_TOKEN")

engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=Route(base_url="https://example.com", path="/webhook"),
    webhook_config=WebhookConfig(drop_pending_updates=True),
)
```

## How it combines with other parts

| Part | Typical value |
| --- | --- |
| Web | `FastAPIAdapter()` or `AiohttpAdapter()`. |
| Route | Static path such as `/webhook`. |
| Security | `StaticSecretToken` and optional `IPCheck`. |
| Webhook options | One shared `WebhookConfig`. |

Call `await engine.set_webhook()` when your public HTTPS endpoint is ready.

## Telegram options

`SingleBotEngine` uses one `WebhookConfig` for one Telegram webhook.

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=web,
    route=route,
    webhook_config=WebhookConfig(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    ),
)
```

## Startup and shutdown

During engine startup, `SingleBotEngine` adds the configured `bot` to dispatcher startup workflow data.

| Hook | What happens |
| --- | --- |
| Startup | Emits dispatcher startup with `bot`, `app`, `dispatcher`, and `webhook_engine`. |
| Shutdown | Rejects late webhook requests, waits for tracked tasks, emits dispatcher shutdown, and closes the bot session when owned by the engine. |

Call `set_webhook()` from your web framework startup or lifespan function:

```python
@asynccontextmanager
async def lifespan(app):
    await engine.set_webhook()
    yield
```

`engine.register(app)` wires local framework callbacks. `engine.set_webhook()` calls Telegram.
