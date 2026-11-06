# Cross-review ĐẶC TẢ wp1236 r8 — vòng 1 của r8 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/work/`.
- Không tìm kết luận của reviewer khác. Bạn có VERDICT vòng 7 (trên r7) CỦA CHÍNH BẠN: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/VERDICT_VONG7_CUA_BAN.md`.
- Hướng thử nào đòi soạn nội dung tấn công (ngoài các lệnh shell vô hại kiểu `false`, `true`, `python x.py`) thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả r8: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/SPEC.md`, sha256 `2a8c42e1d711e3c09281df6d36eb8c5a698c577ebad688e52e9ce0583c5828ff`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Bản r7 để so: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/SPEC_R7.md` (sha256 `31415a8a…`). r8 khai CHỈ đổi luật chốt shell của bước luật (mục *K7-S*) và những gì nó kéo theo; mọi thay đổi khác so với r7 mà không được khai là finding.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/repo`, HEAD `cf0ee8b1581c13aa3ab5377c444a43fe56b84b10` = origin/master `d26b36f` + hai commit chỉ thêm `ops/specs/wp1236-r8.md` và `ops/reviews/wp1236-r8-soan/`. Lịch sử master đầy đủ, KHÔNG nông. Có ref `refs/remotes/origin/claude/wp1236-a1-g1` (mã ứng viên generation 1 của đợt A1, đầu `508d678`) — chỉ để tham khảo/đo, KHÔNG phải nguồn luật.
- Hiện vật đo của phiên soạn: `ops/reviews/wp1236-r8-soan/` (`gram.py` cài đặt tham chiếu, `probes_r8.py` + json, `dot_bien_r8.py` + json, `census_r8.py` + txt). Chạy lại được bằng `python3 -I <script>` từ gốc kho.
- Thân Issue #1236 + chuỗi quyết định đợt A1 + bốn comment connector trên PR #1260: `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/ISSUE.md`. Quyết định ra r8 là comment CUỐI (6692008457) — không tranh luận lại hướng đã chọn, chỉ kiểm cách thi hành.
- Đọc thêm trong kho: `CLAUDE.md` (bài học "danh sách CẤM không bao giờ đủ", "ca có MẶT khác ca có ĐO", đột biến) · `docs/PROTOCOL_DA_PHIEN.md` (§8, §10.2.2) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) · `ops/ci_provenance.py` · `.github/workflows/ci.yml` · `docs/adr/0052*`, `0053*`, `0055*`, `0037*`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Tính ĐÚNG của grammar K7-S** — trọng tâm. Tìm một thân `run` (với `shell` vắng/`bash`/`sh`) mà grammar NHẬN nhưng một lỗi của chương trình được gọi KHÔNG làm bước thất bại dưới đúng mẫu lệnh GitHub (`bash -e {0}`, `bash --noprofile --norc -eo pipefail {0}`, `sh -e {0}`). Chạy Bash/sh thật trong `work/` với chương trình vô hại thoát 1. Xét cả: ký tự trong `W`/`P` có nghĩa đặc biệt nào không (`=`, `:`, `-`, `.`, `/`; từ đầu dòng; `--`); ba dạng `DANG`; ống; dòng cuối; Unicode; `${{ }}`; thứ tự đánh giá; tương tác với `chan_k7` (env/defaults/`BASH_ENV`…). Mỗi phản ví dụ là P1/P2.
2. **Đủ và đúng với quyết định 6692008457**: một dòng, một lệnh đơn, không toán tử ngoài đối số; ống chỉ với `shell: bash` và giữa lệnh đơn; còn lại `not_measured`; bỏ suy luận `set`/`errexit`; grammar là danh sách CHO PHÉP. Có chỗ nào r8 nới hơn (vd ba dạng `DANG`, đối số `W`) hay chặt hơn quyết định mà không khai thành câu hỏi cho chủ kho không?
3. **ĐO LẠI con số của r8**: 30/24/6 bước luật trên `ci.yml` ở `d26b36f` và `fe84620`, 25/5 ở `8983e1b`; 10/22 job J; 13 mục lý do của A15d; `luat_sha256` `ee0f2db8…`; 91 vế âm / 36 nuốt lỗi thật / 7 vế dương; 40/40 đột biến; ước kích thước 1750–1900 và căn cứ +1620 của `508d678`; số đếm `g_*` = 39, `kt_*` = 24. Số lệch là finding.
4. **Nghiệm thu đợt A1 sau r8**: `F-ok` + `VL-F` + `F-ok-goc` có dựng được và có làm A1 dương `passed` không (đối chiếu `ci.yml@fe84620` và mã/fixture của `508d678` nếu cần); A14-S1…S5, A15, A15d, A23; mỗi chốt có ca và đột biến riêng chưa, đột biến có răng không (đo trên `gram.py` hoặc bản sao), có đột biến TƯƠNG ĐƯƠNG bị liệt kê là có răng, hay chốt nào KHÔNG có đột biến; 16 biến thể lượt 8 + 10 biến thể lượt 9 + các probe connector có phủ đủ không, so với văn bản ISSUE.md.
5. **Mục *Kế thừa từ A1***: có đúng và đủ so với chuỗi VERDICT/quyết định trong ISSUE.md không (neo provenance, F09 chuỗi rỗng, F11 land dương đúng neo, chốt đếm > 0 ngoài luật, `luat_sha256` giữ nguyên, F01–F10).
6. `nang_tran` kích thước, `tran_loi_goi_codex_A1_gen2`, *Hệ quả trên ci.yml thật*, R1–R6, Q-r8-1…3: chỉ nêu nếu dựa trên số đo sai, thiếu hệ quả, hoặc mâu thuẫn ADR.
7. Luật soan-spec L1–L6 cho mọi tiêu chí mới.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r8 vòng 1
spec_sha256: <sha256 bạn đo được>
## Finding vòng 7 của tôi
- G0x: ĐÓNG | CÒN MỞ | HẾT ĐỐI TƯỢNG — <một câu>
## Findings mới
- id: H01
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
