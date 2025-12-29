import pytest
from aiogram import Bot

from aiogram_webhook.routing.path import PathRouting
from aiogram_webhook.routing.query import QueryRouting
from tests.conftest import DummyBoundRequest


@pytest.mark.parametrize(
    ("url", "param", "expected_webhook", "params", "expected_key"),
    [
        ("https://example.com/webhook", None, "https://example.com/webhook", {"path_params": {}}, None),
        (
            "https://example.com/webhook/{bot_token}",
            "bot_token",
            "https://example.com/webhook/42:TEST",
            {"path_params": {"bot_token": "42:TEST"}},
            "42:TEST",
        ),
        (
            "https://example.com/webhook/{bot_token}",
            "bot_token",
            "https://example.com/webhook/42:TEST",
            {"path_params": {}},
            None,
        ),
    ],
)
def test_path_routing(url, param, expected_webhook, params, expected_key):
    routing = PathRouting(url=url, param=param)
    bot = Bot("42:TEST")
    assert routing.webhook_point(bot) == expected_webhook
    req = DummyBoundRequest(**params)
    assert routing.extract_key(req) == expected_key


@pytest.mark.parametrize(
    ("url", "param", "expected_webhook", "query_params", "expected_key"),
    [
        (
            "https://example.com/webhook?token={token}",
            "token",
            "https://example.com/webhook?token=42:TEST",
            {"token": "42:TEST"},
            "42:TEST",
        ),
        ("https://example.com/webhook?token={token}", "token", "https://example.com/webhook?token=42:TEST", {}, None),
    ],
)
def test_query_routing(url, param, expected_webhook, query_params, expected_key):
    routing = QueryRouting(url=url, param=param)
    bot = Bot("42:TEST")
    assert routing.webhook_point(bot) == expected_webhook
    req = DummyBoundRequest(query_params=query_params)
    assert routing.extract_key(req) == expected_key
