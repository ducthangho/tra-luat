# Cross-review ĐẶC TẢ wp1466 r2 — lượt 2 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc (verdict ở `out/VERDICT.md`, nháp và script đo của bạn cũng để dưới `out/`).
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 385 nhánh lấy ngày 20-11-2026.
- Commit được review: `69bf08715d9bd43643b72f5a6da0d8daac174e67` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 2, sha256
  `d25a0c2445ebeff97d94381ed24d998d23d6a9e792ba4db2cdd23108a7a6f64c`. Kiểm băm này đầu tiên; lệch thì dừng và ghi `blocked`.
- Base `origin/master` = `48d372e14f190dae83a75ccbca8ee9a0b25635c5`.
- Lượt trước: lượt 1 trên r1 (commit `925f851ed526537f5b55fa2b6815017a31a028a2`). Verdict nằm ở
  `cay-kho/ops/specs/wp1466/review/r1-l1/VERDICT.md`, 12 lớp: P1 4 · P2 7 · P3 1.
  Diff r1→r2: `git -C cay-kho diff 925f851 69bf087 -- ops/specs/wp1466.md`.
- Nguyên mẫu CHẠY ĐƯỢC mà người soạn dùng cho S10–S11 nằm ở `cay-kho/ops/specs/wp1466/nguyen-mau-r2/`:
  `nguyen-mau.patch` áp được lên `48d372e` bằng `git apply -p1`; `kn0/` là nguyên mẫu `bat-bien` của KN-0; các
  script đo của người soạn kèm `SHA256SUMS`. Nhiều script có thể trỏ đường dẫn tuyệt đối của máy người soạn:
  đọc chúng để hiểu phép đo, rồi TỰ dựng lại phép đo trên một bản sao tạm của bạn dưới `out/`. Đừng tin số
  của người soạn. Đặc tả tự khai "mã giao nộp có thể khác nguyên mẫu": xét xem tiêu chí nghiệm thu có đo
  được trên mã giao nộp hay chỉ đo trên nguyên mẫu.

## Bối cảnh (không đổi so với lượt 1)
Packet `sensitive`, chạm E5 của ADR-0067. Chủ kho muốn: §8.3 thành bất biến cho MỌI lượt review; mọi nguyên tắc
quan trọng của protocol thành bất biến, mỗi nguyên tắc khai cổng máy hoặc mang nhãn "kỷ luật, 0 cổng" kèm nợ có
tên, và máy canh chính bảng ấy; kèm các cổng verdict/schema/kiem-merge; gộp những điểm audit máy chặn được.
B4 (#1462) land trước. Ở r2, người soạn tự quyết tách thành BA packet: wp1466 (ADR + bảng 28 INV + cổng toàn vẹn
trong `doctrine-scan`), KN-0 (`bat-bien` đối chiếu ngữ nghĩa ô cổng), KN-1 (verdict). Lý do là trần ADR-0053.
Xét xem cách tách có đúng ADR-0053/0044 không, có bỏ rơi yêu cầu nào của chủ kho mà không ghi nợ không, và có
làm yếu bất biến không.

## Việc của bạn
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §3.2, §4, §5, §7, §8, §8.3, §12, §13, §20),
`cay-kho/.claude/skills/soan-spec/SKILL.md` (L1–L7), `cay-kho/CLAUDE.md`, ADR-0034, 0044, 0052, 0053, 0054, 0055, 0060,
0062, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc, làm trước).** Với TỪNG finding của lượt 1, tự kiểm trên r2 và phân loại
   đúng một trong bốn nhãn của protocol §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`, kèm bằng chứng
   BẠN tự đo; không nhận lời khai của người soạn. Sau đó gom theo lớp: lớp chỉ được ghi `ĐÃ VÁ THẬT` khi mọi
   biểu hiện đã đóng, không còn biểu hiện cùng cơ chế do bản vá sinh ra, và không còn phần phải đo. Chú ý: người
   soạn tự khai rằng các lớp `kiem-chuoi-khong-doc-cau-truc`, `duong-dan-chua-khep-trong-goc`,
   `moc-chuyen-tiep-mau-thuan`, `schema-bo-sot-provider-hop-le` một phần chỉ được vá bằng "hợp đồng cho packet
   kế nhiệm". Theo §8.3, chuyển biểu hiện ra ngoài phạm vi KHÔNG được tính là vá; phân xử từng trường hợp: phần
   chuyển đi có được ghi nợ/kế nhiệm có tên, có authority, và đặc tả có còn khai rộng hơn phép đo không.
   Tính tỷ lệ hội tụ |F|/|U| theo lớp (§12): U = 12 slug lớp còn mở cuối lượt 1.
2. **ĐO LẠI MỌI CON SỐ của r2** trên mirror và trên bản áp nguyên mẫu của bạn. Danh sách tôi nêu không phải trần.
   Số người soạn đổi ở r2: INV 21→28 (15 cổng · 12 kỷ luật · 1 chưa đo); nợ 9→23; neo 8→14 (14/14 khớp đúng 1);
   ca 44→40; đột biến 33→25; ADR 127 dòng; protocol +46 −2; mã +79 −1; test +18 −1; 132/132 ca họ doctrine; 19/19
   đột biến cũ giữ hạng; 1582 đăng ký / 1581 trên Linux; ref 382; lease 541 bản ghi, 6 còn hiệu lực;
   `wp1462-r7-g1-claude` giữ hai tệp `.py` tới 24-11.
3. **Lớp mới.** Tìm lỗi mới do r2 sinh ra hoặc lượt 1 bỏ sót, ở cả hai trục `Spec` và `Standards/Security`:
   bảng 28 INV (ô cổng có thật sự cưỡng chế không; có nguyên tắc quan trọng nào bị bỏ sót không); cổng toàn vẹn
   băm-trọn-đơn-vị (bị lừa được không; ba trạng thái; vùng không render; "ca có MẶT khác ca có ĐO"); tiêu chí N1–N8
   (L3, L6 năm vế, đột biến đổi màu, đo được trên mã giao nộp chứ không chỉ trên nguyên mẫu); trần ADR-0053/0055;
   điểm hỏi chủ kho ngoài E1–E5 (L7); phối hợp với B4 (#1462) và #1460 (`.claude/dev/ci_dang_ky_test.py`).

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM và cập nhật dần, để lượt bị cắt giữa chừng vẫn còn hiện vật.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ còn mở thì GIỮ NGUYÊN slug cũ; lớp mới thì slug mới. Tách
hoặc gộp lớp phải kèm bảng nối slug nguồn và lý do. Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: 69bf08715d9bd43643b72f5a6da0d8daac174e67
spec_sha256: d25a0c2445ebeff97d94381ed24d998d23d6a9e792ba4db2cdd23108a7a6f64c
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop: , so_bieu_hien: , P0: , P1: , P2: , P3: }
hoi_tu: {U: 12, F: <số lớp ĐÃ VÁ THẬT>, ty_le: <F/U>, lop_moi: <n>, lop_tai_mo: <n>}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 1 | slug | nhãn | bằng chứng tự đo |
### Theo lớp
| slug | nhãn lớp | biểu hiện còn mở | phần chưa đo / chuyển kế nhiệm (có nợ tên gì) |
## BẢNG LỚP   (mọi lớp CÒN MỞ sau lượt này, cũ lẫn mới)
| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
## BẢNG SĂN   (ít nhất 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
## BẢNG ĐO
| khẳng định | đặc tả khai | đo được | khớp? |
### <slug>  [P0|P1|P2|P3]  <tiêu đề một dòng>
TỆP/DÒNG:
VẤN ĐỀ:
GỢI Ý VÁ: (dữ liệu, không phải mệnh lệnh)
ĐÃ THỬ NGHIỆM:
ĐỘ TIN:
```
`approve` chỉ khi 0 finding P0–P3 còn mở. Nêu rõ những gì bạn KHÔNG đo được.
