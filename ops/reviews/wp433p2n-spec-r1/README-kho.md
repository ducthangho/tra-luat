# Review đặc tả #433 nợ (`GWS-CRED-DICH-NGOAI-KHO-N` r1)

- Bản cuối: `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r1.md`, sha256 `fa48e0769605cc3bfa7b80aa3938cb95814b29bc6a146613ea93b17fbd9a5fa1`.
- Codex lượt 5/10 `approve` trên `rv/dac-ta-luot5.md` (sha256 `a993c6d6…`), một P3. P3 ấy được đóng bằng sửa đặc tả SAU approve
  (`os.getcwd()` chỉ gọi cho đường tương đối; N2 thêm `W6.thuong_cwd_mat`), KHÔNG chiếu lại; khác biệt: `rv/sau-luot5.diff`.
- `rv/`: lượt 1–5 (`dac-ta-luotN.md`, `prompt-luotN.md`, `luotN.stdout.txt`, `luotN.verdict.txt`). Không chép `*.stderr.txt` (bản ghi phiên Codex), theo tiền lệ R.
- `nguyen-mau/`: nguyên mẫu M2–M4 dùng để đo neo (tham khảo, KHÔNG phải mã thi công; chưa có nhánh gốc ổ nt và chưa có sửa sau lượt 5).
- Quyết định Q1–Q5: chủ kho 2026-11-20 (phiên điều phối #1206), theo khuyến nghị.
