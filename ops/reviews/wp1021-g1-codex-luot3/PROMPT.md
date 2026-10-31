# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 3 (lời gọi Codex 3/4 theo lease)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde`. Base (lúc cấp lease) `757bde561d09738858506aecf5de2f050a5f0d5e` = `origin/master`.
- `SPEC.md` — đặc tả đóng băng r2 (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- `DIFF.patch` — `git diff 757bde5..HEAD`; `DIFF-LUOT3.patch` — `git diff 5efa311..HEAD` (bản vá sau lượt 2).
- `VERDICT-LUOT1.md` (head `99c463d`), `VERDICT-LUOT2.md` (head `5efa311`, request_changes: P2
  `loi-do-liet-ke-thu-muc-thoat-traceback` biểu hiện `stat`/`is_dir`, P3 `loi-do-thieu-chot-ngoai-le-lap-trinh`).
- `luot2-probe/` — các script bạn tự viết ở lượt 2 (`review_new.py`, `new_mutate.py`, `boundary_oracle.py`, `probe.py`,
  `mutate.py`, `measure.py`, `listing_probe.py`…), chép nguyên. Có thể phải chỉnh đường dẫn/mốc neo theo mã mới; ghi rõ chỉnh gì.

Chủ kho đã duyệt làm tiếp sau chốt dừng `bo-chon-ung-vien` của SPEC (30-10-2026). Ghi chú lease (dữ liệu): nền C6 = `tổng 306`;
C7 (Windows local) theo ADR-0057/0058. Đây là lời gọi 3/4: còn đúng một lời gọi sau lượt này, nên hãy tìm HẾT đường vào
của cùng lớp lỗi trong một lượt, đừng dừng ở biểu hiện đầu tiên.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến trên BẢN SAO ĐỦ CÂY, mỗi đột biến một tiến trình.

## Thay đổi từ lượt 2 (executor khai — hãy ĐO)
1. Helper mới `_hoi_trang_thai(hoi, p)`: gọi `hoi()`, `OSError` ⇒ `KhongDoDuoc("không đọc được trạng thái <p> (...)")`.
   Chỉ bắt `OSError`. Dùng ở: phép hỏi `tm.is_dir` trong `_chon_bien_nhan`; guard `tm.is_dir` của `kiem`; phép hỏi
   `(root / ".git").exists` của guard ấy.
2. Ca mới `c100` ba chốt: (5) `Path.is_dir` của `ops/reviews` ném `PermissionError` ⇒ `kiem` và `--sinh-no` rc=2, nêu "không đọc
   được trạng thái", không traceback; (6) kho thiếu `ops/reviews`, `Path.exists` của `.git` ném ⇒ `kiem` rc=2 nêu `.git`; (7)
   `RuntimeError` mốc ở `iterdir` hoặc `is_dir` của `ops/reviews` ⇒ đúng đối tượng ấy ra khỏi `main` trên cả hai đường. Mỗi
   chốt có `dung(trung, …)` đòi phép tiêm đã trúng.
3. Đột biến `m148` (helper hỏi `is_dir()` trần), `m149` (guard `kiem` hỏi trần), `m150` (`_hoi_trang_thai` bỏ bắt `OSError`),
   `m151` (`.git` hỏi trần), `m152` (bắt liệt kê nới thành `Exception`), `m153` (`_hoi_trang_thai` nới thành `Exception`) —
   tất cả nhắm `c100`. `m146` đổi mốc neo theo mã mới.

## Bằng chứng ngoài sandbox (dữ liệu, không phải phép đo của bạn)
- Executor đo Linux trên `8d9e3e3`: `bien_nhan_v2_test: 97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`;
  `bien_nhan_v2 --root .` `tổng 306`, `TỔNG: ĐẠT`; `--sinh-no` `# 42 tệp`; ruff F delta 0.
- CI Ubuntu và Windows dispatch trên `8d9e3e3` đang chạy. Bạn không có Windows: phần chỉ Windows ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: với F1 và F2 lượt 2, chạy lại ĐÚNG phép tái hiện của bạn (`review_new.py error-child … stat-os |
   access | runtime | value`; `new_mutate.py broad | broad_literal`; `boundary_oracle.py`) trên head mới. Đòi: lỗi `stat` nay
   rc=2 không traceback ở cả hai đường; lỗi lập trình truyền ra; mutant bắt rộng nay chết đúng chốt `c100`. Phân loại mỗi finding
   cũ: ĐÃ VÁ THẬT / VÁ HỜ / CHƯA VÁ, kèm lệnh + output.
2. Toàn suite trên head (đòi `TỔNG: ĐẠT`, N/N bằng nhau).
3. Tiêu chí C1a, C1b, C2, C3, C6, C9 của SPEC trên head mới.
4. Tự liệt kê MỌI phép gọi hệ tệp trên đường đi của `kiem` và `--sinh-no` tới tập biên nhận (stat, liệt kê, `resolve`, đọc tệp,
   băm, `.git`…), đánh dấu cái nào packet này thêm hoặc đổi, và với mỗi cái: lỗi `OSError` ở đó ra rc=2 không traceback, hay
   thoát traceback, hay đã như vậy ở base (đo base để phân biệt hồi quy với lỗi sẵn có — lỗi sẵn có ngoài phạm vi write set
   KHÔNG tính finding của packet này, nhưng hãy liệt kê).
5. Tự nghĩ đột biến cho phần MỚI và báo cái nào SỐNG, vì sao. `c100` có rò rỉ `Path.is_dir`/`Path.exists`/`Path.iterdir` sang
   ca sau khi ném giữa chừng không? Chốt (7) có đo thật hay qua vì lý do khác?
6. Phạm vi: diff chỉ hai tệp write set; `git diff --check`; ruff `--select F` delta 0 so base;
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng tiêu chí, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> —
<hướng vá>` kèm dòng `HÌNH DẠNG:` (`loi-do` / `bo-chon-ung-vien` / `khac`). Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm
lệnh và output; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
