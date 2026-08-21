# PROMPT REVIEWER — `PLAT-M4` (#194 / PR "#204"), lượt 3. Neo exact head `825e9704`.

Bạn là reviewer cho một packet do một phiên `claude` khác vá. **Read-only.** Kho nằm ở
`./kho`; mọi tệp bạn tạo phải nằm NGOÀI cây ấy. Chốt: `git -C kho status --short` phải RỖNG
ở cuối lượt, và HEAD phải vẫn là `825e97042b86f5e200c2ab8a00b58d8642510353`.

## ĐỌC ĐIỀU NÀY TRƯỚC — bạn là bản THAY THẾ, và điều đó đổi việc của bạn

Reviewer đúng của packet này là `codex` (nhà cung cấp khác). Hai lượt codex ĐÃ chạy thật và
tìm ra finding thật. Lượt 3 thì **không chạy được**: bộ lọc nội dung của nhà cung cấp cắt
giữa lượt với `flagged for possible cybersecurity risk` — đo được là nó bắt vào **nội dung
diff** (URL dạng `user:SENTINEL@host`), không phải vào prompt, nên viết lại prompt không cứu
được. Chủ kho đã hạ mức assurance `cross_approved` → `same_provider_approved`, có ghi ở
`kho/ops/uy-quyen-194-same-provider-20260821.yaml`.

**Hệ quả cho bạn, nói thẳng:** bạn CÙNG nhà cung cấp với người vá. Cái lợi thế "nền khác
nhìn ra thứ nền này mù" — thứ đã tìm ra cả ba finding trước — **bạn không có**. Vậy nên
đừng cố diễn vai cross-review. Hãy làm thứ bạn THẬT SỰ làm được: **đo lại bằng tay**, chạy
lệnh, dựng đột biến. Một lời khai "tôi đã đọc và thấy ổn" từ bạn có giá trị gần bằng không
ở đây, và bản ghi hạ mức đã nói đúng như vậy.

## Ba thứ đã đổi so với hai lượt codex

**(1) Đặc tả có trong cây:** `kho/ops/specs/plat-m4-v0.md`, sha256
`63ff22bcc2427850ddd66322ed4a5ac5dcaa03f8d242cc857d12825b601953d1`. **Kiểm băm trước.**
Lệch băm là finding.

**(2) Hai verdict codex cũ đọc lại được**, và bạn PHẢI đọc:
`kho/ops/reviews/plat-m4-review-1-codex-verdict.md` · `…-2-codex-verdict.md`.

**(3) Bản vá của lượt này trả lời F2 và F3 của lượt 2.** Đừng tin lời khai — đo.

## Việc

Delta cần soi: `git -C kho diff origin/master...HEAD` — **đúng hai tệp**,
`.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`, `+473/−25`. Ba tệp trở lên là
finding. (Nhánh có vài commit gộp master; delta ba-chấm đã loại phần gộp ấy.)

1. **F2 đã đóng THẬT chưa** — "URL méo vẫn làm lộ bí mật qua mô tả". codex đã đưa bốn đầu
   vào: `http:///user:SENTINEL@host/mcp` · `javascript:user:SENTINEL@host` ·
   `http ://user:SENTINEL@host/mcp` · `http://?u=user:SENTINEL@host`. **Chạy lại cả bốn**
   (dựng `urlopen` giả, ghi `full_url`/`host`) và khẳng định `desc_has_secret=false` cho
   từng cái, đồng thời `urlopen` KHÔNG được gọi. Rồi tự nghĩ đầu vào thứ NĂM mà bản vá này
   không chặn — chú ý bản vá đổi cả **THỨ TỰ kiểm** (userinfo trước scheme), nên tấn công
   thứ tự ấy, đừng chỉ thử chuỗi lạ.
2. **F3 đã đóng THẬT chưa** — "test chưa khoá biên cấu trúc của `userinfo`". Hai đột biến
   codex nêu: `if ai_ep != (None, None):` → `if "@" in str(url):`, và → `if p_ep.username:`.
   Cả hai từng **SỐNG SÓT**. Đo lại xem nay có bị giết không, và **tự thêm đột biến thứ ba**
   mà bảng hiện tại không giết được.
3. **Bản vá có mở lỗ mới không.** `scheme` cũng là dữ liệu từ `url` —
   `urlsplit("GOCSPX-abc:x")` cho scheme `gocspx-abc`. Còn nhánh nào mang bất kỳ mảnh nào
   của `url` ra mô tả không?
4. **Lời khai có bằng phạm vi đo được không.** Docstring `t143` khai "TÁM điều" — đếm xem
   có đúng tám điều được ĐO không, hay chỉ được liệt kê. Lượt 2 đã bắt đúng lỗi này ở
   phiên bản "sáu điều", nên đây là chỗ đã có tiền án.

## Bốn chốt của kho
1. Bằng chứng DƯƠNG: đọc `N/N` với hai số bằng nhau, đừng dừng ở `rc=0`.
2. Đột biến chạy trên BẢN SAO TẠM, không ghi vào tệp thật.
3. Ba trạng thái: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`**. Trạng thái thứ ba phải được KHAI,
   không được làm tròn thành một trong hai cái kia.
4. Khai thẳng thứ bạn KHÔNG đo được (Windows, endpoint MCP thật) thay vì im lặng.

## Đầu ra
Mỗi finding: bằng chứng chạy được · mức (P0..P3) · bất biến bị cắt · gợi ý vá.
Kết thúc bằng đúng hai dòng, mỗi dòng xuất hiện đúng một lần:

```
VERDICT: approve | changes_requested | blocked
Reviewed commit: 825e97042b86f5e200c2ab8a00b58d8642510353
```
