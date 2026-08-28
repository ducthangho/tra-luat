# Packet `D9-CON-HO` (#382) — hồ sơ CÓ THẨM QUYỀN

> Thân Issue #382 là **bản chiếu**. Thứ định danh là **băm**, không phải tên nhánh.
> Xuất xứ nội dung: một lượt cross-review **độc lập thứ hai** trên PR #371 (`claude-opus-5/xhigh`,
> 1171s), chạy song song và không biết gì về lượt đã đăng lúc 07:53Z. Hai lượt **hội tụ** trên P1
> và một P2 — cả hai đã đóng ở `r4`. Bốn phát hiện dưới đây lượt kia **không có**, và cả bốn đã
> được đo lại trên `245905e2` (bản đã land vào master qua `58b85cc2`).

## Vì sao packet này tồn tại

Packet #369 sinh ra vì #319 đã nâng trần **bốn lần**. Nó đổi đơn vị đếm sang dòng-không-trắng và
chốt trần `779`. Câu hỏi đúng — **ai chặn lần nâng thứ năm?** — hoá ra **không ai**.

Đây không phải "một cổng còn thiếu tính năng". Đây là **một cổng không có răng trong một khoảng
rộng, mà trên kho sạch nó trông y hệt một cổng đang canh** — đúng hình dạng lỗi kho đã trả giá
nhiều lần. Hai việc đầu cùng một hình dạng, nên gộp một packet.

## VIỆC 1 — `tran-779-khong-co-rang` (P2)

Đo trên `245905e2`: sửa **nhất quán** `assert tong <= 779` rồi chạy trọn cổng.

```
đối chứng không đột biến   rc=0  TỔNG: ĐẠT
trần -> 800                rc=0  TỔNG: ĐẠT
trần -> 850                rc=0  TỔNG: ĐẠT
trần -> 900                rc=0  TỔNG: ĐẠT
trần -> 919                rc=0  TỔNG: ĐẠT
trần -> 920                rc=0  TỔNG: ĐẠT
```

**Không ca nào, không đột biến nào bắt.** Nâng thêm **≥141** dòng đi qua sạch. Biên KHAI là 18;
biên **CƯỠNG CHẾ** là ≥141.

Ở SHA trước (`82cb066f`) mốc `920` còn đỏ — nhưng **vì tình cờ**: `920` đúng bằng số dòng VẬT LÝ,
nên khi trần ≥ 920 thì mutant `d9_dem_ca_dong_trang` thôi làm `D9` đỏ và `D8(a)` kêu vì **sổ sách**.
Đó là hệ quả phụ của cách dựng mutant, **không phải một ratchet được thiết kế** — và ở `245905e2`
trùng hợp ấy đã trôi mất. Một cổng dựa vào trùng hợp số học là cổng chưa tồn tại.

Đường chữa **đã được đo** ở nguồn: ràng buộc HAI PHÍA — biến biên thành thứ **đo được** thay vì
thứ hứa.

```python
TRAN, BIEN = 779, 20
assert tong <= TRAN, ...
assert TRAN - tong <= BIEN, f"biên {TRAN - tong} > {BIEN}: nâng trần phải kèm lý do, hoặc TÁCH tệp"
```

`TRAN=779` ⇒ ĐẠT. `TRAN=800` ⇒ `ĐỎ D9: biên 39 > 20`.

**Đây là GỢI Ý có số kèm theo, không phải chỉ định.** Executor tự chọn cách; cách nào khác mà đo
được là tốt hơn thì làm và nói vì sao. Nhưng cách nào cũng phải trả lời đúng câu hỏi: *nâng trần
mà không thêm mã phải ĐỎ ngay tại `D9`, không phụ thuộc một trùng hợp số học.*

## VIỆC 2 — `D13-tu-dem-chinh-no` (P2)

```
D13: '!= 1' -> '> 1'       rc=0  TỔNG: ĐẠT
```

`D13` đếm `sources[target].count(old)` trên **nguyên văn tệp** — mà tệp ấy **chứa chính bảng
`MUTATIONS`**. Nên một mẫu đột biến **CHẾT** (0 vị trí thật trong mã) nhắm `test` **tự đếm chính nó
thành 1** và được cho qua:

```
số vị trí THẬT trong mã            : 0
số lần khớp khi mẫu nằm trong bảng : 1
D13 báo lỗi?                       : False
```

Bất đối xứng đo được: mẫu chết nhắm **app** thì `D13` BẮT (`mcp_gh.py` không chứa bảng); nhắm
**test** thì LỌT. **27** mẫu nhắm app, **27** nhắm test — tức đúng một nửa bảng không được canh.

Nguyên nhân: self-assert của `D13` chỉ phủ **một chiều** — có ca 2-chỗ, thiếu ca **0-chỗ**.

Đường chữa đã đo là **không sinh dương tính giả**: đếm trên nguồn đã **cắt vùng bảng `MUTATIONS`**;
54/54 mẫu hiện có vẫn khớp đúng 1, và mẫu chết nhắm `test` chuyển từ *cho qua* sang *bắt được*.
Cộng một self-assert chiều 0. Lại là **gợi ý**, không phải chỉ định.

## VIỆC 3 — `duong-nen-ke-tiep-doan-nham-cho` (P2, về LỜI KHAI)

`ops/specs/mcp-gh-cuu-ho.md` hàng `D9` hiện khai rằng chọn (A) vì loại chú thích khỏi phép đếm
"sẽ tạo áp lực xoá tri thức kho coi trọng". Đo trên `245905e2`:

```
mcp_gh.py        không-trắng=199   chú-thích-thuần= 1
mcp_gh_test.py   không-trắng=562   chú-thích-thuần=10
TỔNG             không-trắng=761   chú-thích-thuần=11     trần=779 => biên KHAI = 18
```

**Xoá SẠCH mọi dòng chú thích của cả hai tệp chỉ mua được 11 dòng — chưa bằng biên 18.** Mối lo
"áp lực xoá chú thích" **không có chân** trên hai tệp này.

Đường nén thật sự rẻ là **gói một đoạn văn vào một dòng vật lý**:

```
dòng > 120 ký tự : 37        dài nhất: 669 ký tự
trần độ dài dòng trong kho : KHÔNG CÓ   (grep line-length|E501|max-line => rỗng)
```

Luật đếm mới **dời** động cơ nén chứ không **giết** nó: từ *xoá dòng trắng* (đã bị chặn) sang *gói
dòng dài* (không ai chặn, **không có giới hạn trên**).

Phần phải sửa trong tầm tay: **câu tại `D9` phải nêu ĐÚNG đường nén kế tiếp** (gói dòng dài), thay
vì nêu một mối lo đã bị số bác bỏ. Nói thẳng trong đặc tả rằng phép đo cho thấy nỗi lo cũ sai —
đừng xoá dấu vết, vì chính lời khai sai ấy là bài học.

**KHÔNG đổi đơn vị đếm ở packet này.** `ops/specs/mcp-gh-cuu-ho.md` cấm "đổi đơn vị lần hai", và
đó là quyết định của người giữ kho. Số cho phương án (C) đếm token, để lần quyết định sau có dữ
liệu: `mcp_gh.py` **1439** · `mcp_gh_test.py` **5345**.

## VIỆC 4 — KHÔNG làm ở packet này (P3, nợ có tên)

`try`/`finally` là bản vá ĐÚNG (phản chứng dựng được), nhưng lùi `d12` về đúng dạng base ⇒ `D12`
XANH; thứ duy nhất kêu là `D13`, và nó kêu vì **sổ sách**, không vì **hành vi**. Đây là nợ độ phủ,
không phải lỗ fail-open. Đo tại `82cb066f`, **chưa đo lại trên `245905e2`** — phạm vi ghi đúng như
nguồn khai. Thành nợ `AG-382-P3-01-d12-thieu-ca-do-hanh-vi`.

## RÀNG BUỘC ĐẶC BIỆT — packet phải sống bên trong cái ratchet nó đang sửa

`D9` hiện là **761/779**, tức chỉ còn **18 dòng** không-trắng cho `mcp_gh_test.py` trước khi chính
cổng này ĐỎ. Đó **không phải** một bất tiện cần né: nó là phép thử của chính packet. Nếu bản vá
không vừa 18 dòng thì câu trả lời đúng là điều kiện dừng `S2` và câu hỏi **"tệp này có nên TÁCH ĐÔI
không"** — đúng `chot_chong_lap_bat_buoc` mà #369 vừa land. **KHÔNG nâng `779`.**

`ops/specs/mcp-gh-cuu-ho.md` KHÔNG nằm trong phép đếm của `D9`, nên phần đặc tả không tiêu vào 18
dòng ấy.

## Phản chứng bắt buộc

Mỗi chốt mới phải có ĐỘT BIẾN RIÊNG làm nó ĐỎ, chạy trên **bản sao ngoài cây**:
- nâng `TRAN` mà không thêm mã ⇒ ĐỎ **tại `D9`**, không phải ở nơi khác vì lý do khác;
- nới chốt duy-nhất của `D13` (`!= 1` -> `> 1`) ⇒ ĐỎ;
- một mẫu đột biến **chết** nhắm `test` (0 vị trí thật trong mã) ⇒ `D13` phải BẮT;
- **ca đối chứng**: 54/54 mẫu hiện có vẫn khớp đúng 1 và cổng vẫn XANH — chốt bắt oan cũng là
  chốt hỏng.
