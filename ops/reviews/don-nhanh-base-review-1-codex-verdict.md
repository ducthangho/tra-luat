verdict: changes_requested
reviewed_sha: 5bc635d2ea64bcedd41378cc33c6b4cdbf03f164

## Findings

- `gh` thoát khác 0 nhưng in JSON hợp lệ làm fail-close bị mở. `scripts/don-nhanh.ps1` không kiểm `$LASTEXITCODE` ngay sau `gh`; `ConvertFrom-Json` vẫn thành công, `$doDuocPR = $true`, rồi nhánh đã merge bị xoá. Trên bản sao `git archive`, tôi thêm ca `gh` in `[]`, `exit 1`: script trả `rc=0` và xoá `ops/xong-viec`, trong khi ca đòi `rc=13` và remote không đổi. Kết quả: `0/1 dat`. Bộ gốc vẫn `9/9`, nên đây là đường lỗi sống sót ngoài chín ca hiện tại. Cần kiểm mã thoát native ngay sau lời gọi `gh` trước pipeline/JSON parsing và chỉ đặt `$doDuocPR = $true` khi cả mã thoát lẫn payload hợp lệ.

## Nợ khai báo

- `gh` giả in cùng một JSON trong suốt một ca là mô hình trạng thái PR bất biến, không phụ thuộc số thứ tự lời gọi; không phải đồ giả diễn kịch bản.
- Tên ref Git không cho phép `*`, `?`, `[` hoặc `\`, nên glob injection từ tên head/base PR không khả thi với ref hợp lệ. Phép PowerShell xác nhận `"x-other" -like "x*"` là `True`, nhưng `x*` không thể là tên ref Git. Với `-GiuThem`, glob là giao diện hiện hữu có chủ đích và chỉ làm giữ rộng hơn.
- Chốt fail-close nằm trước vòng duy nhất gọi `git push --delete`; không thấy đường xoá nào vượt chốt.
- `-BoQuaLopPR` không tác động khi danh sách PR đã đọc thành công là đúng với mô tả “bỏ qua khi không đọc được”, không phải hồi quy giao diện.
- CI gọi `pwsh` lồng nhau, nhưng phép thử tiến trình trong `exit 7` làm tiến trình ngoài trả mã khác 0 (`rc=1`), nên runner vẫn đỏ.
- Lần chạy đầu của `don-nhanh_test` hỏng do sandbox khóa `/tmp`; chạy lại với `TMPDIR=/dev/shm` và tắt cấu hình ký commit toàn cục thì đạt. Đây là hạn chế môi trường review, không phải lỗi CI.
- `release-verify` trực tiếp trong worktree đỏ duy nhất vì `nhiem_vu.txt` ngoài manifest; chạy trên `git archive` của đúng SHA thì sạch.
- `tl --selftest` trên nhánh và nền: KHÔNG ĐO ĐƯỢC đáng tin cậy trong harness này; lượt chạy so sánh không trả báo cáo có thể diễn giải, nên tôi không xác nhận hay bác lời khai `pyo3_runtime.PanicException`.

## Phép đo đã chạy

- `git rev-parse HEAD` → `5bc635d2ea64bcedd41378cc33c6b4cdbf03f164`.
- `git diff --stat 1a6aedf6b92ff271bf07a8b9deee2f83d430ed49..HEAD` → 6 tệp, `362 insertions`, `16 deletions`.
- `sha256sum prompt.snapshot` → `5fb34f0571fa10d0eae2b6b3f606f1820f44ced8ab6c87ec0b6a41431090d2d1`, khớp `prompt_sha256_required` trong lease.
- `pwsh --version` → PowerShell `7.4.6`.
- `TMPDIR=/dev/shm ... pwsh -NoProfile -File scripts/don-nhanh_test.ps1` → `9/9 dat`, rc=0.
- Ca bổ sung trên bản sao: `gh` in `[]`, thoát 1, chạy `don-nhanh.ps1 -Xoa` → script rc=0, nhánh đã bị xoá; test `0/1 dat`.
- `actionlint .github/workflows/*.yml` → rc=0 trên 5 workflow.
- Phép `pwsh` lồng, tiến trình trong `exit 7` → tiến trình ngoài rc=1.
- `python3 ops/lease_publish_test.py` → `31/31 đạt`, rc=0.
- `python3 scripts/tl.py golden-test --json` trên `git archive` → `ok=true`, 20/20, rc=0.
- `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trên `git archive` → `ok=true`, checked=179, failed=0, extra=0, rc=0.

