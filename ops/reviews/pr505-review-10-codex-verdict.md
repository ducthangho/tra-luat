verdict: approve
reviewed_sha: de49fa0d077a2a00e9f936240378979a8ebc080c
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: 87b85d00ce4627d8f09f1317b72157ead712a99ef20e10f4bd5ebe3d81f9a38b
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 10
review_generation: 4; lượt 1
review_class: sensitive

**Approve: 0 P1, 0 P2 được xác nhận.** Finding gen3/lượt3 **ĐÃ VÁ THẬT**. HEAD cấp đúng header, đúng phạm vi một lời gọi fetch cùng cây tiến trình con trong phép đo offline. Suite và wrapper đều **147/147, bỏ qua=0**; actionlint/ShellCheck sạch. Trong m1–m34: **33 GIẾT, 1 SỐNG hợp lệ (m17)**. Không tìm được mutant âm sống thêm; không suy từ đó rằng mọi đột biến đều bị bắt.

Áp dụng điều kiện dừng generation 4 do người dùng cung cấp: chỉ chặn khi có P1 hoặc P2 workflow đủ bằng chứng; P2 thuần fixture sẽ ghi nợ. Lượt này không có finding mới đủ bằng chứng ở cả hai nhóm. Kết luận không dựa vào số vòng đã qua và không xác nhận nghiệm thu A3 trên runner thật.

Bắt đầu theo yêu cầu: 2026-09-11T10:34:31Z. Đã ghi VERDICT sớm rồi bổ sung; mọi số thực thi bên dưới được đo mới ở lượt 10.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đọc verdict/HINT gen3/lượt3 trước tiên; so hunk và chạy m23 cùng m1–m22, m24–m26 trước khi làm lại các mục (1)–(6). Chỉ đọc thêm test/spec để dựng phép đối chiếu.

- `nguon/VERDICT.rvm9-9.md`: **8623f20bad8a67cc08558c26d63d0f026b6224d7f7a31f149dbd71170cdd22c1**, khớp.
- `nguon/HINT.rvm9-9.patch`: **67a3b7d5cf558103ee080931efaf8457d1021e85a5cd3cc4eb75b6a23c77bccc**, khớp tiền tố được giao.

Slug `t152-fixture-bo-sot-token-lan-hoa-thuong` [P2]: **ĐÃ VÁ THẬT**.

| Phép đối chiếu tự đo | Kết quả |
|---|---|
| `git diff 3ae4f61..HEAD` so HINT | Đúng một hunk, một literal; tọa độ/thân hunk bằng nhau, Git chỉ thêm tên hàm sau `@@` |
| Áp HINT lên test 3ae4f61 trong scratch | `patch -p0` rc=0; toàn tệp sau áp trùng byte HEAD |
| Kích thước tệp | Cũ/mới đều **304776 bytes**; chạy `python3 -B`, không nạp cache |
| Delta còn lại | Workflow không đổi; đúng một commit mới |
| m23 với test 3ae4f61 | **SỐNG**, t152 XANH |
| m23 với test HEAD | **GIẾT (i)**: Git không nhận header hiệu lực dẫn từ TL_TOKEN |
| Toàn m1–m26 đo mới | **25 GIẾT / 1 SỐNG hợp lệ (m17)** |
| Kiểm độc lập bằng Git/helper | HEAD với token lẫn hoa/thường fetch rc=0, nhận H; m23 header sai byte, helper từ chối rc=128 |

Không có bằng chứng vá hờ hoặc vá sinh lỗi mới. Tác giả áp nguyên HINT được cung cấp, không sửa khác trong delta này.

Bằng chứng: [so HINT](scratch/logs/prior-hint.json), [delta](scratch/logs/prior-delta.patch), [m1–m26](scratch/logs/prior-mutants.json), [runtime](scratch/logs/runtime.json). Script [review.py](scratch/review.py) trích nguyên AST hàm t152 và các helper cần thiết từ nguồn từng phiên bản; đã đối chứng với nạp cả module HEAD, cùng XANH.

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 10 | Khớp? |
|---|---|---|---|
| Spec đóng băng | b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường spec trong clone không tồn tại | Khớp bản cung cấp |
| Head/base | de49fa0d / 27c413c3 | Đúng SHA đầy đủ đầu verdict | Có |
| Nguyên HINT, workflow không đổi | Một literal, một commit | Apply trùng byte; workflow còn trùng byte head lượt 1 `62c299a` | Có |
| Write set | +11 workflow/+69 test, −0 | **2 tệp, +80/−0**; từng commit base..HEAD cũng chỉ chạm hai đường | Có |
| Master đi tiếp | Prompt nêu e82af37 | Ref cục bộ thực tế **0bf0ba7e926cdd3e189c7ae89cba5894becd3ecd**; e82af37 là tổ tiên | Lệch mốc trong prompt |
| Master không chạm write set | Diff hai tệp rỗng | `git diff --stat 27c413c3..origin/master -- <hai tệp>` **rỗng** | Có; không kích hoạt S4 |
| Ca cũ / whitespace | Không đổi / sạch | AST bỏ t152 bằng base; bỏ đoạn thêm cùng separator cho bytes cũ bằng nhau; `git diff --check` rc=0 | Có |
| t152 nền | ĐỎ đúng (i) | Hàm HEAD đọc workflow base: **(i) đoạn auth/fetch không chạy được: rc=1** | Có |
| t152/t148 HEAD | QUA | Gọi riêng cả hai từ module HEAD: **XANH** | Có |
| m23 cũ/mới | SỐNG/GIẾT | Đúng cả hai đối chứng | Có |
| m16/m15/m13/m8 | ĐỎ (i)/(i)/(v)/(v) | Đúng các chốt tác giả khai | Có |
| Các mutant tác giả chưa chạy lại | EVIDENCE liệt kê rõ | Reviewer đo mới toàn m1–m26 | Không gán công reviewer cho tác giả |
| Suite HEAD | 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, bản sao đủ ops/.github |
| Wrapper A2 | AL_VER=1.7.7, 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, đường cài gói offline |
| Lint | actionlint + shellcheck rc=0 | **actionlint 1.7.7 / ShellCheck 0.9.0**, rc=0; hai run block được kiểm | Có |
| Credential đến Git | Header Basic từ TL_TOKEN | Git **2.43.0** fetch thật tới helper HTTPS cục bộ; config theo URL đúng byte, host đối chứng không nhận | Có tại biên config/helper |
| Fetch nhận H | Khắc phục thiếu auth | H thiếu trước fetch; **pack-objects/unpack-objects truyền object**, ref nhận đúng H, shell `NHAN==TL_H` qua | Có offline; chưa HTTP |
| Phạm vi / argv / đĩa | Một lời gọi, không config/URL/argv chứa credential mới | Một helper; argv Git/helper/encoder/Trace2 không có token/base64; config repo không đổi; bốn biến auth/config vắng sau fetch | Có trong probe |
| Shell/encoder | -euo pipefail, GNU -w0, mask trước, unset sau | Byte input/output đúng ở token dài **16/42/43/81/82/83/160**; lỗi encoder/printf/fetch/token vắng đều dừng | Có trên runtime tại đây |
| Mutant mới m27–m34 | Reviewer tìm thêm ngoài bốn ca A1 | **8 GIẾT**, đúng chốt (i) | Không tìm được mutant âm sống thêm |
| Đối chứng dương bổ sung | Không khóa cứng cú pháp dạng (a) | Dạng (b), nguồn github.token, `--wrap=0`, port mặc định :443 đều **SỐNG hợp lệ** | Có |
| Tính toàn vẹn clone | Read-only ở mức git | Hai tệp gốc giữ đúng hash, working diff hai đường rỗng; bản sao trùng byte | Có |

Bằng chứng: [metadata](scratch/logs/metadata.json), [full diff](scratch/logs/full-diff.patch), [controls](scratch/logs/controls.json), [suite](scratch/logs/suite.json), [log suite](scratch/logs/suite.log), [wrapper](scratch/logs/wrapper.json), [lint](scratch/logs/lint.json), [actionlint debug](scratch/logs/actionlint.log), [runtime](scratch/logs/runtime.json), [độ dài](scratch/logs/runtime-lengths.json), [mutant mới](scratch/logs/extra-mutants.json), [kiểm cuối](scratch/logs/final-checks.json).

**Cách chạy:** `python3 ops/lease_publish_test.py` tại `scratch/head-tree/`, bản sao đầy đủ `ops/` và `.github/`. T82 ở test:2778 sao cả `HERE.parent`, nên chạy trực tiếp trong clone sẽ sao các tệp bị cấm đọc. Bản sao giữ đầy đủ workflows; không cho ca tự qua vì thiếu thư mục. Không có symlink trong hai cây nguồn đã sao, không có cache Python trong bản sao; `PYTHONDONTWRITEBYTECODE=1` và TMPDIR trong scratch. Git system/global config được cô lập. Wrapper chạy `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` với `AL_GOI` trỏ gói cung cấp `nguon/actionlint/goi.gz`, `AL_DICH`/RUNNER_TEMP trong scratch, `TAR_OPTIONS=--no-same-owner`. Gói có sha256 **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**. Không chạy đường tải mạng.

### (1) Shell và mức kết luận fetch xanh

- **Workflow 71/73:** TL_TOKEN của bước lấy `secrets.GITHUB_TOKEN`; shell bật `set -euo pipefail`. Probe chạy nguyên shell từ đầu bước qua phép so NHAN==H; cờ cuối **ehuB**, không có `x`.
- **97:** `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định và quote biến. Đo encoder nhận đúng **15+n bytes**, không LF thêm; argv encoder chỉ `-w0`. `printf` và `echo` là Bash builtin tại đây. GNU base64 **9.4** nhận `-w0`, không wrap; output khớp Python base64 ở bảy độ dài, gồm các nhánh padding 0/2/1. Command substitution loại LF cuối output, không sửa LF nằm giữa output; m14/m19 làm sai bytes và bị bắt.
- **98:** Gán AUTH_B64 thành công rồi mới phát command `::add-mask::`, trước lời gọi Git. HEAD chỉ in command mask ở phần auth; dòng POST/CHILD là quan sát viên do reviewer thêm sau khối. Stderr tiến độ fetch không chứa token/base64 fixture. Đây là đo thứ tự shell, chưa đo runner xử lý mask.
- **99–104:** Ba phép gán và các dấu nối dòng thuộc cùng một simple command Git. COUNT=1 chọn KEY_0/VALUE_0, header scoped `http.https://github.com/.extraheader` khớp endpoint `https://github.com/$TL_KHO`; dòng 80 đã chốt kho canonical. Git **2.43.0** thực sự đọc cấu hình env trong fetch; helper hỏi config Git thật và nhận đúng header. Host đối chứng không nhận; m24 đổi host key làm endpoint canonical thiếu header. Hai `-c protocol…` không ghi đè header; m11 HTTPS=never bị Git thật chặn trước helper.
- **105–107:** Sau fetch thành công, unset AUTH_B64 rồi Git rev-parse thật và so NHAN==H. HEAD không còn AUTH_B64/COUNT/KEY_0/VALUE_0 trong shell hậu kiểm, Git rev-parse sau fetch hoặc child hậu kiểm. Khi fetch lỗi, `-e` dừng trước unset và trước các bước sau; shell không tiếp tục tạo receipt. Unset không chứng minh xóa sạch mọi bản sao trong memory.
- **Đường lỗi đo riêng:** encoder rc=**9**, printf rc=**8**, token chưa đặt rc=**1** đều dừng trước mask/fetch; fetch rc=**128** dừng trước POST. Với printf lỗi, pipefail bảo toàn lỗi dù encoder bên phải pipe vẫn có thể chạy. Không dùng header dở dang trong các đối chứng này.

**ĐÚNG/ĐỦ tại phạm vi đã đo:** HEAD sửa đúng phần thiếu credential, không thấy lỗi shell/config khiến bản vá chắc chắn fetch đỏ. Kết luận fetch xanh trên runner thật còn phụ thuộc token/quyền/ref/server và các chốt còn lại của job. Không thể xác nhận các điều kiện ấy offline.

Probe giữ nguyên URL HTTPS canonical nhưng thay `git-remote-https` bằng helper cục bộ kiểm header rồi nối `git upload-pack` qua pipe. Git thật truyền pack từ server fixture có H sang client chỉ có S. **Không đi qua libcurl/HTTP/TLS/GitHub.** Rc=128 ở base/m5/m7/m23/m24 là helper từ chối header thiếu/sai, không tái lập lỗi Username hoặc phản hồi GitHub thật. M11 bị protocol policy của Git chặn. Chỉ đo một binary **2.43.0** thuộc dải ≥2.31; không nhận đã đo 2.31/toàn dải hoặc ảnh ubuntu-latest hiện hành. A3 sau land vẫn chưa hoàn thành.

Script tái lập: [probe.py](scratch/probe.py); [Trace2 HEAD](scratch/runtime/head/trace.jsonl).

### (2) Base64 có thể lộ ở đâu

| Bề mặt | Kết quả và giới hạn |
|---|---|
| Log stdout/stderr | HEAD không bật xtrace, phát mask trước Git, không in thêm credential trong probe. M12/m13 bị t152 giết do stderr thừa. Log offline của reviewer chứa command mask thô với **token giả**, vì không có Actions masker. |
| `::add-mask::` | Command yêu cầu runner đăng ký giá trị để che các log được xử lý sau đó. Không che ngược log trước đăng ký; không bảo đảm che mọi dạng đã biến đổi của giá trị. Chưa thực thi bộ masker thật nên không nhận chứng minh log Actions sạch. |
| argv / ps | Argv Git/helper/encoder và các argv Trace2 đã thu không chứa token/base64 HEAD. Bash builtin printf không tạo một external printf mang token qua argv. Không quét ps hoặc đọc proc ngoài cwd. Một tiến trình đủ quyền đọc environment vẫn có thể thấy credential; mask không bảo vệ argv/environment/pipe/memory. |
| Environment | Git fetch, helper và các tiến trình con nhận VALUE_0 đầy đủ; TL_TOKEN thô vốn là env cả bước. “Một tiến trình” trong comment thực tế là **một lời gọi fetch cùng cây con**, không chỉ một PID. Bốn biến auth/config mới vắng sau fetch thành công; TL_TOKEN thô vẫn còn theo env của bước. |
| Config đĩa / URL | Config repo fixture trước/sau trùng byte. Workflow không có lệnh ghi auth config; m3 bị bắt riêng. URL fetch không có credential. Mask không có tác dụng với file/artifact. |
| Dạng (b) | Spec yêu cầu t152 nhận `git -c …extraheader=…`, và đối chứng này XANH. Dạng đó đặt base64 vào argv; không được gán tính “không argv” của HEAD dạng (a) cho nó. |
| Curl có sẵn | Workflow:118 truyền **TL_TOKEN thô** trong argv curl; dòng này có từ base. Không phải bề mặt base64 mới do 11 dòng patch thêm. |
| Receipt | Dict ở `ops/lease_publish.py:1772` và phần bổ sung workflow:121–141 không serialize TL_TOKEN/AUTH_B64/VALUE_0. Băm workflow lấy blob trước nội suy shell. Đây là đọc mã, chưa đọc receipt/artifact thật và không chứng minh toàn nội dung artifact thực tế sạch. |

### (3)–(6) Test, lint, write set và EVIDENCE

T152 chạy Bash thật từ đầu bước nhưng thay Git fetch bằng shell function; trong đó `command git config` là oracle cấu hình theo URL. Test đo bytes đến cấu hình Git, không đo xác thực HTTP hay engine biểu thức Actions. Base chưa có t152; đối chứng nền ở đây là **hàm t152 HEAD đọc workflow base**, đúng ý thiếu header ở (i).

Bốn mutant A1 được giết riêng ở **(i)/(ii)/(iii)/(iv)**. Ba gợi ý “mutant thứ năm” COUNT sai, nguồn TL_KHO, fetch lần hai đều bị giết (m5/m7/m10). Reviewer thử thêm m27–m34, cả tám bị giết. **Không tìm được mutant âm sống thứ năm**; đây là kết quả tìm kiếm có giới hạn, không thay bằng tuyên bố “đã tìm” hoặc dùng một biến thể hợp lệ làm finding. Các SỐNG hợp lệ được ghi đầy đủ bên dưới.

Actionlint **1.7.7 từ nguon/**, ShellCheck **0.9.0 trên PATH**: debug xác nhận gọi ShellCheck cho cả hai run block, 0 lỗi. ShellCheck riêng trên shell trích từ YAML cũng rc=0, dùng `--norc --shell=bash -e SC2154` để nhận biến được YAML cấp. Pyflakes không có, không nhận tín dụng kiểm Python inline bằng pyflakes.

Toàn diff base..HEAD và danh sách đường theo từng commit chỉ có hai tệp write set. Không thay checkout/ref/index/commit trong clone; mọi mutant và repo fixture ở scratch. Master cục bộ đã tiến thêm từ e82af37, chỉ các đường changelog/manifest/reviews trong đoạn mới ấy; diff toàn base..master ở hai tệp review vẫn rỗng. Không coi lệch mốc mô tả trong prompt là finding sản phẩm hoặc lời khai sai của EVIDENCE.

EVIDENCE giữ các số +50/+79 trong phần lịch sử, rồi cập nhật +80 ở phần mới; không dùng số lịch sử làm số HEAD. Phần gen4/lượt1 khai nguyên HINT, workflow không đổi, m23 cũ sống/mới đỏ, m16/m15/m13/m8, suite/lint: **khớp phép đo mới**. Tác giả nêu rõ chưa chạy lại các mutant khác; reviewer đã chạy, không gán công ngược. EVIDENCE nói rõ chưa đo runner/mask thật, không khai A3 hoàn thành hay giết mọi mutant. Không xác minh độc lập được lịch sử chạy của tác giả, sự cố bytecode trong lần đo đầu, lease/reroute/comment/run hoặc quyền cấp lease từ dữ liệu live; những điều đó là lời khai được cung cấp.

## Findings

**Không có finding P1/P2/P3 mới đủ bằng chứng.** Finding duy nhất cần đối chiếu từ lượt trước đã vá thật như mục đầu. Giới hạn offline và việc không tìm được mutant âm sống thêm không được nâng thành finding.

## Mutant đã chạy

M1–m4 theo §A1, m5–m26 dựng lại từ các verdict được cung cấp, m27–m34 reviewer lượt 10. Mỗi bản dựng độc lập từ bytes HEAD trong `scratch/mutants/`, có delta riêng tại `scratch/logs/mN.patch`. M2 dùng mẫu credential URL đã có trong spec. Không tạo mẫu đường dẫn thoát/khai thác.

| Mutant | Đột biến | t152 HEAD | Lý do / đối chứng |
|---|---|---|---|
| m1 | KEY_0 → http.postBuffer | **GIẾT** | (i) rc=1, thiếu header |
| m2 | URL credential mẫu A1 | **GIẾT** | (ii), URL chứa credential |
| m3 | Thêm git config local extraheader | **GIẾT** | (iii), lệnh ghi config |
| m4 | persist-credentials true | **GIẾT** | (iv), checkout sai |
| m5 | COUNT=0 | **GIẾT** | (i) rc=1; helper thiếu header, rc=128 |
| m6 | VALUE_0 dummy | **GIẾT** | (i), khác header oracle |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), sai nguồn; helper rc=128 |
| m8 | Bỏ add-mask | **GIẾT** | (v), thiếu mask |
| m9 | KEY http.extraheader toàn cục | **GIẾT** | (i) rc=94, host đối chứng nhận header |
| m10 | Fetch thứ hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Đếm hai lời gọi fetch |
| m11 | HTTPS=never | **GIẾT** | (i) rc=95; Git thật chặn trước helper, rc=128 |
| m12 | set -x trước AUTH_B64 | **GIẾT** | (v), stderr thừa |
| m13 | Thêm -x vào set đầu bước | **GIẾT** | (v), cờ trước WF_BLOB có hiệu lực |
| m14 | Bỏ -w0 | **GIẾT** | (i), wrap khác oracle |
| m15 | Bỏ padding = | **GIẾT** | (i), fixture có padding |
| m16 | Env TL_TOKEN của bước rỗng | **GIẾT** | (i), nguồn env không hợp lệ |
| m17 | Scope header riêng repo canonical | **SỐNG** | **Biến thể hợp lệ**; Git/helper nhận đúng header, fetch rc=0, host đối chứng không nhận |
| m18 | COUNT=2, thiếu KEY_1 | **GIẾT** | (i) rc=95, missing config key |
| m19 | printf thêm LF trước encoder | **GIẾT** | (i), sai bytes |
| m20 | Bỏ unset AUTH_B64 | **GIẾT** | (i) rc=1, hậu kiểm biến |
| m21 | Dời mask sau fetch | **GIẾT** | (i), thứ tự stdout sai |
| m22 | Export VALUE_0 riêng trước nhóm gán | **GIẾT** | (i) rc=1, hậu kiểm tồn dư biến |
| m23 | Hạ TL_TOKEN thành chữ thường | **GIẾT** | (i), fixture lẫn hoa/thường; test 3ae4f61 SỐNG |
| m24 | Scope header sang host đối chứng | **GIẾT** | (i) rc=1; helper URL canonical thiếu header |
| m25 | Basic → Bearer | **GIẾT** | (i), khác header oracle |
| m26 | Export KEY_0 riêng trước nhóm gán | **GIẾT** | (i) rc=1, hậu kiểm tồn dư biến |
| m27 mới | Mất dấu nối dòng sau COUNT | **GIẾT** | (i) rc=1, COUNT không đến Git config |
| m28 mới | AUTHORIZATION → PROXY-AUTHORIZATION | **GIẾT** | (i), sai tên header |
| m29 mới | VALUE_0 chỉ còn base64 | **GIẾT** | (i), thiếu tên header/scheme |
| m30 mới | Unset AUTH_B64 trước fetch | **GIẾT** | (i) rc=1, unbound variable |
| m31 mới | Username x-access-token → token | **GIẾT** | (i), sai bytes đầu vào Basic |
| m32 mới | Cắt TL_TOKEN còn 40 ký tự | **GIẾT** | (i), header khác token gốc |
| m33 mới | Encode base64 hai lần | **GIẾT** | (i), sai header |
| m34 mới | Mất dấu nối dòng sau VALUE_0 | **GIẾT** | (i) rc=1, env không đến Git |

**Tín dụng HEAD:** m1–m26 = **25 GIẾT / 1 SỐNG hợp lệ**; m1–m34 = **33 GIẾT / 1 SỐNG hợp lệ**. Không có mutant âm sống đã xác nhận trong tập này. Không nhận công “giết” m17.

Đối chứng ngoài mẫu số: HEAD XANH; base ĐỎ (i); dạng (b) dùng `-c`, nguồn `github.token`, encoder `--wrap=0` và scope header có port mặc định `:443` đều **SỐNG hợp lệ**. Không gộp các mutant nội bộ của 146 ca cũ vào bảng này.

Bằng chứng: [m1–m26](scratch/logs/prior-mutants.json), [m27–m34 và đối chứng dương](scratch/logs/extra-mutants.json). Script [extra.py](scratch/extra.py).

## NỢ GHI SANG #499

Không có P2 fixture mới được xác nhận để ghi nợ lượt này. **A3/M3 đã có vẫn chưa đo:** canary trên PR đầu tiên sau land và readback receipt/log/mask thật. Đây là nghĩa vụ nghiệm thu còn lại của spec, không phải finding mới hoặc bằng chứng đã hoàn thành.

## HINT và phạm vi

`HINT.patch`: **0 hunk**, kèm ghi chú không có P1/P2 cần vá. Không có bản vá đề nghị để apply/dry-run. Không sửa workflow hoặc test trong clone.

Không mạng, không đọc tệp doctrine bị cấm hay tài liệu ngoài cwd; chỉ chạy công cụ/runtime có sẵn. Không gọi ứng dụng ngoài, không gửi review/PR/comment, không canary/land. Phép đọc receipt giới hạn ở mã nguồn được nêu, không đọc dữ liệu live.

## chua_do_duoc

1. Fetch trên runner GitHub thật với token/quyền/ref kho thật; libcurl/HTTP/TLS/redirect và toàn job. Lỗi Username gốc là log được cung cấp trong spec, chưa tái lập trực tiếp; helper offline chỉ chứng minh header thiếu/sai và chuyển pack có kiểm oracle.
2. Bộ secret masker Actions, log/artifact/receipt thật; các trường check_run_id, workflow_definition_commit, workflow_definition_sha256, checker_rc từ run thật. A3 sau land chưa chạy.
3. Binary Git 2.31 hoặc mọi bản ≥2.31, ảnh ubuntu-latest hiện hành và base64 BSD/Windows. Đã đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4, Python 3.11.15, actionlint 1.7.7, ShellCheck 0.9.0 tại đây.
4. Engine biểu thức Actions và token thật. Test nhận hai nguồn env được spec cho phép rồi cấp fixture; không mô phỏng mọi trạng thái môi trường runner hoặc định dạng token hiện hành.
5. Ps/proc/environment/memory ngoài fixture; không chứng minh unset xóa mọi bản sao memory. Argv/env được đo từ chính các tiến trình fixture và Trace2. Command mask không bảo vệ những kênh ngoài log.
6. Timeline/lease/reroute/Issue/comment/run và lịch sử thao tác tác giả. Dùng chỉ thị generation 4 trực tiếp của người dùng; không xác minh live hoặc đọc doctrine.
7. Wrapper theo đường tải mạng, pyflakes, và suite trực tiếp trong clone có doctrine. Đã chạy đường gói offline và bản sao đủ ops/.github, nêu rõ giới hạn.
8. **Chưa tìm được mutant âm sống thứ năm ngoài bốn A1** dù đã đo lại các gợi ý m5/m7/m10 và thử mới m27–m34. Các biến thể sống đo được là hợp lệ; không biến chúng thành finding. Tập đột biến hữu hạn không chứng minh test hoàn chỉnh.

Hoàn tất các phép đo: 2026-09-11T10:45:44Z; chốt hồ sơ trong giới hạn 40 phút.
