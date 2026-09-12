verdict: changes_requested
reviewed_sha: c851f8005c0493799df87f87e3e4d586e2746634
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: da7aec4701081ea617e25077186afb22c3e9031624b27ea0304386e87c21cbb6
model_tu_khai: GPT-6 / Codex / OpenAI; reviewer khác nền tác giả claude
review_round: 3
review_class: sensitive
hint_sha256: c4f7bcd97801cfd9a1090cba203743e4386b06ed369f4892b1a64d12f1dc5f7d

Hai finding lượt 2 **ĐÃ VÁ THẬT**, áp đúng nguyên HINT. Workflow HEAD truyền header đúng tới Git/helper trong phép đo offline. Còn một **P1 của chốt regression**: m12 bật xtrace ngay trước phép gán base64 vẫn qua t152, dù Bash phát base64 ra stderr trước command đăng ký mask. **HEAD hiện tại không bật xtrace; không có phép đo token thật bị lộ trên HEAD.** HINT sửa được trong một tệp của write set, giữ tổng diff **+80/−0**. Vì còn P1 vá được, kết luận `changes_requested` theo quy tắc lượt 3/3.

Mọi số đo dưới đây được chạy lại trong lượt 3; hoàn tất lúc 06:20 UTC ngày 11-09-2026, trong giới hạn 40 phút.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc verdict/HINT lượt 2 và đối chiếu diff trước các công việc review khác; ghi VERDICT sớm, rồi bổ sung theo phép đo.

- SHA256 `nguon/VERDICT.rvm9-2.md` = **13a0b829fa81f330a8989872b4d3df4ed9968f5f5c563d9baa2dc4912784c4fb**, khớp yêu cầu.
- SHA256 `nguon/HINT.rvm9-2.patch` = **ebb87804eb7d1f4d8519aa671ccdbc1e6c5d5610d06f5cbf716d8a2331e3c2d8**.
- Lấy test từ `git show 6254570:ops/lease_publish_test.py`, áp HINT bằng `patch -p0` trong `scratch/prior-apply/`: rc=0; `cmp` toàn tệp với HEAD rc=0. SHA256 cả hai = **da7aec4701081ea617e25077186afb22c3e9031624b27ea0304386e87c21cbb6**. Không có ngoại lệ docstring ở lượt này.

| Slug lượt 2 | Phân loại | So từng hunk và bằng chứng tự đo lượt 3 |
|---|---|---|
| `t152-bo-sot-fetch-thu-hai` [P1] | **ĐÃ VÁ THẬT** | Hunk `@@ -5390,7 +5390,7 @@`: vị trí và toàn bộ thân hunk bằng HINT. m10 mới dựng ĐỎ: `đúng một lời gọi fetch H, thấy 2`. Chạy lại test 6254570 trên cùng m10: SỐNG. Git fetch thật qua helper: hai lời gọi, header lần 1 đúng/lần 2 rỗng, rc=128. |
| `t152-stub-khong-do-quyen-transport` [P2] | **ĐÃ VÁ THẬT** | Hunk `@@ -5412,6 +5412,7 @@`: vị trí và toàn bộ thân hunk bằng HINT. m11 mới dựng ĐỎ (i), rc=95. Test 6254570 trên cùng m11: SỐNG. Git thật rc=128, `fatal: transport 'https' not allowed`, **0** lần gọi helper. |

Đã chạy lại **m1–m9: 9/9 GIẾT đúng chốt**, HEAD XANH, nền ĐỎ (i), rc=1. Vì vậy không gọi hai cách vá là vá hờ hoặc vá sinh lỗi mới. m12 phát hiện trong lượt này cũng SỐNG trên test 6254570 đo lại: đó là lỗ còn sót, không phải hai hunk lượt 2 làm phát sinh.

Bằng chứng: [so từng hunk và metadata](scratch/logs/prior-hint-and-metadata-round3.json), [m1–m11](scratch/logs/mutants-round3.json), [đối chứng test lượt 2/m12](scratch/logs/extra-mutants-round3.json), [Git thật/helper](scratch/logs/git-fetch-round3.json).

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 3 | Khớp? |
|---|---|---|---|
| Spec đóng băng | b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; không có bản tại `cay-kho/ops/specs/M9-FETCH-AUTH.md` trong snapshot | Băm bản cung cấp khớp |
| HEAD/base | c851f80 / 27c413c3 | SHA đầy đủ đúng metadata đầu tài liệu | Có |
| Diff PR | Hai tệp, +11 workflow/+69 test | `git diff --stat/--numstat 27c413c3..HEAD`: **2 tệp, +80/−0** | Có, đúng trần |
| Ngoài write set | Không chạm | Không có tệp thứ ba trong diff; git status sạch | Có ở snapshot; không suy lịch sử thao tác chưa commit |
| Áp nguyên HINT lượt 2 | 2 hunk, không sửa gì khác | Apply/cmp đúng byte; `6254570..HEAD` đúng **1 commit**, chỉ test thay đổi | Có |
| Workflow từ lượt 1 | Không đổi | Diff `62c299a..HEAD` riêng workflow rỗng; SHA256 khớp | Có |
| origin/master đi tiếp | 27 commit, prompt nói chỉ reviews/CHANGELOG/manifest | **4b5184e21373eb8f8a36493d0282ebd020bb4458**, **27 commit**, còn chạm **ops/cong_cu.py**; diff hai tệp write set base..origin/master rỗng | Danh sách tổng trong prompt sai; điều kiện không chạm write set đúng |
| t152 trên nền | ĐỎ đúng (i) | Nạp t152 HEAD, trỏ tới workflow `git show 27c413c3:…`: `TinHieuChotCa`, `(i) đoạn auth/fetch không chạy được: rc=1` | Có; nền chưa có hàm t152 |
| t152/t148 HEAD | QUA | Cả hai XANH khi gọi riêng | Có |
| m1–m4 | Bốn lý do độc lập | GIẾT lần lượt (i)/(ii)/(iii)/(iv) | Có |
| m5–m11 | Các chốt cũ đều giữ | **7/7 GIẾT**; m5 rc=1, m6/m7 sai header, m8 (v), m9 rc=94, m10 đếm 2, m11 rc=95 | Có |
| Suite HEAD | 147/147 | `python3 ops/lease_publish_test.py`: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0, trong bản sao nguồn HEAD | Có với phạm vi bản sao ghi dưới |
| Wrapper HEAD | AL_VER=1.7.7, 147/147, rc=0 | **147/147, đã chạy=147, bỏ qua=0, rc=0**; gói cung cấp qua AL_GOI, TAR_OPTIONS=--no-same-owner | Có với điều kiện offline |
| actionlint + shellcheck | rc=0 | actionlint **1.7.7**, shellcheck PATH **0.9.0**; debug ghi hai lần gọi shellcheck, tổng **0 lỗi**, rc=0 | Có; pyflakes không có, không nhận tín dụng kiểm pyflakes |
| Whitespace | Sạch | `git diff --check 27c413c3..HEAD` rc=0 | Có |
| Header tới fetch | Sửa credential thiếu | Git **2.43.0** gọi fetch thật: HEAD rc=0, helper nhận đúng header; base/m5/m7 rc=128 với header thiếu/sai | Có ở biên Git/helper, chưa phải HTTP |
| URL scope | github.com canonical | HEAD header có ở URL fetch, vắng ở host đối chứng; đổi KEY sang host khác làm t152 ĐỎ (i), helper thiếu header/rc=128 | Có |
| Shell/bytes | Mask trước dùng, unset sau | Bash **5.2.21**, GNU base64 **9.4**; bytes Bash khớp Python, giải mã đúng, base64 trực tiếp không LF; thành công qua hậu kiểm unset | Có trên Linux này |
| Chốt không output thừa | Docstring/chốt (v) của t152 | m12 vẫn XANH nhưng stderr có base64 trước mask; lint m12 rc=0 | **Không đủ**, xem finding |
| Suite m12 | Reviewer đối chứng toàn cổng | **147/147, đã chạy=147, bỏ qua=0, rc=0** trên bản sao có m12 | Xác nhận toàn cổng vẫn bỏ lọt |
| HINT lượt 3 | Phải trong hai tệp/trần 80 | Một hunk test, thay hai dòng; dry-run/apply rc=0, bytes bằng bản sửa thử; AST ngoài t152 bằng HEAD; so base **+11/+69 = +80/−0** | Có |
| HINT / ma trận | Giữ dương, giết âm | HEAD/dạng (b)/scope repo XANH; nền/m1–m12 và host sai ĐỎ đúng lý do | Có |
| HINT / suite | Không hồi quy | **147/147, đã chạy=147, bỏ qua=0, rc=0** trên bản sao HEAD đã áp HINT | Có |

Log: [metadata](scratch/logs/metadata-round3.log), [suite HEAD](scratch/logs/head-suite-round3.log), [rc suite](scratch/logs/head-suite-round3.json), [wrapper HEAD](scratch/logs/head-wrapper-round3.log), [rc/gói wrapper](scratch/logs/head-wrapper-round3.json), [actionlint/shellcheck](scratch/logs/actionlint-round3.log), [shell/bytes](scratch/logs/shell-round3.json), [HINT](scratch/logs/hint-validation-round3.json), [suite m12](scratch/logs/m12-tree-suite-round3.log), [suite HINT](scratch/logs/hint-tree-suite-round3.log).

Suite và wrapper chạy nguyên lệnh trên bản sao `scratch/head-tree/` chỉ chứa đầy đủ `ops/` và `.github/`; hai tệp review trùng byte với HEAD. AST của toàn bộ 146 ca cũ và helper bằng base sau khi bỏ riêng hàm t152: [đối chiếu](scratch/logs/old-tests-unchanged-round3.json). Lý do: t82 dùng `copytree(HERE.parent, …)` sẽ đọc cả cây nếu chạy trực tiếp trong `cay-kho/`, trái yêu cầu không đọc doctrine. Các thư mục workflow, leases, reviews, prompts và tệp phụ thuộc đều có trong bản sao; không dùng việc thiếu workflow để cho ca tự qua. TMPDIR được đặt tới `scratch/tmp/`, tắt ghi bytecode. Không gọi mạng; wrapper dùng gói đã cung cấp, SHA256 **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**.

### Shell và kết luận fetch

- **Workflow 73:** `set -euo pipefail` có trong thân bước; probe HEAD có cờ `ehuBc`, không có `x`. Mọi token trong probe là fixture công khai.
- **97:** `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định, biến được quote, không thêm LF. Đo `printf` là Bash builtin. GNU `base64 -w0` nhận dữ liệu qua stdin, không wrap/không LF; bytes thu từ Bash bằng base64 tính độc lập bằng Python, giải mã đúng `x-access-token:` cộng token fixture. `$(...)` bỏ LF cuối nếu có; với `-w0` không có LF để bỏ. Việc GNU base64 tại đây nhận `-w0` không thay thế đo ảnh ubuntu-latest thật.
- **97 khi lỗi:** làm base64 trả 9 hoặc printf trả 8 khiến phép gán thất bại và script dừng trước mask/fetch; TL_TOKEN chưa đặt bị `-u` chặn rc=1. Token rỗng không bị cú pháp shell từ chối; giá trị/quyền token thật còn cần canary.
- **98:** echo là builtin; phát command mask sau gán, trước Git. Chuỗi base64 chuẩn một dòng không chứa các ký tự escape đặc biệt của payload workflow-command. Probe chỉ chứng minh phát command/thứ tự; không giả làm bộ lọc log Actions.
- **99–104:** ba phép gán liên tiếp cùng continuation thuộc environment của một simple command `git … fetch`. COUNT=1 bật cặp KEY_0/VALUE_0; VALUE chứa đúng Basic header. `-c protocol…` là các key khác, không ghi đè header. URL fetch `https://github.com/$TL_KHO` khớp `http.https://github.com/.extraheader`; dòng 80 chốt TL_KHO canonical. Git fetch thật ở đây đọc được các GIT_CONFIG_* và truyền tới helper con; host đối chứng không có header. Dạng (b) bằng `-c` và scope riêng repo đều qua t152 lẫn probe fetch.
- **Phiên bản Git:** thực thi **2.43.0**, gồm chính lệnh fetch và quyết định cho phép protocol. Không có phép đo binary **2.31** trong cwd; không nhận kết quả 2.43 thành chứng minh toàn dải 2.31+ hoặc phiên bản Git trên runner hiện hành.
- **105:** thành công thì `unset AUTH_B64` chạy; hậu kiểm AUTH_B64 và GIT_CONFIG_COUNT không còn đặt đều qua. Nếu fetch trả 128, `-e` kết thúc shell trước unset/hậu kiểm/NHAN. Điều đó không chạy tiếp tới receipt; unset cũng không phải xoá an toàn mọi bản sao trong bộ nhớ.
- **106–107:** so OID nhận được với TL_H còn nguyên. Probe Git local chạy từ đầu thân shell qua cả preflight và hai dòng này, rồi mới in POST_OK. Không suy fetch rc=0 đồng nghĩa đã nhận đúng H.

**ĐÚNG/ĐỦ:** không tìm thấy lỗi trong phần truyền credential của workflow HEAD ở biên đo được. Nó sửa đúng việc thiếu header trên lời gọi Git canonical. **Chưa đủ bằng chứng kết luận fetch xanh trên runner thật:** quyền token, ref thật, HTTP/TLS/redirect, ảnh runner và toàn job chưa được đo. Helper cục bộ thay riêng transport HTTPS, quảng bá object fixture đã có trong repo; rc=128 thiếu/sai header do helper từ chối, không phải tái lập thông điệp `could not read Username` của GitHub. M3/A3 vẫn là canary sau land.

### Token/base64 có thể hiện ở đâu

| Bề mặt | Kết luận theo phép đo và mã HEAD |
|---|---|
| Log thường | HEAD không bật xtrace, không in Authorization trong auth block ngoài command đăng ký mask. Log probe chứa fixture nguyên văn vì không có runner mask. m12 chứng minh stderr trước mask là một bề mặt test đang bỏ sót. |
| `::add-mask::` | Yêu cầu runner che giá trị đã đăng ký trong log do runner xử lý sau đăng ký. Không thể dựa vào command này để bảo vệ output đã phát trước đăng ký, dạng đã biến đổi, argv, environment, memory, tệp hay artifact. Chưa đo bộ lọc thật hoặc giả định tự che base64 dẫn từ secret. |
| argv | Dạng (a) HEAD: đối số Git sau expansion chỉ có các cờ protocol, URL/refspec sạch; helper argv cũng không có token/base64. printf/echo là builtin, base64 chỉ có `-w0`. Dạng (b) đặt header trong argv Git, dù được spec nhận. |
| Environment/cây tiến trình | Helper thực đo có `GIT_CONFIG_VALUE_0` chứa header và TL_TOKEN được kế thừa; AUTH_B64 không export. “Một tiến trình” ở comment 93 phải hiểu là **một lời gọi fetch và cây tiến trình con**, không phải đúng một PID. Sau fetch, environment gán riêng command không còn ở shell. |
| ps/quan sát máy | Quan sát argv thông thường không thấy base64 mới của dạng (a); tiến trình đủ quyền đọc environment có thể thấy header/token. Mask log không chặn việc ấy. Không thử đọc ps/environment của tiến trình ngoài fixture. |
| curl sau fetch | Dòng 118 đã truyền token thô qua argv curl từ base. Đây là bề mặt có sẵn, không phải base64 mới do patch; không dùng mask log để khẳng định argv an toàn. |
| Config trên đĩa | Không có lệnh ghi config trong block HEAD. Repo fixture sau fetch không có extraheader/token/base64 trong `.git/config`. t152 m3 chặn riêng lệnh git config ghi extraheader. |
| Receipt/artifact | Đã đọc `ops/lease_publish.py:1772` và workflow 121–141: mã dựng receipt không serialize biến auth; băm blob là bytes mã nguồn, không phải script đã thay secret. Không có receipt/artifact thật để readback; không tuyên chúng đã được kiểm sạch. |

## Findings

### t152-bo-qua-stderr-truoc-mask [P1] Xtrace phát base64 trước mask nhưng t152 vẫn xanh

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5430`–5434, đặc biệt chốt (v) ở **5433**. `p.stderr` chỉ được đưa vào thông điệp khi rc khác 0 tại 5429. Điểm đột biến tương ứng là trước workflow **97**.
- **VẤN ĐỀ:** m12 thêm đúng một dòng `set -x` ngay trước gán AUTH_B64, trong bản sao. t152 thực thi dòng đó, nhận rc=0, stdout vẫn đúng hai dòng nên XANH; stderr có trace chứa base64 trước command mask. Lời hứa “không có output thừa” bỏ mất một luồng log thực. Đây là đột biến ở phần gán/mask của bản vá, không phải thay endpoint hoặc nội dung khai thác. **HEAD hiện tại không bật xtrace và chưa đo token thật bị lộ trên runner.** Xếp P1 theo thang yêu cầu về mutant SỐNG ở chốt bảo vệ base64; không dùng thiếu canary làm lý do P1.
- **ĐÃ THỬ VÁ:** HINT thêm `and not p.stderr` vào chính chốt (v), sửa thông điệp nói rõ stderr. Không blacklist chuỗi `set -x`: kiểm kết quả thực thi. Một hunk trong test, thay hai dòng đã được thêm bởi PR; workflow giữ nguyên, tổng so base vẫn **+80/−0**.
- **ĐÃ THỬ NGHIỆM:** observer quanh `subprocess.run` không đổi giá trị trả về: m12 t152/t148 XANH, stderr chứa trace base64. Probe gộp stdout/stderr vào cùng pipe ghi trace gán ở **dòng 4**, command mask ở **dòng 6**. Git fetch thật/helper trên m12 rc=0, header đúng nhưng trace vẫn phát; actionlint+shellcheck m12 rc=0. HINT giết m12 đúng (v), giữ HEAD/dạng (b)/scope repo XANH và nền/m1–m11 ĐỎ đúng nhánh. Dry-run/apply rc=0, cmp bytes đúng, AST ngoài t152 không đổi. Suite đầy đủ m12 **147/147, rc=0** (chứng minh toàn cổng bỏ lọt); suite đầy đủ HINT **147/147, rc=0**, không bỏ qua ca nào.
- **ĐỘ TIN:** cao về chỗ mù stderr, bytes/thứ tự Bash và hiệu quả HINT; chưa đo xử lý hai luồng log hoặc secret masker của runner GitHub thật. m12 cũng SỐNG với test 6254570 đo lại, nên không quy lỗi này cho hai hunk vừa được tác giả áp.

Bằng chứng: [m12/đối chứng](scratch/logs/extra-mutants-round3.json), [stderr và thứ tự](scratch/logs/shell-round3.json), [Git/helper](scratch/logs/git-fetch-round3.json), [lint m12](scratch/logs/m12-lint-round3.log), [HINT/ma trận](scratch/logs/hint-validation-round3.json). Script tái lập nằm ở `scratch/mutants.py`, `scratch/extra_mutants.py`, `scratch/probe_shell.py`, `scratch/probe_git.py`, `scratch/validate_hint.py`.

## Mutant đã chạy

Mỗi mutant được dựng độc lập từ bytes workflow HEAD dưới `scratch/mutants/`; m1–m11 theo spec/verdict đã cung cấp, m12 là đột biến cờ debug vào bản sao. Không tạo nội dung đường dẫn thoát/khai thác. Cột t152 HEAD chỉ nhận tín dụng của PR hiện tại.

| Mutant | Thay đổi | t152 HEAD | Lý do / đối chứng | Sau HINT lượt 3 |
|---|---|---|---|---|
| m1 (A1) | KEY_0 extraheader → http.postBuffer | **GIẾT** | (i), rc=1, thiếu header | GIẾT (i) |
| m2 (A1) | URL credential theo mẫu spec cung cấp | **GIẾT** | (ii), URL mang credential | GIẾT (ii) |
| m3 (A1) | Thêm git config local extraheader | **GIẾT** | (iii), phát hiện ghi config | GIẾT (iii) |
| m4 (A1) | persist-credentials false → true | **GIẾT** | (iv), checkout sai | GIẾT (iv) |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; Git/helper thiếu header, rc=128 | GIẾT (i) |
| m6 | VALUE_0 là header dummy | **GIẾT** | (i), header hiệu lực sai | GIẾT (i) |
| m7 | Sau gán đúng, ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), header không dẫn từ TL_TOKEN; Git/helper rc=128 | GIẾT (i) |
| m8 | Xoá add-mask | **GIẾT** | (v), thiếu command đăng ký | GIẾT (v) |
| m9 | KEY thành http.extraheader toàn cục | **GIẾT** | (i), rc=94; helper nhận header cả host đối chứng | GIẾT (i) |
| m10 | Fetch thứ hai sau NHAN, --quiet trước --no-tags, không header | **GIẾT** | Đếm được 2; Git/helper lần hai thiếu header, rc=128 | GIẾT, đếm 2 |
| m11 | protocol.https.allow=never | **GIẾT** | (i), rc=95; Git thật rc=128 trước helper | GIẾT (i) |
| m12 (mới) | Thêm set -x trước gán AUTH_B64 | **SỐNG** | stderr phát base64 trước mask; t152 chỉ so stdout, lint vẫn xanh | GIẾT (v), có stderr |

**Tín dụng nhóm m1–m12 của t152 HEAD: 11 GIẾT / 1 SỐNG.** Đột biến sống ngoài bốn ca A1 đã tìm được là m12; không nhận công cho PR vì HINT giết nó. Đối chứng phụ: dạng (b) và scope riêng repo XANH cả test/probe, KEY sang host khác ĐỎ/thiếu header. Không gộp mutant của 146 ca cũ vào mẫu số này.

## Đối chiếu EVIDENCE.md

Các bảng +50 và +79 là lịch sử lượt 1/2, đã được phần lượt 3 cập nhật +80; không coi lịch sử là lời khai HEAD sai. Lượt 3 khai áp nguyên hai hunk, chỉ một commit, workflow không đổi, m5/m7/m8/m10/m11 ĐỎ và suite 147/147: **đã tự đo khớp**. EVIDENCE chỉ khai nhóm mutant ấy, không khai đã giết mọi mutant; m12 không phải bằng chứng tác giả khai gian các con số đã nêu.

EVIDENCE tự ghi **chưa đo runner thật/mask thật**; không có lời khai đã nghiệm thu A3 cần bác. Các mốc giờ riêng, thao tác khôi phục worktree của tác giả, run #500, Issue/comments, “mọi PR/không bao giờ xanh”, trạng thái lease khác và timeline nâng trần không xác minh độc lập trong điều kiện không mạng. Trần lượt 3 được nhận theo chỉ thị trực tiếp của chủ kho trong prompt, không dùng spec S6 cũ để xin lại phép. Sai lệch danh sách file origin/master thuộc prompt, không phải EVIDENCE.

## HINT và phạm vi kiểm

`HINT.patch` là unified diff so với **HEAD c851f80**, đường `ops/lease_publish_test.py` cho `patch -p0` từ gốc `cay-kho/`. Một hunk xử lý finding P1 duy nhất. Đã dry-run/apply trên `scratch/final-apply/`; bytes bằng bản sửa thử; AST ngoài t152 không đổi. Workflow giữ bytes hiện tại; so lease base, test **+69/−0** và workflow **+11/−0**.

Giới hạn HINT: kiểm stderr của đoạn auth/fetch được t152 thực thi với fixture, nơi Git config bình thường im lặng; không giả làm parser mọi Bash hoặc scanner toàn bộ log/job. Bộ dò fetch vẫn nhận lệnh Git/ref PR viết trực tiếp; stub vẫn đòi hình dạng đối số canonical và đo config, không đo HTTP. Các giới hạn ấy không thay thế việc vá stderr trong chính đoạn mà chốt đang chạy và tuyên không output thừa.

Không sửa tracked files, checkout/reset/commit hay ref của `cay-kho/`; không đọc nội dung các tệp doctrine bị cấm, không gọi mạng. Các bản sao suite chỉ chứa `ops/` và `.github/`. Lỗi thao tác reviewer: lần tạo hai script helper đầu dùng nhầm thư mục scratch ở ngoài cwd; lệnh chạy tại cwd báo không thấy tệp (rc=2). Hai tệp vừa tạo đã được xoá bằng đúng tên, không đọc/chạy; sau đó dựng lại trong `scratch/` của cwd và phép probe hoàn tất rc=0. Không dùng lần lỗi làm bằng chứng sản phẩm.

## chua_do_duoc

1. Fetch xanh trên GitHub runner thật, quyền/giá trị GITHUB_TOKEN đối với kho/ref thật, HTTP/TLS/redirect, ảnh ubuntu-latest và toàn job. Canary M3/A3 sau land chưa thực hiện; không có mạng.
2. Bộ lọc mask/ordering log của Actions và log debug thực tế. Chỉ đo Bash phát command/bytes/thứ tự; secret trong mọi probe đều là fixture công khai.
3. Receipt/artifact thật cùng `check_run_id`, `workflow_definition_commit`, `workflow_definition_sha256`, `checker_rc`. Đọc mã dựng receipt không thay được readback artifact.
4. **Windows KHÔNG ĐO ĐƯỢC**; Git 2.31, macOS/BSD base64 và Git/ảnh runner hiện hành không được chạy. Thực đo Linux, Python 3.11.15, Bash 5.2.21, Git 2.43.0, GNU base64 9.4, actionlint 1.7.7, shellcheck 0.9.0.
5. Quan sát ps/environment của tiến trình ngoài fixture, memory dump, hoặc việc unset xoá sạch bí mật khỏi bộ nhớ. Header trong environment helper con đã đo được; đây là giới hạn của dạng (a)/mask log.
6. Sự kiện Issue/comment/run lịch sử, thao tác tác giả và timeline lease/S5; chỉ snapshot/diff/băm được xác minh độc lập.
7. Wrapper tải mạng nguyên dạng không chạy. Dùng AL_GOI đã cung cấp, băm đúng pin, TAR_OPTIONS=--no-same-owner; không nhận là kiểm tải mạng/Windows. Suite chạy trên bản sao hai thư mục để tránh I/O doctrine của t82, không phải lần chạy trực tiếp ở clone gốc.
