# Thẩm định chung Claude–Codex cho kế hoạch orchestrator

> - Ngày thẩm định: 17-08-2026
> - Base/HEAD: `1a6aedf6b92ff271bf07a8b9deee2f83d430ed49`
> - Worktree: `work/orchestrator-process-plan`
> - Trạng thái: **đã hội tụ sau 5 vòng; chủ kho đã duyệt D1/D2 và bundle A–G; tài liệu kế hoạch đã cập nhật, runtime chưa triển khai**

## 1. Kết luận điều hành

Claude Opus/max và Codex thống nhất giữ nguyên khung người dùng đã chốt:

- Claude Opus/max là Executor mặc định;
- Codex là Reviewer read-only trên exact PR head cho packet giá trị/rủi ro cao, tối đa hai lượt mỗi PR;
- sau hai lượt Codex chưa approve thì dừng gọi Codex, checkpoint để tách stable slice hoặc xem lại
  thiết kế;
- packet thường có thể hạ sang same-provider/human; phạm vi nhạy cảm vẫn chờ Codex hoặc human audit;
- giữ Codex làm Executor ở tỷ trọng thấp, mục tiêu 30/70, không lấy slot review để bù executor budget;
- tối đa hai writer độc lập, không preempt writer đang chạy; rework nhận slot kế tiếp theo priority/tie-break;
- skill tiếp tục là adapter mỏng; protocol là nguồn quy tắc;
- mỗi packet phải có phản chứng chạy được;
- connector/App/shadow không có quyền phán khi chưa qua bằng chứng và promote gate.

Không còn bất đồng kỹ thuật. Chủ kho đã duyệt hai lựa chọn:

1. deadline khởi điểm `90 phút Executor / 90 phút Reviewer`;
2. không bồi 11 receipt v1 cũ; giữ chúng là historical/read-only và không cho nâng quyền thành
   bằng chứng identity v2.

## 2. Cách thẩm định

Claude được gọi qua `.claude/dev/launcher.py`, cùng một session, model Opus, effort max, permission
mode `plan`, cấm `Edit`, `Write`, `NotebookEdit`. Mỗi lượt đều neo repo, root commit, HEAD, ref, prompt
SHA và deadline.

| Vòng | Run | Mục tiêu | Kết quả |
|---|---|---|---|
| 1 | `dc43102f` | audit toàn bộ plan/protocol/ADR | 8 nhóm finding; không đề nghị đổi khung |
| 2 | `02018969` | Codex phản biện finding và thu hẹp scope | hội tụ về probe, receipt, sandbox, queue; phát hiện deadline/standby |
| 3 | `ade01b3b` | chốt lane, path map, bundle A–G | chốt thứ tự; sửa write set W0-R2; còn 2 owner decision |
| 4 | `f492c0bb` | chọn khuyến nghị cho 2 owner decision | đề nghị `90/90` và receipt-v1 allowlist đóng băng |
| 5 | `2aa50f0a` | hiệu chính clock semantics | thống nhất working-state clock; đóng phiên, không còn dissent |

SHA-256 của cả năm prompt source vẫn khớp `prompt_sha256` trong từng `run.json`; audit trail không bị
viết lại sau khi model trả lời.

Một lần gọi r1 trước đó bị từ chối kết nối trước khi model làm việc (`052c1eaa`, zero
token/cost); một preflight bị Git `dubious ownership`. Biện pháp khôi phục chỉ là process-local
`safe.directory`, không sửa global Git config.

Claude không sửa tệp. Năm prompt và biên bản này do Codex ghi để giữ audit trail. Không có commit,
push, cài package hay workflow/GitHub mutation.

## 3. Finding đã thống nhất

| ID | Mức | Phát hiện | Điều chỉnh chốt |
|---|---|---|---|
| F1 | MUST | Doctor tìm candidate path của Codex nhưng probe lại gọi tên trần; lỗi một candidate có thể che candidate sau. Fingerprint sandbox và host khác nhau. | Thêm W0-M3 P0 trước M4/M2: gọi đúng path, thử candidate kế, ghi path+lỗi; fingerprint luôn kèm actor/environment/time. |
| F2 | MUST | Code block ghi review state đang đặt `record-review` trước `begin-attempt`/`reviewing`. | Sửa §7.4a/§7.5 theo thứ tự chạy được: begin, publish/record-post, transition exact head, gọi reviewer, record-review. |
| F3 | MUST | Kho đã có `review_delivery_receipt`, `delivered_by`, `receipt_written_by`, t26/t27. Xây schema identity song song sẽ tạo hai nguồn sự thật. | W0-R2 nâng receipt hiện có; W0-R3 để packet state chỉ tham chiếu receipt id/hash đã validate. Khai rõ anchor strength; không bắt tag tuyệt đối. |
| F4 | SHOULD | `codex_calls_used` mơ hồ khi Codex có thể là Executor. | Tách `codex_review_calls_used` và `codex_executor_calls_used`; review cap không vay budget executor. |
| F5 | SHOULD | Dossier mô tả review worktree read-only đầy đủ, trong khi skill hiện tại dùng prepared sandbox với closed read scope. | Giữ adapter hiện tại khi bootstrap và khai caveat; thêm W1-S1 sau W1-P1+W0-R3; đánh dấu command là `target-after-W1-S1`. |
| F6 | SHOULD | Chưa có luật rework giành lại writer slot; nhiều write set mới chỉ là prose. | Rework lấy slot kế tiếp, không preempt; cùng priority thì rework trước unstarted, khác priority thì P cao hơn đi trước. Pin path/prefix `planned:`. |
| F7 | SHOULD | Targeted doc-claims xanh nhưng bỏ qua L9. | Evidence dossier phải ghi rõ `layers_skipped: L9`; không trình bày như full-layer pass. |
| F8 | MUST | Launcher có absolute `deadline_utc` nhưng một `p.wait(timeout=...)` dài trên Windows không đếm low-power state; r1 chạy 3456s vẫn `xong` dù deadline 1799s. | W0-M4 P0: wait theo lát, so lại wall clock mỗi lát, giữ kill-tree/rc 124–125; ghi wall và working-state evidence bằng clock đã kiểm chứng. |
| F9 | MUST | Đặt W0-M1 sau M3/M4 khiến ba packet đầu được báo cáo bằng headline đang tính skip là pass. | Đảo W0-M1 lên đầu launcher lane. |

## 4. Thứ tự thi công chốt

```text
launcher : W0-M1(P0) → W0-M3(P0) → W0-M4(P0) → W0-M2(P1)
review   : W0-R1(P0) → W0-R2(P1) → W0-R3(P1)
mở màn   : W0-M1 ∥ W0-R1
W0-C1(P1): slot an toàn đầu tiên sau khi một lane đóng/yield, nếu executor budget Codex cho phép
M2       : W1-P1 → (W1-G1 → W1-G2) · W1-C2a → W1-C2b
W1-S1    : sau W1-P1 + W0-R3
```

Hai writer chỉ chạy song song khi write set không chồng lấn. Các packet cùng seam ở từng lane phải serial.
W0-C1 không được chen vào bằng cách cướp slot của P0 hay tiêu budget review.

### Path map bổ sung/sửa

| Packet | Write set chốt ở mức kế hoạch |
|---|---|
| W0-M1/M3/M4/M2 | `.claude/dev/launcher.py` và/hoặc `.claude/dev/launcher_test.py`, đóng băng chi tiết theo từng Issue |
| W0-R2 | `ops/lease_publish_test.py`; `ops/reviews/README.md` nếu contract index đổi; `planned:.github/coordination/schemas/review_delivery_receipt.v2.schema.json`; validator runtime nếu cần là module mới `planned:ops/review_receipt.py` |
| W0-R3 | `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py` |
| W0-C1 | `planned:.claude/dev/review_connector.py`, `planned:.claude/dev/review_connector_test.py` |
| W1-P1 | `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`, `planned:.github/coordination/schemas/review_verdict.v1.schema.json` |
| W1-G1 | `planned:.claude/dev/gate_lifecycle.py`, `planned:.claude/dev/gate_lifecycle_test.py` |
| W1-G2 | `.claude/dev/gate_lifecycle_test.py`; mutant dùng temporary copy, không sửa production gate |
| W1-C2a | `.claude/dev/review_connector.py`, `.claude/dev/review_connector_test.py` |
| W1-C2b | `planned:.github/workflows/review-connector-shadow.yml` |
| W1-S1 | `.claude/skills/cross-review/SKILL.md` |

**Không sửa `ops/lease_publish.py` trong W0-R2.** Tệp này là cổng đăng lease và không chứa receipt logic;
mở write set ở đó không tạo thêm năng lực cần thiết.

## 5. Bundle A–G sẽ áp dụng sau khi được duyệt

| Gói | Chỉnh sửa |
|---|---|
| A | Sửa fingerprint, thêm W0-M3/W0-M4, đổi launcher lane để W0-M1 đứng đầu. |
| B | Sửa §7.4a/§7.5 theo state order có thể chạy. |
| C | Tách review-call counter khỏi executor-call counter. |
| D | Tái dùng receipt hiện có qua W0-R2/R3; khai anchor strength; áp receipt-v1 allowlist đóng băng. |
| E | Thêm W1-S1 và đánh dấu command chỉ là target sau W1-S1. |
| F | Pin `planned:` path/prefix; thêm rework next-slot và tie-break, không preempt. |
| G | Khai rõ L9 bị skip trong evidence dossier. |

Bundle này chỉ làm kế hoạch thi công đúng với khung đã chốt; không đổi chính sách vai trò, review
cap, fallback hay 30/70.

## 6. Hai owner decision đã duyệt

### D1 — deadline `90/90`

**Khuyến nghị chung:**

- deadline vẫn là absolute wall-clock, fail-closed;
- 90 phút cho Claude Executor và 90 phút cho Reviewer;
- không tự sửa/chặn power policy;
- xem lại profile sau 3–5 lượt thật, không tự nâng trần;
- sổ ghi `wall_elapsed_seconds`, `working_elapsed_seconds`, `working_clock`, `timeout_clock=wall`;
- W0-M4 chỉ cung cấp bằng chứng, không tự động `void-attempt`. Operator có thể dùng cơ chế void hiện
  có khi bằng chứng xác nhận lỗi hạ tầng; tự động hóa sau này phải là packet riêng.

Lý do chọn 90/90: lượt reviewer toàn diện r1 chạy 57,6 phút wall, trong đó khoảng 43 phút là Modern
Standby. Trần reviewer 45 phút sẽ giết đúng lượt audit có giá trị nhất. 90 phút vẫn là trần hữu hạn,
không phải cho chạy vô hạn.

Clock semantics đã kiểm lại:

- `WaitForSingleObject` trên Windows 8+ không tính low-power state;
- Python `time.monotonic()` trên máy này dùng `QueryPerformanceCounter`, mà QPC có tính thời gian sleep;
- trên Windows, working-state metric phải dùng `QueryUnbiasedInterruptTime` sau khi probe symbol an toàn;
- nền chưa đo được working-state clock thì ghi `null/unavailable`, không suy đoán từ Windows.

Nguồn chính thức:

- [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [Acquiring high-resolution time stamps](https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps)
- [Windows Time](https://learn.microsoft.com/en-us/windows/win32/sysinfo/windows-time)

Phản chứng W0-M4 phải tách hai bất biến:

1. wall clock nhảy qua deadline khi process còn sống ⇒ timeout và kill tree;
2. fake working clock không nhảy trong khoảng sleep mô phỏng ⇒ wall elapsed lớn hơn working elapsed.

### D2 — receipt v2 không viết lại lịch sử

**Khuyến nghị chung:**

- identity fields v2 bắt buộc cho mọi receipt tạo mới sau cutover;
- giữ nguyên 11 receipt v1 hiện có, không bồi identity bằng suy đoán;
- v1 là historical/read-only và không đủ tư cách làm identity evidence cho required check mới;
- legacy exemption neo vào allowlist đóng băng gồm đúng 11 filename + hash, không neo vào
  `schema_version` do tác giả receipt tự ghi;
- tệp mới khai `schema_version: 1` vẫn phải đỏ.

Phản chứng bắt buộc:

1. receipt mới mang v1/thiếu identity ⇒ đỏ;
2. mutant nới allowlist để chứa tệp tấn công ⇒ ca đích đỏ;
3. 11 legacy filename/hash đóng băng vẫn đọc được như lịch sử nhưng không thể thỏa required-check v2.

## 7. Không khuyến nghị

- Không để reviewer 45 phút trong khi Executor 90 phút: vai trò không quyết định thời gian Modern Standby.
- Không đổi timeout sang active-time: như vậy làm mất nghĩa của absolute deadline và có thể giữ process
  sống quá lâu theo wall clock.
- Không tự động chặn standby hay sửa power policy: phát sinh quyền/side effect ngoài nhu cầu.
- Không gọi `time.monotonic()` là awake/working clock trên Windows.
- Không auto-void attempt từ một ngưỡng mềm trong W0-M4: nó cắt qua seam launcher/packet-loop và
  có thể xoá oan attempt.
- Không tự khai legacy bằng `schema_version: 1`: input yếu do tác giả tự ghi không được quyết định
  mức trust.
- Không bồi receipt cũ bằng suy đoán và không mở `ops/lease_publish.py` chỉ vì receipt v2.
- Không gộp M3+M2 hoặc G1+G2: mỗi packet đang đo một bất biến khác nhau.
- Không mở vòng review kế hoạch thứ sáu; bước kế tiếp là đóng băng Packet Spec W0-M1 và W0-R1
  sau khi chủ kho duyệt.

## 8. Giới hạn sau khi áp dụng tài liệu

- Bundle A–G và D1/D2 đã được chép vào plan/protocol/ADR sau phê duyệt của chủ kho.
- W0-M1…W1-S1 chưa được implement trong lượt thẩm định này.
- Working-state clock trên Linux/macOS chưa được đo trong phiên này; implementation phải probe theo nền
  và fail thành `unavailable`, không sao chép kết luận Windows.
- Profile 90/90 là giá trị khởi điểm có bằng chứng một audit dài; chưa phải percentile ổn định của
  review code. Việc xem lại sau 3–5 run là một phần của quyết định.

## 9. Hành động sau khi cập nhật kế hoạch

Sau khi D1, D2 và bundle A–G đã được duyệt:

1. giữ thay đổi ở lớp tài liệu kế hoạch/protocol/ADR trong worktree này;
2. chạy `doctrine-scan`, targeted doc-claims và kiểm whitespace/diff;
3. không implement production code trong cùng bước;
4. đóng băng Packet Spec W0-M1 và W0-R1 để hai Claude Executor có thể mở song song;
5. chỉ mở Codex review khi packet thuộc class cần cross-provider và exact PR head đã neo.
