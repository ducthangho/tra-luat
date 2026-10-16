# ADR-0052 — Trần trục LỜI GỌI Codex nâng lên TÁM, và nó chỉ có một chỗ ở

- **Trạng thái:** Accepted (2026-10-16, chỉ thị chủ kho `ducthangho`; thi hành bằng packet
  `TRAN-CODEX-VA-SENSITIVE` revision 1, Issue #782 — không phải một phiên tự nâng trần)

Mỗi PR packet được dùng tối đa **tám lời gọi Codex review** — trục LỜI GỌI, bộ đếm
`codex_review_calls_used`. ADR này thay **đúng một con số**: con số trục LỜI GỌI đang được chép trong
`ADR-0036`, `ADR-0037`, `ADR-0038` và `docs/PROTOCOL_DA_PHIEN.md` (năm chỗ trong protocol, đo
16-10-2026: bốn câu chép số hai, một câu về điều kiện cấp *"lượt hai"* của class `systemic`).

Hai trục kia **KHÔNG đổi**: trục VÒNG giữ trần của `ADR-0048`, trục ATTEMPT giữ trần của nó. Cách đếm
LỜI GỌI cũng **KHÔNG đổi**: một lời gọi tính khi launcher có bằng chứng model đã bắt đầu sinh
output/token, kể cả timeout hoặc output sai schema; lỗi preflight, permission denial hay rate-limit
trước khi có output thì không tính. Đổi prompt, phiên hay tên attempt không reset bộ đếm. Nâng trần mà
đồng thời nới cách đếm là nâng hai thứ cùng lúc rồi không biết cái nào có tác dụng.

## Lượt thứ hai trở đi phải có lý do

Trước ADR này protocol mô tả hai lượt là *"một review đầu và một rereview sau khi Executor gom bản
vá"*. Với trần tám, câu ấy không còn mô tả được trần, và nếu chỉ đổi con số thì tám lượt dễ thành
mức phải tiêu.

Luật thay thế: lượt đầu cấp theo Review Class như cũ. **Mọi lượt từ thứ hai tới thứ tám** chỉ được
cấp khi còn P0/P1, còn finding cắt ngang, hoặc cần xác minh lại một bản vá — tức mở rộng đúng điều
kiện mà `ADR-0038` đặt cho *"lượt hai"* của class `systemic` sang mọi lượt sau lượt đầu, ở mọi class.
Hết lượt thứ tám mà chưa approve thì vào Review Rescue Checkpoint (`ADR-0037`), không gọi thêm bằng
prompt hay phiên khác.

## Mức DÀNH SẴN của `ADR-0041` KHÔNG đổi

`ADR-0041` buộc dành sẵn ngân sách **tối đa hai Codex review cho mỗi PR `sensitive`** trước khi giao
Codex làm Executor. Con số ấy **giữ nguyên là hai**. Tám là TRẦN được dùng, không phải mức phải
dành sẵn: dành sẵn tám lượt cho mỗi PR `sensitive` sẽ gần như xoá ngân sách Codex Executor, tức đổi
luôn tỷ lệ 70/30 của `ADR-0041` mà chỉ thị không đòi. Lượt thứ ba trở đi của một PR dùng ngân sách
Codex còn lại tại thời điểm gọi; hết ngân sách thì vào checkpoint như hết trần.

## Trần LỜI GỌI chạm TRƯỚC trần VÒNG — đừng đọc thành "mười vòng Codex"

Với reviewer Codex, trần tám lời gọi luôn chạm trước trần mười vòng của `ADR-0048`: mọi lời gọi đều
tính vào trục LỜI GỌI, còn trục VÒNG chỉ tính verdict có biên nhận hợp lệ, nên số vòng Codex của một
PR không vượt được số lời gọi Codex của nó. Trần mười vòng chỉ còn chạm được khi PR có thêm reviewer
khác nền (phiên Claude độc lập, human). Đây là hệ quả của luật *"trần chạm trước thắng"* của
`ADR-0043`, không phải mâu thuẫn — ghi ra để không ai đọc bảng §20 thành *"mười vòng Codex"*.

## Vượt trần MỚI vẫn phải khai `nang_tran` — và KHÔNG cổng nào cưỡng chế

Vượt trần tám đòi khối `nang_tran` khai `ai_nang` (chủ kho, theo thẩm quyền §2 của protocol),
`can_cu`, `tran_cu` và `tran_moi`, như `ADR-0043`.

**Không cổng nào cưỡng chế nghĩa vụ ấy, và không cổng nào đếm lời gọi.** Đo 17:01Z 16-10-2026, khớp
**nguyên từ** (`rg -w`), đếm riêng từng tên:

| tên | `ops/lease_publish.py` — số dòng | toàn kho — số tệp `*.py` |
|---|---:|---:|
| `codex_review_calls_used` | 0 | 0 |
| `nang_tran` | 0 | 2 |
| `ai_nang` | 0 | 0 |
| `tran_cu` | 0 | 0 |
| `tran_moi` | 0 | 0 |

Hai tệp chứa `nang_tran` là hiện vật review đã đóng (`ops/reviews/bookkeeping-650-pr667/`), không
phải cổng. Khớp chuỗi con thay vì nguyên từ thì `tran_cu` ra **1** tệp — `t156_…_tran_cung` trong
`ops/lease_publish_test.py` — cũng không phải cơ chế này; nên đếm phải theo nguyên từ.

Người cấp lease và reviewer phải kiểm khối `nang_tran` và số lời gọi **bằng tay**. Đừng chép câu
*"không có khối ấy thì cổng đăng lease từ chối"* của `ADR-0043`: `ADR-0048` đã đo nó sai, và phép đo
trên cho thấy nó vẫn sai.

## Hiệu lực — đặc tả trích OID LAND của ADR; không hồi tố

Ba bản trước của mục này hỏng cùng một lớp (cross-review lượt 1–3, P2
`moc-hieu-luc-thieu-thu-tu-trong-ngay`): mốc theo NGÀY không phân xử được đặc tả đóng băng cùng ngày;
mốc theo THỜI ĐIỂM COMMIT dò bằng `git log --all` đổi kết quả khi ref bị dọn; điều kiện *"`base_sha`
của lease chứa tệp ADR"* cấp trần mới từ một nhánh **chưa land**, và đổi `base_sha` là đổi trần của
cùng một đặc tả. Gốc chung: suy *"ADR đã land chưa"* từ một thứ không chứng minh việc land. Luật dưới
đây đòi chính bằng chứng land, và đặt lựa chọn vào nội dung đã băm của đặc tả.

Trần **tám** áp cho một packet **khi và chỉ khi** blob đặc tả mà `spec_hash` của lease trỏ tới có
**đúng một** dòng khớp `^tran_loi_goi_codex: ADR-0052@([0-9a-f]{40})$` (so trên byte gốc), và OID
`<L>` bắt được thoả cả ba phép đo:

1. `git cat-file -e <L>:docs/adr/0052-tran-loi-goi-codex-len-tam.md` ⇒ `rc=0` — `<L>` chứa ADR;
2. `git cat-file -e <L>^1:docs/adr/0052-tran-loi-goi-codex-len-tam.md` ⇒ `rc≠0` — cha thứ nhất chưa
   có, tức `<L>` là commit ĐƯA ADR vào;
3. `<L>` nằm trên chuỗi first-parent của nhánh mặc định, đo trên clone **không shallow** có ref nhánh
   mặc định vừa fetch: `git rev-list --first-parent origin/master | grep -qx <L>`.

Ba phép đo cùng nhau nói: `<L>` là commit land ADR trên nhánh mặc định. PR của kho land bằng merge
commit hoặc squash, nên OID ấy chỉ sinh ra **lúc** land — một đặc tả đóng băng trước đó không thể trích
nó. Lựa chọn nằm trong `spec_hash`, nên `base_sha` của lease không tham gia, đổi lease không đổi trần;
rebase hay xoá ref không đổi nội dung đã băm. Muốn đổi lựa chọn phải sửa đặc tả, tức revision mới theo
§3.2.

Thiếu dòng, hai dòng trở lên, một phép đo `rc` sai, clone shallow, hoặc **không đo được** ⇒ trần cũ
(**hai**), fail-closed. Phép đo 3 phụ thuộc ref nhánh mặc định — chấp nhận được vì nhánh ấy không bị
viết lại lịch sử; nếu nó từng bị viết lại thì `<L>` rơi khỏi chuỗi và kết quả là trần cũ, tức chặt hơn.
Giới hạn đã biết: land bằng **fast-forward** sẽ đưa chính commit của tác giả lên chuỗi first-parent, nên
OID ấy có thể được biết trước; PR của kho không land kiểu ấy, nhưng nếu xảy ra thì người cấp lease phải
kiểm tay.

Ngày ở dòng *Trạng thái* là ngày chủ kho duyệt, không tham gia phép đo. Ca của chính packet đọc ra đúng
một câu trả lời: đặc tả `spec_hash 56a0bf28…` không có dòng khai ⇒ trần mặc định **hai**. Lời gọi thực tế
của PR ấy được nâng riêng bằng khối `nang_tran` của chủ kho (Issue #782), không phải bằng luật này.

Vì vậy ADR này **không** sửa `ADR-0036`, `ADR-0037`, `ADR-0038`, `ADR-0041` hay đặc tả đóng băng
nào: sửa chúng là viết lại một lời khai vốn đúng tại thời điểm của nó.

## Con số chỉ có MỘT chỗ ở

Chỗ ở duy nhất của con số trục LỜI GỌI là **tệp này**. `docs/PROTOCOL_DA_PHIEN.md` trỏ tới đây, không
chép. Dòng §20 của ADR này cũng không mang con số.

## Nợ

**Không bộ đếm, không cổng.** `codex_review_calls_used` không tồn tại trong mã (bảng trên), nên trần
tám — như trần hai trước nó — chỉ được canh bằng kỷ luật đọc. Cùng họ nợ `SO-CANON-CHUA-TON-TAI`.

**Không có số đo nào biện hộ con số tám.** `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:143` đếm
**2/57** biên nhận có bộ đếm này, nhưng đó là số tệp **nhắc tên** trường: đo lại tại `c03a409`, cả 57
tệp `ops/reviews/*.receipt.yaml` parse được và **0/57** có khoá `codex_review_calls_used` ở bất kỳ cấp
nào — hai lần nhắc nằm trong chuỗi ghi chú `lease_ghi_chu` (cross-review lượt 1, P2
`nham-ten-truong-voi-gia-tri-bo-dem`). Kho không có giá trị nào của bộ đếm, nên không biết một PR thường
dùng bao nhiêu lời gọi. Tám là **quyết định của chủ kho**; đừng khai mạnh hơn thế.

**Không có con trỏ tiến** từ `ADR-0036`/`0037`/`0038` tới đây; đường duy nhất là bảng §20.
