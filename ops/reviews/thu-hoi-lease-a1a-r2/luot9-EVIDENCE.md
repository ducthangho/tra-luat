# EVIDENCE — lượt 9 (lời khai phiên soạn `claude`; reviewer tự kiểm lại, đừng tin)

- Head `3f1bf2e2e5a77ec2bb1a40bb65b8c26410a3ff12` (PR #658). Từ lượt 8 (`d766717`) chỉ thêm `ops/specs/THU-HOI-LEASE-A1a-r3.md`
  và sửa đúng một gạch đầu dòng F18 trong `HAU-KIEM-CONNECTOR-652.md` (`DIFF.luot8-luot9.patch`).
- F17 đã sửa ở `d766717` (trước lượt 8 kết thúc? KHÔNG — sau: lượt 8 review `4abfdeb`; bảng S theo từng lượt nằm trong
  `d766717`, lượt này là lần đầu reviewer thấy nó).
- Cùng `d766717`: ca `ten-DEL-sau-duoi`, `ten-byte-sau-duoi`; chốt `ten-tep-khong-phai-utf8`; mutant `bo-rieng-DEL`,
  `bo-chot-utf8`; mở rộng tập đích `doc-ls-tree-khong-z` (4 ca tên) và `bo-chot-ky-tu-dieu-khien` (xuống dòng + DEL) vì
  hai lần đo đầu LỆCH theo chiều hành vi đúng/tập khai hẹp. Mutant decode `strict` KHÔNG đưa vào: nó chết bằng
  `UnicodeDecodeError`, tức giết bằng lỗi vô can.
- r3: tạo bằng script chép r2 rồi thay đúng 7 đoạn (tiêu đề · hàng `revision` · `thay_the_cho` · `reviewer` · `dong_bang` ·
  câu "Tìm ở master…fetch nhánh" · §0 thêm vòng 5 · §8 mục 2 thay câu chỉ dẫn chạy bằng khối "Bộ đo THI CÔNG").
  r2 sha256 vẫn `9bc0fe28…`; r3 sha256 `ac7e0129…`, 436 dòng.
- Tiêu chí dương của r3 đo trên log thật: dòng cuối `TU_KIEM: 35/35 dat`, 0 `HONG`; dòng cuối `TAT_CA_KHOP`, 27 `DUNG `,
  0 `SAI `, `DUNG LECH` duy nhất `chet-im-lang-rc2`; Q6 `cmp` rc0 (`1fc99cd9…`). Băm: `do_q6_hk.py` `0ec537e4…`,
  `mut_q6_hk.py` `c4f04f03…`.
- Quyết định vòng 5: #564 `5852159297` là BẢN GHI của phiên soạn cho chỉ thị chủ kho trong chat ("Đồng ý, làm đi"),
  không phải comment của chủ kho. Sandbox không mạng nên reviewer không đọc được comment ấy.
- Mirror: 441 head, tập (tên, OID) lệch 0 so `git ls-remote --heads origin` lúc `2026-09-27T03:06:01Z`.
