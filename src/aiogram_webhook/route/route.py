from collections import Counter
from collections.abc import Mapping
from string import Formatter
from typing import TypeVar
from urllib.parse import quote

from yarl import URL

from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.errors import (
    EmptyPathParamError,
    InvalidBaseUrlError,
    InvalidPathTemplateError,
    InvalidRoutePathError,
    MissingPathParamError,
    MissingQueryParamError,
    MissingRouteParamDeclarationError,
    QueryParamMismatchError,
    RepeatedPathParamError,
    RouteBuildInvalidPathTemplateError,
    RouteBuildMissingParamError,
    UnknownQueryParamReferenceError,
    UnusedRouteParamDeclarationError,
)
from aiogram_webhook.route.params import RouteParam, RouteParams
from aiogram_webhook.route.query import QueryInput, QueryValue, normalize_query
from aiogram_webhook.web.base import WebRequest

RawRequestT = TypeVar("RawRequestT")


class Route:
    """Universal web route"""

    __slots__ = (
        "_base_url",
        "_params",
        "_path_param_names",
        "_path_params",
        "_path_template",
        "_query",
        "_query_items"
    )

    def __init__(
        self,
        *,
        base_url: str | URL,
        path: str | URL,
        params: Mapping[str, RouteParam] | None = None,
        query: Mapping[str, QueryInput] | None = None,
    ) -> None:
        self._base_url = self._prepare_base_url(base_url)
        self._path_template = self._prepare_path(path)
        self._path_param_names = self._extract_path_param_names(self._path_template)

        self._params = dict(params or {})
        self._query = normalize_query(query or {})
        self._path_params = tuple((name, self._params[name]) for name in self._path_param_names)
        self._query_items = tuple(self._query.items())

        self._validate_config()

    @property
    def path(self) -> str:
        """
        Get path template for route registration in a web framework.

        This is not a full URL, only the path part, for example "/webhook/{bot_id}".
        """
        return self._path_template

    async def build_url(self, target: Target) -> str:
        route_params = await self._build_params(target)

        path_params = {name: quote(value, safe="") for name, value in route_params.items()}
        try:
            path = self._path_template.format_map(path_params)
        except KeyError as exc:
            raise RouteBuildMissingParamError(path=self._path_template, param=str(exc.args[0])) from exc
        except ValueError as exc:
            raise RouteBuildInvalidPathTemplateError(path=self._path_template) from exc

        url = self._base_url.with_path(path, encoded=True)

        if self._query_items:
            url = url.with_query([
                (name, value.render(route_params)) for name, values in self._query_items for value in values
            ])

        return str(url)

    async def match(self, request: WebRequest[RawRequestT]) -> RouteParams:
        route_params = await self._parse_params(request)

        if self._query_items:
            self._check_query(request=request, params=route_params)

        return route_params

    async def _build_params(self, target: Target) -> dict[str, str]:
        route_params: dict[str, str] = {}

        for name, route_param in self._path_params:
            route_params[name] = await route_param.build(target=target, params=route_params)

        return route_params

    async def _parse_params(self, request: WebRequest[RawRequestT]) -> dict[str, str]:
        route_params: dict[str, str] = {}

        path_params = request.path_params

        for name, route_param in self._path_params:
            raw_value = path_params.get(name)

            if raw_value is None:
                raise MissingPathParamError(param=name, available_params=route_params)

            if raw_value == "":
                raise EmptyPathParamError(param=name)

            route_params[name] = await route_param.parse(value=raw_value, params=route_params)
        return route_params

    def _check_query(self, *, request: WebRequest[RawRequestT], params: RouteParams) -> None:
        query_params = request.query_params

        for name, expected_values in self._query_items:
            actual = query_params.getall(name, [])

            if not actual:
                raise MissingQueryParamError(query_param=name, available_query_params=query_params.keys())

            expected = [value.render(params) for value in expected_values]

            if sorted(actual) != sorted(expected):
                raise QueryParamMismatchError(query_param=name, expected=expected, got=actual)

    def _validate_config(self) -> None:
        declared_param_names = set(self._params)
        path_param_names = set(self._path_param_names)

        if repeated_path_params := [name for name, count in Counter(self._path_param_names).items() if count > 1]:
            raise RepeatedPathParamError(path=self._path_template, repeated_params=repeated_path_params)

        if missing_params := path_param_names - declared_param_names:
            raise MissingRouteParamDeclarationError(path=self._path_template, missing_params=missing_params)

        if unused_params := declared_param_names - path_param_names:
            raise UnusedRouteParamDeclarationError(path=self._path_template, unused_params=unused_params)

        unknown_query_param_refs: set[str] = set()
        for _, values in self._query_items:
            for value in values:
                unknown_query_param_refs.update(value.required_params())

        if unknown_query_param_refs := unknown_query_param_refs - path_param_names:
            raise UnknownQueryParamReferenceError(path=self._path_template, unknown_params=unknown_query_param_refs)

    @staticmethod
    def _prepare_base_url(base_url: str | URL) -> URL:
        if not isinstance(base_url, URL):
            base_url = URL(base_url)

        if not base_url.is_absolute():
            raise InvalidBaseUrlError(
                base_url=base_url, reason="base_url must be an absolute URL, for example 'https://example.com'"
            )
        if base_url.query_string:
            raise InvalidBaseUrlError(
                base_url=base_url, reason="base_url must not contain query params; move them to Route(query=...)"
            )
        if base_url.fragment:
            raise InvalidBaseUrlError(base_url=base_url, reason="URL fragment is not supported for route")

        return base_url

    @staticmethod
    def _prepare_path(path: str | URL) -> str:
        if not isinstance(path, URL):
            path = URL(path)

        if path.is_absolute():
            raise InvalidRoutePathError(path=path, reason="path must be a relative path starting with '/'")
        if not path.path.startswith("/"):
            raise InvalidRoutePathError(path=path, reason="path must be a relative path starting with '/'")
        if path.query_string:
            raise InvalidRoutePathError(
                path=path, reason="path must not contain query params; move them to Route(query=...)"
            )
        if path.fragment:
            raise InvalidRoutePathError(path=path, reason="URL fragment is not supported for route")

        return path.human_repr()

    @staticmethod
    def _extract_path_param_names(path_template: str) -> tuple[str, ...]:
        names: list[str] = []

        try:
            parsed = Formatter().parse(path_template)
        except ValueError as exc:
            raise InvalidPathTemplateError(path=path_template, reason="malformed path template") from exc

        for _, field_name, format_spec, conversion in parsed:
            if field_name is None:
                continue

            if not field_name:
                raise InvalidPathTemplateError(
                    path=path_template, reason="empty path param name is not supported", value="{}"
                )
            if format_spec:
                raise InvalidPathTemplateError(
                    path=path_template,
                    reason="path param converters are not supported; use '{name}' only",
                    value=f"{{{field_name}:{format_spec}}}",
                )
            if conversion:
                raise InvalidPathTemplateError(
                    path=path_template,
                    reason="path param conversions are not supported; use '{name}' only",
                    value=f"{{{field_name}!{conversion}}}",
                )
            if not field_name.isidentifier():
                raise InvalidPathTemplateError(
                    path=path_template, reason="path param name must be a valid Python identifier", value=field_name
                )

            names.append(field_name)

        return tuple(names)
