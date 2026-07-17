---
description: In 8 bước quy trình chuẩn mỗi đợt (§6 kế hoạch guard-va-boc-tl-core) — lặp không chệch
---

In checklist sau cho user (đúng §6 kế hoạch `ke-hoach-guard-va-boc-tl-core-2026-07-18.md`), đánh dấu
bước nào đã/chưa làm nếu ngữ cảnh phiên cho biết:

1. **Characterization capture** TRƯỚC khi động code — `/charact --clusters --stability 2` →
   `scripts/.tl_state/charact/` (scrub `_scrub_volatile`).
2. **TDD rN negative-trước** — drift-lock wiring: handler tồn tại; `__tl_stub__ == (key_mới, tên)`;
   COMMAND_META y nguyên (kể cả `nlm_fallback`); `_CREDS_LAZY_CMDS` membership y nguyên.
   (Điểm sửa đã tra: Đợt A = `r75_ingest_ops_module_wired` 11 tên → `source_ops`; Đợt B =
   `r71_nlm_ops_module_wired` 7 tên → `nlm_admin_ops`; `r81` TỰ thích nghi; `r99_resolve_stub_wired` GIỮ.)
3. **MOVE NGUYÊN VĂN** def/hằng — không viết lại lời; module mới đúng khuôn I5 (docstring nguồn gốc +
   stdlib `# noqa: F401` + `bind()` REBASE `__globals__`).
4. **Wire**: `_tl_core_import` (+1 dòng ~tl.py:1250) + key `_STUB_MAP` (CHUYỂN tên, không copy) +
   HẰNG re-export TRỰC TIẾP (bẫy I11 — hằng KHÔNG vào _STUB_MAP).
5. **Gate offline**: `/gate` — selftest FULL + 3 audit strict + **golden 0-DIFF** (diff = BUG của move —
   DỪNG; **CẤM `golden-test --write`**, trừ nếp SKILL.md-header cuối release) + charact so-khớp-byte.
6. **Live-smoke**: Đợt A = offline đủ (source-CRUD không cần NLM); Đợt B = dead-path fake-home
   (add→DEFERRED; migrate --apply→DEFERRED+artifact; audit→UNVERIFIED stale) + 1 vòng đọc-sống
   `nlm-list`/audit DRY khi có cookie (~1h DBSC); KHÔNG ghi sống. Journal theo HOME.
7. **Release trọn chu trình**: CHANGELOG; manifest CUỐI (`release-manifest --out` — dry mặc định!);
   bundle ×2 same-SHA; secret-guard; commit -F; CI ubuntu+windows xanh.
8. **Deploy**: script upload (tl release-bundle) + byte-match download + curl VERSION + ghi memory.
   SKILL.md chỉ đổi header version → user re-import "khi tiện".

Doctrine đứng: MOVE nguyên văn — KHÔNG refactor logic; move theo DANH-SÁCH-TÊN trong kế hoạch —
KHÔNG sweep tự động (R2); golden 0-diff là GATE (R6); số version = VERSION hiện hành +1 (danh nghĩa).
