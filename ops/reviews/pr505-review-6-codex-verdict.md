verdict: changes_requested
reviewed_sha: 301aac8e09b2195e0a8e53426d302c910b2a2484
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: bcc72d708f3e8da80795b1f7f0f98d807591669076770da089fcf850922b18bb
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 6
review_generation: 2; lượt 3
review_class: sensitive
hint_sha256: a7b0abc6cab235abaedf50cd2d692155074a484404df343cdb821b94c644f7f5

**0 P1, 1 P2 sửa được trong write set.** Workflow HEAD tạo đúng header trong các phép đo offline. Bản vá theo HINT lượt trước bắt được wrap, nhưng fixture mới mất nhánh padding: m15 bị test 19337fa giết, lại sống trên HEAD. HINT kèm theo chạy cùng oracle với ba độ dài, giữ tổng diff +80/−0. Không có bằng chứng HEAD fetch đỏ hoặc token thật bị lộ trên runner.

Bắt đầu theo yêu cầu: 2026-09-11T08:27:07Z. Hoàn tất: 2026-09-11T08:41:51Z; trong giới hạn 40 phút.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc/băm verdict gen2/lượt 2 và so HINT trước các mục (1)–(6); chạy lại m14 và m1–m13 trước khi chuyển sang suite/lint/probe mới. Không chép kết quả lượt trước.

- `nguon/VERDICT.rvm9-5.md`: **e4e825726b4c1073fe875f198bc82bd794bfb96b3768a8eac8e95bb46ea13b88**, khớp toàn băm yêu cầu.
- `nguon/HINT.rvm9-5.patch`: **27b2cc7f89235ec1f818e6a44e9d9362222d18c17abc612ba85880dcf15edbd1**, khớp tiền tố cung cấp.

Slug `t152-fixture-ngan-bo-sot-base64-wrap` [P2]: **VÁ SINH LỖI MỚI trong độ phủ test; riêng nhánh wrap ĐÃ VÁ THẬT**.

| Đối chứng tự đo | Kết quả lượt 6 |
|---|---|
| Diff `19337fa..HEAD` với HINT | Một hunk `-5415,7 +5415,7`, tọa độ và toàn bộ thân hunk bằng nhau; chỉ khác tên hàm Git thêm sau `@@` |
| Áp HINT lên test tại 19337fa trong `scratch/prior-apply/` | `patch -p0` rc=0; toàn tệp kết quả trùng bytes HEAD |
| Workflow so lượt trước | Trùng byte; một commit mới chỉ sửa test |
| m14 bỏ `-w0` | Test 19337fa **SỐNG**; test HEAD **GIẾT đúng (i)** |
| m1–m13 dựng lại | **13/13 GIẾT** đúng chốt; không mất chốt trong nhóm này |
| m15 mới bỏ padding `=` | Test 19337fa **GIẾT (i)**; test HEAD **SỐNG** |

Đánh giá đầu tiên sau m1–m14 là wrap đã vá thật. Phép đối chứng m15 sau đó làm rõ hồi quy mới: fixture cũ 16 ký tự cộng prefix 15 = 31 bytes, có `==`; fixture mới 81 + 15 = 96 bytes, không padding. **Tác giả áp nguyên HINT reviewer lượt 5, không sửa lệch. Lựa chọn fixture trong HINT đó gây mất độ phủ**, không phải tác giả tự bỏ chốt. Workflow nguyên byte nên không gọi đây là lỗi runtime mới của workflow.

Bằng chứng: [so HINT](scratch/logs/prior-hint-round6.json), [m1–m14](scratch/logs/mutants-round6.json), [m15 cũ/mới và bytes](scratch/logs/extra-mutants-round6.json).

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 6 | Khớp? |
|---|---|---|---|
| Spec đóng băng | SHA256 b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường spec trong clone không tồn tại | Khớp bản cung cấp |
| SHA head/base | 301aac8 / 27c413c3 | Đúng SHA đầy đủ đầu tài liệu | Có |
| Write set exact | 2 tệp, +11/+69, −0 | `git diff --stat/--numstat 27c413c3..HEAD`: **2 tệp, +80/−0**; cả sáu commit trong khoảng chỉ chạm hai đường này | Có |
| Origin/master đi tiếp | 26e2555, không chạm hai tệp | **26e2555d36c48b3c0f625ae50ab2cfb62b6cb858**; `git diff --stat 27c413c3..origin/master -- <hai tệp>` rỗng | Có |
| Delta lượt 6 | Áp nguyên HINT lượt 5 | 1 hunk/1 dòng thay; apply trùng byte, workflow không đổi | Có |
| t152 trên nền | ĐỎ đúng (i) | Hàm t152 HEAD đọc workflow base: `TinHieuChotCa`, `(i) đoạn auth/fetch không chạy được: rc=1` | Có; base chưa có t152 |
| t152/t148 HEAD | XANH | Gọi riêng cả hai XANH | Có |
| m14 | Cũ XANH, mới ĐỎ (i) | Đúng cả hai đối chứng | Có |
| m1–m13 | Tác giả nói chưa chạy lại lượt này | Reviewer tự chạy lại **13/13 GIẾT** | Không gán số reviewer cho tác giả |
| Suite HEAD | 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, bản sao nêu dưới |
| Wrapper HEAD | AL_VER=1.7.7; 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0; gói AL_GOI cục bộ | Có, không tải mạng |
| Lint | actionlint + shellcheck rc=0 | **1.7.7 / 0.9.0**, rc=0; debug chứng minh gọi ShellCheck cả hai run block; chạy ShellCheck riêng cũng 0 | Có |
| Ca cũ / whitespace | Không đổi ca cũ, diff sạch | AST bỏ riêng t152: base=HEAD=HINT; `git diff --check` rc=0 | Có |
| Credential tới fetch | Header đúng từ TL_TOKEN | Git **2.43.0 fetch thật**, helper HTTPS cục bộ nhận header đúng; HEAD rc=0, qua NHAN==TL_H; base/m5/m7 rc=128 | Có ở biên helper/config |
| URL matching | URL canonical nhận header | HEAD/scope repo/dạng (b) nhận đúng header; host đối chứng không có; key host sai thiếu header ở URL fetch, rc=128 | Có ở config, chưa đo HTTP/redirect |
| Scope / argv / đĩa | Một lời gọi, không ghi config hoặc token URL | Một helper; argv Git/helper không token/base64; config fixture nguyên byte; helper kế thừa header qua environment | Có, gồm cây tiến trình con |
| Shell / bytes | GNU -w0, mask trước fetch, unset sau | HEAD đúng bytes ở token 16/42/43/81/160 ký tự; thành công qua hậu kiểm unset; encoder/printf/Git lỗi dừng shell | Có ở Linux tại đây |
| M15 mới | Reviewer tìm mutant sống ngoài A1 | Nối bỏ `=` vào encoder: **t152/t148 SỐNG**, lint rc=0; test 19337fa GIẾT | P2 mất nhánh padding |
| Suite m15 | Đo toàn cổng có bỏ lọt | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |
| HINT | Sửa P2 trong write set/trần dòng | 1 hunk, chỉ test; apply/dry-run rc=0, trùng byte; vẫn +69 test/+11 workflow = **+80/−0** | Có |
| Ma trận HINT | Giữ dương, giết âm | HEAD/scope repo/dạng (b) XANH; base và **m1–m15 GIẾT** | Có |
| Suite HINT | Không hồi quy | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |

Bằng chứng: [metadata](scratch/logs/metadata-round6.json), [suite HEAD](scratch/logs/head-suite-round6.log), [rc suite HEAD](scratch/logs/head-suite-round6.json), [wrapper](scratch/logs/head-wrapper-round6.log), [rc wrapper](scratch/logs/head-wrapper-round6.json), [versions](scratch/logs/versions-round6.json), [actionlint/ShellCheck](scratch/logs/actionlint-round6.log), [kiểm cuối/numstat](scratch/logs/final-checks-round6.json), [Git/helper](scratch/logs/git-probe-round6.json), [URL/dạng (b)](scratch/logs/url-form-probes-round6.json), [shell/bytes](scratch/logs/shell-round6.json), [HINT](scratch/logs/hint-validation-round6.json).

**Cách chạy suite:** nguyên lệnh `python3 ops/lease_publish_test.py` chạy tại `scratch/head-tree/`, chứa bản sao đầy đủ `ops/` và `.github/`, hai tệp review trùng băm HEAD. T82 dùng `copytree(HERE.parent, …)`; chạy trong clone sẽ đọc/sao cả các tệp bị cấm. Bản sao tránh việc đó và giữ đủ workflows; không cho ca tự qua vì thiếu workflow. TMPDIR đặt trong `scratch/tmp/`, tắt bytecode. Cây m15 chỉ sửa workflow tương ứng; cây HINT chỉ sửa t152. Wrapper chạy `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` với AL_GOI là gói cung cấp trong cwd, SHA256 **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**, đích cài trong scratch và TAR_OPTIONS=--no-same-owner. Không gọi đó là chạy trực tiếp trong clone hoặc kiểm đường tải mạng.

### (1) Shell, cấu hình Git và mức kết luận fetch

- **Workflow 73:** chạy `set -euo pipefail`. Probe thực thi từ đầu bước tới sau kiểm NHAN. HEAD thành công có cờ `ehuB`, không `x`. T152 cũng chạy cả preflight nhưng stub rev-parse cấp S/blob giả; không dùng nó để chứng minh nguồn S/blob thật.
- **97:** Bash builtin `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định, quote biến, không thêm LF. GNU base64 **9.4**, `-w0`, tạo một dòng đúng bytes Python ở các độ dài đã thử. Command substitution bỏ LF cuối, giữ LF giữa chuỗi: m14 đo lại token 42 chỉ 76 ký tự nên chưa hỏng; 43 tạo 76+4, 81 tạo 76+52 nên sai header và command mask bị tách dòng.
- Dưới `-e` và `pipefail`, encoder trả **9**, printf trả **8** đều dừng trước mask/fetch. TL_TOKEN chưa đặt bị `-u` chặn **1**. Fetch trả **128** dừng trước hậu kiểm/receipt. Đây không phải kiểm quyền hay token rỗng trên GitHub.
- **98:** `echo` là builtin, phát command đăng ký base64 sau gán và trước Git. Chuỗi HEAD một dòng. Phép đo xác nhận command/bytes/thứ tự phát; không xác nhận masker Actions thật xử lý thành công.
- **99–104:** COUNT=1 chọn KEY_0/VALUE_0. Ba phép gán môi trường và continuation thuộc cùng simple command Git. KEY `http.https://github.com/.extraheader` khớp URL `https://github.com/$TL_KHO`; dòng 80 đã chốt kho canonical. Không có host mismatch trên HEAD. Hai `-c protocol…` không ghi đè header. Git 2.43.0 đọc cấu hình tại helper; m5 COUNT=0 mất header; m11 HTTPS=never bị Git thật từ chối trước helper.
- **105:** `unset AUTH_B64` chạy sau fetch thành công. Hậu kiểm trong probe Git thật xác nhận AUTH_B64 và COUNT không còn đặt. Khi fetch lỗi, `-e` kết thúc shell trước unset; không có luồng tiếp tục tới receipt. `unset` không bảo đảm xoá mọi bản sao trong memory.
- **106–107:** repo fixture có S/H khác nhau; thực thi `git rev-parse` thật, fetch cập nhật ref và so NHAN==TL_H trước POST_OK. H đã có sẵn trong object store fixture; helper quảng bá ref, không truyền pack qua HTTP.

**ĐÚNG/ĐỦ:** HEAD sửa đúng phần thiếu credential ở biên đã đo. Không đủ bằng chứng kết luận toàn job/fetch trên runner thật chắc chắn xanh. Probe thay riêng transport HTTPS bằng helper cục bộ, helper hỏi Git config thật và kiểm header exact; **chưa chứng minh libcurl gửi header trên dây**. Rc=128 của base/m5/m7/m14/m15 là helper fixture từ chối header, không tái lập thông báo Username hay phản hồi GitHub. Git 2.43.0 thuộc dải ≥2.31 nhưng không có binary 2.31/toàn dải để đo. GNU `-w0` hợp với Linux/GNU đang chạy; ảnh ubuntu-latest hiện hành không được xác minh offline. A3/canary vẫn phải đo sau land, không dùng giới hạn này làm finding P1/P2.

### (2) Bề mặt token/base64

| Bề mặt | Đo được / giới hạn |
|---|---|
| Log stdout/stderr | HEAD không xtrace. Trong auth block, base64 chỉ phát qua command đăng ký mask; Git fetch probe in URL/ref sạch. Log offline giữ command thô vì không có runner masker. M12/m13 bị t152 giết do stderr thừa. |
| `::add-mask::` | Đăng ký giá trị để runner che log được xử lý sau đó; không che output đã phát trước đăng ký hoặc mọi biến thể chưa đăng ký. Không bảo vệ argv, environment, stdin, memory, tệp config hay artifact. Không coi command đăng ký là phép đo mask thật. |
| argv Git/helper | Wrapper ghi chính argv trước `execv` Git; helper ghi argv của mình: HEAD không chứa token/base64. Dạng (b) được spec cho phép nhưng đưa header vào argv; HEAD dùng (a). |
| Encoder / builtin | Theo shell HEAD, printf/echo là builtin; encoder ngoài chỉ có đối số `-w0`, nhận dữ liệu qua stdin. Không đưa token thành đối số encoder. Chưa làm phép đọc process memory. |
| Environment / ps | Helper tự ghi nhận GIT_CONFIG_VALUE_0 chứa header và TL_TOKEN thô kế thừa; AUTH_B64 không export. “Một tiến trình” trong comment phải hiểu là **một lời gọi fetch cùng cây con**. Process đủ quyền đọc environment có thể thấy credential; masker không che kênh này. Không quét ps/proc ngoài fixture. |
| Config đĩa | `.git/config` fixture nguyên byte sau probe, không có token/base64; source HEAD không ghi auth config. |
| Curl sau fetch | Dòng 118 đã có từ base đưa TL_TOKEN thô vào argv curl. Đây là bề mặt sẵn có; bản vá không thêm base64 vào đó. Mask log không che argv. |
| Receipt | Mã dựng receipt ở `ops/lease_publish.py:1772` và workflow 121–141 không serialize TL_TOKEN/AUTH_B64; băm workflow dùng blob chưa expand biến. Chưa readback artifact thật, không tuyên receipt thật sạch. |

### (3)–(6) Phạm vi của test, lint, write set và EVIDENCE

T152 hiện đo Bash thật + config Git với stub fetch, phân biệt bốn răng A1: m1→(i), m2→(ii), m3→(iii), m4→(iv). Test nền ĐỎ đúng (i); HEAD XANH. M5 COUNT sai, m7 dẫn từ biến khác và m10 fetch lần hai đều GIẾT khi dựng lại. Mutant sống mới là m15; không nhận tín dụng HINT giết nó cho PR hiện tại.

Actionlint 1.7.7 có sẵn trong `nguon/` được dùng, không tải. Debug ghi rõ ShellCheck 0.9.0 chạy cả hai run block, tổng 0 lỗi; kiểm ShellCheck riêng trên script trích từ YAML cũng rc=0 (`--norc --shell=bash -e SC2154`, SC2154 vì biến do env bước cấp). Pyflakes không có nên actionlint không kiểm Python inline bằng pyflakes.

Diff toàn khoảng base..HEAD và danh sách đường từng commit đều chỉ có hai tệp được phép. Origin/master đi tiếp nhưng diff hai tệp với base rỗng. AST ca cũ không đổi. Băm cuối hai tệp trùng đầu review; `git diff --name-only` cây tracked rỗng. Không checkout/commit/đổi ref hoặc chủ động ghi index trong `cay-kho/`; mọi mutant, repo fixture, bản thử HINT nằm trong scratch.

EVIDENCE giữ các số +50/+79 ở phần lịch sử rồi cập nhật +80, không coi đó là khai sai HEAD. Phần gen2/lượt 3 khai áp nguyên HINT, một commit, workflow không đổi, m14 cũ xanh/mới đỏ, t152/t148 và suite xanh: tự đo lại khớp. Tác giả nói rõ chưa chạy lại m1–m13; reviewer đo lại, không gán công cho tác giả. EVIDENCE nói rõ chưa đo runner và masker thật, không khai nghiệm thu A3 hoặc giết mọi mutant. M15 không chứng minh tác giả khai gian; nó chứng minh HINT/fixture lượt trước làm mất một nhánh. Timeline riêng tác giả, Issue/comments/run lịch sử, lease/reroute và thao tác khôi phục cây không xác minh độc lập offline. Trần lượt 3/gen2 nhận theo chỉ thị trực tiếp người dùng, không đọc doctrine hoặc xin lại phép.

## Findings

### t152-fixture-mat-nhanh-padding-base64 [P2] Fixture mới bỏ mất phép đo padding

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5418` chọn một token 81 ký tự; **5431–5436** kiểm header/mask duy nhất với token ấy. Vị trí mutant tương ứng: `.github/workflows/ops-thu-hoi-admission.yml:97` trên bản sao.
- **VẤN ĐỀ:** m15 nối thao tác `tr -d '='` sau encoder. Input fixture mới gồm 15+81=96 bytes nên base64 dài 128 và không có padding: thao tác sai này không đổi kết quả ở fixture, t152/t148 HEAD XANH, lint rc=0. Cùng mutant **ĐỎ với test 19337fa** vì fixture cũ 16 ký tự cần `==`. Với token giả 16/79/80 ký tự, m15 làm mất 2/2/1 dấu `=`, header khác oracle base64 và Python decoder strict báo `Incorrect padding`. Đây là nhánh số bytes modulo 3 có thật của đúng encoder đang được kiểm, và là độ phủ đã có rồi bị mất. HEAD workflow vẫn có base64 chuẩn; không có bằng chứng token thật bị lộ hoặc GitHub thực tế từ chối mutant.
- **ĐÃ THỬ VÁ:** HINT giữ nguyên oracle, chuyển một fixture thành vòng ba token dài **81/82/83**, tương ứng input **96/97/98** bytes, output **128/132/132**, padding **0/2/1**. Cả ba đều vượt ngưỡng wrap 76; không dò chuỗi `-w0` hoặc `tr`. Một hunk, chỉ t152; không tăng dòng so HEAD, vẫn test +69/workflow +11. Dạng (b) và scope repo tiếp tục được nhận.
- **ĐÃ THỬ NGHIỆM:** m15 SỐNG ở t152/t148 HEAD, GIẾT ở t152 19337fa; lint m15 rc=0. Probe token ngắn: HEAD Git/helper rc=0, m15 rc=128 vì helper exact-header; token 81: m15 rc=0 vì chưa có padding để mất. Đây không phải HTTP/GitHub test. HINT giết m15 đúng (i), giữ HEAD/dạng (b)/scope repo xanh, giết base/m1–m14. Dry-run/apply patch rc=0 và byte bằng bản thử; AST ngoài t152 không đổi. Suite m15: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0. Suite HINT: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0.
- **ĐỘ TIN:** cao về mutant sống, hồi quy giữa hai test, bytes và hiệu quả HINT. Xếp **P2 thiếu ca của nhánh dữ liệu**, không nâng P1 do chưa đo được tác động GitHub và HEAD không sinh header sai. Còn P2 sửa được trong write set nên kết luận `changes_requested`, bất kể trần lượt đã hết. HINT cũ của reviewer đã chọn fixture không padding; không đổ lỗi cho tác giả vì áp nguyên nó.

Bằng chứng: [m15 cũ/mới, decoder, shell và Git/helper](scratch/logs/extra-mutants-round6.json), [lint m15](scratch/logs/m15-lint-round6.log), [ma trận HINT](scratch/logs/hint-validation-round6.json), [suite m15](scratch/logs/m15-suite-round6.log), [rc m15](scratch/logs/m15-suite-round6.json), [suite HINT](scratch/logs/hint-suite-round6.log), [rc HINT](scratch/logs/hint-suite-round6.json).

## Mutant đã chạy

Dựng riêng từ bytes HEAD trong `scratch/mutants/`; m1–m4 theo §A1, m5–m14 dựng lại theo verdict được cung cấp. M2 lấy đúng mẫu URL credential của spec. M15 chỉ biến đổi đầu ra encoder; không tạo nội dung đường dẫn thoát/khai thác. Các lượt test và probe bên dưới đều chạy mới ở lượt 6.

| Mutant | Thay đổi | t152 HEAD | Lý do / đối chứng mới | HINT |
|---|---|---|---|---|
| m1 | KEY_0 thành http.postBuffer | **GIẾT** | (i), rc=1, thiếu header | GIẾT (i) |
| m2 | URL credential mẫu A1 | **GIẾT** | (ii), URL chứa credential | GIẾT (ii) |
| m3 | Thêm git config local extraheader | **GIẾT** | (iii), phát hiện lệnh ghi | GIẾT (iii) |
| m4 | persist-credentials true | **GIẾT** | (iv), checkout sai | GIẾT (iv) |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; helper thiếu header, fetch rc=128 | GIẾT (i) |
| m6 | VALUE_0 dummy | **GIẾT** | (i), header khác oracle | GIẾT (i) |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), header sai; helper rc=128 | GIẾT (i) |
| m8 | Bỏ add-mask | **GIẾT** | (v), không có command đăng ký | GIẾT (v) |
| m9 | KEY http.extraheader toàn cục | **GIẾT** | (i), rc=94, host đối chứng có header | GIẾT (i) |
| m10 | Fetch thứ hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Đếm 2; Git/helper gọi 2 lần, lần sau thiếu header, rc=128 | GIẾT, đếm 2 |
| m11 | HTTPS=never | **GIẾT** | (i), rc=95; Git thật rc=128 trước helper | GIẾT (i) |
| m12 | set -x trước AUTH_B64 | **GIẾT** | (v), stderr thừa | GIẾT (v) |
| m13 | Thêm -x vào set đầu bước | **GIẾT** | (v), thực thi cả trạng thái shell đầu bước | GIẾT (v) |
| m14 | Bỏ -w0 | **GIẾT** | (i), base64 wrap; test 19337fa SỐNG | GIẾT (i) |
| **m15 reviewer** | **Bỏ padding `=` sau base64** | **SỐNG** | Fixture mới không padding; test 19337fa GIẾT, token có padding làm header sai | GIẾT (i) |

**Tín dụng t152 HEAD: 14 GIẾT / 1 SỐNG.** M15 là mutant sống mới ngoài bốn ca A1; không nhận công HINT cho PR hiện tại. Dạng (b)/scope repo là đối chứng dương XANH; key host sai là đối chứng âm ĐỎ, không gộp vào mẫu số. Catalogue mutant nội bộ của 146 ca cũ không gộp vào nhóm m1–m15.

Script tái lập: [ma trận](scratch/review_matrix.py), [Git/shell probe](scratch/probe_runtime.py), [m15](scratch/extra_mutants.py), [gate runner](scratch/run_gates.py), [kiểm HINT](scratch/validate_hint.py), [kiểm cuối](scratch/final_checks.py). Repo fixture chỉ chứa workflow và commit giả S/H, helper không dùng network.

## HINT và giới hạn phạm vi

`HINT.patch` là unified diff `patch -p0` từ gốc `cay-kho/`, dựa đúng HEAD; **1 hunk, chỉ `ops/lease_publish_test.py`**. Đã áp thử trong scratch, không áp vào clone. Numstat test sau HINT so base **+69/−0** (`git diff --no-index` rc=1 là có diff, không phải lỗi chạy); cộng workflow nguyên byte **+11/−0**, vẫn đúng hai tệp và trần +80. HINT chỉ mở rộng dữ liệu fixture cho cùng chốt đã có.

Không dùng mạng, không đọc nội dung các tệp bị cấm hoặc nguồn tài liệu ngoài cwd; các công cụ/runtime có sẵn được thực thi theo yêu cầu. Không có phép canary, gửi bình luận, sửa PR hay land. Trần generation không làm hạ chuẩn, cũng không coi giới hạn không đo được là finding.

## chua_do_duoc

1. Fetch xanh trên GitHub runner thật, token/quyền contents:read với ref kho thật, HTTP/TLS/redirect, toàn job. A3 sau land chưa thực hiện. Rc fixture 128 không phải thông báo Username/HTTP thật.
2. Secret masker Actions, log/artifact thật, receipt thật cùng check_run_id/workflow_definition_commit/workflow_definition_sha256/checker_rc. Đọc mã và command mask không thay readback.
3. Git binary 2.31/toàn dải 2.31+, ảnh ubuntu-latest hiện hành, Windows/macOS/BSD base64. Đã đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4, Python 3.11.15, actionlint 1.7.7, ShellCheck 0.9.0 tại đây.
4. Độ dài/định dạng GITHUB_TOKEN hiện hành và mức dung nạp base64 thiếu padding của GitHub. Decoder strict và helper exact-header chỉ là phép đo offline; không dùng chúng để tuyên GitHub đã từ chối m15.
5. Ps/environment/memory ngoài fixture hoặc bảo đảm unset xoá sạch memory. Helper fixture đo được environment có credential; masker không bảo vệ kênh ấy.
6. Timeline Issue/comments/run/lease, thao tác tác giả, lời lịch sử “mọi PR/không bao giờ xanh”. Chỉ snapshot/diff/băm và hành vi offline được xác minh độc lập.
7. Wrapper tải mạng nguyên dạng; kiểm tại đây dùng AL_GOI cục bộ. Suite chạy trên bản sao ops/.github để tránh đọc doctrine, không trực tiếp trong clone. Pyflakes không có, không nhận tín dụng kiểm Python inline bằng pyflakes.
