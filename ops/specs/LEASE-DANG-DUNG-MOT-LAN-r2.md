# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`, **bản sửa đổi 2**

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (§3.2, §4) mới được bắt tay.
>
> Bản sửa đổi 1 (`ops/specs/LEASE-DANG-DUNG-MOT-LAN.md`, sha256 `e1026adb…`) **KHÔNG bị sửa và
> KHÔNG bị xoá** — nó là thứ lease lượt 1 neo và biên nhận lượt 1 trỏ tới. Bản này **thay thế**
> nó cho mọi lượt từ đây trở đi.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN`
`packet_issue`: `#227`
`ke_thua`: `ops/specs/LEASE-DANG-DUNG-MOT-LAN.md` (sha256 `e1026adb569f5b4732197afac9c0f35cdd5a8945d46301b1d4cb062624e7c72c`)

## Vì sao có bản sửa đổi này

Lượt review 1 (`claude`, verdict sha256 `42b438ad…`) kết luận **`can_sua`**: 2×P1, 1×P2, 4×P3.
Người giữ kho chọn **sửa đặc tả trước, rồi vá lại** (2026-08-21).

**Bản sửa đổi 1 là NGUYÊN NHÂN của P1 thứ nhất.** Mục tiêu 4 của nó ghim thẳng cơ chế:

> *"hai lớp mới chỉ áp khi đang chạy trong Actions (`GITHUB_ACTIONS` có mặt), đúng tiền lệ của
> lớp `GITHUB_ACTOR` ngay trong tệp"*

Tiền lệ ấy **không áp dụng được**, và đặc tả đã không đo trước khi mượn nó. `GITHUB_ACTOR` là
một phép so **CHUỖI THUẦN**; hai lớp mới là **LỜI GỌI MẠNG**. Mà bộ tự kiểm của chính cổng chạy
**BÊN TRONG Actions** và **không bước nào cấp `GH_TOKEN`**, nên `GITHUB_ACTIONS` có mặt ở đúng
chỗ ta **không** muốn hai lớp ấy chạy. Đo được trên `fefa15b6`:

```
$ GITHUB_ACTIONS=true python3 ops/lease_publish_test.py
  ĐỎ  t01_lease_hop_le_thi_QUA … t02c … t02d … t09 … t14 … t21
lease_publish: 46/52 đạt      rc=1
```

`chay_lease_publish_test.sh` giữ mã thoát và bước `tự kiểm cổng` có `set -euo pipefail` ⇒ job
`dang` chết **trước** bước `tìm lease`. **Land nguyên trạng = cổng đăng lease tự khoá vĩnh
viễn**, và `ci.yml` cũng đỏ.

**Hai finding, MỘT quyết định.** P2 (mỏ neo comment) cũng sinh ra từ chỗ ấy: đưa lời gọi mạng
vào `kiem()` làm `lenh_body` **cũng** gọi mạng (đo: `check` 2 lời gọi, `body` 2 lời gọi), sinh
thêm một khe `check`→`body` mà khi thua thì `body` trả `rc=9` và **giết cả bước**. Đúng doctrine
của kho: **đếm HÌNH DẠNG lỗi, đừng chỉ đếm lỗi** — cùng một hình dạng lặp lại thì câu hỏi đúng
là *"có nên làm việc này không"*, không phải *"vá thế nào"*.

## Quyết định MỚI — Q9…Q14

| # | quyết định | căn cứ ĐO ĐƯỢC |
|---|---|---|
| **Q9** | **`kiem()` GIỮ THUẦN — không lời gọi mạng nào.** Hai lớp GitHub chuyển sang **một lệnh con RIÊNG** (`lease_publish.py kiem-github <tệp>`), và **CHỈ** bước `đăng` của workflow gọi nó. **BỎ HẲN** việc dò `GITHUB_ACTIONS`. | Cả P1-1 lẫn nửa sau của P1-2 chết theo **KIẾN TRÚC**, không theo bản vá. Bộ selftest gọi `check`/`body` nên không bao giờ chạm mạng ⇒ suite xanh ở mọi môi trường. `body` hết gọi mạng ⇒ khe `check`→`body` biến mất. Tiền lệ: `shell_environment_policy` — bốn lượt vá rồi mới bỏ cả lớp rủi ro. |
| **Q10** | Lớp chạy **vì workflow GỌI nó**, không vì một biến môi trường có mặt. Chạy tay `check` ở máy vẫn phải **NÓI RA** là hai lớp ấy chưa chạy. | "Có mặt biến" là suy đoán về ngữ cảnh; "có lời gọi" là sự thật. Dòng khai vẫn cần vì `check` xanh mà thiếu hai lớp là một câu nửa vời. |
| **Q11** | `DA_DOI=1` ghi vào `$GITHUB_ENV` **ngay sau mỗi `mark`, TRONG vòng lặp**. `kiem-github`, `body`, `gh api` POST và `mark` đều bọc `set +e` và rẽ về cùng nhánh `BI_CHAN=1; continue` như `check`. | P1-2. Q4/Q5 của bản 1 chỉ đúng cho **đúng một** đường đỏ. Đo: POST 403 ⇒ `GITHUB_ENV` **rỗng** ⇒ `always() && env.DA_DOI == '1'` SAI ⇒ ghi ngược vẫn bị bỏ qua. |
| **Q12** | Mỏ neo comment phải **neo TÁC GIẢ**: chỉ tính comment do `github-actions[bot]` đăng, và dấu phải nằm ở **ĐẦU** thân. Thiếu `user.login` ⇒ **CHẶN**. Thêm phép kiểm dạng `lease_id` (`^[A-Za-z0-9._-]+$`) trong `kiem()`. | P2, đo hai chiều: (a) comment của `nguoi-la` mang dấu ⇒ lease chính đáng `rc=9` **vĩnh viễn**, workflow in "đã đăng trước đó", **không** đặt `BI_CHAN` ⇒ **lượt chạy XANH**; (b) `lease_id` chứa `` ` `` và `**` ⇒ lease A bịt được lease B. Q2 dời bản ghi từ chỗ **có cổng ghi** sang chỗ **ai cũng ghi được** mà quên chốt danh tính. |
| **Q13** | `--slurp` trả **`[]`** (không trang nào) ⇒ **CHẶN**. `[[]]` (một trang rỗng) ⇒ issue thật sự chưa có comment ⇒ **cho qua**. | P3. `all(...)` trên danh sách rỗng là `True` ⇒ trạng thái thứ ba sập thành "chưa đăng". |
| **Q14** | `T49` đo bằng **MẪU**, không bằng một tên đoán trước: bơm `os.environ` đầy biến khớp `*GH*` `*GITHUB*` `*API*` `*PATH*` rồi đòi số lời gọi tới mối nối giả **không đổi**. | P3: đột biến `[os.environ.get("GH_PATH") or "gh", …]` **SỐNG SÓT** `52/52`. Đúng bài "danh sách cấm không bao giờ đủ — phải đảo thành danh sách cho phép" của chính kho. |
| **Q15** | `T52` phải đo **HÀNH VI**, không khớp chuỗi `if:`. | P3, và đây là **lý do P1-2 lọt**: `t52` chỉ kiểm `"always()" in buoc.get("if")` nên **không thể đỏ**. `t51` đã chứng minh thân bước đo được thật. |
| **Q16** | Thông báo khi lời gọi đo loại số hiệu **hỏng** phải nêu **"số hiệu trỏ vào PR là một nguyên nhân có thể"**, và **khai rõ đó là phỏng đoán, không phải phép đo**. | P3: workflow không có `pull-requests`, nên với một PR lời gọi `GET /issues/{n}` **có thể** trả 403 ⇒ thông báo thực tế là `KHÔNG ĐO ĐƯỢC` chứ không phải câu nêu `pull-requests` mà Q1 mua. Chưa ai đo được nhánh ấy ⇒ **không được khai là đã đo**. |

**Q1…Q8 của bản 1 GIỮ NGUYÊN**, trừ hai chỗ bị Q9 và Q11 ghi đè: mục tiêu 4 cũ (dò
`GITHUB_ACTIONS`) **BỎ**; Q4/Q5 cũ được **siết** chứ không đảo chiều.

**Q8 (executor `codex` để thử giả thuyết) — giả thuyết ĐÃ BỊ BÁC BỎ.** Hình dạng *lời khai rộng
hơn phép đo* trước lượt này đếm 5 lần, cả 5 cùng `claude`; lượt này `codex` mắc nó (Q5 khai rộng
hơn `T52` đo). Bộ đếm nay là **6, hai tác giả**. Executor vẫn là `codex` — nhưng vì **liên tục
ngữ cảnh mã**, KHÔNG còn vì một giả thuyết.

## `write_set`

Không đổi so với bản 1 — đúng **ba** đường dẫn:

```
.github/workflows/ops-publish-lease.yml
ops/lease_publish.py
ops/lease_publish_test.py
```

**Ngân sách MỚI: ≤ 3 tệp, ≤ 500 dòng THÊM** so với `cfaccff9`. Người giữ kho nới trần
300 → 500 trong phiên 2026-08-21, có chủ đích và ghi ra đây.

Nêu số để đối chiếu (L1, đơn vị = dòng thêm theo `git diff --numstat cfaccff9..HEAD`): bản vá
lượt 1 đo được **+298**; bảy finding cần vá, trong đó `T52` phải viết lại thành phép đo hành vi
và `T49` phải viết lại theo mẫu. **Vượt 500 ⇒ DỪNG, xuất handoff.** Vẫn KHÔNG được tự chia nhỏ
packet và KHÔNG được tự nới trần (§2).

## `ngoai_pham_vi`

Giữ nguyên bảng của bản 1, thêm hai mục:

| thứ | vì sao KHÔNG làm |
|---|---|
| Cấp `GH_TOKEN` cho bước `tự kiểm cổng` | Đó là vá P1-1 bằng cách cho bộ **test** một credential thật. Q9 giết cả lớp rủi ro; cấp token là giữ nguyên nó rồi mua thêm một bề mặt. |
| Đổi `dung_than()` | Vẫn ngoài phạm vi. Q12 siết **phía đọc** và siết **đầu vào `lease_id`**, không đụng phía sinh. |

## `muc_tieu`

Mỗi mục chiếu vào **một** đường dẫn trong `write_set` (L2). Thay trọn bộ mục tiêu của bản 1.

1. **`ops/lease_publish.py`** — `kiem()` **THUẦN**: không `subprocess`, không mạng, không đọc
   `GITHUB_ACTIONS`. Thêm phép kiểm dạng `lease_id`.
2. **`ops/lease_publish.py`** — lệnh con **`kiem-github <tệp>`**: đo loại số hiệu (issue / PR /
   KHÔNG ĐO ĐƯỢC) và dò comment đã đăng theo dấu **có neo tác giả**. Ba trạng thái ở **mọi**
   lớp; trạng thái thứ ba **CHẶN**. Mã thoát dùng lại bảng cũ (`9` = đã đăng).
3. **`ops/lease_publish.py`** — đúng **một** mối nối `GOI_GH`, mặc định `gh api`, **không** chọn
   được bằng biến môi trường hay trường trong lease.
4. **`ops/lease_publish.py`** — `check` chạy tay phải **NÓI RA** rằng hai lớp GitHub chưa chạy.
5. **`.github/workflows/ops-publish-lease.yml`** — bước `đăng` gọi `kiem-github` **trước**
   `check`; mọi lệnh trong vòng lặp bọc `set +e`; hỏng ⇒ `BI_CHAN=1; continue`; `DA_DOI=1` ghi
   vào `$GITHUB_ENV` **ngay sau mỗi `mark`**; cuối vòng `BI_CHAN != 0` ⇒ **thoát khác 0**.
6. **`.github/workflows/ops-publish-lease.yml`** — bước ghi ngược giữ `if: always() && …`.
7. **`ops/lease_publish_test.py`** — phản chứng cho cả sáu mục, đồ giả **GIỮ TRẠNG THÁI**.

## `nghiem_thu`

Giữ `T43`–`T51` của bản 1 (chuyển sang đo lệnh con `kiem-github`), **viết lại** `T49`, `T52`,
và thêm bốn ca. Mỗi tiêu chí nêu **phép đo nào làm nó ĐỎ** (L3). Đột biến chạy trên **bản sao tạm**.

| # | mục tiêu | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|---|
| T49′ | 3 | Bơm `os.environ` đầy biến khớp `*GH*`/`*GITHUB*`/`*API*`/`*PATH*` ⇒ số lời gọi tới mối nối giả **không đổi** | `[os.environ.get("GH_PATH") or "gh", …]` — đột biến này **SỐNG SÓT** ở lượt 1, phải chết ở lượt 2 |
| T52′ | 5,6 | **Chạy thân bước**: POST của lease **giữa** hỏng ⇒ lease **cuối vẫn đăng**, `$GITHUB_ENV` **có** `DA_DOI=1`, rc≠0 | (a) ghi `DA_DOI` một lần ở cuối vòng · (b) bỏ `set +e` quanh POST — **hai đột biến riêng** |
| **T53** | 1 | **Toàn suite phải `N/N` khi `GITHUB_ACTIONS`/`GITHUB_REPOSITORY`/`GITHUB_ACTOR` ĐƯỢC ĐẶT** và `gh` **vắng** | cho `kiem()` gọi mạng trở lại ⇒ ca này ĐỎ. **Đây là ca khoá P1-1; không có nó thì lỗi ấy lọt lần nữa** |
| **T54** | 2 | Comment mang dấu do **người ngoài** đăng ⇒ **KHÔNG** tính là đã đăng | bỏ lọc `user.login` |
| **T55** | 2 | Thiếu `user.login` ⇒ **CHẶN** · dấu **không** ở đầu thân ⇒ không tính | coi thiếu tác giả là "không phải bot" rồi cho qua |
| **T56** | 1 | `lease_id` chứa `` ` `` hoặc `*` ⇒ **CHẶN** ở `kiem()` | bỏ phép kiểm dạng ⇒ lease A bịt lease B |
| **T57** | 2 | `--slurp` trả `[]` ⇒ **CHẶN**; trả `[[]]` ⇒ **cho qua** | coi `[]` là "chưa có comment" |
| **T58** | 2,4 | `check`/`body` **không** sinh lời gọi `GOI_GH` nào; `check` in dòng khai hai lớp chưa chạy | gọi `kiem-github` từ trong `kiem()` |

Ngoài các ca trên: **suite `rc=0`, `N/N` hai số bằng nhau, ≥ 58 ca**; mỗi đột biến giết **đúng ca
của nó**. Đột biến giết nhiều ca ⇒ **NÓI RA**. Lượt 1 đã có một ca như vậy (đột biến "bỏ lớp
comment" giết `t46` **và** `t48`) — lượt 2 phải **tách hai ca đó ra**.

## `hinh_dang_ke_thua`

Hai hình dạng, cả hai nay đều **đa tác giả** — chép theo L4.

**A. *lời khai rộng hơn phép đo*** — bộ đếm **6**:

| lần | ở đâu | tác giả |
|---|---|---|
| 1–3 | PLAT-X5 review 1/2/3 | `claude` |
| 4–5 | DONREF review 1/2 | `claude` |
| **6** | **#227 lượt 1**: Q5 khai "ghi ngược chạy kể cả khi bước đăng đỏ" — đúng cho **đúng một** đường đỏ; `T52` khớp CHUỖI nên **không thể đỏ** | **`codex`** |

**Giả thuyết *"hình dạng bám người viết, không bám bài toán"* BỊ BÁC BỎ.** Hệ quả cho packet
này: **đổi executor không phải phương thuốc**; thứ phải siết là **phép đo**, và đó chính là
`T52′`, `T53`, `T58`.

**B. *mượn một tiền lệ mà không đo xem nó có áp dụng được không*** — bộ đếm **2**:

| lần | ở đâu | tác giả |
|---|---|---|
| 1 | `os.getpgid` mượn từ POSIX sang Windows ⇒ suite **0/103** trên `windows-latest`, không ai biết vì job Windows mặc định SKIP | `claude` |
| **2** | **Bản sửa đổi 1 của chính đặc tả này**: mượn tiền lệ `GITHUB_ACTOR` (so CHUỖI) cho một **lời gọi mạng** ⇒ P1-1 | **`claude`** (phiên soạn đặc tả) |

**Chốt cho lượt 2:** gặp hình dạng **A** lần thứ **7**, hoặc hình dạng **B** lần thứ **3** ⇒
**DỪNG, không vá**, xuất handoff, trả về người giữ kho.

## `chua_do_duoc`

1. **Không có lượt chạy GitHub Actions THẬT nào** trên bản vá. `T51`/`T52′` đo thân bước trích
   từ YAML (tiền lệ `t32`), và đó **không** phải một lượt chạy. Bằng chứng thật chỉ có ở lần
   đăng lease kế tiếp sau khi land.
2. **Chưa ai đo GitHub có cho `issues: write` ĐỌC một PR qua `GET /issues/{n}` hay không.** Q16
   vì vậy chỉ được **phỏng đoán có khai**, không được khai là đã đo.
3. **Khe race giữa "hỏi comment" và "đăng comment" vẫn MỞ** — hai lượt chạy trên hai nhánh
   `ops/**` khác nhau, cùng một lease. `concurrency` gom theo `github.ref` nên **không** gom hai
   nhánh khác nhau. Q9 xoá khe `check`→`body` (vì `body` hết gọi mạng) nhưng **không** đụng khe
   này. **Thu hẹp**, không phải **đóng**.
4. **7 comment trùng đã đăng** và **4 tệp lease thiếu `posted_comment_id`** vẫn nằm đó (Q7).
5. **`tri-thuc-review-1-codex-20260821` chưa từng được đăng**, #214 đã đóng.
6. **Chưa đo trên Windows.** `ci.yml` chỉ chạy `ubuntu` cho PR thường; muốn có Windows trước khi
   merge thì phải gọi tay `workflow_dispatch` trên ref đó — **gắn nhãn `windows` KHÔNG đủ** cho
   một PR đang mở (`ci.yml` khai `pull_request:` không kèm `types:` nên `labeled` không bắn).
