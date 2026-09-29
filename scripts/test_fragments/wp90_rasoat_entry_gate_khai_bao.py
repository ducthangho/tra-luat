# -*- coding: utf-8 -*-
"""LỚP 2 — khoá KHAI BÁO cổng vào rà soát hồ sơ (khuôn r210_loop_khong_ghi_trong_cay).

LINT thuần: chứng minh cổng `RASOAT_ENTRY_GATE_v1` (a) được nhắc trên LUỒNG CHÍNH của kernel — TRƯỚC
`## 1. KHỞI ĐỘNG`, không phải trong bảng tham chiếu cuối file — và (b) có khối máy đọc đủ khoá trong
`references/RASOAT_HOSO_LOOP.md`, kèm `TRA_KHO_LOG_v1`. KHÔNG chạy vòng rà nào: vế CHẠY thuộc cổng máy
`rasoat-dot-check` (LỚP 3).
"""

import json
import re
from pathlib import Path

TEST_ID = "wp90_rasoat_entry_gate_khai_bao"

_GATE = "RASOAT_ENTRY_GATE_v1"
_KHOA_GATE = ("tien_kiem:", "doc_state:", "truoc:", "chan_dung:", "chan_lan_ghi:",
              "dot_tuan_tu:", "nap_giua_chung:", "tra_kho_3_khoa:", "dem_nfc:")
_KHOA_LOG = ("truong_bat_buoc:", "ket_qua:", "ket_luan_thieu_hop_le:", "so_file:")
_LENH_CONG = "rasoat-dot-check"


def _block(text: str, name: str) -> str:
    m = re.search(r"<!--\s*" + re.escape(name) + r"\b(.*?)-->", text, re.S)
    return m.group(1) if m else ""


def _kernel_ok(skill_md: str) -> bool:
    """Cổng phải nằm TRƯỚC mục `## 1. KHỞI ĐỘNG` (luồng chính), và phải là bất biến §0 có đánh số."""
    head = skill_md.split("## 1. KHỞI ĐỘNG", 1)[0]
    return (_GATE in head
            and "CỔNG VÀO RÀ SOÁT HỒ SƠ" in head
            and re.search(r"^20\. \*\*CỔNG VÀO RÀ SOÁT HỒ SƠ", head, re.M) is not None)


def _the_ok(card: dict) -> bool:
    """F1 (cross-review P1) — cổng LỚP 3 phải nằm TRÊN ĐƯỜNG ĐI MẶC ĐỊNH, không chỉ tồn tại.

    Bản đầu có đủ lệnh + đủ tài liệu mà thẻ `rasoat_hoso` KHÔNG nhắc nó ở `recommended_commands`
    lẫn `verify`, và §1bis đóng Đợt được với 4 vế không vế nào gọi nó ⇒ cổng không gác gì. Đó đúng
    khuyết tật mà LỚP 2 sinh ra để chữa, tái phát ngay bên trong bản vá của chính nó."""
    return (any(_LENH_CONG in str(c) for c in (card.get("recommended_commands") or []))
            and any(_LENH_CONG in str(v) for v in (card.get("verify") or [])))


def _dong_dot_ok(loop_md: str) -> bool:
    """Điều kiện đóng Đợt phải ĐẾM cả cổng máy — 4 vế lời khai + 1 vế phép ĐO."""
    return ("đủ cả 5" in loop_md
            and re.search(r"^5\. \*\*CỔNG MÁY CUỐI ĐỢT", loop_md, re.M) is not None
            and _LENH_CONG in loop_md)


def _dong_bo_dong_han_che(loop_md: str, card: dict) -> bool:
    """Văn xuôi và thẻ MÁY-ĐỌC phải nói CÙNG một luật đóng.

    Vá lượt trước sửa văn xuôi (rc≠0 chặn `da_dong` nhưng vẫn cho `da_dong_co_gioi_han` kèm khai
    giới hạn) mà QUÊN thẻ — thẻ vẫn đòi rc=0 cho CẢ HAI đường. Agent đọc thẻ và người đọc văn xuôi
    khi ấy nhận hai luật khác nhau, và không ai biết vì mỗi bên tự nhất quán.

    ★ BẢN ĐẦU CỦA CHÍNH HÀM NÀY KHÔNG CÓ RĂNG, và đột biến của tôi cũng sai chỗ nên không lộ ra:
    nó dò TOKEN rải rác (`da_dong_co_gioi_han`, `gioi_han_da_biet`) trên văn bản ĐÃ NỐI, mà bản
    mâu thuẫn CŨ cũng chứa đủ hai token ấy ở những câu KHÁC nhau ⇒ hoàn nguyên bản vá vẫn XANH.
    Đột biến tôi dựng lại XOÁ HẲN token — một hình dạng hỏng KHÁC với hình dạng thật. Nay neo vào
    MỆNH ĐỀ chỉ tồn tại ở bản đã sửa, ở CẢ hai phía; hoàn nguyên là ĐỎ."""
    ĐO = ("CHAN dong BINH THUONG", "KHONG triet tieu duong dong HAN CHE")
    _v = " ".join(str(x) for x in (card.get("verify") or [])
                  + (card.get("stop_conditions") or []) if _LENH_CONG in str(x))
    return (all(x in _v for x in ĐO)
            and "gioi_han_da_biet" in _v
            and "chặn ĐÓNG BÌNH THƯỜNG (`da_dong`)" in loop_md
            and "KHÔNG triệt tiêu đường" in loop_md
            and "đóng HẠN CHẾ" in loop_md)


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
    card = json.loads((root / "references" / "workflows" / "rasoat_hoso.json").read_text(encoding="utf-8"))
    if not (_kernel_ok(skill) and _loop_ok(loop) and _the_ok(card) and _dong_dot_ok(loop)
            and _dong_bo_dong_han_che(loop, card)):
        return False
    # PHẢN CHỨNG (phép đo phải phân biệt được):
    #  1. cổng chỉ nằm ở bảng tham chiếu cuối kernel  → ĐỎ
    #  2. khối máy đọc thiếu một khoá                 → ĐỎ
    #  3. sổ tra kho không được khai trong WRITE_PATHS→ ĐỎ
    #  4. gỡ cổng khỏi `recommended_commands` HOẶC khỏi `verify` của thẻ → ĐỎ (F1)
    #  5. hạ điều kiện đóng Đợt về 4 vế → ĐỎ (F1)
    doi_cho = skill.replace("20. **CỔNG VÀO RÀ SOÁT HỒ SƠ", "zz. **cong vao ra soat ho so")
    thieu_khoa = loop.replace("dem_nfc:", "xx_dem_nfc_da_bo:")
    mat_so = loop.replace("<out-dir>/rasoat_tra_kho.jsonl\n", "")
    bo_rec = dict(card, recommended_commands=[c for c in card["recommended_commands"]
                                              if _LENH_CONG not in str(c)])
    bo_verify = dict(card, verify=[v for v in card["verify"] if _LENH_CONG not in str(v)])
    ha_ve = loop.replace("đủ cả 5", "đủ cả 4").replace("5. **CỔNG MÁY CUỐI ĐỢT", "x. cong may cuoi dot")
    #  6. thẻ nói luật đóng KHÁC văn xuôi → ĐỎ (chống "vá một chỗ, quên chỗ kia")
    # PHẢN CHỨNG phải là BẢN MÂU THUẪN THẬT, không phải bản xoá token. Bản cũ vẫn CHỨA đủ token
    # `da_dong_co_gioi_han`/`gioi_han_da_biet` ở những câu rời — chính vì thế phép dò token cũ mù
    # với nó, còn đột biến "xoá token" thì lại giết được. Hình dạng hỏng THẬT là: thẻ đòi rc=0 cho
    # CẢ HAI đường đóng, trong khi văn xuôi cho đóng hạn chế.
    _cau_cu = ("DONG DOT: `rasoat-dot-check --in <out-dir> --dot <dot_id> --strict` rc=0 TRUOC khi "
               "chot dot.trang_thai=da_dong hoac da_dong_co_gioi_han; rc=1/2 CHAN dong Dot")
    the_cu = dict(card,
                  verify=[_cau_cu if _LENH_CONG in v else v for v in card["verify"]],
                  stop_conditions=[_cau_cu if _LENH_CONG in v else v
                                   for v in (card.get("stop_conditions") or [])])
    loop_cu = (loop.replace("chặn ĐÓNG BÌNH THƯỜNG (`da_dong`)", "CHẶN đóng Đợt")
                   .replace("KHÔNG triệt tiêu đường", "và triệt tiêu đường"))
    return ((not _kernel_ok(doi_cho)) and (not _loop_ok(thieu_khoa)) and (not _loop_ok(mat_so))
            and (not _the_ok(bo_rec)) and (not _the_ok(bo_verify)) and (not _dong_dot_ok(ha_ve))
            and (not _dong_bo_dong_han_che(loop, the_cu))       # thẻ cũ mâu thuẫn ⇒ ĐỎ
            and (not _dong_bo_dong_han_che(loop_cu, card)))     # văn xuôi cũ mâu thuẫn ⇒ ĐỎ
