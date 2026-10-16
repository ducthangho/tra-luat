# ADR-0053 — Trần kích thước packet `sensitive` nâng lên SÁU tệp / 450 dòng thêm

- **Trạng thái:** Accepted (2026-10-16, chỉ thị chủ kho `ducthangho`; thi hành bằng packet
  `TRAN-CODEX-VA-SENSITIVE` revision 1, Issue #782 — không phải một phiên tự nâng trần)

Một packet `sensitive` chạm authority: **≤ 6 tệp và ≤ 450 dòng thêm** theo `git diff --numstat`. ADR
này thay **đúng một cặp số** của `ADR-0044` — cặp số của class `sensitive` (trước là ≤ 3 tệp / ≤ 300
dòng thêm) — và không thay gì khác.

`ADR-0044` vẫn hiệu lực ở mọi phần còn lại: trần packet thường **≤ 6 tệp và ≤ 1.000 dòng thêm cộng
xoá** KHÔNG đổi; vượt ngưỡng thì dừng TRƯỚC review để revision thiết kế hoặc khai lý do trong spec;
không tự mở hai PR chồng lấn; nối tiếp chỉ hợp lệ trên integration branch đã nhận slice trước.

## Vì sao sáu tệp chứ không mười

Chỉ thị gốc nêu **≤ 10 tệp / ≤ 450 dòng thêm**. Mười tệp vượt trần packet thường (sáu tệp), tức một
packet chạm authority sẽ được rộng hơn một packet thường — đảo thứ bậc mà `ADR-0044` dựng: rủi ro cao
hơn thì diện review phải hẹp hơn, không rộng hơn. Chủ kho chọn **sáu tệp** (bằng trần thường) khi được
hỏi đúng điểm này (Q1 của đặc tả). Phương án còn lại — giữ mười tệp và nâng luôn trần thường lên
mười — bị bác vì đổi thêm một con số mà chỉ thị đã dặn giữ.

Hai trần **khác đơn vị** và vẫn khác: `sensitive` đếm *dòng thêm*, packet thường đếm *dòng thêm cộng
xoá*. Thống nhất đơn vị nằm ngoài ADR này.

## Giới hạn của lý lẽ

`ADR-0044` neo ngưỡng cũ vào số đo của kho (`PLAT-M4` = 2 tệp, +351 ⇒ một vòng, một finding;
`PLAT-X4` = 4 tệp, +721 ⇒ ba vòng, tám finding). Số đo ấy **không** chứng minh sáu tệp / 450 dòng là
đúng; nó chỉ cho thấy +721 dòng đã là quá lớn, và 450 nằm dưới mức ấy. Cặp số mới là **quyết định của
chủ kho**; đừng đọc nó như một phép tối ưu.

## Vượt trần vẫn phải khai lý do — và KHÔNG cổng nào canh

Cơ chế vượt trần của `ADR-0044` giữ nguyên: khai lý do trong spec, người giữ kho chấp nhận. `ADR-0044`
khai *"cổng write-set và `numstat` chạy TRƯỚC review"*, nhưng §20 ghi ADR ấy là **`0 cổng`**; ADR này
cũng **không** có cổng nào canh ngưỡng mới. Người soạn spec, người cấp lease và reviewer phải đo
`git diff --numstat` **bằng tay**. Ô *"trần `ADR-0044`"* trong thân PR là một lời khai về THẨM QUYỀN
(`.claude/skills/soan-spec/SKILL.md` §2), nên đo lại trước mỗi lần công bố.

## Hiệu lực theo THỜI ĐIỂM ĐÓNG BĂNG — không hồi tố

- **MỐC** — ngày ADR này được chấp nhận: **2026-10-16**.
- **THỨ NEO** — `spec_hash` đóng băng của packet.
- **Đọc ra:** đặc tả đóng băng **TRƯỚC** mốc ⇒ trần `sensitive` cũ (≤ 3 tệp / ≤ 300 dòng thêm); **TỪ
  mốc trở đi** ⇒ trần của ADR này.

Chính packet thi hành ADR này đóng băng đặc tả trước mốc, nên nó chịu trần cũ: write set **3** tệp.
Đó là lý do nó **không** sửa `.claude/skills/soan-spec/SKILL.md`, nơi vẫn trỏ ngưỡng về `ADR-0044` —
thêm tệp ấy là thành bốn tệp, vượt trần cũ. Đây không phải con trỏ chết (`ADR-0044` vẫn tồn tại và §20
dẫn tới ADR này) mà là nợ, ghi dưới đây.

ADR này **không** sửa `docs/adr/0044-*.md`: sửa là viết lại một lời khai vốn đúng tại thời điểm của nó.

## Con số chỉ có MỘT chỗ ở

Cặp số `sensitive` chỉ ở **tệp này**. Protocol không chép nó; dòng §20 của ADR này và của `ADR-0044`
chỉ định tuyến.

## Nợ

**`SOAN-SPEC-TRO-NGUONG-CU`.** `.claude/skills/soan-spec/SKILL.md:89` trỏ ngưỡng về `ADR-0044` mà không
nhắc ADR này. Một packet `routine` sau khi ADR này land nên đổi dòng ấy sang trỏ §20.

**Không có con trỏ tiến** từ `ADR-0044` tới đây; đường duy nhất là bảng §20.
