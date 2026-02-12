from aiogram import Bot

from aiogram_webhook.adapters.base import BoundRequest
from aiogram_webhook.security.checks.check import Check


class PassingCheck(Check):
    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        return True


class FailingCheck(Check):
    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        return False


class ConditionalCheck(Check):
    def __init__(self, condition: bool):
        self.condition = condition

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        return self.condition
