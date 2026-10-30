"""Phan chung cho packet #324 pha A1 — danh sach CHO PHEP cua agent read-only.

Chay: python .claude/hooks/pretooluse_guard_test.py
Thoat 0 khi VA CHI KHI moi ca DAT va moi dot bien BI GIET.

Doc truoc khi sua: mot ca xanh vi LY DO KHAC van la ca xanh. Nen moi tinh chat cua guard deu
co mot DOT BIEN rieng o duoi; bo mot dot bien la bo mot chot. Dot bien chay tren BAN SAO trong
thu muc tam (khong bao gio ghi vao tep that — bai hoc "dot bien ghi vao tep THAT roi khoi phuc
trong finally la bom hen gio"), moi ban sao mot TEN RIENG + chay bang `-B`, de tranh va cham
`.pyc` da tung tuoc rang moi mutant (CPython coi .pyc con hop le theo (mtime GIAY, kich thuoc)).
"""
import functools
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = pathlib.Path(__file__).resolve().parent
GUARD = HERE / "pretooluse_guard.py"
PACKET_BASE_SHA = "c03a409afc17ee3b8287cd1a88b0ed3f9ba02fab"


@functools.lru_cache(maxsize=1)
def _git_for_windows_usr_bin():
    if os.name != "nt":
        return None
    git = shutil.which("git")
    if not git:
        return None
    candidates = [pathlib.Path(git)]
    try:
        probe = subprocess.run([git, "--exec-path"], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=20)
        if probe.returncode == 0 and probe.stdout.strip():
            candidates.append(pathlib.Path(probe.stdout.strip()))
    except (OSError, subprocess.SubprocessError):
        pass
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except OSError:
            continue
        for root in (candidate, *candidate.parents):
            usr_bin = root / "usr" / "bin"
            if usr_bin.is_dir():
                return usr_bin
    return None


def _moi_truong_co_git(env=None):
    env = dict(os.environ if env is None else env)
    usr_bin = _git_for_windows_usr_bin()
    if usr_bin:
        env["PATH"] = str(usr_bin) + os.pathsep + env.get("PATH", "")
    return env


def moi_truong_do(env=None):
    """Measurement children use explicit UTF-8 and Git-for-Windows tools."""
    env = _moi_truong_co_git(env)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _la_cau_hinh_git_pham_vi_lenh(k):
    if k in ("GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"):
        return True
    return any(k.startswith(p) and k[len(p):].isdigit()
               for p in ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))


def _moi_truong_git_repo(env=None):
    """Bo cau hinh Git pham vi lenh roi bind dung checkout dang do."""
    env = moi_truong_do(env)
    for k in [k for k in env if _la_cau_hinh_git_pham_vi_lenh(k)]:
        del env[k]
    env.update({"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "safe.directory",
                "GIT_CONFIG_VALUE_0": str(HERE.parent.parent.resolve())})
    return env


def moi_truong_hook():
    """Decision child mirrors production's default Windows code page."""
    env = _moi_truong_co_git()
    env.pop("PYTHONUTF8", None)
    env.pop("PYTHONIOENCODING", None)
    return env


_RUFF_PROBED = {}


def _ruff_01515_that(env):
    path = shutil.which("ruff", path=env.get("PATH"))
    if not path:
        return None
    if path not in _RUFF_PROBED:
        try:
            probe = subprocess.run([path, "--version"], capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", env=env, timeout=20)
            ok = probe.returncode == 0 and probe.stdout.strip() == "ruff 0.15.15"
        except (OSError, subprocess.SubprocessError):
            ok = False
        _RUFF_PROBED[path] = path if ok else None
    return _RUFF_PROBED[path]


def _kiem_bang_that(g, goc, env=None):
    """Chạy guard với Ruff 0.15.15 thật; thiếu/sai bản thì fail-closed."""
    env = moi_truong_do() if env is None else env
    args = [sys.executable, "-B", str(g), "--kiem-bang", str(goc)]
    if _ruff_01515_that(env) is None:
        return subprocess.CompletedProcess(
            args, 4, "", "KHONG DO DUOC: can Ruff 0.15.15 that tren PATH\n")
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          env=env, timeout=400)


def _cong_cu_diff_that(env):
    if os.name == "nt":
        usr_bin = _git_for_windows_usr_bin()
        path = usr_bin / "diff.exe" if usr_bin else None
        if path is None or not path.is_file():
            found = shutil.which("diff", path=env.get("PATH"))
            path = pathlib.Path(found) if found else None
    else:
        found = shutil.which("diff", path=env.get("PATH"))
        path = pathlib.Path(found) if found else None
    if path is None or not path.is_file():
        return None
    try:
        probe = subprocess.run([str(path), "--version"], capture_output=True, text=True,
                               encoding="utf-8", env=env, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    van = (probe.stdout or "") + (probe.stderr or "")
    return path if probe.returncode == 0 and "diff" in van.lower() else None

# 8 hinh dang GHI — dung bang da do 2026-08-26 trong Issue #324, noi ca 8 DI LOT.
GHI = [
    ("sed -i tai cho", "sed -i 's/x/y/' scripts/tl.py"),
    ("chuyen huong >", 'echo "r" > scripts/tl.py'),
    ("chuyen huong >>", 'echo "r" >> scripts/tl.py'),
    ("tee", 'echo "r" | tee scripts/tl.py'),
    ("cp de len", "cp /tmp/x scripts/tl.py"),
    ("mv de len", "mv /tmp/x scripts/tl.py"),
    ("python -c ghi", "python -c \"open('scripts/tl.py','w').write('x')\""),
    ("truncate : >", ": > scripts/tl.py"),
]
# Lenh DOC hop le — CO ong, `;`, `$( )`, `2>/dev/null`. Day la ca chong tai dien #314:
# allowlist kieu tien to se chan oan sach nhung dong nay.
DOC = [
    "git log --oneline -1",
    "git status --porcelain | wc -l",
    "python scripts/tl.py cat-audit --json | head -40",
    'M=$(git rev-parse HEAD); echo "$M"',
    'rg -n "def main" .claude/dev | head -5',
    "git diff --numstat HEAD~1..HEAD -- docs/ 2>/dev/null | sort",
    "cat CLAUDE.md | grep -c python",
]
# Lenh GHI giau BEN TRONG thay the lenh. Vo lenh trong ra la vo hai (`echo THAYTHE`), nen
# chi bat duoc neu guard KIEM DE QUY phan trong. Dot bien m3 song o luot dau chinh vi
# bang GHI o tren khong co hinh dang nay — dot bien tim ra lo hong cua BO TEST, dung viec.
GHI_LONG = [
    ("ghi long trong $()", 'echo "$(cp /tmp/x scripts/tl.py)"'),
    ("ghi long trong backtick", 'echo "`sed -i s/a/b/ scripts/tl.py`"'),
    ("ghi long hai tang", 'echo "$(echo "$(mv /tmp/x scripts/tl.py)")"'),
    # Ba hinh dang duoi do duoc bang PHEP RA DOI NGHICH sau khi suite dau tien da xanh 8/8 —
    # tuc suite xanh KHONG chung minh khong con lo. Xuong dong: `shlex` whitespace_split nuot
    # newline nen hai lenh gop lam mot doan, chi chuong trinh DAU bi kiem.
    ("xuong dong tach lenh", "echo hi\ncp /tmp/x scripts/tl.py"),
    ("xuong dong + sed -i", "git log -1\nsed -i 's/a/b/' scripts/tl.py"),
    ("thay the tien trinh <()", "cat <(cp /tmp/x scripts/tl.py)"),
    # Ca nay chi LOT khi bo CA HAI chot (heredoc + tach xuong dong) — xem m10.
    ("ghi trong than heredoc", "python scripts/tl.py <<'E'\ncp /tmp/x scripts/tl.py\nE"),
]
# Ca do CROSS-REVIEW CODEX (PR #328) tim ra, DA TAI HIEN la ALLOW tren ban da day. Chung o
# day vi bo test truoc do xanh ma khong thay cai nao.
# KHONG GHI SO O DAY. Ban truoc viet "11 ca" roi mot ca bi BO (`diff --output=`, xem `t14`)
# ma cau ay o lai; cross-review luot 2 dem duoc 10. So dem la thu doi theo bang ngay ben
# duoi, nen no phai doc TU bang (`len(GHI_CHE_DO)`), khong phai chep vao chu thich.
GHI_CHE_DO = [
    ("chuyen huong &>", "echo x &> scripts/tl.py"),
    ("chuyen huong &>>", "echo x &>> scripts/tl.py"),
    ("chuyen huong doc-ghi <>", "cat <> scripts/tl.py"),
    ("sort -o", "sort -o scripts/tl.py CLAUDE.md"),
    ("uniq doi so ra", "uniq CLAUDE.md scripts/tl.py"),
    # ("diff --output=", ...) DA BO — xem t14. Co ay KHONG TON TAI tren
    # diffutils, nen ca cu xanh VI LY DO SAI (#336 muc 5).
    ("ruff format", "ruff format .claude/hooks/pretooluse_guard.py"),
    ("sed lenh w", "sed -n 'w scripts/tl.py' CLAUDE.md"),
    ("git branch tao ref", "git branch readonly-agent-wrote-this"),
    ("git tag tao ref", "git tag readonly-agent-wrote-this"),
    ("awk system co khoang trang", 'awk \'BEGIN { system ("touch scripts/written") }\''),
]
# Ca DUONG di kem — cross-review doi giu lai che do DOC cua dung nhung chuong trinh tren, kẻo
# ban va bien thanh chan oan. Khong co danh sach nay thi "deny N/N" khong noi len dieu gi.
DOC_CHE_DO = [
    "sort CLAUDE.md | head -3",
    "uniq CLAUDE.md | wc -l",
    "diff CLAUDE.md CONTEXT.md | head -5",
    "ruff check .claude/hooks/pretooluse_guard.py",
    "git branch --list",
    "git tag --list",
    "git branch",
    "git log --oneline -1 2>/dev/null",
]
DOI_CHUNG = [("rm -rf /x", "ask"), ("git push origin master --force", "ask")]
AGENT = ("tl-auditor", "tl-rasoat")


def hoi(guard, cmd, agent=None):
    d = {"tool_name": "Bash", "tool_input": {"command": cmd}}
    if agent:
        d["agent_type"] = agent
    p = subprocess.run([sys.executable, "-B", str(guard)], input=json.dumps(d),
                       capture_output=True, text=True, encoding="utf-8", env=moi_truong_hook())
    out = (p.stdout or "").strip()
    if not out:
        return "allow", ""
    o = json.loads(out)["hookSpecificOutput"]
    return o["permissionDecision"], o["permissionDecisionReason"]


def t1_agent_bi_chan_moi_hinh_dang_ghi(g):
    xau = [t for t, c in GHI if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"8 hinh dang ghi -> deny {8 - len(xau)}/8" + (f"; LOT: {xau}" if xau else ""))


def t2_ca_hai_agent_deu_bi_chan(g):
    xau = [(a, t) for a in AGENT for t, c in GHI if hoi(g, c, a)[0] != "deny"]
    return (not xau, f"2 agent x 8 ca -> deny {16 - len(xau)}/16" + (f"; LOT: {xau}" if xau else ""))


def t3_khong_chan_oan_lenh_doc(g):
    xau = [c for c in DOC if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"lenh doc hop le -> allow {len(DOC) - len(xau)}/{len(DOC)}"
                     + (f"; CHAN OAN: {xau}" if xau else ""))


def t4_phien_chinh_khop_packet_base(g):
    """Đối chiếu với parent/base được packet cấp quyền, không so HEAD với chính nó."""
    try:
        # Tu tiem mot command-scope config sai de ca nay CHUNG MINH lop loc co tac dung,
        # thay vi chi xanh khi runner tinh co khong mang cau hinh nao vao child.
        thu = dict(os.environ, GIT_CONFIG_COUNT="1",
                   GIT_CONFIG_KEY_0="safe.directory",
                   GIT_CONFIG_VALUE_0="C:/R12/khong-phai-checkout")
        cu = subprocess.run(["git", "show",
                             f"{PACKET_BASE_SHA}:.claude/hooks/pretooluse_guard.py"],
                            cwd=HERE.parent.parent, capture_output=True, text=True,
                            encoding="utf-8", env=_moi_truong_git_repo(thu),
                            check=True).stdout
    except Exception as e:
        return (False, f"KHONG DO DUOC blob base {PACKET_BASE_SHA[:12]} "
                       f"({type(e).__name__}) -> fail-close")
    if not cu.strip():
        return (False, "blob packet base rong -> fail-close")
    with tempfile.TemporaryDirectory() as d:
        nen = pathlib.Path(d) / "guard_packet_base.py"
        nen.write_text(cu, encoding="utf-8")
        moi_lenh = [c for _, c in GHI] + DOC + [c for c, _ in DOI_CHUNG]
        lech = [c for c in moi_lenh if hoi(g, c)[0] != hoi(nen, c)[0]]
        # Candidate-only control: mutate the candidate while keeping the authorized base fixed.
        if pathlib.Path(g).resolve() == GUARD:
            source = GUARD.read_text(encoding="utf-8")
            anchor = '(r"\\brm\\s+-rf\\b", "rm -rf"),'
            if source.count(anchor) != 1:
                lech.append("candidate-only control mat mo neo")
            else:
                candidate = source.replace(anchor, '(r"\\bNEVER_MATCH_RM\\b", "rm -rf"),', 1)
                compile(candidate, "<candidate-only-control>", "exec")
                mutant = pathlib.Path(d) / "guard_candidate_mutant.py"
                mutant.write_text(candidate, encoding="utf-8")
                if hoi(mutant, DOI_CHUNG[0][0])[0] == hoi(nen, DOI_CHUNG[0][0])[0]:
                    lech.append("candidate-only mutant song")
    return (not lech, f"phien chinh: {len(moi_lenh) - len(lech)}/{len(moi_lenh)} "
                      f"khop base {PACKET_BASE_SHA[:12]}"
                      + (f"; LECH: {lech}" if lech else ""))


def t5_doi_chung_van_ask(g):
    xau = [c for c, mong in DOI_CHUNG if hoi(g, c)[0] != mong]
    return (not xau, f"doi chung -> ask {len(DOI_CHUNG) - len(xau)}/{len(DOI_CHUNG)}"
                     + (f"; SAI: {xau}" if xau else ""))


def t6_agent_la_khong_bi_ap_luat(g):
    """`Explore` khong nam trong _AGENT_CHI_DOC => phai xu nhu phien chinh, khong chan."""
    xau = [c for _, c in GHI if hoi(g, c, "Explore")[0] == "deny"]
    return (not xau, f"agent ngoai danh sach: khong ap luat ({len(xau)} ca bi chan oan)")


def t8_ghi_giau_qua_tach_lenh_va_thay_the(g):
    xau = [t for t, c in GHI_LONG if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"ghi giau ($() · backtick · xuong dong · <()) -> deny {len(GHI_LONG) - len(xau)}/{len(GHI_LONG)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t9_che_do_ghi_cua_chuong_trinh_cho_phep(g):
    xau = [t for t, c in GHI_CHE_DO if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"che do GHI (10 ca cross-review) -> deny "
                     f"{len(GHI_CHE_DO) - len(xau)}/{len(GHI_CHE_DO)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t10_che_do_doc_cua_cung_chuong_trinh_khong_bi_chan(g):
    xau = [c for c in DOC_CHE_DO if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"che do DOC -> allow {len(DOC_CHE_DO) - len(xau)}/{len(DOC_CHE_DO)}"
                     + (f"; CHAN OAN: {xau}" if xau else ""))


def t7_nhom_mutate_tra_luat_bi_chan(g):
    ca = ["python scripts/tl.py corpus-audit --apply",
          "python scripts/tl.py reg-delete 123",
          "python scripts/tl.py golden-test --write"]
    xau = [c for c in ca if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"nhom mutate tra-luat -> deny {len(ca) - len(xau)}/{len(ca)}")


# ── #336: lo DO DUOC cua che do GHI, va phep do doi CA HAI dieu ─────────────────────────
# LOI KHAI DA THU HEP HAI LAN, ghi lai vi ca hai lan deu la toi noi RONG hon phep do:
#   luot 1: "NAM lo deu tai hien duoc" -> sai, chi 2 mode co CA HAI ve;
#   luot 2: van de lai chu "NAM lo" trong tieu de muc nay du bang chi con 2 phan tu.
# Bang la nguon; tieu de khong duoc mang so.
# Bai hoc sinh ra muc nay: ca `diff --output=` cu o `GHI_CHE_DO` XANH suot, ma no xanh VI LY
# DO SAI — `diff` KHONG CO co `--output` nao, nen lenh ay that bai voi `unrecognized option`
# va chang bao gio ghi gi. Cong "canh" mot cua khong ton tai, va bo test "chung minh" duoc
# dieu do. Nen tu day moi ca GHI phai chung minh HAI dieu:
#   (1) chay THAT trong thu muc tam => he tep DOI  (lo co that, khong phai ao)
#   (2) guard tra `deny`                            (cong bat duoc no)
# Thieu (1) thi (2) khong noi len gi. Do la khac biet giua PHEP DO va LOI KHAI.
GHI_336 = [
    # (ten, lenh mau — {T} thay bang duong dan tep dich trong thu muc tam)
    ("git diff --output= tao tep", "git diff --output={T} HEAD~1 HEAD"),
    ("ruff check --output-file=", "ruff check --output-file={T} --quiet ."),
]
# `tl recat` KHONG chay that duoc o day (no cham Drive/registry), nen no co ca RIENG o duoi
# do bang TANG 1 (ten lenh) chu khong bang phep do he tep — va ca ay noi ro nhu vay.

DOC_336 = [
    "git diff --numstat HEAD~1 HEAD",
    "git log --oneline -3",
    "git status --porcelain -uall",
    "git rev-parse --short HEAD",
    "ruff check --quiet .claude/hooks/pretooluse_guard.py",
    "diff -u CLAUDE.md CONTEXT.md | head -5",
    "ls -la .claude | head -3",
    "rg -n --glob '*.py' 'def main' .claude/dev | head -3",
]


def _chay_that(mau, thu_muc):
    """Chay lenh THAT trong thu muc tam; tra True neu tep dich XUAT HIEN (lo co that)."""
    dich = pathlib.Path(thu_muc) / "ra.txt"
    env = _moi_truong_git_repo()
    if mau.startswith("ruff ") and _ruff_01515_that(env) is None:
        return False
    # Hai template GHI_336 la argv don gian co chu y. Khong dua duong Windows qua bo
    # tach POSIX: thay placeholder sau khi tach bang khoang trang giu nguyen destination.
    argv = [x.replace("{T}", str(dich)) for x in mau.split()]
    try:
        subprocess.run(argv, cwd=str(HERE.parent.parent), capture_output=True,
                       text=True, encoding="utf-8", env=env, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return False
    return dich.exists() and dich.stat().st_size > 0


def t11_lo_336_co_that_VA_bi_chan(g):
    """A1 cua #336: doi CA HAI — lo chay that duoc, VA guard tu choi."""
    xau = []
    for ten, mau in GHI_336:
        with tempfile.TemporaryDirectory() as d:
            that = _chay_that(mau, d)
        quyet = hoi(g, mau.replace("{T}", "scripts/ra.txt"), "tl-auditor")[0]
        if not that:
            xau.append(f"{ten}: lo KHONG TAI HIEN DUOC (ca nay dang canh mot cua khong ton tai)")
        elif quyet != "deny":
            xau.append(f"{ten}: lo CO THAT nhung guard tra {quyet}")
    return (not xau, f"lo #336 chay-that-VA-bi-chan {len(GHI_336) - len(xau)}/{len(GHI_336)}"
                     + (f"; {xau}" if xau else ""))


def t12_tl_lenh_read_only_false_bi_chan(g):
    """Lo #336 muc 1: `recat` tran lot `_TL_CAM` vi no khong can CO nao de ghi."""
    ca = ["python scripts/tl.py recat x --cat 01",
          "python scripts/tl.py extract 123",
          "python scripts/tl.py corpus-audit --json",
          "python3 scripts/tl.py nlm-reconcile"]
    xau = [c for c in ca if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"lenh tl read_only=False -> deny {len(ca) - len(xau)}/{len(ca)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t13_khong_chan_oan_che_do_doc(g):
    xau = [c for c in DOC_336 if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"che do DOC cua cung chuong trinh -> allow "
                     f"{len(DOC_336) - len(xau)}/{len(DOC_336)}"
                     + (f"; CHAN OAN: {xau}" if xau else ""))


def t14_co_khong_ton_tai_phan_biet_duoc_voi_bi_chan(g):
    """A3 cua #336 — chinh lo muc 5. `diff --output` KHONG TON TAI: phai phan biet duoc
    "guard chan" voi "chuong trinh tu choi doi so". Ca nay do CA HAI phia."""
    quyet, ly = hoi(g, "diff --output=scripts/ra.txt CLAUDE.md CONTEXT.md", "tl-auditor")
    env = moi_truong_do()
    diff = _cong_cu_diff_that(env)
    if diff is None:
        return (False, "KHONG DO DUOC diff that (Windows chi nhan ban bundled da probe)")
    with tempfile.TemporaryDirectory() as d:
        dich = pathlib.Path(d) / "khong-bao-gio-tao"
        r = subprocess.run([str(diff), f"--output={dich}", "CLAUDE.md", "CONTEXT.md"],
                           cwd=str(HERE.parent.parent), capture_output=True, text=True,
                           encoding="utf-8", env=env)
        loi = ((r.stderr or "") + (r.stdout or "")).lower()
        khong_ton_tai = (r.returncode != 0 and "output" in loi and any(
            x in loi for x in ("unrecognized option", "unknown option", "invalid option", "illegal option")))
        tao_tep = dich.exists()
    ok = (quyet == "deny" and "danh sach cho phep" in ly and khong_ton_tai and not tao_tep)
    return (ok, f"co KHONG TON TAI: guard={quyet} · ly-do-la-allowlist="
                f"{'danh sach cho phep' in ly} · diff-tu-choi={khong_ton_tai} · "
                f"tao-tep={tao_tep} (mong doi deny/True/True/False)")


# t16_so_tran_chi_cho_chuong_trinh_do_duoc_la_nhan DA XOA: no KHOA dung LOI KHAI
# "-<so> chi head/tail/uniq/git nhan", ma cross-review DO DUOC rang GNU grep va GNU
# diff cung nhan `-3` (rc=0). Ca ay khong sai ky thuat — no dung, va no dung mot
# dieu SAI. `t26` la ban do LAI, hai chieu (6 nhan / 5 tu choi). Giu ca hai la giu
# mot ca doi CHAN OAN vinh vien.


def t17_co_sinh_tep_cua_tl_bi_chan_nhung_che_do_doc_thi_khong(g):
    """`read_only=True` KHONG co nghia la khong ghi: 8 lenh co `write_scope != none`, tuc
    "chi ghi khi nguoi goi tu khai --out". DO 2026-08-26: `tl sweep --out /tmp/x` -> ALLOW
    truoc khi co ho co nay, va `sweep` KHONG nam trong 90 ten cua TANG 1."""
    phai_chan = ["python scripts/tl.py sweep --out /tmp/x",
                 "python scripts/tl.py counts --output-file=/tmp/y",
                 "python scripts/tl.py review-queue --out-dir /tmp/z"]
    phai_qua = ["python scripts/tl.py sweep --json",
                "python scripts/tl.py doc-claims-check --strict --json",
                "python scripts/tl.py cat-audit --json | head -40"]
    xau = ["(khong chan) " + c for c in phai_chan if hoi(g, c, "tl-auditor")[0] != "deny"]
    xau += ["(chan oan) " + c for c in phai_qua if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"ho co sinh tep tl: chan {len(phai_chan)}/{len(phai_chan)} · "
                     f"qua {len(phai_qua)}/{len(phai_qua)}" + (f"; XAU: {xau}" if xau else ""))


def t20_TL_CAM_bat_cai_ma_hai_tang_kia_KHONG_bat(g):
    """Rang RIENG cho `_TL_CAM`. Khong co ca nay thi m7 SONG, va ta khong biet `_TL_CAM` con
    can hay da bi TANG 1 phu het. Ca duoi la lenh `read_only=True` (TANG 1 khong bat) va co
    khong thuoc ho sinh tep (TANG 1b khong bat) — chi `_TL_CAM` bat."""
    ca = ["python scripts/tl.py doc-claims-check --apply",
          "python scripts/tl.py cat-audit --confirm",
          "clasp push"]
    xau = [c for c in ca if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"chi _TL_CAM bat duoc -> deny {len(ca) - len(xau)}/{len(ca)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t18_co_ngan_GOP_mot_chu_xau_la_ca_cum_xau(g):
    """Rang cho `_RE_CO_NGAN_GOP`. Khong co ca nay thi dot bien m19 SONG — da do that:
    bo nhanh no cum khong lam ca nao do, tuc nhanh ay chua tung duoc canh."""
    phai_qua  = ["ls -la .claude", "ls -lh .claude", "git log -np 2>/dev/null"]
    phai_chan = ["ls -lQ .claude", "ls -laZ .claude", "cat -nQ CLAUDE.md"]
    xau  = ["(chan oan) " + c for c in phai_qua  if hoi(g, c, "tl-auditor")[0] != "allow"]
    xau += ["(khong chan) " + c for c in phai_chan if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"co ngan gop: qua {len(phai_qua)}/{len(phai_qua)} · "
                     f"chan {len(phai_chan)}/{len(phai_chan)}" + (f"; XAU: {xau}" if xau else ""))


def t19_kiem_bang_FAIL_CLOSE_khi_thieu_nguon(g):
    """Rang cho nhanh "KHONG DO DUOC" cua TANG 1. Mot cong tu tat khi thieu nguon la cong
    khong ton tai dung luc no can nhat. Dot bien m20 SONG truoc khi co ca nay."""
    with tempfile.TemporaryDirectory() as d:
        r = _kiem_bang_that(g, d)
    ok = r.returncode != 0 and "KHONG DO DUOC" in (r.stderr or "")
    return (ok, f"goc KHONG co command_registry.py -> rc={r.returncode} "
                f"(mong doi khac 0), co 'KHONG DO DUOC' tren stderr="
                f"{'KHONG DO DUOC' in (r.stderr or '')}")


def t15_cong_kiem_bang_khop_nguon_that(g):
    """A4 cua #336: bang TINH thi TROI; cong CI la thu duy nhat giu no khong troi."""
    r = _kiem_bang_that(g, HERE.parent.parent)
    ok = r.returncode == 0 and "TANG 1 :" in r.stdout and "TANG 2:" in r.stdout
    dong = [x for x in r.stdout.splitlines() if x.startswith("TANG")]
    return (ok, f"--kiem-bang rc={r.returncode} · " + " · ".join(dong[:3]))


# ── Luot 2: BA P1 cua cross-review codex tren PR #341 ────────────────────────────────────
# Ca ba deu DA TAI HIEN bang chinh guard truoc khi va (reviewer co y KHONG chay duong ghi
# — do la gioi han phan cong toi dat ra sau khi luot 1 chet vi bo loc noi dung).

# P1-a: `_RE_META` chi nhan entry viet thang `_m(...)`, bo qua `dict(_m(...))` va lenh LONG.
# Regex -> 90 writer; runtime -> 104. Nam ten duoi day deu ALLOW truoc ban va, va deu la
# duong STAGE/SET CREDENTIAL. Cong VAN in "bang khop" => CONG XANH GIA.
GHI_336B_CRED = [
    "python scripts/tl.py gws-auth-stage",
    "python scripts/tl.py nlm-auth-stage",
    "python scripts/tl.py secrets-stage khoa gia-tri",
    "python scripts/tl.py secrets-set khoa gia-tri",
    "python scripts/tl.py state-put khoa gia-tri",
]
# 7 lenh LONG (`tl <nhom> <lenh>`) — phai so HAI token, khong phai mot.
GHI_336B_LONG = [
    "python scripts/tl.py hygiene plan", "python scripts/tl.py hygiene reconcile",
    "python scripts/tl.py rasoat keywords", "python scripts/tl.py rasoat orchestrate",
    "python scripts/tl.py rasoat phuluc", "python scripts/tl.py rasoat titles",
    "python scripts/tl.py rasoat worksheet",
]
# P1-b: co GLOBAL an gia tri day ten lenh lui mot o => TANG 1 mu.
GHI_336B_GLOBAL = [
    "python scripts/tl.py --profile vbqppl recat x --cat 01",
    "python scripts/tl.py --config c.json recat x --cat 01",
    "python scripts/tl.py --profile=vbqppl recat x --cat 01",
    "python scripts/tl.py --deterministic recat x --cat 01",
    "python3 scripts/tl.py --profile vbqppl secrets-set k v",
]
# P1-c: vung kich ban theo THU MUC la danh sach CAM doi vai — no gia dinh moi tep `.py`
# duoi scripts/ .claude/dev/ ops/ khong ghi, va gia dinh ay SAI ngay trong cay nay.
GHI_336B_KICHBAN = [
    "python scripts/build_cache.py --input a --cache-dir /tmp/x --number-symbol s",
    "python .claude/dev/packet_loop.py init --packet 9 --mission 9",
    "python ops/lease_publish.py mark x --comment-id 1",
]
# Doi chung DUONG: lenh DOC cua CUNG nhung be mat tren phai van ALLOW.
DOC_336B = [
    "python scripts/tl.py cat-audit --json",
    "python scripts/tl.py --profile vbqppl cat-audit --json",
    "python scripts/tl.py --deterministic sweep --json",
    "grep -3 def /etc/hostname",
    "diff -3 /etc/hostname /etc/hostname",
]


def t28_writer_credential_bi_chan(g):
    xau = [c for c in GHI_336B_CRED if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"stage/set credential -> deny {len(GHI_336B_CRED)-len(xau)}"
                     f"/{len(GHI_336B_CRED)}" + (f"; LOT: {xau}" if xau else ""))


def t29_lenh_LONG_bi_chan(g):
    xau = [c for c in GHI_336B_LONG if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"lenh LONG -> deny {len(GHI_336B_LONG)-len(xau)}/{len(GHI_336B_LONG)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t41_co_GLOBAL_DON_khong_lam_lech_ten_lenh(h):
    """`co-global-don-timings-khong-co-rang` — `_TL_CO_GLOBAL_CO_DON` co bon ten ma chi ba
    co ca giu. Co don KHONG an gia tri, nen tieu nham mot token la day ten lenh di mot o —
    dung co che da lam TANG 1 mu o P1 `tl-global-option-lam-lech-ten-lenh`."""
    xau = []
    for co in ("--timings", "--deterministic", "--version", "--selftest"):
        if hoi(h, f"python scripts/tl.py {co} recat", "tl-auditor")[0] != "deny":
            xau.append(f"{co}: lenh GHI `recat` lot")
        if hoi(h, f"python scripts/tl.py {co} sweep", "tl-auditor")[0] != "allow":
            xau.append(f"{co}: lenh DOC `sweep` bi chan oan")
    return (not xau, f"co global don: {8 - len(xau)}/8" + (f"; SAI: {xau}" if xau else ""))


def t42_bo_dem_khoa_theo_BAM_khong_theo_THOI_GIAN(h):
    """`cache-hash-khong-co-mutant` — thuoc tinh nay tung chi duoc KHAI trong docstring.

    Ba chieu, va chieu thu hai moi la chieu dat: doi NOI DUNG phai doi khoa; doi rieng MTIME
    (dung `touch`) phai KHONG doi khoa — vi neu no doi thi dem gan nhu vo dung, con neu khoa
    dan tu mtime thi mot `touch` du de giu lai ban CU cua mot registry da troi.
    """
    import importlib.util, os, tempfile as _tf, time as _t
    sp = importlib.util.spec_from_file_location("g42", str(h))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    if not hasattr(m, "_duong_bo_dem"):
        return (False, "guard khong con `_duong_bo_dem` — moc phep do da chet")
    d = pathlib.Path(_tf.mkdtemp(prefix="tl336-dem-"))
    p = d / "command_registry.py"
    p.write_text("COMMAND_META = {}\n", encoding="utf-8")
    k1 = m._duong_bo_dem(p)
    os.utime(p, (0, 0))                      # doi RIENG mtime
    k2 = m._duong_bo_dem(p)
    p.write_text("COMMAND_META = {'x': 1}\n", encoding="utf-8")
    k3 = m._duong_bo_dem(p)
    xau = []
    if k1 != k2:
        xau.append("doi rieng mtime ma khoa doi -> dem gan nhu vo dung")
    if k1 == k3:
        xau.append("doi NOI DUNG ma khoa KHONG doi -> dem che duoc registry da troi")
    return (not xau, f"khoa bo dem: {2 - len(xau)}/2" + (f"; SAI: {xau}" if xau else ""))


def t43_hook_quyet_dinh_duoi_code_page_mac_dinh(g):
    env = moi_truong_hook()
    mac_dinh = all(k not in env for k in ("PYTHONUTF8", "PYTHONIOENCODING"))
    quyet = hoi(g, 'echo x > "scripts/đỏ.py"', "tl-auditor")[0]
    return (mac_dinh and quyet == "deny",
            f"decision child default-code-page={mac_dinh} · non-ASCII write={quyet}")


def t44_thieu_Ruff_01515_lam_cong_do(_g):
    with tempfile.TemporaryDirectory(prefix="tl336-no-ruff-") as d:
        env = moi_truong_do()
        env["PATH"] = d
        r = _kiem_bang_that(GUARD, HERE.parent.parent, env)
    ok = r.returncode != 0 and "Ruff 0.15.15" in (r.stderr or "")
    return (ok, f"PATH khong Ruff -> rc={r.returncode} · fail-closed={ok}")


def t30_co_global_khong_lam_lech_ten_lenh(g):
    xau = [c for c in GHI_336B_GLOBAL if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"co global + writer -> deny {len(GHI_336B_GLOBAL)-len(xau)}"
                     f"/{len(GHI_336B_GLOBAL)}" + (f"; LOT: {xau}" if xau else ""))


def t31_kich_ban_ngoai_danh_sach_bi_chan(g):
    xau = [c for c in GHI_336B_KICHBAN if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"kich ban ngoai danh sach -> deny {len(GHI_336B_KICHBAN)-len(xau)}"
                     f"/{len(GHI_336B_KICHBAN)}" + (f"; LOT: {xau}" if xau else ""))


def t32_khong_chan_oan_be_mat_vua_siet(g):
    xau = [c for c in DOC_336B if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"doc hop le -> allow {len(DOC_336B)-len(xau)}/{len(DOC_336B)}"
                     + (f"; CHAN OAN: {xau}" if xau else ""))


def t33_cong_hoi_RUNTIME_chu_khong_parse_van_ban(g):
    """P1-a o goc: cong cu doc `COMMAND_META` bang regex nen do SAI TAP roi in "bang khop".
    Ca nay doi cong noi ro no dem duoc BAO NHIEU va tu dau — 106, tu runtime (WP1009 +agent-creds-set, WP1038 +agent-creds-exec)."""
    r = _kiem_bang_that(g or GUARD, HERE.parent.parent)
    dong = next((x for x in r.stdout.splitlines() if x.startswith("TANG 1 :")), "")
    ok = (r.returncode == 0 and "nguon: runtime" in dong and "= 106" in dong)
    return (ok, f"rc={r.returncode} · {dong or '(khong co dong TANG 1)'}")


def t34_so_tran_chi_cho_chuong_trinh_DO_DUOC_la_nhan(g):
    """DO tung chuong trinh, khong doan. Ban truoc co BON ten nen `grep -3`/`diff -3` bi
    CHAN OAN — cross-review bat duoc. Ca nay do CA HAI chieu."""
    nhan = ["head -3 /etc/hostname", "tail -3 /etc/hostname", "uniq -3 /etc/hostname",
            "git log -3 --oneline", "grep -3 x /etc/hostname",
            "diff -3 /etc/hostname /etc/hostname"]
    tu_choi = ["sort -3 /etc/hostname", "ls -3", "rg -3 x", "cat -3 /etc/hostname",
               "nl -3 /etc/hostname"]
    xau = [c for c in nhan if hoi(g, c, "tl-auditor")[0] != "allow"]
    xau += [c for c in tu_choi if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"-<so>: 6 nhan / 5 tu choi -> dung {11-len(xau)}/11"
                     + (f"; SAI: {xau}" if xau else ""))


# P2 `so-tran-va-co-ngan-gan-gia-tri-chan-oan`: `_RE_CO_NGAN_GOP` hieu MOI token chu-so
# ngan la BO co, nen `-n3` bi doc thanh bo `-n`+`-3` roi tu choi. Cross-review do duoc
# MUOI ca chan oan, gom `git log -n1` va `git diff -U3` — hai lenh doc thuong nhat cua kho.
# Moi dong duoi day DA DO: chuong trinh that tra rc=0.
DOC_CO_NGAN_GAN = [
    "head -n3 CLAUDE.md", "tail -n3 CLAUDE.md", "uniq -w3 CLAUDE.md",
    "git log -n1 --oneline", "grep -m1 x CLAUDE.md", "rg -m1 x CLAUDE.md",
    "sort -k1 CLAUDE.md", "cut -f1 CLAUDE.md", "nl -w3 CLAUDE.md",
    "git diff -U3 HEAD~1 HEAD",
]


def t35_co_ngan_an_gia_tri_gan_lien_khong_bi_chan_oan(h):
    xau = [c for c in DOC_CO_NGAN_GAN if hoi(h, c, "tl-auditor")[0] != "allow"]
    # Doi chung NGUOC: bo co that va co la van phai deny, keo ban va thanh noi bua.
    cam = ["sort -o F A", "ruff check --output-file=F .", "cat -xyz F", "uniq A B"]
    xau += [c for c in cam if hoi(h, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"co ngan gan gia tri: 10 allow / 4 deny -> dung {14-len(xau)}/14"
                     + (f"; SAI: {xau}" if xau else ""))


def t37_duong_dan_kich_ban_KHONG_CO_LOI_THOAT(h):
    """P1 `python-allowlist-lstrip-khong-phai-exact-path` (cross-review luot 2).

    `str.lstrip` bo MOI ky tu trong tap chu khong phai mot TIEN TO, nen `../../scripts/tl.py`
    co ve dung `scripts/tl.py`. Danh sach cho phep dung; PHEP SO thi sai — va mot phep chuan
    hoa long hon phep so lam danh sach cho phep vo hieu.
    DO DUOC (A/B tren `9583293` va head): 4 dang thoat cay tu ALLOW -> deny, duong hop le
    giu nguyen ALLOW.
    """
    thoat = ["python ../../scripts/tl.py sweep",
             "python ../scripts/tl.py sweep",
             "python .././scripts/tl.py sweep",
             "python ../../scripts/tl.py --profile x sweep"]
    hop_le = ["python scripts/tl.py sweep", "python ./scripts/tl.py sweep"]
    xau = [c for c in thoat if hoi(h, c, "tl-auditor")[0] != "deny"]
    xau += [c for c in hop_le if hoi(h, c, "tl-auditor")[0] != "allow"]
    n = len(thoat) + len(hop_le)
    return (not xau, f"duong dan kich ban: {n - len(xau)}/{n}"
                     + (f"; SAI: {xau}" if xau else ""))


def t38_git_c_chi_nhan_khoa_DA_DO(h):
    """P1 `git-read-subcommand-van-goi-duoc-helper-ngoai`, mat thu nhat.

    `-c` nam trong bang co cho phep, ma TANG 2 chi soi TEN CO chu khong soi GIA TRI, nen
    `git -c core.pager=<lenh> log` la mot subcommand DOC goi chuong trinh NGOAI. Tap khoa
    nguy hiem khong liet het duoc (`core.editor` `diff.external` `core.hooksPath`
    `credential.helper` `alias.*` `core.sshCommand` …), nen DAO sang danh sach CHO PHEP.
    """
    cam = ["git -c core.pager=touch log --oneline",
           "git -c core.hooksPath=/x status",
           "git -c credential.helper=touch log",
           "git -c diff.external=touch diff HEAD~1 HEAD"]
    tha = ["git -c core.abbrev=7 log --oneline", "git log --oneline"]
    xau = [c for c in cam if hoi(h, c, "tl-auditor")[0] != "deny"]
    xau += [c for c in tha if hoi(h, c, "tl-auditor")[0] != "allow"]
    n = len(cam) + len(tha)
    return (not xau, f"git -c theo khoa: {n - len(xau)}/{n}" + (f"; SAI: {xau}" if xau else ""))


def t39_gan_bien_TIEN_TO_bi_chan_gan_bien_THUAN_thi_KHONG(h):
    """P1 tren, mat thu hai — VA chieu tha, vi ban dau toi lam do chinh `t3`.

    `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.pager ... git log` dat dung thu ma `-c` vua bi
    chan, chi bang duong khac. Nhung ap danh sach cho phep cho MOI phep gan la CHAN OAN:
    `M=$(git rev-parse HEAD)` chi doi bien CUA SHELL. Phan biet o TIEN TO: gan lam tien to
    cho mot lenh thi no vao moi truong cua tien trinh se chay.
    """
    cam = ["GIT_PAGER=touch git log", "GIT_CONFIG_COUNT=1 git log",
           "LD_PRELOAD=/x.so git log", "GIT_EXTERNAL_DIFF=touch git diff"]
    tha = ['M=$(git rev-parse HEAD); echo "$M"', "LC_ALL=C git log --oneline",
           "PYTHONDONTWRITEBYTECODE=1 python scripts/tl.py sweep"]
    xau = [c for c in cam if hoi(h, c, "tl-auditor")[0] != "deny"]
    xau += [c for c in tha if hoi(h, c, "tl-auditor")[0] != "allow"]
    n = len(cam) + len(tha)
    return (not xau, f"gan bien tien to: {n - len(xau)}/{n}" + (f"; SAI: {xau}" if xau else ""))


def t40_co_ngan_gia_tri_PHI_SO_khong_bi_chan_oan(h):
    """P2 `co-ngan-gia-tri-phi-so-van-bi-chan-oan` — luot 2 SIET QUA TAY.

    Ban luot 2 doi `goc[2:].isdigit()`, nen gia tri khong phai so cung roi xuong nhanh bo co
    va bi DENY oan. Dieu kien an toan khong nam o HINH DANG gia tri ma o CHU DAU: no phai la
    co CO TRONG bang VA la co AN GIA TRI.
    """
    tha = ["cut -d, -f1 a.csv", "grep -ePAT a.txt", "rg -epat a.txt", "sort -k1,1 a.txt"]
    cam = ["cat -xyz F", "sort -o F A"]           # chu dau KHONG an gia tri / la co GHI
    xau = [c for c in tha if hoi(h, c, "tl-auditor")[0] != "allow"]
    xau += [c for c in cam if hoi(h, c, "tl-auditor")[0] != "deny"]
    n = len(tha) + len(cam)
    return (not xau, f"co ngan gia tri phi so: {n - len(xau)}/{n}"
                     + (f"; SAI: {xau}" if xau else ""))


def t36_moi_ca_DINH_NGHIA_deu_phai_DANG_KY(h):
    """Ca CO MAT khac ca CO DO. Da tra gia trong chinh packet nay: bay ca cua luot 2 duoc
    viet xong nhung moc `replace` tro sai dong nen KHONG cai nao vao `CA`. Bo test bao
    "DAT" trong khi khong do gi phan moi, va no chi lo ra vi mot dot bien SONG.

    Phep kiem nay doc CHINH tep nguon, khong doc `CA` da nap — mot ca bi bo quen thi no
    van nam trong van ban."""
    van = pathlib.Path(__file__).read_text(encoding="utf-8")
    dinh = set(re.findall(r"^def (t\w+)\(", van, re.M))
    # Neo theo DAU DONG: chuoi "CA = [" cung xuat hien trong chinh docstring nay, va ban
    # dau `index` khop vao do => dang_ky = 0 => ca bao DO voi ca 28 ten. Mot phep do bat
    # duoc loi that cua nguoi khac van co the sai o chinh no.
    i = re.search(r"^CA = \[", van, re.M).start()
    dang_ky = set(re.findall(r"\b(t\w+)\b", van[i:van.index("]", i)]))
    bo_quen = sorted(dinh - dang_ky)
    ma = sorted(x for x in dang_ky - dinh if x.startswith("t") and "_" in x)
    return (not bo_quen and not ma,
            f"dinh nghia {len(dinh)} · dang ky {len(dinh) - len(bo_quen)}"
            + (f"; BO QUEN: {bo_quen}" if bo_quen else "")
            + (f"; DANG KY MA KHONG CO: {ma}" if ma else ""))


# ── NEN: Windows KHONG chay vong lap dot bien ─────────────────────────────────────────
# DO 06-09-2026 tren Linux: bo nay 346s, trong do NEN-ONLY 10s => dot bien = 336s = 97%
# chi phi cua bo, ~68% chi phi ca buoc `test registry`. Tren windows-latest ca buoc ay
# ton 44,3 phut va job `gate` bi CAT o tran 60 phut (`cancelled`) hai luot master lien
# tiep — tuc chan Windows CHUA BAO GIO chay tron. Cat vong lap dot bien khoi Windows la
# cat dung khoan ay; ca NEN van chay du, khong bo ca nao.
#
# Ba ham duoi day la HAM THUAN, cung ly do voi `giet_duoc`/`duoc_cong_bo_diem` ben duoi:
# phan chung phai ep duoc CA HAI nhanh nen ma KHONG can may Windows that.
def nen_bo_qua_dot_bien(ten_nen=None):
    """Nen `nt` (Windows) thi KHONG chay vong lap dot bien. Vi tu THUAN de do duoc."""
    return (os.name if ten_nen is None else ten_nen) == "nt"


def dat_windows(so_ca, do, so_dot_bien):
    """Tieu chi DAT cua nhanh Windows — DOI SO DUONG hai ve, y het nhanh Linux.

    `so_dot_bien > 0` la CHOT TUONG DUONG cua `len(DOT_BIEN) > 0` o nhanh Linux, KHONG
    duoc bo. Bai hoc #319 la "tap RONG thoa `not song`": neu bang dot bien rong thi bo
    test da mat chinh thu no dang khai la "se do o cho khac", nen loi hua ay thanh loi
    hua suong — phai DO, du o day khong chay dot bien nao.
    """
    return so_ca > 0 and do == 0 and so_dot_bien > 0


def dong_windows(so_ca_dat, so_ca, so_dot_bien):
    """Dong bang chung DUONG cua Windows: khai RO dot bien khong do o day, va do O DAU.

    KHONG duoc mang chu `bi giet` — o day khong giet cai nao. Dong `DOT BIEN 0/0 bi giet`
    chinh la hinh dang ma #319 sinh ra de chan, nen no phai TRUOT o so dang ky.
    """
    return (f"TONG: CA {so_ca_dat}/{so_ca} dat · "
            f"DOT BIEN {so_dot_bien} muc KHONG DO TREN WINDOWS — do tren ubuntu-latest")


def t45_windows_bang_dot_bien_RONG_thi_KHONG_dat(g):
    """Chot TUONG DUONG `len(DOT_BIEN) > 0` cho nhanh Windows (bai hoc #319)."""
    return (not dat_windows(36, 0, 0) and not dat_windows(0, 0, 34)
            and not dat_windows(36, 1, 34) and dat_windows(36, 0, 34),
            "Windows: bang dot bien RONG / khong ca / co ca DO -> KHONG dat")


def t46_dong_windows_KHONG_gia_dang_dong_linux(g):
    """Dong Windows khong duoc doi lot dong Linux — no chua do gi de ma 'giet'."""
    d = dong_windows(36, 36, 34)
    return ("bi giet" not in d and "KHONG DO TREN WINDOWS" in d and "ubuntu-latest" in d,
            "Windows: dong bang chung khai dung noi dot bien duoc do")


def t47_vi_tu_nen_chi_cat_dot_bien_tren_nt(g):
    """Cat dot bien la hanh vi RIENG cua Windows; nen khac phai chay du."""
    return (nen_bo_qua_dot_bien("nt") and not nen_bo_qua_dot_bien("posix")
            and not nen_bo_qua_dot_bien("java"),
            "vi tu nen: chi 'nt' moi cat vong lap dot bien")



# ── CHE DO NHE (#647): CI bo vong lap dot bien khi diff KHONG cham vung ─────────────────
# Do run 36238709647: bo nay 756,50 s tren gate-registry, ca nen chi 10,2 s. `ci_dang_ky_test.py`
# dat co duoi day khi diff khong cham `pretooluse_guard.py`/bo nay/vung chung (luat #643), va
# GO co khi cham — nen dot bien van do dung luot can do. Ca NEN chay du moi luot.
CO_NHE = "PRETOOLUSE_GUARD_KHONG_DOT_BIEN"


def che_do_chay(ten_nen=None, env=None):
    """`windows` | `nhe` | `du`. Windows DUNG TRUOC va khong doi; co nhe chi nhan dung "1"."""
    if nen_bo_qua_dot_bien(ten_nen):
        return "windows"
    return "nhe" if (os.environ if env is None else env).get(CO_NHE) == "1" else "du"


def dong_nhe(so_ca_dat, so_ca, so_dot_bien):
    """Dong bang chung che do nhe. KHONG mang chu `bi giet` — o day khong giet cai nao, nen
    dong nay PHAI truot mau che do du (`MAU_DAY_DU`) cua so dang ky."""
    return (f"TONG: CA {so_ca_dat}/{so_ca} dat · "
            f"DOT BIEN {so_dot_bien} muc CHE DO NHE — do khi diff cham vung")


def t48_che_do_nhe_chi_khi_co_DUNG_1_va_windows_dung_truoc(g):
    """Co rong/"0"/"true" KHONG duoc bat nhe; Windows giu nhanh cu du co dat co."""
    ok = (che_do_chay("posix", {CO_NHE: "1"}) == "nhe" and che_do_chay("posix", {}) == "du"
          and all(che_do_chay("posix", {CO_NHE: v}) == "du" for v in ("", "0", "true", " 1"))
          and che_do_chay("nt", {CO_NHE: "1"}) == "windows" and che_do_chay("nt", {}) == "windows")
    return ok, "vi tu che do: nhe chi khi co == '1' tren nen khac nt"


def t49_dong_nhe_KHONG_gia_dang_dong_du_va_bang_rong_thi_DO(g):
    """Dong nhe khong doi lot dong Linux; tieu chi dat van doi so DUONG hai ve (#319)."""
    d = dong_nhe(39, 39, 34)
    return ("bi giet" not in d and "CHE DO NHE" in d and "KHONG DO TREN WINDOWS" not in d
            and not dat_windows(39, 0, 0) and not dat_windows(39, 1, 34),
            "che do nhe: dong bang chung rieng, bang dot bien rong -> DO")

def t50_duong_dan_tl_py_DAU_PHAN_CACH_nao_cung_bi_chan(g):
    """WP1009 F14 (cross-review luot 5): `"scripts\\tl.py"` qua allowlist (da chuan hoa) nhung nhanh
    chan writer lai so tren token GOC theo dau `/` => lot. Moi cach viet CUNG MOT kich ban, moi agent:
    lenh ghi (moi + cu) phai deny; lenh doc `secrets-keygen` van allow."""
    bs = chr(92)
    duong = ("scripts/tl.py", "./scripts/tl.py", "scripts" + bs + "tl.py", "." + bs + "scripts" + bs + "tl.py")
    xau = []
    for a in AGENT:
        for d in duong:
            for lenh, mong in (("agent-creds-set --new", "deny"), ("agent-creds-exec --claude -- x", "deny"),
                               ("secrets-set --gws", "deny"), ("secrets-keygen", "allow")):
                c = 'python "%s" %s' % (d, lenh)
                if hoi(g, c, a)[0] != mong:
                    xau.append("%s: %s" % (a, c))
    return (not xau, "2 agent x 4 cach viet x 4 lenh -> dung %d/32" % (32 - len(xau))
                     + ("; SAI: %s" % xau if xau else ""))


def t51_ten_lenh_tl_qua_mo_rong_shell_bi_chan(g):
    """WP1038 F03 (cross-review luot 3): Bash mo rong `$'..'`/`${..}`/`$( )`/backtick/brace/glob thanh ten lenh THAT,
    shlex thi khong — nen moi cach viet ay phai deny o CA HAI agent; con `$` la DU LIEU sau ten lenh, ten trich dan
    nguyen van va gia tri co global binh thuong van allow (khong chan oan)."""
    dl = chr(36)
    tu_choi = ["%s'agent-creds-exec' --claude -- x" % dl, "%s{X:-agent-creds-exec} --claude -- x" % dl,
               "agent-creds-%s'exec' --claude -- x" % dl, "agent-creds-%s(printf exec) --claude -- x" % dl,
               "agent-creds-`printf exec` --claude -- x", "--profile %sP recat x" % dl, "agent-creds-{exec,} --claude",
               "agent-creds-exe? --claude -- x", "hygiene %s'plan'" % dl]
    cho_phep = ["profile-list", "--profile vbqppl locate 'Luat dat dai 2024' --json", "\"profile-list\"",
                "locate \"%sX\"" % dl, "locate %s(echo a)" % dl]
    xau = []
    for a in AGENT:
        for c in tu_choi:
            if hoi(g, "python scripts/tl.py " + c, a)[0] != "deny":
                xau.append("LOT %s: %s" % (a, c))
        for c in cho_phep:
            if hoi(g, "python scripts/tl.py " + c, a)[0] != "allow":
                xau.append("CHAN OAN %s: %s" % (a, c))
    tong = len(AGENT) * (len(tu_choi) + len(cho_phep))
    return (not xau, "mo rong shell o vung ten lenh tl -> dung %d/%d" % (tong - len(xau), tong)
                     + ("; %s" % xau if xau else ""))


CA = [t1_agent_bi_chan_moi_hinh_dang_ghi, t2_ca_hai_agent_deu_bi_chan,
      t3_khong_chan_oan_lenh_doc, t4_phien_chinh_khop_packet_base,
      t5_doi_chung_van_ask, t6_agent_la_khong_bi_ap_luat,
      t7_nhom_mutate_tra_luat_bi_chan, t8_ghi_giau_qua_tach_lenh_va_thay_the,
      t9_che_do_ghi_cua_chuong_trinh_cho_phep,
      t10_che_do_doc_cua_cung_chuong_trinh_khong_bi_chan,
      t11_lo_336_co_that_VA_bi_chan, t12_tl_lenh_read_only_false_bi_chan,
      t13_khong_chan_oan_che_do_doc,
      t14_co_khong_ton_tai_phan_biet_duoc_voi_bi_chan,
      t15_cong_kiem_bang_khop_nguon_that,
      t17_co_sinh_tep_cua_tl_bi_chan_nhung_che_do_doc_thi_khong,
      t18_co_ngan_GOP_mot_chu_xau_la_ca_cum_xau,
      t19_kiem_bang_FAIL_CLOSE_khi_thieu_nguon,
      t20_TL_CAM_bat_cai_ma_hai_tang_kia_KHONG_bat,
      # --- luot 2: BA P1 + HAI P2 cua cross-review codex tren PR #341 ---
      t28_writer_credential_bi_chan, t29_lenh_LONG_bi_chan,
      t30_co_global_khong_lam_lech_ten_lenh,
      t31_kich_ban_ngoai_danh_sach_bi_chan,
      t32_khong_chan_oan_be_mat_vua_siet,
      t33_cong_hoi_RUNTIME_chu_khong_parse_van_ban,
      t34_so_tran_chi_cho_chuong_trinh_DO_DUOC_la_nhan,
      t35_co_ngan_an_gia_tri_gan_lien_khong_bi_chan_oan,
      t37_duong_dan_kich_ban_KHONG_CO_LOI_THOAT, t38_git_c_chi_nhan_khoa_DA_DO,
      t39_gan_bien_TIEN_TO_bi_chan_gan_bien_THUAN_thi_KHONG,
      t40_co_ngan_gia_tri_PHI_SO_khong_bi_chan_oan,
      t41_co_GLOBAL_DON_khong_lam_lech_ten_lenh,
      t42_bo_dem_khoa_theo_BAM_khong_theo_THOI_GIAN,
      t43_hook_quyet_dinh_duoi_code_page_mac_dinh,
      t44_thieu_Ruff_01515_lam_cong_do,
      t45_windows_bang_dot_bien_RONG_thi_KHONG_dat,
      t46_dong_windows_KHONG_gia_dang_dong_linux,
      t47_vi_tu_nen_chi_cat_dot_bien_tren_nt,
      t48_che_do_nhe_chi_khi_co_DUNG_1_va_windows_dung_truoc,
      t49_dong_nhe_KHONG_gia_dang_dong_du_va_bang_rong_thi_DO,
      t50_duong_dan_tl_py_DAU_PHAN_CACH_nao_cung_bi_chan,
      t51_ten_lenh_tl_qua_mo_rong_shell_bi_chan,
      t36_moi_ca_DINH_NGHIA_deu_phai_DANG_KY]

# --- DOT BIEN: moi cai go DUNG MOT tinh chat, va phai lam it nhat mot ca DO ---
DOT_BIEN = [
    # m1/m5 phai noi CA HAI bang. Noi mot bang thi bang KIA van chan, va dot bien don le
    # SONG — do duoc: `_kiem_co` fail-close voi chuong trinh khong co trong `_CO_CHO_PHEP`,
    # nen them `sed` vao danh sach chuong trinh KHONG du de mo duong. Do la phong thu nhieu
    # lop CHAY THAT, nhung mot dot bien chi go mot lop thi khong do duoc lop nao.
    ("m1_cho_sed_awk_vao_CA HAI bang",
     ('"git", "python", "python3", "py", "find",', '    "egrep":     frozenset(),'),
     ('"sed", "awk", "git", "python", "python3", "py", "find",',
      '    "sed": frozenset({"-i", "-n", "-e"}), "awk": frozenset({"-F", "-v"}),\n    "egrep":     frozenset(),')),
    ("m2_bo_chot_chuyen_huong", 'if ">" in t:', 'if False:'),
    ("m3_bo_de_quy_thay_the", "ly = _kiem_lenh_agent(t, sau + 1)", "ly = None"),
    ("m4_bo_kiem_python", '"python": _kiem_python, ', ""),
    ("m5_cho_tee_vao_CA HAI bang",
     ('"rg", "grep",', '    "egrep":     frozenset(),'),
     ('"tee", "cp", "mv", "rg", "grep",',
      '    "tee": frozenset({"-a"}), "cp": frozenset(), "mv": frozenset(),\n    "egrep":     frozenset(),')),
    ("m6_rong_danh_sach_agent", '_AGENT_CHI_DOC = frozenset({"tl-auditor", "tl-rasoat"})',
     "_AGENT_CHI_DOC = frozenset()"),
    ("m7_bo_chot_tl_mutate", "if _TL_CAM.search(cmd):", "if False:"),
    ("m8_bo_tach_xuong_dong", 'if "\\n" in cmd:', "if False:"),
    ("m9_bo_thay_the_tien_trinh", 'if cmd[i:i + 2] in ("$(", "<("):', 'if cmd[i:i + 2] == "$(":'),
    # GHEP hai chot: rieng le thi cai nay che cai kia nen dot bien don le SONG — khong phai vi
    # test yeu ma vi hai lop doc lap cung chan mot ca. Doctrine: "phai dot bien ghep ca bon".
    # m12_bo_kiem_sort DA BO cung luc voi `_kiem_sort`: TANG 2 phu no, nen dot bien ay
    # SONG (do duoc). Dot bien cho mot chot khong con ton tai la dot bien chua tung chay.
    ("m13_bo_kiem_uniq", '"uniq": _kiem_uniq,', ""),
    ("m14_bo_chot_vi_tri_git_ref",
     'if [a for a in con if not a.startswith("-")] and not any(', "if False and any("),
    # --- #336: moi chot moi mot dot bien RIENG; chot khong co dot bien la chot se ho lai ---
    ("m15_bo_tang2_kiem_co", "    ly = _kiem_co(ten, doi)", "    ly = None"),
    # Moc cu (`if len(vt) > 1 and vt[1] in _TL_LENH_GHI:`) da bien mat khi va P1-b — luot
    # chay bao "MOC KHONG CON TRONG MA -> dot bien chua tung chay", dung nhu no phai bao.
    ("m16_bo_tang1_lenh_tl_ghi",
     'if lenh and (lenh[0] in _TL_LENH_GHI', 'if False and (lenh[0] in _TL_LENH_GHI'),
    # m17 BAN DAU la dot bien RONG: `frozenset({} or {...})` -> `{} or {...}` cho ra chinh
    # tap cu, nen no khong doi gi va "SONG" ma khong noi len dieu gi. Nay lam RONG that su
    # bang cach gan ten khac cho phan than.
    ("m17_rong_bang_lenh_ghi", "_TL_LENH_GHI = frozenset({",
     "_TL_LENH_GHI = frozenset()\n_TL_LENH_GHI_CU = frozenset({"),
    ("m18_noi_bang_co_git_cho_output", '"-uall", "-uno"}),',
     '"-uall", "-uno", "--output", "--output-file"}),'),
    ("m23_rong_ho_co_sinh_tep", '_TL_CO_SINH_TEP = frozenset({"--out",',
     '_TL_CO_SINH_TEP = frozenset({"--khong-bao-gio-co",'),
    ("m24_bo_mien_tang2_cho_python", '    if ten in _MIEN_TANG2:',
     "    if False:"),
    ("m21_noi_so_tran_cho_moi_chuong_trinh",
     'if _RE_SO_TRAN.match(goc) and ten in _CHO_SO_TRAN:',
     "if _RE_SO_TRAN.match(goc):"),
    ("m22_bo_luat_so_tran", 'if _RE_SO_TRAN.match(goc) and ten in _CHO_SO_TRAN:',
     "if False:"),
    ("m19_no_cum_cho_qua_tat_ca",
     '            xau = [c for c in ("-" + ch for ch in goc[1:]) if c not in cho_phep]',
     "            xau = []"),
    # m20_tang1_fail_open_khi_thieu_meta DA GO: no dot bien duong `loi.append("KHONG DO
    # DUOC: thieu <meta>")` cua ban PARSE VAN BAN, ma duong ay khong con — cong nay hoi
    # RUNTIME. `m26_cong_fail_OPEN_khi_khong_hoi_duoc_runtime` la ban KE NHIEM, dot bien
    # dung tinh chat ay tren duong moi. Giu m20 chi de no bao "MOC KHONG CON" moi luot.
    # --- luot 2: dot bien cho BA chot vua them ---
    ("m23_rong_bang_lenh_LONG", "_TL_LENH_GHI_LONG = frozenset({",
     "_TL_LENH_GHI_LONG = frozenset()\n_TL_LENH_GHI_LONG_CU = frozenset({"),
    ("m24_bo_tieu_gia_tri_co_global", "                k += 2 if not ra else 1",
     "                k += 1"),
    ("m25_noi_kich_ban_ve_theo_THU_MUC",
     '_KICH_BAN_CHO_PHEP = frozenset({"scripts/tl.py"})',
     '_KICH_BAN_CHO_PHEP = frozenset({"scripts/tl.py", "scripts/build_cache.py",\n'
     '                                ".claude/dev/packet_loop.py"})'),
    ("m26_cong_fail_OPEN_khi_khong_hoi_duoc_runtime",
     'loi.append("KHONG DO DUOC: khong hoi duoc `tl tool-inventory --json` — fail-close")',
     "pass"),
    ("m27_bo_grep_diff_khoi_so_tran",
     '_CHO_SO_TRAN = frozenset({"head", "tail", "uniq", "git", "grep", "diff"})',
     '_CHO_SO_TRAN = frozenset({"head", "tail", "uniq", "git"})'),
    ("m28_bo_nhanh_co_ngan_gan_gia_tri",
     '        if (len(goc) > 2 and not goc.startswith("--")',
     '        if (False and len(goc) > 2 and not goc.startswith("--")'),
    ("m29_bo_mot_spelling_THAT_khoi_ho_sinh_tep",
     '_TL_CO_SINH_TEP = frozenset({"--out", "--output", "--out-dir", "--output-file"})',
     '_TL_CO_SINH_TEP = frozenset({"--output", "--out-dir", "--output-file"})'),
    ("m10_ghep_bo_heredoc_va_tach_dong",
     ('if "<<" in cmd:', 'if "\\n" in cmd:'), ("if False:", "if False:")),
    # ── luot 3: dot bien cho ba ban va P1/P2 cua cross-review luot 2 ────────────────────
    # Tra lai `lstrip` — phep so long hon phep chuan hoa, tuc danh sach cho phep vo hieu.
    ("m30_tra_lai_lstrip_cho_kich_ban",
     "    chuan = _chuan_hoa_kich_ban(kich)\n    if chuan is None or chuan not in _KICH_BAN_CHO_PHEP:",
     '    chuan = kich.lstrip("./")\n    if chuan not in _KICH_BAN_CHO_PHEP:'),
    # Tha moi khoa `git -c` — quay ve trang thai chi soi TEN CO.
    ("m31_git_c_tha_moi_khoa",
     '    khoa = str(v).split("=", 1)[0].strip().lower()',
     '    khoa = "core.abbrev"  # dot bien: khoa nao cung coi la hop le'),
    # Bo kiem gan bien lam TIEN TO cho lenh.
    ("m32_gan_bien_tien_to_tha_vo_dieu_kien",
     "    for t in toks[:k]:\n        ten = t.split(\"=\", 1)[0]",
     "    for t in []:\n        ten = t.split(\"=\", 1)[0]"),
    # Siet lai `isdigit` — tra ve dung chan oan ma luot 2 gay ra.
    # Dan khoa tu MTIME thay vi tu BAM — dung hinh dang ma docstring khai la KHONG lam.
    ("m35_bo_dem_khoa_theo_mtime",
     "    khoa = hashlib.sha256(pathlib.Path(reg).read_bytes()).hexdigest()[:32]",
     '    khoa = "%d" % int(pathlib.Path(reg).stat().st_mtime)'),
    ("m34_bo_timings_khoi_co_global_don",
     '_TL_CO_GLOBAL_CO_DON = frozenset({"--version", "--timings", "--deterministic", "--selftest"})',
     '_TL_CO_GLOBAL_CO_DON = frozenset({"--version", "--deterministic", "--selftest"})'),
    # WP1009 F14: quay ve nhan dien tl.py tren token GOC — dung hinh dang lo cua luot 5.
    ("m36_nhan_dien_tl_py_tren_kich_goc",
     '    if chuan.rsplit("/", 1)[-1] == "tl.py":',
     '    if kich.rsplit("/", 1)[-1] == "tl.py":'),
    # WP1038 F03: nui danh sach cho phep ky tu de chua `$` · bo chot dau thay the `THAYTHE`.
    ("m37_cho_dau_dola_vao_vung_ten_lenh_tl",
     '_RE_TL_VUNG_TEN_AN_TOAN = re.compile(r"[A-Za-z0-9._/\\\\:=+@ -]*\\Z")',
     '_RE_TL_VUNG_TEN_AN_TOAN = re.compile(r"[A-Za-z0-9._/\\\\:=+@ ${}\'?*`-]*\\Z")'),
    ("m38_bo_chot_THAYTHE_o_vung_ten_lenh_tl",
     ' or "THAYTHE" in a]', ']'),
    ("m33_siet_lai_isdigit_cho_co_ngan",
     '                and ("-" + goc[1]) in an and ("-" + goc[1]) in cho_phep):',
     '                and ("-" + goc[1]) in an and ("-" + goc[1]) in cho_phep\n'
     '                and goc[2:].isdigit()):'),
]


# ── PHEP CHAM DIEM, tach thanh HAM THUAN de co the DO duoc ─────────────────────────────
# Chinh bo test nay tung in `CA 27/28 dat · DOT BIEN 28/28 bi giet` — HAI CON SO CANH NHAU
# trong mot dong, va con so thu hai KHONG CO NGHIA: khi nen da co ca DO, moi dot bien "giet"
# tam thuong bang chinh ca do san. Do la P1 `suite-do-do-tren-nen-gpgsign` ma PR #342 phai va
# tren packet anh em; o day no chua bao gio duoc va, va no lo ra vi lan chay dau cua luot 3
# lam do `t3` (chan oan do chinh toi gay ra).
# Hai chot, can CA HAI: "giet" tinh bang HIEU SO, va nen do thi TU CHOI cong bo diem.
def giet_duoc(do_san, ket_qua):
    """Ca bi dot bien GIET = PASS o NEN ma FAIL o MUTANT."""
    return sorted(t for t, ok in ket_qua.items() if t not in do_san and not ok)


def duoc_cong_bo_diem(do_san):
    """Nen do thi KHONG duoc cong bo ty le dot bien — no khong phai 'so nho hon su that'."""
    return not do_san


def chay():
    goc = GUARD.read_text(encoding="utf-8")
    print("CA:")
    do, do_san = 0, set()
    for f in CA:
        ok, mo_ta = f(GUARD)
        do += not ok
        if not ok:
            do_san.add(f.__name__)
        print(f"  {'DAT ' if ok else 'DO  '} {f.__name__:38} {mo_ta}")

    # WINDOWS (va CHE DO NHE #647): cat DUNG vong lap dot bien, khong cat gi khac. Ca NEN o tren DA chay du —
    # bo ca nen la lam mu chan Windows, khac han voi bo phep DO LAI cua dot bien.
    # Tieu chi `dat` van doi SO DUONG hai ve qua `dat_windows`, khong duoc im.
    che_do = che_do_chay()
    if che_do != "du":
        dat = dat_windows(len(CA), do, len(DOT_BIEN))
        dong = dong_windows if che_do == "windows" else dong_nhe
        print(dong(len(CA) - do, len(CA), len(DOT_BIEN)))
        print("TONG:", "DAT" if dat else "DO")
        return 0 if dat else 1

    print("DOT BIEN (moi cai PHAI lam it nhat mot ca DO):")
    song = []
    with tempfile.TemporaryDirectory() as d:
        for ten, cu, moi in DOT_BIEN:
            cap = list(zip(cu, moi)) if isinstance(cu, tuple) else [(cu, moi)]
            if any(c not in goc for c, _ in cap):
                print(f"  DO   {ten:30} MOC KHONG CON TRONG MA -> dot bien chua tung chay")
                song.append(ten)
                continue
            ma = goc
            for c, m in cap:
                ma = ma.replace(c, m, 1)
            tep = pathlib.Path(d) / f"guard_{ten}.py"      # TEN RIENG tung dot bien
            tep.write_text(ma, encoding="utf-8")
            giet = giet_duoc(do_san, {f.__name__: f(tep)[0] for f in CA})
            if giet:
                print(f"  GIET {ten:30} lam DO: {', '.join(giet)}")
            else:
                print(f"  SONG {ten:30} KHONG ca nao do -> chot nay KHONG CO RANG")
                song.append(ten)

    tap_giet = len(DOT_BIEN) - len(song)
    if not duoc_cong_bo_diem(do_san):
        print(f"TONG: CA {len(CA) - do}/{len(CA)} dat")
        print(f"TONG: DIEM DOT BIEN BI TU CHOI — nen co {len(do_san)} ca DO SAN "
              f"({', '.join(sorted(do_san)[:3])}). Sua nen xanh truoc, roi moi doc duoc so.")
    else:
        print(f"TONG: CA {len(CA) - do}/{len(CA)} dat · "
              f"DOT BIEN {tap_giet}/{len(DOT_BIEN)} bi giet")
    # Vi ngu phai doi SO DUONG hai ve, khong duoc thoa man boi so rong (bai hoc "so rong thoa
    # `not DO`" cua #319): so ca da chay phai BANG so ca dang ky VA > 0.
    dat = (len(CA) > 0 and do == 0 and len(DOT_BIEN) > 0 and not song)
    print("TONG:", "DAT" if dat else "DO")
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(chay())
