"""Authenticity that does not live on the object it authenticates.

The previous design kept a sentinel attribute on the envelope and asked the envelope whether it
was sealed.  That question can only ever be answered by the thing under suspicion: `object.__new__`
plus `object.__setattr__` produced an instance that carried the sentinel, reported itself sealed,
and held whatever fields the caller liked.  A frozen dataclass stops ordinary assignment; it does
not stop the two calls that were actually used to forge one.

So the record moves OUT of the instance.  This module keeps a private map from object identity to
the digest of the payload that was verified at build time.  A forged instance is absent from the
map, and a mutated instance no longer hashes to the digest the map remembers.  Neither failure can
be repaired from inside the object, because the object was never asked.

The map is keyed by `id()` and cleaned by a finalizer that runs during deallocation, before the
address can be handed to another object.  Nothing here is exported: there is no token a candidate
can mint, present or copy, and the only way to obtain an attested envelope is to build one.
"""

from __future__ import annotations

import hashlib
import json
import weakref

_ATTESTATIONS: dict[int, str] = {}


def canonical_payload(payload: object) -> str:
    """One deterministic byte-string for a complete payload."""

    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def payload_digest(payload: object) -> str:
    return hashlib.sha256(canonical_payload(payload).encode("utf-8")).hexdigest()


def attest(instance: object, digest: str) -> None:
    """Record, outside the instance, the payload digest that was verified for it."""

    key = id(instance)
    _ATTESTATIONS[key] = digest
    weakref.finalize(instance, _ATTESTATIONS.pop, key, None)


def attested_digest(instance: object) -> str | None:
    """The recorded digest, or None when this object never came from the builder."""

    return _ATTESTATIONS.get(id(instance))


def attested_count() -> int:
    """Population of the private map, for suite evidence only."""

    return len(_ATTESTATIONS)
