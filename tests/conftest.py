import pytest
from aiogram import Bot


@pytest.fixture
def bot():
    return Bot("42:TEST")
