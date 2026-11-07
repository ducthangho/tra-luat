# Cross-review ĐẶC TẢ wp1236 r8 — vòng 4 (CUỐI) của r8 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/work/`.
- Không tìm kết luận của reviewer khác (thư mục VERDICT vòng 1–3 của reviewer Codex đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 3 r8 CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/VERDICT_VONG3_R8_CUA_BAN.md`. Bảng *Phản biện* cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.
- Hướng thử nào đòi soạn nội dung tấn công (ngoài lệnh vô hại kiểu `false`, `true`, `python x.py` thoát 1) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả r8 (bản sửa 3, sau vòng 3): `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/SPEC.md`, sha256 `5153cf17e3f5f73871fc0248db783919535b48df94b987f75594acd76924de8b`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`2a8c42e1…`, `git show cf0ee8b:ops/specs/wp1236-r8.md`) vòng 2 (`a37c41a3…`, `git show cb394bc:…`) và vòng 3 (`885017a6…`, `git show 97ed697:…`) có trong lịch sử kho. Bản r7: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/SPEC_R7.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/repo`, HEAD `a1c81b8f2d3eee6f59af50970206a1e0aaf661d5` = `2e7fab1` (origin/master `d26b36f` + các commit chỉ thêm `ops/specs/wp1236-r8.md`, `ops/reviews/wp1236-r8-soan/`, `ops/reviews/wp1236-spec-r8-{1,2,3}-*`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử master đầy đủ, KHÔNG nông. Ref `refs/remotes/origin/claude/wp1236-a1-g1` (`508d678`, mã gen 1) chỉ để tham khảo/đo.
- Hiện vật đo của phiên soạn: `ops/reviews/wp1236-r8-soan/` (`gram.py`, `probes_r8.py`, `dot_bien_r8.py`, `census_r8.py`, `g1/` = phản chứng GỐC của generation 1 kèm sha256, `g1_qua_grammar.py`). Chạy lại bằng `python3 -I <script>` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/ISSUE.md`: thân #1236, chuỗi quyết định đợt A1, comment duyệt r7 (6676924904 — các P3 r7 chủ kho đã cho làm), quyết định ra r8 (6692008457), sáu comment connector trên PR #1260 (gồm 4495881317, 4495881327 mới).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) · `ops/ci_provenance.py` · `.github/workflows/ci.yml` · `docs/adr/0052*`, `0053*`, `0055*`, `0037*`.

## Việc phải làm (theo thứ tự ưu tiên)
Đây là vòng 4/4, vòng CUỐI của ngân sách review spec r8. Hết vòng này mà còn P2 thì soạn giả DỪNG và trình chủ kho — nên mỗi P2 phải có phép đo
hoặc trích dẫn cụ thể, và nói rõ nó có chặn THI CÔNG hay chỉ là câu chữ.
1. **Từng finding vòng 3 CỦA BẠN**: ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo. Trọng tâm: hướng đổi phương pháp — **grammar NGUYÊN VĂN + ca A14-S0** (so byte sáu hằng, `flags`, kiểm `ast` không có đường nhận thứ ba) — có thật sự đóng lớp "cài đặt khác mà tưởng tương đương" không; còn đường nào để một module qua A14-S0 mà nhận khác tham chiếu (vd đọc hằng nhưng tiền xử lý `run` khác, gọi `RE_ONG.match`, bọc `fullmatch`)? Các đột biến LOGIC `cu_phap_run` (m-S1…S5, m-S16…S20) đủ chưa?
2. Harness A14-S6 bản vòng 3 (`sinh_r8.py`: nguyên byte, đường dẫn chữ, bash thật, pwsh giả chặt, ba lớp phân loại) và số đo: 61 530 / 2 647 / 0 / 0 / 0; 91/91 đột biến, 9 nuốt / 40 không chạy / 42 chỉ (a).
3. Tính ĐÚNG của grammar K7-S trong môi trường sạch.
4. Các sửa khác: `GIOI_HAN` ở B1/C1/D1 + m-*b, `kiem-ho-so` + m-A1c; 35 ký tự; 158 đột biến; ước 2050–2200, `tran_moi` 2300.
5. Q-r8-1…5 và `tran_loi_goi_codex_A1_gen2`: chỉ nêu nếu dựa trên số đo sai, thiếu hệ quả, hay mâu thuẫn ADR.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r8 vòng 4
spec_sha256: <sha256 bạn đo được>
## Finding vòng 3 của tôi
- H0x / G0x: ĐÓNG | CÒN MỞ | HẾT ĐỐI TƯỢNG — <một câu>
## Findings mới
- id: I01
  severity: P0|P1|P2|P3
  vi_tri: <mục/dòng trong SPEC.md>
  van_de: <một câu>
  bang_chung: <lệnh đã chạy + output rút gọn, hoặc trích dẫn>
  de_xuat: <sửa thế nào>
## Đã đo lại, khớp
- <liệt kê ngắn>
KET_LUAN: approve | changes_requested
```
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2. P3 không chặn. Dòng `KET_LUAN:` là dòng cuối cùng.
