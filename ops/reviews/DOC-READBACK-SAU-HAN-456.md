# READBACK SAU HẠN — lease #456 hết hiệu lực lúc 14:30:07Z

Mục đích: cung cấp đúng thứ verdict lượt 12 nói là còn thiếu.

> `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1] … **Đây chưa phải readback sau hạn hoặc quét đủ máy chủ**
> — `ops/reviews/pr468-hoso-4-packet-review-12-codex-verdict.md`, dòng 14

Reviewer đo lúc `2026-09-07T13:15:45.214989Z`, tức **TRƯỚC** hạn, nên chỉ mô phỏng được. Bản ghi
này là phép đo THẬT trên máy, sau hạn.

## Kết luận

P1 `bia-mo-mot-ref-khong-thu-hoi-moi-ban` **ĐÃ ĐÓNG**, đóng bằng THỜI GIAN đúng như dự báo,
không phải bằng bản vá. Không ai đặt bia mộ; lease #456 đơn giản là hết hạn.

## Số đo

Giờ đo: `2026-09-07T14:39:17Z` — sau hạn `2026-09-07T14:30:07Z` **9 phút 10 giây**.

### Canh ref hai nguồn (fail-close)

| nguồn | lệnh | số ref |
|---|---|---|
| A | `git ls-remote --heads origin` | **303** |
| B | `git for-each-ref refs/remotes/origin` (bỏ symref `HEAD`) | **303** |

`comm -3 A B` ⇒ **0 dòng**. So như TẬP HỢP, không so `wc -l`. Lệch ⇒ ĐỎ; ở đây không lệch.
Tổng ref được `ai-dang-giu` quét (`refs/heads` + `refs/remotes/origin`): **306**.

Ghi chú phép đo: lần chạy đầu B ra **304** vì `%(refname:short)` của `refs/remotes/origin/HEAD`
rút gọn thành `origin` chứ không phải `HEAD`, nên bộ lọc `grep -v '^HEAD$'` trượt. Đã lọc lại bằng
`%(symref)` rỗng. Chênh lệch ấy là lỗi của bộ lọc, không phải của kho.

### Người giữ, sau hạn

| đường ghi | NGƯỜI_GIỮ | tên | rc |
|---|---|---|---|
| `.claude/dev/ci_dang_ky_test.py` | **1** | `gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906` | 11 |
| `.claude/hooks/pretooluse_guard_test.py` | **0** | không có | 0 |
| `.github/workflows/ci.yml` | **1** | `gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906` | 11 |

`rc=11` nghĩa là CÓ người giữ, không phải lỗi.

### Bằng chứng dương rằng #456 hết hạn chứ không phải biến mất

`ai-dang-giu .claude/dev/ci_dang_ky_test.py` vẫn in **2** dòng mang tên
`mutant-khong-chay-tren-windows-exec-1-claude-20260906`; trạng thái của cả hai là **`HẾT_HẠN`**,
tập trạng thái phân biệt = `{HẾT_HẠN}`, không có `CÒN_HẠN`. Tệp lease vẫn nằm trên hai ref —
nó rụng khỏi phép đếm vì hạn, không vì bị xoá hay bị bia mộ.

### Đối chiếu với mô phỏng của reviewer

| mốc | reviewer mô phỏng (13:15:45Z) | đo thật (14:39:17Z) | khớp? |
|---|---|---|---|
| registry sau 14:30:07Z | **1** | **1** | có |
| `ci.yml` sau 14:30:07Z | **1** | **1** | có |

Mô hình của reviewer dự báo đúng.

## Điều bản ghi này KHÔNG chứng minh

- Không chứng minh cơ chế bia mộ đã được sửa. **Chưa sửa gì cả.** Lỗ hổng
  `_kiem_bia_mo` dùng `any(...)` vẫn nguyên vẹn; nó chỉ thôi gây hại trên packet này vì
  lease hết giờ.
- Không đóng P1 còn lại `mirror-thieu-ref-khong-du-do-a9`. Bundle giao cho reviewer chỉ mang
  **3** tên nhánh, nên reviewer vẫn không tự tái đo được khẳng định 303/303 ở trên. Muốn đóng
  P1 ấy phải sửa cách dựng gói hiện vật, không phải chờ thêm.
- Không đóng hai P2 hồ sơ của lượt 12.
- Cùng lỗ hổng đang tái diễn ở packet `wp461`: hai lease CÒN HẠN cùng giữ y hệt bốn đường ghi,
  chạy tới `2026-09-08`. Đã lập phiên riêng để bổ sung cơ chế chủ kho thu hồi lease và cấp lại
  cho PR khác.
