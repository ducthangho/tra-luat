# Đặc tả packet PY314-PATH-EXISTS-NUOT-OSERROR — r1

Đặc tả đóng băng. Sửa tệp này là đổi băm; muốn đổi thì soạn `py314-path-exists-nuot-oserror-r2.md`, không sửa đè.
Soạn bởi phiên executor (claude) ngày 16-10-2026 từ Issue #743; các lựa chọn Q1–Q4 dưới đây là KHUYẾN NGHỊ của phiên
soạn, và chủ kho chấp nhận chúng bằng chính comment cấp lease neo băm tệp này.

## packet_id · packet_issue

- `packet_id`: `py314-path-exists-nuot-oserror`
- `packet_issue`: [#743](https://github.com/ducthangho/tra-luat/issues/743)
- `revision`: 1

## nguon_cap_viec

Nợ P2 `py314-path-exists-nuot-oserror` (owner ducthangho), chấp nhận khi land wp685:
[PR #732 issuecomment-6099799597](https://github.com/ducthangho/tra-luat/pull/732#issuecomment-6099799597).
Finding gốc: [discussion_r4238336830](https://github.com/ducthangho/tra-luat/pull/732#discussion_r4238336830);
đo của land operator: [discussion_r4238355357](https://github.com/ducthangho/tra-luat/pull/732#discussion_r4238355357).

## loi

`.claude/dev/launcher.py`, hàm `_con_song`: phép thăm dò `trang_thai.exists()` được bọc
`try/except ProcessLookupError/OSError`. Từ Python 3.14, `pathlib.Path.exists()` là `os.path.exists(self)`, nuốt mọi
`OSError` và trả `False`, và KHÔNG đi qua `Path.stat`. Hệ quả trên 3.14:

- nhánh `except ProcessLookupError` (ESRCH ⇒ chết) và `except OSError` (chưa kết luận ⇒ đọc nội dung một lần, zombie =
  chết) không bao giờ chạy;
- EACCES/EIO khi thăm dò `/proc/<pid>/stat` rơi thẳng xuống `os.kill(pid, 0)`: zombie bị đọc là còn sống, hạn chót
  trả 125 thay vì 124;
- seam `Path.stat` của `t156`/`t157` không chạm ⇒ hai ca đỏ ("B1 result True", "seam Path.stat khong cham").

CI ghim Python 3.12 nên không thấy.

## base

`origin/master` = `9fddb1d19e8e5b753bb687673846d484fb710182` (đo 16-10-2026, sau khi fetch đủ 542/542 nhánh).
Lease neo `start_from_sha` vào SHA master đo lại lúc cấp.

## review_class

`sensitive` — cùng lớp với wp685 (bộ giết cây tiến trình và chốt 124/125 của launcher). Reviewer: Codex CLI (khác họ),
read-only. Assurance để land: `human_audited`.

## quyet_dinh (khuyến nghị, chủ kho chấp nhận bằng comment cấp lease)

- **Q1 — phép thăm dò:** `Path.stat()` (không dùng `os.stat` trần), để seam `Path.stat` sẵn có của `t156`/`t157` chặn
  đúng thao tác mới trên MỌI phiên bản Python mà không phải viết lại seam.
- **Q2 — phân loại errno:** `FileNotFoundError` (ENOENT) và `NotADirectoryError` (ENOTDIR) ⇒ không có tệp (giữ đường
  rơi về `os.kill`/`ps` như hiện nay); `ProcessLookupError` (ESRCH) ⇒ `False`; mọi `OSError` khác ⇒ chưa kết luận
  (`co_tep = None`, đọc nội dung đúng một lần). EBADF/ELOOP — mà `Path.exists` của 3.12 nuốt thành `False` — chuyển sang
  "chưa kết luận". Lý do: trên `/proc/<pid>/stat` chúng không có nghĩa "không có tệp", và nhánh chưa kết luận vẫn rơi về
  `os.kill(pid, 0)` khi đọc lỗi, nên không có đường nào kết luận "chết" mạnh hơn trước. Phạm vi bắt vẫn chỉ họ `OSError`
  (bất biến wp685 lượt 3/5).
- **Q3 — CI 3.14:** KHÔNG thêm workflow. Thay vào đó, ca hồi quy mới (M3) đỏ trên CHÍNH Python 3.12 của CI nếu
  `_con_song` gọi lại `Path.exists` cho `/proc/<pid>/stat`, tức chốt hình dạng chạy ở cổng hiện có. Lượt chạy thật trên
  3.14 là phép đo cục bộ ghi vào biên nhận. Nợ còn lại có tên: `ci-chua-co-lan-python-314` (chưa có job CI nào chạy suite
  launcher trên 3.14).
- **Q4 — ba ca đỏ sẵn trên 3.14** (`r09`, `r15`, `r351`): ngoài phạm vi; đo nền để chứng minh delta = 0, không sửa.

## write_set

1. `.claude/dev/launcher.py`
2. `.claude/dev/launcher_test.py`

Không ký tự đại diện. Workflow CI KHÔNG thuộc write set (Q3).

## muc_tieu

| # | Mục | Đường dẫn |
|---|---|---|
| M1 | `_con_song`: thay `trang_thai.exists()` bằng `trang_thai.stat()` phân loại theo Q2; giữ nguyên nhánh tệp có, nhánh chưa kết luận, `os.kill`, Darwin, Windows. Chú thích theo idiom "vX.Y.Z (bằng chứng) — fix" của tệp, nêu #743. | `launcher.py` |
| M2 | Seam `t156` nhãn `B2-thoat-parse` tiểu nhãn `hoi-*`: đổi từ `exists=sentinel` sang `stat=sentinel` (thao tác thăm dò mới), đếm `stat`; điều kiện dừng "seam không chạm" chuyển sang `n_stat`. Mọi nhãn khác giữ. | `launcher_test.py` |
| M3 | Ca hồi quy mới `r743_…`, độc lập phiên bản Python, chỉ trên Linux: (a) seam `Path.exists` trên `/proc/<pid>/stat` ném sentinel ⇒ `_con_song` không được chạm nó (`n_exists == 0`); (b) ESRCH ⇒ `False`, không đọc, không `kill`; (c) EACCES trên con zombie THẬT ⇒ `False`; (d) EACCES trên tiến trình sống ⇒ `True`, đọc 1 lần; (e) ENOENT và ENOTDIR ⇒ không đọc, `kill` 1 lần; (f) ELOOP ⇒ đọc 1 lần (Q2). | `launcher_test.py` |
| M4 | Ca ENOENT (`B2-nhanh-cu vang*`) và Darwin hiện có giữ nguyên, xanh. | `launcher_test.py` |

## nghiem_thu

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| chung | `python3.14 -B .claude/dev/launcher_test.py`: tập ca đỏ = tập ca đỏ của nền `9fddb1d` trừ `t156`, `t157`. | Ca đỏ mới, hoặc `t156`/`t157` còn đỏ. |
| chung | Python 3.12 và 3.13: tập ca đỏ BẰNG nền (delta = 0); số ca tăng đúng bằng số ca mới. | Bất kỳ ca đỏ mới nào. |
| chung | `python -m ruff check --select F` trên hai tệp: delta so nền = 0. `git diff --check` sạch. | Số F tăng; diff có lỗi khoảng trắng. |
| M1 | Đột biến về lại `exists()` ⇒ `r743` ĐỎ trên 3.12 VÀ `t156` ĐỎ trên 3.14. | Một trong hai còn xanh. |
| M1/Q2 | Mỗi chốt có đột biến riêng làm đúng ca đích đỏ, chạy trên BẢN SAO TẠM (không trên tệp thật): bỏ nhánh ESRCH; gộp ENOENT vào "chưa kết luận"; bỏ ENOTDIR khỏi "không có tệp"; gộp OSError khác vào "không có tệp". | Đột biến nào sống, hoặc chết vì lỗi vô can (tín dụng giả). |
| M3 | `r743` xanh trên 3.12, 3.13, 3.14. | Đỏ ở bất kỳ phiên bản nào. |
| review | Codex CLI read-only trên exact SHA: P1 = 0, P2 = 0. | Bất kỳ P1/P2 mở. |

Điều kiện land: hết P1/P2 trên đúng head; CI xanh gồm `launcher (Windows that)`; chủ kho uỷ quyền bằng comment bền neo
đúng head. Executor KHÔNG merge, KHÔNG land, KHÔNG deploy.

## ngoai_pham_vi

- `r09`, `r15`, `r351` đỏ sẵn trên 3.14 (Q4).
- Workflow CI chạy 3.14 (Q3, nợ `ci-chua-co-lan-python-314`).
- Mọi đường gọi `Path.exists()` khác trong launcher không thăm dò `/proc/<pid>/stat`.

## Trần kích thước

ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm. Packet này: 2 tệp. Vượt thì DỪNG, xin ngoại lệ chủ kho.

## chua_do_duoc

- Hành vi trên Darwin không đo được trong container Linux; chỉ đổi đường `/proc`, nhánh Darwin giữ nguyên xi.
- Python 3.15 trở lên: không đo.
