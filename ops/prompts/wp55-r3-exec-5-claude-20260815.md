# wp55 revision 3 · generation 5 · EXECUTOR `claude` — attempt 2/3

Bạn là **executor**. Ghi trong đúng 6 đường dẫn write_set và không gì khác.
Reviewer kế tiếp bắt buộc là `codex` (§8). Đừng tự review.

---

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại.

```bash
git rev-parse --is-shallow-repository        # ĐÒI false
git remote -v                                # ĐÒI github.com/ducthangho/tra-luat
git config core.abbrev 7

git fetch origin ops/wp55-r3-spec
git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md | sha256sum
#   ĐÒI e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d

git fetch origin claude/wp55-r3g4-f3-03
git rev-parse origin/claude/wp55-r3g4-f3-03
#   ĐÒI e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8   — head XUẤT PHÁT
```

**Đọc `ops/specs/wp55-r3-spec.md` TRỌN VẸN.** Spec là hợp đồng, prompt này chỉ là hướng dẫn
thi hành; lệch nhau thì **spec thắng** và bạn báo chỗ lệch.

Đọc **bản gốc** verdict lượt 6 trên PR #115 (review của `codex` dưới lease
`wp55-r3-review-6-codex-20260814`), không đọc tóm tắt. Nó có probe chạy được cho từng finding.

**Kiểm đường ghi GitHub TRƯỚC khi làm việc.** Bốn lượt liên tiếp bị `403`
(`GitHub access is not enabled for this session`); `git push` thì chạy. Không ghi được thì
**vẫn làm**, ghi handoff vào kho như generation 4 đã làm (`ops/handoffs/**`,
`ops/evidence/**` trên một nhánh `ops/**`) và nói rõ ai cần đăng hộ. Đừng bỏ dở, đừng im lặng.

---

## Nhánh

Tạo **`claude/wp55-r3g5-f3-03`** xuất phát từ `e6e4b73`, mở PR mới nhắm `master`.
PR **#115** giữ nguyên làm hồ sơ generation 4 — **bạn không đóng, không merge**.

Xuất phát từ `e6e4b73` vì bản vá generation 4 đã được cross-review soi và **không bị bác về
hướng**: 18 lớp doctrine và 16 hình dạng lease vẫn đóng, gate vẫn xanh. Việc của lượt này là
**bịt chỗ hở còn lại và chứng minh cho đủ**, không phải làm lại từ đầu.

---

## BẢY finding phải đóng

Verdict lượt 6 nêu **tám**. Finding thứ tám — `ac20-archive-tree-suite-not-self-contained`,
disposition `spec_revision_required` — **KHÔNG thuộc lượt này**: sửa nó là sửa spec, tức đổi
`spec_hash`, tức vô hiệu chính lease của bạn. Chủ kho đã chốt hoãn sang revision 4. **Đừng
đụng vào, và đừng khai là đã xử lý.**

### Bốn P1 — code

**1. `review-transition-bypasses-record-review`** · `packet_loop.py:103-117`

`CHUYEN_HOP_LE["reviewing"] = ("running", "blocked")` cho phép rời `reviewing` bằng
`transition`, không qua `cmd_record_review`. Probe của reviewer qua **public CLI**:

```text
reviewing1_rc=0 · back_to_running_rc=0 · reviewing2_rc=0
state=reviewing · attempts_used=1 · attempt_open=true · reviews=[] · finding_counts={}
```

⇒ lặp review↔fix vô hạn trong **cùng một** attempt, `same_failure_limit` không bao giờ chạm.
Đường ra khỏi `reviewing` phải do **verdict** điều khiển, không do `transition`.

**2. `void-reviewing-accepts-attempt-zero`** · `packet_loop.py:734-755` và `758+`

`void-attempt` giảm `attempts_used` và đóng `attempt_open` nhưng **để nguyên** `state`
= `reviewing` và không xoá `reviewing_head_sha`; `record-review` lại không đòi có lượt đang
mở và số lượt lớn hơn 0:

```text
void-attempt --reason quota      rc=0   attempts_used=0, state=reviewing
begin-attempt --provider claude  rc=8   kẹt cứng
record-review --verdict approve  rc=0   → state=accepted, reviews[0].attempt=0
```

Packet **được duyệt bằng lượt số 0**. AC 8 cho phép trả quota mà không tiêu attempt — nó
KHÔNG cho phép cái này.

**3. `doctrine-html-quoted-angle-bypass`** · `packet_loop.py:269-274`

Regex gỡ tag cấm `<` `>` ở mọi vị trí, kể cả khi nằm **hợp lệ trong dấu nháy** của thuộc tính,
nên tag không bị gỡ:

```text
mer<span title=">">ged:</span> PR đã vào nhánh đích   → rc=0  LỌT
mer<span title="x">ged:</span> PR đã vào nhánh đích   → rc=6  bắt
merged: PR đã vào nhánh đích       (ASCII nền)        → rc=6  bắt
```

Lớp lách **thứ 19**, ngoài danh sách đóng.

**4. `doctrine-common-term-fail-open`** · `packet_loop.py:374-394, 959-962`
— **ĐỌC KỸ NHẤT, đây là cái đắt nhất của lượt trước**

```text
## Người có thẩm quyền     (heading trần)  → rc=0  LỌT
Người có thẩm quyền        (dòng trần)     → rc=0  LỌT
| Người có thẩm quyền |…   (trong bảng)    → rc=6  bắt
```

`_co_ngu_canh_doctrine` — thứ sinh ra ở generation 4 để **thôi bắt oan** câu văn xuôi bị ngắt
dòng — đã **quá tay thành fail-open**: nay chỉ bắt khi cụm nằm trong ô bảng hoặc kèm cụm cùng
nhóm. Nhưng **AC 2 nói thẳng**: bơm *một cụm từ trong danh sách* vào adapter là **phải ĐỎ**.
AC 19 chỉ cho tha **câu văn xuôi kể lại kết quả đo**, không cho tha một heading chép nguyên cụm.

**Bài học ở đây quan trọng hơn bản vá:** chữa một chiều làm hở chiều kia. Lượt này **cấm** sửa
một chiều rồi đo một chiều. Mọi thay đổi trong `_chuan_hoa` / `_co_ngu_canh_doctrine` phải chạy
**cả hai ma trận** (lọt và bắt-oan) trước và sau, và báo **cả bốn** con số.

### Ba P2 — bộ test chưa chứng minh đủ AC

**5. `ac18-mutation-not-per-class`** · `packet_loop_test.py:1089-1094, 1606-1621`

- `nbsp_phu_hai_lop` bị **chủ động loại** khỏi mọi mutant ⇒ lớp đó không có đột biến nào.
- `ha_NFKC_ve_NFC` **không** giết ca ligature, vì `casefold()` độc lập vẫn gấp ligature ⇒ đột
  biến không đo đúng thứ nó tưởng.
- Runner chỉ chạy tập `phai_chet` **do chính mutant khai** ⇒ không chứng minh được các ca
  NGOÀI tập vẫn sống, tức không chứng minh "giết **đúng** ca đó".

⇒ Suite xanh 23/23 vì **tiêu chí tự khai hẹp hơn AC 18**. Sửa: mỗi lớp một đột biến, và runner
phải đo **cả hai** vế — ca đích ĐỎ **và** ca ngoài tập vẫn XANH.

**6. `ac19-false-positive-matrix-incomplete`** · `packet_loop_test.py:1130-1153`

`LOP_LACH` khai 40 lớp nhưng `LOP_BAT_OAN` chỉ có **14** ca, thiếu ca bắt-oan riêng cho các
chốt mới (bỏ nháy cong, gấp mũi tên, xoá HTML comment, tổ hợp dấu / thứ tự chuẩn hoá); ca
được mô tả là `Cf` **không chứa ký tự Cf** nào. Không có **mapping lớp → ca**.

⇒ AC 19 đòi *ít nhất một ca bắt-oan cho mỗi lớp*. Phải có bảng ánh xạ tường minh, và một chốt
làm suite ĐỎ khi có lớp không có ca.

**7. `ac14-codepage-void-attempt-uncovered`** · `packet_loop_test.py:791-817`

Ma trận codepage bỏ sót `void-attempt`, trong khi lệnh đó in stdout tiếng Việt. AC 14 đòi
**MỌI** lệnh con có stdout. Đột biến `bo_cung_hoa_stdout` giết hai ca hiện có **không bù được**
một lệnh chưa nằm trong ma trận.

⇒ Sửa ở **tầng**: sinh ma trận từ **danh sách lệnh con thật** (duyệt parser), đừng liệt kê tay
— liệt kê tay là thứ vừa để lọt `void-attempt`.

---

## Cách làm — thứ tự bắt buộc, giống AC 18 của generation 4

1. **Đo TRƯỚC khi vá.** Chạy cả bốn ma trận trên `e6e4b73` và ghi số nền: lọt · bắt-oan ·
   lease · codepage. Cộng bốn probe của bốn P1 ở trên.
2. **Mở rộng danh sách lớp** cho hai lớp mới lộ ra (quoted-angle-bracket; cụm-đứng-một-mình)
   và soát xem còn lớp nào cùng họ chưa xét — cùng tinh thần "danh sách phải ĐÓNG" của AC 18.
3. **Vá một lượt ở tầng**, không vá theo hình dạng.
4. **Đo LẠI cả bốn ma trận.** Báo tám con số (trước/sau × bốn ma trận).
5. **Không được lùi:** 18 lớp doctrine và 16 hình dạng lease đã đóng ở generation 4 phải vẫn
   đóng. Nếu một bản vá làm lùi bất cứ ca nào, đó là hỏng, không phải đánh đổi.

Mỗi lớp: **một ca phản chứng** + **một đột biến giết đúng ca đó và chỉ ca đó**.

---

## Gate — đọc rc THẬT từng lệnh, `rc` của pipe là `rc` của lệnh CUỐI

```bash
python3 .claude/dev/packet_loop_test.py           # ĐÒI N/N + đủ đột biến
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest                  # ĐÒI hai số BẰNG NHAU
python3 scripts/tl.py doc-claims-check --strict --json     # ĐÒI flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test                 # KHÔNG --write
python3 .githooks/eol_policy.py --all --json      # ĐÒI violations=0
# release-bundle ×2 trên head + ×1 từ fbe5ab9e — ĐÒI cả BA cùng sha256
git diff --name-status fbe5ab9e <head-cua-ban>    # ĐÒI ĐÚNG 6 tệp
```

**AC 20 — đo trên cây ĐÃ MERGE, neo SHA BẤT BIẾN** (đừng dùng `origin/master`):

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7   # hoặc SHA master lúc BẠN đo, ghi rõ
merged=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$merged"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..<head-cua-ban> | git -C "$merged" apply
python3 -B "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"
GIT_DIR="$PWD/.git" python3 -B "$merged/.claude/dev/packet_loop_test.py"
```

`GIT_DIR` là **cách đo hợp lệ đã được reviewer xác nhận** — công thức trong spec thiếu điều
kiện đó, và việc sửa spec **hoãn sang revision 4**. Ghi rõ trong handoff rằng bạn dùng
`GIT_DIR`, đừng khai suông là công thức spec chạy được.

---

## Ranh giới — vượt là dừng

- Ghi **đúng 6 tệp** write_set. Không đụng `RELEASE_MANIFEST.json`, `references/golden/**`,
  `scripts/tl_test_fragments_bundled.py`, `VERSION`, `CHANGELOG`.
- KHÔNG sửa `ops/specs/wp55-r3-spec.md` — đổi băm là vô hiệu lease của chính bạn.
- KHÔNG merge, land, deploy, gọi LIVE, đọc/ghi secrets, force-push, xoá nhánh.
- KHÔNG tự review. KHÔNG tự cấp lease. KHÔNG đóng #54/#55/#92/#115.
- Phát hiện ngoài spec ⇒ xuất successor §7 rồi dừng; không tự mở write set.

## Trần

`attempts_used: 1`, `attempts_limit: 3`. Lượt này là **attempt 2/3**. Còn một lượt dự phòng
sau lượt này — đừng vì thế mà giao dở, nhưng cũng đừng hạ chuẩn vì sợ hết lượt.

Dừng và báo khi: head đổi giữa chừng · lease hết hạn · chạm quota (ghi lý do allowlist,
**không** tiêu attempt nội dung) · phát hiện chính spec revision 3 thiếu ⇒ báo, **không** tự nới.

## Giao nộp

Handoff §7 máy đọc được lên #55, neo `spec_hash e321f811…`, `base_sha fbe5ab9e`, `head_sha`
thật, kèm **bảng tám con số** (bốn ma trận, trước/sau) và bằng chứng cây-đã-merge.

Heartbeat **mỗi 30 phút** lên #55. Ghi được thì ghi; bị `403` thì ghi nhịp vào tệp trong kho
và nói rõ — im lặng không được đọc thành phiên chết, cũng không được đọc thành phiên còn sống.
