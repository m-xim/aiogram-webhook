import pytest
from aiogram import Bot

from aiogram_webhook.routing.path import PathRouting
from aiogram_webhook.routing.query import QueryRouting
from aiogram_webhook.routing.static import StaticRouting
from tests.conftest import DummyBoundRequest


@pytest.fixture
def bot():
    return Bot("42:TEST")


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/webhook",
        "https://example.com/webhook/",
        "https://example.com/webhook/any/path",
        "https://example.com/webhook?foo=bar",
    ],
)
def test_static_routing(url, bot):
    routing = StaticRouting(url=url)
    assert routing.webhook_point(bot) == url


@pytest.mark.parametrize(
    ("url", "param", "token", "path_params", "expected_url", "expected_token"),
    [
        # Standard param, parameter present
        (
            "https://example.com/webhook/{token}",
            "token",
            "42:TEST",
            {"token": "42:TEST"},
            "https://example.com/webhook/42:TEST",
            "42:TEST",
        ),
        # Standard param, parameter missing
        ("https://example.com/webhook/{token}", "token", "42:TEST", {}, "https://example.com/webhook/42:TEST", None),
        # Custom param, parameter present
        (
            "https://example.com/webhook/{mytoken}",
            "mytoken",
            "42:TEST",
            {"mytoken": "42:TEST"},
            "https://example.com/webhook/42:TEST",
            "42:TEST",
        ),
        # Custom param, parameter missing
        (
            "https://example.com/webhook/{mytoken}",
            "mytoken",
            "42:TEST",
            {},
            "https://example.com/webhook/42:TEST",
            None,
        ),
    ],
)
def test_path_routing(url, param, token, path_params, expected_url, expected_token):
    routing = PathRouting(url=url, param=param)
    bot = Bot(token)
    assert routing.webhook_point(bot) == expected_url
    req = DummyBoundRequest(path_params=path_params)
    assert routing.extract_token(req) == expected_token


@pytest.mark.parametrize(
    ("url", "param", "token", "query_params", "expected_url", "expected_token"),
    [
        # Standard param, parameter present
        (
            "https://example.com/webhook?token={token}",
            "token",
            "42:TEST",
            {"token": "42:TEST"},
            "https://example.com/webhook?token=42:TEST",
            "42:TEST",
        ),
        # Standard param, parameter missing
        (
            "https://example.com/webhook?token={token}",
            "token",
            "42:TEST",
            {},
            "https://example.com/webhook?token=42:TEST",
            None,
        ),
        # Custom param, parameter present
        (
            "https://example.com/webhook?mytoken={mytoken}",
            "mytoken",
            "42:TEST",
            {"mytoken": "42:TEST"},
            "https://example.com/webhook?mytoken=42:TEST",
            "42:TEST",
        ),
        # Custom param, parameter missing
        (
            "https://example.com/webhook?mytoken={mytoken}",
            "mytoken",
            "42:TEST",
            {},
            "https://example.com/webhook?mytoken=42:TEST",
            None,
        ),
    ],
)
def test_query_routing(url, param, token, query_params, expected_url, expected_token):
    routing = QueryRouting(url=url, param=param)
    bot = Bot(token)
    assert routing.webhook_point(bot) == expected_url
    req = DummyBoundRequest(query_params=query_params)
    assert routing.extract_token(req) == expected_token
