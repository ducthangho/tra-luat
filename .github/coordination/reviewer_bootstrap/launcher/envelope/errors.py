"""Typed, redaction-safe rejection errors for the RA-04A launch envelope.

Every fail-closed branch in this package raises one of these with a stable machine category.
Messages are selected by trusted code: sealed bytes, environment values, plan fields and
candidate-controlled strings are never interpolated into a diagnostic, because a rejection that
echoes its input is a credential channel wearing an error message.
"""

from __future__ import annotations


class EnvelopeRejected(Exception):
    """A fail-closed rejection carrying a stable machine category."""

    def __init__(self, category: str, message: str):
        self.category = category
        super().__init__(message)


def reject(category: str, message: str) -> EnvelopeRejected:
    return EnvelopeRejected(category, message)
