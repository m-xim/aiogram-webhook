import pytest
from aiogram import Bot

from aiogram_webhook.routing.path import PathRouting
from aiogram_webhook.routing.query import QueryRouting
from aiogram_webhook.routing.static import StaticRouting
from tests.fixtures import DummyBoundRequest


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
        (
            "https://example.com/webhook/{token}",
            "token",
            "42:TEST",
            {"token": "42:TEST"},
            "https://example.com/webhook/42:TEST",
            "42:TEST",
        ),
        ("https://example.com/webhook/{token}", "token", "42:TEST", {}, "https://example.com/webhook/42:TEST", None),
        (
            "https://example.com/webhook/{mytoken}",
            "mytoken",
            "42:TEST",
            {"mytoken": "42:TEST"},
            "https://example.com/webhook/42:TEST",
            "42:TEST",
        ),
        (
            "https://example.com/webhook/{mytoken}",
            "mytoken",
            "42:TEST",
            {},
            "https://example.com/webhook/42:TEST",
            None,
        ),
    ],
    ids=["standard-param-present", "standard-param-missing", "custom-param-present", "custom-param-missing"],
)
def test_path_routing(url, param, token, path_params, expected_url, expected_token):
    routing = PathRouting(url=url, param=param)
    assert routing.webhook_point(Bot(token)) == expected_url
    req = DummyBoundRequest(path_params=path_params)
    assert routing.extract_token(req) == expected_token


@pytest.mark.parametrize(
    ("url", "param", "token", "query_params", "expected_url", "expected_token"),
    [
        (
            "https://example.com/webhook?token={token}",
            "token",
            "42:TEST",
            {"token": "42:TEST"},
            "https://example.com/webhook?token=42:TEST",
            "42:TEST",
        ),
        (
            "https://example.com/webhook?token={token}",
            "token",
            "42:TEST",
            {},
            "https://example.com/webhook?token=42:TEST",
            None,
        ),
        (
            "https://example.com/webhook?mytoken={mytoken}",
            "mytoken",
            "42:TEST",
            {"mytoken": "42:TEST"},
            "https://example.com/webhook?mytoken=42:TEST",
            "42:TEST",
        ),
        (
            "https://example.com/webhook?mytoken={mytoken}",
            "mytoken",
            "42:TEST",
            {},
            "https://example.com/webhook?mytoken=42:TEST",
            None,
        ),
    ],
    ids=["standard-param-present", "standard-param-missing", "custom-param-present", "custom-param-missing"],
)
def test_query_routing(url, param, token, query_params, expected_url, expected_token):
    routing = QueryRouting(url=url, param=param)
    assert routing.webhook_point(Bot(token)) == expected_url
    req = DummyBoundRequest(query_params=query_params)
    assert routing.extract_token(req) == expected_token
