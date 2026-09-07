# Đặc tả packet — LO-319-LINUX-BANG-CHUNG-XANH

- `packet_id`: **LO-319-LINUX-BANG-CHUNG-XANH** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được ngay khi có số Issue — tiền lệ #456 giữ bí danh ở `packet_id`,
  số ở `packet_issue`)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi trường này; lease #456 không có và
  bốn hồ sơ này cũng không có mission nào đang mở cho lane "chi phí CI Windows". Khuyến nghị:
  mở MỘT Mission Issue cho cả bốn packet (`GATE` · `LO` · `2A` · `2B`) rồi điền chung; nếu chủ
  kho không mở, ghi số Issue của packet tiền nhiệm `#456` và nói rõ đó là thay thế.
- `revision`: 1 · `generation`: 1 — **giữ 1 có chủ ý**: `§3.2` chỉ sinh revision khi spec đã đóng
  băng lúc vào `ready`; bốn packet này chưa có Issue nên chưa có revision nào để thay. Đây là bản
  NHÁP thứ năm của revision 1 (`81ba4e4` → `b1c2284` → `4c6aea4` → `e5ab4b7` → bản này); quy ước kho đo 21:31Z 06-09-2026
  trên 4 lease đã cấp (`cong-ngoai-write-set-exec-1{,r2,r3}-codex-20260828` ⇒ `revision: 1/2/3`,
  `n7-hook-giai-ma-utf8-exec-1r2-claude-20260830` ⇒ `2`): `revision: N` ⇔ `lease_id …-exec-1rN-…`,
  nên bump là đổi tên 4 lease nháp cùng mọi tham chiếu chéo cho một thứ chưa từng được cấp — không làm.
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (sửa CHÍNH vị từ quyết định xanh/đỏ của một
  cổng CI; không rõ ⇒ lấy mức chặt nhất). Hai trường là hai thứ: `risk` là khai báo của packet,
  `review_class` là mức tối thiểu; `effective_review_class` do dispatcher tính (`§8`).
- `depends_on`: **`GATE-TACH-JOB-CAT-CHI-PHI`** — giao write set tại `.claude/dev/ci_dang_ky_test.py`
  (từ bản sửa theo verdict lượt 1, GATE cũng chạm tệp ấy — xem `GATE-TACH-JOB-CAT-CHI-PHI.md`
  mục `write_set`). Trước đó packet này đứng đầu chuỗi; nay nó đi THỨ HAI.
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`) — **chỗ giữ, không
  phải mỏ neo**: ba mỏ neo trong lease (`base_sha` · `start_from_sha` · `reviewed_sha_required`)
  phải ĐO LẠI tại lúc cấp, bằng head `origin/master` SAU khi `GATE` đã integrated (`§5`: packet
  có dependency chỉ chạy sau predecessor đã integrated).
  **Trôi đã đo, 22:45Z 06-09-2026:** `origin/master` = `28cb898`, **46** commit sau `1b3caa1`
  (`git rev-list --count`), chạm write set của packet này đúng **1** dòng: `ci_dang_ky_test.py` thêm
  mục `"ops/bien_nhan_v2_test.py"` vào `DA_NOI` (dòng 65) — `MOI`, `MOI_WINDOWS`, `bang_chung_xanh`,
  `chay_moi`, `phan_chung` **không đổi**, nên mọi phép đo của hồ sơ này còn hiệu lực; **mọi số dòng**
  của tệp ấy trong hồ sơ (`:205`, `:474`…) là số trên `1b3caa1`, trên master nay **+1** (`:206`,
  `:475`). Kèm `ci.yml` +8 dòng (một bước `bien-nhan v2 selftest`, 39 → 40 bước) — thuộc write set
  của `GATE`, không của packet này. Phiên cấp lease đo lại ba mỏ neo và số dòng, không chép từ đây.

## `nguon_cap_viec`

Packet **khắc phục**. Không phải một dòng trong bảng packet của
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.

Nguồn: `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #1 và khối chú thích
`.claude/dev/ci_dang_ky_test.py:35-38` — cả hai khai thẳng rằng lỗ #319 phía **Linux** CÓ THẬT,
có sẵn từ trước packet #456, và bị để lại **có chủ đích** vì M4 của #456 đóng băng hành vi Linux.
Cross-review Codex lượt 1 của #456 bắt đúng chỗ này (finding P2) và bản vá đã phải lùi lại
(`426bfc0` — *"trả mẫu Linux về nguyên bản, dời chốt số dương sang đường Windows"*).

Packet này là chỗ M4 ấy được **gỡ đóng băng có thẩm quyền**, không phải chỗ nó bị lách.

Bản này là **bản sửa theo verdict cross-review lượt 4** (`reviewed_sha` `e5ab4b7`, Codex), sau lượt 3
(`4c6aea4`), lượt 2 (`b1c2284`) và lượt 1 (`d09f2f1`). Lịch sử thiết kế: A-b (bản đầu) → A-c *"soi cặp CÓ
NHÃN"* (lượt 1) → T *"bản ghi TỔNG theo từng định dạng"* (lượt 2) → T' *"T + luật 7 đếm hằng trong mã
regex"* (lượt 3) → **H** *"phủ VỊ TRÍ cặp trên dòng được chọn"* (bản này — phương án reviewer lượt 4 gợi
ý, executor tái dẫn xuất từng hunk và **đo lại bằng bộ ca của mình**, mục *"Thiết kế H"*). Slug
`span-rong-nuot-ti-le-vo-can` hỏng **bốn lượt liên tiếp**; bản lượt 3 viết *"không có thiết kế thứ tư"* và
trả lời `PROTOCOL §12` bằng *"hợp đồng T đúng, chỉ gỡ mâu thuẫn"* — verdict lượt 4 bác câu trả lời ấy bằng
hai phản chứng chạy được (16 ca tổng cụt/tab trong bộ 131 đã giao; countermodel của luật 7). Bản này
**không khai `§12` đã xong**: câu hỏi *"có nên tiếp tục cách làm này không"* là quyết định của **chủ kho**,
đặt lên bàn ở mục *"§12 — bốn lần hỏng"* cùng ba lựa chọn và năm điều kiện đo được; H là ứng viên đã đo,
**chưa được chọn**.

## Bối cảnh đo được (mọi số kèm thời điểm)

### Lỗ là gì, đo bằng lời gọi thật

`bang_chung_xanh(text, mau)` (`.claude/dev/ci_dang_ky_test.py:205`) chỉ soi **hai nhóm bắt** của
regex — mà ở `MOI` hai nhóm ấy là cặp số **CA**. Cặp số **đột biến** nằm ngoài nhóm bắt
(`DOT BIEN \d+/\d+ bi giet`) nên **không bao giờ được nhìn tới**.

Đo lại 19:32Z 06-09-2026 trên `1b3caa1`, gọi thẳng `bang_chung_xanh` với mẫu
`MOI[".claude/hooks/pretooluse_guard_test.py"]`. Đầu vào ghi **NGUYÊN CHUỖI**, kể cả dòng
`TONG: DAT` mà mẫu đòi (bản đầu của bảng này cắt mất dòng ấy nên chuỗi B1 nguyên byte trả `False`
vì không khớp — finding P3 lượt 1; nay ghi đủ):

| đầu vào (nền Linux) | mẫu `MOI` hiện tại | đúng ra phải |
|---|---|---|
| `TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n` | `True` | `True` |
| `TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n` | **`True`** ← LỖ | `False` |
| `TONG: CA 0/39 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n` | `False` | `False` |

`DOT BIEN 0/0 bi giet` là đúng hình dạng *"tập rỗng thoả `not song`"* mà bài học **#319** sinh ra
để chặn.

### Lỗ chạm MẤY mục, không phải một

Đo lại 19:29–19:32Z 06-09-2026 — đếm theo **số mục trong `MOI`** (8 mục) và theo **số LẦN XUẤT
HIỆN của `\d+/\d+` trong span khớp** (hai bộ cùng in `8/8` là hai lần xuất hiện):

| mục `MOI` | số nhóm bắt | cặp `n/m` có trong span | cặp được KIỂM hôm nay | nguồn bản in |
|---|---:|---:|---:|---|
| `chon_reviewer_test.py` | 2 | 1 (`25/25`) | 1 | thật, 19:29Z |
| `gh_readback_test.py` | 2 | 1 (`8/8`) | 1 | thật, 19:29Z |
| `mcp_gh_test.py` | 2 | 2 (`42/42`, `54/54`) | 1 | thật, 19:29Z (`rc=0`; trong sandbox reviewer bộ này ĐỎ 4 ca vì socket bị chặn — lệch rig) |
| `mcp_github_doc_test.py` | 2 | 1 (`17/17`) | 1 | thật, 19:29Z |
| `probe_mang_test.py` | **0** | 3 (`9/9`, `1/1`, `11/11`) | **0** | thật, 19:29Z |
| `pretooluse_guard_test.py` | 2 | 2 (`39/39`, `34/34`) | 1 | **canonical** (`0c5e889` khai `CA=39, DOT_BIEN=34`) |
| `subagent_ghi_detect_test.py` | 2 | 2 (`33/33`, `22/22`) | 1 | thật, 19:30Z |
| `nhanh_don_duoc_test.py` | 2 | 1 (`8/8`) | 1 | thật, 19:31Z |
| **tổng** | | **13** | **7** | |

Dòng `pretooluse_guard_test.py` KHÔNG đo trên bản in của container này — bộ ấy ở đây `rc=1` với
3 ca đỏ sẵn (xem `chua_do_duoc` #2), nên mẫu không khớp và không đo được tại chỗ.

Nên câu đúng **không** phải *"một mục bị hở"* mà là: **hai** mục (`pretooluse_guard_test.py`,
`subagent_ghi_detect_test.py` — cùng một regex, hai dòng kề nhau trong `MOI`) mang cặp đột biến
không ai canh, và **6 trong 13** cặp bằng chứng của cả sổ đăng ký chưa từng được kiểm. Dưới T/T' (lượt
2–3) 13/13 cặp nằm trong bản ghi tổng có grammar — nhưng 3 cặp của `probe_mang` là **hằng trong mã
regex**, và phép đo *tập giá trị `SPAN` bắt ⊆ tập `GRAMMAR` giải trình* (22:33Z 06-09-2026, 10/10 khối)
chỉ chứng minh **giá trị**, không chứng minh **vị trí và số lần**: reviewer lượt 4 dựng được hằng ở nhánh
regex không tham gia match vẫn được cộng (`law7.json`). Dưới H (bản này) cả **13/13** cặp Linux là **nhóm
bắt**, kể cả ba hằng probe (`(9)/(9)` · `(1)/(1)` · `(11)/(11)`), và vị từ đối chiếu **danh sách vị trí**
các cặp trên dòng với danh sách vị trí các nhóm trong match (đo 00:15Z 07-09-2026, mục *"Thiết kế H"*).
Phép đo tập giá trị cũ giữ làm lịch sử, không dùng làm chứng minh của H.

### Các hướng vá đã ĐO — A-b, A-c, T, T' đều bị bác; H là ứng viên

Đơn vị của bảng: **số phản chứng trong `phan_chung()` đổi màu** (nền `1b3caa1` = `51/51` đỏ đúng,
đo 19:32Z 06-09-2026 trong CÂY THẬT — bản sao ngoài cây cho `47/51` vì `ROOT = parents[2]` giải
sai, đó là **tạo tác rig**, không phải hồi quy), **số mẫu regex phải sửa**, và hai cột do verdict
lượt 1 rồi lượt 2 sinh ra, đo qua chính `chay_moi`: **đỏ giả** (bản in hợp lệ + ghi chú vô can ⇒
bị đếm đỏ) và **bỏ sót** (bản ghi tổng mang `0/0`, `n ≠ m`, hay TRÙNG ⇒ không bị đếm đỏ).

| hướng | mẫu phải sửa | phản chứng đổi màu | bịt `DOT BIEN 0/0`? | đỏ giả | bỏ sót | trạng thái |
|---|---:|---:|---|---:|---:|---|
| **A-a** — soi các nhóm bắt THEO CẶP | 0 | 0 (`51/51`) | **KHÔNG** | 0 | 16 / 64 | không đủ |
| **A-b** — soi **mọi** cặp `n/m` trong span | 0 | 1 (`50/51`) | CÓ | **1** (ghi chú `3/5`, 19:32Z) | — | bác ở lượt 1 |
| **A-c** — nhóm bắt theo cặp + cặp CÓ NHÃN trong span | 0 | 1 (`50/51`) | CÓ | **7 / 64** (21:07Z) | **7 / 64** (21:07Z) | **bác ở lượt 2** |
| **B-tự nhiên** — thêm nhóm bắt cho cặp đột biến (4 nhóm) | 2 | — | **KHÔNG — HỒI QUY** (xem dưới) | — | — | bẫy |
| **B-thật** — siết từng mẫu thành `[1-9]\d*/[1-9]\d*` | 2 | 3 | chỉ cho 2 mẫu ấy | 0 | không đọc tổng TRÙNG | không đủ |
| **T** (lượt 2) — bản ghi TỔNG theo từng định dạng, nhưng prototype còn lấy số từ nhóm `SPAN`, và grammar `probe` #1 có `(?: .*)?` | 0 chuỗi regex | ≥ 3 (A5) | CÓ ở bản ghi · **KHÔNG** ở đuôi wildcard | **7 / 66** (reviewer lượt 3, 22:10Z) · **8 / 137** (đo lại 22:33Z, bộ ca lượt 3) | **1 / 66** · **5 / 137** | **bác ở lượt 3** |
| **T'** (lượt 3) — T với luật 5 viết lại (số CHỈ từ dòng tổng) + luật 7 **đếm hằng trong mã regex** | 0 chuỗi regex (đổi KIỂU giá trị `MOI`) | ≥ 3 (A5) | CÓ ở bản ghi · **KHÔNG** khi hằng nằm ở nhánh regex không tham gia match | **0 / 137** (22:33Z 06-09) · **0 / 131** bộ verdict lượt 3 (đo lại 00:15Z 07-09) · luật 7 **3 / 11** ca `law7` | **0 / 137** · **16 / 131** (tổng cụt/tab — bộ chọn đòi dấu cách/payload) · luật 7 **5 / 11** | **bác ở lượt 4** |
| **H** (bản này) — bộ chọn nhận NHÃN độc lập payload; hằng cũng là nhóm bắt; đối chiếu **DANH SÁCH VỊ TRÍ** cặp trên dòng với vị trí nhóm trong match | 0 chuỗi regex (đổi KIỂU giá trị `MOI`, `ngoai_pham_vi` #1) | ≥ 3 (A5) | CÓ, kể cả khi grammar có lỗ — grammar lỗ làm ĐỎ ngay bản in xanh | **0 / 131** · **0 / 137** · **0 / 32** ca tấn công mới (00:15Z 07-09-2026) | **0 / 131** · **0 / 137** · **0 / 32** · `law7` **0 lệch / 11** theo hợp đồng H | **ứng viên — chưa chọn** (`§12` thuộc chủ kho) |

A-c bị bác ở HAI chiều, cả hai reviewer lượt 2 dựng được và tôi đo lại 21:07Z 06-09-2026 qua
chính `chay_moi` trên bản in THẬT:

- **đỏ giả** — `NHAN` quét cả span, nên `Ghi chú: DOT BIEN đã xem 3/5 hướng cải tiến.` hay
  `Giải thích: ví dụ DOT BIEN 0/0 là bảng rỗng.` chèn trước `TỔNG: ĐẠT` của bản in thật
  `chon_reviewer` làm `0 → 1`. Nhãn trong VĂN XUÔI bị đọc như bằng chứng; đây đúng là bệnh của A-b
  quay lại với một bộ lọc hẹp hơn.
- **bỏ sót** — `[^\n\d]{0,24}?` là một khoảng cách tuỳ ý: `DOT BIEN` + 25 khoảng trắng + `0/0`,
  `DOT BIEN\n0/0`, `DOT BIEN đợt 2: 0/0` đều lọt. Và A-c không hề nhìn TỔNG TRÙNG: hai dòng
  `TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet`, hay hai dòng `8/8`, hai dòng `nền: 25/25 đạt`
  ⇒ `0` đỏ, trong khi không có quy tắc nào chọn một trong hai — 7 ca như thế trong bảng đo.

Gốc chung của A-b lẫn A-c: cả hai hỏi *"trong span có cặp số nào đáng ngờ không"* — đọc TOÀN BỘ
văn bản như bằng chứng rồi cố lọc, và bộ lọc nào cũng vừa quá rộng vừa quá hẹp. Câu hỏi đúng là
*"bản ghi tổng của bộ này nằm ở dòng nào, có đúng MỘT, và có đúng CẤU TRÚC không"*. Đó là T.

T (lượt 2) hỏi đúng câu ấy, nhưng prototype của nó vẫn trả lời thêm câu cũ ở một chỗ (nhóm của
`re.search(SPAN)`) và để ngỏ một khoảng `.*` trong một grammar. T' (lượt 3) gỡ hai chỗ ấy rồi **dời phần
mù sang luật 7**: `len(_CAP.findall(grammar))` đếm ký tự của *chương trình regex*, không đếm hằng đã tiêu
thụ *trên dòng* — reviewer lượt 4 dựng được cả hai chiều (mục `§12`, (b)). Và bộ chọn của T' (`TONG: CA `,
`nền: `, `CA\s+:`…) đòi dấu cách hoặc payload nên **bỏ qua tổng cụt/tab** (`TONG: CA`, `nền:\t0/0 đạt`) —
16 ca của bộ 131 mà verdict lượt 3 đã giao, T' cho `0` thay vì `1`. Mục kế tiếp là câu trả lời `§12` viết
lại lần thứ hai — lần này **không kết luận thay chủ kho**.

### §12 — bốn lần hỏng: câu hỏi "có nên tiếp tục" thuộc CHỦ KHO, đặc tả này không tự trả lời

`PROTOCOL §12`: *"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên tiếp tục cách làm
đó, không chỉ vá lần thứ tư."* Slug `span-rong-nuot-ti-le-vo-can` hỏng **bốn** lượt: A-b (lượt 1) → A-c
(lượt 2) → T (lượt 3) → **T' (lượt 4)**. Bản lượt 3 đã trả lời câu hỏi ấy bằng *"ba lần cùng một gốc; hợp
đồng T đúng, prototype trái hợp đồng; T' chỉ gỡ mâu thuẫn — không có thiết kế thứ tư"*. Verdict lượt 4
kiểm câu trả lời đó bằng phép đo, và kết quả là:

- **(a) ĐÚNG** — *"BASE cũng đỏ giả ở mảnh (i)"*: 8 ca ghi-chú-trước của BASE trùng 8 ca của T trên bộ
  137 (`replay-summary.json`; executor đo lại 00:15Z 07-09-2026: BASE `8/33` trên 137 và `8/28` trên 131).
  Mệnh đề lịch sử đứng vững, nhưng nó chỉ chứng minh T *chép lại* một lỗi của BASE — **không** chứng minh
  cả thiết kế T đúng.
- **(b) SAI ở luật 7** — T' đổi nguồn số (đúng) rồi **dời phần mù sang mã regex**:
  `len(_CAP.findall(grammar))` đếm hằng trong *chương trình regex*, không đếm hằng đã tiêu thụ *trên
  dòng*. Hai chiều, đều chạy được (`law7.json`; executor đo lại 00:15Z 07-09-2026 qua chính `chay_moi`):
  đổi hằng `9/9` thành `9[/]9` — cùng ngôn ngữ, cùng stdout thật — làm số hằng đếm được từ `1` xuống `0`
  ⇒ T' **đỏ giả** (2 ca); hằng ở nhánh tuỳ chọn vắng mặt `(?: \(schema 1/1\))?` hay nhánh alternative
  không được chọn `(?:1/1|\d+/\d+)` vẫn được cộng ⇒ đẳng thức `2 = 1 + 1` **đúng** mà `0/0` **không bị
  kiểm** ⇒ T' **bỏ sót** (5 ca: hai nhánh ấy, nhóm chồng vị trí, literal `0/0`, literal `33/34`).
- **(c) Lý do loại hướng "đổi bên IN" KHÔNG còn đứng vững như đã viết.** Phần chi phí đúng (9 tệp, vượt
  write set và trần `sensitive` của `ADR-0044`) — nhưng đó là lý do **không thi công trong packet này**,
  không phải lý do **bỏ qua revision**. Và điều kiện mở lại thứ hai do chính bản lượt 3 viết (*"lượt review
  kế tìm được đỏ giả/bỏ sót KHÔNG thuộc vùng 'số ngoài dòng tổng'"*) **đã đạt**: countermodel ở (b) nằm
  **ngay trong dòng tổng được chọn**. Điều kiện thứ nhất (*"bản in thật mà grammar đóng không mô tả
  được"*) reviewer chỉ ra là **không thực thi được** khi chưa định nghĩa lớp grammar được phép — một chuỗi
  hữu hạn luôn viết được thành literal regex; bản này thay nó bằng Đ2 ở bảng dưới.
- **(d) Bộ chọn của T' bỏ tổng lỗi** — phần này verdict lượt 3 đã nêu và bản lượt 3 **chưa vá**: với
  `TONG: CA ` làm bộ chọn, `TONG: CA` cụt hay `TONG: CA\t0/0 …` không được chọn ⇒ thành văn xuôi ⇒ `0` đỏ
  trong khi M3/A3 đòi `1` (tổng sai cấu trúc). 16 ca như thế **đã có kỳ vọng trong bộ 131** của verdict
  lượt 3 — không phải 49 ca ranh giới đã công khai. Bản lượt 3 chỉ đo bộ 137 của mình và không replay bộ
  131 được giao: đúng *"hỏi chỗ tiện tay thay vì hỏi chỗ kết luận được ghi"* (`CLAUDE.md`).

**Hình dạng lỗi, đếm cho đúng — BỐN lần, và phân biệt production với bản nháp review** (bảng đầy đủ ở
`hinh_dang_ke_thua`):

| hình dạng | trong MÃ ĐÃ LAND (production) | trong BẢN NHÁP đặc tả bị review bác | tổng |
|---|---:|---:|---:|
| tập RỖNG thoả `not song` (`0/0` được nhận là bằng chứng) | **3** — #319 · #456 đường Windows (đã bịt) · đường Linux (lỗ hiện hữu, packet này bịt) | 0 | 3 |
| vùng bằng chứng KHÔNG được khoanh đủ, và lời khai hai chiều rộng hơn phép đo | **0** — chưa dòng mã nào của packet này land | **4** — A-b (lượt 1, 19:32Z 06-09) · A-c (lượt 2, 21:07Z) · T (lượt 3, 22:10Z) · T' (lượt 4, `prior131.json` + `law7.json`; đo lại 00:15Z 07-09-2026) | 4 |

Hai cột không cộng vào nhau: cột đầu là lỗi cổng CI đã cho qua thật; cột sau là bốn bản thiết kế chết
trên giấy trước khi thi công — chính cơ chế review đang làm việc. Nhưng `§12` đếm **hình dạng**, không
đếm nơi nó xuất hiện: cùng một gốc (*số làm bằng chứng đến từ vùng mà hợp đồng không khoanh*) tái phát
bốn lần trong cùng một packet, hai lần sau khi đã có câu trả lời `§12` lần thứ nhất. **H là bản thiết kế
thứ NĂM.** Nó có phép đo tốt hơn bốn bản trước (mục kế), nhưng "tốt hơn" không phải là câu trả lời cho
*"có nên tiếp tục cách làm này không"* — câu ấy hỏi về CÁCH LÀM (đọc bản in cho người bằng grammar), không
hỏi về bản vá.

**Ba lựa chọn đặt lên bàn — chủ kho chọn, ghi vào `granted_on_instruction` của lease:**

| # | lựa chọn | chạm gì | mua được gì | giá phải trả |
|---|---|---|---|---|
| 1 | **Tiếp H trong write set hiện tại** (1 tệp `ci_dang_ky_test.py`) | không đổi write set, không đổi formatter | bịt lỗ #319 Linux sớm nhất; 0 đỏ giả / 0 bỏ sót trên 311 hàng đo có kỳ vọng (00:15Z 07-09-2026); grammar lỗ làm ĐỎ ngay bản in xanh | hợp đồng HỮU HẠN với đúng 8 formatter hiện tại; 5 ranh giới mới của H + 49 ranh giới cũ (`chua_do_duoc` #1); **không** hỗ trợ cặp `n/m` metadata trên dòng tổng; vẫn là bản thứ năm của cùng một cách làm |
| 2 | **Mở revision đổi bên IN** — mỗi bộ test in thêm MỘT dòng máy đọc (ví dụ JSON tổng `{"ca": [39, 39], "dot_bien": [34, 34]}`), sổ đăng ký đọc dòng ấy | 8 tệp in (2 là hook `.claude/hooks/**`) + consumer = **9 tệp** ⇒ vượt `ADR-0044` `sensitive` (≤ 3 tệp) ⇒ cần **ngoại lệ chủ kho** hoặc tách thành ≥ 3 packet nối tiếp, mỗi packet cross-review riêng | lớp lỗi *"vùng bằng chứng không khoanh"* chết theo **kiến trúc** (bằng chứng không còn nằm trong văn bản cho người đọc) — bài học `CLAUDE.md` *"bảy phát hiện cùng một đường ⇒ sai ở quyết định gốc"* | ≥ 3 vòng review nữa; consumer vẫn cần hợp đồng đọc (đúng MỘT dòng, khớp trọn, cặp `n == m > 0` — luật 3/4/5 dưới cú pháp khác), nên H không mất mà **thu nhỏ** thành parser một dòng; lỗ Linux mở thêm chừng ấy thời gian |
| 3 | **Dừng packet này và tách lại** | đóng packet với biên nhận `blocked: same-failure ×4`; mở packet/mission mới với spec đóng băng từ đầu, chép `hinh_dang_ke_thua` sang | cắt chuỗi vá; spec mới không phải mang năm bản lịch sử | lỗ Linux tiếp tục mở; chi phí soạn lại; bốn lease nháp `GATE/LO/2A/2B` phải đánh lại chuỗi phụ thuộc (2A/2B `depends_on` LO) |

Khuyến nghị của executor — **chỉ là khuyến nghị**: lựa chọn 1 với H, **kèm** năm điều kiện bên dưới làm
chốt tự động chuyển sang 2/3; lý do là lỗ #319 Linux đang MỞ trong CI thật, còn lựa chọn 2 mua sự an toàn
kiến trúc bằng ≥ 3 vòng review nữa. Nhưng người viết khuyến nghị này cũng là người đã viết *"không có
thiết kế thứ tư"* ở lượt 3 — nên câu trả lời phải là của chủ kho.

**Điều kiện ĐO ĐƯỢC để biết H có đủ hay không** — mỗi điều kiện nêu phép đo và ngưỡng; chạm ngưỡng nào
thì H **không đủ** và packet chuyển sang lựa chọn 2 hoặc 3, không vá lần thứ sáu:

| # | điều kiện | phép đo | ngưỡng ⇒ H KHÔNG đủ |
|---|---|---|---|
| Đ1 | lượt review kế tìm được đỏ giả hoặc bỏ sót **ngoài** danh sách ranh giới đã công khai (49 ca lượt 3 + 5 ca của H, `chua_do_duoc` #1) | replay qua `chay_moi` với bộ chạy giả; đơn vị: số mục ĐỎ | **≥ 1** ca ⇒ lần **thứ năm** của hình dạng; dừng cách làm |
| Đ2 | bản in xanh THẬT của một formatter hiện có (thu qua `_chay_that`, `rc=0`) bị H bác | A6(a) trên bản in của phiên thi công, 8 định dạng | **≥ 1** định dạng ⇒ grammar đóng không mô tả được bản in thật — điều kiện mở lại thứ nhất của bản lượt 3, nay thực thi được |
| Đ3 | cần một cặp `n/m` **không phải bằng chứng** trên dòng tổng (metadata kiểu `schema 1/2`) | một formatter hiện có hoặc một packet đang mở đòi in nó | **có** ⇒ H không hỗ trợ theo thiết kế (`law7.json` `optional-version-present`: H bác); phải quyết schema vai trò ở revision |
| Đ4 | additions runtime | `git diff --numstat`, cột additions, trên `ci_dang_ky_test.py`, đo trước review | **> 300** ⇒ dừng (`ADR-0044`); không cắt ca, không nâng trần |
| Đ5 | `phan_chung()` sau thi công | `N/N` với `N ≥ 51 + số ca mới A1–A6` (A5) | **< N/N** ⇒ chưa đủ; không tính là lần thứ năm nếu nguyên nhân là ca mới viết sai |

**Đặc tả này không khai `§12` đã xong.** Thứ nó khai là: H đã đo (mục kế), ba lựa chọn và năm điều kiện
ở trên, và bộ đếm bốn lần. Lease nháp giữ `thay_the_cho: []` và sáu ô trống — không ai bắt tay cho tới
khi chủ kho chọn.

### Thiết kế H — phủ VỊ TRÍ cặp trên dòng được chọn (ứng viên, đã đo, CHƯA được chọn)

Nguồn: gói gợi ý của verdict lượt 4 (`goi-y/cay/`, nhãn *"chưa chạy trên cây thật — executor tự áp, tự
đo, tự chịu trách nhiệm commit"*; `hint_provenance.json` 40 hunk). Executor **tái dẫn xuất từng hunk** và
**đo lại bằng bộ ca của mình** (`do_h.py`, băm ở `MANIFEST.sha256` của gói `executor-luot4-va/`) — không
chép số của reviewer. Hai khối mã dưới đây chép **nguyên văn** từ cây gợi ý để băm khối trùng với thứ
reviewer đã đo (`validate_candidate.py --hint-tree`): bảng `TONG` `c23bcd01…` · vị từ `bde441a0…` (đủ 64
ký tự trong `do_h.json`, khoá `khoi_ma_sha256_H`) — băm lại nội dung giữa hai hàng rào mà lệch thì thứ được
đo không phải thứ đang đọc.

**Hợp đồng — 7 luật; luật 2 và luật 7 khác T'** (so với bản lượt 3: luật 1, 3, 4, 6 giữ; luật 5 giữ ý,
đổi `a == b` thành `int(a) == int(b)`; luật 2 nới bộ chọn; luật 7 viết lại hoàn toàn):

1. Đơn vị bằng chứng của một mục là **cặp `(SPAN, TONG)`**. `SPAN` là regex hiện có, **giữ nguyên chuỗi**
   — nó vẫn canh thứ tự và dòng kết (`TỔNG: ĐẠT` / `TONG: DAT`) và **là điều kiện khớp đứng TRƯỚC** mọi
   luật dưới (đo: chuỗi `34/34/0` trên `pretooluse` bị SPAN trượt trước khi H kịp đo — ca `D1d`). `TONG`
   là danh sách **bản ghi tổng**, mỗi bản ghi = `(BỘ CHỌN, GRAMMAR)`.
2. **BỘ CHỌN** khớp bằng `re.match` ở **ĐẦU DÒNG**, chỉ nhận **NHÃN**, **độc lập với payload**: `TONG: CA`
   theo sau bởi khoảng trắng, dấu hai chấm hoặc cuối dòng (`(?=\s|:|$)`); `CA:`/`ĐỘT BIẾN:` không đòi khoảng
   trắng trước dấu hai chấm (`\s*:`); các nhãn `nền:` `gh_readback tests:` … không đòi dấu cách sau nhãn.
   Hệ quả cố ý: **tổng cụt/tab là BẢN GHI SAI CẤU TRÚC** (luật 4 làm ĐỎ), không còn biến thành văn xuôi
   — đây là chỗ T' hỏng 16/131. `nhanh` vẫn là cả dòng chỉ mang cặp số (`\d+/\d+\s*$`); dòng có hậu tố
   không thuộc hợp đồng (ranh giới công khai từ lượt 3).
3. Mỗi BỘ CHỌN phải chọn **ĐÚNG MỘT** dòng. `0` hay `≥ 2` ⇒ `False`.
4. Dòng được chọn phải khớp **GRAMMAR bằng `re.fullmatch`** — trọn dòng; grammar **đóng** (hậu tố/dấu
   ngoặc khai cụ thể, không `.*`).
5. Khi mục có `TONG`, số làm bằng chứng **CHỈ** đến từ nhóm bắt của `GRAMMAR` trên dòng được chọn, soi
   **theo cặp** `int(n) == int(m) > 0`. `SPAN` chỉ là điều kiện khớp và phải có số nhóm **chẵn**; nhánh
   chuỗi trần (không `TONG`) vẫn soi số từ nhóm `SPAN`, nay có chốt `isdecimal()` cho nhóm `None`/không
   phải số. Số nhóm LẺ ⇒ `False`; chuỗi trần `0` nhóm ⇒ `False` (M2).
6. Dòng **không** khớp bộ chọn nào là **VĂN XUÔI**: không được đọc. Không nới thành quét cả stdout.
7. **Phủ VỊ TRÍ, không đếm nguồn regex.** Mọi cặp `\d+/\d+` mà `_CAP.finditer` tìm thấy trên dòng được
   chọn phải trùng **CHÍNH XÁC** hai `span` của một cặp nhóm bắt trong match grammar; hai **danh sách**
   (không phải tập) phải bằng nhau — giữ **thứ tự** và **số lần**. Hằng cũng phải là nhóm bắt:
   `9/9` → `(9)/(9)`, `1/1` → `(1)/(1)`, `11/11` → `(11)/(11)`. Mỗi bản ghi có **ít nhất một** cặp. Nhóm
   không tham gia match (`span (-1, -1)`), nhóm chồng vị trí, nhóm lệch biên số, literal không nhóm — đều
   làm bản ghi ĐỎ **ngay trên bản in xanh** (grammar lỗi ⇒ ồn ào, không mù).

**Bảng bản ghi tổng của 8 mục** — bản đo, chưa phải bản thi công. Bản in nguồn như bản lượt 3 (A6: 5 bộ
chạy tại container soạn spec 21:00:15–21:00:23Z 06-09-2026, `rc=0`; `subagent`/`nhanh` từ sandbox reviewer
lượt 1; `pretooluse` canonical — `chua_do_duoc` #2, #4). So với T' chỉ đổi **bộ chọn** (8 chuỗi) và **ba
hằng probe thành nhóm bắt**; mọi grammar khác giữ nguyên văn:

```python
# BỘ CHỌN: re.match ở ĐẦU DÒNG · GRAMMAR: re.fullmatch TRỌN dòng · mọi nhóm bắt là cặp (n, m).
TONG = {
    ".claude/dev/chon_reviewer_test.py":   [(r"nền:", r"nền: (\d+)/(\d+) đạt")],
    ".claude/dev/gh_readback_test.py":     [(r"gh_readback tests:", r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)")],
    ".claude/dev/mcp_gh_test.py":          [(r"CA\s*:", r"CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT"),
                                            (r"ĐỘT BIẾN\s*:", r"ĐỘT BIẾN\s+: đã đo (\d+)/(\d+) tập giết · ĐẠT")],
    ".claude/dev/mcp_github_doc_test.py":  [(r"mcp_github_doc tests:", r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)")],
    ".claude/dev/probe_mang_test.py":      [(r"tự đột biến cổng:", r"tự đột biến cổng: (9)/(9) chết(?: \(m1\.\.m5 \+ 4 dòng cơ chế\))?"),
                                            (r"named mutant probe_missing_tool_executes_git:", r"named mutant probe_missing_tool_executes_git: (1)/(1) chết"),
                                            (r"nền:", r"nền: (11)/(11) đạt")],
    ".claude/hooks/pretooluse_guard_test.py":    [(r"TONG: CA(?=\s|:|$)", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    ".claude/hooks/subagent_ghi_detect_test.py": [(r"TONG: CA(?=\s|:|$)", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    "ops/nhanh_don_duoc_test.py":          [(r"\d+/\d+\s*$", r"(\d+)/(\d+)")],
}
# Windows — ghép theo THỨ TỰ hai dạng của MOI_WINDOWS[pretooluse]: dòng Windows · dòng Linux đầy đủ.
TONG_WINDOWS = {
    ".claude/hooks/pretooluse_guard_test.py": (
        [(r"TONG: CA(?=\s|:|$)", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS — do tren ubuntu-latest")],
        [(r"TONG: CA(?=\s|:|$)", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    ),
}
```

**Vị từ** (bản đo — thi công được đổi cách biểu diễn `(SPAN, TONG)` miễn giữ đủ 7 luật; đổi khối mã thì
**đo lại toàn bộ**, không chép số của các bảng dưới):

```python
_CAP = re.compile(r"(\d+)/(\d+)")

def _cap(g):
    return None if len(g) % 2 else [(g[i], g[i + 1]) for i in range(0, len(g), 2)]

def bang_chung_xanh(text, mau):
    span, tong = (mau, ()) if isinstance(mau, str) else mau
    m = re.search(span, text, re.M)
    if not m or _cap(m.groups()) is None:
        return False
    if not tong:
        pairs = _cap(m.groups())
        return bool(pairs) and all(a and b and a.isdecimal() and b.isdecimal()
                                  and int(a) == int(b) > 0 for a, b in pairs)
    cap = []
    for chon, grammar in tong:
        hits = [line for line in text.splitlines() if re.match(chon, line)]
        if len(hits) != 1:
            return False
        g = re.fullmatch(grammar, hits[0])
        c = _cap(g.groups()) if g else None
        if not c:
            return False
        actual = [(p.span(1), p.span(2)) for p in _CAP.finditer(hits[0])]
        covered = [(g.span(i), g.span(i + 1)) for i in range(1, len(g.groups()) + 1, 2)]
        if covered != actual:
            return False
        cap += c
    return bool(cap) and all(int(a) == int(b) > 0 for a, b in cap)
```

`MOI[path]` trở thành `(SPAN, TONG[path])`; mỗi phần tử của `MOI_WINDOWS[path]` thành
`(SPAN, TONG_WINDOWS[path][i])`; `mau_theo_nen` và `chay_moi` **không đổi chữ ký** (đo: H đi qua `chay_moi`
thật mà không sửa hàm ấy). Hai ca neo mẫu cũ so `MOI[_P456]` với một CHUỖI nên đổi màu theo thiết kế — xử
ở A5, không xoá.

**Ba chỗ của vị từ H đáng nói thẳng, vì đọc code không thấy** (đo 00:15Z 07-09-2026):
- `int(a) == int(b) > 0` thay `a == b`: `039/39` được H **nhận** (T' bác) — ca `D2`, ranh giới, không
  formatter nào in số 0 đứng đầu; ghi để phiên thi công biết đây là đổi ngữ nghĩa có chủ ý (so SỐ, không
  so CHUỖI), không phải sơ suất.
- `bool(cap)` ở dòng `return` là **mã chết** dưới H: `if not c: return False` trong vòng lặp đã chặn bản
  ghi rỗng, và nhánh `not tong` thoát trước; đột biến bỏ nó (`mH13`) đổi màu **0/311** ca. Giữ làm dây an
  toàn cũng được, nhưng đừng khai nó là một chốt.
- `_CAP` là **định nghĩa duy nhất** của "cặp": tìm trái→phải, không chồng lấn. Chuỗi `54/54/0` chỉ là MỘT
  cặp `54/54` cộng một đuôi `/0`; tác giả grammar **khai tường minh** `(\d+)/(\d+)/\d+` thì H nhận (ca
  `D1`, ranh giới — phải dựng trên `mcp` vì SPAN của `pretooluse` chặn ca tương đương). `\d` là Unicode:
  `３９/３９` được nhận vì `int('３９') == 39` (ca `D3`). Siết `_CAP` (`[0-9]`, cấm `/` kề cặp) là lựa chọn
  của phiên thi công — đổi khối mã thì đo lại toàn bộ.

**Đo hai chiều — bốn bộ ca, qua chính `chay_moi` trên module thật** (`do_h.py`, đo **00:15Z 07-09-2026**
trên cây `e5ab4b7`, module không sửa; vị từ H và bảng `TONG` lấy NGUYÊN VĂN từ hai khối mã ở trên; T' từ
blob `e5ab4b7`; BASE là hàm trong module; đơn vị: số ca mà giá trị `chay_moi` ≠ kỳ vọng). Bốn bộ **có ca
trùng nhau** (bộ 131 và 137 cùng dựng từ 12 kiểu probe của reviewer lượt 3), nên KHÔNG cộng thành 311 ca
độc lập — 311 là số **hàng đo có kỳ vọng**, 54 hàng ranh giới không đặt kỳ vọng:

| bộ ca | nguồn kỳ vọng | hàng có kỳ vọng | BASE đỏ giả / bỏ sót | T' | **H** |
|---|---|---:|---:|---:|---:|
| A — bộ verdict lượt 3 (`review-artifacts-luot3/T.json`) | reviewer lượt 3 | 131 | 8 / 28 | 0 / **16** | **0 / 0** |
| B — bộ executor lượt 3 (`executor-luot3-va/do_t2.py`, 186 ca) | executor, kỳ vọng ghi ở lượt 3 | 137 (+ 49 ranh giới) | 8 / 33 | 0 / 0 | **0 / 0** |
| C — bộ thăm dò luật 7 (`review-artifacts-luot4/law7.json`) | reviewer lượt 4, kỳ vọng đặt cho **T'** | 11 | 0 / 7 | 3 / 5 | 3 / 0 theo kỳ vọng T' — **ba ca "đỏ" là đỏ ĐÚNG THIẾT KẾ H**: `equivalent-slash-class` · `equivalent-escaped-slash` dùng hằng KHÔNG nhóm bắt (grammar lỗi theo luật 7 H; cùng ba cách viết CÓ nhóm bắt ⇒ H nhận 3/3, ca `D16`); `optional-version-present` là metadata `1/2` ngoài hợp đồng (Đ3). Theo hợp đồng H: **0 lệch / 11** |
| D — ca tấn công MỚI của executor vào H (bảng dưới) | executor | 32 (+ 5 ranh giới) | 0 / 19 | 0 / 11 | **0 / 0** |
| **tổng hàng đo** | | **311** (+ 54 ranh giới) | 16 / 87 | 3 / 32 | **0 / 0** theo hợp đồng H (3 / 0 theo kỳ vọng T' của bộ C) |

**16 ca selector của verdict lượt 4** (P1, phần cũ) — tất cả trong bộ A, kỳ vọng `1`: BASE `0` cả 16,
T' `0` cả 16, **H `1` cả 16**. Đột biến `mH11` (trả cả 8 bộ chọn về T') làm **16/16** về `0`; `mH1` (lấy
dòng đầu thay vì đòi đúng một) làm 13/16 về `0` — 3 ca còn lại là tổng cụt đứng TRƯỚC tổng xanh, dòng đầu
vẫn là dòng cụt nên vẫn ĐỎ.

**Bộ D — 37 ca executor dựng để tìm chỗ H hỏng** (32 có kỳ vọng, 5 ranh giới; grammar sửa qua
`tong_override`/`tongw_override`, bản in thật từ `fixtures/`; `—` = ranh giới, không đặt kỳ vọng):

| nhóm | ca | kỳ vọng | BASE | T' | **H** | điều ca này đo |
|---|---|---:|---:|---:|---:|---|
| chuỗi cặp `a/b/c` | `D1` `mcp` `54/54/0` + grammar khai `(\d+)/(\d+)/\d+` | — | 0 | 0 | **0** | **ranh giới định nghĩa `_CAP`**: `/0` không là cặp; tác giả grammar khai tường minh thì qua |
| | `D1b` cùng chuỗi, grammar chuẩn · `D1c` `0/0/54` + grammar khai đuôi · `D1d` `34/34/0` trên `pretooluse` | 1 · 1 · 1 | 0 · 0 · 1 | 1 · 1 · 1 | **1 · 1 · 1** | fullmatch trượt · cặp đầu `0/0` vẫn bị soi · SPAN chặn trước |
| số 0 đứng đầu / Unicode | `D2` `039/39` · `D3` `３９/３９` | — · — | 1 · 0 | 1 · 0 | **0 · 0** | H so số nguyên; `\d` Unicode — hai ranh giới, formatter không in |
| | `D2b` `0/00` · `D3b` `٠/٠` | 1 · 1 | 0 · 0 | 1 · 1 | **1 · 1** | `int` về 0 ⇒ `> 0` bác |
| nhóm tuỳ chọn | `D4` grammar `(?: thêm (\d+)/(\d+))?` vắng mặt trên bản in xanh | 1 | 0 | 1 | **1** | nhóm không tham gia match ⇒ span `(-1,-1)` ⇒ grammar lỗi ⇒ ĐỎ ngay bản in xanh (ồn ào) |
| | `D4b` có mặt `thêm 1/1` · `D4c` có mặt `thêm 0/0` | 0 · 1 | 0 · 0 | 0 · 1 | **0 · 1** | 3 cặp = 3 cặp ⇒ nhận; cặp tuỳ chọn `0/0` vẫn bị soi |
| grammar bắt sai | `D5` Windows bắt `([1-9]\d*) muc` (1 nhóm) · `D6` `CA 1(\d+)/(\d+)` trên `139/39` · `D7` `(\d+)(/\d+)` | 1 · 1 · 1 | 0 · 1 · 0 | 1 · **0** · 1 | **1 · 1 · 1** | nhóm LẺ · span lệch biên số (T' bỏ sót) · span lệch dấu gạch |
| | `D5b` grammar Windows chuẩn của H | 0 | 0 | 0 | **0** | đối chứng |
| bộ chọn | `D8` `TONG: CA` + tab / NBSP / `:` / cuối dòng, SAU tổng xanh (4 ca) | 1 | 0 | **0** | **1** | tổng cụt/tab là bản ghi sai cấu trúc (T' bỏ sót cả 4) |
| | `D8e` `TONG: CAX 0/0` · `D8f` `TONG: CA. 0/0` | 0 · 0 | 0 · 0 | 0 · 0 | **0 · 0** | không qua bộ chọn ⇒ văn xuôi — ranh giới công khai của luật 6 |
| | `D10` `mcp` + dòng `CA:` cụt · `D10b` + `CACH LY: 1/1` | 1 · 0 | 0 · 0 | **0** · 0 | **1 · 0** | `CA\s*:` chọn `CA:`, không chọn `CACH` |
| | `D13` `nền:` cụt TRƯỚC bản in thật `chon` · `D13b` `nền:\t0/0 đạt` TRƯỚC | 1 · 1 | 0 · 0 | **0 · 0** | **1 · 1** | tổng cụt đứng TRƯỚC cũng bị đếm |
| hằng probe | `D11` `9/9 → 0/0` · `D11b` `11/11 → 10/11` · `D11c` `1/1 → 2/2` | 1 · 1 · 1 | 1 · 1 · 1 | 1 · 1 · 1 | **1 · 1 · 1** | hằng nay là nhóm bắt nên bị soi; `2/2` trượt grammar ghim hằng — hợp đồng hữu hạn |
| | `D16` ba cách viết `(9)/(9)` · `(9)[/](9)` · `(9)\/(9)` trên stdout thật | 0 · 0 · 0 | 0 | 0 | **0 · 0 · 0** | cùng ngôn ngữ, cùng bản in ⇒ nhận (chỗ T' đỏ giả với hằng không nhóm) |
| | `D17` hằng KHÔNG nhóm bắt `9/9` trên stdout thật | 1 | 0 | **0** | **1** | grammar lỗi ⇒ ĐỎ trên bản in xanh (T' nhận vì đếm nguồn regex) |
| thứ tự / số lần | `D14` grammar lookahead bắt cặp DOT BIEN TRƯỚC cặp CA (cùng tập span, thứ tự đảo) | 1 | 0 | **0** | **1** | danh sách ≠ tập: đột biến so TẬP (`mH8`) nhận ca này |
| bản ghi 0 cặp | `D15` thêm bản ghi `("TONG: DAT", "TONG: DAT")` 0 nhóm | 1 | 0 | **0** | **1** | luật 7 H đòi ≥ 1 cặp (răng của `mH10`) |
| `nhanh` | `D12` `8/8\n0/0` · `D12b` `8/8\n0/0 (xong)` | 1 · — | 0 · 0 | 1 · 0 | **1 · 0** | bộ chọn neo cuối dòng — ranh giới công khai từ lượt 3 |
| số quá dài | `D9` `9…9/9…9` (5000 chữ số) | — | EXC | EXC | **EXC** | `int()` ném `ValueError` (Python 3.11 trần 4300 chữ số) ⇒ ngoại lệ lan ra `chay_moi` ⇒ `rc≠0` — fail-closed ồn ào, không xanh; BASE/T' y hệt |

Năm ranh giới của H (`D1` · `D2` · `D3` · `D9` · `D12b`) chép vào `chua_do_duoc` #1 cùng 49 ranh giới cũ;
Đ1 của `§12` đếm ca **ngoài** danh sách ấy.

**Răng của từng luật — 14 đột biến áp vào NGUỒN của hai khối mã H** (thay chuỗi; bộ đo ép nguồn phải
THAY ĐỔI), đo 00:15Z 07-09-2026 trên 311 hàng có kỳ vọng. Cột *"chỉ nó bắt"* tính **trừ `mH4`** (bỏ hẳn
`TONG` = A-a, siêu-đột-biến). Ca mà đột biến làm vị từ **ném ngoại lệ** thay vì đổi màu **không tính** là
răng (`CLAUDE.md`: *đột biến bị giết không phải bị giết đúng lý do*): `mH7` trên `D4`/`D7`, `mH9` trên `D7`
— ghi riêng ở `do_h.json` → `rang_dot_bien_NGOAI_LE_khong_tinh`:

| đột biến vào H | luật | ca đổi màu / 311 | chỉ nó bắt (trừ mH4) | ca chứng |
|---|---|---:|---:|---|
| mH1 `len(hits) != 1` → `not hits` | 3 | 45 | 27 | hai bản ghi cùng loại về `0`; 13/16 ca selector về `0` |
| mH2 `fullmatch` → `search` | 4 | 2 | 2 | ` rác` sau dòng tổng probe #1 / #3 về `0` — chỉ 2 vì luật 7 vị trí đã chặn mọi đuôi mang cặp |
| mH3 `cap += c` → `cap += [("1", "1")]` (có bản ghi, không soi số thật) | 5 | 33 | 16 | `0/0`, `n ≠ m`, `CA 0/n` về `0` |
| mH4 bỏ hẳn `TONG` (= A-a) | 2–5, 7 | 113 | — (siêu) | 10 ca chỉ nó bắt: ba `D16` (SPAN 0 nhóm, chỉ bản ghi đo được), `D1b`/`D4`/`D5`/`D7` (grammar lỗi chỉ bản ghi thấy), `rỗng rồi xanh`, `đuôi thêm 0/0 cùng dòng`, `two_labels_same_line` |
| mH5 thêm lại quét nhãn `NHAN` (A-c) | 6 | 29 | 18 | `Ghi chú: DOT BIEN đã xem 3/5 …` lên `1` |
| mH6 `cap = []` → `cap = _cap(m.groups())` (nhóm `SPAN` trở lại) | 5 | 16 | 8 | `Ghi chú: ví dụ nền: 3/5 đạt` TRƯỚC bản in lên `1` |
| **mH7 `covered != actual` → `False`** (bỏ phủ vị trí) | **7** | 12 | 9 | grammar bỏ nhóm bắt + `0/0` · + `34/34` · 5 countermodel `law7` · `optional-version-present` · `D6` · `D14` về `0` |
| mH8 so **TẬP** thay danh sách | 7 (thứ tự/số lần) | 1 | 0 (⊂ mH7) | `D14` (thứ tự đảo) về `0` — ca chứng riêng cho "danh sách, không phải tập" |
| mH9 chỉ so **SỐ LƯỢNG** (≈ luật 7 của T') | 7 (vị trí) | 3 | 0 (⊂ mH7) | `overlapping-captures` · `D6` · `D14` về `0` |
| mH10 `if not c` → `if c is None` | 7 (≥ 1 cặp) | 1 | 1 | `D15` về `0` |
| mH11 trả 8 bộ chọn về T' | 2 | 23 | 5 | **16/16** ca selector về `0` (+ 4 `D8`, `D10`, 2 `D13`) |
| mH12 ba hằng probe bỏ nhóm bắt | 7 (dữ liệu) | 18 | 15 | bản in THẬT `probe` lên `1` — grammar lỗ làm đỏ ngay bản in xanh |
| mH13 bỏ `bool(cap)` | — | **0** | 0 | **không có ca**: mã chết (xem trên) — nói thẳng, không khai là chốt |
| mH14 bỏ `> 0` | 5 | 17 | 0 (trùng mH3) | `0/0` về `0` |

Kill-list đầy đủ theo tên ca: `do_h.json` → `rang_dot_bien_ca` / `rang_dot_bien_chi_no_bat_ca`. Reviewer
lượt 4 khai *"bỏ kiểm vị trí ⇒ 7 ca đổi màu; trả selector pretooluse cũ ⇒ 7 ca"* trên bộ của họ; bộ này
cho 12 và 23 vì rộng hơn và `mH11` trả CẢ 8 bộ chọn, không riêng `pretooluse` — hai bộ khác nhau, không
chép số qua lại.

**A2 dưới H** (ma trận số nhóm 0..4 × có/không `TONG`, 20 ô): **20/20** khớp cột kỳ vọng của bảng A2
(`do_h.json` → `A2_dat: true`, 00:15Z 07-09-2026). **B-tự nhiên vẫn là cái BẪY** — mệnh đề
`len(m.groups()) != 2` của BASE trả `True` vô điều kiện cho mẫu 0/1/3/4 nhóm (đo lại 21:07Z 06-09) — và H
gỡ nó bằng luật 5 y như T.

**H không đổi hành vi Windows của #456** — cùng giá trị với BASE ở 5 ca `win-*` đã đo từ lượt 2 (dòng
Windows trên Linux `1` · trên Windows `0` · dòng Linux đầy đủ trên Windows `0` · `0/0 bi giet` trên Windows
`1` · `CA 0/39` trên Windows `1`), cộng hai chốt mới `0/0 bi giet` trên **Linux** `1` và **hai** dòng
Windows `1` (BASE `0` cả hai), cộng `windows-malformed-duplicate` (tổng Windows xanh + `TONG: CA\t0/0 dat`
trên Windows) `1` (BASE/T' `0`) — bộ A/B/D, 00:15Z 07-09-2026. Grammar Windows giữ `[1-9]\d* muc` **không**
nhóm bắt cho số mục (không phải cặp); bắt nó thành 1 nhóm ⇒ nhóm LẺ ⇒ ĐỎ (`D5`).

### Ca đang khoá chiều "vẫn còn lỗ"

`p456-linux-nhan-0-tren-0-Y-HET-base` trong `.claude/dev/ci_dang_ky_test.py:474`
(`_dem_nen(_RONG456, False) == 0`) **cố ý** khẳng định rằng Linux VẪN nhận `0/0`. Packet này làm
mệnh đề ấy sai, nên ca ấy phải **đảo chiều**, không phải bị xoá — xem `nghiem_thu` A5.

### Lease đang giữ write set — PHẢI THU HỒI TRƯỚC KHI CẤP, và "thu hồi" nghĩa là gì

Đo 17:46Z 06-09-2026, `python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py`:

```
NGƯỜI_GIỮ 1: mutant-khong-chay-tren-windows-exec-1-claude-20260906
```

Lease ấy cấp `14:30:07Z 06-09`, hết hạn `14:30:07Z 07-09` — còn ~20,7 giờ hiệu lực lúc 17:46Z
trong khi packet #456 **ĐÃ LAND** (PR #457 merge vào `1b3caa1`). Nó giữ cả
`.claude/dev/ci_dang_ky_test.py` lẫn `.claude/hooks/pretooluse_guard_test.py`. Đây đúng nợ
`AG-T0-01B-thu-hoi-lease-chua-co-duong` mà `CLAUDE.md` đã đo một lần trên packet `#355`.

Phép quét hai nguồn (đo lại 19:29Z): `git ls-remote --heads origin` = **298** ·
`git for-each-ref refs/remotes/origin` (bỏ `HEAD`) = **298** · `comm -23` **rỗng** ⇒ không mù ref.
(Lúc 17:46Z là `295/295`; ba nhánh mới xuất hiện trong khoảng đó — số trôi, kết luận không.)

**Bốn tệp nháp của đợt này từng bị bộ quét tính là lease thật** (verdict lượt 1, P1
`lease-nhap-bi-tinh-la-dang-giu`): `ai-dang-giu` không gọi `check`, chỉ đọc mọi blob dưới
`ops/leases` có đuôi `.yaml`/`.yml` (`ops/lease_publish.py:521`) và phân loại theo hạn. Đo 19:33Z
trong bản sao có đủ **299** ref của kho: `ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 4` · `ci.yml` ⇒ `1` ·
`subagent_ghi_detect_test.py` ⇒ `1` · `nhanh_don_duoc_test.py` ⇒ `1`. Chữa: nháp lưu với đuôi
**`.yaml.nhap`** — bộ quét bỏ qua, `ops-publish-lease.yml` (paths `**.yaml`/`**.yml`) không bắn,
`t23` của `ops/lease_publish_test.py` (lọc `suffix in (".yaml", ".yml")`) không đọc. Đo lại 19:34Z
sau khi commit đổi tên trong bản sao và cập nhật ref remote-tracking cùng tên (mô phỏng trạng thái
SAU push — trên kho thật số này chỉ đúng sau khi commit đổi tên được đẩy):
`ci_dang_ky_test.py` ⇒ **`NGƯỜI_GIỮ 1`** (chỉ còn #456) · ba đường kia ⇒ **`0`**. `check` vẫn
chạy được trên tên `.nhap` — đo lại 21:00Z 06-09-2026 trên cây này, cả bốn nháp: `rc=8`, thiếu
**ba** trường `packet_issue`, `granted_by`, `lease_expires_at_utc` (bản này đã bỏ hạn điền sẵn nên
hạn cũng thành ô trống; số 19:31Z "thiếu hai trường" là của bản trung gian còn hạn mặc định, không
phải của nháp hiện tại). **Đổi tên về `.yaml` là BƯỚC CUỐI khi cấp thật**, sau khi đã điền đủ các ô.

**Thu hồi #456 phải phủ MỌI bản — cơ chế đo trên tập ref THẬT của cây này** (verdict lượt 1 P1 và
lượt 2 P1 `bia-mo-mot-ref-khong-thu-hoi-moi-ban`; bản lượt 1 viết hai lối ra mà lối "đợi hết hạn"
**không chạy được như đã viết** — reviewer đo `_kiem_bia_mo` vẫn `rc=8`; sửa ở đây):

- Trước mọi phép đo ref, so HAI NGUỒN (`CLAUDE.md` mục `for-each-ref`), 20:59:53Z 06-09-2026:
  `ls-remote --heads` **298** · `for-each-ref refs/remotes/origin` (bỏ `HEAD`) **298** · `comm -23`
  rỗng · `comm -13` rỗng ⇒ không mù.
- Lease #456 là **1 blob** (`8b2103c`) trên **10 ref** ở cây này (20:59:59Z): `refs/heads/master` ·
  `refs/heads/claude/soan-spec-3-viec-treo-20260906` · `origin/HEAD` · `origin/master` ·
  `origin/ops/cap-lease-456` · `origin/claude/cap-nhat-trang-thai-pr-taxzax` ·
  `origin/claude/soan-spec-3-viec-treo-20260906` · `origin/claude/elegant-bun-cd554f` ·
  `origin/claude/priceless-volhard-329577` · `origin/claude/tra-luat-process-review-o4d7kb`. Sandbox
  reviewer lượt 2 đếm **9** vì không có `refs/heads/master` — hai topology, hai số; con số có nghĩa
  là của máy CHẠY `ai-dang-giu`, phải đếm lại tại đó, không chuyển số giữa hai máy.
- Quan hệ với `origin/master` (ahead/behind, 20:59:59Z): `ops/cap-lease-456` **0/3** ·
  `claude/cap-nhat-trang-thai-pr-taxzax` **0/1** · `claude/elegant-bun-cd554f` **1/0** ·
  `claude/priceless-volhard-329577` **1/0** · `claude/tra-luat-process-review-o4d7kb` **38/0** ·
  `claude/soan-spec-3-viec-treo-20260906` (nhánh của chính hồ sơ này) **3/0**.
- **Hai cổng đọc `thay_the_cho`/`da_bi_thay_the` theo hai luật KHÁC nhau**, đo lại 21:02Z trên cây
  này:
  - `check` (`_kiem_bia_mo`, `ops/lease_publish.py:595`): với `thay_the_cho` còn tên thì đòi **ít nhất
    một** bản (`any`) của lease cũ mang `da_bi_thay_the: <lease mới>`, và **không nhìn hạn**. Nháp
    GATE điền tạm sáu ô (issue `999`, `ducthangho`, hạn `2026-09-08T15:00:00Z`) trong thư mục tạm,
    `--root` trỏ cây này: giữ `thay_the_cho: [#456]` ⇒ **`rc=8`** (*"chưa mang dòng
    `da_bi_thay_the`"*); `thay_the_cho: []` ⇒ **`rc=0`** (`ĐĂNG ĐƯỢC`) — **ngay lúc #456 còn
    `CÒN_HẠN`**. Tức `check` **không chặn chồng lấn write set**; bia mộ chỉ là điều kiện của trường
    `thay_the_cho`, và chốt duy nhất canh hai writer là `ai-dang-giu`.
  - `ai-dang-giu` (`:935`): cộng **mọi** bản `(blob, path)` trên mọi ref; bản `CÒN_HẠN` không mang bia
    mộ HAI CHIỀU là người giữ; bản `HẾT_HẠN` **không được đếm**, bất kể bia mộ. Đo với đồng hồ giả
    (`_phan_loai_lease(lease, bay_gio)`, cùng tập ref thật): `14:30:06Z 07-09` ⇒ `NGƯỜI_GIỮ 1` ·
    `14:30:07Z 07-09` ⇒ **`NGƯỜI_GIỮ 0`** (so hạn bằng `<=`).

**Hai lối ra, viết đủ ĐIỀU KIỆN THỰC THI** — áp cho từng mắt xích `#456 → GATE → LO → 2A → 2B`.
Tiền nhiệm trực tiếp của LO là **GATE**, và hạn của GATE là `lease_expires_at_utc` chủ kho điền lúc
cấp GATE — **không** phải `14:30:07Z 07-09-2026` của #456 (verdict lượt 2: đợi #456 hết hạn không làm
GATE hết hạn).

**(a) Đợi tiền nhiệm HẾT HẠN — đường mặc định của bốn nháp.**
1. Đo lại hai nguồn ref (`comm`), rồi `ai-dang-giu` cho **mọi** đường trong write set. Còn một dòng
   `CÒN_HẠN` của tiền nhiệm ⇒ chưa tới lúc; không có gì để "xử" ở bước này ngoài đợi.
2. Điền sáu ô; **`thay_the_cho: []`**; tên tiền nhiệm ghi ở chú thích ngay trên trường ấy — dấu vết
   audit, không phải điều kiện cổng. Lý do: `_kiem_bia_mo` không miễn cho `HẾT_HẠN` (đo `rc=8`), còn
   bia mộ trên một lease đã hết hạn không đổi kết quả `ai-dang-giu`. Đường khác cũng chạy được — giữ
   tên và thêm `da_bi_thay_the` vào tệp lease cũ trên nhánh `ops/**` cấp lease (`check` `any` qua) —
   nhưng nó sửa một tệp ngoài write set của packet và không mua thêm phép đo nào; **không chọn**.
3. `check` ⇒ `rc=0`; đổi tên `.nhap → .yaml`; commit; đẩy nhánh `ops/**` — cổng đọc từ REF, chưa
   commit thì `rc=8` (`CLAUDE.md`, bài học lease `#355`).
4. **SAU** khi cấp: `ai-dang-giu` lại cho mọi đường ⇒ `NGƯỜI_GIỮ 1` và tên ấy là lease vừa cấp — đó
   là A8. Ref mới xuất hiện giữa hai lần đo (nhánh phiên khác fork từ master cũ) mang blob cũ
   `HẾT_HẠN` ⇒ vẫn không đếm; mang blob cũ `CÒN_HẠN` không xảy ra ở đường này vì tiền nhiệm đã hết
   hạn trước bước 1.

**(b) Cấp TRƯỚC khi tiền nhiệm hết hạn — điều kiện thực thi, không phải lời hứa.** Cần **đồng
thời**:
1. tệp lease tiền nhiệm mang `da_bi_thay_the: <lease mới>` trên nhánh `ops/**` cấp lease (chủ kho
   làm — `check` của lease mới đòi bia mộ ấy **đã commit**), và lease mới khai `thay_the_cho`;
2. **mọi** ref còn giữ blob CŨ (chưa bia mộ) của tiền nhiệm phải hoặc được cập nhật tới blob mới,
   hoặc biến mất, **trước** khi bắt tay — vì `ai-dang-giu` đếm từng bản. Với #456 hôm nay:
   `ops/cap-lease-456` và `claude/cap-nhat-trang-thai-pr-taxzax` (0 ahead) xoá được qua
   `ops-don-ref.yml` (chốt `behind_by = 0`, `.github/workflows/ops-don-ref.yml:256-264`); ba nhánh
   `claude/elegant-bun-cd554f` · `claude/priceless-volhard-329577` ·
   `claude/tra-luat-process-review-o4d7kb` còn **1/1/38** commit ngoài master ⇒ workflow ấy **từ
   chối** (`DỪNG: … còn N commit CHƯA có trong master`); chủ kho chấp thuận bằng lời cũng không làm nó
   cho qua. Chúng chỉ rời phép đếm khi (i) phiên giữ nhánh land, hoặc merge master đã mang bia mộ vào
   nhánh mình; (ii) chủ kho xoá/ép nhánh bằng thẩm quyền riêng NGOÀI workflow — hành động ngoài kho
   này, và phải readback; hoặc (iii) chờ tới hạn — tức quay về (a). Không kết luận "không bao giờ
   xử được"; kết luận là **không xử được từ packet này**.
3. Readback: `ai-dang-giu` ⇒ **0** dòng của tiền nhiệm thiếu `ĐÃ_BỊ_THAY_THẾ`/`HẾT_HẠN`. Không đạt
   ⇒ **không bắt tay**; `check rc=0` không thay được phép đo này (đo 21:02Z ở trên).

Ghi vào `granted_on_instruction` lối nào đã chọn. Nợ gốc vẫn là
`AG-T0-01B-thu-hoi-lease-chua-co-duong`; mặt đo được ở đây: **`_kiem_bia_mo` đếm `any` và không
nhìn hạn, còn `ai-dang-giu` đếm mọi bản và chỉ nhìn hạn** — sửa là việc của một packet chạm
`ops/lease_publish.py`, ngoài phạm vi này.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng THÊM** (cột `additions` của `git diff --numstat`,
không phải thêm-trừ-xoá). Write set là **1 tệp**. Ước cũ *"≈ 10 dòng vị từ + `NHAN` 1 dòng + ≈ 40
dòng phản chứng ⇒ dưới 100"* là ước của **A-c** (bản lượt 1) và bị rút; `NHAN` không tồn tại trong H.
Kích thước hai khối mã của từng bản, đo **đúng thước `ADR-0044`** — cột additions của
`git diff --no-index --numstat <tệp rỗng> <khối>` (00:11Z 07-09-2026; lệnh trả `rc=1` vì có diff, không
phải lỗi): T' tại `e5ab4b7` **21 + 26** (bản lượt 3 ghi `21 + 22` — số dòng của vị từ T lượt 2 chưa cập
nhật theo T', P3 lượt 4) · **H (bản này) 21 + 29**. Đó là số dòng NGUỒN của hai khối mẫu, **chưa phải**
additions của bản thi công: còn phần ghép kiểu giá trị `MOI`/`MOI_WINDOWS`, các ca A1–A6 mới trong
`phan_chung()`, và có dòng cũ được thay. `git diff --numstat 1b3caa1..e5ab4b7 -- .claude/dev/ci_dang_ky_test.py`
rỗng — chưa có thi công nào để đo tổng; không suy từ net, không suy từ diff tài liệu. Phiên thi công đo
`git diff --numstat` trước review; vượt `300` thì DỪNG (Đ4) — không cắt ca để lách, không nâng trần.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/dev/ci_dang_ky_test.py` | nơi `bang_chung_xanh` sống, và nơi phản chứng của chính nó sống |

Không ký tự đại diện. Không đường dẫn nào khác.

Đo 17:48Z 06-09-2026: `rg -n 'bang_chung_xanh' --glob '!*.md'` ngoài tệp này ⇒ **0 kết quả**. Hàm
không có caller nào khác trong kho, nên write set một tệp là ĐỦ chứ không phải là cắt gọt.

Giao write set: `GATE-TACH-JOB-CAT-CHI-PHI` (sửa `loi_ruff_ci` trong cùng tệp) ·
`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT` · `MUTANT-WINDOWS-NHANH-DON-DUOC`. Thứ tự nối tiếp:
**GATE → LO (packet này) → 2A → 2B**.

## `ngoai_pham_vi`

1. **`MOI` và `MOI_WINDOWS` ĐƯỢC sửa — nhưng chỉ đổi KIỂU giá trị, không đổi chuỗi `SPAN`.** Quyết
   định *"không sửa một ký tự"* của hai bản đầu được mở lại có chủ ý từ bản lượt 2, vì A-c bị bác
   bằng phép đo (bảng *"Các hướng vá đã ĐO"*). Chuỗi regex `SPAN` của 8 mục và của `MOI_WINDOWS`
   giữ NGUYÊN VĂN — thứ thêm là `TONG` đi kèm. Hai ca neo `p456-mau-linux-KHONG-DOI-so-voi-base` và
   `p456-linux-A-B-tung-dau-vao-khop-base` đổi neo theo A5, không xoá.
2. **Không đụng `.claude/hooks/pretooluse_guard_test.py` hay
   `.claude/hooks/subagent_ghi_detect_test.py`.** Bản in của chúng đã đúng (`34/34`, `22/22`);
   thứ hỏng là bên ĐỌC, không phải bên IN.
3. **Không cắt vòng lặp đột biến của bộ nào khỏi Windows** — đó là hai packet riêng
   (`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`, `MUTANT-WINDOWS-NHANH-DON-DUOC`). Gộp vào đây là 3 tệp
   và một write set giao nhau ba chiều; `ADR-0044` đo được giá của việc ấy (`PLAT-X4` 4 tệp ⇒
   3 vòng, 8 finding).
4. **Không đụng `.github/workflows/ci.yml`.** Packet này không đổi thời gian chạy của bất cứ thứ
   gì; nó chỉ làm một cổng đang mù nhìn thấy.
5. **Không đụng `loi_ruff_ci`** trong cùng tệp — đó là việc của `GATE-TACH-JOB-CAT-CHI-PHI`, và
   GATE đi trước; khi packet này bắt tay, hàm ấy đã ở dạng mới.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `bang_chung_xanh` đọc **bản ghi tổng** của từng mục theo `(BỘ CHỌN, GRAMMAR)`: đúng MỘT dòng, khớp TRỌN, số CHỈ từ dòng tổng, mọi cặp `int(n) == int(m) > 0`, mọi cặp `_CAP` tìm được trên dòng tổng được **nhóm bắt của match phủ đúng vị trí, đúng thứ tự, đúng một lần** (luật 1–5, 7). `DOT BIEN 0/0 bi giet` trong bản ghi bị từ chối trên **mọi** nền — kể cả khi nó nằm ở đuôi dòng tổng, khi grammar quên nhóm bắt, hay khi hằng nằm ở nhánh regex không tham gia match. | `write_set` #1 |
| M2 | Mệnh đề thoát `len(m.groups()) != 2` bị **gỡ**: nhóm bắt soi theo cặp với mọi số nhóm chẵn; LẺ ⇒ `False`; `0` nhóm và `0` bản ghi ⇒ `False`. Không còn số nhóm nào cho `True` vô điều kiện. | `write_set` #1 |
| M3 | Văn xuôi không là bằng chứng (luật 6): dòng không khớp bộ chọn nào không được đọc, kể cả khi mang nhãn `CA`/`DOT BIEN`/`ĐỘT BIẾN` hay cặp số. Tổng TRÙNG và tổng SAI CẤU TRÚC là ĐỎ. | `write_set` #1 |
| M4 | Đường Windows của #456 giữ nguyên năm hành vi đã đo; dòng Windows có grammar riêng (`[1-9]\d* muc`, không nhóm bắt cho số mục); thêm ba chốt mới (`0/0` trên Linux, hai dòng Windows, tổng Windows xanh + `TONG: CA\t0/0 dat` trên Windows). | `write_set` #1 |
| M5 | Ca `p456-linux-nhan-0-tren-0-Y-HET-base` **đảo chiều và đổi tên**; hai ca neo mẫu đổi neo sang `SPAN` (chuỗi cũ nguyên văn) + `TONG` canonical; không ca nào bị xoá. | `write_set` #1 |
| M6 | Đủ **8** định dạng có phản chứng qua `chay_moi` từ bản in nguyên byte (7 thật + canonical `pretooluse`); mỗi luật 2–7 có đột biến làm ít nhất một ca đổi màu (bảng răng H); `mH13` (`bool(cap)`) và `m8` cũ (wildcard) **không** được khai là răng độc lập. | `write_set` #1 |

## `nghiem_thu`

**A1 (M1) — lỗ #319 phía Linux đóng, đo bằng SỐ ĐỎ của `chay_moi`, không bằng mắt.**
`chay_moi(moi={P: MOI[P]}, chay_mot=lambda _: (0, RONG), doc_nen_windows=lambda: False)` với
`RONG = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"` ⇒ **1** (BASE `0`; T `1` 21:07Z; T' `1`
22:33Z 06-09; **H `1`** 00:15Z 07-09-2026); cùng chuỗi với `doc_nen_windows=lambda: True` ⇒ `1` (BASE `1`).
Cùng đơn vị, đo 00:15Z 07-09 dưới H: `· DOT BIEN 0/0 bi giet` nối vào đuôi dòng tổng `probe_mang` ⇒ **1**;
grammar `pretooluse` cố ý bỏ nhóm bắt cặp đột biến (`DOT BIEN \d+/\d+`) + `RONG` ⇒ **1** và + bản in xanh
`34/34` ⇒ **1** (ồn ào, không mù); **năm countermodel luật 7 của lượt 4** — hằng ở nhánh tuỳ chọn vắng mặt
`(?: \(schema 1/1\))?` · hằng ở alternative không được chọn `(?:1/1|\d+/\d+)` · hai cặp nhóm chồng vị trí
CA (lookahead) · literal `0/0` · literal `33/34` — ⇒ **1** mỗi ca (T' `0` cả năm); bản in THẬT của
`subagent_ghi_detect` (`22/22 → 0/0`) và `mcp_gh` (`54/54 → 0/0`) ⇒ `1` mỗi bộ (BASE `0`). Đi qua chính
`chay_moi` — khuyết tật "làm tròn" nằm ở NƠI TIÊU THỤ (r6/#401). Đơn vị: **số mục bị đếm là ĐỎ**. Phép
làm ĐỎ của ca: `mH7` bỏ phủ vị trí ⇒ 9 ca grammar-lỗi về `0`; `mH3` bỏ soi cặp ⇒ `RONG` về `0` (bảng răng).

**A2 (M2) — mệnh đề thoát theo số nhóm không còn.**
Năm mẫu span, số nhóm ∈ {0, 1, 2, 3, 4}; mỗi mẫu đo hai lần — **không** kèm bản ghi tổng và **kèm**
bản ghi tổng của `pretooluse`. Đo 21:07Z, trị phải đạt:

| số nhóm | `CA 0/39 · DOT BIEN 0/0` — BASE | T, không `TONG` | T, kèm `TONG` | `CA 39/39 · DOT BIEN 34/34` — BASE | T, không `TONG` | T, kèm `TONG` |
|---:|---|---|---|---|---|---|
| 0 | `True` (tha) | **`False`** (không đo gì) | **`False`** | `True` | **`False`** (không đo gì) | `True` |
| 1 | `True` (tha) | `False` (lẻ) | `False` | `True` | `False` (lẻ) | `False` |
| 2 | `False` | `False` | `False` | `True` | `True` | `True` |
| 3 | `True` (tha) | `False` (lẻ) | `False` | `True` | `False` (lẻ) | `False` |
| 4 | **`True`** (BẪY) | `False` | `False` | `True` | `True` | `True` |

Phép làm ĐỎ: bất kỳ ô nào lệch cột T (đo lại 22:33Z 06-09 trên T' và **00:15Z 07-09-2026 trên H**: 20/20 ô
khớp, `A2_dat: true` trong `do_t2.json` / `do_h.json`). Đơn vị: **giá trị trả về của `bang_chung_xanh`**. Số nhóm LẺ
trả `False` ngay cả trên bản in đầy đủ — có chủ ý; `0` nhóm **không** bản ghi cũng `False` — mẫu
không đo gì thì không phải bằng chứng.

**A3 (M3) — văn xuôi không là bằng chứng; tổng TRÙNG và tổng SAI CẤU TRÚC là ĐỎ.**
Qua `chay_moi`, đo 00:15Z 07-09-2026 dưới H (cột A-c/T' để thấy đúng chỗ H khác):
- bản in thật `chon_reviewer` + lần lượt từng ghi chú `Ghi chú: đã xem 3/5 hướng cải tiến.` ·
  `Ghi chú: DOT BIEN đã xem 3/5 hướng cải tiến.` · `Giải thích: ví dụ DOT BIEN 0/0 là bảng rỗng.` ·
  `Ghi chú: CA 0/0 là ví dụ.` ⇒ **0** mỗi ca (A-c: `0` · `1` · `1` · `1`). Cùng phép trên bản in thật
  `subagent` và `mcp_gh` ⇒ **0** (A-c `1`);
- bản in thật `probe_mang` + dòng lẻ `DOT BIEN 0/0 bi giet` hay `đã xem 0/0 hướng` ⇒ **0** (A-c:
  `1` · `0`). **Đây là chỗ H cố ý giống T, khác A-c**: dòng lẻ mang nhãn không phải bằng chứng vì không
  formatter nào in nó, và luật 6 là ranh giới đã chọn — `chua_do_duoc` #1; `TONG: CAX 0/0`, `TONG: CA. 0/0`
  cũng là văn xuôi (`D8e`/`D8f`);
- HAI bản ghi cùng loại ⇒ **1**: hai dòng `TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet` · xanh rồi
  rỗng · rỗng rồi xanh · hai dòng `CA … :` (`mcp_gh`) · hai `nền: 11/11 đạt` (`probe`) · hai
  `nền: 25/25 đạt` (`chon`) · hai dòng `gh_readback tests: 8/8 …` · hai dòng `8/8` (`nhanh`) · hai
  dòng Windows. BASE cho **0** ở cả 9 ca;
- có tiền tố tổng mà sai grammar ⇒ **1**: `DOT BIEN` + 25 khoảng trắng + `0/0` (và + `34/34`) ·
  `DOT BIEN\n0/0` · `DOT BIEN đợt 2: 0/0` · đuôi thêm `· DOT BIEN 0/0 bi giet` cùng dòng (BASE `0`
  ở ca cuối) · nhánh từ chối điểm `TONG: CA 30/33 dat` + `TONG: DIEM DOT BIEN BI TU CHOI …`;
- **tổng CỤT/TAB là bản ghi sai cấu trúc** (P1 lượt 4, phần cũ; T' bỏ sót cả 16): `TONG: CA` cụt ·
  `TONG: CA\t0/0 dat · DOT BIEN 0/0 bi giet` · `TONG: CA: 0/0 …` — mỗi dạng đặt TRƯỚC và SAU tổng xanh
  ⇒ **1**; `nền:` cụt và `nền:\t0/0 đạt` sau (và trước, `D13`) bản in thật `chon` ⇒ **1**; nhãn cụt
  `gh_readback tests:` · `CA:` · `ĐỘT BIẾN:` · `mcp_github_doc tests:` · `tự đột biến cổng:` ·
  `named mutant …:` · `nền:` (probe) sau bản in thật ⇒ **1** mỗi ca; tổng Windows xanh + `TONG: CA\t0/0
  dat` trên Windows ⇒ **1**. Không đòi formatter thật in được chuỗi lỗi mới dùng nó làm ca âm của hợp đồng;
- **văn xuôi mang tiền tố tổng đứng TRƯỚC bản in** (P1 lượt 3, chiều a) — `Ghi chú: ví dụ nền: 3/5
  đạt` trước bản in thật `chon_reviewer` ⇒ **0**; cùng kiểu cho `gh_readback`, `mcp_gh`,
  `mcp_github_doc`, `subagent`, `pretooluse` Linux, dòng Windows trên Windows ⇒ **0** mỗi ca; đặt SAU
  cũng **0** (T lượt 2 và BASE cho `1` ở 7 ca). Phản chứng tự soi: cùng ghi chú trước + `0/0` trong bản
  ghi ⇒ **1**;
- **cặp trên dòng tổng phải được PHỦ VỊ TRÍ** (luật 7 H): grammar `pretooluse` cố ý viết `DOT BIEN
  \d+/\d+` (không nhóm bắt) + `0/0` ⇒ **1**; + bản in xanh `34/34` ⇒ **1**; năm countermodel `law7` ⇒ **1**
  (A1); ba hằng probe viết KHÔNG nhóm bắt trên bản in thật ⇒ **1** (`D17`; T' `0`); ba cách viết CÓ nhóm bắt
  `(9)/(9)` · `(9)[/](9)` · `(9)\/(9)` ⇒ **0** (`D16`; T' `1` ở hai cách sau — đỏ giả của luật 7 cũ);
  grammar lỗi kiểu khác (`D4` nhóm tuỳ chọn vắng, `D5` nhóm lẻ, `D6` lệch biên số, `D7` gộp dấu gạch,
  `D14` thứ tự đảo, `D15` bản ghi 0 cặp) ⇒ **1** mỗi ca. Thay cho ca tĩnh *"tập `SPAN` ⊆ tập `GRAMMAR`"*
  của bản lượt 3 (chỉ chứng minh giá trị), `phan_chung()` phải có ca: với mỗi mục `MOI`/`MOI_WINDOWS` trên
  bản in canonical, **danh sách span** `_CAP` trên dòng được chọn == danh sách span nhóm của match; đột
  biến bỏ nhóm bắt ở bất kỳ grammar nào ⇒ ca ĐỎ;
- **đuôi lạ trên dòng tổng** (luật 4): ` rác` sau `tự đột biến cổng: … cơ chế)` ⇒ **1**; ` rác` sau
  `nền: 11/11 đạt` ⇒ **1** — hai ca chứng riêng của `mH2`.
Phép làm ĐỎ (bảng răng, 00:15Z 07-09): `mH1` ⇒ 45 ca đổi màu (hai bản ghi + 13/16 selector); `mH11`
⇒ 16/16 selector về `0`; `mH2` ⇒ 2 ca đuôi rác về `0`; `mH5` ⇒ 29 ca đỏ giả lên `1`; `mH6` ⇒ 16 ca
ghi-chú-trước lên `1`; `mH7` ⇒ 12 ca grammar-lỗi về `0`; `mH8` ⇒ `D14` về `0`; `mH10` ⇒ `D15` về `0`;
`mH12` ⇒ 18 ca probe thật lên `1`. Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A4 (M4) — đường Windows của #456 nguyên vẹn, cộng hai chốt mới.**
Qua `chay_moi` với seam `doc_nen_windows`, đo 21:07Z: dòng Windows trên Linux **1** · trên Windows
**0** · dòng Linux đầy đủ trên Windows **0** · `0/0 bi giet` trên Windows **1** · `CA 0/39` trên
Windows **1** · `DOT BIEN 0 muc` trên Windows **1** · `0/0 muc` sau nhãn trên Windows **1** — bằng
BASE; **mới**: `0/0 bi giet` trên Linux **1** và **hai** dòng Windows **1** (BASE `0` cả hai). Đo lại
00:15Z 07-09-2026 dưới H: cùng giá trị ở mọi ca trên; **thêm** tổng Windows xanh + `TONG: CA\t0/0 dat` trên
Windows ⇒ **1** (BASE/T' `0` — bộ chọn cũ đòi dấu cách).
Đột biến bắt buộc: xoá điều kiện nền trong `mau_theo_nen` ⇒ `p456-dong-windows-tren-linux-la-DO`
phải ĐỎ.

**A5 (M5) — ca cũ đảo chiều và đổi tên; hai ca neo đổi neo; KHÔNG ca nào bị xoá.**
- `p456-linux-nhan-0-tren-0-Y-HET-base` (`_dem_nen(_RONG456, False) == 0`) ⇒ `== 1`, đổi tên (đề
  nghị `lo319-linux-KHONG-CON-nhan-0-tren-0`) — tên nói *"y hệt base"* cạnh khẳng định ngược lại là
  đúng lớp lỗi *"hai lời khai mâu thuẫn trong cùng tệp"* (cross-review PR #250 lượt 3);
- `p456-mau-linux-KHONG-DOI-so-voi-base` (`MOI[_P456] == _MAU_BASE456`) ⇒ neo vào phần `SPAN`:
  `MOI[_P456][0] == _MAU_BASE456` **và** phần `TONG` bằng hằng canonical ghi cứng trong ca — chuỗi
  regex cũ vẫn phải NGUYÊN VĂN, đúng ý của ca gốc;
- `p456-linux-A-B-tung-dau-vao-khop-base` (so `bang_chung_xanh` giữa `MOI[_P456]` và chuỗi trần
  `_MAU_BASE456` trên ba đầu vào) ⇒ đầu vào `_RONG456` **cố ý lệch** dưới T/H (chuỗi trần có 2 nhóm,
  không `TONG` ⇒ `True`; mục đầy đủ ⇒ `False`); ca phải khai đúng ba giá trị mới thay vì `is` bằng
  nhau, để chính chỗ lệch ấy được ĐO chứ không bị làm phẳng.
Đơn vị: **số phản chứng đỏ đúng / tổng** — `N/N`, `N ≥ 51 + số ca mới của A1–A6`. `51` là nền
19:32Z 06-09-2026 trong CÂY THẬT — lượt này **không đo lại** (cấm chạy suite; `KHÔNG ĐO ĐƯỢC ở lượt
này (ràng buộc chủ kho)`); **đo lại tại lúc thi công**. Phép làm ĐỎ: giữ khẳng định cũ của bất kỳ
ca nào trong ba ⇒ `phan_chung()` dưới `N/N`.

**A6 (M6) — tám định dạng từ bản in NGUYÊN BYTE, và sổ đăng ký chạy thật.**
- (a) qua `chay_moi`: 7 bản in thật + canonical `pretooluse` (Linux, Windows) ⇒ **0** đỏ mỗi bộ
  (đo 21:07Z với T; đo lại 22:33Z với T', nhóm `that-*`/`canonical-*`/`*-baseline` của `do_t2.json`:
  **0**; đo lại 00:15Z 07-09-2026 với H, cùng nhóm ca trong `do_h.json`: **0**, kể cả `probe_mang` nay có
  ba hằng là nhóm bắt). `sha256` bản in, đủ để ai cũng tự đo lại: `chon_reviewer` `a5807082…` · `gh_readback`
  `0a476a97…` · `mcp_gh` `b3034838…` · `mcp_github_doc` `82f89e9d…` · `probe_mang` `c9997dac…` (5 bộ
  này chạy 21:00:15–21:00:23Z 06-09-2026 tại container soạn spec, `rc=0`) · `subagent_ghi_detect`
  `449578d8…` · `nhanh_don_duoc` `366795e4…` (bản in `rc=0` của sandbox reviewer lượt 1).
  **Bản in nằm ở đâu, nói cho đúng ở cả hai phía:** tệp nguyên byte ở gói bàn giao
  `executor-luot3-va/fixtures/*.stdout` kèm `MANIFEST.sha256` (bản lượt 2 dẫn `executor-luot2-va/…`
  — gói ấy có thật nhưng **không được giao vào sandbox lượt 3**, verdict lượt 3 P3
  `thieu-ban-in-de-do-span-mcp`; băm bảy tệp trong hai gói **trùng nhau từng byte**, kiểm 22:26Z).
  Định danh tệp là **BĂM**, không phải tên thư mục: reviewer nhận gói nào thì so băm gói ấy với bảy
  băm trên; **không có tệp mang đúng băm trong sandbox ⇒ mọi số dẫn từ bản in ấy là KHÔNG ĐO ĐƯỢC với
  reviewer**, kể cả `2171/2251` ở `chua_do_duoc` #6 — không tự sinh log mới để thay bản đã dẫn. Phiên
  thi công phải **chạy lại** 5 bộ ngắn và dùng bản in của mình; `subagent`/`nhanh`/`pretooluse` lấy từ
  lượt full-gate cuối.
- (b) `python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success` — **KHÔNG ĐO
  ĐƯỢC ở lượt này (ràng buộc chủ kho)**; full-gate cuối sau khi hết P1 trả lời.
Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A9 — bằng chứng DỊ DẠNG phải ra `ĐỎ` CÓ LÝ DO, không ra TRUY VẾT PYTHON.**
Ca `D9` (cặp `9…9/9…9`, **5000 chữ số**) làm `int()` ném `ValueError` (Python 3.11 trần **4300**
chữ số). Dưới H, ngoại lệ ấy **lan ra khỏi `chay_moi`**; `main()` ở `:542` gọi
`ok = chay_moi() == 0 and ok` **không** bọc `try` (đo 02:5xZ 07-09-2026: `grep -n except` trên tệp
cho **4** vị trí, không vị trí nào bao `chay_moi`), nên tiến trình chết bằng truy vết, `rc=1`.

**Nói cho ĐÚNG mức, vì bản đầu của mục này viết QUÁ TAY và phép đo bác nó:** `rc=1` là **FAIL-CLOSED
— cổng ĐỎ**, KHÔNG phải "cổng vắng mặt". Đo trực tiếp trên cây hiện tại (BASE, chưa có H):
`chay_moi` với cùng chuỗi 5000 chữ số trả **`1`** và **không ném gì** — `ValueError` là thuộc tính
của vị từ **H**, không phải của mã đang land. Nên đây **KHÔNG** phải lỗ an ninh và **KHÔNG** phải
điều kiện chặn lease.

Cái còn lại là thật và đáng một tiêu chí: một ngoại lệ không bắt **giết cả bộ**, nên phán quyết của
**7 định dạng còn lại bị mất** trong cùng lượt, và người đọc log thấy truy vết chứ không thấy
`ĐỎ: <lý do>`. Đó là **thiệt hại kèm theo + khả năng chẩn đoán**, không phải bằng chứng giả.

Trị phải đạt sau thi công: `chay_moi(moi={P: MOI[P]}, chay_mot=lambda _: (0, D9))` ⇒ trả **`1`**
và **không** ném ngoại lệ; **7** định dạng còn lại vẫn được phán quyết trong cùng lượt (đếm số mục
đã xét = **8**). Đơn vị: **số mục bị đếm là ĐỎ** và **số mục được xét**. Phép làm ĐỎ: gỡ chốt
chiều-dài/`try` ra ⇒ ngoại lệ lan ⇒ số mục được xét tụt xuống **< 8**. Cách đạt là lựa chọn của
phiên thi công (so chuỗi chữ số đã bỏ số 0 đầu thay vì `int()`, hoặc chặn theo độ dài, hoặc bọc
`try` trả `False`); đặc tả **không** chỉ định cách, chỉ chỉ định TRỊ.

**A7 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **1** đường dẫn.

**A8 — tiền nhiệm không còn giữ TRƯỚC khi bắt tay, đo trên MỌI bản, bằng `ai-dang-giu` chứ không
bằng `check`.**
Sau khi cấp, `python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py` phải:
- in `NGƯỜI_GIỮ 1` và tên ấy là lease của **packet này**;
- **0** dòng mang `lease_id` của GATE (tiền nhiệm trực tiếp) hoặc của `#456` mà thiếu `ĐÃ_BỊ_THAY_THẾ`
  lẫn `HẾT_HẠN` — `grep <lease_id> | grep -v 'ĐÃ_BỊ_THAY_THẾ' | grep -vc HẾT_HẠN` ⇒ **0**.
`check rc=0` **không** thay được phép đo này: đo 21:02Z 06-09-2026, `check` cho `rc=0` với
`thay_the_cho: []` ngay khi #456 còn giữ. Phép làm ĐỎ: chạy trước khi tiền nhiệm hết hạn (đường a)
hay trước readback thu hồi (đường b) ⇒ ra tên lease khác ⇒ DỪNG, không bắt tay. Đường (a) đo được
ngay sau `lease_expires_at_utc` của GATE (mô phỏng 21:02Z với #456: `NGƯỜI_GIỮ 1 → 0` đúng tại giây
hết hạn); đường (b) chỉ đo được sau readback ở mục *"Lease đang giữ"* (b)3.

## `hinh_dang_ke_thua`

Bộ đếm **hình dạng lỗi**, chép từ `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` và từ hồ sơ
`CI-CAI-JSONSCHEMA` (r1→r2→r3), cộng thêm những gì packet này đo được. Mỗi dòng ghi thời điểm đo
hoặc nguồn trích (L5):

| hình dạng | số lần đã gặp | đo/trích lúc (đọc lại 21:03Z 06-09-2026 trên `b1c2284`) | ghi chú |
|---|---:|---|---|
| tập RỖNG thoả `not song` (`0/0` được nhận là bằng chứng) | **3** | trích `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md:137-140` (đọc lại 21:03Z) + đo B1 19:32Z và đo lại A1 21:07Z, 22:33Z 06-09-2026 | #319 (gốc) · #456 đường Windows (đã bịt) · đường Linux (packet này). Lần thứ ba ⇒ `PROTOCOL §12` đòi xem lại CÁCH LÀM: câu trả lời là **bịt ở vị từ dùng chung**, không bịt ở từng mẫu. Lần thứ tư **suýt** xảy ra trong chính bản nháp T lượt 2 (`(?: .*)?` cho `0/0` lọt ở đuôi dòng tổng — reviewer lượt 3 đo 22:10Z); chưa thi công nên không đếm, nhưng luật 7 sinh ra từ đó. |
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức: `25` khởi tạo `9e4f361` → `45` `6d88a2c` → `60` `7657bfd`) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml` chạy lại 21:03Z 06-09-2026: `9e4f361` (2026-07-09) · `6d88a2c` (2026-08-29 03:29Z) · `7657bfd` (2026-08-29 04:49Z) | Bản đầu chép `3` từ #456; #456 đếm MỨC chứ không đếm LẦN NÂNG (verdict lượt 1, P2). Lần nâng kế tiếp là lần **thứ ba** ⇒ `§12`. Packet này không đụng `ci.yml`. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** | trích `ops/specs/CI-CAI-JSONSCHEMA-r3.md:135-160` (A5), đọc lại 21:03Z 06-09-2026 | Đã đo được ở #456. Sự kiện lịch sử, không tái chạy. |
| cổng vắng mặt trông giống cổng xanh | nhiều | trích `CLAUDE.md` (mục dấu bỏ-qua-CI / PR #100; `ops-don-ref.yml` run `31971137920`), đọc lại 21:03Z 06-09-2026 | Ở đây: cổng CÓ MẶT, CÓ CHẠY, và vẫn không đo — biến thể đắt hơn. Sự kiện GitHub không readback lại ở lượt này. |
| lease không tự chết khi packet đã land | **2** | `#355`: trích `CLAUDE.md` mục *"LEASE KHÔNG TỰ CHẾT KHI PACKET ĐÃ LAND"*, đọc lại 21:03Z; `#456`: đo 17:46Z và **đo lại 21:00Z 06-09-2026** (`ai-dang-giu` ⇒ `NGƯỜI_GIỮ 1`, còn ~17,5 giờ) | Xem A8. |
| lời khai rộng hơn phép đo | **4** — đều ở BẢN NHÁP đặc tả, **0** trong mã đã land (bản đầu: *"A-b không sinh đỏ giả"*; lượt 1: *"mọi cặp mang nhãn được kiểm"* trong khi `[^\n\d]{0,24}?` bỏ sót; lượt 2: *"T: đỏ giả 0, bỏ sót 0"* trong khi prototype còn đọc nhóm `SPAN`; **lượt 3: *"T': 0/137"* và *"hợp đồng T đúng, chỉ gỡ mâu thuẫn, không có thiết kế thứ tư"* trong khi bộ 131 đã giao còn 16 bỏ sót và luật 7 đếm nguồn regex**) | verdict lượt 1 tái hiện 19:32Z; lượt 2 21:07Z; lượt 3 22:10Z 06-09-2026; lượt 4 `prior131.json`/`law7.json`, executor đo lại 00:15Z 07-09-2026 | Cùng họ *"thu hẹp mà viết thành đóng"* trong `CLAUDE.md`. Lần thứ ba đã kích `§12` ở lượt 3, và câu trả lời khi ấy **tự nó là lần thứ tư**. Bản này: mọi điểm hai chiều là `X/N trên bộ ca S` kèm băm bộ đo + danh sách lớp chưa phủ, **và** câu hỏi `§12` chuyển cho chủ kho với ba lựa chọn + năm điều kiện đo được — không tự trả lời lần nữa. |
| vùng bằng chứng không được khoanh đủ (A-b, A-c, mảnh `SPAN`/`.*` trong T, **hằng trong mã regex ở T'** — và bộ chọn đòi payload ở cả T lẫn T') | **4** — đều ở BẢN NHÁP, **0** trong mã đã land | verdict lượt 1 (19:32Z), lượt 2 (21:07Z), lượt 3 (22:10Z 06-09-2026), lượt 4 (`law7.json` 3 đỏ giả / 5 bỏ sót trên 11; `prior131.json` 16 bỏ sót trên 131); executor đo lại 00:15Z 07-09-2026 | **Lần thứ tư ⇒ `§12` lần hai**, mục *"§12 — bốn lần hỏng"*: H đổi phép chứng minh sang phủ VỊ TRÍ (0/0 trên 311 hàng đo, 5 ranh giới mới), nhưng H là bản thứ NĂM của cùng cách làm; tiếp / đổi bên IN / tách lại là quyết định của chủ kho, chốt tự động Đ1–Đ5. |

## `chua_do_duoc`

1. **Giá của luật 6 và luật 7 — văn xuôi không được đọc, hợp đồng là HỮU HẠN, và định nghĩa "cặp" là
   `_CAP`.** H không hứa đọc mọi cặp có nhãn ở mọi vị trí văn bản; một bộ TƯƠNG LAI in bằng chứng ngoài
   bản ghi tổng đã khai sẽ không được canh cho tới khi có grammar riêng; đổi formatter ⇒ phải đổi `TONG`
   rồi chạy lại bộ ca + bản in thật. Nợ có tên **`GRAMMAR-TONG-LA-HOP-DONG-HUU-HAN`**. Rủi ro ngược —
   grammar quá chặt bác một formatter hợp lệ — đo được ở A6(a): 7 bản in thật ⇒ `0` đỏ (00:15Z 07-09-2026
   dưới H); **chưa đo** trên bản in thật của `pretooluse` (mục 2, 4) và trên **Windows** (mục 3).
   **Metadata `n/m` trên dòng tổng KHÔNG được hỗ trợ** — H bác `bi giet (schema 1/2)` (Đ3); muốn có thì
   revision schema vai trò, không miễn kiểm bằng cách đếm hằng trong mã regex.
   **Lớp CHƯA PHỦ, liệt kê để không ai đọc "0/311" thành "0 với mọi cách in":**
   · 49 ca ranh giới reviewer lượt 3 dựng và cố ý không đặt kỳ vọng (`do_t2.json` → `ranh_gioi_T'`; giá
   trị H đo lại 00:15Z 07-09-2026 **y hệt T'** ở cả 49, `do_h.json`): thêm khoảng trắng cuối dòng tổng ·
   hậu tố ` (xong)` · thụt lề dòng tổng · mã màu ANSI ⇒ **từ chối** (8/8 định dạng mỗi kiểu) — giá của hợp
   đồng hữu hạn, và reviewer kiểm tĩnh không thấy tuỳ chọn formatter hiện tại nào in các biến thể ấy qua
   đường capture; dòng tổng RỖNG **thụt lề** đứng sau tổng xanh ⇒ **nhận** (8/8: ngoài bộ chọn, luật 6 —
   ranh giới thật, không phải "an toàn"); CRLF thô ⇒ nhận 7/8, `nhanh` từ chối vì `SPAN` neo `$` — mà
   `_chay_that` dùng `subprocess.run(text=True)` nên đường thật đã chuẩn hoá về LF
   (`consumer_normalized_CRLF` ⇒ 0 đỏ 8/8); `nhanh` + dòng `0/0 (xong)` ⇒ nhận (bộ chọn neo cuối dòng).
   **Tổng cụt/tab đầu dòng KHÔNG thuộc nhóm này** — chúng là 16 ca có kỳ vọng của verdict lượt 3, H đếm ĐỎ
   cả 16.
   · **5 ranh giới mới của H** (bộ D, 00:15Z 07-09-2026): `D1` chuỗi `54/54/0` khi tác giả grammar khai
   `(\d+)/(\d+)/\d+` ⇒ nhận (`_CAP` không coi `/0` là cặp; SPAN `pretooluse` chặn ca tương đương, `mcp`
   thì không) · `D2` `039/39` ⇒ nhận (so số nguyên; T' bác) · `D3` chữ số Unicode `３９/３９` ⇒ nhận
   (`\d` Unicode) · `D9` số 5000 chữ số ⇒ `ValueError` lan ra `chay_moi` ⇒ `rc≠0` (fail-closed, cổng
   ĐỎ — **nay có tiêu chí A9**, không còn chỉ là ranh giới khai suông; BASE trả `1` mà KHÔNG ném) · `D12b` `nhanh` `0/0 (xong)` ⇒ nhận. Không formatter hiện có in ca nào trong năm ca ấy.
   Siết `_CAP` (`[0-9]`, cấm `/` kề cặp) là lựa chọn của phiên thi công; đổi khối mã thì đo lại toàn bộ.
   Đổi formatter ⇒ phải khai lại `TONG` và chạy lại toàn bộ bộ ca; **không** được nới grammar bằng `.*`
   hay bỏ nhóm bắt để "qua" — luật 7 H làm ĐỎ ngay bản in xanh, và đó là kết quả đúng.
2. **Nền của `pretooluse_guard_test.py` KHÔNG xanh trong container soạn spec.** `rc=1`,
   **270 giây**, 3 ca đỏ sẵn (`t11_lo_336_co_that_VA_bi_chan` ·
   `t15_cong_kiem_bang_khop_nguon_that` · `t33_cong_hoi_RUNTIME_chu_khong_parse_van_ban`, đo
   17:4xZ 06-09-2026, chưa chạy lại ở lượt sửa này), nên nó in `TONG: DIEM DOT BIEN BI TU CHOI` và
   mẫu `MOI` **không khớp**. CI ubuntu xanh (`test registry` 14,33 phút trên `1b3caa1`, run
   `34048685345`) ⇒ lệch **rig**, không phải hồi quy. Hệ quả: phiên thi công **không** dùng
   container này làm nền so sánh cho ca nền; phải dựng hai vế trong MỘT lệnh.
3. **Chưa đo trên Windows.** Container này là Linux. Mọi khẳng định về hành vi Windows đi qua CI.
   Packet này không đổi gì theo nền nên rủi ro thấp, nhưng "thấp" không phải "đã đo".
4. **Không đo được cặp `n/m` của `pretooluse_guard_test.py` trên bản in thật ở đây** (lý do ở
   mục 2). Cặp `39/39` · `34/34` lấy từ thông điệp commit `0c5e889`, tức là **lời khai của lượt
   trước**, không phải phép đo của lượt này. Phiên thi công phải đo lại từ log CI.
5. **Đường (b) — cấp trước hạn — chưa có readback nào chứng minh hoàn tất được từ packet này.** Ba
   nhánh `claude/**` của phiên khác còn giữ blob cũ của #456 với `1/1/38` commit ngoài master (đo
   20:59:59Z 06-09-2026), `ops-don-ref.yml` từ chối xoá chúng, và không có lệnh nào trong kho cập
   nhật tệp trên nhánh của người khác. Đường (a) chạy được bằng công cụ hiện có — đo 21:02Z: `check`
   `rc=0` với `thay_the_cho: []`, `ai-dang-giu` về `0` đúng giây hết hạn — nhưng nó **đợi hạn của
   tiền nhiệm trực tiếp (GATE)**, không phải hạn của #456. Chủ kho chọn và ghi vào
   `granted_on_instruction`. Nợ gốc `AG-T0-01B-thu-hoi-lease-chua-co-duong`; mặt mới đo được:
   `_kiem_bia_mo` đếm `any` và không nhìn hạn, `ai-dang-giu` đếm mọi bản và chỉ nhìn hạn — sửa là
   việc của packet chạm `ops/lease_publish.py`.
6. **Độ dài span ghi bằng KÝ TỰ, không phải byte** — đo lại 21:07Z 06-09-2026 trên bản in THẬT
   của lượt 2 (bản in 19:32Z không được lưu nên số ấy không tự đo lại được — verdict lượt 2, P3):
   `chon_reviewer` span `2745` ký tự = `2764` byte UTF-8 (stdout `2746`/`2765`, `sha256`
   `a5807082…`) · `mcp_gh` span `2171` ký tự = `2251` byte (stdout `2172`/`2252`, `sha256`
   `b3034838…`, `rc=0`, chạy 21:00:15–21:00:22Z; đo lại 22:33Z trên cùng tệp: `2171/2251`, băm khớp).
   Hai số của lượt 1 trùng số hôm nay. Bản in nguyên byte: `executor-luot3-va/fixtures/mcp_gh_test.stdout`
   (định danh bằng BĂM — A6(a)); reviewer lượt 3 không nhận được gói lượt 2 nên với họ số này còn
   **KHÔNG ĐO ĐƯỢC** cho tới khi sandbox có tệp mang đúng băm — nói thẳng thay vì gọi là đã đóng. Độ
   dài span không nói gì về việc grammar đọc đúng — H không dùng nhóm `SPAN` để lấy số. Bản đầu ghi
   `2745 b`/`2179 b` — sai đơn vị, và số `mcp_gh` trôi theo bản in; P3 lượt 1 đóng bằng đơn vị đúng,
   P3 lượt 2 đóng bằng bản in được LƯU cùng `sha256`; P3 lượt 3 (`thieu-ban-in-de-do-span-mcp`, VÁ HỜ)
   đóng bằng cách nói đúng vị trí tệp ở CẢ HAI phía của lần giao gói, và bằng chính tệp được giao.
