# -*- coding: utf-8 -*-
"""LỚP 2 — khoá KHAI BÁO cổng vào rà soát hồ sơ (khuôn r210_loop_khong_ghi_trong_cay).

LINT thuần: chứng minh cổng `RASOAT_ENTRY_GATE_v1` (a) được nhắc trên LUỒNG CHÍNH của kernel — TRƯỚC
`## 1. KHỞI ĐỘNG`, không phải trong bảng tham chiếu cuối file — và (b) có khối máy đọc đủ khoá trong
`references/RASOAT_HOSO_LOOP.md`, kèm `TRA_KHO_LOG_v1`. KHÔNG chạy vòng rà nào: vế CHẠY thuộc cổng máy
`rasoat-dot-check` (LỚP 3).
"""

import re
from pathlib import Path

TEST_ID = "wp90_rasoat_entry_gate_khai_bao"

_GATE = "RASOAT_ENTRY_GATE_v1"
_KHOA_GATE = ("tien_kiem:", "doc_state:", "truoc:", "chan_dung:", "chan_lan_ghi:",
              "dot_tuan_tu:", "nap_giua_chung:", "tra_kho_3_khoa:", "dem_nfc:")
_KHOA_LOG = ("truong_bat_buoc:", "ket_qua:", "ket_luan_thieu_hop_le:", "so_file:")


def _block(text: str, name: str) -> str:
    m = re.search(r"<!--\s*" + re.escape(name) + r"\b(.*?)-->", text, re.S)
    return m.group(1) if m else ""


def _kernel_ok(skill_md: str) -> bool:
    """Cổng phải nằm TRƯỚC mục `## 1. KHỞI ĐỘNG` (luồng chính), và phải là bất biến §0 có đánh số."""
    head = skill_md.split("## 1. KHỞI ĐỘNG", 1)[0]
    return (_GATE in head
            and "CỔNG VÀO RÀ SOÁT HỒ SƠ" in head
            and re.search(r"^20\. \*\*CỔNG VÀO RÀ SOÁT HỒ SƠ", head, re.M) is not None)


def _loop_ok(loop_md: str) -> bool:
    gate = _block(loop_md, _GATE)
    log = _block(loop_md, "TRA_KHO_LOG_v1")
    return (all(k in gate for k in _KHOA_GATE)
            and all(k in log for k in _KHOA_LOG)
            and "§3bis" in loop_md
            and "§1bis" in loop_md
            and "rasoat_tra_kho.jsonl" in _block(loop_md, "WRITE_PATHS_v1"))


def run(tl_module):  # noqa: ARG001 — lint thuần, không cần tl
    root = Path(__file__).resolve().parents[2]
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    loop = (root / "references" / "RASOAT_HOSO_LOOP.md").read_text(encoding="utf-8")
    if not (_kernel_ok(skill) and _loop_ok(loop)):
        return False
    # PHẢN CHỨNG (phép đo phải phân biệt được):
    #  1. cổng chỉ nằm ở bảng tham chiếu cuối kernel  → ĐỎ
    #  2. khối máy đọc thiếu một khoá                 → ĐỎ
    #  3. sổ tra kho không được khai trong WRITE_PATHS→ ĐỎ
    doi_cho = skill.replace("20. **CỔNG VÀO RÀ SOÁT HỒ SƠ", "zz. **cong vao ra soat ho so")
    thieu_khoa = loop.replace("dem_nfc:", "xx_dem_nfc_da_bo:")
    mat_so = loop.replace("<out-dir>/rasoat_tra_kho.jsonl\n", "")
    return (not _kernel_ok(doi_cho)) and (not _loop_ok(thieu_khoa)) and (not _loop_ok(mat_so))
