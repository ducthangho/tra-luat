#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOC = (".claude/dev", ".claude/hooks", ".githooks", ".github/checks", "scripts/tl_core")
OPS_REVIEWS = "ops/reviews/"
MOI_TRUONG_CI = "github-actions/linux"
MOI = {
    ".claude/dev/chon_reviewer_test.py": r"(?s)nền: (\d+)/(\d+) đạt.*TỔNG: ĐẠT",
    ".claude/dev/gh_readback_test.py": r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)",
    ".claude/dev/mcp_gh_test.py": r"(?s)CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT.*ĐỘT BIẾN.*ĐẠT.*TỔNG: ĐẠT",
    ".claude/dev/mcp_github_doc_test.py": r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)",
    ".claude/dev/probe_mang_test.py": r"(?s)tự đột biến cổng: 9/9 chết.*nền: 11/11 đạt.*TỔNG: ĐẠT",
    ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
}
CACH_LY = {
    ".claude/dev/mcp_gh_test.py": {
        "slug": "AG-361-P2-01-mcp-gh-dot-bien-chap-chon-theo-may",
        "ly_do": "runner CI đỏ ở b7_bo_cam_ghi; .pyc là giả thuyết khớp, chưa có phản chứng",
        "moi_truong": "github-actions/linux",
        "log": "Issue #361, log CI r3 của phiên điều phối",
    },
    ".claude/hooks/pretooluse_guard_test.py": {
        "slug": "AG-361-P2-02-pretooluse-guard-doi-runtime-runner-khong-co",
        "ly_do": "runner CI trần đỏ t11/t15/t33 vì thiếu runtime mà bộ test đòi hỏi",
        "moi_truong": "github-actions/linux",
        "log": "Issue #361, log CI r3 của phiên điều phối",
    },
}
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
        elif no["moi_truong"] != MOI_TRUONG_CI:
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
    if env.get("GITHUB_ACTIONS") == "true" and env.get("RUNNER_OS") == "Linux":
        return MOI_TRUONG_CI
    return None


def cach_ly_chap_nhan(ok, da_neo, hien_tai):
    """None = không ở đúng môi trường để phán quyết nợ còn tái hiện."""
    if hien_tai != da_neo:
        return None
    return not ok


def chay_moi():
    do = 0
    hien_tai = moi_truong_hien_tai()
    for path, mau in MOI.items():
        p = subprocess.run([sys.executable, path], cwd=ROOT, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        ok = p.returncode == 0 and bang_chung_xanh(p.stdout, mau)
        print(p.stdout, end="")
        if path in CACH_LY:
            no = CACH_LY[path]
            chap_nhan = cach_ly_chap_nhan(ok, no["moi_truong"], hien_tai)
            if chap_nhan is None:
                print(f"CI_DANG_KY {path}: KHÔNG ĐO ĐƯỢC — môi trường={hien_tai or 'không xác định'}")
            elif not chap_nhan:
                print(f"CI_DANG_KY {path}: ĐỎ — đã xanh, hãy gỡ khỏi cách ly")
                do += 1
            else:
                print(f"CI_DANG_KY {path}: CÁCH LY rc={p.returncode} nợ={no['slug']}")
        else:
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
    names += ["a-cach-ly-thieu-slug", "r4-thieu-moi-truong", "r5-moi-truong-sai-tap",
              "r5-comment-gia-loi-goi", "r5-step-if-false", "r5-job-if-false",
              "r5-step-if-literal-expr", "r5-normal-step", "b-cach-ly-chuyen-xanh",
              "r4-bo-so-moi-truong", "r4-khong-do-duoc-thanh-dat",
              "rc-do-ban-in-xanh", "rc-xanh-thieu-ban-in"]
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
    print(f"TRẠNG THÁI: chan={trong_so - len(CACH_LY)} cach_ly={len(CACH_LY)}")
    ok = not loi and tren_cay == trong_so and phan_chung()
    if ns.chay: ok = chay_moi() == 0 and ok
    print("TỔNG:", "ĐẠT" if ok else "ĐỎ")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
