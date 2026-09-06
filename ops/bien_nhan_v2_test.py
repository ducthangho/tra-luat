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
`git ls-tree` THẬT thay vì với một hằng chép tay. Không tra được (clone nông — CI dùng
`actions/checkout` mặc định depth 1) thì tầng ấy in KHÔNG ĐO ĐƯỢC và **không** làm ca xanh
lên: hằng đóng băng vẫn quyết định. Đó là ba trạng thái, không phải hai.
"""
from __future__ import annotations

import copy
import importlib.util
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


V2_DU = """schema_version: 2
receipt_id: ca-thu-{ten}
kind: review_delivery_receipt
role: reviewer
reviewed_sha: {sha}
verdict: approve
verdict_path: ops/reviews/{ten}-verdict.md
verdict_sha256: {bam}
evidence_url: https://github.com/ducthangho/tra-luat/pull/1
model_reviewer_identity:
  provider: openai_codex
  surface: codex_cli
github_submitter_identity:
  actor: ducthangho
anchor:
  loai: {loai}
  cuong_do: trung_binh
"""


def _cay(tmp: Path, tep: dict, la_kho_git=True):
    """Dựng một cây tối thiểu: `ops/reviews` + tuỳ chọn dấu `.git`."""
    tm = tmp / bnv2.THU_MUC
    tm.mkdir(parents=True, exist_ok=True)
    if la_kho_git:
        (tmp / ".git").mkdir(exist_ok=True)
    for ten, than in tep.items():
        (tm / ten).write_text(than, encoding="utf-8")
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
def c3_v2_thieu_identity():
    with tempfile.TemporaryDirectory() as t:
        than = V2_DU.format(ten="a", sha="a" * 40, bam="b" * 64, loai="canonical_ancestry")
        than = than.replace("model_reviewer_identity:\n  provider: openai_codex\n  surface: codex_cli\n", "")
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": than})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "model_reviewer_identity" in loi[0],
             f"thiếu `model_reviewer_identity` phải ĐỎ đúng lý do, được: {loi}")


@ca
def c4_v2_du_truong_phai_XANH():
    """ĐỐI CHỨNG DƯƠNG: cổng đỏ MỌI THỨ cũng qua được c2/c3. Ca này chặn đúng bệnh đó."""
    with tempfile.TemporaryDirectory() as t:
        than = V2_DU.format(ten="a", sha="a" * 40, bam="b" * 64, loai="canonical_ancestry")
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": than})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"biên nhận v2 ĐỦ trường mà vẫn bị từ chối: {loi}")


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
        than = V2_DU.format(ten="a", sha="a" * 40, bam="b" * 64, loai="canonical_ancestry")
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": than})
        b = bnv2._bam(tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml")
        n, loi = _kiem(tmp, allowlist={}, no_da_do={"a-verdict.receipt.yaml": b})
        bang(n == 1 and "ĐÃ ĐẠT v2 mà vẫn nằm trong" in loi[0],
             f"tệp đã đạt v2 mà còn trong danh sách nợ phải ĐỎ, được: {loi}")


@ca
def c8_anchor_loai_ngoai_danh_sach_CHO_PHEP():
    """Danh sách CHO PHÉP, không phải danh sách cấm — bài học `v1.36.68`."""
    with tempfile.TemporaryDirectory() as t:
        than = V2_DU.format(ten="a", sha="a" * 40, bam="b" * 64, loai="canonical_ancestryy")
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": than})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "ngoài danh sách CHO PHÉP" in loi[0],
             f"`anchor.loai` lạ phải ĐỎ, được: {loi}")


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
def c13_no_chi_duoc_CO_LAI():
    """Bánh cóc tầng 2: `NO_DA_DO` là TẬP CON của bản đóng băng. Co được; nở là ĐỎ."""
    thua = sorted(set(bnv2.NO_DA_DO) - NO_TRAN_DONG_BANG)
    bang(not thua,
         f"`NO_DA_DO` ĐÃ NỞ thêm {len(thua)} tệp: {thua[:5]}\n"
         f"      Bánh cóc chỉ quay một chiều: biên nhận MỚI phải đạt v2, không được đóng băng "
         f"thành nợ. Muốn thêm thật thì phải sửa CẢ hằng ở tệp test này, và đó là chủ ý có dấu vết.")
    bang(len(bnv2.NO_DA_DO) <= NO_SO_LUONG_DONG_BANG,
         f"số nợ {len(bnv2.NO_DA_DO)} > trần đóng băng {NO_SO_LUONG_DONG_BANG}")


@ca
def c15_v2_thieu_receipt_id():
    """`PROTOCOL §8` liệt kê "receipt ID" trong đích v2 tối thiểu — có ca riêng cho nó.

    Bản nháp đầu KHÔNG có ca này và nhắm đột biến `m5` vào `c1`: bỏ đòi `receipt_id` mà `c1`
    vẫn XANH, vì 42 tệp nợ hỏng ở NHIỀU chỗ nên gỡ một đòi hỏi không lật nổi tệp nào. Một
    đột biến không giết được ca nào thì nó đo số không — và ca đích sai làm nó TRÔNG như
    cổng thiếu răng."""
    with tempfile.TemporaryDirectory() as t:
        than = V2_DU.format(ten="a", sha="a" * 40, bam="b" * 64, loai="canonical_ancestry")
        than = than.replace("receipt_id: ca-thu-a\n", "")
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": than})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "receipt_id" in loi[0],
             f"thiếu `receipt_id` phải ĐỎ đúng lý do, được: {loi}")


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


# Bản ĐÓNG BĂNG của NỢ — chép TÊN vào ĐÂY, KHÔNG import từ cổng.
# Bản nháp đầu lấy `frozenset(bnv2.NO_DA_DO)` lúc nạp: nó CÓ răng với đột biến chạy
# (m2 sửa module lúc chạy) nhưng MÙ HOÀN TOÀN với việc ai đó thêm một tệp vào
# `NO_DA_DO` trong MÃ NGUỒN — lúc ấy 'bản đóng băng' tự nở theo. Đúng bệnh mà chính
# chú thích của `ALLOWLIST_DONG_BANG` vừa tố cáo, tái phát cách nó ba chục dòng.
NO_TRAN_DONG_BANG = frozenset({
    "bien-nhan-review-s2-review-4-codex-verdict.receipt.yaml",
    "don-nhanh-base-review-1-codex-verdict.receipt.yaml",
    "don-nhanh-base-review-2-codex-verdict.receipt.yaml",
    "don-nhanh-base-review-3-claude-verdict.receipt.yaml",
    "don-nhanh-base-review-4-claude-verdict.receipt.yaml",
    "don-nhanh-base-review-5-claude-verdict.receipt.yaml",
    "don-nhanh-base-review-6-claude-verdict.receipt.yaml",
    "don-nhanh-base-review-7-claude-verdict.receipt.yaml",
    "don-nhanh-kien-truc-gh-1-claude-verdict.receipt.yaml",
    "donref-xoa-an-toan-review-1-claude-verdict.receipt.yaml",
    "donref-xoa-an-toan-review-2-claude-verdict.receipt.yaml",
    "lease-dang-review-1-claude-verdict.receipt.yaml",
    "lease-dang-review-2-claude-verdict.receipt.yaml",
    "lease-dang-review-3-claude-verdict.receipt.yaml",
    "lease-dang-review-4-claude-verdict.receipt.yaml",
    "lease-dang-review-5-claude-verdict.receipt.yaml",
    "lease-dang-windows-review-1-claude-verdict.receipt.yaml",
    "lease-dang-windows-review-2-claude-verdict.receipt.yaml",
    "lease-dang-windows-review-3-claude-verdict.receipt.yaml",
    "lease-hoi-toan-kho-review-1-claude-verdict.receipt.yaml",
    "lease-hoi-toan-kho-review-2-claude-verdict.receipt.yaml",
    "lease-hoi-toan-kho-review-3-claude-verdict.receipt.yaml",
    "n5-lenh-hook-windows-review-1-codex-verdict.receipt.yaml",
    "n5-lenh-hook-windows-review-2-codex-verdict.receipt.yaml",
    "plat-m4-human-audit-ducthangho-verdict.receipt.yaml",
    "plat-m4-review-1-codex-verdict.receipt.yaml",
    "plat-m4-review-2-codex-verdict.receipt.yaml",
    "plat-m4-review-3-claude-verdict.receipt.yaml",
    "plat-x5-review-1-claude-verdict.receipt.yaml",
    "plat-x5-review-2-claude-verdict.receipt.yaml",
    "plat-x5-review-3-claude-verdict.receipt.yaml",
    "plat-x8-review-1-claude-verdict.receipt.yaml",
    "plat-x8-review-2-claude-verdict.receipt.yaml",
    "plat-x8-review-3-claude-verdict.receipt.yaml",
    "slice-b-c-human-audit-ducthangho-verdict.receipt.yaml",
    "slice-b-c-review-1-codex-verdict.receipt.yaml",
    "slice-b-c-review-2-codex-verdict.receipt.yaml",
    "t33-doi-shellcheck-review-1-codex-verdict.receipt.yaml",
    "t33-doi-shellcheck-review-2-codex-verdict.receipt.yaml",
    "t33-doi-shellcheck-review-3-codex-verdict.receipt.yaml",
    "t33-doi-shellcheck-review-4-codex-verdict.receipt.yaml",
    "tri-thuc-review-1-codex-verdict.receipt.yaml",
})


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
              for k in ("ALLOWLIST_CUTOVER", "NO_DA_DO", "TRUONG_ANH_XA",
                        "ANCHOR_LOAI_CHO_PHEP", "TRUONG_VO_HUONG")}
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
       "c12_allowlist_khop_TUYET_DOI_ban_dong_bang",
       "PROTOCOL đòi ĐÚNG ca này")
    do("m2_no_lon_them_mot_tep",
       lambda: bnv2.NO_DA_DO.__setitem__("ke-gian-verdict.receipt.yaml", "0" * 64),
       "c13_no_chi_duoc_CO_LAI", "bánh cóc quay ngược")
    do("m3_bo_doi_hai_identity",
       lambda: setattr(bnv2, "TRUONG_ANH_XA", ("anchor",)),
       "c3_v2_thieu_identity", "cổng thôi đòi identity")
    # NỚI danh sách cho phép để chứa ĐÚNG tên tấn công — đây là hình dạng doctrine đòi
    # (`v1.36.68`), và bản nháp đầu đặt sai chiều: `frozenset()` RỖNG vẫn làm chốt đỏ nên
    # ca đích vẫn xanh, tức đột biến ấy đo số không.
    do("m4_noi_anchor_chua_ten_tan_cong",
       lambda: setattr(bnv2, "ANCHOR_LOAI_CHO_PHEP",
                       bnv2.ANCHOR_LOAI_CHO_PHEP | {"canonical_ancestryy"}),
       "c8_anchor_loai_ngoai_danh_sach_CHO_PHEP", "danh sách cho phép bị nới")
    do("m5_bo_doi_receipt_id",
       lambda: setattr(bnv2, "TRUONG_VO_HUONG", ("reviewed_sha", "verdict_path",
                                                 "verdict_sha256", "evidence_url")),
       "c15_v2_thieu_receipt_id", "cổng thôi đòi receipt ID")
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
    print(f"\nĐỘT BIẾN ({5} cái, mỗi cái phải làm ĐÚNG ca đích đỏ):")
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
