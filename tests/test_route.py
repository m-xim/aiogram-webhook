import pytest

from aiogram_webhook.engines.target import Target
from aiogram_webhook.route import BotTokenParam, Const, Ref, Route
from aiogram_webhook.route.errors import InvalidRoutePathError, MissingQueryParamError
from tests.fixtures import DummyRequest, dummy_web_request


@pytest.mark.asyncio
async def test_route_builds_static_webhook_url(bot):
    route = Route(base_url="https://example.com", path="/webhook")
    target = Target(bot_id=bot.id, bot_token=bot.token)

    assert await route.build_url(target=target) == "https://example.com/webhook"


def test_route_rejects_path_without_leading_slash():
    with pytest.raises(InvalidRoutePathError):
        Route(base_url="https://example.com", path="webhook/{bot_token}", params={"bot_token": BotTokenParam()})


@pytest.mark.asyncio
async def test_route_matches_standardized_path_params(bot):
    route = Route(
        base_url="https://example.com",
        path="/webhook/{bot_token}",
        params={"bot_token": BotTokenParam()},
    )

    request = dummy_web_request(DummyRequest(path_params={"bot_token": "42:TEST"}))
    target = Target(bot_id=bot.id, bot_token=bot.token)

    assert await route.build_url(target=target) == "https://example.com/webhook/42%3ATEST"
    assert await route.match(request) == {"bot_token": "42:TEST"}


@pytest.mark.asyncio
async def test_route_matches_repeated_standardized_query_params():
    route = Route(
        base_url="https://example.com",
        path="/webhook/{bot_token}",
        params={"bot_token": BotTokenParam()},
        query={"token": Ref("bot_token"), "kind": (Const("telegram"), "webhook")},
    )
    request = dummy_web_request(
        DummyRequest(
            path_params={"bot_token": "42:TEST"},
            query=[("token", "42:TEST"), ("kind", "telegram"), ("kind", "webhook")],
        )
    )

    assert await route.match(request) == {"bot_token": "42:TEST"}


@pytest.mark.asyncio
async def test_route_reports_missing_query_param():
    route = Route(
        base_url="https://example.com",
        path="/webhook/{bot_token}",
        params={"bot_token": BotTokenParam()},
        query={"token": Ref("bot_token")},
    )
    request = dummy_web_request(DummyRequest(path_params={"bot_token": "42:TEST"}))

    with pytest.raises(MissingQueryParamError):
        await route.match(request)


@pytest.mark.asyncio
async def test_route_reports_available_query_param_names():
    route = Route(
        base_url="https://example.com",
        path="/webhook/{bot_token}",
        params={"bot_token": BotTokenParam()},
        query={"token": Ref("bot_token")},
    )
    request = dummy_web_request(DummyRequest(path_params={"bot_token": "42:TEST"}, query={"other": "value"}))

    with pytest.raises(MissingQueryParamError) as exc_info:
        await route.match(request)

    assert exc_info.value.available_query_params == ("other",)
