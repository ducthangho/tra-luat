# Gói gợi ý review PR #468 lượt 10

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**

Nền: `c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355`. Cây tệp nằm trong `cay/`;
`hint_provenance.json` ghi nguồn byte, băm nền, băm đầu ra và từng hunk → slug.
Tệp thêm mới có `target_base_sha256: null`; 19 hiện vật phục dựng có nguồn
`source_path`/`source_sha256` trong gói lượt 8. Không áp mù khi nền khác.

- `bia-mo-mot-ref-khong-thu-hoi-moi-ban`: Issue #463 được bổ sung số đo chặn và thủ tục readback sau hạn.
  Đây là sửa hồ sơ vận hành; **không đóng P1 trước 14:30:07Z**, không thay/cấp/thu hồi lease.
  Đường chủ kho chọn cần thời gian thực và readback mới; gói tệp không thay được việc đó.
- `manifest-luot8-liet-ke-hien-vat-khong-duoc-giao`: phục dựng đúng 19 tệp còn thiếu trong bản thử lượt 9,
  giữ nguyên manifest. Kèm 50 tệp và manifest nguyên trạng để tự kiểm checksum trong cây gợi ý;
  README phân biệt bản thử lịch sử với hiện vật đo mới.

Gói không chứa commit, push, lease mới, biên nhận mới hay kết quả CI mới.
