# Audit launcher vòng 4 — POSIX

Ngày đo: 2026-08-13, Linux/Python 3.11.15. Chỉ kết luận những gì đã chạy
trên Linux; không suy diễn cho Windows.

## CHẶN

### Wrapper thoát làm launcher xoá prompt trước khi cháu đọc

Phản chứng mới `t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau` chạy một
wrapper sinh cháu cùng nhóm, cháu đợi 0,4 giây rồi mới mở
`{PROMPT_FILE}`. Hành vi trước bản vá: wrapper rc=0, launcher xoá
snapshot, cháu nhận `FileNotFoundError`; sổ vẫn có thể ghi `xong`.

Lệnh đo sau bản vá:

```text
python3 .claude/dev/launcher_test.py
76/76 ca (qua 74, bo qua 2, hong 0)
```

Đột biến khôi phục đúng hành vi xoá sớm:

```text
xoa_prompt_khi_wrapper_vua_thoat OK  giet 1/1:
t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau
```

## ĐÃ VÁ

`lenh_run` chỉ xoá snapshot mặc định khi `_thanh_vien_nhom(p.pid) == []`,
tức đã có bằng chứng dương nhóm POSIX rỗng. Còn hậu duệ hoặc
không đo được thì giữ tệp 0600. Việc này ưu tiên không làm
hỏng lần đọc prompt đang diễn ra; snapshot giữ lại có thể được dọn
thủ công hoặc bằng cơ chế thu gom sau này.

## KHÔNG VÁ ĐƯỢC TRÊN MÁY NÀY

- Windows thật: `taskkill`, PowerShell `StartTime.Ticks`, cp1258 và fixture t62.
- Darwin: `ps` không cung cấp khoá starttime trong ảnh `_chup_cay`; khoá rỗng
  khiến `_con_song_dung_khoa` chỉ xác minh PID còn sống, không chống PID
  tái dùng. Cần máy Darwin thật để chọn và đo nguồn khoá thích hợp.
- Khe cháu sinh sau ảnh chụp rồi `setsid()` ngay vẫn không thể phủ
  hoàn toàn bằng quét `/proc`. `PR_SET_CHILD_SUBREAPER` chỉ giữ quan hệ
  reparent/cho phép reap, không tự nó chặn thoát nhóm; cgroup v2 có thể
  liệt kê/kill trọn cgroup nhưng cần quyền và vòng đời cgroup riêng.

## GHI NHẬN

- Baseline trước sửa: doctor rc=0; `75/75` (73 qua, 2 bỏ qua, 0 hỏng);
  đột biến `32/32` (1 không đo được); worktree sạch.
- `_tim_luot` với 1.200 sổ, tìm run_id đầy đủ ở sổ cuối:
  `STATUS_FULL runs=1200 elapsed=0.094807s rc=0`.
- 300 tiến trình, 20 cặp quét `_chup_cay` + `_thanh_vien_nhom`:
  `PROC_SCAN processes=300 pairs=20 elapsed=0.196737s` (~9,8 ms/cặp).
  Đường chờ 2 giây quét nhóm mỗi 0,1 giây vì thế thêm chi phí
  cỡ hàng trăm ms trong fixture này, không phải nhiều giây.
- `pip install --dry-run --quiet -r requirements.txt`: rc=0, 0,982s.
  Thêm `--no-index`: rc=0, 0,901s. Ca hiện tại đã đủ gói nên không
  chứng minh đường thiếu gói có cần mạng; pip mặc định vẫn được
  phép hỏi index và hook không đặt timeout riêng.
- Mốc `.git/.tl_reqs_*` không làm bẩn `git status`; `git clean -x`
  không nhắm tới nội dung trong `.git`. Xoá mốc chỉ làm hook chạy pip
  lại và tạo lại mốc sau khi cài thành công.
- Grep `.claude/`, `docs/`, CHANGELOG chỉ thấy `{sid}-{rid}` trong tài liệu
  lịch sử, test và đột biến; không thấy consumer hiện hành phụ thuộc
  tên cũ. `_cap_id` tối đa 64 lần, không thể treo vô hạn; với
  1.000 short-id 32-bit, xác suất một lần bốc va chạm xấp xỉ
  `1000 / 2^32` (~2,3e-7), còn 64 lần liên tiếp là không đáng kể.
- Các `print()` còn lại ở check/run/stop được `main` bắt
  `BrokenPipeError`; nếu kết luận chưa in xong thì trả 141. status/doctor
  dùng `_in_an_toan` và giữ mã kết luận đã tính.
- Mã con có thể trùng mã launcher; `run.json.trang_thai` là phân biệt
  chính xác. `run` không có deadline mà bị tác nhân ngoài giết sẽ ghi
  `xong` với mã âm của signal (và CLI chuẩn hoá thành 1), chứ chưa có
  nhãn riêng cho “bị giết bởi bên ngoài”.

Cổng cuối sau bản vá: `76/76` ca, `33/33` đột biến, hỏng 0;
`ruff --select F` sạch.
