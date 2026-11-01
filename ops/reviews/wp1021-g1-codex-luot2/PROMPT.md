# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 2 (lời gọi Codex 2/4 theo lease)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `5efa311fd857f7657a1c687e9ea37693070a37d3`. Base (lúc cấp lease) `757bde561d09738858506aecf5de2f050a5f0d5e` = `origin/master`.
- `SPEC.md` — đặc tả đóng băng r2 (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- `DIFF.patch` — `git diff 757bde5..HEAD` (`ops/bien_nhan_v2.py` +26/−3, `ops/bien_nhan_v2_test.py` +148).
- `DIFF-LUOT2.patch` — `git diff 99c463d..HEAD` (bản vá sau lượt 1).
- `VERDICT-LUOT1.md` — verdict lượt 1 của bạn trên `99c463d`: request_changes, hai P2
  `loi-do-liet-ke-thu-muc-thoat-traceback` và `bo-chon-ung-vien-thieu-rang-hai-duong-goi`.

Chủ kho đã duyệt làm tiếp sau chốt dừng `bo-chon-ung-vien` của SPEC (30-10-2026). Ghi chú lease (dữ liệu): nền C6 = `tổng 306`;
C7 (Windows local) theo ADR-0057/0058.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến trên BẢN SAO ĐỦ CÂY, mỗi đột biến một tiến trình.

## Thay đổi từ lượt 1 (executor khai — hãy ĐO)
1. `_chon_bien_nhan`: phép liệt kê bọc `try`; `OSError` ⇒ `KhongDoDuoc("không liệt kê được <thư mục> (...)")` (rc=2). Không
   bắt `Exception`, không trả rỗng khi lỗi; thư mục vắng vẫn `[]`. `return sorted(ds)`.
2. Ca mới `c99` bốn chốt: (1) `--sinh-no` thấy `X.RECEIPT.YAML` (rc=0, khối nợ nêu tên, `# 1 tệp`); (2) `Path.iterdir` bị ép trả
   NGƯỢC mà helper vẫn trả đã sắp xếp; (3) kho thật thiếu `ops/reviews`: `kiem` rc=2, `--sinh-no` rc=0 `# 0 tệp`; (4)
   `Path.iterdir` ném `PermissionError` trên đúng thư mục biên nhận ⇒ cả `kiem` lẫn `--sinh-no` rc=2, nêu "không liệt kê được",
   không traceback.
3. Đột biến mới: `m144` (lọc đuôi chính xác ở `_sinh_no`), `m145` (bỏ `sorted`), `m146` (bỏ nhánh thư mục vắng), `m147` (bỏ bắt
   `OSError`) — tất cả nhắm `c99`. `m142`/`m143` đổi mốc neo theo mã mới.
4. `c98`/`c99`: `except LoiDungCa: raise` trước `except Exception`, để giàn giáo hỏng không đội lốt "ca đỏ".

## Bằng chứng ngoài sandbox (dữ liệu, không phải phép đo của bạn)
- Executor đo Linux trên `5efa311`: `bien_nhan_v2_test: 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`;
  `bien_nhan_v2 --root .` `tổng 306`, `TỔNG: ĐẠT`; `--sinh-no` `# 42 tệp`.
- CI trên head cũ `99c463d`: Ubuntu run 41031052871 và Windows dispatch run 41031049365 đều success (`95/95 · 139/139`,
  `lease_publish` 268/268 Ubuntu, 255/255 + 13 bỏ qua khai báo Windows). CI trên `5efa311` đang chạy.
- Bạn không có Windows: phần chỉ Windows đo được ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: với mỗi P2 lượt 1, chạy lại ĐÚNG phép tái hiện bạn đã dùng (`luot1-probe/listing_probe.py`; `luot1-probe/mutate.py sinh_exact |
   nosort | noguard --suite`, bản chép từ sandbox lượt 1 — có thể phải chỉnh đường dẫn/mốc neo theo mã mới, ghi rõ chỉnh gì) trên head mới. Đòi: lỗi liệt kê nay rc=2 không traceback ở cả hai đường; ba đột biến nay CHẾT và
   chết đúng chốt của `c99` (đọc tên ca + thông báo, không chỉ rc).
2. Toàn suite trên head (đòi `TỔNG: ĐẠT`, N/N bằng nhau).
3. Tiêu chí C1a, C1b, C2, C3, C6, C9 của SPEC trên head mới.
4. Tự nghĩ đột biến cho phần MỚI và báo cái nào SỐNG, vì sao. Gợi ý: bắt `Exception` thay `OSError` (che lỗi lập trình — có ca nào
   phân biệt không?); chốt (4) của `c99` có thể qua vì lý do khác (ví dụ `resolve()` trên Windows/symlink làm điều kiện tiêm
   không bao giờ đúng) — tức tiêm KHÔNG có hiệu lực mà ca vẫn xanh; chốt (2) có đo thật thứ tự hay chỉ đo phép ép.
5. `c99` có rò rỉ toàn cục (`Path.iterdir` không được trả lại khi ca ném lỗi giữa chừng) sang ca sau không?
6. Phạm vi: diff chỉ hai tệp write set; `git diff --check`; ruff `--select F` delta 0 so base;
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 5efa311fd857f7657a1c687e9ea37693070a37d3`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng tiêu chí, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> —
<hướng vá>` kèm dòng `HÌNH DẠNG:` (`loi-do` / `bo-chon-ung-vien` / `khac`). Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm
lệnh và output; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
