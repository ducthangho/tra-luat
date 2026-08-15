"""WP122 GitHub capability gateway (offline candidate implementation)."""

from .authority import AuthoritySnapshot, load_authority
from .errors import GatewayRejected
from .fake_transport import FakeGatewayGitHub
from .gateway import CapabilityGateway

__all__ = [
    "AuthoritySnapshot",
    "CapabilityGateway",
    "FakeGatewayGitHub",
    "GatewayRejected",
    "load_authority",
]
