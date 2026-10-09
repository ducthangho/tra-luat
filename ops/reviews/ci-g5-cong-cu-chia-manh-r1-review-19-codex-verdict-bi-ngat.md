<!-- executor: luot 19 BI NGAT boi nen ("Selected model is at capacity", 17:16Z) SAU khi da ghi bang finding F41/F42 va HUONG 16; khong co dong chot cuoi. Noi dung duoi day la NGUYEN VAN. -->

# Cross-review độc lập packet #668 r1 g2 — lượt 19

verdict: dang_review
reviewed_sha: 9aaeb032556dbaae925316f4fe8d06d83cddbc1b

Phạm vi: chỉ đọc cây ứng viên; mọi đột biến trên bản sao `/tmp`. Không tạo payload ký tự điều khiển/ẩn; chạy phản chứng có sẵn. Miền mô phỏng xoá/đổi `os.symlink` bị loại theo quyết định chủ kho; vẫn đo symlink thật và EPERM syscall.

Reviewer: OpenAI/Codex qua API và công cụ shell (machine transport); không có attestation độc lập model/effort hoặc human audit. Không suy danh tính reviewer/executor từ tài khoản GitHub. Không chạy GitHub CI, không đăng/commit/push.

HƯỚNG 1: Neo hiện vật và chống dùng lại kết quả cũ
  giả thuyết : runner có cache hoặc đường cũ khiến kết quả không thuộc head đang review.
  lệnh       : git -C cay-kho rev-parse HEAD; git status --porcelain; sha256sum SPEC.md; inventory.py trên hai bản sao; dựng evidence-luot-19 chỉ từ script và dữ liệu đầu vào.
  output     : HEAD=9aaeb032556dbaae925316f4fe8d06d83cddbc1b; cây sạch; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15. Baseline 212 mutant/53 ca; head 398 mutant/56 ca; không mất mutant cũ, thêm 186. Runner đổi đường /tmp/review668-r18 sang /tmp/review668-r19, không chép JSON kết quả hoặc cache sample. Baseline clone riêng tại f8a7829cc44f296c25faf1a6439b603ba840f70b.
  kết luận   : KHÔNG PHẢI LỖI. Phạm vi 5 tệp và trần ~1.960 theo chỉ thị mới nhất của chủ kho; không dùng trần cũ trong SPEC để chặn phép review đã được giao.

HƯỚNG 2: Liệt kê trọn miền đọc chế độ và nguồn vân tay
  giả thuyết : bỏ một nhánh hoặc một thành phần grammar khiến chốt chỉ có tên mà không có răng.
  lệnh       : đọc _doc_che_do/_van_tay và oracle; chạy probe.py, domain.py, domain_check.py, extent.py, source_io.py; all-domain-mutations.json là hợp của bảy bảng r12/r13/r14/r14-extra/r14-artifact/r15/r15-extra (103 phép).
  output     : ĐANG ĐO; chưa coi tiến trình đang chạy là bằng chứng qua.
  kết luận   : KHÔNG ĐO ĐƯỢC ở thời điểm khối này được ghi; kết quả hoàn tất sẽ nối bên dưới.

Miền `_doc_che_do` (đầu vào thực là chuỗi từ môi trường, không mở thêm miền object tuỳ ý):

- Ba biến BK/MH/RA: vắng, rỗng, có; đủ tích 27 ô và thứ tự ưu tiên lỗi. MH vắng: RA có kể cả rỗng ⇒ C-ra-le; BK vắng ⇒ du; BK khác đúng `manh` ⇒ C-ban-kinh; đúng ⇒ gate. MH có: BK có kể cả rỗng ⇒ C-ca-hai trước grammar.
- `fullmatch`, không search/match hay trim; toán hạng k là `0` HOẶC `[1-9][0-9]?`; dấu chia đúng một `/`; N là `[1-9][0-9]?`. Kiểm từng vị trí chữ số ASCII, 0 dẫn đầu, 1/2/3 chữ số, chữ số Unicode, dấu âm/dương, dấu chia sai/thiếu/thừa, tiền/hậu tố, khoảng trắng và hoa/thường. Các fixture ký tự đặc biệt chỉ tái dùng dữ liệu có sẵn.
- Lấy group(1) cho k, group(2) cho N; đổi sang int; biên `2 <= N <= 16`, `k < N`; đo mọi cặp hợp lệ và biên ngoài. RA phải truthy sau khi grammar/range đã qua; path có dấu cách, khoảng trắng đầu/cuối hoặc thư mục con phải giữ nguyên. Trả đúng chế độ và tuple `(k,N,RA)`.

Miền `_van_tay`:

- Nguồn Git: chính argv `git -C str(GOC) rev-parse HEAD`, `capture_output=True`, `text=True`, `timeout=60`; không dùng cwd khác, ref khác hoặc hằng. rc đúng 0 mới lấy stdout; rc dương/âm với stdout đúng/sai/rỗng phải cho None. Bắt OSError và SubprocessError (gồm TimeoutExpired); trim stdout trước grammar.
- Hai nhánh regex độc lập `[0-9a-f]{40}` và `[0-9a-f]{64}` dưới fullmatch: đúng độ dài, ngắn/dài một hoặc nhiều ký tự; đủ chữ số 0..9 và a..f; A/F/g/z/underscore/chữ số Unicode tại đầu/giữa/cuối; nhiều token, prefix/suffix; chỉ lowercase ASCII hex. HEAD không hợp lệ ⇒ None, người gọi fail-closed.
- SHA256: đọc toàn bytes của chính TEP_TEST; hexdigest, không nguồn khác/đầu/cuối/độ dài cố định/chuẩn hoá văn bản. Fixture rỗng, nhỏ, non-ASCII, hoa/thường, spaces, 63/64/65, 4095/4096/4097/8193, source thật; dữ liệu CR/LF có sẵn. Đổi bytes giữ HEAD, đổi HEAD giữ bytes, kho không Git, Git SHA256 thật. Lỗi nguồn vắng/thư mục/OSError không được trả vân tay giả hợp lệ.

HƯỚNG 3: Danh mục đầy đủ dây nối main/dispatcher
  giả thuyết : một quyết định/đối số/đầu ra không được quan sát có thể làm main xanh mà thiếu đo.
  lệnh       : run_checklists.py (138 phép lượt 10); fields_full.py, novel_entry.py, partition_identity.py; các phép main trong r12; mỗi phép qua đủ 56 ca.
  output     : ĐANG ĐO; ma trận độc lập không dùng lời khai executor.
  kết luận   : KHÔNG ĐO ĐƯỢC ở thời điểm ghi; sẽ chốt bằng tập JSON đủ 56 tên ca cho mỗi phép.

Miền main/dispatcher phải được đối chiếu:

- Đọc cấu hình trước mọi hành động; ValueError ⇒ đúng chẩn đoán/rc=2; hai tiền kiểm theo đúng thứ tự, giữ tên/lý do; từng CA chạy đúng một lần đúng thứ tự. Phân biệt qua/BoQuaMoiTruong/AssertionError/Exception, giữ danh tính/lý do/số đếm/mẫu số/stdout.
- Mảnh: chọn đúng nhánh, truyền k/N/RA, phân hoạch đúng thứ tự; nền đỏ hoặc tiền kiểm bỏ qua ⇒ cleanup với None/lý do/vân tay rồi rc=1, không phóng con. Nền ca bỏ qua giữ ngữ nghĩa cũ. Nhánh xanh: tên, baseline rỗng và worker vào _phong_con; mỗi nhóm/rc/stdout/baseline vào receiver; giữ dữ liệu của mọi nhóm, lý do nhóm lỗi đầu (nguyên lý do + rc + đuôi stdout), nhóm trước/sau/cả hai lỗi. Writer nhận đúng k/N/path/tập tên/ket hoặc None/lý do/vân tay, in mọi dòng và chuẩn hoá rc khác 0. k=0, N=2/8/16, path khác x, worker 1/3.
- Đủ/gate: cổng cây thật GOC; tự kiểm phân hạng, giàn giáo; tên ca đỏ sorted vào báo cáo nền và song song; cộng mọi nguồn lỗi (0/1/>1 và nhiều nguồn), không ghi đè. Gate chỉ giao mảnh, đủ gọi bán kính với toàn DOT_BIEN/baseline/worker, xử lý mọi kết quả và dòng. Bảng cuối giữ đúng số liệu; hong/loi_db/tien_kiem_bo_qua/loi_cong đều tác động rc.
- Dispatcher: argv[1] chọn cửa; cờ ở tham số không chiếm cửa; --gop đúng arity/thư mục/vân tay/hàm/rc và giữ bảng/thứ tự; cửa không đối số gọi main đúng một lần, chuyển nguyên rc 0/1/2 trên cấu hình hợp lệ du/gate/mảnh và cấu hình hỏng.

HƯỚNG 4: Workflow — chạy phản chứng sẵn có, tháo chốt bản vá
  giả thuyết : lớp F1/F3/F10/F14 đã đóng bị mở lại.
  lệnh       : env.py python batch.py quick-jobs.json; workflow.py và workflow_ablation_extra.py trên cây /tmp/review668-r19.
  output     : gốc: F1 20/20, F3 28/28, F10 7/7, F14 5/5 bị chặn. Gỡ raw guard ⇒ 7 F10 lọt. Chỉ đổi splitlines vẫn bị raw guard chặn; đổi splitlines + gỡ raw guard ⇒ 27 F3 lọt. Gỡ execution guard ⇒ 13 F1 lọt; gỡ shell guard ⇒ cả 5 F14 lọt. Head registry: 1025/1025 phản chứng đỏ đúng, TỔNG ĐẠT.
  kết luận   : KHÔNG PHẢI LỖI; lớp workflow còn răng trong miền đã đo. Không tạo workflow/payload ký tự điều khiển hoặc ẩn mới.

Miền workflow: toàn 87 ca p668; hình dạng gate/probe/selftest, env cấp workflow/job/step, defaults/shell/working-directory, container, runs-on, needs/if, matrix OS và k/N, fail-fast, thứ tự bước thiết lập, checkout/ref, phiên bản Python/action, upload/download/name/path/pattern theo cùng OS, không bước/with/env thừa; raw run được kiểm trước bỏ chú thích và chỉ tách LF. `actionlint` chạy trên YAML thật, không chỉ dữ liệu parse.

HƯỚNG 5: Hồi quy gate và công cụ — kết quả sớm
  giả thuyết : bản vá F40 làm gate/cổng phụ đỏ hoặc chỉ xanh nhờ mã thoát.
  lệnh       : env.py python run_regression.py; Ruff so theo (tệp, mã F, thông báo), baseline/head riêng.
  output     : gate rc=0, 352,9s, 56/56 đạt, bỏ qua=0, tiền kiểm bỏ qua=0; N126 ĐẠT; cổng cây thật ĐẠT; 398 mutant giao mảnh, lỗi đột biến=0. t152, lease t24/t31/t35/t161/t162, actionlint và probe kiem-tra --json đều rc=0 ở hai vế. Ruff mỗi vế 6 F841, added=[] và removed=[]. Head registry 1025/1025; baseline lần đầu 937/938, riêng p637-A3c-chau-setsid-thoat-nhom-van-bi-bat LỌT (đang đối chứng, giữ log gốc).
  kết luận   : KHÔNG PHẢI LỖI mới của packet ở gate/cổng phụ; không dùng gate giao mảnh thay bằng chứng bán kính. Registry baseline chưa được gọi là qua lần đầu.

HƯỚNG 6: Đóng trọn lưới chế độ/HEAD/bytes và hình dạng artifact
  giả thuyết : có biên ngoài các ví dụ đơn lẻ bị nhận sai.
  lệnh       : probe/domain/domain_check/extent/source_io/schema_io/mode_domain/partition_roundtrip trong quick-jobs.json.
  output     : MODE_SPEC 458 PASS; HEAD_SPEC 275 PASS; NUMERIC_GRID 135 nhận/10.681 từ chối, 11 grammar âm, mismatch=[]; lưới 27 ô và rc×stdout có oracle. 13 fixture bytes × 10 phiên bản; nguồn vắng/thư mục/lỗi đọc đều ném OSError, không có vân tay giả. Round-trip từng N=2..16: coverage 398, disjoint True, gom_errors 0, table_order True. 214 neo ops/cong_cu_test.py đều duy nhất; ba neo bash_nen.py lặp 2/2/3 cũng đúng số ấy ở baseline.
  kết luận   : KHÔNG PHẢI LỖI hành vi trên lưới. Răng qua 56 ca của các bảng đột biến vẫn chờ hoàn tất, chưa chốt lớp từ lưới hành vi đơn thuần.

HƯỚNG 7 (MỚI): Hash seed khác nhau giữa các job
  giả thuyết : cùng HEAD/bytes nhưng thứ tự registry/phân hoạch phụ thuộc PYTHONHASHSEED, làm gom nhận sai hoặc đỏ oan.
  lệnh       : check.py novel-probes.json, mục hash_seed; năm tiến trình Python mới với seed 0/1/42/314159/random.
  output     : PASS; 5 registry đều đúng 398 tên theo cùng thứ tự; 675 phân hoạch (135 × 5) bằng oracle list(DOT_BIEN)[k::N]; mọi vân tay bằng nhau. evidence-luot-19/hash-seed.json.
  kết luận   : KHÔNG PHẢI LỖI. Đây là đo môi trường tiến trình thật, không giả lập thứ tự dict.

HƯỚNG 8 (MỚI): Git linked worktree có .git là tệp và HEAD riêng
  giả thuyết : _van_tay vô tình đọc HEAD của kho chính thay vì worktree, cho artifact cũ qua sau đổi HEAD riêng.
  lệnh       : check.py novel-probes.json, mục linked_worktree; clone tạm, git worktree add --detach, empty commit riêng, source path có khoảng trắng.
  output     : PASS; .git là file; trước/sau: bytes SHA giữ nguyên, HEAD worktree đổi, HEAD kho chính không đổi. Bộ hai mảnh dựng bằng vân tay trước gom xanh với vân tay trước, bị G-van-tay với vân tay sau. evidence-luot-19/linked-worktree.json.
  kết luận   : KHÔNG PHẢI LỖI. Bản ghi ở phép này là dữ liệu dựng, không tính vào bán kính native.

HƯỚNG 9: Registry năng lực trên nền bị EPERM ở syscall
  giả thuyết : F40 chỉ có răng phía True hoặc phần thu hẹp làm sai nền không có quyền symlink.
  lệnh       : REVIEW_CAP=denied env.py python system_probe.py check.py capability-probes.json; baseline-probes.json cùng syscall filter.
  output     : _CO_SYMLINK=False, registry=395, os.symlink vẫn builtin_function_or_method. Nền 56 ca: t51 tin_dung_gia và t46 bo_qua; hai trạng thái này cũng có ở baseline. f24_kieu_phien_ban/f24_kieu_so_manh/f37_dk_dao/f37_dk_luon_dung/f40_false_khong đều chỉ THÊM t52 giet_that ngoài hai trạng thái nền. Không xoá/đổi os.symlink, không nạp lại module nhiều trạng thái.
  kết luận   : KHÔNG PHẢI LỖI ở phép vá gốc F40 phía False. Chưa dùng kết quả này để khẳng định mọi đăng ký mới của lớp đã được quan sát.

HƯỚNG 10: Tập quan sát còn bỏ sót chính hai tên f40 mới
  giả thuyết : f40_false_luon/f40_false_khong đăng ký có điều kiện nhưng không thuộc _TEN_SL/_TEN_SL_FALSE; đăng ký sai miền hoặc mất tên có thể qua t52.
  lệnh       : r19-registry-mutations.json; measure.py ... target, rồi đo đủ 56 ca độc lập ở registry-real/ và registry-denied/.
  output     : Bốn phép ca đích trên nền thật đều qua: meta_false_unconditional, meta_false_removed, meta_true_removed, meta_true_unconditional. Hai phép trên miền không tương đương cần kết quả đủ 56 ca trước khi chốt: đưa f40_false_khong ra ngoài khối False trên nền True; đưa f40_false_luon ra ngoài khối True trên nền EPERM. Phép xoá tên cũng đang đo ở đúng miền đăng ký.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận cuối lớp ở thời điểm ghi; dấu hiệu thiếu răng đã tái hiện, chưa tính phép tương đương làm finding.

HƯỚNG 11: Xác nhận F41 bằng đủ 56 ca ở cả hai miền
  giả thuyết : thiếu tên f40 trong tập quan sát chỉ là chi tiết không có hệ quả.
  lệnh       : registry-real/measure.py và system_probe.py registry-denied/measure.py, cùng r19-registry-mutations.json; so trạng thái từng tên ca với capability-real/denied.
  output     : Nền có symlink: 4/4 phép qua 56/56. Trong đó meta_false_unconditional thêm f40_false_khong sai miền và meta_true_removed làm mất f40_false_luon là KHÔNG tương đương. Nền EPERM: cả 4 phép không thêm bất kỳ ca đỏ nào so nền (t51 tin_dung_gia, t46 bo_qua); meta_true_unconditional thêm f40_false_luon sai miền và meta_false_removed làm mất f40_false_khong là KHÔNG tương đương. Mỗi JSON có đủ đúng 56 tên ca. Các phép còn lại là đối chứng tương đương trên miền đó, không tính lỗi.
  kết luận   : LỖI (P2), F41 — lớp registry năng lực CHƯA ĐÓNG. Đây là thuộc tính/callable os.symlink thật trên True và syscall EPERM trên False; không dùng miền thuộc tính vắng/nạp lại đã loại. Bản vá F40 bắt được lỗi cũ nhưng tạo thêm hai đăng ký điều kiện ngoài tập quan sát.

F41 — HINT PATCH (đang đo trên bản sao): **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**.

Tệp `ops/cong_cu_test.py`, `_TEN_SL`/`_TEN_SL_FALSE` phục vụ `t52` và `_in_tu_kiem_gom`: đưa TOÀN BỘ tên có điều kiện hiện tại vào hai tập oracle. Hiện có đúng **5 tên True** (f24_nhan_symlink, f35_writer_broken_link, f37_bo_f24, f37_bo_f35, f40_false_luon) và **2 tên False** (f37_dk_luon_dung, f40_false_khong). Không cần thêm giàn giáo nạp lại hoặc phát sinh thêm một tầng mutant có điều kiện để vá lần này.

```diff
-_TEN_SL = ("f24_nhan_symlink", "f35_writer_broken_link", "f37_bo_f24", "f37_bo_f35")
+_TEN_SL = ("f24_nhan_symlink", "f35_writer_broken_link", "f37_bo_f24", "f37_bo_f35", "f40_false_luon")
-_TEN_SL_FALSE = ("f37_dk_luon_dung",)
+_TEN_SL_FALSE = ("f37_dk_luon_dung", "f40_false_khong")
```

Miền đủ của lớp: True có đúng 5/vắng cả 2 False; False có đúng 2/vắng cả 5 True. Kiểm danh tính, không tổng số. Giữ `_CO_SYMLINK` do probe thật quyết định; t52 trước/sau không mutant phải qua; từng điều kiện phía True/False và từng tên đăng ký phải được quan sát. Nếu sau này thêm mutant chỉ sống ở một miền, thêm tên đó vào oracle trong cùng thay đổi. Không mở lại AttributeError/thuộc tính vắng.

Các phép bắt buộc giết ở t52: (1) bỏ khối False trên False, mở khối False trên True — F40 hiện có; (2) đưa riêng assignment f40_false_khong ra cột 0 trên True; (3) xoá tuple f40_false_luon trong vòng đăng ký True trên True; (4) thêm assignment f40_false_luon ngoài điều kiện trên False; (5) xoá assignment f40_false_khong trên False. Neo/thay đầy đủ, duy nhất ở `r19-registry-mutations.json`; bốn tên f24/f35/f37 True và tên f37 False cũng phải giữ răng. Đối chứng các phép tương đương trên miền đối diện phải không sinh đỏ oan.

Rủi ro bán kính: không đăng ký một phép chỉ có nghĩa trên True vào False hoặc ngược lại; không thêm kiểm này sang t53/t54. Hint chỉ mở rộng hai tuple quan sát, không thay probe/registry/thuật toán gom/mảnh nên không tạo vòng đăng ký tự sinh. Đo đủ 56 ca cho bốn phép không tương đương; so delta với nền EPERM, không coi t51/t46 sẵn có là giết thật. Mẫu mutant cũ tráo TEP_TEST/GOC phải giữ ba ca mới qua.

HƯỚNG 12: Hệ quả F41 và kiểm hint hai chiều
  giả thuyết : tên bỏ ngoài tập quan sát không thể làm bán kính sai, hoặc hint mở rộng tuple sẽ giết oan.
  lệnh       : check.py expanded-probes.json; hint-real/measure.py và system_probe.py hint-denied/measure.py; hint-validation.json ở cả hai nền.
  output     : Cây đột biến meta_false_unconditional có 399 mutant, _CO_SYMLINK=True; chính f40_false_khong thừa sống 56/56, errors=1. Hint hai tuple: bốn phép không tương đương đều chỉ thêm t52 giet_that qua đủ 56 ca; t52/t53/t54 không mutant đều qua ở cả True/EPERM. Mọi mutant F37/F40 hiện có bị t52 giết ở đúng miền; bốn đối chứng tương đương vẫn qua. Raw: expanded-registry.json, hint-real/measure-*.json, hint-denied/measure-*.json, hai validation.json.
  kết luận   : LỖI (P2) F41 có hệ quả đo được và hint hẹp đã được kiểm. Không gọi bán kính của head 398 là đỏ từ phép này: lỗi ở head là chốt không phát hiện đăng ký sai; 399 là cây phản chứng.

HƯỚNG 13 (MỚI): Miền GIÁ TRỊ truyền qua main, ngoài vài ví dụ của t54
  giả thuyết : biết truyền đúng tham số tại k=0/1/3/5, N=2/8/16, worker=1/3 và path thường chưa chứng minh truyền nguyên miền hợp lệ.
  lệnh       : measure.py r19-main-mutations.json (bốn phép đầu) và r19-main-path-mutations.json (hai phép sau), đủ 56 ca mỗi phép; check.py main-domain-probes.json, 173 ô cho mỗi phiên bản.
  output     : CẢ SÁU phép sống 56/56: main_k_mod_eight, main_n_power_two, main_shard_worker_cap_three, main_full_worker_cap_three, main_path_strip, main_path_lower. Lưới mới: mọi 135 cặp 2≤N≤16, 0≤k<N; worker 1..16 ở cả đủ/mảnh (32 ô); sáu path thường/khoảng trắng/hoa-thường/non-ASCII/thư mục con. Control cả 173 ô rc=0. Số ô khác control lần lượt 58/105/13/13/2/2.
  kết luận   : LỖI (P2), F42 — lớp main/dispatcher CHƯA ĐÓNG ở miền bảo toàn GIÁ TRỊ đầu vào; không phải lỗi thuật toán hiện tại. Checklist cũ vẫn cần hoàn tất, nhưng việc nó xanh không đóng được miền chưa có ca.

Phản chứng cụ thể (trace của main thật chạy trong giàn giáo sẵn có, dữ liệu ở main-domain.json):

- `k, n, ra = tham_so` → thêm `k %= 8`: input 8/9 thành `ghi:0/9:x:False:dung:none:True` và phóng sai tập tên; mong `ghi:8/9:x:True:dung:none:True`.
- Cùng neo → thêm `n = 1 << (n.bit_length() - 1)`: 0/3 thành 0/2, phóng sai phân hoạch. Các N của t54 hiện tại đều là luỹ thừa hai nên không phân biệt.
- Worker vào `_phong_con` hoặc biến `so_tien_trinh` ở nhánh đủ → kẹp `min(3, ...)`: worker 4..16 bị truyền thành 3, dù API helper cho phép tới 16. t54 chỉ đặt 1 và 3.
- Cùng neo tuple → `ra = ra.strip()` hoặc `ra = ra.lower()`: path ` space ` thành `space`; `Mixed.TXT` thành `mixed.txt`. t53 đo bộ đọc và t52 đo bộ ghi, nhưng cả hai không đi qua dây main này.

**F42 — HINT PATCH:** **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Thiết kế dưới đây đã được hiện thực trên bản sao bằng `hint-main-data.json`; kết quả kiểm bản hint được nối ở H16, không tính vào kết quả của head.

Sửa `ops/cong_cu_test.py`, `_in_tu_kiem_main` và `t54_main_chon_DUNG_vong_ban_kinh_theo_che_do`; giữ thuật toán `main` đang đúng. Thêm bảng dữ liệu đầu vào cho dây nối, không thêm một ca CA mới:

1. 135 dòng `(che_do='manh', k, N, RA='x', worker=3)` phủ toàn miền hữu hạn k/N. Không chỉ thêm 8/9 và 0/3.
2. 16 worker từ 1 tới `_TRAN_TIEN_TRINH` ở cả `du` và `manh` (mảnh nên dùng 9/16); giữ các ca tiền kiểm/lỗi và worker hiện có.
3. Path có khoảng trắng đầu/cuối, path toàn dấu cách, chữ hoa/thường trộn, non-ASCII, thư mục con có dấu cách, path thường. Dùng nguyên path vào kỳ vọng `ghi`, không gọi strip/lower/Path.resolve ở oracle.
4. Giữ kiểm nguyên nhật ký và stdout như t54 đang làm: thứ tự ca/tiền kiểm, `phong` có đúng tên và worker, `ghi` có đúng k/N/RA/records/reason/fingerprint, đủ/worker có đúng toàn registry, mọi dòng và rc. Bảng `mong_manh` cần mở từ bốn cặp hiện tại sang đủ 135 cặp.

**Cách cô lập bán kính bắt buộc:** các dòng thêm nhằm đo main BẢO TOÀN kết quả của dependency. Trong riêng các dòng mới, tạm đặt `_doc_che_do` trả tuple thử đã biết (hoặc `('du', None)`), và `_so_tien_trinh_ban_kinh` trả worker thử; gọi main thật, khôi phục hai hàm bằng finally. Các ca cũ, nhất là cấu hình hỏng, vẫn dùng bộ đọc thật. Nếu chỉ thêm path/k/N vào env rồi dùng mọi dependency thật, mutant chuẩn thuộc t53 như đổi path/group trong `_doc_che_do` có thể giết thêm t54: đó là bán kính 2, không phải hint đạt. Tương tự không kéo mutant helper worker/partition của ca cũ sang t54; phân hoạch/kỳ vọng đếm có thể tiếp tục dựa trên cùng `_phan_manh` như giàn giáo hiện tại, còn oracle độc lập của phân hoạch nằm ở t52.

Sáu neo→thay trong `r19-main-mutations.json` phải chết ĐÚNG t54. Giữ các mutant F2/F5/F6/F7/F12/F15/F18/F23/F27/F28 và dispatcher hiện có; đo lại cả 56 trạng thái cho sáu phép mới, các mutant chuẩn t53 làm đổi tuple/path và helper worker, cùng mẫu cũ tráo TEP_TEST/GOC. Không sinh mutant cho từng 135 giá trị; các phép có tính hệ thống modulo 8, làm tròn N, kẹp worker, chuẩn hoá path đủ phân biệt các chiều, bảng dữ liệu hữu hạn đóng miền giá trị của dây nối.

HƯỚNG 14: Đối chứng baseline registry và giới hạn phép đo
  giả thuyết : một lỗi hạ tầng cũ bị gán nhầm cho bản vá.
  lệnh       : chạy lại nguyên registry baseline bằng env.py; so các log regression hai vế; đối chiếu input-coverage.json.
  output     : baseline lần hai rc=0, 938/938 đỏ đúng, TỔNG ĐẠT; head lần đầu 1025/1025. Log lần đầu 937/938 được giữ nguyên. Sáu bảng đột biến r12/r13/r14/r14-artifact/r15/r15-extra bằng nguyên dữ liệu đầu vào gốc (7/4/52/22/6/3 mục); không bỏ/sửa neo để làm kết quả xanh.
  kết luận   : KHÔNG PHẢI LỖI mới chứng minh được của packet. Không đổi kết quả lần đầu thành pass; ghi riêng lần đối chứng.

HƯỚNG 15: Biến thể workflow mới chỉ mô tả bằng lời
  giả thuyết : một BOM Unicode ở vị trí không phải đầu tệp có thể gây lệch giữa nhìn thấy lệnh và tên lệnh Bash thực thi.
  lệnh       : không dựng/chạy payload; đọc raw predicate và whitelist, đối chiếu phép tháo guard H4.
  output     : đề nghị executor đặt U+FEFF ngay trước chữ đầu của lệnh Python trong thân run, rồi đối chứng đặt cùng ký tự bên trong một chú thích bình thường. Dự kiến Bash ở trường hợp đầu coi BOM là phần tên lệnh và không tìm được lệnh; trường hợp sau vẫn là chú thích. Validator phải từ chối ký tự không in được trước khi bỏ chú thích, độc lập cơ chế whitelist lệnh. Không có lệnh giấu được soạn trong lượt này.
  kết luận   : KHÔNG ĐO ĐƯỢC fixture mới này; chỉ là hướng kiểm bổ sung theo phân công. Không tính vào 87 ca đã chạy và không mở finding dựa trên suy đoán.

Điều phối bán kính: vòng native_all 398 được ngắt bằng SIGINT (rc=130) để ưu tiên mẫu cố định 176 của sample_run.py; chỉ JSON đã hoàn tất đủ 56 tên được giữ. Mẫu gồm toàn bộ đích t52/t53, các họ main/dispatcher t54 có chủ đích và mutant cũ tráo TEP_TEST/GOC/công cụ. Tám phép native năng lực đã đo đầy đủ trong chính lượt 19 được tái dùng từ capability-real.json (reuse-native.json ghi tên), không phải cache lượt cũ. Không tính tiến trình đang chạy, JSON dở hoặc rc=130 là pass.

| Finding mới | Lớp | Mức | Tệp:dòng | Mô tả | Phản chứng |
|---|---|---|---|---|---|
| F41 | Registry năng lực artifact | P2 | ops/cong_cu_test.py:7402, :7410, :7581, :6781 | Hai tên f40 mới ngoài oracle; mất tên/đăng ký sai miền qua suite | r19-registry-mutations.json; registry-real/ và registry-denied/; expanded-registry.json: 399 mutant, mutant thừa sống 56/56 |
| F42 | Main/dispatcher — bảo toàn giá trị | P2 | ops/cong_cu_test.py:6920, :7921, :7957 | t54 chưa phủ k≥8, N không là luỹ thừa hai, worker≥4, path có khoảng trắng/hoa; sáu phép đổi sống | r19-main-mutations.json; measure-main_*.json: 56/56 qua; main-domain.json: 173 ô, sáu sai lệch hệ thống |

HƯỚNG 16: Hiện thực và đo hint F42 trên bản sao
  giả thuyết : lưới đầy đủ có thể đóng F42 mà không làm rộng bán kính hoặc sửa main đang đúng.
  lệnh       : áp hint-main-data.json vào /tmp/review668-r19-hint-main; hint-main/check.py hint-main-probes.json; hint-main/measure.py mutations.json; hint-main-collateral.json.
  output     : Nền hint 56/56 qua. Cả sáu phép F42 qua đủ 56 ca đều chỉ t54 giet_that. f33_output_trim, f9_sha_hang, t45_cong_khong_noi trong đối chứng native đều errors=0 và t54 qua; đối chứng GOC cuối đang chạy tại thời điểm ghi. Hint thêm bảng 173 ô, riêng ô mới stub bộ đọc/worker và khôi phục finally; trường hợp cũ giữ nguyên. Artifact goi-y-F42.patch (+30/-3 so head), goi-y-F41.patch (+2/-2) có nhãn chưa chạy cây thật.
  kết luận   : KHÔNG PHẢI LỖI của hướng hint trong phần đã đo; F42 của head vẫn mở. Không suy từ hint đã qua thành source ứng viên đã được sửa.

Kiểm trọn danh tính registry còn trong phạm vi: các mutant chuẩn F37 bỏ f24/f35 đã giết đúng t52; hai phép bỏ tên f37_bo_f24/f37_bo_f35 trong registry-extra-mutations.json cũng bị t52 giết. Trên EPERM, bỏ riêng tên f37_dk_luon_dung bị t52 giết. Hai tên f40 là toàn bộ phần tên có điều kiện còn lọt; đã đo cả mất tên và đăng ký nhầm miền ở H11, hint hai phía ở H12. Không có nhu cầu thêm tầng mutant có điều kiện mới để sửa F41.
