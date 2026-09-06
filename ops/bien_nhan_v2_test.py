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


# Module THẬT, giữ riêng: `bnv2` toàn cục bị `_dot_bien_tep` thay chỗ trong lúc đo.
_BNV2_THAT = bnv2
_TAM_DOT_BIEN: list = []


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
        # Đủ HÌNH DẠNG attestation: provider trong danh sách cho phép · surface · và
        # `session_run_id` (hoặc `KHONG_do_duoc` giải thích vì sao thiếu). Chốt `_mri` chặt
        # hơn đã bắt chính fixture này — lần thứ hai trong đợt một chốt mới bắt fixture của
        # chính bộ test, và cả hai lần fixture mới là thứ sai.
        "model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_cli",
                                    "session_run_id": "f" * 32},
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
# MA TRẬN YÊU CẦU — chép từ `PROTOCOL §8` dòng 453-454, **KHÔNG import từ cổng**.
#
# Mỗi mục: (tên yêu cầu, cách phá fixture, chuỗi phải có trong thông báo lỗi).
# MỘT YÊU CẦU CÓ NHIỀU HÀNG — mỗi hàng phá một NHÁNH khác nhau. Vòng 1 sinh đúng một ca cho
# mỗi TÊN yêu cầu và cross-review vòng 2 (R2-03) đo được ba đột biến sản phẩm vẫn sống:
# bỏ kiểm `actor` trong `_gsi` · cho nhánh MRI không-phải-dict trả `None` · đổi điều kiện
# assurance từ `or` thành `and`. Tên yêu cầu vẫn đủ, `c16` vẫn xanh — nhưng NHÁNH thì hở.
# "Đúng một ca mỗi yêu cầu" là SÀN của độ phủ, không phải TRẦN.
MA_TRAN = (
    ("schema_version",            lambda d: d.__setitem__("schema_version", 1),        "schema_version"),
    ("schema_version",            lambda d: d.pop("schema_version"),                   "schema_version"),
    ("receipt_id",                lambda d: d.pop("receipt_id"),                       "receipt_id"),
    ("receipt_id",                lambda d: d.__setitem__("receipt_id", "   "),        "receipt_id"),
    # SHA VIẾT TẮT — ca reviewer vòng 1 dựng.
    ("reviewed_sha",              lambda d: d.__setitem__("reviewed_sha", "a" * 7),    "reviewed_sha"),
    ("reviewed_sha",              lambda d: d.__setitem__("reviewed_sha", "A" * 40),   "reviewed_sha"),
    ("reviewed_sha",              lambda d: d.pop("reviewed_sha"),                     "reviewed_sha"),
    ("verdict_path",              lambda d: d.pop("verdict_path"),                     "verdict_path"),
    ("verdict_sha256",            lambda d: d.__setitem__("verdict_sha256", "khong-phai-bam"), "verdict_sha256"),
    ("verdict_sha256",            lambda d: d.__setitem__("verdict_sha256", "b" * 63), "verdict_sha256"),
    ("evidence_url",              lambda d: d.__setitem__("evidence_url", "http://e"), "evidence_url"),
    ("evidence_url",              lambda d: d.pop("evidence_url"),                     "evidence_url"),
    # --- `model_reviewer_identity`: bốn NHÁNH, không phải một ---
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity", {"x": 1}), "model_reviewer_identity"),
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity", "chuoi"), "model_reviewer_identity"),
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity", {}), "model_reviewer_identity"),
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity",
                                                          {"provider": "khong-co-thuc"}), "CHO PHÉP"),
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity",
                                                          {"provider": "anthropic"}), "surface"),
    ("model_reviewer_identity",   lambda d: d.__setitem__("model_reviewer_identity",
                                                          {"provider": "anthropic", "surface": "cli"}),
                                                          "session_run_id"),
    # SAI KIỂU, không phải VẮNG. `R4-01` (`mri_rid_str_coercion`) đo được: phục hồi phép ép
    # `str(rid)` ở `_mri` vẫn qua cả suite, vì ca kiểu duy nhất (`c4g`) đi đường `_thieu` và
    # được chốt assurance che. Hàng này khoá chốt kiểu TẠI `_mri`, không mượn chốt khác.
    ("model_reviewer_identity",   lambda d: d["model_reviewer_identity"].__setitem__(
                                                          "session_run_id", {"a": 1}), "session_run_id"),
    # --- `github_submitter_identity`: bốn NHÁNH ---
    ("github_submitter_identity", lambda d: d.__setitem__("github_submitter_identity", "banana"), "github_submitter_identity"),
    ("github_submitter_identity", lambda d: d.__setitem__("github_submitter_identity", False), "github_submitter_identity"),
    ("github_submitter_identity", lambda d: d.__setitem__("github_submitter_identity", []), "github_submitter_identity"),
    # `actor` RỖNG trong một ánh xạ hợp lệ — đúng đột biến R2-03 số 1 mà vòng 1 mù.
    ("github_submitter_identity", lambda d: d.__setitem__("github_submitter_identity", {"actor": "  "}), "actor"),
    ("github_submitter_identity", lambda d: d.pop("github_submitter_identity"),        "github_submitter_identity"),
    ("anchor",                    lambda d: d.pop("anchor"),                           "anchor"),
    ("anchor",                    lambda d: d.__setitem__("anchor", "chuoi"),          "anchor"),
    ("anchor.loai",               lambda d: d["anchor"].__setitem__("loai", ""),       "anchor.loai"),
    ("anchor.loai",               lambda d: d["anchor"].__setitem__("loai", "canonical_ancestryy"), "CHO PHÉP"),
    ("anchor.cuong_do",           _pha_anchor_cuong_do,                                "anchor.cuong_do"),
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


def _sach_hoan_toan(fn):
    """ĐỐI CHỨNG NGHIÊM: ca dương phải QUA **và** không để lại `chua_do` nào.

    Cross-review vòng 3 (R3-01) đo được: dưới `m9`, `c18` vẫn `qua` trong khi `kiem` trả về
    MỘT mục `chua_do` — `_kiem` vứt thống kê đi nên "đối chứng xanh" KHÔNG có nghĩa phép xác
    minh còn chạy. Một đối chứng chỉ hỏi `loi` là đối chứng nửa mù."""
    tt, ct = _chay_1(fn)
    if tt != "qua":
        return False, f"{tt}: {ct}"
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        import yaml as _y
        (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
        (tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").write_text(
            _y.safe_dump(_bn_neo(sha, bam, duong), allow_unicode=True), encoding="utf-8")
        try:
            loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
        except Exception as ex:                                  # noqa: BLE001
            return False, f"đối chứng ném {type(ex).__name__}: {ex}"
    if loi or tk.get("chua_do"):
        return False, f"mỏ neo ĐÚNG mà còn loi={loi} chua_do={tk.get('chua_do')}"
    return True, ""


def _dot_bien_tep(cu: str, moi: str, bo_qua_parity=()):
    """Đột biến MỨC TỆP: chép nguồn cổng, thay ĐÚNG MỘT chỗ, nạp bản sao làm `bnv2` và trỏ
    `CONG` sang nó.

    Vì sao `setattr` KHÔNG với tới được bốn đột biến dùng hàm này:
      · `c21`/`c23` đo MÃ THOÁT của CLI qua `subprocess`, mà tiến trình con nạp lại module TỪ
        ĐĨA — mọi `setattr` ở tiến trình cha vô hình với nó. `m13` bản trước đổi hằng ở cha,
        child vẫn trả 2, nên ca đỏ vì ORACLE sai chứ không vì CLI bị làm yếu (R3-01).
      · Ba nhánh của `_neo_git` là NHÁNH bên trong một hàm, không phải một tên tra được.
        R3-02 đo được cả ba gỡ đi mà suite vẫn `25/25 · 16/16`.

    Chốt chống "đột biến rỗng" — bài học `sed` đụng dấu phân cách sinh tệp RỖNG chạy `rc=0`
    rồi được đọc thành CÓ RĂNG: đòi mẫu khớp ĐÚNG MỘT chỗ, và bản mới phải khác bản gốc mà
    không bị cắt cụt."""
    goc = Path(_BNV2_THAT.__file__).read_text(encoding="utf-8")
    if goc.count(cu) != 1:
        raise LoiDungCa(f"đột biến mức tệp: mẫu khớp {goc.count(cu)} chỗ, đòi ĐÚNG 1 — {cu!r}")
    ban_moi = goc.replace(cu, moi)
    if ban_moi == goc or len(ban_moi) < len(goc) // 2:
        raise LoiDungCa("đột biến mức tệp KHÔNG đổi gì hoặc cắt cụt tệp")
    # CÂY GƯƠNG, không phải một tệp lẻ trong `/tmp`. `_provider_chinh_tac()` đọc
    # `__file__.parent.parent/.claude/dev/launcher.py`, nên một bản sao đặt phẳng làm
    # `PROVIDER_CHO_PHEP` tụt về bản lịch sử `{anthropic, human}` — và mọi biên nhận
    # `openai_codex` rớt cổng. Đo được ngay lượt đầu: ba đột biến R3-02 cùng bị đối chứng
    # `c18` báo "phá cả cổng" trong khi thứ hỏng là RIG, không phải bản vá. Đúng bài học
    # "rig tự đẻ ra hồi quy không tồn tại" — hai vế phải khác ĐÚNG MỘT biến.
    d = Path(tempfile.mkdtemp(prefix="bnv2-dotbien-"))
    _TAM_DOT_BIEN.append(d)
    (d / "ops").mkdir()
    (d / ".claude" / "dev").mkdir(parents=True)
    # ĐỦ BA nguồn từ vựng provider, không phải một. Thiếu `AGENTS.md` là chốt parity ĐỎ
    # ngay — và nó ĐÃ đỏ đúng lúc thêm nguồn thứ ba, báo `giàn giáo hỏng` cho MƯỜI đột biến
    # thay vì để chúng đội lốt "KHÔNG RĂNG". Đây là lần thứ ba rig lệch, và lần đầu tiên nó
    # bị bắt NGAY mà không tốn một vòng review.
    shutil.copyfile(GOC / ".claude" / "dev" / "launcher.py", d / ".claude" / "dev" / "launcher.py")
    shutil.copyfile(GOC / "AGENTS.md", d / "AGENTS.md")
    tep = d / "ops" / "bien_nhan_v2.py"
    tep.write_text(ban_moi, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(f"bnv2_db_{len(_TAM_DOT_BIEN)}", tep)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # CHỐT PARITY: bản sao chỉ được khác bản gốc ĐÚNG dòng ta thay. Thiếu chốt này thì một
    # lệch do RIG đội lốt "đột biến có răng" (hoặc ngược lại, đội lốt "phá cả cổng").
    for k in ("PROVIDER_CHO_PHEP", "ALLOWLIST_CUTOVER", "NO_DA_DO", "ANCHOR_LOAI_CHO_PHEP"):
        # `bo_qua_parity` miễn ĐÚNG hằng đang là ĐÍCH của đột biến: giữ nó ở đây thì phép
        # canh hoá ra đang đòi đột biến ĐỪNG xảy ra. Miễn phải TƯỜNG MINH từng tên, không
        # có cờ "tắt hết" — một chốt tắt được bằng một cờ là chốt sẽ bị tắt.
        if k in bo_qua_parity:
            continue
        if getattr(mod, k) != getattr(_BNV2_THAT, k):
            raise LoiDungCa(f"rig đột biến làm lệch `{k}`: bản sao KHÔNG chỉ khác một dòng — "
                            f"{getattr(mod, k)!r} != {getattr(_BNV2_THAT, k)!r}")
    globals()["bnv2"] = mod
    globals()["CONG"] = tep


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
        d["model_reviewer_identity"] = {"provider": "anthropic", "surface": "claude_code_cli",
                                        "che_do": "subagent_trong_phien_dieu_phoi",
                                        "KHONG_do_duoc": "khong co phien rieng"}
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
def c4e_assurance_CHI_co_dieu_kien_che_do():
    """Từng điều kiện ĐƠN ĐỘC phải đủ để chặn — R2-03 số 3 đo được đổi `or` thành `and` vẫn xanh
    vì `c4d` bật CẢ HAI điều kiện cùng lúc. Một ca bật hết mọi điều kiện không phân biệt được
    `or` với `and`."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["model_reviewer_identity"] = {"provider": "anthropic", "surface": "cli",
                                        "session_run_id": "e" * 32,      # CÓ bằng chứng
                                        "che_do": "subagent_trong_phien_dieu_phoi"}
        d["assurance"] = "cross_approved"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "phiên điều phối" in loi[0],
             f"tự khai subagent (dù CÓ run_id) phải chặn mức approval, được: {loi}")


@ca
def c4f_assurance_CHI_thieu_bang_chung():
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["model_reviewer_identity"] = {"provider": "anthropic", "surface": "cli",
                                        "KHONG_do_duoc": "x"}          # KHÔNG che_do, KHÔNG run_id
        d["assurance"] = "cross_approved"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "session_run_id" in loi[0],
             f"thiếu bằng chứng độc lập phải chặn mức approval, được: {loi}")
        d["model_reviewer_identity"]["phien_doc_lap"] = True
        tmp2 = _cay(Path(t + "/y"), {"a-verdict.receipt.yaml": d})
        n2, loi2 = _kiem(tmp2, allowlist={}, no_da_do={})
        bang(n2 == 0, f"ĐỐI CHỨNG: khai `phien_doc_lap` tường minh phải QUA, được: {loi2}")


@ca
def c4g_bang_chung_doc_lap_phai_dung_KIEU():
    """`phien_doc_lap: "false"` là CHUỖI KHÔNG RỖNG nên truthy — nó KHÔNG phải lời khai dương.

    Cùng lớp "CÓ MẶT khác KHẢ NĂNG", ở tầng KIỂU DỮ LIỆU. Cross-review vòng 3 (P1) đo được."""
    for ten, mri in (
        ("phien_doc_lap là chuỗi 'false'",
         {"provider": "anthropic", "surface": "cli", "KHONG_do_duoc": "x", "phien_doc_lap": "false"}),
        ("session_run_id là ánh xạ",
         {"provider": "anthropic", "surface": "cli", "session_run_id": {"a": 1}, "KHONG_do_duoc": "x"}),
    ):
        with tempfile.TemporaryDirectory() as t:
            d = v2_du(); d["model_reviewer_identity"] = mri; d["assurance"] = "cross_approved"
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            bang(n >= 1 and any("bằng chứng phiên độc lập" in x for x in loi),
                 f"{ten}: phải chặn mức approval, được: {loi}")


@ca
def c23_trang_thai_thu_ba_UU_TIEN_hon_vi_pham():
    """Kết quả HỖN HỢP (một vi phạm + một chưa đo) phải ra rc=2, không phải rc=1.

    Gộp nó thành "vi phạm thường" khiến bên điều phối đọc *thiếu bằng chứng* thành *đã đo và
    sai* — hai kết luận khác hẳn nhau."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        import yaml as _y
        (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
        chua = _bn_neo(sha, bam, duong); chua["reviewed_sha"] = "deadbeef" * 5   # chưa đo
        (tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").write_text(
            _y.safe_dump(chua, allow_unicode=True), encoding="utf-8")
        xau = _bn_neo(sha, bam, duong); xau.pop("receipt_id")                    # vi phạm
        (tmp / bnv2.THU_MUC / "b-verdict.receipt.yaml").write_text(
            _y.safe_dump(xau, allow_unicode=True), encoding="utf-8")
        r = subprocess.run([sys.executable, str(CONG), "--root", str(tmp)],
                           capture_output=True, text=True)
        # SỐ 2 VIẾT THẲNG: một oracle lấy từ chính module đang bị đột biến sẽ trôi theo nó.
        bang(r.returncode == 2,
             f"hỗn hợp phải rc=2, được {r.returncode}\n{r.stderr[-300:]}")
        bang("receipt_id" in r.stderr and "KHÔNG ĐO ĐƯỢC" in r.stderr,
             f"phải IN CẢ HAI nhóm, chỉ đổi mã thoát: {r.stderr[-300:]!r}")


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
    cua_test = {ten for ten, _, _ in MA_TRAN}   # nhiều hàng có thể trùng tên: đó là NHÁNH
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
        # NỬA SAU, và đây là chỗ bản trước hở: soi danh sách nội bộ KHÔNG chứng minh CLI
        # làm gì với nó. Cross-review vòng 2 (P1) đo được `1 KHÔNG ĐO ĐƯỢC` trên stderr mà
        # `rc=0` + `TỔNG: ĐẠT` — cổng CI bắt buộc vẫn xanh với một SHA bịa. Ca phải neo
        # MÃ THOÁT, không neo trạng thái trong bộ nhớ.
        r = subprocess.run([sys.executable, str(CONG), "--root", str(tmp)],
                           capture_output=True, text=True)
        # SỐ 2 VIẾT THẲNG, không đọc `bnv2.RC_KHONG_DO_DUOC`: một oracle lấy từ chính
        # module đang bị đột biến sẽ trôi theo nó. `m13` bản trước đổi hằng ở TIẾN TRÌNH
        # CHA trong khi child nạp lại tệp từ đĩa nên vẫn trả 2 — ca đỏ vì oracle sai, không
        # vì CLI bị làm yếu (R3-01).
        bang(r.returncode == 2,
             f"CLI phải trả rc=2 khi có KHÔNG ĐO ĐƯỢC, được {r.returncode}")
        bang("TỔNG: ĐẠT" not in r.stdout,
             f"CLI KHÔNG được in marker tổng đạt khi còn chưa đo: {r.stdout[-200:]!r}")


def _kho_git_re_nhanh(tmp: Path, than_verdict: str, lui_head=True):
    """Kho git nơi commit CHỨA verdict **KHÔNG** phải tổ tiên của HEAD.

    Phân biệt "object CÓ" với "object VỚI TỚI ĐƯỢC": `cat-file -e` và `rev-parse <c>:<đường>`
    đều QUA ở đây, chỉ `merge-base --is-ancestor` mới đỏ. Không có fixture này thì nhánh tổ
    tiên gỡ đi mà suite vẫn xanh — đúng phép đo R3-02.
    Trả (sha_nền, sha_rẽ, băm_blob, đường_dẫn)."""
    E = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
         "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", ""),
         "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}

    def g(*a):
        r = subprocess.run(["git", "-C", str(tmp), *a], capture_output=True, text=True, env=E)
        dung(r.returncode == 0, f"git {' '.join(a)} hỏng: {r.stderr[:200]}")
        return r.stdout.strip()

    duong = "ops/reviews/x-verdict.md"
    (tmp / "ops" / "reviews").mkdir(parents=True, exist_ok=True)
    (tmp / "nen.txt").write_text("nen\n", encoding="utf-8")
    g("init", "-q"); g("add", "-A"); g("commit", "-qm", "nen")
    nen = g("rev-parse", "HEAD")
    (tmp / duong).write_text(than_verdict, encoding="utf-8")
    g("add", "-A"); g("commit", "-qm", "re")
    re_ = g("rev-parse", "HEAD")
    if lui_head:
        g("checkout", "-q", nen)      # HEAD LÙI về nền ⇒ `re_` thôi là tổ tiên của HEAD
        dung(g("rev-parse", "HEAD") == nen, "checkout không đưa HEAD về commit nền")
    import hashlib as _h
    return nen, re_, _h.sha256(than_verdict.encode("utf-8")).hexdigest(), duong


def _kho_git_hai_commit(tmp: Path, than_verdict: str):
    """Hai commit, HEAD ở commit SAU: `reviewed_sha` và commit trong `evidence_url` KHÁC NHAU.

    Cần cho `c32`: bảng bơm lỗi phải nhắm ĐÚNG MỘT thao tác, mà `_bn_neo` cho hai trường ấy
    cùng một SHA nên không tách được `cat-file -e` của `reviewed_sha` với của `evidence_url`.
    Cùng lý do `_blob_khop` được tách ra: một phép bơm giết cả cụm thì không phân biệt gì."""
    return _kho_git_re_nhanh(tmp, than_verdict, lui_head=False)


def _ghi_bn(tmp: Path, d: dict, ten="a-verdict.receipt.yaml"):
    import yaml as _y
    (tmp / bnv2.THU_MUC).mkdir(parents=True, exist_ok=True)
    (tmp / bnv2.THU_MUC / ten).write_text(_y.safe_dump(d, allow_unicode=True), encoding="utf-8")


@ca
def c24_anchor_KHONG_CO_DUONG_DO_vao_trang_thai_THU_BA():
    """`protected_evidence_ref` · `check_object`: cổng CHƯA có đường đo ⇒ KHÔNG ĐO ĐƯỢC.

    R3-02 đo được nhánh này gỡ đi mà suite vẫn `25/25 · 16/16` — mọi ca cũ đều dùng
    `canonical_ancestry`, nên hai loại kia CÓ MẶT trong danh sách cho phép mà chưa từng
    được ai chạm. Ca đo TỪNG loại RIÊNG và neo cả MÃ THOÁT: "vào `chua_do`" mà CLI vẫn
    `rc=0` thì cổng vẫn xanh, đúng bệnh `c21` từng bắt."""
    for loai in ("protected_evidence_ref", "check_object"):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
            d = _bn_neo(sha, bam, duong); d["anchor"]["loai"] = loai
            _ghi_bn(tmp, d)
            loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
            bang(not loi, f"{loai}: KHÔNG được thành vi phạm (đó là trạng thái thứ ba): {loi}")
            bang(any("CHƯA có đường đo" in x for x in (tk.get("chua_do") or [])),
                 f"{loai}: phải vào KHÔNG ĐO ĐƯỢC, được: {tk.get('chua_do')}")
            r = subprocess.run([sys.executable, str(CONG), "--root", str(tmp)],
                               capture_output=True, text=True)
            bang(r.returncode == 2, f"{loai}: CLI phải rc=2, được {r.returncode}")


@ca
def c25_commit_CO_THAT_ma_KHONG_phai_to_tien_thi_DO():
    """`canonical_ancestry` đòi mỏ neo VỚI TỚI ĐƯỢC — một nhánh rẽ không phải canonical.

    Bản trước chỉ có fixture mà mọi phép git đều qua, nên `if rc_tt == 1:` gỡ đi vẫn xanh:
    blob còn đó, băm còn khớp, cổng in "sạch" cho một commit ngoài lịch sử."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        nen, re_, bam, duong = _kho_git_re_nhanh(tmp, "noi dung verdict\n")
        d = v2_du()
        d["reviewed_sha"] = nen                       # tra được, không phải thứ đang đo
        d["verdict_sha256"] = bam
        d["verdict_path"] = duong
        d["evidence_url"] = f"https://github.com/o/r/blob/{re_}/{duong}"
        _ghi_bn(tmp, d)
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "KHÔNG phải tổ tiên" in loi[0],
             f"commit ngoài lịch sử của HEAD phải ĐỎ (blob vẫn khớp): {loi}")


@ca
def c26_merge_base_rc_NGOAI_0_1_la_KHONG_DO_DUOC():
    """`merge-base` trả rc ngoài {0,1} (kho hỏng, git bị giết) là trạng thái THỨ BA.

    Bơm lỗi ở RIÊNG phép ấy — mọi lời gọi git khác đi qua nguyên vẹn — nên ca này phân biệt
    được "cổng còn phân ba trạng thái ở merge-base" với "cổng chết ở một phép git bất kỳ".
    Một đột biến giết cả cụm không chứng minh từng chốt còn răng."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        _ghi_bn(tmp, _bn_neo(sha, bam, duong))
        that = bnv2._git

        def _bom(root, *args, **kw):
            if tuple(args[:2]) == ("merge-base", "--is-ancestor"):
                return 128, "fatal: bơm lỗi (ca c26)"
            return that(root, *args, **kw)

        bnv2._git = _bom
        try:
            loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
        finally:
            bnv2._git = that
        bang(not loi, f"git hỏng KHÔNG được thành vi phạm: {loi}")
        bang(any("KHÔNG ĐO ĐƯỢC quan hệ tổ tiên" in x for x in (tk.get("chua_do") or [])),
             f"rc=128 của merge-base phải vào KHÔNG ĐO ĐƯỢC, được: {tk.get('chua_do')}")


@ca
def c27_loai_CO_KHOANG_TRANG_khong_duoc_tron_khoi_phep_do():
    """MỘT phép đọc `anchor.loai` cho CẢ schema LẪN dispatch (R2-01).

    Hai cách đọc cùng một trường là cùng lớp với "hai bản trôi lệch": `" canonical_ancestry "`
    qua được chốt hình dạng (chuẩn hoá) rồi TRỐN khỏi `_neo_git` (so thô). `c22` không phân
    biệt được — nó dùng giá trị sạch, nên đột biến dispatch giết nó vì lý do KHÁC."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["anchor"]["loai"] = "  canonical_ancestry  "
        d["evidence_url"] = "https://github.com/o/r/pull/1"      # KHÔNG ghim commit
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "KHÔNG đo được" in loi[0],
             f"`loai` có khoảng trắng phải đi ĐÚNG đường dispatch canonical, được: {loi}")


def _cay_guong(tmp: Path, co_launcher=True, than_launcher=None, co_agents=True):
    """Cây GƯƠNG đủ để chạy CLI THẬT: `ops/bien_nhan_v2.py` + `.claude/dev/launcher.py` + kho git.

    Chép chính tệp thật rồi bỏ/đổi ĐÚNG nguồn cần hỏng — không mô phỏng lại cổng, vì một
    bản mô phỏng sẽ trôi lệch và ca sẽ đo bản mô phỏng chứ không đo cổng."""
    (tmp / "ops").mkdir(parents=True, exist_ok=True)
    # CHÉP BẢN ĐANG HIỆU LỰC, không phải bản THẬT: dưới một đột biến mức tệp, `bnv2` là bản
    # đã sửa, và một cây gương chép bản gốc sẽ chạy CLI CHƯA BỊ ĐỘT BIẾN — ca đích xanh, đột
    # biến lĩnh "KHÔNG RĂNG" oan. Đo được ngay lượt đầu: `m18`/`m19` báo không răng trong khi
    # phép làm yếu có thật. Đúng lớp lỗi "rig đo thứ khác với thứ được công bố".
    shutil.copyfile(Path(bnv2.__file__), tmp / "ops" / "bien_nhan_v2.py")
    if co_agents:
        shutil.copyfile(GOC / "AGENTS.md", tmp / "AGENTS.md")
    if co_launcher or than_launcher is not None:
        (tmp / ".claude" / "dev").mkdir(parents=True, exist_ok=True)
        (tmp / ".claude" / "dev" / "launcher.py").write_text(
            than_launcher if than_launcher is not None
            else (GOC / ".claude" / "dev" / "launcher.py").read_text(encoding="utf-8"),
            encoding="utf-8")
    sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
    _ghi_bn(tmp, _bn_neo(sha, bam, duong))
    return tmp / "ops" / "bien_nhan_v2.py"


@ca
def c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA():
    """`R4-02`: hỏng NGUỒN phải ra `KHÔNG ĐO ĐƯỢC`, không được thành lời kết tội biên nhận.

    Reviewer đo được: bỏ riêng `.claude/dev/launcher.py` ⇒ `PROVIDER_CHO_PHEP` tụt về hai bí
    danh lịch sử và cổng kết tội một biên nhận `openai_codex` **hợp lệ** là *"chuỗi tự do
    không phải attestation"* — `rc=1`, `1 vi phạm`, **0 chưa đo**. Lỗi ĐO báo thành lỗi DỮ
    LIỆU, tức người đọc sẽ đi sửa hiện vật đúng. Ba đường hỏng, cùng một kết luận."""
    for ten, kw, rc_mong, phai_co in (
        ("đủ nguồn",              {},                              0, "TỔNG: ĐẠT"),
        ("thiếu launcher.py",     {"co_launcher": False},          2, "KHÔNG ĐO ĐƯỢC danh sách provider"),
        ("không có bảng hợp đồng", {"than_launcher": "X = 1\n"},   2, "không có phép gán"),
        ("nguồn hỏng cú pháp",    {"than_launcher": "def (\n"},   2, "không phân tích được"),
        # NGUỒN THỨ BA cũng phải fail-close: từ vựng provider nằm ở BA chỗ, nên mỗi chỗ mất
        # là một đường mù riêng. Bỏ sót hàng này thì `AGENTS.md` biến mất mà cổng vẫn xanh.
        ("thiếu AGENTS.md",       {"co_agents": False},            2, "không đọc được nguồn từ vựng"),
    ):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            cong = _cay_guong(tmp, **kw)
            r = subprocess.run([sys.executable, str(cong), "--root", str(tmp)],
                               capture_output=True, text=True)
            bang(r.returncode == rc_mong,
                 f"{ten}: đòi rc={rc_mong}, được {r.returncode}\n{r.stderr[-400:]}")
            hop = r.stdout + r.stderr
            bang(phai_co in hop, f"{ten}: thiếu bằng chứng dương {phai_co!r}: {hop[-400:]!r}")
            bang("chuỗi tự do" not in hop,
                 f"{ten}: KẾT TỘI biên nhận hợp lệ thay vì khai lỗi ĐO: {hop[-400:]!r}")


@ca
def c31_hop_dong_provider_doc_DU_BA_NGUON_khong_chep_tay():
    """Mọi provider kho KHAI — ở CẢ BA chỗ khai — phải được cổng CHẤP NHẬN.

    `R4-01` (`provider_back_to_handcopy`): phục hồi tập chép tay cũ qua được cả suite, mà
    tập ấy TỪ CHỐI `anthropic_claude` — một biên nhận Claude hợp lệ mới tạo rớt cổng CI bắt
    buộc. Chốt parity của cây gương KHÔNG bắt được: nó so bản sao với module, nên hai bản
    cùng sai thì vẫn khớp."""
    import ast
    import re as _re
    dung((GOC / ".claude" / "dev" / "launcher.py").is_file() and (GOC / "AGENTS.md").is_file(),
         "KHÔNG ĐO ĐƯỢC: thiếu .claude/dev/launcher.py hoặc AGENTS.md")
    van_l = (GOC / ".claude" / "dev" / "launcher.py").read_text(encoding="utf-8")
    van_a = (GOC / "AGENTS.md").read_text(encoding="utf-8")
    cay = ast.parse(van_l)
    ten = set()
    for n in ast.walk(cay):
        if (isinstance(n, ast.Assign) and n.targets
                and getattr(n.targets[0], "id", "") == "_TRANSPORT_CONTRACTS"):
            ten = {t.elts[0].value for t in n.value.elts}
    dung(ten, "KHÔNG ĐO ĐƯỢC: không đọc được `_TRANSPORT_CONTRACTS`")
    # BA NGUỒN, vì từ vựng provider của kho KHÔNG nằm một chỗ. Cross-review connector (P2)
    # đo được: rút CHỈ từ `_TRANSPORT_CONTRACTS` là TỪ CHỐI `google_antigravity` (vốn đã
    # được chấp nhận ở bản chép tay cũ) và `openai_chatgpt` (AGENTS.md §4 khai đích danh) —
    # tức bản vá "đọc, không chép" của vòng trước THU HẸP tập hợp lệ. Đọc đủ chỗ mới là đọc.
    ngoai = set(_re.findall(r"provider\s+([a-z0-9_]+)\s+qua\s+execution_surface", van_l))
    web = set(_re.findall(r"(?m)^provider:\s*([a-z0-9_]+)\s*$", van_a))
    dung(ngoai and web,
         f"KHÔNG ĐO ĐƯỢC nguồn 2/3: launcher={sorted(ngoai)} agents={sorted(web)}")
    ten |= ngoai | web
    thieu = sorted(x for x in ten if x not in bnv2.PROVIDER_CHO_PHEP)
    bang(not thieu, f"cổng TỪ CHỐI provider chính tắc {thieu} — danh sách đã tụt về bản chép tay")
    # HÀNH VI, không chỉ tập hợp: một biên nhận dùng tên chính tắc phải QUA thật.
    for prov in sorted(ten):
        with tempfile.TemporaryDirectory() as t:
            d = v2_du(); d["model_reviewer_identity"]["provider"] = prov
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n_, loi = _kiem(tmp, allowlist={}, no_da_do={})
            bang(n_ == 0, f"provider chính tắc {prov!r} bị từ chối: {loi}")


@ca
def c29_CLI_CHI_co_vi_pham_phai_tra_rc_1():
    """Ba trạng thái phải đo RIÊNG TỪNG CÁI, không mượn nhau.

    `R4-01` (`cli_violation_returns_clean`): `return RC_VI_PHAM` → `return RC_SACH` sống sót
    cả suite. `c14` mang tên "ba trạng thái" nhưng chỉ chạy ca SẠCH và ca thiếu thư mục;
    `c23` chỉ khoá kết quả HỖN HỢP. Nhánh **chỉ có vi phạm** không ai chạm."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        xau = _bn_neo(sha, bam, duong); xau.pop("receipt_id")
        _ghi_bn(tmp, xau)
        r = subprocess.run([sys.executable, str(CONG), "--root", str(tmp)],
                           capture_output=True, text=True)
        # SỐ 1 VIẾT THẲNG: oracle lấy từ module đang bị đột biến sẽ trôi theo nó.
        bang(r.returncode == 1,
             f"CHỈ vi phạm (không có chưa đo) phải rc=1, được {r.returncode}\n{r.stderr[-300:]}")
        bang("TỔNG: ĐỎ" in r.stderr, f"thiếu bằng chứng ÂM trên stderr: {r.stderr[-300:]!r}")
        bang("TỔNG: ĐẠT" not in r.stdout, f"in marker tổng ĐẠT khi đang có vi phạm: {r.stdout[-200:]!r}")


@ca
def c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC():
    """BẢNG theo TỪNG THAO TÁC, vì `R4-01` đo được **năm** phép gỡ `chua` mà suite vẫn xanh.

    `c26` chỉ bơm lỗi ở `merge-base`. Bốn đường còn lại — `rev-parse HEAD`, `cat-file -e`
    của commit trong `evidence_url`, `cat-file -p` trả rc khác 0, và `cat-file -p` ném —
    chưa ca nào chạm. Đây là **một hình dạng lỗi thiếu ca nhánh**, nên vá bằng bảng chứ
    không bằng bốn ca đặt tên rời."""
    def dung_bnv2_git(nen, khop, rc, ra=""):
        def _bom(root, *args, **kw):
            if khop(args):
                return rc, ra
            return nen(root, *args, **kw)
        return _bom

    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        nen_sha, moi_sha, bam, duong = _kho_git_hai_commit(tmp, "noi dung verdict\n")
        d = v2_du()
        d["reviewed_sha"] = nen_sha                 # tra được, KHÁC commit trong URL
        d["verdict_sha256"] = bam
        d["verdict_path"] = duong
        d["evidence_url"] = f"https://github.com/o/r/blob/{moi_sha}/{duong}"
        _ghi_bn(tmp, d)

        # ĐỐI CHỨNG DƯƠNG trước: fixture này phải SẠCH khi không bơm gì.
        loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
        bang(not loi and not tk.get("chua_do"),
             f"fixture hai commit phải sạch khi chưa bơm lỗi: loi={loi} chua_do={tk.get('chua_do')}")

        bang_thao_tac = (
            ("reviewed_sha: git không gọi được",
             lambda a: a[:2] == ("cat-file", "-e") and a[2].startswith(nen_sha),
             127, "không gọi được git"),
            ("commit của evidence_url không tra được",
             lambda a: a[:2] == ("cat-file", "-e") and a[2].startswith(moi_sha),
             1, "KHÔNG ĐO ĐƯỢC commit"),
            ("không có HEAD để so tổ tiên",
             lambda a: a[:2] == ("rev-parse", "--verify"),
             1, "KHÔNG ĐO ĐƯỢC tổ tiên"),
        )
        for ten, khop, rc, phai_co in bang_thao_tac:
            that = bnv2._git
            bnv2._git = dung_bnv2_git(that, khop, rc)
            try:
                loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
            finally:
                bnv2._git = that
            bang(not loi, f"{ten}: lỗi ĐO không được thành VI PHẠM: {loi}")
            bang(any(phai_co in x for x in (tk.get("chua_do") or [])),
                 f"{ten}: phải vào KHÔNG ĐO ĐƯỢC ({phai_co!r}), được: {tk.get('chua_do')}")

        # Hai đường ĐỌC BLOB đi thẳng `subprocess.run` trong cổng, không qua `_git`.
        class _Shim:
            def __init__(self, that, hong):
                self._that, self._hong = that, hong
            def __getattr__(self, k):
                return getattr(self._that, k)
            def run(self, cmd, *a, **kw):
                if isinstance(cmd, list) and "cat-file" in cmd and "-p" in cmd:
                    return self._hong()
                return self._that.run(cmd, *a, **kw)

        class _KetQua:
            returncode, stdout = 3, b""

        for ten, hong in (("blob đọc trả rc khác 0", lambda: _KetQua()),
                          ("blob đọc NÉM ngoại lệ", lambda: (_ for _ in ()).throw(OSError("bơm lỗi")))):
            that = bnv2.subprocess
            bnv2.subprocess = _Shim(that, hong)
            try:
                loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
            finally:
                bnv2.subprocess = that
            bang(not loi, f"{ten}: lỗi ĐO không được thành VI PHẠM: {loi}")
            bang(any("KHÔNG ĐO ĐƯỢC nội dung blob" in x for x in (tk.get("chua_do") or [])),
                 f"{ten}: phải vào KHÔNG ĐO ĐƯỢC, được: {tk.get('chua_do')}")


# MỌI trường attestation × MỌI kiểu KHÔNG-PHẢI-CHUỖI. Bảng, không phải bốn ca đặt tên:
# vòng trước vá đúng lớp này cho `session_run_id` + `phien_doc_lap` rồi DỪNG, bỏ sót
# `surface` + `KHONG_do_duoc` trong CÙNG một hàm — vá một danh sách, không phải một lớp.
TRUONG_ATTESTATION = (
    ("model_reviewer_identity.provider",
     lambda d, v: d["model_reviewer_identity"].__setitem__("provider", v), "provider"),
    ("model_reviewer_identity.surface",
     lambda d, v: d["model_reviewer_identity"].__setitem__("surface", v), "surface"),
    ("model_reviewer_identity.session_run_id",
     lambda d, v: d["model_reviewer_identity"].__setitem__("session_run_id", v), "session_run_id"),
    # `KHONG_do_duoc` chỉ được đọc khi KHÔNG có `session_run_id`, nên phải bỏ nó đi thì
    # nhánh mới chạy — đây đúng chỗ chốt cũ bị chốt khác che.
    ("model_reviewer_identity.KHONG_do_duoc",
     lambda d, v: (d["model_reviewer_identity"].pop("session_run_id", None),
                   d["model_reviewer_identity"].__setitem__("KHONG_do_duoc", v)), "session_run_id"),
    ("github_submitter_identity.actor",
     lambda d, v: d["github_submitter_identity"].__setitem__("actor", v), "actor"),
    ("anchor.loai", lambda d, v: d["anchor"].__setitem__("loai", v), "anchor.loai"),
    ("anchor.cuong_do", lambda d, v: d["anchor"].__setitem__("cuong_do", v), "anchor.cuong_do"),
)
KIEU_KHONG_PHAI_CHUOI = ({"fake": 1}, ["fake"], 123, True)


@ca
def c34_MOI_truong_attestation_phai_la_CHUOI_khong_chi_truthy():
    """`str(v or "").strip()` biến MỌI thứ thành lời khai — `{fake: 1}` ra `"{'fake': 1}"`.

    Phản chứng của connector trên head `4ef73e6` (P1): `surface: {fake: 1}` cộng
    `KHONG_do_duoc: {fake: 1}` ⇒ `_thieu` trả **KHÔNG vi phạm nào**, nên một biên nhận
    không có bề mặt thực thi hợp lệ **lẫn** lời giải thích vẫn lĩnh `cross_approved`."""
    hong = []
    for ten, pha, phai_chua in TRUONG_ATTESTATION:
        for gt in KIEU_KHONG_PHAI_CHUOI:
            with tempfile.TemporaryDirectory() as t:
                d = v2_du(); pha(d, gt)
                tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
                n, loi = _kiem(tmp, allowlist={}, no_da_do={})
                if n < 1:
                    hong.append(f"{ten} = {gt!r}: cổng NHẬN một giá trị không phải chuỗi")
                elif not any(phai_chua in x for x in loi):
                    hong.append(f"{ten} = {gt!r}: đỏ nhưng SAI LÝ DO: {loi[0][:100]}")
    bang(not hong, f"{len(hong)}/{len(TRUONG_ATTESTATION) * len(KIEU_KHONG_PHAI_CHUOI)} "
                   f"cặp (trường × kiểu) KHÔNG bị chặn:\n      " + "\n      ".join(hong[:8]))


@ca
def c34b_PHAN_CHUNG_NGUYEN_VAN_cua_connector():
    """Dựng lại ĐÚNG biên nhận reviewer mô tả, không diễn giải lại — nó phải ĐỎ."""
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["model_reviewer_identity"] = {"provider": "anthropic", "surface": {"fake": 1},
                                        "KHONG_do_duoc": {"fake": 1}, "phien_doc_lap": True}
        d["assurance"] = "cross_approved"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n >= 1 and any("surface" in x for x in loi),
             f"phản chứng nguyên văn của connector phải ĐỎ vì `surface`, được: {loi}")


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


_mri_that = bnv2._mri
_thieu_that = bnv2._thieu


def _thieu_or_thanh_and(d):
    """Đột biến: chốt chéo assurance đòi CẢ HAI điều kiện thay vì MỘT."""
    loi = [msg for _, kt in bnv2.YEU_CAU for msg in [kt(d)] if msg]
    mri = d.get("model_reviewer_identity")
    if isinstance(mri, dict):
        trong_phien = "subagent" in str(mri.get("che_do") or "").lower()
        co_bang_chung = bool(str(mri.get("session_run_id") or "").strip()) or bool(mri.get("phien_doc_lap"))
        khai = str(d.get("assurance") or d.get("assurance_dat") or "").strip()
        if khai in bnv2.ASSURANCE_CAN_DOC_LAP and (trong_phien and not co_bang_chung):
            loi.append("khai vượt bằng chứng (phiên điều phối)")
    return loi


_git_that = bnv2._git


def _git_bo_kiem_duong_dan(root, *args, timeout=20):
    """Đột biến GIỮ nhận dạng URL và GIỮ mọi lời gọi khác; chỉ làm phép tra đường dẫn
    trong commit LUÔN trỏ về tệp có thật. Mô phỏng đúng "cổng thôi kiểm đường dẫn"."""
    if len(args) >= 2 and args[0] == "rev-parse" and ":" in str(args[1]):
        goc = str(args[1]).split(":", 1)[0]
        return _git_that(root, "rev-parse", f"{goc}:ops/reviews/x-verdict.md", timeout=timeout)
    return _git_that(root, *args, timeout=timeout)


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

    def do(ten, sua, ca_dich, mo_ta, doi_chung=None, mong_khong_rang=False):
        # BẢN SAO SÂU, không phải tham chiếu: đột biến dưới đây sửa TẠI CHỖ
        # (`dict.__setitem__`), nên `setattr` lại chính object đã bẩn thì khôi phục ĐƯỢC SỐ
        # KHÔNG — và mọi ca chạy sau sẽ đo trên một cổng đã bị nới. Đúng bài học "đột biến
        # ghi vào tệp THẬT rồi khôi phục" của kho, chỉ đổi tệp thành object.
        # `_dot_bien_tep` THAY CHỖ module toàn cục, nên phải giữ tham chiếu module THẬT ở
        # đây: khôi phục thuộc tính lên module đã bị thay là khôi phục nhầm chỗ.
        mod_cu, cong_cu = globals()["bnv2"], globals()["CONG"]
        cu = {k: copy.deepcopy(getattr(mod_cu, k))
              for k in ("ALLOWLIST_CUTOVER", "NO_DA_DO", "YEU_CAU",
                        "ANCHOR_LOAI_CHO_PHEP", "_HEX40",
                        "_HEX64", "_BLOB_URL", "_blob_khop", "_doc_loai", "_git",
                        "_mri", "_gsi", "_thieu", "RC_KHONG_DO_DUOC")}
        # ĐỐI CHỨNG PHẢI CHẠY TRONG KHI ĐỘT BIẾN CÒN HIỆU LỰC — và bản trước KHÔNG:
        # nó gọi đối chứng SAU khối `finally`, tức trên cổng ĐÃ KHÔI PHỤC. Nên một đột biến
        # "từ chối tất cả" giết được ca đích, rồi đối chứng chạy trên cổng sạch nên xanh, và
        # nó vẫn lĩnh tín dụng CÓ RĂNG. Cross-review vòng 3 (P2) bắt đúng chỗ này: cái chốt
        # tôi thêm ở vòng trước ĐỂ CHỐNG tín dụng giả tự nó là một NGHI LỄ. Đây là tầng thứ
        # tư của cùng lớp lỗi — và lần này nó nằm trong chính cơ chế chống lớp lỗi ấy.
        tt, ct, dc_ok, dc_vi_sao = "gian_giao", "chưa chạy", True, ""
        try:
            sua()          # có thể THAY CHỖ module ⇒ phải nằm TRONG try, kẻo hỏng là rò
            fn = next(f for f in CA if f.__name__ == ca_dich)
            tt, ct = _chay_1(fn)
            if tt == "giet_that" and doi_chung:
                fn_dc = next(f for f in CA if f.__name__ == doi_chung)
                dc_ok, dc_vi_sao = _sach_hoan_toan(fn_dc)
        except LoiDungCa as ex:
            tt, ct = "gian_giao", f"giàn giáo đột biến hỏng: {ex}"
        finally:
            for k, v in cu.items():
                setattr(mod_cu, k, v)
            globals()["bnv2"], globals()["CONG"] = mod_cu, cong_cu
            while _TAM_DOT_BIEN:
                shutil.rmtree(_TAM_DOT_BIEN.pop(), ignore_errors=True)
        ok = tt == "giet_that"
        if ok and doi_chung and not dc_ok:
            ok = False
            mo_ta += f" — NHƯNG đối chứng {doi_chung} KHÔNG sạch hoàn toàn ({dc_vi_sao}): đột biến phá cả cổng"
        # Ca TỰ KIỂM đảo kỳ vọng: nó ĐẠT khi bị báo KHÔNG CÓ RĂNG.
        dat = (not ok) if mong_khong_rang else ok
        # HAI CỜ đi kèm mỗi hàng để TỔNG KẾT TỰ SUY RA, không chép tay: `R4-03` đo được
        # tử số loại `m14` ra mà mẫu số vẫn giữ nó, và một tỉ lệ "6/21" chép tay trong chú
        # thích + CHANGELOG đã lệch ngay ở đoạn vừa sửa một lời khai rộng hơn phép đo.
        ra.append((ten, ca_dich, dat, tt, ((ct or "").splitlines() or [""])[0][:80],
                   bool(mong_khong_rang), bool(doi_chung)))
        nhan = ("TỰ KIỂM ok" if dat else "TỰ KIỂM ĐỎ") if mong_khong_rang else (
            "CÓ RĂNG " if ok else "KHÔNG RĂNG")
        print(f"  {nhan:10s} {ten:38s} → {ca_dich} = {tt}  ({mo_ta})")

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
    do("m7_bo_phep_kiem_DUONG_DAN_trong_commit",
       lambda: setattr(bnv2, "_git", _git_bo_kiem_duong_dan),
       "c19_neo_git_SAI_DUONG_DAN_thi_DO", "bỏ kiểm đường dẫn, GIỮ nhận dạng URL",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # Bản đầu của m8 nhắm `_HEX64` vào `c17` và KHÔNG CÓ RĂNG: nới chốt hình dạng không
    # làm ca ma trận đỏ vì fixture ấy không mang mỏ neo blob. Đột biến đo số không thì phải
    # sửa cho đúng đích, không phải bỏ đi — nay nó nhắm thẳng phép so băm blob.
    # R2-04: m7/m9 bản trước KHÔNG nới URL như tên khai — chúng làm verifier TỪ CHỐI ngay ở
    # hình dạng, nên ca đích chết vì lý do KHÁC và `12/12` không chứng minh 12 thuộc tính đã
    # bị khoá. Đây là `tin_dung_gia` ở tầng NGỮ NGHĨA: assert có chạy, nhưng đo khác điều
    # được công bố. Nay CỤM MỎ NEO (`m7` `m9` `m14` `m15` `m16` `m17`) kèm ĐỐI CHỨNG `c18`
    # phải VẪN QUA — một đột biến "từ chối tất cả" rớt đối chứng ấy thay vì lĩnh tín dụng.
    # NÓI ĐÚNG PHẠM VI: các đột biến khác KHÔNG khai đối chứng, vì `c18` không nằm trên đường
    # chúng phá (đột biến allowlist/ma trận không đi qua `_neo_git`), nên một đối chứng luôn
    # xanh ở đó chỉ là nghi lễ. Bản trước viết "mỗi đột biến" trong khi đo được 2/16 — một
    # lời khai rộng hơn phép đo, đúng lớp lỗi tệp này sinh ra để bắt.
    # TỈ LỆ CỤ THỂ KHÔNG CHÉP Ở ĐÂY: dòng tổng kết của `main()` TỰ SUY RA từ các hàng, vì bản
    # trước chép tay "6/21" rồi nó lệch ngay lượt sau (`R4-03`). Một con số chép tay trong chú
    # thích là một con số sẽ trôi.
    # m9 bản trước ép `_doc_loai` trả HẲN một loại khác — nó giết `c22` nhưng ĐỐI CHỨNG
    # NGHIÊM bắt được: dưới nó `c18` (mỏ neo ĐÚNG) cũng rơi vào `chua_do`, tức đột biến phá
    # cả đường mỏ neo chứ không đo riêng phép chuẩn hoá. Nay nó dựng lại ĐÚNG lỗi R2-01:
    # schema đọc chuẩn hoá, dispatch đọc THÔ — và có ca riêng (`c27`) cho đúng thuộc tính ấy.
    do("m9_dispatch_doc_THO_khong_chuan_hoa",
       # NEO THÊM DÒNG SAU: `loai = _doc_loai(a)` có ở CẢ `_anchor_loai` (schema) lẫn
       # `_neo_git` (dispatch); chốt "khớp đúng 1 chỗ" vừa bắt được bản đầu nhắm nhầm
       # (báo `gian_giao` thay vì lặng lẽ đột biến sai chỗ).
       lambda: _dot_bien_tep('    loai = _doc_loai(a)\n    if loai in (',
                             '    loai = (a.get("loai") if isinstance(a, dict) else "")\n'
                             '    if loai in ('),
       "c27_loai_CO_KHOANG_TRANG_khong_duoc_tron_khoi_phep_do",
       "hai cách đọc cùng một trường ⇒ qua schema rồi trốn dispatch",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m9b_URL_khong_ghim_tut_xuong_trang_thai_thu_ba",
       lambda: _dot_bien_tep("loi.append(f\"{ten}: khai `anchor.loai: canonical_ancestry` nhưng",
                             "chua.append(f\"{ten}: khai `anchor.loai: canonical_ancestry` nhưng"),
       "c22_canonical_ancestry_ma_URL_khong_ghim_thi_DO",
       "mỏ neo TỰ KHAI mà không đo được bị hạ từ VI PHẠM xuống chưa đo",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m8_neo_git_khong_so_bam_blob",
       lambda: setattr(bnv2, "_blob_khop", lambda a, b: True),
       "c20_neo_git_BAM_LECH_thi_DO", "cổng thôi so băm blob")
    do("m6_bo_yeu_cau_anchor_cuong_do",
       lambda: setattr(bnv2, "YEU_CAU", tuple(x for x in bnv2.YEU_CAU if x[0] != "anchor.cuong_do")),
       "c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong", "gỡ một yêu cầu con của anchor")
    # ĐỘT BIẾN TỰ KIỂM CHO CHÍNH CƠ CHẾ ĐỐI CHỨNG: một mutant TỪ CHỐI TẤT CẢ giết được ca
    # đích nhưng phá luôn ca dương, nên nó PHẢI bị báo là KHÔNG CÓ RĂNG. Nếu nó lĩnh được
    # tín dụng thì đối chứng lại là nghi lễ — như bản trước.
    do("m14_TU_KIEM_tu_choi_tat_ca_phai_bi_bao_KHONG_RANG",
       lambda: setattr(bnv2, "_thieu", lambda d: ["từ chối tất cả"]),
       "c19_neo_git_SAI_DUONG_DAN_thi_DO", "PHẢI hiện KHÔNG RĂNG — đây là ca tự kiểm",
       doi_chung="c18_neo_git_DUNG_thi_qua", mong_khong_rang=True)
    do("m12_assurance_doi_OR_thanh_AND",
       lambda: setattr(bnv2, "_thieu", _thieu_or_thanh_and),
       "c4e_assurance_CHI_co_dieu_kien_che_do", "R2-03 số 3: một ca bật cả hai điều kiện thì mù")
    # m13 đột biến MỨC TỆP rồi chạy CLI từ bản sao ấy — child mới là thứ `c23` đo. Bản trước
    # `setattr` hằng ở tiến trình CHA trong khi child nạp lại tệp từ đĩa, nên nó đo SỐ KHÔNG.
    do("m13_go_UU_TIEN_cua_trang_thai_thu_ba",
       lambda: _dot_bien_tep('if loi and not tk.get("chua_do"):', "if loi:"),
       "c23_trang_thai_thu_ba_UU_TIEN_hon_vi_pham",
       "kết quả HỖN HỢP bị gộp thành vi phạm thường (rc=1 thay vì 2)")
    # --- R3-02: BA NHÁNH trong `_neo_git` mà reviewer gỡ được với suite XANH (`25/25 · 16/16`).
    # Chúng là nhánh BÊN TRONG một hàm, không phải một tên tra được ⇒ chỉ mức tệp với tới.
    do("m15_bo_nhanh_hai_loai_anchor_khong_co_duong_do",
       lambda: _dot_bien_tep('if loai in ("protected_evidence_ref", "check_object"):',
                             "if False:"),
       "c24_anchor_KHONG_CO_DUONG_DO_vao_trang_thai_THU_BA",
       "loại mỏ neo cổng không đo được thì TRỐN luôn khỏi phép đo",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m16_bo_phep_kiem_TO_TIEN",
       lambda: _dot_bien_tep("if rc_tt == 1:", "if False:"),
       "c25_commit_CO_THAT_ma_KHONG_phai_to_tien_thi_DO",
       "`cat-file -e` qua là đủ ⇒ một nhánh rẽ thành canonical ancestry",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m17_bo_trang_thai_thu_ba_cua_merge_base",
       lambda: _dot_bien_tep("if rc_tt not in (0, 1):", "if False:"),
       "c26_merge_base_rc_NGOAI_0_1_la_KHONG_DO_DUOC",
       "git hỏng bị đọc thành 'là tổ tiên'",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # --- R4-02: hỏng NGUỒN phải ra trạng thái thứ ba, không thành lời kết tội biên nhận
    do("m18_go_hang_KHONG_DO_DUOC_cua_nguon_provider",
       lambda: _dot_bien_tep("    if PROVIDER_NGUON_HONG is not None:", "    if False:"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "hỏng nguồn trở lại IM LẶNG ⇒ cổng xanh",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m19_van_KET_TOI_provider_khi_nguon_hong",
       lambda: _dot_bien_tep("    if PROVIDER_NGUON_HONG is None and prov not in PROVIDER_CHO_PHEP:",
                             "    if prov not in PROVIDER_CHO_PHEP:"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "lỗi ĐO lại bị báo thành lỗi DỮ LIỆU — đúng ca reviewer dựng",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # ĐÍCH của đột biến này CHÍNH LÀ `PROVIDER_CHO_PHEP`, nên phải miễn nó khỏi parity —
    # giữ lại thì phép canh hoá ra đang đòi đột biến đừng xảy ra.
    do("m20_provider_tut_ve_ban_CHEP_TAY",
       lambda: _dot_bien_tep(
           "PROVIDER_CHINH_TAC, PROVIDER_NGUON_HONG = _provider_chinh_tac()",
           'PROVIDER_CHINH_TAC, PROVIDER_NGUON_HONG = ({"anthropic", "openai_codex", '
           '"openai_api", "google_antigravity", "human"}, None)',
           bo_qua_parity=("PROVIDER_CHO_PHEP",)),
       "c31_hop_dong_provider_doc_DU_BA_NGUON_khong_chep_tay",
       "bản chép tay TỪ CHỐI `anthropic_claude` — biên nhận Claude hợp lệ rớt cổng",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # --- R4-01: ba trạng thái CLI đo riêng, và chốt kiểu ở `_mri` không mượn chốt khác
    do("m21_CLI_vi_pham_tra_ve_SACH",
       lambda: _dot_bien_tep("        return RC_VI_PHAM", "        return RC_SACH"),
       "c29_CLI_CHI_co_vi_pham_phai_tra_rc_1", "nhánh CHỈ có vi phạm không ai chạm")
    # `m28` đo CHÍNH `_chuoi`; `m22` đo rằng `_mri` THẬT SỰ GỌI nó. Hai thuộc tính khác
    # nhau: một helper đúng mà chỗ gọi bỏ qua thì lỗ vẫn còn — đúng kiểu "có mặt ≠ dùng được".
    do("m22_MRI_khong_goi_chot_kieu_o_cho_goi",
       lambda: _dot_bien_tep(
           '    rid = _chuoi(v.get("session_run_id"))',
           '    rid = str(v.get("session_run_id") or "").strip()'),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am", "R4-01: chốt kiểu ở `_mri` bị chốt khác che")
    # --- R4-01: NĂM phép gỡ `chua` trong `_neo_git`, mỗi thao tác một đột biến RIÊNG
    do("m23_go_KHONG_DO_DUOC_khi_git_khong_goi_duoc",
       lambda: _dot_bien_tep("        if rc == 127:", "        if False:"),
       "c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC",
       "rc=127 tụt xuống nhánh 'object không tra được'",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m24_go_KHONG_DO_DUOC_cua_commit_trong_evidence_url",
       lambda: _dot_bien_tep(
           '        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC commit `{commit[:12]}…` trong `evidence_url`")\n',
           "        pass\n"),
       "c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC",
       "commit không tra được thành IM LẶNG", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m25_go_KHONG_DO_DUOC_khi_khong_co_HEAD",
       lambda: _dot_bien_tep(
           '        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC tổ tiên — cây không có HEAD để so")\n',
           "        pass\n"),
       "c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC",
       "không có HEAD để so mà cổng vẫn im", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m26_go_KHONG_DO_DUOC_khi_doc_blob_tra_rc_khac_0",
       lambda: _dot_bien_tep(
           '        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}… (git rc={pb.returncode})")\n',
           "        pass\n"),
       "c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC",
       "đọc blob hỏng thành IM LẶNG", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m27_go_KHONG_DO_DUOC_khi_doc_blob_NEM",
       lambda: _dot_bien_tep(
           '        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}… ({type(ex).__name__})")\n',
           "        pass\n"),
       "c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC",
       "ngoại lệ khi đọc blob thành IM LẶNG", doi_chung="c18_neo_git_DUNG_thi_qua")
    # --- vòng 5 (connector): LỚP kiểu, và từ vựng provider nằm ở BA chỗ
    do("m28_phuc_hoi_phep_ep_str_cho_MOI_truong",
       lambda: _dot_bien_tep(
           "    return v.strip() if isinstance(v, str) and v.strip() else None",
           '    return str(v or "").strip() or None'),
       "c34_MOI_truong_attestation_phai_la_CHUOI_khong_chi_truthy",
       "ánh xạ/danh sách lại thành lời khai hợp lệ", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m29_tu_vung_provider_tut_ve_MOT_nguon",
       lambda: _dot_bien_tep("    return hd | ngoai | web, None", "    return hd, None",
                             bo_qua_parity=("PROVIDER_CHO_PHEP",)),
       "c31_hop_dong_provider_doc_DU_BA_NGUON_khong_chep_tay",
       "đọc MỘT nguồn ⇒ `google_antigravity` và `openai_chatgpt` bị từ chối",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m10_bo_kiem_actor_cua_submitter",
       lambda: setattr(bnv2, "_gsi", lambda d: None if "github_submitter_identity" in d
                       else "thiếu khoá `github_submitter_identity`"),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am", "R2-03 số 1: vòng 1 mù với nhánh này")
    do("m11_MRI_khong_phai_dict_van_qua",
       lambda: setattr(bnv2, "_mri", lambda d: None if not isinstance(
           d.get("model_reviewer_identity"), dict) else _mri_that(d)),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am", "R2-03 số 2: nhánh không-phải-dict")
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
    # HAI MẪU SỐ KHÁC NHAU, nói rõ từng cái. Gộp `m14` (ca TỰ KIỂM, ĐẠT khi bị báo KHÔNG
    # RĂNG) vào tử số "CÓ RĂNG" là đếm hai thứ khác loại làm một — `R4-03`.
    thuong = [x for x in db if not x[5]]
    tu_kiem = [x for x in db if x[5]]
    dc = [x for x in thuong if x[6]]
    print(f"\nbien_nhan_v2_test: {len(CA) - len(hong)}/{len(CA)} ca đạt · "
          f"{len([x for x in thuong if x[2]])}/{len(thuong)} đột biến thường CÓ RĂNG · "
          f"{len([x for x in tu_kiem if x[2]])}/{len(tu_kiem)} ca TỰ KIỂM đạt · "
          f"{len(dc)}/{len(thuong)} đột biến thường khai đối chứng")
    if hong or khong_rang:
        print("TỔNG: ĐỎ")
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
