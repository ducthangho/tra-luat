Mọi phép đo đã xong. Ba kết quả chốt: **DELGUARD sống 21/21** (xoá hẳn guard mới thêm mà suite không thấy), `gh issue list --json headRefName` bị gh thật từ chối **cục bộ** ("Unknown JSON field"), và ba cặp số trong chú thích t19 mới **đo lại khớp từng giá trị**. Kho không bị đụng (mọi đột biến chạy trên bản sao trong scratchpad; golden ghim `core.abbrev=7` qua biến môi trường, không ghi config).

---

verdict: changes_requested
reviewed_sha: 99e9383e9ff60bb8850f41242beb607808a821e9
assurance: same_provider_approved

**Lượt này không cấp điều kiện land** (same-provider, `codex` hết quota — §8 chưa thoả; muốn land cần uỷ quyền mới của chủ kho neo SHA cuối). Verdict dưới đây chỉ nói về chất lượng bản vá.

## Danh sách đóng được của lượt 5

**Finding P2 (gh giả mù argv): ĐÓNG cho bốn con đã nêu — CHƯA ĐÓNG LỚP.**
Đã dựng lại cả bốn và chạy: A1 `--limit 200` · A2 bỏ `--limit` · A3 `--state closed` · A4 bỏ `baseRefName` — **mỗi con 20/21, đỏ đúng `t21`**, khớp số người vá. Phản chứng cho chính chốt cũng đạt: gỡ khối đòi argv + A1 ⇒ **21/21, A1 sống lại** — `t21` đang đo argv thật chứ không đo thứ khác. Nhưng cùng lớp `--limit`/`--state` tái sinh được bằng token THỪA mà chốt `-contains` không thấy — xem Finding 1, đúng ca prompt định trước là P1.

**Chốt `t20` đòi "cua 999 PR dang mo": ĐÓNG — và giữ nguyên là đúng.**
Helper-rỗng ⇒ **18/21, `t20` ĐỎ thật** (khớp số người vá; trước đây chỉ `t21` bắt). Đã đo cả hai vế câu hỏi lượt 5 đặt ra: (a) đổi câu in chính đáng trong `don-nhanh.ps1` (`ref cua`→`ref tu`) ⇒ `t20` đỏ oan 20/21 — cái giá là THẬT; (b) dựng biến thể `t20` ghim-theo-hành-vi đúng phác thảo lượt 5 (PR cuối trỏ base nhánh thật, đòi nhánh được giữ, bỏ ghim chuỗi) rồi bơm helper-rỗng vào: **`t20` biến thể XANH** (19/21, chỉ t19/t21 đỏ) — phác thảo ấy **trượt đúng ca nó được đề xuất để bắt**, vì PR đặc biệt không đi qua helper. Ghim chuỗi rẻ hơn VÀ bắt được nhiều hơn; đỏ-oan là giá chấp nhận, có thông điệp tự giải thích.

**Guard `Nhieu-PR` (`$So -lt 1`): ĐÓNG MỘT NỬA.** Bẫy `1..0` đóng thật (counts −1→0, 0→0, 1→1, 2→2 tái lập khớp). Nhưng nhánh guard không giao thứ nó viết, và xoá hẳn guard suite vẫn 21/21 — xem Finding 2.

**Chú thích `t19` (sửa lời khai "10/9 nhỏ nhất"): ĐÓNG.** Đo lại trên pwsh 7.4.6: (10,9) số True/chuỗi False · (10,2) số True/chuỗi False · (9,2) số True/chuỗi True — khớp từng giá trị với lời khai mới "nhỏ nhất thật sự là ĐẾM = 10".

## Findings

### Finding 1 — P1 · đột biến sống sót: chốt argv `-contains` bị vượt bằng token THỪA; cờ lặp trên `gh` thật là cờ-SAU-thắng (đã đo), nên đúng hai lỗ `--limit`/`--state` vừa vá tái sinh nguyên vẹn

Bốn đột biến mới vào dòng gọi `gh`, **cả bốn sống 21/21** (chạy thật, bản sao tạm):

| | Đột biến | Suite | Hệ quả trên `gh` thật |
|---|---|---|---|
| B1 | thêm `--limit 30` **sau** `--limit $TranPR` | **21/21** | limit hiệu lực = **30** → danh sách cắt ở 30 → `30 -ge 1000` không bao giờ nổ → xoá base của PR ngoài 30 con đầu — **đúng lỗ gốc PR #150 sinh ra để vá** |
| B2 | thêm `--state closed` cuối dòng | **21/21** | state hiệu lực = closed → giữ base PR ĐÃ ĐÓNG, bỏ rơi PR đang mở — tái sinh A3 |
| B3 | thêm `--repo x/y` | **21/21** | **lời khai trong chú thích t21 "thêm một cờ chính đáng (vd `--repo`) SẼ làm ca này ĐỎ" là SAI ĐO ĐƯỢC** — đúng họ lỗi lời-khai-trong-chú-thích mà chính lượt này vừa sửa ở t19 |
| B4 | `pr list` → `issue list` | **21/21** | `pr`/`list` không nằm trong sáu token bị đòi; gh thật từ chối **cục bộ** `Unknown JSON field: "headRefName"` → công cụ thành luôn-từ-chối (fail-close, kẹt chứ không xoá nhầm) mà suite vẫn xanh |

Lớp "cờ sau thắng" không còn là suy luận: cài `gh` 2.45.0 (apt) và đo **hai chiều, hoàn toàn cục bộ** — `--limit 1000 --limit 0` → `invalid value for --limit: 0` (giá trị hiệu lực là cờ SAU); `--limit 0 --limit 1000` → **không phàn nàn gì về 0**, đi thẳng tới tầng mạng (cờ 0 không hợp lệ bị cờ sau đè mất); `--state open --state closed` được parse chấp nhận. Gốc bệnh: `-contains` đo sự CÓ MẶT của từng token, không đo CÂU HỎI — danh sách-cấm-theo-token thua từ thiết kế trước token thừa, cùng họ bài học allow-list của kho.

**Gợi ý vá:**
1. **Vá ở đâu:** `scripts/don-nhanh_test.ps1`, khối chốt argv trong `t21` (vòng `foreach … -contains`). Vì lỗ nằm ở PHÉP SO, không ở cách ghi: `argv.txt` đã chứa đủ cả 8 token (đo được), chỉ phép so đang mù.
2. **Vá thế nào:** thay vòng foreach bằng MỘT phép so nguyên câu: `($tok -join ' ') -ceq 'pr list --state open --limit 1000 --json headRefName,baseRefName'`. Phải `-ceq` chứ không `-eq` — `-eq` chuỗi của PowerShell mù hoa-thường (đo: `'--STATE OPEN' -eq '--state open'` → True). So nguyên câu tự khắc ghim luôn `pr list`, cấm token thừa/lặp/đảo chỗ. Đã chạy thử hướng này trên bản sao: **baseline 21/21; giết cả B1–B4 lẫn A1** (spot-check).
3. **Ca khoá + đột biến phải chết:** vẫn `t21`. Sau vá, bốn con B1–B4 phải 20/21 đỏ `t21`; giữ nguyên phản chứng cũ (gỡ chốt → A1 sống lại 21/21). Muốn trả thêm tính đơn-ca của chốt (mục kiểm 2), cùng dòng bang ấy dùng được cho `t20` với `999` — mở rộng, không bắt buộc để đóng lớp.
4. **Bản vá đẻ ra gì:** (a) mọi thay đổi hợp đồng chính đáng (thêm `--repo`, đảo thứ tự cờ) nay bắt buộc sửa test — đúng ý đồ đã khai, và làm lời khai `--repo` trong chú thích thành ĐÚNG thay vì phải viết lại nó; (b) chuỗi kỳ vọng lặp hằng `1000` lần thứ ba — cùng họ nợ "hằng không tự canh" đã khai; (c) nếu mai kia script mọc lời gọi `gh` thứ hai (phân trang), `argv.txt` ghi `>` chỉ giữ lần cuối và phép so đo lần cuối — lúc đó phải đổi cả cách ghi lẫn cách so (xem Nợ).

### Finding 2 — P3 · đột biến sống sót + lời hứa sai trong mã mới: xoá hẳn guard `Nhieu-PR` suite vẫn 21/21, và nhánh guard giao `$null` chứ không phải `@()` — fake gh sẽ in `[null]`, thứ gh thật không bao giờ in

Ba phép đo, đều trên pwsh 7.4.6:
- Đột biến **xoá nguyên dòng** `if ($So -lt 1) { return @() }` → **21/21** — guard là mã không phép đo nào canh (miền gọi hiện tại 10/999/1000 không chạm nó).
- `$null -eq (Nhieu-PR 0)` → **True**: `return @()` qua pipeline bị tháo rỗng thành `$null`, không phải mảng rỗng như dòng mã viết. Qua binding `[object[]]$PR` của `Dung-Gh-Gia`, `@($PR)` = `@($null)` = 1 phần tử → fake gh in **`[null]`** (đo), trong khi `-PR @()` in `[]`. Script thật đọc `[null]` thành **1 PR ma** (đo: `@(ConvertFrom-Json '[null]').Count` = 1, "cua 1 PR dang mo" với 0 ref giữ).
- Phép nghiệm của người vá (−1→0, 0→0 qua `.Count`) **tái lập được nhưng mù với lỗi này**: `$null.Count` cũng bằng 0 — dụng cụ đo không thể đỏ, nên không phải bằng chứng, đúng doctrine kho.

Latent — chưa caller nào gọi `Nhieu-PR 0` — nhưng lý do tồn tại duy nhất của guard là caller tương lai, theo chính chú thích của nó; và "vá bẫy `1..0` mở bẫy `[null]` kề bên trong cùng hàm" là đúng hình dạng lỗi CLAUDE.md đã ghi.

**Gợi ý vá:**
1. **Vá ở đâu:** đầu hàm `Dung-Gh-Gia` — KHÔNG phải trong `Nhieu-PR`. Lỗ nằm ở BIÊN tiêu thụ ($null qua binding), vá ở biên đóng cả ba đường một lúc: `(Nhieu-PR 0)`, `-PR $null` tường minh, và quên `-PR`.
2. **Vá thế nào:** một dòng chuẩn hoá `$null → @()` cho `$PR` trước khi dựng `$than`. **ĐỪNG** vá bằng `,@()` trong `Nhieu-PR` — đo rồi: nó làm `@(Nhieu-PR 0).Count` thành **1** (mảng-bọc-mảng) và ai bọc phòng thủ `@(…)` sẽ đưa `[[]]` vào fake. Đã đo hướng chuẩn-hoá-ở-biên: cả bốn đường đều ra `[]`, đường thường không đổi, counts giữ nguyên 0,0,1,2.
3. **Ca khoá + đột biến phải chết:** một ca "0 PR" nhỏ: `Dung-Gh-Gia -PR (Nhieu-PR 0)` + `-Xoa`, đòi rc=0 **và** `cua\s+0\s+PR dang mo`. Ca này giết CẢ HAI con đang sống: bỏ dòng chuẩn hoá → `[null]` → "cua 1 PR" → đỏ; xoá guard → `1..0` → 2 PR ma → "cua 2 PR" → đỏ.
4. **Bản vá đẻ ra gì:** chuẩn hoá $null→@() che mất ca "cố tình truyền $null để thử fake hỏng" — rủi ro thấp vì đường bơm rác/rỗng đã có sẵn `-ThoNguyen`; ca "0 PR" mới ghim thêm một câu chữ ("cua 0 PR") — cùng cái giá đỏ-oan-khi-đổi-câu như t20, đã cân nhắc và chấp nhận ở đó.

## Nợ khai báo

- **Chốt argv đơn-ca (chỉ `t21`).** Đã đo: không có đường chết-lặng — `bang` ném là ca đỏ, và đột biến "không bao giờ gọi gh nhưng vẫn rc=13" chết ĐÚNG tại bang `Test-Path` ("chot nay dang khong do gi"), kèm 7 ca khác đỏ. Nợ kiến trúc nhỏ, không phải lỗ đang chảy máu; gợi ý mở rộng nằm trong Finding 1.3.
- **`argv.txt` ghi `>` (đè).** Hôm nay vô hại: script hỏi `gh` đúng **1 lần/lượt** (đo bằng fake có đếm: 19/19 ca = 1 call; 19 thư mục GUID riêng, 0 rác lọt giữa các ca). Thành bẫy nếu script mọc lời gọi thứ hai (phân trang) — lúc đó chốt chỉ đo lần cuối.
- **Ghim câu chữ ở `t20` có đỏ-oan đo được** (đổi `ref cua`→`ref tu` ⇒ 20/21). Chấp nhận, vì đường thay thế của lượt 5 trượt helper-rỗng (đo ở phần đóng lượt 5) — khai để người đổi câu in sau này biết phải sửa `t20` kèm theo, đó là ý đồ chứ không phải oan sai.
- **`gh` thật nay CÓ trong container (apt 2.45.0) nhưng chỉ đo được tầng PARSE cục bộ** — mạng vẫn bị proxy chặn (403 tự sinh). Nợ `gh-phan-trang-that-chua-ai-do` GIỮ NGUYÊN; các probe cờ-lặp ở Finding 1 là tầng parse, không phải phép đo phân trang.
- Các nợ đã khai còn lại: kiểm đúng như khai, không nêu lại.

## Phép đo đã chạy

Môi trường: pwsh 7.4.6 tại `/dev/shm/pwsh/pwsh` (kiểm chạy được trước khi đọc số), `TMPDIR=/dev/shm`, gh 2.45.0 (apt, chỉ dùng đo parse cục bộ). Mọi đột biến trên bản sao tạm trong scratchpad, mỗi con một thư mục, diff xác nhận đã áp trước khi chạy; cây repo không bị ghi.

1. Baseline: **21/21**, rc=0 (~17s/lượt).
2. A1/A2/A3/A4 (dựng lại): mỗi con **20/21, đỏ t21** — khớp người vá.
3. Phản chứng chốt: gỡ khối argv + A1 → **21/21** (A1 sống lại) — khớp.
4. B1 (`--limit 30` sau) · B2 (`--state closed` cuối) · B3 (`--repo x/y`) · B4 (`issue list`): **cả bốn 21/21** — Finding 1.
5. gh thật: `--limit 1000 --limit 0` → `invalid value: 0`; `--limit 0 --limit 1000` → không lỗi về 0, tới tầng mạng; `--state` lặp parse OK; `issue list --json headRefName` → `Unknown JSON field` cục bộ.
6. FIX thử (so nguyên câu `-ceq`): baseline **21/21**; giết B1, B2, B3, B4, A1 (mỗi con 20/21 đỏ t21). Probe `-eq` mù hoa-thường → True, `-ceq` → False.
7. Helper-rỗng: **18/21, đỏ t19+t20+t21** — t20 độc lập thật, khớp người vá.
8. NOGH (không bao giờ gọi gh, vẫn rc=13): 13/21; t21 chết đúng tại bang `Test-Path`.
9. Đếm lời gọi gh: 19 thư mục gh giả (=21−2 ca $null), **mỗi calls.txt đúng 1 dòng**, 0 thư mục mồ côi.
10. WORD (đổi câu in): **20/21, đỏ t20** (đỏ-oan thật). VARIANT ghim-hành-vi (phác thảo lượt 5): baseline 21/21; **+helper-rỗng → 19/21, t20 XANH** (trượt); +WORD → 21/21 (miễn nhiễm câu chữ).
11. `Nhieu-PR`: `$null -eq (Nhieu-PR 0)` → True; `-is [array]` → False; qua `-PR` → JSON **`[null]`** (đối chứng `-PR @()` → `[]`); `@(ConvertFrom-Json '[null]').Count` → 1; counts −1,0,1,2 → 0,0,1,2 (khớp người vá, và vì sao phép đo ấy mù). DELGUARD (xoá guard) → **21/21 sống** — Finding 2. Vá thử `,@()` → counts thành 1,1,1,2 (bác); vá thử chuẩn-hoá-ở-biên → cả bốn đường `[]`, counts nguyên vẹn.
12. t19: (10,9)/(10,2)/(9,2) — số/chuỗi khớp từng giá trị lời khai mới.
13. Cổng khác (đối chiếu số người vá): eol `ok=true checked=398 violations=0` · lease_publish **31/31** · release-verify trên `git archive HEAD` `ok=true failed=[]` · golden rc=0 `ok=true` (ghim `core.abbrev=7` qua `GIT_CONFIG_*`, không ghi config) · file_count **179** (RELEASE_MANIFEST.json). Tất cả khớp.
