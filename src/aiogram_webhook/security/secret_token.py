from hmac import compare_digest
from typing import Protocol

from aiogram import Bot

from aiogram_webhook.adapters.base import BoundRequest


class SecretToken(Protocol):
    """
    Protocol for secret token verification in webhook requests.
    """

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        """
        Verify the secret token in the incoming request.
        """
        raise NotImplementedError

    def secret_token(self, bot: Bot) -> str:
        """
        Return the secret token for the given bot.
        """
        raise NotImplementedError


class StaticSecretToken(SecretToken):
    """
    Static secret token implementation for webhook security.
    """

    def __init__(self, token: str) -> None:
        self._token = token

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:  # noqa: ARG002
        incoming = bound_request.secret_token()
        if incoming is None:
            return False
        return compare_digest(incoming, self._token)

    def secret_token(self, bot: Bot) -> str:  # noqa: ARG002
        return self._token
