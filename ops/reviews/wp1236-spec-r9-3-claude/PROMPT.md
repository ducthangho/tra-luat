# Cross-review ĐẶC TẢ wp1236 r9 — vòng 3 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách SỬA BẢN SAO fixture thật là được.
- Không tìm kết luận của reviewer kia (VERDICT vòng 1–2 của họ đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 2 CỦA CHÍNH BẠN (vòng 1 của bạn có ở `ops/reviews/wp1236-spec-r9-1-claude/`): `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/VERDICT_VONG2_CUA_BAN.md`. Bảng `phan_bien` cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.

## Đầu vào
- Đặc tả r9 bản sửa 2: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/SPEC.md`, sha256 `50269a88976968f60f50f714c882ab88cba6f597ff0249bd19b5ce157342b496`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`ba466e72…`): `git show 89c07bc:…`; vòng 2 (`18da18c4…`): `git show d81f359:ops/specs/wp1236-r9.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/repo`, HEAD `e9afa78927a771c734ea14dae8b5007c1fdfb6f2` = `9e05aac` (master `8048551` + ba commit chỉ thêm `ops/specs/wp1236-r9.md`, `ops/reviews/wp1236-r9-soan/`, `ops/reviews/wp1236-spec-r9-{1,2}-*`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử đầy đủ, KHÔNG nông.
- r8 để đối chiếu: `git show refs/remotes/origin/claude/spec-1236-r8:ops/specs/wp1236-r8.md`.
- Bản tham chiếu đo (đã cập nhật theo bản sửa 1): `ops/reviews/wp1236-r9-soan/`. Chạy lại: `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` và `python3 -B ops/reviews/wp1236-r9-soan/do_loi_khai.py .` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/ISSUE.md`: thân #1236, các quyết định chủ kho liên quan, thân #1257.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L7) · `docs/adr/0053*`, `0055*`, `0067*` · `ops/land_evidence_nguon.py` · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `CHECK_BAT_BUOC`, `_canon`) · `ops/ci_provenance.py` · ba phiên bản `ops/land/*/danh_gia_gate.py`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding vòng 2 CỦA BẠN (và finding vòng 1 còn mở):** ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo.
2. **Các chốt MỚI của bản sửa 2** có đúng, có chặn oan dữ liệu thật, có ca + đột biến đỏ đúng đích không: `la_landed` ba dạng (A2-12, A2-13, m47–m49), D2b neo OID (`git branch -r --contains`, `git ls-tree` mode, `git archive <oid>`, tên lý do cố định, C1–C9), B8 bản sao pr680, m45–m46, K3 `moc.checkout` khác rỗng. Số 25/56/39/50.
3. **Thiết kế có đạt mục 1–2 của Issue #1236 không** — tìm một lời khai dương mà hồ sơ MỚI qua được L8/D2b mà không có tệp danh-gia khớp provenance của một run land thật (ngoài các giới hạn đã khai ở `chua_do_duoc`/`ngoai_pham_vi`).
4. Số đo, `kich_thuoc`, `nang_tran`, `pham_vi_e`, `luat_dung`: chỉ nêu nếu sai số đo, sai ADR, hay thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r9 vòng 3
spec_sha256: <sha256 bạn đo được>
## Finding vòng 1–2 của tôi còn mở
- R0x / S0x: ĐÓNG | CÒN MỞ | HẾT ĐỐI TƯỢNG — <một câu>
## Findings mới
- id: T01
  severity: P0|P1|P2|P3
  vi_tri: <mục/dòng trong SPEC.md>
  van_de: <một câu>
  bang_chung: <lệnh đã chạy + output rút gọn, hoặc trích dẫn>
  de_xuat: <sửa thế nào>
## Đã đo lại, khớp
- <liệt kê ngắn>
KET_LUAN: approve | changes_requested
```
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2. P3 không chặn. Mỗi P2 trở lên phải có phép đo hoặc trích dẫn cụ thể. Dòng `KET_LUAN:` là dòng cuối cùng.
Ghi VERDICT tăng dần vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/work/VERDICT.md` trong lúc làm (reviewer chỉ có Bash thì ghi bằng Bash, chỉ dưới `work/`).
