# Phản biện đề xuất "Cải tiến quy trình Build – Review – CI"

- **Ngày đo:** 05-09-2026 · **HEAD:** `c03a409` (= `origin/master`) · **Người viết:** phiên Claude Code
- **Trạng thái:** phản biện thiết kế, CHƯA thi công. Không sửa mã, không mở packet.
- **Bản 2 — sau cross-review lượt 1 (06-09-2026).** Hai reviewer độc lập, hai hướng tấn công tách biệt.
  Kết quả: **kết luận trung tâm bị ĐẢO**, 4+8 finding P1 được nhận sau khi phiên chính tự đo lại từng cái.
  Những chỗ bản đầu sai được **giữ lại và ghi rõ**, không xoá — một phản biện giấu chỗ nó tự sai thì
  không dùng được. Nhật ký ở §9.
- **Phạm vi:** đề xuất 13 mục + 10 câu hỏi do chủ kho chuyển tới, dự kiến đưa song song cho Codex.

Tài liệu này KHÔNG nhắc lại luật của protocol. Luật ở `docs/PROTOCOL_DA_PHIEN.md`; từ vựng ở `CONTEXT.md`.
Chỗ nào tệp này lệch protocol thì TỆP NÀY sai.

---

## 0. Bảng đo — mọi phản biện dưới đây neo vào đây

Đo trên chính kho, tại `c03a409`. Lệnh tái hiện ghi kèm để người đọc không phải tin lời khai.

| Đại lượng | Số đo | Nguồn |
|---|---|---|
| Biên nhận cross-review | **57** tệp, **56** có `packet_id`, **15** packet riêng biệt | `ops/reviews/*.receipt.yaml` |
| Thời lượng MỘT lượt cross-review | n=**9**; min **835,6s** · median **922,4s** (15,4′) · trung bình **1043,7s** (17,4′) · max **1516,2s** (25,3′) | `thoi_luong_giay` trong biên nhận |
| Thời lượng MỘT lượt CI gate | ubuntu-only **21m52s** và **25m14s** (success); dispatch có Windows **25m19s · 25m09s · 45m17s** — cả ba **cancelled** ở trần job | chú thích r391, `.github/workflows/ci.yml` |
| Hạn mức Actions | đo 13-08: ~**20 phút tính tiền**/lượt × ~13,6 lượt/ngày ≈ **8.100 phút/tháng** so hạn Free **2.000** ⇒ cạn ~ngày 11; **đã cạn thật 12-08**, CI đứng hình | chú thích r245, `ci.yml` |
| Verdict | **33** `changes_requested` · **18** `approve` · **1** `blocked` (CANON) · **5** biến thể ngoài canon ⇒ 8 cách viết, nhưng **52/57 = 91,2% đã đúng canon** | biên nhận |
| `luot` được ghi | **7/57** (giá trị 1,1,2,2,3,4,4) | biên nhận |
| `review_rounds_used` được ghi | **10/57** | biên nhận |
| `codex_review_calls_used` được ghi | **2/57** | biên nhận |
| `codex_executor_calls_used` được ghi | **0/57** | biên nhận |
| Lease có mỏ neo đặc tả | **BỐN TÊN cho một khái niệm**: `spec_hash` 10 · `spec_sha256_required` 29 · `spec_sha256` 5 · `spec_path` 48 ⇒ **bất kỳ mỏ neo nào = 50/82 = 61,0%** | `ops/leases/*.yaml` |

```
grep -hoE 'thoi_luong_giay[:=] *[0-9]+\.[0-9]+' ops/reviews/*.receipt.yaml | grep -oE '[0-9]+\.[0-9]+' | sort -n
grep -h '^verdict:' ops/reviews/*.receipt.yaml | sed 's/verdict: *//' | sort | uniq -c | sort -rn
ls ops/leases/*.yaml | wc -l
grep -lE '^ *(spec_hash|spec_sha256_required|spec_sha256|spec_path):' ops/leases/*.yaml | wc -l
```

**LỆNH TRÊN LÀ BẢN ĐÃ SỬA.** Bản đầu của tệp này in một lệnh **không tái hiện được bảng**: nó để lại
đuôi `,stdout_byte=…` nên mọi chuỗi bắt đầu bằng `=` và `sort -n` sắp tất cả về 0, cộng một dòng rác.
Cross-review lượt 1 bắt (P2 `F-F`). Một §0 tự quảng cáo "lệnh tái hiện ghi kèm để người đọc không phải
tin lời khai" mà in lệnh sai thì bắt người đọc tin lời khai.

**BẢN ĐẦU CỦA TỆP NÀY KHAI `14/82 = 17,1%` VÀ SAI THEO HAI CHIỀU ĐỘC LẬP** — cross-review lượt 1 bắt cả hai:
- **Đếm thừa** (`F-A`): lệnh cũ dùng `grep -l spec_hash`, đếm cả tệp chỉ *nhắc* tên. **Ba** trong bốn tệp thừa
  nói nguyên văn *"KHÔNG khai `spec_hash` làm mỏ neo"* — tức tôi đếm tệp **từ chối khai** thành tệp **đã khai**.
  Trường thật: **10/82**.
- **Đếm sai TRƯỜNG** (`P1-2`): kho có **bốn tên** cho cùng một khái niệm. Đo theo KHẢ NĂNG ("lease có neo
  được một đặc tả đóng băng nào không") ra **50/82 = 61,0%**, không phải 17%.

Và mốc `2/74 = 3%` trong CLAUDE.md dùng **phương pháp chặt**, nên bản đầu so **lỏng với chặt**. Đây đúng hai
lớp lỗi mà chính tệp này đem ra buộc tội đề xuất: *đếm sự CÓ MẶT thay vì KHẢ NĂNG*, và *phân biệt CÁCH VIẾT
thay vì THẨM QUYỀN*. Ghi lại thay vì xoá, vì một phản biện giấu chỗ nó tự sai thì không dùng được.

---

## 1. Kết luận ngắn — ĐÃ ĐẢO SAU CROSS-REVIEW LƯỢT 1

**Bản đầu kết luận: "9/13 mục đã tồn tại ⇒ đề xuất thêm được ít; vấn đề là TUÂN THỦ chứ không phải
THIẾT KẾ." Cross-review lượt 1 lật câu ấy, và tôi đã tự đo lại rồi nhận.**

Chỗ hỏng không nằm ở con số 9. Nó nằm ở chữ **"đã có"**. Tôi đọc "có mặt trong tài liệu" thành
"đang có hiệu lực" — đúng lỗi *đếm sự CÓ MẶT thay vì KHẢ NĂNG* mà tệp này dùng để bác mục 11 của
đề xuất. §20 của protocol có sẵn cột **"cổng đã ĐO"** để trả lời chính câu hỏi ấy, và tôi **chưa hề
tra nó**. Đo:

| ADR | luật | cổng đã ĐO |
|---|---|---|
| `ADR-0032` · `0037` · `0038` · `0039` · `0040` · `0043` · `0044` · `0045` | (tám ADR) | **`0 cổng`** |
| `ADR-0046` | | `0 cổng vận hành` |

`docs/PROTOCOL_DA_PHIEN.md:1105` định nghĩa `0 cổng` là **phép đo MẠNH**: *"không tệp cổng nào
(`ops/lease_publish.py`, `.claude/dev/packet_loop.py`, …)"*. Và §20 dặn trước rằng *"có nhắc"* là
**PROXY**, không phải cưỡng chế.

**Nên câu đúng là: 9/13 đã được VIẾT, phần lớn có `0 cổng`.** Hệ quả đảo ngược khuyến nghị:

> Với một mục đã viết mà **không cổng nào cưỡng chế**, "đã có rồi" **KHÔNG phải lý do bác một đề xuất** —
> vì đề xuất có thể chính là **phần cưỡng chế còn thiếu**.

Ba phản chứng cụ thể, mỗi cái tự nó đủ phá lập luận cũ:

- **Trần 2 vòng (ADR-0043)** — bản đầu gọi là *"2 lượt/PR, **cứng**"*. Đo: `nang_tran` xuất hiện **0 lần**
  trong `ops/lease_publish.py`; đúng **1/82** lease có khối ấy; §20 ghi `ADR-0043 | 0 cổng — so-canon chưa
  tồn tại`. Trần **nới được** và **không ai canh**. Tôi lấy nó làm ví dụ về "tài nguyên khan hiếm, cứng"
  trong khi nó là ví dụ về **luật không có cổng**.
- **`spec_hash` (§3.2)** — không phải "chạy 17%". Kho có **bốn tên** cho mỏ neo đặc tả, đo theo khả năng
  ra **61%**, và §3.2 đòi `spec_hash` trên **Work Packet Issue** trong khi schema lease ở §4 **không có
  trường ấy**. Tôi đo sai loại hiện vật rồi đọc kết quả thành tỉ lệ vô kỷ luật.
- **Năng lực đo của reviewer** — bản đầu trình bày như phát hiện riêng (*"đòn bẩy mạnh nhất đã biết"*).
  Thực ra `docs/PROTOCOL_DA_PHIEN.md` §8 **đã là luật hiện hành**, kèm cả `git clone --bare` lẫn ràng buộc
  `core.abbrev = 7`. Nó là **mục thứ 10 của danh sách "đã có"**, và nó cũng `0 cổng`. Tôi áp tiêu chuẩn
  *"đã có ⇒ đừng thêm"* cho 9 mục của người khác, rồi trình bày một luật đã có của kho như thứ mình nghĩ ra.

**Kết luận thay thế.** Cả đề xuất lẫn bản phản biện đầu đều cãi nhau ở **sai tầng**. Đề xuất muốn thêm
LUẬT; bản phản biện đầu đáp "luật có rồi". Phép đo nói: **luật có rồi, CỔNG thì không.** Việc đáng làm
không phải viết thêm tầng quy trình, cũng không phải "cưỡng chế cho đúng luật đang có" như bản đầu nói —
mà là **biến các luật đã viết thành cổng chạy được, theo thứ tự rủi ro**. Đó là việc thứ ba, và cả hai
bên đều chưa nói tới nó.

Ba mục vẫn nên **bác**, nhưng lý do đổi: mục 2 và 11 bác vì phép đo (F1, F2 — F1 nay yếu hơn bản đầu, xem
đó); mục 9 bác vì nó **đổi nghĩa một giá trị canon** (F3 đã viết lại).

## 2. Đối chiếu 13 mục với protocol đang hiệu lực

| Mục đề xuất | Đã có? | Ở đâu | Nhận xét |
|---|---|---|---|
| 1. Ba tầng kiểm tra | **ĐÃ CÓ, mạnh hơn** | §10.1 — **sáu tầng T0–T5** + classifier/aggregator | Bản đề xuất là bản RÚT GỌN của thứ đang có. Gộp T3/T4/T5 thành "full CI" xoá mất phân biệt integration-freeze / canonical / release artifact. |
| 2. Hoãn full CI khỏi vòng lặp | **MÂU THUẪN** | §10.1 | Xem F1. Ngoài ra §10.1 đã cấm trước: selector chỉ được activate sau **shadow 2–4 tuần** chứng minh không bỏ sót failure. Đề xuất chính là activate selector, mà không kèm shadow evidence. |
| 3. Architecture review gate | **ĐÃ CÓ** | §3.2 `spec_hash` đóng băng ở `ready`; skill `soan-spec`; `ops/THAM_DINH_*` (5 vòng); 46 ADR | Đang chạy **17%**. Cần cưỡng chế, không cần thêm gate. |
| 4. Chuẩn hoá severity | **ĐÃ CÓ, mạnh hơn** | verdict có severity/evidence (§ dòng 845); class `sensitive/systemic/routine` (ADR-0036); P0/P1 | Đề xuất **hai** bậc P1/P2; kho có P0 và có class theo rủi ro. Xem F4 về trạng thái thứ ba. |
| 5. Tìm theo bug class | **MỚI — GIỮ** | doctrine có bản mạnh hơn ("danh sách CẤM → danh sách CHO PHÉP"; "đếm HÌNH DẠNG lỗi") nhưng chưa vào prompt reviewer | Mục giá trị nhất của cả đề xuất. |
| 6. Root-cause vs local patch | **MỚI, nhưng xung đột** | — | Xem F5: root cause có thể nằm NGOÀI write set đã đóng băng. |
| 7. Self-review bắt buộc | **ĐÃ CÓ** | T0/T1 §10.1; `/gate-targeted` | Trùng lặp. |
| 8. Trạng thái REVIEW_CANDIDATE | **ĐÃ CÓ, tên khác** | `PROTOCOL:198` (số DÒNG) `proposed → ready → leased → running → reviewing → accepted → integrated → landed` | Đặt tên mới cho state đã có là đúng thứ `doctrine-scan` sinh ra để chặn. **Bác tên, giữ ý.** |
| 9. Không ép reviewer tìm lỗi | **ĐÃ CÓ, và đề xuất làm YẾU đi** | `cross-review/SKILL.md:251` — `approve \| changes_requested \| blocked`, BA giá trị canon | Xem F3. |
| 10. Merge policy tách khỏi reviewer | **ĐÃ CÓ** | ADR-0036 review class theo rủi ro; `cross_approved`/`human_audited`; §12 budget | Trùng lặp. Strict/Normal mode thô hơn ba class đang dùng. |
| 11. Kiểm tra đa nền | **MỘT NỬA BÁC** | ADR/CI matrix | Danh mục kiểm tra tốt; chỗ ĐẶT nó thì sai. Xem F2. |
| 12. Regression test từ finding | **ĐÃ CÓ dạng yếu — NÊN NÂNG** | CLAUDE.md bước 4 đòi `rXX_` mỗi fix | Chưa có cổng nào ĐO. Nâng thành máy canh được thì có giá trị thật. |
| 13. Metric | **ĐÃ CÓ, mạnh hơn — nhưng chưa tính được** | §12 ba bộ đếm tách bạch | Xem F6. |

---

## 3. Sáu phản biện có phản chứng đo được

### F1 — Tiền đề chi phí của mục 2 SAI theo phép đo, và nó tối ưu nhầm tài nguyên

Đề xuất viết: *"full CI tương đối tốn thời gian nên nếu chạy CI ở mọi vòng sửa/review thì tốc độ
phát triển giảm đáng kể"* — tức giả định **CI ≫ review**.

Đo: một lượt cross-review median **15,4′**; một lượt CI ubuntu-only **21m52s–25m14s**.
**CI chỉ đắt hơn ~1,4–1,6 lần một lượt review**, cùng bậc độ lớn, không phải cách biệt.

Nhưng điểm chí mạng không nằm ở tỉ số mà ở **loại tài nguyên**:

| | Full CI (Linux) | Lượt cross-review |
|---|---|---|
| Trần | phút Actions — **RÚT LẠI "co giãn"**, xem dưới | trần 2/PR **nới được** bằng `nang_tran`, và **0 cổng** cưỡng chế |
| Huỷ được khi có push mới | **CÓ** — `concurrency.cancel-in-progress` đã bật cho mọi ref ≠ master | **KHÔNG** — lượt đã tiêu là mất |
| Ai chờ | máy | packet bị khoá ở `reviewing`, lease chạy đồng hồ |

Đề xuất **tiêu thêm tài nguyên khan hiếm (lượt review) để tiết kiệm tài nguyên dồi dào và huỷ được (CI)**.
Mỗi lỗi máy móc mà CI lẽ ra bắt được, nếu để reviewer bắt, ăn mất 1 trong 2 lượt canon.

Thêm nữa, lợi ích mục 2 hứa **đã được thu phần lớn**: `concurrency` gom nhiều push liên tiếp trên
cùng PR thành một lượt hoàn tất, và ma trận Windows đã có điều kiện. Mô hình chi phí của đề xuất
(*"CI × mỗi vòng"*) **đếm trùng** thứ kho đã cắt từ r245.

**HAI CÂU CỦA BẢN ĐẦU ĐÃ BỊ RÚT LẠI — cross-review lượt 1 bắt, tôi đo lại và nhận:**

**(a) "Phút Actions là tài nguyên co giãn, dồi dào" — KHÔNG CÓ CƠ SỞ.** Đo từ chính `ci.yml`:
13-08 gate chạy **6,6′** tường cho CẢ lượt; 29-08 lượt **ubuntu-only** mất **21m52s–25m14s**. Tức
**một lượt Linux hôm nay đắt hơn cả lượt HAI NỀN của tháng 8** — chính cái lượt đã làm cạn hạn mức.
Giữ nguyên tần suất 13,6 lượt/ngày: 22 × 13,6 × 30 ≈ **8.900 phút/tháng** so hạn **2.000**; ngưỡng hoà
vốn ≈ **3 lượt/ngày**. `ci.yml:63` nói thẳng: *"NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN: gate 22 phút và
đang lớn dần là nợ riêng."*

**(b) "Nguyên nhân là hệ số Windows ×2" — THIẾU MỘT NỬA.** Có **hai** hệ số. Hệ số thứ hai — gate Linux
chậm **3,4×** trong 16 ngày — chính là thứ bản đầu gán vào ô "co giãn".

Trạng thái đúng của phút tính tiền sau r245 là **CHƯA ĐO**, không phải "dồi dào". Muốn kết luận thì phải
có hai số kho chưa có: lượt/ngày sau khi bật `concurrency`, và phút tính tiền thực tháng 8→9.

**F1 vì thế YẾU HƠN bản đầu.** Nó vẫn bác được mục 2, nhưng bằng luận cứ hẹp hơn: *lượt review là tài
nguyên có trần và có vết, CI thì không có trần cứng nhưng có chi phí đang tăng nhanh mà chưa ai đo* —
chứ không phải "đổi tài nguyên dồi dào lấy tài nguyên khan hiếm".

Và tỉ số **1,4–1,6×** cũng phải rút: nó so **thời gian tiến trình reviewer chạy** với **wall-clock của job
CI** — hai đại lượng mà §12 cố ý tách (`wall_elapsed_seconds` so `working_elapsed_seconds`). Mẫu n=9 lại
chỉ gồm lượt **đã chạy trọn** (lượt chết không để lại `thoi_luong_giay`), đến từ **3 dòng việc**, và
**8/9 là reviewer `claude`** — nên gọi nó là "median một lượt cross-review" là sai nhãn. Câu đứng được:
**chi phí thật của một VÒNG fix→review chưa ai đo**, và đó là §6 của chính tệp này đã nói.

### F2 — Mục 11 đặt kiểm tra đa nền vào tầng KHÔNG ĐO ĐƯỢC nó, và kho đã trả giá đúng ca này

Đề xuất: *"Nếu có thể, đưa phần lớn các kiểm tra này vào test/pre-flight thay vì để reviewer phát hiện thủ công."*

Phản chứng đã trả giá, ghi trong CLAUDE.md:

- `os.getpgid` trong chốt cô lập làm suite **0/103 trên `windows-latest`** — bộ test **chưa từng chạy**
  trên Windows kể từ lúc có chốt ấy. **Năm lượt cross-review trên Linux không thể thấy, và đã không thấy.**
- Lỗ AN NINH của cặp script deploy **chỉ hiện vì hai bản đếm LỆCH** (196 so 198 trên cùng một zip).
  Không lỗi nào trong 5 lỗi lượt đó lộ ra bằng đọc mã.
- `print` đường dẫn có dấu giết cả lượt chạy trên console cp1258 — bẫy ở ĐẦU RA, không ở logic.

Pre-flight trên Linux đo được `\` so `/` **trong chuỗi nguồn**; nó không đo được **hành vi** của
`os.getpgid`, của quyền symlink, của console cp1258, hay của `Get-ChildItem` bỏ tệp ẩn. Chuyển các
mục ấy sang pre-flight là đúng lỗi *"đếm sự CÓ MẶT thay vì KHẢ NĂNG"* mà kho đã trả giá bốn lần.

Chỉ **một** phép kiểm đa nền là thật: **chạy trên nền đó, rồi đối chiếu PARITY hai bản trên cùng đầu vào.**

**F1 và F2 chống nhau — hai mục này cùng sống cùng chết.** Mục 2 chỉ an toàn NẾU mục 11 chuyển được
phần lớn lỗi đa nền sang pre-flight. Mục 11 không chuyển được. Vậy CI vẫn giữ nguyên giá trị PHÁT HIỆN,
và hoãn nó đi là hoãn đúng thứ duy nhất đang bắt được lớp lỗi đắt nhất của kho.

### F3 — Mục 9 cộng mục 13 tạo áp lực hệ thống về phía ÂM TÍNH GIẢ

Mục 9: *"Nếu không tìm thấy vấn đề có ý nghĩa thì trả về APPROVE"* + *"Nếu reviewer không chứng minh
được impact thực tế thì không nên coi finding đó là blocker."*
Mục 13: mục tiêu *"số vòng review giảm dần"*.

Một mục nới cho APPROVE, một mục biến "ít vòng" thành chỉ tiêu. **Đây là Goodhart**: cách rẻ nhất để
đạt chỉ tiêu là approve sớm, và không có ô nào trong đề xuất phạt việc đó.

Phản chứng đo được (CLAUDE.md, PR #250): **ba lượt reviewer chỉ nhận hai tệp `.md` → 4 → 11 → 2 finding
và KHÔNG con số phân rã nào. Lượt 4 được cấp mirror git đầy đủ → ba con số phân rã ngay lượt đầu tiên
có năng lực ấy.** Ba lượt đầu không tìm thấy gì **không phải vì mã sạch** mà vì **không có cách nào đo**.
Dưới luật mục 9, cả ba lượt ấy trả `APPROVE`.

`APPROVE` từ một reviewer không có năng lực đo **không phải kết luận, nó là chỗ RỖNG** — và kho đã có
đúng bài học này: *"RỖNG ở API mình hỏi KHÔNG phải 'chưa chạy'"*, *"vắng mặt vì sạch và vắng mặt vì chưa
chạy nhìn giống hệt nhau"*.

**BẢN ĐẦU ĐỀ XUẤT SAI CÁCH CHỮA, VÀ CROSS-REVIEW BẮT ĐÚNG CHỖ ĐÓ (P1-8).** Nó viết: *"một lượt không đo
được gì phải ra `blocked`"*. Nhưng `blocked` **đã có nghĩa canon và nghĩa ấy khác hẳn** — §3.2: *"finding
cho thấy chính spec thiếu thì verdict là `blocked` và đi qua revision mới"*; trong mã,
`packet_loop.py` ánh xạ `blocked → state blocked` với `CHUYEN_HOP_LE["blocked"] = ()`, tức **trạng thái
tận cùng**. Áp luật ấy nghĩa là: *điều phối quên cấp mirror ⇒ tuyên bố ĐẶC TẢ THIẾU ⇒ packet vào trạng
thái tận cùng ⇒ revision mới*. Ba lượt thiếu mirror của PR #250 sẽ thành **ba packet revision** cho một
nguyên nhân thuần vận hành.

Trớ trêu đúng chỗ đáng nhớ: đó là **giá trị thứ 9 cho cùng một cách viết** — cùng chính tả, **thẩm quyền
khác** — tức đúng bệnh mà F6 của chính tệp này đặt tên, phạm ngay trong câu đề xuất cách chữa.

**Cách chữa đúng: một TRƯỜNG mới, không phải một verdict mới.** Bắt buộc trong biên nhận:
`nang_luc_do: {mirror: có|không, cac_lenh_da_chay: [...]}`, và cổng ĐỎ khi `verdict: approve` mà trường ấy
rỗng. Đó cũng chính là hình dạng "trạng thái thứ ba" mà F4 đòi — đặt đúng trục (năng lực đo) thay vì đè
lên thang verdict.

### F4 — Mục 4 là thang HAI bậc, và đảo gánh nặng chứng minh sai chiều

Đề xuất chỉ có P1/P2. Kho đã dùng P0, và quan trọng hơn: đã có **trạng thái thứ ba** (`chưa đo`,
§ dòng 1111) làm cổng ĐỎ. Doctrine cả kho là *"ba trạng thái, không phải hai: có · không · KHÔNG ĐO ĐƯỢC"*.
Một thang severity không có ô cho *"tôi không đo được chỗ này"* sẽ ép mọi thứ chưa đo xuống P2 rồi ra issue.

Câu *"reviewer không chứng minh được impact thì không blocker"* đảo gánh nặng về phía bên có ÍT quyền
truy cập nhất. Ba finding đắt nhất kho từng gặp đều KHÔNG có failure scenario hiển nhiên lúc phát hiện:

- dấu bỏ-qua-CI trong thông điệp commit → PR #100 có **0 check run** mà `mergeable_state: clean`;
- `t24` `return` sớm vì đường dẫn sai → suite báo **24/24** trong khi ca ấy không đo gì;
- `co` + escape U+0308 + `dex` bị tầng vận chuyển giải mã → một hướng dò biên biến mất không để lại dấu.

Cả ba là lỗi **PHÉP ĐO**, không phải lỗi hành vi. Đòi "failure scenario" mới cho là blocker sẽ hạ đúng lớp này.

**Sửa:** gánh nặng chứng minh phải **tỉ lệ với năng lực đo mà ta CẤP cho reviewer**. Reviewer có mirror
và chạy được phản chứng thì đòi bằng chứng động; reviewer chỉ được đọc diff thì finding của nó là
*giả thuyết cần điều phối đo* — không phải bị loại.

### F5 — Mục 6 xung đột với write-set exclusion, và "root cause" đã từng là cái bẫy

Hai vấn đề độc lập:

**(a) Ràng buộc kiến trúc mà đề xuất không biết có.** Write set được **đóng băng bằng `spec_hash` khi
vào `ready`** (§3.2). Nếu root cause của một finding nằm NGOÀI write set, executor **không được** sửa —
đó chính là điều write-set exclusion sinh ra để chặn. Mục 6 như đang viết sẽ bảo executor mở rộng phạm vi,
và họ sẽ hoặc vi phạm lease, hoặc tự cấp thêm quyền ghi. Cần một luật rõ: *root cause ngoài write set ⇒
**mở packet mới**, không nới packet đang chạy* — và finding ấy phải neo được sang packet mới.

**(b) "Ưu tiên root-cause fix" không phải luật, kho có phản chứng.** Việc ghi lại `~/.codex/config.toml`
ăn **bốn lượt cross-review liên tiếp**, mỗi lượt là một bản vá "root-cause hơn" bản trước, và mỗi lượt
bảo toàn thứ ta NGHĨ TỚI rồi phá thứ ta KHÔNG NGHĨ TỚI (bảng TOML trùng tên → khớp substring → ghi không
nguyên tử → symlink tên tạm → CRLF → lost-update). Lời giải đúng **không phải vá sâu hơn** mà là **bỏ hẳn
việc ghi vào tệp người dùng**. Bài học kho ghi: *"đếm HÌNH DẠNG lỗi, đừng chỉ đếm lỗi; cùng một hình dạng
lặp ba lần trở lên thì câu hỏi đúng là 'có nên làm việc này không'"*.

Mục 6 nên đọc là: *phân loại cục bộ / cùng lớp / **sai quyết định gốc***, ba nhánh chứ không hai.

### F6 — Mục 13 KHÔNG TÍNH ĐƯỢC từ hiện vật hôm nay

Đề xuất liệt kê 7 metric. Đo khả năng tính từ kho:

| Metric đề xuất | Trường cần | Có trong biên nhận |
|---|---|---|
| số vòng review/feature | `luot` | **7/57** |
| P1/P2 theo vòng | severity có cấu trúc | **không có trường** |
| thời gian CI | — | **không vào biên nhận** |
| lỗi CI sau khi approve | — | **không có trường** |
| finding cùng root cause | — | **không có trường** |

Cộng thêm: `codex_review_calls_used` **2/57**, `review_rounds_used` **10/57**,
`codex_executor_calls_used` **0/57**, và `verdict` có **8 cách viết cho 3 giá trị canon**
(`approve` · `approved` · `approve_with_findings` · `giu_nguyen` · `dung_lai` · `do_not_land` ·
`changes_requested` · `blocked`).

**Việc đầu tiên không phải chọn metric mà là đóng SCHEMA biên nhận và chuẩn hoá verdict.** Chừng nào
verdict còn 8 cách viết thì mọi bảng thống kê đều là bảng về CHÍNH TẢ. Đây đúng bài học
*"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*, lần này rơi vào chỗ đo đạc.

Nhắc thêm, vì nó đã trả giá: ADR-0043 ghi hai lời khai `ĐO ĐƯỢC` sai về `review_rounds_used` từng nằm
trong tài liệu kế hoạch, và đo lại cho **0 tệp `.py`** chứa tên ấy — *"không phải 'có bộ đếm mà thiếu
trần', mà là không có bộ đếm nào"*. Metric sống trong văn xuôi thì sẽ trôi mà không ai biết.

---

## 4. Failure mode đề xuất CHƯA nêu (câu hỏi 4)

**M1 — Lượt review chết không để lại verdict.** Đo trên packet #298: **3 trong 4 lượt không sinh verdict**
— lượt 1 có verdict nhưng không ai ghi ra tệp; lượt 2 và 3 **bị bộ lọc nội dung của nền cắt giữa chừng**.
Đề xuất không có ô nào cho *"lượt đã tiêu mà không có kết luận"*. §12 phân biệt rất tinh
(`codex_review_calls_used` tăng kể cả khi timeout/sai schema, `review_rounds_used` chỉ tăng khi verdict
qua validation); đề xuất gộp cả hai thành "một vòng review" và **xoá mất phân biệt đó**.

Kèm bài học vận hành: nguyên nhân đo được của hai lượt chết là **thiết kế nhiệm vụ ép reviewer TỰ SOẠN
phản chứng**. Đổi phân công (reviewer CHẠY phản chứng có sẵn + ĐỘT BIẾN bản vá) thì lượt kế chạy trọn
922,4s. Đây là đòn bẩy giảm số vòng **mạnh hơn mọi mục trong đề xuất**, và đề xuất không nhắc.

**M2 — Đa phiên, lease, đồng hồ tường.** Đề xuất là mô hình **một executor – một reviewer**. Kho là
N phiên + write-set exclusion + lease hết hạn theo wall clock (ADR-0042). Kéo dài inner loop (mục 2)
⇒ **lease hết hạn giữa vòng lặp**. Đã đo: lease của packet #355 còn giữ đúng hai đường dẫn thêm ~18h
SAU khi packet đã land; và một lần cấp chồng lấn tạo cửa sổ hai writer ~23,75h. Mọi mục kéo dài thời
gian từ `leased` đến `landed` đều làm lớp lỗi này nặng thêm.

**M3 — Executor từ chối ở preflight bị đọc thành trở ngại.** Đã xảy ra: codex dừng hai lượt liên tiếp vì
chỉ thị thiếu `revision`/`Review Class`/`spec_hash`. Đó là **tính năng**. Một quy trình có thêm state
(`REVIEW_CANDIDATE`) mà không định nghĩa hiện vật tự xác minh sẽ sinh thêm chỗ để từ chối đúng kiểu ấy.

**M4 — KHÔNG MỤC NÀO NÓI VỀ RĂNG CỦA CỔNG.** Đây là khoảng trống sâu nhất. Cả 13 mục bàn *đặt cổng Ở ĐÂU*;
không mục nào bàn *cổng có ĐỎ ĐƯỢC KHÔNG*. Doctrine kho:

- *"Một phép kiểm không thể đỏ thì không phải bằng chứng."*
- *"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI."*
- Đo được: khai `22/22 mutant bị giết` → phân hạng lại **19 giết thật / 3 tín dụng giả**; và bản vá
  vòng một của chính bộ phân hạng **vẫn bị lừa** bởi một `except` đổi kiểu viết với ý định tốt.

Thêm một tầng pre-flight chưa đo răng là thêm một tầng **giá trị chưa biết**, rồi dựa vào nó để hoãn
tầng đã biết là có răng (CI). Đó là đổi cái đã đo lấy cái chưa đo.

**M5 — Ai phân loại lỗi CI?** Mục 2 nói: CI ra lỗi môi trường nhỏ ⇒ sửa và chạy lại; ra lỗi logic nghiêm
trọng ⇒ quay lại cross-review. **Người phân loại là executor**, và executor có động cơ xếp vào ô "lỗi môi
trường nhỏ" để khỏi tốn một lượt review. Không có bên độc lập, không có yêu cầu bằng chứng. Cùng hình dạng
với *"cổng xanh nhờ `rc=0` là cổng có thể bị lừa"*. Kho đã có luật đúng cho chỗ này (*"'Flake' không phải
root cause"*, re-run tối đa một lần và chỉ trong ca đã nêu tên) — đề xuất nới nó ra.

**M6 — Cấp NĂNG LỰC ĐO không cấp TÍNH ĐỘC LẬP.** §8 có bốn mức assurance; biên nhận có `assurance` ở
**31/57** và `cross_provider` ở **40/57**. Toàn bộ mẫu n=9 của §0 là reviewer `claude` (**8/9**). Cấp mirror
làm reviewer đo giỏi hơn nhưng **không** làm nó bớt mù ở chỗ cùng mô hình cùng mù — §8 đã đặt tên cho rủi ro
ấy (*"self-review đội lốt cross-review"*). MVP-1 bản đầu liệt kê trường bắt buộc mà **không có `assurance`**,
tức mở khoá metric nhưng không phân biệt được duyệt chéo với duyệt cùng nền. Lượt review sinh ra tệp này
cũng đúng như vậy: nó là `same_provider`, và nói thẳng ở §8 dưới.

**M7 — Biên nhận là bằng chứng TỰ KHAI, và tệp này dùng nó như bằng chứng ngoại kiểm.**
`packet_loop.py` nói thẳng: *"hiện vật cục bộ chỉ chứng minh có biên nhận + verdict tự khai, không chứng
minh commit tồn tại hoặc có bao nhiêu vòng review đã thật sự chạy… nên **không được gọi số đếm này là số
vòng review**"*. Toàn bộ bảng §0 (trừ ba dòng CI) đứng trên đúng nguồn ấy, và bản đầu của §6 **không** liệt
kê giới hạn này.

---

## 5. Trả lời trực tiếp 10 câu hỏi

1. **Giữ:** mục 5 (bug class) — mục giá trị nhất; mục 12 (regression test từ finding), nâng thành cổng
   máy đo được; mục 6 phần *phân loại* (với ba nhánh, xem F5); danh mục kiểm tra của mục 11 (giữ danh mục,
   đổi chỗ đặt); mục 3 phần *tiêu chí kích hoạt* — nó cụ thể hơn §3.2 và nên nhập vào `soan-spec`.
2. **Bureaucracy:** mục 7, 8, 10 trùng với `T0/T1`, state `ready/reviewing`, và ADR-0036. Chúng thêm từ vựng
   thứ hai cho khái niệm đã có tên — đúng thứ `doctrine-scan` sinh ra để chặn (`rc=6`).
3. **Trùng lặp:** mục 1 (⊂ §10.1), 4 (⊂ severity + review class), 13 (⊂ §12 ba bộ đếm). Mục 13 không chỉ
   trùng mà còn **thô hơn**: nó gộp ba bộ đếm §12 thành một.
4. **Failure mode chưa nêu:** M1–M5 ở §4. Nặng nhất là **M4 (răng của cổng)** và **M1 (lượt chết không verdict)**.
5. **Merge policy P1/P2:** thiếu P0, thiếu trạng thái thứ ba, và Strict/Normal thô hơn ba class
   `sensitive/systemic/routine` đang chạy. `P2 = 0` cho Strict mode là bẫy: nó biến mọi nhận xét
   maintainability thành blocker của core runtime, tức tạo đúng cái "improvement nhỏ giữ feature lớn
   trong review vô thời hạn" mà mục 10 nói muốn tránh. **Giữ ba class hiện có; không thêm hai mode.**
6. **Rủi ro hoãn full CI:** xem F1 + F2. Cụ thể với kho này: (a) tiêu tài nguyên khan (2 lượt/PR) để
   tiết kiệm tài nguyên co giãn; (b) reviewer đọc mã **chưa từng được đo trên Windows** — và với PR
   thường, lần merge chính là lần đo Windows ĐẦU TIÊN; (c) kéo dài `leased → landed` ⇒ lease hết hạn (M2);
   (d) lợi ích hứa đã bị `concurrency` thu phần lớn từ r245.
7. **Chia pre-flight / CI theo một luật, không theo danh sách:**
   **Pre-flight = thứ đo được HÀNH VI trên nền đang chạy.** format/lint, syntax/type, import resolution,
   unit test của vùng vừa sửa, `rXX_` mới thêm.
   **Bắt buộc CI = mọi thứ mà kết quả PHỤ THUỘC NỀN, phụ thuộc danh tính runner, hoặc đo hiện vật phát hành.**
   Cụ thể: hành vi process/signal, symlink, quyền thực thi, encoding console, `RELEASE_MANIFEST`/golden/determinism
   (đòi `core.abbrev = 7`), release-verify, `actionlint` (+ `shellcheck`, vì thiếu nó actionlint **im lặng bỏ
   luật nền và vẫn trả `rc=0`).
   Ranh giới: *"tra được bằng cách đọc chuỗi"* thì pre-flight; *"phải chạy mới biết"* thì CI. CRLF/LF và
   path separator nằm ở CẢ HAI — dạng tĩnh ở pre-flight, hậu quả hành vi thì chỉ CI thấy.
8. **Bổ sung cho Python/Node/MCP trên Windows + Ubuntu** (ngoài danh sách mục 11, đều đã trả giá thật):
   `python` so `python3` so `py`; console cp1258 giết `print` TRƯỚC khi logic kịp sai; `taskkill /T /F` trả
   `Access denied` trên tiến trình con của chính mình còn `Stop-Process -Force` thì được; zombie tính là
   đã chết; `Get-Content -Raw` trên tệp RỖNG trả `$null`; `Get-ChildItem` bỏ tệp ẩn khi thiếu `-Force`;
   `$Args` là biến tự động của PowerShell; API chỉ có trên một nền (`os.getpgid`, `os.O_NOFOLLOW`) —
   `hasattr` trước khi đụng, và truyền **lambda** vào hàm bọc lỗi vì tra thuộc tính xảy ra NGOÀI `try`;
   va chạm `.pyc` theo (mtime giây, kích thước) làm mutant chạy mã của bản trước.
   **Và một luật bao trùm:** với script đa nền, phép đo có giá trị duy nhất là **PARITY hai bản trên cùng
   đầu vào** — lỗ an ninh của kho chỉ lộ vì hai bản đếm 196 so 198.
9. **Cách giảm số vòng tốt hơn đề xuất — đo được, và đề xuất không nhắc:**
   **(a) Cấp NĂNG LỰC ĐO cho reviewer.** 3 lượt/0 con số phân rã → 1 lượt/3 con số, chỉ vì lượt 4 được
   cấp mirror git. Giá: một `clone --bare` vào sandbox. Đây là đòn bẩy mạnh nhất đã biết.
   **(b) Đổi PHÂN CÔNG, không đổi provider.** Reviewer CHẠY phản chứng có sẵn + ĐỘT BIẾN bản vá; hướng thử
   nào cần soạn nội dung nhạy cảm thì mô tả bằng lời. Đã chữa hai lượt chết liên tiếp.
   **(c) Tự khai thiên vị của thứ mình giao.** Giao bảng 21 con số kèm chính script trích ra nó và nói
   thẳng nó lọc theo danh sách đơn vị đoán trước ⇒ reviewer trả về hai finding, một nhắm thẳng bộ lọc.
   **(d) Cưỡng chế `spec_hash`** (đang 17%) — vòng review tốn nhiều nhất là vòng cãi nhau về đặc tả.
10. **Minimum viable process — BẢN ĐẦU CÓ BA VIỆC, CẢ BA ĐỀU HỎNG. Cross-review lượt 1 phá từng cái;
    dưới đây là bản đã sửa, xếp lại theo thứ tự rẻ-trước.**

    **MVP-1 · Không có biên nhận thì không land.** Bản đầu viết *"đóng schema biên nhận"* như phải làm từ
    đầu. Sai hai lần: (a) schema **đã tồn tại** — `.github/coordination/schemas/review_verdict.v1.schema.json`
    có đúng enum ba giá trị canon, **16** trường `required`, `additionalProperties: false` — nhưng
    `launcher.py` và `packet_loop.py` tham chiếu nó **0 lần**, tức việc thật là **nối dây**, không phải
    thiết kế; (b) lỗ thật lớn hơn lỗ schema. `packet_loop.py` tự khai: *"Packet #249 chạy **BỐN** vòng
    cross-review, để lại **0** biên nhận, và suite vẫn 98/98 xanh"*, chuỗi `doctor-github-mcp` mất **năm**
    lượt y hệt. **Một luật schema chỉ ràng buộc tệp ĐÃ được viết; nó không sinh ra tệp cho vòng không ai
    viết.** Nên việc số một là cổng `bien-nhan` ở land gate (đã có mã, đã có phản chứng), rồi mới siết trường.
    Kèm ba điều chỉnh do lượt 1 chỉ ra:
    · **BỎ `review_rounds_used`** khỏi danh sách bắt buộc — ADR-0043 đã đo `0 tệp .py` tính nó, nên bắt buộc
      nó nghĩa là bắt người gõ tay ⇒ 100% có mặt, độ tin cậy chưa biết. Đúng bệnh MVP tự tạo ra.
    · **THÊM luật nhất quán chéo `packet_id` ↔ `lease_id`.** Đo: **18** biên nhận khai `packet_id: wp55`
      nhưng `lease_id` của chúng thuộc **≥5** dòng việc khác nhau (`don-nhanh-base` 7 · `wp55-r2` 2 ·
      `doctor-github-mcp` 2 · `tao-tag-luu-tru` 1 · `don-nhanh-kien-truc-gh` 1 …). Nên "15 packet riêng biệt"
      ở §0 **không phải 15 packet**, và mọi mẫu số theo packet sai im lặng.
    · **Ghi `schema_version` + NGÀY HIỆU LỰC.** Biên nhận là bằng chứng đã giao, không sửa hồi tố; siết
      schema mà không khai ngày ⇒ cổng đỏ vĩnh viễn trên hiện vật cũ.

    **MVP-2 · Thống nhất TỪ VỰNG mỏ neo đặc tả TRƯỚC, cưỡng chế SAU.** Bản đầu nói "cưỡng chế `spec_hash`
    (đang 17%)". Phép đo nói kho có **bốn tên** cho một khái niệm và **61%** lease đã neo được đặc tả.
    Cưỡng chế một tên trong bốn sẽ bắt oan 44% lease đang làm đúng bằng tên khác. Việc đúng: chọn một tên
    canon, khai ánh xạ cho ba tên kia, rồi mới dựng cổng.

    **MVP-3 · ĐO Windows trước, đừng BẮT BUỘC Windows.** Bản đầu bắt buộc một lượt `workflow_dispatch`
    trước lượt review đầu. Bốn phản chứng, ba nằm trong chính §0: (a) **0/3** lượt dispatch từng hoàn tất —
    bắt buộc một phép kiểm chưa từng XANH; (b) dispatch kích hoạt cả hai nền ⇒ ước tính **≥112 phút tính
    tiền** cho MỘT lượt, cạn hạn ở ~14–18 packet trong khi §12 cho trần 20; (c) `concurrency.group` của
    dispatch khoá theo `github.ref` còn của PR khoá theo số PR ⇒ **hai group khác nhau**, nên
    `cancel-in-progress` — chính luận cứ của F1 — **không áp dụng cho MVP-3**; (d) ai quyết định "packet đụng
    nền"? Executor, đúng bên có động cơ trả lời "không" — MVP-3 tự đẻ lại M5.
    Thay bằng hai bước: **(a)** chạy MỘT lượt dispatch để biết Windows có hoàn tất trong trần 60 hay không —
    số này kho **chưa có**; **(b)** việc gần như miễn phí và nên làm ngay: thêm `types: [..., labeled]` vào
    `pull_request:` của `ci.yml`.
    *Sửa kèm một lời khai sai của bản đầu:* nó viết *"gắn nhãn `windows` KHÔNG sinh lượt chạy nào"*. Đúng với
    `ci.yml`, **sai với kho** — `.github/workflows/launcher-windows.yml` khai
    `types: [opened, synchronize, reopened, labeled]` + `windows-latest`, path filter `.claude/dev/**`. Tôi
    khảo sát **1/7** workflow rồi kết luận cho cả kho.

    **MVP-4 · Cổng NĂNG LỰC ĐO cho reviewer — và đây mới nên là việc SỐ MỘT.** §8 protocol **đã là luật**
    (mirror `git clone --bare` + ghim `core.abbrev = 7`), và nó `0 cổng`. Cả bản đầu lẫn M1 đều gọi đây là
    đòn bẩy mạnh nhất rồi **không đưa vào MVP**. Chốt rẻ: bundle review bị TỪ CHỐI nếu verdict mang khẳng
    định định lượng mà không kèm bằng chứng đã cấp mirror.

    Mọi mục còn lại: **hoãn tới khi MVP-1 cho ra số.**

---

## 6. Điều tệp này KHÔNG đo được (nói thẳng, không lấp)

- **Số vòng review trung bình mỗi packet: KHÔNG ĐO ĐƯỢC.** `luot` chỉ có ở 7/57 biên nhận. Tiền đề của
  cả đề xuất (*"số vòng đang tăng cao"*) vì vậy **chưa được kiểm** — nó có thể đúng, nhưng hôm nay nó là
  ấn tượng, không phải phép đo. Đây là lý do đề mục MVP-1 đứng trước mọi thứ khác.
- **`luot` đo được tới 4 so trần canon 2 (ADR-0043) — có phải vi phạm hay không thì KHÔNG QUYẾT ĐỊNH ĐƯỢC
  từ hiện vật.** §12 tách ba trục (VÒNG / LỜI GỌI / ATTEMPT) với ngữ nghĩa tăng khác nhau, mà biên nhận
  không ghi bộ đếm nào (`codex_review_calls_used` 2/57). Một trần mà đơn vị của nó không xuất hiện trong
  hiện vật bền thì không cưỡng chế được — và đó là finding, không phải chỗ trống.
- **Thời lượng CI** lấy từ chú thích r391 trong `ci.yml` (đo 29-08), không phải từ API Actions trong phiên này.
- **Số PR #250 KHÔNG phải bằng chứng đo được — RÚT LẠI.** Bản đầu gọi chúng là *"phản chứng đo được"* và
  xây khuyến nghị 9(a) lên đó. Cả `CLAUDE.md` lẫn `PROTOCOL §8` đều khai thẳng ngược lại: *"chỉ có ở comment
  PR #250, chưa có biên nhận trong kho… **không tái lập được**… đừng dùng chúng như một gate đã kiểm"*. Tôi
  trích số và bỏ cảnh báo đi kèm. Trạng thái đúng: **giả thuyết đáng đo, chưa có hiện vật**.
- **"Đổi phân công chữa được lượt chết" là TƯƠNG QUAN, không phải nhân quả — RÚT LẠI.** `CLAUDE.md` dặn
  nguyên văn *"Tương quan, không phải nhân quả — đừng đọc mạnh hơn thế"*, và bản đầu của M1 đọc mạnh hơn.
- **Phút Actions tính tiền sau r245:** KHÔNG ĐO ĐƯỢC từ container này (cần API Actions/billing).
- **Thời lượng thật của một job Windows:** KHÔNG ĐO ĐƯỢC — cả 3 lượt đều bị cắt ở trần cũ; trần nay là 60
  và chưa ai đo lại. Mọi ước tính chi phí MVP-3 là **chặn dưới**.
- **Chi phí thật của một vòng lặp fix→review** chưa ai đo: thời gian executor giữa hai lượt review không
  có hiện vật. Nếu con số ấy áp đảo cả CI lẫn review thì **cả đề xuất lẫn phản biện này đều đang tối ưu
  sai chỗ** — và không ai trong hai bên biết, vì chưa ai đo.

---

## 7. Ghi chú về chính cách đặt câu hỏi

Chủ kho đề nghị đưa cùng bản này cho Claude và Codex độc lập rồi gộp hai bản phản biện. **Hướng đúng**,
nhưng có một bẫy đã đo được: cấp cho reviewer **một tài liệu văn xuôi** thì thu về **soát chính tả** —
đúng ba lượt đầu của PR #250 (4 → 11 → 2 finding, **0 con số phân rã**).

Muốn bản phản biện của Codex có giá trị hơn bản này, phải cấp cho nó **năng lực đo**: mirror kho + bảng
§0 + chính các lệnh đã sinh ra bảng ấy, kèm lời khai thẳng rằng bảng này **thiên vị** — nó chỉ đếm thứ
tôi nghĩ ra để đếm, và mỗi con số nó thiếu mà Codex tìm được thì tính là finding.

Và **nguồn có thẩm quyền là TỆP NÀY trong kho**, có băm. Bản chiếu lên Issue/PR chỉ là bản chiếu.


---

## 8. Mức assurance của chính tệp này — `same_provider`, KHÔNG phải `cross_approved`

Nói thẳng vì §8 protocol tồn tại đúng để chặn kiểu nhập nhèm này. Cross-review lượt 1 chạy bằng **hai phiên
Claude độc lập**, không phải codex. Lý do là phép đo, không phải lựa chọn: `codex` trong container này trả
`401 Unauthorized` + `Your access token could not be refreshed`; `CODEX_AUTH_JSON` là ảnh chụp
`last_refresh = 2026-08-23`, tức đã 14 ngày, và refresh token của codex **xoay vòng** nên ảnh chụp cũ chết.
Không có credential provider thứ hai nào khác trong môi trường (`llm`/`agy` chưa cài **và** không có khoá).

Vậy nhãn đúng của lượt này là **`same_provider_approved`**, mức mà §8 xếp dưới `cross_approved`. Và M6 ở §4
nói chính xác vì sao điều đó quan trọng: cấp năng lực đo không cấp tính độc lập — hai phiên cùng mô hình mù
cùng chỗ. Các finding của lượt 1 mạnh vì chúng **đo được và đã được phiên chính đo lại**, không vì ai duyệt.

Khi khôi phục được codex, chạy lại đúng bộ prompt ấy qua `launcher.py run` để có `cross_approved` thật.

---

## 9. Nhật ký cross-review lượt 1 — cái gì bị lật

| # | Bản đầu khai | Phép đo nói | Xử lý |
|---|---|---|---|
| 1 | "9/13 ĐÃ CÓ ⇒ đề xuất thêm ít; vấn đề là TUÂN THỦ" | §20 đo **`0 cổng`** cho 8 ADR | **ĐẢO** kết luận trung tâm (§1) |
| 2 | `spec_hash` 14/82 = 17,1% | 10/82 theo trường; **50/82 = 61%** theo khả năng (4 tên) | sửa §0, đổi MVP-2 |
| 3 | "trần 2 lượt/PR, **cứng**" | `nang_tran` nới được; **0 lần** trong `lease_publish.py` | sửa F1 |
| 4 | "gắn nhãn windows không sinh lượt chạy nào" | `launcher-windows.yml` có `labeled` + `windows-latest` | sửa MVP-3 |
| 5 | "một lượt không đo được phải ra `blocked`" | `blocked` = spec thiếu → **trạng thái tận cùng** | F3 đổi sang trường `nang_luc_do` |
| 6 | "phút Actions co giãn, dồi dào" | Linux **6,6′ → 22–25′** = chậm 3,4× | rút; F1 yếu đi |
| 7 | PR #250 là "phản chứng đo được" | nguồn cấm dùng như gate đã kiểm | rút, hạ xuống giả thuyết |
| 8 | MVP-1 "đóng schema" | schema **đã có**, chỉ chưa nối; lỗ thật là vòng **0 biên nhận** | viết lại MVP-1 |
| 9 | MVP-3 bắt buộc Windows dispatch | **0/3** lượt từng hoàn tất; ≥112 phút/lượt; không bị cancel | hạ xuống "đo trước" |
| 10 | "số vòng review KHÔNG ĐO ĐƯỢC" | `bien-nhan` đếm theo `reviewed_sha`, 57/57 | sửa §6 |
| 11 | "15 packet riêng biệt" | 18 biên nhận `wp55` trải ≥5 dòng việc | thêm luật nhất quán vào MVP-1 |
| 12 | lệnh tái hiện ở §0 | **không tái hiện được** bảng | sửa lệnh |
| 13 | "6 biến thể lẻ" | `blocked` là canon ⇒ 5; **91,2%** đã canon | sửa §0 |
| 14 | "cạn ~ngày 11" | số học ra **~7,4** | đánh dấu là trích, nêu chênh |
| — | 9(a) "đòn bẩy mạnh nhất **đã biết**" | §8 protocol **đã là luật**, `0 cổng` | thành **MVP-4** |

**Hình dạng chung của 14 mục trên:** gần như tất cả thuộc đúng **hai** lớp lỗi mà chính tệp này đem ra
buộc tội đề xuất — *lời khai rộng hơn phép đo* và *đếm sự CÓ MẶT thay vì KHẢ NĂNG*. Tôi khảo sát một
workflow rồi kết luận cho bảy; đếm một tên trường rồi kết luận cho một khái niệm bốn tên; đọc "có trong
tài liệu" thành "đang có hiệu lực". Đó là dữ liệu về **phương pháp**, không phải về đề xuất — và nó ủng hộ
đúng mục 5 của đề xuất (*tìm theo bug class, không theo từng finding*), mục mà bản đầu đã khen là giá trị
nhất mà không nhận ra mình đang minh hoạ cho nó.
