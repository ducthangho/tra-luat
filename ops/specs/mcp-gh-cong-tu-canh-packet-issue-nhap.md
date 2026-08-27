# `MCP-GH-CONG-TU-CANH` — ba dòng của cổng đo mà KHÔNG ai đo

Tách khỏi **#319** theo quyết định của người giữ kho ngày 2026-08-27, đúng lời hứa đã ghi trước
trong lease `mcp-gh-cuu-ho-exec-1r5`: *"MÃ chạm 900 ⇒ TÁCH. Không nâng lần bốn, và không đổi đơn
vị lần hai."* Ngân sách của #319 chạm **900/900, biên 0**, và ba việc dưới đây cần khoảng 7 dòng.

Đây KHÔNG phải việc mới nghĩ ra. Cả ba đã ĐO ĐƯỢC trên `f461413a`, biên nhận
`ops/reviews/mcp-gh-cuu-ho-kiem-doc-lap-r6.md` trên nhánh `ops/cap-lease-tach-314`.

## Ba việc

### 1. Bộ chạy đột biến KHÔNG có chốt duy-nhất — fail-close

`chay_dot_bien` chỉ kiểm `if old not in src`. Nó KHÔNG kiểm `src.count(old) == 1`, và dùng
`src.replace(old, new, 1)` — nên khi mẫu trùng, nó im lặng đánh vào lần xuất hiện ĐẦU.

**Đã bắn thật một lần.** Mẫu của `d11_xoa_d8` là `"    lines += dong_d8(d8_errors, failed)"`,
xuất hiện HAI lần: mã thật ở dòng 660, và **dữ liệu trong chính bảng `MUTATIONS`** ở dòng 597.
Đột biến đánh vào BẢNG, không vào mã ⇒ không ca nào đỏ ⇒ tập giết RỖNG ⇒ `D8(a)` và `D8(b)` ĐỎ,
`rc=1`. Executor không thấy vì sandbox của nó không `bind` được nên nền đỏ và mọi ô in
`KHÔNG_ĐO_ĐƯỢC` — đúng `D7b`, nhưng nghĩa là nó chưa từng đo cổng của chính mình đầu–cuối.

**Phần đáng lo hơn cái đã bắn:** quét cả bảng cho **14 trong 48** mẫu KHÔNG duy nhất. 13 cái còn
lại đánh đúng chỗ **chỉ nhờ thứ tự tình cờ** — mã đích của chúng nằm TRƯỚC bảng `MUTATIONS`
(dòng 552–601), nên lần xuất hiện đầu là mã thật. **Chuyển một hàm xuống dưới bảng là 13 đột biến
ấy lặng lẽ trở thành vô nghĩa**, và cổng vẫn xanh.

Việc: `src.count(old) != 1` ⇒ `KHÔNG_ĐO_ĐƯỢC` kèm tên mẫu, đừng đoán. Cộng phản chứng cho chính
chốt ấy.

### 2. Dòng 657 không có đột biến canh

Hậu tố `ĐẠT`/`ĐỎ` của dòng `CA` là dòng cơ chế do bản vá r6 thêm. Ép nó thành `"ĐẠT"` cho một bản
chạy **xanh hoàn toàn**, `rc=0`, không ca nào đỏ. Không đột biến nào trong 48 nhắm vào nó.

Đặc tả `mcp-gh-cuu-ho.md` bản sửa đổi 4 viết thẳng: *"không được có dòng nào trong cơ chế mà xoá
đi vẫn xanh."* Nên đây là vi phạm chính đặc tả của packet cha.

Nói cho công bằng: nó KHÔNG phải chốt duy nhất — bỏ một ca khỏi vòng lặp vẫn chết qua đường khác.
Nhưng *"có đường khác bắt hộ"* không phải là *"có phản chứng"*.

### 3. Ca `D10-main` bị hạ thành mệnh đề luôn đúng

Thân ca nay là đúng một dòng: `assert ma_thoat(False) == 1`.

Đặc tả r4 đòi `D10`: *"ca dựng cảnh sổ ca một phần tử có cờ ghi nhận, gọi điểm vào, và đòi CẢ HAI:
mã thoát khác 0 VÀ cờ đã được đặt."* Ca mới không dựng cảnh, không gọi điểm vào, không có cờ.
Bản CŨ mạnh hơn: nó khẳng định *"có ca đăng ký mà không chạy ca nào ⇒ 1"*.

Khả năng ấy chưa mất hẳn — nó chuyển sang ca `D11-gate` và sang `_du_ca` trong dòng `CA` — nhưng
`D10` nay không còn tự đo tiêu chí mang tên nó. Đây là **hồi quy**, và điều kiện dừng `S1` của
lease r6 đã bắn ở đúng chỗ này.

## Một việc thứ tư, nhỏ hơn: sửa một lời khai QUÁ MẠNH của đặc tả r4

Đặc tả r4 viết *"`D11` thu hẹp bề mặt ấy xuống một dòng duy nhất"*. **Đo được là sai.** Có ít nhất
BA dòng mà đột biến làm tiến trình thoát 0: 381 (`ma_thoat`), 377 (`phan_dinh`), 670 (`sys.exit`).
Khác biệt thật — và đây mới là điều đáng khai — là hai dòng đầu **để lại vết đỏ trong bản in**, còn
dòng 670 thì **không in gì cả**.

Câu đúng: *`D11` không xoá được bề mặt, nhưng nó làm mọi đường làm giả TRỪ dòng ngoài cùng nhất
đều phải để lại vết trong báo cáo.*

Ghi ra vì phiên điều phối vừa soạn đặc tả, vừa soạn tiêu chí, vừa chấm — một lời khai quá mạnh của
chính nó là thứ dễ trôi qua nhất.

## write set đề xuất

- `.claude/dev/mcp_gh_test.py`
- `ops/specs/mcp-gh-cuu-ho.md` (chỉ để sửa lời khai ở mục 4)

`.claude/dev/mcp_gh.py` KHÔNG cần — cả bốn việc đều nằm trong tệp test.

## RÀNG BUỘC — đọc trước khi cấp lease

**Đường dẫn đang CÓ NGƯỜI GIỮ.** Đo lúc 2026-08-27 bằng `ops/lease_publish.py ai-dang-giu`
(sau khi so hai nguồn ref bằng TẬP TÊN: 223 = 223, `comm` hai chiều rỗng, trừ một symref
`refs/remotes/origin/HEAD`):

    .claude/dev/mcp_gh_test.py  ->  NGƯỜI_GIỮ 1: mcp-gh-cuu-ho-exec-1r6-codex-20260827

Lease ấy hết hạn `2026-08-28T03:00:00Z`. **Packet này KHÔNG được cấp lease chồng lên nó.** Đường
đúng: chờ #319 kết thúc (land hoặc đóng lease), rồi mới cấp.

Ghi thêm một cái bẫy vừa bắt được: lần đo ĐẦU cho `NGƯỜI_GIỮ 2` vì **nhánh cục bộ
`ops/cap-lease-tach-314` tụt sau bản đã đẩy**, nên bản r5 nó đọc chưa có `da_bi_thay_the`. Đồng bộ
nhánh cục bộ xong mới ra `NGƯỜI_GIỮ 1`. Cùng hình dạng "người giữ ma" đã báo ở #313 — **đo trên
nhánh tụt sau thì con số CAO HƠN sự thật**, và không tầng nào cảnh báo.

## Ngân sách đề xuất

Ước lượng: chốt duy-nhất ~2 · phản chứng cho chốt ~2 · đột biến canh dòng 657 ~1 · khôi phục
`D10` ~4 · sửa lời khai đặc tả (tệp riêng, theo dõi riêng).

**Cảnh báo thật:** ước lượng của phiên điều phối đã sai HAI LẦN ở packet cha. Con số này là DỰ BÁO,
không phải hạn mức được phép tiêu. Trần nên đặt theo `ADR-0044` và có khối `nang_tran`/`ha_tran`
với `ai_nang`/`vi_sao` nếu đổi — đừng sửa con số trần trần trụi.

Và ĐƠN VỊ đo phải nói rõ: packet cha đã ĐỔI ĐƠN VỊ một lần (từ "cả write set" sang "chỉ hai tệp
mã"), nên mọi báo cáo ở đây phải nêu con số theo cả hai cách đọc, đừng chỉ nêu cái có lợi.
