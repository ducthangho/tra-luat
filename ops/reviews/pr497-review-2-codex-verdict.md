verdict: changes_requested
reviewed_sha: 1d58500b2ecaf7ccd38dcc6f8ad9bf0dbf13c77e

Review lượt 2 bằng OpenAI/Codex, dùng shell qua API trong sandbox được giao. Tree tự đo: `0430d2bdbc8e6e6c11bbf93c8bb12b1272b1202d`. Kết quả: **0 P1 / 7 P2 / 0 P3** (gồm P2 còn tồn tại từ lượt 1). Cả **12 lệnh cổng** trong EVIDENCE đạt khi chạy lại; các finding dưới đây thuộc tính đúng và giới hạn của lời khai, không phải hồi quy runtime của khối chú thích.

## ĐỐI CHIẾU LƯỢT 1

- `hai-loi-khai-thieu-nhan-va-sai-co-trang`: **VÁ HỜ** — `CHANGELOG.md:122–139` đã gắn nhãn đúng cho 128/101, bốn Issue và #498; phép chia được tách khỏi đầu vào; “~7 giờ” được rút và khai thiếu mốc đọc CI. Nhưng phạm vi finding lượt 1 còn bao gồm số ref máy chủ lịch sử: đoạn 7–22 vẫn xếp “mọi số Git” vào tự đo được và ghi trần 320/320, mù 1, sau fetch 0. Đoạn mới 216–234 tiếp tục ghi 322/321, MÙ 2, THỪA 1 như phép đo có thể đối chiếu, không có nhãn nguồn tại chỗ. `ops/cong_cu.py:223` cũng còn “nợ đã mở thành Issue #498” không nhãn. Tự chạy `ls-remote --heads origin` được 324 head của **mirror**, so bộ đệm được 324/324; tệp máy chủ chỉ xác nhận được 322 dòng của một attestation, không có snapshot bộ đệm trước fetch. Đột biến mù 1 thành 0 vẫn qua doc-claims và release-verify sau tái sinh manifest. Đây là lần thứ hai trong chuỗi lượt 1 → lượt 2 slug này còn **VÁ HỜ**; không phủ nhận phần nhãn Issue đã sửa thật.
- `dan-protocol-nham-so-dong-thanh-so-muc`: **ĐÃ VÁ THẬT** — `CHANGELOG.md:116–117` dẫn `docs/PROTOCOL_DA_PHIEN.md:28`, `:116`, `:164`; `ops/cong_cu.py:221` ghi rõ DÒNG 28/116/164. `rg -n '^## [0-9]+' cay-kho/docs/PROTOCOL_DA_PHIEN.md` đếm **20 mục chính**, từ §1 đến §20. Ba câu nằm đúng dòng 28, 116, 164; mục chứa chúng lần lượt là **§1, §3.1.1, §3.2**. `§28/§116/§164` còn xuất hiện ở phần thuật lại finding cũ trong §3/biên nhận, nơi nói rõ chúng là cách dẫn sai, không phải dẫn chiếu đang dùng. Doc-claims strict và release-verify strict trên cây thật đều rc=0.

## BẢNG ĐO

Quy ước: **KHÔNG ĐO ĐƯỢC** không có nghĩa là sai, cũng không có nghĩa là đạt. Tính đúng phép cộng, băm hay so tập trên hiện vật không xác thực xuất xứ GitHub/runtime của hiện vật đó. Các lệnh Git và 12 cổng nền chạy trong `cay-kho/`; checkout lịch sử, đột biến và thử sửa chạy trong `.review-tmp/copy`, là bản chép riêng trong sandbox. Đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` và cấu hình Git global riêng trong sandbox; `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`. Không fetch hoặc gọi GitHub.

Các nhóm phép đo để tái lập:

- **GIT**: `git -C cay-kho rev-parse HEAD`, `HEAD^{tree}`, `--is-shallow-repository`; `git config --local --get remote.origin.url`, `core.abbrev`; `git diff --no-ext-diff 0721811..HEAD`, `--numstat`, `--check`; `git show`, `git merge-base --is-ancestor` tại SHA ghi trong bảng.
- **REF**: `git -C cay-kho ls-remote --heads origin`; `git -C kho.git for-each-ref --format='%(refname)' refs/heads`; `git -C cay-kho for-each-ref --format='%(refname)' refs/remotes/origin`. Bỏ đúng alias `HEAD`, chuẩn hóa tiền tố rồi so tập tên và OID. Quét **tiêu đề mục** r360/r362/r363 trong `git show <ref>:CHANGELOG.md` trên toàn bộ tập, không đếm lần nhắc trong văn xuôi.
- **BLOB**: Python `hashlib.sha256`, `len(read_bytes())`, `len(splitlines())`; `git log --all --diff-filter=A --format=%H -- ops/reviews/pr497-review-1-codex-verdict.md`; băm lại blob ở commit neo và so với tệp thật.
- **CI-TĨNH**: parse `jobs.gate.steps` trong `.github/workflows/ci.yml` tại `8cee941`, `7693852`, `28ba133`, HEAD. Số bước runtime được kể tương ứng vị trí YAML cộng một bước setup job; đây chỉ là đối chiếu cấu trúc.
- **GÓI**: đọc đủ 180 mục manifest, tự tính kích thước/SHA-256 từng tệp và so với manifest ở `0721811`; sau đó chạy release-verify strict.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head và tree | `1d58500`; cây đã merge master | SHA đầy đủ đúng đầu báo cáo; tree `0430d2bdbc8e6e6c11bbf93c8bb12b1272b1202d`; detached | Có |
| Clone đầy đủ; viết tắt | không nông; core.abbrev=7 | Cả `cay-kho` và `kho.git` shallow=false; cấu hình local abbrev=7 | Có |
| Origin trong EVIDENCE đã sửa | mirror trong sandbox | URL local trỏ đúng `<sandbox>/kho.git`; ls-remote rc=0, đọc mirror | Có; không phải phép hỏi GitHub |
| Số nhánh thực trong gói | EVIDENCE: 323 | Mirror **324** heads; bộ đệm 325 ref kể alias HEAD, **324** sau loại alias; thiếu/thừa giữa hai tập đều 0 | **Không — finding về gói** |
| Ref giao exact head | không giải thích ref phụ | `pr497-head` → `1d58500`; `claude/handoff-tra-luat-repo-2ak5th` → **e826730**. Hai ref khác OID, không phải hai bí danh của cùng commit | Phải khai rõ phạm vi đếm |
| Diff giao so master hiện tại | `0721811..HEAD`, 6 tệp | `diff.patch` khớp từng byte diff Git; `numstat.txt` khớp. Tổng 6 tệp, +613/−5 | Có |
| Chi tiết diff | CHANGELOG, manifest, comment, hồ sơ | +239/−0 CHANGELOG; +5/−5 manifest; +16/−0 cong_cu.py; +2/−0 README; +161 verdict; +190 receipt | Có |
| Chỉ chú thích trong cong_cu.py | không đổi runtime | AST tại `0721811` và HEAD bằng nhau; diff đúng 16 dòng chú thích; `git diff --check` rc=0 | Có |
| Ngày r362 | 2026-09-10 | Commit đầu `25c2d5b` 03:43:16Z; HEAD 07:03:13Z, cùng ngày | Có về ngày Git |
| Phạm vi nội dung | hai việc chính, thêm §3 ghi review | Đủ §1 đóng nợ #490, §2 rút lời khai shellcheck, §3 hồ sơ review | Có |
| VERSION từ r336 | không nâng; 1.36.68 | VERSION hiện tại và tại `3dcdc6a` cùng 1.36.68; diff VERSION rỗng | Có |
| r360 đã bị chiếm | nhánh khác chưa merge | Đúng 1 ref có tiêu đề r360: `claude/pr491-land-va-findings-wip`. Đầu tệp hiện tại của ref này đã là r361; lịch sử chọn số và trạng thái PR/phiên **KHÔNG ĐO ĐƯỢC** | Có về mục tồn tại; không xác thực GitHub |
| Phép canh ref lịch sử đầu r362 | 320 máy chủ / 320 bộ đệm | **KHÔNG ĐO ĐƯỢC**: không có hai tập lịch sử; hiện vật hiện tại là 324/324 cục bộ | Thiếu nhãn nguồn |
| Nhánh mù lịch sử | MÙ 1: `codex/wp484-g3-windows` | Ref hiện có; trạng thái mù tại thời điểm kể **KHÔNG ĐO ĐƯỢC** | Chưa xác minh lịch sử |
| Sau fetch lịch sử | mù 0; quét 320; r362 chỉ 1 | **KHÔNG ĐO ĐƯỢC** thao tác/thời điểm và tập 320; snapshot gói khác | Thiếu nhãn nguồn |
| Nội dung nhánh g3 từng mù | đầu tệp r356 | `git show refs/remotes/origin/codex/wp484-g3-windows:CHANGELOG.md`: dòng đầu đúng r356 | Có |
| Tệp thô máy chủ lượt 2 | 322 dòng; ec6ef20a…; 07:04:17Z | **322** dòng, 322 tên duy nhất; SHA-256 **ec6ef20af4eb7f734fcb0e321c86b93d0efbb34493630e968fcfb138b51b5ec8**. Nguồn GitHub và giờ chụp **KHÔNG ĐO ĐƯỢC** | Byte/số dòng đúng; xuất xứ là ATTESTATION |
| Phép canh mới trước fetch | 322/321 | 322 đếm được trong tệp thô; **321 trước fetch KHÔNG ĐO ĐƯỢC** vì gói không có snapshot bộ đệm lúc ấy | Không xác nhận cả cặp bằng snapshot hiện tại |
| Hiệu tập mới trước fetch | MÙ 2: land-492-bookkeeping, wp484-g4-windows; THỪA 1: pr487-merge | Hai tên mù được kể đều có trong tệp thô và mirror hiện tại; pr487-merge chỉ có trong mirror. **KHÔNG ĐO ĐƯỢC** việc hai tên ấy vắng ở bộ đệm trước fetch | Tên hiện vật nhất quán; lịch sử là lời kể |
| Số học lệch tập | 322−321=1 nhưng mù 2/thừa 1 | 322−321=1; 2−1=1. Điều kiện số học đúng, không chứng minh hai tập đầu vào | Có về số học |
| So tệp thô với mirror hiện tại | sau fetch mù 0 | Thiếu tên/OID từ tệp thô: **0**; tất cả OID chung khớp. Mirror thừa **2**: `pr487-merge`, `pr497-head` | Có cho snapshot hiện tại; không chứng minh fetch lịch sử |
| Quét r362 trên 323 ref | đúng 1, chính nhánh PR | Quét cả **324** ref thật: **2** ref có tiêu đề r362, là nhánh PR ở e826730 và pr497-head ở 1d58500. Nếu loại riêng ref giao head, còn 323/1 | Phải phân biệt snapshot gói với tập nguồn được kể |
| Quét r363 | 1 ở `claude/land-492-bookkeeping` | Quét cả 324 ref: **đúng 1**, đầu CHANGELOG của ref đó là r363 | Có; “vừa mù” là lịch sử chưa đo được |
| Ba P2 trước lượt 1; P2 ×2 cuối §2 | 3 nhóm đính chính | Diff `25c2d5b..e826730` và verdict lượt 1 nêu ba nhóm; kết quả review GitHub gốc **KHÔNG ĐO ĐƯỢC** | Có hồ sơ thuật lại, không xác thực GitHub |
| Ba vế ADR-0034 | merged, hậu-merge gate, bookkeeping | ADR-0034 và CONTEXT yêu cầu vào canonical + hậu-merge gate + bookkeeping | Có về định nghĩa |
| Merge #490 và hai cha | 8cee941; 00e017a + 01e7f77 | Git trả `8cee9410e958a6b9d956e080c11878fbd80d9f5f`, cha `00e017af102bc8355e0c276d2d813e20620ddb42` + `01e7f77d707cb093b5ba6d9b9d8577f40d025488` | Có trong Git |
| Nợ r359 | chưa đọc CI; 0 hiện vật CI neo 8cee941 | Tại `71e0053`, `git grep -l 8cee941` chỉ thấy CHANGELOG. HEAD thấy thêm receipt review 7 và verdict lượt 1, đều không phải response CI thô | Có trong phạm vi hiện vật kho |
| CI đánh số | 41 bước mỗi job | YAML có **40** bước khai báo; lời kể dùng thêm setup job. **41 bước runtime KHÔNG ĐO ĐƯỢC** | Cấu trúc nhất quán |
| Ubuntu #490 | success; 37 success, 4 skipped, 0 failure | 37+4+0=41; kết quả job thực **KHÔNG ĐO ĐƯỢC** | Số học đúng; đã có nhãn CI thuật lại |
| Windows #490 | success; 35 success, 6 skipped, 0 failure | 35+6+0=41; kết quả job thực **KHÔNG ĐO ĐƯỢC** | Số học đúng; đã có nhãn CI thuật lại |
| Thời lượng Ubuntu | 18:50:37Z → 19:11:32Z | Hiệu hai giờ được kể: **20 phút 55 giây**; mốc runtime **KHÔNG ĐO ĐƯỢC** | Số học đúng |
| Thời lượng Windows | 18:50:37Z → 19:44:09Z | Hiệu: **53 phút 32 giây**; mốc runtime **KHÔNG ĐO ĐƯỢC** | Số học đúng |
| Danh tính run #490 | 34391481045; push; master; head 8cee941 | **KHÔNG ĐO ĐƯỢC**: không response Actions, không mạng | ATTESTATION |
| Attempt #490 | 1, không chạy lại | **KHÔNG ĐO ĐƯỢC** lịch sử attempt | ATTESTATION |
| Hai run đối chiếu | 7693852 attempt 2; 28ba133 attempt 1 | Hai commit có thật; attempt/kết quả **KHÔNG ĐO ĐƯỢC** | Chỉ Git xác nhận được |
| Ba run cùng hình dạng skip | 3 lượt; 4 Ubuntu, 6 Windows | Bốn cây `8cee941`, `7693852`, `28ba133`, HEAD có cùng blob CI **2e21c0c1f0701e837f7c13fa20a55ab39fd5805c**. Với push/master thành công, điều kiện cho tập skip Ubuntu 11,23,28,39; Windows 11,21,22,28,36,39 | Có về thiết kế 4/6; quan sát 3 run **KHÔNG ĐO ĐƯỢC** |
| Các bước được dẫn | #11 PR-only; #22/#23 loại trừ; #38 LAND/#39 WORKER | Biểu thức `if` trong YAML khớp từng trường hợp | Có về mã, không phải runtime |
| #490 nay landed | cả ba vế ĐẠT; hai nền 0 failure | Merge/bookkeeping đọc được; CI và authority GitHub **KHÔNG ĐO ĐƯỢC** | Không tự chứng nhận landed |
| Bookkeeping không có tệp riêng | dùng r359, chủ kho đóng chuỗi | r359 ghi đúng quyết định ấy; xác thực người quyết định và trạng thái GitHub **KHÔNG ĐO ĐƯỢC** | Có văn bản nguồn |
| Nợ treo | “khoảng vài giờ”; rút ~7 giờ; bằng chứng từ 19:44:09Z | Không có mốc đọc CI; không lấy giờ commit làm giờ đọc. Khoảng thời gian thật **KHÔNG ĐO ĐƯỢC** | Đã hạ độ chính xác đúng |
| Câu r361 bị rút | “Nếu chỉ shellcheck hỏng thì không ai biết” | Câu cũ còn trong r361:395–399; r362 rút rõ. A/B dưới đây bác được câu đó | Có; giữ mục lịch sử không phải mâu thuẫn mới |
| A/B có shellcheck | actionlint DAT; shellcheck DAT; canary DAT, SC1003 rc=1 | PATH thử giữ các executable thật: đúng các giá trị; tổng DAT, CLI rc=0 | Có |
| A/B thiếu shellcheck | actionlint DAT; shellcheck KHONG_DO_DUOC; canary DO/blocking | Chỉ bỏ wrapper shellcheck khỏi PATH: đúng các giá trị; chi tiết SUY_GIAM, fixture rc=0; tổng DO, CLI rc=2 | Có |
| Chỉ chạy canary khi full scan | `chi is None` | Full scan có **1** canary; `--chi shellcheck` có **0** canary | Có |
| Một công cụ thiếu vẫn xanh | shellcheck thiếu, tổng DAT, canary=[] | Thiếu shellcheck + `--chi shellcheck`: đúng JSON, rc=0 | Có |
| Quyền chặn và ngoại lệ | blocking nâng tổng; advisory không nâng | Bỏ nhánh nâng tổng: canary DO nhưng tổng DAT/rc=0. Đổi chính sách advisory: cùng kết quả tổng, giữ canary DO | Có về cơ chế |
| Hai bước cài đơn và G5 | #7 shellcheck; #8 rg; #9 full không --chi | YAML gọi đúng hai tên; installer kết thúc bằng kiểm `--chi`; G5 gọi full scan rồi suite | Có về đường gọi |
| Lượt Windows hỏng giữa chừng | #7 xanh, #8 đỏ, #9 skipped | Cấu trúc workflow cho phép diễn biến đó; JSON/bước của lượt cụ thể **KHÔNG ĐO ĐƯỢC** | Không nâng thiết kế thành quan sát |
| Hai lần chạy bác lời r361 | 2 lần cong_cu.py | A/B full thực tế hai lần đã cho DAT→DO của canary và tổng; số lần tác giả cũ chạy **KHÔNG ĐO ĐƯỢC** | Tái hiện được cơ chế |
| Bài học “đã ghi ba lần” | 3 lần trong tệp | Không chỉ ra ba mục hoặc quy tắc đếm ngữ nghĩa; **KHÔNG ĐO ĐƯỢC** con số chính xác | Không xác nhận bằng đếm từ khóa |
| Xuất xứ #290, spec đóng băng | xuất xứ, không phải authority hiện hành | Spec revision **1**, cảnh báo đóng băng ở dòng 10; `59fe955` có thật và là tổ tiên HEAD; không suy Git merge thành landed GitHub | Có về nguồn cục bộ |
| Protocol/AGENTS | dòng 28/116/164; AGENTS 22–23; 20 mục | Đúng các dòng; mục thực §1, §3.1.1, §3.2; 20 mục chính | ĐÃ VÁ THẬT |
| Trang Issue cũ | 30 là cỡ trang, 0 khớp bị rút | Bản `25c2d5b` có lời khai cũ; bản hiện tại đã rút cách hiểu tổng; response trang cũ **KHÔNG ĐO ĐƯỢC** | Đúng cách ghi giới hạn |
| Các số Issue mới | 128 mở; total_count 101 | **KHÔNG ĐO ĐƯỢC** giá trị API; đã có nhãn THUẬT LẠI — search_issues, thiếu response thô | Nhãn đúng tại đoạn này |
| Tỷ lệ quét | ≈23%; 30/128 | **23,4375%**; hai đầu vào chưa được xác thực | Có về phép chia |
| Bốn Issue liên đới | #249, #295, #269, #297 | Danh sách có đúng **4** số khác nhau; nội dung, tình trạng và “khác cơ chế nên không trùng” **KHÔNG ĐO ĐƯỢC** từ API | Đã có nhãn; chỉ đếm được danh sách |
| t33 và write set | #249 nhắm lease_publish_test.py, nợ này nhắm cong_cu.py | Thân `t33_workflow_dang_lease_phai_qua_actionlint` kiểm actionlint, không đòi shellcheck; hai đường dẫn mã khác nhau. Việc Issue #249 thật sự giao write set ấy **KHÔNG ĐO ĐƯỢC** | Có về thân ca; không chứng nhận spec Issue |
| Phiên đang chạy | KHÔNG ĐO ĐƯỢC | Không có nguồn trạng thái phiên; truy vấn Issue không trả lời được | Nhãn đúng |
| Issue nhận nợ | đã mở #498 | **KHÔNG ĐO ĐƯỢC** việc mở/nội dung; CHANGELOG:138–139 có nhãn; chú thích mã:223 chưa có | Vá chưa phủ mọi chỗ |
| Verdict nhập kho | 28 955 byte, 161 dòng, a6bf4bea… | **28 955 byte; 161 dòng; a6bf4bea67c347385960285c5e5d0d28346887da684595b6429f22a6d67aed27** | Có, băm/đếm lại tệp thật |
| Neo đầu tiên | evidence_url ghim 8104480 | `git log --all --diff-filter=A` trả đúng **1 commit**, **8104480fe756978455abf1baf96adf6f9b399cbb**; commit chỉ thêm verdict; blob tại đó bằng tệp HEAD từng byte | Có; URL GitHub có truy cập được hay không **KHÔNG ĐO ĐƯỢC** |
| Neo là tổ tiên | canonical_ancestry | `git merge-base --is-ancestor 8104480 HEAD`: **rc=0**; reviewed SHA cũ e826730 có thật, đúng trong verdict và receipt | Có trong Git |
| Commit đầu thiếu hồ sơ kèm | t27 đỏ tại 8104480; commit sau đóng lại | Checkout **bản chép**: t27 tại 8104480 rc=1, lỗi đầu tiên là thiếu hàng mục lục; tại 52b36d1 rc=0 | Có; tại commit đầu cũng chưa có receipt |
| Mục lục và cảnh báo | 1 hàng mục lục + 1 hàng cảnh báo | Diff README thêm đúng **2** hàng, dòng 272 và 17; cùng verdict/receipt/caveat id | Có về cấu trúc |
| Severity lượt 1 | so_p1=0, so_p2=1, so_p3=1 | Đếm tiêu đề bắt đầu `### `, chứa nhãn severity tương ứng: **0/1/1**, hai finding. Mẫu Pn trong lệnh tài liệu tái lập được khi thay n lần lượt 1/2/3 | Có; không dùng phần tự tóm tắt |
| Hai bản vá trước được chấp nhận, một bị bác | 2 ĐÃ VÁ THẬT; 1 VÁ HỜ | Đúng ba gạch đầu dòng trong verdict lượt 1 | Có với hiện vật verdict |
| Tree reviewer lượt 1 khai | 67df2efa… bằng tree e826730 | `git rev-parse e826730^{tree}` = **67df2efa7e6f6c7b23bedfb43da647b395800a37** | Có về khớp định danh; không tự xác thực session đã đọc cây |
| Các ca đột biến lượt 1 | 13; 5/5 lời khai sống; t13 0→1 | Bảng đột biến verdict có **13 hàng**. Lượt này chạy lại đủ 5 kiểu lời khai và t13: đúng kết quả; toàn bộ lịch sử thực thi lượt 1 vẫn là báo cáo reviewer | Có về nội dung bảng và phần đã chạy lại |
| Số hàng KHÔNG ĐO ĐƯỢC | receipt/README: 17 hàng cho GitHub | Đếm literal trong bảng chính được **28 hàng**. Nhóm riêng “17 phía GitHub” không có danh sách/rule phân loại để tái lập; xem finding riêng | Chưa đủ nguồn cho số 17 |
| Danh tính model lượt 1 | receipt: yêu cầu gpt-6-astra; đã chạy KHONG_DO_DUOC | Đúng hai scalar trong receipt; không có log model backend. README bỏ chữ “yêu cầu” khi ghi gpt-6-astra | Mục lục khai rộng hơn receipt |
| Runtime lượt 1 | run 93f5036f…; 878,149 s; rc=0; xong; chết 1 lần, lần hai xong | **KHÔNG ĐO ĐƯỢC** runtime. Hiệu hai timestamp được kể là **878,14888 s**, làm tròn đúng 878,149 s / 878 s | Phép tính đúng; runtime là ATTESTATION |
| Prompt/stdout/stderr lượt 1 | prompt fd117770…; stdout 297 byte/897a4fec…; stderr 396316 byte/5b23cba8… | **KHÔNG ĐO ĐƯỢC**: thiếu ba hiện vật và run.json tương ứng. Tìm prompt digest trong HEAD chỉ ra chính receipt | Không có ngoại lệ “prompt đối chiếu được” |
| Lượt chết và probe | lỗi 111; một lượt chết; probe rc=0, 0 lỗi; record dang_chay/null | **KHÔNG ĐO ĐƯỢC**: không log/probe/run.json của các run này; mã launcher không chứng minh một phiên cụ thể đã xảy ra như kể | Receipt gọi ATTESTATION nhưng CHANGELOG §3 gọi NỢ ĐÃ ĐO |
| Tuân thủ và người vận chuyển lượt 1 | cây sạch=true; 0 commit thêm; ducthangho là tác giả/người vận chuyển | **KHÔNG ĐO ĐƯỢC** runtime/authority lịch sử; hash verdict không chứng minh các scalar này | Giữ đúng nhãn attestation |
| Nguyên nhân không chạy ls-remote lượt 1 | “reviewer tin câu origin trỏ mirror” | Verdict:157 ghi đã đo cấu hình thật ra URL GitHub, **vì vậy** không chạy ls-remote; verdict chủ động giới hạn phép so là hai tập cục bộ | **Không khớp nguồn được nhập** |
| Phạm vi kết luận về cổng ngữ nghĩa | “Không cổng nào trong kho” | Năm mutant lời khai được đối chiếu bằng **hai cổng** doc-claims và release-verify; không có phép quét mọi cổng theo từng mutant | **Rộng hơn phép thử** |
| Số mục manifest | 180→180; thêm/bớt 0; ops có 0 mục | Tập đường dẫn bằng nhau; tự kiểm đủ **180** size/hash, **0 lệch**; **0** đường dẫn ops | Có |
| Byte và hash gói | manifest HEAD khai 8.128.797 byte; 0e38cde3… | Tự cộng **8.128.797**; base **8.110.218**, tăng **18.579**. Hash xác minh **0e38cde3fd871e649ad5ccd55efa5fc7946ef0e5cfaf935ff257bd3bcae75a67** | Có |
| Chỉ CHANGELOG ảnh hưởng gói | ops không được đóng gói | Chỉ một entry đổi: CHANGELOG **815.896→834.475** byte; SHA-256 hiện tại **8ef33612b58cd493a3e52ffb8a44c38bea5a7643a8815ced18d2c60538113452** | Có |
| Merge master giữa vòng | 28ba133→0721811; 3 tệp; giao write set rỗng | `0721811` có cha 28ba133; `1e75335` có hai cha **52b36d1 + 0721811**. Master đổi đúng workflow thu hồi, lease_publish.py, lease_publish_test.py; giao với 6 tệp PR = **0** | Có trong Git |
| Suite trước merge | 121/121 | Trên bản chép checkout **52b36d1**, chạy suite thật: **rc=0; 121/121; đã chạy=121; bỏ qua=0** | Có; không lấy số đăng ký ca thay cho chạy |
| Suite sau merge | 146/146; đã chạy 146; bỏ qua 0 | `python3 ops/lease_publish_test.py`: **rc=0; 146/146; đã chạy=146; bỏ qua=0** | Có |
| Biên nhận v2 | 49 ĐẠT; 11/11 legacy; 42 nợ; 0 vi phạm; 0 không đo; tổng 102 | `python3 ops/bien_nhan_v2.py --root .`: **rc=0**, đúng cả bảy số, **TỔNG: ĐẠT**; 49+11+42=102 | Có |
| Suite biên nhận | 48/48; 63/63 mutant; 2/2 tự kiểm | `python3 ops/bien_nhan_v2_test.py`: **rc=0**, đúng ba cặp, TỔNG: ĐẠT | Có |
| Full G5 | tổng DAT; canary DAT | `python3 ops/cong_cu.py kiem-tra --json`: **rc=0**, tổng DAT; actionlint_shellcheck DAT | Có |
| Suite công cụ | ca=23; đột biến=18; lỗi đột biến=0 | `python3 ops/cong_cu_test.py`: **rc=0**, đúng **23/18/0** | Có |
| Release verify | expected=checked=180; ok=true; không extra | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: **rc=0, ok=true**, 180/180, failed=[], extra_files=[] | Có |
| Golden | rc=0; ok=true | `python3 scripts/tl.py golden-test --json`: **rc=0, ok=true; 20 ca**, không mismatch | Có |
| Determinism | rc=0; ok=true | `python3 scripts/tl.py determinism-audit --strict --json`: **rc=0, ok=true; 15 kiểm tra đạt** | Có |
| Doc claims | rc=0; ok=true | `python3 scripts/tl.py doc-claims-check --strict --json`: **rc=0, ok=true; 106 tệp; flags=[]**. Có **367 advisory**, không phải “không có điều gì cần xem” | Có với điều PR thực sự khai |
| Workflow audit | rc=0 | `python3 scripts/tl.py workflow-audit --strict --json`: **rc=0, ok=true**, errors=[], warnings=[] | Có |
| Doctrine | rc=0 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **rc=0; 7 tệp; 0 chỗ chép doctrine** | Có |
| ADR sống | rc=0 | `python3 .claude/dev/packet_loop.py adr-song --root .`: **rc=0; 46 ADR = 46 dòng §20**, giữ ngoại lệ 0016 | Có |
| Số cổng được báo so CI | EVIDENCE 12 lệnh; CI 31 bước cổng | Đúng **12** lệnh trong EVIDENCE, đã chạy đủ. YAML **40 = 8 setup + 31 cổng + 1 upload**. Khối số đo r362 liệt kê 10 lệnh; hai lệnh còn lại ở EVIDENCE | Có; không phải chạy đủ CI |
| Phiên bản môi trường | actionlint 1.7.7; shellcheck 0.9.0; jsonschema 4.26.0 | Probe thật trả đúng cả ba. PyYAML tại đây 6.0.1; CI cài 6.0.3 | Có cho ba bản đã khai, không nhận môi trường hoàn toàn bằng CI |
| Ba phiên bản “CI ghim” | cả ba bản trên được ghim | actionlint và jsonschema có pin; **shellcheck ban_ghim=null**, lệnh cài các nền không chỉ định 0.9.0 | **Không — sai cả EVIDENCE và r362** |
| Khác số G5 so lượt 1 | do nền thiếu jsonschema; không phải mã đổi | cong_cu.py chỉ đổi comment, AST không đổi; cong_cu_test.py và cong_cu.yaml không đổi từ e826730. Nền hiện tại có 4.26.0 và suite đạt; việc thiếu gói trong phiên cũ **KHÔNG ĐO ĐƯỢC** độc lập | Phù hợp hồ sơ; không xác thực runtime cũ |
| CI exact HEAD chưa chạy theo yêu cầu chủ kho | cố ý chưa đốt CI | **KHÔNG ĐO ĐƯỢC** trạng thái/quyết định GitHub. Không chạy mạng và không yêu cầu chạy CI mới | Không xem là cổng đỏ |

**Đột biến và thử sửa — đã chạy, mỗi ca được trả về nội dung gốc trước ca tiếp theo:**

Lệnh gọi riêng hai chốt hồ sơ trên bản chép:

```sh
python3 -c "import sys; sys.path.insert(0, 'ops'); import lease_publish_test as t; t.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()"
python3 -c "import sys; sys.path.insert(0, 'ops'); import lease_publish_test as t; t.t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()"
python3 -c "import sys; sys.path.insert(0, 'ops'); import cong_cu_test as t; t.t13_actionlint_bien_mat_giua_probe_va_canary()"
```

| khẳng định/ca | PR khai hoặc đối chứng | đo được | khớp/răng? |
|---|---|---|---|
| t27 với hồ sơ nguyên vẹn | xanh | rc=0 | Có |
| Bỏ receipt mới | hồ sơ phải thiếu mảnh | t27 **rc=1**, chỉ đúng receipt thiếu | Có răng |
| Bỏ hàng mục lục mới | t27 đòi hàng | t27 **rc=1**, thiếu verdict trong cột mục lục | Có răng |
| Bỏ hàng cảnh báo mới | t27 đòi hàng | t27 **rc=1**, caveat không có đúng hàng/cột | Có răng |
| Bỏ chính verdict mới | hỏi t27 có cưỡng chế đủ ba mảnh một mình không | **t27 vẫn rc=0**; **t26 rc=1**, “trỏ vào tệp không có” | t27 một mình không đủ; cặp t26+t27 bắt được cả hồ sơ. Không gọi sự sống sót ở t27 là cả suite bỏ lọt |
| Đổi một chữ số digest receipt | băm neo phải khớp blob | bien_nhan_v2 **rc=1; 1 vi phạm; TỔNG: ĐỎ** | Có răng |
| verdict_bytes 28955→28956 | thử mức kiểm scalar | bien_nhan_v2 **vẫn rc=0; 49 ĐẠT; 0 vi phạm** | Không kiểm scalar này; số hiện tại được reviewer tự đếm và đúng. Không yêu cầu mở rộng validator trong PR này |
| Thiếu shellcheck, full scan | canary blocking | tổng DAT/rc=0 → **DO/rc=2**, actionlint vẫn DAT | Có răng với suy giảm thật |
| Thiếu shellcheck, --chi shellcheck | nhánh giới hạn đã mô tả | tổng **DAT/rc=0**, shellcheck KHONG_DO_DUOC, canary=[] | Tái hiện đúng lời r362 |
| Đổi điều kiện chạy canary từ `if chi is None` thành `if False` | t13 phải phát hiện mất chốt | t13 **rc=0→1**, “canary mất executable bị nuốt” | Có răng |
| Cùng đột biến, full scan thiếu shellcheck | đo hậu quả trực tiếp | tổng DO/rc=2 → **DAT/rc=0**, canary=[] | Mất chặn thật |
| Bỏ nhánh nâng tổng cho canary DO | canary có kết quả chưa đủ | canary vẫn DO, tổng **DAT/rc=0** | Chứng minh vai trò tổng hợp |
| Đổi blocking thành advisory | ngoại lệ có chủ ý | canary DO, tổng **DAT/rc=0** | Khớp ngoại lệ đã mô tả |
| Đổi 128→129, giữ manifest cũ | toàn vẹn byte | release-verify **rc=2, ok=false** | Có răng với hash |
| Đổi 128→129, tái sinh manifest | kiểm nghĩa lời khai | doc-claims **rc=0**, release-verify **rc=0** | Sống |
| Đổi 37 success→36, giữ 4 skipped và tổng 41 | mâu thuẫn phép cộng | hai cổng trên **rc=0/0** sau tái sinh manifest | Sống |
| Đổi cha thứ nhất merge thành cha thứ hai | dùng SHA thật nhưng quan hệ sai | hai cổng **rc=0/0** | Sống |
| Đổi “xuất xứ” #290 lại thành “chủ” | sai nghĩa thẩm quyền | hai cổng **rc=0/0** | Sống |
| Đổi mù 1→0 trong lời khai lịch sử | sai số kể | hai cổng **rc=0/0** | Sống |
| Thử sửa nguồn/diễn đạt trong báo cáo mới | chỉ sửa bản chép; không đổi verdict neo băm | doc-claims, bien_nhan_v2, t27, release-manifest, release-verify đều **rc=0**; validator vẫn 49/102; release-verify ok=true | Bản sửa khả thi về cổng; không tự chứng minh nghĩa bằng rc |

Mỗi mutant lời khai dùng `python3 scripts/tl.py doc-claims-check --strict --json`, rồi `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json`, rồi `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`. **5/5 sống** là kết quả của hai cổng trên năm đầu vào này. Không yêu cầu xây cổng ngữ nghĩa mới.

### hai-loi-khai-thieu-nhan-va-sai-co-trang  [P2]  Nhãn Issue đã vá nhưng số ref GitHub lịch sử vẫn đứng như phép đo tại chỗ

TỆP/DÒNG: `cay-kho/CHANGELOG.md:7–22`, `:216–234`; `cay-kho/ops/cong_cu.py:223`; đối chiếu finding lượt 1 trong `ops/reviews/pr497-review-1-codex-verdict.md:130–140`.

VẤN ĐỀ: Giữ “mọi số Git” trong hạng tự đo được làm mất ranh giới giữa Git object hiện có và ref máy chủ ở một thời điểm quá khứ. Cả 320/320/MÙ 1 cũ và 322/321/MÙ 2/THỪA 1 mới chưa được dán nhãn tại chỗ. Gói chỉ có một tệp được thuật lại là máy chủ, không có bộ đệm trước fetch. Nhãn 128/101/bốn Issue/#498 trong đoạn đính chính không phủ các đoạn này; chú thích mã cũng còn khẳng định đã mở #498. Đây chính là phần số ref lịch sử finding lượt 1 đã chỉ ra, không phải mở rộng slug sang một yêu cầu mới. Không kết luận các số lịch sử chắc chắn sai.

ĐÃ THỬ VÁ: có — trên bản chép, tách Git object khỏi ref lịch sử trong giới hạn nguồn; thêm THUẬT LẠI trước cả hai phép canh; khai thiếu snapshot bộ đệm; thêm nhãn cho #498 trong chú thích. Giữ nguyên số được thuật lại, không thay bằng số snapshot mới.

ĐÃ THỬ NGHIỆM: REF cho 324/324 cục bộ, raw 322, thiếu raw→mirror 0/thừa 2; không tái lập được tập 321 trước fetch. Mutant mù 1→0 sống qua doc-claims và release-verify sau tái sinh manifest. Bản sửa nhãn: các cổng thử sửa ghi trên đều rc=0.

ĐỘ TIN: cao.

### attestation-runtime-bi-nang-thanh-phep-do  [P2]  Biên nhận tự tạo ngoại lệ cho prompt và bản tóm tắt nâng quá mức nguồn runtime

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml:11–13`, `:92–129`; `cay-kho/ops/reviews/README.md:272`; `cay-kho/CHANGELOG.md:187–193`.

VẤN ĐỀ: Receipt khai toàn bộ model_reviewer_identity là ATTESTATION vì run.json ngoài kho, nhưng ngay sau đó nói “Riêng prompt_sha256 thì đối chiếu được” và kết luận hai lượt chạy cùng prompt. Trong kho chỉ có **một digest được chép vào receipt**, không có hai prompt/run.json để đối chiếu. README còn ghi `gpt-6-astra` như danh tính lượt chạy, trong khi receipt chỉ biết **model yêu cầu** và để model đã chạy là KHONG_DO_DUOC. CHANGELOG §3 chuyển các scalar về một lượt chết, probe rc=0/0 lỗi, record dang_chay/null thành “NỢ ĐÃ ĐO” mà không mang nhãn ATTESTATION của nguồn. Nhãn runtime ở cuối hàng README không sửa được việc đổi model yêu cầu thành model đã chạy, cũng không phủ đoạn CHANGELOG. Khớp tree OID chỉ xác nhận định danh trong verdict nhất quán với Git, không độc lập xác thực session/runtime.

ĐÃ THỬ VÁ: có — giữ prompt cũng là ATTESTATION; ghi model yêu cầu và model đã chạy chưa đo được ngay trong hàng mục lục; thêm nhãn và sự vắng mặt hiện vật trước đoạn NỢ trong CHANGELOG. Không yêu cầu nhập transcript, chạy lại model hay công bố runtime riêng tư.

ĐÃ THỬ NGHIỆM: `git -C cay-kho grep -l fd117770fa4c651aad6194d4dfb9adfc51b60ba78a3a9ea4928823799c480c85 HEAD -- .` chỉ trả chính receipt. Đối chiếu YAML xác nhận `model_yeu_cau=gpt-6-astra`, `model_da_chay=KHONG_DO_DUOC`. Hiệu hai timestamp chỉ kiểm được phép tính 878,14888 giây, không xác thực mốc. Bản sửa qua bien_nhan_v2 và t27 rc=0, cùng doc-claims/release-verify rc=0.

ĐỘ TIN: cao.

### so-hang-github-khong-co-quy-tac-dem  [P2]  Số 17 hàng không có tập hàng hoặc phép phân loại để tái lập

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml:87–90`; `cay-kho/ops/reviews/README.md:272`.

VẤN ĐỀ: Hồ sơ mới gán số chính xác **17** cho những hàng bảng đo mang nhãn KHÔNG ĐO ĐƯỢC “cho phía GitHub”, nhưng không ghi tiêu chí hoặc danh sách 17 hàng. Đếm nguyên văn nhãn trong bảng chính được **28**, không phải 17. Ngay một tập chỉ lấy các hàng rõ về PR/Issue/CI/authority/phiên đã có **21** dòng: 31, 37, 42–50, 52–53, 65, 68, 70–71, 73–76 của verdict. Tập này chưa lấy ba hàng ref lịch sử 32–34, hàng thời gian treo nợ 54, hoặc ba hàng giới hạn khác 66/67/94. Không thể suy lại tác giả đã loại những hàng nào để ra 17. Đây là số đếm chưa đủ nguồn, **không phải khẳng định mọi cách phân nhóm hợp lý đều bắt buộc cho 28**.

ĐÃ THỬ VÁ: có — trên bản chép đổi sang khẳng định cơ học kiểm được: “28 hàng chứa nguyên văn nhãn KHÔNG ĐO ĐƯỢC, gồm cả giới hạn ngoài GitHub”, tại receipt và mục lục. Nếu muốn giữ nhóm GitHub hẹp, cách sửa khác là cung cấp tập hàng và quy tắc chọn thay vì mặc nhiên giữ 17.

ĐÃ THỬ NGHIỆM: chạy phép đếm dưới đây trên verdict nguyên bản, kết quả **28**; bản sửa receipt/README qua bien_nhan_v2 và t27 rc=0.

```sh
python3 - <<'PY'
from pathlib import Path
s = Path('cay-kho/ops/reviews/pr497-review-1-codex-verdict.md').read_text()
s = s.split('## BẢNG ĐO', 1)[1].split('**Đột biến và phép thử', 1)[0]
print(sum(line.startswith('|') and 'KHÔNG ĐO ĐƯỢC' in line for line in s.splitlines()))
PY
```

ĐỘ TIN: vừa — số 28 và sự thiếu quy tắc là chắc; ranh giới nhóm ngữ nghĩa “phía GitHub” chưa được tác giả định nghĩa.

### ke-sai-ly-do-reviewer-khong-chay-ls-remote  [P2]  Cảnh báo mới kể ngược lý do được ghi trong verdict gốc

TỆP/DÒNG: `EVIDENCE.md:3–6`; `cay-kho/CHANGELOG.md:178–185`; `cay-kho/ops/reviews/pr497-review-1-codex-verdict.receipt.yaml:175–181`; `cay-kho/ops/reviews/README.md:17`. Nguồn đối chiếu: verdict lượt 1 dòng 19 và 157.

VẤN ĐỀ: Các bản tóm tắt nói reviewer **tin câu origin trỏ mirror**, rồi kết luận ls-remote đi ra mạng nên không chạy. Chính verdict được nhập nói đã đo `git config --local --get remote.origin.url` ra **URL GitHub**, “Vì vậy không chạy ls-remote origin”. Nó còn tự ghi phép so chỉ gồm hai tập cục bộ, không phải hỏi máy chủ. Kết luận giới hạn 321/321 của cảnh báo là đúng; phần kể reviewer tin cấu hình sai và bị câu ấy chặn đường không đúng với nguồn mà cảnh báo đang tóm tắt. Origin trỏ mirror cũng không dẫn tới kết luận phải ra mạng. Việc chỉ sửa URL trong EVIDENCE chưa sửa câu giải thích này.

ĐÃ THỬ VÁ: có — trên các bản chép, đổi thành “theo verdict, reviewer đo cấu hình thực tế là URL GitHub, vì vậy không chạy ls-remote trong sandbox không mạng”; giữ cảnh báo 321/321 chỉ là hai tập cục bộ. Không sửa verdict đã neo băm.

ĐÃ THỬ NGHIỆM: đọc lại nguồn verdict:19/157 và so với bốn nơi kể; đây là đối chiếu **nội dung hiện vật**, không tự chứng nhận trạng thái tâm trí hoặc runtime phiên cũ. Bản sửa trong cây chép qua doc-claims, bien_nhan_v2, t27, release-verify rc=0; EVIDENCE sửa trên bản riêng trong sandbox.

ĐỘ TIN: cao.

### evidence-dem-thieu-ref-giao-head  [P2]  EVIDENCE khai 323 nhánh nhưng gói thực có 324

TỆP/DÒNG: `EVIDENCE.md:19`, `:40–42`; liên hệ `cay-kho/CHANGELOG.md:231–233`.

VẤN ĐỀ: Dòng cấu hình hiện tại có lệnh cụ thể nhưng kết quả sai: mirror có **324**, không phải 323. `pr497-head` được đưa vào gói cùng nhánh PR còn ở e826730; nó là một ref thật trỏ 1d58500, không phải alias HEAD. Vì thế quét toàn bộ gói cho r362 ra **2**, không phải 1. Loại riêng ref giao head mới thu được 323/1. Không được lặng lẽ lọc ref này để làm khớp lời khai. Điều này **không bác số 323 của một snapshot lịch sử phía điều phối**; nó bác mô tả hiện trạng gói và sự thiếu phân biệt hai tập. Đây là lỗi gói review theo yêu cầu người giao, không phải thay đổi ref trên GitHub do PR gây ra.

ĐÃ THỬ VÁ: có — trên bản chép EVIDENCE, sửa số hiện tại thành 324 và nêu riêng ref giao exact head ngoài tập 323 được thuật lại. Không xóa ref, không sửa mirror/cay-kho, không thay số lịch sử r362 bằng số mới.

ĐÃ THỬ NGHIỆM: `git -C kho.git for-each-ref --format='%(refname)' refs/heads | wc -l` → **324**; `git -C cay-kho ls-remote --heads origin | wc -l` → **324**, cả hai rc=0. REF so tập và quét tiêu đề cho đúng các tên/OID trong BẢNG ĐO; bộ đệm 325 kể HEAD/324 bỏ HEAD; r363 vẫn đúng 1 ở land-492-bookkeeping. Tệp thô 322 dòng khớp băm, mirror thừa pr487-merge và pr497-head.

ĐỘ TIN: cao.

### khai-shellcheck-duoc-ci-ghim-khi-khong-co-pin  [P2]  Phiên bản shellcheck đo tại sandbox bị khai thành pin của CI

TỆP/DÒNG: `EVIDENCE.md:61–64`; `cay-kho/CHANGELOG.md:235–238`. Đối chiếu `.github/workflows/ci.yml:92–104`, `ops/cong_cu.yaml:68–79`.

VẤN ĐỀ: Cả hai nơi nói actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0 là “đúng ba bản CI ghim”. Hai công cụ đầu/cuối có pin, nhưng shellcheck có `ban_ghim: null`; công thức apt/brew/choco không chỉ định 0.9.0. Probe tại sandbox thật sự trả shellcheck 0.9.0, song đó là **phiên bản đã thấy**, không phải phiên bản CI cưỡng chế. Câu này làm điều kiện tái lập môi trường mạnh hơn cấu hình thực. Không đòi đổi chính sách cài của CI trong PR hồ sơ này.

ĐÃ THỬ VÁ: có — trên bản chép đổi thành “actionlint và jsonschema được ghim; shellcheck 0.9.0 là bản đo tại môi trường này, CI không ghim shellcheck”.

ĐÃ THỬ NGHIỆM: `actionlint -version` → 1.7.7; `shellcheck --version` → 0.9.0; probe importlib.metadata của jsonschema → 4.26.0. Parse YAML trả shellcheck ban_ghim=null và đọc đủ ba công thức cài; G5 trên cây thật rc=0 nhưng không chứng nhận có pin. Bản sửa lời khai qua doc-claims và release-verify rc=0.

ĐỘ TIN: cao.

### hai-cong-duoc-khai-thanh-moi-cong-trong-kho  [P2]  Kết luận về mọi cổng vượt phạm vi năm phép thử trên hai cổng

TỆP/DÒNG: `cay-kho/CHANGELOG.md:169–176`; nguồn được thuật lại: bảng đột biến trong verdict lượt 1 dòng 100–113.

VẤN ĐỀ: Dữ liệu cho thấy năm đột biến văn xuôi sống qua doc-claims và release-verify sau tái sinh manifest. Câu tiếp theo đổi phạm vi thành **“Không cổng nào trong kho canh được nghĩa của những câu ấy”**. Verdict không cung cấp phép chạy mọi cổng trên năm mutant, và số 12 lệnh xanh ở cây nguyên vẹn cũng không bổ sung phép đo đó. Không cần tìm một cổng khác bắt được mutant mới thấy bước suy rộng này chưa có bằng chứng; hai cổng được thử không đại diện mặc nhiên cho mọi cổng.

ĐÃ THỬ VÁ: có — trên bản chép đổi thành “Hai cổng vừa nêu không phát hiện năm đột biến lời khai trong phép thử này”. Giữ bài học review độc lập và giữ nguyên giới hạn; **không đề nghị xây cổng ngữ nghĩa mới**.

ĐÃ THỬ NGHIỆM: chạy lại đủ năm mutant Issue/số bước/cha merge/thẩm quyền/mù ref: doc-claims và release-verify đều rc=0 sau tái sinh manifest, **5/5 sống**. Mutant Issue với manifest cũ làm verify rc=2, xác nhận phép thử có thay đổi byte thật. Bản sửa phạm vi kết luận qua doc-claims và release-verify rc=0.

ĐỘ TIN: cao.

## GIỚI HẠN

- Không mạng; không đo trực tiếp PR/Issue, Actions run/job/attempt, quyền người duyệt, landed, phiên đang chạy, hay CI trên exact HEAD. `ls-remote origin` chỉ hỏi mirror trong sandbox. Tệp `ls-remote-may-chu.txt` xác minh được byte/số học, xuất xứ và timestamp vẫn là ATTESTATION. Thiếu snapshot bộ đệm trước fetch; không dựng tập theo lời kể rồi gọi nó là snapshot đã đo.
- Không có run.json, prompt, stdout/stderr của hai lần phóng reviewer được receipt này kể. Các run.json của hồ sơ khác trong kho không xác thực phiên #497. Tính hiệu hai mốc được thuật lại và khớp một tree/hash không nâng danh tính/runtime thành phép đo độc lập.
- Đã chạy đủ 12 lệnh EVIDENCE, thêm ca riêng và suite tại cây trước merge; chưa chạy toàn bộ 31 bước CI, chưa chạy Windows. Kết quả hiện tại không chứng nhận một run GitHub, không đòi đốt CI trong vòng review.
- Không tự soạn nội dung tấn công. Chỉ chạy suite/fixture sẵn trong cây và tự đột biến số, chữ mô tả, trạng thái chính sách, điều kiện canary, sự có mặt của hiện vật. Các hướng cần dữ liệu thoát/đồng tự/đường dẫn vượt cây không được bổ sung.
- Các bản thử sửa chỉ nằm trên bản chép trong sandbox, không phải bản vá đã áp lên PR. Độ đúng của prose được đối chiếu bằng nguồn và giới hạn phép đo; cổng xanh sau thử sửa chỉ xác nhận các chốt được chạy vẫn đạt.
- Chỉ giữ một sản phẩm mới là `VERDICT.md` tại gốc sandbox; dữ liệu tạm và bản chép được dọn cuối lượt. Kiểm cuối: `git -C cay-kho status --porcelain` **rc=0, stdout rỗng**; HEAD vẫn **1d58500b2ecaf7ccd38dcc6f8ad9bf0dbf13c77e**. Không sửa cây được review hoặc mirror.
