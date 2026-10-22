Reviewed commit: 19fdfa6e48c8b203bd89362c18bd198ba81e9793
Verdict: changes_requested — P0=0 P1=0 P2=3 P3=0

## Định danh và phạm vi

Review độc lập Codex/OpenAI, họ `openai`, bằng agent qua API và shell cục bộ, offline. Không suy model/effort attestation hoặc surface CLI từ tên actor. Không gọi reviewer khác, không ghi KHO, không push, tạo PR, comment hoặc chạy CI từ xa. Đây là lời gọi 2/8 theo prompt.

- KHO `/home/user/rv856`, detached, full clone; head đúng SHA trên, tree `5e350fc2012459afd0e0f55de97e1e4b8523151e`.
- Base `94220547cd155c73392e95726e8daf353888b3aa`. Diff đúng `.claude/dev/packet_loop_test.py`, **+957/−7**. `packet_loop.py` không đổi; vượt số dòng đã được cho phép.
- Đọc trọn đặc tả T1–T6, M1–M4, A1–A8, điều kiện dừng và lease r1/g1. Spec SHA-256 `d50065e79fcb92c223fc1799418e266579e339b4033cc509ef22a083e6e8dd34`; phụ lục `6b1c41958fb36eaeef35d32bd03c424ef7a90e5ab2d8a32cc7d67bc8bea9e85d`, lấy đúng ref/path và băm lại.
- Chỉ tính hạng trong `tap_toan_tu`. Ngưỡng approve là cả bốn hạng bằng 0; ba lớp dưới đây đều trong tập.

[Định danh đầu lượt](evidence/repository-identity.json), [cuối lượt và hash tệp](evidence/final-identity.json), [diff](evidence/reviewed.diff). Head/tree và tracked/untracked status không đổi. Không có snapshot ignored đầu lượt; không nhận đây là chứng minh lịch sử mọi tệp trên máy.

## Bảng lớp

Mọi dòng chỉ tệp trên **head được review**, không phải số dòng của HINT. Có **106 hiện thực không tương đương sống đủ 413/413 ca kg**: 18 của T1, 77 biến thể chỉ số giữa và 11 biến thể T2 trong ma trận. Mỗi hiện thực sống có phản chứng CLI native không sập. Lớp T3 là miễn sai hai ô dù các ca hiện có đã bắt được chúng. Đếm ba lớp, không đếm mỗi hiện thực thành một finding.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `kiem-kieu-chi-do-mot-loai-sai` | P2 | `.claude/dev/packet_loop_test.py:5935`, `:6305`, `:6373` | `python3 -B evidence/coercion_audit.py` và `coercion_json.py`, rc0: 26 hiện thực; **18 SỐNG**, mỗi cái 413/413 SONG, 0 TIN_DUNG_GIA. Native fixture đơn chốt **rc12→0**. | Sinh cả giá trị không chuyển đổi được và giá trị ép kiểu bảo toàn; thêm mutant nhận/bỏ qua tương ứng vào cùng kiểm kê T1 và giữ bản sửa T6. |
| `so-khop-tuyet-doi-chua-du` | P2 | `.claude/dev/packet_loop_test.py:6432`, `:6440`, `:6454`, `:6515` | `middle_delete_audit.py`, rc0: **77/96 SỐNG**; `cell_audit.py` bốn worker, rc0: **11** hiện thực nới chuỗi SỐNG; tất cả đủ 413 ca. Native chỉ số giữa/sắp xếp **rc12→0**; cảnh báo **rc0 giữ nguyên nhưng stderr đổi**. | Phủ mọi chỉ số; thêm ảnh chuẩn hoá/sắp xếp và đối số không chuẩn; kiểm chiều nới vẫn giữ phép bằng gốc. Đăng ký mutant và tự kiểm độ phủ để không lấy tín dụng chỉ từ từ chối dữ liệu đúng. |
| `so-khop-so-nguyen-chua-chinh-xac` | P2 | `.claude/dev/packet_loop_test.py:6697` | `max_prefix.py`, rc0: hai hiện thực `id_max` qua tiền tố đầy đủ và `cmp_to_key`, đủ 413 ca; native `kg_t3_id_max` GIẾT sạch, cặp 1/12 và −12/−1 **rc0→12**. | Thay hai `khong_ap_dung` bằng mutant sinh vòng qua `_kg_o`, dùng fixture hiện có. Đây là thiếu bộ sinh/kiểm kê, không phải thiếu ca phát hiện hành vi. |

### T1 — miền giá trị ép kiểu bị bỏ sót

`float` chỉ được sinh bằng `1.5`; list chỉ dạng `[1]`, str chủ yếu `x`. Các cách hiện thực cùng toán tử T1 sau không được kích hoạt:

- Nhận sau ép `float.is_integer()` hoặc bỏ phần tử ấy: run id và suite id (`1.0`).
- Nhận/bỏ object chuyển được từ list cặp khoá/giá trị: phần tử run, `check_suite`, trang.
- Nhận/bỏ object/list đọc được từ chuỗi JSON: phần tử run, `check_suite`, trang, `check_runs`.

Chín ô miền giá trị × hai cách nhận/bỏ qua = 18 hiện thực sống. Fixture native có một bản hợp lệ cùng bản trùng sai kiểu, hoặc trang rỗng sai kiểu, `total_count=1`; sửa riêng kiểu cho ra rc0. Cả nhận và bỏ đều ra rc0 mà không bị số id chặn hộ. Ép chuỗi số thập phân và float của total_count đã bị ca cũ bắt, không tính chúng là biểu hiện sống.

[Đủ màu, tìm/thay và native](evidence/coercions.jsonl), [chuỗi JSON](evidence/coercion-json.jsonl), [mã đo](evidence/coercion_audit.py), [mã đo JSON](evidence/coercion_json.py).

### T2 — chỉ số giữa và chiều nới một phía

Toán tử “bỏ một ký tự giữa” không có nghĩa chỉ bỏ đúng `len(s)//2`. Ví dụ xoá chỉ số 2 ở cả hai phía nhận `suxcess` như `success`; toàn suite vẫn xanh. Đã quét mọi chỉ số nội bộ của các giá trị chuẩn, ở đủ tám vị trí so chuỗi:

| vị trí | số hiện thực sống | chỉ số sống (từ 0) |
|---|---:|---|
| `canh_bao` | 0 | — |
| `conclusion` | 2 | 2, 4 |
| `dedup` | 0 | — |
| `dt_head` | 34 | 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38 |
| `dt_ten` | 0 | — |
| `head` | 36 | 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38 |
| `status` | 5 | 2, 3, 5, 6, 7 |
| `ten` | 0 | — |

Đồng thời, các bản nới `x == y or projection(x/y)` giữ dữ liệu đúng được chấp nhận nhưng vẫn nhận chuỗi sai. Các fixture hiện có chủ yếu dùng đích chuẩn và/hoặc giết bản chiếu vì nó từ chối dữ liệu đúng. Những ô sau sống; đã có native phân biệt từng ô:

| vị trí | toán tử |
|---|---|
| `status` | `sap_xep:phai` |
| `conclusion` | `sap_xep:phai` |
| `head` | `sap_xep:trai` |
| `head` | `sap_xep:phai` |
| `canh_bao` | `casefold:phai` |
| `canh_bao` | `strip:phai` |
| `canh_bao` | `lstrip:phai` |
| `canh_bao` | `rstrip:phai` |
| `canh_bao` | `nfc:phai` |
| `canh_bao` | `nfkc:phai` |
| `canh_bao` | `sap_xep:trai` |

Bảy biến thể tại so tên đã bị các ca dedup bắt qua sai số tên đỏ, nên **không** tính chúng là sống. Hai ứng viên OR-sort phía trái trước hằng `completed`/`success` thực ra đồng nhất với gốc vì hằng không được sắp; đã loại chúng và đo lại bằng toán tử một phía đầy đủ, cả hai bị giết. Không lấy ứng viên tương đương làm finding.

[Đủ màu 96 biến thể và native](evidence/middle-delete.jsonl), [ma trận tổng](evidence/matrix-summary.json), [native sắp xếp](evidence/sorting-native.json), [native chuẩn hoá đối số](evidence/normalizers-native.json), [hai ô đo lại](evidence/cells-overrides.jsonl).

### T3 — `max` vẫn áp dụng được phép so tiền tố

Hai ô `id_max/bat_dau_xy` và `id_max/bat_dau_yx` bị miễn với lý do cần thứ tự toàn phần. Nhưng Python `max` thực thi bộ so qua `cmp_to_key`, không kiểm tính toàn phần. Một hiện thực nới hợp lệ coi cặp có quan hệ tiền tố là bằng nhau, rồi dùng so số thường cho cặp còn lại. Hai hướng giữ nhầm id đầu tiên ở 1/12 và −12/−1, không sập và không tương đương CLI.

Các ca `kg_t3_id_max` đã bắt được cả hai. Tuy nhiên không có mutant sinh vòng/kiểm kê cho hai ô áp dụng được, trái M1/A4; chiếu một ký tự đầu không hiện thực tiền tố đầy đủ. Đã quét tám vị trí số, chỉ hai ô max bị miễn sai. [Mã đo](evidence/max_prefix.py), [toàn bộ màu và native](evidence/max-prefix.json).

## Ma trận độc lập, ca đích và tín dụng giết

Dựng từ hai hàm trên base, rồi mới đối chiếu khai báo: **T1=148, T2=272, T3=48, T4=203, T5=35**, tổng **706**. AST có 16 vòng/comprehension, cộng ba phép duyệt ngầm; các guard thuần chọn đầu/cuối của những phép duyệt còn lại tương ứng các lát cắt đã có.

Khoá khai báo thiếu/thừa 0/0; việc khớp khoá không đóng ba finding ngữ nghĩa trên. Phân loại đúng: 654 ô cần mutant (652 có, hai max thiếu), 50 tương đương, hai regex `--bat-buoc` không áp dụng. Đã thử hiện thực khác trên **704 ô áp dụng**, mỗi ô đủ 413 ca: **290.752 màu**; 643 bị giết sạch, 50 tương đương không có ca CLI đỏ, 11 sống. Không có ô chỉ được cấp GIẾT nhờ ca đọc source/đếm AST. Phép đo 96 chỉ số và 26 ép kiểu là các quét bổ sung cùng toán tử.

[Ma trận](evidence/independent-matrix.json), [AST base](evidence/independent-ast.json), [bộ đo](evidence/cell_audit.py), [tổng](evidence/matrix-summary.json). Dữ liệu từng worker: [0](evidence/cells-0.jsonl), [1](evidence/cells-1.jsonl), [2](evidence/cells-2.jsonl), [3](evidence/cells-3.jsonl).

A1: **652/652** mutant được ma trận tham chiếu đã chạy ca đích bằng Python subprocess thường, **653 màu ca đích GIẾT**. Có 1.366 lượt CLI mutant và đối chiếu baseline cùng argv/input; mọi lượt mutant rc thuộc 0/2/12, tất cả mutant có rc/stdout/stderr đổi thật. Cờ `changed` so byte gốc; trường text hiển thị dùng `_txt` như harness. Không coi rc giữ nguyên là tương đương nếu chẩn đoán đã đổi.

[Native từng ca đích](evidence/target-cli.jsonl), [tổng A1/A6](evidence/native-target-summary.json).

Các phép quét lớn vẫn gọi `chay_suite` và `_phan_loai_giet`, chạy toàn source entrypoint `__main__` với argv/streams/môi trường riêng, cache theo source và input, không gọi trực tiếp hàm sản phẩm. Có **260/260** mẫu native/fork/exec-main cùng rc/stdout/stderr (chuẩn hoá địa chỉ bộ nhớ). Full gate, mọi nhân chứng ca đích và phản chứng native dùng subprocess Python thường. Không nhận parity này là phép đo native toàn bộ hàng trăm nghìn lượt.

Một ô tương đương `T4/id_max/chi_khi_khac_rong` làm riêng `kg_t_ma_tran` đỏ vì biểu thức phụ tăng số nút AST từ 16 lên 17; 412 ca khác xanh và CLI không đổi. Đó không phải nhân chứng giết hành vi; đã giữ nguyên dữ liệu và không cấp tín dụng từ phép đếm source.

[Runner](evidence/review_lib.py), [parity](evidence/parity.json). Các tạo tác bộ đo nháp đã bị loại và chạy lại được ghi riêng ở [ghi chú hạ tầng](evidence/infrastructure-notes.txt), không tính thành finding hay GIẾT.

50 dòng tương đương đã được đọc lập luận, không chỉ nhận màu xanh: chuẩn hoá phía hằng/ASCII SHA bất biến; NFC không có tiền ảnh ngoài bảng chữ mục tiêu; `str(int)` đơn ánh ở các vị trí chỉ so bằng/đếm khoá; bỏ `khai[0]` không đổi `any`; guard tập khác rỗng không đổi phép duyệt. Đo độc lập toàn miền Unicode scalar và 1.340 cặp ghép chuẩn, không có phản ví dụ; Hangul/surrogate không tạo biên trắng/ngắt dòng hay tiền ảnh ASCII. Bổ đề NFKC chỉ tha **kiểm bool**, không tha chuẩn hoá đối số rồi dùng tiếp.

[Bổ đề độc lập](evidence/equivalence-proofs.json), [mã đo](evidence/equivalence_proofs.py).

## T6, M5/M6 và đối chiếu 79 biến thể cũ

T6 duyệt đủ **1.092 fixture từ chối được sinh**, thiếu bản sửa 0, cộng **18** ca đối số cũ. Baseline native có `kg_t6_ban_sua` và `kg_t6_co_rang` xanh. Đã đọc delta bản sửa: các thay đổi ở đối số cùng run khớp nguyên văn, danh tính tuple hoặc metadata đếm đi cùng dữ liệu là cùng chốt logic; không đếm số đường dẫn JSON như số chốt độc lập.

**18/18** mutant nhắm test M5/M6/T6/ma trận làm đúng ca đỏ sạch, đối chứng khác họ xanh. `_kg_ho` giữ chuẩn chỉ-sập ⇒ TIN_DUNG_GIA, sập rồi đỏ sạch ⇒ GIẾT. Các phản chứng sập chạy nguyên từ cây, không tự soạn payload hay mã in/giả/bọc traceback.

[Kiểm kê T6](evidence/t6-coverage.json), [delta sửa](evidence/repair-deltas.json), [18 tự kiểm](evidence/selfcheck-mutants.json).

79 biến thể lượt trước: 75 có AST hai hàm trùng đúng mutant đã đo native; bốn chuẩn hoá đối số còn lại chạy lại đủ 413 ca và có nhân chứng native GIẾT. Không dùng AST thay phép chạy khi AST khác. [Biên nhận 79](evidence/previous-79.json).

## Gate và A1–A8

Tạo bản sao đầy đủ gồm `.git` bằng `shutil.copytree(..., symlinks=True)` trước phép đo; base được checkout detached trong bản sao riêng. Gate thật:

```text
python3 -B -u /tmp/rv856-r2-head/.claude/dev/packet_loop_test.py
rc=0
nền: 863/863 đạt · BỎ QUA: 1
ca: 864 · đột biến: 1071
TỔNG: ĐẠT
```

**1.070** mutant có dòng giết thành công; một mutant chỉ Windows được bỏ qua như base, không gọi là đã giết cả 1.071. Hai dòng `ok` kiểm ánh xạ AC18/AC19 giải thích tổng 1.072 dòng `ok` trong log.

| tiêu chí | kết quả |
|---|---|
| A1 | Đạt ca đích/đối chứng và không sập; 652 mutant của ma trận đo native độc lập |
| A2 | 75/75 GIẾT, có nhân chứng native; xem bảng từng tên dưới đây |
| A3 | Đạt T6 và gỡ tự kiểm làm đỏ; thiếu độ phủ toán tử được tính ở A4 |
| A4 | **Không đạt: ba lớp P2** |
| A5 | Đạt gate native rc0, 863/863, TỔNG ĐẠT; một skip Windows có sẵn |
| A6 | Base 635 tên: 634 PASS +1 SKIP; head 864 tên: 863 PASS +1 SKIP; vắng/đổi màu tên base 0 |
| A7 | doctrine-scan base/head rc0, 10 tệp/0 lỗi; adr-song rc0, 53/53. Ruff 0.16.9 cùng rc1 do 2 F541, delta F=0; F401/F821=0 |
| A8 | Một tệp +957/−7, sản phẩm không đổi; không áp trần số dòng |

[Log gate đầy đủ](evidence/gate.log), [tổng gate](evidence/gate-summary.json), [màu base từng tên](evidence/base-colors.json), [lệnh/đầu ra A7](evidence/auxiliary-gates.json).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 1: `7302ea3623ebb7a0250a6c5090985807753cc031`, hiện vật `rv1_hienvat_ro`; đã đọc diff từ lượt ấy tới head.

| lớp lượt 1 | nhãn | bằng chứng trên head hiện tại |
|---|---|---|
| `so-khop-tuyet-doi-chua-du` | **vá hờ** | 20 ô dedup một phía đã có và 79 biến thể cũ bị bắt; còn 77 chỉ số giữa và 11 hiện thực nới chuỗi sống cùng lớp |
| `so-khop-so-nguyen-chua-chinh-xac` | **vá hờ** | Tiền tố đầy đủ ở các vị trí đã được thêm và giết; còn hai ô max miễn sai, thiếu mutant/kiểm kê |
| `chuan-hoa-doi-so-chi-trong-phep-kiem` | **đã vá thật** | Phân biệt chỉ-kiểm và dùng-tiếp, kiểm đủ T5; biến thể đối số cũ bị giết; NFKC chỉ-kiểm có lập luận CLI đúng |
| `fixture-vi-pham-nhieu-chot` | **đã vá thật** | T6 lấy mọi họ qua `.muc`, đủ sửa 1.092+18, gỡ một họ hoặc gỡ thực thi sửa đều làm đúng ca đỏ |

`kiem-kieu-chi-do-mot-loai-sai` là lớp mới ghi nhận ở lượt này của #856, nối slug lịch sử #822. Không đổi slug để giấu tái diễn. Hai lớp trước được đóng thật/4; không lấy việc vá riêng 79 mẫu làm bằng chứng đóng cả tập toán tử.

## HINT.patch

[HINT.patch](HINT.patch) là **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Chỉ chạm `.claude/dev/packet_loop_test.py`, áp được trên exact head.

- T1: thêm dạng chuyển đổi bảo toàn giá trị, fixture bản lặp đơn chốt cùng sửa T6, 18 mutant nhận/bỏ qua để khoá miền mới.
- T2: mọi chỉ số, ảnh chuẩn hoá/sắp xếp và đích không chuẩn/đã sắp; thêm mutant nới giữ so nguyên văn và ca tự kiểm độ phủ dữ liệu. Gỡ phạm vi về bốn chỉ số làm ca tự kiểm đỏ sạch.
- T3: sinh hai mutant max-prefix qua cùng bộ đăng ký và classifier.

Đã kiểm `git apply --check` rc0, áp cây riêng cho bytes trùng bản thử; Ruff vẫn 2 F541/delta0. Nền hint **414 ca kg xanh**; **96/96** biến thể chỉ số bị giết; **38** mutant bổ sung đo native có ca đích GIẾT/đối chứng xanh; mutant nhắm tự kiểm độ phủ cũng GIẾT sạch. Không khai đã chạy full gate 1.110 mutant của hint. Rủi ro chính là tăng fixture/thời gian suite; executor cần chạy gate trên SHA sau áp và tái dẫn xuất patch.

[Apply/hash](evidence/hint-apply.json), [nền +96 biến thể](evidence/hint-results.json), [38 mutant native](evidence/hint-generated.json), [tự kiểm có răng](evidence/hint-selfcheck.json).

## Ngoài phạm vi

`_kg_kiem` mới tách tên bằng ` · `, nên báo sai với tên hợp lệ chứa chính dấu ấy. `python3 -B evidence/outside_helper.py`, rc0: CLI native nhận `gate · extra` với rc0, helper ném AssertionError. Đây là giả định trình bày của helper, ngoài các ô toán tử trên hai hàm sản phẩm; **không tính hạng**. [Biên nhận](evidence/outside-helper.json). Chủ kho quyết định có mở rộng tập hoặc làm packet riêng.

Không sửa `packet_loop.py`, không chấm nguồn gốc API/JSON, không mở chiều ngoài tập hay ca ngoài `kg_*` thành finding.

## A2 — biên nhận từng đột biến phụ lục

Lệnh `python3 -B -u evidence/replay.py 0 1`, rc0; từng mutant chạy đủ 413 ca qua `chay_suite` + `_phan_loai_giet`, rồi chạy lại nhân chứng bằng Python native. **75/75 GIẾT, 0 tín dụng chỉ-sập được nhận.** Có năm màu TIN_DUNG_GIA ngoài nhân chứng của `schema_page_ends`; ghi nguyên trạng, không dùng chúng để giết. Tổng 30.975 màu: 30.482 SONG, 488 GIET, 5 TIN_DUNG_GIA.

[Tổng](evidence/replay-summary.json), [toàn bộ màu/lỗi/native](evidence/replay-0.jsonl), [mã phát lại](evidence/replay.py).

| đột biến | ca giết native |
|---|---|
| `suite_digits_interior_space` | `kg_t5_suite` |
| `suite_digits_interior_unicode` | `kg_t5_suite` |
| `count_negative_last` | `kg_t4_trang_tc_am` |
| `count_negative_page_ends` | `kg_t4_trang_tc_am` |
| `count_presence_last` | `kg_t1_total_count_vang` |
| `count_presence_page_ends` | `kg_t1_total_count_vang` |
| `count_type_page_ends` | `kg_t1_total_count_null` |
| `run_shape_page_ends` | `kg_t1_phan_tu_null` |
| `schema_page_ends` | `kg_t1_id_null` |
| `suite_shape_page_ends` | `kg_t1_check_suite_null` |
| `count_coerce_dict` | `kg_t1_total_count_dict` |
| `count_coerce_list` | `kg_t1_total_count_list` |
| `presence_skip_head_sha` | `kg_t1_head_sha_vang` |
| `presence_skip_id` | `kg_t1_id_vang` |
| `presence_skip_name` | `kg_t1_name_vang` |
| `run_shape_skip_bool` | `kg_t1_phan_tu_bool` |
| `run_shape_skip_float` | `kg_t1_phan_tu_float` |
| `run_shape_skip_list` | `kg_t1_phan_tu_list` |
| `run_shape_skip_null` | `kg_t1_phan_tu_null` |
| `run_shape_skip_str` | `kg_t1_phan_tu_str` |
| `suite_shape_skip_bool` | `kg_t1_check_suite_bool` |
| `suite_shape_skip_float` | `kg_t1_check_suite_float` |
| `suite_shape_skip_int` | `kg_t1_check_suite_int` |
| `suite_shape_skip_str` | `kg_t1_check_suite_str` |
| `run_identity_abs` | `kg_t3_id_danh_tinh` |
| `run_identity_abs_safe` | `kg_t3_id_danh_tinh` |
| `run_identity_float` | `kg_t3_id_danh_tinh` |
| `run_identity_float_safe` | `kg_t3_id_danh_tinh` |
| `suite_anchor_abs_safe` | `kg_t3_suite_neo` |
| `suite_anchor_float` | `kg_t3_suite_neo` |
| `suite_identity_abs` | `kg_t3_dt_suite` |
| `suite_identity_float` | `kg_t2_dt_ten_casefold` |
| `suite_identity_strprefix` | `kg_t2_dt_ten_casefold` |
| `suite_range_positive` | `kg_t3_dt_suite` |
| `suite_range_small` | `kg_t3_dt_suite` |
| `suite_warning_abs_safe` | `kg_t3_suite_canh_bao` |
| `suite_warning_float` | `kg_t3_suite_canh_bao` |
| `suite_warning_strprefix` | `kg_t3_suite_canh_bao` |
| `warning_id_abs` | `kg_t3_id_canh_bao` |
| `warning_id_float` | `kg_t3_id_canh_bao` |
| `boundary_conclusion_left` | `kg_t2_conclusion_bo_dau` |
| `boundary_conclusion_right` | `kg_t2_conclusion_bo_cuoi` |
| `boundary_dt_head_left` | `kg_t2_dt_ten_casefold` |
| `boundary_dt_head_right` | `kg_t2_dt_ten_casefold` |
| `boundary_dt_name_left` | `kg_t2_dt_ten_casefold` |
| `boundary_dt_name_right` | `kg_t2_dt_ten_casefold` |
| `boundary_head_left` | `kg_t2_head_bo_dau` |
| `boundary_head_right` | `kg_t2_head_bo_cuoi` |
| `boundary_name_left` | `kg_t2_ten_bo_dau` |
| `boundary_status_left` | `kg_t2_status_bo_dau` |
| `boundary_status_right` | `kg_t2_status_bo_cuoi` |
| `boundary_warning_left` | `kg_t2_canh_bao_bo_dau` |
| `dedup_boundary_first` | `kg_t2_dedup_bo_dau` |
| `dedup_boundary_left` | `kg_t2_dedup_bo_dau` |
| `dedup_casefold` | `kg_t2_dedup_casefold` |
| `dedup_nfc` | `kg_t2_dedup_nfc` |
| `dedup_nfkc` | `kg_t2_dedup_nfc` |
| `dedup_position_middle` | `kg_t2_dedup_ho` |
| `dedup_position_sorted` | `kg_t2_dedup_sap_xep` |
| `dedup_strip` | `kg_t2_dedup_strip` |
| `position_conclusion_middle` | `kg_t2_conclusion_ho` |
| `position_conclusion_sorted` | `kg_t2_conclusion_sap_xep` |
| `position_dt_head_middle` | `kg_t2_dt_ten_casefold` |
| `position_dt_head_sorted` | `kg_t2_dt_ten_casefold` |
| `position_dt_name_middle` | `kg_t2_dt_ten_casefold` |
| `position_dt_name_sorted` | `kg_t2_dt_ten_casefold` |
| `position_head_middle` | `kg_t2_head_ho` |
| `position_head_sorted` | `kg_t2_head_sap_xep` |
| `position_name_middle` | `kg_t2_ten_ho` |
| `position_name_sorted` | `kg_t2_ten_sap_xep` |
| `position_status_middle` | `kg_t2_status_ho` |
| `position_status_sorted` | `kg_t2_status_sap_xep` |
| `position_warning_middle` | `kg_t2_canh_bao_ho` |
| `position_warning_sorted` | `kg_t2_canh_bao_sap_xep` |
| `status_slice_first` | `kg_t2_status_bo_dau` |
