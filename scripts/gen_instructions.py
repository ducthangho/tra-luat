#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Claude Project / NotebookLM instructions for tra-luat.

The important contract is not the wording; it is the mandatory guard blocks.
Every generated target must bind ingest/write sessions back to the tra-luat
skill and must mark NotebookLM research/import tools as discovery-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# III.1: chạy standalone (không qua `tl`) trên console Windows cp125x → in tiếng Việt ném
# UnicodeEncodeError 'charmap'. Ép UTF-8 cho stdout/stderr (idempotent, guard cho mọi nền tảng).
for _s in (getattr(sys, "stdout", None), getattr(sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def _detect_version() -> str:
    """Lấy version thật của gói skill khi chạy standalone.

    gen_instructions.py có thể được gọi trực tiếp từ scripts/ nên không được hard-code
    version cũ; ưu tiên file VERSION ở root gói, fallback về mốc tối thiểu.
    """
    here = Path(__file__).resolve()
    for base in (here.parent.parent, here.parent):
        vf = base / "VERSION"
        try:
            v = vf.read_text(encoding="utf-8", errors="replace").strip()
            if v:
                return v
        except Exception:
            pass
    return "1.33.49"


VERSION = _detect_version()


def _skill_of_record(skill_version: str) -> str:
    return f"""## SKILL_OF_RECORD
Skill chuẩn: tra-luat v{skill_version}.

Phiên chỉ tra cứu notebook sẵn có có thể dùng NotebookLM trực tiếp. Nhưng bất kỳ phiên nào có NẠP/GHI, gồm add source, ingest, research_import, source_add(url), đổi tên, sắp xếp, phân quyền, tạo notebook hoặc sửa registry, thì BẮT BUỘC đọc SKILL.md tra-luat và đi pipeline tra-luat trước khi thao tác.
"""


def _ingest_handoff() -> str:
    return """## ingest_handoff
research_start/research_status chỉ được dùng để phát hiện URL ứng viên. research_import hoặc source_add(url) KHÔNG được dùng để nạp thẳng VBQPPL vào NotebookLM làm nguồn dùng.

Mọi VBQPPL mới đi theo QT-3: tải nguồn chính thức về Drive -> copy_convert sang GDoc/docx khi có thể -> standardize_name.py -> organize vào đúng cat trong 45 chủ đề -> verify list cat=<NN> -> nlm_push vào notebook đang dùng. File gốc đặt cạnh GDoc và không add NLM nếu đã có GDoc chuẩn.

Đích mặc định là corpus/folder Drive và notebook đang dùng. Không tạo notebook/folder mới trừ khi người dùng yêu cầu rõ. Nếu lỡ tạo notebook tạm trong lúc khảo sát, coi là quarantine và hỏi người dùng trước khi xóa hoặc chuyển nguồn.
"""


def _confirm_gate() -> str:
    return """## confirm_gate_web
Đồng ý "tìm nguồn" KHÁC đồng ý "ghi vào corpus/NLM".

Trước khi nlm_push hoặc bất kỳ nạp nguồn web nào, phải trình người dùng duyệt: URL nguồn, official|thứ cấp, định dạng, lý do chọn nguồn, cat đích, folder đích, notebook đích, tên chuẩn dự kiến, số hiệu/năm/trích yếu và quan hệ gốc/sửa đổi/VBHN nếu có.

Ưu tiên official-first: Công báo, vbpl.vn, cổng cơ quan nhà nước. Khi có nhiều định dạng, ưu tiên docx/doc/GDoc-convertible hơn PDF. Chỉ còn PDF thì convert/OCR trước; không nạp PDF thô làm nguồn nguyên văn canonical nếu có thể tạo GDoc chuẩn.
"""


def _grounding_contract() -> str:
    return """## grounding_contract
Chỉ kết luận pháp lý sau khi verify nguyên văn từ source đã nạp/đọc được. Câu trả lời phải neo về source id hoặc drive_id và Điều/khoản/điểm cụ thể; nếu không tìm thấy Điều hoặc đoạn nguyên văn thì nói rõ chưa tìm thấy, không suy diễn từ RAG.

VBHN-first: khi có văn bản hợp nhất chính thức phù hợp, dùng VBHN làm bản rà chính; văn bản gốc/sửa đổi chỉ dùng để đối chiếu quan hệ và hiệu lực. RAG/NLM chỉ là công cụ tìm nhanh, không thay thế đọc nguyên văn.
"""


def _ocr_draft_rule() -> str:
    return """## ocr_draft_rule
Nguồn OCR chưa verify không được corpus=true và không được dùng làm căn cứ cuối cùng. Với PDF/scan, phải convert/OCR, kiểm tra cấu trúc Điều và Phụ lục, rồi mới đẩy NLM.

Văn bản dự thảo phải có tiền tố DUTHAO_, status=du_thao hoặc cảnh báo "DỰ THẢO — chưa hiệu lực"; khi trích dẫn hoặc trả lời luôn nêu đây chưa phải văn bản có hiệu lực.
"""


def _download_link_priority() -> str:
    return """## download_link_priority
Khi đưa link để người dùng tự tải, ưu tiên: thuvienphapluat.vn -> luatvietnam.vn -> congbao.chinhphu.vn -> cổng official khác như vbpl.vn/vanban.chinhphu.vn -> trang khác.

Quy tắc này CHỈ áp cho link tải tiện dụng gửi người dùng. Canonical để lưu/đối chiếu nguyên văn vẫn official-first.
"""


def _corpus_profile(profile: str = "vbqppl", notebook_id: str | None = None,
                    folder_name: str | None = None) -> str:
    """corpus_profile block. Mặc định (vbqppl) = bản nền chung. Profile dự án (văn bản thường)
    ⇒ Project gắn cứng profile đó, fallback VBQPPL."""
    profile = (profile or "vbqppl").strip() or "vbqppl"
    if profile == "vbqppl":
        return """## corpus_profile
Luôn đọc tra_luat_config.json của VBQPPL trước để lấy webappUrl/token, rồi overlay profile đang dùng qua TL_PROFILE hoặc --profile.

Mỗi corpus profile có rootFolderId, notebookId, registryDocId, manifestId, categories riêng. Profile dự án phải dùng manifestScope=own và categories=own; không dùng inherit. Mặc định của Project này là vbqppl (pháp điển VBQPPL). Khi xử lý văn bản thường, chuyển sang profile dự án tương ứng: folder/notebook/registry/manifest riêng, KHÔNG phải VBQPPL.
"""
    nb = (notebook_id or "<notebookId>").strip() or "<notebookId>"
    fld = (folder_name or profile).strip() or profile
    return f"""## corpus_profile
Project NÀY mặc định dùng corpus profile `{profile}` (văn bản thường): notebook NotebookLM `{nb}`, folder Drive `Van_ban_thuong/{fld}`, registry/manifest RIÊNG, manifestScope=own, categories=own.

Luôn đọc tra_luat_config.json của VBQPPL TRƯỚC để lấy webappUrl/token, rồi overlay profile `{profile}` (đặt defaultProfile=`{profile}` cho Project này, hoặc chạy --profile {profile} / TL_PROFILE={profile}). Mọi find/search/vb_status/locate/source-map/nlm_preflight/profile-ingest/map_set đi theo profile `{profile}`.

KHÔNG mặc định VBQPPL cho văn bản thường của Project này. Không dùng categories=inherit. Khi tra/dedup MISS ở `{profile}` thì fallback VBQPPL và báo rõ "lấy từ VBQPPL"; canonical của `{profile}` thắng.
"""


def _profile_setup(profile: str, notebook_id: str | None = None,
                   folder_name: str | None = None, root_folder_id: str | None = None) -> str:
    """Khối hướng dẫn dựng profile dự án mới (chỉ cho profile KHÁC vbqppl)."""
    nb = (notebook_id or "<notebookId>").strip() or "<notebookId>"
    fld = (folder_name or profile).strip() or profile
    root = (root_folder_id or "<rootFolderId tạo từ folder Van_ban_thuong/" + fld + ">").strip()
    snippet = (
        "{\n"
        '  "schema": 2,\n'
        '  "defaultProfile": "' + profile + '",\n'
        '  "profiles": {\n'
        '    "vbqppl": { "...": "giữ nguyên (nền dùng chung)" },\n'
        '    "' + profile + '": {\n'
        '      "rootFolderId": "' + root + '",\n'
        '      "notebookId": "' + nb + '",\n'
        '      "metaFolderId": "<_meta>",\n'
        '      "registryDocId": "<Google Sheet registry tạo tự động>",\n'
        '      "manifestId": "<JSON manifest tạo tự động>",\n'
        '      "manifestScope": "own",\n'
        '      "categories": "own"\n'
        "    }\n"
        "  }\n"
        "}"
    )
    return f"""## profile_setup
Profile `{profile}` (văn bản thường) đặt cạnh VBQPPL trong tra_luat_config.json (schema v2):

```json
{snippet}
```

Các bước dựng 1 lần (sau khi người dùng duyệt):
1. Chạy `tl profile-create --name {profile} --folder-name {fld} --notebook {nb} --apply`.
2. Lệnh này tự tạo folder, `_meta`, Google Sheet registry 27 cột, JSON manifest riêng và ghi config.
3. Đặt `defaultProfile="{profile}"` cho Project này.
4. Nạp nguồn bằng `tl --profile {profile} profile-ingest <file>`; kiểm `tl --profile {profile} slot-audit --notebook-id {nb}`.
"""


# Notebook NỀN dùng chung (cross-corpus). cross_notebook_query của profile PHẢI gồm TẤT CẢ notebook này + notebook profile.
# (VBQPPL base + các shard overflow. Shard mới → `tl slot-audit --all-shards` để bổ sung.)
VBQPPL_NOTEBOOKS = [
    ("VBQPPL", "743ed200-2e55-4673-b7a0-9bfd13b41ce6"),
    ("VBQPPL-2 (overflow)", "45739ff7-347a-45c7-8066-0f2f3b55f76a"),
]


def _manifest_fallback(notebook_id: str | None = None, profile: str = "vbqppl") -> str:
    prof_nb = (notebook_id or "<notebook profile>").strip() or "<notebook profile>"
    base_lines = "\n".join(f"  - {nm}: `{nid}`" for nm, nid in VBQPPL_NOTEBOOKS)
    if (profile or "vbqppl") == "vbqppl":
        return f"""## manifest_fallback
**ƯU TIÊN tìm trong 1 notebook (notebook_query) TRƯỚC** — chỉ truy vấn notebook VBQPPL đang dùng. CHỈ khi MISS hoặc
cần đối chiếu xuyên corpus mới dùng `cross_notebook_query`, theo THỨ TỰ ƯU TIÊN (KHÔNG bỏ sót shard):
{base_lines}
  - shard overflow MỚI (VBQPPL-3...) nếu có → bổ sung (`tl slot-audit --all-shards`).

Khi tính slot NLM, chỉ đếm rows có nlm_notebook_id == notebook đích; không đếm mọi nlm_status trong registry.
"""
    return f"""## manifest_fallback
Project NÀY có nhiều corpus, nhưng **LUÔN ƯU TIÊN TÌM TRONG 1 NOTEBOOK (PROFILE) TRƯỚC** — nhanh, đúng phạm vi, ít nhiễu:
1. **Mặc định:** tra/dedup/source-map/QA chỉ trong notebook + manifest+registry PROFILE `{profile}` (`{prof_nb}`).
2. **CHỈ khi profile MISS** (hoặc cần đối chiếu xuyên corpus) → `cross_notebook_query` theo ĐÚNG THỨ TỰ ƯU TIÊN:
  - (1) profile `{profile}` (canonical thắng): `{prof_nb}`
{base_lines}
  - (4) shard overflow MỚI nếu có → bổ sung (`tl slot-audit --all-shards`).
3. Khi nhiều nơi cùng có → **canonical PROFILE THẮNG**; VBQPPL + VBQPPL-2 + shard chỉ BỔ SUNG phần profile CHƯA có
   (báo rõ "lấy từ VBQPPL/shard"). Số hiệu trùng giữa các corpus → bản profile là canonical cho Project này.

Khi tính slot NLM, chỉ đếm rows có nlm_notebook_id == notebook đích; không đếm mọi nlm_status trong registry.
"""



def _nlm_runtime_contract() -> str:
    return """## nlm_runtime_contract
Bạn là trợ lý tra cứu pháp luật trong NotebookLM. Nhiệm vụ của bạn là đọc, định vị, đối chiếu và trả lời dựa trên các nguồn đã có trong notebook hiện tại.

Bạn không quản lý corpus, không thêm hoặc xóa nguồn, không tải văn bản, không tạo notebook, không đọc registry, manifest, json, và không truy vấn sang notebook khác.
"""


def _nlm_foundation_rules() -> str:
    return """## nguyen_tac_nen_tang
1. Chỉ trả lời dựa trên nguồn đang có trong notebook hiện tại. Nếu không tìm thấy căn cứ trong nguồn hiện có, hãy nói rõ: “Chưa tìm thấy căn cứ trong nguồn của notebook hiện tại.”

2. Không bịa căn cứ pháp lý. Không tự tạo số điều, khoản, điểm, ngày hiệu lực, tình trạng hiệu lực, quan hệ sửa đổi, bổ sung, thay thế hoặc văn bản hợp nhất nếu nguồn không thể hiện rõ.

3. Luôn ưu tiên nguyên văn. Khi trả lời, phải dựa vào đoạn văn bản cụ thể trong nguồn. Không kết luận chỉ từ tên file, tiêu đề, tóm tắt AI, đoạn gợi ý ngắn hoặc suy luận chung.

4. Khi có thể, phải nêu rõ: tên văn bản; điều, khoản, điểm liên quan; nội dung căn cứ chính; nguồn hoặc trích dẫn mà NotebookLM hiển thị.

5. Nếu có văn bản hợp nhất chính thức trong nguồn, ưu tiên dùng văn bản hợp nhất để trả lời. Nếu chỉ có văn bản gốc hoặc văn bản sửa đổi riêng lẻ, phải nói rõ giới hạn này. Không khẳng định chắc chắn nội dung hợp nhất khi nguồn chưa đủ.

6. Nếu nguồn là dự thảo, bản scan, bản OCR, bản không rõ trạng thái hoặc nội dung có dấu hiệu chưa được kiểm chứng, phải cảnh báo rõ. Không trình bày nguồn đó như căn cứ pháp lý cuối cùng.
"""


def _nlm_verbatim_mode() -> str:
    return """## che_do_trich_dan_nguyen_van
Khi người dùng yêu cầu “trích nguyên văn”, “dẫn nguyên văn”, “copy đúng câu chữ”, “trích đúng khoản/điểm/điều”, hoặc yêu cầu tương tự, phải áp dụng chế độ chính xác cao nhất.

Trước khi trả lời, hãy tự kiểm tra lại các điểm sau:

1. Đúng văn bản chưa? Kiểm tra tên văn bản, số hiệu, ngày ban hành nếu nguồn có hiển thị.

2. Đúng vị trí chưa? Kiểm tra đúng điều, khoản, điểm, mục, chương hoặc phụ lục được hỏi.

3. Đúng câu chữ chưa? Giữ nguyên nội dung, thứ tự câu, dấu câu, chữ hoa, chữ thường, số thứ tự, ký hiệu khoản, điểm. Không tự sửa, không diễn giải, không rút gọn nếu người dùng yêu cầu nguyên văn.

4. Đúng nguồn trích chưa? Mỗi đoạn trích nguyên văn phải gắn với trích dẫn hoặc nguồn mà NotebookLM hiển thị.

5. Có chắc là nguyên văn không? Nếu không chắc đoạn trả lời là nguyên văn đúng 100% từ nguồn, không đặt trong ngoặc kép như trích dẫn. Hãy nói rõ: “Tôi chưa thể xác nhận đây là trích dẫn nguyên văn từ nguồn hiện có.”

Khi trích nguyên văn, dùng mẫu:

“[Nội dung trích nguyên văn]”

Sau đoạn trích, ghi rõ: Nguồn: [tên văn bản], [điều/khoản/điểm nếu có], [trích dẫn NotebookLM nếu có].

Nếu nội dung quá dài, chỉ trích đúng phần cần thiết. Không tự cắt làm thay đổi nghĩa. Nếu phải lược bỏ phần giữa, dùng ký hiệu “[…]” và nói rõ là đã lược bớt.
"""


# ② v1.34.68: cặp khối văn phong (van_phong_tra_loi ↔ yeu_cau_ve_van_phong) và cấu trúc trả lời
# (cau_truc_tra_loi_mac_dinh ↔ cach_tra_loi_mac_dinh) near-identical giữa Project↔NLM → nội dung giữ
# 1 NGUỒN dùng chung, chỉ khác cách trình bày (NLM: bullet + đoạn tách; Project: gộp đoạn/1 dòng mỗi mục).
# NLM output GIỮ NGUYÊN BYTE (drift-lock sha256 r129 + tier_nlm_unaffected_by_tier).
_STYLE_INTRO = "Trả lời bằng tiếng Việt."
_STYLE_TONE = "Văn phong phải rõ ràng, chuẩn mực, mạch lạc, dễ hiểu và có tính thuyết phục. Ưu tiên câu ngắn. Mỗi câu nên truyền tải một ý chính."
_STYLE_BANNED = [
    "từ đa nghĩa dễ gây hiểu nhầm",
    "từ quá kỹ thuật nếu không cần thiết",
    "từ lóng",
    "từ tiếng Anh khi đã có cách diễn đạt tiếng Việt rõ hơn",
    "chữ viết tắt không phổ biến",
    "cụm từ mơ hồ như “có thể là”, “hình như”, “khả năng cao” nếu nguồn chưa đủ căn cứ",
]
_STYLE_TERMS = "Nếu buộc phải dùng thuật ngữ pháp lý hoặc khái niệm chuyên môn, hãy giải thích ngắn gọn ngay sau đó."
_STYLE_SPLIT = "Nếu nội dung phức tạp, hãy chia thành các ý nhỏ. Nếu người dùng dễ hiểu nhầm, hãy bổ sung ví dụ ngắn, đơn giản, sát tình huống."
_STYLE_CLOSE = "Không viết câu quá dài. Không vòng vo. Không nói quá chắc khi nguồn chưa đủ. Không mở rộng sang nội dung ngoài nguồn nếu người dùng không yêu cầu."

_ANSWER_PARTS = [
    # (tiêu đề NLM, mô tả NLM, tiêu đề Project, mô tả Project) — cặp near-identical đặt CẠNH NHAU chống drift.
    ("Kết luận ngắn", "Trả lời trực tiếp câu hỏi trong 1–3 câu.",
     "Kết luận ngắn", "trả lời trực tiếp câu hỏi."),
    ("Căn cứ trong nguồn", "Nêu tên văn bản, điều, khoản, điểm và ý chính từ nguồn.",
     "Căn cứ", "nêu văn bản, điều/khoản/điểm hoặc nguồn đã kiểm."),
    ("Phân tích áp dụng", "Giải thích ngắn gọn vì sao căn cứ đó dẫn đến kết luận.",
     "Phân tích áp dụng", "giải thích ngắn vì sao căn cứ dẫn đến kết luận."),
    ("Lưu ý giới hạn nguồn", "Chỉ thêm phần này khi nguồn chưa đủ, có rủi ro về hiệu lực, thiếu văn bản hợp nhất, hoặc chỉ thấy bản dự thảo, bản scan, bản OCR.",
     "Lưu ý", "chỉ nêu khi nguồn chưa đủ, có rủi ro hiệu lực, thiếu văn bản hợp nhất hoặc nguồn chưa được kiểm chứng."),
]


def _language_style_block(for_nlm: bool) -> str:
    if for_nlm:
        banned = "\n".join("- " + x + ";" for x in _STYLE_BANNED[:-1]) + "\n- " + _STYLE_BANNED[-1] + "."
        return ("## yeu_cau_ve_van_phong\n" + _STYLE_INTRO + "\n\n" + _STYLE_TONE + "\n\n"
                + "Không dùng:\n" + banned + "\n\n" + _STYLE_TERMS + "\n\n" + _STYLE_SPLIT + "\n\n" + _STYLE_CLOSE + "\n")
    return ("## van_phong_tra_loi\n" + _STYLE_INTRO + " " + _STYLE_TONE + "\n\n"
            + "Không dùng: " + "; ".join(_STYLE_BANNED) + ".\n\n"
            + _STYLE_TERMS + " " + _STYLE_SPLIT + "\n\n" + _STYLE_CLOSE + "\n")


def _answer_structure_block(for_nlm: bool) -> str:
    if for_nlm:
        items = "\n\n".join(f"{i}. **{t}**  \n{d}" for i, (t, d, _pt, _pd) in enumerate(_ANSWER_PARTS, 1))
        return "## cach_tra_loi_mac_dinh\nMặc định trả lời theo cấu trúc:\n\n" + items + "\n"
    items = "\n".join(f"{i}. **{pt}** — {pd}" for i, (_t, _d, pt, pd) in enumerate(_ANSWER_PARTS, 1))
    return "## cau_truc_tra_loi_mac_dinh\nKhi trả lời câu hỏi pháp lý, ưu tiên cấu trúc:\n\n" + items + "\n"


def _nlm_answer_style() -> str:
    return _answer_structure_block(for_nlm=True)


def _nlm_language_style() -> str:
    return _language_style_block(for_nlm=True)


def _nlm_insufficient_source_samples() -> str:
    return """## mau_cau_khi_khong_du_can_cu
- “Trong nguồn hiện có của notebook, tôi chưa tìm thấy căn cứ trực tiếp để khẳng định nội dung này.”
- “Nguồn hiện tại chỉ cho thấy quy định tại …, chưa đủ để kết luận về …”
- “Cần kiểm tra thêm văn bản hợp nhất hoặc văn bản sửa đổi, bổ sung liên quan trước khi kết luận chắc chắn.”
- “Tôi chưa thể xác nhận đây là trích dẫn nguyên văn từ nguồn hiện có.”
- “Nguồn này có dấu hiệu là dự thảo, bản scan hoặc OCR, nên chỉ nên dùng để tham khảo, chưa nên coi là căn cứ cuối cùng.”
"""

def _project_orchestration_contract() -> str:
    return """## project_orchestration_contract
Claude Project là lớp điều phối sử dụng skill `tra-luat`. Project Instruction chỉ nêu các nguyên tắc then chốt; không chép lại toàn bộ skill. Khi có xung đột, `SKILL.md` và quy trình hiện hành trong skill `tra-luat` là chuẩn ưu tiên.

Mục tiêu chính của Project là chất lượng truy vấn: chọn đúng công cụ, chọn đúng nguồn, hỏi đúng phạm vi, kiểm lại nguyên văn, rồi mới trả lời. Không dùng trí nhớ mô hình hoặc câu trả lời RAG để thay thế căn cứ đã kiểm chứng.
"""


def _project_bootstrap_contract(tier: str = "core") -> str:
    """① v1.34.68: CORE rút gọn (1 đoạn, giữ nguyên nghĩa 5 bước); FULL giữ bản 5 bước đánh số cũ."""
    if tier == "full":
        return """## bootstrap_bat_buoc
Khi bắt đầu phiên làm việc trong Project này, Claude phải:

1. Đọc `SKILL.md` của skill `tra-luat`.
2. Thực hiện bootstrap theo hướng dẫn của skill.
3. Nạp hoặc kiểm tra các tool cần thiết trước khi xử lý yêu cầu.
4. Xác định đúng loại yêu cầu: tra cứu, trích nguyên văn, kiểm hiệu lực, nạp nguồn, rà soát, soạn thảo hay tạo prompt/instruction.
5. Xác định đúng profile/corpus nếu yêu cầu liên quan đến nguồn dữ liệu. Mặc định của Project này là vbqppl, trừ khi người dùng nêu profile khác.
"""
    return """## bootstrap_bat_buoc
Khi bắt đầu phiên làm việc trong Project này, Claude phải: đọc `SKILL.md` của skill `tra-luat`; bootstrap và nạp/kiểm tool theo hướng dẫn của skill; xác định đúng loại yêu cầu (tra cứu, trích nguyên văn, kiểm hiệu lực, nạp nguồn, rà soát, soạn thảo, tạo prompt/instruction) và profile/corpus tương ứng. Mặc định của Project này là vbqppl, trừ khi người dùng nêu profile khác.
"""


def _project_dev_gate_pointer() -> str:
    """① v1.34.68 (Q4): CORE thay 2 khối dev (script_reuse + van_ban_lon) bằng con trỏ điều kiện
    "CHỈ KHI" — chi tiết sống ở SKILL.md/references, bản đầy đủ lấy qua --tier full."""
    return """## chi_khi_dev_release_ocr
**CHỈ KHI nạp/ghi nguồn, đóng gói/release, live-smoke/deploy hoặc OCR/chunk văn bản lớn:** làm theo `SKILL.md` + `references/RUNBOOK.md`/`references/DEV_TOOLING_GUIDE.md`; bản đầy đủ các gate dev: `tl instructions --target project --tier full`.

KHÔNG viết tool mới khi chưa qua `tl tool-inventory` và `tl route-task`; lệnh ghi phải có dry-run và verify/readback theo skill.
"""

def _project_script_reuse_gate() -> str:
    return """## script_reuse_va_quyet_dinh_viet_tool
Trước khi viết bất kỳ script, hàm, tool, loop hoặc đoạn xử lý tự chế nào, Claude phải kiểm kho công cụ hiện có của skill `tra-luat`.

Thứ tự bắt buộc:

1. Đọc `SKILL.md` và phần bản đồ tool/script hiện hành.
2. Chạy hoặc kiểm `tl tool-inventory --json` để xem các nhóm lệnh và năng lực hiện có.
3. Chạy `tl route-task --task <tac_vu> --json` với tác vụ rủi ro như nạp nguồn, OCR, zip, convert/rename, chunk, gọi NLM hoặc viết tool mới; với lệnh ghi phải đọc `idempotency_key`, `resume_command`, `readback_command`, `rollback_hint`.
4. Trước khi đóng gói hoặc sau khi sửa workflow/tool, chạy `tl workflow-audit --json`, `tl determinism-audit --strict --json`, `tl golden-test --json` và `tl release-check --strict-determinism --full --json` để bắt drift giữa Project Instruction, workflow cards, router và CLI.
5. Trước khi phát hành zip, chạy `tl release-manifest --out RELEASE_MANIFEST.json --json` và `tl release-verify RELEASE_MANIFEST.json --json`; khi cần đóng gói tất định dùng `tl release-bundle --out <file.zip> --json`.
6. Trước khi chạy test live, dùng `tl live-readiness --json` và `tl live-contract-check --json`; nếu đạt, chụp `tl live-state-snapshot --out before.json --json`, dùng `tl live-smoke-plan --json`, chụp `after.json`, rồi chạy `tl live-state-diff before.json after.json --json` để chỉ cho phép thay đổi dự kiến.
7. Khi cần bàn giao triển khai hoặc rollback, dùng `tl final-acceptance --json`, `tl go-live-runbook --out GO_LIVE_RUNBOOK.md`, `tl deploy-plan --json` và `tl rollback-plan --json` để có kế hoạch không ghi dữ liệu trước.
8. Kiểm `tl -h` và `tl <lệnh> --help` với nhóm lệnh liên quan.
9. Liệt kê hoặc tra cứu `scripts/*.py` kèm docstring dòng đầu khi cần kiểm năng lực ở mức script.
10. Tìm hàm nghiệp vụ đã có trong `scripts/tl.py`, `scripts/common.py` và script liên quan.
11. Kiểm `references/API_CONTRACT.md` nếu thao tác gọi webapp, Drive, registry hoặc NotebookLM.
12. Chỉ viết tool mới khi không có lệnh, script hoặc hàm hiện có đáp ứng.

Nếu vẫn cần viết tool mới, Claude phải nêu rõ: tác vụ cần giải quyết; các lệnh/script/hàm đã kiểm; vì sao công cụ hiện có không đủ; tool mới thuộc nhóm chức năng nào; input/output dự kiến, ưu tiên JSON; chế độ dry-run; bước verify/readback; selftest hoặc audit cần bổ sung.

Trước khi phát hành bản skill mới hoặc bàn giao triển khai/rollback, chạy lại ĐÚNG trình tự audit → release → live → bàn giao ở các bước 4–7 nêu trên; không bỏ bước, không thay bằng lệnh tự chế.

Không viết tool mới khi chưa qua `tl tool-inventory` và `tl route-task`. Không viết snippet tạm để thay thế lệnh đã có của skill. Không sửa file skill trực tiếp bằng thao tác native nếu skill yêu cầu dùng `tl edit-skill` hoặc quy trình sửa an toàn.
"""


def _project_tool_roles() -> str:
    return """## phan_vai_cong_cu
- `tra-luat`: công cụ chính để tra cứu, kiểm chứng, trích nguyên văn điều/khoản/điểm, kiểm hiệu lực, kiểm quan hệ sửa đổi/bổ sung/VBHN, quản lý nguồn, registry, manifest, profile và pipeline nạp nguồn.
- NotebookLM: công cụ hỗ trợ đọc nhanh, định vị nội dung, đối chiếu trong nguồn đã có.
- Claude: lớp điều phối, chọn công cụ đúng, chia nhỏ truy vấn, kiểm tra rủi ro, tổng hợp và trả lời người dùng.

Không coi câu trả lời của NotebookLM là căn cứ cuối cùng nếu chưa kiểm lại bằng nguồn hoặc skill phù hợp.
"""


def _project_source_priority() -> str:
    return """## uu_tien_nguon
Khi cần tìm hoặc tải văn bản, ưu tiên theo workflow thực tế của người dùng:

1. Thư Viện Pháp Luật.
2. LuatVietnam.
3. Công báo.
4. vbpl.vn.
5. vanban.chinhphu.vn.
6. Cổng cơ quan ban hành hoặc nguồn chính thức tương đương.

Lý do: người dùng có tài khoản Thư Viện Pháp Luật và LuatVietnam, nên hai nguồn này được ưu tiên để tra cứu, tải, đối chiếu và lấy văn bản có cấu trúc thuận tiện.

Khi cần kiểm chứng tính chính thức, hiệu lực, văn bản gốc, văn bản sửa đổi hoặc văn bản hợp nhất, có thể đối chiếu thêm với Công báo, vbpl.vn, vanban.chinhphu.vn hoặc cổng cơ quan ban hành.
"""


def _project_nlm_query_quality() -> str:
    return """## chat_luong_truy_van_notebooklm
Khi cần gọi NotebookLM, mục tiêu là truy vấn hẹp, đúng nguồn và có khả năng kiểm chứng cao nhất. Không hỏi một câu lớn trên quá nhiều nguồn.

Quy trình chọn nguồn trước khi hỏi NLM:

1. Dùng skill để lọc nguồn trước: `locate`, `source-map`, `reg-query`, `vb_status` hoặc lệnh tương đương.
2. Chọn đúng phiên bản: ưu tiên VBHN còn hiệu lực nếu phù hợp; loại bớt bản gốc đã bị thay thế, bản sửa đổi rời, bản dự thảo, bản OCR hoặc nguồn không đúng trạng thái.
3. Chỉ đưa vào NLM số nguồn tối thiểu đủ để trả lời.
4. Mỗi lần `tl nlm-query`/`notebook_query` nên dùng 1–3 `source_id`. Đây là vùng tối ưu.
5. Trường hợp cần đối chiếu phức tạp có thể dùng 4 nguồn, nhưng phải có lý do rõ.
6. `hard cap` là 5 nguồn. Không dùng 5 nguồn như mặc định; chỉ dùng khi thật sự cần và vẫn phải kiểm lại bằng nguyên văn.
7. Nếu cần nhiều hơn 4 nguồn, phải chia câu hỏi thành nhiều lượt nhỏ theo từng văn bản, từng nhóm điều, từng vấn đề pháp lý hoặc từng giai đoạn hiệu lực. Sau đó Claude tổng hợp kết quả.

Gợi ý chọn số nguồn:

- Trích nguyên văn một điều/khoản/điểm: 1 nguồn, ưu tiên dùng `tra-luat`/`tl extract` thay vì NLM.
- Đối chiếu văn bản hợp nhất với văn bản gốc hoặc văn bản sửa đổi: 2–3 nguồn.
- So sánh nhiều văn bản cùng chủ đề: chia thành nhiều lượt, mỗi lượt 2–3 nguồn.
- Rà soát hồ sơ hoặc văn bản dài: chia theo chương, mục, nhóm điều hoặc câu hỏi kiểm tra; không gom toàn bộ vào một truy vấn.

Sau khi NLM trả lời, Claude phải verify nguyên văn và kiểm lại phần quan trọng bằng nguồn nguyên văn hoặc lệnh của skill. Không nhận RAG làm nguyên văn.
"""


def _project_verbatim_contract() -> str:
    return """## trich_nguyen_van_vbqppl
Đối với văn bản quy phạm pháp luật, khi người dùng yêu cầu trích nguyên văn điều, khoản, điểm, chương, mục hoặc phụ lục, Claude phải ưu tiên sử dụng skill `tra-luat`, đặc biệt là lệnh trích đúng Điều/khoản/điểm nếu có.

Không dùng NotebookLM làm nguồn trích nguyên văn cuối cùng nếu skill có công cụ phù hợp hơn.

Trước khi trả lời trích nguyên văn, phải kiểm tra: đúng văn bản; đúng số hiệu, ngày ban hành nếu có; đúng điều, khoản, điểm, mục, chương hoặc phụ lục; đúng câu chữ, dấu câu, ký hiệu, số thứ tự; đúng nguồn trích.

Nếu chưa chắc là nguyên văn, không đặt nội dung trong ngoặc kép như trích dẫn. Hãy nói rõ: “Tôi chưa thể xác nhận đây là trích dẫn nguyên văn từ nguồn hiện có.”
"""


def _project_legal_answer_rules() -> str:
    return """## nguyen_tac_tra_loi_phap_ly
Chỉ kết luận chắc chắn khi đã có căn cứ đủ rõ. Không tự tạo căn cứ pháp lý. Không tự suy đoán số điều, khoản, điểm, hiệu lực, quan hệ sửa đổi, bổ sung, thay thế hoặc văn bản hợp nhất.

Khi có văn bản hợp nhất phù hợp và đã kiểm được nguồn, áp dụng VBHN-first: ưu tiên dùng văn bản hợp nhất để rà chính. Nếu chỉ có văn bản gốc hoặc văn bản sửa đổi riêng lẻ, phải nói rõ giới hạn này.

Với nguồn dự thảo, bản scan, OCR hoặc nguồn chưa rõ trạng thái, phải cảnh báo rõ và không trình bày như căn cứ pháp lý cuối cùng.
"""


def _project_ingest_guard() -> str:
    return """## nap_nguon_va_cap_nhat_corpus
Khi người dùng yêu cầu thêm nguồn, nạp văn bản, cập nhật corpus, registry, manifest hoặc NotebookLM, Claude phải làm theo pipeline của skill `tra-luat`.

Không nạp thẳng URL vào NotebookLM làm nguồn canonical nếu skill yêu cầu đi qua bước chuẩn hóa.

Trước khi ghi hoặc nạp nguồn mới vào corpus, phải trình người dùng duyệt các thông tin chính: nguồn dự kiến, lý do chọn nguồn, tên văn bản, số hiệu/năm nếu có, loại văn bản, profile/corpus/notebook đích nếu có, tên chuẩn dự kiến và rủi ro nếu nguồn chưa phải bản tốt nhất.
"""


def _project_large_doc_ocr_rule() -> str:
    return """## van_ban_lon_va_pdf_scan
Mục tiêu khi nạp văn bản là chất lượng truy vấn và khả năng kiểm chứng, không phải nạp thật nhiều nguồn.

Với văn bản quy phạm pháp luật, giữ bản canonical đầy đủ. Không tách bản canonical. Nếu cần tăng chất lượng truy vấn NotebookLM, chỉ tạo nguồn phụ theo Phần/Chương/cụm Điều và phải liên kết về bản canonical.

Với văn bản thường trong profile, có thể tách văn bản lớn thành nhiều nguồn nhỏ để truy vấn tốt hơn. Việc tách phải theo cấu trúc tự nhiên của văn bản và phải có kế hoạch dry-run trước khi apply.

Khi gặp file PDF, scan hoặc OCR:

1. Ưu tiên tìm bản `.docx`, `.doc`, Google Doc hoặc nguồn text sạch trước.
2. Không coi PDF scan/OCR là căn cứ cuối cùng nếu chưa kiểm chứng.
3. Nếu cần OCR local hoặc trích text-layer, dùng `tl ocr-run` để tạo sidecar text kèm `ocr_manifest.v1`, rồi chạy `tl ocr-verify` trước khi ingest.
4. Nếu dùng OCR từ Drive/Paddle/Document AI bên ngoài, vẫn phải đưa text sidecar qua `tl ocr-verify`, gắn `source_quality=ocr` khi ingest và bảo đảm manifest/hash đọc lại được.
5. Chỉ dùng `--ocr-verified` khi manifest có `verification_status=verified`, `source_sha256`/`text_sha256` khớp và đã đối chiếu đủ để tin rằng nội dung không mất trang, không mất Điều, không sai phụ lục và không lỗi chữ nghiêm trọng.
6. Với VBQPPL, OCR thiếu manifest verified thì không được đưa vào corpus/NLM làm nguồn canonical.
7. Với profile văn bản thường, OCR chưa verify có thể lưu làm bản tham khảo, nhưng phải cảnh báo rõ và không dùng làm căn cứ cuối cùng.

Khi văn bản lớn cần đưa vào NotebookLM, Claude phải ưu tiên lập kế hoạch tách ổn định:

- dùng `tl chunk-plan` trước để lập kế hoạch;
- chỉ dùng `tl chunk-apply` khi kế hoạch rõ và không phải bản canonical VBQPPL;
- mỗi chunk nên dưới khoảng 100.000 ký tự;
- mỗi chunk phải có tên rõ;
- mỗi chunk phải có phạm vi rõ;
- mỗi chunk phải liên kết về bản gốc;
- chạy `tl chunk-verify` trước khi dùng chunk để nạp hoặc truy vấn;
- khi hỏi NLM chỉ chọn chunk liên quan, không hỏi toàn bộ văn bản lớn.

Khi OCR/chunk đã verify cần đưa vào corpus, không tạo pipeline ghi mới. Phải dùng bridge về pipeline hiện có:

- OCR VBQPPL: `tl ingest-ocr <file> --text-file <ocr.txt> --cat <NN>` để verify rồi gọi lại `ingest-local` với `--source-quality ocr --ocr-verified`.
- OCR profile: `tl profile-ingest-ocr <file> --text-file <ocr.txt>` để verify rồi gọi lại `profile-ingest` với `--source-quality ocr --ocr-verified`.
- Chunk profile: `tl profile-ingest-chunks <chunk_manifest.json>` để chạy `chunk-verify` rồi gọi lại `profile-ingest` từng chunk.

Mọi bridge apply phải có `--confirm yes`. Bridge không ghi trực tiếp vào Drive, registry hoặc NotebookLM; convert/readback/register/NLM vẫn do pipeline hiện có xử lý.
"""


def _project_profile_rule(profile: str = "vbqppl", notebook_id: str | None = None, folder_name: str | None = None) -> str:
    profile = (profile or "vbqppl").strip() or "vbqppl"
    if profile == "vbqppl":
        return """## profile_va_corpus
Mặc định của Project này là vbqppl. Khi yêu cầu thuộc văn bản thường, hồ sơ nội bộ hoặc corpus dự án, Claude phải xác định profile phù hợp trước khi tìm, hỏi NLM hoặc nạp nguồn.

Tra cứu trong profile đang dùng trước. Nếu miss mới fallback VBQPPL và phải nói rõ nguồn lấy từ VBQPPL. Không ghi/nạp nhầm văn bản thường vào corpus VBQPPL.
"""
    nb = (notebook_id or "<notebookId>").strip() or "<notebookId>"
    fld = (folder_name or profile).strip() or profile
    return f"""## profile_va_corpus
Project này mặc định dùng profile `{profile}`: notebook NotebookLM `{nb}`, folder Drive `Van_ban_thuong/{fld}`, registry/manifest riêng.

Tra cứu trong profile `{profile}` trước. Nếu miss mới fallback VBQPPL và phải nói rõ nguồn lấy từ VBQPPL. Không ghi/nạp nhầm dữ liệu của profile này vào corpus VBQPPL.
"""




def _project_language_style() -> str:
    return _language_style_block(for_nlm=False)


def _project_answer_structure() -> str:
    return _answer_structure_block(for_nlm=False)


def _project_prompt_generation_contract() -> str:
    return """## prompt_generation_contract
Khi người dùng yêu cầu tạo System Prompt cho NotebookLM hoặc Claude Project Instruction, KHÔNG viết prompt tự do từ trí nhớ. Phải sinh từ generator của skill:

- `python scripts/tl.py instructions --target nlm|project|both` (Project mặc định tier CORE; bản đầy đủ gate dev/release/OCR: thêm `--tier full`).
- Profile văn bản thường: thêm `--profile <ten_profile> --notebook <notebook_id> --folder-name <ten_folder>`.
- Kiểm audit: thêm `--check`, hoặc `python scripts/tl.py instruction-audit --generate --target <nlm|project> [--tier core|full]`.

Có thể nhận mô tả ngắn qua `scripts/gen_instructions.py --brief "..."` để tương thích ngược, nhưng output vẫn phải lắp từ các khối đã thẩm định; không được tự chế guard mới làm suy yếu SKILL_OF_RECORD, QT-3, confirm_gate_web hoặc grounding_contract.
"""


def _operating_rule(target: str) -> str:
    if target == "nlm":
        return """## operating_rule
Khi phát hiện văn bản mới, văn bản sửa đổi, VBHN hoặc nguồn official có thể tồn tại ngoài nguồn hiện có, hãy dừng kết luận chắc chắn và yêu cầu quay về tra-luat/Claude Project để chạy exists/source-map/relation-check/vbhn-check trước khi kết luận hoặc nạp.
"""
    return """## operating_rule
Khi phát hiện văn bản mới, văn bản sửa đổi, VBHN hoặc nguồn official có thể tồn tại ngoài corpus, phải dừng, báo người dùng, rồi chạy exists/source-map/relation-check/vbhn-check trước khi kết luận hoặc nạp.
"""

def generate_style_template() -> str:
    return """# Tra-luat Style Template

Dùng tài liệu này như artifact văn phong riêng, không trộn vào Project/System prompt kỹ thuật.

## Mẫu trung tính Quốc hội/Chính phủ
- Nêu kết luận ngắn trước, sau đó căn cứ theo Điều/khoản/điểm.
- Phân biệt rõ: quy định hiện hành, dự thảo, đề xuất sửa đổi, và điểm cần xác minh.
- Khi là dự thảo, mở đầu đoạn bằng: "DỰ THẢO — chưa hiệu lực".

## Mẫu nội bộ Đảng/cơ quan
- Văn phong chặt, tránh phán đoán vượt căn cứ.
- Ghi rõ nguồn: source id/drive_id, tên văn bản, Điều/khoản/điểm, ngày truy xuất nếu là nguồn ngoài corpus.
"""


def generate_profile_load_block(meta: dict, target: str = "session", skill_version: str = VERSION) -> str:
    """P2 (v1.34.24, ADR-0003 + Q7): Instruction Block của MỘT profile — sinh từ MARKER (định danh +
    description/style/relations/source_policy), dùng làm doctrine PHIÊN hoặc dán Project Instruction.
    MỘT bản THỐNG NHẤT cho mọi môi trường (Chat = Cowork = Code); chỉ rẽ theo `target` đúng 1 dòng đầu —
    thân block bằng nhau từng byte (selftest khoá)."""
    meta = meta or {}
    p = str(meta.get("profile") or "vbqppl").strip() or "vbqppl"
    tline = {
        "session": "> DOCTRINE PHIÊN — áp dụng ngay trong phiên này; mọi môi trường (Chat = Cowork = Code) như nhau.",
        "project": "> DÁN VÀO Claude Project Instruction — một bản thống nhất cho mọi môi trường (Chat = Cowork = Code).",
    }.get((target or "session").lower(), "> DOCTRINE PHIÊN — áp dụng ngay trong phiên này; mọi môi trường (Chat = Cowork = Code) như nhau.")
    if p == "vbqppl":
        nb_lines = "\n".join(f"  - {nm}: `{nid}`" for nm, nid in VBQPPL_NOTEBOOKS)
        head = f"# Instruction Block — corpus nền VBQPPL (tra-luat v{skill_version})"
        body = [
            f"""## dinh_danh_scope
Đây là corpus nền VBQPPL (pháp điển 45 chủ đề, registry/manifest nền). Notebooks (đủ shard, đúng thứ tự):
{nb_lines}""",
            """## tra_cuu_nlm
Ưu tiên `notebook_query`/`tl nlm-query` scope 1–3 source_id (hard cap 5) trong notebook VBQPPL đang dùng;
chỉ khi MISS hoặc cần đối chiếu xuyên corpus mới `cross_notebook_query` đủ shard.""",
            """## khong_bia
Chỉ kết luận sau khi verify NGUYÊN VĂN từ nguồn đã nạp (neo source_id/drive_id + Điều/khoản/điểm khi có).
Không bịa số điều/khoản/điểm, hiệu lực, quan hệ sửa đổi/VBHN. Không nhận RAG làm nguyên văn.
Thiếu căn cứ → nói rõ: "Chưa tìm thấy căn cứ trong nguồn hiện có." """,
            """## van_phong
Trả lời tiếng Việt, rõ ràng, chuẩn mực, câu ngắn, mỗi câu một ý; không dùng cụm mơ hồ khi nguồn chưa đủ căn cứ.""",
        ]
        return head + "\n\n" + tline + "\n\n" + "\n\n".join(x.strip() for x in body).strip() + "\n"
    nb = str(meta.get("notebookId") or "<notebookId>").strip() or "<notebookId>"
    fld = str(meta.get("folder_name") or p).strip() or p
    root = str(meta.get("rootFolderId") or "<rootFolderId>").strip() or "<rootFolderId>"
    reg = str(meta.get("registryDocId") or "<registryDocId>").strip() or "<registryDocId>"
    man = str(meta.get("manifestId") or "<manifestId>").strip() or "<manifestId>"
    desc = str(meta.get("description") or "").strip()
    style = str(meta.get("style") or "").strip()
    rel = meta.get("relations") if isinstance(meta.get("relations"), dict) else {}
    see_also = [str(x) for x in (rel.get("see_also") or []) if str(x).strip()]
    policy = str(meta.get("source_policy") or "materialize_preferred").strip()
    head = f"# Instruction Block — profile `{p}` (tra-luat v{skill_version})"
    body = [
        f"""## dinh_danh_scope
Profile `{p}` (văn bản thường): notebook NotebookLM `{nb}`, folder Drive `Van_ban_thuong/{fld}`
(rootFolderId `{root}`), registry Sheet `{reg}` + manifest `{man}` RIÊNG (manifestScope=own, categories=own).{(chr(10) + 'Mô tả phạm vi: ' + desc) if desc else ''}
Nguồn sự thật định danh = marker `_meta/tra_luat_profile.json` (ADR-0003); kiểm nhanh: `tl --profile {p} profile-info`.""",
        f"""## tra_cuu_nlm
Tra cứu NLM của profile này đi ĐÚNG notebook `{nb}`: `notebook_query`/`tl nlm-query` scope 1–3 source_id
(hard cap 5). Tìm trong notebook profile TRƯỚC; MISS mới `cross_notebook_query` sang nền VBQPPL (+shards)
và báo rõ "lấy từ VBQPPL". Trùng nhau → canonical của profile THẮNG.""",
        f"""## khong_bia
Chỉ kết luận sau khi verify NGUYÊN VĂN từ nguồn đã nạp (neo source_id/drive_id + Điều/khoản/điểm khi có).
Không bịa số điều/khoản/điểm, hiệu lực, quan hệ sửa đổi/VBHN. Không nhận RAG làm nguyên văn.
Thiếu căn cứ → nói rõ: "Chưa tìm thấy căn cứ trong nguồn của profile `{p}`." """,
        "## van_phong\n" + (style if style else
                            "Trả lời tiếng Việt, rõ ràng, chuẩn mực, câu ngắn, mỗi câu một ý; "
                            "không dùng cụm mơ hồ khi nguồn chưa đủ căn cứ."),
        f"""## quan_he_corpus
Nền VBQPPL LUÔN BẬT (base-also): đối chiếu căn cứ pháp lý dùng nền vbqppl, hit nền phải báo `scope=vbqppl`.{(chr(10) + 'Profile liên quan (tra chéo khi người dùng nhắc tới): ' + ', '.join('`' + x + '`' for x in see_also) + '.') if see_also else ''}""",
        f"""## scope_ghi
Ghi/nạp nguồn CHỈ vào registry/manifest/notebook của `{p}` (`tl --profile {p} profile-ingest ...`);
KHÔNG ghi vào corpus nền VBQPPL. Nguồn chỉ-có-trên-NLM (nlm-only) phải nói rõ CHƯA có file Drive;
chính sách nguồn: {policy} (ưu tiên materialize về Drive khi xuất được).""",
    ]
    # v1.34.71 (ke-hoach-profile-templates Q4): khối trinh_bay_theo_mau — CHỈ khi marker có templates
    # (không templates → block VẮNG, giữ y nguyên profile cũ). Nội dung entry từ marker (Q1); scope dùng
    # tiền tố điều kiện "CHỈ KHI" (nếp Q4 kế hoạch instruction-refactor). Thân session==project byte-equal.
    tpls = [t for t in (meta.get("templates") or []) if isinstance(t, dict) and str(t.get("drive_id") or "").strip()]
    if tpls:
        _tl_lines = []
        for t in tpls:
            _tid = str(t.get("id") or "").strip() or "<id>"
            _seg = f"  - `{_tid}` — {str(t.get('name') or '').strip() or _tid}: `{str(t.get('drive_id') or '').strip()}`."
            if str(t.get("scope") or "").strip():
                _seg += f" **CHỈ KHI {str(t.get('scope') or '').strip()}.**"
            if str(t.get("note") or "").strip():
                _seg += f" {str(t.get('note') or '').strip()}"
            _tl_lines.append(_seg)
        body.append("## trinh_bay_theo_mau\nProfile có mẫu trình bày riêng (đọc khung bằng `tl doc-text <drive_id>`):\n"
                    + "\n".join(_tl_lines)
                    + "\n\nKhi soạn theo mẫu: GIỮ NGUYÊN khung/đề mục/trật tự phần của mẫu, chỉ điền nội dung; "
                      "mọi căn cứ pháp lý phải verify NGUYÊN VĂN trước khi đưa vào; văn phong theo khối van_phong; "
                      "dựng file .docx thành phẩm bằng `tl the-thuc-build --spec <json> --out <docx>` "
                      "(hệ hanh-chinh | dang | vbqppl-qh, hoặc mau=phieu_trinh) rồi kiểm bằng "
                      "`tl the-thuc-check`; mẫu phức tạp ngoài khả năng dựng thì dùng công cụ "
                      "docx của MÔI TRƯỜNG theo khung mẫu.")
    return head + "\n\n" + tline + "\n\n" + "\n\n".join(x.strip() for x in body).strip() + "\n"


def _target_blocks(target: str, skill_version: str, profile: str, notebook_id: str | None,
                   folder_name: str | None, root_folder_id: str | None, tier: str = "core") -> list[str]:
    is_project_profile = profile != "vbqppl"
    suffix = f" ({profile})" if is_project_profile else ""
    head = {
        "project": "# Claude Project Instruction — tra-luat",
        "nlm": "# NotebookLM System Prompt — tra-luat",
        "config": "# Tra-luat Project Config Guard",
    }[target] + suffix

    if target == "nlm":
        body = [
            head,
            _nlm_runtime_contract(),
            _nlm_foundation_rules(),
            _nlm_verbatim_mode(),
            _nlm_answer_style(),
            _nlm_language_style(),
            _nlm_insufficient_source_samples(),
        ]
    else:
        # ① v1.34.68 (Q3): tier CORE (mặc định — Project tra cứu thường ngày) bỏ 2 khối dev
        # script_reuse_va_quyet_dinh_viet_tool + van_ban_lon_va_pdf_scan (41% bloat), thay bằng con trỏ
        # "CHỈ KHI"; tier FULL giữ đủ gate cho Project bảo trì skill. NLM không có tier.
        full = tier == "full"
        body = [
            head,
            _project_orchestration_contract(),
            _skill_of_record(skill_version),
            _project_bootstrap_contract("full" if full else "core"),
            _project_script_reuse_gate() if full else _project_dev_gate_pointer(),
            _project_tool_roles(),
            _project_source_priority(),
            _project_nlm_query_quality(),
            _project_verbatim_contract(),
            _project_legal_answer_rules(),
            _project_ingest_guard(),
        ]
        if full:
            body.append(_project_large_doc_ocr_rule())
        body += [
            _project_profile_rule(profile, notebook_id, folder_name),
            _manifest_fallback(notebook_id, profile),
            _project_prompt_generation_contract(),
            _project_language_style(),
            _project_answer_structure(),
        ]
        if is_project_profile:
            body.append(_profile_setup(profile, notebook_id, folder_name, root_folder_id))
    return body


def generate(target: str = "both", skill_version: str = VERSION,
             profile: str = "vbqppl", notebook_id: str | None = None,
             folder_name: str | None = None, root_folder_id: str | None = None,
             brief: str | None = None, he: str | None = None, tier: str = "core") -> str:
    """Sinh Instruction/System Prompt từ các khối đã thẩm định.

    - `target='nlm'` ⇒ System Prompt chuyên cho NotebookLM: đọc/định vị, không quản trị corpus.
    - `target='project'` ⇒ Claude Project Instruction: điều phối skill, registry, manifest, QT-3.
    - `tier='core'` (MẶC ĐỊNH từ v1.34.68 — breaking Q3 có chủ đích) ⇒ Project tra cứu thường ngày,
      2 khối dev thay bằng con trỏ "CHỈ KHI"; `tier='full'` ⇒ thêm đủ gate dev/release/OCR (bản cũ).
      NLM không có tier (output như nhau).
    - `profile='vbqppl'` ⇒ corpus VBQPPL nền.
    - `profile=<tên dự án>` ⇒ gắn Project vào profile văn bản thường, fallback VBQPPL.
    - `brief`/`he` giữ tương thích CLI cũ; không sinh prompt tự do.
    """
    target = (target or "both").lower()
    if target not in {"project", "nlm", "both", "config", "style-template"}:
        raise ValueError(f"unknown target: {target}")
    tier = (tier or "core").lower()
    if tier not in {"core", "full"}:
        raise ValueError(f"unknown tier: {tier}")
    if target == "style-template":
        return generate_style_template()
    profile = (profile or "vbqppl").strip() or "vbqppl"

    if target == "both":
        nlm = generate("nlm", skill_version, profile, notebook_id, folder_name, root_folder_id, brief, he, tier).strip()
        project = generate("project", skill_version, profile, notebook_id, folder_name, root_folder_id, brief, he, tier).strip()
        return nlm + "\n\n---\n\n" + project + "\n"

    concrete = "project" if target == "config" else target
    body = _target_blocks(concrete, skill_version, profile, notebook_id, folder_name, root_folder_id, tier)
    if target == "config":
        body[0] = "# Tra-luat Project Config Guard" + (f" ({profile})" if profile != "vbqppl" else "")
    return "\n\n".join(x.strip() for x in body).strip() + "\n"


# ⑤ v1.34.68: REQUIRED_PROJECT = bộ khóa tier CORE — CHỈ guard tra-cứu + write-safety. Các khóa
# dev/release/live/deploy/OCR dời sang _REQUIRED_FULL_EXTRA (audit target "full"). Đổi ĐỒNG BỘ với ①
# (CORE bỏ 2 khối dev) — nếu thêm khóa mới ở đây phải chắc khối CORE tương ứng có chữ đó.
REQUIRED_PROJECT = {
    "SKILL_OF_RECORD": "Instruction phải chỉ rõ skill chuẩn.",
    "project_orchestration_contract": "Project phải là lớp điều phối skill.",
    "đọc `SKILL.md`": "Project phải buộc đọc SKILL.md khi bắt đầu.",
    "bootstrap": "Project phải buộc bootstrap tool.",
    "tl tool-inventory": "Claude phải tra inventory trước khi tự viết tool.",
    "tl route-task": "Claude phải hỏi router với tác vụ rủi ro.",
    "không viết tool mới": "Project phải chặn viết tool mới khi chưa kiểm kho.",
    "dry-run": "Project phải yêu cầu kế hoạch dry-run cho tác vụ rủi ro.",
    "verify/readback": "Project phải yêu cầu verify/readback sau thao tác ghi.",
    "tra-luat": "Project phải ưu tiên skill tra-luat.",
    "profile_va_corpus": "Project phải có quy tắc profile/corpus ngắn gọn.",
    "NotebookLM": "Project phải phân vai NotebookLM.",
    "Thư Viện Pháp Luật": "Phải ưu tiên nguồn theo workflow người dùng.",
    "LuatVietnam": "Phải ưu tiên nguồn theo workflow người dùng.",
    "chat_luong_truy_van_notebooklm": "Phải có khối chất lượng truy vấn NLM.",
    "1–3": "Mỗi lượt NLM nên dùng 1–3 nguồn.",
    "hard cap": "Phải nêu hard cap nguồn khi gọi NLM.",
    "5 nguồn": "Phải nêu giới hạn 5 nguồn.",
    "chia câu hỏi": "Phải chia nhỏ nếu cần nhiều nguồn.",
    "tl nlm-query": "Phải ưu tiên wrapper CLI khi gọi NLM.",
    "source_id": "Phải scope đúng source_id.",
    "Không nhận RAG làm nguyên văn": "Phải buộc verify sau NLM.",
    "tl extract": "Trích nguyên văn VBQPPL nên ưu tiên skill/extract.",
    "verify nguyên văn": "Phải buộc kiểm chứng bằng nguyên văn.",
    "VBHN-first": "Phải giữ nguyên tắc VBHN-first.",
    "DỰ THẢO": "Phải cảnh báo dự thảo chưa hiệu lực.",
    "Điều": "Phải neo về Điều/khoản/điểm.",
}

# ⑤ Khóa CHỈ bắt buộc ở tier FULL (Project bảo trì skill: dev/release/live/deploy/OCR-chunk).
_REQUIRED_FULL_EXTRA = {
    "script_reuse_va_quyet_dinh_viet_tool": "Project phải có gate tái sử dụng script/tool.",
    "tl workflow-audit": "Project phải audit workflow/router để bắt drift.",
    "tl release-check": "Project phải có acceptance harness offline trước khi đóng gói.",
    "tl release-manifest": "Project phải tạo manifest SHA-256 trước khi phát hành zip.",
    "tl release-verify": "Project phải verify manifest trước khi phát hành zip.",
    "tl release-bundle": "Project phải có đường đóng gói tất định khi cần zip.",
    "tl live-readiness": "Project phải kiểm readiness live 3 tầng trước smoke test.",
    "tl live-contract-check": "Project phải kiểm contract live read-only trước smoke test.",
    "tl live-state-snapshot": "Project phải chụp snapshot before/after smoke.",
    "tl live-state-diff": "Project phải diff snapshot và chặn unexpected drift.",
    "tl final-acceptance": "Project phải có cổng acceptance cuối trước bàn giao.",
    "tl go-live-runbook": "Project phải xuất runbook triển khai live/rollback khi bàn giao.",
    "tl deploy-plan": "Project phải có kế hoạch triển khai an toàn.",
    "tl rollback-plan": "Project phải có kế hoạch rollback.",
    "van_ban_lon_va_pdf_scan": "Phải có quy tắc văn bản lớn/PDF scan-OCR.",
    "không tách bản canonical": "VBQPPL phải giữ canonical đầy đủ.",
    "source_quality=ocr": "PDF scan/OCR phải gắn chất lượng nguồn.",
    "--ocr-verified": "OCR verified phải có điều kiện rõ.",
    "100.000 ký tự": "Chunk NLM profile nên có ngưỡng ký tự rõ.",
}

REQUIRED_FULL = {**REQUIRED_PROJECT, **_REQUIRED_FULL_EXTRA}

# ④ Size-budget CORE (Q5): đo KÝ TỰ — đơn vị đo instruction của kế hoạch (Project cũ 15.127 ký tự;
# ô Instruction claude.ai đếm ký tự, không phải byte; bytes UTF-8 tiếng Việt ~1.2× ký tự).
# WARN >9K advisory, FAIL >12K (selftest đỏ). Khuôn _kernel_size_findings (workflow.py).
_CORE_SIZE_WARN_CHARS = 9 * 1024
_CORE_SIZE_FAIL_CHARS = 12 * 1024


def _core_size_findings(n_chars: int) -> dict:
    n = int(n_chars)
    return {
        "size_chars": n,
        "size_warn_limit": _CORE_SIZE_WARN_CHARS,
        "size_limit": _CORE_SIZE_FAIL_CHARS,
        "size_warn": n > _CORE_SIZE_WARN_CHARS,
        "size_ok": n <= _CORE_SIZE_FAIL_CHARS,
    }


REQUIRED_NLM = {
    "nlm_runtime_contract": "NLM phải chỉ là lớp đọc/truy vấn nguồn hiện có.",
    "không quản lý corpus": "NLM không được nhận nhiệm vụ quản trị corpus.",
    "Chỉ trả lời dựa trên nguồn": "NLM phải giới hạn trong nguồn của notebook hiện tại.",
    "Không bịa căn cứ pháp lý": "NLM không được tạo căn cứ pháp lý.",
    "Luôn ưu tiên nguyên văn": "NLM phải ưu tiên nguyên văn.",
    "Chế độ chính xác cao nhất": "NLM phải có chế độ trích dẫn nguyên văn.",
    "Đúng văn bản": "Trích dẫn phải tự kiểm đúng văn bản.",
    "Đúng vị trí": "Trích dẫn phải tự kiểm đúng điều/khoản/điểm.",
    "Đúng câu chữ": "Trích dẫn phải giữ câu chữ.",
    "Đúng nguồn trích": "Trích dẫn phải gắn nguồn.",
    "Tôi chưa thể xác nhận đây là trích dẫn nguyên văn": "Không chắc thì phải nói không xác nhận được nguyên văn.",
    "Kết luận ngắn": "NLM phải có cấu trúc trả lời ngắn trước.",
    "Căn cứ trong nguồn": "NLM phải nêu căn cứ trong nguồn.",
    "Phân tích áp dụng": "NLM phải phân tích áp dụng ngắn.",
    "Văn phong": "NLM phải có quy tắc văn phong.",
    "không dùng": "NLM phải có các điều cấm về văn phong.",
    "từ đa nghĩa": "NLM phải tránh từ đa nghĩa.",
    "từ lóng": "NLM phải tránh từ lóng.",
    "từ tiếng Anh": "NLM phải tránh tiếng Anh không cần thiết.",
    "chữ viết tắt": "NLM phải tránh viết tắt không rõ.",
}

def audit(text: str, target: str = "project") -> dict:
    """⑤ v1.34.68: target "project" = bộ khóa CORE; target "full" = CORE + khóa dev/release/OCR
    (REQUIRED_FULL) cho Instruction tier FULL. "config"→project; "both" = project(CORE) + nlm."""
    target = (target or "project").lower()
    if target == "config":
        target = "project"
    if target == "both":
        project_res = audit(text, "project")
        nlm_res = audit(text, "nlm")
        missing = ["project:" + k for k in project_res["missing"]] + ["nlm:" + k for k in nlm_res["missing"]]
        return {
            "ok": not missing,
            "missing": missing,
            "required": {"project": REQUIRED_PROJECT, "nlm": REQUIRED_NLM},
            "note": "Audit both yêu cầu đủ guard Project và đủ quy tắc NLM truy vấn/trích dẫn.",
        }
    required = REQUIRED_NLM if target == "nlm" else (REQUIRED_FULL if target == "full" else REQUIRED_PROJECT)
    missing = [k for k in required if k.lower() not in (text or "").lower()]
    note = (
        "Fail nghĩa là NLM prompt có thể lẫn nhiệm vụ corpus hoặc thiếu guard trích dẫn nguyên văn."
        if target == "nlm"
        else "Fail nghĩa là Project Instruction có thể cho phép nạp tắt vào NLM hoặc không buộc đọc skill tra-luat khi ghi/nạp."
    )
    return {
        "ok": not missing,
        "missing": missing,
        "required": required,
        "note": note,
    }


def selftest() -> int:
    cases = []
    for target in ("project", "nlm", "both", "config"):
        out = generate(target, VERSION)
        audit_target = "project" if target == "config" else target
        cases.append((f"generate_{target}_audit", audit(out, audit_target)["ok"]))
        if target != "nlm":
            cases.append((f"generate_{target}_skill_version", f"v{VERSION}" in out))
    # NLM phải sạch: không lẫn pipeline nạp nguồn/corpus.
    nlm = generate("nlm", VERSION)
    cases.append(("nlm_no_ingest_blocks", "ingest_handoff" not in nlm and "confirm_gate_web" not in nlm and "manifest_fallback" not in nlm))
    cases.append(("nlm_verbatim_mode", "che_do_trich_dan_nguyen_van" in nlm and "Đúng câu chữ" in nlm))
    # profile mặc định = vbqppl (không chèn profile_setup)
    vb = generate("project", VERSION)
    cases.append(("default_profile_is_vbqppl", "profile_setup" not in vb and "Mặc định của Project này là vbqppl" in vb))
    cases.append(("nlm_project_are_distinct", "nlm_runtime_contract" in nlm and "project_orchestration_contract" in vb))
    cases.append(("brief_compat_no_free_prompt", audit(generate("nlm", VERSION, brief="tối ưu cho NLM"), "nlm")["ok"]))
    # profile dự án: gắn profile + folder Van_ban_thuong + fallback VBQPPL + profile_setup
    pj = generate("project", VERSION, profile="luat_dat_dai", notebook_id="nb-123", folder_name="Dat_dai")
    cases.append(("project_profile_audit", audit(pj, "project")["ok"]))
    cases.append(("project_profile_binds_name", "luat_dat_dai" in pj and "profile_setup" in pj))
    cases.append(("project_profile_folder_under_vbt", "Van_ban_thuong/Dat_dai" in pj and "nb-123" in pj))
    cases.append(("project_profile_fallback_vbqppl", "fallback VBQPPL" in pj))
    # v1.34.68 ①: gate dev/release/OCR nay thuộc tier FULL — 5 ca dưới đổi sang generate(tier="full").
    def _gen_tier(*a, **kw):
        try:
            return generate(*a, **kw)
        except TypeError:   # đỏ-trước / hồi quy signature: bản chưa có tier → ca tier FAIL thay vì crash
            return ""
    vbf = _gen_tier("project", VERSION, tier="full")
    cases.append(("project_large_doc_ocr_block", "van_ban_lon_va_pdf_scan" in vbf and "source_quality=ocr" in vbf and "không tách bản canonical" in vbf.lower()))
    cases.append(("project_script_reuse_gate", "script_reuse_va_quyet_dinh_viet_tool" in vbf and "tl tool-inventory" in vbf and "tl route-task" in vbf and "verify/readback" in vbf))
    cases.append(("project_release_audit_gate", "tl workflow-audit" in vbf and "tl release-check" in vbf and "tl live-smoke-plan" in vbf and "tl live-readiness" in vbf and "tl live-contract-check" in vbf and "tl live-state-snapshot" in vbf and "tl live-state-diff" in vbf and "tl final-acceptance" in vbf and "tl go-live-runbook" in vbf))
    cases.append(("project_release_manifest_gate", "tl release-manifest" in vbf and "tl release-verify" in vbf and "tl release-bundle" in vbf))
    cases.append(("project_deploy_rollback_gate", "tl deploy-plan" in vbf and "tl rollback-plan" in vbf))
    # v1.34.68 tier CORE/FULL (Q3–Q5 kế hoạch instruction-refactor): mặc định CORE (breaking chủ đích);
    # CORE thay 2 khối dev bằng con trỏ "CHỈ KHI"; FULL giữ đủ gates + litany release đã khử lặp (②);
    # size budget CORE đo KÝ TỰ (đơn vị kế hoạch — Project cũ 15.127 ký tự) WARN>9K/FAIL>12K (④);
    # audit tách target "full" (⑤); NLM không bị tier đụng tới (⑥).
    cases.append(("tier_default_is_core", vb != "" and vb == _gen_tier("project", VERSION, tier="core")))
    cases.append(("tier_core_drops_dev_blocks", "script_reuse_va_quyet_dinh_viet_tool" not in vb
                  and "van_ban_lon_va_pdf_scan" not in vb and "CHỈ KHI" in vb and "--tier full" in vb))
    cases.append(("tier_core_audit_ok", audit(vb, "project")["ok"]))
    cases.append(("tier_full_audit_ok", vbf != "" and audit(vbf, "full")["ok"] and audit(vbf, "project")["ok"]))
    cases.append(("tier_core_fails_full_audit", not audit(vb, "full")["ok"]))
    cases.append(("tier_full_litany_deduped", vbf != "" and vbf.count("tl release-manifest --out RELEASE_MANIFEST.json --json") == 1))
    _csf = globals().get("_core_size_findings")
    cases.append(("tier_core_size_budget", bool(_csf) and _csf(len(vb))["size_ok"] and len(vb) <= 12 * 1024))
    cases.append(("tier_nlm_unaffected_by_tier", _gen_tier("nlm", VERSION, tier="full") == nlm))
    st = generate("style-template", VERSION)
    cases.append(("style_template_separate_artifact", "Style Template" in st and "SKILL_OF_RECORD" not in st))
    # P2 (v1.34.24, ADR-0003 + Q7): Instruction Block profile — sinh từ MARKER, THỐNG NHẤT mọi env,
    # chỉ rẽ theo target (session | project) ở đúng 1 dòng; thân block phải bằng nhau từng byte.
    _mt = {"profile": "beta", "notebookId": "nb-1", "rootFolderId": "FB", "folder_name": "Beta",
           "registryDocId": "RB", "manifestId": "MB", "description": "Hồ sơ BHXH Thái Nguyên",
           "style": "Văn phong trang trọng nội bộ.", "relations": {"base": "vbqppl", "see_also": ["duan_a"]},
           "source_policy": "materialize_preferred"}
    _bs = generate_profile_load_block(_mt, "session", VERSION)
    _bp = generate_profile_load_block(_mt, "project", VERSION)
    cases.append(("profile_block_binds_marker_meta",
                  "nb-1" in _bs and "Văn phong trang trọng nội bộ." in _bs and "duan_a" in _bs
                  and "Hồ sơ BHXH Thái Nguyên" in _bs and "materialize_preferred" in _bs
                  and "Van_ban_thuong/Beta" in _bs))
    cases.append(("profile_block_no_fabrication_guard",
                  "Chưa tìm thấy căn cứ" in _bs and "Không nhận RAG làm nguyên văn" in _bs
                  and "lấy từ VBQPPL" in _bs))
    cases.append(("profile_block_unified_env_target_split",
                  _bs != _bp and _bs.split("\n\n", 2)[2] == _bp.split("\n\n", 2)[2]
                  and "phiên" in _bs.split("\n\n", 2)[1].lower()
                  and "project instruction" in _bp.split("\n\n", 2)[1].lower()))
    _bv = generate_profile_load_block({"profile": "vbqppl"}, "session", VERSION)
    cases.append(("profile_block_vbqppl_base_variant",
                  "corpus nền VBQPPL" in _bv and VBQPPL_NOTEBOOKS[0][1] in _bv))
    _bd = generate_profile_load_block({"profile": "beta", "notebookId": "nb-1", "rootFolderId": "FB"},
                                      "session", VERSION)
    cases.append(("profile_block_default_style_when_empty", "## van_phong" in _bd and "tiếng Việt" in _bd))
    # v1.34.71 (ke-hoach-profile-templates Q4): khối trinh_bay_theo_mau CHỈ hiện khi marker có templates;
    # đủ 4 mệnh lệnh (doc-text / giữ khung / verify nguyên văn / phân vai docx môi trường).
    _bt = generate_profile_load_block({**_mt, "templates": [
        {"id": "phieu-trinh", "drive_id": "DTPL", "name": "Phiếu trình", "scope": "soạn phiếu trình",
         "note": ""}]}, "session", VERSION)
    cases.append(("profile_block_templates_conditional",
                  "## trinh_bay_theo_mau" in _bt and "`DTPL`" in _bt and "tl doc-text" in _bt
                  and "GIỮ NGUYÊN khung" in _bt and "verify NGUYÊN VĂN" in _bt
                  and "KHÔNG sinh docx" in _bt and "trinh_bay_theo_mau" not in _bs))
    bad = "research_start có thể import nguồn vào NotebookLM khi cần."
    cases.append(("audit_bad_project_instruction_fails", not audit(bad, "project")["ok"]))
    cases.append(("audit_bad_nlm_prompt_fails", not audit(bad, "nlm")["ok"]))
    ok = sum(1 for _, passed in cases if passed)
    for name, passed in cases:
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print(f"== gen_instructions selftest {ok}/{len(cases)} ==")
    return 0 if ok == len(cases) else 1
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["project", "nlm", "both", "config", "style-template"], default="both")
    ap.add_argument("--skill-version", default=VERSION)
    ap.add_argument("--profile", default="vbqppl", help="vbqppl (mặc định) hoặc tên profile dự án (văn bản thường)")
    ap.add_argument("--notebook", "--notebook-id", dest="notebook", help="notebookId NotebookLM của profile dự án")
    ap.add_argument("--folder-name", dest="folder_name", help="tên folder trong Van_ban_thuong (mặc định = tên profile)")
    ap.add_argument("--root-folder-id", dest="root_folder_id", help="rootFolderId nếu đã tạo folder")
    ap.add_argument("--brief", default="", help="mô tả ngắn kiểu cũ; chỉ dùng để tương thích, không sinh prompt tự do")
    ap.add_argument("--he", choices=["dang", "nhanuoc", "vbqppl", "quochoi", "all", "auto"], default="auto", help="hệ thể thức kiểu cũ; hiện dùng như metadata tương thích")
    ap.add_argument("--tier", choices=["core", "full"], default="core",
                    help="(v1.34.68 Q3) core (MẶC ĐỊNH — Project tra cứu, con trỏ CHỈ KHI) | full (thêm gate dev/release/OCR)")
    ap.add_argument("--out")
    ap.add_argument("--audit")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.audit:
        text = Path(a.audit).read_text(encoding="utf-8", errors="replace")
        _audit_target = "full" if (a.tier == "full" and a.target in ("project", "config")) else a.target
        res = audit(text, _audit_target)
        print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else ("OK" if res["ok"] else "MISSING: " + ", ".join(res["missing"])))
        return 0 if res["ok"] else 2
    target = a.target
    brief_low = (a.brief or "").lower()
    if a.brief and target == "both":
        if any(k in brief_low for k in ("nlm", "notebooklm", "notebook lm", "sổ tay")) and not any(k in brief_low for k in ("claude", "project")):
            target = "nlm"
        elif any(k in brief_low for k in ("claude", "project", "instruction")) and not any(k in brief_low for k in ("nlm", "notebooklm", "notebook lm")):
            target = "project"
    text = generate(target, a.skill_version, a.profile, a.notebook, a.folder_name, a.root_folder_id, a.brief, a.he, a.tier)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    print(json.dumps({"target": target, "text": text}, ensure_ascii=False, indent=2) if a.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
