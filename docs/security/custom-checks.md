# Custom Checks

Custom checks let you add project-specific request verification. A check implements the `SecurityCheck` protocol.

```python
class HeaderCheck:
    async def verify(self, target, request, route_params) -> bool:
        return request.headers.get("X-App-Webhook") == "enabled"
```

Pass the check to `Security`:

```python
from aiogram_webhook.security import Security

security = Security(HeaderCheck())
```

## Check inputs

| Argument | Meaning |
| --- | --- |
| `target` | Resolved bot target. |
| `request` | Normalized `WebRequest`. |
| `route_params` | Parsed route path/query values. |

## Order

`Security` verifies the secret token first, then runs custom checks in the order they were passed.

Return `False` to reject the request with `403 Forbidden`.

