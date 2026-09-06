# Đặc tả packet — LO-319-LINUX-BANG-CHUNG-XANH

- `packet_id`: **LO-319-LINUX-BANG-CHUNG-XANH** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được ngay khi có số Issue — tiền lệ #456 giữ bí danh ở `packet_id`,
  số ở `packet_issue`)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi trường này; lease #456 không có và
  bốn hồ sơ này cũng không có mission nào đang mở cho lane "chi phí CI Windows". Khuyến nghị:
  mở MỘT Mission Issue cho cả bốn packet (`GATE` · `LO` · `2A` · `2B`) rồi điền chung; nếu chủ
  kho không mở, ghi số Issue của packet tiền nhiệm `#456` và nói rõ đó là thay thế.
- `revision`: 1 · `generation`: 1
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

## `nguon_cap_viec`

Packet **khắc phục**. Không phải một dòng trong bảng packet của
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.

Nguồn: `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #1 và khối chú thích
`.claude/dev/ci_dang_ky_test.py:35-38` — cả hai khai thẳng rằng lỗ #319 phía **Linux** CÓ THẬT,
có sẵn từ trước packet #456, và bị để lại **có chủ đích** vì M4 của #456 đóng băng hành vi Linux.
Cross-review Codex lượt 1 của #456 bắt đúng chỗ này (finding P2) và bản vá đã phải lùi lại
(`426bfc0` — *"trả mẫu Linux về nguyên bản, dời chốt số dương sang đường Windows"*).

Packet này là chỗ M4 ấy được **gỡ đóng băng có thẩm quyền**, không phải chỗ nó bị lách.

Bản này là **bản sửa theo verdict cross-review lượt 1** (`reviewed_sha` `d09f2f1`, Codex): thiết
kế vá đổi từ *"soi mọi cặp trong span"* sang *"soi cặp CÓ NHÃN"* vì reviewer dựng được đỏ giả
thật — xem mục *"Ba hướng vá"*.

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
không ai canh, và **6 trong 13** cặp bằng chứng của cả sổ đăng ký chưa từng được kiểm.

### Ba hướng vá, ĐO CẢ BA rồi mới chọn

Đơn vị: **số phản chứng trong `phan_chung()` đổi màu** (nền `1b3caa1` = `51/51` đỏ đúng, đo lại
19:32Z trong CÂY THẬT — đo trong bản sao ngoài cây cho `47/51` vì `ROOT = parents[2]` giải sai,
đó là **tạo tác rig**, không phải hồi quy), **số mẫu regex phải sửa**, và — thêm từ verdict lượt 1 —
**số mục đỏ của `chay_moi` trên một bản in hợp lệ có thêm một cặp vô can**.

Phản chứng vô can là của reviewer, tái hiện lại ở đây 19:32Z: bản in THẬT của
`chon_reviewer_test.py` (xanh, 19:29Z), chèn thêm dòng `Ghi chú: đã xem 3/5 hướng cải tiến.`
ngay trước `TỔNG: ĐẠT`. Regex vẫn khớp, `rc` vẫn 0, mọi bằng chứng test giữ nguyên — chỉ có một tỉ
lệ không phải bằng chứng lọt vào span.

| hướng | mẫu phải sửa | phản chứng đổi màu | bịt `DOT BIEN 0/0`? | đỏ giả trên ghi chú `3/5` | cặp được kiểm / 13 |
|---|---:|---:|---|---:|---:|
| **A-a** — soi các nhóm bắt THEO CẶP | 0 | **0** (`51/51`) | **KHÔNG** — mẫu vẫn không bắt cặp đột biến | 0 | 7 |
| **A-b** — soi **mọi** cặp `n/m` trong span khớp | 0 | 1 (`50/51`) | CÓ | **1** ← ĐỎ GIẢ, đo 19:32Z | 13 |
| **A-c** — nhóm bắt theo cặp **+ cặp CÓ NHÃN** (`CA` · `DOT BIEN` · `ĐỘT BIẾN`) trong span | **0** | **1** (`50/51`) | **CÓ** | **0** | **10** |
| **B-tự nhiên** — thêm nhóm bắt cho cặp đột biến (4 nhóm) | 2 | — | **KHÔNG — HỒI QUY** (xem dưới) | — | — |
| **B-thật** — siết từng mẫu thành `[1-9]\d*/[1-9]\d*` | 2 | 3 | CÓ, chỉ cho 2 mẫu ấy | 0 | 9 |

Ca duy nhất đổi màu dưới A-b lẫn A-c là `p456-linux-nhan-0-tren-0-Y-HET-base` — đúng ca phải đảo
chiều (A5). Hai ca anh em `p456-mau-linux-KHONG-DOI-so-voi-base` và
`p456-linux-A-B-tung-dau-vao-khop-base` **không** đổi màu vì `MOI` không bị sửa một ký tự nào.

**Chọn A-c.** A-b bị loại vì đỏ giả **đo được**, và vì bản đầu của đặc tả này tự mâu thuẫn: một
chỗ khai *"A-b không sinh đỏ giả"*, chỗ A6 lại gọi chính cái đỏ giả ấy là *"hành vi ĐÚNG"* —
không thể nghiệm thu bằng cách tuyên bố đỏ oan là đúng (verdict lượt 1, P1
`span-rong-nuot-ti-le-vo-can`).

**A-c là gì, nói bằng mã** (bản đo, chưa phải bản thi công):

```python
NHAN = re.compile(r"(?:\bCA\b|DOT BIEN|ĐỘT BIẾN)[^\n\d]{0,24}?(\d+)/(\d+)")

def bang_chung_xanh(text, mau):
    m = re.search(mau, text, re.M)
    if not m:
        return False
    g = m.groups()
    if len(g) % 2:                       # số nhóm LẺ = mẫu lỗi ⇒ fail-close
        return False
    cap = [(g[i], g[i + 1]) for i in range(0, len(g), 2)]
    return all(int(a) > 0 and a == b for a, b in cap + NHAN.findall(m.group(0)))
```

Hai tính chất làm nó khác A-b, cả hai đo 19:32Z trên bảy bản in thật:

1. **Tập nhãn là DANH SÁCH CHO PHÉP** (`CA` · `DOT BIEN` · `ĐỘT BIẾN`), đúng doctrine *"danh sách
   cấm không bao giờ đủ — phải đảo thành danh sách cho phép"* trong `CLAUDE.md`. A-b cần một danh
   sách CẤM các hình dạng vô can (`3/5 hướng`, `x/y điểm`, …) mà không ai liệt kê hết được.
2. **Nhãn không bắt nhầm gì trong span thật**: `NHAN.findall` trên span của bảy bản in cho
   `chon_reviewer` 0 · `gh_readback` 0 · `mcp_gh` 2 (`42/42`, `54/54`) · `mcp_github_doc` 0 ·
   `probe_mang` 0 · `subagent_ghi_detect` 2 (`33/33`, `22/22`) · `nhanh_don_duoc` 0. Cộng dòng
   canonical `pretooluse` 2 (`39/39`, `34/34`). Không có lần khớp nào ngoài bằng chứng.

**Cái giá của A-c, nói thẳng:** `10/13` chứ không phải `13/13`. Ba cặp không được kiểm là
`9/9` · `1/1` · `11/11` của `probe_mang_test.py` — chúng là **hằng số ghi cứng trong chính regex**
(`tự đột biến cổng: 9/9 chết…`), nên không thể mang giá trị khác mà vẫn khớp; "kiểm" chúng theo
nghĩa so số là vô nghĩa. Và một cặp `n/m` **không mang nhãn** trong span sẽ KHÔNG được kiểm — đó
là giới hạn có chủ ý, ghi thành nợ ở `chua_do_duoc` #1.

**B-tự nhiên là một cái BẪY, đo được:** mệnh đề `len(m.groups()) != 2` trong `bang_chung_xanh`
trả `True` **vô điều kiện** cho mọi mẫu có số nhóm khác 2. Nên cách hiển nhiên nhất để "canh cặp
đột biến" — bắt nó thành nhóm 3/4 — làm hàm **ngừng kiểm cả cặp CA**:

```
mẫu 2 nhóm, "CA 0/39 · DOT BIEN 0/0"  -> False   (đúng)
mẫu 4 nhóm, "CA 0/39 · DOT BIEN 0/0"  -> True    (SAI — đo 17:45Z, đo lại 19:32Z 06-09-2026)
```

Hôm nay chưa mẫu nào có 1/3/4 nhóm nên mệnh đề ấy **đang ngủ**; nó thức dậy đúng lúc ai đó vá
theo hướng hiển nhiên. Đây là lý do quyết định: **lỗ phải được bịt ở `bang_chung_xanh`**, vì
hướng B để lại một cái bẫy nạp sẵn ngay trên đường mà người vá tiếp theo sẽ đi. A-c gỡ mệnh đề ấy
(M2) — bảng đo ở A2.

**A-c không đụng đường Windows:** dòng `MOI_WINDOWS` (`DOT BIEN [1-9]\d* muc KHONG DO TREN
WINDOWS`) chỉ có **một** cặp `n/m` là cặp CA; sau `DOT BIEN` là `34 muc`, không có `/` nên nhãn
không khớp. Đo 19:32Z qua `chay_moi`: dòng Windows hợp lệ trên nền Windows ⇒ `0` đỏ; cùng dòng
với `CA 0/39` ⇒ `1` đỏ; dòng Linux đầy đủ trên Windows ⇒ `0`; `0/0 bi giet` trên Windows ⇒ `1`.
Bốn số này **bằng hệt** BASE.

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
chạy được trên tên `.nhap` (đo 19:31Z: `rc=8`, thiếu `packet_issue`, `granted_by` — đúng chẩn
đoán cũ). **Đổi tên về `.yaml` là BƯỚC CUỐI khi cấp thật**, sau khi đã điền đủ các ô.

**Thu hồi #456 phải phủ MỌI bản, và bản đầu của mục này viết thiếu** (verdict lượt 1, P1
`bia-mo-mot-ref-khong-thu-hoi-moi-ban`). Cơ chế, đo trên tập ref thật:

- Lease #456 là **1 blob** (`8b2103c`) nằm trên **10 ref** (đo 19:29Z): `refs/heads/master` ·
  `refs/heads/claude/soan-spec-3-viec-treo-20260906` · `origin/master` · `origin/HEAD` ·
  `origin/ops/cap-lease-456` · `origin/claude/cap-nhat-trang-thai-pr-taxzax` ·
  `origin/claude/soan-spec-3-viec-treo-20260906` · `origin/claude/elegant-bun-cd554f` ·
  `origin/claude/priceless-volhard-329577` · `origin/claude/tra-luat-process-review-o4d7kb`.
- `_kiem_bia_mo` (`ops/lease_publish.py:595`) đòi **một** bản của lease cũ mang `da_bi_thay_the`
  (`any`). `ai-dang-giu` (`:935`) lại cộng **mọi** bản `(blob, path)` trên **mọi** ref, và mỗi bản
  đọc `da_bi_thay_the` của CHÍNH nó. Đặt bia mộ trên một nhánh là tạo một blob MỚI; blob cũ vẫn
  nằm trên 9 ref kia.
- Đo 19:34–19:35Z trong bản sao: thêm `da_bi_thay_the` vào #456 **chỉ trên nhánh này**, commit,
  cập nhật ref remote-tracking; dựng lease GATE khai `thay_the_cho: #456` và điền tạm ba ô ⇒
  `check` **`rc=0`** (bia mộ `any` qua) — nhưng `ai-dang-giu ci_dang_ky_test.py` in **hai** dòng
  cho #456: `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ` (nhánh này) và `CÒN_HẠN` trần
  (`origin/claude/cap-nhat-trang-thai-pr-taxzax`) ⇒ **`NGƯỜI_GIỮ 1`**. Cổng cấp cho qua, cổng
  điều phối vẫn thấy hai writer. Gỡ bia mộ đi ⇒ `check` `rc=8` đúng chẩn đoán — tức chốt hai
  chiều CÓ răng, chỉ là răng đếm `any`.

**Thủ tục thu hồi, viết cho đủ:**

1. Liệt kê mọi bản: `git for-each-ref --format='%(refname)' refs/heads refs/remotes/origin |
   while read r; do git ls-tree -r "$r" -- ops/leases | grep <lease_id>; done | sort -u` — đếm
   **blob phân biệt** và **ref**. Hôm nay: `1` blob / `10` ref.
2. Bản mang bia mộ phải **đến được master** (PR của packet đầu chuỗi mang nó).
3. Mọi ref còn giữ blob CŨ phải hoặc **được cập nhật** tới blob mới, hoặc **biến mất**. Đo quan hệ
   với master 19:31Z: `ops/cap-lease-456` (0 ahead / 3 behind) và
   `claude/cap-nhat-trang-thai-pr-taxzax` (0 / 1) là nhánh vùng làm việc đã land ⇒ xoá được qua
   `ops-don-ref.yml` (`behind_by = 0` theo luật của nó là "mọi commit đã nằm trong master" — nhánh
   0 ahead thoả). Ba nhánh `claude/elegant-bun-cd554f` (1 ahead) · `claude/priceless-volhard-329577`
   (1 ahead) · `claude/tra-luat-process-review-o4d7kb` (38 ahead) là **của phiên khác, có commit
   chưa land** — packet này KHÔNG có thẩm quyền xoá, và không có lệnh nào trong kho cập nhật một
   tệp trên nhánh của người khác.
4. Đo lại bằng `ai-dang-giu <đường dẫn>`: đếm số dòng chứa `<lease_id cũ>` và **không** chứa
   `ĐÃ_BỊ_THAY_THẾ` ⇒ phải bằng **0**. Đây là tiêu chí A8.

**Hệ quả thẳng thắn:** với bộ công cụ hiện có, bước 3 **KHÔNG hoàn tất được** cho ba nhánh phiên
khác, nên A8 **không đạt được** nếu cấp lease trước khi #456 hết hạn — trừ khi chủ kho tự tay xử
ba nhánh ấy. Có một đường thứ hai, rẻ hơn và đo được: **cấp lease sau `14:30:07Z 07-09-2026`** —
lúc đó #456 là `HẾT_HẠN` trên mọi ref, `ai-dang-giu` không đếm nó, và `thay_the_cho` chỉ còn là
dấu vết chứ không phải điều kiện. Ghi cả hai đường ở `chua_do_duoc` #5; chủ kho chọn.

**Điều kiện tiên quyết của packet này** (chuỗi thu hồi mới, vì GATE đi đầu): lease của packet này
khai `thay_the_cho: gate-tach-job-cat-chi-phi-exec-1-claude-20260906`, và tệp lease của GATE phải
mang `da_bi_thay_the: lo-319-linux-bang-chung-xanh-exec-1-claude-20260906` — chốt `_kiem_bia_mo`
đòi **hai chiều**, và thủ tục bốn bước ở trên áp cho MỌI mắt xích, không riêng #456.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng THÊM** (cột `additions` của `git diff --numstat`,
không phải thêm-trừ-xoá). Write set là **1 tệp**. Ước dòng thêm: `bang_chung_xanh` mới ≈ 10 dòng,
`NHAN` 1 dòng, phản chứng A1–A6 ≈ 40 dòng ⇒ dưới `100`. Đo thật bằng `git diff --numstat` trước
review; vượt `300` thì DỪNG.

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

1. **Không sửa một ký tự nào trong `MOI` hay `MOI_WINDOWS`.** Quyết định này đã được **mở lại**
   khi thiết kế lại theo verdict lượt 1 — và giữ nguyên, nhưng vì lý do ĐO chứ không vì mặc định:
   hướng A-c cần `0` mẫu phải sửa (bảng "Ba hướng vá", 19:32Z), và giữ nguyên chúng là thứ giữ
   được hai ca `p456-mau-linux-KHONG-DOI-so-voi-base` và `p456-linux-A-B-tung-dau-vao-khop-base`
   — hai chốt do cross-review lượt 1 của #456 sinh ra. Nếu lượt review kế chứng minh A-c cũng
   không đủ, đây là quyết định phải mở lại lần nữa, và mở bằng revision mới.
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
| M1 | `bang_chung_xanh` kiểm **mọi nhóm bắt theo cặp** VÀ **mọi cặp `n/m` mang nhãn** `CA` / `DOT BIEN` / `ĐỘT BIẾN` trong span khớp (tập nhãn là danh sách CHO PHÉP, khai ở một hằng). `DOT BIEN 0/0 bi giet` bị từ chối trên **mọi** nền. Cặp không mang nhãn KHÔNG được kiểm — có chủ ý. | `write_set` #1 |
| M2 | Mệnh đề thoát `len(m.groups()) != 2` bị **gỡ**: nhóm bắt được soi theo cặp với mọi số nhóm chẵn; số nhóm LẺ ⇒ `False` (mẫu lỗi, fail-close). Không tồn tại số nhóm nào làm hàm trả `True` vô điều kiện. | `write_set` #1 |
| M3 | Mẫu 0 nhóm (`probe_mang_test.py`) vẫn ĐẠT trên bản in thật; nhưng "0 nhóm" không còn là lối tha: một cặp mang nhãn trong span của nó vẫn bị kiểm. | `write_set` #1 |
| M4 | Đường Windows của #456 không đổi hành vi: dòng `KHONG DO TREN WINDOWS` vẫn ĐẠT trên Windows, vẫn ĐỎ trên Linux. | `write_set` #1 |
| M5 | Ca `p456-linux-nhan-0-tren-0-Y-HET-base` được **đảo chiều và đổi tên** cho khớp sự thật mới; hai ca anh em giữ nguyên. | `write_set` #1 |
| M6 | Một bản in hợp lệ có thêm một cặp `n/m` **vô can** (không nhãn) KHÔNG bị đếm đỏ. | `write_set` #1 |

## `nghiem_thu`

**A1 (M1) — lỗ #319 phía Linux đóng, đo bằng SỐ ĐỎ của `chay_moi`, không bằng mắt.**
Phép làm ĐỎ: gọi `chay_moi(moi={P: MOI[P]}, chay_mot=lambda _: (0, RONG), doc_nen_windows=lambda: False)`
với `RONG = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"`. Trị phải là **1**
(đo 19:32Z: BASE **0**, A-c **1**). Đi qua chính `chay_moi` chứ không gọi thẳng `bang_chung_xanh`
— khuyết tật "làm tròn" nằm ở NƠI TIÊU THỤ, bài học r6/#401 đã trả giá ba lần trong đúng tệp này.
Đơn vị: **số mục bị đếm là ĐỎ**, không phải chuỗi in ra.

**A2 (M2) — mệnh đề thoát theo số nhóm không còn.**
Năm mẫu, số nhóm ∈ {0, 1, 2, 3, 4}, hai đầu vào mỗi mẫu. Đo 19:32Z, cột A-c là trị phải đạt:

| số nhóm | `CA 0/39 · DOT BIEN 0/0` — BASE | — A-c | `CA 39/39 · DOT BIEN 34/34` — BASE | — A-c |
|---:|---|---|---|---|
| 0 | `True` (tha) | **`False`** (nhãn bắt) | `True` | `True` |
| 1 | `True` (tha) | **`False`** (lẻ) | `True` | **`False`** (lẻ) |
| 2 | `False` | `False` | `True` | `True` |
| 3 | `True` (tha) | **`False`** (lẻ) | `True` | **`False`** (lẻ) |
| 4 | **`True`** (BẪY) | **`False`** | `True` | `True` |

Phép làm ĐỎ: bất kỳ ô nào lệch cột A-c. Đơn vị: **giá trị trả về của `bang_chung_xanh`**. Số nhóm
LẺ trả `False` ngay cả trên bản in đầy đủ — có chủ ý: đó là mẫu viết sai, không phải bằng chứng.

**A3 (M3) — mẫu 0 nhóm không còn được tha vô điều kiện, nhưng KHÔNG đỏ oan.**
Ba ca trên `MOI["probe_mang_test.py"]` (0 nhóm), đo 19:32Z:
- bản in thật của `probe_mang_test.py` (`9/9`, `1/1`, `11/11`) ⇒ `True` (BASE `True`);
- cùng bản in, chèn `DOT BIEN 0/0 bi giet` trước `TỔNG: ĐẠT` ⇒ **`False`** (BASE `True` ← lối tha);
- cùng bản in, chèn `đã xem 0/0 hướng` (không nhãn) ⇒ **`True`** — có chủ ý, đây là giới hạn ở
  `chua_do_duoc` #1, và ca này tồn tại để ai siết tập nhãn thành "mọi cặp" phải thấy nó đổi màu.

**A4 (M4) — đường Windows của #456 nguyên vẹn.**
Phép làm ĐỎ: bốn phản chứng `p456-*` hiện có phải vẫn xanh, cụ thể `_dem_nen(_WIN456, False) == 1`
và `_dem_nen(_WIN456, True) == 0` và `_dem_nen(_LNX456, True) == 0` (đo 19:32Z dưới A-c: `1` ·
`0` · `0`, bằng BASE). Đột biến bắt buộc: xoá điều kiện nền trong `mau_theo_nen` ⇒
`p456-dong-windows-tren-linux-la-DO` phải ĐỎ.

**A5 (M5) — ca cũ đảo chiều, KHÔNG bị xoá, và ĐỔI TÊN.**
Ca `p456-linux-nhan-0-tren-0-Y-HET-base` khẳng định `_dem_nen(_RONG456, False) == 0`. Sau packet
này mệnh đề đúng là `== 1`. Đổi khẳng định **và** đổi tên (đề nghị:
`lo319-linux-KHONG-CON-nhan-0-tren-0`), vì một cái tên nói *"y hệt base"* đứng cạnh một khẳng
định nói ngược lại là đúng lớp lỗi *"hai lời khai mâu thuẫn trong cùng một tệp"* mà cross-review
PR #250 lượt 3 đã bắt.
Phép làm ĐỎ: giữ nguyên tên cũ ⇒ finding quy trình; giữ nguyên khẳng định cũ ⇒ `phan_chung()`
cho `50/51` (đo 19:32Z dưới A-c, chính xác một ca: `p456-linux-nhan-0-tren-0-Y-HET-base`).
Đơn vị: **số phản chứng đỏ đúng / tổng** — phải là `N/N` với `N ≥ 51 + số ca mới của A1–A6`. Con
số `51` là nền đo 19:32Z 06-09-2026 trong CÂY THẬT; **đo lại tại lúc thi công**, đừng chép.

**A6 (M6) — không đỏ giả trên cặp vô can, và sổ đăng ký chạy thật vẫn xanh.**
Hai phần:
- (a) phản chứng đi qua `chay_moi`: bản in thật của `chon_reviewer_test.py` (`rc=0`) chèn thêm
  `Ghi chú: đã xem 3/5 hướng cải tiến.` trước `TỔNG: ĐẠT` ⇒ **`0`** đỏ (đo 19:32Z: BASE `0` ·
  A-b **`1`** · A-c `0`). Phép làm ĐỎ: đổi `NHAN.findall(span)` thành `re.findall(r"\d+/\d+",
  span)` (tức quay về A-b) ⇒ ca này ĐỎ. Ca này là lý do A-c tồn tại; không có nó thì không ai đo
  được packet này khác A-b chỗ nào.
- (b) `python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`, và cả
  bảy bộ có bản in thật đo 19:29–19:31Z (`chon_reviewer` · `gh_readback` · `mcp_gh` ·
  `mcp_github_doc` · `probe_mang` · `subagent_ghi_detect` · `nhanh_don_duoc`) qua `chay_moi` với
  A-c cho **`0`** đỏ mỗi bộ (đo 19:32Z, bằng BASE).
Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A7 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **1** đường dẫn.

**A8 — lease cũ đã thu hồi TRƯỚC khi bắt tay, đo trên MỌI bản.**
`python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py` phải:
- in `NGƯỜI_GIỮ 1` và tên ấy là lease của **packet này**;
- **không** có dòng nào mang `lease_id` của mắt xích trước (`gate-tach-job-cat-chi-phi-…`) lẫn
  của `#456` mà thiếu nhãn `ĐÃ_BỊ_THAY_THẾ` hoặc `HẾT_HẠN` — đếm bằng `grep <lease_id> | grep -v
  'ĐÃ_BỊ_THAY_THẾ' | grep -vc HẾT_HẠN` ⇒ **0**.
Phép làm ĐỎ: chạy lệnh trước khi thu hồi ⇒ ra tên lease khác ⇒ DỪNG, không được bắt tay. Đo 19:34Z:
bia mộ trên một ref ⇒ số dòng ấy là **1**, tức ĐỎ — đúng ca reviewer dựng.
Nếu chủ kho chọn đường "cấp sau khi #456 hết hạn" (`chua_do_duoc` #5) thì điều kiện thứ hai đo
được ngay; nếu chọn đường thu hồi sớm, điều kiện ấy **không đo được là ĐẠT** bằng công cụ hiện có —
xem `chua_do_duoc` #5, đừng làm tròn.

## `hinh_dang_ke_thua`

Bộ đếm **hình dạng lỗi**, chép từ `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` và từ hồ sơ
`CI-CAI-JSONSCHEMA` (r1→r2→r3), cộng thêm những gì packet này đo được. Mỗi dòng ghi thời điểm đo
hoặc nguồn trích (L5):

| hình dạng | số lần đã gặp | đo/trích lúc | ghi chú |
|---|---:|---|---|
| tập RỖNG thoả `not song` (`0/0` được nhận là bằng chứng) | **3** | trích #456 spec + đo 19:32Z (B1 `rong ⇒ True`) | #319 (gốc) · #456 đường Windows (đã bịt) · đường Linux (packet này). Lần thứ ba ⇒ `PROTOCOL §12` đòi xem lại CÁCH LÀM: câu trả lời là **bịt ở vị từ dùng chung**, không bịt ở từng mẫu. |
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức: `25` khởi tạo `9e4f361` → `45` `6d88a2c` → `60` `7657bfd`) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml`, 19:29Z | Bản đầu chép `3` từ #456; #456 đếm MỨC chứ không đếm LẦN NÂNG (verdict lượt 1, P2). Lần nâng kế tiếp là lần **thứ ba** ⇒ `§12`. Packet này không đụng `ci.yml`. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** | trích `CI-CAI-JSONSCHEMA-r3` A5 | Đã đo được ở #456. |
| cổng vắng mặt trông giống cổng xanh | nhiều | trích `CLAUDE.md` | Ở đây: cổng CÓ MẶT, CÓ CHẠY, và vẫn không đo — biến thể đắt hơn. |
| lease không tự chết khi packet đã land | **2** | `#355` trích `CLAUDE.md`; `#456` đo 17:46Z (còn 20,7 giờ sau merge) | Xem A8. |
| lời khai rộng hơn phép đo — "A-b không sinh đỏ giả" | **1** (bản đầu của chính đặc tả này) | verdict lượt 1, tái hiện 19:32Z | Cùng họ *"thu hẹp mà viết thành đóng"* trong `CLAUDE.md`. |

## `chua_do_duoc`

1. **Cặp `n/m` KHÔNG mang nhãn thì KHÔNG được kiểm** — giới hạn có chủ ý của A-c, thay cho nợ
   `SPAN-RONG-CO-THE-NUOT-CAP-VO-CAN` của bản đầu (nợ ấy đã bị đóng bằng cách đổi thiết kế, không
   phải bằng cách "chưa có ca thật nào đòi"). Hôm nay `10/13` cặp được kiểm; ba cặp còn lại là
   hằng số trong regex của `probe_mang`. Một bộ TƯƠNG LAI in cặp đột biến với nhãn ngoài tập
   (`CA` · `DOT BIEN` · `ĐỘT BIẾN`) sẽ không được canh — nợ có tên
   **`NHAN-BANG-CHUNG-LA-DANH-SACH-CHO-PHEP`**: mở tập nhãn khi thêm bộ, và mỗi lần mở phải chạy
   lại phản chứng "nhãn không bắt nhầm gì trong span thật". Không có cách nào chặn nó bằng mã ở
   packet này.
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
5. **A8 không đạt được bằng công cụ hiện có nếu cấp lease trước `14:30:07Z 07-09-2026`.** Ba nhánh
   `claude/**` của phiên khác còn giữ blob cũ của #456 (đo 19:29Z), và không có lệnh nào trong kho
   cập nhật hay xoá chúng từ packet này. Hai đường, chủ kho chọn và ghi vào
   `granted_on_instruction`: (a) cấp SAU giờ hết hạn ⇒ #456 thành `HẾT_HẠN` trên mọi ref, A8 đo
   được ngay; (b) cấp TRƯỚC ⇒ chủ kho tự xử ba nhánh (xoá qua `ops-don-ref.yml` nếu chấp nhận, hay
   chờ chúng land), rồi mới đo A8. Nợ gốc vẫn là `AG-T0-01B-thu-hoi-lease-chua-co-duong`; mặt mới
   đo được ở đây là **`_kiem_bia_mo` đếm `any` còn `ai-dang-giu` đếm `all`** — sửa nó là việc
   của một packet chạm `ops/lease_publish.py`, ngoài phạm vi này.
6. **Độ dài span ghi bằng KÝ TỰ, không phải byte.** `chon_reviewer` span `2745` ký tự = `2764`
   byte UTF-8; `mcp_gh` `2171` ký tự = `2251` byte (đo 19:32Z; bản đầu ghi `2745 b`/`2179 b` — sai
   đơn vị và số mcp_gh trôi vì bản in hôm nay dài khác). Với A-c con số này không còn là rủi ro
   (nhãn, không phải span, quyết định cặp nào được soi); ghi lại để đóng finding P3 lượt 1.
