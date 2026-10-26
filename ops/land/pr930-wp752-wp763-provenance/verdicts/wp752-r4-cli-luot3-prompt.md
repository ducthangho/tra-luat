# Cross-review packet #752 (`NO-P3-CONG-CU-HO-SO`) — lượt CLI THỨ 3, khác nền (Codex review mã do Claude viết)

Bạn là reviewer độc lập. Executor là Claude. Bạn KHÔNG sửa mã trong mirror; bạn ĐO và CHẤM.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

- Mirror: thư mục làm việc hiện tại (`--cd`), git detached đúng `reviewed_sha` =
  `9d34a8e7e97fdc8ac178fc209219cea067e4c279`. Kiểm `git rev-parse HEAD` trước tiên; khác ⇒ dừng, ghi vào VERDICT.
- Base: `1797c32530fba381afd4009340a3fa558b7e37b0`. Diff cần chấm: `git diff 1797c32..9d34a8e`, đúng 4 tệp:
  `ops/kiem_ho_so_land.py`, `ops/kiem_ho_so_land_test.py`, `ops/kiem_nhan_hint.py`, `ops/kiem_nhan_hint_test.py`.
- Đặc tả đóng băng: `ops/specs/no-p3-cong-cu-ho-so-r4.md` trong chính mirror, sha256
  `a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791`. Đo băm trước khi đọc; lệch ⇒ dừng.
  Đọc TOÀN BỘ đặc tả: mục tiêu, tiêu chí nghiệm thu (B1…B7), đường land, giới hạn.

## Bối cảnh các lượt trước (để làm mục ĐỐI CHIẾU LƯỢT TRƯỚC — BẮT BUỘC)

- Lượt CLI 1 (run `43502cca`, head `f9b3dc1`): `changes_requested`, F752-01 [P2] và F752-02 [P2]. Verdict:
  `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli3/goi/VERDICT-luot1.md` (sha256 `97b0770b08ec40889c65737163ce7dcfc55cb3740dc1abc5f009d6e529ee53e6`).
- Lượt CLI 2 (run `f8f838f0`, head `fc1bb3add70b7e7a2f17cdf4f940d7ce484b7053`): `changes_requested`; F752-01 ĐÃ VÁ THẬT;
  F752-02 VÁ SINH LỖI MỚI ⇒ **F752-03 [P2]**: ca tự kiểm `ca_tu_kiem_bo_qua_symlink` gán đè `_cho_phep_bo_qua` và luôn dựng
  `os.symlink`, nên bốn đột biến sống (t04 luôn tha, t05 không bao giờ tha, t06 đảo nền, t08 `return` sớm khi API vắng).
  Verdict: `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli3/goi/VERDICT-luot2.md` (sha256 `8410d08121342ee97c2e8f0fc8b1f7819b5f38d576f3ccfaf63d710a30163a28`).
  Đo băm hai tệp verdict trước khi dùng.
- Executor khai đã vá F752-03 ở `9d34a8e` (diff `git diff fc1bb3a..9d34a8e`, chỉ `ops/kiem_nhan_hint_test.py`): giữ nguyên
  `_cho_phep_bo_qua` thật; thay `os` CỦA MODULE test bằng proxy cục bộ (`name` `nt`/`posix`; `symlink` ném PermissionError
  hoặc VẮNG); kỳ vọng độc lập theo ma trận 4 ô; khai 9/9 đột biến t01..t09 chết đúng ca tự kiểm.
- Connector P2 `4369279124` (lỗi dựng scalar YAML): lượt 1 và 2 xếp ĐÃ VÁ THẬT — đo lại trên `9d34a8e`.

Với MỖI finding F752-01, F752-02, F752-03, `4369279124`: xếp ĐÚNG MỘT trạng thái ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI /
CHƯA VÁ, kèm phép đo (chạy lại các đột biến t01..t08 của lượt 2 trên `9d34a8e`). Soi riêng xem bản vá F752-03 có mở đường
nào khác cùng hình dạng "ca test tuyên bố đo một điều mà thật ra không đo" không — ví dụ proxy che mất một thuộc tính mà ca
thật dùng, ma trận bỏ sót một tổ hợp, hay ca symlink THẬT trên Linux còn gọi công cụ đúng một lần và kiểm rc 3.

## Đỏ CÓ KIỂM SOÁT — không phải finding

Theo đường land A của đặc tả, trên head riêng của #752 thì `gate-registry` và `gate-ops` (ca `k01`) ĐỎ vì hai test
mới chưa đăng ký trong `.claude/dev/ci_dang_ky_test.py` (việc của packet #763). Đừng chấm điều đó là finding. Nhưng
nếu bạn đo được rằng đỏ ở đó vì lý do KHÁC, đó là finding.

## Thang chấm (nghiêm)

- P1: hành vi sai/thiếu an toàn chạm hợp đồng của đặc tả; P2: vi phạm một tiêu chí nghiệm thu, hoặc một lời khai
  (docstring, chú thích, thông điệp) mà phép đo bác bỏ, hoặc một ca test không đo điều nó tuyên bố (ca "có mặt" mà
  không "có đo"); P3: còn lại. Chỉ P1/P2 chặn merge.
- Mọi finding phải có PHÉP ĐO chạy được (lệnh + đầu ra), không suy từ đọc mã.

## Việc phải làm (đo, không đọc)

1. Chạy `python3 -B ops/kiem_ho_so_land_test.py` và `python3 -B ops/kiem_nhan_hint_test.py`; ghi dòng `N/N`.
2. Chạy hai công cụ trên chính mirror: `python3 -B ops/kiem_ho_so_land.py --root . --json` và
   `python3 -B ops/kiem_nhan_hint.py --root . --json`; đối chiếu số đếm với tiêu chí của đặc tả.
3. ĐỘT BIẾN BẢN VÁ để đo răng: chép công cụ + test vào một thư mục tạm (`mktemp -d -p <thư mục gói>`), mỗi lần đổi
   một chốt (ví dụ quay `except Exception` về `except yaml.YAMLError`; đổi `fullmatch` thành `match`; bỏ kiểm
   `startswith`; đổi `landed is not True` thành `not landed`), chạy bộ test trên bản sao, ghi ca nào đỏ. Đột biến
   sống sót ⇒ xét xem có phải ca test thiếu răng (finding) không. KHÔNG sửa tệp trong mirror.
4. Đối chiếu từng tiêu chí B1…B7 của đặc tả với phép đo; ghi bảng.
5. Hướng thử nào cần SOẠN nội dung dạng đường dẫn thoát khỏi cây thư mục hay tải trọng tấn công: đừng soạn —
   MÔ TẢ BẰNG LỜI trong VERDICT để phiên điều phối tự viết.

## Ràng buộc an toàn — vi phạm là hỏng lượt

- Chỉ ghi vào thư mục gói: `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli3/goi`. Không ghi, không xoá, không chuyển hướng tới bất kỳ tệp thiết bị hay đường dẫn
  hệ thống nào; không chạy `rm` trên đường dẫn ngoài thư mục gói. Không đọc tệp bí mật (`*.enc`, `*token*`,
  `*cookie*`, `credentials*`, `auth.json`). Không gọi mạng ngoài `git` cục bộ. Không `git push`, không sửa ref.

## Đầu ra

Ghi `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli3/goi/VERDICT.md` TĂNG DẦN (ghi phần đầu ngay, bổ sung sau mỗi bước — lượt có thể bị ngắt). Cấu trúc:

```
---
verdict: approve | changes_requested
reviewed_sha: 9d34a8e7e97fdc8ac178fc209219cea067e4c279
spec_sha256: a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791
so_p0: <n>
so_p1: <n>
so_p2: <n>
so_p3: <n>
---
## ĐỐI CHIẾU LƯỢT TRƯỚC
## Bảng đo lại        (lệnh · đầu ra · khớp/lệch)
## Đột biến           (tên · chốt đổi · ca đỏ · giết/sống)
## Findings           (mỗi finding một tiêu đề `### <id> [P1|P2|P3] <tóm tắt>` + phép đo + đề xuất sửa)
## chua_do_duoc       (những gì không đo được và vì sao)
```

`verdict: approve` chỉ khi 0 P0/P1/P2. Khi xong, in đúng một dòng ra stdout:
`XONG VERDICT sha256=<sha256 của VERDICT.md>`.
