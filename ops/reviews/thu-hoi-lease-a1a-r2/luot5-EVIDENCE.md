# EVIDENCE lượt 5 — lời khai của phiên soạn, KHÔNG phải phép đo của reviewer

## E17. Xử lý lượt 4 (bản nháp 5: commit `a22d3198` + ghi quyết định `43a17e1e`)
- Áp `luot4-HINT.patch` nguyên hunk (SPEC + `do_q6.py` + `mut_q6.py`); băm `do_q6.py` sau áp = `957b6432…`, khớp băm bạn khai.
- Đóng ba khoảng trống phủ bạn chỉ ra ở lượt 4 (đột biến tự soạn SỐNG): ca `han-bang-dung-C` (hạn = C ⇒ rc0, giữ `()`),
  `thu-muc-con` (`ops/leases/sub/z.yaml` hợp lệ ⇒ rc3), `han-vang` (chỉ có ID ⇒ rc3); ba mutant tương ứng với tập đích khai
  trước. `_kho_gia` sửa để tạo được thư mục con.
- Bản in: `--tu-kiem` 29/29; `mut_q6.py` 18/18 KHOP + gốc, 0 Traceback, `TAT_CA_KHOP`. Hai lần đo đầu LỆCH theo chiều ngược:
  mutant "hạn hỏng coi như hết hạn" giết thêm `han-vang`, "bỏ lọc hạn" giết thêm `han-bang-dung-C` — hành vi đúng, tập khai hẹp ⇒
  mở rộng tập khai, không sửa mutant.
- Kho thật: bản in script bản nháp 5 **byte-equal** `q6-do-2026-09-26.json` (`cmp` rc0).
- SPEC: §0 vòng 4 ghi ngoại lệ ADR-0044 (≤3 tệp, ≤663 dòng, #564 `5851070255`) và quyết định nâng trần 10 + lặp tới sạch
  (#564 `5851241285`, thay lựa chọn "fix rồi human audit" trước đó); §8.1 ghi quyết định; §8.2 số mới.
- `do_q6.py` sha256 `8d8da92f…`, `mut_q6.py` sha256 `37575113…`.
