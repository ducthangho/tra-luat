tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# BUNDLED-GATE-ORACLE-FRESHNESS r5: đóng lớp oracle cổng (F10) và oracle hình dạng AST (F11) trong fragment `wp433_bundled_tach_manh`

- Revision 5, thay r4 (`61221558a`, `867243d5e`), r3 (`121bbaa3e`, `ef3e0c006`), r2 (`978c13ccd`, `dfc345c18`) và r1 (`22151bced`, `b531cd2a2`) trên cùng nhánh. Lý do thay: review độc lập r4 tìm ra một hồi quy so với base (R4-F1), thuộc đúng tiêu chí chặn (a) của Q7 (§9).

| trường | giá trị |
|---|---|
| `packet_id` · `packet_issue` | `wp433`, revision **11**, `spec_packet_id: BUNDLED-GATE-ORACLE-FRESHNESS`. Issue **#433** (Q4). Revision 10 là SECRETS-SET-BUNDLE-KIEU, đã merge ở PR #1490. |
| `nguon_cap_viec` | Mục sổ `xet_lai_cach_lam` của chủ kho: https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7058076373. Mục này chuyển F10 thành nợ `bundled-gate-oracle-freshness` và F11 thành nợ `bundled-tach-manh-do-min-ve`. Nguồn finding là verdict lượt 3 `ops/reviews/bundled-tach-manh-cr/luot3-codex-5293a85.txt` @ `3f5641c8cd93ace4bc786dc8d19c1be7468983ba`, sha256 `360c8a4fe56a58a40e4bf8e6292ac03d297060db831ac3104b519e6b13cc4b12` (đo lại 12:30Z 21-11, khớp). |
| `phu_thuoc` | Không. Packet cha BUNDLED-TACH-MANH r9 đã land qua PR #1485. |
| `review_class` | **`sensitive`** (Q5). Cổng `ops/lease_publish.py` (`_tinh_lop_tu_write_set`, bảng `_BANG_LOP` kiểu danh sách cho phép) trả `sensitive` cho cả bốn đường W1–W4, kể cả khi tính riêng từng đường. Đo 13:31Z 21-11 trên `29c22f7d`. |
| `reviewer` | Codex, read-only, trên exact SHA ứng viên (Q5). Trần lời gọi theo dòng khai `ADR-0055` ở đầu tệp. Đóng packet đòi `cross_approved` hoặc `human_audited` (protocol §8). Merge cần chủ kho audit `human_exact_head_audit.v1` và duyệt riêng (`docs/PROTOCOL_DA_PHIEN.md` §3.2.1, K1/K4 theo ADR-0063). Đây là nghĩa vụ land của protocol, không phải điểm hỏi do đặc tả đặt. |
| `base` | `29c22f7d1f92321978d4d1dff16bd80d9ea744e0` (`origin/master`, đo 13:14Z 21-11). |

Các quyết định Q1–Q6 do chủ kho chốt ngày 2026-11-21 (§9).

## 0. Hiện trạng và tiền đề đo

**Tiền đề cho mọi phép đo của §4:**
- Dùng clone ĐẦY ĐỦ: `git rev-parse --is-shallow-repository` phải trả `false`, và phải có object `358451e8`.
- `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`.
- Base và SHA ứng viên C dựng bằng HAI clone trong MỘT lệnh. Mỗi lệnh ghi rc, giờ UTC và đầu ra.
- Đo trên clone nông là KHÔNG ĐO ĐƯỢC, không phải đạt.

**Hiện vật trên nhánh `ops/bundled-gate-oracle-spec`, thư mục `ops/reviews/bundled-gate-oracle-spec-r5/`.** Băm của từng tệp ghi trong `README.md` cùng thư mục:
- `ma_tran_r11.py`: ma trận đột biến A2, tự đủ, sinh bởi `gen_ma_tran.py` cùng thư mục. Mọi đột biến được ghim NGUYÊN VĂN dưới dạng cặp (chuỗi cũ, chuỗi mới), mỗi đột biến khai sẵn tập khoá đích.
- `va.py`: bản vá chuẩn cho W1.

Trong ma trận:
- 49 đột biến g5 lấy nguyên văn từ `ops/handoff/wp433/r9-g5/ma_tran_dot_bien.py` @ `bf38a110`.
- Ba đột biến g5 được khai lại đích theo cơ chế đã đo:
  - `f05_manh_1_gan_nhieu_dich` → {V8, V9} (lý do ở M2);
  - `v28_bam_nhieu_manh_bo_ten` → {V24, V28}: `hong()` nay kiểm băm của payload stale nhiều mảnh, mà đột biến bỏ tên làm băm ấy sai;
  - `f01_dem_ky_tu_thay_vi_byte` → {V5, V31}: khi đếm theo ký tự, mảnh thật đo trên cây ĐÃ vá (W1 dài thêm, có chữ nhiều byte) vượt 0,7·WARN tính theo byte. Đích này phụ thuộc nội dung kho thật, nên sẽ trôi khi kích thước fragment đổi.
- 43 đột biến lớp F10/F11 mang tiền tố `r11_`: gồm m1–m8 do review r2 tự nghĩ, 5 đột biến `r11_rv3_` của review r3 và 10 đột biến `r11_rv4_` của review r4.
- 13 ca nợ mang tiền tố `no_`, đích RỖNG: đột biến còn SỐNG trên cả base lẫn bản vá, thuộc nợ `bundled-gate-oracle-to-hop` (§2). Ai đóng nợ thì ca tương ứng SAI và phải khai lại đích, nên nợ không biến mất trong im lặng.
- 20 ca gỡ từng chốt mang tiền tố `a7_`.
- `doi_chieu_don_dieu.py`: phép đo A6. Đầu vào là đầu ra ma trận trên base và trên C.
- Thêm luật: các ca `r11_`/`a7_` (trừ bốn ca có đích chứa V32 hoặc cố ý văng) phải trả `_LY_DO` rỗng.
- Script tự kiểm mỗi V1–V32 có ít nhất một đột biến đơn đích (dòng `DON_DICH`).
- Đột biến không áp được thì ghi `KHONG_AP_DUOC`, tính là SAI và chạy tiếp.

Đo trên `29c22f7d` và nguyên mẫu `va.py` r5 bằng `ma_tran_r11.py`, mỗi đột biến chạy trong một tiến trình mới và trả đủ 32 khoá. Giờ đo và băm đầu ra ghi trong `README.md`.

| đột biến (`ma_tran_r11.py`) | khoá đỏ trên base | khoá đỏ trên nguyên mẫu `va.py` |
|---|---|---|
| `r11_size_only` (cổng so `len(a or b'') != len(d)`) | — (lọt) | V24 V27 |
| `r11_one_stale_ok` (chèn `"ok": len(expected_modules) == 1,` ngay sau `"status": "stale",`) | — (lọt) | V27 |
| `r11_ann_empty` (mảnh 1 nhiều mảnh thêm `X: int`) | V4 V5 V6 V8 V9 (`ValueError`) | V8 |
| `r11_duplicate` (mảnh 1 nhiều mảnh thêm `BUNDLED_FRAGMENT_SOURCES = ()`) | V4 V5 V6 V8 | V8 |
| `r11_missing_ok_narrow` (nhánh `missing` thêm `"ok": not bundled_path.is_symlink()`) | — (lọt, reviewer r1 đo) | V26 |
| 23 đột biến `r11_` còn lại: `*_status`, `stale_rc1`, `sha_swap`, sáu đột biến so một phần byte, m1–m8, … | phần lớn lọt ở base (chi tiết trong `ma-tran-base.out`) | đúng đích khai |

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

- Trần theo `ADR-0053` cho `sensitive`. Đo trên nguyên mẫu `va.py` r5 (16:47Z 21-11): W1 +48/−20. Reviewer r2 đo trên bản r2: W2 +1/−1, W4 +5/−5, W3 không đổi. Ước tính 3 đến 4 đường, khoảng 54 dòng thêm.
- Reviewer r1 đo bản vá tương đương: selftest 1786/1786 và các cổng xanh mà không cần đổi tệp nào ngoài W1–W4.

## 2. `ngoai_pham_vi`

- Phần chia mịn khác của V1–V32 trong nợ `bundled-tach-manh-do-min-ve` (Q1). F11 chỉ vá hai biểu hiện `ann-empty` và `duplicate`. Phần còn lại của nợ ấy vẫn mở.
- Mã sản phẩm `scripts/tl_core/release.py` và `scripts/tl_core/test_fragments.py`.
- Khoảng đua kiểm-rồi-mở, và link đứt tại tên thư mục `test_fragments` (verdict lượt 3, mục B.3).
- Thêm hoặc bớt khoá: tập nghiệm thu vẫn đúng V1–V32 với nghĩa như r9 §4. Packet chỉ làm các phép đo trong khoá chặt hơn.
- Windows native: MIỄN, cùng lý do r9 §4c.
- **Nợ mới `bundled-gate-oracle-to-hop` (P2, Q7).** Gồm các lỗ ĐO, không phải lỗi sản phẩm: cổng thật hiện không có các lỗi này. Đột biến tương ứng sống trên CẢ base lẫn bản vá, tức không phải hồi quy. Danh sách nguyên văn là 13 ca `no_` trong `ma_tran_r11.py`, nguồn là review r3 R3-F2 và R3-F5:
  - hai mảnh cùng hỏng;
  - tráo nội dung giữa mảnh;
  - hai mảnh lạc cùng lúc;
  - `extra_shards` chỉ báo tên đầu;
  - mảnh lạc trên gói một mảnh;
  - mảnh lạc là symlink;
  - mất mảnh 1 trên gói nhiều mảnh;
  - vùng mù giữa các điểm lấy mẫu;
  - `actual_bytes` sai khi thiếu mảnh phụ;
  - nhánh `invalid` trả `ok`;
  - hai biến thể regex số mảnh;
  - `SOURCES` mảnh phụ dạng list.
  Cách đóng có cấu trúc được đề xuất là oracle VI SAI: một mô hình tham chiếu độc lập chạy trên tập tổ hợp tất định. Phương án này đã được chủ kho cân nhắc và để lại cho packet sau.

## 3. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Đóng lớp `bundle-gate-fixture-oracle` trong phạm vi khoá cổng V23–V27. (a) `quyet(rc, j)` trả đủ bốn trường `(rc, ok, status, error)`. V23 và V25 đòi `(2, False, "stale", "GENERATED_BUNDLE_STALE")`. V26 đòi `(2, False, "missing", "BUNDLED_MODULE_MISSING")`. Vế current của V27 đòi `(0, True, "current", None)`. (b) `hong(t, nhom)` phủ theo HỌ nhiễu loạn. Mỗi nhiễu loạn là một fixture riêng trên mảnh `t`, gồm bảy fixture: lật một byte ở đầu, ở giữa, ở cuối (giữ độ dài); nối một byte; cắt byte cuối (đổi độ dài); nối dòng `# sua\n`, tức nguyên văn nhiễu loạn của base; đổi `\n` đầu tiên thành `\r\n` (kết thúc dòng). **Luật đơn điệu:** tập nhiễu loạn của bản vá phải chứa mọi nhiễu loạn của base, và A6 đo luật này. Mỗi fixture phải cho quyết định stale đủ bốn trường. Cả bốn trường `expected_sha256`, `actual_sha256`, `expected_bytes`, `actual_bytes` phải bằng băm và độ dài tính độc lập: vế kỳ vọng từ bytes đã ghim ở `cong()`, vế đĩa từ bytes trên đĩa (một mảnh: bytes tệp; nhiều mảnh: chuỗi `tên\0bytes` nối theo thứ tự). (c) V23 dựng mỗi mảnh lạc một fixture riêng, với `_9` (một chữ số) và `_10` (hai chữ số). Mỗi fixture đòi quyết định stale đủ bốn trường và `extra_shards` đúng bằng `[tên mảnh lạc]`. V24 (mảnh chính và mảnh phụ của gói ba mảnh) và vế stale của V27 (gói một mảnh) dùng `hong()`. | W1 |
| M2 | Tách đọc dữ liệu khỏi đọc hình dạng trong `_gan()`. Hình dạng (`ten`, dùng cho V3/V8) giữ nguyên nghĩa. Dữ liệu (`SOURCES`/`SHARDS`) chỉ đến từ phép gán CHUẨN: `ast.Assign` có đúng một đích `ast.Name` mang đúng tên, và mỗi tên lấy lần gán chuẩn ĐẦU TIÊN. `_gan()` không văng với `AnnAssign`. Khi không có phép gán `SOURCES` chuẩn, dữ liệu là RỖNG (không văng), và V3/V8 phán bằng hình dạng. **V8 soi hình dạng trên MỌI gói nhiều mảnh mà fragment sinh ra** (`deu`, `lech` của V5, `lon` của V6). Ba khoá V5/V6/V8 dùng chung hai fixture `lech`/`lon`, khai một lần ở phạm vi `_do`. Lý do: base vô tình bắt được rác hình dạng nằm ở mảnh một-fragment qua V5/V6 (đọc dữ liệu rộng, hoặc văng), còn khoá hình dạng V8 cũ chỉ soi gói `deu`, vốn không có mảnh một-fragment nào (R4-F1). Hệ quả đã đo: gán nhiều đích (`f05`) không còn là nguồn dữ liệu, nên V9 đọc ra `None` và đỏ cùng V8. | W1 |
| M3 | Tái sinh bundle bằng `write_bundled_modules` trên cây đã sửa. | W2, W3 |
| M4 | Tái sinh manifest làm commit cuối. | W4 |

- Cài đặt M1/M2 bằng đúng văn bản của `va.py` (mười một thay thế, mỗi thay thế khớp đúng một lần trên base), vì các ca `a7_` của ma trận ghim theo chuỗi ấy.
- Lệch khỏi `va.py` là được, nhưng phải: giữ nghĩa M1/M2; sửa các ca `a7_` cho cùng ý nghĩa gỡ chốt; và nêu lý do trong handoff. Ma trận đã sửa phải đặt trong handoff và neo băm.

## 4. `nghiem_thu`

Mọi tiêu chí đo trên C theo tiền đề §0.

| # | tiêu chí | đỏ khi |
|---|---|---|
| A0 | Trên base thật của lease, `ma_tran_r11.py` cho các ca `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow` là SAI với `do=` rỗng (lỗ cũ còn). `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`, `r11_duplicate` cho `do=V4,V5,V6,V8`. | một trong năm ca cho kết quả khác. Khi đó giả định của packet đã sai: DỪNG thi công và mở revision mới |
| A1 | Trên C, `run()` của fragment trả True, đủ 32 khoá, cả 32 True. | `run()` không True; hoặc số khoá ≠ 32; hoặc có khoá False |
| A2 | `python -B ma_tran_r11.py <clone C>` rc 0, dòng đầu `DON_DICH: 32/32 …`, dòng cuối `TONG: 125 dot bien + doi chung, sai=0`. Như vậy mỗi đột biến cho đủ 32 khoá, tập False = tập đích khai, và ca nào thuộc luật `_LY_DO` rỗng thì không văng. Mỗi V1–V32 là đích của ít nhất một đột biến đơn đích. | rc ≠ 0; hoặc `sai` ≠ 0; hoặc số đột biến ≠ 125; hoặc `DON_DICH` < 32/32 |
| A3 | Răng của từng chốt, đo qua các ca `a7_` của A2. Có mười chốt: nhiễu loạn của base, họ đổi độ dài, họ giữ độ dài, mỗi vị trí một fixture, bốn trường quyết định, bốn trường băm/độ dài, lần đầu thắng, phép gán chuẩn, mảnh lạc hai chữ số, mỗi mảnh lạc một fixture. Gỡ riêng một chốt thì fragment vẫn xanh, nhưng đột biến đích của chốt ấy sống (đích rỗng) hoặc lan rộng. | một cặp `a7_` SAI trong A2 |
| A4 | Gate trên C so với base, chạy cùng lệnh. Số nền đo trên `29c22f7d` lúc 13:15–13:29Z 21-11:<br>• `--selftest` N/N với hai số bằng nhau, **N = 1786** (packet không thêm ca);<br>• `test-fragments-check --json` rc 0, `ok: true`;<br>• `.github/checks/bundle_fragment_check.py --json` `ok: true`, `failed: []`, `case_count` **20**;<br>• `release-verify RELEASE_MANIFEST.json --strict --json` trên tệp ĐÃ commit: `ok: true`, `expected_file_count == checked_file_count == 186`;<br>• `workflow-audit --strict --json` rc 0, `py_size.fail == []`, `py_size.warn == []`, `files_scanned` **74**;<br>• `golden-test --json` `ok: true`, 20 ca;<br>• `.githooks/eol_policy_test.py` **32/32**;<br>• ruff F trên W1: 0 lỗi;<br>• `git diff --check base C`, `doctrine-scan` và `adr-song` rc 0. | bất kỳ vế nào |
| A5 | `git diff --name-only base C` ⊆ {W1, W2, W3, W4}. W2/W3 trùng byte với `write_bundled_modules` chạy lại trên C. `release-manifest` chạy lại trên C không tạo diff. | tệp ngoài W1–W4 đổi; hoặc bundle hay manifest lệch đầu ra sinh lại |
| A6 | Đơn điệu so với base, TRÊN 125 ca của ma trận: `python3 doi_chieu_don_dieu.py <ma trận trên base> <ma trận trên C>` rc 0. Script in dòng `DON_DIEU: … C yeu di 0; C thieu 0`, tức trong các ca của ma trận, ca nào base giết (có khoá đỏ, hoặc văng cả fragment) thì C cũng giết. Đầu ra hai ma trận phải từ hai clone dựng trong MỘT lệnh. | rc ≠ 0; hoặc có dòng `YEU_DI`/`THIEU` |

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
| `bundle-gate-fixture-oracle` | F03 `4e74fe1` → F06 `36dc91a` → F10 `5293a85` → spec r1 F3 → spec r2 R1–R4 → spec r3 R3-F1/F2 (ba review độc lập, 21-11) | 6 lần mở |
| `shard-ast-shape-oracle` | F02 `4e74fe1` → F05 `36dc91a` → F11 `5293a85` → spec r3 R3-F3 → spec r4 R4-F1 | 5 lượt |

Tỷ lệ đóng lớp của chuỗi BUNDLED-TACH-MANH: lượt 1→2 là 1/4, lượt 2→3 là 1/3, tức hai chuyển tiếp liền dưới 50% (mục sổ 7058076373).

Hình dạng lặp: **mỗi bản vá oracle chỉ bịt đúng đột biến được báo**. Hình dạng này đã xuất hiện ba lần ngay trong lượt soạn đặc tả này:
- spec r1: M1 chỉ nâng `hong()`, nên review r1 tìm được 8 đột biến cùng lớp vẫn sống;
- spec r2: bỏ fixture nối byte để giữ độ dài, nên review r2 cho thấy `m1`/`m7` sống trên bản vá mà base lại giết được, tức bản vá làm oracle YẾU đi;
- nguyên mẫu r3 đầu tiên: dồn hai mảnh lạc vào một fixture, nên `r11_extra_ok` sống. Phiên soạn tự đo ra trước khi gửi review.

Ba lần cùng hình dạng thì phải đổi cách làm, không vá tiếp theo danh sách. Cách r3: phủ theo **HỌ** nhiễu loạn, với **mỗi nhiễu loạn một fixture riêng**. Lý do: dồn nhiều nhiễu loạn vào một fixture cho phép một cổng chỉ nhìn một phần vẫn thấy khác. Kèm theo:
- kiểm đủ bốn trường quyết định và bốn trường băm/độ dài tính độc lập;
- chín chốt, mỗi chốt được đo răng riêng.

Review r3 vẫn mở lớp lần thứ sáu (R3-F1, R3-F2), kể cả sau khi đã đổi thiết kế. Đó là E1 theo ADR-0067. Gốc rễ: một oracle dựa trên TẬP FIXTURE HỮU HẠN không bao giờ đóng được lớp "cổng nói dối", vì reviewer luôn dựng được một cổng sai ngoài tập ấy. Chủ kho chọn (Q7) chốt phạm vi:
- packet này đóng phần HỒI QUY so với base, bằng luật đơn điệu A6 và nhiễu loạn của base giữ nguyên;
- packet này đóng hai lỗ F10 và hai biểu hiện F11;
- các lỗ đo còn lại, vốn có sẵn từ base, thành nợ `bundled-gate-oracle-to-hop` (§2) và được ghi nhận bằng các ca `no_`.

**Độ mịn nghiệm thu, theo tiền lệ Q9:** review trên C chỉ chặn khi chỉ ra (a) một đột biến base giết mà C để sống, (b) một lỗi của mã sản phẩm, hoặc (c) một tiêu chí A0–A6 đo sai. Đột biến sống trên cả base lẫn C thì ghi vào nợ `bundled-gate-oracle-to-hop` (P3 cho packet này).

Hệ quả cho packet khác: không có. Ranh mảnh trôi (r9 §7) vẫn áp, nên W3 nằm trong write set.

## 8. `chua_do_duoc` và số đo

- Số nền A4 đo trên `29c22f7d` lúc 13:15–13:29Z 21-11, cả tám lệnh rc 0. Số liệu ghi trong A4.
- `ma_tran_r11.py` trên nguyên mẫu (clone `29c22f7d` + `va.py`): kết quả ghi trong `README.md` của thư mục hiện vật, kèm giờ đo.
- Chưa đo được:
  - CI GitHub trên exact SHA C (chỉ có sau khi push);
  - Codex review trên C;
  - human audit;
  - Windows native: miễn (§2).
- Đột biến ngoài 125 ca của ma trận: chưa đo. A6 chỉ chứng minh tính đơn điệu TRÊN các ca của ma trận, không chứng minh cho mọi đột biến (R4-F2). Reviewer Codex được thêm đột biến. Đột biến thêm cũng phải thoả A2, nếu không thì là finding.

## 9. Quyết định của chủ kho và lịch sử

Quyết định (AskUserQuestion, phiên `session_015Gtxrb38PyN9US77Ccx4us`, 2026-11-21):
- **Q1 Phạm vi F11:** chỉ hai biểu hiện `ann-empty` và `duplicate`.
- **Q2 Khoá đích:** chốt theo số đo. Không thêm vế stale vào V28.
- **Q3 Write set, ngoại lệ:** W1–W4; cấp lại hai ngoại lệ bundled và manifest. Phần "routine, reviewer Claude" của Q3 bị Q5 thay.
- **Q4 Định danh:** Issue #433 revision 11.
- **Q5 (E3, sau finding F1 của review r1):** `sensitive`, kèm Codex review.
- **Q6 Uỷ quyền:** phiên soạn được đăng lên #433 comment ngoại lệ E2 và lease r11 g1 neo `spec_hash`, rồi thi công, đẩy nhánh code và mở PR nháp. Merge theo nghĩa vụ land của protocol (xem dòng `reviewer`).
- **Q7 (E1, sau review r3):** chốt phạm vi và ghi nợ (xem §7). Không đổi sang oracle vi sai trong packet này.

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

Review độc lập r2 (subagent Claude read-only, 14:01–14:26Z 21-11, trên `978c13ccd`): `request_changes`. Cách xử lý từng finding:

| finding | mức | xử lý ở r3 |
|---|---|---|
| R1 `bundle-gate-fixture-oracle`: bản vá yếu hơn base (`m1`, `m7`) | P1 | `hong()` giữ cả họ đổi độ dài (nối, cắt) bên cạnh họ giữ độ dài. `r11_m1`, `r11_m7` có đích {V24, V27}. Chốt `a7_go_ho_doi_do_dai` đo răng. |
| R2 kiểm `actual_bytes` không có răng | P2 | Có fixture đổi độ dài, và kiểm đủ bốn trường băm/độ dài. `r11_m6` có đích {V24, V27}, chốt `a7_go_bon_truong_bam`. |
| R3 lời khai đóng mức LỚP rộng hơn phép đo (`m2`–`m5`) | P2 | Thêm fixture cắt byte và CRLF. Kiểm `expected_*` trong nhánh stale. `r11_m2`…`r11_m5` vào ma trận. §7 viết lại: ma trận là phép đo, không phải trần. |
| R4 mảnh lạc hai chữ số (`m8`) | P3 | V23 dựng mỗi mảnh lạc một fixture riêng (`_9`, `_10`). `r11_m8` có đích {V23}. |
| R5 A2 không tự kiểm đột biến đơn đích | P3 | Script in `DON_DICH` và tính thiếu là SAI. |
| R6 câu chờ chủ kho không mang mã E | P3 | Dòng `reviewer` và Q6 dẫn §3.2.1 và ADR-0063 (nghĩa vụ land), không phải điểm hỏi. |
| R7 `_gan()` kết thúc ở dòng 74 | P3 | Đã sửa. |

Review độc lập r3 (subagent Claude read-only, 15:09–15:47Z 21-11, trên `ef3e0c006`): `request_changes`. Cách xử lý từng finding:

| finding | mức | xử lý ở r4 |
|---|---|---|
| R3-F1 bản vá yếu hơn base (bỏ qua dòng nối thêm) | P1 | Giữ nguyên văn nhiễu loạn `# sua\n` của base. Thêm luật đơn điệu A6 có phép đo riêng. Hai đột biến `r11_rv3_bo_qua_*` có đích {V24, V27}. Thêm cặp chốt `a7_go_nhieu_loan_base`. |
| R3-F2 họ đa nhiễu loạn và topology bỏ trống (7 đột biến sống trên cả hai cây) | P2 | Q7: ghi nợ `bundled-gate-oracle-to-hop`, ghi nhận bằng 7 ca `no_`. |
| R3-F3 `_gan()` văng `KeyError` khi `SOURCES` là AnnAssign có giá trị | P3 | `_gan()` trả rỗng khi thiếu phép gán chuẩn. Ca `r11_rv3_sources_annassign_gia_tri` có đích {V1, V2, V3, V4, V5, V6, V8} và không văng. Base cho {V1, V2, V3, V8}: C giết mọi thứ base giết, và V4–V6 đỏ do đo dữ liệu rỗng thật, không do văng. |
| R3-F4 số 79 trôi, docstring `va.py` | P3 | Đã sửa. |
| R3-F5 sáu lỗ ngoài phạm vi | P3 | Ghi nợ `bundled-gate-oracle-to-hop`, ghi nhận bằng 6 ca `no_`. |

Review độc lập r4 (subagent Claude read-only, 16:1x–16:46Z 21-11, trên `867243d5e`): `request_changes`. Cách xử lý từng finding:

| finding | mức | xử lý ở r5 |
|---|---|---|
| R4-F1 hồi quy so với base: 7 đột biến chèn rác hình dạng vào mảnh một-fragment (gói `lech`/`lon`), base giết qua V5/V6, C để sống | P1 | Mở rộng V8 ra mọi gói nhiều mảnh (xem M2). Đích của `ann-empty`/`duplicate` giữ {V8} như Q2. Thêm s1–s7 thành ca `r11_rv4_s*`, đích {V8}. |
| R4-F2 A6 khai rộng hơn phép đo; không tính ca VĂNG của base | P2 | A6 viết rõ "trên 125 ca của ma trận". `doi_chieu_don_dieu.py` tính dòng `VANG` của base là "giết" (có phép thử răng). §8 khai giới hạn. |
| R4-F3 13 ca `no_` đúng là nợ | P3 | Không đổi. |
| R4-F4 `_gan()` ở dòng 67–75 | P3 | Đã sửa. |
| g1–g3 (đột biến cổng của reviewer, C giết y như base) | – | Đưa vào ma trận thành ca `r11_rv4_g*`. |

## 10. Nhật ký revision

- r1 (2026-11-21): bản đầu.
- r2 (2026-11-21): xử lý review độc lập r1 (F1–F8) và Q5/Q6.
- r3 (2026-11-21): xử lý review độc lập r2 (R1–R7). Đổi cách đóng lớp: từ liệt kê đột biến sang phủ theo họ nhiễu loạn, mỗi nhiễu loạn một fixture.
- r4 (2026-11-21): E1 (Q7), chốt phạm vi. Xử lý R3-F1, R3-F3, R3-F4. Thêm luật đơn điệu A6. Ghi nợ `bundled-gate-oracle-to-hop`.
- r5 (2026-11-21): xử lý review độc lập r4 (R4-F1: V8 soi mọi gói nhiều mảnh; R4-F2: A6 nói đúng phạm vi và tính ca văng; R4-F4).
