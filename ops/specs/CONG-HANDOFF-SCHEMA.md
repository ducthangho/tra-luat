# ĐẶC TẢ ĐÓNG BĂNG — `CONG-HANDOFF-SCHEMA`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `CONG-HANDOFF-SCHEMA`
`packet_issue`: `CHUA_CO` — người giữ kho chưa mở. **Không bịa số.**

`review_class`: **`sensitive`** — packet sửa `CLAUDE.md` (doctrine) và dựng một cổng mà các
phiên sau phải qua. Phân lớp theo **hệ quả**, không theo đường dẫn bị chạm.

## `nguon_cap_viec`

**KHÔNG phải packet khắc phục một sự cố LIVE.** Nguồn là phiên thi công `CI-BANG-PHU-THUOC`
(#245) ngày 22-08-2026: cross-review trên PR #253 nêu một finding **P1** rằng handoff thiếu
khối máy đọc được của protocol §7. Finding đúng. Nhưng lúc đi kiểm để vá, phép đo cho thấy nó
**không phải sơ suất của một phiên** — nó là trạng thái của **cả kho**.

Người giữ kho chỉ đạo trực tiếp trong phiên: *"Soạn thành packet: Issue + spec cho các mục trên."*

## Bằng chứng — ĐO, không suy

### B1. Khối §7 gần như không tồn tại trong kho

`docs/PROTOCOL_DA_PHIEN.md` §7 mở đầu bằng *"Executor luôn xuất handoff máy đọc được"* rồi cho
nguyên một schema YAML. Đo trên `master` = `79de656`:

```
python3 - <<'PY'   # doi chieu tap truong voi schema §7, bo hint_provenance (§7 khai TUY CHON)
... quet ops/handoff/*.md, tim khoi ```yaml co schema_version == 1 va co packet_id ...
PY

=> 1/11 handoff co khoi schema-v1
```

**Và cái `1` ấy là tệp vừa được viết hôm nay để vá đúng finding này.** Trước 22-08-2026 con số
là **0/10**. Một mục protocol dùng chữ *"luôn"* mà tuân thủ bằng không trong suốt vòng đời kho.

### B2. Có khối YAML trong handoff KHÔNG PARSE ĐƯỢC — nặng hơn "thiếu"

`ops/handoff/phien-dieu-phoi-20260821-handoff.md` có **ba** khối ```yaml. Khối 1 parse được nhưng
mang khoá tự chế (`do_luc`, `nhanh`, `commit_gioi_thieu_bam_spec`…), **không phải** schema §7.
Khối 2 và 3 **ném lỗi cú pháp**:

```
khoi 2: PARSE HONG — while scanning a block scalar ... expected a comment or a line break
khoi 3: PARSE HONG — while scanning a block scalar ... expected a comment or a line break
```

Khác biệt đáng giá: handoff **thiếu** khối thì máy biết là thiếu; handoff **có** khối hỏng thì
máy đọc vào rồi mới chết, và người viết tưởng mình đã tuân thủ vì "có YAML rồi". Đây là ca
*"CÓ MẶT khác DÙNG ĐƯỢC"* ở tầng dữ liệu.

### B3. Bảng bằng chứng có thể XANH VỀ SỐ mà SAI VỀ TÊN

Cùng lượt review trên #253, finding **P2**: bảng `passed/failed/skipped` của handoff kể
`gate lifecycle selftest (nen khong co cgroup)` vào nhóm bỏ qua của Windows. Đo lại từ dữ liệu
job của lượt `32591958672`:

| bước | ubuntu | windows |
|---|---|---|
| `#12 bo ca gate chay TRONG cgroup (Linux)` | success | **skipped** |
| `#13 gate lifecycle selftest (nen khong co cgroup)` | **skipped** | success |

Hai bước **BÙ NHAU** (`ci.yml` neo `#13` bằng `runner.os != 'Linux'`). Câu văn nêu **năm** mục
dưới một con số ghi **bốn** — trong khi `28+3 = 27+4 = 31` vẫn khớp, nên **mọi phép kiểm bằng số
học đều xanh**. Chỉ ai đọc TÊN mới thấy.

Đây là anh em của *"cổng xanh nhờ `rc=0`"*, dịch lên một tầng: **bằng chứng xanh nhờ phép cộng**.
Và nó nguy hiểm hơn một bảng chỉ có số, vì bảng có tên *trông như* đã kiểm tới từng bước.

### B4. Bảng đột biến không kèm phép thay thì không tái hiện được

Cùng phiên, khi đo lại toàn bộ bảng đột biến thay vì chép từ ghi chép review, **một ô sai** lộ
ra: đột biến "bỏ qua nội dung gói" được đăng là giết `n1 n5 n6`, đo lại cho `n1 n5`. Và trong
chính lượt đo ấy, một phép thay **neo trượt** vì thừa thụt đầu dòng — nó **im lặng** thành
"không ca nào chết", tức một bảng đột biến toàn màu xanh cho một chốt chưa từng bị tắt.

Không có nguyên văn `cu → moi` thì người sau không dựng lại được, nên bảng ấy là **lời khai**.

## `write_set`

Đúng ba tệp:

- `ops/handoff_song.py` — cổng
- `ops/handoff_song_test.py` — phản chứng
- `CLAUDE.md` — hai dòng doctrine mà cổng **không** cưỡng chế được (B3, B4)

## `ngoai_pham_vi`

- `docs/PROTOCOL_DA_PHIEN.md` — packet này **thi hành** §7, không sửa §7.
- `.github/workflows/ci.yml` — nối cổng vào CI là việc riêng; xem `hinh_dang_ke_thua`.
- 10 handoff cũ — **KHÔNG viết lại**. Chúng là hồ sơ lịch sử; sửa hồi tố là làm hỏng bằng chứng.
- `ops/lease_publish.py` — write set ấy **đang bị giữ** bởi `LEASE-HOI-TOAN-KHO`.

## `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| **M1** | `handoff_song.py <đường-dẫn|thư-mục>` kiểm: có đúng một khối ```yaml mang `schema_version: 1`, parse được, đủ 20 trường bắt buộc của §7 (`hint_provenance` TUỲ CHỌN — §7 khai thẳng thế) | `ops/handoff_song.py` |
| **M2** | **BA trạng thái**: `dat` · `thieu_truong` · **`khong_doc_duoc`** (khối tồn tại nhưng ném lỗi cú pháp — ca B2). Trạng thái thứ ba làm cổng **ĐỎ**, không được gộp vào "thiếu" | `ops/handoff_song.py` |
| **M3** | **Miễn trừ là DANH SÁCH CHO PHÉP ĐÓNG BĂNG**, không phải luật "tệp cũ thì tha": hằng `_MIEN_TRU` liệt kê đúng 10 tên tệp có sẵn lúc land. Không suy theo ngày, không suy theo git log | `ops/handoff_song.py` |
| **M4** | **BÁNH CÓC**: một ca đòi `_MIEN_TRU` **không lớn hơn 10**. Thêm tên mới vào đó ⇒ ĐỎ. Miễn trừ chỉ được **co lại** | `ops/handoff_song_test.py` |
| **M5** | `tested_sha` và `head_sha` phải là commit **tra được** (`git cat-file -e`); tra không được ⇒ `khong_doc_duoc`, không phải `dat` | `ops/handoff_song.py` |
| **M6** | Hai dòng doctrine: (a) bảng `passed/failed/skipped` phải liệt kê **TÊN** dẫn xuất từ dữ liệu job, và bước neo `runner.os` **bù nhau** chứ không cùng bị bỏ; (b) bảng đột biến phải kèm **nguyên văn** phép thay, neo khớp đúng một lần, trượt thì DỪNG | `CLAUDE.md` |
| **M7** | Phản chứng cho từng luật + đột biến giết đúng ca của nó | `ops/handoff_song_test.py` |

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo làm nó ĐỎ**.

| # | nghiệm thu | phép đo làm ĐỎ |
|---|---|---|
| **N1** | Cổng ĐẠT trên handoff của #245 | đột biến xoá một trường bắt buộc khỏi khối ⇒ ĐỎ, thông điệp **nêu tên trường** |
| **N2** | Cổng ĐỎ trên 10 handoff cũ **nếu gỡ miễn trừ** | đột biến `_MIEN_TRU = set()` ⇒ 10 ca ĐỎ. Không có phép đo này thì không biết cổng đang đo hay đang tha tất |
| **N3** | Khối hỏng cú pháp ⇒ `khong_doc_duoc`, **không** ⇒ `dat` | ca dựng khối scalar hỏng như B2; đột biến gộp `khong_doc_duoc` vào `thieu_truong` ⇒ ca ĐỎ |
| **N4** | `hint_provenance` vắng **vẫn ĐẠT** — chiều **BẮT OAN** | ca chiều-tha; giết nó bằng đột biến **SIẾT THÊM** (đưa `hint_provenance` vào tập bắt buộc), và đột biến ấy phải **KHÔNG** làm N1 đỏ |
| **N5** | Bánh cóc có răng | đột biến thêm một tên vào `_MIEN_TRU` ⇒ chỉ ca M4 ĐỎ |
| **N6** | `tested_sha` bịa ⇒ ĐỎ | ca đặt `tested_sha` là 40 ký tự hex không phải commit |
| **N7** | delta so master = 0 cho `packet_loop_test.py` và `lease_publish_test.py` | nền master đo **trong worktree của chính kho** |

## `hinh_dang_ke_thua`

Packet này **KHÔNG tự nối vào `ci.yml`** — cùng lý do đã trả giá ở `CI-BANG-PHU-THUOC`: cổng land
xong mà không ai gọi thì nó nằm im. Nhưng bài học ấy nói **phải có bước nối**, không nói **phải
nối trong cùng packet**. Việc nối là slice kế tiếp, và nó gộp được với slice nối `ci_phamvi_test.py`
đang chờ (`ops/handoff/ci-noi-bang-vao-gate-BAN-GIAO.md`) vì cùng chạm đúng một chỗ trong `ci.yml`.

**Điều kiện mọc của slice nối:** cả hai cổng đã có hiện vật trên `master`.

## `chua_do_duoc`

- **Cổng không đo được B3 và B4.** Nó biết trường có mặt hay không; nó **không** biết tên bước
  trong bảng có đúng với dữ liệu job không, cũng không biết bảng đột biến có kèm phép thay thật
  không. M6 vì thế là **kỷ luật đọc**, và đặc tả khai thẳng thay vì đặt tên cổng to hơn phạm vi
  nó cưỡng chế được — bài học *"PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC"*.
- **Không đo được "handoff có TRUNG THỰC không".** Khối đủ trường vẫn có thể khai số bịa. Cổng
  này chặn *thiếu* và *hỏng*, không chặn *sai*.
- **Con số 10 của `_MIEN_TRU` đo lúc viết đặc tả** (`master` = `79de656`). Nếu có handoff mới land
  trước packet này thì executor phải ĐO LẠI và khai số thật, không bê con số ở đây.
