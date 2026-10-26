# Cross-review packet #763 (`NO-P3-DANG-KY-CI`) — lượt Codex CLI, khác nền (Codex review mã do Claude viết)

Bạn là reviewer độc lập. Executor là Claude. Bạn KHÔNG sửa mã trong mirror; bạn ĐO và CHẤM.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

- Mirror: thư mục làm việc hiện tại, git detached đúng `reviewed_sha` = `b0fadc96366115d3545b9c723b30f04281898d94`
  (head GỘP của PR #930). Kiểm `git rev-parse HEAD` trước tiên; khác ⇒ dừng, ghi vào VERDICT.
- Lịch sử: base packet `9d34a8e7e97fdc8ac178fc209219cea067e4c279` (head đã duyệt của #752); commit packet `7a7d52d`
  (thêm 2 dòng `MOI` vào `.claude/dev/ci_dang_ky_test.py`); merge commit `b0fadc9` nhận `master` `cdc4e80`
  (ke_hoach_rebase của lease: merge, không rebase).
- Phần CHẤM CHÍNH: `git diff 9d34a8e 7a7d52d` (đúng 1 tệp, numstat `2 0`) VÀ việc merge `b0fadc9` không làm hỏng gì:
  `git diff cdc4e80 b0fadc9` phải đúng 5 tệp — 4 tệp của #752 (`ops/kiem_ho_so_land*.py`, `ops/kiem_nhan_hint*.py`,
  đã được duyệt riêng ở biên nhận `cross_approved` lượt 3 của #752, KHÔNG chấm lại nội dung) + tệp sổ.
- Đặc tả đóng băng: `ops/specs/no-p3-dang-ky-ci-r2.md` trong mirror, sha256
  `30776483ab40e57708c6b03ba0877bc3f40dd27edf334e7dceb0fe5629a113e2`. Đo băm trước khi đọc. Đọc mục "Mục tiêu" và
  "Nghiệm thu" (C1…C8, bảng "Soát L6"); các mục "Vá sau review" là lịch sử.

## Lượt trước

Connector Codex trên PR #930 review `b0fadc9`: không finding (`has_any_findings: false`). Không có finding cũ nào để
đối chiếu; ghi mục ĐỐI CHIẾU LƯỢT TRƯỚC với nội dung ấy.

## Lời khai của executor (đo lại, đừng tin)

Trên head packet `7a7d52d`: C1 rc 0, 0 dòng `ĐỎ:`, `ĐĂNG KÝ: 26/26` (nền S1 trên `9d34a8e`: `26/24`),
`PHẢN CHỨNG: 1070/1070 đỏ đúng` (đặc tả ghi 1064 trên `1d7e642`; executor khai đổi vì commit `518fa0c` của #892 sửa tệp
sổ +15/−3), `TỔNG: ĐẠT`, numstat `2 0`; C1b `True 12`; C2 hai đột biến gỡ từng mục ⇒ `26/25` + đúng một dòng `ĐỎ:`; C3
tên sai ⇒ hai dòng `ĐỎ:` đúng nội dung; C4 `chay_moi` thật ⇒ hai dòng `CI_DANG_KY …: ĐẠT rc=0`, M3/M4 ⇒ ĐỎ; C5 hai tệp
là blob trên base; C7 ruff sạch. Trên head gộp `b0fadc9`: C1 `26/26` · `1070/1070` · `TỔNG: ĐẠT`; C1b `True 12`; C8
`CA: 104/104` · `DOT BIEN: 392/392` (đặc tả ghi 384 trên `1d7e642`) · `TONG: DAT`.
Kiểm từng lời khai bằng phép đo của bạn; kiểm riêng hai lý do "số đổi so với đặc tả" có đúng không.

## Thang chấm (nghiêm)

- P1: hành vi sai/thiếu an toàn chạm hợp đồng của đặc tả; P2: vi phạm một tiêu chí nghiệm thu, hoặc một lời khai của
  executor/commit/PR mà phép đo bác bỏ; P3: còn lại. Chỉ P1/P2 chặn merge.
- Mọi finding phải có PHÉP ĐO chạy được (lệnh + đầu ra), không suy từ đọc mã.
- C6 (CI thật trên GitHub) KHÔNG đo được trong lượt offline này: ghi vào `chua_do_duoc`, không chấm.

## Việc phải làm

1. Đo lại C1, C1b, C2 (CẢ HAI đột biến), C3, C4 (M3, M4, hai test thật — mẫu lấy từ `MOI` của chính tệp), C5, C7 (nếu
   có ruff), C8 trên mirror. Đột biến chạy trên BẢN SAO tạm (`mktemp -d -p <thư mục gói>`), KHÔNG sửa mirror.
2. Kiểm hai mục mới chép NGUYÊN byte dòng `nhanh` (chỉ khác khoá) và nằm liền ngay sau khoá `nhanh`.
3. Kiểm merge `b0fadc9`: không có thay đổi ngoài dự kiến trong `git diff cdc4e80 b0fadc9`; không tệp nào của `master`
   bị lùi bản.
4. Hướng thử nào cần SOẠN đường dẫn thoát khỏi cây thư mục hay tải trọng tấn công: đừng soạn — MÔ TẢ BẰNG LỜI.

## Ràng buộc an toàn — vi phạm là hỏng lượt

- Chỉ ghi vào thư mục gói: `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review763cli/goi`.
  Không ghi, không xoá, không chuyển hướng tới bất kỳ tệp thiết bị hay đường dẫn hệ thống nào; không chạy `rm` trên
  đường dẫn ngoài thư mục gói. Không đọc tệp bí mật (`*.enc`, `*token*`, `*cookie*`, `credentials*`, `auth.json`).
  Không gọi mạng ngoài `git` cục bộ. Không `git push`, không sửa ref.

## Đầu ra

Ghi `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review763cli/goi/VERDICT.md`
TĂNG DẦN. Cấu trúc:

```
---
verdict: approve | changes_requested
reviewed_sha: b0fadc96366115d3545b9c723b30f04281898d94
spec_sha256: 30776483ab40e57708c6b03ba0877bc3f40dd27edf334e7dceb0fe5629a113e2
so_p0: <n>
so_p1: <n>
so_p2: <n>
so_p3: <n>
---
## ĐỐI CHIẾU LƯỢT TRƯỚC
## Bảng đo lại        (tiêu chí · lệnh · đầu ra · khớp/lệch với lời khai)
## Đột biến
## Findings           (mỗi finding một tiêu đề `### <id> [P1|P2|P3] <tóm tắt>` + phép đo + đề xuất sửa)
## chua_do_duoc
```

`verdict: approve` chỉ khi 0 P0/P1/P2. Khi xong, in đúng một dòng ra stdout:
`XONG VERDICT sha256=<sha256 của VERDICT.md>`.
