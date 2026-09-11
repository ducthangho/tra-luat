verdict: changes_requested
reviewed_sha: f6ec9c0650de2716776e8b58a63b3141095097fa

**0 P1 / 8 P2 / 0 P3.** Cổng và các mỏ neo đều đạt; lời khai về việc đã vá hết chưa đúng. Không phát hiện lệch giữa cấu hình gói hiện tại, `do-goi.txt` và `EVIDENCE.md`. Có lỗi mới trong chính biên nhận lượt 4 và bảng tự đính chính.

## ĐỐI CHIẾU LƯỢT 4

- `phep-grep-prompt-khong-ghim-snapshot-sau-khi-nhap-verdict`: **VÁ HỜ** — năm vị trí được kể thực sự đã đổi: grep BN1, diff tại CHANGELOG §3/§4, BN3 và README lượt 3. Nhưng đó không phải danh sách đầy đủ: BN2:80 còn “trên HEAD nay trả HAI”; BN3:120,125 còn `HEAD ⇒ 2` và “HEAD nay có hai tệp”; CHANGELOG:290,450 và README:274 cũng tiếp tục dùng kết quả ấy. Lấy digest từ YAML rồi `git grep -l <digest> <sha> -- .`: `1d58500/4e6a2d5/25974e7/f6ec9c0` lần lượt **1/2/3/4 tệp**. Không sửa các verdict nguyên văn đã neo băm.
- `attestation-runtime-bi-nang-thanh-phep-do`: **VÁ HỜ** — 5 vị trí đã sửa nhưng có **6 vị trí** trong finding cũ: CHANGELOG, BN1/2/3, hai hàng README lượt 1/2. BN1:77–80 còn nguyên câu khớp OID là bằng chứng reviewer “đọc đúng cây”. Chuỗi được hỏi, tìm phân biệt hoa thường trên từng dòng, đúng là **0**; nó bị ngắt dòng tại `đúng`/`cây`. Đọc scalar YAML nối dòng thì câu khẳng định vẫn còn. BN4:67 còn tự chứa một bản viết hoa đầu câu của chuỗi mà nó khai đã hết. Lỗi thực chất là suy hành vi từ OID còn tồn tại, không phải việc giữ trích dẫn lịch sử.
- `dem-finding-doi-mau-va-bo-sot-phan-moi`: **ĐÃ VÁ THẬT** — README:275 đã sửa cả hai số: P2 **1→7**, tổng **2→7**, bề mặt phát sinh sau lượt 1 **6/7**. Đếm tiêu đề V1/V2 được `0/1/1` và `0/7/0`; `git log -S 'Không cổng nào' f6ec9c0 -- CHANGELOG.md` xác nhận câu của finding thứ bảy được thêm tại `52b36d1`, sau `e826730`. Tiêu chí “phát sinh sau lượt 1” ở đây khác tiêu chí đường dẫn của bảng mới §4; không dùng hai mẫu số thay nhau.
- `bang-cong-r362-con-neo-so-truoc-bien-nhan-luot-hai`: **VÁ HỜ** — số sai tại BN3 đã sửa thật, có mốc `25974e7`. Chạy validator trên bốn bản chép checkout từng SHA cho **49/102, 50/103, 51/104, 52/105**, đều rc=0. Nhưng lời hứa “mọi con số phải neo commit” chưa áp đầy đủ: CHANGELOG:341 dùng **“head hiện tại (có biên nhận lượt 4)”**, bảng :346 không có SHA cố định. Số hiện tại đúng; phép dẫn nguồn vẫn phụ thuộc lúc đọc. Các câu kể HEAD của lượt 3 tại :289/:452, BN3:97 và README:274 cũng nên ghi thẳng `4e6a2d5`. Xem finding về snapshot; không chấm riêng lần nữa cùng nguyên nhân.
- `hai-loi-khai-thieu-nhan-va-sai-co-trang`: **VÁ HỜ** — `ops/cong_cu.py:209–229` đã dán nhãn đúng và phân biệt cơ chế với sự kiện; bảng CHANGELOG:416–428 đã tách bốn verdict đếm được khỏi connector thuật lại. Tuy nhiên BN3:149–155 vẫn đặt connector trong `do_duoc.so_luot_bi_cham: 4`, chỉ liệt kê ba tệp verdict, và còn chỉ dẫn cộng dòng ĐỐI CHIẾU. Ở §2, nhãn :107 chỉ nói **“DƯỚI ĐÂY”** trong khi câu thuật lại JSON Windows ở :103–105 nằm phía trên. Đây vẫn là hai chỗ sót của cùng finding.

## BẢNG ĐO

Quy ước: C = `cay-kho/CHANGELOG.md`, BNn/Vn = biên nhận/verdict PR497 lượt n, MLn = hàng mục lục lượt n. Các phép đọc Git dùng clone được giao; các cổng, checkout lịch sử và đột biến chạy trên bản chép trong sandbox, với thư mục tạm cũng ở trong sandbox. `KHÔNG ĐO ĐƯỢC` không được tính là đạt. Những số runtime lịch sử dưới đây chỉ được kiểm số học hoặc đối chiếu với lời reviewer ghi, không được chứng thực bằng việc chạy lại hôm nay.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head/tree của gói | `f6ec9c0` / `fc13419…` | `f6ec9c0650de2716776e8b58a63b3141095097fa` / `fc13419ae063b9985d5e6636b9b69c8381b12d2e` | Có |
| Clone đầy đủ, abbrev, sạch | false / 7 / true | `rev-parse --is-shallow-repository`: false; `config --local --get core.abbrev`: 7; `status --porcelain`: rỗng | Có |
| Origin | mirror trong sandbox | Đúng đường dẫn tuyệt đối tới `kho.git` đã in trong `do-goi.txt` | Có; không phải GitHub |
| Chín trường cấu hình | EVIDENCE = do-goi = thực tế | Tái dựng đủ 9 key/value, so từng giá trị và khối code EVIDENCE: **9/9** | Có |
| Mirror | 324 = 323 + 1 | `for-each-ref refs/heads`: 324; đúng 1 `pr497-head`; loại công khai ref ấy còn 323 | Có |
| Bộ đệm clone | tập cục bộ | Bỏ alias HEAD còn 324 remote-tracking refs; không nhầm đây là tập máy chủ | Có về dữ liệu cục bộ |
| Raw máy chủ được giao | 322 dòng, băm `ec6ef20a…` | **322 dòng, 25.944 byte**, SHA-256 `ec6ef20af4eb7f734fcb0e321c86b93d0efbb34493630e968fcfb138b51b5ec8` | Có về byte |
| Xuất xứ/giờ raw | GitHub; `2026-09-10T09:42:24Z` | **KHÔNG ĐO ĐƯỢC**: tệp không chứng thực nơi và lúc tạo | ATTESTATION |
| Raw so mirror đã bỏ giao hàng | canh hai tập tên | Thiếu 0, thừa đúng `pr487-merge`: 1; **322 OID chung, 0 lệch** | Có về tập đã giao; không chứng thực việc xóa nhánh trên GitHub |
| Ref r360 | nhánh khác có r360 | Có tiêu đề r360 trên `claude/pr491-land-va-findings-wip`; trạng thái PR/phiên **KHÔNG ĐO ĐƯỢC** | Có phần object/ref |
| Quét r362 | 1 trong 323; 2 trong 324 | Đúng `claude/handoff-tra-luat-repo-2ak5th` và `pr497-head`; bỏ giao hàng còn 1 | Có |
| Quét r363 | 1, nhánh land-492-bookkeeping | Đúng 1, `claude/land-492-bookkeeping` | Có |
| Nhánh từng mù lần đầu | wp484-g3-windows mang r356 | Ref hiện có, dòng đầu CHANGELOG là r356; việc từng mù **KHÔNG ĐO ĐƯỢC** | Một phần |
| Canh lịch sử lần 1 | 320/320; mù 1; sau fetch 0; quét 320 | **KHÔNG ĐO ĐƯỢC**: không snapshot máy chủ/bộ đệm trước fetch | Nhãn THUẬT LẠI đúng |
| Canh lịch sử lần 2 | 322/321; mù 2; thừa 1; sau fetch 0 | **KHÔNG ĐO ĐƯỢC** trạng thái trước fetch; tên hai nhánh và ref thừa hiện có | Nhãn THUẬT LẠI đúng |
| Số học của hai tập lệch | tổng lệch 1 nhưng thiếu 2 | `322−321=1`; `2−1=1` | Có; số đếm không xác định hiệu tập |
| Ngày/nội dung r362 | 10-09-2026; hai việc | Commit đầu `25c2d5b`, hai việc ở §1/§2; hiện có §1–§4 | Có về văn bản/Git |
| VERSION | không nâng; 1.36.68 từ r336 | VERSION tại `3dcdc6a`, `0721811`, SHA review đều **1.36.68** | Có |
| Diff gói | 12 tệp, +2446/−5, 12 commit | Cộng `git diff --numstat 0721811 f6ec9c0`: đúng; `rev-list --count`: 12; diff.patch và numstat khớp Git từng byte | Có |
| Chi tiết 12 tệp | numstat.txt | C +506; manifest +5/−5; cong_cu +23; README +6; V1/BN1 +161/+221; V2/BN2 +259/+282; V3/BN3 +285/+253; V4/BN4 +296/+149 | Có |
| Master đã hợp nhất | `0721811`, từ `28ba133` | `merge-base --is-ancestor 0721811 f6ec9c0`: rc=0; merge `1e75335` có cha `52b36d1` và `0721811` | Có trong Git |
| Giao write set | master đổi 3 tệp; giao 0 | Đúng workflow thu hồi, lease_publish.py, lease_publish_test.py; giao với write set nhánh bằng rỗng | Có; không chứng thực nhật ký thao tác merge |
| cong_cu.py chỉ thêm chú thích | không đổi runtime | `ast.dump(ast.parse(...))` tại `0721811` và SHA review bằng nhau | Có |
| Manifest | 180→180; 1/12 tệp đổi thuộc kiểm kê; 0 ops | Đúng; tệp giao duy nhất là CHANGELOG, manifest không kiểm kê chính nó | Có |
| Toàn vẹn manifest | toàn bộ size/hash đúng | Tự băm **180/180**, 0 lệch; tổng **8.156.216 byte** đúng `total_bytes` | Có |
| package_hash/content_hash | manifest hiện tại | Cả hai `f6a0e19639bbf0c511d07c83b2075c9dff116ca316cbf82239d7c0d3864d56b2`; strict verify đạt | Có |
| ADR-0034, #490 | ba vế merged/gate/bookkeeping | Quy tắc ba vế có trong tài liệu; merge và mục r359 có trong Git | Có phần quy tắc và hồ sơ |
| Merge #490 | `8cee941`, 2 cha `00e017a` + `01e7f77` | `show -s --format='%H %P'`: `8cee9410e958a6b9d956e080c11878fbd80d9f5f`; cha `00e017af102bc8355e0c276d2d813e20620ddb42`, `01e7f77d707cb093b5ba6d9b9d8577f40d025488` | Có |
| 0 hiện vật CI ở r359 | không response CI neo merge trong cây | `git grep -l 8cee941 71e0053 -- .` chỉ trả CHANGELOG; SHA mới thêm hồ sơ thuật lại, không có response Actions trong các kết quả | Có trong phạm vi tìm; không suy CI chưa chạy |
| Ubuntu: 41 bước | 37 success + 4 skip + 0 failure | Cộng =41; kết quả runtime **KHÔNG ĐO ĐƯỢC**, thiếu response job | Chỉ khớp số học |
| Windows: 41 bước | 35 success + 6 skip + 0 failure | Cộng =41; runtime **KHÔNG ĐO ĐƯỢC** | Chỉ khớp số học |
| Giờ Ubuntu | 18:50:37→19:11:32 | Hiệu **1255 s = 20m55s**; hai mốc thực **KHÔNG ĐO ĐƯỢC** | Chỉ số học |
| Giờ Windows | 18:50:37→19:44:09 | Hiệu **3212 s = 53m32s**; hai mốc thực **KHÔNG ĐO ĐƯỢC** | Chỉ số học |
| Run #490 | 34391481045; push/master; attempt 1; không rerun; xanh hai nền | **KHÔNG ĐO ĐƯỢC**: không mạng/response Actions | Không tự chứng nhận landed |
| Hai run so sánh | `7693852` attempt 2; `28ba133` attempt 1 | Commit có thật; workflow tại hai SHA, `8cee941` và SHA review cùng blob `2e21c0c1f0701e837f7c13fa20a55ab39fd5805c`; attempts/trạng thái **KHÔNG ĐO ĐƯỢC** | Một phần |
| Ba run cùng mẫu skip; #11,22,23,38,39 | LAND đúng mẫu; 4/6 skip | Điều kiện YAML phù hợp PR-only, Linux/không Linux, LAND/WORKER; quan sát ba run **KHÔNG ĐO ĐƯỢC** | Không lấy cấu hình làm log |
| Toàn CI | 31 bước cổng | Parse job gate: **40 mục = 8 setup + 31 cổng + 1 upload**. Số 41 của runtime tính thêm setup job không đo trực tiếp được | Có về YAML |
| Nợ treo | khoảng vài giờ, rút ~7 giờ | **KHÔNG ĐO ĐƯỢC**: không mốc đọc CI; giờ commit không thay được nó | Giới hạn đã khai |
| A/B có shellcheck | actionlint/shellcheck/canary DAT, SC1003 rc=1 | Chạy CLI: rc=0, tổng DAT, đúng SC1003/rc=1 | Có |
| A/B thiếu shellcheck | shellcheck KHONG_DO_DUOC; canary DO/blocking | Chạy CLI: rc=2, tổng DO, canary SUY_GIAM/rc=0; **7 công cụ còn lại vẫn DAT** | Có |
| Quét riêng shellcheck thiếu | canary=[], tổng DAT | `kiem-tra --chi shellcheck --json`: rc=0, shellcheck KHONG_DO_DUOC, canary rỗng | Có |
| Hai phép chạy bác lời r361 | full scan A/B | Hai full scan tái hiện DAT→DO; số lần điều phối đã chạy trước đây **KHÔNG ĐO ĐƯỢC** | Có về cơ chế |
| #7 shellcheck, #8 rg, #9 G5 | installer gọi --chi; G5 không --chi | YAML thứ tự 6/7/8, phù hợp số kể nếu cộng setup job; đọc installer xác nhận --chi; rg bắt buộc, shellcheck không | Có về mã |
| Windows từng đỏ | #7 xanh, #8 đỏ, #9 skip | Cơ chế cho phép; sự kiện/JSON lịch sử **KHÔNG ĐO ĐƯỢC** | Nhãn trong mã đúng; C:103–105 còn nằm ngoài nhãn “dưới đây” |
| “tệp này đã ghi ba lần” | 3 lần cùng kiểu suy từ rỗng | **KHÔNG ĐO ĐƯỢC** số phân loại: không chỉ ba đoạn hoặc quy tắc chọn | Không nhận là số đã tái lập |
| Packet #290 | xuất xứ, spec đóng băng; successor/corrective | Đọc spec/protocol phù hợp; trạng thái landed và quyền GitHub **KHÔNG ĐO ĐƯỢC** | Có phần quy tắc |
| Dẫn protocol | 28/116/164 là dòng; tối đa §20; AGENTS:22–23 | Đếm được **20** mục; ba dòng chứa đúng ba câu trích, AGENTS đúng | Có |
| Connector trước lượt 1 | 3 P2, 2 ở đoạn nhận việc | V1 liệt kê ba slug; review GitHub gốc **KHÔNG ĐO ĐƯỢC** | Chỉ kiểm lời thuật lại |
| Quét Issue cũ/mới | trang 30, 0 khớp; 128 mở; total_count 101 | **KHÔNG ĐO ĐƯỢC**: thiếu response/query/phân trang | Nhãn Issue đã có |
| 30/128 ≈23% | tỷ lệ cỡ trang | **23,4375%** | Có về phép chia; không chứng thực đầu vào |
| Bốn Issue, nợ #498 | #249/#295/#269/#297; đã mở #498 | Đếm đúng 4 ID khác nhau; nội dung/trạng thái/việc mở Issue và phiên đang chạy **KHÔNG ĐO ĐƯỢC** | Đã thuật lại |
| V1: byte/dòng/băm | 28955/161/a6bf4bea… | **28955/161**, SHA-256 `a6bf4bea67c347385960285c5e5d0d28346887da684595b6429f22a6d67aed27` | Có |
| V2: byte/dòng/băm | 43791/259/206aaf28… | **43791/259**, SHA-256 `206aaf2814c5cb249506b6ae607b17a9071ac4d50eeea51b5cb031ca92531b00` | Có |
| V3: byte/dòng/băm | 48843/285/9a244e3d… | **48843/285**, SHA-256 `9a244e3d5cb9adfdda4842b207019018c7f805c936d12160cdd6eeaf51f7f86b` | Có |
| V4: byte/dòng/băm | 51844/296/30a0ddea… | **51844/296**, SHA-256 `30a0ddeaa852c9a56ff669374a7c8ef009a3bcf4b27360f13d3af7fe0f95f1bd` | Có |
| so_p1/2/3 của cả bốn | 0/1/1; 0/7/0; 0/6/0; 0/5/0 | Đếm riêng từng hạng từ tiêu đề `^### .*\[P[123]\]`: đúng cả **12 số**, tổng **2/7/6/5** | Có; `Pn` trong hướng dẫn phải được thay bằng từng hạng |
| reviewed_sha / tree V1 | e826730 / 67df2efa… | `e82673014baefca23b50663cecad80fdbde79b3b`; tree `67df2efa7e6f6c7b23bedfb43da647b395800a37` | Có về OID |
| reviewed_sha / tree V2 | 1d58500 / 0430d2bd… | `1d58500b2ecaf7ccd38dcc6f8ad9bf0dbf13c77e`; tree `0430d2bdbc8e6e6c11bbf93c8bb12b1272b1202d` | Có về OID |
| reviewed_sha / tree V3 | 4e6a2d5 / 115b1835… | `4e6a2d59386335f966bfb7160e98af02ae30d1ec`; tree `115b1835be0a14c63669357a4c8e05a0ad542c4a` | Có về OID |
| reviewed_sha / tree V4 | 25974e7 / 1d303009… | `25974e78ac4dbeb67db5f797b08b4dd276d0d666`; tree `1d303009eaef2471c4c51a449f46abef1d4bc58b` | Có về OID; không xác thực hành vi đọc |
| evidence_url V1 | neo commit thêm đầu tiên | `git log --all --diff-filter=A --format=%H -- <path>` trả đúng 1: `8104480fe756978455abf1baf96adf6f9b399cbb` | Có về object/path/băm; khả năng truy cập GitHub KHÔNG ĐO ĐƯỢC |
| evidence_url V2 | như trên | Đúng 1: `4d2a6f69e67ce5299253bf8905b6b742d516f3fc` | Có, cùng giới hạn |
| evidence_url V3 | như trên | Đúng 1: `60b99bdf1bb644912c10df09d05b303c73d23ccc` | Có, cùng giới hạn |
| evidence_url V4 | như trên | Đúng 1: `5ef3b3d3a9e7a1a5d4a50ff9175c5c2bce837012` | Có, cùng giới hạn |
| Bốn quan hệ tổ tiên | neo canonical_ancestry | reviewed_sha→neo và neo→SHA review: **8/8 rc=0**; neo→origin/master `0721811`: **4/4 rc=1**; blob ở neo bằng byte hiện tại | Có điều kiện; chưa là tổ tiên master |
| Ba lối land | merge/FF giữ; squash có thể phá neo mới | BN1/2/3/4 dẫn phép thử cũ và giới hạn đúng; suite bien_nhan_v2_test chạy lại c45 đạt | Có về fixture; không đo nút merge/chính sách GitHub |
| Tách hai commit mỗi hồ sơ | commit nhập verdict đỏ t27; commit sau xanh | `8104480→52b36d1`, `4d2a6f6→4e6a2d5`, `60b99bd→25974e7`, `5ef3b3d→f6ec9c0`: **rc 1→0 cả bốn** | Có; lỗi đầu tiên thực tế là thiếu hàng mục lục |
| Runtime BN1–4 | 878.149 / 1242.188 / 1477.302 / 1356.61 s | Trừ timestamp khai được **878.148880 / 1242.187745 / 1477.301757 / 1356.609529**; làm tròn đúng; thời gian thực **KHÔNG ĐO ĐƯỢC** | Chỉ số học |
| Runtime README | 878 / 1242 / 1477 / 1357 s | Làm tròn bốn scalar biên nhận đúng | Chỉ số học |
| Các scalar runtime khác | model yêu cầu, run IDs, prompt/stdout/stderr hash/byte, rc=0, lần chết 1/0/0/0 | **KHÔNG ĐO ĐƯỢC**: không có bốn run.json/log/prompt; model phục vụ cũng không đo được | Không có ngoại lệ cho prompt hash |
| Tuân thủ/sự cố runtime | sạch, 0 commit thêm; probe rc=0; 0 lỗi mạng; lỗi 111; dang_chay/null | **KHÔNG ĐO ĐƯỢC** phiên cũ; chỉ đọc được người viết khai gì | Không lấy lời tự khai làm phép xác thực |
| Cơ chế launcher | expected-repo thiếu remote chặn 11 | Dựng kho trống trong sandbox; `chot_kho(...,'ducthangho/tra-luat',None)` ném `Chan`, `ma=11`, `(khong co remote)` | Có về cơ chế; cờ phiên cũ là ATTESTATION |
| Root commit | 394e9346… | `rev-list --max-parents=0 f6ec9c0`: `394e93468fc8d84ec20938e6df8fb7ab72b2cc37` | Có |
| V1 có 28 hàng KĐĐ | sửa từ 17; quy tắc cắt bảng | Cắt BẢNG ĐO tới “Đột biến và phép thử”, đếm dòng bảng có đúng nhãn: **28** | Có; không tự gán cả 28 cho GitHub |
| V1 có 13 ca, 5 ca lời khai | bảng đột biến đã chạy | Đếm **13 hàng** trong bảng V1; chạy lại **5/5** thay đổi lời khai: hai cổng đều cho qua sau tái sinh manifest | Có về bảng và phép chạy lại; không chứng thực runtime cũ |
| “Ba trong bảy” ở hồ sơ lượt 1 | attestation, đếm hàng, kể lý do | V2 đúng ba finding này nhắm BN1/README; finding kể lý do còn chạm nơi khác | Có, không loại trừ các vị trí khác |
| Tổng/bề mặt mới lượt 2 | P2 1→7, tổng 2→7, mới 6/7 | Khớp tiêu đề và lịch sử câu thêm `52b36d1`; README:275 đã sửa | Có |
| Đếm slug hai-loi-khai | 4 lượt file + 1 connector thuật lại | **1 tiêu đề trong mỗi V1–V4**, tổng 4; connector **KHÔNG ĐO ĐƯỢC** | Bảng C đúng, BN3 vẫn gộp nguồn |
| Số lượt lặp các slug lượt 4 | grep 2; attestation 3; đổi mẫu 2; bộ đếm 2; hai-loi-khai 4 | Đếm tiêu đề trong V1–V4 lần lượt **2/3/2/2/4** | Có; số lượt không tự chứng minh vá xong |
| Năm finding lượt 4 đều đã vá hết | 5/5; còn 0 | Còn các chỗ sót nêu ở ĐỐI CHIẾU | Không |
| Bảng tự đính chính §4 | 0/2 · 5/7 · 4/6 · 5/5 | Theo tập đường dẫn toàn trường TỆP/DÒNG, giải nghĩa tên viết tắt: **0/2 · 6/7 · 6/6 · 5/5** | Không; xem phép tái lập bên dưới |
| Nội dung gốc còn bị chấm | cong_cu.py ở lượt 2/3/4 | TỆP/DÒNG của hai-loi-khai tại cả V2/V3/V4 chứa đúng đường dẫn ấy | Có |
| Phạm vi §3/README | BA lượt; 3 hàng mục lục + 2 cảnh báo | **4 lượt**, **4 hàng mục lục + 2 cảnh báo = 6**; đúng các hàng README 17,18,273–276 | Không ở lời tổng kết C |
| Cắt ngắn BN4 | 253→146; bớt 107 | `wc -l`: **253→149; bớt 104** | Không; numstat.txt khai 149 đúng |
| BN4 chỉ trường đo được + một dòng/finding | bỏ văn xuôi, lớp rủi ro đã chết | 5 object finding ở **dòng 53–95**, mỗi object nhiều trường/văn xuôi; còn phần dẫn giải 5–16, 97–101 và nguồn ngoài kho | Không |
| Gói lượt 3/4 sạch | 9/9; mirror 324; raw 322 | V3/V4 đúng có ghi các kết luận đó; gói cũ **KHÔNG ĐO ĐƯỢC** độc lập từ gói hiện tại; gói hiện tại đo lại khớp | Không suy thành đã đóng mọi lỗi cùng lớp |
| Các bài học CLAUDE.md | ngưỡng ≥3; bốn lượt vá; bảy phát hiện | Đoạn CLAUDE:723–729 có câu ngưỡng và lời kể tương ứng; số sự kiện lịch sử **KHÔNG ĐO ĐƯỢC** chỉ từ việc trích câu ấy | Có về nguồn văn bản |
| lease_publish_test tại SHA review | 146/146, đã chạy 146, skip 0 | `python3 ops/lease_publish_test.py`: **rc=0, 146/146, chạy 146, skip 0** | Có |
| lease_publish_test trước merge | 121/121 | Bản chép checkout `52b36d1`: **rc=0, 121/121, chạy 121, skip 0** | Có |
| bien_nhan_v2 tại SHA review | 52 đạt v2, 11/11 legacy, 42 nợ, 0 vi phạm, 0 KĐĐ, tổng 105 | `python3 ops/bien_nhan_v2.py --root .`: **rc=0**, đúng mọi số, TỔNG ĐẠT | Có |
| Chuỗi bộ đếm ghim SHA | 49/102→50/103→51/104→52/105 | Checkout riêng `4d2a6f6/4e6a2d5/25974e7/f6ec9c0`, chạy validator: đúng, cả bốn rc=0 | Có; C vẫn dùng mốc “head hiện tại” cho số cuối |
| bien_nhan_v2_test | 48/48; 63/63 mutant; 2/2 tự kiểm | **rc=0**, đúng cả ba; suite còn ghi 45/63 mutant thường có đối chứng | Có; không gọi 63 là toàn không gian lỗi |
| cong_cu / cong_cu_test | DAT, canary DAT; ca23/mutant18/lỗi0 | Cả hai **rc=0**; đúng **23/18/0** và canary SC1003 | Có |
| Phiên bản nền và pin | actionlint1.7.7, shellcheck0.9.0, jsonschema4.26.0; chỉ 2 được ghim | Công cụ trả đúng ba bản; ci.yml ghim actionlint/jsonschema, shellcheck.ban_ghim=null | Có |
| Thiếu jsonschema ở lượt cũ | lỗi mutant=1, tổng DO | Phiên cũ **KHÔNG ĐO ĐƯỢC**; nền hiện tại có 4.26.0, chạy ra lỗi0 | Không gọi khác môi trường là lỗi mã |
| release-verify | ok=true, expected=checked=180 | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json`: **rc=0, true, 180/180** | Có |
| golden-test | ok=true | `python3 scripts/tl.py golden-test --json`: **rc=0, true** | Có |
| determinism-audit | ok=true | `python3 scripts/tl.py determinism-audit --strict --json`: **rc=0, true** | Có |
| doc-claims-check | ok=true | `python3 scripts/tl.py doc-claims-check --strict --json`: **rc=0, true** | Có |
| workflow-audit | rc=0 | `python3 scripts/tl.py workflow-audit --strict --json`: **rc=0, true**, errors=[] | Có |
| doctrine-scan | rc=0 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **rc=0**, 7 tệp, 0 chỗ chép | Có |
| adr-song | rc=0 | `python3 .claude/dev/packet_loop.py adr-song --root .`: **rc=0**, 46 ADR/46 dòng, ngoại lệ 0016 như cổng khai | Có |
| 12 lệnh tại chỗ là đủ CI? | KHÔNG đủ | Đã chạy lại đủ 12 lệnh EVIDENCE; không chạy toàn bộ 31 bước cổng | Giới hạn EVIDENCE đúng |

**Đột biến và đối chứng đã chạy.** Phép A/B công cụ dùng cùng một bản kê chép từ YAML: ghim đường gọi executable cho bảy công cụ khác, giữ shellcheck tra theo PATH. Đổi PATH từ môi trường hiện tại sang thư mục rỗng trong sandbox; không đọc/sửa nội dung executable hệ thống. Kết quả bảy probe khác giữ DAT, chỉ shellcheck mất. Đây là điều kiện đo cụ thể, không giả log Windows.

| ca trên bản chép | cổng | nền → đột biến → phục hồi | kết luận |
|---|---|---|---|
| Bỏ verdict V1/V2/V3/V4, giữ BN + ML | t27 | **0→0→0 cả 4** | t27 không kiểm sự tồn tại tệp được BN trỏ tới |
| Cùng bốn ca mất verdict | t26 | **0→1**, lỗi đúng tên tệp mất; phục hồi đạt | Chốt này thuộc t26 |
| Bỏ BN1/2/3/4, giữ verdict + ML | t27 | **0→1→0 cả 4** | Có răng, đúng lý do thiếu biên nhận |
| Bỏ ML1/2/3/4, giữ hai tệp | t27 | **0→1→0 cả 4** | Có răng, đúng cột tệp verdict trong mục lục |
| Bỏ riêng từng hàng cảnh báo V1/V2 | t27 | **0→1→0 cả 2** | Có răng, báo đúng ID cảnh báo |
| Thay `if chi is None` bằng `if False` | ca t13 cong_cu_test hiện có | **0→1→0** | Bắt việc mất vòng canary |
| Đổi số Issue, giữ manifest cũ | release-verify strict | **0→2**, đúng CHANGELOG lệch hash, size không đổi | Có răng với byte |
| Cùng thay đổi, tái sinh manifest | doc-claims strict + release-verify strict | **0→0** cả hai | Không bắt nghĩa số Issue |
| Đổi 37 thành 36 nhưng giữ 4 skip và tổng41 | hai cổng trên, tái sinh manifest | **0→0** cả hai | Không bắt mâu thuẫn cộng này |
| Đổi cha thứ nhất thành cha thứ hai đã có trong Git | như trên | **0→0** cả hai | Không kiểm quan hệ cha trong câu |
| Đổi nhãn “xuất xứ” thành “chủ” | như trên | **0→0** cả hai | Không kiểm nghĩa thẩm quyền trong câu |
| Đổi mù1 thành mù0 | như trên | **0→0** cả hai | Không kiểm lời kể lịch sử tập ref |

Không suy năm mutant sống sót trên hai cổng thành “mọi cổng đều không có răng”; cũng không yêu cầu xây cổng ngữ nghĩa. Tất cả thay đổi trên được trả lại sau từng ca.

**Biên nhận lượt 4 có mất thông tin cần thiết không?** Không phát hiện mất trường bắt buộc của hợp đồng biên nhận hiện hành: validator chấp nhận, hash/path/SHA/evidence/identity/anchor còn đủ; năm slug vẫn có, V4 nguyên văn còn đủ bảng đo và giới hạn. Việc không tạo caveat mới phù hợp với V4 không báo lỗi gói mới. Không cần khôi phục các khối bài học BN3 chỉ để đạt độ dài cũ. Tuy nhiên, “chỉ giữ trường đo được”, “một dòng mỗi finding” và “kết quả cổng” không mô tả đúng BN4 hiện tại: phần kết quả cổng chi tiết vẫn phải tìm ở V4/CHANGELOG, còn BN4 vẫn giữ nhiều lời khai mới. Giới hạn nguồn lại bị nới ở đầu tệp, như finding bên dưới.

### phep-grep-prompt-khong-ghim-snapshot-sau-khi-nhap-verdict  [P2]  Danh sách năm vị trí đã sửa vẫn bỏ sót kết quả HEAD đang trôi

TỆP/DÒNG: BN2:78–83; BN3:116–125; C:290,450; README:274; đối chiếu lời khai đủ 5/5 tại BN4:59 và README:273. C:337–346 là cùng thiếu sót ghim mốc đối với bộ đếm biên nhận.

VẤN ĐỀ: Năm hunk được kể đều tồn tại, nhưng phép kê vị trí không bao trùm mọi câu đã được finding lượt 4 chỉ ra. BN2/BN3 còn khẳng định “HEAD nay hai”, khi cùng digest tại SHA review có bốn tệp chứa. Đây là lời đính chính đang dùng làm bằng chứng, không phải chỉ trích nguyên văn verdict lịch sử. Bộ đếm đã sửa đúng số 52/105 nhưng được neo bằng “head hiện tại”, trái yêu cầu ghim commit vừa nêu. Việc đã sửa năm chỗ không chứng minh còn không chỗ nào cần sửa.

ĐÃ THỬ VÁ: không — bản chép được dùng để đo; đề nghị thay các mốc kết quả lịch sử bằng SHA cụ thể, giữ nguyên V1–V4 đã neo hash. Số 52/105 hiện tại đúng, không chấm thành sai số.

ĐÃ THỬ NGHIỆM: lấy `model_reviewer_identity.prompt_sha256` của BN1 bằng `yaml.safe_load`; gọi `git -C cay-kho grep -l <digest> <sha> -- .` trên `1d58500`, `4e6a2d5`, `25974e7`, `f6ec9c0` được **1/2/3/4**. `git -C cay-kho diff --numstat 1d58500 4e6a2d5 -- ops/cong_cu.py` rỗng; đổi đích thành `25974e7` được **+3/−2**, thành `f6ec9c0` được **+11/−4**. Diff `25974e7..f6ec9c0` chứng minh BN2:80 và BN3:120/125 chưa sửa. Validator tại bốn mốc cho chuỗi đúng đã ghi trong bảng.

ĐỘ TIN: cao

### attestation-runtime-bi-nang-thanh-phep-do  [P2]  Câu chứng thực đọc cây còn nguyên trong scalar YAML bị ngắt dòng

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml:77–80`; đối chiếu BN4:65–67 và README:273.

VẤN ĐỀ: BN1 còn suy “reviewer đọc đúng cây” từ so hai OID. Đây chính là vị trí lượt 4 đã chỉ ra. Diff lần sửa chỉ chạm khối prompt của BN1, không chạm `tree_khop`. Năm vị trí khác đã sửa; gọi chúng là 5/5 che mất vị trí thứ sáu. Phép tìm một chuỗi trên từng dòng bỏ sót scalar YAML gấp dòng; nó không đo việc mệnh đề còn tồn tại hay không.

ĐÃ THỬ VÁ: không — cần hạ chính scalar này xuống “OID khớp”, cùng mức chứng thực mà BN2/BN3/BN4 hiện đã ghi đúng.

ĐÃ THỬ NGHIỆM: đọc `yaml.safe_load(Path('cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml').read_text())['ba_lop_bang_chung_DUONG_reviewer_tu_dung']['tree_khop']` trả nguyên câu khẳng định đọc cây. Tìm chuỗi người giao nêu, phân biệt hoa thường trên byte văn bản: **0**; nối whitespace rồi tìm không phân biệt hoa thường trong các tệp Git theo dõi: **5 lần/5 tệp**, trong đó BN1 là mệnh đề chưa rút; C, BN2, V3 là trích dẫn/đính chính và BN4 tự nhắc chuỗi. Không đòi xóa các trích dẫn ấy. `git rev-parse e826730^{tree}` khớp OID chỉ xác nhận chính OID.

ĐỘ TIN: cao

### hai-loi-khai-thieu-nhan-va-sai-co-trang  [P2]  Bảng CHANGELOG đã tách nguồn nhưng biên nhận lượt 3 vẫn cộng connector vào số đo

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-3-codex-verdict.receipt.yaml:149–155`; `cay-kho/ops/reviews/README.md:274`; `cay-kho/CHANGELOG.md:103–107`.

VẤN ĐỀ: BN3 vẫn đặt bốn lượt trong `do_duoc`, liệt kê connector cộng V1/V2/V3. Chỉ ba tệp thuộc danh sách đó có tiêu đề để đếm; không có response connector. Câu “cộng dòng ĐỐI CHIẾU” còn có thể đếm hai lần một lượt. README lượt 3 vẫn kể bốn lượt mà không tách nguồn cho lượt thứ tư. C:416–428 đã sửa đúng, nhưng không sửa các bản chép này. Nhãn mới ở C:107 giới hạn “DƯỚI ĐÂY”, bỏ sót câu JSON của lượt Windows ở ngay trên. Chú thích mã đã sửa thật, không chấm lại phần đó.

ĐÃ THỬ VÁ: không — cần áp cùng phép tách nguồn của bảng C vào BN3/README; đặt nhãn CI trước toàn bộ đoạn sự kiện hoặc ghi rõ nó bao gồm cả câu phía trên.

ĐÃ THỬ NGHIỆM: `git -C cay-kho diff 25974e7 f6ec9c0 -- ops/reviews/pr497-review-3-codex-verdict.receipt.yaml` không có hunk sửa khối `NGUONG_HINH_DANG_LOI_DA_DAT`. Đếm `^### hai-loi-khai-thieu-nhan-va-sai-co-trang` được một trong mỗi V1–V4; riêng danh sách ba file của BN3 được **3**, không phải 4. A/B CLI tái hiện cơ chế CI như bảng đo, nhưng sự kiện Windows/connector **KHÔNG ĐO ĐƯỢC** vì thiếu log/response.

ĐỘ TIN: cao

### bang-tu-dinh-chinh-khong-tai-lap-duoc-quy-tac-duong-dan  [P2]  Bảng mới đếm thiếu dù đã nêu quy tắc trước kết quả

TỆP/DÒNG: `cay-kho/CHANGELOG.md:469–489`; BN4:7–12; README:273; `commit-messages.txt:19–29`.

VẤN ĐỀ: Có nêu quy tắc trước, nhưng các số 5/7 và 4/6 không sinh từ quy tắc được viết. Quy tắc hỏi toàn tập đường dẫn của trường TỆP/DÒNG có chứa hiện vật review không, không quy định loại các đường dẫn được dùng để “đối chiếu”. V2 finding đầu cũng chứa đường dẫn V1, nên tính theo quy tắc ấy ra 6/7. Với V3, phải giải nghĩa các tên viết tắt “receipt lượt n”; **năm finding trực tiếp chỉ tới receipt**: hai-loi-khai, attestation, ke-sai-ly-do, phep-grep, dem-finding. Chỉ riêng năm này đã bác 4/6. Finding bộ đếm còn dẫn EVIDENCE, nên lấy toàn trường sẽ ra 6/6. Regex chỉ nhìn đường dẫn viết đầy đủ lại bỏ sót alias, không phải phép đếm tập đường dẫn đã hứa.

Lời kết đã rút đúng câu “nội dung gốc sạch”. Tuy nhiên đếm sự có mặt của đường dẫn, gồm cả nguồn đối chiếu, không tương đương đếm “finding nhắm vào hiện vật” hay chứng minh mọi khối văn xuôi đều tự sinh lỗi. Cần nêu rõ đích finding hay mọi dẫn chiếu và liệt kê các slug được tính; không dùng phép đếm này để chứng minh lớp rủi ro đã biến mất.

ĐÃ THỬ VÁ: không — chưa tự chọn thay tiêu chí của tác giả. Hai lựa chọn đều có thể viết rõ, nhưng không giữ số không suy được từ tiêu chí đã công bố.

ĐÃ THỬ NGHIỆM: script sau đã chạy; kết quả **0/2, 6/7, 6/6, 5/5**. Giải nghĩa alias chỉ áp các tên receipt lượt 1–3 thực sự có trong TỆP/DÒNG của bốn verdict; không đọc toàn phần văn xuôi finding để tăng số.

```python
from pathlib import Path
import re
for n in range(1, 5):
    text = Path(f'cay-kho/ops/reviews/pr497-review-{n}-codex-verdict.md').read_text()
    blocks = re.split(r'(?=^### .*\[P[123]\])', text, flags=re.M)[1:]
    selected = []
    for block in blocks:
        location = re.search(r'(?m)^TỆP/DÒNG:.*$', block).group()
        if re.search(r'ops/reviews/pr497-|EVIDENCE\.md|receipt lượt [123]', location):
            selected.append(block.splitlines()[0].split()[1])
    print(n, len(selected), len(blocks), selected)
```

ĐỘ TIN: cao

### bien-nhan-luot-bon-tu-cap-hang-do-cho-cac-truong-ngoai-runtime  [P2]  Quy tắc nguồn mới mâu thuẫn với dữ liệu ngay trong biên nhận ngắn

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-4-codex-verdict.receipt.yaml:18–19`, `:126–136`, `:144–149`; C:496–498; README:273.

VẤN ĐỀ: Sau khi gán `model_reviewer_identity` là ATTESTATION, tệp viết **“Mọi trường khác đo lại được từ kho, không cần mạng.”** Nhưng `tuan_thu_cam_cua_reviewer` nằm ngoài khối đó: sạch/0 commit thêm là tự khai về phiên cũ, và chính :129 ghi ATTESTATION. `github_submitter_identity.actor`, `la_tac_gia_PR`, phiên vận chuyển cũng không được xác thực chỉ bằng YAML. `khong_do_duoc` lại liệt kê dữ liệu ngoài kho. Có thể đọc lại giá trị được khai không đồng nghĩa đo lại sự kiện mà giá trị mô tả. Đây là lỗi mới cùng kiểu tự tạo ngoại lệ chứng thực của các biên nhận trước.

ĐÃ THỬ VÁ: không — cần thay câu bao trùm bằng danh sách hẹp các trường đo tại chỗ: byte/hash/path, OID, quan hệ tổ tiên, số tiêu đề. Các trường tự khai và GitHub phải giữ hạng riêng dù nằm ngoài khối runtime.

ĐÃ THỬ NGHIỆM: parse BN4 bằng `yaml.safe_load` xác nhận `tuan_thu_cam_cua_reviewer` và `github_submitter_identity` là khóa ngang hàng với `model_reviewer_identity`; scalar :129 chứa ATTESTATION. `python3 ops/bien_nhan_v2.py --root .` vẫn **rc=0, 52/105**, chỉ chứng minh validator chấp nhận cấu trúc/neo. Xác thực lần chạy và actor GitHub **KHÔNG ĐO ĐƯỢC** vì không có run.json/response tương ứng.

ĐỘ TIN: cao

### bien-nhan-ngan-chua-thuc-hien-ban-va-cau-truc-da-khai  [P2]  Số dòng sai và văn xuôi vẫn tồn tại dưới lời tuyên bố đã loại cả lớp rủi ro

TỆP/DÒNG: `cay-kho/CHANGELOG.md:496–504`; BN4:5–16,53–101; README:273; `commit-messages.txt:11–17`.

VẤN ĐỀ: Đo ở trạng thái giao cuối cùng là 149 dòng, không phải 146; giảm 104, không phải 107. Năm finding không phải năm dòng: chúng chiếm khối 53–95, có `van_de`, `phep_do`, `da_va` và nhiều scalar nhiều dòng. Phần dẫn nhập và `goi_luot_4_SACH` vẫn giải thích bài học và tuyên bố đóng lớp lỗi. “Cả lớp rủi ro chết theo kiến trúc” vì vậy không được hỗ trợ bởi cấu trúc thực tế; BN4 đã chứa các lời khai sai mới được chỉ ra ngay trong lượt này. Hai gói cũ được reviewer báo sạch cũng không chứng minh mọi lời khai về gói tương lai đã được bảo vệ.

ĐÃ THỬ VÁ: không — có thể mô tả trung thực mức rút gọn hiện có, hoặc thực hiện đúng cấu trúc được hứa. Không cần phục hồi các khối bị cắt; không phát hiện mất trường bắt buộc của receipt.

ĐÃ THỬ NGHIỆM: `wc -l cay-kho/ops/reviews/pr497-review-{3,4}-codex-verdict.receipt.yaml` ⇒ **253 và 149**; `253-149=104`; numstat.txt cũng ghi **149**. `yaml.safe_load(BN4)['nam_finding']` có **5 object**, không phải năm scalar một dòng; không có khối kết quả cổng độc lập như danh sách C:497 có thể khiến người đọc kỳ vọng. Băm verdict và validator vẫn đạt; chúng không kiểm lời tuyên bố đã loại văn xuôi.

ĐỘ TIN: cao

### tong-ket-pham-vi-van-dung-o-ba-luot-va-nam-hang  [P2]  Tổng kết §3 chưa tính lượt 4 đã có trong chính bảng bên dưới

TỆP/DÒNG: `cay-kho/CHANGELOG.md:156–161`, `:178`.

VẤN ĐỀ: Tiêu đề còn “BA lượt”, mở đầu còn “ba lượt này”, hàng vai trò README còn “3 hàng mục lục + 2 hàng cảnh báo”. Cùng mục đã liệt kê V4/BN4 và có phần LƯỢT 4. README thực có sáu hàng PR497: bốn mục lục và hai cảnh báo. Đây là số phạm vi hiện hành, không được đóng khung như snapshot lịch sử.

ĐÃ THỬ VÁ: không — cần cập nhật ba chỗ tổng kết thành bốn lượt, bốn hàng mục lục cộng hai cảnh báo; không thêm cảnh báo giả cho lượt 3/4.

ĐÃ THỬ NGHIỆM: chọn các dòng README bắt đầu bằng `|` và có tên verdict `pr497-review-[1-4]-codex-verdict.md` ở cột đầu ⇒ **6 dòng**, vị trí **17,18,273,274,275,276**; bốn dòng có liên kết verdict/receipt là mục lục. `git diff --numstat 0721811 f6ec9c0 -- ops/reviews/README.md` ⇒ **+6/−0**.

ĐỘ TIN: cao

### t27-duoc-gan-ca-trach-nhiem-kiem-tep-cua-t26  [P2]  Bỏ verdict ở cả bốn lượt vẫn qua riêng t27

TỆP/DÒNG: `commit-messages.txt:2` (nội dung commit `f6ec9c0`, lặp ở các commit đóng hồ sơ trước); C:178 về cổng đòi đủ; đối chiếu `cay-kho/ops/lease_publish_test.py:1032–1070` và `:959–963`.

VẤN ĐỀ: Lời “t27 đòi đủ ba mảnh cho MỖI verdict” gán phạm vi của hai ca cho một ca. t27 duyệt verdict có trên đĩa để đòi receipt, rồi duyệt receipt để kiểm tên trong bảng; lượt duyệt sau không đòi tệp verdict tồn tại. Vì vậy bỏ riêng tệp verdict vẫn qua t27. t26 kiểm `f.is_file()` và chặn đúng. Đây là sai lời khai về chốt, **không phải** bằng chứng toàn suite cho lọt verdict mất; không nâng thành P1 hoặc yêu cầu thêm ca trùng t26. Commit đã ghi thì đính chính bằng hồ sơ mới, không sửa lịch sử hay tệp gói được giao.

ĐÃ THỬ VÁ: không — cần gọi đúng tổ hợp **t26 + t27** bảo vệ ba mảnh; t27 riêng bảo vệ quan hệ receipt/mục lục/caveat trong các ca đã đo.

ĐÃ THỬ NGHIỆM: trên bản chép, trước mỗi ca chạy t27 nền rc=0; lần lượt bỏ Vn, BNn, MLn và phục hồi. Kết quả **4/4 thiếu verdict vẫn rc=0; 4/4 thiếu receipt rc=1; 4/4 thiếu ML rc=1**. Gọi t26 trên bốn cây mất verdict đều rc=1, thông báo đúng đường dẫn mất. Bỏ hai hàng caveat riêng lẻ cũng bị t27 chặn. Lệnh gọi đúng các ca:

```sh
python3 -c "import sys; sys.path.insert(0, 'ops'); import lease_publish_test as t; t.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()"
python3 -c "import sys; sys.path.insert(0, 'ops'); import lease_publish_test as t; t.t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()"
```

Hai lệnh trên chạy **từ gốc bản chép**, không từ cay-kho. Chỉ bỏ dòng mục lục của lượt đang thử; giữ nguyên hàng cảnh báo để phân biệt hai loại chốt. Kết quả phục hồi cuối: cả t26 và t27 đạt.

ĐỘ TIN: cao

## GIỚI HẠN

- Không mạng: không xác thực PR/Issue/check/review/actor/authority/landed trên GitHub, không gọi GitHub và không lấy origin mirror làm máy chủ thật. evidence_url chỉ được kiểm commit/path/blob/ancestry cục bộ.
- Không có log Actions hoặc run.json/prompt/stdout/stderr của bốn phiên cũ. Băm verdict, số học timestamp, OID trùng và việc runtime scalar được chép nhất quán không xác thực model, hành vi đọc hay việc phiên cũ đã chạy những lệnh nào. “Điều phối tự bắt” và thứ tự nội bộ “liệt kê trước, sửa sau” cũng không thể chứng thực từ lời commit; đã kiểm sản phẩm cuối và lịch sử diff.
- Đã chạy 12 cổng EVIDENCE và các phép thử ghi trên, cùng suite lease trước merge và validator tại bốn SHA. Không chạy toàn bộ CI, Windows, LIVE, publish, merge hoặc deploy. Lượt gọi release-verify ban đầu dùng nhầm cờ `--manifest` trả rc=2 lỗi cú pháp; đã xem help và chạy lại đúng đối số vị trí, kết quả 180/180 trong bảng. Một phép chọn chuỗi đột biến bắt đầu gặp hai bản sao trong toàn CHANGELOG; đã thu hẹp vào r362 trước khi chạy bốn ca còn lại. Hai lỗi giàn đo này không được tính là lỗi PR hay phép thử đạt.
- Chỉ dùng fixture/suite sẵn có và đổi số, nhãn, điều kiện canary, sự có mặt của hiện vật. Không tự soạn nội dung tấn công. Các hướng cần chuỗi thoát, đồng tự hoặc đường dẫn vượt cây không được thử.
- Phiên này dùng công cụ thực thi cục bộ của Codex/OpenAI; không suy danh tính model của các phiên cũ từ nhãn model yêu cầu. Không áp quy định bề mặt phiên cũ thay cho khả năng công cụ đang có trong phiên này.
- Cây gốc được giữ nguyên. Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**; HEAD vẫn **f6ec9c0650de2716776e8b58a63b3141095097fa**. Các bản chép, log và script tạm đã dọn; chỉ để lại tệp kết quả `VERDICT.md` ở gốc sandbox.
