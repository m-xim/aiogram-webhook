import asyncio
from collections.abc import Iterator
from contextlib import contextmanager

from aiogram_webhook.engines.errors import RequestHandlingStoppedError
from aiogram_webhook.logs import get_logger

logger = get_logger("gate")


class RequestGate:
    """Admit requests while open; on close, reject new ones and wait for those already inside."""

    def __init__(self) -> None:
        self._closed = False
        self._active = 0
        self._idle = asyncio.Event()
        self._idle.set()

    def ensure_open(self) -> None:
        if self._closed:
            raise RequestHandlingStoppedError

    @contextmanager
    def enter(self) -> Iterator[None]:
        self.ensure_open()
        self._active += 1
        self._idle.clear()
        try:
            yield
        finally:
            self._active -= 1
            if not self._active:
                self._idle.set()

    def open(self) -> None:
        self._closed = False

    async def close(self, timeout: float | None = None) -> bool:
        self._closed = True
        if self._active:
            logger.info("Waiting for %s in-flight request(s) to finish", self._active)
        try:
            await asyncio.wait_for(self._idle.wait(), timeout)
        except asyncio.TimeoutError:
            logger.warning("Timeout reached. %s request(s) still in flight.", self._active)
            return False
        return True
