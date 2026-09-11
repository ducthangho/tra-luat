verdict: changes_requested
reviewed_sha: 2b52173529365ea04c854c738a1578a97c55a65a
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: eb9fed2b3275352bcffd3708f402367a18cbde3be38b90b81e9cc47be0330547
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 4
review_generation: 2; lượt 1
review_class: sensitive
hint_sha256: a4057e4a80ac787bfde38ac8b9877498a85f0dbfb62d7e868aa148cf5c7635fc

Finding lượt 3 **ĐÃ VÁ THẬT**. Phần truyền credential của workflow HEAD hoạt động đúng tại biên Git/helper đã đo offline. Còn **một P1 của chốt regression**: t152 bỏ phần đầu shell nên mutant m13 bật xtrace ở dòng `set` thực của bước vẫn XANH, trong khi Bash phát base64 trước mask. HEAD hiện tại không bật xtrace; đây không phải kết luận token thật đã lộ trên HEAD. HINT sửa được chỉ trong test, tổng diff so base vẫn +80/−0.

Hoàn tất lúc 2026-09-11T07:01:56Z; bắt đầu theo yêu cầu 2026-09-11T06:47:20Z, trong giới hạn 40 phút.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đọc và băm verdict/HINT lượt 3 trước mọi công việc khác. Verdict SHA256 khớp `ebaff0d45b1c4eb0b2f15f92462f78cc311698c6e3fd479414d8099b6c751dde`; HINT SHA256 `c4f7bcd97801cfd9a1090cba203743e4386b06ed369f4892b1a64d12f1dc5f7d`.

Slug `t152-bo-qua-stderr-truoc-mask` [P1]: **ĐÃ VÁ THẬT**. Tự áp HINT vào test tại c851f80 trong scratch: rc=0, toàn tệp trùng byte HEAD. Vị trí và toàn bộ thân hunk bằng nhau; chỉ tên hàm Git thêm sau `@@` khác. Chạy lại m12: test c851f80 XANH, HEAD ĐỎ đúng (v), có kiểm stderr. m1–m11 đều GIẾT; HEAD XANH, base ĐỎ (i). Log `scratch/logs/prior-hint-round4.json` và `scratch/logs/mutants-round4.json`. Chưa thấy hồi quy do hunk này.

## BẢNG ĐO

Mọi số đo dưới đây được chạy lại trong lượt 4, không kế thừa tín dụng lượt trước.

| Khẳng định | PR khai / yêu cầu | Đo được lượt 4 | Khớp? |
|---|---|---|---|
| Spec đóng băng | SHA256 b8200141… | Bản `nguon/M9-FETCH-AUTH.md` có SHA256 **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường tương ứng trong clone không tồn tại | Khớp bản cung cấp |
| Head/base | 2b52173 / 27c413c3 | SHA đầy đủ đúng metadata đầu tài liệu | Có |
| Write set | Hai tệp, +11 workflow/+69 test | `git diff --stat/--numstat 27c413c3..HEAD`: **2 tệp, +80/−0**, không tệp thứ ba; git status sạch | Có ở snapshot |
| Delta lượt này | Áp nguyên HINT lượt 3 | Một commit sau c851f80; một tệp, một hunk, 2 dòng thay; áp patch/cmp đúng byte | Có |
| Workflow không đổi | Từ 62c299a | Diff riêng workflow `62c299a..HEAD` rỗng | Có |
| Master đã đi tiếp | Không chạm write set | `origin/master=26e2555d36c48b3c0f625ae50ab2cfb62b6cb858`; `git diff --stat 27c413c3..origin/master -- <hai tệp>` rỗng | Có |
| t152 trên nền | ĐỎ đúng (i) | Test HEAD đọc workflow từ `git show 27c413c3:…`: `TinHieuChotCa`, `(i) đoạn auth/fetch không chạy được: rc=1` | Có; base chưa có t152 |
| t152/t148 HEAD | XANH | Hai ca gọi riêng đều XANH | Có |
| m1–m4 A1 | Bốn chốt độc lập | GIẾT lần lượt (i)/(ii)/(iii)/(iv) | Có |
| m1–m11 lượt này | Tác giả chưa chạy lại | Reviewer dựng và chạy lại: **11/11 GIẾT** | Không gán số reviewer cho tác giả |
| m12 | C851f80 SỐNG, HEAD GIẾT | Đúng; HEAD ĐỎ ở (v), stderr | Có |
| Suite HEAD | 147/147, rc=0 | `python3 ops/lease_publish_test.py`: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, trên bản sao mô tả dưới |
| Wrapper offline HEAD | AL_VER=1.7.7, 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, điều kiện offline nêu dưới |
| actionlint + shellcheck | rc=0 | actionlint **1.7.7**, shellcheck **0.9.0**, debug xác nhận gọi shellcheck trên cả hai run block; rc=0, không lỗi | Có; pyflakes không có |
| Whitespace | Sạch | `git diff --check 27c413c3..HEAD`: rc=0, output rỗng | Có |
| Header tới fetch | Sửa thiếu xác thực | Git **2.43.0 fetch thật** qua helper offline: HEAD rc=0, header đúng, kiểm OID qua; base/m5/m7 rc=128, header thiếu/sai | Có tại biên helper; chưa phải HTTP |
| URL scope | Chỉ github.com | Helper HEAD đọc đúng header cho URL canonical; URL host đối chứng không nhận header | Có |
| Phạm vi credential | Một lời gọi, không ghi config/argv | HEAD: 1 helper; argv Git/helper không có token/base64; `.git/config` fixture không chứa credential; helper con có header trong environment | Có, phải hiểu gồm cây tiến trình con |
| Shell/bytes | GNU -w0, mask trước dùng, unset sau | Bash **5.2.21**, base64 GNU **9.4**; bytes bằng Python; không LF; success qua hậu kiểm unset; lỗi encoder/Git dừng shell | Có trên Linux tại đây |
| m13 mới | Reviewer tìm mutant ngoài A1 | **t152/t148 XANH**, lint rc=0; thực thi shell+Git có trace base64 trước mask | Chốt còn thiếu, xem finding |
| Suite m13 | Đối chứng toàn cổng | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Xác nhận toàn cổng bỏ lọt |
| HINT / ma trận | Giết m13, giữ các chốt cũ | HEAD/dạng (b)/scope repo XANH; nền/m1–m13 ĐỎ đúng chốt | Có |
| HINT / phạm vi | Hai tệp, tối đa +80 | HINT 4 hunk trong test; dry-run/apply rc=0; byte sau apply bằng bản sửa thử; test so base **+69/−0**, workflow giữ **+11/−0** | Có |
| HINT / suite | Không hồi quy | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |
| Các ca cũ | Không đổi | AST sau bỏ riêng hàm t152: base = HEAD = HINT | Có |

Bằng chứng: [metadata](scratch/logs/metadata-round4.json), [so HINT lượt 3](scratch/logs/prior-hint-round4.json), [ma trận](scratch/logs/mutants-round4.json), [suite HEAD](scratch/logs/head-suite-round4.log), [rc suite](scratch/logs/head-suite-round4.json), [lint/versions](scratch/logs/lint-versions-round4.json), [Git/helper/argv](scratch/logs/git-probe-round4.json), [shell/bytes](scratch/logs/shell-round4.json), [HINT](scratch/logs/hint-validation-round4.json), [wrapper HEAD](scratch/logs/head-wrapper-round4.log), [rc wrapper](scratch/logs/head-wrapper-round4.json), [suite m13](scratch/logs/m13-suite-round4.log), [rc m13](scratch/logs/m13-suite-round4.json), [suite HINT](scratch/logs/hint-suite-round4.log), [rc HINT](scratch/logs/hint-suite-round4.json).

Suite chạy nguyên lệnh trong `scratch/head-tree/`, chứa đầy đủ `ops/` và `.github/` sao từ HEAD, hai tệp review trùng băm HEAD. T82 dùng `copytree(HERE.parent, …)`; chạy trực tiếp trong clone sẽ sao/đọc cả các tệp doctrine bị cấm. Bản sao tránh việc đó, vẫn giữ mọi workflow và dữ liệu trong hai thư mục; không lợi dụng thiếu workflow để cho ca tự qua. Bản sao m13/HINT dùng cùng cây này. TMPDIR nằm trong `scratch/tmp/`, tắt bytecode. Wrapper dùng AL_GOI cung cấp, SHA256 **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**, AL_VER=1.7.7, TAR_OPTIONS=--no-same-owner; không tải mạng.

### Shell và mức kết luận fetch

- Workflow **73** thực sự có `set -euo pipefail`; probe HEAD kết thúc với cờ `ehuBc`, không có `x`. T152 HEAD lại dùng cờ viết cứng trong stub và cắt bỏ dòng 73: đó là nguyên nhân m13 sống.
- **97:** `printf 'x-access-token:%s' "$TL_TOKEN"` là Bash builtin, format cố định, biến được quote, không thêm LF. `base64 -w0` GNU nhận stdin, không wrap/không LF; đo bytes Bash bằng base64 tính độc lập bằng Python và giải mã đúng. `$(...)` bỏ LF cuối nếu có; ở đây `-w0` không tạo LF. Không nhận phiên bản GNU container thành phép đo ảnh ubuntu-latest thật.
- Với encoder giả trả **9** hoặc printf trả **8**, pipeline/assignment dưới `-e` và `pipefail` dừng trước mask/fetch. TL_TOKEN chưa đặt bị `-u` chặn rc=1. Token rỗng/quyền token thật không được các cờ shell bảo đảm.
- **98:** echo là builtin; HEAD phát command đăng ký đúng base64 sau gán, trước Git. Base64 chuẩn ở đây một dòng. Đây là phép đo phát command và thứ tự, chưa phải phép đo secret masker Actions.
- **99–104:** ba phép gán cùng continuation thuộc environment của một simple command Git. COUNT=1 chọn đúng KEY_0/VALUE_0. Cờ `-c protocol…` không ghi đè extraheader. KEY scope `https://github.com/` khớp endpoint `https://github.com/$TL_KHO`; dòng 80 chốt kho canonical. Git fetch 2.43.0 thật đọc các biến và chuyển header tới helper con; m5 COUNT=0 thiếu header, m11 protocol=https never bị Git từ chối trước helper.
- **105:** success chạy `unset AUTH_B64`; hậu kiểm AUTH_B64/GIT_CONFIG_COUNT không còn đặt đều qua. Nếu fetch trả 128, `-e` kết thúc shell trước unset/NHAN/receipt; không có nhánh chạy tiếp. Unset không phải bảo đảm xoá mọi bản sao trong bộ nhớ.
- **106–107:** probe chạy cả preflight thật và kiểm OID `NHAN == TL_H`; HEAD qua rồi mới POST_OK. Helper quảng bá object fixture đã có trong repo. Không suy rc=0 đơn độc là đã kiểm đúng H.

**ĐÚNG/ĐỦ:** workflow HEAD sửa đúng phần thiếu credential ở biên đã đo; chưa đủ bằng chứng khẳng định xanh trên runner thật. Git thực chạy ở đây là **2.43.0**, không có phép đo binary **2.31** hoặc toàn dải 2.31+, runner hiện hành, GitHub token/ref thật, HTTP/TLS/redirect. Helper thay riêng transport HTTPS và từ chối thiếu/sai header bằng rc khác 0; rc=128 của base không phải tái lập thông điệp Username từ GitHub. A3 vẫn cần canary sau land. Việc chưa có canary không phải finding P1 của review này.

### Bề mặt token/base64

| Bề mặt | Đo được / giới hạn |
|---|---|
| Log HEAD | Không bật xtrace; auth block chỉ xuất base64 trong command đăng ký mask. Log fixture thô vẫn chứa command vì không có runner masker. m13 chứng minh đường phát base64 trước mask bị chốt bỏ sót. |
| `::add-mask::` | Đăng ký giá trị để runner che trong log do nó xử lý sau đăng ký. Không dùng command này để bảo đảm che output đã phát trước đăng ký, các dạng biến đổi khác, argv, environment, memory, config hoặc artifact. Bộ lọc Actions thật chưa đo. |
| argv | Wrapper fixture ghi đối số ngay trước exec Git thật; HEAD không có token/base64 trong argv Git/helper. printf/echo là builtin; base64 chỉ nhận `-w0`. Dạng (b) mà spec cho phép sẽ đặt header vào argv Git; HEAD dùng dạng (a). |
| Environment/ps | Helper thật nhận GIT_CONFIG_VALUE_0 có Basic header và TL_TOKEN kế thừa; AUTH_B64 không export. “Một tiến trình” phải hiểu là một lời gọi fetch cùng cây con. Tiến trình có quyền đọc environment vẫn có thể thấy credential; mask log không che được kênh ấy. Không đọc /proc hay ps của tiến trình ngoài fixture. |
| Config đĩa | Source không ghi auth config; `.git/config` fixture sau fetch không chứa extraheader/token/base64. |
| Curl sau fetch | Workflow 118 đã đưa TL_TOKEN thô vào argv curl ở base; không phải phần base64 mới do patch. Không nhận log mask thành bảo vệ argv. |
| Receipt | Đọc mã dựng receipt tại `ops/lease_publish.py:1772` và workflow 121–141: không serialize AUTH_B64/TL_TOKEN; băm blob là mã nguồn, không phải script đã expand secret. Chưa đọc artifact thật, không nhận tín dụng receipt thật sạch. |

## Findings

### t152-bo-qua-co-shell-truoc-wf-blob [P1] Bật xtrace ở đầu bước vẫn qua chốt bảo vệ base64

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5407` cắt đoạn chạy sau WF_BLOB; **5408** tự đặt `set -euo pipefail` trong stub; **5433** chỉ kiểm stderr của đoạn đã cắt. Vị trí mutant là `.github/workflows/ops-thu-hoi-admission.yml:73`.
- **VẤN ĐỀ:** m13 đổi duy nhất cờ shell đầu bước từ `set -euo pipefail` thành `set -euxo pipefail` trên bản sao. T152/t148 HEAD vẫn XANH, actionlint+shellcheck rc=0. Trong Bash chạy phần đầu bước thật, `-x` tiếp tục có hiệu lực tới phép gán AUTH_B64; base64 đi vào stderr trước mask. T152 bỏ chính dòng bật cờ và thay trạng thái shell bằng preamble viết cứng, nên kiểm stderr mới không thấy luồng output này. Đây là mutant ở trạng thái shell chi phối trực tiếp khối auth; không phải đòi test quét mọi phần job. **HEAD hiện tại không có `-x`; chưa đo token thật bị lộ.** Xếp P1 theo thang của yêu cầu về mutant SỐNG ở chốt bảo vệ base64.
- **ĐÃ THỬ VÁ:** HINT chạy nguyên bytes phần shell từ đầu bước tới trước NHAN, gồm preflight/cờ shell của workflow; cấp fixture S/H/workflow_ref và stub hẹp cho hai lời gọi rev-parse. Giữ phân giải config bằng Git thật, chốt stderr, đếm fetch và (ii)–(iv). Rút docstring để vẫn +69 test/+11 workflow = +80/−0. Không sửa mã workflow.
- **ĐÃ THỬ NGHIỆM:** m13 t152/t148 XANH; test c851f80 trên cùng m13 cũng XANH nên không phải lỗi do HINT lượt 3 sinh ra. Probe Git/helper thật rc=0, header đúng nhưng stderr có trace base64. Khi gộp hai luồng vào cùng pipe, trace gán ở **dòng 18**, command mask ở **dòng 20**. HINT giết m13 ở (v); giữ HEAD/dạng (b)/scope repo XANH; nền/m1–m12 vẫn ĐỎ đúng chốt; apply/dry-run rc=0 và AST ngoài t152 không đổi. Suite m13 **147/147, rc=0** xác nhận toàn cổng bỏ lọt; suite HINT **147/147, rc=0**, không bỏ qua ca nào.
- **ĐỘ TIN:** cao về mutant sống, bytes/thứ tự Bash và hiệu quả HINT trong phạm vi đo. Chưa đo log/mask trên runner GitHub thật. Giới hạn runner không xoá được bằng chứng shell phát output trước đăng ký mask.

Bằng chứng: [m13 t152](scratch/logs/extra-mutants-round4.json), [m13/test cũ và lint](scratch/logs/shell-round4.json), [lint m13](scratch/logs/m13-lint-round4.log), [Git thật](scratch/logs/git-probe-round4.json), [thứ tự hai luồng m13](scratch/logs/m13-merged-round4.json), [HINT ma trận/apply](scratch/logs/hint-validation-round4.json).

## Mutant đã chạy

Các mutant độc lập được dựng từ bytes HEAD trong `scratch/mutants/`; m1–m4 dùng mẫu spec, m5–m12 dựng lại theo verdict đã cung cấp. M13 chỉ đổi cờ debug trên bản sao; không tạo nội dung đường dẫn thoát/khai thác. m2 lấy nguyên mẫu URL credential từ spec được cung cấp.

| Mutant | Thay đổi | t152 HEAD | Lý do / phép đo thêm | Sau HINT |
|---|---|---|---|---|
| m1 A1 | KEY_0 → http.postBuffer | **GIẾT** | (i), rc=1, không header | GIẾT (i) |
| m2 A1 | URL credential theo mẫu spec | **GIẾT** | (ii), URL mang credential | GIẾT (ii) |
| m3 A1 | git config local extraheader | **GIẾT** | (iii), phát hiện lệnh ghi | GIẾT (iii) |
| m4 A1 | persist-credentials true | **GIẾT** | (iv), checkout giữ credential | GIẾT (iv) |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; fetch thật/helper rc=128, thiếu header | GIẾT (i) |
| m6 | VALUE_0 dummy | **GIẾT** | (i), header không bằng token fixture | GIẾT (i) |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), header sai; fetch thật/helper rc=128 | GIẾT (i) |
| m8 | Xoá add-mask | **GIẾT** | (v), thiếu đăng ký mask | GIẾT (v) |
| m9 | KEY thành http.extraheader toàn cục | **GIẾT** | (i), rc=94, host đối chứng nhận header | GIẾT (i) |
| m10 | Fetch lần hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Đếm 2; fetch thật/helper gọi 2 lần, lần hai thiếu header, rc=128 | GIẾT, đếm 2 |
| m11 | protocol.https.allow=never | **GIẾT** | (i), rc=95; Git thật rc=128, 0 helper | GIẾT (i) |
| m12 | set -x ngay trước AUTH_B64 | **GIẾT** | (v), stderr; test c851f80 vẫn SỐNG | GIẾT (v) |
| m13 reviewer | Thêm -x vào set đầu bước, trước WF_BLOB | **SỐNG** | T152 không chạy dòng bật xtrace; Git/shell thật vẫn phát base64 trước mask | GIẾT (v) |

**Tín dụng t152 HEAD: 12 GIẾT / 1 SỐNG.** Không nhận công HINT giết m13 cho PR hiện tại. M13 là mutant sống ngoài bốn ca A1 theo yêu cầu tìm mutant thứ năm; số m13 tiếp tục catalogue cũ.

Script tái lập: `scratch/review_matrix.py`, `scratch/probe_git.py`, `scratch/probe_shell.py`, `scratch/validate_hint.py`, `scratch/run_gates.py`. Các lần neo mutant ban đầu sai quote/count bị assert chặn trước khi chạy; đã sửa rồi chạy lại. Bản m10 đầu thiếu dòng refspec nên chưa dùng làm bằng chứng transport; bản cuối trong log có refspec đầy đủ, hai helper. Không có phép đo sản phẩm nào lấy từ lần dựng lỗi.

## Đối chiếu EVIDENCE.md

Các số +50/+79 là lịch sử lượt 1/2, được phần lượt 3 và gen 2 cập nhật +80; không coi đó là khai sai HEAD. Lời khai gen 2 áp nguyên HINT lượt 3, một commit, workflow không đổi, m12 sống trên test cũ/đỏ trên test mới, t152/t148 và suite HEAD xanh đều được đo lại khớp. Tác giả nói rõ **chưa chạy lại m1–m11 ở lượt này**; reviewer đã đo lại đủ, không chép số vòng cũ hoặc gán công cho tác giả.

EVIDENCE tự ghi chưa đo runner thật và mask thật; không khai đã nghiệm thu A3. Không có bằng chứng tác giả khai đã giết m13 hay mọi mutant. Các mốc giờ, Issue/comment/run lịch sử, lease/reroute và thao tác khôi phục cây của tác giả không xác minh độc lập khi không mạng. Quyền review gen 2/lượt 1 và giới hạn write set nhận theo chỉ thị trực tiếp của người dùng; không dùng S6 cũ trong spec để xin lại phép.

## HINT và phạm vi kiểm

`HINT.patch` là unified diff cho `patch -p0` từ gốc `cay-kho/`, so với đúng HEAD đã review. **4 hunk, chỉ `ops/lease_publish_test.py`**. Đã dry-run/apply trong `scratch/hint-apply/`, bytes khớp bản sửa thử; giữ workflow nguyên byte, AST 146 ca cũ/helpers nguyên. Tổng so lease base vẫn +80/−0.

Stub rev-parse chỉ cấp fixture cho preflight để trạng thái shell thật đi tới auth; không nhận tín dụng kiểm nguồn S/blob hoặc HTTP từ stub ấy. HINT còn dựa vào hình dạng NHAN của workflow hiện tại; không phải parser mọi Bash. Probe Git độc lập dùng Git thật qua helper offline, khác phép đo t152 và có ghi rõ biên thay thế transport.

Không sửa tracked files, checkout/reset/commit/ref trong `cay-kho/`; không đọc nội dung doctrine bị cấm, không gọi mạng hoặc đọc nội dung tệp ngoài cwd. Mọi repo fixture, mutant và bản sửa thử ở `scratch/`.

## chua_do_duoc

1. Fetch xanh trên GitHub runner thật, GITHUB_TOKEN/quyền contents:read đối với ref kho thật, HTTP/TLS/redirect và cả job. M3/A3 sau land chưa thực hiện.
2. Secret masker Actions, thứ tự xử lý các luồng log của runner, debug thực tế. Chỉ đo Bash phát bytes/command/thứ tự; token sử dụng đều là fixture công khai.
3. Receipt/artifact thật cùng check_run_id, workflow_definition_commit, workflow_definition_sha256, checker_rc. Đọc mã dựng receipt không thay cho readback.
4. **Windows KHÔNG ĐO ĐƯỢC**; Git 2.31/toàn dải 2.31+, macOS/BSD base64, ảnh ubuntu-latest hiện hành chưa chạy. Đã đo Linux, Python 3.11.15, Bash 5.2.21, Git 2.43.0, GNU base64 9.4, actionlint 1.7.7, shellcheck 0.9.0.
5. Memory dump/ps/environment ngoài fixture, hoặc việc unset xoá sạch bí mật trong bộ nhớ. Helper fixture có header trong environment đã đo; mask không bảo vệ kênh đó.
6. Timeline Issue/comments/run/lease, thao tác tác giả, tính đúng của tuyên bố lịch sử “mọi PR/không bao giờ xanh”; chỉ snapshot/diff/băm và hành vi offline được xác minh độc lập.
7. Wrapper tải mạng nguyên dạng; wrapper ở đây dùng AL_GOI đã ghim băm. Suite chạy trên bản sao ops/.github để tuân thủ lệnh cấm đọc doctrine; không gọi đó là lần chạy trực tiếp trong clone gốc. Pyflakes không cài, không nhận tín dụng kiểm Python inline từ actionlint.
