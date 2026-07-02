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

VERSION = "1.23.23"


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


def generate(target: str = "both", skill_version: str = VERSION,
             profile: str = "vbqppl", notebook_id: str | None = None,
             folder_name: str | None = None, root_folder_id: str | None = None) -> str:
    """Sinh Instruction.

    - Mặc định `profile='vbqppl'` ⇒ Instruction VBQPPL như cũ.
    - `profile=<tên dự án>` (+ notebook_id/folder_name) ⇒ Instruction gắn Project vào profile văn bản
      thường đó (folder dưới Van_ban_thuong, notebook riêng), mặc định theo profile + fallback VBQPPL,
      kèm khối profile_setup để dựng 1 lần.
    """
    target = (target or "both").lower()
    if target not in {"project", "nlm", "both", "config", "style-template"}:
        raise ValueError(f"unknown target: {target}")
    if target == "style-template":
        return generate_style_template()
    profile = (profile or "vbqppl").strip() or "vbqppl"
    is_project_profile = profile != "vbqppl"
    suffix = f" ({profile})" if is_project_profile else ""
    head = {
        "project": "# Claude Project Instruction — tra-luat",
        "nlm": "# NotebookLM System Prompt — tra-luat",
        "both": "# Tra-luat Instruction Blocks",
        "config": "# Tra-luat Project Config Guard",
        "style-template": "# Tra-luat Style Template",
    }[target] + suffix
    body = [
        head,
        "",
        _skill_of_record(skill_version),
        _ingest_handoff(),
        _confirm_gate(),
        _grounding_contract(),
        _ocr_draft_rule(),
        _download_link_priority(),
        _corpus_profile(profile, notebook_id, folder_name),
        _manifest_fallback(notebook_id, profile),
    ]
    if is_project_profile:
        body.append(_profile_setup(profile, notebook_id, folder_name, root_folder_id))
    body += [
        "## operating_rule",
        "Khi phát hiện văn bản mới, văn bản sửa đổi, VBHN hoặc nguồn official có thể tồn tại ngoài corpus, phải dừng, báo người dùng, rồi chạy exists/source-map/relation-check/vbhn-check trước khi kết luận hoặc nạp.",
    ]
    return "\n\n".join(x.strip() for x in body).strip() + "\n"


REQUIRED = {
    "SKILL_OF_RECORD": "Instruction phải chỉ rõ skill chuẩn.",
    "ingest_handoff": "Instruction phải chuyển research_* sang discovery-only/QT-3.",
    "confirm_gate_web": "Instruction phải có cổng xác nhận trước khi nạp web.",
    "research_import": "Phải nhắc rõ research_import là điểm cấm nạp thẳng.",
    "source_add(url)": "Phải nhắc rõ source_add(url) là điểm cấm nạp thẳng.",
    "QT-3": "Phải buộc đi pipeline QT-3.",
    "notebook đang dùng": "Phải mặc định nạp vào notebook đang dùng.",
    "docx": "Phải ưu tiên docx/GDoc-convertible hơn PDF.",
    "official-first": "Phải giữ official-first.",
    "download_link_priority": "Phải có thứ tự link tải cho người dùng.",
    "corpus_profile": "Phải có quy tắc profile đa-corpus.",
    "manifest_fallback": "Phải có manifest profile-first + fallback VBQPPL.",
    "cross_notebook_query": "Phải nhắc QA xuyên corpus.",
    "nlm_notebook_id": "Phải nhắc slot theo notebook.",
    "verify nguyên văn": "Phải buộc kiểm chứng bằng nguyên văn.",
    "VBHN-first": "Phải giữ nguyên tắc VBHN-first.",
    "DỰ THẢO": "Phải cảnh báo dự thảo chưa hiệu lực.",
    "source id": "Phải neo về source id/drive_id.",
    "Điều": "Phải neo về Điều/khoản/điểm.",
}


def audit(text: str) -> dict:
    missing = [k for k in REQUIRED if k.lower() not in (text or "").lower()]
    return {
        "ok": not missing,
        "missing": missing,
        "required": REQUIRED,
        "note": "Fail nghĩa là Instruction có thể cho phép nạp tắt vào NLM hoặc không buộc đọc skill tra-luat khi ghi/nạp.",
    }


def selftest() -> int:
    cases = []
    for target in ("project", "nlm", "both", "config"):
        out = generate(target, VERSION)
        cases.append((f"generate_{target}_audit", audit(out)["ok"]))
        cases.append((f"generate_{target}_skill_version", f"v{VERSION}" in out))
    # v1.19: profile mặc định = vbqppl (không chèn profile_setup)
    vb = generate("project", VERSION)
    cases.append(("default_profile_is_vbqppl", "profile_setup" not in vb and "Project này là vbqppl" in vb))
    # profile dự án: gắn profile + folder Van_ban_thuong + fallback VBQPPL + profile_setup
    pj = generate("project", VERSION, profile="luat_dat_dai", notebook_id="nb-123", folder_name="Dat_dai")
    cases.append(("project_profile_audit", audit(pj)["ok"]))
    cases.append(("project_profile_binds_name", "luat_dat_dai" in pj and "profile_setup" in pj))
    cases.append(("project_profile_folder_under_vbt", "Van_ban_thuong/Dat_dai" in pj and "nb-123" in pj))
    cases.append(("project_profile_fallback_vbqppl", "fallback VBQPPL" in pj))
    st = generate("style-template", VERSION)
    cases.append(("style_template_separate_artifact", "Style Template" in st and "SKILL_OF_RECORD" not in st))
    bad = "research_start có thể import nguồn vào NotebookLM khi cần."
    cases.append(("audit_bad_instruction_fails", not audit(bad)["ok"]))
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
    ap.add_argument("--out")
    ap.add_argument("--audit")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.audit:
        text = Path(a.audit).read_text(encoding="utf-8", errors="replace")
        res = audit(text)
        print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else ("OK" if res["ok"] else "MISSING: " + ", ".join(res["missing"])))
        return 0 if res["ok"] else 2
    text = generate(a.target, a.skill_version, a.profile, a.notebook, a.folder_name, a.root_folder_id)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    print(json.dumps({"target": a.target, "text": text}, ensure_ascii=False, indent=2) if a.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
