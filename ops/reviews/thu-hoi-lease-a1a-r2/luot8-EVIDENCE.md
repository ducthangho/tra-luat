# EVIDENCE — lượt 8 (lời khai phiên soạn `claude`; reviewer tự kiểm lại, đừng tin)

- PR #658 head `4abfdeb596c7e5e744e0354a7bad1b775da54c38`, base `master` `67802bf9a1b9adba6d8b13c63ee46744d74655b5`
  (merge #652). Diff: `DIFF.pr658.patch`, chỉ trong `ops/reviews/thu-hoi-lease-a1a-r2/`.
- Tự kiểm `do_q6_hk.py --tu-kiem`: 33/33 (31 ca cũ + `ten-co-tab`, `ten-xuong-dong-sau-duoi`).
- Ma trận `mut_q6_hk.py`: 25/25 DUNG, `TAT_CA_KHOP` (22 mutant cũ + `doc-ls-tree-khong-z`, `bo-chot-ky-tu-dieu-khien`,
  `chet-im-lang-rc2` mong LECH). Bảy assert tự kiểm bộ phân hạng chạy trước ma trận.
- Phản chứng chốt rc: gỡ dòng `if rc!=(1 if dich else 0): return False` + thay 7 assert bằng `pass` ⇒
  `SAI  KHOP chet-im-lang-rc2` ⇒ `CO_LECH` (chạy trên bản trước khi đổi tên tệp; khác đúng dòng docstring đầu).
- Q6 thật: `do_q6_hk.py <kho> 072181157a27… 2026-09-10T04:55:37Z` ⇒ rc0, output **cmp bằng** `q6-do-2026-09-26.json`.
- `do_q6.py` sha256 `36d8f1667aaa72a1bf00dfb7d1ded4331cb65efab5a0376bb3506528fd6d89d0`, `mut_q6.py` sha256
  `272dc1e82a32331348f59c182803c7cada373f98fbbdd6d4f91ce40d6641e794`: bằng băm đặc tả trích (dòng 303, 325).
- HINT: `git apply --check` của cả sáu patch OK trước và sau nhãn, trên đúng bản nháp gốc (bảng H), có đủ `do_q6.py`/
  `mut_q6.py` của bản nháp ấy cho lượt 3, 4.
- Bề mặt thực thi 7 lượt: đọc từ `run.json` (khoá `provider`, `execution_surface`, `transport`, `transport_sha256`) và
  header `stderr.log` của launcher. `origin` của `cay-kho` 7 lượt: `git remote get-url origin` trên chính các workspace còn giữ.
- `f1dec864…` (connector gọi là reviewed commit) KHÔNG có trong kho cục bộ; cây `15c0240b` / `45e611fa` khớp mô tả connector.
- Lượt này: `cay-kho` `origin` = `https://github.com/ducthangho/tra-luat.git`; 440 head, tập (tên, OID) lệch 0 so
  `git ls-remote --heads origin` lúc `2026-09-27T01:58:41Z` (sha256 tập `d854f679…`, `.tap-ten-oid-may-chu.txt`).
