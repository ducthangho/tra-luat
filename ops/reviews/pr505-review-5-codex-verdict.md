verdict: changes_requested
reviewed_sha: 19337fad89ff7fdb47475105d7bdde6e910aedf0
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: 2a61f52b737688ebbe573517d8f199b23e3b400edc2f09539e93697a5e04ab6c
model_tu_khai: GPT-6 / Codex / OpenAI; khác nền tác giả phiên claude
review_round: 5
review_generation: 2; lượt 2
review_class: sensitive
hint_sha256: 27b2cc7f89235ec1f818e6a44e9d9362222d18c17abc612ba85880dcf15edbd1

Finding lượt trước **ĐÃ VÁ THẬT**. Workflow HEAD truyền đúng header ở biên Git/helper đã đo offline, kể cả với token giả dài. Còn **một P2 trong t152**: fixture quá ngắn khiến mutant bỏ `-w0` vẫn XANH; với token dài, cùng mutant sinh base64 nhiều dòng, header sai và command mask bị tách dòng. HINT thay đúng một dòng test, giữ tổng diff +80/−0. Không có phép đo token thật bị lộ hay HEAD fetch thất bại trên runner.

Hoàn tất lúc 2026-09-11T07:25:08Z. Bắt đầu theo yêu cầu: 2026-09-11T07:12:24Z; trong giới hạn 40 phút.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc/băm verdict và HINT gen2/lượt 1 trước các kiểm tra khác. Verdict SHA256 **83ee3cd4c4d11059328d9a5002e8fdfabad78d961af5b790c49c3f9971f8795b** khớp; HINT SHA256 **a4057e4a80ac787bfde38ac8b9877498a85f0dbfb62d7e868aa148cf5c7635fc**.

Slug `t152-bo-qua-co-shell-truoc-wf-blob` [P1]: **ĐÃ VÁ THẬT**.

| Hunk HINT trước | Tọa độ trong diff `2b52173..HEAD` | Toàn bộ thân hunk |
|---|---|---|
| `-5367,16 +5367,11` | Bằng | Bằng |
| `-5391,11 +5386,11` | Bằng | Bằng |
| `-5403,10 +5398,13` | Bằng | Bằng |
| `-5422,6 +5420,8` | Bằng | Bằng |

Đã áp HINT lên bytes test tại 2b52173 trong `scratch/prior-apply/`: `patch -p0` rc=0, kết quả **trùng byte toàn tệp HEAD**. Khác biệt phần tên hàm sau `@@` là ngữ cảnh Git tự thêm. Chỉ một commit mới, một tệp đổi; diff workflow từ 62c299a rỗng.

Tự dựng lại m13: test 2b52173 **SỐNG**, HEAD **GIẾT đúng (v)**. Tự chạy lại m1–m12: **12/12 GIẾT** đúng các chốt dưới bảng mutant. Không thấy hồi quy do bốn hunk này. M14 mới cũng SỐNG trên test 2b52173 khi đo lại, nên là thiếu sót còn sót, không phải bản vá lượt này sinh ra.

Bằng chứng: [so HINT](scratch/logs/prior-hint-round5.json), [ma trận mới](scratch/logs/mutants-round5.json). Không sử dụng số lượt trước thay phép đo lượt 5.

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 5 | Khớp? |
|---|---|---|---|
| Spec đóng băng | SHA256 b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; đường spec trong clone không tồn tại | Khớp bản cung cấp |
| Head/base | 19337fa / 27c413c3 | Đúng SHA đầy đủ đầu tài liệu | Có |
| Write set | Đúng 2 tệp, +11/+69 | `git diff --stat/--numstat 27c413c3..HEAD`: **2 tệp, +80/−0**; danh sách đường ở cả 5 commit trong khoảng này chỉ gồm hai tệp | Có |
| Master đã đi tiếp | Không chạm write set | `origin/master=26e2555d36c48b3c0f625ae50ab2cfb62b6cb858`; diff hai tệp `27c413c3..origin/master` rỗng | Có |
| Delta gen2/lượt 2 | Áp nguyên HINT, workflow không đổi | Bốn hunk bằng nhau, apply trùng byte; 1 commit mới | Có |
| t152 nền | ĐỎ đúng (i) | Test HEAD đọc workflow base: `TinHieuChotCa`, `(i) đoạn auth/fetch không chạy được: rc=1` | Có; base chưa có hàm t152 |
| t152/t148 HEAD | XANH | Gọi riêng cả hai đều XANH | Có |
| m13 | Test cũ xanh, test mới đỏ (v) | Đúng cả hai đối chứng | Có |
| m1–m12 | Tác giả nói chưa chạy lại lượt này | Reviewer tự chạy lại **12/12 GIẾT** | Không gán số reviewer cho tác giả |
| Suite HEAD | 147/147, không bỏ qua | `python3 ops/lease_publish_test.py`: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, bản sao nêu dưới |
| Wrapper HEAD | AL_VER=1.7.7, 147/147 | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có, offline AL_GOI |
| Lint workflow | actionlint + shellcheck rc=0 | actionlint **1.7.7**, shellcheck **0.9.0**, rc=0; debug xác nhận shellcheck chạy cả hai run block | Có; không có pyflakes |
| Whitespace / ca cũ | Không đổi ca cũ, diff sạch | `git diff --check` rc=0; AST sau bỏ riêng t152: base = HEAD = HINT | Có |
| Header tới fetch | Sửa thiếu xác thực | Git **2.43.0 fetch thật**, helper HTTPS offline: HEAD rc=0, đúng header, qua kiểm NHAN==TL_H; base/m5/m7 rc=128 | Có tại biên helper |
| URL và scope | Endpoint canonical, chỉ github.com | Helper HEAD nhận header; URL host đối chứng không nhận; dạng (b) và scope repo đều qua | Có ở config, không phải redirect |
| Credential scope | Một lời gọi, không config/argv | HEAD gọi 1 helper; Git/helper argv không token/base64; config fixture không đổi; helper con kế thừa header trong environment | Có, gồm cây tiến trình con |
| Bytes và shell | GNU -w0, mask trước fetch, unset | HEAD token giả 15/43/44/80 ký tự cho base64 đúng Python, không LF; success qua hậu kiểm unset; encoder/printf/Git lỗi dừng shell | Có trên Linux tại đây |
| m14 mới | Reviewer tìm mutant sống ngoài A1 | Bỏ `-w0`: t152/t148 **SỐNG**, lint rc=0. Token 80 ký tự: base64 **76+52**, header có LF, command mask thành 2 dòng | Thiếu nhánh fixture, xem P2 |
| Suite m14 | Kiểm toàn cổng có bỏ lọt không | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Xác nhận toàn cổng bỏ lọt |
| HINT | Sửa được trong write set/trần dòng | 1 hunk, thay 1 dòng fixture; dry-run/apply rc=0, byte bằng bản thử; +69 test/+11 workflow vẫn +80/−0 | Có |
| Ma trận HINT | Giữ dương, giết âm | HEAD/dạng (b)/scope repo XANH; base và **m1–m14 GIẾT** | Có |
| Suite HINT | Không hồi quy | **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0 | Có |

Bằng chứng: [metadata](scratch/logs/metadata-round5.json), [đường từng commit](scratch/logs/commit-paths-round5.log), [suite HEAD](scratch/logs/head-suite-round5.log), [rc suite HEAD](scratch/logs/head-suite-round5.json), [wrapper](scratch/logs/head-wrapper-round5.log), [rc wrapper](scratch/logs/head-wrapper-round5.json), [rc suite m14](scratch/logs/m14-suite-round5.json), [rc suite HINT](scratch/logs/hint-suite-round5.json), [lint/versions](scratch/logs/lint-versions-round5.json), [debug shellcheck](scratch/logs/actionlint-round5.log), [Git/helper](scratch/logs/git-probe-round5.json), [shell/bytes](scratch/logs/shell-round5.json), [m14](scratch/logs/m14-measurement-round5.json), [HINT](scratch/logs/hint-validation-round5.json).

**Cách chạy suite:** nguyên lệnh yêu cầu chạy ở `scratch/head-tree/`, chứa đầy đủ `ops/` và `.github/` sao từ HEAD, hai tệp review trùng băm. T82 gọi `copytree(HERE.parent, …)`; chạy trong clone sẽ đọc/sao cả các tệp bị cấm. Bản sao tuân thủ lệnh cấm và giữ đủ workflow, không cho ca tự qua vì thiếu workflow. TMPDIR nằm trong `scratch/tmp/`, tắt bytecode. M14/HINT dùng cùng cây này, mỗi cây chỉ thay đúng tệp tương ứng. Wrapper dùng `AL_GOI` cục bộ có SHA256 **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**, AL_VER=1.7.7 và TAR_OPTIONS=--no-same-owner; không tải mạng.

### Shell và mức kết luận fetch

- **Workflow 73:** `set -euo pipefail` thật sự chạy. Probe HEAD có cờ `ehuBc`, không `x`; m13 có `ehuxBc` và phát trace phép gán. T152 mới chạy cả đầu bước nên giết m13.
- **97:** `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định, quote biến, là Bash builtin và không thêm LF. `base64 -w0` GNU nhận bytes qua stdin, tạo một dòng. Đã so với base64 Python ở bốn độ dài. `$(...)` bỏ LF cuối, **không bỏ LF giữa chuỗi** — m14 chứng minh khác biệt này.
- Dưới `-e` + `pipefail`, encoder giả trả **9**, printf trả **8** đều dừng trước mask/fetch. TL_TOKEN chưa đặt bị `-u` chặn **1**. Những cờ này không xác minh token rỗng hay quyền token thật.
- **98:** `echo` builtin phát command đăng ký chính chuỗi base64 sau gán, trước fetch. HEAD chỉ có một dòng command kể cả token dài. Đây là phép đo bytes/thứ tự phát, không phải phép đo secret masker Actions.
- **99–104:** ba phép gán môi trường cùng continuation gắn với một simple command `git`. COUNT=1 chọn KEY_0/VALUE_0. KEY `http.https://github.com/.extraheader` khớp URL `https://github.com/$TL_KHO`; dòng 80 chốt kho canonical. Các `-c protocol…` không ghi đè header. Git 2.43.0 thực sự đọc cấu hình khi fetch và chuyển tới helper con. COUNT=0 làm helper mất header; protocol HTTPS=never bị Git từ chối trước helper.
- **105:** khi fetch thành công, `unset AUTH_B64` chạy; hậu kiểm AUTH_B64 và GIT_CONFIG_COUNT đều không còn đặt. Fetch trả 128 thì `-e` kết thúc shell trước unset/NHAN/receipt; không có lối tiếp tục chạy sau lỗi. Unset không phải xoá mọi bản sao bí mật trong bộ nhớ.
- **106–107:** probe thực thi `git rev-parse` và kiểm NHAN==TL_H bằng Git thật, với S/H khác nhau trong fixture; HEAD qua rồi mới in POST_OK. Helper quảng bá H đã tồn tại trong object store fixture, không truyền pack qua HTTP.

**ĐÚNG/ĐỦ:** HEAD sửa đúng phần thiếu credential trong phạm vi đã đo. Không đủ bằng chứng khẳng định fetch xanh trên runner thật: Git được chạy là 2.43.0, thuộc nhóm ≥2.31, nhưng không có binary 2.31/toàn dải phiên bản để đo; không mạng nên không kiểm GitHub token/ref, HTTP/TLS/redirect hoặc ảnh ubuntu-latest hiện hành. Probe thay riêng transport HTTPS bằng helper cục bộ kiểm header chính xác. Rc=128 của base/m14 là từ helper từ chối, **không phải** tái lập lỗi Username hay phản hồi GitHub. A3/canary sau land còn phải làm; giới hạn này tự nó không là finding P1/P2.

### Bề mặt token/base64

| Bề mặt | Kết luận trong phạm vi đo |
|---|---|
| Log | HEAD không bật xtrace. Trong auth block, base64 chỉ được phát trong command đăng ký mask. Log offline vẫn có command thô vì không có runner masker. M14 với token dài phát đuôi base64 ở dòng riêng không có tiền tố command. |
| `::add-mask::` | Mục đích là đăng ký giá trị cho log runner xử lý sau đó. Không bảo vệ output đã phát trước đăng ký, biến thể chưa đăng ký, argv, environment, memory, config hay artifact. Không coi một dòng command là phép đo che log thật. |
| argv tiến trình con | Probe ghi đối số Git/helper ngay trước exec: HEAD không chứa token/base64; base64 trên source chỉ nhận `-w0`, nhận dữ liệu bằng stdin. printf/echo là builtin nên không sinh argv của tiến trình ngoài. Dạng (b) spec cho phép có header trong argv; HEAD đang dùng (a). |
| Environment và ps | Helper đo được GIT_CONFIG_VALUE_0 có header và TL_TOKEN thô kế thừa; AUTH_B64 không export. “Một tiến trình” trong comment phải hiểu là một lời gọi fetch **cùng cây con**. Tiến trình đủ quyền đọc environment có thể thấy credential; masker không che kênh đó. Không đọc ps/proc của tiến trình ngoài fixture. |
| Config đĩa | Source không ghi auth config; `.git/config` của fixture không đổi bytes và không có credential sau fetch. |
| Curl sau fetch | Dòng 118 đưa TL_TOKEN thô vào argv curl đã có ở base. Đây là bề mặt có sẵn, không phải base64 mới do patch. Không gọi mask log là bảo vệ argv. |
| Receipt | Mã dựng receipt ở `ops/lease_publish.py:1772` và workflow 121–141 không serialize TL_TOKEN/AUTH_B64. Workflow hash lấy blob nguồn chưa expand secret. Chưa có artifact thật để readback; không nhận tín dụng “receipt thật sạch”. |

## Findings

### t152-fixture-ngan-bo-sot-base64-wrap [P2] Token fixture ngắn bỏ lọt nhánh base64 nhiều dòng

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5418` đặt `token = "m9-fixture-token"` (16 ký tự); **5432–5436** so header/mask chỉ với fixture đó. Dòng workflow chịu tác động mutant: `.github/workflows/ops-thu-hoi-admission.yml:97`.
- **VẤN ĐỀ:** m14 bỏ đúng `-w0` khỏi lệnh base64 trên bản sao. T152 và t148 HEAD vẫn XANH; actionlint+shellcheck rc=0. Prefix `x-access-token:` dài 15 bytes; cộng fixture 16 bytes chỉ tạo 44 ký tự base64, chưa đến ngưỡng GNU wrap 76. Vì command substitution bỏ LF cuối, mutant cho cùng giá trị như HEAD với fixture hiện tại. Với token giả 43/44 ký tự, base64 đo được 76+4; với 80 ký tự là **76+52**. LF giữa chuỗi còn nguyên: Git/helper nhận header khác chuỗi Basic đúng; `echo ::add-mask::…` phát dòng thứ hai gồm 52 ký tự đuôi base64, không có tiền tố command. Test bỏ sót nhánh độ dài của đúng thao tác vừa được patch. Spec không đặt trần độ dài TL_TOKEN.
- **ĐÃ THỬ VÁ:** HINT chỉ đổi fixture thành token giả ASCII **81 ký tự**, kèm comment giải thích >76 base64; giữ nguyên oracle Git/header/mask, không dò chuỗi `-w0`, không sửa workflow. Dạng (b) và scope repo vẫn được nhận. Một hunk/1 dòng thay, tổng so base vẫn +80/−0.
- **ĐÃ THỬ NGHIỆM:** m14 SỐNG ở t152 HEAD và test 2b52173, t148 XANH; lint rc=0. Probe shell đo bytes ở 15/43/44/80 ký tự, HEAD luôn đúng, m14 chỉ đúng ở 15. Fetch Git thật/helper với token 80: HEAD rc=0, đúng header, qua NHAN; m14 rc=128 vì **helper offline kiểm exact-header**, không phải phép đo HTTP thật. HINT giết m14 đúng (i), giữ HEAD/dạng (b)/scope repo XANH và base/m1–m13 ĐỎ. Dry-run/apply patch trùng byte; AST ngoài t152 không đổi. Suite m14 **147/147, rc=0**, xác nhận toàn cổng vẫn bỏ lọt; suite HINT **147/147, rc=0**, không bỏ qua ca nào.
- **ĐỘ TIN:** cao về mutant sống, ngưỡng wrap, bytes header/output và hiệu quả HINT. Xếp **P2 thiếu ca cho nhánh dữ liệu đo được**: HEAD hiện có `-w0` đúng; token giả dài không chứng minh độ dài GITHUB_TOKEN hiện hành, log thật bị lộ hoặc HEAD fetch đỏ. Không nâng thành P1 dựa trên giả định runner/mask chưa đo. Đây vẫn là P2 sửa được trong write set nên không đủ điều kiện approve.

Bằng chứng: [ma trận HEAD/cũ](scratch/logs/mutants-round5.json), [shell](scratch/logs/shell-round5.json), [tóm tắt m14](scratch/logs/m14-measurement-round5.json), [Git/helper](scratch/logs/git-probe-round5.json), [lint m14](scratch/logs/m14-lint-round5.log), [HINT ma trận/apply](scratch/logs/hint-validation-round5.json), [suite m14](scratch/logs/m14-suite-round5.log), [suite HINT](scratch/logs/hint-suite-round5.log).

## Mutant đã chạy

Dựng độc lập từ bytes HEAD trong `scratch/mutants/`. M1–m4 theo A1; m5–m13 dựng lại từ verdict trước. M2 lấy nguyên mẫu URL credential trong spec được cung cấp. M14 chỉ bỏ tùy chọn của encoder; không soạn nội dung đường dẫn thoát/khai thác.

| Mutant | Thay đổi | t152 HEAD | Lý do / phép đo độc lập | Sau HINT |
|---|---|---|---|---|
| m1 | KEY_0 → http.postBuffer | **GIẾT** | (i), rc=1, thiếu header | GIẾT (i) |
| m2 | URL credential theo mẫu A1 | **GIẾT** | (ii), URL mang credential | GIẾT (ii) |
| m3 | Thêm git config local extraheader | **GIẾT** | (iii), phát hiện lệnh ghi | GIẾT (iii) |
| m4 | persist-credentials true | **GIẾT** | (iv), checkout sai | GIẾT (iv) |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; Git/helper thiếu header, rc=128 | GIẾT (i) |
| m6 | VALUE_0 dummy | **GIẾT** | (i), header không bằng token fixture | GIẾT (i) |
| m7 | Ghi đè AUTH_B64 từ TL_KHO | **GIẾT** | (i), header sai; Git/helper rc=128 | GIẾT (i) |
| m8 | Xóa add-mask | **GIẾT** | (v), thiếu command đăng ký | GIẾT (v) |
| m9 | KEY thành http.extraheader toàn cục | **GIẾT** | (i), rc=94, host đối chứng có header | GIẾT (i) |
| m10 | Fetch thứ hai sau NHAN, --quiet --no-tags, không header | **GIẾT** | Đếm 2; Git/helper gọi 2 lần, lần sau thiếu header, rc=128 | GIẾT, đếm 2 |
| m11 | protocol.https.allow=never | **GIẾT** | (i), rc=95; Git thật rc=128 trước helper | GIẾT (i) |
| m12 | set -x ngay trước AUTH_B64 | **GIẾT** | (v), stderr có trace | GIẾT (v) |
| m13 | Thêm -x vào set đầu bước | **GIẾT** | (v), chạy trạng thái shell thật; test 2b52173 SỐNG | GIẾT (v) |
| m14 reviewer | Bỏ -w0 của base64 | **SỐNG** | Fixture 16 ký tự không wrap; token 80 cho base64 76+52/header sai/command mask tách dòng | GIẾT (i) |

**Tín dụng t152 HEAD: 13 GIẾT / 1 SỐNG.** Không nhận công HINT giết m14 cho PR hiện tại. M14 là mutant sống ngoài bốn ca A1 yêu cầu tìm; không gộp các catalogue mutant nội bộ của 146 ca cũ vào mẫu số này.

Script tái lập: `scratch/review_matrix.py`, `scratch/probe_runtime.py`, `scratch/finish_measurements.py`, `scratch/validate_hint.py`, `scratch/run_gates.py`. Lần đầu helper trả thừa dòng trống lúc Git đóng pipe, tạo BrokenPipeError của fixture; đã sửa trạng thái kết thúc protocol rồi **chạy lại toàn probe**. Log cuối Git/helper không có lỗi fixture đó; log thử đầu giữ riêng `scratch/logs/git-probe-initial-helper-error.json`, không dùng thay bằng chứng cuối.

## Đối chiếu EVIDENCE.md

Các số +50/+79 thuộc lịch sử lượt 1/2, được các phần sau cập nhật +80; không coi việc giữ lịch sử là khai sai HEAD. Gen2/lượt 2 khai áp nguyên HINT, một commit, workflow không đổi, m13 cũ sống/mới đỏ, t152/t148 và suite HEAD xanh: tự đo lại khớp. Tác giả nói rõ **chưa chạy lại m1–m12** ở lượt này; reviewer đã chạy lại, không gán công cho tác giả.

EVIDENCE ghi rõ **chưa đo runner thật và mask thật**; không có lời khai đã nghiệm thu A3 hay giết mọi mutant. M14 là thiếu sót fixture mới đo được, không chứng minh tác giả khai gian các phép thử đã nêu. Mốc giờ riêng tác giả, Issue/comment/run lịch sử, lease/reroute và thao tác khôi phục cây không xác minh độc lập khi không mạng. Quyền review gen2/lượt 2/trần vòng nhận theo chỉ thị trực tiếp người dùng, không đọc doctrine hay xin lại phép.

## HINT và phạm vi kiểm

`HINT.patch` là unified diff cho `patch -p0` từ gốc `cay-kho/`, dựa trên đúng HEAD. **1 hunk, chỉ `ops/lease_publish_test.py`**. Dry-run và apply trong `scratch/hint-apply/` rc=0; bytes bằng bản sửa thử. Workflow nguyên byte; AST các ca cũ/helpers nguyên; so lease base vẫn +69 test/+11 workflow = +80/−0. Sửa được P2 duy nhất trong hai tệp cho phép.

T152 vẫn là phép đo Bash + Git config với stub fetch, không phải parser toàn bộ Bash hay HTTP test. Stub rev-parse chỉ cấp preflight fixture; nó không chứng minh nguồn S/blob. Probe độc lập chạy Git thật, thay transport HTTPS bằng helper offline; không tiếp xúc GitHub. Không chủ động sửa tracked files/index, không checkout, commit hay đổi ref trong `cay-kho/`; không đọc các tệp doctrine bị cấm, không dùng mạng hoặc đọc nội dung tệp ngoài cwd. Mọi mutant/fixture/bản sửa thử nằm trong `scratch/`.

## chua_do_duoc

1. Fetch xanh trên GitHub runner thật, GITHUB_TOKEN/quyền contents:read với ref kho thật, HTTP/TLS/redirect, toàn job. A3 sau land chưa thực hiện.
2. Secret masker Actions và log/artifact thật. Đã đo bytes/command do Bash phát; mọi token ở phép thử là fixture công khai. Độ dài GITHUB_TOKEN hiện hành **chưa đo**; không coi token giả 80 ký tự là thông tin về token thật.
3. Receipt thật cùng check_run_id, workflow_definition_commit, workflow_definition_sha256, checker_rc. Đọc mã dựng receipt không thay readback artifact.
4. Git binary 2.31/toàn dải 2.31+, Windows, macOS/BSD base64, ảnh ubuntu-latest hiện hành. Đã chạy Linux, Git 2.43.0, Bash 5.2.21, GNU base64 9.4, Python 3.11.15, actionlint 1.7.7, shellcheck 0.9.0.
5. Ps/environment/memory dump ngoài fixture hoặc bảo đảm unset xoá sạch bộ nhớ. Environment của helper fixture có header đã đo; add-mask không bảo vệ kênh ấy.
6. Timeline Issue/comments/run/lease, thao tác tác giả, tuyên bố lịch sử “mọi PR/không bao giờ xanh”. Chỉ snapshot/diff/băm và hành vi offline được xác minh độc lập.
7. Wrapper tải mạng nguyên dạng. Wrapper kiểm ở đây dùng gói AL_GOI cục bộ đã ghim băm. Suite chạy trên bản sao ops/.github để tuân thủ lệnh cấm đọc doctrine; không gọi đó là chạy trực tiếp trong clone. Pyflakes không có, không nhận tín dụng kiểm Python inline từ actionlint.
