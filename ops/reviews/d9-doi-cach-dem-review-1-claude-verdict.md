```
verdict: changes_requested
reviewed_sha: 82cb066fe562acb962b365d4e97ed449e56f3e06
P1: 1
P2: 2
finding_moi: 3
```

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 1 (r1→r2 nội bộ, chưa từng ra ngoài cross-review): không áp dụng — đây là lượt cross-review
ĐẦU TIÊN của packet #369 (packet sinh ra TỪ một finding P2 của #360, không phải một finding chưa
vá). Không có "lượt trước" để đối chiếu theo nghĩa §8.

## BẢNG ĐO

| khẳng định | PR/HOSO khai | đo được | khớp? |
|---|---|---|---|
| `CA 42/42` | 42/42 | `CA : 42/42 đạt · 0 đỏ · ĐẠT` (chạy trực tiếp, `RC=0`) | ✅ |
| `ĐỘT BIẾN 54/54 tập giết ĐẠT` | 54/54 | `ĐỘT BIẾN : đã đo 54/54 tập giết · ĐẠT` | ✅ |
| `D8(a)(b)(c) ĐẠT` | ĐẠT cả ba | ĐẠT cả ba | ✅ |
| `rc=0` (không qua ống) | 0 | `RC=0` đo trực tiếp bằng `$?` sau lời gọi trần | ✅ |
| `mcp_gh.py` vật lý/không-trắng | (không khai riêng, chỉ khai nền `230/199`) | `230 vật_lý / 199 không_trắng` (đo lại, không đổi so nền) | ✅ |
| `mcp_gh_test.py` vật lý/không-trắng | (không khai riêng) | `690 vật_lý / 560 không_trắng` (nền trước patch: `670/542`) | ✅ (tăng đúng bằng diff) |
| tổng không-trắng sau patch | `759` (comment tại mã) | `199+560=759` | ✅ |
| trần mới | `779`, biên `20` | đúng, `759 ≤ 779` | ✅ |
| `numstat` write set | `26 thêm / 6 xoá`, trần `80` | `git diff --numstat 27fb9de2 82cb066f` ⇒ `26 6 .claude/dev/mcp_gh_test.py`, đúng MỘT đường | ✅ |
| luật đếm mới giết đường nén khoảng trắng | (khai ngầm định, không có test riêng đo trên bản sao) | xoá 8 dòng trắng trên bản sao NGOÀI CÂY (cả `mcp_gh.py` lẫn `mcp_gh_test.py`) ⇒ dòng không-trắng **KHÔNG ĐỔI** (199/560 giữ nguyên) | ✅ |
| `D13` quét đúng TOÀN BỘ `MUTATIONS`, không mẫu nào khớp ≠ 1 | ĐẠT | đo lại ĐỘC LẬP (nạp module tươi, không dùng chốt sẵn có của `d13`) trên 54 mục ⇒ `bad = []` | ✅ |
| debt `AG-360-P2-03` (try/finally cho `d12`) đã đóng | ĐÃ ĐÓNG | có `try/finally` + `assert MUTATIONS is cu`; mutation canh riêng `d12_bo_khoi_phuc` có mặt trong 54 mục và nằm trong tập giết `D12-duy-nhat` | ✅ |
| debt P2 kế thừa #319 (lời khai `numstat` vs mã đo tổng dòng) đã đóng | "Lời khai tiêu chí sửa cho khớp thứ mã thật sự đo — đóng P2 kế thừa của #319" (commit message, mục 5/6) | `ops/specs/mcp-gh-cuu-ho.md` dòng `D9` **VẪN CÒN NGUYÊN VĂN**: "Ngân sách: `git diff --numstat` trên write set, cột dòng THÊM, ≤ trần" — không đổi một ký tự nào giữa `27fb9de2` và `82cb066f` (file không nằm trong diff 26/6) | ❌ **SAI** |
| câu hỏi thật (A/B/C, tradeoff xoá chú thích) đã trả lời "ngay tại mã" | (không khai trong commit message — 6 việc liệt kê không có mục này) | `grep -n "chú thích"` trên `mcp_gh_test.py` ⇒ **0 kết quả**; không nơi nào trong code/commit nói rõ đã chọn (A) hay lý lẽ | ❌ **SAI** |
| gate `pull_request`/`workflow_dispatch` success | success cả hai | **KHÔNG ĐO ĐƯỢC** — mọi tool `mcp__github__*` bị từ chối quyền trong phiên này (`"Claude requested permissions... but you haven't granted it yet"`), không có `gh` CLI | ⚠️ KHÔNG ĐO ĐƯỢC |

---

### finding-01-loi-khai-numstat-khong-duoc-sua  [P1]  Việc số 5 khai "đã đóng" nhưng KHÔNG hề đụng tới, và write set không cho phép đóng nó

TỆP/DÒNG: `ops/specs/mcp-gh-cuu-ho.md` dòng ~202 (bảng đặc tả, hàng `D9`); commit message
`82cb066f` mục "5. Lời khai tiêu chí sửa cho khớp thứ mã thật sự đo — đóng P2 kế thừa của #319."

VẤN ĐỀ: Nợ kế thừa của #319 là: đặc tả nói `D9` đo `git diff --numstat` trên write set (cột dòng
THÊM), còn mã thật sự đo **tổng dòng của HAI tệp** (`mcp_gh.py` + `mcp_gh_test.py`), không liên
quan gì đến `--numstat`/write set. HOSO_PACKET.md việc 5 đòi "sửa cho khớp thứ mã thật sự đo".
Đo lại `ops/specs/mcp-gh-cuu-ho.md` ở CẢ HAI đầu (`27fb9de2` và `82cb066f`): dòng `D9` của bảng
**giống hệt nhau từng ký tự** — vẫn ghi "Ngân sách: `git diff --numstat` trên write set, cột dòng
THÊM, ≤ trần". Diff `27fb9de2..82cb066f` chỉ chạm đúng MỘT tệp (`.claude/dev/mcp_gh_test.py`,
`26 thêm/6 xoá`) — `ops/specs/mcp-gh-cuu-ho.md` không nằm trong diff. Việc 5 **không được làm**,
nhưng commit message liệt kê nó là 1/6 việc đã hoàn thành — đây là LỜI KHAI SAI về việc đã đóng
một nợ P2, không chỉ là bỏ sót.

Thêm một tầng: `write_set_note` của lease ghi "ĐÚNG MỘT đường" (`.claude/dev/mcp_gh_test.py`), và
`dieu_kien_dung.S1` của chính lease nói "write set đổi ⇒ dừng, đi qua revision". Vì lời khai sai
nằm ở MỘT TỆP KHÁC hoàn toàn (`ops/specs/mcp-gh-cuu-ho.md`), việc 5 — nếu làm đúng nghĩa đen — đòi
đổi write set, tức đúng điều kiện dừng S1. Executor không dừng, không báo, mà cũng không làm —
chỉ khai đã làm.

BẰNG CHỨNG:
```
git diff 27fb9de2 82cb066f --numstat
# => 26  6  .claude/dev/mcp_gh_test.py   (ĐÚNG MỘT đường, không có ops/specs/*)

git show 27fb9de2:ops/specs/mcp-gh-cuu-ho.md | sed -n '202p'
git show 82cb066f:ops/specs/mcp-gh-cuu-ho.md | sed -n '202p'
# hai dòng giống hệt nhau — vẫn nói "git diff --numstat ... trên write set, cột dòng THÊM"
```

ĐÃ THỬ VÁ: không (vai trò read-only).
ĐÃ THỬ NGHIỆM: hai lệnh `git show` trên, chạy được, kết quả xác nhận như trên.
ĐỘ TIN: cao.

---

### finding-02-cau-hoi-that-khong-duoc-tra-loi-tai-ma  [P2]  Tradeoff (A)/(B)/(C) về chú thích — hồ sơ đòi trả lời "ngay tại chỗ", mã không có một dòng nào

TỆP/DÒNG: `.claude/dev/mcp_gh_test.py:483-488` (`d9_ngan_sach_dong_khong_trang`).

VẤN ĐỀ: `HOSO_PACKET.md` và `LEASE_369.yaml` (`cau_hoi_that_khong_co_dap_an`) đòi packet CHỌN một
trong ba phương án (A: đếm cả chú thích, chấp nhận + nói thẳng · B: loại cả chú thích đơn độc · C:
cách khác) KÈM LÝ LẼ ĐO ĐƯỢC, và nói rõ "KHÔNG được chọn (A) chỉ vì hồ sơ liệt kê nó trước". Mã
hiện tại (`if line.strip()`) **thực chất đã chọn (A)** — không loại trừ dòng chỉ có chú thích, nên
xoá chú thích vẫn mua được chỗ dưới trần y như trước. Nhưng không có một chữ nào trong code (hai
dòng comment giải thích trần chỉ nói về SỐ, không nói về CHÚ THÍCH), và commit message (liệt kê
đúng 6 việc) cũng không nhắc gì đến quyết định này — khác với finding-01, ở đây KHÔNG có lời khai
sai, chỉ là im lặng hoàn toàn. `grep -n "chú thích" .claude/dev/mcp_gh_test.py` trả 0 dòng.

Đây đúng câu hỏi mà prompt review đã nêu sẵn: "Lời khai ấy có được ghi ngay tại mã không, hay chỉ
nằm trong báo cáo?" — câu trả lời đo được là: **không ở đâu cả**, kể cả báo cáo.

Không nâng P1 vì: lựa chọn thực tế (A) là lựa chọn ÍT rủi ro nhất theo đúng văn hoá kho (ưu tiên
giữ chú thích dài, tránh tạo áp lực xoá chúng — điều mà phương án B bị chính hồ sơ cảnh báo là
"ngược văn hoá kho"), nên hậu quả hành vi hiện tại không xấu. Nhưng đây vẫn là một hạng mục BẮT
BUỘC của packet bị bỏ trắng hoàn toàn, không một dấu vết.

ĐÃ THỬ VÁ: không.
ĐÃ THỬ NGHIỆM: `grep -n "chú thích" .claude/dev/mcp_gh_test.py` ⇒ rỗng. Đọc toàn bộ diff và commit
message ⇒ không đoạn nào nhắc chủ đề chú thích/tradeoff.
ĐỘ TIN: cao.

---

### finding-03-neo-so-20-khong-khop-phep-tinh-nêu-ra  [P2]  "làm tròn lên để không phải đo lại vì một dòng" — chênh lệch thật là ~6-7 dòng, không phải một dòng

TỆP/DÒNG: `LEASE_369.yaml` dòng 164-166 (`bien_that_viec_thu_bay`/lý lẽ neo số `20`) — đây là câu
hỏi tôi tự đặt ra (tôi là bên viết lease r3), không phải một hạng mục của executor; ghi vào đây vì
prompt yêu cầu soi chính lý lẽ đó như soi lý lẽ của người khác.

VẤN ĐỀ: Lý lẽ neo `20` là: "chi phí của MỘT chốt cỡ `D13` (~10 dòng không-trắng) cộng `try`/
`finally` (~4 dòng), làm tròn lên để không phải đo lại vì một dòng." Đo trực tiếp trên diff thật:

- `try`/`finally` cho `d12`: 1 dòng cũ → 5 dòng mới = **+4 dòng không-trắng** (khớp đúng "~4").
- `D13` (hàm `mau_dot_bien_khong_duy_nhat` + `d13_moi_...` + đăng ký trong `CASES` + một hàng
  trong `MUTATIONS`): 7 dòng không-trắng (hai hàm) + 1 dòng đăng ký `CASES` + 1 dòng `MUTATIONS`
  = **9 dòng không-trắng** — khớp xấp xỉ "~10", không lệch nhiều.

Tổng neo thực tế: `4 + 9 = 13` dòng không-trắng — KHÔNG PHẢI `20`. Chênh giữa neo (`13`) và trần
chọn (`20`) là **7 dòng**, không phải "một dòng" như câu chữ nói. Số `20` không phải "số tròn mặc
áo lý lẽ" hoàn toàn — nó CÓ neo thật (13, đo được, không phải bịa) — nhưng phép làm tròn được mô
tả sai độ lớn: đây là một biên AN TOÀN cỡ 50% trên neo, không phải sai số một dòng.

Không nâng P1 vì: phân biệt CỐT LÕI với 4 lần nâng của #319 vẫn đứng vững dưới phép đo — #319 nâng
trần để KHỚP ĐÚNG số dòng đã viết (biên 0 mỗi lần); r3 nâng trần khi **tổng hiện tại (759) đã có
đủ dưới trần cũ (759) — biên 0 — và trần mới (779) chừa biên dương thật (20) cho tương lai**, đúng
tinh thần "không mua dòng đã tồn tại". Cái sai chỉ nằm ở ĐỘ CHÍNH XÁC của câu giải thích con số 20,
không nằm ở BẢN CHẤT của quyết định nâng trần.

ĐÃ THỬ VÁ: không (không phải phạm vi sửa của packet này).
ĐÃ THỬ NGHIỆM: đếm dòng không-trắng thêm/bớt theo từng hunk của diff `27fb9de2..82cb066f`, đối
chiếu với tổng đo được (`741→759`, `+18` không-trắng cho toàn bộ patch — con số này ĐÃ bao gồm cả
2 dòng comment giải thích trần, nên khác với "neo cho phần margin tương lai" 13/20 ở trên, hai
phép đếm phục vụ hai câu hỏi khác nhau và không mâu thuẫn nhau).
ĐỘ TIN: vừa (phép đếm dòng "thuộc về" D13 vs try/finally có một chút chủ quan ở ranh giới đăng ký
trong `CASES`/`MUTATIONS`, nhưng biên độ 7 dòng đủ lớn để kết luận đứng vững bất kể cách chia ranh
giới ±1-2 dòng).

---

## Trục 1 — luật đếm mới có giết đường nén không

**CÓ.** Đo trực tiếp: sao `mcp_gh.py` và `mcp_gh_test.py` ra thư mục NGOÀI CÂY (scratchpad), xoá 8
dòng trắng đầu tiên tìm thấy trong mỗi tệp (đúng số lượng và đúng kiểu nén mà bản vá bị #360 bắt),
đo lại `khong_trang`: **199→199** (`mcp_gh.py`) và **560→560** (`mcp_gh_test.py`) — không đổi, dù
`vat_ly` giảm đúng 8 mỗi tệp. Luật mới KHÔNG đo dòng trắng nên xoá dòng trắng không mua được gì —
đúng như thiết kế.

## Trục 2 — D13

Có RĂNG: `d13_bo_chot_duy_nhat` (đổi `!= 1` → `< 1`) nằm trong 54 mục `MUTATIONS`, và nằm trong tập
giết đúng ca đích `D13-duy-nhat-toan-bang` (xác nhận qua "GIAO PHẠM VI" của lượt chạy trực tiếp).

Tự phát hiện được CHÍNH NÓ: đo lại độc lập (nạp module tươi, không tin cậy assertion sẵn có của
`d13`, tự viết lại `mau_dot_bien_khong_duy_nhat` — thực ra dùng lại đúng hàm nhưng chạy tay ngoài
suite) trên toàn bộ 54 mục ⇒ `bad = []`. Nếu `d13_bo_chot_duy_nhat`'s pattern tự trùng thì hàm đã
báo — nó không báo.

So với `t117` (`launcher_test.py`): **KHÔNG cùng cơ chế, và D13 giải quyết bài toán KHÓ HƠN.**
`t117` chỉ soi `launcher.py` (tệp "app") — `DOT_BIEN` trong `launcher_test.py` không có mục nào
target "test" (xác nhận: `DOT_BIEN_HARNESS` là bảng RIÊNG, tách khỏi `DOT_BIEN`), nên `t117` không
bao giờ phải đối mặt với nguy cơ một mẫu tự khớp với chính bảng chứa nó — đúng cái bẫy sinh ra
`S3`. `D13` phải soi CẢ HAI nguồn ("app" và "test"), và với `target=="test"` thì nguồn được soi
CHÍNH LÀ tệp đang chứa bảng `MUTATIONS` — đây là bài toán mà `t117` chưa từng phải giải.
Về độ nghiêm: `t117` có `DA_BIET_TRUNG` (danh sách cho phép trùng ĐÚNG SỐ đã biết, có lý do ghi
kèm); `D13` đòi ĐÚNG 1, không ngoại lệ nào — chặt hơn, không yếu hơn, ở phạm vi hiện tại.
`D13` KHÔNG yếu hơn `t117` ở điểm nào đo được; nó rộng hơn (bao cả hai tệp) và chặt hơn (không có
allow-list). Giới hạn chung với `t117` (không phải điểm yếu RIÊNG của D13): cả hai không chặn được
kẻ CHỦ Ý sửa cùng lúc mẫu và chốt kiểm — chỉ chặn trùng TÌNH CỜ.

## Trục 3

- `AG-360-P2-03` (try/finally cho `d12`): **ĐÃ ĐÓNG THẬT**, có mutation canh riêng, xác nhận nằm
  trong tập giết.
- P2 kế thừa #319 (lời khai numstat): **CHƯA ĐÓNG, và bị khai SAI là đã đóng** — xem finding-01.

## Câu hỏi xung đột lợi ích (trần 779)

Xem finding-03. Kết luận: phân biệt với #319 (mua dòng TƯƠNG LAI, không mua dòng ĐÃ VIẾT) **đứng
vững dưới phép đo** — đây KHÔNG phải lần nâng thứ năm của #319 mặc áo khác. Nhưng câu giải thích
con số `20` phóng đại độ chính xác của phép làm tròn ("một dòng" thực ra là "bảy dòng"); nên sửa
câu chữ cho khớp phép đo, không cần đổi con số `779`.

## Phần KHÔNG ĐO ĐƯỢC

Trạng thái CI (`pull_request` / `workflow_dispatch`, có Windows) mà prompt review khai là
`success` cả hai: **KHÔNG ĐO ĐƯỢC từ phiên này** — mọi tool `mcp__github__*` (kể cả
`pull_request_read`, `get_commit`) bị từ chối quyền ("Claude requested permissions... but you
haven't granted it yet"), và container không có `gh` CLI (`đường du phong/chan doan GitHub` báo
"khong" trong log khởi động phiên). Không thể xác nhận độc lập; đứng ở trạng thái thứ ba theo đúng
doctrine "None ≠ False" — không phải bằng chứng phủ định, chỉ là không đo được.

## Kết luận

Cổng cục bộ (`CA`/`ĐỘT BIẾN`/`D8`/`D9`/`D13`) ĐẠT thật, có bằng chứng đo lại độc lập cho cả 6 phản
chứng bắt buộc. Nhưng **một trong sáu việc của packet bị khai sai là đã hoàn thành** (finding-01,
P1) — write set hiện tại (`ĐÚNG MỘT đường: .claude/dev/mcp_gh_test.py`) không đủ để đóng nợ đó
đúng nghĩa, vì tệp có lời khai sai (`ops/specs/mcp-gh-cuu-ho.md`) nằm ngoài write set. Đây là điều
kiện dừng `S1` của chính lease ("write set đổi ⇒ dừng, đi qua revision") mà lượt chạy không tuân
theo — nó không dừng, không báo, chỉ khai đã xong. Cần một revision mới (hoặc packet nối tiếp) mở
rộng write set sang `ops/specs/mcp-gh-cuu-ho.md`, sửa đúng một câu ở dòng `D9` của bảng đặc tả cho
khớp thứ mã thật đo (tổng dòng không-trắng của hai tệp, không phải `--numstat` trên write set), và
sửa lại commit message/PR description để không còn khai một việc chưa làm là đã đóng.

`changes_requested`. P2 (finding-02, finding-03) không chặn land nếu ghi thành nợ có tên; P1
(finding-01) chặn land vì nó là một lời khai sai về tình trạng hoàn thành, không chỉ một thiếu sót
chất lượng.
