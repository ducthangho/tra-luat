# ĐẶC TẢ PACKET — `N6-LOI-KHAI-RONG-HON-PHEP-DO` **revision 1**

| | |
|---|---|
| `packet_id` | `N6-LOI-KHAI-RONG-HON-PHEP-DO` |
| `packet_issue` | **#411** |
| `revision` | 1 |
| `generation` | 1 |
| `executor` | `claude` |
| `environment` | `cloud` |
| `review_class` | **`sensitive`** — xem `vi_sao_sensitive` |
| `base` | `master` `6fa8a745` (đo `09:21:47Z 30-08-2026`, HAI nguồn khớp: `git ls-remote origin refs/heads/master` và `git rev-parse refs/remotes/origin/master`) |
| `assurance_target` | **`cross_approved`** (reviewer `codex`) **+** duyệt khác danh tính |

> **MỌI CON SỐ TRONG TỆP NÀY KÈM THỜI ĐIỂM ĐO (L5). ĐO LẠI trước mỗi bước công bố** — đăng băm,
> cấp lease, xin review, merge. Ba trạng thái: có · không · **KHÔNG ĐO ĐƯỢC**; cái thứ ba làm cổng
> ĐỎ, KHÔNG làm tròn lên.

## `nguon_cap_viec`

Hai nguồn, cả hai bắt buộc:

1. **Issue #411** — nợ `loi-khai-rong-hon-phep-do` trong docstring `_bash_tuyet_doi()`, mở bởi phiên
   thi hành packet **#405** lúc `~07:4xZ 30-08-2026` sau khi chủ kho chạy phép đo Windows thật
   (#408 comment `5467512515`). Packet #405 **đã land** (`master` `7a2f177`), nên không sửa được
   dưới lease của nó.
2. **Quyết định trực tiếp của chủ kho trong phiên `soan-spec` này** (`30-08-2026`, vòng 1–3):
   bộ đếm hình dạng **A → 8**, và packet phải có **HAI** mục — không chỉ sửa một câu chữ. Xem
   `hinh_dang_ke_thua`. Đây là điều kiện tiên quyết: **một packet chỉ sửa docstring là bản vá thứ 8
   của cùng hình dạng, đúng thứ chốt kế thừa nói KHÔNG nên làm.**

## `vi_sao_sensitive`

Lớp là thứ **MÁY TÍNH RA**, không phải lời khai (đo `09:04Z 30-08-2026`):

```
_tinh_lop_tu_write_set([".claude/hooks/subagent_ghi_detect_test.py",
                        ".claude/dev/packet_loop_test.py"])   ⇒   sensitive
```

**ĐỌC ĐÚNG LÝ DO.** Không đường dẫn nào khớp tiền tố trong `_BANG_LOP` — bảng ấy đo được có đúng
**7** mục (`.github/workflows/`, `.github/coordination/`, `packet_loop.py`, `launcher.py`,
`gate_lifecycle.py`, `lease_publish.py`, `tl_gws.py`) và **không** mục nào phủ `.claude/hooks/`
hay `packet_loop_test.py`. Lớp đến từ giá trị **MẶC ĐỊNH fail-closed**, KHÔNG phải vì packet chạm
authority. Vẫn áp trần `≤3 tệp / ≤300 dòng thêm` theo fail-closed, nhưng **CẤM** khai ngược lại
rằng packet "chạm authority" để mượn uy tín cụm từ ấy.

Ghi thêm cho rõ, vì nó là một quyết định có chủ ý: phương án đặt cổng vào `.claude/dev/packet_loop.py`
(có trong `_BANG_LOP`, tức chạm authority THẬT) **đã bị loại ở vòng 3** — xem `ngoai_pham_vi`.

## `write_set`

Đúng **HAI** đường dẫn, liệt kê từng cái, không ký tự đại diện:

```
.claude/hooks/subagent_ghi_detect_test.py
.claude/dev/packet_loop_test.py
```

**Đo trước khi soạn** (`09:22:12Z 30-08-2026`, kho ĐÃ `--unshallow`, refspec đầy đủ, đã
`git remote prune origin`; so tập tên hai chiều: `ls-remote` **269** ↔ `for-each-ref` **269**,
`comm` **rỗng cả hai chiều**):

| đường dẫn | `rc` | người giữ |
|---|---|---|
| `.claude/hooks/subagent_ghi_detect_test.py` | **11** | `n5-lenh-hook-windows-exec-1-claude-20260830`, CÒN_HẠN tới `2026-08-30T10:53:00Z` |
| `.claude/dev/packet_loop_test.py` | **0** | không có |

**CHẶN THẬT — không được cấp lease trước `10:53:00Z`.** Chủ kho đã chọn **đợi hết hạn**, không
land PR rút hạn. Trước khi cấp lease phải đo lại cả hai đường và đòi **`NGƯỜI_GIỮ 0` cho CẢ HAI**.

**Cảnh báo đo được về chính công cụ đo** (`08:55Z 30-08-2026`): `ai-dang-giu` **ĐẾM THIẾU nhánh** —
nó in **3** dòng cho lease #405 trong khi quét đủ 269 nhánh máy chủ cho ra **4** nhánh mang tệp
lease (`master`, `ops/bien-nhan-n5-review-2`, `ops/cap-lease-n5-lenh-hook-windows`,
`ops/cap-nhat-lease-n5-review-1` — cả bốn cùng hạn `10:53:00Z`); hai bản trùng blob bị gộp thành
một dòng. **Đừng lập kế hoạch thu hồi từ đầu ra của nó.** Nợ riêng, gắn #400 (chủ kho duyệt mở ở
vòng 1). KHÔNG thuộc packet này.

## `ngoai_pham_vi`

Thứ **CỐ Ý** không làm, kèm lý do:

1. **KHÔNG đụng `.claude/dev/packet_loop.py`.** Đặt cổng thành một subcommand ở đó là tiền lệ
   `adr-song` (`3df5525`, `22-08-2026`) — đo được là **`packet_loop.py` +100 · `packet_loop_test.py`
   +207 = +307 dòng thêm**, tức **đã vượt trần 300** trước khi cộng mục 1. Cộng thêm: `packet_loop.py`
   nằm trong `_BANG_LOP` nên đưa nó vào write set biến lớp `sensitive` thành *chạm authority thật*.
   Chủ kho chọn lối test-only ở vòng 3. **Đánh đổi đã nhận:** cổng này KHÔNG có lệnh CLI gọi tay.
2. **KHÔNG đụng `ops/lease_publish_test.py`** dù `t26`/`t27` ở đó là chỗ đặt tự nhiên nhất.
   Đo `09:07:25Z 30-08`: đang bị lease `bo-ghi-nguoc-exec-1-claude-20260829` (packet **#396**) giữ
   tới `2026-08-30T12:40:00Z`. Đụng vào là tự tạo cửa sổ hai writer.
3. **KHÔNG sửa ngược các spec đã đóng băng.** Đo `09:29:19Z 30-08-2026` bằng ĐÚNG luật chặt mà Đ2
   sẽ cài (xem `dang_duoc_chap_nhan`), neo theo **TIÊU ĐỀ MỤC**: `ops/specs` có **53** tệp · **27**
   có mục `hinh_dang_ke_thua` · **26** không có mục · trong 27 mục ấy: **8 ĐẠT**, **19 TRƯỢT**.
   (Bốn số hạng, không chỉ hiệu — L5: *kiểm SỐ HẠNG, đừng kiểm quan hệ*.) Spec là hiện vật **có băm**
   mà lease neo vào; sửa ngược làm băm trong lease cũ trỏ vào thứ không còn tồn tại. Cổng phải
   **diff-scoped** (chủ kho chốt vòng 3).
4. **KHÔNG đụng `ops/specs/N5-LENH-HOOK-WINDOWS.md`.** Packet #405 đã đóng; băm
   `930b12ef41aa58e2efa42473518466de547dac0cd3df3090f2467e3b6579a557` (kiểm khớp `08:22Z 30-08`)
   đang được lease của nó neo vào.
5. **KHÔNG đụng hai bộ `cach_ly` (`mcp_gh_test.py`, `pretooluse_guard_test.py`) và
   `.claude/dev/ci_dang_ky_test.py`.** Đó là nợ `AG-361-P2-01`/`-02`, Issue #361, và là **câu hỏi
   THIẾT KẾ** riêng (*"chốt neo một nền thì trên nền khác đọc là ĐỎ hay KHÔNG-ÁP-DỤNG?"*). Nới
   write set để với tới nó chính là vá lần thứ tư của hình dạng KHÁC.
6. **KHÔNG cố làm `master` xanh.** Windows còn 2 dòng đỏ và **đó là ĐẠT** theo chủ ý #401/#405.

## `muc_tieu`

Hai mục tiêu. **Đ2 là điều kiện để packet này tồn tại**, không phải phần thêm nếm — bỏ Đ2 thì
packet trở lại đúng hình dạng "vá lần 8" mà chốt kế thừa cấm.

| # | mục tiêu | chiếu vào (L2) |
|---|---|---|
| **Đ1** | Thu hẹp **hai** lời khai trong tệp về đúng mỏ neo phép đo, ghi kèm phản chứng từ máy Windows thật, và khai đúng hệ quả. **KHÔNG đổi một dòng hành vi nào.** | `.claude/hooks/subagent_ghi_detect_test.py` |
| **Đ2** | Dựng cổng **cưỡng chế L4**: spec **MỚI** (thêm trong diff) bắt buộc chép bộ đếm hình dạng. Đây là câu trả lời §12 cho *"xem lại CÁCH LÀM"*. | `.claude/dev/packet_loop_test.py` |

### Đ1 — hai chỗ, đã định vị

Đo `09:23Z 30-08-2026` trên `6fa8a745`:

| chỗ | dòng | nguyên văn hiện tại (rút gọn) |
|---|---|---|
| **Đ1a** | `437`–`441` | *"Chinh su BAT DONG giua hai cach do la bang chung: `shutil.which("bash")` … tra ve `C:\Program Files\Git\bin\bash.EXE`, con `CreateProcess` tra ve vo WSL. Hai ket qua khac nhau cho cung mot ten ⇒ day la TAO TAC CUA VO BOC"* |
| **Đ1b** | `467` | *"# Hai dong khac nhau CHINH LA con bo — xem `_bash_tuyet_doi`."* |

**Khuyết tật ĐÚNG là gì.** Cả hai câu neo một phép đo **CÓ THẬT và có trích run id**, nhưng viết ở
**thì phổ quát** — đọc như tính chất của Windows, trong khi nó là tính chất của **một cấu hình
runner**. Phản chứng đo được trên máy Windows 11 của chủ kho (`30-08-2026`, #408 comment
`5467512515`):

```
VANTAY shutil.which('bash') : C:\Windows\system32\bash.EXE
VANTAY ten tran             : rc=0 · GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)
VANTAY duong tuyet doi      : rc=0 · y hệt   ⇒ HAI CÁCH DÒ ĐỒNG Ý, cả hai ra WSL
```

`x86_64-pc-linux-gnu` là vân tay quyết định — Git Bash báo `x86_64-pc-msys`.

**Hệ quả phải khai, không được bỏ:** trên máy chủ kho, **đường dẫn tuyệt đối KHÔNG tránh được vỏ
WSL**, vì `shutil.which` chính nó trỏ vào đấy. Đường tuyệt đối chỉ loại **sự BẤT ĐỒNG giữa hai cách
dò**, không bảo đảm tránh WSL. Ai đọc docstring cũ rồi kết luận *"ca đã miễn nhiễm với vỏ WSL"* sẽ
sai trên chính máy mà kho được phát triển.

**Đ1b sai theo chiều nguy hơn Đ1a:** nó nói *sự khác nhau* CHÍNH LÀ con bọ, tức hàm ý *giống nhau =
không có bọ*. Trên máy chủ kho hai dòng **giống hệt nhau** mà nguy cơ vẫn còn (chạy dưới không gian
tệp Linux của WSL ⇒ **chạy và trả lời SAI trong im lặng**, tệ hơn chết ồn ào trên runner).

**KHÔNG PHẢI LÀ GÌ.** Không phải lỗi hành vi: mã vẫn phân giải tuyệt đối, vẫn khai trạng thái thứ ba
CÓ TÊN và ĐỎ khi không phân giải được, vẫn đòi `4/4`. `A2`–`A6` của #405 không lung lay. **Đổi hành
vi khi sửa docstring là vi phạm đặc tả này.**

### Đ2 — cổng L4-carry

**Luật:** mỗi tệp `ops/specs/*.md` **THÊM MỚI trong diff** phải có mục `hinh_dang_ke_thua`, và mục
ấy phải **chép được một bộ đếm** — hoặc một cặp `<chữ cái hình dạng> = <số>`, hoặc khai thẳng
`khong_ap_dung` kèm lý do. Thiếu ⇒ **ĐỎ**.

**Diễn giải "spec MỚI"** (chủ kho chốt vòng 3 — BASE ba nhánh + fail-close):

```
git diff --diff-filter=A --name-only <BASE>...HEAD -- ops/specs/
```

| tình huống | `BASE` |
|---|---|
| lượt `pull_request` | `origin/$GITHUB_BASE_REF` |
| lượt `push` lên `master` | `HEAD^1` (cha thứ nhất của commit merge) |
| lượt `workflow_dispatch` | `git merge-base HEAD refs/remotes/origin/master` |
| **không giải được `BASE`** | **KHÔNG ĐO ĐƯỢC ⇒ ĐỎ** |

**Hàng `workflow_dispatch` là BẮT BUỘC, không phải cho đủ bộ** — thiếu nó thì đặc tả **tự mâu thuẫn**:
`A7` đòi một lượt `workflow_dispatch`, `ci.yml:126` chạy `packet_loop_test.py` trong đúng lượt ấy, và
nếu `BASE` không giải được thì cổng mới phải khai `KHÔNG ĐO ĐƯỢC ⇒ ĐỎ` **ngay trong lượt dùng để
nghiệm thu** — tức `A7` không bao giờ đạt được. Phát hiện bởi cross-review `codex` trên PR #415
(finding P1, `09:39Z 30-08-2026`); phiên soạn spec **không tự thấy**.

Dispatch ngay trên `master` cho `merge-base = HEAD` ⇒ tập spec THÊM MỚI **rỗng** ⇒ XANH. Đó **không**
phải fail-open: so `master` với chính nó thì thật sự không có spec nào được thêm. Trên một nhánh có
spec mới, `merge-base` là điểm rẽ và `--diff-filter=A` bắt đúng tệp ấy.

**Ngoại lệ tha DUY NHẤT:** cây rõ ràng là **bản sao rời** — không có `.git`. Trong kho thật mà
thiếu thì **ĐỎ**. Đây là chốt của bài học `t24` (*"ca có MẶT khác ca có ĐO"*): một nhánh
"không thấy thì bỏ qua" từng làm suite báo `24/24` trong khi ca ấy không đo gì.

**`fetch-depth: 0` đã có sẵn** — `ci.yml:86`, đo `09:10:39Z 30-08` ⇒ `merge-base`/`HEAD^1` dùng được
trên runner. **Không có tiền lệ diff-scoped nào** trong hai bộ test cổng (`packet_loop_test.py`,
`lease_publish_test.py`) — đây là cái đầu tiên, nên luật phải tự đứng, không mượn khuôn có sẵn.

**Đường dẫn:** chỉ đọc đầu ra của `git` (luôn dấu `/`) và xử bằng `PurePosixPath`. KHÔNG dùng
`os.sep`, KHÔNG dựng đường dẫn hệ thống từ chuỗi git.

## `dang_duoc_chap_nhan` — luật của Đ2, viết dưới dạng DANH SÁCH CHO PHÉP

**Hai bẫy dưới đây do chính lượt soạn spec này vấp phải và đo ra. Cả hai làm cổng SAI theo hai chiều
NGƯỢC nhau, nên luật phải khai chúng chứ không để phiên thi hành gặp lại.**

**Bẫy 1 — neo sai chỗ.** Bộ đo bản đầu tìm mục bằng `t.find('hinh_dang_ke_thua')`, tức bắt vào **lần
nhắc đầu tiên trong văn xuôi**, không phải **tiêu đề mục**. Hậu quả đo được (`09:27:50Z` so
`09:28:15Z 30-08-2026` trên cùng 53 tệp): `27` mục thật bị đọc thành `36`, và chính đặc tả này bị xếp
nhầm là **thiếu bộ đếm** trong khi nó có. **Luật phải neo `^#{2,3}\s*`?hinh_dang_ke_thua`?` và cắt tới
tiêu đề `#{2,3}` kế tiếp.**

**Bẫy 2 — nhận diện quá lỏng.** Bản kế tiếp hỏi *"trong mục có chữ A–F nào gần một chữ số không"*.
Nó xếp `N5-LENH-HOOK-WINDOWS.md` là **ĐẠT** — sai — vì mục ấy có bảng `| 1 | t21_... |` với chữ và số
cạnh nhau. Đó là bắt theo **hình dáng ngẫu nhiên**, không theo **thứ cần có**.

**Vì vậy luật KHÔNG hỏi "có số không". Nó đòi ĐÚNG MỘT trong ba dạng dưới đây, không dạng nào khác:**

| # | dạng được chấp nhận | nhận diện |
|---|---|---|
| 1 | hàng bảng bộ đếm | dòng khớp `^\|\s*\*{0,2}[A-F]\*{0,2}\s*\|.*\|\s*\*{0,2}\d+\*{0,2}\s*\|` |
| 2 | cặp phẳng | `\b[A-F]\s*=\s*\d` |
| 3 | miễn, **có lý do** | `khong_ap_dung` cộng **văn bản khác rỗng** sau nó trên cùng dòng (sau dấu `:` hoặc khoảng trắng), tối thiểu **20 ký tự không phải khoảng trắng** |

**Dạng 3 đòi LÝ DO, không chỉ đòi cái nhãn.** Bản đầu nhận diện `khong_ap_dung` bằng chuỗi trần, nên
một spec mới chỉ cần gõ đúng nhãn ấy là **đi vòng qua** bộ đếm mà không phải khai vì sao — cổng biến
thành nghi lễ. Phát hiện bởi cross-review `codex` trên PR #415 (finding P2, `09:39Z 30-08-2026`).
`A6` vì vậy mang thêm **một ca ÂM**: nhãn trần, không lý do ⇒ **ĐỎ**.

**Đây là danh sách CHO PHÉP có chủ ý** — CLAUDE.md: *"Danh sách CẤM không bao giờ đủ; nó phân biệt
CÁCH VIẾT chứ không phân biệt THẨM QUYỀN."* Một danh sách cấm ở đây sẽ phải đoán trước mọi kiểu viết
bộ đếm và thua từ trong thiết kế.

**Phép đo nền của chính luật này** (`09:29:19Z 30-08-2026`, 53 tệp): `27` có mục · `8` ĐẠT · `19` TRƯỢT ·
`N5-LENH-HOOK-WINDOWS.md` **TRƯỢT** (nuôi `A4`) · đặc tả này **ĐẠT** (nuôi `A6`).

## `vi_sao_KHONG_dung_cong_da_de_xuat_o_vong_1`

Ghi vào đặc tả vì nó là **phép đo lật một thiết kế**, không phải ghi chú.

Vòng 1 đề xuất cổng *"docstring trích run/job id phải kèm mỏ neo phạm vi"*. **Đã chạy nó lên chính
đích #411** (`09:05:48Z`–`09:06Z 30-08-2026`):

```
docstring _bash_tuyet_doi:
  có trích run/job id?   True   -> ['99198878779']
  có mỏ neo phạm vi?     True   -> 'Runner'
  ==> PHÁN QUYẾT: XANH  (KHÔNG bắt được)
```

Cổng ấy **xanh trên chính đích nó sinh ra để bắt**. Lý do: docstring **có** nêu mỏ neo; khuyết tật
nằm ở câu **sau đó** khái quát vượt mỏ neo — thuộc **ngữ nghĩa**, không phải từ vựng. Một cổng như
thế **tệ hơn không có cổng**: nó cấp bảo chứng giả.

Kèm một lỗi của **chính bộ đo**, ghi lại vì nó là hình dạng A xảy ra ngay bên trong lượt soạn spec
chống hình dạng A: bản đầu lọc docstring theo **tiền tố dòng** nên `.claude/hooks/**` cho **0** chỗ
trong khi đích nằm đúng ở đó. Đo lại bằng `ast` + `tokenize` mới ra số thật (`hooks+dev`: trích 10,
thiếu mỏ neo 9). **Kết luận rút ra: hình dạng A KHÔNG quy được về một luật văn bản** — nên Đ2 chuyển
sang cưỡng chế **cơ chế đếm** (L4), là thứ đo được, thay vì cưỡng chế **câu chữ**, là thứ không đo được.

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo nào làm nó ĐỎ** (L3). Tiêu chí không thể đỏ thì không phải tiêu chí.

### `A1` (Đ1) — lời khai thu hẹp đúng, và HÀNH VI không đổi

- **ĐẠT khi:** cả `Đ1a` và `Đ1b` nêu rõ mỏ neo là **runner `windows-latest`, job `99198878779`**;
  ghi phản chứng máy Windows thật (`x86_64-pc-linux-gnu`, hai cách dò ĐỒNG Ý); và khai hệ quả
  *"đường tuyệt đối chỉ loại BẤT ĐỒNG, không bảo đảm tránh WSL"*.
- **ĐỎ khi:** `git diff` cho thấy **bất kỳ dòng nào ngoài chú thích/docstring** thay đổi trong
  `.claude/hooks/subagent_ghi_detect_test.py`. Phép đo: thân hàm `_bash_tuyet_doi` và
  `_van_tay_nen_chay` sau khi lược docstring/chú thích phải **giống hệt** bản `6fa8a745`.

### `A2` (Đ1) — không hồi quy bộ test của chính tệp ấy

- **Nền đo `09:12Z 30-08-2026`:** `python -B .claude/dev/packet_loop_test.py` ⇒ `TỔNG: ĐẠT`, `rc=0`,
  `ca 278 · đột biến 81 · lớp lách 78 · ca bắt-oan 35 · ngoại lệ AC 18 = 0`.
- **ĐỎ khi:** sau bản vá, bất kỳ số nào **giảm**, hoặc `ngoại lệ AC 18` **khác 0**, hoặc `TỔNG` khác
  `ĐẠT`. Chép số **TỪ ĐẦU RA MÁY**, đừng gõ tay — chính bộ ấy in dòng *"đếm bằng máy — chép vào hồ sơ
  TỪ ĐÂY"*.

### `A3` (Đ2) — cổng có RĂNG: phải ĐỎ trên một spec mới thiếu bộ đếm

- **ĐẠT khi:** dựng một spec giả `ops/specs/<tên tạm>.md` **thêm mới trong diff** và **không** có
  bộ đếm ⇒ ca đích **ĐỎ**, thông điệp nêu đích danh tên tệp.
- **ĐỎ khi:** ca ấy XANH. Đây là tiêu chí quan trọng nhất — cổng ở vòng 1 chết đúng ở đây.

### `A4` (Đ2) — CHỐNG BẢO CHỨNG GIẢ: cổng phải ĐỎ trên chính `N5-LENH-HOOK-WINDOWS.md`

- **Bằng chứng nền (`09:29:19Z 30-08-2026`, neo theo TIÊU ĐỀ MỤC):**
  `ops/specs/N5-LENH-HOOK-WINDOWS.md` **có** mục `hinh_dang_ke_thua` (1390 ký tự) nhưng **trượt cả ba
  dạng được chấp nhận** — không hàng bảng bộ đếm, không cặp `<A-F> = <số>`, không `khong_ap_dung`, và
  không nhắc tên hình dạng A. Đó **chính là** đường mà lỗi #411 đi lọt.
- **ĐẠT khi:** cho luật chạy trên tệp ấy như thể nó là spec MỚI ⇒ **ĐỎ**.
- **ĐỎ khi:** nó XANH — nghĩa là luật không bắt được ca lịch sử đã biết, tức lại là một cổng xanh
  trên đích của chính nó.

### `A5` (Đ2) — ĐỘT BIẾN đổi màu, theo AC 18

Bộ `packet_loop_test.py` cưỡng chế *"mỗi LỚP LÁCH phải có đột biến của nó"*. Đ2 phải nộp đủ bộ:

| đột biến | phải làm ca đích |
|---|---|
| nới luật để spec **thiếu bộ đếm** đi lọt | **ĐỎ** |
| đổi `--diff-filter=A` thành quét **toàn bộ** `ops/specs` | **ĐỎ** (vì 19 spec cũ sẽ đỏ ⇒ ca bắt-oan bắt được) |
| bỏ nhánh fail-close, cho `BASE` không giải được đi qua thành XANH | **ĐỎ** |
| nới ngoại lệ "bản sao rời" thành *"không giải được `BASE` thì tha"* | **ĐỎ** |
| **bỏ hàng `workflow_dispatch` khỏi bảng `BASE`** | **ĐỎ** — ca đích phải chạy được với `GITHUB_EVENT_NAME=workflow_dispatch` |
| **nhận `khong_ap_dung` trần, không đòi lý do** | **ĐỎ** — ca âm của `A6` |

- **ĐỎ khi:** bất kỳ đột biến nào **SỐNG SÓT**, hoặc bị giết bởi một ca **KHÁC** ca đích, hoặc bị
  giết bằng một ngoại lệ **không phải** assertion của ca đích (tín dụng giả — xem bài học `#355`/`#359`).

### `A6` (Đ2) — ca BẮT-OAN: không được đỏ oan

- **ĐẠT khi (ba ca DƯƠNG):** spec mới **CÓ** bộ đếm hợp lệ ⇒ **XANH** · spec khai `khong_ap_dung`
  **kèm lý do khác rỗng** ⇒ **XANH** · diff **không thêm** spec nào ⇒ **XANH**.
- **ĐẠT khi (hai ca ÂM):** spec mới khai `khong_ap_dung` **TRẦN, không lý do** ⇒ **ĐỎ** ·
  spec mới có mục `hinh_dang_ke_thua` nhưng **rỗng** ⇒ **ĐỎ**.
- **ĐỎ khi:** bất kỳ ca dương nào đỏ, **hoặc** bất kỳ ca âm nào xanh. Thiếu ca âm thì `A6` chỉ chứng
  minh cổng *không kêu bậy*, không chứng minh nó *kêu đúng lúc* — và một cổng chỉ có ca dương là
  cổng không ai biết có răng hay không.

### `A7` — bằng chứng **Windows** trên exact head

- Chủ kho chốt ở vòng 3: **CÓ**, một lượt `workflow_dispatch` trên `ci.yml` tại **exact head**
  trước khi land.
- **ĐẠT khi:** có `run_id` của một lượt mà job `windows-latest` chạy `packet_loop_test.py` và
  bước ấy **không đỏ thêm so nền**.
- **ĐỎ khi:** land mà **không** có `run_id` ấy, hoặc `run_id` neo vào một SHA **khác** head.
- Giá đo `29-08-2026`: ≈**122–136 phút TÍNH TIỀN** mỗi lượt (windows 51–55 phút × hệ số 2, cộng
  ubuntu 20–26). Lượt `pull_request` chỉ chạy `ubuntu-latest` (`ci.yml` d.43–48) nên **KHÔNG** thay
  được. **Gắn nhãn `windows` KHÔNG sinh lượt chạy** — `ci.yml` khai `pull_request:` mà không khai
  `types:`, nên `labeled` không nằm trong cò mặc định.

## `hinh_dang_ke_thua` — L4

**Nguồn là hồ sơ có băm, không phải trí nhớ.** Bộ đếm chép từ
`ops/specs/LEASE-DANG-WINDOWS-r4.md` (chốt `ed5353d`, `2026-08-23 03:30`), xác nhận chéo bởi
`ops/specs/t33-doi-shellcheck-r2.md` (dẫn quyết định của chủ kho tại `#269`):

| | hình dạng | kế thừa | packet này |
|---|---|---|---|
| **A** | *lời khai rộng hơn phép đo* | 7 | **→ 8** |
| **B** | *mượn tiền lệ mà không đo xem nó áp dụng được không* | 2 | 2 |
| **C** | *phản chứng bắt buộc còn thiếu* | 1 | 1 |
| **D** | *đặt câu hỏi kiểm chứng ở sai độ phân giải / sai pha* | 3 | 3 |
| **E** | *khoá theo thứ liệt kê được thay vì theo thứ thật sự chặn* | 4 | 4 |
| **F** | *land trên một nền, đo trên nền khác* | 2 | 2 — **xem cảnh báo dưới** |

**Đơn vị của A (L1):** *số lần một phiên VIẾT RA một lời khai rộng hơn phép đo chống đỡ nó.* Đếm
**lần phạm**, không đếm lần vá — tiền lệ của chủ kho tại `#269`: *"vá một biểu hiện ĐÃ ĐẾM thì không
khai biểu hiện mới"*.

**Vì sao A → 8, đo được:** lời khai `Đ1a` sinh bởi commit `97049d7` (`2026-08-30 04:29`), tức **SAU**
mốc chốt `A = 7` (`2026-08-23 03:30`) ⇒ **biểu hiện MỚI, chưa hồ sơ nào đếm**. Quét mọi spec và biên
nhận sau `23-08` (`09:00:04Z 30-08`) ⇒ **không tệp nào tăng A**. Và `ops/specs/N5-LENH-HOOK-WINDOWS.md`
**không chép bộ đếm A** — đó chính là cơ chế hỏng mà Đ2 sinh ra để chặn.

**Chốt kế thừa nói: `A lần 8 ⇒ DỪNG, không vá.`** Chủ kho đã phán quyết ở vòng 1: **không dừng hẳn,
nhưng cũng không cho vá suông** — packet phải mang **Đ2**, tức thứ khiến lần 9 không xảy ra. Ai đọc
hồ sơ này hãy cân đúng: **nếu Đ2 bị cắt trong lúc thi công thì điều kiện tồn tại của packet mất, và
lối đúng là DỪNG chứ không phải land riêng Đ1.** Xem `dieu_kien_dung` `S4`.

**CẢNH BÁO VỀ `F` — KHÔNG được dùng làm cổng dừng.** `ops/specs/t33-doi-shellcheck-r2.md:337` đính
chính: quét **47** biên nhận trên master ⇒ **0** hiện vật cho `F = 2`; ba chỗ duy nhất nhắc nó đều là
prompt/spec. Chép sang đây để giữ liên tục hồ sơ, **không** để làm cổng. Packet này **KHÔNG** khai
*"F lần 3 ⇒ DỪNG"* dù hình dạng thoạt trông khớp (`A7` giải quyết chuyện Windows bằng một tiêu chí
đo được, không bằng một bộ đếm không có hiện vật).

## `ngan_sach`

### kích thước

- **Trần (fail-closed, lớp `sensitive`):** `≤ 3 tệp` và `≤ 300 dòng THÊM`.
- **Đo bằng:** `git diff --numstat 6fa8a745 -- .claude/hooks/subagent_ghi_detect_test.py .claude/dev/packet_loop_test.py`
  — **pathspec TRONG lệnh**, KHÔNG `..HEAD`.
- **Ước (`09:12Z 30-08`), theo tiền lệ `adr-song` `3df5525` (`+207` riêng tệp test):**
  Đ2 ≈ `+207` · Đ1 ≈ `+25` ⇒ ≈ **`+232` trên 2 tệp**. Dưới trần nhưng **biên mỏng** ⇒ `S2`.
- `da_dung`: **0** (chưa có commit công việc nào lúc soạn). **PHẢI ĐO LẠI trước mỗi bước công bố** —
  bài học `PLAT-X8`: cùng con số trôi 4 lần, lần thứ tư khai sai một cổng là ĐẠT.

### lượt CI Windows

- `ci_dispatch_toi_da`: **1** · `ci_dispatch_da_dung`: **0**.
- Trần **1** vì `A7` chỉ cần **một** lượt xanh trên exact head. Chạm trần mà `A7` chưa đạt ⇒ `S5`.
- Số dư Actions thật **KHÔNG đo được** từ phiên này (proxy chặn `api.github.com/repos/*`; MCP không
  có tool billing) ⇒ trần này là **PHÒNG NGỪA**, không tính từ số dư. Kho **đã cạn hạn mức Actions
  một lần thật**.

### bộ đếm review

- `reviewer_provider`: **`codex`** · `assurance_target`: **`cross_approved`**.
- `codex_review_calls_max`: **2** · `codex_review_calls_used`: **0** · `review_rounds_used`: **0**.
- **Đây KHÔNG phải một lựa chọn của packet — nó là trần của PROTOCOL.** `docs/PROTOCOL_DA_PHIEN.md`
  nói ba chỗ: d.**579** *"Trần 2 lượt Codex/PR, các bộ đếm §12, và mức assurance theo class không đổi"* ·
  d.**597** *"Mỗi PR được dùng tối đa hai lượt Codex"* · d.**811–812** *"tối đa hai trên một PR"*.
  Trần tính **theo PR**, không theo packet.
- **Ghi lại một lỗi của phiên soạn spec, vì nó là hình dạng A ngay trong hồ sơ chống hình dạng A:**
  bản đầu khai `max: 3`. Phiên soạn spec đã **dựng một lựa chọn trái protocol rồi mời chủ kho chọn**,
  và chủ kho chọn `3` từ thực đơn hỏng ấy — phiên **không kiểm protocol trước khi hỏi**. Cross-review
  `codex` bắt được trên PR #415 (finding P1, `09:39Z 30-08-2026`) và phép kiểm tại nguồn gốc xác nhận
  reviewer đúng. Muốn vượt trần thì phải là **override tường minh của chủ kho** viện §2, ghi thành một
  dòng riêng trong lease — **không** bằng cách để một con số rộng nằm im trong đặc tả.
- Đổi prompt, phiên hay tên attempt **KHÔNG** reset bộ đếm (§12). Chạm **2/2** mà chưa `approve` ⇒
  **Review Rescue Checkpoint** (§ trần review budget), **không** phải tự khai `blocked`, và **không**
  được gọi thêm bằng prompt/phiên khác để lách trần.
- Lớp `sensitive` ⇒ `same_provider_approved` **KHÔNG** thay được `cross_approved` (§8).
- `codex` đã chứng minh khả dụng bằng **lời gọi thật** (không phải `codex login status`, thứ NÓI DỐI):
  `codex exec --skip-git-repo-check` ⇒ `rc=0`, `08:22:52Z` và `09:22:4xZ 30-08-2026`.

## `chua_do_duoc`

Ghi thẳng, không giấu sau chữ "có thể":

1. **Ước `+232` dòng là ƯỚC, không phải đo.** Nó ngoại suy từ `adr-song`. Con số thật chỉ có sau khi
   viết. Nếu vượt 300 ⇒ `S2`, KHÔNG tự khai cổng ADR-0044 là ĐẠT.
2. **Chưa đo hành vi luật `BASE` trên lượt `push:master` thật.** `HEAD^1` của commit merge là lý
   thuyết đúng; chưa có lượt CI nào chạy nó. `A7` là chỗ duy nhất phát hiện được.
3. **Chưa đo trên Windows.** Toàn bộ số nền (`ca 278` v.v.) đo trên Linux container. Lượt
   `pull_request` cũng chỉ ubuntu.
4. **`ai-dang-giu` đếm thiếu nhánh** (4 thật vs 3 in ra). Mọi phép đo write set trong tệp này dùng nó,
   nên chúng thừa hưởng khuyết tật ấy. Đã bù bằng phép quét đủ 269 nhánh ở `write_set`; nhưng phép bù
   đó là **thủ công**, chưa thành công cụ.
5. **Không đo được số dư Actions.**
6. **Không khai đã quét hết hình dạng A trong tệp `subagent_ghi_detect_test.py` (960 dòng).** Đã tìm
   được **hai** chỗ (`Đ1a`, `Đ1b`) bằng grep có chủ đích; **chưa ai chứng minh chỉ có hai**. Đây đúng
   caveat mà reviewer #405 nêu và nó **chưa đóng**.

## `dieu_kien_dung`

| | điều kiện | phải làm gì |
|---|---|---|
| `S1` | Cần đường dẫn thứ **ba** | **DỪNG**, trình phép đo, xin mở write set |
| `S2` | Vượt `≤3 tệp` **hoặc** `≤300 dòng thêm` | **DỪNG**, KHÔNG tự khai cổng ADR-0044 là ĐẠT |
| `S3` | Phải sửa `.github/workflows/**`, `ops/leases/**`, `ops/specs/**` từ nhánh packet | **DỪNG** — "không được chạm" nghĩa là **không sửa VÀ không land qua nhánh packet** (nợ N11 sinh ra từ đúng chỗ đọc sai này) |
| `S4` | Đ2 hoá ra không khả thi trong trần | **DỪNG** — **KHÔNG** land riêng Đ1. Điều kiện tồn tại của packet mất (xem `hinh_dang_ke_thua`) |
| `S5` | Chạm trần **1** lượt dispatch mà `A7` chưa đạt | **DỪNG**, `blocked` + failure evidence |
| `S6` | `origin/master` đi tiếp so `base` `6fa8a745` mà chưa đo lại | **DỪNG**, đo lại hai nguồn |
| `S7` | `A2` hồi quy (bất kỳ số nền nào giảm, hoặc `ngoại lệ AC 18 ≠ 0`) | **DỪNG** |
| `S8` | Phát hiện phải đụng `ci_dang_ky_test.py` hoặc hai bộ `cach_ly` | **DỪNG** — đó là packet khác (#361) |
| `S9` | Lúc xin lease, **bất kỳ** đường nào trong write set có `NGƯỜI_GIỮ > 0` | **DỪNG**, không cấp lease |

## `canh_bao_cho_nguoi_thi_hanh`

1. **KHÔNG bắt đầu trước `10:53:00Z 30-08-2026`.** `.claude/hooks/subagent_ghi_detect_test.py` còn
   bị lease #405 giữ. Chủ kho chọn **đợi**, không rút hạn. Đo lại `ai-dang-giu` cho **cả hai** đường
   và đòi `NGƯỜI_GIỮ 0` trước khi xin lease.
2. **`reviewed_sha_required` phải dời sang exact head TRƯỚC khi gọi reviewer**, không phải sau.
   Packet #405 vấp đúng chỗ này và ăn một finding P1 dù `reviewed_sha_ghi_chu` đã cảnh báo trước.
3. **Đừng đổi hành vi khi sửa docstring.** `A1` có phép đo làm nó ĐỎ nếu bạn đổi.
4. **`stderr` RỖNG không phải "không có lỗi" — nó là KÊNH SAI.** Đọc `stdout`.
5. **`core.abbrev=7` phải ghim TRONG mọi clone/sandbox.**
6. **KHÔNG `git push` thẳng `master`, KHÔNG ép qua ruleset.** `merge_pull_request` bị harness chặn;
   chủ kho merge trên UI.
7. **ĐỪNG viết dấu bỏ-qua-CI nguyên văn** vào commit message hay thân PR — GitHub khớp CHUỖI trên
   toàn thông điệp, và squash-merge lấy thân PR làm thông điệp. Đã sập thật một lần (PR #100, và
   merge commit `464124d` của master).
8. **Chạy `python -B ops/lease_publish_test.py` TRƯỚC khi đẩy.** `t33` sẽ ĐỎ cục bộ vì container
   thiếu `actionlint` — đó là **KHÔNG ĐO ĐƯỢC**, không phải lỗi của thay đổi; nền cục bộ đúng là
   `120/121`.
9. **Phép đo delta phải dựng CẢ HAI vế trong MỘT lệnh.** Nếu bạn so nền/sau, đừng dựng hai rig ở hai
   thời điểm — phiên soạn spec này đã tự đẻ ra **hai** bảng kết quả sai vì đúng lỗi ấy (một lần
   `clone --bare` chỉ chép `refs/heads/*` nên mất hai nhánh `ops`; một lần kế thừa một **ref ma**
   `claude/new-session-uples2` có trong cache cục bộ mà `ls-remote` không có).
10. **Đột biến bị giết KHÔNG phải đột biến bị giết ĐÚNG LÝ DO.** `A5` đòi giết bằng assertion của
    **ca đích**; chết vì `TypeError`/`AttributeError` là **tín dụng giả**.
