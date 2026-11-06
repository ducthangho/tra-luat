# Cross-review ĐẶC TẢ wp1236 r8 — vòng 2 của r8 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/work/`.
- Không tìm kết luận của reviewer khác (thư mục VERDICT vòng 1 của reviewer Claude đã bị gỡ khỏi sandbox bằng một commit cục bộ). Bạn có VERDICT vòng 1 r8 CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/VERDICT_VONG1_R8_CUA_BAN.md`. Bảng *Phản biện* cuối đặc tả tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả.
- Hướng thử nào đòi soạn nội dung tấn công (ngoài lệnh vô hại kiểu `false`, `true`, `python x.py` thoát 1) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả r8 (bản sửa sau vòng 1): `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/SPEC.md`, sha256 `a37c41a37dc4cdebabfbfa50777cc4bc3a5352f0618e5bde31945a0bceb5619c`. Kiểm sha256 trước tiên; lệch thì dừng và báo. Bản vòng 1 (`2a8c42e1…`) có trong lịch sử kho: `git show cf0ee8b:ops/specs/wp1236-r8.md`. Bản r7: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/SPEC_R7.md`.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/repo`, HEAD `a52954721ebeb29cff9e58e3fdade17d7b565929` = `cb394bc` (origin/master `d26b36f` + các commit chỉ thêm `ops/specs/wp1236-r8.md` và `ops/reviews/wp1236-r8-soan/`, `ops/reviews/wp1236-spec-r8-1-*`) + một commit sandbox gỡ VERDICT của reviewer kia. Lịch sử master đầy đủ, KHÔNG nông. Ref `refs/remotes/origin/claude/wp1236-a1-g1` (`508d678`, mã gen 1) chỉ để tham khảo/đo.
- Hiện vật đo của phiên soạn: `ops/reviews/wp1236-r8-soan/` (`gram.py`, `probes_r8.py`, `dot_bien_r8.py`, `census_r8.py`, `g1/` = phản chứng GỐC của generation 1 kèm sha256, `g1_qua_grammar.py`). Chạy lại bằng `python3 -I <script>` từ gốc kho.
- `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-codex/ISSUE.md`: thân #1236, chuỗi quyết định đợt A1, comment duyệt r7 (6676924904 — các P3 r7 chủ kho đã cho làm), quyết định ra r8 (6692008457), sáu comment connector trên PR #1260 (gồm 4495881317, 4495881327 mới).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) · `ops/ci_provenance.py` · `.github/workflows/ci.yml` · `docs/adr/0052*`, `0053*`, `0055*`, `0037*`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding vòng 1 CỦA BẠN** (kể cả P3 và các G cũ của r7): ĐÓNG / CÒN MỞ / HẾT ĐỐI TƯỢNG, kèm phép đo. Kiểm bản sửa có tạo lỗ MỚI không (đặc biệt: `F-ok` commit con của `fe84620`, A15 43/30/13, A20 (f)–(i′), Q-r8-4, ranh giới môi trường thừa kế, các vế/đột biến mới).
2. **Tính ĐÚNG của grammar K7-S** (như vòng 1): một thân `run` mà grammar nhận nhưng lỗi chương trình bị nuốt dưới đúng mẫu lệnh GitHub, trong môi trường sạch. Phần môi trường thừa kế nay là giới hạn khai (Q-r8-4) — chỉ nêu nếu cách khai sai hay thiếu.
3. **ĐO LẠI các con số MỚI hoặc ĐỔI**: 109 vế âm (106/2/1), 41 rc 0 = 36 nuốt thật + 5 không chạy; 7 dương; 53/53 đột biến; 52/52 vế gốc gen 1; ước 1850–2000, `tran_moi` 2050; 22/22 job J có `uses:` trước bước luật; R4a/R4b và `91686a6`. Số lệch là finding.
4. Mỗi chốt có ca và đột biến riêng? Có đột biến tương đương bị khai có răng, hay chốt nào không có vế đỏ (L3)?
5. Q-r8-1…4 và `tran_loi_goi_codex_A1_gen2`: chỉ nêu nếu dựa trên số đo sai, thiếu hệ quả, hay mâu thuẫn ADR.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r8 vòng 2
spec_sha256: <sha256 bạn đo được>
## Finding vòng 1 của tôi
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
