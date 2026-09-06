# Đặc tả packet — MUTANT-WINDOWS-NHANH-DON-DUOC

- `packet_id`: **MUTANT-WINDOWS-NHANH-DON-DUOC**
- `packet_issue`: **(để trống — chủ kho cấp)**
- `revision`: 1
- `generation`: 1
- `executor`: claude · `environment`: cloud
- `review_class`: **sensitive** (chạm chốt bằng chứng dương của một cổng CI; không rõ ⇒ lấy mức chặt nhất)
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`)
- `depends_on`: **`LO-319-LINUX-BANG-CHUNG-XANH`** và **`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`**
  (cả ba cùng chạm `.claude/dev/ci_dang_ky_test.py` ⇒ write-set exclusion buộc nối tiếp)

## `nguon_cap_viec`

Packet **kế nhiệm**. Nguồn: `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #2
— bộ thứ hai trong hai bộ được để dành ở đó.

Tiền nhiệm trực tiếp: `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT` (bộ thứ nhất của cặp ấy). Packet này
phải đọc biên nhận của packet đó trước khi bắt tay: nó là chỗ ghi những khác biệt cấu trúc mà
lượt review tìm thêm được.

## Bối cảnh đo được (mọi số kèm thời điểm)

### Chi phí — đo lại, không chép

Đo 17:39–17:47Z 06-09-2026, container Linux, **một lượt, không lặp**:

| | ĐẦY ĐỦ | NỀN-ONLY | đột biến | phần đột biến |
|---|---:|---:|---:|---:|
| `ops/nhanh_don_duoc_test.py` | **33 s** | **2 s** | 31 s | **93,9 %** |

`#456` đo bộ này **39 s** cùng ngày. Hôm nay **33 s**. Không số nào sai lúc nó được đo — đây là
lý do `L5` đòi đo lại trước mỗi bước công bố. Đơn vị: **giây tường của một lượt
`python ops/nhanh_don_duoc_test.py`**.

Phần bộ này chiếm trong bước `test registry`: **33 / 400 giây = 8,3 %** (tổng 400 s đo cùng lúc,
tám bộ). Đây là bộ **rẻ nhất trong ba bộ** mang vòng lặp đột biến — nói thẳng vì nó quyết định
thứ tự: packet này đi SAU, không đi trước.

### Bảng đột biến

Đo 17:50Z 06-09-2026: `CA` = **8** mục · `DOT_BIEN` = **10** mục. Một kênh đột biến (khác
`subagent_ghi_detect_test.py` với ba kênh).

### CÁI BẪY — bộ này đã có sẵn một seam, và dùng nó là SAI

`ops/nhanh_don_duoc_test.py:220-233` (`main`):

```python
if os.environ.get("NHANH_DON_DUOC_KHONG_DOT_BIEN"):
    print(f"{tong}/{tong}")
    return 0
mutant_dat = chay_dot_bien()
print(f"{tong}/{tong}")
return 0 if mutant_dat == len(DOT_BIEN) else 1
```

Cách port hiển nhiên nhất — đặt biến ấy trên Windows — **không phát hiện được**. Đo 17:47Z
06-09-2026, hai lượt thật trên cùng cây:

| lượt | dòng mà `MOI[".../nhanh_don_duoc_test.py"]` (`^(\d+)/(\d+)$`) nhìn thấy | `rc` |
|---|---|---:|
| đầy đủ (10 đột biến chạy) | `8/8` | 0 |
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1` (0 đột biến chạy) | `8/8` | 0 |

**Giống nhau từng byte tại điểm quan sát của sổ đăng ký.** Một lượt đo 10 đột biến và một lượt đo
0 đột biến cho **cùng một bằng chứng**. Đó đúng là hình dạng *"cổng không nói dối, nó VẮNG MẶT"* —
và ở đây cái vắng mặt còn ký tên vào chỗ của cái có mặt.

### Lỗ thứ hai, có sẵn từ trước, cùng họ #319

Cùng đoạn mã: `return 0 if mutant_dat == len(DOT_BIEN) else 1`. Nếu `DOT_BIEN` **rỗng** thì
`0 == 0` ⇒ `rc = 0` ⇒ bộ ĐẠT. Bảng đột biến rỗng thoả điều kiện, y hệt `DOT BIEN 0/0 bi giet`.

Và lỗ này **`LO-319-LINUX-BANG-CHUNG-XANH` KHÔNG chữa được**: packet ấy dạy `bang_chung_xanh`
soi mọi cặp `n/m` trong span, nhưng số đột biến của bộ này **chưa bao giờ được in ra** dưới dạng
cặp. Không có gì để soi. Đây là **địa điểm thứ ba** của cùng một hình dạng lỗi, và là địa điểm
duy nhất mà cách chữa phải là **in ra thứ chưa từng in**, không phải soi kỹ hơn thứ đã in.

Nói rõ vì nó đổi phạm vi packet: packet này **không chỉ** cắt đột biến khỏi Windows; nó còn phải
làm cho bằng chứng đột biến của bộ này **tồn tại** ở tầng sổ đăng ký trên **cả hai** nền.

### `MOI` hôm nay

`.claude/dev/ci_dang_ky_test.py:41` — `"ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$"`. Hai nhóm,
span **3 byte**, một cặp (`8/8`). Đây là mẫu chặt nhất trong cả `MOI` về span và lỏng nhất về nội
dung: nó không đòi một chữ nào ngoài hai con số.

### Lease đang giữ

Đo 17:46Z 06-09-2026:

- `ai-dang-giu ops/nhanh_don_duoc_test.py` ⇒ `NGƯỜI_GIỮ 0: không có`.
- `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1:
  mutant-khong-chay-tren-windows-exec-1-claude-20260906` (còn ~20,7 giờ, packet đã land).

Quét hai nguồn: `ls-remote` **295** · `for-each-ref` **295** · `comm -23` rỗng ⇒ không mù.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng thêm**. Write set là **2 tệp** — đúng hình dạng
`PLAT-M4` (2 tệp ⇒ 1 vòng, 1 finding).

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `ops/nhanh_don_duoc_test.py` | nơi vòng lặp đột biến chạy, nơi `rc` được quyết, và nơi bằng chứng đột biến còn thiếu |
| 2 | `.claude/dev/ci_dang_ky_test.py` | nơi mẫu bằng chứng dương của bộ ấy được khai (`MOI`, `MOI_WINDOWS`) |

Không ký tự đại diện. Không đường dẫn nào khác.

## `ngoai_pham_vi`

1. **`ops/nhanh_don_duoc.py`** (mã sản xuất) — không đụng. Packet này sửa cách bộ TEST tự khai
   bằng chứng, không sửa thứ nó đo.
2. **`.github/workflows/ci.yml`** — packet `GATE-TACH-JOB-CAT-CHI-PHI`.
3. **Hai bộ kia** — đã xong ở #456 và `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`.
4. **Không XOÁ seam `NHANH_DON_DUOC_KHONG_DOT_BIEN`.** Nó là đường mà chính runner đột biến dùng
   để chạy bản con mà không đệ quy (`ops/nhanh_don_duoc_test.py:208`). Xoá là làm hỏng vòng lặp
   đột biến. Việc phải làm là **tách hai câu hỏi** — *"đang chạy bản con"* khác *"đang trên
   Windows"* — chứ không phải bỏ biến.
5. **Không đổi bộ ca `CA` hay bảng `DOT_BIEN`.** Bộ này đo `nhanh_don_duoc.py`; packet này không
   có ý kiến gì về việc ấy.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Trên Windows, vòng lặp đột biến KHÔNG chạy. Tám ca nền vẫn chạy đủ. | `write_set` #1 |
| M2 | Bộ in **số mục đột biến** ra bản in trên **cả hai** nền — Linux in số đã giết, Windows in số **không đo ở đây** kèm nơi đo. Hôm nay không nền nào in con số ấy. | `write_set` #1 |
| M3 | Seam `NHANH_DON_DUOC_KHONG_DOT_BIEN` (bản con của runner) và vị từ nền Windows là **hai đường tách biệt**: bản con vẫn in dạng riêng, không mượn dòng Windows. | `write_set` #1 |
| M4 | Bảng đột biến RỖNG ⇒ `rc != 0` trên **mọi** nền — chốt tương đương `len(DOT_BIEN) > 0`, lấp lỗ #319 tại địa điểm thứ ba. | `write_set` #1 |
| M5 | Sổ đăng ký đòi con số ấy: mẫu Linux siết để nhìn thấy cặp đột biến; `MOI_WINDOWS` nhận dòng Windows **chỉ** khi nền là Windows. | `write_set` #2 |
| M6 | Trên Linux, số ca và số đột biến không đổi: `8` ca, `10` đột biến, `rc=0`. | `write_set` #1, #2 |

## `nghiem_thu`

**A1 (M1) — đột biến thật sự không chạy trên Windows.**
Phép làm ĐỎ: giả lập nền Windows qua vị từ THUẦN (`ten_nen="nt"`) rồi đo **số lần sinh tiến trình
con** — bộ này spawn `git archive`, `tar` và một `python` con cho **mỗi** mục trong `DOT_BIEN`
(`ops/nhanh_don_duoc_test.py:195-213`), nên con số ấy còn tỉ lệ với `10` thì ĐỎ.
Không đo bằng thời gian tường.
Đơn vị: **số lần sinh tiến trình con**.

**A2 (M2) — bằng chứng đột biến TỒN TẠI ở bản in, cả hai nền.**
Phép làm ĐỎ, hai chiều:
- lượt Linux đầy đủ mà bản in **không** chứa số đột biến ⇒ ĐỎ;
- lượt Windows mà bản in **không** khai *"không đo ở đây, đo ở ubuntu-latest"* ⇒ ĐỎ.

Đột biến bắt buộc: làm nhánh Windows in **dòng của Linux** ⇒ ca đích ĐỎ.
**Đây là tiêu chí phân biệt được hai lượt mà hôm nay giống nhau từng byte** (`8/8`, `rc=0`) — nếu
sau bản vá hai lượt vẫn cho cùng một bản in thì A2 ĐỎ, bất kể mọi thứ khác xanh.

**A3 (M3) — bản con của runner KHÔNG mượn được đường Windows.**
Phép làm ĐỎ: chạy với `NHANH_DON_DUOC_KHONG_DOT_BIEN=1` trên nền **không** phải Windows ⇒ bản in
phải KHÁC dòng Windows **và** khác dòng Linux đầy đủ. Đột biến bắt buộc: nối hai đường thành một
điều kiện `or` ⇒ ca này phải ĐỎ.
Vì sao cần: nếu bản con in dòng Windows thì mỗi lượt đột biến trên Linux cũng "khai không đo ở
đây", và runner đột biến sẽ đọc nhầm chính bản con của mình.

**A4 (M4) — bảng đột biến rỗng làm bộ ĐỎ.**
Phép làm ĐỎ: đột biến `DOT_BIEN = []` (trên BẢN SAO tạm, không đụng tệp thật — bài học "đột biến
ghi vào tệp THẬT rồi khôi phục trong `finally` là bom hẹn giờ") ⇒ `rc` phải khác 0 trên cả nền
Linux lẫn nền `nt` giả lập. Hôm nay đột biến ấy cho `rc = 0`.
Đơn vị: **mã thoát của tiến trình**.

**A5 (M5) — sổ đăng ký đòi con số, và phân biệt được nền.**
Phép làm ĐỎ, đi qua chính `chay_moi` với năm seam:
- dòng Linux **thiếu** phần đột biến ⇒ **1** đỏ (hôm nay: 0 — mẫu `^(\d+)/(\d+)$` không đòi gì);
- dòng đột biến `0/0` trên nền Linux ⇒ **1** đỏ;
- dòng Windows trên nền Linux ⇒ **1** đỏ;
- dòng Windows trên nền Windows ⇒ **0** đỏ;
- dòng Linux đầy đủ trên nền Windows ⇒ **0** đỏ.

Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A6 (M6) — Linux không đổi về SỐ LƯỢNG đo được.**
`python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`; bản in phải
khai `8` ca và `10` đột biến. Hai con số đo 17:50Z 06-09-2026 — **đo lại tại lúc thi công**.
Nói rõ: bản in **có đổi** (M2 đòi thế). Thứ không được đổi là **số ca chạy** và **số đột biến
chạy** trên Linux. Đây là khác biệt so với M4 của #456, và nó là khác biệt CÓ CHỦ Ý — mẫu cũ của
bộ này không có gì đáng đóng băng, nó đang đóng băng một chỗ mù.

**A7 — bằng chứng Windows THẬT.**
`workflow_dispatch` `ci.yml` trên nhánh packet: job `gate (windows-latest)` `success`, bước
`test registry` `success` với `completed_at` đọc được, và thời lượng bước ấy **nhỏ hơn** thời
lượng của lượt liền trước trên cùng bước.
Đơn vị: **phút tường của bước `test registry` trên `windows-latest`**
(`completed_at − started_at` của BƯỚC, không phải của job). Mốc so sánh phải là lượt Windows gần
nhất **có bước ấy chạy trọn**, đo lại tại lúc thi công — `17,70` phút (run `34045664423`, head
`426bfc0`) là số của **trước** hai packet mutant-Windows, không dùng làm mốc cho packet này.

**A8 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **2** đường dẫn.

**A9 — lease cũ đã thu hồi trước khi bắt tay** (như hai packet anh em).

## `hinh_dang_ke_thua`

| hình dạng | số lần đã gặp | ghi chú |
|---|---:|---|
| tập RỖNG thoả `not song` | **4** | #319 (gốc) · #456 Windows · `LO-319` Linux · **bộ này** (`mutant_dat == len(DOT_BIEN)` với bảng rỗng). Lần thứ tư. `PROTOCOL §12` đòi xem lại CÁCH LÀM từ lần thứ ba — câu trả lời của kho là: **chốt số dương phải nằm ở vị từ `dat`, không nằm ở mẫu regex**, vì mẫu chỉ soi được thứ đã in. |
| nâng `timeout-minutes` để mua cổng xanh | **3** (`25`→`45`→`60`) | Không đụng `ci.yml`. |
| hai lượt khác nhau cho cùng một bằng chứng | **2** | `[skip ci]` làm PR #100 có 0 check mà `mergeable_state: clean` · bộ này: 10 đột biến và 0 đột biến cùng in `8/8` rc=0. Cùng gốc: **cổng vắng mặt trông giống cổng xanh**. |
| chép bản vá đã chứng minh sang bộ khác mà không đo khác biệt cấu trúc | **1** (từ `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`) | Bộ này khác **bốn** chỗ: một kênh (không phải ba), có seam env sẵn, không in dòng `DOT BIEN` nào, gác đột biến bằng `rc` chứ không bằng bản in. |
| số đo trong tài liệu trôi | **≥ 6** | `39`s→`33`s là cái mới nhất, do chính packet này đo. |
| lease không tự chết khi packet đã land | **2** (`#355`, `#456`) | Xem A9. |

## `chua_do_duoc`

1. **Chi phí bộ này trên Windows chưa ai đo** — cùng nợ
   `CHUA-CO-PHAN-RA-THOI-GIAN-THEO-BO-TREN-WINDOWS`. `33 s` là Linux; `test registry` chỉ báo một
   con số cho cả tám bộ.
2. **Bộ này spawn `git archive` + `tar` cho mỗi đột biến.** `tar` có trên `windows-latest` nhưng
   hành vi ống (`Popen ... | tar -x`) trên Windows **chưa từng được đo riêng** — nó luôn nằm
   trong con số gộp của `test registry`. Nếu chi phí Windows của bộ này thấp hơn ước, khoản tiết
   kiệm của packet này nhỏ hơn ước, và A7 sẽ nói ra.
3. **Không có đường đo Windows tại chỗ** (container Linux).
4. **Lỗ "bảng đột biến rỗng" ở M4 chưa từng biểu hiện thật.** Nó là lỗ đo được bằng đột biến, chưa
   phải sự cố đã xảy ra. Ghi đúng như vậy: đây là chốt phòng ngừa, không phải bản vá sau tai nạn —
   khác với #319, vốn sinh ra từ một ca thật.
