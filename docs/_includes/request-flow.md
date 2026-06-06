```mermaid
sequenceDiagram
    participant TG as Telegram
    participant FW as Web framework
    participant AD as Web adapter
    participant RT as Route
    participant SEC as Security
    participant EN as Engine
    participant DP as aiogram Dispatcher

    TG->>FW: POST update JSON
    FW->>AD: framework request
    AD->>EN: WebRequest
    EN->>RT: match(request)
    RT-->>EN: route_params
    EN->>EN: resolve Target and Bot
    EN->>SEC: verify(...)
    EN->>EN: parse JSON update
    alt handle_in_background (default)
        EN->>DP: feed_raw_update (background task)
        EN-->>TG: 200 {}
    else handle_in_background=False
        EN->>DP: feed_webhook_update
        DP-->>EN: TelegramMethod (optional)
        EN-->>TG: 200 multipart or {}
    end
```

By default the HTTP response is an empty `200` while handlers run in the background. User-facing replies go through the Bot API in a separate call — not inside the webhook body.
