# Review offline độc lập — packet `KIEM-MERGE-M9` r1 (Issue #1120, kho ducthangho/tra-luat)

Bạn là reviewer ĐỘC LẬP (provider openai_codex), CHỈ ĐỌC. Không sửa tệp nào trong checkout, không commit, không push,
không gọi mạng tới GitHub. Được phép chạy lệnh đọc và chạy test/đột biến trên BẢN SAO TẠM của bạn (ngoài checkout).

## Neo
- checkout: thư mục hiện hành (cwd), head ứng viên `268c665` (đọc `git rev-parse HEAD`, phải bắt đầu bằng `268c665`).
- base: `f4b513da5802d439aedbe58ae4a5cd38ff47d6ab`. Diff cần review: `git diff f4b513d..HEAD` (5 tệp).
- Đặc tả đóng băng: `ops/specs/KIEM-MERGE-M9-r1.md` (sha256 phải là `d18820c854af40a4e0d6ca58f6b8812296a3057b0e7b063f704f5a4cdd7ca442`).
- Luật: `docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (M1–M3 severity/lớp, M9 phạm vi audit), `CLAUDE.md` mục "Bài học đắt giá".

## Việc
1. Đọc đặc tả §2 (K7), §4 (A1–A7) và diff. Kiểm `cmd_kiem_merge` k7, `_diff_raw`, `_cham_m9` trong `.claude/dev/packet_loop.py`.
2. Tìm lỗi THEO LỚP (ADR-0060 M2): với mỗi lỗi, liệt kê MỌI đường vào cùng lớp, không chỉ ca đầu tiên. Gợi ý hướng
   (không phải giới hạn): phạm vi M9 (tên tệp lạ, chữ hoa, rename/xoá/mode, symlink, đường dẫn có ký tự đặc biệt),
   chọn run/job (nhiều run, re-run attempt, run_attempt kiểu khác int/bool, job thiếu trường, jobs của run khác trong cùng
   tệp, nhiều tệp jobs), trang readback (`_trang_du`), dòng miễn của chủ kho (khoảng trắng, SHA ngắn, comment không phải
   của chủ kho mà run vẫn xanh), M6 (mọi thiếu đều được liệt kê), hồi quy cho K6 do tách `_diff_raw`
   (trước đây `rc != 0` và diff rỗng đều raise; xem bây giờ còn đúng không), và đột biến đích có giết ĐÚNG lý do không.
3. Đo, đừng đoán: chạy test chọn lọc trên một bản sao tạm. Bộ chạy nhanh (chỉ ca chọn):
   ```
   python3 - <<'EOF'
   import sys, tempfile, importlib.util; from pathlib import Path
   root = Path('.').resolve(); sys.path.insert(0, str(root/'.claude/dev'))
   sp = importlib.util.spec_from_file_location('plt', root/'.claude/dev/packet_loop_test.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
   ten = {t for t,_ in m.CASES if t.startswith(('cong_m9_','cong_c_'))}
   with tempfile.TemporaryDirectory() as td: ket = m.chay_suite(m.CANONICAL, Path(td), ten)
   print(sum(v is None for v in ket.values()), '/', len(ket)); [print(t, v) for t, v in ket.items() if v]
   EOF
   ```
   Đột biến: chép `.claude/dev/` ra thư mục tạm, áp chuỗi thay của `MUTANTS["m9_*"]`, gọi `m.chay_suite(<bản sao>/packet_loop.py, ...)`
   với các ca đích; đột biến phải làm ca đích đỏ bằng AssertionError của chính ca (không phải traceback/lỗi vô can).
   Tự viết thêm đột biến bạn nghĩ cần mà bộ ca không bắt — mỗi đột biến SỐNG là một finding.
   Nếu một hướng thử đòi bạn tự soạn nội dung nhạy cảm (đường dẫn thoát khỏi cây thư mục v.v.), hãy MÔ TẢ BẰNG LỜI thay vì soạn.
4. Severity: P0 (sai an ninh/mất dữ liệu), P1 (cổng cho qua thứ phải chặn, hoặc chặn oan ca hợp lệ của đặc tả), P2 (lỗ phụ,
   thiếu ca/đột biến cho một đường đặc tả đòi), P3 (nit). Mỗi finding: id, severity, tệp:dòng, phản chứng chạy được
   (lệnh + output đo được), đề xuất sửa.

## Đầu ra
Viết báo cáo ra stdout. Dòng CUỐI CÙNG phải đúng một trong hai:
`KET_LUAN: approve` (không còn P0–P2; P3 liệt kê riêng) hoặc `KET_LUAN: changes_requested`.
