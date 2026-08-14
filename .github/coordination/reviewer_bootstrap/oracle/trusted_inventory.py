"""Single machine source for trusted RA-02 inventory and protocol keys.

This module contains no Mission or Packet authority values.  Those values arrive
in the sealed Dispatcher bundle and are verified against the measured checkout.

Mọi hằng dùng chung giữa runner, oracle và selftest phải khai báo Ở ĐÂY đúng MỘT
lần.  Bản sao thứ hai của một bảng hằng là thứ trôi lệch âm thầm — bên quên cập
nhật chính là bên đẩy lọt.
"""

from __future__ import annotations

# Gốc duy nhất của hai tiền tố ghi được phép; source_pin và oracle đều dẫn xuất
# từ đây thay vì viết lại chuỗi ".github/coordination/reviewer_bootstrap/...".
REVIEWER_BOOTSTRAP_ROOT = ".github/coordination/reviewer_bootstrap"
ORACLE_PREFIX = REVIEWER_BOOTSTRAP_ROOT + "/oracle/"
SANDBOX_PREFIX = REVIEWER_BOOTSTRAP_ROOT + "/sandbox/"
TRUSTED_PREFIXES = (ORACLE_PREFIX, SANDBOX_PREFIX)

TRUSTED_SOURCE_PATHS = (
    ORACLE_PREFIX + "__init__.py",
    ORACLE_PREFIX + "authority.py",
    ORACLE_PREFIX + "corpus.json",
    ORACLE_PREFIX + "corpus.py",
    ORACLE_PREFIX + "engine.py",
    ORACLE_PREFIX + "fake_validators.py",
    ORACLE_PREFIX + "oracle.py",
    ORACLE_PREFIX + "safe_io.py",
    ORACLE_PREFIX + "selftest.py",
    ORACLE_PREFIX + "source_pin.py",
    ORACLE_PREFIX + "trusted_inventory.py",
    SANDBOX_PREFIX + "__init__.py",
    SANDBOX_PREFIX + "runner.py",
    SANDBOX_PREFIX + "selftest.py",
)

# Corpus nằm TRONG cây tin cậy: một corpus chỉ tồn tại trên máy Executor là đầu
# vào mà không ai kiểm lại được (R1 của verdict 5297249899).  Ghim ở đây nghĩa là
# digest kiểm kê trusted-source đã phủ luôn cả corpus.
PINNED_CORPUS_PATH = ORACLE_PREFIX + "corpus.json"
SOURCE_PIN_PATH = ORACLE_PREFIX + "source_pin.py"
TRUSTED_INVENTORY_PATH = ORACLE_PREFIX + "trusted_inventory.py"

PROTOCOL_SOURCE_PATH = "docs/PROTOCOL_DA_PHIEN.md"

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

# Ba control khả chuyển này KHÔNG phải bộ đầy đủ: chúng không đo được một ID nào
# trong SANDBOX_TEST_IDS.  Tên tách riêng để báo cáo nói rõ điều đó.
SANDBOX_PORTABLE_CONTROL_IDS = (
    "watchdog_timeout_precedes_cpu_heuristics",
    "cpu_limit_requires_explicit_signal_evidence",
    "descendant_checks_treat_zombies_as_gone_with_one_snapshot",
    "disposable_namespace_guard_rejects_inherited_environment_claim",
    "host_loopback_fixture_refuses_outside_disposable_namespace",
)

FAKE_VALIDATOR_IDS = (
    "always_pass",
    "always_fail",
    "exact_hash_only",
    "stdout_forger",
    "path_aware_detector",
)

# Trần authority: Dispatcher cấp trong pin niêm phong; mọi bó authority thấp hơn
# sàn này phải chết TRƯỚC khi oracle chạy (R3).
AUTHORITY_FLOOR_KEYS = (
    "mission_issue",
    "mission_revision_min",
    "packet_issue",
    "packet_revision_min",
    "packet_generation_min",
)
