verdict: changes_requested
reviewed_sha: 8726a1c91ac913da041ed021cc787c71ab57ffc6
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: 42a7ac85709a3630d759738cd3214684f42b77d43f45f22faca6aff2727c90e7
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 7
review_generation: 3; lượt 1
review_class: sensitive
hint_sha256: b9e367abeec69f95296265d870b0aa4c90999c373279834ea8a0739f0eb27e53

**0 P1, 1 P2 sửa được trong write set.** Finding padding lượt trước **ĐÃ VÁ THẬT**. Workflow HEAD tạo và truyền đúng header trong phép đo offline. Tuy nhiên, m16 xoá nguồn token của bước fetch bằng cách đặt `env.TL_TOKEN` rỗng vẫn qua t152/t148, lint và toàn suite 147/147: test luôn tự cấp token giả mà chưa kiểm nguồn env trong YAML. HINT bổ sung chốt này trong riêng t152, giữ tổng diff +80/−0. Không có bằng chứng HEAD fetch đỏ hay token thật bị lộ trên runner.

Bắt đầu theo yêu cầu: 2026-09-11T09:08:53Z. Cập nhật: 2026-09-11T09:22:19Z. Hoàn tất trong giới hạn 40 phút.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc và băm verdict/HINT gen2 lượt 3 trước các mục (1)–(6), rồi dựng và chạy m15 trước, tiếp theo m1–m14. Tất cả số dưới đây được đo lại trong lượt 7.

- `nguon/VERDICT.rvm9-6.md`: **e7871b29012d78b95acd2a50f5f9551051efc3380cea80288d9caf3348db7f9d** — khớp.
- `nguon/HINT.rvm9-6.patch`: **a7b0abc6cab235abaedf50cd2d692155074a484404df343cdb821b94c644f7f5** — khớp tiền tố được cấp.

Slug `t152-fixture-mat-nhanh-padding-base64` [P2]: **ĐÃ VÁ THẬT**.

| Phép đối chiếu tự đo | Kết quả |
|---|---|
| `git diff 301aac8..HEAD` với HINT | Đúng một hunk, tọa độ và thân hunk bằng nhau; chỉ khác tên hàm Git thêm sau `@@` |
| Áp HINT lên test 301aac8 trong scratch | `patch -p0` rc=0; cả tệp kết quả trùng byte HEAD |
| Workflow so 301aac8 | Không đổi byte |
| m15 bỏ padding | Test 301aac8 **SỐNG**; test HEAD **GIẾT (i)** |
| m1–m14 dựng lại trên HEAD | **14/14 GIẾT**, giữ các chốt độc lập |
| Fixture mới | Ba token 81/82/83 ký tự; input 96/97/98 bytes; padding 0/2/1; cả ba vượt ngưỡng wrap 76 |

Tác giả áp nguyên HINT, không sửa khác. M16 cũng SỐNG với test 301aac8 khi chạy lại: lỗ nguồn env còn sót, **không phải hồi quy do hunk padding**. Không đổi kết luận “ĐÃ VÁ THẬT” của slug cũ vì finding độc lập mới.

Bằng chứng: [so HINT](scratch/logs/prior-hint.json), [delta thực](scratch/logs/prior-delta.patch), [m1–m15](scratch/logs/prior-mutants.json), [m16 với test cũ](scratch/logs/old-m16-t148.json).

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 7 | Khớp? |
|---|---|---|---|
| Spec đóng băng | SHA256 b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường trong clone không tồn tại | Khớp bản cung cấp |
| Head/base | 8726a1c / 27c413c3 | Đúng SHA đầy đủ đầu verdict | Có |
| Delta gen3 lượt1 | Áp nguyên HINT, một commit, không đổi workflow | Một hunk, apply trùng byte; một commit mới | Có |
| Write set | 2 tệp, workflow +11/test +69, −0 | **2 tệp, +80/−0**; từng commit từ base chỉ chạm hai đường này | Có |
| `origin/master` | Prompt nói 26e2555 | Thực tế **e82af37fe66629d5378ac56fc689e24db26594fa** | SHA lời nhắc đã cũ |
| Master không chạm write set | Diff hai tệp phải rỗng | `git diff --stat 27c413c3..origin/master -- <hai tệp>` rỗng | Có; không kích hoạt điều kiện chồng tệp |
| t152 trên nền | ĐỎ đúng (i) | Hàm t152 HEAD đọc workflow 27c413c3: `TinHieuChotCa`, `(i) đoạn auth/fetch không chạy được: rc=1` | Có; base chưa có t152 |
| t152/t148 HEAD | XANH | Cả hai gọi riêng đều XANH | Có |
| m15 cũ/mới | XANH / ĐỎ (i) | Đúng cả hai đối chứng | Có |
| m14/m13/m5/m8 | Tác giả nói đã chạy lại | ĐỎ đúng (i)/(v)/(i) rc=1/(v) | Có |
| Các mutant trước còn lại | Tác giả nói chưa chạy lại ở lượt này | Reviewer tự dựng và chạy; m1–m15 đều GIẾT | Không gán số reviewer cho tác giả |
| Suite HEAD | 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, bản sao nêu dưới |
| Wrapper HEAD | AL_VER=1.7.7, 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0; AL_GOI cục bộ | Có ở đường offline |
| Lint workflow | actionlint + shellcheck rc=0 | **1.7.7 / 0.9.0**, rc=0; debug xác nhận ShellCheck chạy cả hai run block; ShellCheck riêng rc=0 | Có |
| Ca cũ, whitespace | Không đổi / sạch | AST bỏ t152: base=HEAD=HINT; `git diff --check` rc=0 | Có |
| Auth tới fetch | Header từ TL_TOKEN, URL canonical | Git **2.43.0 fetch thật** qua helper HTTPS cục bộ nhận đúng header; HEAD rc=0, NHAN==TL_H | Có ở biên helper/config |
| Phạm vi, argv, đĩa | Một lời gọi Git, không token trong argv/URL/config đĩa | Một helper; argv Git/helper không token/base64; config repo không đổi; helper kế thừa header qua env | Có; phạm vi gồm cây tiến trình con |
| Shell/encoder | -euo pipefail, GNU -w0, mask trước, unset sau | Bytes đúng với token dài 16/42/43/81/82/83/160; thành công qua hậu kiểm unset; lỗi printf/encoder/Git dừng | Có tại Linux này |
| Mutant mới m16 | Reviewer tìm ca sống ngoài A1 | TL_TOKEN rỗng trong YAML: **t152/t148 SỐNG**, lint rc=0, **suite 147/147 rc=0** | P2 nguồn env chưa được kiểm |
| M16 với env theo YAML | Không khai trong EVIDENCE | Header giải mã thành `x-access-token:`; helper đòi token fixture nên từ chối, Git rc=128 | Đo offline, không phải GitHub HTTP |
| HINT | Chỉ hai tệp cho phép, ≤80 dòng thêm | 2 hunk, riêng test; dry-run/apply rc=0, byte đúng; vẫn +69 test/+11 workflow = **+80/−0** | Có |
| Ma trận HINT | Giữ dương, giết âm | HEAD/dạng (b)/scope repo/nguồn github.token XANH; base/m1–m16/m18–m21 GIẾT | Có |
| Suite HINT | Không hồi quy | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |

Bằng chứng: [metadata](scratch/logs/metadata.json), [suite HEAD](scratch/logs/suite.json), [log suite](scratch/logs/suite.log), [wrapper](scratch/logs/wrapper.json), [log wrapper](scratch/logs/wrapper.log), [lint/versions](scratch/logs/lint-and-versions.json), [debug actionlint](scratch/logs/actionlint.log), [runtime Git](scratch/logs/runtime.json), [controls](scratch/logs/controls.json), [m16 runtime](scratch/logs/m16-runtime.json), [suite m16](scratch/logs/m16-suite.json), [log m16](scratch/logs/m16-suite.log), [HINT](scratch/logs/hint-validation.json).

**Cách chạy suite:** lệnh `python3 ops/lease_publish_test.py` chạy ở `scratch/head-tree/`, bản sao `ops/` và `.github/`; hai tệp review trùng băm clone. T82 gọi `copytree(HERE.parent, …)` nên chạy trực tiếp trong clone sẽ sao cả các tệp người dùng cấm đọc. Bản sao có đủ workflows, không cho ca tự qua do thiếu workflow. TMPDIR nằm trong `scratch/tmp/`, tắt bytecode; không copy doctrine. Wrapper chạy `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh`, `AL_GOI=nguon/actionlint/goi.gz` qua đường tuyệt đối, gói SHA256 **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**, đích cài trong scratch và `TAR_OPTIONS=--no-same-owner`. Không gọi đây là kiểm đường tải mạng.

### (1) Shell, Git và mức kết luận fetch

- **Workflow 71/73:** HEAD cấp `TL_TOKEN: ${{ secrets.GITHUB_TOKEN }}` và chạy `set -euo pipefail`. Probe chạy bytes từ đầu bước tới sau phép so NHAN, với repo fixture thật có S/H khác nhau; trạng thái cuối có `ehuBc`, không có `x`.
- **97:** `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định, quote biến, không thêm LF. Bash builtin printf đưa dữ liệu qua pipe; encoder GNU base64 9.4 chỉ nhận argv `-w0`. Với ba fixture HEAD, Python oracle và header Git khớp ở cả padding 0/2/1. Command substitution loại LF cuối, giữ LF bên trong; -w0 tránh wrap bên trong. M14 và m19 thêm LF vào input đều bị giết.
- **98:** echo builtin phát command đăng ký mask **sau khi gán, trước Git**. Chuỗi HEAD một dòng. Đây là số đo thứ tự/bytes phát command, chưa phải phép đo bộ che log Actions.
- **99–104:** ba phép gán có continuation thuộc cùng simple command Git. COUNT=1 chọn KEY_0/VALUE_0; Git 2.43.0 truyền cấu hình ấy tới helper của `fetch`. Scope `http.https://github.com/.extraheader` khớp endpoint `https://github.com/$TL_KHO`; dòng 80 chốt kho canonical. Host đối chứng không nhận header; key đổi host bị thiếu header, rc=128 ở helper. Hai `-c protocol...` không ghi đè auth. M5 COUNT=0 mất header; m11 HTTPS=never bị Git thật chặn trước helper.
- **105:** unset chạy sau fetch thành công; probe và t152 qua hậu kiểm AUTH_B64/COUNT không còn đặt. Nếu fetch rc=128, `-e` dừng trước unset và receipt. Unset không bảo đảm xoá sạch mọi bản sao trong memory.
- **106–107:** Git rev-parse thật và so NHAN==TL_H được thực thi trong probe. H đã có trong object store fixture; helper quảng bá ref, không chuyển pack qua HTTP.
- Khi encoder trả **9**, printf trả **8**, hoặc TL_TOKEN chưa đặt (**1**), shell dừng trước mask/fetch. Rc fetch lỗi dừng trước POST_OK. Đây là các lỗi thực thi, không dùng t152 thành công để suy rằng mọi nhánh lỗi đều đã thử.

**Kết luận ĐÚNG/ĐỦ:** bản vá HEAD sửa đúng phần cấp credential cho Git ở biên offline đã đo. Chưa đủ bằng chứng tuyên fetch trên runner GitHub chắc chắn xanh. Probe thay riêng transport HTTPS bằng helper cục bộ và hỏi config Git thật; không chứng minh libcurl đã gửi header trên dây. Rc=128 của base/m5/m7/m16 là helper fixture từ chối header, không tái lập thông báo Username hay phản hồi GitHub. Có Git 2.43.0 trong dải ≥2.31; chưa đo binary 2.31 hoặc toàn dải. `-w0` phù hợp GNU ở đây; không xác minh ảnh ubuntu-latest hiện hành. A3/canary sau land còn phải đo; giới hạn ấy không bị nâng thành finding.

### (2) Bề mặt token/base64

| Bề mặt | Đo được / giới hạn |
|---|---|
| Log stdout/stderr | HEAD không xtrace; auth block chỉ phát base64 trong command đăng ký mask. Probe offline lưu command thô do không có runner masker. M12/m13 bị test giết vì stderr thừa. |
| `::add-mask::` | Cơ chế đăng ký để runner che giá trị trong log được xử lý sau đó; không che output đã có trước đăng ký hoặc bảo đảm che mọi biến thể. Không bảo vệ argv, environment, stdin, memory, file hay artifact. Tại đây chỉ xác minh command được phát đúng. |
| argv Git/helper | Wrapper ghi argv rồi exec Git thật; helper ghi argv của mình. HEAD không có token/base64 trong argv. Dạng (b) đối chứng có base64 trong argv; được spec cho phép, nhưng HEAD chọn (a). |
| Encoder | printf/echo là builtin trong Bash; base64 ngoài nhận `-w0`, token đi qua stdin. Không có token trong argv encoder theo câu lệnh này. |
| Environment / ps | Helper tự ghi nhận TL_TOKEN thô và GIT_CONFIG_VALUE_0; AUTH_B64 không export. Phạm vi thực tế là **một lời gọi fetch và các tiến trình con**. Tiến trình đủ quyền đọc environment có thể thấy credential; add-mask không che kênh ấy. Không quét ps/proc ngoài fixture. |
| Config đĩa | `.git/config` fixture không đổi byte; HEAD không ghi auth config. T152 m3 chặn lời gọi git config ghi extraheader. |
| Curl sau fetch | Dòng 118 đã có từ base truyền TL_TOKEN thô trong argv curl. Đây là bề mặt sẵn có của bước, không phải base64 mới do patch đưa vào. |
| Receipt | Mã tạo receipt ở `ops/lease_publish.py:1772` và workflow 121–141 không serialize TL_TOKEN/AUTH_B64. Blob workflow được băm trước nội suy env. Chưa đọc artifact/receipt thật; không tuyên đã đo chúng sạch. |

### (3)–(6) Test, lint, write set và EVIDENCE

T152 HEAD chạy Bash thật và đọc config Git qua stub fetch; bốn mutant A1 bị giết ở bốn chốt (i)/(ii)/(iii)/(iv). Base ĐỎ đúng (i), HEAD XANH. COUNT sai, nguồn AUTH_B64 sai biến, fetch thứ hai, mask/xtrace, wrap và padding đều đã đo lại. M16 là chỗ mù khác: **test tự đặt TL_TOKEN bất kể giá trị YAML của chính bước fetch**, nên đường từ secret tới input shell chưa được khoá.

Actionlint từ `nguon/actionlint/` 1.7.7 được dùng, không tải; debug cho thấy gọi ShellCheck 0.9.0 trên cả hai run block, không lỗi. ShellCheck riêng dùng `--norc --shell=bash -e SC2154` vì biến được cấp từ env của bước; rc=0. Pyflakes không có, không nhận tín dụng kiểm Python inline bằng pyflakes.

Toàn diff base..HEAD và danh sách đường từng commit chỉ có hai tệp được phép. Master tại đây đã đi tiếp hơn SHA trong prompt, nhưng so write set với base vẫn rỗng. AST ngoài t152 không thay đổi. Không checkout/commit/đổi ref hay chủ động ghi index clone; mutant, repo fixture và bản thử HINT đều dưới scratch.

EVIDENCE giữ các bảng +50/+79 như lịch sử và cập nhật +80 ở các lượt sau; không coi chúng là khai sai HEAD. Phần gen3/lượt1 khai áp nguyên HINT, workflow không đổi, m15 cũ sống/mới chết, các ca m14/m13/m5/m8, suite và lint xanh: tự đo khớp. Các mutant tác giả nói chưa chạy được reviewer chạy lại, không gán công ngược. EVIDENCE nói rõ chưa đo runner/mask thật, không khai A3 xong hoặc mọi mutant đều chết. M16 chứng minh thiếu độ phủ, không chứng minh tác giả khai gian các số đã nêu. Lease, reroute, thời điểm và các comment/run lịch sử không xác minh độc lập offline. Chỉ thị trực tiếp gen3 “chạy đến hết P1, P2” được dùng, không đọc doctrine.

## Findings

### t152-khong-khoa-nguon-token-trong-env [P2] Token giả che mất nguồn credential rỗng của bước fetch

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5389` chỉ giữ thân lệnh, không giữ env bước; **5422** luôn gán `TL_TOKEN=token` do fixture tạo. Điểm mutant tương ứng: `.github/workflows/ops-thu-hoi-admission.yml:71` trong bản sao.
- **VẤN ĐỀ:** m16 đổi đúng khai báo TL_TOKEN của bước fetch sang chuỗi rỗng; giữ nguyên 11 dòng auth mới. T152/t148 vẫn XANH vì test không đọc giá trị này mà tự cấp token khác. Toàn suite mutant **147/147**, lint **rc=0**. Khi shell được cấp giá trị rỗng theo YAML, header giải mã thành `x-access-token:` — không mang token fixture; Git/helper đòi header chứa token đã cấp nên rc=128. M1 yêu cầu nguồn `secrets.GITHUB_TOKEN` qua TL_TOKEN, còn test hiện chỉ đo nửa sau TL_TOKEN→header. Đây là chốt nguồn env độc lập bị thiếu. **HEAD vẫn có khai báo token đúng**; không nói workflow HEAD lỗi hay phép đo header hiện tại vô giá trị.
- **ĐÃ THỬ VÁ:** HINT giữ env của bước chứa fetch và kiểm TL_TOKEN lấy từ `secrets.GITHUB_TOKEN` hoặc dạng `github.token`; nhận khác biệt khoảng trắng quanh biểu thức. Không bỏ các oracle Bash/Git hay ba fixture padding. Rút hai dòng docstring để bù hai dòng chốt, giữ diff so base **+69 test/+11 workflow**. Chỉ đổi t152, 2 hunk.
- **ĐÃ THỬ NGHIỆM:** m16 SỐNG ở test HEAD và 301aac8; t148/lint cũng XANH. Suite m16 **147/147, đã chạy=147, bỏ qua=0, rc=0**. Probe dùng token giả làm giá trị cho biểu thức secret của HEAD, còn chuỗi rỗng của m16 được cấp nguyên dạng; HEAD/header chuẩn rc=0, m16/header thiếu token rc=128. Không chạy engine biểu thức Actions hay GitHub HTTP. HINT giết m16 đúng `(i) env TL_TOKEN của bước fetch phải lấy GitHub token`, giữ HEAD/dạng (b)/scope repo/github.token/khác khoảng trắng XANH và base/m1–m15/m18–m21 GIẾT. Dry-run/apply rc=0, file đúng byte, AST ngoài t152 không đổi. Suite HINT: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0.
- **ĐỘ TIN:** cao về mutant sống, dữ liệu header thiếu token và hiệu quả HINT. Xếp **P2 thiếu chốt tích hợp nguồn env**, không P1: HEAD cấp đúng nguồn và test vẫn thực sự đo header từ input TL_TOKEN của nó. Chưa đo phản hồi GitHub/token thật. M16 sống cả trước hunk padding nên không gọi cách vá lượt trước là vá sinh lỗi mới.

Bằng chứng: [mutant mới](scratch/logs/extra-mutants.json), [m16 test cũ](scratch/logs/old-m16-t148.json), [m16 Git/helper và lint](scratch/logs/m16-runtime.json), [suite m16](scratch/logs/m16-suite.json), [ma trận HINT](scratch/logs/hint-validation.json), [suite HINT](scratch/logs/hint-suite.log). Script: [dựng mutant](scratch/extra_mutants.py), [probe binding](scratch/validate_m16.py), [thử HINT](scratch/validate_hint.py).

## Mutant đã chạy

Dựng độc lập từ bytes HEAD, chạy mới trên bản sao `scratch/mutants/`. M1–m4 theo A1, m5–m15 dựng lại theo verdict trước. M2 dùng mẫu URL đã có trong spec. Không tạo payload đường dẫn thoát/khai thác.

| Mutant | Đột biến | t152 HEAD | Lý do / đối chứng | HINT |
|---|---|---|---|---|
| m1 | KEY_0 thành http.postBuffer | **GIẾT** | (i), rc=1, thiếu header | GIẾT (i) |
| m2 | URL credential mẫu A1 | **GIẾT** | (ii), URL chứa credential | GIẾT (ii) |
| m3 | Thêm git config local extraheader | **GIẾT** | (iii), lệnh ghi config | GIẾT (iii) |
| m4 | persist-credentials true | **GIẾT** | (iv), checkout sai | GIẾT (iv) |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; Git/helper thiếu header rc=128 | GIẾT (i) |
| m6 | VALUE_0 dummy | **GIẾT** | (i), header khác oracle | GIẾT (i) |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), sai nguồn; helper rc=128 | GIẾT (i) |
| m8 | Bỏ add-mask | **GIẾT** | (v), thiếu đăng ký mask | GIẾT (v) |
| m9 | KEY http.extraheader toàn cục | **GIẾT** | (i), rc=94, host đối chứng nhận header | GIẾT (i) |
| m10 | Fetch thứ hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Đếm 2; Git thật/helper lần hai thiếu header, rc=128 | GIẾT, đếm 2 |
| m11 | HTTPS=never | **GIẾT** | (i), rc=95; Git thật chặn transport trước helper | GIẾT (i) |
| m12 | set -x trước AUTH_B64 | **GIẾT** | (v), stderr thừa | GIẾT (v) |
| m13 | Thêm -x vào set đầu bước | **GIẾT** | (v), chạy cờ shell đầu bước | GIẾT (v) |
| m14 | Bỏ -w0 | **GIẾT** | (i), wrap khác oracle | GIẾT (i) |
| m15 | Bỏ padding `=` | **GIẾT** | (i), token thứ hai bắt mất `==`; test 301aac8 SỐNG | GIẾT (i) |
| **m16 mới** | **env TL_TOKEN của bước fetch rỗng** | **SỐNG** | Test tự cấp token khác; suite mutant 147/147; probe theo YAML thiếu token | **GIẾT (i), nguồn env** |
| m17 mới | Scope header hẹp riêng repo canonical | **SỐNG** | Biến thể hợp lệ: Git/helper nhận đúng header, host đối chứng không nhận | SỐNG, đúng |
| m18 mới | COUNT=2, không có KEY_1 | **GIẾT** | (i), rc=95, Git báo missing config key | GIẾT (i) |
| m19 mới | printf thêm LF vào input encoder | **GIẾT** | (i), bytes header khác oracle | GIẾT (i) |
| m20 mới | Bỏ unset AUTH_B64 | **GIẾT** | (i), rc=1, hậu kiểm lifetime | GIẾT (i) |
| m21 mới | Dời add-mask xuống sau fetch | **GIẾT** | (i), thứ tự stdout đổi, dòng cuối không phải header | GIẾT (i) |

**Tín dụng HEAD: m1–m15 là 15 GIẾT/0 SỐNG; toàn nhóm m1–m21 là 19 GIẾT/2 SỐNG.** Trong hai ca sống, m16 là lỗ cần vá, m17 là biến thể hợp lệ nên không lập finding. Không nhận công HINT giết m16 cho PR hiện tại. Dạng (b), nguồn `github.token` và khác khoảng trắng là đối chứng dương, host sai là đối chứng âm; không cộng vào mẫu số. Mutant nội bộ của 146 ca cũ không gộp vào nhóm này.

Script tái lập: [ma trận trước](scratch/review_matrix.py), [runtime](scratch/probe_runtime.py), [mutant mới](scratch/extra_mutants.py), [gates](scratch/run_gates.py), [HINT](scratch/validate_hint.py). Repo fixture chỉ chứa workflow/commit giả, helper không dùng network. Probe helper ban đầu trả thừa dòng khi Git kết thúc khiến BrokenPipe trong đồ giả; đã sửa xử lý EOF và chạy lại toàn probe. Các log runtime cuối không còn traceback; không quy lỗi đồ giả cho PR.

## HINT và phạm vi

`HINT.patch` là unified diff `patch -p0` từ gốc `cay-kho/`, dựa đúng HEAD: **2 hunk, riêng `ops/lease_publish_test.py`**. Đã áp thử trong scratch, không áp vào clone. Test sau HINT vẫn +69/−0 so base (`git diff --no-index` rc=1 nghĩa là có diff), workflow +11/−0, tổng +80/−0. Không sửa ca cũ.

Không mạng, không đọc tệp bị cấm hoặc tài liệu ngoài cwd, chỉ thực thi công cụ/runtime có sẵn. Không thao tác PR, canary hay land. Các phép đo chạy tại đây độc lập với số tác giả và verdict cũ. Trần generation không được dùng để hạ chuẩn hoặc tạo thêm finding.

## chua_do_duoc

1. Fetch trên runner GitHub thật, token/quyền/ref kho thật, HTTP/TLS/redirect, libcurl trên dây và toàn job. A3 sau land chưa thực hiện; rc helper 128 không phải thông báo Username/HTTP thật.
2. Secret masker Actions, log/artifact/receipt thật cùng check_run_id/workflow_definition_commit/workflow_definition_sha256/checker_rc. Command mask và đọc mã không thay readback.
3. Git binary 2.31/toàn dải 2.31+, ảnh ubuntu-latest hiện hành, Windows/macOS/BSD base64. Đã đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4, Python 3.11.15, actionlint 1.7.7, ShellCheck 0.9.0 ở đây.
4. Engine biểu thức Actions, độ dài/định dạng token thật và phản hồi GitHub cho Basic password rỗng. Probe m16 cấp trực tiếp literal rỗng của YAML, so header với token fixture; không mô phỏng mọi dạng biểu thức/env inheritance.
5. Ps/environment/memory ngoài fixture hoặc đảm bảo unset xoá memory. Đo được helper kế thừa credential qua env; add-mask không bảo vệ kênh ấy.
6. Timeline Issue/comments/run/lease/reroute và hành động lịch sử của tác giả. SHA master được tự đo khác lời nhắc; không suy nguồn gốc các commit đó ngoài snapshot hiện có.
7. Wrapper tải mạng nguyên dạng, pyflakes và chạy suite trực tiếp trong clone có doctrine. Đã dùng gói offline/bản sao đủ ops/.github và nêu đúng phạm vi.
