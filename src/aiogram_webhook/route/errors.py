import logging
from collections.abc import Iterable

from yarl import URL

from aiogram_webhook.errors import AiogramWebhookError


def format_names(names: Iterable[str]) -> str:
    return ", ".join(repr(name) for name in sorted(names))


class RouteError(AiogramWebhookError):
    code = "route_error"


class RouteConfigError(RouteError):
    status_code = 500
    public_detail = "Internal server error"
    log_level = logging.ERROR


class RouteBuildError(RouteError):
    status_code = 500
    public_detail = "Internal server error"
    log_level = logging.ERROR


class RouteMatchError(RouteError):
    status_code = 404
    public_detail = "Not found"
    log_level = logging.INFO


class InvalidBaseUrlError(RouteConfigError):
    code = "route_config_invalid_base_url"

    def __init__(self, *, base_url: URL, reason: str) -> None:
        self.base_url = base_url
        self.reason = reason

        super().__init__(f"Invalid Route base_url. Reason: {reason}. base_url={base_url}.")


class InvalidRoutePathError(RouteConfigError):
    code = "route_config_invalid_path"

    def __init__(self, *, path: URL, reason: str) -> None:
        self.path = path
        self.reason = reason

        super().__init__(f"Invalid Route path. Reason: {reason}. path={path!r}.")


class InvalidPathTemplateError(RouteConfigError):
    code = "route_config_invalid_path_template"

    def __init__(self, *, path: str, reason: str, value: str | None = None) -> None:
        self.path = path
        self.reason = reason
        self.value = value

        message = f"Invalid Route path template. Reason: {reason}. path={path!r}."

        if value is not None:
            message += f" Value: {value!r}."

        super().__init__(message)


class RepeatedPathParamError(RouteConfigError):
    code = "route_config_repeated_path_params"

    def __init__(self, *, path: str, repeated_params: Iterable[str]) -> None:
        self.path = path
        self.repeated_params = tuple(sorted(repeated_params))

        super().__init__(
            "Invalid Route config: repeated path params are not supported. "
            f"path={path!r}. "
            f"Repeated params: {format_names(self.repeated_params)}."
        )


class MissingRouteParamDeclarationError(RouteConfigError):
    code = "route_config_missing_param_declarations"

    def __init__(self, *, path: str, missing_params: Iterable[str]) -> None:
        self.path = path
        self.missing_params = tuple(sorted(missing_params))

        super().__init__(
            "Invalid Route config: some path params are not declared in Route(params=...). "
            f"path={path!r}. "
            f"Missing declarations: {format_names(self.missing_params)}."
        )


class UnusedRouteParamDeclarationError(RouteConfigError):
    code = "route_config_unused_param_declarations"

    def __init__(self, *, path: str, unused_params: Iterable[str]) -> None:
        self.path = path
        self.unused_params = tuple(sorted(unused_params))

        super().__init__(
            "Invalid Route config: some Route(params=...) declarations are not used in path. "
            f"path={path!r}. "
            f"Unused declarations: {format_names(self.unused_params)}."
        )


class UnknownQueryParamReferenceError(RouteConfigError):
    code = "route_config_unknown_query_param_refs"

    def __init__(self, *, path: str, unknown_params: Iterable[str]) -> None:
        self.path = path
        self.unknown_params = tuple(sorted(unknown_params))

        super().__init__(
            "Invalid Route config: query references params that are not declared in path. "
            f"path={path!r}. "
            f"Unknown params: {format_names(self.unknown_params)}."
        )


class RouteBuildMissingParamError(RouteBuildError):
    code = "route_build_missing_param"

    def __init__(self, *, path: str, param: str) -> None:
        self.path = path
        self.param = param

        super().__init__(f"Failed to build URL: missing route param. path={path!r}. param={param!r}.")


class RouteBuildInvalidPathTemplateError(RouteBuildError):
    code = "route_build_invalid_path_template"

    def __init__(self, *, path: str) -> None:
        self.path = path

        super().__init__(f"Failed to build URL: invalid path template. path={path!r}.")


class MissingPathParamError(RouteMatchError):
    code = "route_match_missing_path_param"

    def __init__(self, *, param: str, available_params: Iterable[str]) -> None:
        self.param = param
        self.available_params = tuple(sorted(available_params))

        super().__init__(
            "Incoming request does not match route: missing path param. "
            f"param={param!r}. "
            f"Available path params: {format_names(self.available_params)}."
        )


class InvalidPathParamError(RouteMatchError):
    code = "route_match_invalid_path_param"

    def __init__(self, *, param: str, value: str) -> None:
        self.param = param
        self.value = value

        super().__init__(
            f"Incoming request does not match route: path param value is invalid. param={param!r}. value={value!r}."
        )


class MissingQueryParamError(RouteMatchError):
    code = "route_match_missing_query_param"

    def __init__(self, *, query_param: str, available_query_params: Iterable[str]) -> None:
        self.query_param = query_param
        self.available_query_params = tuple(sorted(available_query_params))

        super().__init__(
            "Incoming request does not match route: missing query param. "
            f"query_param={query_param!r}. "
            f"Available query params: {format_names(self.available_query_params)}."
        )


class QueryParamMismatchError(RouteMatchError):
    code = "route_match_query_param_mismatch"

    def __init__(self, *, query_param: str, expected: Iterable[str], got: Iterable[str]) -> None:
        self.query_param = query_param
        self.expected = tuple(expected)
        self.got = tuple(got)

        super().__init__(
            "Incoming request does not match route: query param values mismatch. "
            f"query_param={query_param!r}. "
            f"Expected values: {self.expected!r}. "
            f"Got values: {self.got!r}."
        )


class UnexpectedQueryParamError(RouteMatchError):
    code = "route_match_unexpected_query_param"

    def __init__(self, *, query_params: Iterable[str], expected_query_params: Iterable[str]) -> None:
        self.query_params = tuple(sorted(query_params))
        self.expected_query_params = tuple(sorted(expected_query_params))

        super().__init__(
            "Incoming request does not match route: unexpected query params. "
            f"Unexpected query params: {format_names(self.query_params)}. "
            f"Expected query params: {format_names(self.expected_query_params)}."
        )
