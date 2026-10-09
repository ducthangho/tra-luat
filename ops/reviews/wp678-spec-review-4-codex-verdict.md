verdict: changes_requested
reviewed_sha: a9019a911a4fe2770ede5abafebc41afbd97aa16
spec_sha256: 2726d59ffb683f44e68c1409241250c40025bc02a9c9bfb257e767831a1e17f2
model/effort tự khai: GPT-6 (Codex); không có tham số effort được công bố cho phiên.

Kết luận: **0 P1 / 1 P2 / 0 P3**. Còn lớp `bo-quet-chung-cu-khong-neo-anh`: báo cáo có thể gắn bytes blob sai băm với OID của ảnh đã chụp rồi báo sạch. Các phản chứng cũ về replace, race và phân loại CLI đã đóng. Điều kiện dừng §9 được kích hoạt; HINT gỡ mã tham chiếu và bảo toàn A9 bằng hợp đồng chứng cứ/trình tự trước–sau cấp lease.

provider: openai_codex
execution_surface: API agent có công cụ shell cục bộ (không phải ChatGPT Web)
transport: machine; bàn giao hiện vật cục bộ, không có GitHub submitter
assurance: review nội dung độc lập; không tự cấp approval/land authority. Exact served model/effort và session identity theo máy: KHÔNG ĐO ĐƯỢC từ hiện vật được cấp.

Đã đọc toàn bộ prompt.snapshot. Kiểm định đầu vào: sha256sum SPEC.md và git -C cay-kho rev-parse HEAD khớp định danh yêu cầu.

## ĐỐI CHIẾU LƯỢT TRƯỚC
Đã kiểm trước khi săn mới: `PYTHONDONTWRITEBYTECODE=1 python goi/recheck.py` → `PRECHECK_DONE`; log `goi/recheck.log`. Mô hình chốt nằm trong scratch, chỉ chứng minh tính khả thi, không phải mã ứng viên.

| lớp lượt 1–3 | trạng thái | bằng chứng chạy lại |
|---|---|---|
| bo-quet-chung-cu-khong-neo-anh | **CÒN MỞ** ở biểu hiện bytes blob; replace/race cũ ĐÃ ĐÓNG | `tukiem_r4.sh`: replace commit/blob r4 rc=1, r3 rc=0 trên cùng kho; cùng blob hai miền: 1 blob/2 cặp; `race_r4.py`: giữ OID cũ, errors có int, tự kiểm True. |
| bo-quet-khong-co-cua-chay | ĐÃ ĐÓNG các biểu hiện cũ | Entry point cho good0/JSON, lỗi lease1/JSON; argv, thiếu Git/YAML, decode, ngày, số dài, sâu đều2/không JSON. Log `goi/recheck-scanner.log`. |
| bang-duong-phan-loai-sai | ĐÃ ĐÓNG | diff nền có t131 hai hunk, t139/t192; r4 ghi đúng. Hai bảng tách CLI và seam; script race được cấp và chạy rc0/True. D7/D8/D9 đúng các dòng in trong recheck.log. |
| bo-quet-nghiem-thu-thieu-mien | ĐÃ ĐÓNG các phản chứng cũ | .yml, local-only, topic/HEAD, thiếu ID, nonmapping, parse, pointer list/trắng đều1; thay_the_cho=[] hợp lệ0. Tự dựng blank-list: r2 CLI0/rỗng và quet=(1,1,1,[]), r4 rc1 đúng field. |
| tieu-chi-dot-bien-khong-phan-biet-chot | ĐÃ ĐÓNG | D2 strict8→restore RETURN/L RETURN nhưng probe RETURN/GH0; D5_self/peer False→True, D6_self/peer8→RETURN; từng toán hạng riêng, đối chứng chuỗi True/RETURN. |
| so-do-nen-khong-khop | ĐÃ ĐÓNG biểu hiện A6 | Hai ref/path thực: nền rc11, NGƯỜI_GIỮ1:True. A6 chốt nhãn và cả ref/path, không chỉ nonzero; số ảnh/suite đo tiếp riêng. |
| hop-dong-dong-bang-thieu-neo | ĐÃ ĐÓNG trong phạm vi lời khai được giao | Mission682/object5627190292 + closure trong bytes; đổi required_checks đổi băm (`CLOSURE hash_changes=True`). Chưa xác minh live và không yêu cầu điều đó. |
| objective-dong-nhat-cu-phap-voi-danh-tinh | ĐÃ ĐÓNG | quoted/tagged yes và1.5 bằng nhau sau safe_load; objective r4 chấp nhận cùng chuỗi là cùng danh tính. |
| trang-thai-q3-chua-dong-bo | ĐÃ ĐÓNG | `Q3 anchors=2 open_question=False`, neo5885268193; authority theo prompt. |

Bảng đã cập nhật bằng hướng 1: không gọi cả lớp provenance đã đóng chỉ vì các phản chứng cũ qua. Các lớp còn lại đóng trong phạm vi đã kiểm, không phải lời hứa vét hết mọi đầu vào. Lệnh scanner: `review_scratch=$(cat goi/scratch-path); PYTHONDONTWRITEBYTECODE=1 TMPDIR="$review_scratch" bash tukiem_r4.sh "$review_scratch"`; race: `PYTHONDONTWRITEBYTECODE=1 python "$review_scratch/race_r4.py"`. 28 ca r4 và 2 đối chứng r3; race là phép đo trực tiếp, không tính CLI.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện (vị trí trong SPEC) | phương án chung | phép kiểm / giới hạn |
|---|---|---|---|---|
| bo-quet-chung-cu-khong-neo-anh | P2 | Phụ lục A :367–372, :402–404, :429: tắt replace nhưng nhận bytes do cat-file trả mà không kiểm băm blob; map/pairs vẫn khai OID cũ | Thực hiện stop §9: gỡ mã tham chiếu, hạ §8 về tham khảo; A9 phải kiểm bytes/OID và có dụng cụ trước cấp lease độc lập với helper sau cấp | `hunt_scanner.py objects`, `object_confirm.py`: blob hỏng 1→0 dù same map; fsck3/hash mismatch; khôi phục→1/fsck0. Cùng phép thử commit/tree bị chặn2. Chỉ fixture scratch có hỏng, không cáo buộc snapshot thật. |

Giữ slug của lượt 2–3 vì cùng nguyên nhân: thông tin OID trong báo cáo chưa đủ ràng buộc nội dung đã đọc. Không tạo lớp mới cho mỗi tầng Git hay mỗi biến thể. Có một biểu hiện còn mở; không xếp thành lỗi mã sản phẩm hoặc P1 vì Q1–Q4 và D1–D8 vẫn khả thi.

## BẢNG SĂN

Sáu hướng độc lập mới được tính là **1, 2, 3, 8, 9, 10**: toàn vẹn bytes/OID; phân loại ngoại lệ YAML; đóng khung tên path/ref; độ nhạy của giàn tự kiểm; khử trùng theo cặp trên đồ thị nhiều phiên bản; ranh giới root detached/tag so runtime. Chúng thay các biến khác nhau và không lấy việc chạy lại phản chứng cũ làm hướng mới. Hướng 4–7 giữ riêng để đáp ứng đối chiếu số r4/phần ngoài HINT/stop condition; không cần tính chúng để đủ ngưỡng. Phần runtime kế thừa cũng không tính.

### HƯỚNG 1: OID gốc và object hỏng sau khi tắt replace

- Giả thuyết: Tắt replace vẫn có thể đọc bytes không mang OID báo cáo nếu Git object-store hỏng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunt_scanner.py objects`
- Output thật:
```text
UTC 2026-09-29T09:56:11.513214+00:00
control 1 head e24038be4d5e0b59dbb459f851d9bc8b15e6743a blob 0a0253c78fafc3c43ecb09a2df533c9607984c14 errors [['ops/leases/a.yaml', 'lease_id=1000']]
wrong_hash 0 same_map True reported_blob 0a0253c78fafc3c43ecb09a2df533c9607984c14 actual_hash 13e1d8b32c17b85b5c103b834d5bf5f4f9557f44 errors []
fsck 3 error: 13e1d8b32c17b85b5c103b834d5bf5f4f9557f44: hash-path mismatch, found at: .git/objects/0a/0253c78fafc3c43ecb09a2df533c9607984c14
missing_blob 2 json False KHONG_DO_DUOC: KhongDoDuoc: git cat-file blob 0a0253c78fafc3c43ecb09a2df533c9607984c14 rc=128: fatal: git cat-file 0a0253c78fafc3c43ecb09a2df533c9607984c14: bad file
```
- Kết luận: LỖI P2, cùng lớp `bo-quet-chung-cu-khong-neo-anh`. Cam kết là chứng cứ về ảnh OID gốc; dữ liệu lỗi ở object store chưa bị chặn và vẫn nhận JSON sạch. Phản chứng cần object-store hỏng được dựng chủ ý, không phải một lease YAML thông thường; không đòi chống người kiểm soát toàn bộ máy. Cổng có thể yêu cầu/kiểm toàn vẹn nguồn thay vì tin cat-file. Snapshot cấp thực tế không có lỗi băm blob (hướng4).

### HƯỚNG 2: Biên YAML/mã hoá/tài nguyên ngoài bảng mới

- Giả thuyết: Biên Exception mới có thể phân sai constructor hoặc lỗi output; thử các dạng không có trong script được cấp.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunt_scanner.py yaml`
- Output thật:
```text
UTC 2026-09-29T09:55:47.690186+00:00
unknown_tag bytes 17 rc 1 json True errors [['ops/leases/a.yaml', 'parse']]
bad_int bytes 21 rc 2 json False errors KHONG_DO_DUOC: ValueError: invalid literal for int() with base 10: 'nope'
null_byte bytes 18 rc 1 json True errors [['ops/leases/a.yaml', 'parse']]
bad_timestamp bytes 31 rc 2 json False errors KHONG_DO_DUOC: ValueError: hour must be in 0..23
utf16 bytes 26 rc 2 json False errors KHONG_DO_DUOC: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
unicode_note bytes 35 rc 0 json True errors []
recursive_extra bytes 28 rc 0 json True errors []
surrogate bytes 19 rc 1 json True errors [['ops/leases/a.yaml', "lease_id='\\ud800'"]]
large_note bytes 1000022 rc 0 json True errors []
```
- Kết luận: KHÔNG PHẢI LỖI ở các nhánh đã đo. YAMLError→1/JSON; ngoại lệ ngoài YAMLError/giải mã→2; tài liệu lớn và alias phụ vẫn xử lý được. Chưa đo OOM/kill/timeout hoặc mọi kích thước.

### HƯỚNG 3: Tên path/ref và namespace replace khác mặc định

- Giả thuyết: Map và JSON mới có thể đánh mất tên đặc biệt hoặc chỉ tắt refs/replace mặc định.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunt_scanner.py names`
- Output thật:
```text
UTC 2026-09-29T09:55:48.895490+00:00
unusual_paths 1 pair_count 3 paths ['ops/leases/a\tb.yaml', 'ops/leases/a\nb.yml', 'ops/leases/tiếng.yaml'] errors [['ops/leases/a\tb.yaml', 'lease_id=1000'], ['ops/leases/a\nb.yml', 'lease_id=True']]
symbolic_refs 1 refs ['refs/heads/main', 'refs/remotes/origin/alias']
custom_replace 1 [['ops/leases/a.yaml', 'lease_id=1000']]
```
- Kết luận: KHÔNG PHẢI LỖI. NUL ls-tree giữ nguyên path tab/newline/Unicode; chỉ symbolic HEAD bị bỏ; namespace replace tuỳ chỉnh vẫn bị vô hiệu. Không dựng đường thoát cây.

### HƯỚNG 4: Các số mới của r4 và đối chiếu mẫu số độc lập

- Giả thuyết: 512/563/563 có thể là số cũ được chuyển tiếp hoặc hai mẫu số vô tình đồng nhất.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/measure.py`
- Output thật:
```text
UTC 2026-09-29T10:00:01.139324+00:00
checkout rc 0 {'areas': {'ops/leases': {'blobs': 563, 'pairs': 563}, 'ops/leases_retired': {'blobs': 0, 'pairs': 0}}, 'blob_count': 563, 'errors': [], 'id_count_pairs': 563, 'mapping_count_pairs': 563, 'pair_count': 563, 'ref_count': 511, 'type_counts_pairs': {'str': 563}}
mirror rc 0 {'areas': {'ops/leases': {'blobs': 563, 'pairs': 563}, 'ops/leases_retired': {'blobs': 0, 'pairs': 0}}, 'blob_count': 563, 'errors': [], 'id_count_pairs': 563, 'mapping_count_pairs': 563, 'pair_count': 563, 'ref_count': 510, 'type_counts_pairs': {'str': 563}}
independent 511 563 563 {'str': 563} invalid_ID [] blob_hashes_match True
map_compare 510 510 equal True local_heads 1
shallow false core.abbrev 7 replace_count 0
master 89fc4fac8cea65979cc2483043dc8cd07a6e8518
FILE ops/lease_publish.py lines 2206 same_baseline 0
FILE ops/lease_publish_test.py lines 10502 same_baseline 0
old_new_numstat 13	19	ops/lease_publish_test.py
CA 187 max 192
shellcheck ShellCheck - shell script analysis tool | version: 0.9.0 | license: GNU General Public License, version 3 | website: https://www.shellcheck.net
actionlint 1.7.7
ruff 1 /usr/local/bin/python: No module named ruff
```
- Kết luận: KHÔNG PHẢI LỖI số lease trên ảnh cấp. Chênh ref do thành phần local/remote, không lấy tổng trùng để chứng minh nguồn. Map mirror và cache được đối chiếu tên+OID; không đo máy chủ hoặc map lịch sử lúc09:44. Suite chạy độc lập, kết quả bổ sung dưới bảng đo.
### HƯỚNG 5: Bỏ yêu cầu thu hồi T131 có mở hai writer?

- Giả thuyết: depends_on mới dùng hết hạn thay thu hồi có thể không khớp trạng thái thực mà ai-dang-giu tính.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/holders.py`
- Output thật:
```text
UTC 2026-09-29T09:58:15.347189+00:00
entries 563 source=verified mirror (offline seam)
ops/lease_publish.py rc 0 last NGƯỜI_GIỮ 0: không có
T131
ops/lease_publish_test.py rc 0 last NGƯỜI_GIỮ 0: không có
T131
HẾT_HẠN	t131-deadline-dem-spawn-exec-1-claude-20260929	refs/remotes/origin/claude/bookkeeping-676:ops/leases/t131-deadline-dem-spawn-exec-1-claude-20260929.yaml
T131 expiry 2026-09-29T08:15:00Z ref refs/remotes/origin/claude/bookkeeping-676 path ops/leases/t131-deadline-dem-spawn-exec-1-claude-20260929.yaml classification HẾT_HẠN
caller_operational
cay-kho/ops/dung_goi_review.sh:15:#       "`ai-dang-giu` CHI QUET refs/heads/*". DIEU DO SAI. `_cac_ref_cuc_bo`
cay-kho/ops/dung_goi_review.sh:84:#    LY DO DUNG (khong phai "ai-dang-giu chi quet refs/heads" — xem DINH CHINH o dau tep):
```
- Kết luận: KHÔNG PHẢI LỖI trên snapshot. Hạn đã qua, không còn người giữ hai tệp; r4 vẫn bắt đo lại tại cấp lease nên số này không cấp quyền. Phép đo offline thay duy nhất nguồn tên nhánh máy chủ bằng mirror đã so map; không đo live. Q3 thay đổi hành vi từ chối thuộc hai tệp, chưa có bằng chứng đòi sửa caller ngoài write set.

### HƯỚNG 6: Hợp đồng #677 được r4 dẫn mới và L sau D3

- Giả thuyết: Bổ sung nhánh spec #677 có thể khiến r4 hứa giữ một oracle không còn thực hiện được.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/interaction.py`
- Output thật:
```text
UTC 2026-09-29T09:58:16.482120+00:00
SPEC677 81468e21c7a7d32167d210b17813dab2b825992a1587b86d8bc8b3dc9142a4da
null False nen rc 1 GH 0 POST 0 skip False
null False L rc 1 GH 1 POST 0 skip False
null False strict rc 1 GH 0 POST 0 skip False
null False strict_L rc 1 GH 0 POST 0 skip False
true True nen rc 1 GH 1 POST 0 skip False
true True L rc 0 GH 1 POST 0 skip True
true True strict rc 1 GH 0 POST 0 skip False
true True strict_L rc 1 GH 0 POST 0 skip False
1.5 True nen rc 1 GH 1 POST 0 skip False
1.5 True L rc 0 GH 1 POST 0 skip True
1.5 True strict rc 1 GH 0 POST 0 skip False
1.5 True strict_L rc 1 GH 0 POST 0 skip False
2026-09-29 True nen rc 1 GH 1 POST 0 skip False
2026-09-29 True L rc 0 GH 1 POST 0 skip True
2026-09-29 True strict rc 1 GH 0 POST 0 skip False
2026-09-29 True strict_L rc 1 GH 0 POST 0 skip False
'fresh-id' False nen rc 0 GH 4 POST 1 skip False
'fresh-id' False L rc 0 GH 4 POST 1 skip False
'fresh-id' False strict rc 0 GH 4 POST 1 skip False
'fresh-id' False strict_L rc 0 GH 4 POST 1 skip False
yes False nen rc 0 GH 2 POST 0 skip True
yes False L rc 0 GH 1 POST 0 skip True
yes False strict rc 1 GH 0 POST 0 skip False
yes False strict_L rc 1 GH 0 POST 0 skip False
A2 direct mutants: see recheck.log; TinHieuChotCa available at lease_publish_test.py:4674
```
- Kết luận: KHÔNG PHẢI LỖI đã chứng minh. L mất khác biệt ở biên sau chốt độc lập D3 như A2 dự liệu; A2 buộc chuyển phép giết sang D2 trực tiếp, sửa mô tả và oracle kế thừa trong test file. #677 có Q10 khai thứ tự677→678; r4 chưa cấp lease, vẫn nhường điều phối chốt thứ tự theo Q4. Không tự xác minh live/freeze từ tên revision. Mô hình chứng minh khả thi, chưa có catalog ứng viên.

### HƯỚNG 7: Điều kiện dừng mới có giữ được cổng trước cấp lease?

- Giả thuyết: Gỡ Phụ lục A rồi đặt cổng vào helper của lượt thi hành có thể tạo phụ thuộc vòng: phải có lease mới được viết helper nhưng cần helper trước cấp lease.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/contract.py`
- Output thật:
```text
UTC 2026-09-29T09:59:13.686542+00:00
CI gate name_override None matrix {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
CI gate-ops name_override None matrix {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
CI gate-registry name_override None matrix {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
CI gate-packet-loop name_override None matrix {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
THU_HOI thu-hoi jobs ['thu-hoi']
BASE_ANCESTOR_RC 0
POLICY_AT_BASE_RC 128
DIFF_PATHS ['ops/specs/lease-id-ep-kieu-yaml-r1.md', 'ops/specs/lease-id-ep-kieu-yaml-r2.md', 'ops/specs/lease-id-ep-kieu-yaml-r3.md', 'ops/specs/lease-id-ep-kieu-yaml-r4.md']
FIELD schema_version present True
FIELD packet_id present True
FIELD packet_issue present True
FIELD mission_issue present True
FIELD objective present True
FIELD write_set present True
FIELD depends_on present True
FIELD executor present True
FIELD environment present True
FIELD risk present True
FIELD review_class present True
FIELD spec_hash present True
FIELD change_policy_sha present True
FIELD effective_write_set present True
FIELD required_checks present True
FIELD land_obligations present True
FIELD effective_review_class present True
PREVIOUS 1 bo-quet classes ['bo-quet-nghiem-thu-thieu-mien']
PREVIOUS 2 bo-quet classes ['bo-quet-nghiem-thu-thieu-mien', 'bo-quet-chung-cu-khong-neo-anh', 'bo-quet-khong-co-cua-chay']
PREVIOUS 3 bo-quet classes ['bo-quet-chung-cu-khong-neo-anh', 'bo-quet-khong-co-cua-chay']
REFERENCE_CODE_BLOCKS 1
REMOVAL_EDGE 231 - **A9 (quét lại, không đổi lease)** — Trước cấp lease và trước xin land, quét miền bao trùm
REMOVAL_EDGE 252 Đặt helper/self-test mới trong `ops/lease_publish_test.py`; ghi lệnh tái lập trong
REMOVAL_EDGE 280 - **Quét lease** bằng đúng khối mã ở **Phụ lục A** (bản r4, đã áp HINT lượt 3), chạy qua entry
REMOVAL_EDGE 336 một lớp `bo-quet-*`, thì r5 **GỠ mã bộ quét khỏi đặc tả**; §8 hạ số quét xuống "tham khảo,
REMOVAL_EDGE 337 không phải cổng"; cổng là helper A9 có ca kiểm trong `ops/lease_publish_test.py`.
candidate_A9_helper_exists False
```
- Kết luận: KHÔNG PHẢI LỖI độc lập trên đường r4 chưa gỡ; đây là rủi ro thực của phương án gỡ phải xử trong cùng HINT khi điều kiện được kích hoạt. Không được chỉ xoá khối mã và gọi A9 đã đạt. Cần bàn giao dụng cụ kiểm độc lập, có self-test và băm dưới authority chuẩn bị/cấp việc; executor sau khi có lease mới đưa helper vào test file. Đây không là finding P1 độc lập trên đường r4 chưa gỡ. Schema/closure/job names và việc dời nền không cho thấy mâu thuẫn mới trong phạm vi lời khai682.

### HƯỚNG 8: Độ nhạy của chính giàn tự kiểm mới

- Giả thuyết: Một scanner cố ý xoá errors có thể vẫn khiến người đọc tin bảng r4 đã đạt nếu chỉ tin rc script.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/extra_hunts.py rig`
- Output thật:
```text
UTC 2026-09-29T10:08:13.670428+00:00
mutant_script_rc 0 r4_rows 28 explicit_mismatches 14 [('int_yml', '1', '0'), ('thieu_id', '1', '0'), ('khong_anh_xa', '1', '0'), ('yaml_loi', '1', '0'), ('bia_list', '1', '0'), ('ttc_rong', '1', '0'), ('ttc_trang', '1', '0'), ('bia_trang', '1', '0'), ('chi_local', '1', '0'), ('topic_HEAD', '1', '0'), ('replace_commit', '1', '0'), ('khong_replace_commit', '1', '0'), ('replace_blob', '1', '0'), ('yaml_loi_thuong', '1', '0')]
control_rows 28 explicit_mismatches []
positive_controls [('doi_chung', '0', '0'), ('tep_lon_hop_le', '0', '0')]
```
- Kết luận: KHÔNG PHẢI LỖI trong lời khai đã đo của r4: script là giàn in quan sát, không tuyên bố aggregate gate; bảng ghi mong/được phát hiện rõ mutant. rc script đơn lẻ vẫn0, nên không được dùng làm oracle. Reviewer đã so từng dòng gốc; A9 helper tương lai phải chốt kết quả từng ca. Đây là phép thử dụng cụ chứng nhận, không thêm finding chỉ vì script báo cáo không tự exit1.

### HƯỚNG 9: Khử trùng khi cùng đường có nhiều phiên bản và blob dùng lại

- Giả thuyết: Cấu trúc mới có thể đếm theo ref hoặc blob thay vì cặp trong đồ thị nhiều bản của cùng path.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/extra_hunts.py aggregation`
- Output thật:
```text
UTC 2026-09-29T10:08:17.899895+00:00
rc 1 counts {'ref_count': 3, 'blob_count': 2, 'pair_count': 5, 'mapping_count_pairs': 5, 'id_count_pairs': 5, 'type_counts_pairs': {'int': 2, 'str': 3}, 'areas': {'ops/leases': {'blobs': 2, 'pairs': 3}, 'ops/leases_retired': {'blobs': 2, 'pairs': 2}}}
errors [['ops/leases/a.yaml', 'lease_id=1000'], ['ops/leases_retired/z.yaml', 'lease_id=1000']]
pairs [('ops/leases/a.yaml', 2), ('ops/leases/b.yml', 3), ('ops/leases_retired/a.yaml', 3), ('ops/leases_retired/z.yaml', 2), ('ops/leases/a.yaml', 1)]
expected_all True
```
- Kết luận: KHÔNG PHẢI LỖI. Khử trùng đúng theo cặp, giữ các ref và tách live/retired; mỗi bản sai trong một cặp có lỗi. Không suy lỗi cần gắn ref duy nhất: một cặp có thể xuất hiện trên nhiều ref.

### HƯỚNG 10: Lease chỉ ở HEAD detached hoặc tag có thuộc miền phải quét?

- Giả thuyết: Checkout r4 detached có thể làm khẳng định mọi lease rộng hơn miền mà runtime đọc.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/extra_hunts.py roots`
- Output thật:
```text
UTC 2026-09-29T10:08:18.093591+00:00
detached_only rc 0 ref_count 1 errors [] runtime_types ['str'] map_has_detached False
name_remote_other rc 1 ref_count 2 errors [['ops/leases/a.yaml', 'lease_id=1000']] map_has_detached True
tag_only rc 0 ref_count 1 errors []
```
- Kết luận: KHÔNG PHẢI LỖI. A9 nêu rõ miền heads/remotes, không hứa duyệt mọi object/tag/detached HEAD; runtime cùng giới hạn. Khi đặt đúng commit vào remote khác origin, scanner lập tức báo lỗi. Không yêu cầu mở rộng miền ngoài hợp đồng hoặc biến cache object thành lease hiện hành.
### KIỂM BỔ SUNG: A1–A10, mọi đường danh tính và Q1

- Giả thuyết: Đo lại các scalar/collision và độ độc lập D1/D3/D4/D8; không tính là hướng mới vì hợp đồng này kế thừa r3.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`
- Output thật:
```text
UTC 2026-09-29T10:00:02.294233+00:00
SCALAR true bool 'True' D2 8 D1 0 strict 8
SCALAR yes bool 'True' D2 8 D1 0 strict 8
SCALAR on bool 'True' D2 8 D1 0 strict 8
SCALAR True bool 'True' D2 8 D1 0 strict 8
SCALAR 1.5 float '1.5' D2 8 D1 0 strict 8
SCALAR 1.50 float '1.5' D2 8 D1 0 strict 8
SCALAR 0x1F int '31' D2 RETURN D1 0 strict 8
SCALAR 017 int '15' D2 RETURN D1 0 strict 8
SCALAR 1_000 int '1000' D2 RETURN D1 0 strict 8
SCALAR 5 int '5' D2 RETURN D1 0 strict 8
SCALAR 2026-09-29 date '2026-09-29' D2 8 D1 0 strict 8
SCALAR 'yes' str 'yes' D2 RETURN D1 0 strict 0
COLLISION True yes base 9 strict 8
COLLISION True on base 9 strict 8
COLLISION 1.5 1.50 base 9 strict 8
COLLISION 31 0x1F base 9 strict 8
COLLISION 15 017 base 9 strict 8
COLLISION 1000 1_000 base 9 strict 8
COLLISION khac-lease yes base RETURN strict 8
BODY strict= 8 base_marker True
D8 lpbase check_rc 0 holder_rc 0 reached [('check', 'int'), ('holder', 'int')]
D8 lpmodel check_rc 8 holder_rc 0 reached [('holder', 'int')]
Q1 '" a"' value ' a' allowed False
Q1 '"a "' value 'a ' allowed False
Q1 '"a\\n"' value 'a\n' allowed False
Q1 'é' value 'é' allowed False
Q1 'é' value 'é' allowed False
Q1 'Ａ' value 'Ａ' allowed False
Q1 'A' value 'A' allowed True
Q1 'a' value 'a' allowed True
Q1 '!!str 1.5' value '1.5' allowed True
Q1 'lease_id: yes\nlease_id: fresh' value 'fresh' allowed True
IDENTITY_INVENTORY_LINES 61
```
- Kết luận: KHÔNG PHẢI LỖI mới. A1/A3/A4 có đại lượng phân biệt; D8 check được D1 che, ai-dang-giu vẫn tới; Q1 loại Unicode/trắng và cố ý nhận tagged string/cùng giá trị cuối. Đã đọc flow và inventory, không tìm đường quyết định lease_id thiếu ngoài D1–D8; D9 hiển thị và sổ thu hồi có chốt riêng. Mô hình không thay nghiệm thu ứng viên.



## BẢNG ĐO

Các số hiện tại dưới đây đo bởi `goi/measure.py` (UTC trong `goi/measure.log`); runtime bởi `goi/runtime.py`; các dòng D1–D9 bởi `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho|\.stem|name\[:-5\]' cay-kho/ops/lease_publish.py` và đọc luồng. Không dùng số bằng nhau thay bằng chứng cùng snapshot.

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| Định danh r4 | sha2562726d59f… / head a9019a9… | lệnh đầu khớp đầy đủ; blob repo = SPEC.md | Có |
| §1 bool true/yes/on/True | bool/True; D2=8; D1 qua | từng giá trị đúng; mô hình D1 mới8 | Có |
| §1 float1.5/1.50 | float/1.5; D2=8; D1 qua | đúng từng số hạng | Có |
| §1 hex/octal/separator | int31/15/1000; D2/D1 qua | đúng; A1 thêm5 cũng qua nền/strict8 | Có |
| §1 date | date2026-09-29; D2=8/D1 qua | đúng | Có |
| §1 quoted yes | str/yes; cả hai qua | đúng; mô hình vẫn qua | Có |
| §1 sáu cặp va chạm + đối chứng | 6×rc9; đối chứngrc0 | mỗi cặp9; khác tên RETURN(0) | Có |
| §1/A3 workflow | yes rc0/POST0; fresh rc0/POST1 | đúng; mô hình strict yes1/0; fresh0/1 | Có |
| §2 D1/D2/D3/D4 |861/949/668/1070 | inventory đúng | Có |
| §2 D5/D6 |587/592 và609/612 | đọc đúng các toán hạng; mutant mỗi vế có khác biệt | Có |
| §2 D7 |2110/2123 | đọc/lập khoá đúng | Có |
| §2 D8 |1938/1942/1946/1967 | raw/raw/f-string/str đúng | Có |
| §2 D9 |2074/2089/2139/2143 | chỉ hiển thị; các chốt trước không bị gán nhầm | Có |
| §2 sổ thu hồi/packet_loop |1192 và769–771 đã đòi str | đã đọc chốt str/regex/tên; packet_loop loop/guard đúng | Có |
| §2 workflow |0 dòng đọc lease_id | `rg -n lease_id cay-kho/.github/workflows/*.yml`: rc1/không output | Có |
| Nền/header |89fc4fa; sản phẩm không đổi; test+13/−19/bốn hunk | master89fc4fa; diff sản phẩm0; test13/19; t131×2/t139/t192 | Có |
| §8 shallow/replace |false/0 |false/0 | Có trên snapshot |
| §8 remote tên |510=510; thiếu/thừa0 |cache origin510=mirror heads510; tên+OID đều bằng | Có trên ảnh cấp; máy chủ/lịch sử KHÔNG ĐO ĐƯỢC |
| Prompt số nhánh clone |505 |510, khớp mirror510 | Prompt trôi số; hai định danh bắt buộc vẫn đúng |
| §8 tổng ref |512=510 remote+2 local |checkout511=510+1; mirror510 heads | Khác thành phần local; không bác mốc09:44 |
| §8 blob/cặp/ánh xạ/có ID |563/563/563/563 |563/563/563/563, cả scanner và phép độc lập | Có |
| §8 kiểu/lỗi |str563/errors0 |str563/errors0; băm mọi blob đã đọc khớp | Có trên ảnh cấp |
| §8 live/retired |563/563 và0/0 |đúng từng miền | Có |
| §8 chênh r3→r4 |ref+4/blob+1 |chỉ có map ảnh hiện tại; thiếu map gốc hai mốc | KHÔNG ĐO ĐƯỢC từng ref/blob tăng theo lịch sử |
| §8 số559/560/562 và503/505/506 lịch sử |nhãn thời điểm cũ |không có map của từng thời điểm | KHÔNG ĐO ĐƯỢC; không lấy ảnh mới bác số cũ |
| §8 người giữ |0/0; T131 HẾT_HẠN08:15Z |0/0, rc0; cùng lease/hạn/nhãn | Có offline; chưa đo live |
| §8 số dòng |2206/10502 (test cũ10508) |2206/10502; diff−6, blob cũ10508 | Có |
| §8 số ca/max |187/t192 |len(CA)=187/max192 | Có |
| §8/A8 suite |187/187, rc0/bỏ0 |187/187, rc0/bỏ0; shellcheck0.9.0/actionlint1.7.7 | Có |
| §8/A8 lịch sử185/187 |thiếu shellcheck t137/t159 |môi trường này đủ công cụ; không có log cũ | Không bác lời khai lịch sử |
| Ruff |KHÔNG ĐO ĐƯỢC |python -m ruff --version rc1/No module named ruff | Bare lint/delta: chưa đo |
| §9 hình dạng |bo-quet có ở3 lượt trước |recheck/contract.py liệt kê đúng các slug của cả3 | Có; lượt này thêm biểu hiện cùng lớp |
| Phụ lục CLI/race |28 r4+2 đối chứngr3; race riêng |đếm log:28+2, mọi rc khớp bảng; race True | Có trong phạm vi ca đã chạy |
| CLI lỗi mới |0/1/2 phân loại |unknown tag/NUL→1; !!int/ngày giờ/UTF16→2; note lớn1000022bytes→0 | Có ở nhánh thử; không suy hết tài nguyên |

Suite đã chạy từ R: `review_scratch=$(cat goi/scratch-path); PYTHONDONTWRITEBYTECODE=1 TMPDIR="$review_scratch" python cay-kho/ops/lease_publish_test.py > goi/suite.log 2>&1`. Test tìm tài nguyên bằng HERE, hai tệp Python của reviewed_sha bằng base_sha nên đây chính là suite nền, không có candidate implementation để khai delta. Output cuối: `lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0`, `suite_rc=0`.

### Khả năng đỏ A1–A10

| tiêu chí | căn cứ phân biệt/chốt che | giới hạn |
|---|---|---|
| A1 |runtime.py đọc YAML qua _doc_yaml; D1 nền0/strict8, quoted yes0 |kiem không tep và bỏ hạn để D6/neo/hạn không che |
| A2 |recheck.py direct D2 strict8→restore/L RETURN; probe vẫn GH0 |không nhận GH0 là phép giết D2 |
| A3 |interaction.py trích workflow thật, gh giữ trạng thái trên PATH; yes0/0→1/0, fresh0/1; direct D3 9→8 |không dùng workflow qua D1 để chứng minh mutant D3 |
| A4 |runtime.py direct body bool cho marker ở nền, strict8 |chưa có mutant catalog ứng viên |
| A5 |recheck.py kho Git thật; từng D5_self/peer False→True; D6_self/peer8→RETURN; đối chứng chuỗi qua |không hoàn nguyên cả hàm để đại diện từng toán hạng |
| A6 |fixture hai ref/path nền rc11/NGƯỜI_GIỮ1:True; spec buộc nhãn và cả ref/path |mới chứng minh oracle tách nền; chưa có D7 candidate |
| A7 |main CLI được instrument riêng: D1 chặn check, holder vẫn tới D8 với int |D8 helper được thay bằng quan sát, chỉ chứng minh reachability; không khai đã giết mutant D8 |
| A8 |nền đủ187/187; tiêu chí delta có thể đỏ khi thêm ca đỏ/F |candidate và Ruff chưa có/chưa đo |
| A9 |tự kiểm cũ qua; phản chứng object cho thấy bằng chứng vẫn có âm giả |finding P2; số snapshot sạch không đóng lỗi dụng cụ |
| A10 |TinHieuChotCa/chot ở4674/4699 có sẵn; strict helper cho giá trị oracle phân biệt |chưa có catalog A1–A7 thật, không xác nhận target/cause matrix đã đạt |

Fixture khả thi trong write set: `_buoc_workflow`555, `GhGia`193, `_kho_thu`1506, `_git_fixture`3746, `_kho_do_thi`4730. `_chay_buoc_dang`2703 dùng stub nên riêng nó chưa đủ A3; interaction.py đã dùng bộ trích thật + Python thật + executable gh giữ trạng thái. Đã đọc mã không chỉ tìm tên helper.

### Phần r4 ngoài HINT lượt3

Đã áp HINT cũ trên bản r3 riêng (`PREVIOUS_HINT 0`) rồi so nội dung r4, lưu `goi/beyond-hint.diff`; đã đọc cả `r3-r4.diff`. Header giữ nền/closure; depends_on hết hạn đo đúng ở hướng5. A2 mới dẫn đúng hash/path spec677 (hướng6), chưa tự cấp thứ tự/lease. §8 số mới đo ở hướng4; các số lịch sử không được chứng nhận live. §9 đếm đúng lịch sử nhưng điều kiện gỡ cần giữ cổng trước cấp (hướng7). §10 và hai bảng tự kiểm đúng phạm vi CLI/seam; không mở P3 vì khẳng định chưa đo những thứ thật sự chưa đo.

Closure đủ trường trong bytes; descriptor682/5627190292 và ngoại lệ được kiểm như lời khai điều phối theo prompt, không lấy OWNER làm bằng chứng người gõ. Tiền lệ wp461/#470 chỉ cho thấy cách mô tả ngoại lệ, không tự cấp authority cho wp678. `required_checks` khớp tên job/matrix Ubuntu và workflow/job thu-hoi; chưa chứng minh CI live đã chạy. Nghĩa vụ ghi sổ/thu hồi/audit là vai land, không bắt executor viết ngoài hai tệp. Baseline mới là tổ tiên của candidate; không có product diff bị che bởi việc dời nền.

## CHI TIẾT TỪNG LỚP

### bo-quet-chung-cu-khong-neo-anh [P2] Cat-file thành công chưa chứng minh bytes blob mang OID đã báo

VỊ TRÍ: SPEC.md :367–372 (ảnh OID gốc), :402–404 (đọc blob), :429 (báo errors); A9 :238–242; điều kiện dừng :335–337.

VẤN ĐỀ: ref_map và pairs có OID nhưng blob đi thẳng từ `git cat-file blob <OID>` vào safe_load. Git có thể trả rc0 khi nội dung giải nén của loose blob không mang hash ghi ở đường object. Bộ quét vì thế báo cùng ref/OID của lease int, trong khi đã kiểm nội dung lease chuỗi khác. JSON hoàn chỉnh, errors=[] và rc0 nên đây là âm giả của chứng cứ, khác các lỗi CLI r3 đã sửa.

Phạm vi phản chứng rất cụ thể: reviewer làm hỏng object-store trong kho Git tạm, không tạo SHA collision, không sửa repo nguồn, không giả gh/Git executable và không dựng đường thoát cây. Đường YAML/ref thông thường không tạo được trạng thái này; cần lỗi/hỏng nguồn object. Tuy vậy hợp đồng hiện tại tuyên bố chứng minh ảnh OID gốc và chưa yêu cầu kiểm toàn vẹn nguồn/blob trước khi tin cat-file. Không suy từ một Git command thành công rằng đã kiểm hash: đối chứng cùng cơ chế trên commit/tree thực trả2, còn blob trả0. Đây là P2 về công cụ chứng cứ, không là lỗ quyền của sản phẩm và không nâng thành P1.

ĐÃ THỬ:

- `PYTHONDONTWRITEBYTECODE=1 python goi/hunt_scanner.py objects`: kho int rc1; thay bytes loose blob dưới cùng OID bằng YAML chuỗi hợp lệ → rc0/JSON/errors=[]/same_map=True; `git fsck --full` rc3 báo hash-path mismatch. Thiếu blob → rc2/không JSON.
- `PYTHONDONTWRITEBYTECODE=1 python goi/object_confirm.py`: xác nhận lại và khôi phục đối chứng trên từng lớp. Output:

```text
UTC 2026-09-29T10:01:48.163162+00:00
blob baseline_rc 1 corrupt_rc 0 same_refs True errors [] fsck_rc 3 hash_mismatch True
blob restored_rc 1 restored_errors [['ops/leases/a.yaml', 'lease_id=1000']] fsck_rc 0
tree baseline_rc 1 corrupt_rc 2 same_refs None errors KHONG_DO_DUOC: KhongDoDuoc: git ls-tree -r -z e049659e49be06f169763fcfaf507afa55cb5ad0 -- ops/leases/ ops/leases_retired/ rc=128: error: hash mismatch b63c7e9ae fsck_rc 3 hash_mismatch True
tree restored_rc 1 restored_errors [['ops/leases/a.yaml', 'lease_id=1000']] fsck_rc 0
commit baseline_rc 1 corrupt_rc 2 same_refs None errors KHONG_DO_DUOC: KhongDoDuoc: git ls-tree -r -z e049659e49be06f169763fcfaf507afa55cb5ad0 -- ops/leases/ ops/leases_retired/ rc=128: error: hash mismatch e049659e4 fsck_rc 3 hash_mismatch True
commit restored_rc 1 restored_errors [['ops/leases/a.yaml', 'lease_id=1000']] fsck_rc 0

```

Không gọi `git fsck` thành cơ chế nguyên tử chống writer đồng thời. Cách chữa ở A9 là ràng buộc OID với chính bytes đưa vào parser (hoặc chứng minh nguồn đã xác minh và bất biến trong suốt phép đo), tránh kiểm một ảnh rồi dùng ảnh khác. Hướng4 tự băm blob snapshot hiện tại đều khớp; không cáo buộc kho thật có object hỏng.

HINT: có — nhóm `# lop: bo-quet-chung-cu-khong-neo-anh`, chỉ nhắm r4. Theo stop condition đã đăng ký, không vá thêm scanner tham chiếu: gỡ khối Python, chuyển số/tự kiểm cũ sang hồ sơ lịch sử, giữ nghĩa vụ provenance và self-test trong A9. Việc gỡ **không tự chữa** một helper chưa viết và không được đổi nhãn lớp thành đã đóng chỉ vì không còn code.

Hệ quả cần xử cùng HINT: nếu chỉ gỡ code rồi nói “cổng là helper test file”, A9 trước cấp lease phụ thuộc vào mã mà executor chưa có quyền viết. HINT tách trách nhiệm: bên cấp việc chuẩn bị dụng cụ độc lập có source/băm/self-test/output trước cấp; executor sau cấp mới đặt helper trong test file và chạy lại trước land. Chưa có dụng cụ đủ chuẩn thì DỪNG cấp, không lấy §8 tham khảo thay nghiệm thu. Không cấp thêm write set cho executor, không đòi sửa sản phẩm ngoài hai tệp.

ĐỘ TIN: cao về âm giả đã tái hiện và cơ chế; giới hạn là object-store hỏng dựng chủ ý. Chưa có dụng cụ A9 mới hoặc candidate để tuyên bố đã đóng lớp. Không phát hiện thêm lớp P1/P2/P3 từ các hướng còn lại.

## DRY-RUN HINT.patch

Nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Đây là gợi ý sửa ĐẶC TẢ r4 để điều phối soạn r5; r1–r3 bất khả xâm phạm, không có patch mã sản phẩm. Source/spec hiện tại chưa bị sửa.

Lệnh đã chạy (R là đường tuyệt đối trong prompt):

```sh
PYTHONDONTWRITEBYTECODE=1 python goi/build_hint.py
review_hint_tmp=$(mktemp -d -p "$R")
cp -a "$R/cay-kho" "$review_hint_tmp/cay"
patch -d "$review_hint_tmp/cay" -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```

Output nguyên văn (`goi/hint-dry-run.log`):

```text
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: bo-quet-chung-cu-khong-neo-anh
|--- ops/specs/lease-id-ep-kieu-yaml-r4.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r4.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r4.md
Using Plan A...
Hunk #1 succeeded at 241.
Hunk #2 succeeded at 253.
Hunk #3 succeeded at 292.
Hunk #4 succeeded at 336.
Hunk #5 succeeded at 352.
Hunk #6 succeeded at 371.
Hunk #7 succeeded at 401.
Hunk #8 succeeded at 424.
done
dry_run_rc=0

```

Áp thật tiếp trên cùng BẢN SAO rồi cmp với `goi/hint-expected.md`:

```text
patching file ops/specs/lease-id-ep-kieu-yaml-r4.md
apply_rc=0
expected_cmp_rc=0

```

Không dùng riêng dry-run xanh làm bằng chứng vị trí đúng. Sau áp, chỉ r4 có diff; khối Python tham chiếu đã vắng, A1–A10 và hai đường write set vẫn có. Dụng cụ A9 mới chưa triển khai nên không khai đã chạy nó.


## TOÀN VẸN VÀ GIỚI HẠN CUỐI

`PYTHONDONTWRITEBYTECODE=1 python goi/verify.py` kiểm source snapshot trước/sau, blob spec, exact HEAD/tree, nhóm HINT, phạm vi diff trên bản sao và kết quả suite. Output:

```text
source_files_before 3012 after 3012 delta []
HEAD a9019a911a4fe2770ede5abafebc41afbd97aa16
tree 61de3c55d7c256fecc242a01fd20b12297241e62
r1 578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c
r2 1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715
r3 64c67225335cf50b2a394ffda005e03d338ff545757b210640fd05ac14564af1
r4 2726d59ffb683f44e68c1409241250c40025bc02a9c9bfb257e767831a1e17f2
class_headings [('bo-quet-chung-cu-khong-neo-anh', 'P2')]
hunt_headings ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
r4_CLI_cases 28 explicit_mismatches [] r3_controls 2
hint_changed ops/specs/lease-id-ep-kieu-yaml-r4.md
applied_expected_match True python_blocks 0
suite_rc=0
lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0
VERIFIED

```

Snapshot băm cả regular files của checkout/mirror, gồm tracked, untracked, ignored và Git metadata. Không có delta quan sát được ở hai mốc; không suy thành audit mọi syscall của cả phiên. Sandbox thực là workspace-write; chỉ thị read-only được giữ bằng giới hạn đường ghi, không tự khai mount read-only. Mọi script/fixture/mô hình nằm ở goi hoặc mktemp dưới R; không dùng mạng, không sửa checkout/mirror, không đăng GitHub.

Lỗi dụng cụ review đã sửa rồi chạy lại: helper Git độc lập `.strip()` làm mất ô symref cuối; fixture loose object chỉ đọc cần thay tệp fixture trước ghi; ca kiểm đối chứng object ban đầu giả định cả tree/commit cũng trả JSON, đã sửa để ghi nhận chính kết quả rc2/không JSON. Các lỗi thiết lập ấy không tính finding; các log cuối và lệnh tái lập ở trên là kết quả sau sửa.

Chưa đo: GitHub live, bytes thân Issue682, candidate implementation, Windows, bare Ruff/delta F, OOM/OS kill/timeout và dụng cụ A9 tương lai. Không làm tròn “chưa đo” thành “không có”. Closure được review theo lời khai có phạm vi của prompt; descriptor không tự chứng minh người ký hay trạng thái live. Verdict này là review đặc tả, không cấp lease, approval, merge hoặc land authority.

Băm hai hiện vật bàn giao được ghi ngoài chúng tại `goi/artifact-hashes.txt`; không nhúng băm tự tham chiếu vào verdict.
