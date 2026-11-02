Verdict: approve
Reviewed commit: 91466322f705658ed51b80c7c152f6b77f4f90c6
Spec sha256: 253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230

Kết luận: **approve** — không phát hiện finding P0/P1/P2/P3 còn mở trong phạm vi đo.
Ba finding lượt 1 đã được xác minh vá thật bằng đúng mutant cũ và đúng chốt c98
(`evidence/mutations-results.json`, bảng đối chiếu bên dưới).
Head đạt `95/95 · 137/137 · 2/2`; 139 dòng đột biến đạt giống base từng byte
(`evidence/{head,base}-suite.log`, `evidence/green-comparison.json`).
Không thấy rò trạng thái ở bảy kịch bản đã đo, gồm sáu điểm lỗi cưỡng bức;
mutant sống và giới hạn phép đo được ghi riêng bên dưới (`evidence/state-head.json`).

| Finding còn mở | Vị trí — lệnh tái hiện — output — hướng vá |
|---|---|
| Không có P0/P1/P2/P3 | Các bằng chứng và giới hạn được ghi ở từng mục dưới. Không đề xuất sửa mã ứng viên. |

Lệnh trong báo cáo tính từ sandbox này. Tất cả tiến trình đo đặt
`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
Chỉ thử đột biến trên bản sao đủ cây; không sửa nguồn `cay-kho`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-LUOT1.md`, reviewed commit `016852ae7acc22a75bae9505febd1697a1ab79ba`.
Kết quả lượt 2: **ĐÃ VÁ THẬT** cả ba lớp `c98-khong-khoa-noi-in-that`,
`c98-bo-sot-tran-mac-dinh`, `c98-bo-sot-so-dong-nem` trong phạm vi đã nêu.
Phép đo mới trên exact head lượt 2 ở bảng dưới; không dùng kết quả executor hay kết quả cũ làm bằng chứng pass.

Đo đầu vào: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/preflight.py` → `evidence/preflight.json`; HEAD/spec khớp ba dòng đầu; tree `c20eace3f4aacea3f33afc5861688cb94d64cf3d`; scope chỉ `ops/bien_nhan_v2_test.py`; `git diff --check` rc=0, diff sản phẩm rỗng; hai patch packet khớp byte. Ba bản sao đầy đủ `copies/head`, `copies/base`, `copies/mutations` đều đặt `git config core.abbrev 7` trước đo.

Lệnh phản chứng: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py`; mỗi mutant chạy tiến trình mới `python3 evidence/probe_c98.py copies/mutations`. Bản vá từng mutant: `evidence/<tên>.patch`; output `evidence/<tên>.json`.

| Slug lượt 1 | Mutant | Kết quả lượt 2 / đúng chốt c98 |
|---|---|---|
| `c98-khong-khoa-noi-in-that` | `old_print` | rc=1; `giet_that`; stdout của `do()` thiếu ngoại lệ/vị trí `bien_nhan_v2_test.py:3677 in _c74_gia`: ['  KHÔNG RĂNG m81_bo_chot_no_chet                    → c74_A5_no_cau_lich_su_chi_co_va_no_chet_la_vi_pham = tin_dung_gia  (A5: nợ chết không bị bắt)'] |
| `c98-bo-sot-tran-mac-dinh` | `default_cap_infinite` | rc=1; `giet_that`; trần mặc định 2000 không cắt đúng: …'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyDUOI5' |
| `c98-bo-sot-so-dong-nem` | `wrong_line` | rc=1; `giet_that`; vị trí ném phải là khung TRONG CÙNG `bien_nhan_v2_test.py:3633 in _nem_trong`: 'AttributeError: thuoc_tinh_1037_vang [ném tại bien_nhan_v2_test.py:0 in _nem_trong]' |

Cả ba chết ở `c98_TIN_DUNG_GIA_phai_in_DU_ngoai_le_va_vi_tri_nem`, không phải lỗi dựng fixture. Đối chứng không đổi mã: rc=0, `qua`, stdout rỗng.

Cổng đã đo: `python3 evidence/run_logged.py copies/head doctrine.log python3 .claude/dev/packet_loop.py doctrine-scan --root .` → rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.

`python3 evidence/run_logged.py copies/head receipts.log python3 ops/bien_nhan_v2.py --root .` → rc=0, `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`; `TỔNG: ĐẠT`.

Ruff: `python3 evidence/run_logged.py copies/{head,base} {head,base}-ruff.json ruff check --no-cache --select F --output-format json ops/bien_nhan_v2_test.py` (hai lệnh riêng) → đều rc=1. `python3 evidence/compare_checks.py` → ruff 0.16.9; mỗi bên 1 F541, `added=[]`, `removed=[]`, delta=0. Chuẩn hóa mã/thông điệp/cột, bỏ dịch số dòng; JSON thô giữ đủ vị trí.

## PHẦN MỚI — trạng thái lồng và phản chứng

`python3 evidence/run_logged.py . state-checks.log python3 evidence/state_checks.py copies/head`
→ rc=0; `evidence/state-head.json` ghi bảy kịch bản: thành công (c98 ×3), lỗi trước `_dot_bien`,
sau nạp module đột biến, sau lời gọi lồng thứ nhất/thứ hai, trong đối chứng, và lúc phát dòng in của `do()`.
Sáu lỗi đều là `RuntimeError: review_fault_<điểm tiêm>` được bắt bởi probe ngoài c98.
Từng kịch bản: `bnv2_same`, `CONG_same`, `CA_same`, `CA_entries_same`, `_CA_restored`,
`temp_list_same`, `temp_entries_same`, `stdout_same` đều `true`; `product_changed=[]`,
`temp_dirs_remaining=[]`, `environment_changed=false`, stdout ngoài rỗng. `_CA` trực tiếp giữ sentinel;
sau ca tiếp theo qua `_chay_1` trở lại null. Ca c74 tiếp theo = `["qua", null]` và ca chốt tiếp theo =
`["giet_that", "review_expected_provenance"]`. Không thấy rò ở các trạng thái/điểm lỗi đã đo;
không khẳng định mọi trạng thái ngoài các phép đo này.

`python3 evidence/run_logged.py . focused-stdout.log python3 evidence/focused_stdout.py`
→ rc=0; `evidence/focused-stdout.json`: mô phỏng m81/c74 `AttributeError` qua `_dot_bien` thật cho
`tin_dung_gia`, `exception_visible=true`, `location_visible=true`; ca thật in đúng 1 dòng, kết quả đạt.
`chi=set()` trả `[]`, stdout 0 dòng; chọn m1+m81 trả đúng 2 hàng, 2 dòng. Đối chứng bẩn: `dat=false`,
stdout có `KHÔNG sạch hoàn toàn`, cả `review_control_line1`, `review_control_line2`, và `chi tiết [giet_that]`.

Các mutant dưới đây dùng cùng lệnh `python3 evidence/mutations.py`, probe chỉ chạy c98,
output đầy đủ trong `evidence/mutations-results.json`. “SỐNG” ở bảng này chỉ có nghĩa c98 trả `qua`,
không tự khẳng định toàn suite xanh.

| Mutant mới | Kết quả | Chốt / lý do |
|---|---|---|
| `drop_redirect` | CHẾT, rc=1, `giet_that` | `stdout của do() thiếu ngoại lệ/vị trí …: []`; 3 dòng nội bộ bị lọt ra stdout ngoài |
| `extra_green_line` | CHẾT, rc=1, `giet_that` | `đột biến ĐẠT qua do() phải in đúng một dòng`; thực tế 2 dòng |
| `chi_skips_requested` | CHẾT, rc=1, `giet_that` | `_dot_bien(chi=…) phải chạy đúng m81… và ra tin_dung_gia: []` |
| `drop_restore_ca` | SỐNG, rc=0, `qua` | Lời gọi thứ hai gán lại c74 thật nên che mất lần khôi phục thứ nhất ở luồng thành công |
| `drop_restore_outer_ca` | SỐNG, rc=0, `qua` | Các chốt đều đạt; `_chay_1` ngoài cùng xóa `_CA`, che việc mất sentinel trong c98 |
| `drop_count_guard` | SỐNG, rc=0, `qua` | Chỉ xóa chốt, không làm `do()` hiện tại in sai |
| `extra_green_line_without_guard` | SỐNG, rc=0, `qua` | Phản chứng kép: thêm dòng và xóa chốt đếm; xác nhận chốt hiện tại cần thiết |
| `chi_main_only_m81` | SỐNG qua c98, rc=0, `qua` | Probe c98 không gọi main; dùng so log/số hàng head-base để đo đường main |

`python3 evidence/run_logged.py . state-mutants.log python3 evidence/state_mutants.py`
→ rc=0 (probe thu kết quả, không phải nhãn mutant chết); `state-drop_restore_ca.json` cho thấy
bỏ `CA[i] = c74_that` làm `CA_entries_same=false` và ca sau thành `tin_dung_gia` khi lỗi ở
`before_nested`, `after_load`, `after_nested_1`, `during_print`. Head nguyên vẹn ở cả bốn điểm
có `CA_entries_same=true`, ca sau `qua`.
`state-drop_restore_outer_ca.json` đo được `_CA_restored=false` ngay cả ở luồng thành công
và các lỗi sau ca lồng. Head nguyên vẹn giữ sentinel ở tất cả điểm này.
Đây là giới hạn độ phủ của c98 với các mutant xóa cơ chế kiểm/khôi phục; phép đo lỗi cưỡng bức độc lập
phân biệt được chúng với head. Không coi việc xóa chính chốt kiểm rồi sống là một vi phạm M1–M3
của head đang có chốt và đã vượt đối chứng. 

A2 bổ sung: mutant `no_location` chết tại chốt vị trí khung trong cùng; `no_cap` chết tại
`vượt trần phải cắt và nói đã cắt` (`evidence/{no_location,no_cap}.json`, rc=1, `giet_that`).

## Toàn suite và đường main

- `python3 evidence/run_logged.py copies/head head-suite.log python3 ops/bien_nhan_v2_test.py`
  → rc=0; `95/95 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`.
- `python3 evidence/run_logged.py copies/base base-suite.log python3 ops/bien_nhan_v2_test.py`
  → rc=0; `94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`.
- `python3 evidence/compare_checks.py` → `byte_equal=true`, `base_lines=139`, `head_lines=139`,
  `detail_lines_head=0`, `full_log_equal_after_only_new_case_normalization=true`.
  Cả khối đột biến có SHA-256 `fdc23ad4c17b1834e8b8b002dd5c05a521486060960d9adc27854682feca9485`.
  Diff toàn log chỉ thêm c98 và đổi số ca 94→95 (`evidence/base-head-log.diff`).
  Như vậy main ở head không chạy thiếu đột biến do tham số `chi`; cả tên, thứ tự, số hàng và byte log đều khớp base.

## Đọc lại tính toàn vẹn và phần chưa đo

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/final_integrity.py` → rc=0,
`evidence/final-integrity.json`: HEAD/tree/spec không đổi; status bao gồm tracked/untracked/ignored rỗng;
worktree diff/index diff rỗng; `git diff --check` rc=0; scope vẫn chỉ `ops/bien_nhan_v2_test.py`.
Hai tệp `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py` khớp blob HEAD và bản sao đã chạy suite.
Đây là phép đọc lại trạng thái cuối; không suy thành theo dõi mọi thao tác ghi trong lịch sử tiến trình.

**KHÔNG ĐO ĐƯỢC:** Windows thật và CI trên exact SHA; các lệnh/hiện vật ở trên không cung cấp kết quả đó.
Mô phỏng AttributeError chỉ xác nhận log và phân hạng, không xác nhận nguyên nhân lỗi laptop.
Không cấp quyền merge/land.
