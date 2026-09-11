# ADR-0047 — Nguồn tin cậy cho CỔNG ĐỌC lease: danh tính ghim, hồ sơ tiến trình, toàn vẹn object

- **Trạng thái:** Proposed (2026-09-08; chủ kho duyệt SOẠN tại Review Rescue Checkpoint của PR #475 — chưa
  có mã, chưa có phản chứng chạy được ⇒ chưa `Accepted`; đồng bộ với spec r9 theo S10 lượt 7, 09-09-2026)

> **Vì sao có ADR này.** Cùng MỘT hình dạng lỗi — *"cổng đọc lease tin một nguồn mà chưa xác minh"* — trúng
> **5** lượt cross-review liên tiếp của đặc tả `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (PR #475), mỗi lần ở
> một lớp sâu hơn: symref cục bộ (lượt 1, L1 `default-ref-is-untrusted-cache`) → remote `origin` bất kỳ
> (lượt 2, N1) → config kho / helper / `refs/replace` (lượt 3, R1/R2) → env tiến trình + bytes cache (lượt 4b,
> S1/S2) → miền giá trị config + cạnh đồ thị object (lượt 5, S1/S2). Verdict: `b60a755f…` · `bb293295…` ·
> `6b8dde21…` · `7d3017ec…` · `1596d562…` (hiện vật `ops/reviews/thu-hoi-lease-va-cap-lai-spec/`). §12 protocol:
> *"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên tiếp tục cách làm đó"* — reviewer lượt 4b và
> 5 cùng khuyến nghị ADR trước thi công; đặc tả r4 tự khai *"lượt 4 còn tìm ra ⇒ dừng packet, ADR riêng"* rồi
> lượt 5 vẫn tìm ra. Đây là ADR ấy. Nó **không** phải bản vá lần thứ sáu: nó nói **cổng đọc được tin cái gì**,
> để lần sau reviewer đo hợp đồng này thay vì mỗi lượt bóc thêm một lớp.

## Quyết định

Mọi **cổng đọc lease** — `check` · `ai-dang-giu` · `body` · `kiem-github` · `kiem-thu-hoi-github` trong
`ops/lease_publish.py`, guard trong `.claude/dev/packet_loop.py`, và workflow tiếp nhận `ops-thu-hoi-admission.yml`
— chỉ được lấy verdict từ **một** ảnh chụp có đủ BA lớp dưới đây. Thiếu một lớp, hay một lớp *không đo được*,
thì trạng thái là `KHÔNG ĐO ĐƯỢC` và cổng **ĐỎ**, không phải "coi như sạch". **Hai biên mã lỗi (S10 lượt 7):**
reader/`lease_publish` trả `12`; wrapper giữ ánh xạ lỗi công khai của riêng nó — `packet_loop` trả `RC_STATE=8` kèm
nguyên nhân gốc (`reader_rc=12`) và không đổi state. ADR này giữ bất biến *"không đo được ⇒ đỏ"*; mã lỗi/giao diện cụ
thể ở spec (Q5/A10).

### Lớp 1 — DANH TÍNH nguồn ghim trong mã, không trong config

- Nguồn có thẩm quyền là kho canonical `KHO_CANONICAL = "github.com/ducthangho/tra-luat"`, ghim là hằng trong mã
  đã canonical; endpoint dựng **tường minh** từ hằng ấy (`https://` + `KHO_CANONICAL`). Cổng **không bao giờ**
  discovery qua tên remote (`origin`), qua `remote.<x>.url`, `url.*.insteadOf`, `remote.<x>.vcs` hay symref cục bộ.
- Nhánh mặc định = symref máy chủ trong advertisement (`ls-remote --symref … HEAD`); tham số `--nhanh-mac-dinh`
  do workflow truyền phải **bằng** symref; lệch/vắng/mơ hồ ⇒ 12. Không fallback sang `master`/`main` đoán.
- `ls-remote --get-url origin`, `refs/remotes/origin/HEAD`, `.git/config` chỉ là **chẩn đoán**; không phải bằng chứng.
- Test tiêm nguồn giả (bare cục bộ) qua **API nội bộ**; **không** có biến môi trường hay cờ production nào đổi
  được authority. Đây là chốt chống chính lỗi "một cờ để test mở đường cho production".

### Lớp 2 — NỀN THỰC THI được duyệt, so với mỏ neo do người khác cấp

> Bản đầu của lớp này (08-09-2026, trước lượt review 6) chỉ băm *executable Git + version + tệp CA + tên helper*.
> Cross-review lượt 6 (S1, VERDICT `9090aadd…`) bác đúng chỗ: **tên helper không định danh bytes chương trình mà nó
> phân giải tới**, `http.sslCAPath` là **thư mục**, và transport HTTPS/runtime/thư viện nằm **ngoài** digest — cùng
> digest vẫn có thể đi qua bộ helper/trust khác. Đó là lần thứ **6** của hình dạng lỗi này, và nó nằm ngay trong ADR
> viết ra để chặn nó. Lớp 2 vì thế nói về **nền thực thi**, không nói về một hàm băm.

- **Deployment profile là một NỀN THỰC THI được duyệt**, không phải tập biến của lời gọi: một manifest bất biến ghim
  image/runtime (Git chính: đường, sha256, version; chương trình HTTPS/credential helper **thật sự dùng**, hoặc "không
  dùng"; runtime/thư viện; **toàn bộ trust store hiệu lực** — tệp, thư mục CA, default store nếu dùng; endpoint và proxy
  profile: scheme/host/port). Không đòi băm đệ quy cả OS: dùng manifest của image/deployment đã xác minh và **giữ
  read-only suốt invocation**.
- **Producer của manifest độc lập với caller và với cây ứng viên** (bước bootstrap/deployment tin cậy); **approver** của
  mỏ neo `PROFILE_ADAPTER_DA_DUYET` là chủ kho hoặc người được chủ kho **uỷ quyền bền, có phạm vi** (§2 protocol), qua
  commit có review — executor không tự duyệt. **Cấm** đo profile từ chính deployment tuỳ ý rồi tự
  đăng ký làm "đã duyệt" trong cùng lượt chạy — đó là tự khai, đúng thứ luật 3 dưới đây cấm.
- Adapter dựng **env con từ RỖNG** (không kế thừa `os.environ`); `GIT_DIR` = repo tạm cô lập do adapter tạo
  (`git init --template=`), `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_NO_REPLACE_OBJECTS=1`,
  `GIT_TERMINAL_PROMPT=0`, `GIT_ALLOW_PROTOCOL=https`, `LC_ALL=C`; executable giải bằng đường tuyệt đối **trong profile**
  trước khi chạy. Danh sách cấm (`GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_EXEC_PATH`, `GIT_SSL_NO_VERIFY`,
  `GIT_PROXY_COMMAND`, `GIT_ASKPASS`, `SSH_*`, …) là **chẩn đoán**; thứ cưỡng chế là profile.
- Từ profile chỉ lấy một **allowlist HỮU HẠN theo khoá + kiểu + miền giá trị**: `credential.helper` = không dùng hoặc
  đúng helper trong manifest; username chỉ scope URL canonical; `http.sslCAInfo`/`http.sslCAPath` chỉ đúng trust store
  trong manifest; proxy chỉ đúng scheme/host/port đã duyệt, và `http.proxy`/`HTTPS_PROXY`/`https_proxy` phải quy về
  **cùng một** giá trị. Không wildcard `http.*`/`credential.*`, không dò chuỗi; giá trị **parse theo kiểu Git** rồi chuyển
  thành đối số Git hữu hạn; không kế thừa `GIT_CONFIG_*` của caller; khoá lạ ⇒ 12; TLS verification bắt buộc.
- **Digest** = sha256(JSON UTF-8 chuẩn hoá, `sort_keys`, schema_version ghim) của manifest + cấu hình không bí mật hiệu lực
  + định danh/version nguồn secret. Đường tạm (`HOME`, `GIT_DIR`, object store) là **vai trò** do adapter tạo/xác định và
  kiểm isolation/ownership riêng — **không** đưa đường tạm ngẫu nhiên vào digest. Digest phải **bằng** một neo đã duyệt;
  lệch hoặc không tính được ⇒ 12. Đây là **MỘT** phép so profile duy nhất: câu "receipt ghi hồ sơ" không tạo thêm chốt so
  thứ hai (chốt kép che mutant — S3 lượt 6).
- Hệ quả chấp nhận: đổi image/runner/package làm manifest đổi ⇒ **12 cho tới khi neo mới được duyệt**. Một deployment hợp
  lệ chưa đăng ký bị chặn là đúng thiết kế; chữa bằng duyệt profile có receipt, không bằng fallback kế thừa env.
- **Còn mở, của chủ kho:** nền thực thi cụ thể nào được tin (runner GitHub-hosted theo image digest? self-hosted?) và
  quy trình duyệt mỏ neo. ADR này giữ bất biến; giá trị điền vào khi có quyết định, trước ready slice A0.

### Lớp 3 — TOÀN VẸN OBJECT: băm lại bytes, cạnh từ bytes đã băm, store cô lập

- Cache object cục bộ của kho đọc là **không tin cậy**. Adapter đọc object qua `GIT_DIR` = repo tạm cô lập (không
  ref, không `refs/replace`, config trống) + `GIT_OBJECT_DIRECTORY` = object directory của kho nguồn **giải một lần
  bằng API Git** (bare / working copy / linked worktree — không ghép literal `<kho>/.git/objects`; S8 lượt 6), chỉ đọc;
  alternates chỉ qua `GIT_ALTERNATE_OBJECT_DIRECTORIES` do adapter dựng; loose + pack; partial/promisor thiếu object ⇒
  12 (không phải "vắng"); shallow ⇒ 12; `cat-file --batch`. Đo được (reviewer lượt 5): repo tạm **không** trỏ
  object directory ⇒ `cat-file` trả `<OID> missing` với `rc=0` — nên `missing` là **12**, không phải "vắng".
- Với mọi object dùng để quyết định: đọc bytes một lần, băm `sha1("<type> <size>\0" + bytes)` **= OID** rồi mới
  dùng; **mọi cạnh** (entry tree: mode/tên/OID; header `tree`/`parent` của commit) trích từ **bytes đã xác minh** của
  object cha. Không `merge-base`, không revision walker, không `ls-tree` để suy cạnh. Ancestry S→H = tự đi đồ thị
  parent với visited-set + ngân sách có đơn vị: **vượt** trần count/byte/depth (biên inclusive: n≤bound qua) hoặc hết
  deadline ⇒ 12 — định nghĩa từng counter và biên ở spec Q4.5, không ở đây. Memoize theo `(expected_type, OID)` trong
  một ảnh chụp, cache-hit vẫn kiểm actual type.
- Lời khai *"sổ vắng"* chỉ hợp lệ khi tree cha **đã xác minh** không có entry tương ứng. Lệch băm / thiếu / kiểu
  sai / `rc≠0` ⇒ 12.
- `refs/replace` của kho nguồn **không thể** áp vì repo tạm không có ref; no-replace là dây đai thứ hai, băm là dây
  đai thứ ba — **ba chốt riêng, ba seam riêng** trong catalog mutant, không hứa "một lớp bắt tất cả".

### Ba luật cắt ngang cả ba lớp

1. **Ba trạng thái, không phải hai:** `có` · `không` · `KHÔNG ĐO ĐƯỢC`; trạng thái thứ ba làm cổng ĐỎ (doctrine
   `None ≠ False`). Không "đệm offline", không cache kết luận qua hai lần đọc.
2. **MỘT ảnh chụp, MỘT phép tính:** map ref cục bộ chụp **trước** discovery; so **từng tên với cùng SHA40** với
   advertisement; không chụp lại giữa chừng; mọi lệnh đọc dùng chung một hàm trạng thái.
3. **Claim phái sinh không bao giờ THU HẸP thẩm quyền:** trường phái sinh tự khai trong lease/Issue (`effective_write_set`,
   `da_bi_thay_the`, …) chỉ được **so** với giá trị tính lại từ nguồn đã xác minh; lệch ⇒ 8 (lỗi claim). Input khai báo
   hợp lệ (`write_set`, timestamp, …) là đầu vào, không phải phái sinh không producer. Descriptor ngoại lệ / activation
   binding không xác minh được theo Q13 ⇒ reader 12 rồi ánh xạ tại caller; descriptor phải **bằng** hằng ghim trong mã
   đã canonical.

## Phạm vi và giới hạn, nói thẳng

- ADR này là **hợp đồng cho cổng ĐỌC**; nó không nói ai được **GHI** (ADR-0023/0034) và không thay đổi luật lease §4.
- Nó **không** chứng nhận nền runner/OS: băm executable + CA + version là *định danh của cái ta đã nghĩ tới*, không
  phải chứng minh toàn bộ chuỗi thực thi TLS/proxy là sạch. Reviewer lượt 5 nói đúng: *"không đòi băm đệ quy cả OS"*.
  Giới hạn ấy được **khai** trong receipt (digest + trường không bí mật), không được che.
- Nó **không** chốt kênh receipt của workflow tiếp nhận (M9) hay lifecycle của ngoại lệ closure (Q13) — hai thứ ấy
  là hợp đồng của đặc tả, không phải nguồn tin cậy.
- Hợp đồng chi tiết (allowlist khoá cụ thể, thành phần digest, tập gốc object, trần độ sâu) sống trong đặc tả
  Q4.1/Q4.5 và trong mã A0; ADR chỉ giữ **bất biến**. Đặc tả đổi chi tiết mà giữ ba lớp + ba luật thì ADR không đổi.

## Cổng

**0 cổng hôm nay** — chưa có một dòng mã nào: `ops/lease_publish.py` trên `origin/master` (`585c7d5`, 08-09-2026)
không có adapter, không có profile digest, không băm lại object; `check` vẫn `any(...)` trên mọi ref (đo trong đặc
tả §1). `adr-song` chỉ canh đăng ký/trạng thái của dòng này ở §20.

Điều kiện promote lên `Accepted`: slice **A0** của packet `THU-HOI-LEASE-VA-CAP-LAI` land với ca nghiệm thu A2
(danh tính/symref/discovery) và A6 (hồ sơ adapter, routing object-store, băm, no-replace — mỗi seam một đột biến)
**ĐỎ đúng ca** trong `ops/lease_publish_test.py`, và receipt A0 ghi `PROFILE_ADAPTER_DA_DUYET` đầu tiên đã readback.
Tới lúc đó, dòng "0 cổng" ở §20 phải được đo lại và ghi thành `có nhắc: <tệp>×<n>` — không tự nâng bằng chữ.
