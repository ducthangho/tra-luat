# Review offline độc lập — packet `KIEM-MERGE-M9` r1 (Issue #1120, kho ducthangho/tra-luat)

Bạn là reviewer ĐỘC LẬP (provider openai_codex), CHỈ ĐỌC. Không sửa tệp nào trong checkout, không commit, không push,
không gọi mạng tới GitHub. Được phép chạy lệnh đọc và chạy test/đột biến trên BẢN SAO TẠM của bạn (ngoài checkout).

## Neo
- checkout: thư mục hiện hành (cwd), head ứng viên `6c965dc` (đọc `git rev-parse HEAD`, phải bắt đầu bằng `6c965dc`).
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

## Lượt trước (lượt 1, trên `268c665`, changes_requested)
F01 jobs gộp mọi tệp vào một `_trang_du` · F02 join chấp nhận bool/float · F03 dòng miễn bị `strip()` · F04–F09 sáu đột biến
sống (run_id, run/job `completed`, trang jobs, run_attempt float, diff rỗng K6). Commit `6c965dc` vá cả chín.
Việc thêm của lượt này: (a) kiểm từng bản vá bằng chính phản chứng lượt 1 và bằng đột biến; (b) tìm ĐƯỜNG VÀO KHÁC của cùng lớp
mà bản vá chưa đóng (đọc cùng tham số nhiều nơi, gán lại tên cục bộ, hai chốt tương đương không phân biệt được bằng đầu vào);
(c) kiểm bản vá có chặn oan ca hợp lệ của đặc tả không (nhiều run, nhiều tệp jobs hợp lệ, re-run attempt mới nhất).

## Lượt 2 (trên `91d4653`, changes_requested, 7 P2)
F10–F12 bool≠int · F13 SHA miễn rút gọn · F14 git lỗi kèm output · F15 `.PY` · F16 tệp bị xoá. Commit `6c965dc` thêm 6 ca + 7 đột
biến, mã runtime không đổi. Lượt này: kiểm từng bản vá bằng phản chứng lượt 2, rồi tìm đường vào khác cùng lớp như trước.
Ghi chú: đặc tả khai `tran_loi_goi_codex: ADR-0055@d2e3052` (trần 10 lời gọi); đây là lời gọi thứ 6.

## Lượt 3 (trên `18af003`, changes_requested, 1 P1 + 8 P2)
F03 tái diễn (splitlines tách ở \v \f \x1c–\x1e \x85    ) · F17–F21 (run đạt ở giữa, attempt 2, job sau job đầu) ·
F22–F24 (rename vào M9, symlink, chỉ đổi mode). Commit `6c965dc`: `_dong_chu_kho(tho=True)` chỉ tách ở LF/CRLF; 5 ca + 9 đột biến;
ma trận git thật trong `_m9_pham_vi_git`. Lượt này: kiểm bản vá bằng phản chứng lượt 3, rồi tìm đường vào khác cùng lớp.
Ràng buộc: diff đang 318/400 dòng thêm (trần nâng 300 → 400 bởi chủ kho sau lượt 5). Với finding chỉ là khoảng trống kiểm thử, nêu rõ mức P2 hay P3 theo M1
của ADR-0060 (đột biến sống trên một đường đặc tả ĐÒI là P2; ca biên ngoài hợp đồng đặc tả là P3).

## Lượt 4 (trên `856f3d3`, changes_requested, 1 P1 + 3 P2 + 1 P3)
F25 comment người khác phủ quyết run xanh · F26 run_id float ở job sau · F27 nhóm jobs đầu/cuối · F28 CRLF hợp lệ · F29 (P3) run
thiếu run_attempt. Commit `6c965dc`: K7 bắt ValueError của `_dong_chu_kho` ⇒ không miễn, vẫn xét run; 5 ca + 6 đột biến. K5/K6 cùng
hành vi có từ packet C (đã trên master), ngoài phạm vi đặc tả §2 — không đổi; nếu bạn xếp chúng thành finding của diff này, nêu
rõ vì sao chúng thuộc diff. Diff 318/400 dòng: một finding chỉ đáng thêm ca khi đột biến tương ứng phá một điều đặc tả §2.1 đòi.

## Lượt 5 (trên `d6a7404`, changes_requested, 4 lớp P2 thiếu ca)
F30 tệp M9 không đứng đầu diff · F31 job giữa lô · F32 nhóm jobs run khác đỏ vẫn đạt · F33 ranh giới prefix/đuôi. Commit `6c965dc`:
5 ca + 8 đột biến, mã runtime không đổi. Lượt này: kiểm bản vá bằng phản chứng lượt 5; với finding mới, ưu tiên lỗi HÀNH VI của mã
(P0/P1). Finding kiểm thử P2 chỉ khi đột biến phá một điều §2.1 đòi mà CHƯA có lớp ca nào phủ — ghi rõ lớp đã có ca nào gần nhất.
