# Prompt BẤT BIẾN — EXECUTOR `PLAT-X8` (#225), lượt 1, provider `codex`

Bạn là NGƯỜI THI CÔNG packet này. Reviewer sẽ là `claude` — khác họ model, tiêu chí N14 thoả.

**ĐẶC TẢ CÓ THẨM QUYỀN là `ops/specs/plat-x8.md`**, băm
`9cb54a2e4e7c4d66c60f7717e1ca8aacd57785222777d30dbadab2448157c120`. Prompt này KHÔNG chép lại đặc
tả — chép là dựng hai bản trôi lệch. Đọc đặc tả TRƯỚC, rồi đọc prompt này để biết nếp của kho.
Chỗ nào prompt này lệch đặc tả thì **đặc tả đúng**.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#225` — `[PLAT-X8]` |
| đặc tả | `ops/specs/plat-x8.md` (băm ở trên — **kiểm bằng `sha256sum` trước khi đọc**) |
| write set | `ops/lease_publish.py` · `ops/lease_publish_test.py` — **ĐÚNG hai tệp** |
| base | xem `base_sha` trong lease — neo vào `master` sau khi PR `#226` merge |
| nhánh | `codex/plat-x8-exec-1` |

Trần `sensitive` của ADR-0044: **≤3 tệp / ≤300 dòng thêm**. Bạn dùng 2 tệp; suất thứ ba chừa cố ý
cho lượt vá sau verdict. Đừng tiêu nó.

## 2. Việc

Cổng `ops/lease_publish.py` hiện **TÍNH 0 dòng** về lớp review — nó nhận LỜI KHAI. Đo được:
`rg review_class ops/lease_publish.py` = 0, `rg schema_version ops/lease_publish.py` = 0.
Packet này thay lời khai bằng phép TÍNH từ `write_set`.

Chín mục tiêu ở §5 đặc tả, mười hai tiêu chí nghiệm thu ở §6. **Mỗi tiêu chí đã nêu sẵn phép đo
làm nó ĐỎ** — đó không phải gợi ý, đó là phần bắt buộc của bằng chứng.

**Ba chỗ dễ đọc lệch, nói trước:**

1. **Bảng `_BANG_LOP` là danh sách CHO PHÉP, không phải danh sách cấm.** Danh sách cấm thua từ
   trong thiết kế — nó phân biệt CÁCH VIẾT chứ không phân biệt THẨM QUYỀN. Đo được ở `v1.36.68`.
2. **ĐỪNG nới bảng.** §4.2 đặc tả xếp việc nới vào `ngoai_pham_vi`, và người giữ kho đã quyết
   **giữ nguyên** ngày 21-08-2026 sau khi có con số 15/15 trên bàn. Nới bảng là packet khác.
   A7 là đột biến **nới bảng để ca đích ĐỎ** — đó là phép đo, không phải lời mời sửa bảng.
3. **Cổng này mua tính NHẤT QUÁN, không mua tính ĐÚNG của bảng** (§8 đặc tả). Đừng viết chú
   thích hay thông điệp commit nói rộng hơn thế.

## 3. Nếp của kho này — KHÔNG phải tuỳ chọn

1. **`rc` đọc TRỰC TIẾP từ tiến trình.** Nối `| tail`/`| head` là **nuốt mã thoát**. Và
   `MA=$?` SAU pipeline rồi đọc `${PIPESTATUS[0]}` là tự giết mã thoát — phép gán LÀ một lệnh,
   nó đặt lại `PIPESTATUS` về 0. Chốt fail-close đã chết vì dòng đó **ba lần**.
2. **Đột biến chạy trên BẢN SAO CẢ CÂY trong thư mục tạm** (A10), mỗi đột biến một **tên tệp
   riêng**. Ghi vào tệp thật rồi khôi phục trong `finally` là bom hẹn giờ: `finally` không chạy
   khi bị cắt giữa chừng, và một bản vá NGƯỢC đã đi thẳng vào commit theo đường ấy. Sao **một
   tệp** thay vì cả cây cũng sai — `HERE` trỏ lệch, số đo vô nghĩa.
3. **Bytecode có thể làm đột biến CHƯA TỪNG ĐƯỢC CHẠY.** CPython coi `.pyc` còn hợp lệ theo
   (mtime tính bằng **GIÂY**, kích thước) — hai đột biến cùng kích thước ghi trong cùng một giây
   thì bản sau chạy **mã của bản trước**, và mutant báo "giết 0/1" vì lý do đó suốt ba lượt
   review. Ba lớp bịt: xoá `.pyc` · `sys.dont_write_bytecode = True` · `invalidate_caches()`,
   cộng tên tệp riêng.
4. **Ca có MẶT khác ca có ĐO.** Harness `lease_publish_test.py` **KHÔNG có cơ chế bỏ qua** —
   `main()` chỉ `qua += 1` khi hàm không ném, nên một ca `return` sớm vẫn được đếm là ĐẠT. Đừng
   viết nhánh *"không thấy thì bỏ qua"*.
5. **Ba trạng thái, không phải hai:** `có` · `không` · **`không đo được`** — trạng thái thứ ba
   phải làm cổng ĐỎ (`None ≠ False`). Áp thẳng vào mục tiêu 6: lease executor *đọc không được*
   phải ra `sensitive`, không được lẫn vào nhánh "không thấy".
6. **A11 fail-close khi thiếu `actionlint`.** Thay bằng PyYAML là KHÔNG ĐO ĐƯỢC: **sáu** lượt
   cross-review từng kết luận "YAML ok" bằng PyYAML trên một tệp mà GitHub **từ chối**. Một cổng
   tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc nó cần nhất.
7. **ĐỪNG viết chuỗi bỏ-qua-CI** (`skip` + `ci` trong ngoặc vuông) vào thông điệp commit, **kể cả
   khi trích dẫn để giải thích** — GitHub khớp CHUỖI trên toàn thông điệp, dấu nháy ngược không
   phải hàng rào. Đã tắt gate của master thật một lần theo đúng đường này.
8. **Chú thích tiếng Việt có dấu trong `.py`**, theo tệp xung quanh. Ghi **LÝ DO** và **bằng
   chứng đo được**, không chỉ ghi "cái gì".
9. **Chú thích khẳng định về tệp mình đang nằm trong thì phải kiểm trên tệp đó.** Một câu sai ở
   đó biến bản vá thành bản phá.

## 4. Tiêu chí hoàn tất

§6 đặc tả, A1–A12. Nhắc hai cái hay bị bỏ:

- **A9**: `python3 ops/lease_publish_test.py` ⇒ `rc=0`, `N/N` **hai số BẰNG NHAU**, `N >= 42`.
  Nền hiện tại là **42/42**. `rc=0` một mình là cổng có thể bị lừa — đòi bằng chứng DƯƠNG.
- **A12**: `ready to review` = CI xanh trên **exact head**, gọi bằng `workflow_dispatch`, **cả
  hai** job `success`. *"PR xanh"* KHÔNG đủ: `ci.yml` chỉ chạy `ubuntu` cho PR thường, còn master
  chạy cả `windows`. Gắn nhãn `windows` **không sinh lượt chạy nào** — workflow khai
  `pull_request:` mà không khai `types:`, nên `labeled` không nằm trong cò.

## 5. Ranh giới

**Commit vào nhánh `codex/plat-x8-exec-1`. ĐỪNG `git push`** — phiên điều phối đẩy sau khi kiểm.
Đừng đụng tệp ngoài write set. Đừng đụng `ops/NO_KY_THUAT.md` (thuộc `#209`) và đừng sửa 49 lease
cũ (forward-only, §4.1 đặc tả).

Hết attempt hoặc hết vòng review thì **DỪNG và báo**, đừng tự nới trần.
