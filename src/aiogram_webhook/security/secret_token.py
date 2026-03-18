import re
from abc import ABC, abstractmethod
from hmac import compare_digest
from typing import Final

from aiogram_webhook.adapters.base_adapter import BoundRequest

SECRET_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,256}$")
SECRET_TOKEN_HEADER: Final[str] = "x-telegram-bot-api-secret-token"  # noqa: S105


class SecretToken(ABC):
    """
    Base class for secret token verification in webhook requests.
    """

    async def verify(self, bot_token: str, bound_request: BoundRequest) -> bool:
        incoming_secret_token = bound_request.headers.get(SECRET_TOKEN_HEADER)
        if incoming_secret_token is None:
            return False
        return compare_digest(incoming_secret_token, await self.secret_token(bot_token))

    @abstractmethod
    async def secret_token(self, bot_token: str) -> str:
        """
        Return the webhook secret token associated with the given bot token.

        :param bot_token: Bot token used to resolve expected secret token.
        """
        raise NotImplementedError


class StaticSecretToken(SecretToken):
    """
    Static secret token implementation for webhook security.

    Token format: 1-256 characters, only A-Z, a-z, 0-9, _, - are allowed.
    See: https://core.telegram.org/bots/api#setwebhook
    """

    def __init__(self, secret_token: str) -> None:
        if not SECRET_TOKEN_PATTERN.match(secret_token):
            raise ValueError("Invalid secret token format. Must be 1-256 characters, only A-Z, a-z, 0-9, _, -.")
        self.__secret_token = secret_token

    async def secret_token(self, bot_token: str) -> str:  # noqa: ARG002
        return self.__secret_token
