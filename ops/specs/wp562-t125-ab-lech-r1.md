# WP562 T125-AB-LECH-CHUA-RO — spec r1 (packet revision 1 / generation 1)

> ĐẶC TẢ ĐÓNG BĂNG. KHÔNG phải lease, KHÔNG cấp việc. Phải có lease còn hiệu lực
> (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4) thì mới được bắt tay.
>
> **Đây là packet ĐO, không phải packet VÁ.** Sản phẩm là một biên bản có số. Một bản vá làm
> `t125` xanh **không** phải sản phẩm của packet này, và sẽ bị từ chối.
>
> Mọi con số ghi kèm ĐƠN VỊ (L1) và THỜI ĐIỂM ĐO (L5).

## packet_id · packet_issue

| trường | giá trị |
|---|---|
| `packet_id` | `WP562-T125-AB-LECH-CHUA-RO` |
| `packet_issue` | **562** — *"ĐO vì sao A/B toàn suite lệch; đã chặn cổng 3 lần"*, `open`, tạo `2026-09-18T16:22Z` |
| `revision` / `generation` | 1 / 1 |
| `mission_issue` | `KHONG_CO` |
| `base_sha` | `eb15657dae7a5f0e494a1dca50fdd6d8a55ed7d3` (`origin/master`, đo `16:25Z 18-09-2026`) |
| `chay song song voi` | **#541** (`wp541-path-r2-g2-antigravity`, hiệu lực tới `2026-09-19T15:54Z`) — write set rời hẳn |

## nguon_cap_viec

**Issue #562**, cộng chỉ thị chủ kho phiên điều phối `18-09-2026`, nguyên văn:
*"mở packet riêng cho t125"* · *"soạn spec cho #562"*.

## review_class

`risk` = `review_class` = **`sensitive`**, và đây là phép ĐO chứ không phải lời khai:
`_tinh_lop_tu_write_set` trả `sensitive` cho **mọi** đầu vào đã thử — `_BANG_LOP` có **7** mục, cả
7 `sensitive`, và mặc định của `next()` cũng `sensitive`, nên giá trị khởi tạo `"routine"` trong hàm
**không bao giờ tới được** (đo `15:40Z 18-09` trên `origin/master`). Khai lệch thì cổng bác `rc=10`.

`assurance_target`: **`human_audited`**. `antigravity` xuất hiện **0** lần trong PROTOCOL nên chưa
phải provider hợp lệ cho `cross_approved`; và một phiên `claude` chấm thì trần cứng là
`advisory_review`.

## write_set

Hai đường, **cả hai là tệp MỚI**:

1. `ops/do_t125_ab_lech.py` — bộ đo
2. `ops/DO_VI_SAO_T125_AB_LECH_20260918.md` — biên bản

**Vì sao không lấy `ops/lease_publish_test.py`:** packet này KHÔNG sửa `t125`, nên nó không cần
quyền ghi lên thứ nó đang đo. Hai đường ấy thuộc vùng tranh chấp `#541`/`#548`. Hệ quả có chủ đích:
#562 **chạy song song** #541, không xếp hàng sau.

## hien_trang_da_do

### Ba lần chặn — đo được

| # | khi nào | ca lệch | số |
|---|---|---|---|
| 1 | CI `e6feddb`, **12-09-2026** | `t139` | `S8-bo-deadline` **sống** ở vế B. Ghi sẵn trong docstring `_phan_loai_lech_ab` |
| 2 | Windows chủ kho, **18-09-2026** | `t156_han_NGOAI_khong_nho_hon_tong_han_TRONG_va_duoi_tran_cung` | không-actor `143/154` · có-actor `144/154` |
| 3 | CI đăng lease #541 g2, **18-09 15:54:30Z** | `t139` | không-actor `157/157` `rc=0` · có-actor `156/157` `rc=1` |

Lần 3 chặn một việc thật: bước `đăng` bị `skipped`, lease `wp541-path-r2-g2-antigravity` đã cấp mà
không có bản chiếu; phải chạy lại (`attempt 2`, `16:13Z`) mới đăng được.

### Cơ chế của `t125` — đọc từ mã, không suy

```python
CO_AB = "--ab-con-noi-bo"          # :32   — lượt con thấy cờ này thì RETURN, chống đệ quy
if CO_AB in sys.argv: return       # trong t125
...
with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(max_workers=2) as pool:
    #   A = nền, đã bỏ GITHUB_ACTOR
    #   B = dict(nen, GITHUB_ACTOR="ke-la-mat-khong-co-quyen")
do = frozenset(re.findall(r"(?m)^  ĐỎ  (\w+):", out))      # so bằng TẬP TÊN, không bằng số
```

**Hai vế chạy SONG SONG**, `max_workers=2`. Đó là mấu chốt bị bỏ qua cho tới nay: thiết kế A/B
tuyên bố *"khác nhau ĐÚNG một biến `GITHUB_ACTOR`"*, nhưng trên thực tế **hai vế còn khác nhau ở
tải và ở lịch biểu CPU** — và cả ba ca lệch đều thuộc **họ HẠN CHÓT**:

- `t156` đo quan hệ giữa **hạn ngoài** của `t125` và **tổng hạn trong**;
- `S8-bo-deadline` đột biến đúng chốt `if con <= 0` → `if False`, seam `KhoObject._con_thoi_gian`,
  ca đích `t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline`.

**Đó là một HÌNH DẠNG đo được, KHÔNG phải nguyên nhân đã chứng minh.** Ba điểm dữ liệu cùng một họ
là lý do để đi đo, không phải kết luận để ghi vào đâu.

### Luật của kho áp thẳng vào packet này

`_phan_loai_lech_ab` ra lệnh, nguyên văn:

> *"Một lần đo lại khớp, **kể cả tuần tự**, cũng không loại trừ rò actor phụ thuộc thứ tự ca hoặc
> tải. Đo lại một ca riêng còn thay đổi ngữ cảnh của phép đo TOÀN SUITE."*
>
> *"…`t125` phải ĐỎ ngay, không chạy thêm chẩn đoán thiếu ngân sách tổng, thu hồi cây hoặc tee rồi
> **gọi nó là chập chờn**."*

**Nhãn `"chập chờn"` / `"flake"` bị CẤM làm kết luận.** Trạng thái đúng là
`LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN`. Đính chính kèm: phiên điều phối đã dùng nhãn ấy trong
`ops/specs/wp541-path-toi-thieu-theo-nen-r3.md:287` và trong bản đầu của
`ops/prompts/wp541-exec-2-antigravity-20260918.md`; prompt đã sửa và ghi đính chính, spec r3 giữ
nguyên vì sửa nó đổi `spec_hash`. **Nhãn ấy sai ở cả hai chỗ.**

## muc_tieu

Mỗi mục chiếu vào ĐÚNG MỘT đường dẫn trong `write_set` (L2).

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Bộ đo chạy **BỘ TEST HIỆN CÓ** như tiến trình con, có kiểm soát, **KHÔNG sửa một byte** của nó. Mỗi lượt con nhận cờ `--ab-con-noi-bo` để `t125` tự `return` — thiếu cờ ấy thì mỗi lượt lại đẻ thêm hai lượt toàn suite. | `ops/do_t125_ab_lech.py` |
| **M2** | **PHÉP THỬ RỖNG (A/A)** — hai vế **giống hệt nhau** về môi trường, vẫn chạy **song song** như `t125` làm. Đây là chốt chẩn đoán trung tâm: nếu **A/A cũng lệch** thì `GITHUB_ACTOR` được **loại trừ**, và nguyên nhân nằm ở lịch biểu/tải/thứ tự. | `ops/do_t125_ab_lech.py` |
| **M3** | **ĐỔI CHỖ HAI VẾ** (A mang actor, B không) — tách *"lệch theo NHÃN actor"* khỏi *"lệch theo VỊ TRÍ khe chạy"*. | `ops/do_t125_ab_lech.py` |
| **M4** | **BIẾN THỂ TUẦN TỰ** — chạy hai vế nối tiếp thay vì song song. Không phải để "đo lại cho khớp" (mã đã cấm đọc thế), mà để **đo trực tiếp giả thuyết tải**: nếu lệch biến mất khi hết tranh CPU thì đó là số liệu về tải, không phải bằng chứng vô can của actor. | `ops/do_t125_ab_lech.py` |
| **M5** | **TẦN SUẤT** — mỗi cấu hình chạy `N ≥ 10` lượt, báo `n/N` với **cả hai số**. Một lần khớp không chứng minh gì; mã đã nói thẳng. | `ops/do_t125_ab_lech.py` |
| **M6** | Biên bản trả lời **bốn câu của Issue #562**, mỗi câu bằng **số** hoặc bằng **`KHÔNG ĐO ĐƯỢC` kèm lý do**. Không làm tròn, không suy. | `ops/DO_VI_SAO_T125_AB_LECH_20260918.md` |

### Thiết kế bảng cấu hình — tối thiểu, và vì sao từng dòng tồn tại

| cấu hình | vế A | vế B | song song? | trả lời câu gì |
|---|---|---|---|---|
| `AB-song-song` | không actor | có actor | có | tái hiện đúng `t125` |
| **`AA-song-song`** | không actor | **không actor** | có | **actor có liên quan không** |
| `BB-song-song` | có actor | có actor | có | đối xứng của trên; loại trừ "chỉ vế không-actor mới lệch" |
| `AB-doi-cho` | có actor | không actor | có | lệch theo NHÃN hay theo KHE |
| `AB-tuan-tu` | không actor | có actor | **không** | tải/tranh CPU đóng vai gì |

**`AA-song-song` là dòng quan trọng nhất.** Nếu nó lệch, mọi tranh luận về actor kết thúc.

## nghiem_thu

Mỗi tiêu chí nêu PHÉP ĐO LÀM NÓ ĐỎ (L3). Đây là packet ĐO, nên tiêu chí nói về **dụng cụ đo**,
không nói về việc `t125` có xanh hay không.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | Lượt con **không đẻ đệ quy**: mỗi lượt con nhận `--ab-con-noi-bo`, và `t125` trong lượt con kết thúc dưới **5 giây** (đơn vị: giây tường). | **Đột biến:** bỏ cờ ⇒ thời lượng mỗi lượt con nở gấp bội và N1 ĐỎ. Không có chốt này thì một lượt đo 10 lượt × 2 vế thành 30 lượt toàn suite. |
| **N2** | `AA-song-song` được chạy và báo cáo **RIÊNG**, không tái dùng kết quả của `AB-song-song`. | **Đột biến:** cho `AA` trả lại đối tượng kết quả của `AB` ⇒ ĐỎ. Chốt này chặn đúng cách một phép thử rỗng đi chết. |
| **N3** | So bằng **TẬP TÊN** ca đỏ, không bằng số đếm. Phản chứng dựng sẵn: hai lượt cùng `n/m` mà tập đỏ khác nhau ⇒ phải báo **LỆCH**. | **Đột biến:** đổi phép so sang `len(do_a) == len(do_b)` ⇒ ca phản chứng ĐỎ. Đây là bệnh *"bất biến còn đúng, số hạng đã trôi"* mà kho đã trả giá. |
| **N4** | **FAIL-CLOSE**: lượt con quá hạn, chết, hay không đọc được dòng tổng kết ⇒ ghi `KHÔNG ĐO ĐƯỢC` cho lượt ấy và **KHÔNG** tính nó là "khớp". | **Đột biến:** cho nhánh quá hạn rơi vào nhánh "khớp" ⇒ ĐỎ. Ba trạng thái, không phải hai — `None ≠ False`. |
| **N5** | Bộ đo **từ chối in kết luận** khi `N` thực tế nhỏ hơn `N` đã khai, hoặc khi có bất kỳ lượt `KHÔNG ĐO ĐƯỢC` nào chưa được khai trong biên bản. | **Đột biến:** hạ chốt xuống "có ít nhất 1 lượt là in" ⇒ ĐỎ. Chống đúng thói lấy một lượt đẹp làm kết luận. |
| **N6** | Bộ đo **neo cây đo**: từ chối chạy khi băm của `ops/lease_publish.py` **hoặc** `ops/lease_publish_test.py` khác băm đã ghim trong biên bản. | **Đột biến:** bỏ phép neo ⇒ ĐỎ. #541 đang sửa đúng hai tệp ấy; số đo trên hai cây khác nhau **không so được với nhau**, và trộn chúng là tự sinh kết luận giả. |
| **N7** | `git diff --numstat` so `eb15657`: **≤ 2 tệp và ≤ 300 dòng thêm**. | Vượt ⇒ DỪNG, handoff, không tự nới. |

### Cái KHÔNG phải tiêu chí

- **`t125` xanh KHÔNG phải tiêu chí.** Nếu nó tình cờ xanh suốt `N` lượt thì đó là **một số liệu**
  (`0/N` lệch), không phải nghiệm thu.
- **Tìm ra nguyên nhân KHÔNG phải tiêu chí.** Packet có thể kết thúc bằng *"đã loại trừ actor, chưa
  xác định được cơ chế còn lại"* và vẫn `approve` — miễn là mỗi câu có số hoặc có `KHÔNG ĐO ĐƯỢC`.
  Một packet ĐO mà bị ép phải ra nguyên nhân là packet sẽ bịa ra nguyên nhân.

## ngoai_pham_vi

| # | cố ý KHÔNG làm | lý do |
|---|---|---|
| 1 | **Sửa `t125`** — không ổn định hoá, không nới hạn, không thêm retry, không hạ xuống cảnh báo | Cổng đang làm ĐÚNG việc của nó là ĐỎ khi hai vế lệch. Sửa nó trước khi biết nguyên nhân là bịt một cái chuông báo cháy. |
| 2 | **Sửa `t139` / `t156` / `t131`** | Chưa có nguyên nhân. |
| 3 | **Chạm `ops/lease_publish.py`, `ops/lease_publish_test.py`** | Thuộc #541 (lease `wp541-path-r2-g2-antigravity`). Chạm là tạo cửa sổ hai writer. |
| 4 | Sửa `ops/specs/wp541-path-toi-thieu-theo-nen-r3.md` | Đặc tả đã đóng băng của packet khác. Nhãn `"chập chờn"` ở `:287` sai, nhưng sửa nó là việc của #541, qua revision. |
| 5 | Workflow, ruleset, manifest, credential | Ngoài mọi packet đang mở. |
| 6 | Chạy CI Windows bằng tay | `manual_ci_budget: 0`. |

## chua_do_duoc

1. **Nền nào đo.** Cả ba lần chặn: một trên Windows của chủ kho, hai trên `ubuntu-latest`. Chưa biết
   lệch có phụ thuộc nền không. Bộ đo phải **ghi nền và ghi tải**, và biên bản phải nói rõ số liệu
   thuộc nền nào — đừng gộp.
2. **Ngân sách thời gian thật.** Một lượt toàn suite đo được `~115 s` trên ubuntu (`M4 lượt 4`) và
   `~350 s` trên Windows (`AB_SUITE_DO_DUOC_GIAY = 350`, từ `t125 = 344.438 s`). Với 5 cấu hình ×
   `N=10` × 2 vế, cận dưới thô là `100` lượt con. Trên ubuntu ≈ **3,2 giờ**; trên Windows ≈ **9,7
   giờ**. Con số ấy **chưa đo**, mới là phép nhân — executor phải đo một lượt thật rồi báo lại trước
   khi chạy trọn, và **được phép hạ `N`** nếu khai thẳng `N` thật trong biên bản.
3. **`AB_HAN_GIAY` có đủ không.** Docstring ghi *"M4 lượt 4 ghi t125=344.438 s, không chứng minh trần
   đủ"*. Nếu bộ đo gặp quá hạn, đó là **số liệu**, không phải lý do nới trần.
4. **Quan hệ với `#541`.** #541 đang sửa `ops/lease_publish.py` và `..._test.py`. Số đo trước và sau
   bản vá ấy **không so được với nhau** — đó là lý do N6 tồn tại. Nếu #541 land giữa chừng thì phải
   ghi mốc và **tách bảng số theo băm cây**, đừng gộp.

## Ràng buộc thi công

- **KHÔNG sửa `t125`**, không sửa bộ test, không chạm write set của #541.
- **KHÔNG chạy CI Windows bằng tay**, không `workflow_dispatch`.
- **KHÔNG tự merge, tự approve, tự review.**
- **KHÔNG viết nhãn `"chập chờn"` / `"flake"` như một kết luận** trong biên bản. Trạng thái đúng là
  `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN`.
- **KHÔNG viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit**, kể cả khi trích dẫn.
- **Đọc `rc` TRỰC TIẾP**, đừng qua pipe.
- **`core.abbrev = 7`** khi chạy gate.
- Đột biến (cho N1–N6) chạy trên **BẢN SAO TẠM**, không bao giờ trên tệp thật.
