# Custom Adapter

Create a custom adapter when your web framework is not FastAPI or aiohttp. The adapter is the **only** layer that should know framework-specific request and response types.

`FastAPIAdapter` and `AiohttpAdapter` are shipped reference implementations — useful to read, not mandatory templates. Study their source when you need working lifecycle wiring or multipart reply handling:

* `aiogram_webhook.web.fastapi` — `engine.lifespan(app)` context manager pattern, Starlette payload bridge
* `aiogram_webhook.web.aiohttp` — `web.Application` routes and startup/shutdown hooks

See also [Extending overview](../custom-integrations.md) for how adapters fit next to engines and security.

## Contract: `WebAdapter`

| Method | Responsibility | Called when |
| --- | --- | --- |
| `bind_request(raw)` | Wrap the framework request as `WebRequest`. | Every webhook `POST`. |
| `register(app, path, handler, on_startup, on_shutdown)` | Register `POST` only; wire lifecycle hooks. | `engine.register(app)`. |
| `json_response(status_code, data, headers)` | Map engine errors and empty `200 {}` success. | Most responses. |
| `payload_response(status_code, payload, headers)` | Stream aiohttp `Payload` (multipart Telegram method). | `handle_in_background=False` with a returned `TelegramMethod`. |

## `WebRequest` protocol

Your wrapper must expose:

```python
class MyWebRequest:
    @property
    def raw(self): ...

    @property
    def client_ip(self) -> str | None: ...

    async def json(self) -> dict: ...

    @property
    def headers(self): ...

    @property
    def query_params(self): ...

    @property
    def path_params(self): ...
```

`client_ip` feeds `IPCheck`. `path_params` must match what your framework extracted for the registered path — the engine does not parse paths itself; `Route.match()` uses these values.

## Minimal skeleton

```python
from aiogram_webhook.web.base import WebAdapter


class MyAdapter(WebAdapter):
    def bind_request(self, request):
        return MyWebRequest(request)

    def register(self, app, path, handler, *, on_startup, on_shutdown) -> None:
        async def endpoint(raw_request):
            return await handler(self.bind_request(raw_request))

        app.post(path, endpoint)
        app.on_startup(on_startup)
        app.on_shutdown(on_shutdown)

    def json_response(self, status_code: int, data=None, headers=None):
        return my_json_response(status_code=status_code, data=data, headers=headers)

    def payload_response(self, status_code: int, payload, headers=None):
        return my_payload_response(status_code=status_code, payload=payload, headers=headers)
```

Replace `app.post` / lifecycle hooks with your framework's equivalents. The handler signature is always `async (WebRequest) -> FrameworkResponse`.

{% note warning %}

`payload_response()` matters when `handle_in_background=False`. Handlers may return a `TelegramMethod` that must be streamed back to Telegram as multipart content. Returning JSON instead will break foreground webhook replies.

FastAPI bridges aiohttp `Payload` through `AiohttpPayloadResponse` in `aiogram_webhook.web._starlette` — reuse or adapt that approach on ASGI stacks.

{% endnote %}

## Boundaries: adapter vs engine

| Concern | Belongs in |
| --- | --- |
| Framework route registration | Adapter |
| Request/response type mapping | Adapter |
| Bot resolution | Engine |
| URL construction and matching | `Route` |
| Secret token and IP verification | `Security` |
| Telegram `setWebhook` options | `WebhookConfig` on the engine |
| Parsing updates and calling aiogram | Engine (`handle_request`) |

If verification or bot lookup leaks into the adapter, you duplicate logic that `SingleBotEngine` / `TokenEngine` already centralize and tests no longer cover your path.

## Framework-specific notes

| Stack | Practical approach |
| --- | --- |
| Starlette (without FastAPI) | Mirror `FastAPIAdapter`: `APIRouter` or raw routes + lifespan; reuse `_starlette.AiohttpPayloadResponse` for payloads. |
| Django (async) | Wrap `ASGIRequest`; register an async view; map `JsonResponse` and a streaming response for payloads. |
| Litestar, Quart, etc. | Same four-method contract; lifecycle hook names differ per framework. |

Register **POST** only on the webhook path. `GET` probes from browsers or health checks should not hit the engine handler unless you add them separately.

## Using a custom adapter

```python
engine = SingleBotEngine(
    dispatcher,
    bot,
    web=MyAdapter(),
    route=route,
    security=security,
)
engine.register(app)
```

Engine and `Route` configuration are identical to FastAPI or aiohttp — only `web=` changes.
