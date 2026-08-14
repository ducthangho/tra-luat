# Packet Spec — wp55 revision 3 (F3-03)

**TỆP NÀY LÀ NGUỒN SỰ THẬT của revision 3.** Comment trên #55 chỉ là bản chiếu.

Kiểm mỏ neo:

```bash
sha256sum ops/specs/wp55-r3-spec.md
```

Con băm ấy **là** `spec_hash` của revision 3. Mọi lease, verdict và evidence §7 của revision
này phải neo đúng con số đó; lệch một byte thì dừng và hỏi, đừng đoán.

## Vì sao mỏ neo đổi từ "băm thân Issue" sang "băm TỆP" — đã đo, không phải tiện tay

Revision 2 khai cơ sở băm là *"SHA-256 của toàn bộ Issue body revision hiện hành sau chuẩn
hoá LF, với giá trị dòng `spec_hash` để trống"*. Cơ sở ấy **không kiểm được từ bất kỳ phiên
agent nào trong kho này**, và nó đã hỏng sẵn:

| đo | kết quả |
|---|---|
| `curl https://api.github.com/repos/ducthangho/tra-luat/issues/55` | **HTTP 403** qua proxy — đã đo 14-08-2026 |
| `gh` CLI trong container | không cài (`docs/GOI_AGENT_DA_NEN.md` đã ghi) |
| đường đọc còn lại | MCP GitHub — trả JSON, **không trả byte thô** |
| thân #55 revision 2 hiện tại | chứa **`&#34;` nguyên văn** ở đúng những chỗ đáng ra là dấu nháy kép |

Dòng cuối là chỗ đau: thân Issue mà công thức đang băm **không phải văn bản tác giả gõ** —
một lớp mã hoá trên đường đăng đã đổi `"` thành `&#34;`. Verdict lượt 4 cũng đã ghi nhận đúng
lớp ấy (*"lớp mã hoá JSON của đường MCP giải mã chuỗi thoát"*).

Nên công thức cũ sinh ra một con băm **không ai xác minh được**, trên một văn bản **đã bị
biến dạng**. Đó đúng là thứ AC 7 của chính packet này cấm: *"ảo tưởng xác minh tệ hơn không
xác minh"*.

Băm một tệp trong kho thì ngược lại: `sha256sum` chạy được ở mọi nền, không cần mạng, không
cần token, và git bảo toàn từng byte. Đây cũng là khuôn `ops/leases/**` đang dùng — *"nguồn
sự thật là tệp, comment chỉ là bản chiếu"*.

**Hệ quả phải nói thẳng:** thân #55 vẫn đang hiển thị revision 2. Tệp này KHÔNG tự sửa được
thân Issue. Việc đồng bộ thân #55 là việc còn lại của chủ kho — xem mục "Việc chưa làm".

---

## Spec

```yaml
schema_version: 1
packet_id: wp55
mission_issue: 54
mission_revision: 6
revision: 3
phase_key: F3-03
spec_path: ops/specs/wp55-r3-spec.md
spec_hash_basis: sha256 của chính tệp này, byte nguyên trạng, không chuẩn hoá gì thêm
supersedes_revision: 2
supersedes_spec_hash: a05c10f71e205d6268c46c62de9fd2d1cc5f7629b070af69a8e3b4254d782c5c

base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
objective: >-
  Giữ nguyên mục tiêu revision 2 — biến vòng lặp executor↔reviewer thành CƠ CHẾ có dấu vết
  bền và có trần cưỡng chế — nhưng đóng ba lớp lỗ mà revision 2 KHÔNG có tiêu chí nào bắt
  được: (a) chuẩn hoá doctrine chọn nhầm dạng chuẩn (NFC không gộp ký tự tương thích);
  (b) hai chốt lease tự kiểm rời nhau nên `begin-attempt` nhận state mà `record-lease`
  không bao giờ sinh ra được; (c) mọi gate chỉ được đo TRÊN NHÁNH, nên một xung khắc chỉ
  hiện sau khi merge với master đi lọt hoàn toàn. Revision 3 đổi TIÊU CHÍ, không vá thêm
  một lượt trên tiêu chí cũ.

write_set:
  - type: exact
    path: .claude/skills/work-packet/SKILL.md
  - type: exact
    path: .claude/skills/cross-review/SKILL.md
  - type: exact
    path: .claude/skills/land-packets/SKILL.md
  - type: exact
    path: .claude/dev/packet_loop.py
  - type: exact
    path: .claude/dev/packet_loop_test.py
  - type: exact
    path: CLAUDE.md

depends_on: []
executor: claude
environment: local
risk: normal

attempts_limit: 3
attempts_used: 0
attempts_note: >-
  Trần đếm lại từ 0 cho revision 3. Revision 2 đã cạn 3/3 và kết ở `blocked` — số cũ
  KHÔNG mang sang, đó là ý nghĩa của việc đi qua revision (§12).

reviewer_provider: codex
reviewer_note: executor là claude ⇒ §8 bắt reviewer khác provider
```

---

## Ba finding P1 khiến revision 2 phải dừng

Cả ba đo trên head `546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f`.

### P1-A · `doctrine-rendering-bypass-nfkc` — chọn nhầm DẠNG CHUẨN HOÁ

`_chuan_hoa` dùng **NFC**. NFC **theo định nghĩa** không đụng tới ký tự tương thích; chỉ
**NFKC** mới gộp. Đây không phải "sót một trường hợp" mà là sai ở lựa chọn dạng chuẩn.

```text
merged： PR đã vào nhánh đích        (hai chấm TOÀN RỘNG U+FF1A)   -> rc=0  LỌT
ｍｅｒｇｅｄ： PR đã vào nhánh đích    (chữ TOÀN RỘNG)                -> rc=0  LỌT
merged: PR đã vào nhánh đích        (ASCII, nền)                  -> rc=6  bắt
```

Tái hiện:

```bash
mkdir -p /tmp/f3/.claude/skills/x
cp .claude/dev/packet_loop.py /tmp/f3/pl.py && cd /tmp/f3
printf 'merged： PR đã vào nhánh đích' > .claude/skills/x/SKILL.md
python3 pl.py doctrine-scan --root .        # rc=0 = còn lọt
```

Nguồn: `chatgpt-codex-connector[bot]` trên PR #92, 2026-08-14T17:27:49Z, neo `546ecf9`.
Đã tái lập độc lập.

**Đây là lớp thứ NĂM liên tiếp của cùng một cơ chế.** Bốn lớp trước: dấu `.` → `==`/`!=`/`!`
→ nháy ngược Markdown → ZWSP + HTML entity. Mỗi lần vá một hình dạng, lần sau lộ hình dạng
mới. Revision 3 vì thế **cấm** cách vá theo hình dạng: xem AC 18.

### P1-B · `partial-lease-authority-bypass` — kiểm SỰ TỒN TẠI một khoá, không kiểm TRỌN LƯỢC ĐỒ

`record-lease` chỉ tạo lease sau khi kiểm `lease_id`, `granted_by`, `evidence`, `expires_utc`.
Nhưng `begin-attempt` chỉ đòi `lease` truthy **và** có `expires_utc`. Nên nó nhận một state
mà `record-lease` **không bao giờ sinh ra được**.

```text
lease = {"expires_utc": "2099-01-01T00:00:00Z"}   -> rc=0  LỌT, mở được lượt
lease thiếu / null / dict rỗng                     -> rc=8  (chặn, đúng)
lease là chuỗi                                     -> rc=1 + TRACEBACK THÔ
expires_utc là số                                  -> rc=1 + TRACEBACK THÔ
expires_utc sai dạng / thiếu múi giờ               -> rc=2
```

Tái hiện — **`--state-dir` là cờ GỐC, phải đứng TRƯỚC lệnh con**; đặt sau sẽ ra
`unrecognized arguments` và bạn sẽ tưởng chốt đang chặn:

```bash
python3 pl.py --state-dir st init --packet 9003 --mission 54 \
    --executor claude --reviewer codex
# sửa st/**.json: state="leased", lease={"expires_utc":"2099-01-01T00:00:00Z"}
python3 pl.py --state-dir st begin-attempt --packet 9003 --provider claude   # rc=0 = còn lọt
```

Nguồn: verdict lượt 5 (`wp55-r2-review-5-codex-20260814`) trên PR #92, 2026-08-14T18:01Z.
Đã tái lập độc lập. Hai traceback thô cho thấy nhánh dữ liệu hỏng **chưa** fail-closed có
kiểm soát — nó chỉ đang vỡ.

**Đây là lớp thứ HAI của cùng một lỗ** (lượt 4: thiếu hẳn `lease` → lượt 5: có `lease` nhưng
dở dang). Cùng bệnh với P1-A: vá theo hình dạng thì hình dạng sau lại lọt.

### P1-C · `merged-tree-doctrine-false-positive` — gate chỉ đo TRÊN NHÁNH

`doctrine-scan` sạch trên nhánh, **đỏ trên cây sau merge với master**:

```text
doctrine-scan trên cây ĐÃ MERGE (origin/master = 3d2c52d)  -> rc=6   CLAUDE.md:82
doctrine-scan trên nhánh 546ecf9 một mình                   -> rc=0   sạch, 4 tệp
git merge-tree fbe5ab9e origin/master 546ecf9               -> rc=0   KHÔNG conflict
```

Tái hiện:

```bash
merged_tmp=$(mktemp -d /tmp/wp55-merged.XXXXXX)
git archive origin/master | tar -x -C "$merged_tmp"
git diff --binary fbe5ab9e..546ecf9 | git -C "$merged_tmp" apply
python3 "$merged_tmp/.claude/dev/packet_loop.py" doctrine-scan --root "$merged_tmp"
```

Nguyên nhân gốc, đã truy tới dòng: `CLAUDE.md` của master ngắt dòng ngay giữa cụm

> …ba tên tấn công `rc=0` → `rc=4`, **người có**
> **thẩm quyền** vẫn `rc=0`…

`_chuan_hoa` chuẩn hoá **cả tệp** nên nó nối hai dòng lại rồi khớp cụm `người có thẩm quyền`.
Câu ấy đang **kể lại một kết quả đo**, không chép doctrine.

Hai điều quan trọng, đừng đọc nhầm:

1. Đây là chiều **BẮT OAN**, ngược với cả bốn vòng doctrine trước (đều là lọt). Một bộ quét
   chỉ được đo một chiều thì chiều kia luôn có chỗ trống.
2. Đây là lỗi **tương thích tích hợp**, không phải merge conflict. `merge-tree` trả `rc=0` và
   vẫn đúng — nó chỉ trả lời "có xung đột văn bản không", nó **không** trả lời "cây sau merge
   còn qua gate không". Revision 2 không có tiêu chí nào hỏi câu thứ hai.

---

## Acceptance criteria

### Giữ nguyên 17 AC của revision 2

Chép nguyên văn từ thân #55 revision 2, **có một sửa đổi duy nhất đã nêu rõ**: chuỗi `&#34;`
được trả về dấu nháy kép `"` (xem mục mỏ neo ở đầu tệp — đó là biến dạng của đường đăng, không
phải chữ tác giả gõ). Không sửa gì khác.

1. Ba adapter đúng tên và đúng phân loại trigger của §13 — `work-packet` và `cross-review`
   model-invoked; `land-packets` KHÔNG tự trigger (`disable-model-invocation: true`).
2. Adapter chỉ chứa cú pháp/công cụ của nền Claude Code và TRỎ về `docs/PROTOCOL_DA_PHIEN.md`.
   Cưỡng chế bằng KIỂM CƠ HỌC, không bằng cảm tính — một danh sách cụm từ doctrine bị cấm
   (tối thiểu: ngưỡng số của stop conditions, tên state machine đầy đủ, bảng vai trò §2, định
   nghĩa merged/integrated/landed/complete) được khai TƯỜNG MINH trong repo, và một lệnh quét
   `.claude/skills/**` thoát khác 0 khi bắt gặp. Phản chứng HAI CHIỀU — bơm một cụm từ trong
   danh sách vào adapter thì kiểm phải ĐỎ; adapter sạch thì XANH. Không có danh sách khai
   tường minh thì tiêu chí này coi như KHÔNG ĐẠT — ba lượt review đã chứng minh đọc bằng mắt
   không có đáy.
3. Trần 3 lượt review↔fix được CƯỠNG CHẾ — lượt thứ 4 thoát mã 3 và state về `blocked`. Phải
   có phản chứng chạy được.
4. Same-failure-limit 2 được CƯỠNG CHẾ THEO ID ỔN ĐỊNH, không theo văn xuôi. Reviewer khai
   `--finding-id SLUG` (slug kebab-case ổn định, ví dụ `url-alias`); máy đếm ID, KHÔNG chuẩn
   hoá và KHÔNG đoán ngữ nghĩa mô tả. `--finding-id` thiếu hoặc sai dạng slug thì lệnh thoát
   khác 0, không tự suy ra từ mô tả. Phản chứng BỐN CHIỀU — (a) cùng ID qua hai review thì
   DỪNG ở lần 2; (b) hai ID khác nhau KHÔNG kích trần; (c) cùng ID lặp TRONG MỘT review chỉ
   tính MỘT lần, không chặn oan ngay lượt đầu; (d) hai mô tả khác nhau CÙNG một ID vẫn tính là
   một finding.
5. Cross-provider được CƯỠNG CHẾ — executor trùng reviewer bị chặn từ `init`; review sai
   provider và executor sai provider đều thoát mã 4.
6. Dừng cứng trước merge/deploy/LIVE/secrets/force-push/xoá branch/xoá worktree/sửa spec packet
   khác — lệnh `guard` chặn MỌI hành vi trong bảng và KHÔNG có cờ nới. Có cờ nới là không có chốt.
7. Mọi transition có dấu vết BỀN — còn comment chưa đăng thì mọi lệnh chuyển trạng thái bị chặn
   (thoát mã 5). Bằng chứng "đã đăng" là **ID comment do GitHub TRẢ VỀ** lúc đăng (id số hoặc
   node id), do phiên Claude ghi lại; KHÔNG xác minh bằng regex trên chuỗi URL. Phản chứng — ID
   bịa/không tồn tại phải bị từ chối; cùng một ID dùng lại cho transition thứ hai phải bị từ
   chối. Nếu packet chọn KHÔNG xác minh được ID thì phải khai tường minh trong adapter rằng đây
   chỉ là SỔ TAY không có bảo đảm, và bỏ mọi câu chữ ngụ ý đã xác minh — ảo tưởng xác minh tệ
   hơn không xác minh.
8. §8 — lỗi quota/rate-limit KHÔNG tiêu thụ attempt nội dung; lý do trả lượt là allowlist,
   không cho lý do tự chế.
9. Suite phản chứng phải TỰ CHỨNG MINH không rỗng — nâng trần 3→99 làm ca trần ĐỎ; nâng
   same-failure 2→99 làm ca same-failure ĐỎ. Báo số cụ thể.
10. Suite chạy CHÍNH entrypoint qua subprocess với `--state-dir` riêng trong Temp, KHÔNG gọi
    hàm nội bộ.
11. `RELEASE_MANIFEST.json`, `references/golden/**`, `scripts/tl_test_fragments_bundled.py`
    KHÔNG đổi, và điều đó phải được CHỨNG MINH BẰNG SỐ (`release-verify --strict` +
    `golden-test` + `release-bundle` ×2 trước/sau), không khai suông.
12. `doc-claims-check --strict` vẫn xanh sau khi thêm con trỏ vào `CLAUDE.md`.
13. Nghiệm thu vòng lặp end-to-end trên TARGET TỔNG HỢP (synthetic), bơm một finding lặp lại
    theo ID để thấy nó DỪNG ở trần. "Có trần trong code" KHÔNG phải nghiệm thu.
14. MỌI lệnh con in được ra stdout ĐÃ BỊ BẮT dưới codepage không phải UTF-8. Phản chứng — chạy
    CHÍNH entrypoint qua subprocess với stdout bị capture và encoding mặc định ép về
    cp1258/cp1252, đòi rc=0 và stdout KHÔNG rỗng cho mọi lệnh in tiếng Việt.
15. `cross-review` có CÚ PHÁP TƯỜNG MINH để ghi verdict lên PR.
16. Full gate xanh với rc THẬT từng lệnh; selftest N/N hai số BẰNG NHAU; `release-verify
    --strict` 0 failed / 0 extra; `release-bundle` hai lần cùng SHA-256.
17. Không bump VERSION, không cấp rNNN, không sửa CHANGELOG, không deploy, không gọi LIVE.

### Bốn AC MỚI của revision 3

**18 · Chuẩn hoá doctrine phải quy về MỘT MỐI, và danh sách lớp ký tự phải ĐÓNG TRƯỚC KHI VÁ.**

`_chuan_hoa` dùng **NFKC** (không phải NFC), lọc ký tự Unicode hạng `Cf`, giải HTML entity
đúng **một** lần, và áp **cả hai vế** so khớp — cụm cấm cũng đi qua đúng hàm ấy.

Trước khi sửa mã, executor phải xuất một **danh sách ĐÓNG** các lớp ký tự có thể hiển thị ra
cụm cấm, tối thiểu phủ: NFKC vs NFC (toàn rộng, ký tự tương thích, chữ số tròn, ligature);
ký tự định dạng (ZWSP/ZWNJ/ZWJ/WORD JOINER/soft hyphen/BOM); HTML entity (thập phân, thập lục,
có tên, thiếu `;`, lồng nhau như `&amp;#58;`); đồng tự Cyrillic/Hy Lạp; nháy cong; biến thể
dash; nhấn mạnh Markdown giữa từ, tag HTML xen giữa, comment HTML, link/anchor, bảng, code
fence; tổ hợp dấu và thứ tự chuẩn hoá.

Mỗi lớp trong danh sách phải có **một ca phản chứng** và **một đột biến giết đúng ca đó**.
Vá một hình dạng mà không có danh sách là KHÔNG ĐẠT — bốn vòng trước đã chứng minh cách ấy
chỉ dời lỗ sang hình dạng kế tiếp.

**19 · Chiều BẮT OAN phải được đo, ngang hàng với chiều lọt.**

Tối thiểu: một cụm doctrine bị **ngắt qua xuống dòng** trong văn xuôi kể lại kết quả đo
KHÔNG được tính là chép doctrine (ca thật: `CLAUDE.md` master dòng 82–83). Chuẩn hoá mạnh
hơn mà bắt oan văn bản bình thường là KHÔNG ĐẠT, y như để lọt.

Suite phải có ít nhất một ca bắt-oan cho **mỗi** lớp chuẩn hoá được thêm ở AC 18.

**20 · Gate phải được đo TRÊN CÂY ĐÃ MERGE với `origin/master`, không chỉ trên nhánh.**

`git merge-tree` trả `rc=0` **KHÔNG** phải bằng chứng tương thích — nó chỉ trả lời có xung
đột văn bản hay không. Bằng chứng giao nộp phải gồm `doctrine-scan` và bộ suite chạy trên
cây dựng bằng `git archive origin/master` + `git diff base..head | git apply`, kèm SHA của
master lúc đo. Chỉ đo trên nhánh là KHÔNG ĐẠT.

**21 · `record-lease` là NGUỒN SỰ THẬT về lược đồ lease; `begin-attempt` dùng CHUNG hàm kiểm.**

Một hàm kiểm duy nhất, kiểm **trọn lược đồ và kiểu**: `lease_id`, `granted_by`, `evidence`,
`expires_utc`. Hai chỗ tự kiểm rời nhau là một đường vòng — đó chính là P1-B.

Mọi hình dạng sai phải trả **mã thoát có kiểm soát**, KHÔNG traceback: `lease` là chuỗi / số
/ mảng / `null` / dict rỗng / thiếu từng khoá; `expires_utc` rỗng / sai dạng / thiếu múi giờ
/ là số / năm 9999 / trước 1970. Phản chứng phải phủ từng hình dạng, và một đột biến tách hai
chốt ra khỏi hàm chung phải làm ca đích ĐỎ.

Chiều bắt oan: một state **hợp lệ** không được bị chặn khiến packet kẹt cứng.

---

## Đổi gì so với revision 2

| | revision 2 | revision 3 |
|---|---|---|
| chuẩn hoá doctrine | NFC + gỡ trang trí + giải entity | **NFKC** + lọc `Cf` + entity, áp **hai vế**; danh sách lớp ký tự phải ĐÓNG trước khi vá (AC 18) |
| chiều đo của doctrine-scan | chỉ đo chiều LỌT | thêm chiều **BẮT OAN**, mỗi lớp một ca (AC 19) |
| phạm vi đo gate | trên nhánh | **trên cây đã merge với master** (AC 20) |
| lược đồ lease | `record-lease` và `begin-attempt` tự kiểm rời nhau | **một hàm kiểm chung**, mọi hình dạng sai có mã thoát (AC 21) |
| cơ sở `spec_hash` | băm thân Issue | băm **tệp trong kho** — xem đầu tệp |
| `attempts_used` | 3/3, cạn | đếm lại **0/3** |

`write_set` GIỮ NGUYÊN 6 tệp — không giao với packet đang mở nào. `depends_on`, `executor`,
`environment`, `risk` giữ nguyên. `base_sha` giữ `fbe5ab9e`.

**Không cần MCR.** Mission #54 không có `plan_hash` và không có `packet_plan` trong code fence,
nên sửa spec packet không đụng hash-material — cùng căn cứ đã dùng cho revision 2.

---

## Ngoài phạm vi — nêu rõ thay vì im lặng

- **`AGENTS.md`** — chuyển F3-08, chủ kho đã chốt hoãn (lý do đo được: đẩy `file_count`
  179→180 hoặc buộc sửa `release.py`, cả hai kéo manifest + golden vào write-set).
- **Wiring suite vào CI** — gộp vào #52, packet đó vốn đã sửa `ci.yml`. Chủ kho đã chốt hoãn.
- **`land-packets` `--apply`** — không thực thi trong packet này.
- **same-provider fallback §8** — câu hỏi mức spec còn treo. Revision 3 **không** cài; muốn có
  thì đi Mission Change Request, không nới trong packet.

## Việc chưa làm, phải nói ra

1. **Thân #55 vẫn hiển thị revision 2.** Tệp này không sửa được thân Issue, và đường ghi khả
   dụng (MCP) đã chứng minh làm biến dạng ký tự — nên tự ý viết đè 15KB văn bản tiếng Việt là
   đổi một lỗi đã biết lấy một lỗi chưa đo. Cần chủ kho đồng bộ, hoặc duyệt cho một lượt viết
   đè có đối chiếu đọc-lại.
2. **Verdict lượt 5 chưa có trong kho.** Bản review trên PR #92 khai lưu tại
   `ops/reviews/wp55-r2-review-5-codex-verdict.md` (sha256 `d1d04452d0ab…`, 4392 byte) — đã
   quét **mọi** ref remote, tệp đó không tồn tại. Mỏ neo xuất xứ của verdict hiện không giải
   được; cần phiên soạn hoặc người đăng hộ push lên một nhánh `ops/**`.
3. **`attempts_used` của revision 2 chưa từng vào máy trạng thái.** `.claude/.packet_state`
   không nằm trong kho — state chỉ sống trong container phiên executor. Con số 3/3 đến từ sổ
   lease, không từ máy. Revision 3 đếm lại từ 0 nên chuyện này không chặn, nhưng nếu muốn máy
   trạng thái là nguồn sự thật thì phải giải quyết ở một packet riêng.
