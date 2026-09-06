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
  NHÁP thứ ba của revision 1 (`81ba4e4` → `b1c2284` → bản này); quy ước kho đo 21:31Z 06-09-2026
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

Bản này là **bản sửa theo verdict cross-review lượt 3** (`reviewed_sha` `4c6aea4`, Codex), sau lượt 2
(`b1c2284`) và lượt 1 (`d09f2f1`). Lịch sử thiết kế: A-b (bản đầu) → A-c *"soi cặp CÓ NHÃN"* (lượt 1)
→ **T — bản ghi TỔNG theo từng định dạng** (lượt 2) → **T'** (bản này). Slug
`span-rong-nuot-ti-le-vo-can` hỏng **ba lượt liên tiếp**, nên `PROTOCOL §12` đòi trả lời *"có nên tiếp
tục cách làm này không"* TRƯỚC khi vá — câu trả lời, có phép đo, ở mục *"§12 — ba lần hỏng, một gốc"*
dưới đây. Tóm tắt: ba lần cùng một gốc (số làm bằng chứng đến từ một vùng văn bản không được khoanh);
hợp đồng T đúng nhưng prototype T trái với chính hợp đồng ấy ở hai chỗ; T' **gỡ mâu thuẫn** và thêm một
luật để vị từ TỰ kiểm vùng bằng chứng thay vì tin tác giả mẫu. Không có thiết kế thứ tư.

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
không ai canh, và **6 trong 13** cặp bằng chứng của cả sổ đăng ký chưa từng được kiểm. Dưới thiết
kế T (bên dưới) cả **13/13** cặp nằm trong một bản ghi tổng có grammar — 10 cặp là nhóm bắt, 3 cặp
của `probe_mang` là hằng số trong grammar (đo 21:07Z 06-09-2026, bảng đo hai chiều). Đo lại 22:33Z
06-09-2026 bằng bất biến *cặp `SPAN` bắt ⊆ cặp `GRAMMAR` giải trình* (`do_t2.py`, khoá
`bat_bien_span_tap_con_grammar`): đúng ở **10/10** khối (8 định dạng + 2 dạng Windows); đột biến bỏ
nhóm bắt ở grammar `chon` làm bất biến VỠ (`tap_con: false`) — đó là câu trả lời đo được cho rủi ro
reviewer lượt 3 tự khai (*"bỏ nguồn số `SPAN` chỉ đúng nếu `GRAMMAR` bao phủ mọi cặp cần đo"*): hôm
nay bao phủ, và bất biến này phải thành một ca trong `phan_chung()` (A3) để mai vẫn bao phủ.

### Ba hướng vá đã ĐO, và vì sao A-c cũng bị bác

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
| **T** (lượt 2) — bản ghi TỔNG theo từng định dạng, nhưng prototype còn lấy số từ nhóm `SPAN`, và grammar `probe` #1 có `(?: .*)?` | 0 chuỗi regex | ≥ 3 (A5) | CÓ ở bản ghi · **KHÔNG** ở đuôi wildcard | **7 / 66** (reviewer lượt 3, 22:10Z) · **8 / 137** (đo lại 22:33Z, bộ ca lượt này) | **1 / 66** · **5 / 137** | **bác ở lượt 3** |
| **T'** — T với luật 5 viết lại (số CHỈ từ dòng tổng) + luật 7 (mọi cặp trên dòng tổng phải được grammar giải trình) | 0 chuỗi regex (đổi KIỂU giá trị `MOI`, xem `ngoai_pham_vi` #1) | ≥ 3 (A5) | CÓ, kể cả khi grammar có lỗ | **0 / 137** (22:33Z) | **0 / 137** (22:33Z) | **chọn** |

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
`re.search(SPAN)`) và để ngỏ một khoảng `.*` trong một grammar — cùng một gốc, ở dạng nhỏ hơn.
Reviewer lượt 3 dựng được cả hai. Mục kế tiếp là câu trả lời `§12` — viết vào đặc tả, không chỉ vào
báo cáo, vì một packet hỏng ba lần ở cùng chỗ mà đặc tả không nói ra thì phiên sau sẽ vá lần thứ năm.

### §12 — ba lần hỏng, một gốc: câu trả lời TRƯỚC khi vá lần thứ tư

`PROTOCOL §12`: *"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên tiếp tục cách làm
đó, không chỉ vá lần thứ tư."* Slug `span-rong-nuot-ti-le-vo-can` hỏng ba lượt liên tiếp: A-b (lượt 1)
→ A-c (lượt 2) → T (lượt 3). Câu hỏi phải trả lời trước, có bằng chứng: **ba lần ấy có cùng một
nguyên nhân gốc không, hay là ba lỗi khác nhau ở ba thiết kế khác nhau?**

**Cùng một gốc — và đo được.** Cả ba (và cả BASE) để số làm bằng chứng đến từ — hoặc nằm khuất
trong — một **vùng văn bản mà hợp đồng không khoanh**:

| bản | vùng không được khoanh | phản chứng đã chạy | điều cột kế bên cho thấy |
|---|---|---|---|
| A-b | mọi cặp `n/m` trong span (`findall` cả span) | `Ghi chú: … 3/5` trong span ⇒ đỏ giả (lượt 1, 19:32Z) | vùng = toàn span |
| A-c | cặp CÓ NHÃN trong span, khoảng cách `{0,24}` | nhãn trong văn xuôi ⇒ đỏ giả 7/64; nhãn cách xa / gãy dòng ⇒ bỏ sót 7/64 (lượt 2, 21:07Z) | vùng = toàn span, chỉ đổi bộ lọc |
| T (lượt 2) | (i) `cap = _cap(m.groups())` — nhóm của `re.search(SPAN)`, tức lượt khớp **TRÁI NHẤT ở bất kỳ đâu** trong văn bản; (ii) `(?: .*)?` trong grammar `probe_mang` #1 — một vùng mở **ngay trong dòng tổng** | (i) `Ghi chú: ví dụ nền: 3/5 đạt` đứng TRƯỚC bản in thật ⇒ đỏ giả (reviewer: 7/66, 22:10Z; đo lại 22:33Z: 8/137); (ii) `· DOT BIEN 0/0 bi giet` nối vào chính dòng tổng probe ⇒ bỏ sót (reviewer: 1/66; 22:33Z: T lượt 2 bỏ sót 5/137) | **BASE cũng đỏ giả ở (i)** (T004 của reviewer: BASE `1`; `do_t2`: BASE 8 ca cùng nhóm) ⇒ (i) là mảnh của BASE mà T **chép lại**, không phải lỗi mới; **A-c bắt được (ii)** (`1` đỏ) ⇒ (ii) là lỗ T **mở ra** khi thu hẹp bằng chứng về một grammar còn lỗ |

Hai mảnh của T mâu thuẫn với chính hợp đồng của nó: luật 6 / M3 nói *dòng ngoài bộ chọn không được
đọc*, mà luật 5 (bản lượt 2) và prototype vẫn lấy nhóm của `SPAN` — và `(?: .*)?` nghĩa là *phần này
của dòng tổng không được đọc*, trái luật 4 *"khớp TRỌN dòng"*. Nên đây **không phải thiết kế thứ tư**:
hợp đồng T đúng, prototype T trái với hợp đồng, và bản vá đúng là **gỡ mâu thuẫn** — T'.

**Cách làm đổi thế nào, để lần thứ tư khác ba lần trước.** Ba bản trước đều **tin một tác giả mẫu**
khoanh đúng vùng bằng chứng (chuỗi `SPAN`, bộ lọc `NHAN`, rồi `GRAMMAR`) — một danh sách cấm đội lốt
regex, và `CLAUDE.md` đã đo rằng danh sách cấm không bao giờ đủ. T' đảo thành danh sách CHO PHÉP và để
**vị từ tự kiểm vùng**:

1. luật 5 viết lại — khi có `TONG`, số **chỉ** đến từ nhóm bắt của `GRAMMAR` trên dòng được chọn;
   `SPAN` chỉ còn là điều kiện khớp (chuỗi nguyên văn, thứ tự, dòng kết);
2. **luật 7 mới** — mọi cặp `\d+/\d+` trên dòng được chọn phải được grammar **giải trình** (số cặp trên
   dòng = số cặp nhóm bắt + số cặp hằng trong grammar). Một `.*`, một `\d+/\d+` không nhóm bắt — đúng
   hình #319 — không còn giấu được một cặp: cổng ĐỎ **ngay trên bản in xanh** khi grammar có lỗ, thay vì
   mù. Đo 22:33Z: grammar cố ý viết sai `DOT BIEN \d+/\d+` (không nhóm bắt) + `0/0` ⇒ T lượt 2 **0**,
   T' **1**; cùng grammar sai + bản in xanh `34/34` ⇒ T' **1** — ồn ào, không mù;
3. mọi lời khai hai chiều từ nay ghi **`X/N trên bộ ca S`** kèm `sha256` của bộ đo và danh sách **lớp
   chưa phủ** — không còn "đỏ giả 0" tuyệt đối. Bản lượt 2 viết *"T: đỏ giả 0, bỏ sót 0"* trong khi
   prototype còn đọc nhóm `SPAN`: đó là lần thứ ba của hình dạng *lời khai rộng hơn phép đo* trong
   chính đặc tả này (`hinh_dang_ke_thua`).

**Hướng khác đã xét và KHÔNG chọn — đổi thứ các bộ test IN RA** (một dòng máy đọc, ví dụ JSON tổng,
thay vì sổ đăng ký đọc bản in cho người). Không chọn vì: (a) lỗi ba lượt **không nằm ở bản in** — 7 bản
in thật đều có đúng một dòng tổng rõ ràng, chưa ca đỏ giả nào là do formatter mơ hồ; lỗi nằm ở NƠI ĐỌC
lấy số ngoài dòng tổng; (b) nó chạm 8 tệp in, trong đó 2 hook — write set từ 1 lên 9 tệp, trái
`ADR-0044` cho `sensitive` và trái `ngoai_pham_vi` #2 của chính packet; (c) sổ đăng ký vẫn phải có hợp
đồng đọc dòng máy ấy — luật 3/4/7 vẫn cần, chỉ đổi cú pháp. **Điều kiện mở lại hướng này** (đòi
revision, ngoài write set): xuất hiện một bản in THẬT của formatter hiện có mà grammar đóng không mô
tả được, hoặc lượt review kế tìm được đỏ giả/bỏ sót **không** thuộc vùng *"số ngoài dòng tổng"* — khi
ấy gốc khác gốc đã đo, và cách làm phải đổi thật chứ không phải vá lần thứ năm.

### Thiết kế T — bản ghi TỔNG theo từng định dạng (chọn)

**Hợp đồng — 7 luật, mỗi luật có đột biến riêng ở bảng răng bên dưới** (bản lượt 2 có 6; luật 5
được viết lại và luật 7 thêm vào theo câu trả lời `§12` ở trên — không phải vá thêm một mệnh đề, mà
là gỡ chỗ prototype trái với chính hợp đồng):

1. Đơn vị bằng chứng của một mục là **cặp `(SPAN, TONG)`**. `SPAN` là regex hiện có, **giữ nguyên
   chuỗi** — nó vẫn giữ thứ tự và dòng kết (`TỔNG: ĐẠT` / `TONG: DAT`). `TONG` là danh sách
   **bản ghi tổng**, mỗi bản ghi = `(BỘ CHỌN, GRAMMAR)`.
2. **BỘ CHỌN** khớp bằng `re.match` ở **ĐẦU DÒNG** và chỉ trả lời *"dòng này có phải bản ghi tổng
   loại X không"*. Nhãn xuất hiện giữa dòng (`Ghi chú: DOT BIEN …`) không tạo bản ghi.
3. Mỗi BỘ CHỌN phải chọn **ĐÚNG MỘT** dòng. `0` hay `≥ 2` ⇒ `False` — kể cả khi cả hai dòng đều
   xanh, vì không có quy tắc chọn một trong hai.
4. Dòng được chọn phải khớp **GRAMMAR bằng `re.fullmatch`** — trọn dòng, không phải một khúc. Có
   tiền tố tổng mà sai cấu trúc ⇒ `False`; không được bỏ nó rồi tìm dòng khác.
5. Khi mục có `TONG`, số làm bằng chứng **CHỈ** đến từ nhóm bắt của `GRAMMAR` trên dòng được chọn,
   soi **theo cặp** `(n, m)`: `n == m > 0`. `SPAN` vẫn phải khớp (chuỗi giữ nguyên, thứ tự và dòng
   kết vẫn được canh) nhưng **không** lấy giá trị nhóm của nó làm số — `re.search` trả lượt khớp TRÁI
   NHẤT ở bất kỳ đâu, kể cả trong văn xuôi đứng trước tổng (đây là chỗ bản lượt 2 trái luật 6, P1
   lượt 3). Chỉ nhánh tương thích **chuỗi trần** (không `TONG`) mới soi số từ nhóm `SPAN`. Số nhóm
   LẺ ở bất kỳ mẫu nào ⇒ `False` (mẫu lỗi). Chuỗi trần `0` nhóm ⇒ `False` — mẫu không đo gì thì
   không được tha (đây là chỗ mệnh đề `len(m.groups()) != 2` của bản hiện tại bị gỡ, M2).
6. Dòng **không** khớp bộ chọn nào là **VĂN XUÔI**: không được đọc, dù chứa nhãn hay cặp số gì. Đây
   là ranh giới có chủ ý thay cho danh sách nhãn của A-c; giá của nó ghi ở `chua_do_duoc` #1.
7. **Mọi cặp `\d+/\d+` trên dòng được chọn phải được grammar GIẢI TRÌNH**: số cặp đếm được trên dòng
   = số cặp từ nhóm bắt + số cặp viết HẰNG trong grammar; lệch ⇒ `False`. Đây là bài học #319 đặt
   vào chính vị từ: một `.*`, một `\d+/\d+` không nhóm bắt (đúng mẫu `MOI` hiện tại) hay bất kỳ
   khoảng mở nào trong grammar không còn giấu được một cặp — cổng ĐỎ **ngay trên bản in xanh** khi
   grammar có lỗ, thay vì mù. Luật này không tin tác giả grammar; nó đo dòng tổng.

**Bảng bản ghi tổng của 8 mục, tái dẫn xuất từ bản in thật** — bản đo, chưa phải bản thi công.
Bản in nguồn: 5 bộ chạy tại container này 21:00:15–21:00:23Z 06-09-2026, `rc=0` cả 5
(`sha256` ở A6); `subagent_ghi_detect` và `nhanh_don_duoc` lấy bản in `rc=0` của sandbox
reviewer lượt 1 (18:59Z / 18:47Z 06-09 — mã hai bộ không đổi từ đó, lượt này cấm chạy lại bộ dài);
`pretooluse` **chỉ có canonical** (`chua_do_duoc` #2, #4):

```python
# BỘ CHỌN: re.match ở ĐẦU DÒNG · GRAMMAR: re.fullmatch TRỌN dòng · mọi nhóm bắt là cặp (n, m).
TONG = {
    ".claude/dev/chon_reviewer_test.py":   [(r"nền: ", r"nền: (\d+)/(\d+) đạt")],
    ".claude/dev/gh_readback_test.py":     [(r"gh_readback tests: ", r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)")],
    ".claude/dev/mcp_gh_test.py":          [(r"CA\s+:", r"CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT"),
                                            (r"ĐỘT BIẾN\s+:", r"ĐỘT BIẾN\s+: đã đo (\d+)/(\d+) tập giết · ĐẠT")],
    ".claude/dev/mcp_github_doc_test.py":  [(r"mcp_github_doc tests: ", r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)")],
    ".claude/dev/probe_mang_test.py":      [(r"tự đột biến cổng: ", r"tự đột biến cổng: 9/9 chết(?: \(m1\.\.m5 \+ 4 dòng cơ chế\))?"),
                                            (r"named mutant probe_missing_tool_executes_git: ", r"named mutant probe_missing_tool_executes_git: 1/1 chết"),
                                            (r"nền: ", r"nền: 11/11 đạt")],
    ".claude/hooks/pretooluse_guard_test.py":    [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    ".claude/hooks/subagent_ghi_detect_test.py": [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    "ops/nhanh_don_duoc_test.py":          [(r"\d+/\d+\s*$", r"(\d+)/(\d+)")],
}
# Windows — ghép theo THỨ TỰ hai dạng của MOI_WINDOWS[pretooluse]: dòng Windows · dòng Linux đầy đủ.
TONG_WINDOWS = {
    ".claude/hooks/pretooluse_guard_test.py": (
        [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS — do tren ubuntu-latest")],
        [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    ),
}
```

`probe_mang` giữ số cố định trong grammar: 3 bản ghi, 0 nhóm bắt — hợp lệ theo luật 5 vì có bản
ghi; xoá dòng `named mutant …: 1/1 chết` ⇒ `False` (đo). Dòng Windows của `pretooluse` mang
`[1-9]\d* muc` **không** thành nhóm bắt — số mục không phải cặp; số dương được ép trong grammar.

Grammar `probe_mang` #1 nay **ĐÓNG**: chỉ nhận hậu tố formatter đã kiểm tĩnh `(m1..m5 + 4 dòng cơ
chế)`, không còn `(?: .*)?` (hunk H002 của reviewer lượt 3, tái dẫn xuất trên cây thật). Đo 22:33Z
06-09-2026: nối `· DOT BIEN 0/0 bi giet` vào CHÍNH dòng ấy ⇒ T lượt 2 **0**, T' **1**; nối ` rác`
(đuôi lạ, không cặp) ⇒ T' **1**. Hai lớp ĐỘC LẬP cùng chặn ca `0/0`-trong-đuôi — hậu tố đóng (luật 4)
**và** luật 7 — nên đột biến trả wildcard `(?: .*)?` lại **không** đổi màu ca ấy (đo: `1 → 1`, luật 7
bắt). Reviewer viết *"đột biến trả hậu tố về `(?: .*)?` phải làm ca này ĐỎ"*: đúng cho T lượt 2, **sai
cho T'** — nên không chép. Răng riêng của hậu tố đóng là ca đuôi rác không cặp (`1 → 0`); răng riêng
của luật 7 là grammar bỏ nhóm bắt (bảng răng). Nói rõ vì *"hai lớp chặn cùng một ca ⇒ đột biến một
lớp không đổi màu"* là bài học đã trả giá trong `CLAUDE.md` — đột biến sai chỗ, không phải mã sai.

**Vị từ** (bản đo — thi công được đổi cách biểu diễn `(SPAN, TONG)` miễn giữ đủ 7 luật):

```python
_CAP = re.compile(r"(\d+)/(\d+)")

def _cap(g):
    return None if len(g) % 2 else [(g[i], g[i + 1]) for i in range(0, len(g), 2)]

def bang_chung_xanh(text, mau):
    span, tong = (mau, ()) if isinstance(mau, str) else mau
    m = re.search(span, text, re.M)
    if not m or _cap(m.groups()) is None:
        return False                                    # không khớp · nhóm LẺ (mẫu lỗi)
    if not tong:                                        # chuỗi trần (tương thích): số CHỈ từ SPAN
        return bool(m.groups()) and all(int(a) > 0 and a == b for a, b in _cap(m.groups()))
    cap = []                                            # có TONG: SPAN chỉ là điều kiện khớp (luật 5)
    lines = text.splitlines()
    for chon, grammar in tong:
        hits = [l for l in lines if re.match(chon, l)]
        if len(hits) != 1:                              # luật 3: 0 hay ≥ 2 bản ghi cùng loại
            return False
        g = re.fullmatch(grammar, hits[0])              # luật 4: trọn dòng
        c = _cap(g.groups()) if g else None
        if c is None:
            return False
        if len(_CAP.findall(hits[0])) != len(c) + len(_CAP.findall(grammar)):
            return False                                # luật 7: cặp trên dòng tổng mà grammar không giải trình
        cap += c
    return all(int(a) > 0 and a == b for a, b in cap)
```

`MOI[path]` trở thành `(SPAN, TONG[path])`; mỗi phần tử của `MOI_WINDOWS[path]` thành
`(SPAN, TONG_WINDOWS[path][i])`; `mau_theo_nen` và `chay_moi` **không đổi chữ ký** (đo: prototype
đi qua `chay_moi` thật mà không sửa hàm ấy). Hai ca neo mẫu cũ so `MOI[_P456]` với một CHUỖI nên
đổi màu theo thiết kế — xử ở A5, không xoá.

**Đo hai chiều — bảng 1: 64 ca của lượt 2 qua chính `chay_moi` trên module thật**, chỉ hoán vị từ và
bảng `MOI` trong bộ nhớ, `doc_nen_windows` là seam; đo 21:07Z 06-09-2026 với T, **đo lại 22:33Z với
T'** (`do_t2.py`, nhóm `do-gia`/`bo-sot`): cột T' **bằng hệt** cột T ở cả 64 ca — 13 ca T' khác T
lượt 2 đều nằm ngoài 64 ca này, tức bộ ca lượt 2 **không có ca nào đo được hai lỗ mà reviewer lượt 3
dựng** (đó là lý do nó cho `0/64` mà vẫn sai). Script và bản in nguyên byte kèm `sha256`: gói lượt 2
`do_grammar.{py,json,md}` + `fixtures/`, nay được chép vào gói bàn giao lượt này
(`executor-luot3-va/`, xem A6) vì reviewer lượt 3 không nhận được gói lượt 2:

| chiều | ca | BASE | A-c | **T = T'** |
|---|---|---:|---:|---:|
| đỏ giả (kỳ vọng 0) | 7 bản in thật + canonical `pretooluse` Linux (trên Linux, trên Windows) + canonical Windows | 0 | 0 | **0** |
| đỏ giả | `chon` thật + `Ghi chú: đã xem 3/5 hướng cải tiến.` | 0 | 0 | **0** |
| đỏ giả | `chon` thật + `Ghi chú: DOT BIEN đã xem 3/5 hướng cải tiến.` | 0 | **1** | **0** |
| đỏ giả | `chon` thật + `Giải thích: ví dụ DOT BIEN 0/0 là bảng rỗng.` · + `Ghi chú: CA 0/0 là ví dụ.` | 0 | **1** · **1** | **0** |
| đỏ giả | `subagent` thật + `Ghi chu: DOT BIEN da xem 3/5 huong.` · `mcp_gh` thật + `Ghi chú: ĐỘT BIẾN 0/0 là ví dụ.` | 0 | **1** · **1** | **0** |
| đỏ giả | dòng LẺ `DOT BIEN 0/0 bi giet` (không tiền tố tổng) trước / giữa / sau span, hay cách 25 khoảng trắng; `probe` + `đã xem 0/0 hướng` | 0 | 0–1 | **0** — văn xuôi, luật 6 |
| bỏ sót (kỳ vọng 1) | bản ghi `TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet` — A1, trên Linux / trên Windows | **0** / 1 | 1 / 1 | **1** / **1** |
| bỏ sót | `DOT BIEN 33/34` · `subagent` thật `22/22 → 0/0`, `→ 21/22` · `mcp_gh` thật `54/54 → 0/0`, `→ 53/54` | **0** | 1 | **1** |
| bỏ sót | có tiền tố tổng mà sai grammar: 25 khoảng trắng (`0/0` và cả `34/34`) · gãy dòng `DOT BIEN\n0/0` · `đợt 2: 0/0` · đuôi thêm `· DOT BIEN 0/0 bi giet` cùng dòng | 1 · 1 · 1 · **0** | 1 | **1** |
| bỏ sót | HAI bản ghi cùng loại: hai dòng xanh (`pre`, `mcp`, `probe`, `chon`, `gh_readback`, `nhanh`, Windows) · xanh rồi rỗng · rỗng rồi xanh | **0** | **0** (7 ca hai-dòng-xanh) · 1 · 1 | **1** |
| bỏ sót | nhánh từ chối điểm `TONG: CA 30/33 dat` + `TONG: DIEM DOT BIEN BI TU CHOI …` (`pre`, `sub`) | 1 | 1 | **1** |
| bỏ sót | Windows: dòng Windows trên Linux · `0 muc` · `CA 0/39` · `0/0 muc` sau nhãn · **hai** dòng Windows | 1 · 1 · 1 · 1 · **0** | 1 · 1 · 1 · 1 · **0** | **1** |
| **tổng 64 ca** | | đỏ giả **0** · bỏ sót **16** | đỏ giả **7** · bỏ sót **7** | đỏ giả **0** · bỏ sót **0** |

**Bảng 2 — 186 ca của lượt này** (`do_t2.py`, đo **22:33Z 06-09-2026** trên module thật của
`4c6aea4`; vị từ T' và bảng `TONG` được bộ đo lấy NGUYÊN VĂN từ hai khối mã ở trên — thứ được đo là
thứ được viết; T lượt 2 lấy từ blob `4c6aea4`, A-c từ blob `b1c2284`, BASE từ module). Bộ ca S = 64 ca
của bảng 1 + 12 kiểu probe của reviewer lượt 3 (`measure_t.py`) dựng lại trên bản in THẬT của 8 định
dạng (reviewer dựng trên chuỗi canonical ở 6/8 định dạng) + 11 fixture lưu của lượt 2 + 6 ca Windows
+ 2 ca đuôi probe + **6 ca mới** (răng riêng cho từng lớp chốt). **137** ca có kỳ vọng, **49** ca ranh
giới (reviewer cố ý không đặt kỳ vọng — liệt kê ở `chua_do_duoc` #1). Bộ của reviewer là 66 ca có kỳ
vọng — **hai bộ khác nhau**, không chép số qua lại. Đơn vị: số ca mà giá trị `chay_moi` ≠ kỳ vọng.

| nhóm ca | số ca | BASE | A-c | T (lượt 2) | **T'** |
|---|---:|---:|---:|---:|---:|
| bản in thật + canonical (kỳ vọng 0) | 20 | 0 | 0 | 0 | **0** |
| văn xuôi mang nhãn / dòng lẻ SAU tổng, cách 25 khoảng trắng, gãy dòng, `đợt 2:` ở dòng lẻ (kỳ vọng 0) | 21 | 0 | 10 | 0 | **0** |
| `Ghi chú: ví dụ <dòng tổng với 3/5>` đứng **TRƯỚC** bản in — P1 lượt 3 chiều (a) (kỳ vọng 0) | 10 | **8** | **8** | **8** | **0** |
| cùng ghi chú đứng SAU · CRLF đã chuẩn hoá (kỳ vọng 0) | 16 | 0 | 0 | 0 | **0** |
| bản ghi `0/0`, `n ≠ m`, `CA 0/n`, thiếu dòng/`TONG: DAT`, từ chối điểm, Windows lệch nền (kỳ vọng 1) | 40 | 7 | 0 | 0 | **0** |
| HAI bản ghi cùng loại (kỳ vọng 1) | 18 | 18 | 16 | 0 | **0** |
| có tiền tố tổng mà sai grammar: 25 khoảng trắng, gãy dòng, `đợt 2:`, đuôi thêm `· DOT BIEN 0/0` (kỳ vọng 1) | 6 | 2 | 0 | 0 | **0** |
| `· DOT BIEN 0/0 bi giet` nối vào CHÍNH dòng tổng `probe_mang` — P1 lượt 3 chiều (b) (kỳ vọng 1) | 2 | 2 | 0 | **2** | **0** |
| grammar viết SAI (cặp đột biến không nhóm bắt, đúng hình #319) — với `0/0` và với bản in xanh (kỳ vọng 1) | 2 | 2 | 1 | **2** | **0** |
| đuôi rác không mang cặp trên bản ghi có grammar đóng (kỳ vọng 1) | 2 | 2 | 2 | 1 | **0** |
| **tổng 137 ca có kỳ vọng** | 137 | đỏ giả **8** · bỏ sót **33** | đỏ giả **18** · bỏ sót **19** | đỏ giả **8** · bỏ sót **5** | đỏ giả **0** · bỏ sót **0** |

Gói bàn giao `executor-luot3-va/`: `do_t2.py` (`sha256 46b3558c…`, đủ 64 ký tự ở `MANIFEST.sha256`) ·
`do_t2.json` (đủ 186 hàng kể cả giá trị 8 đột biến; băm ghi ở `MANIFEST.sha256` — JSON tự ghi
`spec_sha256_luc_do` nên không thể dẫn băm của nó trong chính spec) · `do_t2.md` · `fixtures/*.stdout`.
Thứ neo mã-đã-đo vào mã-đang-đọc là băm hai KHỐI MÃ mà bộ đo trích từ spec, ghi trong JSON
(`khoi_ma_sha256`): bảng `TONG` `545dedc7…` · vị từ `11fb6d15…` — băm lại hai khối ```python``` ở trên
(nội dung giữa hai hàng rào, UTF-8) mà lệch thì thứ được đo không phải thứ đang đọc. Reviewer không có
gói ấy trong sandbox ⇒ mọi số của bảng này là **KHÔNG ĐO ĐƯỢC** với họ, không phải "đã đóng".

**Răng của từng luật** — 8 đột biến áp vào **NGUỒN** của hai khối mã ở trên (thay chuỗi; bộ đo ép
nguồn phải THAY ĐỔI, một đột biến không đổi nguồn là đột biến chưa từng chạy), đo 22:33Z trên 186 ca.
Cột *"chỉ nó bắt"* tính **trừ m4**: m4 (bỏ hẳn `TONG`) là siêu-đột-biến nuốt mọi ca do grammar quyết
định, tính nó vào thì không luật nào của `TONG` có ca riêng — tạo tác của phép đo, không phải luật thừa:

| đột biến vào T' | luật | ca đổi màu / 186 | chỉ nó bắt (trừ m4) | ví dụ ca riêng |
|---|---|---:|---:|---|
| m1 `len(hits) != 1` → `not hits` (lấy dòng đầu) | 3 | 17 | 17 | hai dòng `nền: 25/25 đạt` về `0` |
| m2 `fullmatch` → `search` | 4 | 16 | 13 | ` rác` sau `nền: 11/11 đạt` (probe #3, grammar đóng) về `0` |
| m3 bỏ `cap += c` (không soi cặp GRAMMAR) | 5 | 27 | 27 | `nền: 0/25` về `0` |
| m4 bỏ hẳn `TONG` (= A-a, chỉ nhóm `SPAN`) | 2–5, 7 | 68 | — (siêu) | `that-probe` lên `1` (0 nhóm, không bản ghi) |
| m5 thêm lại quét nhãn `NHAN` của A-c | 6 | 14 | 10 | `Ghi chú: CA 0/0 là ví dụ.` lên `1` |
| **m6 `cap = []` → `cap = _cap(m.groups())`** (nhóm `SPAN` trở lại khi có `TONG`) | **5 (mới)** | 8 | 4 | `Ghi chú: ví dụ nền: 3/5 đạt` TRƯỚC bản in `chon` lên `1` |
| **m7 bỏ luật 7** | **7 (mới)** | 2 | 2 | grammar bỏ nhóm bắt + `0/0` về `0`; + `34/34` về `0` |
| m8 grammar probe #1 trả về `(?: .*)?` | 4 (dữ liệu) | 3 | **0** | ⊆ m2 (đo `m8_tap_con_m2: true`) — hậu tố đóng là mặt DỮ LIỆU của luật 4, không có răng tách khỏi m2; ca `0/0`-trong-đuôi **không** đổi màu vì luật 7 bắt |

Kill-list đầy đủ theo tên ca: `do_t2.json` → `rang_dot_bien` và `rang_dot_bien_chi_no_bat_tru_m4`.
Reviewer lượt 3 đề xuất đo răng bằng *"đưa nhóm số của `SPAN` trở lại danh sách cặp khi có `TONG`"*
(= m6) và *"trả wildcard hậu tố lại"* (= m8); m6 áp nguyên ý; m8 đo được là không có răng riêng dưới
T' — ghi thẳng, không chép lời hint thành bằng chứng.

**B-tự nhiên vẫn là cái BẪY, và T gỡ nó:** mệnh đề `len(m.groups()) != 2` trong `bang_chung_xanh`
hiện tại trả `True` **vô điều kiện** cho mọi mẫu có số nhóm khác 2 (đo lại 21:07Z: mẫu 0/1/3/4
nhóm trên `CA 0/39 · DOT BIEN 0/0` ⇒ `True`). Hôm nay chưa mẫu nào có 1/3/4 nhóm nên mệnh đề ấy
**đang ngủ**; nó thức dậy đúng lúc ai đó "canh cặp đột biến" bằng cách bắt nó thành nhóm 3/4. T
thay mệnh đề ấy bằng luật 5 — bảng đo ở A2.

**T không đổi hành vi Windows của #456** (đo 21:07Z qua `chay_moi` với T; đo lại 22:33Z với T' —
cùng giá trị ở cả 9 ca `win-*`/`windows_*` của `do_t2.json`): dòng Windows trên Linux `1` ·
trên Windows `0` · dòng Linux đầy đủ trên Windows `0` · `0/0 bi giet` trên Windows `1` · `CA 0/39`
trên Windows `1` — bằng hệt BASE; thêm hai chốt mới: `0/0 bi giet` trên **Linux** `1` và **hai**
dòng Windows `1` (BASE `0` cả hai).

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
dòng phản chứng ⇒ dưới 100"* là ước của **A-c** (bản lượt 1) và bị rút: `NHAN` không tồn tại trong
T', và T' thêm bảng `TONG`/`TONG_WINDOWS` (hai khối mẫu ở trên đã là 21 + 22 dòng), phần ghép kiểu giá
trị của `MOI`/`MOI_WINDOWS`, vị từ 7 luật và các ca A1–A6 — **chưa có bản thi công để đo tổng
additions**, nên không khẳng định con số nào dưới `300`. Phiên thi công đo `git diff --numstat` trước
review; vượt `300` thì DỪNG — không cắt ca để lách, không nâng trần.

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
   định *"không sửa một ký tự"* của hai bản trước được mở lại có chủ ý ở bản này, vì A-c bị bác
   bằng phép đo (bảng *"Ba hướng vá đã ĐO"*). Chuỗi regex `SPAN` của 8 mục và của `MOI_WINDOWS`
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
| M1 | `bang_chung_xanh` đọc **bản ghi tổng** của từng mục theo `(BỘ CHỌN, GRAMMAR)`: đúng MỘT dòng, khớp TRỌN, số CHỈ từ dòng tổng, mọi cặp `n == m > 0`, mọi cặp trên dòng tổng được grammar giải trình (luật 1–5, 7). `DOT BIEN 0/0 bi giet` trong bản ghi bị từ chối trên **mọi** nền — kể cả khi nó nằm ở đuôi dòng tổng hay grammar quên nhóm bắt. | `write_set` #1 |
| M2 | Mệnh đề thoát `len(m.groups()) != 2` bị **gỡ**: nhóm bắt soi theo cặp với mọi số nhóm chẵn; LẺ ⇒ `False`; `0` nhóm và `0` bản ghi ⇒ `False`. Không còn số nhóm nào cho `True` vô điều kiện. | `write_set` #1 |
| M3 | Văn xuôi không là bằng chứng (luật 6): dòng không khớp bộ chọn nào không được đọc, kể cả khi mang nhãn `CA`/`DOT BIEN`/`ĐỘT BIẾN` hay cặp số. Tổng TRÙNG và tổng SAI CẤU TRÚC là ĐỎ. | `write_set` #1 |
| M4 | Đường Windows của #456 giữ nguyên năm hành vi đã đo; dòng Windows có grammar riêng (`[1-9]\d* muc`, không nhóm bắt cho số mục); thêm hai chốt mới (`0/0` trên Linux, hai dòng Windows). | `write_set` #1 |
| M5 | Ca `p456-linux-nhan-0-tren-0-Y-HET-base` **đảo chiều và đổi tên**; hai ca neo mẫu đổi neo sang `SPAN` (chuỗi cũ nguyên văn) + `TONG` canonical; không ca nào bị xoá. | `write_set` #1 |
| M6 | Đủ **8** định dạng có phản chứng qua `chay_moi` từ bản in nguyên byte (7 thật + canonical `pretooluse`); mỗi luật 1–6 có đột biến riêng làm ít nhất một ca đổi màu. | `write_set` #1 |

## `nghiem_thu`

**A1 (M1) — lỗ #319 phía Linux đóng, đo bằng SỐ ĐỎ của `chay_moi`, không bằng mắt.**
`chay_moi(moi={P: MOI[P]}, chay_mot=lambda _: (0, RONG), doc_nen_windows=lambda: False)` với
`RONG = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"` ⇒ **1** (đo 21:07Z 06-09-2026:
BASE `0`, T `1`; đo lại 22:33Z: T' `1`); cùng chuỗi với `doc_nen_windows=lambda: True` ⇒ `1` (BASE
`1`). Thêm hai ca cùng đơn vị (đo 22:33Z): `· DOT BIEN 0/0 bi giet` nối vào đuôi dòng tổng `probe_mang`
⇒ **1** (T lượt 2 `0`); grammar `pretooluse` cố ý bỏ nhóm bắt cặp đột biến (`DOT BIEN \d+/\d+`) +
`RONG` ⇒ **1** (T lượt 2 `0`) — luật 7. Cùng phép đo trên
bản in THẬT của `subagent_ghi_detect` (`22/22 → 0/0`) và `mcp_gh` (`54/54 → 0/0`) ⇒ `1` mỗi bộ
(BASE `0`). Đi qua chính `chay_moi` — khuyết tật "làm tròn" nằm ở NƠI TIÊU THỤ (r6/#401). Đơn vị:
**số mục bị đếm là ĐỎ**. Phép làm ĐỎ của ca: bỏ soi cặp của GRAMMAR ⇒ về `0` (đo, bảng răng).

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

Phép làm ĐỎ: bất kỳ ô nào lệch cột T (đo lại 22:33Z trên T': 20/20 ô khớp, `A2_dat: true` trong
`do_t2.json`). Đơn vị: **giá trị trả về của `bang_chung_xanh`**. Số nhóm LẺ
trả `False` ngay cả trên bản in đầy đủ — có chủ ý; `0` nhóm **không** bản ghi cũng `False` — mẫu
không đo gì thì không phải bằng chứng.

**A3 (M3) — văn xuôi không là bằng chứng; tổng TRÙNG và tổng SAI CẤU TRÚC là ĐỎ.**
Qua `chay_moi`, đo 21:07Z (cột A-c để thấy đúng chỗ T khác):
- bản in thật `chon_reviewer` + lần lượt từng ghi chú `Ghi chú: đã xem 3/5 hướng cải tiến.` ·
  `Ghi chú: DOT BIEN đã xem 3/5 hướng cải tiến.` · `Giải thích: ví dụ DOT BIEN 0/0 là bảng rỗng.` ·
  `Ghi chú: CA 0/0 là ví dụ.` ⇒ **0** mỗi ca (A-c: `0` · `1` · `1` · `1`). Cùng phép trên bản in thật
  `subagent` và `mcp_gh` ⇒ **0** (A-c `1`);
- bản in thật `probe_mang` + dòng lẻ `DOT BIEN 0/0 bi giet` hay `đã xem 0/0 hướng` ⇒ **0** (A-c:
  `1` · `0`). **Đây là chỗ T cố ý khác A-c**: dòng lẻ mang nhãn không phải bằng chứng vì không
  formatter nào in nó, và luật 6 là ranh giới đã chọn — `chua_do_duoc` #1;
- HAI bản ghi cùng loại ⇒ **1**: hai dòng `TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet` · xanh rồi
  rỗng · rỗng rồi xanh · hai dòng `CA … :` (`mcp_gh`) · hai `nền: 11/11 đạt` (`probe`) · hai
  `nền: 25/25 đạt` (`chon`) · hai dòng `gh_readback tests: 8/8 …` · hai dòng `8/8` (`nhanh`) · hai
  dòng Windows. BASE cho **0** ở cả 9 ca; A-c cho `0` ở 7 ca "hai dòng xanh";
- có tiền tố tổng mà sai grammar ⇒ **1**: `DOT BIEN` + 25 khoảng trắng + `0/0` (và + `34/34`) ·
  `DOT BIEN\n0/0` · `DOT BIEN đợt 2: 0/0` · đuôi thêm `· DOT BIEN 0/0 bi giet` cùng dòng (BASE `0`
  ở ca cuối) · nhánh từ chối điểm `TONG: CA 30/33 dat` + `TONG: DIEM DOT BIEN BI TU CHOI …`.
- **văn xuôi mang tiền tố tổng đứng TRƯỚC bản in** (P1 lượt 3, chiều a) — `Ghi chú: ví dụ nền: 3/5
  đạt` trước bản in thật `chon_reviewer` ⇒ **0**; cùng kiểu cho `gh_readback`, `mcp_gh`,
  `mcp_github_doc`, `subagent`, `pretooluse` Linux, dòng Windows trên Windows ⇒ **0** mỗi ca; đặt SAU
  cũng **0** (đo 22:33Z; T lượt 2 và BASE cho `1` ở 7 ca Linux/Windows — `probe` và `nhanh` `0` vì
  `SPAN` của chúng không có nhóm bắt hoặc neo `^…$`). Phản chứng tự soi: cùng ghi chú trước + `0/0`
  trong bản ghi ⇒ **1** — văn xuôi không đổi màu theo cả hai chiều;
- **cặp trên dòng tổng phải được giải trình** (luật 7): grammar `pretooluse` cố ý viết `DOT BIEN
  \d+/\d+` (không nhóm bắt — đúng mẫu `MOI` hiện tại) + `0/0` ⇒ **1**; cùng grammar + bản in xanh
  `34/34` ⇒ **1** (ồn ào, không mù; T lượt 2 `0` cả hai). Thêm ca **tĩnh** trong `phan_chung()`: với
  mỗi mục `MOI`/`MOI_WINDOWS` trên bản in canonical, tập cặp `SPAN` bắt ⊆ tập cặp `GRAMMAR` giải trình
  (đo 22:33Z: 10/10 khối đúng); đột biến bỏ nhóm bắt ở grammar `chon` ⇒ ca ĐỎ;
- **đuôi lạ trên dòng tổng** (luật 4, hậu tố đóng): ` rác` sau `tự đột biến cổng: … cơ chế)` ⇒ **1**;
  ` rác` sau `nền: 11/11 đạt` ⇒ **1** (T lượt 2 `0` / `1`).
Phép làm ĐỎ (bảng răng, đo 22:33Z): m1 gỡ luật 3 ⇒ 17 ca "hai bản ghi" về `0`; m2 `fullmatch` →
`search` ⇒ 16 ca (13 chỉ nó) về `0`; m5 thêm lại `NHAN` ⇒ 14 ca đỏ giả lên `1`; **m6 trả nhóm `SPAN`
lại khi có `TONG` ⇒ 8 ca ghi-chú-trước lên `1`**; **m7 bỏ luật 7 ⇒ 2 ca grammar-sai về `0`**. Đơn vị:
**số mục bị `chay_moi` đếm là ĐỎ**.

**A4 (M4) — đường Windows của #456 nguyên vẹn, cộng hai chốt mới.**
Qua `chay_moi` với seam `doc_nen_windows`, đo 21:07Z: dòng Windows trên Linux **1** · trên Windows
**0** · dòng Linux đầy đủ trên Windows **0** · `0/0 bi giet` trên Windows **1** · `CA 0/39` trên
Windows **1** · `DOT BIEN 0 muc` trên Windows **1** · `0/0 muc` sau nhãn trên Windows **1** — bằng
BASE; **mới**: `0/0 bi giet` trên Linux **1** và **hai** dòng Windows **1** (BASE `0` cả hai).
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
  `_MAU_BASE456` trên ba đầu vào) ⇒ đầu vào `_RONG456` **cố ý lệch** dưới T (chuỗi trần có 2 nhóm,
  không `TONG` ⇒ `True`; mục đầy đủ ⇒ `False`); ca phải khai đúng ba giá trị mới thay vì `is` bằng
  nhau, để chính chỗ lệch ấy được ĐO chứ không bị làm phẳng.
Đơn vị: **số phản chứng đỏ đúng / tổng** — `N/N`, `N ≥ 51 + số ca mới của A1–A6`. `51` là nền
19:32Z 06-09-2026 trong CÂY THẬT — lượt này **không đo lại** (cấm chạy suite; `KHÔNG ĐO ĐƯỢC ở lượt
này (ràng buộc chủ kho)`); **đo lại tại lúc thi công**. Phép làm ĐỎ: giữ khẳng định cũ của bất kỳ
ca nào trong ba ⇒ `phan_chung()` dưới `N/N`.

**A6 (M6) — tám định dạng từ bản in NGUYÊN BYTE, và sổ đăng ký chạy thật.**
- (a) qua `chay_moi`: 7 bản in thật + canonical `pretooluse` (Linux, Windows) ⇒ **0** đỏ mỗi bộ
  (đo 21:07Z với T; đo lại 22:33Z với T', nhóm `that-*`/`canonical-*`/`*-baseline` của `do_t2.json`:
  **0**). `sha256` bản in, đủ để ai cũng tự đo lại: `chon_reviewer` `a5807082…` · `gh_readback`
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
| lời khai rộng hơn phép đo | **3** (bản đầu: *"A-b không sinh đỏ giả"*; bản lượt 1: *"mọi cặp mang nhãn được kiểm"* trong khi `[^\n\d]{0,24}?` bỏ sót; **bản lượt 2: *"T: đỏ giả 0, bỏ sót 0"* viết như tính chất tuyệt đối trong khi prototype còn đọc nhóm `SPAN` và một grammar còn `.*`** — 64 ca không có ca nào đo hai chỗ ấy) | verdict lượt 1 tái hiện 19:32Z; verdict lượt 2 tái hiện 21:07Z; verdict lượt 3 tái hiện **22:10Z 06-09-2026**, đo lại 22:33Z | Cùng họ *"thu hẹp mà viết thành đóng"* trong `CLAUDE.md`. **Lần thứ ba ⇒ `§12`:** cách làm đổi — mọi điểm hai chiều từ nay là `X/N trên bộ ca S` kèm băm bộ đo và danh sách lớp chưa phủ (`chua_do_duoc` #1), không còn "0" tuyệt đối. |
| đọc toàn bộ văn bản làm bằng chứng rồi cố lọc (A-b, A-c, và mảnh `SPAN`/`.*` còn sót trong T) | **3** (ba bản trước của chính đặc tả này; ở T là mảnh CHÉP LẠI từ BASE + một khoảng mở trong grammar) | verdict lượt 1 (19:32Z), lượt 2 (21:07Z), lượt 3 (22:10Z 06-09-2026) | **Lần thứ ba ⇒ `§12`**, trả lời ở mục *"§12 — ba lần hỏng, một gốc"*: cùng gốc, hợp đồng T đúng, prototype trái hợp đồng; sửa = gỡ mâu thuẫn + luật 7 để vị từ tự kiểm vùng bằng chứng. Hướng "đổi bên IN" đã xét và ghi điều kiện mở lại. |

## `chua_do_duoc`

1. **Giá của luật 6 — văn xuôi không được đọc, và hợp đồng là HỮU HẠN.** T' không hứa đọc mọi cặp
   có nhãn ở mọi vị trí văn bản; một bộ TƯƠNG LAI in bằng chứng ngoài bản ghi tổng đã khai sẽ không
   được canh cho tới khi có grammar riêng, và đổi formatter ⇒ phải đổi `TONG` rồi chạy lại bộ ca +
   bản in thật. Nợ có tên **`GRAMMAR-TONG-LA-HOP-DONG-HUU-HAN`** (thay cho
   `NHAN-BANG-CHUNG-LA-DANH-SACH-CHO-PHEP` của bản lượt 1). Rủi ro ngược — grammar quá chặt bác một
   formatter hợp lệ — đo được ở A6(a): 7 bản in thật ⇒ `0` đỏ; **chưa đo** trên bản in thật của
   `pretooluse` (mục 2, 4) và trên **Windows** (mục 3).
   **Lớp CHƯA PHỦ, liệt kê để không ai đọc "0/137" thành "0 với mọi cách in"** — 49 ca ranh giới
   reviewer lượt 3 dựng và cố ý không đặt kỳ vọng (`do_t2.json` → `ranh_gioi_T'`), giá trị T' ghi
   nguyên: thêm khoảng trắng cuối dòng tổng · hậu tố ` (xong)` · thụt lề dòng tổng · mã màu ANSI ⇒ T'
   **từ chối** (8/8 định dạng mỗi kiểu) — đó là giá của hợp đồng hữu hạn, và reviewer kiểm tĩnh không
   thấy tuỳ chọn formatter hiện tại nào in các biến thể ấy qua đường capture; dòng tổng RỖNG **thụt
   lề** đứng sau tổng xanh ⇒ T' **nhận** (8/8: dòng ấy ngoài bộ chọn, luật 6 — không formatter nào in
   nó, nhưng đây là ranh giới thật, không phải "an toàn"); CRLF thô ⇒ nhận 7/8, `nhanh` từ chối vì
   `SPAN` neo `$` — mà `_chay_that` dùng `subprocess.run(text=True)` nên đường thật đã chuẩn hoá về
   LF (ca `consumer_normalized_CRLF` ⇒ 0 đỏ 8/8); `nhanh` + dòng `0/0 (xong)` ⇒ nhận (bộ chọn neo
   cuối dòng, luật 6). Đổi formatter ⇒ phải khai lại `TONG` và chạy lại toàn bộ bộ ca; **không** được
   nới grammar bằng `.*` để "qua" — luật 7 sẽ làm ĐỎ ngay bản in xanh, và đó là kết quả đúng.
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
   của lượt này (bản in 19:32Z không được lưu nên số ấy không tự đo lại được — verdict lượt 2, P3):
   `chon_reviewer` span `2745` ký tự = `2764` byte UTF-8 (stdout `2746`/`2765`, `sha256`
   `a5807082…`) · `mcp_gh` span `2171` ký tự = `2251` byte (stdout `2172`/`2252`, `sha256`
   `b3034838…`, `rc=0`, chạy 21:00:15–21:00:22Z; đo lại 22:33Z trên cùng tệp: `2171/2251`, băm khớp).
   Hai số của lượt 1 trùng số hôm nay. Bản in nguyên byte: `executor-luot3-va/fixtures/mcp_gh_test.stdout`
   (định danh bằng BĂM — A6(a)); reviewer lượt 3 không nhận được gói lượt 2 nên với họ số này còn
   **KHÔNG ĐO ĐƯỢC** cho tới khi sandbox có tệp mang đúng băm — nói thẳng thay vì gọi là đã đóng. Độ
   dài span không nói gì về việc grammar đọc đúng — T' không dùng span để chọn cặp. Bản đầu ghi
   `2745 b`/`2179 b` — sai đơn vị, và số `mcp_gh` trôi theo bản in; P3 lượt 1 đóng bằng đơn vị đúng,
   P3 lượt 2 đóng bằng bản in được LƯU cùng `sha256`; P3 lượt 3 (`thieu-ban-in-de-do-span-mcp`, VÁ HỜ)
   đóng bằng cách nói đúng vị trí tệp ở CẢ HAI phía của lần giao gói, và bằng chính tệp được giao.
