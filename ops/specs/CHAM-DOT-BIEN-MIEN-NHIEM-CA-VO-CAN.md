# Đặc tả packet — CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN (revision 1)

- `packet_id`: **CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được khi có số Issue — tiền lệ `#456`/`#463` giữ bí danh ở `packet_id`,
  số ở `packet_issue`)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi. Packet này sinh ra từ một sự cố đo được
  chứ không từ một lane kế hoạch, nên chưa có mission nào ôm nó. Khuyến nghị: gắn vào cùng mission
  với `#463` nếu chủ kho mở một mission chung cho lane CI.
- `revision`: **1** · `generation`: 1
- Thời điểm soạn: **06:45Z 11-09-2026**. Mọi con số dưới đây ghi kèm thời điểm đo (`L5`).

---

## Vấn đề — đo được, không suy diễn

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
   để master không phải chờ một packet 648 dòng đặc tả land.
4. **KHÔNG đụng `ops/lease_publish_test.py`** — `ai-dang-giu` 06:40Z 11-09-2026 ⇒ `rc=11`,
   `NGƯỜI_GIỮ 1: m9-fetch-auth-exec-1-claude-20260911` (`#503`, hạn `17:00:00Z 11-09-2026`).
   Việc cắt bội-3 của `t125` thuộc `#463` revision 5, khai `depends_on: [wp503]`.
5. **KHÔNG sửa `ops/lease_publish_test.py` hay ba bộ test khác cho nhất quán `gpgsign`** — chúng đã
   có (đo 06:2xZ 11-09-2026: `packet_loop_test.py` 10 · `lease_publish_test.py` 8 ·
   `bien_nhan_v2_test.py` 1 · **`nhanh_don_duoc_test.py` 0**). Chỉ tệp thiếu mới được sửa.
6. **KHÔNG chạy lại lượt master `34563553711`** — công cụ chỉ có `rerun_failed_jobs`, không nhắm
   được một job, nên sẽ kéo theo một lượt Windows 60 phút đã biết trước là chết.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Tín hiệu *"ca đích chết vì CHÍNH chốt của nó"* phải là thứ mã hạ tầng **không giả mạo được**: một lớp `TinHieuChotCa(AssertionError)` chỉ do thân ca ném; **16** `assert` trần đổi sang một hàm `chot()` ném lớp ấy. `run()` giữ nguyên `AssertionError` trần — nó LÀ lỗi hạ tầng. | `write_set` #1 |
| M2 | Bộ chấm phân **BA** trạng thái, không phải hai: **GIẾT** (mọi ca trong `dich` đỏ bằng `TinHieuChotCa`, và không ca nào ngoài `dich` đỏ bằng `TinHieuChotCa`) · **KHÔNG GIẾT** · **KHÔNG ĐO ĐƯỢC** (có ca đỏ vì ngoại lệ KHÔNG phải `TinHieuChotCa`). | `write_set` #1 |
| M3 | `KHÔNG ĐO ĐƯỢC` ⇒ chạy lại **ĐÚNG MỘT** lần chính mutant ấy; lần hai vẫn `KHÔNG ĐO ĐƯỢC` ⇒ suite **ĐỎ** kèm in rõ ngoại lệ. Tuyệt đối **không** đường nào biến `KHÔNG ĐO ĐƯỢC` thành GIẾT. | `write_set` #1 |
| M4 | Fixture `kho_bare` đặt `commit.gpgsign=false` như ba bộ test anh em, để bộ test chạy được trong môi trường ký commit. | `write_set` #1 |
| M5 | Bộ chấm có **ca tự kiểm cho chính nó** — không ca nào thì bộ chấm là thứ duy nhất trong tệp không ai canh. | `write_set` #1 |

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo làm nó ĐỎ** (`L3`). Tên ca dùng tiền tố `r5xx_` theo idiom kho; số thật
do phiên thi công chọn liên tiếp và ghi vào biên nhận.

**A1 (M1) — tín hiệu chốt KHÔNG giả mạo được, đo bằng PHẢN CHỨNG DƯƠNG.**
Ca `r5xx_tin_hieu_chot_khong_gia_mao_duoc`: trong một lượt mutant, ép **một ca ngoài `dich`** hỏng
bằng đúng đường hạ tầng đã quan sát được (`run()` gặp `rc != 0`, tức `AssertionError` trần).
Đòi: kết quả là **`KHÔNG ĐO ĐƯỢC`**, KHÔNG phải `GIẾT`, KHÔNG phải `KHÔNG GIẾT`.
**Phép làm ĐỎ:** đột biến bản vá — đổi phép so `isinstance(..., TinHieuChotCa)` thành
`isinstance(..., AssertionError)` ⇒ ca này **phải ĐỎ**. Không có đột biến ấy thì không biết ca đang
đo LỚP hay đo thứ khác. (Đúng chốt mà `CLAUDE.md` đòi ở chuỗi `#355`/`#359`.)

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

**A5 (M4) — chạy được trong môi trường CÓ ký commit, đo bằng PHẢN CHỨNG.**
Ca `r5xx_fixture_tat_ky_commit`: dựng fixture rồi đọc lại `git config --get commit.gpgsign` trong
repo `work` ⇒ phải là `false`.
**Phép làm ĐỎ:** gỡ dòng `commit.gpgsign=false` ⇒ ca ĐỎ.
**Kèm phép đo môi trường thật, không thay thế được bằng ca trên:** chạy trọn bộ test trong một môi
trường ép ký commit (`gpg.format` trỏ một helper luôn hỏng) ⇒ phải `8/8`. Không dựng được môi
trường ấy thì khai **`KHÔNG ĐO ĐƯỢC`**, đừng khai ĐẠT.

**A6 (M5) — bộ chấm tự kiểm không phải là một lời hứa.**
Đòi: **≥ 5** ca `r5xx_` mới (A1–A5), và **mỗi ca có đúng một đột biến riêng làm nó ĐỎ**. Đếm bằng
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
| bộ chấm tin một tín hiệu mà **mã vô can dựng lên được** | **3** | `#355`/`#359` (2) trích `CLAUDE.md` 06:45Z 11-09-2026; lần 3 = sự cố này, đo 05:00:27Z 11-09-2026 | `#355`: khai `22/22 bị giết` ⇒ phân hạng lại **19 giết thật / 3 tín dụng giả / 0 sống sót**. `#359`: bản vá vòng một **vẫn bị lừa** vì `except Exception: raise AssertionError(...)` viết với ý định ĐÚNG lại dựng đúng tín hiệu bộ chấm tin. **Lần thứ 3 ⇒ `§12` đòi xem lại CÁCH LÀM, không chỉ vá.** Câu trả lời của packet này: **lớp ngoại lệ riêng + neo tên ca**, tức đổi loại tín hiệu, không nới phép so. |
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
