from abc import ABC, abstractmethod
from collections.abc import ItemsView, KeysView, Mapping, ValuesView
from typing import Any, Generic, TypeVar

M = TypeVar("M", bound=Mapping)


class MappingABC(ABC, Generic[M]):
    def __init__(self, mapping: M):
        self._mapping = mapping

    def get(self, name: str, default=None):
        return self._mapping.get(name, default)

    @abstractmethod
    def getlist(self, name: str) -> list[Any]:
        raise NotImplementedError

    def __getitem__(self, name: str) -> Any:
        return self._mapping[name]

    def __contains__(self, name: str) -> bool:
        return name in self.keys()

    def keys(self) -> KeysView:
        return self._mapping.keys()

    def values(self) -> ValuesView:
        return self._mapping.values()

    def items(self) -> ItemsView:
        return self._mapping.items()
