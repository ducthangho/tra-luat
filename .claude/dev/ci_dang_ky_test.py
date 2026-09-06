#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import contextlib
import io
import json
import os
import pathlib
import re
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
    # `[1-9]\d*` HAI VE, khong phai `\d+`: mau cu nhan ca `DOT BIEN 0/0 bi giet` —
    # dung hinh dang "tap RONG thoa `not song`" ma bai hoc #319 sinh ra de chan.
    # `bang_chung_xanh` chi soi HAI nhom CA nen no khong bao gio nhin toi cap so dot
    # bien; chot ay phai nam trong CHINH mau, khong o dau khac.
    ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d*/[1-9]\d* bi giet.*TONG: DAT",
    ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
}
# Mau CHI duoc chap nhan khi nen dang chay la Windows. Day la mot nua cua phan chung
# A3: dua dong Windows vao mot luot chay tren Linux phai DO; nua kia la dong Linux
# tren nen Windows van phai DAT (ai do chay tay do du thi khong duoc phat).
MOI_WINDOWS = {
    ".claude/hooks/pretooluse_guard_test.py":
        r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS"
        r".*TONG: DAT",
}
CACH_LY = {}
DA_NOI = {
    ".claude/dev/ci_dang_ky_test.py",
    ".claude/dev/duyet_danh_tinh_test.py",
    ".claude/dev/codex_cred_test.py", ".claude/dev/gate_lifecycle_test.py",
    ".claude/dev/idiom_py_test.py", ".claude/dev/launcher_test.py",
    ".claude/dev/packet_loop_test.py", ".githooks/eol_policy_test.py",
    ".githooks/pre_push_test.py", ".github/checks/ci_phamvi_test.py",
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


def loi_ruff_ci(source=None):
    source = CI_WORKFLOW.read_text(encoding="utf-8") if source is None else source
    try:
        data = yaml.safe_load(source) or {}
    except yaml.YAMLError as e:
        return [f"CI YAML lỗi khi kiểm Ruff: {e}"], 1
    steps = (((data.get("jobs") or {}).get("gate") or {}).get("steps") or [])
    runs = [s.get("run", "") for s in steps if isinstance(s, dict)]
    joined = "\n".join(x for x in runs if isinstance(x, str))
    ruff_i = next((i for i, x in enumerate(runs) if "ruff==0.15.15" in x), -1)
    gate_i = next((i for i, x in enumerate(runs)
                   if "ci_dang_ky_test.py --chay" in x), -1)
    checks = [
        ("ruff==0.15.15" in joined, "CI không ghim Ruff 0.15.15"),
        (bool(re.search(r"(?m)^\s*ruff --version\s*$", joined)),
         "CI không in probe Ruff --version"),
        (0 <= ruff_i < gate_i, "CI không provision Ruff trước test registry"),
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

    Windows nhan CA HAI dong: dong Windows (da cat dot bien) VA dong Linux (ai do chay
    tay do du thi van dat). Nen khac chi nhan dong goc — dua dong Windows vao Linux la DO.
    """
    mau_nen = MOI_WINDOWS.get(path)
    return [mau, mau_nen] if (la_windows and mau_nen) else [mau]


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
    cases, names = [], ["i-thieu-so", "ii-mat-tep", "iii-mat-loi-goi", "iv-vi-tri-la"]
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
                cases.append(bool(kiem(r, reg, wf)[0]))
            finally:
                DA_NOI.clear(); DA_NOI.update(old)
        # (a) Bản sao sổ cách ly mất slug phải đỏ.
        mutant_cu = {".claude/dev/a_test.py": {"slug": "", "ly_do": "đỏ trên CI"}}
        cases.append(bool(kiem(r, reg, wf, mutant_cu)[0]))
        mutant = {".claude/dev/a_test.py": {"slug": "nợ", "ly_do": "đỏ trên CI",
                                                "log": "log-r3"}}
        cases.append(bool(kiem(r, reg, wf, mutant)[0]))
        # r5: neo môi trường ngoài đúng nguồn giá trị phải đỏ ở tầng cấu trúc.
        mutant = {".claude/dev/a_test.py": {"slug": "nợ", "ly_do": "đỏ trên CI",
                    "moi_truong": "github-actions/lin-typo", "log": "log-r3"}}
        cases.append(any("môi trường không hợp lệ" in x for x in kiem(r, reg, wf, mutant)[0]))
        # r5: xoá run thật, giữ nguyên lệnh trong YAML comment vẫn phải đỏ.
        yml = r / ".github/workflows/comment.yml"
        yml.write_text("jobs:\n  x:\n    steps:\n      # - run: python .claude/dev/a_test.py\n", encoding="utf-8")
        old = set(DA_NOI); DA_NOI.clear(); DA_NOI.add(".claude/dev/a_test.py")
        try: cases.append(any("CI không gọi mục" in x for x in kiem(r, reg)[0]))
        finally: DA_NOI.clear(); DA_NOI.update(old)
        old = set(DA_NOI); DA_NOI.clear(); DA_NOI.add(".claude/dev/a_test.py")
        for level in ("step", "job", "expr", "normal"):
            yml.write_text("jobs:\n  x:\n" + ("    if: false\n" if level == "job" else "") + "    steps:\n      - " + (("if: ${{ false }}\n        " if level == "expr" else "if: false\n        ") if level in ("step", "expr") else "") + "run: python .claude/dev/a_test.py\n", encoding="utf-8")
            found = any("CI không gọi mục" in x for x in kiem(r, reg)[0]); cases.append(found if level != "normal" else not found)
        DA_NOI.clear(); DA_NOI.update(old)
        # (b) Bản sao chương trình cách ly chuyển xanh phải bị yêu cầu gỡ.
        green = base / "green_test.py"
        green.write_text("print('1/1')\n", encoding="utf-8")
        p = subprocess.run([sys.executable, green], text=True, stdout=subprocess.PIPE)
        xanh = p.returncode == 0 and bang_chung_xanh(p.stdout, r"^(\d+)/(\d+)$")
        cases.append(not cach_ly_chap_nhan(xanh, "github-actions/linux", "github-actions/linux"))
        # r4: bỏ phép so làm bản xanh bắn ở môi trường khác; đúng ra phải là None.
        cases.append((not xanh) is not cach_ly_chap_nhan(xanh, "github-actions/linux", None))
        # r4: đột biến đổi trạng thái thứ ba thành ĐẠT phải bị bắt.
        cases.append(cach_ly_chap_nhan(xanh, "github-actions/linux", None) is None and True is not None)
    # Hai chiều bằng chứng: rc đỏ dù có dòng xanh; rc xanh nhưng thiếu dòng xanh.
    cases += [not (1 == 0 and bang_chung_xanh("TỔNG: ĐẠT", r"TỔNG: ĐẠT")),
              not (0 == 0 and bang_chung_xanh("", r"TỔNG: ĐẠT"))]
    # r6 (#401): VỊ TỪ trung thực rồi mà NƠI TIÊU THỤ vẫn làm tròn lên được — đó là
    # khuyết tật đã sống sót qua r4 và r5. Nên canh cả hai tầng.
    cases += [dem_la_do(None, True) is True, dem_la_do(None, False) is False,
              dem_la_do(False, False) is True, dem_la_do(True, True) is False]
    # r6: `trong_ci` phải ĐỘC LẬP với `moi_truong_hien_tai` — thiếu RUNNER_OS vẫn là CI,
    # còn không có GITHUB_ACTIONS thì dù có RUNNER_OS vẫn KHÔNG phải CI.
    cases += [trong_ci({"GITHUB_ACTIONS": "true"}) is True,
              trong_ci({"RUNNER_OS": "Linux"}) is False,
              trong_ci({"GITHUB_ACTIONS": "false", "RUNNER_OS": "Linux"}) is False]
    cases += [moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "Linux"}) == MOI_TRUONG_CI,
              moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "Windows"}) == MOI_TRUONG_WINDOWS,
              moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "macOS"}) is None,
              cach_ly_chap_nhan(True, MOI_TRUONG_CI, MOI_TRUONG_WINDOWS) is True,
              cach_ly_chap_nhan(False, MOI_TRUONG_CI, MOI_TRUONG_WINDOWS) is False]
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
    MIEN_DEM = [(None, True, 1), (None, False, 0),
                (True, True, 0), (True, False, 0),
                (False, True, 1), (False, False, 1)]
    for _cn, _ci, _mong in MIEN_DEM:
        _nen = None if _cn is None else "github-actions/linux"
        _kq = (0, "1/1\n") if _cn is False else (1, "0/1\n")
        cases.append(_dem(_ci, _nen, _kq)[0] == _mong)
    known = _dem(True, MOI_TRUONG_WINDOWS, (1, "0/1\n"))
    unknown = _dem(True, "github-actions/macos", (1, "0/1\n"))
    windows = _dem(True, MOI_TRUONG_WINDOWS, (1, "0/1\n"), MOI_TRUONG_WINDOWS)
    cases += [known[0] == 1 and "KHÔNG CÁCH LY" in known[1],
              unknown[0] == 1 and "KHÔNG ĐO ĐƯỢC" in unknown[1],
              windows[0] == 0 and "CÁCH LY" in windows[1],
              cach_ly_chap_nhan(True, MOI_TRUONG_CI, "github-actions/macos") is None]
    # ── packet #456: SO DANG KY PHAN BIET DUOC NEN ────────────────────────────────────
    # Di qua chinh `chay_moi`, khong goi thang `mau_theo_nen`: khuyet tat "lam tron" nam o
    # NOI TIEU THU gia tri, va do la bai hoc r6/#401 da tra gia ba lan trong tep nay.
    # HAI CHIEU, khong phai mot: dong Windows tren Linux phai DO, VA dong Linux tren
    # Windows phai DAT (Windows do du bang tay thi khong duoc phat).
    _P456 = ".claude/hooks/pretooluse_guard_test.py"
    _WIN456 = ("TONG: CA 39/39 dat · DOT BIEN 34 muc KHONG DO TREN WINDOWS"
               " — do tren ubuntu-latest\nTONG: DAT\n")
    _LNX456 = "TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n"
    # `0/0 bi giet` = tap RONG thoa `not song` (#319). Phai DO tren MOI nen.
    _RONG456 = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"

    def _dem_nen(ban_in, la_windows):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            return chay_moi(moi={_P456: MOI[_P456]}, cach_ly={},
                            chay_mot=lambda _p: (0, ban_in),
                            doc_moi_truong=lambda: MOI_TRUONG_CI,
                            doc_trong_ci=lambda: True,
                            doc_nen_windows=lambda: la_windows)

    cases += [_dem_nen(_WIN456, False) == 1, _dem_nen(_WIN456, True) == 0,
              _dem_nen(_LNX456, True) == 0, _dem_nen(_LNX456, False) == 0,
              _dem_nen(_RONG456, False) == 1, _dem_nen(_RONG456, True) == 1]
    try:
        launcher_source = LAUNCHER_WORKFLOW.read_text(encoding="utf-8")
        cases.append(giet_windows_311_launcher_workflow(launcher_source))
        cases.append(not loi_launcher_windows(
            launcher_source.replace("fromJSON(", "fromJSON( ", 1))[0])
        ci_source = CI_WORKFLOW.read_text(encoding="utf-8")
        cases += [bool(loi_ruff_ci(
                      ci_source.replace("ruff==0.15.15", "ruff", 1))[0]),
                  bool(loi_ruff_ci(
                      ci_source.replace("ruff --version", "ruff --help", 1))[0])]
    except OSError:
        cases += [False, False, False, False]
    names += ["a-cach-ly-thieu-slug", "r4-thieu-moi-truong", "r5-moi-truong-sai-tap",
              "r5-comment-gia-loi-goi", "r5-step-if-false", "r5-job-if-false",
              "r5-step-if-literal-expr", "r5-normal-step", "b-cach-ly-chuyen-xanh",
              "r4-bo-so-moi-truong", "r4-khong-do-duoc-thanh-dat",
              "rc-do-ban-in-xanh", "rc-xanh-thieu-ban-in",
              "r6-vi-tu-none-trong-ci-la-do", "r6-vi-tu-none-ngoai-ci-khong-do",
              "r6-vi-tu-da-xanh-van-do", "r6-vi-tu-cach-ly-hop-le-khong-do",
              "r6-trong-ci-khong-doi-runner-os", "r6-thieu-github-actions-khong-phai-ci",
              "r6-github-actions-false-khong-phai-ci",
              "wp430-nhan-linux", "wp430-nhan-windows", "wp430-runner-la-fail-close",
              "wp430-windows-xanh-that", "wp430-windows-do-that",
              "r6-TIEU-THU-o-none-trong-ci", "r6-TIEU-THU-o-none-ngoai-ci",
              "r6-TIEU-THU-o-cach-ly-hop-le-trong-ci",
               "r6-TIEU-THU-o-cach-ly-hop-le-ngoai-ci",
               "r6-TIEU-THU-o-da-xanh-trong-ci", "r6-TIEU-THU-o-da-xanh-ngoai-ci",
               "wp430-known-other-consumer", "wp430-unknown-consumer",
               "wp430-windows-anchor-positive", "wp430-unknown-predicate",
              "p456-dong-windows-tren-linux-la-DO",
              "p456-dong-windows-tren-windows-DAT",
              "p456-dong-linux-tren-windows-DAT",
              "p456-dong-linux-tren-linux-khong-doi",
              "p456-dot-bien-0-tren-0-DO-tren-linux",
              "p456-dot-bien-0-tren-0-DO-ca-tren-windows",
               "windows_311_launcher_workflow", "launcher-semantic-spacing",
               "ruff-pin-required", "ruff-version-probe-required"]
    for name, ok in zip(names, cases): print(f"ĐỘT BIẾN {name}: {'ĐỎ đúng' if ok else 'LỌT'}")
    print(f"PHẢN CHỨNG: {sum(cases)}/{len(cases)} đỏ đúng")
    return all(cases)


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
