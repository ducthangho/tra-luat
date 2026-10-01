verdict: changes_requested
reviewed_sha: 00d2ee3e911fbc0ef1978a19eab3da91580f3fa6
spec_sha256: cbf9c8380f0da45e2af07034cc6715b75c8ac2deb36a4967497b94d1a9394150
model/effort tự khai: GPT-6 (Codex), không có metadata xác nhận mức effort trong phiên.

## KIỂM ĐỊNH DANH
Lệnh: `sha256sum SPEC.md && git -C cay-kho rev-parse HEAD`
Output:
```
cbf9c8380f0da45e2af07034cc6715b75c8ac2deb36a4967497b94d1a9394150  SPEC.md
00d2ee3e911fbc0ef1978a19eab3da91580f3fa6
```
Khớp; tiếp tục review độc lập, offline.

provider: openai_codex
execution_surface: API agent có công cụ shell cục bộ
transport: machine; bàn giao tệp, không đăng GitHub
assurance: review nội dung độc lập; không tự cấp lease/approval/land authority; exact served model/effort theo máy KHÔNG ĐO ĐƯỢC.

## ĐỐI CHIẾU LƯỢT TRƯỚC
Đã làm trước các hướng săn mới. Lệnh `PYTHONDONTWRITEBYTECODE=1 python goi/precheck.py`; output đầy đủ `goi/precheck.log`. Mô hình chốt chỉ ở thư mục mktemp dưới R, không phải ứng viên.

| lớp lượt 1–4 | trạng thái | bằng chứng |
|---|---|---|
| bo-quet-chung-cu-khong-neo-anh | **CHUYỂN GIAO CHƯA ĐỦ / CÒN MỞ** (cập nhật sau hướng 1) | A9:261–268 giữ map/OID, tắt mọi replace, thêm băm Git blob theo object format trên cùng biến bytes đọc một lần; :290–304 có replace/race/object-store; §9:410 nói chưa đóng. `PYTHON_BLOCKS 0`. Chưa có helper để chứng nhận đóng; hướng 1 chứng minh phần tree con chưa được chuyển đủ. |
| bo-quet-nghiem-thu-thieu-mien | **TÁI PHÁT khi chuyển giao** (cập nhật sau hướng 4) | A9:251–260,285–289 giữ heads/remotes, HEAD thường, yaml/yml, retired, mapping/ID/schema con trỏ; empty list đối chứng. Tự dựng kho khác: `R2_CLI 0 stdout '' stderr ''`, `R2_CALL (1, 1, 1, [])` với `thay_the_cho: ["   "]`; A9 buộc ca ấy rc1, nhưng mất ngoại lệ null/chuỗi rỗng hợp lệ (hướng 4). |
| bo-quet-khong-co-cua-chay | **CHUYỂN GIAO** các biểu hiện đã đóng ở mã r4 | A9:275–299 bảo toàn phân loại 0/1/2, JSON dương, ngoại lệ chưa phân loại, ca đi qua đúng biên; CLI argv chỉ áp khi helper có CLI. §10 khai helper chưa tồn tại. |
| tieu-chi-dot-bien-khong-phan-biet-chot | **ĐÃ ĐÓNG** trong hợp đồng | A2 đo D2 trực tiếp; A5 từng toán hạng. Mô hình: `D2 RETURN 8`; `D5_self strict False mutant True`; `D5_peer strict False mutant True`; `D6_self strict 8 mutant RETURN`; `D6_peer strict 8 mutant RETURN`. |
| so-do-nen-khong-khop | **ĐÃ ĐÓNG** biểu hiện A6/số lịch sử; đo số hiện tại bổ sung riêng | A6 chốt nhãn/ref/path, khai nền rc11; A8/§8 tách lịch sử 185/187 khỏi 187/187, ghi thời điểm/phạm vi. Không lấy số snapshot hiện tại bác mốc lịch sử. |
| hop-dong-dong-bang-thieu-neo | **ĐÃ ĐÓNG** trong phạm vi lời khai được giao | Mission682/object5627190292, closure nằm trong bytes; `CLOSURE_HASH_CHANGES True`; miễn trừ có phạm vi và thời hạn. Không cần đo live. |
| objective-dong-nhat-cu-phap-voi-danh-tinh | **ĐÃ ĐÓNG** | `Q1_EQUAL 'yes' !!str yes True`; `Q1_EQUAL '1.5' !!str 1.5 True`; objective nhận cùng chuỗi sau safe_load là cùng danh tính. |
| bang-duong-phan-loai-sai | **ĐÃ ĐÓNG** các biểu hiện trước | D7/D8/D9 giữ phân loại đã sửa; header ghi hunk t131×2/t139/t192; Phụ lục tách CLI và race seam, đều gắn nhãn lịch sử. |
| trang-thai-q3-chua-dong-bo | **ĐÃ ĐÓNG** | Q3:115 ghi đã xác nhận; §10 ghi không còn là câu hỏi mở; nguồn authority là prompt và lời khai682. |

Q7 được giữ nguyên: chỉ A9 trước land; không đề xuất phục hồi cổng trước cấp lease. CHUYỂN GIAO là kết luận về đủ/đúng nghĩa vụ đặc tả, không là pass cho helper chưa viết. Các lớp sẽ được cập nhật nếu hướng săn sau phát hiện tái phát.

## BẢNG LỚP

Kết luận nội dung: **0 P1 / 2 P2 / 0 P3**; `changes_requested`. Đếm theo lớp, không nhân lớp theo loose/packed hoặc theo từng giá trị con trỏ. Ngưỡng được giao: chỉ approve khi không còn P1/P2/P3. Đây là review đặc tả; không chấm điểm một helper chưa tồn tại.

| slug lớp | hạng | biểu hiện (vị trí trong SPEC) | phương án chung | phép kiểm / giới hạn |
|---|---|---|---|---|
| bo-quet-chung-cu-khong-neo-anh | P2 | A9:264–268 chỉ băm blob; :302–303 tin Git tự từ chối tree/commit hỏng; Phụ lục:542–548 dễ bị đọc rộng từ fixture tree gốc | Băm toàn chuỗi commit/tree gốc/tree con/blob; lấy cạnh từ chính bytes đã băm; ca tree con loose/packed | `tree_probe.py`: tree con sai băm vẫn ls-tree0, blob hash đúng, ID str; mô hình toàn chuỗi trả2; khôi phục trả1. Không cáo buộc nguồn thật hỏng. |
| bo-quet-nghiem-thu-thieu-mien | P2 | A9:258–260 thay mã cũ bằng miền con trỏ thiếu None/chuỗi rỗng; danh mục :286–289 thiếu đối chứng miền không-con-trỏ | Bảo toàn schema tuỳ chọn và ngoại lệ vắng/null/chuỗi rỗng, thêm ca dương riêng | `pointer_transfer.py`: null ở hai trường, chuỗi rỗng ở da_bi_thay_the được runtime/r4 nhận, prose r5 đọc đúng từng chữ có thể bác. Snapshot hiện không có các giá trị này. |

Rủi ro quyết định Q7 có phản chứng ở hướng 6, được ghi riêng **không xếp hạng**, không tính vào các lớp P2 và không yêu cầu khôi phục cổng trước cấp lease.

## BẢNG SĂN

Các hướng độc lập được tính là 1–6: cạnh tree con trong đồ thị object; chuẩn hoá bytes do I/O/attributes; encoding tự nhận dạng; phần bù schema hợp lệ sau gỡ mã; ưu tiên khi một ảnh mang hai loại lỗi; cửa sổ Q7 với bia mộ ép kiểu. Mỗi hướng thay một giả thuyết khác trên phần hợp đồng A9/Q7 r5. Đối chiếu lượt trước, đo số nền, SHA-1/SHA-256, đọc một lần và kiểm A1–A10 bên dưới là phần bắt buộc bổ sung, không dùng chúng để nâng số hướng.

### HƯỚNG 1: Đổi tầng lưu object, giữ đúng phép băm blob mới của r5
- Giả thuyết: băm blob đúng vẫn không neo được cạnh tree→blob nếu Git trả thành công cho tree có nội dung sai OID.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/object_probe.py` (log `goi/object_probe.log`).
- Output thật:
```
tree ls_tree_rc 0 cat_file_rc 0 object_hash_match False pairs [('ops/leases/a.yaml', True, 'str')] fsck_rc 12 map_unchanged True
commit ls_tree_rc 128 cat_file_rc 0 object_hash_match False pairs [] fsck_rc 6 map_unchanged True
blob ls_tree_rc 0 cat_file_rc 0 object_hash_match False pairs [('ops/leases/a.yaml', False, 'str')] fsck_rc 4 map_unchanged True
```
- Kết luận: **LỖI**, lớp `bo-quet-chung-cu-khong-neo-anh` P2. Đây là phép đổi tầng lưu (packed tree) và phép kiểm cạnh có trước blob, khác ca blob sai băm của lượt 4. Băm blob mới đóng đúng blob sai; tree sai vẫn trỏ tới blob khác hoàn toàn nguyên vẹn. Git thực trả rc0, không stderr. Đang kiểm thêm loose/nested/root để chốt phạm vi; không cáo buộc kho nguồn hỏng.

### HƯỚNG 2: Bộ lọc Git và chuyển newline có đổi bytes dưới cùng nội dung YAML?
- Giả thuyết: Một helper dùng text=True hoặc hash-object --path có thể băm nội dung đã chuẩn hoá thay cho object gốc.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py bytes`.
- Output thật:
```text
UTC 2026-09-29T10:31:46.716599+00:00
crlf raw_hash_match True text_roundtrip_match False parsed_equal True
bom raw_hash_match True text_roundtrip_match True parsed_equal True
utf8 raw_hash_match True text_roundtrip_match True parsed_equal True
attributes_path_filter_changes_oid True
```
- Kết luận: KHÔNG PHẢI LỖI của hợp đồng: A9 đòi CHÍNH bytes; phép đo cho thấy cần binary I/O, không hash văn bản tái mã hoá hay áp attributes. CRLF và LF parse cùng nghĩa nhưng OID khác; BOM/Unicode là đối chứng. Đây là trục cấu hình/chuẩn hoá dữ liệu, không phải kiểm lại sai băm tĩnh của lượt 4.

### HƯỚNG 3: Tự nhận dạng encoding khi chuyển từ text sang bytes
- Giả thuyết: safe_load(bytes) có thể nhận UTF-16 dù runtime UTF-8 từ chối, sau khi r5 yêu cầu cùng biến bytes.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py encoding`.
- Output thật:
```text
UTC 2026-09-29T10:31:46.976341+00:00
utf8 bytes_safe_load str strict_utf8 ok
utf16 bytes_safe_load str strict_utf8 UnicodeDecodeError
invalid_utf8 bytes_safe_load ReaderError strict_utf8 UnicodeDecodeError
SPEC_UTF8_LINE [296, 499]
```
- Kết luận: KHÔNG PHẢI LỖI của hợp đồng: A9:296 vẫn bắt blob không UTF-8 ra2. Executor có thể kiểm decode UTF-8 trên cùng buffer trước safe_load(buffer), không đọc lại nguồn. Nếu bỏ chốt encoding thì UTF-16 là ca phân biệt; chưa có helper để xác nhận cài đặt.

### HƯỚNG 4: Schema con trỏ sau khi nguồn định nghĩa bằng mã bị gỡ
- Giả thuyết: Prose A9 mới có thể bỏ mất các giá trị biểu diễn không có con trỏ đã được runtime và mã r4 chấp nhận.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py pointers`.
- Output thật:
```text
UTC 2026-09-29T10:31:47.161757+00:00
thay_the_cho None runtime [] legacy_errors []
thay_the_cho '' runtime [] legacy_errors []
thay_the_cho [] runtime [] legacy_errors []
thay_the_cho [''] runtime None legacy_errors [('ops/leases/a.yaml', 'thay_the_cho')]
thay_the_cho ['   '] runtime None legacy_errors [('ops/leases/a.yaml', 'thay_the_cho')]
thay_the_cho '   ' runtime [] legacy_errors []
thay_the_cho False runtime None legacy_errors [('ops/leases/a.yaml', 'thay_the_cho')]
thay_the_cho 0 runtime None legacy_errors [('ops/leases/a.yaml', 'thay_the_cho')]
SPEC_pointer `thay_the_cho` là chuỗi hoặc danh sách chuỗi không trắng; `da_bi_thay_the` là
  chuỗi không trắng; không dùng chung phép chấp nhận list cho cả hai. Không biến việc kiểm schema thành
  yêu cầu mọi bia mộ lịch sử đều còn cặp đối xứng trên cùng ref. Chỉ đo, không sửa lease cũ.
```
- Kết luận: LỖI: chuyển giao miền schema chưa đủ; xem phép so literal-r5 với r4/runtime trong goi/pointer_transfer.log và lớp bo-quet-nghiem-thu-thieu-mien. Không đòi đối xứng bia mộ lịch sử, không đổi Q1.

### HƯỚNG 5: Một ảnh vừa lỗi YAML vừa lỗi toàn vẹn object
- Giả thuyết: Một lỗi lease có thể che lỗi không đo được ở object sau, làm mã1 bị hiểu là quét đầy đủ.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py precedence`.
- Output thật:
```text
UTC 2026-09-29T10:31:47.599069+00:00
order ('ops/leases/parse.yaml', 'ops/leases/hash.yaml') rc_json (2, False)
order ('ops/leases/hash.yaml', 'ops/leases/parse.yaml') rc_json (2, False)
```
- Kết luận: KHÔNG PHẢI LỖI của hợp đồng: A9 đòi JSON đầy đủ cho1 và sai băm→2; mô hình biên giữ2 ở cả hai thứ tự. Đây là phép phối hợp hai nhóm lỗi mới, không phải chỉ chạy lại ca parse hay ca object đơn lẻ; mô hình chưa chứng nhận helper tương lai.

### HƯỚNG 6: Cửa sổ trước land của quyết định Q7 và phép loại trừ write set
- Giả thuyết: Trước khi Q3 mới land, ai-dang-giu cũ có thể coi bia mộ dùng ID int là đối xứng và trả không có người giữ.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py q7risk`.
- Output thật:
```text
UTC 2026-09-29T10:31:47.803775+00:00
baseline rc 0 lines ['CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ\told\trefs/heads/main:ops/leases/old.yaml', 'NGƯỜI_GIỮ 0: không có'] err 
strict_Q3_model rc 12 lines ['PHẠM_VI: quét refs/heads/*; nhánh cục bộ tụt sau origin/<cùng tên> sẽ bị CHẶN'] err KHÔNG_XÁC_ĐỊNH: bia mộ một chiều 'old' -> '1000' tại refs/heads/main:ops/leases/old.yaml; không tìm thấy lease thay thế trỏ ngược bằng thay_the_cho
bad_ID_present int old_active CÒN_HẠN
```
- Kết luận: CÓ RỦI RO CỦA QUYẾT ĐỊNH Q7, không xếp P1/P2/P3 chỉ vì làm đúng quyết định. Fixture dùng old còn hạn trỏ "1000", peer có ID int1000 trỏ ngược: nền trả0/người giữ0; mô hình strict Q3 trả12. A9 trước land sẽ phát hiện ID int, nhưng không làm phép hỏi cấp lease trước đó trở thành phép kiểm kiểu. Trên snapshot thật đã đo mọi ID là str, nên không khai rủi ro này đang xảy ra. Không đề nghị khôi phục cổng trước cấp lease.

### Kiểm bắt buộc bổ sung: object format và đọc một lần (không tính vào sáu hướng)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py format`
```text
UTC 2026-09-29T10:31:48.112801+00:00
sha1 oid_len 40 object_hash_match True raw_file_hash_matches False hardcoded_sha1_matches True
opposite_default 0 True
sha256 oid_len 64 object_hash_match True raw_file_hash_matches False hardcoded_sha1_matches False
opposite_default 0 True
```

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_probes.py aba`
```text
UTC 2026-09-29T10:31:48.338768+00:00
ABA outer_hashes_match True middle_type str
single_read hash_match True type int lease_rc 1
reread_mutant hash_match True type str lease_rc 0
```
KHÔNG PHẢI LỖI: công thức là hash object Git gồm header `blob <length>\0`, dùng format của chính kho, không phải SHA-256 trần hay GIT_DEFAULT_HASH của host. Kho SHA-256 dựng được và chốt hardcode SHA-1 đỏ được. Đọc một buffer băm/phân tích đóng ABA blob; ca ref-race lịch sử không tự chứng minh điều này. Đây là mô hình feasibility, không phải helper sản phẩm.

## KIỂM BỔ SUNG HỢP ĐỒNG VÀ A1–A10

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`, `python goi/independence.py` (cũng đặt PYTHONDONTWRITEBYTECODE=1). Toàn output ở `goi/runtime.log`, `goi/independence.log`.

```text
UTC 2026-09-29T10:34:42.277401+00:00
SCALAR true bool 'True' D2 8 D1 0 strict 8
SCALAR yes bool 'True' D2 8 D1 0 strict 8
SCALAR on bool 'True' D2 8 D1 0 strict 8
SCALAR True bool 'True' D2 8 D1 0 strict 8
SCALAR 1.5 float '1.5' D2 8 D1 0 strict 8
SCALAR 1.50 float '1.5' D2 8 D1 0 strict 8
SCALAR 0x1F int '31' D2 0 D1 0 strict 8
SCALAR 017 int '15' D2 0 D1 0 strict 8
SCALAR 1_000 int '1000' D2 0 D1 0 strict 8
SCALAR 5 int '5' D2 0 D1 0 strict 8
SCALAR 2026-09-29 date '2026-09-29' D2 8 D1 0 strict 8
SCALAR 'yes' str 'yes' D2 0 D1 0 strict 0
COLLISION True yes 9 8
COLLISION True on 9 8
COLLISION 1.5 1.50 9 8
COLLISION 31 0x1F 9 8
COLLISION 15 017 9 8
COLLISION 1000 1_000 9 8
COLLISION khac-lease yes 0 8
BODY 8 base_marker True
Q1 '" a"' ' a' valid False
Q1 '"a "' 'a ' valid False
Q1 '"a\\n"' 'a\n' valid False
Q1 'é' 'é' valid False
Q1 'é' 'é' valid False
Q1 'Ａ' 'Ａ' valid False
Q1 'A' 'A' valid True
Q1 'a' 'a' valid True
Q1 '!!str 1.5' '1.5' valid True
Q1_DUPLICATE {'lease_id': 'good'}
A6 11 ['CÒN_HẠN\tTrue\trefs/heads/main:ops/leases/a.yaml', 'CÒN_HẠN\tTrue\trefs/heads/other:ops/leases/b.yaml', 'NGƯỜI_GIỮ 1: True']
A7 base check 0 holder 0 seen [('check', 'int'), ('holder', 'int')]
A7 strict check 8 holder 0 seen [('holder', 'int')]
WORKFLOW base yes rc 0 POST 0 GH 2 traceback False
WORKFLOW base 'fresh-id' rc 0 POST 1 GH 4 traceback False
WORKFLOW strict yes rc 1 POST 0 GH 0 traceback False
WORKFLOW strict 'fresh-id' rc 0 POST 1 GH 4 traceback False
```

```text
UTC 2026-09-29T10:38:40.313986+00:00
strict probe 0 GH 0 direct 8 oracle PASS
D2_restore probe 0 GH 0 direct 0 oracle TinHieuChotCa(A2 direct int)
L probe 0 GH 0 direct 0 oracle TinHieuChotCa(A2 direct int)
A5_STRING_CONTROL self D5 True D6 0
A5_STRING_CONTROL peer D5 True D6 0
```

| tiêu chí | khả năng đỏ và che chốt | giới hạn |
|---|---|---|
| A1 | Văn bản YAML qua _doc_yaml, D1 nền0/strict8; quoted yes vẫn0 | Fixture bỏ hạn/neo để lỗi không liên quan không che D1 |
| A2 | D2 trực tiếp strict8→restore/L0, chot phát TinHieuChotCa đúng ca; probe vẫn GH0 | Đo mạng không còn giết L sau D3, đúng A2; spec677 được đọc ở hash đã neo, không suy freeze/lease live |
| A3 | Trích _buoc_workflow('đăng'), Python thật, gh executable giữ trạng thái: yes nền0/POST0→strict1/POST0; fresh0/POST1 | Direct D3 bool nền9→strict8 tách khỏi D1; không nhận workflow đơn lẻ là bằng chứng mutant D3 |
| A4 | dung_than trực tiếp bool: nền có marker True; strict8 | Chưa có catalog mutant ứng viên |
| A5 | Kho Git thật: từng toán hạng D5 False→True, D6 8→0; đối chứng chuỗi D5 True/D6 0 | Mô hình chỉ chứng minh khả thi, không sửa mã thật |
| A6 | Hai ref/path yes/on nền rc11, NGƯỜI_GIỮ1:True | A6 buộc nhãn KHÔNG_XÁC_ĐỊNH cho cả hai nên không bị nonzero che; chưa có D7 ứng viên |
| A7 | Main CLI check/holder đo riêng: D1 mới chặn check8, holder vẫn tới dự báo int | Instrument đúng entry point dự báo, không khai đã đo mutant D8 hay toàn dự báo sản phẩm mới |
| A8 | Suite nền187/187, rc0/bỏ0; thêm ca đỏ làm delta đỏ | Ứng viên chưa có; Ruff module vắng nên bare lint/delta F KHÔNG ĐO ĐƯỢC |
| A9 | Cổng đúng thời điểm theo Q7; có thể dựng các ca trên kho tạm, SHA-256 cũng dựng được | Hai P2 ở hợp đồng chứng cứ/miền; helper chưa có; không tái đưa mã quét vào spec |
| A10 | TinHieuChotCa/chot có sẵn; A2 mô hình giết trực tiếp bằng lớp tín hiệu riêng | Chưa có catalog A1–A7 của executor để chứng nhận bảng giết thật/tín dụng giả/sống sót |

Fixture sẵn có: `_buoc_workflow` :555; `GhGia` :193; `_kho_thu` :1506; `_git_fixture` :3746; `_kho_do_thi` :4730; `TinHieuChotCa` :4674. `_chay_buoc_dang` dùng stub nên tự nó chưa đủ A3; phép đo của reviewer dùng bước trích thật và Python thật. Tất cả mô hình/fixture nằm ngoài checkout trong mktemp dưới R.

Kiểm kê danh tính: `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho|\.stem|name\[:-5\]' cay-kho/ops/lease_publish.py` → `goi/identity-inventory.log`; đã đọc luồng D1–D9. Sổ thu hồi kiểm str/regex/tên tệp tại1192–1195; cap_lai_cho kiểm tại1232–1236, không đưa non-str vào danh tính. Packet loop :769–771 đòi str. Không tìm thấy đường quyết định danh tính khác bị bỏ khỏi D1–D8 trong phạm vi đọc. `rg -n lease_id cay-kho/.github/workflows` → không output, rc1 (`goi/workflow-id.log`). D9 là hiển thị; tên tệp lease thông thường chỉ là vị trí, còn tên tệp sổ thu hồi được validator riêng canh.

Q3 không đòi sửa workflow/caller ngoài write set. `rg -n ai-dang-giu cay-kho/.github/workflows cay-kho/ops/*.sh cay-kho/.claude/skills` chỉ gặp chú thích của `ops/dung_goi_review.sh` trong phạm vi ấy; không suy từ grep thành đã vét mọi consumer bên ngoài kho. Hành vi fail-close là điều Q3 cho phép ngay trong lease_publish.py.

`goi/contract.py` so cấu trúc A1–A8/A10 giữa r4/r5: mọi `AC_UNCHANGED` đều True. Gỡ mã chỉ làm A9 mất dụng cụ tham chiếu; không làm mất nguồn phép đo của những tiêu chí còn lại. A9 có biên mã thoát được mô tả, không bắt buộc thêm một tệp CLI ngoài write set.

Closure: `contract.py` xác nhận đủ field/schema/mục bắt buộc; các job gate/gate-ops/gate-registry/gate-packet-loop không đổi tên qua name override và có matrix os, nhánh chuẩn bị luôn có ubuntu-latest (`ci.yml`:37–43); workflow/job thu-hoi đúng tên. `ANCESTOR 0`, `POLICY 128` (policy chưa có ở nền), `SPEC_BLOB_MATCH True`. Đổi required_checks làm băm spec đổi. Tiền lệ wp461/#470 được đọc ở `ops/leases/wp461-*.yaml`: chỉ là tiền lệ ngoại lệ có phạm vi, không tự cấp quyền cho wp678. Theo authority prompt, descriptor682/5627190292 và miễn trừ r3 trở đi được xét như lời khai điều phối, không yêu cầu OWNER hoặc byte thân Issue làm bằng chứng chưa được cấp. Nghĩa vụ ghi sổ/thu hồi/audit nằm ở vai land, không yêu cầu executor sửa ngoài hai tệp. Việc dời nền đã thành revision bền, không che product diff; không phát hiện mâu thuẫn closure mới.

A2/#677: blob spec677 đo lại `81468e21c7a7d32167d210b17813dab2b825992a1587b86d8bc8b3dc9142a4da`; nghĩa vụ hai thứ tự vẫn khả thi trong test file. Mô hình L bên trên xác nhận phải chuyển phép giết sang D2 trực tiếp. Trạng thái freeze/lease677 live KHÔNG ĐO ĐƯỢC.

§8/§9/§10 và header: đã đọc r4-r5.diff. §9 đếm đúng các lớp từ bốn verdict, đã kích hoạt gỡ mã và ghi chuyển giao. §10 không tự khai helper đã đạt. Không còn khối Python hoặc lệnh dùng bộ quét cũ làm cổng hiện hành; các lệnh cũ đều có nhãn lịch sử. Câu bao quát “Mọi con số … đo lại … cấp lease” ở369 phải đọc cùng ngoại lệ Q7/A9 và câu373: nó không phục hồi cổng quét kiểu trước cấp. Không mở finding chỉ vì tuân Q7. Header depends_on giữ kiểm write-set exclusion và yêu cầu đo lại; kết quả snapshot hiện tại thực sự cho thấy lý do cần yêu cầu ấy (bảng đo dưới).

## BẢNG ĐO

Lệnh đo số hiện tại: `PYTHONDONTWRITEBYTECODE=1 python goi/measure.py`, `python goi/contract.py`, `python goi/runtime.py` và `goi/holder-detail.log` (mọi lần chạy Python thử nghiệm đều đặt PYTHONDONTWRITEBYTECODE=1). UTC nằm đầu từng log. §1 đã đo riêng từng scalar và từng cặp, không chỉ kiểm quan hệ.

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| Định danh r5 | cbf9c838…/00d2ee3e… | Khớp đầy đủ kiểm đầu + blob repo | Có |
| §1 true/yes/on/True | bool, str=True, D2=8, D1 qua | Từng dạng D2=8/D1=0 | Có |
| §1 1.5/1.50 | float, str=1.5, D2=8, D1 qua | Từng dạng D2=8/D1=0 | Có |
| §1 0x1F/017/1_000 | int31/15/1000, D2/D1 qua | Đúng từng giá trị; A1 thêm5 cũng đúng | Có |
| §1 date/quoted yes | date2026-09-29:8/qua; str yes:qua/qua | Đúng từng trường hợp | Có |
| §1 va chạm | sáu cặp rc9; khác tên rc0 | Đúng cả sáu và đối chứng | Có |
| §1/A3 workflow | yes0/POST0; fresh0/POST1 | Đúng; mô hình strict1/0 và0/1 | Có |
| §2 D1/D2/D3/D4 |861/949/668/1070 | Inventory đúng | Có |
| §2 D5/D6 |587/592 và609/612 | Inventory + riêng từng toán hạng đã thử | Có |
| §2 D7 |2110/2123 | đọc ID/lập khoá người giữ | Có |
| §2 D8 |1938/1942/1946/1967 | raw/raw/f-string/str; holder CLI tới được | Có |
| §2 D9 |2074/2089/2139/2143 | chỉ hiển thị | Có |
| §2 thu hồi/packet_loop/workflow |1192/769–771/0 dòng | Chốt str có; workflow rg rc1 | Có |
| Header nền |89fc4fa; sản phẩm không đổi; test+13/−19 | base_equal0 cả hai; diff13/19, bốn hunk t131×2/t139/t192 | Có |
| §8 số dòng |2206/10502, test cũ10508 |2206/10502/10508 | Có |
| §8 số ca/max |187/t192 |len(CA)=187, max192 | Có |
| §8/A8 suite hiện tại |187/187, rc0, bỏ0 |187/187 đạt, đã chạy187/bỏ0, rc0; shellcheck0.9.0/actionlint1.7.7 | Có |
| Lịch sử185/187 |thiếu shellcheck t137/t159 |Môi trường hiện tại có công cụ; log lịch sử gốc không được cấp | KHÔNG ĐO ĐƯỢC lịch sử; không bác bằng số hiện tại |
| §8 shallow/replace |false/0 |false/0 | Có trên ảnh cấp |
| §8 remote510; prompt505 |mốc10:14/lời mô tả sandbox |cache512=mirror512 theo tên+OID; local1 | Ảnh cấp mới hơn; không chứng minh mốc10:14 sai, không đo live |
| §8 quét giữ từ r4 |512 ref=510+2;563 blob/cặp/ID str |513 ref=512+1;564 blob/cặp, str564, invalid[], bad_hash[] | Khác ảnh và thành phần local; số r4 đã có nhãn tham khảo |
| §8 retired |0 blob/0 cặp |0/0; live564/564 | Có trên ảnh cấp |
| §8 chênh lịch sử +4ref/+1blob,559/560/562 |nhãn lịch sử |Không có đầy đủ map đúng các mốc ấy | KHÔNG ĐO ĐƯỢC lịch sử |
| §8 người giữ10:14 |0/0, rc0 |tệp sản phẩm0/rc0; test1/rc11: lease-publish-windows-do-r1-g1-claude | Đã trôi sau10:14; lease mới ghi leased_at10:20, hết hạn30-09T10:20Z; depends_on hiện chưa thoả |
| §8 T131 |HẾT_HẠN,08:15Z |HẾT_HẠN tại ref bookkeeping-676 | Có |
| Ruff |KHÔNG ĐO ĐƯỢC |python -m ruff --version rc1/No module named ruff | Có giới hạn; không khai lint passed |
| Phụ lục28 CLI/race |Hồ sơ lịch sử |Đã đọc script/output được cấp; không chạy lại toàn bộ giàn r4 trong lượt này | Không dùng làm bằng chứng helper; không khai tự đo28 ca |

Suite đã chạy: `review_tmp=$(cat goi/scratch-path); PYTHONDONTWRITEBYTECODE=1 TMPDIR="$review_tmp" python cay-kho/ops/lease_publish_test.py > goi/suite.log 2>&1`. Hai tệp Python trùng nền nên đây là suite nền. Không có ứng viên để đo delta. Snapshot mirror đủ tên+OID cục bộ; thay đúng nguồn tên nhánh máy chủ bằng mirror trong phép người giữ, không gọi mạng và không khai trạng thái GitHub live.

Điều kiện cấp lease hiện **chưa thoả** vì lease Windows đang giữ test file. Đây là kết quả kiểm prerequisite của header, **không** phải finding rằng spec thiếu prerequisite, và không phải lý do dừng việc review đặc tả.

## CHI TIẾT TỪNG LỚP

### bo-quet-chung-cu-khong-neo-anh [P2] Băm blob không chứng minh cạnh từ tree con nguyên vẹn

VỊ TRÍ: SPEC.md:264–268,302–303; Phụ lục542–548. Cùng slug của lượt2–4; biểu hiện tree con không được tách thành lớp mới theo định dạng object.

VẤN ĐỀ: A9 chuyển đúng phép băm blob, nhưng câu “Tree hoặc commit hỏng: Git tự từ chối ở lệnh liệt kê cây, helper phải kiểm rc ấy” sai ở tree con. Khi bytes dưới OID của tree `HEAD:ops/leases` được đổi để trỏ tới blob chuỗi khác có băm hoàn toàn đúng, Git ls-tree vẫn0/không stderr, ref và tree OID vẫn như cũ. Băm các blob kết quả không bắt được cạnh bị đổi; báo cáo sạch đang nói về một nội dung không thuộc ảnh OID đã neo. R5 đưa kiểm toàn vẹn object vào hợp đồng rồi dựa vào một giả định Git chỉ được chứng minh trên tree gốc.

Phản chứng không tạo va chạm SHA, không đổi Git executable, không có đường thoát cây; chỉ làm hỏng object-store riêng trong fixture. Cả loose và packed đều có biểu hiện; packed thử lại với checksum pack/index và CRC được cập nhật, chỉ liên kết OID→bytes cố ý sai. Không cáo buộc kho thật hỏng. Tính toàn vẹn mọi blob thật được kiểm riêng; điều ấy không đóng lỗi hợp đồng cho tree.

ĐÃ THỬ: `PYTHONDONTWRITEBYTECODE=1 python goi/tree_probe.py`. Output (tuple là ls-tree_rc, kết luận theo băm-blob, cặp(path,hash_khớp,kiểu), stderr; verified_chain là mô hình chữa giới hạn đúng path fixture):
```text
UTC 2026-09-29T10:37:11.834828+00:00
control loose root (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
corrupt loose root (128, 2, [], 'error: hash mismatch b63c7e9ae97acc320ff7e41ca36b6105743554e0\nfatal: not a tree object') same_head True
fsck 11 verified_chain 2
restore loose root (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
control loose nested (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
corrupt loose nested (0, 0, [('ops/leases/a.yaml', True, 'str')], '') same_head True
fsck 11 verified_chain 2
restore loose nested (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
control packed root (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
corrupt packed root (128, 2, [], 'error: hash mismatch b63c7e9ae97acc320ff7e41ca36b6105743554e0\nfatal: not a tree object') same_head True
fsck 12 verified_chain 2
restore packed root (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
control packed nested (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
corrupt packed nested (0, 0, [('ops/leases/a.yaml', True, 'str')], '') same_head True
fsck 12 verified_chain 2
restore packed nested (0, 1, [('ops/leases/a.yaml', True, 'int')], '') verified_chain 1
```

HINT: có — nhóm `# lop: bo-quet-chung-cu-khong-neo-anh`. Sửa hợp đồng A9 để xác minh toàn chuỗi commit/tree/subtree/blob và lấy cạnh từ chính bytes đã băm; thêm ca tree con loose/packed độc lập, giữ blob chốt nguyên khi gỡ chốt tree. Thu hẹp lời suy từ bảng lịch sử. Không đưa lại code bộ quét; executor tự triển khai trong write set đã có. Phép đo verified_chain cho2 ở nguồn hỏng,1 ở cả đối chứng trước/sau.

Rủi ro vá: kiểm băm rồi đọc lại bằng ls-tree sẽ mở lại ABA; băm text chuẩn hoá/sha1 ghi cứng sẽ từ chối oan kho SHA-256 hoặc CRLF. Giữ nghĩa vụ đọc cùng bytes, object format và ca độc lập của A9. Chỉ xác minh các object/cạnh dùng trong miền quét, không tự mở rộng sang toàn lịch sử Git hoặc toàn bộ object không liên quan.

ĐỘ TIN: cao. P2 về chứng cứ nghiệm thu, không P1 về quyền sản phẩm. Helper chưa tồn tại nên kết luận là chuyển giao chưa đủ, không phải một lỗi đã quan sát trong helper.

### bo-quet-nghiem-thu-thieu-mien [P2] Prose thay mã làm mất miền con trỏ rỗng hợp lệ

VỊ TRÍ: SPEC.md:258–260,286–289; mã runtime `_danh_sach_thay_the_cho`:563–569 và `_bia_mo_doi_xung`:581–585; khối lịch sử r4 có ngoại lệ `None`/`""` trước kiểm kiểu.

VẤN ĐỀ: r5 nói giữ nguyên nghĩa vụ nhưng mô tả mới chỉ cho `thay_the_cho` là str/list và `da_bi_thay_the` là chuỗi không trắng. Cả hai trường vốn tuỳ chọn; YAML null là không có con trỏ, và `da_bi_thay_the: ""` cũng là không có bia mộ. Khi code định nghĩa các ngoại lệ bị gỡ, executor có thể viết đúng miền prose r5 (kể cả cho phép vắng trường) mà vẫn bác ba đầu vào hợp lệ này ở A9. Danh mục tối thiểu chỉ có empty-list dương nên không bắt được việc siết sai ấy. Một lease với ID chuỗi hợp lệ có thể khiến nghiệm thu báo lỗi lease và chặn land chỉ vì cách biểu diễn không-có-con-trỏ vốn được runtime nhận. Đây là sai miền schema sau chuyển giao, không đề nghị nới Q1 hay sửa lease lịch sử.

ĐÃ THỬ: `PYTHONDONTWRITEBYTECODE=1 python goi/pointer_transfer.py`; mỗi ca là kho Git riêng, so nguyên code r4/runtime với đúng predicate miền prose r5. Predicate là phản ví dụ một cách cài đặt được văn bản cho phép, không tự nhận đó là helper tương lai.
```text
UTC 2026-09-29T10:32:52.990251+00:00
thay_the_cho None runtime [] r4_rc 0 literal_r5_rc 1
thay_the_cho '' runtime [] r4_rc 0 literal_r5_rc 0
thay_the_cho '   ' runtime [] r4_rc 0 literal_r5_rc 0
thay_the_cho [] runtime [] r4_rc 0 literal_r5_rc 0
thay_the_cho ['x'] runtime ['x'] r4_rc 0 literal_r5_rc 0
da_bi_thay_the None runtime None r4_rc 0 literal_r5_rc 1
da_bi_thay_the '' runtime None r4_rc 0 literal_r5_rc 1
da_bi_thay_the '   ' runtime False r4_rc 1 literal_r5_rc 1
da_bi_thay_the [] runtime False r4_rc 1 literal_r5_rc 1
da_bi_thay_the ['x'] runtime False r4_rc 1 literal_r5_rc 1
```

HINT: có — nhóm `# lop: bo-quet-nghiem-thu-thieu-mien`. Ghi rõ hai trường tuỳ chọn; vắng/null/chuỗi rỗng là không có con trỏ; giữ nguyên quy tắc chuỗi/list còn lại và thêm đối chứng dương tương ứng. False/0, list ở da_bi_thay_the, phần tử list trắng vẫn phải đỏ. Không yêu cầu đối xứng mọi bia mộ lịch sử. Không có thay đổi sản phẩm ngoài write set.

Rủi ro vá: dùng truthiness chung sẽ nuốt luôn False/0; HINT chặn điều ấy bằng ca âm và mô tả tường minh. Chuỗi trắng của thay_the_cho được helper runtime chuẩn hoá thành danh sách rỗng, còn chuỗi trắng da_bi_thay_the không hợp lệ; không gộp hai miền.

ĐỘ TIN: cao về chênh schema có thể thi hành theo chữ; snapshot thật hiện chỉ có các con trỏ nonempty khi trường hiện diện (measure.log), nên chưa có ca chặn nhầm ở kho nguồn. Chính các fixture hợp lệ phần bù là phạm vi finding.

## DRY-RUN HINT.patch

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

HINT chỉ nhắm `ops/specs/lease-id-ep-kieu-yaml-r5.md` làm gợi ý cho revision6; không sửa r1–r4, không sửa checkout hiện hành, không tái đưa mã scanner vào đặc tả. Giữ nguyên Q7. Các đề xuất về triển khai chỉ mô tả bằng lời.

Lệnh đã chạy (R là đường tuyệt đối trong prompt):

```sh
PYTHONDONTWRITEBYTECODE=1 python goi/build_hint.py
review_hint_tmp=$(mktemp -d -p "$R")
cp -a "$R/cay-kho" "$review_hint_tmp/cay"
patch -d "$review_hint_tmp/cay" -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```

Output thật:
```text
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: bo-quet-chung-cu-khong-neo-anh
|--- ops/specs/lease-id-ep-kieu-yaml-r5.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r5.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r5.md
Using Plan A...
Hunk #1 succeeded at 267.
Hunk #2 succeeded at 305.
Hunk #3 succeeded at 553.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: bo-quet-nghiem-thu-thieu-mien
|--- ops/specs/lease-id-ep-kieu-yaml-r5.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r5.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r5.md
Using Plan A...
Hunk #1 succeeded at 255.
Hunk #2 succeeded at 290 (offset -6 lines).
done
dry_run_rc=0
```

Áp thật trên chính bản sao, `cmp` với `goi/hint-expected.md`, rồi `git diff --check`:
```text
patching file ops/specs/lease-id-ep-kieu-yaml-r5.md
patching file ops/specs/lease-id-ep-kieu-yaml-r5.md
apply_rc=0
expected_cmp_rc=0
diff_check_rc=0
```

Hai nhóm hunk áp tuần tự, cùng một đường repo-relative; dry-run có offset dòng vì nhóm trước chưa ghi file, không có fuzz. Áp thật khớp byte kết quả dự kiến. Đây không phải bằng chứng ca helper đã chạy.

## TOÀN VẸN VÀ GIỚI HẠN

Không có GitHub/mạng, không sửa cay-kho hoặc kho.git, không cấp lease/approve/merge/land. Q7 là quyết định được tôn trọng; hướng6 ghi rủi ro có điều kiện của việc cấp trước khi chốt mới land, không dùng nó để ép thêm cổng. Snapshot thật mọi ID đều str, nhưng đang có lease Windows giữ test file như đã ghi riêng.

Chưa đo: GitHub live, bytes thân Issue682, model/effort/session identity theo máy, helper/candidate thật, Windows, Ruff lint/delta F, timeout/OS kill/OOM và toàn bộ không gian YAML/object corruption. Các mô hình chỉ chứng minh fixture và tính khả thi, không thay nghiệm thu executor. Đã đọc log/script tự kiểm r4 nhưng không khai đã chạy lại toàn bộ chúng; r2 được trích chạy nguyên entry point và ca riêng như yêu cầu.

Lỗi rig đã sửa trước khi dùng kết luận: pack fixture do Git tạo là read-only nên thay tệp trong scratch; khôi phục packed cần bỏ pack hỏng của fixture thay vì chỉ ghi loose object; mô hình strict khi chạy CLI phải định nghĩa helper trước main guard. Các output bàn giao là lần chạy sau sửa, không dùng lỗi setup làm finding hoặc tín hiệu giết mutant.

Sandbox thực là workspace-write; tuân read-only bằng giới hạn đường ghi. Snapshot đầu/cuối regular files của checkout và mirror gồm tracked/untracked/ignored/Git metadata; chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh mọi syscall của cả phiên.

Kiểm cuối: `PYTHONDONTWRITEBYTECODE=1 python goi/verify.py`:

```text
UTC 2026-09-29T10:42:51.184051+00:00
SOURCE_FILES 3014 3014 delta []
HEAD 00d2ee3e911fbc0ef1978a19eab3da91580f3fa6
TREE 9865652f4df6ea1528637ac0799791db688263d0
SPEC 1 578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c
SPEC 2 1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715
SPEC 3 64c67225335cf50b2a394ffda005e03d338ff545757b210640fd05ac14564af1
SPEC 4 2726d59ffb683f44e68c1409241250c40025bc02a9c9bfb257e767831a1e17f2
SPEC 5 cbf9c8380f0da45e2af07034cc6715b75c8ac2deb36a4967497b94d1a9394150
CLASSES [('bo-quet-chung-cu-khong-neo-anh', 'P2'), ('bo-quet-nghiem-thu-thieu-mien', 'P2')]
HUNTS ['1', '2', '3', '4', '5', '6']
HINT_GROUPS ['bo-quet-chung-cu-khong-neo-anh', 'bo-quet-nghiem-thu-thieu-mien']
HINT_PATHS ['ops/specs/lease-id-ep-kieu-yaml-r5.md', 'ops/specs/lease-id-ep-kieu-yaml-r5.md', 'ops/specs/lease-id-ep-kieu-yaml-r5.md', 'ops/specs/lease-id-ep-kieu-yaml-r5.md']
HINT_CHANGED ops/specs/lease-id-ep-kieu-yaml-r5.md
APPLIED_MATCH True
PYTHON_BLOCKS 0
SUITE
lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0
suite_rc=0
VERIFIED
```

Băm các hiện vật bàn giao lưu ngoài chúng tại `goi/artifact-hashes.txt`; không nhúng băm tự tham chiếu.
