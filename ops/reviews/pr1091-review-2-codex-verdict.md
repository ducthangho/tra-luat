verdict: approve
reviewed_sha: 90b3f1cd9ff8a3459285796da37dc96b8553690e
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Đã hoàn tất kiểm tra độc lập theo runs/4eb21f94/prompt.snapshot. Chỉ đọc cây cay-kho; mọi probe/đột biến chạy trên bản sao. Không gọi mạng. Hành vi Windows native (icacls/NTFS) không đo được trong môi trường Linux này.

## Hướng 0 — Mỏ neo, phạm vi và tính độc lập

- Giả thuyết: cây nguồn, snapshot hoặc diff không khớp exact SHA được giao.
- Lệnh: đọc snapshot, `cay-kho/AGENTS.md`, CONTEXT/protocol/CLAUDE và hợp đồng provider có liên quan; `git --no-optional-locks -C cay-kho rev-parse HEAD origin/master HEAD^{tree}`, `status --porcelain=v1 --untracked-files=all --ignored`, `rev-parse --is-shallow-repository`, `config core.abbrev`; so byte diff và prompt bằng Python (lưu `evidence/preflight.json`).
- Output: HEAD `90b3f1cd9ff8a3459285796da37dc96b8553690e`; base `90c101b8d1f8895b66607de8582a18c5e72d834c`; tree `b077af062b784383994a556f165e54abb947fcf2`; detached HEAD, shallow=false, core.abbrev=7, status rỗng; diff.patch và prompt.snapshot khớp byte. Write set review đúng hai tệp ops/vm; delta sản phẩm +8/-1, test +65/-7 so master.
- Kết luận: KHÔNG PHẢI LỖI. Chỉ thị trực tiếp là authority cho review ngoại tuyến; không thao tác lease/GitHub/land. Reviewer Codex, provider `openai_codex`, model_family `openai`, execution_surface lúc ghi ban đầu suy là `codex_service` (đính chính thành `codex_cli` theo metadata launcher tại Hướng 2), transport `machine`; phiên độc lập với executor, không fork context executor. Model/effort phục vụ cụ thể và identity executor KHÔNG ĐO ĐƯỢC bằng công cụ phiên này; không tự cấp assurance/receipt vận hành. Cây nguồn chỉ đọc theo thao tác reviewer, sandbox workspace có khả năng ghi nên không nhận là mount read-only.

## Hướng 1 — Bộ test bắt buộc trên HEAD

- Giả thuyết: số 118/118 executor khai không tái lập trên cây hiện tại.
- Lệnh: `TL_TEST_PYTHON=python3 PYTHONDONTWRITEBYTECODE=1 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/head-tests.log 2>&1`; lưu mã thoát ở `evidence/head-tests.rc`.
- Output thật: `cap-nhat-cong-cu tests: 118/118 ca QUA`; rc=0. Không có ca skipped trong tổng kết này.
- Kết luận: KHÔNG PHẢI LỖI trong suite Linux ở exact reviewed_sha. Windows native và kết quả VM executor thuật lại: KHÔNG ĐO ĐƯỢC ở đây, không được cộng vào số test reviewer đã đo.

## Hướng 2 — Provenance của vá test và hợp đồng đã chốt

- Giả thuyết: executor áp hint thiếu/khác hoặc thay sản phẩm ngoài delta đã khai.
- Lệnh: lấy Git blob test tại `d58d649ff061ff125bc004414ed4a0787de8e5f3` vào `copies/provenance/`, áp `luot1/HINT.patch` bằng `patch -p0 --batch`, so byte với test HEAD; so blob sản phẩm hai SHA và `git diff d58d649...HEAD` với `diff-tu-luot1.patch`. Output lưu `evidence/provenance.json` và `provenance-apply.log`.
- Output: patch rc=0, không fuzz/reject; HEAD test bằng byte old+hint; sản phẩm bằng byte lượt 1; diff giữa hai head khớp tệp giao. Đã đọc `verdict-luot16.md` để giữ các hợp đồng nền, không lấy approve lịch sử làm bằng chứng cho thay đổi mới.
- Kết luận: KHÔNG PHẢI LỖI về delta/provenance đo được. `hint_provenance` do snapshot khai; handoff/biên nhận GitHub không kèm để kiểm độc lập, nên không chứng nhận metadata từ xa. Đã làm theo hint chưa đủ đóng finding; tiếp tục chạy mutant/oracle.

Bổ sung nhận dạng sau khi đọc `runs/4eb21f94/run.json`: metadata launcher khai `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, khởi động qua chương trình `codex`. Dùng surface `codex_cli` theo bằng chứng launcher này; tên `codex_service` trong Hướng 0 là suy luận ban đầu từ API/tool và được đính chính ở đây. Không suy model/effort thực phục vụ từ tên chương trình.

## Hướng 3 — ACL, kế thừa, thứ tự và các biên Windows

- Giả thuyết: reset kế thừa từ Program Files làm Users ghi được; reset/chép sai thứ tự hoặc bỏ sót cây lồng/ẩn; lỗi native bị nuốt.
- Lệnh: đọc có số dòng `ops/vm/cap-nhat-cong-cu.ps1:172–235,595–700`, test `:946–1045,1087–1103`, README và diff. Chạy lại nguyên văn `luot1/probes/native-wrapper.ps1` trên `copies/head/ops/vm/cap-nhat-cong-cu.ps1`, lưu `evidence/native-wrapper.{log,json,rc}`.
- Output thật wrapper: `Wrapper/argv: 3/3 PASS; enumeration Linux: 1/1 PASS; native Windows: KHONG_DO_DUOC`, rc=0. Executable shim nhận đúng một đối số `<install [x]>/*` nguyên vẹn và `/reset /T /C /L /Q`; native rc=1 và 5 đều ném, rc=0 không ném. Enumeration Linux có 3 nút thường, 4 khi Force, gồm `.hidden`, `noextension`, `normal.txt`, `nested`.
- Phân tích tĩnh: thứ tự là tạo thư mục → Assert-KhongReparse (tổ tiên, gốc, Recurse/Force) → setowner toàn cây → đặt ACL riêng root, bỏ kế thừa và grant SYSTEM/Administrators F, Users RX → nếu có con thì reset `<root>/* /T /C /L /Q` → chép ba tệp → setowner toàn cây lần nữa → đo owner/bit ghi bốn nút (root + ba tệp) và băm từng tệp → đăng ký tác vụ. `/reset` không nhắm root nên root vẫn chặn kế thừa từ Program Files. Với ACL root đạt yêu cầu, nguồn kế thừa con là root đã khóa, qua cha trực tiếp ở mỗi cấp; grant Users RX không chứa bit ghi.
- Phạm vi: phép đếm chỉ trả lời có con trực tiếp hay không, không cần bằng số nút icacls xử lý. Force cần cho hidden/system ở PowerShell; `/T` chịu trách nhiệm cây lồng của icacls, `/L` là thao tác chính liên kết. Assert từ chối reparse trước mọi lệnh ACL. Wrapper không nuốt rc khác 0 dù có `/C`; `$ErrorActionPreference='Stop'` và catch đăng ký sẽ đưa lỗi enumeration/copy/icacls ra mã 6.
- Điều kiện kế thừa: `/inheritance:r /grant:r` không có nghĩa xóa mọi explicit ACE khác ở root. Mô hình test xóa toàn Access ở nhánh inheritance chỉ là xấp xỉ, không chứng minh root tùy ý được tẩy sạch. Chốt bit ghi ở root/ba tệp sẽ từ chối ACE Allow ghi không tin cậy còn lại. Chốt không đo quyền đọc dương hay mọi hậu duệ; các giới hạn nền này không được biến thành tuyên bố chứng nhận NTFS toàn cây.
- Kết luận: KHÔNG PHẢI LỖI về cấu trúc thứ tự/nguồn kế thừa, chuyển argv và xử lý rc đã đo trên Linux. Native icacls wildcard với Hidden/System, tệp không đuôi/tên dài, thứ tự truyền DACL thật, thư mục con không thể duyệt, sharing lock, privilege setowner khi DACL rỗng và race: KHÔNG ĐO ĐƯỢC. Tệp dấu chấm Linux không thay thế thuộc tính Hidden/System Windows; lỗi giữa chừng có thể để lại cây đổi một phần, không có hợp đồng rollback ở delta này. Không nhận lời thuật VM là phép đo reviewer.

## Hướng 4 — Tái chạy probe và đột biến lượt 1 trên bản sao HEAD

- Giả thuyết: vá test chỉ thêm ca xanh, ba đột biến cũ vẫn lọt.
- Lệnh: `python3 -B probes/mutations.py > evidence/mutations-driver.log 2>&1` (rc driver ở `mutations-driver.rc`). Probe được sao từ `luot1/probes/mutations.py` ra thư mục `probes/` ngang cấp cay-kho để ROOT trỏ đúng nguồn hiện tại; chỉ thay đúng mỏ neo reset từ `$AclGia[$goc]` thành `$AclGia[(Split-Path -Parent $key)]` vì HEAD đã đổi dòng ấy. Diff thích nghi ở `evidence/mutations-adaptation.patch`. Mỗi ca chạy suite trên một bản sao năm tệp ở `copies/<tên>/`; delta, log, rc, số ca và băm riêng ở `evidence/<tên>.patch`, `.log`, `mutations.json`. Không sửa nguồn hay hiện vật lượt 1.
- Output thật: control 118/118 rc0; 13 mutant đều khác byte và không ParserError; 12 bị bắt, 1 sống sót. Chi tiết:

| Mutant | N/M | rc | Ca trọng tâm đỏ / ý nghĩa |
| --- | --- | --- | --- |
| old_T_no_reset | 114/118 | 1 | grant, đăng ký lại, DACL rỗng, cây lồng |
| no_reset | 115/118 | 1 | đăng ký lại, DACL rỗng, cây lồng |
| reset_no_T | 117/118 | 1 | `dk_chay_reset_ca_cay_long_va_tep_an` |
| reset_no_L | 117/118 | 1 | ca đăng ký lại kiểm argv `/L` |
| reset_before_grant | 115/118 | 1 | đăng ký lại, DACL rỗng, cây lồng |
| reset_after_copy | 116/118 | 1 | ca clean install + DACL rỗng |
| reset_after_copy_cached_condition | 117/118 | 1 | `dk_chay_sua_tep_dacl_rong_truoc_khi_chep` |
| grant_with_T_and_reset | 117/118 | 1 | ca grant cấm `/T` |
| reset_root_instead_of_children | 115/118 | 1 | đăng ký lại, DACL rỗng, cây lồng |
| no_final_setowner | 110/118 | 1 | chủ sau chép không đạt |
| users_modify | 110/118 | 1 | chốt bit ghi từ chối |
| model_reset_noop | 116/118 | 1 | cả hai ca mới |
| model_copy_no_denial | 118/118 | 0 | HEAD reset trước copy nên nhánh từ chối không cần chạy |

- Kết luận: KHÔNG PHẢI LỖI; ba mutant làm cơ sở finding lượt 1 đều bị bắt đúng ca do trạng thái/hành vi. Mutant bỏ từ chối copy của đồ giả sống sót không tự chứng minh lỗi sản phẩm hay fixture: với sản phẩm lành, reset đã chữa ACL trước khi copy. Không đếm mutant này là finding mới. Các ca chỉ kiểm argv (như `/L`) không được trình bày thành phép đo native tác dụng của cờ ấy.

## Hướng 5 — Đối chứng trạng thái bằng probe lượt 1 và mô hình hiện tại

- Giả thuyết: suite đỏ vì assertion hình dạng thay vì hậu điều ACL/reset, hoặc mô hình mới vẫn gán mọi hậu duệ trực tiếp từ root.
- Lệnh: `python3 -B probes/state-probes.py > evidence/state-probes-driver.log 2>&1`, rc=0. Driver gọi nguyên văn `luot1/probes/state-original-model.ps1` và `state-recursive-model.ps1` với `-Product copies/<mutant>/ops/vm/cap-nhat-cong-cu.ps1`; đồng thời dùng `probes/state-head-model.ps1` trích fixture/đồ giả từ test HEAD hiện tại, giữ nguyên đuôi xuất JSON của probe cũ. Không chạy chồng thao tác thêm fixture/hint của script lượt 1 lên HEAD đã có fixture; Hướng 2 đã kiểm hiệu lực hint từ blob cũ. JSON/command ở `evidence/state-probes.json` và từng `<tên>.json`.
- Output thật: 9/9 harness rc0, nhưng oracle đọc trạng thái/lỗi bên trong, không coi rc0 của harness là đăng ký thành công:
  - HEAD + DACL ba tệp rỗng: tới dấu dừng trước mật khẩu, tasks=1, bốn nút không grant ghi lạ.
  - Bỏ reset, reset sau copy, reset sau copy có cache điều kiện: AccessDenied ở tệp đầu chép, tasks=0. Không tới đo ACL/đăng ký.
  - HEAD + cây chín nút: tasks=1, 0 nút có grant ghi lạ.
  - Mutant không `/T`: mô hình gốc lượt 1 vẫn báo 0 nút xấu; mô hình sửa lượt 1 và mô hình hiện tại đều báo đúng **3 nút** còn Users Modify. HEAD chạy mô hình sửa lượt 1 cũng báo 0.
- Kết luận: KHÔNG PHẢI LỖI ở HEAD; phép đối chứng tái tạo được thiếu sót mô hình cũ và phân biệt được mô hình mới. Mô hình hiện tại duyệt theo độ dài đường dẫn từ cha xuống con, đọc ACL cha trực tiếp, chỉ chọn con trực tiếp khi thiếu `/T`, và dùng Test-Path Leaf để phân biệt tệp/thư mục khi xử lý `(OI)/(CI)`. Bảng ACL không giữ inheritance flags/IsInherited hay tự lan truyền khi sửa cha; coi các nút ban đầu là độc lập/protected để đo nhu cầu reset tường minh. Đây là mô hình giới hạn, không mô phỏng đủ NTFS. `bad_nodes=0` riêng lẻ chỉ nghĩa không có grant ghi lạ, không chứng minh quyền đọc dương; kiểm cuối sẽ kiểm cả ba grant của các control.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding | Phân loại | Bằng chứng reviewer tự đo |
| --- | --- | --- |
| `test-reset-thieu-trang-thai-va-pham-vi` [P2] | **ĐÃ VÁ THẬT** | HEAD 118/118 rc0; reset_no_T 117/118 rc1 đúng ca cây lồng; reset_after_copy_cached_condition 117/118 rc1 đúng ca DACL rỗng; model_reset_noop 116/118 rc1 đúng hai ca mới. Oracle trạng thái Hướng 5 phân biệt được mô hình cũ/mới và AccessDenied trước copy. |

Finding P2 duy nhất của lượt 1 đã đóng bằng phép đo, không chỉ vì HEAD trùng hint. Không có finding mới qua các hướng đã hoàn tất; đang kiểm cuối tính toàn vẹn và các lỗi I/O mô phỏng.

## Hướng 6 — Chỉ có tệp ẩn và lỗi enumeration/reset/copy

- Giả thuyết: điều kiện có con bỏ lỡ cây chỉ có tệp ẩn; lỗi reset/chép vẫn cho đăng ký tác vụ.
- Lệnh: `python3 -B probes/edge-probes.py > evidence/edge-probes-driver.log 2>&1`, rc=0. Dùng harness từ HEAD trên bản sao; thêm fixture `.only-hidden` và tiêm ba lỗi có dấu hiệu riêng. Mutant chẩn đoán bỏ Force nằm riêng ở `copies/edge-no-Force/`, delta `evidence/edge-no-Force.patch`. JSON ở `evidence/edge-probes.json` và từng tên ca.
- Output thật: HEAD với root chỉ có một tệp dấu chấm ban đầu → reset=1, copies=3, tasks=1 (đúng dấu dừng trước mật khẩu), năm nút có ACL đúng mô hình; bỏ Force trên cùng fixture → reset=0, còn một nút Users Modify. Tiêm `RESET-FAIL-INJECTED` hoặc `ENUM-FAIL-INJECTED` → tasks=0, copies=0; tiêm `SHARING-LOCK-INJECTED` tại copy → tasks=0, lần thử copy=1, chưa tạo tệp mới.
- Kết luận: KHÔNG PHẢI LỖI của HEAD ở nhánh Force và truyền ngoại lệ đã đo. Mutant bỏ Force là đối chứng nhánh trong probe riêng, không tuyên bố đã chạy toàn suite cho mutant này. Ba lỗi I/O là ngoại lệ mô phỏng có kiểm marker, không phải native rc/sharing lock thật. `/reset` hay copy lỗi sẽ dừng trước khi tạo tác vụ mới; không có phép đo rollback hoặc xóa tác vụ cũ. Windows Hidden/System và lock NTFS vẫn KHÔNG ĐO ĐƯỢC.

## Hướng 7 — Kiểm cuối hiện vật, oracle và cây nguồn

- Giả thuyết: cây đổi sau test, log không khớp số ca/mutant, hoặc `bad_nodes=0` che DACL rỗng ở control.
- Lệnh: `python3 -B probes/final-audit.py > evidence/final-audit.log 2>&1` (kế thừa các oracle cần thiết từ probe audit lượt 1 nhưng neo SHA/số ca/kết quả hiện tại; tệp probe kiểm độc lập các log/patch/băm). Output đầy đủ và manifest băm ở `evidence/final-audit.json`; mã thoát ở `.rc`.
- Output thật: `Final audit: PASS; source unchanged; exact SHA, suite, target mutants, state/edge/argv oracles verified.`, rc=0. HEAD/base/tree giữ nguyên; tracked/index/untracked/ignored snapshot đều rỗng. Năm tệp nguồn bằng Git blob, băm preflight và cả hai bản sao control/head. Diff và snapshot khớp byte. Suite 118/118 rc0; 13 mutant riêng, 12 bị bắt, ba mutant trọng tâm bắt đúng ca; log, rc, patch và băm từng bản sao đều được so lại. Oracle trạng thái 9/9, edge 5/5, wrapper 3/3 và enumeration Linux 1/1. Bốn control (DACL rỗng, cây lồng với mô hình mới và mô hình sửa lượt 1, hidden-only) có đủ đúng ba grant Allow SYSTEM F / Administrators F / Users RX trên **từng nút**, owner Administrators, không chỉ kiểm danh sách vi phạm rỗng. Môi trường Linux, không tìm thấy `icacls.exe`.
- Kết luận: KHÔNG PHẢI LỖI về tính toàn vẹn bằng chứng và các oracle đã chạy. Reviewer không sửa cay-kho, không push, không gọi mạng. Snapshot sạch đầu/cuối chứng minh không có delta quan sát được, không tự chứng minh lịch sử mount read-only. Native Windows chưa được đo và không được tính là pass.

## Kết luận review

**approve** tại `90b3f1cd9ff8a3459285796da37dc96b8553690e`. Finding P2 `test-reset-thieu-trang-thai-va-pham-vi` lượt 1 **ĐÃ VÁ THẬT** theo suite và ba đột biến độc lập. Không có finding P0/P1/P2/P3 còn mở trong phạm vi diff này; không có HINT.patch mới vì không đề nghị sửa thêm.

Đây là verdict review mã/bằng chứng ngoại tuyến trên Linux, không phải biên nhận assurance vận hành, quyền merge/land hay chứng nhận NTFS/Task Scheduler Windows. Kết quả VM Windows executor thuật lại không được dùng thay phép đo reviewer.
