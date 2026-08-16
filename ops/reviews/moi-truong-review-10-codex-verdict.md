# Cross-review lượt 10 — `ops/moi-truong-ba-p1`

- Reviewer: `codex`
- Head bất biến: `a3fd3ff705bf4831495b1988de7655b32dc68197`
- Verdict: **changes_requested**
- Phạm vi: chỉ đọc; không sửa/commit/push/merge/land/deploy cây kho.

## Findings

### MEDIUM — Gỡ một config CRLF làm đổi kết thúc dòng của toàn bộ phần người dùng

Vị trí: `.claude/dev/codex_env_policy.py:275` (đọc text) và `:290` → `:199-204` (ghi text/replace).

`Path.read_text(encoding="utf-8")` mở với universal-newline, nên CRLF được đổi thành `\n` trước cả `go_khoi`. Khối CRLF thật được chấp nhận (điều này tốt), nhưng khi ghi lại, không chỉ khối bị gỡ: mọi dòng còn lại của người dùng bị đổi CRLF → LF. Điều này trái hợp đồng bảo toàn phần ngoài khối được nhấn mạnh ngay trong mã.

Phản chứng chạy trong `TemporaryDirectory`, không đụng config thật: tạo canonical block và phần `[user]` hoàn toàn bằng CRLF, gọi `main(["--tep", ...])`. Kết quả `rc=0`, nhưng `crlf_con_lai=0`, bytes còn lại là `b'[user]\nname = "giu-nguyen"\n'`.

Đề nghị đọc/ghi với `newline=""` (hoặc bằng bytes), nhận diện newline của khối mà không chuẩn hoá phần được giữ, và thêm fixture kiểm bytes ngoài khối bất biến. BOM hiện bị từ chối oan một cách an toàn; CRLF hiện không bị từ chối mà gây sửa ngoài phạm vi, nên là lỗi cần sửa.

### MEDIUM — `os.replace` vẫn làm mất chỉnh sửa đồng thời giữa lần đọc và lần thay thế

Vị trí: `.claude/dev/codex_env_policy.py:275-290`, đặc biệt `ghi_nguyen_tu` tại `:182-204`.

`mkstemp` đã đóng lỗ symlink tên tạm và bảo đảm reader thấy bản cũ hoặc bản mới, nhưng không bảo đảm bản đang thay vẫn là bản đã đọc. Không có compare-before-replace, lock, hay kiểm `(st_dev, st_ino, mtime_ns, size)`/digest ngay trước `os.replace`. Một editor hoặc Codex ghi config sau dòng 275 nhưng trước dòng 204 sẽ bị bản dựng từ snapshot cũ ghi đè, làm mất thay đổi.

Phản chứng xác định: sau khi `main` đọc config và dựng `moi`, wrapper tại cửa `ghi_nguyen_tu` thay đích bằng `'[a]\nx=2\n# concurrent edit\n'`, rồi gọi writer thật. Kết quả `rc=0`, nội dung cuối là `'[a]\nx=1\n'`: chỉnh sửa đồng thời mất hoàn toàn.

Đề nghị giữ fingerprint/file descriptor của bản đã đọc và fail-close nếu đường đích thay inode hoặc nội dung/metadata đổi trước replace; tốt hơn là dùng cơ chế lock/compare-and-swap phù hợp nền. Cũng cần test mutation ngay trong cửa sổ này. Race `islink` → `replace` còn có thể thay mất một symlink vừa được tạo, dù không ghi xuyên vào target của symlink.

## Kết quả đo bắt buộc

### Bước 0

- `git rev-parse --is-shallow-repository` → `false`.
- `git config --get core.abbrev` → `7`.
- `git rev-parse HEAD` → `a3fd3ff705bf4831495b1988de7655b32dc68197`.
- Diff từ `1df800be15580d7432a1200900dd04ed9a7b997c` đúng 5 tệp được khai.

### Bản khai môi trường

```json
{
  "he_dieu_hanh": "Linux",
  "python": "3.11.15",
  "pid": 4,
  "ppid": 2,
  "pgid": 1,
  "sid": 1,
  "la_truong_nhom": false,
  "chung_nhom_voi_cha": true,
  "co_job_control": null,
  "stdin_la_tty": false,
  "stdout_la_tty": false,
  "ns_pid": "pid:[4026532315]",
  "ns_pid_cua_init": "pid:[4026532315]",
  "tien_trinh_1_la": "3",
  "co_dockerenv": false,
  "so_cpu": 4
}
```

Không in giá trị biến môi trường/token; mọi lần chạy dùng HOME tạm.

### `t72` và suite đầy đủ

- `--lap-ca t72 --lan 40 --nhat-ky ...`: `40/40` vào, `40/40` ra, không lần chết, có `# XONG TRON VEN`, rc=0. Stdout của công cụ thu kết quả dừng hiển thị sau lần 38, nhưng nhật ký bền và tệp rc xác nhận đủ 40 lần.
- Kết luận theo protocol: `t72` **một mình không chết** trên nền reviewer; cái chết trước đây cần ngữ cảnh hoặc không tái hiện ở lượt này. Không đoán nguyên nhân.
- Suite đầy đủ có nhật ký: `102/102` ca; 101 qua, 1 bỏ qua fixture Windows, 0 hỏng; `vao=102`, `ra=102`, không ca chết, có `# XONG TRON VEN`.

### Hai lượt tự đột biến

- Lượt 1: rc=0, `58/58 dat`, 1 không đo được trên nền này.
- Lượt 2: rc=0, `58/58 dat`, 1 không đo được trên nền này.
- Hai lượt cùng con số như khai. Cổng xanh không phủ hai phản chứng findings ở trên.

## Trả lời các câu hỏi delta

- Fail-close: các lệnh gọi Codex trong mã kho thấy được đều qua guard tương ứng; hook đặt `CODEX_BI_CHAN=1` cho mọi rc khác 0 của bộ gỡ và bọc cả hai lệnh hook. Phạm vi “cửa của kho, không phải lệnh gõ tay” là đúng. Nếu không ghi được cờ bền, phiên hook hiện tại vẫn chặn nhờ biến shell; phiên khác không có cờ thì không thể được bảo đảm, và thông báo đã khai phải chặn tay.
- Canonical: chuẩn hoá trailing whitespace/dòng trắng biên không mở lỗ nội dung đáng kể trong chính thân canonical; `t100(e)` chỉ là phép quét lexical, không phải chứng minh tuyệt đối rằng không thể sinh chuỗi bằng cách ghép/dynamic. Việc cắt cả vùng hằng có thể che side effect nếu ai nhét biểu thức có tác dụng vào tuple; nên test hành vi/AST tốt hơn quét chuỗi. CRLF là lỗi bảo toàn thật như finding; BOM bị từ chối oan nhưng fail-close.
- Symlink đích: từ chối là lựa chọn an toàn, nhưng hướng dẫn `--tep <realpath>` chưa gỡ ngay cờ cạnh symlink gốc trong chính lần đó; lần chạy mặc định kế tiếp mới thấy target sạch và gỡ cờ. Nên nói rõ hoặc cho phép chỉ định đúng cờ gốc.
- Quyền: giữ nguyên `0644` là đúng với phạm vi “chỉ gỡ, không âm thầm đổi metadata”; vị trí cạnh `auth.json` không biến `config.toml` thành secret. `mkstemp` bắt đầu `0600`, sau khi ghi/fsync mới mở rộng tới mode cũ, nên không có khoảnh khắc dữ liệu mới rộng hơn mode người dùng đã chọn. Tuy nhiên race mode/nội dung trước replace là finding thứ hai.
- CLI: `t101` phủ `--lan` thiếu `--lap-ca`, `--lan 0`, mode conflict và các flag lặp chính. Khớp tiền tố nhưng từ chối 0 hoặc nhiều hơn 1 ca là hành vi chẩn đoán hợp lý; không đoán khi mơ hồ.

## Kết luận

Hai bản vá lớn của lượt này (guard chung và `mkstemp`) đi đúng hướng, nhưng writer vẫn sửa ngoài khối trên CRLF và vẫn có lost-update race. Vì đây là đường tự động sửa config người dùng, nhánh chưa nên dừng ở trạng thái hiện tại và chưa thể approve.
