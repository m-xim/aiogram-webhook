from collections.abc import Mapping
from typing import Protocol, TypeAlias

from aiogram_webhook.engines.target import Target

RouteParams: TypeAlias = Mapping[str, str]


class RouteParam(Protocol):
    async def build(self, target: Target, params: RouteParams) -> str:
        """
        Build raw path param value for an outgoing URL.

        Route will encode this value for URL path.
        """

    async def parse(self, value: str, params: RouteParams) -> str:
        """
        Parse incoming framework path param into a normalized route param value.
        """
