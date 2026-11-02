# Cross-review độc lập #668 — lượt 18

verdict: changes_requested
reviewed_sha: 42f74db160762dcb6248e98e1ceb17a148194d28

**Kết luận: 0 P1, 1 P2 (F40), 0 P3.** Lớp registry năng lực artifact chưa đóng: ô tự kiểm bỏ sót tên chỉ đăng ký khi năng lực False. Các lớp còn lại đóng trong miền đã đo. Hoàn tất 263/263 phép checklist × 56 ca và mẫu native 175/397; giới hạn và nhiễu được giữ riêng dưới đây.

Phạm vi: review theo lớp; không sửa mã trong cay-kho. Đột biến chỉ trên bản sao /tmp. Miền mô phỏng xoá/đổi thuộc tính os.symlink bị loại theo quyết định chủ kho; vẫn đo năng lực thật và lỗi OSError/NotImplementedError.

HƯỚNG 1: Neo nguồn và phạm vi
  giả thuyết : vật liệu không khớp head hoặc spec.
  lệnh       : git -C cay-kho rev-parse HEAD; git status --porcelain; sha256sum SPEC.md; đọc SPEC/LEASE/AGENTS/CLAUDE/protocol §8 và diff-vong-18.patch.
  output     : HEAD=42f74db160762dcb6248e98e1ceb17a148194d28; status rỗng; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15. Sao đo /tmp/review668-r18; baseline /tmp/review668-r18-base tại f8a7829. Runner env ghim core.abbrev=7, commit.gpgsign=false.
  kết luận   : KHÔNG PHẢI LỖI. Dùng quyết định thu hẹp và trần ~1.960 của chủ kho trong prompt. Không chạy GitHub CI/push/đăng comment.

HƯỚNG 2: Workflow và răng F1/F3/F10/F14
  giả thuyết : thu hẹp artifact làm hỏng lớp workflow, hoặc phản chứng chỉ hiện diện mà không bắt được lỗi.
  lệnh       : python evidence-luot-18/env.py python evidence-luot-18/workflow.py; workflow_ablation_extra.py. Chỉ chạy payload đã có sẵn.
  output     : control chặn 20 F1 + 28 F3 + 7 F10 + 5 F14; gỡ raw guard làm 7 F10 lọt; gỡ raw guard và đổi splitlines làm 27 F3 lọt; gỡ execution guard làm 13 F1 lọt; gỡ shell guard làm 5 F14 lọt. Log và JSON ở evidence-luot-18/workflow-*.
  kết luận   : KHÔNG PHẢI LỖI. Chốt LF có bảo vệ chồng raw guard: đổi splitlines riêng không làm lọt, không được diễn giải thành ca thiếu răng.

HƯỚNG 3: Neo đột biến — kiểm toàn registry
  giả thuyết : hai neo F29 còn trùng oracle, hoặc neo bị mất sau gỡ F38.
  lệnh       : check.py anchors-probes.json; đếm chuỗi neo trên đúng tệp của từng tuple DOT_BIEN.
  output     : 397 tên; toàn bộ 213 neo trên ops/cong_cu_test.py xuất hiện đúng 1 lần. Có 3 neo cũ của ops/bash_nen.py xuất hiện 2/2/3 lần: bn_khong_gap_noi_hang, bn_anh_chup_chi_dem_so, bn_bo_hang_byte. Chi tiết anchors.json.
  kết luận   : KHÔNG PHẢI LỖI mới ở packet; lời khai duy nhất ĐÚNG khi giới hạn ops/cong_cu_test.py, không đúng nếu diễn rộng thành mọi tệp. Sẽ đối chiếu ba neo cũ với baseline trước chốt.

HƯỚNG 4: Liệt kê trọn miền chế độ và vân tay trước kết luận
  giả thuyết : các vòng trước chỉ vá biên đầu tiên, còn nhánh chưa được đo.
  lệnh       : đọc _doc_che_do/_van_tay; measure.py all-domain-mutations.json; probe.py, domain.py, domain_check.py, mode_domain.py, extent.py, source_io.py đang chạy trên head này.
  output     : miền liệt kê dưới đây; kết quả hoàn tất sẽ ghi khối riêng, không nhận kết quả lượt cũ.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận cuối tại checkpoint này.

Miền `_doc_che_do` (đầu vào env thực: giá trị chuỗi hoặc vắng):

- Cả ba biến BK/MH/RA: vắng, rỗng, có; 27 ô và thứ tự lỗi. MH vắng: RA hiện diện luôn C-ra-le; RA vắng + BK vắng → du; BK đúng nguyên văn manh → gate, mọi chuỗi khác → C-ban-kinh. MH hiện diện và BK hiện diện (kể cả rỗng) → C-ca-hai trước grammar.
- Grammar MH là fullmatch: nhóm k nhánh riêng 0 hoặc chữ số đầu ASCII 1..9 + chữ số ASCII 0..9 tuỳ chọn; đúng một dấu /; nhóm N chữ số đầu ASCII 1..9 + một chữ số ASCII tuỳ chọn; không số dẫn 0, dấu cộng/trừ, thập phân, số mũ, whitespace, Unicode digits, tiền/hậu tố. Hai nhóm không tráo; int rồi 2≤N≤16, k<N, k=0 nhận.
- RA sau grammar/biên: vắng/rỗng bị C-thieu-ra; chuỗi không rỗng được giữ nguyên, kể cả dấu cách và đường lồng. Giá trị trả đúng nhãn và bộ (k,N,RA), không strip/lower hoặc ép vắng.

Miền `_van_tay`:

- Gọi đúng git -C str(GOC) rev-parse HEAD; capture_output=True, text=True, timeout=60; rc=0 và rc khác 0 độc lập với stdout. OSError và SubprocessError (kể cả TimeoutExpired) → HEAD None; lỗi đọc nguồn không tạo digest giả.
- stdout strip hai đầu rồi fullmatch đúng hai nhánh độ dài 40 hoặc 64; mỗi vị trí chỉ ASCII 0..9/a..f, không uppercase, g..z, Unicode, tiền/hậu tố hoặc độ dài xen giữa. Chuỗi rỗng/sai → None.
- sha256_test từ TOÀN BỘ bytes của Path(TEP_TEST) đang chạy, không SCRIPT/GOC/đường thay thế; đúng SHA-256 hexdigest. Đo bytes rỗng, ngắn, case/space/Unicode, biên 63/64/65, 4095/4096/4097/8193, nguồn thật; lỗi vắng/thư mục/đọc. Fixture độc lập với oracle để tránh đổi cả nguồn và kỳ vọng cùng lúc.

HƯỚNG 5: Liệt kê trọn quyết định main/dispatcher
  giả thuyết : giàn giáo bỏ sót một dây nối hay tham số nhưng 56 ca vẫn xanh.
  lệnh       : run_checklists.py; fields_full.py; novel_entry.py; partition_identity.py; toàn suite từng phép.
  output     : ma trận đang chạy, kết quả hoàn tất ghi sau; danh mục kiểm bên dưới.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận cuối tại checkpoint này.

Miền main: lỗi cấu hình phải rc=2 trước tiền kiểm/CA; hai tiền kiểm đúng thứ tự/tên; mọi CA đúng một lần và thứ tự, qua/AssertionError/ngoại lệ khác/BoQuaMoiTruong tách tên+lý do+bộ đếm+mẫu số; toàn dòng stdout. Mảnh truyền k/N/RA nguyên vẹn, phân hoạch đúng tên/thứ tự; nền đỏ hoặc tiền kiểm bỏ qua dọn tệp bằng writer với đúng fingerprint và rc=1; nhóm/worker/baseline rỗng tới `_phong_con`; từng nhom/rc/stdout/baseline tới receiver; giữ lý do lỗi đầu, đuôi 300 ký tự và rc, gom mọi nhóm và mọi giá trị; lỗi con buộc ket=None; writer đủ bảy tham số, in mọi dòng và chuẩn hoá lỗi 0/1/>1 thành rc. Nhánh đủ/gate gọi cổng cây thật GOC, phân hạng, giàn giáo, báo nền đỏ đã sort, worker và tự kiểm song song đúng đối số; cộng lỗi không ghi đè, nhiều nguồn lỗi đồng thời; gate không gọi vòng bán kính nhưng in giao mảnh; đủ truyền trọn DOT_BIEN/thứ tự/baseline/worker, nhận mọi kết quả/dòng/lỗi; tổng kết và rc phụ thuộc đủ bốn nguồn. Dispatcher chọn duy nhất argv[1], --gop đúng cửa/arity/thư mục/vân tay/bảng/rc; cờ nằm ở đối số không đổi cửa; đối số lạ rc=2; cửa không đối số gọi main và giữ rc trên cấu hình hợp lệ du/gate/mảnh lẫn cấu hình sai.

HƯỚNG 6 (MỚI): Nhánh đăng ký chỉ dành cho năng lực False, vừa thêm ở lượt 18
  giả thuyết : bộ lọc `_TEN_SL` chỉ nhìn bốn tên phía True; bỏ sót tên `f37_dk_luon_dung` vừa chuyển sang phía False.
  lệnh       : measure.py r18-mutations.json; check.py expanded-probes.json. Phép đổi là dữ liệu JSON, không sửa cay-kho và không thay os.symlink.
  output     : trên nền có symlink thật, `false_registry_always` (điều kiện mới `if not _CO_SYMLINK:` → `if True:`) và `false_registry_never` (→ `if False:`) đều 56/56 qua. Bản luôn đăng ký có registry 398; đo chính mutant được thêm `f37_dk_luon_dung` cũng 56/56 qua, bộ phân hạng trả errors=1. Raw: native-measure-false_registry_always.json, native-measure-false_registry_never.json, expanded-registry.json.
  kết luận   : LỖI (P2) — F40, lớp năng lực artifact chưa đóng trong phạm vi THẬT có symlink. Chốt mới thiếu răng với đăng ký SAI phía. `false_registry_never` tương đương trên True, không dùng nó làm finding phía True. Không có P1: vòng bán kính thật sẽ đỏ vì mutant tương đương; lỗi là suite t52 không bảo vệ chốt đăng ký như yêu cầu.

HƯỚNG 7 (MỚI): Hạn chế symlink ở syscall, giữ nguyên thuộc tính/callable os.symlink
  giả thuyết : nhánh không quyền thực tế có lỗi đăng ký khác với nền True; mô phỏng gán cờ có thể bỏ qua lỗi startup.
  lệnh       : REVIEW_CAP=denied python env.py python system_probe.py check.py capability-probes.json; system_probe.py measure.py r18-mutations.json force. libseccomp chỉ trả EPERM cho symlink/symlinkat; bộ lọc kế thừa sang con.
  output     : hai phép r18 vẫn không giết t52; cả hai chỉ có t51 tin_dung_gia vì PermissionError và t46 bo_qua vì không tạo được symlink. Đối chứng toàn baseline và registry nguyên bản đang chạy, sẽ báo riêng.
  kết luận   : LỖI (P2) cùng F40 ở nhánh False: t52 không kiểm tên chỉ được đăng ký khi False, nên bỏ đăng ký ấy không bị t52 bắt. Đây không phải xoá/đổi os.symlink; builtin còn nguyên, hệ điều hành từ chối thao tác. Không cấp tín dụng giết thật cho hai trạng thái nền cũ.

HƯỚNG 8: Gom/mảnh/bộ ghi — miền hành vi và dữ liệu
  giả thuyết : gom xanh trên bộ sai hoặc writer vẫn tạo artifact sau lỗi.
  lệnh       : domain.py; schema_io.py; partition_roundtrip.py; probe.py; ma trận gom-semantic/cli-new/gom-extra/writer-extra/new/r14-artifact.
  output     : control phân hoạch sai 0/135 ô; hai phép xoay/đảo nguồn sai 135/135. Round-trip N=2..16 đều phủ/rời 397 tên, gom_errors=0, bảng đúng thứ tự. Header bool/float ở trường số bị từ chối; bỏ strict type làm phien_ban True/1.0 và manh False/0.0 được nhận. Symlink bị từ chối, gỡ chốt thì gom xanh; writer xoá link cũ và giữ đích KEEP; ghi lỗi không còn tệp cũ.
  kết luận   : KHÔNG PHẢI LỖI thuật toán qua phép hành vi. Bán kính ma trận còn đang chạy.

Miền artifact đã đặt để đo: thư mục vắng/rỗng/không thư mục; mọi mục thường và không symlink; header UTF-8/prefix/JSON/dict/đúng năm khoá; strict int ở version/k/N, version=1; cả HEAD và digest khớp nguồn; head nguồn vắng; body chỉ BKCON/blank; N đồng nhất 2..16, tập k đủ và đúng một tệp/k; phân hoạch phủ/rời/đúng danh tính/thứ tự; đủ record/đúng nhóm/đích/trạng thái/mọi ca, đích sống/tín dụng giả/bán kính >1; bảng nguyên danh tính/thứ tự/chi tiết và CLI chuẩn hoá rc 0/1/>1. Writer: tệp cũ/link sống/link gãy, ket=None, HEAD=None, thiếu record, lỗi cuối/nhiều lỗi, đủ trường header/body, parent lồng/có sẵn, giữ path có space, lỗi read/decode/unlink/write. Record có thứ tự khác được giao thức cho phép, bảng gom vẫn theo DOT_BIEN. Các round-trip dùng record dựng sẵn, không gọi là bán kính native.

HƯỚNG 9: Cổng hồi quy hai vế
  giả thuyết : thu hẹp làm đổi các cổng ngoài lớp năng lực.
  lệnh       : run_regression.py (regression.py, registry hai vế, gate).
  output     : registry head 1025/1025 đỏ đúng, baseline 938/938 đỏ đúng; cả hai TỔNG: ĐẠT. t152 và năm ca lease t24/t31/t35/t161/t162 đều PASS hai vế; actionlint rc=0 hai vế; ruff F 6→6. Gate còn đang chạy; chưa tính là đạt.
  kết luận   : KHÔNG PHẢI LỖI trong phần đã hoàn tất.

HƯỚNG 10: Hint cho cả hai phía của registry năng lực
  giả thuyết : có thể đóng F40 bằng chính ô năng lực hiện có, không mở lại miền nạp lại/thuộc tính vắng.
  lệnh       : check.py hint-probes.json trên bản sao /tmp/review668-r18-hint; chạy cả builtin thật lẫn syscall EPERM. Hint ở hint-data.json, không áp lên cây ứng viên.
  output     : True: t52/t53/t54 đều qua; always→giet_that, never→qua (tương đương). False: t52/t53/t54 đều qua; always→qua (tương đương), never→giet_that. Đang đo thêm toàn 56 ca để kiểm collateral.
  kết luận   : LỖI (P2) F40 có hướng vá hẹp đã đo hai chiều. Không cần helper nạp lại hoặc mô phỏng xoá/đổi thuộc tính.

HƯỚNG 11: Biến thể workflow mới — mô tả, không tạo payload
  giả thuyết : ký tự định dạng Unicode in được theo cách người đọc hiển thị nhưng không in được theo Python có thể làm bộ tách bỏ sai chú thích.
  lệnh       : không soạn payload mới; đối chiếu raw guard với phép tháo guard HƯỚNG 2.
  output     : đề nghị executor đặt U+2060 WORD JOINER ngay sau dấu chú thích ở một dòng trước lệnh gom. Bash vẫn coi cả dòng là chú thích; validator hiện từ chối vì isprintable() trả False. Đây là đối chứng âm về ranh giới raw policy, không phải một đường thực thi lệnh bị giấu. Có thể ghép với biểu thức GitHub trong cùng chú thích sinh LF U+000A; khi đó GitHub nội suy trước Bash có thể tạo dòng lệnh mới, nhưng raw guard phải từ chối ngay dấu mở biểu thức, độc lập U+2060.
  kết luận   : KHÔNG PHẢI LỖI theo predicate đã đo; biến thể chỉ được mô tả bằng lời, không tính vào số fixture đã chạy.

HƯỚNG 12: Đối chứng nhiễu và lỗi nền, không làm tròn thành pass
  giả thuyết : thay đổi t52 gây giết thêm t5 hoặc hai ca phụ thuộc symlink.
  lệnh       : recheck_noise.py (40 lượt mỗi vế); noise_sources.py; check.py retry-probes.json; system_probe.py check.py baseline-probes.json; check.py baseline-radius-probes.json.
  output     : mutant chuẩn t32_bo_nhan_dong_ho_nhay lần đầu giết đích và t5 (rc=141), bán kính 2/56. Đo lại đủ 56 ca: đúng một đích, errors=0; 80 lượt t5 riêng đều qua. AST t5 và bytes năm phụ thuộc không đổi so baseline. Dưới syscall EPERM, baseline 53 ca cũng có đúng t51 tin_dung_gia và t46 bo_qua như head; không có delta ở hai ca này. Hai mutant tráo GOC có 6/5 ca bỏ qua, so đủ 53 tên/trạng thái với baseline: delta=0.
  kết luận   : KHÔNG PHẢI LỖI mới chứng minh được của packet. Giữ nguyên radius-t32_bo_nhan_dong_ho_nhay.json ban đầu và retry-t32.json; không thay raw bằng lần xanh. Bán kính mới sẽ báo số đạt lần đầu và lần đo lại riêng.

HƯỚNG 13: Chốt gate và nghĩa hẹp của tính duy nhất
  giả thuyết : rc=0 nhưng thiếu bằng chứng dương hoặc số neo bị khai quá rộng.
  lệnh       : đọc gate.log/regression-run.log; baseline-probes.json; so Ruff bằng (tệp, mã F, thông báo), không chỉ tổng số.
  output     : gate rc=0, cong_cu_test 56/56, tổng 56, bỏ qua=0, tiền kiểm bỏ qua=0; N126 ĐẠT; cổng cây thật ĐẠT; 397 đột biến giao mảnh; lỗi đột biến=0. Ruff added=[]/removed=[]. Ba neo ops/bash_nen.py không duy nhất có đúng số 2/2/3 trên baseline, không do packet.
  kết luận   : KHÔNG PHẢI LỖI. Gate không đo vòng bán kính là hành vi M1, không dùng gate xanh để thay bằng chứng bán kính.

Phương pháp resume: ba runner pool ban đầu được ngắt ở tầng điều phối để chia lại tải; chỉ JSON đã hoàn tất, đủ tập 56 tên CA của chính lượt 18 được tái dùng. Không lấy JSON kết quả lượt 17. `resume.py` gọi lại đúng các phép cũ; các runner native/measure dùng cache kết quả hoàn tất theo tên. Log điều phối có rc=130 là lượt ngắt chưa kết luận, không phải ca test pass/fail. Bảng cuối phải đủ 263 phép trước khi chốt lớp.

HƯỚNG 14: Chốt trọn miền registry năng lực còn trong phạm vi
  giả thuyết : việc thu hẹp gây thêm lỗi ở phía True hoặc các lỗi OSError/NotImplementedError hợp lệ.
  lệnh       : capability-probes.json ở ba môi trường; r18-mutations.json đầy đủ 56 ca ở True và EPERM; registry-extra-mutations.json qua ca đích; hint-data.json ở ba môi trường và hint-real/hint-denied qua đủ 56 ca.
  output     : True: registry 397, baseline 56 qua; 7 mutant F24/F35/F37 đo riêng đều chỉ giết t52. False/EPERM: registry 394; 4 mutant đăng ký tương ứng chỉ thêm t52 giet_that so với baseline (t51 tin_dung_gia, t46 bo_qua). False/NotImplementedError: baseline t51/t46 tin_dung_gia, 4 mutant cũng chỉ thêm t52 giet_that. Bỏ tên đăng ký f37_bo_f24 hoặc f37_bo_f35 bị t52 giết. Hint: cả ba ca mới vẫn qua trên ba môi trường; toàn suite luôn-đăng-ký trên True chỉ t52 giet_that; không-đăng-ký trên EPERM chỉ thêm t52 giet_that ngoài hai trạng thái nền.
  kết luận   : LỖI (P2) duy nhất trong lớp là F40: tên ở nhánh False bị bỏ ngoài tập quan sát. Bốn tên True, điều kiện phía True, bỏ từng tên, và hai cách False còn trong phạm vi đã được đo. Không mở lại lớp nạp lại hoặc thuộc tính vắng; không biến NotImplementedError mô phỏng thành bằng chứng nền Windows thật.

HƯỚNG 15: Bán kính chuẩn — hoàn tất mẫu có chủ đích 175/397
  giả thuyết : bỏ giàn giáo làm mutant chuẩn mất bán kính hoặc mutant cũ giết oan ba ca mới.
  lệnh       : sample_run.py và các lượt resume theo cùng sample/sample-names.json; native_summary.py; kiểm đúng tập 56 CA từng kết quả.
  output     : 175/175 tên hoàn tất. Bao gồm TOÀN BỘ 59 mutant đích t52 + 50 đích t53, 25 đích t54 và 41 mutant cũ. 174/175 đạt phân hạng ngay lần đầu; t32_bo_nhan_dong_ho_nhay có thêm t5 rc=141, đã đo lại 1/56 ở H12. Raw tổng: 9.613 qua, 176 giet_that, 11 bo_qua, 0 tin_dung_gia. Không mutant cũ nào làm t52/t53/t54 khác qua. Toàn bộ 134 mutant mới trong mẫu đều đúng một giet_that và 55 qua.
  kết luận   : KHÔNG PHẢI LỖI hồi quy packet trong mẫu, với nhiễu lần đầu giữ nguyên như H12. Đây là 175/397, không phải 397/397; không lấy phép đang chạy hoặc lời khai executor làm bằng chứng.

Mẫu cố định theo tiêu chí: tất cả đích t52/t53 để bao phủ thay đổi artifact và nguồn; t54 đại diện nhánh/dispatcher/worker/path/rc cùng ma trận reviewer đầy đủ; mutant cũ gồm toàn bộ 28 tráo TEP_TEST, cả hai tráo GOC, 10 tráo SCRIPT và một tráo CAI_SH. Chưa đo native: 161 BASH_NEN cũ, 9 SCRIPT cũ, 1 CAI_SH cũ và 51 đích t54. Không có lượt tám mảnh native đo đủ 397 rồi gom; round-trip N=2..16 dùng record dựng sẵn và được báo riêng ở H8.

HƯỚNG 16: Chốt TOÀN BỘ checklist và toàn miền chế độ/vân tay
  giả thuyết : còn phép chưa chạy hoặc một survivor không tương đương bị bỏ qua.
  lệnh       : summarize.py; đối chiếu input-coverage.json với đúng các bảng r12/r13/r14/r14-artifact/r15/r15-extra được yêu cầu; kiểm đủ tập 56 tên CA từng kết quả.
  output     : MATRIX 263; MISSING 0; 234 phép chỉ ca đích giet_that; 17 phép ngoài mẫu một ca; 12 survivor. Toàn bộ 138 phép checklist lượt 10 + 22 phép fields/entry/partition + 103 phép miền đã hoàn tất trên head này. Không mục nào của sáu bảng được yêu cầu bị thiếu hoặc đổi neo/thay. Lưới chế độ 458 ô, lưới số 10.816 ô (135 nhận/10.681 từ chối), 11 grammar âm; 27 ô phối hợp và lưới rc×stdout; HEAD 275 ô; bytes 13 fixture × 10 phiên bản = 130 lượt đều đối chiếu oracle độc lập. Chi tiết: mutation-matrix.md, review-summary.json, grids.json, domain-check.json, domain-results.json, extent.json, source-io.json.
  kết luận   : KHÔNG PHẢI LỖI mới. Main/dispatcher, đọc chế độ, nguồn vân tay, phân hoạch/gom/CLI/bộ ghi đều giữ trạng thái đóng trong miền H4/H5/H8. Registry năng lực vẫn chưa đóng vì F40 đã đo riêng, không bị phép tổng hợp loại khỏi kết luận.

12 survivor, giữ nguyên trong ma trận:

- `receiver_baseline` chỉ thêm tên không thuộc CA; `main_receiver_baseline_hong` truyền chính danh sách đang rỗng sau chốt nền. Cả hai không đổi tập ca được nhận.
- `break_on_error` không bỏ việc phóng/đợi con vì `_phong_con` đã trả cả danh sách; mảnh vẫn đỏ và không có file.
- `final_hong` còn bị `loi_nen` kéo đỏ; `final_gate_eq_one` tương đương vì `_cong_tren_cay_that` trả 0/1.
- `main_no_sorted_baseline` vẫn được helper sắp; đã đối chứng trực tiếp `baseline_report_sort_equal=True`.
- `main_empty_launch_guard`/`main_receive_false` tương đương khi nhóm không rỗng và worker đã kẹp; registry hiện lớn hơn N tối đa.
- `writer_drop_missing` vẫn KeyError và không file; control trả lỗi=1 và không file. Caller thật đã kiểm đủ tên trước writer.
- `gom_drop_decodeerror`: UnicodeDecodeError vẫn bị ValueError bắt.
- `writer_record_order`: giao thức cho phép thứ tự record khác; bảng gom tái lập thứ tự DOT_BIEN.
- `source_utf8_roundtrip`: decode/encode UTF-8 giữ nguyên bytes của nguồn Python UTF-8 hợp lệ; không phải phép chuẩn hoá newline/case/space.

17 phép ngoài mẫu một ca: 10 phép thay miền cấu hình hợp lệ làm cả t53/t54 giet_that; `head_64_only`/`head_no_strip` làm t53 giet_that và t52 tin_dung_gia; `source_wrong_root` làm t52/t53 giet_that; `source_no_capture`/`source_no_text`/`source_digest_form` làm t52/t53 tin_dung_gia; `writer_existing_parent` làm t52 tin_dung_gia. Đây là phép thăm dò reviewer, không phải các mutant chuẩn được khai 1/56; không cấp tín dụng giết thật cho tin_dung_gia. Không có nhiễu t5 trong 263 kết quả lượt này.

HƯỚNG 17: Khoá nguồn và kiểm tính đầy đủ cuối lượt
  giả thuyết : cây đo trôi khỏi exact head hoặc kết quả thiếu ca nhưng được đếm như hoàn tất.
  lệnh       : check.py final-probes.json; Git HEAD/tree/status/numstat, băm năm tệp, SPEC, so tập kết quả và CA.
  output     : final_audit PASS; HEAD=42f74db160762dcb6248e98e1ceb17a148194d28, tree=fbf41d8ce73391eafc8fc7836adde78b6430bf64, status sạch. Năm tệp bản sao bằng nguyên bytes cây ứng viên; +1897/-49, nằm trong trần ~1.960. SPEC đúng băm được cấp. Matrix đủ 263; sample đúng 175 tên và từng kết quả đúng tập 56 CA. final-audit.json lưu băm từng tệp và thống kê đầy đủ.
  kết luận   : KHÔNG PHẢI LỖI. Không sửa cay-kho; mọi đột biến/hint nằm ở bản sao /tmp và dữ liệu evidence.

**Bảng kết luận theo lớp** — “đóng” chỉ trong miền đã liệt kê và đo, không phải khẳng định mọi biến thể tương lai đã được bảo vệ.

| Lớp | Miền đã đo | Trạng thái |
|---|---|---|
| Workflow/thực thi hai job | 87 p668, gồm 60 F1/F3/F10/F14; raw/LF/nội suy/shell; whitelist job/step/env/defaults/setup/with, matrix OS/k/N, needs/if/fail-fast, artifact đúng OS; tháo chốt, registry, actionlint | **Đóng**. Biến thể H11 chỉ mô tả, không tính là fixture đã chạy |
| Main/dispatcher | Toàn danh mục H5; du/gate/mảnh, cấu hình/tiền kiểm/CA, từng đối số/giá trị/nhóm/bộ đếm, nhiều nguồn lỗi, worker/path, stdout, argv/arity/exit; đủ checklist qua 56 ca | **Đóng** |
| Đọc chế độ | H4: vắng/rỗng/có và thứ tự lỗi; mỗi thành phần grammar ASCII k/N, fullmatch, nhóm, biên và path; 458 ô + 10.816 cặp số + 27 ô phối hợp, mutations r12–r14 | **Đóng** |
| Nguồn vân tay | H4: argv/kwargs/rc/ngoại lệ Git; strip và hai grammar HEAD 40/64; toàn bytes TEP_TEST/digest; lưới 275 HEAD, rc×stdout, 130 lượt bytes và IO; mutations r12–r15 | **Đóng** |
| Phân hoạch/gom/CLI/bộ ghi | H8: N=2..16, danh tính/thứ tự/phủ/rời, header strict type/khóa/vân tay, record/kết quả, bảng/rc/path/IO, stale file và symlink thật | **Đóng** |
| Registry năng lực artifact | H6/H7/H14: True thực; False do EPERM thật ở syscall và NotImplementedError mô phỏng; 4 tên phía True, điều kiện và từng đăng ký; tên phía False; răng native/56 ca/hint hai phía | **Chưa đóng — F40**. Miền thuộc tính vắng/nạp lại đã loại và không dùng làm finding |
| Hồi quy/cổng phụ | Gate 56/56, registry 1025/1025 và baseline 938/938, t152, lease chọn, actionlint, Ruff F delta rỗng; mẫu native 175/397, 41 cũ không giết thêm ca mới | **Đóng trong mẫu đã đo**, giữ riêng nhiễu t5 lần đầu; không suy thành 397/397 |
| Neo đột biến | 213 neo của ops/cong_cu_test.py đều xuất hiện đúng 1 lần; toàn 397 neo được đếm; 3 neo bash_nen.py lặp đã có trên baseline | **Đóng cho packet**; không khai mọi neo toàn kho đều duy nhất |

| F<n> | Lớp | Mức | Tệp:dòng | Mô tả | Phản chứng |
|---|---|---|---|---|---|
| F40 | Registry năng lực artifact | P2 | `ops/cong_cu_test.py:6781`, `:7402`, `:7576`, `:7836` | `_TEN_SL` và ô năng lực chỉ quan sát bốn tên phía True, bỏ sót `f37_dk_luon_dung` mới chuyển sang nhánh False. Trên nền có symlink thật, đăng ký sai tên này vô điều kiện vẫn qua 56/56; registry thành 398 và chính mutant thêm vào sống 56/56, làm bán kính đỏ. Trên nền syscall EPERM, bỏ đăng ký phía False cũng không làm t52 đỏ. | `r18-mutations.json`; `native-measure-false_registry_always.json`; `expanded-registry.json` (398, errors=1, 56 qua); `measure-false_registry_never.json` và `capability-denied.json` (delta=0). Hint giết đúng t52 ở từng miền: `hint-real/measure-false_registry_always.json`, `hint-denied/measure-false_registry_never.json`. |

**F40 — HINT PATCH: kiểm ĐỦ tên đăng ký có điều kiện ở CẢ HAI phía**

Gợi ý **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã thử trên bản sao; không thay thuật toán gom/mảnh, không thêm miền đã loại.

- Sửa `ops/cong_cu_test.py`, `t52...` và `_in_tu_kiem_gom`. Giữ `_TEN_SL` là bốn tên chỉ hợp lệ khi True; ô dữ liệu phải quan sát thêm `f37_dk_luon_dung`. Khi False, kỳ vọng chính xác danh sách chứa tên này, thay vì danh sách rỗng. Ví dụ thay hai dòng:

```diff
-    mong_sl = [True, sorted(_TEN_SL)] if _CO_SYMLINK else [False, []]
+    mong_sl = [True, sorted(_TEN_SL)] if _CO_SYMLINK else [False, ["f37_dk_luon_dung"]]
-    kq["nang_luc"] = [_CO_SYMLINK, sorted(t for t in DOT_BIEN if t in _TEN_SL)]
+    kq["nang_luc"] = [_CO_SYMLINK, sorted(t for t in DOT_BIEN if t in _TEN_SL or t == "f37_dk_luon_dung")]
```

- Miền đủ để đóng lớp hiện tại: True có đúng bốn tên/vắng tên False; False do OSError hoặc NotImplementedError có đúng tên False/vắng bốn tên True. Mỗi tên phải kiểm danh tính, không chỉ tổng số. Thuộc tính vắng vẫn là nợ ngoài phạm vi. Nếu executor thêm tên mutant đăng ký có điều kiện mới, danh sách quan sát và kỳ vọng phải bao phủ cả tên mới đó, không lặp lỗi bỏ sót tên mới.
- Răng phải có: điều kiện phía True đảo (f37_dk_dao); mất từng đăng ký True (f37_bo_f24/f35 và các kiểm fixture hiện có); điều kiện phía False thành `if True` **chỉ đo trên True**, thành `if False`/bỏ tuple **chỉ đo trên False**. Cả hai phép mới có neo duy nhất trong `r18-mutations.json`, đích t52. Có thể dùng runner ngoài để giữ kiểm hai môi trường; nếu đưa vào DOT_BIEN phải đăng ký theo đúng miền không tương đương và cập nhật oracle theo trọn registry có điều kiện.
- Rủi ro bán kính: `if False` phía False là tương đương trên nền True; `if True` phía False là tương đương trên nền False. Không đăng ký vô điều kiện rồi coi mutant sống là hồi quy. Giữ so registry trong cửa con t52; không đưa kiểm này sang t53/t54. Đo lại 56 trạng thái cho phép mới/nhóm F24/F35/F37 và mẫu cũ tráo TEP_TEST/GOC; đối chiếu nền thiếu quyền trước khi tính delta, không gọi t51/t46 là giết thật.

**ĐỐI CHIẾU LƯỢT TRƯỚC — F39:** phần lỗi do `_nap_lai_sl`/5 mutant F38 đã **được loại thật theo quyết định thu hẹp**; không có helper nạp lại và không dùng mô phỏng thuộc tính vắng để giữ finding cũ. Tuy nhiên bản vá **VÁ SINH LỖI MỚI trong phạm vi còn lại**: nhánh False mới ở dòng 7402 không nằm trong ô quan sát tên registry. F40 được phản chứng trên nền có symlink thật và nền builtin bị syscall EPERM, độc lập miền đã loại. Lỗi gốc bị loại đúng không đồng nghĩa cả lớp đã đóng.

**Trạng thái F1–F39 (không có F4)**

| Finding | Trạng thái và bằng chứng lượt 18 |
|---|---|
| F1 | Đóng — 20 ca workflow bị chặn; tháo execution/shell guards có ca lọt |
| F2 | Đóng — đầy đủ ma trận main/du/gate/mảnh |
| F3 | Đóng — 28 ca có sẵn; splitlines + gỡ raw guard làm 27 lọt |
| F5 | Đóng — receiver/writer/rc có răng trong checklist |
| F6 | Đóng — mọi giá trị record và kết quả nhiều nhóm |
| F7 | Đóng — cấu hình, tiền kiểm, lỗi trước/sau và nhiều nhóm |
| F8 | Đóng — CLI gom đúng hàm, tham số, vân tay và rc |
| F9 | Đóng — HEAD/digest độc lập, toàn bytes được đo |
| F10 | Đóng — 7 ca raw/nội suy bị chặn; gỡ guard làm lọt |
| F11 | Đóng — t152 hai vế qua; hook/CI khớp 5 AL_VER |
| F12 | Đóng — tên ca, nhiều kết quả, nguyên stdout |
| F13 | Đóng — dispatcher --gop và sys.exit qua cửa thật |
| F14 | Đóng — 5 ca thiếu shell bị chặn, tháo guard làm lọt |
| F15 | Đóng — lỗi 0/1/>1 và cộng nhiều nguồn không ghi đè |
| F16 | Đóng — bộ đúng cấu trúc sai kết quả bị từ chối |
| F17 | Đóng — CLI nhiều lỗi giữ bảng và chuẩn hoá rc |
| F18 | Đóng — N=8, đúng một lỗi, nhiều dòng/nhiều nguồn |
| F19 | Đóng — bảng giữ danh tính, thứ tự, chi tiết |
| F20 | Đóng — đảo bảng CLI bị bắt |
| F21 | Đóng — mọi record/lỗi, không ghi mảnh sai |
| F22 | Đóng — toàn 28 mutant TEP_TEST cũ và hai GOC trong mẫu; không thêm lỗi t52/t53/t54 |
| F23 | Đóng — nhiều ca bỏ qua, tên/lý do/số đếm không bị nén |
| F24 | Đóng lỗi gốc — strict int, symlink thật và mutant theo năng lực; cả lớp registry còn F40 |
| F25 | Đóng — chỉ argv[1] chọn cửa, đối số không chiếm dispatcher |
| F26 | Đóng — cửa không đối số gọi main và giữ rc |
| F27 | Đóng — k=0, path khác x, worker 1/khác 1, lỗi tự kiểm nhánh đủ |
| F28 | Đóng — default entry trên cấu hình hợp lệ du/gate/mảnh |
| F29 | Đóng — 27 ô và thứ tự thẻ lỗi; hai neo hiện duy nhất |
| F30 | Đóng — rc Git và grammar HEAD độc lập |
| F31 | Đóng — whitespace/case của gate không bị chuẩn hoá để nhận |
| F32 | Đóng — đúng độ dài 40/64 và lowercase ASCII hex |
| F33 | Đóng — toàn grammar k/N, biên số và path |
| F34 | Đóng — nguồn, lời gọi Git, ngoại lệ và bytes |
| F35 | Đóng lỗi gốc — phân hoạch/header/N/path/parent/IO; cả lớp registry còn F40 |
| F36 | Đóng — đủ r15/r15-extra qua 56 ca, fixture bytes độc lập và native t53 |
| F37 | Đóng lỗi gốc — bốn tên phía True và guard có răng trên cả True/False; tên mới phía False sinh F40 |
| F38 | Đóng theo phạm vi thu hẹp — giàn giáo gây lỗi đã gỡ; thuộc tính vắng là nợ ngoài phạm vi |
| F39 | Đóng phần lỗi đã loại theo quyết định chủ kho; bản vá sinh F40 trên miền thật còn trong phạm vi, nên lớp registry chưa đóng |

**Giới hạn:** Linux/Python 3.11.15; không đo Windows/Python 3.12 thật. EPERM được áp ở syscall, còn NotImplementedError là mô phỏng có đối chứng, không phải Windows. Không đo upload/download artifact trên GitHub, ruleset hoặc thời gian A9; không chạy GitHub CI. Không có phép A1 tám mảnh native đầy đủ 397. Các mức `qua`, `bo_qua`, `giet_that`, `tin_dung_gia` và lượt chưa hoàn tất/ngắt điều phối được giữ riêng. Reviewer OpenAI/Codex làm việc qua API và công cụ shell; không có attestation độc lập model/effort hoặc human audit trong bundle, không xác minh lời khai danh tính/effort executor.

verdict: changes_requested
reviewed_sha: 42f74db160762dcb6248e98e1ceb17a148194d28
