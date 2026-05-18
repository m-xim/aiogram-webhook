import logging
from typing import Final

from aiogram_webhook.errors import AiogramWebhookError

LOGGER_NAME: Final[str] = "aiogram_webhook"


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{LOGGER_NAME}.{name}")


def log_webhook_error(logger: logging.Logger, exc: AiogramWebhookError) -> None:
    logger.log(
        exc.log_level,
        "Webhook request failed: %s: %s",
        exc.code,
        exc,
        extra={"error_type": exc.__class__.__name__, "status_code": exc.status_code},
    )
