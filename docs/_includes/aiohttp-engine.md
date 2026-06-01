```python
from aiohttp import web
from aiogram import Bot, Dispatcher

from aiogram_webhook import AiohttpAdapter, SingleBotEngine, WebhookConfig
from aiogram_webhook.route import Route
from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

dispatcher = Dispatcher()
bot = Bot("BOT_TOKEN")

engine = SingleBotEngine(
    dispatcher,
    bot,
    web=AiohttpAdapter(),
    route=Route(base_url="https://example.com", path="/telegram/webhook"),
    security=Security(IPCheck(), secret_token=StaticSecretToken("webhook-secret")),
    webhook_config=WebhookConfig(drop_pending_updates=True),
)


async def set_webhook(app: web.Application) -> None:
    await engine.set_webhook()


app = web.Application()
app.on_startup.append(set_webhook)
engine.register(app)
```
