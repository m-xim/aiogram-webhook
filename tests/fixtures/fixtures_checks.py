from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.security.checks.check import SecurityCheck
from aiogram_webhook.web.base import WebRequest


class PassingCheck(SecurityCheck):
    async def verify(self, target: Target, request: WebRequest, route_params: RouteParams) -> bool:
        return True


class FailingCheck(SecurityCheck):
    async def verify(self, target: Target, request: WebRequest, route_params: RouteParams) -> bool:
        return False


class ConditionalCheck(SecurityCheck):
    def __init__(self, condition: bool):
        self.condition = condition

    async def verify(self, target: Target, request: WebRequest, route_params: RouteParams) -> bool:
        return self.condition
