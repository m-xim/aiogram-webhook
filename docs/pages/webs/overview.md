# Compare Web Adapters

Web adapters connect `aiogram-webhook` to a concrete HTTP framework. Use this page to choose the adapter, not to study framework-specific setup.

| Adapter | Framework | Use when |
| --- | --- | --- |
| `FastAPIAdapter` | FastAPI | You already use FastAPI, or want its routing, middleware, lifespan, and ecosystem. |
| `AiohttpAdapter` | `aiohttp.web.Application` | You already use aiohttp, or want lower-level async web primitives. |
| Custom `WebAdapter` | Any async web framework | You need another framework while keeping engine logic unchanged. |

## Comparison

| Question | FastAPI | aiohttp | Custom |
| --- | --- | --- | --- |
| Framework object | `FastAPI` app | `aiohttp.web.Application` | Your app type |
| Lifecycle style | Lifespan/router integration | Startup/shutdown callbacks | Adapter-defined |
| Best fit | API services and FastAPI projects | aiohttp services | Existing custom stack |
| Implementation effort | Ready to use | Ready to use | Requires adapter code |

## Adapter boundary

Regardless of framework, the adapter boundary stays the same:

* register a `POST` route;
* convert a framework request into `WebRequest`;
* create JSON responses;
* create payload responses for foreground webhook replies.

The adapter does not resolve bots, verify security checks, or call the dispatcher. Those responsibilities stay inside the engine.

## Decision rule

Choose the adapter that matches the web framework already used by the application. If there is no existing framework choice, start with FastAPI for the shortest path.
