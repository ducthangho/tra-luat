# Cross-review độc lập packet #668 — lượt 15

trang_thai_luc_mo_review: dang_review
reviewed_sha: b3863e2af32cc8892144d9c573667a98701ab614

Chỉ đo trên bản sao trong `/tmp`; không sửa mã sản phẩm trong `cay-kho/`. Kết quả các lượt trước chỉ dùng làm checklist.

HƯỚNG 1: Định danh, phạm vi, môi trường
  giả thuyết : bundle lệch head/spec hoặc vượt write set/trần đã duyệt.
  lệnh       : sha256sum SPEC.md; git -C cay-kho rev-parse HEAD HEAD^{tree}; git diff --numstat baseline HEAD; git status --short.
  output     : spec dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; head b3863e2af32cc8892144d9c573667a98701ab614; tree 8b0f108f2a8c07f1dfbb2f73752178118ba53d36; sạch; +1839/-49 đúng 5 tệp W1–W5.
  kết luận   : KHÔNG PHẢI LỖI. Lease g2, trần ~1900 và lặp review do chỉ thị chủ kho; không kích hoạt CI/đăng ngoài. Sandbox /tmp/review668-r15 và baseline /tmp/review668-r15-base, core.abbrev=7, commit.gpgsign=false; runner + dữ liệu chép lại vào evidence-luot-15, không chép kết quả cũ.

Danh tính reviewer: OpenAI Codex qua API và công cụ shell của phiên này; phiên độc lập với executor. Không có attestation ngoài để tự chứng minh model/effort hoặc launcher cụ thể; không suy danh tính từ actor GitHub. Review kỹ thuật theo sensitive, ngưỡng chỉ thị 0 P1/P2/P3; human audit vẫn là cổng land.

HƯỚNG 2: Workflow — chạy lại phản chứng và đột biến bản vá
  giả thuyết : lớp thực thi F1/F3/F10/F14 tái mở.
  lệnh       : python evidence-luot-15/env.py python -u evidence-luot-15/workflow.py; workflow_ablation_extra.py.
  output     : control chặn 20 F1 + 28 F3 + 7 F10 + 5 F14. Gỡ F10 lọt 7/7; gỡ shell F14 lọt 5/5; bỏ guard thực thi lọt 13 F1. Output chi tiết lưu workflow-*.log và workflow-summary.json.
  kết luận   : KHÔNG PHẢI LỖI trong miền lịch sử đã đo. Không tự soạn payload điều khiển/ẩn; chỉ chạy fixture có sẵn và đổi validator trên bản sao.

  biến thể mới chỉ MÔ TẢ, chưa chạy: đặt ZERO WIDTH SPACE U+200B ngay trước dấu # của một dòng dự định là chú thích trong bước gom. Bash không xem ký tự ấy là khoảng trắng cú pháp, nên dòng trở thành tên lệnh lạ và phải đỏ; validator hiện phải từ chối ở guard ký tự không in được trước khi phân tích dòng. Executor có thể thêm ca để xác nhận. Đây không phải bằng chứng P1 và không được tính vào 60 ca đã chạy.

HƯỚNG 3: Miền trọn của chế độ, nguồn và main — định nghĩa trước kết luận
  giả thuyết : các ca mới chỉ vá đúng biểu hiện cũ, còn thiếu nhánh/so sánh/tham số.
  lệnh       : run_checklists.py; fields_full.py; novel_entry.py; partition_identity.py; measure.py prior-mutations.json; domain.py; mode_domain.py.
  output     : đang đo lại 138 phép checklist lượt 5–10, 17 trường main, 3 entry, 2 phân hoạch và 94 phép r12/r13/r14; mỗi phép đầy đủ 56 trạng thái. domain.py có oracle ngoài tiến trình, không lấy kết quả cũ làm kết quả lượt này.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận cuối cho tới khi các runner hoàn tất.

Miền `_doc_che_do`: ba biến B/M/R mỗi biến vắng/rỗng/đúng (27 ô), giá trị lạ/hoa/thường/space; ưu tiên ra-lẻ → du/gate khi M vắng, ca-hai khi M hiện diện; regex fullmatch, nhánh k=0, chữ đầu 1..9 và đuôi 0..9 tùy chọn ở cả k/N, ASCII/Unicode từng vị trí, dấu phân cách '/', dấu +/−, độ dài, số 0 đầu, prefix/suffix/khoảng trắng; ép đúng hai group sang int; N=2..16, k<N; RA vắng/rỗng và mọi chuỗi không rỗng giữ nguyên; cả tên chế độ lẫn tuple trả về.

Miền `_van_tay`: đúng TEP_TEST, mọi bytes của tệp (rỗng/ngắn/nhiều khối, hoa/thường/non-ASCII), SHA-256/hexdigest; đúng git/-C/GOC/rev-parse/HEAD, capture_output/text/timeout=60; rc=0/1/2/âm; OSError/SubprocessError/TimeoutExpired; strip hai đầu; fullmatch hai nhánh 40 và 64 độc lập, độ dài −1/đúng/+1, chữ 0..9/a..f, hoa/ngoài bảng/Unicode ở đầu/giữa/cuối, nhiều token; None khi HEAD không hợp lệ; thay bytes giữ HEAD, thay HEAD giữ bytes, không git. Lỗi đọc nguồn không được biến thành vân tay xanh; argv/kwargs đo bằng spy, không gọi đó là đo thời hạn treo thật.

Đối chứng I/O nguồn riêng (`source_io.py`, `source-io.json`): nguồn vắng → FileNotFoundError; đường nguồn là thư mục → IsADirectoryError; read_bytes ném OSError → OSError đi ra. Cả ba không trả vân tay. Đây là kiểm hành vi fail-closed, không tính ngoại lệ thành một ca tự kiểm giết mutant.

Miền `main`/dispatcher: đọc cấu hình trước mọi ca, lỗi rc=2; hai tiền kiểm, từng CA/danh tính/thứ tự/một lần; AssertionError/exception/BoQua và mọi bộ đếm/stdout; mảnh k/N/ra/nhóm/workers; nền đỏ/tiền kiểm bỏ qua → dọn đúng tệp/không phóng con/rc=1; truyền đủ bốn đối số nhận; mọi nhóm/lỗi đầu/rc/đuôi 300 ký tự; bảy đối số bộ ghi ở nhánh sạch và dọn; mọi dòng bảng và mã 0/1 với 0/1/>1 lỗi; đủ/gate gọi cổng đúng GOC, tự kiểm phân hạng/giàn giáo/song song, tập nền sắp xếp, cộng lỗi nhiều nguồn/nhiều kết quả; gate không đo bán kính, đủ đo nguyên DOT_BIEN với đúng nền/workers; summary đầy đủ. Dispatcher không đối số × du/gate/mảnh × rc 0/1/2; --gop, argv[1], thiếu/thừa/lạ, thư mục trùng tên cửa, sys.exit. Nhóm rỗng không phát sinh với 387 tên và N≤16; tương đương phải tách khỏi survivor có nghĩa.

HƯỚNG 4 (MỚI): Tính đầy đủ của nguồn bytes — vượt fixture một dòng
  giả thuyết : fixture nguồn nhỏ/toàn chữ thường/ASCII không phân biệt băm đầu tệp hoặc chuẩn hoá nội dung.
  lệnh       : measure.py r15-mutations.json target; extent.py; đang chạy measure.py r15-mutations.json (56 ca/phép).
  output     : riêng t53 qua với source_prefix_4096, source_prefix_64, source_ascii_ignore, source_casefold; source_upper_digest bị giết. source_utf8_roundtrip qua, là đối chứng tương đương trên nguồn UTF-8 hợp lệ. Toàn bộ neo→thay ở r15-mutations.json.
  kết luận   : KHÔNG ĐO ĐƯỢC răng cả suite ở thời điểm ghi; ứng viên cùng lớp nguồn F34, chưa coi bước sàng lọc là finding đã xác nhận.

  cập nhật   : source_prefix_4096, source_prefix_64, source_ascii_ignore đã có đủ 56/56 `qua` (measure-source_*.json). extent.py đối chiếu trực tiếp SHA-256 độc lập: control không lệch ô nào; cắt 4096 lệch ở 4097/8193 bytes và tệp nguồn thật; cắt 64 lệch ngay 65 bytes; bỏ non-ASCII lệch fixture Unicode và tệp thật. Xác nhận **LỖI (P2), F36**, nối lớp F9/F30/F32/F34. Chưa thấy lỗi thuật toán nguồn trên head nguyên bản; lỗi nằm ở răng t53.

HƯỚNG 5 (MỚI): Gián đoạn ghi giữa chừng và lần ghi phục hồi
  giả thuyết : tệp mảnh bị ghi dở có thể được gom xanh hoặc làm lần ghi sau dùng lại dữ liệu hỏng.
  lệnh       : python evidence-luot-15/env.py python -u evidence-luot-15/recovery.py.
  output     : giả OSError sau khi ghi 0/1/100 bytes hoặc thiếu 2 bytes cuối ⇒ gom G-dau/G-ban-ghi, lỗi=1; mỗi lần ghi lại thành công ⇒ gom 8/8, 387 bản ghi, bytes khớp bản gốc. Thiếu đúng LF cuối nhưng JSON cuối nguyên vẹn ⇒ gom lỗi=0, dữ liệu đo vẫn đủ. Writer vẫn ném OSError; workflow không bỏ lỗi bước mảnh và không upload ở nhánh lỗi.
  kết luận   : KHÔNG PHẢI LỖI. Phép đầu của reviewer đòi mọi truncate đều đỏ đã sai ở ô chỉ thiếu LF cuối; recovery-first.log giữ nguyên AssertionError, runner sửa oracle rồi chạy lại toàn bộ. Không gán ô ấy thành “gom xanh trên bộ sai”. Phép này dùng bản ghi tổng hợp để kiểm giao thức, KHÔNG khai là đã đo bán kính 387 thật.

HƯỚNG 6: Hồi quy cấu trúc và công cụ
  giả thuyết : delta tạo lỗi registry, t152, các ca lease, actionlint hoặc Ruff F.
  lệnh       : run_regression.py; inventory.py; đối chiếu JSON Ruff head/base.
  output     : regression rc=0; head-registry rc=0; base-registry rc=0; t152 và t24/t31/t35/t161/t162 đều PASS hai phía; actionlint và probe rc=0 hai phía; Ruff 6/6 lỗi nền, added=[], removed=[]; baseline 212 mutant/53 ca, head 387 mutant/56 ca, không mất mutant cũ. Gate trọn vẫn đang chạy ở thời điểm ghi.
  kết luận   : KHÔNG PHẢI LỖI cho các phép đã xong; chưa coi gate đang chạy là ĐẠT.

HINT PATCH F36 — nguồn bytes đầy đủ, giữ răng riêng t53

Chỉ gợi ý cho executor; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không đổi thuật toán `_van_tay` hiện đang đúng. Sửa `_in_tu_kiem_che_do` và `t53` trong `ops/cong_cu_test.py`:

- Chốt chính ở **toàn tệp đang chạy**: trước khi tráo GOC/TEP_TEST sang fixture, child trả thêm `kq["sha_nguon"] = _van_tay()["sha256_test"]`. Parent so với `hashlib.sha256(Path(TEP_TEST).read_bytes()).hexdigest()` do parent tự tính. Khi đo đột biến, TEP_TEST của parent đã trỏ đúng tệp đột biến, nên vẫn so đúng bytes mà child đang chạy. Tệp thật dài, có chữ hoa/thường, space và Unicode; một chốt này giết cả họ cắt đầu/cuối và chuẩn hoá nguồn. Không để child trả boolean “tôi tự băm đúng”.
- Thêm bảng fixture nguồn bytes độc lập gồm: tệp rỗng; ngắn; chữ ASCII trộn hoa/thường; UTF-8 có dấu; các độ dài 63/64/65, 4095/4096/4097 và nhiều khối (8193 hoặc lớn hơn). Giữ fixture CR/LF đã có; không cần reviewer dựng byte điều khiển mới.
- Với từng fixture, child gọi `_van_tay` thật và trả digest thực, parent tính SHA-256 từ fixture chuẩn của chính parent, so **chuỗi digest đầy đủ**, không nhận boolean do child tự so. Có cặp cùng tiền tố 4096 bytes, chỉ khác một byte ở cuối; cặp cùng chữ khác hoa/thường; cặp khác phần non-ASCII. HEAD cố định, rồi kiểm đổi HEAD mà bytes giữ nguyên như ca hiện có. Nguồn test dài thật cũng có thể được băm một lần để đối chiếu, tránh băm toàn tệp trong mỗi ô Git.
- Neo `Path(TEP_TEST).read_bytes()` → `Path(TEP_TEST).read_bytes()[:64]`, `[:4096]`, `.decode("utf-8").encode("ascii", errors="ignore")`, `.lower()`; cả bốn phải bị **t53** giết, mọi ca khác qua. `source_upper_digest` là đối chứng đỏ sẵn; `source_utf8_roundtrip` là đối chứng tương đương với nguồn UTF-8 hợp lệ, không bắt buộc giết.
- Rủi ro bán kính: không thêm oracle digest vào t52 (producer/consumer đang dùng chung nguồn theo chủ đích), không móc t54 vào nguồn thật. Fixture nhỏ trong thư mục tạm, khôi phục GOC/TEP_TEST/subprocess bằng finally; lỗi gọi/đọc phải thành dữ liệu phân biệt, không cho tiến trình con chết rồi nhận `tin_dung_gia`. Chạy toàn bộ mutant đích t53 và mẫu cũ phụ thuộc TEP_TEST, bảo đảm bán kính 1/56.

  cập nhật miền F36: hai neo cùng nguồn → `Path(TEP_TEST).read_bytes()[-64:]` / `[-4096:]` cũng 56/56 qua. Thêm vào danh sách phải bị t53 giết; không chỉ kiểm tiền tố. Dữ liệu ở r15-extra-mutations.json; phép bỏ space cũng đang đo. Fixture bổ sung nên có space đầu/giữa/cuối; chốt toàn tệp phía trên là cách sửa cấu trúc để tránh tiếp tục vá từng ví dụ.

  cập nhật HƯỚNG 4: source_casefold cũng 56/56 `qua`; extent.json chứng minh băm sai fixture trộn hoa/thường, Unicode và tệp thật. Tổng F36 hiện 4 survivor có nghĩa, gộp một finding.

HƯỚNG 7: Miền phân hoạch, gom, CLI và bộ ghi
  giả thuyết : gom xanh với sai cấu trúc hoặc sai kết quả; producer/consumer tự che lỗi; CLI nén mất bảng/lỗi.
  lệnh       : partition_roundtrip.py; domain.py; novel_files.py; schema_io.py; schema_cli.py; gom_current_data.py; các runner wiring và matrix kế thừa.
  output     : round-trip N=2..16 đều phủ 387 tên, rời nhau, gom lỗi=0, bảng đúng thứ tự. Oracle danh tính ngoài hàm: control lệch 0/135, hai phép xoay/đảo nguồn lệch 135/135. Đảo tên tệp và thứ tự bản ghi vẫn gom đủ; hardlink trùng/FIFO/thư mục/tệp cắt dở/HEAD khác đều đỏ. Bộ đúng schema nhưng đích sống, đích bỏ qua, tín dụng giả, bán kính rộng, lỗi đo đều đỏ; ca lạ/đích sai bị chốt bản ghi bắt. CLI tên thư mục trùng cửa tự kiểm vẫn gọi gom; workflow bác thêm cờ sau thư mục gom.
  kết luận   : KHÔNG PHẢI LỖI ở hành vi head trong các ô trên. Kết luận răng trọn lớp chờ matrix 56 ca, không suy từ round-trip tự dùng cùng producer/consumer.

Miền artifact đã rà: thư mục vắng/rỗng; mọi mục tệp thường/symlink gãy hoặc lành/FIFO/thư mục/hardlink trùng; read/decode/JSON/prefix/khóa/kiểu; từng trường version/index/count/hash/HEAD; N đồng nhất/2..16, tập k đúng, đúng một tệp mỗi k; tổng và hợp của phân hoạch; chuyển/xóa/trùng tên; nhóm, rc=0, thân và nền rỗng truyền receiver; cấu trúc bản ghi, ca đích/trạng thái/lý do, kết quả không đo được hoặc sai bán kính; đủ từng dòng theo DOT_BIEN và tổng lỗi 0/1/>1; CLI arity/dispatch/vân tay/bảng/exit; writer dọn tệp thường/symlink/đường không có, lỗi con/HEAD/thiếu record/kết quả đầu-cuối, cộng mọi lỗi; header/body serialization; parent có sẵn/nhiều tầng, giữ nguyên path có space, lỗi trước và giữa ghi, phục hồi. Các nhánh dự phòng không thể tới dưới các chốt trước được phân biệt với chốt độc lập.

  cập nhật HƯỚNG 6: gate giao mảnh đã hoàn tất rc=0 sau 347,0s: `cong_cu_test: 56/56`, tiền kiểm bỏ qua=0, tự kiểm ĐẠT, cổng cây thật ĐẠT, lỗi đột biến=0. Đây không thay cho đo đủ 387 mutant; A1 tám mảnh đang chạy riêng.

  cập nhật F36: source_remove_spaces (`read_bytes()` → `read_bytes().replace(b" ", b"")`) cũng 56/56 qua, lệch digest ở fixture có space và nguồn thật. F36 gồm **7 phép có nghĩa**, không tính round-trip UTF-8. Hint phải giết thêm phép bỏ space này bằng chốt băm toàn tệp/fixture có space.

HƯỚNG 8: Kiểm độc lập lưới đầu vào và oracle mới
  giả thuyết : expected lấy từ cùng regex/thuật toán mutant hoặc chỉ kiểm rc nên che sai giá trị.
  lệnh       : domain.py; mode_domain.py; runtime-counts.json; đọc `_mong_che_do` / `_mong_git` cùng luồng child→parent.
  output     : lưới ngoài 10.816 cặp số nhận 135, từ chối 10.681, mismatch=[]; 11 grammar âm đều từ chối. domain.py: 258 cấu hình và 275 ô HEAD, CONTROL_PASS. Lưới t53 trong cây: 200 ô chế độ (gồm 27 ô hiện diện), 57 ô Git; expected của parent được viết bằng so ký tự, child in giá trị thật. Oracle phân hoạch của parent dùng range(k,L,N), không `_phan_manh`.
  kết luận   : KHÔNG PHẢI LỖI ở các oracle giá trị/HEAD/phân hoạch này. Lưới Git trong cây không phải tích Descartes đầy đủ rc×mọi stdout: các rc khác 0 dùng stdout hợp lệ; lưới ngoài 275 ô đã kiểm thêm tích này. Không đánh tráo số 57 thành 275, hoặc kiểm HEAD thành kiểm digest bytes (điểm hở F36).

  kiểm lại runner: domain.py cũ chỉ assert expected độc lập cho HEAD; phần mode của nó so với control. Đã bổ sung domain_check.py (oracle riêng của reviewer viết từ spec bằng tách '/', bảng chữ ASCII, kiểm độ dài/biên; không gọi `_doc_che_do` hay `_mong_che_do` để sinh expected). Kết quả chạy thật: `MODE_SPEC 458 PASS; HEAD_SPEC 275 PASS` — 258 cấu hình ngoài + 200 ô trong cây, so cả chế độ/tuple/path/thẻ lỗi; 275 ô HEAD dùng kiểm chiều dài/tập chữ, không regex sản phẩm. Vì vậy kết luận cho control không chỉ dựa vào nhãn CONTROL_PASS của runner kế thừa.

HƯỚNG 9 (MỚI): Đồng bộ đăng ký mutant với năng lực symlink
  giả thuyết : F35 thêm mutant symlink vô điều kiện, trong khi fixture vẫn chỉ chạy khi có năng lực; nền không symlink sẽ đỏ oan.
  lệnh       : capability-fixture.json đặt `_CO_SYMLINK=False` trên bản sao riêng /tmp/review668-r15-no-links; capability_radius.py chạy chính mutant chuẩn f35_writer_broken_link qua đủ 56 ca; control t52/t53/t54 trên cùng bản sao.
  output     : đọc mã thấy f35_writer_broken_link đăng ký vô điều kiện ở dòng 2214; f24_nhan_symlink có điều kiện ở 7375; fixture ghi_gay có điều kiện ở 7797. Đang chờ kết quả chạy để kết luận. Lần gọi control đầu vội trước khi copy xong gây ModuleNotFoundError của runner; giữ capability-control-setup-race.log, đã chờ chuẩn bị xong và chạy lại.
  kết luận   : KHÔNG ĐO ĐƯỢC ở thời điểm ghi. Đây là mô phỏng nhánh năng lực trên Linux, không khai là đã chạy Windows thật.

  cập nhật   : control: capability=false, 386 mutant, f24_registered=false, f35_registered=true; t52/t53/t54 đều `qua`. `capability-radius-f35_writer_broken_link.json`: 56/56 `qua`; `_ket_luan_ban_kinh` trả lỗi=1, “đích ... vẫn XANH ⇒ đột biến không giết được gì”. Xác nhận **LỖI (P2), F37**, nối lớp artifact F24/F35. F35 đã vá răng symlink trên nền có năng lực nhưng sinh lỗi đăng ký ở nhánh không có năng lực; không đủ bằng chứng để nâng thành P1 về runner Windows thật.

HINT PATCH F37 — đóng cả hai nhánh năng lực của lớp artifact

Chỉ gợi ý cho executor; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Trong `ops/cong_cu_test.py`, chuyển đăng ký `f35_writer_broken_link` khỏi vòng tuple vô điều kiện (dòng 2214) vào cùng khối `if _CO_SYMLINK` với `f24_nhan_symlink` (dòng 7375), hoặc dùng một bảng đăng ký symlink chung chỉ được nạp ở đó. Giữ `_ket_thuc_manh` và `_gom_manh` nguyên trạng.

- Capability=true: cả f24/f35 được đăng ký, cả fixture symlink gom và ghi đều chạy, hai mutant bị t52 giết đúng 1/56; target symlink không bị sửa và broken-link được gỡ.
- Capability=false: cả hai mutant vắng; fixture tương ứng vắng có chủ đích; t52/t53/t54 qua; không còn mutant đã đăng ký mà không có đường đo. Tổng DOT_BIEN và phân hoạch phải tự tính, không ghim 387/385 vào assertions hoặc artifact.
- Probe năng lực: thành công ⇒ true; OSError/NotImplementedError/AttributeError ⇒ false. Việc hạ năng lực cần áp nhất quán cả parent lẫn child; chỉ gán cờ trong parent sẽ không kiểm được chương trình con và có thể tạo lỗi giả.
- Chốt metadata trong t52/giàn giáo: child trả capability và danh sách hai mutant symlink thực sự có; parent kiểm quan hệ “đúng hai khi có / không có khi vắng”. Đột biến cần giết: bỏ điều kiện đăng ký (nhánh false vẫn có f35), đảo điều kiện, bỏ từng đăng ký khi capability=true. Fixture phải đi qua cửa subprocess dùng TEP_TEST như các ca hiện có; không nhận thông báo tự khai thay cho registry thực.
- Rủi ro bán kính: giữ oracle này trong t52, không thêm vào t53/t54; kiểm cả hai điều kiện capability bằng cây riêng. Không sửa os.symlink toàn cục trong suite đầy đủ để rồi làm các ca cũ chết oan; tách phép kiểm probe có stub và khôi phục trong finally. Việc chuyển vị trí mutant có thể đổi phân hoạch theo thứ tự DOT_BIEN: cần đo lại 8 mảnh/gom cùng source mới, không tái dùng artifact của SHA này.

  đối chứng F37: cùng mô phỏng `_CO_SYMLINK=False` với nguồn `cong_cu_test.py` từ head lượt 14 (`9440dc1`): 351 mutant, f24=false/f35=false, t52/t53/t54 đều qua. Probe `_do_co_symlink` thật với stub riêng: success=true; OSError/NotImplementedError/AttributeError=false. Chi tiết capability-before.json, capability-control.json, capability-probe.json; không phải suy luận từ riêng một dòng diff.

HƯỚNG 10: Nhiễu t5 và tính trung thực của báo cáo bán kính
  giả thuyết : chết thêm t5 dưới một phép đổi gom là hồi quy do packet.
  lệnh       : đọc new-header_accept_symlink.json; measure.py r15-retry-mutations.json; recheck_noise.py.
  output     : lần đầu t52 giết đúng chốt G-tep, thêm t5 “cai_cong_cu.sh thất bại: rc=141”; đang chạy lại đủ 56 ca và 8 control t5 mỗi phía head/baseline. Giữ nguyên file thô, không ghi đè bằng retry.
  kết luận   : KHÔNG ĐO ĐƯỢC nguyên nhân ở thời điểm ghi; chưa gọi là hồi quy sản phẩm, cũng chưa khai mọi phép ngay lần đầu đều 1/56.

  cập nhật   : retry đủ 56 ca chỉ t52 `giet_that`; 8/8 control t5 baseline và 8/8 head đều qua. `_t5` và `ops/cai_cong_cu.sh` không thuộc phần hành vi đổi của packet. Không xác định dứt điểm nguyên nhân rc=141; không dùng nó như P1 của #668. Raw new-header_accept_symlink.json và retry measure-header_accept_symlink_retry.json cùng được giữ; bảng ma trận thô vẫn thể hiện hai ca chết ở lần đầu.

HƯỚNG 11: Chốt toàn ma trận kế thừa trên exact head
  giả thuyết : đóng lớp từ một vài ca đích mà chưa chạy đủ checklist sẽ bỏ sót survivor khác.
  lệnh       : run_checklists.py; fields_full.py; novel_entry.py; partition_identity.py; measure.py prior-mutations.json / r15-mutations.json / r15-extra-mutations.json; summarize.py.
  output     : 263/263 phép, mỗi phép đủ tập 56 ca. Gồm 138 checklist lượt 5–10, 17 trường main + 3 entry + 2 phân hoạch lượt 11, 7 lượt 12, 4 lượt 13, 83 lượt 14, 9 phép nguồn bytes lượt này. Raw: 226 chỉ đúng ca đích giet_that; 18 ngoài mẫu đó (17 phép thăm dò cố ý gây chết rộng/giàn giáo, 1 nhiễu t5 đã retry); 19 survivor. Sau retry đã khai: 227 đúng đích, 17 ngoài mẫu, 19 survivor.
  kết luận   : LỖI (P2) ở 7 survivor nguồn F36; 12 survivor còn lại là tương đương hoặc fail-closed dưới hợp đồng đã có, nêu đầy đủ dưới đây. Main/dispatcher và chế độ không có survivor có nghĩa mới; các biểu hiện F33/F34/F35 cũ bị bắt. F37 là phép riêng trên nhánh capability=false, không trộn vào 263 phép trên nền thật capability=true.

12 survivor không dùng làm finding: receiver_baseline chỉ thêm tên ngoài CA; break_on_error không bỏ đo vì `_phong_con` đã chạy/đợi hết con và kết quả toàn mảnh vẫn đỏ/không file; final_hong được lỗi nền bảo vệ; final_gate_eq_one đúng miền mã 0/1 của cổng; main_no_sorted_baseline được helper sắp xếp; writer_drop_missing vẫn KeyError/không file và receiver bảo đảm tập tên trước writer; main_receiver_baseline_hong luôn nhận hong rỗng sau chốt nền; main_empty_launch_guard/main_receive_false không đổi hành vi vì không có nhóm rỗng trong miền 387 tên, N≤16, worker kẹp theo tên; gom_drop_decodeerror vẫn bắt UnicodeDecodeError qua ValueError; writer_record_order được giao thức nhận thứ tự dòng bất kỳ; source_utf8_roundtrip giữ nguyên bytes nguồn UTF-8 hợp lệ. Đã chạy lại survivor_equivalence.py: missing-record control lỗi=1/không file, mutant KeyError/không file; baseline_report_sort_equal=True. Hai phép xoay/đảo phân hoạch KHÔNG được coi tương đương: chúng nay bị t52 giết.

HƯỚNG 12: Bán kính native — giữ kết quả hoàn tất tách khỏi tiến trình đang chạy
  giả thuyết : các phép reviewer đủ 56 ca nhưng registry chuẩn có hồi quy bán kính hoặc giết thêm t52/t53/t54.
  lệnh       : run_a1.py (8 mảnh thật rồi gom); sample_run.py (165/387 có chủ đích, mỗi mutant lưu riêng); retry_base.py t6_day_g5_sau_py_compile / t21_git_regex_cat_hau_to.
  output     : A1 đang chạy, chưa có artifact hoàn tất ở lúc ghi này. Mẫu dự phòng 165 gồm 41 cũ, toàn bộ 56 mutant đích t52 + 43 đích t53 và 25 đại diện t54; kết quả sẽ chốt theo file radius-*.json đã hoàn tất, không theo tên đã lên lịch. Baseline t6/t21 đều đúng 1/53; sẽ đối chiếu tập bỏ qua với head.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận cuối cho native ở thời điểm ghi; kết quả được cập nhật bên dưới khi runner xong.

  đối chứng bỏ qua: t6 có 6 ca `bo_qua`, t21 có 5; tập danh tính trên head trùng hoàn toàn với baseline, cả hai có bán kính đúng 1/56 (baseline 1/53). baseline-skip-comparison.json giữ lý do từng ca. Đây là giới hạn fixture cũ, không phải các ca mới t52/t53/t54 bị giết thêm; không ghi 11 trạng thái ấy thành `qua`.

  cập nhật 09:18Z: bốn mảnh k=0..3 đã hoàn tất rc=0 (3800,04–3858,92 giây), có 195 bản ghi native thật; `_ket_luan_ban_ghi` kiểm lại đều lỗi=0, gồm 108 mutant cũ, không mutant cũ nào giết thêm t52/t53/t54. Mẫu riêng hoàn tất 47/165, gồm đủ 41 mutant cũ đã chọn, lỗi=0. Chưa chạy được gom đủ tám mảnh; không dùng thời gian container đang chạy nhiều phép đo để suy A9 trên GitHub runner.

  đối chứng bổ sung: bốn mutant cũ `bn_import_ro_ri_qua_pham_vi`, `bn_ten_bi_che_khong_chan`, `bn_khong_giai_callee`, `bn_quet_theo_chuoi` ở các mảnh thật có tổng 5 trạng thái bỏ qua phụ thuộc cơ chế phân tích đang bị đột biến. Đã đo lại cả bốn trên baseline: bán kính đúng 1/53, tập danh tính bỏ qua trùng head. Cộng t6/t21 thành **16 trạng thái bỏ qua trên 6 mutant**, được lưu ở [native-baseline-skips.json](evidence-luot-15/native-baseline-skips.json). Không cộng lặp một mutant xuất hiện ở cả mảnh thật và mẫu riêng.

  CHỐT 09:41:37Z: sample_run.py hoàn tất rc=0, **165/165**, gồm 41 cũ + toàn bộ 56 đích t52 + toàn bộ 43 đích t53 + 25 đích t54. Cả 11 F33, 12 F34, 12 F35 đều đúng ca đích `giet_that`, đúng 1/56; riêng hai sửa cuối chống tín dụng giả cũng đạt trong vòng đầy đủ. Sample có 165 `giet_that`, 9064 `qua`, 11 `bo_qua`, không `tin_dung_gia`, không lỗi kết luận bán kính.

  Gộp sample với 195 mutant trong bốn mảnh thật và loại tên trùng: **275/387 mutant chuẩn khác nhau**, từng mutant đủ 56 trạng thái, tất cả bán kính đúng; 127 mutant cũ và 148 mutant mới (t52=56, t53=43, t54=49). 85 mutant được đo lặp giữa hai đường có tập trạng thái phân hạng giống nhau. Tổng 15.400 trạng thái = 275 `giet_that` + 15.109 `qua` + 16 `bo_qua`; không mutant cũ nào giết thêm t52/t53/t54. Xem [native-summary.json](evidence-luot-15/native-summary.json), [actual-radius.json](evidence-luot-15/actual-radius.json), `sample/radius-*.json` và bốn artifact thật ở `native-shards/`.

  kết luận cuối HƯỚNG 12: KHÔNG PHẢI LỖI trên mẫu lớn có chủ đích được chỉ thị cho phép. **Không khai đã đo đủ 387 hoặc đã gom đủ 8/8**: k=4..7 còn chạy khi chốt; chưa có kết quả A1 gom cuối. Log có thể tiếp tục tăng sau mốc này, không tự động thay đổi verdict. Không dùng kết quả executor đang chạy hoặc kết quả lượt cũ để bù phần chưa hoàn tất.

## Kết luận theo lớp

“Đóng” dưới đây nghĩa là không còn phản chứng có nghĩa trong miền nhánh/ngữ pháp/tham số đã liệt kê và đo ở lượt này; không phải chứng minh mọi chương trình đột biến tùy ý. Kết quả từng phép nằm trong [mutation-matrix.md](evidence-luot-15/mutation-matrix.md); bảng dữ liệu và lý do đầy đủ ở [review-summary.json](evidence-luot-15/review-summary.json).

| Lớp | Miền đã đo | Trạng thái |
|---|---|---|
| Workflow | F1/F3/F10/F14: 60 phản chứng sẵn có; bỏ từng guard và tổ hợp guard; shape job/needs/if/matrix/env/run/shell, câu lệnh và nội suy; registry toàn bộ | **Đóng** trong miền này; biến thể U+200B chỉ mô tả, chưa chạy |
| main/dispatcher | Toàn danh mục HƯỚNG 3: ba chế độ, mọi tiền kiểm/CA/ngoại lệ/bỏ qua, tham số và danh tính gọi, worker/nhóm/nền, cộng lỗi và stdout, dọn/ghi, CLI và mã thoát; checklist kế thừa đầy đủ, không chỉ ca đích | **Đóng**; 12 survivor tương đương/fail-closed được giải thích, không giấu khỏi bảng |
| Đọc chế độ | 27 ô hiện diện/rỗng/đúng; mọi thành phần regex hai toán hạng; 10.816 cặp số, 135 cặp hợp lệ; biên/Unicode/khoảng trắng; path nguyên văn; oracle độc lập 458 ô | **Đóng**; F29/F31/F33 đã vá thật |
| Nguồn vân tay | Git argv/kwargs, rc/exception, strip, hai grammar HEAD 40/64, 275 ô; bytes rỗng/ngắn/nhiều khối/nguồn thật/hoa/thường/Unicode/space, thay HEAD và bytes độc lập | **Chưa đóng — F36**: 7 phép làm digest sai vẫn qua 56/56; grammar HEAD đã đóng |
| Phân hoạch/gom/CLI/bộ ghi và registry theo năng lực | Miền HƯỚNG 7; mọi N=2..16, danh tính phân hoạch, sai cấu trúc và sai kết quả, kiểu/đường dẫn/tệp đặc biệt, bảng/exit, dọn/ghi/khôi phục, hai nhánh symlink | **Chưa đóng — F37**: hành vi và các biểu hiện F35 trên Linux có symlink đã đạt; registry khi không có symlink chưa đồng bộ |
| Hồi quy | Gate trọn giao bán kính; registry hai phía; t152 và năm ca lease; actionlint; Ruff F; 275/387 native, gồm đủ 99 t52/t53, 49 t54 và 127 cũ | Không thấy hồi quy trong miền đã đo; 112 native còn lại và A1 gom đủ tám mảnh chưa được xác nhận |

## Finding và gợi ý vá theo lớp

| Finding | Lớp | Mức | Tệp:dòng | Mô tả | Phản chứng |
|---|---|---|---|---|---|
| F36 | Nguồn vân tay / tự kiểm t53 | P2 | `ops/cong_cu_test.py:6813`, `:7973`, fixture `:8010`; hàm được kiểm `:7414` | Fixture bytes quá nhỏ và đồng dạng; chốt tự kiểm không bảo vệ việc băm toàn bộ bytes nguồn. Thuật toán hiện tại đúng. | 7 survivor `source_prefix_64/4096`, `source_suffix_64/4096`, `source_ascii_ignore`, `source_casefold`, `source_remove_spaces`: từng phép 56/56 qua, nhưng digest nguồn thật sai theo oracle độc lập; [extent.json](evidence-luot-15/extent.json) và hai JSON r15 |
| F37 | Artifact / đăng ký đột biến theo năng lực | P2 | `ops/cong_cu_test.py:2214`, `:7375`, `:7797` | `f35_writer_broken_link` đăng ký vô điều kiện trong khi fixture chỉ chạy khi `_CO_SYMLINK`; nhánh không có năng lực nhận mutant không thể bị giết. | Capability=false: control t52/t53/t54 qua; mutant chuẩn f35 sống 56/56, kết luận bán kính lỗi=1; đối chứng lượt 14 không đăng ký mutant này. [capability-radius-f35_writer_broken_link.json](evidence-luot-15/capability-radius-f35_writer_broken_link.json) |

**HINT PATCH F36 (toàn lớp; chi tiết và rủi ro đã ghi ở khối cùng tên phía trên).** Sửa giàn giáo `_in_tu_kiem_che_do` và parent t53, không sửa thuật toán `_van_tay`: child trả digest nguồn thực trước khi tráo fixture; parent tự tính SHA-256 từ chính TEP_TEST đang đo và so chuỗi đầy đủ. Bổ sung rỗng, nhiều khối, 63/64/65 và 4095/4096/4097/8193 bytes, cặp cùng tiền tố/khác hậu tố và cùng hậu tố/khác tiền tố, hoa/thường, non-ASCII, space đầu/giữa/cuối; giữ ca CR/LF sẵn có, thay HEAD độc lập và đường lỗi đọc. Bảy neo→thay chính xác ở [r15-mutations.json](evidence-luot-15/r15-mutations.json) và [r15-extra-mutations.json](evidence-luot-15/r15-extra-mutations.json), đều phải bị t53 giết đúng 1/56. Riêng `source_upper_digest` đã bị giết; `source_utf8_roundtrip` tương đương trên nguồn hợp lệ nên không đòi giết. Không thêm oracle độc lập vào t52/t54; khôi phục globals bằng finally, trả ngoại lệ có chủ đích thành dữ liệu để tránh tín dụng giả. Giữ fixture tráo TEP_TEST để vẫn bắt sai nguồn; chốt toàn tệp đơn độc không thay được fixture này.

**HINT PATCH F37 (toàn lớp; chi tiết và rủi ro đã ghi ở khối cùng tên phía trên).** Chuyển đăng ký f35 symlink vào cùng điều kiện năng lực với f24. Đo cả capability=true/false nhất quán parent và child: đúng hai mutant khi có, không mutant nào khi vắng; probe thành công/OSError/NotImplementedError/AttributeError; fixture tương ứng và target t52 đúng 1/56 khi có. Chốt metadata registry thực trong t52, thêm phép đảo điều kiện, bỏ điều kiện, bỏ từng đăng ký. Các neo cụ thể: `if _CO_SYMLINK:` của khối đăng ký → `if True:` hoặc `if not _CO_SYMLINK:`; từng phép gán `DOT_BIEN["f24_nhan_symlink"]` / `DOT_BIEN["f35_writer_broken_link"]` → bỏ đăng ký tương ứng. Đích mong đợi của từng phép là t52. Muốn đo nhánh false trên host có symlink, nhập bản sao với probe năng lực trả false trước khi registry được dựng; không chỉ gán cờ sau import. Không stub os.symlink suốt suite cũ; chỉ cô lập kiểm probe và khôi phục ngay. Không ghim số mutant; đo lại phân hoạch khi thứ tự registry đổi.

Cả hai hint chỉ là gợi ý: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không có patch sản phẩm nào được reviewer áp vào `cay-kho/`.

## Trạng thái F1–F35 (không có F4)

Bảng này phân biệt biểu hiện lịch sử đã vá với trạng thái toàn lớp hiện tại; không đổi nhãn cũ thành “đóng cả lớp” khi F36/F37 còn tồn tại.

| Finding cũ | Trạng thái tại head này | Căn cứ lượt 15 |
|---|---|---|
| F1 | Đóng | 20 phản chứng và bỏ guard thực thi |
| F2 | Đóng | Checklist main, danh tính/tham số/nhánh qua đủ 56 ca |
| F3 | Đóng | 28 phản chứng; splitlines kết hợp bỏ F10 bộc lộ 27 ca |
| F5 | Đóng | Checklist main kế thừa và phép đổi từng dây nối |
| F6 | Đóng | Main kế thừa, nhiều nhánh kết quả |
| F7 | Đóng | Checklist main đầy đủ, không chỉ 19 dây nối ban đầu |
| F8 | Đóng | Gom CLI thật, bảng và rc |
| F9 | **Chưa đóng cả lớp → F36** | Sai nguồn cũ bị bắt; băm thiếu/chuẩn hoá bytes vẫn sống |
| F10 | Đóng | 7 phản chứng nội suy; bỏ guard lọt 7/7 |
| F11 | Đóng | t152 hai phía, năm AL_VER và chú thích |
| F12 | Đóng | Danh tính CA, nhiều bán kính, stdout trong ma trận main |
| F13 | Đóng | __main__/--gop đi qua cửa CLI thật |
| F14 | Đóng | 5 phản chứng shell và phép bỏ chốt |
| F15 | Đóng | Lỗi 0/1/>1, tổng lỗi và stdout |
| F16 | Đóng biểu hiện cũ | Bộ đúng schema nhưng sai kết quả bị đỏ; lớp artifact còn F37 |
| F17 | Đóng | CLI nhiều lỗi, mã thoát và tổng |
| F18 | Đóng | N khác 8, nhiều dòng/nhiều nguồn lỗi, giá trị 1 |
| F19 | Đóng | So bảng gom nguyên văn, không chỉ số đếm |
| F20 | Đóng | CLI đảo bảng bị bắt |
| F21 | Đóng biểu hiện cũ | Bộ ghi/dọn/path/header/records; lớp còn F37 |
| F22 | Đóng trong môi trường đã đo | Gate và mẫu mutant cũ qua; không thêm chết t52/t53/t54 |
| F23 | Đóng | Nhiều ca bỏ qua, danh tính/lý do riêng |
| F24 | Đóng biểu hiện cũ; **lớp chưa đóng → F37** | Kiểu version/count và symlink gom bị bắt; F35 mới thiếu điều kiện registry |
| F25 | Đóng | Chọn cờ theo argv[1], thư mục trùng tên cửa |
| F26 | Đóng | Cửa CLI mặc định sys.exit(main()) có răng |
| F27 | Đóng | k=0, path khác x, worker khác, tự kiểm nhánh đủ |
| F28 | Đóng | CLI không đối số với cấu hình hợp lệ và hỏng |
| F29 | Đóng | 27 ô hiện diện/rỗng/đúng và toàn r12-mutations |
| F30 | Đóng biểu hiện cũ; **lớp nguồn chưa đóng → F36** | Hai chốt HEAD thật/không Git bị bắt |
| F31 | Đóng | Khoảng trắng giá trị gate, r13-mutations |
| F32 | Đóng | Hai grammar HEAD độc lập, độ dài/bảng chữ/vị trí |
| F33 | **Đã vá thật — đóng** | 11 phép sống lượt 14 nay bị t53 giết, lưới oracle độc lập |
| F34 | **Đã vá thật các biểu hiện cũ; lớp chưa đóng → F36** | 12 phép cũ bị bắt; thêm 7 survivor nguồn bytes |
| F35 | **Vá sinh lỗi mới → F37; lớp chưa đóng** | Các chốt cũ đã có răng trên nền có symlink; nhánh không có symlink còn mutant vô điều kiện |

## Chốt review

**0 P1 được xác nhận, 2 P2 (F36/F37), 0 P3. Yêu cầu sửa.** Workflow, main/dispatcher và đọc chế độ còn/đã đóng trong miền được liệt kê. Nguồn vân tay và artifact theo năng lực chưa đóng. Hai lớp mở đều có hint ở tầng tự kiểm/đăng ký, bộ ô cần thêm, neo→thay, ca đích và rủi ro bán kính; reviewer không áp hint vào sản phẩm.

Các hướng mới so với checklist trước: bảo toàn toàn bộ bytes nguồn (F36); ghi gián đoạn rồi phục hồi (không lỗi); registry theo năng lực symlink ở cả hai nhánh (F37). Phản chứng ký tự ẩn mới chỉ mô tả bằng lời đúng phân công; các F3/F10 đã chạy đều lấy nguyên fixture sẵn có.

Kết quả hồi quy hoàn tất: gate giao bán kính rc=0, 56/56, không tiền kiểm bỏ qua; registry head 1025/1025 và baseline 938/938; t152 cùng t24/t31/t35/t161/t162 đạt hai phía; actionlint/probe rc=0; Ruff F giữ nguyên sáu F841 nền, delta=0. Ma trận reviewer 263/263 hoàn tất; bảng raw giữ nhiễu t5 rc=141 và retry riêng, không tô lại lần đầu thành xanh.

Giới hạn: dùng phương án mẫu native lớn 275/387 được chỉ thị cho phép; chưa có A1 tám mảnh/gom cuối, chưa chạy native đủ ở cửa CLI mặc định (cửa ấy đã được đột biến qua giàn giáo), chưa đo Windows thật/Python 3.12/CI artifacts hoặc thời gian A9. F37 là phản chứng nhánh capability=false trên Linux, không phải lời khai đã chạy Windows. Không kích hoạt CI, không đăng/push/land và không dùng lời khai executor làm kết quả.

Kiểm cuối: `cay-kho/` sạch, HEAD vẫn `b3863e2af32cc8892144d9c573667a98701ab614`; nguồn `ops/cong_cu_test.py` trong cây và bản sao đo cùng SHA-256 `384a9f85a2ef730a2eddef09a899f52fed95f2c310ec9c249a2d977768b0b487`. [source-final-state.json](evidence-luot-15/source-final-state.json) giữ định danh cây/spec; [README evidence](evidence-luot-15/README.md) chỉ cách đọc và tái lập.

verdict: changes_requested
reviewed_sha: b3863e2af32cc8892144d9c573667a98701ab614
