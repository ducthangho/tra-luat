#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOC = (".claude/dev", ".claude/hooks", ".githooks", ".github/checks", "scripts/tl_core")
OPS_REVIEWS = "ops/reviews/"
MOI = {
    ".claude/dev/gh_readback_test.py": r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)",
    ".claude/dev/mcp_gh_test.py": r"(?s)CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT.*ĐỘT BIẾN.*ĐẠT.*TỔNG: ĐẠT",
    ".claude/dev/mcp_github_doc_test.py": r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)",
    ".claude/dev/probe_mang_test.py": r"(?s)tự đột biến cổng: 9/9 chết.*nền: 11/11 đạt.*TỔNG: ĐẠT",
    ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
}
DA_NOI = {
    ".claude/dev/ci_dang_ky_test.py",
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


def kiem(root=ROOT, registry=DANG_KY, workflows=None):
    song, _, la = tim(root)
    loi = []
    loi += ["test sống chưa đăng ký: " + x for x in sorted(song - registry)]
    loi += ["mục đăng ký không có tệp: " + x for x in sorted(registry - song)]
    loi += ["test ở vị trí chưa biết: " + x for x in sorted(la)]
    if workflows is None:
        workflows = "\n".join(p.read_text(encoding="utf-8") for p in (root / ".github/workflows").glob("*.yml"))
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


def chay_moi():
    do = 0
    for path, mau in MOI.items():
        p = subprocess.run([sys.executable, path], cwd=ROOT, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        ok = p.returncode == 0 and bang_chung_xanh(p.stdout, mau)
        print(p.stdout, end="")
        print(f"CI_DANG_KY {path}: {'ĐẠT' if ok else 'ĐỎ'} rc={p.returncode}")
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
    # Hai chiều bằng chứng: rc đỏ dù có dòng xanh; rc xanh nhưng thiếu dòng xanh.
    cases += [not (1 == 0 and bang_chung_xanh("TỔNG: ĐẠT", r"TỔNG: ĐẠT")),
              not (0 == 0 and bang_chung_xanh("", r"TỔNG: ĐẠT"))]
    names += ["rc-do-ban-in-xanh", "rc-xanh-thieu-ban-in"]
    for name, ok in zip(names, cases): print(f"ĐỘT BIẾN {name}: {'ĐỎ đúng' if ok else 'LỌT'}")
    print(f"PHẢN CHỨNG: {sum(cases)}/{len(cases)} đỏ đúng")
    return all(cases)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chay", action="store_true")
    ns = ap.parse_args()
    loi, tren_cay, trong_so = kiem()
    for x in loi: print("ĐỎ:", x)
    print(f"ĐĂNG KÝ: {tren_cay}/{trong_so}")
    ok = not loi and tren_cay == trong_so and phan_chung()
    if ns.chay: ok = chay_moi() == 0 and ok
    print("TỔNG:", "ĐẠT" if ok else "ĐỎ")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
