# Cross-review MÃ exact-H của wp1466: lượt 2 trên mã (reviewer: Codex, effort high)

Bạn là REVIEWER độc lập và CHỈ ĐỌC. Không được sửa kho, không push, không gọi API GitHub để ghi.
Chỉ ghi vào `out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng đặt dưới `out/`. Viết bằng tiếng Việt.

## Đối tượng
- **Kho:** `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`. Cây làm việc `cay-kho/`, ghim `core.abbrev 7`, đang detach tại H.
  Ref `refs/remotes/origin/*` là ảnh chụp ngày 26-11-2026.
- **Exact H:** `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2`, nhánh `claude/wp1466-r11-g3`, chưa push.
  - Kiểm `git -C cay-kho rev-parse HEAD` ĐẦU TIÊN. Nếu lệch thì ghi `blocked` rồi dừng.
- **Base:** `6a4f52dde37582df5c6a562e988d9551f45ae150` (master).
  - Diff cần review: `git -C cay-kho diff 6a4f52d c5d44c9`, gồm 4 tệp, +478 −4, chia 4 commit.
- **Đặc tả đóng băng r11:** `cay-kho/ops/specs/wp1466.md`, sha256 `9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910`.
  - Kiểm băm này TRƯỚC khi review. Lệch thì ghi `blocked`.
  - Đặc tả là nguồn sự thật. Ưu tiên đọc mục 0, 5, 8 (8.1–8.4), 9 (N1–N16), 10, 19.
- **Lease:** `wp1466-r11-g3-claude`, nhánh `origin/ops/wp1466-r11-g3-lease`, commit `ca001f8`.
  - Đọc bằng `git -C cay-kho show origin/ops/wp1466-r11-g3-lease:ops/leases/wp1466-r11-g3-claude.yaml`.
- **Handoff của executor (Claude Fable 5.2, high):** `exec-out/HANDOFF.md` (lượt 1), `exec-out/HANDOFF-l2.md`, `exec-out/HANDOFF-l3.md`, `exec-out/HANDOFF-l4.md` (lượt 4: mã do Fable 5.2, handoff viết nốt bởi Opus 5.5 vì Fable hết credit — chủ kho quyết E2).
  - Script đo của executor ở `exec-out/sc/`.
  - Đây là LỜI KHAI của executor. Hãy tự đo lại; đừng lấy danh sách của họ làm trần.
- **Review class:** `sensitive`. Assurance đích: `human_audited`; chủ kho audit exact-H sau review này.
- **Trần:** lời gọi này là lời gọi Codex thứ 13/13, tức lời gọi CUỐI (ADR-0055, nâng trần E2). Trần kích thước: ≤6 tệp / ≤500 dòng thêm theo khối `nang_tran` của đặc tả r11 mục 10 và của lease.

## Quyết định chủ kho đã có (bạn không mở được URL; nội dung tóm ở đây)
- **Q0 (E3) "Ra đặc tả r9":** bảng §1.1 bỏ backtick quanh con trỏ ca, băm K01 mới.
- **Q2 (E5) "Giữ bản vá":** thêm luật "phần đầu tệp" ở đặc tả mục 8.3.
- **Miễn Windows (C3, E2):** dòng `windows: <H> mien`.
- **Q3 (E3) "Thu hẹp lời hứa, chuyển #1469":** phép (3) chỉ đếm bản sao đứng thành đơn vị cùng loại; phần còn lại là nợ `INV-KHOA-BAN-SAO-DINH-CHU` (#1469). Đặc tả r11 mục 8.3 có câu giới hạn: wp1466 không đòi đỏ chỉ vì bản sao như thế, nhưng mọi điều kiện khác vẫn áp dụng.
- **E2 nâng trần 500** để đóng P3 `ca-id-chi-do-mot-gia-tri` (dòng G8 của r11).
- **Q4/E5:** dòng Trạng thái của ADR dẫn lần duyệt đặc tả hiện hành (r11): ngày `2026-11-27` (REST `created_at` `00:04:02Z`), URL `issuecomment-7206141143`.
- **Lượt trước trên mã:** `exec-out/VERDICT-ma-h-l1.md` (`blocked`: P2 `phep-dem-ban-sao-khong-phu-ca-tep`, P3 `ca-id-chi-do-mot-gia-tri`). Review đặc tả r10: `exec-out/VERDICT-spec-r10-l10.md`. ĐỐI CHIẾU LƯỢT TRƯỚC là bắt buộc: P2 phải ở bảng (ii) đủ ba điều kiện, KHÔNG được ghi ĐÃ VÁ THẬT; P3 phải được đo là đã đóng (ca và đột biến thật, kể cả mutant `rv_id_only_99` của reviewer lượt 1).

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
   - Ưu tiên `python3 -u -B .claude/dev/ci_dang_ky_test.py --chay` (sổ `CASES`/`MUTANTS` đã đổi ở lượt 4; executor chưa chạy trọn), so DELTA với base `6a4f52d`.
   - Lưu ý môi trường: `pretooluse_guard_test` đỏ SẴN 3 ca (t11, t15, t33) trên cả nền lẫn H trong container này, tức delta 0. Đừng tính thành finding nếu bạn đo được delta 0.
4. **Kiểm thẩm quyền và phạm vi.**
   - Chỉ 4 tệp thuộc write set được đổi.
   - Lease khớp H.
   - Ghi nhận việc executor lượt 1 đã đi vòng chốt ghi tệp bằng git plumbing. Nội dung kết quả vẫn nằm trong write set; ở lượt 2 và 3 executor dùng `git apply`. Hãy đánh giá xem việc này có để lại dấu vết nào trên H không.

Ghi `out/VERDICT.md` SỚM với đủ khung, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc)
```
verdict: approve | changes_requested | blocked
reviewed_sha: c5d44c93b4aa9326fa087af0bd07cbe918c2adc2
base_sha: 6a4f52dde37582df5c6a562e988d9551f45ae150
spec_sha256: 9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910
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
