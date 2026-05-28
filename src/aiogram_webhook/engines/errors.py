import logging
from collections.abc import Iterable

from aiogram_webhook.errors import AiogramWebhookError


def format_names(names: Iterable[str]) -> str:
    return ", ".join(repr(name) for name in sorted(names))


class EngineError(AiogramWebhookError):
    code = "engine_error"


class TargetNotFoundError(EngineError):
    code = "engine_target_not_found"
    status_code = 404
    public_detail = "Not found"
    log_level = logging.INFO

    def __init__(self, *, route_param_names: Iterable[str]) -> None:
        self.route_param_names = tuple(sorted(route_param_names))

        super().__init__(f"Webhook target was not found. Route param names: {format_names(self.route_param_names)}.")


class BotNotFoundError(EngineError):
    code = "engine_bot_not_found"
    status_code = 404
    public_detail = "Not found"
    log_level = logging.ERROR

    def __init__(
        self,
        *,
        target_bot_id: int | None = None,
        target_type: str | None = None,
    ) -> None:
        self.target_bot_id = target_bot_id
        self.target_type = target_type

        message = "Webhook bot was not found."

        if target_bot_id is not None:
            message += f" Target bot id: {target_bot_id}."

        if target_type is not None:
            message += f" Target type: {target_type!r}."

        super().__init__(message)


class InvalidJsonError(EngineError):
    code = "engine_invalid_json"
    status_code = 400
    public_detail = "Bad request"
    log_level = logging.ERROR

    def __init__(self, *, original_error: BaseException | None = None) -> None:
        self.original_error_type = type(original_error).__name__ if original_error is not None else None

        message = "Invalid webhook JSON payload."

        if self.original_error_type is not None:
            message += f" Original error type: {self.original_error_type}."

        super().__init__(message)


class RequestHandlingStoppedError(EngineError):
    code = "engine_request_handling_stopped"
    status_code = 503
    public_detail = "Service unavailable"
    log_level = logging.DEBUG

    def __init__(self) -> None:
        super().__init__("Webhook engine is shutting down and no longer accepts requests.")
