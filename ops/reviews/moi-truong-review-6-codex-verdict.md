# CROSS-REVIEW lượt 6 — codex

Verdict: **changes_requested**

Mỏ neo: `c775c0a5b0bf0816e913ba0b300d898fec3c58b0` (base `fe895a068368754bd11b25ca59c504f973e9f086`).

## Findings

### [P1] Chốt trưởng nhóm vẫn fail-open khi không đo được PGID

`.claude/dev/launcher.py:730-754` biến mọi `OSError` từ `getpgid(pid)` thành `None`, rồi vẫn gọi `killpg(pid, ...)`. Như vậy chính ca nguy hiểm nhất — tiến trình vừa chết, PID/PGID đang đổi, `/proc` hoặc syscall không đo được — lại bỏ qua chốt duy nhất chứng minh số PID đang cầm thật sự là process-group ID. `t92` còn ghim hành vi này thành kỳ vọng (`launcher_test.py:2460-2467`), nên test bảo vệ đường fail-open thay vì cấm nó.

Đây không chỉ là suy luận. Với `HOME` tạm, lần chạy suite chuẩn tự khai `pid=5 pgid=1 sid=1`, `chung_nhom_voi_cha=True`, sau đó báo đã `setsid` sang `pgid=5`, nhưng dừng ngay sau dòng bỏ qua `t62`; không có tổng kết và câu lệnh shell kế tiếp không chạy. Triệu chứng giết caller vẫn tái hiện ở đúng HEAD này. Cần không gọi `killpg` khi chưa có bằng chứng đích là nhóm dự kiến; nếu leader đã chết nhưng còn hậu duệ thì phải chứng minh nhóm/cây từ ảnh chụp và khóa danh tính, không suy `pid == pgid` từ việc `getpgid` thất bại. Race giữa lần kiểm khóa danh tính, `getpgid`, ảnh chụp và `killpg` cũng cần được mô hình hóa; chốt hiện tại không loại nó.

`setsid` ở `fe895a0` vì thế chưa thừa: nó vẫn bảo vệ chính runner khi thành công. Nhưng nó không sửa được việc `_giet_cay` nhắm một số chưa được chứng minh là PGID, và bản thân suite vừa cho thấy lớp bảo vệ đó chưa đủ.

### [P1] `CO_CREDENTIAL` vẫn được doctor đối xử như khả dụng

`_do_codex` trả `CO_CREDENTIAL` khi chưa `--kiem-song` (`launcher.py:1882-1884`), nhưng `lenh_doctor` chỉ đưa `CHUA_XAC_THUC` và `CAN_CHUAN_BI` vào `chua_xac_thuc` (`launcher.py:2122-2131`). Hệ quả: một Codex có `login status` rc=0 nhưng token đã bị thu hồi và không đo được là hết hạn vẫn cho `ok_kha_dung=true`, không xuất hiện trong `chua_xac_thuc`, và có thể trả mã 0 kể cả đường `--doi-kha-dung` (`launcher.py:2134-2147`). Đây chính là nâng nhãn ở tầng tiêu thụ dù tầng đo đã đổi tên đúng. Cần cho `CO_CREDENTIAL` là trạng thái chưa chứng minh khả dụng trong phép tính gate, hoặc tách rõ “không biết” khỏi “dùng được” và để `--doi-kha-dung` fail-closed.

Việc đổi kỳ vọng `t85` từ `DUNG_DUOC` sang `CO_CREDENTIAL` là đúng với hợp đồng mới ở cấp `_do_codex`, và việc ghim `_han_token_codex` tránh đọc credential thật là đúng. Thiếu sót nằm ở test tích hợp của doctor: không có ca khóa `ok_kha_dung`/mã thoát khi nhận nhãn mới.

### [P1] Cổng đột biến đỏ ổn định sau khi đổi hợp đồng t85

Cả hai lần `python3 .claude/dev/launcher_test.py --dot-bien` đều trả rc=1 và cùng kết quả `49/50 dat` (một mục không đo được). Đột biến `do_codex_tin_DONG_DAU_thay_vi_ma_thoat` sống sót: `SAI, giet 0/1`. Nguyên nhân trực tiếp là mutation chỉ dựng lại lỗi đọc dòng đầu, còn `t85(c)` nay đòi `CO_CREDENTIAL`; đường mutated vẫn trả đúng nhãn đó, nên ca không chết. Cần cập nhật mutation/ca đích theo hợp đồng mới hoặc tách ca rc/dòng đầu khỏi ca nhãn, để cổng tự đột biến xanh thật.

### [P2] Bản khai nuốt cả tín hiệu điều khiển tiến trình

`launcher_test.py:1960-1964` bắt `BaseException`, nên `KeyboardInterrupt` và `SystemExit` trong bất kỳ probe nào bị đổi thành `None` rồi runner tiếp tục tới các ca có `killpg`. Chẩn đoán không nên biến yêu cầu dừng thành “không đo được”; bắt `Exception` là đủ cho lỗi probe thông thường. Các trường đang khai không chứa giá trị biến môi trường/token; PID, PGID, namespace inode và tên PID 1 là metadata chẩn đoán hợp lý, không thấy rò bí mật trực tiếp.

## Credential/JWT/live check

`_han_token_codex` không xác thực chữ ký nên `exp` chỉ là lời khai không tin cậy. Dùng nó để hạ nhãn khi hết hạn là heuristic fail-closed, nhưng không được coi JWT tương lai là bằng chứng dùng được; finding doctor ở trên hiện làm đúng điều nguy hiểm đó theo đường gián tiếp. Không thấy giá trị token bị in; chỉ tên token, số giờ và `last_refresh` được in. `_do_codex_song` chạy `codex exec` thật, có thể tốn quota, tạo log/session, refresh `auth.json`, và theo chính sách sandbox của Codex có khả năng ghi workspace nếu agent làm khác prompt. Vì chỉ chạy khi người dùng yêu cầu `--kiem-song`, tác dụng phụ được opt-in, nhưng nên chạy trong cwd/HOME tạm hoặc sandbox chỉ-đọc nếu mục tiêu chỉ là auth probe. Tôi không chạy live check và không đụng credential thật.

## Bản khai môi trường reviewer

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

## Xác minh

- Bước 0: `false`; `core.abbrev=7`; HEAD đúng SHA; diff đúng `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`.
- Suite chuẩn với `HOME=$(mktemp -d)`: không hoàn tất; caller bị ngắt sau `t62`, không có dòng tổng kết/RC.
- `--dot-bien` lần 1: rc=1, `49/50 dat`, một mutation không đo được, mutation t85 sống.
- `--dot-bien` lần 2: rc=1, kết quả giống hệt.
- Không chạy `--kiem-song`; không đọc/sửa `~/.codex/auth.json` thật.
- `git status --porcelain` được kiểm tra cuối và sạch.

