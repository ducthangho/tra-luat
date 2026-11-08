# Review Codex offline lượt 1: packet #1272 HOTFIX-R1252-POSIX r1 (Review Class: standard)

Bạn là reviewer độc lập (họ OpenAI). Lượt này CHỈ ĐỌC trên thư mục làm việc. **KHÔNG ghi bất kỳ tệp nào trong thư mục làm việc** (kể cả tệp ignored, `__pycache__`, `.git/**`, `git config`). Lượt chạy bằng `launcher.py run --chup-workspace`; một lần ghi vào cây là lượt vô hiệu. Gốc workspace có sẵn `.aws/` và `.codex/` rỗng — đừng xoá.

**Bước đầu tiên:** `git clone --no-hardlinks <thư mục làm việc> /tmp/rvh1272-copy`, `git config core.abbrev 7` trong bản sao; mọi lệnh chạy TRONG bản sao, `TMPDIR` ngoài cả hai cây.

## Neo
- HEAD phải là `fc6fbc7c07351ea75ece6a0a25a96262225bef03`; base `efebadf83409a81e42e6c97f1b7255ede76110f5` (master). Khác ⇒ `request_changes`.
- Spec: `ops/specs/hotfix-r1252-posix-r1.md` trên nhánh `ops/hotfix-r1252-posix-lease` (KHÔNG có trong cây này), sha256 `4133641145d1a595439aab30dd02f2d991f211258d9cd274917f3ff8a946e65b`. Tóm tắt: thêm phần tử thứ 4 `("posix", lý do)` cho mục `DOT_BIEN` `r1252_ghi_de_dich_truc_tiep` trong `.claude/dev/launcher_test.py`; diff đúng 1 tệp, ≤15 dòng thêm, ≤5 xoá; không đổi `launcher.py`, không đổi mục đột biến khác; Linux đột biến vẫn bị giết.
- PR #1277 đã push trước lượt này (connector sạch, CI 24 xanh). Lượt này là review trên đúng SHA đã push.

## Bối cảnh đo
`launcher-windows.yml` trên master đỏ đúng 1 đột biến `r1252_ghi_de_dich_truc_tiep SAI giet 0/1` (run 42360967762, 42398808503). Đột biến sửa `os.replace(..., src_dir_fd=dfd, dst_dir_fd=dfd)` trong nhánh `if _CO_DIR_FD:` của `_ghi_tep_0600`. Đo trên Windows thật (Python 3.12.10): `_CO_DIR_FD = False`, ca đích qua, đột biến tái hiện `SAI giet 0/1`. Bước Windows có nhãn posix CHƯA đo (chỉ mô phỏng Linux `LA_WINDOWS=True`).

## Việc
1. Đọc diff `efebadf..fc6fbc7`. Xác minh: đúng một tệp/một mục; nhãn dùng đúng cơ chế `muc[3]` của `chay_dot_bien` (`(nen == "posix") == LA_WINDOWS` ⇒ bỏ qua trên Windows); nhánh dir_fd thật sự không chạy khi `_CO_DIR_FD` False (đọc `_ghi_tep_0600`, `_CO_DIR_FD`).
2. Chạy tập trung ĐÚNG MỘT đột biến trên Linux: nạp `launcher_test.py` bằng importlib, đặt `DOT_BIEN` chỉ còn mục ấy, `DOT_BIEN_HOOK = []`, `DOT_BIEN_HARNESS = []` (BẮT BUỘC cả ba — `chay_dot_bien` chạy cả hai bảng phụ), gọi `chay_dot_bien()`; xác nhận số dòng kết quả = 1 và `OK giet 1/1`. Rồi lặp lại với `LA_WINDOWS = True` ⇒ phải `KHONG DO DUOC tren nen nay`.
3. Xét: nhãn posix có che mất phép đo nào có ý nghĩa trên Windows không (tức có đường Windows nào chạy dòng bị đột biến)? Có đột biến nào khác của `r1252_*` cùng tình trạng mà chưa được nhãn (đọc log CI master: chỉ một SAI)?
4. `python .claude/dev/launcher_test.py` (Linux) N/N trùng nền (2 ca bỏ qua như nền); ruff F delta 0.
Không tự viết script tấn công/symlink/race mới.

## Đầu ra
Phát hiện P0–P3 kèm lệnh tái hiện; khai lệnh nào chạy ở bản sao nào. Dòng CUỐI stdout đúng một dòng: `KET_LUAN: approve` nếu không còn P0/P1/P2, ngược lại `KET_LUAN: request_changes`.
