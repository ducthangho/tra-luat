# Hiện vật reviewer lượt 14 — PR #468

reviewed_sha: 922956a7048fd23eea1c9f88aeb986e076f10e24

Kết luận ở `../VERDICT.md`. Checkout `../cay-kho/` giữ read-only.

- `preflight.json`: HEAD/tree, 306 refs, diff/numstat, danh sách path và sáu script lưu trữ.
- `verify_manifests.py`, `manifests.json`, `manifest-*.stdout/stderr`: giải ánh xạ DOC-MANIFEST rồi sha256sum; 12 manifest, 967 mục.
- `manifest-*.mapped.sha256`: chỉ thay đường dẫn từ manifest nguồn sang đường tuyệt đối của snapshot sandbox này, không đổi hash. Nếu vận chuyển, chạy lại verify_manifests.py trên snapshot đúng SHA để giải đường mới; không dùng đường máy cũ làm bằng chứng thiếu tệp.
- `audit_evidence.py`: đọc log/byte/JSON/YAML, đối chiếu receipt/blob/prompt và gọi riêng t33 với PATH thiếu/có actionlint. Không gọi main của suite, không gọi CI. Cần PyYAML và binary actionlint đã giao trong sandbox nếu muốn tái chạy probe.
- `full-gate.json`, `receipt.json`, `t33-probe.json`: kết quả của script trên. Trường parsed/rc_records_only là nội dung hồ sơ tự khai; không tự trở thành xác thực nguồn.
- `short-gates.json`, các stdout/stderr cùng tên: ba cổng ngắn chạy mới; `doc-claims-difference.json` ghi khác biệt JSON lịch sử so lần mới.
- `goi-y/`: patch/prose gợi ý cho hai P3; nhãn áp dụng nằm trong README của gói. Không sửa checkout.
- `build_prose_hint.py`: dựng và áp thử gợi ý vào bản sao scratch; chỉ dùng khi prose-check chưa tồn tại, không phải script gate kho.
- `prose-hint-check.json`: dry-run/apply patch và manifest bản sao đều rc0.
- `final-check.json`: HEAD/tree giữ nguyên, status/index/diff rỗng, 306 refs, không mạng/suite dài/CI.

ARTIFACTS.sha256 tính từ gốc sandbox: VERDICT.md là verdict ngoài thư mục này;
do-review14/ là thư mục hiện vật. Manifest không băm bản thân, không gồm bản sao
prose-check/ dùng thử patch. Tất cả hash nguồn của các gói lịch sử được giữ nguyên.
