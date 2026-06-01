# Custom Adapter

Create a custom adapter when your web framework is not FastAPI or aiohttp. A custom adapter is the only component that should know framework-specific request and response types.

The adapter implements the `WebAdapter` abstract base class.

## Required behavior

| Method | Responsibility | Used by |
| --- | --- | --- |
| `bind_request()` | Wrap a framework request in the `WebRequest` protocol. | Engine request handling. |
| `register()` | Register a `POST` route and lifecycle callbacks. | `engine.register(app)`. |
| `json_response()` | Return a framework JSON response. | Error and empty success responses. |
| `payload_response()` | Return a framework response from an aiohttp `Payload`. | Foreground Telegram method replies. |

## WebRequest protocol

Your request wrapper must expose:

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

## Adapter skeleton

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

{% note warning %}

`payload_response()` is important when `handle_in_background=False`.
In that mode, handlers may return a Telegram method that must be streamed back to Telegram.

{% endnote %}

## Combining with other components

The engine calls adapter methods, but the adapter should not duplicate engine work:

| Concern | Keep it in |
| --- | --- |
| Framework route registration | Adapter |
| Bot resolution | Engine |
| URL construction and matching | Route |
| Token and IP verification | Security |
| Telegram `setWebhook` options | WebhookConfig |
