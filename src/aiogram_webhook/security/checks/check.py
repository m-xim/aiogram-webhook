from typing import Protocol

from aiogram import Bot

from aiogram_webhook.adapters.base import BoundRequest


class SecurityCheck(Protocol):
    """Protocol for security check on webhook requests."""

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        """
        Perform a security check.

        :return: True if the check passes, False otherwise.
        """
        raise NotImplementedError
