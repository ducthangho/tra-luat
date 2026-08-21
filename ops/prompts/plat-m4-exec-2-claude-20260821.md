# PROMPT EXECUTOR — `PLAT-M4` (#194) vòng vá V0

Đặc tả có thẩm quyền: `ops/specs/plat-m4-v0.md`,
sha256 `63ff22bcc2427850ddd66322ed4a5ac5dcaa03f8d242cc857d12825b601953d1`.
Kiểm băm TRƯỚC khi làm gì. Lệch băm ⇒ DỪNG, không tự đoán ý.

Nhánh `claude/plat-m4-exec-1`, xuất phát từ `5813fc450efe3cb349b082044708d27a589b69fb`.
Write set đúng hai tệp: `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`.
Đụng tệp thứ ba là ra ngoài phạm vi — dừng và báo, đừng mở rộng lấy được.

## Việc
Đóng finding P2 duy nhất của `ops/reviews/plat-m4-review-1-codex-verdict.md`: URL mang
`userinfo` vẫn được probe THẬT, credential đi nguyên văn vào `req.full_url` và `req.host`.

Gợi ý vá của reviewer, theo đúng bốn phần đã nêu ở đó: `urllib.parse.urlsplit`; chỉ nhận
`scheme ∈ {http, https}`; đòi `hostname` hợp lệ; từ chối khi `username` hoặc `password` khác
`None`. Bổ sung ca khẳng định `khong_do_duoc` **và** `urlopen` KHÔNG được gọi.

## Bốn chốt của kho, áp cho lượt này
1. **Bằng chứng DƯƠNG, không phải `rc`.** Đọc dòng `N/N` với hai số BẰNG NHAU. `rc=0` một
   mình đã từng lừa cổng của kho này nhiều lần.
2. **Đột biến trên BẢN SAO TẠM.** Không ghi vào tệp thật rồi khôi phục trong `finally` — một
   lượt bị cắt giữa chừng để lại tệp méo, và bản vá NGƯỢC đã từng vào commit theo đường đó.
3. **Mỗi ca mới phải có đột biến giết ĐÚNG MỘT ca.** Giết 0 ⇒ ca không có răng; giết nhiều ⇒
   phạm vi trùng, phải tách.
4. **Đo nền trước khi nghi bản vá của mình.** Suite đỏ ⇒ chạy lại trên `origin/master` sạch và
   so DELTA trước khi sửa lung tung.

## Không được làm
- Không đụng `ops/reviews/README.md` — ĐO trên master: `35/35`, `t27` XANH. Xem `ngoai_pham_vi`.
- Không gộp E4/C5 (biên nông) dù write set trùng.
- Không tự cấp lượt review. Xong thì báo, `#194` còn đúng một lượt review trong ngân sách.

## Xong là gì
Đẩy lên `claude/plat-m4-exec-1`, báo lại: SHA head mới · dòng `N/N` · số đột biến và mỗi con
giết mấy ca · `git status --short` rỗng · và khai thẳng thứ KHÔNG đo được (Windows).
