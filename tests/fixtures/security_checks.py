from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.security.checks.check import SecurityCheck
from aiogram_webhook.web.base import WebRequest


class RecordingCheck(SecurityCheck):
    def __init__(self, name: str, *, result: bool, calls: list[str]) -> None:
        self.name = name
        self.result = result
        self.calls = calls

    async def verify(self, target: Target, request: WebRequest, route_params: RouteParams) -> bool:
        self.calls.append(self.name)
        return self.result
