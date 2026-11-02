Verdict: approve
Reviewed commit: e9e0048b48ab610fee1246368b4f134c1ac4ae76
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận cuối: **approve** trên đúng commit dòng 2; **0 finding P0/P1/P2/P3 mở**. F3 lượt 3 **ĐÃ VÁ THẬT**, F1/F2 lượt 2 vẫn đóng. Head đạt `97/97 ca · 151/151 đột biến thường · 2/2 tự kiểm`, `TỔNG: ĐẠT`; mutant thu hẹp helper nay đỏ đúng c100 trong toàn suite, mutant thu hẹp liệt kê đỏ đúng c99 ở phép ca đích. Cổng thật rc=0/`tổng 306`, khớp phép đếm độc lập. Các lệnh, output và giới hạn được ghi dưới đây; Windows và CI exact head **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

Rà soát packet #1021 r2, lượt 4. Kết quả được ghi tăng dần. Các phép đột biến chỉ thực hiện trên bản sao đủ cây trong sandbox; mã nguồn `cay-kho/` được giữ nguyên. Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`; cấu hình `core.abbrev=7` theo chỉ thị.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn đối chiếu: `VERDICT-LUOT3.md` trên `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde` và `VERDICT-LUOT2.md` trên `5efa311fd857f7657a1c687e9ea37693070a37d3`. Không coi lời khai executor hoặc verdict cũ là phép đo trên head hiện tại.

| Finding / lớp cũ | Phân loại trên head mới | Bằng chứng độc lập |
|---|---|---|
| F3/P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror` (lượt 3; hai biểu hiện helper/liệt kê) | **ĐÃ VÁ THẬT** | `extra_mutate.py narrow_helper --suite`: rc=1, 96/97, c100 `giet_that` đúng EIO; `extra_mutate.py narrow_listing`: c99 `giet_that` đúng EIO; c18 đều sạch. `errno_probe.py` đủ EIO/ESTALE, 12/12 ở head rc=2/hit=1/không traceback. Tracer đo đủ cả hai lớp và thử đột biến factory ở Đợt 3 chứng minh m154/m155 có răng riêng. |
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` (lượt 2) | **ĐÃ VÁ THẬT**, không bị mở lại | `review_new.py error-child head <kiem\|sinh> <stat-os\|access>`: 4/4 rc=2/có hit/không traceback; lỗi liệt kê muộn cũng rc=2. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` (lượt 2) | **ĐÃ VÁ THẬT**, không bị mở lại | `boundary_oracle.py head` rc=0/2 trên 2 truyền đúng đối tượng; `new_mutate.py broad` và `broad_literal` chết đúng c100, c18 sạch; tracer có đủ bốn RuntimeError mốc. |

Ba lớp lịch sử trên mang HÌNH DẠNG: `loi-do`; 0 lớp/0 biểu hiện còn mở sau phép đối chiếu. Không có finding mới `bo-chon-ung-vien`.

## Nhật ký đo

### Đợt 1 — neo, phạm vi và phép tái hiện

`evidence/preflight.json`: `git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master` rc=0 ⇒ head đúng dòng 2, tree `e1e840c06edf6d93d7ce0a527ca0d8c2d15dcd41`, base `757bde561d09738858506aecf5de2f050a5f0d5e`; `--is-shallow-repository` ⇒ `false`, `.git` là thư mục, HEAD detached, status tracked/untracked/ignored rỗng. SHA-256 SPEC khớp dòng 3. Hai patch được so byte với `git diff`: đều khớp.

`git diff 8d9e3e3..HEAD -- ops/bien_nhan_v2.py` rc=0/rỗng: mã sản phẩm không đổi từ lượt 3. `git diff --numstat 757bde5..HEAD` ⇒ `40 5 ops/bien_nhan_v2.py`, `283 0 ops/bien_nhan_v2_test.py`; đúng hai tệp write set. `git diff --check 757bde5..HEAD` rc=0/rỗng.

Các script `luot3-probe/*.py` được chép nguyên byte ra gốc sandbox để `ROOT=parent(__file__)` trỏ đúng nơi; chưa thay mốc neo/oracle trong `extra_mutate.py`, `errno_probe.py`, `probe.py`, `mutate.py`, `new_mutate.py`, `review_new.py`, `boundary_oracle.py`, `measure.py`. `work/head` và `work/base` là bản sao đủ cây, gồm `.git` thường; base checkout đúng SHA nêu trên. Các log lệnh chạy qua `measure.run` có ba tệp `.json` (lệnh/rc/thời gian), `.stdout`, `.stderr` trong `evidence/`.

`python3 extra_mutate.py narrow_helper --suite`: ca đích **c100 `giet_that`** với thông báo `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, không traceback`; c98/c99/c89 qua, c18 `[true, ""]`. Phần toàn suite đang chạy; chưa suy từ phép ca đích sang toàn suite.

`python3 extra_mutate.py narrow_listing`: ca đích **c99 `giet_that`** với thông báo `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021): '…/ops/reviews' — đòi mã thoát, không traceback`; c98/c100/c89 qua, c18 `[true, ""]`. Script báo rc=0 vì ghi quan sát; trạng thái `giet_that` và thông báo trong `mut-narrow_listing-cases.stdout` mới là bằng chứng chết mutant.

`python3 measure.py head gate` (lệnh tương đương ghi trong `head-gate.json`) rc=0: `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Lệnh riêng `python3 -c 'import os; n=os.listdir("ops/reviews");print("casefold_suffix",sum(x.lower().endswith(".receipt.yaml") for x in n));print("exact_suffix",sum(x.endswith(".receipt.yaml") for x in n))'` ⇒ `306`, `306`. Base cũng đạt và đếm 306.

### Đợt 2 — EIO/ESTALE, F1/F2 và khôi phục phương thức

`python3 errno_probe.py <head|mut-narrow_helper|mut-narrow_listing> <mode> <site> <EIO|ESTALE>` chạy đủ sáu tổ hợp: `kiem/guard`, `kiem/helper`, `sinh/helper`, `kiem/git`, `kiem/listing`, `sinh/listing`. Mỗi tổ hợp/mã lỗi là tiến trình riêng. `evidence/errno-summary.json` tổng hợp 36 log: **head 12/12 rc=2, hit=1, không traceback**; `mut-narrow_helper` **8/12 rc=1/traceback** ở bốn tổ hợp trạng thái, 4/12 liệt kê vẫn rc=2; `mut-narrow_listing` **4/12 rc=1/traceback** ở hai đường liệt kê, 8/12 trạng thái vẫn rc=2. Tất cả 36 phép có hit=1. `kiem/helper` có attempts=2, nên đo riêng lần hỏi trạng thái thứ hai, không nhầm với guard. Head lỗi nêu đúng `ops/reviews`/`.git`; mutant kết thúc `OSError: [Errno 5|116] review EIO|ESTALE failure`.

F1 lượt 2: `python3 review_new.py error-child head <kiem|sinh> <stat-os|access>` ⇒ **4/4 rc=2**, `REVIEW_FAULT_HIT: stat-os`, `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái …/ops/reviews (PermissionError…)`, không traceback. Nhánh iterator đã yield rồi lỗi (`late`) cũng rc=2 trên cả hai đường.

F2 lượt 2: `python3 review_new.py error-child head <kiem|sinh> <runtime|value>` ⇒ **4/4 rc=1**, traceback đúng `RuntimeError|ValueError: review programming fault`; không bị đổi thành KhongDoDuoc. `python3 boundary_oracle.py head` rc=0, hai đường `propagated_same_error=true, hit=1, restored=true`. `python3 new_mutate.py broad` và `broad_literal` ⇒ c100 **giet_that**: `lỗi lập trình ở iterdir [] bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, được không ngoại lệ`; c98/c99/c89 qua, c18 sạch.

Phép mới `python3 audit_l4.py head <c99|c100> trace` dùng `sys.settrace` quan sát ngoại lệ THỰC SỰ ném từ `hong`/`gia` trong test nguyên trạng, không đếm lần tạo đối tượng chỉ phục vụ thông báo:

| Chốt / phương thức | Đường | PermissionError(EACCES) thực ném | OSError(EIO) thực ném |
|---|---|---:|---:|
| c99 / iterdir | kiem | 1 | 1 |
| c99 / iterdir | sinh | 1 | 1 |
| c100 / is_dir | kiem | 1 | 1 |
| c100 / is_dir | sinh | 1 | 1 |
| c100 / exists(.git) | kiem | 1 | 1 |

Cả hai lệnh rc=0, ca `qua`, mọi `restored=true`. **5/5 lần EIO có `type(ex) is OSError`, `isinstance(ex, PermissionError)=false`, errno=5**; 5 lần EACCES là PermissionError/errno=13. Vì vậy chốt không qua do Python đổi EIO thành PermissionError. Tracer c100 còn đo bốn RuntimeError của chốt (7), đủ iterdir/is_dir × kiem/sinh, tất cả đúng đối tượng mốc.

`python3 audit_l4.py head <c99|c100> cleanup <stage> <rig|runtime|value>`: c99 stage 1..4, c100 stage 1..10, tổng **42/42 tiến trình rc=0**. Tiêm ngắt tại mỗi lần gọi main khi Path đang bị thay; sau ngắt `Path.is_dir`, `Path.exists`, `Path.iterdir` đều đúng đối tượng gốc; chạy lại chính ca `qua`, c18 sạch, kiểm cuối vẫn khôi phục. Có lỗi giàn giáo/ngoại lệ khi cố tình ngắt, không dùng chúng làm tín dụng giết mutant. Không phát hiện rò monkeypatch trong phạm vi các nhánh đã đo.

### Đợt 3 — đột biến mới của phần EIO

`python3 mutate_l4.py <tên>` tạo một bản sao đầy đủ `work/mut4-<tên>` và patch trong `evidence/`; mỗi đột biến chạy tiến trình riêng. `probe.py` chạy c98/c99/c100/c89 và đối chứng c18. Với đột biến tệp test, `focused_l4.py` lấy bằng AST đúng thân đăng ký m154/m155 cùng hàm `do`/các biến của `_dot_bien` hiện tại; giữ nguyên cơ chế giết thật/đối chứng/khôi phục, chỉ chọn hai đăng ký cần đo. Đây là phép đo chọn lọc, KHÔNG được gọi là toàn suite.

| Đột biến reviewer | Kết quả đo | Diễn giải |
|---|---|---|
| `eio_helper_empty`: EIO trong `_hoi_trang_thai` trả False | c100 **giet_that**, c18 sạch | Vẫn rc=2 nhưng thông báo thành “kho thật mà không có”; chốt bắt được SAI NGHĨA, không chỉ so rc. |
| `eio_git_escape`: chỉ EIO ở `.git` được ném lại | c100 **giet_that**, `CLI chết bằng OSError: [Errno 5]…`; c18 sạch | Phân biệt nhánh `.git` với is_dir, không chết ở phép PermissionError trước đó. |
| `eio_listing_empty`: EIO khi liệt kê trả danh sách rỗng | c99 **giet_that**, c18 sạch | Vẫn rc=2 nhưng thông báo thành “không có tệp”; chốt đòi “không liệt kê được”. |
| `c99_duplicate_permission`: đổi errno của factory mới EIO → EACCES | **SỐNG ở bốn ca thường**, nhưng phép m155 **KHÔNG RĂNG / qua**, focused rc=1; m154 còn CÓ RĂNG | Tracer ghi 4 PermissionError, 0 OSError thuần. Bảng đột biến phát hiện sự mất lớp EIO của c99. |
| `c100_duplicate_permission`: đổi errno của OS_LOI mới EIO → EACCES | **SỐNG ở bốn ca thường**, nhưng phép m154 **KHÔNG RĂNG / qua**, focused rc=1; m155 còn CÓ RĂNG | Tracer ghi 6 PermissionError, 0 OSError thuần, bốn RuntimeError; bảng đột biến phát hiện sự mất lớp EIO của c100. |
| `reverse_osloi`: đảo thứ tự hai factory tại cả hai vòng OS_LOI | **SỐNG** ở các ca thường và focused rc=0/2 trên 2 CÓ RĂNG | Đối chứng tương đương: vẫn đủ 3 EIO + 3 EACCES + 4 RuntimeError, Path khôi phục. Không phải lỗi cần giết; thứ tự factory không thuộc hợp đồng. |

Cả sáu mutant có c18 sạch. Hai mutant làm mất EIO chỉ sống ở tầng ca thường; không được mô tả là sống qua toàn suite. Không có mutant sai hành vi sản phẩm nào trong tập mới này sống ở ca đích. Log chi tiết `mut4-*-cases.stdout`, `mut4-*-focused.{stdout,json}`, `mut4-*-trace.stdout`; m154/m155 trên head đối chứng focused rc=0/cả hai `giet_that`.

### Đợt 4 — C1/C2/C3/C9

`python3 probe.py head behaviors` (`head-behaviors` và từng `fixture-head-*`) ⇒ C1a rc=1/`tổng 2`/nêu `x.RECEIPT.YAML`/không `TỔNG: ĐẠT`; chỉ-x rc=1/`tổng 1`/không “không có tệp”; C1b rc=2/stderr nêu x/không traceback/không dòng tổng. Thư mục `X.RECEIPT.YAML` tới bước băm rồi rc=2. Base được đo lại: C1a tổng 1/bỏ x, chỉ-x rc=2/không có tệp, C1b rc=1/bỏ x.

`python3 mutate.py exact --behaviors` ⇒ c98/c99 **giet_that**, c18 sạch; fixture C1a/C1b/chỉ-x bỏ x. `python3 mutate.py isfile --behaviors` ⇒ c89 **giet_that**, `đòi rc=2 nêu tệp hỏng, được rc=1`, c18 sạch. `python3 mutate.py glob --behaviors` ⇒ c98/c99 **giet_that** vì bỏ x, c18 sạch; c100 `gian_giao` vì không gọi iterdir KHÔNG được tính làm tín dụng chết. C3 dựa vào c98 và kết quả fixture, không dựa vào lỗi giàn giáo.

C9: Ruff **đỏ sẵn, delta=0**, không ghi “Ruff sạch”: `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` head/base cùng rc=1, chỉ F541 `f-string without any placeholders`, cột 19 tại cùng dòng nội dung của test; vị trí dịch 1677 → 1678 do import. So chuẩn hóa theo tên tệp/rule/thông báo/cột/nội dung dòng cho delta 0 (`criteria-summary.json`); `python3 -m ruff --version` ⇒ `ruff 0.15.15`. Chỉ đo bare lint theo tiêu chí; không suy đã đo pin/probe CI.

`python3 .claude/dev/packet_loop.py doctrine-scan --root .` head/base rc=0: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` head rc=1/0 dòng, base 2 dòng (1442/1601), mutant glob rc=0/1 dòng (116). Vế dương C1a/C1b đã đo riêng ở trên. `python3 summarize_l4.py` rc=0 đối chiếu các log criterion và cleanup bằng assertion; kết quả `evidence/criteria-summary.json`.

### Đợt 5 — toàn suite và chốt cuối

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` chạy `python3 ops/bien_nhan_v2_test.py` trong `work/head`: **rc=0, 401.34 s**, stderr rỗng, output:

```text
bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

`python3 extra_mutate.py narrow_helper --suite` đã hoàn tất phần suite trên bản sao mutant: **rc=1, 403.08 s**, stderr rỗng, **96/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt**, `TỔNG: ĐỎ`. Ca thường duy nhất đỏ:

```text
ĐỎ  c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang [giet_that]: []: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, không traceback
```

Log `head-suite.{json,stdout,stderr}` và `mut-narrow_helper-suite.{json,stdout,stderr}`. m154/m155 trong head đều **CÓ RĂNG / giet_that** tại đúng c100/c99. Không lấy rc đơn lẻ hoặc việc giàn giáo hỏng làm bằng chứng đạt. Không chạy toàn suite cho narrow_listing vì phép tái hiện được yêu cầu ở mutant ấy là ca đích; không suy số liệu toàn suite cho nó.

## Bảng tiêu chí cuối

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Suite head | **ĐẠT** | `python3 measure.py head suite`: rc=0, 97/97 · 151/151 · 2/2, `TỔNG: ĐẠT`; Đợt 5. |
| C1a | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | `probe.py head behaviors`: rc=1/tổng 2/nêu x; chỉ-x tổng 1/không “không có tệp”. `mutate.py exact --behaviors` giết thật c98, c18 sạch. |
| C1b | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Cùng phép behaviors: YAML hỏng đuôi hoa rc=2/nêu x/không traceback; mutant exact bỏ x. |
| C2 | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Suite head in `ĐẠT c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback`; `mutate.py isfile --behaviors` ⇒ c89 `giet_that`, c18 sạch. |
| C3 | **ĐẠT phép hoàn nguyên glob được yêu cầu** | `mutate.py glob --behaviors` ⇒ c98 `giet_that` vì tổng 1/bỏ x, c18 sạch. Không đưa mutant glob phụ thuộc nền vào bảng thường. |
| C4 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo độc lập job/runner/log Windows CI trên exact head trong lượt này. |
| C5 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo độc lập job/runner/log Ubuntu CI trên exact head trong lượt này; suite vừa chạy không được nhận là CI. |
| C6 | **ĐẠT** | `measure.py head gate`: rc=0/`tổng 306`/`TỔNG: ĐẠT`; lệnh `os.listdir` riêng đếm 306. Base cũng 306. |
| C7 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows local; không suy kết quả từ ghi chú lease/ADR hay báo cáo executor. |
| C8 — phần review | **ĐẠT ngưỡng nội dung review** | 0 P0/P1/P2/P3 mở, exact reviewed SHA đúng dòng 2; lượt cuối theo assignment. Các cổng CI/Windows chưa đo không được coi đã đạt; không cấp quyền merge/land. |
| C9 | **ĐẠT** | Ruff F delta 0; doctrine rc=0/10 tệp/0 chỗ; diff-check rc=0; glob 0 dòng; numstat đúng hai tệp +40/−5 và +283/−0. Đợt 1/4 và `criteria-summary.json`. |

## Bảng finding cuối

| Mức | Số finding mở | Vị trí / tái hiện / hướng vá |
|---|---:|---|
| P0 / P1 / P2 / P3 | **0 / 0 / 0 / 0** | Không có finding mới cần vá trong phạm vi đã đo. Bằng chứng đóng ba lớp lịch sử nằm ở bảng đối chiếu và Đợt 1–5. |

Không tạo mục `[P0..P3]` hay gán `HÌNH DẠNG` cho một lỗi không tồn tại. Các mutant tương đương hoặc chỉ sống ở một tầng được phân biệt rõ tại Đợt 3; không che mutant sống, cũng không biến đối chứng tương đương thành finding.

## Toàn vẹn cuối và giới hạn

`python3 integrity.py` qua `measure.run('integrity-run', ...)`: **rc=0**; `evidence/final-integrity.json` ghi lại lệnh và kết quả. Head/tree/base không đổi so neo ban đầu, detached, không nông, `core.abbrev=7`. Status gồm tracked/untracked/ignored của `cay-kho` và `work/head` rỗng; diff worktree/index so HEAD rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT4.patch byte-identical với diff tương ứng; SPEC giữ đúng SHA-256 dòng 3. Đây là đối chiếu nội dung tại hai mốc, không phải lời khẳng định đã quan sát toàn bộ lịch sử ghi.

`integrity.py` là script cũ duy nhất được chỉnh: mốc `previous-head` từ `99c463d` thành `8d9e3e3`, diff lượt từ `5efa311`/`DIFF-LUOT3.patch` thành `8d9e3e3`/`DIFF-LUOT4.patch`, cùng tên khóa assert tương ứng. Không đổi oracle kiểm toàn vẹn. `evidence/adapter-integrity.patch` giữ diff; `probe-provenance.json` ghi SHA-256 và xác nhận **15/16 script cũ nguyên byte**. Các script mới là `audit_l4.py`, `focused_l4.py`, `mutate_l4.py`, `summarize_l4.py`.

Tất cả tiến trình đo dùng cho kết luận đã hoàn tất. Các lỗi I/O được nêu là phép tiêm có hit kiểm chứng, không phải đo sự cố phần cứng/quyền truy cập thật. Windows CI/local và Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không dùng lời khai executor thay số đo, không sửa mã nguồn checkout được review, không cấp quyền merge/land.
