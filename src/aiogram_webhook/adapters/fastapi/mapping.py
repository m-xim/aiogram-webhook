from typing import Any

from starlette.datastructures import Headers, QueryParams

from aiogram_webhook.adapters.base_mapping import MappingABC


class FastApiHeadersMapping(MappingABC[Headers]):
    def getlist(self, name: str) -> list[Any]:
        return self._mapping.getlist(name)


class FastApiQueryMapping(MappingABC[QueryParams]):
    def getlist(self, name: str) -> list[Any]:
        return self._mapping.getlist(name)
