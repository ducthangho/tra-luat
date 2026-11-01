# Đặc tả packet DOC-CLAIMS-XOA r3 — `doc-claims-check` cờ trích dẫn tới tệp ĐÃ XOÁ trong tài liệu sống

Đặc tả đóng băng. Muốn đổi thì soạn `DOC-CLAIMS-XOA-r4.md`, không sửa đè.
Đặc tả KHÔNG cấp việc: cần Packet Issue #1121 + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).
Chỗ nào đặc tả không nói, executor DỪNG và hỏi trên #1121 — không tự nới.

- `packet_id`: `DOC-CLAIMS-XOA` · `packet_issue`: #1121 · `revision`: 3. r1 (sha256 `d712e3c9c61f9313b4232d00a255d3c659db55717f06a381cf7a082bf7421be9`)
  và r2 (sha256 `ba79394d368917f24f5c012d4f00c0eca919fe065c439709e9d0350c9b2ab9ad`) là nháp chỉ đi review offline, không lên
  kho. r2 xử lý 7 finding của lượt 1; r3 xử lý 4 finding của lượt 2 (R2-F1…F4).
- `nguon_cap_viec`: chủ kho (ducthangho) giao qua phiên packet #1113 `CI-LAN-LUU-TRU` r1 (01-11-2026): lỗ "DO6" trên ĐƯỜNG
  ĐẦY ĐỦ của CI. #1113 tự chặn cùng ca ở đường NHANH (`kiem_xoa_bi_trich`, `ops/ci_duong_nhanh.py`).
- base `origin/master` = `f4b513da5802d439aedbe58ae4a5cd38ff47d6ab`.
- `review_class`: **sensitive** — đổi hành vi bước gate CI `doc-claims-check strict` (job `gate`, `.github/workflows/ci.yml`),
  tức gate lifecycle (§8). Executor `claude` · reviewer `codex` ⇒ `cross_approved`.
- `windows`: **required** (ADR-0060 M3 bước 2: fragment test thêm dòng `subprocess`; chủ kho chốt). `full_mutant_audit`:
  không bắt buộc (M9: diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**`).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

Lời gọi Codex đã dùng lúc đóng băng: **2** (review offline r1, r2). Dự kiến tổng ≤ 4. Trước MỖI lời gọi: đếm lại.

## Quyết định của chủ kho (AskUserQuestion, phiên `session_015GtxraNWSWRDjqY58pqwAN`, 01-11-2026)
- **Q1** Tài liệu KHÔNG lịch sử trích tệp đã xoá ⇒ CỜ; tài liệu lịch sử ⇒ advisory.
- **Q2** Phạm vi `docs/`: tiền đề câu hỏi SAI — `_DOC_CLAIMS_DEFAULT_PATHS` (`scripts/tl_core/workflow.py:817`) ĐÃ có `"docs"`
  từ r264, selftest `scripts/tl_selftest.py:29227` khoá. Không còn việc; đã báo lại chủ kho.
- **Q3** `docs/adr/` là tài liệu SỐNG (đã khoá sẵn bởi selftest r264 `ok5`, `scripts/tl_selftest.py:29265`).
- **Q4** Theo protocol §5 (`docs/PROTOCOL_DA_PHIEN.md:355–356`, `:874–878`): worker KHÔNG sửa `VERSION`, hằng version trong
  `scripts/tl.py`, header `SKILL.md`, `CHANGELOG.md`, `RELEASE_MANIFEST.json`. Bỏ `nang_tran` của r1 (3 tệp nằm trong trần
  ADR-0053). Bản giao việc gốc đòi bump — trái protocol, protocol thắng.
- **Q5** Mã lý do: tài liệu sống ⇒ `PATH_DELETED` thành CỜ; lịch sử ⇒ mã MỚI `PATH_DELETED_IN_HISTORICAL_DOC` (advisory).
- **Q6** F1 (gốc thư mục đã mất; token `./`, `../`) NGOÀI phạm vi — khai nợ. F2 (biên tiền tố của `_DOC_CLAIMS_HISTORICAL`)
  SỬA trong packet này.
- **Q7** Khai `dieu_kien_merge: ADR-0060`, Windows `required`.

## Hiện trạng (đo trên base, clone ĐỦ lịch sử, `core.abbrev=7`, ~16:00Z 01-11-2026; review r1 đo lại khớp)
- L1 (`scripts/tl_core/workflow.py:1206–1213`): đường dẫn hụt thuộc `_doc_claims_deleted_set(ctx)` (`git log --diff-filter=D`)
  ⇒ `PATH_DELETED` advisory, **bất kể** tài liệu. Nhánh `historical` (`:1210`) chỉ xét cho đường dẫn KHÔNG thuộc tập xoá.
- `historical = rel.startswith(_DOC_CLAIMS_HISTORICAL)` (`:1169`) và `src.startswith(_DOC_CLAIMS_HISTORICAL)` (`:1414`): khớp
  tiền tố cả với mục là TÊN TỆP ⇒ `CHANGELOG.md.live.md` được coi là lịch sử (review r1 F2, đo bằng hàm sản xuất).
- Tái hiện lỗ (clone `--no-local` tại base): `git rm ops/RUT_LEASE_PLAT_X8_20260821.md ops/land/pr909-wp748-r25-land-evidence.yaml`
  — chưa commit ⇒ rc=2 (`PATH_MISSING`); đã commit ⇒ **rc=0**.
- Nền mặc định: rc=0, 6 gốc / 120 tệp, `flags` 0, **3** advisory `PATH_DELETED` (đơn vị: phát hiện), cả 3 ở tài liệu lịch sử
  (`CHANGELOG.md:9628`, `:9657`; `references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md:2294`). Chỉ `docs/`: 0 phát hiện
  `PATH_DELETED`.
- Đổi luật lịch sử sang "mục kết thúc `/` = tiền tố thư mục, còn lại = bằng chính xác": trên `git ls-files` của base,
  **0** tệp đổi phân loại, **6** tệp lịch sử.
- Kho nông: lịch sử bị cắt có thể THIẾU sự kiện xoá (không phải luôn rỗng — review r1 F7 đo được ranh giới nông còn 2 sự kiện).
  Với token đã qua bộ lọc L1, sự kiện thiếu ⇒ tài liệu sống ra `PATH_MISSING` (cờ), tài liệu lịch sử ra
  `PATH_MISSING_IN_HISTORICAL_DOC` (advisory) — review r2 F3 đo bằng `ctx["_deleted"]=set()`. CI dùng `fetch-depth: 0`.
- Không ca selftest/golden/tài liệu nào chứa chuỗi `PATH_DELETED` (`rg` trên `scripts/tl_selftest.py`, `references/`, `docs/`).
  Fixture `references/golden/doc_claims_check_fixture.json` không có ca xoá ⇒ không cần ghi lại golden.
- Selftest nền: `tl selftest 1774/1774`.
- Lease: `ops/lease_publish.py ai-dang-giu` cho `scripts/tl_core/workflow.py` ⇒ `NGƯỜI_GIỮ 0`; quét 743/743 nhánh. Hai tệp mới
  chưa tồn tại. Đo lại trước khi cấp lease.

## Việc
**M1** (`scripts/tl_core/workflow.py`) Thêm hàm `_doc_claims_is_historical(rel: str) -> bool`: mục của `_DOC_CLAIMS_HISTORICAL`
kết thúc bằng `/` ⇒ `rel.startswith(mục)`; ngược lại ⇒ `rel == mục`. Thay CẢ HAI chỗ `startswith(_DOC_CLAIMS_HISTORICAL)`
(`:1169`, `:1414`) bằng hàm này. Không đổi nội dung `_DOC_CLAIMS_HISTORICAL`.
Hệ quả CHẤP NHẬN (review r2 mục 4, là hệ quả của Q6 chứ không phải việc thêm): `:1169` cấp `historical` cho L1, L2, L4, L8, L12;
`:1414` thuộc L9. Một tệp hậu tố kiểu `references/DOCTRINE_APPENDIX.md.live.md` trước bị coi là lịch sử ở MỌI lớp, nay là tài
liệu sống ở mọi lớp (advisory L2/L4/L8/L12 thành cờ; L9 thôi tính nó là nguồn lịch sử). Trên nền: 0 tệp đổi phân loại, và
mô phỏng M1+M2 cho phát hiện ngoài L1 BẰNG HỆT base (flags và advisories) — N4 đo lại vế này.
**M2** (`scripts/tl_core/workflow.py`, L1) Đường dẫn hụt thuộc tập đã xoá: `historical` ⇒ advisory `PATH_DELETED_IN_HISTORICAL_DOC`;
ngược lại ⇒ CỜ `PATH_DELETED` (không `advisory`). Mọi nhánh khác của L1 giữ nguyên. Không đổi `_DOC_CLAIMS_DEFAULT_PATHS`,
`_doc_claims_deleted_set`, các lớp L2–L12. Sửa chú thích/docstring nào đang nói `PATH_DELETED` là advisory.
**M3** (`scripts/test_fragments/wp1121_doc_claims_xoa.py`, `TEST_ID = "wp1121_doc_claims_xoa"`, hàm `run(tl_module)` trả bool,
theo khuôn `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py`). Dựng kho git THẬT trong thư mục tạm, gọi
`tl_module._doc_claims_check(root=…)`. Fixture:
  - một tệp được TRACK cố định dưới `ops/` (vd `ops/giu.md`) để gốc `ops` còn sống sau khi xoá; `ops/x.md` commit rồi `git rm`
    + commit;
  - `CONTEXT.md`, `CHANGELOG.md`, `docs/adr/0001-t.md`, `references/DOCTRINE_APPENDIX.md.live.md`,
    `references/changelog_archive/c.md` đều trích `` `ops/x.md` ``; `CONTEXT.md` trích thêm `` `ops/chua-tung-co.md` ``
    (chưa từng tồn tại). (r2 dùng `CHANGELOG.md.live.md` ở gốc — tệp ấy KHÔNG thuộc phạm vi quét mặc định vì tệp gốc được
    chọn theo tên cố định; review r2 F1. Tệp dưới `references/` được quét đệ quy, và theo luật CŨ nó khớp tiền tố
    `references/DOCTRINE_APPENDIX.md` nên là ca biên đúng của F2.)
  Phạm vi so: CHỈ phát hiện lớp `L1` (gộp `flags` + `advisories`, lọc `layer == "L1"`), so theo TẬP bộ ba
  `(file, reason, là_advisory)`. KHÔNG dùng `ok`/rc làm bằng chứng — kho tạm thiếu chỉ mục test-ID nên L12 cờ
  `TEST_ID_INDEX_UNAVAILABLE` (review r1 F5); khai rõ điều này trong docstring. Kỳ vọng:
  (a) `CONTEXT.md` ⇒ `PATH_DELETED` cờ; (b) `CHANGELOG.md` ⇒ `PATH_DELETED_IN_HISTORICAL_DOC` advisory;
  (c) `docs/adr/0001-t.md` ⇒ `PATH_DELETED` cờ; (d) `CONTEXT.md` / `ops/chua-tung-co.md` ⇒ `PATH_MISSING` cờ;
  (e) `references/DOCTRINE_APPENDIX.md.live.md` ⇒ `PATH_DELETED` cờ; (f) `references/changelog_archive/c.md` ⇒ `PATH_DELETED_IN_HISTORICAL_DOC` advisory.
  Kèm tiền điều kiện: `ops/x.md` ∈ `_doc_claims_deleted_set` của kho tạm, `ops` ∈ `toplevel`, và MỖI tài liệu của
  (a)–(f) thuộc tập tệp mà `_doc_claims_targets(None, kho_tạm)` trả về — sai thì FAIL có thông báo nêu tên tài liệu (không
  trả True). Ca vắng phát hiện vì tài liệu không được quét phải ĐỎ ở tiền điều kiện, không được lẫn vào phép so. Không dựng được fixture (git thiếu, lệnh git rc≠0) ⇒ FAIL, không BỎ QUA. Chỉ được BỎ QUA khi theo đúng
  điều kiện topo phát hành của wp1030 (gốc không có `.git` và chính sách phát hành loại thứ cần thiết) — nếu không áp được thì
  không có nhánh BỎ QUA.
**M4** (`changelog.d/wp-1121.md`) Mô tả thay đổi theo khuôn `changelog.d/wp-1030.md`: đã đo gì, chưa đo gì (F1).

**KHÔNG đổi:** `VERSION`, `scripts/tl.py`, `SKILL.md`, `CHANGELOG.md`, `RELEASE_MANIFEST.json`, `scripts/tl_selftest.py`,
`references/golden/**`, `.github/workflows/ci.yml`; write set #1113 (`ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`,
`ops/lease_publish_test.py`, `ops/cong_cu_test.py`, `.claude/dev/ci_dang_ky_test.py`); write set packet C
(`.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`, `docs/adr/0060-…`, `docs/PROTOCOL_DA_PHIEN.md`,
`.claude/skills/land-packets/SKILL.md`). KHÔNG deploy Package.

## ngoai_pham_vi
- **F1** (review r1): L1 bỏ token TRƯỚC khi tra tập xoá khi (i) đoạn đầu không thuộc `toplevel` (gốc đã mất hẳn, vd
  `references/DEV_TOOLING_GUIDE.md:56` → `gas-project/Code.gs`, xoá ở `c8af1d4`); (ii) token `./x`, `../x` bị `strip` mất dấu
  chấm; (iii) đường dẫn tương đối mà đoạn đầu không thuộc `toplevel`. Ước lượng bằng bộ quét nháp: mở rộng ⇒ 1 trích dẫn sống
  đỏ trên nền. Lý do để ngoài: đổi lớp NHẬN DIỆN có rủi ro báo giả (đường dẫn trong DOCX, cache cục bộ) và cần sửa thêm tài
  liệu. Nợ: `DOC-CLAIMS-XOA-F1-GOC-MAT`, ghi trên #1121.
- Rename: `--diff-filter=D` không bắt tên cũ của một lần đổi tên; trích tên cũ trong tài liệu sống vẫn bị cờ `PATH_MISSING`
  (đo r1). Không đổi.

## Write set (diff PR ≤ 3 tệp; ≤ 450 dòng thêm theo `git diff --numstat origin/master...HEAD`)
1. `scripts/tl_core/workflow.py` 2. `scripts/test_fragments/wp1121_doc_claims_xoa.py` 3. `changelog.d/wp-1121.md`
Đặc tả này vào qua PR đặc tả riêng. Handoff/verdict trên nhánh lease, không vào diff PR thi công.

## Nghiệm thu (mỗi tiêu chí kèm phép làm nó ĐỎ)
- **N1** `python scripts/tl.py --selftest` N/N, hai số BẰNG nhau, trên đúng commit sẽ đẩy; fragment `wp1121_doc_claims_xoa`
  được auto-discover và ĐẠT (ghi dòng output chứng minh nó chạy). Trên base fragment chưa tồn tại; chạy fragment trên mã base
  ⇒ phải FAIL (ghi tên ca đỏ). Đỏ khi: các đột biến N2.
- **N2** Đột biến trên BẢN SAO TẠM, mỗi cái đọc TÊN ca (a)–(f) bị lệch trong thông báo FAIL, không chỉ rc. Baseline (không đột
  biến) phải ĐẠT trước:
  D1 khôi phục `advisory=True` cho `PATH_DELETED` ở tài liệu sống ⇒ (a), (c), (e) lệch;
  D2 bỏ phân nhánh `historical` ở M2 (mọi tài liệu ⇒ cờ) ⇒ (b), (f) lệch;
  D3 thêm `"docs/adr/"` vào `_DOC_CLAIMS_HISTORICAL` ⇒ (c) lệch (selftest r264 cũng đỏ; vẫn đòi fragment đỏ đúng (c));
  D4 khôi phục `startswith` cho mọi mục trong `_doc_claims_is_historical` ⇒ (e) lệch (thành advisory `PATH_DELETED_IN_HISTORICAL_DOC`);
  D5 so bằng chính xác cho mọi mục (bỏ nhánh `/`) ⇒ (f) lệch;
  D6 đổi `PATH_MISSING` ở tài liệu sống thành advisory ⇒ (d) lệch (review r1 F3);
  D7 xoá tệp giữ `ops/giu.md` khỏi fixture ⇒ fragment FAIL ở tiền điều kiện `toplevel`, không ĐẠT;
  D8 đổi tài liệu (e) về `CHANGELOG.md.live.md` ở gốc ⇒ fragment FAIL ở tiền điều kiện targets (khoá review r2 F1).
- **N3** Tái hiện lỗ (vế dương mới / vế âm cũ): clone head, `core.abbrev=7`, `git rm` + commit hai tệp ở mục Hiện trạng ⇒
  `doc-claims-check --strict --json` **rc=2** với cờ `PATH_DELETED` cho trích dẫn ở `CLAUDE.md` và ở
  `docs/adr/0055-tran-loi-goi-codex-len-muoi.md`; cùng phép trên base ⇒ rc=0. Đỏ khi: D1.
- **N4** Nền không vỡ: head sạch, clone đủ lịch sử, `core.abbrev=7` ⇒ `doc-claims-check --strict --json` rc=0, `flags` 0,
  advisory `PATH_DELETED_IN_HISTORICAL_DOC` = 3, advisory `PATH_DELETED` = 0 (đếm phát hiện; đo lại lúc thi công, lệch thì ghi
  số mới + lý do). Đỏ khi: D2 (3 cờ trong CHANGELOG/archive).
- **N5** `python -m ruff check --select F scripts/tl.py` và trên hai tệp `.py` của write set: DELTA so base = 0 (ruff 0.15.15,
  base đo cùng phiên). `git diff --check` rc 0. `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0.
  Lane WORKER (`.github/workflows/ci.yml`, bước `release-verify strict (lane WORKER — manifest TẠM ngoài repo)`): chạy ĐÚNG ba
  lệnh của bước ấy tại chỗ — `release-manifest --root . --out <tạm ngoài repo>`, `release-verify <tạm> --root . --strict
  --json`, và kiểm mọi đường dẫn trong manifest tạm đều được `git ls-files` theo dõi ⇒ cả ba rc=0. Đỏ khi: để một tệp
  untracked trong cây đóng gói (lệnh 3 rc=1), hoặc xoá tạm `references/API_CONTRACT.md` (lệnh 1 rc=2). KHÔNG dùng
  `RELEASE_MANIFEST.json` committed: `scripts/tl_core/workflow.py` NẰM trong manifest (`RELEASE_MANIFEST.json:930`), nên
  M1/M2 tất yếu làm lane LAND lệch sha — review r2 F2. Tái sinh manifest là việc của phiên land (protocol §5), worker
  không sửa. Ghi kết quả `release-verify RELEASE_MANIFEST.json --strict` trên head chỉ để đối chiếu: kỳ vọng `failed` đúng
  MỘT đường dẫn `scripts/tl_core/workflow.py` (bundle fragment do phiên land sinh, chưa đổi ở worker).
- **N6** Windows (ADR-0060 M3): selftest + N3 chạy trên máy Windows của chủ kho qua Desktop Commander theo ADR-0057/0058/0059;
  ghi sổ đo. Trạng thái `chưa đo được` cho tới khi chạy thật.
- **N7** CI lượt PR xanh trên head cuối, đọc bằng check run từng job (`gate` có bước `doc-claims-check strict`).

## hinh_dang_ke_thua
`khong_ap_dung` — không phải packet khắc phục của packet đã land. Lớp lỗi review r1 (để lượt sau đếm):
`tien-de-sai-pham-vi` (Q2) · `bien-nhan-dien-truoc-tra-cuu` (F1) · `khop-tien-to-ten-tep` (F2) · `ca-khong-dot-bien` (F3) ·
`guard-khong-doc-du-nguon` (F4, hết hiệu lực do Q4) · `fixture-do-sai-lop` (F5) · `trai-protocol-noi-dat-test` (F6) ·
`khai-qua-rong` (F7). Review r2: `fixture-do-sai-lop` lần 2 (R2-F1, tài liệu ngoài phạm vi quét) ·
`tieu-chi-sai-hop-dong-lane` (R2-F2) · `khai-qua-rong` lần 2 (R2-F3) · `khoang-trang-cuoi-dong` (R2-F4).
Hình dạng lặp lần 2: `fixture-do-sai-lop`, `khai-qua-rong` — tới lần 3 thì hỏi lại có nên giữ cách dựng fixture/lời khai này.

## chua_do_duoc
- PR/nhánh đang mở nào xoá một tệp mà tài liệu sống còn trích sẽ ĐỎ sau khi land — đúng mục đích; số lượng lúc land chưa đo.
- Windows (N6) cho tới khi chủ kho chạy.
- F1: số trích dẫn sống bị bỏ qua chỉ là ước lượng của bộ quét nháp (1), chưa đo bằng mã sản xuất.
