"""Single machine source for trusted RA-02 inventory and protocol keys.

This module contains no Mission or Packet authority values.  Those values arrive
in the sealed Dispatcher bundle and are verified against the measured checkout.
"""

from __future__ import annotations

TRUSTED_SOURCE_PATHS = (
    ".github/coordination/reviewer_bootstrap/oracle/__init__.py",
    ".github/coordination/reviewer_bootstrap/oracle/authority.py",
    ".github/coordination/reviewer_bootstrap/oracle/corpus.py",
    ".github/coordination/reviewer_bootstrap/oracle/engine.py",
    ".github/coordination/reviewer_bootstrap/oracle/fake_validators.py",
    ".github/coordination/reviewer_bootstrap/oracle/oracle.py",
    ".github/coordination/reviewer_bootstrap/oracle/selftest.py",
    ".github/coordination/reviewer_bootstrap/oracle/source_pin.py",
    ".github/coordination/reviewer_bootstrap/oracle/trusted_inventory.py",
    ".github/coordination/reviewer_bootstrap/sandbox/__init__.py",
    ".github/coordination/reviewer_bootstrap/sandbox/runner.py",
    ".github/coordination/reviewer_bootstrap/sandbox/selftest.py",
)

PROTOCOL_SCHEMA_PATHS = (
    ".github/schemas/handoff.schema.json",
    ".github/schemas/review.schema.json",
    ".github/schemas/land.schema.json",
    ".github/schemas/state.schema.json",
    ".github/schemas/command.schema.json",
)

REQUIRED_ESCAPE_KEYS = (
    "network",
    "dns",
    "loopback",
    "metadata",
    "target_write",
    "path_escape",
    "fd_leak",
)
REQUIRED_RESOURCE_KEYS = (
    "cpu",
    "memory",
    "pid",
    "output",
    "timeout",
    "descendant_cleanup",
)

RUNNER_REQUIREMENTS = {
    "distro": "Ubuntu 24.04.4 LTS",
    "kernel": "6.18.33.2-microsoft-standard-WSL2",
    "cgroup_filesystem": "cgroup2fs",
    "cgroup_controllers": ("cpu", "memory", "pids"),
    "parent_uid": 0,
    "parent_gid": 0,
    "child_uid": 1000,
    "child_gid": 1000,
    "child_no_new_privs": 1,
}

SANDBOX_TEST_IDS = (
    "healthy_positive_control",
    "credential_channels",
    "network_dns_loopback_metadata_unix",
    "target_readonly_and_path_escapes",
    "retained_output_integrity",
    "memory_hog",
    "cpu_busy_loop",
    "pid_fork_bomb",
    "stdout_flood",
    "timeout_and_descendant_cleanup",
    "signal_handler_timeout",
)

FAKE_VALIDATOR_IDS = (
    "always_pass",
    "always_fail",
    "exact_hash_only",
    "stdout_forger",
    "path_aware_detector",
)
