"""Typed, redaction-safe rejection errors for the WP122 capability gateway."""

from __future__ import annotations


class GatewayRejected(Exception):
    """A fail-closed rejection with a stable machine category.

    Messages are selected by trusted code.  Raw payload bytes, response bodies, headers,
    environment values and user-provided strings are never interpolated into diagnostics.
    """

    def __init__(self, category: str, message: str):
        self.category = category
        super().__init__(message)


def reject(category: str, message: str) -> GatewayRejected:
    return GatewayRejected(category, message)
