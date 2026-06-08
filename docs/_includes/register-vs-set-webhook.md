{% note info "Two registrations" %}

| Step | Call | Purpose |
| --- | --- | --- |
| Local route | `engine.register(app)` | Registers `POST` in your web framework. With aiohttp, also wires engine startup/shutdown via callback lists. |
| Lifecycle (FastAPI) | `engine.lifespan(app)` | Async context manager — runs engine startup on enter, shutdown on exit. Required for FastAPI; not needed for aiohttp. |
| Telegram delivery | `await engine.set_webhook()` | Tells Telegram the public HTTPS URL for future updates. |

Run `set_webhook()` from framework startup **after** the endpoint is reachable. For `TokenEngine`, call `add_bot(token)` per bot instead.

{% endnote %}
