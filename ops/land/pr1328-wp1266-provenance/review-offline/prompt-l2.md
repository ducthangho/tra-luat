# Review Codex offline lượt 2 — packet #1266 THU-HOI-ADMISSION-MERGE-BASE-B r13 g1 (Review Class: sensitive)

Bạn là reviewer ĐỘC LẬP (họ OpenAI). Executor là một phiên Claude khác. Lượt này CHỈ ĐỌC trên thư mục làm việc.

**Không ghi bất kỳ tệp nào trong thư mục làm việc** (kể cả tệp ignored, `__pycache__`, `.git/**`, `git config`). Lượt chạy bằng `launcher.py run --chup-workspace`; một lần ghi vào cây là cả lượt vô hiệu. Gốc workspace có thể có sẵn hai thư mục rỗng `.aws/` và `.codex/`; đừng xoá.

**Bước đầu tiên:** `git clone --no-hardlinks <thư mục làm việc> /tmp/rv1266b-copy`, rồi `git -C /tmp/rv1266b-copy checkout --detach 2acd5c7cd6ccdac99011e408217ca34081ee4fb6` và `git -C /tmp/rv1266b-copy config core.abbrev 7`. Mọi lệnh chạy trong bản sao hoặc bản sao tạm khác dưới `/tmp`. `TMPDIR` và `PYTHONDONTWRITEBYTECODE=1` đặt ngoài cả hai cây. Bản sao có đủ lịch sử; nhánh `h1` trỏ H1.

## Neo
- HEAD phải là H2 `2acd5c7cd6ccdac99011e408217ca34081ee4fb6`, tree `b76a912d76e911b697de235934f0362e49750d56`, cha DUY NHẤT là H1 `802a5665df9ae512d5b2df125b8e219f496fa9f9`; H1 có cha duy nhất là base `997b383f824ca63d7cee4a659bb6f9cf19bc439f`. Khác ⇒ `request_changes`.
- Đặc tả `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r13.md`, sha256 phải `e8ba54b72abffe80f1177d406b2bbdfa63441b4826ff6b45cbd2f798cb6a7d02`.
- Write set đúng năm tệp (như lượt 1). Trần ≤ 6 tệp, ≤ 780 dòng thêm theo `git diff --numstat 997b383..HEAD`.

## Bối cảnh
- Lượt 1 (H1 `802a566`): `approve`, 0 finding; bạn đã đo B1–B12, B16, B17 Linux.
- Sau đó lượt Windows native tập trung (đặc tả mục 6, máy `tra-luat-win`, Python 3.12, git 2.56 for Windows) cho ứng viên **203/204**: `t246_amb05_criss_cross_mot_base_lech` (B5) ra rc 0 thay vì rc 12 `VUNG_LECH`.
- Phiên điều phối đã CHẨN ĐOÁN trên Windows: lỗi ở FIXTURE. `_amb_cay_rong` gọi `subprocess.run([... "mktree"], input=<str>, text=True)`; trên Windows chế độ text đổi `\n` → `\r\n` ở stdin, nên `mktree` tạo tên có `\r` (`git ls-tree -r` ra `".github\r/coordination\r/change-impact.v1.json\r"`). Vùng tại X2 vì thế rỗng (oracle `_amb_vung_git(X2) == {}` trên Windows). Mã sản phẩm làm đúng: merge_bases đủ hai, tô màu đúng.
- H2 sửa (chỉ `ops/lease_publish_test.py`, +3 −1): `_amb_cay_rong` truyền bytes vào stdin; t246 thêm chốt fixture `list(_amb_vung_git(cay, X2)) == [".github/coordination/change-impact.v1.json"]`. Executor khai: đột biến giả lập CRLF (`dong.replace("\n","\r\n")`) làm t246 đỏ đúng ở chốt fixture; full lease suite 303/303; catalog 83/80/3/0; validator 296/296 · 344/344; numstat 773.

## Việc
1. Kiểm neo. Đọc `git diff 802a566..HEAD` và `git diff 997b383..HEAD`.
2. Xác minh phần sửa: chạy `python -u ops/lease_publish_test.py --chi-ca=t246_`; chạy lại đột biến giả lập CRLF trên bản sao tạm và xác nhận t246 đỏ ĐÚNG ở chốt fixture mới (không phải chỗ khác); khôi phục.
3. **Đóng lỗi THEO LỚP, không theo chỗ.** Rà MỌI lời gọi `subprocess` trong diff `997b383..HEAD` (cả tệp test lẫn mã sản phẩm `ops/lease_publish.py`, `.claude/dev/doc_receipt_thu_hoi*.py`) truyền `input=` tới tiến trình con: chỉ ra cái nào còn chế độ text (`text=True`, `universal_newlines`, `encoding=`) với dữ liệu nhạy dòng (tên tệp, tree, commit, JSON) có thể đổi byte trên Windows. Rà thêm chỗ đọc stdout ở chế độ text mà mã so sánh byte/OID có thể bị `\r\n` làm lệch. Mỗi chỗ còn hở là finding (nêu mức). Đồng thời nêu mọi chỗ khác trong diff có giả định chỉ đúng trên POSIX (dấu `/` vs `\`, symlink, quyền tệp, `os.sep`) mà tập bắt buộc Windows (t129, t133, t137, t151, `_amb01`…`_amb10`, toàn bộ ca `doc_receipt_thu_hoi_test.py`) có thể vấp.
4. Chạy lại full `ops/lease_publish_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` (bằng chứng dương N/N; ca đỏ do môi trường thì nêu và so với base).
5. `adr-song`, `doctrine-scan`, ruff `--select F` delta, numstat.

## Giới hạn
- Không gọi mạng. Không push, không đăng gì. Không đề xuất sửa ngoài write set. Mức dư còn 7 dòng: finding đòi thêm dòng thì ước lượng số dòng.
- Hướng thử cần tự soạn nội dung dựng đường dẫn thoát khỏi cây thì MÔ TẢ bằng lời.

## Đầu ra
Báo cáo stdout: (1) bảng kiểm phần sửa + lệnh + số đo + đột biến; (2) danh sách finding P0–P3 với tệp:dòng, mô tả, phản chứng chạy được hoặc lý do; (3) kết quả rà theo lớp ở Việc 3 (liệt kê từng lời gọi đã xét và kết luận).

Dòng CUỐI CÙNG của stdout phải đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ `approve` khi không còn P0–P2 và phần sửa đạt bằng phép đo của bạn.
