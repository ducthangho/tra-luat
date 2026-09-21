# VERDICT — human_audited, packet #523 slice r12 (PR #585)

**BẢN CHIẾU. Nguồn có thẩm quyền là COMMENT trên GitHub, không phải tệp này.**

Với verdict của một MÔ HÌNH, quy ước của kho là ngược lại: tệp có băm trong kho là nguồn, comment là
bản chiếu. Ở lượt này ĐẢO CHIỀU — §8 neo `human_audited` vào **danh tính bền trên GitHub**, mà một
tệp trong kho không mang được danh tính ấy. Nên:

| | |
|---|---|
| nguồn có thẩm quyền | https://github.com/ducthangho/tra-luat/pull/585#issuecomment-5757310858 |
| tác giả | `ducthangho` · `author_association: OWNER` |
| thời điểm | `2026-09-21T08:04:17Z` |

## Phép đo bản ĐÃ ĐẾN — kèm một phép đo SAI đã bị bắt

Đọc ngược thân comment qua API rồi `diff` với bản đã gửi. Kết quả **sau khi chuẩn hoá xuống dòng**:
khớp từng byte, và tập ký tự phi-ASCII giống hệt (43 ký tự cả hai bên).

**Nhưng "sau khi chuẩn hoá xuống dòng" KHÔNG phải một câu trang trí, và lượt đo đầu đã đọc nhầm nó.**
Đo lại ở mức BYTE:

| | |
|---|---|
| thân comment ĐÃ ĐẾN | **1078 byte**, xuống dòng **CRLF** — **18 cặp**, 0 LF đơn |
| bản ĐÃ GỬI | **1061 byte**, **LF**, 0 CRLF |
| blob của tệp này | **LF** (git chuẩn hoá khi commit) |

Lượt đo đầu khai *"CRLF trong bản đã đến: False"*. **Sai.** Nó mở tệp ở chế độ VĂN BẢN của Python,
mà universal newlines dịch `\r\n` thành `\n` **ngay lúc đọc** — nên phép kiểm `"\r\n" in s` không
thể nào đúng, bất kể dữ liệu là gì. Một phép kiểm không bao giờ đỏ được thì không phải bằng chứng.
Thứ bắt được nó không phải phép đo nào của tôi mà là cảnh báo của git (*"CRLF will be replaced by
LF"*) lúc `git add`. Cùng lớp bài học *"phải biết mình đang đứng ở LỚP NÀO"*: lần này cái lớp làm
mình mù chính là hàm `open()`.

Nên câu đúng là: **nội dung khớp từng byte; xuống dòng thì không, và khác biệt ấy đo được là 18 cặp
CRLF.** Không phải "khớp từng byte" trần trụi.

Chép nguyên văn thân comment dưới đây (xuống dòng đổi sang LF, không đổi gì khác). Sửa tệp này
**không** đổi được verdict — phải sửa ở comment.

---

## VERDICT — human_audited · approve

Reviewed commit: 27283d2e6ed57a6e97bf45e3179c157a59f0ff86

Tôi đã tự đọc trọn diff hai tệp trên đúng head này (`a1bbdc1..27283d2`, +201/−0,
`.claude/skills/cross-review/SKILL.md` và `.claude/skills/work-packet/SKILL.md`) và đọc đặc tả r12
(`sha256 9fc90435ad7c8b4ae93d19f8b163c5cffca9168e3df6043d8fe54ab880fe8059`). Không phải đọc bản tóm
tắt của executor — S14 của r12 loại trừ cách ấy.

Chấp nhận slice theo Review Rescue Checkpoint §12, đường (a): bốn lớp mở chuyển thành nợ (#582,
#583) và KHÔNG được vá trong slice này.

Khai thẳng phạm vi chữ ký này: nó xác nhận "tôi đã đọc và chấp nhận". Nó KHÔNG phải một lượt dò tìm
— reviewer của r6–r11 dựng phép đo, lượt này thì không. Đừng đọc approve ở đây thành "đã qua cùng
mức soi như các lượt trước".

assurance_target: human_audited
review_class: sensitive
lease: quy-trinh-lap-review-r12-exec-12-claude-20260921
