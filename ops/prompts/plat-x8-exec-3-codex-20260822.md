# Prompt BẤT BIẾN — EXECUTOR `PLAT-X8` (#225), **lượt 2**, provider `codex`

> # ✅ CÓ HIỆU LỰC — **thẩm quyền là TỆP LEASE, không phải dòng này**
>
> ## Prompt này CỐ Ý KHÔNG nêu tên lease, số revision, hay `posted_comment_id`
>
> Hai bản trước của chính prompt này đã chết vì nêu. Chuỗi thật, trong một giờ: lease `…exec-2`
> (rev 1) → chốt chống đăng trùng trả `rc=9` nên revision phải đổi id thành `…exec-2r2` → prompt
> vừa viết xong lập tức nói dối, vì nó chép tên lease cũ. **Executor codex bắt được và DỪNG** —
> đúng thứ nó được dặn làm, và nó đúng.
>
> Nên bản này bỏ HẲN mọi thứ đã có trong lease: tên lease, revision, `posted_comment_id`, hạn chót.
> Đọc chúng ở **tệp lease** mà phiên điều phối đưa đường dẫn. Prompt chỉ giữ thứ lease KHÔNG có:
> nếp của kho, chỗ dễ đọc lệch, tiêu chí hoàn tất.
>
> **Luật rút ra:** hai tài liệu cùng chép một sự thật thì chúng sẽ trôi lệch, và bên quên cập nhật
> chính là bên nói dối. Cách chữa không phải "nhớ cập nhật cả hai" — mà là **chỉ một bên giữ**.
>
> **MỌI BẢN PROMPT CŨ GIỮ NGUYÊN TRẠNG, KHÔNG SỬA ĐÈ.** `plat-x8-exec-1-codex-20260821.md` và
> `plat-x8-exec-2r2-codex-20260822.md` đều đang bị một lease ĐÃ ĐĂNG neo vào băm của chúng. Bản đầu của lượt r2 đã sửa đè tệp kia — `t23` bắt ngay (*"LỆCH BĂM"*), và
> nó đúng: **một artefact đã bị lease neo là BẤT BIẾN**; muốn đổi thì ra tệp mới, không sửa tại chỗ.
> Lý lẽ *"giữ tên tệp để con trỏ cũ khỏi chết"* của bản trước SAI ngược: con trỏ là BĂM, nên giữ tên
> mà đổi ruột chính là cách giết con trỏ.
>
> Lease lượt **1** (`plat-x8-exec-1-codex-20260821`) đã bị RÚT, chưa từng đăng — biên bản
> `ops/RUT_LEASE_PLAT_X8_20260821.md`. Lease đang hiệu lực và hạn chót của nó: **đọc ở tệp lease**.
>
> **Vật cản đã hết.** `#238` land `563e0eb8` lúc 11:58:18Z 22-08 (PR #246). Quét lease toàn ref lúc
> 14:09:32Z: 22 lease chạm `ops/lease_publish*`, 9 chưa hết hạn, **cả 9 thuộc packet ĐÃ LAND**
> ⇒ **0 lease còn hiệu lực**. Đừng đọc *"chưa hết hạn"* thành *"đang giữ"*.
>
> **NGOẠI LỆ `ADR-0045`.** Packet `sensitive` + executor `codex` là ngoại lệ CÓ ĐIỀU KIỆN, hợp lệ khi
> lease (a) do chủ kho chỉ định tường minh · (b) reviewer khác nền · (c) khai `review_class` ·
> (d) **khai RÕ là ngoại lệ theo §2** · (e) human readback trước land. Lease lượt 2 có ĐỦ (a)–(e) —
> khối `ngoai_le_ADR_0045`. **KHÔNG cổng nào canh việc này** (đo: `lease_publish.py` có 0 chỗ nhắc
> `review_class`/`0045`; `PROTOCOL §20` xếp `ADR-0045` là `0 cổng`) ⇒ preflight THỦ CÔNG, không phải
> bằng chứng cổng dương tính. **(e) là việc của lượt LAND — đừng coi là đã xong.**
>
> ## Bản trước của chính prompt này đã SAI, và nó suýt tới tay bạn
>
> Bản neo trước ghi *"CHƯA CÓ HIỆU LỰC — ĐỪNG DÙNG NGUYÊN TRẠNG"*, *"chưa cấp lease được"*,
> *"đặc tả vẫn mang hộp ⛔ ĐỪNG CẤP LEASE"*, nhánh `codex/plat-x8-exec-1`, sàn `N >= 42`. **Tất cả
> đã sai** vào lúc nó được neo. Nguyên nhân: phiên điều phối neo lại theo **BĂM**, nên `grep` băm tìm
> được mọi chỗ trích băm nhưng **không bao giờ** thấy câu khẳng định trạng thái viết bằng CHỮ.
> **Quét theo băm không thay được quét theo TRẠNG THÁI.** Nếu bạn thấy câu nào trong tệp này vẫn nói
> ngược với lease hoặc đặc tả — **DỪNG và báo**, đừng tự hoà giải.

Bạn là NGƯỜI THI CÔNG packet này. Reviewer sẽ là `claude` — khác họ model, tiêu chí N14 thoả.

**ĐẶC TẢ CÓ THẨM QUYỀN là `ops/specs/plat-x8.md`**, băm
`d85a75d835566c902cb62fead8521ad44851baa388d65329e4c94025b9bad6ca` — **BẢN 5**, 22-08-2026.
Bản 5 là bản **lease đang hiệu lực neo vào** (đối chiếu `spec_sha256_required` trong tệp lease): hộp ⛔ đổi từ *chặn* sang
*đã giải* (`#238` land `563e0eb8` lúc 11:58:18Z, quét 13:01Z ra **0** lease còn hiệu lực), còn
mười ba phát hiện **giữ nguyên văn** làm hồ sơ. Bản 4 (`46d9a0299a09…`), `3i` (`ca852d95ab59…`) và mọi bản trước đã HẾT HIỆU LỰC —
**bản 4 bỏ sót ba con số phụ thuộc `#238`; bản 5 sửa.**
Bản 3h (`3c9bff4f5410…`), 3g (`f3a2f5595120…`), 3f (`497c68360de7…`), 3e (`ce14fb0b75e4…`), 3d (`f7f8e6209e4f…`), 3c (`182ea7621d02…`), 3b (`308d0cf44fc1…`) và mọi bản trước KHÔNG còn hiệu lực. Hộp đầu đặc tả nay là **✅ ĐÃ GIẢI**, nhưng **vẫn phải đọc**: nó giữ nguyên văn
mười ba chỗ từng sai, ba trong số đó là lỗi của chính phiên soạn đặc tả. Prompt này KHÔNG chép lại đặc
tả — chép là dựng hai bản trôi lệch. Đọc đặc tả TRƯỚC, rồi đọc prompt này để biết nếp của kho.
Chỗ nào prompt này lệch đặc tả thì **đặc tả đúng**.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#225` — `[PLAT-X8]` |
| đặc tả | `ops/specs/plat-x8.md` — bản **5** (băm ở trên; **kiểm bằng `sha256sum` trước khi đọc**). Các bản trước (`9cb54a2e…`, `b88c53df…`, `328a74fa…`, `308d0cf4…`, `182ea762…`, `f7f8e620…`) KHÔNG còn hiệu lực |
| write set | `ops/lease_publish.py` · `ops/lease_publish_test.py` — **ĐÚNG hai tệp** |
| base | **`08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9`** = `origin/master` sau khi `#238`/`#246` land. Bằng `base_sha` trong lease |
| nhánh | **`codex/plat-x8-exec-2`** (`branch_ownership: exclusive`) |

Trần `sensitive` của ADR-0044: **≤3 tệp / ≤300 dòng thêm**. Bạn dùng 2 tệp; suất thứ ba chừa cố ý
cho lượt vá sau verdict. Đừng tiêu nó.

## 2. Việc

Cổng `ops/lease_publish.py` hiện **TÍNH 0 dòng** về lớp review — nó nhận LỜI KHAI. Đo được:
`rg review_class ops/lease_publish.py` = 0, `rg schema_version ops/lease_publish.py` = 0.
Packet này thay lời khai bằng phép TÍNH từ `write_set`.

Chín mục tiêu ở §5 đặc tả, **mười bốn** tiêu chí nghiệm thu ở §6 (`A13`/`A14` là phản chứng
của hai P1 cross-review lượt 1 — đừng bỏ). **Mỗi tiêu chí đã nêu sẵn phép đo
làm nó ĐỎ** — đó không phải gợi ý, đó là phần bắt buộc của bằng chứng.

**Ba chỗ dễ đọc lệch, nói trước:**

1. **Bảng `_BANG_LOP` là danh sách CHO PHÉP, không phải danh sách cấm.** Danh sách cấm thua từ
   trong thiết kế — nó phân biệt CÁCH VIẾT chứ không phân biệt THẨM QUYỀN. Đo được ở `v1.36.68`.
2. **ĐỪNG nới bảng.** §4.2 đặc tả xếp việc nới vào `ngoai_pham_vi`, và người giữ kho đã quyết
   **giữ nguyên** ngày 21-08-2026 sau khi có con số 15/15 trên bàn. Nới bảng là packet khác.
   A7 là đột biến **nới bảng để ca đích ĐỎ** — đó là phép đo, không phải lời mời sửa bảng.
3. **Cổng này mua tính NHẤT QUÁN, không mua tính ĐÚNG của bảng** (§8 đặc tả). Đừng viết chú
   thích hay thông điệp commit nói rộng hơn thế. Cùng kỷ luật ấy áp cho §9.3: cổng đo **lời khai
   về phạm vi**, KHÔNG đo phạm vi ĐÃ XẢY RA — nó không đọc `risk` (0/49 lease có trường ấy) và
   không đọc `diff thật` (chưa tồn tại lúc đăng lease). Đừng viết câu nào hàm ý nó đọc.
4. **Mục tiêu 6 KHÔNG tra cứu gì cả.** Lease reviewer `schema_version >= 2` ⇒ `sensitive` **vô
   điều kiện**; cổng **không** mở `ops/leases/`, **không** tra lease executor, **không** kế thừa.
   Q1 đã bị THU HỒI sau bốn P1 trên cùng một đường (§10 đặc tả). **Đừng dựng lại đường kế thừa**,
   kể cả khi nó trông hiển nhiên đúng — `A3` và `A13` khoá đúng sự VẮNG MẶT của cơ chế ấy, nên
   chúng sẽ ĐỎ nếu bạn thêm bất kỳ lượt đọc thư mục nào vào đường reviewer.
5. **`A14` là vế DƯƠNG, phải sống.** Không có nó thì mọi bản vá "cho chắc" biến cổng thành máy trả
   `sensitive` mà không ai đo được.

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
   phải làm cổng ĐỎ (`None ≠ False`). Áp cho `write_set` của lease **executor**: thiếu, rỗng, hay
   không đọc được đều ⇒ `sensitive` (mục tiêu 3, tiêu chí `A6`).
   **KHÔNG áp cho mục tiêu 6.** Ở đó không có gì để đọc nên cũng không có trạng thái thứ ba —
   lease reviewer ra `sensitive` vô điều kiện. Câu này từng viết ngược (dặn xử lý ca *"lease
   executor đọc không được"* trong mục tiêu 6) — tàn dư từ TRƯỚC khi Q1 bị thu hồi, và làm theo
   nó là dựng lại đúng đường tra cứu mà `A3`/`A13` sinh ra để chặn. Cross-review bắt được (P2
   trên PR "#228").
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

§6 đặc tả, **A1–A14** — đủ mười bốn, không phải mười hai. `A13`/`A14` là phản chứng thêm sau
hai P1 của cross-review lượt 2; khai hoàn tất mà bỏ chúng là khai chưa chứng minh gì về đường
reviewer lẫn về vế dương. Nhắc ba cái hay bị bỏ:

- **A9**: `python3 ops/lease_publish_test.py` ⇒ `rc=0`, `N/N` **hai số BẰNG NHAU**, **`N >= 73`**.
  Nền hiện tại là **73/73** trên `08bb4ecd`. Sàn 42 của bản cũ là sàn CHẾT — nó nằm 31 ca DƯỚI thực tế. `rc=0` một mình là cổng có thể bị lừa — đòi bằng chứng DƯƠNG.
- **A13/A14**: `A13` đo HÀNH VI của *"không quét"* — thư mục lease chứa một tệp YAML **hỏng cú
  pháp** mà lease reviewer vẫn ra `sensitive`; thêm bất kỳ lượt đọc thư mục nào là ca ĐỎ vì tệp
  hỏng sẽ ném. `A14` giữ **vế dương** (executor `write_set: ['docs/x.md']` với bảng nới tạm ⇒
  `routine`, `rc=0`) — không có nó thì bản vá "cho chắc" biến cổng thành máy trả `sensitive`.
- **A12**: `ready to review` = CI xanh trên **exact head**, gọi bằng `workflow_dispatch`, **cả
  hai** job `success`. *"PR xanh"* KHÔNG đủ: `ci.yml` chỉ chạy `ubuntu` cho PR thường, còn master
  chạy cả `windows`. Gắn nhãn `windows` **không sinh lượt chạy nào** — workflow khai
  `pull_request:` mà không khai `types:`, nên `labeled` không nằm trong cò.

## 5. Ranh giới

**Commit vào nhánh `codex/plat-x8-exec-2`. ĐỪNG `git push`** — phiên điều phối đẩy sau khi kiểm.
Đừng đụng tệp ngoài write set. Đừng đụng `ops/NO_KY_THUAT.md` (thuộc `#209`) và đừng sửa 49 lease
cũ (forward-only, §4.1 đặc tả).

Hết attempt hoặc hết vòng review thì **DỪNG và báo**, đừng tự nới trần.
