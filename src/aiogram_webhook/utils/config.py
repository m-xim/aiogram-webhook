from dataclasses import fields, is_dataclass
from functools import cache
from typing import Any, Final, TypeAlias, TypeVar, final

T = TypeVar("T")


@final
class OmittedType:
    __slots__ = ()

    def __repr__(self) -> str:
        return "OMITTED"

    def __bool__(self) -> bool:
        raise TypeError("OMITTED cannot be used in boolean context")


OMITTED: Final = OmittedType()

Omittable: TypeAlias = T | OmittedType


@cache
def dataclass_field_names(cls: type[Any]) -> tuple[str, ...]:
    return tuple(field.name for field in fields(cls))


def dataclass_config_to_kwargs(base: object, override: object | None = None) -> dict[str, Any]:
    if not is_dataclass(base) or isinstance(base, type):
        raise TypeError(f"Expected dataclass instance, got {type(base).__name__}")

    if override is not None and type(base) is not type(override):
        raise TypeError(f"Override config must be {type(base).__name__}, got {type(override).__name__}")

    kwargs: dict[str, Any] = {}

    for name in dataclass_field_names(type(base)):
        value = getattr(base, name)

        if override is not None:
            override_value = getattr(override, name)

            if override_value is not OMITTED:
                value = override_value

        if value is OMITTED or value is None:
            continue

        kwargs[name] = value

    return kwargs
