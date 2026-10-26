# Cross-review packet #752 (`NO-P3-CONG-CU-HO-SO`) — lượt CLI, khác nền (Codex review mã do Claude viết)

Bạn là reviewer độc lập. Executor là Claude. Bạn KHÔNG sửa mã trong mirror; bạn ĐO và CHẤM.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

- Mirror: thư mục làm việc hiện tại (`--cd`), git detached đúng `reviewed_sha` =
  `f9b3dc1ec11a5089b06d67a658e0f840742466eb`. Kiểm `git rev-parse HEAD` trước tiên; khác ⇒ dừng, ghi vào VERDICT.
- Base: `1797c32530fba381afd4009340a3fa558b7e37b0`. Diff cần chấm: `git diff 1797c32..f9b3dc1`, đúng 4 tệp:
  `ops/kiem_ho_so_land.py`, `ops/kiem_ho_so_land_test.py`, `ops/kiem_nhan_hint.py`, `ops/kiem_nhan_hint_test.py`.
- Đặc tả đóng băng: `ops/specs/no-p3-cong-cu-ho-so-r4.md` trong chính mirror, sha256
  `a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791`. Đo băm trước khi đọc; lệch ⇒ dừng.
  Đọc TOÀN BỘ đặc tả: mục tiêu, tiêu chí nghiệm thu (B1…B7), đường land, giới hạn.

## Bối cảnh các lượt trước (để làm mục ĐỐI CHIẾU LƯỢT TRƯỚC)

Ba lượt connector Codex trên PR #918:
1. head `5208254`: một P2 (comment `4369279124`) — lỗi dựng scalar YAML (ví dụ `recorded_at: 2026-13-01`) ném
   `ValueError` thay vì `yaml.YAMLError`, làm cả lượt quét chết rc 1 kèm traceback thay vì ghi `LOI` rc 3.
   Executor khai đã vá ở `f9b3dc1` bằng cách bắt cả lớp ngoại lệ quanh đúng lời gọi `safe_load`, thêm ca
   `ca_b1b_scalar_hong` (4 dạng: tháng 13, `!!timestamp 'x'`, `!!int 'x'`, lồng sâu).
2. head `f9b3dc1`: không finding. 3. head `f9b3dc1` (tự chạy khi PR rời draft): không finding.
Với finding (1), xếp ĐÚNG MỘT trạng thái: ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ — kèm phép đo của bạn.

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

- Chỉ ghi vào thư mục gói: `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli/goi`. Không ghi, không xoá, không chuyển hướng tới bất kỳ tệp thiết bị hay đường dẫn
  hệ thống nào; không chạy `rm` trên đường dẫn ngoài thư mục gói. Không đọc tệp bí mật (`*.enc`, `*token*`,
  `*cookie*`, `credentials*`, `auth.json`). Không gọi mạng ngoài `git` cục bộ. Không `git push`, không sửa ref.

## Đầu ra

Ghi `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli/goi/VERDICT.md` TĂNG DẦN (ghi phần đầu ngay, bổ sung sau mỗi bước — lượt có thể bị ngắt). Cấu trúc:

```
---
verdict: approve | changes_requested
reviewed_sha: f9b3dc1ec11a5089b06d67a658e0f840742466eb
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
