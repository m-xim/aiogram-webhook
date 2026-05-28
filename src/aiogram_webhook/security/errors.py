import logging

from aiogram_webhook.errors import AiogramWebhookError


class SecurityError(AiogramWebhookError):
    code = "security_error"
    status_code = 403
    public_detail = "Forbidden"
    log_level = logging.WARNING


class SecretTokenError(SecurityError):
    code = "security_secret_token_invalid"
    status_code = 403
    public_detail = "Forbidden"
    log_level = logging.ERROR

    def __init__(self, *, target_bot_id: int) -> None:
        self.target_bot_id = target_bot_id

        super().__init__(
            f"Webhook security verification failed: invalid Telegram secret token. Target bot id: {target_bot_id}."
        )


class SecurityCheckError(SecurityError):
    code = "security_check_failed"
    status_code = 403
    public_detail = "Forbidden"
    log_level = logging.ERROR

    def __init__(self, *, security_check: str, client_ip: str | None = None) -> None:
        self.security_check = security_check
        self.client_ip = client_ip

        message = f"Webhook security verification failed: security check rejected request. Check: {security_check!r}."

        if client_ip is not None:
            message += f" Client IP: {client_ip}"

        super().__init__(message)
