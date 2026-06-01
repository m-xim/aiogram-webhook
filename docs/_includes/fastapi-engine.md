```python
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from aiogram_webhook import FastAPIAdapter, SingleBotEngine, WebhookConfig
from aiogram_webhook.route import Route
from aiogram_webhook.security import IPCheck, Security, StaticSecretToken

dispatcher = Dispatcher()
bot = Bot("BOT_TOKEN")

engine = SingleBotEngine(
    dispatcher,
    bot,
    web=FastAPIAdapter(),
    route=Route(base_url="https://example.com", path="/telegram/webhook"),
    security=Security(IPCheck(), secret_token=StaticSecretToken("webhook-secret")),
    webhook_config=WebhookConfig(drop_pending_updates=True),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await engine.set_webhook()
    yield


app = FastAPI(lifespan=lifespan)
engine.register(app)
```
