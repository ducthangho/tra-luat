# Hiện vật cross-review lượt 6

reviewed_sha: `2adb6819caee0225d7b7e4f0c4e8c16f2faa7e73`

Chạy từ thư mục chứa PROMPT.md. Các script chỉ dùng bản sao `cay-kho/` và tài liệu được giao; không commit/push vào ref của bản sao. Bộ test git tự tạo kho fixture trong `do-review/tmp/`.

- `harness.py`: trích đúng hai khối H, ghi `h_tong.py`/`h_predicate.py`, giữ nguyên các hàm consumer `chay_moi`/`mau_theo_nen` và chuỗi SPAN.
- `attack_h.py`: tái lập 1213 hàng có oracle hai chiều. `attack-h-cases.json` giữ đầu vào, grammar thay thế, kỳ vọng và kết quả; không đồng nhất số hàng với số đầu vào duy nhất.
- `run_real.py`: gọi `_chay_that` trên 8 formatter thật, lưu từng stdout và `real-results.json`. Các suite có thể kéo dài nhiều phút. Lượt gốc thiếu socket loopback, Ruff đúng phiên bản và môi trường fixture nên một số suite đỏ; không thay chúng thành xanh giả.
- `rerun_nhanh.py`: sửa riêng cấu hình git fixture trong tiến trình (`commit.gpgsign=false`) để tránh gọi dịch vụ ký của môi trường. Không sửa mã test. Bản in rc=0 có băm trùng lịch sử.
- `run_gates.py`: bốn cổng ngắn, lease check và hai phép ai-dang-giu. HTTPS bị chặn bằng `GIT_ALLOW_PROTOCOL=file`, nên hai phép cuối fail-closed rc=12; không coi là phép đo GitHub.
- `audit_static.py`: băm, diff, trường lease, dependency, số dòng, inventory hiện vật và phép đọc snapshot lease với `doi_chieu_ref=False`. Phép đọc này không thay cổng hai nguồn.
- `recheck_contracts.py`: đối chiếu ví dụ Issue, consumer khi tách YAML, số học các bảng đã in. `d9-comparison.json` ghi thêm hai fixture 5000 chữ số tại cặp CA/nhanh qua cùng harness; cùng BASE/H đều ValueError.
- `extra_checks.py`: số nhóm/span/byte của đầu ra, bốn mutant H trên cùng 1213 hàng và workload tại 11 head.
- `count_spawn.py`: đếm Popen một lần mỗi tiến trình cho đối chứng 2A/2B; lưu `spawn-counts.json`.

Mỗi script đo xuất JSON/log tại đây. Tệp `.stdout` giữ nguyên chuỗi do `_chay_that` trả về sau chuẩn hoá newline của `subprocess.run(text=True)`. Băm khối H tính cả newline cuối trước hàng rào Markdown.

`ARTIFACTS.sha256` băm các script/dữ liệu/log ổn định trong thư mục này, loại cache và thư mục temp. VERDICT.md được giao riêng; không chạy `finalize_verdict.py` như một phép kiểm, vì nó là công cụ dựng báo cáo và sẽ ghi đè báo cáo.
