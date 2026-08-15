# Packet Spec (DỰ THẢO) — `packet-session-mutex`

**Trạng thái: successor §7 đã xuất, CHƯA được cấp số packet và CHƯA được lease.**
Tệp này là hồ sơ để chủ kho mở packet, không phải giấy phép chạy.

`successor_key: packet-session-mutex` — khoá cục bộ ổn định. Số issue do chủ kho cấp;
phiên soạn KHÔNG tạo được issue (`api.github.com` trả 403 cho cả REST lẫn GraphQL).

Xuất bởi: phiên executor wp55 `wp55-r3-exec-4-claude-20260814`, 2026-08-15 giờ VN.
Nguồn: va chạm THẬT giữa hai phiên cùng chạy wp55 — xem
`ops/handoffs/wp55-VA-CHAM-hai-phien.md` và `…-phu-luc-2.md` trên nhánh
`ops/wp55-r3g4-exec-4-evidence`.

---

## 1 · KHÔNG ĐƯỢC BẮT ĐẦU TRƯỚC KHI wp55 LAND — lý do đo được, không phải thận trọng suông

`write_set` của packet này **giao 2 tệp** với wp55, packet đang MỞ và đang được review:

```text
giao nhau:
  .claude/dev/packet_loop.py
  .claude/dev/packet_loop_test.py
```

wp55 đang ở PR #115, head `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8`, lease review lượt 6
(`wp55-r3-review-6-codex-20260814`) còn hiệu lực tới `2026-08-15T20:00:00Z`.

Chính spec wp55 revision 3 đặt ra bất biến: *"`write_set` GIỮ NGUYÊN 6 tệp — không giao với
packet đang mở nào."* Mở packet này trước khi wp55 land là tự phá bất biến ấy, và hậu quả
không phải merge conflict văn bản mà là **xung khắc ngữ nghĩa**: hai packet cùng sửa
`_kiem_luoc_do_lease` và `CHUYEN_HOP_LE` theo hai hướng, mỗi bên gate xanh trên nhánh mình,
đỏ sau khi merge — đúng hình dạng của finding `merged-tree-doctrine-false-positive` mà
wp55 vừa phải trả giá để học.

**`depends_on: [wp55]` là ràng buộc CỨNG.** Điều kiện khởi động: wp55 đã `landed`.

---

## 2 · Lỗ, ĐÃ ĐO — không phải suy luận

Phép đo chạy được: `ops/evidence/probe-packet-session-mutex.py`, đo trên
`packet_loop.py` tại head wp55 `e6e4b73`.

```bash
python3 ops/evidence/probe-packet-session-mutex.py .claude/dev/packet_loop.py
```

### H1 · hai tiến trình ĐỒNG THỜI cùng mở lượt trên CÙNG state-dir

Lỗ CÓ THẬT nhưng **HIẾM và phụ thuộc tải**. Số đo đầy đủ, kể cả các lần KHÔNG lộ lỗ —
giấu chúng đi là biến một lỗ hiếm thành lời khai mạnh hơn thực tế:

```text
N=8  đồng thời, 12 vòng  → 12/12 vòng: thắng=1, attempts_used=1   (KHÔNG lộ lỗ lần nào)
N=32 đồng thời, 15 vòng  → 13/15 vòng: thắng=1, attempts_used=1
                             2/15 vòng: thắng=2, attempts_used=1   ← LỖ
```

Reproducer mạnh: `ops/evidence/probe-packet-session-mutex-race.py <packet_loop.py> 32 15`.

Chữ ký `thắng=2, attempts_used=1` chỉ khớp một cơ chế: **lost update**. Hai tiến trình cùng
đọc `attempts_used=0`, cùng thấy `attempt_open=False`, cùng ghi `1`. Hai hệ quả:

1. **Hai lượt mở song song trên một packet.** Hai executor cùng tin mình đang giữ lượt.
2. **Đếm THIẾU** — nặng hơn. 2 lượt THẬT chỉ tiêu 1 đơn vị trần ⇒ **trần attempt, lý do
   tồn tại của `packet_loop.py`, bị bào mòn**: chạy được nhiều lượt hơn `attempts_limit`.

`begin-attempt` CÓ chốt `attempt_open`, và chốt ấy ĐÚNG khi gọi tuần tự. Nó thua vì
read-modify-write không nguyên tử: `_load` → kiểm → `_save`, giữa hai đầu không giữ chỗ.

> **CẢNH BÁO cho người viết ca nghiệm thu — chỗ dễ tự lừa nhất của packet này.**
> Ở N=8 lỗ KHÔNG lộ trong 12 vòng liên tiếp. Một ca đua chạy một lần rồi kết luận sẽ XANH
> GIẢ, và xanh giả tệ hơn không có ca. AC 2 vì thế đòi: lặp tới khi quan sát được tranh
> chấp, HOẶC chèn điểm dừng tất định (hook giữa `_load` và `_save`). Ca ấy còn phải tự
> chứng minh không rỗng: trên bản CHƯA vá nó phải ĐỎ ĐƯỢC. Không quan sát được lỗ trên
> bản chưa vá thì ca không đo gì.

### H1b · `packet_loop.py` CHƯA TỒN TẠI trên master — `depends_on` là điều kiện vật lý

```bash
git show origin/master:.claude/dev/packet_loop.py
# fatal: path '.claude/dev/packet_loop.py' ... not in 'origin/master'
```

Không chỉ GIAO write_set với wp55 — **cả hai tệp `.claude/dev/packet_loop*.py` là do wp55
TẠO RA**, chúng chưa có mặt trên `master` (`2531366`). Packet này không sửa được một tệp
chưa tồn tại. `depends_on: [wp55]` vì thế không phải lựa chọn thận trọng mà là điều kiện
vật lý: chạy trước khi wp55 land thì không có gì để sửa.

### H2 · hai phiên KHÁC container — không có state dùng chung nào

```text
phiên A: state='running' attempts_used=1
phiên B: state='running' attempts_used=1
```

Đây không phải điều kiện đua, mà là **vắng mặt hoàn toàn cơ chế loại trừ**.
`.claude/.packet_state` không nằm trong kho, nên mỗi container có một máy trạng thái riêng.
Đây đúng là hình dạng đã xảy ra thật hôm nay: hai phiên cloud cùng chạy wp55, cách nhau 14
giây, không bên nào hỏi được bên kia. Spec wp55 r3 đã ghi nhận ở "Việc chưa làm" #3.

### H3 · lease định danh LƯỢT, không định danh PHIÊN

```text
khoá trong lease    : ['evidence', 'expires_utc', 'granted_by', 'lease_id']
khoá định danh phiên: KHÔNG CÓ
```

Hai phiên cùng cầm một `lease_id` hợp lệ là trạng thái **không phân biệt được** với một
phiên. Không có gì để hỏi "ai đang giữ", nên không có gì để từ chối.

---

## 3 · Hướng chữa ĐỀ XUẤT — không bắt buộc, nhưng đã cân nhắc

Người thực thi tự chọn, miễn qua được AC. Ghi lại đây để khỏi phải nghĩ lại từ đầu:

**`git` chính là primitive compare-and-set sẵn có.** Cả kho đã học một bài lớn: mọi phiên
agent bị 403 ở `api.github.com` nhưng `git push` thì luôn chạy — đó là lý do có
`ops-publish-lease.yml`. Push non-fast-forward bị TỪ CHỐI, và `--force-with-lease` từ chối
khi ref đã dịch. Nghĩa là **một nhánh `ops/state/**` giữ state packet cho ta CAS thật, bền,
và dùng được từ mọi phiên** — không cần API, không cần khoá tệp cục bộ.

Ghép ba lớp, mỗi lớp đóng một H:

| lớp | đóng | cơ chế |
|---|---|---|
| `holder_token` trong state bền | H3 | state khai AI đang giữ, không chỉ lượt nào đang mở |
| state bền trên nhánh `ops/state/**` | H2 | một nguồn sự thật, mọi container đọc chung |
| ghi state bằng CAS (push bị từ chối nếu ref đã dịch) | H1 | mất cuộc đua = push hỏng = biết ngay |

Lớp khoá tệp cục bộ (`O_CREAT\|O_EXCL`) chỉ đóng H1 trong một máy — **không đủ**, vì hình
dạng đã xảy ra thật là H2 (khác container). Đừng dừng ở đó.

### 3.1 · Định danh phiên — KHUYẾN NGHỊ: đừng phụ thuộc nền, hãy tự đúc token

Câu hỏi ban đầu là "`session_id` lấy từ đâu". Đã soát các nguồn nền cung cấp, và **khuyến
nghị là KHÔNG dùng cái nào trong số đó**:

| nguồn | có ở đâu | vì sao không đủ |
|---|---|---|
| `session_01…` của phiên cloud | chỉ phiên cloud | phiên CLI cục bộ và desktop không có |
| `GITHUB_RUN_ID` | chỉ trong Actions | phiên executor không chạy trong Actions |
| hostname + PID | mọi nơi | PID đổi sau mỗi lần nối lại ⇒ phiên nối lại bị coi là phiên khác |

Bất kỳ thiết kế nào neo vào một trong ba nguồn ấy đều **đóng được trên nền này, hở trên nền
kia** — và rồi phải khai "đã đóng" trong khi thực tế nửa vời. Đó đúng là thứ AC 7 của wp55
cấm: *ảo tưởng xác minh tệ hơn không xác minh*.

**Khuyến nghị: token do chính phiên đúc, kèm số rào (fencing) tăng đơn điệu.**

```text
claim:
  1. đọc state bền  → (nội_dung, sha_đã_đọc)
  2. nếu đang có holder còn hạn và token ≠ token của mình ⇒ TỪ CHỐI (mã thoát kiểm soát)
  3. sinh holder_token ngẫu nhiên 128-bit; fence := fence_cũ + 1
  4. ghi state, đẩy bằng CAS neo vào sha_đã_đọc
       git push --force-with-lease=<ref>:<sha_đã_đọc>
     push bị từ chối  ⇒ THUA cuộc đua ⇒ đọc lại, KHÔNG ghi đè
  5. lưu holder_token vào state-dir cục bộ
mọi lệnh đổi trạng thái sau đó: phải trình đúng holder_token VÀ fence ≥ fence đang ghi
```

Ba tính chất, mỗi cái đổi lấy một thứ cụ thể:

- **Không phụ thuộc nền.** Token tự đúc chạy được ở cloud, CLI, desktop, Actions như nhau.
  Không có nền nào bị bỏ lại, nên không phải khai nửa vời.
- **`--force-with-lease` LÀ compare-and-set.** Không cần phát minh giao thức khoá: git đã
  có sẵn, và nó là đường DUY NHẤT mọi phiên agent dùng được khi `api.github.com` trả 403.
- **Số rào đóng lỗ mà HẠN KHÔNG đóng được.** Đây là chỗ dễ bỏ sót nhất: holder A treo
  (container bị đóng băng, GC dài), lease hết hạn, B tiếp quản, rồi A tỉnh dậy và ghi.
  Hạn KHÔNG chặn được cú ghi muộn ấy — chỉ số rào chặn được, vì fence của A đã cũ hơn fence
  đang ghi nên cú ghi bị từ chối. Thiết kế chỉ có hạn mà không có fence là thiết kế còn hở.

**Đường tiếp quản, để không đổi lỗ này lấy lỗ kẹt cứng:** holder hết hạn VÀ không heartbeat
quá ngưỡng ⇒ phiên khác được `takeover` bằng một bản ghi TƯỜNG MINH có lý do, và cú đó bump
fence — vừa cho packet đi tiếp, vừa vô hiệu holder cũ.

**Giới hạn, nói thẳng đừng để ai đọc rộng hơn:** cơ chế này định danh một RUNTIME đang giữ
khoá, KHÔNG định danh con người hay agent. Nó chặn va chạm VÔ Ý — đúng thứ đã xảy ra hôm
nay — chứ không chặn một bên cố ý có quyền ghi kho. Cùng mức trung thực mà
`NGUOI_CO_THAM_QUYEN` đang tự khai: *chứng minh cái TÊN được phép, không chứng minh đúng
người đó đã gõ*. Nếu mất tệp token cục bộ mà container vẫn sống, phiên ấy phải chờ hết hạn
hoặc takeover — không có đường tắt, và đó là chủ ý.

---

## 4 · Spec

```yaml
schema_version: 1
successor_key: packet-session-mutex
packet_id: 119           # ĐỀ XUẤT, chưa reserve được — xem mục 7.1
packet_id_status: provisional
mission_issue: 54
depends_on: [wp55]
depends_on_reason: >-
  write_set giao 2 tệp với wp55 đang mở; chính spec wp55 r3 cấm giao write_set với packet
  đang mở. Điều kiện khởi động: wp55 đã landed.
executor: codex          # §8 — phiên PHÁT HIỆN lỗ là claude, nên đổi nền để có assurance chéo
reviewer_provider: claude
environment: local
risk: normal
attempts_limit: 3

write_set:
  - type: exact
    path: .claude/dev/packet_loop.py
  - type: exact
    path: .claude/dev/packet_loop_test.py
  - type: exact
    path: docs/PROTOCOL_DA_PHIEN.md

objective: >-
  Biến "một packet, một phiên đang chạy" từ QUY ƯỚC thành điều CƯỠNG CHẾ ĐƯỢC. Hiện hai
  phiên cùng mở lượt trên một packet là trạng thái mà máy không phân biệt được với một
  phiên, và tệ hơn: hai lượt song song chỉ tiêu một đơn vị trần, nên trần attempt bị vô hiệu.
```

## 5 · Acceptance criteria

Cùng doctrine đã trả giá ở wp55: **đòi bằng chứng dương, mỗi chốt một phản chứng chạy được,
mỗi phản chứng một đột biến giết đúng nó.**

1. **Danh sách ĐÓNG trước khi vá (kế thừa AC 18 của wp55).** Xuất danh sách các hình dạng
   tranh chấp kèm phép thử đo được TRƯỚC khi sửa mã: đồng thời cùng state-dir; khác
   state-dir; khác container; phiên nối lại sau mất kết nối; lease hết hạn giữa chừng;
   hai phiên trình cùng `holder_token`; holder treo rồi tỉnh dậy ghi muộn sau khi bị
   takeover; state bị sửa tay. Vá một hình dạng mà không có danh sách là KHÔNG ĐẠT.
2. **H1 đóng:** N tiến trình đồng thời gọi `begin-attempt` ⇒ **đúng MỘT** cái `rc=0`, các
   cái còn lại thoát mã có kiểm soát (không traceback). Ca phải lặp tới khi quan sát được
   tranh chấp, hoặc dùng điểm dừng tất định — **không được xanh nhờ may**.
3. **Đếm không mất:** sau N lượt đồng thời, `attempts_used` bằng đúng số lượt THẬT đã mở.
   Phản chứng: ghi đè mù phải bị từ chối, không phải được chấp nhận rồi mất số.
4. **H2 đóng:** state có một bản BỀN dùng chung ngoài container. Phản chứng: hai state-dir
   khác nhau, cùng packet ⇒ cái thứ hai bị từ chối, KHÔNG cùng vào `running`.
5. **H3 đóng:** state bền mang `holder_token`. Lệnh đổi trạng thái không trình đúng token
   thoát mã có kiểm soát. Đột biến: bỏ phép kiểm token ⇒ ca đích ĐỎ.
6. **Số rào (fencing) đóng lỗ mà HẠN không đóng được.** Ca bắt buộc: holder A đọc state,
   bị "treo"; lease hết hạn; B `takeover` (fence tăng); A tỉnh dậy và ghi ⇒ cú ghi của A
   phải bị TỪ CHỐI. Đột biến: bỏ so fence, chỉ giữ kiểm hạn ⇒ ca này phải ĐỎ. Không có ca
   này thì thiết kế mới nhìn giống đã đóng mà thực ra còn hở đúng chỗ khó thấy nhất.
7. **Chiều BẮT OAN, ngang hàng (kế thừa AC 19):** phiên nối lại (CÙNG `holder_token` lưu ở
   state-dir) **KHÔNG** bị chặn; lease còn hạn và đúng holder thì mở lượt bình thường.
   Đường `takeover` phải chạy được để một holder chết không khoá cứng packet. Siết tới mức
   packet kẹt cứng là KHÔNG ĐẠT, y như để lọt.
8. **Đo trên CÂY ĐÃ MERGE với `origin/master` (kế thừa AC 20)**, kèm SHA master lúc đo.
   Chỉ đo trên nhánh là KHÔNG ĐẠT.
9. **`ops-publish-lease.yml` chống trùng theo LƯỢT, không chỉ theo TỆP.** Hôm nay
   `posted_comment_id` chỉ chặn đăng lại CÙNG MỘT tệp; hai tệp lease khác nhau cho cùng
   (packet, revision, role, lượt) vẫn đăng được cả hai — và hôm nay chuyện đó SUÝT xảy ra
   thật. Phản chứng: tệp lease thứ hai cho cùng lượt phải bị TỪ CHỐI.
10. **`docs/PROTOCOL_DA_PHIEN.md` nói rõ bất biến mới** và nói thẳng phần CHƯA đóng —
    đặc biệt: cơ chế này định danh RUNTIME, không định danh người. Không khai rộng hơn
    thứ cưỡng chế được.
11. Full gate xanh, `rc` đọc trực tiếp từng lệnh; `release-verify --strict` 0 failed /
    0 extra; `release-bundle` hai lần cùng SHA-256; không bump VERSION, không cấp rNNN,
    không sửa CHANGELOG.
12. **`file_count` của `RELEASE_MANIFEST.json` KHÔNG đổi** (hiện 179). Đã đo: 0/179 tệp
    thuộc `ops/`, nên `ops/state/**` nằm ngoài gói. Chốt này bắt đúng lúc ai đó định đưa
    state vào cây làm việc thay vì nhánh riêng.

## 6 · Ngoài phạm vi — nêu rõ thay vì im lặng

- **Loại trừ ở tầng điều phối** (dispatcher từ chối cấp hai lease cho một packet): khác
  tầng, và cần bàn ở mức mission. Packet này lo tầng CƯỠNG CHẾ CỤC BỘ + state bền.
- **Bật GitHub App cho org** để phiên agent gọi được API: việc hạ tầng của chủ kho, không
  phải việc của packet. Nhưng nếu bật thì hướng chữa mục 3 vẫn đúng — CAS bằng git không
  phụ thuộc API.
- **Đưa `.claude/.packet_state` vào kho như một tệp thường**: CỐ Ý không đề xuất — state
  đổi mỗi lượt sẽ đẩy `file_count` của `RELEASE_MANIFEST.json` và kéo manifest + golden vào
  write-set, đúng cái bẫy đã hoãn `AGENTS.md` sang F3-08. Dùng nhánh `ops/state/**` riêng
  thì tránh được.

## 7 · Ba câu hỏi — chủ kho ĐÃ QUYẾT, 2026-08-15

### 7.1 · Số packet: **#119** (đề xuất, KHÔNG reserve được)

Chỉ thị: *"lấy số kế tiếp còn trống"*. Đo được:

```text
ref PR cao nhất trên remote            : 118   (git ls-remote 'refs/pull/*/head')
packet có spec/lease THẬT trong kho     : wp55
'wp123' trong docs/runbooks/…ps1        : ví dụ giữ chỗ, KHÔNG phải packet thật
⇒ số kế tiếp còn trống                  : 119
```

**Giới hạn phải nói thẳng:** issue và PR DÙNG CHUNG một bộ đếm trên GitHub, và phiên này
KHÔNG tạo được issue (`api.github.com` 403) nên **không reserve được 119**. Nếu ai đó mở
một PR/issue trước, số thật sẽ trượt. Vì vậy:

- mỏ neo bền của packet này là `successor_key: packet-session-mutex`, KHÔNG phải con số;
- `packet_id: 119` mang `packet_id_status: provisional` — người mở issue điền lại số THẬT
  do GitHub cấp rồi cập nhật đúng một dòng ấy;
- không tệp nào khác trong kho được neo vào số 119 cho tới khi nó được xác nhận.

### 7.2 · `ops/state/**` là hạ tầng ops — ĐÃ XÁC NHẬN, và đã KIỂM

Chỉ thị: *"đúng, không tính vào hạ tầng ops"* ⇒ state nằm ngoài gói release. Không nhận
lời suông, đã đo:

```text
RELEASE_MANIFEST.json : file_count = 179
tệp thuộc ops/        : 0/179
```

Nên nhánh `ops/state/**` không đụng `file_count`, không kéo manifest + golden vào write-set
— tránh đúng cái bẫy đã hoãn `AGENTS.md` sang F3-08. Đã thành **AC 12** để chốt này được
cưỡng chế chứ không chỉ được hứa.

**Còn phải kiểm khi thực thi:** ruleset/branch protection có chặn push vào `ops/**` không.
Chưa đo được từ phiên này (cần API). Nếu chặn, phải mở đúng đường `ops/state/**`, nếu không
toàn bộ lớp CAS mất chỗ đứng.

### 7.3 · Định danh phiên — chủ kho giao cho phiên này đề xuất

Chỉ thị: *"đề xuất cho tôi"*. Khuyến nghị đầy đủ ở **mục 3.1**, tóm tắt:

> **Đừng neo vào bất kỳ `session_id` nào do nền cung cấp.** Phiên cloud có `session_01…`,
> CLI cục bộ và desktop không có, Actions có thứ khác — neo vào cái nào cũng đóng nền này
> hở nền kia rồi phải khai nửa vời. Thay vào đó: **phiên tự đúc `holder_token` ngẫu nhiên,
> ghi vào state bền bằng CAS (`git push --force-with-lease`), kèm số rào tăng đơn điệu.**

Ba điểm quyết định, mỗi điểm đổi lấy một thứ cụ thể: token tự đúc thì mọi nền chạy như
nhau; `--force-with-lease` đã LÀ compare-and-set nên không phải phát minh giao thức khoá;
và số rào đóng đúng cái lỗ mà HẠN không đóng được — holder treo, hết hạn, bị takeover, rồi
tỉnh dậy ghi muộn. Điểm thứ ba là chỗ dễ bỏ sót nhất nên nó thành **AC 6** riêng, có đột
biến giết đúng ca đó.

Giới hạn đã ghi vào AC 10: cơ chế này định danh **runtime đang giữ khoá**, không định danh
con người. Nó chặn va chạm VÔ Ý — đúng thứ đã xảy ra hôm nay — không chặn một bên cố ý có
quyền ghi kho.

## 8 · Việc còn lại trước khi lease được

1. Mở issue (số thật thay cho 119 provisional) — cần quyền GitHub, phiên agent 403.
2. Chờ **wp55 land** — `depends_on` cứng, xem mục 1 và H1b.
3. Kiểm ruleset cho `ops/state/**` (mục 7.2).
4. Cấp lease executor cho `codex` neo spec hash của tệp này sau khi số packet chốt.
