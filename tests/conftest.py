from ipaddress import IPv4Address

import pytest
from aiogram import Bot


@pytest.fixture
def bot():
    return Bot("42:TEST")


@pytest.fixture
def localhost_ip() -> IPv4Address:
    return IPv4Address("127.0.0.1")
