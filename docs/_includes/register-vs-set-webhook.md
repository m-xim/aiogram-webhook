{% note info "Two registrations" %}

| Step | Call | Purpose |
| --- | --- | --- |
| Local route | `engine.register(app)` | Registers `POST` in your web framework and wires engine startup/shutdown. |
| Telegram delivery | `await engine.set_webhook()` | Tells Telegram the public HTTPS URL for future updates. |

Run `set_webhook()` from framework startup **after** the endpoint is reachable. For `TokenEngine`, call `add_bot(token)` per bot instead.

{% endnote %}
