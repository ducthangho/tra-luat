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

## Vượt trần MỚI vẫn phải khai `nang_tran` — và KHÔNG cổng nào canh

Packet `sensitive` vượt ≤ 6 tệp hoặc ≤ 450 dòng thêm phải mang trong đặc tả (và chép vào lease) một
khối `nang_tran` khai đủ bốn trường: `ai_nang` (chủ kho, theo thẩm quyền §2 của protocol), `can_cu`
(vì sao không tách được, kèm số đo `git diff --numstat`), `tran_cu` (cặp trần của ADR này) và `tran_moi`
(cặp trần xin cho packet ấy). Khối chỉ đòi khi VƯỢT; packet nằm trong trần không cần nó. Đây là cùng
hợp đồng với trần LỜI GỌI ở `ADR-0052` và trần VÒNG ở `ADR-0048`.

Hai đường của `ADR-0044` giữ nguyên bên cạnh khối ấy: dừng TRƯỚC review để revision thiết kế, hoặc khai
lý do trong spec cho người giữ kho chấp nhận — khối `nang_tran` là hình thức của lời khai ấy. `ADR-0044`
khai *"cổng write-set và `numstat` chạy TRƯỚC review"*, nhưng §20 ghi ADR ấy là **`0 cổng`**; ADR này
cũng **không** có cổng nào canh ngưỡng mới. Người soạn spec, người cấp lease và reviewer phải đo
`git diff --numstat` và kiểm khối `nang_tran` **bằng tay**: đo 17:01Z 16-10-2026, khớp nguyên từ, cả
bốn tên `nang_tran` `ai_nang` `tran_cu` `tran_moi` có **0** dòng trong `ops/lease_publish.py`. Ô *"trần `ADR-0044`"* trong thân PR là một lời khai về THẨM QUYỀN
(`.claude/skills/soan-spec/SKILL.md` §2), nên đo lại trước mỗi lần công bố.

## Hiệu lực — neo vào thứ BẤT BIẾN, không hồi tố

Luật **y hệt** `ADR-0052` (vì sao không dùng ngày hay thời điểm commit: xem mục cùng tên ở đó). Trần
của ADR này áp cho một packet **khi và chỉ khi đủ CẢ HAI**:

1. blob đặc tả mà `spec_hash` của lease trỏ tới chứa một dòng đúng nguyên văn
   `tran_kich_thuoc_sensitive: ADR-0053`;
2. `git cat-file -e <base_sha>:docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` ⇒ `rc=0`, với
   `base_sha` lấy từ lease.

Thiếu một trong hai, hoặc không đo được ⇒ trần `sensitive` cũ (≤ 3 tệp / ≤ 300 dòng thêm), fail-closed.

Chính packet thi hành ADR này không thoả điều kiện nào (đặc tả `56a0bf28…` không có dòng khai; `base_sha
653fef3f` không chứa tệp này) ⇒ trần cũ: write set **3** tệp.
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
