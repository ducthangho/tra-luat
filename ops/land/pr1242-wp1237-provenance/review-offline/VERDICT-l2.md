verdict: approve
reviewed_sha: 4458d06a8180d5d74f5c786a57b1c5a3176540d9

Finding P2 lượt trước đã được vá thật; **0 finding P0–P2 mở, 1 P3 không chặn theo chỉ thị lượt này**. Approval này là kết luận review nội dung mã, không chứng nhận các phép HTTP/Windows chưa đo được hoặc các điều kiện merge khác.

- Base: `fe84620f897913c7f6c2ce5a0c7316a49655e82f`.
- Reviewed tree: `f484d430e0d535c7d567554f3c7d84d7d7c56e34`.
- `SPEC.md` SHA-256: `b0e12304e0c591db6e2130454ed6a72c1458d4541b1312037935b0ccbb210666`, khớp lease wp1237/r1/g1; class sensitive, write set đúng 2 tệp. Lease tới 2026-11-07T15:12:00Z.
- Reviewer/provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, session/run `4f773891`, theo sổ `runs/4f773891/run.json`. Model/effort phục vụ không có trong sổ: KHÔNG ĐO ĐƯỢC; không suy từ cấu hình yêu cầu hoặc tài khoản vận chuyển.
- Linux, Bash 5.2.21, curl 8.5.0. Áp dụng quy trình read-only trong `cay-kho/.claude/skills/cross-review/SKILL.md`; đầu ra theo prompt là tệp sandbox này. Mọi bản sao/phép phản chứng nằm ngoài kho `cay-kho`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

`retry-max-time-decimal-equivalence` [P2] — **ĐÃ VÁ THẬT**. `python3 -B repro_max_time.py` chạy installer thật và curl thật qua `file://` trên bản sao exact head: `1/00001/08/0099/000300/0001800` đều rc0, stdout đúng một dòng, băm tải đúng; `0/00000/1801/0001801/18446744073709551617/abc/rỗng` đều rc13, không giải nén. Đối chứng SHA lượt 1 vẫn trả rc13 với `000300`. Log: `review-evidence/repro-max-time.log`.

`python3 -B review_probes.py numeric`: 200 đầu vào chạy nguyên khối kiểm M2 trích từ head, dưới `set -euo pipefail`, đối chiếu oracle Python ⇒ `mismatches:[]`, `arithmetic_error_count:0`, gồm 4096 số 0, 4096 số 0 trước 1/1800, số tràn sau nhiều số 0, chuỗi rỗng và chữ số Unicode. Ngoài phép trích khối, installer đầy đủ được chạy với cả ba núm unset ⇒ rc0; từng núm rỗng/abc/-1 ⇒ rc13. Không phát hiện lỗi mới do chuẩn hóa.

Trình tự bảo vệ đúng: regex chặn rỗng/ký tự khác số trước; phép `${x#"${x%%[!0]*}"}` chỉ xử lý chuỗi đã tồn tại; dạng toàn 0 được đổi rỗng rồi gán `0` trước `10#`; độ dài dạng đã chuẩn hóa được kiểm trước số học, và `||` ngắn mạch chặn chuỗi quá 4 chữ số. Vì vậy các ca đã đo không đưa chuỗi rỗng hay số dài vào phép `10#`.

| Giá trị MAX_TIME, lệnh `python3 -B repro_max_time.py` | installer rc thật | curl thật qua file:// |
|---|---|---|
| `1`, `00001`, `08`, `0099`, `000300`, `0001800` | 0 cho từng giá trị; stdout đúng; gói được giải nén | 0 cho từng giá trị, băm đúng |
| `0`, `00000`, `1801`, `0001801`, `18446744073709551617` | 13 cho từng giá trị; không giải nén | không gọi curl đối chứng với đầu vào ngoài khoảng |
| `abc`, chuỗi rỗng | 13, đúng tên/giá trị trong lỗi | không gọi curl đối chứng với đầu vào sai dạng |
| `000300` trên SHA lượt 1 | 13 | đối chứng âm xác nhận tái hiện lỗi cũ |

Không nâng bằng chứng executor thành phép đo độc lập. Probe socket lượt này vẫn trả `PermissionError(1, 'Operation not permitted')` trước bind; HTTP/Windows chưa đo được.

## BẢNG SĂN

| Hướng | Lệnh đã chạy | Output thật / kết luận |
|---|---|---|
| 1. Chuẩn hóa, toàn 0, tràn số, set -u | `python3 -B review_probes.py numeric` | `cases:200,mismatches:[],arithmetic_error_count:0`; unset rc0, 9 giá trị núm sai đều rc13. KHÔNG PHẢI LỖI trong miền đã đo. |
| 2. Đường offline và stdout/độ trễ lần đầu | `python3 -B review_probes.py security` | base/head offline rc0, `curl_called:false,stdout_exact:true`; tải đầu base 0.0475s/head 0.0344s, rc0, băm đúng, stderr rỗng. KHÔNG PHẢI LỖI; đây là file://, không đo HTTP. |
| 3. Cổng băm/giải nén/chạy | `python3 -B review_probes.py security` | `wrong-hash` và `partial-body`: `rc:9,extracted:false,executed:false`; thiếu pin: rc8, chưa tạo đích. KHÔNG PHẢI LỖI. |
| 4. TimeoutExpired có xanh rỗng hoặc nuốt ngoại lệ khác | `python3 -B review_probes.py harness` | Chèn TimeoutExpired vào seam subprocess ⇒ `AssertionError,calls:22,failed_assertions:22,groups:D1..D8,green:false`; OSError ngoài dự kiến lan ra ngay sau 1 lời gọi. Phép unit phụ trợ dùng server không socket, không chạy/giả curl, không chứng nhận HTTP t237. |
| 5. Tính nguyên vẹn/phạm vi | `python3 -B review_probes.py scope` | `old_definitions_changed:[]`; chỉ insert 171 dòng test; hai định nghĩa thêm `_MayChuGoiT237` và `t237_cai_actionlint_retry_song_qua_5xx`. Numstat: 36+171=207 dòng thêm, 2 tệp; diff check rc0; workflows/hook/wrapper/công cụ khác diff rỗng. Khối băm và đoạn đối chiếu/giải nén/chạy giống base từng byte. |
| 6. Retry thật và các cờ có tác dụng | `python3 -B review_probes.py retry` | D7 tương đương file lỗi: rc4, 9 lần/8.0443s; D8: rc4, 7 lần/6.0179s. Bỏ max: 9/8.0224s; bỏ delay: 4/7.0399s; default3: 4/3.0311s. Không dùng curl giả. Không tính các phép file:// này là t237 HTTP hay tín dụng GIẾT mutation bắt buộc. |
| 7. Biên lịch chạy D8 | `python3 -B review_probes.py stall` | Installer thật/curl thật, file:// không tồn tại, đình chỉ curl 4.2s: rc4, 4 lần/6.217s; cùng biểu thức D8 cho false. Biên phụ thuộc wall clock được tái hiện; suy luận rủi ro Windows có giới hạn bên dưới. |

Log nguyên văn: `review-evidence/probe-{numeric,security,scope,harness,retry,stall}.jsonl`. Script đo là `review_probes.py`, `repro_max_time.py`, `run_review_gate.py`; có thể đọc và chạy lại từ thư mục sandbox này. Mọi thay đổi mutation chỉ ghi vào tệp tạm ngoài nguồn.

## BẢNG ĐỐI CHIẾU SPEC

| Mục | Kết quả |
|---|---|
| M1 | Mặc định 8/15/300 và đủ mọi cờ yêu cầu tại installer dòng 58–60, 139–142; curl thật có retry/trần/nhịp như bảng săn. HTTP 504/partial chưa đo độc lập. |
| M2 | Lỗi số 0 đứng đầu đóng; các ca bắt buộc dương/âm đều chạy lại; không thấy lỗi mới từ set -u/chuỗi rỗng/tràn số. |
| M3 | Khối băm ghim/helper và toàn bộ đoạn đối chiếu→giải nén→kiểm bản giống base từng byte. AL_GOI không gọi curl. Gói sai hoặc cắt nửa bị rc9 trước giải nén/chạy. |
| M4 | Lỗi tải thật in `toi da 1+8 lan thu (AL_RETRY=8, cach 1s, tran 6s)`; D3 giữ kiểm `1+2 lan thu` và `30s`. |
| M5 | Tải file:// thành công lần đầu không chờ retry, không thêm stdout; base/head đều đúng một dòng đích và stderr rỗng. Không suy thời gian mạng HTTP từ file://. |
| Phạm vi | 2 tệp, 207 dòng thêm ≤250; test chỉ thêm một khối 171 dòng; mọi định nghĩa test cũ giữ nguyên AST. Không đổi workflow/hook/wrapper/công cụ khác. |

## GATE ĐÃ CHẠY

Hai bản sao Git độc lập `review-evidence/base` và `review-evidence/head` checkout đúng SHA, `core.abbrev=7`; không dùng worktree chia sẻ metadata với nguồn. Tắt bytecode, Ruff dùng `--no-cache`. Dùng lệnh `python3 -B run_review_gate.py <base|head> <gate>`; script ghi argv và rc vào JSON tương ứng.

| Lệnh thực tế trong bản sao | Base | Head | Đánh giá |
|---|---|---|---|
| `python3 -B ops/lease_publish_test.py` | rc0 / 394.511s; `284/284 đạt; đã chạy=284, bỏ qua=0` | rc1 / 394.092s; `284/285 đạt; đã chạy=285, bỏ qua=0` | 284 test ID chung cùng QUA; chỉ t237 mới đỏ bởi socket EPERM. Không gọi suite head N/N. |
| `t35`, `t37`, `t38` trong suite trên | QUA / QUA / QUA | QUA / QUA / QUA | ĐẠT, đã có kết quả theo từng test ID trong log. |
| `bash -n ops/cai_actionlint.sh` | rc0 | rc0 | ĐẠT |
| `shellcheck ops/cai_actionlint.sh` | rc0, không chẩn đoán | rc0, không chẩn đoán | ĐẠT, delta0 |
| `python3 -m ruff check --no-cache --select F ops/lease_publish_test.py` | rc1, 9 lỗi cũ | rc1, cùng 9 lỗi | Chẩn đoán giống từng byte, delta0; không phải lint tuyệt đối sạch. |
| `actionlint -no-color` | rc1, SC1003 ở `ops-don-ref.yml:117:9` | rc1, cùng chẩn đoán | Giống từng byte, delta0. Actionlint đo workflow, shellcheck đo trực tiếp installer. |
| `python3 -B ops/lease_publish_test.py --chi-ca=t237` | không có ca này | rc1; `0/1 đạt`, EPERM | KHÔNG ĐO ĐƯỢC HTTP, không quy cho sản phẩm. |

Log: `review-evidence/{base,head}-{suite,bash-n,shellcheck,ruff,actionlint}.log`, `head-t237.log`; rc/thời gian/argv nằm trong JSON cùng tên; phép đối chiếu test ID và lint nằm trong `gate-parity.json`.

**Windows:** required theo spec và thay đổi `.sh`/subprocess; bundle không có kết quả trên `tra-luat-win`. Phiên Linux này không đo Windows. Theo phân công spec, phiên điều phối còn phải chạy tập trung t237+t35/t37/t38 với KHOA.txt; đây là giới hạn bằng chứng, không phải finding sản phẩm. Không gọi workflow hay thao tác mạng bên ngoài.

## D7/D8 VÀ TIMEOUT

D7 cần 8 nhịp 1s để có 9 yêu cầu, trần 60s cho dư khoảng 52s so với thời gian chờ danh định. D8 thường có 7 lần trên curl 8.5.0 ở môi trường này; cận 5..8 cho phép mất khoảng hai lần so với lần đo nhanh, nhưng không bảo đảm trên runner bị đình chỉ. Thời gian khởi động bash trước curl không tiêu ngân sách retry của curl; độ trễ trong curl, phục vụ HTTP, hoặc scheduling sau đó mới ảnh hưởng số lần. Curl thiếu delay đo được 4 lần, nên chú thích “~3” chỉ là xấp xỉ; assertion hiện tại vẫn phân biệt đúng phép đo này.

`TimeoutExpired` trả `rc=None`, không thể bằng bất kỳ mã 0/4/9/13 nào mà các vế đòi. Phép unit fault injection đã xác nhận 22/22 lượt đều được ghi lỗi, và ngoại lệ khác không bị nuốt. Nó thay ngoại lệ quá hạn bằng lỗi assertion có nhãn vế, không làm test xanh. Tuy vậy D7/D8 không đưa `err` vào mô tả lỗi nên mất chữ QUÁ HẠN ở riêng hai thông điệp đó; vẫn thấy `rc=None`. Đây là giới hạn chẩn đoán, không bằng chứng che fail thành pass.

HTTP t237 độc lập: `python3 -B run_review_gate.py head t237` ⇒ rc1, `lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0`, `PermissionError: [Errno 1] Operation not permitted` ngay khi tạo server. KHÔNG ĐO ĐƯỢC, không phải lỗi sản phẩm. Executor cung cấp ba lần `1/1 đạt` (32.312/32.301/32.298s) và 11 mutation GIẾT có đúng nhãn; đó là bằng chứng executor, chưa được reviewer lặp độc lập qua HTTP.

Đối chiếu ba dự đoán lượt trước: executor báo `bo_retry_max_time` đỏ D8, `bo_retry_delay` đỏ D7/D8, `mac_dinh_retry_3` đỏ D7/D8. Mã mới đã thêm D7/D8 đúng chỗ để phân biệt, và phép file:// bổ sung xác nhận tác dụng của ba thay đổi; không nhận việc “đã thêm test” đơn thuần làm bằng chứng GIẾT. Bảng 11/11 của executor không kèm rc/trace từng request nguyên vẹn, và đường REPO trong runner là môi trường executor, nên không gọi đó là 11/11 reviewer đo được. Các dự đoán SỐNG cũ đã có bằng chứng executor phản bác; không còn coi chúng là finding mở.

## TÍNH TOÀN VẸN VÀ BẢNG LỚP

`python3 -B finalize_review.py` đã đối chiếu snapshot trước/sau trên nguồn: **12.248/12.248 tệp**, `added:[],removed:[],changed:[]`; status kể cả untracked/ignored rỗng; HEAD/tree vẫn đúng các OID đầu verdict. Hai diff cung cấp khớp từng byte với `git diff --abbrev=9` trên đúng cặp SHA (khác mặc định độ dài index hash không phải khác nội dung). Bằng chứng: `review-evidence/integrity.json`, `snapshot-before.json`, `snapshot-after.json`, `finalize.log`.

Snapshot không gồm metadata `.git` và bắt đầu sau các lệnh đọc preflight; nó chứng minh không có delta nội dung quan sát được giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Reviewer không sửa/commit/push nguồn, không đăng GitHub hoặc gọi workflow.

| Slug lớp | Lượt trước | Lượt này | Bằng chứng |
|---|---|---|---|
| retry-max-time-decimal-equivalence | P2 mở | ĐÃ VÁ THẬT, đóng | Repro đầy đủ + đối chứng SHA cũ; 200 ca khối M2 |
| retry-window-request-count-flakiness | chưa có | P3 mới, không chặn theo prompt | Curl thật bị đình chỉ, predicate D8 false; chưa đo HTTP/Windows |

Đóng 1/1 lớp cũ; P0–P2 mở = 0, P3 = 1. Không tự tuyên bố waiver/merge authorization từ verdict này.

## FINDINGS

### retry-window-request-count-flakiness [P3] — D8 có thể đỏ vì trễ lịch chạy dù retry đúng

**TỆP/DÒNG:** `ops/lease_publish_test.py:14728`–14730, `t237`, vế D8.

**VẤN ĐỀ:** yêu cầu ít nhất 5 lần trong một ngân sách retry 6s phụ thuộc thời gian CPU/HTTP thực nhận được. Khi các lượt bị trì hoãn, curl đúng có thể đạt trần với chỉ 4 lần. D7 có dư lớn; D8 không có bảo đảm tương đương cho runner chậm. Không khẳng định Windows hiện tại đã flaky.

**ĐÃ THỬ NGHIỆM:** `python3 -B review_probes.py stall` ⇒ `installer_rc:4,attempts_from_curl37:4,seconds:6.217,stopped_seconds:4.2,d8_predicate:false`. Không sửa installer; thực thi Bash/curl thật, đình chỉ riêng curl bằng SIGSTOP/SIGCONT. Nguồn file:// lỗi giúp đo clock/retry không cần socket; số lần được đếm bằng curl37, không phải bộ đếm HTTP. Đối chứng không đình chỉ ở `review_probes.py retry`: 7 lần/6.0179s và predicate đúng. Log: `review-evidence/probe-stall.jsonl`, `probe-retry.jsonl`.

**ĐÃ THỬ VÁ:** không sửa kho hoặc sinh patch sản phẩm. Mới chạy phản chứng.

**ĐỘ TIN:** cao cho sự phụ thuộc scheduling đã đo trên Linux/curl 8.5.0; vừa cho suy luận rủi ro runner Windows. Chưa có tái hiện HTTP/Windows nên không nâng thành P2. Theo chỉ thị lượt này, P3 không chặn verdict.

**GỢI Ý VÁ:** sửa riêng test D8 tại đây, vì installer đang làm đúng ngân sách retry. Tách phép kiểm nhịp delay khỏi phép kiểm max-time: đo delay với số retry nhỏ và ngân sách dư; phép max-time giữ cận trên để phát hiện bỏ cờ mà không ép cận dưới 5 khi runner bị chậm. Không đơn giản nới cận dưới hiện tại rồi bỏ khả năng bắt mutation thiếu delay.

**CA TEST KHÓA:** giữ ba mutation `bo_retry_delay`, `bo_retry_max_time`, `mac_dinh_retry_3` chết đúng vế; thêm đối chứng trì hoãn tiến trình/handler để bản đúng vẫn được đánh giá đúng. Chạy HTTP thật trên Linux và tập trung Git Bash Windows. Phép file:// ở đây chỉ là phản chứng bổ sung.

**BẢN VÁ CÓ THỂ ĐẺ RA GÌ:** dung sai rộng hoặc bỏ cận dưới đơn độc khiến thiếu delay qua; tăng ngân sách quá nhiều làm suite chậm. Giữ nhánh kiểm delay riêng và lặp bảng mutation sau khi chỉnh.
