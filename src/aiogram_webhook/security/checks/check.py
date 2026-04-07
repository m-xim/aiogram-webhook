from typing import Protocol

from aiogram import Dispatcher

from aiogram_webhook.adapters.base_adapter import BoundRequest


class SecurityCheck(Protocol):
    """Protocol for security check on webhook requests."""

    async def verify(self, bot_token: str, bound_request: BoundRequest, dispatcher: Dispatcher) -> bool:
        """
        Perform a security check.

        :param bot_token: Bot token used by token-aware checks.
        :param dispatcher: Dispatcher instance for dependency-aware checks.
        :return: True if the check passes, False otherwise.
        """
        raise NotImplementedError
