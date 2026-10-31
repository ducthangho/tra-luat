"""PreToolUse guard (dev-side, KHONG vao zip deploy): lenh Bash cham nhom MUTATE cua tra-luat
-> tra permissionDecision=ask de user duyet tay (KHONG deny cung — runbook van co ngay phai chay --apply).
Exit 0 + khong output = cho qua binh thuong."""
import hashlib
import json
import pathlib
import re
import subprocess
import tempfile
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
    "git", "python", "python3", "py", "find",
})
# CO Y VANG MAT (dung xem la thieu sot): tee cp mv rm mkdir touch chmod ln dd truncate patch
# install xargs sh bash env command which eval source. `env`/`command`/`xargs` bi loai vi chung
# CHAY DUOC chuong trinh khac — cho phep chung la vo hieu hoa ca danh sach nay.
# `sed` va `awk` BI LOAI sau cross-review codex tren PR #328 (2 finding P1, da tai hien):
#   sed -n 'w scripts/tl.py' CLAUDE.md              ALLOW  — lenh `w` cua sed GHI tep
#   awk 'BEGIN { system ("touch x") }'                ALLOW  — bo kiem chi do chuoi `system(`,
#                                                            mot khoang trang la thoat
# Ca hai la NGON NGU co lenh ghi rieng, khong phan tich tin cay duoc bang chuoi — va awk con
# dung duoc bieu thuc de DUNG ten ham luc chay. Va tai cho la lai danh sach CAM. `rg` `grep`
# `cut` `head` `tail` du cho viec doc cua hai agent nay.

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
                         "--set-upstream", "-u", "--edit-description", "-c", "-C", "--copy"})
_GIT_CO_LIET_KE = frozenset({"--list", "-l"})
_GIT_CO_MANG_GIA_TRI = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace"})

# ── TANG 1: TEN LENH `tl` ─────────────────────────────────────────────────────────────────
# Lo do duoc o #336 muc 1: `recat` tran LOT `_TL_CAM`, vi `_TL_CAM` do CO ma `recat` khong
# can co nao de ghi. Chan theo TEN LENH moi la dung tang: `read_only` la thuoc tinh cua
# LENH, khong phai cua co. 90 ten duoi sinh tu `COMMAND_META` (read_only=False) va duoc
# cong CI doi chieu lai — xem `--kiem-bang`. Bang nay SE TROI khi `tl` them lenh; cong CI
# la thu duy nhat giu no khong troi, nen dung bo cong ay di.
_TL_LENH_GHI = frozenset({
    "agent-creds-set",   # WP1009: ghi credential agent len Drive — subagent PHAI bi chan
    "agent-creds-exec",  # WP1038: dat credential vao tien trinh khac — subagent PHAI bi chan
    "backfill-hieuluc", "backfill-loai", "backfill-nlm-status", "backfill-notebook",
    "backfill-title-vn", "bench", "boot", "bootstrap", "bundle-export", "cache-build",
    "cache-snapshot", "chunk-apply", "config-pin-registry", "confirm", "consolidation-cleanup",
    "corpus-audit", "corpus-fix", "dedup-corpus", "dedup-plan", "doc-patch", "download",
    "drive-push", "edit-skill", "external-ingest", "extract", "fetch-batch", "golden-test",
    "gws-auth-load", "gws-auth-stage", "gws-bootstrap-cowork", "ingest", "ingest-inbox",
    "ingest-local", "ingest-missing", "ingest-ocr", "ingest-zip", "init-config", "instructions",
    "journal", "loop", "manifest", "missing-sohieu", "nlm-add", "nlm-auth-load",
    "nlm-auth-pull", "nlm-auth-stage", "nlm-install", "nlm-migrate", "nlm-reconcile",
    "nlm-source-remove", "ocr-run", "profile-adopt", "profile-backfill-markers",
    "profile-create", "profile-delete", "profile-doctor", "profile-file-add",
    "profile-file-remove", "profile-from-nlm", "profile-index", "profile-ingest",
    "profile-ingest-chunks", "profile-ingest-ocr", "profile-ingest-zip",
    "profile-materialize-sources", "profile-promote", "profile-rebuild-registry",
    "profile-rename", "profile-set-meta", "profile-sync", "profile-use", "push-overflow",
    "quarantine-fix", "rasoat-loop", "rasoat-merge", "recat", "reconcile", "reg-delete",
    "register", "relation-backfill", "release-bundle", "release-check", "release-manifest",
    "resume", "secrets-set", "secrets-stage", "shared-source-fix", "source-delete",
    "source-rename", "source-update-corpus", "state-put", "the-thuc-build",
    "the-thuc-normalize", "undo", "up", "vbhn-year-fix", "verify-staged",
})
# Lenh LONG (`tl <nhom> <lenh>`) — phai so HAI token, khong phai mot.
_TL_LENH_GHI_LONG = frozenset({
    "hygiene plan", "hygiene reconcile", "rasoat keywords", "rasoat orchestrate",
    "rasoat phuluc", "rasoat titles", "rasoat worksheet",
})

# WP1038 (S5 sau F01/F03/F04/F06, chu kho duyet): bang CHO PHEP — subagent chi chay `tl.py` khi ten lenh KHOP DUNG mot
# lenh read_only=True. Guard (shlex) khong the doc ten lenh nhu Bash; ten la/manh/dong => deny. `--kiem-bang` doi chieu.
_TL_LENH_DOC = frozenset({
    "cat-audit", "cat-list", "cat-verify", "chunk-plan", "chunk-verify", "cluster", "convert-verify",
    "corpus-relation-sweep", "counts", "cowork-plan", "dedup-check", "deploy-plan", "determinism-audit",
    "doc-claims-check", "doc-compare", "doc-text", "doctor", "drive-parity", "exists", "fetch-links", "fetch-route",
    "final-acceptance", "find-doc", "footnote-map", "frontier-expand", "go-live-runbook", "gws-ping",
    "header-verify", "hygiene query", "hygiene scan", "ingest-analyze", "ingest-route", "instruction-audit",
    "link-priority", "live-contract-check", "live-readiness", "live-smoke-plan", "live-state-diff",
    "live-state-snapshot", "locate", "nlm-audit-physical", "nlm-auth-status", "nlm-content", "nlm-cross", "nlm-get",
    "nlm-links", "nlm-list", "nlm-orphans", "nlm-query", "nlm-query-plan", "ocr-analyze", "ocr-verify", "ops-plan",
    "overflow-resolve", "overlap", "perf", "ping", "precheck", "preflight", "profile-files", "profile-info",
    "profile-list", "profile-load", "profile-manifest", "rasoat-chongcheo", "reg-query", "registry-coverage",
    "registry-doctor", "registry-map", "relation-check", "release-verify", "review-queue", "rollback-plan",
    "route-task", "secrets-keygen", "slot-audit", "source-map", "source-verify", "state-get", "status", "sweep",
    "test-fragments-check", "the-thuc-check", "tool-inventory", "transport-info", "tvpl-url", "vbhn-check",
    "vbhn-compare", "vbhn-normalize", "vbhn-verify", "verify-integrity", "workflow-audit", "xref",
})
_TL_CHA_LONG = frozenset(x.split()[0] for x in _TL_LENH_GHI_LONG | _TL_LENH_DOC if " " in x)

# ── TANG 2: CO, theo DANH SACH CHO PHEP tung chuong trinh ─────────────────────────────────
# Doctrine kho: "danh sach CAM khong bao gio du — phai dao thanh danh sach CHO PHEP".
# Lo #336 muc 2 va 3 deu la co GHI cua chuong trinh DUOC PHEP: `git diff --output=F` tao tep
# 1559 B, `ruff check --output-file=F` tao tep 9840 B. Ca hai LOT vi cong chi soi TEN chuong
# trinh, roi (voi git) BO QUA MOI CO.
#
# Vi sao KHONG liet ke ~600 co dai ma 30 chuong trinh phoi ra qua `--help`: liet ke het roi
# danh dau an/khong-an chinh la doan xem cai nao an — tuc mot danh sach CAM doi vai. Bang
# duoi chi chua co ma hai agent doc THAT SU can; moi co khac, ke ca co MOI cua ban coreutils
# tuong lai, TU DONG bi tu choi. Do la chieu fail-close dung.
#
# `--kiem-bang` doi chieu bang nay voi `--help` cua chuong trinh DA CAI: moi co o day phai
# TON TAI that. Do la phep do bat duoc lo #336 muc 4+5 — `_kiem_diff` canh `--output`, mot
# co ma `diff` KHONG HE CO (`diff: unrecognized option '--output'`).
_CO_CHO_PHEP = {
    "git":   frozenset({"-C", "-c", "-n", "-p", "-U", "-M", "-l", "-q", "-v", "-z",
                        "--oneline", "--stat", "--numstat", "--shortstat", "--name-only",
                        "--name-status", "--format", "--pretty", "--date", "--graph",
                        "--all", "--merges", "--no-merges", "--follow", "--reverse",
                        "--porcelain", "--short", "--long", "--branch", "--untracked-files",
                        "--cached", "--staged", "--word-diff", "--color", "--no-color",
                        "--abbrev", "--no-patch", "--quiet", "--verify", "--max-count",
                        "--since", "--until", "--author", "--grep", "--first-parent",
                        "--is-ancestor", "--count", "--heads", "--tags", "--max-parents",
                        "--contains", "--merged", "--no-merged", "--list", "--get",
                        "--get-all", "--get-regexp", "--show-toplevel", "--show-object-format",
                        "--is-shallow-repository", "--is-inside-work-tree", "--abbrev-ref",
                        "--symbolic-full-name", "--no-optional-locks", "--no-pager",
                        "--unified", "--find-renames", "--text", "--decorate",
                        "-uall", "-uno"}),
    "ruff":  frozenset({"--select", "--ignore", "--output-format", "--statistics", "--no-cache",
                        "--quiet", "-q", "--config", "--isolated", "--preview", "--exclude",
                        "--extend-select", "--line-length", "--target-version", "--no-fix"}),
    "rg":    frozenset({"-n", "-i", "-l", "-c", "-o", "-w", "-F", "-e", "-A", "-B", "-C", "-U",
                        "-g", "-t", "-m", "-v", "-H", "-h", "-r", "-S", "-s", "-u", "-P",
                        "--line-number", "--ignore-case", "--files-with-matches", "--count",
                        "--count-matches", "--only-matching", "--word-regexp",
                        "--fixed-strings", "--regexp", "--after-context", "--before-context",
                        "--context", "--multiline", "--multiline-dotall", "--glob", "--type",
                        "--max-count", "--invert-match", "--with-filename", "--no-filename",
                        "--no-heading", "--heading", "--color", "--files", "--hidden",
                        "--no-ignore", "--smart-case", "--case-sensitive", "--sort",
                        "--null-data", "--max-columns", "--max-depth", "--pcre2"}),
    "grep":  frozenset({"-n", "-i", "-l", "-c", "-o", "-w", "-F", "-E", "-e", "-A", "-B", "-C",
                        "-r", "-R", "-v", "-h", "-H", "-q", "-a", "-x", "-s", "-z", "-m",
                        "--line-number", "--ignore-case", "--files-with-matches", "--count",
                        "--only-matching", "--word-regexp", "--fixed-strings", "--regexp",
                        "--extended-regexp", "--after-context", "--before-context",
                        "--context", "--recursive", "--invert-match", "--no-filename",
                        "--with-filename", "--quiet", "--color", "--include", "--exclude",
                        "--max-count", "--text", "--binary-files", "--null-data",
                        "--line-regexp"}),
    "sort":  frozenset({"-n", "-r", "-u", "-k", "-t", "-f", "-b", "-h", "-V", "-g", "-s", "-z",
                        "--numeric-sort", "--reverse", "--unique", "--key",
                        "--field-separator", "--ignore-case", "--version-sort", "--stable",
                        "--zero-terminated", "--human-numeric-sort",
                        "--general-numeric-sort"}),
    "uniq":  frozenset({"-c", "-d", "-u", "-i", "-f", "-s", "-w", "-z",
                        "--count", "--repeated", "--unique", "--ignore-case",
                        "--skip-fields", "--skip-chars", "--check-chars",
                        "--zero-terminated"}),
    "cut":   frozenset({"-d", "-f", "-c", "-b", "-s", "-z", "--delimiter", "--fields",
                        "--characters", "--bytes", "--only-delimited", "--complement"}),
    "head":  frozenset({"-n", "-c", "-q", "-v", "-z", "--lines", "--bytes", "--quiet",
                        "--silent", "--verbose", "--zero-terminated"}),
    "tail":  frozenset({"-n", "-c", "-q", "-v", "-z", "--lines", "--bytes", "--quiet",
                        "--silent", "--verbose", "--zero-terminated"}),
    "wc":    frozenset({"-l", "-w", "-c", "-m", "-L", "--lines", "--words", "--bytes",
                        "--chars", "--max-line-length"}),
    "tr":    frozenset({"-d", "-s", "-c", "-t", "--delete", "--squeeze-repeats",
                        "--complement", "--truncate-set1"}),
    "nl":    frozenset({"-b", "-n", "-w", "-s", "-v", "--body-numbering", "--number-format",
                        "--number-width", "--number-separator"}),
    "ls":    frozenset({"-l", "-a", "-A", "-h", "-t", "-r", "-S", "-1", "-d", "-R", "-i", "-n",
                        "--all", "--almost-all", "--human-readable", "--reverse",
                        "--directory", "--recursive", "--time", "--sort", "--color",
                        "--format", "--time-style", "--full-time", "--inode"}),
    "cat":   frozenset({"-n", "-b", "-A", "-e", "-t", "-s", "-v", "-E", "-T",
                        "--number", "--show-all", "--squeeze-blank", "--show-ends",
                        "--show-tabs", "--show-nonprinting", "--number-nonblank"}),
    "jq":    frozenset({"-r", "-c", "-e", "-n", "-s", "-S", "-j", "-a", "-R", "--raw-output",
                        "--compact-output", "--exit-status", "--null-input", "--slurp",
                        "--sort-keys", "--join-output", "--arg", "--argjson", "--tab",
                        "--indent", "--ascii-output", "--raw-input",
                        "--monochrome-output"}),
    "diff":  frozenset({"-u", "-U", "-r", "-q", "-i", "-w", "-b", "-B", "-N", "-a", "-y",
                        "--unified", "--recursive", "--brief", "--ignore-case",
                        "--ignore-all-space", "--ignore-space-change",
                        "--ignore-blank-lines", "--new-file", "--text", "--side-by-side",
                        "--color", "--label"}),
    "find":  frozenset({"-name", "-iname", "-type", "-path", "-ipath", "-maxdepth",
                        "-mindepth", "-print", "-print0", "-size", "-newer", "-mtime",
                        "-not", "-o", "-a", "-empty", "-regex", "-iregex", "-prune",
                        "-follow", "-xdev", "-links"}),
    "stat":  frozenset({"-c", "-f", "-t", "-L", "--format", "--printf", "--terse",
                        "--dereference", "--file-system"}),
    "file":  frozenset({"-b", "-i", "-L", "-z", "--brief", "--mime", "--mime-type",
                        "--mime-encoding", "--dereference"}),
    "date":  frozenset({"-u", "-d", "-R", "-I", "--utc", "--date", "--rfc-3339",
                        "--iso-8601", "--rfc-email", "--universal"}),
    "sha256sum": frozenset({"-b", "-t", "-c", "-z", "--binary", "--text", "--check",
                            "--zero", "--quiet", "--status"}),
    "md5sum":    frozenset({"-b", "-t", "-c", "-z", "--binary", "--text", "--check",
                            "--zero", "--quiet", "--status"}),
    "basename":  frozenset({"-a", "-s", "-z", "--multiple", "--suffix", "--zero"}),
    "dirname":   frozenset({"-z", "--zero"}),
    "echo":      frozenset({"-n", "-e", "-E"}),
    "printf":    frozenset(),
    "pwd":       frozenset({"-L", "-P"}),
    "test":      frozenset(),
    "[":         frozenset(),
    "true":      frozenset(),
    "false":     frozenset(),
    "egrep":     frozenset(),
    "fgrep":     frozenset(),
}
# MIEN TANG 2 — CO LY DO, khong phai cho tien. `tl.py` co ~180 lenh, moi lenh mot bo co
# rieng; liet ke chung o day la dung mot bang KHAC de canh mot be mat da co bo canh CHAT
# HON. Ba lop dang phu `python*`:
#   1. `_kiem_python` — cam `-c`/`-m`/`-` (chay ma tuy y) va bat kich ban phai nam trong
#      `_RE_KICH_BAN_CHO_PHEP` (scripts/ · .claude/dev/ · ops/, duoi .py);
#   2. TANG 1 `_TL_LENH_GHI` — 90 lenh `read_only=False` bi tu choi theo TEN;
#   3. `_TL_CAM` — nhom MUTATE theo co (`--apply` `--write` ...).
# DE `frozenset()` RONG thi TANG 2 tu choi MOI co, ke ca `--json`: DO DUOC — ca
# `python scripts/tl.py cat-audit --json | head -40` bi CHAN OAN, va `t3` bat duoc.
_MIEN_TANG2 = frozenset({"python", "python3", "py"})

# HO CO SINH TEP cua `tl` — do trong Issue #336: 187 subcommand co `--help` rc=0, 45 nhan
# DUNG `--out`, 47 nhan mot trong bon ten duoi. Day KHONG phai mot danh sach cam doan ra:
# `--kiem-bang` doi chieu no voi `write_scope` trong COMMAND_META va DO se khi co lenh
# `read_only=True` ma `write_scope != "none"` lai khong bi ho co nay phu.
# Vi sao can: TANG 1 chi chan `read_only=False`. Nhung `read_only=True` + `write_scope`
# khac "none" nghia la "CHI ghi khi nguoi goi tu khai `--out`" (chinh chu thich trong
# command_registry.py noi vay). Do duoc: `tl sweep --out /tmp/x` -> ALLOW truoc khi co ho
# co nay, va `sweep` KHONG nam trong 90 ten cua TANG 1.
_TL_CO_SINH_TEP = frozenset({"--out", "--output", "--out-dir", "--output-file"})
# `egrep`/`fgrep` de RONG CO CHU DINH: chung la wrapper bi khai tu, va cho co qua day la
# nhan doi be mat phai canh. Ai can thi dung `grep -E` / `grep -F` — deu nam trong bang.
# `python*` de RONG vi `_kiem_python` da soi rieng va CHAT HON (chi cho kich ban trong vung
# cho phep, cam -c/-m/-); bang co o day chi lam yeu di.

# Co MANG GIA TRI o token KE TIEP (`-n 5`), khac voi `--x=5` gop mot token. Khong biet dieu
# nay thi gia tri cua co bi doc nham thanh doi so VI TRI — dung lo `uniq IN OUT`.
_CO_AN_GIA_TRI = {
    "git":  frozenset({"-C", "-c", "-n", "-U", "-M", "--format", "--pretty", "--date",
                       "--abbrev", "--max-count", "--since", "--until", "--author", "--grep",
                       "--untracked-files", "--unified", "--max-parents", "--contains",
                       "--merged", "--no-merged", "--find-renames"}),
    "ruff": frozenset({"--select", "--ignore", "--output-format", "--config", "--exclude",
                       "--extend-select", "--line-length", "--target-version"}),
    "rg":   frozenset({"-e", "-A", "-B", "-C", "-g", "-t", "-m", "-r", "--regexp", "--glob",
                       "--type", "--max-count", "--after-context", "--before-context",
                       "--context", "--color", "--sort", "--max-columns", "--max-depth"}),
    "grep": frozenset({"-e", "-A", "-B", "-C", "-m", "--regexp", "--after-context",
                       "--before-context", "--context", "--max-count", "--include",
                       "--exclude", "--color", "--binary-files"}),
    "sort": frozenset({"-k", "-t", "--key", "--field-separator"}),
    "uniq": frozenset({"-f", "-s", "-w", "--skip-fields", "--skip-chars", "--check-chars"}),
    "cut":  frozenset({"-d", "-f", "-c", "-b", "--delimiter", "--fields", "--characters",
                       "--bytes"}),
    "head": frozenset({"-n", "-c", "--lines", "--bytes"}),
    "tail": frozenset({"-n", "-c", "--lines", "--bytes"}),
    "nl":   frozenset({"-b", "-n", "-w", "-s"}),
    "jq":   frozenset({"--arg", "--argjson", "--indent"}),
    "diff": frozenset({"-U", "--unified", "--label", "--color"}),
    "stat": frozenset({"-c", "--format", "--printf"}),
    "date": frozenset({"-d", "--date"}),
    "basename": frozenset({"-s", "--suffix"}),
    "ls":   frozenset({"--color", "--format", "--sort", "--time", "--time-style"}),
}

_RE_CO_NGAN_GOP = re.compile(r"^-[A-Za-z0-9]{2,}$")
_RE_SO_TRAN = re.compile(r"^-[0-9]+$")
# `head -3` la viet tat cua `-n 3`. KHONG suy rong — DO tung chuong trinh:
#   `-3` -> rc=0     tren head · tail · uniq · git · grep · diff
#   `-3` -> rc!=0    tren sort · ls · rg · cat · nl
# Cho `-3` qua o chuong trinh khong nhan no la noi be mat ma khong mua duoc gi.
#
# CHO NAY TUNG CO HAI KHOI CHU THICH NOI NGUOC NHAU: khoi cu (viet luc bang con BON ten) khai
# `-3` bi "TU CHOI boi grep · diff", va no O LAI ngay tren phep do moi noi nguoc lai. Ca
# `t16` khoa dung loi khai cu ay, nen luot 2 phai BO `t16` — nhung chu thich thi khong ai bo,
# va cross-review luot 2 bat dung no. Bo test sai thi xoa duoc; lo khai sai thi phai xoa TAY.
_CHO_SO_TRAN = frozenset({"head", "tail", "uniq", "git", "grep", "diff"})


def _kiem_co(ten, doi):
    """Danh sach CHO PHEP theo co. Co nao KHONG co trong bang => TU CHOI."""
    if ten in _MIEN_TANG2:
        return None
    cho_phep = _CO_CHO_PHEP.get(ten)
    if cho_phep is None:
        return "chuong trinh chua co bang co: " + ten          # fail-close
    an = _CO_AN_GIA_TRI.get(ten, frozenset())
    i = 0
    while i < len(doi):
        a = doi[i]
        if a == "--":
            break
        if not a.startswith("-") or a == "-":
            i += 1
            continue
        goc, gop = (a.split("=", 1)[0], True) if "=" in a else (a, False)
        if _RE_SO_TRAN.match(goc) and ten in _CHO_SO_TRAN:
            i += 1
            continue
        if goc in cho_phep:
            i += 2 if (goc in an and not gop and i + 1 < len(doi)) else 1
            continue
        # CO NGAN AN GIA TRI GAN LIEN: `-n3` = `-n 3`, `-U3` = `-U 3`, `-m1`, `-k1`, `-f1`,
        # `-w3`. Phai xet TRUOC nhanh no bo co, kẻo `-n3` bi hieu la bo `-n` + `-3` roi tu
        # choi. Cross-review luot 1 do duoc MUOI ca chan oan kieu nay, gom `git log -n1` va
        # `git diff -U3` — hai lenh doc thuong nhat cua kho.
        #
        # LUOT 2 SIET QUA TAY, va cross-review luot 2 do duoc: doi `goc[2:].isdigit()` nen
        # MUOI dang gia tri KHONG PHAI SO cung bi chan oan (`-d,` cua `cut`, `-e<mau>` cua
        # `grep`, `--date`-style dinh lien, hau to don vi…). Chuong trinh THAT tra rc=0 ca
        # muoi; guard DENY ca muoi.
        # Dieu kien AN TOAN khong nam o HINH DANG gia tri ma o CHU DAU: no phai la mot co
        # CO TRONG bang cho phep VA la co AN GIA TRI. Da qua hai chot ay thi phan con lai la
        # GIA TRI cua co do — noi dung cua no khong the mo them che do nao. Neu mot binary cu
        # the khong nhan cach viet ay thi chinh binary tu choi, va do la loi cua NGUOI GOI,
        # khong phai mot che do ghi bi mo.
        if (len(goc) > 2 and not goc.startswith("--")
                and ("-" + goc[1]) in an and ("-" + goc[1]) in cho_phep):
            i += 1
            continue
        # co NGAN GOP: `-la` = `-l -a`. No ra roi kiem tung cai; mot chu xau la ca cum xau.
        if _RE_CO_NGAN_GOP.match(goc):
            xau = [c for c in ("-" + ch for ch in goc[1:]) if c not in cho_phep]
            if xau:
                return "co ngoai danh sach cho phep cua `" + ten + "`: " + " ".join(xau) \
                       + " (trong `" + goc + "`)"
            i += 1
            continue
        return "co ngoai danh sach cho phep cua `" + ten + "`: " + goc
    return None


_RE_GAN_BIEN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
# P1 `python-mien-tang2-cho-phep-script-ghi-bat-ky`: ban truoc cho MOI tep `.py` duoi
# `scripts/` `.claude/dev/` `ops/`. Do duoc: `python scripts/build_cache.py --cache-dir X`
# -> ALLOW, ma script ay `mkdir` + ghi hai tep JSON; `python .claude/dev/packet_loop.py init`
# -> ALLOW, va no ghi state. Vung theo THU MUC la mot danh sach CAM doi vai: no gia dinh moi
# tep trong ba thu muc ay khong ghi, va gia dinh do SAI ngay trong chinh cay nay.
#
# Dao thanh DANH SACH CHO PHEP TUNG TEP. Chi `scripts/tl.py` — vi no la thu duy nhat co bo
# canh rieng (TANG 1 `_TL_LENH_GHI` 104 lenh · TANG 1b `_TL_CO_SINH_TEP` · `_TL_CAM`). Moi
# tep khac bi tu choi cho toi khi co nguoi ĐO no va them vao day CO CHU DICH.
_KICH_BAN_CHO_PHEP = frozenset({"scripts/tl.py"})
_RE_KICH_BAN_CHO_PHEP = None      # giu ten cu = None de moi cho doc no deu hong TO, khong
                                  # am tham roi ve hanh vi cu
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


# P1 `git-read-subcommand-van-goi-duoc-helper-ngoai` (cross-review luot 2, PR #341).
# `-c` nam trong `_CO_CHO_PHEP["git"]`, va TANG 2 chi soi TEN CO chu khong soi GIA TRI. Nen
# `git -c core.pager=<lenh> log` la mot subcommand DOC goi mot chuong trinh NGOAI. Cung ho
# ay con `core.editor` `diff.external` `core.hooksPath` `credential.helper` `alias.*`
# `core.sshCommand` `filter.*.clean` `diff.*.textconv` … — mot tap KHONG liet het duoc, tuc
# dung hinh dang danh sach CAM. DAO: chi CHO PHEP mot tap khoa DA DO.
#
# `core.abbrev` la khoa DUY NHAT kho nay that su can o duong doc: `CLAUDE.md` §Quy uoc deploy
# muc 6 doi ghim `core.abbrev=7` khi chay cong, va `cross-review/SKILL.md` ghim no cho mirror.
# Them khoa nao thi phai co ly do DO DUOC, khong them "cho tien".
_GIT_KHOA_CAU_HINH_CHO_PHEP = frozenset({"core.abbrev"})


def _kiem_gia_tri_c(v):
    khoa = str(v).split("=", 1)[0].strip().lower()
    if khoa not in _GIT_KHOA_CAU_HINH_CHO_PHEP:
        return "git -c dat khoa cau hinh ngoai danh sach cho phep: %s" % khoa
    return None


def _kiem_git(doi):
    i = 0
    while i < len(doi):
        a = doi[i]
        if a in _GIT_CO_MANG_GIA_TRI:
            if a == "-c":
                ly = _kiem_gia_tri_c(doi[i + 1] if i + 1 < len(doi) else "")
                if ly:
                    return ly
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
    if lenh in ("branch", "tag"):
        if any(a in _GIT_CO_GHI for a in con):
            return "git %s o che do GHI/XOA" % lenh
        # `git branch TEN` / `git tag TEN` TAO ref ma khong co co nao — doi so VI TRI la dang
        # tao. Doi dang LIET KE tuong minh thay vi chi tu choi vai co (cross-review PR #328).
        if [a for a in con if not a.startswith("-")] and not any(
                a in _GIT_CO_LIET_KE for a in con):
            return "git %s co doi so VI TRI => dang TAO ref" % lenh
    return None


# Co GLOBAL cua `tl` — khai TRUOC subcommand trong `build_parser` (scripts/tl_core/cli.py).
# Hai co dau AN GIA TRI o token ke tiep, va do la lo P1 `tl-global-option-lam-lech-ten-lenh`:
# ban truoc lay "token dau tien khong bat dau bang `-`" lam ten kich ban va token thu hai lam
# ten lenh, nen `tl --profile vbqppl recat ...` day `vbqppl` vao vi tri ten lenh va `recat`
# tut xuong => TANG 1 mu. DO DUOC: `recat` tran -> deny, them `--profile vbqppl` -> ALLOW.
_TL_CO_GLOBAL_AN_GIA_TRI = frozenset({"--config", "--profile"})
_TL_CO_GLOBAL_CO_DON = frozenset({"--version", "--timings", "--deterministic", "--selftest"})


def _tach_lenh_tl(doi, kich):
    """Tra danh sach token LENH sau `tl.py`, da tieu het co global va gia tri cua chung.

    Fail-close theo huong CHAT: co global la ma KHONG biet an gia tri hay khong thi coi nhu
    CO an — bo qua mot token thua chi lam ta doc nham ten lenh thanh rong (=> khong chan),
    nen chieu an toan la nguoc lai: co la => tieu ca token sau no."""
    try:
        k = doi.index(kich) + 1
    except ValueError:
        return []
    ra = []
    while k < len(doi):
        a = doi[k]
        if a == "--":
            k += 1
            continue
        if a.startswith("-"):
            if "=" in a or a in _TL_CO_GLOBAL_CO_DON:
                k += 1
            else:
                k += 2 if not ra else 1     # co global an gia tri; sau khi da co ten lenh
            continue                         # thi co la cua chinh lenh do, khong tieu bua
        ra.append(a)
        k += 1
    return ra


# WP1038 (review F03, chu kho duyet): shlex KHONG mo rong nhu Bash — `$'recat'`, `${X:-recat}`, `re$(printf cat)`
# den tay hook van mang `$` nen khong trung bang writer, trong khi Bash dua `recat` that cho tl. DANH SACH CHO PHEP
# ky tu (khong liet ke cach viet): moi token tu sau kich ban toi het TEN LENH (co global + gia tri + ten lenh, them
# ten con neu la lenh LONG) phai nam trong tap nay; ngoai tap => coi nhu ten lenh KHONG DOC DUOC => deny.
_RE_TL_VUNG_TEN_AN_TOAN = re.compile(r"[\w./\\:=+@ -]*\Z")   # F05: \w Unicode — duong dan/profile tieng Viet


def _vung_ten_lenh_tl(doi, kich):
    """Token tu sau `tl.py` toi het ten lenh, theo dung luat tieu co cua `_tach_lenh_tl`."""
    cha_long = {x.split()[0] for x in _TL_LENH_GHI_LONG}
    k, ra, ten = doi.index(kich) + 1, [], []
    while k < len(doi) and len(ten) < (2 if ten and ten[0] in cha_long else 1):
        a = doi[k]
        if a.startswith("-") and a != "--":
            an = not ("=" in a or a in _TL_CO_GLOBAL_CO_DON)
            ra += doi[k:k + 2] if an else [a]
            k += 2 if an else 1
            continue
        ra.append(a)
        if a != "--":
            ten.append(a)
        k += 1
    return ra


# P1 `python-allowlist-lstrip-khong-phai-exact-path` (cross-review luot 2, PR #341).
# Ban luot 2 so bang `kich.lstrip("./")`. `str.lstrip` bo MOI ky tu trong tap, khong phai
# mot TIEN TO — nen `../../scripts/tl.py` co ve dung `scripts/tl.py` va lot vao danh sach
# CHO PHEP, roi duoc huong mien TANG 2 danh cho mot tep KHAC. Danh sach cho phep dung, phep
# SO thi sai: mot phep chuan hoa long hon phep so lam danh sach cho phep vo hieu.
#
# Chuan hoa CHINH XAC, fail-close: tuyet doi -> tu choi · o dia Windows -> tu choi ·
# thanh phan `..` -> tu choi · thanh phan `.` -> bo (vo hai) · chap ca hai dau phan cach
# de khong chan oan `scripts\tl.py` tren Windows.
#
# GIOI HAN, KHAI THANG: day la phep so CHUOI. Mot symlink ten `scripts/tl.py` tro di cho
# khac van qua duoc. Giai symlink doi cham he tep ngay trong hook (cham, va co dieu kien
# tranh chap), nen no KHONG duoc lam o day — no la no co ten
# `kich-ban-cho-phep-khong-giai-symlink`, va co ca test khai dung dieu do.
def _chuan_hoa_kich_ban(kich):
    """Tra duong dan repo-relative CHUAN, hoac None neu khong an toan."""
    if not kich or kich.startswith("-"):
        return None
    if kich.startswith(("/", "\\")) or (len(kich) > 1 and kich[1] == ":"):
        return None
    phan = [x for x in re.split(r"[/\\]+", kich) if x]
    if any(x == ".." for x in phan):
        return None
    phan = [x for x in phan if x != "."]
    return "/".join(phan) if phan else None


def _kiem_python(doi):
    for a in doi:
        if a in ("-c", "-m", "-"):
            return "python %s chay ma tuy y" % a
    kich = next((a for a in doi if not a.startswith("-")), None)
    if kich is None:
        return "python khong co kich ban (doc stdin)"
    chuan = _chuan_hoa_kich_ban(kich)
    if chuan is None or chuan not in _KICH_BAN_CHO_PHEP:
        return "kich ban ngoai danh sach cho phep: %s" % kich
    # TANG 1 — lo #336 muc 1. `recat` khong can CO nao de ghi, nen chan theo CO khong bao gio
    # bat duoc no; `read_only` la thuoc tinh cua LENH. Lay doi so VI TRI ke sau kich ban.
    # WP1009 F14: nhan dien tl.py tren duong dan DA CHUAN HOA (cung thu ma allowlist vua duyet) —
    # so tren `kich` goc thi `"scripts\tl.py"` qua allowlist ma bo qua ca bang writer ben duoi.
    if chuan.rsplit("/", 1)[-1] == "tl.py":
        # `$( )`/backtick da bi `_boc_thay_the` doi thanh chu `THAYTHE` (toan chu cai) — o vung ten lenh no la
        # gia tri DO SHELL TINH RA, nen cung tinh la khong doc duoc.
        la = [a for a in _vung_ten_lenh_tl(doi, kich) if not _RE_TL_VUNG_TEN_AN_TOAN.match(a) or "THAYTHE" in a]
        if la:
            return "ten lenh tl qua mo rong shell (ky tu ngoai danh sach cho phep): %s" % la[0]
        lenh = _tach_lenh_tl(doi, kich)
        ten = " ".join(lenh[:2]) if lenh and lenh[0] in _TL_CHA_LONG else (lenh[0] if lenh else None)
        if ten not in (None, *_TL_CHA_LONG) and ten not in _TL_LENH_DOC | _TL_LENH_GHI | _TL_LENH_GHI_LONG:
            return "ten lenh tl `%s` khong nam trong danh sach lenh DOC (ten la/manh/qua mo rong shell)" % ten
        if lenh and (lenh[0] in _TL_LENH_GHI
                     or " ".join(lenh[:2]) in _TL_LENH_GHI_LONG):
            return "lenh tl `%s` co read_only=False trong COMMAND_META" % " ".join(lenh[:2])
        for a in doi:
            if a.split("=", 1)[0] in _TL_CO_SINH_TEP:
                return "co sinh tep cua tl: %s (lenh read_only=True van GHI khi co co nay)" \
                       % a.split("=", 1)[0]
    return None


def _kiem_find(doi):
    cam = {"-delete", "-exec", "-execdir", "-ok", "-okdir",
           "-fprint", "-fprint0", "-fprintf", "-fls"}
    for a in doi:
        if a in cam:
            return "find %s thi hanh/ghi" % a
    return None


def _cam_co(doi, co):
    """Tu choi co lam TEP RA, ke ca dang `--x=gia-tri`. Doi thu hai cua cross-review PR #328:
    `sort -o`, `diff --output=`, `ruff --fix` deu GHI, va deu nam trong danh sach cho phep."""
    for a in doi:
        if a in co or any(a.startswith(c + "=") for c in co):
            return "co GHI ra tep: %s" % a
    return None


def _kiem_uniq(doi):
    # `uniq IN OUT` — doi so VI TRI thu hai la TEP RA, khong co co nao bao hieu.
    if len([a for a in doi if not a.startswith("-")]) > 1:
        return "uniq: doi so vi tri thu hai la TEP RA"
    return None


def _kiem_ruff(doi):
    vt = [a for a in doi if not a.startswith("-")]
    if not vt or vt[0] != "check":
        return "ruff chi duoc chay `check` (`format` GHI de tep)"
    return _cam_co(doi, ("--fix", "--fix-only", "--unsafe-fixes"))


_KIEM_RIENG = {"git": _kiem_git, "python": _kiem_python, "python3": _kiem_python,
               "py": _kiem_python, "find": _kiem_find,
               "uniq": _kiem_uniq, "ruff": _kiem_ruff}
# `sort` BO bo soi rieng cung ly do `diff`: TANG 2 da phu. DO tren ban sao tam TRUOC khi
# bo — khong _kiem_sort thi `sort -o F A` va `sort --output=F A` VAN deny (vi `-o` va
# `--output` khong nam trong `_CO_CHO_PHEP["sort"]`), con `sort A | head -3` van ALLOW.
# Dot bien `m12_bo_kiem_sort` SONG chinh vi vay: chot ay khong con rang. Kho da co tien
# le — chu thich cua chot `<>`/`>&` ghi "giu mot chot khong co rang la tu doi".
# `diff` CO Y khong co bo soi rieng: no KHONG CO co sinh tep nao. Do 2026-08-26 tren
# diffutils cua container: `diff --output=F a b` -> `unrecognized option`, rc khac 0, khong
# tao tep. `_kiem_diff` cu canh dung cai cua ay, va ca test cua no chung minh mot dieu RONG
# (lo #336 muc 4+5). Nay `diff` di qua TANG 2 nhu moi chuong trinh khac: co nao khong co
# trong `_CO_CHO_PHEP["diff"]` deu bi tu choi, ke ca `-o`/`--output` cua mot ban `diff` KHAC
# (BSD/busybox) neu ban ay co that — chan theo DANH SACH CHO PHEP thi khong can biet truoc.


# Cung P1 tren, mat thu hai: `_kiem_doan` BO QUA moi phep gan bien dat truoc lenh, nen
# `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.pager GIT_CONFIG_VALUE_0=<lenh> git log` dat
# dung thu ma `-c` vua bi chan — chi bang mot duong khac. `GIT_EXTERNAL_DIFF`, `GIT_PAGER`,
# `GIT_SSH_COMMAND`, `PAGER`, `LD_PRELOAD` cung the.
# DAO sang danh sach CHO PHEP, va giu no NHO: chi nhung bien doi NGON NGU/MAU/DEM, khong
# bien nao doi duoc chuong trinh se chay.
_BIEN_MOI_TRUONG_CHO_PHEP = frozenset({
    "LANG", "LC_ALL", "LC_CTYPE", "LC_COLLATE", "LC_NUMERIC", "LC_TIME", "TZ",
    "NO_COLOR", "CLICOLOR", "CLICOLOR_FORCE", "TERM", "COLUMNS",
    "PYTHONDONTWRITEBYTECODE", "PYTHONIOENCODING", "PYTHONUTF8", "PYTHONHASHSEED",
})


def _kiem_doan(toks):
    k = 0
    while k < len(toks) and _RE_GAN_BIEN.match(toks[k]):
        k += 1
    if k >= len(toks):
        # CHI GAN BIEN, khong chay gi => KHONG ap danh sach cho phep. Ban dau toi ap no cho
        # MOI phep gan va lam do `t3_khong_chan_oan_lenh_doc`: `M=$(git rev-parse HEAD)` bi
        # tu choi vi ten `M` khong co trong bang. Do la CHAN OAN, va no lo ra vi bo test co
        # san mot ca chieu-tha — dung thu ma cross-review PR #328 bat phai co.
        # Phan biet dung tang: gan bien THUAN chi doi bien CUA SHELL, con thu nguy hiem la
        # gan lam TIEN TO cho mot lenh (`GIT_PAGER=x git log`) — luc ay no vao moi truong
        # cua tien trinh se chay. Noi dung trong `$( )` da duoc kiem rieng o duong long nhau.
        return None
    for t in toks[:k]:
        ten = t.split("=", 1)[0]
        if ten not in _BIEN_MOI_TRUONG_CHO_PHEP:
            return "dat bien moi truong lam TIEN TO cho lenh, ngoai danh sach cho phep: %s" % ten
    ten = toks[k].rsplit("/", 1)[-1]
    if ten not in _CHUONG_TRINH_CHO_PHEP:
        return "chuong trinh ngoai danh sach cho phep: %s" % ten
    doi = toks[k + 1:]
    # TANG 2 chay cho MOI chuong trinh duoc phep, khong chi 9 chuong trinh co `_KIEM_RIENG`.
    # Truoc #336, 27/36 chuong trinh KHONG co bo soi co nao — do la lo, khong phai thiet ke.
    ly = _kiem_co(ten, doi)
    if ly:
        return ly
    kiem = _KIEM_RIENG.get(ten)
    return kiem(doi) if kiem else None


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
    cmd = re.sub(r"\\\n", "", cmd)   # WP1038 F04: Bash BO cap `\` + xuong dong (noi lien tu), khong thay bang dau cach
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
        # `shlex` phat `&>` `&>>` `<>` `>&` thanh MOT token — chot cu chi khop dung ba dang
        # `>` `>>` `>|` nen ca bon dang ghep di lot (cross-review PR #328, da tai hien).
        # Nay khop theo TINH CHAT chu khong theo danh sach dang: token nao CHUA `>` deu la
        # chuyen huong. Do roi moi bo: mot chot RIENG cho `<>`/`>&` la THUA — ca hai đeu chua
        # `>` nen nhanh nay da bat; dot bien go chot rieng ay khong lam ca nao do, tuc no
        # khong co rang. Giu mot chot khong co rang la tu doi.
        if ">" in t:
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


# ── CONG CI: doi chieu HAI BANG TINH voi NGUON THAT ───────────────────────────────────────
# Hai bang tren la BANG TINH, va bang tinh thi TROI. Cong nay la thu duy nhat giu chung
# khong troi. Chay o CI, KHONG chay trong hook — hook phai nhe vi no chan truoc MOI lenh
# Bash, va chi phi import `tl` chua ai do (#336 muc "Chua do duoc").
#
# HOI RUNTIME, KHONG PARSE VAN BAN — day la ban va cua P1 `command-meta-regex-bo-sot-writer`.
# Ban truoc doc `COMMAND_META` bang regex voi ly do "tranh chi phi import". Ly do ay dung cho
# HOOK (chan truoc moi lenh Bash) nhung SAI cho CONG: cong chay o CI, mot lan, va no phai noi
# SU THAT. Regex chi nhan entry viet thang `_m(...)`, bo qua `dict(_m(...))` va lenh LONG:
#     regex    ->  90 writer
#     runtime  -> 104 writer  (97 top-level + 7 long)
# va cong VAN IN "bang khop". Do la CONG XANH GIA — te hon khong co cong, vi no bao da kiem.
# Nam ten lot: gws-auth-stage · nlm-auth-stage · secrets-stage · secrets-set · state-put —
# deu la duong STAGE/SET CREDENTIAL, va deu ALLOW truoc ban va nay (do bang chinh guard).
#
# Phan cong dung: HOOK doc BANG TINH (nhe), CONG hoi RUNTIME (that). Bang tinh troi khoi
# runtime => cong DO.
# TACH RIENG phep dan KHOA de no DO DUOC. `cache-hash-khong-co-mutant` (cross-review luot 2):
# thuoc tinh "dem theo BAM, khong theo thoi gian" chi duoc KHAI trong docstring, khong ca nao
# giu. Ma thuoc tinh ay la thu duy nhat ngan bo dem che mot registry DA TROI: dem theo mtime
# thi `touch` la du de giu ban cu; dem theo SU TON TAI cua tep dem thi con te hon.
# Ham thuan, nhan DUONG DAN lam doi so, nen ca `t42` goi duoc voi du lieu dung san.
def _duong_bo_dem(reg):
    khoa = hashlib.sha256(pathlib.Path(reg).read_bytes()).hexdigest()[:32]
    return pathlib.Path(tempfile.gettempdir(), "tl-writer-%s.json" % khoa)


def _writer_tu_runtime(goc):
    """Tra (top_level, long, write_scope_khac_none) tu `tl tool-inventory --json`.
    None = KHONG DO DUOC.

    CO BO DEM, va khoa la BAM NOI DUNG cua `command_registry.py` — doi registry mot byte la
    dem mat hieu luc. Khong dem thi bo test goi cong 2 ca x 30 dot bien = 60 lan x ~40s.
    Dem theo THOI GIAN hay theo su TON TAI cua tep dem thi che duoc troi; dem theo BAM thi
    khong."""
    tl = pathlib.Path(goc, "scripts/tl.py")
    reg = pathlib.Path(goc, "scripts/tl_core/command_registry.py")
    if not tl.is_file() or not reg.is_file():
        return None
    dem = _duong_bo_dem(reg)
    if dem.is_file():
        try:
            d = json.loads(dem.read_text(encoding="utf-8"))
            return set(d["top"]), set(d["long"]), set(d["ws"]), set(d["doc"])
        except Exception:
            pass
    try:
        r = subprocess.run([sys.executable, "-B", str(tl), "tool-inventory", "--json"],
                           capture_output=True, text=True, timeout=300, cwd=str(goc))
        d = json.loads(r.stdout)
        cmds = d["registry"]["commands"]
    except Exception:
        return None
    w = {k for k, v in cmds.items() if v.get("read_only") is False}
    ws = {k for k, v in cmds.items()
          if v.get("read_only") is True and v.get("write_scope") not in (None, "none")}
    top = {x for x in w if " " not in x}
    lng = {x for x in w if " " in x}
    doc = {k for k, v in cmds.items() if v.get("read_only") is True}
    try:
        dem.write_text(json.dumps({"top": sorted(top), "long": sorted(lng),
                                   "ws": sorted(ws), "doc": sorted(doc)}), encoding="utf-8")
    except OSError:
        pass                                   # dem hong KHONG duoc lam hong phep do
    return (top, lng, ws, doc)


def _co_tu_help(lenh):
    """Tra tap co DAI+NGAN ma chuong trinh DA CAI phoi ra. None = khong do duoc (fail-close)."""
    try:
        r = subprocess.run(lenh, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    van = (r.stdout or "") + (r.returncode is not None and (r.stderr or "") or "")
    if not van.strip():
        return None
    return set(re.findall(r"(?<![\w-])(--?[A-Za-z0-9][\w-]*)", van))


def _kiem_bang(goc):
    """rc=0 hai bang con khop nguon that; rc khac 0 kem ly do tren stderr."""
    loi = []

    # (a) TANG 1 + 1b vs RUNTIME (khong phai regex — xem chu thich `_writer_tu_runtime`)
    rt = _writer_tu_runtime(goc)
    if rt is None:
        # FAIL-CLOSE. Mot cong tu tat khi thieu phep do la cong khong ton tai dung luc no
        # can nhat — va lan truoc chinh cho nay in "bang khop" tu mot phep do SAI TAP.
        loi.append("KHONG DO DUOC: khong hoi duoc `tl tool-inventory --json` — fail-close")
    else:
        top, lng, ws, doc = rt
        for nhan, that, bang in (("_TL_LENH_GHI", top, _TL_LENH_GHI),
                                 ("_TL_LENH_GHI_LONG", lng, _TL_LENH_GHI_LONG), ("_TL_LENH_DOC", doc, _TL_LENH_DOC)):
            thieu, thua = sorted(that - bang), sorted(bang - that)
            if thieu:
                loi.append("%s THIEU %d lenh read_only=%s: %s"
                           % (nhan, len(thieu), bang is _TL_LENH_DOC, " ".join(thieu)))
            if thua:
                loi.append("%s THUA %d ten khong con read_only=%s: %s"
                           % (nhan, len(thua), bang is _TL_LENH_DOC, " ".join(thua)))
        print("TANG 1 : %d writer top-level + %d writer LONG = %d (nguon: runtime)"
              % (len(top), len(lng), len(top) + len(lng)))
        print("TANG 1d: %d lenh DOC trong danh sach cho phep (nguon: runtime)" % len(doc))
        if ws and not _TL_CO_SINH_TEP:
            loi.append("_TL_CO_SINH_TEP RONG trong khi co %d lenh read_only=True co "
                       "write_scope != none" % len(ws))
        # Ban truoc CHI kiem ho co co RONG hay khong. Cross-review do duoc: doi ca ho co
        # thanh mot ten GIA van khong lam `t15` do — tuc cong khong he doi chieu NOI DUNG.
        # Nay doi chieu voi HELP THAT cua dung 8 lenh ma TANG 1b tuyen bo canh: moi ten
        # trong ho phai xuat hien o it nhat mot trong 8 lenh ay, va moi co sinh tep 8 lenh
        # ay phoi ra phai nam trong ho. Tam kiem = tam tuyen bo, khong rong hon.
        elif ws:
            phoi = set()
            for lenh in sorted(ws):
                h = _co_tu_help([sys.executable, "-B", str(pathlib.Path(goc, "scripts/tl.py")),
                                 *lenh.split(), "--help"])
                if h is None:
                    loi.append("KHONG DO DUOC `tl %s --help` — fail-close" % lenh)
                    continue
                phoi |= {c for c in h if c.startswith("--")
                         and ("out" in c or "output" in c)}
            mo_coi = sorted(_TL_CO_SINH_TEP - phoi)
            lot = sorted(phoi - _TL_CO_SINH_TEP)
            # CHIEU RUI RO — day la bang CAM, nguoc voi bang CHO PHEP o TANG 2, nen phan
            # quyet cung nguoc:
            #  · ten trong ho ma 8 lenh ay KHONG phoi ra  -> PHONG NGUA. Vo hai: no chan mot
            #    thu khong the xay ra o day (va co the CO that o 40 lenh khac — reviewer do
            #    duoc 45 lenh phoi `--out`). BAO, khong DO. Nhung phai goi dung ten no la
            #    PHONG NGUA chu khong phai phep do, kẻo lai thanh `_kiem_diff` lan hai.
            #  · co sinh tep 8 lenh ay PHOI RA ma KHONG nam trong ho -> LO THAT -> DO.
            if lot:
                loi.append("%d co sinh tep cua %d lenh TANG 1b KHONG nam trong ho bi chan: %s"
                           % (len(lot), len(ws), " ".join(lot)))
            print("TANG 1b: help THAT cua %d lenh phoi %d spelling; ho co %d ten, trong do "
                  "%d la PHONG NGUA (khong lenh nao trong %d lenh ay phoi ra): %s"
                  % (len(ws), len(phoi), len(_TL_CO_SINH_TEP), len(mo_coi), len(ws),
                     " ".join(mo_coi) or "-"))
        print("TANG 1b: %d lenh read_only=True nhung write_scope != none (chi ghi khi co %s)"
              % (len(ws), "/".join(sorted(_TL_CO_SINH_TEP))))

    # (a3) DANH SACH KICH BAN — moi tep o day phai TON TAI, kẻo lai canh mot cua khong co
    for k in sorted(_KICH_BAN_CHO_PHEP):
        if not pathlib.Path(goc, k).is_file():
            loi.append("_KICH_BAN_CHO_PHEP tro toi tep KHONG TON TAI: %s" % k)
    print("KICH BAN: %d tep trong danh sach cho phep (%s)"
          % (len(_KICH_BAN_CHO_PHEP), " ".join(sorted(_KICH_BAN_CHO_PHEP))))

    # (b) TANG 2 vs `--help` cua chuong trinh DA CAI
    #     git khai co theo TUNG subcommand (`git --help` chi phoi 4 co dai), nen hop cac
    #     `git <sub> -h` cua nhom doc. Do la ly do phai co nhanh rieng, khong phai ngoai le.
    do_duoc = khop = chua_xn = 0
    chua_theo_ct = []
    for ten, cho_phep in sorted(_CO_CHO_PHEP.items()):
        if not cho_phep:
            continue
        if ten == "ruff":
            co = _co_tu_help(["ruff", "check", "--help"])
        elif ten == "git":
            co = set()
            for sub in sorted(_GIT_LENH_DOC):
                mot = _co_tu_help(["git", sub, "-h"])
                if mot:
                    co |= mot
            co |= (_co_tu_help(["git", "-h"]) or set())
        else:
            co = _co_tu_help([ten, "--help"])
        if co is None:
            loi.append("KHONG DO DUOC `%s --help` — fail-close (mot cong tu tat khi thieu "
                       "cong cu la cong khong ton tai dung luc no can nhat)" % ten)
            continue
        do_duoc += 1
        xn = cho_phep & co
        chua = sorted(cho_phep - co)
        khop += len(xn)
        chua_xn += len(chua)
        if chua:
            chua_theo_ct.append("%s(%d): %s" % (ten, len(chua), " ".join(chua)))
    print("TANG 2: do duoc --help cua %d/%d chuong trinh co bang co khong rong"
          % (do_duoc, sum(1 for v in _CO_CHO_PHEP.values() if v)))
    print("TANG 2: %d co XAC NHAN co that · %d co KHONG DO DUOC" % (khop, chua_xn))
    for d in chua_theo_ct:
        print("  KHONG DO DUOC  " + d)
    # VI SAO "khong do duoc" o TANG 2 KHONG lam cong DO, trong khi o TANG 1 thi CO:
    # hai tang co CHIEU RUI RO NGUOC NHAU.
    #  · TANG 1 la bang CAM (lenh read_only=False). Thieu mot ten = lenh ghi ay duoc PHEP
    #    => lo an ninh. Phai chan.
    #  · TANG 2 la bang CHO PHEP. Mot ten co KHONG TON TAI nam trong bang thi chang mo ra
    #    gi ca — no chi cho phep mot thu khong the xay ra. Vo hai.
    # Va `--help` KHONG phai ban liet ke day du: do 2026-08-26, `git` khai co theo TUNG
    # subcommand nen 31 co that (`--oneline` `--porcelain` `--since`...) khong hien o
    # `git <sub> -h`; `find --help` terse nen thieu `-ipath` du GNU find CO. Bien mot phep
    # do KHONG DAY DU thanh cong DO la tu bao dong gia — nhung GIAU no di thi con te hon,
    # nen in ra tung ten.
    # Chi mot thu o TANG 2 lam cong DO: KHONG CHAY DUOC `--help`. Do la thieu PHEP DO, khac
    # han voi phep do khong day du.

    for x in loi:
        print("CHAN: " + x, file=sys.stderr)
    return 0 if not loi else 4


def main() -> int:
    if "--kiem-bang" in sys.argv[1:]:
        i = sys.argv.index("--kiem-bang")
        goc = sys.argv[i + 1] if len(sys.argv) > i + 1 else "."
        return _kiem_bang(goc)
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
