tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# BUNDLED-TACH-MANH r1 — tách `scripts/tl_test_fragments_bundled.py` thành nhiều mảnh dưới ngưỡng WARN, GIỮ NGUYÊN bộ canh kích thước

- packet_id: BUNDLED-TACH-MANH; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | **[QUYẾT ĐỊNH Q1 — khuyến nghị: #433]** (packet này mở để gỡ chặn packet SECRETS-SET-BUNDLE-KIEU của #433; TEST_ID fragment mới mang tiền tố `wp433_`). Phương án khác: issue mới, khi ấy đổi tên fragment theo số issue. |
| `nguon_cap_viec` | Chủ kho 2026-11-20 (phiên điều phối #1206): "Tách bundled trước" — packet riêng, làm TRƯỚC secrets-set, giữ nguyên bộ canh (không nâng ngưỡng, không waiver). |
| `phu_thuoc` | Không. Chặn: SECRETS-SET-BUNDLE-KIEU (nhánh `agent/wp433-r8-g1-claude` `a8a3b3c`, đang giữ). |
| `review_class` | `sensitive`: chạm `scripts/tl_core/test_fragments.py` (hợp đồng nạp fragment, chạy trong gói phát hành) và `scripts/tl_core/release.py` (cổng `test-fragments-check` lane LAND). |
| `base` | `0f9aa2a2cc697129e1f5be72feddf60986286865`. Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. Đo trên clone ĐẦY ĐỦ: clone nông làm `wp1099_nlm_nap_lai` đỏ giả (thiếu object `358451e8`). |

Các mục **[QUYẾT ĐỊNH Qn]** ghi phương án KHUYẾN NGHỊ; chủ kho chọn khác thì đặc tả revision trước khi đóng băng.

## 0. Hiện trạng (đo trên `0f9aa2a`)

Bằng chứng ở `ops/reviews/bundled-tach-manh-spec-r1/` (README nêu từng tệp).

- **Bộ canh:** `_py_size_findings` (`scripts/tl_core/workflow.py:732`) WARN > 280 KiB = 286.720 B, FAIL > 320 KiB = 327.680 B; mục đích: trần mount Cowork ~343 KB/tệp
  (cắt cụt). Ca `r125_py_size_guard_wired_in_audit` (`scripts/tl_selftest.py:14716–14735`) đòi `py_size.warn == []`. Bundled là tệp RUNTIME: nằm trong
  `_RELEASE_REQUIRED_FILES` (`scripts/tl_core/release.py:486`) và được `load_runtime_fragment_cases` đọc trong gói ⇒ lý do của bộ canh áp đúng cho nó.
- **Kích thước:** bundled 285.112 B (18 fragment, 285.000 B dòng nguồn); dư 1.608 B trước WARN. Lớn nhất: `wp433_gws_cred_dich_ngoai_kho.py` 35.219 B,
  nhỏ nhất `wp45_fragment_canary.py` 245 B. Fragment secrets-set (15,7 KB) ⇒ 300.798 B ⇒ WARN ⇒ r125 đỏ. Mọi fragment mới đều vượt.
- **Điểm chạm** (rg toàn kho, trừ `ops/land`, `ops/reviews`):
  - `scripts/tl_core/test_fragments.py`: `_BUNDLED_MODULE_NAME` (31), `_read_bundled_sources` (353–400, hợp đồng data-only MỘT phép gán
    `BUNDLED_FRAGMENT_SOURCES`), `_compile_bundled_entries`, `discover_bundled_test_ids`, `load_bundled_fragment_cases`, `_runtime_fragment_topology` (dev nếu có
    `scripts/test_fragments/` không rỗng, ngược lại bundle), `generate_bundled_module_bytes` (464).
  - `scripts/tl_core/release.py`: `_test_fragments_check` (206–255, so byte MỘT tệp), `_RELEASE_REQUIRED_FILES` (486).
  - `.github/checks/bundle_fragment_check.py`: chỉ gọi `load_runtime_fragment_cases` trong gói giải nén + `has_bundled_module` (tệp chính) — không đổi.
  - `.githooks/eol_policy_test.py`: `_tai_sinh_bundled` (884–887) và `case_…driver` (976–979) ghi bundled từ fragment THẬT bằng
    `generate_bundled_module_bytes` ⇒ phải ghi đủ mảnh. Các ca khác (934, selftest 31884–32090, `wp47`) dùng thư mục fixture nhỏ ⇒ một mảnh, byte y hệt nay.
  - `references/golden/workflow_audit.json:1196` `files_scanned: 73` ⇒ thêm một tệp `.py` thành 74.
  - `.claude/dev/gate_lifecycle.py:73` `_CATALOG_POLICY_PATHS` chứa đường bundled (dev-side, chỉ băm chính sách) — xem §2.
  - Tài liệu: `references/COMMANDS.md:60`, `docs/PROTOCOL_DA_PHIEN.md`, ADR-0031, nhiều `ops/specs/*` nhắc tên tệp — xem §2.
  - Trần gói 200 tệp: hiện 185; +1 mảnh ⇒ 186.

## 1. `write_set`

```
.githooks/eol_policy_test.py
references/golden/workflow_audit.json
scripts/test_fragments/wp433_bundled_tach_manh.py
scripts/tl_core/release.py
scripts/tl_core/test_fragments.py
scripts/tl_test_fragments_bundled.py
scripts/tl_test_fragments_bundled_2.py
```

**7 tệp > trần 6 của ADR-0053 ⇒ [QUYẾT ĐỊNH Q2 — khuyến nghị: nâng trần lên 7 tệp, 450 dòng giữ nguyên] (E2).** Không gộp được: golden phải đổi vì
`files_scanned`; `eol_policy_test` phải đổi vì hai ca ghi bundled từ fragment thật. Hai tệp bundled CHỈ sinh bằng `write_bundled_modules(scripts/test_fragments,
scripts)` (M1), không sửa tay. KHÔNG `RELEASE_MANIFEST.json` (PR manifest sau land). **Điều kiện cấp lease (E2):** comment chủ kho trên #433 cấp ngoại lệ
bundled nêu đúng `packet_id` `BUNDLED-TACH-MANH`, hai tệp bundled, sha256 đặc tả đã đóng băng, và trần đã nâng.

## 2. `ngoai_pham_vi`

- Không đổi ngưỡng, waiver hay vị từ của `_py_size_findings`; không sửa `r125_*` hay `scripts/tl_selftest.py`.
- Không sửa `.github/checks/bundle_fragment_check.py`, `scripts/tl.py`, `_RELEASE_REQUIRED_FILES` (chỉ tệp chính là bắt buộc; mảnh được `test-fragments-check`
  canh), `.claude/dev/gate_lifecycle.py` (đề xuất nợ riêng nếu muốn băm cả mảnh), tài liệu `references/COMMANDS.md` / `docs/**` / ADR (nợ tài liệu riêng:
  `bundled-tach-manh-tai-lieu`).
- Không đổi thứ tự, nội dung hay số fragment hiện có.

## 3. `muc_tieu` (nguyên văn nguyên mẫu ở `ops/reviews/bundled-tach-manh-spec-r1/nguyen-mau.diff`)

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **Sinh mảnh.** `generate_bundled_modules(root) -> tuple[(tên, bytes), …]`: xếp fragment theo thứ tự ổn định hiện có, gom tham lam, mảnh mới khi tổng byte dòng nguồn vượt `_BUNDLED_SHARD_LIMIT` **[QUYẾT ĐỊNH Q3 — khuyến nghị: 192 KiB = 196.608 B ≈ 68,6% WARN]** (một fragment đơn lớn hơn hạn vẫn đứng riêng một mảnh). Mảnh 1 tên `tl_test_fragments_bundled.py`; mảnh k≥2 tên `tl_test_fragments_bundled_<k>.py`. Khi >1 mảnh, mảnh 1 thêm đúng MỘT phép gán `BUNDLED_FRAGMENT_SHARDS = ("tl_test_fragments_bundled_2.py", …)` sau `BUNDLED_FRAGMENT_SOURCES`; khi 1 mảnh, byte Y HỆT `generate_bundled_module_bytes` hiện nay. `generate_bundled_module_bytes(root)` giữ chữ ký, trả bytes mảnh 1. `write_bundled_modules(root, scripts_dir)` ghi mọi mảnh và XOÁ mảnh đánh số lạc; là đường tái sinh duy nhất được phép. | `test_fragments.py` |
| M2 | **Nạp mảnh.** `_read_bundled_sources(primary)` đọc mảnh 1 rồi ĐÚNG các mảnh mảnh 1 khai trong `BUNDLED_FRAGMENT_SHARDS`, theo thứ tự khai; tệp đánh số không khai thì KHÔNG nạp. Hợp đồng mỗi mảnh vẫn data-only: mảnh 1 cho phép `[SOURCES]` hoặc `[SOURCES, SHARDS]`; mảnh k≥2 chỉ `[SOURCES]`. Danh sách khai phải là `("…_2.py", …, "…_N.py")` liên tục, không rỗng. Thứ tự và tính duy nhất (NFC+casefold) kiểm XUYÊN mảnh. Mảnh khai mà thiếu ⇒ `BUNDLED_MODULE_MISSING` (mã lỗi giữ nguyên, kèm đường mảnh). | `test_fragments.py` |
| M3 | **Cổng `test-fragments-check`.** So từng mảnh kỳ vọng theo byte, cộng phát hiện tệp `tl_test_fragments_bundled_<k>.py` lạc trên đĩa (`extra_shards`) ⇒ `GENERATED_BUNDLE_STALE`. Thiếu mảnh 1 ⇒ `BUNDLED_MODULE_MISSING` như nay. Một mảnh: `expected_sha256`/`actual_sha256`/`*_bytes` giữ nguyên nghĩa (băm tệp). Nhiều mảnh: băm trên chuỗi `tên\0bytes` nối theo thứ tự. Thêm khoá `shards`. | `release.py` |
| M4 | `eol_policy_test.py`: hai chỗ ghi bundled từ fragment thật (`_tai_sinh_bundled`, ca driver) đổi sang `write_bundled_modules`. | `.githooks/eol_policy_test.py` |
| M5 | Golden `workflow_audit.json`: `files_scanned` 73 → 74; không khoá nào khác đổi (`golden-test` ok). | golden |
| M6 | Fragment `wp433_bundled_tach_manh.py`, 8 nhãn (§4). Fragment KHÔNG được văng ngoại lệ dưới đột biến: mọi chỉ số/độ dài phải chốt trước khi dùng (đột biến c lần đầu văng `IndexError` ⇒ tín dụng giả; đã thêm chốt). | fragment |
| M7 | Tái sinh bằng `write_bundled_modules`; ra đúng hai mảnh trên base (mảnh 1 ≈ 189 KB, mảnh 2 ≈ 102 KB). | bundled |

## 4. `nghiem_thu`

| # | ca | tiêu chí | đỏ khi |
|---|---|---|---|
| N1 | fragment mới | `run()` True; 8 nhãn True: `mot_manh` (1 mảnh, không dòng SHARDS, = `generate_bundled_module_bytes`), `nhieu_manh` (hạn 100 KiB, 6×40 KiB ⇒ ≥3 mảnh, nạp đủ đúng thứ tự, mảnh 1 khai), `manh_lac` (tệp `_9` không khai: loader bỏ qua, cổng `GENERATED_BUNDLE_STALE` + `extra_shards == ["tl_test_fragments_bundled_9.py"]`), `ghi_xoa_lac`, `thieu_manh` (`BUNDLED_MODULE_MISSING`), `thu_tu_xuyen_manh` (đổi chỗ mảnh 2/3 ⇒ `BUNDLED_MODULE_CONTRACT`), `manh_tu_khai` (mảnh k≥2 có SHARDS ⇒ `BUNDLED_MODULE_CONTRACT`), `kho_that` (`_BUNDLED_SHARD_LIMIT ≤ 0,7·WARN`, mọi mảnh thật ≤ WARN). | nhãn nào khác True |
| N2 | đột biến (§4b) | 6/6 đỏ ĐÚNG nhãn đích, `run()` trả False (không văng). | sống, hoặc chết do ngoại lệ |
| N3 | gate trên head, clone đầy đủ | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1784, nguyên mẫu 1785); `test-fragments-check` `ok: true` hai mảnh; `bundle_fragment_check` `ok: true`, `failed: []`, `case_count` 19; `release-manifest` tạm + `release-verify --strict` ok, `expected == checked` = 186; `workflow-audit` `py_size.warn == []`, `files_scanned` 74; `golden-test` ok; `.githooks/eol_policy_test.py` 32/32 (trên cây ĐÃ commit); ruff F delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0. | bất kỳ vế nào |
| N4 | phản chứng mục đích | Áp `scripts/test_fragments/wp433_secrets_set_bundle.py` + `scripts/tl_gws.py` của `origin/agent/wp433-r8-g1-claude` lên head, `write_bundled_modules`: `py_size.warn == []`, `test-fragments-check` ok, selftest N/N (đo nguyên mẫu: 1786/1786, mảnh 189.145 / 117.343 B). Không commit phần áp. | còn WARN |

### 4b. Đột biến (đã đo trên nguyên mẫu, `dot-bien.txt`)

| # | đột biến | nhãn đỏ |
|---|---|---|
| a | loader nạp mọi `tl_test_fragments_bundled_*.py` trên đĩa, bỏ qua khai báo | `manh_lac`, `thieu_manh` |
| b | bỏ kiểm thứ tự xuyên mảnh | `thu_tu_xuyen_manh` |
| c | generator bỏ hạn mảnh (một mảnh) | `nhieu_manh` |
| d | cổng bỏ `extra_shards` | `manh_lac` |
| e | `write_bundled_modules` không xoá mảnh lạc | `ghi_xoa_lac` |
| f | mảnh k≥2 được đọc như mảnh 1 (cho phép SHARDS) | `manh_tu_khai` |

### 4c. Đo native Windows

**[QUYẾT ĐỊNH Q4 — khuyến nghị: miễn]** Mã chỉ là `pathlib` iterdir/write/unlink và AST/JSON; không API riêng nền, không ký tự đường đặc biệt. Nếu chủ kho
muốn: một lượt D1 nhẹ trên Desktop — chạy fragment mới và `test-fragments-check` trên clone exact head (`git -c core.longpaths=true`), kỳ vọng như N1.

## 5. `pham_vi_e`

Không chạm E4/E5: thư mục tạm, không mạng, không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex theo ADR-0055; trần kích thước ADR-0053 (sau Q2) đo bằng numstat thật; vượt ⇒ DỪNG.
- §0 lệch trên base thật (kích thước bundled, `files_scanned`, các điểm chạm) ⇒ DỪNG, revision.
- Một mảnh bất kỳ trên head > 0,7·WARN, hoặc số mảnh trên base ≠ 2 ⇒ DỪNG, báo (Q3 sai giả định).
- Bất kỳ ca selftest nào khác ngoài +1 ca mới đổi trạng thái ⇒ DỪNG.
- Đo trên clone nông ⇒ KHÔNG ĐO ĐƯỢC cho N3, không được báo đạt.
- Chưa có comment ngoại lệ bundled đúng `packet_id` + trần nâng ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm (ADR-0067, **E2**).

## 7. `hinh_dang_ke_thua` và hệ quả cho packet khác

- **Ranh mảnh trôi:** gom tham lam theo thứ tự tên ⇒ thêm một fragment ở giữa thứ tự có thể đẩy fragment sang mảnh sau, đổi CẢ HAI tệp. Vì vậy từ packet này,
  mọi packet thêm/sửa fragment phải khai write set gồm MỌI tệp `scripts/tl_test_fragments_bundled*.py` (kể cả mảnh mới có thể sinh), và ngoại lệ bundled phải
  nêu cả nhóm tệp, sinh bằng `write_bundled_modules` (không còn `generate_bundled_module_bytes`).
- **SECRETS-SET-BUNDLE-KIEU cần revision r2 sau khi packet này land:** fragment `wp433_secrets_set_bundle.py` rơi vào mảnh 2 (đo N4) ⇒ write set thêm
  `scripts/tl_test_fragments_bundled_2.py` (4 tệp), ngoại lệ bundled mới, lease mới; nhánh `a8a3b3c` phải merge master mới rồi tái sinh bằng
  `write_bundled_modules`. Mã `tl_gws.py` và fragment của nó không đổi.

## 8. `chua_do_duoc` và dự toán

- Numstat nguyên mẫu (đo, base `0f9aa2a`, bundled tái sinh bằng `write_bundled_modules`): `eol_policy_test.py` 2/4 · golden 1/1 · fragment mới 130/0 ·
  `release.py` 22/5 · `test_fragments.py` 90/26 · `tl_test_fragments_bundled.py` 2/9 · `tl_test_fragments_bundled_2.py` 14/0 ⇒ **7 tệp, 261 dòng thêm, 45 xoá**.
- Chưa đo: Windows (Q4); `RELEASE_MANIFEST.json` lane LAND (PR manifest sau land, 186 tệp).

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: secrets-set bị chặn bởi WARN bundled ⇒ chọn "Tách bundled trước" (không nâng ngưỡng, không waiver, không đưa test ra ngoài bundle).
- Q1–Q4 chờ chủ kho (đầu tệp và §1, §3, §4c).

## 10. Nhật ký revision

- 2026-11-20T15:1xZ (phiên con của điều phối #1206): bản 1, đo §0 và nguyên mẫu trên clone đầy đủ `0f9aa2a` (Linux).
