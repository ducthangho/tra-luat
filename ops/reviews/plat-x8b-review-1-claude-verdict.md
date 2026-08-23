# VERDICT — cross-review lượt 1 (VÒNG CANON) của `PLAT-X8b` (#255 / PR #263), reviewer `claude`

`reviewed_sha` **`135adf78c1f6175c977ae3439ce27619202dff08`** · `base_sha`
**`1ef928db2a409ea73de5a30f8bd14023c0aca3b1`** · executor `codex` · lease
`plat-x8b-review-1-claude-20260823` (role: reviewer, đã tự kiểm tồn tại — bảng đo #1)

## VERDICT: `approve`

Diff (1 tệp, 10 dòng thêm, `ops/lease_publish_test.py`, ca `t88`) làm đúng những gì đặc tả đòi: khôi
phục phép đo dương tính cho `posixpath.normpath` trong `_tinh_lop_tu_write_set` mà không đụng
`ops/lease_publish.py`, không nới `_BANG_LOP` thật, không sửa `t83`. Đã tự đo lại — không nhận lời
khai của điều phối — cả bốn trạng thái trong bảng của điều phối và thêm một đột biến TINH VI hơn
ngoài bảng đó; tất cả khớp. Có **hai điểm còn mở** trước khi land (xem "Còn mở"), không điểm nào nằm
trong write set của packet.

## Đối chiếu finding gốc (`PLAT-X8` lượt 4: `chuan-hoa-traversal-mat-phep-do-sau-khi-vet-hazard-bi-xoa`)

**`ĐÃ VÁ THẬT`** — tự đo độc lập trên bản sao cả cây, không dùng lại cache của điều phối lẫn của
finding gốc.

- Baseline (`base_sha`, chưa có `t88`): `87/87 rc=0` (bảng đo #3) — khớp "số nền" §0 đặc tả.
- Xoá dòng `posixpath.normpath(duong)`, **chưa** có `t88`: `87/87 rc=0`, **0 ca ĐỎ** (bảng đo #4) —
  tái xác nhận đúng hình dạng lỗ mà finding gốc mô tả: xoá hẳn chuẩn hoá mà suite không phát hiện.
- Có `t88`, mã nguyên vẹn: `88/88 rc=0` (bảng đo #6, cả trong sandbox lẫn bản sao riêng).
- Có `t88` + xoá `normpath`: `87/88 rc=1`, **CHỈ** `t88` đỏ, `t83` vẫn xanh (bảng đo #5) — đúng bằng
  chứng chính: cơ chế bảo vệ nay có phép đo sống, và `t83` xanh một cách vô nghĩa như finding gốc đã
  chỉ ra vẫn đúng (nó không còn đo được gì, `t88` mới là ca đo).
- **Đột biến tinh vi hơn** (ngoài bảng của điều phối, tự nghĩ ra và tự chạy): thay
  `posixpath.normpath(duong)` bằng chuẩn hoá SAI nhưng không rỗng —
  `duong.replace("/../", "/", 1)` (chỉ xoá MỘT lần, không đệ quy) ⇒ vẫn còn `"tam/lop-thap/"` ở đầu
  chuỗi kết quả ⇒ `t88` vẫn bắt được, đỏ đúng (bảng đo #7). Trả lời trực tiếp câu hỏi PROMPT "đột
  biến tinh vi hơn thì sao" bằng phép đo, không chỉ bằng suy luận.
- Không rò giữa các ca: `_nap_cong()` dùng `importlib.util.module_from_spec` + `exec_module`,
  **không** đăng ký `sys.modules` (đọc mã, dòng 117-122) ⇒ mỗi lần gọi là module độc lập. Bằng chứng
  thực nghiệm: suite `88/88` XANH bao gồm cả `t86` (đòi MỌI mục `_BANG_LOP` là `sensitive`) chạy
  ngay sau khi `t88` đã bơm một mục `routine` vào module CỦA RIÊNG NÓ — nếu rò, `t86` phải đỏ.
- Không trùng đường thật: `git ls-tree -r --name-only HEAD | grep "^tam/"` và `grep -i "lop-thap"`
  đều **0 kết quả** (bảng đo #8) — prefix tổng hợp `tam/lop-thap/` không đụng path thật nào trong kho.
- Vế DƯƠNG của nhánh `routine` không phải mã chết: `t81` (không nằm trong diff, đã có sẵn) vẫn gọi
  `_kiem_lop_review` với một mục `routine` bơm tạm và đòi KHÔNG raise — xác nhận
  `_tinh_lop_tu_write_set` còn trả được giá trị khác `sensitive` khi dữ liệu (test) cho phép.

## BẢNG ĐO — `rc` đọc trực tiếp, kể cả cái khớp

| # | lệnh | kết quả | `rc` | ghi chú |
|---|---|---|---|---|
| 1 | `git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ \| grep x8b-review` | `ops/leases/plat-x8b-review-1-claude-20260823.yaml` có mặt | 0 | sau `git fetch` đủ |
| 2 | `git rev-parse HEAD` (cây review) / `git cat-file -e <reviewed_sha>` / `<base_sha>` / `git config core.abbrev` / `git rev-parse --is-shallow-repository` | `135adf78…` · cả hai commit tồn tại · `7` · `false` | 0/0/0/n·a/n·a | sandbox tái lập đúng môi trường cổng theo yêu cầu prompt |
| 3 | `python3 ops/lease_publish_test.py` trên `git archive <base_sha>` (bản sao riêng) | `87/87 đạt, rc=0` | 0 | khớp "số nền" §0 đặc tả |
| 4 | cùng bản sao base, xoá dòng `posixpath.normpath(duong)`, **không** thêm `t88` | `87/87 đạt` — 0 ca ĐỎ | 0 | khớp dòng 2 bảng điều phối |
| 5 | cùng cây `reviewed_sha`, xoá lại `posixpath.normpath(duong)` (bản sao riêng có `t88`) | `87/88 đạt`, CHỈ `t88` đỏ, `t83` xanh | 1 | khớp dòng 4 bảng điều phối |
| 6 | `python3 ops/lease_publish_test.py` trên sandbox (`reviewed_sha`, mã nguyên vẹn) VÀ trên bản sao `git archive` riêng thứ hai | `88/88 đạt, rc=0` cả hai lần | 0 | khớp dòng 3 bảng điều phối; đo 2 lần độc lập |
| 7 | (bản sao có `t88`) thay `posixpath.normpath(duong)` bằng `duong.replace("/../","/",1)` | `87/88 đạt`, CHỈ `t88` đỏ | 1 | **ngoài bảng điều phối** — đột biến tinh vi hơn, tự nghĩ tự chạy |
| 8 | `git ls-tree -r --name-only HEAD \| grep "^tam/"` ; `grep -i "lop-thap"` | rỗng cả hai | n/a | không trùng path thật |
| 9 | `grep -n "_BANG_LOP = (" -A 12 ops/lease_publish.py` | 7 mục, tất cả `"sensitive"` | n/a | không đổi so với finding gốc |
| 10 | `git diff <base_sha> <reviewed_sha> \| diff - diff.patch` (bỏ dòng `index`) | khớp **hoàn toàn** nội dung; chỉ lệch độ dài abbrev blob ở dòng `index` (8 ký tự trong `diff.patch` vs 7 khi tôi tự sinh, do `core.abbrev` môi trường sinh tệp khác sandbox) | n/a | vô hại — không phải nội dung mã, chỉ là artefact hiển thị |
| 11 | `python3 scripts/tl.py doc-claims-check --strict` | `rc=0` | 0 | gate không liên quan diff này vẫn xanh, kiểm cho chắc |
| 12 | `mcp__github__pull_request_read(method=get_check_runs, pullNumber=263)` | **từ chối quyền** ("chưa được cấp") — thử 2 lần | n/a | **KHÔNG ĐO ĐƯỢC** — xem B6 ở mục Còn mở |
| 13 | `git show origin/master:ops/specs/plat-x8b.md` | không tồn tại | 128 | xem finding QUY TRÌNH bên dưới |
| 14 | `git show origin/ops/cap-lease-plat-x8-2:ops/specs/plat-x8b.md \| sha256sum` | khớp đúng `spec_sha256_required` | 0 | đặc tả CÓ tồn tại, chỉ không ở master |
| 15 | `sha256sum PROMPT.md` | khớp `c1a02...` đã khai ở đầu prompt | n/a | mỏ neo prompt hợp lệ |

## Finding QUY TRÌNH mới — `lease-ghi-chu-chep-tu-goi-packet-me-sai-du-lieu` [P2] — không thuộc write set

Tìm được **ngoài** cả 5 hướng "trần" mà prompt liệt kê. Hai trường ghi chú tự do trong chính
`ops/leases/plat-x8b-review-1-claude-20260823.yaml` — `spec_note` và `base_ghi_chu` — chứa dữ liệu
**thuộc packet MẸ** (`PLAT-X8`, PR #248, base `08bb4ecd`), không phải của `PLAT-X8b` (PR #263, base
`1ef928db`), rõ ràng là copy-paste quên sửa số khi soạn lease này từ mẫu lease của packet mẹ.

**Bằng chứng đo được (không suy diễn):**
- `spec_note` viết *"Bản 5 SAU khi vá cross-review lượt 3 của PR #240 ... ĐÃ TRÊN MASTER (merge
  `6675eca4`) — tra ở `master` là thấy"*. Đo trực tiếp: `git show origin/master:ops/specs/plat-x8b.md`
  ⇒ **rc=128, tệp KHÔNG tồn tại trên master** (bảng đo #13). Đặc tả THẬT của `PLAT-X8b` (SPEC.md tôi
  nhận) không hề nhắc "Bản 5"/"PR #240" — nó chỉ ghi "đã duyệt · duyệt bởi ducthangho, 23-08-2026". Đặc
  tả CÓ tồn tại đúng hash neo, nhưng **chỉ** trên `origin/ops/cap-lease-plat-x8-2` (bảng đo #14) —
  đúng nhánh mà chính packet mẹ trong `no_da_khai`/`CLAUDE.md` đã gọi tên là "sổ không nằm một chỗ".
- `base_ghi_chu` viết *"`reviewed_sha_required` là EXACT HEAD của PR #248"* và *"`base_sha` giữ
  `08bb4ecd`"* — nhưng trường `target_pull_request` của CHÍNH lease này là `263`, và trường `base_sha`
  của CHÍNH lease này là `1ef928db` (không phải `08bb4ecd`). Ghi chú tự mâu thuẫn với chính field nó
  đang giải thích.
- Viết một script đo (`check_lease_pr_refs.py`, đính kèm ý tưởng bên dưới) quét mọi chuỗi `PR #N`
  trong lease và so với `target_pull_request`: chạy trên **bản gốc** ⇒ báo lệch ở **3** trường
  (`lop_ghi_chu`→248, `spec_note`→240, `base_ghi_chu`→248), `rc=1`. Đọc tay từng cái: `lop_ghi_chu`
  ("chính cổng mà PR #248 dựng") là **trích dẫn LỊCH SỬ hợp lệ** — PR #248 thật sự là PR đã dựng cơ
  chế `role==reviewer⇒sensitive`/A3/A13 — **KHÔNG phải lỗi**; đây là giới hạn thật của một checker
  máy (không phân biệt được "PR này dựng cơ chế X" với "PR này là danh tính packet"). Còn
  `spec_note`/`base_ghi_chu` là lỗi thật, đã xác nhận độc lập bằng bảng đo #13/#14 ở trên, không chỉ
  bằng checker.
- **Đã thử vá + kiểm chứng trên bản sao** (KHÔNG đụng lease thật — lease đã cấp/tồn tại trên nhánh
  máy chủ, sửa lại sau khi cấp là việc khác, không phải việc của reviewer): viết lại hai trường trên
  bản sao cho đúng dữ liệu `PLAT-X8b` (PR #263, base `1ef928db`, và câu đúng "spec KHÔNG trên master,
  chỉ trên `ops/cap-lease-plat-x8-2`"), chạy lại checker ⇒ chỉ còn đúng 1 dòng lệch
  (`lop_ghi_chu`→248, đã xác nhận là hợp lệ, không phải lỗi) — hai lỗi thật đã biến mất sau khi sửa
  đúng nội dung.

| phần | nội dung |
|---|---|
| **vá ở đâu** | Không phải mã. Trường `spec_note` và `base_ghi_chu` trong `ops/leases/plat-x8b-review-1-claude-20260823.yaml` (đã cấp trên `ops/cap-lease-plat-x8-2`) |
| **vá thế nào** | Thay nội dung nhắc PR #248/#240/`08bb4ecd`/`d85a75d8`/`cd81649c` (toàn bộ thuộc packet mẹ) bằng dữ kiện đúng của `PLAT-X8b`: PR #263, `base_sha=1ef928db` (snapshot master 23-08-2026 00:32Z theo §0 đặc tả), và nói thẳng đặc tả CHỈ tồn tại trên `ops/cap-lease-plat-x8-2`, không trên `master` |
| **ca test khoá nó + đột biến phải chết** | Không phải ca `pytest` — là script `check_lease_pr_refs.py` (viết mới, chạy thật trong `/tmp`, không phải chỉ nghĩ ra): quét chuỗi `PR #\d+` trong mọi giá trị chuỗi của lease, so với `target_pull_request`. Trên bản GỐC: đỏ đúng ở `spec_note`/`base_ghi_chu` (`rc=1`, cộng 1 dòng cần đọc tay để loại vì là trích dẫn lịch sử hợp lệ). Trên bản ĐÃ VÁ (bản sao riêng): hai dòng lỗi biến mất, chỉ còn đúng dòng hợp lệ. Đây LÀ đột biến hai chiều theo đúng yêu cầu lease — **giới hạn thật**: checker không tự phân biệt được trích dẫn lịch sử với lỗi copy-paste, cần người đọc; không đề xuất biến nó thành gate cứng tự động nếu không giải quyết được điểm mù đó trước |
| **bản vá đẻ ra gì** | Rủi ro thấp — chỉ text ghi chú, không đụng trường neo (`spec_path`, `spec_sha256_required`, `base_sha`, `reviewed_sha_required` đều ĐÚNG và đã tự đo khớp, xem bảng đo #2/#14/#15). Rủi ro nếu KHÔNG sửa: người đọc sau tin theo câu "tra ở master là thấy" sẽ không tìm ra đặc tả (đúng lớp lỗi mà `CLAUDE.md` của kho này đã tự ghi là "đã trả giá" — "câu mô tả VỊ TRÍ của một artefact phải đúng ở CẢ HAI phía"), hoặc audit sai `base_sha` khi đối chiếu bằng mắt |

**Không chặn land của packet này** — các trường neo thật (hash/SHA) đều đúng, tôi đã tự đo trực tiếp
độc lập với văn bản ghi chú; đây là nợ vệ sinh quy trình soạn lease, không phải lỗi ảnh hưởng packet.

## Còn mở — phải đóng trước khi land

1. **`B6` (CI cả `ubuntu-latest` lẫn `windows-latest` `success` trên `reviewed_sha`) — KHÔNG ĐO
   ĐƯỢC bởi reviewer.** Không có `gh` CLI trong phiên (xác nhận qua hook đầu phiên: "khong gh"), và
   `mcp__github__pull_request_read(get_check_runs)` bị từ chối quyền hai lần liên tiếp (bảng đo #12).
   Không có `EVIDENCE.md` nào do điều phối cung cấp cho vòng này (khác packet mẹ, nơi có
   `A12-EVIDENCE.md`) — nên đây không phải "đã có bằng chứng nơi khác", mà thật sự là khoảng trống
   đo lường. **Điều phối phải tự đo B6 bằng công cụ Actions trước khi coi packet đủ điều kiện land**,
   đọc **THEO JOB** như đặc tả đòi (`"PR xanh" không đủ` — đúng câu SPEC.md B6 tự cảnh báo).
2. **Finding QUY TRÌNH `lease-ghi-chu-chep-tu-goi-packet-me-sai-du-lieu` (P2)** ở trên — không chặn
   kỹ thuật, nhưng nên có một dòng xác nhận/sửa quy trình trước khi lấy lease này làm mẫu cho lease
   tiếp theo (nó sẽ bị copy-paste tiếp nếu không ai sửa).

## Giới hạn của chính lượt review này — nói thẳng

- **Không đo được B6 (CI theo job)** — thiếu quyền công cụ, đã nêu ở trên. Đây là giới hạn CÔNG CỤ
  của phiên, không phải tôi bỏ qua.
- **`check_lease_pr_refs.py` là heuristic tôi viết trong phiên này, không phải công cụ đã qua review
  riêng** — nó có false positive đã xác nhận tay (`lop_ghi_chu`). Không đề xuất đưa thẳng vào gate mà
  không xử lý điểm mù "trích dẫn lịch sử vs. copy-paste nhầm" trước, đúng bài học `CLAUDE.md`
  "công cụ nháp của chính mình dễ tin nhất, nên nguy nhất" — tôi tự đọc tay để loại false positive
  thay vì tin thẳng số ra từ script.
- **Không xác minh được danh tính "khác phiên soạn đặc tả/prompt/lease" bằng cơ chế ngoài lời khai
  của chính phiên này** — không có quyền ghi `ops/`, không thấy dấu vết đã soạn đặc tả trong ngữ cảnh
  phiên, nhưng đây là suy luận từ vắng mặt, không phải phép đo dương tính (đúng cảnh báo `nguoi_review_phai_khac_phien_ghi_chu` của lease).
- **Không chạm cây review thật lẫn nhánh executor.** Mọi đột biến/vá thử chạy trên bản sao cả cây
  dựng bằng `git archive` trong `/tmp`, tách biệt hoàn toàn khỏi `rv-x8b` đang review và khỏi lease
  thật trên `ops/cap-lease-plat-x8-2`.
- **Không quét lại toàn bộ ref cho corpus lease lịch sử** ngoài phạm vi cần để định vị đặc tả
  `plat-x8b.md` — trọng tâm lượt này là diff + finding gốc + hai trường ghi chú mới phát hiện.
- Chưa tự khai `cross_approved` đầy đủ theo receipt v2 (đòi receipt ID + hai danh tính chứng thực độc
  lập) — đó là việc của điều phối SAU verdict này, không phải của reviewer. Mức đo được: review
  cross-provider (`codex` thi công · `claude` review) có lease reviewer hợp lệ, khác phiên soạn đặc
  tả (theo suy luận từ vắng mặt ở trên), chạy trong cây rời không sửa kho thật — thoả các điều kiện
  MÁY ĐO ĐƯỢC của mục tiêu, nhưng KHÔNG tự nhận đã đạt đủ `cross_approved`.
