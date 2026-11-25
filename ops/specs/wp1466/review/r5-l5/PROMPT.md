# Cross-review ĐẶC TẢ wp1466 r5 — lượt 5 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 392 nhánh lấy ngày 21-11-2026.
- Commit được review: `05d12f1e326a7822a8d94b699eee32926af3284c` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 5, sha256
  `5357004a67d83528dc903d6a29a989eeedc373d21ec4812d453db95320ef84f4`. Kiểm băm này đầu tiên; lệch thì dừng, ghi `blocked`.
- Base của đặc tả: `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. `origin/master` nay ở `5a152c1`; người soạn khai đã áp
  nguyên mẫu lên đó và `doctrine-scan`/`adr-song` đều rc 0. Kiểm lại, và kiểm xem master mới có chạm tệp nào đặc tả đo không.
- Lượt trước là lượt 4 trên r4, commit `937d135d903fe71a1660b138ebb2234cbc10bdbc`. Verdict:
  `cay-kho/ops/specs/wp1466/review/r4-l4/VERDICT.md`. Bảng (i) còn 3 lớp P2, 5 nhóm biểu hiện; bảng (ii) có 4 lớp nợ
  kế nhiệm. Các lượt 1–3 nằm ở `r1-l1/`, `r2-l2/`, `r3-l3/`. Diff r4→r5:
  `git -C cay-kho diff 937d135 05d12f1 -- ops/specs/wp1466.md`.
- Nguyên mẫu r5: `cay-kho/ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch`, áp lên `48d372e` bằng `git apply -p1`,
  4 tệp, numstat +434 −4. Kèm script đo của người soạn ở `nguyen-mau-r5/sc/` và báo cáo `bao_cao.txt`. Script có thể
  trỏ đường dẫn tuyệt đối trên máy người soạn: đọc để hiểu phép đo, rồi TỰ dựng lại trên bản sao tạm dưới `out/`.
  Đừng tin số của người soạn.

## Sự kiện từ lượt 4
1. **Người soạn r5 là Opus 5.5**, không phải Fable 5.2. Chủ kho quyết theo E2 vì Fable hết hạn mức. Reviewer vẫn là
   Codex. Kiểm xem đặc tả ghi đúng việc đổi này và không vì thế mà đổi executor hay assurance.
2. **Cách chấm bảng (i)/(ii) giữ nguyên như lượt 4.** Lượt 4 đã đồng ý cách đọc §8.3 ấy. Ở đối chiếu lượt trước, vẫn
   gán đúng bốn nhãn cho mọi lớp, kể cả 4 lớp bảng (ii); không ghi `ĐÃ VÁ THẬT` cho phần đã chuyển kế nhiệm. Chỉ bảng
   (i) quyết định verdict. Biểu hiện chỉ vào bảng (ii) khi đủ ba điều kiện: wp1466 không còn lời hứa hay tiêu chí nào
   chạm tới; nợ có tên; Issue kế nhiệm được nêu. Thiếu một thì ở bảng (i).
3. **Checkpoint §12 đã ghi sổ ở lượt 3.** Các lớp có mặt từ lượt 1 nay là lần thứ năm. Báo danh sách ấy như lượt
   trước; đừng coi việc lặp lại là lý do riêng để đổi verdict, nhưng nếu thấy cách làm vẫn sai gốc thì nói thẳng.
4. **Lớp `tien-kiem-lease-chua-du`:** lượt 4 nói nợ chưa có Issue kế nhiệm. R5 chọn hướng khác: đưa tiền kiểm thành
   điều kiện bắt đầu 3a–3f của chính wp1466, kèm khối `tien-kiem` fail-closed; nợ INV-02 giữ cho ca tổng quát và
   wp1466 khai không dựa vào nó. Xét xem như thế có đóng thật lớp ấy trong bảng (i) không.

## Việc của bạn
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §3.2, §4, §5, §7, §8, §8.3, §12, §13, §20),
`cay-kho/.claude/skills/soan-spec/SKILL.md` (L1–L7), `cay-kho/CLAUDE.md`, ADR-0034, 0044, 0052, 0053, 0054, 0055, 0060,
0062, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (làm trước).** Với TỪNG nhóm biểu hiện còn mở cuối lượt 4, ở cả hai bảng, tự kiểm trên r5
   và gán một trong bốn nhãn, kèm bằng chứng BẠN tự đo. Gom theo lớp. Tính |F|/|U| với U = 3 (lớp bảng (i) cuối lượt 4).
   Báo riêng lớp mới và lớp tái mở. Kiểm cả 4 lớp bảng (ii): r5 có vô tình thêm lời hứa nào kéo chúng về bảng (i) không.
2. **ĐO LẠI MỌI CON SỐ của r5** trên mirror và trên bản áp nguyên mẫu. Người soạn khai, trong số đó:
   - numstat 434 dòng / trần 450, 4 tệp; ruff F 16→16;
   - 190/190 ca; đột biến mới 26/26, đột biến cũ 21/21;
   - `kiem-chuoi`: 48/48 phản chứng lượt 4 ra đúng; `tieu-chi`: 65/65 biến thể N8; `tien-kiem`: 19/19 kịch bản;
   - 392 nhánh; 5 lease còn hiệu lực trên 549 bản ghi;
   - trên `5a152c1`: `doctrine-scan` rc 0, `adr-song` 67/67; sổ `CASES` 1582→1639, `MUTANTS` 1864→1890.

   Danh sách này không phải trần.
3. **Săn lớp mới** ở cả hai trục `Spec` và `Standards/Security`, nhất là trong các thiết kế mới của r5:
   - **Băm trên byte thô, biên là dòng rỗng 0 byte, đơn vị phải hiển thị tại địa chỉ:** có bị lừa không; có chặn oan
     tệp hợp lệ không (ví dụ CRLF hợp pháp, BOM, dòng cuối không xuống dòng); giá đổi có khai đúng không.
   - **ID so sau NFKC và bỏ ký tự Cf:** có làm hai ID khác nhau thành một không; người soạn khai chưa đo chữ cùng hình
     khác hệ chữ, hãy xét tầm quan trọng.
   - **N8 theo ngữ pháp đóng F/A/R, mẫu CHEN, `compile`:** đo được trên mã giao nộp không; ngữ pháp đóng có quá chặt
     làm executor không viết nổi H hợp lệ không; có binding nào còn lọt không.
   - **Khối `so-dang-ky`** và việc tăng sổ `CASES`/`MUTANTS`: có đụng #1460 (`.claude/dev/ci_dang_ky_test.py`) không.
   - **Điều kiện bắt đầu 3a–3f và khối `tien-kiem`:** ba trạng thái, fail-closed khi policy vắng, so tập ref, đo lại
     sau đăng; có cửa sổ hai writer nào còn hở; có tự mâu thuẫn với điều kiện C5 (merge thẳng master) không.
   - Ba quyết định D5, D9, D12 người soạn tự chốt không gắn mã E: có cái nào thật ra là điểm chủ kho phải quyết (L7) không.
   - Ngoài ra kiểm L3, L6 năm vế, trần ADR-0053/0055, phối hợp với B4 (#1462) và #1460.

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM với đủ khung và bảng đối chiếu, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ giữ slug cũ. Tách hay gộp lớp phải kèm bảng nối.
Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: 05d12f1e326a7822a8d94b699eee32926af3284c
spec_sha256: 5357004a67d83528dc903d6a29a989eeedc373d21ec4812d453db95320ef84f4
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: 3, F: , ty_le: , lop_moi: , lop_tai_mo: , lop_lan_thu_nam: [<slug>...]}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 4 | slug | nhãn | bằng chứng tự đo |
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
