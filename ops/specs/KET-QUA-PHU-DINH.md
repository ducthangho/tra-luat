# ĐẶC TẢ ĐÓNG BĂNG — `KET-QUA-PHU-DINH`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `KET-QUA-PHU-DINH`
`packet_issue`: `CHUA_CO` — người giữ kho chưa mở. **Không bịa số.**

`review_class`: **`sensitive`** — packet sửa **hợp đồng** (`docs/PROTOCOL_DA_PHIEN.md` §7 và §12).
`ADR-0034` xếp đây là **thay đổi material**: phải đi qua ADR có phê duyệt của chủ kho, không phải
một bản vá tài liệu.

## `nguon_cap_viec`

Phiên thi công `CI-BANG-PHU-THUOC` (#245), 22-08-2026. Người giữ kho chỉ đạo trực tiếp:
*"Soạn thành packet: Issue + spec cho các mục trên."*

Packet này **không sinh ra từ một finding**. Nó sinh ra vì phiên ấy tạo ra một loại kết quả mà
**protocol không có chỗ để ghi**, và vì một đặc tả đã đóng băng **bị vô hiệu mà không cơ chế nào
phát hiện**. Hai chuyện là hai mặt của cùng một thiếu sót: hệ thống ghi được *đã làm gì*, không
ghi được *đã chứng minh cái gì là không làm được*, và do đó không lan được kết luận ấy đi.

## Bằng chứng — ĐO, không suy

### B1. Protocol không có trạng thái cho "đã chứng minh là KHÔNG THỂ"

Vế ĐỌC của `CI-BANG-PHU-THUOC` (`M3`) tiêu **bốn vòng cross-review** để đi tới một kết luận
**dương về mặt tri thức**: cơ chế đo bằng audit hook nạp qua `PYTHONPATH` **không thể trung
thực**. Thứ tự khởi động Python là cố định (`.pth` → `sitecustomize` → `usercustomize` → mã người
dùng); cả ba là cơ chế **một khe một tên** mà kẻ chèn thư mục tạm lên đầu `PYTHONPATH` **luôn**
thắng ⇒ **không tên nào an toàn**. Phản chứng chạy được: một `sitecustomize` đọc `ops/` vẫn cho
`"ops": "doc_lap"`, `rc=0`.

Đó không phải `blocked` (không ai chặn), không phải `failed` (không có lỗi kỹ thuật), không phải
`done`. Enum của §7 là `done | needs_followup | blocked`. Handoff thật buộc phải khai:

```yaml
status: needs_followup
failure:
  fingerprint: null
  category: null          # KHONG phai that bai
```

…rồi **cầu xin bằng văn xuôi** ở ba chỗ khác nhau rằng đừng thử lại hướng ấy. Một phiên sau đọc
`needs_followup` một cách ngay tình sẽ hiểu là *"việc còn dở, làm tiếp đi"* — và tiêu thêm bốn
vòng cho đúng ngõ cụt đã được chứng minh.

### B2. Một đặc tả ĐÓNG BĂNG đã bị vô hiệu, và mọi tín hiệu đều nói "cứ làm đi"

`ops/specs/CI-FASTPATH-THEO-DIFF.md` (sha256 `32ba1b32ec9436453f7f8fe3c6f8e4d9a4af6e2ceb4e40bfefd8ffb2917d7580`)
khai **ĐIỀU KIỆN MỌC**: chỉ bắt đầu khi `CI-BANG-PHU-THUOC` *"đã có hiện vật trên `master`"*.
Điều kiện ấy **ĐÃ THOẢ** — `26856f9` land hai tệp.

Nhưng lý lẽ của quyết định **Q1** trong chính đặc tả ấy đọc nguyên văn:

> *"nếu merge chỉ chạm nhóm ngoài **cả tập đọc lẫn tập băm** thì cây runtime **giống hệt** commit
> cha, nên lượt mới **kế thừa** bằng chứng còn hiệu lực thay vì dựng lại."*

Vế **tập đọc không tồn tại** và theo B1 sẽ không tồn tại theo cơ chế cũ. Nên bảng chỉ phủ **nửa**
điều kiện Q1 dựa vào.

Trạng thái quan sát được của đặc tả ấy lúc này: băm khớp · đóng băng · điều kiện mọc thoả ·
không cờ nào. Một phiên đọc nó sẽ dựng hàm quyết định fast-path **trên nửa bảng** — đúng hình
dạng *"chứng minh bỏ bước này an toàn bằng thứ nhẹ hơn"* mà `CLAUDE.md` đã đếm **ba** lần và
`dieu_kien_dung` của lease #245 liệt vào điều kiện DỪNG.

**Không trường nào trong đặc tả nói nó phụ thuộc KẾT QUẢ của packet nào.** `ĐIỀU KIỆN MỌC` chỉ
nói *"hiện vật có trên master chưa"* — một câu hỏi về **sự tồn tại**, không phải về **nội dung**.
Cùng họ bài học *"đếm sự CÓ MẶT thay vì KHẢ NĂNG"*, ở tầng đặc tả.

### B3. Lý lẽ biện minh cho việc tách slice SAI ngay lúc land, và không ai đo

`ops/specs/CI-BANG-PHU-THUOC.md` biện minh việc tách hai slice bằng câu:

> *"Tách ra thì bảng lên trước, chạy vài lượt **trong lúc chưa ai dựa vào nó**."*

Đo trên `master` sau khi slice land:

```
grep -n "ci_phamvi" .github/workflows/*.yml      -> KHONG mot dong nao
rg -n "ci_phamvi" --glob '!.github/checks/*' .    -> KHONG mot dong nao
```

Bảng **không chạy lượt nào**. Cổng xanh, review sạch, ngân sách trong trần, nghiệm thu sáu tiêu
chí đều đạt — và **mệnh đề biện minh cho chính hình dạng của packet thì sai**, vì nó không nằm
trong `nghiem_thu`. §12 đòi Stable Slice *"hữu ích độc lập"* và *"có test/evidence dương của
chính nó"*, nhưng không đòi **mệnh đề biện minh** phải có phép đo.

## `write_set`

Đúng ba tệp:

- `docs/adr/0046-ket-qua-phu-dinh-va-phu-thuoc-ket-qua.md` — ADR mới (số kế tiếp; 45 ADR đang có)
- `docs/PROTOCOL_DA_PHIEN.md` — §7 (enum + khối), §12 (một câu), §20 (một dòng bảng ADR)
- `.claude/dev/packet_loop.py` — mở rộng `adr-song` **chỉ** ở phần đọc bảng §20 nếu cần

## `ngoai_pham_vi`

- **KHÔNG sửa `ops/specs/CI-FASTPATH-THEO-DIFF.md`.** Nó đóng băng; sửa phải qua bản sửa đổi
  riêng (`-r2`). Packet này dựng **cơ chế đánh dấu**, không dùng thử lên đặc tả ấy.
- **KHÔNG viết lại handoff hay lease cũ.** Trường mới áp cho cái sinh sau.
- `ops/lease_publish.py` — write set **đang bị giữ** bởi `LEASE-HOI-TOAN-KHO`.
- Cổng cưỡng chế `nang_tran` — **đã là nợ D3** trong `ops/HOAN_THIEN_KE_HOACH_20260822.md`, và
  nó phải đứng sau D1/D2. Không mở lại ở đây.

## `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| **M1** | ADR ghi quyết định, kèm B1–B3 làm căn cứ, và nêu **cái giá của việc KHÔNG làm**: bốn vòng review có thể bị tiêu lại | `docs/adr/0046-*.md` |
| **M2** | §7: thêm `status: disproven` vào enum, kèm khối bắt buộc khi dùng nó — `disproven: {menh_de, co_che, phan_chung, huong_con_lai[]}`. `phan_chung` phải là **lệnh chạy được**, không phải câu văn | `docs/PROTOCOL_DA_PHIEN.md` |
| **M3** | §7: `disproven` **KHÔNG** đi kèm `failure.category` — kết quả phủ định không phải thất bại. Khai cả hai ⇒ sai hợp đồng | `docs/PROTOCOL_DA_PHIEN.md` |
| **M4** | Đặc tả khai `phu_thuoc_ket_qua:` — liệt kê deliverable của packet khác mà **lý lẽ** của nó dựa vào, không chỉ hiện vật nó cần có mặt | `docs/PROTOCOL_DA_PHIEN.md` |
| **M5** | Handoff mang `status: disproven` được khai `vo_hieu_hoa: [<packet_id>…]`. **Nó là KHUYẾN NGHỊ, không phải hiệu lực**: handoff của executor là **bằng chứng**, không phải nguồn thẩm quyền (`AGENTS.md` §5). Cờ chỉ có hiệu lực chặn lease sau khi **dispatcher xác nhận** — đã đối chiếu `phu_thuoc_ket_qua` khai đúng, đã đọc `phan_chung`, và có quyết định bền ghi lại | `docs/PROTOCOL_DA_PHIEN.md` |
| **M5b** | `vo_hieu_hoa` trỏ packet **không liên quan** (không nằm trong `phu_thuoc_ket_qua` của bất kỳ bên nào) ⇒ **không chặn được gì**, và phải in ra là bị bỏ qua chứ không im lặng | `docs/PROTOCOL_DA_PHIEN.md` |
| **M6** | §12: Stable Slice phải đưa **mệnh đề biện minh cho việc tách** vào `nghiem_thu` của chính nó (ca B3) | `docs/PROTOCOL_DA_PHIEN.md` |
| **M7** | §20 có đúng một dòng cho ADR-0046, kèm cột *"cổng nào ĐỌC luật ấy"* — khai thẳng `0 cổng` nếu chưa có, đừng để trống | `docs/PROTOCOL_DA_PHIEN.md` |

## `nghiem_thu`

| # | nghiệm thu | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | `packet_loop.py adr-song --root .` ⇒ rc=0 sau khi thêm ADR-0046 | **đo NỀN trước**: chạy trên `origin/master` sạch, phải rc=0 (đã đo 22-08: *"sạch — 45 ADR, 45 dòng §20"*). Thêm ADR mà quên dòng §20 ⇒ ĐỎ |
| **N2** | Khối `disproven` của handoff #245 **parse được** và đủ trường | dựng lại khối ấy từ `ops/handoff/ci-bang-phu-thuoc-exec-1-*.md` rồi kiểm; thiếu `phan_chung` ⇒ ĐỎ |
| **N3** | `disproven` + `failure.category` cùng lúc ⇒ **sai hợp đồng** | ca chiều **BẮT OAN**: `disproven` với `failure.category: null` phải ĐẠT. Giết ca ấy bằng đột biến **siết thêm** (cấm luôn khoá `failure`) |
| **N3b** | **Một handoff `disproven` KHÔNG tự chặn được lease của packet khác** | ca: handoff khai `vo_hieu_hoa: [PACKET-KHONG-LIEN-QUAN]` ⇒ cấp lease cho packet ấy **vẫn được**, kèm dòng in ra rằng cờ bị bỏ qua. Đột biến cho cờ hiệu lực ngay ⇒ ĐỎ. Không có ca này thì một executor nhầm (hoặc bị chiếm) khoá được cả đồ thị packet |
| **N4** | `doctrine-scan --root .` ⇒ rc=0 — ADR mới **không** được chép lại doctrine của protocol | đột biến chép nguyên một đoạn §7 vào ADR ⇒ ĐỎ |
| **N5** | delta so master = 0 cho `packet_loop_test.py` và `lease_publish_test.py` | nền master đo **trong worktree của chính kho** (chép ra thư mục rỗng cho ĐỎ GIẢ) |
| **N6** | `tl.py --selftest` giữ nguyên N/N | packet không chạm `scripts/`; số lệch ⇒ có thứ ngoài write set bị đụng |

## `hinh_dang_ke_thua`

Sau packet này, **hai** việc mọc ra và **cả hai đều cần quyết định riêng**:

1. `CI-FASTPATH-THEO-DIFF-r2` — bản sửa đổi tính lại Q1 cho một bảng chỉ có vế BĂM.
2. Cổng đọc `phu_thuoc_ket_qua` lúc cấp lease. Packet này **chỉ định nghĩa trường**; cưỡng chế là
   việc sau, và đặc tả khai thẳng thế thay vì hứa suông — bài học *"PHẠM VI TUYÊN BỐ phải bằng
   phạm vi ĐO ĐƯỢC"*.

## `chua_do_duoc`

- **Không đo được một mệnh đề `disproven` có ĐÚNG hay không.** Protocol chỉ đòi khai `phan_chung`
  là lệnh chạy được; nó không chạy hộ. Một kết luận phủ định SAI sẽ chặn oan một hướng đúng —
  và đó là rủi ro **thật** của packet này, phải nói ra chứ không giấu.
- **M5 đổi `vo_hieu_hoa` thành KHUYẾN NGHỊ, và cái giá của việc ấy là ĐỘ TRỄ.** Một kết luận phủ
  định **đúng** nay phải chờ dispatcher xác nhận mới chặn được lease — nghĩa là có một cửa sổ trong
  đó phiên khác vẫn cấp được lease cho packet đã hỏng tiền đề. Đó là **đánh đổi có chủ đích**: cái
  giá ngược lại (executor tự khoá cả đồ thị packet) nặng hơn, vì nó biến bằng chứng thành thẩm
  quyền. Rút ngắn cửa sổ là việc của cổng đọc `phu_thuoc_ket_qua`, đã khai ở `hinh_dang_ke_thua`.
- **Không đo được lý lẽ của một đặc tả có phụ thuộc gì.** `phu_thuoc_ket_qua` do người viết khai;
  quên khai thì cơ chế im lặng — cùng lớp với `nang_tran` (1/121 lease). Vì thế M7 đòi §20 ghi
  thẳng **`0 cổng`** nếu chưa cưỡng chế, để lần sau đếm được nợ thay vì tưởng đã có cổng.
- **Số 45 ADR và bảng §20 đo lúc viết đặc tả** (`master` = `79de656`). Executor phải đo lại.
