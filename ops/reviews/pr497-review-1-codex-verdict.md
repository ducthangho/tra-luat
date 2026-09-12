verdict: changes_requested
reviewed_sha: e82673014baefca23b50663cecad80fdbde79b3b

Review độc lập bằng Codex/GPT-6, provider OpenAI, execution surface API với công cụ shell tại sandbox, transport trực tiếp trong phiên này. Không dùng connector GitHub. Tree đã đo: `67df2efa7e6f6c7b23bedfb43da647b395800a37`. Kết luận có **1 P2 còn tồn tại và 1 P3**; không phát hiện hồi quy runtime trong thay đổi chỉ thêm chú thích.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `chu-packet-sai-tham-quyen`: **ĐÃ VÁ THẬT** — `CHANGELOG.md:110–117` và `ops/cong_cu.py:219–223` đã đổi sang xuất xứ và yêu cầu packet kế nhiệm/corrective được cấp thẩm quyền. Spec có cảnh báo đóng băng ở dòng 10; `git show -s --format='%h %s' 59fe955` xác nhận merge PR #291 của packet #290, và `git merge-base --is-ancestor 59fe955 HEAD` trả 0. Nội dung ba trích dẫn đúng tại **dòng** 28, 116–117, 164–165 của protocol; ký hiệu `§` là lỗi dẫn chiếu nhỏ, ghi riêng P3 bên dưới. Đột biến đổi lại “xuất xứ” thành “chủ” trên bản chép vẫn qua doc-claims và doctrine-scan: bản vá văn bản đúng, nhưng hai cổng ấy không bảo vệ nghĩa này. Không dùng Git merge để tự chứng nhận trạng thái `landed` trên GitHub.
- `quet-so-hieu-r-doc-bo-dem-cuc-bo`: **ĐÃ VÁ THẬT** — phương pháp đã phân biệt máy chủ/bộ đệm và dùng hiệu tập, đúng `CLAUDE.md:217–236`. Tái đo snapshot: 322 remote-tracking refs, loại alias `HEAD` còn **321 nhánh**; mirror có **321 heads**, thiếu 0/thừa 0. Quét tiêu đề CHANGELOG trên toàn bộ tập ấy: `r362` ở đúng một nhánh `claude/handoff-tra-luat-repo-2ak5th`; nhánh Windows được nêu có đầu tệp `r356`. Đối chứng thay một phần tử của tập bộ đệm: hai lực lượng vẫn 321, nhưng hiệu tập tìm đúng một nhánh mù; phép so số đếm vẫn cho qua. Các số lịch sử **320/320, mù 1 rồi 0** là **KHÔNG ĐO ĐƯỢC** từ snapshot này, không được coi là đã tái xác nhận GitHub. Đột biến lời khai mù 1 thành 0 vẫn qua doc-claims.
- `hai-loi-khai-thieu-nhan-va-sai-co-trang`: **VÁ HỜ** — đã phân biệt cỡ trang/tổng và đã đổi lời khai về phiên sang `KHÔNG ĐO ĐƯỢC`. Tuy nhiên, các số mới **128**, **101**, **bốn Issue** và việc mở **#498** vẫn không mang nhãn thuật lại tại chỗ (`CHANGELOG.md:122–131`), trái chính lời hứa ở dòng 120. `30/128 × 100 = 23,4375%` khớp phép tính, không xác minh được hai đầu vào GitHub. Đổi 128 thành 129 trên bản chép: `doc-claims-check --strict --json` vẫn `rc=0`, 106 tệp, không cờ; tái sinh manifest rồi release-verify cũng `rc=0`. Finding P2 bên dưới giữ nguyên slug này.

## BẢNG ĐO

Mọi lệnh cổng nền dưới đây đã chạy trong `cay-kho/`; phép sửa, dựng fixture, checkout nền và đột biến chạy trên bản chép tạm nằm trong sandbox. Đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` vào thư mục tạm trong sandbox và dùng cấu hình Git global rỗng trong sandbox. Không gọi mạng, không fetch. “Khớp” đối với phép tính chỉ xác nhận phép tính; không xác nhận đầu vào thuật lại.

Các phép đo dùng để đọc bảng:

- **GIT**: `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git rev-parse --is-shallow-repository`, `git config --get core.abbrev`; `git diff --no-ext-diff HEAD~2 HEAD`; `git show`, `git merge-base --is-ancestor` tại các SHA ghi trong hàng tương ứng.
- **REF**: `git -C cay-kho for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin`; bỏ đúng `HEAD`. So tập tên với `git -C kho.git for-each-ref --format='%(refname:lstrip=2)' refs/heads`. Đọc `CHANGELOG.md` từ từng ref bằng Git, đếm **tiêu đề mục**, không đếm mọi lần nhắc số r. Đây là hai tập **cục bộ**, không phải phép hỏi máy chủ.
- **CI-TĨNH**: đọc và parse `.github/workflows/ci.yml` bằng PyYAML tại `8cee941`, `7693852`, `28ba133` và HEAD. Cả bốn có cùng blob `2e21c0c1f0701e837f7c13fa20a55ab39fd5805c`. Kiểm từng điều kiện theo trường hợp push/master, job thành công; không giả làm response Actions.
- **CÔNG-CỤ**: `python3 ops/cong_cu.py kiem-tra --json` và `python3 ops/cong_cu.py kiem-tra --chi shellcheck --json`. Với phép A/B, dựng PATH riêng trong sandbox bằng wrapper gọi các executable đã có; chỉ thêm/bỏ mục shellcheck trong PATH, không sửa fixture hay mã gốc. Không cài gói hoặc sao chép dữ liệu từ ngoài sandbox.
- **GÓI**: `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`; đồng thời tự đọc từng tệp được manifest liệt kê, tính lại kích thước và SHA-256 bằng Python. So cả ba manifest tại base `28ba133`, head cũ `25c2d5b`, head mới `e826730`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head, lịch sử, viết tắt | `e826730`; clone đầy đủ; abbrev 7 | GIT: SHA đầy đủ đúng dòng đầu báo cáo; shallow=false; abbrev=7; detached | Có |
| Phạm vi PR | 132 dòng CHANGELOG; 15 dòng chú thích; manifest 5 thêm/5 bớt | Diff Git khớp **từng byte** `diff.patch`; numstat đúng cả ba tệp | Có |
| Hai việc ở r362 | đóng nợ #490; rút lời khai shellcheck | Có đủ hai phần §1 và §2; đối chiếu r359/r361 bên dưới | Có về nội dung |
| Ngày r362 | 2026-09-10 | Commit đầu 03:43:16Z, bản vá 04:54:24Z cùng ngày | Có về ngày Git |
| VERSION và xuất xứ r336 | không nâng; `1.36.68` từ r336 | VERSION hiện tại và `git show 3dcdc6a:VERSION` cùng 1.36.68; diff VERSION rỗng | Có |
| Số r360 đã có ở nhánh khác | 1 mục r360, chưa merge | REF: đúng một nhánh `claude/pr491-land-va-findings-wip`, đầu tệp r360; trạng thái PR/phiên trên GitHub **KHÔNG ĐO ĐƯỢC** | Một phần |
| Lịch sử canh hai nguồn | 320 heads máy chủ, 320 nhánh đệm | **KHÔNG ĐO ĐƯỢC** ở thời điểm kể lại; hiện tại mirror=321, đệm=321 sau loại HEAD | Không cùng snapshot |
| Nhánh mù trước fetch | 1: `codex/wp484-g3-windows` | **KHÔNG ĐO ĐƯỢC** trạng thái trước fetch, không có snapshot thô; ref ấy hiện có | Chưa xác minh |
| Sau fetch | mù=0, quét 320 nhánh | Snapshot hiện tại thiếu=0/thừa=0 trên 321/321; lịch sử 320 và thao tác fetch **KHÔNG ĐO ĐƯỢC** | Một phần |
| Không va chạm r362 | chỉ trên nhánh PR này | REF: đúng **1 nhánh thật** có tiêu đề r362. `origin/HEAD` trỏ chính nhánh đó, không đếm thành nhánh thứ hai | Có trong snapshot |
| Nội dung nhánh từng mù | đầu tệp r356 | `git show refs/remotes/origin/codex/wp484-g3-windows:CHANGELOG.md`: tiêu đề đầu là r356 | Có trong snapshot |
| Ba P2 ở lượt trước; hai đính chính sau phần ref | tổng 3, phần cuối P2 ×2 | Diff `25c2d5b..e826730` có ba nhóm sửa; số finding thật trên GitHub **KHÔNG ĐO ĐƯỢC**; danh sách được người giao review cung cấp | Có cấu trúc; chưa xác minh GitHub |
| Ba vế ADR-0034 | merged, hậu-merge gate, bookkeeping | ADR-0034 nêu vào canonical + hậu-merge gate + bookkeeping; định nghĩa trong CONTEXT tương ứng | Có |
| Merge #490 và hai cha | `8cee941`: `00e017a` + `01e7f77` | `git show -s --format='%H %P' 8cee941` đúng cả ba OID; ancestor `01e7f77` → `8cee941` rc=0 | Có trong Git |
| r359 khai chưa đủ hậu-merge gate | chưa đọc CI; 0 hiện vật CI neo merge | Nội dung r359 đúng lời dẫn. `git grep -l 8cee941 71e0053 -- .` chỉ trả CHANGELOG; không có hiện vật CI neo SHA này ở cây lúc r359 sửa | Có trong cây lịch sử |
| Hiện vật CI neo merge ở HEAD | vẫn phân biệt hồ sơ kho với CI | Tìm SHA hiện trả CHANGELOG và biên nhận review 7; biên nhận không phải response CI. **0 response CI thô** neo merge được tìm thấy | Có giới hạn nguồn |
| Số bước CI đánh số | 41 mỗi job | YAML có 40 bước khai báo; các số được kể nhất quán với độ lệch +1 cho bước setup job. **41 bước runtime KHÔNG ĐO ĐƯỢC** vì thiếu response job | Chỉ đối chiếu cấu trúc |
| Ubuntu CI #490 | success; 37 success + 4 skipped + 0 failure | 37+4+0=41. Trạng thái thật và số đếm runtime **KHÔNG ĐO ĐƯỢC** | Số học đúng; CI chưa xác minh |
| Windows CI #490 | success; 35 success + 6 skipped + 0 failure | 35+6+0=41. Trạng thái thật và số đếm runtime **KHÔNG ĐO ĐƯỢC** | Số học đúng; CI chưa xác minh |
| Khoảng thời gian Ubuntu | 18:50:37Z → 19:11:32Z | Hiệu hai giờ được kể là **20 phút 55 giây**; mốc runtime **KHÔNG ĐO ĐƯỢC** | Số học đúng |
| Khoảng thời gian Windows | 18:50:37Z → 19:44:09Z | Hiệu là **53 phút 32 giây**; mốc runtime **KHÔNG ĐO ĐƯỢC** | Số học đúng |
| Danh tính run #490 | 34391481045; push; master; head 8cee941 | **KHÔNG ĐO ĐƯỢC**: không response Actions trong kho, không mạng. Git commit tồn tại không chứng minh run gắn với commit ấy | Chưa xác minh |
| Attempt run #490 | 1, không chạy lại | **KHÔNG ĐO ĐƯỢC**: không lịch sử attempt hoặc response Actions | Chưa xác minh |
| Hai lượt CI đối chiếu | 7693852 attempt 2; 28ba133 attempt 1 | Cả hai commit tồn tại, workflow cùng blob; attempt và kết quả **KHÔNG ĐO ĐƯỢC** | Một phần |
| Ba lượt cùng hình dạng skip | 3 lượt, khớp từng bước | CI-TĨNH: cùng workflow; khi push/master thành công, Ubuntu skip **11,23,28,39**; Windows skip **11,21,22,28,36,39**. Quan sát ba lượt thực **KHÔNG ĐO ĐƯỢC** | Thiết kế khớp 4/6; runtime chưa xác minh |
| Các điều kiện được dẫn | #11 PR-only; #22/#23 loại trừ; #38 LAND/#39 WORKER | Đúng từng biểu thức trong workflow. Mục r362 chỉ liệt kê một phần tập skip, không dùng phần liệt kê đó để tự đếm 4/6 | Có về mã |
| #490 nay landed | cả ba vế ĐẠT, 0 failure hai nền | Merge và chỗ bookkeeping đo được; vế CI **KHÔNG ĐO ĐƯỢC**. Do đó reviewer không tự chứng nhận landed | Chưa xác minh trạng thái GitHub |
| Bookkeeping không có tệp riêng #490 | dùng r359, chủ kho đóng chuỗi | r359 có ghi sổ và nêu quyết định đó; xác thực quyết định/authority GitHub **KHÔNG ĐO ĐƯỢC** | Có văn bản, chưa xác thực ngoại bộ |
| Thời gian treo nợ | ~7 giờ; bằng chứng sẵn từ 19:44:09Z | **KHÔNG ĐO ĐƯỢC**: thiếu mốc đọc/đóng nợ. Nếu lấy giờ commit đầu r362 làm điểm cuối thì hiệu là **7 giờ 59 phút 07 giây**, nhưng commit không phải thời điểm đọc CI | Không đủ mốc để kết luận |
| Câu r361 bị rút | “Nếu chỉ shellcheck hỏng thì không ai biết” | Câu có tại `CHANGELOG.md:287–292`; nợ tương ứng còn ở 314, dưới mục lịch sử r361. r362 rút rõ, không xem giữ văn bản lịch sử là lỗi mới | Có |
| A/B có shellcheck | actionlint DAT, shellcheck DAT, canary DAT, SC1003 rc=1 | Đo thật đúng cả bốn giá trị: actionlint **1.7.7**, shellcheck **0.9.0** | Có |
| A/B thiếu shellcheck | actionlint DAT, shellcheck KHONG_DO_DUOC, canary DO, blocking | PATH cô lập: đúng cả bốn; chi tiết SUY_GIAM, actionlint chạy fixture rc=0 | Có |
| Full scan tại môi trường reviewer | lời khai chỉ hứa trạng thái thành phần/canary | Có shellcheck: tổng DO, rc=2 vì probe jsonschema rc=1; thiếu shellcheck: tổng DO, rc=2, thêm canary DO. Không gọi nền này là xanh toàn bộ | Khớp thành phần; tổng bị lỗi môi trường khác |
| Quyền chặn của canary | `actionlint.canary=actionlint_shellcheck`; blocking | YAML và fixture tồn tại. Bản kê thử chỉ giữ cặp actionlint/shellcheck: có shellcheck tổng DAT rc=0; thiếu tổng DO rc=2 | Có; đã tách yếu tố jsonschema |
| Canary DO nâng tổng, trừ advisory | blocking chặn | Đổi chính sách thành advisory trong bản kê thử: canary vẫn DO nhưng tổng DAT rc=0. Đột biến bỏ nhánh nâng tổng cũng cho tổng DAT rc=0 | Có răng trong phép đo cô lập |
| Điều kiện chạy canary | chỉ khi `chi is None` | Full scan có 1 canary; cả hai lần `--chi shellcheck` có **0 canary** | Có |
| Một công cụ thiếu vẫn xanh | shellcheck KHONG_DO_DUOC, tổng DAT, `canary=[]` | Thiếu shellcheck + `--chi shellcheck`: đúng JSON và rc=0; có shellcheck: DAT, tổng DAT, rc=0 | Có |
| Hai bước cài riêng | #7 shellcheck, #8 rg | Workflow gọi đúng hai tên; dòng cuối installer gọi `kiem-tra --chi "$TEN" --json`; YAML khai shellcheck optional, rg bắt buộc | Có về đường gọi |
| Bước #9 G5 | full scan không `--chi` | YAML gọi `python ops/cong_cu.py kiem-tra --json`, rồi suite; đúng vị trí khai báo thứ 8, tương ứng số runtime được kể #9 | Có về mã |
| Windows đỏ: #8 chặn #9 | #7 xanh, #8 đỏ, #9 skipped | Workflow cho phép diễn biến ấy; JSON và trạng thái của lượt cụ thể **KHÔNG ĐO ĐƯỢC** | Chưa xác minh runtime |
| Hai lần chạy đủ bác r361 | 2 lần cong_cu.py | Một lần full với shellcheck, một lần thiếu: đo được canary DAT→DO. Số lần chính tác giả đã thực hiện **KHÔNG ĐO ĐƯỢC** | Có về khả năng tái hiện |
| Bài học đã ghi ba lần | “tệp này đã ghi ba lần” | **KHÔNG ĐO ĐƯỢC** con số ngữ nghĩa: không chỉ ra ba mục hay quy tắc đếm. CLAUDE có đoạn “ba lần trong MỘT phiên”, nhưng đó không phải phép đếm ba mục trong CHANGELOG | Chưa xác minh |
| Xuất xứ packet #290 | mã/spec từ #290, đóng băng | Spec và lịch sử merge `59fe955` khớp xuất xứ; header spec revision **1**, cảnh báo đóng băng có thật. `landed` GitHub **KHÔNG ĐO ĐƯỢC** | Có nguồn cục bộ |
| Protocol và AGENTS | §28/§116/§164; AGENTS:22–23 | Ba câu có ở **dòng** 28/116/164; AGENTS:22–23 đúng. Protocol chỉ có các mục chính đến **20**, không có ba mục được ký hiệu như vậy | Nội dung đúng; ký hiệu dẫn sai |
| Trang Issue cũ | 30 là cỡ trang, 0 khớp bị rút | Bản `25c2d5b` có lời khai 30/0; bản mới đã rút cách hiểu tổng. Response trang cũ **KHÔNG ĐO ĐƯỢC** | Đã sửa cách diễn đạt; không tái đo API |
| Tổng Issue và truy vấn từ khóa | 128 mở; total_count 101 | **KHÔNG ĐO ĐƯỢC**: thiếu response, truy vấn cụ thể, phân trang và thời điểm chụp; chưa gắn nhãn thuật lại tại chỗ | P2 |
| Tỷ lệ quét cũ | ≈23% | `30/128*100 = 23,4375%`; hai đầu vào không được xác thực ở đây | Số học đúng |
| Bốn Issue liên đới | #249, #295, #269, #297; cùng lớp, khác cơ chế | Danh sách viết ra có **4 số khác nhau**. Nội dung/trạng thái Issue và kết luận không trùng **KHÔNG ĐO ĐƯỢC** | Chỉ đếm được danh sách |
| Ca t33 liên quan #249 | đòi actionlint, không đòi shellcheck; tệp lease_publish_test.py | Đọc thân `t33_workflow_dang_lease_phai_qua_actionlint` ở dòng 1337: kiểm actionlint rồi lint một workflow, không kiểm shellcheck; quan hệ với Issue trực tiếp **KHÔNG ĐO ĐƯỢC** | Có về thân ca |
| Phiên đang chạy | KHÔNG ĐO ĐƯỢC | Không có nguồn trạng thái phiên; truy vấn Issue không đủ chứng minh | Nhãn đã đúng |
| Issue nhận nợ | đã mở #498 với các đính chính | **KHÔNG ĐO ĐƯỢC**: không có response Issue, không mạng; câu chưa mang nhãn thuật lại | P2 |
| Số mục manifest | 180→180, thêm/bớt 0 | Tự kiểm đủ 180 mục tại base, head cũ và head mới; tập đường dẫn không đổi | Có |
| Byte toàn gói | base 8.110.218; head mới 8.119.788 | Cộng byte thật được **8.119.788**; chênh **9.570** bằng byte CHANGELOG thêm | Có |
| Byte CHANGELOG | 815.896→825.466 | Byte thật **825.466**, SHA-256 `372cf56128918cb18087a8c39b4be832539b178377469765da54be43851f42d3` | Có |
| Hash gói ở ba mốc | base e116f6a8…; head cũ 124b13fc…; mới 279bac5d… | Đúng ba manifest. Strict verify tính lại hash hiện tại **279bac5d9069fcfb4ad1d42c5f041b2a4fc0d72179b7475412f2a43132ea2283** | Có; không nhầm base với head cũ |
| ops không nằm trong gói | 0 mục ops; chỉ CHANGELOG đổi hash nội dung gói | Cả ba manifest có **0** đường dẫn ops; so từng mục chỉ CHANGELOG đổi size/hash | Có |
| Release verify | ok=true; expected=checked=180; failed=[] | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: **rc=0**, đúng toàn bộ; tự kiểm 180 hash/kích thước, **0 lệch** | Có |
| Golden | ok=true; 0 mismatch; không đổi fixtures | `python3 scripts/tl.py golden-test --json`: **rc=0**, 20 ca, 0 ca sai; diff `references/golden/` rỗng | Có |
| Determinism | ok=true | `python3 scripts/tl.py determinism-audit --strict --json`: **rc=0**, 15 kiểm tra đạt | Có |
| Doc claims | ok=true; 106 tệp | `python3 scripts/tl.py doc-claims-check --strict --json`: **rc=0**, 106 tệp, flags=[] | Có; không chứng minh số liệu văn xuôi |
| Biên nhận v2 | 48 ĐẠT; 11/11 legacy; 42 nợ; 0 vi phạm; 0 không đo; tổng 101 | `python3 ops/bien_nhan_v2.py --root .`: **rc=0**, đúng cả bảy số, TỔNG: ĐẠT | Có |
| Suite biên nhận | 48/48; 63/63 đột biến; 2/2 tự kiểm | `python3 ops/bien_nhan_v2_test.py`: **rc=0**, đúng cả ba cặp, TỔNG: ĐẠT | Có |
| Suite lease | 121/121; đã chạy 121; bỏ qua 0 | `python3 ops/lease_publish_test.py`: **rc=0**, đúng cả bốn số | Có |
| Doctrine | rc=0 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **rc=0**, 7 tệp, 0 chỗ chép doctrine | Có |
| ADR sống | 46 ADR / 46 dòng §20 | `python3 .claude/dev/packet_loop.py adr-song --root .`: **rc=0**, 46/46 khớp 1–1; giữ ngoại lệ 0016 như cổng khai | Có |
| Suite công cụ và nền | ca=23; đột biến=18; lỗi đột biến=1; delta=0 | `python3 ops/cong_cu_test.py` tại HEAD và bản chép checkout **28ba133**: cùng **rc=1**, cùng 23/18/1; T2 bỏ qua do jsonschema, mutant t2_go_canary KHÔNG_ĐO_ĐƯỢC | Có; không gọi suite này đạt |
| Runtime tệp bị chạm | chỉ thêm chú thích | `ast.dump(ast.parse(...))` của cong_cu.py tại base và HEAD bằng nhau; diff đúng 15 dòng comment | Có |
| 9 lệnh so với toàn CI | 9 lệnh có bằng chứng; 31 bước cổng | Đã chạy lại 9 lệnh được liệt kê, thêm suite công cụ và hai lệnh CLI yêu cầu. YAML: **40 = 8 setup + 31 cổng + 1 upload**; không khai đã chạy toàn CI | Có |
| So mã thoát nền với sandbox ở EVIDENCE | doc-claims 0/0; biên nhận 0/0 | Phía sandbox đã đo lại đều 0; phía môi trường điều phối **KHÔNG ĐO ĐƯỢC** độc lập. Hai mã bằng nhau không mở rộng sang cổng khác | Một phần |

**Đột biến và phép thử bản vá — kết quả đã chạy, không phải kế hoạch:**

| ca trên bản chép | cổng/phép đo liên quan | nền → đột biến | kết luận về răng |
|---|---|---|---|
| Đổi 128 Issue thành 129, giữ manifest cũ | release-verify strict | rc=0 → **rc=2**, chỉ CHANGELOG lệch băm dù kích thước không đổi | Có răng với toàn vẹn byte |
| Cùng đột biến nhưng tái sinh manifest | doc-claims strict; release-verify strict | cả hai vẫn **rc=0**, 106 tệp, flags=[], failed=[] | Không kiểm được đúng/sai số Issue |
| Đổi 37 success thành 36, giữ 4 skipped và tổng 41 | doc-claims; tái sinh manifest; release-verify | tất cả **rc=0** | Không bắt cả mâu thuẫn cộng đơn giản |
| Ghi cha thứ nhất merge thành chính cha thứ hai, dùng SHA có thật | doc-claims; tái sinh manifest; release-verify | tất cả **rc=0** | Chỉ biết SHA tồn tại không bảo vệ quan hệ cha |
| Đổi xuất xứ #290 lại thành chủ | doc-claims; doctrine-scan; tái sinh manifest; release-verify | tất cả **rc=0** | Nghĩa thẩm quyền cần review văn bản |
| Đổi lời khai nhánh mù 1 thành 0 | doc-claims; tái sinh manifest; release-verify | tất cả **rc=0** | Không bảo vệ kết luận lịch sử về tập ref |
| Thay một tên trong tập bộ đệm đã đo, giữ nguyên lực lượng | so số đếm và so hiệu tập | 321=321 vẫn true; điều kiện không mù từ true thành **false**, tìm đúng nhánh Windows | Hiệu tập có răng; đây là đối chứng dữ liệu cục bộ, không giả một lượt GitHub |
| Bỏ shellcheck khỏi PATH, giữ hai công cụ trong bản kê thử | cong_cu.py kiem-tra --ban-ke … --json | tổng **DAT/rc=0 → DO/rc=2**; actionlint vẫn DAT | Canary bắt suy giảm thật, không dùng lỗi jsonschema làm tín dụng |
| Chặn vòng lặp canary bằng thay `if chi is None` thành `if False` | ca t13 có sẵn, gọi dưới đây | **rc=0 → rc=1**, lỗi “canary mất executable bị nuốt” | Ca hiện hữu giết đột biến đúng chốt |
| Cùng đột biến bỏ vòng canary, thiếu shellcheck | CLI với bản kê cặp thử | tổng DO/rc=2 → **DAT/rc=0**, canary=[] | Phản chứng trực tiếp: bỏ cơ chế làm mất chặn |
| Bỏ nâng tổng khi canary blocking DO | CLI với bản kê cặp thử | tổng DO/rc=2 → **DAT/rc=0**, canary vẫn DO | Phân biệt có kết quả với kết quả có quyền chặn |
| Đổi chính sách canary thành advisory | CLI với bản kê cặp thử | canary vẫn DO; tổng **DAT/rc=0** | Đối chứng đúng nhánh ngoại lệ mô tả trong r362 |
| Thêm nhãn nguồn rõ cho ref/Issue/#498; đổi ký hiệu dẫn protocol thành số dòng | doc-claims; release-manifest; release-verify | **rc=0** cả ba | Đã thử cách sửa trên bản chép, không sửa cây được review |

Lệnh gọi riêng ca t13 đã chạy từ gốc bản chép, trước và sau đột biến:

```sh
python3 -c "import sys; sys.path.insert(0, 'ops'); import cong_cu_test as t; t.t13_actionlint_bien_mat_giua_probe_va_canary()"
```

Năm ca đột biến lời khai dùng lần lượt các lệnh sau trong bản chép; mỗi ca được trả về nội dung gốc trước ca tiếp theo:

```sh
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
```

Không biến sự sống sót của đột biến văn xuôi thành finding rằng PR phải xây thêm cổng ngữ nghĩa. Phép thử này xác định rõ phần kết luận cần nguồn và review độc lập.

### hai-loi-khai-thieu-nhan-va-sai-co-trang  [P2]  Các số GitHub mới vẫn thiếu nhãn nguồn ngay trong bản đính chính

TỆP/DÒNG: `cay-kho/CHANGELOG.md:122–131`; lời hứa nguồn tại 7–8 và 119–120; cùng khoảng trống ở số ref lịch sử 16–22.

VẤN ĐỀ: Bản vá sửa được cỡ trang và lời khai về phiên, nhưng thay lời khai cũ bằng “Đo lại: 128”, “total_count: 101”, “Quét đúng … bốn Issue” và “Nợ đã mở … #498” mà không ghi đây là thuật lại của phiên điều phối. Nhãn “thuật lại” tại bảng CI không phủ những đoạn này; định nghĩa nguồn đầu r362 chỉ gọi run/job/bước CI là loại (b), còn dòng 120 lại hứa dán nhãn mọi số GitHub tại chỗ. Không có query/response/phân trang/timestamp trong kho để reviewer kiểm chứng. Đây là việc tiếp tục nâng lời kể thành phép đo đã đối chiếu, không phải bằng chứng rằng 128 hay 101 chắc chắn sai. Các số máy chủ lịch sử cũng cần phân biệt với số Git đọc lại được từ object/ref hiện có. Số “~7 giờ” chưa có hai mốc đo; cần ghi nguồn và mốc hoặc bỏ độ chính xác không có căn cứ.

ĐÃ THỬ VÁ: có — trên bản chép, mở rộng giới hạn nguồn sang mọi số GitHub, ghi rõ thiếu response thô; thêm nhãn thuật lại trước phép đo ref và đoạn số Issue; gắn nhãn riêng cho #498, giữ phần trạng thái phiên KHÔNG ĐO ĐƯỢC. Không thay số bằng một số tự đoán và không yêu cầu đốt CI.

ĐÃ THỬ NGHIỆM: Đột biến 128→129: `python3 scripts/tl.py doc-claims-check --strict --json` **rc=0**, files_scanned=106, flags=[]; manifest chưa tái sinh làm release-verify **rc=2** vì băm CHANGELOG. Sau `release-manifest --out RELEASE_MANIFEST.json --json`, release-verify **rc=0**. Với bản sửa nhãn nguồn, doc-claims, tái sinh manifest và release-verify đều **rc=0**. Số Issue, nội dung #498 và dữ liệu máy chủ lịch sử: **KHÔNG ĐO ĐƯỢC**, không mạng và không có response thô trong gói.

ĐỘ TIN: cao.

### dan-protocol-nham-so-dong-thanh-so-muc  [P3]  Ba dẫn chiếu protocol dùng số dòng dưới ký hiệu số mục

TỆP/DÒNG: `cay-kho/CHANGELOG.md:113–115`; `cay-kho/ops/cong_cu.py:220`.

VẤN ĐỀ: “§28/§116/§164” không phải các mục của protocol. Những câu được dẫn nằm ở **dòng 28, 116, 164**; tài liệu có mục chính đến §20. Nội dung thẩm quyền đã sửa đúng, nhưng người theo dẫn chiếu sẽ tìm các mục không có. Đổi sang `docs/PROTOCOL_DA_PHIEN.md:28`, `:116`, `:164` hoặc tên mục tương ứng; không cần sửa quy tắc thẩm quyền.

ĐÃ THỬ VÁ: có — đổi thành “dòng 28/116/164” ở cả CHANGELOG và chú thích trên bản chép.

ĐÃ THỬ NGHIỆM: `rg -n '^## ' docs/PROTOCOL_DA_PHIEN.md` cho mục cuối §20; `nl -ba docs/PROTOCOL_DA_PHIEN.md` tại ba vị trí xác nhận nguyên văn. Sau sửa: doc-claims **rc=0**, release-manifest **rc=0**, release-verify strict **rc=0**. Các cổng không kiểm kiểu dẫn số dòng này.

ĐỘ TIN: cao.

## GIỚI HẠN

- Không đo trực tiếp GitHub: trạng thái PR/Issue/phiên, review trước, run/job/attempt, thời lượng, skip runtime, thẩm quyền hiện hành, hoặc `landed`. Các nhãn KHÔNG ĐO ĐƯỢC trong bảng là giới hạn bằng chứng, không tự biến thành finding hay yêu cầu chạy CI mới. Đặc biệt không yêu cầu CI hoàn tất cho head e826730.
- Có lệch giữa gói thực và mô tả dựng gói: `EVIDENCE.md` nói origin trỏ mirror, nhưng `git config --local --get remote.origin.url` thực tế trả URL GitHub. Vì vậy không chạy `ls-remote origin`; chỉ đọc `kho.git` trong sandbox. Tập hiện tại là 321/321 sau loại alias HEAD, khác lời kể nguồn 320/321 và khác snapshot trước fetch 320/320. Không có snapshot theo thời gian để quyết định các số lịch sử sai hay chỉ khác thời điểm.
- `cong_cu_test.py` không đạt trọn: T2 và đột biến của nó KHÔNG_ĐO_ĐƯỢC vì thiếu jsonschema. Đã kiểm cùng lỗi trên exact base 28ba133 và HEAD; không quy lỗi này cho 15 dòng chú thích. Phép thử bản kê hai công cụ chỉ chứng minh cơ chế canary/tổng, không chứng minh cả môi trường G5 đạt.
- Không chạy toàn bộ 31 bước CI và không chạy trên Windows. Parse điều kiện workflow chỉ xác minh thiết kế, không chứng nhận một lượt CI thực. Các phép đo còn lại và mọi đột biến đều chạy cục bộ.
- Không tự soạn chuỗi tấn công. Những ca cần dữ liệu kiểu thoát/đồng tự/đường dẫn vượt cây không được thêm; chỉ chạy các suite hiện có và đột biến số, nhãn, điều kiện canary trên bản chép.
- Chỉ giữ một sản phẩm review mới ở gốc sandbox: `VERDICT.md`. Thư mục tạm do lượt này tạo đã được dọn sau khi ghi kết quả. Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**; reviewed HEAD vẫn là SHA đầy đủ đầu báo cáo.
