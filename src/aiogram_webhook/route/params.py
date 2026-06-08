from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

from aiogram_webhook.engines.target import Target

RouteParams: TypeAlias = Mapping[str, Any]


class RouteParam(Protocol):
    async def build(self, target: Target, params: RouteParams) -> str:
        """
        Build raw path param value for an outgoing URL.

        Route will encode this value for URL path.
        """

    async def parse(self, value: str, params: RouteParams) -> Any:
        """
        Parse incoming framework path param into a normalized route param value.
        """


@dataclass(frozen=True, slots=True)
class RouteParamBinding:
    name: str
    param: RouteParam


class BotIdParam(RouteParam):
    async def build(self, target: Target, params: RouteParams) -> str:  # noqa: ARG002
        return str(target.bot_id)

    async def parse(self, value: str, params: RouteParams) -> int:  # noqa: ARG002
        return int(value)


class BotTokenParam(RouteParam):
    async def build(self, target: Target, params: RouteParams) -> str:  # noqa: ARG002
        return target.bot_token

    async def parse(self, value: str, params: RouteParams) -> str:  # noqa: ARG002
        return value
