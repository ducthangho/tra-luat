# r2 — bằng chứng sửa hồi quy C1 trên Windows (packet N)

- `c1-m7.diff`: diff nguyên văn của M7 trên `scripts/test_fragments/wp433_gws_cred_win_duong.py` so với head `143115a`.
- `do433r2b.py` (chẩn đoán + nguyên mẫu `lexists`), `do433r2c.py` (nguyên mẫu byte config), `do433r2d.py` (nguyên mẫu đủ M7): driver Desktop, mỗi bản giữ `F:\tl-win\KHOA.txt`, chạy trên clone sạch `143115a` / `dd1985b`, tự kiểm sha256 của từng biến thể trước khi chạy. `chay_c1.py`: chạy một biến thể C1 bằng `chay_fr` của rig `wp433n_rig.py` (sha256 `f5bbdb4d…`, comment PR #1441 7029480932).
- `linux-c1.txt`: Linux, head và base × (gốc, nguyên mẫu byte config, đủ M7).
- Đầu ra thô Desktop: `F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\r2-bang-chung.zip`, sha256 `bc68aae96e53b8f7bcd77fe4252cbd7e8990d26c88f7df56800b5b0e7433ab90` (chưa kéo vào kho; phiên land kéo về như #1425).

Kết quả Desktop (tóm tắt `TOM-TAT.txt`):

| lượt | C1 `run` | bộ đếm |
|---|---|---|
| head gốc | False | CA 2/3 · LUOT 73/76 · DOT BIEN 45/47 (đỏ `W4.loai_o_loi · hop_dong`, 2 tín dụng giả) |
| head + `lexists` | False | đỏ nhãn `w6` (config đã có từ lượt W4 trước) |
| head + byte config (M7 a) | False | CA 3/3 · LUOT 76/76 · DOT BIEN 46/47 — `db_nt_git_nuot_loi` SONG_SOT |
| head + đủ M7 (a+b), 2 lần | True | CA 3/3 · LUOT 76/76 · DOT BIEN 47/47 · HONG 0 · TU_KIEM 3/3 |
| base gốc | True | CA 3/3 · LUOT 76/76 · DOT BIEN 47/47 |
| base + đủ M7 (phản chứng) | False | đỏ `W4.loai_o_loi · hop_dong` |
