# Cross-review ĐẶC TẢ wp1236 r9 — vòng 1 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-claude/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách SỬA BẢN SAO fixture thật (đổi một băm, xoá một dòng…) là được.

## Đầu vào
- Đặc tả r9: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-claude/SPEC.md`, sha256 `ba466e72bb86c33462847c9ab92469d44acbf6bcc81b4443179d33c2e00940e7`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-claude/repo`, HEAD `89c07bc` = `origin/master` `8048551` + một commit chỉ thêm `ops/specs/wp1236-r9.md` và `ops/reviews/wp1236-r9-soan/`. Lịch sử đầy đủ, KHÔNG nông.
- r8 (bản bị thay, để đối chiếu lý do bỏ): `git show refs/remotes/origin/claude/spec-1236-r8:ops/specs/wp1236-r8.md`; VERDICT vòng 6 r8 ở `ops/reviews/wp1236-spec-r8-6-{codex,claude}/VERDICT.md` trên cùng ref.
- Bản tham chiếu đo của phiên soạn: `ops/reviews/wp1236-r9-soan/` (`thamchieu.py`, `do_loi_khai.py`, kết quả `do_tep.txt`, `do_loi_khai.txt`). Chạy lại: `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-claude/ISSUE.md`: thân #1236, quyết định duyệt r7 (Q1–Q10), quyết định ra r8, hai quyết định vòng 4–5 r8, thân #1257. Quyết định của chủ kho ngày 20-11 chọn r9 phạm vi hẹp: ghi ở mục `nguon_cap_viec` của đặc tả.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L7) · `docs/adr/0053*`, `0055*`, `0067*` · `ops/land_evidence_nguon.py` · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `CHECK_BAT_BUOC`) · `ops/ci_provenance.py` · các `ops/land/*/danh_gia_gate.py` (ba phiên bản).

## Việc phải làm (theo thứ tự ưu tiên)
1. **Thiết kế có đạt mục 1–2 của Issue #1236 không?** Tìm một lời khai `gate_output` dương mà hồ sơ MỚI có thể ghi, qua được L8/D2b như đặc tả viết, trong khi KHÔNG có tệp danh-gia khớp provenance của một run land thật. Giới hạn "tệp danh-gia viết tay chép đúng băm" đã được khai ở `chua_do_duoc`; nêu nó lại chỉ khi bạn cho rằng khai thế là không đủ và có cách đóng rẻ trong phạm vi.
2. **K1–K8 có đúng trên dữ liệu thật không?** Chạy lại bản tham chiếu, đối chiếu số 47/10/9 và 53/40/77, kiểm sáu fixture. Có chặn oan một tệp danh-gia đúng không? Chốt nào trong đặc tả KHÁC bản tham chiếu (đặc tả là chuẩn; lệch thì nói rõ cái nào đúng)?
3. **Tiêu chí nghiệm thu** (L3, L6 của soan-spec): mỗi ca có đỏ được không, mỗi đột biến có đúng ca đích không, có ca nào chỉ đo sự có mặt? Có ca nào phụ thuộc thứ không có trong CI (lịch sử git, symlink, mạng)?
4. Write set, kích thước, `nang_tran`, `pham_vi_e`, `luat_dung`: chỉ nêu nếu sai số đo, sai ADR, hay thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r9 vòng 1
spec_sha256: <sha256 bạn đo được>
## Findings
- id: <R01…>
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
Ghi VERDICT tăng dần vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-claude/work/VERDICT.md` trong lúc làm, để lượt bị ngắt vẫn giữ được phần đã ghi.
