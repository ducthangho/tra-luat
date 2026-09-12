# Đặc tả packet — `CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE` (revision 1)

- `packet_id`: **`CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE`**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **1** · `generation`: 1 · soạn **14:4xZ 12-09-2026**
- `depends_on`: **`[]`** — bản mẫu đã LAND trên `master`, không chờ gì.
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

> **Đây là một PORT, KHÔNG phải một thiết kế mới.** Kiến trúc đã được thiết kế, cross-review 5 lượt,
> và **LAND** trong packet `CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN` (Issue **#513**, closed-completed
> `2026-09-12T07:19:50Z`). Tệp này chỉ nói: mang nó sang tệp thứ hai. Mọi câu ở thì hiện tại.

---

## `nguon_cap_viec`

**Sự cố đo được** qua ba vòng cross-review liên tiếp của PR **#512** / packet **#504** — lớp **F6**.
Verdict có băm: `ops/handoff/512-luot7/VERDICT.rvwin512-{6,7,8}.md`.

Bộ đo đột biến `ops/handoff/512-luot7/dotbien512.py` chạy **ngoài tiến trình** và chỉ đọc **CHUỖI** trên
stdout, nên nó phải **suy** xem một mutant chết vì chốt của ca đích hay vì một ngoại lệ vô can.
`ops/lease_publish_test.py::main()` in hai hình dạng:

```
except AssertionError as ex: hong.append((fn.__name__, str(ex)))                        # CHỐT ca đích
except Exception       as ex: hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))  # VÔ CAN
```

**Ba lượt vá, ba lượt cùng một hình dạng** (chi tiết + log: `ops/NO_KY_THUAT.md` §23):

| lượt | phép đo | đường lọt lượt SAU tìm ra |
|---|---|---|
| gốc | tiền tố **bắt buộc** trước `Error\|Exception` | `Exception:` trần · `Error:` trần |
| 6→7 | tiền tố **tuỳ chọn** | `StopIteration` |
| 7→8 | hình dạng `^<định danh>: ` | tên lớp **Unicode** · **thông điệp rỗng** · **HỒI QUY**: chốt thật `t96: …` bị xếp vô can |

Phép đo ba bản trên **cùng 10 control**, dựng trong **MỘT lệnh**, khác nhau **đúng một dòng**:

| bản | đúng | lọt (false GREEN) | hồi quy (false RED) |
|---|---|---|---|
| `v0` | `4/10` rc=1 | 6 | 0 |
| `v6` | `7/10` rc=1 | 3 | 0 |
| `v8` **(mặc định hiện tại)** | `7/10` rc=1 | 2 | 1 |

### Vì sao KHÔNG vá tiếp — lý do CẤU TRÚC

Hai miền chuỗi *"thông điệp assertion"* và *"tên lớp + thông điệp"* **GIAO NHAU**. Đo ghim trên blob
`13a2af8c…` của `36f68c7`: **`8` trong `454`** lời gọi `bang()`/`chot()` của tệp test trùng hình dạng
`^<định danh>: `, trải trên **4 ca** — `t96` (4 thông điệp), `t133`, `t136`, `t151`. Đó là tiền tố tên ca
**bình thường, có sẵn trong cây**. Một phép đo trên chuỗi **không thể** tách hai miền giao nhau.

## Đường đã có — TÁI DÙNG, đừng thiết kế lại

`ops/nhanh_don_duoc_test.py` trên **`origin/master`** đã có bản cài đặt đủ, đã land:

| thứ | ở đâu (master) | làm gì |
|---|---|---|
| `class TinHieuChotCa(AssertionError)` | `:30` | lớp tín hiệu **chỉ thân ca ném được** |
| `def chot(dieu_kien, ten_ca)` | `:34` | ném `TinHieuChotCa` |
| `GIET · KHONG_GIET · KHONG_DO_DUOC` | `:48` | **ba** trạng thái |
| `sinh_dau_phien()` | `:51` | dấu phiên **ngẫu nhiên, sinh mới mỗi lượt** |
| kênh JSONL + `_neo = {dau_phien, mutant, lan_thu}` | `:70`–`:72` | **kênh riêng**, vì lớp ngoại lệ KHÔNG qua được ranh giới tiến trình |
| `dong_luot(rc)` | `:83` | bản ghi **đóng lượt** mang `rc`, so với mã thoát THẬT của con |
| `doc_kenh` / `_doc_kenh_xac_thuc` | `:90` / `:113` | phân ba trạng thái, ~15 nhánh **fail-close** có nêu lý do |
| `DOT_BIEN_TU_KIEM` | `:2236` (khối M5 mở ở `:553`) | **đột biến tự kiểm cho CHÍNH bộ chấm** |

`ops/lease_publish_test.py` **đã có** `TinHieuChotCa` (`:4328`) và `chot()` (`:4332`) — nhưng chỉ dùng
cho khối `A0`/`t139`, và **`main()` bắt `AssertionError` rồi in `str(ex)`** nên **danh tính lớp chết
ngay tại đó**. Đó là đúng chỗ phải sửa.

## `write_set` — MỘT đường

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `ops/lease_publish_test.py` | chứa `main()` (hai nhánh in), **59** lời gọi `bang()` của 9 ca `#504`, `TinHieuChotCa`/`chot()` đã có, và — theo bản mẫu `#513` — là nơi catalogue tự kiểm phải **nằm trong** |

Không ký tự đại diện. Không đường dẫn nào khác.

**Catalogue đi VÀO tệp test**, không giữ ở `ops/handoff/**`: bản mẫu `#513` đặt `DOT_BIEN_TU_KIEM` ngay
trong tệp test, nhờ đó write set là **một** đường và bộ chấm được canh bởi cùng một suite. Thư mục
handoff là chỗ **ephemeral**, không phải nhà của một bộ đo.

**Phải đo `ai-dang-giu` lại lúc cấp** — `#504` gen 2 giữ đường này tới `2026-09-13T14:22:00Z`.
Cấp trước mốc đó ⇒ chồng lấn ⇒ phải thu hồi bằng **bia mộ hai chiều**.

## `ngoai_pham_vi`

1. **KHÔNG đụng `ops/nhanh_don_duoc_test.py`** — bản mẫu đã land, không sửa lại.
2. **KHÔNG đụng `ops/lease_publish.py`** — mã sản phẩm; nợ `S8-bo-deadline` ở đó vẫn là nợ.
3. **KHÔNG đụng `.github/workflows/**`** và **KHÔNG đụng `ops/chay_lease_publish_test.sh`**.
4. **KHÔNG nâng `timeout-minutes`**, **KHÔNG** skip/cách ly/vô hiệu ca nào.
5. **KHÔNG đổi ngữ nghĩa 155 ca hiện có** — port chỉ đổi **tín hiệu**, không đổi điều được khẳng định.
6. **KHÔNG chữa nguyên nhân Unicode/thông điệp rỗng bằng một regex khác** — mục đích của packet là
   **thôi phụ thuộc vào hình dạng chuỗi**, nên một bản vá regex thứ tư là đi ngược đặc tả.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | **59** lời gọi `bang()` của 9 ca `#504` (`t125` 3 · `t153` 5 · `t154` 10 · `t155` 4 · `t156` 11 · `t157` 6 · `t158` 7 · `t159` 4 · `t160` 9) đổi sang `chot()` ⇒ ném `TinHieuChotCa`. `bang()` **giữ nguyên** cho hạ tầng và cho các ca ngoài `#504`. | `write_set` #1 |
| M2 | `main()` phát **kênh kết quả riêng** theo bản mẫu `#513`: bản ghi mỗi ca mang `(tên ca · nhãn · chi tiết)`, neo `(dấu phiên · mutant · lần thử)`, cộng bản ghi **đóng lượt** mang `rc` — và `rc` ấy được so với **mã thoát THẬT** của tiến trình con. Tên ca do **khung** đóng dấu, không lấy từ đối số người gọi. | `write_set` #1 |
| M3 | Bộ chấm phân **BA** trạng thái. `KHÔNG ĐO ĐƯỢC` ⇒ chạy lại **ĐÚNG MỘT** lần; lần hai vẫn vậy ⇒ **ĐỎ** kèm in ngoại lệ. **Không đường nào** biến `KHÔNG ĐO ĐƯỢC` thành `GIẾT`. | `write_set` #1 |
| M4 | Catalogue `#504` (16 mutant hiện có + 10 control) **nằm trong** tệp test, theo khuôn `DOT_BIEN_TU_KIEM`. | `write_set` #1 |
| M5 | **Đột biến tự kiểm cho CHÍNH bộ chấm**, gồm ca **gỡ chốt** — gỡ ra thì một ca đích phải **ĐỎ**. Thiếu M5 là lặp lại `F6.10`. | `write_set` #1 |
| M6 | Bộ chấm **không còn đọc hình dạng chuỗi** để phân biệt chốt với ngoại lệ vô can. | `write_set` #1 |

## `nghiem_thu`

| # | tiêu chí | phép đo |
|---|---|---|
| A1 | 10 control **đều ĐẠT** | `--tu-kiem` ⇒ `10/10`, `rc=0` (hiện `7/10`, `rc=1`) |
| A2 | va chạm hình dạng chuỗi về **0** | script ghim blob ở §`nguon_cap_viec` ⇒ `0`, không còn `8/454` |
| A3 | gỡ chốt ⇒ ca đích **ĐỎ** | đột biến M5, đo `rc` và tên ca đỏ |
| A4 | catalogue 16 mutant giữ `16/16 giết thật`, **0** tín dụng giả, **0** sống sót | catalogue trong tệp test |
| A5 | suite đầy đủ `N/N` với **hai số bằng nhau** ở **CHA + `[A]` + `[B]`** — ba dòng | `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` |
| A6 | `doctrine-scan` rc=0 · `adr-song` rc=0 | `packet_loop.py` |
| A7 | dòng thêm ≤ trần `S2` của lease | `git diff --numstat <base>...HEAD -- ops/lease_publish_test.py` |
| A8 | `rc` đóng lượt **lệch** mã thoát thật ⇒ `KHÔNG ĐO ĐƯỢC` | đột biến bơm `rc` sai vào kênh |

`review_class: sensitive` ⇒ chỉ đóng khi có **`approve` tường minh**; *"0 P1 + 0 P2"* **KHÔNG đủ**.

## `chua_do_duoc`

1. **Chống giả mạo tín hiệu bởi mã CÙNG interpreter** — `#513` đã khai giới hạn này và **không** khai là
   đã chặn: kênh bảo vệ khỏi một **tập lỗi khai tường minh**, không khỏi mã sửa thẳng trạng thái khung.
   Packet này **kế thừa nguyên** giới hạn ấy, không được khai mạnh hơn.
2. **Windows** — `A3`/`A4` của `#504` vẫn `KHÔNG ĐO ĐƯỢC`; packet này không đo Windows.
3. **Chi phí thời gian của kênh** trên 155 ca — chưa đo; nếu nó đẩy `t125` vượt hạn thì đó là phát hiện
   mới, không phải cái cớ để bỏ kênh.

## Điều kiện DỪNG

- `S1` cần đường dẫn **thứ hai**.
- `S2` dòng thêm vượt trần lease.
- `S3` phải sửa `ops/lease_publish.py`.
- `S4` muốn skip / cách ly / vô hiệu một ca, hoặc nâng `timeout-minutes`.
- `S5` `ai-dang-giu` ≠ `0` lúc cấp mà **không** thu hồi được bằng bia mộ hai chiều.
- `S6` chạm trần vòng review.
- `S7` phải sửa `ops/nhanh_don_duoc_test.py` — nghĩa là bản mẫu không đủ, và **đó là câu hỏi thiết kế
  khác**, không giải trong packet này.
