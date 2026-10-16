verdict: changes_requested
reviewed_sha: 61b4c24936a478b80f124ac11dea0ce126c842a0

**KHÔNG CÒN P1 · KHÔNG CÒN P2 · CÒN 4 P3: 2 lỗi hồ sơ lớp B và 2 nợ D.** Lỗi F lượt 16 đã vá thật, kể cả phép đo mới về chính bản vá. Hai nợ D không chặn `approve` một mình. Lý do yêu cầu sửa là câu mô tả workflow hiện hành trong thân PR và bản chiếu cặp mẫu CI trong README còn chắc hơn nguồn; không phải độ dài bản vá hay việc không có log GitHub.

Reviewer: Codex/GPT-6 theo cấu hình phiên; provider OpenAI, execution surface agent API có shell cục bộ, transport machine; khác provider executor Claude theo chỉ thị giao việc. Không chứng thực độc lập backend/model phục vụ, không tự ghi transition `cross_approved` hoặc cấp quyền merge. Chỉ thị trực tiếp lượt 17 là authority cho phạm vi và điều kiện dừng này.

Base tự đo: `26e2555d36c48b3c0f625ae50ab2cfb62b6cb858`; tree: `bd4cafcb0d662cb6a13decd1edd7d15931263fe4`. `cay-kho/` giữ read-only; cổng chạy trên `review17-current/`, phép thử trên `review17-probe/`. Tất cả scratch và TMPDIR trong workspace; không mạng, không tự soạn payload đường dẫn. Tắt pycache, ghim `core.abbrev=7`, thêm **thư mục** actionlint 1.7.7 vào **cuối** PATH. Các đường dẫn kho dưới đây tính từ `cay-kho/`.

Bằng chứng tự chạy: [measurements.json](review17-evidence/measurements.json), [gates.json](review17-evidence/gates.json), [probes.json](review17-evidence/probes.json), [doc-checks.json](review17-evidence/doc-checks.json). Script tái lập và stdout/stderr từng lệnh nằm cùng thư mục. Hai trục đã kiểm: yêu cầu/phạm vi và tính đúng, nhất quán của hồ sơ cùng hợp đồng cổng.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `so-do-va-toi-gian-khong-khop-diff-cuoi`: **ĐÃ VÁ THẬT** — CHANGELOG:1619–1623 neo đính chính vào `95071a1`. Tự chạy `git diff --numstat d47ea59 95071a1`: CHANGELOG **19/8**, manifest **5/5**, tổng **2 tệp,+24/−13**. Cắt r360 từ heading đến ngay trước heading kế tiếp, gồm dòng trống: **654→665 (+11)**. Message `e880b6a` cũng ghi đúng các số này. Kiểm riêng `git diff --numstat e880b6a~1 e880b6a`: CHANGELOG **8/1**, manifest **5/5**, tổng **2 tệp,+13/−6**; r360 **665→672 (+7)**. Không sinh lỗi F mới. Nguyên nhân “ảnh chụp giữa chừng” là tự thuật của executor; Git xác minh được sai số cũ và số cuối đúng, không tái dựng được thời điểm đo bản nháp.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — mã không đổi so cả `95071a1` và base mới. Tự tạo ba đột biến văn bản độc lập, mỗi cái đúng một byte, giữ kích thước **961940 byte**: heading r358 `1016→1017`, heading r360 `5→6`, phép trừ `13 − 2 = 11→12`. Cả ba: claims **rc0/ok=true/flags=[]**; release **rc2/ok=false**, failed chỉ CHANGELOG. Control xanh. Giữ nợ D.
- `cong-receipt-chua-dinh-nghia-cay-dang-merge`: **CHƯA VÁ** — `_neo_git` vẫn kiểm ancestry với HEAD, `kiem` đọc tệp trên đĩa. Giữ từng cây merge lịch sử và đổi HEAD cha1/merge: **6/1/4/2/11 vi phạm, rc1 → 0/0/0/0/0, rc0**. Đây là phép A/B trên cây đã giải được lưu trong Git, không giả nhận log năm lần merge chưa commit. Không suy thành mọi merge pending đều đỏ. Giữ nợ D.

Tổng ba slug: **1 ĐÃ VÁ THẬT · 0 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 2 CHƯA VÁ**. Hai finding B bên dưới độc lập với sửa F; lỗi README đã có từ trước, không quy là do `e880b6a` sinh ra.

## CỔNG DUYỆT ĐÃ BỊ GỠ — HỒ SƠ CÓ THEO KỊP KHÔNG

`ls .github/workflows/` còn đúng sáu tệp: `ci.yml`, `launcher-windows.yml`, `ops-don-ref.yml`, `ops-open-pr.yml`, `ops-publish-lease.yml`, `ops-thu-hoi-admission.yml`. Cả hai workflow duyệt đều vắng. `git log --oneline 4b5184e..26e2555` có `1e36bb4` (gỡ cổng), `88e89b3` (vá hồ sơ rút cổng), `26e2555` (merge #506). `git log --diff-filter=D` chỉ đúng commit gỡ `1e36bb4`; cả hai tệp có tại `2ec6171` của PR #491.

**Câu 1 — Có một mô tả chưa theo kịp trạng thái hiện hành:** `than-pr-493.md:111` còn “gỡ draft thì CÓ bắn `duyet-khac-danh-tinh.yml`, vì tệp ấy khai … Hai workflow cùng kho”. Mục này giải thích điều kiện CI nhưng không ghim câu ấy vào cây lịch sử và không nói workflow đã bị gỡ. Đây là finding B thứ nhất. Không suy từ việc gỡ tệp rằng mọi cấu hình required checks trên GitHub đã được gỡ: phần đó **KHÔNG ĐO ĐƯỢC** offline, runbook mới cũng giữ giới hạn này.

Đã vét cả dòng lẫn ngữ cảnh ở những nơi sau (các hit lưu trong `doc-checks.json`):

| hiện vật | kết quả phân loại |
|---|---|
| `ops/land/pr491-r358-ghi-so-land-evidence.yaml`, toàn tệp | `authorization_ghi_chu`, `uy_quyen`, `pre_merge_checks` nói về approve/merge PR #491 ở `2ec6171`/`00e017a`, các run cụ thể; là lịch sử có nhãn GitHub attestation |
| `ops/reviews/pr491-review-1-codex-verdict.receipt.yaml`, toàn tệp | Không viện workflow duyệt để chứng nhận cross-review; assurance khai provider, anchor là Git |
| `ops/reviews/pr491-review-2-codex-verdict.receipt.yaml`, toàn tệp | Như lượt 1; “Draft marked ready” là nguồn thuật lại sự kiện bot lịch sử, không là điều kiện merge hiện tại |
| `ops/reviews/README.md`, cả hai bảng và prose | Các hàng PR #492/#500 có `cong` đỏ **khi merge**, ghim PR/head; lịch sử. Hai hàng PR #491 không dùng workflow làm bằng chứng provider. Vấn đề cặp mẫu CI được ghi riêng bên dưới |
| r360, toàn mục | :1132–1134 nói “Đo được **cùng đợt**” sau câu hai P2 PR #491 vá trước merge; đọc là phép đo lịch sử. :1136–1143 ghim các run trước/sau approve và có nhãn (b); không yêu cầu xoá chuyện cổng từng tồn tại |
| r364/r363/r362/r359/r358 | Các đoạn `cong` của #500/#492 gắn “lúc merge”, PR/commit cụ thể; không biến chúng thành lời khai về cổng hiện tại. r362 không có lời khai mới rằng workflow duyệt đang sống |
| Thân PR, toàn bộ | Phần Land: lịch sử PR #491 có nhãn. Dòng111 trong phần giải thích CI còn trình bày tệp đã gỡ như cấu hình dùng được hiện nay |
| `thong-diep-commit.txt`, toàn bộ 1044 dòng | Message lịch sử ghim từng commit, không thấy message mới dùng cổng đã gỡ làm điều kiện approve PR #493. Bản trích khớp byte Git range base..HEAD |

**Câu 2 — Có phụ thuộc làm bằng chứng, nhưng ở hồ sơ land lịch sử:** `land-evidence.yaml:30–34` gọi cổng là “phép đo độc lập” của điều kiện khác danh tính; :48–54 thuật lại việc đợi approve rồi merge. Không trả lời “không có phụ thuộc” một cách tuyệt đối. Đây là bằng chứng **được thuật lại cho PR #491**, đã có nhãn thiếu raw response; việc gỡ workflow sau đó không phủ định một lần chạy trước đó. Không tìm thấy lời kết luận PR #493 “đã duyệt khác danh tính” hoặc `cross_approved` dựa vào cổng này. Không nâng attestation lịch sử thành xác thực danh tính thật của reviewer hay authorization cho SHA lượt 17.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence:** đã đọc từng nhóm trường, không dùng YAML parse thành bằng chứng sự kiện.

| trường/nhóm | phép đo, hạng nguồn và kết quả |
|---|---|
| `p1_theo_luot: {1:3,2:0}`; `luot_cuoi` | Parse heading finding: verdict1 **3/5/6 =14**, verdict2 **0/3/10 =13**; khớp |
| `doi_chieu_luot_truoc` | Parse 14 dòng slug verdict2: **7/1/0/6**; cả ba slug P1 verdict1 thuộc ĐÃ VÁ THẬT |
| `authorized_head_sha`, reviewed SHA cuối, `khop_head_da_merge` | Cùng **2ec6171f7a2e21ae950633f9e328329a355f7a6d**, bằng cha2 `00e017a`; quan hệ Git khớp. Không chứng minh approval từ cha merge |
| “land evidence thứ bảy” | `git ls-tree -r --name-only 00e017a ops/land/`: **6 tệp** trước khi thêm; khớp |
| `schema_version`, mission/generation, provider/role/session/recorded_by | Metadata khai báo hồ sơ; không phải chứng thực độc lập identity/generation runtime |
| Approver, authorization URL, merged_at/operator, run/job/bước/thời lượng, bot, trạng thái Issue/PR | Thuộc nhãn GitHub **ATTESTATION** đầu tệp và các giới hạn tại trường; **KHÔNG ĐO ĐƯỢC** độc lập vì không có response thô và không mạng |
| `land_operator_neo.uy_quyen` | Trích chỉ thị trong phiên và nhận rõ không URL bền cho chỉ thị ấy; **KHÔNG ĐO ĐƯỢC** transcript gốc |
| `pre_merge_checks[0]` | Nhãn riêng phân biệt rc/duration/worktree/số mục bẩn từ launcher `run.json` ngoài kho (**ATTESTATION**) với 0 P1 và SHA (**đếm/Git**). Không mất nhãn |
| Các kết quả cổng lịch sử 121/121, 41 v2/tổng94 | Chú thích nhận thiếu stdout gốc; chạy lại được không đồng nghĩa xác thực lần chạy cũ. Số hiện tại146/120 không bác số lịch sử |
| Bookkeeping: sửa hai P2 thân PR, đọc ngược 0 dòng lệch | GitHub attestation; thiếu body/readback gốc. `ci.yml` và workflow thu hồi là hai cấu hình/event khác nhau; không lấy tệp này chứng minh event thực tế đã chạy |
| Số11 lúc merge | Tái lập được **13−2=11**, với điều kiện nhận hai sửa body được thuật lại. **KHÔNG ĐO ĐƯỢC số finding thật còn sống tại thời điểm merge** |

Không phát hiện thêm trường sự kiện trong **land evidence** bị nâng hạng mà thiếu nhãn. Việc này không bảo đảm mọi bản chiếu bên ngoài nó đúng: README có lỗi độc lập bên dưới.

**Hai verdict nguyên văn:**

| tệp | byte tự đếm | SHA-256 tự băm | lịch sử |
|---|---:|---|---|
| `pr491-review-1-codex-verdict.md` | 35088 | `38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c` | 0 commit M; blob A = HEAD |
| `pr491-review-2-codex-verdict.md` | 36958 | `14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468` | 0 commit M; blob A = HEAD |

Cả hai khớp byte/băm biên nhận. `git log --diff-filter=M --format=%H -- <tệp>` rỗng; commit thêm duy nhất là `34e9d35be0fc52406e3659bfc24c388bf54262cd`. Không có byte bị sửa kể từ lúc nhập Git trong lịch sử được giao; không chứng thực giai đoạn trước nhập kho.

**Hai biên nhận v2:** gọi riêng `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()` và `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()` đều **PASS**, rc0. Suite đầy đủ **146/146, chạy146, bỏ0**, rc0. Mỗi cặp verdict/receipt có trong mục lục; **4+5 =9** ID đều có đúng một hàng cảnh báo gắn đúng verdict.

| lượt / caveat ID | đối chiếu nội dung |
|---|---|
|1 / `HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE`|ba4a258 khác2ec6171; khớp hai header và cha merge|
|1 / `SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1`|Đếm sáu heading P3: năm về độ phủ, một về giới hạn cổng; khớp|
|1 / `MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU`|Nguồn tự khai model, không có chứng thực backend; caveat giữ giới hạn đó. Model yêu cầu từ launcher là attestation|
|1 / `phan-cong-CAM-tu-soan-phan-chung`|Khớp giới hạn phân công; không biến thiếu finding thành độ phủ đầy đủ|
|2 / `changes_requested-KHONG-phai-chua-dat-dieu-kien-dung`|Khớp nguyên văn dòng4:0 P1 đủ điều kiện lịch sử, vẫn changes_requested|
|2 / `HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge`|13 tại review tự đếm được;11 khớp số học có điều kiện. ID không phải phép đo số thật lúc merge|
|2 / `NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI`|Biên nhận liệt kê5, cờ mới3/trùng2; hai slug trùng nối được verdict. Đây là báo cáo bot bổ sung do điều phối thuật lại, không phải5 heading trong verdict gốc; sự kiện bot KHÔNG ĐO ĐƯỢC offline|
|2 / `MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU`|Cùng giới hạn model như lượt1|
|2 / `phan-cong-CAM-tu-soan-phan-chung`|Nguồn nói không soạn payload; có thuật lại các mutant văn bản và vắng công cụ; khớp phạm vi|

Không đổi “11” thành “13” khi không có bằng chứng bác hai sửa body. Biên nhận2 `dieu_kien_dung_da_thoa.khong_suy_rong` và README hàng mục lục321 đã nói rõ số11 dựa vào attestation. **Đính chính đánh giá lượt16:** không tìm thấy một đoạn nhãn nguồn riêng phủ toàn nhóm PR491 ở đầu bảng README như verdict trước nói; nhãn cho số11 thực tế nằm trong hàng mục lục và biên nhận. Vì vậy không dùng nhận xét tổng quát cũ để miễn vét các trường khác của README, đặc biệt cặp mẫu CI ở hàng322.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/base |61b4c24/26e2555|Full OID đầu verdict; ancestry rc0|Có|
| First-parent base..HEAD |Lượt vá + merge master6|26 commit; hai mới sau95071a1 làe880b6a và61b4c24|Có|
| Toàn PR |numstat.txt|**8 tệp,+1826/−26**|Có; numstat/diff bằng byte Git|
| Delta lượt16→17, gồm merge |patch giao|**8 tệp,+26/−1716**|Có|
| Phần sửa findings |e880b6a:2 tệp,+13/−6|CHANGELOG8/1; manifest5/5|Có|
| Phần merge master6 |master không đụng8 tệp PR|**6 tệp,+13/−1710**, bằng byte diff4b5184e..26e2555|Có, tách khỏi phần vá|
| Phạm vi master trong EVIDENCE |“chỉ .claude/dev/** và .github/workflows/**”|Còn **ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md +13/−0**|Không; sai mô tả gói, không lẫn vào diff PR hay mở finding kho riêng|
| Đính chính95071a1 |24/13;19/8;654→665|Đúng cả ba|Có|
| Phép đo chính e880b6a |13/6;8/1;665→672|Đúng cả ba|Có|
| r360 tại reviewed SHA |672 dòng|Heading1031, heading kế1703;672|Có|
| Sáu heading r đầu |Không va chạm|r364/r363/r362/r361/r360/r359 tại1/98/199/845/1031/1703|Có|
| Mục master giữ nguyên |Không nuốt nội dung|r364/r363/r362/r361/r359 bằng byte base|Có|
| Năm slice |Theo heading thật|97/646/672/120/233 dòng cho r364/r362/r360/r359/r358;5/5 bằng byte|Có|
| Bản chép YAML/README/workflow |Từ cây|6/6 bằng byte HEAD|Có|
| 16 hàng bảng lượt |SHA/verdict/severity/đối chiếu|Parse từng verdict,16/16 khớp mọi ô|Có, chi tiết dưới|
| Năm receipt THÊM MỚI |6/1/4/2/11|Lọc `--diff-filter=A` và `.receipt.yaml`:6/1/4/2/11|Có|
| Năm A/B ancestry |6/1/4/2/11→0|Tự chạy khớp từng cây|Có trong năm ca|
| Hai verdict PR491 |35088/36958, băm ghim|2/2 băm+byte khớp,0 commit M|Có|
| P1 PR491 |3/0|Heading3/0; tổng14/13|Có|
| Chín caveat |4+5, t26/t27 đạt|9 ID đúng hàng; hai ca PASS|Có về liên kết/băm, không xác thực số11|
| Workflow duyệt hiện tại |Body:gỡ draft có bắn|Cả2 workflow vắng, đã gỡ ở1e36bb4|Không, B|
| Cặp mẫu CI trong README |“thuộc run34176439015”|Nguồn chỉ “được cho là”, thiếu response cùng job/attempt|Không, B|
| Toàn vẹn gói |ARTIFACTS.sha256|**3361/3361**,0 lệch|Có; không chứng thực provenance|
| Bảng khẳng định |3564 dòng|11 input tái sinh bằng byte;3564 dòng dữ liệu không rỗng,2201 có số,3588 dòng vật lý cả khung|Có theo đơn vị đã khai|
| Ref snapshot |330/330/330,lệch0|Ba TSV bằng byte,local heads330|Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC|
| Message trích |Range26e2555..HEAD|Bằng byte `git log --format=%H%n%B%n---`|Có về vận chuyển|
| `python3 -B ops/bien_nhan_v2.py` |67 v2/tổng120,sạch|rc0;67+11 legacy+42 nợ=120;0 vi phạm,0 KHÔNG ĐO ĐƯỢC|Có|
| `python3 -B ops/lease_publish_test.py` |146/146|rc0;146/146,chạy146,bỏ0|Có|
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` |180/180,ok|rc0;180/180,hai hash match=true;failed/extra/required_missing/errors=[]|Có|
| `python3 scripts/tl.py doc-claims-check --strict --json` |ok|rc0;ok=true,106 tệp,flags=[],370 advisory|Có trong hợp đồng|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` |sạch|rc0;7 tệp,0 chỗ chép doctrine|Có|
| `python3 .claude/dev/packet_loop.py adr-song --root .` |sạch|rc0;46 ADR/46 hàng,khớp1–1;tha trạng thái0016|Có|
| Ba mutant một byte |Nợ claims còn|claims3/3 xanh,release3/3 đỏ chỉCHANGELOG|Có, nợ D|
| Mã hai nợ D |Ngoài write set|Diff so base mới và95071a1 đều rỗng|Có|
| CI/approval thật,11 lúc merge |Thuật lại|Thiếu raw response/body/run và không mạng|KHÔNG ĐO ĐƯỢC|

Cột đối chiếu được parse **từ các dòng slug trong mục ĐỐI CHIẾU của từng verdict**, không từ câu tổng kết hay số trong bảng r360. Thứ tự bốn số: **ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ**. SHA và verdict đọc từ header; severity chỉ đếm heading finding. Hàng5 theo dõi cả slug đã đóng nên tổng đối chiếu không phải số finding còn sống.

| lượt | P1/P2/P3 tự đếm | bốn trạng thái tự đếm | tổng slug | ô SHA/verdict/severity/đối chiếu r360 |
|---|---|---|---:|---|
|1|1/4/12|—|—|Khớp từng ô|
|2|1/4/15|0/6/0/11|17|Khớp từng ô|
|3|0/2/15|7/3/0/10|20|Khớp từng ô|
|4|0/1/15|1/2/0/14|17|Khớp từng ô|
|5|0/0/14|3/0/1/13|17|Khớp từng ô|
|6|0/0/10|11/2/0/1|14|Khớp từng ô|
|7|0/0/9|4/3/2/1|10|Khớp từng ô|
|8|0/0/10|7/0/1/1|9|Khớp từng ô|
|9|0/0/5|7/2/0/1|10|Khớp từng ô|
|10|0/0/3|3/1/0/1|5|Khớp từng ô|
|11|0/0/2|2/0/0/1|3|Khớp từng ô|
|12|0/0/3|1/0/0/1|2|Khớp từng ô|
|13|0/0/2|2/0/0/1|3|Khớp từng ô|
|14|0/0/4|0/0/1/1|2|Khớp từng ô|
|15|0/0/5|1/0/1/2|4|Khớp từng ô|
|16|0/0/3|3/0/0/2|5|Khớp từng ô|

### than-pr-con-mo-ta-workflow-da-go-nhu-dieu-kien-hien-hanh  [P3]  Thân PR vẫn hướng dẫn rằng gỡ draft sẽ kích hoạt workflow đã bị xoá
LỚP: B
TỆP/DÒNG: `than-pr-493.md:111`; nguồn hiện hành `.github/workflows/` và `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md:3–15`.
VẤN ĐỀ: Câu “nhưng gỡ draft thì CÓ bắn … vì tệp ấy khai … Hai workflow cùng kho” không có mốc Git/lịch sử cho cấu hình này. Sau merge master6, tệp ấy không còn trong cây. Người đọc phần giải thích CI của PR đang mở sẽ nhận sai điều kiện hiện hành. Nhãn attestation phần Land không sửa được sự lệch này: nó phủ một phần khác và không nói workflow đã bị rút. Chỉ cần ghim phép đo cũ vào `2ec6171` và nói đã gỡ ở `26e2555`; không cần bỏ lịch sử hay khôi phục cổng.
CÙNG LỚP CÒN Ở ĐÂU: r360:1132–1134 có cùng câu nhưng nối rõ “Đo được cùng đợt” vào lần sửa body PR #491; tôi đọc đó là lịch sử, không đếm thêm một lỗi. Các đoạn cổng đỏ/xanh trong land evidence, r364/r363 và các message là lịch sử ghim PR/commit/run; không chấm việc chúng vẫn còn nhắc cổng.
ĐÃ THỬ VÁ: có — bản gợi ý ngoài kho [than-pr-hint.md](review17-evidence/than-pr-hint.md) thay đúng một gạch đầu dòng, ghi cấu hình ở `2ec6171` và việc gỡ ở `26e2555`. Chưa áp lên PR thật. Nguy cơ vá: nói rộng thành GitHub đã gỡ required checks/approval rules; bản gợi ý chỉ nói tệp trong kho đã gỡ.
ĐÃ THỬ NGHIỆM: `python3 -B review17-evidence/doc_checks.py`: hai `cat-file -e 2ec6171:<workflow>` rc0; hai đường dẫn HEAD không tồn tại; log D đều chỉ `1e36bb4`. Bản gợi ý không còn câu cũ và có mốc mới. Ca khoá nội dung: mô tả lịch sử phải ghim cây còn tệp; mô tả hiện hành không được khẳng định tệp đã xoá vẫn chạy. Không gọi API nên chưa áp/đọc ngược body GitHub.
ĐỘ TIN: cao về trạng thái tệp; vừa về mức nhập nhằng của câu trong thân PR

### readme-pr491-luot1-chieu-cap-run-van-mat-gioi-han-nguon  [P3]  Mục lục còn gán chắc cặp mẫu CI cho một run dù nguồn giữ giả định
LỚP: B
TỆP/DÒNG: `ops/reviews/README.md:322` (bản chép `reviews-README.md:322`); nguồn `ops/land/pr477-dung-goi-review-land-evidence.yaml:157–166`; bản chiếu đã sửa `ops/reviews/pr491-review-1-codex-verdict.receipt.yaml:56–65`.
VẤN ĐỀ: Hàng mục lục viết “cặp 43/1→44/6 thuộc run `34176439015`”. Nguồn chỉ thuật lại “hai mẫu **được cho là** của cùng một job thuộc run”, và nói thiếu response trước/sau để kiểm job/attempt/danh sách bước. Biên nhận1 đã khôi phục đúng giới hạn ấy từ lượt13; README vẫn bỏ nó. Nhãn “ATTESTATION — toàn bộ khối runtime” ở cuối hàng liệt kê thời lượng/model/effort từ `run.json`, không phủ cặp mẫu GitHub này và không phục hồi giả định về cùng job. “CHƯA XÁC ĐỊNH” trước đó nói về **nguyên nhân**, không về việc đã xác thực danh tính hai mẫu. Không khẳng định cặp run là sai; lỗi là bản chiếu chắc hơn nguồn.
CÙNG LỚP CÒN Ở ĐÂU: Receipt1 đã đúng; r358 giữ “được cho là”, r360:1529–1535 kể chính bài học này và nhận biên nhận2 đã chỉ ra nó. Bảng khẳng định trích nguyên hàng README nên mang theo câu chưa sửa; không đếm đó thành finding riêng. Đây là một vị trí cũ bị các lượt trước bỏ sót, không phải sửa F lượt17 làm phát sinh.
ĐÃ THỬ VÁ: có — trên `review17-probe/`, thay đúng đoạn cặp mẫu của hàng322 bằng lời thuật lại có “được cho là” và giới hạn thiếu response cùng job/attempt; giữ các số, heading, verdict gốc và caveat ID. [readme-hint.patch](review17-evidence/readme-hint.patch) là gợi ý **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nguy cơ vá: xoá hết số lịch sử hoặc gán mọi trường trong hàng thành attestation, làm hạ hạng các số Git/P1 đếm được; bản gợi ý chỉ sửa cụm liên quan.
ĐÃ THỬ NGHIỆM: `python3 -B review17-evidence/doc_checks.py` kiểm neo cũ xuất hiện đúng1 lần; sau thay, gọi riêng t26/t27 **rc0, PASS**. Đối chiếu văn bản nguồn :157–166 với receipt1 :56–65 xác nhận hai nơi cùng giữ giả định và giới hạn còn thiếu ở README. Ca khoá kế nhiệm: mọi bản chiếu cặp mẫu phải giữ hạng nguồn/giả định, trong khi số finding và băm verdict không thay. t26/t27 xanh chỉ xác nhận không làm hỏng liên kết/băm, không chứng minh lịch sử CI.
ĐỘ TIN: cao

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Claims chưa kiểm ba đại lượng nội dung đã có phản chứng
LỚP: D
TỆP/DÒNG: `scripts/tl_core/workflow.py:1163`, :1430; các điểm đột biến `CHANGELOG.md:1823`, :1031, :1352.
VẤN ĐỀ: Claims cho cả ba số sai qua, release chỉ bắt sai byte với manifest. Ngoài write set hồ sơ, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: Ba nhóm đại lượng đã đo; không suy mọi câu hoặc mọi lớp đầu vào đều lọt.
ĐÃ THỬ VÁ: không — cần packet cổng riêng, khai đại lượng/nguồn đếm có cấu trúc. Tránh hardcode ba chuỗi hoặc làm đỏ cả câu lịch sử đang trích để bác. Ca khoá: control xanh, từng số bị đổi đỏ ở cổng nội dung.
ĐÃ THỬ NGHIỆM: `python3 -B review17-evidence/probes.py`: mỗi mutant1 byte, kích thước961940 giữ nguyên; claims3/3 rc0/ok=true, release3/3 rc2/ok=false/failed chỉCHANGELOG. Mã hai cổng không đổi so base mới và reviewed SHA lượt16; control tại HEAD xanh.
ĐỘ TIN: cao

### cong-receipt-chua-dinh-nghia-cay-dang-merge  [P3]  Cổng đọc cây trên đĩa nhưng ancestry chỉ xét HEAD
LỚP: D
TỆP/DÒNG: `ops/bien_nhan_v2.py:808–824`, :861.
VẤN ĐỀ: Nội dung candidate trên đĩa có thể khác HEAD trước khi merge được commit. Cùng cây đã giải, thay HEAD cha1/merge đổi kết quả. Đây là nợ hợp đồng đầu vào cho trạng thái dở, không phải bằng chứng ancestry của commit đã chốt đang bị kiểm sai. Ngoài write set, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: Năm cây `7e236cf`, `dd4a3ae`, `9e78e19`, `e921131`, `f618e01`; không mở rộng thành mọi merge pending.
ĐÃ THỬ VÁ: không — packet kế nhiệm cần ràng buộc candidate commit/tập cha với nội dung đang kiểm hoặc trả chưa đo được khi thiếu hợp đồng. Không thay HEAD bằng tree hash vì tree không có ancestry. Nguy cơ vá: mở rộng vô điều kiện tập tổ tiên khiến nhánh không liên quan qua; ca khoá phải giữ chặn nhánh ấy và phân biệt thiếu object.
ĐÃ THỬ NGHIỆM: `python3 -B review17-evidence/probes.py` giữ đĩa mỗi cây merge, đổi riêng HEAD cha1/merge: **6/1/4/2/11 → 0/0/0/0/0**, rc1→0 cả5. Đây là thí nghiệm A/B cấu tạo trên bản sao, không transcript MERGE_HEAD lịch sử. Không cần chạy lại toàn bộ phạm vi ứng dụng để xác nhận mã cổng không đổi.
ĐỘ TIN: cao về hành vi; vừa về thiết kế kế nhiệm

Kiểm cuối: giữ nguyên `cay-kho/` tại reviewed SHA, status rỗng; băm lại hiện vật gốc ghi trong [final-check.json](review17-evidence/final-check.json). Kết luận có **0 P1 / 0 P2 / 4 P3**, gồm **2 B + 2 D**. Không yêu cầu sửa hai nợ D trong PR hồ sơ này; hai sửa hồ sơ B đều có thể làm ngắn, không cần thêm tự sự chiến thuật.
