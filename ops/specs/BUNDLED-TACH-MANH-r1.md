tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# BUNDLED-TACH-MANH r1 — tách `scripts/tl_test_fragments_bundled.py` thành nhiều mảnh dưới ngưỡng WARN, GIỮ NGUYÊN bộ canh kích thước

- packet_id: BUNDLED-TACH-MANH; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | **#433** (Q1, chủ kho chốt 2026-11-20). Packet này mở để gỡ chặn packet SECRETS-SET-BUNDLE-KIEU của #433; TEST_ID fragment mới mang tiền tố `wp433_`. |
| `nguon_cap_viec` | Chủ kho 2026-11-20 (phiên điều phối #1206): "Tách bundled trước" — packet riêng, làm TRƯỚC secrets-set, giữ nguyên bộ canh (không nâng ngưỡng, không waiver). |
| `phu_thuoc` | Không. Chặn: SECRETS-SET-BUNDLE-KIEU (nhánh `agent/wp433-r8-g1-claude` `a8a3b3c`, đang giữ). |
| `review_class` | `sensitive`: chạm `scripts/tl_core/test_fragments.py` (hợp đồng nạp fragment, chạy trong gói phát hành) và `scripts/tl_core/release.py` (cổng `test-fragments-check` lane LAND). |
| `base` | `0f9aa2a2cc697129e1f5be72feddf60986286865`. Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. Đo trên clone ĐẦY ĐỦ: clone nông làm `wp1099_nlm_nap_lai` đỏ giả (thiếu object `358451e8`). |

Các quyết định Q1–Q6 đã được chủ kho chốt 2026-11-20 (xem §9); mỗi chỗ ghi kèm nhãn Qn.

## 0. Hiện trạng (đo trên `0f9aa2a`)

Bằng chứng ở `ops/reviews/bundled-tach-manh-spec-r1/` (README nêu từng tệp).

- **Bộ canh:** `_py_size_findings` (`scripts/tl_core/workflow.py:732`) WARN > 280 KiB = 286.720 B, FAIL > 320 KiB = 327.680 B; mục đích: trần mount Cowork ~343 KB/tệp
  (cắt cụt). Ca `r125_py_size_guard_wired_in_audit` (`scripts/tl_selftest.py:14716–14735`) đòi `py_size.warn == []`. Bundled là tệp RUNTIME: nằm trong
  `_RELEASE_REQUIRED_FILES` (`scripts/tl_core/release.py:486`) và được `load_runtime_fragment_cases` đọc trong gói ⇒ lý do của bộ canh áp đúng cho nó.
- **Kích thước:** bundled 285.112 B (18 fragment, 285.000 B dòng nguồn); dư 1.608 B trước WARN. Lớn nhất: `wp433_gws_cred_dich_ngoai_kho.py` 35.219 B,
  nhỏ nhất `wp45_fragment_canary.py` 245 B. Fragment secrets-set thêm 15.686 B ⇒ 300.798 B ⇒ WARN ⇒ r125 đỏ. Một fragment nhỏ (≤ 1.608 B) vẫn lọt dưới WARN (reviewer đo: fixture nhỏ ⇒ 285.236 B), nhưng mọi fragment cỡ thường thì vượt.
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
  - `scripts/tl_selftest.py`: hai ca `r291_docs_ngoai_goi` (~22775) và `r357_agents_ngoai_goi` (~22836) đọc `RELEASE_MANIFEST.json` ĐÃ COMMIT và ghim `len(paths) == 185` kèm dòng KÊ KHAI SLOT ⇒ thêm mảnh 2 phải đổi thành 186 cùng lúc với manifest (reviewer lượt 2 đo: manifest 186 + ghim 185 ⇒ selftest 1783/1785).
  - Trần gói 200 tệp: `RELEASE_MANIFEST.json` liệt kê 185 tệp ⇒ 186; ZIP phát hành có thêm chính manifest nên 186 ⇒ 187 entry. Trần 200 đếm theo entry ZIP.
  - `RELEASE_MANIFEST.json` băm nội dung từng tệp gói: bản vá đổi 4 tệp đã có trong manifest (`release.py`, `test_fragments.py`, bundled mảnh 1, golden) và thêm mảnh 2 ⇒ nếu không tái sinh trong chính packet thì job `gate` (lane LAND `release-verify --strict`) trên master ĐỎ từ lúc merge tới lúc merge PR manifest. Đây là nếp các packet trước (đo: merge #1453 `00ee839` ⇒ run 44711337223 job `gate` failure, xanh lại sau #1454). Reviewer đo trên nguyên mẫu: `release-verify RELEASE_MANIFEST.json --strict` rc 2.

## 1. `write_set`

```
.githooks/eol_policy_test.py
references/golden/workflow_audit.json
scripts/test_fragments/wp433_bundled_tach_manh.py
scripts/tl_core/release.py
scripts/tl_core/test_fragments.py
scripts/tl_selftest.py
scripts/tl_test_fragments_bundled.py
scripts/tl_test_fragments_bundled_2.py
```

Ngoài write set của WORKER, candidate có thêm đúng MỘT đường do **Land Operator** (phiên điều phối) ghi — protocol §9 cấm worker sửa manifest:

```
RELEASE_MANIFEST.json
```

**Candidate 9 đường (worker 8 + Land Operator 1) > trần 6 của ADR-0053 ⇒ nâng trần (Q2 + Q5 + Q6, chủ kho; E2), khối dưới chép nguyên vào lease.**
Không gộp được: golden phải đổi vì `files_scanned`; `eol_policy_test` phải đổi vì hai ca ghi bundled từ fragment thật; manifest phải đổi để master không đỏ
(Q5); `tl_selftest.py` phải đổi vì hai ca ghim số tệp manifest (Q6). Hai tệp bundled CHỈ sinh bằng `write_bundled_modules(scripts/test_fragments, scripts)`
(M1); `RELEASE_MANIFEST.json` CHỈ sinh bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` (M8) — không sửa tay.

```yaml
nang_tran:
  truc: kich_thuoc_packet
  ai_nang: ducthangho
  tran_cu: '<= 6 tep, <= 450 dong them (ADR-0053, packet sensitive)'
  tran_moi: '<= 9 duong dan trong candidate (worker 8 + Land Operator 1: RELEASE_MANIFEST.json), <= 450 dong them'
  can_cu: 'Chu kho 2026-11-20 trong phien dieu phoi #1206: Q2 nang len 7 tep, Q5 dua RELEASE_MANIFEST.json vao candidate, Q6 them scripts/tl_selftest.py (2 ca ghim 185 -> 186) => 9 duong dan. Numstat nguyen mau base 0f9aa2a, 7 tep khong ke manifest: eol_policy_test 2/4, golden 1/1, fragment 130/0, release.py 22/5, test_fragments.py 90/26, bundled 2/9, bundled_2 14/0 = +261/-45; manifest do o review luot 2: +16/-11 (tong 8 tep +277/-56); tl_selftest du toan <= 6 dong them.'
```

**Điều kiện cấp lease (E2):** comment chủ kho trên #433 cấp ngoại lệ
bundled nêu đúng `packet_id` `BUNDLED-TACH-MANH`, hai tệp bundled, sha256 đặc tả đã đóng băng, và trần đã nâng.

## 2. `ngoai_pham_vi`

- Không đổi ngưỡng, waiver hay vị từ của `_py_size_findings`; không sửa `r125_*`. Trong `scripts/tl_selftest.py` CHỈ được đổi hai chỗ ghim `== 185` → `== 186` của `r291_docs_ngoai_goi` / `r357_agents_ngoai_goi` và thêm một dòng KÊ KHAI SLOT cho mỗi ca (M9); không chạm ca nào khác.
- Không sửa `.github/checks/bundle_fragment_check.py`, `scripts/tl.py`, `_RELEASE_REQUIRED_FILES` (chỉ tệp chính là bắt buộc; mảnh được `test-fragments-check`
  canh), `.claude/dev/gate_lifecycle.py` (đề xuất nợ riêng nếu muốn băm cả mảnh), tài liệu `references/COMMANDS.md` / `docs/**` / ADR (nợ tài liệu riêng:
  `bundled-tach-manh-tai-lieu`).
- Không đổi thứ tự, nội dung hay số fragment hiện có.

## 3. `muc_tieu` (nguyên văn nguyên mẫu ở `ops/reviews/bundled-tach-manh-spec-r1/nguyen-mau.diff`)

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **Sinh mảnh.** `generate_bundled_modules(root) -> tuple[(tên, bytes), …]`: xếp fragment theo thứ tự ổn định hiện có, gom tham lam, mảnh mới khi tổng byte dòng nguồn vượt `_BUNDLED_SHARD_LIMIT` **192 KiB = 196.608 B ≈ 68,6% WARN (Q3, chủ kho chốt 2026-11-20)** (một fragment đơn lớn hơn hạn vẫn đứng riêng một mảnh). Mảnh 1 tên `tl_test_fragments_bundled.py`; mảnh k≥2 tên `tl_test_fragments_bundled_<k>.py`. Khi >1 mảnh, mảnh 1 thêm đúng MỘT phép gán `BUNDLED_FRAGMENT_SHARDS = ("tl_test_fragments_bundled_2.py", …)` sau `BUNDLED_FRAGMENT_SOURCES`; khi 1 mảnh, byte Y HỆT `generate_bundled_module_bytes` hiện nay. `generate_bundled_module_bytes(root)` giữ chữ ký, trả bytes mảnh 1. `write_bundled_modules(root, scripts_dir)` ghi mọi mảnh và XOÁ mảnh đánh số lạc; là đường tái sinh duy nhất được phép. | `test_fragments.py` |
| M2 | **Nạp mảnh.** `_read_bundled_sources(primary)` đọc mảnh 1 rồi ĐÚNG các mảnh mảnh 1 khai trong `BUNDLED_FRAGMENT_SHARDS`, theo thứ tự khai; tệp đánh số không khai thì KHÔNG nạp. Hợp đồng mỗi mảnh vẫn data-only: mảnh 1 cho phép `[SOURCES]` hoặc `[SOURCES, SHARDS]`; mảnh k≥2 chỉ `[SOURCES]`. Danh sách khai phải là `("…_2.py", …, "…_N.py")` liên tục, không rỗng. Thứ tự và tính duy nhất (NFC+casefold) kiểm XUYÊN mảnh. Mảnh khai mà thiếu ⇒ `BUNDLED_MODULE_MISSING` (mã lỗi giữ nguyên, kèm đường mảnh). | `test_fragments.py` |
| M3 | **Cổng `test-fragments-check`.** So từng mảnh kỳ vọng theo byte, cộng phát hiện tệp `tl_test_fragments_bundled_<k>.py` lạc trên đĩa (`extra_shards`) ⇒ `GENERATED_BUNDLE_STALE`. Thiếu mảnh 1 ⇒ `BUNDLED_MODULE_MISSING` như nay. Một mảnh: `expected_sha256`/`actual_sha256`/`*_bytes` giữ nguyên nghĩa (băm tệp). Nhiều mảnh: băm trên chuỗi `tên\0bytes` nối theo thứ tự. Thêm khoá `shards`. | `release.py` |
| M4 | `eol_policy_test.py`: hai chỗ ghi bundled từ fragment thật (`_tai_sinh_bundled`, ca driver) đổi sang `write_bundled_modules`. | `.githooks/eol_policy_test.py` |
| M5 | Golden `workflow_audit.json`: `files_scanned` 73 → 74; không khoá nào khác đổi (`golden-test` ok). | golden |
| M6 | Fragment `wp433_bundled_tach_manh.py`, 8 nhãn (§4). Fragment KHÔNG được văng ngoại lệ dưới đột biến: mọi chỉ số/độ dài phải chốt trước khi dùng (đột biến c lần đầu văng `IndexError` ⇒ tín dụng giả; đã thêm chốt). | fragment |
| M7 | Tái sinh bằng `write_bundled_modules`; ra đúng hai mảnh trên base (mảnh 1 ≈ 189 KB, mảnh 2 ≈ 102 KB). | bundled |
| M8 | **Land Operator** (phiên điều phối, không phải worker — protocol §9) tái sinh `RELEASE_MANIFEST.json` bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` trên đầu nhánh PR SAU khi worker xong mọi commit và review đã approve, commit một commit riêng lên nhánh PR, rồi mới trình chủ kho duyệt exact SHA (Q5). Worker chỉ đo bằng manifest TẠM hoặc bản tái sinh KHÔNG commit trong cây làm việc (khôi phục trước khi commit). Có commit vá nào sau commit manifest ⇒ Land Operator tái sinh lại trước khi chốt SHA. | manifest |
| M9 | `scripts/tl_selftest.py`: hai ca ghim số tệp manifest đổi `185` → `186` và thêm dòng `# KÊ KHAI SLOT (BUNDLED-TACH-MANH): 185 → **186** = + scripts/tl_test_fragments_bundled_2.py. Trần Package 200 (ZIP 187 entry).` cho mỗi ca (Q6). | `tl_selftest.py` |

## 4. `nghiem_thu`

| # | ca | tiêu chí | đỏ khi |
|---|---|---|---|
| N1 | fragment mới | `run()` True; 8 nhãn True: `mot_manh` (1 mảnh, không dòng SHARDS, = `generate_bundled_module_bytes`), `nhieu_manh` (hạn 100 KiB, 6×40 KiB ⇒ ≥3 mảnh, nạp đủ đúng thứ tự, mảnh 1 khai), `manh_lac` (tệp `_9` không khai: loader bỏ qua, cổng `GENERATED_BUNDLE_STALE` + `extra_shards == ["tl_test_fragments_bundled_9.py"]`), `ghi_xoa_lac`, `thieu_manh` (`BUNDLED_MODULE_MISSING`), `thu_tu_xuyen_manh` (đổi chỗ mảnh 2/3 ⇒ `BUNDLED_MODULE_CONTRACT`), `manh_tu_khai` (mảnh k≥2 có SHARDS ⇒ `BUNDLED_MODULE_CONTRACT`), `kho_that` (`_BUNDLED_SHARD_LIMIT ≤ 0,7·WARN`, mọi mảnh thật ≤ WARN). | nhãn nào khác True |
| N2 | đột biến (§4b) | 6/6 đỏ ĐÚNG nhãn đích, `run()` trả False (không văng). | sống, hoặc chết do ngoại lệ |
| N3 | gate trên SHA candidate (sau commit manifest M8), clone đầy đủ; worker đo trước bằng manifest tái sinh không commit | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1784, nguyên mẫu 1785); `test-fragments-check` `ok: true` hai mảnh; `bundle_fragment_check` `ok: true`, `failed: []`, `case_count` 19; `release-verify RELEASE_MANIFEST.json --strict --json` trên CHÍNH tệp đã commit: `ok: true`, `expected == checked` = 186 (lane LAND; chốt land chỉ trên SHA thoả vế này); `workflow-audit` `py_size.warn == []`, `files_scanned` 74; `golden-test` ok; `.githooks/eol_policy_test.py` 32/32 (trên cây ĐÃ commit); ruff F delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0. | bất kỳ vế nào |
| N4 | phản chứng mục đích | Áp `scripts/test_fragments/wp433_secrets_set_bundle.py` + `scripts/tl_gws.py` của `origin/agent/wp433-r8-g1-claude` lên head, `write_bundled_modules`: `py_size.warn == []`, `test-fragments-check` ok, selftest N/N (đo nguyên mẫu: 1786/1786, mảnh 189.328 / 117.343 B). Không commit phần áp. | còn WARN; HOẶC `test-fragments-check` không phải rc 0 kèm `ok: true`; HOẶC selftest không phải rc 0 với số đạt = tổng |

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

**MIỄN (Q4, chủ kho chốt 2026-11-20).** Mã chỉ là `pathlib` iterdir/write/unlink và AST/JSON; không API riêng nền, không ký tự đường đặc biệt. Không có lượt D1; ngân sách Windows của lease = 0.

## 5. `pham_vi_e`

Không chạm E4/E5: thư mục tạm, không mạng, không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex theo ADR-0055; trần kích thước theo khối `nang_tran` §1 (8 tệp / 450 dòng thêm) đo bằng numstat thật; vượt ⇒ DỪNG.
- `release-verify RELEASE_MANIFEST.json --strict` trên SHA ứng viên không `ok: true` ⇒ không trình land.
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
  `scripts/tl_test_fragments_bundled_2.py` (4 tệp worker) cộng `RELEASE_MANIFEST.json` do Land Operator tái sinh trong candidate (5 đường; thiếu ⇒ strict verify rc 2, reviewer lượt 2 đo), ngoại lệ bundled mới, lease mới; nhánh `a8a3b3c` phải merge master mới rồi tái sinh bằng
  `write_bundled_modules`. Mã `tl_gws.py` và fragment của nó không đổi.

## 8. `chua_do_duoc` và dự toán

- Numstat nguyên mẫu (đo, base `0f9aa2a`, bundled tái sinh bằng `write_bundled_modules`): `eol_policy_test.py` 2/4 · golden 1/1 · fragment mới 130/0 ·
  `release.py` 22/5 · `test_fragments.py` 90/26 · `tl_test_fragments_bundled.py` 2/9 · `tl_test_fragments_bundled_2.py` 14/0 ⇒ **7 tệp, 261 dòng thêm, 45 xoá**.
- Chưa đo: Windows (miễn theo Q4). Đã đo (review lượt 2): manifest +16/−11, tổng 8 tệp +277/−56; cộng `tl_selftest.py` (≤ 6) ⇒ dự toán ≤ 283/450.

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: secrets-set bị chặn bởi WARN bundled ⇒ chọn "Tách bundled trước" (không nâng ngưỡng, không waiver, không đưa test ra ngoài bundle).
- Chủ kho 2026-11-20 chốt Q1–Q4 theo khuyến nghị: #433 · nâng trần ADR-0053 lên 7 tệp/450 dòng · hạn mảnh 192 KiB · miễn đo Windows. Yêu cầu Codex review đặc tả trước khi duyệt băm.
- Chủ kho 2026-11-20, sau Codex lượt 1 (P1 manifest): Q5 — đưa `RELEASE_MANIFEST.json` vào packet, trần 8 tệp / 450 dòng; bỏ PR manifest riêng sau land.
- Sau Codex lượt 2 (P1 hai ca selftest ghim 185): Q6 — thêm `scripts/tl_selftest.py` vào write set worker (M9); manifest do Land Operator commit (M8, protocol §9). Candidate 9 đường / 450 dòng: CHỜ chủ kho xác nhận khi duyệt băm.

## 10. Nhật ký revision

- 2026-11-20T15:1xZ (phiên con của điều phối #1206): bản 1, đo §0 và nguyên mẫu trên clone đầy đủ `0f9aa2a` (Linux).
- 2026-11-20 (điều phối #1206): ghi quyết định Q1–Q4 của chủ kho; chưa đổi nội dung kỹ thuật.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 1 (run `402df797`, request_changes): P1 manifest vào packet (Q5, M8, N3) · P2 khối `nang_tran` · P2 N4 đỏ đủ ba vế · P3 đếm entry ZIP 186→187 · P3 số đo §0/N4.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 2 (run `1e18f41a`, request_changes): P1 `tl_selftest.py` vào write set (Q6, M9) · P2 manifest do Land Operator (M8) · P2 §7 secrets-set 5 đường · P3 README.
