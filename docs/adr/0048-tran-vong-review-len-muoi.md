# ADR-0048 — Trần trục VÒNG nâng lên MƯỜI, và nó vẫn chỉ có một chỗ ở

- **Trạng thái:** Accepted (2026-09-12, chỉ thị chủ kho `ducthangho`; thi hành `ADR-0034` bằng packet
  `TRAN-VONG-REVIEW-LEN-BON` revision 2, không phải một phiên tự nâng trần)

Trần canon cho một PR packet là **mười vòng review hợp lệ**. ADR này thay **đúng một con số** của
`ADR-0043` — con số của trục VÒNG — và không thay gì khác.

`ADR-0043` là tiền nhiệm và **vẫn hiệu lực** ở mọi phần còn lại: nó tách ba trục VÒNG (canon, kỷ
luật) · LỜI GỌI (chi phí) · ATTEMPT (số lần tuyên bố DONE), giữ các trần độc lập, và giữ luật trần
chạm trước thắng. Hai trục kia **KHÔNG đổi** theo ADR này: `codex_review_calls_used` giữ nguyên trần
của nó, và trần ATTEMPT giữ nguyên. Nâng nhầm trục kia là nâng CHI PHÍ chứ không nâng kỷ luật.

Định nghĩa vòng review canon cũng **KHÔNG đổi**: vòng chỉ tính khi có biên nhận hợp lệ. Nâng trần mà
đồng thời nới định nghĩa là nâng hai thứ cùng lúc rồi không biết cái nào có tác dụng.

## Vượt trần MỚI vẫn phải khai `nang_tran`

Nâng trần **không** bỏ cơ chế vượt trần. Vượt trần mười vẫn đòi khối `nang_tran` khai `ai_nang`
(phải là chủ kho, theo thẩm quyền §2 của protocol), `can_cu`, `tran_cu` và `tran_moi`. Một trần
không có đường vượt được khai báo là một trần người ta sẽ đi vòng quanh, và một trần vượt được trong
im lặng thì không phải trần.

**Nghĩa vụ ấy KHÔNG có cổng nào cưỡng chế — nói thẳng, vì bản đầu của ADR này khai ngược.** Bản đầu
viết *"không có khối ấy thì cổng đăng lease từ chối"*, chép lời khai của `ADR-0043`. Đo lại
12-09-2026, **đếm RIÊNG từng tên** vì chúng có phạm vi khác nhau:

| tên | `ops/lease_publish.py` — số LẦN xuất hiện | toàn kho — số TỆP `*.py` chứa nó |
|---|---:|---:|
| `nang_tran` | 0 | 0 |
| `ai_nang` | 0 | 0 |
| `tran_cu` | 0 | 0 |
| `tran_moi` | 0 | 0 |
| `review_rounds_used` | 0 | 0 |
| `can_cu` | **7** | **11** |

Bốn tên RIÊNG của cơ chế vượt trần — `nang_tran`, `ai_nang`, `tran_cu`, `tran_moi` — cùng bộ đếm
`review_rounds_used` đều **vắng mặt hoàn toàn**. `can_cu` thì KHÔNG: nó có mặt, nhưng thuộc cơ chế
**thu hồi lease** (`ops/lease_publish.py:960`, `1062`–`1067` đòi `can_cu` là một URL Issue comment),
không phải cơ chế vượt trần. Nên kết luận *"không có cổng nào cưỡng chế `nang_tran`"* vẫn đứng, còn
lời khai *"cả năm tên đều 0"* thì **sai** — và bản trước của chính đoạn này đã viết đúng câu sai ấy.

**Hai cột trên CỐ Ý khác đơn vị, và phải khai ra đơn vị kẻo bảng tự sinh đúng cái lớp lỗi nó đang
tố cáo.** Đo lại 12-09-2026: `can_cu` trong `ops/lease_publish.py` là **6 dòng / 7 lần xuất hiện**
(dòng `1062` mang hai lần trên cùng một dòng), và toàn kho là **11 tệp / 53 dòng / 62 lần**. Nên `7`
là số LẦN còn `11` là số TỆP. Bản đầu của bảng chỉ ghi đơn vị cho cột thứ hai, nên đọc thoáng thì hai
cột trông như cùng một phép đếm — với các hàng `0` thì không ai thấy, vì 0 bằng nhau ở mọi đơn vị.

Ghi cả cái sai vì nó là một lớp lỗi có tên: **gộp nhiều tên trường khác phạm vi vào một con số 0**.
Một tên dùng chung với cơ chế khác sẽ khác 0 mà chẳng chứng minh gì về cơ chế đang xét; đếm gộp thì
vừa khai sai, vừa che mất điều đó. Đếm riêng từng tên, và phân biệt *token có mặt* với *cơ chế có
cưỡng chế*.

Câu hứa cũ hứa một chốt máy không tồn tại, và nó mâu thuẫn với chính mục *Nợ* ở cuối tệp này. Người
cấp lease và người review phải kiểm khối `nang_tran` **bằng tay**; ai tin có cổng sẽ bỏ đúng bước
kiểm ấy.

Nghĩa vụ giữ nguyên, chỉ lời khai về cưỡng chế bị hạ xuống đúng mức đo được. Đây là lớp lỗi *"chép
lời khai cưỡng chế từ chính sách cũ sang chính sách mới mà không đối chiếu hành vi sản phẩm"* —
ADR kế nhiệm nào chép lại câu này phải đo lại trước, đừng chép tiếp.

## Số biện hộ — và giới hạn của nó

Hai chuỗi review THẬT của kho, đo 12-09-2026:

| PR | số vòng cross-review đã dùng | trần 2 | trần 4 | trần 10 |
|---|---:|---|---|---|
| `#508` (`#513`) | **13** | vượt từ vòng 3 | vượt từ vòng 5 | vượt từ vòng 11 |
| `#512` (`#504`) | **4** | vượt từ vòng 3 | **chạm đúng ở vòng 4** | còn chỗ |
| `#517` | 3 | vượt từ vòng 3 | trong trần | trong trần |
| `#520` | 3 | vượt từ vòng 3 | trong trần | trong trần |

Trần **4** đã bị chạm bởi một packet đang chạy (`#512`) ngay trong ngày con số ấy được đề xuất, và
`#508` vượt nó gấp ba. Một trần mà thực tiễn thường xuyên vượt thì mỗi lần vượt lại đòi một khối
`nang_tran`; khi việc khai ngoại lệ thành THƯỜNG LỆ thì ngoại lệ không còn là tín hiệu — đúng khuyết
tật *"cổng đỏ thường trực"* mà kho đã ghi.

**Giới hạn của lý lẽ trên, nói thẳng:** phép đo này biện hộ cho việc trần phải **CAO HƠN 4**. Nó
**KHÔNG** chứng minh con số 10 là đúng. Con số 10 là **quyết định của chủ kho**; phần đo được chỉ là
*"4 quá thấp so với thực tiễn đã đo"*. Đừng khai mạnh hơn thế, và đừng đọc bảng trên như một phép
tối ưu.

Hai lời khai yếu nữa của chính bảng ấy: số vòng được đếm **bằng TAY** từ hiện vật phiên (sandbox,
verdict có băm, comment PR), không từ một bộ đếm trong kho — vì bộ đếm ấy không tồn tại (xem *Nợ* bên
dưới). Và **không đo được** trần mười có đủ hay không: nó chưa từng bị chạm. Câu duy nhất đo được là
trần bốn ĐÃ bị chạm.

## Hiệu lực theo THỜI ĐIỂM ĐÓNG BĂNG — không hồi tố

Con số cũ đã được **chép** vào thân của bốn đặc tả đã đóng băng
(`ops/specs/BO-CONG-DUYET-KHAC-DANH-TINH.md`, `ops/specs/CI-CAI-JSONSCHEMA-r2.md`,
`ops/specs/CI-CAI-JSONSCHEMA-r3.md`, `ops/specs/TAT-DINH-VOID-HA-TANG-r2.md`). `§3.2` cấm sửa một
đặc tả đã đóng băng, nên chúng không được sửa; không có luật hiệu lực thì lần đọc kế tiếp thấy *"ADR
nói mười, bốn đặc tả nói hai"* mà không có gì phân xử.

Luật phân xử, và nó phải đọc ra **đúng một** câu trả lời cho mỗi packet:

- **MỐC** — ngày ADR này được chấp nhận: **2026-09-12**.
- **THỨ NEO** — `spec_hash` của packet, tức thời điểm đặc tả của nó được ĐÓNG BĂNG, **không** phải
  thời điểm packet chạy, không phải thời điểm lease được cấp, không phải ngày PR mở.
- **Đọc ra:** đặc tả đóng băng **TRƯỚC** mốc ⇒ packet ấy giữ **trần cũ** của `ADR-0043`; đặc tả đóng
  băng **TỪ mốc trở đi** ⇒ trần mười của ADR này.

Nên bốn đặc tả kia giữ trần cũ cho packet của chúng, và đó **KHÔNG** phải mâu thuẫn — đó là lời khai
ĐÚNG về trần **tại thời điểm chúng đóng băng**. Packet nào muốn trần mới thì đi đường `§3.2` đã có
sẵn: *"Policy đổi làm closure thay đổi thì packet phải tạo revision và generation mới trước khi chạy
tiếp"* — tạo **revision mới** với `spec_hash` mới, đóng băng từ mốc trở đi.

Đây cũng là lý do ADR này **không** sửa `docs/adr/0043-*.md` và không sửa bốn đặc tả trên: sửa chúng
là viết lại một lời khai vốn đúng tại thời điểm của nó.

## Con số chỉ có MỘT chỗ ở

`ADR-0043` ra đời vì con số trần sống ở bốn chỗ với hai giá trị và hai luật ưu tiên loại trừ nhau.
Nâng trần bằng cách **chép con số mới đi khắp nơi** là tái tạo đúng khuyết tật ấy.

Chỗ ở duy nhất của con số trục VÒNG là **tệp này**. Mọi tài liệu khác **TRỎ**, không chép:
`docs/PROTOCOL_DA_PHIEN.md` và `docs/adr/0037-*.md` giữ nguyên dạng trỏ. Dòng `§20` của ADR này cũng
không mang con số — nó định tuyến, không phát biểu luật.

## Nợ — đọc trước khi tin rằng trần này được canh

**`SO-CANON-CHUA-TON-TAI`.** `§20` ghi `ADR-0043` → **`0 cổng`**, và phép đo lại 12-09-2026 vẫn cho
kết quả cũ: `grep -rln "review_rounds_used" --include=*.py .` ⇒ **0 tệp**. Không có bộ đếm nào trong
kho, nên **trần mười cũng KHÔNG có cổng nào canh**, y hệt trần hai. ADR này **không** chữa điều đó và
**không** được khai là đã chữa; nó chỉ đổi con số mà kỷ luật đọc phải tuân. Cổng `so-canon` là packet
riêng.

**`ADR-0043` KHÔNG có con trỏ tiến.** ADR này trỏ ngược về `ADR-0043`, nhưng chiều ngược lại không
tồn tại: `ADR-0043` là hồ sơ đã đóng và packet này bị cấm sửa nó, nên một người mở thẳng
`docs/adr/0043-*.md` sẽ đọc con số cũ mà không thấy dòng nào dẫn tới đây. Đường duy nhất phát hiện
được là **bảng `§20`**, nơi dòng của `ADR-0043` khai rằng con số trục VÒNG của nó đã bị ADR này thay.
Ai đọc ADR mà không đi qua `§20` thì không có gì cảnh báo — nói thẳng ra đây thay vì để nó thành một
con trỏ chết không ai khai.
