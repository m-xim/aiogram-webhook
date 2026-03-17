from typing import Protocol

from aiogram_webhook.adapters.base_adapter import BoundRequest


class SecurityCheck(Protocol):
    """Protocol for security check on webhook requests."""

    async def verify(self, token: str, bound_request: BoundRequest) -> bool:
        """
        Perform a security check.

        :return: True if the check passes, False otherwise.
        """
        raise NotImplementedError
