verdict: approve
reviewed_sha: 525c824e29cdf035af5b4061ffd492be0a783f4a

## Findings

Không có hồi quy, lỗ an ninh mới, hoặc P1 làm workflow không chạy được được phát hiện.

## Nợ khai báo

- Bộ test thường trực chưa khóa hai biên `luu-tru-gia/*` và `xluu-tru/*`. Phép thử bổ sung tạm thời cho cả hai đều QUA; đây không phải lỗi của mã hiện tại.
- `actionlint`: **KHÔNG ĐO ĐƯỢC** vì môi trường không có binary. Không dùng PyYAML để thay thế kết luận này.

## Phép đo đã chạy

- Xác thực nguồn:

  - Prompt SHA-256: `0f969a94f66d2a80a90282daaaf645fa47cfdf035a1de6389ceac0676f885208`, khớp lease.
  - Hai tệp phạm vi trong worktree khớp từng byte với commit được review.
  - Diff `f9730f6..525c824`: đúng `.github/workflows/ops-don-ref.yml` và `ops/don_ref_chot_test.sh`, `+36/−4`.

- `bash ops/don_ref_chot_test.sh`: `81/82`; chỉ đỏ phép `actionlint` fail-close.

- Nền `f9730f6` trên bản sao tạm: `73/74`; chỉ đỏ vì thiếu `actionlint`. Vì vậy phần đo được vẫn là nhánh `81` so với nền `73`, delta `+8`, không có ca chức năng đỏ.

- Phạm vi mở:

  - `tao-tag luu-tru/x` và `tao-tag LUU-TRU/x`: QUA.
  - `xoa-tag luu-tru/x`: DỪNG `rc=2`, kể cả khi giả lập có tag giữ cùng commit.
  - `xoa-nhanh luu-tru/*`: chỉ QUA khi đọc được SHA nhánh và danh sách tag có SHA ấy; không tag, không đọc được SHA, hoặc lỗi giữa phân trang đều DỪNG.
  - `tao-tag ops/*`, `claude/*`, `codex/*`, `agent/*`, `mission/*`, `dispatcher/*`: vẫn DỪNG.
  - Việc thường hóa bằng `tr` khiến `LUU-TRU/*` có cùng chính sách với chữ thường.
  - Hai ca bổ sung: `tao-tag luu-tru-gia/x` và `tao-tag xluu-tru/x` đều QUA, xác nhận không khớp oan tiền tố.

- Hai đột biến được neo vào toàn bộ khối `case` của riêng `tao-tag`:

  - Cấm lại `luu-tru/*`: `79/82`; ngoài lỗi thiếu `actionlint`, đỏ đúng hai ca chữ thường và chữ hoa vốn phải QUA. Tương đương `80/82` khi có `actionlint`.
  - Gỡ `codex/*` khỏi danh sách cấm: `80/82`; ngoài lỗi thiếu `actionlint`, đỏ đúng ca `tạo tag codex/ vẫn DỪNG`. Tương đương `81/82` khi có `actionlint`.

- Lập luận “đặt tên khác”:

  Chốt `xoa-nhanh` thực sự chỉ so SHA và không kiểm tên tag, nên một tag tên khác vẫn giúp thao tác xoá nhánh qua về mặt kỹ thuật. Tuy nhiên `CLAUDE.md` khai `luu-tru/*` là không gian ref bền duy nhất cho commit công bố verdict. Vì vậy “đặt tên khác” phá quy ước lưu trữ dù vượt qua được chốt; bản vá là cần thiết để trình tự chính thức tuân thủ quy ước đó.
