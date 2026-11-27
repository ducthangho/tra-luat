# wp1466 r10 — hồ sơ dựng đặc tả

Đặc tả r10 được dựng máy từ r9 (sha256 `28de9d57…a6f7c`) bằng script `dung_r10.py.txt`. Mỗi phép thay trong script đều có assert, đòi chuỗi cũ khớp đúng số lần.

Phép đo: lấy H exact `da4e876`, áp phần diff r9→r10 của khối `adr` vào tệp ADR-0068, rồi chạy:
- `doc-claims-check --strict`: rc 0, `ok: true`, `flags` rỗng; kết quả lưu ở `doc-claims-H-cong-adr-r10.json`;
- `doctrine-scan`: rc 0;
- `adr-song`: rc 0.

Protocol không đổi so với r9, nên bảy băm khoá không đổi.
