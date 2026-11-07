# Cross-review ĐẶC TẢ wp1236 r8 — vòng 5 (THÊM theo quyết định chủ kho 6700073306, CUỐI) của r8 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/work/`.
- Không tìm kết luận của reviewer khác (thư mục VERDICT vòng 1–4 của reviewer Codex đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 4 r8 CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/VERDICT_VONG4_R8_CUA_BAN.md`. Bảng *Phản biện* cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.
- Hướng thử nào đòi soạn nội dung tấn công (ngoài lệnh vô hại kiểu `false`, `true`, `python x.py` thoát 1) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả r8 (bản sửa 4, sau vòng 4): `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/SPEC.md`, sha256 `36bbcee68fcbbd5079a399f5cc8a8d00e179d6615272c7ed9754199da4b70b6c`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`2a8c42e1…`, `git show cf0ee8b:ops/specs/wp1236-r8.md`) vòng 2 (`a37c41a3…`, `git show cb394bc:…`) và vòng 3 (`885017a6…`, `git show 97ed697:…`), vòng 4 (`5153cf17…`, `git show 2e7fab1:…`) có trong lịch sử kho. Bản r7: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/SPEC_R7.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/repo`, HEAD `a419a01c8159c4e57f1d0901646db6bf7b964bff` = `3eb4be1` (nhánh gồm các commit chỉ thêm `ops/specs/wp1236-r8.md`, `ops/reviews/wp1236-r8-soan/`, `ops/reviews/wp1236-spec-r8-{1,2,3,4}-*`, cộng MỘT merge `origin/master` `9607e3e`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử master đầy đủ, KHÔNG nông. Ref `refs/remotes/origin/claude/wp1236-a1-g1` (`508d678`, mã gen 1) chỉ để tham khảo/đo.
- Hiện vật đo của phiên soạn: `ops/reviews/wp1236-r8-soan/` (`gram.py`, `probes_r8.py`, `dot_bien_r8.py`, `census_r8.py`, `g1/` = phản chứng GỐC của generation 1 kèm sha256, `g1_qua_grammar.py`). Chạy lại bằng `python3 -I <script>` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/ISSUE.md`: thân #1236, chuỗi quyết định đợt A1, comment duyệt r7 (6676924904 — các P3 r7 chủ kho đã cho làm), quyết định ra r8 (6692008457), sáu comment connector trên PR #1260 (gồm 4495881317, 4495881327 mới).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) · `ops/ci_provenance.py` · `.github/workflows/ci.yml` · `docs/adr/0052*`, `0053*`, `0055*`, `0037*`.

## Việc phải làm (theo thứ tự ưu tiên)
Đây là vòng 5, vòng THÊM duy nhất chủ kho cho (issuecomment-6700073306, cuối ISSUE.md). Còn P2 thì soạn giả DỪNG và trình chủ kho — nên mỗi
P2 phải có phép đo hoặc trích dẫn cụ thể, và nói rõ nó có chặn THI CÔNG hay chỉ là câu chữ.
1. **Từng finding vòng 4 CỦA BẠN**: ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo. Trọng tâm: bản sửa 4 — hàm `cu_phap_run` chép NGUYÊN VĂN và
   A14-S0 (5 vế: hằng; kiểu `re.Pattern` + `pattern`/`flags`; binding `__globals__` + cấm bóng tên; `ast.dump` thân hàm bỏ docstring; đúng một
   lời gọi `cu_phap_run(<b>.get("run"), <b>.get("shell"))`), A14-S3b, ba vế mới, m-S21…S26 (`ops/reviews/wp1236-r8-soan/khoa_ast_r8.py`).
   Còn đường nào để một module qua A14-S0 + các ca hành vi mà nhận khác tham chiếu không? Chốt có chặn oan một cài đặt hợp lệ không?
2. P3 đã sửa: 24 hạt, lấy mẫu 1/3; m-S0f; một ca đích mỗi đột biến; chi phí/POSIX của A14-S6; hằng `GIOI_HAN` xuất trong API; số vế 112/42/37;
   ước 2150–2300, `tran_moi` 2400.
3. Tính ĐÚNG của grammar K7-S trong môi trường sạch.
4. Merge `origin/master` không đưa tệp nào ngoài `ops/specs/**`, `ops/reviews/**` vào diff của nhánh.
5. Q-r8-1…5 và `tran_loi_goi_codex_A1_gen2`: chỉ nêu nếu dựa trên số đo sai, thiếu hệ quả, hay mâu thuẫn ADR.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r8 vòng 5
spec_sha256: <sha256 bạn đo được>
## Finding vòng 4 của tôi
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
