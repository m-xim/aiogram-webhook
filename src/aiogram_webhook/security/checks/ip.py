from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network, ip_address, ip_network
from typing import TYPE_CHECKING, Final

from aiogram_webhook.security.checks.check import Check

if TYPE_CHECKING:
    from aiogram_webhook.adapters.base import BoundRequest

DEFAULT_TELEGRAM_NETWORKS: Final[tuple[IPv4Network | IPv6Network, ...]] = (
    IPv4Network("149.154.160.0/20"),
    IPv4Network("91.108.4.0/22"),
)

IPAddressOrNetwork = IPv4Network | IPv6Network | IPv4Address | IPv6Address


class IPCheck(Check):
    """
    Security check for validating client IP address against allowed networks and addresses.

    Allows requests only from specified IP networks.
    """

    def __init__(self, *ip_entries: IPAddressOrNetwork | str, include_default: bool = True) -> None:
        """
        Initialize the IPCheck with allowed IP addresses and networks.

        Args:
            *ip_entries: IP addresses or networks to allow.
            include_default: Whether to include default Telegram IP networks.
        """
        networks: set[IPv4Network | IPv6Network] = set()
        addresses: set[IPv4Address | IPv6Address] = set()

        if include_default:
            networks.update(DEFAULT_TELEGRAM_NETWORKS)

        for item in ip_entries:
            parsed = self._parse(item)
            if parsed is None:
                continue
            if isinstance(parsed, (IPv4Network, IPv6Network)):
                networks.add(parsed)
            else:
                addresses.add(parsed)

        self._networks: set[IPv4Network | IPv6Network] = networks
        self._addresses: set[IPv4Address | IPv6Address] = addresses

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

    def _get_client_ip(self, bound_request: BoundRequest) -> IPv4Address | IPv6Address | str | None:
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
            addr = ip_address(raw_ip)
        except ValueError:
            return False

        if addr in self._addresses:
            return True

        return any(addr in net for net in self._networks)

    @staticmethod
    def _parse(item: IPAddressOrNetwork | str) -> IPAddressOrNetwork | None:
        if isinstance(item, (IPv4Network, IPv6Network, IPv4Address, IPv6Address)):
            return item
        if isinstance(item, str):
            return ip_network(item, strict=False) if "/" in item else ip_address(item)
        return None
