"""The structured argument vector.

Two properties carry this module.  First, the vector is a tuple of whole tokens that a process
API receives directly: nothing here builds a command STRING, so there is no `cmd.exe`, PowerShell
or `sh` quoting layer to get wrong, and a path containing spaces, Vietnamese diacritics or a
trailing separator is simply one element.  Second, the shape of the vector is owned by this
module, not by the plan: the permission flag, its value and their positions are constants, and the
controller only ever contributes the two variable slots.  A plan therefore has no slot in which to
spell a second `--permission-mode`.

`audit_argument_vector` re-derives those properties from the finished tuple instead of trusting
the builder that produced it.  A builder that checks itself proves nothing once someone edits the
builder.
"""

from __future__ import annotations

import re

from .errors import reject

PERMISSION_FLAG = "--permission-mode"
PERMISSION_MODE = "dontAsk"
PRINT_FLAG = "-p"
SETTINGS_FLAG = "--settings"

EXECUTABLE_INDEX = 0
PERMISSION_FLAG_INDEX = 2
PERMISSION_MODE_INDEX = 3
SETTINGS_INDEX = 5
VECTOR_LENGTH = 6
VARIABLE_SLOTS = (EXECUTABLE_INDEX, SETTINGS_INDEX)
FIXED_SLOTS = {
    1: PRINT_FLAG,
    PERMISSION_FLAG_INDEX: PERMISSION_FLAG,
    PERMISSION_MODE_INDEX: PERMISSION_MODE,
    4: SETTINGS_FLAG,
}

# Spellings that change the permission decision, including the separator and case variants an
# argument parser would still honour.  Compared case-insensitively with `-`/`_` folded together.
_PERMISSION_SPELLINGS = frozenset(
    {
        "--permission-mode",
        "-permission-mode",
        "--permissionmode",
        "--permission-prompt-tool",
        "--dangerously-skip-permissions",
        "--allowed-tools",
        "--disallowed-tools",
        "--yes",
        "-y",
    }
)

# Every BARE value that a permission-mode option would accept.  Rejecting only the option token
# was half a control: a variable slot holding `auto` still lands next to `--permission-mode` if any
# consumer ever reorders or re-parses the vector, and `dontAsk` was the only value the previous
# rule caught. Folded, so case is not a way through.
PERMISSION_MODE_VALUES = frozenset(
    {
        "dontask",
        "default",
        "acceptedits",
        "bypasspermissions",
        "plan",
        "auto",
        "ask",
        "always",
        "never",
        "allow",
        "deny",
        "yes",
        "no",
    }
)

_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")


def _fold(value: str) -> str:
    return value.replace("_", "-").lower()


def build_argument_vector(executable: str, settings: str) -> tuple[str, ...]:
    """Assemble the only vector this package can produce, then audit it before returning."""

    vector = (
        executable,
        PRINT_FLAG,
        PERMISSION_FLAG,
        PERMISSION_MODE,
        SETTINGS_FLAG,
        settings,
    )
    audit_argument_vector(vector)
    return vector


def audit_argument_vector(vector: object) -> dict[str, object]:
    """Measure the finished vector: exact shape, exactly one permission decision, whole tokens."""

    if not isinstance(vector, tuple):
        raise reject("argument_vector_shape", "argument vector must be a tuple")
    if len(vector) != VECTOR_LENGTH:
        raise reject("argument_vector_shape", "argument vector has an unexpected length")
    for index, element in enumerate(vector):
        if not isinstance(element, str):
            raise reject("argument_not_string", "argument %d is not a string" % index)
        if not element:
            raise reject("argument_empty", "argument %d is empty" % index)
        if _CONTROL_CHARACTERS.search(element) is not None:
            raise reject("argument_control_character", "argument %d contains a control character" % index)

    for index, expected in FIXED_SLOTS.items():
        if vector[index] != expected:
            if index == PERMISSION_FLAG_INDEX:
                raise reject("argument_permission_missing", "the permission flag is not in its slot")
            if index == PERMISSION_MODE_INDEX:
                raise reject("argument_permission_value", "the permission value is not exact")
            raise reject("argument_vector_shape", "argument %d is not its declared constant" % index)

    # Counted across the WHOLE vector before the per-slot rules, so that a second permission
    # switch reports as a duplicate decision rather than as whatever slot it happened to occupy.
    permission_flags = [
        index for index, element in enumerate(vector) if _fold(element) in _PERMISSION_SPELLINGS
    ]
    if not permission_flags:
        raise reject("argument_permission_missing", "the vector declares no permission mode")
    if len(permission_flags) != 1 or permission_flags[0] != PERMISSION_FLAG_INDEX:
        raise reject("argument_permission_duplicate", "the vector declares more than one permission mode")
    if vector[PERMISSION_MODE_INDEX] != PERMISSION_MODE:
        # Case-folded acceptance is how `dontask` and `DONTASK` become "close enough"; they are
        # not, because the value is compared byte for byte by whatever consumes the vector.
        raise reject("argument_permission_value", "the permission value is not exactly dontAsk")

    for index in VARIABLE_SLOTS:
        element = vector[index]
        folded = _fold(element)
        if folded in PERMISSION_MODE_VALUES or folded in _PERMISSION_SPELLINGS:
            # Checked BEFORE the dash rule so that `-y` in a variable slot reports as a permission
            # injection rather than as a generic option: the specific category is the one that
            # tells a reader which control fired.
            raise reject("argument_permission_injection", "argument %d injects a permission value" % index)
        if element.startswith("-"):
            raise reject("argument_option_smuggling", "argument %d smuggles an option" % index)

    return {
        "length": len(vector),
        "permission_flag_index": PERMISSION_FLAG_INDEX,
        "permission_mode": vector[PERMISSION_MODE_INDEX],
        "permission_flag_count": len(permission_flags),
        "variable_slots": [vector[index] for index in VARIABLE_SLOTS],
        "fixed_slots": {str(index): value for index, value in sorted(FIXED_SLOTS.items())},
    }
