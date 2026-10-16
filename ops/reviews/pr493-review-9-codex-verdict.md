verdict: changes_requested
reviewed_sha: dd4a3ae8e551ea07445c79fa3274249285f15e42

**KHÔNG CÒN P1 · KHÔNG CÒN P2 trong phạm vi review · CÒN 5 P3. Điều kiện “tới hết P3” CHƯA ĐẠT.**

Reviewer: Codex, provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`; độc lập với executor Claude theo hồ sơ được giao. Không có chứng cứ độc lập về backend/model thực phục vụ. Review khác nền theo §8 và chỉ thị trực tiếp lượt 9; không tự ghi state `cross_approved`, không cấp quyền merge. Hai trục đã kiểm: phạm vi/yêu cầu và tính đúng/nhất quán của hồ sơ cùng hành vi các cổng liên quan.

Exact tree: `6134ee69f4e9a06870ee9e483d882aee495ac695`. Base: `072181157a27804e69deb35bb792a88c70ac31e3`. `cay-kho/` detached, không nông, sạch trước và sau đo; giữ read-only. Cổng chạy trên bản sao mới `review9-current/`; đột biến ở `review9-mutant/`; đối chứng trạng thái merge ở `review9-state/`. Không mạng, không tự soạn payload đường dẫn. TMPDIR trong workspace; thêm thư mục actionlint 1.7.7 cuối PATH, ghim `core.abbrev=7` qua môi trường.

Bằng chứng tự chạy lượt này: [gates.json](review9-evidence/gates.json), [measurements.json](review9-evidence/measurements.json), [probes.json](review9-evidence/probes.json), [extra.json](review9-evidence/extra.json), [targeted.json](review9-evidence/targeted.json), các script cùng thư mục và stdout `.out`. Script có sẵn được đọc trước, sao sang thư mục mới rồi **chạy lại**; không dùng kết quả cũ làm kết quả lượt này. Dòng CHANGELOG dưới đây là dòng trong exact tree; dòng `muc-r360.md` cộng 186 tương ứng CHANGELOG.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — ba mutant riêng `1016→1017`, heading `5→6`, `13 − 2 = 11→12`: mỗi ca đổi đúng một byte, giữ 865878 byte CHANGELOG; cả ba claims `rc=0, ok=true`. Release mutant đầu `rc=2`, failed chỉ CHANGELOG. Địa chỉ `scripts/tl_core/workflow.py` đã sửa đúng, hành vi chưa đổi.
- `printf-khai-do-duoc-khong-co-payload-goc`: **ĐÃ VÁ THẬT** — CHANGELOG:604–616 giới hạn “có thể” và nêu ca cụ thể. Chạy Bash `--noprofile --norc`: `printf '- example\n'` ⇒ rc2/stdout rỗng; `printf '-'` ⇒ rc0/stdout `-`; `printf '%s\n' '- example'` ⇒ rc0/nội dung đủ. Phần comment lịch sử vẫn được ghi rõ tự thuật thiếu payload, không bị nâng thành phép đo.
- `kiem-ke-lop-tong-muoi-hai-khong-khop-hang`: **VÁ HỜ** — đã sửa thật phép cộng và đơn vị: 13 ID riêng, 6+4+3=13, không cộng hàng D. Nhưng phân hoạch địa chỉ 9/4 vẫn sai (đo 12/1), và đoạn CHANGELOG:428–430 vẫn gọi B4 là lỗi đã vá dù inventory rút nó. Phần dư được chấm ở hai finding inventory/B4 dưới đây; không đếm lại thành một finding thứ sáu.
- `phat-hien-them-da-co-trong-verdict-bay`: **VÁ HỜ** — C1 được chuyển sang “có” đúng với lượt 7: `CHANGELOG.md:14,28–31`. Tuy nhiên A2 ở dòng 173 nằm trong địa chỉ 168–179 của finding nợ cổng; A6 ở dòng 298 nằm trong địa chỉ 298–303 của **hai** finding lượt 7. Bảng mới vẫn gán chúng thành ngoài địa chỉ reviewer. Lỗi C1 cụ thể đã đóng; cùng lỗi phân hoạch còn sống.
- `message-moi-chieu-ba-cho-vao-sai-tep`: **ĐÃ VÁ THẬT** — CHANGELOG:562–567 đính chính đích danh commit `025c6b2`, tách C1/C2 ở r360 khỏi C3 trong thân PR và phân biệt #490/#494. Message lịch sử được giữ nguyên. Đây là đính chính có neo đúng, không đòi viết lại lịch sử; các sai mới của message được xét riêng.
- `mo-dau-r360-van-dem-sau-luot`: **ĐÃ VÁ THẬT** — CHANGELOG:193–197 bỏ số và dẫn đúng mục Cross-review PR #493. Bảng:433–441 có tám hàng, tám SHA/verdict/bộ ba finding đều khớp tám verdict được giao. Phân biệt “nhập hiện vật #491” với “tóm tắt #493” vẫn rõ. Một câu cũ “verdict gốc của bảy lượt” ở:430 là phần sót khác trong cùng đoạn B4, không làm câu mở đã sửa mất nghĩa.
- `runtime-pr491-luot1-mat-nhan-khi-chieu`: **ĐÃ VÁ THẬT** — README:290 có “ATTESTATION — toàn bộ khối runtime”; CHANGELOG:246–250 tách rõ 696s/rc0 khỏi số heading. Đếm verdict1: 3/5/6, 35088 byte, hash khớp receipt. Nhãn không hạ Git/băm/số finding thành tự thuật.
- `runtime-pr491-luot2-mat-nhan-khi-chieu`: **ĐÃ VÁ THẬT** — README:289 bao thời lượng/trạng thái chạy bằng nhãn toàn runtime; bảng r360 giải thích rõ 714s/rc0. Verdict2 đếm 0/3/10, 36958 byte. Cụm “chạy trọn ngay lần đầu” ở README thuộc khối runtime; các chỉ số Git/heading được loại rõ khỏi nhãn.
- `runtime-pr489-luot1-mat-nhan-khi-chieu`: **ĐÃ VÁ THẬT** — mục lục có đúng **1** hàng verdict1 tại README:288, giữ nguyên hàng master có nhãn toàn runtime. Đếm lần lượt c31d8f1/025c6b2/9349bb0/0721811/HEAD = 1/2/1/1/1. Không còn bản cũ thiếu nhãn.
- `runtime-pr489-luot2-mat-nhan-khi-chieu`: **ĐÃ VÁ THẬT** — cùng phép đếm cho verdict2 = 1/2/1/1/1, hàng giữ lại README:287 đúng nguyên byte của master. Cả bảng cảnh báo lẫn mục lục không có khóa trùng.

Tổng đối chiếu: **7 ĐÃ VÁ THẬT · 2 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Bốn sự kiện runtime lịch sử vẫn **KHÔNG ĐO ĐƯỢC độc lập** do thiếu run.json gốc; đóng lỗi mất nhãn không đồng nghĩa xác minh runtime.

## KIỂM INVENTORY LỚP VÀ LẦN MERGE

Bảng có đúng **13 ID duy nhất**, mỗi ID định vị được một chỗ khác nhau; A3 là một khối tại một chỗ, không tách tiêu đề và hai số byte thành ba đơn vị. A5 là khối nháp, A6 là nhãn cuối mục: hai vị trí khác nhau dù cùng finding từng dẫn tới chúng. Hàng D không có ID, mô tả phần không đụng tới, không thuộc 13.

Đối chiếu bên dưới dùng dòng **blob a4bc01d**, là SHA của lượt 7, không lấy số dòng đã trôi sau merge. Bốn vị trí ngoài Git (B1/B2/B3/C3) có vị trí hiện hành tương ứng và lời trích trong verdict cũ; **KHÔNG ĐO ĐƯỢC nguyên byte phiên bản cũ** của thân PR/script ngoài Git chỉ từ cây kho. Không biến trích dẫn của verdict thành blob nguồn đã phục hồi.

| ID | Vị trí đối chiếu | Trường TỆP/DÒNG lượt 7 có bao phủ? | Bảng khai đúng? |
|---|---|---|---|
| A1 | CHANGELOG cũ:16–19, câu thời điểm phát hiện | Có — `va-cham-r-ke-sai-thoi-diem-cu`:16–19 | Có |
| A2 | CHANGELOG cũ:173, “thứ duy nhất chặn…” | **Có** — `cong-byte-co-rang-cong-claims-khong-dem-su-that`:168–179 | **Không**, bảng ghi không |
| A3 | CHANGELOG cũ:278–284, khối printf | Có — `printf-khai-do-duoc-khong-co-payload-goc`:278–284,298–303 | Có |
| A4 | CHANGELOG cũ:294–296, endpoint chỉ có ba tool | Có — `ket-luan-thieu-tool-khong-co-inventory`:294–296 | Có |
| A5 | CHANGELOG cũ:139–146, khối nháp | Có — `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`:139–146,298–303 | Có |
| A6 | CHANGELOG cũ:298, nhãn “cho cả mục này” | **Có** — cả finding nháp lẫn printf dẫn 298–303 | **Không**, bảng ghi không |
| B1 | thân PR:13, chỉ dẫn “dưới” | Có — `than-pr-tro-muc-va-cham-khong-ton-tai`:13 | Có |
| B2 | thân PR:92–100, bảng “head này” | Có — `than-pr-khai-so-cong-cua-head-cu`:92–100 | Có |
| B3 | docstring trich_khang_dinh.py:6–11 | Có — `mo-ta-bo-trich-va-no-khong-theo-kip-ban-va`:6–11 | Có |
| B4 | CHANGELOG cũ:211–219, bảng ba lượt | Không; văn bản review có nhận xét “tóm tắt chọn lọc”, nhưng không có địa chỉ finding này | Có về cột địa chỉ; không phải lỗi |
| C1 | CHANGELOG cũ:14, land #490 rồi #494 | Có — `phan-vai-khai-duy-nhat-vuot-noi-dung`:14,28–31 | Có |
| C2 | CHANGELOG cũ:28, cũng kể #490 đã land | Có — cùng finding phân vai:14,28–31 | Có |
| C3 | thân PR:13, #494 land→merge | **Có địa chỉ :13** ở finding B1, dù finding đó chấm **mệnh đề chỉ dẫn khác** | **Không về địa chỉ**; chưa chứng minh lỗi C |

**Phân biệt cần giữ:** bao phủ một mệnh đề trong vùng TỆP/DÒNG không chứng minh reviewer đã phát hiện đúng khuyết tật mới ở mệnh đề đó. Nhưng cột được đặt tên là **“đã nêu địa chỉ?”**, và câu kết cũng nói **“ngoài địa chỉ reviewer nêu”**. A2/A6 thất bại theo chính tiêu chí đó. C3 và B1 là hai mệnh đề khác nhau cùng dòng thân PR: finding B1 chấm lỗi đích “dưới”, nhưng trường địa chỉ vẫn là :13. Áp nhất quán tiêu chí địa chỉ thì C3 cũng phải là “có”; không gộp C3 với B1 thành một ID, cũng không suy reviewer đã chấm trạng thái #494.

Theo phép nối vùng địa chỉ cho các mệnh đề A2/A6/C3 mà inventory đã chọn, tổng là **13 = 12 đã nêu địa chỉ + 1 còn lại (B4)**. Vị trí còn lại B4 không phải lỗi. C3 cũng chưa có nguồn phủ định, dù địa chỉ của đoạn thân PR ấy đã được dẫn. Có thể bàn riêng việc executor tự nhận diện hai khuyết tật A2/A6 trong vùng đã được dẫn, nhưng không dùng đó để khẳng định tìm ra hai lỗi **ngoài địa chỉ**. Không kết luận “executor không tự tìm được gì” hay “quét lớp vô ích”.

Riêng A2/A6 có đối chứng blob lịch sử nguyên byte, đã đủ bác9/4 và câu kết2lỗi ngoài địa chỉ ngay cả khi không dùng C3. Số12/1 dùng thêm định vị C3 ở thân PR:13 qua bản chiếu và verdict được giao; giới hạn không có raw thân PR cũ đã nêu trên.

**Tách bản vá khỏi merge:** `025c6b2→9349bb0` chỉ đổi CHANGELOG, manifest và README; `9349bb0→dd4a3ae` là merge master. Master đi thêm 12 commit so c31d8f1. Delta cuối so 0721811 chỉ tám tệp hồ sơ, +1588/−26; mã lease/workflow mới của master không phải sản phẩm riêng của PR493.

**Bốn số merge:** 0 số r trùng **đúng**; 257 cảnh báo **sai**, thực tế **258**; 103 mục lục **đúng**; 0 hàng trùng ở cả hai bảng **đúng**. Đếm cảnh báo theo khóa `(verdict_path, caveat_id)`, mục lục theo verdict_path (khóa mạnh hơn verdict_path+SHA); kiểm thêm trùng nguyên hàng cũng bằng 0. Hai parser độc lập đều ra 258. Diễn biến:

| mốc | cảnh báo | mục lục | pr489 lượt1/lượt2 |
|---|---:|---:|---|
| c31d8f1 | 247 | 100 | 1/1 |
| 025c6b2 | 256 | 104 | 2/2 |
| 9349bb0, sau vá trước merge mới | 256 | 102 | 1/1 |
| master 0721811 | 249 | 101 | 1/1 |
| dd4a3ae | **258** | **103** | **1/1** |

**Không thấy merge nuốt nội dung master:** tập 249 hàng cảnh báo và 101 hàng mục lục của master đều là tập con nguyên byte của HEAD; thêm đúng 9/2 hàng của nhánh. Hai cảnh báo pr490-review-7 còn đủ. r361, r359 và toàn bộ sau r358 khớp master nguyên byte; r358 chỉ có bản vá chủ ý của PR. Cả **11 tệp** master thay ngoài ba tệp giao nhau cũng khớp HEAD nguyên byte. `origin/master` không có ref trong bản sao giao; lệnh dùng literal ref ấy không chạy được. Đối chứng dùng **OID 0721811** đã xác minh bằng `refs/heads/master`, không tự tạo ref hoặc gọi mạng.

**Manifest:** chạy `release-manifest` trên bản sao đã khôi phục, ghi ra ngoài repo; output **khớp nguyên byte** RELEASE_MANIFEST.json. Điều này chứng minh kết quả tái sinh đúng, không xác thực thao tác shell lịch sử “đã tái sinh, không giải tay”.

**Tạo tác trạng thái đo được xác nhận:** trong bản sao riêng, giữ nguyên tất cả tệp của dd4a3ae và index, đặt detached HEAD về cha thứ nhất 9349bb0, MERGE_HEAD=0721811. `453c6bc` không là tổ tiên HEAD (rc1), là tổ tiên MERGE_HEAD/master (rc0). Bien_nhan báo đúng **1 vi phạm** evidence_url pr490-review-7, 49 đạt v2/tổng103. Đổi HEAD lại dd4a3ae, bỏ MERGE_HEAD: **0 vi phạm**, 50 đạt v2/tổng103; so byte cây tệp trước/sau không đổi. Đây là đối chứng cơ chế có kiểm soát, không khẳng định đã phục hồi transcript merge gốc. Trước commit, cổng đang bác đúng quan hệ với HEAD cũ; sau commit quan hệ mới đúng. Không gọi phép đỏ trước commit là bằng chứng cổng hỏng.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree | dd4a3ae | SHA đầy đủ đúng; tree 6134ee69f4e9a06870ee9e483d882aee495ac695 | Có |
| Base đã nhập | 0721811, master thêm12 commit | ancestry rc0; rev-list c31d8f1..0721811=12 | Có |
| First-parent 0721811..HEAD | chuỗi PR + vá + merge | 14 commit, mới→cũ: dd4a3ae,9349bb0,025c6b2,a4bc01d,cdd5891,2c57e99,7e236cf,f5098dd,b004da9,fae2fb7,9484970,4af7e29,cdd0b1d,34e9d35 | Có |
| Delta/awk | so base mới | **8 tep, +1588/-26**, khớp git diff --numstat | Có |
| Patch/numstat/message | trích Git | 4/4 khớp nguyên byte | Có |
| Bốn slice CHANGELOG | cắt heading thật | 4/4 byte-exact; heading361/360/359/358/356 tại1/187/657/777/1010 | Có |
| Thứ tự/số r trùng | 361→360→359→358;0 trùng | Đúng thứ tự;0 trùng toàn tập heading dev-side | Có |
| Bốn bản chiếu README/land/receipt | trích cây | 4/4 byte-exact | Có |
| ARTIFACTS.sha256 | toàn vẹn gói | **3288/3288**,0 sai | Có; không chứng thực nguồn GitHub |
| Ref snapshot |322/322/322, lệch0 | ba tập tên+OID bằng nhau; Git có322head ref | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Bộ trích | 10 input,2505 dòng | tái chạy byte-exact;2505 không rỗng,1586 có chữ số,0 loại | Có trong tập input |
| Bảng PR493 lượt1 |4af7e29;changes_requested;1/4/12 | cùng SHA/verdict/heading | Có |
| Bảng PR493 lượt2 |9484970;changes_requested;1/4/15 | cùng SHA/verdict/heading; đối chiếu0/6/11 | Có |
| Bảng PR493 lượt3 |fae2fb7;changes_requested;0/2/15 | cùng SHA/verdict/heading; đối chiếu7/3/10 | Có |
| Bảng PR493 lượt4 |b004da9;changes_requested;0/1/15 | cùng SHA/verdict/heading | Có |
| Bảng PR493 lượt5 |f5098dd;approve;0/0/14 | cùng SHA/verdict/heading | Có |
| Bảng PR493 lượt6 |2c57e99;changes_requested;0/0/10 | cùng SHA/verdict/heading; đối chiếu11/2/1 | Có |
| Bảng PR493 lượt7 |a4bc01d;changes_requested;0/0/9 | cùng SHA/verdict/heading; đối chiếu4/3/2/1 | Có |
| Bảng PR493 lượt8 |025c6b2;changes_requested;0/0/10 | cùng SHA/verdict/heading; đối chiếu7/0/1/1 | Có |
| Lần đầu VÁ HỜ=0 | lượt8 | lượt5 đã có0, VERDICT-LUOT-5:36 | **Không** |
| Inventory |13;9 đã nêu;4 tự tìm;2 lỗi ngoài địa chỉ |13 ID;12/1;0 lỗi được chứng minh ngoài vùng địa chỉ theo bảng | **Không** phân hoạch/kết luận |
| README sau merge |257/103;0 trùng |**258/103**;0 trùng cả hai bảng | **Sai số cảnh báo** |
| Master rows |giữ2 cảnh báo mới+9 của nhánh |master249+nhánh9=258; không mất hàng master | Có bảo toàn |
| Runtime491 |696s/714s,rc0 | nhãn toàn runtime đủ; thời lượng/rc lịch sử không có log gốc | KHÔNG ĐO ĐƯỢC runtime |
| Verdict491 |3/5/6 và0/3/10 | đếm heading khớp;35088/36958byte,băm khớp receipt | Có |
| ls-tree ops/reviews,ops/land |có491,không pr493-review-* | có2verdict+2receipt491;không verdict493; danh sách đầy đủ trong ls-tree.txt | Có |
| Manifest tái sinh |đúng sau merge |byte-exact với release-manifest mới | Có kết quả |
| release-verify --strict --json |xanh |rc0,ok=true,180/180;hai hash_match=true;failed/extra/errors rỗng | Có |
| doc-claims-check --strict --json |xanh |rc0,ok=true | Có trong phạm vi cổng |
| bien_nhan_v2 sau merge |0 vi phạm |rc0;50v2+11legacy+42nợ=103;0vi phạm;0KHÔNG ĐO ĐƯỢC | Có |
| bien_nhan_v2 trước merge commit |1 vi phạm453c6bc |rc1;49v2,tổng103,đúng1 lỗi; cây tệp không đổi | Có cơ chế |
| lease_publish_test |thân PR ghim121/121 ởa4bc01d | rc0; **146/146 đạt, đã chạy146, bỏ qua0** | Đo head mới riêng, không gán số cũ cho dd4a3ae |
| doctrine-scan --root . |rc0 |rc0;7tệp,0chép doctrine | Có |
| adr-song --root . |rc0 |rc0;46ADR/46hàng,khớp1–1 | Có |
| Ba mutant số |claims vẫn xanh |cả3rc0/ok=true;1byte mỗi ca,size865878 | Có; nợ D còn |
| Release mutant |phải chặn |rc2,failed chỉCHANGELOG,package_hash_match=false | Có răng |
| Bash printf |ca cụ thể lỗi, dấu trừ đơn không lỗi |rc2/stdout rỗng;rc0/`-`;ca%s rc0/nội dung đủ | Có |
| CI/approval/comment/endpoint lịch sử |lời thuật lại, có giới hạn |thiếu raw response/log/payload,không mạng | KHÔNG ĐO ĐƯỢC |
| Cổng thân PR |ghim a4bc01d,khác head GitHub4af7e29 |có nhãn SHA và trạng thái snapshot; không dùng số này cho head mới | Có phạm vi; GitHub hiện tại KHÔNG ĐO ĐƯỢC |

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Ba phép sai số vẫn qua cổng claims
LỚP: D
TỆP/DÒNG: CHANGELOG.md:371–383,588–594; scripts/tl_core/workflow.py:1163,1430,1488.
VẤN ĐỀ: Nợ cổng vẫn chưa đạt ba tiêu chí phản chứng. Không phải hồi quy do merge hoặc lỗi mới do PR hồ sơ gây ra; đây là finding được yêu cầu giữ mở tới hết P3. Ghi đúng địa chỉ và thừa nhận nợ không đóng hành vi.
CÙNG LỚP CÒN Ở ĐÂU: receipt-luot1.yaml:74–76, thân PR:68, phần nợ D trong message9349bb0. Các bản chiếu không có bằng chứng đóng hành vi.
ĐÃ THỬ VÁ: không sửa sản phẩm; đã thử ba mutant riêng trên bản sao, khôi phục từng ca. Hướng vá: successor có write set mã phù hợp kiểm mệnh đề hiện hành bằng Git/verdict có mốc, không hard-code số. Ca khóa: control xanh, cả ba mutant đỏ. Nguy cơ: kiểm nhầm trích dẫn lịch sử hoặc đánh đồng kiểm byte với kiểm chân trị.
ĐÃ THỬ NGHIỆM: `python3 -B review9-evidence/probes.py`; cả ba claims rc0/ok=true; release ca đầu rc2/failed chỉ CHANGELOG. Cổng xanh hiện tại không đủ đóng finding.
ĐỘ TIN: cao

### phat-hien-them-da-co-trong-verdict-bay  [P3]  A2, A6 và C3 vẫn bị xếp ra ngoài địa chỉ reviewer đã nêu
LỚP: C
TỆP/DÒNG: CHANGELOG.md:509,530,534,544–545,558–560,569–570; thong-diep-commit.txt:44–56; VERDICT-LUOT-7.md — trường TỆP/DÒNG của các finding nháp, nợ cổng, printf và chỉ dẫn thân PR.
VẤN ĐỀ: C1 đã được sửa, nhưng cột địa chỉ vẫn gán trạng thái “không được nêu” cho A2/A6/C3 trong vùng nguồn đã nêu. Tự đọc blob a4bc01d: A2:173 thuộc168–179; A6:298 thuộc298–303. C3 ở thân PR:13, cũng là địa chỉ B1 đã nêu (không phải cùng khuyết tật). Vì thế9/4 và “2 lỗi thật ngoài địa chỉ” sai theo chính đơn vị đang khai. Phép cộng13 đã đúng không cứu được phân hoạch. Không đồng nhất “đã dẫn vùng chứa mệnh đề” với “đã chấm riêng khuyết tật mới”; hai cột đó cần tách nếu tác giả muốn đo cả hai.
CÙNG LỚP CÒN Ở ĐÂU: heading kiểm kê, hai đoạn kết luận r360 và message9349bb0 đều mang cùng9/4/2. C1 đúng; không tái chấm trạng thái land#490 đã sửa. Sai mốc VÁ HỜ là sự kiện khác, chấm riêng.
ĐÃ THỬ VÁ: không — sửa inventory và sinh lại tổng từ quan hệ ID→mệnh đề→vùng TỆP/DÒNG trên SHA lượt7. Với tiêu chí hiện tại, ghi12/1 và không nhận2lỗi ngoài địa chỉ. Nếu muốn giữ công tự nhận diện A2/A6, đặt cột riêng về **khuyết tật đã được chấm**, trích nội dung finding thay vì tráo nghĩa cột địa chỉ. Đính chính message9349bb0 bằng văn bản có neo. Ca khóa: kiểm A2/A6/C1 và B1/C3 (hai mệnh đề cùng dòng); nguy cơ: đếm dòng thay mệnh đề, hoặc suy một vùng được dẫn thành mọi lỗi trong đó đã bị reviewer phát hiện.
ĐÃ THỬ NGHIỆM: `python3 -B review9-evidence/targeted.py`; đọc toàn bộ9 trường TỆP/DÒNG lượt7, nối tới blob a4bc01d;13ID,12có,1không; A6 được2finding dẫn nhưng chỉ tính1vị trí.
ĐỘ TIN: cao về mâu thuẫn cột địa chỉ; không chứng nhận ai nhận thức lỗi đầu tiên.

### bang-ba-luot-van-bi-goi-la-loi-da-va  [P3]  Đoạn dẫn bảng chưa theo phán quyết rút B4
LỚP: B
TỆP/DÒNG: CHANGELOG.md:428–431 đối chiếu552–554; muc-r360.md:242–245 đối chiếu366–368.
VẤN ĐỀ: Đoạn dẫn vẫn viết bảng ba lượt “cùng LỚP” với lỗi bản chiếu và “được vá cùng lớp chứ không đợi ai chấm”. Inventory mới lại nhận rõ B4 “không phải một lỗi”, không được tính công vá. Đoạn cũ không được đánh dấu trích dẫn đã rút, nên cùng mục đưa hai phán quyết hiện hành trái nhau. Câu kề đó còn nói “verdict gốc của bảy lượt” dưới heading/bảng tám lượt.
CÙNG LỚP CÒN Ở ĐÂU: đã vét phần giải thích B4 trong r360, message9349bb0 nhận phán quyết mới đúng; bản chiếu còn sống là đoạn dẫn trên. Thân PR chọn hai lượt để kể năm bản vá đầu không tự là lỗi.
ĐÃ THỬ VÁ: không — viết lại đoạn dẫn là mở rộng bản tóm tắt có ích, không coi bảng chọn lọc cũ là lỗi; bỏ số bảy hoặc ghim đúng tập lịch sử. Giữ phán quyết inventory thống nhất. Ca khóa: đọc đoạn dẫn cùng hàng B4 và đoạn kết sau nối dòng. Nguy cơ: biến mọi bảng tóm tắt chọn lọc thành bắt buộc liệt kê đầy đủ lịch sử.
ĐÃ THỬ NGHIỆM: đọc `review9-evidence/patch-only.diff` và hai đoạn tại exact tree; bản vá thay heading/thêm hàng8 nhưng giữ lời kết tội B4 cũ. Không cần dữ liệu mạng để thấy mâu thuẫn nội tại.
ĐỘ TIN: cao

### merge-khai-257-canh-bao-thuc-te-258  [P3]  Số cảnh báo tự khai đo sau merge thiếu một hàng
LỚP: B
TỆP/DÒNG: thong-diep-commit.txt:9–11 (message dd4a3ae); ops/reviews/README.md:13–274.
VẤN ĐỀ: Message merge gọi257 là số đã đo trên kết quả giải xung đột, nhưng bảng thật có258hàng dữ liệu. Master249+nhánh9=258; trước merge256+2=258. Số103mục lục và hai số0trùng đúng. Không có bằng chứng mất hàng; lỗi nằm ở bản chiếu kết quả đo, chính thứ message dùng làm bằng chứng đã khắc phục sai sót của merge trước.
CÙNG LỚP CÒN Ở ĐÂU: con số257 còn trong lời giao việc lượt9; trong các hiện vật hồ sơ được giao không tìm thêm bản chiếu hiện hành khác của nó.
ĐÃ THỬ VÁ: không — đính chính có neo dd4a3ae, nêu258 và phương pháp đếm dữ liệu giữa hai heading; lưu danh sách khóa làm chứng thay vì chép số tay. Không sửa/xóa hàng hợp lệ để làm số257 đúng. Ca khóa: tổng258,khóa duy nhất và tập hàng master là tập con; nguy cơ: trừ nhầm hàng đầu/cuối khi bỏ header hoặc đếm chỉ số verdict thay số caveat.
ĐÃ THỬ NGHIỆM: `python3 -B review9-evidence/measure.py` và `extra.py`: hai parser ra258;0khóa/0hàng nguyên văn trùng; missing_master_rows=[]; giữ đủ2cảnh báo pr490-review-7.
ĐỘ TIN: cao

### luot-tam-khong-phai-lan-dau-va-ho-bang-khong  [P3]  Bài học mới bỏ qua mốc 0 VÁ HỜ của lượt 5
LỚP: C
TỆP/DÒNG: CHANGELOG.md:449–453,572–574; thong-diep-commit.txt:34–36; VERDICT-LUOT-5.md:36.
VẤN ĐỀ: Tác giả dùng “lần đầu trong tám lượt VÁ HỜ bằng0” và “bảy lượt trước lần nào cũng có” làm bằng chứng riêng cho đổi cách vá theo lớp. Verdict lượt5 ghi rõ “17slug:3 ĐÃ VÁ THẬT · **0 VÁ HỜ** ·1 VÁ SINH LỖI MỚI ·13 CHƯA VÁ”. Chữ VÁ HỜ vẫn xuất hiện trong lượt5 khi kể lượt3/4; tìm sự có mặt của từ không phải đếm trạng thái lượt5. Lượt8 thật có0, nhưng không phải đầu tiên.
CÙNG LỚP CÒN Ở ĐÂU: cả hai đoạn r360 và message9349bb0 nêu trên; bảng8hàng không khai sai số finding. Câu “sáu lượt trước lần nào cũng có” ở:574 cũng vấp mốc lượt5.
ĐÃ THỬ VÁ: không — bỏ tính đầu tiên/toàn xưng; giữ số7/9đóng thật,0VÁ HỜ của lượt8 và so với từng mốc có dữ liệu. Đính chính message bằng neo9349bb0. Ca khóa: trích các tổng trạng thái từ phần đối chiếu từng verdict, với lượt5 làm phản chứng bắt buộc. Nguy cơ: grep từ “VÁ HỜ” trong toàn verdict rồi nhận trích dẫn lịch sử hoặc “0 VÁ HỜ” thành một finding VÁ HỜ; suy nhân quả đổi phương pháp chỉ từ một chỉ số.
ĐÃ THỬ NGHIỆM: `rg -n 'VÁ HỜ|Tổng' VERDICT-LUOT-5.md`; dòng36 là tổng trạng thái, dòng32/63 chỉ nhắc lịch sử lượt3/4. Đọc lại phần đối chiếu lượt5 và lượt8 xác nhận cả hai đều0.
ĐỘ TIN: cao

**Kết luận: 0 P1 · 0 P2 · 5 P3 — changes_requested trên exact SHA đã giao.** Merge bảo toàn nội dung master và hai chiều ancestry đúng; các bản vá runtime/printf có hiệu lực. Những điều đúng ấy không đóng nợ cổng hoặc chữa các lời khai kiểm kê còn sai. Không đăng review, không sửa kho được review, không push/merge.
