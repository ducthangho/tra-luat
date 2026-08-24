verdict: changes_requested
reviewed_sha: ee545cf5afaa0b3286b3cf7fe13dd12ee1ec94f3
luot: 4

## ĐỐI CHIẾU LƯỢT TRƯỚC

- Lượt 1, các khẳng định chức năng và bảy ô: **ĐÃ VÁ THẬT** — đo lại trên head mới vẫn khớp cả bảy ô.
- Lượt 2, finding `ubuntu-leg-overclaim` trong mã: **ĐÃ VÁ THẬT** — mã head và khối r4 cùng băm `1ed3eb53770076d6`; câu mới đúng bằng phép chạy X2 cục bộ trên Linux, không rộng hơn và cũng không hẹp hơn. Ngày `23-08-2026` khớp neo thời gian của phép đo trong r3.
- Lượt 3, khẳng định nguồn đặc tả còn sai nhưng mã đã đúng: **VÁ HỜ** — r4 đóng đúng câu trong khối `t98`, nhưng phép quét mới phát hiện lời tương đương vẫn còn hiệu lực ở r2:215-216; vì vậy tuyên bố “sửa ĐÚNG MỘT lời khai” của r4 không đứng được.
- Không thấy bản vá lượt này sinh lỗi logic mới; lỗi mới được thấy là nợ nguồn cũ chưa được quét, đúng nợ `SPEC-QUET-LOI-KHAI` mà r4 tự khai.

## BẢNG ĐO

Tất cả số suite dưới đây đo sau khi áp bản vá môi trường Issue #296 **đối xứng** vào `cay-kho/` và `nen-f33c12d/`; chúng **không phải số pristine**. Smoke sau hiệu chỉnh là `98/98`; bản vá môi trường và mọi đột biến đã được hoàn nguyên, hai cây sạch.

| khẳng định | ai khai | đo được | khớp? |
|---|---|---|---|
| head/base | hồ sơ | `ee545cf5afaa0b3286b3cf7fe13dd12ee1ec94f3` / `f33c12db19e7bcc0b18b394635a142c9d45d671d` | có |
| NỀN | spec/executor | `97/97`, chạy 97, bỏ qua 0, rc=0 | có |
| NỀN + X2 | spec/executor | `97/97`, chạy 97, bỏ qua 0, rc=0 | có |
| VÁ | spec/executor | `98/98`, chạy 98, bỏ qua 0, rc=0 | có |
| VÁ + X1 | spec/executor | `89/90`, chạy 90, bỏ qua 8, rc=1, đỏ `t73` | có |
| VÁ + X2 | spec/executor | `97/98`, chạy 98, bỏ qua 0, rc=1, đỏ `t98` | có |
| VÁ + X1 · gỡ t70 | spec/executor | `88/89`, chạy 89, bỏ qua 8, rc=1, đỏ `t73` | có |
| VÁ + X2 · gỡ t70 | spec/executor | `96/97`, chạy 97, bỏ qua 0, rc=1, đỏ `t98` | có |
| delta toàn PR đúng hai tệp | executor | `ops/lease_publish_test.py`; `ops/specs/t33-doi-shellcheck-r4.md` | có |
| delta riêng lượt này chỉ thêm r4, không sửa r1/r2/r3 | executor | `git diff --name-status 3239279b..ee545cf5` chỉ `A ops/specs/t33-doi-shellcheck-r4.md` | có |
| spec r4 trong hồ sơ bằng byte tệp head | executor | cùng SHA-256 `4585dc2e4f5e27a1d7c5d463ea270c06d4fe369cd815297d1ff2fcb857317661` | có |
| khối `t98` r4 bằng byte khối 14 dòng trong mã | executor | cùng SHA-256 tiền tố `1ed3eb53770076d6` | có |
| r5 còn khoá `noi_da_duoc_cho_phep_ma_KHONG_dung` | yêu cầu review | YAML parse: khoá vắng; chỉ còn `noi_da_dung_o_r5` | không |
| write set r5 đúng hai path, diff nằm trọn | lease/executor | đúng hai path và bằng đúng hai path của diff | có |
| “rc=0 khi chạy cục bộ trên Linux” | r4/mã | X2 trên cây nền, worktree cục bộ, container Linux: `97/97`, rc=0 | đúng bằng |
| ngày của câu mới | r4/mã | r3 neo ma trận vào `10:0xZ 23-08-2026` | có |
| r2:215-216 “toàn bộ chân Ubuntu im lặng” | r2, vẫn hiệu lực | phép đo đứng sau chỉ là X2 tại worktree Linux `00d4b3d7`, `88/88`, rc=0; không có runner Ubuntu | rộng hơn |
| r1:77 “cả khi có lẫn khi vắng shellcheck” | r1 | hai phép actionlint cục bộ được nêu ngay trong câu | đúng bằng |
| r1:152 “39 biên nhận/0 F” | r1 | phạm vi, nguồn `master`, thời điểm và kết quả quét đều được nêu | đúng bằng |
| r2:82 “133 blob/180 ref” và r3:46 “0 trên 186 ref” | r2/r3 | nêu đối chiếu `ls-remote`/`for-each-ref` và `comm -23` rỗng | đúng bằng |
| r2:170 “3/5 workflow không cổng nào lint” | r2 | bảng kê đủ 5 workflow ngay trước câu | đúng bằng |
| r2:308 `t70` là ca duy nhất gọi thẳng | r2 | phép đo 4 occurrence và phân loại từng occurrence được nêu | đúng bằng |
| r4:93-94 “môi trường sạch” | r4 | hồ sơ chỉ tự khai sạch, không định nghĩa/receipt độc lập cho trạng thái thoáng qua #296 | KHÔNG XÁC ĐỊNH |
| r4:35 “PR #288 với 0 finding” | r4 | lease nêu phân bố `r2=0, r3=0, handoff=4`; không có GitHub trực tiếp trong sandbox | KHÔNG XÁC ĐỊNH |
| Windows thật | hồ sơ | sandbox không có runner Windows thật | KHÔNG ĐO ĐƯỢC |
| trạng thái GitHub trực tiếp | hồ sơ | chỉ có mirror/hồ sơ đóng băng, không có nguồn GitHub trực tiếp | KHÔNG ĐO ĐƯỢC |

### spec-source-second-ubuntu-leg-overclaim [P1] r4 sửa khối code nhưng bỏ sót cùng lời khai đang sống ở r2

TỆP/DÒNG: `ops/specs/t33-doi-shellcheck-r2.md:215-216`; hệ quả tự mâu thuẫn tại `ops/specs/t33-doi-shellcheck-r4.md:12,16,24-28,48-56,109-111`. · VẤN ĐỀ: r2 nói X2 làm “toàn bộ chân Ubuntu im lặng”, nhưng phép đo ngay trước nó chỉ chạy X2 trong worktree rời tại `00d4b3d7`, cho `88/88`, rc=0. r3 thay khối `ca_va_M3`, không thay đoạn phân tích này; r4 chỉ thay câu `r3:192`, nên lời rộng thứ hai vẫn nguyên hiệu lực. Vì vậy r4 tự mang khuyết tật nó sửa khi tuyên bố “sửa ĐÚNG MỘT lời khai”. Đây là hình dạng A tiếp theo trong khi A đã ở 8, ngưỡng DỪNG đã kêu; không thể approve một spec delta chưa đóng nguồn. · ĐÃ THỬ VÁ: tạo patch-as-hint tại `goi-va-293-luot4/ops/specs/t33-doi-shellcheck-r5.md`: hạ câu r2 xuống phép chạy cục bộ có tree, số và ngày; đồng thời bỏ tuyên bố duy nhất chưa được phép quét chứng minh. Tệp kế nhiệm cần lease/write set mới, reviewer không tự sửa branch executor. · ĐÃ THỬ NGHIỆM: đối chứng X2 trên cây nền mới (sau hiệu chỉnh #296) vẫn `97/97`, rc=0; `git diff --name-status` xác nhận r4 hiện không sửa/supersede r2; quét định lượng r1-r4 tìm được chính câu thứ hai. Nguy cơ của vá: delta kế nhiệm có thể mâu thuẫn tiếp nếu không chỉ rõ nó supersede đúng r2:215-216, và thêm path thứ ba sẽ vượt write set r5 hiện tại. · ĐỘ TIN: cao.

CAU_HOI_MOI_CUA_LUOT_NAY: Quét toàn r1/r2/r3/r4 để tìm lời khai khác rộng hơn phép đo; kiểm r4 có tự mang khuyết tật nó sửa; kiểm lease r5 đã thay chứ không giữ song song khoá cấm nới write set; kiểm delta lượt này không sửa đè r1/r2/r3.
