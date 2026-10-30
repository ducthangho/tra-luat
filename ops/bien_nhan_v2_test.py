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

import contextlib
import copy
import errno
import importlib.util
import io
import os
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
import shutil
import re as _RE
import subprocess
import sys
import tempfile
import traceback
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


# CHÉP TAY từ `AGENTS.md` §4 — *"ChatGPT Web không được … tự tạo `cross_approved`,
# `same_provider_approved` hoặc `human_audited`"*. KHÔNG import từ cổng: một oracle sinh từ
# chính module nó kiểm sẽ CO THEO mỗi lần cổng bị nới. Cross-review vòng 6 (`R6-01`) đo
# được: giao `cam` với tập chỉ chứa `cross_approved` ⇒ mất hai mức cấm còn lại mà cả suite
# vẫn xanh, vì `c36` chỉ thử mức ĐẦU TIÊN.
ASSURANCE_CAM_DONG_BANG = {
    "openai_chatgpt": ("cross_approved", "same_provider_approved", "human_audited"),
}
# CHÉP TAY từ `docs/PROTOCOL_DA_PHIEN.md` §8 mục 1-3 (`R7-02`): `human_audited` là mức của NGƯỜI
# audit; `cross_approved`/`same_provider_approved` là mức giữa các MÔ HÌNH. Bộ ba Human Auditor chép
# từ `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §2. KHÔNG import từ cổng — cùng lý do với bảng trên.
VAN_CHUYEN_NGUOI_DONG_BANG = "human"
ASSURANCE_CUA_NGUOI_DONG_BANG = ("human_audited",)
ASSURANCE_CUA_MO_HINH_DONG_BANG = ("cross_approved", "same_provider_approved")
HOP_DONG_HUMAN_DONG_BANG = {"be_mat": frozenset({"manual_audit"}), "van_chuyen": frozenset({"human"})}
# BA câu neo luật chép tay — CHÉP TAY từ `AGENTS.md` §4 và `docs/PROTOCOL_DA_PHIEN.md` §8, KHÔNG
# import từ `bnv2._NEO_LUAT_CHEP_TAY`. `R8-01` đo được vì sao: `_cay_guong` bản trước lấy danh sách
# neo TỪ CHÍNH SẢN PHẨM, nên hàng PROTOCOL của `c28` xoá CẢ HAI câu cùng lúc và bỏ kiểm RIÊNG một
# luật thì luật kia vẫn làm hàng ấy đỏ. Hai mutant, mỗi cái thêm một `continue` bỏ đúng một neo,
# **sống sót qua toàn suite** (`45/45 · 57/57 · 2/2`, rc=0, `TỔNG: ĐẠT`). Phụ thuộc vòng: một oracle
# hỏi sản phẩm "anh neo vào câu nào" rồi xoá đúng câu ấy sẽ CO THEO mỗi lần sản phẩm bỏ bớt neo.
# BỘ BA provider — CHÉP TAY từ `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §2, bảng "Nhận dạng
# provider và execution surface". Cross-review PR #460 đo được hàng Antigravity trong
# `launcher.py` LỆCH nguồn (`machine` thay vì `machine/local`) và lệch theo chiều CHẶN NHẦM:
# biên nhận khai TRUNG THỰC bị từ chối, khai SAI được nhận. Oracle nằm ở ĐÂY, không đọc từ
# `launcher.py`, vì một oracle hỏi chính bảng nó kiểm thì không canh được gì.
BO_BA_PROVIDER_DONG_BANG = (
    ("google_antigravity", "antigravity", "machine/local"),
    ("openai_chatgpt", "chatgpt_web", "human_mediated"),
    ("anthropic_claude", "claude_code", "machine/local"),
    ("openai_codex", "codex_cli", "machine"),
    ("openai_codex", "codex_desktop", "machine"),
    ("openai_codex", "codex_service", "machine"),
    ("human", "manual_audit", "human"),
)
KE_HOACH_PROVIDER = "ops/KE_HOACH_THI_CONG_DA_PROVIDER.md"
NEO_LUAT_DONG_BANG = (
    ("ASSURANCE_CAM_THEO_PROVIDER[openai_chatgpt]", "AGENTS.md",
     "tự tạo `cross_approved`, `same_provider_approved` hoặc `human_audited`"),
    ("ASSURANCE_CUA_NGUOI", "docs/PROTOCOL_DA_PHIEN.md",
     "`human_audited`: người audit có danh tính bền trên GitHub"),
    ("ASSURANCE_CUA_MO_HINH", "docs/PROTOCOL_DA_PHIEN.md",
     "`cross_approved`: reviewer và executor dùng hai họ model độc lập phục vụ lượt chạy (ví dụ họ Claude review họ Codex hoặc ngược lại)"),
)
# BA nguồn mà cổng đọc — chép tay để rig không hỏi cổng "anh cần gì" rồi chép đúng thứ cổng nói.
NGUON_PHU = ("AGENTS.md", "docs/PROTOCOL_DA_PHIEN.md", ".claude/dev/launcher.py")
# Hằng của cổng mà MỌI đột biến mức tệp phải giữ nguyên trừ khi khai đích danh (`bo_qua_parity`).
# `R7-03`: bản trước so bốn hằng cũ, bỏ `PROVIDER_HOP_DONG`/`PROVIDER_BI_DANH`/trạng thái nguồn —
# reviewer bơm mất hàng `_BE_MAT_BI_DANH` vào riêng bản launcher rig chép: 4/4 hằng vẫn BẰNG NHAU
# mà hợp đồng đã khác, và một biên nhận lịch sử nguyên byte bị gương từ chối trong khi gốc nhận.
HANG_PARITY = ("PROVIDER_CHO_PHEP", "PROVIDER_HOP_DONG", "PROVIDER_BI_DANH", "PROVIDER_NGUON_HONG",
               "ALLOWLIST_CUTOVER", "NO_DA_DO", "ANCHOR_LOAI_CHO_PHEP", "ASSURANCE_CAM_THEO_PROVIDER",
               "ASSURANCE_CUA_NGUOI", "ASSURANCE_CUA_MO_HINH", "VAN_CHUYEN_NGUOI", "HO_MODEL_MAC_DINH",
               "MUC_BANG_CHUNG_MODEL", "HO_MODEL_CHO_PHEP", "NO_CAU_LICH_SU")


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
                                                          {"provider": "anthropic", "surface": "claude_code_cli"}),
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
    # ĐỦ nguồn phụ, không phải một. Thiếu `AGENTS.md` là chốt parity ĐỎ ngay — và nó ĐÃ đỏ
    # đúng lúc thêm nguồn thứ ba, báo `giàn giáo hỏng` cho MƯỜI đột biến thay vì để chúng đội
    # lốt "KHÔNG RĂNG". Đây là lần thứ ba rig lệch, và lần đầu tiên nó bị bắt NGAY mà không
    # tốn một vòng review.
    # `R7-03`: và bản CHÉP phải BYTE-IDENTICAL với nguồn — nguồn phụ không phải đích đột biến,
    # nên khác một byte là RIG lệch chứ không phải đột biến. Reviewer đã bơm mất hàng bí danh
    # vào riêng bản rig chép mà bốn hằng parity cũ vẫn bằng nhau. So `read_bytes`, không
    # `read_text`, kẻo Windows đổi newline rồi chốt đỏ giả.
    for rel in NGUON_PHU:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(GOC / rel, d / rel)
        if (d / rel).read_bytes() != (GOC / rel).read_bytes():
            raise LoiDungCa(f"rig đột biến làm lệch nguồn phụ `{rel}`: bản chép KHÔNG byte-identical "
                            f"với nguồn — không phải đột biến, là rig")
    tep = d / "ops" / "bien_nhan_v2.py"
    tep.write_text(ban_moi, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(f"bnv2_db_{len(_TAM_DOT_BIEN)}", tep)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # CHỐT PARITY: bản sao chỉ được khác bản gốc ĐÚNG dòng ta thay. Thiếu chốt này thì một
    # lệch do RIG đội lốt "đột biến có răng" (hoặc ngược lại, đội lốt "phá cả cổng").
    for k in HANG_PARITY:
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
        d["model_reviewer_identity"] = {"provider": "anthropic", "surface": "claude_code_cli",
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
        d["model_reviewer_identity"] = {"provider": "anthropic", "surface": "claude_code_cli",
                                        "KHONG_do_duoc": "x"}          # KHÔNG che_do, KHÔNG run_id
        d["assurance"] = "cross_approved"
        d["executor_provider"] = "openai_codex"
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
         {"provider": "anthropic", "surface": "claude_code_cli", "KHONG_do_duoc": "x", "phien_doc_lap": "false"}),
        ("session_run_id là ánh xạ",
         {"provider": "anthropic", "surface": "claude_code_cli", "session_run_id": {"a": 1}, "KHONG_do_duoc": "x"}),
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
    # BYTES: nội dung fixture phải GIỐNG NHAU trên mọi nền, kẻo hai lượt CI đo hai thứ khác
    # nhau mà không ai thấy. (Hàm này vốn đã băm đĩa nên không sai — chỉ là hết trôi theo nền.)
    (tmp / duong).write_bytes(than_verdict.encode("utf-8"))
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
        # ĐỔI CẢ HAI trường: chốt `c37` (URL phải neo đúng `verdict_path`) nay chạy TRƯỚC,
        # nên fixture chỉ đổi URL sẽ chết vì lý do KHÁC — ca đo nhánh "trỏ hụt" phải thật sự
        # tới được nhánh ấy. Lần thứ ba trong đợt một chốt mới bắt fixture của chính bộ test,
        # và cả ba lần fixture mới là thứ sai.
        d["evidence_url"] = f"https://github.com/o/r/blob/{sha}/ops/reviews/KHONG-HE-CO.md"
        d["verdict_path"] = "ops/reviews/KHONG-HE-CO.md"
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
    # BYTES, không `write_text`. Trên Windows `write_text` dịch `\n` → `\r\n`, nên tệp trên
    # ĐĨA khác chuỗi Python — và dòng dưới từng băm CHUỖI thay vì băm ĐĨA. Đo được ở lượt CI
    # Windows ĐẦU TIÊN của bộ này (`e057edb`, `gate (windows-latest)`): `c32` ĐỎ ngay ở đối
    # chứng dương vì băm blob lệch. Đây đúng là `R2-02` — *"băm hai BIỂU DIỄN của cùng một
    # thứ"* — mà PR này đã vá cho SẢN PHẨM, rồi tái phát trong FIXTURE của chính nó.
    (tmp / duong).write_bytes(than_verdict.encode("utf-8"))
    g("add", "-A"); g("commit", "-qm", "re")
    re_ = g("rev-parse", "HEAD")
    if lui_head:
        g("checkout", "-q", nen)      # HEAD LÙI về nền ⇒ `re_` thôi là tổ tiên của HEAD
        dung(g("rev-parse", "HEAD") == nen, "checkout không đưa HEAD về commit nền")
    import hashlib as _h
    # BĂM THỨ TRÊN ĐĨA, không băm chuỗi đã đưa vào. `git` băm bytes của tệp, nên mọi phép so
    # phải xuất phát từ cùng một nguồn — cùng lý do `_neo_git` chỉ đọc đường bytes.
    # `lui_head=True` đã checkout về commit nền nên tệp không còn; đọc từ chính commit rẽ.
    ra = subprocess.run(["git", "-C", str(tmp), "cat-file", "-p", f"{re_}:{duong}"],
                        capture_output=True, env=E)
    dung(ra.returncode == 0, f"không đọc lại được blob verdict: {ra.stderr[:200]!r}")
    return nen, re_, _h.sha256(ra.stdout).hexdigest(), duong


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


def _cay_guong(tmp: Path, co_launcher=True, than_launcher=None, co_agents=True,
               bo_cau_neo=False, sua_launcher=None, sua_agents=None,
               co_protocol=True, sua_protocol=None, bo_cau_neo_cua=None, bo_neo_luat=None,
               kho_rieng=True):
    """Cây GƯƠNG đủ để chạy CLI THẬT: cổng + ba nguồn phụ + (mặc định) kho git có biên nhận.

    Chép chính tệp thật rồi bỏ/đổi ĐÚNG nguồn cần hỏng — không mô phỏng lại cổng, vì một
    bản mô phỏng sẽ trôi lệch và ca sẽ đo bản mô phỏng chứ không đo cổng.

    `R7-03`: mỗi nguồn phụ KHAI RIÊNG phần cố ý thay (`sua_*`/`than_*`/`bo_cau_neo*`); nguồn
    KHÔNG khai thay thì phải byte-identical với gốc, không thì rig lệch ⇒ `LoiDungCa`. Ghi
    BYTES chứ không `write_text` (Windows đổi newline). `kho_rieng=False` ⇒ chỉ dựng cổng +
    nguồn, để chạy CLI trên `--root` của kho THẬT (`c40`)."""
    (tmp / "ops").mkdir(parents=True, exist_ok=True)
    # CHÉP BẢN ĐANG HIỆU LỰC, không phải bản THẬT: dưới một đột biến mức tệp, `bnv2` là bản
    # đã sửa, và một cây gương chép bản gốc sẽ chạy CLI CHƯA BỊ ĐỘT BIẾN — ca đích xanh, đột
    # biến lĩnh "KHÔNG RĂNG" oan. Đo được ngay lượt đầu: `m18`/`m19` báo không răng trong khi
    # phép làm yếu có thật. Đúng lớp lỗi "rig đo thứ khác với thứ được công bố".
    shutil.copyfile(Path(bnv2.__file__), tmp / "ops" / "bien_nhan_v2.py")
    # `R8-01`: danh sách neo lấy từ ORACLE ĐỘC LẬP, không từ `bnv2._NEO_LUAT_CHEP_TAY`. Một
    # fixture hỏi sản phẩm "anh neo vào câu nào" thì khi sản phẩm bỏ một neo, fixture thôi xoá
    # câu ấy và ca đích xanh lên — chốt co theo thứ nó phải canh.
    neo_theo_tep = {}
    for _luat, tep_neo, cau in NEO_LUAT_DONG_BANG:
        neo_theo_tep.setdefault(tep_neo, []).append(cau)
    if bo_neo_luat is not None:
        chon = [r for r in NEO_LUAT_DONG_BANG if r[0] == bo_neo_luat]
        dung(len(chon) == 1,
             f"KHÔNG ĐO ĐƯỢC: `bo_neo_luat={bo_neo_luat!r}` khớp {len(chon)} mục của oracle, đòi ĐÚNG 1")
        neo_theo_tep = {chon[0][1]: [chon[0][2]]}

    def _ghi_nguon(rel, co, than, sua, xoa_neo):
        if not co and than is None:
            return
        goc_b = (GOC / rel).read_bytes()
        van = than if than is not None else goc_b.decode("utf-8")
        doi = than is not None or sua is not None or xoa_neo
        if xoa_neo:
            for cau in neo_theo_tep.get(rel, []):
                # Mẫu khớp KHÁC 1 chỗ ⇒ rig lệch oracle, KHÔNG phải kết quả của ca: một phép
                # `replace` hụt để nguồn nguyên vẹn và ca đích sẽ xanh mà chẳng đo gì
                # ("ca có MẶT khác ca có ĐO").
                dung(van.count(cau) == 1,
                     f"KHÔNG ĐO ĐƯỢC: câu neo {cau!r} khớp {van.count(cau)} chỗ trong `{rel}`, đòi ĐÚNG 1")
                van = van.replace(cau, "(đã xoá)")
        if sua:
            van = sua(van)
        (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp / rel).write_bytes(van if isinstance(van, bytes) else van.encode("utf-8"))
        if not doi:
            dung((tmp / rel).read_bytes() == goc_b,
                 f"rig cây gương làm lệch nguồn phụ `{rel}` dù không khai thay — không đo được")

    xoa_a = bool(bo_cau_neo or bo_cau_neo_cua == "AGENTS.md"
                 or (bo_neo_luat and "AGENTS.md" in neo_theo_tep))
    xoa_p = bool(bo_cau_neo or bo_cau_neo_cua == "docs/PROTOCOL_DA_PHIEN.md"
                 or (bo_neo_luat and "docs/PROTOCOL_DA_PHIEN.md" in neo_theo_tep))
    _ghi_nguon("AGENTS.md", co_agents, None, sua_agents, xoa_a)
    _ghi_nguon("docs/PROTOCOL_DA_PHIEN.md", co_protocol, None, sua_protocol, xoa_p)
    _ghi_nguon(".claude/dev/launcher.py", co_launcher, than_launcher, sua_launcher, False)
    if not kho_rieng:
        return tmp / "ops" / "bien_nhan_v2.py"
    sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
    _ghi_bn(tmp, _bn_neo(sha, bam, duong))
    # HAI biên nhận, không phải một: `b` khai `cross_approved` bằng một provider có hợp đồng.
    # `R7-01`: cây gương cũ chỉ có `a` (không khai assurance) nên nhánh KẾT TỘI "không hợp
    # đồng" khi nguồn hỏng chưa từng được chạm — 11 biên nhận thật bị kết tội mà `c28` xanh.
    b = _bn_neo(sha, bam, duong)
    b["receipt_id"] = "ca-thu-b"
    b["assurance"] = "cross_approved"
    b["executor_provider"] = "anthropic_claude"
    _ghi_bn(tmp, b, "b-verdict.receipt.yaml")
    return tmp / "ops" / "bien_nhan_v2.py"


# Các HÀNG của `launcher.py` mà ma trận nguồn (`c28`/`c40`) sửa — chép nguyên văn để một hàng đổi
# tên/đổi chỗ làm `_thay_1` báo KHÔNG ĐO ĐƯỢC thay vì im lặng sửa hụt.
HANG_CODEX = '    ("openai_codex", ("codex",), "codex_cli", "machine"),'
HANG_API = '    ("openai_api", ("llm",), "llm_cli", "machine"),'
HANG_AG = '    ("google_antigravity", "antigravity", "machine/local"),'
HANG_BD = '    ("anthropic", "anthropic_claude"),'
HANG_BM = '    ("claude_code_cli", "claude_code"),'


def _thay_1(cu, moi):
    """Sửa ĐÚNG MỘT chỗ trong một nguồn phụ; mẫu khớp khác 1 chỗ là rig hỏng, không phải ca đo."""
    def _f(v):
        dung(v.count(cu) == 1, f"KHÔNG ĐO ĐƯỢC: mẫu {cu!r} khớp {v.count(cu)} chỗ, đòi ĐÚNG 1")
        return v.replace(cu, moi, 1)
    return _f


@ca
def c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA():
    """`R4-02`: hỏng NGUỒN phải ra `KHÔNG ĐO ĐƯỢC`, không được thành lời kết tội biên nhận.

    Reviewer đo được: bỏ riêng `.claude/dev/launcher.py` ⇒ `PROVIDER_CHO_PHEP` tụt về hai bí
    danh lịch sử và cổng kết tội một biên nhận `openai_codex` **hợp lệ** là *"chuỗi tự do
    không phải attestation"* — `rc=1`, `1 vi phạm`, **0 chưa đo**. Lỗi ĐO báo thành lỗi DỮ
    LIỆU, tức người đọc sẽ đi sửa hiện vật đúng. Ba đường hỏng, cùng một kết luận.

    `R7-01`/`R7-03`: ma trận mở theo TỪNG THÀNH PHẦN của lược đồ nguồn — mỗi bảng bắt buộc
    (vắng · rỗng · khai hai lần · không phải literal), mỗi cột (arity ở MỖI bảng, kiểu ô ở
    provider/surface/transport/bí danh), mỗi đích bí danh đúng miền, mỗi cột đối chiếu với
    `AGENTS.md`, mỗi câu neo luật, mỗi nguồn có byte hỏng. Bản trước chỉ thử mất bảng bí danh
    PROVIDER (không bề mặt) và AGENTS lệch TRANSPORT (không surface): reviewer bỏ riêng hai chốt
    ấy trong sản phẩm mà `41/41 · 48/48` — hai phép làm yếu đi qua toàn suite.

    Cây gương nay có biên nhận `b` khai `cross_approved`, nên mọi hàng đòi thêm: KHÔNG traceback
    (cổng phải PHÂN ba trạng thái chứ không chết), và KHÔNG biên nhận nào bị KẾT TỘI khi lỗi ở
    nguồn — đúng 11 cáo buộc oan reviewer đo được."""
    for ten, kw, rc_mong, phai_co in (
        ("đủ nguồn",                   {},                              0, "2 ĐẠT v2"),
        ("thiếu launcher.py",          {"co_launcher": False},          2, "không đọc được nguồn từ vựng"),
        ("thiếu AGENTS.md",            {"co_agents": False},            2, "không đọc được nguồn từ vựng"),
        ("thiếu docs/PROTOCOL_DA_PHIEN.md", {"co_protocol": False},     2, "không đọc được nguồn từ vựng"),
        ("launcher hỏng cú pháp",      {"than_launcher": "def (\n"},   2, "không phân tích được"),
        # --- từng BẢNG bắt buộc: vắng · RỖNG · khai hai lần · không phải literal
        ("`_TRANSPORT_CONTRACTS` vắng",
         {"sua_launcher": _thay_1("_TRANSPORT_CONTRACTS = (", "_KHAC = (")},
         2, "`_TRANSPORT_CONTRACTS` thiếu hoặc sai hình dạng"),
        ("`_TRANSPORT_CONTRACTS` RỖNG",
         {"sua_launcher": lambda v: _RE.sub(r"(?ms)^_TRANSPORT_CONTRACTS = \(.*?^\)",
                                            "_TRANSPORT_CONTRACTS = ()", v, count=1)},
         2, "`_TRANSPORT_CONTRACTS` RỖNG"),
        ("`_PROVIDER_NGOAI_CLI` vắng",
         {"sua_launcher": _thay_1("_PROVIDER_NGOAI_CLI = (", "_KHAC = (")},
         2, "`_PROVIDER_NGOAI_CLI` thiếu hoặc sai hình dạng"),
        ("`_PROVIDER_NGOAI_CLI` RỖNG",
         {"sua_launcher": lambda v: _RE.sub(r"(?ms)^_PROVIDER_NGOAI_CLI = \(.*?^\)",
                                            "_PROVIDER_NGOAI_CLI = ()", v, count=1)},
         2, "`_PROVIDER_NGOAI_CLI` RỖNG"),
        ("`_PROVIDER_BI_DANH` vắng",
         {"sua_launcher": _thay_1("_PROVIDER_BI_DANH = (", "_KHAC2 = (")},
         2, "`_PROVIDER_BI_DANH` thiếu hoặc sai hình dạng"),
        ("`_BE_MAT_BI_DANH` vắng",
         {"sua_launcher": _thay_1("_BE_MAT_BI_DANH = (", "_KHAC3 = (")},
         2, "`_BE_MAT_BI_DANH` thiếu hoặc sai hình dạng"),
        ("bảng khai HAI lần ở mức module",
         {"sua_launcher": lambda v: v + "\n_PROVIDER_BI_DANH = ()\n"},
         2, "`_PROVIDER_BI_DANH` khai 2 lần ở mức module"),
        ("bảng không phải literal thuần",
         {"sua_launcher": _thay_1(HANG_BD, '    ("anthropic", _TEN_TINH_TOAN),')},
         2, "không phải literal thuần"),
        # --- từng CỘT: arity thiếu/thừa ở MỖI bảng, kiểu ô ở MỖI cột
        ("hàng `_TRANSPORT_CONTRACTS` thiếu cột",
         {"sua_launcher": _thay_1(HANG_API, '    ("openai_api", ("llm",), "llm_cli"),')},
         2, "`_TRANSPORT_CONTRACTS` hàng 3 có 3 cột, lược đồ đòi 4"),
        ("hàng `_PROVIDER_NGOAI_CLI` thừa cột",
         {"sua_launcher": _thay_1(HANG_AG, '    ("google_antigravity", "antigravity", "machine/local", "thua"),')},
         2, "`_PROVIDER_NGOAI_CLI` hàng 1 có 4 cột, lược đồ đòi 3"),
        ("hàng `_PROVIDER_BI_DANH` thiếu cột",
         {"sua_launcher": _thay_1(HANG_BD, '    ("anthropic",),')},
         2, "`_PROVIDER_BI_DANH` hàng 1 có 1 cột, lược đồ đòi 2"),
        ("hàng `_BE_MAT_BI_DANH` thiếu cột",
         {"sua_launcher": _thay_1(HANG_BM, '    ("claude_code_cli",),')},
         2, "`_BE_MAT_BI_DANH` hàng 1 có 1 cột, lược đồ đòi 2"),
        # surface/transport TRƯỚC provider: `m48` (bỏ kiểm kiểu ô) phải chết ở đúng thuộc tính
        # reviewer đo — hợp đồng `[None]` kết tội biên nhận — chứ không ở hàng provider-là-số
        # (hàng ấy chết bằng crash `sorted(int, str)`, một hệ quả khác của cùng lỗ).
        ("surface Codex là None",
         {"sua_launcher": _thay_1(HANG_CODEX, '    ("openai_codex", ("codex",), None, "machine"),')},
         2, "cột `execution_surface` = None"),
        ("surface Codex RỖNG",
         {"sua_launcher": _thay_1(HANG_CODEX, '    ("openai_codex", ("codex",), "", "machine"),')},
         2, "cột `execution_surface` = ''"),
        ("transport Codex là None",
         {"sua_launcher": _thay_1(HANG_CODEX, '    ("openai_codex", ("codex",), "codex_cli", None),')},
         2, "cột `transport` = None"),
        ("provider Codex là SỐ",
         {"sua_launcher": _thay_1(HANG_CODEX, '    (123, ("codex",), "codex_cli", "machine"),')},
         2, "cột `provider` = 123"),
        ("bộ tên lệnh không phải tuple chuỗi",
         {"sua_launcher": _thay_1(HANG_CODEX, '    ("openai_codex", "codex", "codex_cli", "machine"),')},
         2, "cột `lenh` = 'codex'"),
        ("đích bí danh provider là None",
         {"sua_launcher": _thay_1(HANG_BD, '    ("anthropic", None),')},
         2, "`_PROVIDER_BI_DANH` hàng 1 cột `provider` = None"),
        ("đích bí danh bề mặt là None",
         {"sua_launcher": _thay_1(HANG_BM, '    ("claude_code_cli", None),')},
         2, "`_BE_MAT_BI_DANH` hàng 1 cột `execution_surface` = None"),
        # --- từng ĐÍCH bí danh phải đúng MIỀN
        ("bí danh trỏ provider KHÔNG hợp đồng",
         {"sua_launcher": _thay_1(HANG_BD, '    ("anthropic", "khong_he_co"),')},
         2, "không có hợp đồng"),
        ("bí danh bề mặt trỏ bề mặt KHÔNG CÓ",
         {"sua_launcher": _thay_1(HANG_BM, '    ("claude_code_cli", "khong_he_co"),')},
         2, "không phải bề mặt của provider nào"),
        # --- từng CỘT ĐỐI CHIẾU với `AGENTS.md`: provider · surface · transport
        ("AGENTS.md khai provider KHÔNG hợp đồng",
         {"sua_agents": _thay_1("provider: openai_chatgpt", "provider: ke_gian_9")},
         2, "hai nguồn LỆCH nhau"),
        ("AGENTS.md khai LỆCH bề mặt (mượn `codex_cli` có sẵn)",
         {"sua_agents": _thay_1("execution_surface: chatgpt_web", "execution_surface: codex_cli")},
         2, "be_mat=`codex_cli` khác hợp đồng"),
        ("AGENTS.md khai LỆCH vận chuyển",
         {"sua_agents": _thay_1("transport: human_mediated", "transport: machine")},
         2, "van_chuyen=`machine` khác hợp đồng"),
        # --- từng NEO luật chép tay, theo TỪNG tệp nguồn
        ("AGENTS.md mất câu biện minh", {"bo_cau_neo_cua": "AGENTS.md"}, 2, "luật chép tay mất neo"),
        # HAI neo của PROTOCOL tách thành hai LƯỢT RIÊNG ở khối dưới, không phải một hàng ở đây:
        # một hàng xoá cả hai câu thì bỏ kiểm RIÊNG một luật vẫn đỏ nhờ luật kia (`R8-01`).
        # --- byte KHÔNG giải mã được ở MỖI nguồn
        ("launcher có byte KHÔNG giải mã được",
         {"sua_launcher": lambda v: v.encode("utf-8") + b"\n# \xff\xfe\n"},
         2, "không đọc được nguồn từ vựng"),
        ("AGENTS.md có byte KHÔNG giải mã được",
         {"sua_agents": lambda v: v.encode("utf-8") + b"\n\xff\xfe\n"},
         2, "không đọc được nguồn từ vựng"),
        ("PROTOCOL có byte KHÔNG giải mã được",
         {"sua_protocol": lambda v: v.encode("utf-8") + b"\n\xff\xfe\n"},
         2, "không đọc được nguồn từ vựng"),
    ):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            cong = _cay_guong(tmp, **kw)
            r = subprocess.run([sys.executable, str(cong), "--root", str(tmp)],
                               capture_output=True, text=True)
            hop = r.stdout + r.stderr
            bang("Traceback" not in hop,
                 f"{ten}: cổng CHẾT bằng traceback thay vì phân ba trạng thái:\n{r.stderr[-400:]}")
            bang(r.returncode == rc_mong,
                 f"{ten}: đòi rc={rc_mong}, được {r.returncode}\n{r.stderr[-400:]}")
            bang(phai_co in hop, f"{ten}: thiếu bằng chứng dương {phai_co!r}: {hop[-400:]!r}")
            if rc_mong == 0:
                bang("TỔNG: ĐẠT" in r.stdout, f"{ten}: rc=0 mà không có `TỔNG: ĐẠT`: {r.stdout[-200:]!r}")
            bang("chuỗi tự do" not in hop,
                 f"{ten}: KẾT TỘI biên nhận hợp lệ thay vì khai lỗi ĐO: {hop[-400:]!r}")
            ket_toi = [x for x in r.stderr.splitlines() if x.startswith("  ĐỎ")]
            bang(not ket_toi,
                 f"{ten}: {len(ket_toi)} biên nhận bị KẾT TỘI trong khi lỗi ở NGUỒN — lỗi ĐO thành "
                 f"lỗi DỮ LIỆU:\n      " + "\n      ".join(x[:140] for x in ket_toi[:4]))
    # --- `R8-01`: MỖI neo luật một LƯỢT RIÊNG, mất ĐÚNG một câu, câu kia giữ NGUYÊN BYTE.
    # Reviewer đo được hai mutant (mỗi cái `continue` bỏ đúng một neo) SỐNG SÓT qua toàn suite
    # `45/45 · 57/57 · 2/2`, rc=0, `TỔNG: ĐẠT` — vì hàng cũ xoá cả hai câu cùng lúc nên luật còn
    # lại vẫn làm hàng ấy đỏ. Bảng câu chữ ở đây là `NEO_LUAT_DONG_BANG` (chép tay), KHÔNG phải
    # `bnv2._NEO_LUAT_CHEP_TAY`: một oracle sinh từ sản phẩm sẽ co theo sản phẩm.
    neo_protocol = [r for r in NEO_LUAT_DONG_BANG if r[1] == "docs/PROTOCOL_DA_PHIEN.md"]
    dung(len(neo_protocol) == 2,
         f"KHÔNG ĐO ĐƯỢC: oracle có {len(neo_protocol)} neo PROTOCOL, khối này dựng cho ĐÚNG 2")
    for luat, tep_neo, cau in neo_protocol:
        kia = [c for _l, _t, c in neo_protocol if c != cau]
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            cong = _cay_guong(tmp, bo_neo_luat=luat)
            # RIG TRƯỚC KẾT QUẢ: mất đúng câu này, và câu KIA còn nguyên byte trong bản gương.
            van_guong = (tmp / tep_neo).read_text(encoding="utf-8")
            dung(cau not in van_guong,
                 f"KHÔNG ĐO ĐƯỢC: `{luat}` — rig KHÔNG xoá được câu neo, ca sẽ xanh mà chẳng đo gì")
            dung(all(van_guong.count(c) == 1 for c in kia),
                 f"KHÔNG ĐO ĐƯỢC: `{luat}` — rig đụng cả câu neo KIA, lượt này mất HAI neo chứ không một")
            r = subprocess.run([sys.executable, str(cong), "--root", str(tmp)],
                               capture_output=True, text=True)
            hop = r.stdout + r.stderr
            ket_toi = [x for x in r.stderr.splitlines() if x.startswith("  ĐỎ")]
            bang("Traceback" not in hop,
                 f"mất RIÊNG neo `{luat}`: cổng CHẾT bằng traceback:\n{r.stderr[-400:]}")
            bang(r.returncode == 2,
                 f"mất RIÊNG neo `{luat}`: đòi rc=2, được {r.returncode}\n{r.stderr[-400:]}")
            # ĐÚNG THUỘC TÍNH: thông báo phải nêu ĐÚNG luật mất neo — không phải chỉ "mất neo"
            # chung chung, và KHÔNG được nêu luật kia (nêu cả hai = vẫn không phân biệt được).
            bang(f"không còn câu biện minh cho `{luat}`" in hop,
                 f"mất RIÊNG neo `{luat}`: thông báo không nêu ĐÚNG tên luật: {hop[-400:]!r}")
            for _l, _t, _c in neo_protocol:
                if _l != luat:
                    bang(f"không còn câu biện minh cho `{_l}`" not in hop,
                         f"mất RIÊNG neo `{luat}`: thông báo còn kết tội `{_l}` — hai neo che nhau")
            bang("TỔNG: ĐẠT" not in r.stdout,
                 f"mất RIÊNG neo `{luat}`: mất một neo mà vẫn `TỔNG: ĐẠT`: {r.stdout[-200:]!r}")
            bang(not ket_toi,
                 f"mất RIÊNG neo `{luat}`: {len(ket_toi)} biên nhận bị KẾT TỘI trong khi lỗi ở "
                 f"NGUỒN — lỗi ĐO thành lỗi DỮ LIỆU: {ket_toi[:2]}")
    # LƯỢT LỖI HỖN HỢP: nguồn hỏng + một biên nhận sai THẬT ở chốt KHÔNG phụ thuộc nguồn. Trạng
    # thái thứ ba thắng ở mã thoát (rc=2), nhưng biên nhận sai VẪN phải được báo sai — "không đo
    # được hợp đồng" không phải "miễn kiểm" (reviewer: *"Bỏ mọi kiểm khi nguồn lỗi lại che vi
    # phạm độc lập"*).
    with tempfile.TemporaryDirectory() as t:
        import yaml as _y
        tmp = Path(t)
        cong = _cay_guong(tmp, co_launcher=False)
        c = _y.safe_load((tmp / bnv2.THU_MUC / "a-verdict.receipt.yaml").read_text(encoding="utf-8"))
        c.pop("receipt_id")
        _ghi_bn(tmp, c, "c-verdict.receipt.yaml")
        r = subprocess.run([sys.executable, str(cong), "--root", str(tmp)],
                           capture_output=True, text=True)
        ket_toi = [x for x in r.stderr.splitlines() if x.startswith("  ĐỎ")]
        bang(r.returncode == 2, f"hỗn hợp nguồn hỏng + biên nhận sai: đòi rc=2, được {r.returncode}")
        bang(len(ket_toi) == 1 and "c-verdict" in ket_toi[0] and "receipt_id" in ket_toi[0],
             f"biên nhận sai THẬT phải vẫn bị báo (đúng một, đúng tệp, đúng lý do), được: {ket_toi}")
        bang("KHÔNG ĐO ĐƯỢC danh sách provider" in r.stderr,
             f"lượt hỗn hợp phải vẫn khai lỗi nguồn: {r.stderr[-300:]!r}")


@ca
def c31_hop_dong_provider_doc_DU_BA_NGUON_khong_chep_tay():
    """Tập provider phải khớp ĐÚNG hai bảng CÓ CẤU TRÚC của kho — hai chiều, không một.

    Chiều THIẾU: bản chép tay từ chối `anthropic_claude`, tức một biên nhận Claude hợp lệ
    rớt cổng CI. Chiều THỪA: nhét execution surface vào tập provider ⇒ `claude_code`
    `codex_cli` `llm_cli` thành provider hợp lệ mà suite vẫn xanh (`R5-02`). Một ca chỉ hỏi
    một chiều khoá được một nửa, và nửa nó bỏ là nửa NỚI QUYỀN."""
    dung((GOC / ".claude" / "dev" / "launcher.py").is_file() and (GOC / "AGENTS.md").is_file(),
         "KHÔNG ĐO ĐƯỢC: thiếu .claude/dev/launcher.py hoặc AGENTS.md")
    ten = ({r[0] for r in _doc_bang_launcher("_TRANSPORT_CONTRACTS")}
           | {r[0] for r in _doc_bang_launcher("_PROVIDER_NGOAI_CLI")})
    bi_danh = {r[0] for r in _doc_bang_launcher("_PROVIDER_BI_DANH")}
    dung(ten and bi_danh, "KHÔNG ĐO ĐƯỢC: bảng provider rỗng")
    thieu = sorted(x for x in ten if x not in bnv2.PROVIDER_CHO_PHEP)
    bang(not thieu, f"cổng TỪ CHỐI provider chính tắc {thieu}")
    # `R7-02`: không còn tập "không hợp đồng" để trừ — oracle này nay ĐỘC LẬP với cổng: tên nào
    # không ở hai bảng và không phải bí danh thì là tên cổng tự nở thêm.
    thua = sorted(x for x in bnv2.PROVIDER_CHO_PHEP if x not in ten | bi_danh)
    bang(not thua,
          f"cổng CHẤP NHẬN {thua} — không có trong bảng nào, cũng không phải bí danh. "
          f"Danh sách CHO PHÉP nở thêm là nới quyền.")
    # HÀNH VI, không chỉ tập hợp: mỗi provider chính tắc + bề mặt của CHÍNH NÓ phải QUA.
    for prov in sorted(ten):
        with tempfile.TemporaryDirectory() as t:
            d = v2_du(); d["model_reviewer_identity"]["provider"] = prov
            hd = bnv2.PROVIDER_HOP_DONG.get(prov) or {"be_mat": {"codex_cli"}}
            d["model_reviewer_identity"]["surface"] = sorted(hd["be_mat"])[0]
            if prov in bnv2.ASSURANCE_CAM_THEO_PROVIDER:
                d["assurance"] = "advisory_review"
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
            # THAO TÁC THỨ SÁU — connector (P2 trên `670071b`) chỉ đúng chỗ bảng này còn
            # thiếu: `rev-parse <commit>:<đường dẫn>` trả 127 (KHÔNG GỌI ĐƯỢC git) bị đọc
            # thẳng thành *"mỏ neo trỏ hụt"*, tức lỗi ĐO thành lời KẾT TỘI, `rc=1` thay `rc=2`.
            ("không tra được đường dẫn trong commit",
             lambda a: a[0] == "rev-parse" and len(a) > 1 and ":" in str(a[1]),
             127, "KHÔNG ĐO ĐƯỢC đường dẫn"),
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
    # `R8-04`: trường TUỲ CHỌN cũng phải phân biệt VẮNG với CÓ-MÀ-HỎNG. `transport` từng lọt
    # MỌI kiểu không-phải-chuỗi vì `_chuoi` trả `None` cho cả hai và nhánh `if vc and …` gộp
    # chúng; chỉ chuỗi-sai-hợp-đồng mới bị bắt. Nó nằm ở ĐÂY, trong ma trận chung, chứ không
    # thành một ca lẻ — cùng lý do `_chuoi` là MỘT cửa: vá một danh sách không phải vá một lớp.
    ("model_reviewer_identity.transport",
     lambda d, v: d["model_reviewer_identity"].__setitem__("transport", v), "transport"),
    ("anchor.cuong_do", lambda d, v: d["anchor"].__setitem__("cuong_do", v), "anchor.cuong_do"),
)
# `R8-04` thêm `""`: chuỗi RỖNG là một trong các giá trị reviewer đo được lọt qua `transport`,
# và nó là ca biên riêng — đúng KIỂU chuỗi, nhưng `_chuoi` vẫn trả `None`, nên nó đi CHUNG
# nhánh với "vắng mặt" y như các kiểu sai. Đo trước khi thêm: cả 6 trường còn lại đã chặn nó.
# `R9-F02` thêm `None`: bản trước khai `None` là "phản chứng tìm thêm" cho `transport` nhưng KHÔNG
# đưa nó vào ma trận, nên `5/40` đúng mà null KHÔNG bị khoá — reviewer lượt 9 đo được: đột biến coi
# riêng null là "vắng mặt" bỏ được một hành vi ĐÃ CÔNG BỐ mà toàn suite vẫn `48/48 · 62/62`, rc=0.
# Ca có MẶT (trong lời khai) khác ca có ĐO (trong ma trận).
KIEU_KHONG_PHAI_CHUOI = ({"fake": 1}, ["fake"], 123, True, "", None)


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


def _doc_bang_launcher(ten):
    """Đọc một bảng của `launcher.py` bằng AST RIÊNG của bộ test — oracle không mượn cổng.

    Ô là tuple (bộ tên lệnh) bị bỏ, nên hàng của `_TRANSPORT_CONTRACTS` cũng ra
    `[provider, surface, transport]` như `_PROVIDER_NGOAI_CLI`."""
    import ast
    cay = ast.parse((GOC / ".claude" / "dev" / "launcher.py").read_text(encoding="utf-8"))
    nut = next((n for n in ast.walk(cay) if isinstance(n, ast.Assign) and n.targets
                and getattr(n.targets[0], "id", "") == ten), None)
    dung(nut is not None, f"KHÔNG ĐO ĐƯỢC: `{ten}` không có trong launcher.py")
    return [[x.value for x in t.elts if isinstance(x, ast.Constant)] for t in nut.value.elts]


def _nap_guong(tmp: Path, bom_launcher="", bom_agents=""):
    """Nạp cổng từ một CÂY GƯƠNG có thể BƠM THÊM văn bản vào hai nguồn từ vựng.

    Dùng để đo hướng tấn công *nới danh sách CHO PHÉP*: cây thật không bị đụng, và phần bơm
    là văn bản HỢP LỆ về cú pháp — đúng thứ một lần sửa vô hại có thể mang theo."""
    (tmp / "ops").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(bnv2.__file__), tmp / "ops" / "bien_nhan_v2.py")
    bom = {".claude/dev/launcher.py": bom_launcher, "AGENTS.md": bom_agents}
    # BYTES + phần bơm, và kiểm lại bản đã ghi ĐÚNG bằng gốc + bơm (`R7-03`: nguồn không cố ý
    # thay phải byte-identical; phần cố ý thay khai đích danh là chính đối số `bom_*`).
    for rel in NGUON_PHU:
        (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
        mong = (GOC / rel).read_bytes() + bom.get(rel, "").encode("utf-8")
        (tmp / rel).write_bytes(mong)
        dung((tmp / rel).read_bytes() == mong, f"rig cây gương ghi lệch `{rel}` — không đo được")
    sp = importlib.util.spec_from_file_location(
        f"bnv2_guong_{abs(hash(bom_launcher + bom_agents)) % 10**8}",
        tmp / "ops" / "bien_nhan_v2.py")
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


@ca
def c35_KHONG_duoc_NOI_danh_sach_provider_bang_van_ban_tu_do():
    """Danh sách CHO PHÉP nới được bằng một dòng CHÚ THÍCH thì KHÔNG phải danh sách cho phép.

    Phiên thi công tự dựng phản chứng này TRƯỚC khi reviewer chạy, và nó BẮN TRÚNG bản vừa
    viết: thả đúng một dòng `# … provider ke_gian qua execution_surface …` vào cuối
    `launcher.py` ⇒ `ke_gian` được CHẤP NHẬN. Bài học `v1.36.68` ở dạng mới: đảo danh sách
    cấm thành danh sách cho phép là ĐÚNG, nhưng một danh sách cho phép rút từ VĂN BẢN TỰ DO
    thì lại nới được bằng văn bản tự do.

    Nay chỉ đọc: hằng CHUỖI **trong** literal `CONG_CU`/`KHA_NANG` (AST — chú thích KHÔNG
    nằm trong AST), và khối MÃ RÀO của `AGENTS.md` (không phải văn xuôi)."""
    with tempfile.TemporaryDirectory() as t:
        nen = _nap_guong(Path(t) / "nen")
        bang(nen.PROVIDER_NGUON_HONG is None,
             f"ĐỐI CHỨNG DƯƠNG hỏng — cây gương phải đọc được ba nguồn: {nen.PROVIDER_NGUON_HONG}")
        bang(nen.PROVIDER_CHO_PHEP == bnv2.PROVIDER_CHO_PHEP,
             f"cây gương lệch cây thật: {sorted(nen.PROVIDER_CHO_PHEP)} "
             f"≠ {sorted(bnv2.PROVIDER_CHO_PHEP)}")
    bang_tan_cong = (
        ("chú thích cuối launcher.py", "ke_gian_1",
         {"bom_launcher": "\n# ghi chu vo thuong: provider ke_gian_1 qua execution_surface x\n"}),
        ("chuỗi NGOÀI hai bảng", "ke_gian_2",
         {"bom_launcher": '\n_GHI_CHU = "provider ke_gian_2 qua execution_surface x"\n'}),
        ("docstring cuối launcher.py", "ke_gian_3",
         {"bom_launcher": '\ndef _x():\n    """provider ke_gian_3 qua execution_surface x"""\n'}),
        ("văn xuôi trong AGENTS.md", "ke_gian_4",
         {"bom_agents": "\nprovider: ke_gian_4\n"}),
    )
    # HƯỚNG THỨ NĂM — đúng vector cross-review dùng (P2 trên `5a78c15`): không thêm dòng
    # mới, mà SỬA CHÍNH chuỗi lý do của một mục có sẵn trong `CONG_CU`. Bản vá trước thu hẹp
    # từ "toàn tệp" xuống "dưới hai bảng" nhưng vẫn ĐỌC PROSE, nên lỗ chỉ đổi chỗ. Không
    # dùng `bom_*` được vì phải sửa nội dung sẵn có, nên nó là một ca riêng ngay dưới.
    with tempfile.TemporaryDirectory() as t:
        van = (GOC / ".claude" / "dev" / "launcher.py").read_text(encoding="utf-8")
        cu_ = "duong du phong/chan doan GitHub"
        dung(cu_ in van, f"KHÔNG ĐO ĐƯỢC: không tìm thấy chuỗi lý do {cu_!r} để sửa")
        mod = _nap_guong(Path(t) / "g5", bom_launcher="")
        # dựng lại cây gương với chuỗi ĐÃ SỬA (không thêm dòng, chỉ đổi nội dung có sẵn)
        d = Path(t) / "g5b"
        (d / "ops").mkdir(parents=True); (d / ".claude" / "dev").mkdir(parents=True)
        (d / "docs").mkdir(parents=True)
        shutil.copyfile(Path(bnv2.__file__), d / "ops" / "bien_nhan_v2.py")
        shutil.copyfile(GOC / "AGENTS.md", d / "AGENTS.md")
        shutil.copyfile(GOC / "docs" / "PROTOCOL_DA_PHIEN.md", d / "docs" / "PROTOCOL_DA_PHIEN.md")
        (d / ".claude" / "dev" / "launcher.py").write_bytes(
            van.replace(cu_, "provider ke_gian_5 qua execution_surface forged", 1).encode("utf-8"))
        sp = importlib.util.spec_from_file_location("bnv2_g5b", d / "ops" / "bien_nhan_v2.py")
        m5 = importlib.util.module_from_spec(sp); sp.loader.exec_module(m5)
        bang("ke_gian_5" not in m5.PROVIDER_CHO_PHEP,
             "sửa CHÍNH chuỗi lý do của một mục `CONG_CU` vẫn NỚI được danh sách CHO PHÉP")
        bang(m5.PROVIDER_CHO_PHEP == mod.PROVIDER_CHO_PHEP,
             f"sửa prose làm đổi tập provider: {sorted(m5.PROVIDER_CHO_PHEP)}")
    hong = []
    for i, (ten, ke_gian, kw) in enumerate(bang_tan_cong):
        with tempfile.TemporaryDirectory() as t:
            mod = _nap_guong(Path(t) / f"g{i}", **kw)
            if ke_gian in mod.PROVIDER_CHO_PHEP:
                hong.append(f"{ten}: NỚI được danh sách CHO PHÉP bằng văn bản tự do")
    bang(not hong, f"{len(hong)}/{len(bang_tan_cong)} hướng nới được:\n      "
                   + "\n      ".join(hong))


@ca
def c36_provider_KHONG_mang_theo_quyen_cua_provider_khac():
    """MA TRẬN: mọi mức assurance bị cấm × mọi provider có hợp đồng — không chỉ mức/tên ĐẦU.

    `R6-01` đo được **bốn** phép làm yếu sống sót vì ca cũ chỉ thử **giá trị mà fixture
    chọn**: giao `cam` với `{cross_approved}` mất hai mức còn lại; đặt `hop_le=None` cho ba
    provider ngoài hai tên ca dùng thì ba provider ấy mất kiểm bề mặt. *"Một ca mỗi TÊN là
    SÀN của độ phủ, không phải TRẦN"* — ở đây là một ca mỗi GIÁ TRỊ."""
    # (a) bảng cấm của cổng phải khớp TUYỆT ĐỐI bản đóng băng chép từ `AGENTS.md` §4.
    bang(({k: tuple(sorted(v)) for k, v in bnv2.ASSURANCE_CAM_THEO_PROVIDER.items()}
          == {k: tuple(sorted(v)) for k, v in ASSURANCE_CAM_DONG_BANG.items()}),
         f"`ASSURANCE_CAM_THEO_PROVIDER` LỆCH bản đóng băng: "
         f"cổng={ {k: sorted(v) for k, v in bnv2.ASSURANCE_CAM_THEO_PROVIDER.items()} } "
         f"đóng băng={ {k: sorted(v) for k, v in ASSURANCE_CAM_DONG_BANG.items()} }")
    hong = []
    # (b) MỖI mức cấm × MỖI provider bị cấm.
    for prov, muc in sorted(ASSURANCE_CAM_DONG_BANG.items()):
        hd = bnv2.PROVIDER_HOP_DONG.get(prov)
        dung(hd, f"KHÔNG ĐO ĐƯỢC: provider bị cấm {prov!r} không có hợp đồng")
        for m in muc:
            with tempfile.TemporaryDirectory() as t:
                d = v2_du()
                d["model_reviewer_identity"] = {"provider": prov,
                                                "surface": sorted(hd["be_mat"])[0],
                                                "session_run_id": "f" * 32}
                d["assurance"] = m
                tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
                n, loi = _kiem(tmp, allowlist={}, no_da_do={})
                if not (n >= 1 and any("KHÔNG được tự tạo" in x for x in loi)):
                    hong.append(f"{prov} + {m}: không bị chặn ({loi})")
    # (c) MỖI provider có hợp đồng × một bề mặt của provider KHÁC (không bịa tên nào).
    for prov, hd in sorted(bnv2.PROVIDER_HOP_DONG.items()):
        khac = sorted(set().union(*[v["be_mat"] for k, v in bnv2.PROVIDER_HOP_DONG.items()
                                    if k != prov]) - set(hd["be_mat"]))
        dung(khac, f"KHÔNG ĐO ĐƯỢC: không có bề mặt của provider khác để mượn thử cho {prov}")
        with tempfile.TemporaryDirectory() as t:
            d = v2_du()
            d["model_reviewer_identity"] = {"provider": prov, "surface": khac[0],
                                            "session_run_id": "f" * 32}
            d["assurance"] = "review_deferred"
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            if not (n >= 1 and any("không phải bề mặt của provider" in x for x in loi)):
                hong.append(f"{prov} + bề mặt mượn {khac[0]!r}: không bị chặn ({loi})")
    # (d) vận chuyển SAI.
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["model_reviewer_identity"] = {"provider": "openai_chatgpt", "surface": "chatgpt_web",
                                        "transport": "machine", "session_run_id": "f" * 32}
        d["assurance"] = "cross_approved"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        if not (n >= 1 and any("không phải vận chuyển của provider" in x for x in loi)):
            hong.append(f"vận chuyển SAI: không bị chặn ({loi})")
    # (e) provider KHÔNG hợp đồng khai mức có thẩm quyền — tên được nhét TAY vào danh sách CHO
    # PHÉP, tức đúng đường "nới quyền" thật. `R7-02`: bản trước mượn `human` từ tập
    # `PROVIDER_KHONG_HOP_DONG` làm đại diện; tập ấy đã bị gỡ (human có hợp đồng trong nguồn),
    # nên "có tên mà không hợp đồng" chỉ còn dựng được bằng cách làm đúng việc kẻ nới quyền làm.
    cho_phep_that = bnv2.PROVIDER_CHO_PHEP
    bnv2.PROVIDER_CHO_PHEP = cho_phep_that | {"ke_gian_co_ten_khong_hop_dong"}
    try:
        with tempfile.TemporaryDirectory() as t:
            d = v2_du()
            d["model_reviewer_identity"] = {"provider": "ke_gian_co_ten_khong_hop_dong",
                                            "surface": "x", "session_run_id": "f" * 32}
            d["assurance"] = "cross_approved"
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            if not (n >= 1 and any("KHÔNG có hợp đồng" in x for x in loi)):
                hong.append(f"provider KHÔNG hợp đồng (nhét tay vào CHO PHÉP): không bị chặn ({loi})")
    finally:
        bnv2.PROVIDER_CHO_PHEP = cho_phep_that
    bang(not hong, f"{len(hong)} nhánh KHÔNG bị chặn:\n      " + "\n      ".join(hong[:8]))
    # ĐỐI CHỨNG DƯƠNG — chốt không được bắt oan một lượt advisory hợp lệ.
    with tempfile.TemporaryDirectory() as t:
        d = v2_du()
        d["model_reviewer_identity"] = {"provider": "openai_chatgpt", "surface": "chatgpt_web",
                                        "transport": "human_mediated", "session_run_id": "f" * 32}
        d["assurance"] = "advisory_review"
        tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"ĐỐI CHỨNG: ChatGPT Web khai `advisory_review` phải QUA, được: {loi}")


@ca
def c37_URL_phai_neo_DUNG_duong_dan_bien_nhan_khai():
    """Hai trường cùng nói về MỘT tệp mà không ai so chúng với nhau.

    Connector (P2 trên `670071b`): `verdict_path` chỉ bị kiểm "không rỗng", còn `_neo_git`
    chỉ xác minh đường dẫn PHÂN TÍCH TỪ URL — nên khai một `verdict_path` không liên quan mà
    `evidence_url` trỏ tệp BẤT KỲ có băm trùng `verdict_sha256` thì vẫn qua."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_neo(sha, bam, duong)
        d["verdict_path"] = "ops/reviews/mot-tep-KHAC-han.md"      # URL vẫn trỏ `duong`
        _ghi_bn(tmp, d)
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 1 and "KHÔNG neo thứ nó khai" in loi[0],
             f"`verdict_path` lệch đường dẫn trong URL phải ĐỎ, được: {loi}")
    # `lstrip("./")` BÓC MỌI dấu chấm và gạch chéo — cả `../../x` lẫn `/x` đều chuẩn hoá về
    # `x` rồi KHỚP URL, trong khi trường THÔ mà người đọc mở lại trỏ tệp khác (P2 trên
    # `5a78c15`). Bản chuẩn hoá tự viết thứ hai trong tệp này làm nhiều hơn tên gọi của nó.
    # `R7-04`: HAI assertion, không phải một. "Được NHẬN (0 lỗi)" và "đỏ nhưng SAI LÝ DO" là hai
    # thuộc tính khác nhau; gộp vào một `bang` thì mutant `m43` cũ (chỉ đổi thông báo từ chối,
    # đường dẫn thoát vẫn bị chặn ở chốt so URL) lĩnh tín dụng cho thuộc tính "traversal được
    # nhận" mà nó chưa từng dựng lại. Nay `m43` phục hồi `.lstrip("./")` thật, và phải chết ở
    # assertion ĐẦU — receipt sai thành 0 lỗi — chứ không phải ở assertion sau.
    for tien_to in ("../../", "/"):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
            d = _bn_neo(sha, bam, duong)
            d["verdict_path"] = tien_to + duong
            _ghi_bn(tmp, d)
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            bang(n >= 1, f"`verdict_path: {tien_to + duong}` được NHẬN (0 lỗi) — đường dẫn thoát "
                         f"chuẩn hoá về đường dẫn trong URL rồi khớp")
            bang(n == 1 and "không phải đường dẫn tương đối gốc kho" in loi[0],
                 f"`verdict_path: {tien_to + duong}` đỏ nhưng SAI LÝ DO/SỐ LỖI: {loi}")
    # ĐỐI CHỨNG: `./` dẫn đầu là hợp lệ và phải QUA — chốt không được siết quá tay.
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_neo(sha, bam, duong); d["verdict_path"] = "./" + duong
        _ghi_bn(tmp, d)
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"ĐỐI CHỨNG: `./` dẫn đầu phải QUA, được: {loi}")
    # ĐỐI CHỨNG: khớp thì sạch (đã có `c18`, nhắc lại ở đây để chốt không bắt oan).
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        _ghi_bn(tmp, _bn_neo(sha, bam, duong))
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n == 0, f"ĐỐI CHỨNG: `verdict_path` khớp URL phải QUA, được: {loi}")


@ca
def c38_BI_DANH_phai_duoc_CHUAN_HOA_truoc_moi_phep_kiem():
    """Một bí danh không được chuẩn hoá là đường vòng quanh ràng buộc của tên nó trỏ tới.

    Hai lượt liên tiếp bắt đúng chỗ này, mỗi lượt một nửa. Phiên thi công tự tìm nửa đầu
    (`anthropic` + bề mặt **bịa** ⇒ 0 vi phạm) và vá bằng cách cho bí danh mượn **hợp nhất
    mọi bề mặt** — rồi cross-review (P1 trên `5a78c15`) đo nửa sau: `anthropic` +
    `chatgpt_web` + `cross_approved` vẫn 0 vi phạm, vì bí danh **mượn được bề mặt của
    provider khác** và luật assurance thì khoá theo TÊN. Vá nửa vời còn tệ hơn không vá: nó
    làm chỗ ấy trông như đã đóng. Nay bí danh được **chuẩn hoá TRƯỚC** mọi phép kiểm."""
    dung(bnv2.PROVIDER_BI_DANH, "KHÔNG ĐO ĐƯỢC: không đọc được bảng bí danh")
    for bd, chinh_tac in sorted(bnv2.PROVIDER_BI_DANH.items()):
        hd = bnv2.PROVIDER_HOP_DONG.get(chinh_tac) or {"be_mat": frozenset()}
        lam = sorted(set().union(*[v["be_mat"] for v in bnv2.PROVIDER_HOP_DONG.values()])
                     - set(hd["be_mat"]))
        dung(lam, f"KHÔNG ĐO ĐƯỢC: không có bề mặt nào của provider KHÁC để mượn thử")
        for be_mat, vi_sao in (("banana", "bề mặt BỊA"), (lam[0], f"bề mặt MƯỢN {lam[0]!r}")):
            with tempfile.TemporaryDirectory() as t:
                d = v2_du()
                d["model_reviewer_identity"] = {"provider": bd, "surface": be_mat,
                                                "session_run_id": "f" * 32}
                d["assurance"] = "cross_approved"
                tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
                n, loi = _kiem(tmp, allowlist={}, no_da_do={})
                bang(n >= 1 and any("không phải bề mặt của provider" in x for x in loi),
                     f"bí danh {bd!r} + {vi_sao} phải ĐỎ, được: {loi}")
        # ĐỐI CHỨNG: bề mặt THẬT của tên chính tắc phải QUA — chốt không được bắt oan hiện vật.
        with tempfile.TemporaryDirectory() as t:
            d = v2_du()
            d["model_reviewer_identity"] = {"provider": bd, "surface": sorted(hd["be_mat"])[0],
                                            "session_run_id": "f" * 32}
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            bang(n == 0, f"ĐỐI CHỨNG: {bd!r} + bề mặt của {chinh_tac!r} phải QUA, được: {loi}")
    # NEO CHO HIỆN VẬT: mọi biên nhận ĐANG ĐẠT v2 phải nằm trong hợp đồng — không có neo
    # thì bảng bí danh là một danh sách bịa, đặt đúng chỗ nguy nhất có thể đặt nó.
    import yaml as _y
    tm = GOC / bnv2.THU_MUC
    dung(tm.is_dir(), f"KHÔNG ĐO ĐƯỢC: thiếu {tm}")
    ngoai = []
    for f in sorted(tm.glob("*.receipt.yaml")):
        d = _y.safe_load(f.read_text(encoding="utf-8")) or {}
        if not isinstance(d, dict) or bnv2._thieu(d):
            continue
        mri = d.get("model_reviewer_identity") or {}
        pv = bnv2._chuan_hoa_provider(str(mri.get("provider") or ""))
        hd = bnv2.PROVIDER_HOP_DONG.get(pv)
        bm = str(mri.get("surface") or "")
        if hd and bm and bm not in hd["be_mat"]:
            ngoai.append(f"{f.name}: {pv}/{bm}")
    bang(not ngoai, f"{len(ngoai)} biên nhận ĐANG ĐẠT dùng bề mặt ngoài hợp đồng:\n      "
                    + "\n      ".join(ngoai[:5]))


@ca
def c39_bam_fixture_phai_LAY_TU_GIT_khong_tu_chuoi_Python():
    """Bất biến chống trôi-theo-nền: băm fixture phải là băm THỨ GIT LƯU, không phải chuỗi.

    NÓI THẲNG PHẠM VI: trên POSIX ca này gần như không thể ĐỎ, vì `\n` trên đĩa bằng `\n`
    trong chuỗi — nên **đột biến của nó chỉ có răng trên Windows**, và tôi KHÔNG dựng một
    mutant giả vờ có răng ở đây. Phản chứng THẬT của nó là một phép đo có thật, không phải
    một giả thuyết: lượt CI Windows ĐẦU TIÊN của bộ này (`e057edb`,
    `gate (windows-latest)` job `101524189479`) cho **`40/41 ca`** — `c32` ĐỎ ngay ở đối
    chứng dương vì `_kho_git_re_nhanh` băm `than_verdict.encode()` trong khi `write_text`
    đã dịch `\n` → `\r\n` lúc ghi đĩa.

    Đây đúng là `R2-02` — *"băm hai BIỂU DIỄN của cùng một thứ"* — mà PR này đã vá cho SẢN
    PHẨM ở vòng 3, rồi tái phát trong FIXTURE của chính nó. Ca này khoá bất biến ấy ở dạng
    kiểm được trên mọi nền: giá trị trả về phải khớp `git cat-file -p <commit>:<đường dẫn>`."""
    import hashlib as _h
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for ten, dung_ham in (("_kho_git", False), ("_kho_git_hai_commit", True)):
            d = tmp / ten
            d.mkdir()
            if dung_ham:
                _nen, sha, bam, duong = _kho_git_hai_commit(d, "noi dung verdict\n")
            else:
                sha, bam, duong = _kho_git(d, "noi dung verdict\n")
            r = subprocess.run(["git", "-C", str(d), "cat-file", "-p", f"{sha}:{duong}"],
                               capture_output=True)
            dung(r.returncode == 0, f"KHÔNG ĐO ĐƯỢC: không đọc lại được blob của {ten}")
            bang(bam == _h.sha256(r.stdout).hexdigest(),
                 f"{ten}: băm fixture KHÔNG phải băm thứ git lưu — "
                 f"fixture={bam[:12]}… git={_h.sha256(r.stdout).hexdigest()[:12]}…")


@ca
def c40_R7_01_nguon_hong_tren_bien_nhan_THAT_khong_ket_toi_bien_nhan_nao():
    """Phản chứng NGUYÊN VĂN của `R7-01`, chạy trên chính hiện vật của kho (68 biên nhận lúc đo).

    Reviewer chép cổng vào một cây tạm, làm hỏng RIÊNG nguồn ở cây ấy rồi chạy `--root <kho thật>`:
    thiếu `launcher.py` ⇒ `rc=2` nhưng **11 vi phạm oan** (`openai_codex`/`anthropic` "không hợp
    đồng"); surface/transport Codex thành `None` ⇒ `rc=1`, 9 và 1 biên nhận nguyên byte bị KẾT
    TỘI, **0 chưa đo**. Cây gương của `c28` không chạm được nhánh ấy vì fixture của nó không khai
    assurance. Ca này đo đúng thứ reviewer đo: NGUỒN hỏng ⇒ `rc=2`, KHÔNG dòng ĐỎ nào, KHÔNG
    traceback — trên biên nhận thật, không phải fixture."""
    dung((GOC / bnv2.THU_MUC).is_dir() and (GOC / ".git").exists(),
         "KHÔNG ĐO ĐƯỢC: không phải kho thật (thiếu ops/reviews hoặc .git)")
    for ten, kw, phai_co in (
        ("đủ nguồn (đối chứng)", {}, "TỔNG: ĐẠT"),
        ("thiếu launcher.py", {"co_launcher": False}, "không đọc được nguồn từ vựng"),
        ("surface Codex là None",
         {"sua_launcher": _thay_1(HANG_CODEX, '    ("openai_codex", ("codex",), None, "machine"),')},
         "cột `execution_surface` = None"),
        ("transport Codex là None",
         {"sua_launcher": _thay_1(HANG_CODEX, '    ("openai_codex", ("codex",), "codex_cli", None),')},
         "cột `transport` = None"),
    ):
        with tempfile.TemporaryDirectory() as t:
            cong = _cay_guong(Path(t), kho_rieng=False, **kw)
            r = subprocess.run([sys.executable, str(cong), "--root", str(GOC)],
                               capture_output=True, text=True)
            hop = r.stdout + r.stderr
            ket_toi = [x for x in r.stderr.splitlines() if x.startswith("  ĐỎ")]
            bang("Traceback" not in hop, f"{ten}: cổng CHẾT bằng traceback:\n{r.stderr[-400:]}")
            bang(phai_co in hop, f"{ten}: thiếu bằng chứng dương {phai_co!r}: {hop[-400:]!r}")
            if not kw:
                bang(r.returncode == 0 and not ket_toi,
                     f"ĐỐI CHỨNG: kho thật với đủ nguồn phải sạch, rc={r.returncode}, ĐỎ={len(ket_toi)}")
                continue
            bang(r.returncode == 2, f"{ten}: đòi rc=2 (KHÔNG ĐO ĐƯỢC), được {r.returncode}")
            bang(not ket_toi,
                 f"{ten}: {len(ket_toi)} biên nhận THẬT bị KẾT TỘI vì lỗi ở NGUỒN:\n      "
                 + "\n      ".join(x[:140] for x in ket_toi[:5]))
            bang("KHÔNG ĐO ĐƯỢC danh sách provider" in r.stderr,
                 f"{ten}: phải khai lỗi nguồn ở trạng thái thứ ba: {r.stderr[-300:]!r}")


def _bn_human(sha, bam, duong):
    """Biên nhận v2 human-audit TỐI THIỂU theo `PROTOCOL §8` mục 2: người audit khai danh tính
    (`github_submitter_identity.actor`), độc lập với executor (`phien_doc_lap: true`), không có
    session máy (`KHONG_do_duoc` nói rõ), verdict bền neo vào exact `reviewed_sha` (mỏ neo git của
    bản chiếu). Đây là FIXTURE dựng từ lược đồ, không phải một audit thật, và không nâng hai biên
    nhận human lịch sử (đang là nợ v1) lên v2 bằng suy đoán."""
    d = _bn_neo(sha, bam, duong)
    d["model_reviewer_identity"] = {"provider": "human", "surface": "manual_audit",
                                    "transport": "human", "phien_doc_lap": True,
                                    "KHONG_do_duoc": "audit thủ công — không có session máy để neo"}
    d["github_submitter_identity"] = {"actor": "nguoi-audit"}
    d["assurance"] = "human_audited"
    return d


@ca
def c41_human_audit_theo_PROTOCOL_8_QUA_va_muc_MO_HINH_cho_nguoi_bi_chan():
    """`R7-02`: `human` từng bị chép tay vào tập "không hợp đồng" và cấm cả `human_audited`.

    Phân vùng suy từ HỢP ĐỒNG vận chuyển, hai chiều: (c) người audit khai đủ §8 phải QUA cả trong
    tiến trình lẫn CLI; (d) người khai mức của MÔ HÌNH phải ĐỎ; (e) người không khai độc lập phải
    ĐỎ; (f) MÔ HÌNH khai `human_audited` phải ĐỎ — mặt thứ ba của cùng lớp, chưa ai chỉ; (g) bằng
    chứng human chỉ là comment GitHub ⇒ `protected_evidence_ref` ⇒ trạng thái THỨ BA, không phải
    sạch, không phải vi phạm. Oracle (a)/(b) chép tay từ protocol và bảng chuyển tiếp."""
    # (a) oracle phân vùng đóng băng.
    bang(bnv2.VAN_CHUYEN_NGUOI == VAN_CHUYEN_NGUOI_DONG_BANG
         and tuple(sorted(bnv2.ASSURANCE_CUA_NGUOI)) == ASSURANCE_CUA_NGUOI_DONG_BANG
         and tuple(sorted(bnv2.ASSURANCE_CUA_MO_HINH)) == ASSURANCE_CUA_MO_HINH_DONG_BANG,
         f"phân vùng người/mô hình LỆCH bản đóng băng: người={sorted(bnv2.ASSURANCE_CUA_NGUOI)} "
         f"mô hình={sorted(bnv2.ASSURANCE_CUA_MO_HINH)} vận chuyển người={bnv2.VAN_CHUYEN_NGUOI!r}")
    # (b) hợp đồng human phải nằm trong NGUỒN CÓ CẤU TRÚC (đọc bằng AST riêng), đúng bộ ba.
    hang_human = [r for r in _doc_bang_launcher("_PROVIDER_NGOAI_CLI") if r and r[0] == "human"]
    dung(hang_human, "KHÔNG ĐO ĐƯỢC: `_PROVIDER_NGOAI_CLI` trong launcher.py chưa có hàng `human` — "
                     "đường human-audit không đo được trên cây này (R7-02 đòi hàng "
                     "`(\"human\", \"manual_audit\", \"human\")`)")
    bang(tuple(hang_human[0]) == ("human", "manual_audit", "human"),
         f"bộ ba human trong nguồn LỆCH bảng chuyển tiếp: {hang_human[0]}")
    bang(bnv2.PROVIDER_HOP_DONG.get("human") == HOP_DONG_HUMAN_DONG_BANG,
         f"cổng đọc hợp đồng human ra {bnv2.PROVIDER_HOP_DONG.get('human')!r}")
    # (c) DƯƠNG.
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        _ghi_bn(tmp, _bn_human(sha, bam, duong))
        loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
        bang(not loi and not tk.get("chua_do"),
             f"human-audit v2 đủ §8 bị từ chối: loi={loi} chua_do={tk.get('chua_do')}")
        r = subprocess.run([sys.executable, str(CONG), "--root", str(tmp)],
                           capture_output=True, text=True)
        bang(r.returncode == 0 and "TỔNG: ĐẠT" in r.stdout,
             f"CLI với human-audit hợp lệ: đòi rc=0 + TỔNG: ĐẠT, được {r.returncode}\n{r.stderr[-300:]}")
    # (d) ÂM: NGƯỜI khai mức của MÔ HÌNH — từng mức.
    for m in ASSURANCE_CUA_MO_HINH_DONG_BANG:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
            d = _bn_human(sha, bam, duong); d["assurance"] = m
            _ghi_bn(tmp, d)
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            bang(n >= 1 and any(f"KHÔNG được tự tạo `{m}`" in x and "NGƯỜI" in x for x in loi),
                 f"human + `{m}` phải ĐỎ đúng lý do (mức của mô hình), được: {loi}")
    # (e) ÂM: NGƯỜI khai `human_audited` mà KHÔNG khai độc lập.
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_human(sha, bam, duong); d["model_reviewer_identity"].pop("phien_doc_lap")
        _ghi_bn(tmp, d)
        n, loi = _kiem(tmp, allowlist={}, no_da_do={})
        bang(n >= 1 and any("bằng chứng phiên độc lập" in x for x in loi),
             f"human_audited mà không khai độc lập phải ĐỎ, được: {loi}")
    # (f) ÂM: MÔ HÌNH khai `human_audited` — mọi provider có hợp đồng vận chuyển KHÁC `human`,
    # danh sách lấy từ launcher bằng AST riêng, không hỏi cổng.
    mo_hinh = {}
    for prov, be_mat, van_chuyen in (_doc_bang_launcher("_TRANSPORT_CONTRACTS")
                                     + _doc_bang_launcher("_PROVIDER_NGOAI_CLI")):
        if van_chuyen != VAN_CHUYEN_NGUOI_DONG_BANG:
            mo_hinh.setdefault(prov, be_mat)
    dung(mo_hinh, "KHÔNG ĐO ĐƯỢC: không có provider mô hình nào trong nguồn")
    for prov, be_mat in sorted(mo_hinh.items()):
        with tempfile.TemporaryDirectory() as t:
            d = v2_du()
            d["model_reviewer_identity"] = {"provider": prov, "surface": be_mat,
                                            "session_run_id": "f" * 32}
            d["assurance"] = "human_audited"
            tmp = _cay(Path(t), {"a-verdict.receipt.yaml": d})
            n, loi = _kiem(tmp, allowlist={}, no_da_do={})
            bang(n >= 1 and any("KHÔNG được tự tạo `human_audited`" in x for x in loi),
                 f"mô hình {prov!r} khai `human_audited` phải ĐỎ, được: {loi}")
    # (g) TRẠNG THÁI THỨ BA: evidence của người audit chỉ là comment GitHub.
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        sha, bam, duong = _kho_git(tmp, "noi dung verdict\n")
        d = _bn_human(sha, bam, duong)
        d["anchor"]["loai"] = "protected_evidence_ref"
        d["evidence_url"] = "https://github.com/o/r/pull/1#issuecomment-1"
        _ghi_bn(tmp, d)
        loi, tk = bnv2.kiem(tmp, allowlist={}, no_da_do={})
        bang(not loi and any("CHƯA có đường đo" in x for x in (tk.get("chua_do") or [])),
             f"evidence human không đo được phải là trạng thái THỨ BA: loi={loi} chua_do={tk.get('chua_do')}")


@ca
def c42_hai_builder_cay_guong_cung_nguon_phai_cho_CUNG_hanh_vi_tren_bien_nhan_THAT():
    """`R7-03`: nguồn KHÔNG đổi qua cả hai builder ⇒ hợp đồng/bí danh/trạng thái nguồn bằng gốc,
    và `_mri`/`_thieu` cho CÙNG kết quả trên MỌI biên nhận nguyên byte của kho.

    Reviewer đo được một biên nhận lịch sử (`phan-bien-quy-trinh-review-1-claude`) mà gốc nhận
    còn gương từ chối — do rig, không do sản phẩm. RĂNG của ca này là ca TỰ KIỂM `m53` (rig làm
    hỏng nguồn phụ phải bị phân giàn giáo TRƯỚC khi ca đích chạy), không phải một đột biến sản
    phẩm — nói thẳng kẻo ai đếm nó vào cột "có đột biến"."""
    import yaml as _y
    tm = GOC / bnv2.THU_MUC
    dung(tm.is_dir(), f"KHÔNG ĐO ĐƯỢC: thiếu {tm}")
    bien_nhan = [(p.name, _y.safe_load(p.read_text(encoding="utf-8")))
                 for p in sorted(tm.glob("*.receipt.yaml"))]
    bien_nhan = [(n, d) for n, d in bien_nhan if isinstance(d, dict)]
    dung(bien_nhan, "KHÔNG ĐO ĐƯỢC: không có biên nhận nào")
    goc_mod = bnv2

    def _so(mod, nhan):
        for k in ("PROVIDER_HOP_DONG", "PROVIDER_BI_DANH", "PROVIDER_NGUON_HONG", "PROVIDER_CHO_PHEP"):
            bang(getattr(mod, k) == getattr(goc_mod, k),
                 f"{nhan}: `{k}` LỆCH gốc — {getattr(mod, k)!r} != {getattr(goc_mod, k)!r}")
        lech = [n for n, d in bien_nhan
                if mod._thieu(d) != goc_mod._thieu(d) or mod._mri(d) != goc_mod._mri(d)]
        bang(not lech, f"{nhan}: {len(lech)}/{len(bien_nhan)} biên nhận THẬT cho kết quả KHÁC gốc: {lech[:5]}")

    with tempfile.TemporaryDirectory() as t:
        _so(_nap_guong(Path(t) / "g"), "_nap_guong (không bơm)")
    # Builder thứ hai: `_dot_bien_tep` với một đột biến KHÔNG đổi hành vi (chỉ chạm một docstring).
    mod_cu, cong_cu = globals()["bnv2"], globals()["CONG"]
    try:
        _dot_bien_tep('"""Trạng thái thứ ba. KHÔNG được đọc thành \'sạch\'."""',
                      '"""Trạng thái thứ ba. KHÔNG được đọc thành \'sạch\'. (c42)"""')
        _so(globals()["bnv2"], "_dot_bien_tep (đột biến rỗng hành vi)")
    finally:
        globals()["bnv2"], globals()["CONG"] = mod_cu, cong_cu
        while _TAM_DOT_BIEN:
            shutil.rmtree(_TAM_DOT_BIEN.pop(), ignore_errors=True)


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


@ca
def c43_bang_neo_luat_cua_san_pham_phai_khop_ORACLE_chep_tay():
    """`R8-01`: bảng neo của sản phẩm là TẬP CON KHÔNG ĐƯỢC CO của oracle chép tay.

    Vì sao cần một ca riêng chứ không để `c28` gánh: `c28` xoá câu neo trong NGUỒN rồi đo cổng.
    Phép làm yếu ở đây đi lối khác — bỏ một MỤC khỏi `_NEO_LUAT_CHEP_TAY` — và nếu fixture còn
    lấy danh sách neo từ chính bảng ấy (bản trước) thì nó thôi xoá câu tương ứng, nguồn còn
    nguyên, cổng rc=0 và MỌI ca xanh. Fixture co theo đúng thứ nó phải canh. Oracle nằm ở
    `NEO_LUAT_DONG_BANG` — chép tay từ hai nguồn phụ, không import từ cổng."""
    bang(tuple(bnv2._NEO_LUAT_CHEP_TAY) == NEO_LUAT_DONG_BANG,
         f"`_NEO_LUAT_CHEP_TAY` LỆCH oracle chép tay:\n  sản phẩm={tuple(bnv2._NEO_LUAT_CHEP_TAY)}\n"
         f"  oracle  ={NEO_LUAT_DONG_BANG}")
    # …và mỗi câu của oracle phải CÓ THẬT, đúng một chỗ, trong nguồn nó khai. Thiếu chốt này thì
    # một oracle chép sai (câu không tồn tại) làm `c28` xoá hụt và cả hai lượt xanh mà không đo gì.
    for luat, tep_neo, cau in NEO_LUAT_DONG_BANG:
        n = (GOC / tep_neo).read_text(encoding="utf-8").count(cau)
        bang(n == 1, f"câu neo của `{luat}` khớp {n} chỗ trong `{tep_neo}`, đòi ĐÚNG 1")


@ca
def c44_bo_ba_provider_phai_KHOP_nguon_ke_hoach_va_hang_LECH_phai_doi_hanh_vi():
    """`R8-05`: `launcher.py` là NGUỒN CÓ CẤU TRÚC của hợp đồng — lệch nguồn là chặn/nhận sai.

    Ba tầng, vì hai tầng đầu chỉ so chuỗi và không chứng minh hàng ấy QUYẾT ĐỊNH điều gì:
      (a) mỗi bộ ba của oracle chép tay phải có trong bảng `launcher.py`, **đúng cả cột vận chuyển**;
      (b) oracle chép tay phải khớp CHÍNH bảng §2 của kế hoạch — kẻo oracle và nguồn cùng trôi;
      (c) WITNESS ĐỐI XỨNG trên cây gương: với hàng THẬT, biên nhận Antigravity khai TRUNG THỰC
          `machine/local` phải ĐƯỢC NHẬN; với hàng LỆCH (`machine`, đúng bản trước bản vá) chính
          biên nhận ấy phải BỊ TỪ CHỐI. Không có (c) thì (a)/(b) chỉ là hai chuỗi bằng nhau."""
    # (a) bảng launcher ⊇ oracle, khớp từng cột
    hang = {(r[0], r[-2]): r for r in (_doc_bang_launcher("_TRANSPORT_CONTRACTS")
                              + _doc_bang_launcher("_PROVIDER_NGOAI_CLI")) if r}
    for prov, be_mat, van_chuyen in BO_BA_PROVIDER_DONG_BANG:
        r = hang.get((prov, be_mat))
        bang(r is not None, f"`{prov}`/`{be_mat}` KHÔNG có hàng nào trong bảng của launcher.py")
        bang(r[-2:] == [be_mat, van_chuyen],
             f"hàng `{prov}` LỆCH oracle §2: launcher={r[-2:]} oracle={[be_mat, van_chuyen]}")
    # (b) oracle ⊆ bảng §2 của kế hoạch, đọc Ô CUỐI chứ không dò substring (`machine` là tiền tố
    #     của `machine/local`, nên `in` sẽ khớp nhầm và chốt mất răng đúng chỗ cần nó nhất).
    van = (GOC / KE_HOACH_PROVIDER).read_text(encoding="utf-8")
    for prov, be_mat_s2, van_chuyen in BO_BA_PROVIDER_DONG_BANG:
        dong = [l for l in van.splitlines() if l.startswith("|") and f"`{prov}`" in l
                and f"`{be_mat_s2}`" in l]
        bang(len(dong) == 1,
             f"`{prov}`: tìm được {len(dong)} hàng trong §2 của `{KE_HOACH_PROVIDER}`, đòi ĐÚNG 1")
        o = [c.strip() for c in dong[0].strip("|").split("|")]
        bang(o[-1].strip("`") == van_chuyen,
             f"`{prov}`: §2 khai vận chuyển {o[-1]!r}, oracle chép tay {van_chuyen!r}")
        # `R9-F05`: đối chiếu CẢ cột surface, không chỉ transport. Bản trước chỉ so ô cuối, nên
        # lời khai "Antigravity là hàng DUY NHẤT lệch §2" rộng hơn phép đo — reviewer lượt 9 đổi
        # riêng ô surface trong bản sao kế hoạch và `c44` VẪN QUA.
        # Mỗi hàng §2 có đúng một surface máy; nợ tên Codex service ở #461
        # không được dùng làm ngoại lệ cho bảng contract hiện hành.
        bang(o[-2] == f"`{be_mat_s2}`",
             f"`{prov}`: §2 khai bề mặt {o[-2]!r}, đòi đúng một token `{be_mat_s2}`")
    # (c) witness đối xứng — hàng ấy phải ĐỔI HÀNH VI, không chỉ đổi chuỗi
    d = v2_du()
    d["model_reviewer_identity"].update(provider="google_antigravity", surface="antigravity",
                                        transport="machine/local")
    for nhan, kw, mong_nhan in (("hàng THẬT (machine/local)", {}, True),
                                ("hàng LỆCH (machine)",
                                 {"sua_launcher": _thay_1(HANG_AG,
                                  '    ("google_antigravity", "antigravity", "machine"),')}, False)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            cong = _cay_guong(tmp, kho_rieng=False, **kw)
            sp = importlib.util.spec_from_file_location(f"bnv2_ag_{abs(hash(nhan)) % 10**8}", cong)
            mod = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(mod)
            loi = mod._thieu(copy.deepcopy(d))
            # `R9-F04`: vế DƯƠNG đòi danh sách lỗi RỖNG, không phải "không có chữ transport".
            # Bản trước dùng `not any("transport" in x …)` nên một receipt hỏng vì lý do KHÁC
            # (reviewer đo bằng `receipt_id` rỗng ⇒ `_thieu` trả `thiếu/rỗng receipt_id`) vẫn
            # được đọc là ĐƯỢC NHẬN — đúng khoảng cách hành vi/diagnostic mà ca này định khoá.
            if mong_nhan:
                bang(loi == [],
                     f"{nhan}: biên nhận Antigravity khai TRUNG THỰC `machine/local` phải ĐƯỢC NHẬN "
                     f"SẠCH (0 lỗi), được {len(loi)} lỗi: {loi[:2]}")
            else:
                bang(any("transport" in x for x in loi),
                     f"{nhan}: phải BỊ TỪ CHỐI vì `transport`, được: {loi[:2]}")
                bang(not any("receipt_id" in x or "surface" in x for x in loi),
                     f"{nhan}: vế ÂM phải đỏ vì ĐÚNG transport, không vì trường khác: {loi[:2]}")


@ca
def c45_neo_canonical_ancestry_KHONG_song_sot_qua_land_bang_SQUASH():
    """`R8-06` — khoá TIỀN ĐỀ của một nợ đã khai, KHÔNG khoá chính sách land của kho.

    Cross-review lượt 8 (codex) kết luận master ĐỎ vì `#455` land bằng squash. **Kết luận SAI**:
    `origin/master` là MERGE commit (hai cha) và cả bảy neo ĐỀU là tổ tiên; cổng chạy trên chính
    `cacaba3` cho `rc=0`. Nhưng TIỀN ĐỀ thì ĐÚNG, và ca này là phản chứng chạy được cho nó: cùng
    một NỘI DUNG cây, land bằng merge thì neo còn là tổ tiên, land bằng squash thì KHÔNG.

    PHẠM VI — nói thẳng kẻo bị đọc rộng hơn: ca này KHÔNG đo kho thật và KHÔNG cưỡng chế
    "phải land bằng merge". Bất biến ấy sống ở GitHub (nút merge), ngoài tầm một ca test cục bộ;
    ép nó ở đây là **KHÔNG ĐO ĐƯỢC** đội lốt đã đo. Xem caveat có tên trong `ops/reviews/README.md`.

    `R9-F06` — MỆNH ĐỀ PHẢI HẸP ĐÚNG BẰNG PHÉP ĐO. Bản đầu viết *"đúng khi và chỉ khi land bằng
    MERGE COMMIT"*: **SAI**, vì **fast-forward cũng giữ nguyên neo** — reviewer lượt 9 đổi đúng
    lựa chọn merge trong fixture này sang FF và ca vẫn qua. Thứ phá quan hệ tổ tiên là **SQUASH**
    (thay commit của nhánh bằng một commit MỚI), và chỉ phá những neo **chưa** nằm sẵn trong lịch
    sử nhánh đích. Nên ca này nay đo **BA** lối land, không hai."""
    import subprocess as _sp
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        def g(*a, **kw):
            return _sp.run(["git", "-C", str(d), *a], capture_output=True, text=True, **kw)
        dung(g("init", "-q", "-b", "main", ".").returncode == 0, "KHÔNG ĐO ĐƯỢC: git init hỏng")
        g("config", "user.email", "t@t.t"); g("config", "user.name", "t")
        g("config", "commit.gpgsign", "false")      # CI ký commit; fixture không có khoá
        (d / "f").write_text("base\n"); g("add", "-A"); g("commit", "-qm", "base")
        g("checkout", "-qb", "nhanh")
        (d / "g").write_text("x\n"); g("add", "-A"); g("commit", "-qm", "neo")
        neo = g("rev-parse", "HEAD").stdout.strip()
        dung(len(neo) == 40, f"KHÔNG ĐO ĐƯỢC: không lấy được SHA neo: {neo!r}")
        # `R9-F03`: BA TRẠNG THÁI, không phải hai. Bản trước dùng `returncode != 0` cho vế squash,
        # nên `rc=128` (git KHÔNG ĐO ĐƯỢC: sai đối số, kho hỏng, object thiếu) được đếm y hệt
        # `rc=1` ("không phải tổ tiên") và ca vẫn XANH — reviewer lượt 9 bơm 128 vào đúng lời gọi
        # cuối, mọi lời gọi khác chạy thật, và ca QUA. Một ca không đo được tiền đề mà báo đạt thì
        # tệ hơn không có ca. Nay lỗi công cụ thành `LoiDungCa` (giàn giáo), không thành kết quả.
        def to_tien(sha, mo_ta):
            r = g("merge-base", "--is-ancestor", sha, "HEAD")
            dung(r.returncode in (0, 1),
                 f"KHÔNG ĐO ĐƯỢC quan hệ tổ tiên ({mo_ta}): git thoát {r.returncode}, "
                 f"chỉ 0/1 mới là câu trả lời — {r.stderr.strip()[:120]}")
            return r.returncode == 0

        def cay(ref):
            r = g("rev-parse", f"{ref}^{{tree}}")
            oid = r.stdout.strip()
            dung(r.returncode == 0 and len(oid) == 40 and all(c in "0123456789abcdef" for c in oid),
                 f"KHÔNG ĐO ĐƯỢC cây của `{ref}`: rc={r.returncode} oid={oid!r}")
            return oid

        g("checkout", "-q", "main")
        dung(g("merge", "-q", "--no-ff", "nhanh", "-m", "merge").returncode == 0,
             "KHÔNG ĐO ĐƯỢC: merge hỏng")
        bang(to_tien(neo, "sau MERGE"),
             "land bằng MERGE mà neo KHÔNG còn là tổ tiên — tiền đề của ca này sai")
        g("checkout", "-q", "-B", "main2", "main~1")
        dung(g("merge", "--squash", "nhanh").returncode == 0, "KHÔNG ĐO ĐƯỢC: merge --squash hỏng")
        g("commit", "-qm", "squash")
        bang(cay("main") == cay("HEAD"),
             "KHÔNG ĐO ĐƯỢC: hai lối land ra CÂY KHÁC nhau — phép so không còn cô lập lịch sử")
        bang(not to_tien(neo, "sau SQUASH"),
             "land bằng SQUASH mà neo VẪN là tổ tiên — nợ `canonical_ancestry` không còn như đã khai")
        # LỐI THỨ BA — FAST-FORWARD: cũng GIỮ neo, nên "chỉ merge commit mới giữ" là mệnh đề SAI.
        # Đo nó ở đây thay vì chỉ sửa câu chữ: một mệnh đề hẹp mà không có ca thì lần sau lại nới ra.
        g("checkout", "-q", "-B", "main3", "main~1")
        r_ff = g("merge", "-q", "--ff-only", "nhanh")
        dung(r_ff.returncode == 0, f"KHÔNG ĐO ĐƯỢC: fast-forward hỏng — {r_ff.stderr.strip()[:120]}")
        bang(to_tien(neo, "sau FAST-FORWARD"),
             "land bằng FAST-FORWARD mà neo MẤT tư cách tổ tiên — mệnh đề của caveat sai chiều")
        # TỰ KIỂM chính chốt ba trạng thái (`R9-F03`): hỏi quan hệ tổ tiên của một SHA KHÔNG TỒN
        # TẠI ⇒ git thoát 128 ⇒ phải thành `LoiDungCa` (giàn giáo), KHÔNG thành "không phải tổ
        # tiên". Nghĩ ra phép thử mà không chạy thì phép thử ấy không tồn tại.
        try:
            to_tien("0" * 40, "tự kiểm lỗi công cụ")
        except LoiDungCa:
            pass
        else:
            bang(False, "chốt ba trạng thái KHÔNG bắt được lỗi git 128 — nó đang đọc lỗi ĐO "
                        "thành câu trả lời 'không phải tổ tiên'")


@ca
def c49_cross_approved_cung_ho_model_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "openai_codex"
    bang(any("cùng họ model" in x for x in bnv2._thieu(d)), "cùng họ model phải bị từ chối")


@ca
def c50_cross_approved_khai_co_audit_thieu_nguoi_audit_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["model_reviewer_identity"]["model_evidence"] = "khai_co_audit"
    bang(any("thiếu người audit" in x for x in bnv2._thieu(d)), "thiếu audit phải bị từ chối")


@ca
def c51_cross_approved_khac_ho_model_co_audit_phai_QUA():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["model_reviewer_identity"]["model_evidence"] = "khai_co_audit"; d["model_reviewer_identity"]["nguoi_audit"] = "ducthangho"
    bang([x for x in bnv2._thieu(d) if "cross_approved" in x or "họ model" in x or "người audit" in x] == [], "cross_approved hợp lệ dính lỗi")


@ca
def c52_cross_approved_thieu_executor_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"
    bang(any("không xác định được họ model của executor" in x for x in bnv2._thieu(d)), "thiếu họ executor phải bị từ chối")


@ca
def c53_cross_approved_antigravity_khong_khai_model_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "google_antigravity"
    bang(any("không xác định được họ model của executor" in x for x in bnv2._thieu(d)), "antigravity thiếu model phải bị từ chối")


@ca
def c54_cross_approved_model_la_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["executor_model"] = "grok-4"
    bang(any("không xác định được họ model của executor" in x for x in bnv2._thieu(d)), "model lạ phải bị từ chối")


@ca
def c55_cross_approved_muc_bang_chung_la_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["model_reviewer_identity"]["model_evidence"] = "xin_the"
    bang(any("ngoài danh sách CHO PHÉP" in x for x in bnv2._thieu(d)), "mức lạ phải bị từ chối")


@ca
def c56_cross_approved_khong_do_duoc_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["model_reviewer_identity"]["model_evidence"] = "khong_do_duoc"
    bang(any("không đủ điều kiện cho cross_approved" in x for x in bnv2._thieu(d)), "khong_do_duoc phải bị từ chối")


@ca
def c57_cross_approved_do_may_thieu_ref_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["model_reviewer_identity"]["model_evidence"] = "do_may"
    bang(any("thiếu tham chiếu đo lường" in x for x in bnv2._thieu(d)), "do_may thiếu ref phải bị từ chối")


@ca
def c58_cross_approved_do_may_co_ref_phai_QUA():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "anthropic_claude"; d["model_reviewer_identity"]["model_evidence"] = "do_may"; d["model_reviewer_identity"]["model_evidence_ref"] = "runs/a1b2/telemetry.json"
    bang([x for x in bnv2._thieu(d) if "cross_approved" in x or "họ model" in x or "đo lường" in x] == [], "do_may có ref dính lỗi")


@ca
def c59_cross_approved_executor_khai_de_thieu_evidence_phai_bi_tu_choi():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "google_antigravity"; d["executor_model"] = "gemini-2.5-pro"
    bang(any("khai đè model executor cho `cross_approved` mà thiếu mức bằng chứng" in x for x in bnv2._thieu(d)), "executor khai đè thiếu evidence phải bị từ chối")


@ca
def c60_cross_approved_executor_do_may_co_ref_phai_QUA():
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "google_antigravity"; d["executor_model"] = "gemini-2.5-pro"; d["executor_model_evidence"] = "do_may"; d["executor_model_evidence_ref"] = "runs/c3d4/telemetry.json"
    bang([x for x in bnv2._thieu(d) if "cross_approved" in x or "họ model" in x or "đo lường" in x or "bằng chứng" in x] == [], "executor do_may có ref dính lỗi")


@ca
def c61_ho_model_cho_phep_phai_quyet_dinh_nhan_dien():
    bang(bnv2._ho_model_cua_ten("gemini-2.5-pro") == "gemini", "gemini phải nhận diện được")
    goc = bnv2.HO_MODEL_CHO_PHEP
    try:
        bnv2.HO_MODEL_CHO_PHEP = frozenset({"claude", "gpt"})
        bang(bnv2._ho_model_cua_ten("gemini-2.5-pro") == "", "gỡ gemini khỏi CHO_PHEP phải trả về rỗng")
    finally:
        bnv2.HO_MODEL_CHO_PHEP = goc



@ca
def c62_khoi_model_executor_identity_phai_doi_xung_voi_khoi_reviewer():
    """`M17` — `P2` của verdict lượt 3. Bên trong khối đã mang tên vai, khoá KHÔNG mang tiền tố.

    Bản trước áp tiền tố `executor_` cho khoá tra CẢ TRONG `sub` lẫn `d`, nên
    `model_reviewer_identity: {model: …}` CHẠY (vai reviewer tiền tố rỗng) còn
    `model_executor_identity: {model: …}` thì KHÔNG — và thông điệp *"không xác định được họ model
    của executor"* đọc như "bạn chưa khai" trong khi người ta ĐÃ khai.

    Đo trên CẢ 184 biên nhận trước khi đổi: dạng CÓ tiền tố bên trong `sub` xuất hiện **0** lần,
    nên bỏ nó không thu hẹp ai trong thực tế."""
    d = v2_du(); d["assurance"] = "cross_approved"
    d["model_executor_identity"] = {"model": "gemini-2.5-pro"}
    bang(bnv2._giai_ho_va_bc(d, "executor")[0] == "gemini",
         "model_executor_identity {model: …} phải nhận diện được họ model")
    e = v2_du(); e["assurance"] = "cross_approved"
    e["model_reviewer_identity"] = dict(e.get("model_reviewer_identity") or {}, model="gpt-5")
    bang(bnv2._giai_ho_va_bc(e, "reviewer")[0] == "gpt",
         "ĐỐI CHỨNG: khối reviewer vẫn phải nhận diện được bằng cùng cách viết")


@ca
def c63_muc_bang_chung_RONG_KHONG_khai_de_phai_QUA():
    """`M21` — đóng `S2`. `A14` của r3 viết *"RỖNG ⇒ CHẶN"*, RỘNG HƠN mã: mã chỉ chặn RỖNG khi CÓ
    khai đè (`ov and not bc`). Đo được **50/50** biên nhận `cross_approved` thật có mức bằng chứng
    RỖNG mà vẫn QUA — nên `A14` và `A3` chưa bao giờ thật sự loại trừ nhau.

    Ca này là ĐỐI CHỨNG BIẾT TRƯỚC ĐÁP ÁN cho `A14`: nó CHẶN nghĩa là `A3` sắp vỡ."""
    d = v2_du(); d["assurance"] = "cross_approved"; d["executor_provider"] = "openai_codex"
    bang([x for x in bnv2._thieu(d) if "bằng chứng" in x] == [],
         "không khai đè + bằng chứng RỖNG phải QUA — nếu CHẶN thì 50 biên nhận cũ sắp đỏ")


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


@ca
def c64_desktop_advisory_va_cli_giu_hop_dong():
    """WP610: hai bề mặt khác nhau, cùng provider; oracle viết tay."""
    for surface in ("codex_cli", "codex_desktop"):
        d = v2_du()
        d["assurance"] = "advisory_review"
        d["model_reviewer_identity"].update(surface=surface, transport="machine")
        bang(bnv2._thieu(d) == [], f"{surface}: receipt đúng bị từ chối: {bnv2._thieu(d)}")


@ca
def c65_desktop_khong_muon_quyen_hoac_bien_thanh_cli():
    """Thêm surface không mở provider/transport/assurance khác."""
    # Oracle đọc AST riêng: Desktop không phải lệnh CLI và chỉ có một hàng đúng.
    cli = _doc_bang_launcher("_TRANSPORT_CONTRACTS")
    ngoai_cli = _doc_bang_launcher("_PROVIDER_NGOAI_CLI")
    bang(not any(r[-2] == "codex_desktop" for r in cli if r),
         "Desktop bị khai thành CLI trong `_TRANSPORT_CONTRACTS`")
    desktop = [r for r in ngoai_cli if r and r[:2] == ["openai_codex", "codex_desktop"]]
    bang(desktop == [["openai_codex", "codex_desktop", "machine"]],
         f"Desktop ngoài CLI phải có ĐÚNG 1 hàng với transport machine: {desktop}")
    # Giữ đủ evidence phiên để đo riêng phân vùng NGƯỜI/MÔ HÌNH.
    d = v2_du(); d["assurance"] = "human_audited"
    d["model_reviewer_identity"].update(surface="codex_desktop", transport="machine", phien_doc_lap=True)
    loi = bnv2._thieu(d)
    bang(any("mức của NGƯỜI audit" in x for x in loi),
         f"Desktop có session phải bị chặn human_audited bởi phân vùng người/mô hình: {loi}")
    for field, value, reason in (("provider", "anthropic_claude", "surface"),
                                  ("transport", "human", "transport"),
                                  ("surface", "codex_desktop_fake", "surface")):
        d = v2_du(); d["assurance"] = "advisory_review"
        d["model_reviewer_identity"].update(surface="codex_desktop", transport="machine")
        d["model_reviewer_identity"][field] = value
        bang(any(reason in x for x in bnv2._thieu(d)), f"{field}={value}: thiếu lỗi đúng tính chất")
    for assurance in ("human_audited", "same_provider_approved", "cross_approved"):
        d = v2_du(); d["assurance"] = assurance
        d["model_reviewer_identity"].update(surface="codex_desktop", transport="machine",
                                            che_do="subagent", phien_doc_lap=False)
        d["model_reviewer_identity"].pop("session_run_id")
        d["model_reviewer_identity"]["KHONG_do_duoc"] = "Không đo được session/model"
        loi = bnv2._thieu(d)
        bang(any(assurance in x for x in loi), f"Desktop không evidence được nâng {assurance}: {loi}")


@ca
def c66_desktop_xoa_hang_doi_hanh_vi_cli_van_qua():
    """Đột biến trên cây gương: bỏ đúng hàng Desktop; CLI là đối chứng cùng lúc."""
    row = '    ("openai_codex", "codex_desktop", "machine"),'
    for removed in (False, True):
        with tempfile.TemporaryDirectory() as t:
            kw = {"sua_launcher": _thay_1(row, "")} if removed else {}
            cong = _cay_guong(Path(t), kho_rieng=False, **kw)
            sp = importlib.util.spec_from_file_location("wp610_mirror", cong)
            mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
            dung(mod.PROVIDER_NGUON_HONG is None, f"rig không đọc được nguồn: {mod.PROVIDER_NGUON_HONG}")
            for surface in ("codex_cli", "codex_desktop"):
                d = v2_du(); d["assurance"] = "advisory_review"
                d["model_reviewer_identity"].update(surface=surface, transport="machine")
                loi = mod._thieu(d)
                if removed and surface == "codex_desktop":
                    bang(len(loi) == 1 and "surface" in loi[0], f"bỏ hàng không chặn đúng surface: {loi}")
                else:
                    bang(loi == [], f"đối chứng {surface} removed={removed}: {loi}")


@ca
def c67_service_khai_that_duoc_nhan_khai_sai_bi_tu_choi_dung_cot():
    """wp461 r3 (Mission #470 Q1): bề mặt thứ ba của Codex là `codex_service` — dịch vụ / GitHub App
    `chatgpt-codex-connector[bot]`. Ba điều phải đúng CÙNG LÚC: (1) khai THẬT được nhận với danh
    sách lỗi RỖNG (`R9-F04`: không phải "không có chữ surface"); (2) mọi tên khác cho cùng bề mặt
    bị từ chối ĐÚNG MỘT lỗi, ĐÚNG cột surface — kể cả tên mà lượt r15 của wp523 đã thử
    (`codex_github_connector`); (3) hợp đồng của `openai_codex` đúng ba bề mặt, không hơn."""
    d = v2_du(); d["assurance"] = "advisory_review"
    d["model_reviewer_identity"].update(surface="codex_service", transport="machine")
    bang(bnv2._thieu(d) == [], f"codex_service khai THẬT bị từ chối: {bnv2._thieu(d)}")
    for sai in ("codex_api", "codex_github_connector", "Codex service", "codex_service_fake"):
        d = v2_du(); d["assurance"] = "advisory_review"
        d["model_reviewer_identity"].update(surface=sai, transport="machine")
        loi = bnv2._thieu(d)
        bang(len(loi) == 1 and "surface" in loi[0] and "openai_codex" in loi[0],
             f"surface={sai!r}: đòi ĐÚNG 1 lỗi ở cột surface, đo được {loi}")
    bang(bnv2.PROVIDER_HOP_DONG["openai_codex"]["be_mat"] == frozenset({"codex_cli", "codex_desktop", "codex_service"}),
         f"hợp đồng openai_codex lệch: {sorted(bnv2.PROVIDER_HOP_DONG['openai_codex']['be_mat'])}")
    # service KHÔNG phải CLI: không được có mặt trong `_TRANSPORT_CONTRACTS` (S5 của spec r3).
    cli = _doc_bang_launcher("_TRANSPORT_CONTRACTS")
    bang(not any(r[-2] == "codex_service" for r in cli if r),
         "codex_service bị khai thành CLI trong `_TRANSPORT_CONTRACTS`")
    ngoai_cli = _doc_bang_launcher("_PROVIDER_NGOAI_CLI")
    service = [r for r in ngoai_cli if r and r[:2] == ["openai_codex", "codex_service"]]
    bang(service == [["openai_codex", "codex_service", "machine"]],
         f"service ngoài CLI phải có ĐÚNG 1 hàng với transport machine: {service}")
    # Tên hợp đồng KHÔNG mua được assurance: không session ⇒ không nâng mức mô hình; phân vùng
    # người/mô hình vẫn chặn `human_audited` — y hệt Desktop (`c65`).
    d = v2_du(); d["assurance"] = "human_audited"
    d["model_reviewer_identity"].update(surface="codex_service", transport="machine", phien_doc_lap=True)
    bang(any("mức của NGƯỜI audit" in x for x in bnv2._thieu(d)),
         "codex_service có session không được chặn human_audited bởi phân vùng người/mô hình")
    for assurance in ("same_provider_approved", "cross_approved"):
        d = v2_du(); d["assurance"] = assurance
        d["model_reviewer_identity"].update(surface="codex_service", transport="machine")
        d["model_reviewer_identity"].pop("session_run_id")
        d["model_reviewer_identity"]["KHONG_do_duoc"] = "GitHub App không xuất session/model"
        loi = bnv2._thieu(d)
        bang(any(assurance in x for x in loi), f"codex_service không evidence được nâng {assurance}: {loi}")


@ca
def c68_service_xoa_hang_doi_hanh_vi_cli_desktop_van_qua():
    """Đột biến trên cây gương: bỏ ĐÚNG hàng `codex_service`; CLI và Desktop là đối chứng cùng lúc.
    Đây là phép đo A6 của spec r3: rút hàng phải làm ca dương ĐỎ với thông báo nêu đúng cột."""
    row = '    ("openai_codex", "codex_service", "machine"),'
    for removed in (False, True):
        with tempfile.TemporaryDirectory() as t:
            kw = {"sua_launcher": _thay_1(row, "")} if removed else {}
            cong = _cay_guong(Path(t), kho_rieng=False, **kw)
            sp = importlib.util.spec_from_file_location("wp461_mirror", cong)
            mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
            dung(mod.PROVIDER_NGUON_HONG is None, f"rig không đọc được nguồn: {mod.PROVIDER_NGUON_HONG}")
            for surface in ("codex_cli", "codex_desktop", "codex_service"):
                d = v2_du(); d["assurance"] = "advisory_review"
                d["model_reviewer_identity"].update(surface=surface, transport="machine")
                loi = mod._thieu(d)
                if removed and surface == "codex_service":
                    bang(len(loi) == 1 and "surface" in loi[0] and "codex_service" in loi[0],
                         f"bỏ hàng không chặn đúng surface: {loi}")
                else:
                    bang(loi == [], f"đối chứng {surface} removed={removed}: {loi}")


# ------------------------------------------------------------------ câu lịch sử (#960)
# Đặc tả `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md` A1–A6. Mỗi ca dựng kho git THẬT có lịch sử rồi đổi
# đúng MỘT yếu tố; mỗi chốt có đột biến riêng trong `_dot_bien`. Biên nhận fixture đi qua `allowlist`
# tiêm vào (băm đúng) nên chỉ ba luật mới lên tiếng — lược đồ v2 có ca riêng ở trên.
# CHÉP TAY từ `--sinh-no-cau-lich-su` trên base `4488444` của lease r2 (27-10-2026, 61 mục: r1 sinh 66 trên `e3ea139`, PR #976 gỡ 2 L-SURFACE trích dẫn, r2 M4 làm chết 3 L-SURFACE còn lại). KHÔNG import từ cổng:
# một oracle sinh từ chính thứ nó kiểm thì co theo mỗi lần cổng bị nới.
NO_CAU_DONG_BANG = frozenset({
    ("ci-g5-cong-cu-chia-manh-r1-review-1-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-1-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-10-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-10-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-12-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-12-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-14-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-14-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-15-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-15-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-16-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-16-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-17-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-17-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-18-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-18-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-20-claude-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-20-claude-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-21-claude-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-21-claude-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-5-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-5-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-7-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-7-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", "L-ANCESTRY"),
    ("ci-windows-review-5-claude-verdict.receipt.yaml", "chuoi_verdict_ghi_chu", "L-ANCESTRY"),
    ("doctrine-scan-review-1-claude-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("doctrine-scan-review-2-claude-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("doctrine-scan-review-3-claude-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("lease-publish-windows-do-review-r1-codex.receipt.yaml", "reviewed_sha_to_tien", "L-ANCESTRY"),
    ("pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml", "verdict_usage_caveats[1].noi_dung", "L-REVIEW"),
    ("pr490-review-7-codex-verdict.receipt.yaml", "verdict_usage_caveats[1].phep_do_BA_LOI_LAND.cong_tren_ban_squash", "L-ANCESTRY"),
    ("pr508-review-1-codex-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("pr508-review-2-codex-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("pr508-review-3-codex-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("pr508-review-4-codex-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("pr508-review-5-codex-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("pr526-review-3-codex-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("pr896-review-3-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("pr896-review-4-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("pr896-review-5-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("pr896-review-6-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("pr896-review-7-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("pr896-review-8-codex-verdict.receipt.yaml", "anchor.mo_ta", "L-ANCESTRY"),
    ("r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml", "land.head_da_doi_TRUOC_merge.vi_sao", "L-ANCESTRY"),
    ("wp461-review-1-codex-verdict.receipt.yaml", "anchor.cuong_do", "L-ANCESTRY"),
    ("wp461-review-1-codex-verdict.receipt.yaml", "lich_su_ban_ung_vien.ghi_chu", "L-ANCESTRY"),
    ("wp523-r15-review-1-codex-verdict.receipt.yaml", "anchor.cuong_do", "L-ANCESTRY"),
    ("wp523-r15-review-1-codex-verdict.receipt.yaml", "lich_su_ban_ung_vien.ghi_chu", "L-ANCESTRY"),
    ("wp538-review-1-claude-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("wp538-review-2-claude-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("wp540-review-1-claude-verdict.receipt.yaml", "anchor.gioi_han", "L-ANCESTRY"),
    ("wp541-review-1-claude-verdict.receipt.yaml", "ci_tu_dong_tren_ung_vien.thu_hoi", "L-ANCESTRY"),
})


def _kho_cau(tmp: Path):
    """Kho git có lịch sử: master `B0 → M`; nhánh rẽ `re` từ `B0` có `X` (KHÔNG vào master).

    Ngày commit GHIM ⇒ SHA tất định. Bản trước để ngày trôi, nên tiền tố 7 ký tự của `M` có lúc toàn chữ
    số và `c74` đỏ trên CI (run 40479809106) mà xanh tại chỗ — một ca chập chờn theo SHA ngẫu nhiên."""
    E = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
         "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", ""),
         "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
         "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"}

    def g(*a):
        r = subprocess.run(["git", "-C", str(tmp), *a], capture_output=True, text=True, env=E)
        dung(r.returncode == 0, f"git {' '.join(a)} hỏng: {r.stderr[:200]}")
        return r.stdout.strip()
    g("init", "-q"); g("checkout", "-q", "-b", "master")
    # #1017: BYTE LF, không `write_text` — chế độ văn bản của Python đổi `\n` thành `\r\n` trên Windows nên
    # blob khác byte, SHA mọi commit đổi theo, và các fixture ghim SHA (`_COMMIT_BLOB_TRUNG`, `_THONG_DIEP_TRUNG`)
    # gãy ở đó mà xanh trên Linux (run 40833816523: c93 ra đúng SHA của bản CRLF, đã tái hiện trên Linux).
    (tmp / "a.txt").write_bytes(b"a\n"); g("add", "-A"); g("commit", "-qm", "B0")
    b0 = g("rev-parse", "HEAD")
    g("checkout", "-q", "-b", "re")
    (tmp / "x.txt").write_bytes(b"x\n"); g("add", "-A"); g("commit", "-qm", "X")
    x = g("rev-parse", "HEAD")
    g("checkout", "-q", "master")
    (tmp / "m.txt").write_bytes(b"m\n"); g("add", "-A"); g("commit", "-qm", "M")
    return {"B0": b0, "X": x, "M": g("rev-parse", "HEAD"), "g": g}


def _ghi_bn_cau(tmp: Path, k: dict, tep: dict):
    """Ghi + COMMIT các biên nhận (văn bản YAML thô, để giữ nguyên `>-`/`|`). Trả allowlist {tên: băm}."""
    import hashlib as _h
    tm = tmp / bnv2.THU_MUC
    tm.mkdir(parents=True, exist_ok=True)
    for ten, van in tep.items():
        (tm / ten).write_bytes(van.encode("utf-8"))
    k["g"]("add", "-A"); k["g"]("commit", "-qm", "bien nhan")
    return {ten: _h.sha256((tm / ten).read_bytes()).hexdigest() for ten in tep}


def _kiem_cau(tmp: Path, al: dict, no=frozenset()):
    """(rc theo đúng hàm CLI dùng, loi của ba luật, tk)."""
    loi, tk = bnv2.kiem(tmp, allowlist=al, no_da_do={}, no_cau_lich_su=no)
    return bnv2._ma_thoat(loi, tk), [x for x in loi if x.startswith("[L-")], tk


def _bn_cau(luot, than, sha=None):
    return (f"schema_version: 1\nluot: {luot}\n" + (f"reviewed_sha: {sha}\n" if sha else "") + than)


@ca
def c69_A1_cau_chua_review_ma_luot_sau_DA_review_dung_SHA():
    """A1 (M1): câu "chưa review lại" + biên nhận sau cùng `reviewed_sha`, `luot` lớn hơn ⇒ rc=1;
    biên nhận sau lệch MỘT ký tự (cuối, ngoài 7 ký tự đầu) ⇒ rc=0. (Mốc `dung_tai`: r2 bỏ — xem `c86`.)"""
    lech = None
    for ten, sau, moc, rc_doi in (("co-luot-sau", "dung", "", 1), ("lech-mot-ky-tu", "lech", "", 0)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            h = k["M"]
            lech = h[:-1] + ("0" if h[-1] != "0" else "1")
            dong_moc = f"    dung_tai: {k[moc]}\n" if moc else ""
            al = _ghi_bn_cau(tmp, k, {
                "r1.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Ban va tai {h} chua duoc review lai.\n{dong_moc}"),
                "r2.receipt.yaml": _bn_cau(2, "", h if sau == "dung" else lech)})
            rc, loi, _ = _kiem_cau(tmp, al)
            bang(rc == rc_doi, f"{ten}: đòi rc={rc_doi}, được {rc}: {loi}")
            if rc_doi:
                bang(len(loi) == 1 and loi[0].startswith("[L-REVIEW] r1.receipt.yaml: `anchor.mo_ta`"),
                     f"{ten}: đỏ SAI chỗ/luật: {loi}")


@ca
def c70_A1_luot_KHONG_so_duoc_la_KHONG_DO_DUOC():
    """`luot` không phải số — của CHÍNH biên nhận chứa câu, hoặc của biên nhận KHÁC cùng `reviewed_sha` —
    ⇒ không so được "lớn hơn" ⇒ trạng thái thứ ba, không phải sạch và không phải crash."""
    for ten, r1, r2 in (("luot-cau-thieu", "schema_version: 1\n", "luot: 2\n"),
                        ("luot-bien-nhan-khac-thieu", "schema_version: 1\nluot: 1\n", "")):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            h = k["M"]
            al = _ghi_bn_cau(tmp, k, {
                "r1.receipt.yaml": f"{r1}anchor:\n    mo_ta: Ban va tai {h} chua duoc review lai.\n",
                "r2.receipt.yaml": f"schema_version: 1\n{r2}reviewed_sha: {h}\n"})
            try:
                rc, loi, tk = _kiem_cau(tmp, al)
            except Exception as ex:                                   # noqa: BLE001
                bang(False, f"{ten}: `kiem` chết bằng {type(ex).__name__}: {ex}")
            bang(rc == 2 and not loi and any(x.startswith("[L-REVIEW]") for x in tk["chua_do"]),
                 f"{ten}: đòi rc=2 + một mục L-REVIEW KHÔNG ĐO ĐƯỢC, được rc={rc} loi={loi} chua={tk['chua_do']}")


@ca
def c71_A2_cau_ancestry_do_bang_merge_base():
    """A2 (M2): OID đã là tổ tiên ⇒ rc=1 · chưa ⇒ rc=0 · không tồn tại (trộn số-chữ) ⇒ rc=2.
    (Mốc `dung_tai`: r2 bỏ — xem `c86`; OID theo ngữ cảnh: `c87`.)"""
    for ten, oid, moc, rc_doi in (("da-to-tien", "M", "", 1), ("chua-to-tien", "X", "", 0),
                                   ("khong-ton-tai", None, "", 2)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            o = k[oid][:7] if oid else "1234abc"
            if oid is None:
                dung(bnv2._commit_cua(tmp, o) is None, f"fixture: `{o}` lại tra được commit")
            dong_moc = ""
            al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(
                1, f"anchor:\n    mo_ta: Commit {o} chua vao master.\n{dong_moc}")})
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == rc_doi, f"{ten}: đòi rc={rc_doi}, được {rc}: loi={loi} chua={tk['chua_do']}")
            if rc_doi == 1:
                bang(len(loi) == 1 and loi[0].startswith("[L-ANCESTRY] r.receipt.yaml: `anchor.mo_ta`"),
                     f"{ten}: đỏ SAI chỗ/luật: {loi}")
            if rc_doi == 2:
                bang(any(x.startswith("[L-ANCESTRY]") for x in tk["chua_do"]),
                     f"{ten}: rc=2 mà không phải vì L-ANCESTRY: {tk['chua_do']}")


@ca
def c72_A3_bien_the_co_dau_khong_dau_xuong_dong_deu_bi_nhan():
    """A3 (M2): có dấu / không dấu / gãy dòng trong `|` và `>-` đều bị nhận; câu chỉ NHẮC cụm từ
    trong ngoặc trích, không có OID ⇒ không phải vi phạm.

    Giới hạn (r2 B6): khối `>-` được bộ phân tích YAML gấp TRƯỚC khi cổng thấy, nên cổng KHÔNG có chốt riêng
    cho nó — trường `khoi_gap` ở đây chỉ là ca HỒI QUY; chốt "gộp dòng" có răng với khối `|` (`m78`)."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        m = k["M"][:7]
        than = (f"co_dau: Commit {m} chưa vào master.\n"
                f"khong_dau: Commit {m} chua vao master.\n"
                f"khoi_lit: |\n    Commit {m} khong phai to\n    tien cua master.\n"
                f"khoi_gap: >-\n    Commit {m} chi la mot\n    nhanh.\n"
                "chi_trich: 'Finding cu noi \"chi la mot nhanh\" va \"khong phai to tien\".'\n")
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, than)})
        rc, loi, _ = _kiem_cau(tmp, al)
        truong = {x.split("`")[1] for x in loi}
        # MỖI trường một assertion riêng, để một đột biến giết ca chỉ ra ĐÚNG biến thể nó làm mù. `>-`
        # được bộ phân tích YAML gấp TRƯỚC khi cổng thấy, nên cổng không có chốt riêng cho nó; trường
        # ấy ở đây là hồi quy, còn chốt "gộp dòng" của cổng chỉ có răng với khối `|` (`m78`).
        for tr, vi_sao in (("khoi_lit", "khối `|` gãy dòng"), ("khoi_gap", "khối `>-` gãy dòng"),
                           ("co_dau", "có dấu"), ("khong_dau", "không dấu")):
            bang(tr in truong, f"biến thể {vi_sao} (`{tr}`) không bị nhận: {sorted(truong)}")
        bang("chi_trich" not in truong, f"câu chỉ trích cụm từ, không OID, bị nhận nhầm: {loi}")


def _kho_surface(tmp: Path, d: dict, run_json, verdict: str):
    """Kho git THẬT cho L-SURFACE (đặc tả: mọi ca có lịch sử thật — codex CLI lượt 1, P2): commit
    biên nhận + `run.json` (None = không tạo) + verdict, rồi đòi HEAD chứa đúng các tệp ấy."""
    import yaml as _y
    k = _kho_cau(tmp)
    (tmp / "ops/reviews/v").mkdir(parents=True, exist_ok=True)
    if run_json is not None:
        (tmp / "ops/reviews/v/run.json").write_text(run_json, encoding="utf-8")
    (tmp / "ops/reviews/v.md").write_text(verdict, encoding="utf-8")
    al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _y.safe_dump(d, allow_unicode=True)})
    co = k["g"]("ls-tree", "-r", "--name-only", "HEAD", "--", "ops/reviews").split()
    dung("ops/reviews/v.md" in co and "ops/reviews/r.receipt.yaml" in co
         and (run_json is None) == ("ops/reviews/v/run.json" not in co), f"fixture: HEAD thiếu tệp: {co}")
    return al


def _bn_surface(rj, dong_verdict, caveat=False):
    d = {"schema_version": 1, "verdict_path": "ops/reviews/v.md",
         "model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_cli", "run_json": rj}}
    if caveat:
        d["verdict_usage_caveats"] = [{"id": "VERDICT-KHAI-SAI-EXECUTION-SURFACE", "mo_ta": "x"}]
    return d, dong_verdict


@ca
def c73_A4_surface_verdict_doi_chieu_run_json():
    """A4 (M3): run.json `codex_cli` + verdict khai `codex_service` + thiếu caveat ⇒ rc=1; có caveat
    ⇒ rc=0; verdict khai đúng ⇒ rc=0; `run_json` trỏ tệp không có ⇒ không áp, đếm vào `chua_do_duoc`."""
    import json as _j
    for ten, rj, dong, cv, rc_doi, sf in (
            ("khai-sai-thieu-caveat", "ops/reviews/v/run.json", "execution_surface: codex_service", False, 1, 0),
            ("khai-sai-co-caveat", "ops/reviews/v/run.json", "execution_surface: codex_service", True, 0, 0),
            ("khai-dung", "ops/reviews/v/run.json", "execution surface `codex_cli`", False, 0, 0),
            ("run-json-khong-co", "ops/reviews/khong-co/run.json", "execution_surface: codex_service", False, 0, 1)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            d, _ = _bn_surface(rj, dong, cv)
            al = _kho_surface(tmp, d, _j.dumps({"execution_surface": "codex_cli"}),
                              f"verdict: approve\nprovider: openai_codex\n{dong}\n")
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == rc_doi, f"{ten}: đòi rc={rc_doi}, được {rc}: {loi} {tk['chua_do']}")
            bang(len(tk["surface_chua_do"]) == sf,
                 f"{ten}: đòi {sf} mục L-SURFACE chua_do_duoc, được {tk['surface_chua_do']}")
            if rc_doi:
                bang(len(loi) == 1 and loi[0].startswith("[L-SURFACE] r.receipt.yaml"), f"{ten}: {loi}")


@ca
def c74_A5_no_cau_lich_su_chi_co_va_no_chet_la_vi_pham():
    """A5 (M4): vi phạm nằm trong danh sách nợ ⇒ rc=0; xoá mục nợ ⇒ rc=1; vá câu mà GIỮ mục nợ ⇒ rc=1."""
    khoa = ("r.receipt.yaml", "anchor.mo_ta", bnv2.LUAT_ANCESTRY)
    for ten, va, no, rc_doi in (("trong-no", False, {khoa}, 0), ("xoa-no", False, set(), 1),
                                 ("no-chet", True, {khoa}, 1)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            cau = "Commit da vao master." if va else f"Commit {k['M'][:7]} chua vao master."
            al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: {cau}\n")})
            rc, loi, tk = _kiem_cau(tmp, al, frozenset(no))
            bang(rc == rc_doi, f"{ten}: đòi rc={rc_doi}, được {rc}: {loi}")
            if ten == "trong-no":
                bang(tk["no_cau"][bnv2.LUAT_ANCESTRY] == 1, f"{ten}: nợ không được đếm: {tk['no_cau']}")
            if ten == "no-chet":
                bang(len(loi) == 1 and "NỢ CHẾT" in loi[0], f"{ten}: đòi đúng một dòng NỢ CHẾT: {loi}")


@ca
def c75_no_cau_lich_su_CHI_CO_LAI_va_tro_tep_co_that():
    """Bánh cóc M4: `NO_CAU_LICH_SU` ⊆ bản đóng băng ở tệp NÀY; mọi mục trỏ biên nhận CÓ trong kho."""
    thua = sorted(set(bnv2.NO_CAU_LICH_SU) - NO_CAU_DONG_BANG)
    bang(not thua, f"`NO_CAU_LICH_SU` ĐÃ NỞ {len(thua)} mục: {thua[:3]} — câu mới phải đúng hoặc có mốc")
    mat = sorted({t for t, _, _ in bnv2.NO_CAU_LICH_SU if not (GOC / bnv2.THU_MUC / t).is_file()})
    bang(not mat, f"mục nợ trỏ tệp không còn trong kho (nợ chết không ai canh): {mat[:3]}")


@ca
def c76_A6_kho_that_voi_no_RONG_phai_DO_dung_bang_so_no():
    """A6: trên kho thật, danh sách nợ RỖNG ⇒ rc=1 với đúng `len(NO_CAU_LICH_SU)` dòng của ba luật —
    bằng chứng luật có răng trên dữ liệu thật, và nợ khớp đúng vi phạm (không thừa, không thiếu)."""
    dung((GOC / bnv2.THU_MUC).is_dir() and (GOC / ".git").exists(), "KHÔNG ĐO ĐƯỢC: không phải kho thật")
    loi, tk = bnv2.kiem(GOC, no_cau_lich_su=frozenset())
    cau = [x for x in loi if x.startswith("[L-")]
    bang(bnv2._ma_thoat(loi, tk) == 1 and not tk["chua_do"],
         f"đòi rc=1 không KHÔNG ĐO ĐƯỢC, được rc={bnv2._ma_thoat(loi, tk)} chua={tk['chua_do'][:3]}")
    bang(len(cau) == len(bnv2.NO_CAU_LICH_SU) == len(loi),
         f"đòi {len(bnv2.NO_CAU_LICH_SU)} dòng ba luật và không dòng nào khác, được {len(cau)}/{len(loi)}")
    # L-SURFACE KHÔNG có trong vòng này từ r2: theo định nghĩa lời tự khai (M4) mọi khai sai trên kho thật
    # đều đã mang caveat (đo 27-10: 6/6), nên nợ rỗng KHÔNG sinh dòng L-SURFACE. Răng của nó ở `c73`/`c88`.
    for lu in (bnv2.LUAT_REVIEW, bnv2.LUAT_ANCESTRY):
        bang(any(x.startswith(f"[{lu}]") for x in cau), f"luật {lu} không bắt được gì trên kho thật")


@ca
def c77_run_json_CO_ma_HONG_la_KHONG_DO_DUOC_khong_phai_no_chet():
    """Connector PR #976 (P2) + codex CLI lượt 1 (P1): `run.json` CÓ mà hỏng (JSON lỗi / không phải
    ánh xạ / thiếu trường) hoặc verdict không giải mã được ⇒ rc=2, kể cả khi mục ấy đang là NỢ — không
    được thành `NỢ CHẾT`. Miễn trừ "không áp" của A4 chỉ dành cho tệp VẮNG (`c73` giữ ca ấy)."""
    khoa = ("r.receipt.yaml", "verdict_path", bnv2.LUAT_SURFACE)
    for ten_hong, rj_text, verdict in (("json-loi", "{khong phai json", "execution_surface: codex_service\n"),
                                       ("khong-phai-anh-xa", "[]", "execution_surface: codex_service\n"),
                                       ("thieu-truong", "{}", "execution_surface: codex_service\n"),
                                       ("verdict-byte-hong", '{"execution_surface": "codex_cli"}', None)):
        for ten_no, no in (("khong-no", frozenset()), ("dang-la-no", frozenset({khoa}))):
            ten = f"{ten_hong}/{ten_no}"
            with tempfile.TemporaryDirectory() as t:
                tmp = Path(t)
                d, _ = _bn_surface("ops/reviews/v/run.json", "")
                al = _kho_surface(tmp, d, rj_text, verdict or "x\n")
                if verdict is None:
                    (tmp / "ops/reviews/v.md").write_bytes(b"execution_surface: \xff\n")
                rc, loi, tk = _kiem_cau(tmp, al, no)
                bang(rc == 2 and not loi and any(x.startswith("[L-SURFACE]") for x in tk["chua_do"]),
                     f"{ten}: đòi rc=2 + KHÔNG ĐO ĐƯỢC L-SURFACE, không dòng ĐỎ; được rc={rc} loi={loi} "
                     f"chua={tk['chua_do']}")


def _commit_tien_to_so(tmp: Path, k: dict, dk=str.isdigit, nhan="so", tran=2000):
    """Commit rẽ từ B0 có 7 ký tự đầu thoả `dk` (toàn chữ số / toàn chữ cái) — tìm bằng `commit-tree` với
    ngày GHIM, nên tất định."""
    E = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
         "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", ""),
         "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
         "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"}
    cay = k["g"]("rev-parse", f"{k['B0']}^{{tree}}")
    for i in range(tran):
        r = subprocess.run(["git", "-C", str(tmp), "commit-tree", cay, "-p", k["B0"], "-m", f"{nhan}{i}"],
                           capture_output=True, text=True, env=E)
        dung(r.returncode == 0, f"commit-tree hỏng: {r.stderr[:200]}")
        sha = r.stdout.strip()
        if dk(sha[:7]):
            return sha
    dung(False, f"không tìm được commit tiền tố `{nhan}` trong {tran} lượt")


@ca
def c78_OID_viet_tat_TOAN_CHU_SO_van_duoc_tra():
    """Connector PR #976 (P2) + codex CLI lượt 1 (P1): OID viết tắt toàn chữ số / toàn chữ cái là OID thật
    — phải tra; số run Actions hay từ hex thường không tra ra commit thì KHÔNG phải ứng viên (không vi phạm,
    không KHÔNG ĐO ĐƯỢC)."""
    for nhan, dk, tran in (("so", str.isdigit, 2000), ("chu", str.isalpha, 30000)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            sha = _commit_tien_to_so(tmp, k, dk, nhan, tran)
            k["g"]("merge", "-q", "--no-ff", sha, "-m", "merge")
            dung(bnv2._commit_cua(tmp, sha[:7]) == sha, f"{nhan}: fixture tiền tố không tra ra đúng commit")
            al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(
                1, f"anchor:\n    mo_ta: Commit {sha[:7]} chua vao master.\n"
                   "run:\n    ghi_chu: Run 40268583940 va deadbeef khong phai to tien cua master.\n")})
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == 1 and len(loi) == 1 and loi[0].startswith("[L-ANCESTRY] r.receipt.yaml: `anchor.mo_ta`"),
                 f"{nhan}: đòi đúng một vi phạm ở `anchor.mo_ta`, số run/từ hex không tính; được rc={rc} "
                 f"loi={loi} chua={tk['chua_do']}")


@ca
def c79_dong_TRICH_DAN_hien_vat_khac_khong_phai_tu_khai_surface():
    """Connector PR #976 (P2): verdict tự khai ĐÚNG `codex_cli` và TRÍCH dòng `tệp.md:6:` của hiện vật
    khác có `codex_service` ⇒ không vi phạm (pr896-review-8 dòng 215 là ca thật). r2 (M4): có trích dẫn
    `tệp:N` trong cửa sổ ba dòng thì dòng ấy KHÔNG là lời tự khai — kể cả khi trích dẫn đứng sau khai báo
    (revision 1 còn đòi rc=1 cho ca ấy; quy tắc mới bỏ cả dòng, chấp nhận đổi lấy 0 bắt nhầm trên kho thật)."""
    import json as _j
    for ten, verdict, rc_doi in (
            ("trich-dan-truoc", "provider: openai_codex\nexecution_surface: codex_cli\n\n"
             "ops/land/khac/luot5-verdict.md:6: Reviewer; provider `openai_codex`, execution surface `codex_service`\n", 0),
            ("trich-dan-sau", "provider `openai_codex`; execution_surface: codex_service (so ops/land/khac/luot5-verdict.md:6)\n", 0)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            d, _ = _bn_surface("ops/reviews/v/run.json", "")
            al = _kho_surface(tmp, d, _j.dumps({"execution_surface": "codex_cli"}), verdict)
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == rc_doi, f"{ten}: đòi rc={rc_doi}, được {rc}: loi={loi}")


@ca
def c82_alias_VONG_la_KHONG_DO_DUOC_alias_dung_lai_van_duyet():
    """codex CLI lượt 1 (P1): alias vòng (`&a [*a]`, `safe_load` nhận) ⇒ `KhongDoDuoc`, không traceback;
    alias DÙNG LẠI không vòng vẫn được duyệt theo từng đường (câu vi phạm ở cả hai chỗ đều bị bắt)."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, "cycle: &self [*self]\n")})
        try:
            bnv2.kiem(tmp, allowlist=al, no_da_do={}, no_cau_lich_su=frozenset())
            bang(False, "alias vòng mà `kiem` không ném KhongDoDuoc")
        except bnv2.KhongDoDuoc as ex:
            bang("alias" in str(ex), f"KHÔNG ĐO ĐƯỢC sai lý do: {ex}")
        except Exception as ex:                                   # noqa: BLE001
            bang(False, f"alias vòng làm `kiem` chết bằng {type(ex).__name__}, không phải KhongDoDuoc")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(
            1, f"a: &c\n    mo_ta: Commit {k['M'][:7]} chua vao master.\nb: *c\n")})
        rc, loi, _ = _kiem_cau(tmp, al)
        truong = sorted(x.split("`")[1] for x in loi)
        bang(truong == ["a.mo_ta", "b.mo_ta"], f"alias dùng lại phải được duyệt theo cả hai đường: {truong}")


@ca
def c83_MOI_khai_bao_surface_tren_cung_dong_deu_duoc_xet():
    """codex CLI lượt 1 (P1): `execution_surface: codex_cli; execution_surface: codex_service` — theo cả
    hai thứ tự — vẫn là verdict khai sai ⇒ rc=1."""
    import json as _j
    for ten, dong in (("dung-truoc", "execution_surface: codex_cli; execution_surface: codex_service"),
                      ("sai-truoc", "execution_surface: codex_service; execution_surface: codex_cli")):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            d, _ = _bn_surface("ops/reviews/v/run.json", "")
            al = _kho_surface(tmp, d, _j.dumps({"execution_surface": "codex_cli"}), "provider: openai_codex\n" + dong + "\n")
            rc, loi, _ = _kiem_cau(tmp, al)
            bang(rc == 1, f"{ten}: khai báo sai trên cùng dòng bị che: rc={rc} loi={loi}")


@ca
def c84_merge_base_HONG_la_KHONG_DO_DUOC_khong_phai_vi_pham():
    """codex CLI lượt 1 (P1, r3): `merge-base` trả mã ngoài 0/1 (đây: nhánh mặc định là một TREE) ⇒ rc=2,
    không phải vi phạm."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})
        cay = k["g"]("rev-parse", "HEAD^{tree}")
        loi, tk = bnv2.kiem(tmp, allowlist=al, no_da_do={}, no_cau_lich_su=frozenset(), nhanh_mac_dinh=cay)
        loi = [x for x in loi if x.startswith("[L-")]
        bang(bnv2._ma_thoat(loi, tk) == 2 and not loi and any("merge-base" in x for x in tk["chua_do"]),
             f"merge-base hỏng phải là KHÔNG ĐO ĐƯỢC: loi={loi} chua={tk['chua_do']}")


@ca
def c86_B1_moc_dung_tai_KHONG_con_mien():
    """r2 B1 (M1): mốc `dung_tai: <B0>` HỢP LỆ theo luật r1 mà nay vẫn vi phạm — cả L-REVIEW lẫn L-ANCESTRY."""
    for ten, than, lu in (
            ("review", "anchor:\n    mo_ta: Ban va tai {M} chua duoc review lai.\n    dung_tai: {B0}\n", "L-REVIEW"),
            ("ancestry", "anchor:\n    mo_ta: Commit {M7} chua vao master.\n    dung_tai: {B0}\n", "L-ANCESTRY")):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            tep = {"r1.receipt.yaml": _bn_cau(1, than.format(M=k["M"], M7=k["M"][:7], B0=k["B0"]))}
            if lu == "L-REVIEW":
                tep["r2.receipt.yaml"] = _bn_cau(2, "", k["M"])
            al = _ghi_bn_cau(tmp, k, tep)
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == 1 and len(loi) == 1 and loi[0].startswith(f"[{lu}] r1.receipt.yaml: `anchor.mo_ta`"),
                 f"{ten}: mốc còn miễn được câu cũ: rc={rc} loi={loi} chua={tk['chua_do']}")


@ca
def c87_B3_OID_khong_tra_duoc_theo_NGU_CANH():
    """r2 B3 (M3): OID không tra được ⇒ rc=2 khi có ngữ cảnh (40 hex · backtick · sau `commit`); token
    thuần số / thuần chữ không ngữ cảnh ⇒ bỏ qua (rc=0). Trộn số-chữ đo RIÊNG không từ commit/backtick;
    OID thật ở `c78`.
    Ranh giới của từng ngữ cảnh (r2 review 1, `bo-chon-moi-chua-khoa-bien`): `Precommit` không phải từ
    `commit`; backtick chỉ MỞ không phải trong backtick ⇒ rc=0."""
    for ten, cau, rc_doi in (("40-hex", "Ban " + "a" * 40 + " chua vao master.", 2),
                             ("backtick", "Ban `abcdefa` chua vao master.", 2),
                             ("sau-commit", "Commit 1234567 chua vao master.", 2),
                             ("tron-so-chu-rieng", "Ban 12ab34c chua vao master.", 2),
                             ("tu-thuong", "Tu deadbeef chua vao master.", 0),
                             ("so-run", "Run 40268583940 chua vao master.", 0),
                             ("tien-to-commit", "Precommit 1234567 chua vao master.", 0),
                             ("backtick-chi-mo", "Ban `abcdefa chua vao master.", 0)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            tok = next(x for x in cau.replace("`", " ").split() if all(c in "0123456789abcdef" for c in x) and len(x) >= 7)
            dung(bnv2._commit_cua(tmp, tok) is None, f"{ten}: fixture `{tok}` lại tra được commit")
            al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: '{cau}'\n")})
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == rc_doi and not loi, f"{ten}: đòi rc={rc_doi}, được {rc}: loi={loi} chua={tk['chua_do']}")
            if rc_doi == 2:
                bang(any(x.startswith("[L-ANCESTRY]") for x in tk["chua_do"]), f"{ten}: rc=2 sai lý do: {tk['chua_do']}")


@ca
def c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan():
    """r2 B4 (M4): (i) `provider` ở dòng kề + khai `codex_service`, thiếu caveat ⇒ rc=1; (ii) cùng thế mà
    dòng trước là trích dẫn `tệp:N` ⇒ rc=0; (iii) khai báo không có `provider` trong cửa sổ ⇒ rc=0.
    Ranh giới cửa sổ (r2 review 1, `bo-chon-moi-chua-khoa-bien`): (iv) `notprovider` không phải từ `provider`
    ⇒ rc=0; (v) `provider` ở dòng SAU cũng thuộc cửa sổ ⇒ rc=1. Hai dòng cách xa là NGOÀI cửa sổ:
    provider ngoài cửa sổ không tạo tự khai; trích dẫn ngoài cửa sổ không miễn tự khai.
    #1021 (Codex lượt 5, P1 `bien-ngoai-cua-so-surface-chua-co-rang`, áp `HINT.patch` của reviewer): bỏ tiền tố cố định
    để các hàng thật sự chạm biên đầu tệp `j = 0` (m156 bỏ chặn chỉ số âm), thêm (ii-b) trích dẫn ở dòng NGAY SAU vẫn
    miễn tự khai (m157 bỏ dòng sau khỏi phép tìm trích dẫn)."""
    import json as _j
    for ten, verdict, rc_doi in (
            ("i-tu-khai", "provider: openai_codex\nexecution_surface: codex_service\n", 1),
            ("ii-trich-dan-ke", "ops/x/v.md:6\nSELF: provider `openai_codex`, execution surface `codex_service`\n", 0),
            ("ii-b-trich-dan-dong-sau", "provider: openai_codex execution_surface: codex_service\nops/x/v.md:6\n", 0),
            ("iii-khong-provider", "Bang do: thay dong verdict thanh `execution_surface: codex_service`.\n", 0),
            ("iv-notprovider", "notprovider: openai_codex\nexecution_surface: codex_service\n", 0),
            ("v-provider-dong-sau", "execution_surface: codex_service\nprovider: openai_codex\n", 1),
            ("vi-provider-truoc-hai-dong", "provider: openai_codex\n\nexecution_surface: codex_service\n", 0),
            ("vii-provider-sau-hai-dong", "execution_surface: codex_service\n\nprovider: openai_codex\n", 0),
            ("viii-trich-dan-truoc-hai-dong", "ops/x/v.md:6\n\nprovider: openai_codex execution_surface: codex_service\n", 1),
            ("ix-trich-dan-sau-hai-dong", "provider: openai_codex execution_surface: codex_service\n\nops/x/v.md:6\n", 1)):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            d, _ = _bn_surface("ops/reviews/v/run.json", "")
            al = _kho_surface(tmp, d, _j.dumps({"execution_surface": "codex_cli"}), verdict)
            rc, loi, tk = _kiem_cau(tmp, al)
            bang(rc == rc_doi, f"{ten}: đòi rc={rc_doi}, được {rc}: loi={loi} chua={tk['chua_do']}")


@ca
def c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback():
    """r2 B2 (M2, finding `receipt-khong-doc-duoc-thoat-1`): một `*.receipt.yaml` là THƯ MỤC (băm/đọc ném
    `IsADirectoryError`, kể cả dưới root) ⇒ CLI rc=2, không traceback."""
    import contextlib
    import io
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, "x: 1\n")})
        (tmp / bnv2.THU_MUC / "thu-muc.receipt.yaml").mkdir()
        ra, loi_ra = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi_ra):
                rc = bnv2.main(["--root", str(tmp)])
        except Exception as ex:                                   # noqa: BLE001
            bang(False, f"CLI chết bằng {type(ex).__name__}: {ex} — đòi rc=2")
        bang(rc == 2 and "thu-muc.receipt.yaml" in loi_ra.getvalue(),
             f"đòi rc=2 nêu tệp hỏng, được rc={rc}: {loi_ra.getvalue()[-300:]!r}")


@ca
def c90_B2_MOT_BIEN_loi_do_khong_traceback_khong_no_chet():
    """r2 B2 (M2): một lỗi đo KHÔNG lường trước bên trong ba luật (ở đây: `_commit_cua` ném `RuntimeError`)
    ⇒ rc=2 cho tệp ấy, không traceback; và mục nợ của tệp ấy KHÔNG bị kết luận là nợ chết."""
    khoa = ("r.receipt.yaml", "anchor.mo_ta", bnv2.LUAT_ANCESTRY)
    for ten, no in (("khong-no", frozenset()), ("dang-la-no", frozenset({khoa}))):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})
            that = bnv2._commit_cua

            def _hong(*a, **kw):
                raise RuntimeError("git gia hong")
            bnv2._commit_cua = _hong
            try:
                rc, loi, tk = _kiem_cau(tmp, al, no)
            except Exception as ex:                               # noqa: BLE001
                bang(False, f"{ten}: lỗi đo thoát biên: {type(ex).__name__}: {ex}")
            finally:
                bnv2._commit_cua = that
            bang(rc == 2 and not loi and any("r.receipt.yaml" in x for x in tk["chua_do"]),
                 f"{ten}: đòi rc=2, không dòng ĐỎ (không NỢ CHẾT); được rc={rc} loi={loi} chua={tk['chua_do']}")


def _chay_cli(tmp: Path, al: dict, no_cau=frozenset(), co=(), path=None, env=None):
    """Chạy `bnv2.main` THẬT trên `tmp` với allowlist/nợ của fixture (tiêm vào biến mô-đun, trả lại sau).
    `path` đặt PATH trong lúc chạy (git vắng); `env` đặt thêm biến môi trường. Trả (rc, stderr) — ngoại lệ thoát
    `main` là lỗi của ca."""
    import contextlib
    import io
    env = dict(env or {})
    if path is not None:
        env["PATH"] = path
    cu_env = {k: os.environ.get(k) for k in env}
    cu = (bnv2.ALLOWLIST_CUTOVER, bnv2.NO_DA_DO, bnv2.NO_CAU_LICH_SU)
    bnv2.ALLOWLIST_CUTOVER, bnv2.NO_DA_DO, bnv2.NO_CAU_LICH_SU = al, {}, frozenset(no_cau)
    os.environ.update(env)
    ra, loi_ra = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi_ra):
            rc = bnv2.main(["--root", str(tmp), *co])
    except Exception as ex:                                       # noqa: BLE001
        bang(False, f"CLI {list(co)} chết bằng {type(ex).__name__}: {ex} — đòi rc=2, không traceback")
    finally:
        bnv2.ALLOWLIST_CUTOVER, bnv2.NO_DA_DO, bnv2.NO_CAU_LICH_SU = cu
        for k, v in cu_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return rc, loi_ra.getvalue()


# Hai commit rẽ từ B0 của `_kho_cau` (ngày ghim) mà 7 ký tự đầu TRÙNG nhau và toàn chữ số (`5298700`) — tìm
# ngoại tuyến bằng băm đối tượng commit (đo 27-10-2026); `commit-tree` với đúng thông điệp ra đúng hai SHA ấy.
_THONG_DIEP_TRUNG = ("mh122110", "mh211952")


def _commit_trung_tien_to(tmp: Path, k: dict):
    E = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
         "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", ""),
         "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
         "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"}
    cay = k["g"]("rev-parse", f"{k['B0']}^{{tree}}")
    sha = [subprocess.run(["git", "-C", str(tmp), "commit-tree", cay, "-p", k["B0"], "-m", m],
                          capture_output=True, text=True, env=E).stdout.strip() for m in _THONG_DIEP_TRUNG]
    dung(len({s[:7] for s in sha}) == 1 and sha[0] != sha[1] and sha[0][:7].isdigit(),
         f"fixture: hai commit không trùng tiền tố số: {sha}")
    return sha[0][:7]


def _tiem_git(dk, ket_qua):
    """Context manager: thay `_chay_git` của module `bnv2` ĐANG HIỆN HÀNH (đọc `globals()` lúc vào — module đột biến
    nếu có): lệnh mà `dk(args)` đúng thì trả `ket_qua(root, args, vao, timeout, goc)`, lệnh khác đi `goc`. Gỡ lại khi ra,
    kể cả khi thân ném lỗi. #1017: dùng cho nhánh mà nền không dựng được bằng git thật."""
    import contextlib

    @contextlib.contextmanager
    def _cm():
        mod = globals()["bnv2"]
        goc = mod._chay_git

        def gia(root, args, vao=None, timeout=60):
            if dk(args):
                return ket_qua(root, args, vao, timeout, goc)
            return goc(root, args, vao, timeout)
        mod._chay_git = gia
        try:
            yield
        finally:
            mod._chay_git = goc
    return _cm()


def _bn_anc_cau(tmp: Path):
    k = _kho_cau(tmp)
    return k, _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})


def _nguon_lstat_tiem(tmp: Path):
    """Nguồn c91 (#1017): "lstat lỗi khác ENOENT/ENOTDIR" dựng bằng TIÊM, chạy MỌI nền — tên quá dài chỉ cho lỗi ấy
    trên POSIX. Đường dẫn không tồn tại; `Path.lstat` của đúng đường dẫn ấy ném `PermissionError` trong lúc chạy CLI."""
    import json as _j
    rj = "ops/reviews/tiem-lstat/run.json"
    d, _ = _bn_surface(rj, "")
    al = _kho_surface(tmp, d, _j.dumps({"execution_surface": "codex_cli"}),
                      "provider: openai_codex\nexecution_surface: codex_service\n")
    return (tmp, al, ("r.receipt.yaml", "verdict_path", bnv2.LUAT_SURFACE), None, "tiem-lstat",
            lambda: _tiem_lstat(rj, PermissionError(13, "tiem #1017")))


def _nguon_canh_bao_tiem(tmp: Path):
    """Nguồn c91 (#1017): git in cảnh báo ở MỌI lệnh, dựng bằng TIÊM vào stderr — `core.fsyncObjectFiles` không làm
    git for Windows 2.55 in gì (đo trên máy Windows của chủ kho 29-10-2026), git 2.43 Linux thì có."""
    _, al = _bn_anc_cau(tmp)

    def kq(root, args, vao, timeout, goc):
        p = goc(root, args, vao, timeout)
        return subprocess.CompletedProcess(p.args, p.returncode, p.stdout, p.stderr + "warning: tiem-canh-bao-1017\n")
    return (tmp, al, ("r.receipt.yaml", "anchor.mo_ta", bnv2.LUAT_ANCESTRY), None, "tiem-canh-bao-1017",
            lambda: _tiem_git(lambda a: True, kq))


def _c96_tiem(tmp: Path, mau: str):
    """Biến thể tiêm của c96 (#1017), MỌI nền: lệnh khớp `mau` trả rc=3 + stderr RỖNG, lệnh khác đi git thật."""
    _, al = _bn_anc_cau(tmp)
    with _tiem_git(lambda a: any(mau in str(x) for x in a),
                   lambda root, a, v, t, g: subprocess.CompletedProcess(["git", *a], 3, "", "")):
        return _chay_cli(tmp, al)


def _qua_nguon_c91(dung_: tuple, co_no: bool):
    """Chạy MỘT nguồn c91 ĐÃ DỰNG qua CLI; trả (đạt?, mô tả). Dùng chung cho c91 và c97."""
    import contextlib
    goc, al, khoa, path, dau, *boc = dung_
    with (boc[0]() if boc else contextlib.nullcontext()):
        rc, loi_ra = _chay_cli(goc, al, {khoa} if co_no else (), path=path)
    dat = rc == 2 and "NỢ CHẾT" not in loi_ra and "Traceback" not in loi_ra and dau in loi_ra
    return dat, f"đòi rc=2, không NỢ CHẾT, stderr nêu `{dau}`; được rc={rc}: {loi_ra[-400:]!r}"


def _tiem_lstat(duoi: str, loi: OSError):
    """Context manager: `Path.lstat` của đường dẫn kết thúc bằng `duoi` (so theo `/`) ném `loi`; mọi đường khác đi lstat
    THẬT. Gỡ lại khi ra. #1017: chỉ dùng cho nhánh mà nền không dựng được bằng tệp thật."""
    import contextlib

    @contextlib.contextmanager
    def _cm():
        that = Path.lstat

        def gia(self, *a, **k):
            if str(self).replace("\\", "/").endswith(duoi):
                raise loi
            return that(self, *a, **k)
        Path.lstat = gia
        try:
            yield
        finally:
            Path.lstat = that
    return _cm()


@ca
def c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no():
    """r2 B2 (M2) + review r2 lượt 1–2: MỖI nguồn hỏng × {không nợ, có nợ trúng khoá} chạy QUA CLI ⇒ rc=2,
    không ngoại lệ, không `NỢ CHẾT`, và stderr nêu đúng nguồn (ca có ĐO, không chỉ rc). Nguồn: receipt là
    thư mục · receipt byte UTF-8 hỏng · alias vòng · `origin/master` là TREE (ref thật, không tiêm) · loose ref
    hỏng · symref `origin/HEAD` gãy · `run.json` là thư mục / symlink gãy / tên quá dài (lstat lỗi khác ENOENT) ·
    git vắng · tiền tố OID MƠ HỒ (hai commit) · object commit RỖNG · kho nông · partial clone (hai kiểu) · grafts ·
    cấu hình in cảnh báo ở mọi lệnh (tiền đề "cấu hình git không in cảnh báo", review r2 lượt 4).
    Tiền đề KHÔNG đo (quyết định chủ kho 29-10, #960): object/commit-graph sai mà git im lặng — cần `git fsck`."""
    import json as _j
    k_anc = ("r.receipt.yaml", "anchor.mo_ta", bnv2.LUAT_ANCESTRY)
    k_sf = ("r.receipt.yaml", "verdict_path", bnv2.LUAT_SURFACE)

    def _anc(tmp):
        k = _kho_cau(tmp)
        return k, _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})

    def receipt_thu_muc(tmp):
        k = _kho_cau(tmp)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, "x: 1\n")})
        (tmp / bnv2.THU_MUC / "hong.receipt.yaml").mkdir()
        return tmp, al, ("hong.receipt.yaml", "anchor.mo_ta", bnv2.LUAT_ANCESTRY), None, "hong.receipt.yaml"

    def receipt_utf8(tmp):
        k = _kho_cau(tmp)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, "x: 1\n")})
        (tmp / bnv2.THU_MUC / "hong.receipt.yaml").write_bytes(b"schema_version: 1\nx: \xff\n")
        return tmp, al, ("hong.receipt.yaml", "anchor.mo_ta", bnv2.LUAT_ANCESTRY), None, "UnicodeDecodeError"

    def alias_vong(tmp):
        k = _kho_cau(tmp)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, "cycle: &self [*self]\n")})
        return tmp, al, k_anc, None, "alias"

    def nhanh_la_tree(tmp):
        k, al = _anc(tmp)
        k["g"]("update-ref", "refs/remotes/origin/master", k["g"]("rev-parse", "HEAD^{tree}"))
        return tmp, al, k_anc, None, "refs/remotes/origin/master"

    def ref_hong(tmp):
        k, al = _anc(tmp)
        (tmp / ".git/refs/remotes/origin").mkdir(parents=True)
        (tmp / ".git/refs/remotes/origin/master").write_text("this-is-not-an-oid\n", encoding="utf-8")
        return tmp, al, k_anc, None, "broken ref"

    def symref_gay(tmp):
        k, al = _anc(tmp)
        k["g"]("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/gone")
        return tmp, al, k_anc, None, "dangling symref"

    def _surface(tmp, rj):
        d, _ = _bn_surface(rj, "")
        return _kho_surface(tmp, d, _j.dumps({"execution_surface": "codex_cli"}),
                            "provider: openai_codex\nexecution_surface: codex_service\n")

    def run_json_thu_muc(tmp):
        al = _surface(tmp, "ops/reviews/v/run.json")
        (tmp / "ops/reviews/v/run.json").unlink()
        (tmp / "ops/reviews/v/run.json").mkdir()
        return tmp, al, k_sf, None, "run.json"

    def run_json_symlink_gay(tmp):
        al = _surface(tmp, "ops/reviews/v/run.json")
        (tmp / "ops/reviews/v/run.json").unlink()
        (tmp / "ops/reviews/v/run.json").symlink_to("khong-co.json")
        return tmp, al, k_sf, None, "run.json"

    def run_json_ten_qua_dai(tmp):
        # #1017: hai thành phần, thử theo thứ tự, mỗi cái ĐO bằng lstat ĐỘC LẬP với `_vang` (m116 nhắm hàm ấy): tên quá dài
        # cho ENAMETOOLONG trên POSIX nhưng ENOENT trên Windows; ký tự cấm `<` cho WinError 123 (EINVAL) trên Windows nhưng
        # là tên hợp lệ (ENOENT) trên POSIX (đo phiên #1014 trên máy Windows của chủ kho). Dấu stderr lấy từ CHÍNH thành
        # phần đã dùng. Không cái nào cho lỗi khác ENOENT/ENOTDIR thì nói ra; nhánh ấy đo bằng `_nguon_lstat_tiem`.
        # Thư mục cha PHẢI có trước: thiếu nó thì lstat dừng ở ENOENT của `ops` mà chưa tới thành phần đang đo.
        (tmp / "ops/reviews").mkdir(parents=True, exist_ok=True)
        for phan, dau in (("a" * 300, "a" * 40), ("b" * 40 + "<c", "b" * 40)):
            rj = "ops/reviews/" + phan + "/run.json"
            try:
                os.lstat(tmp / rj)
                dung(False, f"fixture: lstat thành phần {dau}… lại thành công")
            except (FileNotFoundError, NotADirectoryError):
                continue
            except OSError:
                return tmp, _surface(tmp, rj), k_sf, None, dau
        return None


    def git_vang(tmp):
        k = _kho_cau(tmp)
        sha = _commit_tien_to_so(tmp, k, str.isalpha, "chu", 30000)
        k["g"]("merge", "-q", "--no-ff", sha, "-m", "merge")
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Ban {sha[:7]} chua vao master.\n")})
        trong = tmp / "_khong_co_git"
        trong.mkdir()
        return tmp, al, k_anc, str(trong), "không gọi được `git"

    def tien_to_mo_ho(tmp):
        k = _kho_cau(tmp)
        tt = _commit_trung_tien_to(tmp, k)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Ban {tt} chua vao master.\n")})
        return tmp, al, k_anc, None, "mơ hồ"

    def object_rong(tmp):
        k = _kho_cau(tmp)
        sha = _commit_tien_to_so(tmp, k, str.isalpha, "chu", 30000)
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Ban {sha[:7]} chua vao master.\n")})
        f = tmp / ".git/objects" / sha[:2] / sha[2:]
        dung(f.is_file(), f"fixture: object {sha} không phải loose")
        f.chmod(0o644)
        f.write_bytes(b"")
        return tmp, al, k_anc, None, "is empty"

    def kho_nong(tmp):
        nguon_ = tmp / "nguon"
        nguon_.mkdir()
        k = _kho_cau(nguon_)
        al = _ghi_bn_cau(nguon_, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})
        dich = tmp / "nong"
        r = subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{nguon_}", str(dich)],
                           capture_output=True, text=True)
        dung(r.returncode == 0, f"fixture: clone nông hỏng: {r.stderr[:200]}")
        return dich, al, k_anc, None, "kho nông"

    def kho_partial(tmp):
        k, al = _anc(tmp)
        k["g"]("config", "extensions.partialclone", "origin")
        return tmp, al, k_anc, None, "extensions.partialclone"

    def kho_partial_promisor(tmp):
        nguon_ = tmp / "nguon"
        nguon_.mkdir()
        k = _kho_cau(nguon_)
        al = _ghi_bn_cau(nguon_, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})
        k["g"]("config", "uploadpack.allowfilter", "true")
        dich = tmp / "partial"
        r = subprocess.run(["git", "clone", "-q", "--filter=blob:none", f"file://{nguon_}", str(dich)],
                           capture_output=True, text=True)
        dung(r.returncode == 0, f"fixture: clone partial hỏng: {r.stderr[:200]}")
        return dich, al, k_anc, None, "promisor` = true"

    def cau_hinh_canh_bao(tmp):
        k, al = _anc(tmp)
        # #1017: `core.fsyncObjectFiles=true` KHÔNG làm git for Windows 2.55 in gì (đo trên máy Windows của chủ kho; git
        # 2.43 Linux có in) ⇒ đổi sang thành phần `core.fsync` LẠ: git cảnh báo "ignoring unknown core.fsync component"
        # ở mọi lệnh trên CẢ HAI nền (đo: Linux 2.43 tại chỗ; Windows 2.55 do phiên #1014 đo trên cùng máy).
        k["g"]("config", "core.fsync", "khong-co-thanh-phan-1017")
        # Vẫn ĐO trước bằng chính đường gọi git của cổng: git nào không cảnh báo thì nói ra, đo bằng `_nguon_canh_bao_tiem`.
        if "khong-co-thanh-phan-1017" not in bnv2._chay_git(tmp, ["rev-parse", "--is-shallow-repository"]).stderr:
            return None
        return tmp, al, k_anc, None, "khong-co-thanh-phan-1017"

    def grafts(tmp):
        k, al = _anc(tmp)
        dau = k["g"]("rev-parse", "HEAD")
        (tmp / ".git/info").mkdir(exist_ok=True)
        (tmp / ".git/info/grafts").write_text(f"{dau} {k['B0']}\n", encoding="utf-8")
        k["g"]("config", "advice.graftFileDeprecated", "false")      # tắt lời nhắc: chốt phải đứng một mình
        return tmp, al, k_anc, None, "grafts"

    for nguon in (receipt_thu_muc, receipt_utf8, alias_vong, nhanh_la_tree, ref_hong, symref_gay, run_json_thu_muc,
                  run_json_symlink_gay, run_json_ten_qua_dai, _nguon_lstat_tiem, git_vang, tien_to_mo_ho,
                  object_rong, kho_nong, kho_partial, kho_partial_promisor, grafts, cau_hinh_canh_bao,
                  _nguon_canh_bao_tiem):
        for ten_no in ("khong-no", "co-no"):
            ten = f"{nguon.__name__}/{ten_no}"
            with tempfile.TemporaryDirectory() as t:
                dung_ = nguon(Path(t))
                if dung_ is None:                   # nền không dựng được nguồn này — nói ra, ĐỪNG giả xanh
                    print(f"  GHI CHÚ c91 {ten}: nền KHÔNG dựng được (đo) — nhánh ấy đo bằng nguồn tiêm")
                    continue
                dat, mo_ta = _qua_nguon_c91(dung_, ten_no == "co-no")
                bang(dat, f"{ten}: {mo_ta}")


@ca
def c92_B2_co_SINH_NO_cung_bien_voi_cong():
    """Review r2 lượt 1–2 (`sinh-no-ngoai-bien-doc-receipt`, `sinh-no-van-thoat-loi-yaml`): `--sinh-no` và
    `--sinh-no-cau-lich-su` trên receipt là thư mục / byte UTF-8 hỏng / YAML hỏng / timestamp sai (`ValueError`)
    / lồng sâu (`RecursionError`) ⇒ rc=2 nêu tên tệp, không ngoại lệ; dữ liệu lành ⇒ rc=0."""
    for hong, ghi in (("thu-muc", lambda p: p.mkdir()),
                      ("utf8", lambda p: p.write_bytes(b"schema_version: 1\nx: \xff\n")),
                      ("yaml", lambda p: p.write_text("a: [\n", encoding="utf-8")),
                      ("timestamp", lambda p: p.write_text("date: 2026-99-99\n", encoding="utf-8")),
                      ("long-sau", lambda p: p.write_text("a: " + "[" * 3000 + "]" * 3000 + "\n", encoding="utf-8")),
                      (None, None)):
        for co in ("--sinh-no", "--sinh-no-cau-lich-su"):
            ten = f"{hong}/{co}"
            with tempfile.TemporaryDirectory() as t:
                tmp = Path(t)
                k = _kho_cau(tmp)
                al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, "x: 1\n")})
                if hong:
                    ghi(tmp / bnv2.THU_MUC / "hong.receipt.yaml")
                rc, loi_ra = _chay_cli(tmp, al if co == "--sinh-no-cau-lich-su" else {}, co=(co,))
                if hong:
                    bang(rc == 2 and "hong.receipt.yaml" in loi_ra,
                         f"{ten}: đòi rc=2 nêu tệp hỏng, được rc={rc}: {loi_ra[-300:]!r}")
                else:
                    bang(rc == 0, f"{ten}: dữ liệu lành phải rc=0, được rc={rc}: {loi_ra[-300:]!r}")


# Một commit rẽ từ B0 (thông điệp `cb32615`) và một blob (nội dung `bl5361\n`) chung tiền tố `e4a3f5d` — tìm ngoại
# tuyến bằng băm đối tượng (đo 27-10-2026).
_COMMIT_BLOB_TRUNG = ("cb32615", "bl5361\n")


@ca
def c93_ung_vien_CHI_TINH_COMMIT_blob_chung_tien_to_khong_mo_ho():
    """Review r2 lượt 2 (`loc-ung-vien-commit-chua-co-rang`): tiền tố chung giữa MỘT commit và một blob vẫn trỏ
    đúng commit ấy — commit đã vào master ⇒ đúng một L-ANCESTRY (rc=1), không phải "mơ hồ" (rc=2)."""
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        cay = k["g"]("rev-parse", f"{k['B0']}^{{tree}}")
        E = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
             "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", ""),
             "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
             "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"}
        c = subprocess.run(["git", "-C", str(tmp), "commit-tree", cay, "-p", k["B0"], "-m", _COMMIT_BLOB_TRUNG[0]],
                           capture_output=True, text=True, env=E).stdout.strip()
        # #1017: BYTE qua stdin — `text=True` đổi `\n` thành `\r\n` trên Windows nên blob ra SHA khác.
        b = subprocess.run(["git", "-C", str(tmp), "hash-object", "-w", "--stdin"],
                           input=_COMMIT_BLOB_TRUNG[1].encode("utf-8"),
                           capture_output=True, env=E).stdout.decode("ascii").strip()
        dung(c[:7] == b[:7] and len(c) == 40, f"fixture: commit/blob không chung tiền tố: {c} {b}")
        k["g"]("merge", "-q", "--no-ff", c, "-m", "merge")
        al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {c[:7]} chua vao master.\n")})
        rc, loi, tk = _kiem_cau(tmp, al)
        bang(rc == 1 and len(loi) == 1 and loi[0].startswith("[L-ANCESTRY] r.receipt.yaml: `anchor.mo_ta`"),
             f"đòi đúng một L-ANCESTRY, được rc={rc} loi={loi} chua={tk['chua_do']}")


@ca
def c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC():
    """Kiến trúc tra git (r2, sau review lượt 2): stdout của `--disambiguate` / `cat-file --batch-check` /
    `for-each-ref` mà KHÔNG đúng dạng giao thức ⇒ `KhongDoDuoc`, không được lọc bỏ thành "không có"; ứng viên
    `--disambiguate` liệt kê mà `cat-file` nói `missing` ⇒ `KhongDoDuoc`; `config --type=bool` trả giá trị không
    phải true/false ⇒ `KhongDoDuoc` (review r2 lượt 5). Đồ giả thay `_git_do` theo lệnh."""
    that = bnv2._git_do
    h = "a" * 40

    def gia(bang_ra):
        def _g(root, *args, **kw):
            for khoa, ra in bang_ra.items():
                if khoa in args[0] + " " + " ".join(args[1:]):
                    return 0, ra
            return that(root, *args, **kw)
        return _g

    for ten, fn, bang_ra in (
            ("disambiguate-dong-la", lambda r: bnv2._commit_cua(r, "abcdef1"), {"rev-parse --disambiguate": "khong-phai-oid\n"}),
            ("batch-check-dang-la", lambda r: bnv2._commit_cua(r, "abcdef1"),
             {"rev-parse --disambiguate": h + "\n", "cat-file": h + " commit thua\n"}),
            ("batch-check-sai-oid", lambda r: bnv2._commit_cua(r, "abcdef1"),
             {"rev-parse --disambiguate": h + "\n", "cat-file": "b" * 40 + " commit\n"}),
            ("batch-check-sai-loai", lambda r: bnv2._commit_cua(r, "abcdef1"),
             {"rev-parse --disambiguate": h + "\n", "cat-file": h + " nonsense\n"}),
            ("ung-vien-missing", lambda r: bnv2._commit_cua(r, "abcdef1"),
             {"rev-parse --disambiguate": h + "\n", "cat-file": h + " missing\n"}),
            ("for-each-ref-dong-la", lambda r: bnv2._nhanh_mac_dinh(r), {"for-each-ref": "refs/heads/master khong-phai-oid commit\n"}),
            ("promisor-gia-tri-la", lambda r: bnv2._kho_lanh(r), {"config --type=bool": "remote.archive.promisor maybe\n"})):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _kho_cau(tmp)
            bnv2._git_do = gia(bang_ra)
            try:
                kq = fn(tmp)
                bang(False, f"{ten}: dạng lạ mà không ném KhongDoDuoc, trả {kq!r}")
            except bnv2.KhongDoDuoc:
                pass
            except TinHieuChotCa:
                raise
            except Exception as ex:                                   # noqa: BLE001
                bang(False, f"{ten}: chết bằng {type(ex).__name__}: {ex}, không phải KhongDoDuoc")
            finally:
                bnv2._git_do = that


@ca
def c95_moi_truong_git_KHONG_doi_ket_qua_do():
    """Review r2 lượt 3–4: kho LÀNH với câu sai thật (M đã vào master) phải ra ĐÚNG một L-ANCESTRY (rc=1) dù:
    replace ref che quan hệ tổ tiên · `GIT_DIR` kế thừa trỏ kho khác · `GIT_TRACE=1` · ref con
    `refs/remotes/origin/HEAD/topic` (for-each-ref khớp theo tiền tố) · `remote.<x>.promisor=false` (promisor TẮT) ·
    object nằm trong kho phụ qua `GIT_ALTERNATE_OBJECT_DIRECTORIES`."""
    def replace_ref(tmp, k):
        dau = k["g"]("rev-parse", "HEAD")
        k["g"]("replace", "--graft", dau, k["B0"])
        return {}

    def git_dir_khac(tmp, k):
        khac = tmp / "_khac"
        khac.mkdir()
        kk = _kho_cau(khac)
        # Kho ngoài có master = X (M KHÔNG là tổ tiên) — đo nhầm kho ấy thì ra SẠCH, không ra một vi phạm
        # (review r2 lượt 5: fixture cũ cùng đồ thị nên không phân biệt được kho nào được đo).
        kk["g"]("update-ref", "refs/heads/master", kk["X"])
        return {"GIT_DIR": str(khac / ".git")}

    def git_trace(tmp, k):
        return {"GIT_TRACE": "1"}

    def promisor_tat(tmp, k):
        # Ba cách viết TẮT mà git chấp nhận; `off`/`no` chỉ đúng khi đọc qua `--type=bool` (review r2 lượt 5).
        for remote, gt in (("archive", "false"), ("a2", "off"), ("a3", "no")):
            k["g"]("config", f"remote.{remote}.promisor", gt)
        return {}

    def alternates_env(tmp, k):
        k["g"]("repack", "-q", "-a", "-d")
        k["g"]("prune-packed")
        pool = tmp / "_pool"
        (pool / "pack").mkdir(parents=True)
        for f in (tmp / ".git/objects/pack").iterdir():
            f.rename(pool / "pack" / f.name)
        con = [x for x in (tmp / ".git/objects").rglob("*") if x.is_file() and x.parent.name not in ("info", "pack")]
        dung(not con, f"fixture: còn object rời trong kho: {con[:3]}")
        return {"GIT_ALTERNATE_OBJECT_DIRECTORIES": str(pool)}

    def ref_con_tien_to(tmp, k):
        k["g"]("update-ref", "refs/remotes/origin/master", k["g"]("rev-parse", "HEAD"))
        k["g"]("update-ref", "refs/remotes/origin/HEAD/topic", k["B0"])
        return {}

    for kieu in (replace_ref, git_dir_khac, git_trace, ref_con_tien_to, promisor_tat, alternates_env):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            al = _ghi_bn_cau(tmp, k, {"r.receipt.yaml": _bn_cau(1, f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})
            env = kieu(tmp, k)
            rc, loi_ra = _chay_cli(tmp, al, env=env)
            bang(rc == 1 and loi_ra.count("[L-ANCESTRY] r.receipt.yaml: `anchor.mo_ta`") == 1 and "KHÔNG ĐO" not in loi_ra,
                 f"{kieu.__name__}: đòi đúng một L-ANCESTRY rc=1; được rc={rc}: {loi_ra[-400:]!r}")


@ca
def c96_git_rc_LA_ma_stderr_RONG_van_la_KHONG_DO_DUOC():
    """Review r2 lượt 3–4 (`chot-ma-thoat-git-chua-co-rang`, `chot-probe-git-chua-co-rang`): một lệnh git trả rc ngoài
    tập sạch mà KHÔNG in gì ra stderr (git giả bọc git thật) ⇒ KHÔNG ĐO ĐƯỢC (rc=2), không phải vi phạm hay sạch —
    cho cả `merge-base` lẫn lệnh kiểm sức khoẻ kho đầu tiên (`--is-shallow-repository`)."""
    import shutil
    that = shutil.which("git")
    dung(that is not None, "fixture: không có git")
    for mau in ("merge-base", "is-shallow-repository"):
        for cach in ("path", "tiem"):
            with tempfile.TemporaryDirectory() as t:
                tmp = Path(t)
                if cach == "path":
                    _, al = _bn_anc_cau(tmp)
                    bin_ = tmp / "_bin"
                    bin_.mkdir()
                    gia = bin_ / "git"
                    gia.write_bytes((f"#!/bin/sh\ncase \"$*\" in *__do_gia_wp1017__*) echo GIT-GIA; exit 0;; "
                                     f"*{mau}*) exit 3;; esac\n" f'exec "{that}" "$@"\n').encode("utf-8"))
                    gia.chmod(0o755)
                    path = f"{bin_}{os.pathsep}{os.environ.get('PATH', '')}"
                    # #1017: ĐO nền trước — Windows `CreateProcess` chỉ tìm `git.exe`, nên script không đuôi ở đầu PATH
                    # KHÔNG được gọi và git thật trả rc=1 (run 40833816523). Không bọc được thì nói ra, đo bằng tiêm.
                    try:
                        do = subprocess.run(["git", "__do_gia_wp1017__"], capture_output=True, text=True,
                                            env={**os.environ, "PATH": path}, timeout=60).stdout
                    except OSError:
                        do = ""
                    if "GIT-GIA" not in do:
                        print(f"  GHI CHÚ c96 {mau}/path: nền KHÔNG bọc được git qua PATH (đo) — đo bằng tiêm")
                        continue
                    rc, loi_ra = _chay_cli(tmp, al, path=path)
                else:
                    rc, loi_ra = _c96_tiem(tmp, mau)
                bang(rc == 2 and mau in loi_ra and "rc=3" in loi_ra,
                     f"{mau}/{cach}: đòi rc=2 nêu `{mau}` rc=3, được rc={rc}: {loi_ra[-400:]!r}")



@ca
def c97_NHANH_TIEM_co_rang_tren_module_da_thay_va_tu_go():
    """#1017 cross-review lượt 1 (`nhanh-tiem-thieu-chot-tu-kiem`, P2): trên Linux m116/m125/m114 chết ở biến thể THẬT trước
    khi tới nhánh tiêm, nên hai đột biến của CHÍNH phần tiêm SỐNG qua toàn suite — tiêm vá nhầm module (`_BNV2_THAT` thay
    vì `bnv2` hiện hành) và không gỡ `Path.lstat`. Trên Windows nhánh tiêm là đường DUY NHẤT, nên lỗi ấy biến thành tín
    dụng giết giả. Ca này đo nhánh tiêm ĐỘC LẬP với biến thể thật, trên MỌI nền:
      · đối chứng DƯƠNG: module đã THAY bằng bản sao VÔ HẠI (chỉ đổi một docstring) ⇒ cả ba nhánh tiêm phải qua;
      · răng: bản sao m116 / m125 / m114 ⇒ đúng nhánh tiêm tương ứng phải ĐỎ;
      · tự gỡ: `Path.lstat` và `_chay_git` trở lại đúng object cũ, kể cả khi thân `with` ném lỗi."""
    VO_HAI = ('    """Đường dẫn VẮNG thật — không mục nào, kể cả symlink gãy.',
              '    """Đường dẫn VẮNG thật — không mục nào, kể cả symlink gãy. (bản sao vô hại #1017)')
    M116 = ("    except OSError:\n        return False\n    return False\n",
            "    except OSError:\n        return True\n    return False\n")
    M125 = ("    if p.returncode not in sach:\n        raise KhongDoDuoc(", "    if False:\n        raise KhongDoDuoc(")
    M114 = ("    if con:\n        raise KhongDoDuoc(", "    if False:\n        raise KhongDoDuoc(")

    def lstat_tiem():
        with tempfile.TemporaryDirectory() as t:
            return _qua_nguon_c91(_nguon_lstat_tiem(Path(t)), False)

    def canh_bao_tiem():
        with tempfile.TemporaryDirectory() as t:
            return _qua_nguon_c91(_nguon_canh_bao_tiem(Path(t)), False)

    def rc3_tiem():
        with tempfile.TemporaryDirectory() as t:
            rc, loi_ra = _c96_tiem(Path(t), "merge-base")
            return rc == 2 and "merge-base" in loi_ra and "rc=3" in loi_ra, f"rc={rc}: {loi_ra[-300:]!r}"

    nhanh = {"lstat": (lstat_tiem, M116), "canh-bao": (canh_bao_tiem, M114), "rc3": (rc3_tiem, M125)}
    lstat0 = Path.lstat
    the = globals()["bnv2"], globals()["CONG"]
    try:
        for ten, (ham, dot_bien) in nhanh.items():
            for nhan, sua, mong_dat in (("vo-hai", VO_HAI, True), ("dot-bien", dot_bien, False)):
                _dot_bien_tep(*sua)
                try:
                    mod = globals()["bnv2"]
                    git0 = mod._chay_git
                    dat, mo_ta = ham()
                    bang(dat == mong_dat,
                         f"nhánh tiêm `{ten}` trên bản sao {nhan}: đòi {'QUA' if mong_dat else 'ĐỎ'}, được "
                         f"{'QUA' if dat else 'ĐỎ'} — {mo_ta}")
                    bang(Path.lstat is lstat0, f"nhánh tiêm `{ten}` ({nhan}) KHÔNG gỡ `Path.lstat`")
                    bang(mod._chay_git is git0, f"nhánh tiêm `{ten}` ({nhan}) KHÔNG gỡ `_chay_git`")
                finally:
                    globals()["bnv2"], globals()["CONG"] = the
        # Tự gỡ cả khi thân ném lỗi.
        for cm in (_tiem_lstat("x/y", PermissionError(13, "t")), _tiem_git(lambda a: True, lambda *a: None)):
            git0 = globals()["bnv2"]._chay_git
            try:
                with cm:
                    raise RuntimeError("thân ném lỗi")
            except RuntimeError:
                pass
            bang(Path.lstat is lstat0 and globals()["bnv2"]._chay_git is git0,
                 "context manager tiêm KHÔNG gỡ khi thân ném lỗi")
    finally:
        Path.lstat = lstat0
        globals()["bnv2"], globals()["CONG"] = the
        while _TAM_DOT_BIEN:
            shutil.rmtree(_TAM_DOT_BIEN.pop(), ignore_errors=True)


@ca
def c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen():
    """#1021 (`BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, C1a/C1b): cổng THẤY `x.RECEIPT.YAML` trên MỌI nền.

    `glob` cũ bỏ qua đuôi hoa LẶNG trên POSIX mà kiểm trên Windows. Ba fixture, mỗi cái một kho git thật:
    - C1a: `y.receipt.yaml` + `x.RECEIPT.YAML`, cả hai YAML HỢP LỆ mà sai lược đồ ⇒ dòng tổng `tổng 2`, đầu ra
      nêu `x.RECEIPT.YAML`, không `TỔNG: ĐẠT`. Không đòi rc cụ thể: kho tạm có thể sinh `KHÔNG ĐO ĐƯỢC` vô can.
    - chỉ `x.RECEIPT.YAML` ⇒ `tổng 1`, KHÔNG có thông báo "không có tệp".
    - C1b: `x.RECEIPT.YAML` là YAML HỎNG ⇒ rc=2, stderr nêu tên, không traceback. YAML hỏng làm cổng dừng
      TRƯỚC dòng tổng (hành vi có sẵn), nên C1b không đòi `tổng` — lý do r2 tách C1 (Codex connector P2, #1019).
    Đột biến `m142` (so đuôi CHÍNH XÁC) giết cả ba trên CẢ HAI nền."""
    import contextlib
    import io
    tong_re = _RE.compile(r"· tổng (\d+)$", _RE.M)

    def chay(tep):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            k = _kho_cau(tmp)
            _ghi_bn_cau(tmp, k, tep)
            ra, loi = io.StringIO(), io.StringIO()
            try:
                with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
                    rc = bnv2.main(["--root", str(tmp)])
            except LoiDungCa:
                raise                     # giàn giáo hỏng KHÔNG được đội lốt "ca đỏ" (quan sát RIG, Codex lượt 1)
            except Exception as ex:                               # noqa: BLE001
                bang(False, f"{sorted(tep)}: CLI chết bằng {type(ex).__name__}: {ex}")
            tong = tong_re.findall(ra.getvalue())
            return rc, ra.getvalue(), loi.getvalue(), (int(tong[-1]) if tong else None)

    rc, ra, loi, tong = chay({"y.receipt.yaml": "a: 1\n", "x.RECEIPT.YAML": "b: 2\n"})
    bang(tong == 2 and "x.RECEIPT.YAML" in ra + loi and rc != 0 and "TỔNG: ĐẠT" not in ra,
         f"C1a: đòi tổng 2 nêu x.RECEIPT.YAML, không ĐẠT; được rc={rc} tổng={tong}: {(ra + loi)[-300:]!r}")
    rc, ra, loi, tong = chay({"x.RECEIPT.YAML": "b: 2\n"})
    bang(tong == 1 and "không có tệp" not in loi,
         f"chỉ-x: đòi tổng 1, không 'không có tệp'; được rc={rc} tổng={tong}: {loi[-300:]!r}")
    rc, ra, loi, tong = chay({"y.receipt.yaml": "a: 1\n", "x.RECEIPT.YAML": "b: [\n"})
    bang(rc == 2 and "x.RECEIPT.YAML" in loi and "Traceback" not in ra + loi,
         f"C1b: đòi rc=2 nêu x.RECEIPT.YAML, không traceback; được rc={rc}: {loi[-300:]!r}")


@ca
def c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE():
    """#1021, cross-review Codex lượt 1 (`bo-chon-ung-vien-thieu-rang-hai-duong-goi`, P2): ba đột biến phá bộ
    chọn vẫn qua toàn suite vì `c101` (bản trước tên `c98`) chỉ đi đường `kiem`. Bốn chốt, mỗi chốt một đột biến riêng (m144–m147):
    1. `--sinh-no` THẤY `X.RECEIPT.YAML` (rc=0, khối nợ nêu tên, `# 1 tệp`) — m144 lọc đuôi chính xác ở `_sinh_no`.
    2. Thứ tự: `iterdir` bị ép trả NGƯỢC mà helper vẫn trả đã sắp xếp — m145 bỏ `sorted`. Tên toàn chữ thường nên
       thứ tự `Path` giống nhau trên mọi nền (không so hai tên chỉ khác hoa thường).
    3. Kho thật thiếu `ops/reviews`: `kiem` rc=2 (guard riêng), `--sinh-no` rc=0 + `# 0 tệp` — m146 bỏ nhánh thư mục
       vắng của helper (khi ấy `--sinh-no` ra rc=2 vì lỗi liệt kê).
    4. Liệt kê ném `PermissionError` ⇒ cả `kiem` lẫn `--sinh-no` rc=2 nêu "không liệt kê được", không traceback —
       m147 bỏ phép bắt `OSError` (hồi quy `loi-do-liet-ke-thu-muc-thoat-traceback` mà Codex đo được)."""
    import contextlib
    import io

    def cli(tmp, *co):
        ra, loi = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
                rc = bnv2.main(["--root", str(tmp), *co])
        except LoiDungCa:
            raise
        except Exception as ex:                                   # noqa: BLE001
            bang(False, f"{list(co)}: CLI chết bằng {type(ex).__name__}: {ex} — đòi mã thoát, không traceback")
        return rc, ra.getvalue(), loi.getvalue()

    goc = Path.iterdir
    # (1) --sinh-no thấy đuôi hoa
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        _ghi_bn_cau(tmp, k, {"x.RECEIPT.YAML": "b: 2\n"})
        rc, ra, loi = cli(tmp, "--sinh-no")
        bang(rc == 0 and '"x.RECEIPT.YAML"' in ra and "# 1 tệp" in loi,
             f"sinh-no: đòi rc=0, khối nợ nêu x.RECEIPT.YAML, `# 1 tệp`; được rc={rc}: {(ra + loi)[-300:]!r}")
    # (2) thứ tự: ép iterdir trả ngược
    with tempfile.TemporaryDirectory() as t:
        tm = Path(t) / "r"
        tm.mkdir()
        ten = ["a.receipt.yaml", "m.receipt.yaml", "z.receipt.yaml"]
        for x in ten:
            (tm / x).write_bytes(b"a: 1\n")

        def nguoc(self):
            return iter(sorted(goc(self), reverse=True))
        Path.iterdir = nguoc
        try:
            dung([p.name for p in tm.iterdir()] == ten[::-1], "fixture: iterdir ngược không có hiệu lực")
            ds = [p.name for p in bnv2._chon_bien_nhan(tm)]
        finally:
            Path.iterdir = goc
        bang(ds == ten, f"thứ tự: đòi {ten} khi iterdir trả ngược, được {ds}")
    # (3) kho thật thiếu ops/reviews
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        _kho_cau(tmp)
        dung(not (tmp / bnv2.THU_MUC).exists(), "fixture: ops/reviews không được tồn tại")
        rc, ra, loi = cli(tmp)
        bang(rc == 2 and "không có" in loi, f"vắng/kiem: đòi rc=2 'kho thật mà không có'; được rc={rc}: {loi[-300:]!r}")
        rc, ra, loi = cli(tmp, "--sinh-no")
        bang(rc == 0 and "# 0 tệp" in loi, f"vắng/sinh-no: đòi rc=0 `# 0 tệp`; được rc={rc}: {loi[-300:]!r}")
    # (4) lỗi liệt kê
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        _ghi_bn_cau(tmp, k, {"y.receipt.yaml": "a: 1\n"})
        dich = (tmp / bnv2.THU_MUC).resolve()
        # Codex lượt 3 (#1021, P3): tiêm cả một `OSError` KHÔNG phải `PermissionError` (EIO), kẻo phép bắt bị thu
        # hẹp thành `PermissionError` vẫn qua (m155).
        for tao in (lambda s: PermissionError(errno.EACCES, "Permission denied (tiêm, #1021)", s),
                    lambda s: OSError(errno.EIO, "I/O error (tiêm, #1021)", s)):
            def hong(self, tao=tao):
                if Path(self).resolve() == dich:
                    raise tao(str(self))
                return goc(self)
            for co in ((), ("--sinh-no",)):
                Path.iterdir = hong
                try:
                    rc, ra, loi = cli(tmp, *co)
                finally:
                    Path.iterdir = goc
                bang(rc == 2 and "không liệt kê được" in loi and "Traceback" not in ra + loi,
                     f"liệt kê hỏng {list(co)} ({type(tao('')).__name__}): đòi rc=2 'không liệt kê được'; "
                     f"được rc={rc}: {loi[-300:]!r}")


@ca
def c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang():
    """#1021, cross-review Codex lượt 2. Ba chốt, mỗi chốt một đột biến riêng (m148–m152):
    5. `stat` của `ops/reviews` ném `PermissionError` (`is_dir()` chỉ nuốt ENOENT/ENOTDIR/…) ⇒ cả `kiem` lẫn
       `--sinh-no` rc=2 nêu "không đọc được trạng thái", không traceback (P2 `loi-do-liet-ke-thu-muc-thoat-traceback`,
       biểu hiện thứ hai) — m148 helper hỏi `is_dir()` trần, m149 guard của `kiem` hỏi trần, m150 bỏ bắt `OSError`.
    6. Kho thiếu `ops/reviews` mà `stat` của `.git` ném ⇒ `kiem` rc=2 nêu `.git`, không traceback — m151.
    7. Lỗi LẬP TRÌNH (`RuntimeError` mốc) ở phép liệt kê hoặc phép hỏi thư mục phải đi THẲNG ra khỏi `main`, đúng
       đối tượng, trên cả hai đường (P3 `loi-do-thieu-chot-ngoai-le-lap-trinh`) — m152 nới bắt liệt kê thành
       `Exception`, m153 nới `_hoi_trang_thai` thành `Exception`."""
    import contextlib
    import io

    def cli(tmp, *co):
        ra, loi = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
                rc = bnv2.main(["--root", str(tmp), *co])
        except LoiDungCa:
            raise
        except Exception as ex:                                   # noqa: BLE001
            bang(False, f"{list(co)}: CLI chết bằng {type(ex).__name__}: {ex} — đòi mã thoát, không traceback")
        return rc, ra.getvalue(), loi.getvalue()

    def tiem(ten, dich, loi_tao):
        """Thay `Path.<ten>` bằng bản ném `loi_tao()` khi đúng `dich`; trả (khôi phục, đếm lượt trúng)."""
        goc = getattr(Path, ten)
        trung = []

        def gia(self, *a, **k):
            if Path(self).resolve() == dich:
                trung.append(1)
                raise loi_tao()
            return goc(self, *a, **k)
        setattr(Path, ten, gia)
        return (lambda: setattr(Path, ten, goc)), trung

    # Codex lượt 3 (#1021, P3): hai lớp `OSError` — `PermissionError` VÀ một `OSError` thường (EIO) — kẻo phép bắt
    # thu hẹp thành `PermissionError` vẫn qua (m154).
    OS_LOI = (lambda: PermissionError(errno.EACCES, "Permission denied (tiêm, #1021)"),
              lambda: OSError(errno.EIO, "I/O error (tiêm, #1021)"))

    # (5) stat của thư mục biên nhận ném EACCES
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        _ghi_bn_cau(tmp, k, {"y.receipt.yaml": "a: 1\n"})
        dich = (tmp / bnv2.THU_MUC).resolve()
        for tao in OS_LOI:
            for co in ((), ("--sinh-no",)):
                tra, trung = tiem("is_dir", dich, tao)
                try:
                    rc, ra, loi = cli(tmp, *co)
                finally:
                    tra()
                dung(trung, f"fixture: is_dir của {dich} không được hỏi {list(co)}")
                bang(rc == 2 and "không đọc được trạng thái" in loi and "Traceback" not in ra + loi,
                     f"stat hỏng {list(co)} ({type(tao()).__name__}): đòi rc=2 'không đọc được trạng thái'; "
                     f"được rc={rc}: {loi[-300:]!r}")
    # (6) kho thiếu ops/reviews, stat của .git ném
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        _kho_cau(tmp)
        dung(not (tmp / bnv2.THU_MUC).exists(), "fixture: ops/reviews không được tồn tại")
        for tao in OS_LOI:
            tra, trung = tiem("exists", (tmp / ".git").resolve(), tao)
            try:
                rc, ra, loi = cli(tmp)
            finally:
                tra()
            dung(trung, "fixture: exists của .git không được hỏi")
            bang(rc == 2 and "không đọc được trạng thái" in loi and ".git" in loi and "Traceback" not in ra + loi,
                 f".git hỏng ({type(tao()).__name__}): đòi rc=2 nêu .git; được rc={rc}: {loi[-300:]!r}")
    # (7) lỗi lập trình đi thẳng
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k = _kho_cau(tmp)
        _ghi_bn_cau(tmp, k, {"y.receipt.yaml": "a: 1\n"})
        dich = (tmp / bnv2.THU_MUC).resolve()
        for ten in ("iterdir", "is_dir"):
            for co in ((), ("--sinh-no",)):
                moc = RuntimeError(f"mốc lỗi lập trình #1021 ({ten})")
                tra, trung = tiem(ten, dich, lambda: moc)
                bay = None
                try:
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        bnv2.main(["--root", str(tmp), *co])
                except RuntimeError as ex:
                    bay = ex
                finally:
                    tra()
                dung(trung, f"fixture: {ten} của {dich} không được hỏi {list(co)}")
                bang(bay is moc, f"lỗi lập trình ở {ten} {list(co)} bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, "
                                 f"được {type(bay).__name__ if bay else 'không ngoại lệ'}")
@ca
def c98_TIN_DUNG_GIA_phai_in_DU_ngoai_le_va_vi_tri_nem():
    """#1037: một đột biến KHÔNG đạt phải để lại đủ dấu vết để truy. (a) `_chay_1` với ca ném lỗi không phải chốt ⇒
    `tin_dung_gia` + tên ngoại lệ + thông điệp + vị trí ném ĐÚNG hàm; (b) `_dong_chi_tiet` của kết quả không đạt mang
    `tt` và MỌI dòng `ct`, của kết quả đạt thì rỗng; (c) vượt trần thì cắt và nói đã cắt."""
    global _CA
    ca_ngoai = _CA

    def _nem_trong():
        raise AttributeError("thuoc_tinh_1037_vang")

    def _ca_nem_attr():
        _nem_trong()
    try:
        tt, ct = _chay_1(_ca_nem_attr)
    finally:
        _CA = ca_ngoai
    bang(tt == "tin_dung_gia", f"ca ném AttributeError phải là tin_dung_gia, được {tt}")
    bang("AttributeError: thuoc_tinh_1037_vang" in (ct or ""), f"thiếu tên/thông điệp ngoại lệ: {ct!r}")
    # Dòng `raise` đọc từ code object, KHÔNG ghi cứng: tệp này đổi dòng mỗi lần thêm import.
    vt = f"{Path(__file__).name}:{_nem_trong.__code__.co_firstlineno + 1} in _nem_trong"
    bang(vt in (ct or ""), f"vị trí ném phải là khung TRONG CÙNG `{vt}`: {ct!r}")

    ct2 = "dong-1 loi that\ndong-2 ngu canh\ndong-3 cuoi"
    dong = _dong_chi_tiet(False, "tin_dung_gia", ct2)
    bang(bool(dong) and "tin_dung_gia" in dong[0], f"dòng đầu phải nêu tt: {dong!r}")
    for x in ("dong-1 loi that", "dong-2 ngu canh", "dong-3 cuoi"):
        bang(any(x in d for d in dong), f"chi tiết mất dòng `{x}`: {dong!r}")
    bang(_dong_chi_tiet(True, "giet_that", ct2) == [], "đột biến ĐẠT không được in thêm chi tiết")
    # Dây nối: thứ `do()` in cho đột biến KHÔNG đạt phải chứa ngoại lệ thật; cho đột biến đạt thì đúng một dòng.
    kq = _dong_ket_qua_dot_bien("KHÔNG RĂNG", "mX", "cY", tt, "mo ta", False, ct)
    bang(len(kq) > 1 and any("thuoc_tinh_1037_vang" in d for d in kq) and "mX" in kq[0],
         f"dòng in của đột biến KHÔNG đạt thiếu ngoại lệ thật: {kq!r}")
    bang(len(_dong_ket_qua_dot_bien("CÓ RĂNG ", "mX", "cY", "giet_that", "mo ta", True, ct2)) == 1,
         "đột biến ĐẠT phải in đúng một dòng như trước")
    bang(any("không có chi tiết" in d for d in _dong_chi_tiet(False, "gian_giao", None)),
         "ct rỗng phải nói rõ là không có chi tiết, không im lặng")

    dai = "x" * 50 + "DUOI_BI_CAT"
    cat = "\n".join(_dong_chi_tiet(False, "tin_dung_gia", dai, tran=50))
    bang("DUOI_BI_CAT" not in cat and "cắt" in cat, f"vượt trần phải cắt và nói đã cắt: {cat!r}")
    bang("x" * 50 in cat, f"phần trong trần phải giữ nguyên: {cat!r}")
    # Trần MẶC ĐỊNH (đường `do()` dùng, không truyền `tran`) là 2000 — số của đặc tả, không lấy từ chính hàm.
    cat_md = "\n".join(_dong_chi_tiet(False, "tin_dung_gia", "y" * 2000 + "DUOI5"))
    bang("DUOI5" not in cat_md and "còn 5 ký tự" in cat_md and "y" * 2000 in cat_md,
         f"trần mặc định 2000 không cắt đúng: …{cat_md[-80:]!r}")

    # Đường THẬT của `do()` (#1037 lượt 1, P2): chạy đúng m81 qua `_dot_bien(chi=…)`, thu stdout. Ca đích thay bằng
    # một ca CÙNG TÊN ném AttributeError ⇒ dòng in phải mang ngoại lệ + vị trí; ca đích thật ⇒ đúng một dòng.
    ten_m, i = "m81_bo_chot_no_chet", next(k for k, f in enumerate(CA) if f.__name__.startswith("c74_"))
    c74_that = CA[i]

    def _c74_gia():
        raise AttributeError("c98_qua_do_that")
    _c74_gia.__name__ = c74_that.__name__

    def _qua_do(ca_dich):
        buf = io.StringIO()
        CA[i] = ca_dich
        try:
            with contextlib.redirect_stdout(buf):
                ket = _dot_bien(chi={ten_m})
        finally:
            CA[i] = c74_that
            globals()["_CA"] = ca_ngoai
        return ket, buf.getvalue().splitlines()
    ket, ra_in = _qua_do(_c74_gia)
    vt_gia = f"{Path(__file__).name}:{_c74_gia.__code__.co_firstlineno + 1} in {_c74_gia.__code__.co_name}"
    bang(len(ket) == 1 and ket[0][0] == ten_m and ket[0][3] == "tin_dung_gia",
         f"`_dot_bien(chi=…)` phải chạy đúng {ten_m} và ra tin_dung_gia: {ket!r}")
    bang(any("chi tiết [tin_dung_gia]" in d for d in ra_in)
         and any("AttributeError: c98_qua_do_that" in d and vt_gia in d for d in ra_in),
         f"stdout của `do()` thiếu ngoại lệ/vị trí `{vt_gia}`: {ra_in!r}")
    ket, ra_in = _qua_do(c74_that)
    bang(len(ket) == 1 and ket[0][2] and len(ra_in) == 1 and ten_m in ra_in[0],
         f"đột biến ĐẠT qua `do()` phải in đúng một dòng: {ra_in!r} · {ket!r}")


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
        return "tin_dung_gia", f"{type(ex).__name__}: {ex} [ném tại {_vi_tri_nem(ex)}]"
    finally:
        _CA = None


def _vi_tri_nem(ex: BaseException) -> str:
    """#1037: khung TRONG CÙNG nơi ngoại lệ được ném (`tệp:dòng in hàm`). Laptop Windows (head `7b92e5c`) cho
    `m81 → c74 = tin_dung_gia` đúng một lần trong lượt full rồi 22/22 `giet_that` khi chạy riêng — và không truy
    được gì vì chỉ còn `type: msg`. Lần sau nó lặp lại thì vị trí này là thứ phân biệt rig với sản phẩm."""
    tb = traceback.extract_tb(ex.__traceback__)
    if not tb:
        return "không có traceback"
    f = tb[-1]
    return f"{Path(f.filename).name}:{f.lineno} in {f.name}"


_TRAN_CHI_TIET = 2000


def _dong_chi_tiet(dat: bool, tt: str, ct, tran: int = _TRAN_CHI_TIET) -> list:
    """#1037: dòng in thêm dưới một đột biến KHÔNG đạt — `tt` + `ct` đủ nhiều dòng, có trần. Đột biến đạt ⇒ rỗng
    (log xanh giữ nguyên). Trước đây `do()` chỉ in `mo_ta`, nên ngoại lệ thật của một `tin_dung_gia` mất hẳn."""
    if dat:
        return []
    van = ct or "(không có chi tiết)"
    if len(van) > tran:
        van = van[:tran] + f" …[cắt, còn {len(van) - tran} ký tự]"
    return [f"      chi tiết [{tt}]:"] + [f"        {x}" for x in van.splitlines()]


def _dong_ket_qua_dot_bien(nhan, ten, ca_dich, tt, mo_ta, dat, ct) -> list:
    """Toàn bộ những gì `do()` in cho một đột biến — gom một chỗ để `c98` đo được cả dây nối, không chỉ hàm con."""
    return [f"  {nhan:10s} {ten:38s} → {ca_dich} = {tt}  ({mo_ta})"] + _dong_chi_tiet(dat, tt, ct)


# ------------------------------------------------------------------ đột biến
def _dot_bien(chi=None):
    """Mỗi đột biến phải làm ĐÚNG ca đích ĐỎ. Không đỏ ⇒ ca ấy rỗng.

    `chi` (#1037): tập tên đột biến được chạy — CHỈ để `c98` đi qua đúng thân `do()` thật với một đột biến;
    `main` gọi không đối số nên bảng chạy đủ như trước."""
    ra = []

    def do(ten, sua, ca_dich, mo_ta, doi_chung=None, mong_khong_rang=False, mong_gian_giao=False):
        if chi is not None and ten not in chi:
            return
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
        # Ca TỰ KIỂM đảo kỳ vọng: nó ĐẠT khi bị báo KHÔNG CÓ RĂNG — hoặc, với `mong_gian_giao`
        # (`R7-03`), ĐÚNG khi bị phân GIÀN GIÁO: rig hỏng phải bị bắt TRƯỚC khi ca đích chạy,
        # và "không răng" vì lý do khác không được tính là đạt.
        if mong_gian_giao:
            dat = tt == "gian_giao"
        else:
            dat = (not ok) if mong_khong_rang else ok
        tu_kiem = bool(mong_khong_rang or mong_gian_giao)
        # HAI CỜ đi kèm mỗi hàng để TỔNG KẾT TỰ SUY RA, không chép tay: `R4-03` đo được
        # tử số loại `m14` ra mà mẫu số vẫn giữ nó, và một tỉ lệ "6/21" chép tay trong chú
        # thích + CHANGELOG đã lệch ngay ở đoạn vừa sửa một lời khai rộng hơn phép đo.
        ra.append((ten, ca_dich, dat, tt, ((ct or "").splitlines() or [""])[0][:80],
                   tu_kiem, bool(doi_chung)))
        nhan = ("TỰ KIỂM ok" if dat else "TỰ KIỂM ĐỎ") if tu_kiem else (
            "CÓ RĂNG " if ok else "KHÔNG RĂNG")
        print("\n".join(_dong_ket_qua_dot_bien(nhan, ten, ca_dich, tt, mo_ta, dat, ct)))

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
    # Connector (P2, `#discussion_r3944298447`) chỉ tên đúng chỗ này: bảng cũ có MỘT hàng
    # `anchor` và nó chỉ phá `cuong_do`, nên gỡ `loai` khỏi yêu cầu vẫn xanh. Hai khoá là
    # HAI yêu cầu, và mỗi cái phải có đột biến RIÊNG — không mượn nhau.
    do("m30_bo_yeu_cau_anchor_loai",
       lambda: setattr(bnv2, "YEU_CAU", tuple(x for x in bnv2.YEU_CAU if x[0] != "anchor.loai")),
       "c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong", "gỡ `anchor.loai` khỏi cổng")
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
       lambda: _dot_bien_tep('    if tk.get("chua_do"):\n        return RC_KHONG_DO_DUOC\n    return RC_VI_PHAM if loi else RC_SACH',
                             '    if loi:\n        return RC_VI_PHAM\n    return RC_KHONG_DO_DUOC if tk.get("chua_do") else RC_SACH'),
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
           "_HD, PROVIDER_NGUON_HONG = _provider_chinh_tac()",
           '_HD, PROVIDER_NGUON_HONG = ({"hop_dong": {"anthropic": {"be_mat": frozenset(), '
           '"van_chuyen": frozenset()}, "openai_codex": {"be_mat": frozenset({"codex_cli"}), '
           '"van_chuyen": frozenset()}}, "bi_danh": {}}, None)',
           bo_qua_parity=("PROVIDER_CHO_PHEP", "PROVIDER_HOP_DONG", "PROVIDER_BI_DANH")),
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
    # KHÔNG khai đối chứng, và đây là ca DUY NHẤT trong cụm mỏ neo cố ý bỏ nó: bỏ một bảng
    # nguồn làm hai nguồn LỆCH nhau, và "lệch ⇒ KHÔNG ĐO ĐƯỢC cả lượt" chính là HÀNH VI
    # ĐÚNG vừa thiết kế. Đòi đối chứng dương xanh ở đây là đòi bản vá đừng hoạt động.
    # Đột biến này làm `AGENTS.md` LỆCH bảng ⇒ nguồn thành "hỏng" ⇒ cả bốn hằng nguồn đổi;
    # khai ĐÍCH DANH cả bốn, không phải một cờ tắt hết (`R7-03`).
    do("m29_bo_mot_bang_nguon_phai_lam_HAI_NGUON_LECH",
       lambda: _dot_bien_tep("    for prov, be_mat, van_chuyen in ngoai:",
                             "    for prov, be_mat, van_chuyen in []:",
                             bo_qua_parity=("PROVIDER_CHO_PHEP", "PROVIDER_HOP_DONG",
                                            "PROVIDER_BI_DANH", "PROVIDER_NGUON_HONG")),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "bỏ một bảng nguồn KHÔNG được im lặng thu hẹp")
    do("m31_quet_TOAN_TEP_thay_vi_hai_bang",
       lambda: _dot_bien_tep(
           "    hop_dong = {}",
           '    hop_dong = {p: {"be_mat": {"forged"}, "van_chuyen": {"forged"}} for p in '
           're.findall(r"provider\\s+([a-z0-9_]+)\\s+qua\\s+execution_surface", van_launcher)}',
           # `launcher.py` thật CÓ hai chuỗi `vi_sao` khớp mẫu ấy (`openai_api`, `google_antigravity`),
           # nên trên cây thật đột biến này thêm bề mặt `forged` vào hợp đồng của hai provider —
           # tập TÊN không đổi nhưng `PROVIDER_HOP_DONG` đổi: khai đích danh.
           bo_qua_parity=("PROVIDER_CHO_PHEP", "PROVIDER_HOP_DONG")),
       "c35_KHONG_duoc_NOI_danh_sach_provider_bang_van_ban_tu_do",
       "một dòng chú thích lại cấp được quyền", doi_chung="c18_neo_git_DUNG_thi_qua")
    # --- vòng 7 (connector trên `670071b`): quyền đi kèm tên, và hai trường cùng nói một thứ
    do("m32_bo_gioi_han_assurance_theo_provider",
       lambda: _dot_bien_tep("    for m in ASSURANCE_CAM_THEO_PROVIDER.get(prov, frozenset()):",
                             "    for m in ():"),
       "c36_provider_KHONG_mang_theo_quyen_cua_provider_khac",
       "advisory biến thành bằng chứng có thẩm quyền", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m33_bo_kiem_BO_BA_provider_be_mat",
       lambda: _dot_bien_tep('        if be_mat not in hd["be_mat"]:', "        if False:"),
       "c36_provider_KHONG_mang_theo_quyen_cua_provider_khac",
       "`surface: banana` lại qua", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m34_bo_so_verdict_path_voi_duong_dan_trong_URL",
       lambda: _dot_bien_tep("    if khai_duong and khai_duong != duong:", "    if False:"),
       "c37_URL_phai_neo_DUNG_duong_dan_bien_nhan_khai",
       "mỏ neo trỏ một tệp KHÁC thứ nó khai", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m35_rc127_cua_rev_parse_duong_dan_thanh_TRO_HUT",
       lambda: _dot_bien_tep("    if rc == 127:\n        chua.append(f\"{ten}: KHÔNG ĐO ĐƯỢC đường dẫn",
                             "    if False:\n        chua.append(f\"{ten}: KHÔNG ĐO ĐƯỢC đường dẫn"),
       "c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC",
       "lỗi ĐO thành lời KẾT TỘI ở thao tác git thứ sáu",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m36_luat_chep_tay_MAT_NEO_van_giu_nguyen",
       lambda: _dot_bien_tep("        if cau not in van_luat[tep]:", "        if False:"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "giữ một luật có thể đã hết hiệu lực", doi_chung="c18_neo_git_DUNG_thi_qua")
    # --- vòng 5 launcher (`R5-01`/`R5-02`)
    do("m37_bang_transport_RONG_van_di_tiep",
       lambda: _dot_bien_tep("    if not hd:\n", "    if False:\n"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "nguồn 1 không fail-close như hai nguồn kia", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m38_khong_bat_loi_GIAI_MA_nguon",
       lambda: _dot_bien_tep("    except (OSError, UnicodeDecodeError) as ex:",
                             "    except OSError as ex:"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "cổng chết trước khi kịp phân ba trạng thái", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m39_nhet_execution_surface_vao_tap_provider",
       lambda: _dot_bien_tep(
           "        hop_dong[prov][\"be_mat\"].add(be_mat)\n"
           "        hop_dong[prov][\"van_chuyen\"].add(van_chuyen)\n"
           "    for prov, be_mat, van_chuyen in ngoai:",
           "        hop_dong[prov][\"be_mat\"].add(be_mat)\n"
           "        hop_dong[prov][\"van_chuyen\"].add(van_chuyen)\n"
           "        hop_dong.setdefault(be_mat, {\"be_mat\": set(), \"van_chuyen\": set()})\n"
           "    for prov, be_mat, van_chuyen in ngoai:",
           bo_qua_parity=("PROVIDER_CHO_PHEP", "PROVIDER_HOP_DONG")),
       "c31_hop_dong_provider_doc_DU_BA_NGUON_khong_chep_tay",
       "`R5-02`: nới danh sách bằng chính token trong nguồn",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m40_bi_danh_lich_su_KHONG_co_bien",
       lambda: _dot_bien_tep("    prov = _chuan_hoa_provider(prov)",
                             "    prov = prov"),
       "c38_BI_DANH_phai_duoc_CHUAN_HOA_truoc_moi_phep_kiem",
       "miễn trừ tương thích thành đường lách vĩnh viễn",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m41_bo_kiem_VAN_CHUYEN_trong_bo_ba",
       lambda: _dot_bien_tep('        vc = _chuoi(v.get("transport"))', "        vc = None"),
       "c36_provider_KHONG_mang_theo_quyen_cua_provider_khac",
       "bộ ba SAI SỰ THẬT vẫn qua", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m42_KHONG_hop_dong_van_co_tham_quyen",
       lambda: _dot_bien_tep("        for m in ASSURANCE_CAN_DOC_LAP:", "        for m in ():"),
       "c36_provider_KHONG_mang_theo_quyen_cua_provider_khac",
       "chưa khai hợp đồng mà vẫn cấp thẩm quyền", doi_chung="c18_neo_git_DUNG_thi_qua")
    # `R7-04`: bản trước của `m43` chỉ đổi chốt absolute/`..` thành `False` mà GIỮ normalizer mới,
    # nên `../../x` vẫn bị chốt so URL chặn — `c37` chết vì THÔNG BÁO khác, còn mô tả nói "đường
    # dẫn chuẩn hoá rồi lọt". Tín dụng đo sai thuộc tính (`R2-04` ở tầng khác). Nay mutant phục
    # hồi đúng lỗi gốc `.lstrip("./")`: reviewer trace được receipt `../../` thành **0 lỗi, 1
    # đạt** dưới nó, và `c37` phải chết ở assertion "được NHẬN" — không phải ở assertion lý do.
    do("m43_phuc_hoi_lstrip_bo_MOI_dau_cham_gach_cheo",
       lambda: _dot_bien_tep(
           '    khai_duong = str(d.get("verdict_path") or "").strip()\n'
           '    if khai_duong.startswith("./"):\n'
           '        khai_duong = khai_duong[2:]\n',
           '    khai_duong = str(d.get("verdict_path") or "").strip().lstrip("./")\n'),
       "c37_URL_phai_neo_DUNG_duong_dan_bien_nhan_khai",
       "`../../x` và `/x` chuẩn hoá về `x` rồi khớp URL — receipt sai được NHẬN",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # `R6-01` nêu đích danh hai phép làm yếu này: cả hai chỉ bớt MỘT PHẦN GIÁ TRỊ, nên ca
    # cũ (thử đúng giá trị fixture chọn) mù hoàn toàn.
    do("m44_chi_cam_MOT_muc_assurance",
       lambda: _dot_bien_tep("    for m in ASSURANCE_CAM_THEO_PROVIDER.get(prov, frozenset()):",
                             '    for m in ASSURANCE_CAM_THEO_PROVIDER.get(prov, frozenset()) '
                             '& {"cross_approved"}:'),
       "c36_provider_KHONG_mang_theo_quyen_cua_provider_khac",
       "mất cấm `same_provider_approved` và `human_audited`",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m45_chi_kiem_be_mat_cho_HAI_provider",
       lambda: _dot_bien_tep(
           "    hd = PROVIDER_HOP_DONG.get(prov)\n    if PROVIDER_NGUON_HONG is None and hd:",
           '    hd = PROVIDER_HOP_DONG.get(prov) if prov in ("openai_chatgpt", "openai_codex") else None\n'
           "    if PROVIDER_NGUON_HONG is None and hd:"),
       "c36_provider_KHONG_mang_theo_quyen_cua_provider_khac",
       "ba provider chính tắc khác mất kiểm bề mặt",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # --- lượt 7 (`gpt-6-astra`): R7-01 nguồn hỏng thành kết tội/crash · R7-02 human · R7-03 rig
    # R7-01 — ba chốt cấu trúc nguồn, mỗi cái một mutant RIÊNG (reviewer: "phải chết độc lập").
    do("m46_bo_kiem_arity_RIENG_bang_bi_danh_provider",
       lambda: _dot_bien_tep("            if len(hang) != len(cot):",
                             '            if len(hang) != len(cot) and ten != "_PROVIDER_BI_DANH":'),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "hàng thiếu cột lọt qua lược đồ rồi nổ `ValueError` lúc import (rc=1, traceback)",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m47_bo_kiem_arity_RIENG_bang_bi_danh_be_mat",
       lambda: _dot_bien_tep("            if len(hang) != len(cot):",
                             '            if len(hang) != len(cot) and ten != "_BE_MAT_BI_DANH":'),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "cùng lỗ ở bảng bí danh thứ hai — vá một bảng không phải vá lớp",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m48_bo_kiem_KIEU_o_chuoi_surface_transport",
       lambda: _dot_bien_tep("                    ok = isinstance(x, str) and bool(x) and x.strip() == x",
                             "                    ok = True"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "surface/transport `None` thành hợp đồng `[None]` ⇒ biên nhận nguyên byte bị KẾT TỘI",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m49_van_suy_KHONG_HOP_DONG_khi_nguon_hong",
       lambda: _dot_bien_tep("    if PROVIDER_NGUON_HONG is not None or not prov:", "    if not prov:"),
       "c40_R7_01_nguon_hong_tren_bien_nhan_THAT_khong_ket_toi_bien_nhan_nao",
       "11 biên nhận THẬT bị kết tội `KHÔNG có hợp đồng` khi thiếu launcher.py — đúng ca reviewer",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # R7-02 — phân vùng người/mô hình, ba mặt, mỗi mặt một mutant.
    do("m50_moi_provider_coi_la_MO_HINH_human_mat_human_audited",
       lambda: _dot_bien_tep("    la_nguoi = hd[\"van_chuyen\"] == {VAN_CHUYEN_NGUOI}",
                             "    la_nguoi = False"),
       "c41_human_audit_theo_PROTOCOL_8_QUA_va_muc_MO_HINH_cho_nguoi_bi_chan",
       "human trở lại bị cấm `human_audited` — ca DƯƠNG phải đỏ",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m51_cap_MOI_muc_cho_nguoi",
       lambda: _dot_bien_tep("        for m in ASSURANCE_CUA_MO_HINH:", "        for m in ():"),
       "c41_human_audit_theo_PROTOCOL_8_QUA_va_muc_MO_HINH_cho_nguoi_bi_chan",
       "human tự cấp `cross_approved`/`same_provider_approved` — ca ÂM phải đỏ",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m52_mo_hinh_khai_duoc_human_audited",
       lambda: _dot_bien_tep("        for m in ASSURANCE_CUA_NGUOI:", "        for m in ():"),
       "c41_human_audit_theo_PROTOCOL_8_QUA_va_muc_MO_HINH_cho_nguoi_bi_chan",
       "mặt thứ ba của cùng lớp: một mô hình lĩnh mức của người audit",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # R7-03 — hai phép làm yếu reviewer chạy qua toàn suite (A: bỏ đối chiếu SURFACE của AGENTS;
    # B: bỏ riêng chốt thiếu bảng bí danh BỀ MẶT), nay mỗi cái phải bị hàng riêng của `c28` bắt.
    do("m54_bo_doi_chieu_SURFACE_cua_AGENTS",
       lambda: _dot_bien_tep(
           "            if g and g.group(1) not in hop_dong[ten][khoa]:",
           '            if khoa == "be_mat":\n                g = None\n'
           "            if g and g.group(1) not in hop_dong[ten][khoa]:"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "phép A của reviewer: AGENTS khai bề mặt của provider khác mà vẫn 'khớp'",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m55_bo_RIENG_chot_thieu_bang_bi_danh_be_mat",
       lambda: _dot_bien_tep("    if loi_bm:\n        return {}, loi_bm", "    if False:\n        return {}, loi_bm"),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "phép B của reviewer: mất bảng bí danh bề mặt ⇒ `None` đi vào vòng unpack",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # `R8-01` — HAI phép làm yếu reviewer chạy SỐNG SÓT qua toàn suite (`45/45 · 57/57 · 2/2`,
    # rc=0, `TỔNG: ĐẠT`): mỗi cái bỏ ĐÚNG MỘT neo luật. Chúng sống được vì hàng PROTOCOL cũ của
    # `c28` xoá CẢ HAI câu cùng lúc, nên luật còn lại vẫn làm hàng ấy đỏ. Nay mỗi neo có lượt
    # riêng và mỗi mutant phải chết ở ĐÚNG thuộc tính: thông báo nêu tên luật CỦA NÓ.
    _VONG_NEO = "    for luat, tep, cau in _NEO_LUAT_CHEP_TAY:"
    do("m56_bo_RIENG_chot_neo_ASSURANCE_CUA_NGUOI",
       lambda: _dot_bien_tep(_VONG_NEO,
                             _VONG_NEO + '\n        if luat == "ASSURANCE_CUA_NGUOI":\n            continue'),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "mất neo `human_audited` của PROTOCOL §8 mà cổng vẫn nhận nguồn",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m57_bo_RIENG_chot_neo_ASSURANCE_CUA_MO_HINH",
       lambda: _dot_bien_tep(_VONG_NEO,
                             _VONG_NEO + '\n        if luat == "ASSURANCE_CUA_MO_HINH":\n            continue'),
       "c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA",
       "mất neo `cross_approved` của PROTOCOL §8 mà cổng vẫn nhận nguồn",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # …và lối làm yếu THỨ HAI của cùng chốt: bỏ một MỤC khỏi bảng neo. Fixture bản trước lấy
    # danh sách neo TỪ bảng ấy nên nó co theo và `c28` vẫn xanh; oracle chép tay bắt được.
    do("m58_bo_MOT_MUC_khoi_bang_neo_cua_san_pham",
       lambda: _dot_bien_tep(
           '    ("ASSURANCE_CUA_NGUOI", "docs/PROTOCOL_DA_PHIEN.md",\n'
           '     "`human_audited`: người audit có danh tính bền trên GitHub"),\n', ""),
       "c43_bang_neo_luat_cua_san_pham_phai_khop_ORACLE_chep_tay",
       "bảng neo CO LẠI trong im lặng — oracle chép tay không được co theo",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # `R8-04`/`R8-05` — cross-review lượt 8 bổ sung (codex, trên `c0f18ac`).
    # `m59` là bản vá QUAY NGƯỢC NGUYÊN VĂN: gộp lại "vắng" với "có mà hỏng". Đột biến `if False`
    # KHÔNG dùng được ở đây và đó là bài học riêng: dưới nó `vc=None` rơi xuống chốt hợp đồng
    # (`None not in {...}` ⇒ True) nên giá trị VẪN bị chặn, chỉ khác thông báo — `c34` vẫn xanh và
    # đột biến lĩnh "không răng" OAN. Phải đột biến về đúng HÌNH DẠNG cũ mới đo được.
    _TRANSPORT_MOI = ('        if "transport" in v:\n'
                      '            vc = _chuoi(v.get("transport"))\n'
                      '            if vc is None:\n'
                      '                return (f"`model_reviewer_identity.transport`={v.get(\'transport\')!r} CÓ MẶT nhưng "\n'
                      '                        f"không phải chuỗi không rỗng — VẮNG khác CÓ-MÀ-HỎNG, im lặng không phải "\n'
                      '                        f"lời khai")\n'
                      '            if vc not in hd["van_chuyen"]:')
    _TRANSPORT_CU = ('        vc = _chuoi(v.get("transport"))\n'
                     '        if vc and vc not in hd["van_chuyen"]:')
    do("m59_transport_gop_VANG_voi_CO_MA_HONG",
       lambda: _dot_bien_tep(_TRANSPORT_MOI, _TRANSPORT_CU),
       "c34_MOI_truong_attestation_phai_la_CHUOI_khong_chi_truthy",
       "`{fake:1}` `[..]` `7` `True` `''` lọt LẶNG y như vắng mặt — chỉ chuỗi-sai bị bắt",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m60_bo_HAN_chot_hop_dong_van_chuyen",
       lambda: _dot_bien_tep('            if vc not in hd["van_chuyen"]:', "            if False:"),
       "c44_bo_ba_provider_phai_KHOP_nguon_ke_hoach_va_hang_LECH_phai_doi_hanh_vi",
       "hàng launcher thôi QUYẾT ĐỊNH gì — witness đối xứng của `c44` mất vế TỪ CHỐI",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # `R9-F02` — reviewer lượt 9: bỏ RIÊNG chặn null vẫn qua TOÀN suite (`48/48 · 62/62`, rc=0),
    # vì `None` chưa có trong ma trận kiểu. Đột biến coi `transport: null` là "vắng mặt" — đúng
    # hình dạng lỗ, không phải một `if False` tiện tay.
    do("m61_transport_null_bi_coi_la_VANG_MAT",
       lambda: _dot_bien_tep('        if "transport" in v:',
                             '        if v.get("transport") is not None:'),
       "c34_MOI_truong_attestation_phai_la_CHUOI_khong_chi_truthy",
       "`transport: null` lọt vì bị gộp vào nhánh VẮNG — hành vi đã công bố mà không ai canh",
       doi_chung="c18_neo_git_DUNG_thi_qua")
    # M7 / A6 — các chốt họ model và mức bằng chứng cho cross_approved
    do("m62_bo_chot_cung_ho_model", lambda: _dot_bien_tep("            if ho_rev and ho_exec and ho_rev == ho_exec:", "            if False:"),
       "c49_cross_approved_cung_ho_model_phai_bi_tu_choi", "gỡ chốt cùng họ model", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m63_bo_chot_thieu_nguoi_audit", lambda: _dot_bien_tep('                elif bc == "khai_co_audit":', '                elif False and bc == "khai_co_audit":'),
       "c50_cross_approved_khai_co_audit_thieu_nguoi_audit_phai_bi_tu_choi", "gỡ chốt thiếu audit", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m64_bo_chot_thieu_ho_executor", lambda: _dot_bien_tep("            if not ho_exec:", "            if False:"),
       "c52_cross_approved_thieu_executor_phai_bi_tu_choi", "gỡ chốt thiếu executor", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m65_bo_chot_antigravity_khong_khai_model", lambda: _dot_bien_tep('    "anthropic_claude": "claude",', '    "google_antigravity": "gemini", "anthropic_claude": "claude",', bo_qua_parity=("HO_MODEL_MAC_DINH",)),
       "c53_cross_approved_antigravity_khong_khai_model_phai_bi_tu_choi", "antigravity ngầm định gemini", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m66_noi_bang_nhan_dien_model_la", lambda: _dot_bien_tep('    if "gemini" in t and "gemini" in HO_MODEL_CHO_PHEP:\n        return "gemini"\n    return ""', '    if "gemini" in t and "gemini" in HO_MODEL_CHO_PHEP:\n        return "gemini"\n    return t'),
       "c54_cross_approved_model_la_phai_bi_tu_choi", "nới nhận diện model lạ", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m67_bo_chot_muc_bang_chung_la", lambda: _dot_bien_tep("                elif bc and bc not in MUC_BANG_CHUNG_MODEL:", "                elif False:"),
       "c55_cross_approved_muc_bang_chung_la_phai_bi_tu_choi", "gỡ chốt mức lạ", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m68_bo_chot_khong_do_duoc", lambda: _dot_bien_tep('                elif bc == "khong_do_duoc":', "                elif False:"),
       "c56_cross_approved_khong_do_duoc_phai_bi_tu_choi", "gỡ chốt khong_do_duoc", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m69_bo_chot_do_may_thieu_ref", lambda: _dot_bien_tep('                elif bc == "do_may":', "                elif False:"),
       "c57_cross_approved_do_may_thieu_ref_phai_bi_tu_choi", "gỡ chốt do_may thiếu ref", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m70_bo_chot_executor_khai_de_thieu_evidence", lambda: _dot_bien_tep("                if ov and not bc:", "                if False:"),
       "c59_cross_approved_executor_khai_de_thieu_evidence_phai_bi_tu_choi", "gỡ chốt khai đè thiếu evidence", doi_chung="c18_neo_git_DUNG_thi_qua")
    do("m71_xoa_gemini_khoi_ho_model_cho_phep", lambda: _dot_bien_tep('HO_MODEL_CHO_PHEP = frozenset({"claude", "gpt", "gemini"})', 'HO_MODEL_CHO_PHEP = frozenset({"claude", "gpt"})', bo_qua_parity=("HO_MODEL_CHO_PHEP",)),
       "c61_ho_model_cho_phep_phai_quyet_dinh_nhan_dien", "xoá gemini khỏi HO_MODEL_CHO_PHEP", doi_chung="c18_neo_git_DUNG_thi_qua")
    # `M17`/`A18` — đột biến TRẢ `pre` VỀ ÁP CHO CẢ `sub`, tức đúng hành vi cũ sinh ra `P2`.
    # Nó phải làm ĐÚNG `c62` đỏ và phải phân hạng `giet_that`; chết vì một lỗi khác là TÍN DỤNG GIẢ.
    do("m72_tra_tien_to_ve_ap_cho_ca_sub", lambda: _dot_bien_tep(
        'return sub, ((sub, ""), (d, f"{vai}_" if vai == "executor" else ""))',
        'return sub, ((sub, f"{vai}_" if vai == "executor" else ""), (d, f"{vai}_" if vai == "executor" else ""))'),
       "c62_khoi_model_executor_identity_phai_doi_xung_voi_khoi_reviewer",
       "áp lại tiền tố vai cho khoá tra BÊN TRONG khối model_<vai>_identity", doi_chung="c18_neo_git_DUNG_thi_qua")

    # R7-03 — TỰ KIỂM RIG: reviewer bơm mất hàng `_BE_MAT_BI_DANH` vào RIÊNG bản launcher mà rig
    # chép (qua `shutil.copyfile`), bốn hằng parity cũ vẫn bằng nhau. Nay rig phải bắt được điều
    # đó TRƯỚC khi ca đích chạy và phân nó là GIÀN GIÁO, không phải "có răng" hay "không răng".
    def _rig_lam_hong_nguon_phu():
        that = shutil.copyfile

        def _chep_hong(src, dst, *a, **kw):
            r = that(src, dst, *a, **kw)
            if Path(dst).name == "launcher.py":
                p = Path(dst)
                p.write_bytes(p.read_bytes().replace(b"_BE_MAT_BI_DANH = (",
                                                     b"_BE_MAT_BI_DANH = ()\n_KHAC3 = (", 1))
            return r

        shutil.copyfile = _chep_hong
        try:
            _dot_bien_tep("    if khai_duong and khai_duong != duong:", "    if False:")
        finally:
            shutil.copyfile = that

    do("m53_TU_KIEM_rig_lam_hong_nguon_phu_phai_bi_phan_GIAN_GIAO", _rig_lam_hong_nguon_phu,
       "c37_URL_phai_neo_DUNG_duong_dan_bien_nhan_khai",
       "PHẢI hiện gian_giao — lệch do rig không được đội lốt đột biến", mong_gian_giao=True)
    do("m10_bo_kiem_actor_cua_submitter",
       lambda: setattr(bnv2, "_gsi", lambda d: None if "github_submitter_identity" in d
                       else "thiếu khoá `github_submitter_identity`"),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am", "R2-03 số 1: vòng 1 mù với nhánh này")
    do("m11_MRI_khong_phai_dict_van_qua",
       lambda: setattr(bnv2, "_mri", lambda d: None if not isinstance(
           d.get("model_reviewer_identity"), dict) else _mri_that(d)),
       "c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am", "R2-03 số 2: nhánh không-phải-dict")
    # --- #960 câu lịch sử (A1–A5 + bánh cóc M4): mỗi chốt một đột biến, giết ĐÚNG ca đích.
    DC = "c18_neo_git_DUNG_thi_qua"
    do("m73_cau_review_bo_so_reviewed_sha", lambda: _dot_bien_tep(
        "sau = [(t, lu) for t, lu in da_review.get(h, ()) if t != ten]", "sau = []"),
       "c69_A1_cau_chua_review_ma_luot_sau_DA_review_dung_SHA", "A1: bỏ phép so `reviewed_sha`", doi_chung=DC)
    do("m74_cau_review_so_tien_to_7", lambda: _dot_bien_tep(
        "sau = [(t, lu) for t, lu in da_review.get(h, ()) if t != ten]",
        "sau = [(t, lu) for k_, v_ in da_review.items() if k_[:7] == h[:7] for t, lu in v_ if t != ten]"),
       "c69_A1_cau_chua_review_ma_luot_sau_DA_review_dung_SHA", "A1: so tiền tố 7 ký tự", doi_chung=DC)
    do("m75_cau_review_luot_thieu_thanh_0", lambda: _dot_bien_tep(
        "        luot_nay = _luot(d)\n", "        luot_nay = _luot(d) or 0\n"),
       "c70_A1_luot_KHONG_so_duoc_la_KHONG_DO_DUOC", "`luot` thiếu bị đọc thành 0", doi_chung=DC)
    do("m76_ancestry_oid_thieu_la_khong_to_tien", lambda: _dot_bien_tep(
        "                            if c is None and not _oid_bat_buoc(cau, mo):\n",
        "                            if c is None:\n                                continue\n"
        "                            if c is None and not _oid_bat_buoc(cau, mo):\n"),
       "c71_A2_cau_ancestry_do_bang_merge_base", "A2: OID không tra được coi là 'không tổ tiên'", doi_chung=DC)
    do("m78_cau_khop_theo_tung_dong", lambda: _dot_bien_tep(
        'return [c for c in _RE_CAU.split(" ".join(van.split())) if c]',
        "return [c for dong in van.splitlines() for c in _RE_CAU.split(dong) if c]"),
       "c72_A3_bien_the_co_dau_khong_dau_xuong_dong_deu_bi_nhan", "A3: khớp từng dòng, không trên scalar đã nối",
       doi_chung=DC)
    do("m79_cau_khong_bo_dau", lambda: _dot_bien_tep(
        "                chuan = _bo_dau(cau)\n", "                chuan = cau.lower()\n"),
       "c72_A3_bien_the_co_dau_khong_dau_xuong_dong_deu_bi_nhan", "A3: biến thể có dấu không được chuẩn hoá",
       doi_chung=DC)
    do("m80_surface_luon_coi_khac", lambda: _dot_bien_tep(
        "        if tu and tu != s_that:\n", "        if tu:\n"),
       "c73_A4_surface_verdict_doi_chieu_run_json", "A4: bỏ phép đọc run.json (luôn coi khác)", doi_chung=DC)
    do("m81_bo_chot_no_chet", lambda: _dot_bien_tep(
        "        if k[0] in tep_doc and k[0] not in tep_hong and k not in vp_cau and k not in chua_cau:\n",
        "        if False:\n"),
       "c74_A5_no_cau_lich_su_chi_co_va_no_chet_la_vi_pham", "A5: nợ chết không bị bắt", doi_chung=DC)
    do("m82_no_cau_lich_su_NO_them_muc", lambda: _dot_bien_tep(
        "NO_CAU_LICH_SU: frozenset = frozenset({\n",
        'NO_CAU_LICH_SU: frozenset = frozenset({\n    ("tep-moi.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),\n',
        bo_qua_parity=("NO_CAU_LICH_SU",)),
       "c75_no_cau_lich_su_CHI_CO_LAI_va_tro_tep_co_that", "M4: danh sách nợ nở thêm", doi_chung=DC)
    # --- connector PR #976 + codex CLI lượt 1 (r1); neo lại theo thân hàm r2.
    do("m83_run_json_hong_thanh_khong_ap", lambda: _dot_bien_tep(
        "            if not s_that:\n                chua[k_sf]",
        "            if not s_that:\n                sf_chua.append(rj)\n                continue\n                chua[k_sf]"),
       "c77_run_json_CO_ma_HONG_la_KHONG_DO_DUOC_khong_phai_no_chet", "run.json hỏng đọc thành 'không áp'",
       doi_chung=DC)
    do("m84_bo_OID_toan_chu_so", lambda: _dot_bien_tep(
        "                            try:\n                                c = _tra(x)\n",
        "                            if not _oid_tron(x):\n                                continue\n"
        "                            try:\n                                c = _tra(x)\n"),
       "c78_OID_viet_tat_TOAN_CHU_SO_van_duoc_tra", "loại token toàn chữ số trước khi tra", doi_chung=DC)
    do("m88_bo_chot_alias_vong", lambda: _dot_bien_tep(
        '        if id(node) in _dang:\n            raise _AliasVong(duong or "<gốc>")\n', ""),
       "c82_alias_VONG_la_KHONG_DO_DUOC_alias_dung_lai_van_duyet", "alias vòng chết bằng RecursionError",
       doi_chung=DC)
    do("m89_chi_xet_khai_bao_dau_tren_dong", lambda: _dot_bien_tep(
        "        ms = list(_RE_DONG_SURFACE.finditer(dong))\n",
        "        ms = list(_RE_DONG_SURFACE.finditer(dong))[:1]\n"),
       "c83_MOI_khai_bao_surface_tren_cung_dong_deu_duoc_xet", "chỉ khai báo đầu tiên trên dòng", doi_chung=DC)
    do("m91_luot_bien_nhan_khac_thieu", lambda: _dot_bien_tep(
        "if luot_nay is None or any(lu is None for _, lu in sau):", "if luot_nay is None:"),
       "c70_A1_luot_KHONG_so_duoc_la_KHONG_DO_DUOC", "r2: `luot` thiếu ở biên nhận khác", doi_chung=DC)
    do("m92_merge_base_loi_thanh_vi_pham", lambda: _dot_bien_tep(
        '                                chua.setdefault(k, f"{ten}: `{duong}` — `merge-base` cho `{x}`: {ex}")\n'
        '                                continue\n',
        '                                rc = 0\n'),
       "c84_merge_base_HONG_la_KHONG_DO_DUOC_khong_phai_vi_pham", "r3: merge-base hỏng thành vi phạm", doi_chung=DC)
    # --- r2 B1–B4 (`ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`): mỗi chốt mới một đột biến.
    do("m94_B1_chen_lai_mien_tru_dung_tai", lambda: _dot_bien_tep(
        "            for duong, node, cha in scalar:\n",
        "            for duong, node, cha in scalar:\n"
        "                if cha is not None and any(getattr(kk, 'value', None) == 'dung_tai' for kk, _ in cha.value):\n"
        "                    continue\n"),
       "c86_B1_moc_dung_tai_KHONG_con_mien", "B1: chèn lại phép miễn khi mapping có `dung_tai`", doi_chung=DC)
    do("m95_B2_bam_receipt_ngoai_bien", lambda: _dot_bien_tep(
        '        except (UnicodeDecodeError, OSError) as ex:\n            raise KhongDoDuoc(f"{ten}: không đọc được',
        '        except UnicodeDecodeError as ex:\n            raise KhongDoDuoc(f"{ten}: không đọc được'),
       "c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback", "B2: lỗi I/O khi băm/đọc receipt thoát biên",
       doi_chung=DC)
    do("m96_B2_go_bien_loi_do", lambda: _dot_bien_tep(
        '        except Exception as ex:                                  # noqa: BLE001\n            chua[(ten, "*", "*")]',
        '        except ZeroDivisionError as ex:\n            chua[(ten, "*", "*")]'),
       "c90_B2_MOT_BIEN_loi_do_khong_traceback_khong_no_chet", "B2: gỡ biên lỗi đo của ba luật", doi_chung=DC)
    do("m97_B2_tep_hong_van_ket_luan_no_chet", lambda: _dot_bien_tep(
        " and k[0] not in tep_hong and ", " and "),
       "c90_B2_MOT_BIEN_loi_do_khong_traceback_khong_no_chet", "B2: tệp đo hỏng mà nợ vẫn bị kết luận chết",
       doi_chung=DC)
    do("m98_B3_bo_ngu_canh_backtick", lambda: _dot_bien_tep(
        '    if truoc.endswith("`") and sau.startswith("`"):\n        return True\n', ""),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "B3: bỏ ngữ cảnh backtick", doi_chung=DC)
    do("m99_B3_bo_ngu_canh_40_hex", lambda: _dot_bien_tep(
        "    if len(x) == 40 or _oid_tron(x):\n", "    if _oid_tron(x):\n"),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "B3: bỏ ngữ cảnh đủ 40 hex", doi_chung=DC)
    do("m100_B3_bo_ngu_canh_sau_commit", lambda: _dot_bien_tep(
        "    return _RE_SAU_COMMIT.search(truoc) is not None\n", "    return False\n"),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "B3: bỏ ngữ cảnh sau từ `commit`", doi_chung=DC)
    do("m101_B3_moi_token_thuan_la_bat_buoc", lambda: _dot_bien_tep(
        "    x = m.group(0)\n    if len(x) == 40 or _oid_tron(x):\n", "    x = m.group(0)\n    if True:\n"),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "B3: mọi token thuần thành bắt buộc (`deadbeef` rc=2)",
       doi_chung=DC)
    do("m102_B4_bo_dieu_kien_provider", lambda: _dot_bien_tep(
        "not any(_RE_PROVIDER.search(x) for x in cua) or ", ""),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "B4: khai báo không `provider` thành tự khai",
       doi_chung=DC)
    do("m85_B4_bo_dieu_kien_trich_dan", lambda: _dot_bien_tep(
        " or any(_RE_TRICH_DAN.search(x) for x in cua)", ""),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "B4: dòng có trích dẫn kề thành tự khai",
       doi_chung=DC)
    # --- review r2 lượt 1: mỗi đường vào của lỗi đo + mỗi ranh giới bộ chọn một đột biến riêng.
    C91 = "c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no"
    do("m103_git_khong_goi_duoc_thanh_rong", lambda: _dot_bien_tep(
        '        raise KhongDoDuoc(f"không gọi được `git {args[0]}`: {type(ex).__name__}: {ex}") from ex\n',
        '        return subprocess.CompletedProcess(args, 0, "", "")\n'),
       C91, "git vắng/hỏng đọc thành stdout rỗng", doi_chung=DC)
    do("m104_ref_mac_dinh_khong_phai_commit_lui_ref_ke", lambda: _dot_bien_tep(
        '            if lo != "commit":\n                raise KhongDoDuoc(f"ref mặc định',
        '            if lo != "commit":\n                continue\n                raise KhongDoDuoc(f"ref mặc định'),
       C91, "`origin/master` là tree mà lùi về `master` cục bộ", doi_chung=DC)
    do("m105_tien_to_mo_ho_thanh_mot", lambda: _dot_bien_tep(
        "    if len(commit) > 1:\n", "    if False:\n"),
       C91, "tiền tố trỏ hai commit đọc thành một", doi_chung=DC)
    do("m106_run_json_thu_muc_thanh_vang", lambda: _dot_bien_tep(
        "or _vang(p_rj):", "or not p_rj.is_file():"),
       C91, "run.json là thư mục bị coi như vắng (không áp)", doi_chung=DC)
    do("m107_bo_bat_UTF8_khi_doc_receipt", lambda: _dot_bien_tep(
        '        except (UnicodeDecodeError, OSError) as ex:\n            raise KhongDoDuoc(f"{ten}: không đọc được',
        '        except OSError as ex:\n            raise KhongDoDuoc(f"{ten}: không đọc được'),
       C91, "byte UTF-8 hỏng trong receipt thoát biên", doi_chung=DC)
    do("m108_sinh_no_ngoai_bien_CLI", lambda: _dot_bien_tep(
        "    try:\n        # Hai cờ sinh nợ đi qua CÙNG biên với cổng",
        "    if a.sinh_no:\n        return _sinh_no(root)\n    try:\n        # Hai cờ sinh nợ đi qua CÙNG biên với cổng"),
       "c92_B2_co_SINH_NO_cung_bien_voi_cong", "`--sinh-no` gọi ngoài biên CLI", doi_chung=DC)
    do("m109_sinh_no_khong_doi_loi_doc", lambda: _dot_bien_tep(
        "        except Exception as ex:                                  # noqa: BLE001 — như `kiem`",
        "        except (OSError, UnicodeDecodeError, yaml.YAMLError) as ex:  # noqa: BLE001 — như `kiem`"),
       "c92_B2_co_SINH_NO_cung_bien_voi_cong", "`_sinh_no` không đổi lỗi đọc thành KHÔNG ĐO ĐƯỢC", doi_chung=DC)
    do("m110_B3_bo_ranh_gioi_tu_commit", lambda: _dot_bien_tep(
        'r"\\bcommit\\s*\\Z"', 'r"commit\\s*\\Z"'),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "B3: `Precommit` thành ngữ cảnh commit", doi_chung=DC)
    do("m111_B3_backtick_chi_can_mo", lambda: _dot_bien_tep(
        '    if truoc.endswith("`") and sau.startswith("`"):\n', '    if truoc.endswith("`"):\n'),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "B3: backtick chỉ mở thành ngữ cảnh", doi_chung=DC)
    do("m112_B4_bo_ranh_gioi_tu_provider", lambda: _dot_bien_tep(
        'r"\\bprovider\\b"', 'r"provider"'),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "B4: `notprovider` thành `provider`",
       doi_chung=DC)
    do("m113_B4_cua_so_bo_dong_sau", lambda: _dot_bien_tep(
        "        cua = dong_tep[max(0, j - 1):j + 2]\n", "        cua = dong_tep[max(0, j - 1):j + 1]\n"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "B4: cửa sổ bỏ dòng sau", doi_chung=DC)
    # --- review r2 lượt 2 + kiến trúc tra git (stderr rỗng mới tin): mỗi chốt một đột biến.
    do("m114_bo_qua_STDERR_cua_git", lambda: _dot_bien_tep(
        "    if con:\n        raise KhongDoDuoc(", "    if False:\n        raise KhongDoDuoc("),
       C91, "tin kết quả git dù stderr báo ref/object hỏng", doi_chung=DC)
    do("m115_vang_dung_stat_khong_lstat", lambda: _dot_bien_tep(
        "        p.lstat()\n", "        p.stat()\n"),
       C91, "symlink gãy của run.json bị coi như vắng", doi_chung=DC)
    do("m116_vang_loi_stat_khac_thanh_vang", lambda: _dot_bien_tep(
        "    except OSError:\n        return False\n    return False\n", "    except OSError:\n        return True\n    return False\n"),
       C91, "lỗi lstat khác ENOENT/ENOTDIR bị coi như vắng", doi_chung=DC)
    do("m117_bo_chot_kho_NONG", lambda: _dot_bien_tep(
        '    if nong != "false":\n', "    if False:\n"),
       C91, "kho nông vẫn đo tổ tiên", doi_chung=DC)
    do("m118_bo_chot_kho_PARTIAL", lambda: _dot_bien_tep(
        '    if _git_do(root, "config", "--get", "extensions.partialclone", sach=(0, 1))[1].strip():\n',
        "    if False:\n"),
       C91, "kho partial clone vẫn đo", doi_chung=DC)
    do("m119_bo_chot_SYMREF_gay", lambda: _dot_bien_tep(
        "        if rc == 0 and ref not in co:\n", "        if False:\n"),
       C91, "symref `origin/HEAD` gãy bị coi như vắng", doi_chung=DC)
    do("m120_tinh_MOI_loai_object_la_ung_vien", lambda: _dot_bien_tep(
        '    commit = sorted(x for x, lo in loai.items() if lo == "commit")\n',
        "    commit = sorted(loai)\n"),
       "c93_ung_vien_CHI_TINH_COMMIT_blob_chung_tien_to_khong_mo_ho", "blob chung tiền tố đẩy commit thành mơ hồ",
       doi_chung=DC)
    C94 = "c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC"
    do("m121_disambiguate_loc_bo_dong_la", lambda: _dot_bien_tep(
        '    if len(loai) != len(ung) or "missing" in loai.values():\n',
        '    if "missing" in loai.values():\n'),
       C94, "dòng lạ của `--disambiguate` bị lọc bỏ", doi_chung=DC)
    do("m122_ung_vien_missing_thanh_khong_phai_commit", lambda: _dot_bien_tep(
        '    if len(loai) != len(ung) or "missing" in loai.values():\n',
        "    if len(loai) != len(ung):\n"),
       C94, "ứng viên được liệt kê mà `missing` bị coi là không phải commit", doi_chung=DC)
    do("m123_batch_check_dang_la_thanh_khac", lambda: _dot_bien_tep(
        '    if len(ra) != 2 or ra[0] != oid40 or ra[1] not in ("commit", "tag", "tree", "blob"):\n',
        "    if len(ra) < 2:\n"),
       C94, "dòng lạ của `cat-file --batch-check` được tin", doi_chung=DC)
    do("m124_for_each_ref_dong_la_duoc_tin", lambda: _dot_bien_tep(
        "        if len(t) != 3 or t[0] not in _REF_MAC_DINH or not _HEX40.match(t[1]):\n",
        "        if len(t) != 3:\n"),
       C94, "dòng lạ của `for-each-ref` được tin", doi_chung=DC)
    # --- review r2 lượt 3 (nhóm A): môi trường cô lập, stderr nền, partial/grafts, ref con, chốt rc.
    C95 = "c95_moi_truong_git_KHONG_doi_ket_qua_do"
    do("m125_bo_chot_RC_cua_git", lambda: _dot_bien_tep(
        "    if p.returncode not in sach:\n        raise KhongDoDuoc(", "    if False:\n        raise KhongDoDuoc("),
       "c96_git_rc_LA_ma_stderr_RONG_van_la_KHONG_DO_DUOC", "rc lạ mà stderr rỗng được tin", doi_chung=DC)
    do("m126_ke_thua_bien_GIT", lambda: _dot_bien_tep(
        'if not k.startswith("GIT_") or k in _GIT_GIU}', "if True}"),
       C95, "biến `GIT_*` kế thừa (GIT_DIR, GIT_TRACE) lọt vào phép đo", doi_chung=DC)
    do("m127_khong_tat_replace", lambda: _dot_bien_tep(
        '"GIT_NO_REPLACE_OBJECTS": "1"', '"GIT_NO_REPLACE_OBJECTS_TAT": "1"'),
       C95, "replace ref che quan hệ tổ tiên", doi_chung=DC)
    do("m129_bo_chot_PROMISOR", lambda: _dot_bien_tep(
        '        if gt == "true":                    # `false`/`no`/`off`', '        if False:                    # `false`/`no`/`off`'),
       C91, "partial clone thật (promisor) vẫn đo", doi_chung=DC)
    do("m132_promisor_TAT_van_la_partial", lambda: _dot_bien_tep(
        '        if gt == "true":                    # `false`/`no`/`off`', '        if gt:                    # `false`/`no`/`off`'),
       C95, "`remote.<x>.promisor=false` bị coi là partial clone", doi_chung=DC)
    do("m133_bo_alternates_khoi_danh_sach_giu", lambda: _dot_bien_tep(
        '_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH"})', '_GIT_GIU = frozenset({"GIT_EXEC_PATH"})'),
       C95, "bỏ `GIT_ALTERNATE_OBJECT_DIRECTORIES` làm kho đủ mất object", doi_chung=DC)
    # --- review r2 lượt 5: răng riêng cho hai chốt promisor và fixture GIT_DIR phân biệt được kho.
    do("m134_doc_promisor_khong_chuan_hoa_bool", lambda: _dot_bien_tep(
        '"config", "--type=bool", "--get-regexp"', '"config", "--get-regexp"'),
       C95, "`off`/`no` đọc thô thành dòng lạ ⇒ kho đủ bị chặn", doi_chung=DC)
    do("m135_bo_chot_gia_tri_promisor_la", lambda: _dot_bien_tep(
        '        if gt not in ("true", "false"):\n', "        if False:\n"),
       C94, "giá trị promisor không phải bool được coi là tắt", doi_chung=DC)
    do("m136_giu_GIT_DIR_ke_thua", lambda: _dot_bien_tep(
        '_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH"})',
        '_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH", "GIT_DIR"})'),
       C95, "`GIT_DIR` kế thừa làm cổng đo kho khác", doi_chung=DC)
    # Review r2 lượt 6: từng vế giao thức và từng ngữ cảnh phải có răng riêng.
    do("m137_bo_so_OID_batch_check", lambda: _dot_bien_tep(
        ' or ra[0] != oid40', ''),
       C94, "batch-check trả OID khác mà được tin", doi_chung=DC)
    do("m138_bo_kiem_loai_batch_check", lambda: _dot_bien_tep(
        ' or ra[1] not in ("commit", "tag", "tree", "blob")', ''),
       C94, "batch-check trả loại ngoài giao thức mà được tin", doi_chung=DC)
    do("m139_bo_ngu_canh_tron_so_chu", lambda: _dot_bien_tep(
        'if len(x) == 40 or _oid_tron(x):', 'if len(x) == 40:'),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "OID trộn số-chữ thiếu mà thành token thường", doi_chung=DC)
    # Cửa sổ M4 đúng ba dòng, không được nới thêm về phía trước hoặc phía sau.
    do("m140_B4_noi_cua_so_ve_truoc", lambda: _dot_bien_tep(
        "cua = dong_tep[max(0, j - 1):j + 2]", "cua = dong_tep[max(0, j - 2):j + 2]"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "provider/citation cách hai dòng là ngoài cửa sổ", doi_chung=DC)
    do("m141_B4_noi_cua_so_ve_sau", lambda: _dot_bien_tep(
        "cua = dong_tep[max(0, j - 1):j + 2]", "cua = dong_tep[max(0, j - 1):j + 3]"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "provider/citation cách hai dòng là ngoài cửa sổ", doi_chung=DC)
    # #1021 Codex lượt 5: biên đầu tệp và trích dẫn dòng sau — hai đột biến ấy từng SỐNG qua toàn suite.
    do("m156_B4_bo_chan_bien_dau_tep", lambda: _dot_bien_tep(
        "        cua = dong_tep[max(0, j - 1):j + 2]\n",
        "        max = lambda lower, value: value\n        cua = dong_tep[max(0, j - 1):j + 2]\n"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "dòng đầu bị mất cửa sổ", doi_chung=DC)
    do("m157_B4_trich_dan_bo_dong_sau", lambda: _dot_bien_tep(
        "_RE_TRICH_DAN.search(x) for x in cua",
        "_RE_TRICH_DAN.search(x) for x in (cua[:-1] if j + 1 < len(dong_tep) else cua)"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "trích dẫn ở dòng sau bị bỏ qua", doi_chung=DC)
    do("m130_bo_chot_GRAFTS", lambda: _dot_bien_tep(
        "    if gf and (root / gf", "    if False and (root / gf"),
       C91, "tệp grafts đổi parent mà vẫn đo", doi_chung=DC)
    do("m131_ref_con_tien_to_la_dong_la", lambda: _dot_bien_tep(
        "            continue        # `for-each-ref` khớp theo TIỀN TỐ", "            pass        # `for-each-ref` khớp theo TIỀN TỐ"),
       C95, "ref con `origin/HEAD/topic` làm hỏng phép chọn nhánh mặc định", doi_chung=DC)
    # --- #1021: bộ chọn biên nhận. Hoàn nguyên về `glob` KHÔNG vào bảng này: nó chỉ đỏ trên POSIX
    # (glob Windows vốn không phân biệt hoa thường) nên sẽ SỐNG trên Windows và làm cổng Windows đỏ —
    # đo một lần trên bản sao tạm, ghi ở PR (spec r2 C3).
    do("m142_chon_bien_nhan_so_duoi_CHINH_XAC", lambda: _dot_bien_tep(
        'if p.name.lower().endswith(".receipt.yaml")]', 'if p.name.endswith(".receipt.yaml")]'),
       "c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen", "đuôi hoa lại bị bỏ qua lặng", doi_chung=DC)
    do("m143_chon_bien_nhan_loc_is_file", lambda: _dot_bien_tep(
        "ds = [p for p in tm.iterdir() if p.name", "ds = [p for p in tm.iterdir() if p.is_file() and p.name"),
       "c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback", "thư mục `*.receipt.yaml` trốn khỏi phép băm", doi_chung=DC)
    # Codex lượt 1 (#1021): ba đột biến từng SỐNG qua toàn suite + hồi quy lỗi liệt kê — mỗi cái một chốt của `c99`.
    C99 = "c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE"
    do("m144_sinh_no_loc_duoi_CHINH_XAC", lambda: _dot_bien_tep(
        "    for p in _chon_bien_nhan(tm):\n        if p.name in ALLOWLIST_CUTOVER:",
        "    for p in _chon_bien_nhan(tm):\n        if not p.name.endswith(\".receipt.yaml\") or p.name in ALLOWLIST_CUTOVER:"),
       C99, "`--sinh-no` bỏ qua đuôi hoa (đường gọi thứ hai)", doi_chung=DC)
    do("m145_bo_chon_khong_sap_xep", lambda: _dot_bien_tep("    return sorted(ds)\n", "    return ds\n"),
       C99, "thứ tự duyệt theo hệ tệp, không sắp xếp", doi_chung=DC)
    do("m146_bo_chon_bo_nhanh_thu_muc_vang", lambda: _dot_bien_tep(
        "    if not _hoi_trang_thai(tm.is_dir, tm):\n        return []\n    try:", "    try:"),
       C99, "`--sinh-no` trên kho thiếu ops/reviews thành lỗi đo", doi_chung=DC)
    do("m147_bo_chon_bo_bat_OSError", lambda: _dot_bien_tep(
        "    except OSError as ex:\n        raise KhongDoDuoc(f\"không liệt kê được",
        "    except ZeroDivisionError as ex:\n        raise KhongDoDuoc(f\"không liệt kê được"),
       C99, "lỗi liệt kê thoát thành traceback (Codex lượt 1)", doi_chung=DC)
    # Codex lượt 2 (#1021): lỗi `stat` trước liệt kê + lỗi lập trình phải đi thẳng — chốt của `c100`.
    C100 = "c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang"
    do("m148_bo_chon_hoi_is_dir_TRAN", lambda: _dot_bien_tep(
        "    if not _hoi_trang_thai(tm.is_dir, tm):\n        return []", "    if not tm.is_dir():\n        return []"),
       C100, "`--sinh-no`: EACCES ở `stat` thoát thành traceback", doi_chung=DC)
    do("m149_kiem_guard_hoi_is_dir_TRAN", lambda: _dot_bien_tep(
        "    if not _hoi_trang_thai(tm.is_dir, tm):                      # #1021",
        "    if not tm.is_dir():                      # #1021"),
       C100, "`kiem`: EACCES ở `stat` thoát thành traceback", doi_chung=DC)
    do("m150_hoi_trang_thai_bo_bat_OSError", lambda: _dot_bien_tep(
        "    except OSError as ex:\n        raise KhongDoDuoc(f\"không đọc được trạng thái",
        "    except ZeroDivisionError as ex:\n        raise KhongDoDuoc(f\"không đọc được trạng thái"),
       C100, "lỗi `stat` thoát thành traceback ở cả hai đường", doi_chung=DC)
    do("m151_kiem_hoi_git_TRAN", lambda: _dot_bien_tep(
        "        if _hoi_trang_thai((root / \".git\").exists, root / \".git\"):",
        "        if (root / \".git\").exists():"),
       C100, "`stat` của `.git` thoát thành traceback", doi_chung=DC)
    do("m152_bo_chon_bat_Exception", lambda: _dot_bien_tep(
        "    except OSError as ex:\n        raise KhongDoDuoc(f\"không liệt kê được",
        "    except Exception as ex:\n        raise KhongDoDuoc(f\"không liệt kê được"),
       C100, "lỗi lập trình ở phép liệt kê bị đổi thành KHÔNG ĐO ĐƯỢC", doi_chung=DC)
    do("m153_hoi_trang_thai_bat_Exception", lambda: _dot_bien_tep(
        "    except OSError as ex:\n        raise KhongDoDuoc(f\"không đọc được trạng thái",
        "    except Exception as ex:\n        raise KhongDoDuoc(f\"không đọc được trạng thái"),
       C100, "lỗi lập trình ở phép hỏi thư mục bị đổi thành KHÔNG ĐO ĐƯỢC", doi_chung=DC)
    # Codex lượt 3 (#1021): thu hẹp phép bắt về `PermissionError` — EIO phải vẫn ra rc=2.
    do("m154_hoi_trang_thai_chi_bat_PermissionError", lambda: _dot_bien_tep(
        "    except OSError as ex:\n        raise KhongDoDuoc(f\"không đọc được trạng thái",
        "    except PermissionError as ex:\n        raise KhongDoDuoc(f\"không đọc được trạng thái"),
       C100, "EIO ở `stat` thoát thành traceback", doi_chung=DC)
    do("m155_bo_chon_chi_bat_PermissionError", lambda: _dot_bien_tep(
        "    except OSError as ex:\n        raise KhongDoDuoc(f\"không liệt kê được",
        "    except PermissionError as ex:\n        raise KhongDoDuoc(f\"không liệt kê được"),
       C99, "EIO khi liệt kê thoát thành traceback", doi_chung=DC)
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
