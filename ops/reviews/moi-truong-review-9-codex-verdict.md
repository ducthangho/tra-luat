# CROSS-REVIEW lượt 9 — codex

- Verdict: **changes_requested**
- Head bất biến: `1df800be15580d7432a1200900dd04ed9a7b997c`
- Base: `3f8b2904cfb4f99aab151cd0be435e4ba4553bb8`
- Phạm vi: chỉ đọc; không sửa/commit/push/merge/land/deploy cây kho.

## Findings

### HIGH — cờ `CHAN-CODEX` không chặn đường chạy Codex, chỉ làm đỏ phép đo `doctor`

`.claude/dev/launcher.py:1961-1977` chỉ đọc cờ bên trong `_do_codex`. Nhưng chính hook gọi thẳng `codex login status` tại `.claude/hooks/session-start.sh:168` và `:202`, trước khi bộ gỡ chạy ở `:238-249`; các lệnh này không đi qua `_do_codex` và không đọc cờ. Một lệnh `codex` người dùng chạy trực tiếp cũng không có chốt nào đọc cờ. Vì hook tiếp tục phiên khi rc khác 0, `doctor --doi-kha-dung` có thể từ chối một workflow dùng launcher, nhưng đường nguy hiểm vẫn chạy được. Tuyên bố “CODEX BI CHAN”/fail-close vì thế không đúng.

Ít nhất hook phải xử lý policy trước mọi lời gọi Codex và mọi entry point do kho cung cấp phải dùng chung guard; nếu mục tiêu thật sự là chặn executable Codex trong cả phiên thì một sentinel chỉ được `doctor` đọc không thể thực thi hợp đồng đó. `t102` hiện chỉ chứng minh `_do_codex` đọc cờ, nên xanh giả đối với phạm vi “chặn codex”.

### HIGH — suite vẫn giết caller; lần đo này chết bên trong `t72`, không tới `atexit`

Probe đúng mẫu đề bài, với HOME/nhật ký/marker đều ở `mktemp`, tái hiện hai lần việc shell bị giết. Lần có đường dẫn bền ghi:

- nhật ký `vao=74`, `ra=73`;
- dòng cuối là `>>> vao 73 t72_bi_ngat_KHONG_duoc_ghi_thanh_xong`;
- không có `# XONG TRON VEN`;
- không in `ATEXIT CHAY XONG`;
- marker chỉ có `truoc`, không có `rc=...` hay `sau`;
- phiên đọc độc lập sau đó không thấy tiến trình suite/con còn sống.

Kết quả này khác phép đo lượt 8 (`100/100`, `XONG TRON VEN`, rồi shell chết): lỗi có tính không ổn định hoặc phụ thuộc thứ tự/môi trường. Bằng chứng lượt này đặt điểm chết trong `t72`; tôi không suy đoán nguyên nhân.

### MEDIUM — `_DONG_HOP_LE` vẫn xóa dữ liệu của khối đã bị sửa tay

`.claude/dev/codex_env_policy.py:65-72,121-135` kiểm từng dòng độc lập, không kiểm cấu trúc, thứ tự hay đúng giá trị khối cũ. Phản chứng chạy được: giữa hai marker dòng-riêng, cả ba phần giữa sau đều được nhận và bị xóa với lý do `da go khoi cua ta`:

```text
[shell_environment_policy]
inherit = "core"
```

```text
# ghi chu cua nguoi dung
```

```text
inherit = "all"
[shell_environment_policy]
```

Điều này trái tuyên bố “toàn bộ hình dạng khối cũ, không hơn” và “người dùng sửa giữa khối ⇒ từ chối”. Cần xác thực grammar/trình tự hoàn chỉnh của đúng khối cũ (hoặc so khối canonical), không phải membership từng dòng. Phép xóa tối đa một dòng trắng sau marker là hợp lý đối với writer cũ: nếu phần người dùng vốn bắt đầu bằng dòng trắng thì writer tạo hai dòng và bộ gỡ chỉ lấy lại một.

### MEDIUM — writer “nguyên tử” theo symlink của tên tạm đoán được và ghi đè tệp khác

`.claude/dev/codex_env_policy.py:150-157` dùng tên `config.toml.tra-luat-tam-<pid>` rồi `open(..., "w")`, không tạo độc quyền và không chống symlink. Phản chứng trong `TemporaryDirectory`: đặt tên tạm đó là symlink tới tệp `victim` chứa `DO NOT TOUCH`, gọi `ghi_nguyen_tu(config, "new")`; kết quả cả `victim` lẫn config đều thành `new`. Như vậy lỗi xảy ra trước `os.replace`, phá đúng hợp đồng “hỏng trước replace thì bản gốc/ngoài đích không bị đụng”. Dùng `tempfile.mkstemp`/`O_CREAT|O_EXCL` cùng thư mục và chống theo symlink; cân nhắc fsync thư mục sau replace nếu cần độ bền qua mất điện.

`os.replace` thay chính symlink config chứ không cập nhật target, đồng thời tệp mới có owner của process và mode 0600. Mode 0600 là mặc định an toàn hợp lý cho config Codex, nhưng đây là thay đổi metadata có chủ ý và nên được kiểm/test nếu hỗ trợ config symlink hoặc owner khác.

### LOW — `argparse` vẫn nhận cờ lặp dù bản khai nói đã từ chối

`.claude/dev/launcher_test.py:3688` khai “cờ lặp/cờ lạ không bị từ chối” là lỗi đã sửa, nhưng parser tại `:3694-3708` và `t101` không khóa cờ lặp. Phản chứng:

- `--dot-bien --dot-bien` được nhận;
- `--moi-truong --moi-truong` được nhận;
- `--nhat-ky /tmp/a --nhat-ky /tmp/b` được nhận và âm thầm lấy `/tmp/b`.

Bốn tổ hợp hợp lệ đã khóa là đủ; các tổ hợp lặp trên là phần còn thiếu nếu hợp đồng vẫn yêu cầu từ chối lặp.

## Các kiểm chứng khác

- Bước 0 khớp: non-shallow=`false`, `core.abbrev=7`, HEAD đúng SHA, đúng 6 tệp delta.
- Fixture: toàn tệp 45→34 dòng; bỏ 8 dòng chú thích ẩn danh thì snapshot đúng **37→26**. Kích thước 1407→1010 byte, gỡ 397 byte; dry-run không ghi fixture.
- Marker nằm giữa dòng bị từ chối; hai lớp marker-dòng và kiểm phần giữa đều có tác dụng, nhưng lớp phần giữa quá rộng như finding trên.
- Cờ tự hết ở các nhánh “không có config”/“config không có marker”/gỡ thành công. Không thấy ca hết oan trong phạm vi marker canonical ngoài việc validator nhận oan khối đã sửa.
- Hai lượt `--dot-bien`: cùng `57/57 dat`, mỗi lượt `1 khong do duoc tren nen nay` (`124_khi_chau_con_song`, t62 Windows).
- Bản khai: Linux; Python 3.11.15; pid 4, ppid 2, pgid/sid 1; không là trưởng nhóm, chung nhóm với cha; không TTY; PID namespace `pid:[4026532315]`; init cùng namespace; 4 CPU.
- Không in giá trị biến môi trường/token; không đọc hay sửa config/auth thật.

## Kết luận

`changes_requested`. Lý do chặn chính là fail-close chưa thực sự chặn Codex và suite vẫn giết caller; các đường mất dữ liệu còn lại cũng cần sửa trước khi approve.
