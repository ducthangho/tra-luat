# Đặc tả packet — DOT-BIEN-L-BIEN-CONG-KHAI (revision 1)

- `packet_id`: **DOT-BIEN-L-BIEN-CONG-KHAI**
- `packet_issue`: **#677**
- `mission_issue`: **KHONG_CO**. Đây là nợ số 3 mang sang từ #579, không thuộc lane kế hoạch nào.
- `revision`: **1** · soạn **08:01Z 29-09-2026** · nền đo `origin/master` **`1741e0a`**; đo lại 08:05Z trên **`89fc4fa`**
  (sau khi #676 land, PR #680): giàn Phụ lục A cho cùng `KHAC-GOI 32 · KHAC-RC 4 · = 10`, suite vẫn 187 `@ca`
- `depends_on`: **`[]`** về mã. Về **lease** thì phải chờ #676 nhả `ops/lease_publish_test.py` (xem §9).
- `executor`: claude · reviewer: codex `gpt-6-astra` (effort ≥ medium) · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**
- `assurance_target`: **human_audited**

> Mọi con số trong tệp này đều kèm mốc đo. Đo lại TRƯỚC mỗi bước công bố: cấp lease, đăng verdict, merge.
> Các quyết định neo vào BẤT BIẾN, còn con số chỉ để đối chiếu.

---

## 1. `nguon_cap_viec`

Nợ mang sang của packet #579. Nguồn:

- Human audit [`pull/589#issuecomment-5857502345`](https://github.com/ducthangho/tra-luat/pull/589#issuecomment-5857502345).
- Biên nhận land [`issues/579#issuecomment-5858147839`](https://github.com/ducthangho/tra-luat/issues/579#issuecomment-5858147839), mục "Nợ mang sang":
  *"Vế 'biên công khai' của đột biến `L`: `KHÔNG ĐO ĐƯỢC`"*.
- Đặc tả cha `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md` (sha256 `c8a72a41…0dc2`), §7.8, §10 mục 8, §12.4.

**Đột biến `L`**: gỡ hai dòng chốt `lease_id` khỏi `_tien_kiem_mien_dang` trong `ops/lease_publish.py`:

```python
    if not isinstance(lease.get("lease_id"), (str, int)) or isinstance(lease.get("lease_id"), bool):
        raise Chan(RC_NOI_DUNG, "tiền kiểm: thiếu `lease_id` hoặc sai kiểu")
```

`t178` đã giết `L` ở **đơn vị phép dò** (`_do_dau_da_dang`): nền 0 lời gọi GitHub, `L` 1 lời gọi. Câu hỏi của
packet này: khác biệt ấy có nguy hiểm ở **biên công khai** không, tức ở thân bước `đăng` của
`.github/workflows/ops-publish-lease.yml` khi chạy với `ops/lease_publish.py` THẬT.

## 2. Phép đo của lượt soạn spec — và lời khai SAI mà nó đã sửa

### 2.1 — Giàn đo

Phụ lục A là giàn, chép nguyên văn (sha256 của tệp giàn lúc chép: `fb1950d4…e98b`). Giàn làm ba việc:

1. Trích thân bước `đăng` bằng `_buoc_workflow("đăng")` của chính `ops/lease_publish_test.py`.
2. Chép `ops/lease_publish.py` của cây vào một `$NEO` tạm, ở hai vế: **nền** (nguyên văn) và **`L`** (gỡ đúng hai dòng trên).
   Mỗi lượt dùng một thư mục tạm riêng, với `PYTHONDONTWRITEBYTECODE=1`.
3. Đặt `gh` giả trên **PATH**. `gh` giả **giữ trạng thái**: mỗi số hiệu có danh sách comment và cờ "là PR"; POST thêm comment vào đó.
   Mọi lời gọi được ghi lại dưới dạng `(method, endpoint)`.

**Lần đo đầu, giàn HỎNG, và đây là bẫy chính của packet.** `lease_publish.py` gọi `gh` qua `subprocess` (`GOI_GH`),
chứ không qua thân bước. Thay chuỗi `gh api` trong thân bước là KHÔNG đủ. Khi đó mọi lượt, kể cả ca đối chứng
hợp lệ, đều cho `rc=1` với 0 lời gọi, vì `[Errno 2] No such file or directory: 'gh'`. Bắt được nhờ **ca đối
chứng dương**. Mọi số dưới đây là của giàn đã sửa.

### 2.2 — Không gian đã đo: BA trục (luật Q11)

| trục | giá trị | số giá trị |
|---|---|---|
| `lease_id` trong YAML | `null` · `~` · `[wp579-thu]` · `true` · `yes` · `{x: 1}` · `1.5` · `1.50` · `2026-09-29` · `123` · `wp-ok-1` | 11 |
| số hiệu `packet_issue: 55` | Issue · Pull Request | 2 |
| trạng thái comment | trống · đã có comment `github-actions[bot]` bắt đầu bằng ``**Lease `str(giá trị)`**`` | 2 |
| dạng tài liệu (chỉ ở ô Issue, trống) | thiếu `lease_id` · tài liệu là danh sách | 2 |

Tổng: 11 × 2 × 2 + 2 = **46 dòng**, mỗi dòng chạy hai vế ⇒ **92 lượt chạy bước** (đo 08:01Z 29-09, `1741e0a`).

### 2.3 — Kết quả (đo 08:01Z 29-09-2026, `1741e0a`)

| lớp kết quả | số dòng | nơi xảy ra |
|---|---|---|
| **lệch MÃ THOÁT** của bước | **4** | `true` · `1.5` · `1.50` · `2026-09-29`, mỗi dạng × **PR** × **đã có dấu** |
| chỉ lệch số lời gọi `gh` (mã thoát, POST, log trùng) | 32 | các ô còn lại của **9** dạng `lease_id` bị tiền kiểm chặn (`null` `~` danh sách `true` `yes` ánh xạ `1.5` `1.50` ngày; 9 × 4 − 4) |
| trùng hoàn toàn | 10 | `123` · `wp-ok-1` (4 ô mỗi dạng) · hai dạng tài liệu |

Chi tiết bốn dòng lệch mã thoát:

| `lease_id` | nền | `L` |
|---|---|---|
| `true` · `1.5` · `1.50` · `2026-09-29` (+ PR + có dấu) | `rc=1`, bước **ĐỎ** (`hai lớp GitHub chặn (rc=8)`: số hiệu là PR) | `rc=0`, *"đã đăng trước đó — bỏ qua"*, bước **XANH** |

Dạng `yes` rơi vào "chỉ lệch số lời gọi" ở ô PR + có dấu. Lý do là **tạo tác của fixture**: giàn dựng dấu theo chữ `yes`,
trong khi YAML 1.1 đã ép giá trị thành `True`. Đo riêng với dấu ``**Lease `True`**`` (07:58Z 29-09) thì `yes` cũng
lệch mã thoát, y như `true`.

Không ô nào có POST ở vế này mà không có ở vế kia. Log hai vế chỉ lệch dấu thời gian `hết hạn`, vì fixture gọi `mai_sau()` mỗi lượt.

### 2.4 — Cơ chế

Với `L`, phép dò chạm mạng, thấy dấu, rồi ném `RC_DA_DANG`. Nhánh đã-có-dấu của `kiem_github` chạy
`kiem(bo_qua_han=True)`. Hàm này **nhận** `True`/`1.5`/date: nó làm `str()` trước khi so regex, nên `"True"`,
`"1.5"`, `"2026-09-29"` đều khớp `LEASE_ID`. Nhánh ấy **không chạy `_kiem_loai_so_hieu`**, đúng giới hạn mà docstring
`kiem_github` đã khai. Trên nền, chốt `lease_id` chặn phép dò, nên chuỗi cũ chạy trọn và `_kiem_loai_so_hieu` bắt được "số hiệu là PR".

⇒ **Chốt `lease_id` của `_tien_kiem_mien_dang` có răng ở biên công khai**: nó giữ ĐỎ một tổ hợp mà `L` biến thành XANH.

### 2.5 — Lời khai SAI đã rút lại

Thân Issue #677 lúc tạo (06:19Z 29-09) khai *"vô hại, cho cả 13 dạng"*. Lời khai ấy được đo trên HAI trục
(`lease_id` × trạng thái comment) và **thiếu hẳn trục loại số hiệu**. Rút lại ở
[`issues/677#issuecomment-5886120520`](https://github.com/ducthangho/tra-luat/issues/677#issuecomment-5886120520).
Dấu hiệu đã báo trước mà lượt đầu đọc sót: chênh số lời gọi `L − nền` có giá trị **−1**, tức `L` bỏ qua một
lời gọi mà nền có. Đó là lời gọi `GET issues/55` của `_kiem_loai_so_hieu`.

## 3. Quyết định của chủ kho (29-09-2026, hai vòng, chấp nhận nguyên văn mọi khuyến nghị)

| câu | quyết định |
|---|---|
| **Q1** | Ca biên khoá **cả bộ quan sát** cho tập (i) ở §6: `rc` bước, dãy `(method, endpoint)`, số POST. |
| **Q2** | Các dạng ép kiểu mà hiện đang **được đăng** (Issue thật, chưa có dấu) **không** khoá ở đây. Đó là việc của #678. |
| **Q3** | **Helper mới** (tạm tên `_chay_buoc_dang_that`). **Không** sửa `_chay_buoc_dang`. |
| **Q4** | Ba đột biến bắt buộc ĐỎ **đúng lý do**: `L`; `gh` giả vắng khỏi PATH; `gh` giả không ghi POST. |
| **Q5** | Trần ADR-0044 cho `sensitive`: **≤ 300 dòng thêm**, 1 tệp, không xin ngoại lệ. Vượt thì DỪNG và hỏi. |
| **Q6** | Bỏ qua trên Windows **chỉ** qua `_ly_do_bo_qua_workflow` (tức `os.name == "nt"` **và** job chỉ chạy Ubuntu). Không chạy CI Windows. |
| **Q7** | `human_audited`; spec nằm trên nhánh riêng, land qua PR bookkeeping, không tính vào write set. |
| **Q8** | Tổ hợp §2.3 xếp **NGUY HIỂM** (mất tín hiệu đỏ ở cổng). Nền đã đúng ⇒ **không vá `ops/lease_publish.py`**; chỉ khoá. |
| **Q9** | Tập khoá chia hai, (i) và (ii), xem §6. Tập (ii) thay phần "loại dạng ép kiểu" của Q2 cho riêng ô PR + có dấu. |
| **Q10** | Đóng băng spec ngay; **chờ** #676 land hoặc hết hạn rồi mới xin lease; không xin #676 nhả sớm. Sau #676: #677 rồi #678. |
| **Q11** | Mọi kết luận "vô hại" hoặc "nguy hiểm" phải kèm **danh sách TRỤC đã đo**. Reviewer được giao nhiệm vụ **tìm trục còn thiếu**. |

## 4. `review_class`

`sensitive`. Đo 08:05Z 29-09: `_tinh_lop_tu_write_set(['ops/lease_publish_test.py'])` ⇒ `sensitive`. Kèm giới hạn đã
biết từ #603: hàm này hiện chỉ trả được `sensitive`.

## 5. `write_set`

- `ops/lease_publish_test.py`

**Một đường dẫn.** Không có `ops/lease_publish.py` (Q8: nền đúng, không vá). Không có `.github/workflows/**`.
Không có `CLAUDE.md`. Tệp spec này nằm trên nhánh spec và land qua PR bookkeeping (Q7).

## 6. `muc_tieu`

Mỗi mục chiếu vào `ops/lease_publish_test.py`.

- **M1** — Helper `_chay_buoc_dang_that`. Nó chạy thân bước `đăng` trích bằng `_buoc_workflow("đăng")`, với:
  - `$NEO/ops/lease_publish.py` **chép từ cây đang test** (không phải bản giả, không phải bản neo master);
  - `gh` giả **giữ trạng thái**, đặt trên **PATH**;
  - trả về `rc`, dãy `(method, endpoint)`, danh sách comment đã POST, và `out`.

  Cờ "số hiệu là PR" là một tham số. Helper nhận một **nguồn `lease_publish.py` tuỳ chọn**, để phép đột biến
  không phải ghi đè tệp thật.
- **M2** — Ca biên **tập (i)**, khoá cả bộ quan sát:
  - `lease_id` ∈ {`null`, danh sách, ánh xạ} × {Issue, PR} × {trống, có dấu};
  - và hai dạng tài liệu: thiếu `lease_id`, tài liệu là danh sách.

  Kỳ vọng trên nền, đo 08:01Z 29-09: `rc=1`, **0 lời gọi `gh`**, 0 POST.
- **M3** — Ca biên **tập (ii)**, chỉ khoá `rc ≠ 0`, 0 POST, và **không có** dòng `đã đăng trước đó — bỏ qua`:
  - `lease_id` ∈ {`true`, `1.5`, `2026-09-29`} × **PR** × **có dấu** ``**Lease `str(giá trị)`**``.

  **Không** khoá dãy lời gọi ở tập này, để giữ đúng khi #678 đổi đường từ chối (Q9).
- **M4** — **Đối chứng dương**: `lease_id: wp-ok-1`, Issue, trống ⇒ `rc=0`, **đúng 1 POST**, thân bắt đầu bằng
  ``**Lease `wp-ok-1`**``. Nó là thứ làm giàn hỏng không thể xanh (§2.1).
- **M5** — Docstring của ca nêu:
  - (a) bảng trục đã đo, theo §2.2;
  - (b) vì sao tập (i) khoá dãy lời gọi: đó là **tín hiệu phân biệt** của `L`, không phải vì lượt GET thừa nguy hiểm;
  - (c) vì sao tập (ii) chỉ khoá mã thoát;
  - (d) trỏ #678 cho các dạng ép kiểu **được đăng**.

  Mọi câu khai phải nêu phép đo đứng sau nó, hoặc nói thẳng `KHÔNG ĐO ĐƯỢC`.

## 7. `nghiem_thu`

Mọi đột biến chạy trên **BẢN SAO TẠM** của cây (CLAUDE.md), bằng `python ops/lease_publish_test.py --chi-ca=<tên ca>`.
Ca đỏ được đọc từ dòng `ĐỎ  <tên>: <lý do>`.

| mã | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **A1** | Tập (i) (M2) xanh trên nền | Đột biến **`L`** ⇒ ca M2 **ĐỎ**, lý do nêu dãy lời gọi (0 → 1 GET `comments`). Không được đỏ vì ngoại lệ vô can. |
| **A2** | Tập (ii) (M3) xanh trên nền | Đột biến **`L`** ⇒ ca M3 **ĐỎ** qua **mã thoát** (nền `rc=1` → `L` `rc=0` + dòng "bỏ qua"). Đây là tiêu chí chính của packet (Q8). |
| **A3** | Đối chứng dương (M4) xanh | Đột biến **`gh` giả không nằm trên PATH** (chỉ thay chuỗi trong thân bước, như lỗi của §2.1) ⇒ ca M4 **ĐỎ**. |
| **A4** | Đối chứng dương đo POST thật | Đột biến **`gh` giả in id nhưng KHÔNG ghi comment vào trạng thái** ⇒ ca M4 **ĐỎ** ở chốt "đúng 1 POST". |
| **A5** | Mỗi đột biến A1–A4 đỏ **đúng lý do** | Với mỗi đột biến: ca đỏ phải là **đúng ca đích**, và lý do phải là **thông điệp chốt tường minh của ca**, không phải `AttributeError`/`KeyError`/`FileNotFoundError`… (hình dạng `GIET-NHUNG-KHONG-DUNG-LY-DO`). Người thi hành ghi nguyên dòng `ĐỎ` cho từng đột biến. |
| **A6** | Không hồi quy | Toàn suite `python ops/lease_publish_test.py` ⇒ dòng tổng kết `N/N` với **N = số `@ca` đếm tĩnh**, hai số bằng nhau. Nền 187 ca, đo 07:57Z trên `1741e0a` và 08:05Z trên `89fc4fa` (sau khi #676 land); đo lại lúc thi hành. |
| **A7** | Trần kích thước | `git diff --numstat origin/master...HEAD -- ops/lease_publish_test.py` ⇒ **≤ 300** dòng thêm; không tệp nào khác trong diff mã. |
| **A8** | Không đụng giàn cũ | `_chay_buoc_dang` và `t51`–`t68` **bằng byte** `origin/master` (so bằng `ast` hoặc `git diff`); `--chi-ca=t5` và `--chi-ca=t6` xanh. |
| **A9** | Bỏ qua nền đúng chỗ | Ca mới chỉ ném `BoQuaNen` qua đúng đường của `_chay_buoc_dang`. Phản chứng: trên Linux, ca **không** được `BỎ QUA` (dòng `BỎ QUA` vắng mặt). |
| **A10** | Cổng phụ | `ruff check --select F ops/lease_publish_test.py`: **delta so master = 0**. `doctrine-scan`, `adr-song`, `git diff --check`: rc=0. |

## 8. `ngoai_pham_vi`

1. **Các dạng `lease_id` ép kiểu được ĐĂNG** (Issue, chưa có dấu: `true`/`yes`/`on` → `True`, `1.50` → `1.5`,
   `0x1F` → `31`, `017` → `15`, date) và **va chạm danh tính** giữa chúng. Đó là packet **#678** `LEASE-ID-EP-KIEU-YAML`.
   Khoá hành vi "được đăng" ở đây là chôn lỗi vào test (Q2).
2. **Giới hạn đã khai của nhánh đã-có-dấu**: nó bỏ `_kiem_loai_so_hieu`, nên **chuỗi hợp lệ** + PR + có dấu vẫn ra
   `rc=0` bỏ qua, ở CẢ nền lẫn `L` (đo 08:01Z 29-09). Đây là đánh đổi có chủ đích của #579, không do `L`. Packet này không đổi nó.
3. **Sửa `ops/lease_publish.py`**: nền đúng (Q8).
4. **Sửa `.github/workflows/**`**.
5. **Đo trên endpoint HTTP thật của GitHub**: xem §10.

## 9. Lease — điều kiện trước khi cấp

Đo 08:05Z 29-09-2026, sau khi so `ls-remote` 508 với `for-each-ref` 508, thiếu 0 (lần đo trước: 07:57Z, 506/506):

- `ai-dang-giu ops/lease_publish_test.py` ⇒ **`NGƯỜI_GIỮ 1`**: `t131-deadline-dem-spawn-exec-1-claude-20260929` (#676).
- Lease ấy cấp `2026-09-29T06:05:00Z`, hết hạn `2026-09-30T06:05:00Z`. Lúc 07:57Z nó nằm trên `origin/ops/cap-lease-676`; lúc 08:05Z trên
  `origin/claude/bookkeeping-676`. Mã của #676 **đã land** (PR #680 → `89fc4fa`), nhưng lease **vẫn CÒN_HẠN**:
  land không tự nhả lease (CLAUDE.md, *"LEASE KHÔNG TỰ CHẾT KHI PACKET ĐÃ LAND"*).

**Bất biến (neo quyết định vào đây, không vào con số):** chỉ xin lease cho #677 khi `ai-dang-giu ops/lease_publish_test.py`
cho `NGƯỜI_GIỮ 0`, đo trên đủ ref ngay trước lúc cấp. `start_from_sha` là `origin/master` **tại lúc cấp**, không phải `1741e0a`.

## 10. `chua_do_duoc`

1. **Tổ hợp §2.3 có xảy ra ngoài đời không.** Nó cần một comment của `github-actions[bot]` **trên một PR**, bắt đầu
   đúng bằng ``**Lease `True`**`` (hoặc `1.5`, ngày…). Workflow đăng lease có đăng được lên PR với `issues: write`
   hay không là `KHÔNG ĐO ĐƯỢC` từ phiên này: không có REST tới `repos/…`, và thử bằng cách đăng thật là ghi ra ngoài.
   Q8 xếp nguy hiểm **bất kể** câu này.
2. **Endpoint HTTP thật.** Mọi phép đo đi qua `gh` giả. Hình dạng phản hồi thật của `gh api --paginate --slurp`
   chỉ được mô phỏng, theo đúng dạng mà `_kiem_comment_da_co` chấp nhận.
3. **Windows.** Ca bỏ qua trên Windows (Q6), nên hành vi của giàn trên Windows `KHÔNG ĐO`: đây là **chọn không đo**.
4. **Sau #676.** #676 có thể đổi số ca và vị trí dòng trong tệp. A6/A7 phải đo lại lúc thi hành.

## 11. `hinh_dang_ke_thua`

Chép từ `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md` §6 (packet cha #579), cộng phần phát sinh ở lượt soạn này:

| hình dạng | số lần | nguồn |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 6 → **7** | **+1** ở lượt soạn này: *"vô hại cho cả 13 dạng"* đo trên 2 trục, thiếu trục loại số hiệu (§2.5). Chủ kho (Q11) cho tiếp, kèm luật khai trục. |
| `THOI-DIEM-DO-GAN-SAI` | **1** | MỚI. Vòng 1 của lượt soạn gắn mốc *"đo 06:4xZ"* cho `NGƯỜI_GIỮ 0`, trong khi số ấy đo **trước** 06:05Z. Lease #676 cấp 06:05Z, nên quyết định Q7 được đưa ra trên một số đã chết. |
| `GIET-NHUNG-KHONG-DUNG-LY-DO` | 2 | Chép. Chống bằng A5. |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 2 | Chép. |
| `DEM-SU-CO-MAT-THAY-VI-KHA-NANG` | 1 | Chép. Chính giàn hỏng của §2.1 là một ca gần: `gh` giả CÓ MẶT trong thân bước mà không ai gọi nó. Không đếm +1 vì bắt được trước khi thành lời khai. |
| `CHOT-DO-SAI-TOAN-TU` | 1 | Chép. |
| `DOT-BIEN-SONG-SOT-VI-NHANH-CHUA-AI-CHAM` | 1 | Chép. |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | Chép. |
| `VA-BANG-REGEX-RONG-HON-Y-DINH` | 1 | Chép. |

## 12. Việc của reviewer (Q11)

Ngoài review thường lệ, reviewer phải **tìm trục còn thiếu** trong §2.2. Mỗi trục mới mà làm một kết luận của §2.3
hoặc của ca M2/M3 đổi thì là một finding. Gợi ý khởi đầu, không phải trần: `packet_issue` sai kiểu cùng lúc với
`lease_id` sai kiểu; comment bot có dấu nằm ở **trang thứ hai** của `--paginate`; lease đã hết hạn.

---

## Phụ lục A — giàn đo của lượt soạn (chép nguyên văn)

Chạy: `python do_bien_L.py <gốc kho> [kq.json]`. Bảng in ra stderr; cột cuối `KHAC-RC` / `KHAC-GOI` / `=`.
Giàn **không** thuộc write set. Nó chỉ là bằng chứng tái lập của §2. Ca M1–M4 thay nó trong kho.

**Trích đúng khối — bẫy đã gặp:** tệp này có HAI khối `python`. Khối ở §1 là hai dòng chốt; giàn là khối
**CUỐI**. Lượt soạn đã trích nhầm khối đầu và nhận `IndentationError`. Lệnh đúng (đo 08:06Z 29-09: sha256 của
khối trích ra = `fb1950d4…e98b`, chạy cho `KHAC-GOI 32 · KHAC-RC 4 · = 10`):

```
python -c "import sys;s=open(sys.argv[1],encoding='utf-8').read();open('do_bien_L.py','w',encoding='utf-8').write(s.rsplit(chr(96)*3+'python\n',1)[1].rsplit(chr(96)*3+'\n',1)[0])" ops/specs/dot-bien-l-bien-cong-khai-r1.md
```

```python
"""Đo đột biến L ở BIÊN workflow `ops-publish-lease.yml` bước `đăng`.

Chạy thân bước TRÍCH TỪ YAML với `ops/lease_publish.py` THẬT (nền và L, bản sao tạm),
và một `gh` giả GIỮ TRẠNG THÁI (issue, comments; POST thêm comment vào state).
Ghi: lời gọi gh theo (method, endpoint), rc bước, comment đã đăng, stdout/stderr.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("dùng: python do_bien_L.py <gốc kho> [tệp kết quả .json]")
KHO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(KHO / "ops"))
import lease_publish_test as T  # noqa: E402
import yaml  # noqa: E402

THAN = T._buoc_workflow("đăng")["run"]
GOC_SRC = (KHO / "ops" / "lease_publish.py").read_text(encoding="utf-8")
DONG_L = ('    if not isinstance(lease.get("lease_id"), (str, int)) or isinstance(lease.get("lease_id"), bool):\n'
          '        raise Chan(RC_NOI_DUNG, "tiền kiểm: thiếu `lease_id` hoặc sai kiểu")\n')
assert GOC_SRC.count(DONG_L) == 1, "không định vị được chốt lease_id"
BIEN_THE = {"nen": GOC_SRC, "L": GOC_SRC.replace(DONG_L, "")}

GH_GIA = r'''
import json, os, pathlib, sys
a = sys.argv[1:]
assert a[0] == "api", a
a = a[1:]
st = pathlib.Path(os.environ["GH_STATE"]); d = json.loads(st.read_text())
log = pathlib.Path(os.environ["GH_LOG"])
ep = [x for x in a if x.startswith("repos/")][0]
method = "POST" if "--input" in a else "GET"
with log.open("a") as f: f.write(json.dumps([method, ep, a]) + "\n")
parts = ep.split("/")  # repos o r issues N [comments]
so = parts[4]
iss = d["issues"].get(so)
if iss is None:
    print('{"message":"Not Found"}'); print("gh: Not Found (HTTP 404)", file=sys.stderr); sys.exit(1)
if len(parts) == 5:
    loai = "pull" if iss.get("pr") else "issues"
    print(json.dumps({"number": int(so), "html_url": f"https://github.com/o/r/{loai}/{so}"})); sys.exit(0)
if method == "GET":
    print(json.dumps([iss["comments"]])); sys.exit(0)
body = json.loads(pathlib.Path(a[a.index("--input") + 1]).read_text())["body"]
cid = 7000 + len(iss["comments"])
iss["comments"].append({"id": cid, "body": body, "user": {"login": "github-actions[bot]"}})
st.write_text(json.dumps(d)); print(cid)
'''


def yaml_lease(lid_raw, bo_lease_id=False, packet_issue=55, top_list=False):
    d = T.lease_mau(packet_issue=packet_issue)
    d.pop("lease_id")
    van = yaml.safe_dump(d, allow_unicode=True, sort_keys=False)
    if not bo_lease_id:
        van += f"lease_id: {lid_raw}\n"
    if top_list:
        van = "- " + van.replace("\n", "\n  ").rstrip() + "\n"
    return van


def chay(bien_the, van_yaml, comments_san, la_pr=False):
    with tempfile.TemporaryDirectory() as t:
        goc, neo = Path(t) / "goc", Path(t) / "neo"
        (goc / "ops" / "leases").mkdir(parents=True); (neo / "ops").mkdir(parents=True)
        (neo / "ops" / "lease_publish.py").write_text(BIEN_THE[bien_the], encoding="utf-8")
        (neo / "gh_gia.py").write_text(GH_GIA, encoding="utf-8")
        (goc / "ops" / "leases" / "x.yaml").write_text(van_yaml, encoding="utf-8")
        (goc / "ds.txt").write_text("ops/leases/x.yaml\n", encoding="utf-8")
        st, log = Path(t) / "st.json", Path(t) / "gh.log"
        st.write_text(json.dumps({"issues": {"55": {"comments": list(comments_san), "pr": la_pr}}}))
        log.write_text("")
        py = sys.executable
        than = THAN.replace("python3 ", f"'{py}' ")
        assert "python3 " not in than and than.count("gh api ") == 1
        bin_ = Path(t) / "bin"; bin_.mkdir()
        (bin_ / "gh").write_text(f"#!/bin/sh\nexec '{py}' '{neo}/gh_gia.py' \"$@\"\n")
        (bin_ / "gh").chmod(0o755)
        mt = dict(os.environ, NEO=str(neo), REPO="o/r", GITHUB_REPOSITORY="o/r",
                  GITHUB_ACTOR="ducthangho", GH_TOKEN="gia", GH_STATE=str(st), GH_LOG=str(log),
                  PYTHONDONTWRITEBYTECODE="1", PATH=f"{bin_}:{os.environ['PATH']}")
        p = subprocess.run(["bash", "-c", than], cwd=goc, env=mt, capture_output=True, text=True)
        goi = [tuple(json.loads(x)[:2]) for x in log.read_text().splitlines()]
        sau = json.loads(st.read_text())["issues"]["55"]["comments"]
        moi = sau[len(comments_san):]
        return {"rc": p.returncode, "goi": goi, "dang": [c["body"].splitlines()[0] for c in moi],
                "out": (p.stdout + p.stderr)}


def bot(body):
    return {"id": 1, "body": body, "user": {"login": "github-actions[bot]"}}


FIX = [
    # nhãn, yaml lease_id, dấu mà str() của giá trị Python sẽ dựng
    ("null", "null", "None"),
    ("~ (null)", "~", "None"),
    ("list", "[wp579-thu]", "['wp579-thu']"),
    ("bool true", "true", "True"),
    ("bool yes? (YAML1.1 safe_load: str)", "yes", "yes"),
    ("mapping", "{x: 1}", "{'x': 1}"),
    ("float 1.5", "1.5", "1.5"),
    ("float 1.50", "1.50", "1.5"),
    ("date", "2026-09-29", "2026-09-29"),
    ("int (hợp lệ ở tiền kiểm)", "123", "123"),
    ("str hợp lệ (đối chứng)", "wp-ok-1", "wp-ok-1"),
]

if __name__ == "__main__":
    kq = []
    for nhan, raw, dau_str in FIX:
      for la_pr in (False, True):
        for tt, san in (("trong", []),
                        ("co-dau-bot", [bot(f"**Lease `{dau_str}`** — đăng tự động")])):
            dong = {"fixture": nhan, "yaml": raw, "issue": ("PR-" if la_pr else "issue-") + tt}
            for bt in ("nen", "L"):
                dong[bt] = chay(bt, yaml_lease(raw), san, la_pr)
            kq.append(dong)
    for tt, san in (("issue-trong", []),):
        for nhan, van in (("thiếu lease_id", yaml_lease(None, bo_lease_id=True)),
                          ("tài liệu là danh sách", yaml_lease("wp-ok-1", top_list=True))):
            dong = {"fixture": nhan, "yaml": "-", "issue": tt}
            for bt in ("nen", "L"):
                dong[bt] = chay(bt, van, san)
            kq.append(dong)
    json.dump(kq, open(sys.argv[2] if len(sys.argv) > 2 else "/dev/stdout", "w"),
              ensure_ascii=False, indent=1)
    print(f"{'fixture':38} {'issue':17} | nền: rc goi dang | L: rc goi dang | KHÁC?", file=sys.stderr)
    for d in kq:
        n, l = d["nen"], d["L"]
        tom = lambda r: f"{r['rc']} {[g[0][0]+':'+g[1].split('/',3)[3] for g in r['goi']]} {len(r['dang'])}"
        khac = (n["rc"], n["goi"], n["dang"]) != (l["rc"], l["goi"], l["dang"])
        nhan = "KHAC-RC" if n["rc"] != l["rc"] else "KHAC-GOI" if khac else "="
        print(f"{d['fixture']:38} {d['issue']:17} | {tom(n)} | {tom(l)} | {nhan}",
              file=sys.stderr)
```
