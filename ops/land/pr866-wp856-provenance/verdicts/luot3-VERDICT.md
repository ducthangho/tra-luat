Reviewed commit: bf671b0524a8472eb0b0fcd1d75ea3a89d1f6973
Verdict: approve — P0=0 P1=0 P2=0 P3=0

## Định danh và phạm vi

Reviewer độc lập OpenAI/Codex, công cụ shell cục bộ, transport machine/local, offline; lượt 3/8. Không tái dùng context executor hoặc gọi reviewer phụ. Không suy runtime attestation model/effort từ tài khoản vận chuyển.

HEAD `bf671b0524a8472eb0b0fcd1d75ea3a89d1f6973`, tree `b2eb7d07f6f36693e136e776fb15da45d107b991`; base `94220547cd155c73392e95726e8daf353888b3aa`. Full clone, detached, worktree sạch cả tracked/untracked/ignored ở các mốc kiểm. Đặc tả, phụ lục và lease r1/g1 đã đọc; băm đặc tả và phụ lục khớp lần lượt `d50065e79fcb92c223fc1799418e266579e339b4033cc509ef22a083e6e8dd34` và `6b1c41958fb36eaeef35d32bd03c424ef7a90e5ab2d8a32cc7d67bc8bea9e85d`.

Diff base → head đúng `.claude/dev/packet_loop_test.py`, **+1071/−7**. `packet_loop.py` không đổi. KHO `/home/user/rv856` chỉ đọc; mọi ghi/đột biến nằm trong thư mục ra hoặc `/tmp`. [Định danh](evidence/repository-identity.json), [diff](evidence/review.diff), [spec](evidence/wp856.md), [lease](evidence/lease.yaml).

## Bảng lớp

Không còn finding trong `tap_toan_tu` T1–T6 sau các phép đo dưới đây.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| — | — | Không có lớp mở | A1–A8 và đối chiếu lượt trước | Không cần HINT.patch |

## A4 — ma trận độc lập và các dòng tương đương

Dựng từ biểu thức/AST hai hàm trên base, rồi đối chiếu `_KG_MA_TRAN`; **706 ô lõi**: T1=148, T2=272, T3=48, T4=203, T5=35. Có 16 vòng/comprehension tường minh và 3 phép duyệt ngầm. Head thêm 26 hiện thực ép kiểu T1 và 160 hiện thực `hoặc` T2, thành **892 hàng**: T1=174, T2=432, T3=48, T4=203, T5=35. Khóa thiếu/thừa **0/0**.

Trong 892 hàng: **817** ô có đột biến sinh/kiểm kê, **73** tương đương, **2** regex `--bat-buoc` không áp dụng. Hai ô `id_max/bat_dau_xy,yx` hiện có bộ sinh qua `cmp_to_key`, không còn khai miễn.

Lệnh `python3 -B -u evidence/cell_audit.py <0..3> 4`, rc0 cả bốn worker: mỗi hiện thực khác chạy qua `chay_suite` + `_phan_loai_giet` trên đủ **414 ca kg**. Cả **817/817** ô cụ thể có nhân chứng GIẾT hành vi sạch; **73/73** dòng tương đương không có thay đổi CLI. Tổng **368,460 màu**: {'SONG': 357683, 'GIET': 9864, 'TIN_DUNG_GIA': 913}. Có **126** hàng dùng lại biên nhận khi toàn bộ source đột biến trùng SHA-256; đây là cùng một hiện thực được hai ô tham chiếu, không phải suy màu giữa hai source khác nhau.

Đã kiểm khác nguồn so với mutant đăng ký; sáu biểu thức ngắn có biên nhận hiện thực bổ sung riêng, dùng để thay hàng kiểm toán tương ứng, giữ nguyên dữ liệu gốc. Hiện thực độc lập dùng nhận kiểu mà giữ giá trị, chuyển đổi bảo toàn giá trị, phép nới giữ so nguyên văn (`x == y or ...`), API chuỗi không ràng buộc, slice object, namespace đối số mới và regex compile. Không lấy tín dụng giết từ ca đọc source/đếm AST hoặc các ca tự kiểm T2/T6/M5/M6; nhân chứng đóng ô phải là ca chức năng gọi CLI. Một guard tập khác rỗng ở nhóm id-max làm riêng phép đếm AST đỏ; màu ấy giữ trong dữ liệu và không được nhận làm thay đổi CLI hoặc finding.

Đã kiểm cả bổ đề lẫn suy luận: hằng/ASCII SHA bất biến; NFC không có tiền ảnh khác trong bảng chữ đích; NFC/NFKC không đổi surrogate; NFKC giữ ranh giới trắng/ngắt dòng, 1.340 phép ghép chuẩn không tạo/xóa ranh giới ấy. Chuỗi chưa sắp `completed`/`success` không là ảnh của phép sắp xếp, nên **riêng OR-sort-left** tương đương; pure-sort-left vẫn phải có mutant bị giết. `str(int)` đơn ánh ở năm vị trí chỉ so bằng/đếm khóa; bỏ `khai[0]` không đổi `any`; điều kiện tập khác rỗng không đổi phép duyệt. Không suy bổ đề bool NFKC thành tương đương cho chuẩn hóa rồi dùng tiếp.

[AST base](evidence/independent-ast.json), [ma trận độc lập](evidence/independent-matrix.json), [lời khai từng ô](evidence/matrix-claims.json), [tổng ma trận](evidence/matrix-summary.json), [các hiện thực bổ sung bằng API/lượng từ tương đương](evidence/alternative-overrides.jsonl), [bổ đề độc lập](evidence/equivalence-proofs.json). Biên nhận đầy đủ: [worker 0](evidence/cells-0.jsonl), [1](evidence/cells-1.jsonl), [2](evidence/cells-2.jsonl), [3](evidence/cells-3.jsonl).

## A1/A3, T6 và M5/M6

`python3 -B -u evidence/target_audit.py`, **rc0**: **817/817** mutant được ma trận tham chiếu đã chạy ca đích bằng subprocess Python thường; **818/818 màu GIẾT sạch**. **1.901 cặp CLI** dùng cùng argv/input nền và mutant; từng ca đích có thay đổi thật. Mọi rc thuộc 0/2/12. Không có tín dụng chỉ-sập hoặc chỉ kiểm source. [Từng ca đích và đầu ra](evidence/target-cli.jsonl), [tổng native](evidence/native-target-summary.json).

T6 lấy đủ **224 họ T1–T5** đã đăng trong CASES: **2.042 fixture từ chối**, thiếu bản sửa **0**; **443 bản sửa khác nhau**, cộng **18 ca đối số cũ**. Tất cả được chạy trong `kg_t6_ban_sua`; bản sửa ra rc0. Delta sửa đúng chốt logic: thay đối số cùng giá trị neo nguyên văn trong run, sửa một thành phần danh tính, hoặc thêm run cùng metadata đếm nhất quán. Không coi số đường dẫn JSON thay đổi là số chốt. [Kiểm kê T6](evidence/t6-summary.json), [mọi delta sửa](evidence/repair-deltas.json).

`python3 -B -u evidence/selfcheck_mutants.py`, **rc0**: **20/20** mutant nhắm test M5/M6/T6/độ phủ T2/ma trận làm đúng ca đỏ sạch, đối chứng khác họ xanh. Bao gồm gỡ thực thi bản sửa, bỏ một họ khỏi T6, bỏ phủ mọi chỉ số, bỏ hiện thực `hoặc`, và hai chốt của `_kg_ho`. Phản chứng có sẵn xác nhận **chỉ-sập ⇒ TIN_DUNG_GIA**, **sập rồi đỏ sạch ⇒ GIẾT**. Không tự soạn payload sập hoặc mã in/giả/bọc traceback. [20 tự kiểm](evidence/selfcheck-mutants.json).

## Gate và A1–A8

Gate native trên bản sao đầy đủ exact head, không dùng runner nhanh:

```text
cp -a /home/user/rv856 /tmp/rv856-r3-head
python3 -B -u /tmp/rv856-r3-head/.claude/dev/packet_loop_test.py
rc=0
nền: 864/864 đạt · BỎ QUA: 1
ca: 865 · đột biến: 1238
TỔNG: ĐẠT
```

**1.237 mutant GIẾT**, một mutant Windows được bỏ qua như base (`luong_canonical_chay_that_dao_os_name`, ngoài kg). Không khai đã giết cả 1.238. [Log gate](evidence/gate.log), [tổng gate](evidence/gate-summary.json).

| tiêu chí | kết quả |
|---|---|
| A1 | 817 mutant ma trận /818 ca đích GIẾT native; gate đối chứng khác họ xanh |
| A2 | 75/75 phụ lục GIẾT, có nhân chứng native; bảng từng tên dưới đây |
| A3 | T6 xanh; gỡ thực thi hoặc bỏ một họ làm đúng ca đỏ |
| A4 | Đủ 706 ô lõi +186 hiện thực bổ sung; 817 cụ thể GIẾT, 73 tương đương đứng vững |
| A5 | Gate native rc0, nền 864/864, TỔNG ĐẠT |
| A6 | Base 635 tên: 634 PASS +1 SKIP; head 865: 864 PASS +1 SKIP; vắng/trùng/đổi màu tên base 0 |
| A7 | doctrine-scan base/head rc0, 10 tệp/0 lỗi; adr-song rc0, 53/53. Ruff 0.16.9 cùng rc1 do 2 F541; delta F=0, F401/F821=0 |
| A8 | Đúng một tệp +1071/−7, không áp trần dòng; sản phẩm không đổi |

[Base từng tên/màu](evidence/base-colors.json), [đối chiếu tên/màu](evidence/base-head-names.json), [từng tên A6](evidence/A6-colors.csv), [lệnh/đầu ra A7](evidence/auxiliary-gates.json).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: lượt 1 `7302ea3623ebb7a0250a6c5090985807753cc031` (`rv1_hienvat_ro`) và lượt 2 `19fdfa6` (`rv2_hienvat_ro`). `python3 -B -u evidence/previous_native.py`, **rc0**: **108/108** hiện thực không tương đương tái dựng từ biên nhận cũ bị GIẾT native, mỗi hiện thực có CLI đổi thật. Gồm 18 ép kiểu +77 chỉ số giữa +11 phép nới chuỗi +2 max-prefix. Prompt nêu 110; reviewer không nhận số đó làm phép đo: dữ liệu phân lớp công bố và các JSONL tái dựng được 108, loại hai ứng viên OR-sort-left tương đương.

| lượt | slug | nhãn | bằng chứng trên exact head |
|---|---|---|---|
| 1 | `so-khop-tuyet-doi-chua-du` | **đã vá thật** | 20 ô dedup trái/phải có đủ; T2 đủ 272 ô lõi và các hiện thực nới bổ sung, A1/A4 đạt |
| 1 | `so-khop-so-nguyen-chua-chinh-xac` | **đã vá thật** | Tiền tố đầy đủ ở mọi vị trí số; hai hướng max có bộ sinh/kiểm kê và GIẾT native |
| 1 | `chuan-hoa-doi-so-chi-trong-phep-kiem` | **đã vá thật** | T5 tách chỉ-kiểm/dùng-tiếp, 32 mutant GIẾT; NFKC chỉ-kiểm có lập luận đúng |
| 1 | `fixture-vi-pham-nhieu-chot` | **đã vá thật** | Đủ 2.042+18 bản sửa, T6 xanh; gỡ thực thi hoặc bỏ họ làm đỏ |
| 2 | `kiem-kieu-chi-do-mot-loai-sai` | **đã vá thật** | 18 hiện thực ép kiểu từng sống bị GIẾT native; T1 174 ô và tích vị trí có răng |
| 2 | `so-khop-tuyet-doi-chua-du` | **đã vá thật** | 77 chỉ số giữa +11 hiện thực nới bị GIẾT native; A4 không còn ô cụ thể sống |
| 2 | `so-khop-so-nguyen-chua-chinh-xac` | **đã vá thật** | Hai ô max-prefix từng miễn sai đã được sinh vòng, kiểm kê và giết đúng ca |

[108 tìm/thay, argv và đầu ra nền/đột biến](evidence/previous-native.jsonl), [tổng](evidence/previous-native-summary.json). Không có lớp trong tập tái diễn ở lượt này để kích hoạt điều kiện dừng lần thứ ba.

## A2 — phát lại phụ lục, từng tên

`python3 -B -u evidence/replay.py 0 1`, **rc0**: mỗi mutant chạy đủ **414 ca kg** qua `chay_suite` + `_phan_loai_giet`, rồi chạy lại một ca giết bằng subprocess Python thường. **75/75 GIẾT**, không nhận tín dụng chỉ-sập. Tổng **31.050 màu**: {'SONG': 30554, 'GIET': 491, 'TIN_DUNG_GIA': 5}. Các màu TIN_DUNG_GIA ngoài nhân chứng được giữ nguyên trong dữ liệu; không dùng chúng để giết.

[Đủ màu/lỗi/native](evidence/replay-0.jsonl), [mã phát lại](evidence/replay.py).

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
| `boundary_name_left` | `kg_t2_ten_lstrip` |
| `boundary_status_left` | `kg_t2_status_bo_dau` |
| `boundary_status_right` | `kg_t2_status_bo_cuoi` |
| `boundary_warning_left` | `kg_t2_canh_bao_lstrip` |
| `dedup_boundary_first` | `kg_t2_dedup_bo_dau` |
| `dedup_boundary_left` | `kg_t2_dedup_lstrip` |
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

## Phương pháp, giới hạn và ngoài phạm vi

Các ma trận lớn chạy nguyên source entrypoint `__main__`, argv/env và byte streams riêng, không import/gọi thẳng hàm sản phẩm. Cache theo source/input chính xác; parser và mọi câu lệnh sản phẩm vẫn chạy. Các tối ưu chỉ cache tra gettext bất biến và khôi phục đúng mapping môi trường qua delta. Đối chiếu native/fork/exec-main **260/260** bằng rc/stdout/stderr (chuẩn hóa địa chỉ bộ nhớ), và phát lại sau mỗi thay đổi runner. Full gate, ca đích và 108 nhân chứng cũ dùng Python native. Sau khi ghi xong biên nhận, dọn thư mục tạm của lượt đo ấy để giữ dung lượng; xem `evidence/scratch-cleanup.json` và `evidence/gate-scratch-cleanup.json`. [Runner](evidence/review_lib.py), [parity cuối](evidence/parity.json), [ghi chú hạ tầng](evidence/infrastructure-notes.txt). Không gọi các màu ma trận nhanh là hàng trăm nghìn lượt subprocess native.

Không chấm đột biến ngoài T1–T6, nguồn gốc JSON/API, mã sản phẩm hoặc ca ngoài `kg_*`. Phản ánh helper tên chứa ` · ` của lượt 2 đã đo lại ngoài phạm vi: CLI rc0 và helper PASS trên head này ([biên nhận](evidence/outside-helper.json)); không tính hạng. Không có finding ngoài tập mới được đề nghị mở rộng. Không đo Windows; ca và mutant chỉ Windows được ghi SKIP riêng. Không push, mở PR, gửi tin, CI từ xa, merge hoặc deploy.

Không tự viết phản chứng traceback/sập/byte bất thường/symlink/thoát cây. Chỉ chạy các phản chứng sập có sẵn và đột biến bản vá theo phân công. Không có finding nên không tạo HINT.patch.

Snapshot đầu/cuối chỉ chứng minh không có delta quan sát được, không chứng minh lịch sử không từng ghi rồi hoàn nguyên; sandbox thực tế cấm ghi KHO, cho ghi thư mục ra và /tmp. Reviewed SHA và bytes tệp test được đối chiếu lại trước chốt verdict.
