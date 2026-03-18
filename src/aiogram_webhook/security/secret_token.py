import re
from abc import abstractmethod
from hmac import compare_digest
from typing import Final, Protocol

from aiogram_webhook.adapters.base_adapter import BoundRequest

SECRET_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,256}$")
SECRET_TOKEN_HEADER: Final[str] = "x-telegram-bot-api-secret-token"  # noqa: S105


class SecretToken(Protocol):
    """
    Protocol for secret token verification in webhook requests.
    """

    @abstractmethod
    async def verify(self, token: str, bound_request: BoundRequest) -> bool:
        """
        Verify the secret token in the incoming request.
        """
        raise NotImplementedError

    @abstractmethod
    def secret_token(self, token: str) -> str:
        """
        Return the secret token associated with the given token string.
        """
        raise NotImplementedError


class StaticSecretToken(SecretToken):
    """
    Static secret token implementation for webhook security.

    Token format: 1-256 characters, only A-Z, a-z, 0-9, _, - are allowed.
    See: https://core.telegram.org/bots/api#setwebhook
    """

    def __init__(self, token: str) -> None:
        if not SECRET_TOKEN_PATTERN.match(token):
            raise ValueError("Invalid secret token format. Must be 1-256 characters, only A-Z, a-z, 0-9, _, -.")
        self._token = token

    async def verify(self, token: str, bound_request: BoundRequest) -> bool:  # noqa: ARG002
        incoming = bound_request.headers.get(SECRET_TOKEN_HEADER)
        if incoming is None:
            return False
        return compare_digest(incoming, self._token)

    def secret_token(self, token: str) -> str:  # noqa: ARG002
        return self._token
