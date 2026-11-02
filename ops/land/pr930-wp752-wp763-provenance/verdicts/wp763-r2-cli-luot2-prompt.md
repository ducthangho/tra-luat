# Cross-review packet #763 (`NO-P3-DANG-KY-CI`) — lượt Codex CLI THỨ 2, khác nền (Codex review mã do Claude viết)

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

## Lượt trước (BẮT BUỘC mục ĐỐI CHIẾU LƯỢT TRƯỚC)

- Connector Codex trên PR #930 review `b0fadc9`: không finding.
- Lượt CLI 1 (run `c4103982`, cùng head `b0fadc9`): `changes_requested`, **0 finding** ở mọi mức; lý do duy nhất là C8
  không tái lập được trong sandbox (bind Unix socket bị chặn ⇒ ca `t20zo_la_khong_phai_tep_thuong_do` hỏng, 5 đột biến
  not_measured). Verdict: `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review763cli2/goi/VERDICT-luot1.md` (sha256 `dfe0dda1b5adf68aab940d222e69d288440bcc278d6e499371d2311cf985dd52`;
  đo băm trước khi dùng).
- Chủ kho cho lời gọi thứ 3 (issuecomment-6400666225): lượt này **nhận log CI làm bằng chứng C8**.

## Bằng chứng C8/C6 từ CI thật — ĐO, đừng tin

Thư mục `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review763cli2/goi/ci/` có, tải bằng REST API GitHub ngay trước lượt này:
- `gate-ops-job-121216017879.json` + `.log` (sha256 log `fe84bbc37dc811575a332909ea45cb35a493145a6b3d2c7aef00d87f8f6d066b`)
- `gate-registry-job-121216491297.json` + `.log` (sha256 log `7de94edcc4ae781e47521e54823530fb62524222aaf8a253c0133829273479f7`)
Tự kiểm: (a) JSON job mang `head_sha` = `b0fadc9…`, `conclusion: success`, nhãn runner; (b) log cho thấy runner checkout
`refs/remotes/pull/930/merge` = `e909953`, commit GitHub tự dựng "Merge b0fadc9 into cdc4e80…". Commit `e909953` KHÔNG có
trong mirror. Hãy chứng minh hoặc bác: vì `cdc4e80` là tổ tiên của `b0fadc9` (đo bằng `git merge-base --is-ancestor`),
cây của merge ấy phải bằng cây `b0fadc9` — nêu rõ đây là SUY LUẬN từ quan hệ tổ tiên hay đo được, và mức tin cậy;
(c) đọc trong log `gate-ops` ba dòng `CA:` / `DOT BIEN:` / `TONG:` của `ops/ci_duong_nhanh_test.py` và đối chiếu C8;
(d) đọc trong log `gate-registry` hai dòng `CI_DANG_KY …: ĐẠT rc=0` (khớp toàn dòng sau khi bỏ tiền tố dấu thời gian),
dòng `CI_DANG_KY_THOI_GIAN` (một mục `duong_dan` cho từng khoá `MOI`, có cả hai khoá mới) và `TỔNG: ĐẠT` ⇒ C6.
Ghi rõ giới hạn: log là bản tải về, không phải phép chạy của bạn; bạn không kiểm được chữ ký của GitHub.
Bạn VẪN có thể chạy lại `--mot-ca` các ca không cần socket để đối chứng; đừng cố vượt sandbox.

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
- C6 và C8: chấm theo bằng chứng CI ở mục trên; nếu bằng chứng ấy không đủ thì nói thiếu gì, đừng tạo finding giả.

## Việc phải làm

1. Đo lại C1, C1b, C2 (CẢ HAI đột biến), C3, C4 (M3, M4, hai test thật — mẫu lấy từ `MOI` của chính tệp), C5, C7 (nếu
   có ruff), C8 trên mirror. Đột biến chạy trên BẢN SAO tạm (`mktemp -d -p <thư mục gói>`), KHÔNG sửa mirror.
2. Kiểm hai mục mới chép NGUYÊN byte dòng `nhanh` (chỉ khác khoá) và nằm liền ngay sau khoá `nhanh`.
3. Kiểm merge `b0fadc9`: không có thay đổi ngoài dự kiến trong `git diff cdc4e80 b0fadc9`; không tệp nào của `master`
   bị lùi bản.
4. Hướng thử nào cần SOẠN đường dẫn thoát khỏi cây thư mục hay tải trọng tấn công: đừng soạn — MÔ TẢ BẰNG LỜI.

## Ràng buộc an toàn — vi phạm là hỏng lượt

- Chỉ ghi vào thư mục gói: `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review763cli2/goi`.
  Không ghi, không xoá, không chuyển hướng tới bất kỳ tệp thiết bị hay đường dẫn hệ thống nào; không chạy `rm` trên
  đường dẫn ngoài thư mục gói. Không đọc tệp bí mật (`*.enc`, `*token*`, `*cookie*`, `credentials*`, `auth.json`).
  Không gọi mạng ngoài `git` cục bộ. Không `git push`, không sửa ref.

## Đầu ra

Ghi `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review763cli2/goi/VERDICT.md`
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
