# Đặc tả packet CHANGELOG-D-NGOAI-GOI r2 — đưa `changelog.d/` ra khỏi gói phát hành

Đặc tả đóng băng. Muốn đổi thì soạn `CHANGELOG-D-NGOAI-GOI-r3.md`, không sửa đè.
Đặc tả KHÔNG cấp việc: cần Packet Issue #1134 + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).
Chỗ nào đặc tả không nói, executor DỪNG và hỏi trên #1134 — không tự nới.

- `packet_id`: `CHANGELOG-D-NGOAI-GOI` · `packet_issue`: #1134 · `revision`: 2. r1 (sha256 `a893990a38c0882a2d909d9a1f487cd147c5de90c48eeb2e84578bc941fa4181`) là nháp chỉ đi review
  offline (lượt 1, `request_changes` 0 P1 / 1 P2 / 1 P3); r2 xử lý cả hai.
- `nguon_cap_viec`: chủ kho (ducthangho), "Cả 2. Land và ghi sổ" trong phiên `session_015GtxraNWSWRDjqY58pqwAN`
  (01-11-2026), sau khi packet #1121 (PR #1125) đỏ selftest vì gói ở trần.
- base `origin/master` = `70ab34e68dff4d886c65d85266dfd6892c19b509`.
- `review_class`: **sensitive** — đổi chính sách đóng gói phát hành (`_RELEASE_EXCLUDE_DIRS`) và ratchet của gate
  `release-verify`/selftest. Executor `claude` · reviewer `codex` ⇒ `cross_approved`.
- `windows`: **required** (ADR-0060 M3 bước 2: fragment test thêm dòng `pathlib`). `full_mutant_audit`: không bắt buộc
  (M9: diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**`).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

## Quyết định của chủ kho (AskUserQuestion, phiên trên, 01-11-2026)
- **Q1** Loại thư mục `changelog.d` khỏi gói bằng `_RELEASE_EXCLUDE_DIRS`; sửa hai ratchet khoá số cứng `== 198` thành **184**
  (giữ khoá số cứng, không đổi sang quan hệ).
- **Q2** KHÔNG hợp nhất 14 fragment vào `CHANGELOG.md` trong packet này — nợ `CHANGELOG-D-CHUA-HOP-NHAT`, ghi trên #1134.
- **Kế thừa** quyết định Q8 của #1121 (`ops/specs/DOC-CLAIMS-XOA-r5.md`): PR worker tái sinh bundle fragment và manifest như cách
  xử lý CHUYỂN TIẾP — protocol §5/§9/§10.2.4 vẫn giao artifact ấy cho land, nhưng `docs/PROTOCOL_DA_PHIEN.md:880` ghi cơ chế
  land chưa bật và `bundle_fragment_check` đòi tập ID nguồn = bundled ngay trên PR. Lease của #1134 phải neo ngoại lệ này.

## Hiện trạng (đo trên base, ~22:40Z 01-11-2026)
- `RELEASE_MANIFEST.json`: `file_count` **198**; 14 mục `changelog.d/*.md` (đơn vị: tệp) — `wp-1009 wp-1030 wp-1038 wp-1052
  wp-710 wp-725 wp-726 wp-727 wp-766 wp-802 wp-831 wp-858 wp-868 wp-886`.
- Trần thật: `wp44_release_bundle_topology_under_200` đòi ZIP < 200 entry = `file_count + 1` ⇒ `file_count` ≤ 198.
- Không consumer CHUYÊN BIỆT nào gọi `changelog.d` theo tên (`rg changelog\.d` trên `scripts/tl_core/*.py`, `scripts/tl.py`,
  `.github/workflows/*.yml`, `.github/checks/*.py` chỉ ra chú thích). Consumer GIÁN TIẾP qua manifest (review r1 F2, đo bằng
  audit hook `open`): `_build_release_manifest` đọc 14 tệp; `_verify_release_manifest` đọc 42 lần / 14 tệp (kiểm con trỏ);
  sau M1 cả hai đọc 0. Golden (20 ca, 0 ca release), kiểm kê Python của golden (73) và `doc_claims_targets` không chứa
  `changelog.d/`; `ci_phamvi` không đổi. Tệp TRONG gói nhắc tới nó: `references/RUNBOOK.md:737,840` (`changelog.d/wp-710.md`)
  và `scripts/tl_selftest.py` (chú thích kê khai slot).
- `scripts/tl_core/release.py:394` `_RELEASE_EXCLUDE_DIRS` (khớp theo TỪNG thành phần đường dẫn, `parts & _RELEASE_EXCLUDE_DIRS`).
- Ratchet khoá số: `scripts/tl_selftest.py:22773` (`r291_docs_ngoai_goi`, `len(paths) == 198`) và `:22833`
  (`r357_agents_ngoai_goi`, cùng phép).
- Mô phỏng trên clone tạm của base (thêm `"changelog.d"` vào tập, tái sinh manifest): `file_count` **184**;
  `release-verify RELEASE_MANIFEST.json --strict` ⇒ `ok=true`, `doc_pointers.pointers_fail` rỗng, `pointers_checked` 329 → 318
  (`_doc_pointer_findings` kiểm con trỏ trỏ vào `references/`, `templates/`, `scripts/` — `changelog.d/` không thuộc ba gốc ấy);
  `tl --selftest` **1773/1775**, chỉ đỏ `r291_docs_ngoai_goi` và `r357_agents_ngoai_goi` (đo trong phiên soạn, ngoài sandbox
  reviewer).
- 14 fragment chưa được hợp nhất vào `CHANGELOG.md` (đếm `rg -c` cho wp-1030/1052/886/710: 0) — chúng vẫn nằm trong git.
- Lease: `ai-dang-giu` (22:45Z, 755/755 nhánh) — `release.py`, `tl_selftest.py`, fragment mới: `NGƯỜI_GIỮ 0`;
  `RELEASE_MANIFEST.json`, `scripts/tl_test_fragments_bundled.py`: `wp1121-r5-g1-claude` (đã rút hạn tới 22:59Z, packet #1121
  đã merge). Đo lại trước khi cấp lease.

## Việc
**M1** (`scripts/tl_core/release.py`) Thêm `"changelog.d"` vào `_RELEASE_EXCLUDE_DIRS`, kèm chú thích theo idiom kho (lý do, số
đo 198 → 184, nơi nợ hợp nhất được ghi). Không đổi luật khác của bộ lọc.
**M2** (`scripts/tl_selftest.py`) Hai ratchet `r291_docs_ngoai_goi`, `r357_agents_ngoai_goi`: `== 198` ⇒ `== 184`, cộng một dòng
kê khai slot nêu packet #1134 và số mới. Không đổi gì khác trong harness.
**M3** (`scripts/test_fragments/wp1134_changelog_d_ngoai_goi.py`, `TEST_ID = "wp1134_changelog_d_ngoai_goi"`, `run(tl_module)`)
Khuôn `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py`. Ca, tất cả qua hàm sản xuất `_release_should_include`
(nhớ: nó kết thúc bằng `path.is_file()`, nên dựng tệp THẬT trong thư mục tạm):
  (a) `changelog.d/wp-1.md` ⇒ KHÔNG vào gói;
  (b) `docs-like/changelog.d/x.md` (thư mục `changelog.d` lồng) ⇒ KHÔNG vào gói (khoá ngữ nghĩa theo thành phần);
  (c) `references/changelog.d.md` (TÊN TỆP, không phải thư mục) ⇒ vẫn VÀO gói nếu tệp cùng dạng ở `references/` vào gói;
  (d) đối chứng: một tệp `references/x.md` ⇒ VÀO gói.
  Tiền điều kiện fail-closed: mọi tệp fixture dựng được và tồn tại. KHÔNG có nhánh bỏ qua: `scripts/tl_core/release.py` là
  required release file nên luôn có mặt cả trong gói đã giải nén (review r1 mục 3) — vắng nó ⇒ FAIL.
**M4** (`scripts/tl_test_fragments_bundled.py`) TÁI SINH bằng `generate_bundled_module_bytes`, không sửa tay (tiền lệ wp1030/#1121).
**M5** (`RELEASE_MANIFEST.json`) TÁI SINH sau M1 + M4; `file_count` phải = **184**. Không bump VERSION, không sửa `CHANGELOG.md`.
**M6** Đặc tả này phải CÓ MẶT tại head thi công để `kiem-merge` K1 đọc được: đi qua PR đặc tả riêng, chủ kho merge trước, rồi
nhánh thi công rẽ từ (hoặc merge) master chứa nó — đúng đường #1121 đã đi (#1123 → merge master vào nhánh). Executor không sửa
tệp đặc tả.

**KHÔNG đổi:** `references/RUNBOOK.md` (con trỏ tới `changelog.d/wp-710.md` vẫn đúng trong kho; xem `chua_do_duoc`); nội dung
`changelog.d/`; `CHANGELOG.md`; `VERSION`; `.github/**`; write set packet C/#1113.

## ngoai_pham_vi
- Hợp nhất 14 fragment vào `CHANGELOG.md` (Q2) — nợ `CHANGELOG-D-CHUA-HOP-NHAT`.
- Đổi ratchet sang dạng quan hệ (Q1 chọn giữ số cứng).

## Write set (diff PR ≤ 5 tệp; ≤ 450 dòng thêm theo `git diff --numstat origin/master...HEAD`)
1. `scripts/tl_core/release.py` 2. `scripts/tl_selftest.py` 3. `scripts/test_fragments/wp1134_changelog_d_ngoai_goi.py`
4. `scripts/tl_test_fragments_bundled.py` (chỉ tái sinh) 5. `RELEASE_MANIFEST.json` (chỉ tái sinh)
Đặc tả không thuộc diff thi công (M6: vào qua PR đặc tả). Handoff `ops/handoff/wp1134-g1-claude.md` trên nhánh lease, không vào diff PR.

## Nghiệm thu (mỗi tiêu chí kèm phép làm nó ĐỎ)
- **N1** CI `ci.yml` trên head cuối: `gate` selftest N/N hai số BẰNG nhau (kỳ vọng 1776/1776 = 1775 + fragment mới), 0 `[FAIL]`,
  gồm `[OK]` cho `r291_docs_ngoai_goi`, `r357_agents_ngoai_goi`, `wp44_release_bundle_topology_under_200`,
  `wp1134_changelog_d_ngoai_goi`. Đỏ khi: D1 bỏ M1 **rồi tái sinh manifest** (manifest về 198) ⇒ r291/r357 đỏ vì 198 ≠ 184, và
  fragment ca (a), (b) đỏ — bỏ M1 mà GIỮ manifest M5 thì r291/r357 vẫn xanh (đọc 184 từ manifest committed; review r1 F1), nên
  phép đo ấy không dùng làm bằng chứng; D2 bỏ M2 ⇒ r291/r357 đỏ vì 184 ≠ 198.
- **N2** Đột biến trên BẢN SAO TẠM (đọc tên ca, không chỉ rc): D3 bỏ `"changelog.d"` khỏi tập ⇒ fragment ca (a), (b) đỏ;
  D4 đổi luật loại sang khớp tiền tố tên (`startswith("changelog.d")`) ⇒ ca (c) đỏ; D5 loại cả `references/` ⇒ ca (d) đỏ;
  D6 không tái sinh bundle ⇒ `bundle_fragment_check` rc≠0 `TEST_ID_SET_MISMATCH`.
- **N3** `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked == 184`,
  không mục `changelog.d/` nào trong manifest. Đỏ khi: bỏ M5.
- **N4** `release-bundle` hai lượt cùng SHA-256, ZIP 185 entry (`file_count + 1`). Đỏ khi (vế số entry): D3 (cho `changelog.d`
  lọt bộ lọc) rồi build lại ⇒ 199 entry ≠ 185. Thêm một tệp vào `changelog.d/` sau M1 KHÔNG làm đỏ (tệp vẫn bị loại — review r1
  F1, đo 184/184, 185/185). Vế tất định đã do bước `release-bundle x2 cùng SHA-256` của CI gác; packet này không thêm đột biến
  riêng cho vế ấy.
- **N5** ruff F delta 0 trên `scripts/tl.py` và các tệp `.py` của write set; `git diff --check` rc 0; `doctrine-scan` rc 0.
- **N6** Windows local (ADR-0057..0059): fragment + `bundle_fragment_check` trên máy chủ kho; ghi sổ đo. `chưa đo được` cho tới khi chạy.
- **N7** `kiem-merge` K0–K7 rc=0 trên head cuối trước khi bỏ draft.

## hinh_dang_ke_thua
Packet khắc phục hệ quả của #1121 (hồ sơ: `ops/specs/DOC-CLAIMS-XOA-r5.md` mục `hinh_dang_ke_thua`). Hình dạng chép sang:
`trai-protocol-noi-dat-test` lần 3 (biến thể "tiền lệ chỉ đúng khi còn khe") — packet này là câu trả lời cho câu hỏi "có nên giữ
cách này" của lần 3. Review r1 của packet này: `phan-chung-khong-lam-do-dung-tieu-chi` (F1, ở #1121 tên `ca-khong-dot-bien` —
cùng họ, lần 3 tính gộp) · `ket-luan-phu-thuoc-tu-grep` (F2, lần 1).

## chua_do_duoc
- Một cài đặt Package ĐÃ có (bản cũ chứa `changelog.d/`) sau khi cập nhật sẽ còn tệp thừa hay không — phụ thuộc cách Cowork bung
  gói; không đo được từ phiên này.
- `references/RUNBOOK.md` trong gói trỏ tới `changelog.d/wp-710.md` sẽ là con trỏ ra ngoài gói; `release-verify` không kiểm loại
  con trỏ này (đo được), người đọc gói cài đặt sẽ không mở được tệp ấy. Không sửa ở packet này.
