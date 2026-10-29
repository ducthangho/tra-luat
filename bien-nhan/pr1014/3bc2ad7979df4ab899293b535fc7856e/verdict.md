verdict: changes_requested
reviewed_sha: 32bf0e621b42cc33d6b68a8bb2a80f66f4b682f1
so_lop: P0 0 / P1 0 / P2 0 / P3 1

Review độc lập PR #1014, lượt 3. Hành vi fixture mới đúng theo các phép đo Linux: giữ rc=2, giết m114 ở cả hai chế độ nợ, đối chứng c18 sạch và bỏ cấu hình thì fixture đỏ. Có một finding P3 về lời khẳng định thực nghiệm trong chú thích. Áp ngưỡng prompt: còn P3 thì `changes_requested`.

## Finding

**F1 — P3 — `canh-bao-khong-phai-moi-lenh` — `ops/bien_nhan_v2_test.py:3231`**

Chú thích mới nói thành phần `core.fsync` lạ phát cảnh báo ở **MỌI lệnh**. Trên Git 2.43.0 của sandbox, hai lệnh cổng thực sự gọi khi đi tiếp qua fixture này đều có stderr rỗng:

```text
git config --get extensions.partialclone                          -> rc=1, stderr=''
git config --type=bool --get-regexp '^remote\..*\.promisor$'        -> rc=1, stderr=''
```

Trace đủ 11 lời gọi dưới đúng m114 cho thấy 9 lời gọi có cảnh báo, 2 lời gọi trên không có. Chú thích vì thế ghi rộng hơn bằng chứng; điều này có ý nghĩa trực tiếp với tiền đề lựa chọn fixture mà lượt review này yêu cầu xác minh. Đây là lỗi diễn đạt bằng chứng, không phải lỗi oracle hay fixture xanh giả. Cổng nguyên bản dừng ngay tại `rev-parse --is-shallow-repository`, nên không cần mọi lệnh đều cảnh báo.

**Tái hiện đã chạy:** `PYTHONDONTWRITEBYTECODE=1 python3 -B review-evidence/probes.py`, rc=0; xem `m114/khong-no` và `m114/co-no` trong [probe-results.json](review-evidence/probe-results.json). Phản chứng trực tiếp bổ sung, không sửa cấu hình bản sao:

```sh
git -C review-evidence/head -c core.fsync=tl-thanh-phan-la config --get extensions.partialclone
git -C review-evidence/head -c core.fsync=tl-thanh-phan-la config --type=bool --get-regexp '^remote\..*\.promisor$'
git -C review-evidence/head -c core.fsync=tl-thanh-phan-la rev-parse --is-shallow-repository
```

Hai lệnh đầu rc=1, stdout/stderr rỗng; lệnh cuối rc=0, stderr có `warning: ignoring unknown core.fsync component 'tl-thanh-phan-la'`. Bằng chứng ở [direct-command-results.json](review-evidence/direct-command-results.json).

**Đề xuất:** sửa chú thích ngay trong `cau_hinh_canh_bao`, nơi đặt tiền đề của fixture: nói cấu hình gây cảnh báo tại lệnh kiểm kho đầu tiên `rev-parse --is-shallow-repository`, đủ để cổng trả rc=2. Nếu liệt kê phạm vi lớn hơn, loại hai lệnh `config` khỏi khẳng định. Không cần đổi mã cổng hoặc oracle. Phép kiểm giữ hành vi là trace cùng baseline/m114/c18 đã chạy; không cần thêm test so chuỗi chú thích. Sửa lời mô tả có rủi ro thấp; tránh vô tình biến đề xuất thành yêu cầu cảnh báo ở mọi lệnh hoặc thay fixture để đạt yêu cầu không cần thiết đó.

## Phạm vi và tính độc lập

- Sau khi đọc prompt, phép kiểm Git đầu tiên là `git -C cay-kho rev-parse HEAD`, rc=0, khớp đúng SHA trên. Tree: `d816724bfbaa8bce6db016f22376a8f6e438a4bd`.
- Master: `641b3deff2b3ab2dcecaab00440661a865bde537`; cha lượt này: `abc8607583e822864f07e64956eb64d2edba2ad5`. Đọc diff toàn PR và delta lượt này độc lập với verdict cũ.
- Delta `abc8607..32bf0e6`: đúng một hunk, một tệp test, 5 dòng thêm/2 dòng bớt. Hai dòng thực thi chỉ đổi khóa/giá trị cấu hình và dấu stderr. Toàn PR có đúng hai tệp test, 51 dòng thêm/21 dòng bớt. `git diff --check 641b3de 32bf0e6`: rc=0.
- Reviewer: Codex/OpenAI, `provider=openai_codex`, `execution_surface=codex_service`, `transport=machine`, công cụ shell thật trong sandbox Linux. Không có phép đo độc lập model/effort thực phục vụ; không tự cấp assurance `cross_approved`. Executor Claude là thông tin điều phối, không phải chứng thực tự đo.
- `cay-kho/` được giữ chỉ đọc theo thao tác. Không push, không API ghi GitHub. Clone `--no-hardlinks`, đột biến, fixture, log và script đều ở `review-evidence/`, ngoài kho được review; `TMPDIR` tuyệt đối trỏ `review-evidence/tmp/`. Không tuyên bố hệ điều hành cưỡng chế read-only.

## (a) Delta, lệnh Git và nguồn dấu stderr

Thay `core.fsyncObjectFiles=true` bằng `core.fsync=tl-thanh-phan-la` là thay đổi thực thi tối thiểu cho lỗi đã ghi trong log Windows. Không sửa sản phẩm, không nới điều kiện rc=2/không `NỢ CHẾT`/không traceback/đúng dấu nguồn tại dòng 3253. Ngoại trừ F1, không tìm thấy sai lệch hành vi cần sửa trong delta.

Trace tại `bnv2.subprocess.run` chuyển tiếp tới Git thật; không giả stdout/stderr. Chỉ thay namespace `subprocess` của mô-đun cổng, không thay `subprocess` chung mà giàn giáo dựng kho sử dụng. AST chỉ cô lập fixture và từng chế độ nợ; giữ nguyên thân fixture và khẳng định c91.

**Cổng nguyên bản thực sự chỉ gọi một lệnh Git trong fixture cảnh báo:**

```text
git -C <fixture> rev-parse --is-shallow-repository
rc=0; stdout='false\n'
stderr="warning: ignoring unknown core.fsync component 'tl-thanh-phan-la'\n"
```

`_git_do` từ chối stderr này, CLI trả rc=2. Để đo cả đường còn lại mà cổng sẽ đi nếu bỏ chốt stderr, áp đúng m114 ở mức tệp. Mỗi chế độ nợ gọi 11 lệnh theo thứ tự sau:

| # | Đối số sau `git -C <fixture>` | rc Git | stderr có cảnh báo/dấu |
|---|---|---:|---|
| 1 | `rev-parse --is-shallow-repository` | 0 | Có |
| 2 | `config --get extensions.partialclone` | 1 | Rỗng |
| 3 | `config --type=bool --get-regexp '^remote\..*\.promisor$'` | 1 | Rỗng |
| 4 | `rev-parse --git-path info/grafts` | 0 | Có |
| 5 | `rev-parse --disambiguate=e72d857` | 0 | Có |
| 6 | `cat-file --batch-check=%(objectname) %(objecttype)` | 0 | Có |
| 7 | `for-each-ref --format=%(refname) %(objectname) %(objecttype) refs/remotes/origin/HEAD refs/remotes/origin/master refs/heads/master` | 0 | Có |
| 8 | `symbolic-ref -q refs/remotes/origin/HEAD` | 1 | Có |
| 9 | `symbolic-ref -q refs/remotes/origin/master` | 1 | Có |
| 10 | `symbolic-ref -q refs/heads/master` | 1 | Có |
| 11 | `merge-base --is-ancestor e72d8570d56391888423561308429963ae4f1b56 0dda7648f3476baeba72b8572a393498ca61a22c` | 0 | Có |

Lệnh 6 nhận stdin `e72d8570d56391888423561308429963ae4f1b56\n`. Bảng là lời gọi đo được khi chốt stderr bị bỏ; không gán cả 11 lời gọi cho lượt baseline đã dừng sau lệnh 1. Hai lệnh `config` có rc=1 hợp lệ vì không có khóa tương ứng. Danh sách năm nhóm lệnh executor nêu bỏ sót `config` và `symbolic-ref`.

**Môi trường cổng không tắt cảnh báo.** `_env_git` bỏ các `GIT_*` kế thừa ngoài hai biến được cho phép và đặt locale C cùng `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`, `GIT_NO_REPLACE_OBJECTS=1`. Nó không đặt `git -c core.fsync=...` đè cấu hình local. Đã thử đồng thời `GIT_CONFIG_COUNT/KEY_0/VALUE_0` với giá trị `core.fsync=none`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM` trỏ tệp riêng, `GIT_CONFIG_NOSYSTEM`, `GIT_DIR`, `GIT_TRACE`, `GIT_TRACE_SETUP`: trace xác nhận các biến đó bị loại. Cả hai lượt vẫn rc=2 và hiện đúng dấu cảnh báo. Biến `GIT_*` thực truyền chỉ là ba biến cố định trên trong môi trường lần đo này.

**Dấu không khớp nhầm trong fixture đã đo.** Tìm trong `cay-kho/ops` chỉ thấy `tl-thanh-phan-la` ở hai dòng đặt config/trả oracle. Đường dẫn tạm, YAML biên nhận và toàn bộ đối số lệnh cổng không chứa dấu này. CLI baseline chứa dấu trong chính cảnh báo Git; bỏ dòng config thì dấu biến mất và khẳng định c91 đỏ. Không tuyên bố chuỗi con này là cơ chế xác thực nguồn cho mọi môi trường tùy ý.

## (b) Răng của fixture mới

Áp đúng thay thế m114, khớp duy nhất một chỗ trong nguồn cổng rồi nạp bản sao với kiểm parity của rig:

```text
    if con:\n        raise KhongDoDuoc(
->
    if False:\n        raise KhongDoDuoc(
```

Chỉ chạy `cau_hinh_canh_bao`; các fixture `ref_hong`/`object_rong` đứng trước không thể lấy tín dụng thay. Kết quả ở [probes.log](review-evidence/probes.log) và [probe-results.json](review-evidence/probe-results.json):

| Biến thể | Không nợ: rc CLI / kết quả c91 | Có nợ: rc CLI / kết quả c91 | Đối chứng c18 |
|---|---|---|---|
| Head nguyên bản | 2 / `qua`, đúng dấu | 2 / `qua`, đúng dấu | Sạch |
| m114 còn hiệu lực | 1 / `giet_that` | 0 / `giet_that` | Sạch dưới chính mutant |
| Xóa duy nhất dòng đặt `config core.fsync` trong fixture | 1 / `giet_that` | 0 / `giet_that` | Sạch |
| Biến Git kế thừa có cấu hình đối nghịch/trace/GIT_DIR | 2 / `qua`, đúng dấu | 2 / `qua`, đúng dấu | Không chạy trong lượt môi trường bị bơm |

Đối chứng dùng `_sach_hoan_toan(c18)`: ca qua **và** một lượt kiểm biên nhận dương thật không còn `loi` hay `chua_do`; không chỉ nhìn màu xanh của c18. Đã khôi phục mô-đun giữa các lượt.

Khi xóa config, cổng không nợ rc=1 đúng phép thử được giao. Có nợ thì cổng rc=0 vì vi phạm ancestry được hấp thụ bởi nợ trúng khóa; **fixture vẫn đỏ** vì đòi rc=2 và dấu cảnh báo. Không diễn giải rc=0 của cổng trong phản chứng thành test xanh.

## (c) Toàn bộ 17 fixture c91 và giới hạn Windows

Chỉ dùng log đã giao [windows-log-run40844300802-gate-ops.txt](windows-log-run40844300802-gate-ops.txt). Log dòng 914 neo head `abc8607583e822864f07e64956eb64d2edba2ad5`; dòng 93 ghi Git `2.56.0.windows.2`. Không nhầm với bản `2.55.0.windows.5` được executor khai đã đo local.

Thứ tự dưới đây lấy từ vòng lặp **của cả parent và head**, không lấy thứ tự định nghĩa hàm. Log dòng 1114 báo lỗi đầu tiên tại `cau_hinh_canh_bao/khong-no`. Vòng lặp và `bang` không có nhánh skip/nuốt lỗi; vì vậy suy ra 16 fixture trước nó đã chạy qua **cả hai chế độ**, tổng 32 tổ hợp trên Windows thật ở parent. Log không in riêng từng tổ hợp; đây là suy luận từ luồng thực thi xác định, không phải 32 dòng PASS độc lập.

| # | Fixture (dòng head) | Phần phụ thuộc Git/nền | Windows trong log parent |
|---|---|---|---|
| 1 | `receipt_thu_muc` :3111 | Đọc directory, không khớp riêng tên lỗi OS | Qua cả hai |
| 2 | `receipt_utf8` :3117 | Python `UnicodeDecodeError`, ghi byte | Qua cả hai |
| 3 | `alias_vong` :3123 | Alias YAML, chẩn đoán của cổng | Qua cả hai |
| 4 | `nhanh_la_tree` :3128 | Ref thật trỏ tree; cổng tự nêu tên ref | Qua cả hai |
| 5 | `ref_hong` :3133 | **Git stderr `broken ref`**, có thể đổi theo phiên bản | Qua cả hai |
| 6 | `symref_gay` :3139 | `for-each-ref` bỏ symref gãy; `symbolic-ref` và cổng nhận `dangling symref` | Qua cả hai |
| 7 | `run_json_thu_muc` :3149 | Filesystem, dấu `run.json` | Qua cả hai |
| 8 | `run_json_symlink_gay` :3155 | Quyền symlink/lstat Windows | Qua cả hai |
| 9 | `run_json_ten_qua_dai` :3161 | Tên cấm Windows/errno, dấu từ cùng thành phần | Qua cả hai |
| 10 | `git_vang` :3176 | PATH không có Git; cổng tự chẩn đoán | Qua cả hai |
| 11 | `tien_to_mo_ho` :3185 | SHA ghim, Git liệt kê hai commit, cổng tự nêu `mơ hồ` | Qua cả hai |
| 12 | `object_rong` :3191 | **Git stderr `is empty`**, chmod/loose object | Qua cả hai |
| 13 | `kho_nong` :3201 | Clone file URL/drive, Git báo shallow | Qua cả hai |
| 14 | `kho_partial` :3212 | Git đọc `extensions.partialclone` | Qua cả hai |
| 15 | `kho_partial_promisor` :3217 | Clone/filter/promisor thật; Git chuẩn hóa bool | Qua cả hai |
| 16 | `grafts` :3237 | Cổng chặn tệp tồn tại; đã tắt `advice.graftFileDeprecated` | Qua cả hai |
| 17 | `cau_hinh_canh_bao` :3229 | Hành vi cảnh báo config của Git | Config cũ: không nợ đỏ rc=1; có nợ không tới |

Không còn fixture phụ thuộc Git nào trong 16 fixture đầu **chưa được đi qua trên Windows của parent này**. Các điểm stderr/ref/object/partial/promisor/symref/grafts trên đã được đo trong cấu hình của run đó; vẫn có thể khác trên phiên bản Git hoặc máy khác. `grafts` không dựa vào lời nhắc deprecated: nó chủ động tắt lời nhắc và đòi chẩn đoán riêng của cổng.

Log dòng 1116/1119 ghi c93/c96 `ĐẠT`; dòng 1234 ghi m114 `CÓ RĂNG`; dòng 1262 tổng `92/93`, `137/137`, `2/2`; dòng 1264 job rc=1. m114 trong suite cũ có thể chết ở fixture trước cảnh báo, nên log này **không** chứng minh fixture cảnh báo mới giết m114. Phép cô lập Linux ở mục (b) mới chứng minh điều đó.

**Windows với `core.fsync=tl-thanh-phan-la` và exact head mới: `not_measured`.** Không có log Windows cho cấu hình mới. Không xác nhận lại phép đo local mà executor khai; không gọi CI mới. Cấu hình cũ/có nợ cũng `not_measured` trong log parent vì dừng ở không nợ.

## Đã đo

Môi trường Linux, Python 3.13.17, Git 2.43.0. Hai bản sao dựng bằng `git clone --no-hardlinks -q cay-kho review-evidence/{head,master}`, checkout detached exact SHA. Cả nguồn lẫn bản sao đều `shallow=true`; giữ nguyên shallow, không fetch hoặc xóa cờ để làm xanh. Đặt `core.abbrev=7` trong hai bản sao, khớp cấu hình nguồn. Chi tiết ở [environment.json](review-evidence/environment.json).

| Lệnh / nơi chạy | rc thực | Kết quả |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | Đúng exact reviewed SHA |
| `git -C cay-kho diff --check 641b3de 32bf0e6` | 0 | Không lỗi whitespace |
| `python3 -B review-evidence/run_suites.py` | 0 | Harness hoàn tất, lưu rc riêng của từng suite |
| `python3 ops/bien_nhan_v2_test.py` tại bản sao head | 1 | `89/93 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐỎ` |
| Cùng lệnh tại bản sao master | 1 | Cùng kết quả, log giống head từng byte |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B review-evidence/probes.py` | 0 | 8 lượt cô lập; `ALL PROBES PASSED`; baseline/m114/bỏ config/môi trường đối nghịch × hai chế độ nợ |
| Hai lệnh `git -c core.fsync=... config ...` ở finding | 1, 1 | Stderr rỗng ở cả hai |
| `git -c core.fsync=... rev-parse --is-shallow-repository` ở finding | 0 | Có cảnh báo; stdout `true` vì bản sao suite là kho nông |

[suite-results.json](review-evidence/suite-results.json) lưu lệnh/rc/thời gian. [Log head](review-evidence/head-bien-nhan.log) và [log master](review-evidence/master-bien-nhan.log) có cùng SHA-256 `90169ab20f34776431a75bb779e7e7abcaaddfa54fd0f2386c5741f5f3f7c648`.

Bốn ca đỏ ở cả hai là **c1, c40, c14, c76**. c1/c76 ném lỗi kho nông; c40 thiếu bằng chứng dương vì cổng báo kho nông; c14 đòi rc=0 nhưng nhận rc=2 với cùng chẩn đoán. Đây là giới hạn môi trường có đối chứng master, không phải hồi quy PR; toàn suite vẫn được ghi `failed`, không chuyển thành PASS. Tầng tra commit cutover của c12 cũng báo không đo được, trong khi oracle đóng băng của ca vẫn chạy. c91/c93/c96 đạt trên Linux.

Chưa đo: suite trên lịch sử đầy đủ (`not_measured`), Windows exact head mới (`not_measured`), CI/required checks mới (`not_run`), toàn suite lease (`not_run`, ngoài lệnh test được giao cho lượt này). Không suy approval, merge hay land từ các phép đo này.

Kiểm toàn vẹn kho nguồn trước/sau được ghi ở [source-integrity.json](review-evidence/source-integrity.json); so SHA-256 nội dung tệp kể cả metadata Git và trạng thái tracked/untracked/ignored. Đây là ảnh chụp hai mốc, không chứng minh lịch sử mọi lần ghi giữa hai mốc.
