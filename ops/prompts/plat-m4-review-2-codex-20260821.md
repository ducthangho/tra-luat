# PROMPT REVIEWER — `PLAT-M4` (#194 / PR "#204"), lượt 2/2. Neo exact head `7a2320fe`.

Bạn là reviewer khác nền (codex) cho một packet do claude vá. **Read-only.** Kho nằm ở `./kho`;
mọi tệp bạn tạo phải nằm NGOÀI cây ấy. Chốt: `git -C kho status --short` phải RỖNG ở cuối lượt,
và HEAD phải vẫn là `7a2320fe13b4aad3e7b298d070125a01762a8e54`.

Đây là lượt review **CUỐI** trong ngân sách: còn đúng một vòng và một lời gọi. Không có lượt ba.

## Bối cảnh — đọc trước khi soi mã
Lượt 1 của bạn ra `changes_requested` với **đúng một** finding P2: `_do_mcp_endpoint` khớp TIỀN TỐ
CHUỖI nên `https://user:SECRET@host/mcp` vẫn được probe THẬT, và bí mật đi nguyên văn vào cả
`req.full_url` lẫn `req.host`. Verdict cũ ở `kho/ops/reviews/plat-m4-review-1-codex-verdict.md`
(nếu nhánh gom bằng chứng không có trong bản sao này thì bỏ qua — đừng đi tìm).

Đặc tả có thẩm quyền: `kho/ops/specs/plat-m4-v0.md`, sha256
`63ff22bcc2427850ddd66322ed4a5ac5dcaa03f8d242cc857d12825b601953d1`. **Kiểm băm trước.** Lệch băm
thì đó là finding, không phải chuyện vặt.

Delta cần soi: `git -C kho diff 5813fc450efe3cb349b082044708d27a589b69fb..HEAD` — đúng hai tệp,
`.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`. Ba tệp trở lên là finding.

## Việc
1. **Finding P2 đã ĐÓNG thật chưa** — đo, đừng đọc. Dựng lại phép đo của chính bạn ở lượt 1
   (`urlopen` giả, ghi lại `full_url` và `host`) và khẳng định: URL có `userinfo` ⇒ `khong_do_duoc`,
   `urlopen` KHÔNG được gọi, và **mô tả trả về không chứa bí mật**.
2. **Bản vá có mở lỗ mới không.** Vài hướng đáng thử, không phải danh sách đầy đủ: đường thuận có
   bị chặn nhầm không · `urlsplit` với đầu vào méo (IPv6 hỏng, `http:///`, khoảng trắng đầu chuỗi,
   dấu `@` trong đường dẫn hoặc query) · thứ tự kiểm có chỗ nào vẫn in `url` ra mô tả cho một đầu
   vào mang bí mật không · `hostname` rỗng bị xử ra sao.
3. **Ca kiểm có RĂNG không.** Bộ đột biến ở `launcher_test.py` khai ba con liên quan; đo xem mỗi con
   có giết đúng một ca không, và tự nghĩ thêm đột biến mà bộ hiện tại KHÔNG giết được.
4. **Lời khai có bằng phạm vi đo được không** — kiểm cả docstring lẫn thông điệp, không chỉ mã.

## Bốn chốt của kho
1. Bằng chứng DƯƠNG: đọc `N/N` với hai số bằng nhau, đừng dừng ở `rc=0`.
2. Đột biến chạy trên BẢN SAO TẠM, không ghi vào tệp thật.
3. Ba trạng thái: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`**. Trạng thái thứ ba phải được khai, không
   được làm tròn thành một trong hai cái kia.
4. Khai thẳng thứ bạn KHÔNG đo được (Windows chẳng hạn) thay vì im lặng.

## Đầu ra
Mỗi finding: bằng chứng chạy được · mức (P0..P3) · bất biến bị cắt · gợi ý vá.
Kết thúc bằng đúng hai dòng, mỗi dòng xuất hiện đúng một lần:

```
VERDICT: approve | changes_requested | blocked
Reviewed commit: 7a2320fe13b4aad3e7b298d070125a01762a8e54
```
