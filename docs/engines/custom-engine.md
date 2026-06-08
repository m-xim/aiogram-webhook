# Custom Engine

Create a custom engine when bot resolution does not match `SingleBotEngine` (one fixed `Bot`) or `TokenEngine` (token embedded in the URL).

The request pipeline — route match, security, JSON parsing, background/foreground dispatch, error mapping — already lives in `BaseWebhookEngine`. Your subclass only defines **how a request becomes a `Target` and a `Bot`**, plus lifecycle and webhook registration helpers your app needs.

## Shipped engines are examples

| Engine | `_resolve_target` idea | `_resolve_bot` idea |
| --- | --- | --- |
| `SingleBotEngine` | Always the constructor `Bot` | Returns that same instance |
| `TokenEngine` | Reads `bot_token` from route params | Creates or returns a cached `Bot` |

They are reference implementations. A database-backed registry, `BotIdParam` in the path, or a header-selected bot all belong in a custom engine.

## Choose a base class

| Base class | Use when |
| --- | --- |
| `BaseWebhookEngine` | One bot per request with your own resolution rules, or a single shared `Bot` with custom lifecycle. |
| `BaseMultiBotEngine` | Several bots in one process; provides `self._bots`, per-bot `TaskTracker`, and `bots` property. |

Import from `aiogram_webhook.engines.base` and `aiogram_webhook.engines.multi`. These classes are not re-exported from the top-level package — extension code is expected to import internals explicitly.

## Methods to implement

| Method | Responsibility |
| --- | --- |
| `_resolve_target(request, route_params)` | Return `Target(bot_id=..., bot_token=...)` or `None` (becomes HTTP 404). |
| `_resolve_bot(target)` | Return a `Bot` for that target or `None` (becomes HTTP 404). |
| `_get_task_tracker(bot)` | Return a `TaskTracker` for background tasks (one shared tracker for single-bot; per-bot map for multi-bot). |
| `_on_startup` / `_on_shutdown` | Emit dispatcher lifecycle; close trackers and bot sessions you own. |

`handle_request()` in the base class already calls `route.match`, `security.verify`, and `feed_raw_update` / `feed_webhook_update`. Do not reimplement that loop unless you have an exceptional reason.

For Telegram registration, reuse `_build_webhook_kwargs(target, webhook_config)` so `Security` secret tokens and `WebhookConfig` fields stay aligned with verification.

## Sketch: bot id in the path

`BotIdParam` maps a path segment to `target.bot_id`, but there is no built-in engine that loads bots by id. Below is a minimal sketch — storage and error handling are yours to define.

```python
from aiogram import Bot
from aiogram_webhook.engines.multi import BaseMultiBotEngine
from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.tasks import TaskTracker
from aiogram_webhook.web.base import WebRequest


class BotIdEngine(BaseMultiBotEngine):
    async def _resolve_target(self, request: WebRequest, route_params: RouteParams) -> Target | None:
        bot_id = route_params.get("bot_id")
        if bot_id is None:
            return None
        record = await self._registry.get(int(bot_id))  # your storage
        if record is None:
            return None
        return Target(bot_id=record.id, bot_token=record.token)

    async def _resolve_bot(self, target: Target) -> Bot | None:
        if target.bot_id in self._bots:
            return self._bots[target.bot_id]
        record = await self._registry.get(target.bot_id)
        if record is None:
            return None
        bot = Bot(token=record.token, session=self._session)
        self._bots[bot.id] = bot
        return bot

    def _get_task_tracker(self, bot: Bot) -> TaskTracker:
        return super()._get_task_tracker(bot)

    async def register_bot(self, bot_id: int) -> None:
        target = await self._resolve_target(None, {"bot_id": str(bot_id)})
        bot = await self._resolve_bot(target)
        kwargs = await self._build_webhook_kwargs(target)
        await bot.set_webhook(url=await self.route.build_url(target), **kwargs)
```

Pair this engine with a route such as:

```python
from aiogram_webhook.route import BotIdParam, Route

Route(
    base_url="https://example.com",
    path="/webhook/{bot_id}",
    params={"bot_id": BotIdParam()},
)
```

## Multi-bot lifecycle notes

`BaseMultiBotEngine._on_startup` accepts an optional `bots` iterable and merges it with `self.bots` before `emit_startup`. On shutdown, close every `TaskTracker` in `self._task_trackers` before closing bot sessions you created.

`TokenEngine` is the fullest shipped sample for add/remove bot flows, session ownership, and webhook registration — read its source when your engine exposes similar admin APIs.

## Combining with other components

| Concern | Where it lives |
| --- | --- |
| URL shape and matching | `Route` + param types (`BotIdParam`, `BotTokenParam`, …) |
| Request verification | `Security` on the engine constructor |
| HTTP framework | `WebAdapter` — unchanged by a custom engine |
| Handler code | aiogram `Dispatcher` — unchanged |

{% note info %}

Start from `SingleBotEngine` or `TokenEngine` in source control and edit toward your resolution logic. That is faster than subclassing from scratch and helps you mirror lifecycle and session cleanup correctly.

{% endnote %}
