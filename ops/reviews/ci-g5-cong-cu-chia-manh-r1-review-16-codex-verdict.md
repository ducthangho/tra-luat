# Cross-review độc lập — packet #668, lượt 16

verdict: changes_requested
reviewed_sha: 54b4a01412e1d0240a1474258096ad64a4cbf0b9

Đo trên bản sao trong `/tmp`; không sửa cây sản phẩm `cay-kho/`.

**Kết luận cuối: 0 P1 · 1 P2 (F38) · 0 P3.** F36 đã vá thật; lỗi đăng ký F37 đã sửa nhưng giàn giáo mới sinh F38 ở nhánh thuộc tính symlink vắng. Các khối checkpoint bên dưới là nhật ký ghi dần; số cuối nằm ở HƯỚNG 13–14 và các bảng kết luận.

Reviewer: Codex/OpenAI, phiên độc lập, công cụ shell cục bộ, transport machine (`codex_cli`). Không xác minh độc lập được biến thể model/effort từ artifact; không suy danh tính model từ tài khoản GitHub. Baseline `f8a7829cc44f296c25faf1a6439b603ba840f70b`; tree ứng viên `6624b594e7aa9825b089512e0214b18f2b86cbac`. [Preflight](evidence-luot-16/preflight.json) ghi băm nguồn và trạng thái sạch.

HƯỚNG 1: Neo đầu vào và phạm vi
  giả thuyết : bundle hoặc phạm vi khác khai báo.
  lệnh       : git -C cay-kho rev-parse HEAD; git status --porcelain; sha256sum SPEC.md; inventory.py.
  output     : HEAD đúng 54b4a01412e1d0240a1474258096ad64a4cbf0b9; cây sạch; SPEC dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15. Baseline 212 mutant/53 CA; head 398 mutant/56 CA; không mất tên cũ, thêm 186.
  kết luận   : KHÔNG PHẢI LỖI. Trần ~1.900 theo chỉ thị mới; không dùng trần 600 cũ để chặn review.

HƯỚNG 2: Workflow — phản chứng có sẵn và tháo chốt
  giả thuyết : các lớp F1/F3/F10/F14 đã đóng bị mở lại.
  lệnh       : python evidence-luot-16/env.py python evidence-luot-16/workflow.py; workflow_ablation_extra.py.
  output     : control: F1=20, F3=28, F10=7, F14=5; không ca nào lọt. Gỡ F10: 7 ca lọt; chỉ splitlines: 0 (chốt khác vẫn bảo vệ); splitlines + gỡ F10: 27 F3 và 7 F10 lọt. Gỡ thực thi: 13 F1, 7 F10 lọt; gỡ shell: 5 F14 lọt; gỡ cả hai: 18 F1, 7 F10, 5 F14 lọt.
  kết luận   : KHÔNG PHẢI LỖI. Các phép chỉ thay validator trên bản sao/namespace riêng, dùng nguyên fixture trong cây, không tự soạn payload ẩn.

HƯỚNG 3: Toàn miền cấu hình và nguồn HEAD
  giả thuyết : bỏ sót nhánh/so sánh/thành phần grammar dẫn đến biên kế tiếp.
  lệnh       : domain.py; domain_check.py; probe.py (evidence-luot-16, qua env.py).
  output     : MODE_SPEC 458 PASS; HEAD_SPEC 275 PASS. Lưới 27 ô vắng/rỗng/có của ba biến có đúng 3 ô hợp lệ. Chi tiết domain-check.json, domain-results.json, grids.json.
  kết luận   : KHÔNG PHẢI LỖI ở giá trị của control; phép đo răng 103 đột biến miền đang chạy, chưa suy pass từ việc control đúng.

Miền `_doc_che_do`: ba biến B/M/R, phân biệt None/rỗng/có; thứ tự lỗi R lẻ, B sai, B+M đồng thời; B phải đúng `manh` (hoa/thường, khoảng trắng, hậu tố); regex fullmatch gồm nhánh k=0 hoặc chữ đầu 1..9, chữ thứ hai ASCII 0..9 tùy chọn, dấu `/` đúng một, N đầu 1..9/chữ thứ hai tùy chọn; không dấu số, số 0 dẫn, chữ số Unicode, dư tiền/hậu tố; hai group chuyển đúng sang k/N; N=2..16, k<N; R phải có và không rỗng nhưng giữ nguyên mọi space/path; ba kết quả du/gate/manh và tuple đúng. Miền giá trị gồm mọi k hợp lệ cho mọi N=2..16, các biên 0/1/17/99/100 và k=N/k>N.

Miền `_van_tay`: git/`-C`/GOC/rev-parse/HEAD, capture_output=True/text=True/timeout=60; rc=0 mới dùng stdout, rc dương/âm bị loại; OSError/SubprocessError/TimeoutExpired; strip hai đầu; fullmatch hai nhánh độc lập [0-9a-f]{40} và {64}, chữ ASCII/thường, đầu/giữa/cuối, thiếu/thừa ký tự và không ghép hai HEAD. SHA-256 đọc đúng TEP_TEST bằng bytes, hexdigest thường; rỗng, CR/LF, Unicode, hoa/thường, space, biên 63/64/65/4095/4096/4097/8193, chung tiền tố/hậu tố và tệp nguồn thật; thay bytes giữ HEAD và thay HEAD giữ bytes. Lỗi đọc nguồn phải thoát lỗi, không tạo digest giả.

HƯỚNG 4: Đối chiếu F36/F37 bằng thực thi
  giả thuyết : bản vá chỉ sửa đúng ví dụ mà chưa đóng lớp bytes/năng lực.
  lệnh       : measure.py all-domain-mutations.json target; extent.py; check.py probes.json.
  output     : 103 phép miền đã chạy ca đích; cả 7 phép F36 (prefix/suffix 64/4096, ascii_ignore, casefold, bỏ space) đều `giet_that`. Round-trip UTF-8 vẫn qua, digest không đổi trên miền tệp Python hợp lệ. Mô phỏng `_CO_SYMLINK=False` trên cây riêng: 394 mutant, không đăng ký f24/f35/f37_bo_f24/f37_bo_f35; t52/t53/t54 `qua`.
  kết luận   : KHÔNG PHẢI LỖI ở F36 và control hai nhánh F37; bán kính đầy đủ của mutant chuẩn đang đo riêng. Các lỗi giàn giáo và phép tương đương không bị gộp thành `giet_that`.

HƯỚNG 5 (MỚI): Artifact cùng vân tay nhưng khác registry theo năng lực
  giả thuyết : cùng HEAD/SHA nhưng số mutant khác giữa nền có/không symlink có thể gom xanh nhầm.
  lệnh       : check.py probes.json, case cross_capability; dựng 8 mảnh từ mỗi registry, giữ cùng vân tay, đổi bên nhận theo hai chiều.
  output     : enabled_to_disabled: same=0, different=1, G-ban-ghi tên ngoài nhóm f24_nhan_symlink; disabled_to_enabled: same=0, different=1, G-ban-ghi thiếu f24_nhan_symlink.
  kết luận   : KHÔNG PHẢI LỖI. Bên gom tái tính tên theo registry của chính nó, không chỉ tin số mảnh và vân tay.

HƯỚNG 6 (MỚI): Tái nhập và khôi phục trạng thái sau phép dò F37
  giả thuyết : chốt mới sửa os.symlink toàn cục hoặc làm registry đổi giữa hai lần gọi, gây nhiễu bán kính/đổi phân hoạch.
  lệnh       : check.py probes.json, case reimport_restore; gọi cửa gom ba lần trong cùng tiến trình, so identity os.symlink và toàn danh sách có thứ tự DOT_BIEN trước/sau.
  output     : 3/3 lần trả [[True,[f24_nhan_symlink,f35_writer_broken_link]],[False,[]]], registry=398, restored=True.
  kết luận   : KHÔNG PHẢI LỖI trên đường thành công và đường OSError mô phỏng của F37.

HƯỚNG 7 (MỚI): HEAD bị môi trường Git kế thừa đổi nguồn
  giả thuyết : GIT_DIR ngoại lai thắng `git -C GOC` và cổng vẫn xanh.
  lệnh       : check.py probes.json + environment-probes.json; tạo kho ngoại lai trong /tmp, đặt GIT_DIR rồi đo _van_tay và t52/t53/t54, khôi phục môi trường trong finally.
  output     : _van_tay trả HEAD kho ngoại lai; t52 qua, t53 giet_that tại ô không-git (vector [False,True,True,True,True]), t54 qua. Khôi phục môi trường trả lại HEAD ứng viên.
  kết luận   : KHÔNG PHẢI LỖI theo giả thuyết CI xanh: ca t53 có sẵn chặn môi trường ấy trước khi mảnh ghi artifact. Không nâng hành vi của helper gọi rời thành lỗ vượt gate.

HƯỚNG 8: Hồi quy gate và các cổng liên quan
  giả thuyết : bản vá tự kiểm làm hỏng cổng trọn vẹn hoặc cổng ngoài packet.
  lệnh       : run_regression.py (env.py), trên head và baseline; gate chạy CONG_CU_TEST_BAN_KINH=manh.
  output     : gate 56/56, bỏ qua=0, tiền kiểm bỏ qua=0, tự kiểm đạt, cổng cây thật ĐẠT, lỗi đột biến=0. Head/base: registry ĐẠT; launcher t152 PASS; lease t24/t31/t35/t161/t162 PASS; actionlint rc=0; cong_cu kiem-tra rc=0. Ruff F 6→6, cùng loại/message/path, delta=0.
  kết luận   : KHÔNG PHẢI LỖI. Gate giao mảnh không thay thế bán kính; số mẫu radius sẽ được ghi riêng.

HƯỚNG 9: Phân hoạch, gom, CLI, bộ ghi — miền hành vi
  giả thuyết : bảng cấu trúc đúng nhưng kết quả sai được gom xanh, hoặc bộ ghi giữ artifact cũ sau lỗi.
  lệnh       : partition_roundtrip.py; schema_io.py; source_io.py; cli_mode_collision.py; survivor_equivalence.py; các bảng gom/CLI/writer kế thừa qua run_checklists.py.
  output     : N=2..16 đều coverage=398, disjoint=True, gom_errors=0, table_order=True dù đảo tên tệp/trộn thứ tự bản ghi. Writer symlink: lỗi=1, output_exists=False, target='KEEP'; thư mục làm đường ra: IsADirectoryError; ghi lỗi: OSError, stale_exists=False. Nguồn mất/là thư mục/đọc lỗi lần lượt FileNotFoundError/IsADirectoryError/OSError. Tên thư mục trùng cửa tự kiểm vẫn đi --gop và đỏ G-rong, đối số thừa đỏ rc=2 G-doi-so.
  kết luận   : KHÔNG PHẢI LỖI ở control; ma trận đột biến đầy đủ còn chạy.

Miền artifact: thư mục vắng/rỗng; mọi mục phải tệp thường, symlink lành/gãy/thư mục/FIFO bị loại, hardlink không vượt đếm; read/decode/prefix/JSON/khoá chính xác/kiểu int thật (không bool/float/string/null/list/dict); version, k, N, SHA, HEAD; N đồng nhất/2..16, tập k chính xác, mỗi k một tệp; phân hoạch i%N=k đủ/rời nhau/đúng danh tính; mọi dòng BKCON, tên/tập ca/đích/trạng thái/lý do hợp lệ; đúng cấu trúc nhưng đích sống/tín dụng giả/bán kính>1 vẫn đỏ; cộng đủ lỗi 0/1/>1 và in đủ bảng đúng thứ tự DOT_BIEN. CLI: argv[1], thiếu/thừa/lạ/cờ thành tên thư mục, fingerprint một lần, đúng rc và stdout. Writer: xoá output cũ, con lỗi/HEAD None/thiếu record/kết luận sai không để tệp; lỗi đầu/cuối/nhiều record, header/body/nguyên path, tạo cha và cha có sẵn; lỗi IO fail-closed; năng lực true/false quyết định cả registry lẫn fixture. Chốt G-tong được phân biệt là dự phòng suy ra từ các chốt trước.

HƯỚNG 10: Răng F37 ở nhánh không có năng lực
  giả thuyết : mutant điều kiện mới cũng sống ở nền không symlink.
  lệnh       : capability_radius.py f37_dk_luon_dung; capability_radius.py f37_dk_dao, trên /tmp/review668-r16-no-links.
  output     : mỗi mutant lỗi=0, đúng t52 giet_that, bán kính 1/56. Hai mutant bỏ từng đăng ký không hiện trong registry false; control 394 mutant và t52/t53/t54 qua.
  kết luận   : KHÔNG PHẢI LỖI. Đây là mô phỏng năng lực trên Linux, không khai đã chạy Windows thật.

Miền `main`/dispatcher đang đo bằng ma trận kế thừa: `_doc_che_do(os.environ)` trước mọi tác vụ, lỗi ValueError/rc=2/chẩn đoán; hai tiền kiểm đúng thứ tự/danh tính/lý do; toàn CA một lần đúng thứ tự, phân biệt pass/BoQua/AssertionError/exception, mọi tên/lý do/bộ đếm/stdout. Mảnh: k/N/path nguyên vẹn, phân hoạch, nền đỏ hoặc tiền kiểm bỏ qua phải dọn đúng output và rc=1; `_phong_con` tên/nền rỗng/workers, mọi nhóm, `_nhan_ket_qua_con` đủ bốn đối số, tích luỹ mọi giá trị và lý do lỗi đầu tiên/rc/đuôi 300 ký tự; bảy đối số bộ ghi, toàn bảng, rc theo lỗi 0/1/>1. Gate/đủ: cổng thật đúng GOC, tự kiểm phân hạng/giàn giáo/song song, nền đỏ sắp xếp, cộng nhiều nguồn không gán đè, gate giao mảnh, đủ đo toàn DOT_BIEN với nền/workers đúng, mọi dòng và SỐ LIỆU. Dispatcher: không đối số trên du/gate/mảnh và cấu hình sai, sys.exit giữ mã; --gop ở argv[1], kiểm arity, đối số/cửa sai không chiếm dispatch. Trường hợp không thể tới trong hợp đồng (nhóm rỗng sau worker clamp, hong ở nhánh đã chặn nền đỏ) không được gọi là survivor có nghĩa.

HƯỚNG 11: Ma trận đủ 56 ca — checkpoint, chưa phải kết luận cuối
  giả thuyết : phép đổi qua ca đích nhưng sống cả suite, hoặc bản vá mới giết oan ca khác.
  lệnh       : run_checklists.py; fields_full.py; novel_entry.py; partition_identity.py; measure.py trên hai tập rời domain-survivor/remaining-domain; summarize.py.
  output     : checkpoint 115/263 phép hoàn tất, mỗi phép có đủ 56 states; 17/17 phép trường main chỉ t54 giet_that; 3/3 entry chỉ t54; 2/2 phân hoạch chỉ t52. Mẫu native checkpoint 48/176, gồm đủ 41 mutant cũ: mọi mutant chuẩn hoàn tất bán kính 1/56, 0 ca mới bị giết thêm bởi mutant cũ.
  kết luận   : CHƯA CHỐT — chờ các phép còn lại; không dùng checkpoint này để khai đã đo đủ 263 hoặc 398.

HƯỚNG 12 (MỚI): Năng lực false do thuộc tính symlink vắng hẳn
  giả thuyết : phép nạp lại mới chỉ chịu được callable ném lỗi, không chịu được thuộc tính vắng — dù `_do_co_symlink` chủ động bắt cả AttributeError và trả false.
  lệnh       : `check.py absent-probes.json`; lấy nguồn lượt 15 bằng git show b3863e2, nguồn head hiện tại, thêm bootstrap xoá thuộc tính os.symlink trong hai bản sao /tmp để cả tiến trình cha/con thấy cùng môi trường; chạy t52.
  output     : prior: capability=false, count=386, t52=[qua,null]. Head: capability=false, count=394, t52=tin_dung_gia, cửa --tu-kiem-gom rc=1; AttributeError tại `cu_sl, sp = os.symlink, ...` (dòng gốc 7832, bản mô phỏng thêm hai dòng nên traceback 7834).
  kết luận   : LỖI (P2), F38 — lớp artifact theo năng lực CHƯA ĐÓNG ở miền vắng thuộc tính mà chính `_do_co_symlink` có nhánh hỗ trợ. Đây là hồi quy hẹp của giàn giáo mới, không phải đường CI xanh và không khẳng định Windows/Ubuntu chuẩn đang thiếu os.symlink. OSError/NotImplementedError/AttributeError được ném từ một callable đã qua; VẮNG callable là ô khác.

HINT PATCH F38 — đóng toàn miền năng lực và khôi phục trạng thái

Chỉ là gợi ý cho executor; không sửa `cay-kho/`. Tệp/hàm: `ops/cong_cu_test.py::_in_tu_kiem_gom`, đoạn F37 dòng 7832–7844. Giữ nguyên thuật toán gom/ghi. Lưu cả trạng thái **có/vắng thuộc tính** bằng sentinel, thay vì đọc thuộc tính trực tiếp, và khôi phục đúng trạng thái trong finally:

```diff
-    cu_sl, sp = os.symlink, importlib.util.spec_from_file_location("cct_f37", TEP_TEST)
+    sl_vang = object()
+    cu_sl = getattr(os, "symlink", sl_vang)
+    sp = importlib.util.spec_from_file_location("cct_f37", TEP_TEST)
     ...
     finally:
-        os.symlink = cu_sl
+        if cu_sl is sl_vang:
+            os.__dict__.pop("symlink", None)
+        else:
+            os.symlink = cu_sl
```

Đủ ô cần thêm trong giàn giáo/t52: (1) callable tạo link được; (2–4) callable ném từng OSError/NotImplementedError/AttributeError; (5) thuộc tính vắng hẳn. Đo cả probe trả true/false và registry thật khi nạp lại: true có f24/f35 cùng hai mutant bỏ đăng ký, false không có cả bốn. Đo identity hàm được khôi phục khi vốn có; khi vốn vắng thì sau phép đo vẫn vắng. Đo khôi phục ở cả import thành công và import ném lỗi; lỗi import phải thành dữ liệu `NEM:...` làm t52 đỏ, không được giả thành phép đo false thành công. Vẫn giữ hai fixture symlink thật của bên gom/bên ghi khi có năng lực.

Nên tách đoạn nạp lại/khôi phục thành helper nhỏ của giàn giáo, để gọi được chính helper ấy trong từng trạng thái có/vắng mà không đệ quy chạy toàn `_in_tu_kiem_gom`. Chỉ thử import module dưới trạng thái vắng mà không đi qua helper lưu/khôi phục thì **không bắt được F38**.

Đột biến cần giết, đều đích **t52**, các ca khác qua: `getattr(os,"symlink",sl_vang)` → `os.symlink`; bỏ nhánh vắng trong finally và luôn gán trở lại; bỏ toàn khôi phục; chỉ khôi phục sau import thành công; bỏ `AttributeError` khỏi tuple của `_do_co_symlink` (đo bằng import dưới trạng thái vắng, trả ngoại lệ thành dữ liệu để tránh tín dụng giả). Giữ các mutant F37 hiện có: điều kiện luôn đúng/đảo điều kiện, bỏ từng đăng ký khi capability=true. Hai mutant bỏ đăng ký vẫn chỉ được đăng ký khi có năng lực.

Rủi ro bán kính: không xoá/đổi os.symlink trên tiến trình cha chạy cả CA; phép tráo phải nằm trong cửa con t52 và khôi phục bằng finally, kể cả khi nạp lỗi. Không thêm oracle này vào t53/t54. Đo lại các mutant F24/F35/F37, mutant mới và mẫu mutant cũ tráo TEP_TEST/GOC; không biến lỗi import thành `qua`. Bản sửa sentinel ở trên đang được đối chứng riêng trên bản sao; đó không thay cho test và đăng ký mutant mà executor phải bổ sung.

Đối chứng hint đã hoàn tất (`check.py hint-probes.json`): bản sao sửa sentinel, thuộc tính có: t52/t53/t54 đều qua; thuộc tính vắng: cả ba đều qua. Trên head chưa sửa, mô phỏng import ném RuntimeError: metadata báo `NEM:RuntimeError`, identity os.symlink được khôi phục. Vì vậy lỗi đo được nằm ở ô vắng thuộc tính trước phép lưu, không quy sai toàn bộ finally hiện có. Chưa đo bán kính của bản hint, chưa áp vào cây sản phẩm.

HƯỚNG 13: Chốt ma trận kế thừa trên exact head
  giả thuyết : một kết quả lượt trước bị tái dùng hoặc ca đích xanh che survivor ở toàn suite.
  lệnh       : `summarize.py`, đối chiếu mỗi JSON có đúng tập 56 CA của head; danh mục và từng kết quả ở [mutation-matrix.md](evidence-luot-16/mutation-matrix.md), [review-summary.json](evidence-luot-16/review-summary.json).
  output     : MATRIX 263; MISSING 0; 234 phép chỉ ca đích giet_that; 17 phép ngoài mẫu 1/56; 12 survivor. Đủ 138 phép checklist lượt 5–10, 17 trường main + 3 entry + 2 phân hoạch lượt 11, 7 lượt 12, 4 lượt 13, 83 lượt 14 và 9 phép bytes lượt 15. Không dùng kết quả đo cũ để điền ô nào.
  kết luận   : KHÔNG PHẢI LỖI mới trong ma trận này. F36 đã vá thật: bảy phép bytes đều chỉ t53 giet_that, 55 ca khác qua. F38 là hồi quy ở miền năng lực riêng, không phải survivor của ma trận trên nền có symlink.

12 survivor đã phân loại, không giấu khỏi bảng: `receiver_baseline` chỉ thêm tên ngoài tập CA; `break_on_error` không bỏ đo vì `_phong_con` đã chạy/đợi hết con, mảnh vẫn đỏ và không có file; `final_hong` vẫn bị lỗi nền kéo đỏ; `final_gate_eq_one` đúng miền 0/1 của `_cong_tren_cay_that`; `main_no_sorted_baseline` được helper sắp xếp; `writer_drop_missing` vẫn KeyError/không file và receiver đảm bảo đủ tập trước writer; `main_receiver_baseline_hong` luôn nhận hong rỗng sau chốt nền; `main_empty_launch_guard`/`main_receive_false` không đổi hành vi trong miền nhóm không rỗng và worker kẹp theo số tên; `gom_drop_decodeerror` vẫn bắt UnicodeDecodeError qua ValueError; `writer_record_order` được giao thức cho phép, bảng gom vẫn theo DOT_BIEN; `source_utf8_roundtrip` giữ nguyên bytes nguồn UTF-8 hợp lệ. Đối chứng trực tiếp writer thiếu record: control lỗi=1/không file, mutant KeyError/không file; baseline_report_sort_equal=True.

17 phép ngoài mẫu 1/56 được giữ nguyên trạng thái: 10 phép thay miền cấu hình đúng (`mode_zero_removed`, `mode_k_requires_two`, `mode_n_requires_two`, `mode_n_min`, `mode_n_max_low`, `mode_k_strict`, `mode_output_constant`, `mode_k_group`, `mode_n_group`, `mode_zero_to_one`) làm đỏ t53 và t54; `head_64_only`/`head_no_strip` làm t53 giet_that và t52 tin_dung_gia; `source_wrong_root` làm t52/t53 giet_that; `source_no_capture`/`source_no_text`/`source_digest_form` làm t52/t53 tin_dung_gia; `writer_existing_parent` làm t52 tin_dung_gia. Đây là phép thăm dò reviewer, không phải mutant chuẩn được khai bán kính 1; không đếm lỗi giàn giáo thành tín dụng giết thật.

HƯỚNG 14: Bán kính chuẩn, đối chiếu bỏ qua trên baseline và khóa evidence
  giả thuyết : test mới giết oan mutant cũ hoặc làm mutant chuẩn sai bán kính.
  lệnh       : `sample_run.py`; `native_summary.py`; `check.py baseline-probes.json`; kiểm lại exact HEAD, trạng thái cây và bytes năm tệp.
  output     : 176/176 mutant mẫu hoàn tất, 176 kết luận `ok` bán kính 1/56 theo bộ chấm hiện hữu, errors=[]; 135 mutant mới gồm toàn bộ 60 đích t52 + 50 đích t53 và 25 đích t54, cộng 41 mutant cũ. Raw: 9.669 qua, 176 giet_that, 11 bo_qua, 0 tin_dung_gia. Không mutant cũ nào giết thêm hoặc làm bỏ qua t52/t53/t54. Không cần retry/chọn lại kết quả để đạt các số này.
  kết luận   : KHÔNG PHẢI LỖI hồi quy trong mẫu. Đây là mẫu có chủ đích **176/398**, không phải đã đo đủ 398. Tất cả 135 mutant mới trong mẫu có đúng 1 giet_that + 55 qua; 11 bo_qua nằm riêng ở hai mutant GOC cũ, không được tính thành pass.

Hai mutant có bỏ qua: `t6_day_g5_sau_py_compile` bỏ qua t16–t21 (6 ca); `t21_git_regex_cat_hau_to` bỏ qua t16–t20 (5 ca), vì bản sao tối thiểu thiếu bản kê hoặc `.claude/dev`. Đã chạy lại đủ **53 ca baseline cho cả hai**: tập bỏ qua và trạng thái từng ca cũ bằng head, không có delta. Xem [baseline-radius-two.json](evidence-luot-16/baseline-radius-two.json). Gate trên cây đầy đủ vẫn 56/56, bỏ qua=0.

Mẫu cũ gồm toàn bộ 28 mutant tráo TEP_TEST, cả hai tráo GOC, 10 tráo SCRIPT và một tráo CAI_SH; không khai đã lấy mẫu 161 mutant BASH_NEN cũ. Danh sách chuẩn được cố định trước khi chạy ở [sample-names.json](evidence-luot-16/sample/sample-names.json), kết quả tổng hợp ở [native-summary.json](evidence-luot-16/native-summary.json). Riêng nhánh capability=false còn có hai phép F37 điều kiện, mỗi phép đủ 56 ca và đúng 1/56, đã ghi ở HƯỚNG 10.

Kiểm cuối: HEAD không đổi; `git status --porcelain` của `cay-kho/` rỗng; năm tệp của bản sao đo bằng nguyên bytes ứng viên. Diff baseline→head đúng **5 tệp, +1905/−49**, chạm trần ~1.900 theo chỉ thị. Không dùng kết quả bán kính đang chạy của executor.

**Bảng kết luận theo lớp** — trạng thái trong miền và phiên bản đã đo, không phải chứng minh cho mọi chương trình có thể được viết trong tương lai.

| Lớp | Miền đã đo | Trạng thái |
|---|---|---|
| Workflow/thực thi hai job | 87 ca p668, trong đó 60 F1/F3/F10/F14; shell, job/step/workflow env/defaults/keys, setup/checkout/Python, matrix os/k/N, needs/if/fail-fast, upload/download cùng OS, run và bộ tách dòng; tháo chốt theo lớp; registry và actionlint | **Đóng** |
| main/dispatcher | Toàn danh mục HƯỚNG 10–13: du/gate/mảnh, từng tham số/caller/ngoại lệ/bộ đếm/dòng stdout, nhóm/con/receiver/writer, worker, lỗi 0/1/>1 và nhiều nguồn, CLI không đối số/argv/exit; ma trận kế thừa đầy đủ | **Đóng**; survivor tương đương/fail-closed đã giải thích riêng |
| Đọc chế độ | 27 ô hiện diện; 458 ô oracle; 10.816 cặp số; mọi nhánh/thứ tự lỗi/group/ASCII/quantifier/separator/fullmatch/N/k/path; đột biến r12–r14 qua đủ 56 ca | **Đóng** |
| Nguồn vân tay | Git argv/kwargs, rc/ngoại lệ, strip và toàn grammar HEAD 40/64, 275 ô ngoài + lưới trong cây; nguồn bytes và HEAD thay độc lập; 17 fixture bytes và digest toàn TEP_TEST thật, biên/lớn/CRLF/Unicode/case/space; 7 phép F36 bán kính 1/56 | **Đóng**; F36 đã vá thật |
| Phân hoạch/gom/CLI/bộ ghi/registry theo năng lực | Toàn miền HƯỚNG 9; N=2..16, kiểu/cấu trúc/kết quả/thứ tự/đếm/path/IO; true/false và đăng ký; callable ném ba loại lỗi, thuộc tính vắng, tái nhập và finally, artifact đổi miền năng lực | **Chưa đóng — F38**. Gom/ghi/CLI và lỗi đăng ký cũ đã được bảo vệ; giàn giáo mới hỏng ở ô thuộc tính symlink vắng |
| Hồi quy/cổng phụ | Gate 56/56, registry head 1025/1025 và baseline 938/938, t152, lease t24/t31/t35/t161/t162, actionlint hai vế, ruff F 6→6; bán kính native ghi riêng ở khối cuối | Các cổng đã hoàn tất **đạt**; không suy kết quả 398 từ gate giao mảnh |

**Bảng finding**

| F<n> | Lớp | Mức | Tệp:dòng | Mô tả | Phản chứng |
|---|---|---|---|---|---|
| F38 | Artifact theo năng lực / giàn giáo t52 | P2 | `ops/cong_cu_test.py:7832` (miền được hỗ trợ tại `:7385`) | `_do_co_symlink` cho phép thuộc tính vắng và trả false; đoạn tự kiểm F37 mới đọc trực tiếp thuộc tính trước try/finally, làm cửa gom chết bằng AttributeError. Lỗi gốc F37 đã sửa nhưng lớp sinh hồi quy ở nhánh false khác. | [check-capability_absent.json](evidence-luot-16/check-capability_absent.json): lượt 15 t52 qua, head tin_dung_gia. [check-capability_hint.json](evidence-luot-16/check-capability_hint.json): sửa sentinel trên bản sao làm t52/t53/t54 qua ở cả có/vắng thuộc tính. |

**HINT PATCH cho lớp chưa đóng:** F38 ở ngay sau HƯỚNG 12 nêu diff lưu bằng sentinel/getattr và finally khôi phục cả có/vắng; cần thêm đủ năm trạng thái năng lực, kiểm registry và khôi phục khi import thành công/lỗi, cùng các mutant đích t52. Không sửa thuật toán gom/ghi; không coi bản hint đã đo ba ca là đã đạt bán kính đầy đủ.

**ĐỐI CHIẾU LƯỢT TRƯỚC:** F36 = **ĐÃ VÁ THẬT**, cả bảy biểu hiện cũ bị đúng t53 giết. F37 = **VÁ SINH LỖI MỚI**: đăng ký theo false capability đã sửa thật (394 mutant, bỏ cả bốn đăng ký có điều kiện), hai mutant điều kiện đạt 1/56 ngay trên nhánh false; nhưng giàn giáo đọc thuộc tính vắng sinh F38. Không quy hai kết luận này từ lời khai executor.

**Trạng thái F1–F37 (không có F4)**

| Finding | Trạng thái lỗi gốc và bằng chứng lượt này |
|---|---|
| F1 | Đóng — 20 ca workflow bị chặn, tháo chốt thực thi làm lọt |
| F2 | Đóng — ma trận nhánh đủ/mảnh và native đại diện t54 |
| F3 | Đóng — 28 ca sẵn có; splitlines + gỡ chốt raw làm 27 ca lọt |
| F5 | Đóng — nhận kết quả, bộ ghi và mã thoát được ma trận bắt |
| F6 | Đóng — truyền giá trị bản ghi và tích luỹ nhóm có răng |
| F7 | Đóng — lỗi trước/sau, nhiều nhóm, không nuốt cấu hình |
| F8 | Đóng — CLI gom gọi đúng hàm/vân tay/tham số/exit |
| F9 | Đóng — HEAD thật và digest nguồn độc lập; nối kiểm toàn bytes F36 |
| F10 | Đóng — 7 ca nội suy/raw bị chặn, gỡ guard thì lọt |
| F11 | Đóng — t152 hai vế đạt; hook/ci có 5 AL_VER |
| F12 | Đóng — danh tính ca, hai kết quả và stdout nguyên văn có răng |
| F13 | Đóng — dispatcher --gop và mã thoát qua cửa thật |
| F14 | Đóng — 5 ca thiếu shell bị chặn, gỡ chốt thì lọt |
| F15 | Đóng — nguồn lỗi 0/1/>1, cộng nhiều nguồn được đo |
| F16 | Đóng — bộ đúng cấu trúc nhưng đích sống/tín dụng giả/bán kính 2 bị gom đỏ |
| F17 | Đóng — CLI nhiều lỗi trả đúng mã và bảng |
| F18 | Đóng — N=8, lỗi đúng 1, nhiều dòng và nhiều nguồn |
| F19 | Đóng — gom giữ nguyên từng dòng và danh tính/thứ tự |
| F20 | Đóng — đảo bảng qua CLI bị bắt |
| F21 | Đóng — writer đọc mọi record, cộng lỗi, in bảng, không để file sai |
| F22 | Đóng — mẫu bao gồm toàn bộ 28 mutant cũ tráo TEP_TEST; không giết thêm t52/t53/t54 |
| F23 | Đóng — nhiều ca bỏ qua, lý do đầy đủ và số đếm không nén |
| F24 | Đóng lỗi gốc — strict int version/index/count, symlink có năng lực bị loại; lớp năng lực còn F38 |
| F25 | Đóng — chỉ argv[1] chọn cửa; tên thư mục trùng cờ không chiếm dispatch |
| F26 | Đóng — cửa không đối số gọi main và sys.exit đúng |
| F27 | Đóng — k=0, đường ra khác x, worker 1/khác 1, tự kiểm nhánh đủ |
| F28 | Đóng — cửa mặc định trên cấu hình hợp lệ du/gate/mảnh và nhiều rc |
| F29 | Đóng — đầy đủ 27 ô vắng/rỗng/có và thẻ lỗi |
| F30 | Đóng — rc và grammar HEAD đều được đo bằng lưới độc lập |
| F31 | Đóng — gate có khoảng trắng bị từ chối, không strip/casefold |
| F32 | Đóng — cả hai độ dài 40/64 và bảng chữ lowercase hex |
| F33 | Đóng — mọi thành phần grammar k/N, biên và path, không còn survivor có nghĩa |
| F34 | Đóng — nguồn/lời gọi Git/ngoại lệ/bytes được chốt; F36 bổ sung đã đạt |
| F35 | Đóng lỗi gốc — identity phân hoạch, miền header/N, writer path/parent/IO; lớp năng lực còn F38 |
| F36 | Đóng — 7/7 phép cũ nay đúng t53 giet_that, mỗi phép đủ 56 ca |
| F37 | Chưa đóng lớp — đăng ký cũ đã vá thật; phép tự kiểm mới sinh F38 ở trạng thái thuộc tính vắng |

**Giới hạn đo:** Linux/Python 3.11.15; không đo Windows hoặc Python 3.12 thật. Môi trường vắng thuộc tính symlink của F38 là mô phỏng có đối chứng, không phải tuyên bố runner Ubuntu/Windows chuẩn đang có lỗi này. Chưa chạy 398/398, chưa có lượt A1 tám mảnh native rồi gom 8/8; phép round-trip mọi N=2..16 dùng bản ghi hợp lệ dựng sẵn và được phân biệt với bán kính thật. Không chạy GitHub CI, upload/download artifact thật, hoặc đo thời gian A9; không xác minh effort executor. Các giới hạn này không được điền bằng lời khai hay kết quả lượt trước.

**Bàn giao:** [README và lệnh tái lập](evidence-luot-16/README.md), [ma trận 263 phép](evidence-luot-16/mutation-matrix.md), [manifest bằng chứng](evidence-luot-16/manifest.json). Executor cần vá F38 theo lớp, bổ sung ca/mutant và đo lại; reviewer không sửa `cay-kho/`, không commit/push/đăng verdict lên GitHub, không thay vai human audit/land.

verdict: changes_requested
reviewed_sha: 54b4a01412e1d0240a1474258096ad64a4cbf0b9
