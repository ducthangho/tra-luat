"""Source inventory of the envelope prefix, reduced to one deterministic digest.

The prefix string is not written out again here: it is DERIVED from
`oracle/trusted_inventory.py::REVIEWER_BOOTSTRAP_ROOT`, which RA-02 already established as the one
declaration of that root.  A second hand-copied ".github/coordination/..." literal is a constant
with two owners, and the owner who forgets to update is the one that decides what the digest
covers.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import stat

from oracle.trusted_inventory import REVIEWER_BOOTSTRAP_ROOT

from .errors import reject
from .paths import CANDIDATE_ROOT

LAUNCHER_PREFIX = REVIEWER_BOOTSTRAP_ROOT + "/launcher/"
ENVELOPE_PREFIX = LAUNCHER_PREFIX + "envelope/"

HERE = pathlib.Path(__file__).resolve().parent

# Issue 149 §7 says "every regular file below the exact envelope prefix", so there is no exclusion
# list here at all.  The previous version quietly skipped `__pycache__`, which meant the digest
# described a tree that did not exist on disk — and the one directory it skipped is the one an
# attacker can write into without touching a tracked file.  The conflict is resolved at the source
# instead: `selftest.py` sets `sys.dont_write_bytecode` before importing the package, so the owned
# tree never acquires a cache, and `WP149-R1-017` fails loudly if one appears anyway.
EXCLUDED_NAMES: tuple[str, ...] = ()

_FILE_ATTRIBUTE_REPARSE_POINT = 0x400


def _walk(root: pathlib.Path) -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for entry in sorted(root.iterdir(), key=lambda item: item.name):
        info = entry.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
            # A link inside the inventory would let one blob be counted under a second name, or a
            # file outside the prefix be counted as if it were inside it.
            raise reject("inventory_link", "the inventory prefix contains a link")
        if stat.S_ISDIR(info.st_mode):
            found.extend(_walk(entry))
            continue
        if not stat.S_ISREG(info.st_mode):
            raise reject("inventory_irregular", "the inventory prefix contains an irregular file")
        found.append(entry)
    return found


def inventory_of(root: pathlib.Path) -> dict[str, object]:
    """Every regular file below `root`: relative path, byte size, SHA-256, and one digest."""

    base = pathlib.Path(root).resolve()
    if not base.is_dir():
        raise reject("inventory_root", "the inventory root is not a directory")
    files = []
    for path in _walk(base):
        raw = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(base).as_posix(),
                "size": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    files.sort(key=lambda item: item["path"])
    canonical = json.dumps(files, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "file_count": len(files),
        "files": files,
        "excluded": list(EXCLUDED_NAMES),
        "digest": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def envelope_inventory() -> dict[str, object]:
    """The inventory of this package, bound to the exact authorised write-set prefix."""

    relative = HERE.relative_to(CANDIDATE_ROOT).as_posix() + "/"
    if relative != ENVELOPE_PREFIX:
        raise reject("inventory_prefix", "this package does not sit on the authorised prefix")
    measured = inventory_of(HERE)
    outside = [
        item["path"]
        for item in measured["files"]
        if item["path"].startswith("/") or ".." in item["path"].split("/")
    ]
    if outside:
        raise reject("inventory_outside_write_set", "an inventoried path leaves the write set")
    measured["prefix"] = ENVELOPE_PREFIX
    return measured
