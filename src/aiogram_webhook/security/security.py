from aiogram_webhook.adapters.base_adapter import BoundRequest
from aiogram_webhook.security.checks.check import SecurityCheck
from aiogram_webhook.security.secret_token import SecretToken


class Security:
    """
    Security management for webhook requests.

    Provides methods to verify requests and manage secret tokens.
    """

    def __init__(self, *checks: SecurityCheck, secret_token: SecretToken | None = None) -> None:
        self._secret_token = secret_token
        self._checks: tuple[SecurityCheck, ...] = checks

    async def verify(self, bot_token: str, bound_request: BoundRequest) -> bool:
        """
        Verify the security of a webhook request.

        :param bot_token: Bot token for webhook route and token-aware checks.
        :return: True if the request passes security checks, False otherwise.
        """
        if self._secret_token is not None:
            ok = await self._secret_token.verify(bot_token, bound_request)
            if not ok:
                return False

        for checker in self._checks:
            if not await checker.verify(bot_token, bound_request):
                return False

        return True

    async def secret_token(self, bot_token: str) -> str | None:
        """
        Get the secret token for the given bot, if configured.

        :param bot_token: Bot token for which secret token should be resolved.
        :return: The secret token as a string.
        """
        if self._secret_token is None:
            return None
        return self._secret_token.secret_token(bot_token=bot_token)
