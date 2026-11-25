# Cross-review ĐẶC TẢ wp1466 r3 — lượt 3 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 386 nhánh, lấy ngày 21-11-2026.
- Commit được review: `b0079956d230ccb09b1c1d48f5a2633aaf09a173` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 3, sha256
  `7b6457fda836f740e0d491bd0940532107fa9b4518c0eadf93522e4eb46ee454`. Kiểm băm này đầu tiên; lệch thì dừng và ghi `blocked`.
- Base của đặc tả là `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. `origin/master` nay là `010046f`; người soạn khai
  rằng nó không chạm tệp nào đặc tả đo. Hãy kiểm lại.
- Lượt trước là lượt 2 trên r2 (commit `69bf08715d9bd43643b72f5a6da0d8daac174e67`). Verdict:
  `cay-kho/ops/specs/wp1466/review/r2-l2/VERDICT.md`, 13 lớp còn mở (P1 4 · P2 9). Lượt 1:
  `cay-kho/ops/specs/wp1466/review/r1-l1/VERDICT.md`. Diff r2→r3:
  `git -C cay-kho diff 69bf087 b007995 -- ops/specs/wp1466.md`.
- Nguyên mẫu r3 chạy được: `cay-kho/ops/specs/wp1466/nguyen-mau-r3/nguyen-mau.patch`, áp được lên `48d372e` bằng
  `git apply -p1` (4 tệp, numstat +368), kèm script và log của người soạn. Script có thể trỏ đường dẫn tuyệt đối
  trên máy người soạn: đọc để hiểu phép đo, rồi TỰ dựng lại trên một bản sao tạm dưới `out/`. Đừng tin số của người soạn.

## Sự kiện mới từ lượt 2
- **Chủ kho đã duyệt tách 3 packet (E2)**, ghi hộ tại
  https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7053593553 . KN-0 là Issue #1469, KN-1 là Issue #1470;
  cả hai là packet ĐỀ XUẤT có thẩm quyền chủ kho, `depends_on [1462, 1466]`, nối tiếp. Bạn không mở được URL. Bản
  chép quyết định nằm trong đặc tả. Coi quyết định tách là đã có authority; nhưng theo §8.3, phần biểu hiện chuyển
  sang #1469/#1470 vẫn KHÔNG được tính là vá trong wp1466. Phần đó phải được cắt khỏi lời hứa của wp1466 và ghi nợ
  có tên. Kiểm xem r3 có làm đúng như thế không, hay vẫn khai rộng hơn phép đo.
- Người soạn nêu câu mới C5 (E5): nhánh nhận của chuỗi #1462 → wp1466 → #1469 → #1470 là `master` thay cho
  `mission/<issue>/integration` của §5. Xét câu này có mâu thuẫn protocol không, và có được khai đúng là điểm chủ
  kho quyết không.

## Việc của bạn
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §3.2, §4, §5, §7, §8, §8.3, §12, §13, §20),
`cay-kho/.claude/skills/soan-spec/SKILL.md` (L1–L7), `cay-kho/CLAUDE.md`, ADR-0034, 0044, 0052, 0053, 0054, 0055, 0060,
0062, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc, làm trước).** Với TỪNG finding còn mở cuối lượt 2 (13 lớp, gồm cả các
   biểu hiện), tự kiểm trên r3 và gán đúng một trong bốn nhãn của §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` ·
   `CHƯA VÁ`, kèm bằng chứng BẠN tự đo. Sau đó gom theo lớp. Tính |F|/|U| với U = 13 lớp còn mở cuối lượt 2.
   Báo riêng lớp mới, lớp tái mở, và lớp nào đã xuất hiện ở cả ba lượt (theo §12, đó là lần thứ ba).
2. **ĐO LẠI MỌI CON SỐ của r3** trên mirror và trên bản áp nguyên mẫu của bạn. Danh sách dưới không phải trần.
   Người soạn khai: 368 dòng (ADR 135 · protocol +46 −2 · mã +72 −1 · test +115 −1); 7 đơn vị khoá (§1.1, danh
   sách §1, §8.3, một đoạn §8, ba đoạn §12); 15/15 ô cổng mang `còn nợ`; ca 24; đột biến 17, vòng đột biến thật
   17/17 `ok`, `TỔNG: ĐẠT`; 21/21 đột biến cũ `ok`; 156/156 ca đạt; nợ ADR 26; lease B4 nay là `wp1462-r8-g2-claude`.
3. **Lớp mới** ở cả hai trục `Spec` và `Standards/Security`. Chú ý các thiết kế mới: khoá trọn 7 đơn vị (bị lừa
   được không; luật quan trọng nằm NGOÀI 7 đơn vị thì sao); N8 đo byte nút cũ bằng script nhúng (đo được trên mã
   giao nộp không); ca đổi tiền tố `doctrine_inv_` thay vì sửa bộ chọn (có phải lách bộ chọn không); 3b giao cho
   cổng I2(Đ) (cổng ấy có đọc đủ §5 không); N6/N7 theo tập bắt buộc cộng tập thêm. Kiểm thêm: L3, L6 năm vế, L7 (điểm
   hỏi ngoài E1–E5), trần ADR-0053/0055, phối hợp với B4 và #1460.

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM với đủ khung và bảng đối chiếu, rồi cập nhật sau mỗi phát hiện. Lượt trước từng bị đứt
mạng giữa chừng.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ còn mở thì GIỮ slug cũ; lớp mới dùng slug mới. Tách hoặc
gộp lớp phải kèm bảng nối slug nguồn và lý do. Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: b0079956d230ccb09b1c1d48f5a2633aaf09a173
spec_sha256: 7b6457fda836f740e0d491bd0940532107fa9b4518c0eadf93522e4eb46ee454
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop: , so_bieu_hien: , P0: , P1: , P2: , P3: }
hoi_tu: {U: 13, F: , ty_le: , lop_moi: , lop_tai_mo: , lop_lan_thu_ba: [<slug>...]}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 2 | slug | nhãn | bằng chứng tự đo |
### Theo lớp
| slug | nhãn lớp | biểu hiện còn mở | phần chưa đo / chuyển #1469/#1470 (nợ tên gì) |
## BẢNG LỚP   (mọi lớp CÒN MỞ sau lượt này)
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
