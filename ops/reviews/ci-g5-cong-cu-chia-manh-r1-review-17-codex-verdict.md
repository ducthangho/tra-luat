# Cross-review độc lập packet #668 — lượt 17

verdict: changes_requested
reviewed_sha: 161c4b6ea1df3bb9749f039ad84ed9c4976b5942

Chỉ đo và viết verdict; không sửa mã trong `cay-kho/`. Đột biến trên bản sao `/tmp`. Không tự tạo payload chứa ký tự điều khiển/ẩn.

HƯỚNG 1: Neo nguồn và phạm vi
  giả thuyết : checkout hoặc SPEC khác nguồn yêu cầu.
  lệnh       : git -C cay-kho rev-parse HEAD; git status --short; sha256sum SPEC.md; inventory.py trên bản sao head/baseline.
  output     : HEAD 161c4b6ea1df3bb9749f039ad84ed9c4976b5942; status rỗng; SPEC dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; baseline 212 mutant/53 ca, head 403 mutant/56 ca, không mất tên cũ, thêm 191. Numstat 5 tệp +1948/-49.
  kết luận   : KHÔNG PHẢI LỖI. Trần ~1960 áp theo chỉ thị trực tiếp của chủ kho trong prompt. Đã đọc CLAUDE.md, protocol §8, SPEC và LEASE; chỉ đo tại chỗ, không CI từ xa.

Các runner và bảng đầu vào được chép vào `evidence-luot-17/`, đổi đường sang `/tmp/review668-r17`; không chép JSON/log kết quả cũ. Mọi kết luận dưới đây chỉ dùng lần chạy mới. Các phép đang chạy chưa được tính là đạt.

HƯỚNG 2 (MỚI): Tích chéo trạng thái gốc × thao tác × kết quả nạp
  giả thuyết : tám ô F38 đo các trục riêng, bỏ sót tổ hợp gốc vắng + nạp lỗi.
  lệnh       : `check.py new-probes.json`; `measure.py r17-mutations.json` (đủ 56 CA).
  output     : 48 lượt = 2 phiên bản × 2 trạng thái gốc × 6 thao tác × 2 đường nạp. Control khôi phục đúng 24/24. Đột biến `absent_error_restore` làm sai 7 ô khi gốc vắng (5 nạp FileNotFoundError, 2 callback RuntimeError), nhưng suite 56/56 qua, không ca nào giết.
  kết luận   : LỖI (P2), F39 — lớp artifact theo năng lực chưa đóng về răng kiểm thử. Đây không phải lỗi runtime của helper hiện tại, không phải đường gom xanh bỏ đo. Bằng chứng: `helper-state-product.json`, `measure-absent_error_restore.json` và neo/thay nguyên văn `r17-mutations.json`.

Miền mới đã đo: gốc có/vắng; callback giữ nguyên/xoá/gán callable ném OSError/NotImplementedError/AttributeError/tự ném RuntimeError sau thay trạng thái; module nạp thành công/đường không tồn tại. Quan sát cả dữ liệu trả và trạng thái thuộc tính thực, không chỉ tin cờ helper tự khai.

HƯỚNG 3 (MỚI): Lỗi IO xảy ra SAU khi đã ghi một phần artifact
  giả thuyết : lỗi ghi giữa chừng để lại mảnh cụt mà gom nhận xanh, hoặc giữ nguyên mảnh cũ.
  lệnh       : `check.py partial-probes.json`, chặn Path.write_bytes trên tệp dùng riêng rồi ghi tiền tố trước khi ném OSError.
  output     : 7 điểm cắt trên artifact 788032 byte: 0, 5, 182 (hết header), hết record đầu, nửa tệp, thiếu LF cuối, đủ tệp. Writer đều ném; không giữ STALE. Năm tiền tố thiếu dữ liệu đều bị G-dau/G-ban-ghi chặn. Hai tệp đủ nội dung (có/không LF cuối) gom xanh.
  kết luận   : KHÔNG PHẢI LỖI. Hai trường hợp xanh có đủ mọi bản ghi hợp lệ, không có kết quả nào bị bỏ đo; việc LF cuối không bắt buộc không làm mất dữ liệu. Writer vẫn thoát lỗi nên bước upload mặc định không chạy trong workflow. Không gọi các fixture dựng sẵn này là bán kính native đã đo.

HƯỚNG 4: Workflow và răng các chốt F1/F3/F10/F14
  giả thuyết : thay giàn giáo làm yếu validator hoặc các ca đã đăng ký không còn đo được chốt.
  lệnh       : `workflow.py`; `workflow_ablation_extra.py`; registry head/baseline; actionlint hai vế.
  output     : control chặn 20/20 F1, 28/28 F3, 7/7 F10, 5/5 F14. Gỡ chốt thực thi làm lọt 13 F1 và 7 F10; gỡ raw guard làm lọt 7 F10; splitlines riêng vẫn được raw guard bảo vệ, gỡ cả hai làm lọt 27 F3 + 7 F10; gỡ chốt shell làm lọt 5 F14. Registry head 1025/1025, baseline 938/938; actionlint rc=0 cả hai.
  kết luận   : KHÔNG PHẢI LỖI. Chỉ chạy payload đã có trong cây. Miền: job/step/workflow env và defaults; shell Bash tường minh; setup/checkout/Python; matrix os/k/N, needs/if/fail-fast; upload/download cùng OS; whitelist keys/lệnh, tách LF, raw nội suy/ký tự ngoài miền. Không dựng chuỗi ẩn mới.

HƯỚNG 5: Miền đầy đủ `_doc_che_do` và `_van_tay`
  giả thuyết : còn biên cùng lớp chưa được chốt giữa giá trị vắng/rỗng/có, grammar và nguồn bytes.
  lệnh       : `domain.py`; `domain_check.py`; `probe.py`; `mode_domain.py`; `extent.py`; `source_io.py`; ma trận r12/r13/r14/r14-extra/r14-artifact/r15/r15-extra qua measure.py (đang chạy, chưa chốt bán kính).
  output     : oracle độc lập MODE_SPEC 458 PASS; HEAD_SPEC 275 PASS. Chi tiết các lưới/ma trận còn lại bổ sung khi xong.
  kết luận   : Chưa chốt toàn lớp tại checkpoint này.

Miền `_doc_che_do` (liệt kê từ hàm, không suy từ tên finding):

- Ba biến BK/MH/RA: vắng, rỗng, có; đủ 27 phối hợp và thứ tự lỗi. MH vắng: RA hiện diện luôn C-ra-le; BK vắng trả du; BK đúng chuỗi `manh` trả gate, mọi giá trị khác C-ban-kinh. MH hiện diện: BK hiện diện C-ca-hai trước khi parse MH.
- Fullmatch grammar `(0|[1-9][0-9]?)/([1-9][0-9]?)`: nhánh riêng k=0; chữ số ASCII đầu 1–9; chữ số ASCII đuôi 0–9 có/không; đúng một slash; không dấu/số 0 dẫn đầu/thập phân/space/tiền tố/hậu tố/Unicode digit; nhóm 1 là k, nhóm 2 là N. So sánh N>=2, N<=16, k<N; RA vắng/rỗng lỗi, còn chuỗi path phải được giữ nguyên. Trả chính xác tên chế độ và tuple, không trim/casefold.

Miền `_van_tay`:

- Git argv đúng `git -C str(GOC) rev-parse HEAD`; capture_output=True, text=True, timeout=60. rc=0 so với rc âm/1/2/khác; stdout không được dùng khi rc khác 0. OSError, SubprocessError và TimeoutExpired đều về head=None.
- Strip hai đầu; fullmatch hai nhánh độc lập lowercase ASCII hex độ dài đúng 40 hoặc 64; từng miền chữ 0–9/a–f, uppercase và g trở lên, độ dài sát biên/trung gian, tiền tố/hậu tố, ký tự không ASCII. Không đổi match thành search/match, không nới lượng từ hoặc chỉ giữ một nhánh.
- sha256 của toàn bộ bytes TEP_TEST thật; không lấy SCRIPT, file khác hay chuỗi rỗng; không đổi algorithm/hex/case/nguồn root; không cắt đầu/đuôi/chuẩn hoá newline/case/space/Unicode. Nguồn không có, là thư mục hoặc lỗi đọc phải thất bại, không sinh digest thay thế. HEAD và digest thay độc lập; chốt gom so cả hai.

HƯỚNG 6: Gate và các cổng hồi quy hai vế
  giả thuyết : bản vá t52 làm gate đỏ hoặc thay kết quả các cổng ngoài packet.
  lệnh       : `run_regression.py`, đối chiếu JSON ruff theo filename/code/message.
  output     : gate rc=0; ca=56, đột biến=403 (giao mảnh), lỗi đột biến=0, tiền kiểm bỏ qua=0, cổng cây thật=ĐẠT; tự kiểm song song ĐẠT. t152 và lease t24/t31/t35/t161/t162 hai vế rc=0; probe hai vế rc=0; ruff F 6→6, delta thêm/bớt đều rỗng.
  kết luận   : KHÔNG PHẢI LỖI. Gate giao mảnh không được dùng thay kết quả bán kính native. Linux/Python 3.11; chưa đo Windows/Python 3.12 thật.

HƯỚNG 7: Đối chứng F38 gốc trên hai head
  giả thuyết : F38 chỉ được né bằng giàn giáo giả năng lực.
  lệnh       : `check.py before-after-probes.json` — bản sao nguồn `54b4a01` và `161c4b6`, cùng bootstrap xoá thuộc tính trước khi module nạp.
  output     : prior capability=false, count=394, t52=tin_dung_gia, AttributeError tại phép đọc trực tiếp os.symlink; head capability=false, count=399, t52=qua. Nền có symlink: cả năm mutant f38 đều làm đúng ca t52 giet_that trong phép đo ca đích.
  kết luận   : KHÔNG PHẢI LỖI gốc — **F38 ĐÃ VÁ THẬT**. Không suy từ kết quả t52 đơn lẻ rằng bán kính của mutant trên nền thiếu thuộc tính cũng đúng; phép ấy chạy riêng ở hướng sau.

HINT PATCH F39 (checkpoint, sẽ bổ sung nếu miền năng lực có biểu hiện khác)

Tệp/hàm: `ops/cong_cu_test.py::_in_tu_kiem_gom`, `t52`, `_nap_lai_sl`; ưu tiên bổ sung oracle của giàn giáo, không sửa thuật toán gom/ghi đang đúng. Gợi ý chưa áp trên cây thật; executor tự áp, tự đo, tự chịu trách nhiệm commit.

- Thay việc chỉ liệt kê các trục riêng bằng ma trận trạng thái. Ít nhất hai trạng thái gốc (có/vắng) × đường nạp (thành công/FileNotFoundError/ngoại lệ nạp khác) và callback giữ/xoá/gán callable ném từng OSError/NotImplementedError/AttributeError. Đo thêm callback tự ném lỗi sau thay trạng thái, để ranh giới try/finally cũng có răng.
- Helper giữ sentinel/getattr và finally hiện tại. Hàm fixture gốc vắng nhận cả `cach` và `tep`, gọi chính `_nap_lai_sl(cach, tep)` khi thuộc tính đang vắng, khôi phục trạng thái ngoài cùng bằng finally. T52 đòi đúng trạng thái thực sau lời gọi, mã `NEM:<Loại>` riêng, registry tương ứng; không chỉ đếm số ô.
- Đột biến bắt buộc, đích t52: `if cu_sl is sl_vang:` → `if cu_sl is sl_vang and not str(kq[0]).startswith("NEM:"):`. Ô gốc vắng+nạp lỗi phải giết nó. Giữ đủ năm mutant F38 cũ; các phép di chuyển callback ra ngoài try và nén mọi ngoại lệ thành FileNotFoundError đang được đo toàn suite.
- Rủi ro bán kính: tráo/xoá thuộc tính trong tiến trình con t52, luôn khôi phục sau cả thành công và lỗi; t53/t54 không mang oracle khôi phục này. Không làm import thật của runner thất bại rồi ghi thành giet_that. Cần đo đủ 56 ca cho mutant mới và mẫu mutant cũ tráo TEP_TEST/GOC.

HƯỚNG 8: Danh mục quyết định của `main`/dispatcher và ma trận kế thừa
  giả thuyết : một đường dây/giá trị của main không còn được 56 ca kiểm soát.
  lệnh       : `run_checklists.py`; `fields_full.py`; `novel_entry.py`; `partition_identity.py`; `measure.py all-domain-mutations.json`.
  output     : checkpoint 57/263 phép đã có đủ 56 states; 17/17 trường main bổ sung đều chỉ t54 giet_that. Chưa dùng con số checkpoint để kết luận toàn ma trận.
  kết luận   : Chờ đủ ma trận; danh mục đo cố định bên dưới.

Trọn miền main/dispatcher rà từ thân hàm:

- Cấu hình: dùng os.environ, gọi `_doc_che_do` trước mọi ca; ValueError in nguyên lý do và rc=2, không chạy tiền kiểm. Mọi đường hợp lệ du/gate/mảnh qua cùng tiền kiểm.
- Tiền kiểm: batch rồi alias, giữ tất cả ca/lý do bỏ qua; không trộn mẫu số CA. CA đúng tập/thứ tự/đúng một lần, qua tăng một, BoQua giữ tên+lý do, AssertionError giữ tên+lý do, ngoại lệ khác giữ cả loại. In tất cả dòng với số đếm và mẫu số chính xác.
- Mảnh: dùng đúng k/N/RA, k=0 và k>0, N=2/3/8/16; `_phan_manh(k,n)` lấy đúng danh tính/thứ tự. Nền đỏ hoặc tiền kiểm bị bỏ qua: gọi writer dọn đúng path/nhóm/k/N/reason/vân tay, không phóng con, rc=1. Header nêu đúng k/N/số tên/tổng registry/workers.
- Phóng con: toàn nhóm tên, baseline rỗng sau chốt nền, đúng workers; nhận từng nhóm cùng rc và stdout nguyên vẹn; giữ lý do lỗi đầu tiên với rc và đuôi 300 ký tự, không ghi đè bởi nhóm lành/hỏng sau; hợp nhất đúng mọi giá trị record. Vòng đã phóng/đợi con đầy đủ; break sau lỗi vẫn đỏ/không file, được phân biệt với bỏ đo mà xanh.
- Kết mảnh: writer nhận k/N/RA/tên, toàn ket hoặc None khi có lỗi nhận, nguyên ly_con và vân tay mới. In mọi dòng; lỗi 0→0, 1 hoặc >1→1. Worker=1 và các giá trị khác; path khác `x`; nhiều nhóm/nhiều lỗi độc lập.
- Đủ/gate: cổng thật đúng GOC; in mọi dòng. Tự kiểm phân hạng, giàn giáo, song song đúng thứ tự và tham số; cộng lỗi thay vì ghi đè/lấy max. Nền đỏ sắp tên và truyền đúng tập, in đủ báo cáo. Gate không gọi bán kính, in giao mảnh. Đủ truyền toàn list(DOT_BIEN), nền đỏ và workers; đọc mọi kết quả/mọi dòng/cộng mọi lỗi. SỐ LIỆU đúng số ca/tổng mutant/dấu giao mảnh/lỗi/tiền kiểm/cổng; rc là OR của hong, loi_db, tiền kiểm, lỗi cổng (0/1/>1, nhiều nguồn).
- Dispatcher: argv[1] quyết định duy nhất; --gop gọi đúng hàm, arity đúng một thư mục, vân tay một lần, nguyên bảng/rc; đối số trông giống cờ không chiếm dispatch. Cửa không đối số gọi main và sys.exit giữ rc trên cả du/gate/mảnh hợp lệ và cấu hình lỗi. Cờ lạ rc=2. Cửa tự kiểm được gọi đúng tên, không bị giá trị thư mục chọn hộ.

HƯỚNG 9: Miền phân hoạch/gom/bộ ghi/CLI
  giả thuyết : gom xanh khi bộ sai hoặc writer/CLI làm mất một phần kết quả.
  lệnh       : các nhóm gom-semantic/cli-new/gom-extra/writer-extra/new/r14-artifact trong ma trận; domain.py, schema_io.py, partition_roundtrip.py, probe.py.
  output     : oracle phân hoạch control sai 0/135 ô k/N; xoay phân hoạch và đảo nguồn mỗi phép sai 135/135 ô. Các kết quả còn lại được bổ sung khi các runner kết thúc.
  kết luận   : Chưa chốt ở checkpoint này; miền đã đặt để đo gồm:

Thư mục vắng/rỗng/không phải thư mục; mọi mục phải là tệp thường, loại thư mục/symlink; header UTF-8/prefix/json/dict/đúng năm khoá, strict int (không bool/float/string/null/list/dict) ở version/k/N; version=1, cả head và digest bằng nguồn gom; head nguồn vắng; body ngoài BKCON/blank; N đồng nhất, biên 2..16, tập k đủ 0..N-1, đúng một tệp/k; phân hoạch phủ/rời/đúng danh tính và thứ tự từ registry; record đủ tên/đúng nhóm/đích/trạng thái/mọi ca; lỗi ngữ nghĩa đích sống/tín dụng giả/bán kính >1; tổng/bảng/danh tính/thứ tự/chi tiết/mã CLI 0/1/>1.

Writer: xoá tệp cũ/symlink sống và gãy; không sửa đích link; ket=None, HEAD=None, thiếu record, lỗi ở cuối và nhiều lỗi, nguyên bảng/đếm lỗi; chỉ ghi khi toàn bộ đạt; version/k/N/vân tay/body đúng, parent lồng nhau/có sẵn, nguyên path có space, IO/read/decode/unlink/write thất bại. Record thứ tự khác vẫn được giao thức nhận, bảng gom luôn theo DOT_BIEN. Phân hoạch/round-trip N=2..16 dùng record dựng sẵn, không thay bán kính thật.

HƯỚNG 10 (MỚI): Bán kính trên nền thật sự vắng thuộc tính, không ép cờ False
  giả thuyết : mutant F38 mới hợp lệ ở nền có symlink nhưng chết ngay lúc import trên nền vắng thuộc tính mà chính sản phẩm hỗ trợ.
  lệnh       : `check.py absent-native-probes.json`, PYTHONPATH trỏ sitecustomize chỉ xoá os.symlink; cha và mọi con cùng nhận môi trường đó. Chạy toàn bộ 61 mutant t52 còn đăng ký; bán kính đầy đủ bảy mutant F37/F38 chạy tiếp bằng `absent-radius-probes.json`.
  output     : capability=False, registry=399. Trong 61 ca đích: 60 giet_that, duy nhất `f38_probe_bo_attr` = tin_dung_gia. Traceback: module import gọi `_CO_SYMLINK = _do_co_symlink()`, phép bỏ AttributeError khỏi except làm os.symlink vắng ném ở dòng 7395, trước cửa --tu-kiem-gom. Bảy bán kính còn đang chạy tại checkpoint này.
  kết luận   : LỖI (P2), cùng **F39** — đăng ký theo năng lực chưa đóng. Ca t52 không mutant vẫn qua, nhưng mutant mới không được giết thật trên nhánh vắng thuộc tính mà helper chủ động hỗ trợ. Không suy rằng toàn gate trên nền vắng thuộc tính xanh; đang đối chiếu đủ baseline vì hai ca cũ t51/t46 cũng lỗi khi os.symlink bị xoá. Không khẳng định Windows/Ubuntu chuẩn thiếu thuộc tính; đây là môi trường mô phỏng có đối chứng, nằm đúng nhánh AttributeError mà `_do_co_symlink` chủ động hỗ trợ.

F39 còn hai biểu hiện giàn giáo (đã đo đủ 56 ca): `callback_outside_try` và `reload_error_constant` đều 56/56 qua. Lưới mở rộng 96 lượt (4 phiên bản × 24 ô): callback ngoài try khác control 4 ô; nén loại ngoại lệ khác control 4 ô; nhánh khôi phục vắng chỉ khi thành công khác control 7 ô. Helper hiện tại vẫn đúng 24/24 theo oracle độc lập về capability, registry, mã ngoại lệ và khôi phục; thiếu nằm ở khả năng kiểm thử những sai lệch đó. Xem `r17-extra-mutations.json`, `measure-callback_outside_try.json`, `measure-reload_error_constant.json`, `helper-state-expanded.json`.

HINT PATCH F39 — bổ sung phần đăng ký và miền ngoại lệ (cùng một lớp)

- `f38_probe_bo_attr` đang trong bảng đăng ký vô điều kiện quanh dòng 2240. Đưa nó vào nhánh có năng lực phù hợp, cùng quản lý tên và oracle registry của F37/F38. Phương án bảo thủ: chỉ đăng ký khi `_CO_SYMLINK=True`; thêm nó vào tập tên đăng ký có điều kiện `_TEN_SL` và cập nhật kỳ vọng có/vắng. Khi capability=False, không đưa phép làm module chết trước cửa đo vào DOT_BIEN. Không chỉ đổi `tin_dung_gia` thành `giet_that`.
- Đo lại đăng ký thật bằng import trên từng môi trường: tạo được link; callable ném OSError; NotImplementedError; AttributeError; thuộc tính vắng. Hai ô cuối đặc biệt phải đo chính mutant/cửa tiến trình con, không thay `_CO_SYMLINK=False` trên nguồn để giả lập: cách thay cờ né hẳn `_do_co_symlink` lúc import và che lỗi này.
- Ma trận khôi phục bổ sung ô vắng+nạp lỗi; thêm module nạp ném RuntimeError (khác FileNotFoundError) và callback tự ném sau thay trạng thái ở cả có/vắng. Các mutant cần giết thêm đúng t52: di chuyển `cach()` ra trước try; đổi `"NEM:" + type(ex).__name__` thành hằng `"NEM:FileNotFoundError"`; nhánh khôi phục có điều kiện theo thành công đã nêu. Neo/thay chạy được nằm nguyên văn trong hai JSON r17.
- Chốt registry: khi có năng lực đòi đủ từng tên, khi thiếu đòi vắng đúng nhóm có điều kiện; mutant gỡ từng đăng ký chỉ đăng ký trong miền mà phép gỡ thực sự thay đổi registry. Đo lại điều kiện luôn đúng/đảo, từng đăng ký bỏ, năm mutant F38; đo đủ 56 trạng thái trên cả nền có/vắng thuộc tính. Không thêm oracle này vào t53/t54; giữ cùng thuật toán gom/ghi.

HƯỚNG 11: Đối chiếu đủ 56 ca ở nền vắng thuộc tính
  giả thuyết : lỗi của môi trường mô phỏng bị quy nhầm cho F39.
  lệnh       : `check.py absent-baseline-probes.json`; `absent-radius-probes.json`; đối chiếu từng trạng thái và phân hạng lại với đúng tập đỏ ở nền, giữ nguyên raw evidence.
  output     : baseline 53 ca và head 56 ca cùng có đúng hai lỗi nền t51/t46 = NotImplementedError do pathlib không tạo được symlink; 54 ca còn lại của head qua, t52/t53/t54 đều qua. Sáu mutant f37_dk_luon_dung/f37_dk_dao/f38_doc_thang/f38_bo_nhanh_vang/f38_bo_khoi_phuc/f38_khoi_phuc_khi_thanh_cong chỉ thêm đúng t52 giet_that. Riêng f38_probe_bo_attr thêm 9 tin_dung_gia: t29/t31/t32/t45/t42/t39/t52/t53/t54; không có giet_that.
  kết luận   : LỖI (P2), củng cố cùng F39. Hai lỗi nền không được tính thành hồi quy packet, không được xóa khỏi dữ liệu để khai bán kính thô 1/56. Raw bảy phép đều giữ đủ 56 states; sau loại đúng hai ca đỏ sẵn, sáu phép đạt bán kính một trên miền đo được, còn f38_probe_bo_attr vẫn lỗi. `absent-baseline.json`, `absent-summary.json`, `absent-radius-<name>.json` ghi cả hai cách đọc.

HƯỚNG 12: Đóng phép liệt kê ngoại lệ và tham số nạp của helper
  giả thuyết : chỉ đo FileNotFoundError sẽ bỏ sót nhánh ngoại lệ khác/callback và đường loader.
  lệnh       : `check.py loading-probes.json`; oracle độc lập đối chiếu từng ô, ghi `loading-summary.json`.
  output     : 336 lượt = 4 phiên bản × 84 ô. Hai trạng thái gốc × sáu callback × bảy đầu vào nạp: TEP_TEST mặc định, tệp thiếu, module ném RuntimeError, SyntaxError, không loader, đường là thư mục, chuỗi rỗng dùng default. Control đúng capability/registry/NEM/khôi phục 84/84. Ba mutant sống trong suite làm lệch oracle lần lượt 32, 14, 54 ô.
  kết luận   : LỖI (P2) về giàn giáo, cùng F39; không thêm finding rời cho từng kiểu ngoại lệ. Helper sản phẩm hiện tại đúng trong toàn miền này. HINT F39 cần dùng nhóm ô theo ngữ nghĩa lỗi nạp/callback và trạng thái gốc, không chỉ thêm một ô FileNotFoundError khi gốc vắng.

HƯỚNG 13: Một kết quả t5 rc=141 và phép đối chứng riêng
  giả thuyết : đột biến grammar HEAD gây hồi quy ngoài t53.
  lệnh       : giữ `measure-head_40_ascii_extra.json`; chạy lại nguyên phép qua 56 ca trong `retry/`; `recheck_noise.py` 40 lần/head và 40 lần/baseline; `noise_sources.py` so nguồn.
  output     : lần đầu t53 giet_that đúng, thêm t5 giet_that với cai_cong_cu.sh rc=141/đầu ra rỗng. Lần lặp đủ 56 ca chỉ t53 giet_that; t5 qua. 80/80 lượt t5 trực tiếp qua. Thân t5 cùng AST; cai_cong_cu.sh, cai_actionlint.sh, cong_cu.py, bash_nen.py, lease_publish_test.py cùng bytes baseline.
  kết luận   : KHÔNG ĐO ĐƯỢC nguyên nhân của rc=141 lẻ. Không quy nó thành hồi quy packet khi chỉ thay TEP_TEST::_van_tay, không sửa hoặc dùng TEP_TEST trong t5. Không xóa kết quả đầu, không khai toàn ma trận chỉ có đúng một ca chết cho phép này. Gate thật đã đạt; kết quả thô và lần lặp được bàn giao riêng.

HƯỚNG 14: Trọn miền năng lực callable, ngoài trường hợp thuộc tính vắng
  giả thuyết : F39 chỉ là tạo tác của phép xoá thuộc tính, không xuất hiện ở nhánh callable ném lỗi mà hàm probe hỗ trợ.
  lệnh       : `check.py capability-matrix-probes.json`; sitecustomize gán callable ném từng OSError/NotImplementedError/AttributeError ở cả cha và con. Mỗi môi trường chạy ba ca nền t52/t53/t54 và cả năm mutant F38 qua ca đích.
  output     : cả chín ca nền qua. OSError: 5/5 giet_that; NotImplementedError: 5/5 giet_that; AttributeError: 4 giet_that + f38_probe_bo_attr tin_dung_gia. Nền có symlink đã đo 5/5 ca đích giet_that; nền thuộc tính vắng đã đo toàn 61 đích t52 và bảy bán kính như HƯỚNG 10–11.
  kết luận   : LỖI (P2), cùng F39. Toàn miền probe đã đo: thành công, từng loại ngoại lệ trong except, thuộc tính vắng; lỗi đăng ký xuất hiện ở cả callable ném AttributeError lẫn thuộc tính vắng. `_TEN_SL` hiện chỉ liệt kê bốn tên cũ và bỏ sót mutant f38 mới cần điều kiện, nên bảng metadata tám ô của t52 vẫn xanh dù mutant này không đo được. Không mở finding thứ hai cho cùng lớp.

HƯỚNG 15: Biến thể workflow mới — chỉ mô tả bằng lời theo phân công
  giả thuyết : nội suy từ output thay vì hằng fromJSON trong các ca F10 có thể lọt qua bước bỏ chú thích.
  lệnh       : không soạn/chạy payload mới; đọc predicate raw và đối chiếu phép tháo chốt đã chạy ở HƯỚNG 4.
  output     : mô tả để executor dựng ca: trong chú thích trước lệnh gom, đặt biểu thức GitHub dùng format/output của bước trước để sinh ký tự LF U+000A rồi một lệnh thoát thành công. Nếu GitHub nội suy trước, Bash sẽ thấy dòng lệnh mới và có thể thoát trước phép gom. Validator hiện đọc thân run nguyên văn, thấy dấu mở biểu thức GitHub và từ chối trước khi bỏ chú thích; nguồn của giá trị (hằng/output) không thay predicate này.
  kết luận   : KHÔNG PHẢI LỖI theo cấu trúc guard đã đo; biến thể mới chưa có fixture chạy riêng. Không lấy mô tả này làm số ca đã chạy hoặc tạo thêm payload ký tự ẩn. Executor có thể thêm nó làm ca giữ ranh giới giữa nội suy và phân tích Bash.

HƯỚNG 16: Chốt toàn miền đọc chế độ và nguồn vân tay
  giả thuyết : các lưới ngoài đúng nhưng còn chốt không có răng trong suite.
  lệnh       : `measure.py all-domain-mutations.json` hoàn tất; domain_check.py, probe.py, mode_domain.py, extent.py, source_io.py; phân loại từng kết quả 56 ca bằng summarize.py.
  output     : đủ 103/103 phép miền từ r12/r13/r14/r14-extra/r14-artifact/r15/r15-extra. 458 ô chế độ + 10.816 cặp số (135 nhận/10.681 từ chối) + 11 grammar âm, không lệch oracle. 27 ô phối hợp và lưới rc×stdout đã chạy lại; HEAD 275 ô đúng. Bytes nguồn: 13 fixture độc lập × 10 phiên bản = 130 lượt, cùng fixture trong cây và nguồn TEP_TEST thật. Nguồn vắng/thư mục/lỗi đọc đều ném, không tạo digest giả.
  kết luận   : KHÔNG PHẢI LỖI mới; lớp đọc chế độ và nguồn vân tay **đóng trong miền đã liệt kê ở HƯỚNG 5**. Sáu survivor thuộc tập 103 đã kiểm ngữ nghĩa: baseline nhận luôn rỗng sau chốt nền; nhóm không rỗng/worker kẹp; UnicodeDecodeError vẫn thuộc ValueError; thứ tự record được phép; UTF-8 round-trip giữ bytes của nguồn hợp lệ. Không gọi các phép reviewer làm nhiều ca đỏ hoặc hỏng giàn giáo là mutant chuẩn bán kính 1; trạng thái thô nằm trong ma trận. Bất thường t5 riêng giữ ở HƯỚNG 13.

HƯỚNG 17: Chốt toàn bộ checklist kế thừa — đủ 263 phép × 56 ca
  giả thuyết : ca đích đúng nhưng mutant còn sống cả suite, hoặc chưa chạy đủ các bảng được yêu cầu.
  lệnh       : run_checklists.py (138 phép); fields_full.py/novel_entry.py/partition_identity.py (22 phép); measure.py all-domain-mutations.json (103 phép); summarize.py kiểm đúng tập 56 tên CA cho từng JSON.
  output     : MATRIX 263; MISSING 0. 233 phép chỉ ca đích giet_that; 18 phép ngoài mẫu một ca; 12 survivor. Ba phép r17 mới chạy riêng, đều 56/56 qua và thuộc F39. Không dùng kết quả ca đích đơn lẻ hoặc log lượt cũ để điền ô nào.
  kết luận   : KHÔNG PHẢI LỖI mới trong checklist kế thừa. **main/dispatcher vẫn đóng**; gom/CLI/bộ ghi theo miền HƯỚNG 9 vẫn đóng; riêng năng lực/giàn giáo của artifact chưa đóng vì F39. Danh mục đầy đủ và link từng kết quả: `evidence-luot-17/mutation-matrix.md`; số tổng: `review-summary.json`.

12 survivor được giữ nguyên trong bảng, không loại khỏi mẫu: `receiver_baseline` chỉ thêm tên ngoài CA; `break_on_error` không bỏ việc phóng/đợi con và mảnh vẫn đỏ/không file; `final_hong` vẫn bị loi_nen kéo đỏ; `final_gate_eq_one` tương đương trên miền 0/1 của `_cong_tren_cay_that`; `main_no_sorted_baseline` vẫn được helper sắp; `writer_drop_missing` vẫn KeyError/không file, còn caller thật đã đảm bảo đủ tên trước writer; `main_receiver_baseline_hong` chỉ đổi baseline đang rỗng sau chốt nền; `main_empty_launch_guard`/`main_receive_false` tương đương trong miền nhóm không rỗng và worker đã kẹp; `gom_drop_decodeerror` vẫn bắt qua ValueError; `writer_record_order` được giao thức cho phép; `source_utf8_roundtrip` giữ nguyên bytes nguồn UTF-8 hợp lệ. Đối chứng trực tiếp: writer thiếu record control lỗi=1/không file, mutant KeyError/không file; baseline_report_sort_equal=True.

18 phép ngoài mẫu một ca: 10 phép đổi miền cấu hình đúng làm cả t53/t54 đỏ; `head_64_only`/`head_no_strip` làm t53 giet_that và t52 tin_dung_gia; `source_wrong_root` làm t52/t53 giet_that; `source_no_capture`/`source_no_text`/`source_digest_form` làm t52/t53 tin_dung_gia; `writer_existing_parent` làm t52 tin_dung_gia; một `head_40_ascii_extra` có t5 rc=141 ở lần đầu, đã ghi nguyên trạng và đối chứng ở HƯỚNG 13. Mười bảy phép đầu là phép thăm dò reviewer đã có từ trước, không phải mutant chuẩn được khai bán kính 1. Không cấp tín dụng giết thật cho lỗi giàn giáo.

HƯỚNG 18: Bán kính chuẩn hoàn tất — mẫu có chủ đích 181/403
  giả thuyết : bản vá mới làm mutant chuẩn sai bán kính hoặc giết oan các ca mới dưới mutant cũ.
  lệnh       : sample_run.py; native_summary.py; kiểm tập tên kết quả bằng đúng sample/sample-names.json; mỗi JSON đúng tập 56 CA; baseline-probes.json cho hai mutant tráo GOC.
  output     : 181/181 mẫu đạt bộ phân hạng bán kính, errors=[]; gồm toàn bộ 65 mutant t52 + 50 mutant t53, 25 mutant t54 đại diện và 41 mutant cũ. Raw: 9.944 qua, 181 giet_that, 11 bo_qua, 0 tin_dung_gia. Năm f38 đều đúng 1 giet_that + 55 qua trên nền có symlink. Không mutant cũ trong mẫu làm t52/t53/t54 khác qua. Hai mutant GOC có 6 và 5 ca bỏ qua; so đủ 53 trạng thái cũ với baseline: delta=0, không chỉ so số lượng bỏ qua.
  kết luận   : KHÔNG PHẢI LỖI hồi quy trong mẫu. Đây là **181/403**, không phải 403/403. Toàn bộ 140 mutant mới trong mẫu có đúng một giet_that và 55 qua. Các ca bỏ qua chỉ thuộc hai mutant GOC cũ và được ghi riêng, không biến thành qua. Không lấy bán kính đang chạy của executor làm bằng chứng.

Mẫu cũ chứa toàn bộ 28 mutant tráo TEP_TEST, cả hai tráo GOC, 10 tráo SCRIPT và một tráo CAI_SH. Phần chưa đo native: 161 BASH_NEN cũ, 9 SCRIPT cũ, 1 CAI_SH cũ, 51 mutant mới đích t54. Ma trận reviewer về dây nối main vẫn đã chạy đầy đủ. Danh sách mẫu cố định theo tiêu chí này; các lần resume chỉ dùng kết quả hoàn tất của chính lượt 17, không chọn lại tên theo kết quả.

HƯỚNG 19: Khóa nguồn và giới hạn bằng chứng
  giả thuyết : bản sao đo trôi khỏi head hoặc cây ứng viên bị sửa trong lúc review.
  lệnh       : git rev-parse HEAD; git status --porcelain; git diff --numstat baseline HEAD; so bytes/băm năm tệp ứng viên với bản sao; kiểm tập tên kết quả và số ca.
  output     : HEAD vẫn 161c4b6ea1df3bb9749f039ad84ed9c4976b5942; status rỗng; 5 tệp +1948/-49. Cả năm tệp trong bản sao bằng nguyên bytes ứng viên (`source-final.json`). SPEC giữ băm đã cho. Ma trận 263 không thiếu ô; mẫu đúng 181 tên, mỗi phép đủ 56 trạng thái.
  kết luận   : KHÔNG PHẢI LỖI. Không sửa cay-kho, không commit/push/đăng verdict hoặc chạy GitHub CI.

**Giới hạn:** Linux/Python 3.11.15; không đo Windows hoặc Python 3.12 thật. Không có lượt A1 tám mảnh native đủ 403 rồi gom; round-trip N=2..16 dùng record dựng sẵn và được phân biệt với bán kính thật. Không đo upload/download artifact trên GitHub, ruleset hay thời gian A9; không xác minh danh tính/effort của executor hoặc thay human audit. Môi trường vắng symlink/callable ném lỗi là mô phỏng có đối chứng. Hai lỗi nền t51/t46 trong mô phỏng và rc=141 lẻ của t5 đều được giữ trong raw evidence, không làm tròn thành pass.

**Kết luận theo lớp: 0 P1, 1 P2 (F39), 0 P3.** “Đóng” dưới đây là trong miền đã liệt kê và đo trên exact head, không phải khẳng định mọi chương trình tương lai đều được bảo vệ.

| Lớp | Miền đã đo | Trạng thái |
|---|---|---|
| Workflow/thực thi hai job | 87 p668, trong đó 60 F1/F3/F10/F14; whitelist job/step/env/defaults/shell/setup/with; matrix os/k/N, needs/if/fail-fast; artifact cùng OS; run/raw/nội suy/tách LF; tháo chốt, registry và actionlint | **Đóng**; biến thể mới mô tả ở H15, không tính vào số ca chạy |
| main/dispatcher | Toàn danh mục H8: du/gate/mảnh, cấu hình, tiền kiểm/CA, từng tham số và bộ đếm, nhóm/receiver/writer, worker, nhiều nguồn lỗi, mọi dòng stdout, argv/arity/exit; đủ checklist qua 56 ca | **Đóng**; 12 survivor tương đương/vẫn fail-closed được giải thích ở H17 |
| Đọc chế độ | 27 ô hiện diện; oracle 458 ô; 10.816 cặp số; mọi nhánh/thứ tự lỗi/giá trị trả, từng thành phần grammar ASCII k/N, fullmatch, nhóm, biên và path | **Đóng** |
| Nguồn vân tay | Git argv/kwargs/rc/ngoại lệ, strip, cả hai grammar HEAD 40/64, 275 ô và lưới rc×stdout; nguồn/digest độc lập; toàn bytes, biên độ dài, case/space/Unicode, IO nguồn | **Đóng**; F36 đã được đo lại cả reviewer mutations lẫn native |
| Phân hoạch/gom/CLI/bộ ghi và năng lực artifact | H9: N=2..16, phủ/rời/danh tính/thứ tự, header/kiểu/khóa/vân tay, record và ngữ nghĩa kết quả, bảng/rc/IO/path; H2/H10–12/H14: probe đủ năm trạng thái, registry thật, import/callback/khôi phục | **Chưa đóng — F39**. Thuật toán gom/ghi và chốt dữ liệu giữ được; đăng ký/giàn giáo năng lực còn lỗi |
| Hồi quy/cổng phụ | Gate 56/56; registry 1025/1025 và baseline 938/938; t152, lease chọn, actionlint hai vế; ruff F 6→6; mẫu native 181/403, 41 mutant cũ không giết thêm ba ca mới | **Đóng trong phạm vi đã đo**; không suy ra 403/403 hoặc nền khác |

| F<n> | Lớp | Mức | Tệp:dòng | Mô tả | Phản chứng |
|---|---|---|---|---|---|
| F39 | Năng lực/giàn giáo artifact | P2 | `ops/cong_cu_test.py:2240`, `:6795`, `:7584`, `:7587` | `f38_probe_bo_attr` đăng ký vô điều kiện dù trên hai trạng thái AttributeError/vắng thuộc tính nó làm module chết trước cửa đo; `_TEN_SL` không canh tên mới này. Ba phép đổi giàn giáo ở đường khôi phục vắng+nạp lỗi, ranh giới callback/try và phân biệt loại ngoại lệ vẫn sống cả 56 ca. Helper gốc hiện đúng 84/84 ô, lỗi ở đăng ký và răng kiểm thử. | `absent-targets.json`: 60/61 giet_that, một tin_dung_gia. `absent-summary.json`: mutant này thêm 9 tin_dung_gia ngoài hai lỗi nền; sáu phép còn lại chỉ thêm t52 giet_that. `capability-exception-matrix.json`: lỗi lặp khi callable ném AttributeError. Ba `measure-*.json` r17: mỗi phép 56 qua; `helper-loading-product.json`: lệch 32/14/54 ô. |

**F39 — HINT PATCH hợp nhất để đóng cả lớp**

Gợi ý, chưa áp trên cây thật; executor tự áp, tự đo, tự chịu trách nhiệm commit. Không cần sửa thuật toán phân hoạch/gom/ghi đang đúng.

1. **Đăng ký:** chuyển tuple `f38_probe_bo_attr` khỏi lô vô điều kiện dòng 2240 sang nhánh năng lực phù hợp. Phương án bảo thủ: chỉ đăng ký khi `_CO_SYMLINK=True`, cùng nhóm ở dòng 7402. Thêm tên này vào `_TEN_SL`; oracle phải liệt kê **mọi** tên đăng ký có điều kiện, kể cả tên mutant kiểm việc bỏ đăng ký nếu thêm chúng. True đòi đủ từng tên, False đòi vắng cả nhóm. Không sửa bộ phân hạng để chấp nhận import crash thành giet_that.
2. **Lưu/khôi phục:** giữ sentinel/getattr/finally của `_nap_lai_sl`. Đổi fixture gốc vắng thành hàm nhận cả callback và tệp, gọi chính helper khi thuộc tính vắng, rồi khôi phục trạng thái ngoài cùng bằng finally. Thêm tích chéo gốc có/vắng × nạp thành công/lỗi, thay vì chỉ thử từng trục riêng.
3. **Đủ ô:** dùng miền 84 ô đã đo ở H12, hoặc các nhóm tương đương có giải thích rõ: hai trạng thái gốc; callback giữ/xoá/gán callable ném từng OSError/NotImplementedError/AttributeError/tự ném RuntimeError sau đổi trạng thái; đầu vào mặc định/rỗng và các đường nạp thành công, tệp thiếu, RuntimeError, SyntaxError, thiếu loader, thư mục. Đòi đúng capability, danh tính tên đăng ký, `NEM:<Loại>`, hiện diện thuộc tính và identity được khôi phục. Không chỉ đếm ô. Fixture tệp thiếu nên nằm trong TemporaryDirectory; kỳ vọng “giữ nguyên” phải theo năng lực gốc thực tế, không hardcode True trên nền không hỗ trợ.
4. **Giết đủ ba phép mới bằng t52:** (a) `if cu_sl is sl_vang:` → điều kiện bổ sung chỉ khi kết quả không bắt đầu bằng `NEM:`; ô gốc vắng+nạp lỗi bắt. (b) di chuyển `cach()` ra trước try; callback ném sau đổi trạng thái bắt. (c) `"NEM:" + type(ex).__name__` → hằng `"NEM:FileNotFoundError"`; lỗi nạp/callback loại khác bắt. Neo/thay nguyên văn nằm trong `r17-mutations.json` và `r17-extra-mutations.json`; mỗi phép hiện đã chạy 56/56 qua.
5. **Giữ răng đăng ký:** tiếp tục đo năm mutant F38 cũ trong đúng miền đăng ký, hai mutant điều kiện F37, bỏ từng đăng ký có điều kiện (chỉ đăng ký phép bỏ khi nhánh ấy hoạt động). Đo môi trường thật sự có/vắng/callable ném ba loại lỗi bằng tiến trình con; **không** dùng phép gán `_CO_SYMLINK=False` để thay cho kiểm startup vì nó né chính probe đang lỗi.
6. **Bán kính:** để toàn bộ tráo/xoá thuộc tính trong cửa con t52, khôi phục bằng finally; không gắn oracle mới vào t53/t54. Đo đủ 56 ca cho mutant mới, năm F38 và các mutant đăng ký liên quan ở nền có/vắng thuộc tính; giữ raw states và so đúng baseline khi mô phỏng có hai lỗi cũ t51/t46. Đo lại mẫu cũ tráo TEP_TEST/GOC để tránh lặp F22. Không biến “không đo được” hoặc lỗi import thành tín dụng giết thật.

**ĐỐI CHIẾU LƯỢT TRƯỚC:** F38 gốc **ĐÃ VÁ THẬT**: cùng trạng thái vắng thuộc tính, nguồn lượt 16 làm t52 tin_dung_gia, head này cho qua; sentinel/helper khôi phục đúng ở 84 ô. Nhưng bản vá **VÁ SINH LỖI MỚI** ở đăng ký `f38_probe_bo_attr`, và giàn giáo vẫn thiếu tích chéo/ngoại lệ, gộp thành F39. Không đánh đồng sửa đúng lỗi gốc với đóng cả lớp.

**Trạng thái F1–F38 (không có F4)**

| Finding | Trạng thái và bằng chứng lượt này |
|---|---|
| F1 | Đóng — 20 ca workflow bị chặn; tháo chốt thực thi/shell làm lọt |
| F2 | Đóng — toàn ma trận main/du/gate/mảnh và mẫu native t54 |
| F3 | Đóng — 28 ca có sẵn; splitlines + tháo raw guard làm 27 ca lọt |
| F5 | Đóng — receiver, writer và mã thoát có răng |
| F6 | Đóng — mọi giá trị record và cộng kết quả nhóm được đo |
| F7 | Đóng — cấu hình, tiền kiểm, lỗi trước/sau và nhiều nhóm |
| F8 | Đóng — CLI gom dùng đúng hàm/vân tay/tham số/rc |
| F9 | Đóng — HEAD và digest nguồn độc lập; toàn bytes được F36 bảo vệ |
| F10 | Đóng — 7 ca nội suy/raw bị chặn; gỡ guard làm lọt |
| F11 | Đóng — t152 hai vế đạt, hook/ci thống nhất 5 AL_VER |
| F12 | Đóng — tên ca, nhiều kết quả và stdout nguyên văn |
| F13 | Đóng — dispatcher --gop, cửa thật và sys.exit |
| F14 | Đóng — 5 ca thiếu shell bị chặn; gỡ chốt làm lọt |
| F15 | Đóng — lỗi 0/1/>1, cộng nhiều nguồn không ghi đè |
| F16 | Đóng — record đúng cấu trúc nhưng sai kết quả bị từ chối |
| F17 | Đóng — nhiều lỗi CLI trả đúng mã và nguyên bảng |
| F18 | Đóng — N=8, lỗi đúng một, nhiều dòng/nhiều nguồn |
| F19 | Đóng — bảng giữ danh tính, thứ tự và chi tiết |
| F20 | Đóng — đảo bảng CLI bị bắt |
| F21 | Đóng — writer đọc mọi record, cộng lỗi và không ghi mảnh sai |
| F22 | Đóng — đủ 28 mutant TEP_TEST cũ và hai GOC trong mẫu; không giết thêm ba ca mới |
| F23 | Đóng — nhiều ca bỏ qua, tên/lý do/số đếm không bị nén |
| F24 | Đóng lỗi gốc — strict int và symlink thực; lớp năng lực còn F39 |
| F25 | Đóng — chỉ argv[1] chọn cửa; đối số không chiếm dispatch |
| F26 | Đóng — cửa không đối số gọi main và giữ mã thoát |
| F27 | Đóng — k=0, path khác x, worker 1/khác 1, tự kiểm nhánh đủ |
| F28 | Đóng — default entry trên cấu hình hợp lệ du/gate/mảnh |
| F29 | Đóng — đủ 27 ô vắng/rỗng/có và thứ tự thẻ lỗi |
| F30 | Đóng — rc Git và grammar HEAD được đo độc lập |
| F31 | Đóng — khoảng trắng/hoa-thường gate không được chuẩn hóa để nhận |
| F32 | Đóng — HEAD đúng hai độ dài 40/64, lowercase ASCII hex |
| F33 | Đóng — mọi thành phần grammar k/N, biên và path |
| F34 | Đóng — nguồn, lời gọi Git, ngoại lệ và bytes |
| F35 | Đóng lỗi gốc — phân hoạch, header/N, path/parent/IO; lớp năng lực còn F39 |
| F36 | Đóng — các phép bytes reviewer và bảy mutant native đều bị t53 giết đúng |
| F37 | Đóng lỗi gốc — bốn tên cũ theo năng lực đúng; mutant mới ngoài nhóm sinh F39 |
| F38 | Đóng lỗi gốc — helper chịu thuộc tính vắng; bản vá sinh F39 nên cả lớp chưa đóng |

verdict: changes_requested
reviewed_sha: 161c4b6ea1df3bb9749f039ad84ed9c4976b5942
