from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network, ip_address, ip_network
from typing import TYPE_CHECKING, Final

from aiogram_webhook.security.checks.check import SecurityCheck

if TYPE_CHECKING:
    from aiogram_webhook.adapters.base import BoundRequest

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

    def _extract_ip_from_x_forwarded_for(self, bound_request: BoundRequest) -> IPv4Address | IPv6Address | str | None:
        """
        Extract client IP from X-Forwarded-For header.

        Request got through multiple proxy/load balancers
        https://github.com/aiogram/aiogram/issues/672
        """
        header_value = bound_request.header("X-Forwarded-For")
        if not header_value:
            return None
        forwarded_for, *_ = header_value.split(",", maxsplit=1)
        return forwarded_for.strip()

    def _get_client_ip(self, bound_request: BoundRequest) -> IPAddress | str | None:
        """Get client IP, first trying X-Forwarded-For header, then direct connection."""
        # Try to resolve client IP over reverse proxy
        if forwarded_for := self._extract_ip_from_x_forwarded_for(bound_request):
            return forwarded_for

        # Get direct IP from connection
        return bound_request.ip()

    async def verify(self, bot, bound_request) -> bool:  # noqa: ARG002
        raw_ip = self._get_client_ip(bound_request)
        if not raw_ip:
            return False
        try:
            ip_addr = ip_address(raw_ip)
        except ValueError:
            return False
        return (ip_addr in self._addresses) or any(ip_addr in network for network in self._networks)

    @staticmethod
    def _parse(item: IPAddress | IPNetwork | str) -> IPAddress | IPNetwork | None:
        if isinstance(item, (IPNetwork, IPAddress)):
            return item
        if isinstance(item, str):
            return ip_network(item, strict=False) if "/" in item else ip_address(item)
        return None
