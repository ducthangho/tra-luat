verdict: changes_requested
reviewed_sha: 62c299aa9674aade08263504399539eb60eb89b7
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: 47fe99e88f25eecae6a83c6bb1357a14362e61a9320ce938d6d976fdb99d29ed
model_tu_khai: GPT-6 / Codex / OpenAI; reviewer khác nền với phiên tác giả claude
review_round: 1
review_class: sensitive
hint_sha256: 9f3a5d4ca2b7ebc69e7a4d21a11eae062e96081a79ab7c14dc9554fb408f7437

Bản vá workflow có cấu trúc đúng để khắc phục fetch thiếu xác thực. Đã đo được header hiệu lực qua Git thật ở sandbox, nhưng chưa thể kết luận fetch xanh trên GitHub runner thật. Yêu cầu sửa vì **t152 có đột biến SỐNG tại chốt chịu lực**: COUNT=0 và ghi đè AUTH_B64 đều được test nhận, dù làm mất/sai xác thực. Có thêm chốt mask chưa được test bảo vệ. Cả hai finding sửa được trong write set; HINT chỉ sửa `ops/lease_publish_test.py`.

Phạm vi: không mạng, không đọc các tệp doctrine bị cấm, không checkout/reset/commit/sửa tệp tracked ở `cay-kho/`. Tất cả workflow đột biến và sửa thử nằm dưới `scratch/`. Bộ test được chạy với thư mục tạm trong cwd và tắt ghi bytecode; một tệp bytecode phát sinh ở lượt kiểm dạng (b) riêng đã được xoá lại. HEAD, trạng thái git và hai băm tệp được kiểm lại.

## BẢNG ĐO

| Khẳng định | PR khai / nguồn yêu cầu | Đo được | Khớp? |
|---|---|---|---|
| Spec đóng băng | `b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac` | Băm `nguon/M9-FETCH-AUTH.md` đúng toàn bộ 64 hex | Có |
| HEAD / base | `62c299a` / `27c413c3` | Hai SHA đầy đủ đúng metadata trên | Có |
| Write set / số dòng | Workflow +11/−0; test +50/−0 | `git diff --stat/--numstat 27c413c3..HEAD`: đúng hai tệp, +61/−0 | Có |
| Nội dung ngoài hai tệp trong diff PR | Không có | Không có tệp thứ ba trong diff; trạng thái git sạch | Có; không suy ra lịch sử thao tác chưa commit của tác giả |
| `origin/master` đã đi tiếp | 27 commit, không chạm write set; prompt nói chỉ reviews/CHANGELOG/manifest | `4b5184e21373eb8f8a36493d0282ebd020bb4458`, 27 commit; **còn chạm `ops/cong_cu.py`**. Diff hai tệp write set giữa base và origin/master rỗng | Không khớp danh sách tổng; khớp điều kiện không chạm write set, không kích hoạt S4 |
| t152 trên nền | ĐỎ đúng (i) | Nạp t152 của HEAD, trỏ tới bytes workflow lấy bằng `git show 27c413c3:...`: `TinHieuChotCa`, thông điệp bắt đầu `(i) fetch H không mang ...` | Có; nền chưa có t152 nên không gọi hàm vốn không tồn tại ở nền |
| t152 / t148 HEAD | QUA / QUA | Cả hai XANH khi gọi riêng | Có |
| m1–m4 | ĐỎ đúng (i)/(ii)/(iii)/(iv) | Tự dựng lại bốn bản sao, bốn lỗi đúng nhánh độc lập | Có |
| Bộ test HEAD | Kỳ vọng 147/147 | `python3 ops/lease_publish_test.py`: **147/147**, đã chạy=147, bỏ qua=0, rc=0 | Có |
| Wrapper | `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh`: 147/147, rc=0 | Dùng gói có sẵn qua AL_GOI, băm gói đúng pin. Lượt đầu rc=5 vì tar không đổi được ownership trong sandbox. Với `TAR_OPTIONS=--no-same-owner`: **147/147**, bỏ qua=0, rc=0 | Khớp kết quả với điều kiện môi trường ghi rõ; không tái lập tải mạng |
| Actionlint + shellcheck | 1.7.7, rc=0 | Binary `nguon/actionlint/actionlint` 1.7.7, shellcheck 0.9.0 ở PATH; `-debug -shellcheck=shellcheck` ghi hai lần gọi shellcheck, 0 lỗi, rc=0 | Có |
| Whitespace | `git diff --check` sạch | `git diff --check 27c413c3..HEAD` rc=0 | Có |
| Header được Git sử dụng | Chưa có phép đo runner thật | Git **2.43.0** fetch thật qua remote helper cục bộ thay transport: HEAD rc=0, helper nhận đúng header; m5/m7 rc=128 với thiếu/sai header | Có ở biên helper/config, không phải HTTP GitHub |
| Header đúng host | URL cấu hình và fetch cùng github.com | `git config --get-urlmatch http.extraheader` bên trong helper: URL canonical rc=0, host đối chứng khác rc=1 và không có header | Có trên Git cục bộ |
| Mask trên GitHub / receipt thật | EVIDENCE ghi KHÔNG ĐO ĐƯỢC | Không có runner/token/artifact thật, không gọi mạng | Giữ đúng giới hạn |
| HINT | Reviewer đề xuất | `patch --dry-run -p0` và apply thật trên bản sao đều qua; kết quả byte bằng bản sửa thử. t152 HEAD và dạng (b) XANH, base/m1–m9 ĐỎ | **Full suite HINT cuối 147/147, đã chạy=147, bỏ qua=0, rc=0**; hai lượt đầu lỗi fixture được ghi riêng bên dưới |
| Trần sau HINT | Hai tệp, ≤80 dòng thêm | So với lease base: workflow +11/−0, test +62/−0 = **+73/−0** | Trong trần |

Log chính: [HEAD suite](scratch/logs/head-suite.log), [HINT cuối đầy đủ](scratch/logs/hint-suite-complete-ops.log), [wrapper lượt đầu](scratch/logs/head-wrapper.log), [wrapper điều chỉnh tar](scratch/logs/head-wrapper-no-same-owner.log), [actionlint có trace gọi shellcheck](scratch/logs/actionlint.log), [mutant gốc](scratch/logs/mutants-original.json), [probe Git](scratch/logs/git-fetch-probe.json), [probe shell](scratch/logs/shell-probe.log), [mutant với HINT cuối](scratch/logs/hint-mutants-final.json).

### Shell và cấu hình Git — kết luận theo từng dòng thay đổi

- **Dòng 97:** `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định, quote token, không thêm LF. Trên Bash đo được `printf` là builtin; token không trở thành argv của một tiến trình printf bên ngoài. `base64 -w0` chạy với argv chỉ chứa `-w0`, nhận dữ liệu qua pipe. GNU coreutils 9.4 tại đây nhận `-w0`, không wrap; giải mã kết quả bằng Python khớp chính xác bytes đầu vào, không có LF phụ. `$(...)` bỏ LF cuối nếu có; với `-w0` không có LF để bỏ.
- **Dòng 97 dưới `set -euo pipefail`:** gán hoàn tất trước dòng mask. Dùng token giả, làm base64 trả 9 hoặc printf trả 8 khiến cả đoạn dừng đúng rc, chưa mask/chưa fetch. TL_TOKEN chưa đặt sẽ bị `-u` chặn; token rỗng vẫn mã hoá được nhưng không chứng minh được quyền truy cập — cần token GitHub hợp lệ.
- **Dòng 98:** echo là builtin; chuỗi base64 được đăng ký mask trước khi chuyển header cho Git. Base64 chuẩn không có LF hoặc ký tự định dạng workflow-command cần escape trong giá trị này. Shell hiện tại không bật `set -x`; cờ đo được là `ehuBc`. Dòng echo mang chuỗi thật tới kênh điều khiển stdout của runner; đó là cơ chế đăng ký, không phải mã hoá bí mật.
- **Dòng 99–104:** ba phép gán đứng trước cùng một simple command, nhờ các continuation; không phải các gán tồn tại toàn bộ bước. KEY đúng `http.https://github.com/.extraheader`; VALUE đúng `AUTHORIZATION: basic <base64(x-access-token:token)>`; COUNT=1 bật đúng cặp key/value này. Các `-c protocol...` có key khác nên không ghi đè extraheader. Endpoint fetch đã được chốt ở dòng 80 là `ducthangho/tra-luat`, host HTTPS là github.com, khớp URL scope. Không có host khác trong lệnh fetch hiện tại.
- Giao diện `GIT_CONFIG_COUNT/KEY_n/VALUE_n` là cơ chế cấu hình runtime Git thuộc baseline 2.31+ được hỏi. **Phép đo phiên này chỉ thực thi Git 2.43.0**, không có phép đo riêng binary 2.31 hoặc phiên bản runner tương lai. Đã chạy chính `git fetch`, không chỉ gọi config ở tiến trình cha: remote helper con vẫn nhận cấu hình, URL matching trả header đúng. Helper giả sử dụng ref/object có sẵn để hoàn tất fetch, không làm HTTP/TLS hay GitHub auth.
- **Dòng 105:** khi fetch thành công, `unset AUTH_B64` chạy; probe hậu điều thấy AUTH_B64 và GIT_CONFIG_COUNT không còn đặt trong shell. Khi fetch trả 128, `-e` kết thúc shell trước `unset`; không chạy tiếp tới NHAN/checker/receipt. Đây không phải leak kéo dài sang bước sau; shell đã chết. `unset` không phải thao tác xoá an toàn mọi bản sao trong bộ nhớ.
- **Dòng 106–107:** không đổi; đối chiếu OID nhận được với TL_H vẫn còn. Patch không biến một PR ref đã đổi trong lúc chạy thành thành công giả.

**ĐÚNG và ĐỦ tới đâu:** đúng cơ chế truyền credential đang thiếu; đủ để Git tại biên transport thấy header canonical. Fetch xanh trên runner còn phụ thuộc token thực có quyền, ref tồn tại, mạng/TLS, ảnh runner và các chốt preflight. Không có bằng chứng cục bộ nào thay được canary A3.

### Bề mặt lộ token/base64 và giới hạn của mask

| Bề mặt | Nhận định cho HEAD |
|---|---|
| Log bước hiện tại | Không có lệnh in AUTHORIZATION trong đoạn fetch; dòng mask đứng trước fetch. Không bật xtrace. Log cục bộ của probe thấy dòng `::add-mask::...` nguyên văn vì **không có bộ lọc Actions**; mọi giá trị trong probe đều là fixture công khai, không phải secret. |
| `::add-mask::` | Yêu cầu runner che các lần xuất hiện khớp giá trị đã đăng ký trong log được runner xử lý sau khi đăng ký. Không chứng minh che được dữ liệu đã in trước đó, biến thể mã hoá/biến đổi, tệp, artifact, argv hay environment. Nếu xtrace bị bật từ trước, gán AUTH_B64 có thể được trace trước khi đăng ký mask; HEAD không bật chế độ đó. Không đo mask thật bằng giả lập echo. |
| argv của fetch / helper | Lệnh fetch có protocol flags, URL sạch, refspec; không có token/base64. Probe ghi argv helper và xác nhận không có header. `printf` và `echo` là builtin; base64 nhận payload qua stdin. Dạng (b) dùng `-c` sẽ đặt header trong argv; HEAD dùng dạng (a). |
| Environment của tiến trình con | **Có header trong `GIT_CONFIG_VALUE_0`**, kể cả helper con; probe đo trực tiếp. TL_TOKEN vốn là env của cả step nên cũng được con kế thừa. AUTH_B64 riêng không export. Vì vậy “một tiến trình” nên hiểu là **một lời gọi fetch và cây tiến trình con**, không phải đúng một PID và cũng không phải bí mật với tiến trình cùng quyền. |
| `ps` / quan sát máy | `ps` chỉ hiển thị argv thông thường không thấy base64 mới từ cách (a); công cụ có quyền đọc environment có thể thấy nó. Mask log không bảo vệ bề mặt này. Không đọc môi trường tiến trình thật bên ngoài cwd để thử; chỉ đo environment của helper bằng fixture. Không thấy đường chạy mã PR mới trên runner trong diff này. |
| Curl sau fetch, dòng 118 | Token thô đã có trong argv của `curl -H "Authorization: Bearer ..."` từ base. Đây là bề mặt **có sẵn**, không phải leak base64 do patch; mask Actions không che argv ở hệ điều hành. Không đưa việc đổi curl ngoài mục tiêu patch thành finding mới. |
| Config / receipt / artifact | Không gọi git config để ghi trong auth block. Probe sau fetch thấy config repo không có extraheader/token. Đọc phần dựng receipt ở `ops/lease_publish.py:1772` và phần bổ sung workflow 121–141: không serialize AUTH_B64/TL_TOKEN/GIT_CONFIG_VALUE_0; chỉ thêm định danh và kết quả. Băm blob định nghĩa là băm mã có tên biến, không phải mã đã thay secret. Chưa đọc artifact thật nên không tuyên bố artifact đã được kiểm sạch. |

## Findings

### t152-khong-do-header-hieu-luc [P1] COUNT bằng 0 hoặc base64 bị ghi đè vẫn qua chốt xác thực

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5404–5411`, đặc biệt phép `co_header` và phép tìm chuỗi TL_TOKEN trong toàn văn workflow. Dòng sản phẩm liên quan: workflow 97–101.
- **VẤN ĐỀ:** t152 chỉ nhận diện tên KEY_0, không đo COUNT hay giá trị mà Git đọc; việc có một chuỗi gán đúng ở bất kỳ đâu không chứng minh giá trị cuối tới fetch. Đổi riêng COUNT=1 thành COUNT=0 khiến Git bỏ header nhưng t152 vẫn XANH. Giữ nguyên phép gán đúng rồi ghi đè AUTH_B64 từ TL_KHO cũng vẫn XANH. Theo thang của lượt này đây là **P1 do đột biến sống ở chốt chịu lực**, không phải kết luận rằng workflow HEAD hiện tại đã fetch sai.
- **ĐÃ THỬ VÁ:** `HINT.patch` thay phép dò co_header/TL_TOKEN bằng việc chạy chính auth block của workflow với Bash, token giả và môi trường config rỗng; hàm thay transport chuyển các `-c` vào **Git config thật**, lấy header hiệu lực theo URL thực của lời gọi. So bytes với base64 tính độc lập bằng Python, kèm đối chứng host khác phải không có header. Vẫn giữ chốt URL, ghi config và checkout độc lập; nhận cả dạng env (a) và `-c` (b).
- **ĐÃ THỬ NGHIỆM:** t152 gốc m5/m7 SỐNG. Probe `git fetch` thật với helper cục bộ: HEAD rc=0/header đúng; m5 rc=128/header vắng; m7 rc=128/header sai. Actionlint + shellcheck vẫn rc=0 trên m5/m7. HINT: HEAD và đối chứng dạng (b) XANH; base/m1/m5 ĐỎ (i); m7 ĐỎ vì header hiệu lực không dẫn từ TL_TOKEN; m2/m3/m4 vẫn ĐỎ đúng (ii)/(iii)/(iv). Patch áp dụng thành công trên bản sao; không sửa workflow sản phẩm.
- **ĐỘ TIN:** cao, có đối chứng dương và phân biệt cấu hình thật/chuỗi hiện diện. Không suy rc=128 fixture thành log lỗi GitHub thật.

### t152-khong-khoa-dang-ky-mask [P2] Xoá dòng mask vẫn qua toàn bộ chốt mới

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5385–5415`; thuộc tính cần bảo vệ nằm ở workflow 97–98.
- **VẤN ĐỀ:** phần bảo vệ chuỗi secret đã biến đổi được thêm cùng patch nhưng t152 không kiểm đăng ký mask hoặc thứ tự trước fetch. m8 xoá riêng echo add-mask vẫn XANH; lint cũng XANH. Đây là chốt hồi quy độc lập còn thiếu. **HEAD đang có mask đúng vị trí; chưa đo thấy token thật bị lộ.** Bốn mục M2 của spec không tự cung cấp bằng chứng cho thuộc tính mask bổ sung này.
- **ĐÃ THỬ VÁ:** cùng `HINT.patch` thêm chốt (v): stdout từ auth block với fixture phải gồm đúng đăng ký mask của base64 kỳ vọng trước dòng header đo ở lời gọi Git; kiểm cả dọn AUTH_B64 sau thành công. Không dùng secret thật.
- **ĐÃ THỬ NGHIỆM:** gốc m8 SỐNG; HINT m8 ĐỎ đúng (v), HEAD XANH. Probe shell xác nhận thứ tự mask → fetch → unset trên HEAD; làm fetch fail thì script dừng trước phần hậu kiểm. Phép này kiểm workflow phát lệnh đăng ký đúng, không kiểm bộ lọc log GitHub.
- **ĐỘ TIN:** cao về thiếu test/thứ tự phát command; không có khẳng định leak thực tế.

## Mutant đã chạy

Tất cả là thay đổi vào bản sao dưới `scratch/mutants/`; mỗi ca khôi phục từ bytes HEAD độc lập. Cột GIẾT/SỐNG dưới đây đánh giá **t152 gốc của PR**. Không nhận tín dụng của HINT cho test gốc.

| Mutant | Thay đổi | t152 gốc | Lý do / phép đối chứng | Sau HINT |
|---|---|---|---|---|
| m1 (A1) | KEY_0 extraheader → http.postBuffer | **GIẾT** | TinHieuChotCa (i): không có header trên lời gọi | GIẾT (i) |
| m2 (A1) | URL mang credential theo mẫu spec đã cung cấp | **GIẾT** | (ii): URL chứa credential; chốt (i) gốc đã qua | GIẾT (ii) |
| m3 (A1) | Thêm git config --local ghi extraheader trước fetch | **GIẾT** | (iii): phát hiện ghi config; các chốt trước đã qua | GIẾT (iii) |
| m4 (A1) | persist-credentials false → true | **GIẾT** | (iv): checkout không giữ false | GIẾT (iv) |
| **m5 (reviewer)** | **GIT_CONFIG_COUNT=1 → 0** | **SỐNG** | KEY vẫn có mặt nên t152 nhận; Git thật bỏ toàn bộ cặp cấu hình, helper không có header, fixture fetch rc=128 | GIẾT (i) |
| m6 (reviewer) | VALUE_0 thành header hằng dummy | **GIẾT** | Dòng fetch mất AUTH_B64/TL_TOKEN nên rơi chốt dẫn nguồn (i). Không nhận công cho khả năng bắt mọi header sai | GIẾT (i) |
| m7 (reviewer) | Sau gán đúng, ghi đè AUTH_B64 bằng base64 từ TL_KHO | **SỐNG** | Phép tìm chuỗi gán đúng trong toàn văn vẫn thoả; header thực mang giá trị sai, fixture fetch rc=128 | GIẾT (i) |
| m8 (reviewer) | Xoá riêng echo add-mask | **SỐNG** | t152 không có chốt mask; fetch cấu hình vẫn đúng nên probe transport rc=0 | GIẾT (v) |
| m9 (đối chứng giữ phạm vi) | KEY_0 thành http.extraheader không giới hạn host | **GIẾT** | Gốc bắt thiếu tên key có scope (i); HINT bắt header cũng xuất hiện ở host đối chứng, rc=94 | GIẾT (i) |

Đối chứng: base ĐỎ (i), HEAD XANH, t148 HEAD XANH; dạng (b) của spec với mask giữ nguyên cũng XANH ở cả test gốc và HINT. Đã chạy chín mutant, **gốc giết 6 / sống 3**. Không nâng số tín dụng bằng các mutant thuộc suite cũ có trong log 147 ca.

## Đối chiếu EVIDENCE.md

Các số đo tại EVIDENCE dòng 7–17 tái lập được với giới hạn môi trường wrapper nêu trong bảng. EVIDENCE dòng 22 **đã tự ghi** chưa đo runner và mask thật; không có cơ sở gọi đó là lời khai đã đo mà không đo. Các mốc lịch sử của tác giả, kết quả run #500, số comment, thao tác khôi phục worktree và việc “mọi PR” trước patch bị lỗi **không được kiểm độc lập qua mạng**; review này không dùng chúng làm kết quả đo mới.

Lời khai rộng hơn phép đo nằm cụ thể ở **docstring/logic t152** (“giá trị dẫn từ TL_TOKEN”) và mô tả workflow “t152 khoá”, thể hiện bằng m5/m7/m8. Bốn mutant khai trong EVIDENCE bị giết thật đúng lý do; điều đó không có nghĩa chốt (i) đã đo đầy đủ xác thực hiệu lực. Sai lệch danh sách đường trên origin/master thuộc prompt, không phải EVIDENCE.

## HINT và cách áp dụng

`HINT.patch` là unified diff so với **HEAD đang review**, đường tương đối từ gốc `cay-kho/`, áp dụng bằng `patch -p0`. Chỉ có hunk cho `ops/lease_publish_test.py`, xử lý cả P1 và P2. Không cần tệp thứ ba; sau áp dụng tổng diff với lease base là +73 dòng, còn trong trần +80. Bản HINT cuối đã dry-run và apply bằng `patch -p0` trên `scratch/final-apply/`, cmp bằng bytes với `scratch/hint-tree/`; full suite cuối đạt 147/147, rc=0. AST bên ngoài t152 không thay đổi.

Giới hạn HINT: đây là kiểm hành vi đoạn shell hiện có giữa WF_BLOB và NHAN, dùng `_dong_lenh` của suite để nối continuation; không phải bộ phân tích bảo mật mọi cú pháp shell. Hàm git giả không đo transport HTTP. Phép probe Git thật của reviewer được giữ riêng trong `scratch/probe_git_fetch.py`; không đưa nó thành dependency sản phẩm.

Lịch sử kiểm HINT được giữ đầy đủ: lượt đầu 144/147, rc=1 vì bản sao reviewer thiếu ops/reviews và ops/leases; lượt hai 146/147, rc=1 vì thiếu ops/prompts mà lease tham chiếu. Sau khi chép toàn bộ ops và áp lại HINT cuối, lượt full đạt **147/147, rc=0**. Đây là lỗi dựng fixture của reviewer đã khắc phục. Log lỗi: [lượt đầu](scratch/logs/hint-suite.log), [lượt hai](scratch/logs/hint-suite-with-fixtures.log). Không quy các lỗi ấy cho tác giả và không xoá dấu vết lỗi để nhận kết quả xanh.

## chua_do_duoc

1. Canary GitHub thật sau land: token `contents: read` có fetch được refs/pull của kho này, rc/conclusion thực tế, HTTP/TLS/redirect, và các chốt khác của cả job. Không có mạng, không chạy Actions, không tự nâng quyền.
2. Mask trên log runner thật, cả chế độ debug và bộ lọc runner; không có secret thật trong các phép thử. Chỉ đo phát command đúng/thứ tự đúng với fixture.
3. Artifact/receipt thật và các trường M3 (`check_run_id`, `workflow_definition_commit`, `workflow_definition_sha256`, `checker_rc`). Source review không thay thế đọc artifact.
4. Binary Git 2.31 và ảnh `ubuntu-latest` hiện hành không được chạy. Cục bộ đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4; không đo Windows.
5. Không thử đọc environment/argv của tiến trình ngoài fixture hoặc kiểm memory dump. Environment của helper con trong fixture có header; đó là giới hạn thực của cách dùng env và của add-mask.
6. Không xác minh trạng thái lease khác/S5, các Issue/comment/run lịch sử hoặc timeline thao tác tác giả bằng mạng. Chỉ xác minh snapshot git được cung cấp và write set thực tế.
7. Wrapper tải mạng nguyên dạng không chạy được trong điều kiện cấm mạng; bản offline cần `TAR_OPTIONS=--no-same-owner` do ownership sandbox. Lượt lỗi rc=5 được giữ, không quy cho patch hai tệp.
