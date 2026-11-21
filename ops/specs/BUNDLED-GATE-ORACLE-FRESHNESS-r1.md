tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

# BUNDLED-GATE-ORACLE-FRESHNESS r1: vá oracle cổng (F10) và oracle hình dạng AST (F11) trong fragment `wp433_bundled_tach_manh`

| trường | giá trị |
|---|---|
| `packet_id` · `packet_issue` | `wp433`, revision **11**, `spec_packet_id: BUNDLED-GATE-ORACLE-FRESHNESS`. Issue **#433** (Q4, chủ kho chốt 2026-11-21). Revision 10 là SECRETS-SET-BUNDLE-KIEU (PR #1490 đã merge). |
| `nguon_cap_viec` | Mục sổ `xet_lai_cach_lam` của chủ kho: https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7058076373. Mục này chuyển F10 thành nợ `bundled-gate-oracle-freshness` (làm ở packet nhỏ riêng) và F11 thành nợ `bundled-tach-manh-do-min-ve`. Nguồn finding: verdict lượt 3 `ops/reviews/bundled-tach-manh-cr/luot3-codex-5293a85.txt` @ `3f5641c8cd93ace4bc786dc8d19c1be7468983ba`, sha256 `360c8a4fe56a58a40e4bf8e6292ac03d297060db831ac3104b519e6b13cc4b12` (đo lại 12:30Z 21-11: khớp). |
| `phu_thuoc` | Không. Packet cha BUNDLED-TACH-MANH r9 đã land qua PR #1485. |
| `review_class` | `routine` (Q3): thay đổi chỉ nằm trong một test fragment và hai tệp phái sinh của nó. Packet không đụng `scripts/tl_core/release.py`, `scripts/tl_core/test_fragments.py`, workflow hay cổng cấp quyền. Classifier/dispatcher được nâng lớp theo §8 protocol; executor không được hạ lớp. |
| `reviewer` | Phiên Claude mới, độc lập, read-only, trên exact SHA ứng viên (Q3). Không dự kiến lời gọi Codex review PR. Nếu cần thì trần theo dòng khai `ADR-0055` ở đầu tệp. |
| `base` | `29c22f7d1f92321978d4d1dff16bd80d9ea744e0` (`origin/master`, đo 13:14Z 21-11). Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. |

Các quyết định Q1–Q4 do chủ kho chốt ngày 2026-11-21 (§9).

## 0. Hiện trạng (đo trên `29c22f7d`, 12:31–12:33Z 21-11)

Probe chạy bằng `python -B probe.py <repo> <commit> <mutant>` (trong scratch của phiên soạn, không vào kho). Mỗi lượt `git archive` thư mục `scripts/` vào thư mục tạm, áp đúng một đột biến bằng thay chuỗi duy nhất (`count == 1`), rồi gọi `run(tl)` của fragment trong tiến trình mới. Mỗi lượt trả đủ 32 khoá.

| đột biến | thay đổi | `run()` | khoá đỏ |
|---|---|---|---|
| đối chứng | không | True | — |
| `size-only` | `release.py`: cổng chỉ so `len(a) != len(d)` thay `a != d` | **True** | — (lọt) |
| `one-stale-ok` | `release.py`: payload stale có thêm `"ok": len(expected_modules) == 1` ⇒ CLI rc 0, `ok: true`, `status: stale` | **True** | — (lọt) |
| `ann-empty` | `test_fragments.py`: mảnh 1 của gói nhiều mảnh có thêm dòng `X: int` sau `BUNDLED_FRAGMENT_SHARDS` | False | V4 V5 V6 V8 V9 (`ValueError: malformed node or string: None`) |
| `duplicate` | `test_fragments.py`: mảnh 1 của gói nhiều mảnh có thêm `BUNDLED_FRAGMENT_SOURCES = ()` sau `BUNDLED_FRAGMENT_SHARDS` | False | V4 V5 V6 V8 |

Kết quả này khớp verdict lượt 3: `(0, True, 'current', None)` cho `size-only` và `(0, True, 'stale', 'GENERATED_BUNDLE_STALE')` cho `one-stale-ok`. Cổng nguyên bản trả `(2, False, 'stale', 'GENERATED_BUNDLE_STALE')`.

Nguyên nhân, đọc trên `scripts/test_fragments/wp433_bundled_tach_manh.py` tại base:

- `hong()` (dòng 185–186) làm stale bằng cách NỐI THÊM `b"# sua\n"`, nên độ dài luôn đổi. Hàm này chỉ trả `[3].get("error")`. V24 (dòng 263) và vế stale của V27 (dòng 201) chỉ so mã lỗi, không so rc, `ok` hay `status`.
- `_gan()` (dòng 67–74) gọi `ast.literal_eval` cho MỌI nút có đích `Name`. Với `AnnAssign` không giá trị, `n.value` là `None` nên lời gọi văng. Dict comprehension để lần gán SAU ghi đè lần gán trước. Phép đọc hình dạng (`ten`) và phép đọc dữ liệu (`gan`) dùng chung một vòng duyệt, nên lỗi đọc dữ liệu kéo đỏ cả các khoá chỉ cần dữ liệu (V4, V5, V6, V9).

Vị trí mảnh (đo 12:34Z): fragment nằm ở `scripts/tl_test_fragments_bundled.py` (170.024 B; `_BUNDLED_SHARD_LIMIT` 196.608 B). `scripts/tl_test_fragments_bundled_2.py` dài 142.890 B.

Phép đo nguyên mẫu (chỉ để chứng minh khả thi; executor tự viết bản vá, không bắt buộc theo nguyên mẫu): sửa `hong()` theo M1 và `_gan()` theo M2 trên bản sao base. Kết quả 12:33Z: đối chứng `run()` True với 32/32 khoá. `size-only` đỏ {V24, V27}. `one-stale-ok` đỏ {V27}. `ann-empty` đỏ {V8}. `duplicate` đỏ {V8}. Numstat ước tính của fragment là +12/−5.

## 1. `write_set`

| # | đường dẫn | cách đổi |
|---|---|---|
| W1 | `scripts/test_fragments/wp433_bundled_tach_manh.py` | sửa tay |
| W2 | `scripts/tl_test_fragments_bundled.py` | CHỈ sinh bằng `write_bundled_modules` (ngoại lệ bundled, Q3) |
| W3 | `scripts/tl_test_fragments_bundled_2.py` | CHỈ sinh bằng `write_bundled_modules` (ngoại lệ bundled, Q3). Dự kiến không đổi vì W1 ở mảnh 1. Ranh mảnh trôi thì được phép đổi, theo `hinh_dang_ke_thua` của r9 §7. |
| W4 | `RELEASE_MANIFEST.json` | CHỈ sinh bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json`, và phải là commit CUỐI của SHA ứng viên (ngoại lệ manifest, Q3). Tệp này đổi vì W1 và W2 nằm trong manifest (CLAUDE.md §Quy ước deploy mục 5). |

Không có tệp thứ năm. Phải sửa tệp ngoài W1–W4 (kể cả ghim số đếm trong `scripts/tl_selftest.py`) thì DỪNG, theo §6.

Trần kích thước theo `ADR-0044` cho `routine`. Ước tính: 4 đường, khoảng 20 dòng thêm.

## 2. `ngoai_pham_vi`

- Các phần chia mịn khác của V1–V32 trong nợ `bundled-tach-manh-do-min-ve` (R6-02..05, các phần chia mịn của R6-01/R6-06). Chủ kho chốt ở Q1 chỉ vá hai biểu hiện F11. Nợ ấy vẫn mở cho phần còn lại.
- Mã sản phẩm `scripts/tl_core/release.py` và `scripts/tl_core/test_fragments.py`. Reviewer lượt 3 đã đo cổng thật từ chối đúng cả hai ca F10, nên lỗi nằm ở oracle.
- Khoảng đua kiểm-rồi-mở và link đứt tại tên thư mục `test_fragments` (verdict lượt 3, mục B.3). Hai điểm này không thuộc F10/F11.
- Đổi số khoá: tập nghiệm thu vẫn là đúng 32 khoá V1–V32 với nghĩa như r9 §4. Packet chỉ làm phép đo mạnh hơn, không thêm và không bớt khoá.
- Windows native: MIỄN, cùng lý do r9 §4c (chỉ dùng `pathlib` và AST/JSON, không API riêng nền).

## 3. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | `hong()` làm stale bằng một thay đổi byte GIỮ NGUYÊN độ dài tệp mảnh, và trả quyết định CLI đủ bốn trường `(rc, ok, status, error)`. V24 (mảnh chính và mảnh phụ của gói ba mảnh) và vế stale của V27 (gói một mảnh) đòi đúng `(2, False, "stale", "GENERATED_BUNDLE_STALE")`. | W1 |
| M2 | Tách đọc hình dạng khỏi đọc dữ liệu trong `_gan()`. Hình dạng (`ten`, dùng cho V3/V8) giữ nguyên nghĩa: danh sách nút thân sau một docstring đầu. Dữ liệu (`SOURCES`/`SHARDS`, dùng cho V4/V5/V6/V9/V31) chỉ đọc từ phép gán CHUẨN: `ast.Assign` có đúng một đích `ast.Name` mang đúng tên. Mỗi tên chỉ lấy lần gán chuẩn ĐẦU TIÊN. `AnnAssign`, phép gán nhiều đích và lần gán lặp lại không đổi dữ liệu đọc được và không làm hàm văng. | W1 |
| M3 | Tái sinh bundle từ cây đã sửa bằng `write_bundled_modules`. | W2, W3 |
| M4 | Tái sinh manifest làm commit cuối. | W4 |

## 4. `nghiem_thu`

Mọi phép đo chính thức chạy trên SHA ứng viên C (commit cuối là manifest), trên clone ĐẦY ĐỦ (`--is-shallow-repository` = `false`, có object `358451e8`). Base và C được dựng bằng HAI clone trong MỘT lệnh, giống `ops/handoff/wp433/r9-g5/do_n3.sh` @ `bf38a110`. Mỗi lệnh ghi rc, giờ UTC và đầu ra.

| # | tiêu chí | đỏ khi |
|---|---|---|
| A1 | Trên C, `run()` của fragment trả True, đủ 32 khoá, cả 32 True. | `run()` không True, hoặc số khoá ≠ 32, hoặc có khoá False |
| A2 | Đột biến `size-only` (định nghĩa ở §0, thay đúng một chuỗi trong `release.py` của BẢN SAO C): `run()` False, không văng, đủ 32 khoá, tập khoá False = **{V24, V27}**. Trên base, cùng đột biến cho tập False rỗng (đối chứng lỗ cũ, đo trong cùng lệnh). | tập False trên C ≠ {V24, V27}; hoặc base không tái lập lỗ (tập False khác rỗng) |
| A3 | Đột biến `one-stale-ok` (§0): trên C tập False = **{V27}**. Trên base tập False rỗng. | tập False trên C ≠ {V27}; hoặc base không tái lập |
| A4 | Đột biến `ann-empty` (§0): trên C tập False = **{V8}**, và `_LY_DO` không có khoá nào. Trên base tập False = {V4, V5, V6, V8, V9}. | tập False trên C ≠ {V8}; hoặc có lý do văng; hoặc base không tái lập |
| A5 | Đột biến `duplicate` (§0): trên C tập False = **{V8}**. Trên base tập False = {V4, V5, V6, V8}. | tập False trên C ≠ {V8}; hoặc base không tái lập |
| A6 | Ma trận đột biến g5 (`ops/handoff/wp433/r9-g5/ma_tran_dot_bien.py` @ `bf38a110`, 49 đột biến cộng đối chứng) chạy lại trên C. Thêm bốn đột biến A2–A5 thì thành 53 đột biến cộng đối chứng. Mỗi đột biến chạy trong một tiến trình mới, trả đủ 32 khoá, và tập False BẰNG tập đích khai. Đột biến nào đổi tập đích vì M1/M2 thì khai lại đích trong handoff, kèm lý do theo cơ chế. Mỗi V1–V32 vẫn là đích của ít nhất một đột biến chỉ phá đúng vế ấy. | một đột biến sống, văng, thiếu khoá, hoặc tập False ≠ đích khai; hoặc một khoá mất đột biến đơn đích; hoặc đích bị khai lại mà không có lý do |
| A7 | Chính mã của M1 có răng. Đột biến `hong` nối byte (trả về cách cũ: nối thêm byte, chỉ so `error`) áp lên C thì A2 và A3 đỏ trở lại, tức `size-only` và `one-stale-ok` sống. Đột biến `_gan` đọc rộng (trả về dict comprehension cũ) áp lên C thì A4 và A5 đỏ trở lại. | sau khi gỡ bản vá, A2–A5 vẫn xanh (bản vá không phải thứ tạo ra kết quả) |
| A8 | Gate trên C so với base, cùng lệnh: selftest N/N với hai số bằng nhau và **N = N_base** (packet không thêm ca); `test-fragments-check --json` rc 0, `ok: true`; `.github/checks/bundle_fragment_check.py --json` `ok: true`, `failed: []`, `case_count` = số đo trên base; `release-verify RELEASE_MANIFEST.json --strict --json` trên tệp ĐÃ commit `ok: true`, `expected_file_count == checked_file_count` = số đo trên base; `workflow-audit --strict --json` rc 0, `py_size.fail == []`, `py_size.warn == []`; `golden-test` ok; `.githooks/eol_policy_test.py` N/N bằng base; ruff F trên W1 delta 0 so base; `git diff --check base C`, `doctrine-scan`, `adr-song` rc 0. | bất kỳ vế nào |
| A9 | Đường thay đổi bundle: `git diff --name-only base C` ⊆ {W1, W2, W3, W4}. W2 và W3 trên C trùng BYTE với đầu ra `write_bundled_modules` chạy lại trên C (cũng là điều `test-fragments-check` đo). W4 là thay đổi của commit cuối, và `release-manifest` chạy lại trên C không tạo diff. | một tệp ngoài W1–W4 đổi; hoặc bundle hay manifest lệch đầu ra sinh lại |

Số nền cho A8 (selftest N, `case_count`, `file_count`, EOL N) do phiên soạn đo trên base. Phiên thi hành đo lại trên base thật của lease. Số được ghi ở §8 kèm giờ đo.

## 5. `pham_vi_e`

Không chạm E4/E5. Mọi đo đạc chạy trong thư mục tạm, không mạng, không LIVE, không đẩy Package, không đọc secrets. Packet không đổi danh sách thẩm quyền, cổng cấp lease hay cổng merge.

## 6. `luat_dung`

- Điểm dừng theo `docs/PROTOCOL_DA_PHIEN.md` §12 và bảng trần của `ADR-0055` theo dòng khai ở đầu tệp. Đặc tả không đặt ngân sách mềm.
- Chưa có Issue #433 revision 11 kèm lease còn hiệu lực, cùng comment ngoại lệ bundled và manifest đúng `spec_packet_id` này, thì không thi công (**E2**: quyền cấp ngoại lệ và lease thuộc chủ kho; ngoại lệ comment 7053681301 của r9 KHÔNG chuyển sang).
- Cần sửa tệp ngoài W1–W4, hoặc A8 đòi N ≠ N_base, thì DỪNG và hỏi chủ kho (**E2**: mở write set là quyền của chủ kho), kèm tệp, lý do và phép đo.
- Vượt trần `ADR-0044` cho `routine` thì DỪNG (**E2**), kèm numstat thật.
- §0 lệch trên base thật của lease (hai đột biến F10 không còn lọt, hoặc tập đỏ của F11 khác) thì DỪNG. Giả định của packet đã sai, cần revision mới.
- Đo trên clone nông thì A1–A9 là KHÔNG ĐO ĐƯỢC, không được báo đạt.

## 7. `hinh_dang_ke_thua`

Chép từ hồ sơ tiền nhiệm (verdict lượt 3 và mục sổ 7058076373):

| slug lớp | lịch sử | số lần xuất hiện |
|---|---|---|
| `bundle-gate-fixture-oracle` | F03 `4e74fe1` → F06 `36dc91a` → F10 `5293a85` | 3 lượt review liên tiếp. Lượt này là lần thứ tư lớp được mở, nên reviewer phải quét CẢ LỚP (§8.3), không chỉ hai đột biến đã báo |
| `shard-ast-shape-oracle` | F02 `4e74fe1` → F05 `36dc91a` → F11 `5293a85` | 3 lượt |

Tỷ lệ đóng lớp của chuỗi BUNDLED-TACH-MANH: lượt 1→2 là 1/4, lượt 2→3 là 1/3. Đó là hai chuyển tiếp liền dưới 50% ⇒ Review Rescue Checkpoint (mục sổ 7058076373). Hình dạng lặp của lớp thứ nhất: **mỗi bản vá oracle chỉ bịt đúng đột biến được báo, đột biến cùng lớp mà khác cơ chế (độ dài, trường payload khác) vẫn lọt**. Vì vậy A7 đòi đo răng của chính bản vá, và A6 đòi chạy lại toàn ma trận thay vì chỉ hai đột biến mới.

Hệ quả cho packet khác: không có. Ranh mảnh trôi (r9 §7) vẫn áp: W3 nằm trong write set vì lý do đó.

## 8. `chua_do_duoc` và số đo

- Số nền A8 trên `29c22f7d`, đo 13:15–13:29Z 21-11. Phép đo dùng clone đầy đủ (`shallow=false`), `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`, mỗi lệnh chạy riêng và ghi rc. Cả tám lệnh rc 0:
  - `.githooks/eol_policy_test.py`: **32/32 dat**.
  - `scripts/tl.py --selftest`: **1786/1786**, nên N_base = 1786.
  - `test-fragments-check --json`: `ok: true`, `status: current`, 2 mảnh.
  - `.github/checks/bundle_fragment_check.py --json`: `ok: true`, `failed: []`, `case_count` **20**.
  - `workflow-audit --strict --json`: `ok: true`, `py_size.fail == []`, `py_size.warn == []`, `files_scanned` **74**.
  - `release-verify RELEASE_MANIFEST.json --strict --json`: `ok: true`, `expected_file_count == checked_file_count == 186`.
  - `golden-test --json`: `ok: true`, 20 ca.
  - `ruff check --select F` trên W1: `All checks passed!`.
- CI GitHub trên exact SHA C: chưa đo (chỉ đo được sau push).
- Windows native: miễn (§2).
- Numstat thật: chưa đo. Ước tính 4 đường, khoảng 20 dòng thêm, theo nguyên mẫu §0.

## 9. Quyết định của chủ kho (AskUserQuestion, phiên `session_015Gtxrb38PyN9US77Ccx4us`, 2026-11-21)

- **Q1 Phạm vi F11:** chỉ hai biểu hiện (`ann-empty`, `duplicate`). Phần chia mịn còn lại ở lại nợ `bundled-tach-manh-do-min-ve`.
- **Q2 Khoá đích:** chốt theo số đo nguyên mẫu: `size-only` → {V24, V27}, `one-stale-ok` → {V27}, `ann-empty` → {V8}, `duplicate` → {V8}. Không thêm vế stale vào V28 (V28 không dùng `hong()`).
- **Q3 Write set, ngoại lệ, lớp review:** W1–W4; cấp lại hai ngoại lệ bundled và manifest cho packet này; `routine`; reviewer là phiên Claude mới độc lập.
- **Q4 Định danh và lease:** Issue #433 revision 11, đặc tả ở tệp này. Phiên soạn KHÔNG tự cấp lease; chủ kho cấp. Quét lúc 12:30Z (fetch đủ, `ls-remote` 399 tên khớp bộ đệm 399): người giữ duy nhất của W2–W4 là `wp433-r10-g1-claude`, hết hạn 12:47:06Z 21-11. W1 không có người giữ. Phải quét lại toàn kho trước khi cấp lease.

## 10. Nhật ký revision

- r1 (2026-11-21): bản đầu.
