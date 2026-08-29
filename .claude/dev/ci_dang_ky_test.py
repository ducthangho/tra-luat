#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import contextlib
import io
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
    p = subprocess.run([sys.executable, path], cwd=ROOT, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return p.returncode, p.stdout


def chay_moi(moi=MOI, cach_ly=CACH_LY, chay_mot=_chay_that,
             doc_moi_truong=moi_truong_hien_tai, doc_trong_ci=trong_ci):
    """Bốn tham số sau là ĐƯỜNG NỐI ĐỂ ĐO, không phải cấu hình: phản chứng phải gọi
    được chính hàm này với bộ chạy giả, nếu không tầng tiêu thụ lại không ai canh."""
    do = 0
    hien_tai = doc_moi_truong()
    o_trong_ci = doc_trong_ci()
    for path, mau in moi.items():
        rc, ban_in = chay_mot(path)
        ok = rc == 0 and bang_chung_xanh(ban_in, mau)
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
    # r6: TẦNG TIÊU THỤ — gọi chính `chay_moi` với bộ chạy giả. Gỡ phép cộng ở đó ra thì
    # ba ca này ĐỎ; đó là điều mà đột biến canh-vị-từ `r4-khong-do-duoc-thanh-dat` KHÔNG
    # bắt được, và là lý do nợ N6 lọt cổng trên windows-latest.
    gia_moi = {"gia_test.py": r"^(\d+)/(\d+)$"}
    gia_no = {"gia_test.py": {"slug": "gia", "ly_do": "gia",
                              "moi_truong": "github-actions/linux", "log": "gia"}}

    def _dem(o_trong_ci, nen, rc_ban_in):
        with contextlib.redirect_stdout(io.StringIO()):
            return chay_moi(moi=gia_moi, cach_ly=gia_no, chay_mot=lambda _p: rc_ban_in,
                            doc_moi_truong=lambda: nen, doc_trong_ci=lambda: o_trong_ci)

    # Hai ca cuối phủ nhánh `chap_nhan is False` (bộ cách ly ĐÃ XANH) đi qua chính
    # `chay_moi`. Thiếu chúng thì đột biến TỪNG PHẦN `do += chap_nhan is None and
    # o_trong_ci` sống sót cả 27 ca — finding P1 của cross-review codex trên
    # `dc72c16b`, đã tái lập: đột biến ấy cho rc=0. Bảo chứng tầng tiêu thụ phải phủ
    # MỌI nhánh đếm, không chỉ nhánh trạng thái thứ ba.
    cases += [_dem(True, None, (1, "0/1\n")) == 1,
              _dem(False, None, (1, "0/1\n")) == 0,
              _dem(True, "github-actions/linux", (1, "0/1\n")) == 0,
              _dem(True, "github-actions/linux", (0, "1/1\n")) == 1,
              _dem(False, "github-actions/linux", (0, "1/1\n")) == 1]
    names += ["a-cach-ly-thieu-slug", "r4-thieu-moi-truong", "r5-moi-truong-sai-tap",
              "r5-comment-gia-loi-goi", "r5-step-if-false", "r5-job-if-false",
              "r5-step-if-literal-expr", "r5-normal-step", "b-cach-ly-chuyen-xanh",
              "r4-bo-so-moi-truong", "r4-khong-do-duoc-thanh-dat",
              "rc-do-ban-in-xanh", "rc-xanh-thieu-ban-in",
              "r6-vi-tu-none-trong-ci-la-do", "r6-vi-tu-none-ngoai-ci-khong-do",
              "r6-vi-tu-da-xanh-van-do", "r6-vi-tu-cach-ly-hop-le-khong-do",
              "r6-trong-ci-khong-doi-runner-os", "r6-thieu-github-actions-khong-phai-ci",
              "r6-github-actions-false-khong-phai-ci",
              "r6-TIEU-THU-trong-ci-phai-dem", "r6-TIEU-THU-ngoai-ci-khong-dem",
              "r6-TIEU-THU-nen-khop-neo-van-cach-ly",
              "r6-TIEU-THU-cach-ly-da-xanh-phai-dem",
              "r6-TIEU-THU-da-xanh-dem-ca-ngoai-ci"]
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
