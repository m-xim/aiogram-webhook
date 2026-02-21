from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network, ip_address, ip_network
from typing import Final

from aiogram_webhook.adapters.base_adapter import BoundRequest
from aiogram_webhook.security.checks.check import SecurityCheck

IPNetwork = IPv4Network | IPv6Network
IPAddress = IPv4Address | IPv6Address


DEFAULT_TELEGRAM_NETWORKS: Final[tuple[IPNetwork, ...]] = (
    IPv4Network("149.154.160.0/20"),
    IPv4Network("91.108.4.0/22"),
)


class IPCheck(SecurityCheck):
    """
    Security check for validating client IP address against allowed networks and addresses.

    Allows requests only from specified IP networks.
    """

    def __init__(self, *ip_entries: IPNetwork | IPAddress | str, include_default: bool = True) -> None:
        """
        Initialize the IPCheck with allowed IP addresses and networks.

        :param *ip_entries: IP addresses or networks to allow.
        :param include_default: Whether to include default Telegram IP networks.
        """
        self._networks: set[IPNetwork] = set()
        self._addresses: set[IPAddress] = set()

        if include_default:
            self._networks.update(DEFAULT_TELEGRAM_NETWORKS)

        for item in ip_entries:
            parsed = self._parse(item)
            if parsed is None:
                continue
            if isinstance(parsed, IPNetwork):
                self._networks.add(parsed)
            else:
                self._addresses.add(parsed)

    async def verify(self, bot, bound_request: BoundRequest) -> bool:  # noqa: ARG002
        raw_ip = self._get_client_ip(bound_request)
        if not raw_ip:
            return False
        try:
            ip_addr = ip_address(raw_ip)
        except ValueError:
            return False
        return (ip_addr in self._addresses) or any(ip_addr in network for network in self._networks)

    def _get_client_ip(self, bound_request: BoundRequest) -> IPAddress | str | None:
        # Try to resolve client IP over reverse proxy
        # See: https://github.com/aiogram/aiogram/issues/672
        if forwarded_for := self._extract_first_ip_from_header(bound_request.headers.get("X-Forwarded-For")):
            return forwarded_for

        # Get direct IP from connection
        return bound_request.client_ip

    @staticmethod
    def _extract_first_ip_from_header(header_value: str | None) -> str | None:
        """
        Extract the first IP from a comma-separated header value (e.g., X-Forwarded-For).

        :param header_value: header value with possible IP chain
        :return: first IP or None
        """
        if header_value:
            return header_value.split(",", maxsplit=1)[0].strip()
        return None

    @staticmethod
    def _parse(item: IPAddress | IPNetwork | str) -> IPAddress | IPNetwork | None:
        if isinstance(item, (IPNetwork, IPAddress)):
            return item
        if isinstance(item, str):
            return ip_network(item, strict=False) if "/" in item else ip_address(item)
        return None
