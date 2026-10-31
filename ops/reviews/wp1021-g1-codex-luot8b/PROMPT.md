# Cross-review độc lập — packet #1021 r2 (BIEN-NHAN-V2-GLOB-HOA-THUONG), lượt 8 (lời gọi Codex 8/9)

Bạn là reviewer độc lập (họ openai) cho executor họ claude. Viết bằng tiếng Việt.

## Neo
- Head được review: `356a27e1378b2162bbc0be2ec06ff08fdacbdead` (checkout detached tại `cay-kho/`, clone đủ lịch sử, không nông).
- Lượt trước (7) review `c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8`; nguyên văn verdict: `VERDICT-LUOT7.md` (sha256 `181946a7e31be93140bf45fa35fb3e207d2c8f263bddca24ec504acca00d1a10`).
- Base của diff tổng: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93` (master sau #1041, đã merge vào nhánh ở `3883b60`). Base gốc của packet: `757bde561d09738858506aecf5de2f050a5f0d5e`.
- SPEC: `SPEC.md`, sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d` — kiểm lại băm trước khi dùng.
- Write set: đúng hai tệp `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`.
- `origin/master` trong clone hiện là `b653574` (không chạm hai tệp write set; `git merge-tree` với head sạch). Không phải base của review.

Tệp đầu vào trong sandbox (thứ định danh là BĂM/SHA, không phải tên nhánh):
- `DIFF-LUOT8.patch` = `git diff c8a493c 356a27e` (hai commit `6964930`, `356a27e`: executor khai CHỈ docstring/chú thích).
- `DIFF-TONG-tu-b29da0b.patch` = `git diff b29da0b 356a27e` (toàn bộ thay đổi #1021 + các ca biên c88 cửa sổ M4 chủ kho gộp vào review).
- `DIFF-1021-goc-757bde5-e9e0048.patch` = diff #1021 trước khi merge #1041 (tham khảo).

## Phạm vi (giống lượt 5–7)
1. **ĐỐI CHIẾU LƯỢT TRƯỚC**: P3 `chu-thich-tro-sai-ca-ngoai-le-lap-trinh` (lượt 7, `ops/bien_nhan_v2.py:90`, `c99` → `c100`) — đo xem ĐÃ VÁ THẬT chưa. Các lớp cũ (F1 `loi-do-liet-ke-thu-muc-thoat-traceback`, F2 `loi-do-thieu-chot-ngoai-le-lap-trinh`, F3 OSError ngoài PermissionError, P1 c88 `bien-ngoai-cua-so-surface-chua-co-rang`, P3 chú thích m156/m157, giải xung đột #1037) — xác nhận còn đóng. Được phép kế thừa phép đo sâu của lượt trước KHI chứng minh được AST mã thực thi không đổi so `c8a493c` (nêu rõ đã kế thừa gì, không khai đã chạy lại).
2. **Diff lượt này** (`DIFF-LUOT8.patch`): xác nhận chỉ đổi docstring/chú thích (so AST), và mọi tham chiếu ca/đột biến/hành vi trong các docstring đã sửa là ĐÚNG với mã và bảng đột biến hiện hành (đo, ví dụ bằng đột biến chạy riêng như lượt 7 đã làm với m153 — đừng chỉ đọc).
3. **Rà toàn diff tổng** `b29da0b..HEAD` tìm mọi P0–P3 còn sót, gồm cả docstring/chú thích trỏ sai ca/đột biến ở những chỗ executor chưa sửa.
4. **Tiêu chí SPEC** C1a/C1b/C2/C3/C6/C9 đo lại trên head (Linux). C3 = hoàn nguyên glob phải bị `c101` giết. C6: `python3 ops/bien_nhan_v2.py --root .` phải `TỔNG: ĐẠT` (executor khai `tổng 306`). C9: ruff `--select F` delta so base = 0 (F541 đỏ sẵn), `doctrine-scan` sạch, `git diff --check` rc0, `rg 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` 0 dòng.
5. **Toàn suite** `python3 ops/bien_nhan_v2_test.py` tại `cay-kho/` (executor khai `98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`). Đòi bằng chứng dương: N/N hai số bằng nhau, không suy từ rc.
6. Đột biến chạy riêng (`_dot_bien(chi={tên})`): ít nhất m142, m147, m153, m154, m155, m156, m157 — chết ĐÚNG ca đích, đối chứng sạch, không tín dụng giả.
7. C4/C5/C7 (Windows CI, Ubuntu CI, Windows local): executor KHAI Ubuntu PR run `41113943723` success, Windows dispatch `41113949578` success (job `gate-ops (windows-latest)` runner_id 1000026867, `98/98 · 153/153 · 2/2`), Windows local trên head này KHÔNG ĐO ĐƯỢC. Nếu bạn có đường đọc GitHub độc lập thì đo (jobs/labels/runner_id/log); không có thì ghi **KHÔNG ĐO ĐƯỢC**, không nhận lời khai làm bằng chứng. Không chạy test trên máy Windows từ xa.

## Ràng buộc
- KHÔNG sửa bất kỳ tệp nào trong `cay-kho/` (mã nguồn checkout được review). Mọi đột biến/fixture/script làm trên BẢN SAO hoặc qua cơ chế `_dot_bien_tep` của suite, trong sandbox; kiểm băm nguồn trước/sau. Không commit, không push, không gọi workflow, không ghi gì ngoài sandbox.
- Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`; `core.abbrev=7` đã đặt. Lưu lệnh/cwd/rc/thời gian/stdout/stderr vào `evidence/`.
- Phản chứng nào cần soạn nội dung nhạy cảm (ví dụ đường dẫn thoát khỏi cây thư mục) thì MÔ TẢ bằng lời trong verdict thay vì tự dựng.
- Ngưỡng packet: approve chỉ khi **không còn P0/P1/P2/P3 nào mở**. Mỗi finding: mức, slug lớp, vị trí `tệp:dòng`, lệnh tái hiện + output, `HÌNH DẠNG: <...>` (đặc biệt đánh dấu nếu là hình dạng `bo-chon-ung-vien` — chốt dừng của SPEC), hướng vá cụ thể (có thể kèm `HINT-LUOT8.patch` trong sandbox, đã `git apply --check` trên bản sao).
- Ghi kết quả TĂNG DẦN vào `VERDICT.md` ở gốc sandbox ngay từ đầu (để lượt bị cắt vẫn còn dấu), rồi hoàn thiện.

## Dạng `VERDICT.md`
Ba dòng đầu, đúng dạng:
```
Verdict: approve|request_changes
Reviewed commit: 356a27e1378b2162bbc0be2ec06ff08fdacbdead
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d
```
Sau đó: kết luận ngắn; Neo và cách tái hiện; ĐỐI CHIẾU LƯỢT TRƯỚC (bảng); Bảng tiêu chí (C1a…C9, toàn suite, đột biến); Bảng finding (đếm P0/P1/P2/P3 mở); Kiểm tra cuối và giới hạn (snapshot nguồn đầu/cuối giống nhau). Verdict không cấp quyền merge/land.
