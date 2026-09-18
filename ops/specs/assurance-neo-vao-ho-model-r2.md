# ĐẶC TẢ PACKET — `ASSURANCE-NEO-VAO-HO-MODEL` revision 2

| | |
|---|---|
| `packet_id` | `ASSURANCE-NEO-VAO-HO-MODEL` |
| `packet_issue` | **#551** |
| `revision` / `generation` | **2** / 2 |
| `thay_the_cho` | **revision 1** (`sha256 55904f35d3588a64520fb553ac639c83d7c468c349c4bea1a367412972fc7b67`, 9 636 B) — r1 **giữ nguyên trên đĩa** làm hồ sơ |
| `review_class` | **`sensitive`** |
| `base_sha` | **`d705623162b75b7340ee7cca54ac2d2abbddbb6f`** (`origin/master`, đo `07:35Z 18-09-2026`) |
| `executor` | `claude` |
| `reviewer` | `codex`; **fallback `human_audited`** nếu codex chặn |
| `assurance_target` | `cross_approved` |

## `nguon_cap_viec`

Chỉ thị chủ kho, phiên điều phối `18-09-2026`, **nguyên văn**:

> **Cấp Revision 2 cho Packet #551 đi. Review lại bản vá #541 của agy đi. Có các PR nào đã review xanh, có thể merge được**

Mỏ neo bền: bản chiếu chỉ thị trên Issue #551 (điền URL comment khi đăng).

Nợ gốc **`PROTOCOL-CHUA-BIET-ANTIGRAVITY`** không đổi; r2 **không** đổi mục tiêu của packet.

## VÌ SAO PHẢI CÓ REVISION 2 — §3.2, và nó đã được cảnh báo TRƯỚC

`§3.2`: *"Đổi objective, acceptance, **write set**, dependency, executor hoặc environment tạo revision
mới và làm lease cũ mất hiệu lực."* r2 đổi **write set** và **acceptance**. Ba căn cứ, đều **đo được**:

### `Đ1` — `M4` thêm một tệp `docs/**/*.md` ⇒ `r291_docs_ngoai_goi` sẽ ĐỎ

Đây **không** phải phát hiện mới: lease gen 1 đã mang sẵn khối `canh_bao_r291` nói đúng điều này, và
cố ý **không** cấp trước hai đường để xem nó có xảy ra thật không. Nay đo lại trên `d705623`:

```
docs/**/*.md                                   = 74
scripts/tl_selftest.py:21306  len(paths) + 74 == 254
scripts/tl_selftest.py:21309  len(tren_dia) == 74
```

`M4` thêm `docs/adr/0050-…md` ⇒ **74 → 75** ⇒ hai hằng số trên sai ⇒ ca ĐỎ.

**Tiền lệ y hệt, hai lần:** packet #522 phải đi qua **revision 3** vì chuyện này; packet #548 phải đi
qua **revision 2** vì chuyện này. Đây là lần **thứ ba** cùng một hình dạng — xem `hinh_dang_ke_thua`.

### `Đ2` — sửa `tl_selftest.py` kéo theo `RELEASE_MANIFEST.json`

`RELEASE_MANIFEST.json` băm **nội dung** từng tệp, và `scripts/tl_selftest.py` **nằm trong** manifest
(`file_count` đo được: **180**). Sửa nó ⇒ băm lệch ⇒ phải tái sinh manifest. Đường thứ **sáu**.

`CLAUDE.md` nói thẳng vì sao không thể bỏ qua: lane PR **không** bắt được lệch manifest
(`release-verify strict (lane LAND)` có `if: github.ref == 'refs/heads/master'`, còn lane WORKER sinh
manifest **tạm** từ chính cây nên **hấp thụ** mọi thay đổi nội dung) ⇒ **PR xanh, master ĐỎ**.

### `Đ3` — hai tiêu chí của r1 đã TRÔI SỐ, một trong đó nay TỰ MÂU THUẪN

| tiêu chí r1 | r1 viết | đo lại `07:35Z 18-09` | trạng thái |
|---|---|---|---|
| `A7` | *"`adr-song` ⇒ rc=0, và số ADR **49 / 49**"* | nền **49 / 49** | **TỰ MÂU THUẪN** |
| `A3` | *"`124 ĐẠT v2 · … · tổng 177`"* | nền **124 / 177** | còn đúng, nhưng **giòn** |

`A7` hỏng vì: lúc r1 đóng băng nền là **48/48**, nên `49/49` = 48 + ADR-0050 mới. ADR-0049 đã land
theo #548, nền nay là **49/49**, nên sau khi packet thêm ADR-0050 con số đúng phải là **50/50**.
**Đòi `49/49` sau khi thêm một ADR là đòi packet ĐỪNG THÊM ADR** — đúng hình dạng
`TIEU-CHI-THEO-GIA-TRI-TUYET-DOI` đã làm #548 phải đi qua revision 2.

`A3` giòn vì PR #553 (đang mở) thêm một biên nhận ⇒ nền thành `125 / 178`. Số hạng trôi mà **quan hệ
không trôi** — đúng bẫy *"một bất biến còn đúng không chứng minh các số hạng còn đúng"*.

## `write_set` — SÁU đường, liệt kê tường minh

```
docs/PROTOCOL_DA_PHIEN.md
ops/bien_nhan_v2.py
ops/bien_nhan_v2_test.py
docs/adr/0050-assurance-neo-vao-ho-model-khong-phai-hang-cong-cu.md
scripts/tl_selftest.py                  ← MỚI ở r2 (Đ1)
RELEASE_MANIFEST.json                   ← MỚI ở r2 (Đ2)
```

### `ngoai_le_adr_0044`

| | |
|---|---|
| `ai_nang` | `ducthangho` |
| `tran_goc` | **3 tệp** (class `sensitive`) |
| `tran_da_duyet_cho_r1` | **4 tệp** (Q7) |
| `tran_moi` | **6 tệp** |
| `tran_dong_them` | **250 — GIỮ NGUYÊN**, không xin nới |
| `can_cu` | `Đ1` + `Đ2` ở trên |

**Vì sao trần dòng KHÔNG cần nới dù thêm hai tệp:** `M8` là kê khai slot (hai hằng số + một khối chú
thích ≈ 5–8 dòng); `M9` là tái sinh manifest, và diff của nó chỉ là **một băm đổi** (`file_count` giữ
**180** vì không tệp runtime nào được thêm). Nếu đo thật mà vượt 250 ⇒ **DỪNG và xin**, không tự nới.

## `PHAM_VI_TREN_TL_SELFTEST`

| | |
|---|---|
| được phép | **CHỈ** kê khai slot của `r291_docs_ngoai_goi`: `74 → 75` và `254 → 255`, theo đúng **NẾP** của khối chú thích tệp ấy (nêu **đích danh** tệp được thêm) |
| cấm | Sửa bất kỳ ca nào khác, hoặc đổi ngưỡng của ca khác ⇒ **DỪNG, xin riêng** |

## `PHAM_VI_TREN_MANIFEST`

| | |
|---|---|
| được phép | Tái sinh bằng `python3 scripts/tl.py release-manifest` **SAU** khi sửa `tl_selftest.py` |
| cấm | Sửa tay. Và diff của manifest phải **CHỈ** chứa `scripts/tl_selftest.py`; `file_count` phải **GIỮ 180**. Manifest đổi thêm tệp khác là dấu hiệu đã chạm ngoài write set ⇒ **DỪNG** |

## `ngoai_pham_vi` — cố ý KHÔNG làm (không đổi so r1)

| thứ | vì sao |
|---|---|
| Nới `same_provider_approved` cho `sensitive` | §8 có dòng cứng; đó là **bất biến an toàn** (Q10) |
| Đảo `ASSURANCE_CAM_THEO_PROVIDER` sang CHO PHÉP | nợ `DANH-SACH-CAM-THEO-PROVIDER-CHUA-DAO` (Q8) |
| Nối `bien_nhan_v2` vào CI làm cổng chặn | nợ `CONG-BIEN-NHAN-KHONG-CHAY-TRONG-CI` (Q4) |
| Đọc lại verdict đã giao của #546/#538/#540 | luật mới **KHÔNG hồi tố** (Q3) |
| Cho `agy` phát định danh model từng lượt | nợ `AGY-CHUA-ATTEST-MODEL-TUNG-LUOT` |

## `muc_tieu`

`M1`–`M7` **giữ NGUYÊN VĂN r1** (không chép lại ở đây; đọc r1, `sha256 55904f35…`). Hai mục mới:

| # | mục tiêu | chiếu vào |
|---|---|---|
| **M8** | Kê khai slot `r291_docs_ngoai_goi`: `74 → 75` và `254 → 255`, kèm khối `KÊ KHAI SLOT` nêu **đích danh** `docs/adr/0050-…md`, và ghi rằng đây là lần **thứ BA** cùng một cách sập | `scripts/tl_selftest.py` |
| **M9** | Tái sinh `RELEASE_MANIFEST.json`; diff **CHỈ** chứa `scripts/tl_selftest.py`, `file_count` **GIỮ 180** | `RELEASE_MANIFEST.json` |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

`A1`, `A2`, `A4`, `A5`, `A6`, `A8`, `A9`, `A10` **giữ NGUYÊN VĂN r1**. Ba tiêu chí đổi + hai mới:

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **A3** *(nêu lại theo DELTA)* | Chạy `python3 ops/bien_nhan_v2.py --root .` trên **NỀN** (`base_sha`) **và** trên **ỨNG VIÊN**, so **hai** kết quả. Đòi: `0 vi phạm` **và** `0 KHÔNG ĐO ĐƯỢC` ở **cả hai**, `TỔNG: ĐẠT` ở cả hai, và số `ĐẠT v2` / `tổng` **KHÔNG ĐỔI** giữa hai lần | luật mới từ chối một biên nhận cũ ⇒ hai vế lệch ngay |
| **A7** *(nêu lại theo DELTA)* | `python3 .claude/dev/packet_loop.py adr-song --root .` ⇒ **rc=0**, và số ADR = **(nền + 1)**, khớp 1–1 với số dòng §20. **Đo nền NGAY TRƯỚC khi đo ứng viên**, không chép con số | thêm ADR mà quên dòng §20 ⇒ `rc=9`; hoặc lệch 1–1 |
| **A9** *(nêu lại theo trần mới)* | `numstat` vs `base_sha`: **đúng 6 tệp**, **≤ 250 dòng thêm** | tệp thứ bảy, hoặc vượt 250 |
| **A11** *(MỚI — `M8`)* | `docs/**/*.md` = **75**; ca `r291_docs_ngoai_goi` **ĐẠT**; `python3 scripts/tl.py --selftest` ⇒ **N/N, HAI SỐ BẰNG NHAU**, `0 [FAIL]` | quên kê khai slot ⇒ `r291` ĐỎ; đọc `rc` một mình ⇒ không phát hiện |
| **A12** *(MỚI — `M9`)* | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, **`expected_file_count` == `checked_file_count` == 180**, `package_hash_match=true`, `errors=0`. Và diff manifest theo **chỉ mục đường dẫn** chỉ có **một** mục đổi: `scripts/tl_selftest.py`, **0** thêm, **0** bớt | quên tái sinh ⇒ `ok=false`; manifest đổi thêm mục ⇒ đã chạm ngoài write set |

**Chú ý tên khoá của `A12`** — khoá thật trong `release-verify --json` là **`expected_file_count`** và
**`checked_file_count`**, **không** phải `expected`/`checked`. r1 của #548 viết sai tên này và nó thành
một `P3` tự báo (hình dạng `TIEU-CHI-NEU-TRUONG-CHUA-AI-DO`); r2 này viết đúng ngay từ đầu.

### Nền đo tại lúc đóng băng — `07:35Z 18-09-2026`, trên `d705623162b7`

```
bien_nhan_v2 : 124 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 177
adr-song     : sạch — 49 ADR trên đĩa, 49 dòng §20, khớp 1–1
docs/**/*.md : 74
RELEASE_MANIFEST.json file_count : 180
```

**Mọi con số trên là NỀN, không phải tiêu chí.** `A3` và `A7` so **DELTA** với nền đo lại, đúng luật
`L5`. Ai đọc bảng này rồi ghim con số vào tiêu chí là tái tạo đúng `Đ3`.

## `hinh_dang_ke_thua`

| hình dạng | đếm | nguồn |
|---|---:|---|
| `TIEU-CHI-THEO-GIA-TRI-TUYET-DOI` | **3** | #522 (r2→r3) · #548 (`A1`, `A6`) · **#551 `A7` của r1** |
| `R291-DAM-SO-CUNG` | **3** | #522 · #548 · **#551** |
| `TIEU-CHI-NEU-TRUONG-CHUA-AI-DO` | **1** | #548 `A7` của r2 |

**Cả hai hình dạng đầu nay ở mức BA.** Chốt *"lặp lần thứ BA ⇒ DỪNG, hỏi **có nên làm việc này
không**, không hỏi **vá thế nào**"* **ĐÃ CHẠM TRẦN**. Đặc tả này khai thẳng điều đó thay vì lặng lẽ
vá lần thứ ba:

> **Câu hỏi đúng lúc này không phải *"kê khai slot thế nào"* mà là *"có nên để `r291` đấm số cứng
> nữa không"*.** Ba packet liên tiếp phải mở rộng write set chỉ vì một hằng số trong
> `scripts/tl_selftest.py`. Nợ `R291-DAM-SO-CUNG` **không** đóng ở packet này (nó ngoài phạm vi), nhưng
> phải được **khai lại** và nêu thành đề xuất packet riêng. Chủ kho quyết; r2 này chọn vá lần thứ ba
> **có khai**, không phải vá lặng.

## `chua_do_duoc` — ghi thẳng

| # | thứ | vì sao |
|---|---|---|
| **C1** | Packet có gỡ được trần cho #546 không | **KHÔNG BIẾT, nghiêng về KHÔNG** — giữ nguyên văn r1 |
| **C2** | Model nào agy đã chạy ở #546/#538/#540 | không có bằng chứng máy; `_do_antigravity` chỉ đếm model KHẢ DỤNG |
| **C3** | Có biên nhận cũ nào bị luật mới từ chối không | `A3` là phép đo **tổng**, không nói trước biên nhận nào |
| **C4** | Codex có chạy được lượt review không | `doctor` đo `07:18Z 18-09`: codex **`SAP_HET_HAN`** (ảnh chụp cũ 207,6h). Chặn ⇒ `human_audited` với chủ kho là người audit, **phải khai**, không làm tròn |
| **C5** | Ngưỡng ≤ 250 dòng thêm có đủ không | ước lượng r1, nay cộng `M8`+`M9` ≈ 5–10 dòng. Vượt ⇒ **DỪNG và xin lại** |
| **C6** *(mới)* | `M8` có phải lần cuối phải kê khai slot không | **KHÔNG BIẾT** — phụ thuộc nợ `R291-DAM-SO-CUNG` có được xử không |

## Băm để lease neo vào

```
sha256sum ops/specs/assurance-neo-vao-ho-model-r2.md
```
