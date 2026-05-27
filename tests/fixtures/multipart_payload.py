from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from email.parser import BytesParser
from email.policy import default

from aiohttp import Payload
from aiohttp.abc import AbstractStreamWriter
from multidict import CIMultiDict


class MemoryStreamWriter(AbstractStreamWriter):
    def __init__(self) -> None:
        self.chunks: list[bytes] = []

    async def write(self, chunk: bytes | bytearray | memoryview) -> None:
        self.chunks.append(bytes(chunk))

    async def write_eof(self, chunk: bytes = b"") -> None:
        if chunk:
            await self.write(chunk)

    async def drain(self) -> None:
        return None

    def enable_compression(self, encoding: str = "deflate", strategy: int | None = None) -> None:
        return None

    def enable_chunking(self) -> None:
        return None

    async def write_headers(self, status_line: str, headers: CIMultiDict[str]) -> None:
        return None


@dataclass(frozen=True, slots=True)
class MultipartPart:
    name: str
    body: bytes
    filename: str | None = None


async def render_payload(payload: Payload) -> bytes:
    writer = MemoryStreamWriter()
    await payload.write(writer)
    return b"".join(writer.chunks)


def parse_multipart(content_type: str, body: bytes) -> list[MultipartPart]:
    message = BytesParser(policy=default).parsebytes(
        f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode() + body
    )

    assert message.is_multipart()

    parts: list[MultipartPart] = []
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        if not isinstance(name, str):
            raise TypeError("Multipart part must have a string form-data name.")

        part_body = part.get_payload(decode=True)
        if not isinstance(part_body, bytes):
            raise TypeError(f"Multipart part {name!r} must have a bytes body.")

        parts.append(
            MultipartPart(
                name=name,
                filename=part.get_filename(),
                body=part_body,
            )
        )

    return parts


def assert_multipart_fields(content_type: str, body: bytes, expected: Mapping[str, str]) -> list[MultipartPart]:
    assert content_type.startswith("multipart/form-data; boundary=webhookBoundary")

    parts = parse_multipart(content_type, body)
    plain_parts = {part.name: part for part in parts if part.filename is None}

    assert plain_parts.keys() >= expected.keys()
    for name, value in expected.items():
        assert plain_parts[name].body == value.encode()

    return parts


async def assert_payload_fields(payload: Payload, expected: Mapping[str, str]) -> list[MultipartPart]:
    return assert_multipart_fields(payload.headers["Content-Type"], await render_payload(payload), expected)


def assert_attached_file(parts: Iterable[MultipartPart], *, field: str, filename: str, body: bytes) -> None:
    parts_by_name = {part.name: part for part in parts}

    field_part = parts_by_name[field]
    assert field_part.body.startswith(b"attach://")

    file_key = field_part.body.removeprefix(b"attach://").decode()
    file_part = parts_by_name[file_key]

    assert file_part.filename == filename
    assert file_part.body == body
