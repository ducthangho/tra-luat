verdict: changes_requested
reviewed_sha: 3ae4f6157636949b2941a218deba5dbaa7df1d30
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: d7d4f9d655edd6c81d9964c573bcf3a6c9ea7e9dcb6d2cca98883cc8bb02beaa
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 9
review_generation: 3; lượt 3
review_class: sensitive
hint_sha256: 67a3b7d5cf558103ee080931efaf8457d1021e85a5cd3cc4eb75b6a23c77bccc

**0 P1, 1 P2 sửa được trong write set.** Finding lượt trước **ĐÃ VÁ THẬT**. Workflow HEAD cấp đúng credential và đúng phạm vi trong phép đo offline. Còn m23 SỐNG: hạ chữ hoa của TL_TOKEN thành chữ thường trước encoder vẫn qua t152, vì cả ba fixture đều không có chữ hoa. Phép đo bằng token giả lẫn hoa/thường cho header sai byte. HINT đổi một literal fixture, không tăng dòng và giữ mọi chốt cũ. Không có bằng chứng HEAD fetch đỏ hoặc làm lộ token thật trên runner.

Bắt đầu theo yêu cầu: 2026-09-11T09:47:41Z. VERDICT đã được ghi sớm rồi bổ sung. Các số thực thi dưới đây được đo mới trong lượt 9.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc verdict/HINT gen3 lượt 2, đối chiếu hunk và chạy m22 rồi m1–m21 **trước khi làm lại (1)–(6)**. Đọc phần test/spec cần thiết để dựng phép đối chiếu, không dùng lại số thực thi cũ.

- `nguon/VERDICT.rvm9-8.md`: **50566f7c0110e471696f65032105c90c929f95b90208486022841b68355be922**, khớp.
- `nguon/HINT.rvm9-8.patch`: **86968dcdf6fd06676455998050b8690f663c9acbcbbf68f57eb72d150be0697a**, khớp tiền tố được giao.

Slug `t152-bo-sot-header-env-con-sau-fetch` [P2]: **ĐÃ VÁ THẬT**.

| Phép đối chiếu tự đo | Kết quả |
|---|---|
| `git diff 81af1c9..HEAD` so HINT từng hunk | Đúng 1 hunk/1 dòng; tọa độ và thân hunk bằng nhau; Git chỉ thêm tên hàm sau `@@` |
| Áp HINT lên test 81af1c9 trong scratch | `patch -p0` rc=0; toàn tệp kết quả trùng byte HEAD |
| Workflow / số commit | Không đổi so 81af1c9; đúng 1 commit mới |
| m22 với test cũ / HEAD | **SỐNG / GIẾT**, HEAD đỏ đúng `(i)` rc=1 ở hậu kiểm biến |
| m1–m21 chạy mới | **20 GIẾT / 1 SỐNG hợp lệ (m17)** |
| Phạm vi thực thi HEAD / m22 | HEAD: VALUE_0 vắng ở Git rev-parse và child sau fetch; m22: header đầy đủ còn trong env cả hai |

Tác giả áp nguyên HINT, không sửa gì khác. M23 mới cũng **SỐNG với test 81af1c9** khi tự chạy lại: thiếu fixture hoa/thường đã có trước hunk hậu kiểm, không phải vá sinh lỗi mới.

Bằng chứng: [so HINT](scratch/logs/prior-hint.json), [delta](scratch/logs/prior-delta.patch), [ma trận](scratch/logs/prior-mutants.json), [runtime](scratch/logs/runtime.json), [đối chứng m23 cũ](scratch/logs/hint-validation.json). Script: [review.py](scratch/review.py).

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 9 | Khớp? |
|---|---|---|---|
| Spec đóng băng | b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường spec trong clone không tồn tại | Khớp bản cung cấp |
| Head/base | 3ae4f615 / 27c413c3 | Đúng SHA đầy đủ đầu verdict | Có |
| Delta lượt này | Nguyên HINT, 1 commit, workflow không đổi | Hunk/apply trùng byte; workflow còn trùng byte head lượt 1 `62c299a` | Có |
| Write set | +11 workflow/+69 test, −0 | **2 tệp, +80/−0**; từng commit từ base cũng chỉ chạm hai đường | Có |
| Master đi tiếp | e82af37 không chạm write set | **e82af37fe66629d5378ac56fc689e24db26594fa**; diff hai đường với base rỗng | Có |
| Ca cũ / whitespace | Không đổi / sạch | AST bỏ t152 bằng base; `git diff --check` rc=0 | Có |
| t152 nền | ĐỎ (i) | Hàm t152 HEAD đọc workflow 27c413c3: `(i) đoạn auth/fetch không chạy được: rc=1` | Có |
| t152/t148 HEAD | QUA | Cả hai gọi riêng XANH | Có |
| m22 cũ/mới; m16/m15/m13/m8 | Tác giả khai đã chạy lại | m22 SỐNG/GIẾT; các ca còn lại GIẾT đúng (i)/(i)/(v)/(v) | Có |
| Mutant tác giả chưa chạy lại | m1–m7, m9–m12, m14, m17–m21 | Reviewer đã chạy lại tất cả; m17 hợp lệ sống, các ca âm bị giết | Không gán công reviewer cho tác giả |
| Suite HEAD | 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, bản sao đủ ops/.github |
| Wrapper A2 | AL_VER=1.7.7, 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0, gói offline có sẵn | Có ở đường offline |
| Lint | actionlint + shellcheck rc=0 | **1.7.7 / 0.9.0**, rc=0; debug xác nhận ShellCheck cả hai run block; ShellCheck riêng rc=0 | Có |
| Fetch với header | Khắc phục thiếu auth | **Git 2.43.0 fetch thật**, helper HTTPS cục bộ nhận đúng header; chuyển object H còn thiếu, cập nhật ref; NHAN==H; rc=0 | Có tại biên helper/config, chưa HTTP |
| Phạm vi HEAD | Một lời gọi; không config đĩa/argv | Một helper; không credential trong argv Git/helper/Trace2; config repo không đổi; bốn biến auth/config vắng sau fetch | Có; lời gọi gồm cây tiến trình con |
| Shell/encoder | -euo pipefail, GNU -w0, mask trước, unset sau | Token dài 16/42/43/81/82/83/160: bytes đúng; lỗi encoder/printf/fetch/token chưa đặt đều dừng | Có tại Linux này |
| m23 mới | Chưa có trong EVIDENCE | t152/t148 **SỐNG**, lint rc=0; token lẫn hoa/thường bị đổi byte trước encoder; helper từ chối rc=128 | P2 thiếu nhánh dữ liệu |
| Suite m23 | Reviewer tự đo | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Xác nhận toàn gate bỏ lọt |
| HINT | Trong write set, ≤80 dòng thêm | 1 hunk/1 dòng test; dry-run/apply rc=0, trùng byte; vẫn +69/+11, −0 | Có |
| Ma trận HINT | Giữ dương, giết âm | HEAD/m17/dạng (b)/github.token/khoảng trắng XANH; base và mọi mutant âm m1–m26 GIẾT | Có |
| Suite HINT | Không hồi quy | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |

Bằng chứng: [metadata](scratch/logs/metadata.json), [full diff](scratch/logs/full-diff.patch), [controls](scratch/logs/controls.json), [suite](scratch/logs/suite.json), [log suite](scratch/logs/suite.log), [wrapper](scratch/logs/wrapper.json), [lint](scratch/logs/lint.json), [actionlint debug](scratch/logs/actionlint.log), [runtime](scratch/logs/runtime.json), [độ dài](scratch/logs/runtime-lengths.json), [mutant mới](scratch/logs/extra-mutants.json), [HINT](scratch/logs/hint-validation.json).

**Cách chạy suite:** lệnh `python3 ops/lease_publish_test.py` tại `scratch/head-tree/`, bản sao đầy đủ `ops/` và `.github/`, hai tệp review trùng byte clone. T82 gọi `copytree(HERE.parent, …)` nên chạy trực tiếp trong clone sẽ sao cả tệp người dùng cấm đọc. Bản sao vẫn có đủ workflows, không làm ca tự qua do thiếu thư mục. TMPDIR nằm trong `scratch/tmp/`, tắt bytecode; Git system/global config được cô lập. Wrapper chạy `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` với `AL_GOI=nguon/actionlint/goi.gz` (đường tuyệt đối), `AL_DICH`/RUNNER_TEMP trong scratch, `TAR_OPTIONS=--no-same-owner`. Không chạy đường tải mạng. Các suite đối chứng dùng `scratch/m23-tree/` và `scratch/hint-tree/`.

### (1) Shell và mức kết luận fetch xanh

- **Workflow 71/73:** TL_TOKEN lấy `secrets.GITHUB_TOKEN`; `set -euo pipefail` ở đầu bước. Probe chạy nguyên shell đến hết phép so NHAN==H với repo S/H thật khác nhau. Cờ cuối **ehuBc**, không có `x`.
- **97:** gán AUTH_B64 bằng pipeline. `printf 'x-access-token:%s'` dùng format cố định và quote token; đo input encoder đúng **n+15 bytes**, không LF thêm. Bash `printf`/`echo` được xác nhận là builtin. Encoder argv chỉ `-w0`, token qua pipe. GNU base64 **9.4** nhận -w0 và không wrap; `$(...)` bỏ LF cuối output, không sửa LF giữa chuỗi. Đo cả padding **0/2/1** và token dài 160; tất cả header đúng byte.
- **98:** gán xong mới đăng ký mask, trước Git. HEAD chỉ phát command mask trong phần auth; probe thêm dòng POST và hai dòng builtin để quan sát. Stderr tiến độ Git không chứa token/base64 fixture. Đây là đo command và thứ tự shell, chưa đo masker Actions.
- **99–104:** dấu nối dòng giữ COUNT/KEY/VALUE và Git trong một simple command. Biến chỉ cấp tạm cho lời gọi Git. Git **2.43.0** thực sự đọc cấu hình env khi fetch; helper hỏi Git config thật và nhận header. Key `http.https://github.com/.extraheader` khớp URL `https://github.com/$TL_KHO`; dòng 80 chốt kho canonical. Host đối chứng không nhận header; m24 đổi key sang host đối chứng khiến URL fetch thiếu header. Hai `-c protocol...` không ghi đè header; m11 HTTPS=never bị Git thật chặn trước helper.
- **105–107:** fetch thành công rồi unset AUTH_B64, Git rev-parse và so NHAN==H. HEAD không còn AUTH_B64/COUNT/KEY_0/VALUE_0 ở shell và child hậu kiểm. Git rev-parse sau fetch cũng không nhận chúng. Fetch lỗi thì `-e` dừng trước unset và mọi lệnh sau; không có receipt hay child hậu kiểm trong probe. Unset không phải xoá sạch memory.
- Đối chứng lỗi: encoder **9**, printf **8**, TL_TOKEN chưa đặt **1** đều dừng trước mask/fetch; fetch **128** dừng trước POST. Pipefail giữ lỗi printf dù encoder bên kia pipe vẫn có thể khởi động. Probe không tiếp tục dùng header dở dang.

**ĐÚNG/ĐỦ:** HEAD sửa đúng phần cấp credential ở biên đã đo, với điều kiện runner cấp TL_TOKEN hợp lệ và server cho token đọc ref. Không thể chốt “runner GitHub chắc chắn xanh” offline. Probe giữ URL HTTPS canonical, nhưng thay `git-remote-https` bằng helper cục bộ kiểm header rồi nối Git upload-pack qua pipe. **H chưa có trong client trước fetch; Git pack-objects/unpack-objects thực sự truyền object và ref được cập nhật.** Phép này không đi qua libcurl/HTTP/TLS/GitHub. Rc=128 của base/m5/m7/m16/m23/m24 là helper từ chối header thiếu/sai, không tái lập thông báo Username hoặc phản hồi GitHub thật. Chỉ đo binary 2.43.0 thuộc dải ≥2.31; chưa đo 2.31/toàn dải hay ảnh ubuntu-latest hiện hành. A3 sau land còn phải đo, không nâng giới hạn ấy thành finding.

Script tái lập: [probe.py](scratch/probe.py); [Trace2 HEAD](scratch/runtime/head/trace.jsonl) ghi đường thực thi và pack transfer.

### (2) Base64 có thể lộ ở đâu

| Bề mặt | Đo được / giới hạn |
|---|---|
| Log | HEAD không xtrace, mask trước Git, không in thêm header/token. M12/m13 bị giết vì stderr. Log offline chứa command mask thô của **token giả**, vì không có runner masker. |
| `::add-mask::` | Đăng ký giá trị để che log do runner xử lý sau đó. Không bảo vệ log trước đăng ký, không bảo đảm mọi biểu diễn đã biến đổi được che; không che argv, environment, pipe, memory, file hay artifact. Chưa đo bộ masker thật. |
| argv / ps | Git, helper, encoder và các argv trong Trace2 HEAD không chứa token/base64; encoder chỉ nhận -w0. Không chạy ps hoặc đọc proc ngoài cwd. Tiến trình đủ quyền đọc environment vẫn có thể thấy credential; mask không bảo vệ kênh này. |
| Environment | Helper fetch nhận COUNT/KEY/VALUE và TL_TOKEN. Phạm vi thực tế là **một lời gọi fetch cùng cây tiến trình con**, không phải chỉ một PID. TL_TOKEN thô vốn là env cả bước nên còn sau fetch. Bốn biến auth/config mới vắng ở child và Git sau fetch trên HEAD. |
| m22 đối chứng | Header VALUE_0 còn ở Git rev-parse và child sau fetch; COUNT vắng nên không tự trở thành cấu hình Git hiệu lực. Hậu kiểm mới giết đúng tồn dư env này. Không đo credential thật đi ra bên ngoài. |
| Config đĩa | `.git/config` fixture không đổi byte; HEAD không gọi git config ghi auth. M3 bị giết ở (iii). |
| Dạng (b) | Spec cho test nhận `git -c ...extraheader=...`; dạng này đặt base64 trong argv và vẫn là đối chứng dương của HINT. HEAD dùng dạng (a). Không gán tính “không argv” cho dạng (b). |
| Curl | Dòng 118 có từ base truyền TL_TOKEN thô trong argv curl. Không phải bề mặt base64 mới do 11 dòng patch thêm. |
| Receipt | Đọc workflow 121–141 và dict `ops/lease_publish.py:1772`: không serialize TL_TOKEN/AUTH_B64/VALUE_0. Blob định nghĩa được băm trước nội suy env. Đây là đọc mã, chưa đọc receipt/artifact thật hoặc chứng minh toàn nội dung thực tế sạch. |

### (3)–(6) Test, lint, write set và EVIDENCE

T152 chạy Bash thật nhưng stub hàm Git cho fetch, dùng `command git config` làm oracle. Nó đo bytes tới cấu hình Git theo URL, không mô phỏng HTTP hoặc engine biểu thức Actions. Bốn mutant A1 bị giết riêng ở (i)/(ii)/(iii)/(iv). Base chưa có t152, nên “t152 trên nền” ở đây là **hàm HEAD đọc workflow base**, đúng cách đối chứng lời khai.

Actionlint **1.7.7 từ nguon/**, ShellCheck **0.9.0** có trên PATH. Debug xác nhận ShellCheck trên cả hai run block, rc=0. ShellCheck riêng dùng `--norc --shell=bash -e SC2154` vì các biến env được YAML cấp. Pyflakes không có; không nhận tín dụng kiểm Python inline bằng pyflakes.

Toàn diff và đường theo từng commit base..HEAD chỉ có hai tệp write set. AST ngoài t152 không đổi; master mới không chạm write set. Không checkout/commit/đổi ref/index của clone. Các bản sao, repo fixture, mutant và thử HINT đều nằm trong scratch.

EVIDENCE giữ bảng +50/+79 ở các mục lịch sử, cập nhật +80 trong các phần mới; không coi lịch sử là khai sai HEAD. Phần gen3/lượt3 khai nguyên HINT, workflow không đổi, m22 cũ sống/mới đỏ, m16/m15/m13/m8, suite/lint: số tự đo khớp. Reviewer chạy các mutant tác giả nói chưa chạy lại, không gán công ngược. EVIDENCE nói rõ chưa đo runner và mask thật, không khai A3 xong hay mọi mutant bị giết. M23 chứng minh thiếu độ phủ, không chứng minh tác giả khai gian gate. Timeline, lease/reroute và comment/run không xác minh độc lập được offline; chỉ thị trực tiếp gen3 “chạy đến hết P1, P2” được dùng, không đọc doctrine.

## Findings

### t152-fixture-bo-sot-token-lan-hoa-thuong [P2] Fixture không phát hiện token bị chuyển thành chữ thường

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5418`; mutant ở workflow **97**, chỉ trên bản sao.
- **VẤN ĐỀ:** m23 thay biến đầu vào encoder từ `$TL_TOKEN` thành `${TL_TOKEN,,}`. Cả ba fixture t152 dùng tiền tố chữ thường và chuỗi `0123456789abcdef`, nên phép biến đổi sai này không đổi fixture: t152/t148 **SỐNG**, lint **rc=0**. Hợp đồng M1/M2 là header dẫn nguyên bytes từ TL_TOKEN; token là credential không có phép chuẩn hoá chữ hoa/thường trong spec. Với token giả có chữ hoa, m23 đưa bytes đã hạ chữ vào encoder, header giải mã khác token cấp ban đầu, helper kiểm bytes từ chối **rc=128**, không nhận H. Đây là nhánh dữ liệu có thật của việc giữ nguyên credential, độc lập với ba nhánh độ dài/padding. HEAD không có phép hạ chữ này.
- **ĐÃ THỬ VÁ:** HINT đổi **một literal** `0123456789abcdef` → `0123456789aBcDeF` trong fixture. Giữ nguyên ba độ dài 81/82/83, padding 0/2/1, nguồn env, oracle header/mask và hậu kiểm phạm vi. Không đổi workflow; test vẫn +69 dòng, tổng **+80/−0**. `patch -p0 --dry-run` và apply đều rc=0, trùng byte mong đợi; AST ngoài t152 không đổi.
- **ĐÃ THỬ NGHIỆM:** m23 SỐNG với cả test HEAD và 81af1c9; t148 và actionlint/ShellCheck qua. Probe HEAD với token giả lẫn hoa/thường rc=0, header đúng, H ban đầu thiếu được truyền và NHAN==H; m23 cùng token có header sai, rc=128. HINT giết m23 đúng **(i) Git không nhận header hiệu lực dẫn từ TL_TOKEN trên URL fetch**. Giữ HEAD/m17/dạng (b)/github.token/khác khoảng trắng XANH; base và mọi mutant âm m1–m26 GIẾT. **Suite m23: 147/147, rc=0; suite HINT: 147/147, rc=0; cả hai đã chạy=147, bỏ qua=0.**
- **ĐỘ TIN:** cao về mutant sống, bytes sai và hiệu quả HINT; không đo token thật, phân bố ký tự token hiện hành hoặc phản hồi GitHub. Xếp **P2 thiếu nhánh fixture độc lập**, cùng mức các finding wrap/padding: t152 vẫn đo bản vá thật và giết các mutant chịu lực đã chạy, nhưng thiếu một lớp dữ liệu. Không nâng thành P1 workflow HEAD fetch đỏ hoặc token thật đã lộ. M23 sống trước hunk hậu kiểm nên không phải vá sinh lỗi mới.

Bằng chứng: [delta m23](scratch/logs/m23.patch), [t152/t148/lint](scratch/logs/extra-mutants.json), [runtime bytes](scratch/logs/runtime.json), [HINT/ma trận](scratch/logs/hint-validation.json), [suite m23](scratch/logs/m23-suite.json), [suite HINT](scratch/logs/hint-suite.json). Script: [extra.py](scratch/extra.py), [validate_hint.py](scratch/validate_hint.py), [checks.py](scratch/checks.py).

## Mutant đã chạy

Dựng độc lập từ bytes HEAD trong `scratch/mutants/`. M1–m4 theo A1, m5–m22 theo verdict cung cấp; m23–m26 reviewer lượt 9. M2 dùng mẫu URL đã có trong spec. Không tạo nội dung đường dẫn thoát/khai thác.

| Mutant | Đột biến | t152 HEAD | Lý do / đối chứng | HINT |
|---|---|---|---|---|
| m1 | KEY_0 → http.postBuffer | **GIẾT** | (i) rc=1, thiếu header | GIẾT |
| m2 | URL credential mẫu A1 | **GIẾT** | (ii), URL chứa credential | GIẾT |
| m3 | Thêm git config local extraheader | **GIẾT** | (iii), lệnh ghi config | GIẾT |
| m4 | persist-credentials true | **GIẾT** | (iv), checkout sai | GIẾT |
| m5 | COUNT=0 | **GIẾT** | (i) rc=1; helper thiếu header rc=128 | GIẾT |
| m6 | VALUE_0 dummy | **GIẾT** | (i), header khác oracle | GIẾT |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), sai nguồn; helper rc=128 | GIẾT |
| m8 | Bỏ add-mask | **GIẾT** | (v), thiếu đăng ký mask | GIẾT |
| m9 | KEY http.extraheader toàn cục | **GIẾT** | (i) rc=94, host đối chứng nhận header | GIẾT |
| m10 | Fetch thứ hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Đếm 2 lời gọi fetch | GIẾT |
| m11 | HTTPS=never | **GIẾT** | (i) rc=95; Git thật chặn trước helper rc=128 | GIẾT |
| m12 | set -x trước AUTH_B64 | **GIẾT** | (v), stderr thừa | GIẾT |
| m13 | Thêm -x vào set đầu bước | **GIẾT** | (v), cờ đầu bước có hiệu lực | GIẾT |
| m14 | Bỏ -w0 | **GIẾT** | (i), wrap khác oracle | GIẾT |
| m15 | Bỏ padding = | **GIẾT** | (i), fixture có padding bắt được | GIẾT |
| m16 | env TL_TOKEN của bước fetch rỗng | **GIẾT** | (i), nguồn env | GIẾT |
| m17 | Scope header riêng repo canonical | **SỐNG** | **Biến thể hợp lệ**; helper đúng header, host đối chứng không nhận | SỐNG, đúng |
| m18 | COUNT=2, không có KEY_1 | **GIẾT** | (i) rc=95, missing config key | GIẾT |
| m19 | printf thêm LF trước encoder | **GIẾT** | (i), bytes khác oracle | GIẾT |
| m20 | Bỏ unset AUTH_B64 | **GIẾT** | (i) rc=1, hậu kiểm biến | GIẾT |
| m21 | Dời add-mask sau fetch | **GIẾT** | (i), thứ tự stdout sai | GIẾT |
| m22 | Export VALUE_0 riêng ngoài nhóm gán tạm | **GIẾT** | (i) rc=1; test 81af1c9 SỐNG; runtime còn env sau fetch | GIẾT |
| **m23 mới** | **Hạ TL_TOKEN thành chữ thường trước encoder** | **SỐNG** | **Fixture toàn chữ thường không phân biệt; token lẫn hoa/thường có header sai** | **GIẾT (i)** |
| m24 mới | Scope header sang host đối chứng | **GIẾT** | (i) rc=1; helper URL canonical thiếu header rc=128 | GIẾT |
| m25 mới | Basic → Bearer trong VALUE_0 | **GIẾT** | (i), header khác oracle | GIẾT |
| m26 mới | Export KEY_0 trước nhóm gán tạm | **GIẾT** | (i) rc=1, hậu kiểm bắt key còn đặt | GIẾT |

**Tín dụng HEAD:** m1–m22 = **21 GIẾT / 1 SỐNG hợp lệ**. Toàn m1–m26 = **24 GIẾT / 2 SỐNG**, trong đó m23 là mutant âm còn sót. **HINT = 25 GIẾT / 1 SỐNG hợp lệ.** Không nhận công HINT giết m23 cho PR hiện tại. M23 là phản chứng âm sống ngoài bốn ca A1; m5/m7/m10 gợi ý đã bị giết, không nhận chúng là phát hiện mới. Base, dạng (b), nguồn github.token, khoảng trắng và lỗi runtime là đối chứng riêng, không cộng mẫu số. Mutant nội bộ của 146 ca cũ không gộp vào bảng.

## HINT và phạm vi

`HINT.patch`: unified diff **patch -p0 từ gốc cay-kho/**, đúng HEAD, **1 hunk/1 dòng**, chỉ `ops/lease_publish_test.py`. Đã dry-run và áp trong scratch; không áp vào clone. Tổng diff sau HINT **+80/−0**, giữ workflow và các ca cũ.

Không mạng; không đọc tệp doctrine bị cấm hoặc tài liệu ngoài cwd; chỉ thực thi công cụ/runtime có sẵn. Không thao tác PR, canary hoặc land. Không dùng trần generation để hạ chuẩn, cũng không dùng giới hạn offline làm finding.

## chua_do_duoc

1. Fetch trên runner GitHub thật với quyền/token/ref kho thật; HTTP/TLS/redirect/libcurl và toàn job. A3 sau land chưa chạy. Helper local truyền pack nhưng rc=128 của nó không tái lập lỗi Username/HTTP thật.
2. Secret masker Actions, log/artifact/receipt thật; check_run_id/workflow_definition_commit/workflow_definition_sha256/checker_rc từ run thật. Command mask và đọc mã không thay readback.
3. Binary Git 2.31 hoặc toàn dải 2.31+, ảnh ubuntu-latest hiện hành, Windows/macOS/BSD base64. Đã đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4, Python 3.11.15, actionlint 1.7.7, ShellCheck 0.9.0 tại đây.
4. Engine biểu thức Actions và token thật. T152 nhận hai nguồn env cho phép rồi cấp fixture; probe cấp token giả hoặc literal rỗng m16, không giả lập mọi dạng env inheritance. Không đo định dạng/phân bố ký tự token GitHub hiện hành; finding m23 dựa trên hợp đồng giữ nguyên bytes TL_TOKEN.
5. Ps/proc/environment/memory ngoài fixture hoặc bảo đảm unset xoá memory. Đo argv/env do chính các tiến trình fixture báo và argv Trace2; mask không bảo vệ những kênh ấy.
6. Timeline Issue/comment/run/lease/reroute và hành động lịch sử tác giả; không xác minh quyền sở hữu write set từ hệ thống live. Git dựa trên snapshot cung cấp.
7. Wrapper tải mạng nguyên dạng, pyflakes và suite trực tiếp trong clone có doctrine. Đã dùng gói offline/bản sao đủ ops/.github và nêu rõ phạm vi.

Hoàn tất: 2026-09-11T10:03:40Z; trong giới hạn 40 phút.
