# Verdict: changes_requested

- Reviewer: `codex`
- Lease: `moi-truong-review-4-codex-20260815`
- Reviewed head: `fe895a068368754bd11b25ca59c504f973e9f086`
- Delta base: `c89ca5929c2d5da6c182f7858e652c51df147cd5`
- Master base: `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`
- Prompt SHA-256: `50908590c3beb7bc08b2d2d75d74b6d6c80a042535d5f1b184208a472c072848`
- `la_viec_cua_packet: false`

## Findings

### `launcher-caller-still-does-not-survive-self-detach`

- Severity: high
- Disposition: changes_requested

Chốt mới cho phép Python chạy hết và in `90/90`, nhưng chưa đạt chính tiêu chí hồi quy:
lệnh shell ngay sau Python vẫn không chạy. Hai phép đo độc lập đều chỉ để lại marker
`before`, không có marker `after`; điều này xảy ra cả khi gọi trực tiếp (Python báo
`da tach sang session moi`) lẫn khi bọc `setsid` từ ngoài (Python báo đã là trưởng
nhóm). Log cuối cùng có đủ `90/90`, nên đây không còn là thiếu flush/tổng kết: caller
bị kết thúc hoặc bị cơ chế điều phối bỏ lại sau khi tiến trình test đổi session.

Bằng chứng neo head bất biến, HOME luôn là thư mục tạm:

```bash
probe_home=$(mktemp -d)
printf 'before\n' > /tmp/direct.marker
HOME="$probe_home" python3 .claude/dev/launcher_test.py >/tmp/direct.log 2>&1
printf 'after rc=%s\n' "$?" >> /tmp/direct.marker
```

`direct.log`: SHA-256
`db4f724e6ab8efe8dad4a575c2de35b3cc79ee7994e85f44a870d55b21d2e6e6`, 218 byte;
`direct.marker`: SHA-256
`c784bb5fcf473ac028d0a2f2b8ec118238c0588ca34a9d3e24f0e3423cd47568`, 18 byte,
chỉ có `before`. Đối chứng `setsid` cũng `90/90` nhưng marker giống hệt; log SHA-256
`f057361da3ad21fdf9f13b488851a8f63233f01ea7adcfff966fa852e486d02a`, 214 byte.

Không xác định được đích danh ca phát tín hiệu: `launcher_test.py` không gọi `killpg`
trực tiếp; các điểm thật ở `launcher.py:720` và `launcher.py:739`, được nhiều ca CLI
kích hoạt. Việc tự `setsid()` cũng có tác dụng phụ kiến trúc: bỏ terminal điều khiển và
không còn nhận tín hiệu gửi cho nhóm cũ. Suite hiện không cần nhập terminal/job control,
nhưng không có test khóa hành vi truyền tín hiệu từ caller; vì vậy không thể coi đổi
session là trong suốt.

### `launcher-mutation-gate-still-red`

- Severity: high
- Disposition: changes_requested

Hai lượt `--dot-bien` độc lập đều rc=1 và cùng kết quả `46/47`: mutation
`do_codex_tin_DONG_DAU_thay_vi_ma_thoat` sống (`giet 0/1`); một mutation Windows
không đo được trên POSIX. Đây là cổng bắt buộc đỏ tất định, đồng thời vẫn thiếu bằng
chứng cho đường xác thực fail-closed.

- Lượt 1 log: SHA-256 `98dfedbe46fc93c5e1631b8f0f1c0fa1f7d266292104355940d6eae6214c71e7`,
  4727 byte; marker có `after rc=1`.
- Lượt 2 log: cùng SHA-256 và kích thước; marker có `after rc=1`.

## `t90`, xanh giả và tác dụng phụ

`t90` có răng cho bốn nhánh đã khai. Trên bốn bản sao tạm, lần lượt ép sai (a) quyết
định tách, (b) quyết định không tách, (c) cảnh báo khi `setsid` lỗi, và (d) fail-closed
khi không đọc được PGID; cả bốn đều làm lời gọi riêng `t90` đỏ `AssertionError`.

Ca này chỉ đo quyết định bằng mock, không chứng minh `setsid()` thật bảo toàn caller,
terminal hay tín hiệu. Các ca giết-cây vẫn chạy CLI thật và mutation gate vẫn thực sự
đỏ, nên không có bằng chứng chúng đã xanh giả chỉ vì session mới; ngược lại, thất bại
caller ở trên cho thấy seam thật mà `t90` không phủ.

## Gates và boundaries

- Bước 0 khớp: non-shallow, `core.abbrev=7`, HEAD/ref đúng SHA, remote đúng, delta đúng
  một tệp `.claude/dev/launcher_test.py`; cây kho sạch sau mọi probe.
- Không chạy Windows; một mutation không đo được trên POSIX.
- Không fetch/config trong vai reviewer; điều phối đã chạy trước, reviewer xác minh
  các SHA/ref bất biến bằng đọc.
- Không thử REST/GitHub/`gh`; giao việc chỉ định đường tệp.
- Không đọc/ghi/xóa auth thật; mọi probe dùng HOME tạm. Không in giá trị biến môi trường.
- Fixture và mutation chỉ ở `/tmp`; không sửa tệp kho, commit, push, merge, land/deploy.

