"""Structured argument vector for exactly one headless Claude Reviewer invocation (Issue 125 §4.1).

The vector is *built*, never *concatenated*.  There is no shell string anywhere on this path: no
``shell=True``, no ``Invoke-Expression``, no ``cmd /c`` forwarding, no dynamic PowerShell.  A shell
string is a parser, and handing a parser any untrusted byte hands the attacker the argument
boundary itself — the exact failure this Packet must not reproduce on Windows, where quoting rules
differ between ``CreateProcess``, ``cmd.exe`` and PowerShell.

Two rules carry the section:

* The executable and launch configuration are *controller* inputs pinned outside the candidate
  checkout.  Nothing here discovers an executable from the candidate tree, from ``PATH`` relative to
  the candidate, or from any text the Reviewer might influence.
* Untrusted text never becomes an argument.  The Reviewer's instructions travel as a file whose path
  the controller chose and whose bytes the controller hashed; the vector carries the *path*, and the
  path is one the controller minted.  So an injected ``--permission-mode auto`` inside a prompt is
  prompt bytes, not a switch.

``--permission-mode dontAsk`` is mandatory and exact.  ``auto`` in any spelling, a duplicate or
conflicting permission switch, and omission are each a *named* failure rather than a fallback:
falling back to an interactive prompt in a headless run is how a launch hangs forever, and falling
back to ``auto`` is how a Reviewer silently gains write authority it was never granted.
"""

from __future__ import annotations

import dataclasses
import pathlib
import re
from collections.abc import Mapping, Sequence

from .errors import reject

PERMISSION_SWITCH = "--permission-mode"
REQUIRED_PERMISSION_MODE = "dontAsk"

# `auto` is called out by the contract; the rest are the spellings that reach the same place.  The
# comparison is case-folded because Windows argument parsing is not case sensitive in practice and a
# control that only catches the lowercase spelling is a control an attacker walks around.
FORBIDDEN_PERMISSION_MODES = frozenset(
    {
        "auto",
        "acceptedits",
        "acceptall",
        "bypasspermissions",
        "default",
        "plan",
        "interactive",
        "ask",
    }
)

# Switches the Reviewer child must never receive from this launcher.  Each would move authority out
# of the controller: a second settings source, a hook, a different working directory, a different
# permission decision, or an MCP/tool surface the Packet did not grant.
FORBIDDEN_SWITCHES = frozenset(
    {
        "--settings",
        "--setting",
        "--add-dir",
        "--allowedtools",
        "--allowed-tools",
        "--disallowedtools",
        "--disallowed-tools",
        "--mcp-config",
        "--strict-mcp-config",
        "--append-system-prompt",
        "--system-prompt",
        "--dangerously-skip-permissions",
        "--permission-prompt-tool",
        "--resume",
        "--continue",
    }
)

# A switch-shaped token is anything a CLI parser would read as an option.  Untrusted values that
# look like this are refused outright rather than escaped: escaping is a promise about someone
# else's parser, and this module refuses to make promises it cannot verify.
_SWITCH_SHAPED = re.compile(r"\A[-/]")
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


@dataclasses.dataclass(frozen=True)
class LaunchPlan:
    """An immutable, fully-resolved plan for one child process.

    Frozen because the plan is evidence: the argument vector recorded in the run artifacts must be
    the vector that was actually spawned.  A mutable plan lets a later stage edit history.
    """

    executable: str
    argv: tuple[str, ...]
    working_directory: str
    prompt_path: str

    def command(self) -> tuple[str, ...]:
        """The complete spawn vector, executable first."""
        return (self.executable,) + self.argv


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise reject("argument_vector", "%s must be a non-empty string" % label)
    if _CONTROL_CHARS.search(value):
        raise reject("argument_vector", "%s carries control characters" % label)
    return value


def _require_absolute_outside(path_text: str, candidate_root: pathlib.Path, label: str) -> str:
    """Absolute, outside the candidate tree, and not switch-shaped.

    "Outside the candidate tree" is the whole point of §4.1: an executable or configuration the
    candidate branch can write is an executable the *reviewed code* chooses, which would let a
    Packet under review pick the binary that reviews it.
    """
    path = pathlib.Path(path_text)
    if not path.is_absolute():
        raise reject("argument_vector", "%s must be an absolute path" % label)
    resolved = path.resolve()
    root = candidate_root.resolve()
    if resolved == root or root in resolved.parents:
        raise reject("argument_vector", "%s resolves inside the candidate checkout" % label)
    return str(resolved)


def normalize_permission_mode(value: object) -> str:
    """Return the mode when it is exactly the mandated one; otherwise reject by name."""
    if value is None:
        raise reject("permission_mode", "the explicit permission mode is missing")
    if not isinstance(value, str) or not value:
        raise reject("permission_mode", "the permission mode must be a non-empty string")
    if value.casefold() in FORBIDDEN_PERMISSION_MODES:
        raise reject("permission_mode", "permission mode %r is a named failure" % (value,))
    if value != REQUIRED_PERMISSION_MODE:
        raise reject("permission_mode", "permission mode is not the mandated dontAsk")
    return value


def _reject_switch_injection(extra: Sequence[object]) -> tuple[str, ...]:
    """Validate controller-supplied trailing arguments.

    These come from the pinned launch configuration, not from the Reviewer — but a configuration is
    still a file, and a file is still bytes someone could edit.  The check is cheap and the failure
    mode it prevents (a second `--permission-mode`, a `--settings` override) is not.
    """
    checked: list[str] = []
    for index, item in enumerate(extra):
        text = _require_text(item, "launch_config.extra_args[%d]" % index)
        if _SWITCH_SHAPED.match(text):
            base = text.split("=", 1)[0].casefold()
            if base == PERMISSION_SWITCH:
                raise reject(
                    "permission_mode", "a duplicate permission-mode switch was supplied"
                )
            if base in FORBIDDEN_SWITCHES:
                raise reject("argument_vector", "switch %r is not grantable by this launcher" % base)
        checked.append(text)
    return tuple(checked)


def build_launch_plan(
    launch_config: Mapping[str, object],
    *,
    prompt_path: str,
    candidate_root: str,
) -> LaunchPlan:
    """Build the one permitted headless Reviewer vector, or reject by category.

    ``launch_config`` is the sealed controller input (see :mod:`launcher.inputs`).  ``prompt_path``
    is the controller-owned immutable snapshot of the Reviewer instructions.
    """
    if not isinstance(launch_config, Mapping):
        raise reject("argument_vector", "launch configuration must be a mapping")

    root = pathlib.Path(candidate_root)
    mode = normalize_permission_mode(launch_config.get("permission_mode"))

    executable = _require_absolute_outside(
        _require_text(launch_config.get("executable"), "launch_config.executable"),
        root,
        "launch_config.executable",
    )
    working_directory = _require_text(
        launch_config.get("working_directory"), "launch_config.working_directory"
    )
    working = pathlib.Path(working_directory)
    if not working.is_absolute():
        raise reject("argument_vector", "launch_config.working_directory must be absolute")

    prompt = pathlib.Path(_require_text(prompt_path, "prompt_path"))
    if not prompt.is_absolute():
        raise reject("argument_vector", "prompt_path must be absolute")
    prompt_resolved = _require_absolute_outside(str(prompt), root, "prompt_path")

    extra = launch_config.get("extra_args", ())
    if isinstance(extra, (str, bytes)) or not isinstance(extra, Sequence):
        raise reject("argument_vector", "launch_config.extra_args must be a sequence")
    trailing = _reject_switch_injection(extra)

    # Controller-owned interpreter prefix, validated exactly like the trailing arguments.
    #
    # This exists because the real CLI is not always a bare executable: on Windows it is commonly a
    # script that an interpreter runs, so a vector that can only be `<exe> -p ...` cannot express the
    # actual invocation — and, in testing, cannot be pointed at a controlled fake executable that
    # reports the argv it received.  Without that, "the boundary is preserved" would be a claim about
    # a vector nobody ever observed a process receive.  It is a *prefix*, so it can never displace or
    # duplicate the permission-mode switch, and it goes through the same injection screen.
    prefix_source = launch_config.get("executable_args", ())
    if isinstance(prefix_source, (str, bytes)) or not isinstance(prefix_source, Sequence):
        raise reject("argument_vector", "launch_config.executable_args must be a sequence")
    prefix = _reject_switch_injection(prefix_source)

    # Fixed template.  The only variable slots are the ones the controller minted.
    argv: tuple[str, ...] = prefix + (
        "-p",
        "--permission-mode",
        mode,
        "--prompt-file",
        prompt_resolved,
    ) + trailing

    _assert_single_permission_mode(argv)
    return LaunchPlan(
        executable=executable,
        argv=argv,
        working_directory=str(working.resolve()),
        prompt_path=prompt_resolved,
    )


def _assert_single_permission_mode(argv: Sequence[str]) -> None:
    """Post-condition on the built vector, checked with a branch rather than ``assert``.

    ``python -O`` deletes ``assert``.  A security post-condition written as ``assert`` is a
    post-condition that disappears exactly when someone optimizes the run — so this Packet never
    writes one.
    """
    occurrences = [index for index, token in enumerate(argv) if token == PERMISSION_SWITCH]
    if len(occurrences) != 1:
        raise reject("permission_mode", "the built vector does not carry exactly one permission mode")
    position = occurrences[0]
    if position + 1 >= len(argv):
        raise reject("permission_mode", "the permission-mode switch has no value")
    if argv[position + 1] != REQUIRED_PERMISSION_MODE:
        raise reject("permission_mode", "the built vector does not carry the mandated dontAsk")


def describe(plan: LaunchPlan) -> dict[str, object]:
    """Machine-readable evidence for the retained artifact set.

    The prompt *path* is evidence; the prompt *bytes* are not recorded here.  Reviewer instructions
    can carry anything, including a credential someone pasted, and an artifact is retained.
    """
    return {
        "executable": plan.executable,
        "argv": list(plan.argv),
        "working_directory": plan.working_directory,
        "prompt_path": plan.prompt_path,
        "permission_mode": REQUIRED_PERMISSION_MODE,
        "argument_count": len(plan.argv),
        "shell": False,
    }
