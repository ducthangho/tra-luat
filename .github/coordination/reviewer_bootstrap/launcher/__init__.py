"""WP125 Windows launcher and controller-owned watchdog (offline candidate implementation)."""

from .errors import CATEGORIES, LauncherRejected, reject

__all__ = [
    "CATEGORIES",
    "LauncherRejected",
    "reject",
]
