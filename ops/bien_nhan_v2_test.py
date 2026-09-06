#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/bien_nhan_v2.py` — cổng lược đồ v2 của biên nhận review.

`PROTOCOL §8` đòi đúng hai thứ ở bộ kiểm, và cả hai có ca riêng ở đây:
  *"Bộ kiểm phải làm đỏ cả receipt mới tự khai v1 lẫn mutant nới allowlist để chứa tệp tấn công."*
  → `c2_bien_nhan_moi_tu_khai_v1` và `m1_noi_allowlist_chua_tep_tan_cong`.

BÁNH CÓC. `ALLOWLIST_CUTOVER` phải khớp TUYỆT ĐỐI 11 tên+băm đóng băng tại `2f84531`;
`NO_DA_DO` chỉ được CO LẠI — thêm tệp vào nợ là ĐỎ, bớt đi thì không. Hai luật ấy nằm ở
`c12`/`c13` và có đột biến riêng, vì một danh sách nới được trong im lặng thì không phải
danh sách đóng băng.

Khi commit cutover `2f84531` tra được, `c12` đo THÊM một tầng: đối chiếu allowlist với
`git ls-tree` THẬT thay vì với một hằng chép tay. Không tra được thì tầng ấy in KHÔNG ĐO
ĐƯỢC và **không** làm ca xanh lên: hằng đóng băng vẫn quyết định. Ba trạng thái, không phải hai.
(Bản đầu của dòng này viết "CI dùng `actions/checkout` mặc định depth 1" — SAI: `ci.yml:86`
đặt `fetch-depth: 0` từ `r226`. Cùng một tiền đề chưa đo đã lọt vào BỐN chỗ trong đợt này.)
"""
from __future__ import annotations

import copy
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC = HERE.parent
CONG = HERE / "bien_nhan_v2.py"

_spec = importlib.util.spec_from_file_location("bnv2", CONG)
bnv2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bnv2)

# --- Hằng ĐÓNG BĂNG của bánh cóc: chép TAY từ phép đo `git ls-tree -r 2f84531 -- ops/reviews/`
# (06-09-2026, 11 tệp, tất cả `schema_version: 1`, tất cả còn byte-identical với bản cutover).
# Nó nằm ở ĐÂY chứ không import từ cổng — một hằng tự đối chiếu với chính nó thì không canh gì.
ALLOWLIST_DONG_BANG = {
    "doctor-github-mcp-review-6-codex-verdict.receipt.yaml": "deeef9dc0054db2516ed88b32c8c4db47f7a72c75d15bac4a9cdb4803f40cabf",
    "doctor-github-mcp-review-9-codex-verdict.receipt.yaml": "039a2972c81bd9210f56ffd721b8694e5dfa8885b9841eebef94b41ab34377d8",
    "pr134-ci-lease-gate-codex-verdict.receipt.yaml": "c69347569b7dae133b997cb15b12f28ee962e97934ed2c15873805eec9373885",
    "tao-tag-luu-tru-review-1-codex-verdict.receipt.yaml": "39829e6b0489acc73c2a01bbb5c1997a20f9b9be6a2caea182048a767bfc707d",
    "wp55-r2-review-4-codex-verdict.receipt.yaml": "4081ec009292faa12563eb6b9df40b071e0c9345cae865fe6b766bef1a4ac0eb",
    "wp55-r2-review-5-codex-verdict.receipt.yaml": "ece195f31d3f9abdda57495cd32070d880b54583217f1c62ecaaa3c1b03c2537",
    "wp55-r4-review-1-codex-verdict.receipt.yaml": "b9f0f1d94d777ddda973b642815f5d9a457d9cb13f702009d4b12889649d70a5",
    "wp55-r4-review-2-codex-verdict.receipt.yaml": "dd4da1a3d85f17f5cdc5bf76951f30c657af182966ec8ea186f91c9a090732a4",
    "wp55-r4-review-di-tru-codex-verdict.receipt.yaml": "2758567db8e5f78bedcf27728859e092b6d76d242d550e0716d0ed8578c9f23b",
    "wp55-r4-review-rebase-codex-verdict.receipt.yaml": "9f80a5f69266e7509fe9a8c89bb5116f2848af12eaf1a5bf54dc7235d5e4da42",
    "wp55-r4-review-viet-lai-codex-verdict.receipt.yaml": "de439162c422439523a1b0acc08d9549d3e72be42cfe3f09e7bbec9dadde04ab",
}
CUTOVER = "2f84531"
# Trần của nợ tại lúc đóng băng. Bánh cóc: co được, nở thì ĐỎ (xem `NO_TRAN_DONG_BANG`).
NO_SO_LUONG_DONG_BANG = 42


class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` phát ra. Bài học `R5-01`: một `AssertionError` trần thì mã nào cũng dựng được."""


class LoiDungCa(Exception):
    """Giàn giáo hỏng — ca KHÔNG ĐO ĐƯỢC, KHÔNG được tính là chốt bắt được lỗi."""


_CA = None
CA = []


def bang(dk, msg):
    if not dk:
        ex = TinHieuChotCa(msg); ex.ca_nguon = _CA; raise ex


def dung(dk, msg):
    if not dk:
        raise LoiDungCa(msg)


def ca(fn):
    CA.append(fn); return fn


def v2_du():
    """Fixture ĐẠT v2 tối thiểu, dạng dict để đột biến được từng trường một."""
    return {
        "schema_version": 2,
        "receipt_id": "ca-thu-a",
        "reviewed_sha": "a" * 40,
        "verdict_path": "ops/reviews/a-verdict.md",
        "verdict_sha256": "b" * 64,
        # URL blob GHIM COMMIT: `c22` vừa bắt được chính fixture này khai
        # `canonical_ancestry` với một URL PR — mỏ neo tự khai mà phép đo không chạy.
        "evidence_url": "https://github.com/o/r/blob/" + "c" * 40 + "/ops/reviews/a-verdict.md",
        "model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_cli"},
        "github_submitter_identity": {"actor": "ducthangho"},
        "anchor": {"loai": "canonical_ancestry", "cuong_do": "trung_binh"},
    }


def _pha_anchor_cuong_do(d):
    d["anchor"]["cuong_do"] = ""


# MA TRẬN YÊU CẦU — chép từ `PROTOCOL §8` dòng 453-454, **KHÔNG import từ cổng**.
# Mỗi mục sinh ĐÚNG MỘT ca âm. Một oracle sinh từ chính module nó kiểm sẽ co theo mỗi lần
# cổng bị nới — kho này đã trả giá cho đúng hình dạng ấy hai lần trong cùng bộ test.
#
# VÌ SAO LÀ MA TRẬN, không phải thêm vài ca có tên: cross-review PR #455 (F2/P1) chạy được
# BA đột biến sản phẩm mà bộ test cũ KHÔNG bắt — gỡ `TRUONG_CO_MAT` · gỡ `cuong_do` khỏi
# `ANCHOR_KHOA` · gỡ `reviewed_sha` khỏi `TRUONG_VO_HUONG`; cả ba vẫn `15/15, 5/5`. Cùng
# một hình dạng: có ca âm cho VÀI trường, không có cho TỪNG trường. Vá từng tên ca là vá
# từng đột biến; ma trận là vá cái LỚP.
MA_TRAN = (
    ("schema_version",            lambda d: d.__setitem__("schema_version", 1),        "schema_version"),
    ("receipt_id",                lambda d: d.pop("receipt_id"),                       "receipt_id"),
    # SHA VIẾT TẮT — chính ca reviewer dựng: bản trước chỉ đòi "chuỗi không rỗng".
    ("reviewed_sha",              lambda d: d.__setitem__("reviewed_sha", "a" * 7),    "reviewed_sha"),
    ("verdict_path",              lambda d: d.pop("verdict_path"),                     "verdict_path"),
    ("verdict_sha256",            lambda d: d.__setitem__("verdict_sha256", "khong-phai-bam"), "verdict_sha256"),
    ("evidence_url",              lambda d: d.__setitem__("evidence_url", "http://e"), "evidence_url"),
    # Ánh xạ KHÔNG RỖNG nhưng RỖNG NGHĨA — bản trước nhận `{x: 1}` là "có identity".
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity", {"x": 1}), "model_reviewer_identity"),
    # `null` HỢP LỆ (có ca dương riêng); `"banana"` / `false` / `[]` thì không.
    ("github_submitter_identity", lambda d: d.__setitem__("github_submitter_identity", "banana"), "github_submitter_identity"),
    ("anchor",                    _pha_anchor_cuong_do,                                "anchor.cuong_do"),
)


def _cay(tmp: Path, tep: dict, la_kho_git=True):
    """Dựng một cây tối thiểu: `ops/reviews` + tuỳ chọn dấu `.git`."""
    tm = tmp / bnv2.THU_MUC
    tm.mkdir(parents=True, exist_ok=True)
    if la_kho_git:
        (tmp / ".git").mkdir(exist_ok=True)
    import yaml as _y
    for ten, than in tep.items():
        noi_dung = than if isinstance(than, str) else _y.safe_dump(than, allow_unicode=True)
        (tm / ten).write_text(noi_dung, encoding="utf-8")
    return tmp


def _kiem(tmp, **kw):
    """Trả (so_loi, danh_sach_loi) hoặc ném `bnv2.KhongDoDuoc`."""
    loi, _ = bnv2.kiem(tmp, **kw)
    return len(loi), loi


# ------------------------------------------------------------------ ca
@ca
def c1_kho_that_hien_tai_phai_SACH():
    """Nền: cổng phải XANH trên chính kho này, nếu không thì mọi ca dưới đo trong sương mù."""
    dung((GOC / bnv2.THU_MUC).is_dir(), f"KHÔNG ĐO ĐƯỢC: thiếu {GOC / bnv2.THU_MUC}")
    n, loi = _kiem(GOC)
    bang(n == 0, f"kho thật KHÔNG sạch — {n} vi phạm:\n  " + "\n  ".join(loi[:5]))


@ca
def c2_bien_nhan_moi_tu_khai_v1():
    """`PROTOCOL §8`: *'`schema_version: 1` do tác giả tệp mới tự khai KHÔNG tạo miễn trừ'*."""
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {"ke-gian-verdict.receipt.yaml": "schema_version: 1\nrole: reviewer\n"})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1, f"biên nhận mới tự khai v1 phải ĐỎ, được {n} vi phạm: {loi}")
        bang("schema_version=1" in loi[0], f"đỏ nhưng SAI LÝ DO: {loi[0]}")


@ca
def c4_v2_du_truong_phai_XANH():
    """ĐỐI CHỨNG DƯƠNG: một cổng đỏ MỌI THỨ cũng qua được mọi ca âm. Ca này chặn đúng bệnh đó."""
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": v2_du()})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"biên nhận v2 ĐỦ trường mà vẫn bị từ chối: {loi}")


@ca
def c4b_submitter_NULL_van_HOP_LE():
    """`null` là giá trị HỢP LỆ (protocol dòng 430: "<github actor or null when not published>").

    Ca này tồn tại để bản vá F2 không siết quá tay: reviewer cảnh báo thẳng *"Không bắt null
    thành lỗi chỉ để làm ca đỏ"*. VẮNG KHOÁ mới là lỗi — và đó là một mục của ma trận."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du(); d["github_submitter_identity"] = None
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"`github_submitter_identity: null` bị từ chối oan: {loi}")


@ca
def c4c_vang_khoa_submitter_thi_DO():
    with tempfile.TemporaryDirectory() as t:
        d = v2_du(); d.pop("github_submitter_identity")
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "github_submitter_identity" in loi[0],
             f"VẮNG khoá submitter phải ĐỎ (khác null), được: {loi}")


@ca
def c4d_assurance_vuot_bang_chung_doc_lap_thi_DO():
    """`F3`: biên nhận tự khai chạy bằng subagent trong phiên điều phối thì KHÔNG được khai
    một mức assurance hàm ý review có thẩm quyền."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["model_reviewer_identity"] = {"provider": "anthropic",
                                        "che_do": "subagent_trong_phien_dieu_phoi",
                                        "neo_boi_launcher": None}
        d["assurance"] = "same_provider_approved"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "review_deferred" in loi[0],
             f"assurance vượt bằng chứng phải ĐỎ, được: {loi}")
        d["assurance"] = "review_deferred"
        tmp2 = _cay(Path(t + "/x"), {"a-verdict.receipt.yaml": d})
        n2, loi2 = _kiem(tmp2, allowlist={}, no_da_do={})
        bang(n2 == 0, f"ĐỐI CHỨNG: `review_deferred` phải QUA, được: {loi2}")


@ca
def c5_sua_tep_trong_allowlist_thi_MAT_mien_tru():
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {"legacy-verdict.receipt.yaml": "schema_version: 1\nrole: reviewer\n"})
        n, loi = _kiem(tmp, allowlist={"legacy-verdict.receipt.yaml": "0" * 64}, no_da_do={})
        bang(n == 1 and "băm ĐÃ ĐỔI" in loi[0],
             f"tệp allowlist bị sửa phải ĐỎ vì băm lệch, được: {loi}")


@ca
def c6_sua_tep_trong_no_thi_DO():
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {"no-verdict.receipt.yaml": "schema_version: 1\nrole: reviewer\n"})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={"no-verdict.receipt.yaml": "0" * 64})
        bang(n == 1 and "NỢ ĐÃ ĐO mà băm ĐÃ ĐỔI" in loi[0],
             f"tệp nợ bị sửa phải ĐỎ, được: {loi}")


@ca
def c7_no_da_len_v2_ma_con_trong_danh_sach_no():
    """Bánh cóc quay một chiều: nâng xong thì phải GỠ khỏi `NO_DA_DO`, không để nó nằm lại."""
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": v2_du()})
        b = bnv2._bam(tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml")
        n, loi = _kiem(tmp, allowlist={}, no_da_do={"a-verdict.receipt.yaml": b})
        bang(n == 1 and "ĐÃ ĐẠT v2 mà vẫn nằm trong" in loi[0],
             f"tệp đã đạt v2 mà còn trong danh sách nợ phải ĐỎ, được: {loi}")


@ca
def c8_anchor_loai_ngoai_danh_sach_CHO_PHEP():
    """Danh sách CHO PHÉP, không phải danh sách cấm — bài học `v1.36.68`."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du(); d["anchor"]["loai"] = "canonical_ancestryy"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "ngoài danh sách CHO PHÉP" in loi[0],
             f"`anchor.loai` lạ phải ĐỎ, được: {loi}")


@ca
def c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong():
    """Ma trận phải phủ ĐÚNG tập yêu cầu của cổng — không thiếu, không thừa.

    Thêm một yêu cầu vào cổng mà quên ca âm ⇒ ĐỎ ở đây. Gỡ một yêu cầu khỏi cổng ⇒ cũng ĐỎ.
    Đây là chốt giữ cho ma trận không tụt lại phía sau lược đồ."""
    cua_cong = {k for k, _ in bnv2.YEU_CAU}
    cua_test = {ten for ten, _, _ in MA_TRAN}
    bang(cua_cong == cua_test,
         f"ma trận LỆCH tập yêu cầu của cổng.\n"
         f"      cổng có mà test thiếu ca âm: {sorted(cua_cong - cua_test)}\n"
         f"      test có mà cổng không đòi : {sorted(cua_test - cua_cong)}")


@ca
def c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am():
    """Phá ĐÚNG MỘT trường mỗi lần; mỗi lần phải ĐỎ, và ĐỎ ĐÚNG LÝ DO."""
    hong = []
    for ten, pha, phai_chua in MA_TRAN:
        with tempfile.TemporaryDirectory() as t:
            d = v2_du(); pha(d)
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            if n < 1:
                hong.append(f"{ten}: phá rồi mà cổng vẫn nhận")
            elif not any(phai_chua in x for x in loi):
                hong.append(f"{ten}: đỏ nhưng SAI LÝ DO (đòi chứa {phai_chua!r}): {loi[0][:110]}")
    bang(not hong, f"{len(hong)}/{len(MA_TRAN)} yêu cầu KHÔNG có ca âm hiệu lực:\n      "
                   + "\n      ".join(hong))


@ca
def c9_thieu_thu_muc_trong_kho_git_la_KHONG_DO_DUOC():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t); (tmp / ".git").mkdir()
        try:
            bnv2.kiem(tmp)
        except bnv2.KhongDoDuoc:
            return
        bang(False, "thiếu ops/reviews trong kho git mà cổng KHÔNG kêu — đó là 'sạch' giả")


@ca
def c10_thu_muc_RONG_la_KHONG_DO_DUOC():
    """Thư mục có mà 0 tệp = mốc neo đã đổi. 'Không thấy thì thôi' là cách một ca ĐẠT mà không ĐO."""
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {})
        try:
            bnv2.kiem(tmp)
        except bnv2.KhongDoDuoc:
            return
        bang(False, "thư mục biên nhận RỖNG mà cổng báo sạch")


@ca
def c11_yaml_hong_la_KHONG_DO_DUOC():
    with tempfile.TemporaryDirectory() as t:
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": "khong: [phai: yaml\n  - hop le\n"})
        try:
            bnv2.kiem(tmp, allowlist={}, no_da_do={})
        except bnv2.KhongDoDuoc:
            return
        bang(False, "YAML hỏng mà cổng không kêu KHÔNG ĐO ĐƯỢC")


@ca
def c12_allowlist_khop_TUYET_DOI_ban_dong_bang():
    """Bánh cóc tầng 1: cổng KHÔNG được nới allowlist. So với hằng chép tay ở tệp NÀY."""
    bang(bnv2.ALLOWLIST_CUTOVER == ALLOWLIST_DONG_BANG,
         f"`ALLOWLIST_CUTOVER` LỆCH bản đóng băng.\n"
         f"  thừa : {sorted(set(bnv2.ALLOWLIST_CUTOVER) - set(ALLOWLIST_DONG_BANG))}\n"
         f"  thiếu: {sorted(set(ALLOWLIST_DONG_BANG) - set(bnv2.ALLOWLIST_CUTOVER))}\n"
         f"  băm lệch: {sorted(k for k in set(bnv2.ALLOWLIST_CUTOVER) & set(ALLOWLIST_DONG_BANG) if bnv2.ALLOWLIST_CUTOVER[k] != ALLOWLIST_DONG_BANG[k])}")
    # Tầng 2 — đối chiếu với GIT THẬT khi commit cutover tra được. Clone nông (CI dùng
    # `actions/checkout` mặc định depth 1) thì KHÔNG tra được: in ra và đi tiếp, KHÔNG
    # đọc sự vắng mặt thành xác nhận.
    if not shutil.which("git") or not (GOC / ".git").exists():
        print("     (tầng git: KHÔNG ĐO ĐƯỢC — không có git hoặc không phải kho)"); return
    p = subprocess.run(["git", "-C", str(GOC), "ls-tree", "-r", "--name-only", CUTOVER,
                        "--", "ops/reviews/"], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"     (tầng git: KHÔNG ĐO ĐƯỢC — `{CUTOVER}` không tra được, clone nông?)"); return
    ten = {Path(x).name for x in p.stdout.split() if x.endswith(".receipt.yaml")}
    bang(ten == set(ALLOWLIST_DONG_BANG),
         f"allowlist KHÔNG khớp `git ls-tree {CUTOVER}`: thừa {sorted(set(ALLOWLIST_DONG_BANG) - ten)}, "
         f"thiếu {sorted(ten - set(ALLOWLIST_DONG_BANG))}")
    print(f"     (tầng git: khớp `git ls-tree {CUTOVER}` — {len(ten)} tệp)")


@ca
def c13_no_chi_duoc_CO_LAI_va_KHONG_DUOC_DOI_BAM():
    """Bánh cóc tầng 2 — so CẶP tên→băm, không so tập tên.

    Bản trước chỉ so tập TÊN và cross-review chạy được phản chứng: đổi nội dung một tệp nợ
    rồi cập nhật băm trong `NO_DA_DO` ⇒ mọi thứ vẫn xanh. Nay mỗi cặp còn lại phải khớp
    baseline; muốn hợp thức hoá một thay đổi thì phải NÂNG receipt lên v2 rồi GỠ mục nợ,
    chứ không được rebase băm."""
    thua = sorted(set(bnv2.NO_DA_DO) - set(NO_DONG_BANG))
    bang(not thua,
         f"`NO_DA_DO` ĐÃ NỞ thêm {len(thua)} tệp: {thua[:5]} — biên nhận MỚI phải đạt v2, "
         f"không được đóng băng thành nợ.")
    lech = sorted(k for k in set(bnv2.NO_DA_DO) & set(NO_DONG_BANG)
                  if bnv2.NO_DA_DO[k] != NO_DONG_BANG[k])
    bang(not lech,
         f"{len(lech)} mục nợ ĐỔI BĂM so baseline: {lech[:3]}\n"
         f"      Đổi băm = tái đóng băng một bản KHÔNG ĐẠT v2. Đường đúng: nâng receipt lên "
         f"v2 rồi GỠ nó khỏi `NO_DA_DO`, không rebase baseline.")


def _kho_git(tmp: Path, than_verdict: str):
    """Dựng một kho git THẬT tối thiểu, commit một tệp verdict, trả (sha, băm, đường dẫn)."""
    duong = "ops/reviews/x-verdict.md"
    (tmp / "ops" / "reviews").mkdir(parents=True, exist_ok=True)
    (tmp / duong).write_text(than_verdict, encoding="utf-8")
    E = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
         "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", ""),
         "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    def g(*a):
        r = subprocess.run(["git", "-C", str(tmp), *a], capture_output=True, text=True, env=E)
        dung(r.returncode == 0, f"git {' '.join(a)} hỏng: {r.stderr[:200]}")
        return r.stdout.strip()
    g("init", "-q"); g("add", "-A"); g("commit", "-qm", "x")
    sha = g("rev-parse", "HEAD")
    import hashlib as _h
    return sha, _h.sha256((tmp / duong).read_bytes()).hexdigest(), duong


def _bn_neo(sha, bam, duong):
    d = v2_du()
    d["reviewed_sha"] = sha
    d["verdict_sha256"] = bam
    d["verdict_path"] = duong
    d["evidence_url"] = f"https://github.com/o/r/blob/{sha}/{duong}"
    return d


@ca
def c18_neo_git_DUNG_thi_qua():
    """ĐỐI CHỨNG DƯƠNG cho `_neo_git`: commit thật, đường dẫn thật, blob khớp băm ⇒ sạch."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
        import yaml as _y
        (tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").write_text(
            _y.safe_dump(_bn_neo(sha, bam, duong), allow_unicode=True), encoding="utf-8")
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"mỏ neo git ĐÚNG mà vẫn bị từ chối: {loi}")


@ca
def c19_neo_git_SAI_DUONG_DAN_thi_DO():
    """Commit CÓ THẬT nhưng không chứa đường dẫn ⇒ mỏ neo trỏ hụt ⇒ ĐỎ (không phải KHÔNG ĐO ĐƯỢC)."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_neo(sha, bam, duong)
        d["evidence_url"] = f"https://github.com/o/r/blob/{sha}/ops/reviews/KHONG-HE-CO.md"
        import yaml as _y
        (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
        (tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").write_text(
            _y.safe_dump(d, allow_unicode=True), encoding="utf-8")
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "trỏ hụt" in loi[0], f"đường dẫn không có trong commit phải ĐỎ: {loi}")


@ca
def c20_neo_git_BAM_LECH_thi_DO():
    """Blob có thật nhưng băm khác `verdict_sha256` ⇒ mỏ neo không trỏ đúng thứ nó khai."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_neo(sha, "abcdef01" * 8, duong)   # hình dạng HỢP LỆ, giá trị SAI
        import yaml as _y
        (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
        (tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").write_text(
            _y.safe_dump(d, allow_unicode=True), encoding="utf-8")
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "KHÔNG trỏ đúng thứ nó khai" in loi[0],
             f"băm blob lệch phải ĐỎ (và phải qua được chốt hình dạng trước): {loi}")


@ca
def c22_canonical_ancestry_ma_URL_khong_ghim_thi_DO():
    """Lỗ TỰ TÌM: khai một loại mỏ neo mà cổng đo được, rồi đưa URL khiến phép đo KHÔNG chạy.

    Trước bản vá, `anchor.loai: canonical_ancestry` + `evidence_url` là URL PR ⇒ `_neo_git`
    lặng lẽ bỏ qua và cổng in "sạch". Cùng lớp với ba P1 của lượt này: thứ cổng KHÔNG đo được
    thì phải ĐỎ, không được im."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()                       # anchor.loai = canonical_ancestry
        d["evidence_url"] = "https://github.com/o/r/pull/1"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "KHÔNG đo được" in loi[0],
             f"canonical_ancestry mà URL không ghim commit phải ĐỎ, được: {loi}")


@ca
def c21_object_khong_tra_duoc_la_KHONG_DO_DUOC_chu_khong_phai_DO():
    """SHA đúng hình dạng mà object không có ⇒ trạng thái THỨ BA.

    Reviewer nói thẳng: *"Thiếu lịch sử không phải bằng chứng giả mạo."* Ca này giữ cho bản
    vá F4 không lật sang thái cực kia — clone nông sẽ làm cổng đỏ oan hàng loạt."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_neo(sha, bam, duong)
        d["reviewed_sha"] = "deadbeef" * 5          # 40 hex, KHÔNG tồn tại
        import yaml as _y
        (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
        (tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").write_text(
            _y.safe_dump(d, allow_unicode=True), encoding="utf-8")
        loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
        bang(not loi, f"object vắng KHÔNG được thành vi phạm: {loi}")
        bang(any("KHÔNG ĐO ĐƯỢC" in x and "reviewed_sha" in x for x in tk["chua_do"]),
             f"object vắng phải vào danh sách KHÔNG ĐO ĐƯỢC, được: {tk['chua_do']}")


@ca
def c14_cli_ba_trang_thai():
    """Mã thoát CLI phải là 0/1/2 đúng ba trạng thái — đọc rc TRỰC TIẾP, không qua pipeline."""
    r = subprocess.run([sys.executable, str(CONG), "--root", str(GOC)],
                       capture_output=True, text=True)
    bang(r.returncode == bnv2.RC_SACH, f"kho thật: đòi rc=0, được {r.returncode}\n{r.stderr[:400]}")
    bang("TỔNG: ĐẠT" in r.stdout, f"rc=0 mà KHÔNG có bằng chứng dương trong stdout: {r.stdout[-300:]!r}")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t); (tmp / ".git").mkdir()
        r2 = subprocess.run([sys.executable, str(CONG), "--root", str(tmp)],
                            capture_output=True, text=True)
        bang(r2.returncode == bnv2.RC_KHONG_DO_DUOC,
             f"kho git thiếu ops/reviews: đòi rc=2, được {r2.returncode}")


# Bản ĐÓNG BĂNG của NỢ — **TÊN + BĂM**, chép cứng, KHÔNG import từ cổng.
#
# Hai lần sai liên tiếp ở đúng chỗ này, và lần sau tinh vi hơn lần trước:
#   (1) bản nháp lấy `frozenset(bnv2.NO_DA_DO)` lúc nạp ⇒ oracle TỰ NỞ theo mã nguồn;
#   (2) bản sửa chép cứng nhưng chỉ chép **TÊN** ⇒ vẫn thủng. Cross-review PR #455 (F1/P1)
#       chạy được phản chứng: sửa một biên nhận nợ RỒI cập nhật băm tương ứng trong
#       `NO_DA_DO` — tập tên và số lượng không đổi — kết quả **rc=0, 15/15 ca, 5/5 đột biến
#       CÓ RĂNG**, tức đã tái đóng băng một bản KHÔNG ĐẠT v2 mà không cổng nào kêu.
# Nên baseline phải là CẶP tên→băm. Bánh cóc: `NO_DA_DO` là TẬP CON của bảng dưới đây —
# bỏ mục thì được (đã nâng lên v2), thêm mục hoặc ĐỔI BĂM thì ĐỎ.
NO_DONG_BANG = {
    "bien-nhan-review-s2-review-4-codex-verdict.receipt.yaml":
        "1d1382fb95c209135b8afdbd21a1f602b25328125c2bde8d7c44d129d0ce310f",
    "don-nhanh-base-review-1-codex-verdict.receipt.yaml":
        "bff5e1157fff1a5eda7e425447316976797bcf3703f4f332d0d983f1ec2e53e7",
    "don-nhanh-base-review-2-codex-verdict.receipt.yaml":
        "6295f6057994c606342501ff15cfc6c597f0d403dd966caa3f68c938c918f48a",
    "don-nhanh-base-review-3-claude-verdict.receipt.yaml":
        "602bfc18184d747fd7047fc2efe7d7666d7e02d76fa061ba8b87b8999db2f8f3",
    "don-nhanh-base-review-4-claude-verdict.receipt.yaml":
        "8772712513fa1e491c51526d6a5f0f17d4fc04b0234abb397ae1cd39d132b4e8",
    "don-nhanh-base-review-5-claude-verdict.receipt.yaml":
        "3acb2723a9228666828cc4b321a5fdb2ae192001b66db7c2527a7cdabacec169",
    "don-nhanh-base-review-6-claude-verdict.receipt.yaml":
        "b2e53792c3f945d2e00b5bfc64ed4d6b944762b54ac54353021f67f4f192b587",
    "don-nhanh-base-review-7-claude-verdict.receipt.yaml":
        "7309ab38967838c357100d58ec7a4c86e293fbdd75e81d3e0d4600d22eeb62e5",
    "don-nhanh-kien-truc-gh-1-claude-verdict.receipt.yaml":
        "1f40ee7f6f9b8b17645fef417eccb5777d4f56b49bc3994f065874f2401c9929",
    "donref-xoa-an-toan-review-1-claude-verdict.receipt.yaml":
        "183ec46e1a4cae22a822eefffb95b547f89b7b42c50ec49645d4b5817e3cb744",
    "donref-xoa-an-toan-review-2-claude-verdict.receipt.yaml":
        "28d45ad88e7c3fdc53cab7777f08ace054574c1c6963ec9fcbee8f79b28f34b9",
    "lease-dang-review-1-claude-verdict.receipt.yaml":
        "336755b5fc58c659c535db2e80e724d535f0ceddeb7bac9af4b02102aabfc9f2",
    "lease-dang-review-2-claude-verdict.receipt.yaml":
        "1ea14266d6771759d4721ec0df42bfc6bdd5086e0c4b12693b08c5f853a9c492",
    "lease-dang-review-3-claude-verdict.receipt.yaml":
        "c5775d68f5adf782e1fd792e27b31310856fa67b44926a17f96b9ab9793de73b",
    "lease-dang-review-4-claude-verdict.receipt.yaml":
        "1fa4c33c1744398857658efb0c75f62256f20a64914063f2fb896594df03a078",
    "lease-dang-review-5-claude-verdict.receipt.yaml":
        "dc53836df18f1adf21c59eca73f5aaba692b7ccdc2bc311d74c7ab690da9a028",
    "lease-dang-windows-review-1-claude-verdict.receipt.yaml":
        "9bdd49f4786a23abe67c63ec76c1c8ada9ab18418f03e6fe9513bc16c62d3c7a",
    "lease-dang-windows-review-2-claude-verdict.receipt.yaml":
        "29d3a1a6cb2c46c579f8c224f0874d5f55982afd5a13eba5e50cc871f6fda1d2",
    "lease-dang-windows-review-3-claude-verdict.receipt.yaml":
        "9959343169eb84d4d5b56a3e4ad7611f11db771833d7476284532eb27e862fbd",
    "lease-hoi-toan-kho-review-1-claude-verdict.receipt.yaml":
        "806dbee61c92f89c1a13827d478d5fc4f15ae1e54cd1b2e149ca970b61f7ffe3",
    "lease-hoi-toan-kho-review-2-claude-verdict.receipt.yaml":
        "190a45befd1bd97635c833300ce921d0f4aa06973451f5ac35fceb7f93eda96a",
    "lease-hoi-toan-kho-review-3-claude-verdict.receipt.yaml":
        "a277fb86fc07574593a504f72cb480d9a3d70e2dd0af9511858de64e92151a22",
    "n5-lenh-hook-windows-review-1-codex-verdict.receipt.yaml":
        "82a8664137c0a7b21657479f3db83d6ec147bb37900028b7483c0dc152fdbf31",
    "n5-lenh-hook-windows-review-2-codex-verdict.receipt.yaml":
        "34ca3e907f1fc61a5b8091eded528b3b2fdecf5f85670af9716e1e0fc61166d4",
    "plat-m4-human-audit-ducthangho-verdict.receipt.yaml":
        "b2b147d63f789d91cbfa0a37b5b431b0d4bdec9672ef74e651185b190f383b94",
    "plat-m4-review-1-codex-verdict.receipt.yaml":
        "d0961cb5584914143fa7657f12f348410df9310f3db3d5cba8ae80e50dcf8ecf",
    "plat-m4-review-2-codex-verdict.receipt.yaml":
        "0ac82afcac4dcb92a8a8d7449b6db05c2d9fe033af44d846561043a0582a6b0c",
    "plat-m4-review-3-claude-verdict.receipt.yaml":
        "c5d34d6e432565d8728e753cf9160a4292a118c8dbfc8d0fd24767d33c14a111",
    "plat-x5-review-1-claude-verdict.receipt.yaml":
        "6c19926d05151ba93a71d00dc804642110de8d95f5f8430c590c5037af03269e",
    "plat-x5-review-2-claude-verdict.receipt.yaml":
        "76244daf71981e3c96f3ee842c87d01995883a0747104cfa23163714fe82f818",
    "plat-x5-review-3-claude-verdict.receipt.yaml":
        "2221a079fd4887a0b4717bc1f90d868eddf35aba16488765126dfc27fa3e1408",
    "plat-x8-review-1-claude-verdict.receipt.yaml":
        "8bc0d299881a3ef99ab6c0d96264834c0e1f25af0a9854eb23e60b5382898ef4",
    "plat-x8-review-2-claude-verdict.receipt.yaml":
        "bfa4d9cad30d8e7f36cbb7064489506f4563e50452cc1952409415f856e11207",
    "plat-x8-review-3-claude-verdict.receipt.yaml":
        "c2db6b7600192431cfe74bb3f817b356495bc56247da82442a5dcf820f2641cd",
    "slice-b-c-human-audit-ducthangho-verdict.receipt.yaml":
        "9e76b60472adc90910fbcaff79cb34af73b5c03ee64c552ec71be5364a40d2a7",
    "slice-b-c-review-1-codex-verdict.receipt.yaml":
        "d80cfec7ff64edbe927b07c5105418c4f0382a3eb60e53f22d7effa7570c7192",
    "slice-b-c-review-2-codex-verdict.receipt.yaml":
        "662e6d798278ca40309eb0231fb02b540f63ea5d1f24ddb1b4cb6b3e554290fd",
    "t33-doi-shellcheck-review-1-codex-verdict.receipt.yaml":
        "71eefab1e94a1c0dd071d7418723fcd590cf86feb003a945ca7ef95830e11f23",
    "t33-doi-shellcheck-review-2-codex-verdict.receipt.yaml":
        "6152d0ff2a3b95c98b27dd2dba7e3ffaddb3b3ae27328d29ced3249fec4e088d",
    "t33-doi-shellcheck-review-3-codex-verdict.receipt.yaml":
        "8dcae1dd59624a96502cb92d4b5f6a83b8db789d56d2c935af6d94c2adaa675c",
    "t33-doi-shellcheck-review-4-codex-verdict.receipt.yaml":
        "a829125a652be52e0a93a6f0874cb64a9327d09c1505557693874f7636485513",
    "tri-thuc-review-1-codex-verdict.receipt.yaml":
        "49acb2c1a52c00d25751fdff4a6b77aa453232222bda9d90f5a488c8980b1f8f",
}


def _chay_1(fn):
    global _CA
    _CA = fn.__name__
    try:
        fn(); return "qua", None
    except LoiDungCa as ex:
        return "gian_giao", str(ex)
    except TinHieuChotCa as ex:
        return ("giet_that" if getattr(ex, "ca_nguon", None) == fn.__name__
                else "tin_dung_gia"), str(ex)
    except Exception as ex:                                       # noqa: BLE001
        return "tin_dung_gia", f"{type(ex).__name__}: {ex}"
    finally:
        _CA = None


# ------------------------------------------------------------------ đột biến
def _dot_bien():
    """Mỗi đột biến phải làm ĐÚNG ca đích ĐỎ. Không đỏ ⇒ ca ấy rỗng."""
    ra = []

    def do(ten, sua, ca_dich, mo_ta):
        # BẢN SAO SÂU, không phải tham chiếu: đột biến dưới đây sửa TẠI CHỖ
        # (`dict.__setitem__`), nên `setattr` lại chính object đã bẩn thì khôi phục ĐƯỢC SỐ
        # KHÔNG — và mọi ca chạy sau sẽ đo trên một cổng đã bị nới. Đúng bài học "đột biến
        # ghi vào tệp THẬT rồi khôi phục" của kho, chỉ đổi tệp thành object.
        cu = {k: copy.deepcopy(getattr(bnv2, k))
              for k in ("ALLOWLIST_CUTOVER", "NO_DA_DO", "YEU_CAU",
                        "ANCHOR_LOAI_CHO_PHEP", "ANCHOR_KHOA", "_HEX40",
                        "_HEX64", "_BLOB_URL", "_blob_khop")}
        sua()
        try:
            fn = next(f for f in CA if f.__name__ == ca_dich)
            tt, ct = _chay_1(fn)
        finally:
            for k, v in cu.items():
                setattr(bnv2, k, v)
        ok = tt == "giet_that"
        ra.append((ten, ca_dich, ok, tt, ((ct or "").splitlines() or [""])[0][:80]))
        print(f"  {'CÓ RĂNG ' if ok else 'KHÔNG RĂNG'} {ten:38s} → {ca_dich} = {tt}  ({mo_ta})")

    do("m1_noi_allowlist_chua_tep_tan_cong",
       lambda: bnv2.ALLOWLIST_CUTOVER.__setitem__("ke-gian-verdict.receipt.yaml", "0" * 64),
       "c12_allowlist_khop_TUYET_DOI_ban_dong_bang", "PROTOCOL đòi ĐÚNG ca này")
    do("m2_no_lon_them_mot_tep",
       lambda: bnv2.NO_DA_DO.__setitem__("ke-gian-verdict.receipt.yaml", "0" * 64),
       "c13_no_chi_duoc_CO_LAI_va_KHONG_DUOC_DOI_BAM", "bánh cóc quay ngược")
    # ĐỘT BIẾN CỦA CHÍNH FINDING F1: đổi băm baseline mà KHÔNG đổi tập tên. Bản test trước
    # chỉ đóng băng TÊN nên đột biến này SỐNG SÓT — nó là phản chứng của reviewer, dựng lại
    # ở đây để bản vá có răng đo được chứ không phải lời hứa.
    do("m2b_no_DOI_BAM_giu_nguyen_ten",
       lambda: bnv2.NO_DA_DO.__setitem__(sorted(bnv2.NO_DA_DO)[0], "0" * 64),
       "c13_no_chi_duoc_CO_LAI_va_KHONG_DUOC_DOI_BAM", "tái đóng băng một bản không đạt")
    do("m3_bo_doi_model_identity",
       lambda: setattr(bnv2, "YEU_CAU", tuple(x for x in bnv2.YEU_CAU
                                              if x[0] != "model_reviewer_identity")),
       "c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong", "gỡ một yêu cầu khỏi cổng")
    do("m3b_bo_doi_submitter_identity",
       lambda: setattr(bnv2, "YEU_CAU", tuple(x for x in bnv2.YEU_CAU
                                              if x[0] != "github_submitter_identity")),
       "c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong",
       "đúng đột biến reviewer chạy được mà bản cũ KHÔNG bắt")
    do("m3c_bo_doi_reviewed_sha",
       lambda: setattr(bnv2, "YEU_CAU", tuple(x for x in bnv2.YEU_CAU
                                              if x[0] != "reviewed_sha")),
       "c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong", "đột biến reviewer chạy được, bản cũ mù")
    do("m4_noi_anchor_chua_ten_tan_cong",
       lambda: setattr(bnv2, "ANCHOR_LOAI_CHO_PHEP",
                       bnv2.ANCHOR_LOAI_CHO_PHEP | {"canonical_ancestryy"}),
       "c8_anchor_loai_ngoai_danh_sach_CHO_PHEP", "danh sách cho phép bị nới")
    do("m5_reviewed_sha_nhan_SHA_VIET_TAT",
       lambda: setattr(bnv2, "_HEX40", __import__("re").compile(r"\A[0-9a-f]{7,40}\Z")),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am",
       "đúng ca reviewer dựng: SHA 7 ký tự phải ĐỎ")
    do("m7_bo_hoan_toan_phep_do_MO_NEO_GIT",
       lambda: setattr(bnv2, "_BLOB_URL", __import__("re").compile(r"\\AKHONG_KHOP_GI\\Z")),
       "c19_neo_git_SAI_DUONG_DAN_thi_DO", "gỡ phép đo mỏ neo ⇒ trỏ hụt lọt")
    # Bản đầu của m8 nhắm `_HEX64` vào `c17` và KHÔNG CÓ RĂNG: nới chốt hình dạng không
    # làm ca ma trận đỏ vì fixture ấy không mang mỏ neo blob. Đột biến đo số không thì phải
    # sửa cho đúng đích, không phải bỏ đi — nay nó nhắm thẳng phép so băm blob.
    do("m9_cho_canonical_ancestry_dung_URL_khong_ghim",
       lambda: setattr(bnv2, "_BLOB_URL", __import__("re").compile(r"\\A(?:.*)\\Z")),
       "c19_neo_git_SAI_DUONG_DAN_thi_DO", "nới dạng URL ⇒ phép đo trỏ hụt")
    do("m8_neo_git_khong_so_bam_blob",
       lambda: setattr(bnv2, "_blob_khop", lambda a, b: True),
       "c20_neo_git_BAM_LECH_thi_DO", "cổng thôi so băm blob")
    do("m6_bo_kiem_cuong_do_cua_anchor",
       lambda: setattr(bnv2, "ANCHOR_KHOA", ("loai",)),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am", "đột biến reviewer chạy được, bản cũ mù")
    return ra


def main() -> int:
    print(f"bien_nhan_v2_test — {len(CA)} ca\n")
    hong = []
    for fn in CA:
        tt, ct = _chay_1(fn)
        if tt == "qua":
            print(f"  ĐẠT   {fn.__name__}")
        else:
            hong.append((fn.__name__, tt, ct))
            print(f"  {'ĐỎ' if tt == 'giet_that' else 'KHÔNG ĐO ĐƯỢC'}  {fn.__name__} [{tt}]: {ct}")
    print("\nĐỘT BIẾN (mỗi cái phải làm ĐÚNG ca đích đỏ):")
    db = _dot_bien()
    khong_rang = [x for x in db if not x[2]]
    print(f"\nbien_nhan_v2_test: {len(CA) - len(hong)}/{len(CA)} ca đạt · "
          f"{len(db) - len(khong_rang)}/{len(db)} đột biến CÓ RĂNG")
    if hong or khong_rang:
        print("TỔNG: ĐỎ")
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
