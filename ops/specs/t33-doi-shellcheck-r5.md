# ĐẶC TẢ ĐÓNG BĂNG — `T33-DOI-SHELLCHECK`, **bản sửa đổi 5** (delta)

> **CHỈ ghi phần thay đổi.** r1 (`1405d390ca9376725517d01ef5b8d1abffd6a09d78d2b7206c2f068e7711f4da`),
> r2 (`b9620d17b86f503b12d93359fb6d3423d29c034c29ab372f40cc5d7089b40e71`) và
> r3 (`78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d`) **KHÔNG bị sửa,
> KHÔNG bị xoá**; mọi thứ r5 không nêu thì r3 (rồi r2, rồi r1) nguyên hiệu lực.

```yaml
packet_id: T33-DOI-SHELLCHECK
packet_issue: 297          # KHÁC r1-r4: nguồn cấp việc là #297, không phải #249
revision: 5
sua_hai_dieu:
  - ba chỗ mang lời khai "toàn chân Ubuntu" — RỘNG HƠN phép đo
  - đánh dấu các mục đã TIÊU, kèm thứ đã thay chúng
```

## Bản này KHÔNG đặc tả mục tiêu mới

Nó đóng **NGUỒN** của một lời khai rộng hơn phép đo, và nói ra phần nào của chuỗi r1–r3 còn
là hợp đồng đang sống. Không thêm `M`, không đổi `nghiem_thu`, không đổi write set.

## 1. Ba chỗ mang lời khai "toàn chân Ubuntu"

Đo trên `master = a84b6d15c69cd7161eaca780a1d877b8a79c2b1e`:

| | dòng | dạng |
|---|---|---|
| `ops/specs/t33-doi-shellcheck-r2.md` | **215–216** | văn xuôi |
| `ops/specs/t33-doi-shellcheck-r2.md` | **232** | **trong khối `ca_va_M3` — CHÉP NGUYÊN VĂN**, kèm `88/88` |
| `ops/specs/t33-doi-shellcheck-r3.md` | **192** | **trong khối `ca_va_M3` — CHÉP NGUYÊN VĂN**, kèm `97/97` |

Nguyên văn của `r2:215–216`:

> `X2` là **một mệnh đề**, và nó làm cổng nền tra theo một trục hoàn toàn khác mà **toàn bộ
> chân Ubuntu im lặng**.

Phép đo đứng **ngay trên nó**, cùng tệp (`r2:200–201`): *"Phản chứng, chạy trên **worktree rời**
của `00d4b3d7`"* → `88/88`, `rc=0`.

**Một worktree rời không phải một chân CI.** Đột biến `X2` **chưa bao giờ được đẩy lên CI**, nên
nó chưa từng chạy trên một runner Ubuntu nào. `"toàn chân Ubuntu"` chỉ cả job/leg CI ⇒ **lời khai
rộng hơn phép đo**.

### Lời khai ĐÚNG — thay cho cả ba chỗ

Văn xuôi (thay `r2:215–216`):

> `X2` là **một mệnh đề**, và nó làm cổng nền tra theo một trục hoàn toàn khác mà **không ca nào
> trong bộ test bắt được khi chạy cục bộ trên Linux**. Thứ tách hai trục là 8 dòng `BỎ QUA` chỉ
> xuất hiện khi nền được mô phỏng là `nt`.

Trong khối chép nguyên văn (thay `r2:232` và `r3:192`) — dùng đúng con số của bản tương ứng:

```
rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026)
```

`r2` giữ `88/88` của nó, `r3` giữ `97/97` của nó. **Chỉ mệnh đề phạm vi đổi**, con số không —
chúng là số đo thật của hai thời điểm khác nhau.

### Vì sao ba chỗ chứ không phải một

`r4` (**chỉ có trên nhánh `claude/t33-doi-shellcheck-exec-1`, KHÔNG có trên master** — đo
2026-08-24) thay đúng `r3:192` và khai mình *"sửa ĐÚNG MỘT lời khai"*. Cross-review lượt 4 của
PR #293 bác: `r2` còn **hai** chỗ nữa, và một trong hai nằm trong khối `CHÉP NGUYÊN VĂN`. Tức ai
theo `r4/Q13` mà chép từ `r2` sẽ chép lại câu sai **cộng** con số đã chết.

`r5` này thay cả ba, trên master, nên nó đứng vững **dù #293 land r4 hay gỡ r4 ra**.

## 2. Mục nào của r1–r3 đã TIÊU

Đo: `grep` toàn kho ⇒ **0** tham chiếu tới `r2` ngoài chính chuỗi đặc tả.

| mục | trạng thái | thứ đã thay nó |
|---|---|---|
| `M3` · `M4` | **đã thi công** | ca `t98` + docstring `t33`, PR #293, 4 vòng cross-review |
| `M1` · `M2` | **chuyển giao** | packet #290 `HA-TANG-CONG-CU-TAT-DINH` — lease `r3` khối `thu_hep_pham_vi` |
| `nghiem_thu` của r2 (8 ô) | **bị thay** | bảng 7 ô của r3, đo lại trên base mới |
| `write_set` | **bị thay** | lease `…r5-claude-20260824` (1 → 2 đường dẫn) |
| `base_sha` / mọi số neo `00d4b3d7` | **hết hạn** | master đã đi **51 commit** tính tới `59fe955d`; `180 ref` nay **194**; `88/88` nay `97/98` |

**Số cũ KHÔNG phải khuyết tật.** Đặc tả là ảnh chụp, và r2 tự nói vậy. Khuyết tật là **không có
gì đánh dấu r2 đã tiêu**, nên người đọc không phân biệt được *hợp đồng đang sống* với *biên bản
lịch sử*. Bảng trên là bản đánh dấu ấy — bằng **văn xuôi**, vì (xem §4) đặc tả không có trường
trạng thái nào.

### Cố ý KHÔNG làm

**KHÔNG đo lại toàn bộ số của r2 cho khớp master.** Không ai còn thi hành theo r2; đo lại là làm
việc không có người tiêu thụ, và kết quả lại hết hạn sau 51 commit nữa. Thứ cần sửa là **trạng
thái**, không phải **con số**.

## 3. r5 tự chịu phép thử nó đang áp

Một bản đặc tả sửa lỗi *"khai rộng hơn đo"* mà tự khai rộng hơn đo thì **tệ hơn không sửa** — và
`r4` đã mắc đúng thế (khai *"sửa ĐÚNG MỘT lời khai"* trong khi cùng tệp ghi *"CHƯA AI QUÉT"*, cách
93 dòng). Nên nói chật:

| lời khai của r5 | phép đo đứng sau |
|---|---|
| "ba chỗ" | `grep -n 'chân Ubuntu'` trên r1/r2/r3 tại `a84b6d15` ⇒ đúng 3 dòng |
| "r4 không có trên master" | `git cat-file -e origin/master:…r4.md` ⇒ không có |
| "0 tham chiếu tới r2" | `grep -rn 't33-doi-shellcheck-r2'` loại chính chuỗi đặc tả ⇒ rỗng |
| "51 commit" | `git rev-list --count 00d4b3d7..59fe955d` |
| "180 ref nay 194" | `git ls-remote --heads origin \| wc -l` |
| "88/88 nay 97/98" | `grep -c '^@ca' ops/lease_publish_test.py` ⇒ **97** trên master; 98 sau khi #293 land |

**KHÔNG khai "đã quét hết".** "Ba chỗ" là kết quả của **một** phép quét theo cụm từ `chân Ubuntu`
cộng lượng từ tuyệt đối — tức một **danh sách đoán trước**, và kho đã trả giá nhiều lần vì danh
sách đoán trước. Lời khai đúng là: *ba chỗ mang **cụm từ ấy***. Một lời khai cùng hình dạng viết
bằng chữ khác thì phép quét này **không thấy**.

Nếu ai tìm ra chỗ **thứ tư** thì "ba" là số sai, và theo `dieu_kien_dung` của lease, phạm vi packet
phải khai lại trước khi viết tiếp.

## 4. Nợ có tên — `SPEC-KHONG-CO-TRANG-THAI`

Đặc tả **không có trường trạng thái nào**. `spec_status: dong_bang` chỉ sống trong **lease**, và
nó nói về *cả tệp*, không về từng mục. Nên bảng §2 là **văn xuôi không cổng nào đọc được** — cùng
hình dạng nợ `AG-T0-01B` (*lease không có đường thu hồi sau khi việc xong*), khác lớp hiện vật.

Đề xuất đã trình chủ kho, **CHƯA duyệt**: thêm `trang_thai` cho đặc tả (`dong_bang` ·
`da_bi_thay_the` · `da_tieu`) kèm một cổng đọc nó. Không làm trong packet này.

## 5. `nghiem_thu` của r5

| | tiêu chí | phản chứng làm nó ĐỎ |
|---|---|---|
| `V1` | r5 nêu **đúng ba** vị trí, mỗi vị trí có tệp:dòng tra được | đổi một số dòng ⇒ `grep -n` không khớp |
| `V2` | r5 **không sửa đè** r1/r2/r3 | `git diff --name-status base..HEAD` có tệp nào khác `…r5.md` ⇒ ĐỎ |
| `V3` | mọi lời khai ở §3 có phép đo tra được kèm bên | thêm một dòng khai không có cột phép đo ⇒ ĐỎ khi reviewer soi |
| `V4` | r5 không đổi `M`, `nghiem_thu`, hay write set của r1–r3 | có mục nào như vậy ⇒ ĐỎ |

`V3` **không có cổng máy** — kho không có cơ chế canh văn xuôi (`t42` khớp marker nợ ↔ sổ; `doc-claims-check`
đọc trích dẫn số hiệu văn bản). Đó là tiêu chí của **reviewer**. Khai theo `L3` thay vì làm tròn
thành đã có — đúng chỗ `M4` của r3 đã phải khai y hệt.

## 6. Chưa đo được

1. **Còn lời khai cùng hình dạng mà không mang cụm "chân Ubuntu" hay không** — xem §3.
2. **Hành vi trên `windows-latest` thật** — giữ nguyên từ r1–r3, chưa đo.
3. **`r4` sẽ land hay bị gỡ** — chưa quyết. r5 viết để đúng ở **cả hai** trạng thái.
