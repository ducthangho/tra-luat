"""RA-04A launch envelope: sealed inputs in, one immutable launch description out.

`launcher` itself is an implicit namespace package.  It holds no `__init__.py` because this
Packet's write set is the `launcher/envelope/` prefix exactly, and a file one directory higher
would be a change outside the authorised set — a small convenience is not worth an out-of-scope
path in the diff.
"""

from .arguments import PERMISSION_FLAG, PERMISSION_MODE, audit_argument_vector
from .environment import ALLOWED_ENVIRONMENT_NAMES, MEMORY_FLAG_NAME, MEMORY_FLAG_VALUE
from .envelope import LaunchEnvelope, build_launch_envelope
from .errors import EnvelopeRejected
from .inventory import ENVELOPE_PREFIX, envelope_inventory
from .paths import CANDIDATE_ROOT

__all__ = [
    "ALLOWED_ENVIRONMENT_NAMES",
    "CANDIDATE_ROOT",
    "ENVELOPE_PREFIX",
    "EnvelopeRejected",
    "LaunchEnvelope",
    "MEMORY_FLAG_NAME",
    "MEMORY_FLAG_VALUE",
    "PERMISSION_FLAG",
    "PERMISSION_MODE",
    "audit_argument_vector",
    "build_launch_envelope",
    "envelope_inventory",
]
