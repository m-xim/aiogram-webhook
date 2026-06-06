from functools import lru_cache
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network, ip_address, ip_network
from typing import Final

from aiogram_webhook.engines.target import Target
from aiogram_webhook.route.params import RouteParams
from aiogram_webhook.security.checks.check import SecurityCheck
from aiogram_webhook.web.base import WebRequest

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
        self._networks: frozenset[IPNetwork] = frozenset()
        self._addresses: frozenset[IPAddress] = frozenset()

        networks = set(DEFAULT_TELEGRAM_NETWORKS) if include_default else set()
        addresses = set()

        for item in ip_entries:
            parsed = self._parse(item)
            if parsed is None:
                continue
            if isinstance(parsed, (IPv4Network, IPv6Network)):
                networks.add(parsed)
            elif isinstance(parsed, (IPv4Address, IPv6Address)):
                addresses.add(parsed)

        self._networks = frozenset(networks)
        self._addresses = frozenset(addresses)

    async def verify(self, target: Target, request: WebRequest, route_params: RouteParams) -> bool:  # noqa: ARG002
        forwarded_for = request.headers.get("X-Forwarded-For")
        raw_ip = forwarded_for.split(",", maxsplit=1)[0].strip() if forwarded_for else request.client_ip

        if not raw_ip:
            return False

        try:
            ip_addr = self._parse_ip(raw_ip)
        except ValueError:
            return False

        # Direct address match (faster check first)
        if ip_addr in self._addresses:
            return True

        # Network match (short-circuit on first match)
        return any(ip_addr in network for network in self._networks)

    @staticmethod
    @lru_cache(maxsize=256)
    def _parse_ip(ip_str: str) -> IPv4Address | IPv6Address:
        """Parse and cache IP address parsing results."""
        return ip_address(ip_str)

    @staticmethod
    def _parse(item: IPAddress | IPNetwork | str) -> IPAddress | IPNetwork | None:
        if isinstance(item, (IPv4Network, IPv6Network, IPv4Address, IPv6Address)):
            return item
        if isinstance(item, str):
            return ip_network(item, strict=False) if "/" in item else ip_address(item)
        return None
