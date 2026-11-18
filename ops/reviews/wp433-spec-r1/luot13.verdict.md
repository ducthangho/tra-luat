**Issue #433 · Packet 1 · Review đặc tả lượt 13**

| Finding lượt 12 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — §4b dòng 14, `db_w6_bo_symlink` | Đóng | Bản chuẩn và đột biến cùng truyền `dirname(cfgp)` vào `_trong_kho_git` của base. Đột biến chỉ bỏ luật (b) ở lá config. N6(2) chuyển từ rc 1 với dòng từ chối sang rc 0 với stderr rỗng, làm đỏ đúng nhãn đích `stderr`. Hai đối chứng N10(7), HOME = `K/home` và HOME = `K`, đều giữ nguyên rc 1, cùng dòng từ chối `nằm trong kho git`, và không tạo config. |
| P3 — §2/M3(3), hành vi khi tuần tự hoá lỗi | Đóng | Cả hai cách đều để `UnicodeEncodeError` lan ra. Base để lại JSON ghi dở. Thứ tự ghi theo M3(3) giữ nguyên byte `{"token":"CU"}` vì lỗi xảy ra trước khi gọi writer. §2 và M3(3) mô tả đúng kết quả này. |

**Finding mới trong diff ban12 → bản hiện tại** — Không phát hiện P0–P3.

Mô phỏng Python 3.13.18 bằng `python -B -` với fixture giả trong `/dev/shm`, rc 0. Gate triển khai ở trạng thái `not_run` vì packet chưa có mã.

- Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached tại cùng OID với ref `master` cục bộ.
- SHA-256 đặc tả `3721e4684c12a22ab165a032c409ddb979dc9786e8862f9cdbaeba4bd7a74f88`.
- Reviewer `openai_codex`, thực thi qua phiên Codex API, trả verdict trong phiên này.

KET_LUAN: approve
tokens used
39,216
**Issue #433 · Packet 1 · Review đặc tả lượt 13**

| Finding lượt 12 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — §4b dòng 14, `db_w6_bo_symlink` | Đóng | Bản chuẩn và đột biến cùng truyền `dirname(cfgp)` vào `_trong_kho_git` của base. Đột biến chỉ bỏ luật (b) ở lá config. N6(2) chuyển từ rc 1 với dòng từ chối sang rc 0 với stderr rỗng, làm đỏ đúng nhãn đích `stderr`. Hai đối chứng N10(7), HOME = `K/home` và HOME = `K`, đều giữ nguyên rc 1, cùng dòng từ chối `nằm trong kho git`, và không tạo config. |
| P3 — §2/M3(3), hành vi khi tuần tự hoá lỗi | Đóng | Cả hai cách đều để `UnicodeEncodeError` lan ra. Base để lại JSON ghi dở. Thứ tự ghi theo M3(3) giữ nguyên byte `{"token":"CU"}` vì lỗi xảy ra trước khi gọi writer. §2 và M3(3) mô tả đúng kết quả này. |

**Finding mới trong diff ban12 → bản hiện tại** — Không phát hiện P0–P3.

Mô phỏng Python 3.13.18 bằng `python -B -` với fixture giả trong `/dev/shm`, rc 0. Gate triển khai ở trạng thái `not_run` vì packet chưa có mã.

- Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached tại cùng OID với ref `master` cục bộ.
- SHA-256 đặc tả `3721e4684c12a22ab165a032c409ddb979dc9786e8862f9cdbaeba4bd7a74f88`.
- Reviewer `openai_codex`, thực thi qua phiên Codex API, trả verdict trong phiên này.

KET_LUAN: approve
rc=0 xong 2026-11-18T08:54:32Z
