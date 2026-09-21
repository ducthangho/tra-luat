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

## Phép đo bản ĐÃ ĐẾN — kèm HAI phép đo SAI đã bị bắt

Đọc ngược thân comment qua API rồi so với bản đã gửi. Đo ở mức **BYTE**, không qua hàm nào có
chuẩn hoá ngầm:

| | byte | xuống dòng | kết thúc bằng |
|---|---|---|---|
| thân comment **ĐÃ ĐẾN** | **1078** | CRLF × 18, LF đơn 0 | `…20260921` — **không có LF cuối** |
| bản **ĐÃ GỬI** | **1061** | LF × 19 | `…20260921` + LF |
| ĐÃ ĐẾN sau khi đổi CRLF→LF | **1060** | LF × 18 | — |

`1060 ≠ 1061`. Lệch đầu tiên ở **offset 1060**, đúng chỗ hết phần chung: một dấu xuống dòng cuối
đã bị cắt ở đâu đó trên đường đi. **LỚP NÀO CẮT THÌ KHÔNG ĐO ĐƯỢC.** Bản trước của đoạn này khai
*"GitHub cắt"* — rộng hơn phép đo, và codex bắt (P2 trên #597, dòng 188): chủ kho **dán tay** văn
bản này, nên clipboard, trình duyệt hay chính ô nhập đều có thể cắt dấu ấy **trước** khi GitHub
nhận, và ba con số cùng ba băm dưới đây **tái hiện y hệt** dưới mọi khả năng đó — tức chúng không
có khả năng phân định. Muốn gọi tên thủ phạm thì phải có **thân yêu cầu thô** hoặc một đường ghi
độc lập bằng máy; lượt này không có. Nên câu đúng là *"khớp từng byte sau khi đổi CRLF sang LF
**và** sau khi tính một LF cuối bị cắt ở một lớp **chưa xác định**"* — không phải *"khớp từng byte
sau khi chuẩn hoá xuống dòng"*, cũng không phải *"GitHub cắt"*.
Tập ký tự phi-ASCII giống hệt: 43 cả hai bên.

Băm của **cả ba** thân, để lần sau không phải đoán:

| | sha256 |
|---|---|
| ĐÃ ĐẾN (nguyên bản, CRLF) | `f9b716734f8d6afb2e9fbebef9fbd10a4a101b40b28abef6130c3925e4df6e20` |
| ĐÃ ĐẾN (đã đổi sang LF) | `0e51b2f271f766bd7431228d827c27e3490a03e91ca231c62f90a7a3ac54b4df` |
| ĐÃ GỬI | `da8111b9cfdda3ce6a7b07411cae619b4c06e55b09d43bdd7380d08ac67b01f0` |

### Hai phép đo SAI, cùng MỘT hình dạng

**(1)** Lượt đầu khai *"CRLF trong bản đã đến: False"*. **Sai** — nó mở tệp ở chế độ **VĂN BẢN** của
Python, mà universal newlines dịch CR-LF thành LF **ngay lúc đọc**, nên phép kiểm ấy **không bao giờ
đỏ được**, bất kể dữ liệu. Thứ bắt được nó là cảnh báo của `git add`.

**(2)** Bản đầu của chính mục này khai *"khớp từng byte sau khi chuẩn hoá xuống dòng"*. **Sai một
byte** — phép so chạy `difflib` **sau khi `.rstrip("\n")` cả hai vế**, tức xoá đúng thứ đang cần đo.
Thứ bắt được nó là cross-review codex (P2 trên PR #597).

Cả hai đều là *chuẩn hoá làm mất bằng chứng rồi kết luận từ cái đã chuẩn hoá*, và **không lần nào
phép đo của phiên tự bắt được**. Chốt rẻ rút ra: **so bằng `sha256` của BYTE THÔ**, đừng so bằng một
hàm có chuẩn hoá ngầm bên trong (`open()` chế độ văn bản, `rstrip`, `splitlines`, so chuỗi đã strip).

**KHÔNG sửa comment gốc cho khớp** — comment là nguồn có thẩm quyền; sửa nó là **thay** bằng chứng
chứ không phải **vá**.

Chép nguyên văn thân comment dưới đây (xuống dòng đổi sang LF và thêm lại LF cuối mà GitHub đã
cắt — không đổi gì khác). Sửa tệp này
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
