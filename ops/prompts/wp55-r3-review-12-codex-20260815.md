# wp55 revision 3 · CROSS-REVIEW lượt 12 — reviewer `codex` — nhánh VÁ RIÊNG `5ec8fab`

Bạn là **reviewer độc lập**. Vai này **CHỈ ĐỌC**: không sửa tệp, không commit, không push,
không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

§8 đòi reviewer khác provider với executor. Người viết bản vá là `claude` ⇒ reviewer phải
là `codex`. Không phải `codex` thì **DỪNG** và báo lại.

---

## Đây KHÔNG phải head của PR #120 — đọc kỹ đoạn này

Nhánh cần soi là `ops/wp55-r3-fix-html-table-token`, head `5ec8fabfded6adcfb8b7288ac7846f92267e165e`,
rẽ từ đúng head mà lượt 11 đã soi (`4085bbf22d565a4189977f0504dfd8e5f748bfce`).

Head của PR #120 **vẫn là `4085bbf`** và **cố ý không đổi**: lượt 11 vừa soi đúng head đó,
và ba lượt liên tiếp trước đã bị head bỏ lại phía sau. Bản vá này nằm riêng để chủ kho
quyết có đưa vào revision 3 hay để sang revision 4.

```bash
git rev-parse --is-shallow-repository       # ĐÒI false
git config core.abbrev 7
git fetch origin ops/wp55-r3-fix-html-table-token
git rev-parse origin/ops/wp55-r3-fix-html-table-token
#   ĐÒI 5ec8fabfded6adcfb8b7288ac7846f92267e165e
git diff --name-status 4085bbf22d565a4189977f0504dfd8e5f748bfce 5ec8fabfded6adcfb8b7288ac7846f92267e165e
#   ĐÒI ĐÚNG 2 tệp: .claude/dev/packet_loop.py · .claude/dev/packet_loop_test.py
sha256sum ops/prompts/wp55-r3-review-12-codex-20260815.md   # ĐÒI khớp prompt_sha256_required
```

**KIỂM ĐƯỜNG GIAO VERDICT TRƯỚC KHI LÀM VIỆC.** Đã đo 15-08-2026 trong container điều
phối: REST thẳng tới `api.github.com` bị **proxy** trả 403 (`GitHub access is not enabled
for this session`) **bất kể token**, và `gh` không cài. `git push` thì chạy. Không ghi được
lên GitHub thì **vẫn review**, ghi verdict ra tệp theo mục *Giao kết quả* và nói rõ ngay ở
đầu báo cáo.

---

## Việc cần làm

### 1. Bản vá có bịt đúng thứ nó khai không

Finding `doctrine-html-table-token-context-bypass` (lượt 10, tái lập nguyên trạng ở lượt
11). Bản gốc verdict lượt 11: `ops/reviews/wp55-r3-review-11-codex-verdict.md` trên nhánh
`ops/wp55-r3-review-11-verdict`. **Đọc bản gốc, đừng đọc tóm tắt.**

Hai hàm mới trong `packet_loop.py`, chạy trước lúc đếm mốc bảng:

- `_xoa_gia_tri_thuoc_tinh` — duyệt KÝ TỰ, xoá trắng giá trị thuộc tính có nháy nằm trong thẻ.
- `_xoa_phan_tu_raw_text` — xoá trắng nội dung `script`/`style`/`textarea`.

Người vá đo được (chạy lại đi, đừng chép):

| ca | `4085bbf` | bản vá |
|---|---|---|
| `closer-in-script` | `rc=0` | `rc=6` |
| `closer-in-attribute` | `rc=0` | `rc=6` |
| `opener-in-script` (bắt oan) | `rc=6` | `rc=0` |
| ba đối chứng khác đúng một biến | `6/6/0` | `6/6/0` |

### 2. Trục đáng dồn sức — bản vá này có phải cú đánh quá thứ BẢY không

Chính bạn (lượt 11) kết luận: **AC 19 không cưỡng chế được bằng máy vừa sound vừa
complete**, và vá thêm heuristic thì tiếp tục tạo lách/bắt oan.

Người vá lập luận rằng finding NÀY khác: nó về **dò cấu trúc HTML** (token là markup hay
là dữ liệu) — một câu hỏi cơ học, hữu hạn, **không** phải phân loại ngữ nghĩa như miễn trừ
AC 19. Vì thế vá nó không phải nới AC 19.

**Phán định thẳng lập luận đó.** Nếu bạn thấy nó vẫn là cùng một con lắc, nói rõ — `changes_requested`
hoặc `blocked` là verdict hợp lệ và có giá trị hơn một cái gật.

### 3. Soi kỹ chỗ CỐ Ý LỆCH CHUẨN HTML

`_xoa_phan_tu_raw_text` **không xoá gì** khi thẻ raw-text thiếu thẻ đóng. Chuẩn HTML nói
`<script` cụt chạy tới hết tệp. Lập luận của người vá: làm theo chuẩn sẽ xoá trắng phần
đuôi tệp, `</table>` thật trong đó biến mất, bảng tụt về luật dòng trống, và cụm cấm dưới
dòng trống được tha — tức mở đúng một đường giấu doctrine sau một thẻ `<script` cụt.

Hai chốt bó theo hai hướng khác nhau (một SIẾT, một NỚI). **Kiểm xem lập luận bất đối xứng
đó có đứng vững không**, và có đường lách nào khác mở ra vì nó không.

Đã có đột biến khoá chỗ này: `raw_text_khong_dong_the_nuot_toi_het_tep`.

### 4. Tìm cái bản vá chưa nghĩ tới

Gợi ý những chỗ người vá tự thấy mỏng, đừng giới hạn ở đây:

- Duyệt ký tự coi `<` + chữ cái là mở thẻ, kể cả trong văn xuôi (`a <b "x" c>`). Có bắt oan thật không?
- Nháy KHÔNG đóng ⇒ trả nguyên chuỗi, huỷ cả phần đã xoá đúng. Có đường lách không?
- Danh sách raw-text đóng ở ba tên. `title` thì sao? CDATA? SVG `foreignObject`?
- `_RE_RAW_TEXT_MO` là regex `<(script|style|textarea)\b[^>]*>` chạy SAU khi xoá thuộc tính —
  thứ tự ấy có thật sự đủ không, hay có đầu vào làm nó cắt sai?

### 5. Gate — tự chạy, đừng chép

```bash
python3 .claude/dev/packet_loop_test.py                     # ĐÒI hai số BẰNG NHAU
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py doc-claims-check --strict --json      # ĐÒI flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test                           # KHÔNG --write
python3 .githooks/eol_policy.py --all --json                # ĐÒI violations=0
```

Người vá đã chạy trên `5ec8fab`: suite **178/178** · 47 đột biến · 69 lớp lách · 37 ca
bắt-oan · 0 ngoại lệ AC 18 · `doctrine-scan` rc=0 · EOL checked=304 violations=0 ·
doc-claims `flags=[]`.

`tl.py --selftest` **chết** trong container điều phối (`ModuleNotFoundError: _cffi_backend`
→ `pyo3_runtime.PanicException` từ `cryptography`). Lượt 9 và 11 cũng không chạy được.
**`1696/1696` tới nay CHƯA AI xác minh** — chạy được thì báo số thật, không chạy được thì
nói rõ và **đừng mượn số của ai**.

**Mọi lệnh trong verdict phải neo SHA BẤT BIẾN** — không `origin/master`, không `HEAD`,
không tên nhánh.

### 6. Fixture — đăng NGUYÊN VĂN

Lượt 9 mô tả fixture bằng lời; bên điều phối dựng lại **sai** rồi báo nhầm "không tái lập
được", phải đính chính. Verdict của bạn phải kèm **nội dung tệp fixture nguyên văn** cho
mọi ca, và mỗi ca lọt phải có **đối chứng cùng-câu-khác-đúng-một-biến**.

---

## Verdict và evidence

`approve` · `changes_requested` · `blocked`.

Mỗi finding: `finding_id` (slug kebab-case ổn định), `severity`, `disposition`, **bằng
chứng chạy được neo SHA bất biến** + **fixture nguyên văn**. Không tái lập được thì ghi rõ
là **nghi vấn**.

**Nói thẳng chỗ bạn KHÔNG chạy được.**

### Giao kết quả

Ưu tiên: review trên **PR** nếu có, kèm evidence §7 lên issue #55, neo
`commitID = 5ec8fabfded6adcfb8b7288ac7846f92267e165e`.

Không ghi được thì ghi ra tệp — khuôn đã chạy từ lượt 5:

```
ops/reviews/wp55-r3-review-12-codex-verdict.md
ops/reviews/wp55-r3-review-12-codex-verdict.receipt.yaml
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay. Báo `sha256` + số byte.

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · bước xác minh lệch · bị đòi
sửa tệp/commit/push/merge/land · không chạy được phần thiết yếu (báo `blocked` kèm lý do
ĐO ĐƯỢC, đừng đoán rồi `approve`) · chạm quota (ghi lý do allowlist, **không** tiêu attempt
nội dung).
