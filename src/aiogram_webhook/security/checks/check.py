from typing import Protocol

from aiogram import Bot

from aiogram_webhook.adapters.base import BoundRequest


class Check(Protocol):
    """
    Base class for security checks.

    Subclasses should implement the `verify` method to perform security checks.
    """
    Protocol for security check on webhook requests.
    """

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        """
        Perform a security check.

        :return: True if the check passes, False otherwise.
        """
        raise NotImplementedError
