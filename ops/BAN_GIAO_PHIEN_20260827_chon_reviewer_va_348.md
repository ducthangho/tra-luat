# BÀN GIAO PHIÊN — 27-08-2026, packet #348 (PR #349) và #351 (PR #354)

Phiên gốc: `session_01TSF9Nsd46t1QXvD8pF3UMW`. Tệp này là **con trỏ + trạng thái**, không
định nghĩa lại luật nào — luật ở `docs/PROTOCOL_DA_PHIEN.md`, adapter ở `.claude/skills/**`.

**Đọc câu này trước:** phiên gốc bị đóng vì hết dung lượng ngữ cảnh, **không** vì việc hỏng.
Hai packet đều đang ở trạng thái sạch và đo được. Không có việc nào đang dở dang giữa chừng.

---

## 0. Chủ kho đã ra lệnh gì (giữ nguyên hiệu lực)

- **Executor = `codex`, effort `xhigh`.** Reviewer = `claude`, chọn bậc từ `claude-opus-5 high`
  tới `claude-fable-5 max` **tuỳ độ phức tạp**. Đây là phân vai MỚI (mọi lease trước đảo chiều).
- Uỷ quyền rộng: *"nội dung nào cần tốt thì tôi uỷ quyền bạn làm theo khuyến nghị bạn thấy tốt nhất"*.
- **Chủ kho TỰ dọn nhánh cũ** bằng script riêng của họ. Phiên KHÔNG dọn. (Script ấy không có
  trong container — đã tìm cả `.claude/skills/` trong kho lẫn `~/.claude/skills/`.)
- Merge: mọi lần merge trong phiên gốc đều do chủ kho uỷ quyền MỘT LẦN, và **không lần nào là
  tiền lệ**. `packet_loop.py guard --action merge` vẫn chặn vai executor (`rc=7`).

---

## 1. Packet #348 — PR #349, `claude/tach-danh-tinh-github-exec-1`

**Trạng thái: CHỜ VERDICT.** head `4573b0b` · base `f715fc2` · 5 tệp · CI xanh trên `0268825`
(head trước), **chưa đo CI trên `4573b0b`** — việc đầu tiên của phiên mới.

Lease: `tach-danh-tinh-github-exec-1r2-claude-20260827` (nhánh `ops/cap-lease-tach-danh-tinh-20260827`).

### Đang chạy khi bàn giao
Một lượt cross-review `claude-fable-5 --effort max` neo `4573b0b`:

```
run.json : <scratchpad>/rv349-f5/run/c545dcc5/run.json
verdict  : <scratchpad>/rv349-f5/VERDICT.md      (chua co luc ban giao)
ket qua  : <scratchpad>/rv349-f5/ket-qua.json    (de kiem modelUsage)
```

**Scratchpad MẤT theo container.** Nếu phiên mới không thấy hai tệp ấy thì lượt review coi như
KHÔNG CHẠY — phóng lại, đừng đoán kết quả.

### PHẢI KIỂM `modelUsage` TRƯỚC KHI TIN VERDICT — đây là bài học đắt nhất của phiên

Lượt review trước đó yêu cầu `claude-fable-5 --effort max` và trả:

```
rc = 0    subtype = success    is_error = false
modelUsage = ['claude-haiku-4-5-20251001', 'claude-opus-4-8']
```

Mô hình phục vụ THẬT là `claude-opus-4-8`. Chạy 1964 giây, tốn ~$11. **Ba tín hiệu `rc`,
`subtype`, `is_error` đều báo thành công.** Chỉ phép kiểm *"mô hình đã yêu cầu phải có mặt làm
KHOÁ trong `modelUsage`"* bắt được.

Ba lớp kiểm, dùng cả ba:

1. **Probe TRƯỚC khi phóng** (rẻ): gọi `claude --model <id> --output-format json -p 'OK'` vài
   lần, đòi `<id>` có trong `modelUsage`. Bắt cú tụt trong vài giây thay vì sau 30 phút.
2. **Kiểm SAU khi xong**: `<id>` phải có trong `modelUsage`.
3. **Kiểm mô hình LẠ** (chặt hơn (2), và (2) không thay được): một lượt DÀI có thể tụt GIỮA
   CHỪNG, khi ấy `modelUsage` mang **cả hai** — đủ qua (2) nhưng không đủ gọi là review của
   `<id>`. Loại `claude-haiku-*` (mô hình phụ của harness, có ở mọi lượt), rồi đòi **không còn
   mô hình nào khác**.

Verdict của lượt tụt được ghi nhận **VÔ HIỆU VỀ DANH TÍNH NGƯỜI REVIEW**, nhưng **nội dung vẫn
đứng**: 3 finding của nó có bằng chứng chạy được và phiên gốc đã tái hiện độc lập.

### Lịch sử review đã xong

- **Lượt 1** (codex xhigh): `changes_requested`, 7 finding (5 P1). **Đã đóng cả 7**, xác nhận
  bởi lượt 2.
- **Lượt 2** (claude, danh tính vô hiệu): `changes_requested`, 3 finding F1/F2/F3. **Đã đóng cả 3.**
- **Lượt 2 chạy lại** (fable-5 max): đang chạy khi bàn giao.

### Năm chỗ cùng MỘT hình dạng — đếm hình dạng, đừng chỉ đếm lỗi

Packet này gặp *"danh sách cấm đội lốt allow-list"* **năm lần**:

| # | chỗ | ai bắt |
|---|---|---|
| 1 | `if:` kiểm bằng chuỗi (`\|\| always()` lọt) | cross-review lượt 1 |
| 2 | `permissions` chỉ đọc mức workflow (job ghi đè được) | cross-review lượt 1 |
| 3 | `run` cấm `pip`/`npm` (bước `git` kéo head PR lọt) | cross-review lượt 1 |
| 4 | `with_khoa` = "khoá phải có" thay vì "khoá được phép" (`repository:`, `token:` lọt) | một lượt review ĐÃ CHẾT, đọc từ `stderr` |
| 5 | khoá job `cong` mà không khoá TẬP JOB (job `evil` lọt) | cross-review lượt 2 |

Chỗ 4 đáng kể riêng: lượt review ấy **chết** vì bộ lọc nội dung của nền ở giây 793, không để
lại verdict — nhưng `stderr.log` giữ lại thứ nó **đang đột biến lúc bị giết**. Đọc log của một
lượt chết vẫn ra finding thật.

### Số đo cuối (head `4573b0b`, có `actionlint` 1.7.7 + `shellcheck` 0.10.0 trên PATH)

```
bo phan chung : 31 ca · 35 dot bien · giet DUNG va CHI DUNG tap khai · TONG: DAT
doctrine-scan rc=0 · adr-song rc=0 · doc-claims rc=0 · workflow-audit rc=0
release-verify rc=0 (180/180) · lease_publish 114/114 · idiom_py_test DAT
actionlint rc=1 — DUNG 1 finding `ops-don-ref.yml:106 SC1003:info`, DO SAN tren master, DELTA=0
```

---

## 2. Packet #351 — PR #354, `codex/chon-reviewer-exec-1`

**Trạng thái: ĐÃ ĐẨY, ĐÃ MỞ PR, CHƯA CROSS-REVIEW.** head `236b19a` · 3 tệp / 518 dòng.

Lease: `chon-reviewer-exec-1r4-codex-20260827` (revision 4) · đặc tả đóng băng
`ops/specs/CHON-REVIEWER-THEO-DO-PHUC-TAP.md` sha256 `0e27149d97b9…`.

**PR mở SỚM có chủ đích**: hiện vật codex nằm trong một clone ở scratchpad, sẽ mất theo
container. Đẩy trước, review sau — và PR khai thẳng là chưa review.

### Việc tiếp theo cho packet này
Cross-review bằng `claude`. Bậc theo chính bảng của packet: `sensitive` +2 · vùng `giao-thuc`
(`.claude/skills/`) +1 · vùng `dev` +0 · 3 tệp · 518 dòng ⇒ **điểm 3 ⇒ `claude-fable-5 / xhigh`**.
(Tự tính lại, đừng chép — bảng nằm trong `.claude/dev/chon_reviewer.py` của chính PR ấy.)

### Bốn lượt executor, BA lần ĐẶC TẢ SAI — và hai lần cùng một gốc

| lượt | kết quả | vì sao có lượt sau |
|---|---|---|
| r1 | dừng ở phút ~12 | đặc tả đòi `modelUsage` **đúng một khoá** |
| r2 | 7 ca · 7 đột biến ĐẠT | đặc tả không đòi validate đầu vào |
| r3 | 10 ca · 10 đột biến ĐẠT | allow-list `review_class` là **từ vựng bịa** |
| r4 | **12 ca · 12 đột biến ĐẠT** | — |

**Gốc chung của r1 và r3: viết luật TRƯỚC khi đo miền giá trị.** Cả hai hỏng theo hướng
**fail-CLOSED** — công cụ từ chối đầu vào hợp lệ — nên chúng không lộ ra như một lỗ mà lộ ra
như một công cụ không dùng được. Cả bốn lượt codex cài **đúng** thứ được giao.

Số đếm bác luật r3 (đếm trên tệp lease của **mọi** nhánh `ops/**`):

```
review_class: sensitive 570 · systemic 167 · routine 22 · thuong 0   <- tu vung bia ra
effective_review_class: 147                                          <- lop SAU escalation
```

**Luật thực hành:** đặc tả nêu một TẬP GIÁ TRỊ HỮU HẠN thì phải **ĐẾM nó trong kho trước** và
dán số đếm vào đặc tả. **Allow-list không kèm số đếm là allow-list chưa đo.**

### Ba lỗ fail-open của `claude` CLI 2.1.207+ (đo 27-08, còn hiệu lực)

- `--effort` sai ⇒ cảnh báo rồi **im lặng** lùi về mặc định.
- `--model` sai ⇒ **`rc=0`**, `subtype=success`, nhưng `is_error=true` và `modelUsage` thiếu
  mô hình yêu cầu.
- `--dangerously-skip-permissions` **BỊ TỪ CHỐI dưới root** (`rc=1` sau `1.151s`); container
  chạy root ⇒ reviewer headless phải đi bằng `--allowedTools` + `--permission-mode`. Thiếu hai
  cờ ấy thì phiên chạy nhưng **không gọi nổi công cụ nào** — một lượt review không đo được gì.

---

## 3. Nợ có tên — chưa ai đóng

- **`AG-T0-01B-thu-hoi-lease-chua-co-duong`.** Không có lệnh thu hồi lease. `lease_publish.py`
  chỉ có `check · body · kiem-github · mark · ai-dang-giu · con-tro-treo`. Phiên này đụng nó
  **hai lần trong một ngày**: `ci.yml` (lease #345 đã land) và
  `.claude/skills/cross-review/SKILL.md` (lease #337 + #325 **đều đã land** — đo bằng
  `git merge-base --is-ancestor`, `2d1c074` và `210ff79` đều là tổ tiên của `origin/master`).
  Hai lần cùng một hình dạng thì câu hỏi đúng không còn là *"lách thế nào"*.
- **`ngu-nghia-trigger-chua-do-bang-PR-doi-khang`** (#348). Tầng (B) đo HÌNH DẠNG tệp, không đo
  ngữ nghĩa trigger của GitHub. Bước 0.2 và N1–N6 của
  `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` là chỗ đo thật, và chúng đòi **một người có vai admin
  trước trình duyệt** — phiên không chạy hộ được.
- **Chưa ghi vào `CLAUDE.md`**: bài học *"viết luật trước khi đo miền giá trị"* (§2 trên) và
  *"kiểm `modelUsage`, đừng tin `rc`"* (§1 trên). `CLAUDE.md` đo được **NGƯỜI_GIỮ 0**, viết
  được — nhưng cần một packet + lease riêng, phiên gốc hết ngữ cảnh trước khi mở.

---

## 4. Dọn nhánh — đo được, và chủ kho tự làm

Không tự chạy. Bốn ràng buộc đã đo, để chủ kho đối chiếu script của họ:

1. `.github/workflows/ops-don-ref.yml:197` **từ chối thẳng** `ops/*|claude/*|codex/*|agent/*|mission/*|dispatcher/*`
   với `exit 2` — chặn **222/229** nhánh.
2. **129 tệp lease chỉ tồn tại trên nhánh `ops/**`** (master có 74, hợp trên nhánh ops là 203).
   Xoá nhánh `ops/**` làm `ai-dang-giu` mù đúng chỗ lease mới nhất nằm. *(Số đếm này TRÔI —
   lần đo trước là 128. Đo lại, đừng chép.)*
3. `luu-tru/*` là ref BỀN giữ commit verdict; xoá là làm `published_*` thành SHA không tra được.
4. *Đẩy xoá ref từ phiên có được phép không* = **KHÔNG ĐO ĐƯỢC**. Phép thử bằng một ref không
   tồn tại lỗi ở **phía client** (git tra danh sách ref trước khi gửi), nên nó không chứng minh
   gì. Đừng đọc nó thành "xoá được".

---

## 5. Việc đầu tiên của phiên mới, theo thứ tự

```
1. python3 .claude/dev/launcher.py doctor        # va `chuan-bi` neu codex chua xac thuc
2. Do CI tren PR #349 head 4573b0b               # chua tung do
3. Tim <scratchpad>/rv349-f5/VERDICT.md
   · CO   -> kiem modelUsage (3 lop o §1) TRUOC khi doc verdict
   · KHONG-> phong lai fable-5 max, neo dung head hien tai
4. Cross-review PR #354 (#351) bang claude, bac tu tinh lai
5. Chi merge khi: verdict `approve` NEO DUNG head cuoi + CI xanh + chu kho duyet
```

**Trước MỌI lần quét lease:** so hai nguồn bằng **TẬP TÊN** (`ls-remote --heads` ↔
`for-each-ref`, `comm` hai chiều), rồi mới `ai-dang-giu`. `rc=12` là **KHÔNG XÁC ĐỊNH**, KHÔNG
phải *"không ai giữ"* — chữa nhánh rồi quét lại.

**Công cụ phải tự cài, không có sẵn:** `actionlint` 1.7.7 và `shellcheck` 0.10.0 (tải từ
release page). Thiếu chúng thì `lease_publish_test.py` cho `95/114` thay vì `114/114`, và
`actionlint` **im lặng bỏ toàn bộ luật nền shellcheck** rồi vẫn trả `rc=0`.
