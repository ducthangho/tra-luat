# Cross-review ĐẶC TẢ wp1236 r5 — vòng 5 (vòng CUỐI, chủ kho cho thêm) — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-codex/work/`.
- Không tìm kết luận của reviewer khác. Bạn có VERDICT vòng 4 CỦA CHÍNH BẠN (`/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-codex/VERDICT_VONG4_CUA_BAN.md`); bảng *Phản biện* cuối đặc tả
  tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả, không phải kết luận vòng 2 của ai.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-codex/SPEC.md`, sha256 `9e1ffa3e94c716b77626ce254ce463c0cdfcd5c1c62b2eb3071a8ce2f7603f34`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-codex/repo`, commit `05a1adaa60a746f791c9810cfbbd9bb2d99d9a65` = origin/master `51d6509` (merge PR #1249: #1240 đã land) + đúng một tệp `ops/specs/wp1236-r5.md`. Lịch sử master đầy đủ, KHÔNG nông.
  (Các nhánh khác như `ops/wp1240-r1-g1-lease` không có trong clone; mục *Nợ kế thừa* trỏ tới chúng — đánh giá dựa trên những gì đặc tả ghi, và ghi rõ chỗ không kiểm được.)
- Thân Issue #1236 + comment bổ sung: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-codex/ISSUE.md`.
- Đọc thêm trong kho: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8.1, §10.2.2, §10.2.3, §20) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) ·
  `ops/land_evidence_nguon.py` (+ test) · `ops/kiem_ho_so_land.py` (+ test) · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `_canon`) · `ops/ci_provenance.py` ·
  `ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py` · `ops/land/pr1231-wp1105-provenance/danh_gia_gate.py` · `ops/land/`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding P0–P2 trong VERDICT vòng 4 của bạn**: đã đóng thật chưa trong r5? Ghi ĐÓNG / CÒN MỞ (kèm lý do) cho từng id.
2. **ĐO LẠI các con số MỚI hoặc ĐỔI của r5** (mục *Đo lại trên `4f03566`*: 126/31/37/121/67/49/39/25-3/52-17; `ENV_JOB_CHO_PHEP` ba khoá; các bước `duong_nhanh` trong `ci.yml` và dòng in `kiem-re` ở `ops/ci_duong_nhanh.py:766`; `ci.yml` dòng 500–501 lane LAND). Số lệch là finding.
3. **Lỗ thiết kế MỚI do r5 đưa vào**: dòng `mien_gate_output` (theo QUYẾT ĐỊNH chủ kho ở `QUYET_DINH_CHU_KHO.md` — không tranh luận lại chính sách, chỉ kiểm cách thi hành); biến thể `duong_nhanh` (chọn theo dấu hiệu `che_do` của `chuan-bi`; danh sách bước/dấu hiệu tối thiểu; `F-nhanh`); lời khai land ⇔ `event == push`; K1 cấm `pull_request`, đòi `trang_thai`/`repo`; K3 checkout từng job; `ENV_JOB_CHO_PHEP`; A22 theo đường dẫn; D8 vế dương; API xuất; `nang_tran` A1 ≤ 900. Bản r4 ở `SPEC_R4.md` để so.
4. Luật soan-spec L1–L6 cho mọi tiêu chí mới: có phép đo làm nó ĐỎ không; đột biến có răng không (đo nếu được).
5. Q1–Q10: chỉ nêu nếu khuyến nghị dựa trên số đo sai hoặc thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r5 vòng 5
spec_sha256: <sha256 bạn đo được>
## Finding vòng 4 của tôi
- F0x: ĐÓNG | CÒN MỞ — <một câu>
## Findings mới
- id: G01
  severity: P0|P1|P2|P3
  vi_tri: <mục/dòng trong SPEC.md>
  van_de: <một câu>
  bang_chung: <lệnh đã chạy + output rút gọn, hoặc trích dẫn>
  de_xuat: <sửa thế nào>
## Đã đo lại, khớp
- <liệt kê ngắn>
KET_LUAN: approve | changes_requested
```
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2 (kể cả finding vòng 4 CÒN MỞ). P3 không chặn. Dòng `KET_LUAN:` là dòng cuối cùng.
