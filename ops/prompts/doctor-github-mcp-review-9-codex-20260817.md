# Prompt review lượt 9 — PHẠM VI ĐÓNG BĂNG

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8). CHỈ ĐỌC.
Nguồn có thẩm quyền là TỆP CÓ BĂM trong kho (lease + prompt này).

## Lượt này KHÁC tám lượt trước, đọc kỹ đoạn này trước khi làm gì

Tám lượt trước, prompt luôn mời bạn đi tìm thêm ("tìm lượt thứ N", "kèm bốn hướng tấn
công", "kiểm lại lời khai tôi vừa bác"). Điều đó mua được nhiều lỗi thật — nhưng chủ kho
hỏi thẳng vì sao qua nhiều lượt vẫn chưa `approve`, và **nguyên nhân chính là người vá,
không phải bạn**: mỗi lượt người vá lại thêm mã mới ngoài danh sách, nên lượt sau có bề
mặt mới để soi. Bằng chứng rõ nhất là chính lượt 8: **cả hai finding đều nói về `t117`**,
mà `t117` do người vá tự nghĩ ra trong lúc CHUẨN BỊ lượt 8 — nó chưa từng nằm trong bản
mà lượt 7 đã xét.

Nên lượt này **ĐÓNG BĂNG PHẠM VI**. Người vá KHÔNG thêm ca mới, KHÔNG thêm hàm mới,
KHÔNG "gia cố nhân tiện". Diff so với SHA lượt 8 đã xét (`897b7fab`) là **đúng một tệp**
(`.claude/dev/launcher_test.py`, +38/−15) và chỉ gồm ba việc dưới đây.

## Ba việc đã làm — và CHỈ ba việc này

Danh sách đóng được của lượt 8 có 3 mục. Người vá làm được 2, cộng 1 việc bạn chỉ QUAN
SÁT chứ không đòi:

1. **(mục 1 của bạn)** `DA_BIET_TRUNG` đổi từ `set` + điều kiện `!= 1` sang **bảng
   `{tên: số_chỗ}`** và đòi khớp ĐÚNG số đã khai. Bạn nói đúng: `!= 1` cho qua cả 0 lẫn 3.
2. **(mục 2 của bạn)** docstring `t117` nay khai giới hạn tự-lừa **cùng phạm vi với
   `t116`**: cả đặc tả (`DOT_BIEN`, `DA_BIET_TRUNG`) lẫn bằng chứng (`launcher.py`) đều
   nằm trong những tệp một thay đổi PHỐI HỢP sửa được cùng lúc.
3. **(bạn chỉ quan sát, không đòi)** chốt `rest-kho` đổi từ **dò chuỗi nguồn** sang **đo
   HÀNH VI**: gọi thật `_do_github` với `_git`/`_do_rest_github` giả (origin không phải
   GitHub) và đòi đầu ra có `rest-kho=chua-do-duoc`. Bạn nêu đúng lỗ: giữ chuỗi ấy trong
   một comment rồi để hành vi trả `False` thì ca cũ vẫn xanh.

**Mục 3 trong danh sách của bạn — "chạy lại standard suite trong môi trường không bị ca
process-tree cắt" — người vá KHÔNG đóng được.** Đó là môi trường CỦA BẠN. Nếu lượt này
sandbox vẫn cắt sau `t62` thì cứ khai **KHÔNG ĐO ĐƯỢC** cho số tổng và delta; số `117/117`
vẫn sẽ chỉ có MỘT nguồn là người vá, và người vá không giấu chuyện đó.

## Phản chứng người vá đã chạy (bản sao tạm) — kiểm lại nếu bạn muốn

Hai kịch bản đầu chính là hai kịch bản bạn NÊU RA nhưng không chạy được vì lease read-only:

| kịch bản | trước bản vá | sau bản vá |
|---|---|---|
| K1 — thêm bản sao THỨ BA đặt trước `_do_hook_cu` | xanh | **116/117, `t117` ĐỎ** |
| K2 — mẫu ngoại lệ biến mất hẳn (0 chỗ) | xanh | **116/117, `t117` ĐỎ** |
| K3 — giữ chuỗi trong comment, hành vi trả `False` | xanh | **115/117, `t115` VÀ `t117` ĐỎ** |

## Việc của bạn — MỘT câu hỏi

**Danh sách đóng được của lượt 8 đã ĐÓNG chưa?** Trả lời cho từng mục: `đóng` /
`chưa đóng` / `không đo được`, kèm phép đo.

Nếu cả ba đóng (mục 3 tính là "không đo được" nếu sandbox vẫn cắt) thì **`approve`**.

## Nếu bạn thấy thêm điều gì

Cứ nêu — nhưng **xếp vào `## Nợ khai báo`, KHÔNG phải `## Findings`**, trừ khi nó thoả
một trong hai điều:

- **hồi quy**: bản vá lượt này làm hỏng thứ trước đó đang đúng; hoặc
- **P1**: sai ngay ở đường sản xuất của `_do_github` (không phải ở công cụ đo).

Lý do: mọi thứ ngoài hai loại ấy, người vá sẽ mở thay đổi RIÊNG với lượt review riêng —
vá tại chỗ chính là cỗ máy đã giữ chuỗi này mở suốt tám lượt. Xếp nhầm vào `Findings`
không làm mã tốt hơn, chỉ làm vòng lặp dài thêm.

## Ngoài phạm vi (đừng báo lại)

- `.github/workflows/**`, `.claude/skills/**` dùng `gh`; `ci.yml` không chạy `launcher_test.py`.
- Lời khai phạm vi của nhãn MCP — lượt 2 đo độc lập, lượt 5/6 xác nhận.
- Chốt `tao-tag` cấm `luu-tru/*` — ĐÃ sửa ở nhánh RIÊNG (PR #147), ngoài phạm vi PR này.
- Món nợ `hook_phien_bo_phep_so_nang_luc` (2 chỗ trùng, CÓ SẴN trên master) — đã vào
  `DA_BIET_TRUNG` kèm số lượng và chốt ngược; dọn nó đụng mã #143 ⇒ thay đổi RIÊNG.
- `t116`/`t117` tự-lừa được khi sửa PHỐI HỢP — đã khai trong docstring cả hai.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Danh sách đóng được của lượt 8   (từng mục: đóng / chưa đóng / không đo được)
    ## Findings        (CHỈ hồi quy hoặc P1 đường sản xuất — để trống nếu không có)
    ## Nợ khai báo     (mọi thứ khác)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
