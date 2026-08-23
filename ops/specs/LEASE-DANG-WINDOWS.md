# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-WINDOWS`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (§3.2, §4) mới được bắt tay.

`packet_id`: `LEASE-DANG-WINDOWS` · `packet_issue`: `#238`
`nen`: `master` = `2ab3560a` · `khoi_phuc_tu`: `ba82b06f9df81fc2f13786fec590ec2110d046b7`

## Vì sao có packet này

`#227` land ở `b88744ea` rồi **CI master ĐỎ trên Windows** (`59/68`), phải revert (`#237`).

```
master 3f641673 (TRUOC merge)  ->  success
master b88744ea (SAU merge)    ->  failure
  job gate(ubuntu-latest)   xanh
  job gate(windows-latest)  DO, 59/68
    t49 t51 t52 t59 t60 t62 t63 t66 t68
    FileNotFoundError: ...\argv.log   (t49: ...\calls)
```

**Chín ca đỏ đều là ca MỚI của `#227`, và chưa ca nào từng chạy trên Windows** — `ci.yml` chỉ
chạy `ubuntu` cho PR thường, nên **lần merge chính là lần đo Windows đầu tiên**.

`#237` hoàn nguyên **ba tệp mã**, **giữ nguyên hồ sơ** trên master.

## Điều phải nói trước mọi thứ khác

**Nguyên nhân gốc CHƯA ĐƯỢC ĐO.** Phiên điều phối **không tái hiện được từ Linux**, và đã có hai
giả thuyết chưa kiểm:

- `t49` dựng đồ giả `gh` bằng **shebang** `#!{Path(sys.executable).resolve()}` — **dấu chéo ngược**,
  không phải `.as_posix()`;
- tám ca kia đi qua `_chay_buoc_dang`, nơi thân bước chạy dưới `bash` với `lease_publish.py` giả.

**Đặc tả này CỐ Ý KHÔNG chốt nguyên nhân.** Đoán ở đây đúng là cách kho đã mất thời gian, và
`#227` vừa trả giá năm lần vì đặc tả **liệt kê từ bên ngoài** thay vì để phép đo nói.

## Quyết định đã chốt

| # | quyết định | căn cứ |
|---|---|---|
| **Q1** | **ĐO TRƯỚC, VÁ SAU.** Việc **đầu tiên** là làm `_chay_buoc_dang` **báo được nguyên nhân**; chỉ sau khi có một lượt Windows THẬT in ra lý do mới được sửa. | Hiện nó **nuốt `stdout`/`stderr`** của tiến trình con rồi ném `FileNotFoundError` — phép đo **tự giấu lý do**. Đúng *"trạng thái thứ ba KHÔNG ĐO ĐƯỢC"* mà cả `#227` đi bắt người khác làm. |
| **Q2** | Nghiệm thu neo vào **một lượt chạy GitHub Actions THẬT có job `windows-latest` XANH trên exact head**, gọi bằng `workflow_dispatch`. | Đây là khoảng trống **lớn nhất** của `#227` — bảy lượt vá, không lượt Actions thật nào. Packet này **đóng đúng nó**, và mọi lời khai khác đều thứ yếu. |
| **Q3** | **CẤM** `skip`/`xfail`/rẽ nhánh theo `os.name` để lấy xanh. | *"Không skip, disable, hay quarantine một test để lấy xanh"* — luật kho. Một ca bỏ qua trên Windows là ca **không tồn tại** đúng nơi nó cần nhất. |
| **Q4** | Khôi phục ba tệp mã từ `ba82b06f` là thao tác **CƠ HỌC**, không tính ngân sách. Ngân sách đo **phần MỚI** so với `ba82b06f`. | Ba tệp ấy đã qua bốn lượt cross-review; đếm lại chúng là đếm hai lần. |
| **Q5** | Executor **`codex`** · reviewer **`claude`**. | §8 cross-provider cho phạm vi `.github/workflows/**`. Và `codex` giữ ngữ cảnh mã của `#227`. |

## `write_set`

```
.github/workflows/ops-publish-lease.yml
ops/lease_publish.py
ops/lease_publish_test.py
```

**Ngân sách: ≤ 3 tệp, ≤ 60 dòng THÊM so với `ba82b06f`** (Q4). Vượt ⇒ DỪNG + handoff.

## `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **W1** | `_chay_buoc_dang` khi thiếu log phải ném lỗi **kèm `rc`, `stdout`, `stderr`** của tiến trình con — không phải `FileNotFoundError` trần. | Bỏ phần đính kèm ⇒ ca đòi thông điệp chứa cả ba mảnh phải ĐỎ. |
| **W2** | Ca tương tự cho `t49` và mọi chỗ khác đọc tệp do đồ giả sinh. | như trên |
| **W3** | **Suite `N/N` trên `windows-latest` trong một lượt `workflow_dispatch` THẬT**, `N ≥ 68`, trên **exact head** sẽ land. | Chính lượt chạy ấy. **Không có nó thì packet KHÔNG xong** — bất kể suite xanh ở đâu khác. |
| **W4** | Suite `N/N` trên `ubuntu-latest` trong **cùng** lượt chạy ấy, hai số bằng nhau. | như trên |
| **W5** | Mọi đột biến quyết định của `#227` **vẫn giết** trên head mới: `M1`–`M4` · `A5` · `D3`/`D4` · tám đột biến gỡ guard. | Chạy lại từng cái. |

**Bằng chứng phải nêu `run_id`, `head_sha`, và kết luận của TỪNG job.** Một dòng *"suite xanh"*
không kèm `run_id` là lời khai, không phải phép đo.

## `ngoai_pham_vi`

Hai finding của verdict `#227` lượt 5 (`bao_chan` khoá theo **cách viết** · mất bất biến
`set +e … rc=$? … set -e`) — chúng ở **#235**, đặc tả riêng. **Đừng đụng.**
Cộng mọi mục `ngoai_pham_vi` của `#227` r2–r7.

## `hinh_dang_ke_thua`

| | | |
|---|---|---|
| **A** | *lời khai rộng hơn phép đo* | **7** |
| **B** | *mượn tiền lệ mà không đo xem nó áp dụng được không* | 2 |
| **C** | *phản chứng bắt buộc còn thiếu* | 1 |
| **D** | *đặt câu hỏi kiểm chứng ở sai độ phân giải / sai pha* | 3 |
| **E** | *khoá theo thứ liệt kê được thay vì theo thứ thật sự chặn* | 2 |
| **F** | ***land trên một nền, đo trên nền khác*** | **2** |

**A lên 7** là của **phiên điều phối**: khai *"`actionlint` rc=0 trên 5 workflow"* suốt bốn lượt
trong khi `actionlint` của container **không có `shellcheck`** — phép đo **yếu hơn CI**, và CI đỏ
ngay lần chạy đầu.

**F là hình dạng đã có trong `CLAUDE.md`** (mục 14-08-2026: *"Gate PR và gate master KHÔNG phải
một thứ"*, sáu lần merge là sáu lần đo Windows đầu tiên). Lần **2** là `#227`: tôi **trích chính
mục ấy** trong PR `#234` rồi merge mà không gọi `workflow_dispatch`.

**Chốt:** A lần 8 · B lần 3 · C lần 2 · D lần 4 · E lần 3 · **F lần 3** ⇒ **DỪNG, không vá**.
**F lần 3** = land lần nữa mà không có `run_id` của một lượt Windows xanh trên exact head. `W3`
sinh ra chính để chặn nó.

## `chua_do_duoc`

1. **Nguyên nhân gốc chưa đo** — hai giả thuyết ở trên **chưa cái nào được kiểm**.
2. **Container không tái hiện được Windows.** Mọi kết luận về Windows phải đến từ một lượt
   `workflow_dispatch`, không từ suy luận.
3. **`gh` thật vẫn chưa được đo lần nào** — kế thừa từ `#227`, không đóng ở đây.
