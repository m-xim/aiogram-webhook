from aiogram.types import InputFile
from pydantic import BaseModel, ConfigDict, Field


class WebhookConfig(BaseModel):
    """Webhook configuration for setWebhook API parameters."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    certificate: InputFile | None = None
    """Upload your public key certificate so that the root certificate in use can be checked. See our `self-signed guide <https://core.telegram.org/bots/self-signed>`_ for details."""
    ip_address: str | None = None
    """The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS"""
    max_connections: int | None = Field(default=None, ge=1, le=100)
    """The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to *40*. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput."""
    allowed_updates: list[str] | None = None
    """A JSON-serialized list of the update types you want your bot to receive. For example, specify :code:`["message", "edited_channel_post", "callback_query"]` to only receive updates of these types. See :class:`aiogram.types.update.Update` for a complete list of available update types. Specify an empty list to receive all update types except *chat_member*, *message_reaction*, and *message_reaction_count* (default). If not specified, the previous setting will be used."""
    drop_pending_updates: bool | None = None
    """Pass :code:`True` to drop all pending updates"""
