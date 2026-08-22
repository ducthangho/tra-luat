# Bàn giao — phiên `tra-luat-5a`, 22-08-2026

**Vai:** điều phối + soạn tài liệu. **KHÔNG** phải executor của packet nào ⇒ bản này **không** theo
schema §7 (`ops/handoff/wp55-r4g1-handoff.md` mới là bản §7 thật). Không có `generation`, không
`attempts_used`, không head để review.

**Tiếp nối:** `ops/handoff/phien-dieu-phoi-20260821-handoff.md` (đã trên master). Bản đó vẫn đúng cho
phần lịch sử; bản này chép tiếp từ chỗ nó dừng.

**Trạng thái:** không việc nào đang dở. Một hẹn tự động đang chạy (§5).

---

## 1. Neo

```yaml
# Đo cùng lúc, trên cùng một commit. Đừng vá lẻ từng trường.
do_luc: '2026-08-22'
base_khi_ban_giao: 3f641673205b068e598676f61a429b3bfc25e973   # OID ĐẦY ĐỦ, không tiền tố 7
master_luc_cap_nhat: 2ab3560a8a406c1b436221fb3c6d23234aefdde0  # đã đi 50 commit — xem §5b
nhanh_lam_viec: claude/opus-5-plan-steps-y5r6ci   # đã hết việc, reset về master
pr_da_merge: 230
pr_dang_mo_lien_quan: [233, 234, 229]
hen_dang_chay: trig_0171iMNPHfQSn58J4VmPm6h1     # 06:00Z, kiểm #227
```

## 2. Phiên này đã làm gì

| # | việc | kết quả |
|---|---|---|
| 1 | Vá bốn con trỏ chết trong tài liệu có thẩm quyền | **PR #230 MERGE**, master `3f64167`, 8 tệp |
| 2 | Dán hộp ⛔ lên đầu `ops/specs/plat-x8.md` | bản **3b**, băm `308d0cf4…` |
| 3 | Ghi nợ mục **12** `PLAT-X4-721-dong-chua-verdict-nao-phu` | sổ nợ nay **12** mục |
| 4 | Đính chính append-only câu *"vòng 3 đã lấp chỗ ấy"* | trong `ops/THAM_DINH_KE_HOACH_20260821.md` |
| 5 | Viết bản giao việc hoàn thiện kế hoạch | `ops/prompts/phien-hoan-thien-ke-hoach-20260822.md` |
| 6 | Điều phối với phiên `session_018YdsqSNdxorwxVYW2d2PkH` (PR #233) | đã hồi âm, đã cam kết phạm vi |

Lượt master sau merge (`32552166181`) **xanh cả hai nền**, đo tới từng bước: `gate (windows-latest)`
28 bước chạy thật ~8 phút; `gate (ubuntu-latest)` 5m47s. Bốn bước `skipped` đều có điều kiện, ba cặp
skip **ngược nhau** giữa hai nền. **Việc Windows không còn treo.**

## 3. BỐN LẦN PHIÊN NÀY ĐO SAI — chép ra vì cả bốn cùng một họ

Cross-review (auto-review connector, 4 lượt trên #230) ra **chín** finding thật. Sáu cái là số trôi
theo thời gian. **Bốn cái dưới đây là phép đo SAI của chính phiên**, và đều đã được báo cho người
giữ kho **trước khi** bị bác — nên đính chính nằm trong chính các tệp đã land, không chỉ trong hội thoại.

| # | tôi khai | sự thật đo được |
|---|---|---|
| 1 | *"protocol KHÔNG có canon 2 vòng"* | **SAI.** `docs/PROTOCOL_DA_PHIEN.md:543` và `:561` có sẵn trần 2 lượt Codex/PR |
| 2 | *"`spec_sha256` 11/49 lease"* | **SAI.** Đếm chuỗi con, gộp hai lược đồ: `spec_sha256:` = **5**, `spec_sha256_required:` = **6** |
| 3 | *"X4 cấp HAI lượt review, không verdict ở đâu"* | **SAI.** **BA** lượt; kết quả lượt 1+2 là `changes_requested`, ghi trong **thân lease của lượt kế tiếp** |
| 4 | *"nhánh #227 đứng yên ⇒ executor có thể đã dừng"* | **SAI.** Họ đẩy sang nhánh **khác tên** (`land/227`) và đã mở **PR #234** |

**Họ chung:** cả bốn đều là *hỏi chỗ tiện tay thay vì hỏi chỗ kết luận được ghi*. (1) và (2) là grep
lỏng; (3) đọc `ops/reviews/` rồi kết luận về lịch sử review; (4) neo vào một **tên nhánh tự suy ra**.

**Chốt rút ra, đã áp:** đo bằng **hiện vật** và **khoá chính xác**, không bằng tên/chuỗi con/tín hiệu
gần nhất. Và trong tài liệu thì **bỏ số ghi cứng, thay bằng lệnh đo sống** — PR #230 ăn ba finding
chỉ vì số ghi cứng chết ở commit kế tiếp, ba lần trong cùng một PR.

### 3b. Bổ sung 05:23Z — bài học SẮC HƠN, do phiên #233 tìm ra

Phiên `session_018YdsqSNdxorwxVYW2d2PkH` xác nhận con số **230** và tìm ra gốc lệch 15: regex của họ
`^([a-z_][a-z0-9_]*):` đòi khoá **TOÀN CHỮ THƯỜNG**, mà kho dùng chữ HOA trong tên khoá để nhấn mạnh
(`assurance_KHONG_dat`, `write_set_KHONG_gom`, `pham_vi_NGOAI`, `la_luot_review_CUOI`, …).

Đã kiểm hai chiều, độc lập, trên `origin/master`: `yaml.safe_load` = **230** · regex = **215** ·
`yaml \ regex` = **15** · `regex \ yaml` = **0**. Tập 230 **phủ** 215, không phải hai tập lệch nhau.

> **Nguyên văn chỗ đáng nhớ nhất của họ:** bản đầu còn ship kèm một **lệnh tái lập dùng chính cái
> regex hỏng ấy**. Lệnh chạy được, chạy nhanh, và tái lập **trung thành** một con số sai — nên nó
> trông y hệt bằng chứng. **Một phép đo sai CÓ lệnh tái lập khó phát hiện hơn một phép đo sai không
> có gì**, vì cái lệnh mua cho nó sự tin cậy mà nội dung không xứng.

Điều này **sửa lại lời khuyên của chính bản bàn giao này**. §3 chốt *"thay số ghi cứng bằng lệnh đo
sống"* — chưa đủ. Một lệnh đo sống dựng trên phép dò sai chỉ là lời khai sai chạy nhanh hơn. Chốt
đúng có **hai** vế: (a) lệnh phải dùng **bộ phân tích CẤU TRÚC**, không phải regex trên văn bản thô;
(b) lệnh phải **fail-close** — bản mới của họ đòi `khong parse == 0`, nên tệp hỏng làm phép đo ĐỎ chứ
không lặng lẽ tụt số.

**Thứ khoanh được vùng lỗi là IN CẢ BA CỘT.** Cột giữa (`cổng đọc 8`) khớp tuyệt đối giữa hai bên,
nên lỗi bị dồn về cột đếm tên trường ngay lập tức. Nếu tôi chỉ nói *"215 sai"* thì họ phải truy cả
phép dò cổng. **Báo một con số lệch thì báo luôn con số nào KHỚP** — chỗ khớp mới là thứ khoanh vùng.

**Đếm hình dạng:** phiên #233 ghi nhận **ba lần trong MỘT ngày** cùng hình dạng *regex trên văn bản
thô thay cho bộ phân tích cấu trúc* — bộ quét lease khớp nháy KÉP trong khi YAML ghi nháy ĐƠN (báo
"0 va chạm" sai, giấu một va chạm thật) · `adr-song` đếm dòng bảng nằm trong khối mã có rào · và cái
này. Ba lần ⇒ theo doctrine của kho, câu hỏi đúng không còn là *"vá regex thế nào"* mà là **"có nên
dùng regex cho việc này không"**.

### 3c. Lỗi đo thứ SÁU — và nó khác năm cái trước

Năm lỗi ở §3 và §5b đều là **tôi đo sai**. Cái thứ sáu là **tôi KHÔNG đo**: tôi nhận khung của một
phiên khác vì nó nghe sắc hơn khung của mình, rồi chuyển tiếp cho người giữ kho **và** cho chính
phiên ấy như một xác nhận. Cross-review bắt (P2 trên PR #236).

Nguy hơn năm cái trước ở hai chỗ. **Một:** một phép đo sai của tôi thì chỉ mình tôi mang; một khung
sai được tôi *xác nhận* thì bên kia coi như đã có kiểm chứng độc lập — tôi biến lời khai của họ thành
bằng chứng mà không thêm một phép đo nào. **Hai:** cả phiên này tôi đòi *"đo, đừng nhận lời khai"*,
rồi nhận đúng một lời khai vì nó bất lợi cho tôi và nghe khiêm tốn.

**Chốt:** một khung **bác chính mình** vẫn phải đo. Tự phê không phải bằng chứng.

## 4. Hai con số tôi đã báo người giữ kho mà sau đó bị bác — đọc kỹ

- **"Mục D là hai field"** — hụt **hai bậc**. Đo lại: **49** lease dùng **230** tên trường mức gốc,
  `ops/lease_publish.py` nhắc **8**, còn **222** không ai kiểm. Phiên #233 đo ra 215/8/**207** —
  cột giữa **khớp tuyệt đối**, tổng lệch **15**, chưa ai phân định. Kết luận chịu tải không đổi: mục D
  là một **quyết định phạm vi**, không phải bản vá hai dòng. Phiên #233 đã cắt thành D1–D4.
- **"Protocol im lặng về trần review"** — sai (xem §3.1).
- **VÀ CÁI THAY THẾ NÓ CŨNG SAI — lỗi đo thứ SÁU, xem §3c.** Tôi chép khung của phiên #233
  (*"protocol mang HAI con số mà không nói cái nào thắng"*) và chuyển tiếp cho cả người giữ kho lẫn
  chính họ, **mà không đo**. Đo rồi thì `:750-751` nói rõ: *"Hai lượt Codex review… là một stop
  condition **riêng**… được kích hoạt khi chạm trần này **HOẶC** khi PR đã qua ba vòng code/review
  tổng cộng"*, và `:753` giữ **bộ đếm riêng** cho từng trục. Đó là **hai điều kiện dừng ĐỘC LẬP,
  nối bằng HOẶC — cái nào chạm trước thì thắng**. Protocol có nói, và nói rõ.
  **Chỗ lệch THẬT là LIÊN VĂN BẢN, không phải trong protocol:** `ADR-0043` chốt canon **HAI** vòng
  review, còn protocol `:751` kích hoạt checkpoint ở **BA** vòng. Hai con số trên **cùng một trục**,
  ở hai tài liệu, và protocol trỏ ADR-0043 **0 lần**. Ai đọc khung cũ sẽ đi *thay* một trần bằng
  trần kia; việc đúng là **giữ cả hai trục** rồi phân xử con số trên trục VÒNG.
  Cộng dòng 7 trỏ ADR bằng một **phạm vi đã chết** (`ADR-0017 đến ADR-0035`, trong khi có 45 ADR).

## 5. Việc duy nhất còn treo — `PLAT-X8` bản 4

Chờ **#227** land. Đo 05:07Z: **chưa** (master `0` hàm mới · `RC_` = 6 · 39 ca). Đường land là
**PR #234** (`land/227`, head `86788eb4`, mở 04:59Z) — `gate (ubuntu-latest)` **FAILURE**, chết ở
**bước 10 `lease-publish selftest`**, 18 bước sau `skipped`.

**Không vá hộ:** không có lease trên `ops/lease_publish*`, và lease `#227` còn hiệu lực tới
**23-08T01:00Z**. Đó là việc của executor `#227`.

Hẹn `trig_0171iMNPHfQSn58J4VmPm6h1` (06:00Z) mang **tiêu chí đã sửa**: đo hiện vật trên master +
quét **tập PR đang mở** theo NỘI DUNG; **không canh tên nhánh**. Kèm ba đường thoát để không hẹn vô hạn.

Khi #227 land: sáu chỗ phải sửa cho bản 4 nằm sẵn trong **hộp ⛔ ở đầu `ops/specs/plat-x8.md`**.
Kèm gỡ hộp, thêm hàng `4` vào bảng phiên bản, và cập nhật **cả bốn** chỗ trích băm còn sống. **Hai
bảng LỊCH SỬ giữ nguyên băm cũ.** **Trước khi đổi băm — KHÔNG dùng `grep -rl plat-x8 ops/leases/`.** Bản đầu của tệp này ship đúng
lệnh ấy, và cross-review bắt (P1 trên PR #236): nó chỉ quét **cây đang checkout**, tức đúng phép đo mù
mà §7 của chính tệp này gọi tên là nợ `SO-LEASE-KHONG-NAM-MOT-CHO`. Một tệp vừa mô tả cái bẫy vừa
bước vào nó. Lệnh đúng quét **mọi ref**, và **fail-close**:

```bash
git fetch origin '+refs/heads/*:refs/remotes/origin/*' --prune || { echo "KHONG DO DUOC"; exit 1; }
n=0
for r in $(git for-each-ref --format='%(refname)' refs/remotes/origin); do
  git ls-tree -r --name-only "$r" -- ops/leases/ 2>/dev/null | grep -q plat-x8 && { echo "CO LEASE: $r"; n=1; }
done
[ "$n" = 0 ] || exit 1
```

Không fetch được ref nào ⇒ **ĐỎ**. *"Không đo được"* không phải *"không có"*.

### 5b. CẬP NHẬT 05:4x Z — #227 ĐÃ LAND RỒI BỊ REVERT, và điều đó BÁC tiêu chí canh ở §5

Master đi **50 commit** kể từ `3f64167`. Chuỗi thật:

| commit | việc |
|---|---|
| `b88744e` | **merge PR #234** — `#227` LAND |
| — | master `b88744ea` ⇒ `gate(windows-latest)` **ĐỎ 59/68** |
| `7e75156` → `2ab3560` | **PR #237 revert BA TỆP MÃ** của `#227` |

Chín ca đỏ (`t49 t51 t52 t59 t60 t62 t63 t66 t68`) đều là ca **MỚI** của `#227` và **chưa ca nào từng
chạy trên Windows** — `ci.yml` chỉ chạy ubuntu cho PR thường. Cùng một gốc: đồ giả không chạy được
trên Windows ⇒ không log nào được ghi ⇒ `FileNotFoundError` khi đọc `argv.log`.

**Đó đúng là bài học `CLAUDE.md` mà chính `#227` đã chép vào `r6 §chua_do_duoc`** — *"PR xanh không
hàm ý master xanh; lần merge chính là lần đo Windows đầu tiên"* — và vẫn trôi. Đường đúng là gọi tay
`workflow_dispatch` trước khi merge; đã không làm.

Revert **cố ý thu hẹp**: chỉ ba tệp mã (`ops-publish-lease.yml`, `lease_publish.py`,
`lease_publish_test.py`), **giữ toàn bộ hồ sơ** — đo được: 10 verdict + 12 lease `lease-dang` còn trên
master, và ba tệp ấy khớp **byte-identical** với `3f641673`.

> **TIÊU CHÍ CANH Ở §5 ĐÃ HỎNG — đây là lần thứ NĂM cùng họ.** Nó đo *hiện vật hiện tại*
> (`grep -c "^(GOI_GH|def kiem_github|…)"` ⇒ `0` ⇒ "chưa land"). Phép đo ấy **không phân biệt được**
> *chưa từng land* với *land rồi bị revert*. Ngay lúc này nó trả "chưa land" và **tình cờ** dẫn tới
> hành động đúng (chưa viết bản 4), nhưng vì **lý do sai** — và lần sau nó sẽ đọc nhầm mà không ai biết.
>
> **Tiêu chí đúng phải đo LỊCH SỬ, không đo trạng thái:** `git log --oneline <mốc>..origin/master`
> tìm cả commit land LẪN commit revert. Trạng thái hiện tại là một hàm của lịch sử, và hàm ấy
> **không khả nghịch**.

**Hệ quả cho bản 4:** sáu chỗ trong hộp ⛔ giả định `#227` land và nâng bộ test **42 → 58**. Giả định
ấy nay **đã bị hoàn nguyên**. Bộ test lại là **39 `def t` / 42 đạt**. **Đừng viết bản 4** cho tới khi
`#227` land LẦN HAI — và biên bản revert nói rõ lần ấy sẽ được **đo thật trên Windows bằng
`workflow_dispatch` trước khi land**.

**Bệnh đăng trùng lease QUAY LẠI master** cho tới lúc land lại. Ai cấp lease trong khoảng này phải biết.

## 6. Cam kết phạm vi với phiên #233 — GIỮ ĐÚNG

Phiên `session_018YdsqSNdxorwxVYW2d2PkH` (PR #233) đang làm protocol §20 (bảng **định tuyến** ADR, do
máy canh) và `ops/HOAN_THIEN_KE_HOACH_20260822.md`. Tôi đã hồi âm và cam kết **không đụng**:

- `ops/NO_KY_THUAT.md` — họ dùng §13/§14, cố ý chừa §12 cho tôi (đã land ở #230, ráp sạch)
- `docs/PROTOCOL_DA_PHIEN.md`
- `docs/adr/**`

**#233 CHƯA sắp merge:** codex ra 2 P2 chưa vá (`ADR-NNNN` trong khối mã có rào / comment HTML vẫn bị
tính là metadata sống ⇒ `adr-song` trả `rc=0` sai; và regex tên tệp siết hơn văn bản mô tả).

## 7. Còn mở, không ai đang làm

| thứ | trạng thái |
|---|---|
| `PLAT-X8` (#225) | `state:proposed`, **0 lease**. Lease cũ đã cấp rồi **RÚT** (`c7bb945`), chưa từng đăng |
| `PLAT-X6` (#209) | `state:ready`, **0 lease** — sổ nợ `required-status-check` + đảo `t34` |
| `PLAT-X7` (#220) | `proposed`, chưa spec — đo danh tính model, `depends_on: [PLAT-X8]` |
| PR #229 | `ops/HANG_DOI_PACKET.md` — một chỗ duy nhất cho THỨ TỰ packet, chưa merge |
| nợ `SO-LEASE-KHONG-NAM-MOT-CHO` | chưa có lệnh `ai-dang-giu` |
| nợ mục 12 | verdict lượt 3 của X4 **không có hiện vật ở đâu**; và lease lượt 3 khai sai rằng lượt 1+2 *"có verdict trong `ops/reviews/`"* (ở đó có **0** tệp X4) |

**Một manh mối chưa phân định, đừng đọc thành kết luận:** `mergeable_state` của PR #230 đổi
`clean` → `blocked` đúng lúc cổng chuyển `success` → `in_progress`, rồi về `clean` khi cổng xanh lại.
GitHub trả `blocked` khi **branch protection** chặn, `unstable` khi check **không bắt buộc** đang chờ.
Ta nhận `blocked`. Đó là bằng chứng gián tiếp rằng branch protection **có đòi một thứ gì đó** — nếu
thứ ấy là job `gate` thì nó đụng **Q7** (đã trả lời *"KHÔNG BẬT"*) và nợ thường trực `§9`. **Chưa đo
được** vì REST tới `/repos/<kho>` bị proxy chặn 403 từ container này. Cách phân định: so
`mergeable_state` trên một PR **không có review nào** khi cổng đỏ.

---

**Đọc được bản này KHÔNG phải là được giao việc.** Handoff không phải lease (`docs/PROTOCOL_DA_PHIEN.md` §7).
