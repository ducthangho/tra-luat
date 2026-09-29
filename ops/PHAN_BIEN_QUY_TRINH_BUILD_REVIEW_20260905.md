# Phản biện đề xuất "Cải tiến quy trình Build – Review – CI"

- **Kho:** `ducthangho/tra-luat` · **PR #452** · **Trạng thái:** phản biện thiết kế, CHƯA thi công.
- **Bản 7**, sau **NĂM** lượt cross-review (2 cùng nền Claude, 3 khác nền codex).
- **Lượt 5 chạy SAU KHI PR đã merge** — phiên điều phối merge một phút sau khi lượt review ấy bắt
  đầu, nên hai commit cuối vào `master` không có lượt khác nền nào kết luận. Lượt 5 là bản **vá lỗ
  hổng**, không phải cổng trước-merge. Xem phụ lục J.
- **Cách đọc:** đọc **§1** là đủ để quyết định. Mọi thứ dưới `PHỤ LỤC` là **bằng chứng và lịch sử** —
  giữ lại để kiểm được, không phải để đọc.
- **Vì sao tách:** cross-review lượt 4 (`R4-02`, **P1**) đo được rằng bản trước **không có một kết luận
  hiện hành nhất quán** — ba thứ cùng được gọi "việc số một", và phần khuyến nghị còn mang những con số
  đã bị rút ở phần bằng chứng. Reviewer trả lời thẳng: *"còn giá trị làm hồ sơ bằng chứng, nhưng chưa đạt
  mục tiêu giúp quyết định quy trình."* Bản này tách hai vai ấy ra.

---

# §1. TRANG QUYẾT ĐỊNH

## 1.1 Kết luận về đề xuất 13 mục

| | |
|---|---|
| **Bác, có phép đo** | **mục 2** (hoãn full CI) · **mục 11** (đưa kiểm tra đa nền vào pre-flight) · **mục 9** (nới cho `approve`) |
| **Nên làm TRƯỚC mọi thứ khác** | **mục 5** — *tìm theo bug class, không theo từng finding* |
| **Chưa quyết định được** | 9 mục còn lại. Chúng **đã được VIẾT** trong protocol/ADR/skill, nhưng **trạng thái cưỡng chế phần lớn là `chưa đo`** — và "đã có" một mình **KHÔNG** phải lý do bác |

**Vì sao mục 5 đứng đầu, và đây là kết quả mạnh nhất của cả đợt:** chính tài liệu này là phản chứng thực
nghiệm cho nó. Qua bảy bản, tôi mắc **cùng một lớp lỗi sáu lần** — đọc *sự CÓ MẶT* thành *KHẢ NĂNG*:

> "có trong tài liệu ⇒ có hiệu lực" → "không có mã trong 6 tệp ⇒ không hiệu lực" →
> "không khai `nang_tran` ⇒ không vượt trần" → "`spec_path` có ⇒ đã neo đặc tả" →
> "bốn reviewer bỏ sót" (họ chưa từng thấy câu đó) → **"lớp ngoại lệ riêng ⇒ chốt đích đã chạy"**.

Mỗi lần được chỉ, tôi sửa **đúng dòng được chỉ** và bỏ sót **cả lớp**. Không lần nào tự phát hiện.

**Lần thứ sáu là lần đắt nhất, vì nó nằm BÊN TRONG bản vá dựng ra để chặn lớp ấy.** Bản vá `R4-04` tạo một
lớp ngoại lệ riêng `TinHieuChotCa` để không ai giả được tín hiệu "chốt đã bắt". Nó đóng đúng cái mutant bị
gọi tên. Nhưng `bang()` còn được dùng làm **chốt khởi chạy tiến trình con**, nên một crash vô can trong sản
phẩm vẫn ăn tín dụng giết: reviewer lượt 5 bơm một `raise KeyError` vào `_bash_windows`, con chết trước khi
ca kịp đo thuộc tính nào, mà bộ phân hạng vẫn báo `giet_that`. Năm lần trước còn có thể đổ cho người viết
cẩu thả. Lần này người viết đang **cố ý** vá theo lớp, có tên lớp, có năm ca tự kiểm cho lớp — và vẫn
trượt, vì cả năm ca tự kiểm chạy **trong cùng một tiến trình**.

Kết luận thực hành, và nó chính là mục 5: thứ bắt được lỗi ấy **không** phải một reviewer đọc kỹ hơn, mà
một phép đo **đi qua ranh giới tiến trình** — tức một reviewer có **năng lực ĐO**. Đó cũng là lý do bước 2
ở §1.2 tồn tại.

## 1.2 Việc cần làm — MỘT thứ tự duy nhất

Tiêu chí xếp: **rẻ nhất trong số những việc MỞ KHOÁ được phép đo tiếp theo** đứng trước. Đây là
**phán đoán**, không phải phép đo — chưa ai đo lợi ích của từng bước. Bản trước gọi tới **ba** thứ khác
nhau là thứ phải làm đầu tiên; bảng dưới đây có **đúng một** thứ tự, và tôi khai thẳng rằng thứ tự ấy
chưa được phép đo nào chứng minh.

| # | Việc | Vì sao trước | Trạng thái |
|---|---|---|---|
| 1 | **Không có biên nhận thì không land** — nối `packet_loop.py bien-nhan` vào land gate | Lỗ ĐO ĐƯỢC: packet **#249** chạy **bốn** vòng cross-review, để lại **0** biên nhận, suite vẫn xanh. Mã cổng **đã có**, phản chứng **đã có**. Không có bước này thì mọi metric đều đo trên tập thiếu | chưa làm |
| 2 | **Cổng NĂNG LỰC ĐO cho reviewer** — ở **preflight**, TRƯỚC khi lượt review chạy: quét **cả bốn** đầu vào mà `PROTOCOL §8` liệt kê (đặc tả · handoff · bảng bằng chứng · verdict); bundle nào mang khẳng định **phụ thuộc kho** mà không kèm mirror **đọc được đúng revision cần đo** thì bị từ chối | `PROTOCOL §8` **đã là luật** (mirror + ghim `core.abbrev=7`) và **phần này** vẫn có **0 cổng** — nói chật lại vì từ `ops/bien_nhan_v2.py` thì phần **lược đồ biên nhận v2** của §8 ĐÃ có cổng (`ops/bien_nhan_v2_test.py`, 15 ca · 5 đột biến có răng, chạy trong `ci.yml`); mirror thì chưa. Lượt 3–4 cho thấy reviewer đo được thì tìm ra thứ reviewer chỉ-đọc không tìm ra. **Bản đầu của hàng này chỉ kiểm VERDICT và `R5-03` bác:** con số cần đo thường nằm trong **đặc tả** mà verdict không lặp lại, và nếu hiểu verdict là **đầu ra** của lượt sắp chạy thì kiểm ở đó đã **quá muộn** để cấp năng lực cho chính lượt ấy. Chốt phải là **có mặt ⇒ chưa đủ**: `.git` tồn tại không phải mirror dùng được — đúng lớp lỗi tệp này đếm sáu lần | chưa làm |
| 3 | **Thống nhất TỪ VỰNG mỏ neo đặc tả** (ba tầng: locator / định danh byte / đã xác minh) rồi mới cưỡng chế | Cưỡng chế một tên trong nhiều tên sẽ bắt oan lease đang làm đúng bằng tên khác. Xem §2 hàng 3 | chưa làm |
| 4 | **ĐO Windows trước khi BẮT BUỘC Windows** — chạy một lượt `workflow_dispatch` để biết nó có hoàn tất trong trần 60 không | **0/3** lượt dispatch từng hoàn tất. Bắt buộc một phép kiểm chưa từng XANH là tự tạo deadlock | chưa làm |
| 5 | **Mở rộng phép ĐO RĂNG sang các cổng còn lại** | Lượt 4 đo 6 cổng, tìm ra **2** cổng hỏng thật (`R4-04`, `R4-05`). Cả hai **đã vá** trong PR này. Kho còn nhiều cổng chưa ai đo | 2/N đã làm |

**Việc gần như miễn phí, làm ngay:** thêm `types: [..., labeled]` vào `pull_request:` của `ci.yml`.
Hiện `ci.yml` không khai `types:` nên gắn nhãn **không** bắn nó — trong khi `launcher-windows.yml` thì có.

## 1.3 Giới hạn — cái gì tài liệu này KHÔNG chứng minh

Đọc mục này trước khi trích bất kỳ con số nào ở phụ lục.

- **Tỉ lệ VI PHẠM của mỗi luật: CHƯA AI ĐO.** Đây là biến đúng để xếp ưu tiên, và cả năm bản đều
  chưa đo nó. Ba lần tôi thử thay thế nó bằng một proxy (*luật có được viết / có được mã hoá / có khoá
  nào đó không*) và cả ba lần đều sai.
- **"Điểm mù theo provider": KHÔNG ĐO ĐƯỢC.** Bản 4 khai *"4 bỏ sót so 1 bắt được"*; `R4-03` bác — hai
  vế dùng **đầu vào khác nhau**. Muốn đo phải cho hai provider **cùng bundle, cùng nhiệm vụ, cùng SHA**,
  và giữ cả lượt thất bại.
- **Vật bị phản biện KHÔNG có hiện vật trong kho.** Đề xuất 13 mục chưa được đóng băng thành tệp có băm,
  nên mọi câu *"đề xuất viết: …"* không kiểm được (`R4-02`). Muốn chắc thì đóng băng nó vào `ops/specs/`.
- **Lượt 1–2 là `same_provider`**, chỉ lượt 3–4 là `cross_approved`. Xem phụ lục H.
- **Ràng buộc phân công** (cấm reviewer tự soạn phản chứng) làm **hẹp độ phủ** của cả ba lượt khác nền.
- **"0 âm tính giả" của lượt 5 chỉ đúng TRONG TẬP ĐÃ ĐO** — 18 cặp control–mutant hiện có. Reviewer
  tự khai: năm ca tự kiểm đều nằm **cùng tiến trình**, nên chúng bỏ sót đúng đường `R5-01`. Đừng đọc
  con số ấy thành *"bộ phân hạng đã đúng với mọi crash"*.

## 1.4 Cách kiểm trang này còn nhất quán không

Trang quyết định phải cho **cùng một thứ tự** và **cùng một trạng thái** như phần bằng chứng. Phép kiểm:

Chạy `ops/kiem_trang_quyet_dinh.sh`. Nó cắt §1 ra, **bỏ mọi khối mã** (nếu không thì chính lệnh kiểm
sẽ khớp mẫu của nó — đã xảy ra ở lần viết đầu), rồi tìm các chuỗi **đã bị rút**.

**BA trạng thái, không phải hai:** `0` sạch · `1` còn lời khai đã rút · `2` **KHÔNG ĐO ĐƯỢC**. Bản đầu chỉ
có hai, và `R5-02` đo được rằng nó **báo sạch khi mù**: `grep` trả `1` khi không khớp nhưng `>1` khi không
thực hiện được phép đo, mà cả hai cùng rơi xuống nhánh in "sạch" — nên regex hỏng cho `rc=0 "sạch"`, và
cắt mất mốc kết thúc cũng cho `rc=0`. Cùng họ với *"cổng không nói dối, nó VẮNG MẶT"*, chỉ tệ hơn: cổng
này **có mặt** và **nói sạch**. Phản chứng chạy được: `ops/kiem_trang_quyet_dinh_test.sh` — 7 ca (đòi
`0·2·2·2·2·2·1`) cộng **4 phép đo răng**, trong đó hai đột biến đưa cổng về **đúng hình dạng cũ** và tái
hiện lại chính ba con số reviewer đo được.

**Và khai thẳng giới hạn của chính phép kiểm này: KHÔNG workflow nào chạy nó.** `ci_dang_ky_test.py`
chỉ quét `*_test.py`, nên một `*_test.sh` không nằm trong sổ và không có gì báo động nếu nó thối rữa.
Đây là chốt **chạy tay**. Nói ra rẻ hơn nhiều so với để người đọc tưởng có máy canh — đúng bài học
*"phạm vi TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC"*.

---

# §2. Bằng chứng cho từng quyết định

Mỗi hàng: điều được khai · số đo · lệnh tái hiện. Chi tiết ở phụ lục.

| Khai | Số đo | Lệnh |
|---|---|---|
| Bác **mục 2**: CI không phải tài nguyên "dồi dào" | gate Linux **6,6′** (13-08) → **21m52s–25m14s** (29-08) = chậm **3,4×**; `ci.yml:63` tự khai *"gate 22 phút và đang lớn dần là nợ riêng"* | `sed -n '20,64p' .github/workflows/ci.yml` |
| Bác **mục 11**: Linux không đo được Windows | `os.getpgid` làm suite **0/103** trên `windows-latest`; **5** lượt review Linux không thấy | `CLAUDE.md`, mục "API CHỈ CÓ TRÊN MỘT NỀN" |
| Mỏ neo đặc tả — **ba tầng**, tổng 82 | **44** có định danh byte · **3** chỉ locator (cả ba khai `ban_thao_chua_duyet`) · **3** khoá `spec_path` = `null` · **32** không có gì · **"đã xác minh băm + thẩm quyền" = KHÔNG ĐO ĐƯỢC** | `grep -lE '^ *(spec_hash\|spec_sha256_required\|spec_sha256): *[^ ]' ops/leases/*.yaml \| wc -l` |
| Trần vòng review **không có cổng** | `nang_tran` xuất hiện **0** lần trong `ops/lease_publish.py`; **1/82** lease có khối ấy; §20 ghi `ADR-0043 \| 0 cổng` | `grep -c nang_tran ops/lease_publish.py` |
| Vòng review để lại **0 hiện vật** | packet **#249**: 4 vòng, 0 biên nhận, suite 98/98 xanh | docstring `cmd_bien_nhan` trong `.claude/dev/packet_loop.py` |
| Cổng **có** răng — nhưng phải đo mới biết | Lượt 4 đo 6 cổng → tìm ra **2** hỏng thật. Sau khi vá (kể cả `R5-01`): `cong_cu_test` **23/23 · bỏ qua=0 · 7 ca tự kiểm bộ phân hạng · lỗi đột biến=0**, và phản chứng `R5-01` **qua ranh giới tiến trình** cho `tin_dung_gia` (trước bản vá: `giet_that`); `packet_loop` **278/278 · BỎ QUA=0**; đột biến gỡ cổng sổ comment ⇒ 3 ca **ĐỎ** (261/278) trong khi **trước** bản vá chúng vẫn XANH | `python3 ops/cong_cu_test.py` · `python3 .claude/dev/packet_loop_test.py` |
| Chốt trong kho **không tự chứng nhận được** | `.claude/dev/duyet_danh_tinh.py`: *"mọi chốt dựng trong kho đều là chốt chủ kho tự dựng cho chính mình"*; cổng chạy trên runner GitHub là **cơ chế đầu tiên** không tự chứng nhận | `sed -n '1,12p' .claude/dev/duyet_danh_tinh.py` — **tệp đã RÚT ở #506/#507 (r365)**; lệnh tái hiện chỉ chạy được trên cây trước `0bf0ba7` (vd `git show 27c413c3:.claude/dev/duyet_danh_tinh.py \| sed -n '1,12p'`); trích dẫn giữ nguyên làm sử liệu (r367 đóng P3 `tham-chieu-tai-lieu-song-con-sot`) |

---

# PHỤ LỤC

Từ đây trở xuống là **bằng chứng và lịch sử**. Không cần đọc để quyết định.

**Đổi tên mục (bản 6):** mục từng tên là **§0** nay là **PHỤ LỤC A**. Con trỏ tự dẫn đã đổi theo; các hàng trong **nhật ký J** vẫn giữ nguyên chữ `§0` vì chúng là **ghi chép về trạng thái CŨ** — sửa chúng là sửa lịch sử. `R5-04` bắt đúng lớp lỗi này: bản 6 đổi mục mà để lại con trỏ.
Nguồn có thẩm quyền của mỗi lượt review là tệp verdict + biên nhận trong `ops/reviews/`, không phải
bản tóm ở đây.

## A. Bảng đo đầy đủ

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
| Lease có mỏ neo đặc tả — **BA TẦNG, không phải một** (`R4-01`) | tổng **82**, phân rã cộng đúng: | `ops/leases/*.yaml` |
| · (1) có **ĐỊNH DANH BYTE** (một trong `spec_hash`/`spec_sha256_required`/`spec_sha256` không rỗng) | **44** | |
| · (2) chỉ có **LOCATOR** (`spec_path`, không băm) | **3** — và cả ba khai `spec_status: ban_thao_chua_duyet`, tức **cố ý không neo** | |
| · (3) có KHOÁ `spec_path` nhưng giá trị **`null`** | **3** — ngay cả địa chỉ cũng không có | |
| · (4) không có gì | **32** | |
| · (5) **ĐÃ XÁC MINH** băm + thẩm quyền | **KHÔNG ĐO ĐƯỢC** — chưa ai kiểm băm khớp nội dung và ai duyệt | |

**Một ĐỊA CHỈ nói tìm bản thảo ở đâu; nó KHÔNG định danh byte đã được duyệt.** Nên `44` là *"có định
danh byte"*, **không** phải *"44 lease tuân thủ"* — bậc (5) mới là tuân thủ, và bậc ấy chưa đo được.
| …vì sao 50 là đếm thừa (cross-review lượt 3, `N1`) | **3** lease chỉ có `spec_path` và **tự khai là BẢN THẢO CHƯA DUYỆT**, cố ý không neo; **3** lease có KHOÁ `spec_path` nhưng giá trị **`null`** — được đếm chỉ vì khoá tồn tại. Một **địa chỉ** nói tìm bản thảo ở đâu; nó **không định danh byte đã được duyệt** | |
| Trần vòng review — hiện trạng thật (`N2`) | `review_rounds_limit`: **41 THIẾU** · **23** khai `2` · **18** khai `>2`, trong đó **17/18 KHÔNG có `nang_tran`**. **6** lease tự ghi đã dùng **>2** vòng | `ops/leases/*.yaml` |

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

## B. Đối chiếu 13 mục với protocol đang hiệu lực

| Mục đề xuất | Đã có? | Ở đâu | Nhận xét |
|---|---|---|---|
| 1. Ba tầng kiểm tra | **ĐÃ CÓ, mạnh hơn** | §10.1 — **sáu tầng T0–T5** + classifier/aggregator | Bản đề xuất là bản RÚT GỌN của thứ đang có. Gộp T3/T4/T5 thành "full CI" xoá mất phân biệt integration-freeze / canonical / release artifact. |
| 2. Hoãn full CI khỏi vòng lặp | **MÂU THUẪN** | §10.1 | Xem F1. Ngoài ra §10.1 đã cấm trước: selector chỉ được activate sau **shadow 2–4 tuần** chứng minh không bỏ sót failure. Đề xuất chính là activate selector, mà không kèm shadow evidence. |
| 3. Architecture review gate | **ĐÃ CÓ, chưa đo cưỡng chế** | §3.2 + skill `soan-spec` + 46 ADR | **RÚT cả `17%` LẪN `61%`** — xem **PHỤ LỤC A**: mỏ neo đặc tả có **ba tầng**, `44/82` có định danh byte, và bậc *"đã xác minh băm + thẩm quyền"* là **KHÔNG ĐO ĐƯỢC**. §20 không có ô cổng cho §3.2 ⇒ trạng thái là **chưa đo**. |
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

## C. Sáu phản biện có phản chứng đo được

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

## D. Failure mode đề xuất CHƯA nêu (M1–M7)

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
**31/57** và `cross_provider` ở **40/57**. Toàn bộ mẫu n=9 của **PHỤ LỤC A** là reviewer `claude` (**8/9**). Cấp mirror
làm reviewer đo giỏi hơn nhưng **không** làm nó bớt mù ở chỗ cùng mô hình cùng mù — §8 đã đặt tên cho rủi ro
ấy (*"self-review đội lốt cross-review"*). MVP-1 bản đầu liệt kê trường bắt buộc mà **không có `assurance`**,
tức mở khoá metric nhưng không phân biệt được duyệt chéo với duyệt cùng nền. Lượt review sinh ra tệp này
cũng đúng như vậy: nó là `same_provider`, và nói thẳng ở §8 dưới.

**M7 — Biên nhận là bằng chứng TỰ KHAI, và tệp này dùng nó như bằng chứng ngoại kiểm.**
`packet_loop.py` nói thẳng: *"hiện vật cục bộ chỉ chứng minh có biên nhận + verdict tự khai, không chứng
minh commit tồn tại hoặc có bao nhiêu vòng review đã thật sự chạy… nên **không được gọi số đếm này là số
vòng review**"*. Toàn bộ bảng **PHỤ LỤC A** (trừ ba dòng CI) đứng trên đúng nguồn ấy, và bản đầu của §6 **không** liệt
kê giới hạn này.

---

## E. Trả lời trực tiếp 10 câu hỏi

1. **Giữ:** mục 5 (bug class) — mục giá trị nhất; mục 12 (regression test từ finding), nâng thành cổng
   máy đo được; mục 6 phần *phân loại* (với ba nhánh, xem F5); danh mục kiểm tra của mục 11 (giữ danh mục,
   đổi chỗ đặt); mục 3 phần *tiêu chí kích hoạt* — nó cụ thể hơn §3.2 và nên nhập vào `soan-spec`.
2. **Bureaucracy — ĐÃ LỌC LẠI theo §1 bản 3.** Chỉ giữ lý do bác nào neo được vào một cổng ĐỎ ĐƯỢC: mục 7, 8, 10 trùng với `T0/T1`, state `ready/reviewing`, và ADR-0036. Chúng thêm từ vựng
   thứ hai cho khái niệm đã có tên — đúng thứ `doctrine-scan` sinh ra để chặn (`rc=6`).
3. **Trùng lặp — HẠ XUỐNG "chưa quyết định được".** Mục 1/4/13 neo vào §10.1 và §12, mà §20 không có ô cổng cho hai mục ấy ⇒ trạng thái là `chưa đo`, và theo §1 bản 3 thì "đã có" một mình không đủ để bác. Nguyên văn cũ: mục 1 (⊂ §10.1), 4 (⊂ severity + review class), 13 (⊂ §12 ba bộ đếm). Mục 13 không chỉ
   trùng mà còn **thô hơn**: nó gộp ba bộ đếm §12 thành một.
4. **Failure mode chưa nêu:** M1–M7 ở §4. Nặng nhất là **M4 (răng của cổng)** và **M1 (lượt chết không verdict)**.
5. **Merge policy P1/P2:** thiếu P0, thiếu trạng thái thứ ba, và Strict/Normal thô hơn ba class
   `sensitive/systemic/routine` đang chạy. `P2 = 0` cho Strict mode là bẫy: nó biến mọi nhận xét
   maintainability thành blocker của core runtime, tức tạo đúng cái "improvement nhỏ giữ feature lớn
   trong review vô thời hạn" mà mục 10 nói muốn tránh. **Giữ ba class hiện có; không thêm hai mode.**
6. **Rủi ro hoãn full CI:** xem F1 + F2. Cụ thể với kho này: (a) **RÚT** — xem F1(a): "phút Actions co giãn" không có cơ sở, và trần 2 lượt/PR **nới được** bằng
   `nang_tran`; (b) reviewer đọc mã **chưa từng được đo trên Windows** — và với PR
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
   **(d) TÁCH BA TẦNG mỏ neo đặc tả TRƯỚC** (locator / định danh byte / đã xác minh — xem **PHỤ LỤC A** và MVP-2), rồi mới cưỡng chế — vòng review tốn nhiều nhất là vòng cãi nhau về đặc tả.
10. **Minimum viable process — BẢN ĐẦU CÓ BA VIỆC, CẢ BA ĐỀU HỎNG. Cross-review lượt 1 phá từng cái;
    dưới đây là bản của BẢN 5, xếp lại theo thứ tự rẻ-trước.**

    > **HẾT HIỆU LỰC LÀM KHUYẾN NGHỊ (bản 6).** Thứ tự đang có hiệu lực là bảng 5 bước ở **§1.2**; mục
    > này giữ lại vì nó ghi *vì sao* từng việc được sửa, không phải để chọn việc nào làm trước. `R5-04`
    > bắt bản 6 để lại đúng chỗ này tự xưng là "bản đã sửa" rồi gọi MVP-4 là số một, trong khi §1.2 đã
    > chọn thứ tự khác.

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
      ở **PHỤ LỤC A** **không phải 15 packet**, và mọi mẫu số theo packet sai im lặng.
    · **Ghi `schema_version` + NGÀY HIỆU LỰC.** Biên nhận là bằng chứng đã giao, không sửa hồi tố; siết
      schema mà không khai ngày ⇒ cổng đỏ vĩnh viễn trên hiện vật cũ.

    **MVP-2 · Thống nhất TỪ VỰNG mỏ neo đặc tả TRƯỚC, cưỡng chế SAU.** Bản đầu nói "cưỡng chế `spec_hash`
    (đang 17%)". Bản 3 sửa thành "bốn tên, 61% đã neo" — **cũng sai**, và `R4-01` bắt: nó gộp
    **locator** vào **định danh byte**. Phân rã đúng ở **PHỤ LỤC A**: **44** có định danh byte · **3** chỉ có
    locator và **tự khai là bản thảo chưa duyệt** · **3** có khoá `spec_path` nhưng `null` · **32**
    không có gì · và bậc **"đã xác minh băm + thẩm quyền" là KHÔNG ĐO ĐƯỢC**.
    **Bỏ hẳn tỉ lệ "đang làm đúng"** — cả `40/82` lẫn `48,8%` đều chưa có bằng chứng; *"có giá trị
    băm"* chưa phải *"đã xác minh băm và thẩm quyền"*. Việc đúng: chọn một tên
    canon, khai ánh xạ cho ba tên kia, rồi mới dựng cổng.

    **MVP-3 · ĐO Windows trước, đừng BẮT BUỘC Windows.** Bản đầu bắt buộc một lượt `workflow_dispatch`
    trước lượt review đầu. Bốn phản chứng, ba nằm trong chính **PHỤ LỤC A**: (a) **0/3** lượt dispatch từng hoàn tất —
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

## F. Điều tệp này KHÔNG đo được

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

## G. Ghi chú về chính cách đặt câu hỏi

Chủ kho đề nghị đưa cùng bản này cho Claude và Codex độc lập rồi gộp hai bản phản biện. **Hướng đúng**,
nhưng có một bẫy đã đo được: cấp cho reviewer **một tài liệu văn xuôi** thì thu về **soát chính tả** —
đúng ba lượt đầu của PR #250 (4 → 11 → 2 finding, **0 con số phân rã**).

Muốn bản phản biện của Codex có giá trị hơn bản này, phải cấp cho nó **năng lực đo**: mirror kho + bảng
**PHỤ LỤC A** + chính các lệnh đã sinh ra bảng ấy, kèm lời khai thẳng rằng bảng này **thiên vị** — nó chỉ đếm thứ
tôi nghĩ ra để đếm, và mỗi con số nó thiếu mà Codex tìm được thì tính là finding.

Và **nguồn có thẩm quyền là TỆP NÀY trong kho**, có băm. Bản chiếu lên Issue/PR chỉ là bản chiếu.


---

## H. Mức assurance và xuất xứ của từng lượt review

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

## I. Các kết luận CŨ đã bị lật (giữ để tra, ĐỪNG trích như đang hiệu lực)

### Bản 3 → bản 5, từng bước bị lật

**Ba bản, ba biến, hai bản đầu đo sai biến.**

| bản | đo cái gì | kết quả |
|---|---|---|
| 1 | luật có được **VIẾT** không | sai — nhầm "có trong tài liệu" với "đang có hiệu lực" |
| 2 | luật có được **MÃ HOÁ** không | sai — và sai theo cách trớ trêu hơn (dưới) |
| **3** | luật có bị **VI PHẠM** không | đo được từ 82 lease + 57 biên nhận |

**Bản 1 sai** như đã ghi: nó bác 9 mục bằng lý lẽ *"đã có rồi"* mà chưa hề tra xem chúng có được cưỡng chế
không. Finding ấy đứng nguyên.

**Bản 2 sửa quá tay, và cross-review lượt 2 bắt bằng ba phản chứng độc lập:**

1. **Bằng chứng KHÔNG GIAO với kết luận.** Bản 2 trưng bảng 8 ADR `0 cổng` để đỡ câu *"9 mục ấy phần lớn
   0 cổng"*. Nhưng **không mục nào trong 9 mục neo vào bất kỳ ADR nào trong 8 cái đó** — chúng neo vào
   §10.1, §3.2, §12, `PROTOCOL:198`, `cross-review/SKILL.md`, và **ADR-0036**, mà §20 xếp ADR-0036 là
   `có nhắc: packet_loop.py×29`. Tôi đo phân bố trên tập ADR rồi khai kết luận về tập "9 mục"; giao của
   hai tập là **rỗng**.
2. **Một dòng của bảng ấy SAI TẠI HEAD.** §20 ghi `ADR-0038 | 0 cổng`. Đo: `ops/lease_publish.py:189`
   có cổng thật, fail-closed, **7** ca phản chứng `RC_LOP`, ghim băm trong workflow — và nó land
   **23-08-2026**, đúng **một ngày sau** mốc `22-08-2026` mà §20 tự ghi ở đầu cột. Tôi dùng một phép đo
   **có ghi ngày** mà không kiểm ngày.
3. **Tiền đề bị chính PHỤ LỤC A của tệp này bác** — nhưng **KHÔNG mạnh như bản 3 đã viết**; xem ngay dưới.

**BẢN 3 PHẠM LẠI CÙNG MỘT LỚP LỖI, LẦN THỨ TƯ — cross-review lượt 3 (codex, KHÁC NỀN) bắt.**

Bản 3 viết: *"Luật không cổng vẫn ràng buộc được, ở mức 61–99%"*, dựa trên hai tử số **50/82** và
**81/82**. Cả hai đếm **sự VẮNG MẶT của một khoá thành TUÂN THỦ**:

- **81/82 = 82 − 1** lấy "không khai `nang_tran`" làm "không vượt trần". Không khai có **ít nhất hai**
  nghĩa: *không cần nâng*, hoặc *đã nới mà thiếu khai báo*. Đo trường liên quan trực tiếp:
  **41** lease **không khai** `review_rounds_limit` · **23** khai `2` · **18** khai **>2**, và
  **17/18** trong số ấy **không có** `nang_tran`; **6** lease tự ghi đã dùng **>2** vòng.
- **50/82** gộp `spec_path` vào "mỏ neo", trong khi **3** lease dùng nó cho **bản thảo chưa duyệt** (cố ý
  không neo) và **3** lease có khoá ấy với giá trị **`null`**.

**Và đây là chỗ phải nói cho đúng, kẻo lại sai theo chiều ngược — đúng lỗi bản 2 đã mắc:**
17–18 **KHÔNG** được đọc thành "17–18 vi phạm". Còn ngày hiệu lực của ADR, miễn trừ và thẩm quyền, đơn
vị đếm vòng, và nhiều lease thuộc cùng một việc. Trạng thái đúng của phần lớn quần thể là **CHƯA ĐỦ
BẰNG CHỨNG** — ô thứ ba, không phải một trong hai ô kia.

Nên câu *"luật không cổng vẫn ràng buộc được 61–99%"* **bị rút**. Thứ còn đứng: `0 cổng` **không** đủ
để kết luận "không được cưỡng chế" (bản 2 sai), nhưng cũng **không** có phép đo nào hiện có đỡ được
mệnh đề ngược. Cả hai chiều đều là **chưa đo**.

Và `0 cổng` là **9/30 = 30%** của bảng §20 (15 `có nhắc`, 6 `chưa đo`) — **thiểu số**, không phải "phần lớn".

**Hình dạng của cái sai đáng nhớ hơn cái sai.** Bản 1 suy *"có trong tài liệu ⇒ có hiệu lực"*. Bản 2 suy
*"không có mã trong 6 tệp ⇒ không hiệu lực"*. Đó là **cùng một phép suy một chiều từ sự CÓ MẶT sang KHẢ
NĂNG**, chỉ đảo dấu. Bản 2 phạm lại chính lỗi nó vừa đặt tên, **trong câu dùng để đặt tên nó**.

### Biến đúng, và nó rẻ

Với mỗi luật, đo **tỉ lệ vi phạm trên hiện vật** (lease · biên nhận · PR), không đo `grep` trong 6 tệp.
Ba ô, không phải hai:

| ô | nghĩa | trạng thái đo được hôm nay |
|---|---|---|
| có cổng | cưỡng chế bằng mã | `ADR-0038` — 13/13 lease `schema_version: 2` tuân |
| không cổng **nhưng tuân** | luật sống bằng kỷ luật | **CHƯA CHỨNG MINH ĐƯỢC** — hai tử số bản 3 dùng đều đếm vắng mặt thành tuân (lượt 3, `N2`) |
| không cổng **và có vi phạm đo được** | việc cần làm | chưa ai đo |
| **chưa đủ bằng chứng** | thiếu ngày hiệu lực / thẩm quyền / đơn vị đếm | **ô bản 3 BỎ QUÊN** — và nó chứa phần lớn quần thể (41/82 không khai limit) |

Cộng một ô nữa mà lượt 3 nêu và bản 3 cũng bỏ: **có cổng nhưng CHƯA KIỂM ĐỘ PHỦ/RĂNG**. "Có cổng"
không phải lý do loại một luật khỏi danh sách việc.

Chỉ ô thứ ba là việc. Đó là trục duy nhất khiến chữ *"theo thứ tự rủi ro"* có nghĩa, và **cả ba bản đều
chưa đo nó**.

### Điều CẢ BA bản đều im lặng, và nó quyết định giá trị của mọi MVP

`.claude/dev/duyet_danh_tinh.py` khai thẳng, có ngày, có packet:

> *"phiên chạy bằng credential CỦA CHỦ KHO, nên **mọi chốt dựng trong kho đều là chốt chủ kho tự dựng cho
> chính mình** — `guard --action merge` chặn một NHÃN VAI, không chặn một THẨM QUYỀN. Cổng này chạy trên
> RUNNER CỦA GITHUB bằng `GITHUB_TOKEN`, KHÔNG bằng credential của phiên… Đó là **cơ chế đầu tiên ở đây
> không tự chứng nhận**."*

Nên *"biến luật thành cổng"* **chưa phải việc thứ ba**. Việc thứ ba là làm cho cổng ràng buộc được **chính
người dựng ra nó** — nửa ngoài kho (danh tính chạy-việc khác admin, `master` siết không-bypass), đã có
runbook `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` và **còn treo**. Chừng nào nửa ấy chưa xong, mọi cổng trong
kho là **khuyến nghị**, và bốn MVP dưới đây có giá trị đúng bằng kỷ luật của người chạy chúng.

Trớ trêu, và kiểm được: cổng đã chặn PR chứa chính tệp này suốt phiên — `duyet khac danh tinh` — **là cổng
đầu tiên ấy**. Câu trả lời cho câu hỏi tài liệu đặt ra nằm ngay trên cái PR mang nó.

### Ba mục vẫn nên bác — lý do đã lọc lại

Chỉ giữ mục nào **không** dựa vào công thức *"đã có ⇒ bác"*: mục **2** và **11** (bác bằng phép đo hành vi,
xem F1/F2), mục **9** (bác vì đổi nghĩa một giá trị canon **có mã cưỡng chế** — `CHUYEN_HOP_LE["blocked"]
= ()`). Các mục 1, 4, 13 trước đây bị bác vì *"trùng lặp"* nay hạ xuống **CHƯA QUYẾT ĐỊNH ĐƯỢC**: chúng neo
vào §10.1/§12, mà §20 không có ô cổng nào cho hai mục ấy. Mục 7, 8, 10 giữ nguyên lý do bác vì lý do thật
là **va chạm từ vựng**, và cái đó có cổng đỏ được thật (`RC_DOCTRINE = 6`, `doctrine-scan`).

## J. Nhật ký cross-review — cái gì bị lật qua năm bản

### Lượt 1 (trên `07eb236`)

| # | Bản đầu khai | Phép đo nói | Xử lý |
|---|---|---|---|
| 1 | "9/13 ĐÃ CÓ ⇒ đề xuất thêm ít; vấn đề là TUÂN THỦ" | §20 đo **`0 cổng`** cho 8 ADR | **ĐẢO** kết luận trung tâm (§1) |
| 2 | `spec_hash` 14/82 = 17,1% | 10/82 theo trường; **50/82 = 61%** theo khả năng (4 tên) | sửa §0 — **nhưng `50/82` sau đó bị `R4-01`/`N1` BÁC**: nó gộp locator vào định danh byte. Số đứng: **44** có băm, 3 locator bản thảo, 3 `null`, 32 không có |
| 3 | "trần 2 lượt/PR, **cứng**" | `nang_tran` nới được; **0 lần** trong `lease_publish.py` | sửa F1 |
| 4 | "gắn nhãn windows không sinh lượt chạy nào" | `launcher-windows.yml` có `labeled` + `windows-latest` | sửa MVP-3 |
| 5 | "một lượt không đo được phải ra `blocked`" | `blocked` = spec thiếu → **trạng thái tận cùng** | F3 đổi sang trường `nang_luc_do` |
| 6 | "phút Actions co giãn, dồi dào" | Linux **6,6′ → 22–25′** = chậm 3,4× | rút; F1 yếu đi |
| 7 | PR #250 là "phản chứng đo được" | nguồn cấm dùng như gate đã kiểm | rút, hạ xuống giả thuyết |
| 8 | MVP-1 "đóng schema" | schema **đã có**, chỉ chưa nối; lỗ thật là vòng **0 biên nhận** | viết lại MVP-1 |
| 9 | MVP-3 bắt buộc Windows dispatch | **0/3** lượt từng hoàn tất; ≥112 phút/lượt; không bị cancel | hạ xuống "đo trước" |
| 10 | "số vòng review KHÔNG ĐO ĐƯỢC" | `bien-nhan` lọc `role: reviewer` (**55**/57) rồi khử trùng theo `reviewed_sha` ⇒ **52** vòng phân biệt, KHÔNG phải 57. Và `packet_loop.py` cấm gọi số ấy là "số vòng review" (M7 trích đúng câu đó) | bản 2 sửa SAI; bản 3 sửa lại |
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


### Lượt 2 (trên `ba76a78`) — hai reviewer: một đo RĂNG của bản vá, một tấn công cú đảo

| # | Bản 2 khai | Phép đo nói | Xử lý ở bản 3 |
|---|---|---|---|
| 15 | cú đảo: "9 mục phần lớn `0 cổng`" | bảng 8 ADR **KHÔNG GIAO** với 9 mục | rút bảng, đổi biến (§1) |
| 16 | `ADR-0038 \| 0 cổng` | **SAI tại HEAD** — cổng land 23-08, sau mốc đo 22-08 một ngày | §1 nêu; dùng phép đo có ngày phải kiểm ngày |
| 17 | "`0 cổng` ⇒ không cưỡng chế" | §0 bác: mỏ neo 61% với **0 dòng mã**; trần vòng 81/82 | đổi sang biến **tỉ lệ vi phạm** — **nhưng CẢ HAI tử số ấy sau đó bị `N2`/`R4-01` BÁC** (đếm vắng mặt thành tuân thủ). Xem §1 |
| 18 | "phần lớn" | `0 cổng` = **9/30 = 30%**, thiểu số | sửa §1 |
| 19 | vá `spec_hash` | **5 trường khác đo y hệt cách sai ấy** — `assurance` cũng 4 tên, **17** tệp TỪ CHỐI khai bị đếm thành đã khai | §0 quét theo LỚP |
| 20 | §1 đảo | §2 và §5 **không đổi một ô** — vẫn "17%", "co giãn", "trùng lặp" | truyền vào §2/§5 |
| 21 | MVP-2 "bắt oan 44%" | 61 − 17 trộn nền đo; đúng là **40/82 = 48,8%** | sửa — **rồi `R4-01` BÁC luôn cả 48,8%**: mọi tỉ lệ "đang làm đúng" đều chưa có bằng chứng, nay **bỏ hẳn** |
| 22 | §9 dòng 10 "57/57" | `bien-nhan` lọc `role` (55) rồi khử trùng ⇒ **52** | sửa |
| 23 | §9 dòng 14 "đã đánh dấu" | §0 **chưa hề bị sửa**, vẫn in "cạn ~ngày 11" | sửa tại chỗ |
| 24 | — | **hai lượt review để lại 0 hiện vật** — đúng khuyết tật MVP-1 xếp số một | viết `ops/reviews/phan-bien-quy-trinh-review-{1,2}-*.receipt.yaml` |
| 25 | — | *"mọi chốt dựng trong kho là chốt chủ kho tự dựng cho chính mình"* (`duyet_danh_tinh.py`) | thêm vào §1 — nó quyết định giá trị của mọi MVP |

**HÌNH DẠNG CỦA HAI LƯỢT, và đây mới là thứ đáng giữ.** Lượt 1 đặt tên hai lớp lỗi (*lời khai rộng hơn
phép đo*, *đếm CÓ MẶT thay vì KHẢ NĂNG*). Bản 2 vá **đúng những dòng được chỉ** rồi để nguyên năm dòng cùng
bệnh, và **phạm lại lớp thứ hai theo chiều ngược** ngay trong câu dùng để đặt tên nó. Tức: **được chỉ lỗi
không đủ để hết lỗi; phải quét theo LỚP.** Đó chính là mục 5 của đề xuất gốc (*tìm theo bug class, không
theo từng finding*) — mục mà bản 1 khen là giá trị nhất rồi tự mình không làm, hai lần liên tiếp.

Nên phán quyết cuối cùng về đề xuất gốc đổi: **mục 5 không phải "phần mới đáng giữ", nó là phần đáng làm
TRƯỚC** — và ba bản của tệp này là bằng chứng thực nghiệm cho nó.


### Lượt 3 (trên `76318fa`) — codex, **KHÁC NỀN**, và nó trả lời được câu M6

| # | Bản 3 khai | Phép đo nói | Xử lý |
|---|---|---|---|
| 26 | *"luật không cổng vẫn ràng buộc được 61–99%"* | **KHÔNG CÓ CƠ SỞ** — cả hai tử số đếm **vắng mặt một khoá** thành **tuân thủ** | RÚT (§1) |
| 27 | `nang_tran` 1/82 ⇒ **81/82 giữ trần** | `review_rounds_limit`: **41 THIẾU** · 23 khai `2` · **18 khai >2** với **17/18 không có `nang_tran`**; **6** lease tự ghi đã dùng >2 vòng | RÚT; thêm ô **chưa đủ bằng chứng** |
| 28 | bất kỳ mỏ neo nào = **50/82** | **44/82** có trường băm không rỗng; 3 lease là **bản thảo chưa duyệt** cố ý không neo, 3 lease `spec_path: null` | sửa §0 |
| 29 | bảng ba ô | thiếu ô **chưa đủ bằng chứng** và ô **có cổng nhưng chưa kiểm răng** | thêm cả hai |
| 30 | M4 *"cổng có đỏ được không"* — chưa ai đo | **ĐÃ ĐO**: 6 cổng (`RC_DOCTRINE` · `bien-nhan` · `RC_LOP` · `t26` · `t27` · `t33`) đột biến trên bản sao, **tất cả ĐỎ đúng ca đích**, kiểm bằng **nội dung assertion** chứ không chỉ `rc≠0`; control **4/4, rc=0, bỏ qua=0** | ghi nhận — reviewer tự khai *"không suy thành mọi cổng đều được bảo vệ"* |

**BẢN 4 KHAI MỘT KẾT LUẬN M6 SAI — cross-review lượt 4 lật, và tôi đã đo lại rồi nhận (`R4-03`).**

Bản 4 viết: *"Bốn reviewer cùng nền đọc qua câu `61–99%` mà không dừng lại."* Đo:

| SHA | reviewer nào review nó | câu `61–99%` có mặt? |
|---|---|---|
| `07eb236` | lượt 1 (2 phiên Claude) | **0 lần** |
| `ba76a78` | lượt 2 (2 phiên Claude) | **0 lần** |
| `d3bc218` | — | xuất hiện **lần đầu** |

**Họ không thể "đọc qua" một câu chưa tồn tại.** Và phép suy `50/82` + `81/82` đến từ **chính
verdict lượt 2** (dòng 39 của `phan-bien-quy-trinh-review-2-claude-verdict.md`).

Nên chuỗi sự kiện đúng — và chỉ chừng này là kiểm được:

> lượt 2 (cùng nền) **sinh ra** phép suy sai → tác giả **nhận vào** bản 3 → lượt 3 (khác nền)
> **bác bằng phản chứng**.

Đó **không phải** "4 bỏ sót so 1 bắt được". Bảng so sánh của bản 4 dùng **hai đầu vào khác nhau**,
nên nó không đo được điều nó tuyên bố. Câu *"cùng nền có điểm mù có hệ thống"* và
*"không còn là suy đoán"* đều **bị rút**.

**Đây là lần thứ NĂM cùng một lớp lỗi** — lời khai rộng hơn phép đo — và lần này nó nằm ở đúng
câu tôi viết ra để tổng kết về chính điểm mù của mình. Cái đáng ghi không phải con số nào, mà là:
**một kết luận về việc mình hay sai ở đâu cũng sai theo đúng kiểu ấy.**

**Cái gì còn đứng:** lượt 3 và 4 (khác nền) đã tìm ra `N1`, `N2`, `R4-01`…`R4-05` — những finding
**có thật, đo được, đã được phiên điều phối kiểm lại**. Điều đó đủ để nói cross-review khác nền
**có giá trị đo được**, nhưng **không** đủ để định lượng "điểm mù theo provider". Muốn đo điều ấy
phải cho hai provider **cùng bundle, cùng nhiệm vụ, cùng SHA**, và giữ cả lượt thất bại — chưa ai làm.


### Lượt 4 (trên `2fb43fc`) — codex lần hai; và nó lật kết luận M6 của bản 4

| # | Bản 4 khai | Phép đo nói | Xử lý |
|---|---|---|---|
| 31 | *"bốn reviewer cùng nền đọc qua câu 61–99%"* | câu ấy **0 lần** ở `07eb236` và `ba76a78` — hai SHA họ review; xuất hiện lần đầu ở `d3bc218`. Phép suy sai đến từ **chính verdict lượt 2** | **RÚT** kết luận M6 (`R4-03`) |
| 32 | tài liệu đã dùng được để quyết định | **KHÔNG** — chỉ dẫn hành động **mâu thuẫn trực tiếp**: dòng 128 vẫn coi chỉ ô "vi phạm đo được" là việc, ngược dòng 125–126; **BA** thứ cùng được gọi "số một" | `R4-02` **P1** — **ĐÃ xử lý ở bản 6** (tái cấu trúc §1/§2/PHỤ LỤC). `R5-02`/`R5-04` sau đó bắt phần **còn sót** của chính lần tái cấu trúc ấy |
| 33 | MVP-2 đã vá theo `N1` | phần quyết định **vẫn** khai 61% và 40/82 "đang làm đúng" | `R4-01` — **ĐÃ vá ở bản 5–6**; lượt 5 đọc lại phân rã `44/3/3/32` ở **cả bốn** snapshot và xác nhận |
| 34 | (chưa đo) | `cong_cu` cấp **TÍN DỤNG GIẾT GIẢ**: mutant chết vì lỗi **ngoài** assertion đích vẫn được đếm là bị giết | `R4-04` |
| 35 | (chưa đo) | ba ca comment-id đang đo **chốt head-sha** thay vì sổ comment | `R4-05` |

**`R4-02` là finding P1. Bản 6 ĐÃ xử lý nó sau khi chủ kho chốt ("tái cấu trúc luôn").** Câu dưới đây
giữ nguyên vì nó ghi lý do tôi dừng lại hỏi — nhưng nó **không còn mô tả trạng thái hiện tại**.
Reviewer trả lời thẳng câu H3 mà phiên điều phối đặt ra:

> *"Tệp còn giá trị làm hồ sơ bằng chứng, nhưng **chưa đạt mục tiêu giúp quyết định quy trình**."*

Và nó tự khai đúng phạm vi: *"Chưa đo thời gian đọc của chủ kho hoặc thử nghiệm người dùng 5 phút.
Nhận định biên tập của tôi…"* — tức nó **không** giả vờ đây là phép đo. Đề nghị của nó: một **trang
đầu chỉ chứa quyết định hiện hành + bằng chứng + giới hạn + thứ tự bước tiếp**, đẩy §9 và mọi đoạn
*"bản đầu viết / rút lại"* sang phụ lục — git đã giữ bản cũ, không cần lặp câu sai trong phần khuyến nghị.

Việc ấy đổi tài liệu này từ **nhật ký** thành **bản quyết định**, và đó là lựa chọn về mục đích, nên
để chủ kho chốt.

### Lượt 5 (codex, khác nền) — chạy SAU KHI MERGE, và đó là một lỗi quy trình

Phiên điều phối merge PR #452 **một phút** sau khi một lượt review khác nền bắt đầu, nên hai commit cuối
(`a0978ee` vá `R4-04`/`R4-01`/`R4-05`, `bbf05ea` tái cấu trúc) vào `master` **không** có lượt khác nền nào
kết luận. Lượt 5 chạy trên `master` `4951f55`, soi đúng `git diff 2fb43fc bbf05ea`. Đó là **vá lỗ hổng**,
không phải cổng trước-merge — `CLAUDE.md` đã ghi sẵn bài học *"Gate xanh KHÔNG phải đã được review"*, và
đây là lần trả giá.

| # | Bản 6 khai | Phép đo nói | Xử lý |
|---|---|---|---|
| 36 | `R4-04` đã vá | **VÁ HỜ Ở CẤP LỚP.** `TinHieuChotCa` chỉ chứng minh lỗi đi qua `bang()` của **ca đang chạy**, KHÔNG chứng minh **assertion nghiệp vụ đích** đã chạy. Bơm `raise KeyError` vào đầu `_bash_windows`: con chết rc=1, chưa tới phép kiểm chọn Git Bash, mà bộ phân hạng vẫn trả `giet_that`. Toàn bán kính: **chỉ `t22` chết, 0 ca `tin_dung_gia`** ⇒ cả kiểm tên ca lẫn bán kính 1/23 đều mù | `R5-01` — **ĐÃ vá**: lớp `LoiDungCa` + `dung()` cho chốt giàn giáo; ranh giới khai **tại chỗ gọi**, không đoán theo mã thoát |
| 37 | chốt shell canh trang quyết định | **ĐỒNG NHẤT "đo hỏng" VỚI "không tìm thấy".** `grep` trả 1 khi không khớp và **>1 khi không đo được**, cả hai rơi xuống nhánh in SẠCH; `set -euo pipefail` không chữa được lệnh trong điều kiện `if`. Đo: regex hỏng ⇒ **rc=0 "sạch"**; mất mốc kết thúc ⇒ **rc=0**; đổi tên mốc ⇒ **rc=1 bắt oan** | `R5-02` — **ĐÃ vá**: ba trạng thái `0/1/2`, đòi đúng một cặp mốc theo thứ tự; `ops/kiem_trang_quyet_dinh_test.sh` 7 ca + 4 phép đo răng |
| 38 | bước 2 của §1.2 | kiểm trên **verdict**, trong khi `PROTOCOL §8` đòi phân loại **khi đóng bundle** (đặc tả · handoff · bảng bằng chứng · verdict). Con số cần đo thường nằm trong đặc tả; và nếu verdict là **đầu ra** của lượt sắp chạy thì kiểm ở đó đã **quá muộn** | `R5-03` — **ĐÃ sửa** hợp đồng bước 2 |
| 39 | tái cấu trúc xong | còn con trỏ tự dẫn **"xem §0"** sau khi §0 biến mất; phụ lục E tự xưng *"bản đã sửa"* rồi gọi MVP-4 là số một trong khi §1.2 chọn thứ tự khác; cuối J còn *"`R4-02` CHƯA xử lý"* | `R5-04` — **ĐÃ sửa** con trỏ + đóng dấu hết hiệu lực |

**Xác nhận ĐÃ VÁ THẬT** (lượt 5 tự đo lại, không nhận lời khai): `R4-01` (phân rã `44/3/3/32` đọc lại được
ở **cả bốn** snapshot `c03a409`/`2fb43fc`/`bbf05ea`/HEAD) · `R4-03` (câu *61–99%* **vắng** ở `07eb236` và
`ba76a78`, **có** ở `d3bc218`) · `R4-05` (gỡ lời gọi sổ comment ⇒ cả ba ca đỏ; gỡ riêng từng chốt ⇒ đúng
một ca đỏ). **Âm tính giả:** 18 cặp control–mutant ⇒ 18/18 chết đúng thuộc tính đang đo, **0 âm tính giả
trong tập ấy** — và reviewer tự khai giới hạn: năm ca tự kiểm đều nằm **cùng tiến trình**, nên chúng bỏ
sót đúng đường `R5-01`.

**Cái đáng nhớ của lượt này** không phải bốn finding, mà là: `R5-01` nằm **bên trong chính bản vá dựng ra
để chặn lớp lỗi ấy**. `R4-04` sửa đúng cái mutant bị gọi tên (`t13`) và bỏ sót **hình dạng** của nó
(bất kỳ ca nào dùng `bang()` làm chốt khởi chạy). Đó là lần thứ **sáu** trong cùng đợt của cùng một lớp —
và là bằng chứng mạnh nhất mà đợt này sinh ra cho **mục 5 của đề xuất gốc** (tìm theo *lớp* lỗi, không
theo lỗi): năm lần trước còn có thể đổ cho người viết cẩu thả; lần này người viết đang **cố ý** vá theo
lớp, có tên lớp, có ca tự kiểm cho lớp — vẫn trượt. Cách duy nhất bắt được nó là một phép đo **đi qua
ranh giới tiến trình**, tức một reviewer có **năng lực ĐO**, không phải một reviewer đọc kỹ hơn.
