verdict: changes_requested
reviewed_sha: 6254570b0604b42f9474091b9818dba9cd2b8704
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/ops-thu-hoi-admission.yml: 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23
  ops/lease_publish_test.py: f51a0cf9e4af56e165ee02f35838c8f4b54f5e70c830aa19889ffd7fa9894223
model_tu_khai: GPT-6 / Codex / OpenAI; reviewer khác nền tác giả claude
review_round: 2
review_class: sensitive
hint_sha256: ebb87804eb7d1f4d8519aa671ccdbc1e6c5d5610d06f5cbf716d8a2331e3c2d8

Hai finding lượt 1 **đã vá thật**. Workflow HEAD truyền đúng header ở biên Git/helper đo được tại đây. Tuy nhiên, t152 vẫn bỏ sót fetch thứ hai thiếu xác thực khi thứ tự cờ thay đổi (m10 SỐNG); đây là P1 theo thang review. Có thêm thiếu sót độc lập của stub ở quyết định cho phép HTTPS (m11, P2). HINT sửa test trong write set; tổng diff sau HINT **+80/−0**. Không có số đo fetch hoặc mask trên runner GitHub thật.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc, băm hai tài liệu và đối chiếu HINT trước các phép review khác:

- `nguon/VERDICT.rvm9-1.md`: **a0bb40dc74b6029f0456bf18f61cc5a626669a3575a1a8c89347dd421b1eace9** — khớp.
- `nguon/HINT.rvm9-1.patch`: **9f3a5d4ca2b7ebc69e7a4d21a11eae062e96081a79ab7c14dc9554fb408f7437** — khớp.

Lấy bytes test từ `git show 62c299a:ops/lease_publish_test.py`, áp HINT bằng `patch -p0` vào `scratch/prior-apply/`: rc=0. So kết quả với HEAD theo toàn tệp, bỏ đúng nút docstring t152: **prefix bytes bằng nhau; suffix bytes bằng nhau**. HINT chỉ có một hunk; mọi thay đổi logic trong hunk khớp byte. `git diff 62c299a..HEAD` chỉ có test; workflow không đổi. Khác duy nhất docstring, thêm 6 dòng so HINT. [Bằng chứng so bytes](scratch/logs/prior-hint-comparison.json).

| Slug lượt 1 | Phân loại | Bằng chứng tự đo lượt 2 |
|---|---|---|
| `t152-khong-do-header-hieu-luc` [P1] | **ĐÃ VÁ THẬT** | HEAD XANH; workflow base ĐỎ (i), rc=1. m5 COUNT=0 ĐỎ (i), rc=1; m7 ghi đè AUTH_B64 ĐỎ (i), header không dẫn từ TL_TOKEN. Git fetch thật qua helper cục bộ: HEAD rc=0/header đúng; m5/m7 rc=128/header thiếu hoặc sai. |
| `t152-khong-khoa-dang-ky-mask` [P2] | **ĐÃ VÁ THẬT** | m8 xoá mask ĐỎ đúng (v); HEAD XANH. Probe shell phát mask trước fetch; hậu kiểm sau thành công xác nhận AUTH_B64 và COUNT không còn đặt. Phép đo chỉ kiểm phát command đăng ký, không kiểm bộ lọc log của Actions. |

Đã dựng lại và chạy **đủ m1–m9**, không chép số đo cũ: đều GIẾT đúng nhánh, kể cả m1–m4/m6/m9. [Log mới](scratch/logs/mutants-round2.json). Để phân biệt lỗ mới phát hiện với hồi quy do HINT, còn nạp test cũ 62c299a và chạy lại: m10/m11 cũng SỐNG ở test cũ. Chúng là thiếu sót còn sót, không phải HINT làm hỏng hai cách vá m5/m7/m8. [Ma trận ba phiên bản test](scratch/logs/hint-matrix-round2.json).

**Docstring:** lời khai hiện tại về cách chạy Bash, chuyển `-c` cho Git config, host đối chứng và m1–m9 phù hợp số đo mới. Lịch sử run #500, “mọi PR/không bao giờ xanh” vẫn chỉ là dẫn lại sự kiện của tác giả/spec, KHÔNG ĐO ĐƯỢC offline. Docstring nói rõ dùng stub/config; không khai đã chạy HTTP thật. Không dùng lịch sử ấy làm bằng chứng HEAD fetch xanh.

**Chốt mới có giới hạn nào:**

- Dạng (a) HEAD và dạng (b) `git -c "http.…extraheader=…"` đều XANH ở t152 và probe Git thật.
- Thêm cờ hợp lệ `--quiet` vào một fetch: Git thật rc=0, header đúng; t152 ĐỎ rc=91 vì stub đòi đúng bốn đối số sau các `-c`. Đây là giới hạn có thật về cú pháp được nhận. Không nâng riêng thành finding: hai dạng đã đóng băng trong Q1 đều được nhận, HEAD không dùng cờ thêm. Nếu đổi hình dạng fetch sau này phải cập nhật adapter/test. Thử `-c` dính liền key: **Git 2.43 cũng từ chối rc=129**, nên không gọi đây là dạng hợp lệ bị stub bỏ sót.
- KEY scope riêng repo canonical: t152 XANH, probe Git nhận đúng header; KEY đổi sang host khác: t152 ĐỎ (i), probe thiếu header/rc=128. Scope toàn cục m9: Git nhận header cả host đối chứng và t152 giết rc=94. Nhận scope hẹp hơn vẫn xác thực được URL hiện tại; không chứng minh mọi cấu hình đa giá trị hoặc redirect.
- `San()` dùng tempfile rồi dọn; `_bash_posix()` ở Linux trả `bash`; các lần nạp riêng dùng TMPDIR trong `scratch/`. Nền đo Linux/Bash/Git ghi bên dưới. **Windows: KHÔNG ĐO ĐƯỢC**, không suy từ nhánh dò Git Bash trong mã thành parity Windows.

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được lượt 2 | Khớp? |
|---|---|---|---|
| Spec đóng băng | SHA b8200141… | `nguon/M9-FETCH-AUTH.md` = **b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac**; không có tệp tại `cay-kho/ops/specs/M9-FETCH-AUTH.md` trong snapshot này | Băm nguồn cung cấp khớp |
| HEAD/base | SHA đầy đủ ở metadata | `git rev-parse` đúng cả hai | Có |
| Write set/số dòng | +11 workflow, +68 test; +79/−0 | `git diff --stat/--numstat 27c413c3..HEAD`: đúng hai tệp, **+79/−0** | Có |
| Ngoài hai tệp | Không chạm | Diff không có tệp thứ ba; trạng thái git sạch | Có ở snapshot; không suy lịch sử thao tác chưa commit |
| Workflow so lượt 1 | Không đổi | Diff workflow 62c299a..HEAD rỗng; SHA256 giống đã đo trong metadata | Có |
| Áp nguyên HINT rồi sửa docstring | Logic khớp byte | Patch apply rc=0; toàn tệp chỉ khác docstring, +6 dòng | Có |
| origin/master đi tiếp | 27 commit; prompt nói chỉ reviews/CHANGELOG/manifest | SHA **4b5184e21373eb8f8a36493d0282ebd020bb4458**, 27 commit; **còn chạm `ops/cong_cu.py`**. Diff riêng hai tệp write set từ base tới origin/master rỗng | Danh sách tổng không khớp; điều kiện không chạm write set khớp |
| t152 trên base | ĐỎ (i) | Nạp t152 HEAD, trỏ tới workflow lấy từ base: `TinHieuChotCa`, `(i) đoạn auth/fetch không chạy được: rc=1` | Có; base chưa có hàm t152 |
| t152/t148 HEAD | QUA | Cả hai XANH khi gọi riêng; có đối chứng base/mutant | Có |
| m1–m9 | Đều ĐỎ đúng nhánh | **9/9 GIẾT** trên bản sao mới | Có |
| Bộ test HEAD | 147/147 | `python3 ops/lease_publish_test.py`: **147/147 đạt; đã chạy=147, bỏ qua=0**, rc=0, dùng actionlint cung cấp trên PATH | Có; log sửa môi trường bên dưới |
| Wrapper HEAD | AL_VER=1.7.7, 147/147, rc=0 | **147/147, đã chạy=147, bỏ qua=0, rc=0** trên bản sao `ops/` + `.github/`; AL_GOI là gói cung cấp, TAR_OPTIONS=--no-same-owner | Có với điều kiện offline ghi rõ |
| Actionlint + shellcheck | rc=0 | Binary cung cấp **1.7.7**, shellcheck PATH **0.9.0**; debug ghi hai lần gọi shellcheck, tổng **0 lỗi**, rc=0 | Có |
| Whitespace | Sạch | `git diff --check 27c413c3..HEAD` rc=0 | Có |
| Header Git hiệu lực | Không khai runner đã xanh | Git **2.43.0**, fetch thật qua helper thay HTTP: HEAD rc=0, một helper, header đúng; base/m5/m7 thiếu hoặc sai header → 128 | Có ở biên config/helper |
| Thứ tự và bytes shell | Mask trước dùng; unset sau | Bash **5.2.21**, GNU base64 **9.4**; encode/decode bằng fixture khớp, không LF; mask → fetch → hậu kiểm thành công | Có trên Linux này |
| Fetch thứ hai/protocol bị cấm | Không có số đo trong EVIDENCE | m10/m11 **SỐNG ở t152/t148**, Git thật rc=128; chi tiết Findings | Thiếu phủ định độc lập |
| HINT lượt 2 | Hai tệp/trần 80 | Chỉ test có 2 hunk; patch dry-run/apply rc=0, cmp byte bằng bản sửa thử; AST ngoài t152 bằng HEAD. So base: test +69/−0, workflow +11/−0 = **+80/−0** | Trong trần |
| Kiểm HINT | Phải giữ xanh và giết mutant | HEAD/dạng (b) XANH; base/m1–m11 ĐỎ đúng lý do. Bộ test đầy đủ **147/147, đã chạy=147, bỏ qua=0, rc=0** | Có |

Log: [metadata git](scratch/logs/git-metadata-round2.json), [suite HEAD đúng môi trường](scratch/logs/head-suite-corrected-round2.log), [actionlint và shellcheck](scratch/logs/actionlint-round2.log), [Git fetch/helper](scratch/logs/git-fetch-round2.json), [shell](scratch/logs/shell-round2.json), [kiểm patch/trần/AST](scratch/logs/hint-validation.json).

### Shell của workflow và kết luận fetch

- **Dòng 97:** `printf 'x-access-token:%s' "$TL_TOKEN"` dùng format cố định, token được quote, không thêm LF. Đo `printf` là Bash builtin, base64 nhận dữ liệu qua stdin với argv `-w0`. GNU base64 tại đây không wrap; Python giải mã khớp `x-access-token:` cộng fixture token, không LF phụ. `$(...)` bỏ LF cuối nếu có; với `-w0` không có LF đó.
- **`set -euo pipefail` (73):** phép gán hoàn thành trước mask. Probe làm base64 trả 9 hoặc printf trả 8: script dừng đúng rc, chưa mask/fetch; TL_TOKEN chưa đặt → rc=1/unbound variable. Token rỗng vẫn mã hoá được, nên quyền và giá trị token thật là điều kiện của canary.
- **Dòng 98:** echo builtin phát add-mask trước fetch. Base64 chuẩn không chứa LF hoặc ký tự `%` cần escape ở payload command này. Đo cờ shell `ehuBc`, không có xtrace. Nếu bật `set -x` từ trước, phép gán có thể bị trace trước khi đăng ký; HEAD không bật nó.
- **Dòng 99–104:** COUNT=1 và đúng KEY_0/VALUE_0 là environment cho cùng một simple command nhờ continuation. VALUE là Basic header được mã hoá đúng. Các `-c` protocol không ghi đè header. URL fetch `https://github.com/$TL_KHO` khớp scope `http.https://github.com/.extraheader`; dòng 80 chốt TL_KHO canonical. Probe gọi **Git fetch thật**, rồi helper con đọc runtime config đúng header; host đối chứng không có header.
- Giao diện `GIT_CONFIG_COUNT/KEY_n/VALUE_n` đã được thực thi bằng Git **2.43.0**. Không có binary/tài liệu nguồn Git **2.31** trong phạm vi đã đo; không trình bày kiểm 2.43 thành kiểm toàn dải 2.31+ hoặc ảnh `ubuntu-latest` hiện hành.
- **Dòng 105:** sau thành công, unset chạy; AUTH_B64 và COUNT đều vắng trong hậu kiểm. Khi fetch trả 128, `-e` kết thúc shell trước unset/hậu kiểm/NHAN, không đi tới checker/receipt. Unset không xoá an toàn mọi bản sao trong bộ nhớ. Biến gán riêng command không tồn tại trong shell sau lời gọi thành công.
- **Dòng 106–107:** chốt OID nhận được bằng TL_H còn nguyên. Probe Git local chạy cả hai dòng và qua với OID fixture. Không thay nó bằng suy luận rằng fetch rc=0 đồng nghĩa đúng head.

**ĐÚNG/ĐỦ:** HEAD sửa đúng phần thiếu credential đo được tới biên Git/helper, không có bằng chứng shell đang làm mất header. Chưa đủ bằng chứng tuyên bố runner thật xanh: token/quyền thực, ref, HTTP/TLS, redirect, ảnh runner và toàn bộ preflight/checker chưa được đo. Helper dùng object fixture có sẵn để hoàn tất fetch; rc=128 fixture do helper từ chối thiếu/sai header không phải bản tái lập thông điệp GitHub `could not read Username`. M3/A3 là canary sau land, chưa được nghiệm thu ở đây.

### Bề mặt token/base64 và add-mask

| Bề mặt | Kết luận và giới hạn |
|---|---|
| Log shell hiện tại | Không bật `set -x`; không có lệnh in Authorization trong auth block ngoài kênh đăng ký mask. Probe dùng fixture nên stdout chứa command nguyên văn; không có bộ lọc Actions tại đây. |
| Add-mask | Đăng ký giá trị để runner che các lần xuất hiện khớp trong log được runner xử lý sau đăng ký. Không bảo vệ output trước đăng ký, dạng đã biến đổi, environment, argv, file/artifact hoặc memory. Chưa đo bộ lọc runner thật. |
| argv | Với dạng (a) HEAD, fetch argv có protocol flags, URL và refspec sạch. printf/echo là builtin; base64 chỉ có cờ `-w0`. Helper argv ghi trong probe không có token/base64. Dạng (b) có header trong argv của lời gọi git, dù cũng được spec nhận. |
| Environment/cây tiến trình | Helper đo được `GIT_CONFIG_VALUE_0` chứa header và TL_TOKEN được kế thừa; AUTH_B64 không export. “Một tiến trình” ở comment workflow 93 phải hiểu là một lời gọi fetch **và cây tiến trình con**, không phải đúng một PID. Không thêm finding chỉ vì cách env được spec chọn có đặc tính này. |
| ps/quan sát máy | argv thông thường không chứa base64 mới ở dạng (a); tiến trình đủ quyền đọc environment có thể thấy header/token. Mask log không chặn điều đó. Không đọc environment/ps của tiến trình ngoài fixture để thử. |
| curl sau fetch | Workflow 118 đã có token thô trong argv curl từ base. Đây là bề mặt có sẵn, không phải base64 mới do patch. Không tuyên bố add-mask che argv hệ điều hành. |
| Git config trên đĩa | Không có lệnh ghi config trong auth block HEAD. Config repo fixture sau fetch không có credential/extraheader. t152 m3 kiểm độc lập việc ghi bằng git config. |
| Receipt/artifact | Đọc phần dựng receipt `ops/lease_publish.py:1772` và workflow 121–141: không serialize biến auth; băm blob là bytes mã nguồn, không phải script đã thay token. **Chưa đọc receipt/artifact thật**, không gọi source review là kiểm artifact sạch. |

## Findings

### t152-bo-sot-fetch-thu-hai [P1] Thêm một fetch thiếu header vẫn qua chốt đúng một lời gọi

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5393`, `5408` (kết hợp bộ dò fetch và đoạn thực thi dừng trước NHAN). Workflow hiện tại 103/106 là các mốc của phản chứng bản sao.
- **VẤN ĐỀ:** bộ dò chỉ đếm chuỗi liền `fetch --no-tags`. m10 thêm fetch thứ hai sau NHAN, với `fetch --quiet --no-tags` và cùng URL/refspec hợp lệ. Lần này không có environment header; cũng nằm ngoài đoạn stub chạy. t152 vẫn XANH và tuyên đúng một fetch, t148 cũng XANH. Điều đó bỏ lọt hồi quy đúng yêu cầu M1 “một lời gọi mang xác thực”. **Không nói HEAD đang có fetch thứ hai.**
- **ĐÃ THỬ VÁ:** hunk 1 HINT nhận lệnh có `git … fetch` và ref PR độc lập với vị trí cờ `--no-tags`, nên nhìn thấy cả hai lời gọi trong toàn bộ steps. Chốt đếm từ chối trước khi thực thi đoạn auth. Không đổi workflow hay thêm tệp thứ ba.
- **ĐÃ THỬ NGHIỆM:** HEAD/m10 với t152 gốc: đều XANH. Chạy bytes shell YAML đến hết kiểm NHAN bằng Git thật, thay riêng transport bằng helper local: m10 gọi helper **hai lần**, lần đầu header đúng, lần hai trống, script **rc=128**, không tới POST_OK. Sau HINT m10 ĐỎ: `đúng một lời gọi fetch H, thấy 2`; HEAD/dạng (b) còn XANH; m1–m9 giữ lý do riêng. Cả test 62c299a đo lại cũng bỏ sót m10, nên đây là lỗ còn sót đã được xác nhận, không nhận là hồi quy mới do áp HINT.
- **ĐỘ TIN:** cao về ca cụ thể, số lời gọi và mất header; không đo HTTP GitHub. Bộ dò sau HINT vẫn là bộ dò cú pháp shell hiện tại, không phải parser mọi chương trình Bash.

### t152-stub-khong-do-quyen-transport [P2] Stub nhận cấu hình mà Git fetch thật từ chối

- **TỆP/DÒNG:** `ops/lease_publish_test.py:5410–5416`, đặc biệt dòng 5415 chuyển sang `git config`.
- **VẤN ĐỀ:** stub chuyển các `-c` cho Git config, nhưng config không thực hiện quyết định cho phép transport của fetch. m11 đổi đúng `protocol.https.allow=always` thành `never`: header vẫn đúng, t152/t148 XANH; Git thật rc=128 trước khi gọi helper. Đây là chốt độc lập còn thiếu ở adapter. Xếp **P2**, vì phép đo header của HEAD vẫn có giá trị; không lấy đột biến protocol làm bằng chứng rằng header chưa được đo hoặc token bị lộ.
- **ĐÃ THỬ VÁ:** hunk 2 HINT hỏi Git thật giá trị `protocol.https.allow` hiệu lực dưới chính `cfg`/environment của lời gọi và đòi `always`, phù hợp cấu hình canonical đã có. Một dòng thêm; tổng patch với base bằng 80 dòng thêm.
- **ĐÃ THỬ NGHIỆM:** m11 SỐNG với test HEAD và test lượt 1 đo lại. Git thật **rc=128**, stderr `fatal: transport 'https' not allowed`, **0 helper call** — lỗi này do chính Git, không do quy tắc auth của helper. Sau HINT ĐỎ (i), rc=95; HEAD và dạng (b) XANH. Không có phép transport network nào được gọi.
- **ĐỘ TIN:** cao về quyết định protocol cụ thể. HINT bảo vệ cấu hình canonical này; không giả làm test tích hợp HTTP hoặc mọi global option của Git.

## Mutant đã chạy

Mỗi mutant xuất phát độc lập từ workflow HEAD, đặt dưới `scratch/mutants/`. Cột t152 HEAD là tín dụng của **PR được review**, không lấy HINT nhận thay. m1–m9 được dựng từ spec/verdict đã cung cấp; m10 dùng đúng loại phản chứng fetch thứ hai người yêu cầu gợi ý, m11 đổi một giá trị cấu hình. Không tạo nội dung đường dẫn thoát/khai thác.

| Mutant | Thay đổi | t152 HEAD | Lý do/đối chứng | Sau HINT lượt 2 |
|---|---|---|---|---|
| m1 (A1) | KEY_0 thành http.postBuffer | **GIẾT** | (i), rc=1, thiếu header | GIẾT (i) |
| m2 (A1) | URL credential theo mẫu spec | **GIẾT** | (ii), nhận credential trong URL | GIẾT (ii) |
| m3 (A1) | Thêm ghi config local extraheader | **GIẾT** | (iii), phát hiện lệnh ghi | GIẾT (iii) |
| m4 (A1) | persist-credentials thành true | **GIẾT** | (iv), checkout sai | GIẾT (iv) |
| m5 | COUNT=0 | **GIẾT** | (i), rc=1; Git thật không nhận header, rc=128 | GIẾT (i) |
| m6 | VALUE_0 là header dummy | **GIẾT** | (i), header hiệu lực sai | GIẾT (i) |
| m7 | Ghi đè AUTH_B64 từ TL_KHO sau gán đúng | **GIẾT** | (i), bytes header sai; Git/helper rc=128 | GIẾT (i) |
| m8 | Xoá add-mask | **GIẾT** | (v), thiếu đăng ký mask | GIẾT (v) |
| m9 | KEY_0 thành http.extraheader toàn cục | **GIẾT** | (i), rc=94; header cũng có ở host đối chứng | GIẾT (i) |
| m10 (lượt 2) | Fetch thứ hai sau NHAN, cờ --quiet trước --no-tags, không header | **SỐNG** | Bộ dò không đếm, đoạn chạy không bao phủ; Git/helper lần hai mất header/rc=128 | GIẾT, đếm được 2 |
| m11 (lượt 2) | protocol.https.allow=never | **SỐNG** | Stub chỉ hỏi config; Git thật cấm HTTPS/rc=128, chưa tới helper | GIẾT (i), rc=95 |

**Tín dụng t152 HEAD: 9 GIẾT / 2 SỐNG trên 11 mutant**, không nâng số bằng mutant của 146 ca cũ. Dạng (b), scope repo là đối chứng cấu hình hoạt động; cờ quiet là đối chứng cú pháp; `-c` dính key bị Git thật từ chối, không tính thành mutant chốt auth.

## Đối chiếu EVIDENCE.md

Phần lượt 1 ghi +50 dòng test và thông điệp (i) cũ: đó là lịch sử đã được phần lượt 2 cập nhật +68 và thông điệp rc=1. Không coi việc giữ lịch sử là lời khai HEAD sai. Phần lượt 2 về áp nguyên logic HINT, chỉ đổi docstring, workflow không đổi, +79 và m1–m9 đều ĐỎ **đã tự đo khớp**. Thời điểm riêng của tác giả, thao tác khôi phục worktree, run #500 và quyền token thật KHÔNG ĐO ĐƯỢC độc lập trong điều kiện không mạng.

EVIDENCE đã tự ghi chưa đo fetch/mask trên runner thật; không có cơ sở cáo buộc họ khai đã nghiệm thu A3. Cần phân biệt “m1–m9 giết” với “không còn đột biến sống”: EVIDENCE chỉ khai nhóm chín ca; hai ca sống mới là thiếu sót test đo được ở lượt này, không phải bằng chứng tác giả khai gian số đo ấy.

## HINT và kiểm thử

`HINT.patch` là unified diff từ **HEAD 6254570**, đường tương đối cho `patch -p0` từ gốc `cay-kho/`. Có **hai hunk**, đều trong `ops/lease_publish_test.py`, cho hai finding trên. Đã dry-run/apply trên `scratch/final-apply/`; bytes bằng bản sửa thử; AST ngoài t152 không đổi. Workflow sản phẩm giữ bytes hiện tại; sau HINT so lease base: +11 workflow/+69 test = **+80/−0**.

Ma trận HINT giữ HEAD/dạng (b)/scope repo XANH, base/m1–m11 ĐỎ đúng nhánh. [Log ma trận](scratch/logs/hint-matrix-round2.json). Bộ test đầy đủ: **147/147, đã chạy=147, bỏ qua=0, rc=0** [log HINT](scratch/logs/hint-suite-round2.log). Wrapper HEAD offline: **147/147, đã chạy=147, bỏ qua=0, rc=0** [log wrapper](scratch/logs/head-wrapper-round2.log).

Giới hạn bản HINT: đếm các lệnh Git/ref PR viết trực tiếp trong shell hiện tại; không giải nghĩa mọi alias, biến chứa lệnh, cấu hình nhiều nguồn hoặc mọi tuỳ chọn fetch hợp lệ. Stub vẫn chỉ đo config và thứ tự command, không HTTP. Không khai HINT loại hết mọi chương trình Bash có thể làm hỏng fetch.

Lịch sử lỗi fixture của reviewer được giữ: lần chạy suite đầu đặt PATH/TMPDIR theo nhầm cwd `cay-kho`, thiếu actionlint; **145/147, rc=1**, hai ca đỏ t33/t137. Lần đặt đúng PATH và TMPDIR trong scratch đạt **147/147, rc=0**. Lượt đầu có thể fallback tempfile ngoài cwd do TMPDIR không tồn tại; không dùng kết quả đó để tuyên chạy cô lập. [Log lỗi môi trường](scratch/logs/head-suite-round2.log). Một lượt probe helper khi chạy lại trả thêm BrokenPipe ở lúc kết thúc protocol; đã sửa fixture để phân biệt end-of-fetch và kết thúc helper rồi đo lại, [giữ log fixture cũ](scratch/logs/git-fetch-fixture-noisy.json); log kết luận dùng helper đã sửa.

Phạm vi truy cập: không mở nội dung doctrine bị cấm để review, không gọi mạng, không checkout/reset/commit/sửa tracked files của `cay-kho/`. Có tác dụng phụ của lệnh suite được yêu cầu: t82 gọi `shutil.copytree(HERE.parent, …)` và chỉ loại `.git`/bytecode, nên bản chạy trực tiếp đã sao chép cây vào tempfile; đây không phải bằng chứng đã loại doctrine khỏi mọi I/O của test. Các bản chạy HINT/wrapper tiếp theo chỉ chép `ops/` và `.github/` vào scratch. Không xem nội dung doctrine đã được copy. Trạng thái git và hai băm tệp được kiểm lại khi kết thúc.

## chua_do_duoc

1. Fetch xanh trên GitHub runner thật, token `contents: read` có quyền trên kho/ref thật, ảnh ubuntu-latest, HTTP/TLS/redirect và toàn bộ job. Không dùng mạng; M3/A3 canary sau land chưa thực hiện.
2. Bộ lọc mask runner thật, debug/xtrace thực tế của runner và log/artifact thật; mọi secret trong probe là fixture công khai. Chỉ đo command đăng ký/thứ tự và bytes.
3. Receipt/artifact thật cùng `check_run_id`, `workflow_definition_commit`, `workflow_definition_sha256`, `checker_rc`. Đọc mã dựng receipt không thay được readback artifact.
4. **Windows KHÔNG ĐO ĐƯỢC**; Git 2.31, macOS/BSD base64 cũng không được chạy. Nền thực đo Git 2.43.0, Bash 5.2.21, GNU base64 9.4, actionlint 1.7.7, shellcheck 0.9.0 trên Linux.
5. Đọc ps/environment của tiến trình ngoài fixture, memory dump hoặc kiểm xoá bí mật khỏi bộ nhớ. Environment con chứa header là giới hạn thực đã đo của dạng (a).
6. Timeline lease/S5, Issue/comment/run lịch sử và thao tác khôi phục của tác giả không được xác minh qua mạng. Snapshot/diff/băm đã kiểm độc lập.
7. Wrapper tải mạng nguyên dạng không chạy; dùng AL_GOI đã băm đúng pin **023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757**, TAR_OPTIONS=--no-same-owner và bản sao nguồn trong scratch. Không coi đó là kiểm tải mạng hoặc Windows.
