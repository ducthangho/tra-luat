tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# BUNDLED-GATE-ORACLE-FRESHNESS r2: đóng lớp oracle cổng (F10) và oracle hình dạng AST (F11) trong fragment `wp433_bundled_tach_manh`

- Revision 2, thay r1. r1 nằm trên nhánh này ở `22151bced` và `b531cd2a2`. Lý do thay: review độc lập r1 trả `request_changes` (§9).

| trường | giá trị |
|---|---|
| `packet_id` · `packet_issue` | `wp433`, revision **11**, `spec_packet_id: BUNDLED-GATE-ORACLE-FRESHNESS`. Issue **#433** (Q4). Revision 10 là SECRETS-SET-BUNDLE-KIEU, đã merge ở PR #1490. |
| `nguon_cap_viec` | Mục sổ `xet_lai_cach_lam` của chủ kho: https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7058076373. Mục này chuyển F10 thành nợ `bundled-gate-oracle-freshness` và F11 thành nợ `bundled-tach-manh-do-min-ve`. Nguồn finding là verdict lượt 3 `ops/reviews/bundled-tach-manh-cr/luot3-codex-5293a85.txt` @ `3f5641c8cd93ace4bc786dc8d19c1be7468983ba`, sha256 `360c8a4fe56a58a40e4bf8e6292ac03d297060db831ac3104b519e6b13cc4b12` (đo lại 12:30Z 21-11, khớp). |
| `phu_thuoc` | Không. Packet cha BUNDLED-TACH-MANH r9 đã land qua PR #1485. |
| `review_class` | **`sensitive`** (Q5). Cổng `ops/lease_publish.py` (`_tinh_lop_tu_write_set`, bảng `_BANG_LOP` kiểu danh sách cho phép) trả `sensitive` cho cả bốn đường W1–W4, kể cả khi tính riêng từng đường. Đo 13:31Z 21-11 trên `29c22f7d`. |
| `reviewer` | Codex, read-only, trên exact SHA ứng viên (Q5). Trần lời gọi theo dòng khai `ADR-0055` ở đầu tệp. Đóng packet đòi `cross_approved` hoặc `human_audited` (protocol §8). Trước merge vẫn cần chủ kho audit `human_exact_head_audit.v1`. |
| `base` | `29c22f7d1f92321978d4d1dff16bd80d9ea744e0` (`origin/master`, đo 13:14Z 21-11). |

Các quyết định Q1–Q6 do chủ kho chốt ngày 2026-11-21 (§9).

## 0. Hiện trạng và tiền đề đo

**Tiền đề cho mọi phép đo của §4:**
- Dùng clone ĐẦY ĐỦ: `git rev-parse --is-shallow-repository` phải trả `false`, và phải có object `358451e8`.
- `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`.
- Base và SHA ứng viên C dựng bằng HAI clone trong MỘT lệnh. Mỗi lệnh ghi rc, giờ UTC và đầu ra.
- Đo trên clone nông là KHÔNG ĐO ĐƯỢC, không phải đạt.

**Hiện vật trên nhánh `ops/bundled-gate-oracle-spec`, thư mục `ops/reviews/bundled-gate-oracle-spec-r2/`.** Băm của từng tệp ghi trong `README.md` cùng thư mục:
- `ma_tran_r11.py`: ma trận đột biến A6, tự đủ. Mọi đột biến được ghim NGUYÊN VĂN dưới dạng cặp (chuỗi cũ, chuỗi mới), mỗi đột biến khai sẵn tập khoá đích.
- `va.py`: bản vá chuẩn cho W1.

Trong ma trận:
- 49 đột biến g5 lấy nguyên văn từ `ops/handoff/wp433/r9-g5/ma_tran_dot_bien.py` @ `bf38a110`.
- Đích của `f05_manh_1_gan_nhieu_dich` khai lại thành {V8, V9} (lý do ở M2).
- 20 đột biến lớp F10/F11 mang tiền tố `r11_`.
- 10 ca gỡ từng chốt mang tiền tố `a7`.
- Thêm luật: các ca `r11_`/`a7` (trừ bốn ca có đích chứa V32 hoặc cố ý văng) phải trả `_LY_DO` rỗng.

Đo trên `29c22f7d` (12:31–13:35Z 21-11, probe tiến trình mới, đủ 32 khoá mỗi lượt):

| đột biến (`ma_tran_r11.py`) | khoá đỏ trên base | khoá đỏ trên nguyên mẫu `va.py` |
|---|---|---|
| `r11_size_only` (cổng so `len(a or b'') != len(d)`) | — (lọt) | V24 V27 |
| `r11_one_stale_ok` (chèn `"ok": len(expected_modules) == 1,` ngay sau `"status": "stale",`) | — (lọt) | V27 |
| `r11_ann_empty` (mảnh 1 nhiều mảnh thêm `X: int`) | V4 V5 V6 V8 V9 (`ValueError`) | V8 |
| `r11_duplicate` (mảnh 1 nhiều mảnh thêm `BUNDLED_FRAGMENT_SOURCES = ()`) | V4 V5 V6 V8 | V8 |
| `r11_missing_ok_narrow` (nhánh `missing` thêm `"ok": not bundled_path.is_symlink()`) | — (lọt, reviewer r1 đo) | V26 |
| `r11_*_status`, `r11_stale_sha_swap`, sáu đột biến so một phần byte | lọt ở base hoặc ở bản vá r1 (reviewer r1, hàng 6) | đúng đích khai |

Nguyên nhân, đọc trên `scripts/test_fragments/wp433_bundled_tach_manh.py` @ `29c22f7d`:
- `hong()` (dòng 185–186) làm stale bằng cách NỐI byte, và chỉ trả `error`.
- Oracle V23 (dòng 191), V25 (dòng 195) và V26 (dòng 271) chỉ so `error`, hoặc `rc != 0` cộng `error`. Chúng không so `ok`/`status`.
- `_gan()` (dòng 67–75) gọi `literal_eval` trên mọi nút có đích `Name`, nên văng với `AnnAssign` không giá trị. Dict comprehension để lần gán SAU ghi đè lần gán trước.

## 1. `write_set`

| # | đường dẫn | cách đổi |
|---|---|---|
| W1 | `scripts/test_fragments/wp433_bundled_tach_manh.py` | áp `va.py` (§0), xem M1/M2 |
| W2 | `scripts/tl_test_fragments_bundled.py` | CHỈ sinh bằng `write_bundled_modules` (ngoại lệ bundled, E2) |
| W3 | `scripts/tl_test_fragments_bundled_2.py` | CHỈ sinh bằng `write_bundled_modules` (ngoại lệ bundled, E2). Dự kiến không đổi: reviewer r1 đo bản vá tương đương thì W3 giữ nguyên. Ranh mảnh trôi thì được phép đổi. |
| W4 | `RELEASE_MANIFEST.json` | CHỈ sinh bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json`, và là commit CUỐI của C (ngoại lệ manifest, E2) |

- Trần theo `ADR-0053` cho `sensitive`. Đo trên nguyên mẫu (reviewer r1 và phiên soạn): W1 khoảng +23/−9, W2 +1/−1, W4 +5/−5, tức 3 đến 4 đường và khoảng 29 dòng thêm.
- Reviewer r1 đo bản vá tương đương: selftest 1786/1786 và các cổng xanh mà không cần đổi tệp nào ngoài W1–W4.

## 2. `ngoai_pham_vi`

- Phần chia mịn khác của V1–V32 trong nợ `bundled-tach-manh-do-min-ve` (Q1). F11 chỉ vá hai biểu hiện `ann-empty` và `duplicate`. Phần còn lại của nợ ấy vẫn mở.
- Mã sản phẩm `scripts/tl_core/release.py` và `scripts/tl_core/test_fragments.py`.
- Khoảng đua kiểm-rồi-mở, và link đứt tại tên thư mục `test_fragments` (verdict lượt 3, mục B.3).
- Thêm hoặc bớt khoá: tập nghiệm thu vẫn đúng V1–V32 với nghĩa như r9 §4. Packet chỉ làm các phép đo trong khoá chặt hơn.
- Windows native: MIỄN, cùng lý do r9 §4c.

## 3. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Đóng lớp `bundle-gate-fixture-oracle` trong phạm vi khoá cổng V23–V27. (a) `quyet(rc, j)` trả đủ bốn trường `(rc, ok, status, error)`. V23 và V25 đòi `(2, False, "stale", "GENERATED_BUNDLE_STALE")`. V26 đòi `(2, False, "missing", "BUNDLED_MODULE_MISSING")`. Vế current của V27 đòi `(0, True, "current", None)`. (b) `hong(t, nhom)` dựng BA fixture riêng, mỗi fixture đổi đúng MỘT byte của mảnh `t` (ở vị trí đầu, giữa, cuối), giữ nguyên độ dài. Mỗi fixture phải cho quyết định stale đủ bốn trường, và `actual_sha256`/`actual_bytes` bằng băm và độ dài tính độc lập từ bytes trên đĩa (một mảnh: bytes tệp; nhiều mảnh: chuỗi `tên\0bytes` nối theo thứ tự). V24 (mảnh chính và mảnh phụ của gói ba mảnh) và vế stale của V27 (gói một mảnh) dùng `hong()`. | W1 |
| M2 | Tách đọc dữ liệu khỏi đọc hình dạng trong `_gan()`. Hình dạng (`ten`, dùng cho V3/V8) giữ nguyên nghĩa. Dữ liệu (`SOURCES`/`SHARDS`) chỉ đến từ phép gán CHUẨN: `ast.Assign` có đúng một đích `ast.Name` mang đúng tên, và mỗi tên lấy lần gán chuẩn ĐẦU TIÊN. `_gan()` không văng với `AnnAssign`. Hệ quả đã đo: gán nhiều đích (`f05`) không còn là nguồn dữ liệu, nên V9 đọc ra `None` và đỏ cùng V8. | W1 |
| M3 | Tái sinh bundle bằng `write_bundled_modules` trên cây đã sửa. | W2, W3 |
| M4 | Tái sinh manifest làm commit cuối. | W4 |

- Cài đặt M1/M2 bằng đúng văn bản của `va.py` (bảy thay thế, mỗi thay thế khớp đúng một lần trên base), vì các ca `a7*` của ma trận ghim theo chuỗi ấy.
- Lệch khỏi `va.py` là được, nhưng phải: giữ nghĩa M1/M2; sửa các ca `a7*` cho cùng ý nghĩa gỡ chốt; và nêu lý do trong handoff. Ma trận đã sửa phải đặt trong handoff và neo băm.

## 4. `nghiem_thu`

Mọi tiêu chí đo trên C theo tiền đề §0.

| # | tiêu chí | đỏ khi |
|---|---|---|
| A0 | Trên base thật của lease, `ma_tran_r11.py` cho các ca `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow` là SAI với `do=` rỗng (lỗ cũ còn). `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`, `r11_duplicate` cho `do=V4,V5,V6,V8`. | một trong năm ca cho kết quả khác. Khi đó giả định của packet đã sai: DỪNG thi công và mở revision mới |
| A1 | Trên C, `run()` của fragment trả True, đủ 32 khoá, cả 32 True. | `run()` không True; hoặc số khoá ≠ 32; hoặc có khoá False |
| A2 | `python -B ma_tran_r11.py <clone C>` rc 0, dòng cuối `TONG: 79 dot bien + doi chung, sai=0`. Như vậy mỗi đột biến cho đủ 32 khoá, tập False = tập đích khai, và ca nào thuộc luật `_LY_DO` rỗng thì không văng. Mỗi V1–V32 là đích của ít nhất một đột biến đơn đích. | rc ≠ 0; hoặc `sai` ≠ 0; hoặc số đột biến ≠ 79; hoặc một khoá mất đột biến đơn đích |
| A3 | Răng của từng chốt, đo qua các ca `a7*` của A2. Gỡ riêng một chốt (giữ độ dài, bốn trường, lần đầu thắng, phép gán chuẩn, mỗi vị trí một fixture) thì fragment vẫn xanh, nhưng đột biến đích của chốt ấy sống hoặc lan rộng. | một cặp `a7*` SAI trong A2 |
| A4 | Gate trên C so với base, chạy cùng lệnh. Số nền đo trên `29c22f7d` lúc 13:15–13:29Z 21-11:<br>• `--selftest` N/N với hai số bằng nhau, **N = 1786** (packet không thêm ca);<br>• `test-fragments-check --json` rc 0, `ok: true`;<br>• `.github/checks/bundle_fragment_check.py --json` `ok: true`, `failed: []`, `case_count` **20**;<br>• `release-verify RELEASE_MANIFEST.json --strict --json` trên tệp ĐÃ commit: `ok: true`, `expected_file_count == checked_file_count == 186`;<br>• `workflow-audit --strict --json` rc 0, `py_size.fail == []`, `py_size.warn == []`, `files_scanned` **74**;<br>• `golden-test --json` `ok: true`, 20 ca;<br>• `.githooks/eol_policy_test.py` **32/32**;<br>• ruff F trên W1: 0 lỗi;<br>• `git diff --check base C`, `doctrine-scan` và `adr-song` rc 0. | bất kỳ vế nào |
| A5 | `git diff --name-only base C` ⊆ {W1, W2, W3, W4}. W2/W3 trùng byte với `write_bundled_modules` chạy lại trên C. `release-manifest` chạy lại trên C không tạo diff. | tệp ngoài W1–W4 đổi; hoặc bundle hay manifest lệch đầu ra sinh lại |

## 5. `pham_vi_e`

Không chạm E4 hay E5. Mọi đo đạc chạy trong thư mục tạm, không mạng, không LIVE, không đẩy Package, không đọc secrets. Packet không đổi danh sách thẩm quyền, cổng cấp lease hay cổng merge.

## 6. `luat_dung`

- Điểm dừng theo `docs/PROTOCOL_DA_PHIEN.md` §12 và bảng trần của `ADR-0055` (dòng khai ở đầu tệp). Đặc tả không đặt ngân sách mềm.
- Trần kích thước theo `ADR-0053`. Vượt trần thì DỪNG và hỏi chủ kho (**E2**), kèm numstat thật.
- Chưa có comment ngoại lệ bundled và manifest đúng `spec_packet_id` này, cùng lease r11 còn hiệu lực, thì không thi công (**E2**). Ngoại lệ 7053681301 của r9 KHÔNG chuyển sang. Chủ kho uỷ quyền phiên soạn đăng cả hai (Q6).
- Cần đổi tệp ngoài W1–W4, hoặc A4 đòi N ≠ 1786, thì DỪNG và hỏi chủ kho (**E2**), kèm tệp, lý do và phép đo.

## 7. `hinh_dang_ke_thua`

| slug lớp | lịch sử | số lượt |
|---|---|---|
| `bundle-gate-fixture-oracle` | F03 `4e74fe1` → F06 `36dc91a` → F10 `5293a85` → spec r1 F3 (review độc lập, 21-11) | 4 lần mở |
| `shard-ast-shape-oracle` | F02 `4e74fe1` → F05 `36dc91a` → F11 `5293a85` | 3 lượt |

Tỷ lệ đóng lớp của chuỗi BUNDLED-TACH-MANH: lượt 1→2 là 1/4, lượt 2→3 là 1/3, tức hai chuyển tiếp liền dưới 50% (mục sổ 7058076373).

Hình dạng lặp: **mỗi bản vá oracle chỉ bịt đúng đột biến được báo**. Spec r1 tự rơi vào đúng hình dạng ấy: M1 r1 chỉ nâng `hong()`, nên reviewer tìm được 8 đột biến cùng lớp vẫn sống. Vì vậy r2 đóng ở mức LỚP:
- mọi oracle của khoá cổng V23–V27 so đủ quyết định;
- mỗi vị trí byte có một fixture riêng;
- ma trận khai sẵn 20 đột biến cùng lớp;
- năm chốt được đo răng riêng.

Hệ quả cho packet khác: không có. Ranh mảnh trôi (r9 §7) vẫn áp, nên W3 nằm trong write set.

## 8. `chua_do_duoc` và số đo

- Số nền A4 đo trên `29c22f7d` lúc 13:15–13:29Z 21-11, cả tám lệnh rc 0. Số liệu ghi trong A4.
- `ma_tran_r11.py` trên nguyên mẫu (clone `29c22f7d` + `va.py`): kết quả ghi trong `README.md` của thư mục hiện vật, kèm giờ đo.
- Chưa đo được:
  - CI GitHub trên exact SHA C (chỉ có sau khi push);
  - Codex review trên C;
  - human audit;
  - Windows native: miễn (§2).
- Đột biến ngoài 79 ca của ma trận: chưa đo. Reviewer Codex được thêm đột biến. Đột biến thêm cũng phải thoả A2, nếu không thì là finding.

## 9. Quyết định của chủ kho và lịch sử

Quyết định (AskUserQuestion, phiên `session_015Gtxrb38PyN9US77Ccx4us`, 2026-11-21):
- **Q1 Phạm vi F11:** chỉ hai biểu hiện `ann-empty` và `duplicate`.
- **Q2 Khoá đích:** chốt theo số đo. Không thêm vế stale vào V28.
- **Q3 Write set, ngoại lệ:** W1–W4; cấp lại hai ngoại lệ bundled và manifest. Phần "routine, reviewer Claude" của Q3 bị Q5 thay.
- **Q4 Định danh:** Issue #433 revision 11.
- **Q5 (E3, sau finding F1 của review r1):** `sensitive`, kèm Codex review.
- **Q6 Uỷ quyền:** phiên soạn được đăng lên #433 comment ngoại lệ E2 và lease r11 g1 neo `spec_hash`, rồi thi công, đẩy nhánh code và mở PR nháp. Merge chờ chủ kho audit và duyệt.

Review độc lập r1 (subagent Claude read-only, 13:20–13:30Z 21-11): `request_changes`. Cách xử lý từng finding:

| finding | mức | xử lý ở r2 |
|---|---|---|
| F1 `review-class-lech-cong-lease` | P1 | Hỏi chủ kho (E3) và nhận Q5: `sensitive`, thêm dòng `ADR-0053`, reviewer Codex. |
| F2 `dot-bien-nghiem-thu-khong-ghim-nguyen-van` | P2 | Mọi đột biến ghim nguyên văn trong `ma_tran_r11.py`, neo băm. `r11_size_only` dùng `len(a or b'')`. `r11_size_only_raw` giữ làm ca riêng với đích của nó. |
| F3 `bundle-gate-fixture-oracle` (lần mở thứ tư) | P2 | M1 mở rộng ra V23–V27. Mỗi vị trí byte một fixture. Kiểm `actual_sha256`/`actual_bytes`. 20 đột biến cùng lớp vào ma trận. |
| F4 `dac-ta-du-doan-sai-dich-ma-tran` | P2 | M2 nói rõ hệ quả. `f05` khai lại đích {V8, V9}. |
| F5 `a7-go-gop-khong-do-tung-chot` | P3 | A3 với năm cặp gỡ đơn chốt. |
| F6 `luat-dung-ngoai-hai-loai-dong` | P3 | Dòng "§0 lệch" thành A0; dòng "clone nông" thành tiền đề §0. |
| F7 `so-dong-sai` | P3 | Sửa số dòng ở §0. |
| F8 `cho-dat-handoff-va-ma-tran-mo-rong` | P3 | Ma trận và bản vá nằm ở `ops/reviews/bundled-gate-oracle-spec-r2/` trên nhánh spec, neo băm. Handoff của executor đặt ở `ops/handoff/wp433/r11-g1/` trên nhánh riêng, không nằm trong C. |

## 10. Nhật ký revision

- r1 (2026-11-21): bản đầu.
- r2 (2026-11-21): xử lý review độc lập r1 (F1–F8) và Q5/Q6.
