verdict: changes_requested
reviewed_sha: b43d4ab118c31d2387e4fc6104bb783e5c6521a5

**KHÔNG CÒN P1 · KHÔNG CÒN P2 trong phạm vi review · CÒN 2 P3. Điều kiện tới hết P3 CHƯA ĐẠT.**

Reviewer: Codex/GPT-6 theo cấu hình phiên; provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`. Review độc lập với executor Claude theo chỉ thị người dùng; không có chứng thực độc lập model/backend phục vụ. Không tự ghi transition `cross_approved` hoặc cấp quyền merge. Đã xét tính đúng/phạm vi yêu cầu và tính nhất quán của hồ sơ/cổng.

Head đúng SHA trên; tree `b81f8133ea1c730a0382a76e0e9e369abc741c91`. Base vẫn `c00c88a02a29c057b0c59806760c35968e408dc4`. `cay-kho/` được giữ read-only; cổng và đột biến chạy trên bản sao `review11-current/`, TMPDIR là `review11-tmp/`, đều trong workspace. Không mạng, không tự soạn payload đường dẫn. Thư mục actionlint 1.7.7 được thêm vào CUỐI PATH; Git dùng `core.abbrev=7` khi chạy cổng.

Bằng chứng tự chạy: [measurements.json](review11-evidence/measurements.json), [extra.json](review11-evidence/extra.json), các script và stdout trong `review11-evidence/`. Không lấy output cổng lượt trước làm kết quả lượt này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — ba mutant độc lập trên bản sao: `1016→1017` ở heading r358, `5→6` ở heading r360, `13 − 2 = 11→12` ở phép trừ hiện hành. Mỗi mutant thay đúng một byte, giữ 881004 byte CHANGELOG. Kết quả cổng chi tiết ở BẢNG ĐO và `probes.json`. Mã cổng không thuộc delta; nhận nợ không đóng hành vi.
- `phat-hien-them-da-co-trong-verdict-bay`: **ĐÃ VÁ THẬT** — CHANGELOG:621 đặt heading “13 vị trí, 12 thuộc địa chỉ reviewer đã nêu”; :658–659 gọi rõ bốn vị trí A2/A6/B4/C3 là TỪNG BỊ XẾP NHẦM. Parse bảng :639–651 được 13 ID duy nhất, 12 “có”, một “không” là B4; dòng D không có ID không bị cộng vào inventory. :655–656 và :702–703 cùng phân hoạch 13=12+1, B4 không phải lỗi, 0 lỗi ngoài địa chỉ. :710–715 tự rút cả câu “không còn câu nào khai công” của bản trước. Đối chiếu trường TỆP/DÒNG của verdict 7; riêng A2/A6 đọc lại blob `a4bc01d:CHANGELOG.md` xác nhận dòng 173 trong 168–179 và dòng 298 trong 298–303. Không đánh đồng địa chỉ được nêu với khuyết tật đã được nêu. Đã vét đoạn sau nối whitespace trên r360, thân PR và toàn thông điệp commit: không còn 4/2 làm phân hoạch hiện hành. Message 9349bb0 còn lời cũ trong lịch sử đã được đính chính; message mới và heading cũ được trích để bác, không phải lỗi mới. Câu “A2 và A6 đứng vững” nay nói về hai khuyết tật trong vùng được chỉ, không còn nói hai lỗi ngoài địa chỉ.
- `chuoi-chin-luot-thieu-pham-vi-p3`: **ĐÃ VÁ THẬT** — tự đếm heading finding của CẢ MƯỜI verdict bằng regex `^### .*\[P[123]\]`, không đếm mọi token severity trong văn xuôi. Hai hàng CHANGELOG:728–729 khớp từng ô, dòng lượt 10 :731 đúng 3/3. :674–676 đính chính message cc21507 có neo đích danh. Chi tiết số đếm ở bảng dưới. Nhãn “tương quan-không-nhân-quả không chữa bộ lọc không khai” đúng trong trường hợp này: tên đại lượng/tập đếm và suy nhân quả là hai nghĩa vụ độc lập. Thêm nhãn tương quan không biến 12 thành tổng 17 ở lượt 1; đổi thành tổng 17 cũng không tạo phép kiểm soát biến cho kết luận nhân quả. Không hiểu câu ấy thành định lý về mọi bộ lọc hoặc bằng chứng ưu thế của một phương pháp.

Tổng ba slug lượt 10: **2 ĐÃ VÁ THẬT · 0 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Phát hiện thêm một bản chiếu runtime còn thiếu nhãn ở land evidence; dùng lại slug sự kiện lượt 8, không quy nó thành lỗi mới do delta lượt 11.

| lượt | P1 đếm heading | P2 đếm heading | P3 đếm heading | tổng | đối chiếu hai đường |
|---|---:|---:|---:|---:|---|
| 1 | 1 | 4 | 12 | 17 | Khớp 12/17 |
| 2 | 1 | 4 | 15 | 20 | Khớp 15/20 |
| 3 | 0 | 2 | 15 | 17 | Khớp 15/17 |
| 4 | 0 | 1 | 15 | 16 | Khớp 15/16 |
| 5 | 0 | 0 | 14 | 14 | Khớp 14/14 |
| 6 | 0 | 0 | 10 | 10 | Khớp 10/10 |
| 7 | 0 | 0 | 9 | 9 | Khớp 9/9 |
| 8 | 0 | 0 | 10 | 10 | Khớp 10/10 |
| 9 | 0 | 0 | 5 | 5 | Khớp 5/5 |
| 10 | 0 | 0 | 3 | 3 | Khớp dòng riêng 3/3 |

Hai đường không trùng tại bất kỳ điểm nào trong lượt 1–4; trùng từ lượt 5 đến lượt 10. Chênh lệch bốn điểm đầu là 5+5+2+1=13 **lượt-finding P1/P2**, không phải 13 khuyết tật duy nhất qua lịch sử. Bảng đang đếm theo lượt nên không cần khử trùng slug giữa các lượt.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence:** không phải mọi trường đều đã giữ đúng nhãn nguồn. Đã đối chiếu toàn tệp 218 dòng với hai receipt, hai verdict và Git:

| nhóm trường | nguồn và phép đo | kết quả |
|---|---|---|
| schema/mission/generation/provider/role/session/recorded_by/input_packet_generations | metadata do người lập hồ sơ khai | Không suy đây là chứng thực session hoặc authority từ máy chủ |
| p1_theo_luot; luot_cuoi severity/verdict | parse heading hai verdict trong kho | Lượt 1 = 3 P1+5 P2+6 P3=14; lượt 2 = 0+3+10=13. `{1:3,2:0}` ĐÚNG và có nhãn ĐO ĐƯỢC đúng hạng |
| doi_chieu_luot_truoc | đếm trạng thái slug được in đậm trong verdict 2 | 7 ĐÃ VÁ THẬT, 1 VÁ HỜ, 0 VÁ SINH LỖI MỚI, 6 CHƯA VÁ; tổng 14, đơn vị được khai rõ |
| reviewed_sha/authorized_head_sha/khop_head_da_merge | verdict 2 dòng 2, `git show -s --format=%P 00e017a` | Cùng `2ec6171f7a2e21ae950633f9e328329a355f7a6d`, đúng cha thứ hai; ancestry rc0 |
| land evidence thứ bảy | `git ls-tree -r --name-only 00e017a ops/land/` | 6 tệp trước khi thêm, đúng thứ bảy |
| commit đầu chứa hai verdict | `git log --diff-filter=A`; so byte blob | Đúng `34e9d35be0fc52406e3659bfc24c388bf54262cd` |
| approver, approval URL/state, dismiss, merge actor/time, số run/job/bước/trạng thái CI, bot, cập nhật thân PR | nhãn mọi sự kiện GitHub ở đầu tệp; nhãn actor và giới hạn JSON ở :40, :181–183 | KHÔNG ĐO ĐƯỢC độc lập vì không response/log gốc và không mạng; không dùng timestamp Git để xác nhận push/approve. Nhãn toàn tệp có hiệu lực cho các sự kiện GitHub này |
| chỉ thị chủ kho/ai thực sự thao tác | land_operator_neo.uy_quyen và canh_bao | Tệp tự khai chỉ thị trong phiên không URL, và PAT không phân biệt người/agent. Không nâng thành authority do reviewer xác nhận |
| model_yeu_cau/model_da_chay | receipt và verdict tự khai giới hạn | Giữ KHONG_DO_DUOC cho model thực phục vụ là đúng; không chứng thực biến thể model từ tên yêu cầu |
| CI dự kiến checkout cây nào | phân biệt cấu hình với runner thật tại :128–131 | Có giới hạn rõ; không xác nhận cây runtime bằng cấu hình |
| runtime cross-review lượt 2, pre_merge_checks[0].ket_qua | đối chiếu receipt 2 :142–152, :172–175 | **MẤT NHÃN** cho 714,268s/rc0/trạng thái sạch; nhãn đầu tệp chỉ nói sự kiện GitHub. Xem finding lớp B |
| các output cổng pre/post-merge lịch sử | các lời ghi kết quả trong hồ sơ | Có thể kiểm hành vi bằng tái chạy đúng snapshot, nhưng không xác nhận lần chạy lịch sử/pha chưa commit từ một lần chạy hôm nay. Lượt này chỉ tự chạy cổng trên b43d4ab; các lần chạy lịch sử KHÔNG ĐO ĐƯỢC độc lập |
| bookkeeping còn 11 finding review 2 lúc merge | 13 heading trừ 2 P2 thân PR được khai đã vá | Số học đúng, trạng thái sửa thân PR là attestation; xem caveat bên dưới |

**Hai verdict nguyên văn:**

| tệp | byte tự đo | SHA-256 tự đo | lịch sử |
|---|---:|---|---|
| `ops/reviews/pr491-review-1-codex-verdict.md` | 35088 | `38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c` | `git log --diff-filter=M` rc0, output rỗng; blob đầu bằng byte hiện tại |
| `ops/reviews/pr491-review-2-codex-verdict.md` | 36958 | `14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468` | `git log --diff-filter=M` rc0, output rỗng; blob đầu bằng byte hiện tại |

Cả hai khớp `verdict_bytes`, `verdict_sha256` của receipt. Không thấy sửa một byte kể từ khi thêm trên lịch sử đi tới reviewed head. Phép đo này không chứng thực quá trình sinh văn bản trước khi nó được đưa vào Git.

**Hai receipt và chín caveat:** mỗi receipt có đúng hàng mục lục cùng verdict và receipt (:302 cho lượt 1, :301 cho lượt 2). Mỗi caveat có đúng một hàng cảnh báo chứa CÙNG tên verdict và ID; không lấy một lần xuất hiện đâu đó trong README làm pass. `t26` kiểm băm; `t27` kiểm quan hệ mục lục/caveat, không tự kiểm chân trị văn xuôi.

| lượt / caveat ID | hàng README | đối chiếu nội dung |
|---|---:|---|
| 1 / HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE | 32 | ba4a258 là head verdict 1; 2ec6171 là head verdict 2 và cha merge. Khớp; không gán finding cũ cho master |
| 1 / SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1 | 33 | Đọc sáu heading P3 và nội dung: năm về độ phủ, một về giới hạn cổng. Khớp; verdict 1 :183–188 tự gọi ghi nhận dương |
| 1 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | 34 | Verdict tự khai không chứng thực model/build; phù hợp cảnh báo. Yêu cầu gpt-6-astra và việc tool không phát modelUsage là lời receipt, không bằng chứng backend |
| 1 / phan-cong-CAM-tu-soan-phan-chung | 35 | Phù hợp phạm vi cấm và việc không tự soạn payload được verdict thuật lại; không suy không có lỗ từ không có finding |
| 2 / changes_requested-KHONG-phai-chua-dat-dieu-kien-dung | 27 | Khớp nguyên ý verdict 2 :4: 0 P1 thỏa điều kiện lịch sử tới hết P1, vẫn changes_requested |
| 2 / HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge | 28 | Verdict có 13, hai P2 :133/:140 thuộc thân PR, P2 :126 thuộc CHANGELOG. 13−2=11=1P2+10P3 khớp với attestation sửa hai P2; không phải 11 đếm được trực tiếp từ verdict |
| 2 / NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI | 29 | Là nguồn thứ ba ngoài hai verdict. Danh sách trong receipt có 5, 3 mới/2 trùng; hai trùng nối được với slug verdict. Sự kiện bot/5 P2 và trạng thái #490 KHÔNG ĐO ĐƯỢC độc lập khi thiếu review JSON; không cộng 11+5 |
| 2 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | 30 | Phù hợp verdict 2 :6 không chứng thực variant/build/effort; không xác nhận model thực từ yêu cầu |
| 2 / phan-cong-CAM-tu-soan-phan-chung | 31 | Verdict :8 nói rõ cấm tự soạn; :25, :69–70, :186 ghi ba đột biến 1016/35/revision9. Caveat khớp phạm vi và phép đo được thuật trong nguồn |

**Không thể nói đã tự đo “11 finding thật còn sống lúc merge”.** Đo được 13 finding lúc review và vị trí hai P2 trong thân PR; con số 11 chỉ đúng có điều kiện theo attestation rằng hai P2 đã được sửa trước merge. Receipt :50–52 và mục lục :301 khai rõ giới hạn này. Không có raw body/readback PR #491 tại thời điểm merge để kiểm độc lập; `than-pr-493.md` là PR khác, không thay thế được. ID `…-11-con-song-luc-merge` thống nhất với phép đếm có điều kiện ấy, không mâu thuẫn 13 heading của verdict, và không đại diện tổng nợ gồm cả bot. Không thêm finding vì không biến một dữ kiện đã khai là attestation thành phép đo độc lập.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head/base | b43d4ab/c00c88a | rev-parse đúng SHA và tree nêu đầu; ancestry rc0 | Có |
| First-parent c00c88a..HEAD | bản vá sau lượt 10, không merge mới | 17 commit, mới nhất b43d4ab, cha 9e78e19; log đầy đủ ở measurements.json | Có |
| Delta lượt 10→11 | bản vá thuần | 2 tệp +42/−14: CHANGELOG +37/−9, manifest +5/−5 | Có |
| Toàn PR | numstat so c00c88a | awk và Git: 8 tệp +1650/−26 | Có |
| Diff/numstat/message | bản trích Git | 4/4 byte-exact | Có |
| Năm slice | cắt theo heading thật | 5/5 byte-exact; bắt đầu 1,102,288,820,940 | Có |
| Bốn bản chiếu receipt/README/land | chép từ cây | 4/4 byte-exact | Có |
| Thứ tự heading đầu | r363→361→360→359→358→356 | Đúng; không trùng số r trong dãy dev-side | Có |
| README | 264 cảnh báo,107 mục lục,0 trùng | Đếm theo cấu trúc bảng:264/107, trùng nguyên hàng0/0 | Có |
| Ref snapshot | 324/324/324, lệch0 | ba TSV bằng nhau; live refs/heads cục bộ324 | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Bộ trích | 11 input,2741 dòng | chạy lại byte-exact;2741 dòng không rỗng,1744 mang chữ số | Có trong tập input đã khai |
| Inventory | 13=12+1 | 13 ID duy nhất,12 có,1 không; D ngoài tổng | Có |
| Chuỗi P3 và tổng | hai hàng có nhãn và lượt10 riêng | 20/20 ô khớp bảng số đếm trên | Có |
| Land evidence P1 | 3/0 | heading3/0; tổng14/13 | Có |
| Land runtime |714,268s/rc0/worktree sạch | receipt xếp attestation;land bỏ nhãn ấy | **Không đúng hạng nguồn** |
| Verdict bytes/hash/history |35088/36958 và hai băm | cả hai khớp;0 commit M;blob đầu byte-exact | Có |
| t26/t27 quan hệ dữ liệu |băm và mục lục/caveat cùng hàng |2 hash khớp;2 hàng mục lục;9/9 hàng caveat đúng cặp | Có |
| 11 finding lúc merge |13−2, có attestation |phép trừ đúng;hai lần sửa thân PR lịch sử thiếu raw/readback | Có điều kiện; trạng thái thực KHÔNG ĐO ĐƯỢC |
| `git ls-tree -r --name-only HEAD ops/reviews/ ops/land/` | hiện vật #491 vào kho | rc0; có2verdict+2receipt491 và land491; danh sách đầy đủ trong measurements.json | Có |
| `python3 -B ops/bien_nhan_v2.py` |0 vi phạm,54v2/tổng107 |rc0;54v2+11legacy+42nợ=107;0vi phạm;0 KHÔNG ĐO ĐƯỢC | Có |
| `python3 -B ops/lease_publish_test.py` |146/146 |rc0;146/146 đạt;đã chạy146,bỏ0, gồm t26/t27 | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` |xanh180/180 |rc0;ok=true;180/180;hash match;failed/extra/errors rỗng | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` |xanh |rc0;ok=true;flags=[];106 tệp quét;vẫn có advisories lịch sử | Có trong phạm vi cổng |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` |rc0 |rc0;7 tệp;0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` |rc0 |rc0;46 ADR/46 hàng,khớp1–1;output tự nêu tha thiếu trạng thái0016 | Có |
| Mutant1016→1017 |nợ còn mở |claims rc0/ok=true;release rc2/failed chỉCHANGELOG | Có;nợ chưa đóng |
| Mutantheading5→6 |nợ còn mở |claims rc0/ok=true;release rc2/failed chỉCHANGELOG | Có;nợ chưa đóng |
| Mutant13−2=11→12 |nợ còn mở |claims rc0/ok=true;release rc2/failed chỉCHANGELOG | Có;nợ chưa đóng |
| Đột biến giữ kích thước |một byte |cả3 đúng1byte,giữ881004byte;release package_hash_match=false cả3 | Có |
| Kho sạch sau đo |review read-only |git status --porcelain rc0,0byte ở cảcay-kho và bản sao sau phục hồi | Có |
| ARTIFACTS.sha256 |toàn vẹn gói |3306/3307 khớp;ngoại lệprotocol-read.txt do chính reviewer ghi đè trước kiểm | Không kết luận lỗi gói;chi tiết dưới |

Log và mã thoát đầy đủ: [gates.json](review11-evidence/gates.json), [probes.json](review11-evidence/probes.json), [lease.out](review11-evidence/lease.out), [receipts.out](review11-evidence/receipts.out). `run.py` lưu từng stdout release/claims/control/mutant riêng. Sau ba mutant, khôi phục đúng byte gốc trong `finally` và kiểm Git sạch. Không sửa manifest để làm mutant xanh.

**Giới hạn và sai sót của chính phép review:** tôi đã dùng `> protocol-read.txt` ở workspace để lưu bản protocol đang đọc mà không phát hiện tên này có sẵn trong ARTIFACTS.sha256. Vì vậy băm hiện tại của tệp phụ ấy không còn khớp băm giao; đây là thay đổi do reviewer, không phải finding của PR. **KHÔNG ĐO ĐƯỢC băm byte ban đầu của riêng tệp phụ ấy** sau khi bị ghi đè. 3306 mục còn lại khớp; `cay-kho/` sạch và mọi hiện vật chính được yêu cầu có các đối chiếu độc lập nêu trên. Không tuyên toàn gói 3307/3307 nguyên vẹn. Bản protocol dùng để đọc là nội dung exact reviewed tree, không dùng tệp phụ bị thay để chứng minh provenance gói.

Không chạy mạng, CI từ xa, native Windows/macOS hoặc full selftest sản phẩm; không tính các việc đó là pass. Delta hiện hành chỉ hai tệp hồ sơ/manifest; toàn PR tám tệp hồ sơ. Không cần tái dựng merge lượt10 lần nữa để đánh giá bản vá thuần lần này; quan hệ base và các byte/bảng hiện hành đã được đo. Những lời thuật thao tác lịch sử và trạng thái PR trên máy chủ vẫn KHÔNG ĐO ĐƯỢC độc lập.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Cổng claims vẫn nhận cả ba mệnh đề sai số
LỚP: D
TỆP/DÒNG: CHANGELOG.md:480–493,751–757; điểm đột biến:288,600,940; scripts/tl_core/workflow.py:1163,1430,1488.
VẤN ĐỀ: Cả ba phản chứng còn sống trên exact nội dung mới: số tệp1016→1017, số đối tượng5→6, phép trừ13−2=11→12. `doc-claims-check` vẫn rc0/ok=true, trong khi release chặn sai băm. Đây là nợ cổng đã có, không phải hồi quy do delta hồ sơ. Việc ngoài write set và được tự khai vẫn mở không đáp ứng điều kiện người dùng “tới hết P3”.
CÙNG LỚP CÒN Ở ĐÂU: hai đoạn nợ CHANGELOG nêu trên; receipt lượt1 phần P3 giới hạn cổng; receipt lượt2 no_con_lai; than-pr-493.md:68; message b43d4ab tại thong-diep-commit.txt:29. Các bản chiếu nhận nợ đúng, không chấm chúng là lời khai sai riêng. Đã vét các đầu vào được giao và chạy đủ ba mutant; chưa có bằng chứng đóng.
ĐÃ THỬ VÁ: không sửa sản phẩm hoặc hồ sơ nguồn. Đã thử đột biến trên bản sao, khôi phục byte gốc. Hướng xử lý là packet kế nhiệm có write set mã `_doc_claims_check`/bộ kiểm định lượng trong workflow.py: ràng buộc mệnh đề theo loại và mốc với nguồn Git/verdict/phép tính. Ca nghiệm thu: control xanh, ba mutant đỏ, và trích dẫn số sai lịch sử đã rút không bị kiểm như mệnh đề hiện hành. Không hard-code ba số mẫu hoặc đồng nhất băm với chân trị.
ĐÃ THỬ NGHIỆM: `python3 review11-evidence/run.py` — control claims/release rc0;3/3mutant claims rc0/ok=true,3/3release rc2,failed chỉCHANGELOG,package_hash_match=false. Mỗi ca đúng1byte và giữ881004byte. Chi tiết probes.json và stdout từng ca. Kho gốc và bản sao sau phục hồi đều sạch.
ĐỘ TIN: cao

### runtime-pr491-luot2-mat-nhan-khi-chieu  [P3]  Land evidence vẫn bỏ nhãn attestation của runtime cross-review lượt 2
LỚP: B
TỆP/DÒNG: ops/land/pr491-r358-ghi-so-land-evidence.yaml:102–104; phạm vi nhãn:8–11,181–183. Nguồn: ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:142–152,172–175,190. Bản chiếu ngoài kho:land-evidence.yaml:104.
VẤN ĐỀ: `pre_merge_checks[0].ket_qua` chép `rc=0`, `714,268 s`, `worktree_sach: true`, `so_muc_ban: 0` bên cạnh **0 P1** nhưng không chuyển nhãn nguồn đi cùng. Receipt xếp scalar runtime vào ATTESTATION từ run.json ngoài kho (:152,:190), và phần trạng thái sạch cũng dẫn run.json (:172). Trong land evidence, nhãn đầu tệp chỉ bao “mọi sự kiện GitHub”; `khong_do_duoc` nhắc JSON run/job/PR trong ngữ cảnh CI nhưng không nhắc run.json của launcher hay runtime reviewer. Chạy cross-review cục bộ không phải sự kiện GitHub. Người đọc riêng land evidence vì thế không biết phần nào của hàng là kết quả có thể đếm lại và phần nào chỉ là thuật lại. Đếm0P1 hoặc xác nhận băm verdict không chứng thực714,268s/rc0/trạng thái worktree lúc chạy.

Đây là **cùng sự kiện và cùng lớp** với finding runtime lượt2 của lượt8. Lượt9 đã xác nhận đúng việc sửa README và CHANGELOG, nhưng chưa phát hiện bản chiếu land này. Tôi giữ lại slug cũ và ghi rõ phần sót, không bác những chỗ đã vá và không gọi nó là lỗi mới sinh bởi b43d4ab. Số runtime không bị chứng minh là sai; lỗi đo được là **mất nhãn nguồn** khi chiếu số từ receipt sang hồ sơ land bền.
CÙNG LỚP CÒN Ở ĐÂU: land-evidence.yaml:104 ngoài kho và dòng trích tương ứng trong BANG_KHANG_DINH là bản sao của cùng hàng; không tính thêm finding. Đã vét714/696/rc/runtime/run.json trong land,receipt,README,r360,thânPR,message. README:301 và CHANGELOG:349–355 đã có nhãn runtime đầy đủ; không còn lỗi ấy ở hai chỗ đã đóng. Thân PR không chép hàng runtime714 này. Các output cổng lịch sử pre/post-merge nên được ghi rõ là lời ghi nhận của phiên khi không kèm log, nhưng không dùng chúng để nhân finding714 thành nhiều sự kiện mới.
ĐÃ THỬ VÁ: không sửa hồ sơ được review. Cách vá cụ thể: thêm `canh_bao_doc_ket_qua` ngay sau ket_qua: “Thời lượng714,268s,rc0 và trạng thái worktree của lần chạy là ATTESTATION từ run.json ngoài kho, theo receipt lượt2; gói không kèm log gốc. Riêng0P1 đếm được từ heading verdict, và head đối chiếu được bằng Git.” Có thể dẫn receipt cùng hàng; không gắn nhãn toàn bộ0P1/Git thành tự thuật. Đây là sửa hồ sơ trong write set hiện có, không cần sửa mã cổng.
ĐÃ THỬ NGHIỆM: `python3 review11-evidence/measure.py` xác nhận land/receipt bản chiếu byte-exact,verdict2 có0/3/10; `python3 review11-evidence/extra.py` lưu nguyên văn hàng nguồn và đích, thấy các run.json trong kho thuộcPR468 chứ không phải lần46d8686e củaPR491. Đọc toàn land evidence không thấy nhãn attestation cho runtime launcher. Thời lượng/rc/worktree lịch sử **KHÔNG ĐO ĐƯỢC độc lập** vì thiếu run.json của lần ấy. Cổng v2 và suite146/146 vẫn đạt với hàng thiếu nhãn này; đó là giới hạn kiểm ngữ nghĩa, không phải bằng chứng nhãn đủ.
ĐỘ TIN: cao
