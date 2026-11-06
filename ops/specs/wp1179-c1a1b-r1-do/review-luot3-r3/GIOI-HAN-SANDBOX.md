# Giới hạn sandbox của lượt 3 (run `f2172e8b`)

`run.json` ghi `sandbox_trang_thai: KHONG_DO_DUOC`. Lý do launcher ghi nguyên văn:
`sandbox_ly_do: "argv tien trinh sandbox khong phan tich duoc theo bang so doi so"`.

Phân tích mẫu `/proc` mà launcher lấy, mỗi 0,2 s, trong `sandbox_quan_sat`:
- Đúng **1** mẫu `bwrap` mang `khong_ro: true`.
- Các mẫu còn lại đều thấy cơ chế sandbox:
  - `codex-linux-sandbox` với profile `file_system: restricted`, `network: restricted`;
  - `bwrap` với `--unshare-net`, `--unshare-pid`, `--unshare-user`, `--cap-drop=ALL` và `--ro-bind /`.
- `sandbox_lech`: mọi bộ đếm bằng 0.

Theo luật của launcher, một mẫu không phân tích được làm cả lượt ra `KHONG_DO_DUOC`. Lượt này vì vậy **không** được
khai là "sandbox đã đo". Lượt 2 (`daedf180`) có cùng cơ chế và ra `DO_DUOC`.

Lượt 1–3 chạy với `--add-dir` trỏ vào thư mục chứa cả mirror đang review. Mirror vì thế được phép ghi về mặt kỹ thuật.
Read-only của mirror ở ba lượt ấy chỉ dựa trên hai thứ:
- chỉ thị trong prompt;
- phép đo sau lượt: `git status --porcelain --ignored` rỗng, và ở lượt 3 thêm manifest sha256 12.741 tệp đầu/cuối,
  delta 0 (`evidence/final-r3.txt`).

Đó là bằng chứng "không thấy delta ở hai mốc". Nó không phải sandbox cưỡng chế. Từ lượt 4, `--add-dir` được bỏ.
