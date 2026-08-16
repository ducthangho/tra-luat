# CROSS-REVIEW lượt 8 — verdict của codex

- Verdict: **changes_requested**
- Revision được review: `3f8b2904cfb4f99aab151cd0be435e4ba4553bb8`
- Base: `69bc3cede6085bf6229ac95a44da4aae9e51ee42`
- Reviewer: `codex`; người vá: `claude`; đây không phải wp55.

## Findings

### HIGH — suite vẫn giết caller sau khi toàn bộ 100 ca đã ra

Phép đo sống sót lần này định vị được giới hạn mà các lượt trước không có. Nhật ký còn nguyên 100 dòng `>>> vao`, 100 dòng `<<< ra`, không có ca thiếu `ra`, và kết thúc bằng `# XONG TRON VEN`. Ca cuối là `t97_nap_ban_sao_khong_duoc_an_phai_BYTECODE_CU`, cũng có `ra -> qua`. Tuy nhiên shell gọi chết trước cả `echo "rc=$?"`; thử bọc thêm `setsid -w` vẫn có cùng triệu chứng.

Vì vậy không có “ca giết” trong vòng lặp. Cú chết nằm sau `NhatKyCa.dong()`/sau khi `main` đã chạy hết, tức vùng thoát, cleanup, `atexit`, hoặc hành vi tiến trình còn sót. Finding HIGH số 1 của lượt trước chưa đóng; theo tôi phải đóng nó trước khi approve vì chính test gate vẫn có thể giết caller/runner.

### HIGH — thu hồi policy đang fail-open đúng lúc phát hiện config nguy hiểm nhưng không thể gỡ an toàn

[`session-start.sh`](../clone-env8/.claude/hooks/session-start.sh) bắt rc=3 của bộ gỡ, chỉ in `CANH BAO`, rồi tiếp tục (`3f8b290`, dòng 228–234). Khi đó khối `inherit = "all"` cũ vẫn còn hiệu lực và phiên codex sau hook vẫn có thể đưa toàn bộ môi trường cho lệnh con. Đây chính là trạng thái bảo mật mà commit nói đang thu hồi; cảnh báo không thực hiện việc thu hồi.

Hook không nhất thiết phải khóa toàn bộ phiên, nhưng ít nhất phải fail-close cho đường dùng codex (hoặc cô lập/disable codex cho tới khi sửa tay). Tiếp tục như hiện tại biến một lỗi xác định-an-toàn thành phơi môi trường có chủ ý.

### MEDIUM — `go_khoi` xóa theo substring, chưa chứng minh đó là khối do hook sở hữu

[`codex_env_policy.py`](../clone-env8/.claude/dev/codex_env_policy.py) dùng `str.count/index` ở dòng 62–74. Một cặp chuỗi marker xuất hiện bên trong TOML multiline string vẫn được coi là marker thật và phần giữa bị xóa. Một comment người dùng chứa đúng text marker nhưng có tiền tố trên cùng dòng cũng bị nhận; phản chứng `x=1 # <MOC_MO> ... # <MOC_DONG>` bị biến thành `x=1 #\nz=3\n`, làm mất `y=2`. Cả hai đầu ra vẫn parse TOML nên parse lại không phát hiện mất dữ liệu.

`t100` chỉ phủ marker đứng riêng đúng mẫu, thiếu một đầu, và hai khối nguyên vẹn. Nó chưa phủ marker không phải dòng riêng, marker trong basic/multiline string, hay nội dung khối không đúng schema cũ. Cần nhận đúng marker full-line và xác thực phần giữa là đúng khối legacy dự kiến; trường hợp mơ hồ phải rc=3, không ghi.

### MEDIUM — đường ghi không nguyên tử có thể trả rc=3 sau khi đã làm hỏng tệp

Dòng 109 gọi `Path.write_text` trực tiếp lên config. Nếu truncate/ghi được một phần rồi gặp `OSError`, nhánh catch trả `MA_TU_CHOI` nhưng tệp đã bị cắt. Điều này vi phạm hợp đồng “gỡ đúng hoặc từ chối không đụng tệp”. Nên ghi tệp tạm cùng thư mục, flush/fsync, giữ mode phù hợp rồi `os.replace`; test bằng writer giả ghi một phần rồi ném lỗi.

### LOW — parser `--nhat-ky` có các tổ hợp im lặng nuốt/hoãn lỗi

Parser tay ở `launcher_test.py` dòng 3491–3517 xử lý mode trước khi xử lý đối số nhật ký:

- `--nhat-ky` thiếu path vẫn chạy toàn bộ suite rồi mới rc=2;
- `--nhat-ky --dot-bien` chạy mutation 56/56, rc=0 và không tạo nhật ký (`--dot-bien` bị dùng như path về mặt cú pháp nhưng nhánh mutation thắng trước);
- `--moi-truong` bỏ qua `--nhat-ky`, path và đối số rác, rc=0;
- duplicate/unknown options không bị từ chối.

Lệnh chuẩn trong prompt hoạt động, nên đây không làm sai phép đo lượt này, nhưng làm công cụ chẩn đoán dễ xanh giả. Dùng `argparse` với các mode loại trừ nhau và parse trước mọi công việc.

## Đánh giá các câu hỏi cụ thể

- Không còn đường thực thi nào trong delta ghi lại `inherit = "all"`. `rg` chỉ thấy fixture `t100` và các nhắc lịch sử/tài liệu có nhãn “đã thu hồi”.
- Tài liệu chính đã sửa nhất quán, không còn chỉ dẫn dựng lại; snippet còn lại được gắn rõ “ĐÃ THU HỒI”.
- Khả năng codex vẫn chạy nhờ `codex login --device-auth` chỉ là lập luận/tài liệu trong snapshot, chưa phải phép đo live ở review này. Tôi không dùng credential thật và không chạm `~/.codex/auth.json` hay `~/.codex/config.toml`.
- Không thể đo tuyên bố config thật `37→26`, 9 bảng `[projects]` vì không có bản sao fixture được cung cấp ngoài config thật, trong khi prompt cấm đụng config thật. Trên fixture tạm, gỡ chuẩn parse lại được và lần hai no-op; nhưng `strip("\n")` dòng 76 xóa toàn bộ blank-line đầu/cuối của người dùng, không chỉ whitespace do gỡ tạo ra. TOML vẫn hợp lệ nhưng không bảo toàn byte.
- `t99` có răng cho việc ghi `>>> vao` trước khi ca chạy và cho kết quả `ra`/dấu hoàn tất. Nó không có răng riêng cho `fsync`: bỏ `os.fsync` vẫn cho ca tự đọc thấy dữ liệu qua page cache. Source hiện thực sự gọi `flush` + `fsync` cho mỗi record.
- Microbenchmark 100 no-op, 5 lượt: không nhật ký trung bình 0.0258 s; có nhật ký 0.0714 s, tăng khoảng 45.6 ms/100 ca trong filesystem này. Mức này nhỏ so với suite khoảng 30 s, nhưng độ trễ `fsync` phụ thuộc storage nên không thể suy rộng tuyệt đối.

## Bằng chứng chạy

### Bước 0

- `git rev-parse --is-shallow-repository` → `false`
- `git config --get core.abbrev` → `7`
- `git rev-parse HEAD` → `3f8b2904cfb4f99aab151cd0be435e4ba4553bb8`
- Diff base→HEAD đúng 5 tệp được yêu cầu: 1 `A`, 4 `M`.

### Bản khai môi trường

```json
{
  "he_dieu_hanh": "Linux",
  "python": "3.11.15",
  "pid": 2,
  "ppid": 1,
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

### Kết quả

- Suite + `--nhat-ky`: nhật ký `vao=100 | ra=100 | CA GIET=khong co`; `tron ven=True`; shell caller vẫn chết sau đó, không thu được rc.
- `--dot-bien` lượt 1: `56/56 dat (1 khong do duoc tren nen nay)`, rc=0.
- `--dot-bien` lượt 2: `56/56 dat (1 khong do duoc tren nen nay)`, rc=0.
- Mọi HOME/fixture/policy test đều dùng đường dẫn tạm; không đọc hay ghi credential/config thật.
- Kiểm tra cuối: `git status --porcelain` rỗng; cây kho sạch.

