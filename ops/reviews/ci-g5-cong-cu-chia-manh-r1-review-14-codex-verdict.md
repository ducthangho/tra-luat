# Cross-review độc lập #668 — lượt 14

verdict: changes_requested
reviewed_sha: 9440dc111fa06682d9f82276fbc0cce7cfaed63a

Chỉ đo và phản chứng trên bản sao `/tmp`; không sửa cây ứng viên. Tệp được mở với `dang_review` rồi bổ sung dần. Các dòng “đang chạy/chưa đo được ở thời điểm ghi” bên dưới là nhật ký; **bảng kết luận cuối tệp là kết quả đã chốt**. Kết quả: **0 P1, 3 P2 (F33–F35), 0 P3** trong phạm vi đã đo.

HƯỚNG 1: Neo hiện vật, phạm vi và môi trường
  giả thuyết : bundle trỏ đúng ứng viên, đúng baseline và đặc tả.
  lệnh       : `git -C cay-kho rev-parse HEAD`; `git -C cay-kho status --short`; `sha256sum SPEC.md`; `git -C cay-kho diff --numstat f8a7829cc44f296c25faf1a6439b603ba840f70b`.
  output     : HEAD=9440dc111fa06682d9f82276fbc0cce7cfaed63a; status rỗng; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 5 tệp, +1612/−49.
  kết luận   : KHÔNG PHẢI LỖI. Trong trần ~1650 đã được chủ kho cấp trong chỉ thị lượt này. Reviewer OpenAI/Codex qua công cụ shell của phiên API; không tự nhận có audit máy cho model/effort hoặc human audit. Bản sao /tmp/review668-r14, môi trường tắt bytecode và ghim core.abbrev=7, commit.gpgsign=false. Mọi script bằng chứng sao từ lượt trước được đổi đường sang r14; không sao kết quả đo cũ.

HƯỚNG 2: Workflow — phản chứng có sẵn và đột biến bản vá
  giả thuyết : lớp F1/F3/F10/F14 tiếp tục chặn workflow sai, và ca có răng với bản vá bị gỡ.
  lệnh       : `python evidence-luot-14/env.py python -u evidence-luot-14/workflow.py`; `workflow_ablation_extra.py` (log ở evidence-luot-14).
  output     : control: F1 20/20, F3 28/28, F10 7/7, F14 5/5 không LỌT; gỡ F10 làm lọt đúng 7 ca F10. Các biến thể còn lại đang chạy, sẽ bổ sung kết quả cuối.
  kết luận   : KHÔNG PHẢI LỖI trong phần đã đo. Không tự soạn payload điều khiển/ẩn; chỉ chạy fixture sẵn và gỡ chốt của validator.

HƯỚNG 3: Miền chế độ và nguồn vân tay — kế hoạch phủ theo lớp
  giả thuyết : F29–F32 đã đóng toàn lớp, không chỉ các ô vừa vá.
  lệnh       : `measure.py r12-mutations.json`, `measure.py r13-mutations.json`, `measure.py r14-mutations.json`; `probe.py`; `mode_domain.py`, đều chạy qua `env.py` trên r14.
  output     : Đã khởi chạy; dữ liệu phép đổi mới ở `evidence-luot-14/r14-mutations.json`. Không dùng kết quả executor làm bằng chứng.
  kết luận   : KHÔNG ĐO ĐƯỢC trọn lớp tại thời điểm ghi khối này; sẽ thay bằng kết luận sau khi runner hoàn tất.

Miền cần kết luận của `_doc_che_do`: ba biến chỉ nhận chuỗi từ môi trường, từng biến vắng/rỗng/có giá trị; thứ tự ưu tiên lỗi ra-lẻ/ban-kinh/ca-hai/hình-dạng/phạm-vi/thiếu-ra; gate đúng `manh`, phân biệt hoa/thường và khoảng trắng; regex khớp toàn chuỗi, nhánh k=0, chữ số đầu 1..9 và chữ số sau 0..9 của CẢ k và N, độ rộng 1–2, dấu `/`, không dấu số, không số 0 đầu, không Unicode decimal; chuyển nhóm thành số; N=2..16, k<N; đường ra không rỗng và phải truyền nguyên văn; tuple và mode trả ra.

Miền cần kết luận của `_van_tay`: bytes từ đúng TEP_TEST, SHA-256/hexdigest; git ở đúng GOC, `rev-parse HEAD`, capture/text/timeout; rc=0 so với khác 0; OSError và SubprocessError; chuẩn hoá khoảng trắng stdout; fullmatch; HAI nhánh 40/64, từng khoảng chữ 0..9/a..f, phân biệt hoa/thường, độ dài và ký tự ngoài hex; None khi không có HEAD hợp lệ; dictionary trả về. Kiểm nhận đầu vào thật độc lập với kiểm răng của t53.

HƯỚNG 4: Hồi quy gate và công cụ
  giả thuyết : thay đổi không làm hỏng cổng cũ hoặc thay đổi Ruff F.
  lệnh       : `python evidence-luot-14/env.py python -u evidence-luot-14/run_regression.py`; so JSON Ruff theo code/tệp/message, bỏ số dòng dịch chuyển.
  output     : regression rc=0; head-registry rc=0 1025/1025; base-registry rc=0 938/938; gate rc=0 (243,1s), 56 ca, lỗi đột biến=0, tiền kiểm bỏ qua=0, cổng cây thật=ĐẠT. Head/base: t152 rc=0; lease t24/t31/t35/t161/t162 rc=0; actionlint rc=0; probe kiem-tra --json rc=0; Ruff cùng 6 F841, added=[], removed=[].
  kết luận   : KHÔNG PHẢI LỖI. Đây là gate trọn ở chế độ `manh` (giao bán kính), không tự gọi đó là chạy đủ 352 đột biến. Mẫu bán kính độc lập 130/352 đang chạy, toàn bộ mỗi phép chạy 56 ca.

HƯỚNG 5: Gom, mảnh và tệp đầu ra — checklist kế thừa
  giả thuyết : phân hoạch lệch, thứ tự artifact hoặc đầu vào sai có thể làm gom xanh sai.
  lệnh       : `partition_roundtrip.py`; `novel_files.py`; `probe.py` (đã đổi đường sang r14).
  output     : N=2..16 đều coverage=352, disjoint=True, gom_errors=0, table_order=True; 8 mảnh với tên tệp/thứ tự bản ghi đảo vẫn in đủ 352 dòng đúng thứ tự DOT_BIEN. Hardlink thừa ⇒ G-dem; FIFO/thư mục ⇒ G-tep; tệp cụt ⇒ G-ban-ghi; HEAD khác ⇒ G-van-tay; phục hồi bộ sạch ⇒ 0 lỗi. Kho git SHA-256 thật và 28 ô JSON kế thừa lượt 13 đều đạt kỳ vọng.
  kết luận   : KHÔNG PHẢI LỖI. Các bản ghi ở hướng này là dữ liệu tổng hợp để đo giao thức; không tính chúng vào mẫu đo bán kính thật.

HƯỚNG 6 (MỚI): Bất đối xứng trong grammar của hai toán hạng k/N
  giả thuyết : t53 chỉ thử một phía của regex, số 0 và đường ra, nên lỗi ở phía còn lại sống qua 56 ca.
  lệnh       : `domain.py` đọc `domains.json` và `r14-mutations.json`; `measure.py r14-mutations.json` đo toàn bộ 56 ca từng phép.
  output     : domain control khớp lưới; 258 cấu hình bổ sung gồm biên N, chữ số ASCII/Unicode ở từng vị trí, dấu số, dấu phân cách, độ rộng, ra rỗng/có khoảng trắng. Bảng đột biến đầy đủ đang chạy.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận răng cuối ở thời điểm ghi này; không dừng ở một ô đầu tiên.

  cập nhật   : Hai phép đầu `mode_k_width`, `mode_n_width` đã đo đủ 56 ca và đều 56/56 `qua` (`measure-mode_k_width.json`, `measure-mode_n_width.json`). Đây là hai biểu hiện của F33 (P2, tự kiểm chế độ), không phải hai finding riêng. Head gốc vẫn đúng; nới grammar làm đầu vào ba chữ số chuyển từ C-hinh-dang sang C-pham-vi mà t53 không phát hiện. Các ô còn lại và hint patch trọn lớp được bổ sung khi chạy xong.

  cập nhật 2 : Trọn 29 phép chế độ trong r14-mutations đã xong. 11 survivor thật: k_width, n_width, n_zero, n_unicode_first, n_unicode_tail, k_unicode_tail, k_sign, n_sign, separator, output_trim, output_space (tiền tố `mode_`). Các phép còn lại bị t53 và/hoặc t54 bắt. Ví dụ control từ chối `0/1٦`, mutant nhận `(0,16,x)`; control giữ nguyên ra=` y `, mutant cắt còn `y`.

  HINT PATCH F33 : sửa `_in_tu_kiem_che_do` và kỳ vọng của t53, không sửa `_doc_che_do` đang đúng. Cho bảng fixture chứa cặp `(env, expected)` cố định, child chỉ in kết quả thật, parent đọc kỳ vọng từ bản nguồn không đột biến. Bổ sung đủ 27 tổ hợp hiện diện/rỗng/đúng; toàn bộ 135 cặp hợp lệ N=2..16; k/N 0/1/2/16/17, k=N−1/N/N+1; số 0 đầu ở CẢ hai toán hạng, ba chữ số ở CẢ hai phía; từng vị trí chữ số Unicode ở k/N; dấu +/−, dấu phân cách khác `/`, thiếu toán hạng, khoảng trắng/trailing data; đường ra khác x, có space trong tên và space đầu/cuối, chuỗi toàn space (không rỗng). Mỗi lỗi phải so đúng thẻ, mỗi thành công phải so cả tuple và nguyên văn path. Tất cả 11 neo→thay trong r14-mutations phải bị t53 giết sau vá. Không lấy chính regex sản phẩm làm oracle; không đưa kịch bản vào main hoặc t52. Các phép thăm dò đã bị t54 bắt không đăng ký thêm như mutant 1/56 của t53 nếu chúng sẽ có hai ca đích. Danh sách cụ thể ở domains.json và mutation-matrix.md.

HƯỚNG 7 (MỚI): Lỗi thực thi nguồn Git và ngữ pháp HEAD theo từng nhánh
  giả thuyết : nhánh 64 có thể bị nới riêng; t53 không đo lỗi phóng Git/timeout và mọi giá trị rc khác 0.
  lệnh       : `domain.py`: 275 ô nguồn gồm rc=0/1/2/−9 × stdout, các độ dài 39/40/41/63/64/65, chữ 0..9/a..f/hoa/ngoài hex trên cả 40 và 64, khoảng trắng; OSError/SubprocessError/TimeoutExpired; lưu lời gọi Git.
  output     : CONTROL_PASS. Trên bản sao hàm, bỏ bắt OSError làm 1 ô ném; bỏ bắt SubprocessError làm 2 ô ném; đổi rc==0 thành rc!=1 nhận sai rc=2/−9; các nới regex riêng nhánh 64 nhận sai đầu vào. Kết quả đo 56 ca đang chạy.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận răng cuối ở thời điểm ghi này. Không có dấu hiệu head nguyên bản nhận HEAD sai; đây là phép kiểm xem tự kiểm có giữ được hợp đồng không.

  cập nhật   : F34 (P2) đã được xác nhận qua 56 ca: nới riêng bảng chữ/hoa-thường/underscore của nhánh 64, thêm underscore cho nhánh 40, hoặc thu hẹp nhánh 64 bỏ chữ f đều 56/56 qua. F32 cũ vá thật với phép nới đồng thời hai nhánh, nhưng chưa khép toàn grammar. Đang chờ phần nguồn/exception/bytes của cùng lớp; không tách mỗi biểu hiện thành finding khác.

  cập nhật 2 : Toàn 52 phép r14-mutations đã xong. Ngoài 6 survivor grammar HEAD, còn `head_strip_left`, `head_rc_two`, `head_no_oserror`, `head_no_subprocesserror`, `source_text_bytes` sống qua 56 ca. `head_timeout` và `head_rev_ref` cũng sống, được phân biệt riêng: timeout ảnh hưởng liveness, HEAD~0 vẫn cùng commit; không dùng hai phép ấy chứng minh nhận sai HEAD. Tất cả 275 ô nguồn của control đạt; F34 là thiếu răng, không phải nguồn trên head nguyên bản đang sai.

  HINT PATCH F34 : ở `_in_tu_kiem_che_do`/t53, thay lưới Git chỉ 10 ô bằng bảng hai nhánh 40/64 độc lập. Mỗi nhánh có HEAD hợp lệ chứa đủ 0..9/a..f; biên độ dài ngay dưới/đúng/ngay trên; chữ hoa, g/z, underscore và chữ số Unicode ở đầu/giữa/cuối; prefix/suffix, nhiều token; rc=0/1/2/âm với stdout hợp lệ/rỗng/sai; khoảng trắng hai phía; ba exception OSError/SubprocessError/TimeoutExpired. Spy ghi argv, GOC, capture/text/timeout để xác định rõ chốt tham số, nhưng không giả vờ đo được một tiến trình treo thật. Đặt TEP_TEST vào tệp fixture nhỏ trong lưới để tránh băm lại cả bộ test hàng trăm lần. Kiểm bytes với oracle hashlib của parent; dùng các fixture byte khác nhau và giữ HEAD không đổi, rồi đổi HEAD giữ bytes, không git ⇒ None. Theo phân công, biến thể byte mới chỉ MÔ TẢ: một tệp chứa CR U+000D ngay trước LF U+000A và bản khác chỉ chứa LF; `_van_tay` gốc phải cho hai SHA khác, `read_text().encode()` chuẩn hoá newline nên cho cùng SHA. Bash không tham gia phép này. Executor tự viết fixture ấy; reviewer không tự dựng chuỗi điều khiển. Các neo→thay cần giết ở r14-mutations, ca đích t53; giữ t52 dùng cùng `_van_tay` cho cả producer/consumer, không tự băm độc lập ở t52 (tránh tái mở bán kính 2 kiểu F9). Khôi phục GOC/TEP_TEST/subprocess trong finally; không đòi thêm cong_cu.py vào kho tạm.

HƯỚNG 8 (MỚI): Biên hợp lệ của bộ gom và tiền tố giao thức
  giả thuyết : ca gom N=3 và ca âm N=1 chưa phân biệt từng đầu mút 2/16/17; JSON hỏng chưa đo riêng tiền tố MANH.
  lệnh       : `measure.py r14-artifact-mutations.json target` (sàng lọc); bản đầy đủ 56 ca đã xếp chạy; `domain.py` dựng bộ mảnh N=1/2/3/16/17 và đổi riêng 5 byte tiền tố thành ABCDE.
  output     : head gốc nhận 2/3/16, từ chối 1/17; đầu tệp ABCDE ⇒ G-dau. Bỏ chốt trên hoặc nâng lên 17 ⇒ GOM MẢNH 17/17; bỏ kiểm MANH ⇒ GOM MẢNH 3/3 trên bộ có một đầu tệp ABCDE. Các phép này qua riêng t52; chưa dùng bước sàng lọc đó thay kết quả 56 ca.
  kết luận   : KHÔNG ĐO ĐƯỢC răng trọn bộ ở thời điểm ghi này; ứng viên F35 thuộc lớp gom/bộ ghi, sẽ gộp mọi biểu hiện khi runner hoàn tất.

  cập nhật   : `gom_n_min` và `gom_n_max_low` đã 56/56 qua; F35 (P2) xác nhận lớp artifact chưa đóng. Lưới mở rộng còn chứng minh bỏ chốt tiền tố nhận ABCDE, cho riêng `manh` kiểu float nhận 0.0, bỏ tạo parents làm đường hợp lệ nhiều tầng lỗi, trim path ghi sai tên, và gỡ is_symlink để lại symlink gãy. Các phép này đang được đo đủ 56 ca. Không xem các kết quả tổng hợp `GOM MẢNH` là bán kính thật.

  HINT PATCH F35 : sửa giàn giáo `_in_tu_kiem_gom` và assertions t52. Giữ thuật toán `_gom_manh`/`_ket_thuc_manh` nguyên trạng. Thêm round-trip thật ở N=2 và N=16 (đủ tên, bảng đúng nguyên văn), ca N=0/1/17 bị đúng G-n; tiền tố sai 5 ký tự nhưng JSON/thân hoàn toàn hợp lệ; ma trận bool/float/string/null/list/dict trên MỖI trường phien_ban/manh/so_manh (đặc biệt manh=0.0); giữ các ca hash/HEAD, tập chỉ số, trùng/thiếu/chuyển tên, bản ghi đúng schema sai kết quả. Thêm nhánh lỗi đọc bằng stub Path.read_bytes cục bộ trả OSError, khôi phục trong finally, đòi G-dau. Phía ghi thêm đường cha nhiều tầng chưa tồn tại, tên có khoảng trắng cuối, symlink gãy cũ trên nhánh ket=None/head=None/kết quả đỏ: assert cả exists và is_symlink đều false, target ngoài không bị đụng. Cần đối chứng dương file thường ghi đúng path/nội dung, parent đã tồn tại, N=2/16; đối chứng âm I/O vẫn đỏ. Từng neo→thay có nghĩa trong r14-artifact-mutations phải bị t52 bắt. Có thể dùng một bảng DOT_BIEN nhỏ gồm tên hiện hữu, khôi phục trước các fixture khác, để giới hạn chi phí; không hardcode tổng 352 hay tách phân hạng mới. Không gắn các ca này vào t53/t54: nếu cùng chốt làm nhiều ca chết thì chỉ tạo bán kính rộng. Hai phép `gom_drop_decodeerror` và đảo thứ tự bản ghi serialization là tương đương: UnicodeDecodeError đã thuộc ValueError; gom cố ý nhận mọi thứ tự bản ghi. Không cần tạo mutant riêng cho chúng.

Miền artifact đã kiểm kê: tồn tại/loại/rỗng của thư mục; mọi mục đều phải được xét, không lọc bỏ mục xấu; file thường/symlink/FIFO/subdir/hardlink; đọc/giải mã/JSON/prefix; object và đúng tập 5 khóa; kiểu số nguyên nghiêm ngặt của ba trường (bool không phải int hợp lệ), version; HEAD và hash của chính gom; dòng ngoài BKCON; N đồng nhất và 2..16; đúng tập k và đúng một file/k; tổng và hợp phân hoạch; receiver đúng nhóm/rc=0/nền rỗng và mọi trường bản ghi; bảng tên/thứ tự/chi tiết và tổng lỗi; CLI giữ argv/rc/stdout. Writer: xóa file/symlink cũ; ket=None, HEAD=None, thiếu bản ghi, kết quả đỏ một/nhiều lỗi; không ghi khi đỏ; tham số k/N/path/tên/vân tay; tạo parent, serialization, bảng trả và rc. Các guard dự phòng không thể tới qua đầu vào hợp lệ, hoặc phép đổi vẫn fail-closed, được phân loại riêng thay vì bịa đường xanh.

HƯỚNG 9: Ma trận main/dispatcher — không nhầm ca đích với toàn suite
  giả thuyết : các lớp đóng ở lượt 12 vẫn giữ răng qua head này.
  lệnh       : `run_checklists.py` (138 phép lượt 5–10), `fields_full.py` (17), `novel_entry.py` (3), `partition_identity.py` (2), `measure.py r12-mutations.json` (7); thêm hai phép tương đương dự kiến ở r14-extra.
  output     : đang chạy từng phép qua 56 ca. Phép `mode_n_min` qua t53 nhưng bị t54 giết trên manh_12; `mode_output_constant` qua t53 nhưng bị t54 giết với đường ra khác x. Không báo hai phép ấy là survivor. `mode_n_max_low`/`mode_k_strict` bị cả t53/t54 giết: đây là đột biến thăm dò ngoài DOT_BIEN, không suy thành hồi quy bán kính của bộ 352.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận toàn ma trận cho tới khi đủ tệp kết quả. Miền main được kê dưới đây; không tự coi sống tương đương là đường CI xanh.

Miền main/dispatcher: cấu hình được đọc trước tiền kiểm/CA và lỗi trả 2; hai tiền kiểm, thứ tự và lý do; từng CA đúng một lần/thứ tự/danh tính; AssertionError, exception và BoQua; đếm đạt/đỏ/bỏ qua/tổng/mẫu số; truyền k/N/ra và phân hoạch; nền đỏ hay tiền kiểm bị bỏ qua thì dọn tệp, không phóng con và trả 1; tên/nền rỗng/workers khi phóng; nhóm/rc/stdout/nền rỗng khi nhận; gom đủ dữ liệu, bảo toàn lỗi đầu/rc/đuôi 300 ký tự; toàn bộ 7 đối số bộ ghi ở nhánh sạch và nhánh dọn; bảng nhiều dòng và rc 0/1 khi lỗi bằng 0/1/>1; nhánh đủ/gate gọi cổng đúng GOC và đủ tự kiểm, giữ tập nền sắp xếp; cộng lỗi từ nhiều nguồn và nhiều kết quả; gate không đo bán kính, đủ truyền nguyên danh sách DOT_BIEN/nền/workers; mọi trường summary và stdout; dispatcher không đối số, --gop, vị trí argv, đối số thừa/lạ và tên thư mục trùng cờ; sys.exit giữ rc. Checklist cũ đo k=0, N=2/8/16, path khác x, workers=1/2/3/4. Nhánh mảnh rỗng không phát sinh với 352 tên và N≤16.

HƯỚNG 10: Nhiễu t5 trong một lượt đột biến
  giả thuyết : lỗi phụ thuộc lịch chạy có thể bị nhầm thành bán kính rộng mới.
  lệnh       : đọc `main-no_cleanup.json`; giữ bản đầu `raw-main-no_cleanup-first.json`; `recheck_noise.py`; chạy lại riêng no_cleanup.
  output     : lần đầu no_cleanup bị t54 giết đúng, thêm t5 rc=141 từ cai_cong_cu.sh. Control t5 trên baseline 8/8 qua, head 8/8 qua. Retry toàn 56 ca đang chạy. Dữ liệu thô giữ nguyên; không xoá dấu lỗi đầu.
  kết luận   : KHÔNG ĐO ĐƯỢC nguồn nhiễu từ chỉ một lần; không tính nó thành finding của packet khi chưa đối chiếu xong. Bán kính mẫu và kết luận cuối sẽ ghi rõ raw/retry.

  cập nhật   : retry no_cleanup đủ 56 ca chỉ giết đúng t54. Mã của t5 và cai_cong_cu.sh không nằm trong diff packet; lần đầu rc=141 được giữ ở raw-main-no_cleanup-first.json, không dùng lời khai “ngay lượt đầu mọi phép đều 1/56”.

  cập nhật 2 : mẫu thật `g668_gom_bo_kieu_int` lần đầu có t5 rc=141 ngoài t52; retry riêng đạt 1/56 đúng t52. Bản raw vẫn ở sample/radius-g668_gom_bo_kieu_int.json, retry ở retry-g668_gom_bo_kieu_int.json. Thêm 64 lượt t5 trên baseline + 64 trên head đều qua (noise-ab-64.log). Chưa xác định dứt điểm nguyên nhân rc=141 trong sandbox; không gọi đây là lỗi mới của #668 và cũng không xoá nó khỏi báo cáo.

HƯỚNG 11: Phân hoạch — kiểm lại nhận định “tương đương” của lượt 12
  giả thuyết : đủ/rời nhau chưa chứng minh đúng nhóm k mà M2 yêu cầu.
  lệnh       : `partition_identity.py` (2 phép × 56 ca); `domain.py`, phần `partition-oracle.json`: đối chiếu trực tiếp `_phan_manh(k,n)` với `list(DOT_BIEN)[k::n]` trên N=2..16, mọi k.
  output     : control mismatch=0/135; partition_rotation mismatch=135/135; partition_reverse_source mismatch=135/135. Cả hai mutant vẫn 56/56 qua. Coverage/gom của chúng vẫn đủ nên phép round-trip tự dùng cùng bộ chia ở hai phía không phát hiện.
  kết luận   : LỖI (P2), gộp F35. Tôi không kế thừa kết luận “tương đương” cho hai phép này: chúng tương đương về tổng độ phủ nhưng KHÔNG tương đương với công thức chuẩn `i % N == k` của M2. Đây là thiếu oracle độc lập của lớp phân mảnh, không phải finding mới của dây nối main.

HƯỚNG 12: Hệ quả của nguồn Git ném lỗi trước bước dọn tệp
  giả thuyết : thiếu răng ở nhánh exception của `_van_tay` có hậu quả ngoài nhãn chẩn đoán.
  lệnh       : `domain.py`, phần `source-cleanup.json`: main mảnh có nền đỏ, tệp STALE sẵn, Git giả ném OSError hoặc TimeoutExpired.
  output     : control cả hai ô rc=1, stale_exists=false; no_oserror ⇒ RAISED:OSError, stale_exists=true; no_subprocesserror ⇒ RAISED:TimeoutExpired, stale_exists=true. Hai mutant đều đã sống qua 56 ca.
  kết luận   : LỖI (P2), cùng F34. `_van_tay()` là đối số được tính TRƯỚC `_ket_thuc_manh`; mất sentinel None làm bước dọn không được gọi. CLI vẫn không xanh, nên không gán P1.

KẾT QUẢ CHỐT — thay các trạng thái tạm trong nhật ký trên

- Exact head: `9440dc111fa06682d9f82276fbc0cce7cfaed63a`; tree: `d56ed1f2dc22c7bfed8a217c86d417a203a50802`. `cay-kho/` sạch, không sửa sản phẩm.
- **254/254 phép**, mỗi phép có đủ 56 trạng thái: checklist 138 lượt 5–10; 17 trường main + 3 dispatcher + 2 phân hoạch lượt 11; 7 lượt 12; 4 lượt 13; 83 phép bổ sung lượt 14. **190** bị đúng ca đích dự kiến giết, **17** phép thăm dò làm ca khác/nhiều ca chết hoặc giàn giáo báo tín dụng giả, **47** sống. Không gọi 17 phép ngoài `DOT_BIEN` ấy là hồi quy bán kính của bộ chuẩn. Chi tiết từng phép: [mutation-matrix.md](evidence-luot-14/mutation-matrix.md), [review-summary.json](evidence-luot-14/review-summary.json).
- **130/352 đột biến chuẩn** được chọn có chủ đích: 41 cũ + 89 mới; bao gồm toàn bộ 44 mutant đích t52 và 20 mutant đích t53, 25 đại diện t54, cùng nhóm cũ phụ thuộc TEP_TEST. Kết quả theo `_ket_luan_ban_kinh`: 130/130 bán kính 1/56 sau một retry đã khai rõ; raw 129/130. Không mutant cũ nào giết thêm t52/t53/t54. Có 11 trạng thái bỏ qua ngoài ca đích trong hai cây đột biến cũ t6/t21 thiếu phụ thuộc; được tách riêng ở [sample-skips.json](evidence-luot-14/sample-skips.json), không đánh tráo thành `qua`.
- Đối chứng cuối cho 11 trạng thái bỏ qua: chạy lại chính hai mutant t6/t21 trên baseline bằng `retry_base.py`; cả hai đạt 1/53, và tập ca bỏ qua lần lượt 6/5 **trùng hoàn toàn** với head. Bằng chứng [baseline-skip-comparison.json](evidence-luot-14/baseline-skip-comparison.json); đây là giới hạn fixture cũ, không phải hồi quy do ba ca mới.
- G5 gate chế độ giao mảnh: rc=0, 56/56, tiền kiểm bỏ qua=0, các tự kiểm và cổng cây thật ĐẠT. Registry cấu trúc/phản chứng: head 1025/1025, base 938/938. t152, 5 ca lease yêu cầu, actionlint và probe công cụ đều rc=0 hai phía; Ruff F delta=0 (6 F841 có sẵn).
- Workflow: 60 ca lịch sử F1/F3/F10/F14 đều chặn. Gỡ F10 lọt 7/7; gỡ F14 lọt 5/5; gỡ guard thực thi lọt 13 F1; gỡ cả guard thực thi và shell lọt 18 F1; `splitlines()` đơn lẻ còn được F10 che, gỡ cả F10 và đổi splitlines lọt 27 F3. Hai ca F1 còn lại vẫn có guard khác. Toàn registry thật và actionlint đều xanh.
- **Chưa đo** đủ 352, A1 thật 8 mảnh rồi gom và đối chiếu từng dòng với lượt đủ, Windows/Python 3.12 và thời gian runner A9. Môi trường này là Linux, Python 3.11.15. Không chạy CI từ xa, không nhận bằng chứng A1 executor chưa hoàn tất làm kết luận. Các bảng tổng hợp 352 dòng trong round-trip chỉ là kiểm giao thức.

Bảng lớp

| Lớp | Miền đã đo | Trạng thái |
|---|---|---|
| Workflow/thực thi G5 | Khóa workflow/job/step, env kế thừa, shell Bash, defaults/working-directory, checkout/setup, matrix OS/k, needs/if/fail-fast, thứ tự probe/test/setup/artifact, run literal/LF/không biểu thức, upload/download đúng hình dạng; phản chứng và ablation ở HƯỚNG 2 | **đóng** trong miền này |
| main/dispatcher | Trọn danh mục quyết định/đối số/stdout/rc ở HƯỚNG 9; cấu hình sai/dương, k=0/N=2/8/16, path/workers khác, nhiều lỗi/bỏ qua/kết quả, entry mặc định và --gop | **đóng**; helper chế độ/nguồn/phân hoạch được xét riêng |
| Đọc chế độ | Hiện diện/rỗng, ưu tiên lỗi, gate, hai toán hạng regex và chuyển nhóm, giới hạn số, tuple/path; 10.816 cặp số, 258 cấu hình bổ sung, 35 phép đổi gồm checklist cũ | **chưa đóng — F33** |
| Nguồn vân tay | Bytes/thuật toán/đường nguồn, Git/GOC/argv/kwargs, rc, exceptions, strip, toàn grammar HEAD 40/64; lưới rc×stdout cũ + 275 ô mới; 33 phép đổi gồm checklist cũ | **chưa đóng — F34** |
| Phân mảnh/gom/CLI/bộ ghi | Miền đầy đủ đã kê ở HƯỚNG 8; N=2..16 round-trip; từng trường header và bản ghi; lỗi nhiều dạng, bảng/rc, file/IO/path; oracle độc lập của 135 nhóm; checklist cũ và 22 phép mới | **chưa đóng — F35**; riêng nối CLI và kết luận bản ghi cũ giữ răng |
| Hồi quy G5/registry/công cụ | Gate trọn chế độ manh, registry, t152, lease, actionlint, Ruff F; mẫu 130 có chủ đích và ngoại lệ raw/retry/skip đã khai | **đạt phạm vi đã đo**; không mở rộng thành chứng nhận 352/A1/Windows |

Bảng finding

| F | Lớp | Mức | Tệp:dòng | Mô tả | Phản chứng |
|---|---|---|---|---|---|
| F33 | Đọc chế độ/t53 | P2 | ops/cong_cu_test.py:6695, 7255, 7755 | 11 phép nới grammar hoặc đổi xử lý path sống; có cấu hình sai được nhận và path hợp lệ bị đổi/từ chối | `r14-mutations.json`: 11 `mode_*` đã liệt kê ở HƯỚNG 6; từng `measure-*.json` đều 56/56 qua; `domain-results.json` chứng minh lệch |
| F34 | Nguồn vân tay/t53 | P2 | ops/cong_cu_test.py:6695, 7289, 7755 | Lưới nguồn chưa gác độc lập nhánh 64, bảng chữ, rc≠1, trim, exception, timeout và bytes; 12 survivor có nghĩa, không tính HEAD~0 | `head_64_alpha/case/ascii_extra/narrow/decimal_only`, `head_40_ascii_extra`, `head_strip_left`, `head_rc_two`, `head_no_oserror`, `head_no_subprocesserror`, `head_timeout`, `source_text_bytes`; lưới và `source-cleanup.json`; biến thể CRLF mô tả bằng lời |
| F35 | Phân mảnh/gom/bộ ghi/t52 | P2 | ops/cong_cu_test.py:6644, 7284, 7302, 7330, 7421 | Thiếu oracle đúng danh tính phân hoạch; thiếu biên N/prefix/type manh/read-error và path/parent/symlink của bộ ghi | 2 `partition_*` sống nhưng sai 135/135 nhóm; 4 `gom_n_*`, `gom_drop_head_prefix`, `gom_manh_float`, `gom_drop_oserror`, `writer_broken_link`, `writer_parents`, `writer_path_trim` đều sống; `artifact-domain-results.json` chứng minh lệch |

Ba finding trên là thiếu răng theo M4. Không có phản chứng nào ở đây chứng minh head **chưa đột biến** tự gom xanh trên bộ sai hoặc tự bỏ đo bán kính mà CI xanh.

HINT PATCH — gợi ý cho executor, chưa áp lên cây sản phẩm

**F33 — đóng cả miền chế độ.** Tệp/hàm, toàn bộ ô, neo→thay và rủi ro đã nêu ngay dưới HƯỚNG 6. Dữ liệu có thể chuyển thẳng thành fixture: [domains.json](evidence-luot-14/domains.json) và [r14-mutations.json](evidence-luot-14/r14-mutations.json). Child tính actual, parent giữ kỳ vọng độc lập; không dùng chính `_doc_che_do`/regex của nó sinh expected. Đích giết là **t53** cho 11 survivor. Những phép như N tối thiểu 3, k=0 bị đổi hoặc path cố định đã bị t54 bắt: giữ bằng chứng ấy, không đăng ký bừa mutant t53 làm bán kính thành 2.

**F34 — đóng cả nguồn và grammar HEAD.** Thực hiện bảng hai nhánh, nguồn bytes và lưới lỗi trong HƯỚNG 7; các cặp neo→thay đã có trong JSON. Đích giết là **t53**. Với exception được cố ý bơm, giàn giáo phải bắt exception từ chính lời gọi `_van_tay` và đưa tên exception thành dữ liệu actual để parent so với HEAD=None; đừng để child chết rồi tính tín dụng giả. Lỗi dựng repo Git thật vẫn phải phân biệt là lỗi giàn giáo. Thêm assertion spy `timeout=60` cho phép `head_timeout`; phép đo lượt này xác nhận mất tham số timeout, không tuyên bố đã chạy con treo thật. Giữ t52 lấy vân tay bằng cùng hàm ở hai phía; không nhét oracle hash độc lập vào t52. Phản chứng CRLF chỉ là mô tả theo phân công, executor tự dựng byte. Chạy lại đủ đột biến t53 và mẫu cũ sau vá để tránh tái tạo bán kính 2/F22.

**F35 — đóng cả phân hoạch và artifact.** Ngoài toàn bộ bảng ô/path/schema ở HƯỚNG 8, thêm oracle danh tính phân hoạch vào t52: child trả thứ tự tên nguồn `list(DOT_BIEN)` cùng các nhóm actual cho N=2..16; parent so nhóm k với lát cắt `nguon[k::N]`, tuyệt đối không gọi `_phan_manh` để dựng expected. Cách này cũng tránh parent của runner reviewer có thêm mutant làm tổng tên khác child. Hai neo `if i % n == k → if (i + 1) % n == k` và `enumerate(DOT_BIEN if ten is None else ten) → enumerate(list(DOT_BIEN if ten is None else ten)[::-1])` phải bị **t52** giết. Các neo của 10 biểu hiện còn lại nằm trong [r14-artifact-mutations.json](evidence-luot-14/r14-artifact-mutations.json), cũng đích **t52**. N=0 phải dùng thư mục không rỗng với header đồng loạt khai 0; tạo 0 file chỉ đo G-rong. N=17 cần tách khỏi lỗi thiếu mảnh/bản ghi bằng expected tag G-n; N=2/16 phải có đối chứng gom xanh. Symlink chỉ đăng ký ca/mutant khi `_CO_SYMLINK`; restore mọi monkeypatch/bảng tên trong finally. Không thay thuật toán đang đúng, không gắn thêm oracle này vào t53/t54, không thêm phụ thuộc `cong_cu.py` vào fixture cũ. Giữ `_ket_luan_ban_ghi` dùng chung để không giết oan mutant phân hạng của t29.

Ngân sách: hiện +1612, còn khoảng 38 dòng so với trần ~1650. Nên tổ chức lại bảng fixture/đột biến thay vì tiếp tục chồng từng ca; hint này không tự cấp thêm trần dòng.

Các survivor không dùng làm finding

- Sáu phép cũ: `receiver_baseline` chỉ thêm tên ngoài CA; `break_on_error` vẫn đỏ và không ghi, các con đã được `_phong_con` chạy xong; `final_hong` được lỗi nền bảo vệ; `final_gate_eq_one` đúng miền 0/1 của cổng; `main_no_sorted_baseline` được helper sắp xếp; `writer_drop_missing` vẫn KeyError/không file, còn đầu vào của writer được receiver đảm bảo đủ tên.
- `main_receiver_baseline_hong`: nhánh mảnh chỉ tới receiver khi hong rỗng. `main_empty_launch_guard` và `main_receive_false`: với 352 tên, 2≤N≤16 và số worker được kẹp theo số tên, không có nhóm con rỗng.
- `head_rev_ref` dùng HEAD~0 vẫn cùng commit; `gom_drop_decodeerror` vẫn bắt UnicodeDecodeError qua ValueError; `writer_record_order` chỉ đảo thứ tự dòng BKCON, giao thức gom cố ý nhận thứ tự bất kỳ. Tổng **12** phép thuộc nhóm này. Hai phép partition của lượt 12 đã bị loại khỏi nhóm tương đương bằng HƯỚNG 11.

ĐỐI CHIẾU F1–F32 (trừ F4)

“Đóng” ở bảng này là phản chứng cụ thể đã vá; trạng thái toàn lớp luôn theo bảng lớp phía trên.

| Finding cũ | Trạng thái tại head này | Bằng chứng/lý do |
|---|---|---|
| F1 | đóng | 20 phản chứng workflow chặn; ablation thực thi có ca lọt |
| F2 | đóng | ma trận main chọn đủ/gate/mảnh, tên/phóng/nhận và rc |
| F3 | đóng | 28 ca chặn; gỡ F10 + splitlines lọt 27 |
| F5 | đóng | ca main/giàn giáo đi qua TEP_TEST, đột biến có răng |
| F6 | đóng | checklist nhánh và tham số main đã chạy lại đủ |
| F7 | đóng | lỗi nhóm đầu/cuối, ghép dữ liệu, lý do, dọn và rc được đo |
| F8 | đóng | CLI gọi gom/vân tay, giữ rc/stdout và arity |
| F9 | đóng phản chứng cũ | nguồn hằng/nguồn sai bị t53 bắt; **toàn lớp còn F34** |
| F10 | đóng | 7 ca chặn, gỡ guard lọt 7 |
| F11 | đóng | t152 hai phía qua, head ghi 5 vị trí |
| F12 | đóng | từng danh tính ca, nhiều kết quả và stdout nguyên văn |
| F13 | đóng | dispatcher --gop qua CLI thật, mutant bị t52 giết |
| F14 | đóng | 5 ca thiếu shell chặn, gỡ guard lọt 5 |
| F15 | đóng | giá trị lỗi 0/1/>1, nhiều nguồn cộng dồn |
| F16 | đóng phản chứng cũ | bộ đúng schema/sai kết quả bị kết luận đỏ; **artifact còn F35** |
| F17 | đóng | CLI giữ 1 khi có nhiều lỗi, giữ 2 với lỗi đối số |
| F18 | đóng | N khác 8, nhiều dòng/lỗi/nguồn, truyền đủ tham số |
| F19 | đóng | bảng gom đủ tên/thứ tự/chi tiết, mutant nén bảng bị giết |
| F20 | đóng | đảo bảng CLI bị t52 giết |
| F21 | đóng phản chứng cũ | lỗi bản ghi đầu/cuối và cộng đủ lỗi; **writer còn F35** |
| F22 | đóng | 41 mutant cũ không giết thêm t52/t53/t54; fixture không đòi cong_cu.py |
| F23 | đóng | nhiều ca bỏ qua, đếm và nguyên lý do lỗi con |
| F24 | đóng phản chứng cũ | bool/float version và symlink bị bắt; **manh=0.0 còn F35** |
| F25 | đóng | cửa chỉ ở argv[1], path trùng tên cờ không chiếm dispatcher |
| F26 | đóng | bỏ main/mất sys.exit bị t54 giết |
| F27 | đóng | k=0, path khác x, workers khác, lỗi tự kiểm nhánh đủ |
| F28 | đóng | cả ba mutant cửa mặc định trên cấu hình hợp lệ bị t54 giết |
| F29 | đóng phản chứng cũ | 3 mutant truthiness bị đúng t53 giết, lưới 27 ô đúng; **mode còn F33** |
| F30 | đóng phản chứng cũ | bỏ rc/bỏ format bị đúng t53 giết; **nguồn còn F34** |
| F31 | ĐÃ VÁ THẬT | trim gate bị đúng t53 giết; ca gốc đúng C-ban-kinh |
| F32 | ĐÃ VÁ THẬT ở phép cũ | range độ dài/nới alphabet cũ bị t53 giết; **nhánh 64 và toàn nguồn chưa đóng — F34** |

verdict: changes_requested
reviewed_sha: 9440dc111fa06682d9f82276fbc0cce7cfaed63a
