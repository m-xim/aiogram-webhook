from typing import Protocol

from aiogram_webhook.adapters.base_adapter import BoundRequest


class SecurityCheck(Protocol):
    """Protocol for security check on webhook requests."""

    async def verify(self, bot_token: str, bound_request: BoundRequest) -> bool:
        """
        Perform a security check.

        :param bot_token: Bot token used by token-aware checks.
        :return: True if the check passes, False otherwise.
        """
        raise NotImplementedError
