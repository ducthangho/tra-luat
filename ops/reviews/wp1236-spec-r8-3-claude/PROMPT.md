# Cross-review ĐẶC TẢ wp1236 r8 — vòng 3 của r8 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/work/`.
- Không tìm kết luận của reviewer khác (thư mục VERDICT vòng 1 và 2 của reviewer Codex đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 2 r8 CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/VERDICT_VONG2_R8_CUA_BAN.md`. Bảng *Phản biện* cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.
- Hướng thử nào đòi soạn nội dung tấn công (ngoài lệnh vô hại kiểu `false`, `true`, `python x.py` thoát 1) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả r8 (bản sửa 2, sau vòng 2): `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/SPEC.md`, sha256 `885017a688ae72fb479ee5e6234dd483f27182285b1f9d8a5b1ee3ee1adad1ee`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`2a8c42e1…`, `git show cf0ee8b:ops/specs/wp1236-r8.md`) và vòng 2 (`a37c41a3…`, `git show cb394bc:ops/specs/wp1236-r8.md`) có trong lịch sử kho. Bản r7: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/SPEC_R7.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/repo`, HEAD `487cc8702257869978c042a9943cafdfc4e1b193` = `97ed697` (origin/master `d26b36f` + các commit chỉ thêm `ops/specs/wp1236-r8.md`, `ops/reviews/wp1236-r8-soan/`, `ops/reviews/wp1236-spec-r8-{1,2}-*`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử master đầy đủ, KHÔNG nông. Ref `refs/remotes/origin/claude/wp1236-a1-g1` (`508d678`, mã gen 1) chỉ để tham khảo/đo.
- Hiện vật đo của phiên soạn: `ops/reviews/wp1236-r8-soan/` (`gram.py`, `probes_r8.py`, `dot_bien_r8.py`, `census_r8.py`, `g1/` = phản chứng GỐC của generation 1 kèm sha256, `g1_qua_grammar.py`). Chạy lại bằng `python3 -I <script>` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/ISSUE.md`: thân #1236, chuỗi quyết định đợt A1, comment duyệt r7 (6676924904 — các P3 r7 chủ kho đã cho làm), quyết định ra r8 (6692008457), sáu comment connector trên PR #1260 (gồm 4495881317, 4495881327 mới).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) · `ops/ci_provenance.py` · `.github/workflows/ci.yml` · `docs/adr/0052*`, `0053*`, `0055*`, `0037*`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding vòng 2 CỦA BẠN** (và finding vòng 1 còn mở): ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo. Kiểm bản sửa có tạo lỗ MỚI không — đặc biệt ca **A14-S6 kho sinh tổ hợp** (`ops/reviews/wp1236-r8-soan/sinh_r8.py`, `dot_bien_r8.py --sinh`): kho có thật sự phủ LỚP (mọi toán tử/ký tự ở mọi vị trí), tiêu chí (a) "bằng tham chiếu" và (b) "Bash thật trên mọi thân được nhận, từng thành phần ống" có đo đúng không, chương trình giả `bash`/`pwsh` có làm phép đo yếu đi không; dòng `GIOI_HAN` + m-A1b; A20 (e′); Q-r8-4 (c), Q-r8-5; câu `F-ok` thay G05.
2. **Tính ĐÚNG của grammar K7-S** trong môi trường sạch (như các vòng trước).
3. **ĐO LẠI các con số MỚI hoặc ĐỔI**: 11 838 đầu vào / 86 nhận / 0 lệch / 0 nuốt lỗi; 32/32 đột biến lớp I01 bị bắt, 13/32 có thân nhận mà nuốt lỗi; 109 = 106 chạy shell (41 + 65) + 3; số `uses:` theo tag; `:193`/`:226`; 14/24; 31/31; ước 1900–2050, `tran_moi` 2150. Số lệch là finding.
4. Mỗi chốt có ca và đột biến riêng? Đột biến tương đương khai có răng, chốt không có vế đỏ (L3)?
5. Q-r8-1…5 và `tran_loi_goi_codex_A1_gen2`: chỉ nêu nếu dựa trên số đo sai, thiếu hệ quả, hay mâu thuẫn ADR.
Đây là vòng 3/4 của ngân sách review spec r8. Chỉ nêu P2 khi có phép đo hoặc trích dẫn cụ thể.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r8 vòng 3
spec_sha256: <sha256 bạn đo được>
## Finding vòng 2 của tôi
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
