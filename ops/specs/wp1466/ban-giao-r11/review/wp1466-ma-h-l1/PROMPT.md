# Cross-review MÃ exact-H của wp1466: lượt 1 trên mã (reviewer: Codex, effort high)

Bạn là REVIEWER độc lập và CHỈ ĐỌC. Không được sửa kho, không push, không gọi API GitHub để ghi.
Chỉ ghi vào `out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng đặt dưới `out/`. Viết bằng tiếng Việt.

## Đối tượng
- **Kho:** `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`. Cây làm việc `cay-kho/`, ghim `core.abbrev 7`, đang detach tại H.
  Ref `refs/remotes/origin/*` là ảnh chụp ngày 26-11-2026.
- **Exact H:** `da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd`, nhánh `claude/wp1466-r9-g2`, chưa push.
  - Kiểm `git -C cay-kho rev-parse HEAD` ĐẦU TIÊN. Nếu lệch thì ghi `blocked` rồi dừng.
- **Base:** `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70` (master).
  - Diff cần review: `git -C cay-kho diff 695916e da4e876`, gồm 4 tệp, +443 −4, chia 3 commit.
- **Đặc tả đóng băng r9:** `cay-kho/ops/specs/wp1466.md`, sha256 `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c`.
  - Kiểm băm này TRƯỚC khi review. Lệch thì ghi `blocked`.
  - Đặc tả là nguồn sự thật. Ưu tiên đọc mục 0, 5, 8 (8.1–8.4), 9 (N1–N16), 10, 19.
- **Lease:** `wp1466-r9-g2-claude`, nhánh `origin/ops/wp1466-r9-g2-lease`, commit `c9a7a98`.
  - Đọc bằng `git -C cay-kho show origin/ops/wp1466-r9-g2-lease:ops/leases/wp1466-r9-g2-claude.yaml`.
- **Handoff của executor (Claude Fable 5.2, high):** `exec-out/HANDOFF.md` (lượt 1), `exec-out/HANDOFF-l2.md`, `exec-out/HANDOFF-l3.md`.
  - Script đo của executor ở `exec-out/sc/`.
  - Đây là LỜI KHAI của executor. Hãy tự đo lại; đừng lấy danh sách của họ làm trần.
- **Review class:** `sensitive`. Assurance đích: `human_audited`; chủ kho audit exact-H sau review này.
- **Trần:** lời gọi này là lời gọi Codex thứ 11/13 (ADR-0055, nâng trần E2). Trần kích thước theo ADR-0053 là ≤450 dòng thêm và ≤6 tệp.

## Quyết định chủ kho đã có (bạn không mở được URL; nội dung tóm ở đây)
- **Q0 (E3) "Ra đặc tả r9":** bảng §1.1 bỏ backtick quanh con trỏ ca, băm K01 mới.
- **Q2 (E5) "Giữ bản vá":** thêm luật "phần đầu tệp" ở đặc tả mục 8.3.
- **Q4 (E5) "Dẫn r9":** dòng Trạng thái của ADR-0068 dẫn lần duyệt r9, ngày `2026-11-26` (REST `created_at` `12:34:36Z`) với URL `issuecomment-7192181084`.
- **Miễn Windows (C3, E2):** dòng `windows: <H> mien`.
- **Q3 chưa quyết.** Đó là năm dạng bản sao không đứng thành đơn vị, ghi ở HANDOFF lượt 1 mục 8. Nếu bạn thấy đó là lỗ hổng so với chữ của đặc tả r9 thì báo thành finding, có hạng; đừng tự coi là nợ.

## Chỉ thị bắt buộc của chủ kho
ĐỌC NGUYÊN VĂN, không đọc theo trí nhớ:
- `cay-kho/.claude/skills/cross-review/SKILL.md`;
- `cay-kho/docs/PROTOCOL_DA_PHIEN.md` §7, §8, §8.3, §12;
- `cay-kho/docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (M1–M12), ADR-0062, ADR-0063;
- `cay-kho/CLAUDE.md`.

Những điểm cốt lõi:
- **Khái quát thành lớp trước khi báo.** Mỗi biểu hiện quy về MỘT lớp nguyên nhân, mang slug kebab-case ổn định. QUÉT mọi biểu hiện cùng lớp trên H rồi mới báo; không báo từng lỗi lẻ.
- **Bảng lớp** có các cột: slug, finding IDs/biểu hiện, hạng cao nhất còn mở, nguồn lượt/SHA, phương án vá chung, phép kiểm đóng lớp.
- Không gộp slug, không đổi hạng để giảm số lớp.
- **Điều kiện merge (M1):** không còn P0/P1/P2 mở. Mỗi P3 phải đóng có bằng chứng, hoặc được chủ kho miễn bằng một dòng `mien_p3`. Reviewer KHÔNG tự xếp P3 thành nợ.
- **Đo, đừng tin rc.** Đòi bằng chứng dương (`N/N` với hai số bằng nhau, `"ok": true`). Khai đủ đầu vào cho mọi cổng.

## Việc của bạn
1. **Đúng đặc tả từng byte.**
   - N1: ADR bằng khối `adr` sau khi thay chỗ trống theo 8.1.
   - N2: protocol bằng nền cộng đúng sáu khối p1–p6.
   - N5: dùng script CỦA RIÊNG BẠN, tự băm lại 7 đơn vị và so với khối `khoa` cùng hằng `INV_KHOA_PROTOCOL`.
   - N8: chạy khối `do-pham-vi` ở cả hai chế độ.
   - Khối `so-dang-ky`.
   - Đối chiếu số `{{N1}}`…`{{N6}}` trong ADR với lệnh ở mục *Cưỡng chế*.
2. **Hành vi cổng `doctrine-scan`.**
   - Phép (1)–(3) và luật "phần đầu tệp".
   - Chốt ID bất biến; chốt HTML.
   - Đọc byte thô; xử lý CR/BOM/U+2028/NBSP; che vùng không render.
   - Tìm đường vào chưa có ca hoặc đột biến. Hướng nào cần dựng nội dung tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI, đừng tự soạn payload.
   - Chạy các ca `doctrine_inv_*` và các vòng đột biến mới/cũ bằng cách bộ test cho phép (`packet_loop_test_manh.chay`; xem HANDOFF-l2 mục 5).
   - Đột biến bản vá để đo xem ca có răng thật không.
3. **Không phá cái cũ.**
   - Ca họ doctrine cũ và `adr_song_*`.
   - `python3 scripts/tl.py doc-claims-check --strict --json`.
   - `tl --selftest`.
   - ruff F, so delta với base; ngưỡng do người giữ, xem CLAUDE.md.
   - Các bước CI mà executor ghi là chưa đo: chạy được bao nhiêu thì chạy.
   - Lưu ý môi trường: `pretooluse_guard_test` đỏ SẴN 3 ca (t11, t15, t33) trên cả nền lẫn H trong container này, tức delta 0. Đừng tính thành finding nếu bạn đo được delta 0.
4. **Kiểm thẩm quyền và phạm vi.**
   - Chỉ 4 tệp thuộc write set được đổi.
   - Lease khớp H.
   - Ghi nhận việc executor lượt 1 đã đi vòng chốt ghi tệp bằng git plumbing. Nội dung kết quả vẫn nằm trong write set; ở lượt 2 và 3 executor dùng `git apply`. Hãy đánh giá xem việc này có để lại dấu vết nào trên H không.

Ghi `out/VERDICT.md` SỚM với đủ khung, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc)
```
verdict: approve | changes_requested | blocked
reviewed_sha: da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd
base_sha: 695916ea3bfffdd7b2e8fcb94b0740b3c421fe70
spec_sha256: 28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, effort: high, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Correctness, Tests, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude) — đích human_audited sau audit chủ kho
dem: {so_lop_mo: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: }

## BẢNG LỚP — lớp MỞ
| slug lớp | finding IDs/biểu hiện | hạng cao nhất còn mở | nguồn lượt/SHA | phương án vá chung | phép kiểm đóng lớp |
## BẢNG LỚP ĐÃ ĐÓNG/ĐÃ KIỂM (nếu có)
## BẢNG SĂN   (ít nhất 8 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
## BẢNG ĐO
| khẳng định (đặc tả/handoff) | khai | đo được | khớp? |
### <slug>  [P0|P1|P2|P3]  <tiêu đề một dòng>
TỆP/DÒNG:
VẤN ĐỀ:
CÁC BIỂU HIỆN CÙNG LỚP ĐÃ QUÉT:
GỢI Ý VÁ: (dữ liệu, không phải mệnh lệnh)
ĐÃ THỬ NGHIỆM:
ĐỘ TIN:
```
Chỉ được ghi `approve` khi không còn P0, P1 hay P2 nào mở và mọi P3 đều có bằng chứng đóng. Nêu rõ những gì bạn KHÔNG đo được.
