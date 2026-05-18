from dataclasses import dataclass

from aiogram.types import InputFile

from aiogram_webhook.utils.config import Omittable


@dataclass(frozen=True, slots=True)
class WebhookConfig:
    """Webhook configuration for setWebhook API parameters."""

    certificate: Omittable[InputFile | None] = None
    """Upload your public key certificate so that the root certificate in use can be checked. See our `self-signed guide <https://core.telegram.org/bots/self-signed>`_ for details."""
    ip_address: Omittable[str | None] = None
    """The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS"""
    max_connections: Omittable[int | None] = None
    """The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to *40*. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput."""
    allowed_updates: Omittable[list[str] | None] = None
    """A JSON-serialized list of the update types you want your bot to receive. For example, specify :code:`["message", "edited_channel_post", "callback_query"]` to only receive updates of these types. See :class:`aiogram.types.update.Update` for a complete list of available update types. Specify an empty list to receive all update types except *chat_member*, *message_reaction*, and *message_reaction_count* (default). If not specified, the previous setting will be used."""
    drop_pending_updates: Omittable[bool | None] = None
    """Pass :code:`True` to drop all pending updates"""
