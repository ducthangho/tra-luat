# VERDICT — cross-review lượt 4 (VÒNG CANON, CÓ LEASE) của `PLAT-X8` (#225 / PR #248), reviewer `claude`

`reviewed_sha` **`28f32f7cfb393c759e73e8afbb566a54866fc4b4`** · `base_sha`
**`08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9`** · executor `codex` · lease
`plat-x8-review-4-claude-20260822` (role: reviewer, đã tự kiểm tồn tại — xem bảng đo #1)

## VERDICT: `changes_requested`

Không có hồi quy chức năng nào trong bản vá của lượt 3. Nhưng tìm được **một finding MỚI thật, đo
được, đã thử vá + kiểm chứng trên bản sao** (theo đúng `yeu_cau_rieng_luot_nay` của lease): bản vá
lượt 3 (xoá 4 mục khỏi `_BANG_LOP`) vô tình **xoá luôn hazard duy nhất** mà `t83` dùng để kiểm
`posixpath.normpath` — khiến bước chuẩn hoá traversal có thể bị xoá HOÀN TOÀN mà suite vẫn `87/87
rc=0`. Đây không phải P1 tái phát (không có lease thật nào bị hạ lớp hôm nay), nhưng đúng hình dạng
mà chính packet này đòi phải khoá (`A14`: "vế DƯƠNG phải sống", "không có ca này thì mọi bản vá 'cho
chắc' biến cổng thành máy trả `sensitive` mà không ai đo được").

## Tự khai tư cách canon

**Lease `plat-x8-review-4-claude-20260822` TỒN TẠI THẬT** — đã tự kiểm theo đúng chỉ dẫn PROMPT
(bảng đo #1). Khác hẳn lượt chạy hụt trước (không lease) — lượt đó tự khai đúng vì tại thời điểm nó
chạy (19:34Z) lease chưa được đẩy lên nhánh máy chủ; lease này được cấp SAU đó. `nguoi_review_phai_khac_phien:
true` — lượt này chạy trong phiên `claude` riêng, không phải phiên đã soạn đặc tả/prompt/lease
(không có quyền ghi vào `ops/`, không có bối cảnh soạn đặc tả trong lịch sử phiên).

**Không tự khai `cross_approved` đầy đủ.** Mức đo được: cross-provider review (`codex` thi công ·
`claude` review) có lease reviewer hợp lệ, khác phiên soạn đặc tả, chạy trong cây rời không sửa kho
thật — thoả các điều kiện MÁY ĐO ĐƯỢC của mục tiêu `cross_approved`. Nhưng receipt v2 (đòi receipt ID
+ hai danh tính chứng thực độc lập) là việc của điều phối SAU khi verdict này được đăng, không phải
của reviewer. Và dù receipt có validate hay không: **verdict `changes_requested` nghĩa là packet
chưa sẵn sàng land**, bất kể canon.

## ĐỐI CHIẾU LƯỢT TRƯỚC (L-B)

### 1. Finding nào còn MỞ — đo lại, không tin nhãn

| finding (lượt) | trạng thái lượt trước khai | ĐO LẠI lượt này |
|---|---|---|
| `duong-di-xuyen-thu-muc-ha-lop` (lượt 1, P1) | ĐÓNG (lượt 2, lượt 4-không-lease đo lại) | **ĐÓNG về OUTPUT — nhưng cơ chế bảo vệ đã MẤT phép đo** (xem finding mới #1). `t83` vẫn ra `sensitive`, nhưng không còn vì normalization hoạt động — vì bảng thật không còn hazard nào để traversal khai thác |
| `schema-version-hong-fail-open` (lượt 1, P1) | ĐÓNG | **VẪN ĐÓNG, xác nhận độc lập** — `t84`/`t85` nằm trong suite `87/87 rc=0` (bảng đo #2), tự đọc `_kiem_lop_review`: `isinstance(raw_schema, bool) or not isinstance(raw_schema, (int, str))` chặn trước `int()` |
| `thu-muc-tran-doi-lop` (lượt 2, P2 nợ) | SUPERSEDED (lượt 3 xoá `docs/adr/`) | Xác nhận: `docs/adr/` không còn trong `_BANG_LOP` (bảng đo #3, grep 0 kết quả) |
| `bang-lop-noi-ngoai-8-572` (lượt 3, P1) | ĐÓNG bởi executor tại `28f32f7c` | **ĐÓNG, xác nhận độc lập lần thứ hai** — tự đọc `_BANG_LOP` sống (7 mục, tất cả `sensitive`, bảng đo #3), tự dựng lại đột biến khôi phục 4 mục trên **bản sao riêng của tôi** (không dùng cache của điều phối lẫn không dùng cache của lượt-4-không-lease) ⇒ `85/87 rc=1`, đúng `t86`+`t87` đỏ (bảng đo #4) |
| `commit-message-mot-dong` (lượt 1, P2) | ĐÓNG (lượt 2) | Không đo lại — ngoài `write_set`, không có tín hiệu hồi quy |
| `A12-chua-do-lai-tren-head-moi` (lượt-4-không-lease, khai là finding) | — | **SAI, đúng như PROMPT đã cảnh báo trước.** Xem mục "A12" riêng bên dưới |

### 2. Lượt trước có kết luận nào SAI không?

**Có — hai chỗ, cả hai đều trong lượt-4-KHÔNG-LEASE** (lượt chạy hụt, không tính canon nhưng vẫn là
dữ liệu phải soi như soi mã, đúng chỉ dẫn PROMPT):

**(a) A12 — SAI, đã có bằng chứng trước khi nó chạy.** Lượt-4-không-lease báo
`A12-chua-do-lai-tren-head-moi` là finding, viện dẫn bằng chứng cũ (`run 32587850266`, neo head
`86a55663` — head CŨ) và kết luận A12 "chưa có bằng chứng nó đã được thực hiện sau đó". Sai: đã có
`run 32592693727` chạy `workflow_dispatch` đúng trên `28f32f7c`, cả hai job `gate (ubuntu-latest)` và
`gate (windows-latest)` = `success`, `TONG BUOC HONG = 0` (nội dung đầy đủ ở `A12-EVIDENCE.md`, do
điều phối cung cấp). **Đây là lời khai của phiên điều phối, không phải phép đo của tôi** — tôi không
có công cụ Actions (đã kiểm qua `ToolSearch`, không có `mcp__github__` action nào trong danh sách
công cụ khả dụng của phiên reviewer). Đúng như PROMPT chỉ dẫn và như `plat-x5-review-2` từng làm: tôi
khai đúng A12 đã có bằng chứng — không báo nó là khoảng trống, không tự nhận đó là phép đo của mình.

**(b) Trích dẫn sai NHÁNH cho biên nhận lượt 3 — chỗ SAI thứ hai, chưa ai chỉ ra.** Lượt-4-không-lease
viết ở mục "Giới hạn": *"Tôi đọc và đối chiếu `ops/reviews/plat-x8-review-3-claude-verdict.receipt.yaml`
trên nhánh `ops/cap-lease-plat-x8-2`"*. **Sai** — đo trực tiếp (bảng đo #5): tệp đó **KHÔNG** nằm trên
`origin/ops/cap-lease-plat-x8-2` ở đầu nhánh hiện tại (`ls-tree` chỉ thấy biên nhận lượt 1 và lượt 2,
không có lượt 3). Nó chỉ tồn tại trên `origin/claude/phien-tra-luat-5a-handoff-9o1cqp` — một nhánh
handoff đã được merge MỘT LẦN vào `ops/cap-lease-plat-x8-2` lúc `18:09:08Z` (commit `8cd2262b`), rồi
phiên review lượt 3 tiếp tục commit LÊN TRÊN nhánh handoff đó SAU thời điểm merge (`247c6fb5` lúc
`19:14:40Z`) — và không ai merge lại lần hai. Kết quả: **biên nhận + verdict của lượt 3 đang MỒ CÔI**,
không nằm trên nhánh chính thức của packet, dù nội dung của nó (mà tôi đã đọc trực tiếp qua
`git show f8ebd5f3:...`) khớp với những gì lượt-4-không-lease trích dẫn — chỉ có **vị trí** là sai.
Đây đúng hình dạng doctrine `CLAUDE.md` "SỔ LEASE KHÔNG NẰM MỘT CHỖ": trích dẫn tiện tay (nhánh đang
mở trong sandbox) thay vì trích dẫn nơi có thẩm quyền (nhánh phối hợp chính thức của packet). Không
phải finding trong `write_set` — không có mã để vá — nhưng là một khoảng trống QUY TRÌNH thật, xem
mục finding riêng bên dưới.

**Không có kết luận sai nào của LƯỢT 1/2/3 (ba lượt có lease/tính canon-eligible) mà tôi tìm thêm
được** ngoài những gì lượt 3 đã tự nêu về lượt 1/2 (giả định "bảng seed đúng" chưa từng được đặc tả
cho phép — đã đóng đúng, xác nhận lại ở bảng đo #3).

### 3. Bản vá lượt trước đẻ ra gì mới?

**Có — và đây chính là finding mới của lượt này.** Bản vá lượt 3 (xoá 4 mục `systemic` khỏi
`_BANG_LOP`) đúng về hành vi ĐẦU RA (không lease thật nào bị hạ lớp), nhưng nó xoá luôn ĐÍCH DUY NHẤT
mà `t83` dùng để chứng minh `posixpath.normpath` còn hoạt động. Trước lượt 3, `docs/adr/` là một mục
`systemic` thật trong bảng — traversal qua nó là hazard CÓ THẬT, và `t83` (gián tiếp qua P1 gốc) đo
đúng hazard đó. Sau lượt 3, bảng thật không còn mục nào thấp hơn `sensitive` — traversal không còn gì
để "hạ" xuống nữa, nên `t83` giờ đúng một cách VÔ NGHĨA (đo bằng thực nghiệm ở bảng đo #6: xoá hẳn
dòng `posixpath.normpath` khỏi mã, suite vẫn `87/87 rc=0`). Không ai trong ba lượt trước (kể cả
lượt-4-không-lease) đo theo hướng "nếu tôi xoá hẳn cơ chế bảo vệ, còn ca nào bắt được không?" —
đúng câu hỏi PROMPT gợi ý ("có ca nào chỉ xanh vì dữ liệu hiện tại tình cờ hợp lệ?"), và câu trả lời
lần này là CÓ, cho đúng một cơ chế.

## Finding MỚI — `chuan-hoa-traversal-mat-phep-do-sau-khi-vet-hazard-bi-xoa` (đủ 4 phần)

### Bằng chứng đo được (đã thử vá + kiểm chứng trên BẢN SAO CẢ CÂY, không đụng cây review/nhánh executor)

Quy trình đúng yêu cầu lease (`yeu_cau_rieng_luot_nay`): dựng bản sao cả cây bằng
`git archive 28f32f7c | tar -x` vào thư mục scratch riêng trong `/tmp`, không dùng lại cache của điều
phối lẫn của lượt-4-không-lease.

1. **Baseline trên bản sao riêng**: `python3 ops/lease_publish_test.py` ⇒ `87/87 đạt, rc=0` (bảng đo #7).
2. **Đột biến**: xoá dòng `duong = posixpath.normpath(duong)` khỏi `_tinh_lop_tu_write_set` (giữ
   nguyên mọi thứ khác) ⇒ chạy lại suite **KHÔNG sửa test** ⇒ `87/87 đạt, rc=0` — **KHÔNG CA NÀO ĐỎ**
   (bảng đo #8). Đây là bằng chứng chính: xoá hẳn bước chuẩn hoá không làm suite hiện tại phát hiện.
3. **Xác nhận bằng tay, độc lập với suite**: gọi trực tiếp `_tinh_lop_tu_write_set` sau khi bơm một
   mục `("docs/adr/", "routine")` TẠM vào `_BANG_LOP` (cùng nếp `t77`/`t81`) — trên bản THẬT (chưa
   mutate): `docs/adr/../../ops/lease_publish.py` ⇒ `sensitive` (đúng, normalization hoạt động); trên
   bản mutant (đã xoá `normpath`): cùng input ⇒ **`routine`** — HẠ LỚP thật (bảng đo #9).
4. **Vá đề xuất — ca test mới `t88`**, thêm vào `ops/lease_publish_test.py` ngay sau `t87`:

```python
@ca
def t88_traversal_van_bi_chan_khi_bang_co_muc_thap_hon_TAM():
    """t83 tự nó không còn phủ normalization: bảng thật (7 mục, toàn
    `sensitive`) không có mục thấp hơn nào để traversal hạ xuống, nên xoá
    hẳn `posixpath.normpath` khỏi `_tinh_lop_tu_write_set` vẫn 87/87 — đo
    được, không đoán. Ca này bơm một mục `routine` TẠM (cùng nếp t77/t81)
    để traversal có đích thật, khoá lại đúng P1 lượt 1 cho bảng SAU này."""
    mod = _nap_cong()
    mod._BANG_LOP = (("docs/adr/", "routine"),) + mod._BANG_LOP
    for tien_to in ("", "planned:"):
        duong = tien_to + "docs/adr/../../ops/lease_publish.py"
        bang(mod._tinh_lop_tu_write_set([duong]) == "sensitive",
             f"traversal {duong!r} hạ lớp khi bảng có mục thấp hơn")
```

5. **Kiểm chứng vá**: áp `t88` lên bản sao THẬT (mã không đổi) ⇒ `88/88 đạt, rc=0` (bảng đo #10).
6. **Đột biến gỡ vá phải làm ca đích ĐỎ**: áp lại đúng đột biến bước 2 (xoá `posixpath.normpath`)
   TRÊN bản đã có `t88` ⇒ `87/88 đạt, rc=1`, đúng và CHỈ `t88` đỏ (`t83` vẫn xanh — chính là bằng
   chứng `t83` không còn đo được gì) (bảng đo #11).

| phần | nội dung |
|---|---|
| **vá ở đâu** | `ops/lease_publish_test.py`, thêm ca mới ngay sau `t87` (dòng ~2892 ở exact head). Không vá `ops/lease_publish.py` — mã sản phẩm ĐÚNG, chỉ thiếu phép đo cho đúng nhánh nó bảo vệ |
| **vá thế nào** | Bơm một mục thấp hơn `sensitive` TẠM vào `_BANG_LOP` (cùng nếp `t77`/`t81`/`A14`), rồi kiểm traversal qua đúng mục đó vẫn bị chuẩn hoá về `sensitive`. Không sửa `_BANG_LOP` thật — giữ nguyên chỉ 7 mục theo đúng §8:572 |
| **ca test khoá nó + đột biến phải chết** | `t88` ở trên. Đột biến: xoá dòng `posixpath.normpath(duong)` (giữ nguyên phần còn lại của hàm) ⇒ `t88` phải ĐỎ. Đã đo cả hai chiều: có `t88` + đột biến ⇒ ĐỎ đúng ca; không có `t88` + đột biến ⇒ suite vẫn `87/87` xanh (mù) |
| **bản vá đẻ ra gì** | Rủi ro thấp: `t88` chỉ gọi hàm thuần (`_tinh_lop_tu_write_set`), không đụng I/O, không phụ thuộc trạng thái module khác (`_nap_cong()` nạp module MỚI mỗi lần — xác nhận ở mục riêng bên dưới, trả lời câu hỏi #2 của PROMPT). Không có gì để "đẻ ra" ngoài một dòng test thêm; không đổi hành vi sản phẩm |

## Trả lời ba câu "đáng hỏi" của PROMPT (TRẦN, không phải sàn — nhưng đọc hết vẫn cần)

1. **`t86` đòi MỌI mục `_BANG_LOP` là `sensitive` — giòn quá tay?** Đúng ý định hiện tại (bảng seed
   packet NÀY chỉ được chứa sensitive, §8 ba lần nguyên văn). Nếu một packet SAU được duyệt nới bảng
   đúng quy trình, `t86` sẽ ĐỎ có chủ đích — đây KHÔNG phải lỗi, là chốt đợi sửa CÓ Ý THỨC (đã ghi rõ
   trong `_BANG_LOP` docstring và §8 đặc tả). Không cần vá.
2. **`t77` bơm mục `routine` TẠM vào `mod._BANG_LOP`. Có rò sang ca khác không?** **KHÔNG.** Đo trực
   tiếp: `_nap_cong()` gọi `importlib.util.module_from_spec` + `exec_module` mỗi lần, KHÔNG đăng ký
   vào `sys.modules` — mỗi lệnh gọi tạo một đối tượng module hoàn toàn mới, độc lập bộ nhớ. `t77`,
   `t79`, `t81`, `t88` (đề xuất) đều tự gọi `_nap_cong()` riêng nên sửa `mod._BANG_LOP` của ca này
   không chạm ca khác. Xác nhận bằng đọc mã (bảng đo #12), không cần đột biến vì đây là thuộc tính
   CẤU TRÚC của cách nạp module, không phải hành vi có thể trôi.
3. **Bảng seed nay chỉ còn `sensitive`. Còn ca nào phủ vế DƯƠNG của `routine`/`systemic`, hay đã
   thành mã chết?** **Đã thành mã chết ĐỐI VỚI DỮ LIỆU THẬT** — dưới `_BANG_LOP` thật (7 mục, toàn
   `sensitive`), `_tinh_lop_tu_write_set` KHÔNG THỂ trả về gì khác ngoài `sensitive` cho bất kỳ
   `write_set` không rỗng nào (mọi mục khớp bảng hoặc rơi mặc định đều là `sensitive`). Vế DƯƠNG chỉ
   còn sống nhờ test tự bơm bảng tạm (`t77`, `t81`, và `t88` đề xuất) — đúng như `A14` đã thiết kế.
   Đây **không phải lỗ**, mà là hệ quả ĐÚNG của Q2 (fail-closed) mà đặc tả §8/§9.1 đã tự nói ra
   ("không packet nào của kho là routine/systemic" dưới bảng seed này) — không cần vá, chỉ cần nói
   rõ ràng, và finding mới ở trên là hệ quả TRỰC TIẾP của đúng sự thật này (không còn low-tier thật
   ⇒ traversal-normalization cũng mất luôn đích để chứng minh nó còn chạy).

## Finding QUY TRÌNH (không phải mã, không có write_set để vá) — `bien-nhan-luot-3-mo-coi-nhanh`

| phần | nội dung |
|---|---|
| **vá ở đâu** | Không phải mã. `git`: cherry-pick hoặc merge lại hai commit `247c6fb5` (ghi verdict+biên nhận lượt 3) và `f8ebd5f3` (ghim `evidence_url`) từ `origin/claude/phien-tra-luat-5a-handoff-9o1cqp` vào `ops/cap-lease-plat-x8-2` |
| **vá thế nào** | `git merge-base --is-ancestor 247c6fb5 origin/ops/cap-lease-plat-x8-2` ⇒ `rc=1` (KHÔNG phải tổ tiên) chứng minh nó chưa từng vào nhánh chính thức. Nguyên nhân đo được: nhánh handoff được merge một lần lúc `18:09:08Z` (`8cd2262b`), rồi phiên review lượt 3 tiếp tục commit LÊN TRÊN nhánh handoff đó lúc `19:14:40Z` — sau điểm merge — nên không ai merge lại lần hai |
| **ca test khoá nó + đột biến phải chết** | Không phải ca `pytest` — là một chốt QUY TRÌNH đo được bằng `git`: trước khi coi packet "đã qua lượt N", điều phối chạy `git merge-base --is-ancestor <commit-biên-nhận-lượt-N> origin/<nhánh-phối-hợp-packet>`; `rc != 0` ⇒ biên nhận mồ côi, chặn. Chưa có cơ chế MÁY nào cưỡng chế điều này — cùng họ nợ mà lượt 3 đã khai cho `t86` ("KHÔNG cổng nào ngăn ai đó...") |
| **bản vá đẻ ra gì** | Nếu không sửa: bất kỳ ai sau này audit "packet này đã qua đủ mấy lượt review, biên nhận ở đâu" bằng cách đọc `ops/cap-lease-plat-x8-2` (nhánh có thẩm quyền) sẽ thấy THIẾU lượt 3 — đúng dấu hiệu packet-chưa-đủ-lượt trong khi thực ra lượt 3 đã chạy và đã vá xong. Rủi ro: audit sai, hoặc tệ hơn, một lượt review TƯƠNG LAI tưởng lượt 3 chưa từng xảy ra rồi làm lại |

## A12 — đọc theo đúng chỉ dẫn PROMPT, không tự đo

**Không có công cụ Actions** (đã kiểm `ToolSearch`, không tool `mcp__github__actions*`/`workflow_dispatch`
nào khả dụng cho vai reviewer). Theo `A12-EVIDENCE.md` — **lời khai của phiên điều phối, không phải
phép đo của tôi**: `workflow_dispatch` run `32592693727` trên đúng `28f32f7c`, `gate (ubuntu-latest)`
= `success` (31 bước, 0 hỏng), `gate (windows-latest)` = `success` (31 bước, 0 hỏng), `TONG BUOC HONG
= 0`. Khai đúng như `plat-x5-review-2` đã làm: A12 **ĐÃ CÓ BẰNG CHỨNG**, không phải khoảng trống —
khác với lượt-4-không-lease đã báo sai chỗ này (xem mục ĐỐI CHIẾU #2a).

## Nghiệm thu — bảng đo, `rc` đọc trực tiếp

| # | lệnh | kết quả | `rc` | thời điểm + head |
|---|---|---|---|---|
| 1 | `git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ \| grep review-4` | `ops/leases/plat-x8-review-4-claude-20260822.yaml` có mặt | 0 | 19:5xZ 2026-08-22 |
| — | `git rev-parse HEAD` (cây review) | `28f32f7cfb393c759e73e8afbb566a54866fc4b4` | 0 | cùng lúc |
| — | `git rev-parse --is-shallow-repository` | `false` | 0 | cùng lúc |
| — | `git branch -r \| wc -l` | `168` | n/a | cùng lúc |
| 2 | `python3 ops/lease_publish_test.py` (cây review, chưa mutate) | `87/87 đạt; đã chạy=87, bỏ qua=0` | 0 | 2026-08-22, đầu phiên, head `28f32f7c` |
| 3 | `grep -n "_BANG_LOP = (" -A 12 ops/lease_publish.py`; `grep "docs/adr\|PROTOCOL_DA_PHIEN.md\|chay_lease_publish_test.sh" ops/lease_publish.py` | 7 mục, tất cả `"sensitive"`; 0 tham chiếu chết còn sót trong mã sản phẩm | n/a | cùng lúc |
| 4 | Bản sao cả cây (`git archive 28f32f7c` → scratch riêng), khôi phục 4 mục `systemic`, `python3 -B ops/lease_publish_test.py` | `85/87 đạt; đã chạy=87` — đúng `t86`+`t87` ĐỎ | 1 | ~20:00Z, bản sao riêng tại `28f32f7c` |
| 5 | `git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/reviews/ \| grep plat-x8`; `git merge-base --is-ancestor 247c6fb5 origin/ops/cap-lease-plat-x8-2`; `git branch -r --contains 247c6fb5` | chỉ thấy biên nhận lượt 1+2 (KHÔNG có lượt 3); `is-ancestor` ⇒ **rc=1**; nằm trên `origin/claude/phien-tra-luat-5a-handoff-9o1cqp` | 1 (is-ancestor) | 20:00Z |
| 6 | Bản sao cả cây (mới, sạch), xoá dòng `posixpath.normpath(duong)`, `python3 -B ops/lease_publish_test.py` **KHÔNG sửa test** | `87/87 đạt; đã chạy=87` — **KHÔNG CA NÀO ĐỎ** | 0 | 20:0xZ, bản sao riêng tại `28f32f7c` |
| 7 | baseline lần hai, bản sao cả cây độc lập thứ ba | `87/87 đạt; đã chạy=87` | 0 | 20:0xZ |
| 8 | (trùng #6, ghi lại vì là bằng chứng chính của finding mới) | `87/87 đạt` | 0 | 20:0xZ |
| 9 | Gọi trực tiếp `_tinh_lop_tu_write_set` sau khi bơm `("docs/adr/","routine")`: bản thật vs bản đã xoá `normpath` | thật ⇒ `sensitive`; mutant ⇒ **`routine`** (hạ lớp) | n/a (gọi hàm) | 20:0xZ |
| 10 | Thêm `t88` vào bản sao thật (mã không đổi), `python3 -B ops/lease_publish_test.py` | `88/88 đạt; đã chạy=88` | 0 | 20:0xZ |
| 11 | Bản có `t88`, xoá lại `posixpath.normpath(duong)`, `python3 -B ops/lease_publish_test.py` | `87/88 đạt; đã chạy=88` — **đúng và CHỈ `t88` ĐỎ**, `t83` vẫn xanh | 1 | 20:0xZ |
| 12 | Đọc mã `_nap_cong()` (dòng 117-122 `ops/lease_publish_test.py`) | `module_from_spec` + `exec_module`, KHÔNG đăng ký `sys.modules` ⇒ mỗi lần gọi là module độc lập | n/a (đọc mã) | 20:0xZ |
| — | `git diff --shortstat 08bb4ecd...28f32f7c -- ops/lease_publish.py ops/lease_publish_test.py` | `2 files changed, 328 insertions(+), 1 deletion(-)` — khớp CHÍNH XÁC ngoại lệ ADR-0044 đã duyệt (`3 tệp / 328 dòng thêm`, xem `plat-x8-exec-2r6-codex-20260822.yaml`) | n/a | 20:0xZ |
| — | `sed -n '560,580p' docs/PROTOCOL_DA_PHIEN.md \| cat -n` | dòng 572 (offset 13) chỉ liệt `sensitive`; `systemic` ở dòng 575 | n/a | 20:0xZ, đọc trên `28f32f7c` |

## Những chốt ĐÃ ĐẠT, tái xác nhận độc lập (không lặp lại phép đo cũ, chỉ xác nhận không hồi quy)

| chốt | lượt trước đo | lượt này |
|---|---|---|
| write set đúng 2 tệp | lượt 1/2/3 | không đổi |
| `A9` (N ≥ 73) | 82→85→87 | **87**, khớp lại (bảng đo #2) |
| traversal fail-closed (OUTPUT) | lượt 1 vá, lượt 2/3/4-không-lease xác nhận | tái xác nhận OUTPUT đúng, nhưng phát hiện MẤT phép đo cơ chế (finding mới) |
| `schema_version` hỏng bị chặn | lượt 1 vá, lượt 2 xác nhận | tái xác nhận (t84/t85 trong 87/87) |
| bảng seed chỉ chứa `sensitive` | lượt 3 vá | tái xác nhận độc lập lần thứ hai, mutation-test độc lập lần thứ hai (bảng đo #4) |
| ngoại lệ trần ADR-0044 (328 dòng) | lease `…-2r6` | khớp CHÍNH XÁC, không vượt |

## Còn mở — phải đóng trước khi land

1. **`t88` (hoặc tương đương) chưa vào diff thật** — đề xuất ở trên, đã kiểm chứng đầy đủ trên bản
   sao. Reviewer không tự vá (`attempts_limit: 0` theo lease) — executor quyết định áp hay không.
2. **Biên nhận lượt 3 mồ côi nhánh** — xem finding quy trình ở trên. Không chặn kỹ thuật, nhưng làm
   hồ sơ packet không đầy đủ trên nhánh có thẩm quyền.
3. **`ADR-0045` điều kiện (e) human readback trước land** — lượt 1/2/3 đã khai mở, không có gì mới.
4. **Xác nhận tường minh của `ducthangho` cho việc đảo ngược "chấp nhận nợ `docs/adr/`"** —
   lượt-4-không-lease đã nêu đúng, tôi đồng ý đánh giá rủi ro THẤP (spec bản 5 đã tự settle câu hỏi
   chính sách này, ba lần nguyên văn, và chính bản spec đó đã được `ducthangho` duyệt) nhưng vẫn nên
   xin một dòng xác nhận ngắn trước land, đúng tinh thần "mọi đổi hành vi phải có vết".

## Giới hạn của chính lượt review này — nói thẳng

- **Không chạy lại `workflow_dispatch`/A12/A11** — không có công cụ Actions trong bộ tool của phiên
  reviewer này (xác nhận qua `ToolSearch`). A12 khai theo lời điều phối, có nêu rõ nguồn.
- **Không quét lại toàn bộ 168 ref cho corpus lease lịch sử** (như lượt 3 đã làm, 120 blob) — chỉ
  quét đủ để (a) xác nhận lease review-4 tồn tại, (b) định vị biên nhận lượt 3. Không tái tạo con số
  "120 blob"/"6 lease schema>=2" của lượt 3 — chấp nhận theo lời khai đã có cross-check, không phải
  không làm được, mà vì trọng tâm lượt này là diff + hai câu hỏi L-B.
- **Đánh giá "rủi ro thấp" cho điểm còn mở #4 là suy luận có căn cứ, KHÔNG phải phép đo** (đúng L-A).
- **Không sửa bất cứ gì trong kho thật lẫn nhánh executor.** Mọi đột biến/vá thử chạy trên các bản
  sao cả cây dựng bằng `git archive` trong thư mục scratch riêng của `/tmp`, độc lập với cache của
  điều phối và của lượt-4-không-lease; không ảnh hưởng cây `rv-canon2` đang review.
- **Không xác minh được danh tính "khác phiên soạn đặc tả" bằng cơ chế ngoài lời khai của chính
  phiên này** — không có quyền ghi vào `ops/`, không thấy dấu vết đã soạn đặc tả/lease trong ngữ
  cảnh phiên, nhưng đây vẫn là suy luận từ vắng mặt, không phải một phép đo dương tính.
