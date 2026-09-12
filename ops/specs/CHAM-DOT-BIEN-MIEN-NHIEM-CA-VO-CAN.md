# Đặc tả packet — CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN (revision 6)

- `packet_id`: **CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** Packet sinh từ một sự cố đo được, chưa lane nào ôm.
- `revision`: **6** · `generation`: 1 · soạn **11:1xZ 11-09-2026**
- `depends_on`: **`[]`**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

> **Tệp này KHÔNG thuật lại lịch sử của chính nó.** Vết revision 1–3 nằm ở PR `#508` và `git log`.
> Mọi câu ở đây là **hợp đồng đang hiệu lực**, phát biểu ở thì hiện tại.

---

## `nguon_cap_viec`

**Sự cố đo được**, không phải một dòng kế hoạch: run `34563553711` · job `103150987707` ·
bước 16 `test registry` · `05:00:27Z 11-09-2026`. Trích log nguyên văn (**THUẬT LẠI**):

```
CASE T6: DAT · CASE T7: DAT · CASE T8: DAT      <- luot NEN: 8/8 SACH
MUTANT dao-chieu-to-tien | T1 | 0/1
CA DO THUC TE: T1,T7 | rc=1
CASE T7: DO — [Errno 39] Directory not empty: '/tmp/tmpf7cr81q5/remote.git'
CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐỎ rc=1
```

Lượt **nền sạch**. Chỉ lượt **đột biến** có `T7` chết kèm, vì một lỗi dọn thư mục tạm **vô can** với
đột biến đang thử.

### Cơ chế — đọc được từ mã

`ops/nhanh_don_duoc_test.py:211` (đo 06:30Z 11-09-2026 trên `26e2555`):

```python
ok = p.returncode != 0 and ca_do == list(dich)
```

Bộ chấm so **danh sách chính xác** tập ca đỏ. Đột biến `dao-chieu-to-tien` nhắm `("T1",)`; tập thật
thành `["T1","T7"]`; lệch ⇒ `ok=False` ⇒ chấm `0/1`. Đích **đã chết đúng**, điểm vẫn là không giết.

### Vì sao "phân biệt `AssertionError` với ngoại lệ khác" KHÔNG đủ

`ops/nhanh_don_duoc_test.py:19-20` — hàm hạ tầng `run()` ném **`AssertionError` trần** cho lỗi hạ tầng:

```python
if check and p.returncode:
    raise AssertionError(f"rc={p.returncode}: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
```

Đây đúng đường giả mạo mà `CLAUDE.md` tố cáo ở chuỗi `#355`/`#359`, và nó **không phải giả thuyết**:
phiên soạn đã sinh ra nó THẬT lúc `06:1xZ 11-09-2026` — `CASE T4: DO — rc=128: git commit -m A`, một
`AssertionError` do `git commit` hỏng, **không phân biệt được** với assertion của chính ca.

⇒ Tín hiệu *"đích chết vì CHỐT CỦA NÓ"* phải là **lớp ngoại lệ riêng**, không phải một kiểu dựng sẵn
mà mọi `raise` trên đường đều viết ra được.

`[Errno 39]` **chưa từng được ghi ở đâu trong kho** (`grep -rniE 'errno 39|Directory not empty'` trên
`*.py` `*.md` `*.sh`, đo 06:0xZ 11-09-2026 ⇒ **0** dòng). Hình dạng lỗi mới.

## MÔ HÌNH ĐE DOẠ — khai trước, vì mọi tiêu chí về kênh kết quả neo vào nó

Đặc tả này bảo vệ kênh kết quả khỏi **một TẬP LỖI KHAI TƯỜNG MINH**, không phải khỏi *"lỗi vô ý"* —
**ý định của tác giả không tạo ra ranh giới lỗi nào**, và bản trước nói sai chỗ đó. Tập được bảo vệ:

| # | lỗi | chốt nào bắt |
|---|---|---|
| E1 | một `raise` trên đường hạ tầng sinh ra đúng kiểu ngoại lệ bộ chấm tin | lớp `TinHieuChotCa` riêng (`M1`) |
| E2 | một ca **ngoài `dich`** đỏ và làm lệch tập ca đỏ | ba trạng thái + neo tên ca (`M2`, `A2`) |
| E3 | bản ghi của **lượt khác** (mutant/lần thử/rc khác) lọt vào kênh | neo `(ca·mutant·lần thử·rc)` (`M7`) |
| E4 | bản ghi của **cùng định danh nghiệp vụ nhưng lượt trước** bị phát lại | **dấu phiên sinh mới mỗi lượt** (`M7`, `A5c(1)(1b)`) |
| E5 | lượt con chết giữa chừng để lại đủ số bản ghi | bản ghi **đóng lượt** (`M7`, `A5c(2)`) |
| E6 | hai bản ghi cho cùng một ca, hoặc ca lạ, hoặc thiếu ca | đúng một bản ghi/ca (`M7`, `A5b`) |
| E7 | mã sản phẩm gọi **đúng hàm phát** của khung và tự khai tên ca khác | khung đóng dấu tên ca từ trạng thái của chính nó (`A5c(3)`) |

**Thứ tập này KHÔNG phủ, bất kể tác giả có ý định gì:** mã cùng interpreter **sửa thẳng trạng thái
khung** (gán lại tên ca đang chạy, thay chính hàm phát, vá `sys.modules`). `E7` chỉ chặn đường **gọi
hàm**, không chặn đường **sửa trạng thái** — và một lỗi **vô ý** cũng đi được đường ấy. `chua_do_duoc`
#4/#5 giữ nguyên phần này ở trạng thái **chưa chặn**.
Hai sự cố đã xảy ra (`#355`/`#359` và `CASE T4`) thuộc **E1**.

**Nó KHÔNG bảo vệ khỏi mã ĐỐI KHÁNG — hay khỏi một lỗi vô ý đi cùng đường ấy — trong cùng
interpreter, và không thể.** `nap_tool`
(dòng 78–84) `import` mã sản phẩm **vào chính tiến trình chạy ca**, nên giữa khung test và mã bị thử
**không có ranh giới quyền nào**. Phạm vi biến Python **không phải** một miền quyền: mã cùng
interpreter sửa được trạng thái và hàm của khung.

**Nói thẳng vì bản trước nói sai:** giữ handle trong một hàm **không** phải "quyền ghi", và một dấu
phiên truyền vào cùng miền tin cậy **chỉ canh phát lại**, không chứng minh nguồn. Khai đúng phạm vi
là điều kiện để các tiêu chí dưới đây không rộng hơn phép đo của chúng.

**Thứ vẫn làm được, và làm được thì phải đo:** bộ chấm **không nhận** một bản ghi mà nó không thể
quy về **lượt nó vừa phóng** (neo `(ca · mutant · lần thử · rc · dấu phiên)`), và **không nhận** một
bản ghi thứ hai cho cùng một ca. Hai chốt ấy giết cả lớp giả mạo ngẫu nhiên, và mỗi chốt có một ca
đổi màu. Giới hạn còn lại ghi ở `chua_do_duoc` #5.

## `review_class`

**`sensitive`** — tính **fail-closed**. `ops/nhanh_don_duoc.py` quyết định **nhánh remote nào XOÁ
ĐƯỢC**; đó là thẩm quyền phá huỷ không hoàn tác được, và `ops/nhanh_don_duoc_test.py` là cổng duy
nhất canh nó. `§8`: path không rõ thì lấy mức chặt nhất.

`ADR-0044` cho `sensitive`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **1 tệp**. **Trần dòng thêm đã được chủ kho BỎ cho packet này** — xem A8; ước dòng ở `chua_do_duoc` #3 là ảnh chụp lúc soạn, KHÔNG còn là ràng buộc.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `ops/nhanh_don_duoc_test.py` | chứa bộ chấm đột biến (`chay_dot_bien`, dòng 182–219), **14** `assert` trần của 8 ca (tổng tệp **16**; hai cái kia là HẠ TẦNG — `nap_tool:80`, `chay_dot_bien:198`), và fixture `kho_bare` (dòng 25–66) |

Không ký tự đại diện. Không đường dẫn nào khác.

**Đo `ai-dang-giu` 06:40Z 11-09-2026** (sau canh hai nguồn ref, `comm -23` RỖNG; công cụ quét
`refs/heads/*` nên thiếu nhánh cục bộ là `CHAN [12]`, **không phải** `NGƯỜI_GIỮ 0`):

```
ops/nhanh_don_duoc_test.py                        rc=0   NGƯỜI_GIỮ 0: không có
ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md   rc=0   NGƯỜI_GIỮ 0: không có
```

## `ngoai_pham_vi`

1. **KHÔNG chữa nguyên nhân gốc của `[Errno 39]`** — nó **CHƯA BIẾT** (`chua_do_duoc` #1). Packet làm
   bộ chấm **miễn nhiễm với ca đỏ vô can**; việc ấy không cần biết ca kia đỏ vì gì.
2. **KHÔNG đụng `ops/nhanh_don_duoc.py`** — mã sản phẩm không sai; lượt nền `8/8` sạch.
3. **KHÔNG đụng `.github/workflows/ci.yml`** — thuộc `#463`/`T125-RA-JOB-RIENG`. Packet này cố ý
   **không** gộp vào đó để master không phải chờ chúng land.
4. **KHÔNG đụng `ops/lease_publish_test.py`** — `#503` giữ (đo 06:40Z 11-09-2026, `rc=11`,
   `m9-fetch-auth-exec-1-claude-20260911`). Việc cắt bội số của `t125` thuộc packet
   **`T125-RA-JOB-RIENG`**, không thuộc packet này và không thuộc `#463`.
5. **KHÔNG sửa ba bộ test khác cho nhất quán `gpgsign`** — chúng đã có. **Đơn vị: SỐ DÒNG CHỨA chuỗi
   `gpgsign`** (`grep -c`), không phải số lần xuất hiện — đo 06:2xZ 11-09-2026:
   `packet_loop_test.py` **10 dòng** · `lease_publish_test.py` **8** · `bien_nhan_v2_test.py` **1** ·
   **`nhanh_don_duoc_test.py` 0**. Hai đơn vị **KHÔNG** bằng nhau: `packet_loop_test.py` có **10 dòng**
   nhưng **11 lần xuất hiện** (`grep -o | wc -l`). Chỉ tệp thiếu mới được sửa.
6. **KHÔNG chạy lại lượt master `34563553711`** — công cụ chỉ có `rerun_failed_jobs`, không nhắm được
   một job, nên sẽ kéo theo một lượt Windows 60 phút đã biết trước là chết. Cùng hướng với chỉ thị
   chủ kho 11-09-2026: **không phóng lượt CI khi chưa đủ điều kiện merge**.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Tín hiệu *"ca đích chết vì CHÍNH chốt của nó"* là thứ mã hạ tầng **không giả mạo được**: lớp `TinHieuChotCa(AssertionError)` chỉ do **thân ca** ném. **ĐÚNG 14** `assert` — những cái trong `T1…T8` — đổi sang hàm `chot()`. **HAI `assert` còn lại GIỮ NGUYÊN `AssertionError` trần** vì chúng là **hạ tầng**: `nap_tool:80` và `chay_dot_bien:198`. `run()` cũng giữ nguyên. | `write_set` #1 |
| M2 | Bộ chấm phân **BA** trạng thái: **GIẾT** (mọi ca trong `dich` đỏ bằng `TinHieuChotCa`, và không ca nào ngoài `dich` đỏ bằng `TinHieuChotCa`) · **KHÔNG GIẾT** · **KHÔNG ĐO ĐƯỢC** (có ca đỏ vì ngoại lệ KHÔNG phải `TinHieuChotCa`). | `write_set` #1 |
| M3 | `KHÔNG ĐO ĐƯỢC` ⇒ chạy lại **ĐÚNG MỘT** lần chính mutant ấy; lần hai vẫn `KHÔNG ĐO ĐƯỢC` ⇒ suite **ĐỎ** kèm in rõ ngoại lệ. Không đường nào biến `KHÔNG ĐO ĐƯỢC` thành GIẾT. | `write_set` #1 |
| M4 | Tắt ký commit ở **MỌI** kho bộ test dựng: `kho_bare` (dòng 25–66) **và** repo `src` thứ hai trong `chay_dot_bien` (dòng 186–192). Sửa một chỗ thì tám ca qua còn suite đầy đủ vẫn chết ở lần commit nguồn mutant. | `write_set` #1 |
| M5 | Bộ chấm có **ca tự kiểm cho chính nó** — không có thì nó là thứ duy nhất trong tệp không ai canh. | `write_set` #1 |
| M6 | **Kênh kết quả riêng**, vì **lớp ngoại lệ KHÔNG qua được ranh giới tiến trình**: bộ chấm gọi tiến trình con rồi đọc **chuỗi trên stdout**, object ngoại lệ chết ở biên. Lượt con phát kết quả ra kênh riêng; bộ chấm đọc **kênh ấy**. | `write_set` #1 |
| M7 | **Bản ghi neo vào LƯỢT, và ca do KHUNG đóng dấu.** Mỗi bản ghi **ca** mang `(tên ca · tên mutant · số lần thử · dấu phiên)`; `rc` neo ở mức **LƯỢT**, nằm trong bản ghi **đóng lượt** và được so với mã thoát THẬT của tiến trình con — không lặp lại trong từng bản ghi ca. *(Sửa 12-09-2026: câu gốc liệt kê `rc` vào bản ghi ca, lệch với thứ mã thực sự ghi.)* bộ chấm chỉ nhận bản ghi neo đúng lượt nó vừa phóng. **Dấu phiên phải NGẪU NHIÊN và SINH MỚI MỖI LƯỢT** — mang và so một dấu là chưa đủ: một dấu tái dùng qua hai lần chạy cùng `(mutant, lần thử, rc)` làm bản ghi cũ được nhận lại, và ca *"bỏ so dấu"* vẫn xanh. Cấm lấy mốc thời gian độ phân giải thấp làm dấu (trùng khi chạy nhanh), và đòi bản ghi **đóng lượt**. **Tên ca do khung đóng dấu từ trạng thái của chính khung**, KHÔNG lấy từ đối số người gọi — nên không lời gọi nào tự khai mình là ca khác. **Đúng một** bản ghi cho mỗi ca; cái thứ hai ⇒ `KHÔNG ĐO ĐƯỢC`. | `write_set` #1 |

## `nghiem_thu`

Tên ca dùng tiền tố `r5xx_`; số thật do phiên thi công chọn liên tiếp và ghi vào biên nhận.
Mỗi tiêu chí nêu **phép đo làm nó ĐỎ** (`L3`).

**A1 (M1) — tín hiệu chốt KHÔNG giả mạo được.**
Ca `r5xx_tin_hieu_chot_khong_gia_mao_duoc`: trong một lượt mutant, ép **một ca ngoài `dich`** hỏng
bằng đúng đường hạ tầng đã quan sát (`run()` gặp `rc != 0` ⇒ `AssertionError` trần).
Đòi: **`KHÔNG ĐO ĐƯỢC`** — không phải `GIẾT`, không phải `KHÔNG GIẾT`.
**Phép làm ĐỎ:** đổi `isinstance(..., TinHieuChotCa)` thành `isinstance(..., AssertionError)` ⇒ ca ĐỎ.

**A1b (M1) — HAI `assert` HẠ TẦNG ở NGUYÊN ngoài lớp tín hiệu.**
Ca `r5xx_assert_ha_tang_khong_duoc_cap_lop_chot`: ép `nap_tool:80` **và** chốt cuối
`chay_dot_bien:198` hỏng, mỗi cái một lượt. Đòi **cả hai** cho `KHÔNG ĐO ĐƯỢC`.
**Phép làm ĐỎ:** đổi một trong hai sang `chot()` ⇒ nó thành tín hiệu hợp lệ ⇒ ca ĐỎ.
Ca này tồn tại vì con số **16** **đúng ở tổng, sai ở phân rã**: chỉ **14** thuộc `T1…T8`, và làm đúng
`16` là **tự tay cấp lớp tín hiệu chốt cho hạ tầng** — đúng thứ packet sinh ra để chặn.

**A2 (M1) — tín hiệu neo cả TÊN CA, không chỉ lớp.**
Ca `r5xx_chot_cua_ca_KHAC_khong_tinh_la_giet`: một mutant làm **ca ngoài `dich`** đỏ bằng
`TinHieuChotCa` **thật**. Đòi **KHÔNG GIẾT** (không phải `KHÔNG ĐO ĐƯỢC`: đây là tín hiệu thật của
một ca khác — mutant làm hỏng thứ nó không được phép làm hỏng).
**Phép làm ĐỎ:** bỏ phép so tên ca, chỉ còn so lớp ⇒ ca ĐỎ.

**A3 (M2) — ba trạng thái tồn tại RIÊNG BIỆT.**
Ca `r5xx_ba_trang_thai_khong_gop`: ba lượt dựng sẵn cho đúng ba nhãn `GIET` · `KHONG_GIET` ·
`KHONG_DO_DUOC`; dòng tổng kết in **ba con số** với
`giết + không giết + không đo được == len(DOT_BIEN)`.
**Phép làm ĐỎ:** gộp `KHONG_DO_DUOC` vào `KHONG_GIET` ⇒ tổng vẫn đúng, nhãn mất ⇒ ca ĐỎ.
Nêu rõ vì `L5`: câu này vừa nêu **số hạng** vừa nêu **quan hệ**; ca phải kiểm **số hạng**, vì quan hệ
`tổng = 10` sống sót qua mọi trôi số.

**A4 (M3) — chạy lại ĐÚNG MỘT lần, đếm bằng SỐ LẦN GỌI.**
Ca `r5xx_chay_lai_dung_mot_lan`: đồ giả **GIỮ TRẠNG THÁI** (không diễn kịch bản) đếm số lần mutant
`X` được chạy. Hai kịch bản:
- lượt 1 `KHÔNG ĐO ĐƯỢC`, lượt 2 `GIẾT` ⇒ kết quả `GIẾT`, **số lần gọi = 2**;
- lượt 1 và 2 đều `KHÔNG ĐO ĐƯỢC` ⇒ suite **ĐỎ**, **số lần gọi = 2** (không phải 3).
**Phép làm ĐỎ:** bỏ trần chạy lại ⇒ kịch bản 2 quay vô hạn / số lần gọi ≠ 2 ⇒ ĐỎ.
Đòi đọc **nhật ký lời gọi**, không đọc mã thoát — nếp đã trả giá ở `ops-don-ref` (`40/40` trong khi
một đột biến xoá hẳn lệnh phá vẫn qua).

**A5 (M4) — chạy được trong môi trường CÓ ký commit, đo trên MỌI kho bộ test dựng.**
Ca `r5xx_moi_kho_deu_tat_ky_commit`: liệt kê **mọi** kho bộ test `git init`, đọc
`git config --get commit.gpgsign` ⇒ phải `false`. Hôm nay có **hai**: `work` của `kho_bare` (25–66)
và `src` của `chay_dot_bien` (186–192).
**Phép làm ĐỎ:** gỡ dòng tắt ký ở **một trong hai** ⇒ ca ĐỎ. **Hai đột biến riêng, không gộp** — một
bản vá chỉ sửa `kho_bare` vẫn qua được phép đo chỉ đo `work`.
**Kèm phép đo môi trường thật, KHÔNG thay thế được bằng ca trên:** chạy **TRỌN** bộ test — **có cả
vòng đột biến**, không phải chế độ `NHANH_DON_DUOC_KHONG_DOT_BIEN` — trong môi trường ép ký commit ⇒
phải `8/8` **và** đủ 10 mutant. Chạy ở chế độ bỏ đột biến là **bỏ sót đúng lần commit nguồn mutant**
mà finding này chỉ ra. Không dựng được môi trường ấy ⇒ khai **`KHÔNG ĐO ĐƯỢC`** (và đó là thiếu
nghiệm thu, không được mượn ngoại lệ của tiêu chí khác).

**A5b (M6) — KÊNH KẾT QUẢ không lẫn với stdout, đo QUA CHÍNH TIẾN TRÌNH CON.**
Ca `r5xx_kenh_ket_qua_khong_gia_mao_duoc`: mutant làm mã bị thử in ra **stdout** một dòng mang đúng
hình dạng một kết quả ca (tên ca đích + nhãn lớp). Đòi bộ chấm **KHÔNG** đọc dòng ấy ⇒ mutant ra
`KHÔNG GIẾT` hoặc `KHÔNG ĐO ĐƯỢC`, tuyệt đối không `GIẾT`.
**Phép làm ĐỎ:** cho bộ chấm quay về đọc stdout ⇒ ca ĐỎ.
Ca này **bắt buộc đi qua subprocess thật**, không được gọi bộ phân loại trong bộ nhớ: lỗ hổng nằm ở
**ranh giới tiến trình**, mà một phép thử trong bộ nhớ không có ranh giới ấy để mà thủng.
Thêm ba ca biên: **dòng trùng** · **thiếu dòng** · **dòng của ca không tồn tại**. Cả ba ⇒
`KHÔNG ĐO ĐƯỢC`; không cái nào được ⇒ `GIẾT`.

**A5c (M7) — bản ghi phải QUY VỀ ĐƯỢC lượt vừa phóng, và ca do KHUNG đóng dấu.**
**BỐN** ca (`1`, `1b`, `2`, `3`), mỗi ca một đột biến riêng làm **đúng ca đó** đổi màu.

1. `r5xx_ban_ghi_luot_TRUOC_chi_khac_dau_phien`. Cấy vào kênh một bộ bản ghi **hợp lệ về mọi mặt
   khác**: **đúng tên ca**, **đúng tên mutant của lượt hiện tại**, **đúng số lần thử**, **đúng `rc`**,
   đủ ca, không trùng, không thiếu, có bản ghi đóng lượt — **chỉ khác DẤU PHIÊN**.
   Đòi **`KHÔNG ĐO ĐƯỢC`**.
   **Phép làm ĐỎ:** bỏ phép so **dấu phiên** ⇒ bộ bản ghi ấy được nhận ⇒ ca **ĐỎ**.
   **Ca phải dựng đúng như trên, không được đổi khác:** nếu bản ghi cấy vào mang tên mutant của lượt
   **trước**, thì chốt so tên mutant đã bác nó rồi, nên gỡ chốt dấu phiên **không đổi màu gì** và ca
   trở thành xanh-vô-nghĩa. Dấu phiên phải là **biến DUY NHẤT** thì mới đo được chính nó.
1b. `r5xx_dau_phien_phai_sinh_moi_moi_luot`: chạy **hai** lượt có **cùng** định danh nghiệp vụ
   (cùng mutant, cùng số lần thử, cùng `rc`). Đòi **hai dấu phiên KHÁC nhau**; và cấy bản ghi của
   lượt **thứ nhất** vào kênh của lượt **thứ hai** ⇒ **`KHÔNG ĐO ĐƯỢC`**.
   **Phép làm ĐỎ — ba đột biến, và ca phải đỏ với CẢ BA:**
   (i) bộ sinh trả **hằng số**;
   (ii) bộ sinh trả **mốc thời gian độ phân giải giây**;
   (iii) bộ sinh trả một **bộ đếm tăng dần**.
   **(ii) và (iii) là lý do ca này cần thêm hai ràng buộc — thiếu chúng thì ca xanh oan:**
   - **GHIM NGUỒN CLOCK.** Ca phải chạy hai lượt dưới một clock **bị đóng băng ở cùng một tick**
     (bơm nguồn thời gian, không dựa vào việc hai lượt tình cờ rơi vào hai giây khác nhau). Không
     ghim thì đột biến (ii) cho hai dấu khác nhau và **ca xanh đúng theo quy trình đã viết** —
     tức phép đo mù đúng chỗ nó phải canh.
   - **ĐO NGUỒN NGẪU NHIÊN, không chỉ đo tính khác nhau.** Đòi bộ sinh lấy từ nguồn ngẫu nhiên mã
     hoá (`secrets` / `os.urandom`) và đếm **số lần gọi nguồn ấy = số lượt**. Đột biến (iii) cho
     mọi dấu **khác nhau** nên phép so "hai dấu khác nhau" **không bắt được nó**; chỉ phép đếm lời
     gọi mới bắt.
   **KHÔNG thay bộ sinh thật bằng fixture tự dựng hai dấu** — làm thế là quay về đo PHÉP SO (ca 1),
   đúng thứ ca này sinh ra để tách khỏi.
   **Vì sao ca này tách khỏi ca 1:** ca 1 đo **PHÉP SO** (fixture tự dựng một dấu khác); ca này đo
   **BỘ SINH**. Bỏ ca này thì một triển khai dùng dấu cố định vẫn qua được ba ca kia.

2. `r5xx_ban_ghi_thieu_dau_dong_luot`: lượt con phát đủ kết quả nhưng **không** đóng lượt. Đòi
   **`KHÔNG ĐO ĐƯỢC`** — một lượt bị giết giữa chừng có thể để lại đúng số bản ghi.
   **Phép làm ĐỎ:** bỏ phép đòi bản ghi đóng ⇒ ca ĐỎ.
3. `r5xx_ma_san_pham_phat_khong_doat_duoc_ten_ca`: mutant khiến **mã sản phẩm** (không phải thân ca)
   gọi hàm phát kết quả **trong lúc ca `T3` đang chạy**, khai mình là `T1`.
   Đòi: bản ghi sinh ra mang **`T3`** — vì khung đóng dấu tên ca **từ trạng thái của chính khung**,
   không lấy từ đối số — nên nó là **bản ghi thứ hai của `T3`** ⇒ **`KHÔNG ĐO ĐƯỢC`**; và `T1`
   **không** nhận được kết quả giả nào.
   **Phép làm ĐỎ:** cho hàm phát lấy tên ca **từ đối số người gọi** ⇒ mã sản phẩm đoạt được danh tính
   `T1` ⇒ ca ĐỎ.
   **Phạm vi ca này, khai đúng:** nó đo **một cơ chế thực thi được** (đóng dấu từ khung + đúng một
   bản ghi mỗi ca), **không** đo một ranh giới quyền — ranh giới ấy không tồn tại (xem
   *MÔ HÌNH ĐE DOẠ*). Mã cùng interpreter vẫn sửa được chính trạng thái khung; giới hạn ấy ghi ở
   `chua_do_duoc` #5 và **không** được khai là đã chặn.

**A6 (M5) — bộ chấm tự kiểm không phải một lời hứa.**
Đòi **≥ 12** ca `r5xx_` mới (A1 · A1b · A2 · A3 · A4 · A5 · A5b · **bốn** ca A5c (1, 1b, 2, 3) · ba ca biên của A5b tính
chung một) và **mỗi ca có đúng một đột biến riêng làm nó ĐỎ**. Đếm bằng
`(tên ca, tên đột biến, đã chạy, ĐỎ)`; ca nào không có đột biến riêng thì **không tính**.
**Phép làm ĐỎ:** một ca thiếu đột biến ⇒ bảng đếm lệch ⇒ khai thiếu.
**Riêng A5c(1):** ca ấy chỉ được tính khi đột biến *"bỏ so dấu phiên"* **thật sự làm nó đỏ** — một ca
xanh ở cả hai vế của đột biến **không** được tính vào `11`.

**A7 (toàn packet) — suite vẫn xanh, và số đếm KHÔNG tụt.**
`python3 ops/nhanh_don_duoc_test.py` ⇒ `8/8` cho ca, và dòng tổng kết đột biến khai
`giết = 10 · không giết = 0 · không đo được = 0` trên `len(DOT_BIEN) = 10` (đo 06:30Z 11-09-2026).
Hai số phải **BẰNG NHAU**; không tin `rc=0` suông.
**Phép làm ĐỎ:** bất kỳ mutant nào tụt khỏi `giết`.

**A8 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ **1 tệp**. Trần **dòng thêm** đã được chủ kho **BỎ** (11-09-2026, #513 comment 5637719340, sau ba lần trượt `300→429`, `500→536`, `650→658`): `so_tep = 1` là chốt **DUY NHẤT** còn hiệu lực. `so_tep` ràng buộc **lúc REVIEW** — sau khi vòng lặp review đóng, một lần `git merge master` hợp lệ sẽ làm phép đếm này lớn hơn 1 mà **không** vi phạm A8; đo phần của packet bằng `git diff --numstat <start_from_sha> HEAD -- <write_set>`.
*(Sửa 12-09-2026 theo cross-review trên PR #508: câu cũ còn khai `≤ 300` sau khi trần ấy đã bị bỏ, nên một reviewer đọc đặc tả sẽ mở finding đúng — và đã mở thật.)*
Vượt ⇒ **DỪNG và hỏi chủ kho**, không tự xin ngoại lệ.

## `hinh_dang_ke_thua`

| hình dạng | số lần | nguồn / đo lúc | ghi chú |
|---|---:|---|---|
| bộ chấm **CẤP TÍN DỤNG GIẢ** — mutant không chết đúng chốt mà vẫn tính GIẾT | **2** | `#355`/`#359`, trích `CLAUDE.md`, đọc lại 06:45Z 11-09-2026 | `#355`: khai `22/22` ⇒ phân hạng lại **19 giết thật / 3 tín dụng giả / 0 sống sót**. `#359`: bản vá vòng một **vẫn bị lừa** vì `except Exception: raise AssertionError(...)`. **Chiều: QUÁ RỘNG RÃI.** |
| bộ chấm **TỪ CHỐI GHI CÔNG** — mutant chết ĐÚNG chốt mà tính KHÔNG GIẾT | **1** | sự cố sinh ra packet này, 05:00:27Z 11-09-2026 | `T1` chết ĐÚNG; `T7` đỏ vì `[Errno 39]` vô can ⇒ tập lệch ⇒ `0/1`. **Chiều: QUÁ KHẮT KHE.** |
| con số mutant **báo chủ kho rồi phải rút lại** | **2** | trích `CLAUDE.md` 06:45Z 11-09-2026 | cả hai lần vì *"tin một tầng mà chưa thử tầng dưới nó"* ⇒ A1/A2 đòi **đột biến vào chính bản vá**. |
| lời khai rộng hơn phép đo, trong chính lượt soạn đặc tả này | **2** | 06:1xZ–06:3xZ và 11:1xZ 11-09-2026 | (a) phép thử 80 lượt cho `48/80 đỏ`; truy ra là **rig cạn file descriptor** (PID 488 giữ 19999/20000 socket vì container ký mọi commit) ⇒ **đã RÚT**. (b) bản trước gọi việc giữ handle trong một hàm là **"quyền ghi"**; phạm vi biến Python không phải miền quyền ⇒ **đã RÚT**, thay bằng *MÔ HÌNH ĐE DOẠ* + A5c(3) đo cơ chế thật. |
| đồ giả **diễn kịch bản** thay vì mô phỏng trạng thái | **1** | trích `CLAUDE.md` (`ops-don-ref`, `40/40`) 06:45Z 11-09-2026 | lý do A4 đòi đồ giả GIỮ TRẠNG THÁI và đọc **nhật ký lời gọi**. |
| **ca tự kiểm không đổi màu theo đột biến được chỉ định** | **1** | đo 11:1xZ 11-09-2026 trên chính đặc tả này | bản trước dựng A5c(1) bằng bản ghi mang tên **mutant trước**, nên chốt tên mutant đã bác nó và gỡ chốt dấu phiên **không đổi màu gì** — một ca xanh không đo gì, đúng bệnh *"ca có MẶT khác ca có ĐO"*. Nay ca ép **dấu phiên là biến DUY NHẤT**, và A6 từ chối đếm ca không đổi màu. |

**Hai hàng đầu CỐ Ý tách.** Chúng ngược chiều nhau: `#355`/`#359` là **cấp thừa**, sự cố này là **cấp
thiếu**. Cùng thuộc họ *"thước đo bị lỗi hạ tầng làm sai"* không làm chúng cùng một thuộc tính hẹp
đang đếm.

**Hệ quả: `§12` KHÔNG được kích hoạt bởi con số này.** Chiều *cấp thừa* mới ở lần **2**, chiều *cấp
thiếu* ở lần **1** — **không hình dạng nào đạt 3**. Bản vá của packet (lớp ngoại lệ riêng + neo tên
ca + kênh có mô hình tin cậy) **tự đứng bằng lập luận của nó**, và đặc tả **không** mượn một ngưỡng
chưa đạt để tự cấp thẩm quyền. Người quyết vẫn là chủ kho.

## `chua_do_duoc`

1. **Nguyên nhân gốc của `[Errno 39]`: KHÔNG BIẾT.** Đã thử, không tái hiện:
   - 12 lượt trên `27c413c` + 12 lượt trên `4b5184e`, **một lệnh hai vòng lặp cùng rig** ⇒ `DO=0`,
     `Errno39=0` cả hai ⇒ **delta `r362` = 0** (đo 06:0xZ 11-09-2026);
   - ép `gc.auto=1 autoDetach=true` ×10 ⇒ **0**; đối chứng `gc.auto=0` ×10 ⇒ **0** ⇒ giả thuyết
     *"`git push` → `receive-pack` → `gc --auto` đua với `TemporaryDirectory.cleanup()`"* **KHÔNG
     được xác nhận** (đo 06:2xZ 11-09-2026).
   Tổng **44 lượt hợp lệ, 0 tái hiện**. Khác biệt **chưa thử được**: git cục bộ **2.43.0** so với
   runner **2.55.0**. Nợ để mở, chưa có tên.
2. **Không đo được bản vá có làm lượt master xanh trở lại hay không** cho tới khi nó chạy trên CI.
   Lượt nền `8/8` sạch nên có cơ sở tin, nhưng *"có cơ sở tin"* không phải *"đã đo"*.
3. **Ước dòng thêm chưa phải phép đo.** 14 `assert` → `chot()` + lớp ngoại lệ + bộ chấm ba trạng thái
   + chạy lại có trần + **≥ 12** ca tự kiểm + **≥ 12** đột biến. Ước **≈ 150–260** dòng thêm trên tệp
   **233** dòng (đo 06:2xZ 11-09-2026). *(Câu gốc viết "trần `ADR-0044` là **300**; vượt thì **DỪNG** — A8". Trần ấy đã bị chủ kho BỎ ngày 11-09-2026 sau ba lần trượt; giữ nguyên ước tính làm hồ sơ, nhưng nó KHÔNG còn là điều kiện dừng.)*
4. **`A5c(3)` chỉ đo được ca mã sản phẩm gọi ĐÚNG hàm phát của khung.** Nếu mutant sửa thẳng trạng
   thái khung (gán lại tên ca đang chạy, hoặc thay chính hàm phát), cơ chế đóng dấu **không** chặn
   được. Không có phản chứng nào trong packet này cho đường ấy.
4b. **THU HẸP PHẠM VI, KHAI THẲNG — và nó KHÔNG phải một bản vá.** Cross-review lượt 2 mở finding
   `lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua` với phạm vi gồm **cả** mã sản phẩm đối kháng.
   Bản này **thu hẹp** phạm vi ấy xuống chống giả mạo **ngẫu nhiên** (xem *MÔ HÌNH ĐE DOẠ*), và đưa
   đường sửa khung ra `chua_do_duoc` #4/#5. Theo điều khoản chống lách của chủ kho 11-09-2026:
   **thu hẹp phạm vi là một mục `chua_do_duoc`, KHÔNG được tính là đã vá finding.** Finding ấy vì vậy
   ở trạng thái **PHẠM VI ĐÃ ĐỔI**, còn mở với phần đối kháng, và chỉ chủ kho mới đóng được nó.

5. **KHÔNG có ranh giới quyền giữa khung test và mã sản phẩm, và packet này KHÔNG tạo ra một cái.**
   `nap_tool` import mã sản phẩm vào cùng interpreter. Một ranh giới thật đòi chạy thân ca trong
   **tiến trình riêng** với kênh kết quả là fd kế thừa — đổi kiến trúc `chay_dot_bien` và gần chắc
   vượt trần **300** dòng của `ADR-0044`. **Ngoài phạm vi, khai thẳng, không khai là đã chặn.**
   Nếu chủ kho muốn ranh giới ấy thì đó là **packet khác**, và nó phải được cấp trần riêng.
