verdict: approve
reviewed_sha: 69dbf3af3c82bc6e1d6769666ca670bd706e80a5

**Bản vá đóng P3 `retry-window-request-count-flakiness` theo phản chứng đã đo; không phát hiện P0–P2 hay lỗi mới cần sửa.** Ba đột biến vẫn bị bắt đúng vế bằng installer/curl thật qua `file://`. HTTP t237 độc lập và Windows vẫn **KHÔNG ĐO ĐƯỢC**; approval nội dung này không chứng nhận những gate đó.

- Base: `fe84620f897913c7f6c2ce5a0c7316a49655e82f`.
- SHA lượt 2: `4458d06a8180d5d74f5c786a57b1c5a3176540d9`.
- Reviewed tree: `64d0be09369c91ebf26413e0301657de50b3162e`.
- `SPEC.md` SHA-256: `b0e12304e0c591db6e2130454ed6a72c1458d4541b1312037935b0ccbb210666`, khớp lease wp1237/r1/g1, sensitive, đúng base/write set; lease tới 2026-11-07T15:12:00Z.
- Reviewer/provider: `openai_codex`; execution_surface `codex_cli`, transport `machine`, run `05b8b841`, theo `runs/05b8b841/run.json`. Model/effort phục vụ không có trong sổ: **KHÔNG ĐO ĐƯỢC**, không suy từ cấu hình yêu cầu.
- Linux; Python 3.13.18, Bash 5.2.21, curl 8.5.0, shellcheck 0.9.0, actionlint 1.7.7, Ruff 0.17.3. Sandbox thực tế `workspace-write`; chỉ thị read-only áp riêng checkout được review.
- Áp dụng `cay-kho/.claude/skills/cross-review/SKILL.md`. Mọi script, log, bản sao/đột biến ở sandbox ngoài `cay-kho`; không sửa, commit, push, đăng bình luận hay gọi workflow.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### `retry-window-request-count-flakiness` [P3] — ĐÃ VÁ THẬT trong phạm vi phản chứng lịch chạy

Lượt 2 đòi `5 <= n <= 8` trong ngân sách retry 6s, nên đình chỉ riêng curl 4,2s làm bản đúng chỉ thử 4 lần và đỏ. Lượt này **lặp lại đối chứng cũ**, rồi chạy bản đúng với tham số mới. `n` dưới đây là số thông báo `curl: (37)` từ các lần tải tệp không tồn tại; đây **không phải** bộ đếm yêu cầu HTTP.

| Bản/điều kiện | Installer rc | n | Thời gian thật (s) | Assertion tương ứng |
|---|---:|---:|---:|---|
| D8 cũ, không đình chỉ, trần 6s | 4 | 7 | 6.0244 | qua |
| D8 cũ, SIGSTOP 4,2s | 4 | 4 | 6.2165 | **đỏ**, tái hiện P3 |
| D8a mới, retry3/delay3, không đình chỉ | 4 | 4 | 9.0242 | qua |
| D8a mới, SIGSTOP 4,2s | 4 | 4 | 10.2498 | **qua** |
| D8a mới, SIGSTOP 12s | 4 | 4 | 18.0198 | **qua** |
| D8b mới, delay1/max3, không đình chỉ | 4 | 4 | 3.0169 | qua |
| D8b mới, SIGSTOP 4,2s | 4 | 2 | 4.2149 | **qua** |

Lệnh: `python3 -B review_probes.py legacy`, `python3 -B review_probes.py retry`, `python3 -B review_probes.py stall`; cả ba rc0. Log: `review-evidence/{legacy,retry,stall}.jsonl`; mỗi phép còn có JSON chứa nguyên stderr và SHA-256 installer đã chạy. SIGSTOP/SIGCONT nhắm PID con có `/proc/<pid>/comm` là `curl`; không thay curl bằng đồ giả.

D8a tại `ops/lease_publish_test.py:14730` dùng retry3/delay3, **không đặt MAX_TIME**, nên giữ mặc định 300s; helper vẫn có timeout 240s. Ba nhịp chờ danh định là 9s, cận dưới 8,5s. D8b tại dòng 14735 chỉ giữ cận trên 6, nên khi lịch chạy chậm làm ít lần thử hơn, ca vẫn qua. Phản chứng cũ đã được loại bỏ mà ba mutation vẫn bị bắt.

**Máy rất nhanh:** bỏ delay cho ba lần retry thì curl chờ `1+2+4=7s`, đo thật 7.0220s, dưới cận 8,5s. Suy luận từ lịch chờ này: giảm overhead trên máy nhanh làm đột biến kết thúc sớm hơn; không tạo đường sống qua D8a. Timer thật bọc cả `chay`, gồm khởi động/dọn HTTP server; phần overhead HTTP đó chưa đo độc lập ở đây.

**Giới hạn được đo:** đình chỉ bản thiếu delay 4,2s khiến riêng D8a qua (`rc4/n4/10.2190s`). Cận dưới thời gian có thể bị độ trễ môi trường che. Đo thêm **chính đột biến đó với D7 và cùng SIGSTOP**: `rc4/n7/66.2665s`, predicate `n==9` sai; bộ kiểm vẫn bắt nó. Một vế qua không có nghĩa toàn t237 qua. Không khẳng định bản đúng chịu đình chỉ tùy ý vượt timeout 240s/ngân sách 300s; đó khác cơ chế đỏ oan trong 6s của P3 cũ.

### `retry-max-time-decimal-equivalence` [P2 lượt 1] — GIỮ ĐÃ ĐÓNG Ở LƯỢT 2

Installer giống SHA lượt 2 từng byte; các vế D4 dương/âm và mọi phần t237 ngoài D8 giữ nguyên. Không lặp lại 200 đầu vào của lượt 2 và không nhận chúng là phép đo mới. Không có thay đổi vào khối chuẩn hóa hay so khoảng MAX_TIME.

## BẢNG SĂN

Các lệnh chạy từ sandbox `xr3`, không phải từ checkout `cay-kho`.

| Hướng/giả thuyết | Lệnh đã chạy | Output thật và kết luận |
|---|---|---|
| Đối chứng cũ có tái hiện | `python3 -B review_probes.py legacy` | rc0; control `rc4/n7/6.0244s/true`; SIGSTOP 4,2s `rc4/n4/6.2165s/false`. **P3 cũ tái hiện.** |
| Máy chậm còn làm bản đúng đỏ | `python3 -B review_probes.py stall` | rc0; D8a 4,2s → `rc4/n4/10.2498s/true`; D8b 4,2s → `rc4/n2/4.2149s/true`; D8a 12s → `rc4/n4/18.0198s/true`. **Không còn lỗi trong các lịch đã đo.** |
| Tách D8 làm mất sức bắt mutation | `python3 -B review_probes.py retry` | rc0; ba baseline qua, ba mutation đỏ đúng predicate D8a/D8b/D7; bảng chi tiết dưới. **Không phải lỗi.** |
| Độ trễ che mất thiếu delay trên toàn bộ kiểm | `python3 -B review_probes.py slow_mutant` | rc0; `rc4/n7/66.2665s/stopped:4.2009s`, predicate D7 false. Riêng D8a có thể bị che; D7 vẫn bắt. **Không thấy toàn bộ kiểm xanh sai.** |
| Probe chép sai assertion hoặc knobs | `python3 -B review_probes.py audit` | rc0; đánh giá biểu thức `doi` và keyword `chay` trích AST exact head trên 10 phép đo: khớp tất cả; baseline true, target mutants false. **Không phải lỗi.** Đây là đối chiếu dữ liệu đo, không phải chạy HTTP. |
| Quá hạn làm xanh rỗng hoặc vế mới nuốt ngoại lệ | `python3 -B review_probes.py harness` | rc0; `TimeoutExpired` → `AssertionError,calls:23,failed_assertions:23,groups:D1..D8a/D8b,green:false`; OSError lan ra sau một lời gọi. **Không phải lỗi.** Unit fault injection thay server bằng context không socket và subprocess bằng ngoại lệ; không chạy curl/không nhận tín dụng mutation. |
| Đổi ngoài D8/vượt write set | `python3 -B review_probes.py scope` | rc0; chỉ định nghĩa t237 đổi, không thêm/xóa định nghĩa, định nghĩa cũ so base thay đổi rỗng; installer giống lượt 2; chỉ `ops/lease_publish_test.py` đổi `11+/4-` trong t237; hai patch khớp Git từng byte. **Không phải lỗi.** |
| Hồi quy cũ/lint mới | `python3 -B run_review_gate.py focused`; `python3 -B run_review_gate.py lint` | hai driver rc0; `lease_publish: 3/3 đạt; đã chạy=3, bỏ qua=0`; Ruff previous/head cùng rc1/cùng 9 lỗi cũ, delta0; bash-n/shellcheck rc0. **Không thấy hồi quy.** |
| HTTP t237 có đo được | `PYTHONDONTWRITEBYTECODE=1 python3 -B cay-kho/ops/lease_publish_test.py --chi-ca=t237` | rc1; `PermissionError: [Errno 1] Operation not permitted`; `lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0`. **KHÔNG ĐO ĐƯỢC**, lỗi tạo socket, không phải lỗi sản phẩm hay tín dụng mutation. |
| Có chạm checkout | `python3 -B review_probes.py integrity_before`; `python3 -B review_probes.py integrity_after` | rc0/rc0; `12248 → 12248`, `added:[],removed:[],changed:[],snapshots_equal:true`, HEAD/tree giữ nguyên, status rỗng. **Không có delta quan sát được.** |

Log: `review-evidence/{scope,assertion-audit,harness,slow-mutant,integrity}.jsonl`, `focused-driver.jsonl`, `lint-driver.jsonl`, `t237.log`. Harness focused lần đầu thiếu `sys.path` tới `ops`, khiến ba ca lỗi `ModuleNotFoundError: bash_nen`; đã sửa **harness ngoài kho**, chạy lại 3/3 đạt và giữ log setup lỗi ở `review-evidence/setup-error-*`. Không quy lỗi setup đó cho sản phẩm.

## BA ĐỘT BIẾN

`python3 -B review_probes.py retry`: installer thật trên bản sao tạm, curl thật với `--retry-all-errors`, nguồn file:// không tồn tại. Count lấy từ stderr curl37. Predicate đúng t237 được đối chiếu AST bằng `review_probes.py audit`.

| Đột biến / đối chứng | Vế | rc | n | Giây | Predicate đúng vế |
|---|---|---:|---:|---:|---|
| Bản đúng, mặc định retry8 | D7 | 4 | 9 | 8.0590 | true |
| Bản đúng, retry3/delay3 | D8a | 4 | 4 | 9.0242 | true |
| Bản đúng, delay1/max3 | D8b | 4 | 4 | 3.0169 | true |
| `bo_retry_delay` | D8a | 4 | 4 | 7.0220 | **false — GIẾT qua file://** |
| `bo_retry_max_time` | D8b | 4 | 9 | 8.0260 | **false — GIẾT qua file://** |
| `mac_dinh_retry_3` | D7 | 4 | 4 | 3.0155 | **false — GIẾT qua file://** |

Mỏ neo/thay duy nhất, script kiểm `count == 1` trước khi chạy:

- `bo_retry_delay`: xóa ` --retry-delay "$AL_RETRY_DELAY"`.
- `bo_retry_max_time`: xóa `--retry-max-time "$AL_RETRY_MAX_TIME"`.
- `mac_dinh_retry_3`: `AL_RETRY="${AL_RETRY-8}"` → `AL_RETRY="${AL_RETRY-3}"`.

Không có lỗi cú pháp/permission trong ba phép này: tất cả thật sự thử tải nhiều lần, rồi installer trả mã 4, có thông báo cuối đúng knobs. Đây là tín dụng phân biệt hành vi retry qua file://, **không tự nhận đã chạy t237 HTTP trên mutant**.

`bang_dot_bien_executor.txt` báo HTTP: bỏ delay đỏ D7/D8a; bỏ max-time đỏ D8b; default3 đỏ D7, đều rc1 và có tín hiệu assertion, khớp hướng đo file:// của reviewer. File còn báo 11/11 mutant chết đúng vế. Runner trỏ `/home/user/tra-luat`, là môi trường executor; không chạy nó lên kho read-only hoặc đổi bằng chứng executor thành phép đo độc lập.

## PHẠM VI, GATE VÀ GIỚI HẠN

So SHA lượt 2 chỉ một hunk trong t237, không đổi helper HTTP, `chay`, `doi`, D1–D7 hoặc D4–D6. So base: installer `36+/3-`, test `178+/0-`, tổng **214 dòng thêm trong 2 tệp**, dưới trần 250. Không đổi các ca cũ, workflow, hook, wrapper/công cụ khác. `git diff --check` rc0. Không thấy lỗi mới do tách phép đo, dùng `time.monotonic()` hoặc xử lý timeout.

| Check tại exact head | Trạng thái |
|---|---|
| t35/t37/t38 | **passed**, rc0, 3/3, không bỏ qua |
| `bash -n` / shellcheck installer | **passed**, rc0/rc0, không chẩn đoán |
| Bare Ruff `--no-cache --select F`, previous/head | **failed** tuyệt đối, rc1/cùng 9 lỗi; **passed tiêu chí delta0**. Dùng stdin với cùng `--stdin-filename` trỏ source để so cùng config/path. Ruff pin/probe contract không chạy lượt này. |
| t237 HTTP Linux | **not_measured**: socket EPERM; lệnh thực tế rc1, không gọi là pass |
| Toàn suite / actionlint workflow | **not_run** lại lượt này; không nhận kết quả SHA cũ làm gate exact head mới. Lượt này xác minh scope và chạy focused cho phần liên quan. |
| Windows t237+t35/t37/t38 | **not_measured** trong phiên Linux; theo SPEC do phiên điều phối chạy trên tra-luat-win, giữ KHOA.txt. Không gọi workflow. |

Snapshot byte đầu/cuối bao gồm tracked, untracked và ignored, không gồm metadata `.git`; bắt đầu sau preflight đọc. Giống nhau chỉ chứng minh không có delta nội dung quan sát được giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Chi tiết: `review-evidence/snapshot-before.json`, `snapshot-after.json`, `integrity.jsonl`.

## BẢNG LỚP

| Slug | Nguồn/trạng thái trước | Lượt này | Bằng chứng/giới hạn |
|---|---|---|---|
| `retry-window-request-count-flakiness` | P3, lượt 2 SHA 4458d06a… | **ĐÃ VÁ THẬT** cơ chế đỏ oan đã tái hiện | Đối chứng cũ fail dưới SIGSTOP; D8a/D8b mới qua; ba mutant chết đúng vế bằng file://. HTTP/Windows vẫn chưa đo độc lập. |
| `retry-max-time-decimal-equivalence` | P2 lượt 1; đóng ở lượt 2 | **GIỮ ĐÃ ĐÓNG**, không mở lại | Installer và D4 giống lượt 2 từng byte; không khai lặp 200 ca numeric lượt này. |

## FINDINGS

**Không có finding mới. P0–P2 mở: 0. P3 mục tiêu lượt này: đã đóng theo bằng chứng trên.** Bản đúng qua phản chứng lịch chạy mới; máy nhanh không tạo đường sống cho thiếu delay ở D8a; cả ba mutation còn bị bắt đúng vế. Giới hạn elapsed time dưới máy chậm đã ghi và đo thêm bằng D7; không nhận bằng chứng này là kết quả HTTP/Windows chưa chạy.
