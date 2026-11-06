# Hiện vật đo S5, S6 của đặc tả `launcher-readonly-ignored-r1.md`

Đo 06-11-2026 khoảng 06:15–06:18Z, trong container Claude Code remote (`env.txt`: git, python, kernel).

Kho đo: clone mới `https://github.com/ducthangho/tra-luat.git`, checkout `12e5b36225005e257026e57903f2e859a870e6f9`.
Không đặt cấu hình git nào ngoài mặc định của clone.

- S5: `python3 do_s5.py <kho>`, chạy hai lần liền ⇒ `s5-out.txt`, rc 0. Bộ đệm trang của hệ điều hành đã ấm
  (lần đọc thứ hai của cùng cây), nên đây là chi phí ẤM, không phải chi phí lạnh.
- S6: `git clone <kho> <kho6b>`, `git -C <kho6b> checkout 12e5b36`, `sleep 2`, rồi `bash do_s6.sh <kho6b>`
  ⇒ `s6-out.txt`. Mỗi dòng in rc của lệnh và 16 ký tự đầu sha256 của `.git/index` SAU lệnh đó.

`SHA256SUMS` băm các tệp trong thư mục này.
