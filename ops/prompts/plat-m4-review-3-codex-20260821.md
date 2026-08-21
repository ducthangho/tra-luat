# PROMPT REVIEWER — `PLAT-M4` (#194 / PR "#204"), lượt 3/3. Neo exact head `825e9704`.

Bạn là reviewer khác nền (codex) cho một packet do claude vá. **Read-only.** Kho nằm ở `./kho`;
mọi tệp bạn tạo phải nằm NGOÀI cây ấy. Chốt: `git -C kho status --short` phải RỖNG ở cuối lượt,
và HEAD phải vẫn là `825e97042b86f5e200c2ab8a00b58d8642510353`.

Đây là lượt **CUỐI** trong ngân sách đã được nâng. Trần vòng canon là 2
(`docs/adr/0043-tran-vong-review-canon-la-hai.md`); người giữ kho đã nâng 2→3 cho packet này, và
lời gọi 3→4 theo sau. Không có lượt bốn. `changes_requested` hoặc `blocked` ở đây ⇒ human
checkpoint, không tự mở thêm lượt.

## Ba thứ ĐÃ ĐỔI so với lượt 2 — đọc trước khi soi mã

**(1) Đặc tả nay CÓ TRONG CÂY.** Finding P1 của bạn ở lượt 2 (`ops/specs/plat-m4-v0.md` không tồn
tại, băm `KHÔNG ĐO ĐƯỢC`) là **lỗi của phiên dựng bundle, không phải lỗi của packet** — tệp lúc ấy
còn nằm trên một nhánh chưa merge. Nay nó đã vào master và có trong bản sao này:

```
ops/specs/plat-m4-v0.md
sha256 63ff22bcc2427850ddd66322ed4a5ac5dcaa03f8d242cc857d12825b601953d1
```

**Kiểm băm trước.** Lệch băm thì đó là finding, không phải chuyện vặt. Nếu tệp vẫn không có thì
KHAI THẲNG là `KHÔNG ĐO ĐƯỢC` như bạn đã làm — đừng đoán nội dung đặc tả.

**(2) Hai verdict trước cũng có trong cây**, đọc lại được:
`kho/ops/reviews/plat-m4-review-1-codex-verdict.md` · `kho/ops/reviews/plat-m4-review-2-codex-verdict.md`.

**(3) Bản vá của lượt này trả lời F2 và F3 của bạn.** Đừng tin lời khai ấy — đo.

## Việc

Delta cần soi: `git -C kho diff origin/master...HEAD` — **đúng hai tệp**,
`.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`, `+473/−25`. Ba tệp trở lên là finding.
(Nhánh có vài commit gộp master; delta ba-chấm ở trên đã loại phần gộp đó ra.)

1. **F2 đã đóng THẬT chưa** — "URL méo vẫn làm lộ bí mật qua mô tả". Bạn đã đưa bốn đầu vào:
   `http:///user:SENTINEL@host/mcp` · `javascript:user:SENTINEL@host` · `http ://user:SENTINEL@host/mcp`
   · `http://?u=user:SENTINEL@host`. Chạy lại **cả bốn** và khẳng định `desc_has_secret=false` cho
   từng cái. Rồi tự nghĩ đầu vào thứ năm mà bản vá này KHÔNG chặn — chú ý: bản vá đổi cả THỨ TỰ
   kiểm (userinfo trước scheme) chứ không chỉ đổi chuỗi thông báo, nên hãy tấn công thứ tự ấy.
2. **F3 đã đóng THẬT chưa** — "test chưa khoá biên cấu trúc của `userinfo`". Hai mutant bạn nêu:
   `if ai_ep != (None, None):` → `if "@" in str(url):`, và → `if p_ep.username:`. Cả hai lượt trước
   đều SỐNG SÓT. Đo lại xem nay chúng có bị giết không, và **tự thêm mutant thứ ba** mà bảng hiện
   tại không giết được.
3. **Bản vá có mở lỗ mới không.** `scheme` cũng là dữ liệu từ `url` — `urlsplit("GOCSPX-abc:x")`
   cho scheme `gocspx-abc`. Kiểm xem còn nhánh nào mang bất kỳ mảnh nào của `url` ra mô tả không.
4. **Lời khai có bằng phạm vi đo được không.** Docstring `t143` khai "TÁM điều" — đếm xem có đúng
   tám điều được ĐO không, hay chỉ được liệt kê. Lượt 2 đã bắt đúng lỗi này ở phiên bản "sáu điều".

## Bốn chốt của kho
1. Bằng chứng DƯƠNG: đọc `N/N` với hai số bằng nhau, đừng dừng ở `rc=0`.
2. Đột biến chạy trên BẢN SAO TẠM, không ghi vào tệp thật.
3. Ba trạng thái: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`**. Trạng thái thứ ba phải được khai, không
   được làm tròn thành một trong hai cái kia.
4. Khai thẳng thứ bạn KHÔNG đo được (Windows, endpoint MCP thật) thay vì im lặng.

## Đầu ra
Mỗi finding: bằng chứng chạy được · mức (P0..P3) · bất biến bị cắt · gợi ý vá.
Kết thúc bằng đúng hai dòng, mỗi dòng xuất hiện đúng một lần:

```
VERDICT: approve | changes_requested | blocked
Reviewed commit: 825e97042b86f5e200c2ab8a00b58d8642510353
```
