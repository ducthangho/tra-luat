verdict: changes_requested
reviewed_sha: 25974e78ac4dbeb67db5f797b08b4dd276d0d666

Review lượt 4 bằng OpenAI/Codex, qua API và công cụ shell trong sandbox được giao. Tree tự đo: `1d303009eaef2471c4c51a449f46abef1d4bc58b`. Kết quả **0 P1 / 5 P2 / 0 P3**. Đủ 12 lệnh EVIDENCE đạt; các finding là lời khai sai hoặc vượt phạm vi bằng chứng.

**Ba nếp chưa được áp đầy đủ cho chính lượt 3.** Đã sửa thật nhãn #498, hai câu kể ngược nhân quả và hai ngoại lệ runtime. Tuy nhiên, hàng mục lục lượt 2, phép grep ở biên nhận lượt 1 và lời suy từ tree sang hành vi đọc vẫn còn nguyên. Bằng chứng mới tiếp tục dùng `HEAD`; bảng cổng CHANGELOG đã cập nhật đúng, nhưng biên nhận mới lại khai số trước khi thêm chính nó. Một đường dẫn có diff không chứng minh mọi mệnh đề được hứa sửa trong đường dẫn ấy đều đã sửa.

## ĐỐI CHIẾU LƯỢT 3

- `hai-loi-khai-thieu-nhan-va-sai-co-trang`: **VÁ HỜ** — `git -C cay-kho diff 4e6a2d5 25974e7 -- ops/cong_cu.py` có hunk thêm nhãn THUẬT LẠI cho #498 tại dòng 223–224. Nhưng đoạn Windows tại CHANGELOG:103–111 và sự kiện `rg` đỏ/G5 skip tại cong_cu.py:218 không đổi, vẫn thiếu nhãn CI tại chỗ. §4 mới còn đưa lượt connector “1 trong 3 P2” vào phép đếm được gọi là ĐO ĐƯỢC, dù chỉ có ba verdict trong kho. Giá trị/sự kiện GitHub không tái đo được ở đây.
- `attestation-runtime-bi-nang-thanh-phep-do`: **VÁ HỜ** — diff hai receipt cũ xác nhận “NỢ ĐÃ ĐO” và “Lý do ĐO ĐƯỢC” đã thành lời cũ bị rút; cả ba khối runtime không còn cấp ngoại lệ xác thực phiên cho các scalar ấy. Nhưng câu “reviewer đọc đúng cây” ở hai receipt cũ, CHANGELOG và hai hàng README không đổi; receipt lượt 3:43–46 còn chép thêm cùng suy luận. `rev-parse` xác nhận cả ba OID, không xác nhận hành vi đọc của phiên. Thử riêng `launcher.chot_kho(...)` trả `Chan.ma=11`, xác nhận cơ chế hôm nay; không xác thực cờ phiên cũ.
- `ke-sai-ly-do-reviewer-khong-chay-ls-remote`: **ĐÃ VÁ THẬT** — nguồn là verdict lượt 1:157. Hai chỗ từng sót đã có hunk sửa: README:18 và receipt lượt 1:198–209. Đối chiếu thêm CHANGELOG:203–211, receipt lượt 2:104–113 và README:274: đủ **5/5 nơi** hiện kể reviewer đo cấu hình thật rồi bỏ lệnh; câu “tin/đọc câu sai” chỉ còn trong trích dẫn được rút. EVIDENCE hiện tại không kể lại nguyên nhân sai; receipt lượt 3:64–70 phân biệt lời cũ với bản vá đúng. `t27` cây nguyên vẹn rc=0; bỏ hàng cảnh báo lượt 1 rc=1.
- `bang-cong-r362-con-neo-so-truoc-bien-nhan-luot-hai`: **VÁ SINH LỖI MỚI** — CHANGELOG:301–308 đã sửa thật thành `51/tổng 104`, đúng validator trên SHA đang review. Nhưng receipt lượt 3:98 mới viết “Đổi thành 50 · 103, đo lại trên exact HEAD sau bước cuối”. Tái chạy validator ở `4d2a6f6`, `4e6a2d5`, `25974e7` lần lượt ra **49/102, 50/103, 51/104**, đều rc=0. Sai số đã chuyển sang biên nhận mới.
- `phep-grep-prompt-khong-ghim-snapshot-sau-khi-nhap-verdict`: **VÁ SINH LỖI MỚI** — receipt lượt 2:73 đã ghim `1d58500`, nhưng receipt lượt 1:146–147 giữ nguyên lệnh `HEAD` và kết quả một tệp. Truy vấn cùng digest trên `1d58500`, `4e6a2d5`, `25974e7` trả **1, 2, 3 tệp**. Biên nhận mới tiếp tục kể `HEAD ⇒ 2`, và phép `git diff 1d58500 HEAD -- ops/cong_cu.py ⇒ rỗng` mới chép vào §3/§4/README/receipt nay trả hunk **3 thêm/2 bớt**. Không sửa các verdict lịch sử đã neo băm; cần ghim SHA trong phần tóm tắt/đính chính mới.
- `dem-finding-doi-mau-va-bo-sot-phan-moi`: **VÁ HỜ** — tự đếm ba verdict được **0/1/1, 0/7/0, 0/6/0**, tổng **2, 7, 6**. CHANGELOG:255–261 và receipt lượt 2:151–174 sửa đúng P2 `1→7`, tổng `2→7`, tập mới `6/7`. Nhưng hàng README lượt 2:274 vẫn nguyên byte so với `4e6a2d5`, còn “Số finding tăng 1→7” và `5/7`, trái receipt lượt 3:125 khai đã sửa. `git log -S 'Không cổng nào' 25974e7 -- CHANGELOG.md` và đọc blob lịch sử xác nhận trường hợp thứ sáu được thêm tại `52b36d1`, sau head lượt 1.

## BẢNG ĐO

Quy ước: các SHA ngắn dưới đây đã phân giải duy nhất trong clone đầy đủ; snapshot hiện tại luôn là `25974e78ac4dbeb67db5f797b08b4dd276d0d666`. `BN1/BN2/BN3` lần lượt là `ops/reviews/pr497-review-{1,2,3}-codex-verdict.receipt.yaml`; `V1/V2/V3` là tệp `.md` cùng tên. `C` là phần r362, dòng 1–418 của CHANGELOG; `ML1/ML2/ML3` là README dòng 275/274/273. “Khớp” về phép tính/byte không xác thực nguồn GitHub hoặc hành vi phiên cũ.

Mọi cổng chạy trên bản chép đầy đủ, giữ nguyên exact SHA, trong sandbox. Cây gốc được đọc để so byte/Git; bản chép lịch sử và bản chép đột biến riêng biệt. `TMPDIR`, `TEMP`, `TMP`, cấu hình Git global và cache đều ở sandbox; đặt `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_NOSYSTEM=1`. Không cài công cụ hoặc gọi mạng.

**Kiểm từng lời khai vá, không chỉ kiểm tệp có diff.** Đã chạy cả lệnh người giao yêu cầu `git -C cay-kho diff 4e6a2d5 HEAD -- <đường-dẫn>` khi HEAD được xác nhận là SHA trên, và phép tương ứng ghim `25974e7`. Năm đường dẫn thực tế thay đổi: CHANGELOG **+100/−11**; cong_cu.py **+3/−2**; README **+2/−1**; BN1 **+12/−4**; BN2 **+40/−11**. Đã đọc từng hunk, không lấy năm diff khác rỗng làm bằng chứng “vá đủ 5/5”.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| BN3:3; C:154,273 — hoàn tất bản vá | mọi finding/cả sáu đã vá | Đối chiếu sáu slug bên trên: 1 đóng trọn; 3 vá hờ; 2 có lỗi mới trong lời ghi sổ | **Không** |
| BN3:59–61 — cong_cu.py | nhãn #498 nay có thật | Hunk +3/−2 tại đoạn 223–224 thêm THUẬT LẠI và giới hạn nguồn | Có |
| BN3:70 — README:18, BN1 | hai nơi nay trích dòng 157, giữ câu cũ như đính chính | Cả hai hunk đúng mệnh đề; bảng năm vị trí ở ĐỐI CHIẾU khớp nguồn | Có |
| BN3:75–76 — áp ngay nếp 1 | kiểm đủ 5/5 đường dẫn; chuỗi cũ chỉ là trích dẫn | Có 5 tệp đổi, nhưng BN1 vẫn dùng grep HEAD; ML2 còn số sai và câu chứng thực đọc cây chưa được rút | **Không chứng minh đủ các lời hứa vá** |
| BN3:90 — hai chỗ runtime | hạ xuống THUẬT LẠI | BN1:132–138 và BN2:197–213 đổi đúng; không nhầm trích lời cũ với ngoại lệ mới | Có ở hai chỗ này |
| C:184–186; BN1/BN2; lời “cả sáu” | giới hạn phép khớp tree đã được xử lý | Các câu chứng thực “đọc đúng cây” không có hunk sửa; BN3 còn thêm một bản lặp | **Không** |
| BN3:98 — bảng cổng | đổi 50/103, đo sau bước cuối | C:308 thực tế đổi 49/102 thành 51/104; validator hiện tại 51/104 | **Không** |
| BN3:111 — phép grep | ghim 1d58500; HEAD nay 2 tệp | BN2 có ghim; BN1 không có hunk sửa phép grep; hiện tại 3 tệp | **Không trọn** |
| BN3:125 — cách gọi số và tập mới | P2 1→7, tổng 2→7, 6/7 | C và BN2 đúng; nội dung ML2 không đổi, giữ tổng 1→7 và 5/7 | **Không trọn** |
| C:231 — lời đóng lượt 2 | cả bảy đã vá | Nhãn ref, quy tắc 28, pin 2/3, giới hạn hai cổng và nguyên nhân đã sửa; các phần nguồn/định danh còn finding | **Không thể đọc như đóng trọn hiện tại** |
| C:178–182 — vá của lượt 1 | hai slug đạt, một slug vá hờ; sửa ba dẫn chiếu | V1 có đúng ba dòng đối chiếu; dẫn chiếu hiện tại là số dòng, đúng nguồn | Có về nội dung hồ sơ |
| C:205–206,269; BN1/BN2 | đã nâng hai cảnh báo lên README | Đúng hai hàng 17/18, đúng ID và verdict; đột biến bỏ từng hàng đều làm t27 đỏ | Có |
| C:295–299; BN3:160–166 | gói lượt 3 sạch, sinh bằng script ở bước cuối, không câu gõ tay | V3:283 có lời xác nhận 9 dòng cấu hình; không có gói/script/log tạo gói lượt 3 ở đây để xác thực thao tác và thứ tự lịch sử | Đo được lời reviewer ghi; quy trình cũ **KHÔNG ĐO ĐƯỢC** |
| C §4:402–410; BN3:145–154 | ba nếp đã đổi | Có đúng ba mục kỷ luật; số đo bên trên bác việc đã áp trọn nếp 1/2, bảng C áp đúng nếp 3 nhưng BN3 sai | Một phần |

**Phân biệt lệnh chưa ghim với hiện vật lịch sử.** Các phép `rev-parse <SHA>^{tree}` đã ghim đúng. Các phép cho kết quả cụ thể còn dùng HEAD được liệt kê ở bảng/finding: grep BN1; các câu “HEAD nay hai” BN2/BN3/C/ML3; diff mã C §3/§4, BN3 và ML3. `git log -S` trong C:260, BN2:166, BN3:122 còn mặc định duyệt từ HEAD, dù sự kiện thêm ở 52b36d1 được kể vẫn đúng. Các phép tìm commit đầu dùng `log --all --diff-filter=A` ở cả ba receipt duyệt tập ref hiện có, chưa ghim tập ref; kết quả hiện tại đúng 1 commit mỗi path. Những lệnh HEAD trong V1/V2/V3 nguyên văn được đọc theo `reviewed_sha` của từng verdict, không phải lý do biên tập lại hiện vật đã neo hash. Mẫu hướng dẫn `git diff <head cũ> HEAD` ở nếp 1 là hướng dẫn, không phải một kết quả đã đo.

**Gói, ref, Git và manifest.** Lệnh chính: `git rev-parse`, `for-each-ref`, `show`, `merge-base --is-ancestor`, `diff --numstat`, `rev-list --count`; Python đọc byte bằng `hashlib.sha256`. Quét r dùng tiêu đề cấp 1 của CHANGELOG từng ref, không đếm lần nhắc trong prose. Chỉ gọi `ls-remote --heads origin` sau khi xác minh origin là mirror trong sandbox.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Gói — head/tree | 25974e7; 1d303009… | Đúng hai OID đầy đủ ở đầu verdict; HEAD detached | Có |
| Clone và abbrev | full; false; 7 | `--is-shallow-repository=false`; core.abbrev=7 | Có |
| Origin | đường dẫn kho.git trong sandbox | `remote get-url origin` đúng nguyên văn do-goi; ls-remote rc=0 trả 324 dòng của mirror | Có; không phải GitHub |
| Chín trường cấu hình | EVIDENCE = do-goi | So lại toàn bộ 9 dòng với cấu hình thật; bao gồm trạng thái sạch | Có; xem phép đo cuối |
| Mirror | 324 = 323 + 1 giao hàng | 324 heads; đúng 1 ref pr497-head; loại rõ ref này còn 323 | Có |
| Bộ đệm của clone | phân biệt với máy chủ | 325 remote-tracking refs gồm alias HEAD; bỏ alias còn 324, khớp tên/OID mirror | Có về hai tập cục bộ |
| Raw máy chủ được giao | 322 dòng, ec6ef20af4eb7f73… | 322 dòng, 25.944 byte; SHA-256 `ec6ef20af4eb7f734fcb0e321c86b93d0efbb34493630e968fcfb138b51b5ec8` | Có về byte |
| Nguồn/giờ raw | GitHub; 2026-09-10T08:51:05Z | **KHÔNG ĐO ĐƯỢC**: chỉ có tệp, không có chứng cứ độc lập nguồn/thời điểm | ATTESTATION, không xem băm là chứng thực GitHub |
| Raw so 323 ref đã loại giao hàng | canh tập tên | Thiếu 0; thừa đúng pr487-merge: 1; 322 OID chung khớp | Có số học; việc xóa nhánh trên GitHub không đo được |
| Ref r360 | nhánh khác đã mang r360 | Đúng 1: claude/pr491-land-va-findings-wip; trạng thái PR/phiên “chưa merge” trên GitHub **KHÔNG ĐO ĐƯỢC** | Có phần object/ref |
| Quét r362 | 1 trên tập 323; 2 trên tập 324 | Đúng claude/handoff-tra-luat-repo-2ak5th và pr497-head; loại giao hàng còn 1 | Có |
| Quét r363 | 1 ở land-492-bookkeeping | Đúng 1 ref; tiêu đề đầu r363 | Có |
| Nhánh từng mù lần 1 | wp484-g3-windows mang r356 | Ref hiện có; đầu CHANGELOG r356; việc từng mù **KHÔNG ĐO ĐƯỢC** | Một phần |
| Lịch sử canh lần 1 | 320/320; mù 1; sau fetch 0; quét 320 | **KHÔNG ĐO ĐƯỢC** snapshot máy chủ/bộ đệm trước fetch; không lấy 324 hiện tại bác số lịch sử | Đã gắn THUẬT LẠI |
| Lịch sử canh lần 2 | 322/321; mù 2; thừa 1; sau fetch 0 | Hai tên được kể và pr487-merge có trong ref hiện tại; tập đệm 321 cũ/thao tác fetch **KHÔNG ĐO ĐƯỢC** | Đã gắn THUẬT LẠI |
| Số học lịch sử canh | lệch tổng 1 nhưng mù 2 | 322−321=1; 2−1=1 | Có về phép tính |
| Ngày r362; nội dung | 2026-09-10; hai việc; bốn tiểu mục hiện tại | Commit đầu 25c2d5b: 2026-09-10T03:43:16Z; có §1–§4, §1/§2 là hai việc | Có về Git/văn bản |
| VERSION | 1.36.68 từ r336; không nâng | VERSION tại 3dcdc6a và snapshot này đều 1.36.68; diff VERSION rỗng | Có |
| Phạm vi EVIDENCE | 10 tệp, +1887/−5, 10 commit | Tự cộng numstat và rev-list đúng; diff.patch, numstat.txt khớp Git từng byte | Có |
| Chi tiết 10 tệp | như numstat.txt | C +420; manifest +5/−5; cong_cu +17; README +5; V1/BN1 +161/+216; V2/BN2 +259/+280; V3/BN3 +285/+239 | Có |
| Master đã hợp nhất | 0721811, từ 28ba133 | `merge-base --is-ancestor 0721811 25974e7` rc=0; merge 1e75335 có cha 52b36d1 và 0721811 | Có trong Git |
| Giao write set | master đổi 3 tệp; giao 0 | Diff 28ba133→0721811 đúng workflow thu hồi + lease_publish.py + lease_publish_test.py; giao với nhánh trước merge rỗng | Có; không chứng thực lời “merge sạch” bằng log cũ |
| Hành vi cong_cu.py | chỉ chú thích | AST tại 0721811 và 25974e7 bằng nhau | Có |
| Manifest | 180→180; đúng 1/10 tệp đổi thuộc kiểm kê; 0 ops | Hai manifest cùng 180; giao với diff đúng CHANGELOG; manifest không kiểm kê chính nó hay ops | Có |
| Toàn vẹn manifest | mọi byte khớp | Tự đọc đủ 180 tệp: 0 lệch size/hash; tổng 8.146.762 byte đúng total_bytes; verify strict đạt | Có |
| package_hash | giá trị trong manifest | Verify khớp `226091f23475b33fe19a0e99c9ad94564cdaea8fa3a10b3cc98adaeb17eeaf85` | Có |

**Các số §1/§2 và nguồn GitHub.** Đã parse `jobs.gate.steps` ở `8cee941`, `7693852`, `28ba133`, `25974e7`: cùng blob `2e21c0c1f0701e837f7c13fa20a55ab39fd5805c`. Đây là đo mã workflow, không phải đo kết quả Actions.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| ADR-0034 | ba vế merged/hậu-merge gate/bookkeeping | Nội dung ADR/CONTEXT phù hợp ba vế | Có về quy tắc |
| Merge #490 | 8cee941, hai cha 00e017a + 01e7f77 | `show -s --format='%H %P'`: `8cee9410e958a6b9d956e080c11878fbd80d9f5f`, `00e017af102bc8355e0c276d2d813e20620ddb42`, `01e7f77d707cb093b5ba6d9b9d8577f40d025488` | Có trong Git |
| r359 và 0 hiện vật CI | chưa đủ bằng chứng trong cây | `git grep -l 8cee941 71e0053 -- .` chỉ trả CHANGELOG; snapshot mới thêm hồ sơ review, không có response CI thô neo merge trong kết quả tìm | Có trong phạm vi tìm kiếm, không suy CI chưa chạy |
| Job Ubuntu | 37 success + 4 skipped + 0 failure = 41 | Cộng ra 41; trạng thái/đếm runtime **KHÔNG ĐO ĐƯỢC**, thiếu response job | Số học đúng, đã thuật lại |
| Job Windows | 35 success + 6 skipped + 0 failure = 41 | Cộng ra 41; runtime **KHÔNG ĐO ĐƯỢC** | Như trên |
| Khoảng giờ Ubuntu | 18:50:37→19:11:32 | Hiệu 1.255 s = 20m55s; hai mốc thực **KHÔNG ĐO ĐƯỢC** | Chỉ khớp số học |
| Khoảng giờ Windows | 18:50:37→19:44:09 | Hiệu 3.212 s = 53m32s; hai mốc thực **KHÔNG ĐO ĐƯỢC** | Chỉ khớp số học |
| Run #490 | 34391481045; push/master; 8cee941; attempt 1; không rerun | **KHÔNG ĐO ĐƯỢC**: không mạng/response Actions | Không chứng nhận run |
| Hai run so sánh | 7693852 attempt 2; 28ba133 attempt 1 | Commit có thật, workflow cùng blob; attempt/kết quả **KHÔNG ĐO ĐƯỢC** | Một phần |
| Ba run cùng skip 4/6 | khớp từng bước, hình dạng LAND | YAML push/master cho tập skip Ubuntu 11,23,28,39; Windows 11,21,22,28,36,39 khi cộng bước setup job | Phù hợp thiết kế; quan sát 3 run **KHÔNG ĐO ĐƯỢC** |
| #11, #22/#23, #38/#39 | PR-only; Linux/không Linux; LAND/WORKER | Điều kiện YAML đúng; YAML có 40 mục, không phải 41; 41 runtime không đo được | Có về mã |
| #490 landed/0 failure/không có tệp land riêng | đủ ba vế; chủ kho đóng chuỗi | Merge và bookkeeping đọc được; CI, quyết định/thẩm quyền, trạng thái landed **KHÔNG ĐO ĐƯỢC** | Không tự chứng nhận landed |
| Nợ treo | khoảng vài giờ; rút ~7 giờ | **KHÔNG ĐO ĐƯỢC**: không có thời điểm đọc CI/đóng nợ; giờ commit không thay mốc ấy | Giới hạn đã khai |
| r361 bị rút | nếu chỉ shellcheck hỏng thì không ai biết | Câu có trong r361; thử A/B dưới đây bác nó | Có |
| A/B có shellcheck | actionlint DAT; shellcheck DAT; canary DAT, SC1003 rc=1 | CLI rc=0; tất cả đúng; tổng DAT | Có |
| A/B thiếu shellcheck | actionlint DAT; shellcheck KHONG_DO_DUOC; canary DO/blocking | CLI rc=2, tổng DO; SUY_GIAM, fixture rc=0; các công cụ bắt buộc khác vẫn DAT | Có |
| Quét một công cụ | canary=[]; tổng DAT dù shellcheck thiếu | `kiem-tra --chi shellcheck --json` rc=0, tổng DAT, 0 canary, shellcheck KHONG_DO_DUOC | Có |
| Hai lần cong_cu.py | đủ bác lời r361 | Hai full scan A/B đủ tái hiện DAT→DO; số lần tác giả chạy trong phiên cũ **KHÔNG ĐO ĐƯỢC** | Có về cơ chế |
| Chỉ full scan chạy canary | if chi is None; blocking nâng tổng trừ advisory | Thử tắt vòng canary, tắt nâng tổng, đổi advisory cho đúng các kết quả dưới đây | Có |
| Hai bước cài riêng và G5 | #7 shellcheck, #8 rg; #9 full scan không --chi | YAML vị trí 6/7/8, cộng setup job phù hợp số kể; installer dùng --chi; rg bắt buộc, shellcheck không | Có về mã |
| Lượt Windows đỏ | #7 xanh, #8 rg đỏ, #9 skip | Mã cho phép; log/JSON thực **KHÔNG ĐO ĐƯỢC** | **Thiếu nhãn tại C:103–111 và cong_cu.py:218** |
| “tệp này đã ghi ba lần” | 3 lần đọc rỗng thành phủ định | **KHÔNG ĐO ĐƯỢC** số phân loại: không chỉ ba đoạn/quy tắc đếm | Không nhận lời kể làm số đã kiểm |
| Xuất xứ #290 | spec đóng băng; kế nhiệm/corrective cần authority | Cảnh báo trong spec; Git có merge 59fe955 và quan hệ tổ tiên; trạng thái landed/quyền GitHub **KHÔNG ĐO ĐƯỢC** | Có phần văn bản/Git |
| Ba dẫn protocol | dòng 28/116/164; AGENTS:22–23 | Ba câu đúng ở ba dòng; protocol có 20 mục đánh số; không có §28/116/164 | Có |
| Ba P2 connector; P2 ×2 đoạn nhận việc | 3 tổng, 2 phần cuối | V1 liệt kê 3 slug; hai nhóm cuối có trong diff; review GitHub gốc **KHÔNG ĐO ĐƯỢC** | Có cấu trúc, thiếu nguồn cho phép đếm GitHub |
| Trang Issue cũ | 30, 0 khớp; 30 là cỡ trang | Lời cũ có trong lịch sử; response/phân trang **KHÔNG ĐO ĐƯỢC** | Đã rút cách diễn đạt |
| Issue mới | 128 mở; total_count 101 | **KHÔNG ĐO ĐƯỢC**: thiếu response/query/thời điểm/phân trang | Nhãn C:134–137 đúng |
| Tỷ lệ trang | ≈23%; 30/128 | 23,4375%; đầu vào không xác thực | Có về số học |
| Bốn Issue | #249/#295/#269/#297; cùng lớp nhưng không trùng | Có 4 ID khác nhau; nội dung/trạng thái/quan hệ Issue **KHÔNG ĐO ĐƯỢC** | Nhãn cùng nguồn có |
| t33 và hai write set | actionlint không đòi shellcheck; khác cong_cu.py | Đọc thân t33 xác nhận; hai đường dẫn mã khác nhau | Có về mã; mapping Issue vẫn thuật lại |
| Phiên đang chạy | KHÔNG ĐO ĐƯỢC | Không có nguồn runtime phiên; query Issue không chứng minh phiên | Nhãn đúng |
| #498 đã mở | nhận nợ | **KHÔNG ĐO ĐƯỢC**; C:147–148 và chú thích:223–224 hiện đều gắn nhãn | Bản vá nhãn này đúng |

**Ba biên nhận, năm hàng README và mọi nhóm trường được gọi là ĐO ĐƯỢC.** Với mỗi verdict đã chạy `git log --all --diff-filter=A --format=%H -- <path>`, đọc blob bằng `git show <commit>:<path>`, băm lại và kiểm ancestry tới snapshot đang review. URL chỉ được kiểm phần commit/path/blob; khả năng truy cập và danh tính người đăng trên GitHub không được kiểm.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| V1 byte/dòng/băm | 28.955 / 161 / a6bf4bea… | 28.955 / 161; SHA-256 `a6bf4bea67c347385960285c5e5d0d28346887da684595b6429f22a6d67aed27` | Có |
| V2 byte/dòng/băm | 43.791 / 259 / 206aaf28… | 43.791 / 259; SHA-256 `206aaf2814c5cb249506b6ae607b17a9071ac4d50eeea51b5cb031ca92531b00` | Có |
| V3 byte/dòng/băm | 48.843 / 285 / 9a244e3d… | 48.843 / 285; SHA-256 `9a244e3d5cb9adfdda4842b207019018c7f805c936d12160cdd6eeaf51f7f86b` | Có |
| BN1 reviewed_sha/tree | e826730 / 67df2efa… | `e82673014baefca23b50663cecad80fdbde79b3b` / `67df2efa7e6f6c7b23bedfb43da647b395800a37` | Có về định danh |
| BN2 reviewed_sha/tree | 1d58500 / 0430d2bd… | `1d58500b2ecaf7ccd38dcc6f8ad9bf0dbf13c77e` / `0430d2bdbc8e6e6c11bbf93c8bb12b1272b1202d` | Có về định danh |
| BN3 reviewed_sha/tree | 4e6a2d5 / 115b1835… | `4e6a2d59386335f966bfb7160e98af02ae30d1ec` / `115b1835be0a14c63669357a4c8e05a0ad542c4a` | Có về định danh |
| BN1 evidence_url | commit đầu 8104480 | Đúng 1 commit thêm: `8104480fe756978455abf1baf96adf6f9b399cbb`; URL đúng path; blob bằng byte hiện tại; ancestor rc=0 | Có phần Git |
| BN2 evidence_url | commit đầu 4d2a6f6 | Đúng 1: `4d2a6f69e67ce5299253bf8905b6b742d516f3fc`; path/blob/ancestry đúng, rc=0 | Có phần Git |
| BN3 evidence_url | commit đầu 60b99bd | Đúng 1: `60b99bdf1bb644912c10df09d05b303c73d23ccc`; path/blob/ancestry đúng, rc=0 | Có phần Git |
| Cả ba reviewed_sha | neo cây có thật, trước snapshot hiện tại | Cả ba tồn tại và đều là tổ tiên, rc=0 | Có; không xác thực phiên |
| Hai commit để nhập mỗi hồ sơ | verdict trước; receipt/index ở commit kế | 8104480→52b36d1; 4d2a6f6→4e6a2d5; 60b99bd→25974e7; lần đầu commit chỉ có verdict; lần 2/3 còn có phần vá | Có về topology; “cả bảy/cả sáu bản vá” chưa đúng trọn |
| t27 ở ba commit trung gian | đỏ; commit kế đóng lại | Checkout riêng, gọi riêng t27: rc=1 ở cả 8104480/4d2a6f6/60b99bd vì thiếu hàng; ba commit kế đều rc=0 | Có |
| so_p1/so_p2/so_p3 | V1 0/1/1; V2 0/7/0; V3 0/6/0 | Đếm tiêu đề riêng từng hạng đúng cả 9 scalar, và khớp ba hàng README | Có |
| Tổng finding và P2 | tổng 2→7; P2 1→7 | Tự đếm tổng 2,7,6; P2 1,7,6 | C/BN2/BN3 đúng; **ML2 sai cách gọi** |
| Tập bề mặt mới | 6/7; trước đây 5/7 | Theo tiêu chí đã nêu: ba về receipt/index, một về gói, một về câu pin, một về câu “Không cổng nào”; câu cuối thêm 52b36d1 | C/BN2/BN3 đúng; **ML2 còn 5/7** |
| Ba finding nhắm hồ sơ lượt 1 | 3/7 | attestation, so-hang, ke-sai-ly-do đều có vị trí ở BN1/README vừa nhập sau head V1 | Có theo tiêu chí vị trí bị chấm |
| Hai finding về khai đã vá | 2 trong 6 lượt 3 | Hai tiêu đề/source và trường loi_khai_sai của V3 tương ứng nhãn #498 và “cả bốn nơi” | Có về nội dung V3 |
| Ngưỡng ba lần; lịch sử bốn lượt | CLAUDE có ngưỡng 3; slug bị chấm 4 | CLAUDE:728–729 có quy tắc; đếm được 1 tiêu đề slug ở mỗi V1/V2/V3 = 3. Lượt connector thứ tư chỉ được thuật lại trong chỉ thị/lịch sử, không có response review | Ngưỡng 3 đã chứng minh; **4 lượt không phải 4 verdict đã đo** |
| 13 ca V1 | 13 hàng đột biến | Cắt bảng “Đột biến và phép thử”: 13 hàng dữ liệu | Có về bảng; lịch sử thực thi là reviewer thuật lại |
| 5/5 mutant prose, hai cổng | cả năm sống sau dựng manifest | Đã chạy lại đủ năm trên snapshot này; claims/build/verify đều rc=0; manifest cũ với đổi Issue rc=2 | Có trong phạm vi hai cổng |
| Cả ba reviewer không yêu cầu cổng nghĩa | 3 lượt | Đọc các đoạn kết phần đột biến/GIỚI HẠN của V1/V2/V3: đúng cả ba | Có về nội dung verdict |
| Nhãn KHÔNG ĐO ĐƯỢC trong V1 | 28; bản cũ 17 | Cắt từ BẢNG ĐO đến “Đột biến và phép thử”; đếm dòng bảng chứa nhãn: 28 | Có; 17 chỉ là lời cũ bị rút |
| Nhóm ngữ nghĩa khác trong V2 | ít nhất 21 hàng PR/Issue/CI/authority/phiên | V2:187 liệt kê V1 dòng 31,37,42–50,52–53,65,68,70–71,73–76: tự đếm 21 dòng khác nhau, đều là hàng bảng có nhãn | Có theo danh sách được chỉ rõ; không lấy quy tắc 28 thay quy tắc 21 |
| Runtime durations | 878.149 / 1242.188 / 1477.302 s; README làm tròn 878/1242/1477 | Hiệu cặp timestamp lần lượt 878.148880 / 1242.187745 / 1477.301757; làm tròn khớp | Số học đúng; timestamp thực **KHÔNG ĐO ĐƯỢC** |
| Mốc runtime 3 phiên | 06:22:49.630580→06:37:27.779460; 07:19:05.408534→07:39:47.596279; 08:10:24.176019→08:35:01.477776, ngày 10/09 | Không có run.json/log gốc của ba phiên | **KHÔNG ĐO ĐƯỢC**, toàn bộ là ATTESTATION |
| Runtime stdout/stderr | byte 297/396316; 300/539074; 291/1594141; các sha256 đi kèm | Không có sáu tệp stdout/stderr để đếm/băm | **KHÔNG ĐO ĐƯỢC**, không dùng băm được chép làm chứng thực |
| Runtime còn lại | provider/surface/transport, model yêu cầu, run/session ID, ma_thoat=0, xong, số lần chết 1/0/0 | Không có run.json/transcript; model đã phục vụ đều khai KHONG_DO_DUOC | **KHÔNG ĐO ĐƯỢC**; không có ngoại lệ scalar trong ba khối runtime |
| Prompt ba lượt | ba digest khác nhau; BN1 còn dùng grep như đối chiếu | Digest có trong receipt; prompt/run gốc không có. Riêng digest BN1 hiện nằm trong 3 tệp được liệt kê dưới đây | **KHÔNG ĐO ĐƯỢC** nội dung/nguồn prompt; số tệp đo được |
| BN1 grep | HEAD chỉ chính receipt | 1d58500: 1; 4e6a2d5: 2; 25974e7: 3 | **Không** |
| BN2/BN3/C/ML3 grep đính chính | HEAD nay 2 | Snapshot 25974e7 có thêm V3 chứa digest | **Không**, vẫn dùng mục tiêu di động |
| Diff dùng để bác lời cũ | 1d58500→HEAD cong_cu.py rỗng | Đến 4e6a2d5 rỗng; đến 25974e7 +3/−2 | **Không** với lệnh đang in |
| Cơ chế chọn cờ kho | CHAN 11, root 394e9346… | Gọi riêng chot_kho trên bản chép có origin mirror: `Chan.ma=11`, thực tế `(khong co remote)`; root `394e93468fc8d84ec20938e6df8fb7ab72b2cc37` | Có về cơ chế hiện tại; lý do/cờ phiên cũ chỉ thuật lại |
| Nợ launcher và probe | dang_chay/null; chết 1; probe rc=0/0 lỗi; lỗi111 | Không có run/log chết hoặc probe | **KHÔNG ĐO ĐƯỢC**; BN1 đã hạ nhãn đúng |
| tree_khop ⇒ đọc đúng cây | “bằng chứng dương”, kể cả BN3 mới | Chỉ đo được OID khớp; không có nhật ký đọc chứng thực phiên | **Vượt đối tượng phép đo** |
| Năng lực gói cũ, tuân thủ cấm | clean=true, commit thêm=0, các số ref gói cũ | Có lời reviewer ghi; gói cũ/run.json không được giao | **KHÔNG ĐO ĐƯỢC** lịch sử; không lấy gói hiện tại xác thực gói cũ |
| ket_qua_DO_DUOC gói 3 | reviewer đã xác nhận 9 dòng; bản vá có tác dụng | Đo được V3 chứa câu đó; không chứng thực quá trình sinh script/không gõ tay | Chỉ xác nhận nội dung lời reviewer |
| GitHub submitter và authority | actor ducthangho, tác giả PR, URL phiên vận chuyển; khong-co-lease | Chỉ đọc được scalar và quy tắc ADR-0040; actor/quyền/phiên thực **KHÔNG ĐO ĐƯỢC** | Không nâng thành merge authorization |
| Anchor canonical_ancestry | 3/3 lối đã đo trong hồ sơ #490, không đo lại | Ancestry ba anchor của PR này đo được; ba thử land #490 là dẫn lời hồ sơ khác | Không chạy lại 3 lối land, **KHÔNG ĐO ĐƯỢC** lịch sử thử đó |
| README — năm hàng | 3 mục lục + 2 cảnh báo; lượt 3 không cảnh báo | Đúng dòng 17/18 và 273/274/275; liên kết receipt/verdict, byte, SHA ngắn khớp. BN3 không có verdict_usage_caveats | Có về cấu trúc |
| README — chất lượng các trường | mục lục phản ánh bản vá và bằng chứng | Cảnh báo 1 đã sửa thật; cảnh báo 2 phân biệt hai tập; ML3 có phép đo HEAD trôi; ML2 giữ số sai; ML1/2 giữ suy luận tree quá rộng | Các lỗi cụ thể ở finding, không coi năm hàng có mặt là năm hàng đúng |

**Cổng trên exact snapshot hiện tại.** Các lệnh dưới đây chạy từ gốc bản chép nguyên vẹn của `25974e78ac4dbeb67db5f797b08b4dd276d0d666`. Đã kiểm lại bản chép có đúng SHA và `git status --porcelain` rỗng sau suite. Không có bước nào bị coi là đạt chỉ nhờ không chạy.

| khẳng định / lệnh | PR khai | đo được | khớp? |
|---|---|---|---|
| `python3 ops/lease_publish_test.py` | 146/146; đã chạy146; bỏ qua0 | rc=0; **146/146; đã chạy146; bỏ qua0** | Có |
| `python3 ops/bien_nhan_v2.py --root .` | 51 v2; legacy11/11; nợ42; vi phạm0; không đo được0; tổng104 | rc=0; **51; 11/11; 42; 0; 0; 104; TỔNG ĐẠT** | Có C/EVIDENCE; trái BN3:98 |
| `python3 ops/bien_nhan_v2_test.py` | 48/48; mutant63/63; tự kiểm2/2 | rc=0; **48/48, 63/63 CÓ RĂNG, 2/2 tự kiểm** | Có |
| `python3 ops/cong_cu.py kiem-tra --json` | rc0; tổng DAT; canary DAT | Đúng; SC1003 từ fixture rc=1 | Có |
| `python3 ops/cong_cu_test.py` | ca23; mutant18; lỗi0 | rc=0; **23/23 đạt, bỏ qua0; 18 đột biến; lỗi0** | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | ok; expected=checked180; extra=[] | rc=0; ok=true; **180=180; failed=[]; extra_files=[]** | Có |
| `python3 scripts/tl.py golden-test --json` | ok=true | rc=0; ok=true; 20 case đạt | Có |
| `python3 scripts/tl.py determinism-audit --strict --json` | ok=true | rc=0; ok=true; 15 checks đạt | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` | ok=true | rc=0; ok=true; 106 tệp; flags=[] | Có |
| `python3 scripts/tl.py workflow-audit --strict --json` | rc=0 | rc=0; ok=true | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 | rc=0; 7 tệp; 0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc=0 | rc=0; 46 ADR/46 hàng; ngoại lệ trạng thái0016 được khai | Có |
| Lease trước merge, checkout 52b36d1 ở bản chép lịch sử | 121/121 | Chạy lại suite: rc=0; **121/121, đã chạy121, bỏ qua0** | Có |
| Validator lịch sử | 4d2a6f6:49/102; 4e6a2d5:50/103 | Checkout riêng từng SHA, cùng lệnh validator: **49/102 và 50/103**, đều rc=0 | Có |
| Môi trường | actionlint1.7.7; shellcheck0.9.0; jsonschema4.26.0 | Probe thực đúng cả ba; PyYAML thực6.0.1 | Có; không cài thêm |
| CI ghim | 2/3 bản trên | ci.yml:93 ghim jsonschema4.26.0, :97 AL_VER1.7.7; :101 không ghim shellcheck; cong_cu.yaml shellcheck.ban_ghim=null | Có |
| Nền reviewer lượt 1 | jsonschema thiếu, lỗi mutant1, tổngDO | Không có môi trường cũ ở đây; V1 khai rõ; nền hiện tại có jsonschema nên không tái xác thực trạng thái cũ | **KHÔNG ĐO ĐƯỢC** lịch sử nền; không quy thành hồi quy |
| Không có máy cưỡng chế ba nếp | C:417/BN3:152 nói không cổng nào | Các mutant và bản gốc có lời sai vẫn qua cổng đã thử; chưa kiểm mọi cổng với mọi cách vi phạm ba nếp | Chỉ đo phạm vi đã thử; mệnh đề tuyệt đối toàn kho **KHÔNG ĐO ĐƯỢC** bằng tập thử này |
| Số lệnh so CI | EVIDENCE12; C10; CI31 bước cổng | Đếm EVIDENCE12, khối C:307–316 có10; YAML40 = setup8 + cổng31 + upload1 (setup vị trí1–7,9; upload29) | Có; không gọi là đủ CI |
| CI cho head này | cố ý chưa chạy | **KHÔNG ĐO ĐƯỢC** trạng thái/quyết định GitHub; không yêu cầu chạy thêm | Không coi là cổng đỏ |

**Đột biến: báo cả hai chiều.** Mỗi ca phục hồi byte gốc trước ca kế tiếp. Bỏ từng mảnh riêng ở mỗi hồ sơ; không coi một crash giàn giáo là tín dụng giết mutant. Lệnh gọi chốt:

```sh
python3 -c "import sys; sys.path.insert(0,'ops'); import lease_publish_test as t; t.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()"
python3 -c "import sys; sys.path.insert(0,'ops'); import lease_publish_test as t; t.t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()"
python3 -c "import sys; sys.path.insert(0,'ops'); import cong_cu_test as t; t.t13_actionlint_bien_mat_giua_probe_va_canary()"
```

| khẳng định / đột biến | PR khai hoặc đối chứng | đo được | khớp? |
|---|---|---|---|
| Hồ sơ nguyên vẹn | t26/t27 xanh | rc=0/0; sau phục hồi cũng0/0 | Có |
| Bỏ receipt lượt 1/2/3 | thiếu một mảnh | t27 **rc=1/1/1**, báo thiếu đúng receipt | Có răng3/3 |
| Bỏ hàng mục lục lượt 1/2/3 | thiếu một mảnh | t27 **rc=1/1/1**, báo đúng verdict không ở cột mục lục | Có răng3/3 |
| Bỏ chính verdict lượt 1/2/3 | kiểm chiều ngược | t27 **rc=0/0/0**; t26 **rc=1/1/1**, trỏ tệp không có | t27 riêng không cưỡng chế đủ ba mảnh; t26+t27 bắt đủ |
| Bỏ hàng cảnh báo lượt 1/2 | caveat phải tới mục lục | t27 **rc=1/1**, đúng caveat thiếu | Có răng2/2 |
| Lượt 3 không có cảnh báo | không caveat trong BN3 | Không có hàng để bỏ; thiếu cảnh báo không tự là lỗi khi không khai caveat | Không dựng thêm nghĩa vụ |
| Đổi một chữ số verdict_sha256 ở từng receipt | neo băm phải bắt | validator **rc=1/1/1**, 1 vi phạm mỗi ca | Có răng3/3 |
| verdict_bytes cộng1 ở từng receipt | scalar byte | validator **rc=0/0/0** | Không canh trường này; giá trị gốc đã tự đo đúng |
| so_p2 cộng1 ở từng receipt | scalar số finding | validator **rc=0/0/0** | Không canh trường này; giá trị gốc đã tự đo đúng |
| Tắt vòng canary, if chi is None→if False | t13 cần bắt | t13 **rc=0→1**, TinHieuChotCa “canary mất executable bị nuốt” | Có răng đúng chốt |
| Cùng mutant, full scan thiếu shellcheck | mất cơ chế | tổng **DO/rc2→DAT/rc0**, canary=[] | Mất chặn thật |
| Bỏ vòng nâng tổng canary | phân biệt kết quả và quyền chặn | canary vẫn DO, tổng DAT/rc0 | Đúng quan hệ mô tả |
| Đổi blocking thành advisory | ngoại lệ | canary vẫn DO/advisory, tổng DAT/rc0 | Đúng ngoại lệ |
| Issue128→129, manifest cũ | toàn vẹn byte | release-verify **rc=2, ok=false** | Có răng với byte |
| Issue128→129, dựng lại manifest | nghĩa lời khai | claims/build/verify **0/0/0** | Sống |
| 37→36 success, giữ4 skip/tổng41 | mâu thuẫn số học | claims/build/verify **0/0/0** | Sống |
| Cha thứ nhất đổi thành cha thứ hai | OID thật, quan hệ sai | claims/build/verify **0/0/0** | Sống |
| Xuất xứ#290 đổi thành chủ | sai thẩm quyền | claims/build/verify **0/0/0** | Sống |
| Mù1 đổi thành0 | sai số lịch sử | claims/build/verify **0/0/0** | Sống |
| Thử vá năm finding của lượt này | nhãn, tree, snapshot, số bảng, hàng mục lục | Trên bản chép: validator, t27, claims, build manifest, verify đều **rc=0** | Khả thi với cổng đã chạy; xanh không chứng minh nghĩa đúng |

Năm ca prose chạy `doc-claims-check --strict --json`, `release-manifest --out RELEASE_MANIFEST.json --json`, `release-verify RELEASE_MANIFEST.json --strict --json` qua `python3 scripts/tl.py`. Để A/B PATH, dựng wrapper trong sandbox gọi executable sẵn có; chỉ bỏ/thêm wrapper shellcheck. Không sao chép hay sửa tệp công cụ ngoài sandbox.

Không yêu cầu mở rộng validator trong PR hồ sơ này. Hàng C:171 đòi đúng mục lục/cảnh báo được t27 kiểm; nếu diễn đạt rộng thành bảo đảm tồn tại đủ verdict/receipt/index, phải nêu cặp **t26+t27**. Không gán ba ca sống của riêng t27 thành cả suite bỏ lọt.

### hai-loi-khai-thieu-nhan-va-sai-co-trang  [P2]  Nhãn #498 đã vá thật nhưng sự kiện CI và số lượt connector vẫn vượt nguồn

TỆP/DÒNG: `cay-kho/CHANGELOG.md:103–111`, `:376–385`; `cay-kho/ops/cong_cu.py:218`; `cay-kho/ops/reviews/pr497-review-3-codex-verdict.receipt.yaml:135–141`; đối chiếu C:273 và BN3:3 về “cả sáu đã vá”.

VẤN ĐỀ: Đính chính #498 lần này đã được áp vào mã thật. Phần còn lại của finding lượt 3 — diễn biến lượt Windows/rg đỏ/G5 skip — chưa có hunk sửa, vẫn được kể trần ở §2 và trong khối “NỢ ĐÃ ĐO” của chú thích. Cấu hình hiện tại cho phép diễn biến đó không chứng thực rằng lượt GitHub được kể đã diễn ra như vậy. §4 mới còn xếp “4 lượt, gồm connector 1 trong 3 P2” vào phép đếm ĐO ĐƯỢC. Có ba verdict địa phương, mỗi tệp một tiêu đề slug; lượt connector được người giao việc và lịch sử thuật lại, không có response review để đo độc lập. Ngưỡng ba lần đã đạt bằng ba tệp thật, không cần biến lượt thứ tư thành phép đo. Đây là phần chưa đóng của cùng lỗi giới hạn nguồn, không phải kết luận các sự kiện GitHub chắc chắn sai.

ĐÃ THỬ VÁ: có — trên bản chép thêm nhãn THUẬT LẠI/thiếu log ngay trước diễn biến Windows và ở chú thích, tách “ba lượt đếm được + một lượt connector thuật lại” trong §4/receipt. Giữ các ID và số được kể. Cách khóa lỗi: liệt kê từng vị trí hiện hành của nhãn/sự kiện, kiểm từng hunk rồi mới kết luận đã vá. Tránh để một nhãn ở CHANGELOG được coi là phủ cả chú thích ở tệp khác; không cần tạo cổng nghĩa hay chạy CI mới.

ĐÃ THỬ NGHIỆM: `git -C cay-kho diff 4e6a2d5 25974e7 -- ops/cong_cu.py CHANGELOG.md` xác nhận chỉ nhãn #498 có hunk tại đoạn bị chấm cũ; đoạn CI không đổi. Parse workflow ở bốn SHA nêu trong bảng cho cùng blob, không có dữ liệu job runtime. Python đếm tiêu đề `### hai-loi-khai-thieu-nhan-va-sai-co-trang` trong V1/V2/V3 trả 1/1/1. Bản sửa nhãn qua `bien_nhan_v2`, t27, doc-claims, dựng manifest và release-verify, tất cả rc=0. Giá trị/sự kiện GitHub: **KHÔNG ĐO ĐƯỢC**, không mạng và không response gốc.

ĐỘ TIN: cao về thiếu nhãn và phạm vi phép đếm; không phán đoán giá trị GitHub thật.

### attestation-runtime-bi-nang-thanh-phep-do  [P2]  Khớp tree vẫn bị dùng để chứng thực hành vi đọc, kể cả trong biên nhận mới

TỆP/DÒNG: `cay-kho/CHANGELOG.md:184–186`; `cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml:77–80`; receipt lượt 2:48–51; receipt lượt 3:43–46; `cay-kho/ops/reviews/README.md:274–275`.

VẤN ĐỀ: Hai ngoại lệ trong khối runtime đã được hạ đúng thành thuật lại; receipt lượt 3 cũng không cấp ngoại lệ scalar runtime. Nhưng phần còn lại của finding cũ không đổi: việc OID trong verdict bằng OID từ Git vẫn được gọi là bằng chứng “reviewer đọc đúng cây”. Receipt mới lặp lại câu đó rồi nói không xác nhận “hành vi runtime nào”, tạo mâu thuẫn ngay trong trường `tree_khop`. Phép so xác nhận định danh nhất quán, không xác thực việc phiên đã đọc các tệp của cây đó. Không có kết luận reviewer đọc sai cây hoặc không chạy test; điều sai là mức chứng thực mà phép so được gán.

ĐÃ THỬ VÁ: có — trên bản chép đổi đúng sáu nơi gồm CHANGELOG, ba receipt, hai hàng README thành “định danh cây khớp; không xác thực hành vi đọc/phiên”. Không sửa OID hoặc verdict đã neo băm. Kiểm khóa: đối chiếu đối tượng của từng câu kết luận với đầu vào thực của phép đo. Tránh đẩy câu quá rộng sang một trường khác hoặc xóa mất phép khớp định danh vốn vẫn có ích.

ĐÃ THỬ NGHIỆM: `git -C cay-kho rev-parse e826730^{tree} 1d58500^{tree} 4e6a2d5^{tree}` cho đúng ba OID trong bảng; lệnh này chỉ tra định danh, không đọc nội dung tệp trong tree. Diff `4e6a2d5..25974e7` của BN1/BN2/CHANGELOG/README không sửa các câu bị nêu; BN3 thêm câu lặp. Gọi riêng `launcher.chot_kho(str(Path.cwd()), 'ducthangho/tra-luat', None)` ở bản chép cho `Chan.ma=11`, đúng cơ chế, không tái xác thực cờ phiên cũ. Sau sửa sáu nơi: validator/t27/doc-claims/build/verify đều rc=0. Hành vi phiên cũ: **KHÔNG ĐO ĐƯỢC**, thiếu log/runtime gốc.

ĐỘ TIN: cao.

### phep-grep-prompt-khong-ghim-snapshot-sau-khi-nhap-verdict  [P2]  Biên nhận mới tiếp tục dùng HEAD cho hai phép đo đã đổi kết quả

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml:146–147`; receipt lượt 2:73–82; receipt lượt 3:12,58,106–114; `cay-kho/CHANGELOG.md:278–282`, `:389–407`; `cay-kho/ops/reviews/README.md:273`.

VẤN ĐỀ: Bản sửa chỉ ghim lệnh trong BN2, bỏ sót BN1. Digest trên snapshot đang review có ba tệp chứa nó: BN1, V2, V3. BN1 vẫn khai một; lời đính chính mới trong BN2/BN3 nói HEAD nay hai. Cùng lúc, câu `git diff 1d58500 HEAD -- ops/cong_cu.py ⇒ rỗng` được chép thêm vào bốn nơi mới, nhưng chính bản vá #498 làm diff ấy khác rỗng. Hai kết quả lịch sử đúng tại `4e6a2d5` đang được trình bày bằng lệnh phụ thuộc HEAD hiện tại. Đây là đúng lỗi mà nếp “ghim snapshot” vừa nhận phải chặn, và trái lời BN3:12 về các phép Git GHIM SHA. Một câu hướng dẫn tổng quát dùng HEAD khác một kết quả lịch sử được trích làm bằng chứng; finding nhắm loại thứ hai.

ĐÃ THỬ VÁ: có — trên bản chép ghim `1d58500` cho phép grep ra một tệp, `4e6a2d5` cho phép grep ra hai và diff mã rỗng; nêu snapshot `25974e7` có ba bản chép. Sửa BN1 và các bản lặp mới; giữ nguyên V1/V2/V3 đã neo hash. Kiểm khóa bằng chạy truy vấn trên từng SHA được trích, liệt kê tập tên thật. Không biến ba bản chép digest thành ba nguồn prompt độc lập.

ĐÃ THỬ NGHIỆM: đã chạy cùng digest đầy đủ ở cả ba SHA:

```sh
git -C cay-kho grep -l fd117770fa4c651aad6194d4dfb9adfc51b60ba78a3a9ea4928823799c480c85 1d58500 -- .
git -C cay-kho grep -l fd117770fa4c651aad6194d4dfb9adfc51b60ba78a3a9ea4928823799c480c85 4e6a2d5 -- .
git -C cay-kho grep -l fd117770fa4c651aad6194d4dfb9adfc51b60ba78a3a9ea4928823799c480c85 25974e7 -- .
git -C cay-kho diff 1d58500 4e6a2d5 -- ops/cong_cu.py
git -C cay-kho diff 1d58500 25974e7 -- ops/cong_cu.py
```

Kết quả: grep rc=0 cả ba, lần lượt 1/2/3 tệp; diff đầu rc=0/stdout rỗng, diff sau rc=0/hunk +3/−2. Diff sửa lượt 3 của BN1 không chứa hunk sửa grep. Bản thử ghim qua validator/t27/doc-claims/build/verify, tất cả rc=0. Không dùng rc=0 của Git diff để suy stdout rỗng.

ĐỘ TIN: cao.

### bang-cong-r362-con-neo-so-truoc-bien-nhan-luot-hai  [P2]  CHANGELOG đã đúng 51/104 nhưng biên nhận lượt 3 mới khai đã đo 50/103 sau bước cuối

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-3-codex-verdict.receipt.yaml:91–99`; đối chiếu `cay-kho/CHANGELOG.md:301–308` và `EVIDENCE.md:41`.

VẤN ĐỀ: Cổng thực và bảng CHANGELOG lần này đã được cập nhật sau khi thêm receipt lượt 3, đúng `51 ĐẠT v2/tổng 104`. Nhưng trường `da_va` trong receipt mới nói đã đổi sang `50 · 103` và đo lại “trên exact HEAD sau bước cuối”. Đây là mô tả bản sửa mới, không được neo như phép đo cũ của reviewer. `50/103` là kết quả của cây trước khi thêm receipt mới; tất cả rc vẫn bằng 0 nên nhìn trạng thái xanh không thấy mâu thuẫn. Nếp chạy lại bảng sau bước cuối được áp ở một bản lặp và chưa áp ở bản lặp còn lại.

ĐÃ THỬ VÁ: có — trên bản chép đổi trường này sang `51/104` và ghim snapshot của phép đo. Phương án khác là giữ `50/103` nhưng ghi rõ là kết quả ở `4e6a2d5`, rồi dẫn kết quả mới riêng. Kiểm khóa: sau bước nhập hồ sơ cuối, lấy lại các scalar từ validator và so mọi vị trí hiện hành, không chỉ bảng CHANGELOG. Rủi ro: nhập receipt kế tiếp lại tăng bộ đếm; phép đo lịch sử phải giữ SHA của nó.

ĐÃ THỬ NGHIỆM: checkout riêng `4d2a6f6`, `4e6a2d5`, `25974e7` trên bản chép lịch sử, chạy `python3 ops/bien_nhan_v2.py --root .`: lần lượt **49/102, 50/103, 51/104**, cả ba rc=0 và không vi phạm. Chạy lại trên bản chép nguyên vẹn exact SHA cũng **51/104**. Bản thử sửa trường qua validator/t27/doc-claims/build/verify, tất cả rc=0.

ĐỘ TIN: cao.

### dem-finding-doi-mau-va-bo-sot-phan-moi  [P2]  Hàng README lượt 2 vẫn giữ nguyên cả hai số sai dù biên nhận mới khai đã sửa

TỆP/DÒNG: `cay-kho/ops/reviews/README.md:274`; đối chiếu `cay-kho/CHANGELOG.md:255–261`; receipt lượt 2:151–174; receipt lượt 3:115–125 và :74–76.

VẤN ĐỀ: CHANGELOG và BN2 đã sửa đúng. Nhưng hàng ML2 vẫn viết “Số finding tăng 1→7” và `5/7`, trong khi chính ML3 ở hàng ngay trên kể đúng tổng `2→7` và `6/7`. Đây không phải trích dẫn lời cũ được rút trong ML2: nó là lời tổng kết đang dùng. Toàn bộ nội dung hàng ML2 bằng byte với hàng cùng verdict tại `4e6a2d5`; diff README chỉ sửa cảnh báo lượt 1 và thêm hàng lượt 3. Vì thế BN3:125 khai đã sửa cách gọi/tập mới và BN3:75 khai đã kiểm đủ 5/5 đường dẫn chưa được bằng chứng từng mệnh đề chống lưng. Đường dẫn README có diff, hàng cần sửa thì không.

ĐÃ THỬ VÁ: có — trên bản chép sửa chính hàng ML2 thành “P2 tăng 1→7; tổng tăng 2→7; 6/7 theo tiêu chí bề mặt mới”, giữ các mức P1/P2/P3 và neo verdict đúng. Kiểm khóa: lấy hàng theo liên kết verdict, so cả hai số/cách gọi với tổng tiêu đề và danh sách sáu trường hợp; không chỉ grep thấy câu đúng ở một hàng khác. Không dùng tổng finding để khẳng định chất lượng tăng hoặc giảm.

ĐÃ THỬ NGHIỆM: Python đếm tiêu đề từng hạng trên V1/V2/V3: **0/1/1, 0/7/0, 0/6/0**. So hàng chứa liên kết V2 bằng `git show 4e6a2d5:ops/reviews/README.md` với bản hiện tại: bằng nhau. `git -C cay-kho diff 4e6a2d5 25974e7 -- ops/reviews/README.md` không có hunk sửa hàng ấy. `git -C cay-kho log -S 'Không cổng nào' 25974e7 -- CHANGELOG.md` trả 52b36d1 (thêm), 4d2a6f6 (sửa), 60b99bd (nhắc lại trong đính chính); đọc blob 52b36d1 và e826730 xác nhận phần bị chấm thứ sáu mới xuất hiện sau lượt 1. Bản thử sửa hàng qua validator/t27/doc-claims/build/verify đều rc=0; t27 nguyên bản cũng xanh khi hai số còn sai, nên sự hiện diện của hàng không chứng thực nội dung.

ĐỘ TIN: cao.

## GIỚI HẠN

- Không truy cập mạng, GitHub hay các tệp ngoài sandbox. Các lệnh hệ thống/Python dùng môi trường được cấp; mọi tệp công việc, cache và thư mục tạm do review tạo đều ở sandbox. Không có kết luận trực tiếp về PR/Issue/review/check/attempt, người duyệt, quyền land hay trạng thái CI. Sự không đo được không là cổng đỏ và không phải yêu cầu đốt CI mới.
- URL evidence được kiểm Git object/path/ancestry, không kiểm truy cập GitHub. Tệp ls-remote được kiểm byte và tập tên/OID; nguồn và timestamp vẫn là ATTESTATION. Không có bộ đệm trước fetch hoặc gói cũ của các lượt 1–3; lời reviewer về gói cũ được phân biệt với phép đo gói lượt 4.
- Không có run.json, prompt hoặc stdout/stderr của ba phiên cũ. Phép tính timestamp, so OID hoặc đọc digest không xác thực danh tính/hành vi phiên. Chỉ xác nhận nội dung mà các hiện vật trong cây thực sự ghi.
- Đã chạy đủ 12 lệnh EVIDENCE, suite lease trước merge, các chốt riêng, đột biến và bản sửa thử nêu trên. Không chạy cả 31 bước CI, Windows hoặc ba lối land của hồ sơ #490. Các ca sống được báo đúng phạm vi cổng đã thử.
- Không tự soạn nội dung tấn công. Chỉ chạy suite/fixture có sẵn, bỏ hiện vật/hàng, đổi chữ số/chữ mô tả/chính sách/điều kiện trong bản chép. Các hướng cần nội dung thoát, đồng tự hoặc đường dẫn vượt cây chỉ được mô tả bằng lời.
- Bản sửa thử chỉ là kiểm khả thi, không áp lên PR; giữ nguyên băm của ba verdict. Các câu trong commit message và verdict lịch sử được đọc theo snapshot lịch sử, không yêu cầu sửa lịch sử để che finding. Phần cần sửa là lời khai hiện hành ở CHANGELOG/receipt/mục lục.
- Phép đo CUỐI sau khi dọn bản chép: cả **9/9 trường** trong EVIDENCE = do-goi = cấu hình thực; mirror **324 = 323 + 1**; raw **322 dòng / 25.944 byte**, băm khớp. Không phát hiện lệch đo được giữa EVIDENCE/do-goi của gói lượt 4 và gói thực. Đã dọn mọi script/log/bản chép tạm do review này tạo; sản phẩm mới duy nhất do tôi giữ lại là `VERDICT.md`. Các hiện vật của trình chạy phiên có sẵn ở gốc sandbox không bị chỉnh sửa.
- Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**; HEAD vẫn `25974e78ac4dbeb67db5f797b08b4dd276d0d666`. Không sửa cây được review hoặc mirror.
