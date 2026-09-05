# Phản biện đề xuất "Cải tiến quy trình Build – Review – CI"

- **Ngày đo:** 05-09-2026 · **HEAD:** `c03a409` (= `origin/master`) · **Người viết:** phiên Claude Code
- **Trạng thái:** phản biện thiết kế, CHƯA thi công. Không sửa mã, không mở packet.
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
| Verdict | **33** `changes_requested` · **18** `approve` · **6** biến thể lẻ ⇒ **8 cách viết cho 3 giá trị canon** | biên nhận |
| `luot` được ghi | **7/57** (giá trị 1,1,2,2,3,4,4) | biên nhận |
| `review_rounds_used` được ghi | **10/57** | biên nhận |
| `codex_review_calls_used` được ghi | **2/57** | biên nhận |
| `codex_executor_calls_used` được ghi | **0/57** | biên nhận |
| Lease có `spec_hash` | **14/82 = 17,1%** | `ops/leases/*.yaml` |

```
grep -h thoi_luong_giay ops/reviews/*.receipt.yaml | sed 's/.*thoi_luong_giay:* *//' | tr -d ' `' | sort -n
grep -h '^verdict:' ops/reviews/*.receipt.yaml | sed 's/verdict: *//' | sort | uniq -c | sort -rn
ls ops/leases/*.yaml | wc -l ; grep -l spec_hash ops/leases/*.yaml | wc -l
```

**Một số trong CLAUDE.md đã trôi và tệp này sửa lại:** doctrine ghi `spec_hash` đạt **2/74 = 3%** (đo 28-08).
Đo lại hôm nay: **14/82 = 17,1%**. Bài học đứng nguyên, con số minh hoạ thì hết hạn — đúng lớp "một con số
trong tài liệu không ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết".

---

## 1. Kết luận ngắn

**Đề xuất được viết như cho một kho CHƯA CÓ quy trình. Kho này đã có, và ở dạng mạnh hơn.**
9 trong 13 mục đã tồn tại trong `docs/PROTOCOL_DA_PHIEN.md` — thường chi tiết hơn bản đề xuất.
Phần thật sự MỚI chỉ còn mục 5 (bug class), mục 12 (regression test từ finding) và một nửa mục 11.

Ba mục nên **bác**: mục 2 (hoãn full CI) vì tiền đề chi phí sai theo phép đo; mục 11 phần
"đưa kiểm tra đa nền vào pre-flight" vì Linux không đo được Windows và kho đã trả giá đúng ca đó;
mục 9 (nới cho APPROVE) vì cộng với mục 13 nó tạo áp lực hệ thống về phía **âm tính giả**.

**Vấn đề thật của kho không phải THIẾU quy trình mà là quy trình đang có KHÔNG ĐƯỢC CƯỠNG CHẾ.**
Trần vòng review là **2** (ADR-0043, canon) mà `luot` đo được tới **4**. `spec_hash` là bắt buộc khi
vào `ready` (§3.2) mà thực tế **17%**. Thêm một tầng quy trình mới lên trên một tầng đang chạy 17%
thì tầng mới cũng sẽ chạy 17% — và ta sẽ có hai tầng cùng không có răng thay vì một.

---

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
| 8. Trạng thái REVIEW_CANDIDATE | **ĐÃ CÓ, tên khác** | §198 `proposed → ready → leased → running → reviewing → accepted → integrated → landed` | Đặt tên mới cho state đã có là đúng thứ `doctrine-scan` sinh ra để chặn. **Bác tên, giữ ý.** |
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
| Trần | phút Actions — **co giãn, mua được** | **2 lượt/PR, cứng** (ADR-0043 + §12) |
| Huỷ được khi có push mới | **CÓ** — `concurrency.cancel-in-progress` đã bật cho mọi ref ≠ master | **KHÔNG** — lượt đã tiêu là mất |
| Ai chờ | máy | packet bị khoá ở `reviewing`, lease chạy đồng hồ |

Đề xuất **tiêu thêm tài nguyên khan hiếm (lượt review) để tiết kiệm tài nguyên dồi dào và huỷ được (CI)**.
Mỗi lỗi máy móc mà CI lẽ ra bắt được, nếu để reviewer bắt, ăn mất 1 trong 2 lượt canon.

Thêm nữa, lợi ích mục 2 hứa **đã được thu phần lớn**: `concurrency` gom nhiều push liên tiếp trên
cùng PR thành một lượt hoàn tất, và ma trận Windows đã có điều kiện. Mô hình chi phí của đề xuất
(*"CI × mỗi vòng"*) **đếm trùng** thứ kho đã cắt từ r245.

Chỗ đề xuất ĐÚNG mà nên ghi nhận: chi phí CI là **có thật và đã từng gây chết** — 12-08 kho cạn hạn
mức, mọi job chết ở giây thứ 2. Nhưng nguyên nhân đo được là **hệ số Windows ×2**, không phải tần suất
chạy Linux. Cắt đúng chỗ là cắt Windows theo rủi ro (đã làm), không phải hoãn toàn bộ CI.

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

**Sửa đúng, đã có sẵn:** giữ ba giá trị canon `approve | changes_requested | blocked` và bắt reviewer
khai **NÓ ĐÃ ĐO ĐƯỢC GÌ**. Một lượt không đo được gì phải ra `blocked`, không phải `approve`.

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
10. **Minimum viable process — và nó KHÔNG phải quy trình mới.** Ba việc, đều là cưỡng chế thứ đang có:
    1. **Đóng schema biên nhận** — bắt buộc `luot`, `review_rounds_used`, `thoi_luong_giay`, và `verdict`
       thuộc đúng 3 giá trị canon; `packet_loop.py bien-nhan` ĐỎ khi thiếu. Rẻ nhất, và nó **mở khoá mọi
       mục còn lại** vì không có nó thì không mục nào chứng minh được là có tác dụng.
    2. **Cưỡng chế `spec_hash` ở cổng đăng lease** — biến mục 3 thành hiệu lực mà không thêm gate nào.
    3. **Đổi THỨ TỰ, không thêm tầng:** giữ full CI Linux TRONG vòng lặp (đã có, đã `cancel-in-progress`),
       và bắt buộc **một lượt Windows bằng `workflow_dispatch` TRƯỚC lượt review đầu tiên** cho packet đụng
       đường phụ thuộc nền. Lưu ý đã đo: **gắn nhãn `windows` KHÔNG sinh lượt chạy nào** — `ci.yml` khai
       `pull_request:` không kèm `types:`, nên `labeled` không nằm trong cò mặc định.

    Mọi mục còn lại: **hoãn tới khi (1) cho ra số**. Đó chính là kỷ luật kho đòi ở mọi chỗ khác.

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
