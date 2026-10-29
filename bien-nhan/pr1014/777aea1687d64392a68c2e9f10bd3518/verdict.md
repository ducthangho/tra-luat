verdict: changes_requested
reviewed_sha: ef2c3ff647baf88bad3baf55314fb3a3d2cf14f1
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1014, lượt 1. Có một lớp lỗi, một thể hiện cần sửa: nhánh Windows của c91 đổi đầu vào nhưng giữ dấu nhận diện stderr của đầu vào cũ. Chẩn đoán các lỗi gốc nhìn chung đúng; bản vá c91 chưa hoàn chỉnh.

## Phạm vi và nguồn bằng chứng

- HEAD kiểm đầu phiên: `ef2c3ff647baf88bad3baf55314fb3a3d2cf14f1`; tree: `ed63b07a5568593e24400310928c0b3142714d35`.
- Master đối chứng: `641b3deff2b3ab2dcecaab00440661a865bde537`; tree: `617c8b06224e3895400775a284605dcd1d947aa5`.
- `git -C cay-kho diff 641b3de ef2c3ff` đúng hai tệp được giao: `ops/bien_nhan_v2_test.py` (+32/-15), `ops/lease_publish_test.py` (+12/-3). Đã đọc thêm cổng và tài liệu liên quan để kiểm cơ chế.
- Reviewer: Codex/OpenAI, `provider=openai_codex`, bề mặt API/tools trong sandbox Linux (`codex_service`), transport máy. Model/effort thực phục vụ và launcher attestation: không đo độc lập được. Không tự xác nhận assurance `cross_approved`.
- Kho nguồn chỉ đọc; các lệnh test chạy trong bản sao `review-evidence/head/`, `review-evidence/master/`. Không push hoặc gọi API ghi GitHub. Snapshot nội dung 7.456 tệp, gồm metadata Git, không có delta; tracked/untracked/ignored sạch ở kiểm cuối. Snapshot không chứng minh toàn bộ lịch sử ghi giữa hai mốc.
- **Windows ở lượt này: `not_measured`.** Log Windows đã giao là bằng chứng lịch sử. Các phép mô phỏng dưới đây chỉ chạy trên Linux, không được tính là Windows PASS.

## Finding F1 — P2 — `windows-fixture-path-oracle-drift`

**Vị trí:** `ops/bien_nhan_v2_test.py:3164`, `:3173`; khẳng định sử dụng giá trị này ở `:3250`.

**Lỗi:** `run_json_ten_qua_dai` dùng `ops/reviews/a<b/run.json` khi `os.name == "nt"`, nhưng vẫn trả dấu cần có trong stderr là `"a" * 40`. Cổng đúng sẽ báo đường dẫn `ops/reviews/a<b/run.json`; thông báo đó không chứa 40 chữ `a`. Vì vậy, ngay cả khi thay ENOENT bằng EINVAL thành công như executor dự định, c91 vẫn ĐỎ. Nó dừng ở hàng `run_json_ten_qua_dai/khong-no`, trước khi đo vế có nợ và các nguồn đứng sau.

**Tái hiện đã chạy:** `python3 -B review-evidence/probes.py`, rc=0 của harness kiểm các kỳ vọng. Harness nạp bản sao head, chỉ chọn hàng này và nhánh tên Windows, tiêm EINVAL vào đúng đường dẫn ở `os.lstat`/`os.stat` và `Path.read_text`; CLI, YAML, Git, allowlist/nợ vẫn là mã thật. Kết quả ca gốc:

```text
status=giet_that
run_json_ten_qua_dai/khong-no: đòi rc=2 ... stderr nêu `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`;
được rc=2: ... `ops/reviews/a<b/run.json` có mà không đọc được `execution_surface` ...
```

Đổi riêng dấu mong đợi sang `a<b` trong hàm nạp ở bộ nhớ làm **cả hai vế không nợ/có nợ PASS**. Sau đó áp đúng đột biến mức tệp `m116_vang_loi_stat_khac_thanh_vang`: ca chết tại khẳng định hành vi, do cổng trả rc=0 thay vì rc=2; đối chứng c18 vẫn PASS. Đây là bằng chứng cho cách vá, không phải phép đo Windows thật.

**Đề xuất sửa:** tại helper này, dựng một biến thành phần tên, dùng nó cho cả `rj` và dấu nhận diện trả về, ví dụ trả `thanh_phan[:40]`. Giữ đầy đủ các điều kiện rc=2, không `NỢ CHẾT`, không traceback và stderr chỉ đúng nguồn. Không bỏ điều kiện stderr để xanh hóa ca.

**Ca khóa lỗi:** chạy hàng EINVAL trên cả hai chế độ nợ; baseline phải xanh, m116 phải chết đúng vì rc/nguồn. Tiếp tục chạy Windows thật. Phép đo Linux của reviewer đã xác nhận sửa dấu không làm mất răng m116.

**Rủi ro của cách vá:** dùng dấu quá chung hoặc chỉ giữ rc=2 có thể nhận lỗi từ nguồn khác; chọn dấu từ đúng thành phần đường dẫn. Lỗi này cũng khiến những mutant đi qua cùng ma trận có thể nhận tín dụng từ một assertion vốn đã đỏ; không dùng tổng mutant Windows làm bằng chứng đóng lớp khi baseline c91 chưa xanh.

## Đối chiếu chẩn đoán và c96

| Ca | Bằng chứng độc lập | Đánh giá |
| --- | --- | --- |
| c96 | Log Windows `windows-log-run40833865576-gate-ops.txt:1145` trả rc=1 với L-ANCESTRY, không thấy rc=3. Bản master đặt script không đuôi `git` qua PATH; phù hợp với việc Windows chạy Git thật. Head chặn đúng `bnv2.subprocess.run`. | Chẩn đoán phù hợp triệu chứng; bản vá giữ chốt cần đo. Windows mới chưa chạy. |
| `_kho_cau`/c93 | Log `:1142` có commit `5cfd3f5e…`, blob `70363d66…`. Mô phỏng CRLF trên đúng ba payload fixture và stdin băm tái tạo **nguyên cả hai SHA** ấy. Dùng byte LF cho ra commit `e4a3f5d511d31dfb809024edcde68c4602cd02f1`, blob `e4a3f5daa164ce057bf3ad4a93b1431146ec5a30`; tiền tố trùng. Hai commit của c91 cũng có tiền tố số `5298700`. | Chẩn đoán newline được kiểm bằng SHA, không chỉ suy từ mã. Vá byte hợp lý; Linux byte giữ nguyên. |
| c91 | Log `:1140` báo lstat tên quá dài là ENOENT/ENOTDIR. Đổi sang ký tự cấm nhằm vào cùng nhánh OSError khác ENOENT/ENOTDIR và vẫn có probe độc lập. | Ý tưởng đúng; còn F1. EINVAL trên Windows thật vẫn `not_measured`. |
| t27 | Log `windows-log-run40812761896-gate-ops.txt:3286` nêu đúng verdict viết hoa bị thiếu trong mục lục; `:3288` là 253/254. Mô phỏng phép khớp tên không phân biệt hoa thường tái tạo cùng thông báo. | Đúng nguyên nhân lệch tập tên. Đây còn là thiếu bookkeeping thật, xem phần dưới. t26 dùng cùng selector nhưng log không báo t26 đỏ. |

Lưu ý số liệu: log Windows thứ nhất ghi **121/129** mutant thường có răng (`:1280`), tức **8** mutant thường không răng, không phải 6: m103, m105, m116, m117, m118, m120, m129, m130. Không suy rằng tất cả đã được sửa từ số liệu executor.

**Chốt c96 vẫn được đo:** fixture tạo câu ancestry sai thật; baseline c96 xanh trước khi đột biến. Shim trả `CompletedProcess(rc=3, stdout="", stderr="")` cho đúng từng mẫu. `dem` xác nhận đã gọi shim; assertion đòi đồng thời rc=2, tên lệnh và `rc=3` trong stderr. Đã tách hai mẫu để m125 không chỉ chết ở vòng đầu:

| Phép thử trong bản sao | Kết quả |
| --- | --- |
| Baseline từng `merge-base`, `is-shallow-repository` | Cả hai `qua` |
| m125, chỉ `merge-base` | `giet_that`: cổng trả rc=1 và L-ANCESTRY thay vì rc=2 |
| m125, chỉ `is-shallow-repository` | `giet_that`: vẫn rc=2 do kiểm giá trị kho nông, nhưng mất chẩn đoán `rc=3`; assertion bắt được |
| Đối chứng c18 trong mỗi mutant | `qua` |
| Gỡ assertion bộ đếm, shim vẫn khớp | `qua`; chốt kết quả vẫn đo lỗi rc |
| Shim không bao giờ khớp, giữ bộ đếm | `gian_giao` / KHÔNG ĐO ĐƯỢC: không gọi git giả |
| Shim không khớp, đồng thời gỡ assertion bộ đếm | `giet_that`, rc=1; không xanh giả, nhưng mất phân loại lỗi giàn giáo |
| `_chay_cli` ném ngoại lệ có chủ ý | Harness nhận ngoại lệ dự kiến; `bnv2.subprocess` đã được trả lại đúng object gốc |

`SimpleNamespace(**vars(subprocess))` giữ `CompletedProcess`, `SubprocessError` và các thuộc tính module hiện có; chỉ thay `run`, không sửa module `subprocess` dùng chung của fixture. Cổng hiện có các điểm gọi `subprocess.run` ở `bien_nhan_v2.py:809`, `:936`, `:1142`; nói “một cửa” đúng ở giao diện `run`, không có nghĩa chỉ một call site. Các điểm này đều được namespace bao phủ. `_dot_bien_tep` thay module toàn cục trước khi chạy ca; c96 lấy `goc_sp` từ đúng module đang hoạt động. Phép đo m125 xác nhận điều đó.

Giới hạn có chủ đích: c96 mới không kiểm cơ chế phân giải executable qua PATH. Nó vẫn kiểm đầy đủ chính sách rc lạ/stderr rỗng của `main` đối với hai lệnh được giao. Nếu sau này cổng chuyển sang `Popen` hoặc import trực tiếp một hàm chạy khác, shim có thể không chặn; bộ đếm hiện tại sẽ làm ca báo không đo được. Không tìm thấy đường né như vậy trong mã đang review. `finally` và phép bơm ngoại lệ đã kiểm việc khôi phục; suite hiện chạy tuần tự.

## t26/t27 và nợ mục lục có sẵn

Trên **cả head và master**, Linux `glob` và `endswith` trả cùng 297 receipt và 275 verdict. Không đổi hành vi Linux trên cây được giao; helper vẫn giữ cách xử lý mục thư mục/symlink khớp tên của glob, không tự thêm điều kiện `is_file`.

Phép khớp không phân biệt hoa thường bổ sung đúng hai tệp:

- `ops/reviews/wp929-g1-codex-luot1-VERDICT.md`
- `ops/reviews/wp929-g1-codex-luot2-VERDICT.md`

Cả hai là verdict hoàn chỉnh, tồn tại ở master lẫn head; cả hai **không có tên trong README và không có receipt cạnh nó**. Lượt 2 còn ghi một nợ P3 của chính review wp929. Mô phỏng selector Windows làm t27 trả `lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0`, nêu thiếu hàng cho lượt 1 giống log lịch sử.

Đánh giá: thiếu mục lục/receipt và khoảng trống phát hiện trên Linux là **nợ có sẵn**, không do hai tệp này mới được PR #1014 thêm hay làm sai băm. Bản vá chọn chuẩn khớp tên cũ của Linux, nên đồng thời **bỏ khả năng Windows từng phát hiện nợ đó**. Không nên diễn giải t27 xanh sau vá là hồ sơ hai verdict đã được hoàn thiện. Tôi không đếm nợ nền này thành một lớp lỗi mới của delta; đã ghi riêng tác động mất độ phủ trên Windows.

Đề xuất xử lý bằng việc bookkeeping riêng: giữ nguyên byte verdict, lập receipt có provenance/băm thật, thêm hàng mục lục/caveat đúng; sau đó thống nhất selector bao gồm biến thể hoa thường trên mọi nền hoặc quy định tên canonical và cưỡng chế nó bằng ca riêng. Thêm ca verdict viết hoa mồ côi phải bị bắt, cùng ca đối chứng đủ receipt/mục lục. Chỉ đổi selector sang `casefold` ngay mà chưa xử lý hồ sơ sẽ tái làm gate đỏ đúng vì khoản nợ này; không tự dựng provenance để hết đỏ.

## Quét các điểm cùng lớp trong hai suite

Đã quét mọi vị trí ghi text/byte, băm, stdin subprocess, glob, symlink, chmod và nhánh nền; danh sách từng dòng nằm ở [risk-inventory.tsv](review-evidence/risk-inventory.tsv), kèm [platform-locations.txt](review-evidence/platform-locations.txt). Các nhóm đáng chú ý dưới đây dùng số dòng **head**:

| Vị trí | Kết luận về Windows |
| --- | --- |
| `bien_nhan_v2_test.py:246,270,325,793,829,2156,2158,2708,2709,3136,3237` | Còn ghi text: YAML/mã Python được đọc lại theo ngữ nghĩa, hoặc commit chỉ dùng SHA vừa tra; không so với SHA LF cố định tại những chỗ này. Riêng `nen.txt` ở :793 thay SHA nền nhưng băm verdict lấy từ Git. Không tìm thấy lỗi băm cùng kiểu c93 tại các điểm này. |
| Cùng tệp `:649,661,802,811,814,1741,1744,2588,2592` | Nội dung verdict/receipt quan trọng ghi byte hoặc băm lại đĩa/blob byte; không băm chuỗi LF trong khi ghi CRLF. `_kho_cau:2574,2577,2580` và stdin c93 :3300 đã được vá. |
| Cùng tệp `:3087,3297` | `commit-tree -m` lấy stdout text là SHA ASCII; không truyền payload newline qua stdin text. Các SHA tiền tố cố định phụ thuộc `_kho_cau` đã chuyển byte. Probe xác nhận các tiền tố. |
| Cùng tệp `:1702,1905,3392`; `lease_publish_test.py:2211,2433` | Còn glob receipt/workflow và rglob object. Cây hiện tại không có receipt/workflow sai hoa thường tạo tập bổ sung; rglob `*` không có mẫu chữ cần phân biệt. Không dự báo đỏ trên cây này do các chỗ ấy. Selector verdict t27 là khoản nợ đã nêu. |
| `bien_nhan_v2_test.py:3158`; `lease_publish_test.py:5441,5835,5879,6865` | Symlink cần quyền tạo symlink và Git ghi mode đúng. Thiếu quyền có thể làm c91/t133/t151 lỗi giàn giáo; đây là phụ thuộc nền có sẵn. Log lịch sử đi qua hàng symlink c91 trước lỗi tên dài và ghi t133/t151 QUA; không có bằng chứng lỗi mới ở các chỗ này trên runner đó. Không nâng thành Windows PASS của head. |
| `lease_publish_test.py:1221–1223,11444–11447` | t19 có `return` khi không tạo được symlink: có nguy cơ xanh mà không đo trên Windows thiếu quyền, nợ độ phủ có sẵn; t193 in rõ không đo một vế alias. Không phải ca chắc chắn đỏ, cũng không phải bằng chứng đã kiểm symlink. |
| `bien_nhan_v2_test.py:3196`; `lease_publish_test.py:5792,13303,13314,13325` | Đã chmod trước ghi/xóa object chỉ đọc, hoặc retry khi PermissionError rồi kiểm object thật sự mất. Không thấy bỏ sót cùng lỗi Windows read-only tại các thao tác này. |
| `bien_nhan_v2_test.py:3175–3183,3206,3223` | Ca Git vắng thay PATH của chính tiến trình trước khi gọi cổng; hai clone dùng file URL. Không còn executable Git giả kiểu script PATH sau c96. Các hàng sau F1 chưa có phép đo Windows head; file URL cùng cách dựng đã có trong t132 log Windows QUA. Không có bằng chứng để kết tội thêm. |
| `lease_publish_test.py:2341–2399,2510,2592,2665,2856` | Shell giả actionlint được chạy qua Bash POSIX thật; t40 có nhánh Windows dùng PE thật (:2807–2852). Không phải trường hợp đưa script không đuôi cho CreateProcess như c96 cũ. :2856 chỉ thuộc nhánh ngoài Windows. |
| Cùng tệp `:3074–3092,5738–5743,8126,8152,8184,8206,8245` | gh giả có nhánh `gh.exe`/script `api` và cấu hình venv; deadline dùng `.cmd` trên Windows, `.sh` trên POSIX. Các file shebang tên `git.exe` ở t165–t168 chỉ được bộ phân giải chọn đường dẫn, không thực thi PE giả. Log lịch sử ghi những ca này QUA. |
| Cùng tệp `:11613–11618` | gh shell giả chạy bên trong Bash của bước chỉ Ubuntu; guard workflow/sổ bỏ ca kiểm nền ở :11590–11595 và :571. Không chuyển thành Git giả Windows trực tiếp. |
| Cùng tệp `:183,1193–1195,1215–1217,1270,1682,2231,5441,5849,5851,6593,6835,6837,12754,12824` | Payload/hash quan trọng dùng byte hoặc băm tệp/blob thực; các lời gọi có stdin đều dùng byte, không `text=True`. Không tìm thấy lỗi LF/CRLF cùng lớp c93 còn lại trong suite lease. |
| Cùng tệp `:4861,7226,7301` | API nhóm tiến trình/tín hiệu được phân nhánh POSIX; phía Windows dùng nhánh riêng. Không tìm thấy một phụ thuộc errno/POSIX vô điều kiện khác chắc chắn làm đỏ Windows trong phạm vi quét. |

Ngoài F1 và nợ selector/symlink đã nêu, không xác lập thêm lỗi Windows còn sót bằng mã và bằng chứng hiện có. Đây không phải chứng nhận toàn suite Windows đã xanh.

## Đã đo

Chuẩn bị bằng `git clone --no-hardlinks -q cay-kho review-evidence/head` và bản tương tự cho `master`, rồi checkout detached từng exact SHA. Nguồn và cả hai clone là **shallow=true**; không gỡ cờ shallow hoặc coi kho thiếu lịch sử là kho đầy đủ. Đối chiếu head/master đủ tách lỗi môi trường theo nhiệm vụ; không cần fetch mạng.

Các lệnh test cuối đặt `TMPDIR` bằng đường dẫn tuyệt đối của `review-evidence/tmp/`. Bảng ghi command nghiệp vụ; rc thật ở tệp `.rc` cạnh từng log. Lượt đầu dùng tempfile mặc định `/tmp`; đã chạy lại với TMPDIR trong thư mục làm việc để tuân thủ phạm vi tệp tạm, giữ log lượt đầu riêng ở `review-evidence/first-default-tmp/`.

| Nơi chạy | Lệnh | rc | Kết quả / bằng chứng |
| --- | --- | --- | --- |
| `review-evidence/head` | `python3 ops/bien_nhan_v2_test.py` | 1 | `89/93 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐỎ`. [Log](review-evidence/head-bien-nhan.log). |
| `review-evidence/master` | `python3 ops/bien_nhan_v2_test.py` | 1 | Cùng nguyên dòng tổng trên và cùng bốn ca không đạt. [Log](review-evidence/master-bien-nhan.log). |
| `review-evidence/head` | `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/head-t26.log). |
| `review-evidence/head` | `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/head-t27.log). |
| `review-evidence/master` | `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/master-t26.log). |
| `review-evidence/master` | `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/master-t27.log). |
| Thư mục làm việc | `python3 -B review-evidence/probes.py` | 0 | `ALL REVIEW PROBES PASSED`: baseline/m125 hai nhánh/c18, kiểm bộ đếm/khôi phục, phản chứng F1 và sửa dấu/m116. [Script](review-evidence/probes.py), [log](review-evidence/probes.log). |
| Thư mục làm việc | `python3 -B review-evidence/audit_probes.py` | 0 | `ALL AUDIT PROBES PASSED`: SHA CRLF khớp log Windows, LF collision đúng; parity tập tên head/master; selector rộng làm t27 đỏ như kỳ vọng. [Script](review-evidence/audit_probes.py), [log](review-evidence/audit-probes.log). |
| Kho nguồn, chỉ đọc | `git -C cay-kho diff --check 641b3de ef2c3ff` | 0 | Không lỗi whitespace. |
| Kho nguồn, chỉ đọc | `GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored` và đối chiếu manifest SHA256 | 0 | Status rỗng; 7.456/7.456 tệp, delta rỗng. [Integrity](review-evidence/source-integrity.json). |

Bốn ca không đạt giống nhau ở head/master: **c1, c40, c14, c76**. Từng lý do đều nêu kho nông hoặc rc=2 của cổng vì kho nông; không gán thành hồi quy PR. c91/c93/c96 và m125 đều đạt đúng kỳ vọng trên Linux. Không đổi rc=1 toàn suite thành PASS.

Hai lần dựng harness EINVAL ban đầu chưa tiêm đủ các API mà Python 3.13 dùng (`Path.lstat` gọi `os.stat(..., follow_symlinks=False)`); đã giữ log lỗi harness, sửa móc tiêm và kiểm cả lượt gọi `lstat`, `stat`, `read_text`. Chỉ kết quả harness cuối có đối chứng xanh và m116 chết mới được dùng làm bằng chứng F1.

**Chưa đo:** Windows head/master thật (`not_measured`); toàn suite lease ở lượt review này (`not_run`, chỉ chạy t26/t27 theo yêu cầu); CI mới/required checks (`not_run`); full-history gate (`not_measured`). Không lấy log lịch sử thay cho các phép đo này.
