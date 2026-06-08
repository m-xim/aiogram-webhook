# Errors

Known `aiogram-webhook` errors are converted into safe public JSON responses. Detailed diagnostic messages are logged through the library logger.

| Condition | Status | Body | Start with |
| --- | --- | --- | --- |
| Invalid JSON payload | `400` | `{"detail": "Bad request"}` | Request body and client. |
| Security check failed | `403` | `{"detail": "Forbidden"}` | [Security](../security/overview.md). |
| Secret token failed | `403` | `{"detail": "Forbidden"}` | [Secret token](../security/secret-token.md). |
| Target cannot be resolved | `404` | `{"detail": "Not found"}` | [Route](../route/overview.md) and [Engines](../engines/overview.md). |
| Bot cannot be resolved | `404` | `{"detail": "Not found"}` | Selected engine and bot registration. |
| Shutdown already started | `503` | `{"detail": "Service unavailable"}` | Engine startup/shutdown behavior. |

## Error boundary

The public response intentionally stays short:

```json
{"detail": "Forbidden"}
```

The log message carries more detail so you can debug the actual component that rejected the request.

## Common causes

{% list tabs group=error %}

- 400

  The request body is not valid JSON. Telegram normally sends valid JSON, so this often means a non-Telegram client called the endpoint.

- 403

  A configured secret token or security check rejected the request. Check `X-Telegram-Bot-Api-Secret-Token`, client IP, and proxy headers.

- 404

  The route matched at the framework level, but the engine could not resolve a target or bot. For `TokenEngine`, verify that `{bot_token}` is present, valid, and registered when required.

- 503

  The engine is shutting down. This is expected during graceful worker termination.

{% endlist %}

## Where to start

1. Check the HTTP status.
2. Open the matching component page.
3. Check application logs for the detailed message.
4. Use troubleshooting when the component looks correct but the behavior is still wrong.
