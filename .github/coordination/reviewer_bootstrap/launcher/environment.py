"""Allowlisted child environment for the headless Reviewer (Issue 125 §4.2).

The child environment is *constructed*, not *inherited and filtered*.  The difference decides the
default: a denylist over the parent environment is green until someone invents a variable name
nobody thought of, while an allowlist is red until someone names the variable and says why.  Only
the second one fails closed, and only the second one produces a short, auditable list to retain as
evidence.

Exactly one variable is set by policy: ``CLAUDE_CODE_DISABLE_AUTO_MEMORY=1``.  The selftest observes
that value *inside a real launched child* rather than in the dictionary this module returns — a
mapping the parent built proves what the parent intended, not what the child received.

What this module does not cover is stated rather than implied, following the RA-01 precedent that a
tripwire declaring its limits stays usable while one claiming everything does not.  See
:data:`COVERAGE`.
"""

from __future__ import annotations

import os
import pathlib
import re
from collections.abc import Mapping

from core.guards import is_sensitive

from .errors import reject

MEMORY_VARIABLE = "CLAUDE_CODE_DISABLE_AUTO_MEMORY"
MEMORY_VALUE = "1"

# Named allowlist.  Every entry is here because a process cannot start correctly without it, and the
# comment beside each group is the justification an auditor gets to disagree with.
ALLOWED_NAMES: tuple[str, ...] = (
    # Windows needs these to load system DLLs and resolve the console host at all.
    "SystemRoot",
    "SystemDrive",
    "windir",
    "ComSpec",
    "PATHEXT",
    "NUMBER_OF_PROCESSORS",
    "PROCESSOR_ARCHITECTURE",
    # Executable resolution.  Sanitized before use: see `_sanitize_path`.
    "PATH",
    # Scratch space.  The controller passes explicit run directories, but the interpreter and the
    # C runtime both fall back to these when a library asks for a temporary file.
    "TEMP",
    "TMP",
    "TMPDIR",
    # Home.  Required by the official CLI to find its own configuration; see COVERAGE.not_covered
    # for the boundary this does not draw.
    "HOME",
    "USERPROFILE",
    # Deterministic text handling.  A Vietnamese repository on a cp1258 console decodes wrongly in
    # both directions when these are unset, and wrong evidence is worse than missing evidence.
    "LANG",
    "LC_ALL",
    "PYTHONIOENCODING",
    "PYTHONUTF8",
    # Reproducibility of the child interpreter used by the offline controls.
    "PYTHONHASHSEED",
    "PYTHONDONTWRITEBYTECODE",
)

_ALLOWED = frozenset(ALLOWED_NAMES)

# Credential-shaped *name* families the contract calls out by hand.  This is belt-and-braces behind
# the allowlist: it catches an allowlist entry that someone adds later without thinking.
_DENY_PREFIXES = (
    "GH_",
    "GITHUB_",
    "GIT_ASKPASS",
    "GIT_SSH",
    "SSH_",
    "AWS_",
    "AZURE_",
    "GOOGLE_",
    "GCP_",
    "GCLOUD_",
    "ANTHROPIC_",
    "OPENAI_",
    "CLAUDE_CODE_OAUTH",
    "NPM_",
    "NODE_AUTH",
    "PYPI_",
    "TWINE_",
    "DOCKER_",
    "CARGO_REGISTRY",
    "GPG_",
    "SIGSTORE_",
    "COSIGN_",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "PROXY_",
)

# Word-level shapes.  A name is credential-shaped when a secret noun appears as a whole word; the
# word split keeps `TOKEN_BUDGET` and `SESSION_ID` out of the net, which is the failure RA-01 paid
# for twice before settling on word roles instead of substrings.
_SECRET_WORDS = frozenset(
    {
        "TOKEN",
        "SECRET",
        "PASSWORD",
        "PASSWD",
        "PASS",
        "CREDENTIAL",
        "CREDENTIALS",
        "APIKEY",
        "KEY",
        "COOKIE",
        "SESSIONKEY",
        "AUTH",
        "AUTHORIZATION",
        "BEARER",
        "PAT",
        "PRIVATEKEY",
        "SIGNINGKEY",
    }
)
# Words that turn a secret noun into a measurement or a policy knob rather than a value.
_MEASURE_WORDS = frozenset({"BUDGET", "COUNT", "LIMIT", "MAX", "MIN", "TIMEOUT", "POLICY", "TTL"})

_WORD_SPLIT = re.compile(r"[^A-Za-z0-9]+")

# WP125-RV-001.  The closed set of names ``extra`` may set.  Generation 1 accepted *any* name that
# was not credential-shaped and wrote it straight into the child, which made ``extra`` a general
# environment-injection channel: ``{"PATH": ...}`` silently replaced the sanitized PATH computed six
# lines earlier, and ``PYTHONPATH``/``BASH_ENV``/``NODE_OPTIONS`` are code-execution switches wearing
# ordinary-variable clothes. None of them is credential-shaped, so the only check in the way said
# yes. The fix is the same shape as the parent allowlist: name the three run coordinates the
# controller actually needs, and refuse everything else — including anything already allowlisted, so
# ``extra`` can never override a value the allowlist just computed.
CONTROLLER_EXTRA_NAMES: tuple[str, ...] = (
    "WP125_RUN_ID",
    "WP125_CASE_ID",
    "WP125_PROBE_LABEL",
)

_CONTROLLER_EXTRA = frozenset(CONTROLLER_EXTRA_NAMES)

# Names that change *what code runs* rather than what the code sees. They are already outside the
# closed set above, so this table changes no outcome — it changes the diagnosis. A reviewer reading
# the matrix should see that the injection question was asked by name and answered, instead of
# inferring it from a generic "not in the closed set" rejection.
EXECUTION_INFLUENCING_NAMES = frozenset(
    {
        "PATH",
        "PATHEXT",
        "PYTHONPATH",
        "PYTHONHOME",
        "PYTHONSTARTUP",
        "PYTHONEXECUTABLE",
        "PYTHONWARNINGS",
        "PYTHONINSPECT",
        "BASH_ENV",
        "ENV",
        "SHELLOPTS",
        "BASHOPTS",
        "PROMPT_COMMAND",
        "NODE_OPTIONS",
        "NODE_PATH",
        "LD_PRELOAD",
        "LD_LIBRARY_PATH",
        "LD_AUDIT",
        "DYLD_INSERT_LIBRARIES",
        "COMSPEC",
        "SYSTEMROOT",
        "WINDIR",
        "APPDATA",
        "USERPROFILE",
        "HOME",
    }
)

# Values for the closed extra names are identifiers, not paths. Refusing separators here means a run
# identifier can never smuggle a search path into a variable whose *name* passed the closed-set test.
_EXTRA_VALUE_ALLOWED = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_MAX_EXTRA_VALUE_BYTES = 128

COVERAGE = {
    "covered": (
        "child environment is built from a named allowlist",
        "exactly one policy variable is set and its value is observed inside a real child",
        "credential-shaped names are refused even if an allowlist entry introduces one",
        "PATH entries inside the candidate checkout are dropped before the child sees PATH",
        "no raw parent environment mapping reaches diagnostics or retained artifacts",
        "the controller extra set is closed; overrides, case-folded collisions and "
        "execution-influencing names are refused by name (WP125-RV-001)",
        "extra values must be identifier-shaped, so a run coordinate cannot smuggle a search path",
    ),
    "not_covered": (
        "credentials resident in files under HOME/USERPROFILE, which this boundary does not read "
        "and cannot remove",
        "a credential embedded in an allowlisted path value rather than in a variable name",
        "descendants that re-read the parent environment through an OS handle rather than through "
        "inheritance",
    ),
}


def credential_shaped(name: str) -> bool:
    """True when the *name* alone is enough to refuse the variable."""
    if is_sensitive(name):
        return True
    upper = str(name).upper()
    if any(upper.startswith(prefix) for prefix in _DENY_PREFIXES):
        return True
    words = {word for word in _WORD_SPLIT.split(upper) if word}
    if words & _MEASURE_WORDS:
        return False
    return bool(words & _SECRET_WORDS)


def _sanitize_path(value: str, candidate_root: pathlib.Path) -> str:
    """Drop PATH entries that resolve inside the candidate checkout.

    §4.1 forbids discovering an executable from the candidate tree.  Passing an unsanitized PATH
    would reinstate exactly that discovery one indirection later, through whatever the child spawns.
    """
    kept: list[str] = []
    root = candidate_root.resolve()
    for entry in value.split(os.pathsep):
        if not entry:
            continue
        try:
            resolved = pathlib.Path(entry).resolve()
        except (OSError, ValueError):
            continue
        if resolved == root or root in resolved.parents:
            continue
        kept.append(entry)
    return os.pathsep.join(kept)


def build_child_environment(
    parent: Mapping[str, str],
    *,
    candidate_root: str,
    extra: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Return the complete environment for the child, or reject by category.

    ``extra`` exists for controller-owned run coordinates (a run identifier, a marker probe name).
    It is validated with the same rules as the allowlist, so it cannot become a side door.
    """
    if not isinstance(parent, Mapping):
        raise reject("child_environment", "the parent environment must be a mapping")
    root = pathlib.Path(candidate_root)

    child: dict[str, str] = {}
    for name in ALLOWED_NAMES:
        if name not in parent:
            continue
        value = parent[name]
        if not isinstance(value, str):
            continue
        if credential_shaped(name):
            raise reject(
                "child_environment", "allowlisted name %r is credential-shaped" % (name,)
            )
        if name == "PATH":
            value = _sanitize_path(value, root)
        child[name] = value

    _apply_controller_extra(child, extra)

    child[MEMORY_VARIABLE] = MEMORY_VALUE
    _assert_boundary(child)
    return child


def _apply_controller_extra(child: dict[str, str], extra: Mapping[str, str] | None) -> None:
    """Merge the closed controller extra set, or reject by category (WP125-RV-001).

    Every refusal below is a distinct measurement rather than a fallthrough, because the point of
    this function is that an auditor can see which attack was asked about.
    """
    if extra is None:
        return
    if not isinstance(extra, Mapping):
        raise reject("child_environment", "the extra environment must be a mapping")

    # Case-folded index of everything already decided. Windows environment lookup is
    # case-insensitive, so `path` and `PATH` are one variable there and two keys in a plain dict —
    # comparing exact names only would let the second spelling through and let the child resolve
    # whichever the OS happens to prefer.
    decided = {name.casefold(): name for name in child}
    decided[MEMORY_VARIABLE.casefold()] = MEMORY_VARIABLE
    seen: dict[str, str] = {}

    for name, value in dict(extra).items():
        if not isinstance(name, str) or not name:
            raise reject("child_environment", "an extra variable name is not a non-empty string")
        folded = name.casefold()

        if folded in seen:
            raise reject(
                "child_environment",
                "extra variable %r collides case-folded with %r" % (name, seen[folded]),
            )
        if name.upper() in EXECUTION_INFLUENCING_NAMES:
            raise reject(
                "child_environment",
                "extra variable %r selects what code runs and is never grantable" % (name,),
            )
        if folded in decided:
            raise reject(
                "child_environment",
                "extra variable %r would override allowlisted %r" % (name, decided[folded]),
            )
        if credential_shaped(name):
            raise reject("child_environment", "extra variable %r is credential-shaped" % (name,))
        if name not in _CONTROLLER_EXTRA:
            raise reject(
                "child_environment",
                "extra variable %r is outside the closed controller extra set" % (name,),
            )
        if not isinstance(value, str):
            raise reject("child_environment", "extra variable %r has a non-string value" % (name,))
        if len(value.encode("utf-8")) > _MAX_EXTRA_VALUE_BYTES:
            raise reject("child_environment", "extra variable %r exceeds the value ceiling" % (name,))
        if not _EXTRA_VALUE_ALLOWED.fullmatch(value):
            raise reject(
                "child_environment",
                "extra variable %r carries a separator, control character or path-shaped value"
                % (name,),
            )
        seen[folded] = name
        child[name] = value


def _assert_boundary(child: Mapping[str, str]) -> None:
    """Post-condition on the constructed mapping, checked with branches, never ``assert``."""
    if child.get(MEMORY_VARIABLE) != MEMORY_VALUE:
        raise reject("child_environment", "the automatic-memory variable is not exactly 1")
    offenders = sorted(name for name in child if credential_shaped(name))
    if offenders:
        raise reject(
            "child_environment", "%d credential-shaped names survived construction" % len(offenders)
        )


def describe(child: Mapping[str, str]) -> dict[str, object]:
    """Evidence for the retained artifact set: **names only**, plus the one policy value.

    §4.2 forbids a raw parent environment dump in diagnostics or retained artifacts.  Recording
    values would defeat the boundary the rest of this module builds, so the artifact carries the
    sorted name list and nothing else — except the automatic-memory value, which is policy the
    contract requires to be provable.
    """
    return {
        "names": sorted(child),
        "name_count": len(child),
        MEMORY_VARIABLE: child.get(MEMORY_VARIABLE),
        "values_recorded": False,
        "coverage": {key: list(value) for key, value in COVERAGE.items()},
    }
