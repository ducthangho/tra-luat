Bạn là REVIEWER ĐỘC LẬP cho work packet `W0-R1` của kho `tra-luat`. Đây là LƯỢT 2.

# Bối cảnh lượt 1 — đọc kỹ, nó đổi việc bạn phải làm
Lượt 1 (fable-5, xhigh) trả `blocked` vì **không chạy được lệnh nào**: permission
mode chặn mọi `python3 <script>`. Nó fail-closed đúng doctrine. Lượt này ĐÃ GỠ chặn:
bạn đang ở một **worktree tách rời** và có quyền chạy lệnh. Hãy kiểm chứng ngay đầu
phiên bằng `python3 .claude/dev/packet_loop_test.py`. Nếu VẪN không chạy được, nói
thẳng `KHÔNG ĐO ĐƯỢC` và trả `blocked` — đừng suy "pass" từ đọc tĩnh.

# Ràng buộc
- KHÔNG sửa tệp nào, không `git add/commit/push/checkout`. Nháp thì dùng `/tmp`.
- KHÔNG tin commit message của Executor. Nó là thứ CẦN KIỂM. Mọi con số trong verdict
  phải do CHÍNH BẠN chạy ra.

# Đối tượng
- reviewed_sha CHÍNH XÁC: `7dc8a2f7121d505cb35ffb517842468f547bb455`
- base: `5f6eb9295b4434afaf6295705b971ab7c5f33b53`
- diff: `git diff 5f6eb929...7dc8a2f7`  (hai commit: packet gốc + lượt vá)
- Write set ĐƯỢC PHÉP: CHỈ `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`.
  W0-R1 KHÔNG được sửa `ops/lease_publish.py`.

# Spec đã đóng băng (ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md)
- Outcome: state có `codex_review_calls_used`, `codex_executor_calls_used`,
  `review_rounds_used`, review cycle count và checkpoint transition; review cap không
  vay executor budget và ngược lại.
- Acceptance: call đã sinh output/token nhưng timeout/sai schema vẫn tiêu call;
  preflight/permission/rate-limit trước generation không tiêu call; call thứ ba bị từ
  chối; đổi prompt/session không reset.
- Phản chứng: raw output sai schema hai lần rồi prompt mới vẫn không mở được call thứ ba.

# Phần A — kiểm 5 finding của lượt 1 đã được vá THẬT chưa
Executor khai đã vá cả 5. ĐỪNG tin, hãy tự dựng lại phản chứng cho từng cái:
1. `review-rounds-khong-dem-vong-cham-tran` — hai review cùng finding-id tới trần;
   `len(reviews)` có bằng `review_rounds_used` không?
2. `review-calls-key-thieu-trace-tho` — state có đủ khoá đếm nhưng thiếu `review_calls`;
   có rc=8 không, hay vẫn vỡ traceback?
3. `void-attempt-van-ghi-so-o-checkpoint` — ở `checkpoint`/`blocked`/`accepted`,
   `void-attempt` có bị chặn không, `attempts_used` có đổi không?
4. `thieu-phan-chung-fail-closed-state-cu` — chốt fail-closed nay có mutant chưa, và
   mutant đó có THẬT SỰ giết ca đích không? Tự áp mutant lên bản sao tạm mà kiểm.
5. `chieu-hai-chot-nhan-so-do-khong-co-dot-bien` — như trên, cho chiều 2.
Cái nào vá HỎNG hoặc vá NỬA VỜI thì ghi thành finding mới.

# Phần B — tìm lỗ MỚI, hai trục độc lập
Đọc `CLAUDE.md` trước; kho có doctrine riêng. Soi kỹ:
- Còn đường nào tiêu quá 2 lời gọi review, hoặc né bộ đếm? (`init` đè, đổi
  `--state-dir`, sửa tay state, lệnh khác trong cùng tệp, `record-review` vs
  `record-review-call`…)
- `checkpoint` có thật sự là ngõ cụt ở MỌI cửa không?
- Phân loại tiêu/không-tiêu dựa vào nhãn người gõ + `--output-bytes`. Còn cách nào
  khai một lời gọi ĐÃ tốn tài nguyên thành không-tiêu không?
- Chỗ nào fail-open mà lẽ ra fail-closed, hoặc ngược lại (fail-closed quá tay làm kẹt
  đường hợp lệ)?
- Ca nào XANH RỖNG — chạy mà không đo gì, hoặc không thể đỏ?

# Phép thử BẮT BUỘC
1. `python3 .claude/dev/packet_loop_test.py` — ghi rc và trọn dòng số liệu cuối.
2. Tự nghĩ ≥4 đột biến MỚI (khác 41 cái đã có), áp lên BẢN SAO TẠM, chạy lại suite.
   Đột biến sống sót = finding.
3. Lách trực tiếp bằng CLI trong `/tmp`: cố tiêu >2 lời gọi review, hoặc đưa packet ra
   khỏi `checkpoint`.
4. `git status --short` đầu và cuối phiên — phải rỗng cả hai lần.

# Verdict — in ra CUỐI CÙNG, đúng khối này
```yaml
reviewed_sha: 7dc8a2f7121d505cb35ffb517842468f547bb455
verdict: approve | changes_requested | blocked
spec_axis: pass | fail
standards_security_axis: pass | fail
gates:
  - packet_loop_test: rc=<...> <dòng số liệu cuối cùng suite in ra>
  - dot_bien_tu_nghi: <M>/<N> bị bắt
  - va_luot_1: <số/5 finding đã được xác minh vá THẬT>
  - write_set: <số tệp đổi> / ngoài write set: <số>
  - cay_sach_dau_cuoi: <có/không>
findings:
  - id: <slug-kebab-case>
    severity: P1 | P2 | P3
    locator: <tep>:<dong>
    evidence: <phản chứng CHẠY ĐƯỢC, có lệnh và output>
    required_repair: <sửa gì>
khong_do_duoc: []
```
`findings: []` nếu sạch. `changes_requested` phải có ít nhất một finding kèm phản
chứng chạy được.
