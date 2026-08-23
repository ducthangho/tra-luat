verdict: changes_requested
reviewed_sha: 13e3a9cfdac763a317252e68fa91571fee942bd0
packet: LEASE-HOI-TOAN-KHO (#244), PR #275, lease r2 (`lease-hoi-toan-kho-exec-1r2-codex-20260823`)
reviewer: claude (cross-review, nền khác executor `codex`)

Không có lượt review trước để đối chiếu: lease r1 (`lease-hoi-toan-kho-exec-1-claude-20260823`,
executor claude/reviewer codex) chỉ cấp lease rồi bị reroute (đảo vai) TRƯỚC khi sinh diff nào —
`git log --all` không có commit thi công nào trên nhánh r1, không có verdict/receipt nào trong
`ops/reviews/` mang tên packet này. Mục `ĐỐI CHIẾU LƯỢT TRƯỚC` của PROTOCOL §8 không áp dụng vì
chưa có lượt trước có nội dung để đối chiếu.

## BẢNG ĐO

Mọi số đo lại chạy trực tiếp trong `cay-kho/` (mirror git đầy đủ, `core.abbrev=7`, không nông,
`git rev-parse --is-shallow-repository` = `false`), không suy từ lời khai.

| khẳng định | PR/EVIDENCE khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| sha256 `SPEC.md` | `ffca019e…5da87` | `sha256sum SPEC.md` → **khớp từng ký tự** | ✅ |
| cổng chính tại `reviewed_sha` | `93/94 đạt, đã chạy=94, bỏ qua=0` | `python3 ops/lease_publish_test.py` → `93/94 đạt; đã chạy=94, bỏ qua=0`, đỏ duy nhất `t33` (thiếu `actionlint`) | ✅ |
| cổng chính tại `base_sha` (`8222c101`) | `87/88 đạt, đã chạy=88, bỏ qua=0` | checkout `8222c101` vào bản sao riêng, chạy lại → `87/88 đạt; đã chạy=88, bỏ qua=0`, cùng `t33` đỏ | ✅ |
| delta | `+6 ca, 0 hồi quy` | 94−88=6 ca mới, 93−87=6 ca đạt mới, không ca nào khác đổi màu | ✅ |
| `doc-claims-check --strict` | `rc=0` | `python3 scripts/tl.py doc-claims-check --strict` → `rc=0` | ✅ |
| numstat | `ops/lease_publish.py +151/-0`, `ops/lease_publish_test.py +135/-0` (286 dòng, 2 tệp) | `git diff --numstat 8222c101 13e3a9c` → **khớp từng số**, `diff` với `numstat.txt` rỗng | ✅ |
| nội dung `diff.patch` | (đại diện cho thay đổi) | `diff diff.patch <(git diff 8222c101 13e3a9c)` → **rỗng** (byte-khớp) | ✅ |
| trần ADR-0044 (`sensitive`: ≤3 tệp/≤300 dòng thêm) | không vượt | 2 tệp ≤ 3, 286 dòng ≤ 300 | ✅ trong trần |
| `write_set` (LEASE.yaml) = diff thật | `ops/lease_publish.py`, `ops/lease_publish_test.py` | hai tệp trong diff **đúng bằng** hai đường dẫn trong `write_set`, không thừa không thiếu | ✅ |
| đột biến mã sản phẩm `t94` (yêu cầu M4/`A8`) | "đã chạy=10, bị giết=10" (ngụ ý trong test) | chạy trực tiếp → `đột biến mã sản phẩm: đã chạy=10, bị giết=10` | ✅ |
| `ai-dang-giu ops/lease_publish.py` trên KHO THẬT (không phải fixture) | *(không có trong EVIDENCE — PROMPT.md nêu ví dụ `NGƯỜI_GIỮ 6`)* | chạy lệnh thật trên mirror với `origin` = bare clone cục bộ → **`NGƯỜI_GIỮ 6`** đúng, danh sách gồm cả lease của chính packet này (`lease-hoi-toan-kho-exec-1r2-codex-20260823`) và loại đúng `lease-hoi-toan-kho-exec-1-claude-20260823` (đã bị thay thế, vẫn được in kèm nhãn) | ✅ khớp con số ví dụ, và hành vi A2c đúng trên dữ liệu THẬT chứ không chỉ fixture |
| `ai-dang-giu ops/lease_publish_test.py` trên kho thật | *(không khai)* | `NGƯỜI_GIỮ 7` (đo được, không có gì để đối chiếu) | — ghi nhận, không có lời khai để so |
| EVIDENCE mục "Ref" (177/177, `comm` hai chiều rỗng) | đo trên **máy chủ thật** trước khi clone | **KHÔNG ĐO ĐƯỢC từ sandbox này** — `origin` trong `cay-kho/` là bare mirror cục bộ (`kho.git`), không phải GitHub; EVIDENCE tự khai đúng giới hạn này, không phải một chỗ hổng | ⚠️ không tái lập được, nhưng đã tự khai đúng — không phải finding |
| `plat-x8-exec-2r6-codex-20260822` vẫn `CÒN_HẠN`, giữ đúng cả hai tệp write_set | LEASE.yaml khai "PLAT-X8 quyền ghi ĐÃ TIÊU" (hiện vật trên master, không phải nhãn) | xác nhận: expiry `2026-08-23T14:10:00Z` > giờ hệ thống lúc đo (`2026-08-23T07:25Z`) → đúng là `CÒN_HẠN` theo đồng hồ, và đây CHÍNH LÀ giới hạn đã tự khai trong `SPEC.md/chua_do_duoc#4` ("đã tiêu" không tự khai được từ trường lease) — không phải bug, `ngoai_pham_vi` loại trừ cơ chế thu hồi khỏi packet này | ✅ hành vi đúng như spec dự liệu, không phải finding mới |

## BẢNG ĐỘT BIẾN

10 đột biến bắt buộc của `A8` (do executor viết trong `t94`) đã tự chạy lại, xác nhận `10/10` bị
giết. Phần dưới là đột biến **TÔI tự dựng, độc lập với `t94`**, áp vào bản sao `ops/lease_publish.py`
trong sandbox, chạy lại TOÀN BỘ `ops/lease_publish_test.py` (không chỉ vòng lặp nội bộ của `t94`) để
xem có ca nào — bất kỳ đâu trong 94 ca — bắt được không.

| đột biến (độc lập, tôi dựng) | ca đáng lẽ đỏ | kết quả trên 94 ca gốc | sống sót? |
|---|---|---|---|
| `_git()`: rc≠0 → `return ""` thay vì `raise Chan(KHÔNG_XÁC_ĐỊNH,…)` | (không có — đây chính là lỗ) | `93/94`, không ca nào mới đỏ | **SỐNG SÓT** → finding `git-loi-nuot-thanh-thanh-cong` |
| `_lease_cham_duong`: so `duong in x` thay vì `x == duong` | (không có — đây chính là lỗ) | `93/94`, không ca nào mới đỏ | **SỐNG SÓT** → finding `lease-cham-duong-khop-chua-khong-phai-bang` |
| `_phan_loai_lease`: biên `han <= bay_gio` → `han < bay_gio` (đổi hướng đúng lúc hết hạn) | (không có ca chạm biên) | `93/94`, không ca nào mới đỏ (chỉ `t94` tự báo "neo không duy nhất" vì nó đọc lại đúng dòng này) | **SỐNG SÓT** → finding nhỏ, biên hiếm gặp |
| `_quet_lease_toan_kho`: YAML hỏng → `except Exception: continue` (nuốt lỗi ở tầng YAML) | `A2` | `t90_A2_yaml_hong_fail_close` đỏ | bị giết — đối chứng dương, xác nhận `A2` có răng thật |
| M2: `thieu = _ten_nhanh_may_chu(goc) - ten_cuc_bo` → so **đếm** (`len(sv) > len(ten_cuc_bo)`) thay vì **tập** | `A6` (lực lượng bằng nhau, tên khác nhau) | `t92_A3_A4_A5_A6…` đỏ đúng dòng "ref máy chủ thiếu cục bộ vẫn qua" | bị giết — xác nhận tuyên bố của `SPEC.md` rằng chỉ `A6` giết được kiểu đột biến "so bằng `wc -l`" là ĐÚNG, đã tự đo lại chứ không nhận lời khai |
| `lenh_ai_dang_giu`: bọc dòng `print(...)` trong `if not da_chet:` (ẩn hẳn lease đã-bị-thay-thế khỏi đầu ra, khác với đột biến `print("")` toàn cục của `t94`) | `A2c` | `t91_A2c_…` đỏ | bị giết — xác nhận `A2c` có răng ở đúng biến thể "loại khỏi đầu ra", không chỉ biến thể thô của `t94` |
| `_kiem_dau_toan_kho` chạy trên kho KHÔNG có remote `origin` | (kiểm robustness) | `rc=12 KHÔNG_XÁC_ĐỊNH`, không phải `rc=0` | fail-close đúng, không phải đột biến sống sót — ghi nhận tích cực |
| `ai-dang-giu` chạy trên thư mục không phải git repo | (kiểm robustness) | `rc=12 KHÔNG_XÁC_ĐỊNH` | fail-close đúng, ghi nhận tích cực |

**Hai đột biến sống sót đầu tiên đã được viết thành ca test chạy được** (`t95`, `t96` trong
`goi-va/ops/lease_publish_test.py`) và tự kiểm hai chiều: PASS trên mã gốc (95/96, chỉ `t33` đỏ),
ĐỎ đúng khi áp lại chính đột biến đã phát hiện ra chúng — xem file đó để có bằng chứng chạy được,
không chỉ mô tả.

### git-loi-nuot-thanh-thanh-cong  [P1]  `_git()` không có ca nào kiểm nhánh fail-close khi lệnh git thật sự thất bại
TỆP/DÒNG: `ops/lease_publish.py:234-243` (hàm `_git`)
VẤN ĐỀ: Toàn bộ M1/M2/M3 (`_ten_nhanh_may_chu`, `_cac_ref_cuc_bo`, `_quet_lease_toan_kho`,
`_kiem_dau_toan_kho`) đi qua đúng MỘT điểm gọi git: `_git()`. Nhánh `if p.returncode != 0: raise
Chan(RC_KHONG_XAC_DINH, …)` — tức chính "trạng thái thứ ba" mà cả gói này được sinh ra để cưỡng
chế — **không có ca nào trong 94 ca kiểm tra** khiến `GOI_GIT` trả về `returncode != 0` cho một lệnh
mà sản phẩm THẬT SỰ gọi (`ls-remote`, `for-each-ref`, `ls-tree`, `cat-file -p`, `rev-parse
--git-dir`). Lớp giả `_GitKhoGia` trong `t89`–`t93` có một nhánh `else` trả `rc=1` (dòng ~2926),
nhưng nhánh đó chỉ chạm khi sản phẩm gọi một sub-lệnh KHÔNG nằm trong 5 mẫu đã biết — sản phẩm
không bao giờ làm vậy, nên nhánh giả đó CHẾT (không bao giờ được thực thi bởi bất kỳ đường gọi
thật nào). Đổi `_git()` để nuốt lỗi (`return ""` thay vì `raise`) khiến `93/94` giữ nguyên — 0 ca
đổi màu.
Hậu quả nếu bug này (hoặc một biến thể của nó) từng lọt vào sản phẩm thật: `ls-remote` thất bại
(mạng đứt, quyền credential hết hạn, repo hỏng) sẽ khiến `_ten_nhanh_may_chu` trả **tập rỗng** thay
vì chặn; `_quet_lease_toan_kho` đọc tập rỗng đó thành "máy chủ không có nhánh nào" ⇒ `thieu = {} -
ten_cuc_bo = {}` ⇒ KHÔNG báo `KHÔNG_XÁC_ĐỊNH` ⇒ M2 (phép so hai nguồn — chốt ĐẦU TIÊN theo đúng lời
dặn trong `CLAUDE.md`: *"khi viết `ai-dang-giu`, phép so này phải là chốt ĐẦU TIÊN"*) im lặng bỏ
qua chính lỗi mà nó được thiết kế để bắt. Đây là đúng hình dạng "gộp KHÔNG_XÁC_ĐỊNH vào coi-như-sạch"
mà packet này và toàn bộ lịch sử `CLAUDE.md` (mục *"ba trạng thái, không phải hai"*, *"cổng vắng mặt
trông giống cổng xanh"*) liên tục cảnh báo — chỉ khác là lần này ở TẦNG GIT-WRAPPER, chưa từng được
soi tới vì mọi ca đều giả định lệnh git luôn thành công.
ĐÃ THỬ VÁ: có — thêm `t95_git_that_bai_phai_fail_close_khong_duoc_nuot_loi` vào
`goi-va/ops/lease_publish_test.py`. Test thay `mod.GOI_GIT` bằng một hàm giả luôn trả
`CompletedProcess(rc=128)`, xác nhận `_git()` ném đúng `Chan(RC_KHONG_XAC_DINH, …)`, và lan tới
`_ten_nhanh_may_chu` để xác nhận lỗi không bị nuốt thành tập rỗng.
ĐÃ THỬ NGHIỆM: (1) chạy `t95` trên mã gốc trong bản sao sandbox → PASS (95/96, chỉ `t33` đỏ do
thiếu `actionlint` — không liên quan). (2) Áp đúng đột biến "return \"\" thay vì raise" vào bản sao
→ chạy lại → `t95` ĐỎ với thông điệp `"_git() coi rc != 0 là thành công"`. Cả hai lệnh chạy thật
trong `/tmp/.../scratchpad/verify1` (bên trong sandbox), không suy diễn.
ĐỘ TIN: cao — mutation dựng thủ công, chạy độc lập hai lần (trước/sau vá), kết quả tái lập được.

### lease-cham-duong-khop-chua-khong-phai-bang  [P2]  Phép nối lease↔đường-dẫn của M1 không có ca nào đòi SO BẰNG tuyệt đối
TỆP/DÒNG: `ops/lease_publish.py:314-317` (hàm `_lease_cham_duong`)
VẤN ĐỀ: Đây là hàm quyết định TẬP NGƯỜI GIỮ của `M1` được tính từ đâu — mọi lease trong
`_quet_lease_toan_kho` được lọc qua `_lease_cham_duong(lease, a.duong_dan)` trước khi vào bảng
phân loại. Không ca nào trong `t89`–`t94` bơm một cặp đường dẫn CHỒNG LẤN (một là tiền tố/chuỗi con
của cái kia nhưng không bằng nhau) để buộc phép so phải là `==` chứ không phải `in`. Đổi dòng so
sánh từ `x.strip().removeprefix("planned:") == duong` sang `duong in x.strip().removeprefix
("planned:")` khiến `93/94` giữ nguyên.
Hai chiều lỗi có thể xảy ra tùy ai gõ nhầm hướng: (a) một lease khai `write_set: [ops/lease_publish
.py.bak]` sẽ bị tính là ĐANG GIỮ `ops/lease_publish.py` dù nó không hề khai đường dẫn đó — mở rộng
tập người giữ, tức BÁO ĐỘNG GIẢ (an toàn hơn nhưng sai); (b) nếu ai đó gõ ngược chiều so sánh, một
lease khai chính xác `ops/lease_publish.py` có thể bị BỎ SÓT khi hỏi một đường dẫn ngắn hơn là tiền
tố của nó — đây mới là hướng nguy hiểm (bỏ sót người giữ thật). Mã hiện tại dùng `==` nên KHÔNG có
lỗi này hôm nay; đây thuần là lỗ COVERAGE khiến một lượt sửa sau (vô tình nới `==` thành `in` để "linh
hoạt hơn", đúng kiểu lý do đã từng xảy ra ở nợ `distinguishes spelling, not authority` ghi trong
`CLAUDE.md`) sẽ lọt sạch qua cổng.
ĐÃ THỬ VÁ: có — thêm `t96_lease_cham_duong_khop_tuyet_doi_khong_phai_chua`, bơm CẢ HAI chiều overlap
(mục `write_set` dài hơn nhận `duong` làm tiền tố, và mục ngắn hơn là tiền tố của `duong`), cộng hai
ca đối chứng dương (khớp đúng nghĩa, có và không tiền tố `planned:`, vẫn phải qua).
ĐÃ THỬ NGHIỆM: chạy trên mã gốc → PASS. Áp đột biến `in` thay `==` → `t96` ĐỎ đúng ở chiều "write_set
dài hơn nhận `duong` làm tiền tố vẫn bị coi là khớp". Chạy thật trong
`/tmp/.../scratchpad/verify2`.
ĐỘ TIN: cao.

### phan-loai-lease-bien-het-han  [P3]  Biên đúng lúc hết hạn (`<=` so với `<`) không có ca nào chạm
TỆP/DÒNG: `ops/lease_publish.py:326` (`_phan_loai_lease`)
VẤN ĐỀ: `return "HẾT_HẠN" if han <= bay_gio else "CÒN_HẠN"`. Đổi `<=` thành `<` khiến `93/94` giữ
nguyên vì mọi fixture dùng ngày rất xa quá khứ/tương lai (`mai_sau()`/`khi_truoc()` lệch 4 giờ),
không ca nào đặt `lease_expires_at_utc` đúng bằng thời điểm chạy. Hướng sai của đột biến này là MỞ
RỘNG tập còn hạn (một lease hết hạn đúng lúc `bay_gio` sẽ bị tính là `CÒN_HẠN`) — đúng chiều fail-
OPEN, dù mức độ rủi ro thực tế rất thấp vì `datetime.now()` trùng khớp centi-giây với một mốc ghi
sẵn trong YAML gần như không xảy ra tự nhiên; đáng chú ý chỉ vì đây LÀ dòng biên duy nhất trong toàn
bộ ba trạng thái không có ca kiểm biên.
ĐÃ THỬ VÁ: không — mức độ thấp, để executor cân nhắc có đáng thêm một ca cố định `bay_gio` truyền
tay hay không (hàm `_phan_loai_lease` đã nhận tham số `bay_gio=None` sẵn cho việc này, chỉ cần một
test set `bay_gio` bằng đúng `lease_expires_at_utc` đã parse).
ĐÃ THỬ NGHIỆM: áp `<=`→`<` vào bản sao, chạy lại toàn bộ 94 ca gốc → `93/94`, không ca nào mới đỏ
(bản thân `t94` tự báo "neo mutant A2b-co không duy nhất" vì nó đọc lại đúng dòng nguồn đã bị đổi —
đó là tác dụng phụ của cách `t94` tự kiểm neo trên tệp đang chạy, không phải một ca độc lập bắt được
đột biến).
ĐỘ TIN: vừa — lỗ có thật nhưng bề mặt tấn công thực tế gần như bằng không.

## Ghi nhận không phải finding (đã đo, khớp/đúng như kỳ vọng)

- Toàn bộ 10 đột biến bắt buộc của `A1`–`A7` (biến thể trong `t94`) đã tự chạy lại và bị giết
  `10/10` — khớp lời khai của test, không cần tin test tự báo cáo về chính nó.
- `ai-dang-giu` chạy TRÊN DỮ LIỆU THẬT (không phải fixture) cho kết quả nhất quán với thiết kế:
  loại đúng `ĐÃ_BỊ_THAY_THẾ` khỏi `NGƯỜI_GIỮ` nhưng vẫn in ra kèm nhãn (đúng `A2c`); fail-close đúng
  khi thiếu `.git` hoặc thiếu remote `origin` (`rc=12`, không phải `rc=0`).
- Phạm vi: diff nằm ĐÚNG trong `write_set`, không vượt trần ADR-0044 (2 tệp/286 dòng ≤ 3 tệp/300
  dòng), không tệp nào khác bị chạm.
- `A6` (so tập tên, không phải đếm) có răng thật khi tôi tự dựng lại đột biến "so bằng đếm" theo
  đúng gợi ý trong PROMPT — không nhận lời khai của `SPEC.md` rằng nó đúng, đã tự đo.

## Điều kiện dừng chưa thoả (không phải lỗi code, nhưng chặn LAND)

`LEASE.yaml.ngoai_le_ADR_0045.ba_dieu_kien_ADR_0045.human_readback_truoc_land` ghi **BẮT BUỘC —
CHƯA làm**. Cùng `dieu_kien_dung`: *"Chưa có human readback của chủ kho ⇒ KHÔNG land"*. Verdict này
không thay thế điều kiện đó — dù tôi approve/changes_requested, packet vẫn KHÔNG được land tới khi
chủ kho tự đọc lại diff ở `reviewed_sha` này.

## Kết luận

Hai finding P1/P2 là lỗ COVERAGE trong `ops/lease_publish_test.py` (nằm trong `write_set`, không
cần lease mở rộng để vá), không phải lỗi hành vi của `ops/lease_publish.py` hôm nay — mã sản phẩm
hiện đúng ở cả hai chỗ. Nhưng đúng tinh thần PROTOCOL §8 ("đột biến sống sót = finding") và đúng
mục đích của chính packet này (đóng lỗ fail-open kiểu "gộp trạng thái thứ ba vào coi-như-sạch"), hai
lỗ này nằm ngay trên đường mà toàn bộ M1/M2/M3 phụ thuộc (mọi lời gọi git đi qua `_git()`; mọi phép
lọc "ai giữ đường dẫn X" đi qua `_lease_cham_duong()`) nên đề nghị vá trước khi land, không phải sau.
Patch gợi ý (`t95`, `t96`) đã viết, tự kiểm hai chiều, đặt tại `goi-va/ops/lease_publish_test.py` —
chưa chạy trên cây thật, executor tự áp, tự đo, tự chịu trách nhiệm commit (đúng ràng buộc PROTOCOL
§8/§13 cho patch-as-hint dạng tệp test thuần).
