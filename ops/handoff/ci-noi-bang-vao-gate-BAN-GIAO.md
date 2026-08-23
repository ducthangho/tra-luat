# BÀN GIAO — việc kế tiếp sau `CI-BANG-PHU-THUOC` (#245)

> Tệp này **KHÔNG cấp việc**. Chưa có Packet Issue và chưa có lease cho việc mô tả ở đây.
> Đọc mục **§5 TRẠNG THÁI LEASE** trước khi chạm bất cứ tệp nào.
> Nguồn đầy đủ về packet vừa xong: `ops/handoff/ci-bang-phu-thuoc-exec-1-claude-20260822-handoff.md`.

## 1. Chuyện vừa xảy ra

Packet **#245** (lease `ci-bang-phu-thuoc-exec-1-claude-20260822`) giao **một nửa**, có chủ đích:

| vế | kết cục |
|---|---|
| **BĂM** | **LAND** qua PR #251 ⇒ `master` `26856f9`. `.github/checks/ci_phamvi.py` (135 dòng) · `.github/checks/ci_phamvi_test.py` (174 dòng) |
| **ĐỌC** | **KHÔNG land.** PR #247 **đóng, không merge** |

Vế ĐỌC không land **không phải vì hết giờ**. Bốn vòng review chứng minh cơ chế đo — audit hook
`sys.addaudithook` nạp qua `PYTHONPATH` — **không thể trung thực**: thứ tự khởi động Python là
**cố định** (`.pth` → `sitecustomize` → `usercustomize` → mã người dùng), và cả ba là cơ chế
**một khe một tên** mà ta **luôn** thắng vì chèn thư mục tạm lên đầu `PYTHONPATH`. Nên **không
tên nào an toàn**, và hook ở khe cuối **không bao giờ** thấy được thứ chạy trước nó.

Phản chứng đo được trên #247: một `sitecustomize` đọc `ops/` vẫn cho `"ops": "doc_lap"`, `rc=0`.

**ĐỪNG dựng lại vế ĐỌC theo hướng đó.** Đó là **kết luận phủ định đã trả giá bốn vòng**, không
phải một việc còn dở. Hai hướng còn lại, chưa hướng nào có phản chứng: cài tracer **trước**
`site` init (`.pth` trong user-site tạm), hoặc bỏ hẳn startup-hook và để `tl selftest` **TỰ KHAI**
tập đọc từng ca.

## 2. Việc được khuyến nghị: nối bảng vào `ci.yml`

Đo được, không suy:

```
grep -n "ci_phamvi" .github/workflows/*.yml      -> KHONG mot dong nao
rg -n "ci_phamvi" --glob '!.github/checks/*' .    -> KHONG mot dong nao
```

Hai tệp vừa land **nằm im** — không đường nào trong kho gọi chúng, nên chúng **không tích được
lượt chạy nào**. Lý lẽ tách slice của đặc tả (*"bảng chạy vài lượt trong lúc chưa ai dựa vào
nó"*) hiện **chưa thành thật**. Cùng đúng bài học mà `ci.yml:368` tự ghi:

> *"guard không nối vào đường chạy tự động thì guard chỉ là tài liệu"*

Việc: thêm một bước gọi `python .github/checks/ci_phamvi_test.py` vào job `gate`. Đó là **M7**
của đặc tả đóng băng `ops/specs/CI-FASTPATH-THEO-DIFF.md` (sha256
`32ba1b32ec9436453f7f8fe3c6f8e4d9a4af6e2ceb4e40bfefd8ffb2917d7580` — **chỉ có trên nhánh
`origin/ops/ci-bang-phu-thuoc`, KHÔNG có trên `master`**), tách thành **Stable Slice** theo §12.

**KHÔNG làm công tắc fast-path trong slice này** — xem §4.

## 3. BỐN thứ đã ĐO SẴN — dùng lại, đừng đo lại

1. **Suite chạy được trong clone NÔNG.** `git clone --depth=1` ⇒ `is_shallow=true` ⇒ suite
   `7/7`, `rc=0`. `fetch-depth` **không** phải rủi ro. (`ci.yml` vốn đã đặt `fetch-depth: 0` vì
   lý do khác — `doc-claims-check` L2 cần lịch sử để tra SHA.)

2. **Chi phí: 1,8 giây** (`7/7`, `rc=0`) — **không phải 3–4 phút**. Con số 3–4 phút trong hồ sơ
   cũ là của bản **có vế ĐỌC** (nó chạy `tl selftest` hai lượt); bản đã land không còn vế ấy.

   **Hệ quả cho thiết kế, và phải nói thẳng ra:** quyết định **Q3** của đặc tả — *chỉ chạy khi
   chạm `ci.yml` hoặc tệp bảng, cộng một lượt định kỳ hàng tuần* — có lý lẽ nguyên văn là
   *"Chạy mọi PR thì tự phản (cộng 3–5 phút vào đúng thứ đang đi cắt)"*. **Lý lẽ ấy đo trên bản
   đã bị bỏ.** Với 1,8 giây thì chạy **VÔ ĐIỀU KIỆN** vừa rẻ hơn vừa an toàn hơn cách có điều
   kiện, và bỏ được cả `schedule:` lẫn toàn bộ logic `if:`.

   Đây là **đề xuất LỆCH đặc tả**. Phải nêu thẳng cho người giữ kho và cho reviewer **kèm số**,
   đừng lặng lẽ áp — và cũng đừng lặng lẽ theo Q3 chỉ vì nó đã được đóng băng.

3. **HIỂM HOẠ CHÍNH — `n6` dựng symlink.** `n6_symlink_van_doc_lap` gọi `os.symlink`. Trên
   `windows-latest`, symlink thường **không tạo được** nếu thiếu Developer Mode/quyền.
   **Chưa ai đo.** Nối vào `ci.yml` mà không xử lý chỗ này thì job Windows **ĐỎ**.

   Và chốt bắt buộc theo doctrine: ca có nhánh *"không làm được thì bỏ qua"* **phải kèm chốt** —
   chỉ được tha khi đúng là nền không cho tạo symlink; trong kho thật mà thiếu thì **ĐỎ**.
   *"Ca có MẶT" khác "ca có ĐO"*. Tiền lệ đếm bỏ-qua đúng cách trong chính kho này:
   `ops/lease_publish_test.py` bỏ 8 ca trên Windows, **in ra từng ca kèm lý do**, và `t73` canh
   chính việc bỏ qua đó.

4. **Bảng đột biến đã đo lại toàn bộ** — 6 đột biến, không cái nào sống sót, **kèm nguyên văn
   phép thay** từng cái. Ở §3 của handoff packet 1. Dùng lại được.

## 4. CẢNH BÁO — đặc tả kế nhiệm KHÔNG còn thi hành được nguyên văn

`CI-FASTPATH-THEO-DIFF` có **ĐIỀU KIỆN MỌC đã thoả**: hiện vật **có trên `master`**, đúng như nó
đòi (*"không phải khi PR của nó merged — revert được — không phải khi Issue đóng"*).

**Nhưng** lý lẽ của quyết định **Q1** đọc nguyên văn:

> *"nếu merge chỉ chạm nhóm ngoài **cả tập đọc lẫn tập băm** thì cây runtime **giống hệt** commit
> cha, nên lượt mới **kế thừa** bằng chứng còn hiệu lực thay vì dựng lại."*

Vế **tập đọc không tồn tại**, và theo §1 sẽ không tồn tại theo cơ chế cũ. Dựng hàm quyết định
fast-path theo nguyên văn ⇒ cho đi đường tắt **dựa trên nửa bảng** — đúng hình dạng *"chứng minh
bỏ bước này an toàn bằng thứ nhẹ hơn"* mà `dieu_kien_dung` của lease #245 liệt vào điều kiện
DỪNG, và `CLAUDE.md` đã đếm **ba** lần. Chạm ba là ngưỡng phải hỏi *"có nên làm theo cách này
không"*, không phải *"vá thế nào"*.

Theo chính luật của đặc tả — *"Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**"* — công tắc
fast-path cần **`CI-FASTPATH-THEO-DIFF-r2`** trước khi cấp lease.
**M7 thì không**: nó không phụ thuộc vế ĐỌC, nên tách Stable Slice được và chạy trước được.

## 5. TRẠNG THÁI LEASE — chỗ phải DỪNG

**CHƯA có Issue và CHƯA có lease cho việc này.** Phiên trước **không tự cấp**, vì hai lý do đo được:

- `.github/workflows/ops-publish-lease.yml` chỉ bắn trên `push: branches: ['ops/**']`. Đặt tệp
  lease trên nhánh `claude/**` thì **không comment nào được đăng** ⇒ một lease **trông như đã
  cấp mà thật ra chưa**. Phiên trước bị ràng buộc chỉ được đẩy lên nhánh chỉ định của nó.
- `CLAUDE.md`: *"ĐỌC ĐƯỢC KẾ HOẠCH KHÔNG PHẢI LÀ ĐƯỢC GIAO VIỆC"* — thứ giao việc là Packet
  Issue kèm lease còn hiệu lực. **Đừng tự cấp lease cho chính mình.**

Bẫy kèm theo, đã đo: workflow có `paths:` **đã từng không chạy** ở lần đẩy **TẠO** nhánh mới.
Nên sau khi đẩy lease phải **ĐO** là workflow đã chạy (`list_workflow_runs` lọc theo nhánh),
đừng suy từ việc `git push` thành công.

### Làm gì ngay

1. Đọc `CLAUDE.md`, `docs/PROTOCOL_DA_PHIEN.md`, handoff packet 1, và hai tệp đã land.
2. Chạy `python3 .github/checks/ci_phamvi_test.py` để **tự** có bằng chứng dương — phải
   `7/7`, `rc=0`. Đừng tin con số trong tệp này; nó là lời khai cho tới khi bạn chạy.
3. **Trình người giữ kho** đúng ba thứ rồi CHỜ:
   - bản vá `ci.yml` **cụ thể** (mấy dòng, đặt ở đâu trong job `gate`);
   - cách xử lý hiểm hoạ symlink trên Windows, **kèm chốt chống bỏ-qua-âm-thầm**;
   - khuyến nghị **vô điều kiện vs theo Q3**, kèm số 1,8 giây, nói rõ đó là lệch đặc tả.
4. Chỉ sửa `ci.yml` **sau khi** có Issue + lease. Nhánh làm việc do lease khai.

Bước 1–3 **không cần lease** và làm được ngay. **Đừng viết một dòng nào vào
`.github/workflows/ci.yml` trước bước 4.**

## 6. Kỷ luật của kho (đã trả giá — đừng lặp)

- **Cổng xanh vì `rc=0` là cổng có thể bị lừa** — đòi bằng chứng DƯƠNG (`N/N`, hai số bằng nhau).
- **Đo CI theo JOB, không theo `check_suite`.**
- **Đột biến chạy trên BẢN SAO** (`git worktree add --detach`), không trên cây thật.
- **`ci.yml` khai `pull_request:` không kèm `types:`** ⇒ gắn nhãn `windows` **KHÔNG** sinh lượt
  chạy nào. Muốn có Windows trước khi merge thì gọi tay `workflow_dispatch` trên đúng ref đó.
- **Đừng viết chuỗi bỏ-qua-CI nguyên văn trong thông điệp commit**, kể cả khi đang trích dẫn để
  giải thích — GitHub khớp chuỗi trên **toàn** thông điệp, và nó đã tắt gate của `master` một lần.
- **Trước khi merge: đọc REVIEW, không chỉ đọc cổng.** Connector codex gửi verdict **SẠCH** bằng
  một issue comment thường kèm dòng `Reviewed commit:` — hỏi `get_reviews` thấy **rỗng** không
  nghĩa là chưa review.
- **Ghim `git config core.abbrev 7`** trước khi chạy gate.
- Trước khi kết luận từ một chỗ **RỖNG**, hỏi: *"nếu thứ tôi đang tìm có thật thì nó được ghi ở
  đâu?"* — rồi đi hỏi đúng chỗ đó.
