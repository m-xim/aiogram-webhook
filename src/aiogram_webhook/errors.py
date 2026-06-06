import logging
from typing import ClassVar


class AiogramWebhookError(Exception):
    code: ClassVar[str] = "webhook_error"
    status_code: ClassVar[int] = 500
    public_detail: ClassVar[str] = "Internal server error"
    log_level: ClassVar[int] = logging.ERROR

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def response_payload(self) -> dict[str, str]:
        return {"detail": self.public_detail}
