from typing import Any

from multidict import CIMultiDictProxy, MultiMapping

from aiogram_webhook.adapters.base_mapping import MappingABC


class AiohttpHeadersMapping(MappingABC[CIMultiDictProxy[str]]):
    def getlist(self, name: str) -> list[Any]:
        return self._mapping.getall(name, [])


class AiohttpQueryMapping(MappingABC[MultiMapping[str]]):
    def getlist(self, name: str) -> list[Any]:
        return self._mapping.getall(name, [])
