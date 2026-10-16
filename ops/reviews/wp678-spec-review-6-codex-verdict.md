verdict: approve
reviewed_sha: 03a7219c9f3df4e6304f499b79df968aa7d386cb
spec_sha256: d1f9dd7903c99df03b9e65bc06a2175eb43e0e602758a6945508ff33af76244c
model/effort tự khai: GPT-6 (Codex); effort không được môi trường công bố.
provider: openai_codex
execution_surface: API agent có shell cục bộ
transport: machine; bàn giao tệp offline
reviewed_tree: e692d52c82adffadec70ef5f6ac4b0360423c7e2
assurance: tự khai danh tính; không có metadata máy xác minh exact served model/effort. Không suy từ tên reviewer yêu cầu hoặc tài khoản GitHub.

Đã đọc toàn bộ prompt.snapshot. Kiểm định danh: sha256sum SPEC.md và git -C cay-kho rev-parse HEAD khớp giá trị yêu cầu.

## ĐỐI CHIẾU LƯỢT TRƯỚC
Đối chiếu đã hoàn tất trước các hướng săn mới; kiểm bổ sung có dẫn log bên dưới.

Lệnh đối chiếu ban đầu: `PYTHONDONTWRITEBYTECODE=1 python goi/precheck.py` (UTC và output đầy đủ: `goi/precheck.log`).

| lớp lượt 1–5 | trạng thái | bằng chứng tự đo / giới hạn |
|---|---|---|
| bo-quet-nghiem-thu-thieu-mien | ĐÃ ĐÓNG biểu hiện r5 trong hợp đồng; các nghĩa vụ helper CHUYỂN GIAO | Chạy hai hàm thật: thay_the_cho vắng/null/chuỗi rỗng/chuỗi trắng/[] → []; da_bi_thay_the vắng/null/chuỗi rỗng → None, trắng/list/false/0 → False. A9 viết đúng từng miền, thêm ca dương riêng và ba nhóm đột biến. Helper chưa tồn tại. |
| bo-quet-chung-cu-khong-neo-anh | NGOÀI PHẠM VI THEO Q9 đối với commit/tree; CHUYỂN GIAO đối với blob/race/replace | A9 và §9/§10 đều nói fsck cùng lượt, không nguyên tử, giữ băm cùng bytes blob; không đòi helper kiểm tree. PYTHON_BLOCKS 0. Không gọi chuyển scope là đã vá. |
| bo-quet-khong-co-cua-chay | CHUYỂN GIAO | R2_CLI rc0/stdout rỗng; tự dựng blank-list: R2_DIRECT (1,1,1,[]), r4 CLI1/JSON có lỗi. A9 giữ biên 0/1/2, JSON và ca qua biên thật; helper chưa có để chứng nhận. |
| tieu-chi-dot-bien-khong-phan-biet-chot | ĐÃ ĐÓNG trong hợp đồng | A2/A5 giữ nguyên r5; mô hình từng toán hạng trên bản sao: D5 :587/:592 False→True; D6 :609/:612 8→0. D2 strict8→restore0/L0; phép dò vẫn GH0. Xem runtime.log, independence.log. |
| so-do-nen-khong-khop | ĐÃ ĐÓNG biểu hiện cũ; số hiện tại đã đo lại | A6/A8 nguyên byte so r5; A6 yêu cầu nhãn và ref/path, không chỉ nonzero. Không lấy snapshot mới bác số lịch sử. |
| hop-dong-dong-bang-thieu-neo | ĐÃ ĐÓNG trong phạm vi lời khai được giao | CLOSURE_HASH_CHANGES True; descriptor682/5627190292, miễn trừ có phạm vi và hạn; đủ closure trong bytes. Không cần đo GitHub live. |
| objective-dong-nhat-cu-phap-voi-danh-tinh | ĐÃ ĐÓNG | Q1_EQUAL quoted/tagged yes và 1.5 đều True; objective chủ ý dùng chuỗi sau safe_load. |
| bang-duong-phan-loai-sai | ĐÃ ĐÓNG biểu hiện cũ | D7/D8/D9 theo hàm thật; diff test 13/19, bốn hunk (header diff có thể in tên hàm trước, phải đọc thân); lịch sử race tách khỏi CLI. |
| trang-thai-q3-chua-dong-bo | ĐÃ ĐÓNG | Q3_CLOSED 2 True: cùng neo5885268193, §10 nói không còn câu hỏi mở. |

Đã đối chiếu trước hướng săn mới. Q7/Q9 là quyết định cố định. Không dùng các kiểm bắt buộc ở đây để cộng số hướng săn.

## BẢNG LỚP
Kết luận nội dung: **0 P1 / 0 P2 / 0 P3**. `approve` cho **đặc tả r6** trên exact SHA đã khai; không phải chứng nhận ứng viên/helper chưa viết, không phải cấp lease hay quyền land.

| slug lớp | hạng | biểu hiện (vị trí trong SPEC) | phương án chung | phép kiểm / giới hạn |
|---|---|---|---|---|
| Không có lớp cần sửa | — | — | HINT.patch rỗng | Các lớp chuyển giao vẫn phải được executor chứng minh; phần tree/commit ngoài phạm vi theo Q9. |

## BẢNG SĂN

Các hướng dưới thay các giả thuyết khác nhau trên phần r6 mới: chuẩn hoá khoảng trắng; đồ thị YAML; schema so với quan hệ lịch sử; bố cục kho cho fsck; nghĩa của output fsck; độ mới cache của phép so tên Q8. Không tính đối chiếu cũ, đo số nền, kiểm schema/closure hoặc các ca/đột biến tối thiểu bắt buộc vào số hướng này. `review_model.py` chỉ là mô hình khả thi của reviewer; không là helper sản phẩm, không được gợi ý chép vào đặc tả.

### HƯỚNG 1: Chuẩn hoá con trỏ có lấn sang danh tính ID?

- Giả thuyết: Miền mới viết theo strip() có thể bị hiểu thành cho phép strip lease_id hoặc bỏ Unicode không trắng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_hunts.py normalization`.
- Output thật:
```text
UTC 2026-09-29T11:02:35.899977+00:00
WHITESPACE thay_the_cho '\t' runtime [] schema True
WHITESPACE da_bi_thay_the '\t' runtime False schema False
WHITESPACE thay_the_cho '\xa0' runtime [] schema True
WHITESPACE da_bi_thay_the '\xa0' runtime False schema False
WHITESPACE thay_the_cho '\u2003' runtime [] schema True
WHITESPACE da_bi_thay_the '\u2003' runtime False schema False
WHITESPACE thay_the_cho '\u200b' runtime ['\u200b'] schema True
WHITESPACE da_bi_thay_the '\u200b' runtime False schema True
NORMALIZE ' x ' ['x'] True
NORMALIZE [' x ', 'x'] ['x', 'x'] True
NORMALIZE ['a.b', 'a-b'] ['a.b', 'a-b'] True
ID ' x ' False
ID 'x\n' False
ID 'x' True
ID 'X' True
ID 'é' False
ID 'é' False
NORMALIZED_POINTER_IS_NOT_ID_RULE False ['x']
```
- Kết luận: KHÔNG PHẢI LỖI. Runtime chuẩn hoá con trỏ; Q1 vẫn kiểm nguyên giá trị ID. U+200B không bị strip: schema str không trắng hợp lệ dù chưa có peer đối xứng. A9 không đòi peer.

### HƯỚNG 2: Alias, merge và đồ thị YAML tự tham chiếu

- Giả thuyết: Cú pháp YAML có thể làm một giá trị không phải str lọt qua miền con trỏ mới hoặc khiến thao tác kiểm schema đệ quy không dừng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_hunts.py yaml_graph`.
- Output thật:
```text
UTC 2026-09-29T11:03:13.196618+00:00
alias_null types ['NoneType', 'NoneType'] runtime [] None model 0 []
alias_blank types ['str', 'str'] runtime [] False model 1 [['ops/leases/a.yaml', 'da_bi_thay_the']]
self_list types ['list', 'NoneType'] runtime None None model 1 [['ops/leases/a.yaml', 'thay_the_cho']]
self_map types ['NoneType', 'dict'] runtime [] False model 1 [['ops/leases/a.yaml', 'da_bi_thay_the']]
merge_override types ['NoneType', 'NoneType'] runtime [] None model 0 []
duplicate_last types ['NoneType', 'NoneType'] runtime [] None model 0 []
binary types ['bytes', 'NoneType'] runtime None None model 1 [['ops/leases/a.yaml', 'thay_the_cho']]
set types ['set', 'NoneType'] runtime None None model 1 [['ops/leases/a.yaml', 'thay_the_cho']]
date types ['NoneType', 'date'] runtime [] False model 1 [['ops/leases/a.yaml', 'da_bi_thay_the']]
```
- Kết luận: KHÔNG PHẢI LỖI. Theo safe_load, alias-null hợp lệ, alias-blank lỗi đúng trường; self-list/self-map bị loại ở kiểm kiểu nông, không cần lần theo đồ thị. Merge/duplicate xét giá trị cuối đúng objective. Mô hình chưa chứng nhận helper.

### HƯỚNG 3: Schema con trỏ và khả năng tìm peer ở miền lịch sử

- Giả thuyết: Câu BẰNG miền runtime có thể vô tình buộc A9 tìm peer còn sống hay miễn lease hết hạn.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_hunts.py schema_symmetry`.
- Output thật:
```text
UTC 2026-09-29T11:03:14.022443+00:00
ops/leases thay_the_cho 'missing-peer' expiry HẾT_HẠN symmetry None schema_rc 0
ops/leases_retired thay_the_cho 'missing-peer' expiry HẾT_HẠN symmetry None schema_rc 0
ops/leases thay_the_cho ['missing-peer'] expiry HẾT_HẠN symmetry None schema_rc 0
ops/leases_retired thay_the_cho ['missing-peer'] expiry HẾT_HẠN symmetry None schema_rc 0
ops/leases da_bi_thay_the 'missing-peer' expiry HẾT_HẠN symmetry False schema_rc 0
ops/leases_retired da_bi_thay_the 'missing-peer' expiry HẾT_HẠN symmetry False schema_rc 0
ops/leases da_bi_thay_the ' ' expiry HẾT_HẠN symmetry False schema_rc 1
ops/leases_retired da_bi_thay_the ' ' expiry HẾT_HẠN symmetry False schema_rc 1
ops/leases da_bi_thay_the False expiry HẾT_HẠN symmetry False schema_rc 1
ops/leases_retired da_bi_thay_the False expiry HẾT_HẠN symmetry False schema_rc 1
```
- Kết luận: KHÔNG PHẢI LỖI. A9 phân biệt schema với đối xứng và nói bất kể hạn. Cùng schema được chấp nhận trong live/retired dù peer vắng; chuỗi trắng/false bị bác cả khi hết hạn. False do thiếu peer không đồng nghĩa sai kiểu con trỏ.

### HƯỚNG 4: Khả năng thực hiện Q9 ở các bố cục kho

- Giả thuyết: Điều kiện mới có thể chỉ chạy ở checkout thường hoặc buộc viết ngoài write set khi dùng bare/linked-worktree/SHA-256.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_hunts.py fsck_layout`.
- Output thật:
```text
UTC 2026-09-29T11:03:14.653176+00:00
sha1 checkout fsck 0 stdout '' stderr '' scan 0 pairs 1
sha1 bare fsck 0 stdout '' stderr '' scan 0 pairs 1
sha1 linked_worktree fsck 0 stdout '' stderr '' scan 0 pairs 1
sha256 checkout fsck 0 stdout '' stderr '' scan 0 pairs 1
sha256 bare fsck 0 stdout '' stderr '' scan 0 pairs 1
sha256 linked_worktree fsck 0 stdout '' stderr '' scan 0 pairs 1
```
- Kết luận: KHÔNG PHẢI LỖI. Git fsck --full và mô hình băm blob đều chạy ở checkout, bare và linked worktree với SHA-1/SHA-256; không cần thay tệp sản phẩm để thực hiện prerequisite.

### HƯỚNG 5: Output fsck hợp lệ nhưng không rỗng

- Giả thuyết: Lời khai output rỗng của kho soạn có thể bị hiểu thành điều kiện land và chặn kho có dangling object vô hại.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_hunts.py fsck_output`.
- Output thật:
```text
UTC 2026-09-29T11:03:15.080480+00:00
DANGLING 0 'dangling blob 029e05d8c5005f4eb93c355e7e704c7cebc8fe3f\n' '' scan 0
HANDOFF_ACCEPTS_NONEMPTY_RC0 True
EXTRA_REF 0 scan_refs 2
```
- Kết luận: KHÔNG PHẢI LỖI. Có dangling blob vẫn rc0, scan0; A9 buộc ghi nguyên output, chỉ dùng rc0 làm điều kiện cần, không đòi output rỗng. Mốc output rỗng ở §8 đã mang nhãn tham khảo.

### HƯỚNG 6: Tên nhánh không đổi nhưng lease mới đã được push

- Giả thuyết: So tên ref mới ở Q8 có thể được coi nhầm là kiểm độ mới OID, dẫn tới báo người giữ 0 trên cache cũ.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/new_hunts.py q8_cache`.
- Output thật:
```text
UTC 2026-09-29T11:03:15.594379+00:00
STALE names_equal True oid_equal False holder_rc 0 last NGƯỜI_GIỮ 0: không có stderr ''
AFTER_FETCH names_equal True oid_equal True holder_rc 11 last NGƯỜI_GIỮ 1: other-valid-string stderr ''
```
- Kết luận: KHÔNG PHẢI LỖI được xếp hạng ở đặc tả này; có GIỚI HẠN của phép so tên. STALE cho tên bằng/OID khác và holder0; sau fetch + đồng bộ local branch cho holder11. Q8 được thuật lại đúng phép so tên đã chốt; §8 yêu cầu đo lại lệnh fetch trước công bố. Không coi so tên là so ảnh; A9 còn bắt tên+OID trước land. Không có chứng cứ cửa sổ này đang xảy ra ở snapshot cấp; không nâng rủi ro thành yêu cầu phục hồi cổng kiểu trước cấp.

## KIỂM BẮT BUỘC BỔ SUNG

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`, `PYTHONDONTWRITEBYTECODE=1 python goi/independence.py`, `PYTHONDONTWRITEBYTECODE=1 python goi/acceptance_a9.py`. Mô hình và mọi mutant chỉ ghi vào thư mục mktemp dưới R. Không dùng mô hình làm cổng land.

### A1–A10: tính khả thi và khả năng đỏ

| tiêu chí | bằng chứng tự đo / kết luận | giới hạn |
|---|---|---|
| A1 | Văn bản YAML qua `_doc_yaml`: từng scalar bool/float/int/date D1 nền0→strict8; quoted yes vẫn0. Gỡ riêng D1, giữ D3:8→0, TinHieuChotCa(A1). | Mô hình, chưa có ứng viên. |
| A2 | Thêm int: tiền kiểm strict8→restore0/L0. Phép dò trả về bình thường, GH0 ở cả ba vế do D3; ca trực tiếp giết bằng TinHieuChotCa(A2_direct_int). | Số gọi không còn là tín hiệu phân biệt D2; spec đã nói đúng. |
| A3 | Thân bước đăng trích bằng `_buoc_workflow`, Python thật, gh trên PATH giữ trạng thái: yes nền rc0/POST0→strict rc1/POST0; fresh-id rc0/POST1 cả hai. Đơn vị D3 gỡ riêng, giữ D1:8→9. | Mô phỏng GitHub offline; không đo endpoint thật. |
| A4 | `dung_than` trực tiếp bool: strict8; gỡ riêng D4→trả về thân có marker True, TinHieuChotCa(A4). | Chưa có mutant của executor. |
| A5 | Từng toán hạng D5 :587/:592 False→True, D6 :609/:612 8→0. Kho Git tạm thật cho D6. Đối chứng chuỗi ở cả hai đầu D5=True/D6=0. | Precheck đo kết quả từng toán hạng; chưa chứng nhận catalog tín hiệu của executor. |
| A6 | Hai ref/path yes/on còn hạn: nền rc11, NGƯỜI_GIỮ 1: True. Spec chốt nhãn KHÔNG_XÁC_ĐỊNH cùng ref/path của cả hai nên nhận được khác biệt, không dựa riêng nonzero. | Chưa có D7 ứng viên; không khai đã giết mutant D7 sản phẩm. |
| A7 | CLI check nền tới dự báo int, strict D1 chặn8; holder vẫn tới dự báo int. Mô hình chốt độc lập ở từng helper D8: trực tiếp8→gỡ riêng0. | Đo khả năng tới helper và khả thi chốt, không khai đã phủ mọi tổ hợp sổ thu hồi. |
| A8 | Suite nền187/187, rc0/bỏ0; cả hai tệp trùng blob nền89fc4fa. | Chưa có ứng viên để đo delta; Ruff vắng nên bare lint/delta F KHÔNG ĐO ĐƯỢC. |
| A9 | Ca dương từng dạng, ca false/0 và list đều đi qua subprocess/biên 0/1/2 của mô hình. Ba nhóm mutant đổi đúng ca bằng TinHieuChotCa. Blob sai băm: chốt2→gỡ0, cả SHA-1/SHA-256; khôi phục1, thiếu blob2. | Không có helper thật; không chấm lớp object-store/tree đã được Q9 loại. Fsck là prerequisite bên ngoài helper, không che mutant blob. |
| A10 | Chốt dùng lớp TinHieuChotCa thật của suite, nhãn ca rõ ràng; không tính lỗi setup hoặc exception vô can là giết thật. | Catalog A1–A7 của executor chưa tồn tại. |

Output thực của phép kiểm chốt độc lập:
```text
UTC 2026-09-29T11:10:27.277443+00:00
SINGLE_GUARD A1 [(8, 'PASS'), (0, 'TinHieuChotCa(A1)')]
SINGLE_GUARD A3 [(8, 'PASS'), (9, 'TinHieuChotCa(A3)')]
SINGLE_GUARD A4 [(8, 'PASS'), (0, 'TinHieuChotCa(A4)')]
A5_STRING_CONTROL 1000 new D5 True D6 0
A5_STRING_CONTROL old 1000 D5 True D6 0
D8_DIRECT _du_bao_check strict 8
D8_DIRECT _du_bao_check restore 0
D8_DIRECT _du_bao_ai_dang_giu strict 8
D8_DIRECT _du_bao_ai_dang_giu restore 0
```

Output thực của miền con trỏ mới và ba nhóm đột biến:
```text
UTC 2026-09-29T11:07:43.876158+00:00
POSITIVE thay_the_cho:'missing' baseline (0, True, 'PASS') reject_one (1, True, "TinHieuChotCa(thay_the_cho:'missing')")
POSITIVE thay_the_cho:None baseline (0, True, 'PASS') reject_one (1, True, 'TinHieuChotCa(thay_the_cho:None)')
POSITIVE thay_the_cho:'' baseline (0, True, 'PASS') reject_one (1, True, "TinHieuChotCa(thay_the_cho:'')")
POSITIVE thay_the_cho:'   ' baseline (0, True, 'PASS') reject_one (1, True, "TinHieuChotCa(thay_the_cho:'   ')")
POSITIVE thay_the_cho:[] baseline (0, True, 'PASS') reject_one (1, True, 'TinHieuChotCa(thay_the_cho:[])')
POSITIVE da_bi_thay_the:'missing' baseline (0, True, 'PASS') reject_one (1, True, "TinHieuChotCa(da_bi_thay_the:'missing')")
POSITIVE da_bi_thay_the:None baseline (0, True, 'PASS') reject_one (1, True, 'TinHieuChotCa(da_bi_thay_the:None)')
POSITIVE da_bi_thay_the:'' baseline (0, True, 'PASS') reject_one (1, True, "TinHieuChotCa(da_bi_thay_the:'')")
NEGATIVE thay_the_cho:False baseline (1, True, 'PASS') truthiness (0, True, 'TinHieuChotCa(thay_the_cho:False)')
NEGATIVE thay_the_cho:0 baseline (1, True, 'PASS') truthiness (0, True, 'TinHieuChotCa(thay_the_cho:0)')
NEGATIVE da_bi_thay_the:False baseline (1, True, 'PASS') truthiness (0, True, 'TinHieuChotCa(da_bi_thay_the:False)')
NEGATIVE da_bi_thay_the:0 baseline (1, True, 'PASS') truthiness (0, True, 'TinHieuChotCa(da_bi_thay_the:0)')
LIST dbtt:[] baseline (1, True, 'PASS') lists_mutant (0, True, 'TinHieuChotCa(dbtt:[])')
LIST dbtt:['peer'] baseline (1, True, 'PASS') lists_mutant (0, True, "TinHieuChotCa(dbtt:['peer'])")
BLOB_CONTROL sha1 1
BLOB_BAD sha1 hash_on 2 no_hash 0
BLOB_RESTORE sha1 1
BLOB_MISSING sha1 2
BLOB_CONTROL sha256 1
BLOB_BAD sha256 hash_on 2 no_hash 0
BLOB_RESTORE sha256 1
BLOB_MISSING sha256 2
BOUNDARY utf8_bad 2 False KHONG_DO_DUOC: UnicodeDecodeError
BOUNDARY date_bad 2 False KHONG_DO_DUOC: ValueError
BOUNDARY yaml_bad 1 True 
```

Ở nhóm (i), trường còn lại được đặt một chuỗi con trỏ hợp lệ, nên mutant bác vắng/null/rỗng của trường đích không bị lỗi ở trường khác che. Mỗi dạng dùng một kho Git riêng. Nhóm (ii) chốt false và 0 riêng ở từng trường; nhóm (iii) thử cả list rỗng và list chứa tên. Đây là phép kiểm khả thi của yêu cầu r6; chưa phải bằng chứng nghiệm thu helper tương lai.

### Đường danh tính, fixture và phạm vi ghi

Lệnh: `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho|\.stem|name\[:-5\]' cay-kho/ops/lease_publish.py` → `goi/identity-inventory.log`; đã đọc các hàm/caller tương ứng. D1–D8 bao phủ những chỗ quyết định danh tính trong tệp; D9 chỉ hiển thị. Sổ thu hồi tự kiểm str/regex/tên tệp ở1192–1195, `cap_lai_cho` ở1232–1236; packet_loop769–771 đã đòi str. Không phát hiện đường ép kiểu danh tính khác bị bỏ khỏi danh sách trong phạm vi đọc.

`rg -n lease_id cay-kho/.github/workflows` → không output, rc1 (`goi/workflow-identity.log`). `rg -n ai-dang-giu cay-kho/.github/workflows cay-kho/ops/*.sh cay-kho/.claude/skills` chỉ có chú thích trong `ops/dung_goi_review.sh` (`goi/callers.log`). Q3 có thể thực hiện trong lease_publish.py, không buộc sửa caller/workflow ngoài write set. Không suy grep này thành đã vét consumer bên ngoài kho.

Các fixture có sẵn, đo bằng inspect trong `extra_checks.py`: `_buoc_workflow`:555, `GhGia`:193, `_kho_thu`:1506, `_git_fixture`:3746, `_kho_do_thi`:4730, `TinHieuChotCa`:4674. `_chay_buoc_dang` cũ dùng stub, không đủ để chứng nhận A3; phép đo ở đây dùng thân trích và Python thật. Kho tạm và executable gh đủ dựng A3/A5/A6 trong tệp test hiện hữu, không cần nới write set.

### Closure, dependency, §9/§10

Đã đọc protocol §3.2, §4, §8, §13; CLAUDE mục Bài học đắt giá; soan-spec L1–L5 và bảng mục bắt buộc. `extra_checks.py` cho mọi field bắt buộc có mặt, diff PR chỉ thêm r1–r6. Nội dung acceptance đặt tại `nghiem_thu`; closure nằm trong bytes băm. Đổi required_checks làm SHA-256 đổi (`precheck.py`). Descriptor `{mission_issue:682, object_id:5627190292}` và miễn trừ có phạm vi/thời hạn được xét như lời khai điều phối đúng chỉ thị. Không tự suy OWNER thành tác giả người thật và không đòi đo live.

Tiền lệ wp461/#470: lease revision2 và các generation sau khai mission470 cùng nguồn uỷ quyền bền; đó là tiền lệ neo authority, không tự cấp ngoại lệ cho wp678. Miễn trừ của wp678 phải dựa #682 như r6 đã ghi. Policy canonical vắng ở nền (`cat-file -e`:128), nên không thấy điều kiện hết miễn trừ bị kích hoạt trên snapshot. Nền89fc4fa là tổ tiên HEAD, mã sản phẩm không đổi, diff test giữa nền cũ/mới13/19; dời nền bằng revision bền trước thi hành đúng §3.2.1.

`measure.py` đọc YAML job thật: gate/gate-ops/gate-registry/gate-packet-loop không override tên và đều có matrix os; ci.yml:40–43 luôn có ubuntu-latest trong nhánh PR. Workflow và job thu-hoi đúng tên. Nghĩa vụ audit/ghi sổ/thu hồi/đóng Issue nằm ở vai land, không yêu cầu executor ghi ngoài hai tệp.

Q8 xuất hiện nhất quán ở depends_on, §3, nền nghiệm thu và §10: chờ nhả write set, không review đang chạy, hash revision sạch, dời nền nếu #687 land và đổi test. Điều kiện người giữ0 áp cho mọi lease giao write set, nên sự xuất hiện lease #677 trong snapshot mới cũng chặn cấp. Review này không cấp lease. Trạng thái review live và việc #687 sẽ land hay không KHÔNG ĐO ĐƯỢC; không phải lỗi thiếu điều kiện trong đặc tả.

A2 tương tác #677 đã nêu cả hai thứ tự; việc giữ ca xanh và chuyển phép giết L sang D2 trực tiếp nằm trong write set test. Spec677 r1 được đọc từ đúng ref/blob (`goi/spec677.md`), băm81468e21…a4da khớp lời khai lịch sử. Snapshot còn có lease677 revision4 cấp10:48Z (xem bảng đo); không lấy r1 làm acceptance hiện hành của packet677. Không sửa đặc tả677 hoặc suy trạng thái GitHub từ snapshot.

`extra_checks.py` đếm trực tiếp bảng lớp của các VERDICT: bo-quet-* ở các lượt1–5; không-neo-ảnh ở2,3,4,5; thiếu-miền ở1,2,5. Các tổng lớp từng lượt khớp §9 và header. §9 nói chuyển giao blob, ngoài phạm vi Q9 cho tree, không khai đã đóng. §10 nói helper chưa có và fsck kho soạn không thay fsck lượt land. Không có khối Python bộ quét trong r6. Câu đo lại mọi con số ở §8 được đọc cùng ngoại lệ Q7 tường minh, không khôi phục cổng kiểu trước cấp.

## BẢNG ĐO

Các lệnh đo: `PYTHONDONTWRITEBYTECODE=1 python goi/measure.py`, `PYTHONDONTWRITEBYTECODE=1 python goi/extra_checks.py`, `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`; UTC nằm đầu từng log. Log của lượt hoàn tất là hiện vật được bàn giao. Lệnh suite: `review_tmp=$(cat goi/scratch-path); PYTHONDONTWRITEBYTECODE=1 TMPDIR="$review_tmp" python cay-kho/ops/lease_publish_test.py`.

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| Định danh r6 | reviewed03a7219… / d1f9dd79…244c | Khớp toàn bộ SHA/OID, bản SPEC.md bằng blob repo | Có |
| Chuỗi băm r1–r5 | Các băm header | measure.log khớp từng bản; r5 verdict ce14afd8…/hint7b4f5e06… cũng khớp sha256sum | Có |
| §1 true/yes/on/True | bool, str=True, D2=8, D1 qua | Từng dạng bool/True,8/0 | Có |
| §1 1.5/1.50 | float, str=1.5,8/qua | Từng dạng float/1.5,8/0 | Có |
| §1 0x1F/017/1_000 | int31/15/1000,qua/qua | Từng giá trị31/15/1000,0/0; A1 thêm5 cũng0/0 | Có |
| §1 date/quoted yes | date2026-09-29:8/qua; str yes:qua/qua | 8/0 và0/0 | Có |
| §1 va chạm | Sáu cặp9; khác tên0 | Đúng từng cặp, runtime.log | Có |
| §1/A3 workflow | yes0/POST0, fresh0/POST1 | Đúng; mô hình strict1/POST0 và0/POST1 | Có |
| §2 D1/D2/D3/D4 |861/949/668/1070 | extra_checks.log in đúng dòng và toán tử | Có |
| §2 D5/D6 |587/592,609/612 | Đúng, đã đổi riêng từng toán hạng | Có |
| §2 D7/D8/D9 |2110/2123;1938/1942/1946/1967;2074/2089/2139/2143 | Đúng hàm và vai trò; holder CLI tới D8 | Có |
| §2 thu hồi / packet_loop / workflow |1192 /769–771 /0 dòng | Đúng kiểm kiểu; workflow rg rc1/không output | Có |
| §8 dòng mã/test |2206/10502; test cũ10508 |2206/10502/10508 | Có |
| §8 số ca / lớn nhất |187/t192 |len(CA)=187/max192 | Có |
| Header dời nền |Mã như cũ, test+13/−19, bốn hunk |13/19, hunk nằm trong t131×2/t139/t192; cả hai tệp ứng viên bằng nền | Có |
| §8 suite nền |187/187,rc0,bỏ0 |187/187,rc0,bỏ0 | Có |
| Lịch sử185/187 |Thiếu shellcheck, t137/t159 |Môi trường hiện tại shellcheck0.9.0/actionlint1.7.7; không có log gốc môi trường ấy | KHÔNG ĐO ĐƯỢC lịch sử; không bác bằng số hiện tại |
| §8 Python/PyYAML/git lịch sử |3.11.15/6.0.1/2.43.0 |Cùng phiên bản | Có với môi trường review |
| §8 nền / shallow / replace |89fc4fa /false /0 |Đúng ba giá trị; core.abbrev7 | Có trên snapshot |
| §8 refs10:48 |Server511,cache512,heads3,thiếu0,thừa1 |Mirror513=cache513 theo tên+OID,heads1; không hỏi server | Khác ảnh/bố cục; live KHÔNG ĐO ĐƯỢC |
| Mô tả bundle refs |505 remote |Cache/mirror513 | Mô tả số đếm đã cũ; không lệch định danh đối tượng review |
| Quét tham khảo r4 |512ref=510+2;563blob/cặp/ID str |Snapshot514ref=513+1;566blob/cặp, str566, invalid[],bad_hash[] | Khác ảnh; không dùng làm cổng |
| Quét reviewer lượt5 được trích |513ref=512+1;564blob/cặp |Có đúng số ấy trong VERDICT5; snapshot hiện566 | Khớp nguồn lời khai, không phải số hiện tại |
| §8 miền retired |0blob/0cặp |0/0; live566/566 | Có trên snapshot |
| Các mốc lịch sử559/560/562, ref503/505/506/510, chênh+4/+1 |Có nhãn giờ/lịch sử |Thiếu đầy đủ map tại từng mốc | KHÔNG ĐO ĐƯỢC lịch sử; không làm tròn thành sai |
| §8 người giữ10:48–10:49 |0 cho mã,1 cho test,rc0/11 |0 cho mã,2 cho test,rc0/11; #687 và#677 | Đã trôi theo snapshot; vẫn chặn cấp đúng Q8 |
| #687 |issue687,test file,10:20Z→30-09 10:20Z |Đúng các field trên ref; còn hạn ở clock review | Có |
| #677 (bổ sung, không phải r6 khai hiện trạng) |§10 chưa đo freeze/lease |Lease revision4,10:48Z→30-09 10:48Z,giữ test,spec_hash d69178c6… | Có trên snapshot; push/live KHÔNG ĐO ĐƯỢC |
| T131 |Hết hạn08:15Z |Đúng field và thời điểm hiện tại | Có |
| Fsck kho soạn |rc0,output rỗng,13,7giây ở10:49 |Snapshot của reviewer rc0/output rỗng; UTC11:04:48→11:04:55 | Khả thi; thời lượng/máy lịch sử KHÔNG ĐO ĐƯỢC |
| §8 miền con trỏ |Vắng/null/rỗng và các dạng trắng/list/false/0 |precheck.log khớp từng trường/giá trị; ba nhóm mutant phân biệt được | Có |
| Phụ lục lịch sử28CLI/race |28CLI+1seam, riêng r3 đối chứng |Đã đọc script/log cấp; r2 trích chạy và có fixture riêng; không chạy lại toàn giàn28 | Không khai đã tự đo toàn bộ hồ sơ lịch sử |
| Fsck tree loose11/packed12 ở lượt5 |Dẫn lời reviewer5 |Khớp nguyên output trong VERDICT5 | Khớp dẫn nguồn; không tái thử ngoài phạm vi Q9 |
| Ruff |KHÔNG ĐO ĐƯỢC |python -m ruff --version rc1: No module named ruff | Đúng giới hạn, không khai lint passed |

Output snapshot và suite trọng yếu:
```text
REFS 514 LOCAL 1 ORIGIN 513 MIRROR 513 EQUAL_MAP True REPLACE 0
SCAN BLOBS 566 PAIRS 566 TYPES {'str': 566} INVALID [] BAD_HASH []
AREA ops/leases/ 566 566
AREA ops/leases_retired/ 0 0
HOLDER ops/lease_publish.py 0 NGƯỜI_GIỮ 0: không có ACTIVE [] STDERR 
HOLDER ops/lease_publish_test.py 11 NGƯỜI_GIỮ 2: dot-bien-l-bien-cong-khai-exec-1-claude-20260929, lease-publish-windows-do-r1-g1-claude ACTIVE ['CÒN_HẠN\tlease-publish-windows-do-r1-g1-claude\trefs/remotes/origin/claude/lease-publish-windows-do:ops/leases/lease-publish-windows-do-r1-g1-claude.yaml', 'CÒN_HẠN\tdot-bien-l-bien-cong-khai-exec-1-claude-20260929\trefs/remotes/origin/ops/cap-lease-677:ops/leases/dot-bien-l-bien-cong-khai-exec-1-claude-20260929.yaml'] STDERR 
LEASE_687 {'packet_issue': 687, 'write_set': ['ops/lease_publish_test.py'], 'leased_at_utc': '2026-09-29T10:20:00Z', 'lease_expires_at_utc': '2026-09-30T10:20:00Z'}
T131 2026-09-29T08:15:00Z
lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0

suite_rc=0
```

## CHI TIẾT TỪNG LỚP

Không có lớp P1/P2/P3 còn mở trong **hợp đồng r6** sau các phép kiểm trên. Các nhãn lịch sử ở bảng đối chiếu vẫn được giữ: CHUYỂN GIAO không phải helper đã đạt, NGOÀI PHẠM VI không phải tree/commit đã được helper sửa.

Rủi ro quyết định, không xếp hạng:

- Q7 vẫn có cửa sổ trước land dùng runtime cũ; r6 đã ghi rủi ro bia mộ int. Không đề nghị thêm cổng quét trước cấp.
- Q9 chấp nhận fsck không nguyên tử với scan. Không dựng thêm finding vì tree/commit hỏng lọt helper; không yêu cầu băm toàn chuỗi.
- Hướng6 cho thấy so tên nhánh không chứng minh cache cùng OID. Không nhận tên bằng là ảnh mới, không bỏ bước fetch/đo lại. Phép đo là fixture riêng, không cáo buộc nguồn đang stale.

## DRY-RUN HINT.patch

`HINT.patch` rỗng vì không có lớp cần gợi ý sửa. Không tạo hunk giả để có patch. Không sửa r1–r6 hoặc đưa lại code bộ quét vào đặc tả.

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

Lệnh đã chạy (R là đường tuyệt đối được giao):
```sh
review_hint_tmp=$(mktemp -d -p "$R")
cp -a "$R/cay-kho" "$review_hint_tmp/cay"
patch -d "$review_hint_tmp/cay" -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output thật:
```text
Hmm...  I can't seem to find a patch in there anywhere.
dry_run_rc=0
```
Mã0 ở đây chỉ là hành vi GNU patch với input rỗng, không là bằng chứng hunk nào đã áp. Số byte được kiểm bằng `wc -c goi/HINT.patch` và kiểm cuối.

## GIỚI HẠN VÀ TOÀN VẸN

Chưa đo: GitHub live/bytes thân Mission682, exact model/effort do máy chứng nhận, ứng viên/helper thật, Windows, bare Ruff/delta F, timeout/OS kill/OOM và toàn bộ không gian YAML/object-store. Không có việc đăng GitHub, cấp lease, merge hoặc land. Nguồn chính xác là SHA/OID trong header; ảnh mirror khác thời điểm so với kho soạn đã được tách riêng.

Các lỗi giàn đã sửa trước khi lấy kết luận: parser ref ban đầu dùng strip() làm mất cột symref cuối; fixture A6/A7 chưa cấu hình origin cục bộ nên trả12; object Git fixture có mode read-only nên thay file bằng unlink/recreate trong chính kho tạm. Không dùng các lỗi setup ấy để tính finding hoặc tín dụng giết mutant. Các log bàn giao là lần chạy hoàn tất sau sửa.

Sandbox thực tế workspace-write; giữ checkout/mirror read-only bằng giới hạn đường ghi, PYTHONDONTWRITEBYTECODE=1 và TMPDIR dưới R. Snapshot băm regular files (gồm metadata Git, tracked/untracked/ignored) đầu/cuối chỉ chứng minh không có delta quan sát được tại hai mốc; không khẳng định mọi syscall của cả phiên. Symlink được so đích riêng ở kiểm cuối nếu có. Băm hiện vật bàn giao ghi ngoài chính chúng.

Kiểm cuối: `PYTHONDONTWRITEBYTECODE=1 python goi/verify.py`:

```text
UTC 2026-09-29T11:14:16.762615+00:00
SOURCE_FILES 3016 3016 DELTA []
SYMLINKS {}
HEAD 03a7219c9f3df4e6304f499b79df968aa7d386cb
TREE e692d52c82adffadec70ef5f6ac4b0360423c7e2
SPEC_BLOB_MATCH True
VERDICT verdict: approve
CLASSES []
HUNTS ['1', '2', '3', '4', '5', '6']
HINT_BYTES 0
DRY_RUN Hmm...  I can't seem to find a patch in there anywhere.
dry_run_rc=0
COPY_R6_EQUAL True
SUITE lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0
VERIFIED
```
