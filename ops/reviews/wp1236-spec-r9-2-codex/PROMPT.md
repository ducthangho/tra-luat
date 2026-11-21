# Cross-review ĐẶC TẢ wp1236 r9 — vòng 2 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách SỬA BẢN SAO fixture thật là được.
- Không tìm kết luận của reviewer kia (VERDICT vòng 1 của họ đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 1 CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/VERDICT_VONG1_CUA_BAN.md`. Bảng `phan_bien` cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.

## Đầu vào
- Đặc tả r9 bản sửa 1: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/SPEC.md`, sha256 `18da18c417a446284e7c40bf6c60070206891be88837bc4d88ad81d49c2c2e65`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`ba466e72…`): `git show 89c07bc:ops/specs/wp1236-r9.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/repo`, HEAD `026e35fab50887a6b7b09091ce0ba2200c3db307` = `d81f359` (master `8048551` + hai commit chỉ thêm `ops/specs/wp1236-r9.md`, `ops/reviews/wp1236-r9-soan/`, `ops/reviews/wp1236-spec-r9-1-*`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử đầy đủ, KHÔNG nông.
- r8 để đối chiếu: `git show refs/remotes/origin/claude/spec-1236-r8:ops/specs/wp1236-r8.md`.
- Bản tham chiếu đo (đã cập nhật theo bản sửa 1): `ops/reviews/wp1236-r9-soan/`. Chạy lại: `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` và `python3 -B ops/reviews/wp1236-r9-soan/do_loi_khai.py .` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/ISSUE.md`: thân #1236, các quyết định chủ kho liên quan, thân #1257.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L7) · `docs/adr/0053*`, `0055*`, `0067*` · `ops/land_evidence_nguon.py` · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `CHECK_BAT_BUOC`, `_canon`) · `ops/ci_provenance.py` · ba phiên bản `ops/land/*/danh_gia_gate.py`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding vòng 1 CỦA BẠN:** ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo.
2. **Các chốt MỚI của bản sửa 1** có đúng, có chặn oan dữ liệu thật, có ca + đột biến đỏ đúng đích không: CRLF (`xuong_dong_tron`, `cr_le`), K3 `provenance_chua_du`, K5 `ket_luan_lech`, luật `landed_khong_loi_khai_gate_output`, L8 sau cutover, D2b neo attempt và đọc từ `origin/master` (`git archive`), A1-13…A1-15, A2-12, B7, B8, C9.
3. **Thiết kế có đạt mục 1–2 của Issue #1236 không** — tìm một lời khai dương mà hồ sơ MỚI qua được L8/D2b mà không có tệp danh-gia khớp provenance của một run land thật (ngoài các giới hạn đã khai ở `chua_do_duoc`/`ngoai_pham_vi`).
4. Số đo, `kich_thuoc`, `nang_tran`, `pham_vi_e`, `luat_dung`: chỉ nêu nếu sai số đo, sai ADR, hay thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r9 vòng 2
spec_sha256: <sha256 bạn đo được>
## Finding vòng 1 của tôi
- R0x: ĐÓNG | CÒN MỞ | HẾT ĐỐI TƯỢNG — <một câu>
## Findings mới
- id: S01
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
Ghi VERDICT tăng dần vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-2-codex/work/VERDICT.md` trong lúc làm (reviewer chỉ có Bash thì ghi bằng Bash, chỉ dưới `work/`).
