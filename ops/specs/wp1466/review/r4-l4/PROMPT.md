# Cross-review ĐẶC TẢ wp1466 r4 — lượt 4 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 388 nhánh lấy ngày 21-11-2026.
- Commit được review: `937d135d903fe71a1660b138ebb2234cbc10bdbc` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 4, sha256
  `d248c37823e4b07a89fcc652b79c345e375337beeb5f76e21db719f6f64d4b13`. Kiểm băm này đầu tiên; lệch thì dừng, ghi `blocked`.
- Base của đặc tả: `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. `origin/master` nay ở `e02d748`; kiểm xem nó có chạm tệp nào
  đặc tả đo không.
- Lượt trước là lượt 3 trên r3, commit `b0079956d230ccb09b1c1d48f5a2633aaf09a173`. Verdict:
  `cay-kho/ops/specs/wp1466/review/r3-l3/VERDICT.md`, 9 lớp còn mở (P1 1 · P2 8). Lượt 1 và lượt 2 nằm ở `r1-l1/` và `r2-l2/`.
  Diff r3→r4: `git -C cay-kho diff b007995 937d135 -- ops/specs/wp1466.md`.
- Nguyên mẫu r4 chạy được: `cay-kho/ops/specs/wp1466/nguyen-mau-r4/nguyen-mau.patch`. Nó áp được lên `48d372e` bằng
  `git apply -p1`, gồm 4 tệp, numstat +395. Kèm script và log của người soạn. Đọc để hiểu phép đo, rồi TỰ dựng lại trên
  bản sao tạm dưới `out/`. Đừng tin số của người soạn.

## Sự kiện từ lượt 3 (bản chép quyết định nằm trong đặc tả; bạn không mở được URL)
1. **Checkpoint §12 đã kích hoạt.** Phiên điều phối đã tự xét lại cách làm và ghi sổ `xet_lai_cach_lam` theo ADR-0067.
   Hướng mới:
   - (a) Lớp có biểu hiện còn lại nằm ở packet kế nhiệm #1469/#1470: wp1466 bỏ MỌI lời hứa và mọi tiêu chí về
     chúng. Chủ kho đã duyệt tách packet (E2), nên #1469/#1470 là packet đề xuất có authority.
   - (b) Khoá văn bản theo danh sách cho phép cấu trúc: địa chỉ, cộng duy nhất, cộng băm byte.
   - (c) N8 so cấu trúc AST.
   - (d) Thu hẹp lời khai tiền kiểm lease về đúng phép đo hiện có.
2. **Cách chấm phần chuyển kế nhiệm (theo cách phiên điều phối đọc §8.3).** §8.3 nói: chuyển biểu hiện ra ngoài scope
   KHÔNG được tính là vá; ghi phần successor và authority riêng; giữ slug trong lịch sử.
   - Ở ĐỐI CHIẾU LƯỢT TRƯỚC, vẫn gán đúng bốn nhãn cho các lớp ấy. Không được ghi `ĐÃ VÁ THẬT` cho phần đã chuyển đi.
   - Ở BẢNG LỚP, tách thành hai bảng: (i) **lớp MỞ của wp1466**, tức có biểu hiện mà chính wp1466 hứa hoặc chạm tới;
     (ii) **nợ kế nhiệm có authority**, tức biểu hiện chỉ còn nằm trong phạm vi #1469/#1470 và wp1466 không khai gì
     về nó.
   - Chỉ bảng (i) quyết định verdict của wp1466. Một biểu hiện chỉ được vào bảng (ii) khi đủ ba điều kiện: wp1466 thật
     sự không còn lời hứa hay tiêu chí nào chạm tới nó; nợ có tên rõ; và Issue kế nhiệm được nêu. Thiếu một điều kiện
     thì nó ở bảng (i).
   - Nếu bạn cho rằng cách đọc §8.3 này SAI, ghi thành một finding riêng có lập luận. Đừng âm thầm bỏ qua.
3. **C5 đã được chủ kho quyết (E5): merge thẳng master.** Phạm vi chỉ gồm #1466, #1469, #1470, không gồm B4. Điều kiện
   lease: merge của packet trước nằm trên first-parent master và base chứa merge ấy. Kiểm xem đặc tả chép đúng và
   không mở rộng phạm vi ấy.

## Việc của bạn
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §3.2, §4, §5, §7, §8, §8.3, §12, §13, §20),
`cay-kho/.claude/skills/soan-spec/SKILL.md` (L1–L7), `cay-kho/CLAUDE.md`, ADR-0034, 0044, 0052, 0053, 0054, 0055, 0060,
0062, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (làm trước).** Với TỪNG finding còn mở cuối lượt 3 (9 lớp), tự kiểm trên r4 và gán một
   trong bốn nhãn, kèm bằng chứng BẠN tự đo. Gom theo lớp. Tính |F|/|U| với U = 9. Báo riêng lớp mới, lớp tái mở,
   và lớp đã có mặt ở bốn lượt.
2. **ĐO LẠI MỌI CON SỐ của r4** trên mirror và trên bản áp nguyên mẫu. Người soạn khai:
   - kích thước 395 dòng: ADR 143 · protocol +46 −2 · mã +74 −1 · test +132 −1;
   - ca 31; đột biến 18; nợ ADR 27;
   - vòng đột biến: nền 34/34, có ca kiểm mốc; 18/18 `ok`, `TỔNG: ĐẠT`; 21/21 đột biến cũ `ok`;
   - 164/164 ca và 40/40 `adr_song_*` đạt;
   - N8: chế độ `ma` 12 đỏ + 1 đạt, `test` 6 đỏ + 1 đạt.

   Danh sách này không phải trần.
3. **Săn lớp mới** ở cả hai trục `Spec` và `Standards/Security`, nhất là trong các thiết kế mới:
   - **Khoá có địa chỉ:** băm đường tiêu đề cộng thứ tự khối. Có bị lừa được không? Người soạn tự khai cái giá: thêm
     hay bớt một đoạn đứng trước K04/K05 sẽ làm cổng đỏ. Giá ấy có chấp nhận được không, có được khai đúng không?
   - **Băm byte không chuẩn hoá**, và chốt ID theo chuỗi ID trên mọi dòng có `|`.
   - **Mốc dựng bằng phép nối.**
   - **N8 dùng `ast.dump`:** đo được trên mã giao nộp không; có lỗ khi gán lại tên hay thêm decorator không.
   - **Lời khai thu hẹp của 3b.**
   - Ngoài ra kiểm L3, L6 năm vế, L7, trần ADR-0053/0055, phối hợp với B4 và #1460.

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM với đủ khung và bảng đối chiếu, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ giữ slug cũ. Tách hay gộp lớp phải kèm bảng nối.
Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: 937d135d903fe71a1660b138ebb2234cbc10bdbc
spec_sha256: d248c37823e4b07a89fcc652b79c345e375337beeb5f76e21db719f6f64d4b13
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: 9, F: , ty_le: , lop_moi: , lop_tai_mo: , lop_lan_thu_tu: [<slug>...]}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 3 | slug | nhãn | bằng chứng tự đo |
### Theo lớp
| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
## BẢNG LỚP (i) — lớp MỞ của wp1466
| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
## BẢNG LỚP (ii) — nợ kế nhiệm có authority
| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
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
`approve` chỉ khi bảng (i) có 0 finding P0–P3. Nêu rõ những gì bạn KHÔNG đo được.
