# EVIDENCE — PR #468, reviewed_sha f77f19895e00835d71644d82f1c54e9b519ccfe6 (= 02b0b86 + lượt 12 df0800c/c073655 + readback sau hạn của phiên kia e377c42/f77f198)
Đo 2026-09-07T20:47:26Z trên cây f77f19895e00835d71644d82f1c54e9b519ccfe6, executor (Claude):
## Năng lực đo cấp cho reviewer (vá P1 mirror-thieu-ref-khong-du-do-a9)
- `kho.git` = `git clone --mirror` THẬT từ GitHub (20:44Z), `remote update --prune` lúc readback; `cay-kho/` clone từ mirror ⇒ `refs/remotes/origin/*` = **303** nhánh (origin trỏ URL GitHub, KHÔNG gọi mạng).
- `tai-lieu/ls-remote-heads.txt` = `git ls-remote --heads origin` (tên+OID) tại 20:45:09Z; `tai-lieu/ref-coverage.txt`: máy chủ 303 · cục bộ 303 · thiếu 0 · thừa 0 (so TẬP TÊN, không wc -l). Bạn tự so lại: `for-each-ref refs/remotes/origin` trong cay-kho với ls-remote đã giao.
## Readback SAU HẠN (#456 hết hạn danh nghĩa 14:30:07Z; chủ kho thu hồi sớm bằng comment https://github.com/ducthangho/tra-luat/issues/456#issuecomment-5570971814 12:57Z)
Chạy `ops/lease_publish.py ai-dang-giu` trong cay-kho lúc 20:45:46–52Z (nguyên văn: `ai-dang-giu-readback.txt` + ba tệp `ai-dang-giu-*.txt` ở gốc sandbox):
| đường | NGƯỜI_GIỮ | dòng #456 | rc |
|---|---|---|---|
| .github/workflows/ci.yml | **1** exec-1r4 | 0 | 11 |
| .claude/dev/ci_dang_ky_test.py | **1** exec-1r4 | 2, cả hai HẾT_HẠN | 11 |
| .claude/hooks/pretooluse_guard_test.py | 0 | 2, cả hai HẾT_HẠN | 0 |
Phiên KHÁC đã đo độc lập lúc 14:39:17Z (`tai-lieu/DOC-READBACK-SAU-HAN-456.md`, commit e377c42/f77f198): cùng kết quả 1/1, blob 8b2103c trên 11 nhánh không bia mộ, 1f95042 trên 1 nhánh có bia mộ. Đây là hai phép đo của HAI phiên; bạn là phép đo thứ ba, trên tập ref đủ.
## Cổng trên head (đo trong kho nguồn tại c073655; diff c073655→f77f19895e00835d71644d82f1c54e9b519ccfe6 chỉ thêm 1 tệp DOC-READBACK)
bien_nhan_v2 ĐẠT (27 v2? — tự đếm) · lease_publish_test 121/121 · doc-claims ok · doctrine/adr sạch · EOL ok · gate CI ubuntu trên 02b0b86 = success (run 34125520827), trên c073655/f77f198 chưa đọc kết luận.
## Trạng thái finding lượt 12 theo executor
- P1 bia-mo-mot-ref-khong-thu-hoi-moi-ban: ĐÓNG BẰNG THỜI GIAN (readback ở trên); cơ chế bia mộ (`_kiem_bia_mo` any(...)) KHÔNG sửa — ngoài phạm vi PR này, DOC-READBACK tự khai.
- P1 mirror-thieu-ref-khong-du-do-a9: vá bằng cách dựng bundle này (mirror đủ ref + ls-remote + ref-coverage).
- 2 P2 hồ sơ: vá ở df0800c (receipt lượt 10/11, GHI-NHAN).
GIỚI HẠN TỰ KHAI: chưa chạy packet_loop_test / ci_dang_ky --chay trên head này (PR thuần ops/). Hai lần phóng lượt 12 bị launcher chặn rc=11 là lỗi sandbox executor. Sau lượt này, theo chỉ thị chủ kho ("Sau 14:30 chạy lượt 13 rồi bắt tay #463 luôn"), executor sẽ init packet #463 theo lease exec-1r4 — việc ấy KHÔNG nằm trong PR này.
