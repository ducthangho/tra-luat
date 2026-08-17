"""The child environment: a closed allowlist, built from nothing.

The environment handed to the Reviewer child is CONSTRUCTED, never inherited and never filtered.
The difference matters: a filter starts from the ambient environment and has to enumerate every
name worth removing, so a credential nobody thought of survives; construction starts from an empty
mapping, so a name nobody thought of is absent by default rather than by vigilance.

`CLAUDE_CODE_DISABLE_AUTO_MEMORY` is injected by this module and cannot be spelled by the plan at
all — not in any case, not by folding, not by declaring it twice.  A flag the caller may re-state
is a flag the caller may re-state as `0`.

Declared non-coverage: "untrusted config-loading path" is enforced here as *inside the candidate
tree, relative, empty or current-directory* `PATH` entries.  Whether some absolute directory
outside the candidate is writable by another local principal is not measured; that is an ACL
question this offline module cannot answer honestly, and pretending otherwise would be the kind of
claim RA-01 already learned to write down instead of imply.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from types import MappingProxyType
from typing import Mapping

from oracle.safe_io import require_outside_tree

from .errors import EnvelopeRejected, reject
from .paths import CANDIDATE_ROOT, admit_directory_entry, check_path_text

MEMORY_FLAG_NAME = "CLAUDE_CODE_DISABLE_AUTO_MEMORY"
MEMORY_FLAG_VALUE = "1"

MAX_ENVIRONMENT_NAMES = 32
MAX_VALUE_CHARACTERS = 4096
MAX_PATH_ENTRIES = 64

_NAME_SHAPE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}\Z")
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")

# The closed set.  A name outside it is rejected, not dropped: a plan that asks for something this
# module will not deliver is a plan built against different assumptions, and silently honouring the
# rest of it is how the two sides stay disagreeing.
ALLOWED_ENVIRONMENT_NAMES = frozenset(
    {
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "WINDIR",
        "LANG",
        "LC_ALL",
        "TZ",
        "NUMBER_OF_PROCESSORS",
        "PROCESSOR_ARCHITECTURE",
    }
)

# Removed from the allowlist rather than validated harder, because "absolute and outside the
# candidate" was never the property that mattered for them:
#
#   HOME, USERPROFILE, APPDATA, LOCALAPPDATA, PROGRAMDATA, PROGRAMFILES
#       roots from which tools load configuration, credentials and plugins before reaching their
#       own entry point.  A trustworthy path here is not enough; the CONTENTS decide behaviour.
#   COMSPEC
#       hands the child a shell interpreter, which is the one capability this Packet exists to
#       keep out of the launch description.
#   TEMP, TMP, TMPDIR
#       a writable scratch root is a side effect, and RA-04A is side-effect-free.
#   TERM
#       no console is attached to a headless run (ADR-0021), so it decides nothing.
OMITTED_CONFIG_LOADING_NAMES = frozenset(
    {
        "HOME",
        "USERPROFILE",
        "APPDATA",
        "LOCALAPPDATA",
        "PROGRAMDATA",
        "PROGRAMFILES",
        "COMSPEC",
        "TEMP",
        "TMP",
        "TMPDIR",
        "TERM",
    }
)

# Declared as a list of absolute entries, never as a pre-joined string: a pre-joined string is a
# place to hide a relative entry behind a separator.
PATH_LIST_NAMES = frozenset({"PATH"})

# Single directory values.  Admitted with the same directory rules as a PATH entry: they must
# exist, be a real directory rather than a link to one, and sit inside a controller trusted root.
PATH_VALUE_NAMES = frozenset({"SYSTEMROOT", "WINDIR"})

# Names that load code or configuration into the child before it reaches its own entry point.
INJECTION_NAMES = frozenset(
    {
        "PYTHONPATH",
        "PYTHONSTARTUP",
        "PYTHONHOME",
        "PYTHONEXECUTABLE",
        "BASH_ENV",
        "ENV",
        "CDPATH",
        "IFS",
        "SHELLOPTS",
        "BASHOPTS",
        "PROMPT_COMMAND",
        "NODE_OPTIONS",
        "NODE_PATH",
        "NPM_CONFIG_PREFIX",
        "LD_PRELOAD",
        "LD_LIBRARY_PATH",
        "LD_AUDIT",
        "DYLD_INSERT_LIBRARIES",
        "PERL5LIB",
        "RUBYOPT",
        "PSMODULEPATH",
    }
)
INJECTION_PREFIXES = ("GIT_CONFIG", "GIT_SSH", "GIT_EXEC", "LD_", "DYLD_", "PYTHON", "NODE_")

# Credential shapes.  Matched on the folded name, so `gh_token` and `Gh_Token` are the same claim.
CREDENTIAL_PREFIXES = ("GH_", "GITHUB_", "AWS_", "ANTHROPIC_", "OPENAI_", "AZURE_", "GOOGLE_")
CREDENTIAL_TOKENS = ("TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL", "APIKEY", "API_KEY", "PRIVATE_KEY")


def _folded(name: str) -> str:
    return name.upper()


def _reject_value_text(name: str, value: object) -> str:
    if not isinstance(value, str):
        raise reject("environment_value_type", "%s must be a string value" % name)
    if not value:
        raise reject("environment_value_empty", "%s must not be empty" % name)
    if len(value) > MAX_VALUE_CHARACTERS:
        raise reject("environment_value_oversized", "%s exceeds the value length limit" % name)
    if _CONTROL_CHARACTERS.search(value) is not None:
        raise reject("environment_value_control_character", "%s contains a control character" % name)
    return value


def _admit_path_entry(entry: object, name: str, trusted_roots: tuple) -> str:
    if not isinstance(entry, str):
        raise reject("path_entry_type", "%s contains a non-string entry" % name)
    if not entry:
        raise reject("path_entry_empty", "%s contains an empty entry" % name)
    if entry == ".":
        raise reject("path_entry_current_directory", "%s contains a current-directory entry" % name)
    if os.pathsep in entry:
        raise reject("path_entry_separator", "%s hides a separator inside one entry" % name)
    try:
        check_path_text(entry, "%s entry" % name)
    except EnvelopeRejected as exc:
        if exc.category == "path_not_absolute":
            raise reject("path_entry_relative", "%s contains a relative entry" % name) from exc
        raise
    admitted = admit_directory_entry(entry, name, trusted_roots=trusted_roots)
    require_outside_tree(
        admitted,
        CANDIDATE_ROOT,
        "%s entry" % name,
        lambda _message: reject(
            "path_entry_inside_candidate", "%s points inside the candidate checkout" % name
        ),
    )
    return str(admitted)


def _admit_path_list(name: str, value: object, trusted_roots: tuple) -> str:
    if isinstance(value, str):
        raise reject("environment_path_not_list", "%s must be declared as a list of entries" % name)
    if not isinstance(value, list) or not value:
        raise reject("environment_path_not_list", "%s must be a non-empty list of entries" % name)
    if len(value) > MAX_PATH_ENTRIES:
        raise reject("environment_path_oversized", "%s declares too many entries" % name)
    entries: list[str] = []
    for entry in value:
        admitted = _admit_path_entry(entry, name, trusted_roots)
        if admitted not in entries:
            entries.append(admitted)
    return os.pathsep.join(entries)


def _reject_hostile_name(name: str) -> str:
    if not isinstance(name, str) or _NAME_SHAPE.fullmatch(name) is None:
        raise reject("environment_name_shape", "environment names must be plain identifiers")
    folded = _folded(name)
    if folded == MEMORY_FLAG_NAME:
        raise reject("environment_memory_override", "the automatic-memory flag cannot be declared")
    if folded in INJECTION_NAMES or folded.startswith(INJECTION_PREFIXES):
        raise reject("environment_injection_name", "the name loads code or configuration")
    if folded.startswith(CREDENTIAL_PREFIXES) or any(token in folded for token in CREDENTIAL_TOKENS):
        raise reject("environment_credential_name", "the name has a credential shape")
    if name != folded:
        raise reject("environment_name_shape", "environment names must be canonical upper case")
    if folded not in ALLOWED_ENVIRONMENT_NAMES:
        raise reject("environment_name_not_allowed", "the name is outside the closed allowlist")
    return folded


def build_child_environment(declared: object, trusted_roots: tuple = ()) -> Mapping[str, str]:
    """Build the closed child environment from the plan's declared names only.

    `trusted_roots` arrives from the sealed plan, never from a caller argument: it is the set of
    directories the controller vouched for, and every directory-shaped value must sit inside one.
    """

    if not isinstance(declared, dict):
        raise reject("environment_shape", "the declared environment must be an object")
    if len(declared) > MAX_ENVIRONMENT_NAMES:
        raise reject("environment_oversized", "the declared environment has too many names")

    seen: dict[str, str] = {}
    for name in declared:
        if not isinstance(name, str) or _NAME_SHAPE.fullmatch(name) is None:
            raise reject("environment_name_shape", "environment names must be plain identifiers")
        folded = _folded(name)
        if folded in seen:
            # Two spellings of one name is one name on Windows and two on POSIX.  Either way the
            # child's view depends on which spelling wins, so neither spelling is admitted.
            raise reject("environment_case_collision", "two declared names fold to one name")
        seen[folded] = name

    child: dict[str, str] = {}
    for name, value in declared.items():
        folded = _reject_hostile_name(name)
        if folded in PATH_LIST_NAMES:
            child[folded] = _admit_path_list(folded, value, trusted_roots)
            continue
        text = _reject_value_text(folded, value)
        if folded in PATH_VALUE_NAMES:
            check_path_text(text, folded)
            child[folded] = str(admit_directory_entry(text, folded, trusted_roots=trusted_roots))
            continue
        child[folded] = text

    child[MEMORY_FLAG_NAME] = MEMORY_FLAG_VALUE
    return MappingProxyType(dict(sorted(child.items())))


def environment_evidence(child: Mapping[str, str]) -> dict[str, object]:
    """Names and stable digests only.

    A value is never reported.  Credential-shaped names are already rejected, but "we rejected the
    names we thought of" is not a reason to print the values of the ones we did not.
    """

    shapes = {
        name: {"length": len(value), "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest()}
        for name, value in child.items()
    }
    canonical = json.dumps(shapes, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "names": sorted(child),
        "count": len(child),
        "memory_flag_present": child.get(MEMORY_FLAG_NAME) == MEMORY_FLAG_VALUE,
        "memory_flag_occurrences": sum(1 for name in child if name == MEMORY_FLAG_NAME),
        "path_entry_count": len(child["PATH"].split(os.pathsep)) if "PATH" in child else 0,
        "value_shapes": shapes,
        "digest": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }
