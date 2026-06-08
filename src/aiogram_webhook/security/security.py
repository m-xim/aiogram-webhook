from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.security.checks.check import SecurityCheck
from aiogram_webhook.security.errors import SecretTokenError, SecurityCheckError
from aiogram_webhook.security.secret_token import SecretToken
from aiogram_webhook.web.base import WebRequest


class Security:
    def __init__(self, *checks: SecurityCheck, secret_token: SecretToken | None = None) -> None:
        self._secret_token = secret_token
        self._checks: tuple[SecurityCheck, ...] = checks

    async def verify(self, *, target: Target, request: WebRequest, route_params: RouteParams) -> None:
        if self._secret_token is not None:
            ok = await self._secret_token.verify(target=target, request=request, route_params=route_params)
            if not ok:
                raise SecretTokenError(target_bot_id=target.bot_id)

        for check in self._checks:
            ok = await check.verify(target=target, request=request, route_params=route_params)
            if not ok:
                raise SecurityCheckError(
                    security_check=check.__class__.__name__,
                    client_ip=str(request.client_ip) if request.client_ip is not None else None,
                )

    async def secret_token(self, target: Target) -> str | None:
        """
        Get the secret token for a specific bot target.

        :param target: The target bot to get the token for.
        :return: The secret token string, or None if no token is configured.
        """
        if self._secret_token is None:
            return None

        return await self._secret_token.secret_token(target=target)
