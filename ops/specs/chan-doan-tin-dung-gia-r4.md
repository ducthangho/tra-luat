# `CHAN-DOAN-TIN-DUNG-GIA` — revision 4

| trường | giá trị |
|---|---|
| `packet_id` | `CHAN-DOAN-TIN-DUNG-GIA` |
| `packet_issue` | #568 |
| `revision` | 4 |
| `revision tiền nhiệm` | 3 (spec `596e1614…`, đã thi công ở PR #591) |
| `executor` | `claude` |
| `assurance_target` | `human_audited` |
| `review_class` | `sensitive` — vẫn chạm CHÍNH bộ phân hạng đột biến |
| `base` | `6c761c406cd254cd4f138f2442374badcf9bb795` (head PR #596) |

## `nguon_cap_viec`

Lượt **cross-review trên codex** (reviewer cross-provider, họ model khác executor) chạy trên
`reviewed_sha = 1486689`, verdict **`changes_requested`**. Executor đã **tái hiện bằng phản chứng
chạy được** từng finding, không nhận theo lời. Ba trong số đó thuộc closure #568 và là nội dung
của revision này. Đăng đầy đủ tại
[pull/596#issuecomment-5757583861](https://github.com/ducthangho/tra-luat/pull/596#issuecomment-5757583861).

Chỉ thị chủ kho, nguyên văn: **"Cấp r4 cho #568 đi. Những # PR nào chưa review thì cross review bởi codex đi"**.

## Vì sao đây là REVISION chứ không phải generation

`PROTOCOL_DA_PHIEN.md:300`. r3 đóng ở `596e1614…` với A13–A19. Revision này thêm tiêu chí nghiệm
thu mới và sửa mã đã thi công ở r1 lẫn r3 — đổi closure ⇒ revision.

## Ba bệnh — đều ĐÃ ĐO, đều có phản chứng chạy được

### B1 — `_khoi_chan_doan` dùng `splitlines()`, mã sản phẩm ĐOẠT ĐƯỢC tên ca

```
dau vao    : 'TU KIEM r501: DAT TU KIEM r512: DO_CHOT — injected\n'
regex CU   : set()
parser MOI : {'r512'}
```

`str.splitlines()` coi **tám** ký tự là hết dòng mà `\n` thì không:
`U+000B U+000C U+001C U+001D U+001E U+0085 U+2028 U+2029`.
Bộ đọc cũ (`re.findall(..., re.M)`) chỉ neo sau `\n`.

Hậu quả: một chuỗi **chưa từng là dòng kết quả** nay thành bằng chứng chốt. Với `rc=1` và
`dich=("r512",)`, cùng một đầu vào chuyển từ `hong` sang **`giet`** — tức **cấp `GIET` giả**.
Đây đúng lớp lỗi mà `r511` (*"ma san pham phat khong doat duoc ten ca"*) tồn tại để chặn, và
M3 của r1 tự khai là tập tên ca **không đổi** so bộ đọc cũ — lời khai ấy **sai**.

Do `18d6519` (r1) đưa vào; sống trong #572, #590, #591, #596. `r524` chỉ thử văn bản dùng `\n`
nên mù với đường này.

### B2 — hai dòng chuyển tiếp KHÔNG có đột biến nào canh

Thay cả hai `print` chuyển tiếp (nhánh `DO_KHAC` và nhánh `rc != 1`) bằng `pass`:

```
r516: DAT      r524: DAT      r525: DAT
```

Bỏ trọn phần chuyển tiếp ở hai nhánh ấy mà mọi ca liên quan vẫn xanh. **Đó chính là bệnh #568
cam kết khoá**, và A1/A2 chưa khoá được nó ở lớp cha. `r524` chỉ đo hai helper; `r525` đo nhánh
cuối; `r516` kiểm phân hạng nhưng cho `stderr` rỗng.

### B3 — `r526` xác thực HÌNH DẠNG, không xác thực DANH TÍNH

Làm **nguồn chạy** bẩn (bỏ tiền tố raw của một docstring — đo được 1 cảnh báo escape) rồi cho
`ma` đọc một hằng sạch dài hơn 50 000 ký tự có chứa tên hàm `r526_…`:

```
nguon CHAY that su co 1 canh bao escape-sequence (tuc BAN)
r526: DAT
```

`len(ma) > 50_000` và *"tên hàm có trong `ma`"* chỉ xác thực hình dạng. Một bản chép sạch thoả cả
hai. Lời khai A14 (*"chặn đường đọc bản chép sạch"*) **rộng hơn** phép đo.

## §4 — Mục tiêu

| | |
|---|---|
| **M10** | `_khoi_chan_doan` nhận **đúng bằng** tập dòng mà bộ đọc cũ neo `\n` nhận. Tám ký tự tách dòng Unicode **không** được coi là hết dòng |
| **M11** | Mỗi nhánh in chuyển tiếp có **một đột biến RIÊNG** canh nó. Bỏ nhánh nào cũng phải có ca ĐỎ |
| **M12** | `r526` xác thực **danh tính** nguồn đọc, không chỉ hình dạng |

**Hướng cho M12, vì nó dễ đi sai.** Không thể chứng minh *"văn bản này là tệp đang chạy"* từ chính
văn bản. Thứ **chứng minh được** là: phép đọc chưa bị thay. Dùng **hai đường đọc độc lập** nguồn
của chính module đang chạy và đòi chúng **bằng nhau từng byte**; một đột biến thay một đường vẫn
vỡ vì đường kia không đổi. Đây là lời khai **hẹp hơn và đúng**, thay cho lời khai rộng của A14.

## §5 — Nghiệm thu

| | tiêu chí | đột biến phải giết |
|---|---|---|
| **A20** | Trên một **bộ đầu vào có đủ tám ký tự tách dòng Unicode**, tập tên ca `_khoi_chan_doan` trả về **bằng đúng** tập `re.findall(..., re.M)` trả về. Khai bằng hai tập bằng nhau, không bằng `rc` | Đổi phép tách dòng về `splitlines()` ⇒ ca ĐỎ |
| **A21** | Đầu vào mang `U+2028` + một dòng `DO_CHOT` giả ⇒ `_khoi_chan_doan` trả **rỗng**, và cặp `(giet, hong)` **không đổi** so với khi không có ký tự ấy | Nới phép tách ⇒ cặp lệch ⇒ ca ĐỎ |
| **A22** | Bỏ dòng chuyển tiếp của nhánh `DO_KHAC` ⇒ có ca ĐỎ. Đột biến **riêng**, `dich` khai đúng | thiếu đột biến ấy ⇒ `thieu` khác rỗng |
| **A23** | Bỏ dòng chuyển tiếp của nhánh `rc != 1` ⇒ có ca ĐỎ. Đột biến **riêng**, phân biệt được với A22 **bằng đầu vào** | như trên |
| **A24** | `r526` đọc nguồn bằng **hai đường độc lập** và đòi bằng nhau từng byte. Thay **một** đường bằng hằng ⇒ ca ĐỎ | hai đột biến, mỗi đường một cái |
| **A25** | Phân hạng **không đổi**: cặp `(giet, hong)` bằng đúng cặp của nền trên cùng bảng đầu vào | đổi một nhánh phân hạng ⇒ cặp lệch |
| **A26** | Ca mới nằm trong `NHOM_BAT_BUOC`, có **đột biến riêng**, `SAN_NHOM` cập nhật | bỏ đột biến của ca mới ⇒ `thieu` khác rỗng |
| **A27** | Toàn bộ tệp ⇒ `rc=0`, `TU KIEM N/N` **hai số bằng nhau**, `dot bien giet M/M` **hai số bằng nhau** | bất kỳ ca nào đỏ |
| **A28** | Delta so nền `6c761c4`: nền đã đo `rc=0 · 28/28 · 89/89`; ứng viên `rc=0` và `dot bien giet = 89 + (số đột biến mới)`, hai vế dựng trong **MỘT** lệnh | hai vế dựng ở hai thời điểm ⇒ phép đo vô hiệu |

## §6 — `ngoai_pham_vi`

- **P1 của lượt review về `r508`** — trạng thái thứ ba ở mức ca. Đó là closure của **#593**, không
  phải #568, và nó là một **câu hỏi kiến trúc** đang chờ chủ kho: bộ phân hạng chỉ có
  `DAT`/`DO_CHOT`/`DO_KHAC`, không có nhãn `KHÔNG ĐO ĐƯỢC` ở mức ca. **KHÔNG đụng vào trong r4.**
- Đổi hướng cắt hoặc giá trị `TRAN_CHAN_DOAN` — vẫn ngoài phạm vi, y như r3.
- `CASE T6`; nguyên nhân (A) của `r506` — nợ mở, chưa có chủ.
- Bốn điểm `invalid escape sequence` còn lại của kho — nợ riêng.
- Mọi tệp ngoài `write_set`, kể cả sửa tạm rồi hoàn nguyên.

## §7 — `write_set`

```yaml
write_set:
  - ops/nhanh_don_duoc_test.py
```

Một đường, trong trần `≤ 3 tệp` của `ADR-0044:5` cho class `sensitive`.

Đường đã sạch trước khi cấp: #593 **tự nhả** bằng bia mộ hai chiều
`dau-phien-trung-lam-do-cong-r1-g2-bia-mo`, rồi `ai-dang-giu` trả `NGƯỜI_GIỮ 0`.

`start_from_sha` neo vào head #596 chứ không vào master: r4 xây **trên** r1+r2+r3+#593. Cắt từ
master sẽ làm mất cả bốn khỏi cây làm việc, và A28 phải đo trong **đúng** bảng đột biến mà #593
để lại (89 mục).

## §8 — `hinh_dang_ke_thua`

| hình dạng | trước | **r4** | vì sao |
|---|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 4 | **6** | B1: M3 của r1 khai *"tập tên ca không đổi"* — sai, đo được. B3: A14 khai *"chặn đường đọc bản chép sạch"* — rộng hơn phép đo |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 3 | **4** | B2: hai nhánh chuyển tiếp không có đột biến nào canh, nên các ca liên quan xanh mà không đo gì ở đó |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 2 | 2 | không tái phát |

**Cả ba hình dạng đều đã vượt xa ngưỡng "lần thứ ba ⇒ DỪNG và hỏi".** Executor đã dừng và hỏi;
r4 tồn tại là **kết quả** của lần dừng ấy, và cả ba bệnh đều do **một reviewer khác họ model** tìm
ra chứ không phải executor tự thấy. Đó là dữ kiện nên được đọc thẳng: ba lượt tự kiểm của chính
executor đã **không** bắt được chúng.

**Cơ hội tái phát đã biết, cho chính r4:** A20 so hai tập trên "một bộ đầu vào có đủ tám ký tự".
Nếu bộ đầu vào ấy do executor tự soạn và **thiếu** một ký tự, chốt sẽ xanh mà vẫn hở đúng ký tự
đó. Bộ đầu vào phải được **sinh từ chính danh sách tám ký tự**, không chép tay, và phải có một
đột biến bỏ bớt một ký tự khỏi danh sách để chứng minh chốt bắt được.
