#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import contextlib
import io
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import tempfile

import yaml

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOC = (".claude/dev", ".claude/hooks", ".githooks", ".github/checks", "scripts/tl_core")
OPS_REVIEWS = "ops/reviews/"
MOI_TRUONG_CI = "github-actions/linux"
MOI_TRUONG_WINDOWS = "github-actions/windows"
MOI_TRUONG_DA_BIET = frozenset({MOI_TRUONG_CI, MOI_TRUONG_WINDOWS})
LAUNCHER_WORKFLOW = ROOT / ".github/workflows/launcher-windows.yml"
CI_WORKFLOW = ROOT / ".github/workflows/ci.yml"
MOI = {
    ".claude/dev/chon_reviewer_test.py": r"(?s)nền: (\d+)/(\d+) đạt.*TỔNG: ĐẠT",
    ".claude/dev/gh_readback_test.py": r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)",
    ".claude/dev/mcp_gh_test.py": r"(?s)CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT.*ĐỘT BIẾN.*ĐẠT.*TỔNG: ĐẠT",
    ".claude/dev/mcp_github_doc_test.py": r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)",
    ".claude/dev/probe_mang_test.py": r"(?s)tự đột biến cổng: 9/9 chết.*named mutant probe_missing_tool_executes_git: 1/1 chết.*nền: 11/11 đạt.*TỔNG: ĐẠT",
    # GIU NGUYEN `\d+` — M4 dong bang hanh vi Linux, va mau nay la duong Linux di qua.
    # Lo #319 (`0/0 bi giet` lot vi `bang_chung_xanh` chi soi hai nhom CA) CO THAT va
    # co SAN tu base, nhung bit no o day la doi hanh vi Linux — ngoai pham vi packet
    # #456. Chot tuong duong duoc dat o duong WINDOWS (`MOI_WINDOWS`), la noi dot bien
    # bat buoc cua A2 thuc su bieu hien. Lo phia Linux de lai cho packet ke.
    ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
}
# Tap mau THAY THE, chi dung khi nen dang chay la Windows. Windows nhan HAI dang:
#   (a) dong da cat dot bien;  (b) dong Linux day du — ai do chay tay do du van DAT (A3).
# CA HAI deu doi so dot bien KHAC 0 (`[1-9]\d*`). Do la chot tuong duong `len(DOT_BIEN)>0`
# o tang so dang ky, va la thu giet dot bien bat buoc thu hai cua A2 (nhanh Windows in
# `DOT BIEN 0/0 bi giet`). Dat o DAY chu khong o `MOI` vi dot bien ay bieu hien tren
# WINDOWS; siet `MOI` se doi hanh vi Linux, trai M4 (finding P2 cross-review luot 1).
MOI_WINDOWS = {
    ".claude/hooks/pretooluse_guard_test.py": (
        r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS"
        r".*TONG: DAT",
        r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d*/[1-9]\d* bi giet"
        r".*TONG: DAT",
    ),
}
CACH_LY = {}
DA_NOI = {
    ".claude/dev/ci_dang_ky_test.py",
    ".claude/dev/codex_cred_test.py", ".claude/dev/gate_lifecycle_test.py",
    ".claude/dev/idiom_py_test.py", ".claude/dev/launcher_test.py",
    ".claude/dev/packet_loop_test.py", ".githooks/eol_policy_test.py",
    ".githooks/pre_push_test.py", ".github/checks/ci_phamvi_test.py",
    "ops/bien_nhan_v2_test.py",
    "ops/cong_cu_test.py", "ops/lease_publish_test.py",
    "scripts/tl_core/command_registry_test.py",
}
DANG_KY = set(MOI) | DA_NOI


def tim(root):
    """Trả (test sống, hiện vật, vị trí lạ); ops chỉ nhận tệp mức đỉnh."""
    song, hien_vat, la = set(), set(), set()
    for p in root.rglob("*_test.py"):
        q = p.relative_to(root).as_posix()
        if q.startswith(OPS_REVIEWS):
            hien_vat.add(q)
        elif any(q.startswith(g + "/") for g in GOC) or (q.startswith("ops/") and q.count("/") == 1):
            song.add(q)
        else:
            la.add(q)
    return song, hien_vat, la


def bi_tat(x): return x is False or (isinstance(x, str) and x.strip().lower() in ("false", "${{ false }}"))


def _runner_matrix_dung(expr):
    if not isinstance(expr, str) or "fromJSON(" not in expr:
        return False
    compact = re.sub(r"\s+", " ", expr)
    if not all(x in compact for x in ("github.event_name", "workflow_dispatch",
                                       "inputs.runner_set", "windows-only")):
        return False
    try:
        arrays = [json.loads(x) for x in re.findall(r"'(\[[^']*\])'", expr)]
    except json.JSONDecodeError:
        return False
    return arrays == [["windows-latest"], ["windows-latest", "ubuntu-latest"]]


def _python_matrix_dung(expr):
    if not isinstance(expr, str):
        return False
    compact = re.sub(r"\s+", " ", expr)
    windows = re.search(r"matrix\.os\s*==\s*'windows-latest'.*'3\.13'.*'3\.11'", compact)
    ubuntu = re.search(r"matrix\.os\s*==\s*'ubuntu-latest'.*'3\.11'.*'3\.13'", compact)
    return bool(windows or ubuntu)


def loi_launcher_windows(source=None):
    source = LAUNCHER_WORKFLOW.read_text(encoding="utf-8") if source is None else source
    try:
        data = yaml.safe_load(source) or {}
    except yaml.YAMLError as e:
        return [f"launcher Windows YAML lỗi: {e}"], 1
    triggers = data.get("on", data.get(True))
    if not isinstance(triggers, dict):
        return ["launcher Windows thiếu trigger map"], 1
    dispatch = triggers.get("workflow_dispatch")
    runner = ((dispatch or {}).get("inputs") or {}).get("runner_set") if isinstance(dispatch, dict) else None
    expected = {"required": True, "default": "windows-only", "type": "choice",
                "options": ["windows-only", "windows-and-ubuntu"]}
    job = ((data.get("jobs") or {}).get("launcher") or {})
    matrix = ((job.get("strategy") or {}).get("matrix") or {}).get("os")
    setup = next((s for s in (job.get("steps") or [])
                  if isinstance(s, dict) and s.get("uses") == "actions/setup-python@v5"), {})
    checks = [
        (isinstance(runner, dict) and all(runner.get(k) == v for k, v in expected.items()),
         "launcher Windows sai hợp đồng workflow_dispatch.runner_set"),
        (all(name in triggers for name in ("push", "pull_request")),
         "launcher Windows thiếu hợp đồng non-dispatch"),
        (_runner_matrix_dung(matrix), "launcher Windows sai ánh xạ runner dispatch/non-dispatch"),
        (_python_matrix_dung((setup.get("with") or {}).get("python-version")),
         "launcher Windows sai ánh xạ Python Windows=3.13 Ubuntu=3.11"),
    ]
    return [message for ok, message in checks if not ok], len(checks)


# LOP A (`R6-F01`/`R6-F02` + 13 cua tu liet ke) — DAO BA DANH SACH CAM THANH MOT KHUON DUOC
# CONG NHAN, mac dinh FAIL-CLOSE. Ba tap cu FAIL-OPEN voi moi thu ngoai danh sach (do duoc:
# `pdm|rye|hatch remove ruff` ra GHIM; `--target=tmp`, `-ttmp` lot). Nay mot dong cham `ruff`
# phai la (1) LOI GOI ruff, hoac (2) `<tien to> install [<tuy chon an toan>...] ruff<rang buoc>`.
# Hai danh sach con lai la CHO PHEP: bo mot phan tu lam cong CHAT hon nen chieu NHAN bat duoc.
_TIEN_TO_CAI = (["pip"], ["pip3"], ["uv", "pip"],
                ["python", "-m", "pip"], ["python3", "-m", "pip"])
_TUY_CHON_AN_TOAN = frozenset({"--quiet", "-q", "--no-cache-dir",
                               "--disable-pip-version-check", "--no-input"})
# Ten goi PEP 508; phan con lai cua token la RANG BUOC — khong liet ke toan tu nao nen khong sot.
_TEN_GOI = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:\[[^\]]*\])?")
_RUFF_NHAC = re.compile(r"\bruff\b", re.I)   # PEP 503: ten goi khong phan biet hoa/thuong
# MOT vi tu nhan dang lenh, dung chung cho phan loai VA probe (luot 8): hai duong rieng la hai
# co hoi lech — probe tung so CHUOI NGUYEN VAN nen thua mot dau cach la truot, con co cua trinh
# (`python3 -u -m ruff`, chay that rc=0) bi doc thanh "cai khong phan tich duoc".
_TRINH_PY = re.compile(r"^python3?(\.\d+)?$")

def _lenh_tho(run):
    """Cat than `run` thanh cac LENH tho, MOT luot co y thuc TRICH DAN. Ban truoc cat dong vat ly va
    xoa comment bang regex TRUOC khi tach token nen chuoi TOML nhieu dong, `#` trong dau nhay, toan
    tu duoc TRICH DAN deu doc sai (l9 H1/H2/H10) — cung goc: quyet dinh tren VAN BAN THO truoc khi
    biet ranh gioi trich dan. Trong dau nhay, tat ca la DU LIEU."""
    ra, cur, nhay, i = [], "", "", 0
    while i < len(run or ""):
        c = run[i]
        if nhay:
            cur += c
            if c == "\\" and nhay == '"' and i + 1 < len(run): cur += run[i + 1]; i += 2; continue
            if c == nhay: nhay = ""
        elif c in "'\"":
            nhay = c; cur += c
        elif c == "\\" and i + 1 < len(run) and run[i + 1] == "\n":
            i += 2; cur += " "; continue                      # noi dong: dau chéo nguoc cuoi dong
        elif c == "#":
            while i < len(run) and run[i] != "\n": i += 1     # comment: toi HET dong vat ly
            continue
        elif c == "\n" or c == ";":
            ra.append(cur); cur = ""
        elif c == "&" or c == "|":
            ra.append(cur); cur = ""
            if i + 1 < len(run) and run[i + 1] == c: i += 1
        else:
            cur += c
        i += 1
    ra.append(cur)
    return [x.strip() for x in ra if x.strip()]


def _dong_logic(run):
    """argv cua TUNG lenh trong `run`."""
    out = []
    for ca in _lenh_tho(run):
        try: out.append(shlex.split(ca))
        except ValueError: out.append(ca.split())
    return [t for t in out if t]


def _cham_ruff(tok):
    """Lenh CO nhac goi `ruff` — theo TEN GOI, khong theo chuoi con: `ruff.toml` ra `ruff-toml` nen
    `printf … > ruff.toml` khong con bi doc thanh "cai" roi DO OAN; `pdm remove ruff` van bi bat."""
    return any(_RUFF_NHAC.search(t) and (_TEN_GOI.match(t) is not None)
               and _chuan_ten(_TEN_GOI.match(t).group(0)) == "ruff" for t in tok)


def _la_chay_ruff(tok):
    """argv CHAY ruff: `ruff …` · `python[3] [co trinh] -m ruff …` · `uv run ruff` · `uvx ruff`."""
    if not tok: return False
    dau = _TEN_GOI.match(tok[0])
    if dau and _chuan_ten(dau.group(0)) == "ruff": return True
    if tok[:2] == ["uv", "run"] or tok[:1] == ["uvx"]:
        return any(_chuan_ten(x) == "ruff" for x in tok[1:3])
    if not _TRINH_PY.match(tok[0]): return False
    i = 1
    while i < len(tok) and tok[i] != "-m" and tok[i].startswith("-"):
        if tok[i].startswith("-m") and len(tok[i]) > 2:      # `-mruff` viet lien (l9 H3)
            return _chuan_ten(tok[i][2:]) == "ruff"
        i += 2 if tok[i] in ("-X", "-W") else 1              # hai co NAY an them mot doi so
    return tok[i:i + 1] == ["-m"] and len(tok) > i + 1 and _chuan_ten(tok[i + 1]) == "ruff"


def _chuan_ten(t):
    """PEP 503: bo extras, ha chu thuong, gom `-` `_` `.` — de `Ruff` va `ruff[all]` cung ve mot."""
    t = re.split(r"\[", t, 1)[0]
    return re.sub(r"[-_.]+", "-", t.strip().lower())


def _loai_mot_dong(tok):
    """GHIM | KHONG_GHIM | KHONG_PHAN_TICH_DUOC | KHONG cho MOT dong logic da tach token."""
    if not tok:
        return "KHONG"
    if _la_chay_ruff(tok):
        return "KHONG"                                  # (1) CHAY ruff, khong phai cai
    for tt in _TIEN_TO_CAI:                             # (2) khuon cai duy nhat duoc cong nhan
        if tok[:len(tt)] == tt and tok[len(tt):len(tt) + 1] == ["install"]:
            con = tok[len(tt) + 1:]
            break
    else:
        return "KHONG_PHAN_TICH_DUOC"
    rang_buoc = None
    for t in con:
        if t.startswith("-"):
            if t not in _TUY_CHON_AN_TOAN:
                return "KHONG_PHAN_TICH_DUOC"           # tuy chon la: khong chung minh duoc
            continue
        m = _TEN_GOI.match(t)
        if m is None or _chuan_ten(m.group(0)) != "ruff" or rang_buoc is not None:
            return "KHONG_PHAN_TICH_DUOC"               # goi khac, hoac hai ban ruff
        rang_buoc = t[m.end():]
    if rang_buoc is None:
        return "KHONG"
    return "GHIM" if rang_buoc == "==0.15.15" else "KHONG_GHIM"


def _phan_loai_cai_ruff(run):
    """Ket qua XAU NHAT tren MOI lenh cua mot than `run` — duyet het, khong tra ve o lenh dau, nen
    `upgrade` dat SAU mot ban ghim khong con lot. Xau dan: KHONG < GHIM < KHONG_GHIM < KPT."""
    thu_tu = {"KHONG": 0, "GHIM": 1, "KHONG_GHIM": 2, "KHONG_PHAN_TICH_DUOC": 3}
    ket, vet = "KHONG", None
    for tok in _dong_logic(run):
        if not _cham_ruff(tok): continue
        moi_l = _loai_mot_dong(tok)
        if thu_tu[moi_l] > thu_tu[ket]: ket, vet = moi_l, " ".join(tok)
    return ket, vet


def _probe_sau_ghim(run):
    """Probe `ruff --version` phai SAU dong cai GHIM trong CUNG than `run`. Ban truoc chi doi probe
    CO MAT (l7 h4), va so CHUOI nen thua dau cach la truot (l8) — nay so ARGV bang cung vi tu."""
    ghim = probe = -1
    for i, tok in enumerate(_dong_logic(run)):
        if _la_chay_ruff(tok) and "--version" in tok:
            probe = i if probe < 0 else probe
        elif _cham_ruff(tok) and _loai_mot_dong(tok) == "GHIM" and ghim < 0:
            ghim = i
    return 0 <= ghim < probe


def _buoc_co_dieu_kien(step):
    """DAO DANH SACH: chi buoc VO DIEU KIEN moi chung minh duoc no CHAY. Ban truoc liet ke hai
    cach viet false nen `if: '0'`, `if: '${{false}}'`, `if: runner.os == 'Linux'` deu lot."""
    return step.get("if") is not None


def loi_ruff_ci(source=None):
    """Hợp đồng Ruff của CI, đọc MỌI job — packet #463 tách `test registry` khỏi `jobs.gate`.

    BA chốt (`RUFF CI: n/3`) — đúng `M7` của lease và `A7` của spec r21, không hơn: (1) mọi job cài
    Ruff đều ghim `ruff==0.15.15`; (2) mọi job cài Ruff đều in probe `ruff --version` SAU dòng cài;
    (3) đúng MỘT job chạy `--chay`, Ruff cài CÙNG job và TRƯỚC bước đó. 1–2 đo trên MỌI job vì hai
    phản chứng đột biến bản Ruff ĐẦU TIÊN trong tệp (bản ở `gate`) — chỉ soi job registry thì cả
    hai LỌT. `ci.yml` chưa tách: `[]`.

    Chốt env (`PIP_TARGET`…) ĐÃ BỎ theo quyết định chủ kho 13-09-2026, §12: nó do phiên thi công tự
    thêm ở lượt 7, không có trong `M7` lẫn `A7`, và ba lượt liền sinh CÙNG một hình dạng lỗi (15
    cửa) vì đòi chứng minh TĨNH một chuyện RUNTIME — lượt 9 đo được nó đã chặn OAN
    `PYTHONIOENCODING=utf_8` (chạy thật rc=0). Đóng cả lớp theo KIẾN TRÚC, không theo bản vá.
    """
    source = CI_WORKFLOW.read_text(encoding="utf-8") if source is None else source
    try:
        data = yaml.safe_load(source) or {}
    except yaml.YAMLError as e:
        return [f"CI YAML lỗi khi kiểm Ruff: {e}"], 1
    jobs = {k: v for k, v in ((data.get("jobs") or {}).items()) if isinstance(v, dict)}
    buoc_theo_job = {jn: [x for x in (j.get("steps") or []) if isinstance(x, dict)]
                     for jn, j in jobs.items()}
    runs_theo_job = {jn: [(x.get("run") if isinstance(x.get("run"), str) else "") for x in bs]
                     for jn, bs in buoc_theo_job.items()}
    # Phan loai TUNG BUOC; buoc bi `if: false` khong tinh la provisioning.
    loai_theo_job = {jn: [(("KHONG_PHAN_TICH_DUOC", "buoc co dieu kien")
                           if _RUFF_NHAC.search(str(x.get("run") or "")) else ("KHONG", None))
                          if _buoc_co_dieu_kien(x)
                          else _phan_loai_cai_ruff(x.get("run") if isinstance(x.get("run"), str) else "")
                          for x in bs]
                     for jn, bs in buoc_theo_job.items()}
    job_cai_ruff = {jn: runs for jn, runs in runs_theo_job.items()
                    if any(l != "KHONG" for l, _ in loai_theo_job[jn])}
    # Nhan dien theo ARGV, khong SUBSTRING: space -> tab cho CUNG argv ma ban truoc bao "khong job nao chay registry" (l9 H7).
    def _la_registry(run):
        return any(t.endswith("ci_dang_ky_test.py") and "--chay" in tok
                   for tok in _dong_logic(run) for t in tok)
    job_registry = [jn for jn, runs in runs_theo_job.items() if any(_la_registry(x) for x in runs)]
    # THIEU GHIM = khong buoc nao GHIM, HOAC co buoc KHONG_GHIM/KPT — ve hai bat "upgrade dat SAU".
    thieu_ghim = [jn for jn in job_cai_ruff
                  if not any(l == "GHIM" for l, _ in loai_theo_job[jn])
                  or any(l in ("KHONG_GHIM", "KHONG_PHAN_TICH_DUOC") for l, _ in loai_theo_job[jn])]
    # Probe phai o CHINH buoc cai — cung buoc thi khong the bi mot buoc khac "muon" bang chung.
    thieu_probe = [jn for jn in job_cai_ruff
                   if not any(l == "GHIM" and _probe_sau_ghim(runs_theo_job[jn][i])
                              for i, (l, _) in enumerate(loai_theo_job[jn]))]
    truoc = False
    if len(job_registry) == 1:
        jn = job_registry[0]; runs = runs_theo_job[jn]
        ruff_i = next((i for i, (l, _) in enumerate(loai_theo_job[jn]) if l == "GHIM"), -1)
        gate_i = next((i for i, x in enumerate(runs) if _la_registry(x)), -1)
        truoc = 0 <= ruff_i < gate_i
    checks = [
        (job_cai_ruff and not thieu_ghim, f"CI không ghim Ruff 0.15.15 (job: {thieu_ghim or 'không job nào cài Ruff'})"),
        (job_cai_ruff and not thieu_probe, f"CI không in probe Ruff --version (job: {thieu_probe or 'không job nào cài Ruff'})"),
        (truoc, "CI không provision Ruff trước test registry trong cùng job "
                f"(job chạy test registry: {job_registry or 'KHÔNG CÓ'})"),
    ]
    return [message for ok, message in checks if not ok], len(checks)

def giet_windows_311_launcher_workflow(source):
    anchor = "'3.13'"
    if source.count(anchor) != 1:
        return False
    mutant = source.replace(anchor, "'3.11'", 1)
    return bool(loi_launcher_windows(mutant)[0])

def kiem(root=ROOT, registry=DANG_KY, workflows=None, cach_ly=CACH_LY):
    song, _, la = tim(root)
    loi = []
    loi += ["test sống chưa đăng ký: " + x for x in sorted(song - registry)]
    loi += ["mục đăng ký không có tệp: " + x for x in sorted(registry - song)]
    loi += ["test ở vị trí chưa biết: " + x for x in sorted(la)]
    loi += ["cách ly không nằm trong sổ: " + x for x in sorted(set(cach_ly) - registry)]
    for x, no in cach_ly.items():
        if not all(no.get(k) for k in ("slug", "ly_do", "moi_truong", "log")):
            loi.append("cách ly thiếu slug, lý do, môi trường hoặc log: " + x)
        elif no["moi_truong"] not in MOI_TRUONG_DA_BIET:
            loi.append("cách ly có môi trường không hợp lệ: " + x)
    if workflows is None:
        runs = []
        for p in (root / ".github/workflows").glob("*.yml"):
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            for job in (data.get("jobs") or {}).values():
                if not isinstance(job, dict) or bi_tat(job.get("if")): continue
                for step in (job.get("steps") or []):
                    if isinstance(step, dict) and not bi_tat(step.get("if")) and isinstance(step.get("run"), str):
                        runs.extend(line for line in step["run"].splitlines()
                                    if not line.lstrip().startswith("#"))
        workflows = "\n".join(runs)
    for x in sorted(DA_NOI):
        if x == ".claude/dev/ci_dang_ky_test.py":
            co = "python .claude/dev/ci_dang_ky_test.py --chay" in workflows
        elif x == "ops/lease_publish_test.py":
            co = "ops/chay_lease_publish_test.sh" in workflows
        else:
            co = x in workflows
        if not co:
            loi.append("CI không gọi mục đăng ký: " + x)
    if "python .claude/dev/ci_dang_ky_test.py --chay" not in workflows:
        loi.append("CI không gọi nhóm đăng ký mới")
    return loi, len(song), len(registry)


def bang_chung_xanh(text, mau):
    m = re.search(mau, text, re.M)
    if not m:
        return False
    return not m.groups() or len(m.groups()) != 2 or (int(m.group(1)) > 0 and m.group(1) == m.group(2))


def moi_truong_hien_tai(env=os.environ):
    """Chỉ nhận diện khi cả hai dấu hiệu runner chuẩn cùng khớp."""
    if env.get("GITHUB_ACTIONS") == "true" and env.get("RUNNER_OS") in ("Linux", "Windows"):
        return f"github-actions/{env['RUNNER_OS'].lower()}"
    return None


def nen_la_windows(ten_nen=None):
    """Nen CHAY THAT cua tien trinh nay — KHONG phai nen CI khai trong bien moi truong.

    Phai hoi `os.name`, dung hoi `moi_truong_hien_tai()`: bo test con chay CUNG mot OS
    voi so dang ky nay, va no quyet dinh in dong Windows theo `os.name`. Neu hoi bien CI
    thi mot luot chay TAY tren may Windows (khong co GITHUB_ACTIONS) se bi coi la
    khong-Windows, va dong hop le cua no bi cham DO — do la lam tron XUONG, cung ho voi
    loi lam tron LEN ma `dem_la_do` sinh ra de chan.
    """
    return (os.name if ten_nen is None else ten_nen) == "nt"


def mau_theo_nen(path, mau, la_windows):
    """Tap mau duoc chap nhan cho `path` tren nen dang chay.

    Windows dung tap THAY THE trong `MOI_WINDOWS` — KHONG kem `mau` goc. Co chu dich:
    tap ay da chua dang Linux (sieu chat hon), nen A3 "dong Linux tren nen Windows van
    DAT" van giu, DONG THOI `0/0 bi giet` bi tu choi tren Windows. Neu kem ca `mau` goc
    thi mau long se nhan `0/0` va dot bien bat buoc thu hai cua A2 SONG.

    Nen khac: chi `mau` goc, khong doi mot chut nao so voi base (M4).
    """
    mau_nen = MOI_WINDOWS.get(path)
    return list(mau_nen) if (la_windows and mau_nen) else [mau]


def cach_ly_chap_nhan(ok, da_neo, hien_tai):
    """OS đã biết khác neo dùng kết quả thật; nền lạ vẫn không được làm tròn lên."""
    if hien_tai is None:
        return None
    if hien_tai == da_neo:
        return not ok
    return ok if hien_tai in MOI_TRUONG_DA_BIET else None


def trong_ci(env=os.environ):
    """Có đang chạy TRONG CI không — ĐỘC LẬP với `moi_truong_hien_tai`.

    Hai câu hỏi khác nhau và phải hỏi riêng: `moi_truong_hien_tai` hỏi *"nền nào"*
    và đòi CẢ `RUNNER_OS == Linux`, nên trên `windows-latest` nó trả None. Nếu dùng
    nó để suy ra "có ở CI không" thì Windows bị coi là ngoài CI và cổng lại làm tròn
    lên đúng như cũ.
    """
    return env.get("GITHUB_ACTIONS") == "true"


def dem_la_do(chap_nhan, o_trong_ci):
    """Phán quyết CÓ TÍNH LÀ ĐỎ KHÔNG — bất biến nằm ở TẦNG TIÊU THỤ.

    `cach_ly_chap_nhan` đã trung thực trả None cho trạng thái thứ ba, và đột biến
    `r4-khong-do-duoc-thanh-dat` canh đúng điều đó. Nhưng chỗ LÀM TRÒN LÊN nằm ở nơi
    TIÊU THỤ giá trị ấy, nên bất biến phải được cưỡng chế ở đây, nếu không ta chỉ có
    thêm một bảo chứng giả thứ hai (#401).

    None trong CI ⇒ ĐỎ (fail-closed). None ngoài CI ⇒ không đỏ: chạy cục bộ cũng giải
    ra None, làm đỏ ở đó thì mọi lượt `--chay` trên máy lập trình viên đỏ vĩnh viễn.
    """
    if chap_nhan is None:
        return bool(o_trong_ci)
    return not chap_nhan


def _chay_that(path):
    p = subprocess.run([sys.executable, path], cwd=ROOT, text=True, encoding="utf-8",
                       errors="backslashreplace", stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return p.returncode, p.stdout


def chay_moi(moi=MOI, cach_ly=CACH_LY, chay_mot=_chay_that,
             doc_moi_truong=moi_truong_hien_tai, doc_trong_ci=trong_ci,
             doc_nen_windows=nen_la_windows):
    """Năm tham số sau là ĐƯỜNG NỐI ĐỂ ĐO, không phải cấu hình: phản chứng phải gọi
    được chính hàm này với bộ chạy giả, nếu không tầng tiêu thụ lại không ai canh.

    `doc_nen_windows` là seam thứ năm, thêm cho packet #456: nếu nền chỉ đọc được
    qua `os.name` thật thì phản chứng A3 phải có máy Windows mới chạy được, tức là
    không ai canh — đúng thứ bốn seam kia sinh ra để tránh."""
    do = 0
    hien_tai = doc_moi_truong()
    o_trong_ci = doc_trong_ci()
    la_windows = doc_nen_windows()
    for path, mau in moi.items():
        rc, ban_in = chay_mot(path)
        ok = rc == 0 and any(bang_chung_xanh(ban_in, m)
                             for m in mau_theo_nen(path, mau, la_windows))
        print(ban_in, end="")
        if path in cach_ly:
            no = cach_ly[path]
            chap_nhan = cach_ly_chap_nhan(ok, no["moi_truong"], hien_tai)
            nen = hien_tai or "không xác định"
            if chap_nhan is None and o_trong_ci:
                print(f"CI_DANG_KY {path}: ĐỎ — KHÔNG ĐO ĐƯỢC trong CI, môi trường={nen}, "
                      f"cách ly neo {no['moi_truong']}")
            elif chap_nhan is None:
                print(f"CI_DANG_KY {path}: KHÔNG ĐO ĐƯỢC (ngoài CI) — môi trường={nen}")
            elif hien_tai != no["moi_truong"]:
                print(f"CI_DANG_KY {path}: {'ĐẠT' if ok else 'ĐỎ'} — KHÔNG CÁCH LY trên {nen}, rc={rc}")
            elif not chap_nhan:
                print(f"CI_DANG_KY {path}: ĐỎ — đã xanh, hãy gỡ khỏi cách ly")
            else:
                print(f"CI_DANG_KY {path}: CÁCH LY rc={rc} nợ={no['slug']}")
            do += dem_la_do(chap_nhan, o_trong_ci)
        else:
            print(f"CI_DANG_KY {path}: {'ĐẠT' if ok else 'ĐỎ'} rc={rc}")
            do += not ok
    return do


def phan_chung():
    """Mỗi chốt dùng một bản sao fixture riêng dưới /tmp."""
    # F02 luot 3 — MOT danh sach, MOT diem noi; ten va ket qua o CUNG mot tuple. Hai ban va truoc
    # giu HAI danh sach song song canh bang DO DAI, khong bat lech THU TU (bo ten cuoi ra 64/64
    # True, dao thu tu ra 65/65 True). Khong con `zip` — lop loi chet theo CAU TRUC.
    KQ = []
    def _them(ten, ok):
        if any(t == ten for t, _ in KQ):
            raise AssertionError(f"trung ten ca phan chung: {ten}")
        KQ.append((ten, bool(ok)))
    with tempfile.TemporaryDirectory(prefix="ci-dang-ky-") as d:
        base = pathlib.Path(d)
        for i, kind in enumerate(("thieu", "mat_tep", "mat_loi_goi", "vi_tri_la")):
            r = base / str(i)
            (r / ".claude/dev").mkdir(parents=True)
            (r / ".github/workflows").mkdir(parents=True)
            (r / ".claude/dev/a_test.py").touch()
            reg, wf = {".claude/dev/a_test.py"}, "python .claude/dev/ci_dang_ky_test.py --chay"
            old = set(DA_NOI)
            try:
                DA_NOI.clear()
                if kind == "thieu": reg.clear()
                elif kind == "mat_tep": reg.add(".claude/dev/mat_test.py")
                elif kind == "mat_loi_goi":
                    DA_NOI.add(".claude/dev/a_test.py"); wf = ""
                else:
                    (r / "la").mkdir(); (r / "la/x_test.py").touch()
                _them(("i-thieu-so", "ii-mat-tep", "iii-mat-loi-goi", "iv-vi-tri-la")[i], bool(kiem(r, reg, wf)[0]))
            finally:
                DA_NOI.clear(); DA_NOI.update(old)
        # (a) Bản sao sổ cách ly mất slug phải đỏ.
        mutant_cu = {".claude/dev/a_test.py": {"slug": "", "ly_do": "đỏ trên CI"}}
        _them("a-cach-ly-thieu-slug", bool(kiem(r, reg, wf, mutant_cu)[0]))
        mutant = {".claude/dev/a_test.py": {"slug": "nợ", "ly_do": "đỏ trên CI",
                                                "log": "log-r3"}}
        _them("r4-thieu-moi-truong", bool(kiem(r, reg, wf, mutant)[0]))
        # r5: neo môi trường ngoài đúng nguồn giá trị phải đỏ ở tầng cấu trúc.
        mutant = {".claude/dev/a_test.py": {"slug": "nợ", "ly_do": "đỏ trên CI",
                    "moi_truong": "github-actions/lin-typo", "log": "log-r3"}}
        _them("r5-moi-truong-sai-tap", any("môi trường không hợp lệ" in x for x in kiem(r, reg, wf, mutant)[0]))
        # r5: xoá run thật, giữ nguyên lệnh trong YAML comment vẫn phải đỏ.
        yml = r / ".github/workflows/comment.yml"
        yml.write_text("jobs:\n  x:\n    steps:\n      # - run: python .claude/dev/a_test.py\n", encoding="utf-8")
        old = set(DA_NOI); DA_NOI.clear(); DA_NOI.add(".claude/dev/a_test.py")
        try: _them("r5-comment-gia-loi-goi", any("CI không gọi mục" in x for x in kiem(r, reg)[0]))
        finally: DA_NOI.clear(); DA_NOI.update(old)
        old = set(DA_NOI); DA_NOI.clear(); DA_NOI.add(".claude/dev/a_test.py")
        for level in ("step", "job", "expr", "normal"):
            yml.write_text("jobs:\n  x:\n" + ("    if: false\n" if level == "job" else "") + "    steps:\n      - " + (("if: ${{ false }}\n        " if level == "expr" else "if: false\n        ") if level in ("step", "expr") else "") + "run: python .claude/dev/a_test.py\n", encoding="utf-8")
            found = any("CI không gọi mục" in x for x in kiem(r, reg)[0])
            _them({"step": "r5-step-if-false", "job": "r5-job-if-false",
                   "expr": "r5-step-if-literal-expr", "normal": "r5-normal-step"}[level],
                  found if level != "normal" else not found)
        DA_NOI.clear(); DA_NOI.update(old)
        # (b) Bản sao chương trình cách ly chuyển xanh phải bị yêu cầu gỡ.
        green = base / "green_test.py"
        green.write_text("print('1/1')\n", encoding="utf-8")
        p = subprocess.run([sys.executable, green], text=True, stdout=subprocess.PIPE)
        xanh = p.returncode == 0 and bang_chung_xanh(p.stdout, r"^(\d+)/(\d+)$")
        _them("b-cach-ly-chuyen-xanh", not cach_ly_chap_nhan(xanh, "github-actions/linux", "github-actions/linux"))
        # r4: bỏ phép so làm bản xanh bắn ở môi trường khác; đúng ra phải là None.
        _them("r4-bo-so-moi-truong", (not xanh) is not cach_ly_chap_nhan(xanh, "github-actions/linux", None))
        # r4: đột biến đổi trạng thái thứ ba thành ĐẠT phải bị bắt.
        _them("r4-khong-do-duoc-thanh-dat", cach_ly_chap_nhan(xanh, "github-actions/linux", None) is None and True is not None)
    # Hai chiều bằng chứng: rc đỏ dù có dòng xanh; rc xanh nhưng thiếu dòng xanh.
    _them("rc-do-ban-in-xanh", not (1 == 0 and bang_chung_xanh("TỔNG: ĐẠT", r"TỔNG: ĐẠT")))
    _them("rc-xanh-thieu-ban-in", not (0 == 0 and bang_chung_xanh("", r"TỔNG: ĐẠT")))
    # r6 (#401): VỊ TỪ trung thực rồi mà NƠI TIÊU THỤ vẫn làm tròn lên được — đó là
    # khuyết tật đã sống sót qua r4 và r5. Nên canh cả hai tầng.
    _them("r6-vi-tu-none-trong-ci-la-do", dem_la_do(None, True) is True)
    _them("r6-vi-tu-none-ngoai-ci-khong-do", dem_la_do(None, False) is False)
    _them("r6-vi-tu-da-xanh-van-do", dem_la_do(False, False) is True)
    _them("r6-vi-tu-cach-ly-hop-le-khong-do", dem_la_do(True, True) is False)
    # r6: `trong_ci` phải ĐỘC LẬP với `moi_truong_hien_tai` — thiếu RUNNER_OS vẫn là CI,
    # còn không có GITHUB_ACTIONS thì dù có RUNNER_OS vẫn KHÔNG phải CI.
    _them("r6-trong-ci-khong-doi-runner-os", trong_ci({"GITHUB_ACTIONS": "true"}) is True)
    _them("r6-thieu-github-actions-khong-phai-ci", trong_ci({"RUNNER_OS": "Linux"}) is False)
    _them("r6-github-actions-false-khong-phai-ci", trong_ci({"GITHUB_ACTIONS": "false", "RUNNER_OS": "Linux"}) is False)
    _them("wp430-nhan-linux", moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "Linux"}) == MOI_TRUONG_CI)
    _them("wp430-nhan-windows", moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "Windows"}) == MOI_TRUONG_WINDOWS)
    _them("wp430-runner-la-fail-close", moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "macOS"}) is None)
    _them("wp430-windows-xanh-that", cach_ly_chap_nhan(True, MOI_TRUONG_CI, MOI_TRUONG_WINDOWS) is True)
    _them("wp430-windows-do-that", cach_ly_chap_nhan(False, MOI_TRUONG_CI, MOI_TRUONG_WINDOWS) is False)
    # r6: TẦNG TIÊU THỤ — gọi chính `chay_moi` với bộ chạy giả. Gỡ phép cộng ở đó ra thì
    # ba ca này ĐỎ; đó là điều mà đột biến canh-vị-từ `r4-khong-do-duoc-thanh-dat` KHÔNG
    # bắt được, và là lý do nợ N6 lọt cổng trên windows-latest.
    gia_moi = {"gia_test.py": r"^(\d+)/(\d+)$"}
    gia_no = {"gia_test.py": {"slug": "gia", "ly_do": "gia",
                              "moi_truong": "github-actions/linux", "log": "gia"}}

    def _dem(o_trong_ci, nen, rc_ban_in, neo=MOI_TRUONG_CI):
        no = {"gia_test.py": {**gia_no["gia_test.py"], "moi_truong": neo}}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            count = chay_moi(moi=gia_moi, cach_ly=no, chay_mot=lambda _p: rc_ban_in,
                             doc_moi_truong=lambda: nen, doc_trong_ci=lambda: o_trong_ci)
        return count, out.getvalue()

    # PHỦ TRỌN MIỀN ĐẾM, không vá lẻ từng ô. Hình dạng "tầng tiêu thụ hở một ô" đã
    # xuất hiện BA lần trong chính packet này: (1) khuyết tật gốc — trạng thái thứ ba
    # không được đếm; (2) finding P1 cross-review lượt 1 trên `dc72c16b` — nhánh
    # `chap_nhan is False` không ca nào đi qua `chay_moi`, đột biến `do += chap_nhan
    # is None and o_trong_ci` sống sót 27/27; (3) finding P1 lượt 2 trên `9ab5eb36` —
    # ô `(True, ngoài CI)` còn hở, đột biến sống sót 29/29. Cả ba đã tái lập được.
    # `PROTOCOL §12`: cùng hình dạng lần thứ BA thì phải xem lại CÁCH LÀM, không vá
    # lần thứ tư. Nên canh bằng BẢNG TRỌN MIỀN: 3 giá trị `chap_nhan` × 2 giá trị
    # `o_trong_ci` = 6 ô, mỗi ô một ca đi qua chính `chay_moi`. Thêm giá trị mới vào
    # miền mà quên ca thì bảng này hở lộ ra ngay, khác hẳn danh sách ca rời rạc.
    #
    # Cách dựng từng ô: `chap_nhan is None` cần nền KHÁC neo; `True` cần nền KHỚP neo
    # và bộ test ĐỎ (cách ly còn hiệu lực); `False` cần nền KHỚP neo và bộ test XANH
    # (đã hết nợ, phải đòi gỡ khỏi cách ly).
    MIEN_DEM = [(None, True, 1, "none-trong-ci"), (None, False, 0, "none-ngoai-ci"),
                (True, True, 0, "cach-ly-hop-le-trong-ci"), (True, False, 0, "cach-ly-hop-le-ngoai-ci"),
                (False, True, 1, "da-xanh-trong-ci"), (False, False, 1, "da-xanh-ngoai-ci")]
    for _cn, _ci, _mong, _o in MIEN_DEM:
        _nen = None if _cn is None else "github-actions/linux"
        _kq = (0, "1/1\n") if _cn is False else (1, "0/1\n")
        _them("r6-TIEU-THU-o-" + _o, _dem(_ci, _nen, _kq)[0] == _mong)
    known = _dem(True, MOI_TRUONG_WINDOWS, (1, "0/1\n"))
    unknown = _dem(True, "github-actions/macos", (1, "0/1\n"))
    windows = _dem(True, MOI_TRUONG_WINDOWS, (1, "0/1\n"), MOI_TRUONG_WINDOWS)
    _them("wp430-known-other-consumer", known[0] == 1 and "KHÔNG CÁCH LY" in known[1])
    _them("wp430-unknown-consumer", unknown[0] == 1 and "KHÔNG ĐO ĐƯỢC" in unknown[1])
    _them("wp430-windows-anchor-positive", windows[0] == 0 and "CÁCH LY" in windows[1])
    _them("wp430-unknown-predicate", cach_ly_chap_nhan(True, MOI_TRUONG_CI, "github-actions/macos") is None)
    # ── packet #456: SO DANG KY PHAN BIET DUOC NEN ────────────────────────────────────
    # Di qua chinh `chay_moi`, khong goi thang `mau_theo_nen`: khuyet tat "lam tron" nam o
    # NOI TIEU THU gia tri, va do la bai hoc r6/#401 da tra gia ba lan trong tep nay.
    # HAI CHIEU, khong phai mot: dong Windows tren Linux phai DO, VA dong Linux tren
    # Windows phai DAT (Windows do du bang tay thi khong duoc phat).
    _P456 = ".claude/hooks/pretooluse_guard_test.py"
    _WIN456 = ("TONG: CA 39/39 dat · DOT BIEN 34 muc KHONG DO TREN WINDOWS"
               " — do tren ubuntu-latest\nTONG: DAT\n")
    _LNX456 = "TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n"
    # `0/0 bi giet` = tap RONG thoa `not song` (#319). Tren WINDOWS phai DO — do la dot
    # bien bat buoc thu hai cua A2. Tren LINUX no VAN DUOC NHAN, y het base: lo #319 phia
    # Linux co san tu truoc, va bit no o day la doi hanh vi Linux — trai M4. Ca duoi khoa
    # ca hai chieu ay, ke ca chieu "van con lo", de khong ai vo tinh siet roi pha M4.
    _RONG456 = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"
    # Mau Linux NGUYEN BAN cua base — neo cung, khong doc tu `MOI` (doc tu `MOI` thi
    # sua `MOI` se keo ca ca test di theo, va ca test thanh guong soi chinh no).
    _MAU_BASE456 = (r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet"
                    r".*TONG: DAT")

    def _dem_nen(ban_in, la_windows):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            return chay_moi(moi={_P456: MOI[_P456]}, cach_ly={},
                            chay_mot=lambda _p: (0, ban_in),
                            doc_moi_truong=lambda: MOI_TRUONG_CI,
                            doc_trong_ci=lambda: True,
                            doc_nen_windows=lambda: la_windows)

    _them("p456-dong-windows-tren-linux-la-DO", _dem_nen(_WIN456, False) == 1)
    _them("p456-dong-windows-tren-windows-DAT", _dem_nen(_WIN456, True) == 0)
    _them("p456-dong-linux-tren-windows-DAT", _dem_nen(_LNX456, True) == 0)
    _them("p456-dong-linux-tren-linux-khong-doi", _dem_nen(_LNX456, False) == 0)
    _them("p456-dot-bien-0-tren-0-DO-tren-windows", _dem_nen(_RONG456, True) == 1)
    # M4: duong Linux phai giong BASE tung dau vao, ke ca dau vao xau.
    _them("p456-linux-nhan-0-tren-0-Y-HET-base", _dem_nen(_RONG456, False) == 0)
    _them("p456-mau-linux-KHONG-DOI-so-voi-base", MOI[_P456] == _MAU_BASE456)
    _them("p456-linux-A-B-tung-dau-vao-khop-base",
          all(bang_chung_xanh(x, MOI[_P456]) is bang_chung_xanh(x, _MAU_BASE456)
              for x in (_LNX456, _RONG456, _WIN456)))
    try:
        launcher_source = LAUNCHER_WORKFLOW.read_text(encoding="utf-8")
        ci_source = CI_WORKFLOW.read_text(encoding="utf-8")
    except OSError:
        launcher_source = ci_source = ""        # doc khong duoc = DO, khong phai bo qua
    _them("windows_311_launcher_workflow",
          bool(launcher_source) and giet_windows_311_launcher_workflow(launcher_source))
    _them("launcher-semantic-spacing", bool(launcher_source) and not loi_launcher_windows(
          launcher_source.replace("fromJSON(", "fromJSON( ", 1))[0])
    # Doi DUNG LOAI thong diep, khong phai `bool(loi)`: bo ghim lam CA ghim LAN probe do, nen ca
    # cu van xanh khi da XOA HAN chot ghim — do duoc 102/102 (luot 8, P2 #2).
    _them("ruff-pin-required", bool(ci_source) and any("ghim Ruff" in m for m in
          loi_ruff_ci(ci_source.replace("ruff==0.15.15", "ruff", 1))[0]))
    _them("ruff-version-probe-required", bool(ci_source) and any("probe Ruff" in m for m in
          loi_ruff_ci(ci_source.replace("ruff --version", "ruff --help", 1))[0]))
    # A7 #463 — fixture của đặc tả + ca biên; YAML tối thiểu dựng tại chỗ để ca không đổi màu
    # theo bố cục `ci.yml` hôm nay.
    _ruff = {"name": "cài Ruff 0.15.15 và in probe dương",
             "run": "python -m pip install --quiet ruff==0.15.15\nruff --version\n"}
    _reg = {"name": "test registry", "run": "python .claude/dev/ci_dang_ky_test.py --chay"}
    _khac = {"name": "khác", "run": "python x.py"}
    def _p(lenh): return {"name": "cài Ruff (biến thể)", "run": lenh + "\nruff --version\n"}
    _probe_truoc = {"name": "cài Ruff (probe trước)",  # probe dat TRUOC lenh cai
                    "run": "ruff --version\npython -m pip install --quiet ruff==0.15.15\n"}
    def _wf(jobs, env=None):
        d = {"on": "push", "jobs": jobs}
        if env: d["env"] = env
        return yaml.safe_dump(d, sort_keys=False)
    # Moi fixture la mot bo ba (ten, dau vao, ky vong) — xem chu thich F02 dau ham.
    _FX = [
        ("chua-tach-tuong-thich-lui", {"gate": {"steps": [_ruff, _khac, _reg]}}, None, 0),
        ("da-tach-dung", {"gate": {"steps": [_ruff, _khac]}, "gate-registry": {"steps": [_ruff, _reg]}}, None, 0),
        ("da-tach-thieu-ruff", {"gate": {"steps": [_ruff, _khac]}, "gate-registry": {"steps": [_khac, _reg]}}, None, 1),
        ("da-tach-ruff-sau-registry", {"gate": {"steps": [_ruff, _khac]}, "gate-registry": {"steps": [_reg, _ruff]}}, None, 1),
        ("khong-job-nao-chay-registry", {"gate": {"steps": [_ruff, _khac]}}, None, 1),
        ("hai-job-chay-registry", {"gate": {"steps": [_ruff, _reg]}, "gate-registry": {"steps": [_ruff, _reg]}}, None, 1),
        ("probe-truoc-cai", {"gate": {"steps": [_ruff, _khac]},   # THU TU trong cung than `run`
                             "gate-registry": {"steps": [_probe_truoc, _reg]}}, None, 1),
    ]
    # Chot env DA BO (chu kho 13-09, §12). Ca duoi la cua chot 1-3: probe TUONG DUONG argv + LEXER.
    _g = {"steps": [_ruff, _khac]}
    _pm = dict(_ruff, run="python -m pip install --quiet ruff==0.15.15\npython -m ruff --version\n")
    _pc = dict(_ruff, run="python -m pip install --quiet ruff==0.15.15\nruff   --version\n")
    _toml = dict(_ruff, run='python -m pip install --quiet ruff==0.15.15\nprintf "%s\\n" "[lint]\n'
                            'select = [\\"E\\"]  # chu thich" > ruff.toml\nruff --version\n')
    _nhay = dict(_ruff, run='python -m pip install --quiet ruff==0.15.15\necho "a ; b && c | d"\n'
                            'ruff --version\n')
    _tab = dict(_reg, run="python .claude/dev/ci_dang_ky_test.py\t--chay")
    _pmm = dict(_ruff, run="python -m pip install --quiet ruff==0.15.15\npython -mruff --version\n")
    _FX += [
        ("probe-dang-module", {"gate": _g, "gate-registry": {"steps": [_pm, _reg]}}, None, 0),
        ("probe-thua-khoang-trang", {"gate": _g, "gate-registry": {"steps": [_pc, _reg]}}, None, 0),
        ("toml-nhieu-dong-va-thang", {"gate": _g, "gate-registry": {"steps": [_toml, _reg]}}, None, 0),
        ("toan-tu-trong-dau-nhay", {"gate": _g, "gate-registry": {"steps": [_nhay, _reg]}}, None, 0),
        ("registry-ngan-bang-tab", {"gate": _g, "gate-registry": {"steps": [_ruff, _tab]}}, None, 0),
        ("probe-mruff-lien", {"gate": _g, "gate-registry": {"steps": [_pmm, _reg]}}, None, 0),
    ]
    # Bon ca `if:` do `_buoc_co_dieu_kien` o muc BUOC, khong phai lop phan loai. 19 ca phan
    # loai cu da CHUYEN xuong BANG NHAN (ky vong la DUNG NHAN, khong phai "co loi").
    for _t, _b in [("buoc-if-false", {"if": "false"}), ("if-so-khong", {"if": "0"}),
                   ("if-bieu-thuc-false", {"if": "${{false}}"}),
                   ("if-chi-linux", {"if": "runner.os == 'Linux'"})]:
        _FX.append((_t, {"gate": {"steps": [_ruff]},
                         "gate-registry": {"steps": [dict(_ruff, **_b), _reg]}}, None, 1))
    # BANG NHAN — doi DUNG nhan, khong chi doi "co loi": ky vong `_loi >= 1` cu de dot bien
    # doi KHONG_PHAN_TICH_DUOC thanh KHONG_GHIM van xanh (do duoc: `bo-chot-goi-khac` song).
    # Ky vong THO hon hanh vi no canh la lop loi rieng, bien the thu BA trong packet nay.
    _PIN = "python -m pip install ruff==0.15.15"
    _KPT = "KHONG_PHAN_TICH_DUOC"
    for _t, _run, _nhan in [
            # chieu NHAN — moi phan tu cua HAI danh sach CHO PHEP, cong cac cach viet hop le
            ("ghim-chuan", _PIN, "GHIM"),
            ("tien-to-pip", "pip install ruff==0.15.15", "GHIM"),
            ("tien-to-pip3", "pip3 install ruff==0.15.15", "GHIM"),
            ("tien-to-uv-pip", "uv pip install ruff==0.15.15", "GHIM"),
            ("tien-to-python3", "python3 -m pip install ruff==0.15.15", "GHIM"),
            ("tuy-chon-quiet", "python -m pip install --quiet ruff==0.15.15", "GHIM"),
            ("tuy-chon-q", "python -m pip install -q ruff==0.15.15", "GHIM"),
            ("tuy-chon-no-cache-dir", "python -m pip install --no-cache-dir ruff==0.15.15", "GHIM"),
            ("tuy-chon-disable-pip-version-check",
             "python -m pip install --disable-pip-version-check ruff==0.15.15", "GHIM"),
            ("tuy-chon-no-input", "python -m pip install --no-input ruff==0.15.15", "GHIM"),
            ("ten-hoa-thuong", "python -m pip install Ruff==0.15.15", "GHIM"),
            ("extras", "python -m pip install ruff[all]==0.15.15", "GHIM"),
            ("noi-dong", "python -m pip install \\\n  ruff==0.15.15", "GHIM"),
            ("chay-ruff-khong-phai-cai", "ruff check .", "KHONG"),
            ("chay-module", "python -m ruff --version", "KHONG"),
            ("chay-module-py3", "python3 -m ruff check .", "KHONG"),
            ("chay-uv-run", "uv run ruff --version", "KHONG"),
            ("chay-uvx", "uvx ruff check .", "KHONG"),
            ("chay-co-trinh-u", "python3 -u -m ruff --version", "KHONG"),
            ("chay-co-trinh-B", "python -B -m ruff check .", "KHONG"),
            ("chay-co-trinh-X", "python3 -X utf8 -m ruff --version", "KHONG"),
            ("chay-mruff-lien", "python3 -mruff --version", "KHONG"),
            ("ghep-toan-tu-va", _PIN + " && ruff --version", "GHIM"),
            ("ghep-toan-tu-cham-phay", _PIN + " ; ruff --version", "GHIM"),
            ("comment-khong-tinh", "# " + _PIN, "KHONG"),
            # chieu TU CHOI — nhan phai DUNG, khong chi "co loi"
            ("khong-ghim", "python -m pip install ruff", "KHONG_GHIM"),
            ("toan-tu-lon-hon", 'python -m pip install "ruff>=0.16"', "KHONG_GHIM"),
            ("toan-tu-la", 'python -m pip install "ruff<>0.16"', "KHONG_GHIM"),
            ("extras-khong-ghim", "python -m pip install ruff[all]", "KHONG_GHIM"),
            ("co-gan-bang", "python -m pip install --target=tmp ruff==0.15.15", _KPT),
            ("co-ngan-lien", "python -m pip install -ttmp ruff==0.15.15", _KPT),
            # `--target tmp` `--install-option=...` di CHUNG duong voi hai ca tren
            ("co-chua-biet", "python -m pip install --no-such-flag ruff==0.15.15", _KPT),
            ("cai-them-goi-khac", _PIN + " requests", _KPT),
            ("hai-ban-ruff", _PIN + ' "ruff>=0.16"', _KPT),
            ("go-cai", _PIN + "\npip uninstall -y ruff", _KPT),
            # mot ca dai dien: `pdm` `rye` `hatch` `apt-get` `poetry` nay di CHUNG mot duong
            # (khong khop khuon cai duoc cong nhan), nen giu nam ca la do lai mot thu nam lan
            ("trinh-ngoai-khuon", _PIN + "\npdm remove ruff", _KPT),
            ("upgrade-sau-ghim", _PIN + "\npython -m pip install --upgrade ruff", _KPT),
            ("tuy-chon-truoc-install", "python -m pip --quiet install ruff==0.15.15", _KPT)]:
        _them("nhan-" + _t, _phan_loai_cai_ruff(_run + "\nruff --version\n")[0] == _nhan)
    # Ky vong NEO DOC LAP cho hai danh sach CHO PHEP: bo mot phan tu lam cong CHAT hon nen
    # ca bat no la chieu NHAN o tren; chot nay bat chieu con lai — THEM phan tu ma quen ca.
    _them("tap-tien-to-khop-ky-vong", list(_TIEN_TO_CAI) == [
        ["pip"], ["pip3"], ["uv", "pip"], ["python", "-m", "pip"], ["python3", "-m", "pip"]])
    _them("tap-tuy-chon-khop-ky-vong", _TUY_CHON_AN_TOAN == {
        "--quiet", "-q", "--no-cache-dir", "--disable-pip-version-check", "--no-input"})
    for _ten, _jobs, _env, _mong in _FX:
        _loi = len(loi_ruff_ci(_wf(_jobs, _env))[0])
        _them("ruff-ci-" + _ten, (_loi == 0) if _mong == 0 else (_loi >= 1))
    # Bang ten KHONG con ton tai: 47 ten cu tung nam o day, cach cho sinh ket qua hang tram dong —
    # chinh nguon lech F02 to cao. Nay ten VA ket qua o CUNG mot `_them`, khong con `zip` de cat im.
    for ten, ok in KQ:
        print(f"ĐỘT BIẾN {ten}: {'ĐỎ đúng' if ok else 'LỌT'}")
    print(f"PHẢN CHỨNG: {sum(ok for _, ok in KQ)}/{len(KQ)} đỏ đúng")
    return all(ok for _, ok in KQ)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chay", action="store_true")
    ap.add_argument("--mutant", choices=("windows_311_launcher_workflow",))
    ns = ap.parse_args()
    if ns.mutant:
        killed = giet_windows_311_launcher_workflow(LAUNCHER_WORKFLOW.read_text(encoding="utf-8"))
        print(f"MUTANT {ns.mutant}: {'GIẾT' if killed else 'SỐNG'}")
        return 0 if killed else 1
    loi, tren_cay, trong_so = kiem()
    launcher_loi, launcher_chot = loi_launcher_windows()
    ruff_loi, ruff_chot = loi_ruff_ci()
    loi += launcher_loi
    loi += ruff_loi
    for x in loi: print("ĐỎ:", x)
    print(f"ĐĂNG KÝ: {tren_cay}/{trong_so}")
    print(f"TRẠNG THÁI: chan={trong_so - len(CACH_LY)} cach_ly={len(CACH_LY)}")
    print(f"LAUNCHER WINDOWS: {launcher_chot - len(launcher_loi)}/{launcher_chot} hợp đồng")
    print(f"RUFF CI: {ruff_chot - len(ruff_loi)}/{ruff_chot} hợp đồng")
    ok = not loi and tren_cay == trong_so and phan_chung()
    if ns.chay: ok = chay_moi() == 0 and ok
    print("TỔNG:", "ĐẠT" if ok else "ĐỎ")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
