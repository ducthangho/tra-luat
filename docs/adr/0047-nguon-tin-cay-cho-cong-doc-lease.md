# ADR-0047 — Nguồn tin cậy cho CỔNG ĐỌC lease: danh tính ghim, hồ sơ tiến trình, toàn vẹn object

- **Trạng thái:** Proposed (2026-09-08; chủ kho duyệt SOẠN tại Review Rescue Checkpoint của PR #475 — chưa
  có mã, chưa có phản chứng chạy được ⇒ chưa `Accepted`)

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
thì trạng thái là `KHÔNG ĐO ĐƯỢC` và cổng **ĐỎ** (`rc=12`), không phải "coi như sạch".

### Lớp 1 — DANH TÍNH nguồn ghim trong mã, không trong config

- Nguồn có thẩm quyền là kho canonical `KHO_CANONICAL = "github.com/ducthangho/tra-luat"`, ghim là hằng trong mã
  đã canonical; endpoint dựng **tường minh** từ hằng ấy (`https://` + `KHO_CANONICAL`). Cổng **không bao giờ**
  discovery qua tên remote (`origin`), qua `remote.<x>.url`, `url.*.insteadOf`, `remote.<x>.vcs` hay symref cục bộ.
- Nhánh mặc định = symref máy chủ trong advertisement (`ls-remote --symref … HEAD`); tham số `--nhanh-mac-dinh`
  do workflow truyền phải **bằng** symref; lệch/vắng/mơ hồ ⇒ 12. Không fallback sang `master`/`main` đoán.
- `ls-remote --get-url origin`, `refs/remotes/origin/HEAD`, `.git/config` chỉ là **chẩn đoán**; không phải bằng chứng.
- Test tiêm nguồn giả (bare cục bộ) qua **API nội bộ**; **không** có biến môi trường hay cờ production nào đổi
  được authority. Đây là chốt chống chính lỗi "một cờ để test mở đường cho production".

### Lớp 2 — HỒ SƠ TIẾN TRÌNH tường minh, so với mỏ neo đã duyệt

- Adapter nguồn dựng **env con từ RỖNG** (không kế thừa `os.environ`); `GIT_DIR` = repo tạm cô lập do adapter tạo
  (`git init --template=`), `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_NO_REPLACE_OBJECTS=1`,
  `GIT_TERMINAL_PROMPT=0`, `GIT_ALLOW_PROTOCOL=https`, `LC_ALL=C`, `PATH` tối thiểu; executable `git` giải **một lần**
  thành đường tuyệt đối. Danh sách **cấm** (`GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_EXEC_PATH`, `GIT_SSL_NO_VERIFY`,
  `GIT_PROXY_COMMAND`, `GIT_ASKPASS`, `SSH_*`, …) là danh sách **chẩn đoán**; thứ cưỡng chế là allowlist.
- Từ deployment chỉ kế thừa một **allowlist HỮU HẠN theo khoá + kiểu + miền giá trị** — không wildcard theo tiền tố
  (`http.*`), không dò chuỗi trong giá trị; giá trị **parse theo kiểu Git** (bool/path/URL). Khoá ngoài allowlist ⇒ 12.
  Bài học CLAUDE.md *"danh sách CẤM không bao giờ đủ — đảo thành danh sách CHO PHÉP"* áp nguyên văn ở đây.
- **Profile digest** = sha256 của bản chuẩn hoá {khoá=giá trị không bí mật đã sắp xếp, đường tuyệt đối + sha256
  executable git, `git --version`, sha256 tệp CA, tên credential helper}; digest phải **bằng** mỏ neo
  `PROFILE_ADAPTER_DA_DUYET` ghim trong mã (đổi qua commit có review); khác hoặc không tính được ⇒ 12. Receipt ghi
  digest + các trường không bí mật. Hệ quả chấp nhận: một deployment hợp lệ chưa đăng ký **bị chặn** — chữa bằng
  duyệt profile có receipt, không bằng fallback kế thừa env.

### Lớp 3 — TOÀN VẸN OBJECT: băm lại bytes, cạnh từ bytes đã băm, store cô lập

- Cache object cục bộ của kho đọc là **không tin cậy**. Adapter đọc object qua `GIT_DIR` = repo tạm cô lập (không
  ref, không `refs/replace`, config trống) + `GIT_OBJECT_DIRECTORY` = objects của kho nguồn (chỉ đọc; alternates
  qua `GIT_ALTERNATE_OBJECT_DIRECTORIES`), `cat-file --batch`. Đo được (reviewer lượt 5): repo tạm **không** trỏ
  object directory ⇒ `cat-file` trả `<OID> missing` với `rc=0` — nên `missing` là **12**, không phải "vắng".
- Với mọi object dùng để quyết định: đọc bytes một lần, băm `sha1("<type> <size>\0" + bytes)` **= OID** rồi mới
  dùng; **mọi cạnh** (entry tree: mode/tên/OID; header `tree`/`parent` của commit) trích từ **bytes đã xác minh** của
  object cha. Không `merge-base`, không revision walker, không `ls-tree` để suy cạnh. Ancestry S→H = tự đi đồ thị
  parent với visited-set + trần độ sâu (chạm trần ⇒ 12). Memoize theo `(type, OID)` trong một ảnh chụp.
- Lời khai *"sổ vắng"* chỉ hợp lệ khi tree cha **đã xác minh** không có entry tương ứng. Lệch băm / thiếu / kiểu
  sai / `rc≠0` ⇒ 12.
- `refs/replace` của kho nguồn **không thể** áp vì repo tạm không có ref; no-replace là dây đai thứ hai, băm là dây
  đai thứ ba — **ba chốt riêng, ba seam riêng** trong catalog mutant, không hứa "một lớp bắt tất cả".

### Ba luật cắt ngang cả ba lớp

1. **Ba trạng thái, không phải hai:** `có` · `không` · `KHÔNG ĐO ĐƯỢC`; trạng thái thứ ba làm cổng ĐỎ (doctrine
   `None ≠ False`). Không "đệm offline", không cache kết luận qua hai lần đọc.
2. **MỘT ảnh chụp, MỘT phép tính:** map ref cục bộ chụp **trước** discovery; so **từng tên với cùng SHA40** với
   advertisement; không chụp lại giữa chừng; mọi lệnh đọc dùng chung một hàm trạng thái.
3. **Trường tự khai không bao giờ THU HẸP thẩm quyền:** `effective_write_set`, `da_bi_thay_the`, hay bất kỳ trường
   nào trong YAML lease/Issue chỉ được **so** với giá trị tính lại từ nguồn đã xác minh; lệch ⇒ 8. Descriptor ngoại
   lệ phải **bằng** hằng ghim trong mã đã canonical.

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
