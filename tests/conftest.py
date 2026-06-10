import pytest
from aiogram import Bot

from aiogram_webhook.engines.target import Target
from tests.fixtures.web_request import DummyRequest, DummyWebRequest
from tests.fixtures.webhook_engine import CapturingAdapter, DummyDispatcher


@pytest.fixture
def bot_id() -> int:
    return 42


@pytest.fixture
def bot_token(bot_id: int) -> str:
    return f"{bot_id}:TEST"


@pytest.fixture
def bot(bot_token: str) -> Bot:
    return Bot(bot_token)


@pytest.fixture
def target(bot_id: int, bot_token: str) -> Target:
    return Target(bot_id=bot_id, bot_token=bot_token)


@pytest.fixture
def adapter() -> CapturingAdapter:
    return CapturingAdapter()


@pytest.fixture
def update_request() -> DummyWebRequest:
    return DummyWebRequest(DummyRequest(json_data={"update_id": 1}))


@pytest.fixture
def dispatcher() -> DummyDispatcher:
    return DummyDispatcher()
