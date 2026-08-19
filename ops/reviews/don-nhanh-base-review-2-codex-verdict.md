verdict: changes_requested
reviewed_sha: 1511dd75a5a4f65c623738f2dc91e384b96bad9a

## Danh sách đóng được của lượt 1

Finding lượt 1: ĐÓNG.

Chạy lại `t10` với `gh` in `[]`, thoát `1`, rồi gọi `don-nhanh.ps1 -Xoa`: `rc=13` và danh sách nhánh remote trước/sau giống nhau, không có nhánh bị xoá.

## Findings

Hồi quy mới: `$tho = & gh ... 2>&1` trộn stderr vào JSON trước `ConvertFrom-Json`. Đo với tiến trình native trả `rc=0`, stdout là `[]`, stderr là `warning-from-gh`: chuỗi nhận được là `"[]\nwarning-from-gh"` và parse thất bại với `Additional text encountered...`. Vì vậy một cảnh báo stderr đi kèm JSON stdout hợp lệ làm thao tác hợp lệ bị từ chối.

Đường bình thường không bị chặn oan khi chỉ có `[]` trên stdout và `rc=0`: `t13` đạt, trả `rc=0` và xoá nhánh đích.

Không tìm được đột biến sống sót thứ năm khác trong đúng hai tệp thuộc phạm vi.

## Nợ khai báo

Lease có thẩm quyền không khớp yêu cầu lượt này:

- Snapshot SHA-256: `16778be2cce7a92fe154e4fd9659409233d6687da039415bafecef4390cfea6b`.
- `prompt_sha256_required` trong lease: `5fb34f0571fa10d0eae2b6b3f606f1820f44ced8ab6c87ec0b6a41431090d2d1`.
- Lease vẫn yêu cầu `reviewed_sha_required: 5bc635d2ea64bcedd41378cc33c6b4cdbf03f164`, không phải HEAD đã đọc.

Lời khai về `$PSBoundParameters.ContainsKey` đúng với mục tiêu phân biệt “không truyền” và “có truyền giá trị rỗng”. Truyền `-ThoNguyen $null` tường minh được xem là đã truyền và trở thành chuỗi rỗng; đây vẫn mô phỏng đúng ca đầu ra rỗng, không mở lỗ trong helper test.

## Phép đo đã chạy

- `git rev-parse HEAD` → `1511dd75a5a4f65c623738f2dc91e384b96bad9a`.
- Xác nhận delta mã chỉ gồm `scripts/don-nhanh.ps1` và `scripts/don-nhanh_test.ps1`.
- `pwsh 7.4.6`, `TMPDIR=/dev/shm`.
- `don-nhanh_test.ps1` → `13/13 đạt`, sau khi vô hiệu cấu hình ký commit Git của môi trường.
- `t10`: `gh rc=1` + JSON hợp lệ → `rc=13`, remote không đổi.
- `t12`: `gh rc=0` + đầu ra rỗng → từ chối.
- `t13`: `gh rc=0` + `[]` → `rc=0`, xoá bình thường.
- Phép đo stderr riêng: `rc=0`, stdout `[]`, stderr cảnh báo → `ConvertFrom-Json` thất bại.
- Kiểm `$PSBoundParameters`: không truyền → `ContainsKey=False`; truyền `$null` hoặc `''` → `ContainsKey=True`, giá trị chuỗi rỗng.
