from collections.abc import Mapping

from aiohttp import Payload
from aiohttp.abc import AbstractStreamWriter
from multidict import CIMultiDict
from starlette.responses import Response
from starlette.types import Receive, Scope, Send


class _ASGIStreamWriter(AbstractStreamWriter):
    __slots__ = ("_send",)

    def __init__(self, send: Send) -> None:
        self._send = send

    async def write(self, chunk: bytes | bytearray | memoryview) -> None:
        body = chunk if isinstance(chunk, bytes) else bytes(chunk)
        await self._send({"type": "http.response.body", "body": body, "more_body": True})

    async def write_eof(self, chunk: bytes = b"") -> None:
        if chunk:
            await self.write(chunk)

    async def drain(self) -> None:
        return None

    def enable_compression(self, encoding: str = "deflate", strategy: int | None = None) -> None:  # noqa: ARG002
        return None

    def enable_chunking(self) -> None:
        return None

    async def write_headers(self, status_line: str, headers: CIMultiDict[str]) -> None:  # noqa: ARG002
        return None


class AiohttpPayloadResponse(Response):
    def __init__(self, *, status_code: int, payload: Payload, headers: Mapping[str, str] | None = None) -> None:
        response_headers = dict(payload.headers)
        if headers is not None:
            response_headers.update(headers)

        has_content_length = "content-length" in {name.lower() for name in response_headers}

        super().__init__(content=b"", status_code=status_code, headers=response_headers)
        self.payload = payload

        if not has_content_length:
            self.raw_headers = [(name, value) for name, value in self.raw_headers if name != b"content-length"]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:  # noqa: ARG002
        await send({"type": "http.response.start", "status": self.status_code, "headers": self.raw_headers})
        await self.payload.write(_ASGIStreamWriter(send))
        await send({"type": "http.response.body", "body": b"", "more_body": False})
