verdict: approve
reviewed_sha: a16932aa09ce860a614f0bab4b2015699e7221bc
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Đây là kiểm toán sau merge tại đúng SHA nêu trên, tree `d4eea17c04edc0a62c320d4f44cae8290082cf2f`. Ngưỡng áp dụng: không còn finding P0/P1/P2/P3. Không phát hiện finding còn mở trong phạm vi đo; verdict này không cấp quyền merge/land và không xác nhận hồi tố các điều kiện land.

Toàn suite **98/98 ca · 153/153 đột biến thường · 2/2 ca tự kiểm**, rc=0, `TỔNG: ĐẠT`. Cổng thật **tổng 312**, rc=0, `TỔNG: ĐẠT`, khớp phép đếm độc lập. Hai blob packet giống cha 1; không có nội dung cây merge khác cả hai cha. C4/C5/C7 **KHÔNG ĐO ĐƯỢC**, không ghi thành pass.

Môi trường tự đo: `sys.platform=linux`, `os.name=posix`, Python **3.13.17**, Ruff executable **0.16.9**. Hồ sơ `run/5f76b0b7/run.json` ghi `provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine`; đây là dữ kiện của hồ sơ launcher, không phải phép đo model/effort đã phục vụ. Không tự suy thêm danh tính từ tên công cụ.

`cay-kho/` được dùng để đọc và đo; đột biến/fixture/cache nằm ngoài checkout hoặc bị tắt. Snapshot đầu/cuối của **8.972 tệp**, mode, nội dung, HEAD/tree, index entries và tracked/untracked/ignored đều bằng nhau (h15). Hai snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

## BẢNG TIÊU CHÍ

| Tiêu chí | Kết quả đo tại reviewed_sha | Bằng chứng |
|---|---|---|
| M1/M2 | ĐẠT tại chỗ: một helper `iterdir` + `name.lower().endswith`, không `is_file`, trả `sorted`; `kiem` và `_sinh_no` mỗi hàm gọi helper một lần. Thông báo rỗng giữ nguyên nghĩa và ghi rõ so đuôi không phân biệt hoa thường. | h04, h12 |
| C1a | ĐẠT tại chỗ: hai YAML hợp lệ nhưng sai schema ⇒ rc=1, tổng 2, nêu `x.RECEIPT.YAML`, `TỔNG: ĐỎ`; chỉ-x ⇒ rc=1, tổng 1, không thông báo không có tệp. Windows chưa đo. | h04; m142→c101 `giet_that` tại h05 |
| C1b | ĐẠT tại chỗ: YAML hỏng đuôi hoa ⇒ rc=2, stderr nêu `x.RECEIPT.YAML`, không Traceback; không đòi dòng tổng. Windows chưa đo. | h04; c101 sạch tại h10 |
| C2 | ĐẠT tại chỗ: c89 `qua`; thêm `is_file` ⇒ m143→c89 `giet_that`. Thư mục `X.RECEIPT.YAML` qua CLI độc lập ⇒ rc=2, nêu tên, không Traceback. Windows chưa đo. | h04, h10 |
| C3 | ĐẠT tại chỗ: bản sao helper hoàn nguyên về glob ⇒ c101 `giet_that`, tổng chỉ 1; c18 đối chứng vẫn sạch. Không đưa glob vào bảng đột biến thường. | h06 |
| C4 — Windows CI | KHÔNG ĐO ĐƯỢC: cần GitHub Actions/API, bị loại khỏi phạm vi theo ràng buộc không gọi mạng. Không dùng run trên `356a27e` thay cho SHA này. | Không chạy dispatch hoặc đọc API. |
| C5 — Linux CI | KHÔNG ĐO ĐƯỢC: cần GitHub Actions/API; suite tại chỗ không xác minh runner/job/labels/lease-publish của CI. | Không đọc API. |
| C6 | ĐẠT: cổng thật rc=0, 259 ĐẠT v2 + 11 miễn trừ + 42 nợ = tổng 312, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC, `TỔNG: ĐẠT`; đếm độc lập `os.listdir` = 312. Kho không shallow. | h01, h03, h11 |
| C7 — Windows local | KHÔNG ĐO ĐƯỢC: không truy cập ASUS-LAPTOP/Desktop Commander hoặc thư mục Windows trong lượt chỉ đo tại chỗ này. | Không thao tác máy ngoài. |
| C8 | ĐẠT phần nội dung và neo của lượt này: 0 P0/P1/P2/P3 còn mở; `reviewed_sha` đủ 40 ký tự, khớp HEAD đầu/cuối và là cha 2 của merge `c8ff9ed`. Lượt kiểm toán 11 do PROMPT hiện hành yêu cầu; không dùng verdict này để chứng nhận hồi tố trần 4 lời gọi của SPEC, authority hoặc CI/Windows tại thời điểm land. Các phần lịch sử ấy KHÔNG ĐO ĐƯỢC đầy đủ bằng phép đo offline này. | h01, h02, h05, h12, h15; chỉ thị hiện hành PROMPT.md. |
| C9 | Các phép tĩnh ĐẠT: Ruff 0.16.9 base=1/head=1 F541, added=0/removed=0, vị trí khớp sau ánh xạ dòng; doctrine-scan rc=0, 10 tệp/0 chỗ; `git diff --check 3dfb973 HEAD` rc=0; rg glob 0 dòng, tiêm lại một dòng trên bản sao ⇒ 1 dòng. Numstat +40/−5 và +300/−2. | h01, h07, h08, h09, h12. Module Ruff không có trong python3 mặc định; dùng executable cục bộ, không cài đặt. |

## BẢNG SĂN

Mỗi hướng dưới có lệnh và output thực tế; các log được nối vào verdict ngay sau khi phép đo tương ứng kết thúc. Bảng tóm tắt không thay các khối output đầy đủ phía dưới.

| Hướng độc lập | Lệnh/phép đo | Output quyết định | Kết luận |
|---|---|---|---|
| h01 — tính toàn vẹn merge | `python3 evidence/merge.py` | 2 blob HEAD=P1; chỉ 2 tệp khác P2; 0 mục khác cả hai cha; diff.patch khớp byte | KHÔNG PHẢI LỖI |
| h02 — hồi quy toàn suite | `python3 ops/bien_nhan_v2_test.py` tại cay-kho | 98/98 · 153/153 · 2/2; rc=0; TỔNG: ĐẠT | KHÔNG PHẢI LỖI |
| h03 — cổng trên dữ liệu thật | `python3 ops/bien_nhan_v2.py --root .` | tổng 312; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC; rc=0 | KHÔNG PHẢI LỖI |
| h04 — fixture CLI độc lập | `python3 evidence/fixtures.py` | C1a tổng 2/chỉ-x tổng 1; C1b rc=2; sinh nợ thấy x; thư mục rc=2 | KHÔNG PHẢI LỖI |
| h05 — mutant chỉ định | `python3 evidence/mutations.py` | m142/m147/m153/m156/m157: 5/5 giet_that đúng ca đích, đối chứng sạch | KHÔNG PHẢI LỖI |
| h06 — phản chứng hoàn nguyên glob | C3 trong `evidence/mutations.py` | c101 giet_that; tổng 1; c18 sạch | KHÔNG PHẢI LỖI |
| h07 — Ruff so baseline | `python3 evidence/lint.py` | base=1/head=1 F541; added=0/removed=0; vị trí ánh xạ bằng nhau | KHÔNG PHẢI LỖI |
| h08 — doctrine | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 10 tệp; 0 chỗ; rc=0 | KHÔNG PHẢI LỖI |
| h09 — whitespace | `git diff --check 3dfb973 HEAD` | không output; rc=0 | KHÔNG PHẢI LỖI |
| h10 — nhánh lỗi và đường sinh nợ | ca dương + 11 mutant riêng trong `evidence/mutations.py` | c89/c99/c100/c101 qua; 11/11 giet_that | KHÔNG PHẢI LỖI |
| h11/h13/h14 — đếm và đặc tả | `python3 evidence/data_audit.py` | os.listdir=312=CLI; P1=306; SPEC r2 khớp băm | KHÔNG PHẢI LỖI |
| h12 — cấu trúc và nguồn phụ | `python3 evidence/source_audit.py` | helper 1, hai call site; glob 0 dòng/tiêm thành 1; 3 nguồn phụ giống cả hai cha | KHÔNG PHẢI LỖI |
| h15 — snapshot và phân số thật | `python3 evidence/integrity.py` | 8.972/8.972 tệp bằng nội dung/mode; status rỗng; 98 dòng ca ĐẠT | KHÔNG PHẢI LỖI |
| CI/Windows | Không gọi mạng/máy ngoài theo PROMPT | Không có phép đo runner/jobs/local Windows mới | KHÔNG ĐO ĐƯỢC |

### h01 — Neo SHA, đặc tả và tính toàn vẹn merge

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/merge.py
```

OUTPUT THẬT (rc=0):
```text
HEAD=a16932aa09ce860a614f0bab4b2015699e7221bc
tree=d4eea17c04edc0a62c320d4f44cae8290082cf2f
parents=356a27e1378b2162bbc0be2ec06ff08fdacbdead 3dfb9731ceda05afbcec4e803a919c4df5e2e5a2
shallow=false
symbolic-ref rc=1
core.abbrev=7
SPEC.md sha256=d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d
ops/bien_nhan_v2.py: HEAD=416d612ea5be4691fdeaf912c9e55fd9ecb1fbe6 P1=416d612ea5be4691fdeaf912c9e55fd9ecb1fbe6 P2=83ba1d37a902b7064f95e2efb2a2d0f197a81733
ops/bien_nhan_v2_test.py: HEAD=ab1d5a104d896cc13eca681030bb3fc01d1b3f7d P1=ab1d5a104d896cc13eca681030bb3fc01d1b3f7d P2=3b334cf53622cf041a2953c15edf788463bca932
P2..HEAD paths=['ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py']
P2..HEAD numstat:
40	5	ops/bien_nhan_v2.py
300	2	ops/bien_nhan_v2_test.py
union_tree_entries=8972
entries_different_from_both_parents=[]
actual diff sha256=6b0591b75c9a0b4deeac22c775811d5ed49f56384b078a5a97c5e9441cbdd463
diff.patch sha256=6b0591b75c9a0b4deeac22c775811d5ed49f56384b078a5a97c5e9441cbdd463
diff.patch byte_identical=True
```

Log đầy đủ: [evidence/h01.log](evidence/h01.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h03 — Cổng thật tại reviewed_sha

LỆNH:
```sh
cd cay-kho
PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUFF_NO_CACHE=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file python3 ops/bien_nhan_v2.py --root .
```

OUTPUT THẬT (rc=0):
```text

bien_nhan_v2: 259 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 312
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT

[exit_code=0; elapsed_seconds=29.387]
```

Log đầy đủ: [evidence/h03.log](evidence/h03.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h08 — Doctrine scan tại reviewed_sha

LỆNH:
```sh
cd cay-kho
PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUFF_NO_CACHE=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file python3 .claude/dev/packet_loop.py doctrine-scan --root .
```

OUTPUT THẬT (rc=0):
```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine

[exit_code=0; elapsed_seconds=0.515]
```

Log đầy đủ: [evidence/h08.log](evidence/h08.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h09 — Kiểm tra whitespace so cha master

LỆNH:
```sh
cd cay-kho
PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUFF_NO_CACHE=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file git diff --check 3dfb973 HEAD
```

OUTPUT THẬT (rc=0):
```text

[exit_code=0; elapsed_seconds=0.010]
```

Log đầy đủ: [evidence/h09.log](evidence/h09.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h05 — Năm đột biến chỉ định chạy riêng qua _dot_bien_tep và đối chứng

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py
```

OUTPUT THẬT (rc=0):
```text
  CÓ RĂNG    m156_B4_bo_chan_bien_dau_tep           → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (dòng đầu bị mất cửa sổ)
  CÓ RĂNG    m157_B4_trich_dan_bo_dong_sau          → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (trích dẫn ở dòng sau bị bỏ qua)
  CÓ RĂNG    m142_chon_bien_nhan_so_duoi_CHINH_XAC  → c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen = giet_that  (đuôi hoa lại bị bỏ qua lặng)
  CÓ RĂNG    m147_bo_chon_bo_bat_OSError            → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (lỗi liệt kê thoát thành traceback (Codex lượt 1))
  CÓ RĂNG    m153_hoi_trang_thai_bat_Exception      → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (lỗi lập trình ở phép hỏi thư mục bị đổi thành KHÔNG ĐO ĐƯỢC)

5/5 đúng ca đích; 5/5 giet_that; 5/5 đối chứng sạch; 5/5 tệp đột biến ngoài cay-kho; còn bản sao tạm=0
```

Log đầy đủ: [evidence/h05.log](evidence/h05.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h10 — C2 và các nhánh sinh nợ, thứ tự, vắng thư mục, OSError và lỗi lập trình

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py
```

OUTPUT THẬT (rc=0):
```text
c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback = qua; None
c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = qua; None
c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = qua; None
c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen = qua; None
  CÓ RĂNG    m143_chon_bien_nhan_loc_is_file        → c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback = giet_that  (thư mục `*.receipt.yaml` trốn khỏi phép băm)
  CÓ RĂNG    m144_sinh_no_loc_duoi_CHINH_XAC        → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (`--sinh-no` bỏ qua đuôi hoa (đường gọi thứ hai))
  CÓ RĂNG    m145_bo_chon_khong_sap_xep             → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (thứ tự duyệt theo hệ tệp, không sắp xếp)
  CÓ RĂNG    m146_bo_chon_bo_nhanh_thu_muc_vang     → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (`--sinh-no` trên kho thiếu ops/reviews thành lỗi đo)
  CÓ RĂNG    m148_bo_chon_hoi_is_dir_TRAN           → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (`--sinh-no`: EACCES ở `stat` thoát thành traceback)
  CÓ RĂNG    m149_kiem_guard_hoi_is_dir_TRAN        → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (`kiem`: EACCES ở `stat` thoát thành traceback)
  CÓ RĂNG    m150_hoi_trang_thai_bo_bat_OSError     → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (lỗi `stat` thoát thành traceback ở cả hai đường)
  CÓ RĂNG    m151_kiem_hoi_git_TRAN                 → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (`stat` của `.git` thoát thành traceback)
  CÓ RĂNG    m152_bo_chon_bat_Exception             → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (lỗi lập trình ở phép liệt kê bị đổi thành KHÔNG ĐO ĐƯỢC)
  CÓ RĂNG    m154_hoi_trang_thai_chi_bat_PermissionError → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (EIO ở `stat` thoát thành traceback)
  CÓ RĂNG    m155_bo_chon_chi_bat_PermissionError   → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (EIO khi liệt kê thoát thành traceback)
```

Log đầy đủ: [evidence/h10.log](evidence/h10.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h06 — C3 hoàn nguyên glob trên bản sao tạm

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py
```

OUTPUT THẬT (rc=0):
```text
glob-revert -> c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen = giet_that
detail=C1a: đòi tổng 2 nêu x.RECEIPT.YAML, không ĐẠT; được rc=1 tổng=1: 'òi 2 · thiếu/rỗng `receipt_id` · thiếu/rỗng `reviewed_sha` · thiếu/rỗng `verdict_path` · thiếu/rỗng `verdict_sha256` · thiếu/rỗng `evidence_url` · thiếu/rỗng ánh xạ `model_reviewer_identity` · thiếu khoá `github_submitter_identity` (null hợp lệ, VẮNG thì không) · thiếu/rỗng ánh xạ `anchor`\nTỔNG: ĐỎ\n'
control=c18_neo_git_DUNG_thi_qua; clean=True; reason=
```

Log đầy đủ: [evidence/h06.log](evidence/h06.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### rig-fixture-init — Lượt dựng fixture đầu tiên không đo được

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/fixtures.py
```

OUTPUT THẬT (rc=1):
```text
git commit của fixture đã thừa kế cấu hình ký commit toàn cục, gọi code-sign; socket tới dịch vụ ký localhost bị sandbox từ chối (operation not permitted); fatal: failed to write commit object. Chưa tới cổng packet. Đã cô lập GIT_CONFIG_GLOBAL=/dev/null và GIT_CONFIG_SYSTEM=/dev/null cho Git trong fixture tạm để không gọi signer/hook từ cấu hình toàn cục; không đổi cấu hình cay-kho.
```

Log đầy đủ: [evidence/rig-fixture-init.log](evidence/rig-fixture-init.log).

Kết luận: **KHÔNG ĐO ĐƯỢC — lỗi giàn giáo, sẽ đo lại bằng fixture cô lập cấu hình Git**.

### h07 — Bare Ruff --select F: delta so cha master, so cả vị trí sau ánh xạ dòng

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/lint.py
```

OUTPUT THẬT (rc=0):
```text
ruff 0.16.9
python3 -m ruff --version: /usr/bin/python3: No module named ruff
Dùng executable Ruff có sẵn; không cài đặt và không tải mạng.
COMMAND: cwd=/tmp/rv1040-r11-ruff-base-aus4b1yk /root/.local/bin/ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py
base: rc=1; diagnostics=1
base codes={'F541': 1}
COMMAND: cwd=/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1040-r11/cay-kho /root/.local/bin/ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py
head: rc=1; diagnostics=1
head codes={'F541': 1}
added={}
removed={}
delta_count=0
diagnostics_equal_after_line_mapping=True
```

Log đầy đủ: [evidence/h07.log](evidence/h07.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h04 — CLI thật trên fixture Git độc lập: C1a/C1b, sinh nợ, thư mục và thông báo rỗng

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/fixtures.py
```

OUTPUT THẬT (rc=0):
```text
C1a: files=['y.receipt.yaml', 'x.RECEIPT.YAML'], directory=None, flags=()
rc=1
STDOUT:

bien_nhan_v2: 0 ĐẠT v2 · 0/11 miễn trừ legacy (băm khớp) · 0 NỢ đóng băng · 2 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 2
câu lịch sử: nợ L-REVIEW 0 · L-ANCESTRY 0 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
STDERR:
  ĐỎ  x.RECEIPT.YAML: KHÔNG đạt v2 và KHÔNG nằm trong danh sách nào — schema_version=None, đòi 2 · thiếu/rỗng `receipt_id` · thiếu/rỗng `reviewed_sha` · thiếu/rỗng `verdict_path` · thiếu/rỗng `verdict_sha256` · thiếu/rỗng `evidence_url` · thiếu/rỗng ánh xạ `model_reviewer_identity` · thiếu khoá `github_submitter_identity` (null hợp lệ, VẮNG thì không) · thiếu/rỗng ánh xạ `anchor`
  ĐỎ  y.receipt.yaml: KHÔNG đạt v2 và KHÔNG nằm trong danh sách nào — schema_version=None, đòi 2 · thiếu/rỗng `receipt_id` · thiếu/rỗng `reviewed_sha` · thiếu/rỗng `verdict_path` · thiếu/rỗng `verdict_sha256` · thiếu/rỗng `evidence_url` · thiếu/rỗng ánh xạ `model_reviewer_identity` · thiếu khoá `github_submitter_identity` (null hợp lệ, VẮNG thì không) · thiếu/rỗng ánh xạ `anchor`
TỔNG: ĐỎ


C1a-only-upper: files=['x.RECEIPT.YAML'], directory=None, flags=()
rc=1
STDOUT:

bien_nhan_v2: 0 ĐẠT v2 · 0/11 miễn trừ legacy (băm khớp) · 0 NỢ đóng băng · 1 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1
câu lịch sử: nợ L-REVIEW 0 · L-ANCESTRY 0 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
STDERR:
  ĐỎ  x.RECEIPT.YAML: KHÔNG đạt v2 và KHÔNG nằm trong danh sách nào — schema_version=None, đòi 2 · thiếu/rỗng `receipt_id` · thiếu/rỗng `reviewed_sha` · thiếu/rỗng `verdict_path` · thiếu/rỗng `verdict_sha256` · thiếu/rỗng `evidence_url` · thiếu/rỗng ánh xạ `model_reviewer_identity` · thiếu khoá `github_submitter_identity` (null hợp lệ, VẮNG thì không) · thiếu/rỗng ánh xạ `anchor`
TỔNG: ĐỎ


C1b: files=['y.receipt.yaml', 'x.RECEIPT.YAML'], directory=None, flags=()
rc=2
STDOUT:
STDERR:
KHÔNG ĐO ĐƯỢC: x.RECEIPT.YAML: YAML hỏng (ParserError: while parsing a flow node
expected the node content, but found '<stream end>'
  in "<unicode string>", line 2, column 1:
    
    ^)


sinh-no-upper: files=['x.RECEIPT.YAML'], directory=None, flags=('--sinh-no',)
rc=0
STDOUT:
NO_DA_DO: dict[str, str] = {
    "x.RECEIPT.YAML":
        "d4eed209fa44e2eb45f5dbe26726d1985cef0bc7b9a2c923a8d7e8003662234e",
}
STDERR:
# 1 tệp


directory-upper: files=['y.receipt.yaml'], directory='X.RECEIPT.YAML', flags=()
rc=2
STDOUT:
STDERR:
KHÔNG ĐO ĐƯỢC: X.RECEIPT.YAML: không đọc được (IsADirectoryError: [Errno 21] Is a directory: '/tmp/rv1040-r11-fixture-x626i6xb/ops/reviews/X.RECEIPT.YAML')


empty-receipts: files=['ignore.yaml'], directory=None, flags=()
rc=2
STDOUT:
STDERR:
KHÔNG ĐO ĐƯỢC: /tmp/rv1040-r11-fixture-iwv94dk2/ops/reviews không có tệp `*.receipt.yaml` nào (so đuôi không phân biệt hoa thường) — mốc neo đã đổi?
```

Log đầy đủ: [evidence/h04.log](evidence/h04.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h11 — C6: đếm ứng viên độc lập bằng os.listdir

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/data_audit.py
```

OUTPUT THẬT (trích phần tương ứng; rc=0; toàn output tái hiện tại h14):
```text
sys.platform=linux
Python=3.13.17
os.name=posix
independent_os_listdir_total=312
CLI_total=312
equal=True
```

Log đầy đủ: [evidence/h11.log](evidence/h11.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h12 — M1/M2/C9 và các nguồn luật/provider mà cổng đọc

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/source_audit.py
```

OUTPUT THẬT (rc=0):
```text
kiem: helper calls=1
_sinh_no: helper calls=1
helper definitions=1; iterdir/lower/endswith/sorted present; is_file absent
rg -n 'glob\\("\\*\\.receipt\\.yaml"\\)' ops/bien_nhan_v2.py: rc=1; stdout=''
C9 reverse probe (scratch copy): rc=0; stdout=1675:    Path(".").glob("*.receipt.yaml")
AGENTS.md: HEAD==P1=True; HEAD==P2=True
docs/PROTOCOL_DA_PHIEN.md: HEAD==P1=True; HEAD==P2=True
.claude/dev/launcher.py: HEAD==P1=True; HEAD==P2=True
local merge commit:
c8ff9ed563403fffa3c49c84bfce42e9a66bc68b
9c7dc1135d8fb392aecd69e94db2933fc25eab58 a16932aa09ce860a614f0bab4b2015699e7221bc
HEAD ancestor of c8ff9ed: rc=0
```

Log đầy đủ: [evidence/h12.log](evidence/h12.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h13 — Đối chiếu dữ liệu biên nhận nhập từ master và bản đặc tả trong cây

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/data_audit.py
```

OUTPUT THẬT (trích phần tương ứng; rc=0; toàn output tái hiện tại h14):
```text
HEAD^1 receipt-entry-count=306
HEAD receipt-entry-count=312
ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md sha256=d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d
ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG.md sha256=5882bdd613ff4654224e34419a4ed4e1d11cbd924c3a9082ba52b8012a18ea09
```

Log đầy đủ: [evidence/h13.log](evidence/h13.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h02 — Toàn suite tại reviewed_sha

LỆNH:
```sh
cd cay-kho
PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUFF_NO_CACHE=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file python3 ops/bien_nhan_v2_test.py
```

OUTPUT THẬT (rc=0):
```text
bien_nhan_v2_test — 98 ca

  ĐẠT   c1_kho_that_hien_tai_phai_SACH
  ĐẠT   c2_bien_nhan_moi_tu_khai_v1
  ĐẠT   c4_v2_du_truong_phai_XANH
  ĐẠT   c4b_submitter_NULL_van_HOP_LE
  ĐẠT   c4c_vang_khoa_submitter_thi_DO
  ĐẠT   c4d_assurance_vuot_bang_chung_doc_lap_thi_DO
  ĐẠT   c4e_assurance_CHI_co_dieu_kien_che_do
  ĐẠT   c4f_assurance_CHI_thieu_bang_chung
  ĐẠT   c4g_bang_chung_doc_lap_phai_dung_KIEU
  ĐẠT   c23_trang_thai_thu_ba_UU_TIEN_hon_vi_pham
  ĐẠT   c5_sua_tep_trong_allowlist_thi_MAT_mien_tru
  ĐẠT   c6_sua_tep_trong_no_thi_DO
  ĐẠT   c7_no_da_len_v2_ma_con_trong_danh_sach_no
  ĐẠT   c8_anchor_loai_ngoai_danh_sach_CHO_PHEP
  ĐẠT   c16_MA_TRAN_phu_DUNG_tap_yeu_cau_cua_cong
  ĐẠT   c17_MA_TRAN_moi_yeu_cau_co_MOT_ca_am
  ĐẠT   c9_thieu_thu_muc_trong_kho_git_la_KHONG_DO_DUOC
  ĐẠT   c10_thu_muc_RONG_la_KHONG_DO_DUOC
  ĐẠT   c11_yaml_hong_la_KHONG_DO_DUOC
     (tầng git: khớp `git ls-tree 2f84531` — 11 tệp)
  ĐẠT   c12_allowlist_khop_TUYET_DOI_ban_dong_bang
  ĐẠT   c13_no_chi_duoc_CO_LAI_va_KHONG_DUOC_DOI_BAM
  ĐẠT   c18_neo_git_DUNG_thi_qua
  ĐẠT   c19_neo_git_SAI_DUONG_DAN_thi_DO
  ĐẠT   c20_neo_git_BAM_LECH_thi_DO
  ĐẠT   c22_canonical_ancestry_ma_URL_khong_ghim_thi_DO
  ĐẠT   c21_object_khong_tra_duoc_la_KHONG_DO_DUOC_chu_khong_phai_DO
  ĐẠT   c24_anchor_KHONG_CO_DUONG_DO_vao_trang_thai_THU_BA
  ĐẠT   c25_commit_CO_THAT_ma_KHONG_phai_to_tien_thi_DO
  ĐẠT   c26_merge_base_rc_NGOAI_0_1_la_KHONG_DO_DUOC
  ĐẠT   c27_loai_CO_KHOANG_TRANG_khong_duoc_tron_khoi_phep_do
  ĐẠT   c28_nguon_provider_khong_doc_duoc_la_TRANG_THAI_THU_BA
  ĐẠT   c31_hop_dong_provider_doc_DU_BA_NGUON_khong_chep_tay
  ĐẠT   c29_CLI_CHI_co_vi_pham_phai_tra_rc_1
  ĐẠT   c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC
  ĐẠT   c34_MOI_truong_attestation_phai_la_CHUOI_khong_chi_truthy
  ĐẠT   c34b_P
[… rút gọn; log đầy đủ ở đường dẫn bên dưới …]
    m89_chi_xet_khai_bao_dau_tren_dong     → c83_MOI_khai_bao_surface_tren_cung_dong_deu_duoc_xet = giet_that  (chỉ khai báo đầu tiên trên dòng)
  CÓ RĂNG    m91_luot_bien_nhan_khac_thieu          → c70_A1_luot_KHONG_so_duoc_la_KHONG_DO_DUOC = giet_that  (r2: `luot` thiếu ở biên nhận khác)
  CÓ RĂNG    m92_merge_base_loi_thanh_vi_pham       → c84_merge_base_HONG_la_KHONG_DO_DUOC_khong_phai_vi_pham = giet_that  (r3: merge-base hỏng thành vi phạm)
  CÓ RĂNG    m94_B1_chen_lai_mien_tru_dung_tai      → c86_B1_moc_dung_tai_KHONG_con_mien = giet_that  (B1: chèn lại phép miễn khi mapping có `dung_tai`)
  CÓ RĂNG    m95_B2_bam_receipt_ngoai_bien          → c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback = giet_that  (B2: lỗi I/O khi băm/đọc receipt thoát biên)
  CÓ RĂNG    m96_B2_go_bien_loi_do                  → c90_B2_MOT_BIEN_loi_do_khong_traceback_khong_no_chet = giet_that  (B2: gỡ biên lỗi đo của ba luật)
  CÓ RĂNG    m97_B2_tep_hong_van_ket_luan_no_chet   → c90_B2_MOT_BIEN_loi_do_khong_traceback_khong_no_chet = giet_that  (B2: tệp đo hỏng mà nợ vẫn bị kết luận chết)
  CÓ RĂNG    m98_B3_bo_ngu_canh_backtick            → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (B3: bỏ ngữ cảnh backtick)
  CÓ RĂNG    m99_B3_bo_ngu_canh_40_hex              → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (B3: bỏ ngữ cảnh đủ 40 hex)
  CÓ RĂNG    m100_B3_bo_ngu_canh_sau_commit         → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (B3: bỏ ngữ cảnh sau từ `commit`)
  CÓ RĂNG    m101_B3_moi_token_thuan_la_bat_buoc    → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (B3: mọi token thuần thành bắt buộc (`deadbeef` rc=2))
  CÓ RĂNG    m102_B4_bo_dieu_kien_provider          → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (B4: khai báo không `provider` thành tự khai)
  CÓ RĂNG    m85_B4_bo_dieu_kien_trich_dan          → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (B4: dòng có trích dẫn kề thành tự khai)
  CÓ RĂNG    m103_git_khong_goi_duoc_thanh_rong     → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (git vắng/hỏng đọc thành stdout rỗng)
  CÓ RĂNG    m104_ref_mac_dinh_khong_phai_commit_lui_ref_ke → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (`origin/master` là tree mà lùi về `master` cục bộ)
  CÓ RĂNG    m105_tien_to_mo_ho_thanh_mot           → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (tiền tố trỏ hai commit đọc thành một)
  CÓ RĂNG    m106_run_json_thu_muc_thanh_vang       → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (run.json là thư mục bị coi như vắng (không áp))
  CÓ RĂNG    m107_bo_bat_UTF8_khi_doc_receipt       → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (byte UTF-8 hỏng trong receipt thoát biên)
  CÓ RĂNG    m108_sinh_no_ngoai_bien_CLI            → c92_B2_co_SINH_NO_cung_bien_voi_cong = giet_that  (`--sinh-no` gọi ngoài biên CLI)
  CÓ RĂNG    m109_sinh_no_khong_doi_loi_doc         → c92_B2_co_SINH_NO_cung_bien_voi_cong = giet_that  (`_sinh_no` không đổi lỗi đọc thành KHÔNG ĐO ĐƯỢC)
  CÓ RĂNG    m110_B3_bo_ranh_gioi_tu_commit         → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (B3: `Precommit` thành ngữ cảnh commit)
  CÓ RĂNG    m111_B3_backtick_chi_can_mo            → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (B3: backtick chỉ mở thành ngữ cảnh)
  CÓ RĂNG    m112_B4_bo_ranh_gioi_tu_provider       → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (B4: `notprovider` thành `provider`)
  CÓ RĂNG    m113_B4_cua_so_bo_dong_sau             → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (B4: cửa sổ bỏ dòng sau)
  CÓ RĂNG    m114_bo_qua_STDERR_cua_git             → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (tin kết quả git dù stderr báo ref/object hỏng)
  CÓ RĂNG    m115_vang_dung_stat_khong_lstat        → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (symlink gãy của run.json bị coi như vắng)
  CÓ RĂNG    m116_vang_loi_stat_khac_thanh_vang     → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (lỗi lstat khác ENOENT/ENOTDIR bị coi như vắng)
  CÓ RĂNG    m117_bo_chot_kho_NONG                  → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (kho nông vẫn đo tổ tiên)
  CÓ RĂNG    m118_bo_chot_kho_PARTIAL               → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (kho partial clone vẫn đo)
  CÓ RĂNG    m119_bo_chot_SYMREF_gay                → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (symref `origin/HEAD` gãy bị coi như vắng)
  CÓ RĂNG    m120_tinh_MOI_loai_object_la_ung_vien  → c93_ung_vien_CHI_TINH_COMMIT_blob_chung_tien_to_khong_mo_ho = giet_that  (blob chung tiền tố đẩy commit thành mơ hồ)
  CÓ RĂNG    m121_disambiguate_loc_bo_dong_la       → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (dòng lạ của `--disambiguate` bị lọc bỏ)
  CÓ RĂNG    m122_ung_vien_missing_thanh_khong_phai_commit → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (ứng viên được liệt kê mà `missing` bị coi là không phải commit)
  CÓ RĂNG    m123_batch_check_dang_la_thanh_khac    → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (dòng lạ của `cat-file --batch-check` được tin)
  CÓ RĂNG    m124_for_each_ref_dong_la_duoc_tin     → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (dòng lạ của `for-each-ref` được tin)
  CÓ RĂNG    m125_bo_chot_RC_cua_git                → c96_git_rc_LA_ma_stderr_RONG_van_la_KHONG_DO_DUOC = giet_that  (rc lạ mà stderr rỗng được tin)
  CÓ RĂNG    m126_ke_thua_bien_GIT                  → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (biến `GIT_*` kế thừa (GIT_DIR, GIT_TRACE) lọt vào phép đo)
  CÓ RĂNG    m127_khong_tat_replace                 → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (replace ref che quan hệ tổ tiên)
  CÓ RĂNG    m129_bo_chot_PROMISOR                  → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (partial clone thật (promisor) vẫn đo)
  CÓ RĂNG    m132_promisor_TAT_van_la_partial       → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (`remote.<x>.promisor=false` bị coi là partial clone)
  CÓ RĂNG    m133_bo_alternates_khoi_danh_sach_giu  → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (bỏ `GIT_ALTERNATE_OBJECT_DIRECTORIES` làm kho đủ mất object)
  CÓ RĂNG    m134_doc_promisor_khong_chuan_hoa_bool → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (`off`/`no` đọc thô thành dòng lạ ⇒ kho đủ bị chặn)
  CÓ RĂNG    m135_bo_chot_gia_tri_promisor_la       → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (giá trị promisor không phải bool được coi là tắt)
  CÓ RĂNG    m136_giu_GIT_DIR_ke_thua               → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (`GIT_DIR` kế thừa làm cổng đo kho khác)
  CÓ RĂNG    m137_bo_so_OID_batch_check             → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (batch-check trả OID khác mà được tin)
  CÓ RĂNG    m138_bo_kiem_loai_batch_check          → c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC = giet_that  (batch-check trả loại ngoài giao thức mà được tin)
  CÓ RĂNG    m139_bo_ngu_canh_tron_so_chu           → c87_B3_OID_khong_tra_duoc_theo_NGU_CANH = giet_that  (OID trộn số-chữ thiếu mà thành token thường)
  CÓ RĂNG    m140_B4_noi_cua_so_ve_truoc            → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (provider/citation cách hai dòng là ngoài cửa sổ)
  CÓ RĂNG    m141_B4_noi_cua_so_ve_sau              → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (provider/citation cách hai dòng là ngoài cửa sổ)
  CÓ RĂNG    m156_B4_bo_chan_bien_dau_tep           → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (dòng đầu bị mất cửa sổ)
  CÓ RĂNG    m157_B4_trich_dan_bo_dong_sau          → c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan = giet_that  (trích dẫn ở dòng sau bị bỏ qua)
  CÓ RĂNG    m130_bo_chot_GRAFTS                    → c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no = giet_that  (tệp grafts đổi parent mà vẫn đo)
  CÓ RĂNG    m131_ref_con_tien_to_la_dong_la        → c95_moi_truong_git_KHONG_doi_ket_qua_do = giet_that  (ref con `origin/HEAD/topic` làm hỏng phép chọn nhánh mặc định)
  CÓ RĂNG    m142_chon_bien_nhan_so_duoi_CHINH_XAC  → c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen = giet_that  (đuôi hoa lại bị bỏ qua lặng)
  CÓ RĂNG    m143_chon_bien_nhan_loc_is_file        → c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback = giet_that  (thư mục `*.receipt.yaml` trốn khỏi phép băm)
  CÓ RĂNG    m144_sinh_no_loc_duoi_CHINH_XAC        → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (`--sinh-no` bỏ qua đuôi hoa (đường gọi thứ hai))
  CÓ RĂNG    m145_bo_chon_khong_sap_xep             → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (thứ tự duyệt theo hệ tệp, không sắp xếp)
  CÓ RĂNG    m146_bo_chon_bo_nhanh_thu_muc_vang     → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (`--sinh-no` trên kho thiếu ops/reviews thành lỗi đo)
  CÓ RĂNG    m147_bo_chon_bo_bat_OSError            → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (lỗi liệt kê thoát thành traceback (Codex lượt 1))
  CÓ RĂNG    m148_bo_chon_hoi_is_dir_TRAN           → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (`--sinh-no`: EACCES ở `stat` thoát thành traceback)
  CÓ RĂNG    m149_kiem_guard_hoi_is_dir_TRAN        → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (`kiem`: EACCES ở `stat` thoát thành traceback)
  CÓ RĂNG    m150_hoi_trang_thai_bo_bat_OSError     → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (lỗi `stat` thoát thành traceback ở cả hai đường)
  CÓ RĂNG    m151_kiem_hoi_git_TRAN                 → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (`stat` của `.git` thoát thành traceback)
  CÓ RĂNG    m152_bo_chon_bat_Exception             → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (lỗi lập trình ở phép liệt kê bị đổi thành KHÔNG ĐO ĐƯỢC)
  CÓ RĂNG    m153_hoi_trang_thai_bat_Exception      → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (lỗi lập trình ở phép hỏi thư mục bị đổi thành KHÔNG ĐO ĐƯỢC)
  CÓ RĂNG    m154_hoi_trang_thai_chi_bat_PermissionError → c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang = giet_that  (EIO ở `stat` thoát thành traceback)
  CÓ RĂNG    m155_bo_chon_chi_bat_PermissionError   → c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE = giet_that  (EIO khi liệt kê thoát thành traceback)

bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐẠT

[exit_code=0; elapsed_seconds=414.813]
```

Log đầy đủ: [evidence/h02.log](evidence/h02.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h14 — Tái hiện đầy đủ số đếm độc lập và hash đặc tả

LỆNH:
```sh
cd cay-kho
PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUFF_NO_CACHE=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file python3 ../evidence/data_audit.py
```

OUTPUT THẬT (rc=0):
```text
sys.platform=linux
Python=3.13.17
os.name=posix
independent_os_listdir_total=312
CLI_total=312
equal=True
HEAD^1 receipt-entry-count=306
HEAD receipt-entry-count=312
ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md sha256=d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d
ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG.md sha256=5882bdd613ff4654224e34419a4ed4e1d11cbd924c3a9082ba52b8012a18ea09

[exit_code=0; elapsed_seconds=0.067]
```

Log đầy đủ: [evidence/h14.log](evidence/h14.log).

Kết luận: **KHÔNG PHẢI LỖI**.

### h15 — Kiểm toàn vẹn đầu/cuối và phân số dương của suite

LỆNH:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/integrity.py
```

OUTPUT THẬT (rc=0):
```text
HEAD=a16932aa09ce860a614f0bab4b2015699e7221bc
tree=d4eea17c04edc0a62c320d4f44cae8290082cf2f
snapshot_files_before=8972; after=8972
all_file_contents_and_modes_equal=True
index_entries_equal=True
tracked_untracked_ignored_status=''
full_snapshot_equal=True
bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
positive_case_lines=98; header_denominator=98; equal=True
135/153 là số mutant KHAI đối chứng, không phải tỉ lệ đạt.
Codex home is inside a repository: absent
Không có ca bỏ khỏi mẫu số; không có dòng ca thường ĐỎ/KHÔNG ĐO ĐƯỢC.
suite ĐẠT c14_cli_ba_trang_thai
suite ĐẠT c40_R7_01_nguon_hong_tren_bien_nhan_THAT_khong_ket_toi_bien_nhan_nao
suite ĐẠT c76_A6_kho_that_voi_no_RONG_phai_DO_dung_bang_so_no
suite ĐẠT c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan
suite ĐẠT c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback
suite ĐẠT c98_TIN_DUNG_GIA_phai_in_DU_ngoai_le_va_vi_tri_nem
suite ĐẠT c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE
suite ĐẠT c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang
suite ĐẠT c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen
ops/bien_nhan_v2.py sha256=7f9a86f3fc07429877f2959ad2ecbe238ef145d08860b8f78197340a06e276a6
ops/bien_nhan_v2_test.py sha256=cac81d460abd280c461cf0acf938e412fc4b1c4cb477f36b55d2c5b1b0474b87
```

Log đầy đủ: [evidence/h15.log](evidence/h15.log).

Kết luận: **KHÔNG PHẢI LỖI**.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Các verdict cũ chỉ dùng để lập danh sách kiểm lại. Kết quả dưới đo mới tại `a16932aa09ce860a614f0bab4b2015699e7221bc`, không lấy approve tại `356a27e` phủ SHA merge.

| Mục được nhắc ở verdict nền | Đối chiếu tại SHA hiện tại | Kết luận |
|---|---|---|
| Thiếu object lịch sử / c14, c40, c76 | Cổng thật 0 KHÔNG ĐO ĐƯỢC; c14/c40/c76 ĐẠT trong suite 98/98. | Không tái hiện trở ngại snapshot; không phải vá mã. |
| `chu-thich-tro-sai-ca-ngoai-le-lap-trinh` | Docstring sản phẩm dòng 90 trỏ c100 chốt 7; c100 qua, m153→c100 giet_that và đối chứng sạch. | ĐÃ VÁ THẬT, vẫn đóng. |
| `loi-do-liet-ke-thu-muc-thoat-traceback` | c99/c100 qua; m147→c99, m148–m151/m154→c100, m155→c99 đều giet_that. | ĐÃ VÁ THẬT, không thấy hồi quy. |
| `loi-do-thieu-chot-ngoai-le-lap-trinh` | c100 qua; m152/m153→c100 giet_that, đối chứng sạch. | ĐÃ VÁ THẬT, vẫn đóng. |
| `bien-ngoai-cua-so-surface-chua-co-rang` | c88 ĐẠT trong suite; m156 và m157 đều giet_that đúng c88 khi chạy riêng và trong toàn suite. | ĐÃ VÁ THẬT, vẫn đóng. |
| Giải xung đột c98/c101 với #1037 | c98 và c101 đều ĐẠT trong suite; m142 vẫn nhắm c101; c98 không bị trừ khỏi mẫu số. | Không thấy hồi quy. |
| Chú thích về mutant từng sống ở các lượt cũ | Không chạy lại hiện vật lịch sử; chỉ xác nhận hành vi hiện tại qua các mutant và suite mới. | KHÔNG ĐO ĐƯỢC phần lịch sử; không lấy lời mô tả đó làm bằng chứng nghiệm thu hiện tại. |

## FINDING

Không phát hiện finding P0/P1/P2/P3 còn mở trong phạm vi kiểm toán này.

## GIỚI HẠN PHÉP ĐO

- C4/C5/C7 chưa đo; không kế thừa log trên SHA cũ thành kết quả cho SHA hiện tại. Không xác nhận các required CI check, runner labels/id hoặc Windows local.
- Ruff là bare lint bằng executable 0.16.9 có sẵn. Không chứng nhận hợp đồng pin/probe CI (workflow ghi pin 0.15.15); một F541 ở cả hai phiên bản nguồn là nợ nền, delta bằng 0, không khai lint sạch tuyệt đối.
- Không fetch/push, không truy cập GitHub hoặc máy Windows. Lượt dựng fixture đầu đã thừa kế cấu hình ký commit toàn cục: signer thử socket localhost và bị sandbox từ chối trước khi cổng packet chạy (rig-fixture-init). Sau đó đã cô lập cấu hình Git của fixture tạm và đo lại thành công; không thay cấu hình kho được review. Đây là lỗi giàn giáo đã khắc phục, không được đếm thành phép thử packet đạt.
- Snapshot đầu/cuối chỉ bao phủ checkout được đo, không chứng minh mọi sự kiện trung gian. Toàn bộ đột biến chỉ định và hoàn nguyên glob dùng `_dot_bien_tep` tạo tệp bên ngoài `cay-kho/`.
