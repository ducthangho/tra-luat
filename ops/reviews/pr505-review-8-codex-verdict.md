verdict: changes_requested
reviewed_sha: 81af1c90f21e7a7d861200f3a18b3707e0879162
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: 7f622c157cffd4705d807e17fc30a571dcdb88f4dbd5f3355e5bbc300fa501be
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 8
review_generation: 3; lượt 2
review_class: sensitive
hint_sha256: 86968dcdf6fd06676455998050b8690f663c9acbcbbf68f57eb72d150be0697a

**0 P1, 1 P2 sửa được trong write set.** Finding nguồn token lượt trước **ĐÃ VÁ THẬT**. Workflow HEAD tạo đúng header và giới hạn biến cấu hình trong lời gọi fetch ở phép đo offline. Tuy nhiên, m22 dời VALUE_0 thành một lệnh export riêng vẫn qua t152/t148, lint và toàn suite 147/147, để base64 tiếp tục đi vào tiến trình sau fetch. HINT sửa một dòng hậu kiểm trong t152, vẫn +80/−0 so base. Không có bằng chứng HEAD fetch đỏ hoặc làm lộ token thật trên runner.

Bắt đầu theo yêu cầu: 2026-09-11T09:27:15Z. VERDICT được ghi sớm rồi bổ sung. Tất cả số thực thi dưới đây được đo mới trong lượt 8.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc verdict/HINT gen3 lượt 1 trước các mục (1)–(6), đối chiếu hai hunk rồi chạy m16 trước, tiếp theo m1–m15, m18–m21 và m17.

- `nguon/VERDICT.rvm9-7.md`: **43b157ffe3f0b7092a303ffbc78629f27d3fb2cc6e3c95a3d3f937546b71fa88**, khớp.
- `nguon/HINT.rvm9-7.patch`: **b9e367abeec69f95296265d870b0aa4c90999c373279834ea8a0739f0eb27e53**, khớp tiền tố.

Slug `t152-khong-khoa-nguon-token-trong-env` [P2]: **ĐÃ VÁ THẬT**.

| Phép đối chiếu tự đo | Kết quả |
|---|---|
| `git diff 8726a1c..HEAD` đối chiếu HINT | Đúng 2 hunk; tọa độ và thân từng hunk bằng nhau, chỉ khác nhãn hàm Git thêm sau `@@` |
| Áp HINT lên test 8726a1c trong scratch | `patch -p0` rc=0; cả tệp kết quả trùng byte HEAD |
| Workflow so 8726a1c | Không đổi byte |
| m16 với test cũ / HEAD | **SỐNG / GIẾT** đúng `(i) env TL_TOKEN của bước fetch phải lấy GitHub token` |
| m1–m15, m18–m21 chạy lại | **19/19 GIẾT**, giữ các chốt cũ |
| m17 scope riêng repo | **SỐNG**, biến thể hợp lệ |

Tác giả áp nguyên HINT, không sửa gì khác. M22 cũng chạy **SỐNG với test 8726a1c**: lỗ hậu kiểm tồn dư header không phải hồi quy do hai hunk nguồn env. Không đổi trạng thái slug cũ thành “vá sinh lỗi mới” vì finding độc lập.

Bằng chứng: [so HINT](scratch/logs/prior-hint.json), [delta thực](scratch/logs/prior-delta.patch), [ma trận đo mới](scratch/logs/prior-mutants.json), [m22 với test cũ](scratch/logs/hint-validation.json). Script: [prior_review.py](scratch/prior_review.py).

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 8 | Khớp? |
|---|---|---|---|
| Spec đóng băng | b8200141… | Bản `nguon/` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường spec trong clone không tồn tại | Khớp bản cung cấp |
| Head/base | 81af1c9 / 27c413c3 | Đúng SHA đầy đủ đầu verdict | Có |
| Delta lượt này | Áp nguyên HINT, một commit, workflow không đổi | 2 hunk/apply trùng byte; đúng một commit từ 8726a1c | Có |
| Write set | 2 tệp, +11/+69, −0 | **2 tệp, +80/−0**; mọi commit từ base chỉ chạm hai tệp | Có |
| Master đã đi tiếp | e82af37, không chạm write set | **e82af37fe66629d5378ac56fc689e24db26594fa**; diff hai tệp với base rỗng | Có |
| t152 trên nền | ĐỎ (i) | Hàm t152 HEAD đọc workflow 27c413c3: `(i) đoạn auth/fetch không chạy được: rc=1` | Có |
| t152/t148 HEAD | XANH | Gọi riêng cả hai XANH | Có |
| m16 cũ/mới | XANH / ĐỎ nguồn env | Đúng cả hai đối chứng | Có |
| m15/m14/m13/m8 | Tác giả nói chạy lại | GIẾT đúng (i)/(i)/(v)/(v) | Có |
| Các mutant tác giả chưa chạy lại | m1–m7, m9–m12, m17–m21 | Reviewer chạy đầy đủ; m17 hợp lệ sống, các ca âm bị giết | Không gán số reviewer cho tác giả |
| Suite HEAD | 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, bản sao nêu dưới |
| Wrapper HEAD | AL_VER=1.7.7, 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 với gói cục bộ | Có ở đường offline |
| Lint | actionlint + shellcheck rc=0 | **1.7.7 / 0.9.0**, rc=0; debug xác nhận ShellCheck trên cả 2 run block; ShellCheck riêng rc=0 | Có |
| Ca cũ / whitespace | Không đổi / sạch | AST bỏ t152 bằng base; `git diff --check` rc=0 | Có |
| Header tới fetch | TL_TOKEN → Basic trên URL canonical | Git **2.43.0 fetch thật** với helper HTTPS cục bộ nhận đúng header; rc=0; NHAN==H | Có tại biên helper/config |
| Phạm vi HEAD | Một lời gọi, không argv/URL/config đĩa | Một helper; không credential trong argv Git/helper; config repo không đổi; KEY/VALUE/COUNT không có ở tiến trình sau fetch | Có; lời gọi gồm cây tiến trình con |
| Shell/encoder | -euo pipefail, GNU -w0, mask trước, unset sau | Bytes đúng ở token dài 16/42/43/81/82/83/160; qua NHAN/hậu kiểm; lỗi encoder/printf/fetch/token chưa đặt dừng | Có trên Linux này |
| m22 mới | Không có trong EVIDENCE | t152/t148 **SỐNG**, lint rc=0; Git sau fetch và child hậu kiểm nhận toàn bộ VALUE_0 | P2 thiếu hậu kiểm phạm vi |
| Suite m22 | Reviewer tự đo | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Xác nhận toàn gate bỏ lọt |
| HINT | Chỉ write set, ≤80 dòng thêm | 1 hunk, 1 dòng test; dry-run/apply rc=0, đúng byte; vẫn +69 test/+11 workflow | Có |
| Ma trận HINT | Giữ dương, giết âm | Base/m1–m16/m18–m22 GIẾT; HEAD/m17/dạng (b)/github.token/khoảng trắng XANH | Có |
| Suite HINT | Không hồi quy | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |

Bằng chứng: [metadata](scratch/logs/metadata.json), [controls](scratch/logs/controls.json), [suite](scratch/logs/suite.json), [log suite](scratch/logs/suite.log), [wrapper](scratch/logs/wrapper.json), [log wrapper](scratch/logs/wrapper.log), [lint/versions](scratch/logs/lint-versions.json), [debug actionlint](scratch/logs/actionlint.log), [runtime Git](scratch/logs/runtime.json), [độ dài](scratch/logs/runtime-lengths.json), [HINT](scratch/logs/hint-validation.json), [suite m22](scratch/logs/m22-suite.json), [suite HINT](scratch/logs/hint-suite.json).

**Cách chạy suite:** lệnh `python3 ops/lease_publish_test.py` chạy tại `scratch/head-tree/`, bản sao đầy đủ `ops/` và `.github/`, hai tệp review trùng byte clone. T82 gọi `copytree(HERE.parent, …)` nên chạy trực tiếp trong clone sẽ sao cả những tệp người dùng cấm đọc. Bản sao có workflows để các ca không tự qua do thiếu thư mục. TMPDIR ở `scratch/tmp/`, tắt bytecode. Wrapper chạy `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` với `AL_GOI` trỏ gói `nguon/actionlint/goi.gz`, `AL_DICH` và RUNNER_TEMP trong scratch, `TAR_OPTIONS=--no-same-owner`. Không kiểm đường tải mạng. Suite m22/HINT chạy cùng lệnh ở `scratch/m22-tree/` và `scratch/hint-tree/`.

### (1) Shell và mức kết luận fetch xanh

- **Workflow 71/73:** nguồn `secrets.GITHUB_TOKEN` qua TL_TOKEN đúng; `set -euo pipefail` có hiệu lực. Probe chạy nguyên shell từ đầu bước đến hết phép so NHAN==H, với repo fixture thật có S/H khác nhau. Cờ cuối là `ehuBc`, không có `x`.
- **97:** format `printf 'x-access-token:%s'` cố định, biến được quote, không thêm LF. Đo encoder nhận đúng n+15 bytes cho token n bytes; argv encoder chỉ `-w0`. Bash printf/echo đều được xác nhận là builtin. GNU base64 9.4 với -w0 không wrap; command substitution bỏ LF cuối nhưng không loại LF giữa chuỗi. Fixture 81/82/83 cho padding 0/2/1; m14/m15/m19 bị giết đúng chốt bytes.
- **98:** gán AUTH_B64 xong mới phát `::add-mask::`, trước Git. Probe HEAD chỉ có command mask trên stdout trước dòng POST_OK do reviewer thêm; stderr tiến độ Git không có token/base64 fixture. Đây là đo thứ tự/bytes command, chưa đo bộ che log Actions.
- **99–104:** dấu nối dòng tạo một simple command: COUNT=1/KEY_0/VALUE_0 được cấp tạm cho Git. Git 2.43.0 thực sự đọc chúng khi fetch và helper nhận header đúng. Scope `http.https://github.com/.extraheader` khớp URL `https://github.com/$TL_KHO`; dòng 80 chốt kho canonical. Host đối chứng không nhận header; key đổi host làm helper thiếu header, rc=128. Hai `-c protocol...` không ghi đè header; m11 HTTPS=never bị Git thật chặn trước helper.
- **105–107:** unset AUTH_B64 chạy sau fetch thành công; tiếp đó Git rev-parse thật và NHAN==H qua. Ở HEAD, AUTH_B64/COUNT/KEY_0/VALUE_0 đều không còn đặt sau khối. Header không đi vào Git rev-parse sau fetch hay child hậu kiểm. Nếu fetch rc=128, `-e` dừng trước unset/receipt; không có child hậu kiểm. Unset không phải xoá sạch memory.
- Lỗi encoder **9**, printf **8**, TL_TOKEN chưa đặt **1** đều dừng trước mask/fetch; lỗi fetch **128** dừng trước POST_OK. Pipefail giữ lỗi printf dù encoder vẫn có thể khởi động ở phía còn lại của pipe.

**ĐÚNG/ĐỦ:** HEAD sửa đúng phần cấp credential ở biên đã đo. Chưa thể kết luận fetch trên runner GitHub chắc chắn xanh. Probe dùng Git thật nhưng thay transport HTTPS bằng helper cục bộ: helper hỏi config Git thật và quảng bá ref; H đã có trong object store nên không truyền pack qua HTTP. Không đo libcurl trên dây, TLS, redirect, quyền/ref/token thật. Rc=128 của base/m5/m7/m16/host sai là helper fixture từ chối, không tái lập thông báo Username hoặc phản hồi GitHub. Đã đo binary 2.43.0 thuộc dải ≥2.31, chưa đo 2.31 hoặc mọi bản trong dải; GNU hiện có phù hợp -w0, chưa xác minh ảnh ubuntu-latest hiện hành. A3 sau land vẫn cần đo; không nâng giới hạn offline này thành finding.

### (2) Base64 có thể lộ ở đâu

| Bề mặt | Đo được / giới hạn |
|---|---|
| Log stdout/stderr | HEAD không xtrace, phát mask trước Git; không in thêm header/token. M12/m13 bị test giết vì stderr. Fixture lưu command mask thô do không có runner masker. |
| `::add-mask::` | Đăng ký giá trị để che log runner xử lý sau đó; không bảo vệ output trước đăng ký hoặc đảm bảo che mọi biểu diễn biến đổi. Không che argv, environment, stdin, memory, file hay artifact. Chỉ đo command/thứ tự, chưa đo masker thật. |
| argv | Git/helper HEAD không có token/base64; encoder chỉ nhận -w0, input qua pipe. Dạng (b) của spec có base64 trong argv và vẫn được t152 chấp nhận; HEAD dùng dạng (a). |
| Environment / ps | Helper, Git rev-list/maintenance thuộc fetch kế thừa COUNT/KEY/VALUE và TL_TOKEN. Phạm vi là **một lời gọi fetch cùng cây tiến trình con**. Tiến trình đủ quyền đọc environment có thể thấy credential; mask không che kênh này. Không quét ps/proc ngoài fixture. |
| Sau fetch | HEAD không còn ba biến config; TL_TOKEN thô vốn là env cả bước vẫn còn. M22 làm VALUE_0 có thêm ở Git rev-parse và child sau fetch: tồn dư base64 ngoài phạm vi M1, không chứng minh tăng quyền hoặc log thật bị lộ. |
| Config đĩa | `.git/config` fixture không đổi byte sau HEAD/m22; HEAD không gọi git config ghi auth. M3 bị giết ở (iii). |
| Curl | Workflow 118 đã có từ base truyền TL_TOKEN thô qua argv curl. Không phải bề mặt base64 mới do patch thêm. |
| Receipt | Workflow 121–141 và dict ở `ops/lease_publish.py:1772` không serialize TL_TOKEN/AUTH_B64/VALUE_0. Blob workflow được băm trước nội suy env. Đây là đọc mã, chưa đọc artifact/receipt thật hoặc chứng minh nội dung thực tế sạch. |

### (3)–(6) Test, lint, write set và EVIDENCE

T152 chạy Bash thật nhưng stub hàm Git cho fetch, dùng `command git config` làm oracle; không phải test HTTP. Bốn mutant A1 bị giết ở bốn chốt độc lập (i)/(ii)/(iii)/(iv). Base chưa có t152; phép ĐỎ trên nền là **hàm t152 HEAD đọc workflow base**, đúng phương pháp lời khai. T148 trên HEAD cũng XANH. Chốt mới kiểm nguồn env, còn thực thi cấp token giả: không mô phỏng engine biểu thức Actions.

Actionlint **1.7.7 có sẵn trong nguon/** được dùng, không tải. Debug xác nhận ShellCheck **0.9.0** chạy cả hai run block, không lỗi; ShellCheck riêng dùng `--norc --shell=bash -e SC2154` vì env cấp biến từ YAML. Pyflakes không có, không nhận tín dụng kiểm Python inline bằng pyflakes. Một lần gọi phiên bản gõ thiếu chữ đầu đường binary đã lỗi; lần chạy đúng đường và các gate sau đó đều rc=0, có log.

Toàn diff base..HEAD và đường theo từng commit chỉ có hai tệp write set. AST ngoài t152 không thay đổi; master mới không chạm write set. Không checkout/commit/đổi ref/chủ động ghi index trong clone. Mutant, repo fixture và HINT thử đều ở scratch.

EVIDENCE giữ +50/+79 ở các mục lịch sử, cập nhật +80 ở phần mới; không coi lịch sử là khai sai HEAD. Gen3/lượt2 khai áp nguyên HINT, m16 cũ sống/mới đỏ, m15/m14/m13/m8, suite và lint: số mới khớp. Reviewer chạy các mutant tác giả nói chưa chạy lại, không gán công ngược. EVIDENCE nói rõ chưa đo runner/mask thật, không khai A3 xong hay mọi mutant bị giết. M22 chứng minh thiếu độ phủ, không chứng minh tác giả khai gian gate. Lease/reroute, comment/run và mốc thời gian tác giả không xác minh được offline; chỉ thị trực tiếp gen3 “chạy đến hết P1, P2” được dùng, không đọc doctrine.

## Findings

### t152-bo-sot-header-env-con-sau-fetch [P2] Hậu kiểm bỏ sót VALUE_0 còn export sau fetch

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5427` chỉ hậu kiểm AUTH_B64 và GIT_CONFIG_COUNT. Điểm mutant là workflow **99–101** trong bản sao.
- **VẤN ĐỀ:** m22 dời `GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $AUTH_B64"` khỏi nhóm gán tạm thành một lệnh export riêng trước nhóm COUNT/KEY/Git. T152/t148 vẫn XANH; actionlint/ShellCheck rc=0; toàn suite **147/147, bỏ qua=0**. Git thật nhận đúng header, fetch rc=0 và NHAN==H, nhưng **VALUE_0 chứa toàn bộ header tiếp tục có trong env của Git rev-parse sau fetch và child hậu kiểm**. AUTH_B64/COUNT vắng không chứng minh VALUE_0 đã hết phạm vi. Đây là chốt lifetime độc lập của M1. HEAD không có tồn dư này, và COUNT vắng làm cấu hình hết hiệu lực trong Git sau đó; finding là credential tiếp tục được kế thừa, không phải Git tự gửi header lần hai.
- **ĐÃ THỬ VÁ:** HINT thay một dòng hậu kiểm bằng `test -z` trên chuỗi chỉ báo có đặt của AUTH_B64/COUNT/KEY_0/VALUE_0. Giữ oracle bytes/config/mask, ba fixture padding và nguồn env. Chỉ đổi t152, không tăng dòng: +69 test/+11 workflow = **+80/−0**. Dry-run/apply patch -p0 rc=0, đúng byte; AST ngoài t152 không đổi.
- **ĐÃ THỬ NGHIỆM:** m22 SỐNG với test HEAD và test 8726a1c, t148/lint XANH. Probe HEAD có `value=` sau fetch; m22 có `value=x`, VALUE_0 bằng header mong đợi ở chính Git rev-parse và child hậu kiểm. Cả hai rc=0, config đĩa không đổi, argv không chứa credential. HINT giết m22 đúng `(i)` rc=1 ở hậu kiểm; giữ HEAD/m17/dạng (b)/github.token/khoảng trắng XANH và base/m1–m16/m18–m21 GIẾT. **Suite m22: 147/147 rc=0; suite HINT: 147/147 rc=0; cả hai đã chạy=147, bỏ qua=0.**
- **ĐỘ TIN:** cao về mutant sống, env tồn dư và hiệu quả HINT. **P2 thiếu chốt phạm vi độc lập**: HEAD cấp đúng header/đúng phạm vi, t152 vẫn thực sự đo bytes tới Git. Không suy thành P1 HEAD lộ token, log runner chưa che hoặc fetch thật thất bại. M22 sống cả trước HINT nguồn env nên không phải lỗi mới do vá lượt trước.

Bằng chứng: [delta m22](scratch/logs/m22.patch), [t152/t148](scratch/logs/m22-initial.json), [Git/helper HEAD và m22](scratch/logs/runtime.json), [HINT/m22 cũ/lint](scratch/logs/hint-validation.json), [log suite m22](scratch/logs/m22-suite.log), [log suite HINT](scratch/logs/hint-suite.log). Script: [probe_runtime.py](scratch/probe_runtime.py), [validate_hint.py](scratch/validate_hint.py).

## Mutant đã chạy

Dựng từ bytes HEAD trong `scratch/mutants/`; m1–m4 theo A1, m5–m21 dựng lại theo verdict trước, m22 của reviewer lượt này. M2 dùng mẫu URL sẵn có trong spec. Không tạo nội dung đường dẫn thoát/khai thác.

| Mutant | Đột biến | t152 HEAD | Lý do / đối chứng | HINT |
|---|---|---|---|---|
| m1 | KEY_0 → http.postBuffer | **GIẾT** | (i), rc=1, thiếu header | GIẾT |
| m2 | URL credential mẫu A1 | **GIẾT** | (ii), URL chứa credential | GIẾT |
| m3 | Thêm git config local extraheader | **GIẾT** | (iii), lệnh ghi config | GIẾT |
| m4 | persist-credentials true | **GIẾT** | (iv), checkout sai | GIẾT |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; helper thiếu header rc=128 | GIẾT |
| m6 | VALUE_0 dummy | **GIẾT** | (i), header khác oracle | GIẾT |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), sai nguồn; helper rc=128 | GIẾT |
| m8 | Bỏ add-mask | **GIẾT** | (v), thiếu đăng ký mask | GIẾT |
| m9 | KEY http.extraheader toàn cục | **GIẾT** | (i), rc=94, host đối chứng nhận header | GIẾT |
| m10 | Fetch thứ hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Phát hiện 2 lời gọi fetch | GIẾT |
| m11 | HTTPS=never | **GIẾT** | (i), rc=95; Git thật chặn trước helper rc=128 | GIẾT |
| m12 | set -x trước AUTH_B64 | **GIẾT** | (v), stderr thừa | GIẾT |
| m13 | Thêm -x vào set đầu bước | **GIẾT** | (v), cờ shell đầu bước có hiệu lực | GIẾT |
| m14 | Bỏ -w0 | **GIẾT** | (i), wrap khác oracle | GIẾT |
| m15 | Bỏ padding = | **GIẾT** | (i), fixture có padding bắt được | GIẾT |
| m16 | env TL_TOKEN của bước fetch rỗng | **GIẾT** | (i), nguồn env; test 8726a1c SỐNG | GIẾT |
| m17 | Scope header riêng repo canonical | **SỐNG** | Biến thể hợp lệ; helper đúng header, host đối chứng không nhận | SỐNG, đúng |
| m18 | COUNT=2, không có KEY_1 | **GIẾT** | (i), rc=95, missing config key | GIẾT |
| m19 | printf thêm LF vào input encoder | **GIẾT** | (i), bytes header khác oracle | GIẾT |
| m20 | Bỏ unset AUTH_B64 | **GIẾT** | (i), rc=1, hậu kiểm biến AUTH | GIẾT |
| m21 | Dời add-mask xuống sau fetch | **GIẾT** | (i), thứ tự stdout sai, dòng cuối không phải header | GIẾT |
| **m22 mới** | **Dời VALUE_0 thành export riêng ngoài nhóm gán tạm** | **SỐNG** | **Đúng header nhưng tồn dư VALUE_0 ở tiến trình sau fetch** | **GIẾT (i), hậu kiểm phạm vi** |

**Tín dụng HEAD:** m1–m21 = **20 GIẾT / 1 SỐNG hợp lệ**; thêm m22 = **20 GIẾT / 2 SỐNG**, trong đó m22 là thiếu sót cần vá. **HINT = 21 GIẾT / 1 SỐNG hợp lệ**. Không nhận công HINT giết m22 cho PR hiện tại. Base, dạng (b), github.token, khác khoảng trắng, host sai và lỗi thực thi là đối chứng riêng, không cộng mẫu số. Mutant nội bộ của 146 ca cũ không gộp vào bảng.

## HINT và phạm vi

`HINT.patch`: unified diff **patch -p0 từ gốc cay-kho/**, đúng HEAD, **1 hunk/1 dòng**, chỉ `ops/lease_publish_test.py`. Đã dry-run và áp trong scratch, không áp vào clone. Giữ workflow và các ca cũ. Tổng diff sau HINT **+80/−0**; suite HINT **147/147**, rc=0.

Không mạng; không đọc tệp doctrine bị cấm hoặc tài liệu ngoài cwd; chỉ thực thi công cụ/runtime có sẵn. Không thao tác PR, canary hoặc land. Trần generation không được dùng để hạ chuẩn hay tạo thêm finding.

## chua_do_duoc

1. Fetch trên runner GitHub thật với quyền/token/ref kho thật; HTTP/TLS/redirect/libcurl trên dây và toàn job. A3 sau land chưa chạy. Rc helper fixture không phải tái lập lỗi Username/HTTP thật.
2. Secret masker Actions, log/artifact/receipt thật; check_run_id/workflow_definition_commit/workflow_definition_sha256/checker_rc. Command mask và đọc mã không thay readback.
3. Git 2.31/toàn dải 2.31+, ảnh ubuntu-latest hiện hành, Windows/macOS/BSD base64. Đã đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4, Python 3.11.15, actionlint 1.7.7, ShellCheck 0.9.0 tại đây.
4. Engine biểu thức Actions và token thật. Test nhận hai nguồn env được phép rồi cấp fixture; probe m16 cấp literal rỗng của YAML, không giả lập mọi cách kế thừa env hoặc phản hồi GitHub cho password rỗng.
5. Ps/environment/memory ngoài fixture hoặc bảo đảm unset xoá memory. Đo env do chính các tiến trình fixture báo; mask không bảo vệ kênh ấy. M22 không phải bằng chứng credential thật đã tới bên ngoài.
6. Timeline Issue/comment/run/lease/reroute và hành động lịch sử tác giả; không xác minh quyền sở hữu write set từ hệ thống live. So sánh Git dựa trên snapshot được cung cấp.
7. Wrapper tải mạng nguyên dạng, pyflakes và chạy suite trực tiếp trong clone có doctrine. Đã dùng gói offline/bản sao đủ ops/.github và nêu rõ phạm vi.

Hoàn tất: 2026-09-11T09:43:33Z; trong giới hạn 40 phút.
