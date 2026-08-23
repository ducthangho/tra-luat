# Verdict — `PLAT-X8` lượt review 3 (claude, khác phiên soạn đặc tả)

- **packet_issue**: 225 · **PR**: #248 · **branch**: `codex/plat-x8-exec-2`
- **reviewed_sha_required (đã đọc đúng)**: `86a556632f8464de06262efcc2aa7c0e88415f0e`
- **base_sha**: `08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9`
- **lease_id**: `plat-x8-review-3-claude-20260822` (role: reviewer, `nguoi_review_phai_khac_phien: true`)
- **PROMPT.md sha256 đo được**: `3c723c7ac45c63df53886227d7b180ad9bdaddb420d47f8576ed73eec504eebb` — **khớp** `prompt_sha256_required`
- **SPEC-ban5.md sha256 đo được**: `3e49d0ebf14f6f82b13517a4cfd4fc965a41843320367e93628dbc987c53a4bf` — **khớp** `spec_sha256_required`

## VERDICT: `changes_requested`

Tìm được **một P1 thật, chạy được, đã vá-và-test theo đúng yêu cầu lượt này**: bảng `_BANG_LOP`
trong diff chứa **4 mục ngoài phạm vi đặc tả cho phép** — một unauthorized "nới bảng" hạ lớp thật
sự, và một trong bốn mục đó chạm đúng **write_set của chính packet này**. Không tìm thấy lỗ traversal
mới, không tìm thấy lease lịch sử nào bị chốt mới giết (đã quét **toàn bộ 165 ref** trên máy chủ, không
chỉ 4 ref có sẵn cục bộ).

---

## Finding P1 — `_BANG_LOP` seed vượt phạm vi §8:572, hạ lớp 4 đường dẫn thật xuống `systemic`

### Bằng chứng đo được

`docs/PROTOCOL_DA_PHIEN.md` dòng 572 (đếm trực tiếp, `sed -n '565,578p' | cat -n`, dòng 8 của đoạn =
565+7=572) là **đúng và duy nhất** dòng `- \`sensitive\`: workflow/CI authority, security/credential
boundary, dispatcher/reconciler, review/land authority, launcher hoặc gate lifecycle, migration dữ
liệu và LIVE adapter.` Dòng `- \`systemic\`: ...` nằm ở **575**, KHÁC dòng được đặc tả trích dẫn.

Đặc tả (hộp đầu `SPEC-ban5.md`, §4 mục 2, §8) nói thẳng ba lần:
- "`_BANG_LOP` chỉ được seed bằng thứ **§8:572** nói NGUYÊN VĂN: [sáu hạng mục sensitive]"
- "**Không nới bảng phân loại quá thứ §8 nói NGUYÊN VĂN**... nới bảng phải có bằng chứng riêng cho
  từng đường dẫn, và đó là packet khác."
- "**14/14** đường dẫn từng xuất hiện trong `write_set` của mọi lease đều ra **`sensitive`** dưới
  bảng seed ấy — hoặc vì §8 gọi đích danh, hoặc vì rơi vào nhánh mặc định."

Nhưng `_BANG_LOP` trong diff (`ops/lease_publish.py:55-67`) có **4 mục KHÔNG đến từ dòng 572**, đều
gán **`"systemic"`** — một lớp thấp hơn `sensitive`:

```python
    ("docs/PROTOCOL_DA_PHIEN.md", "systemic"),
    ("docs/adr/", "systemic"),
    ("ops/lease_publish_test.py", "systemic"),
    ("ops/chay_lease_publish_test.sh", "systemic"),
```

Đo trực tiếp trên bản sao cả cây (`/tmp/.../rv-copy-review3`, **chưa vá**):

```
$ python3 -c '... lp._tinh_lop_tu_write_set([p]) ...'
ops/lease_publish_test.py      -> systemic   # SAI, phải sensitive
ops/chay_lease_publish_test.sh -> systemic   # SAI, phải sensitive
docs/PROTOCOL_DA_PHIEN.md      -> systemic   # SAI, phải sensitive
docs/adr/0046-foo.md           -> systemic   # SAI, phải sensitive (đã biết — xem "Chồng lấn" dưới)
ops/lease_publish.py           -> sensitive  # đúng
.claude/dev/launcher.py        -> sensitive  # đúng
```

**Hậu quả thật, không phải lý thuyết:** một lease executor tương lai khai `write_set:
['ops/lease_publish_test.py']` (chỉ sửa file test, KHÔNG đụng `ops/lease_publish.py`) sẽ được cổng
này cho phép khai `effective_review_class: systemic` — tức KHÔNG cần Codex `cross_approved`/
`human_audited` (yêu cầu của `sensitive`), chỉ cần review đầu bình thường. Đây đúng là loại lỗ mà
chính đặc tả cảnh báo ở §8: "**Một dòng sai trong bảng là một lớp sai được cổng XÁC NHẬN — tệ hơn
không có cổng**", và đúng gợi ý số 1 của PROMPT lượt này ("Bảng `_BANG_LOP` phân lớp đúng theo
`PROTOCOL §8` chứ?").

**Vì sao 2 lượt review trước không bắt được cả 4 mục:** họ CÓ bắt một trong bốn — PROMPT §4 xác nhận
"Cộng một P2 khai nợ: `docs/adr/` đổi lớp" — nhưng chỉ khai `docs/adr/` thành nợ (chấp nhận, không
vá), KHÔNG lan ra 3 mục còn lại tuy CÙNG một cơ chế sai. `ops/lease_publish_test.py` đặc biệt nghiêm
trọng hơn `docs/adr/` vì nó nằm ngay trong **write_set của chính packet PLAT-X8** — bug tự hạ lớp
đúng công cụ mà cổng này đang dựng ra để KHÔNG bị hạ lớp.

**Vì sao dữ liệu thật chưa lộ bug (giải thích gợi ý #5 của PROMPT — "có ca nào chỉ xanh vì dữ liệu
hiện tại tình cờ hợp lệ?"):** quét **toàn bộ 165 ref máy chủ** (không chỉ 4 ref có sẵn cục bộ — clone
review ban đầu chỉ thấy `master` + 2 nhánh `claude/**`, phải `git fetch origin
'+refs/heads/*:refs/remotes/origin/*'` mới đủ, đúng bẫy "sổ lease không nằm một chỗ" mà `CLAUDE.md`
đã ghi), gom **120 blob lease phân biệt**, lọc `schema_version >= 2` + `role in
{executor,reviewer}`: đúng **6 lease**, **tất cả đều là lease của chính `PLAT-X8`**
(`plat-x8-exec-2…-2r5-codex` ×5, `plat-x8-review-3-claude`). Cả 5 lease executor đều khai
`write_set: ['ops/lease_publish.py', 'ops/lease_publish_test.py']` — LUÔN kèm file đầu tiên (khớp
đúng, "sensitive"), nên `max()` che mất lỗi ở file thứ hai. Không lease thật nào trong lịch sử từng
CHỈ đụng `ops/lease_publish_test.py` một mình — nên bug chưa từng biểu hiện ra dữ liệu thật, dù đã
tồn tại trong code từ commit `67a7fbe0`.

### Vá ở đâu

`ops/lease_publish.py`, định nghĩa hằng `_BANG_LOP` (dòng 55–67 ở exact head `86a55663`, hàm/khối
đứng ngay dưới `_THU_TU_LOP`). Đúng chỗ vì đây là ĐỊNH NGHĨA DỮ LIỆU của cái bảng — không phải logic
tra bảng (`_khop_tien_to`/`_tinh_lop_tu_write_set` đã đúng, xem phần fuzz test bên dưới).

### Vá thế nào

Xoá 4 mục không bắt nguồn từ §8:572 (patch chạy được, đã áp dụng và đo trên bản sao cả cây):

```diff
--- a/ops/lease_publish.py
+++ b/ops/lease_publish.py
@@ -60,10 +60,6 @@
     (".claude/dev/gate_lifecycle.py", "sensitive"),
     ("ops/lease_publish.py", "sensitive"),
     ("scripts/tl_gws.py", "sensitive"),
-    ("docs/PROTOCOL_DA_PHIEN.md", "systemic"),
-    ("docs/adr/", "systemic"),
-    ("ops/lease_publish_test.py", "systemic"),
-    ("ops/chay_lease_publish_test.sh", "systemic"),
 )
```

Không cần đổi logic `_tinh_lop_tu_write_set`/`_kiem_lop_review` — cả hai đã đúng theo fail-closed
default (mục không khớp bảng ⇒ `sensitive`), nên xoá mục khỏi bảng tự động cho kết quả đúng, không
cần nhánh mã mới.

**Có việc CẦN NGƯỜI GIỮ KHO QUYẾT, không phải tôi tự vá:** patch trên đảo ngược quyết định "chấp
nhận nợ" mà 2 lượt review trước đã đưa ra cho riêng `docs/adr/`. Nếu người giữ kho MUỐN giữ
`docs/adr/` ở `systemic` (có lý do riêng, đã cân nhắc), thì patch đúng là chỉ xoá 3 mục
(`docs/PROTOCOL_DA_PHIEN.md`, `ops/lease_publish_test.py`, `ops/chay_lease_publish_test.sh`) và giữ
lại `docs/adr/` — nhưng khi đó phải sửa lại đặc tả §8 (con số "14/14 sensitive" sẽ sai), vì hiện đặc
tả không chừa ngoại lệ nào. Tôi để nguyên cả 4 trong patch đề xuất vì đó là điều spec hiện hành đòi
NGUYÊN VĂN; nói rõ ra đây để executor không tưởng tôi "quên" nợ đã biết.

### Ca test khoá nó + đột biến phải chết

Thêm `t86` (bất biến: MỌI mục `_BANG_LOP` phải map `"sensitive"` — khoá đúng câu spec trích dẫn
nguyên văn dòng 572) và `t87` (ca hẹp, vận hành: 3 đường dẫn cụ thể phải ra `"sensitive"`). Cũng phải
sửa `t77` đã có sẵn trong diff — nó hard-code `"systemic"` làm kỳ vọng cho
`ops/chay_lease_publish_test.sh`, nên tự nó xung đột với patch; sửa lại để test ý định THẬT của A5
(cắt tiền tố `planned:` KHÔNG đổi kết quả) bằng một mục `routine` tạm trong test, không phụ thuộc giá
trị nào của bảng seed thật.

**Đo trên bản sao cả cây, KHÔNG đụng kho thật/nhánh executor** (đúng cấm của lease):

| bước | trạng thái `_BANG_LOP` | lệnh | kết quả |
|---|---|---|---|
| 1. nền, diff-nguyên-văn (chưa thêm test) | như PR #248 | `python3 ops/lease_publish_test.py` | `85/85 đạt; RC=0` |
| 2. thêm `t86`/`t87` + sửa `t77`, CHƯA vá bảng | như PR #248 (bug còn) | `python3 -B ops/lease_publish_test.py` | `ĐỎ t86, ĐỎ t87`; **`85/87 đạt, RC=1`** |
| 3. áp patch (xoá 4 mục) | đã vá | `python3 -B ops/lease_publish_test.py` | **`87/87 đạt, RC=0`** |
| 4. đột biến: khôi phục 4 mục (gỡ patch), giữ test | bug trở lại | `python3 -B ops/lease_publish_test.py` | ĐỎ đúng `t86`+`t87`; **`85/87 đạt, RC=1`** |
| 5. vá lại lần cuối | đã vá | `python3 -B ops/lease_publish_test.py` | **`87/87 đạt, RC=0`** |

`rc` đọc trực tiếp từ `echo $?` ngay sau lệnh, không qua pipe (đúng nếp §5.1 của PROMPT). Bước 2 và 4
là cùng một trạng thái mã nguồn (bug hiện diện) đo ở hai thời điểm khác nhau, cho cùng kết quả `85/87
RC=1` — chính là "đột biến làm ca đích ĐỎ" mà lease đòi.

Ngoài ra đã audit **toàn corpus lease thật** (120 blob, 165 ref máy chủ) chạy `_kiem_lop_review` với
code **đã vá**: 6/6 lease `schema_version>=2` executor/reviewer đều **PASS**, `0 FAIL` — bản vá **không
giết lease lịch sử nào** (trả lời trực tiếp gợi ý #5 của PROMPT bằng số đo, không phải suy luận).

### Bản vá này có thể đẻ ra gì

1. **Không có cổng nào ngăn ai đó thêm lại 4 mục ấy (hoặc mục tương tự) sau này.** `t86` là bằng
   chứng HÀNH VI cho trạng thái hiện tại, nhưng nó chỉ chạy khi có người CHỦ ĐỘNG chạy suite — không
   phải một cổng cấu trúc chặn PR tương lai tự thêm dòng `systemic`/`routine` vào bảng mà không có lập
   luận riêng theo §8. Đây là **nợ**, không phải thứ patch 4-dòng này giải quyết được; ghi lại để
   không đọc nhầm patch là "đã bịt vĩnh viễn".
2. **Đảo ngược quyết định nợ đã có** (`docs/adr/`) mà không hỏi lại người giữ kho có thể gây tranh
   cãi nếu họ có lý do riêng chưa ghi ra hết — xem mục "Có việc CẦN NGƯỜI GIỮ KHO QUYẾT" ở trên. Nếu
   executor áp patch mà không nói rõ điều này trong commit, người review lượt sau sẽ khó phân biệt
   "sửa lỗi" với "âm thầm lật một quyết định đã duyệt".
3. **`t86` là ca giòn theo thiết kế** (bất kỳ mục nào không phải `"sensitive"` đều ĐỎ) — đúng ý định
   hiện tại (bảng seed ban đầu của packet NÀY chỉ được chứa sensitive), nhưng nếu một packet SAU này
   được người giữ kho duyệt nới bảng thật (đúng quy trình §8 mô tả), `t86` sẽ ĐỎ và người vá phải nhớ
   sửa/xoá nó có chủ đích — không phải bug, nhưng cần ghi chú tại chỗ khi nới bảng thật xảy ra.

---

## Các hướng đã soi nhưng KHÔNG tìm thấy vấn đề mới (nói thẳng, theo yêu cầu §6 PROMPT)

- **Traversal/normalize**: chạy fuzz 11 input đối kháng (`ops/lease_publish.py/../lease_publish.py`,
  `ops//lease_publish.py`, hoa/thường, dấu chấm ở giữa, NUL byte, `planned:planned:`, chuỗi rỗng, hai
  cấp `..`…) — **tất cả đều fail-closed về `sensitive`**, không mục nào lọt xuống tier thấp hơn. Logic
  `_khop_tien_to`/`_tinh_lop_tu_write_set` đúng; round 1 đã vá traversal tốt, không có hồi quy.
- **Lease lịch sử bị chốt mới giết**: đã trả lời bằng số ở finding trên — `0/6` lease thật (toàn bộ
  165 ref) bị vỡ bởi `_kiem_lop_review` sau khi vá.
- **Ba trạng thái có/không/không đo được**: soi nhánh `schema_version < 2` với `leased_at_utc` không
  parse được (`except ValueError: pass`) — im lặng bỏ qua CẢNH BÁO (không phải chốt `rc`), khớp đúng
  spec §5 mục 7 ("in CẢNH BÁO, KHÔNG đổi rc") nên KHÔNG phải một trạng thái thứ ba bị nuốt thành
  "không" theo nghĩa nguy hiểm — nó chỉ là best-effort logging, `rc` không phụ thuộc nó.
- **`write_set` rỗng/thiếu cho executor**: đã xác nhận `_tinh_lop_tu_write_set` fail-closed đúng
  (`sensitive`) qua A6/`t78`; "đòi write_set không rỗng" ở §5 mục 5 của đặc tả là diễn giải lại đúng
  hành vi của mục 3, không phải một chốt riêng còn thiếu.
- **Không tìm chốt nào được "khai mà không tồn tại" NGOÀI những cái đã biết**
  (`CONG-KHONG-KIEM-MO-NEO-DAC-TA` trong lease, `ADR-0045` preflight thủ công trong spec) — nhưng
  chính docstring của `_BANG_LOP` trong diff ("chỉ những đường mà Protocol §8 gọi tên đủ để phân
  lớp") là một VÍ DỤ MỚI đúng hình dạng này: lời khai trong comment KHÔNG khớp bảng thật — xem
  finding P1, cùng một bug, hai cách nhìn.

## Giới hạn của chính lượt review này — khai thẳng

1. **Không đạt `cross_approved` theo đúng nghĩa danh tính kép.** Lease `assurance_ghi_chu` nói rõ:
   biên nhận phải có receipt ID + hai danh tính chứng thực ĐỘC LẬP; lượt này đăng verdict qua tệp +
   (nếu executor/dispatcher đăng hộ) comment dưới tài khoản khác reviewer, nên danh tính thứ hai vẫn
   **thiếu**. Khai đúng: mức đạt được là **cross-provider review có bằng chứng chạy được** (claude
   review codex, khác nền, khác lease), KHÔNG phải `cross_approved` đầy đủ theo receipt v2.
2. **Không xin được GitHub MCP để đọc lại text đúng nguyên văn của P2 "docs/adr/ đổi lớp" ở 2 lượt
   trước** (`mcp__github__pull_request_read` bị từ chối quyền trong phiên này, không ai duyệt kịp).
   Suy luận về phạm vi debt đó dựa trên câu tóm tắt trong `PROMPT.md` mục 4, không phải đọc trực tiếp
   comment gốc trên PR #248 — nếu bản gốc thực ra đã liệt kê cả 4 mục (không chỉ `docs/adr/`) thì
   phần "vì sao 2 lượt trước không bắt được cả 4 mục" ở trên cần sửa lại; bản chất bug và patch không
   đổi.
3. **Không chạy `actionlint`/A11, A12 (CI Windows exact-head)** — ngoài phạm vi write_set của lượt
   review này (không có gì trong diff đụng `.github/workflows/`), và không có quyền `workflow_dispatch`
   từ vai trò reviewer read-only.
4. **`t82` (đột biến A1–A8 tự thân trong diff)** — đã đọc, không chạy lại toàn bộ (không phải trọng
   tâm; không có gì trong diff cho thấy A1–A8 sai) — chỉ xác nhận bằng mắt kỹ thuật cô lập (tên tệp
   mutant riêng, `sys.dont_write_bytecode`, `invalidate_caches`) đúng nếp `A10`/`t82` đòi.
5. **Không đo lại `t23`** theo đúng nghĩa nó tự nhận (neo băm prompt) — xác nhận nó KHÔNG liên quan gì
   tới chốt lớp mới, nên "N/N" của nó không phải bằng chứng cho finding P1; đây là điều tôi tự đo
   thêm (mục "audit toàn corpus" ở trên), không phải thứ `t23` sẵn có cung cấp.

## Việc executor cần làm

1. Áp patch `ops/lease_publish.py` (xoá 4 mục, hoặc 3 mục nếu người giữ kho quyết giữ `docs/adr/` —
   khi đó phải sửa lại con số "14/14" trong đặc tả).
2. Thêm `t86`, `t87`, sửa `t77` vào `ops/lease_publish_test.py` (patch đầy đủ ở trên).
3. Chạy `python3 ops/lease_publish_test.py`, xác nhận `N/N` với N tăng đúng 2 so với hiện tại, `rc=0`.
4. Cập nhật commit message/CHANGELOG nêu rõ đây là sửa một lỗi "nới bảng ngoài §8:572", không phải
   một cải tiến — và nói rõ quyết định về `docs/adr/` (giữ nợ cũ hay đóng nợ luôn) theo mục 1.
