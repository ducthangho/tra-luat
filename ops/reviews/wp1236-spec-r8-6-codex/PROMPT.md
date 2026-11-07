# Cross-review ĐẶC TẢ wp1236 r8 — vòng 6 (THÊM theo quyết định chủ kho 6700574797, CUỐI) của r8 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/work/`.
- Không tìm kết luận của reviewer khác (thư mục VERDICT vòng 1–5 của reviewer Claude đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 5 r8 CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/VERDICT_VONG5_R8_CUA_BAN.md`. Bảng *Phản biện* cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.
- Hướng thử nào đòi soạn nội dung tấn công (ngoài lệnh vô hại kiểu `false`, `true`, `python x.py` thoát 1) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả r8 (bản sửa 5, sau vòng 5): `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/SPEC.md`, sha256 `7c85e68e1ac5a5875925a4a48b7c5b691b146bbdcf4d740e274eb29ff09ab1c4`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`2a8c42e1…`, `git show cf0ee8b:ops/specs/wp1236-r8.md`) vòng 2 (`a37c41a3…`, `git show cb394bc:…`) và vòng 3 (`885017a6…`, `git show 97ed697:…`), vòng 4 (`5153cf17…`, `git show 2e7fab1:…`), vòng 5 (`36bbcee6…`, `git show 3eb4be1:…`) có trong lịch sử kho. Bản r7: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/SPEC_R7.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/repo`, HEAD `5244493221624ca9f521ff2af6cd0444746818a6` = `2c7f69c` (nhánh gồm các commit chỉ thêm `ops/specs/wp1236-r8.md`, `ops/reviews/wp1236-r8-soan/`, `ops/reviews/wp1236-spec-r8-{1..5}-*`, cộng MỘT merge `origin/master` `9607e3e`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử master đầy đủ, KHÔNG nông. Ref `refs/remotes/origin/claude/wp1236-a1-g1` (`508d678`, mã gen 1) chỉ để tham khảo/đo.
- Hiện vật đo của phiên soạn: `ops/reviews/wp1236-r8-soan/` (`gram.py`, `probes_r8.py`, `dot_bien_r8.py`, `census_r8.py`, `g1/` = phản chứng GỐC của generation 1 kèm sha256, `g1_qua_grammar.py`). Chạy lại bằng `python3 -I <script>` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/ISSUE.md`: thân #1236, chuỗi quyết định đợt A1, comment duyệt r7 (6676924904 — các P3 r7 chủ kho đã cho làm), quyết định ra r8 (6692008457), sáu comment connector trên PR #1260 (gồm 4495881317, 4495881327 mới).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) · `ops/ci_provenance.py` · `.github/workflows/ci.yml` · `docs/adr/0052*`, `0053*`, `0055*`, `0037*`.

## Việc phải làm (theo thứ tự ưu tiên)
Đây là vòng 6, vòng THÊM cuối cùng (issuecomment-6700574797, cuối ISSUE.md). Còn P2 sau vòng này thì chuyển sang HUMAN AUDIT của chủ kho,
không gọi thêm vòng nào — nên mỗi P2 phải có phép đo hoặc trích dẫn cụ thể, và nói rõ nó có chặn THI CÔNG hay chỉ là câu chữ.
1. **Từng finding vòng 5 CỦA BẠN**: ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo. Trọng tâm: bản sửa 5 của A14-S0 — vế (3) thuộc tính đối
   tượng hàm; vế (4) `ast` trên `inspect.getsource(module.cu_phap_run)`, bỏ docstring/`returns`, `decorator_list` rỗng; vế (5) gián điệp đối
   số so từng byte với `ci.yml` tại SHA checkout và năm thân đặc biệt (`khoa_ast_r8.py` → `main_v5`). Còn đường nào để một module qua A14-S0
   + các ca hành vi mà nhận khác tham chiếu? Có chặn oan cài đặt hợp lệ không? Có khả thi trong test không (getsource trên module nạp từ tệp)?
2. P3 đã sửa: A14-S3b 325 (112 + 7 + 206 mẫu `i % 299`); bảng disposition là ánh xạ chuẩn; `GIOI_HAN_K7S`; A14-S5 POSIX; cờ chế độ A14-S6.
3. Tính ĐÚNG của grammar K7-S trong môi trường sạch.
4. Q-r8-1…5 và `tran_loi_goi_codex_A1_gen2`: chỉ nêu nếu dựa trên số đo sai, thiếu hệ quả, hay mâu thuẫn ADR.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r8 vòng 6
spec_sha256: <sha256 bạn đo được>
## Finding vòng 5 của tôi
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
