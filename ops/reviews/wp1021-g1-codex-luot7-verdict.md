Verdict: request_changes
Reviewed commit: c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

P3 lượt 6 **ĐÃ VÁ THẬT**. Còn **1 P3 mới phát hiện trong diff tổng thể**: docstring `_hoi_trang_thai` trỏ sai ca kiểm tra lỗi lập trình (`c99` thay vì `c100`). Do ngưỡng yêu cầu không còn bất kỳ P0/P1/P2/P3 nào, verdict là **request_changes**. Không phát hiện lỗi runtime mới trong các phép đo dưới đây.

Suite: **98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt, TỔNG: ĐẠT**. Sáu đột biến chỉ định đều chết đúng ca đích. C6/C9 đạt theo tiêu chí delta. Windows CI/local và Ubuntu CI trên exact head: **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

## Neo và cách tái hiện

Từ gốc sandbox: `PYTHONDONTWRITEBYTECODE=1 python3 measure_l7.py preflight`, `python3 measure_l7.py history`, `python3 measure_l7.py pipeline`. Driver ghi command, cwd, rc, thời gian và băm stdout/stderr trong `evidence/<tên>.json`; stdout/stderr được lưu riêng. Mọi tiến trình đo con dùng `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Các lệnh suite, cổng, Ruff, doctrine và rg chạy tại `cay-kho/`. Các probe dùng cơ chế `_dot_bien_tep` của suite; không sao chép toàn cây kho.

`python3 measure_l7.py preflight` rc=0 ([kết quả](evidence/preflight.json)): HEAD `c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8`, cha `691cb65388e71afb825aeba3b5cbc5359fc4dac5`, base `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`, tree `5ea6194cbf993b93521a01f269f2b446f4b1cf2a`. `.git` là thư mục, `git rev-parse --is-shallow-repository` → `false`; trạng thái tracked/untracked/ignored sạch, nguồn khớp blob HEAD. SPEC khớp băm dòng 3; HINT sha256 `fc52cb294ec8eba18038ffa00f95626e4de45b74d79360c79f7282ece7c3e202`. Hai tệp DIFF đầu vào khớp byte với git diff tương ứng.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding/phạm vi trước | Phép đo, output | Kết luận |
|---|---|---|
| P3 `chu-thich-nang-ca-thuong-thanh-toan-suite`, lượt 6 / 691cb65 | `measure_l7.py preflight`: thay đúng một dòng theo HINT trong blob cha cho kết quả khớp byte HEAD. `measure_l7.py history`: kiểm log gốc lượt 5–6 bằng assertion, rc=0. | **ĐÃ VÁ THẬT** |
| P1 `bien-ngoai-cua-so-surface-chua-co-rang` / c88 | AST hai tệp giống hệt 691cb65. Suite sạch; `_dot_bien(chi={m156})` và `chi={m157}` đều `giet_that` tại c88, đối chứng c18 sạch. | Giữ kết luận **ĐÃ VÁ THẬT** của lượt 6; không mở lại P1. |
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | AST không đổi; m147 chết tại c99; m154 chết tại c100; suite sạch. | Vẫn đóng trong phạm vi đã đo. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | AST không đổi; c100 và m152/m153 đạt trong suite. Probe bổ sung m153 bị c100 giết thật vì RuntimeError bị nuốt, c18 sạch. | Vẫn đóng về hành vi; finding mới bên dưới chỉ là tham chiếu docstring sai. |
| F3/P3, bắt OSError ngoài PermissionError | AST không đổi; m154/m155 chết đúng c100/c99 với errno=5. | Vẫn đóng. |
| Giải xung đột #1037 | `git diff 691cb65..HEAD` chỉ đổi một dòng chú thích; AST hai tệp giống hệt; c98 và toàn suite qua, m142 vẫn nhắm c101. | Giữ kết luận hành vi của lượt 6. Không chạy lại riêng toàn bộ thí nghiệm tiêm lỗi báo cáo của lượt 6. |

Lệnh đối chiếu AST: driver gọi `ast.dump(ast.parse(git show <rev>:<file>), include_attributes=False)` cho cả hai tệp ở HEAD và 691cb65, so chuỗi bằng nhau, lưu băm AST trong [preflight.json](evidence/preflight.json). `git diff --numstat 691cb65..HEAD` tương ứng 1 thêm/1 xóa chỉ trong chú thích trên m156. Chú thích hiện tại tại `ops/bien_nhan_v2_test.py:4760` là: “no_clamp từng SỐNG qua toàn suite; citation_drop_next từng qua đủ 98 ca thường.”

`python3 measure_l7.py history` rc=0 ([audit và provenance](evidence/history-audit.json)): log lượt 5 của no_clamp có rc=0, **98/98 · 151/151 · 2/2, TỔNG: ĐẠT**; hiện vật citation_drop_next ghi **98/98 ca thường**, không lỗi. Phép đo bổ sung lượt 6 trên 3883b60 có rc=1, **98/98 · 150/151 · 2/2, TỔNG: ĐỎ**, m85=`gian_giao` vì mẫu không khớp. Câu mới tách đúng hai phạm vi. Đây là đối chiếu lại hiện vật lịch sử, không gán chúng thành lần chạy mới trên HEAD.

Kết quả 71/71 M4, 40 mutant biên, no_clamp toàn suite đỏ, và phép đo F1/F2/F3 sâu của [lượt 6](VERDICT-LUOT6.md) được **kế thừa theo chỉ thị**, dựa trên AST bất biến; không khai đã chạy lại chúng ở lượt 7. Tập lớp mở lượt 6 có 1, đóng được 1; thêm 1 lớp P3 được phát hiện lượt này.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Neo và write set | ĐẠT | `git diff --name-only b29da0b..HEAD` → đúng `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`; `preflight` rc=0. |
| C1a/C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | c101 qua trong suite và đối chứng sạch của `probe_l7.py glob`; m142 chết đúng c101 với tổng 1 thay vì 2. Ba nhánh ca giữ nguyên AST so lượt 6. |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | `suite.stdout`: c89 ĐẠT, m143 lọc is_file bị c89 `giet_that` / CÓ RĂNG. |
| C3 | ĐẠT | `python3 probe_l7.py glob` rc=0: c101 sạch=`qua`, mutant glob=`giet_that`, tổng=1; c18 sạch; nguồn ổn định, temp dọn sạch ([log](evidence/glob-probe.stdout)). |
| C4 Windows CI | KHÔNG ĐO ĐƯỢC | Không có phép đo độc lập jobs/labels/runner/log trên exact head; không suy pass từ lời khai đang chạy. |
| C5 Ubuntu CI | KHÔNG ĐO ĐƯỢC | Lần chạy suite tại đây không chứng minh job CI exact head. |
| C6 | ĐẠT | `python3 ops/bien_nhan_v2.py --root .` rc=0, tổng 306, TỔNG: ĐẠT; đếm riêng os.listdir/name.lower().endswith = 306. |
| C7 Windows local | KHÔNG ĐO ĐƯỢC | Theo chỉ thị lượt 7; không sử dụng lời khai executor làm bằng chứng. |
| C8 nội dung review | KHÔNG ĐẠT | Còn 1 P3 mới; exact reviewed SHA đúng. Trần lượt 7 theo chỉ thị hiện hành. Không xác nhận điều kiện land/CI còn thiếu. |
| C9 | ĐẠT | Đúng hai tệp; hai diff-check rc=0; Ruff F head/base delta=0; doctrine rc=0; rg glob rc=1/0 dòng. |
| Toàn suite | ĐẠT | rc=0, 396.308 giây, 98/98 · 153/153 · 2/2, TỔNG: ĐẠT; stderr rỗng. |
| Sáu đột biến chạy riêng | ĐẠT | `python3 probe_l7.py focused` rc=0; 6/6 `giet_that` đúng ca đích, 6/6 đối chứng sạch; chi tiết dưới đây. |

Log suite: [stdout](evidence/suite.stdout), [command/rc](evidence/suite.json). Output cuối nguyên văn:

```text
bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

C6: [stdout](evidence/gate.stdout), [command/rc](evidence/gate.json), [đếm độc lập](evidence/receipt-count.json):

```text
bien_nhan_v2: 253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
```

Lệnh đếm độc lập tương đương: `python3 -c 'import os; print(sum(n.lower().endswith(".receipt.yaml") for n in os.listdir("ops/reviews")))'` → **306**. Không lọc is_file.

C9: `git diff --numstat b29da0b..HEAD` → **40/5** ở sản phẩm, **296/2** ở test. `git diff --check` và `git diff --check b29da0b..HEAD` → rc=0, stdout/stderr rỗng. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` → rc=1, 0 dòng.

Ruff `ruff 0.15.15`: `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` → rc=1, **1 lỗi**; base cũng **1 lỗi**. Base lấy từng blob bằng `git show b29da0b:<path>` và lint stdin bằng cùng config, cùng `--select F --stdin-filename <path>`. Chuẩn hóa theo path/code/message/nội dung dòng: thêm 0, mất 0 ([delta](evidence/ruff-delta.json)). Đây là **delta đạt**, không phải Ruff sạch tuyệt đối.

Doctrine: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc=0 ([log](evidence/doctrine.stdout)):

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
```

## Sáu đột biến yêu cầu

`python3 probe_l7.py focused` gọi riêng `_dot_bien(chi={tên_đầy_đủ})` cho từng tên, kiểm đúng một hàng kết quả, `dat=true`, `tt=giet_that`, có đối chứng và không phải ca tự kiểm. Mọi đối chứng chạy khi mutant còn hiệu lực theo cơ chế suite. Băm nguồn trước/sau không đổi, module/CONG phục hồi và danh sách temp rỗng. [Output](evidence/focused.stdout), [bảng máy](evidence/focused-results.json).

| Đột biến | Ca đích | Kết quả | Assertion đầu tiên |
|---|---|---|---|
| `m142_chon_bien_nhan_so_duoi_CHINH_XAC` | `c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen` | `giet_that`; CÓ RĂNG; c18 sạch | `C1a: đòi tổng 2 nêu x.RECEIPT.YAML, không ĐẠT; được rc=1 tổng=1: 'òi 2 · thiếu/r` |
| `m147_bo_chon_bo_bat_OSError` | `c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE` | `giet_that`; CÓ RĂNG; c18 sạch | `[]: CLI chết bằng PermissionError: [Errno 13] Permission denied (tiêm, #1021): '` |
| `m154_hoi_trang_thai_chi_bat_PermissionError` | `c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang` | `giet_that`; CÓ RĂNG; c18 sạch | `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, khô` |
| `m155_bo_chon_chi_bat_PermissionError` | `c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE` | `giet_that`; CÓ RĂNG; c18 sạch | `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021): '/tmp/tmpxd6vy39i/` |
| `m156_B4_bo_chan_bien_dau_tep` | `c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan` | `giet_that`; CÓ RĂNG; c18 sạch | `ix-trich-dan-sau-hai-dong: đòi rc=1, được 0: loi=[] chua=[]` |
| `m157_B4_trich_dan_bo_dong_sau` | `c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan` | `giet_that`; CÓ RĂNG; c18 sạch | `ii-b-trich-dan-dong-sau: đòi rc=0, được 1: loi=["[L-SURFACE] r.receipt.yaml: ver` |

## Bảng finding

**Finding mở: 1. P0=0, P1=0, P2=0, P3=1.**

| Slug lớp | Mức | Vị trí | Trạng thái |
|---|---|---|---|
| `chu-thich-nang-ca-thuong-thanh-toan-suite` | P3 lịch sử | test:4760 | ĐÃ VÁ THẬT |
| `chu-thich-tro-sai-ca-ngoai-le-lap-trinh` | P3 | sản phẩm:90 | MỚI PHÁT HIỆN, còn mở |

- [P3] chu-thich-tro-sai-ca-ngoai-le-lap-trinh: `ops/bien_nhan_v2.py:90` — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe_l7.py comment-probe` — wrapper rc=0; c99/c100 trên nguồn sạch đều `qua`; cùng mutant m153 nới `_hoi_trang_thai` từ bắt OSError sang Exception: **c99 vẫn qua**, **c100 giet_that**, chi tiết “lỗi lập trình ở is_dir [] bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, được không ngoại lệ”; c18 sạch — đổi đúng tham chiếu `c99` thành `c100` trong docstring.

  HÌNH DẠNG: `khac`.

  Docstring hiện gán thuộc tính “lỗi lập trình phải đi thẳng ra” cho “c99 chốt 7”, nhưng c99 không canh thuộc tính này. Người bảo trì chạy ca được chỉ dẫn có thể nhận xanh dù đã nuốt lỗi lập trình; probe trên đã tái hiện đúng tình huống đó. Chốt 7 nằm trong `c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang` tại test:3830 và mutant m153 đăng ký ca này tại test:4820. Đây là lỗi tham chiếu bằng chứng trong diff #1021 tổng thể, đã tồn tại trước commit lượt 7; không phải hồi quy do sửa chú thích m156 và không phủ nhận F2 đã được vá về hành vi. [Kết quả chi tiết](evidence/comment-probe-results.json), [lệnh/rc](evidence/comment-probe.json), [đối chiếu lịch sử](evidence/comment-rename-history.json).

  Gợi ý vá chỉ thay chữ `c99` bằng `c100` ở vị trí nêu trên. Không sửa kho trong lượt review này. Bản probe dùng bản sao tạm đúng tệp nguồn qua `_dot_bien_tep`; đã kiểm băm nguồn không đổi và dọn bản tạm.

## Kiểm tra cuối và giới hạn

`PYTHONDONTWRITEBYTECODE=1 python3 finalize_l7.py` kiểm các rc, mẫu số, đích mutant, delta Ruff, head/spec và snapshot bằng assertion; output **FINAL ASSERTIONS PASS** ([kết quả](evidence/final-validation.json)). Snapshot đầu/cuối giống nhau về HEAD/tree, index, nội dung hai tệp nguồn, diff staged/unstaged và trạng thái tracked/untracked/ignored. Điều này chứng minh không có delta quan sát được ở hai mốc, không dùng để suy toàn bộ lịch sử ghi. Các bản tạm do probe tạo đều được dọn; chỉ giữ script và log bằng chứng trong sandbox. Bản cập nhật tăng dần trước tổng hợp được giữ tại [VERDICT-progress.md](evidence/VERDICT-progress.md).

Windows CI/local, Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không cấp quyền merge/land.
