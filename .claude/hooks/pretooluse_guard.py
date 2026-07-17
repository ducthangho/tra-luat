"""PreToolUse guard (dev-side, KHONG vao zip deploy): lenh Bash cham nhom MUTATE cua tra-luat
-> tra permissionDecision=ask de user duyet tay (KHONG deny cung — runbook van co ngay phai chay --apply).
Exit 0 + khong output = cho qua binh thuong."""
import json
import re
import sys

RISKY = [
    (r"--apply\b", "lenh mutate registry/Drive/NLM (--apply)"),
    (r"--clear-stale\b", "xoa claim NLM stale (--clear-stale)"),
    (r"\bsource-delete\b", "xoa nguon NLM"),
    (r"\breg-delete\b", "xoa dong registry"),
    (r"\bdrive_trash\b", "trash file Drive"),
    (r"\brm\s+-rf\b", "rm -rf"),
    (r"\bclasp\s+push\b", "deploy Apps Script"),
    (r"gas-deploy", "deploy Apps Script"),
    (r"--force-insert\b", "register bo qua existence-check"),
    # G4 (ke-hoach-guard-va-boc-tl-core §11, 2026-07-18): golden diff = BUG cua thay doi (R6/§6.5) —
    # regen fixtures phai la hanh dong CHU DICH user duyet (ask, khong deny cung: van co nep
    # SKILL.md-header hop le cuoi release).
    (r"golden-test\s+--write\b", "regen golden fixtures (CAM §6.5/R6 — golden 0-diff la GATE cua move)"),
]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = str((data.get("tool_input") or {}).get("command") or "")
    hits = [why for pat, why in RISKY if re.search(pat, cmd)]
    if not hits:
        return 0
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "tra-luat guard: " + "; ".join(sorted(set(hits)))
                                        + " — xac nhan truoc khi chay (doctrine: DRY truoc, --apply khi user duyet).",
        }
    }
    print(json.dumps(out, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
