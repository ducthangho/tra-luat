# Cross-review ĐẶC TẢ wp1236 r1 — vòng 1 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r1-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r1-codex/work/`.
- Bạn không có (và không được tìm) kết luận của reviewer khác. Tự kết luận.
- Hướng thử nào đòi soạn nội dung tấn công (đường dẫn thoát cây, mã độc…) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r1-codex/SPEC.md`, sha256 `d599ff336ac68eb0cb30f36167cf1c9f2beeea04fc2909de7324670b93fa8eee`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho tại commit `b9766fe2cafbede82547a6336ab2a9093084b609` (= origin/master `3163f4d` + đúng một tệp `ops/specs/wp1236-r1.md`), ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r1-codex/repo`, lịch sử đầy đủ (không nông).
- Thân Issue #1236 + comment bổ sung: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r1-codex/ISSUE.md`.
- Đọc thêm trong kho: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8.1, §10.2.2, §10.2.3, §20) · `.claude/skills/soan-spec/SKILL.md` (luật L1–L6 cho đặc tả) ·
  `ops/land_evidence_nguon.py` · `ops/kiem_ho_so_land.py` · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`) · `ops/ci_provenance.py` ·
  `ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py` · `ops/land/pr1231-wp1105-provenance/danh_gia_gate.py` · `ops/land/` nói chung.
  Mẫu đặc tả đã duyệt cùng kho: `git show origin/ops/wp1237-spec:ops/specs/wp1237-r1.md` nếu ref có trong clone; không có thì bỏ qua.

## Việc phải làm (theo thứ tự ưu tiên)
1. **ĐO LẠI các con số** của đặc tả trên chính clone này (bảng ba cổng, 123/27 hồ sơ, bảng dạng tệp, bảng A 21 hồ sơ/24 lời khai,
   bảng B 15 hồ sơ/22 lời khai, ba trạng thái #1127, nền ruff nếu có ruff). Số nào lệch là finding; ghi lệnh và output.
2. **Mâu thuẫn nội tại và với protocol/CLAUDE.md**: luật L1–L6 của soan-spec (mỗi số có đơn vị; mỗi mục tiêu chiếu vào một đường
   dẫn trong write set; mỗi tiêu chí có phép đo làm nó ĐỎ; tiêu chí khớp chuỗi qua đủ năm vế L6), thứ tự land, xung đột với
   #1240/#1210/hàng đợi `packet_loop.py` như đặc tả mô tả.
3. **Lỗ thiết kế**: cách nào một hồ sơ/biên bản vẫn lọt luật mới (L8, L-7, D2b, K1–K7) mà không có đo thật; định nghĩa "lời khai
   gate_output" có bỏ sót dạng nào đang có trong `ops/land/` không (đo, đừng đoán); thiết kế có thi công được trong write set đã
   khai không (vd `packet_loop.py` nạp module `ops/`; test mới có đăng ký CI không); ước lượng kích thước có hợp lý không.
4. Nhận xét về các câu hỏi Q1–Q5: chỉ nêu nếu khuyến nghị dựa trên số đo sai hoặc thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời của bạn (Markdown)
```
# VERDICT wp1236 r1 vòng 1
spec_sha256: <sha256 bạn đo được>
## Findings
- id: F01
  severity: P0|P1|P2|P3
  vi_tri: <mục/dòng trong SPEC.md>
  van_de: <một câu>
  bang_chung: <lệnh đã chạy + output rút gọn, hoặc trích dẫn>
  de_xuat: <sửa thế nào>
(...)
## Đã đo lại, khớp
- <liệt kê ngắn các con số đã kiểm và khớp>
KET_LUAN: approve | changes_requested
```
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2. P3 không chặn. Dòng `KET_LUAN:` phải là dòng cuối cùng.
