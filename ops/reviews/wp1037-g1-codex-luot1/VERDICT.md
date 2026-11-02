Verdict: request_changes
Reviewed commit: 016852ae7acc22a75bae9505febd1697a1ab79ba
Spec sha256: 253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230

Kết luận: **request_changes** — 1 finding P2 và 2 finding P3; chưa đạt ngưỡng approve của packet.
Head đạt `95/95 · 137/137 · 2/2`, base đạt `94/94 · 137/137 · 2/2`; 139 dòng đột biến xanh giống từng byte
(lệnh và output: `evidence/run_logged.py`, `evidence/compare_green.py`, log chi tiết bên dưới).
Mô phỏng toàn suite m81 → c74 in đúng ngoại lệ/vị trí, giữ `tin_dung_gia`, rc=1
(`evidence/compare_simulation.py` → `evidence/simulation-comparison.json`).

| Mức | Finding | Vị trí trong `ops/bien_nhan_v2_test.py` | Bằng chứng quyết định |
|---|---|---|---|
| P2 | c98-khong-khoa-noi-in-that | 3647–3652; nơi in 3767 | `old_print`: toàn suite vẫn `95/95 · 137/137 · 2/2`, rc=0; log thất bại không còn ngoại lệ/vị trí (`focused-old-print.log`) |
| P3 | c98-bo-sot-tran-mac-dinh | 3656–3658 | Trần mặc định vô hạn: c98 `qua`, đuôi quá trần vẫn hiện, không dấu cắt (`survivor-checks-infinite.log`) |
| P3 | c98-bo-sot-so-dong-nem | 3638–3639 | Đổi số dòng thành 0: c98 `qua`; probe ném dòng 12 lại nhận dòng 0 (`survivor-checks-infinite.log`) |

Lệnh tái hiện, output và hướng vá cho từng finding được ghi đầy đủ ở các mục `- [P2/P3]` bên dưới.
Mọi lệnh dùng đường dẫn tương đối đều chạy từ sandbox chứa tài liệu này, trừ cwd được nêu trong `run_logged.py`.
Mã thoát được ghi theo **tiến trình kiểm** trong các tệp `.log.json`; rc=1 của các phép phản chứng là kết quả cố ý.

Bằng chứng đã được ghi tăng dần dưới đây; các log được dẫn là phép đo mới của lượt review này.

Đo đầu vào: `python3 evidence/preflight.py` → `evidence/preflight.json`.
HEAD = `016852ae7acc22a75bae9505febd1697a1ab79ba`; tree = `6907a286e95a2c6e86c7c08c0ec700dc2a75ef58`.
`sha256sum SPEC.md` → `253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230`.
`git -C cay-kho diff --name-only 757bde561d09738858506aecf5de2f050a5f0d5e HEAD` → chỉ `ops/bien_nhan_v2_test.py`.
`git diff --check` trên cùng hai mốc → rc=0, stdout rỗng; diff `ops/bien_nhan_v2.py` → rỗng.
`git config core.abbrev 7` đã chạy trước đo. Các lệnh kiểm Python qua `evidence/run_logged.py` đặt
`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
Base được giải nén bằng `git archive` đúng OID, bổ sung bản sao `.git` và đặt HEAD/index của **bản sao** về base để giữ phép kiểm lịch sử.

Đo phản chứng vòng đầu: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py` (bản sao đủ cây `copies/mutations`, từng patch riêng trong `evidence/`).

| Đột biến | rc probe | Phân hạng c98 | Chốt/output |
|---|---:|---|---|
| `no_location` | 1 | `giet_that` | thiếu vị trí ném (tệp:dòng in hàm): 'AttributeError: thuoc_tinh_1037_vang' |
| `empty_detail` | 1 | `giet_that` | dòng đầu phải nêu tt: [] |
| `formatter_drops_detail` | 1 | `giet_that` | dòng in của đột biến KHÔNG đạt thiếu ngoại lệ thật: ['  KHÔNG RĂNG mX                                     → cY = tin_dung_gia  (mo ta)'] |
| `no_cap` | 1 | `giet_that` | vượt trần phải cắt và nói đã cắt: '      chi tiết [tin_dung_gia]:\n        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxDUOI_BI_CAT' |
| `first_line_only` | 1 | `giet_that` | chi tiết mất dòng `dong-2 ngu canh`: ['      chi tiết [tin_dung_gia]:', '        dong-1 loi that'] |
| `detail_on_pass` | 1 | `giet_that` | đột biến ĐẠT không được in thêm chi tiết |
| `outermost_frame` | 1 | `giet_that` | thiếu vị trí ném (tệp:dòng in hàm): 'AttributeError: thuoc_tinh_1037_vang [ném tại bien_nhan_v2_test.py:3666 in _chay_1]' |
| `wrong_line` | 0 | `qua` | SỐNG: qua |
| `default_cap_disabled` | 0 | `qua` | SỐNG: qua |
| `old_print` | 0 | `qua` | SỐNG: qua |

Bảy mutant ĐỎ đều là `giet_that`, không phải `tin_dung_gia`; `_CA` sau chạy = null, `global_changes=[]`, `env_changed=false` trong từng output probe. Ba mutant SỐNG có phép đo bổ sung ở dưới.

Đo trạng thái lồng: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/state_checks.py` → `evidence/state-checks.log`, rc=0.
Ba lần chạy c98 gốc: `qua`; gọi trực tiếp với `_CA=outer_sentinel` giữ nguyên sentinel. Bản sao chèn
`bang(False, "review_after_nested_call")` ngay sau khối `finally` của lời gọi lồng: 3/3 `giet_that`,
`ca_nguon=outer_sentinel` khi gọi trực tiếp. Đối chứng bỏ `_CA = ca_ngoai`: 3/3 `tin_dung_gia`, `ca_nguon=null`.
Cả ba phép: `changed_globals=[]`, `changed_product_globals=[]`, `environment_changed=false`,
`temp_mutation_dirs=[]`, `_CA=null` sau wrapper. Không thấy rò rỉ trong các bề mặt trạng thái đã đo này;
không suy thành bảo đảm cho mọi trạng thái ngoài phép đo.

Đo ruff: chạy `ruff check --no-cache --select F --output-format json ops/bien_nhan_v2_test.py`
qua `evidence/run_logged.py` ở head và base; cả hai rc=1, cùng một F541 vốn có (base:1677, head:1678).
`python3 evidence/check_ruff.py` → `base_count=1, head_count=1, added=[], removed=[]`; delta=0,
so theo mã/thông điệp/cột, bỏ dịch số dòng do import mới. Raw JSON: `evidence/{head,base}-ruff.json`.

Cổng: `python3 evidence/run_logged.py cay-kho evidence/doctrine.log python3 .claude/dev/packet_loop.py doctrine-scan --root .`
→ rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
`python3 evidence/run_logged.py cay-kho evidence/receipts.log python3 ops/bien_nhan_v2.py --root .`
→ rc=0, `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`.

Finding và hướng vá:

- [P2] c98-khong-khoa-noi-in-that: `ops/bien_nhan_v2_test.py:3647` (lời khai “dây nối”), `:3767` (nơi in thật) — `python3 evidence/run_logged.py . evidence/focused-old-print.log python3 evidence/focused_stdout.py copies/mutations` — c98 vẫn `qua` khi thay duy nhất lệnh in của `do()` bằng lệnh cũ; probe m81 dùng nguyên thân `do()` thực tế in `KHÔNG RĂNG ... = tin_dung_gia` nhưng `exception_visible=false`, `location_visible=false`, rc=1. Đối chứng `copies/state` in đủ tên lỗi/thông điệp/vị trí, cùng phân hạng và rc. — Hướng vá: cho ca mới thu stdout của đường thực thi có `do()` và một đột biến giả thất bại; kiểm cả chi tiết lẫn một dòng duy nhất khi đạt. Có thể tách phần thực thi/in một kết quả thành helper dùng chung, nhưng ca phải đi qua nơi phát stdout. Khóa bằng chính mutant `evidence/old_print.patch`; không chỉ kiểm list từ formatter. Khi sửa, giữ khôi phục `_CA`, `bnv2`, `CONG`, danh sách ca và thư mục tạm; tránh để ca mới gọi đệ quy toàn suite.

Phép đo stdout tập trung ở trên chỉ chọn lời gọi m81 bằng AST; giữ nguyên toàn bộ AST của `do()` và kiểm bằng `ast.dump`.
Không thay `print`/formatter trong probe; ca c74 giả ném `AttributeError` chỉ khi `bnv2 is not _BNV2_THAT`.
Log đối chứng: `AttributeError: laptop_1037_missing_attribute [ném tại focused_stdout.py:20 in simulated_c74]`.
Kết quả toàn suite của mutant `old_print` được ghi ở phần xác nhận bên dưới.

Toàn suite gốc hoàn tất:

- `python3 evidence/run_logged.py cay-kho evidence/head-suite.log python3 ops/bien_nhan_v2_test.py` → rc=0, `95/95 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`.
- `python3 evidence/run_logged.py copies/base evidence/base-suite.log python3 ops/bien_nhan_v2_test.py` → rc=0, `94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`.
- `python3 evidence/compare_green.py` → `mutation_block_byte_equal=true`, `mutation_lines_base=139`, `mutation_lines_head=139`, `full_log_equal_after_only_new_case_normalization=true`. Toàn bộ 139 dòng đột biến giống từng byte, không thêm dòng chi tiết khi đạt. Toàn log chỉ khác số ca ở đầu, dòng c98 và tử/mẫu số ca ở tổng kết (`evidence/base-head-log.diff`).

Phản chứng bổ sung về các giá trị mà c98 chưa khóa:
`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 evidence/survivor_checks.py`
→ các output trong `evidence/survivor-checks-infinite.log`.

- [P3] c98-bo-sot-tran-mac-dinh: `ops/bien_nhan_v2_test.py:3656` — lệnh probe trên, biến thể `default_cap_infinite` thay `_TRAN_CHI_TIET = 2000` bằng `float("inf")` trong bản sao đủ cây — `c98=["qua", null]` nhưng gọi formatter như đường thực tế (không truyền `tran`) với 2000 ký tự và đuôi sentinel cho `tail_visible=true, cut_marker=false`; đối chứng `tail_visible=false, cut_marker=true`. — Hướng vá: thêm phép đo qua formatter/nơi in với `ct` vượt trần mặc định và không truyền `tran`, đòi phần trong trần còn nguyên, đuôi biến mất, dấu cắt và số ký tự dư đúng. Ca đang có chỉ khóa nhánh `tran=50`, nên bỏ trần mặc định vẫn sống. Chạy mutant vô hạn cùng mutant bỏ nhánh cắt; giữ lời gọi đạt không in thêm gì và tránh oracle tự lấy trần vô hạn từ chính hàm cần kiểm.
- [P3] c98-bo-sot-so-dong-nem: `ops/bien_nhan_v2_test.py:3638` — cùng lệnh, biến thể `wrong_line` thay `{f.lineno}` thành `{0}` — `c98=["qua", null]`, phép ném độc lập ở dòng 12 lại trả `survivor_checks.py:0 in inner_throw`; đối chứng trả đúng dòng 12. — Hướng vá: xác định dòng `raise` của fixture bằng code object/line metadata độc lập với `_vi_tri_nem`, rồi so cả `tệp:dòng in hàm`, không chỉ tên tệp và hàm. Giữ fixture có hơn một khung để mutant lấy khung ngoài cùng vẫn đỏ. Tránh hardcode số dòng của tệp test lớn vì thêm import sẽ gây đỏ giả.

Hai mutant giá trị này đã đo qua c98 và probe độc lập, **chưa** chạy toàn suite riêng; không khẳng định sống toàn suite.

Xác nhận finding P2 trên **toàn suite**:
`python3 evidence/run_logged.py copies/mutations evidence/old-print-suite.log python3 ops/bien_nhan_v2_test.py`
→ rc=0, `95/95 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`.
`evidence/old-print-full-comparison.json` ghi `old_print_full_suite_log_byte_equal_to_head=true`.
Mutant bỏ hẳn lời gọi hàm mới tại `do()` SỐNG toàn suite, trong khi mất toàn bộ chi tiết trên log thất bại đã đo ở `focused-old-print.log`.

Đo thêm các nhánh của nơi in (dùng nguyên thân `do()` với ca giả, không gọi toàn suite):
`python3 evidence/run_logged.py . evidence/failure-modes.log python3 evidence/failure_modes.py` → rc=0.
`normal_pass`: `lines=1, detail_lines=0`; `dirty_control`: `KHÔNG RĂNG`, có cả `control first line` và
`control second line`, cùng đủ hai dòng lỗi gốc; `selfcheck_red`: `TỰ KIỂM ĐỎ`, có `chi tiết [giet_that]`
và đủ hai dòng; `scaffold_error`: `chi tiết [gian_giao]` và đủ hai dòng. Phép đo này xác nhận lý do
đối chứng không sạch vẫn xuất hiện ở dòng mô tả, và các nhánh thất bại hiện tại phát chi tiết.

Mô phỏng laptop **toàn suite** hoàn tất, trên hai bản sao đủ cây:
`PYTHONDONTWRITEBYTECODE=1 python3 evidence/setup_simulation.py` chèn vào đầu c74 điều kiện
`bnv2 is not _BNV2_THAT` rồi ném `AttributeError("laptop_1037_missing_attribute")`; không đổi sản phẩm.
Patch nằm trong `evidence/laptop-{head,base}.patch`; setup báo `full_tree=True`, dòng ném head=2753/base=2752.

- `python3 evidence/run_logged.py copies/simulation-head evidence/simulation-head-suite.log python3 ops/bien_nhan_v2_test.py` → rc=1, `95/95 ca đạt · 136/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐỎ`.
- `python3 evidence/run_logged.py copies/simulation-base evidence/simulation-base-suite.log python3 ops/bien_nhan_v2_test.py` → rc=1, `94/94 ca đạt · 136/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐỎ`.
- `python3 evidence/compare_simulation.py` → mỗi bên đúng 1 mutant không đạt, cùng dòng `KHÔNG RĂNG m81_bo_chot_no_chet → c74_A5_no_cau_lich_su_chi_co_va_no_chet_la_vi_pham = tin_dung_gia`. Base không có dòng chi tiết; head in ngay bên dưới:

```text
      chi tiết [tin_dung_gia]:
        AttributeError: laptop_1037_missing_attribute [ném tại bien_nhan_v2_test.py:2753 in c74_A5_no_cau_lich_su_chi_co_va_no_chet_la_vi_pham]
```

Tên ngoại lệ, thông điệp và vị trí ném đúng đều có; phân hạng và mã thoát giữ nguyên.
Raw log và kết quả máy đọc: `evidence/simulation-{head,base}-suite.log`, `evidence/simulation-comparison.json`.

Đọc lại tính toàn vẹn: `python3 evidence/final_integrity.py` → HEAD không đổi; status, diff worktree và
index rỗng, rc=0; `git diff --check` rc=0; danh sách file đổi vẫn chỉ `ops/bien_nhan_v2_test.py`.
Bytes của cả hai `ops/bien_nhan_v2*.py` trong `cay-kho` bằng blob HEAD; chi tiết/băm trong `evidence/final-integrity.json`.

KHÔNG ĐO ĐƯỢC: chạy Windows thật và CI của exact SHA; không có log độc lập tương ứng trong các phép đo này.
Không dùng kết quả mô phỏng để khẳng định đã tái hiện nguyên nhân lỗi laptop hay đã đạt Windows/CI.
Không cấp quyền merge/land.
