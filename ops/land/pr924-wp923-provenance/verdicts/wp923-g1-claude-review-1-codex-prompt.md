# Cross-review wp923 r1 (Issue #923, PR #924) — lớp `sensitive`, reviewer codex

Bạn là REVIEWER độc lập. Read-only với mã đã đưa review: KHÔNG commit, KHÔNG push, KHÔNG sửa tệp trong
`cay-kho/` ngoài các bản sao tạm do bạn tự dựng (ví dụ `mktemp -d -p .` để đột biến).

## Thứ định danh
- Thứ định danh là BĂM, không phải tên nhánh. `head` đưa review = `7574c39` (`cay-kho/` đã checkout sẵn);
  base = `1a269f5` (có trong `cay-kho`, `git -C cay-kho show 1a269f5:…`).
- Đặc tả đóng băng: `SPEC.md` trong thư mục này, sha256 phải là
  `65db5e381ce9c7539f5bf9fb3b7d116ba3822a4914f3725e7a9ba98a484e4513` — tự băm lại.
- `diff.patch` = `git diff 1a269f5 7574c39` (2 tệp). Bạn có thể tự dựng lại từ `cay-kho`.
- PowerShell 7.4.6 thật: `./pwsh/pwsh` (Linux x64) trong thư mục này.

## Việc
1. Đọc `SPEC.md`. Đối chiếu diff với write set và với từng mục N1–N4 (N5/N6 phiên điều phối đo, xem dưới).
2. ĐO, đừng tin lời khai của executor dưới đây:
   - N1: `yaml.safe_load` của `.github/workflows/ci.yml` base == head.
   - N2: mọi dòng `-`/`+` của diff `ci.yml` là chú thích.
   - N4: chạy `.claude/dev/chay-cong-windows_test.ps1` bằng `./pwsh/pwsh -NoProfile -File` trên một clone SẠCH
     của head (và của base nếu thời gian cho phép), xem `t9`. Đột biến mặc định về `8999` trên bản sao ⇒ `t9` phải ĐỎ.
     Bộ test có thể chạy vài chục phút; nếu không chạy trọn được, ghi `KHÔNG ĐO ĐƯỢC` thay vì suy.
3. Rà NGỮ NGHĨA của chú thích: (a) có câu nào trong `ci.yml` còn khẳng định `timeout-minutes` HIỆN TẠI của một
   job mà sai trên head không (executor có thể bỏ sót); (b) câu mới thêm có đúng sự thật lịch sử không — kiểm bằng
   `git log -G'timeout-minutes' -- .github/workflows/ci.yml` và `git show` các commit #910 (`6e09f4b`, `a7da463`);
   (c) câu lịch sử có mốc có bị viết lại trái đặc tả không; (d) chú thích `.PARAMETER HanGiay` mới có đúng không.
4. Danh sách câu executor phân loại "lịch sử / không chắc, để handoff, KHÔNG sửa": `ci.yml` dòng 118–119
   (r391 "Nâng tiếp 45 -> 60 … Trần 60 là chỗ trống …") và 1028–1029 (WP856 "60 -> 120"; job nay 150, không có
   câu mốc #910 riêng). Bạn đồng ý hay không, kèm lý do.

## Lời khai của executor (để bạn BÁC, không để tin)
- N1 True; hằng `BAM_GATE_NHANH`/`BAM_GATE_REGISTRY` khớp trên head. N2: 5 dòng (2 `-`, 3 `+`), toàn chú thích.
- N3 actionlint 1.7.7 rc=0 cả hai vế, `shellcheck` vắng.
- N6 `ci_dang_ky_test.py` (không `--chay`) trên head: `TỔNG: ĐẠT`, `PHẢN CHỨNG: 1070/1070`.
- N4: xem `EVIDENCE.md` nếu có trong thư mục này khi bạn đọc; nếu chưa có thì tự đo.

## Đầu ra
Ghi TĂNG DẦN vào `VERDICT.md` trong thư mục này (ghi ngay khi có mỗi phát hiện, đừng đợi cuối lượt):
- dòng đầu: `verdict: approve` hoặc `verdict: request_changes`, kèm `reviewed_sha: 7574c39…` (40 ký tự, tự lấy).
- từng finding: mức `P0`–`P3`, tệp:dòng, đường tái hiện (lệnh + output), đề xuất.
- mục "Đã đo": lệnh + kết quả cho N1/N2/N4 và đột biến 8999.
- mục "KHÔNG ĐO ĐƯỢC" nếu có.
