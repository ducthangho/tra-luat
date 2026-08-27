# `CONG-NGOAI-WRITE-SET` — bộ test tự chấm chính mình là bộ test không ai chấm

Tách theo quyết định của người giữ kho ngày 2026-08-27. Nó **gộp hai nợ của hai packet khác nhau**,
vì đo ra thì chúng là **cùng một việc**.

## Hai nợ, một gốc

### Từ #319 (`MCP-GH-CUU-HO`) — nợ có tên `khong-cong-nao-chay-bo-test`

KHÔNG cổng nào trong kho chạy `.claude/dev/mcp_gh_test.py`. `ci.yml` **liệt kê từng `_test.py` bằng
tay** và tệp này không có trong danh sách; tìm `glob`/`rglob`/`**/*_test` trong
`.github/workflows/*.yml` cho **0** kết quả. Nên mọi con số `40/40`, `48/48` của packet ấy chỉ tồn
tại **khi có người gõ tay**.

`CLAUDE.md` đã chốt *"Workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai canh"*; ở đây còn
nhẹ hơn — **không có cả cái nút**.

### Từ #334 (`MANG-SANDBOX-CODEX`) — P1 `meta-test-tu-canh-khong-ai-canh`

Cross-review vòng 2 đo được: bộ đo của #334 có một lớp canh cổng (`t12_cong_dot_bien_tu_canh`), và
lớp ấy giết được năm phép xoá mà vòng 1 dùng để phá cổng. **Nhưng không ai canh chính `t12`.**
Vô hiệu hoá nó bằng **đúng một dòng** — bỏ lời gọi trong `main`, hoặc để thân hàm rỗng — thì **bốn
trong năm** phép xoá quay lại `TỔNG: ĐẠT`, `rc=0`.

Reviewer trả lời thẳng câu hỏi "đây là finding hay giới hạn không thể xoá": **finding**. Lý do
không phải triết lý mà là giá: *"vô hiệu hoá tầng bảo vệ tốn ĐÚNG MỘT dòng và KHÔNG ca nào phát
hiện."* Thêm một tầng canh nữa sẽ đóng ba trong bốn đường — không vô ích, nhưng chỉ đẩy bề mặt lên
tầng kế.

### Vì sao là CÙNG MỘT việc

Cả hai đòi đúng một thứ: **một cổng chạy các bộ test này từ NGOÀI write set của packet sở hữu
chúng.** Nguyên văn lập luận của reviewer #334:

> Đường thực sự khác họ, không dịch tầng: xác minh `probe_mang_test.py` (rc, VÀ chuỗi
> `"tự đột biến cổng: 9/9 chết"` trong stdout) từ một cổng NẰM NGOÀI write set của packet này —
> vì kẻ sửa đổi ba tệp trong write set của packet này không đồng thời sửa được cấu hình CI đó.

Đó cũng chính xác là thứ #319 thiếu. Một packet vá cả hai; hai packet thì vá hai lần cùng một cổng.

## Đây KHÔNG phải "thêm hai dòng vào ci.yml"

Nói trước để không ai ước lượng nhầm. Việc thật gồm:

1. **Chạy** `mcp_gh_test.py` và `probe_mang_test.py` trong CI.
2. **Đòi bằng chứng DƯƠNG, không chỉ `rc=0`.** Cả hai bộ đo đều có tiền sử in ra một dòng tổng kết
   xanh trong khi có ca đỏ ở trên. Cổng phải khớp chuỗi tổng kết mong đợi trong `stdout`, không chỉ
   đọc mã thoát — #319 vòng 3 đã cho thấy `rc` và bản in tách rời nhau được.
3. **Chống danh sách gõ tay.** `ci.yml` hiện liệt kê từng tệp; thêm hai dòng nữa là tái tạo đúng lỗ
   đã sinh ra nợ này. Cần một phép liệt kê tự động hoặc một chốt chặn khi có `_test.py` mới KHÔNG
   nằm trong danh sách.
4. **Phản chứng cho chính cổng ấy.** Nếu cổng CI mới cũng không có ai canh thì packet này chỉ dời
   lỗ lên tầng năm. Tối thiểu: một ca chứng minh cổng ĐỎ khi một bộ test bị gỡ khỏi danh sách, và
   một ca chứng minh cổng ĐỎ khi bộ test in dòng xanh mà mã thoát khác 0 (hoặc ngược lại).

## write set đề xuất

- `.github/workflows/ci.yml`
- một tệp phản chứng cho phép liệt kê, ví dụ `.claude/dev/ci_dang_ky_test.py` (viết mới)

**KHÔNG** lấy `.claude/dev/packet_loop.py` — xem ràng buộc dưới.

## RÀNG BUỘC — đọc trước khi cấp lease

Đo lúc 2026-08-27T07:0xZ bằng `ops/lease_publish.py ai-dang-giu`, sau khi so hai nguồn ref bằng
TẬP TÊN (229 = 229, `comm -3` RỖNG):

    .github/workflows/ci.yml        ->  NGƯỜI_GIỮ 1: ci-cong-idiom-ba-ten-exec-1r2-claude-20260827
    .claude/dev/packet_loop.py      ->  NGƯỜI_GIỮ 4
    .claude/dev/mcp_gh_test.py      ->  NGƯỜI_GIỮ 0
    .claude/dev/probe_mang_test.py  ->  NGƯỜI_GIỮ 1: mang-sandbox-codex-exec-1r2-codex-20260827

**Packet này CHƯA cấp lease được.** `ci.yml` đang có người giữ tới **2026-08-28T03:40:00Z**
(lease `ci-cong-idiom-ba-ten-exec-1r2`, write set `.claude/dev/idiom_py_test.py` + `ci.yml`).

`.claude/dev/packet_loop.py` có **BỐN** người giữ (`khoa-neo-be-rong` r2/r3/r7 và
`uy-quyen-merge-neo-hien-vat`) — đó là lý do write set đề xuất **tránh** nó. Con số 4 ấy cũng đáng
để #313 nhìn: ba trong bốn là các revision của cùng một chuỗi lease.

Hai tệp test mục tiêu thì **chỉ ĐỌC**, không sửa — nên việc `probe_mang_test.py` đang có người giữ
KHÔNG chặn packet này, miễn là nó không nằm trong write set.

## Thứ tự đúng

1. #334 vá nốt P1 rẻ còn lại (`bang-chinh-gom-unknown-vao-1-nhu-chan`) và land.
2. Lease `ci-cong-idiom-ba-ten-exec-1r2` kết thúc, nhả `ci.yml`.
3. Mới cấp lease cho packet này.

Cấp sớm hơn là cấp lease chồng — thứ mà chính kho đã trả giá để học.
