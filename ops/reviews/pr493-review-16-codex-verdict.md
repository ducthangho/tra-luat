verdict: changes_requested
reviewed_sha: 95071a19670dee33630286a84af6caf5a47d8524

**KHÔNG CÒN P1 · KHÔNG CÒN P2 · CÒN 3 P3: 1 lỗi kiểm kê mới lớp F và 2 nợ D.** Ba lỗi hồ sơ F/C/E của lượt 15 đã được sửa. Lý do chưa approve là số đo bản vá trong **thông điệp commit mới** vẫn sai; hai nợ D không chặn approve một mình.

Reviewer: Codex/GPT-6 theo cấu hình phiên; provider OpenAI, execution surface agent API có shell cục bộ, transport machine; khác provider executor Claude theo chỉ thị giao việc. Không chứng thực độc lập backend/model phục vụ; không ghi transition `cross_approved` hoặc cấp quyền merge. Authority là chỉ thị trực tiếp cho lượt 16, điều kiện dừng tới P3 và ngoại lệ hai nợ D.

Base: `4b5184e21373eb8f8a36493d0282ebd020bb4458`; tree: `823ab74f5c31580f5f43629571ecb0fb5136cf18`. Chỉ thao tác trong workspace, không mạng, không tự soạn payload đường dẫn. `cay-kho/` giữ read-only; các cổng chạy trên bản sao `review16-current/`, đột biến và A/B lịch sử trên `review16-probes/`. TMPDIR nằm trong workspace, tắt pycache; `core.abbrev=7`; thêm **thư mục** actionlint 1.7.7 vào cuối PATH.

Bằng chứng tự chạy và script tái lập: [measurements.json](review16-evidence/measurements.json), [gates.json](review16-evidence/gates.json), [probes.json](review16-evidence/probes.json), [extra.json](review16-evidence/extra.json), [extra-git.json](review16-evidence/extra-git.json), [pending.json](review16-evidence/pending.json). Stdout từng cổng và mutant ở cùng thư mục. Đường dẫn kho dưới đây tính từ `cay-kho/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `phan-chung-bon-tren-nam-dem-receipt-sua-thanh-them`: **ĐÃ VÁ THẬT** — CHANGELOG:1598–1615 đổi tiêu đề cột sang receipt **THÊM MỚI (`--diff-filter=A`)**, ô lần 2 thành 1 và rút phản chứng 4/5. Tự đếm cả hai cách: receipt thay đổi = **6/2/4/2/11**, receipt thêm mới = **6/1/4/2/11**. Tại `dd4a3ae`, lượt 7 là A, lượt 6 là M. A/B năm cây cho lỗi ancestry **6/1/4/2/11**, sau ghim HEAD vào merge đều 0. Lý do mới “năm ca không làm nên luật” đứng vững theo nghĩa năm quan sát chưa chứng minh mệnh đề phổ quát; nó không còn khẳng định đã bác đẳng thức bằng một ca trong mẫu. Message mới cũng rút rõ phản chứng cũ. Lỗi F mới ở phép đo kích thước bản vá là đại lượng khác, ghi riêng; không coi việc cùng lớp là bằng chứng finding receipt cũ chưa đóng.
- `doi-chieu-luot14-trong-message-doi-sinh-loi-thanh-va-that`: **ĐÃ VÁ THẬT** — CHANGELOG:1617–1620 neo đính chính `d47ea59`, gọi đúng slug và đúng bốn số **0/0/1/1**. Tự parse đúng hai dòng slug trong mục đối chiếu của verdict 14; hàng 14 r360 và message mới cùng khớp. Hai số 1/0 cũ chỉ còn được trích để bác hoặc nằm trong lịch sử được đính chính.
- `no-cong-bi-khai-thanh-moi-merge-pending-deu-do`: **ĐÃ VÁ THẬT** — CHANGELOG:1621–1622 và message mới rút chữ “mọi”, giới hạn phép đo vào năm ca. Đính chính ngắn này đủ đóng lượng từ sai, không cần thêm bài giải thích cơ chế. Tái chạy năm A/B đỏ/xanh và một merge pending thật `f618e01 ← d47ea59` cho **rc0, 0 vi phạm**, có MERGE_HEAD. Không có kết luận đảo ngược rằng mọi merge pending đều xanh.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — ba mutant một byte độc lập tại heading r358, heading r360, phép trừ finding: claims đều rc0/ok=true, release đều rc2/ok=false và chỉ lỗi CHANGELOG. Mã cổng không đổi so base, ngoài tám tệp của PR; giữ nợ D.
- `cong-receipt-chua-dinh-nghia-cay-dang-merge`: **CHƯA VÁ** — `_neo_git` vẫn so ancestry với HEAD trong khi `kiem` đọc cây trên đĩa. Tự giữ từng cây lịch sử và thay HEAD cha1/merge cho **6/1/4/2/11 → 0/0/0/0/0**. Mã không đổi; giữ nợ D, không yêu cầu PR hồ sơ sửa mã.

Tổng đối chiếu năm slug: **3 ĐÃ VÁ THẬT · 0 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 2 CHƯA VÁ**. Có **một finding mới độc lập** về báo cáo kích thước bản vá, không gán cưỡng ép nó cho một trong ba sửa chữa đã đóng.

## BẢN VÁ CÓ TỐI GIẢN KHÔNG, VÀ NÓ CÓ GIẢM LỖI MỚI KHÔNG

**Đã ngắn hơn rõ rệt, nhưng không hoàn toàn là “chỉ sửa đúng câu sai”.** Patch được giao bằng byte `git diff d47ea59 HEAD`, đúng một commit mới, một cha, không merge.

| phạm vi | thêm | bớt | ròng |
|---|---:|---:|---:|
| CHANGELOG.md | 19 | 8 | +11 |
| RELEASE_MANIFEST.json | 5 | 5 | 0 |
| Toàn bản vá lượt 15→16 | **24** | **13** | **+11** |
| Toàn PR, base 4b5184e | **1819** | **26** | **+1793** |

Phần thay bốn dòng phản chứng cũ bằng bảy dòng tại 1609–1615 có diễn giải mới về đơn vị và giới hạn năm ca, nhưng phục vụ trực tiếp việc sửa lý do sai. Hai gạch đính chính C/E là cách sửa nguồn bất biến, không phải bỏ sót. Thay tiêu đề “MƯỜI BỐN→MƯỜI LĂM” và thêm hàng 15 là mở rộng bảng tóm tắt ngoài phần bắt buộc sửa; hàng 14 điền đúng nguồn. Không có đoạn tổng kết tự sự mới kiểu “Điều đáng nhớ…”: đoạn ấy đã tồn tại ở `d47ea59`, không được cộng nhầm vào phần thêm của lượt này. Vì vậy đây là bản vá gọn, có một phần cập nhật bảng thêm, chưa phải tối thiểu tuyệt đối. Độ dài tự nó không thành finding.

**Các tiền đề số trong lời giao việc bị lệch.** Tự cắt từ heading r360 đến ngay trước heading kế tiếp, giữ cả dòng trống, được:

| lượt review / SHA | số dòng r360 | tăng từ hàng trước |
|---|---:|---:|
| 6 / 2c57e99 | 263 | — |
| 7 / a4bc01d | 311 | 48 |
| 8 / 025c6b2 | 408 | 97 |
| 9 / dd4a3ae | 470 | 62 |
| 10 / 9e78e19 | 504 | 34 |
| 11 / b43d4ab | 532 | 28 |
| 12 / e921131 | 555 | 23 |
| 13 / 89d938e | 599 | 44 |
| 14 / f618e01 | 617 | 18 |
| 15 / d47ea59 | 654 | 37 |
| 16 / 95071a1 | **665** | **11** |

Lượt 14→15 thật là **3 tệp,+57/−15**, riêng CHANGELOG **+43/−6**; không phải +19/−8 gồm manifest. Số **654 thuộc lượt 15**, không thuộc lượt 14; lượt 6→14 tăng354, lượt 6→15 tăng391. Lỗi trong prompt được ghi ở bảng đo, không tự thành finding của kho. Tuy nhiên, cặp **654→664/+10** và **+16/−6** cũng được ghi trong commit mới, nên sai số đó có hiện vật bền và là finding bên dưới.

**Lỗi hồ sơ mới giảm: lượt 14 có 2 (A/B), lượt 15 có 3 (F/C/E), lượt 16 có 1 (F kiểm kê bản vá).** Tách hai nợ D khỏi số này; ở lượt 14 nợ ancestry mới được đặt tên không phải lỗi hồ sơ do bản vá tạo. Tới lượt này, nội dung sửa F/C/E và hai ô bảng mới không sinh sai nghĩa. Lỗi mới duy nhất nằm trong message tổng kết số đo chiến thuật.

**Chưa đo được quan hệ nhân quả “ít lỗi hơn nhờ tối giản”.** Bản vá nhỏ hơn và ít lỗi mới hơn là hai quan sát cùng xuất hiện. Không có bản vá đối chứng dài trên cùng đầu vào; ba finding lần này cũng đã có cách sửa cụ thể từ verdict trước, và hai lỗi nằm trong message chỉ cần đính chính ngắn. Những yếu tố ấy chưa được tách khỏi độ dài. Có thể nói chiến thuật lần này đi kèm kết quả tốt hơn; không thể chứng nhận nó là nguyên nhân, cũng không đủ chứng cứ tuyên bố nó không có tác dụng. “Đo được là có tác dụng” ở message chỉ có số dòng theo sau, chưa phải phép đo số lỗi hay chứng minh nhân quả. Không mở thêm finding E bằng cách áp cho câu ấy một kết luận mạnh hơn nó buộc phải mang.

Cụm “bản vá lượt 14” ở message:7 được đọc theo nghĩa bản vá **cho findings lượt 14**, tức `d47ea59` như tiêu đề commit đó ghi; không chấm một lỗi lịch sử chỉ từ cách gọi lượt có thể gây nhầm. Các so sánh trong verdict này luôn ghi rõ hai SHA.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence:** đọc theo từng nhóm trường; parse YAML được không đồng nghĩa sự kiện đúng.

| trường / nhóm | phép đo và kết quả / hạng nguồn |
|---|---|
| p1_theo_luot `{1:3,2:0}`; luot_cuoi | Regex chỉ heading finding hai verdict: **3 P1/5 P2/6 P3 =14**, **0 P1/3 P2/10 P3 =13**. Khớp |
| doi_chieu_luot_truoc | Parse 14 dòng slug verdict 2: **7/1/0/6**; cả ba slug P1 verdict 1 thuộc nhóm ĐÃ VÁ THẬT |
| authorized_head_sha, reviewed_sha, khop_head_da_merge | Cùng `2ec6171f7a2e21ae950633f9e328329a355f7a6d`, bằng cha2 merge `00e017a`; khớp Git |
| “land evidence thứ bảy” | `git ls-tree -r --name-only 00e017a ops/land/`: **6** tệp trước khi thêm; khớp |
| provider/role/session/recorded_by/generation | Metadata tự khai của người lập hồ sơ; không là chứng thực độc lập danh tính/authority. Không có phép đo hậu trường để xác nhận |
| chỉ thị chủ kho trong phiên | Trường uy_quyen nhận rõ không URL bền, vết là chính tệp. KHÔNG ĐO ĐƯỢC độc lập transcript |
| approval, merged_by, run/job CI, timestamp, bot, body/readback | Nhãn GitHub ATTESTATION đầu tệp cùng nhãn/giới hạn trong trường liên quan. Thiếu raw response/body ⇒ KHÔNG ĐO ĐƯỢC độc lập |
| pre_merge_checks[0] | rc/duration/worktree_sach/so_muc_ban có nhãn riêng scalar launcher từ run.json ngoài kho; 0 P1 và SHA tách thành phép đo verdict/Git đúng hạng |
| kết quả cổng lịch sử | Chú thích nhận thiếu stdout gốc. Chạy lại chỉ kiểm tái lập, không chứng nhận lần chạy cũ. 146 hiện tại không thay cho 121 lịch sử |
| bookkeeping về edited | Phân biệt đúng cấu hình `pull_request` và `pull_request_target`, nhận thiếu raw event. Không còn dùng lời kể run như phản chứng offline |
| 11 finding lúc merge | Chỉ tái lập được **13−2=11** trên hai sửa body được thuật lại; KHÔNG ĐO ĐƯỢC số thực tế còn sống lúc merge |

Không tìm được trường sự kiện mới bị nâng hạng hoặc mất nhãn trong land evidence. Đầu tệp không phủ launcher, nhưng launcher đã có nhãn riêng. Không coi metadata nhận dạng tự khai là kết quả xác thực. Hai workflow bản chép bằng byte tệp thật: ci.yml có `pull_request` không `types`; workflow thu hồi có `pull_request_target`, types gồm `opened/reopened/synchronize/ready_for_review/edited`. Mặc định nền tảng không nằm trong YAML; không tra mạng để xác thực semantics hay nguyên nhân lần run lịch sử.

**Hai verdict nguyên văn:**

| tệp | byte | SHA-256 | lịch sử |
|---|---:|---|---|
| pr491-review-1-codex-verdict.md | **35088** | `38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c` | 0 commit M |
| pr491-review-2-codex-verdict.md | **36958** | `14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468` | 0 commit M |

Cả hai khớp byte/băm receipt. `git log --diff-filter=M --format=%H -- <tệp>` rỗng; commit A duy nhất là `34e9d35be0fc52406e3659bfc24c388bf54262cd`; blob tại commit A bằng byte HEAD. Không sửa byte kể từ lúc vào lịch sử được giao; không chứng thực giai đoạn trước khi nhập Git.

**Hai biên nhận v2:** toàn suite **146/146, đã chạy146, bỏ0**, rc0. Gọi riêng `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()` và `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()` đều PASS. Tự kiểm 4+5 ID: mỗi ID có đúng một hàng cảnh báo gắn đúng verdict tương ứng; hai cặp verdict/receipt có trong mục lục. Nội dung chín caveat:

| lượt / ID | đối chiếu nội dung |
|---|---|
| 1 / HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE | ba4a258 khác 2ec6171; đúng header verdict và cha merge |
| 1 / SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1 | Sáu heading P3 gồm 5 độ phủ và 1 giới hạn cổng; khớp |
| 1 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Khớp giới hạn tự khai model; không biến model yêu cầu thành backend đã xác thực |
| 1 / phan-cong-CAM-tu-soan-phan-chung | Khớp giới hạn phân công trong nguồn; không suy không finding thành đầy đủ độ phủ |
| 2 / changes_requested-KHONG-phai-chua-dat-dieu-kien-dung | Nguồn giữ changes_requested và nêu đạt điều kiện lịch sử 0 P1; khớp |
| 2 / HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge | 13 heading tại review, 11 khi nhận hai sửa body trước merge. Khớp số học **có điều kiện**, không xác thực số thật lúc merge |
| 2 / NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI | Receipt có 5 mục, 3 mới/2 trùng; hai slug trùng nối được verdict. Đây là báo cáo điều phối bổ sung, không phải 5 finding trong verdict gốc; sự kiện bot KHÔNG ĐO ĐƯỢC offline |
| 2 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Cùng giới hạn model của nguồn |
| 2 / phan-cong-CAM-tu-soan-phan-chung | Khớp giới hạn nguồn và việc nguồn thuật lại mutant nội dung |

Hậu tố **11-con-song-luc-merge chưa được xác thực như sự kiện**. Receipt `dieu_kien_dung_da_thoa.khong_suy_rong` đã ghi rõ con số phụ thuộc ATTESTATION, README có nhãn nguồn cho nhóm PR491. Không dùng t27 xanh chứng minh 11, cũng không đổi thành 13 khi chưa có chứng cứ bác hai sửa body. Không có caveat mới mâu thuẫn verdict trong giới hạn ấy.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| exact HEAD/base | 95071a1 / 4b5184e | Full OID đầu verdict, ancestry rc0 | Có |
| first-parent base..HEAD | bản vá thuần | **24 commit**; chỉ 95071a1 mới sau d47ea59, cha duy nhất d47ea59 | Có |
| delta toàn PR | numstat.txt, base không đổi | **8 tệp,+1819/−26**; numstat và diff bằng byte Git | Có |
| delta lượt 15→16 | commit +16/−6 | **2 tệp,+24/−13**; riêng CHANGELOG +19/−8 | Không, F |
| r360 hiện tại | commit 664,+10 | **665,+11**; heading1031 tới trước1696 | Không, F |
| delta lượt 14→15 | prompt +19/−8 | **3 tệp,+57/−15** | Không, prompt |
| r360 lượt14 | prompt654 | **617**;654 ở lượt15 | Không, prompt |
| khoảng tăng các lượt6→15 | +18…+97 | Các chênh48/97/62/34/28/23/44/18/37 | Có trong khoảng đã khai ở đây |
| năm receipt thay đổi | cách đếm cũ | 6/2/4/2/11 | Có phép đếm, sai nếu gọi “thêm” |
| năm receipt thêm mới | bảng đã vá6/1/4/2/11 | Lọc A và đuôi `.receipt.yaml`:6/1/4/2/11 | Có |
| lỗi ancestry trước/sau commit |6/1/4/2/11 rồi0 | Năm A/B tự chạy khớp từng ca | Có |
| mọi merge pending đều đỏ | câu lịch sử đã rút | Pending f618e01←d47ea59 xanh, MERGE_HEAD tồn tại | Đính chính đúng |
| 15 hàng r360 | SHA/verdict/severity/đối chiếu | Tự parse 15 verdict, mọi ô khớp, chi tiết dưới | Có |
| heading đầu | thứ tự r không va chạm | r364→363→362→361→360→359→358→356; sáu dòng đầu ở1/98/199/845/1031/1696 | Có |
| các mục master không bị nuốt | giữ nội dung master | r364/r363/r362/r361/r359 bằng byte base | Có |
| 5 slice giao | theo heading thật | r364=97,r362=646,r360=665,r359=120,r358=233;5/5 bằng byte | Có |
| YAML/README/workflow bản chép | từ cây |6/6 bằng byte HEAD | Có |
| hai verdict PR491 |35088/36958, băm ghim |Cả hai khớp,0 commit M,blob A=HEAD | Có |
| P1 hai lượt PR491 |3/0 |3/0 heading P1 | Có |
| chín caveat, t26/t27 | liên kết/băm đúng |9/9 ID đúng hàng;hai ca PASS | Có trong hợp đồng |
| land evidence thứ7 |6 trước khi thêm |6 tệp trên00e017a | Có |
| băm hiện vật |ARTIFACTS.sha256 |**3360/3360** khớp | Có toàn vẹn, không xác thực nguồn sinh |
| bảng khẳng định |3525 dòng |Tái chạy11 input bằng byte;3525 dòng dữ liệu không rỗng,2174 có số,**3549 dòng vật lý** cả khung | Có theo đơn vị dữ liệu |
| ref snapshot |329/329/329,lệch0 |Ba TSV bằng byte,local heads329,hai TSV lệch rỗng | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| message trích |Git range base..HEAD |Bằng byte `git log --format=%H%n%B%n--- 4b5184e..HEAD` | Có vận chuyển, không bảo đảm nội dung |
| bien_nhan_v2 |67 v2,tổng120,sạch |rc0;67+11 legacy+42 nợ=120;0 vi phạm,0 KHÔNG ĐO ĐƯỢC | Có |
| lease_publish_test |146/146 |rc0;146/146,chạy146,bỏ0 | Có |
| release-verify --strict --json |180/180,ok=true |rc0;180/180,hai hash match=true,failed/extra/required_missing/errors rỗng | Có |
| doc-claims-check --strict --json |xanh |rc0,ok=true,106 tệp,flags=[],370 advisory | Có trong hợp đồng |
| doctrine-scan --root . |sạch |rc0,7 tệp,0 chỗ chép doctrine | Có |
| adr-song --root . |sạch |rc0,46 ADR/46 hàng,khớp1–1,tha trạng thái0016 | Có |
| nợ claims |cổng không đếm các đại lượng này |3 mutant qua claims,cả3 bị release chặn | Nợ D còn |
| CI/approval thật, số11 lúc merge |thuật lại |Thiếu raw response/body/run và không mạng | KHÔNG ĐO ĐƯỢC |
| code/workflow ngoài write set |không sửa |Diff base..HEAD của mã hai nợ D và workflows rỗng | Có |

**Từng ô đối chiếu của bảng r360.** Parser chỉ lấy dòng slug và trạng thái trong phần ĐỐI CHIẾU của từng verdict; không đếm tổng văn xuôi. Thứ tự: ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ. Hàng1 không có lượt trước; hàng5 gồm cả slug đã đóng được tiếp tục theo dõi, không nhầm tổng slug với tổng finding sống.

| lượt | số tự parse | tổng slug | ô r360 |
|---|---|---:|---|
|1|—|—|Khớp —|
|2|0/6/0/11|17|Khớp từng số|
|3|7/3/0/10|20|Khớp từng số|
|4|1/2/0/14|17|Khớp từng số|
|5|3/0/1/13|17|Khớp từng số|
|6|11/2/0/1|14|Khớp từng số|
|7|4/3/2/1|10|Khớp từng số|
|8|7/0/1/1|9|Khớp từng số|
|9|7/2/0/1|10|Khớp từng số|
|10|3/1/0/1|5|Khớp từng số|
|11|2/0/0/1|3|Khớp từng số|
|12|1/0/0/1|2|Khớp từng số|
|13|2/0/0/1|3|Khớp từng số|
|14|**0/0/1/1**|2|Khớp từng số; đã điền đúng|
|15|**1/0/1/2**|4|Khớp từng số; không tráo với lượt14|

### so-do-va-toi-gian-khong-khop-diff-cuoi  [P3]  Commit báo thiếu dòng ngay trong phép đo chiến thuật tối giản
LỚP: F
TỆP/DÒNG: message commit `95071a19670dee33630286a84af6caf5a47d8524`; bản trích `thong-diep-commit.txt:25–27`.
VẤN ĐỀ: Message khai “bản vá lượt này: +16/−6” và “r360:654→664(+10)”. Diff cha→HEAD cho CHANGELOG **+19/−8**, manifest **+5/−5**, tổng **+24/−13**. R360 có **665 dòng**, tăng **11**, không phải10. Hai phạm vi thông dụng (toàn diff hoặc bỏ manifest) đều không cho16/6. Có thể thu được16/6 nếu còn loại thêm hunk tiêu đề/bảng lượt **+3/−2**, nhưng message không khai bộ lọc ấy và cặp độ dài toàn mục vẫn sai. Không nhận một kiểm kê phần chọn làm kiểm kê toàn bản vá, nhất là khi đó là bằng chứng để đánh giá chiến thuật.
CÙNG LỚP CÒN Ở ĐÂU: `BANG_KHANG_DINH.txt` trích nguyên message; lời giao việc lặp664/+10 nhưng không phải một lỗi kho độc lập. Bảng receipt mới tại CHANGELOG:1598–1605 đã đúng, không mở lại finding cũ. Gộp hai số sai cùng phép đo kích thước thành **một** finding, không nhân số lỗi theo mỗi scalar.
ĐÃ THỬ VÁ: không sửa kho hoặc lịch sử. Hướng sửa: đính chính ngắn neo95071a1, ghi rõ phạm vi **toàn diff2 tệp:+24/−13; riêng CHANGELOG:+19/−8; r360654→665(+11)**. Không cần thêm tự sự chiến thuật. Nếu cập nhật bảng tạo thêm dòng ở lượt sau thì số của95071a1 vẫn phải ghim vào95071a1.
ĐÃ THỬ NGHIỆM: `python3 -B review16-evidence/measure.py` so patch bằng byte Git và đếm heading-boundary trên blob cha/HEAD. `git diff --numstat d47ea59 95071a1` cho19/8 và5/5; các ranh giới1031/1696 xác nhận665. Kiểm bảng15 lượt vẫn khớp, nên không loại hàng15 khỏi phép đo chỉ để đạt664. Ca khóa: tổng theo tệp bằng tổng toàn diff; số dòng mục sau−trước bằng11. Nguyên nhân “số đo chụp trước cập nhật bảng” chỉ là suy đoán từ hunk, không có transcript để chứng nhận.
ĐỘ TIN: cao

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Claims vẫn để lọt ba sai số nội dung
LỚP: D
TỆP/DÒNG: `scripts/tl_core/workflow.py:1163`, :1430; mutant ở `CHANGELOG.md:1816`, :1031, :1351.
VẤN ĐỀ: Release kiểm byte nhưng claims không bác1016→1017,5→6,13−2=11→12. Ngoài write set, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: cả ba nhóm đại lượng đã thử; không suy mọi câu đều lọt.
ĐÃ THỬ VÁ: không; giữ packet cổng riêng. Hướng là hợp đồng đại lượng/nguồn đếm có cấu trúc và phân biệt câu lịch sử được trích để bác; tránh hardcode ba chuỗi.
ĐÃ THỬ NGHIỆM: `python3 -B review16-evidence/probes.py`: ba mutant độc lập, mỗi mutant giữ961237 byte; claims cả3 rc0/ok=true; release cả3 rc2/ok=false,failed chỉCHANGELOG. Control tại reviewed SHA xanh. Ca khóa kế nhiệm: mutant đỏ ở cổng nội dung, control xanh; tránh regex kết tội đoạn đính chính.
ĐỘ TIN: cao

### cong-receipt-chua-dinh-nghia-cay-dang-merge  [P3]  Cổng đọc đĩa nhưng ancestry vẫn theo HEAD
LỚP: D
TỆP/DÒNG: `ops/bien_nhan_v2.py:808–824` (`_neo_git`), :861 (`kiem`).
VẤN ĐỀ: Candidate trên đĩa có thể khác HEAD khi merge chưa commit. Cùng năm cây đã giải cho kết quả khác khi thay HEAD. Nợ giao diện trạng thái dở, không phải kết luận kiểm ancestry của commit đã chốt sai; ngoài write set, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: năm merge lịch sử đã thử; không áp cho mọi merge pending.
ĐÃ THỬ VÁ: không; packet kế nhiệm cần định nghĩa candidate commit/tập cha ràng buộc với nội dung đang kiểm, hoặc trả chưa đo được khi thiếu hợp đồng. Không thay HEAD bằng tree hash vì tree không có ancestry.
ĐÃ THỬ NGHIỆM: `probes.py` chạy checker mỗi cây lịch sử, giữ nội dung và đổi HEAD cha1/merge:6/1/4/2/11 lỗi rc1→0 lỗi rc0 ở cả5. Đây là A/B trên cây đã commit, không giả nhận transcript năm merge cũ. `pending.py` tái dựng riêng merge thật f618e01←d47ea59 chưa commit, MERGE_HEAD tồn tại và cổng rc0/0 lỗi. Ca khóa kế nhiệm phải giữ neo nhánh không liên quan bị chặn và thiếu object là chưa đo được; không mở rộng vô điều kiện tập tổ tiên.
ĐỘ TIN: cao về hành vi; vừa về thiết kế giao diện kế nhiệm

Kiểm cuối: `cay-kho/` vẫn đúng reviewed SHA, `git status --porcelain` rỗng; băm lại **3360/3360** hiện vật gốc khớp. Verdict có đúng **3 heading P3**, không P1/P2; mọi liên kết bằng chứng tồn tại. Kết quả lưu ở [final-check.json](review16-evidence/final-check.json).
