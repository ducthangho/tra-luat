verdict: approve
reviewed_sha: abc8607583e822864f07e64956eb64d2edba2ad5
so_lop: P0 0 / P1 0 / P2 0 / P3 0

Review độc lập PR #1014, lượt 2. F1 lượt trước đã vá thật theo phép đo EINVAL trên Linux; không xác lập finding mới trong delta hai tệp test. Áp ngưỡng của prompt: chỉ approve khi không còn finding P0–P3. **Windows của lượt này: `not_measured`**, kể cả nhánh tên cấm và việc phân giải executable. Approval này không khẳng định Windows đã xanh, CI đã đạt hay cho phép merge/land.

## Phạm vi và tính độc lập

- Lệnh đầu tiên sau khi đọc prompt: `git -C cay-kho rev-parse HEAD`, rc=0, đúng `abc8607583e822864f07e64956eb64d2edba2ad5`. HEAD detached; tree `1e2b6c1e4c838b83be46e902990bc21b3210c72c`. HEAD/tree vẫn như vậy ở kiểm cuối.
- Đối chứng master: `641b3deff2b3ab2dcecaab00440661a865bde537`. `git diff 641b3de abc8607` đúng hai tệp được giao, 46 dòng thêm/19 dòng bớt. Delta so lượt trước `ef2c3ff` chỉ sửa biến tên và dấu stderr của F1.
- Reviewer: Codex/OpenAI, `provider=openai_codex`, bề mặt API/tools trong sandbox Linux (`codex_service`), `transport=machine`; executor Claude là thông tin điều phối cung cấp. Không có phép xác thực độc lập model/effort thực phục vụ hoặc launcher attestation; không tự xác nhận assurance `cross_approved`.
- Không sửa `cay-kho/`, không push, không gọi API ghi GitHub hoặc gửi thông điệp ra ngoài. Clone, fixture, đột biến, script và log nằm trong `review-evidence/`, bên ngoài kho nguồn; `TMPDIR` trỏ tuyệt đối vào `review-evidence/tmp/`.
- Sandbox thực tế là workspace-write; read-only của kho nguồn được giữ bằng cách thao tác và kiểm snapshot, không tuyên bố OS cưỡng chế read-only. [Kiểm toàn vẹn](review-evidence/source-integrity.json): 7.456 tệp gồm metadata Git ở cả hai mốc, delta rỗng; tracked/untracked/ignored status rỗng. Snapshot không chứng minh toàn bộ lịch sử ghi giữa hai mốc.

## Findings

Không có finding P0–P3 cần sửa trong delta đang review. Khoản thiếu bookkeeping của hai verdict viết hoa có sẵn ở master được tách rõ bên dưới; không diễn giải gate xanh thành khoản nợ đó đã được xử lý.

## ĐỐI CHIẾU LƯỢT TRƯỚC

**F1 — `windows-fixture-path-oracle-drift`: ĐÃ VÁ THẬT trong phạm vi có thể đo.**

Tại `ops/bien_nhan_v2_test.py:3164`, `:3165`, `:3174`, cùng biến `thanh_phan` dựng cả đường dẫn lẫn dấu stderr. Linux vẫn dùng 300 chữ `a` và dấu 40 chữ `a`; Windows dùng `a<b` cho cả hai. Khẳng định ở `:3250` vẫn đòi đồng thời rc=2, không `NỢ CHẾT`, không traceback và đúng dấu nguồn.

Đã chạy [probes.py](review-evidence/probes.py), rc=0; [log](review-evidence/probes.log): chỉ ép lựa chọn tên Windows trong hàm test, tiêm EINVAL vào đúng đường dẫn tại `os.lstat`, `os.stat` và `Path.read_text`, giữ CLI/Git/YAML/allowlist/nợ thật. Không đổi `os.name` toàn cục. Kết quả:

| Phản chứng | Kết quả |
| --- | --- |
| Head, tên `a<b`, EINVAL, cả không nợ/có nợ | `qua`; cả hai vế đi qua khẳng định rc/nguồn |
| Head + đúng đột biến mức tệp `m116_vang_loi_stat_khac_thanh_vang` | `giet_that`: cổng trả rc=0 thay vì rc=2 tại hàng tên cấm |
| Đối chứng c18 dưới m116 | `qua` |
| Khôi phục riêng oracle cũ `"a" * 40` | `giet_that`: cổng đúng trả rc=2 và nêu `ops/reviews/a<b/run.json`, nhưng thiếu dấu cũ |

Hook ghi nhận 6 lần lstat, 6 lần stat, 5 lần read_text trên tên cấm trong toàn nhóm probe, chứng minh đã tiêm tới cả kiểm fixture và đường cổng. Đây là mô phỏng Linux, không phải Windows PASS.

## (a) Chẩn đoán lỗi gốc và quét cùng lớp

| Ca | Log lịch sử và phép đo độc lập | Kết luận |
| --- | --- | --- |
| c96 | `windows-log-run40833865576-gate-ops.txt:1145`: rc=1, lỗi L-ANCESTRY. Master tạo script `/bin/sh` không đuôi tên `git` trên PATH; head chặn `bnv2.subprocess.run`. Phép đo c96/m125 từng nhánh bên dưới xác nhận shim tác động đúng cổng. | Cơ chế script không được CreateProcess nạp phù hợp triệu chứng Git thật chạy. Không có trace phân giải executable của Windows ở lượt này. |
| `_kho_cau`/c93 | Log `:1142` có commit `5cfd3f5e87ecd0877a62d75e22c3cf005d842524`, blob `70363d663b5f549bdc70e2b0ce3838c2ad43ffd7`. Mô phỏng CRLF tái tạo nguyên cả hai SHA. Byte LF cho commit `e4a3f5d511d31dfb809024edcde68c4602cd02f1`, blob `e4a3f5daa164ce057bf3ad4a93b1431146ec5a30`; cả hai cùng tiền tố `e4a3f5d`. Cặp commit của c91 cũng cho đúng tiền tố số `5298700`. | Lỗi newline được kiểm bằng SHA, không chỉ suy từ lời khai. Vá `write_bytes` ở :2574/:2577/:2580 và stdin byte ở :3301 giữ byte Linux. |
| c91 tên quá dài | Log `:1140`: fixture nhận ENOENT/ENOTDIR, không vào lớp lỗi stat khác mà ca muốn đo. Head dùng tên cấm và vẫn tự gọi `os.lstat` độc lập với `_vang`. | Chẩn đoán đúng; F1 oracle đã đóng bằng phản chứng ở trên. EINVAL trên Windows thật vẫn chưa đo. |
| t27; selector chung với t26 | `windows-log-run40812761896-gate-ops.txt:3286`, `:3288`: thiếu hàng cho `wp929-g1-codex-luot1-VERDICT.md`, tổng 253/254. Mô phỏng selector không phân biệt hoa thường trên cả master/head tái tạo cùng lỗi. | Đúng nguyên nhân khác tập tên. t26 không được log gốc báo đỏ; nó chỉ dùng chung helper để thống nhất phép chọn. |

[audit_probes.py](review-evidence/audit_probes.py), rc=0, và [log](review-evidence/audit-probes.log) chứa phép đo SHA và selector. Log Windows thứ nhất thực ghi **121/129** mutant thường có răng (`:1280`): **8**, không phải 6, mutant không răng: m103, m105, m116, m117, m118, m120, m129, m130. Các ca tự kiểm không tính vào tám mutant thường này.

### Toàn bộ 17 fixture con của c91

Đã tách từng fixture, chạy **cả hai chế độ không nợ/có nợ**, ép nhánh tên Windows và dịch mọi `Path.write_text` trong phép đo thành CRLF. Cả **34/34 tổ hợp** qua khẳng định rc=2/không nợ chết/không traceback/đúng nguồn. Git và filesystem vẫn là Linux; phép đo không bao phủ đặc tính drive-letter, quyền symlink hay errno thật của Windows.

| Fixture tại dòng head | Dấu oracle | Đánh giá phần phụ thuộc nền |
| --- | --- | --- |
| `receipt_thu_muc`:3111 | `hong.receipt.yaml` | Không phụ thuộc tên lớp ngoại lệ đọc thư mục |
| `receipt_utf8`:3117 | `UnicodeDecodeError` | Byte lỗi được ghi byte; không qua dịch newline |
| `alias_vong`:3123 | `alias` | YAML đọc theo ngữ nghĩa |
| `nhanh_la_tree`:3128 | `refs/remotes/origin/master` | Ref Git thật, dấu là tên ref |
| `ref_hong`:3133/:3136 | `broken ref` | CRLF đã thử; dấu đến từ Git, vẫn phụ thuộc Git thực tế |
| `symref_gay`:3139 | `dangling symref` | Cổng chẩn đoán symref thật |
| `run_json_thu_muc`:3149 | `run.json` | Không đòi riêng IsADirectoryError/POSIX errno |
| `run_json_symlink_gay`:3155/:3158 | `run.json` | Cần quyền symlink thật; xem giới hạn bên dưới |
| `run_json_ten_qua_dai`:3161 | `thanh_phan[:40]` | F1 đã đóng; EINVAL giả lập |
| `git_vang`:3176/:3183 | `không gọi được git` | PATH của tiến trình được đổi qua `_chay_cli`; không tạo script giả |
| `tien_to_mo_ho`:3185 | `mơ hồ` | Cặp SHA cố định phụ thuộc `_kho_cau`; đã xác minh LF + CRLF ở các chỗ còn ghi text |
| `object_rong`:3191/:3197 | `is empty` | Chmod trước khi ghi object; dấu phụ thuộc Git thực tế |
| `kho_nong`:3201/:3207 | `kho nông` | Clone file URL thật; drive-letter Windows chưa đo |
| `kho_partial`:3212 | `extensions.partialclone` | Cấu hình Git thật |
| `kho_partial_promisor`:3217/:3224 | `promisor = true` | Clone file URL thật; cùng giới hạn đường dẫn Windows |
| `grafts`:3234/:3238 | `grafts` | CRLF đã thử; cổng chặn vì tệp tồn tại, không cần nội dung LF cố định |
| `cau_hinh_canh_bao`:3229 | `fsyncObjectFiles` | Cần Git còn phát cảnh báo deprecated; không phải điều kiện riêng Windows |

Không phát hiện đường thứ ba còn sai oracle do newline/nền trong ma trận này. Không suy từ 34 tổ hợp giả lập rằng mọi fixture đã qua Windows thật.

### Các điểm cùng lớp ngoài c91

Danh mục từng call site với tệp/dòng/hàm nằm ở [call-inventory.tsv](review-evidence/call-inventory.tsv): 40 call trong suite bien_nhan và 139 call trong suite lease, gồm ghi text/byte, glob/rglob, symlink, chmod và subprocess có stdin. Quét văn bản rộng hơn, gồm cả script nhúng và điều kiện nền: [bien_nhan](review-evidence/platform-bien-nhan.txt), [lease](review-evidence/platform-lease.txt). Bộ lọc này nhắm các lớp prompt yêu cầu, không phải bằng chứng đã kiểm mọi hành vi của hai suite.

| Vị trí head | Đánh giá Windows |
| --- | --- |
| `bien_nhan_v2_test.py:246,270,325,481,484,681,702,717,753,829,2708,2709,3261,3262,3263` | Ghi YAML, JSON, mã Python hoặc nội dung được đọc theo ngữ nghĩa. Không dùng digest LF cố định của chuỗi thay cho byte thật tại các chỗ này. Không dự báo đỏ vì CRLF. |
| Cùng tệp `:793,2156,2158` | Commit lấy SHA vừa tạo, không đối chiếu SHA cố định. Verdict/blob nhạy băm ở :650/:661, :801/:811/:814 và :2590/:2592 dùng byte/đọc byte thực. Không thấy lỗi cùng kiểu c93 còn sót. |
| Cùng tệp `:1702,1905`; `lease_publish_test.py:2211,2433` | Còn glob receipt/workflow. Cây hiện tại không có biến thể hoa thường bổ sung cho các mẫu này; rglob `*` tại bien_nhan :3393 không có chữ cần case-fold. Không dự báo đỏ trên cây hiện tại vì những selector này. |
| `bien_nhan_v2_test.py:3158`; `lease_publish_test.py:5441,5835,5879,6865` | Symlink/copy symlink cần quyền Windows và Git ghi mode đúng. Nếu thiếu quyền, c91/t133/t151 có thể lỗi giàn giáo. Đây là phụ thuộc có sẵn, không do delta; log gốc đi qua hàng symlink c91 trước lỗi tên dài và ghi t133/t151 QUA. Không coi đó là PASS của head mới. |
| `lease_publish_test.py:1221,1223,11444,11447` | t19 có thể return xanh khi thiếu quyền symlink; t193 in rõ một vế không đo. Nợ độ phủ có sẵn, không phải ca chắc chắn đỏ. |
| `bien_nhan_v2_test.py:3197`; `lease_publish_test.py:5792,13303,13314,13325` | Đã chmod trước ghi/xóa Git object read-only. Có xử lý retry ở t132. Không thấy chỗ bỏ chmod gây lỗi Windows cùng lớp còn lại. |
| `lease_publish_test.py:2341,2353,2364,2384,2399,2510,2592,2665` | Shell actionlint giả được chạy qua Bash POSIX, không giao trực tiếp script không đuôi cho CreateProcess. t40 :2807 dùng PE thật trên Windows; shell tại :2856 chỉ thuộc nhánh ngoài Windows. |
| Cùng tệp `:3074,3076,3082,3091,3092` | gh giả có nhánh Windows dùng `gh.exe`/script `api`, kèm cấu hình venv. Không phải Git giả PATH kiểu c96 cũ. |
| Cùng tệp `:5738,5740,5743` | Deadline fixture chọn `.cmd` trên Windows, shell trên POSIX. Chuỗi batch có CRLF tường minh còn được text-write; chưa có phản chứng nó làm đỏ, log lịch sử t131 QUA. Không tính là đã đo batch của head trên Windows. |
| Cùng tệp `:8126,8152,8184,8206,8245,8246,8273,8277,8289,8316,8325` | File git/git.exe giả chỉ phục vụ bộ phân giải đường dẫn, không được nạp như PE. Các chmod tương ứng không phải tiền đề chạy script trên Windows. |
| Cùng tệp `:11613,11614,11617` | Shell gh giả thuộc helper bước chỉ Ubuntu; guard tại :11591–:11594 chạy trước I/O. Không phải nhánh Windows bị bỏ sót. |
| Cùng tệp `:183,1193,1195,1215,1217,1265,1270,1682,2231,5439,5849,6593,6594,6835,6836,6837,6838,12754,12824` | Payload/hash quan trọng dùng byte hoặc đọc byte thật; cả ba stdin Git ở :6593/:6835/:6837 đều là byte. Các write_text khác trong danh mục dùng dữ liệu ngữ nghĩa, source mutant, marker/log, hoặc SHA Git vừa tra. Không xác lập lỗi băm LF/CRLF còn lại. |
| Cùng tệp `:4214,4230,5704,5711,7051,7053,13119` | Ghi text vào fixture Git nhưng dùng OID vừa đo; ref hỏng đòi `broken ref` (tương tự hàng c91 đã thử CRLF), không SHA LF cố định. |
| Cùng tệp `:4861,7226,7301` | API nhóm tiến trình/tín hiệu có nhánh POSIX/Windows riêng. Không phát hiện errno/POSIX vô điều kiện khác có bằng chứng sẽ làm đỏ Windows trong phạm vi quét. |

## (b) c96 còn đo đủ chốt không?

**Có, đối với hợp đồng được giao: rc Git ngoài tập sạch + stderr rỗng phải dẫn tới rc=2 và chẩn đoán lệnh/rc.** Phép mới không còn kiểm phân giải executable qua PATH. Fixture ancestry vẫn sai thật nếu Git thật chạy, nên shim không hoạt động không tự tạo kết quả xanh.

`SimpleNamespace(**vars(subprocess))` ở :3439 giữ các thuộc tính module, gồm `CompletedProcess`, `SubprocessError`, hằng và những hàm khác; chỉ thay `run` trên module cổng đang hoạt động. Cổng hiện gọi `subprocess.run` tại `bien_nhan_v2.py:809,936,1142`; cả ba đều được chặn. “Một cửa” là giao diện run; có ba call site. Module subprocess dùng chung của fixture không bị sửa.

`_dot_bien_tep` thay `bnv2` toàn cục trước lúc chạy ca; c96 lấy `goc_sp` từ module đó. Đã áp đúng m125 lên tệp cổng trong cây tạm, kiểm module thực sự khác gốc, và kiểm subprocess trở về đúng object sau phép đo. `finally` ở :3442–:3443 khôi phục cả khi bơm RuntimeError vào `_chay_cli`.

| Phép đo | Kết quả thật |
| --- | --- |
| Baseline, tách riêng merge-base và is-shallow-repository | Cả hai `qua` |
| m125 chỉ merge-base | `giet_that`: rc=1 L-ANCESTRY thay vì rc=2 |
| m125 chỉ is-shallow-repository | `giet_that`: vẫn rc=2 do giá trị shallow rỗng, nhưng thiếu `rc=3`; khẳng định bắt được |
| c18 dưới mỗi m125 | `qua` |
| Bỏ riêng assertion bộ đếm, shim khớp | `qua` |
| Shim không khớp, giữ bộ đếm | `gian_giao` / KHÔNG ĐO ĐƯỢC: không có lời gọi Git giả |
| Shim không khớp và bỏ assertion bộ đếm | `giet_that`, rc=1; không xanh giả, nhưng mất phân loại lỗi giàn giáo |
| Bỏ toàn bộ dem, đối số closure, increment và assertion | Shim khớp: cả hai nhánh `qua`; không khớp: cả hai `giet_that` rc=1 |
| Bơm ngoại lệ `_chay_cli` | Nhận đúng RuntimeError dự kiến; subprocess cổng và fixture giữ đúng object gốc |

Bằng chứng: [probes.log](review-evidence/probes.log), [counter_probe.py](review-evidence/counter_probe.py), [counter-probe.log](review-evidence/counter-probe.log), cả hai harness rc=0. Nếu sản phẩm sau này chuyển sang Popen/import trực tiếp runner khác, namespace vẫn có thuộc tính ấy nhưng không giả lập nó; bộ đếm sẽ làm ca báo không đo được. Không có đường né như vậy trong head. Suite chạy tuần tự; không xác nhận cách thay module này an toàn cho chạy đa luồng.

## (c) t26/t27 và hai verdict viết hoa

Trên **cả head và master**, tập glob Linux cũ bằng chính xác tập `endswith` mới: **297 receipt, 275 verdict**. `_tep_co_duoi` ở `lease_publish_test.py:1534` không thêm `is_file`, nên vẫn chọn cả directory/symlink khớp tên như glob trước đó. Không đổi hành vi Linux trên cây được giao.

Selector không phân biệt hoa thường bổ sung đúng hai tệp, byte giống nhau giữa master/head:

- `ops/reviews/wp929-g1-codex-luot1-VERDICT.md`: SHA256 `8a392561044c0ae6b9d504260149ff441fb8ec81cfe828fd8e06bd8f27c80bbf`.
- `ops/reviews/wp929-g1-codex-luot2-VERDICT.md`: SHA256 `40d42d53d7b30f7e703eced0376803907aa3b3a57d1d62dd697adcac25c30e49`.

Đây là hai verdict hoàn chỉnh, nên về mục tiêu “mọi verdict có trong mục lục”, **cả hai đáng được ghi sổ**. Hiện cả hai thiếu tên trong README, thiếu sidecar và không được receipt khác tham chiếu. Lượt 2 còn giữ nợ P3 `wp929-git-error-guards-unmeasured`. Selector rộng làm t27 đỏ đúng ở thiếu hàng lượt 1, tái hiện log Windows gốc; không có receipt viết hoa bổ sung khiến t26 thay tập.

Phân loại: **thiếu bookkeeping và khoảng trống phát hiện trên Linux là nợ có sẵn ở master**; PR không thêm hai tệp ấy hoặc sửa sai băm. **Mất khả năng Windows từng phát hiện chúng là thay đổi độ phủ thật của bản vá**, do chọn chuẩn khớp tên phân biệt hoa thường vốn có trên Linux. Tôi không đếm khoản nợ nền này thành finding mới của delta trong nhiệm vụ vá sự khác biệt nền tảng; cũng không coi Windows từng đỏ là một báo động giả về nội dung hồ sơ. Cách chọn này thống nhất phạm vi selector, chưa thực hiện đầy đủ mục tiêu bao quát mọi verdict bất kể tên.

Đề xuất xử lý bằng packet bookkeeping riêng, owner maintainer `ops/reviews`: giữ nguyên byte verdict, thu thập provenance thật để lập receipt, thêm mục lục/caveat đúng. Sau đó chọn selector bao gồm biến thể hoa thường trên mọi nền, hoặc quy định tên canonical và có ca bắt tên trái quy định. Khóa bằng cặp ca verdict viết hoa mồ côi phải đỏ/đủ hồ sơ phải xanh. Không dựng provenance để hết đỏ; đổi selector ngay mà chưa ghi sổ sẽ làm gate đỏ đúng vì nợ hiện tại.

## (d) Đã đo

Dựng hai bản sao bằng `git clone --no-hardlinks -q cay-kho review-evidence/{head,master}`, checkout detached exact SHA tương ứng, ghim `core.abbrev=7` trong bản sao. Nguồn và hai bản sao đều **shallow=true**; không fetch hoặc xóa cờ shallow. Chạy [run_suites.py](review-evidence/run_suites.py), rc=0 của harness điều phối; rc của từng suite được ghi riêng trong [suite-results.json](review-evidence/suite-results.json) và tệp `.rc`. Python 3.13.17, Git 2.43.0, Linux; `PYTHONDONTWRITEBYTECODE=1`.

| Nơi chạy | Lệnh | rc thật | Dòng tổng / kết quả |
| --- | --- | --- | --- |
| `review-evidence/head` | `python3 ops/bien_nhan_v2_test.py` | 1 | `89/93 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐỎ`. [Log](review-evidence/head-bien-nhan.log). |
| `review-evidence/master` | `python3 ops/bien_nhan_v2_test.py` | 1 | Cùng nguyên dòng tổng trên; `TỔNG: ĐỎ`. [Log](review-evidence/master-bien-nhan.log). |
| `review-evidence/head` | `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/head-t26.log). |
| `review-evidence/head` | `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/head-t27.log). |
| `review-evidence/master` | `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/master-t26.log). |
| `review-evidence/master` | `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. [Log](review-evidence/master-t27.log). |
| Thư mục làm việc | `python3 -B review-evidence/probes.py` | 0 | `ALL REVIEW PROBES PASSED`: F1/EINVAL/m116, 34 tổ hợp c91 với ghi CRLF, hai nhánh c96/m125/c18, bộ đếm và khôi phục ngoại lệ. |
| Thư mục làm việc | `python3 -B review-evidence/counter_probe.py` | 0 | `COUNTER PROBES PASSED`: bỏ toàn bộ bộ đếm, hai nhánh × khớp/không khớp. |
| Thư mục làm việc | `python3 -B review-evidence/audit_probes.py` | 0 | `ALL AUDIT PROBES PASSED`: tái tạo nguyên SHA Windows, tiền tố LF, parity tập tên head/master, selector rộng tái hiện lỗi t27 trên cả hai. |
| Nguồn chỉ đọc | `git -C cay-kho diff --check 641b3de abc8607` | 0 | Không lỗi whitespace. |
| Nguồn chỉ đọc | `GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored` và đối chiếu SHA256 snapshot | 0 | Status rỗng; 7.456/7.456 tệp, delta rỗng; HEAD/tree khớp đầu phiên. |

Hai log bien_nhan head/master **giống toàn bộ nội dung byte**. Bốn ca không đạt ở cả hai là **c1, c40, c14, c76**: c1/c76 báo kho nông; c40 thiếu marker dương vì cổng báo kho nông; c14 nhận rc=2 thay vì 0 cũng vì kho nông. Đây là lỗi môi trường có đối chứng master, không phải hồi quy PR; không đổi rc=1 toàn suite thành PASS. c91/c93/c96 và m125 đạt kỳ vọng trên Linux.

**Chưa đo:** Windows head/master thật (`not_measured`); gate với lịch sử đầy đủ (`not_measured`); toàn suite lease (`not_run`, nhiệm vụ yêu cầu t26/t27); CI mới/required checks (`not_run`). Log Windows đã giao chỉ là bằng chứng lịch sử.
