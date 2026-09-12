# Đặc tả packet — `CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE` (revision 3)

- `packet_id`: **`CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE`**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **3** · `generation`: 1 · soạn **14:4xZ**, sửa **15:0xZ** (vòng 9) và **15:3xZ 12-09-2026**
  (vòng 10) của PR #512. Rev 1 có **ba** lời khai sai; rev 2 sửa chúng nhưng **`A2` mới lại sinh lỗi
  khác** — xem `§dinh_chinh`.
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
`ops/lease_publish_test.py::main()` có **BA** nhánh `except`, in **ba** hình dạng khác nhau:

```
except BoQuaNen       as ex: hong.append((fn.__name__, "bỏ qua không dẫn xuất được từ runs-on"))  # CHUỖI CỐ ĐỊNH
except AssertionError as ex: hong.append((fn.__name__, str(ex)))                                 # CHỐT ca đích
except Exception      as ex: hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))            # VÔ CAN
```

Nhánh thứ nhất in một chuỗi **cố định, không mang tên kiểu**, nên nó **không thuộc** hai hình dạng kia.
Revision 1 mô hình hoá `main()` thành *"hai hình dạng"* và **bỏ sót nhánh này** — đó là gốc của hai lời
khai sai mà vòng 9 bác.

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
`13a2af8c…` của `36f68c7`, mẫu số **493** lời gọi `bang()`/`chot()`:

- **8** lời gọi có **tiền tố TĨNH** trùng hình dạng `^<định danh>: `, trên **4 ca** — `t96` (4 thông
  điệp), `t133`, `t136`, `t151`;
- **39** lời gọi mà bộ lọc tĩnh **không đọc được** vì thông điệp có **tiền tố ĐỘNG**. Trong đó **21**
  mang đúng hình dạng va chạm `f"{x}: …"`, trên **7 ca nữa** — `t23` `t26` `t27` `t126` `t127` `t131`
  `t133`. Vòng 9 chạy thật `t131` và xác nhận nó **va chạm**.

⇒ **≥29 lời gọi trên ≥10 ca**, và 21 cái phụ thuộc **giá trị lúc chạy** nên **không quyết định được
tĩnh**. **Không có biên nào.** Đó là tiền tố tên ca **bình thường, có sẵn trong cây** — và một phép đo
trên chuỗi **không thể** tách hai miền giao nhau.

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
| 1 | `ops/lease_publish_test.py` | chứa `main()` (**ba** nhánh in), **59** lời gọi `bang()` của 9 ca `#504`, `TinHieuChotCa`/`chot()` đã có, và — theo bản mẫu `#513` — là nơi catalogue tự kiểm phải **nằm trong** |

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
| M1b | **Control dương `t96` phải mang tín hiệu RIÊNG khi port.** `t96` nằm **ngoài** chín ca `M1` nên vẫn dùng `bang()` ⇒ ném `AssertionError` **trần**; mà bản mẫu `#513` **chỉ nhận `TinHieuChotCa`**, trong khi `A1` đòi control ấy phải ra `GIẾT`. Phải nói rõ cách chuyển tín hiệu cho **riêng fixture control này** (ví dụ: đột biến control ném `TinHieuChotCa` thay vì đảo `bang()`), và **KHÔNG** được nới bộ chấm nhận **mọi** `AssertionError` — nới thế là phá chính `M1`. | `write_set` #1 |
| M2 | `main()` phát **kênh kết quả riêng** theo bản mẫu `#513`: bản ghi mỗi ca mang `(tên ca · nhãn · chi tiết)`, neo `(dấu phiên · mutant · lần thử)`, cộng bản ghi **đóng lượt** mang `rc` — và `rc` ấy được so với **mã thoát THẬT** của tiến trình con. Tên ca do **khung** đóng dấu, không lấy từ đối số người gọi. | `write_set` #1 |
| M3 | Bộ chấm phân **BA** trạng thái. `KHÔNG ĐO ĐƯỢC` ⇒ chạy lại **ĐÚNG MỘT** lần; lần hai vẫn vậy ⇒ **ĐỎ** kèm in ngoại lệ. **Không đường nào** biến `KHÔNG ĐO ĐƯỢC` thành `GIẾT`. | `write_set` #1 |
| M4 | Catalogue `#504` (16 mutant hiện có + 10 control) **nằm trong** tệp test, theo khuôn `DOT_BIEN_TU_KIEM`. | `write_set` #1 |
| M5 | **Đột biến tự kiểm cho CHÍNH bộ chấm**, gồm ca **gỡ chốt** — gỡ ra thì một ca đích phải **ĐỎ**. Thiếu M5 là lặp lại `F6.10`. | `write_set` #1 |
| M6 | Bộ chấm **không còn đọc hình dạng chuỗi** để phân biệt chốt với ngoại lệ vô can. | `write_set` #1 |

## `nghiem_thu`

| # | tiêu chí | phép đo |
|---|---|---|
| A1 | 10 control **đều ĐẠT** | `--tu-kiem` ⇒ `10/10`, `rc=0` (hiện `7/10`, `rc=1`) |
| A2 | phân hạng **KHÔNG CÒN ĐỌC nội dung thông điệp** | đột biến đặt ở **ĐÚNG RANH GIỚI của bộ chấm**: làm rỗng (hoặc biến đổi) **trường `chi_tiet` phát trên KÊNH, SAU khi `main()` đã xác định loại kết quả của ca** — giữ nguyên **tên ca · loại tín hiệu · nhãn · neo `(dấu phiên, mutant, lần thử)` · `rc`**; rồi so phân hạng trên **cùng** tập control và catalogue ⇒ **không đổi**. *(Xem `§dinh_chinh` — rev 2 đòi làm rỗng ở **hàm chốt**, và đó là SAI.)* |
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

## `dinh_chinh` — revision 1 → 2

Cross-review **vòng 9** của PR #512 bác **ba** lời khai của revision 1. Ghi lại cả câu SAI, vì một đặc tả
chỉ giữ câu đúng thì người đọc sau không biết chỗ nào từng trượt.

| # | revision 1 khai | ĐÚNG, đã đo |
|---|---|---|
| `F6.11` | `main()` có **hai** hình dạng in; `v6` lọt `4/4` lớp ngoại lệ của kho, `v8` bắt `4/4` | `main()` có **BA** nhánh. `BoQuaNen` đi nhánh riêng in **chuỗi cố định** ⇒ **cả hai bản lọt**; `TinHieuChotCa` là con `AssertionError` ⇒ cả hai lọt — **và đếm nó vào đây vốn đã SAI, vì nó LÀ lớp tín hiệu của ca đích**. `v8` loại **2/4**. Trên **ba** lớp vô can THẬT: `v6` lọt `3/3`, `v8` lọt `1/3`. |
| `F6.12` | hồi quy của `v8` **có biên**: `8/454`, bốn ca | Mẫu số **493**; `454` chỉ là tập **tiền tố tĩnh**. Thêm **21** lời gọi tiền tố ĐỘNG hình dạng va chạm trên **7 ca nữa** ⇒ **≥29 / ≥10 ca**, phần lớn **không quyết định được tĩnh**. **Không có biên.** |
| `F9.1` | `A2` đòi *"va chạm hình dạng chuỗi về 0"* | Đo sai đại lượng: `M2`/`M6` bỏ hẳn việc đọc chuỗi. `A2` nay đòi **phân hạng không đổi khi mọi thông điệp chốt thành RỖNG**. |

**Nguyên nhân gốc của cả ba là MỘT:** phiên soạn khớp regex với **chuỗi TỰ GHÉP** (`f"{ten}: m"`) thay vì
**chạy lớp ngoại lệ thật qua `main()`**. Đúng lỗi *"nghĩ ra được phép thử mà KHÔNG CHẠY nó thì phép thử ấy
không tồn tại"*. Hệ quả thực hành, và nó là ràng buộc của packet này: **mọi** tiêu chí nghiệm thu phải
chạy qua `main()` **thật**, không qua một chuỗi dựng tay.

Kèm `N42`: chủ thể của exclusion trong `#513` là **`#503`** (lease `m9-fetch-auth-exec-1-claude-20260911`),
không phải `#504`. Và **thân Issue `#513` ghi `#504` trong khi tệp spec ghi `#503`** — hai hiện vật của
cùng một packet **lệch nhau**; khai ra để người giữ `#513` biết. Exclusion vẫn có thật, chỉ đổi chủ thể,
nên suy luận *"F6 là hệ quả của một write-set exclusion"* đứng vững.

### `dinh_chinh` — revision 2 → 3 (cross-review vòng 10)

Rev 2 sửa ba lời khai sai của rev 1, **nhưng `A2` mới của nó lại SAI theo một cách khác** — và vòng 10
chứng minh bằng phép chạy qua `main()` **thật**, không bằng đọc:

| | rev 2 đòi | vì sao SAI | phép đo |
|---|---|---|---|
| `F9.1` | đổi **mọi thông điệp chốt** thành RỖNG ⇒ phân hạng không đổi | thông điệp ở một số ca **LÀ DỮ LIỆU MÀ CA KIỂM**, chưa phải chi tiết báo cáo cho bộ chấm. Làm rỗng chúng **đổi ngữ nghĩa ca** ⇒ trái `ngoai_pham_vi` #5 của chính đặc tả này | chuyển đúng 59 `bang→chot` rồi `main()` thật với `--chi-ca=t159` ⇒ **`1/1`, rc=0**; giữ nguyên điều kiện mà chỉ làm rỗng thông điệp tại `bang()`/`chot()` ⇒ **`0/1`, rc=1**. Gốc ở `ops/lease_publish_test.py:6460–6475`: `t159` gọi `t137`, bắt `TinHieuChotCa`, rồi **kiểm nội dung** chẩn đoán *"shellcheck chỉ trả 1/2 kết quả"* và nhãn timeout |

Nói cho đúng mức: **đại lượng của rev 2 ĐÚNG** (bất biến phân hạng, phù hợp `M2`/`M6`); chỉ **phạm vi
thao tác** sai. Đòi phân hạng không đổi ở chỗ ấy sẽ **đánh đỏ một port ĐÚNG**, hoặc thúc người thi công đi
gỡ chốt nội bộ của `t159` — **cấm** chữa theo đường đó.

⇒ Rev 3 dời phép biến đổi về **đúng ranh giới của bộ chấm**: `chi_tiet` **trên KÊNH**, **sau** khi `main()`
đã xác định loại kết quả. Nếu ai muốn làm rỗng **trước khi ném**, phải **xác định một tập fixture không
dùng thông điệp làm dữ liệu** và **chứng minh** phép biến đổi giữ hành vi ấy — không được giả định.

Kèm `M1b` mới: quan hệ `M1`/`M4`/`A1` quanh **control dương `t96`** mà vòng 9 nêu và rev 2 **chưa giải**.

**Bài học lặp lại ba lần trong ba revision liên tiếp, nên ghi thành ràng buộc:** rev 1 sai vì khớp regex
với chuỗi tự ghép; rev 2 sai vì đặt phép đo ở sai ranh giới. Cả hai đều là **một phép đo chưa từng chạy
qua đường thật**. Ràng buộc của packet này, đã có ở rev 2 và giữ nguyên: **mọi tiêu chí nghiệm thu phải
chạy qua `main()` THẬT** — và rev 3 thêm: **phải nói rõ nó tác động ở RANH GIỚI NÀO**, vì "chạy qua
`main()`" mà đặt sai ranh giới thì vẫn ra kết luận sai.
