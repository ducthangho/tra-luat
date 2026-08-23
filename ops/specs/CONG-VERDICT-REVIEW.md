# ĐẶC TẢ ĐÓNG BĂNG — `CONG-VERDICT-REVIEW`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `CONG-VERDICT-REVIEW`
`packet_issue`: `CHUA_CO` — người giữ kho chưa mở. **Không bịa số.**

`review_class`: **`sensitive`** — công cụ này trả lời câu *"PR đã được review chưa"*, tức nó đứng
ngay trước quyết định **merge**. Sai một chiều thì land bản chưa soi.

## `nguon_cap_viec`

Phiên thi công `CI-BANG-PHU-THUOC` (#245), 22-08-2026. Người giữ kho chỉ đạo trực tiếp:
*"Soạn thành packet: Issue + spec cho các mục trên."*

**Nguồn thật của packet này không phải một finding của reviewer — mà là việc chính phiên ấy LẶP
LẠI một bài học đã được ghi nguyên văn trong `CLAUDE.md`.** Đó là dữ kiện quan trọng nhất ở đây,
và §B3 nói vì sao.

## Bằng chứng — ĐO, không suy

### B1. Verdict SẠCH và verdict CÓ FINDING đi bằng HAI đường khác nhau

Connector `chatgpt-codex-connector` **chỉ tạo đối tượng review khi CÓ góp ý**. Kết luận sạch nó
gửi bằng một **issue comment thường**. Đo trên chính hai PR của phiên này:

| PR | head | đường | hình dạng |
|---|---|---|---|
| #251 | `a418e68` | **issue comment** `5381935111` | *"Didn't find any major issues"* + `Reviewed commit: a418e68e6a` |
| #251 | `554f7a2` | **review object** `5000689332`, state `COMMENTED` | *"Here are some automated review suggestions"* + 1 thread P2 |
| #251 | `530bad6` | **review object** `5000752127`, state `COMMENTED` | như trên + 1 thread P2 |
| #253 | `08ba88e` | **review object** `5000894577`, state `COMMENTED` | 3 thread (2×P1, 1×P2) |

Nên hỏi `get_reviews` mà thấy **rỗng** có thể nghĩa là *chưa review*, cũng có thể nghĩa là
**đã review và SẠCH**. Hai thứ ấy nhìn giống hệt nhau ở API đó — đúng bài học
*"vắng mặt vì sạch" và "vắng mặt vì chưa chạy" nhìn giống hệt nhau nếu hỏi sai chỗ*.

### B2. Không có state `APPROVED` để mà chờ

Cả bốn dòng trên: **không lượt nào** ở state `APPROVED`. Verdict sạch của connector là
`COMMENTED`-vắng-mặt cộng một issue comment. Phiên nào chờ `APPROVED` sẽ chờ mãi, còn phiên nào
đọc `COMMENTED` thành "có góp ý" sẽ báo sai cho lượt sạch.

### B3. Bài học ĐÃ ĐƯỢC VIẾT không ngăn được lần lặp — đây là lý do packet tồn tại

`CLAUDE.md` có sẵn, nguyên văn, mục **(b)**:

> *"RỖNG ở API mình hỏi KHÔNG phải «chưa chạy». … Muốn biết đã review chưa thì tìm dòng
> `Reviewed commit:` cho ĐÚNG commit đang xét."*

Phiên `CI-BANG-PHU-THUOC` **đã đọc mục đó** — nó nằm trong tệp phiên bắt buộc đọc lúc mở — rồi
vẫn dựng bộ dò review **chỉ canh review object và thread inline**, và **bỏ sót verdict sạch của
#251 khoảng 20 phút**. Chỉ lộ ra vì người giữ kho hỏi *"Kiểm tra kết quả review đi"*.

Cùng phiên, cùng ngày, suýt lặp mục **(a)** (*"Gate xanh KHÔNG phải đã được review"*): thấy cổng
của #253 xanh và định merge, trong khi ba finding đang nằm đó chưa đọc.

**Kết luận: một bài học sống bằng VĂN XUÔI thì người đọc gật đầu rồi vẫn vi phạm.** Kho này đã
tự viết ra luật ấy ở chỗ khác — *"nghĩ ra được phép thử mà không chạy nó thì phép thử ấy không
tồn tại"* — và mục (b) là đúng ca đó ở tầng doctrine: **luật không chạy thì luật không tồn tại**.
Thứ chuyển được nó từ chữ sang cổng là một lệnh trả ba trạng thái.

### B4. Đường REST thẳng bị chặn — công cụ phải đi đúng đường còn sống

Đo lại 22-08-2026 trong container remote: `api.github.com/repos/<kho>/…` trả **403 không header
GitHub nào** (proxy tự sinh), trong khi `api.githubcopilot.com/mcp/` gọi được. Công cụ này vì thế
**không được** dựng trên REST thẳng.

## `write_set`

Đúng hai tệp:

- `ops/review_verdict.py`
- `ops/review_verdict_test.py`

## `ngoai_pham_vi`

- `CLAUDE.md` — mục (a)/(b) **đã có chữ**; packet này thêm **cổng**, không viết lại doctrine.
- `.github/workflows/ci.yml` — công cụ này chạy **trước merge**, không phải một bước CI.
- Mọi thao tác **merge/approve** — công cụ chỉ ĐỌC và TRẢ TRẠNG THÁI. Nó không được merge gì.

## `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| **M1** | `review_verdict.py <pr> <sha>` trả **BA** trạng thái: `sach` · `co_finding` · **`chua_review`** | `ops/review_verdict.py` |
| **M2** | Đọc **cả ba** nguồn: review object · review thread (inline) · **issue comment mang `Reviewed commit:`**. Thiếu nguồn thứ ba là lỗ đã trả giá (B3) | `ops/review_verdict.py` |
| **M2b** | **XÁC THỰC TÁC GIẢ trước khi coi một comment là verdict.** Chỉ nhận comment từ **danh sách CHO PHÉP** danh tính reviewer (`chatgpt-codex-connector[bot]`…), đối chiếu **`user.login` + `author_association`**, không đối chiếu thân comment. Tác giả ngoài danh sách ⇒ comment **không phải verdict**, dù chép đúng từng chữ | `ops/review_verdict.py` |
| **M3** | **Neo EXACT SHA.** Verdict của commit khác **không tính**. `Reviewed commit:` viết dạng rút gọn (`a418e68e6a`) nên phép so là **tiền tố**, không phải bằng chuỗi | `ops/review_verdict.py` |
| **M3b** | **Tiền tố phải ĐỦ DÀI và PHÂN GIẢI DUY NHẤT.** Đòi độ dài tối thiểu, và `git rev-parse --verify <viết-tắt>^{commit}` phải phân giải về **đúng một** commit. Không phân giải được, hoặc mơ hồ ⇒ `chua_review` | `ops/review_verdict.py` |
| **M4** | **FAIL-CLOSE**: gọi API hỏng, phân tích hỏng, hoặc có verdict mà **không** neo được SHA ⇒ `chua_review` + mã thoát khác 0. Không bao giờ im lặng trả `sach` | `ops/review_verdict.py` |
| **M5** | Thread **chưa `is_resolved`** ⇒ `co_finding`, kể cả khi lượt review MỚI NHẤT là sạch. Sạch ở head mới không xoá thread mở ở head cũ | `ops/review_verdict.py` |
| **M6** | Đồ giả **giữ TRẠNG THÁI**, không diễn kịch bản; mỗi thao tác đọc có phép đo đọc **nhật ký lời gọi**, không chỉ đọc mã thoát | `ops/review_verdict_test.py` |
| **M7** | Phản chứng cho từng luật + đột biến giết đúng ca của nó | `ops/review_verdict_test.py` |

## `nghiem_thu`

| # | nghiệm thu | phép đo làm ĐỎ |
|---|---|---|
| **N1** | Fixture #251/`a418e68` (issue comment sạch) ⇒ `sach` | đột biến **bỏ nguồn issue comment** ⇒ ca trả `chua_review` ⇒ ĐỎ. Đây là ca tái hiện đúng lỗ B3 |
| **N2** | Fixture #253/`08ba88e` (3 thread mở) ⇒ `co_finding` | đột biến bỏ đọc thread ⇒ ĐỎ |
| **N3** | PR chưa ai soi ⇒ `chua_review` | đột biến để mặc định `sach` khi không tìm thấy gì ⇒ ĐỎ |
| **N4** | Verdict sạch nhưng của **SHA KHÁC** ⇒ `chua_review` | đột biến bỏ phép neo SHA ⇒ ĐỎ. Không có ca này thì công cụ tái tạo bệnh *"reviewed cái gì đó, không phải cái này"* |
| **N5** | API ném lỗi ⇒ `chua_review` + rc≠0 | đột biến nuốt lỗi thành `sach` ⇒ ĐỎ |
| **N6** | `Reviewed commit: a418e68e6a` khớp SHA đầy đủ `a418e68e6a6be0…` — chiều **BẮT OAN** | ca chiều-tha; giết bằng đột biến **SIẾT THÊM** (đòi bằng chuỗi tuyệt đối) ⇒ chỉ N6 ĐỎ, N4 vẫn xanh |
| **N6b** | **Tác giả KHÔNG thuộc danh sách cho phép chép đúng từng chữ một verdict sạch ⇒ `chua_review`** | đột biến bỏ phép kiểm tác giả ⇒ ca ĐỎ. Kèm chiều BẮT OAN: comment THẬT của connector vẫn phải ra `sach`, nên đột biến **siết** danh sách xuống rỗng cũng phải làm N1 ĐỎ |
| **N6c** | `Reviewed commit: a` (một ký tự) ⇒ `chua_review`, **không** khớp mọi head bắt đầu bằng `a` | đột biến bỏ ngưỡng độ dài ⇒ ĐỎ. Đo được: `'a418e68e…'.startswith('a')` là `True`, nên phép so tiền tố TRẦN nhận nó |
| **N6d** | Viết tắt phân giải ra **nhiều hơn một** commit ⇒ `chua_review` | đột biến lấy commit đầu tiên thay vì từ chối ⇒ ĐỎ |
| **N7** | Thread mở + review mới nhất sạch ⇒ vẫn `co_finding` | đột biến chỉ đọc lượt mới nhất ⇒ ĐỎ |
| **N8** | delta so master = 0 cho `packet_loop_test.py` và `lease_publish_test.py` | nền master đo **trong worktree của chính kho** |

## `hinh_dang_ke_thua`

Nợ để lại **có chủ đích**: công cụ này **không tự chặn merge**. Nối nó thành chốt bắt buộc trước
`merge_pull_request` là quyền hạn khác hẳn và cần quyết định riêng của người giữ kho — một cổng
tự động chặn merge sai một chiều thì khoá cứng cả kho.

## `chua_do_duoc`

- **Không đo được reviewer có ĐỌC KỸ hay không.** Công cụ đếm *đã có verdict cho đúng SHA chưa*,
  không đo chất lượng. `sach` nghĩa là *reviewer nói sạch*, không nghĩa là *mã đúng*.
- **Danh tính reviewer có thể XOAY.** M2b dựng trên tên tài khoản/app, mà tên ấy đổi được: nhà cung cấp đổi slug bot, kho đổi connector. Siết quá thì **từ chối oan chính reviewer thật** — và ca ấy nhìn giống hệt "chưa review". Vì thế danh sách cho phép phải nằm **một chỗ, đặt tên rõ**, và khi không khớp thì thông điệp phải nói **"tác giả X không thuộc danh sách"**, đừng nói chung chung `chua_review`.
- **Hình dạng verdict của connector là thứ NGOÀI TẦM KIỂM SOÁT.** Bốn dòng B1 đo ngày 22-08-2026;
  connector đổi định dạng thì `Reviewed commit:` có thể biến mất. Vì thế M4 fail-close: không
  nhận dạng được thì `chua_review`, chứ không đoán.
- **Reviewer người thật** (không phải bot) có thể approve bằng đường khác — chưa có fixture.
- Chưa đo trên `windows-latest`.
