# Đặc tả packet — MUTANT-WINDOWS-SUBAGENT-GHI-DETECT

- `packet_id`: **MUTANT-WINDOWS-SUBAGENT-GHI-DETECT**
- `packet_issue`: **(để trống — chủ kho cấp)**
- `revision`: 1
- `generation`: 1
- `executor`: claude · `environment`: cloud
- `review_class`: **sensitive** (chạm chốt bằng chứng dương của một cổng CI — cùng lý do và cùng cặp tệp với #456)
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`)
- `depends_on`: **`LO-319-LINUX-BANG-CHUNG-XANH`** (giao write set tại `.claude/dev/ci_dang_ky_test.py`)

## `nguon_cap_viec`

Packet **kế nhiệm**, không phải khắc phục. Nguồn là
`ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #2, nguyên văn:

> **`subagent_ghi_detect_test.py` (`101`s) và `nhanh_don_duoc_test.py` (`39`s)** — để packet sau.
> […] Khi hình dạng bản vá đã chứng minh trên bộ đầu, chép sang hai bộ kia là việc rẻ.

Hình dạng bản vá đã chứng minh: `0c5e889` + `426bfc0`, land trong `1b3caa1`.

## Bối cảnh đo được (mọi số kèm thời điểm)

### Chi phí — đo lại, không chép

Đo 17:39–17:47Z 06-09-2026, container Linux của phiên này, **một lượt, không lặp**, tách
nền/đột biến trên **BẢN SAO** (tệp thật không bị đụng; bản sao bị xoá sau khi đo):

| bộ | ĐẦY ĐỦ | NỀN-ONLY | đột biến | phần đột biến |
|---|---:|---:|---:|---:|
| `.claude/hooks/subagent_ghi_detect_test.py` | **88 s** | **3 s** | 85 s | **96,6 %** |
| `ops/nhanh_don_duoc_test.py` | 33 s | 2 s | 31 s | 93,9 % |
| `.claude/hooks/pretooluse_guard_test.py` | 270 s | — | — | — |
| 5 bộ còn lại **cộng lại** | 9 s | — | — | — |
| tổng bước `test registry` | **400 s** | | | |

**Ba con số này SỬA số của #456, và cái sửa đáng ghi hơn con số:** #456 đo `subagent` = `101`s và
`nhanh_don` = `39`s ngày 06-09; hôm nay cùng ngày, cùng kho, cùng container-hạng ⇒ `88`s và `33`s.
Không số nào sai lúc nó được đo. Đây là lý do `L5` tồn tại: **đo lại trước mỗi bước công bố**.
`pretooluse_guard_test.py` ở đây `270`s so `346`s của #456 — cùng loại trôi, cùng cách xử lý.

Đơn vị của mọi số trên: **giây tường của một lượt `python <tệp>` đơn lẻ**, không phải giây CPU,
không phải trung bình nhiều lượt.

### Bảng đột biến — đo bằng SỐ MỤC, và bộ này KHÔNG giống bộ đã sửa

Đo 17:50Z 06-09-2026 bằng cách nạp module và đếm `len(...)`:

| bộ | `CA` | `DOT_BIEN` | `DOT_BIEN_NHAM_TEST` | `DOT_BIEN_SETTINGS` | tổng kênh đột biến |
|---|---:|---:|---:|---:|---:|
| `pretooluse_guard_test.py` (đã sửa ở #456) | 39 | 34 | — | — | **1 kênh** |
| `subagent_ghi_detect_test.py` (packet này) | 33 | 22 | 6 | 1 | **3 kênh** |

**Đây là chỗ "chép sang là việc rẻ" KHÔNG còn đúng nguyên văn.** Ba khác biệt cấu trúc, mỗi cái
đều phải xử riêng:

1. **Ba kênh đột biến, không phải một.** `chay()` chạy `DOT_BIEN` rồi — nếu
   `duoc_cong_bo_diem(do_san)` — chạy tiếp `_chay_dot_bien_nham_test()` và
   `_chay_dot_bien_settings()`. Cắt một kênh mà bỏ hai kênh kia là cắt được đúng một phần chi phí
   và để lại hai vòng lặp sinh tiến trình con trên Windows.
2. **Bộ này đã có MỘT nhánh `TONG` thứ hai.** Khi nền đỏ, `duoc_cong_bo_diem` **từ chối** công bố
   điểm đột biến và bộ in `TONG: DIEM DOT BIEN BI TU CHOI …` thay cho dòng
   `TONG: CA n/n dat · DOT BIEN x/y bi giet`. Đo được ngay trong container này lúc 17:41Z:
   `TONG: CA 33/33 dat · DOT BIEN 22/22 bi giet` + `TONG: DAT` (nền xanh ⇒ nhánh thường).
   `pretooluse_guard_test.py` cùng lúc ấy rơi vào nhánh từ chối. Nhánh Windows mới là nhánh
   `TONG` **thứ ba**, và nó phải xếp SAU chốt `duoc_cong_bo_diem`, không phải trước — xem A3.
3. **Bộ này đã có `os.name` trong mã sản xuất** (`_git_for_windows_usr_bin` dòng 468, dựng PATH
   dòng 507). Vị từ nền mới phải là hàm THUẦN riêng, không được tái dùng hay đụng hai chỗ ấy.

### `MOI` và `MOI_WINDOWS` hôm nay

`.claude/dev/ci_dang_ky_test.py:39` — `subagent_ghi_detect_test.py` dùng **CÙNG một chuỗi regex**
với `pretooluse_guard_test.py` ở dòng ngay trên (`:38`):

```
r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT"
```

`MOI_WINDOWS` hiện có **đúng một** mục, và đó là `pretooluse_guard_test.py`. Hai dòng ấy độc lập
theo đúng nghĩa cơ học: `mau_theo_nen(path, mau, la_windows)` tra `MOI_WINDOWS.get(path)` **theo
đường dẫn**, nên thêm một mục cho bộ này **không** đụng mục của bộ kia, và sửa mục của bộ kia
không kéo bộ này theo. Hai mục trùng chuỗi regex là trùng **giá trị**, không phải chung **ô nhớ**.
Nói thẳng vì đọc lướt dễ tưởng ngược lại.

### Vì sao TÁCH khỏi `MUTANT-WINDOWS-NHANH-DON-DUOC`

`ADR-0044` đo được giá của packet to: `PLAT-M4` = 2 tệp ⇒ **1 vòng, 1 finding**; `PLAT-X4` =
4 tệp ⇒ **3 vòng, 8 finding**. Gộp hai bộ vào một packet cho **3 tệp**
(`subagent_ghi_detect_test.py` + `nhanh_don_duoc_test.py` + `ci_dang_ky_test.py`) — đúng trần
`sensitive` và trên đường đi tới hình dạng `PLAT-X4`. Tách ra: mỗi packet **2 tệp**, đúng hình
dạng `PLAT-M4`.

Và hai bộ **không cùng một bản vá**: `nhanh_don_duoc_test.py` có sẵn seam
`NHANH_DON_DUOC_KHONG_DOT_BIEN`, in `n/n` chứ không in dòng `DOT BIEN`, và gác đột biến bằng
`rc` chứ bằng dòng bằng chứng — ba khác biệt làm bản vá của nó khác hẳn. Gộp lại là bắt một lượt
review đọc hai thiết kế khác nhau dưới một cái tên.

### Lease đang giữ — đọc trước khi cấp

Đo 17:46Z 06-09-2026:

- `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1:
  mutant-khong-chay-tren-windows-exec-1-claude-20260906` (cấp 14:30:07Z 06-09, hết hạn
  14:30:07Z 07-09, **còn ~20,7 giờ**) — trong khi packet #456 **đã land** ở `1b3caa1`.
- `ai-dang-giu .claude/hooks/subagent_ghi_detect_test.py` ⇒ `NGƯỜI_GIỮ 0: không có`.

Quét hai nguồn trước đó: `ls-remote` **295** ref · `for-each-ref` **295** ref · `comm -23` rỗng
⇒ không mù.

Lease #456 phải được thu hồi (`thay_the_cho` + `da_bi_thay_the`, hai chiều) trước khi cấp bất kỳ
lease nào chạm `.claude/dev/ci_dang_ky_test.py` — packet này **hoặc**
`LO-319-LINUX-BANG-CHUNG-XANH`, tuỳ cái nào đi trước.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng thêm**. Write set là **2 tệp**. Ước dòng thêm:
#456 làm cùng việc trên bộ một tốn `+144/−5` (đo `git show 0c5e889 --stat`); bộ này có ba kênh
nên ước cao hơn, vẫn dưới `300`. Vượt thì DỪNG trước review, đừng tự khai ngoại lệ.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/hooks/subagent_ghi_detect_test.py` | nơi ba vòng lặp đột biến chạy và nơi `dat` được tính |
| 2 | `.claude/dev/ci_dang_ky_test.py` | nơi mẫu bằng chứng dương của bộ ấy được khai (`MOI`, `MOI_WINDOWS`) |

Không ký tự đại diện. Không đường dẫn nào khác.

## `ngoai_pham_vi`

1. **`ops/nhanh_don_duoc_test.py`** — packet riêng `MUTANT-WINDOWS-NHANH-DON-DUOC`. Lý do ở
   *"Vì sao TÁCH"* bên trên; số liệu ở `ADR-0044`.
2. **`.github/workflows/ci.yml`** — không đụng. Packet này đổi CHI PHÍ, không đổi CỔNG. Trần
   `timeout-minutes` và cách chia job là packet `GATE-TACH-JOB-CAT-CHI-PHI`.
3. **`.claude/hooks/pretooluse_guard_test.py`** — đã xong ở #456, không mở lại.
4. **Lỗ #319 phía Linux** — packet `LO-319-LINUX-BANG-CHUNG-XANH`. Packet này **thừa hưởng** kết
   quả ấy: sau nó, `bang_chung_xanh` soi mọi cặp `n/m` trong span, nên dòng Windows mới phải
   không mang cặp `n/m` nào ngoài cặp CA. Kiểm điều đó là A5.
5. **Hai kênh `DOT_BIEN_NHAM_TEST` / `DOT_BIEN_SETTINGS` KHÔNG bị xoá** — chỉ bị cắt khỏi nhánh
   Windows, y hệt kênh chính. Xoá là làm mất phép đo, không phải dời nó.
6. **Không đụng `_git_for_windows_usr_bin` và khối dựng PATH** (dòng 468, 507) — hai chỗ ấy dùng
   `os.name` cho việc KHÁC (tìm bash của Git for Windows). Trộn vào là gộp hai bất biến không
   liên quan.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Trên Windows, **cả ba** kênh đột biến KHÔNG chạy. Ca nền vẫn chạy đủ 33 ca. | `write_set` #1 |
| M2 | Trên Windows, bộ in một dòng bằng chứng **DƯƠNG** khai rõ đột biến không đo ở đây và đo ở đâu, kèm số mục của **cả ba** kênh. Không mang chữ `bi giet`. | `write_set` #1 |
| M3 | Nhánh Windows đứng **SAU** chốt `duoc_cong_bo_diem`: nền đỏ trên Windows vẫn ĐỎ và vẫn in nhánh từ chối, không được mua cổng xanh bằng đường Windows. | `write_set` #1 |
| M4 | Tiêu chí `dat` của nhánh Windows đòi **số dương ba vế** — chốt tương đương của `len(DOT_BIEN) > 0` cho cả ba kênh. | `write_set` #1 |
| M5 | Sổ đăng ký chấp nhận dòng Windows ấy **chỉ** khi nền là Windows, và vẫn chấp nhận dòng Linux đầy đủ trên Windows (ai chạy tay đo đủ thì không bị phạt). | `write_set` #2 |
| M6 | Trên Linux, hành vi KHÔNG đổi: vẫn `CA 33/33`, vẫn `DOT BIEN 22/22 bi giet`, vẫn ba kênh chạy. | `write_set` #1, #2 |

## `nghiem_thu`

**A1 (M1) — ba kênh thật sự không chạy trên Windows.**
Phép làm ĐỎ: giả lập nền Windows qua vị từ thuần (`ten_nen="nt"`) rồi đo **số lần sinh tiến trình
con** và **số lần nạp bản đột biến bằng `exec`** — hai đơn vị, vì kênh 2/3 nạp bằng `exec` chứ
không spawn (`.claude/hooks/subagent_ghi_detect_test.py:1167`). Cả hai con số phải **không còn tỉ
lệ** với `22 + 6 + 1`. **Không đo bằng thời gian tường** — thời gian trôi theo máy; đây là bài học
đắt nhất của #456 (A1 của nó đo `7.738` so `224` lần spawn, không đo giây).
Đơn vị: **số lần sinh tiến trình con** và **số lần `exec` một bản đột biến**.

**A2 (M2) — chốt bằng chứng dương KHÔNG bị làm im.**
Ba đột biến bắt buộc, mỗi cái phải làm ca đích ĐỎ:
- xoá điều kiện nền ⇒ nhánh Windows chạy trên MỌI nền;
- làm nhánh Windows in dòng **của Linux** (`DOT BIEN 0/0 bi giet`);
- làm dòng Windows khai `0 muc` cho một trong ba kênh.

**A3 (M3) — nền đỏ trên Windows vẫn ĐỎ.**
Phép làm ĐỎ: ép `do_san` khác rỗng (nền đỏ) **và** nền `nt` ⇒ bộ phải trả `rc != 0` và **không**
in dòng bằng chứng Windows. Đột biến bắt buộc: đặt nhánh Windows **TRƯỚC** `duoc_cong_bo_diem` ⇒
ca này phải ĐỎ. Đây là chốt mà `pretooluse_guard_test.py` không cần và bộ này thì cần —
đừng chép bản vá cũ nguyên xi.

**A4 (M4) — `dat` của nhánh Windows đòi số dương ba vế.**
Phép làm ĐỎ: bốn ca cho hàm thuần `dat_windows(so_ca, do, n_chinh, n_test, n_settings)` —
`(33,0,0,6,1)` · `(33,0,22,0,1)` · `(33,0,22,6,0)` · `(0,0,22,6,1)` phải **KHÔNG** đạt;
`(33,0,22,6,1)` phải đạt. Bốn vế rỗng, một vế đủ.
Đơn vị: **giá trị trả về của vị từ thuần**, không phải bản in.

**A5 (M5) — sổ đăng ký phân biệt được nền, HAI CHIỀU, và đi qua `chay_moi`.**
Phép làm ĐỎ:
- dòng Windows trên lượt khai nền **Linux** ⇒ `chay_moi` phải đếm **1** đỏ;
- dòng Windows trên nền **Windows** ⇒ **0** đỏ;
- dòng Linux đầy đủ trên nền **Windows** ⇒ **0** đỏ;
- dòng `DOT BIEN 0/0 bi giet` trên nền **Windows** ⇒ **1** đỏ.

Gọi qua chính `chay_moi` với năm seam, **không** gọi thẳng `mau_theo_nen` — khuyết tật "làm tròn"
nằm ở nơi TIÊU THỤ (bài học r6/#401).
**Và một chốt riêng cho packet `LO-319`:** dòng Windows mới không được chứa cặp `n/m` nào ngoài
cặp CA. Phép làm ĐỎ: thêm một cặp `0/0` vào dòng ấy ⇒ sau `LO-319` phải ĐỎ.
Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A6 (M6) — Linux không đổi.**
`python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`, và bản in của
bộ này phải còn nguyên dạng `TONG: CA 33/33 dat · DOT BIEN 22/22 bi giet`. Hai con số `33` và
`22` là đo 17:41Z 06-09-2026 — **đo lại tại lúc thi công**, đừng chép.
Phép làm ĐỎ: `MOI[path]` bị sửa một ký tự ⇒ ca neo mẫu-nguyên-bản ĐỎ (dựng theo mẫu
`p456-mau-linux-KHONG-DOI-so-voi-base` đã có sẵn cho bộ kia).

**A7 — bằng chứng Windows THẬT, không phải suy luận.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Đòi: job `gate (windows-latest)` có
`conclusion == success`, bước `test registry` có `conclusion == success` với `completed_at` đọc
được, **và** thời lượng bước ấy **nhỏ hơn** `17,70` phút (số đo Windows của run `34045664423`,
head `426bfc0`, 06-09-2026). Đọc qua `actions_list` + `method: list_workflow_jobs` trên
`/mcp/x/actions`.
Đơn vị: **phút tường của bước `test registry` trên `windows-latest`**, lấy từ
`completed_at − started_at` của bước, không lấy từ tổng job.
Phép làm ĐỎ: thời lượng không giảm ⇒ A7 ĐỎ ⇒ đó là **KẾT QUẢ ĐO** (giả định "Windows đắt gấp ~3"
sai), không phải thất bại thiết kế — báo chủ kho, đừng nới gì để ép nó xanh.

**A8 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **2** đường dẫn.

**A9 — lease cũ đã thu hồi trước khi bắt tay.** Như `LO-319` A8: `ai-dang-giu
.claude/dev/ci_dang_ky_test.py` phải trả về lease của packet này, không phải
`mutant-khong-chay-tren-windows-exec-1-claude-20260906`.

## `hinh_dang_ke_thua`

Chép từ biên nhận và đặc tả của `MUTANT-KHONG-CHAY-TREN-WINDOWS` (#456), cộng phần packet này đo
được:

| hình dạng | số lần đã gặp | ghi chú |
|---|---:|---|
| nâng `timeout-minutes` để mua cổng xanh | **3** (`25`→`45`→`60`) | Packet này không đụng `ci.yml`. |
| tập RỖNG thoả `not song` (`0/0` là bằng chứng) | **3** | #319 · #456 Windows · Linux (`LO-319`). Nhánh Windows của packet này phải mang chốt tương đương cho **ba** kênh, không phải một. |
| chép bản vá đã chứng minh sang bộ khác mà không đo khác biệt cấu trúc | **0 (mới)** | Packet này là lần ĐẦU kho làm việc ấy. Ba khác biệt đã đo và ghi ở phần bối cảnh; nếu review tìm ra cái thứ tư thì bộ đếm này lên 1 và packet kế phải đọc nó trước. |
| số đo trong tài liệu trôi giữa lúc viết và lúc đọc | **≥ 6** | `117/100`→`120/110` · `37`→`39` · `3/90`→`3/100` · `4/120`→`5/121` · `101`s→`88`s · `39`s→`33`s. Hai cái cuối do chính packet này đo. |
| lease không tự chết khi packet đã land | **2** (`#355`, `#456`) | Xem A9. |

## `chua_do_duoc`

1. **Chi phí của bộ này trên WINDOWS chưa ai đo.** Số `88 s` là Linux. Không có phân rã theo bộ
   trên `windows-latest` ở bất kỳ lượt nào — `test registry` chỉ báo **một** con số cho cả tám bộ
   (`17,70` phút, run `34045664423`). Nên khoản tiết kiệm mà packet này mua được là **ước theo tỉ
   lệ**, không phải đo; A7 là phép đo trả lời câu ấy. Ghi thành nợ có tên
   **`CHUA-CO-PHAN-RA-THOI-GIAN-THEO-BO-TREN-WINDOWS`**.
2. **Không có đường đo Windows tại chỗ.** Container Linux. Mọi khẳng định về hành vi Windows đi
   qua CI, và đó là lý do vị từ nền phải là hàm THUẦN nhận `ten_nen` — nếu chỉ đọc `os.name` thật
   thì phản chứng A1/A5 cần máy Windows mới chạy được, tức không ai canh.
3. **Nền của bộ này XANH trong container soạn spec** (`rc=0`, `33/33`, `22/22`, 17:41Z) — khác
   `pretooluse_guard_test.py` (`rc=1`, 3 ca đỏ sẵn). Đừng suy rằng phiên thi công cũng sẽ thấy
   nền xanh: `CLAUDE.md` đã đo bốn ca rig tự đẻ hồi quy giả. Dựng hai vế **trong MỘT lệnh**.
4. **Kênh `DOT_BIEN_SETTINGS` chỉ có 1 mục.** Một chốt "số dương" trên một tập một phần tử là
   chốt yếu — nó không phân biệt được "có đo" với "đo đúng một thứ". Chưa có cách làm nó mạnh hơn
   trong phạm vi packet này; ghi thẳng thay vì làm tròn thành đã canh.
