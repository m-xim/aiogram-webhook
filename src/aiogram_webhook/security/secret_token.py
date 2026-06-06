import re
from abc import ABC, abstractmethod
from hmac import compare_digest
from typing import Final

from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.web.base import WebRequest

SECRET_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,256}$")
SECRET_TOKEN_HEADER: Final[str] = "x-telegram-bot-api-secret-token"  # noqa: S105


class SecretToken(ABC):
    """
    Base class for secret token verification in webhook requests.
    """

    async def verify(self, target: Target, request: WebRequest, route_params: RouteParams) -> bool:  # noqa: ARG002
        """
        Verify the incoming secret token from the request.

        :param target: The target bot information.
        :param request: The webhook request object.
        :param route_params: Route parameters mapping.
        :return: True if the token is valid, False otherwise.
        """
        incoming_secret_token = request.headers.get(SECRET_TOKEN_HEADER)
        if incoming_secret_token is None:
            return False
        return compare_digest(incoming_secret_token, await self.secret_token(target=target))

    @abstractmethod
    async def secret_token(self, target: Target) -> str:
        """
        Return the webhook secret token associated with the given bot token.

        :param target: The target bot information.
        :return: The secret token string for this bot.
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

    async def secret_token(self, target: Target) -> str:  # noqa: ARG002
        """
        Return the static secret token.

        :param target: The target bot information (unused for static tokens).
        :return: The configured secret token.
        """
        return self.__secret_token
