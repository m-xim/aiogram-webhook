from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TypeAlias

from aiogram_webhook.route.errors import RouteConfigError, RouteError
from aiogram_webhook.route.params import RouteParams


class QueryValue(ABC):
    @abstractmethod
    def render(self, params: RouteParams) -> str:
        raise NotImplementedError

    @abstractmethod
    def required_params(self) -> set[str]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Ref(QueryValue):
    """
    Query value copied from route params.

    Example:
        query={"bot_id": Ref("bot_id")}
    """

    name: str

    def render(self, params: RouteParams) -> str:
        if self.name not in params:
            raise RouteError(f"Failed to render query value: referenced route param is missing. Param: {self.name!r}.")

        return str(params[self.name])

    def required_params(self) -> set[str]:
        return {self.name}


@dataclass(frozen=True, slots=True)
class Const(QueryValue):
    """
    Static query value.

    Usually created internally from str/int.
    """

    value: str | int

    def render(self, params: RouteParams) -> str:  # noqa: ARG002
        return str(self.value)

    def required_params(self) -> set[str]:
        return set()


QueryScalar: TypeAlias = QueryValue | str | int
QueryInput: TypeAlias = QueryScalar | list[QueryScalar] | tuple[QueryScalar, ...]


def normalize_query(query: Mapping[str, QueryInput]) -> dict[str, tuple[QueryValue, ...]]:
    normalized: dict[str, tuple[QueryValue, ...]] = {}

    for name, value in query.items():
        if isinstance(value, QueryValue):
            normalized[name] = (value,)
            continue

        if isinstance(value, str | int):
            normalized[name] = (Const(value),)
            continue

        if not value:
            raise RouteConfigError(
                f"Invalid Route config: query param must contain at least one value. Param: {name!r}."
            )

        values: list[QueryValue] = []
        for item in value:
            if isinstance(item, QueryValue):
                values.append(item)
            else:
                values.append(Const(item))

        normalized[name] = tuple(values)

    return normalized
