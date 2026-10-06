import asyncio

import pytest

from aiogram_webhook.engines.errors import RequestHandlingStoppedError
from aiogram_webhook.gate import RequestGate


@pytest.mark.asyncio
async def test_closed_gate_rejects_and_reopened_gate_admits():
    gate = RequestGate()
    await gate.close()

    with pytest.raises(RequestHandlingStoppedError), gate.enter():
        pytest.fail("closed gate must not admit")
    with pytest.raises(RequestHandlingStoppedError):
        gate.ensure_open()

    gate.open()
    with gate.enter():
        pass


@pytest.mark.asyncio
async def test_close_waits_until_admitted_request_leaves():
    gate = RequestGate()
    inside = asyncio.Event()
    release = asyncio.Event()

    async def request() -> None:
        with gate.enter():
            inside.set()
            await release.wait()

    request_task = asyncio.create_task(request())
    await inside.wait()

    closing = asyncio.create_task(gate.close())
    await asyncio.sleep(0)
    assert not closing.done()

    release.set()
    await request_task
    assert await closing is True


@pytest.mark.asyncio
async def test_close_gives_up_after_timeout():
    gate = RequestGate()

    with gate.enter():
        assert await gate.close(timeout=0.01) is False
