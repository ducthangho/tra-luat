Bạn là REVIEWER ĐỘC LẬP cho work packet `W0-R1` của kho `tra-luat`. Đây là LƯỢT 4,
và là lượt QUYẾT ĐỊNH: nếu sạch thì packet được chấp nhận ở mức `same_provider_approved`.

# Bạn CHẠY ĐƯỢC lệnh
Đã cấp `Bash(python3:*)`. Việc số một: chạy `python3 .claude/dev/packet_loop_test.py`,
ghi rc + dòng số liệu cuối. Nếu không chạy được, nói `KHÔNG ĐO ĐƯỢC` và trả `blocked`.

BẪY ĐÃ CÓ NGƯỜI VẤP: chạy suite từ `/tmp` sẽ cho ĐỎ GIẢ vài ca (chúng tìm tệp kho theo
đường dẫn tương đối và tìm lịch sử git). Đặt bản sao đột biến TRONG `.claude/dev/` của
worktree bạn đang đứng, hoặc trừ ra và nói rõ đã trừ cái nào.

# Ràng buộc
- KHÔNG sửa tệp trong cây kho, không `git add/commit/push/checkout`. Nháp dùng `/tmp`.
- KHÔNG tin commit message của Executor. Mọi con số phải do CHÍNH BẠN chạy ra.

# Đối tượng
- reviewed_sha: `c9042bfe1df8e27a76ec685b89122701eeabe538`   ·   base: `5f6eb9295b4434afaf6295705b971ab7c5f33b53`
- Write set ĐƯỢC PHÉP: CHỈ `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`.

# Lịch sử ba lượt trước — để bạn KHỎI đo lại thứ đã đo
- Lượt 1 và 2 `blocked` vì không chạy được lệnh (lỗi setup, đã sửa).
- Lượt 3 đo động trọn vẹn: suite xanh, 4/4 acceptance qua CLI thật, 8/8 vá trước là thật.
  Nhưng 7 đột biến tự nghĩ SỐNG SÓT CẢ 7 ⇒ 7 cửa cưỡng chế không có phản chứng:
  provider của `record-review-call`; cờ `--review-calls-limit`; `checkpoint` không có
  lối ra; cửa `reviewing` của `record-review`; chặn `--output-bytes` âm; trường `tieu`
  trong sổ cái; `ok`+0 byte.
- Executor khai đã vá cả 7 (6 cặp ca+đột biến, 1 sửa mã: bỏ miễn trừ `ok`).

# ĐÃ BIẾT, ĐÃ KHAI — đừng báo lại như finding mới
`record-review` KHÔNG đọc sổ lời gọi, nên bỏ qua hẳn `record-review-call` thì nhiều
vòng review vẫn khép trọn với `used=0`. Executor khai thẳng điều này trong docstring
`cmd_record_review_call` và hoãn sang packet riêng, vì vá nó là đổi cách hai trần hợp
thành nhau. CHỈ báo lại nếu bạn đo ra mô tả ấy SAI, hoặc tìm được đường lách KHÁC HỌ.

# Việc của bạn
## A. Xác minh 7 bản vá là THẬT
Với mỗi cửa: tự áp đột biến lên bản sao, chạy suite, xem ca đích có CHẾT không. Một
cặp ca+đột biến chỉ có giá trị nếu ca đó thật sự chết khi cửa bị gỡ. Đặc biệt soi ca
`record_review_bi_chan_o_state_cuoi` — bản đầu của nó KHÔNG đo cửa nó khai là đang đo
(nó chết ở chốt `attempt_open` kế tiếp), Executor đã sửa; hãy kiểm bản sửa có thật sự
phân biệt được cửa `reviewing` hay không.

## B. Tìm cửa CÒN LẠI chưa có phản chứng
Tự nghĩ ≥6 đột biến MỚI (khác 50 cái đã có), áp lên bản sao, chạy suite. Sống sót =
finding. Ưu tiên: các chốt trong `cmd_record_review_call`, `cmd_void_attempt`,
`cmd_record_review`, bảng `CHUYEN_HOP_LE`, và bộ đếm trong `cmd_init`.

## C. Lỗ mới ngoài đột biến
Đọc `CLAUDE.md`. Soi: đường né bộ đếm; `checkpoint` kín ở MỌI cửa chưa; nhãn
tiêu/không-tiêu còn khai gian được không; fail-open/fail-closed đặt sai chỗ; ca XANH RỖNG.

## D. Bắt buộc
`git status --short` đầu và cuối phiên — rỗng cả hai lần.

# Verdict — in CUỐI CÙNG, đúng khối này
```yaml
reviewed_sha: c9042bfe1df8e27a76ec685b89122701eeabe538
verdict: approve | changes_requested | blocked
spec_axis: pass | fail
standards_security_axis: pass | fail
gates:
  - packet_loop_test: rc=<...> <dòng số liệu cuối>
  - va_luot_3_xac_minh: <số>/7 cặp ca+đột biến là THẬT
  - dot_bien_moi: <M>/<N> bị bắt
  - write_set: <số tệp đổi> / ngoài write set: <số>
  - cay_sach_dau_cuoi: <có/không>
findings:
  - id: <slug-kebab-case>
    severity: P1 | P2 | P3
    locator: <tep>:<dong>
    evidence: <lệnh + output THẬT>
    required_repair: <sửa gì>
khong_do_duoc: []
```
`findings: []` nếu sạch. Đừng hạ chuẩn để cho qua, cũng đừng bịa finding để tỏ ra kỹ.
