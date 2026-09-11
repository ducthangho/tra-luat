# Đặc tả packet — CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN (revision 2)

- `packet_id`: **CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được khi có số Issue — tiền lệ `#456`/`#463` giữ bí danh ở `packet_id`,
  số ở `packet_issue`)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi. Packet này sinh ra từ một sự cố đo được
  chứ không từ một lane kế hoạch, nên chưa có mission nào ôm nó. Khuyến nghị: gắn vào cùng mission
  với `#463` nếu chủ kho mở một mission chung cho lane CI.
- `revision`: **2** · `generation`: 1 — **revision 2** vá cross-review khác nền lượt 1 (`codex`,
  `reviewed_sha` `4918d5f`, `changes_requested`, VERDICT `sha256 29ee0caa…`): 3 P1 + 3 P2 + 1 P3
  thuộc đặc tả này. Đổi lớn nhất: `M1` từ **16** `assert` xuống **14** (hai cái còn lại là HẠ TẦNG,
  giữ nguyên) · `M6` + `A5b` MỚI cho **kênh kết quả** (lớp ngoại lệ KHÔNG qua được ranh giới tiến
  trình) · `M4`/`A5` phủ **cả hai** kho · `hinh_dang_ke_thua` **tách hai chiều** và **rút** lời
  kích hoạt `§12`. Lịch sử: revision 1
- Thời điểm soạn: **06:45Z 11-09-2026**. Mọi con số dưới đây ghi kèm thời điểm đo (`L5`).

---

## Vấn đề — mức chứng cứ khai theo TỪNG LOẠI, không gộp

**Ba mức, và mục này trộn chúng nếu không nói rõ** (cross-review lượt 1, P2
`so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec`):

- **ĐO LẠI ĐƯỢC** — đọc từ cây kho tại một SHA: số dòng, vị trí dòng, `sha256`, cấu trúc YAML, số
  ca, số biên nhận. Ai cũng tái lập được offline.
- **THUẬT LẠI** — số của GitHub Actions: `run_id`, thời lượng job, `conclusion`. **Không hiện vật
  nào trong kho**; `run_id` và giờ là **mỏ neo truy tìm**, không thay được hiện vật. Trích log dưới
  đây thuộc loại này.
- **SUY LUẬN CÓ ĐIỀU KIỆN** — kết luận rút ra TỪ nhóm THUẬT LẠI. Nó chỉ đúng nếu nhóm kia đúng.

Mọi câu trong mục này dẫn `run`/`job`/phút đều là **THUẬT LẠI**.

Lượt gate **hậu-merge trên `master`** của `r362` (run `34563553711`, head `4b5184e`, job
`103150987707`, `gate (ubuntu-latest)`) **ĐỎ** ở bước 16 `test registry`, lúc `05:00:27Z 11-09-2026`.
Trích log nguyên văn:

```
CASE T6: DAT · CASE T7: DAT · CASE T8: DAT      <- luot NEN: 8/8 SACH
MUTANT dao-chieu-to-tien | T1 | 0/1
CA DO THUC TE: T1,T7 | rc=1
CASE T7: DO — [Errno 39] Directory not empty: '/tmp/tmpf7cr81q5/remote.git'
CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐỎ rc=1
```

Lượt **nền sạch**. Chỉ lượt **đột biến** có `T7` chết kèm, vì một lỗi dọn thư mục tạm **hoàn toàn
vô can** với đột biến đang thử.

### Cơ chế — đọc được từ mã, chắc chắn

`ops/nhanh_don_duoc_test.py:211` (đo 06:30Z 11-09-2026 trên `26e2555`):

```python
ok = p.returncode != 0 and ca_do == list(dich)
```

Bộ chấm so **danh sách chính xác** tập ca đỏ. Đột biến `dao-chieu-to-tien` nhắm `("T1",)`; tập thật
thành `["T1","T7"]`; lệch ⇒ `ok=False` ⇒ chấm `0/1` ⇒ suite ĐỎ. Đích **đã chết đúng**, nhưng điểm
vẫn là không giết.

### Vì sao "phân biệt `AssertionError` với ngoại lệ khác" KHÔNG đủ

`ops/nhanh_don_duoc_test.py:19-20` — hàm hạ tầng `run()` ném **`AssertionError` trần** cho lỗi
hạ tầng:

```python
if check and p.returncode:
    raise AssertionError(f"rc={p.returncode}: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
```

Đây **đúng** đường giả mạo mà `CLAUDE.md` đã tố cáo ở chuỗi `#355`/`#359`, và nó **không phải giả
thuyết**: phiên soạn đặc tả này đã sinh ra nó THẬT lúc `06:1xZ 11-09-2026` — `CASE T4: DO —
rc=128: git commit -m A`, một `AssertionError` do `git commit` hỏng, không phân biệt được với
assertion của chính ca. Nên tín hiệu "đích chết vì CHỐT CỦA NÓ" phải là một **lớp ngoại lệ riêng**,
không phải một kiểu dựng sẵn mà mọi `raise` trên đường đều viết ra được.

`[Errno 39]` **chưa từng được ghi ở đâu trong kho** (`grep -rniE 'errno 39|Directory not empty'`
trên `*.py` `*.md` `*.sh`, đo 06:0xZ 11-09-2026 ⇒ **0 dòng**). Hình dạng lỗi mới.

---

## `nguon_cap_viec`

Không phải một dòng kế hoạch. Nguồn là **sự cố đo được**: run `34563553711` · job `103150987707` ·
bước 16 · `05:00:27Z 11-09-2026`. Packet **khắc phục**, không phải packet tính năng.

## `review_class`

**`sensitive`** — tính **fail-closed**. `ops/nhanh_don_duoc.py` quyết định **nhánh remote nào XOÁ
ĐƯỢC**; đó là thẩm quyền phá huỷ không hoàn tác được, và `ops/nhanh_don_duoc_test.py` là cổng duy
nhất canh nó. Packet không chạm `.github/workflows/**`, nhưng `§8` bảo path không rõ thì lấy mức
chặt nhất, nên không hạ xuống `standard`.

Hệ quả `ADR-0044` cho `sensitive`: **≤ 3 tệp và ≤ 300 dòng thêm**. Packet này **1 tệp**; ước dòng
thêm ở `chua_do_duoc` #3.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `ops/nhanh_don_duoc_test.py` | chứa cả bộ chấm đột biến (`chay_dot_bien`, dòng 182-219), cả 16 `assert` trần của 8 ca, cả fixture `kho_bare` (dòng 25-66) |

Không ký tự đại diện. Không đường dẫn nào khác.

**Đã đo `ai-dang-giu` lúc 06:40Z 11-09-2026** (sau khi canh hai nguồn ref: `comm -23` RỖNG, và sau
khi dựng nhánh cục bộ cho mọi nhánh máy chủ — công cụ quét `refs/heads/*` nên thiếu nhánh cục bộ là
`CHAN [12]`, không phải `NGƯỜI_GIỮ 0`):

```
ops/nhanh_don_duoc_test.py                        rc=0   NGƯỜI_GIỮ 0: không có
ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md   rc=0   NGƯỜI_GIỮ 0: không có
```

## `ngoai_pham_vi`

1. **KHÔNG chữa nguyên nhân gốc của `[Errno 39]`** — nó **CHƯA BIẾT** (xem `chua_do_duoc` #1).
   Packet này làm bộ chấm **miễn nhiễm với ca đỏ vô can**, việc ấy không cần biết ca kia đỏ vì gì.
2. **KHÔNG đụng `ops/nhanh_don_duoc.py`** — mã sản phẩm không sai; lượt nền `8/8` sạch.
3. **KHÔNG đụng `.github/workflows/ci.yml`** — thuộc `#463`, và packet này cố ý **không** gộp vào đó
   để master không phải chờ `GATE-TACH-JOB-CAT-CHI-PHI` land — packet ấy **lớn hơn hẳn** và đã qua
   **mười** lượt cross-review tính tới hôm nay.
   *(Bản r1 dòng này ghi "`648` dòng", bản vá đầu đổi thành "`844`" — cả hai đều **hết hạn trong
   cùng một PR** vì chính bản vá này làm số ấy đổi tiếp. Nên bỏ hẳn con số: **mẫu số của nó nằm
   ngoài tầm kiểm soát của packet này**, mà một con số như thế thì không neo SHA cũng vô nghĩa, còn
   neo SHA thì vô dụng — nếp đã rút ở `r362`.)*
4. **KHÔNG đụng `ops/lease_publish_test.py`** — `ai-dang-giu` 06:40Z 11-09-2026 ⇒ `rc=11`,
   `NGƯỜI_GIỮ 1: m9-fetch-auth-exec-1-claude-20260911` (`#503`, hạn `17:00:00Z 11-09-2026`).
   Việc cắt bội-3 của `t125` thuộc `#463` revision 5, khai `depends_on: [wp503]`.
5. **KHÔNG sửa `ops/lease_publish_test.py` hay ba bộ test khác cho nhất quán `gpgsign`** — chúng đã
   có. **Đơn vị: SỐ DÒNG CHỨA chuỗi `gpgsign`** (`grep -c`), không phải số lần xuất hiện — đo
   06:2xZ 11-09-2026: `packet_loop_test.py` **10 dòng** · `lease_publish_test.py` 8 ·
   `bien_nhan_v2_test.py` 1 · **`nhanh_don_duoc_test.py` 0**. Hai đơn vị **KHÔNG** bằng nhau:
   `packet_loop_test.py` có **10 dòng** nhưng **11 lần xuất hiện** (`grep -o | wc -l`) — bản r1 viết
   *"số lần nhắc"* cho một phép đếm DÒNG, cross-review lượt 1 bắt (P3). Chỉ tệp thiếu mới được sửa.
6. **KHÔNG chạy lại lượt master `34563553711`** — công cụ chỉ có `rerun_failed_jobs`, không nhắm
   được một job, nên sẽ kéo theo một lượt Windows 60 phút đã biết trước là chết.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Tín hiệu *"ca đích chết vì CHÍNH chốt của nó"* phải là thứ mã hạ tầng **không giả mạo được**: một lớp `TinHieuChotCa(AssertionError)` chỉ do **thân ca** ném. **ĐÚNG 14** `assert` — những cái nằm TRONG `T1…T8` — đổi sang hàm `chot()`. **HAI `assert` CÒN LẠI GIỮ NGUYÊN `AssertionError` trần** vì chúng là **hạ tầng**, không phải chốt của ca: `nap_tool` (dòng 80) và `chay_dot_bien` (dòng 198). `run()` cũng giữ nguyên. | `write_set` #1 |
| M2 | Bộ chấm phân **BA** trạng thái, không phải hai: **GIẾT** (mọi ca trong `dich` đỏ bằng `TinHieuChotCa`, và không ca nào ngoài `dich` đỏ bằng `TinHieuChotCa`) · **KHÔNG GIẾT** · **KHÔNG ĐO ĐƯỢC** (có ca đỏ vì ngoại lệ KHÔNG phải `TinHieuChotCa`). | `write_set` #1 |
| M3 | `KHÔNG ĐO ĐƯỢC` ⇒ chạy lại **ĐÚNG MỘT** lần chính mutant ấy; lần hai vẫn `KHÔNG ĐO ĐƯỢC` ⇒ suite **ĐỎ** kèm in rõ ngoại lệ. Tuyệt đối **không** đường nào biến `KHÔNG ĐO ĐƯỢC` thành GIẾT. | `write_set` #1 |
| M4 | Tắt ký commit ở **MỌI** kho mà bộ test dựng, không chỉ `kho_bare`: `chay_dot_bien` (dòng 186–192) còn dựng **repo `src` thứ hai** rồi `git commit -qm "source"` mà chỉ đặt `user.name`/`user.email`. Sửa một chỗ thì tám ca qua còn **suite đầy đủ vẫn chết ở lần commit nguồn mutant**. | `write_set` #1 |
| M5 | Bộ chấm có **ca tự kiểm cho chính nó** — không ca nào thì bộ chấm là thứ duy nhất trong tệp không ai canh. | `write_set` #1 |
| M6 | **KÊNH KẾT QUẢ phải chịu được giả mạo, vì LỚP NGOẠI LỆ KHÔNG QUA ĐƯỢC RANH GIỚI TIẾN TRÌNH.** Bộ chấm gọi tiến trình con rồi đọc **chuỗi trên stdout**; object ngoại lệ chết ở biên. Lượt con phải phát kết quả ra **một kênh riêng** (fd thứ ba, hoặc tệp kết quả mà bộ chấm truyền đường dẫn vào), **không** trộn với stdout của mã đang bị thử. Bộ chấm đọc **kênh ấy**, không đọc stdout. | `write_set` #1 |

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo làm nó ĐỎ** (`L3`). Tên ca dùng tiền tố `r5xx_` theo idiom kho; số thật
do phiên thi công chọn liên tiếp và ghi vào biên nhận.

**A1 (M1) — tín hiệu chốt KHÔNG giả mạo được, đo bằng PHẢN CHỨNG DƯƠNG.**
Ca `r5xx_tin_hieu_chot_khong_gia_mao_duoc`: trong một lượt mutant, ép **một ca ngoài `dich`** hỏng
bằng đúng đường hạ tầng đã quan sát được (`run()` gặp `rc != 0`, tức `AssertionError` trần).
Đòi: kết quả là **`KHÔNG ĐO ĐƯỢC`**, KHÔNG phải `GIẾT`, KHÔNG phải `KHÔNG GIẾT`.
**Phép làm ĐỎ:** đột biến bản vá — đổi phép so `isinstance(..., TinHieuChotCa)` thành
`isinstance(..., AssertionError)` ⇒ ca này **phải ĐỎ**. Không có đột biến ấy thì không biết ca đang
đo LỚP hay đo thứ khác.

**A1b (M1) — HAI `assert` HẠ TẦNG phải Ở NGUYÊN bên ngoài lớp tín hiệu.**
Ca `r5xx_assert_ha_tang_khong_duoc_cap_lop_chot`: ép `nap_tool` (dòng 80) **và** chốt cuối của
`chay_dot_bien` (dòng 198) hỏng, mỗi cái một lượt. Đòi: **cả hai** cho `KHÔNG ĐO ĐƯỢC`, KHÔNG phải
`GIẾT`, KHÔNG phải `KHÔNG GIẾT`.
**Phép làm ĐỎ:** đổi một trong hai `assert` ấy sang `chot()` ⇒ nó thành tín hiệu chốt hợp lệ ⇒ ca ĐỎ.
Ca này tồn tại vì `M1` của bản r1 từng khai *"**16** assert đổi sang `chot()`"*, mà chỉ **14** thuộc
`T1…T8`; làm đúng con số 16 là **tự tay cấp lớp tín hiệu chốt cho hạ tầng** — đúng thứ packet này
sinh ra để chặn. Số 16 **đúng ở tổng, sai ở phân rã**.

**A2 (M1) — tín hiệu neo cả TÊN CA, không chỉ lớp.**
Ca `r5xx_chot_cua_ca_KHAC_khong_tinh_la_giet`: một mutant làm **ca ngoài `dich`** đỏ bằng
`TinHieuChotCa` thật. Đòi: **KHÔNG GIẾT** (không phải `KHÔNG ĐO ĐƯỢC`, vì đây là tín hiệu thật của
một ca khác — mutant làm hỏng thứ nó không được phép làm hỏng).
**Phép làm ĐỎ:** bỏ phép so tên ca, chỉ còn so lớp ⇒ ca ĐỎ.

**A3 (M2) — ba trạng thái tồn tại RIÊNG BIỆT, đo bằng ba đầu ra khác nhau.**
Ca `r5xx_ba_trang_thai_khong_gop`: ba lượt dựng sẵn cho ra đúng ba nhãn `GIET` · `KHONG_GIET` ·
`KHONG_DO_DUOC`, và dòng tổng kết in ra **ba con số** (`giết` / `không giết` / `không đo được`) với
`giết + không giết + không đo được == len(DOT_BIEN)`.
**Phép làm ĐỎ:** gộp `KHONG_DO_DUOC` vào `KHONG_GIET` ⇒ tổng vẫn đúng nhưng nhãn mất ⇒ ca ĐỎ.
Nêu rõ vì `L5`: đây là câu vừa nêu **số hạng** vừa nêu **quan hệ**; ca phải kiểm **số hạng**, vì
quan hệ `tổng = 10` sống sót qua mọi trôi số.

**A4 (M3) — chạy lại ĐÚNG MỘT lần, đếm bằng SỐ LẦN GỌI chứ không bằng mã thoát.**
Ca `r5xx_chay_lai_dung_mot_lan`: đồ giả **GIỮ TRẠNG THÁI** (không diễn kịch bản) đếm số lần mutant
`X` được chạy. Hai kịch bản:
- lượt 1 `KHÔNG ĐO ĐƯỢC`, lượt 2 `GIẾT` ⇒ kết quả `GIẾT`, **số lần gọi = 2**;
- lượt 1 và 2 đều `KHÔNG ĐO ĐƯỢC` ⇒ suite **ĐỎ**, **số lần gọi = 2** (không phải 3).
**Phép làm ĐỎ:** bỏ trần chạy lại (lặp tới khi xanh) ⇒ kịch bản 2 quay vô hạn / số lần gọi ≠ 2 ⇒ ĐỎ.
Đòi đọc **nhật ký lời gọi**, không đọc mã thoát — nếp kho đã trả giá ở `ops-don-ref` (`40/40` trong
khi một đột biến xoá hẳn lệnh phá vẫn qua).

**A5 (M4) — chạy được trong môi trường CÓ ký commit, đo trên MỌI kho bộ test dựng.**
Ca `r5xx_moi_kho_deu_tat_ky_commit`: liệt kê **mọi** kho mà bộ test `git init`, rồi với từng cái đọc
`git config --get commit.gpgsign` ⇒ phải là `false`. Hôm nay có **hai**: `work` của `kho_bare`
(dòng 25–66) và `src` của `chay_dot_bien` (dòng 186–192).
**Phép làm ĐỎ:** gỡ dòng tắt ký ở **một trong hai** ⇒ ca ĐỎ. Hai đột biến riêng, không gộp —
phiên bản r1 của mục này chỉ đo `work`, nên một bản vá chỉ sửa `kho_bare` vẫn qua được nó.
**Kèm phép đo môi trường thật, KHÔNG thay thế được bằng ca trên:** chạy **TRỌN** bộ test — tức
**có cả vòng đột biến**, không phải chế độ `NHANH_DON_DUOC_KHONG_DOT_BIEN` — trong một môi trường ép
ký commit ⇒ phải `8/8` **và** đủ 10 mutant. Chạy ở chế độ bỏ đột biến là **bỏ sót đúng lần commit
nguồn mutant** mà finding này chỉ ra. Không dựng được môi trường ấy thì khai **`KHÔNG ĐO ĐƯỢC`**.

**A5b (M6) — KÊNH KẾT QUẢ không giả mạo được, đo bằng PHẢN CHỨNG ĐI QUA CHÍNH TIẾN TRÌNH CON.**
Ca `r5xx_kenh_ket_qua_khong_gia_mao_duoc`: mutant làm mã bị thử in ra **stdout** một dòng mang đúng
hình dạng một kết quả ca (tên ca đích + nhãn lớp). Đòi: bộ chấm **KHÔNG** đọc dòng ấy — kết quả phải
lấy từ kênh riêng, nên mutant vẫn phải ra `KHÔNG GIẾT` hoặc `KHÔNG ĐO ĐƯỢC`, tuyệt đối không `GIẾT`.
**Phép làm ĐỎ:** cho bộ chấm quay về đọc stdout ⇒ ca ĐỎ.
Ca này bắt buộc phải đi qua **subprocess thật**, không được gọi bộ phân loại trong bộ nhớ: lỗ hổng
nằm ở **ranh giới tiến trình**, mà một phép thử trong bộ nhớ không có ranh giới ấy để mà thủng.
Thêm ba ca biên của kênh: **dòng trùng** (một ca hai kết quả) · **thiếu dòng** (ca chạy mà không phát
kết quả) · **dòng của ca không tồn tại**. Cả ba ⇒ `KHÔNG ĐO ĐƯỢC`, không cái nào được ⇒ `GIẾT`.

**A6 (M5) — bộ chấm tự kiểm không phải là một lời hứa.**
Đòi: **≥ 8** ca `r5xx_` mới (A1 · A1b · A2 · A3 · A4 · A5 · A5b · và ba ca biên của kênh ở A5b tính
chung một), và **mỗi ca có đúng một đột biến riêng làm nó ĐỎ**. Đếm bằng
`(tên ca, tên đột biến, đã chạy, ĐỎ)`; ca nào không có đột biến riêng thì **không tính**.
**Phép làm ĐỎ:** một ca thiếu đột biến ⇒ bảng đếm lệch ⇒ khai thiếu.

**A7 (toàn packet) — suite vẫn xanh, và số đếm KHÔNG tụt.**
`python3 ops/nhanh_don_duoc_test.py` ⇒ `8/8` cho ca, và dòng tổng kết đột biến khai
`giết = 10 · không giết = 0 · không đo được = 0` trên `len(DOT_BIEN) = 10` (đo 06:30Z 11-09-2026:
`DOT_BIEN` có **10** mục). Hai số phải **BẰNG NHAU**, không tin `rc=0` suông.
**Phép làm ĐỎ:** bất kỳ mutant nào tụt khỏi `giết`.

**A8 (toàn packet) — `ADR-0044`.**
`git diff --numstat` trên phạm vi packet ⇒ **1 tệp**, **dòng thêm ≤ 300**. Vượt ⇒ **DỪNG và hỏi chủ
kho**, không tự xin ngoại lệ. Tiền lệ hình thức: `#502` khai `ngoai_le_adr_0044` neo comment chủ kho.

## `hinh_dang_ke_thua`

Chép từ `CLAUDE.md` (mục *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*, đọc lại
06:45Z 11-09-2026) và từ hồ sơ `#355`/`#359`. Mỗi dòng ghi thời điểm đo hoặc nguồn trích (`L5`).

| hình dạng | số lần đã gặp | đo/trích lúc | ghi chú |
|---|---:|---|---|
| bộ chấm **CẤP TÍN DỤNG GIẢ** — mutant không chết đúng chốt mà vẫn được tính GIẾT | **2** | `#355`/`#359`, trích `CLAUDE.md:410–433`, đọc lại 06:45Z 11-09-2026 | `#355`: khai `22/22 bị giết` ⇒ phân hạng lại **19 giết thật / 3 tín dụng giả / 0 sống sót**. `#359`: bản vá vòng một **vẫn bị lừa** vì `except Exception: raise AssertionError(...)` viết với ý định ĐÚNG lại dựng đúng tín hiệu bộ chấm tin. **Chiều: QUÁ RỘNG RÃI.** |
| bộ chấm **TỪ CHỐI GHI CÔNG** — mutant chết ĐÚNG chốt mà bị tính KHÔNG GIẾT | **1** | sự cố sinh ra packet này, đo 05:00:27Z 11-09-2026 | `T1` (đích) chết ĐÚNG; `T7` đỏ vì `[Errno 39]` vô can ⇒ tập lệch ⇒ `0/1`. **Chiều: QUÁ KHẮT KHE.** |

**Hai hàng trên CỐ Ý tách, và bản r1 của đặc tả này đã gộp chúng — cross-review lượt 1 bắt (P2
`lan-thu-ba-khong-cung-hinh-dang-tin-dung-gia`).** r1 đếm sự cố hiện tại là **lần thứ 3** của cùng
một hình dạng rồi lấy số `3` ấy để kích hoạt `§12`. Sai: `#355`/`#359` là **cấp thừa**, sự cố này là
**cấp thiếu** — hai chiều ngược nhau. Cùng thuộc họ *"thước đo bị lỗi hạ tầng làm sai"* không làm
chúng cùng một thuộc tính hẹp đang đếm.

**Hệ quả phải nói thẳng: `§12` KHÔNG được kích hoạt bởi con số này.** Chiều *cấp thừa* mới ở lần 2,
chiều *cấp thiếu* ở lần 1. Bản vá của packet — **lớp ngoại lệ riêng + neo tên ca + kênh kết quả
riêng** — vẫn đúng và vẫn cần, nhưng nó phải tự đứng bằng lập luận của nó, **không** được mượn một
ngưỡng `§12` chưa đạt để tự cấp thẩm quyền. Đây đúng là bệnh *"một con số chống đỡ một câu về THẨM
QUYỀN"* mà `soan-spec` `L5` cảnh báo.
| con số mutant **báo cho chủ kho rồi phải rút lại** | **2** | trích `CLAUDE.md` 06:45Z 11-09-2026 | cả hai lần vì *"tin một tầng mà chưa thử tầng dưới nó"*. Đây là lý do A1/A2 đòi **đột biến vào chính bản vá**, không chỉ đòi ca xanh. |
| lời khai rộng hơn phép đo, trong chính lượt soạn đặc tả này | **1** | đo 06:1xZ–06:3xZ 11-09-2026 | phép thử 80 lượt dưới tải cho `48/80 đỏ`; truy ra là **rig cạn file descriptor** (PID 488 giữ 19999/20000 socket vì container ký mọi commit) ⇒ **đã RÚT**, không phải phát hiện. Ghi vào đây để phiên thi công không đọc lại con số ấy như dữ liệu. |
| đồ giả **diễn kịch bản** thay vì mô phỏng trạng thái | **1** | trích `CLAUDE.md` (mục `ops-don-ref`, `40/40`) 06:45Z 11-09-2026 | lý do A4 đòi đồ giả GIỮ TRẠNG THÁI và đọc **nhật ký lời gọi**. |

## `chua_do_duoc`

1. **Nguyên nhân gốc của `[Errno 39]`: KHÔNG BIẾT.** Đã thử, không tái hiện:
   - 12 lượt trên `27c413c` + 12 lượt trên `4b5184e`, **một lệnh hai vòng lặp cùng rig** ⇒ `DO=0`,
     `Errno39=0` cả hai ⇒ **delta `r362` = 0** (đo 06:0xZ 11-09-2026);
   - ép `gc.auto=1 autoDetach=true` ×10 ⇒ **0**; đối chứng `gc.auto=0` ×10 ⇒ **0** ⇒ giả thuyết
     *"`git push` → `receive-pack` → `gc --auto` tách nền đua với `TemporaryDirectory.cleanup()`"*
     **KHÔNG được xác nhận** (đo 06:2xZ 11-09-2026).
   Tổng **44 lượt hợp lệ, 0 tái hiện**. Một khác biệt **chưa thử được**: git cục bộ **2.43.0** so với
   runner **2.55.0**. Packet này **cố ý không** đi chữa nó (`ngoai_pham_vi` #1) — nợ để mở, chưa có tên.
2. **Không đo được bản vá có làm lượt master xanh trở lại hay không** cho tới khi nó chạy trên CI.
   Lượt nền `8/8` sạch nên có cơ sở tin, nhưng *"có cơ sở tin"* không phải *"đã đo"*.
3. **Ước dòng thêm chưa phải phép đo.** 16 `assert` trần đổi sang `chot()` + lớp ngoại lệ + bộ chấm
   ba trạng thái + chạy lại có trần + 5 ca tự kiểm + 5 đột biến. Ước **≈ 90–150** dòng thêm trên tệp
   233 dòng (đo 06:2xZ 11-09-2026). Trần `ADR-0044` là **300**; nếu thi công vượt thì **DỪNG**, đừng
   tự xin ngoại lệ — A8.
4. **`§12` "lặp ba lần thì hỏi có nên làm cách này không".** `hinh_dang_ke_thua` dòng 1 đếm **3**.
   Đặc tả này khẳng định câu trả lời là **đổi loại tín hiệu** (lớp riêng + tên ca), không phải vá
   tiếp phép so — nhưng **người quyết là chủ kho**, không phải đặc tả. Nếu chủ kho thấy cách làm vẫn
   sai gốc thì packet này phải bị bác chứ không phải được nới.
