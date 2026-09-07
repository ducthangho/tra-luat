# Đặc tả packet — MUTANT-WINDOWS-NHANH-DON-DUOC

- `packet_id`: **MUTANT-WINDOWS-NHANH-DON-DUOC** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được ngay khi có số Issue — tiền lệ #456)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp;** khuyến nghị chung cho bốn packet ở
  `GATE-TACH-JOB-CAT-CHI-PHI.md`**)**
- `revision`: 1 · `generation`: 1 — giữ 1 có chủ ý (nháp thứ ba của revision 1, chưa có Issue nên
  chưa đóng băng; lý do đầy đủ và quy ước `lease_id …-exec-1rN-…` đo được ở `LO-319` dòng `revision`)
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (chạm chốt bằng chứng dương của một cổng CI;
  không rõ ⇒ lấy mức chặt nhất)
- `depends_on`: **`GATE-TACH-JOB-CAT-CHI-PHI`**, **`LO-319-LINUX-BANG-CHUNG-XANH`**,
  **`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`** — cả bốn cùng chạm `.claude/dev/ci_dang_ky_test.py` ⇒
  write-set exclusion buộc nối tiếp; packet này đi **THỨ TƯ**, cuối chuỗi.
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`) — **chỗ giữ,
  không phải mỏ neo.** Ba mỏ neo trong lease (`base_sha` · `start_from_sha` ·
  `reviewed_sha_required`) phải cùng bằng head `origin/master` **SAU khi
  `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT` đã integrated** (`§5`), đo tại lúc cấp. Quy tắc này nằm trong
  đặc tả đóng băng, không chỉ trong chú thích YAML.

## `nguon_cap_viec`

Packet **kế nhiệm**. Nguồn: `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #2
— bộ thứ hai trong hai bộ được để dành ở đó.

Tiền nhiệm trực tiếp: `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT` (bộ thứ nhất của cặp ấy). Packet này
phải đọc **biên nhận** của packet đó trước khi bắt tay: nó là chỗ ghi những khác biệt cấu trúc mà
lượt review tìm thêm được, và là nguồn DUY NHẤT cho bộ đếm kế thừa ở `hinh_dang_ke_thua`.

Bản này là **bản sửa theo verdict cross-review lượt 2** (`reviewed_sha` `b1c2284`, Codex), sau lượt 1
(`d09f2f1`): đối chứng A1 đổi từ "`main()` bảng rỗng" sang `chay_ca()` (P2
`mot-diem-spawn-khong-do-duoc-ti-le`), thu hồi lease theo P1, M4 đồng bộ "địa điểm thứ tư" (P3), và
mọi câu về `LO-319` theo thiết kế T (bản ghi TỔNG).

## Bối cảnh đo được (mọi số kèm thời điểm)

### Chi phí — đo lại, không chép

Đo 17:39–17:47Z 06-09-2026, container Linux, **một lượt, không lặp**:

| | ĐẦY ĐỦ | NỀN-ONLY | đột biến | phần đột biến |
|---|---:|---:|---:|---:|
| `ops/nhanh_don_duoc_test.py` | **33 s** | **2 s** | 31 s | **93,9 %** |

`#456` đo bộ này **39 s** cùng ngày; 17:47Z **33 s**; chạy lại 19:31Z **34 s** (`rc=0`). Không số
nào sai lúc nó được đo — đây là lý do `L5` đòi đo lại trước mỗi bước công bố. Đơn vị: **giây tường
của một lượt `python ops/nhanh_don_duoc_test.py`**.

Phần bộ này chiếm trong bước `test registry`: **33 / 400 giây = 8,3 %** (tổng 400 s đo cùng lúc
17:47Z, tám bộ; `8,25 %` làm tròn một chữ số). Đây là bộ **rẻ nhất trong ba bộ** mang vòng lặp đột
biến — nói thẳng vì nó quyết định thứ tự: packet này đi SAU, không đi trước.

### Bảng đột biến, và số lần sinh tiến trình con — nền đối chứng cho A1

Đo 17:50Z 06-09-2026 (đo lại 19:35Z, không đổi): `CA` = **8** mục · `DOT_BIEN` = **10** mục. Một
kênh đột biến (khác `subagent_ghi_detect_test.py` với ba kênh).

Đo 19:35Z, nạp module thật, bọc `subprocess.run` và `subprocess.Popen` bằng bộ đếm, không sửa tệp.
Đơn vị: **số lần sinh tiến trình con** (`run` + `Popen` gọi trực tiếp):

| pha | `subprocess.run` | `Popen` trực tiếp | tổng spawn | ghi chú |
|---|---:|---:|---:|---|
| `chay_ca()` — 8 ca nền | **136** | 0 | **136** | `S_nen`; ca nền tự gọi `git` qua `run` |
| `chay_dot_bien()` — 10 mutant | 25 | 10 | **35** | = 5 (`git init/config×2/add/commit`) + 10 × (`git archive` Popen + `tar` + `python` con) |

`35` là `5 + 3·N` với `N = 10`. Đây là số phụ thuộc `N`, và một phép đo tại một `N` không phân biệt
được "đã cắt" với "còn nhưng nhỏ" (verdict lượt 1, P2) — nên A1 so **bằng đối chứng** và **tại hai
kích thước**.

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

**Giống nhau từng byte tại ĐIỂM QUAN SÁT của sổ đăng ký.** Toàn bộ stdout thì KHÁC (reviewer đo:
lượt đầy đủ có thêm 10 dòng `MUTANT`), nhưng sổ đăng ký chỉ nhìn dòng `8/8`. Một lượt đo 10 đột
biến và một lượt đo 0 đột biến cho **cùng một bằng chứng** ở chỗ duy nhất có ai đọc. Đó đúng là
hình dạng *"cổng không nói dối, nó VẮNG MẶT"* — và ở đây cái vắng mặt còn ký tên vào chỗ của cái
có mặt.

### Lỗ thứ hai, có sẵn từ trước, cùng họ #319 — và bằng chứng nào ĐÃ được in

Cùng đoạn mã: `return 0 if mutant_dat == len(DOT_BIEN) else 1`. Nếu `DOT_BIEN` **rỗng** thì
`0 == 0` ⇒ `rc = 0` ⇒ bộ ĐẠT. Bảng đột biến rỗng thoả điều kiện, y hệt `DOT BIEN 0/0 bi giet`.
Reviewer tái hiện 18:50Z trên bản sao: đặt bảng rỗng, giữ tám ca thật ⇒ `8/8`, `rc=0`.

**Nói cho đúng thứ đã in và thứ chưa in** (bản đầu viết *"số đột biến của bộ này chưa bao giờ được
in ra dưới dạng cặp"* — sai một nửa, verdict lượt 1 P2 `bang-chung-da-in-bi-khai-la-chua-ton-tai`):

- Lượt đầy đủ **ĐÃ in 10 dòng `MUTANT <tên> | <ca đích> | n/m`** (đo 19:31Z: 10 dòng; **8** dòng
  `1/1`, **2** dòng `3/3`). Cặp `n/m` ở mỗi dòng là **số ca ĐÍCH bị giết / số ca đích của mutant
  ấy** — một mutant SỐNG in `0/3`, không phải vắng dòng. Đơn vị là ca đích, không phải mutant.
- Thứ **chưa** in là cặp TỔNG `mutant_dat / len(DOT_BIEN)` (hôm nay `10/10`).
- `MOI` (`^(\d+)/(\d+)$`, span 3 ký tự) chỉ khớp dòng `8/8`, nên `LO-319` — đọc bản ghi TỔNG theo
  grammar, mà bản ghi tổng hôm nay của bộ này là đúng dòng `8/8` — không nhìn thấy các dòng `MUTANT`. Đó là lý do LO không chữa được lỗ này, **không phải**
  vì bằng chứng không tồn tại.

Hai cách chữa, cả hai đo được:
- **(i) siết `MOI` để đọc các dòng `MUTANT` sẵn có.** Reviewer thử mẫu
  `(?s)MUTANT [^\n]+ \| \d+/\d+\n.*^\d+/\d+$` trên hai stdout thật: đầy đủ ⇒ `True`, bảng rỗng ⇒
  `False`. Đủ để phân biệt hai lượt hôm nay. Nhưng nó chỉ đòi **có ít nhất một** dòng `MUTANT`, không
  đòi tổng; một bảng còn một mục cũng qua, và một mutant sống (`0/3`) cũng qua trừ khi mẫu soi từng
  dòng.
- **(ii) in cặp TỔNG có nhãn** — `DOT BIEN <mutant_dat>/<len(DOT_BIEN)> bi giet` trên Linux —
  rồi siết `MOI` đòi dòng ấy. Sau `LO-319`, dòng ấy được khai là một **bản ghi tổng** trong `TONG`
  của mục này (đổi từ `[(r"\d+/\d+\s*$", r"(\d+)/(\d+)")]` sang bản ghi có nhãn, M5) ⇒ `0/0` và
  `9/10` bị từ chối ở TẦNG SỔ ĐĂNG KÝ theo luật cặp `n == m > 0` của T — cần khai grammar mới cho
  mục này, không cần vị từ riêng.

**Chọn (ii)**, vì nó đưa bộ này về cùng hình dạng bằng chứng với hai bộ kia (một dòng tổng có
nhãn) và tận dụng chốt `LO-319` thay vì dựng một mẫu span dài riêng. (i) không sai; nó chỉ là một
chốt yếu hơn trên một bằng chứng có thật. Câu đúng về phạm vi packet: **không chỉ cắt đột biến
khỏi Windows; còn phải làm bằng chứng đột biến của bộ này ĐỌC ĐƯỢC ở tầng sổ đăng ký trên cả hai
nền** — "đọc được", không phải "tồn tại".

### `MOI` hôm nay

`.claude/dev/ci_dang_ky_test.py:41` — `"ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$"`. Hai nhóm,
span **3 ký tự = 3 byte** (đo 19:32Z), một cặp (`8/8`). Đây là mẫu chặt nhất trong cả `MOI` về span
và lỏng nhất về nội dung: nó không đòi một chữ nào ngoài hai con số.

### Lease đang giữ

Đo 17:46Z 06-09-2026:

- `ai-dang-giu ops/nhanh_don_duoc_test.py` ⇒ `NGƯỜI_GIỮ 0: không có`.
- `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1:
  mutant-khong-chay-tren-windows-exec-1-claude-20260906` (còn ~20,7 giờ lúc đo, packet đã land).

Đo lại 19:33Z trong bản sao đủ 299 ref: nháp `.yaml` của chính packet này bị đếm
(`nhanh_don_duoc_test.py` ⇒ `NGƯỜI_GIỮ 1`); đổi đuôi `.yaml.nhap` ⇒ `0` (19:34Z). Chi tiết và thủ
tục thu hồi ở `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md` mục *"Lease đang giữ"*.

Chuỗi điều phối: **`#456 → GATE → LO-319 → 2A → packet này`** (mắt cuối). Tiền nhiệm trực tiếp là
`2A`. Nháp chọn **đường (a)** của `LO-319` mục *"Lease đang giữ"*: cấp SAU khi lease `2A` hết hạn
(`lease_expires_at_utc` của CHÍNH lease ấy — không phải hạn #456) với `thay_the_cho: []`, tên tiền
nhiệm ghi ở chú thích. Chọn **đường (b)** cấp sớm thì lease này khai
`thay_the_cho: [mutant-windows-subagent-ghi-detect-…]`, tệp lease `2A` mang `da_bi_thay_the` trỏ
ngược **đã commit**, và **mọi bản** trên mọi ref được xử với readback `ai-dang-giu`. Hai cổng khác
luật (`check` đếm `any`, không nhìn hạn; `ai-dang-giu` đếm mọi bản, chỉ nhìn hạn — đo 21:02Z
06-09-2026) — chi tiết ở `LO-319`, không chép lại.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng THÊM** (cột `additions`). Write set là **2 tệp**
— đúng hình dạng `PLAT-M4` (2 tệp ⇒ 1 vòng, 1 finding, trích ADR). Ước dòng thêm `~150` (một kênh,
cộng phản chứng A1 có đối chứng); đo thật trước review.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `ops/nhanh_don_duoc_test.py` | nơi vòng lặp đột biến chạy, nơi `rc` được quyết, và nơi cặp tổng đột biến chưa được in |
| 2 | `.claude/dev/ci_dang_ky_test.py` | nơi mẫu bằng chứng dương của bộ ấy được khai (`MOI`, `MOI_WINDOWS`) |

Không ký tự đại diện. Không đường dẫn nào khác.

## `ngoai_pham_vi`

1. **`ops/nhanh_don_duoc.py`** (mã sản xuất) — không đụng. Packet này sửa cách bộ TEST tự khai
   bằng chứng, không sửa thứ nó đo.
2. **`.github/workflows/ci.yml`** — packet `GATE-TACH-JOB-CAT-CHI-PHI`, đã land trước.
3. **Hai bộ kia** — đã xong ở #456 và `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`.
4. **`loi_ruff_ci` và `bang_chung_xanh` trong `ci_dang_ky_test.py`** — của `GATE` và `LO-319`, đã
   land trước; packet này chỉ đụng hai mục của `MOI`/`MOI_WINDOWS` cho bộ này và phản chứng.
5. **Không XOÁ seam `NHANH_DON_DUOC_KHONG_DOT_BIEN`.** Nó là đường mà chính runner đột biến dùng
   để chạy bản con mà không đệ quy (`ops/nhanh_don_duoc_test.py:208`). Xoá là làm hỏng vòng lặp
   đột biến. Việc phải làm là **tách hai câu hỏi** — *"đang chạy bản con"* khác *"đang trên
   Windows"* — chứ không phải bỏ biến.
6. **Không đổi bộ ca `CA` hay bảng `DOT_BIEN`.** Bộ này đo `nhanh_don_duoc.py`; packet này không
   có ý kiến gì về việc ấy.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Trên Windows, vòng lặp đột biến KHÔNG chạy. Tám ca nền vẫn chạy đủ. | `write_set` #1 |
| M2 | Bộ in **cặp TỔNG đột biến có nhãn** ra bản in trên **cả hai** nền — Linux `DOT BIEN <đã giết>/<tổng> bi giet`, Windows `DOT BIEN <tổng> muc KHONG DO TREN WINDOWS — do tren ubuntu-latest`. Hôm nay không nền nào in cặp tổng; các dòng `MUTANT` theo mutant giữ nguyên. | `write_set` #1 |
| M3 | Seam `NHANH_DON_DUOC_KHONG_DOT_BIEN` (bản con của runner) và vị từ nền Windows là **hai đường tách biệt**: bản con vẫn in dạng riêng, không mượn dòng Windows. | `write_set` #1 |
| M4 | Bảng đột biến RỖNG ⇒ `rc != 0` trên **mọi** nền — chốt tương đương `len(DOT_BIEN) > 0`, lấp lỗ #319 tại **địa điểm thứ tư** của bảng `hinh_dang_ke_thua` (đơn vị: địa điểm/ca tái hiện, gồm ca tổng hợp — chưa phải sự cố sản xuất, `chua_do_duoc` #4). | `write_set` #1 |
| M5 | Sổ đăng ký đòi cặp tổng ấy: mẫu Linux siết để nhìn thấy dòng có nhãn `DOT BIEN`; `MOI_WINDOWS` nhận dòng Windows **chỉ** khi nền là Windows. | `write_set` #2 |
| M6 | Trên Linux, số ca và số đột biến không đổi: `8` ca, `10` đột biến, `rc=0`. | `write_set` #1, #2 |

## `nghiem_thu`

**A1 (M1) — đột biến thật sự không chạy trên Windows, đo với ĐỐI CHỨNG và tại HAI kích thước.**
Giả lập nền qua vị từ THUẦN (`ten_nen="nt"` / `"posix"`), bọc `subprocess.Popen` bằng bộ đếm — **đếm
ở `Popen`, mỗi tiến trình một lần**: `run` gọi `Popen` bên trong, bọc cả hai là đếm ĐÔI (đo 21:02Z
06-09-2026: `chay_ca()` cho `run=136` VÀ `Popen=136` cho cùng 136 tiến trình). Bốn phép đo, qua chính
`main()` (hoặc hàm tương đương nhận vị từ nền):
- `S_ca` = spawn của **riêng `chay_ca()`** trên `posix` — hôm nay **136** (đo 21:02Z, 8 ca xanh,
  2,9 s; đo lại tại lúc thi công). **Đây là đối chứng — không phải "`main()` với bảng rỗng"**:
  `chay_dot_bien` dựng fixture bằng **5** lời gọi `run` (`git init` · `config` ×2 · `add` · `commit`)
  TRƯỚC khi duyệt bảng (đo 21:07Z qua seam `run` trơ với `DOT_BIEN=[]` ⇒ đúng 5 lời gọi, 0 tiến
  trình thật), nên `main()` bảng rỗng trên `posix` là `S_ca + 5` = `141`, và tiêu chí
  `S_nt == S_nen(bảng rỗng)` của bản trước sẽ **bác một triển khai đúng** (verdict lượt 2, P2). M4 còn
  làm lượt bảng rỗng `rc != 0` — không dùng nó làm nền;
- `S_nt` = spawn của `main()` trên `nt` với bảng **đầy đủ** (10 mục);
- `S_nt_nua` = spawn của `main()` trên `nt` với bảng cắt còn **5** mục qua seam;
- `S_posix` = spawn của `main()` trên `posix` với bảng đầy đủ (`136 + 35 = 171`, đo 19:35Z — **chưa
  đo lại lượt này**, cần vòng đột biến ~34 s).
Đòi: **`S_nt == S_ca`** — tức nhánh `nt` không trả một spawn nào cho fixture đột biến; `chay_dot_bien`
không được gọi (đếm qua wrapper = **0**) — và **`S_nt_nua == S_nt`**, tập tên 8 ca nền trên `nt` bằng
trên `posix`, và đối chứng `S_posix − S_ca == 5 + 3·len(DOT_BIEN)` (hôm nay `35`) để chắc rig thấy
vòng lặp.
Phép làm ĐỎ: bỏ cắt ⇒ `S_nt = S_ca + 35` ⇒ ĐỎ; cắt "một nửa" (chỉ bỏ `python` con, còn
`archive|tar`) ⇒ `S_nt = S_ca + 25` ⇒ vẫn ĐỎ; cắt vòng lặp nhưng vẫn dựng fixture ⇒ `S_nt = S_ca + 5`
⇒ vẫn ĐỎ — so BẰNG mới bắt được ba ca này, so "tỉ lệ" thì không. Đơn vị: **số lần sinh tiến trình
con (`Popen`)**. Không đo bằng thời gian tường.

**A2 (M2) — cặp TỔNG đột biến TỒN TẠI ở bản in, cả hai nền.**
Phép làm ĐỎ, hai chiều:
- lượt Linux đầy đủ mà bản in **không** chứa `DOT BIEN 10/10 bi giet` (số đo lại tại lúc thi
  công) ⇒ ĐỎ;
- lượt Windows mà bản in **không** khai `DOT BIEN 10 muc KHONG DO TREN WINDOWS — do tren
  ubuntu-latest` ⇒ ĐỎ.
Đột biến bắt buộc: làm nhánh Windows in **dòng của Linux** ⇒ ca đích ĐỎ.
**Đây là tiêu chí phân biệt được hai lượt mà hôm nay giống nhau từng byte tại điểm quan sát**
(`8/8`, `rc=0`) — nếu sau bản vá lượt đầy đủ và lượt seam vẫn cho cùng một bản in **tại điểm sổ
đăng ký nhìn**, A2 ĐỎ bất kể mọi thứ khác xanh. Mười dòng `MUTANT` sẵn có **không** bị bỏ.

**A3 (M3) — bản con của runner KHÔNG mượn được đường Windows.**
Phép làm ĐỎ: chạy với `NHANH_DON_DUOC_KHONG_DOT_BIEN=1` trên nền **không** phải Windows ⇒ bản in
phải KHÁC dòng Windows **và** khác dòng Linux đầy đủ. Đột biến bắt buộc: nối hai đường thành một
điều kiện `or` ⇒ ca này phải ĐỎ.
Vì sao cần: nếu bản con in dòng Windows thì mỗi lượt đột biến trên Linux cũng "khai không đo ở
đây", và runner đột biến sẽ đọc nhầm chính bản con của mình.

**A4 (M4) — bảng đột biến rỗng làm bộ ĐỎ.**
Phép làm ĐỎ: đột biến `DOT_BIEN = []` (trên BẢN SAO tạm, không đụng tệp thật — bài học "đột biến
ghi vào tệp THẬT rồi khôi phục trong `finally` là bom hẹn giờ") ⇒ `rc` phải khác 0 trên cả nền
Linux lẫn nền `nt` giả lập. Hôm nay đột biến ấy cho `rc = 0` (reviewer tái hiện 18:50Z).
Đơn vị: **mã thoát của tiến trình**.

**A5 (M5) — sổ đăng ký đòi cặp tổng, và phân biệt được nền.**
Phép làm ĐỎ, đi qua chính `chay_moi` với năm seam:
- dòng Linux **thiếu** cặp tổng ⇒ **1** đỏ (hôm nay: 0 — mẫu `^(\d+)/(\d+)$` không đòi gì);
- `DOT BIEN 0/0 bi giet` trên nền Linux ⇒ **1** đỏ (sau `LO-319`, chốt nhãn bắt; ca này canh
  rằng mẫu mới KHÔNG vô hiệu hoá chốt ấy);
- dòng Windows trên nền Linux ⇒ **1** đỏ;
- dòng Windows trên nền Windows ⇒ **0** đỏ;
- dòng Linux đầy đủ trên nền Windows ⇒ **0** đỏ.

Đơn vị: **số mục bị `chay_moi` đếm là ĐỎ**.

**A6 (M6) — Linux không đổi về SỐ LƯỢNG đo được.**
`python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`; bản in phải
khai `8` ca và `10` đột biến. Hai con số đo 17:50Z và đo lại 19:35Z 06-09-2026 — **đo lại tại lúc
thi công**. Nói rõ: bản in **có đổi** (M2 đòi thế). Thứ không được đổi là **số ca chạy** và **số
đột biến chạy** trên Linux — và vì thế tổng Linux của `test registry` **không giảm** ở packet này.
Đây là khác biệt so với M4 của #456, và nó là khác biệt CÓ CHỦ Ý — mẫu cũ của bộ này không có gì
đáng đóng băng, nó đang đóng băng một chỗ mù.

**A7 — bằng chứng Windows THẬT, tìm BƯỚC theo TÊN trên mọi job.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Bước `test registry (phạm vi + các bộ chưa được
nối)` sau `GATE` nằm trong job **`gate-registry (windows-latest)`**; tiêu chí neo vào TÊN BƯỚC,
quét mọi job. Đòi: job chứa bước `success`, bước `success` với `completed_at` đọc được, và thời
lượng bước **nhỏ hơn** thời lượng cùng bước ở lượt Windows gần nhất chạy trọn **sau** `2A` và
**trước** packet này (đo lại tại lúc thi công). `17,70` phút (run `34045664423`) là số của trước cả
bốn packet — không dùng làm mốc cho packet này.
Đơn vị: **phút tường của bước** (`completed_at − started_at` của BƯỚC, không phải job).

**A8 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **2** đường dẫn.

**A9 — tiền nhiệm không còn giữ TRƯỚC khi bắt tay, đo trên MỌI bản bằng `ai-dang-giu`** — như `2A`
A9, đổi tên mắt xích trước thành `mutant-windows-subagent-ghi-detect-exec-1-claude-20260906`, đo
trên **cả hai** đường write set. Đường (a): sau `lease_expires_at_utc` của lease `2A` — không phải
hạn #456; đường (b): sau readback thu hồi mọi bản. `check rc=0` không thay được phép đo này.

## `hinh_dang_ke_thua`

Mỗi dòng ghi thời điểm đo hoặc nguồn trích (L5):

| hình dạng | số lần đã gặp | đo/trích lúc (đọc lại 21:03Z 06-09-2026 trên `b1c2284`) | ghi chú |
|---|---:|---|---|
| tập RỖNG thoả `not song` | **4** (đơn vị: địa điểm/ca tái hiện, gồm ca tổng hợp) | trích `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md:137-140` + `LO-319` (đọc lại 21:03Z); địa điểm thứ tư đo 18:50Z 06-09 (reviewer, `nhanh-probes.json` lượt 1, không chạy lại lượt này) | #319 (gốc) · #456 Windows · `LO-319` Linux · **bộ này** (`mutant_dat == len(DOT_BIEN)` với bảng rỗng). Lần thứ tư. `PROTOCOL §12` đòi xem lại CÁCH LÀM từ lần thứ ba — câu trả lời của kho là: **chốt số dương phải nằm ở vị từ `dat`, không nằm ở mẫu regex**, vì mẫu chỉ soi được thứ đã in. |
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức `25`→`45`→`60`) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml` chạy lại 21:03Z 06-09-2026: `9e4f361` · `6d88a2c` (2026-08-29 03:29Z) · `7657bfd` (04:49Z) | Không đụng `ci.yml`. |
| hai lượt khác nhau cho cùng một bằng chứng | **2** | PR #100: trích `CLAUDE.md` mục dấu bỏ-qua-CI, đọc lại 21:03Z (sự kiện GitHub không readback lại); bộ này: đo 17:47Z 06-09 (hai lượt thật), đọc lại bản in `rc=0` lượt 1 lúc 21:00Z | dấu bỏ-qua-CI làm PR #100 có 0 check mà `mergeable_state: clean` · bộ này: 10 đột biến và 0 đột biến cùng in `8/8` rc=0 tại điểm quan sát. Cùng gốc: **cổng vắng mặt trông giống cổng xanh**. |
| chép bản vá đã chứng minh sang bộ khác mà không đo khác biệt cấu trúc | **0** | tại lúc soạn, 17:50Z 06-09 — cùng số với `2A`; đọc lại cả hai bảng 21:03Z 06-09-2026: vẫn `0`, chưa có biên nhận | Bản đầu ghi `1 (từ 2A)` trong khi `2A` đang ghi `0` và chưa có biên nhận nào — số tự tạo, vi phạm L4 (verdict lượt 1, P2). Giá trị ĐÚNG phải **chép từ biên nhận của `2A`** khi có; cho tới lúc đó là `0`, và bộ này khác `2A` bốn chỗ (một kênh, seam env sẵn, không in dòng `DOT BIEN`, gác bằng `rc`) là lý do bộ đếm ấy có thể tăng — nhưng tăng ở biên nhận, không ở đây. |
| số đo trong tài liệu trôi | **≥ 7** | trích `.claude/skills/soan-spec/SKILL.md:56-59` (đọc lại 21:03Z 06-09-2026) + đo ở đây 17:47Z và 19:31Z | `39`s→`33`s→`34`s là cái mới nhất, do chính packet này đo ba lần; bốn cặp #250 và hai lần trôi của `2A` cộng vào là `≥ 7`. |
| lease không tự chết khi packet đã land | **2** | `#355`: trích `CLAUDE.md`, đọc lại 21:03Z; `#456`: đo 17:46Z, đo lại 21:00Z 06-09-2026 (`NGƯỜI_GIỮ 1`) | Xem A9. |
| lời khai rộng hơn phép đo — "chưa bao giờ được in" | **1** (bản đầu của chính đặc tả này) | verdict lượt 1, đo lại 19:31Z; đọc lại bản in lượt 1 lúc 21:00Z 06-09-2026: 10 dòng `MUTANT` | Đã in 10 dòng `MUTANT`; chưa in cặp tổng. |
| đối chứng trả tiền cho thứ nó không đo (bảng rỗng vẫn dựng fixture) | **1** (bản lượt 1 A1 của chính đặc tả này) | verdict lượt 2; đo lại 21:07Z 06-09-2026: 5 lời gọi | Chữa: đối chứng là `chay_ca()`, đếm ở `Popen`. |

## `chua_do_duoc`

1. **Chi phí bộ này trên Windows chưa ai đo** — cùng nợ
   `CHUA-CO-PHAN-RA-THOI-GIAN-THEO-BO-TREN-WINDOWS`. `33`/`34 s` là Linux; `test registry` chỉ báo
   một con số cho cả tám bộ. Hệ số "gấp ba" là nội suy (xem `2A` `chua_do_duoc` #1) — và nội suy
   ấy nay **đo được là SAI theo cả hai chiều**: trên 9 lượt master (00:47Z 07-09-2026) tỉ lệ
   Windows/ubuntu **cùng bước, cùng head** trải `1,07×` – `9,74×`, job trọn `gate` trung vị
   `1,68×`, `test registry` trung vị `1,21×`. Bảng đủ ở `GATE-TACH-JOB-CAT-CHI-PHI` mục *"Hệ số nền
   KHÔNG phải một con số"*. Nợ VẪN MỞ: không bước nào đo được là một vòng đột biến, nên đó là
   **proxy**, không phải phép đo thay. `A7` vẫn là phép đo trả lời.
2. **Bộ này spawn `git archive` + `tar` cho mỗi đột biến.** `tar` có trên `windows-latest` nhưng
   hành vi ống (`Popen ... | tar -x`) trên Windows **chưa từng được đo riêng** — nó luôn nằm
   trong con số gộp của `test registry`. Nếu chi phí Windows của bộ này thấp hơn ước, khoản tiết
   kiệm của packet này nhỏ hơn ước, và A7 sẽ nói ra.
3. **Không có đường đo Windows tại chỗ** (container Linux).
4. **Lỗ "bảng đột biến rỗng" ở M4 chưa từng biểu hiện thật.** Nó là lỗ đo được bằng đột biến, chưa
   phải sự cố đã xảy ra. Ghi đúng như vậy: đây là chốt phòng ngừa, không phải bản vá sau tai nạn —
   khác với #319, vốn sinh ra từ một ca thật.
5. **Mỏ neo lease chưa có giá trị** — chỉ có khi `2A` integrated; như `2A` `chua_do_duoc` #5.
6. **Bộ đếm "chép bản vá…" chờ biên nhận `2A`.** Không có cách đọc trước; ghi `0` là ghi số đo
   hôm nay, không phải dự đoán.
