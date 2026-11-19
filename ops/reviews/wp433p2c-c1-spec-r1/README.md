# Review đặc tả #433 P2c-C1 (`GWS-CRED-DICH-NGOAI-KHO-C1` r1)

- Bản đóng băng: `ops/specs/GWS-CRED-DICH-NGOAI-KHO-C1-r1.md` = `c1/rv/dac-ta-ban12.md`, sha256 `758782c72e867829533f72ae1ef5fc91e79ce964bc59c633dd8ad4b1cd03ccce`.
  Chủ kho duyệt băm 19-11 (ADR-0067, AskUserQuestion phiên điều phối #1206), phương án (b): KHÔNG qua review vì bản 12 chỉ đóng hai P2 của lượt 11
  bằng nguyên văn câu thay thế của reviewer (`c1/rv/ban11-ban12.diff`, 7 hunk).
- `gop/`: lượt 1–3 trên đặc tả GỘP P2c (`GWS-CRED-DICH-NGOAI-KHO-C`, bản 1–4; `dac-ta-gop-ban-cuoi.md` = bản 4), chưa approve; chủ kho tách thành C1 → R.
- `c1/rv/`: lượt 4–11 trên bản C1 (`dac-ta-luotN.md`, `prompt-luotN.md`, `luotN.stdout.txt`, `luotN.verdict.txt`). Lượt 9–10 do chủ kho cho phép
  (E2); lượt 11 do chủ kho nâng trần +1 (11/11). Lượt 11: `request_changes`, 0 P0/P1, 2 P2 (đóng ở bản 12), 3 finding lượt 10 xác nhận đã đóng.
- `c1/nguyen-mau/`: nguyên mẫu M1/M2 (KHÔNG phải mã thi công) và bộ đột biến; r4: 38/38 đột biến đổi màu đúng lượt đích trên 3.11/3.12/3.13; `dem_neo.py`.
- Không chép `*.stderr.txt` (bản ghi phiên Codex, ~3,5 MB) — theo tiền lệ `ops/reviews/wp433p2b-spec-r1/`.
- Đặc tả R (`GWS-CRED-DICH-NGOAI-KHO-R` r1, sha256 `4d4b3181…`, chủ kho đã duyệt) KHÔNG ở đây; lease R cấp sau khi C1 land.
