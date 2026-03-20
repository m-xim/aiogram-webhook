from ipaddress import IPv4Address

import pytest
from aiogram import Bot, Dispatcher


@pytest.fixture
def bot():
    return Bot("42:TEST")


@pytest.fixture
def dispatcher() -> Dispatcher:
    return Dispatcher()


@pytest.fixture
def localhost_ip() -> IPv4Address:
    return IPv4Address("127.0.0.1")
