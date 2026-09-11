# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 1)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **1** · `generation`: 1 · soạn **12:0xZ 11-09-2026**
- `depends_on`: **`[wp<TRAN-VONG-REVIEW-LEN-BON>]`** — skill trỏ trần, nên ADR phải land trước.
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (skill là hợp đồng hành vi của mọi phiên)

## `nguon_cap_viec`

Chỉ thị chủ kho **11-09-2026**, ba phần: lặp vá/cross-review/đăng verdict tới khi hết P1+P2 hoặc
approve · điều kiện dừng phân biệt theo tình huống · **vá theo LỚP lỗi, không theo từng lỗi**.

**Số biện hộ, đo trên chính `#508`:**

| vòng | P1 | P2 | P3 | tổng | phân hạng finding vòng trước |
|---|---:|---:|---:|---:|---|
| 1 | 6 | 6 | 1 | 13 | — |
| 2 | 5 | 6 | 1 | 12 | 4 VÁ THẬT · **8 VÁ HỜ** · 1 SINH LỖI MỚI |
| 3 | 6 | 4 | 1 | 11 | 3 VÁ THẬT · **8 VÁ HỜ** · 1 SINH LỖI MỚI |

**Tổng đi `13 → 12 → 11` — theo tiêu chí *"số lượng không cải thiện"* thì nó ĐANG cải thiện.** Một
luật keyed vào tổng **sẽ không bắn**. Nhưng vòng lặp không hội tụ: `VÁ HỜ` **đứng yên ở 8** hai vòng
liền, và **đúng 1 lỗi mới mỗi vòng**.

⇒ **Đếm tổng là nhạc cụ SAI.** Tín hiệu đúng nằm ở **phân hạng finding vòng trước**, thứ bảng
`ĐỐI CHIẾU LƯỢT TRƯỚC` của cross-review **đã sinh sẵn**:
`tỉ lệ VÁ THẬT` = `VÁ THẬT ÷ finding vòng trước` ⇒ vòng 2: `4/13 = 31 %`; vòng 3: `3/12 = 25 %`.

**Và lớp là thứ giải thích được `VÁ HỜ = 8`:** `4/11` finding vòng 3 thuộc **một lớp** — *"lời khai cũ
sống sót sau khi đã vá"* — gốc là cấu trúc (`GATE` chồng 9 khối REVISION, `648 → 1056` dòng).
Vá từng câu thì lớp tái sinh mỗi vòng. Viết lại bỏ lớp lịch sử ⇒ `1056 → 445` dòng, lớp chết theo
**KIẾN TRÚC**. Đó là bằng chứng vận hành cho yêu cầu *"vá theo LỚP"*.

**`PROTOCOL §12` đã có nửa luật này** — *"Cùng hình dạng lỗi xuất hiện **lần thứ ba** bắt buộc xem lại
có nên tiếp tục cách làm đó, không chỉ vá lần thứ tư"* — nhưng `§20` ghi `ADR-0037` **`0 cổng`**, và
không có nghĩa vụ nào buộc một vòng vá phải **khai lớp**. Packet này biến nửa luật ấy thành thứ
**đo được**.

## `review_class` và ngưỡng

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **2 tệp**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | bên SINH ra bảng phân hạng và verdict |
| 2 | `.claude/skills/work-packet/SKILL.md` | bên ĐỌC bảng ấy và quyết vá tiếp hay dừng |

Không ký tự đại diện. **KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md` — skill là **adapter MỎNG**;
`doctrine-scan` thoát khác 0 khi adapter **chép** doctrine. Skill phải **TRỎ** `§12`/`ADR-0037`/ADR
trần vòng, không chép luật.
**KHÔNG** đụng `.claude/hooks/**` (packet `CONG-CHAN-CHI-CI-SOM`).

## `ngoai_pham_vi`

1. **KHÔNG chép con số trần vòng vào skill** — trỏ ADR. Chép số là tái tạo đúng bệnh `ADR-0043` sinh
   ra để chữa (con số sống ở bốn chỗ với hai giá trị).
2. **KHÔNG viết cổng cưỡng chế** — skill là chữ. Cưỡng chế chi CI ở packet riêng; `so-canon` là nợ.
   Khai thẳng điều này **trong chính skill**, kẻo người đọc tưởng đã có cơ chế.
3. **KHÔNG đổi định nghĩa P1/P2/P3** — đang dùng được, đổi là làm ba lượt verdict cũ không so được.
4. **KHÔNG tự quyết thay chủ kho** khi vào Rescue Checkpoint; skill chỉ buộc **DỪNG và hỏi**.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | **Điều kiện dừng buộc vào `review_class`** (`§3.2` đã có, không tạo trục mới): `routine` ⇒ **0 P1** (P2 thành nợ có tên trong Issue) · `systemic` ⇒ **0 P1 + 0 P2** · `sensitive` ⇒ **`approve` tường minh**. | #1, #2 |
| M2 | **`sensitive` KHÔNG được dừng ở "0 P1 + 0 P2".** *"Vắng mặt vì sạch"* và *"vắng mặt vì chưa nhìn tới"* nhìn giống hệt nhau; `approve` phân biệt được, "không thấy lỗi" thì không. | #1, #2 |
| M3 | **BẢNG LỚP bắt buộc mỗi vòng vá.** Mỗi finding gán **đúng một** `lop_loi`; mỗi lớp khai **bản vá theo lớp** (một thay đổi đóng cả lớp) hoặc **lý do** vì sao lớp ấy phải vá lẻ. | #2 |
| M4 | **Một lớp xuất hiện ở vòng thứ BA ⇒ CẤM vá lẻ lần nữa** — phải đổi cách làm hoặc vào Review Rescue Checkpoint (`ADR-0037`). Đây là `§12` phát biểu ở mức **thi hành được**. | #2 |
| M5 | **Tín hiệu không hội tụ đo bằng PHÂN HẠNG, không bằng TỔNG.** Hai vòng liên tiếp có `tỉ lệ VÁ THẬT < 50 %` ⇒ **DỪNG và hỏi chủ kho**. | #1, #2 |
| M6 | **Điều khoản chống lách:** một vòng làm finding biến mất bằng cách **thu hẹp phạm vi** phải khai thẳng — thu hẹp phạm vi là một mục `chua_do_duoc`, **KHÔNG** phải một bản vá. | #1, #2 |
| M7 | **Ba loại chi CI** khai trong skill: (a) CI gác cổng do GitHub tự bắn — không đụng · (b) CI làm nhạc cụ đo — cho **đúng `N`** lượt, `N` đóng băng trong spec, mỗi lần ghi `run_id` vào biên nhận · (c) CI thăm dò — **CẤM**. | #2 |

## `nghiem_thu`

Skill là văn bản, nên mọi tiêu chí đo bằng **phép đọc có thể ĐỎ**, không bằng cảm nhận.

**A1 (M1,M2) — bảng điều kiện dừng có mặt và PHÂN BIỆT ĐƯỢC ba lớp.**
`cross-review/SKILL.md` phải có bảng ánh xạ `review_class → điều kiện dừng` với **đúng ba** hàng, và
hàng `sensitive` phải nói **`approve`**, không nói *"0 P1 + 0 P2"*.
**Phép làm ĐỎ:** đổi hàng `sensitive` thành *"hết P1, P2"* ⇒ ca ĐỎ · gộp `routine` với `systemic` ⇒ ĐỎ.
Phép đo: parse bảng Markdown, đòi tập `review_class` **bằng** `{routine, systemic, sensitive}` và ba
giá trị điều kiện **đôi một khác nhau**.

**A2 (M3) — BẢNG LỚP là nghĩa vụ, không phải gợi ý.**
`cross-review/SKILL.md` phải đòi verdict mang mục `BẢNG LỚP` với cột
`(lop_loi, các slug thuộc lớp, bản vá theo lớp | lý do vá lẻ)`; `work-packet/SKILL.md` phải đòi vòng
vá **đọc** bảng ấy trước khi sửa dòng nào.
**Phép làm ĐỎ:** bỏ cột `bản vá theo lớp` ⇒ bảng thành bảng phân loại thuần, không ép đổi cách làm
⇒ ca ĐỎ. Đòi **mỗi finding thuộc đúng một lớp** — finding không có lớp ⇒ verdict thiếu.

**A3 (M4) — ngưỡng LỚP đếm được và có hành động bắt buộc.**
Skill phải nêu: lớp xuất hiện **lần thứ 3** ⇒ **cấm vá lẻ**, phải đổi cách làm hoặc Rescue Checkpoint.
**Phép làm ĐỎ:** viết *"nên xem xét"* thay vì **cấm** ⇒ ĐỎ — `§12` dùng chữ *"bắt buộc"*, adapter
không được làm yếu hơn doctrine.
**Đơn vị: LỚP, không phải finding.** Ba finding cùng lớp trong **một** vòng là **lần 1** của lớp ấy,
không phải lần 3 — nói rõ, vì đếm nhầm đơn vị làm ngưỡng bắn sai lúc.

**A4 (M5) — tín hiệu không hội tụ tính từ PHÂN HẠNG.**
Skill phải nêu công thức `tỉ lệ VÁ THẬT = VÁ THẬT ÷ số finding vòng trước`, ngưỡng **`< 50 %` hai vòng
liên tiếp** ⇒ DỪNG và hỏi chủ kho.
**Phép làm ĐỎ — và ca này bắt buộc, vì nó là lý do packet tồn tại:** áp luật lên dữ liệu thật của
`#508` (`13 → 12 → 11`; VÁ THẬT `4`, rồi `3`). Đòi:
- luật **theo TỔNG** (*"số lượng không cải thiện"*) ⇒ **KHÔNG bắn** ở vòng 3;
- luật **theo PHÂN HẠNG** ⇒ **BẮN** ở vòng 3 (`31 %` rồi `25 %`, cả hai `< 50 %`).
Hai kết quả phải **KHÁC NHAU** trên cùng dữ liệu. Nếu chúng giống nhau thì luật mới **không mua được
gì**, và ca này ĐỎ.

**A5 (M6) — chống lách có răng.**
Skill phải nêu: thu hẹp phạm vi ⇒ mục `chua_do_duoc`, **không** tính là vá; và reviewer phải **gọi tên**
khi thấy một vòng đóng finding bằng cách cắt tiêu chí.
**Phép làm ĐỎ:** bỏ câu ấy ⇒ *"0 P1 + 0 P2"* mua được bằng cách cắt bớt tiêu chí ⇒ ĐỎ.

**A6 (M7) — ba loại chi CI phân biệt được.**
Bảng ba hàng; hàng (b) phải nêu **`N` đóng băng trong spec** và **`run_id` ghi biên nhận**; hàng (c)
phải là **CẤM**.
**Phép làm ĐỎ:** gộp (b) và (c) ⇒ ĐỎ · bỏ yêu cầu `run_id` ⇒ không phân biệt được đã chi mấy lượt ⇒ ĐỎ.

**A7 — adapter KHÔNG chép doctrine.**
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `rc=0`.
**Phép làm ĐỎ:** chép nguyên văn `§12` hay con số trần vòng vào skill ⇒ `doctrine-scan` ĐỎ.
Cổng này **đã có răng** (đo 11-09-2026: `rc=0`, 7 tệp, 0 chỗ chép) — không phải lời hứa.

**A8 — skill KHAI THẲNG thứ nó không cưỡng chế được.**
Phải có một câu nói rõ: các luật ở đây là **kỷ luật đọc**, `§20` ghi `ADR-0037`/ADR trần vòng
**`0 cổng`**, và cưỡng chế chi CI nằm ở packet `CONG-CHAN-CHI-CI-SOM`.
**Phép làm ĐỎ:** bỏ câu ấy ⇒ người đọc tưởng đã có cơ chế ⇒ ĐỎ.
Căn cứ: kho đã trả giá cho *"cảnh báo bằng chữ không chặn được ai"* và cho *"cổng vắng mặt trông
giống cổng xanh"*.

**A9 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ đúng **2** đường dẫn, `additions` ≤ `300`.

**Điều kiện dừng của CHÍNH packet này:** `sensitive` ⇒ đòi cross-review **`approve`** tường minh.
*(Packet này khai luật ấy, nên nó phải là packet đầu tiên tuân luật ấy.)*

## `chua_do_duoc`

1. **Không cổng nào cưỡng chế được các luật của packet này.** `doctrine-scan` (`A7`) chỉ canh **HÌNH
   THỨC** — adapter có chép doctrine không — nó **không** canh việc một phiên có thật sự lập BẢNG LỚP,
   có thật sự tính tỉ lệ VÁ THẬT, hay có dừng đúng ngưỡng. `§20` ghi `ADR-0037` **`0 cổng`**.
   Đây là **kỷ luật đọc**, và `A8` buộc skill nói thẳng điều đó.
2. **`tỉ lệ VÁ THẬT` phụ thuộc reviewer phân hạng đúng.** Nếu reviewer gán `VÁ THẬT` rộng tay thì tỉ lệ
   lên và luật không bắn. Không có phép kiểm chéo nào cho việc phân hạng — nợ, chưa có tên.
   Giảm nhẹ được một phần bằng `ADR-0046` (reviewer mới mỗi lượt), nhưng **không** đóng được.
3. **Ngưỡng `50 %` và `2 vòng` chọn từ MỘT bộ dữ liệu** (`#508`, 3 vòng). Đó là **một mẫu**, không phải
   một phân phối. Chúng có thể sai chiều trên packet khác. Phải **đo lại sau 3 packet dùng luật này**
   và điều chỉnh nếu lệch — nợ có tên: `NGUONG-HOI-TU-CHUA-CO-MAU`.
4. **Ba lượt review của `#508` không sinh biên nhận nào** trong `ops/reviews/` (đo 11:4xZ 11-09-2026),
   nên chúng **không** được tính là vòng canon theo `PROTOCOL:814`. Bảng số ở `nguon_cap_viec` vì thế
   là **dữ liệu vận hành thật** nhưng **không** phải hiện vật canon. Không dùng nó như một gate đã kiểm.
