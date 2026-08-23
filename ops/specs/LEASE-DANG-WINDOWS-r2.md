# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-WINDOWS`, **bản sửa đổi 2** (delta)

> **CHỈ ghi phần thay đổi** so với r1 (`f555cbe1a368c12040726dd706ce25ed8dd4041bd8a2f840590810a3c3908a26`).
> r1 **KHÔNG bị sửa, KHÔNG bị xoá**.

`packet_id`: `LEASE-DANG-WINDOWS` · `packet_issue`: `#238`

## Vì sao có bản này

Phiên `session_018YdsqSNdxorwxVYW2d2PkH` (PR `#233`) chuyển tin: **người giữ kho giao quyết định
Windows cho phiên này**, in-session 22-08-2026. Kèm bốn phép đo. Phiên điều phối **kiểm lại từng
cái** — hai sai, phần lập luận cốt lõi **đúng và đổi hướng packet**.

### Đúng, và nó là điểm xoay

`ops-publish-lease.yml` khai **`runs-on: ubuntu-latest`** (dòng 73). Bộ test thì chạy trên
`ci.yml` với `runs-on: ${{ matrix.os }}`. Tám ca đi qua `_chay_buoc_dang` **trích thân bước từ
workflow ấy rồi chạy dưới `bash`** — nên trên Windows chúng đo **một thứ không bao giờ chạy ở
đó**. Giả định POSIX của chúng **HỢP LỆ**; chúng hỏng vì **tình cờ bị thực thi sai nền**.

Và **chính tệp ấy đã viết sẵn câu trả lời** trước khi lỗi xảy ra — docstring `_bash_posix()`:

> *"Nói rõ phạm vi: bước được đo chạy trong job `runs-on: ubuntu-latest`, nên Windows chỉ là nơi
> bộ test **tình cờ** chạy."*

### Sai — ghi ra để hồ sơ không mang số hỏng

| lời khai | đo lại |
|---|---|
| *"`ops/lease_publish_test.py` có **0** chốt theo nền"* (`grep -c` → 0) | **7** chỗ khớp trên `master` hiện tại **và** trên `ba82b06f` (dòng 1118, 1610, 1628, 1771, 1796, 1914, 1983). Cả bảy là **thích nghi** theo nền, không phải **bỏ qua** — nên phần *"chưa ca nào bị bỏ qua theo nền"* thì đúng, còn **con số 0 thì sai**. |
| *"revert bỏ 5909 dòng, mất toàn bộ vết kiểm toán"* | Phiên điều phối đã revert **THU HẸP**: chỉ ba tệp mã. Đo: `git diff --stat 3f641673..origin/master` ⇒ **46 tệp, +5259 còn nguyên** — 8 đặc tả, 5 verdict + biên nhận, handoff, lease, prompt. **Kịch bản mất hồ sơ KHÔNG xảy ra.** |

Thêm một dữ kiện tin ấy chưa có: **master đã XANH trở lại** — `2ab3560a`, run `32554713709`,
`total_jobs: 2` (ubuntu + windows), `failed_jobs: 0`. PR `#233` hết bị chặn.

## Quyết định MỚI

| # | quyết định | căn cứ |
|---|---|---|
| **Q3′** | **THAY Q3 của r1.** Một ca được phép bỏ qua trên một nền **CHỈ KHI** phạm vi nền của nó **DẪN XUẤT ĐƯỢC** từ `runs-on` của workflow mà nó đo — **không có danh sách viết tay**. | Đúng nước đi đã cứu `#227`: *cái gì máy dẫn xuất được thì đừng để người liệt kê*. Nó cũng đóng thẳng cảnh báo của phiên `#233` rằng danh sách bỏ qua sẽ thành **cửa sau** — không có danh sách thì không có cửa sau. |
| **Q6** | **`t49` KHÔNG thuộc Q3′ — nó phải được VÁ THẬT.** | `t49` không trích thân bước của workflow nào; nó đo **mối nối `GOI_GH`** bằng một `gh` giả. Giả định POSIX của nó là về **bộ đồ giả**, không về một artefact ubuntu-only. Tin của `#233` gộp `t49` chung với tám ca kia — **chỗ ấy gộp sai**. |
| **Q7** | Ngân sách nới **60 → 90 dòng thêm** so với `ba82b06f`. | Q3′ đòi một phép **dẫn xuất** + một ca meta, đắt hơn một danh sách. |

## `nghiem_thu` — thay `W3`, thêm `W6`–`W8`

Giữ `W1`, `W2`, `W4`, `W5` của r1.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **W3′** | Lượt `workflow_dispatch` THẬT: job `windows-latest` **XANH**, và **in ra số ca bỏ qua kèm lý do**. Ubuntu chạy **≥ 69** ca; Windows chạy phần còn lại, `N/N` hai số bằng nhau **trong phần đã chạy**. | Chính lượt chạy ấy. Bằng chứng phải nêu `run_id`, `head_sha`, kết luận **từng job**. |
| **W6** | Phạm vi nền **dẫn xuất từ `runs-on`**: ca đọc thân bước của workflow X ⇒ nền của ca = `runs-on` của X. | Đổi `runs-on` của `ops-publish-lease.yml` thành matrix có `windows-latest` ⇒ tám ca ấy **phải chạy trở lại**, không còn được bỏ qua. Ghi cứng danh sách ⇒ đột biến này **không** đổi gì ⇒ ĐỎ. |
| **W7** | Ca meta: bỏ qua một ca mà workflow của nó **KHÔNG** ubuntu-only ⇒ **ĐỎ**. | Bỏ qua một ca bất kỳ không thoả điều kiện ⇒ phải ĐỎ. Đây là chốt chống cửa sau. |
| **W8** | Ca bị bỏ qua phải **IN RA** rằng nó bỏ qua **và vì sao** (kèm `runs-on` đã đọc được). Tổng kết khai **số đã chạy / số bỏ qua**. | Bỏ dòng in ⇒ ĐỎ. *"Ca có MẶT khác ca có ĐO"* — một ca im lặng bỏ qua là ca biến mất. |

## `hinh_dang_ke_thua` — một mục phải ghi về CHÍNH r1

`Q3` của r1 viết *"CẤM skip/xfail/rẽ nhánh theo `os.name` **để lấy xanh**"*. Đọc đúng chữ thì nó
cấm đúng thứ đáng cấm. Nhưng nó **áp một luật chung mà không đo phạm vi nền của thứ đang bàn**, và
một người đọc rộng sẽ hiểu thành *"cấm mọi khai báo phạm vi"* — tức cấm đúng cách chữa.

Đây **cận** hình dạng **B** (*mượn tiền lệ mà không đo xem nó áp dụng được không*). Phiên điều
phối **không tự tăng bộ đếm**, vì luật ấy đọc đúng chữ vẫn đúng; nhưng ghi thẳng chuyện này ra
thay vì lặng lẽ sửa. **B giữ 2**; người giữ kho quyết nếu muốn khác.

Các bộ đếm khác giữ nguyên: **A** = 7 · **C** = 1 · **D** = 3 · **E** = 2 · **F** = 2.

## `chua_do_duoc`

Giữ r1, sửa mục 1: **nguyên nhân của `t49` nay có giả thuyết mạnh** (shebang không phần mở rộng,
Windows không chạy shebang ⇒ `gh` giả không bao giờ được gọi ⇒ tệp `calls` không sinh) — **vẫn
chưa đo**, và `W1`/`W2` sinh ra để đo nó. Tám ca kia **không cần nguyên nhân**: chúng không nên
chạy ở đó ngay từ đầu.
