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
    # 20-08-2026 — don benh "phien hoi qua nhieu xac nhan" tai phat: settings.json committed
    # nay ALLOW rong rai cho viec thuong ngay (kien truc 7c51e84: mac dinh KHONG hoi, chot
    # giu o hook + deny), nen cac HINH DANG thuc su nguy hiem don ve day. Hook quet CA CHUOI
    # lenh (khong dinh bay prefix-pattern cua settings: "git push origin --force" thoat khoi
    # rule "git push --force:*" nhung khong thoat regex).
    # NOI THANG GIOI HAN: day la danh sach HINH DANG de hoi lai, KHONG phai hang rao an ninh
    # chong ke gian (bai hoc "danh sach cam khong bao gio du") — phien agent la nguoi nha,
    # muc tieu la chan tay trot, khong phai chan tan cong.
    (r"\bgit\s+push\b[^|;&]*(\s--force\b|\s-f\b|\s--delete\b|\s--prune\b|\s\+\S|\s:\S)",
     "git push pha lich su / xoa ref (force/-f/--delete/+ref/:ref)"),
    (r"\bgit\s+reset\s+[^|;&]*--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\b[^|;&]*\s-[a-zA-Z]*f", "git clean -f (xoa tep untracked)"),
    (r"\bgit\s+branch\s+[^|;&]*(-D\b|--delete\s+--force)", "xoa nhanh chua merge (branch -D)"),
    (r"\bgit\s+update-ref\s+[^|;&]*-d\b", "xoa ref truc tiep (update-ref -d)"),
    (r"\bgit\s+worktree\s+remove\s+[^|;&]*--force\b", "go worktree con thay doi (--force)"),
    (r"\bgh\s+pr\s+merge\b", "land PR — land authority (§8 protocol), nguoi giu duyet"),
    (r"\bgh\s+repo\s+(delete|rename|edit|archive)\b", "sua/xoa/doi ten repo"),
    (r"\bgh\s+(issue|pr)\s+(delete|transfer|lock|unlock|pin|unpin)\b", "xoa/khoa/chuyen issue-PR"),
    (r"\bgh\s+run\s+(cancel|delete)\b", "huy/xoa workflow run"),
    (r"\bgh\s+workflow\s+(enable|disable)\b", "bat/tat workflow — doi DINH NGHIA cong"),
    (r"\bgh\s+secret\b", "dung den GitHub secrets"),
    (r"\bgh\s+auth\s+(login|logout|refresh|setup-git)\b", "doi trang thai xac thuc gh"),
    (r"(?i)\bgh\s+api\b[^|;&]*\s(-X|--method)[= ]?\s*(POST|PATCH|PUT|DELETE)\b",
     "gh api mutate (POST/PATCH/PUT/DELETE)"),
    (r"\bgh\s+api\s+graphql\b[^|;&]*mutation", "gh api graphql mutation"),
    (r"--dangerously-skip-permissions|--dangerously-bypass-approvals",
     "spawn agent bo TOAN BO phanh — dung allowlist hep thay the (xem GOI_AGENT_DA_NEN.md)"),
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
