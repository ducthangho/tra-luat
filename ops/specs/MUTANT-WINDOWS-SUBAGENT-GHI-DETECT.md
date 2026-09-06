# Đặc tả packet — MUTANT-WINDOWS-SUBAGENT-GHI-DETECT

- `packet_id`: **MUTANT-WINDOWS-SUBAGENT-GHI-DETECT** (bí danh chữ; ID bền theo `PROTOCOL §3.2`
  là `wp<packet_issue>`, suy ra được ngay khi có số Issue — tiền lệ #456)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp;** khuyến nghị chung cho bốn packet ở
  `GATE-TACH-JOB-CAT-CHI-PHI.md`**)**
- `revision`: 1 · `generation`: 1 — giữ 1 có chủ ý (nháp thứ ba của revision 1, chưa có Issue nên
  chưa đóng băng; lý do đầy đủ và quy ước `lease_id …-exec-1rN-…` đo được ở `LO-319` dòng `revision`)
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (chạm chốt bằng chứng dương của một cổng CI
  — cùng lý do và cùng cặp tệp với #456)
- `depends_on`: **`GATE-TACH-JOB-CAT-CHI-PHI`**, **`LO-319-LINUX-BANG-CHUNG-XANH`** — cả ba cùng
  chạm `.claude/dev/ci_dang_ky_test.py`; thứ tự nối tiếp **cố định** `GATE → LO → 2A (packet này)
  → 2B`. Bản đầu viết *"packet này HOẶC `LO-319`, tuỳ cái nào đi trước"* — ngược với chính
  `depends_on` (verdict lượt 1, P2); bỏ.
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`) — **chỗ giữ,
  không phải mỏ neo.** Ba mỏ neo trong lease (`base_sha` · `start_from_sha` ·
  `reviewed_sha_required`) phải cùng bằng head `origin/master` **SAU khi `LO-319` đã integrated**
  (`§5`), đo tại lúc cấp. Không có SHA tương lai nào để điền hôm nay, và điền một SHA cũ là neo
  review vào một cây không còn tồn tại. Quy tắc này nằm trong đặc tả đóng băng, không chỉ trong
  chú thích YAML.

## `nguon_cap_viec`

Packet **kế nhiệm**, không phải khắc phục. Nguồn là
`ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #2, nguyên văn:

> **`subagent_ghi_detect_test.py` (`101`s) và `nhanh_don_duoc_test.py` (`39`s)** — để packet sau.
> […] Khi hình dạng bản vá đã chứng minh trên bộ đầu, chép sang hai bộ kia là việc rẻ.

Hình dạng bản vá đã chứng minh: `0c5e889` + `426bfc0`, land trong `1b3caa1`.

Bản này là **bản sửa theo verdict cross-review lượt 2** (`reviewed_sha` `b1c2284`, Codex), sau lượt 1
(`d09f2f1`): đổi đối chứng A1 theo P2 `mot-diem-spawn-khong-do-duoc-ti-le`, thu hồi lease theo P1
`bia-mo-mot-ref-khong-thu-hoi-moi-ban`, và mọi câu về `LO-319` theo thiết kế T (bản ghi TỔNG).

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

Chạy lại 19:30Z 06-09-2026 ở lượt sửa này: `subagent_ghi_detect_test.py` **75 s** đầy đủ (`rc=0`,
`CA 33/33`, `DOT BIEN 22/22`); `nhanh_don_duoc_test.py` **34 s**. Cùng máy, cùng cây, hai giờ sau:
`88 → 75`. **Ba lần đo, ba con số** (`101` · `88` · `75`) — không số nào sai lúc nó được đo. Đây là
lý do `L5` tồn tại, và là lý do A1 **không** đo bằng giây.

Đơn vị của mọi số trên: **giây tường của một lượt `python <tệp>` đơn lẻ**, không phải giây CPU,
không phải trung bình nhiều lượt.

### Bảng đột biến — đo bằng SỐ MỤC, và bộ này KHÔNG giống bộ đã sửa

Đo 17:50Z 06-09-2026 bằng cách nạp module và đếm `len(...)` (đo lại 19:35Z: không đổi):

| bộ | `CA` | `DOT_BIEN` | `DOT_BIEN_NHAM_TEST` | `DOT_BIEN_SETTINGS` | tổng kênh đột biến |
|---|---:|---:|---:|---:|---:|
| `pretooluse_guard_test.py` (đã sửa ở #456) | 39 | 34 | — | — | **1 kênh** |
| `subagent_ghi_detect_test.py` (packet này) | 33 | 22 | 6 | 1 | **3 kênh** |

**Đây là chỗ "chép sang là việc rẻ" KHÔNG còn đúng nguyên văn.** Ba khác biệt cấu trúc, mỗi cái
đều phải xử riêng:

1. **Ba kênh đột biến, không phải một.** `chay()` chạy `DOT_BIEN` rồi — nếu
   `duoc_cong_bo_diem(do_san)` và không có `TL329_KHONG_LAP` — chạy tiếp
   `_chay_dot_bien_nham_test()` và `_chay_dot_bien_settings()`. Cắt một kênh mà bỏ hai kênh kia là
   cắt được đúng một phần chi phí và để lại hai vòng lặp sinh tiến trình con trên Windows.
2. **Bộ này đã có 2 nhánh in dòng TỔNG** (đọc `chay()` tại
   `.claude/hooks/subagent_ghi_detect_test.py:1256-1265`, 21:03Z 06-09-2026): khi nền đỏ,
   `duoc_cong_bo_diem` **từ chối** công bố điểm đột biến và bộ in `TONG: CA n/33 dat` +
   `TONG: DIEM DOT BIEN BI TU CHOI …` thay cho `TONG: CA n/n dat · DOT BIEN x/y bi giet`. Đo 19:30Z:
   `TONG: CA 33/33 dat · DOT BIEN 22/22 bi giet` + `TONG: DAT` (nền xanh ⇒ nhánh thường).
   `pretooluse_guard_test.py` cùng container rơi vào nhánh từ chối. Nhánh Windows mới sẽ là nhánh in
   dòng tổng **thứ 3** — thiết kế, chưa có trong mã — và nó phải xếp SAU chốt `duoc_cong_bo_diem`,
   không phải trước — xem A3.
3. **Bộ này đã có `os.name` trong mã sản xuất** (`_git_for_windows_usr_bin` dòng 468, dựng PATH
   dòng 507). Vị từ nền mới phải là hàm THUẦN riêng, không được tái dùng hay đụng hai chỗ ấy.

### Số lần sinh tiến trình con và số lần `exec` — nền đối chứng cho A1

Đo 19:35Z và 19:41Z 06-09-2026, nạp module thật, bọc `subprocess.run` và `builtins.exec` bằng bộ
đếm, không sửa tệp. Đơn vị: **số lần gọi `subprocess.run`** (bộ này không gọi `Popen` trực tiếp) và
**số lần `exec` một bản đột biến** (mã biên dịch từ chuỗi, `co_filename` dạng `<tên>`):

| pha | `subprocess.run` | `exec` bản đột biến | ghi chú |
|---|---:|---:|---|
| ca nền — 33 hàm trong `CA`, gọi `f(None)` | **438** | 0 | `S_nen`; ≈ 13,3 spawn/ca |
| `chay()` với `TL329_KHONG_LAP=1` (nền + kênh 1 `DOT_BIEN`) | **10.045** | 0 | ⇒ kênh 1 ≈ **9.607** = 22 mutant × ≈ 437 |
| kênh 2 `_chay_dot_bien_nham_test()` một mình | **10** | **6** | 6 mục, mỗi mục một `exec` |
| kênh 3 `_chay_dot_bien_settings()` một mình | **6** | 0 | 1 mục; nạp qua tệp, không `exec` |

Ba số ấy là **đối chứng** cho A1: trên nền `nt`, số spawn phải BẰNG `S_nen` (không phải "nhỏ hơn",
không phải "không tỉ lệ") — vì một phép đo tại MỘT kích thước bảng không phân biệt được "vòng lặp
đã cắt" với "vòng lặp còn nhưng nhỏ" (verdict lượt 1, P2 `mot-diem-spawn-khong-do-duoc-ti-le`:
`130` tại `N=10` có thể là `100 + 3×10`). Kênh 3 chỉ `6` spawn — so "tỉ lệ" thì không thấy, so
"bằng đối chứng" thì thấy.

### `MOI` và `MOI_WINDOWS` hôm nay

`.claude/dev/ci_dang_ky_test.py:40` — `subagent_ghi_detect_test.py` dùng **CÙNG một chuỗi regex**
với `pretooluse_guard_test.py` ở dòng ngay trên (`:39`):

```
r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT"
```

`MOI_WINDOWS` hiện có **1** mục (đo `len(MOI_WINDOWS)` = 1 khi nạp module, 21:07Z 06-09-2026), và đó
là `pretooluse_guard_test.py`. Hai dòng ấy độc lập
theo đúng nghĩa cơ học: `mau_theo_nen(path, mau, la_windows)` tra `MOI_WINDOWS.get(path)` **theo
đường dẫn**, nên thêm một mục cho bộ này **không** đụng mục của bộ kia, và sửa mục của bộ kia
không kéo bộ này theo. Hai mục trùng chuỗi regex là trùng **giá trị**, không phải chung **ô nhớ**.
Nói thẳng vì đọc lướt dễ tưởng ngược lại.

Sau `LO-319` (đi trước packet này), `bang_chung_xanh` đọc **bản ghi TỔNG** theo grammar
`(BỘ CHỌN, GRAMMAR)` khai trong `TONG`/`TONG_WINDOWS` (thiết kế T của `LO-319`; văn xuôi không được
đọc). Dòng Windows mới của bộ này vì thế phải có **grammar riêng** trong `TONG_WINDOWS` — mẫu là dòng
Windows của `pretooluse`: `TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS —
do tren ubuntu-latest` — và **không được** mang cặp `n/m` sau nhãn `DOT BIEN` ngoài dạng `<n> muc`
(grammar không có chỗ cho nó ⇒ sai grammar ⇒ đỏ) — kiểm ở A5.

### Vì sao TÁCH khỏi `MUTANT-WINDOWS-NHANH-DON-DUOC`

`ADR-0044` đo được giá của packet to: `PLAT-M4` = 2 tệp ⇒ **1 vòng, 1 finding**; `PLAT-X4` =
4 tệp ⇒ **3 vòng, 8 finding** (trích ADR; lịch sử review ấy không tái lập ở đây). Gộp hai bộ vào
một packet cho **3 tệp** (`subagent_ghi_detect_test.py` + `nhanh_don_duoc_test.py` +
`ci_dang_ky_test.py`) — đúng trần `sensitive` và trên đường đi tới hình dạng `PLAT-X4`. Tách ra:
mỗi packet **2 tệp**, đúng hình dạng `PLAT-M4`.

Và hai bộ **không cùng một bản vá**: `nhanh_don_duoc_test.py` có sẵn seam
`NHANH_DON_DUOC_KHONG_DOT_BIEN`, in `n/n` chứ không in dòng `DOT BIEN`, và gác đột biến bằng
`rc` chứ bằng dòng bằng chứng — ba khác biệt làm bản vá của nó khác hẳn. Gộp lại là bắt một lượt
review đọc hai thiết kế khác nhau dưới một cái tên.

### Lease đang giữ — đọc trước khi cấp

Đo 17:46Z 06-09-2026:

- `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1:
  mutant-khong-chay-tren-windows-exec-1-claude-20260906` (cấp 14:30:07Z 06-09, hết hạn
  14:30:07Z 07-09, **còn ~20,7 giờ** lúc đo) — trong khi packet #456 **đã land** ở `1b3caa1`.
- `ai-dang-giu .claude/hooks/subagent_ghi_detect_test.py` ⇒ `NGƯỜI_GIỮ 0: không có`.

Đo lại 19:33Z trong bản sao đủ 299 ref: bốn tệp NHÁP `.yaml` của đợt này bị bộ quét tính là lease
thật (`subagent_ghi_detect_test.py` ⇒ `NGƯỜI_GIỮ 1`, chính nháp của packet này). Chữa bằng đuôi
`.yaml.nhap`; đo lại 19:34Z ⇒ `0`. Chi tiết, thủ tục thu hồi bốn bước và giới hạn của nó ở
`ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md` mục *"Lease đang giữ"*.

Chuỗi điều phối: **`#456 → GATE → LO-319 → packet này → 2B`**. Tiền nhiệm trực tiếp là `LO-319`.
Nháp chọn **đường (a)** của `LO-319` mục *"Lease đang giữ"*: cấp SAU khi lease `LO-319` hết hạn
(`lease_expires_at_utc` của CHÍNH lease ấy — không phải `14:30:07Z 07-09` của #456) với
`thay_the_cho: []`, tên tiền nhiệm ghi ở chú thích. Chọn **đường (b)** cấp sớm thì lease này khai
`thay_the_cho: [lo-319-…]`, tệp lease `LO-319` mang `da_bi_thay_the` trỏ ngược **đã commit**, và
**mọi bản** của lease ấy trên mọi ref được xử với readback `ai-dang-giu` — không chỉ một tệp. Hai
cổng khác luật (`check` đếm `any`, không nhìn hạn; `ai-dang-giu` đếm mọi bản, chỉ nhìn hạn — đo
21:02Z 06-09-2026) — chi tiết ở `LO-319`, không chép lại để khỏi trôi.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng THÊM** (cột `additions` của `git diff --numstat`).
Write set là **2 tệp**. Ước dòng thêm: #456 làm cùng việc trên bộ một tốn **`+144/−5`**
(`git show --format= --numstat 0c5e889`, đo lại 20:59Z 06-09-2026: `ci_dang_ky_test.py` **+76/−5**,
`pretooluse_guard_test.py` **+68/−0**; bản trước ghi `+81` là số của `--stat` = thêm CỘNG xoá, sai
đơn vị — verdict lượt 2, P3); bộ này có ba kênh và thêm phản chứng đối chứng của A1 nên ước cao hơn, `~200`,
vẫn dưới `300`. Vượt thì DỪNG trước review, đừng tự khai ngoại lệ.

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
   `timeout-minutes` và cách chia job là packet `GATE-TACH-JOB-CAT-CHI-PHI` (đã land trước).
3. **`.claude/hooks/pretooluse_guard_test.py`** — đã xong ở #456, không mở lại.
4. **Lỗ #319 phía Linux** — packet `LO-319-LINUX-BANG-CHUNG-XANH`, đã land trước. Packet này
   **thừa hưởng** kết quả ấy: `bang_chung_xanh` đọc bản ghi tổng theo grammar (thiết kế T), nên
   dòng Windows mới phải có grammar riêng trong `TONG_WINDOWS` và không được mang cặp `n/m` sau
   nhãn `DOT BIEN`. Kiểm điều đó là A5.
5. **`loi_ruff_ci` trong `ci_dang_ky_test.py`** — của `GATE`, đã land trước; không đụng.
6. **Hai kênh `DOT_BIEN_NHAM_TEST` / `DOT_BIEN_SETTINGS` KHÔNG bị xoá** — chỉ bị cắt khỏi nhánh
   Windows, y hệt kênh chính. Xoá là làm mất phép đo, không phải dời nó.
7. **Không đụng `_git_for_windows_usr_bin` và khối dựng PATH** (dòng 468, 507) — hai chỗ ấy dùng
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

**A1 (M1) — ba kênh thật sự không chạy trên Windows, đo với ĐỐI CHỨNG và tại HAI kích thước.**
Giả lập nền qua vị từ thuần (`ten_nen="nt"` / `"posix"`), bọc `subprocess.Popen` và `builtins.exec`
bằng bộ đếm (rig như phần bối cảnh). **Đếm ở `Popen`, không đếm `run`**: mọi `subprocess.run` đi qua
`Popen`, bọc cả hai là đếm ĐÔI (đo trên `2B` 21:02Z 06-09-2026: `run=136` và `Popen=136` cho cùng
136 tiến trình). Bốn phép đo, qua chính `chay()`:
- `S_nen` = số spawn trên `posix` với **cả ba bảng rỗng** qua seam — chỉ ca nền chạy. Đo lại 21:07Z
  06-09-2026 trên cây này: **438** `Popen`, **0** `exec`, `rc=1`, in `DOT BIEN 0/0 bi giet` — bằng
  đúng số của 33 ca nền gọi trực tiếp (19:35Z), vì bộ này **không có bước dựng fixture ngoài vòng
  lặp** (`chay()` chỉ ghi tệp đột biến vào thư mục tạm, không spawn) — khác `2B`, nơi bảng rỗng vẫn
  trả 5 lời gọi dựng fixture (verdict lượt 2, P2). Đo lại tại lúc thi công; lượt ấy `rc=1`, chỉ lấy
  số spawn;
- `S_nt` = số spawn trên `nt` với ba bảng **đầy đủ**;
- `S_nt_nua` = số spawn trên `nt` với `DOT_BIEN` cắt còn **một nửa** qua seam (11 mục);
- `E_nt` = số lần `exec` bản đột biến trên `nt` (hôm nay trên `posix`: kênh 2 = `6`).
Đòi: **`S_nt == S_nen`** và **`S_nt_nua == S_nt`** và **`E_nt == 0`**, số lần ba hàm runner
(`vòng DOT_BIEN`, `_chay_dot_bien_nham_test`, `_chay_dot_bien_settings`) được gọi trên `nt` = **0**
(đếm qua wrapper), và **tập tên 33 ca nền đã gọi** trên `nt` bằng tập trên `posix`. Kèm đối chứng
chiều ngược: `S_posix` với bảng đầy đủ **>** `S_nen` (`10.045 > 438`, đo 19:35Z — **chưa đo lại lượt
này**, cần vòng đột biến đầy đủ), để chắc rig có nhìn thấy vòng lặp.
Phép làm ĐỎ: bỏ cắt **bất kỳ** kênh nào ⇒ `S_nt > S_nen` (kênh 1: `+≈9.600`; kênh 2: `+10` và
`E_nt = 6`; kênh 3: `+6`). Đơn vị: **số lần sinh tiến trình con (`Popen`)** và **số lần `exec`** —
**không** đo bằng thời gian tường (ba lần đo, ba con số: `101` · `88` · `75` s).

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
**Và một chốt riêng cho `LO-319` (đã land trước):** dòng Windows mới không được chứa cặp `n/m` sau
nhãn `DOT BIEN`. Phép làm ĐỎ: thêm `0/0` sau nhãn ấy trên dòng Windows ⇒ **1** đỏ (vì sau `LO-319`
dòng Windows là một bản ghi tổng có grammar, và grammar ấy không có chỗ cho cặp `n/m` sau nhãn —
`0/0 muc` sai grammar ⇒ đỏ; đo 21:07Z 06-09-2026 trên mục `pretooluse`, ca `win-dong-windows-mang-0/0-sau-nhan`).
Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A6 (M6) — Linux không đổi.**
`python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`, và bản in của
bộ này phải còn nguyên dạng `TONG: CA 33/33 dat · DOT BIEN 22/22 bi giet`. Hai con số `33` và
`22` đo 17:41Z và đo lại 19:30Z 06-09-2026 — **đo lại tại lúc thi công**, đừng chép. Tổng Linux
của `test registry` vì thế **không giảm** ở packet này (nói ra vì một bảng ở `GATE` từng trừ nhầm).
Phép làm ĐỎ: `MOI[path]` bị sửa một ký tự ⇒ ca neo mẫu-nguyên-bản ĐỎ (dựng theo mẫu
`p456-mau-linux-KHONG-DOI-so-voi-base` đã có sẵn cho bộ kia).

**A7 — bằng chứng Windows THẬT, không phải suy luận, tìm BƯỚC theo TÊN trên mọi job.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Vì `GATE-TACH-JOB-CAT-CHI-PHI` đã land trước, bước
`test registry (phạm vi + các bộ chưa được nối)` nằm trong job **`gate-registry (windows-latest)`**
— nhưng tiêu chí neo vào **TÊN BƯỚC**, quét mọi job của lượt, không khoá tên job (nếu GATE chưa
land vì lý do nào đó, bước ấy còn ở `gate (windows-latest)` và tiêu chí vẫn đo được). Đòi: job chứa
bước ấy `conclusion == success`, bước ấy `conclusion == success` với `completed_at` đọc được, **và**
thời lượng bước **nhỏ hơn** thời lượng của cùng bước trong lượt Windows gần nhất chạy trọn TRƯỚC
packet này (đo lại tại lúc thi công; mốc lịch sử để đối chiếu: `17,70` phút, run `34045664423`,
head `426bfc0`, trước cả GATE và LO). Đọc qua `actions_list` + `method: list_workflow_jobs`.
Đơn vị: **phút tường của bước** (`completed_at − started_at` của BƯỚC, không phải của job — thời
lượng bước không phụ thuộc bước ấy nằm trong job nào, nên so được xuyên qua GATE).
Phép làm ĐỎ: thời lượng không giảm ⇒ A7 ĐỎ ⇒ đó là **KẾT QUẢ ĐO** (giả định "Windows đắt gấp ~3"
sai — mà giả định ấy là NỘI SUY, xem `chua_do_duoc` #1), không phải thất bại thiết kế — báo chủ
kho, đừng nới gì để ép nó xanh.

**A8 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **2** đường dẫn.

**A9 — tiền nhiệm không còn giữ TRƯỚC khi bắt tay, đo trên MỌI bản bằng `ai-dang-giu`.** Như
`LO-319` A8, đổi tên mắt xích trước thành `lo-319-linux-bang-chung-xanh-exec-1-claude-20260906`:
`ai-dang-giu .claude/dev/ci_dang_ky_test.py` **và** `ai-dang-giu .claude/hooks/subagent_ghi_detect_test.py`
⇒ `NGƯỜI_GIỮ 1` là lease của packet này, và **0** dòng mang lease của `LO-319` (hay của bất kỳ mắt
xích trước) thiếu `ĐÃ_BỊ_THAY_THẾ`/`HẾT_HẠN`. Đường (a): đo được sau `lease_expires_at_utc` của lease
`LO-319` — **không** phải hạn #456 (verdict lượt 2, P1). Đường (b): sau readback thu hồi mọi bản.
`check rc=0` không thay được phép đo này (`check` không chặn chồng lấn write set — đo 21:02Z
06-09-2026 ở `LO-319`). Hai đường và giới hạn ở `LO-319` mục *"Lease đang giữ"* và `chua_do_duoc` #5,
áp nguyên.

## `hinh_dang_ke_thua`

Chép từ biên nhận và đặc tả của `MUTANT-KHONG-CHAY-TREN-WINDOWS` (#456), cộng phần packet này đo
được. Mỗi dòng ghi thời điểm đo hoặc nguồn trích (L5):

| hình dạng | số lần đã gặp | đo/trích lúc (đọc lại 21:03Z 06-09-2026 trên `b1c2284`) | ghi chú |
|---|---:|---|---|
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức `25`→`45`→`60`) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml` chạy lại 21:03Z 06-09-2026: `9e4f361` (2026-07-09) · `6d88a2c` (2026-08-29 03:29Z) · `7657bfd` (2026-08-29 04:49Z) | #456 đếm mức thành lần; sửa, không nhân lỗi. Packet này không đụng `ci.yml`. |
| tập RỖNG thoả `not song` (`0/0` là bằng chứng) | **3** | trích `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md:137-140` (đọc lại 21:03Z) + `LO-319` A1 đo lại 21:07Z 06-09-2026 | #319 · #456 Windows · Linux (`LO-319`). Nhánh Windows của packet này phải mang chốt tương đương cho **ba** kênh, không phải một. |
| chép bản vá đã chứng minh sang bộ khác mà không đo khác biệt cấu trúc | **0** | tại lúc soạn, 17:50Z 06-09; đọc lại 21:03Z 06-09-2026: vẫn `0`, chưa có biên nhận nào | Packet này là lần ĐẦU kho làm việc ấy. Ba khác biệt đã đo và ghi ở bối cảnh. Bộ đếm này **chỉ tăng bằng biên nhận**: review tìm ra cái thứ tư ⇒ biên nhận ghi `1`, và `2B` chép từ biên nhận ấy — không chép từ dự đoán. |
| số đo trong tài liệu trôi giữa lúc viết và lúc đọc | **≥ 7** | trích `.claude/skills/soan-spec/SKILL.md:56-59` (L5, bốn cặp đợt #250; đọc lại 21:03Z 06-09-2026) + đo ở đây 17:4xZ và 19:30Z | `117/100`→`120/110` · `37`→`39` · `3/90`→`3/100` · `4/120`→`5/121` · `101`s→`88`s→`75`s (hai lần trôi, 17:4xZ và 19:30Z) · `39`s→`33`s. |
| lease không tự chết khi packet đã land | **2** | `#355`: trích `CLAUDE.md` mục *"LEASE KHÔNG TỰ CHẾT KHI PACKET ĐÃ LAND"*, đọc lại 21:03Z; `#456`: đo 17:46Z, đo lại 21:00Z 06-09-2026 (`NGƯỜI_GIỮ 1`, còn ~17,5 giờ) | Xem A9. |
| oracle một điểm cho một đại lượng phụ thuộc kích thước | **1** (bản đầu A1 của chính đặc tả này) | verdict lượt 1 (`VERDICT-luot1.md`, đọc lại 21:03Z); lượt 2 mở thêm mặt "đối chứng trả tiền dựng fixture" (P2), xử ở A1 21:07Z 06-09-2026 | Chữa bằng đối chứng + hai kích thước + đếm ở `Popen`. |

## `chua_do_duoc`

1. **Chi phí của bộ này trên WINDOWS chưa ai đo, và hệ số "gấp ba" là NỘI SUY.** `88 s`/`75 s`
   là Linux. Không có phân rã theo bộ trên `windows-latest` ở bất kỳ lượt nào — `test registry`
   chỉ báo **một** con số cho cả tám bộ (`17,70` phút, run `34045664423`). Tỉ lệ `44,3 / 14,6 ≈
   3,03` của #456 là tỉ lệ **tổng bước** hai nền, không phải của bộ này hay của riêng đột biến;
   bản đầu của lease này viết *"giá gấp ba"* như số đo (verdict lượt 1, P2) — sửa thành nội suy.
   Khoản tiết kiệm packet này mua được là **ước theo tỉ lệ**; A7 là phép đo trả lời. Nợ có tên
   **`CHUA-CO-PHAN-RA-THOI-GIAN-THEO-BO-TREN-WINDOWS`**.
2. **Không có đường đo Windows tại chỗ.** Container Linux. Mọi khẳng định về hành vi Windows đi
   qua CI, và đó là lý do vị từ nền phải là hàm THUẦN nhận `ten_nen` — nếu chỉ đọc `os.name` thật
   thì phản chứng A1/A5 cần máy Windows mới chạy được, tức không ai canh.
3. **Nền của bộ này XANH trong container soạn spec** (`rc=0`, `33/33`, `22/22`, 17:41Z và 19:30Z)
   — khác `pretooluse_guard_test.py` (`rc=1`, 3 ca đỏ sẵn). Đừng suy rằng phiên thi công cũng sẽ
   thấy nền xanh: `CLAUDE.md` đã đo bốn ca rig tự đẻ hồi quy giả; sandbox reviewer lượt 1 thấy
   một mutant sống chỉ vì rig ép `GIT_OPTIONAL_LOCKS=0`. Dựng hai vế **trong MỘT lệnh**.
4. **Kênh `DOT_BIEN_SETTINGS` chỉ có 1 mục.** Một chốt "số dương" trên một tập một phần tử là
   chốt yếu — nó không phân biệt được "có đo" với "đo đúng một thứ". A1 bù bằng đối chứng bằng
   nhau (kênh 3 = `6` spawn, thấy được khi so `S_nt == S_nen`), nhưng chốt số dương thì vẫn yếu.
5. **Mỏ neo lease chưa có giá trị.** `base_sha`/`start_from_sha`/`reviewed_sha_required` chỉ có
   khi `LO-319` integrated; hôm nay không đo được. Lease nháp giữ `1b3caa1` làm chỗ giữ, và
   `check` không phân biệt được chỗ giữ với mỏ neo thật — chủ kho phải đo tay tại lúc cấp.
