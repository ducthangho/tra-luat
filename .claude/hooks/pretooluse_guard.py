"""PreToolUse guard (dev-side, KHONG vao zip deploy): lenh Bash cham nhom MUTATE cua tra-luat
-> tra permissionDecision=ask de user duyet tay (KHONG deny cung — runbook van co ngay phai chay --apply).
Exit 0 + khong output = cho qua binh thuong."""
import json
import re
import shlex
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


# --- Packet #324 pha A1 (2026-08-26): DANH SACH CHO PHEP cho agent read-only ---
# `.claude/agents/tl-auditor.md` va `tl-rasoat.md` tu khai "Ranh gioi cung ... TUYET DOI khong
# ghi ... khong duoc lach qua Bash". Do 2026-08-26: 8/8 hinh dang GHI (sed -i, >, >>, tee, cp,
# mv, python -c, : >) di LOT qua chot nay, trong khi hai ca doi chung (rm -rf, push --force)
# tra `ask` — tuc phep do co rang va ket luan dung: KHONG TANG NAO chan duong ghi.
# `disallowedTools: Write, Edit, NotebookEdit` cua tl-rasoat chan TEN TOOL, khong chan DUONG GHI.
#
# Vi sao dao thanh danh sach CHO PHEP chu khong noi them vao RISKY: doctrine "Danh sach CAM
# khong bao gio du — phai dao thanh danh sach CHO PHEP". Them 8 hinh dang thi con dd, perl -pi,
# patch, install, truncate, ex, printf >, >| ... thua tu trong thiet ke.
#
# Vi sao KHONG dung `--allowedTools "Bash(x:*)"`: luat ay khop TIEN TO chuoi lenh, nen moi lenh
# co ong/`;`/`>`/`$( )`/heredoc/gan bien dung truoc deu truot — da lam chet ba luot cross-review
# (packet #314). Khoi nay doc CA CHUOI roi TACH theo toan tu shell, nen khong dinh bay do.
#
# `agent_type` DA DO co that trong payload PreToolUse cua subagent (2026-08-26, Claude Code
# 2.1.246): subagent `tl-auditor` -> `agent_type: "tl-auditor"`; Bash cua PHIEN CHINH thi khoa
# ay KHONG TON TAI (khong phai rong). Nen "vang mat => phien chinh" phan biet duoc, khong doan.
_AGENT_CHI_DOC = frozenset({"tl-auditor", "tl-rasoat"})

_CHUONG_TRINH_CHO_PHEP = frozenset({
    "cat", "head", "tail", "wc", "ls", "sort", "uniq", "cut", "tr", "nl",
    "echo", "printf", "basename", "dirname", "pwd", "date", "true", "false",
    "diff", "sha256sum", "md5sum", "stat", "file", "test", "[",
    "rg", "grep", "egrep", "fgrep", "jq", "ruff",
    "git", "python", "python3", "py", "sed", "awk", "find",
})
# CO Y VANG MAT (dung xem la thieu sot): tee cp mv rm mkdir touch chmod ln dd truncate patch
# install xargs sh bash env command which eval source. `env`/`command`/`xargs` bi loai vi chung
# CHAY DUOC chuong trinh khac — cho phep chung la vo hieu hoa ca danh sach nay.

_GIT_LENH_DOC = frozenset({
    "log", "diff", "status", "show", "rev-parse", "rev-list", "ls-files", "ls-tree",
    "cat-file", "for-each-ref", "merge-base", "blame", "grep", "describe", "name-rev",
    "shortlog", "count-objects", "symbolic-ref", "check-ignore", "ls-remote",
    "remote", "config", "branch", "tag", "diff-tree", "show-ref", "var", "help",
})
_GIT_REMOTE_GHI = frozenset({"add", "remove", "rm", "rename", "set-url", "set-head",
                             "set-branches", "prune", "update"})
_GIT_DOC_CO_CO = frozenset({"--get", "--get-all", "--get-regexp", "--list", "-l"})
_GIT_CO_GHI = frozenset({"-d", "-D", "--delete", "-m", "-M", "--move", "-f", "--force",
                         "--set-upstream", "-u", "--edit-description"})
_GIT_CO_MANG_GIA_TRI = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace"})

_RE_GAN_BIEN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_RE_KICH_BAN_CHO_PHEP = re.compile(
    r"^(?:\./)?(?:scripts/[\w.-]+\.py|\.claude/dev/[\w.-]+\.py|ops/[\w.-]+\.py)$")
_TOAN_TU_TACH = frozenset({"|", "||", "&&", ";", "&", "|&", "\n"})

# Nhom MUTATE cua chinh skill tra-luat — hai agent tu cam trong van xuoi, nay thanh CONG.
_TL_CAM = re.compile(
    r"--apply\b|--confirm\b|--clear-stale\b|--force-insert\b|--write\b|--fix\b"
    r"|\breg-delete\b|\bsource-delete\b|\bsource-rename\b|\bregister\b"
    r"|\bdrive-push\b|\bnlm-add\b|\bclasp\b|\bingest\w*\b|\bgas-deploy\b")


def _boc_thay_the(cmd):
    """Tach `$(...)` va backtick ra khoi chuoi. Tra (danh sach lenh BEN TRONG, chuoi da thay).

    Noi dung ben trong phai duoc kiem RIENG — bo qua no la de nguyen mot duong chay lenh."""
    trong, ra, i, n = [], [], 0, len(cmd)
    while i < n:
        if cmd[i:i + 2] in ("$(", "<("):
            sau, j = 1, i + 2
            while j < n and sau:
                if cmd[j:j + 2] in ("$(", "<("):
                    sau += 1
                    j += 2
                    continue
                if cmd[j] == ")":
                    sau -= 1
                j += 1
            if sau:
                return trong, None          # ngoac khong dong -> fail-close
            trong.append(cmd[i + 2:j - 1])
            ra.append("THAYTHE")
            i = j
            continue
        if cmd[i] == "`":
            j = cmd.find("`", i + 1)
            if j < 0:
                return trong, None
            trong.append(cmd[i + 1:j])
            ra.append("THAYTHE")
            i = j + 1
            continue
        ra.append(cmd[i])
        i += 1
    return trong, "".join(ra)


def _kiem_git(doi):
    i = 0
    while i < len(doi):
        a = doi[i]
        if a in _GIT_CO_MANG_GIA_TRI:
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        break
    if i >= len(doi):
        return None
    lenh, con = doi[i], doi[i + 1:]
    if lenh not in _GIT_LENH_DOC:
        return "git `%s` khong thuoc nhom doc-thuan" % lenh
    if lenh == "remote" and any(a in _GIT_REMOTE_GHI for a in con):
        return "git remote sua cau hinh"
    if lenh == "config" and not any(a in _GIT_DOC_CO_CO for a in con):
        return "git config khong o che do doc"
    if lenh in ("branch", "tag") and any(a in _GIT_CO_GHI for a in con):
        return "git %s o che do GHI/XOA" % lenh
    return None


def _kiem_python(doi):
    for a in doi:
        if a in ("-c", "-m", "-"):
            return "python %s chay ma tuy y" % a
    kich = next((a for a in doi if not a.startswith("-")), None)
    if kich is None:
        return "python khong co kich ban (doc stdin)"
    if not _RE_KICH_BAN_CHO_PHEP.match(kich):
        return "kich ban ngoai vung cho phep: %s" % kich
    return None


def _kiem_sed(doi):
    for a in doi:
        if a == "--in-place" or a.startswith("--in-place=") or (
                a.startswith("-") and not a.startswith("--") and "i" in a[1:]):
            return "sed ghi de tai cho (-i)"
    return None


def _kiem_find(doi):
    cam = {"-delete", "-exec", "-execdir", "-ok", "-okdir",
           "-fprint", "-fprint0", "-fprintf", "-fls"}
    for a in doi:
        if a in cam:
            return "find %s thi hanh/ghi" % a
    return None


def _kiem_awk(doi):
    for a in doi:
        if ">" in a or "system(" in a or "print |" in a:
            return "chuong trinh awk co chuyen huong/system()"
    return None


_KIEM_RIENG = {"git": _kiem_git, "python": _kiem_python, "python3": _kiem_python,
               "py": _kiem_python, "sed": _kiem_sed, "find": _kiem_find, "awk": _kiem_awk}


def _kiem_doan(toks):
    k = 0
    while k < len(toks) and _RE_GAN_BIEN.match(toks[k]):
        k += 1
    if k >= len(toks):
        return None                          # chi gan bien, khong chay gi
    ten = toks[k].rsplit("/", 1)[-1]
    if ten not in _CHUONG_TRINH_CHO_PHEP:
        return "chuong trinh ngoai danh sach cho phep: %s" % ten
    kiem = _KIEM_RIENG.get(ten)
    return kiem(toks[k + 1:]) if kiem else None


def _kiem_lenh_agent(cmd, sau=0):
    """None = cho phep. Chuoi = ly do TU CHOI. Moi duong khong chac chan deu tra ly do."""
    if sau > 2:
        return "long thay the lenh qua sau"
    if _TL_CAM.search(cmd):
        return "cham nhom MUTATE cua tra-luat"
    if ">(" in cmd:
        return "thay the tien trinh GHI `>( )`"
    if "<<" in cmd:
        return "heredoc — than heredoc khong tach duoc an toan, fail-close"
    # `shlex` voi whitespace_split NUOT xuong dong, nen "echo hi\ncp a b" gop thanh MOT doan va
    # chi chuong trinh DAU duoc kiem — do 2026-08-26: lenh ghi o dong 2 di LOT. Tach TRUOC khi
    # tokenize. Gop dong noi bang dau cheo nguoc truoc, keo "git log \\\n --oneline" bi cat doi.
    cmd = re.sub(r"\\\s*\n", " ", cmd)
    if "\n" in cmd:
        for dong in cmd.split("\n"):
            if dong.strip():
                ly = _kiem_lenh_agent(dong, sau)
                if ly:
                    return ly
        return None
    trong, con_lai = _boc_thay_the(cmd)
    if con_lai is None:
        return "khong tach duoc thay the lenh ($( ) hoac ` khong dong)"
    for t in trong:
        ly = _kiem_lenh_agent(t, sau + 1)
        if ly:
            return ly
    try:
        lex = shlex.shlex(con_lai, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        toks = list(lex)
    except ValueError:
        return "khong tach duoc chuoi lenh (trich dan lech)"
    doan, hien, i = [], [], 0
    while i < len(toks):
        t = toks[i]
        if t in (">", ">>", ">|"):
            if i + 1 >= len(toks) or toks[i + 1] != "/dev/null":
                return "chuyen huong GHI ra tep"
            i += 2
            continue
        if t == "<":
            i += 2
            continue
        if t in _TOAN_TU_TACH:
            if hien:
                doan.append(hien)
                hien = []
            i += 1
            continue
        hien.append(t)
        i += 1
    if hien:
        doan.append(hien)
    for d in doan:
        ly = _kiem_doan(d)
        if ly:
            return ly
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = str((data.get("tool_input") or {}).get("command") or "")

    # Agent read-only: DANH SACH CHO PHEP, fail-close, `deny` chu khong `ask` — khong co
    # nguoi ngoi duyet trong mot luot subagent, nen `ask` o day chi la `deny` cham hon.
    # `agent_type` VANG MAT => phien chinh => giu nguyen hanh vi cu. Mot truong THIEU khong
    # duoc bien thanh noi quyen.
    if str(data.get("agent_type") or "") in _AGENT_CHI_DOC:
        ly_do = _kiem_lenh_agent(cmd)
        if ly_do:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason":
                    "tra-luat guard (agent read-only `%s`): %s — agent nay CHI duoc chay lenh "
                    "doc. Can ghi thi ghi vao BAO CAO de phien chinh lam."
                    % (data.get("agent_type"), ly_do),
            }}, ensure_ascii=True))
            return 0

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
