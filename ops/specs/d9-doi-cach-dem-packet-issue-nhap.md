# `D9-DOI-CACH-DEM` — trần đếm dòng VẬT LÝ là trần đo được bằng cách xoá dòng trắng

Tách theo **quyết định của người giữ kho ngày 2026-08-28**: chọn phương án **(b)** cho nợ
`AG-360-P2-02-d9-nen-khoang-trang-danh-vao-phep-do` — **đổi cách `D9` đếm**, không phải chấp nhận
biên 0 rồi cấm nén bằng lời hứa.

## Nợ này đến từ đâu

Cross-review #360 (reviewer `claude`, cross-provider) đo được: bản vá đưa `D9` về đúng `900/900`
**một phần bằng NÉN HÌNH THỨC** — xoá dòng trắng phân cách ở **8 chỗ**, và **cả 8 đều sát các hàm
mới/sửa trong đúng diff ấy**, trong khi **48 hàm khác cùng tệp vẫn giữ hai dòng trắng**. Cộng hai
lệnh ghép bằng dấu chấm phẩy. Nội dung logic **không giảm**; chỉ MẬT ĐỘ DÒNG bị nén để đi qua
ngưỡng.

Reviewer xếp **P2, không P1**, và lý lẽ ấy đáng giữ nguyên: `D9` tự nó **vẫn ĐẠT theo đúng định
nghĩa đo được của nó** — `sum(1 for _ in path.open())` đếm dòng vật lý, không hơn không kém. Bản vá
**khai thác đúng cách `D9` được ĐỊNH NGHĨA**, chứ không làm sai phép đo. Nên chỗ phải sửa là **định
nghĩa**, không phải bản vá.

## Bằng chứng chạy được rằng đây là vấn đề THẬT, không phải chuyện thẩm mỹ

Nợ `AG-360-P2-03-d12-thieu-try-finally` — `d12_mau_dot_bien_phai_duy_nhat` gán đè `MUTATIONS` toàn
cục rồi khôi phục **không có `try`/`finally`** — **không vá ngay được**, vì vá nó cần THÊM dòng mà
biên đang là **0**. Một packet **không sửa nổi P2 của chính nó mà không phá ratchet của chính nó**.
Đó là chứng cứ cho thấy trần đã hết ý nghĩa, không phải người thi công lười.

## Số đo nền (master `27fb9de2`) — ĐO CỦA PHIÊN ĐIỀU PHỐI, KHÔNG PHẢI CHÂN LÝ

|  | `mcp_gh.py` | `mcp_gh_test.py` | tổng |
|---|---:|---:|---:|
| dòng vật lý (`D9` hiện đếm) | 230 | 670 | **900** |
| dòng KHÔNG TRẮNG | 199 | 542 | **741** |

Executor **phải tự đo lại cả bốn con số**. Kho có bài học *"một BẤT BIẾN còn đúng không chứng minh
các SỐ HẠNG còn đúng"*.

## Việc của packet

**1. Đổi `d9_ngan_sach_900_dong_ma` sang đếm dòng KHÔNG TRẮNG.** Đó là cách giết đường nén khoảng
trắng **theo CẤU TRÚC**, không theo lời hứa: dòng trắng không được đếm thì xoá nó chẳng mua được gì.

**2. Đặt lại trần từ SỐ ĐO, kèm biên có LÝ DO.** Không chọn một con số tròn cho đẹp. Nêu rõ biên là
bao nhiêu và **vì sao chừng ấy** — biên 0 chính là thứ đã sinh ra nợ này, nên một trần bằng đúng số
đo hiện tại là tái phạm.

**3. Đột biến canh cho chính luật đếm mới.** Đổi ngược phép đếm về "mọi dòng" phải làm một ca ĐỎ.
Không có đột biến ấy thì không ai biết cổng đang đo LUẬT MỚI hay đo thứ khác — và packet này sẽ chỉ
dời chỗ hở.

**4. Đóng nợ `AG-360-P2-03`** — thêm `try`/`finally` cho `d12_mau_dot_bien_phai_duy_nhat`. Nó nằm
trong write set, và nó là **bằng chứng sống** cho việc số 2: nếu sau khi đổi trần mà vẫn không vá
nổi, thì trần mới cũng sai.

**5. Đóng nợ P2 kế thừa của #319**
`d9-dong-tieu-chi-van-mo-ta-numstat-tren-write-set-nhung-ma-do-tong-dong-hai-tep-ma` — LỜI KHAI của
tiêu chí nói `numstat` trên write set, còn MÃ đo tổng dòng hai tệp. Hai câu khác nhau; sửa cho khớp
thứ mã thật sự đo. Cùng một chỗ, cùng một lượt.

## CÂU HỎI THẬT — hồ sơ CỐ Ý không đưa đáp án

Đếm dòng-không-trắng giết đường nén khoảng trắng. Nhưng nó làm **xoá CHÚ THÍCH** thành đường rẻ
nhất kế tiếp — và kho này **coi trọng chú thích dài**: phần lớn bài học đắt giá sống trong chú
thích ngay tại mã, không phải trong tài liệu rời.

Vậy packet phải trả lời, kèm lý lẽ đo được:
- **(A)** đếm dòng không-trắng, chấp nhận rằng chú thích trở thành đường nén kế tiếp, và nói thẳng
  điều đó ngay tại chỗ;
- **(B)** đếm dòng không-trắng **và** không-phải-chú-thích-đơn-độc — nhưng như thế là **tạo áp lực
  xoá chú thích có giá trị**, đúng thứ ngược với văn hoá kho;
- **(C)** một cách đếm khác mà bạn đo ra là tốt hơn cả hai — nói rõ nó là gì và vì sao.

**Không được chọn (A) chỉ vì hồ sơ liệt kê nó trước.**

## write set đề xuất

- `.claude/dev/mcp_gh_test.py`

Đúng một đường. `.claude/dev/mcp_gh.py` **KHÔNG** vào write set — packet chỉ ĐẾM nó, không sửa.

## Ràng buộc

- **KHÔNG nới trần để cho vừa việc số 4.** Nếu sau khi đổi luật đếm mà vẫn không đủ chỗ cho
  `try`/`finally`, thì **DỪNG và BÁO** — đó là finding về chính trần mới, không phải chỗ để nâng.
- Trần cũ `900` là con số của LUẬT CŨ. Sau khi đổi luật, con số cũ **mất nghĩa** — đừng mang nó
  sang rồi gọi là "không nâng trần". Nói rõ luật mới đo gì và ngưỡng mới là bao nhiêu.
- `#319` đã nâng/đổi đơn vị **bốn lần**. Packet này ĐỔI ĐƠN VỊ MỘT LẦN, **có chủ đích, được người
  giữ kho duyệt, và kèm đột biến canh** — khác hẳn bốn lần kia. Ghi rõ khác biệt ấy ngay tại mã,
  kẻo lượt sau đọc thành tiền lệ cho phép đổi đơn vị tuỳ tiện.
