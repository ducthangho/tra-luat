verdict: changes_requested
reviewed_sha: 9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

Packet #1122 r1/g1, lease `wp1122-r1-g1-claude`, PR #1130, sensitive, lượt Codex 9/10. **Không xác lập finding mã mới; P2 lượt 8 đã được vá thật. Chưa đủ bằng chứng để approve toàn SPEC:** N0 Windows trước vá, A3 Windows và phần check-run CI của A5 trên exact HEAD chưa đo được trong bundle offline. `changes_requested` ở đây yêu cầu bổ sung chứng cứ nghiệm thu, không yêu cầu sửa mã dựa trên giả thuyết. Không gán một severity giả cho phần không đo được.

Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`. HEAD tree `5b75be44bad08bc3d38251fadde507813dd6305e`; blob launcher_test `44967099f0f7fe6244452e08e88fe824c9bab572`. Băm lại SPEC khớp. Review chỉ `.claude/`: một tệp +450/-93. Diff từ cccc5eb +21/-21, gồm bỏ 20 dòng trắng, thay một dòng gọi test, thêm callback/chốt và hai mutant. Diff đầy đủ và diff từ lượt 8 khớp bundle; nguồn HEAD khớp từng byte HINT lượt 8 áp lên cccc5eb. Không cần nâng_trần hoặc sửa producer để đóng P2 cũ.

Reviewer thực tế: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; không có attestation độc lập biến thể/effort model từng request. Shell Linux sandbox qua API, transport machine; không phải ChatGPT Web, không suy model từ Git actor. Executor Claude theo packet; không kế thừa context executor. Review này không đăng GitHub, cấp quyền merge/land, dùng mạng hoặc credential thật. Skill cloud-environment-runtime đã đọc; tool environment_status không có trong danh sách công cụ, không suy readiness từ việc đó.

Cay-kho được giữ chỉ đọc bằng nơi chạy; sandbox thực tế workspace-write, không tự nhận đã mount read-only. Snapshot đầu/cuối, Git/index readback và cleanup ở cuối báo cáo. Mọi suite/probe/mutant chạy trên clone/bản sao ngoài cay-kho. Hai vế A/B cùng clone cục bộ `git clone --no-hardlinks --no-checkout`, cùng Python 3.13.18 và Ruff 0.16.9, TMPDIR riêng, PYTHONDONTWRITEBYTECODE=1 và PIP_NO_INDEX=1. `ls -d /tmp/.git` đã trả `/tmp/.git` trước khi đo; không xóa/chỉnh nó để làm xanh. `/var/tmp` không ghi được. Các điều kiện này tạo lỗi nền được giữ nguyên để so delta.

Theo phân công của prompt: chỉ chạy các lớp ngoại lệ có hành vi đặc biệt ĐÃ CÓ trong cây; không soạn lớp mới. common/guards/mutation_probes/order_mutations/routes/extended/encoding_edges/ast_edges/inventory/scope_inventory được đọc, chép từ artifact lượt 8 và CHẠY LẠI trên HEAD hiện tại; không tái dùng output cũ. Các probe bổ sung chỉ dùng ngoại lệ chuẩn và fixture/seam bình thường. Hướng cần lớp ngoại lệ mới được mô tả bằng lời ở cuối.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / nguồn | Trạng thái trên HEAD | Bằng chứng đo lại |
|---|---|---|
| F01 lượt 1: suite/CLI in 500, transport mất message | ĐÃ VÁ THẬT các biểu hiện đó | routes.py và cli_routes.py: TypeError/AssertionError/TinHieuChotCa giữ loại + đúng 160 message ở suite, nhật ký và CLI thường/lặp; transport bốn loại vẫn loi và giữ message. |
| F01 lượt 1: channel lặp loại/cắt prefix | PHẠM VI ĐÃ ĐỔI do chủ kho; không gọi là vá message | Không còn identifier CHI_TIET_HONG. Channel sáu field nonce/ten/qua/bo_qua/hong/loai, không mang message; harness lỗi ra review_child(khac:TypeError), đúng quyết định sau lượt 5. |
| F01 lượt 2: ket nhật ký, foreign chốt, compiler | ĐÃ VÁ THẬT các biểu hiện đó | Journal LOI/HONG có loại +160; direct foreign vẫn loi và có chi tiết; compiler thật duplicate argument dài 500 bị cắt ở 160. Mỗi mutant reporter tương ứng chết đúng ca. |
| F01 lượt 3: Unicode console và tách nhóm | ĐÃ VÁ THẬT trong luồng chuẩn đã đo | Guard child PYTHONIOENCODING=ascii có footer, đúng 160 ✓; setsid PermissionError +160. Mutant bỏ UTF-8/dùng ASCII/mất chi tiết đều own_signal=true. |
| F01 lượt 4: phát lại message cũ, I/O nhật ký traceback | ĐÃ VÁ THẬT các biểu hiện đó | Hai fixture prelude/lồng khi hong=0 có loai=null và không field message. CLI journal open/write/fsync/final/close qua formatter, không traceback cho Exception. |
| F01 lượt 5: ca lồng đổi loại ở lượt qua/bỏ qua | ĐÃ VÁ THẬT các fixture đó | extended.py: pass/skip/nested-error/nested-signal sau lỗi ngoài đều giữ khac:TypeError và hong=1. Mutant đọc lại map/chụp cả lượt qua chết đúng khóa. |
| F01 lượt 6: format lồng sau ghi map | ĐÃ VÁ THẬT các fixture hiện có | Sáu tổ hợp trong guard và hai tổ hợp journal seam đều qua. Bốn mutant late/early-map của hai handler đều bị own signal bắt. Các tổ hợp cần lớp ngoại lệ đặc biệt khác của lượt 6 không dựng lại theo giới hạn prompt, không khai đã đo chúng. |
| F01 lượt 8: khóa bỏ nhánh AssertionError | **ĐÃ VÁ THẬT** | order_mutations.py: late-assertion và early-map-assertion từ 12/12 lọt ở lượt 8 thành 11/12 qua, chính r1122_nhat_ky_giu_loai_va_thong_diep_160 giết với `formatter long doi loai loi ngoai: TinHieuChotCa`, own_signal=true. Hai entry mới cũng chết đúng ca khi chạy riêng và qua runner/child catalog. |
| F02 lượt 1: khóa nhận cp1252/None | ĐÃ VÁ THẬT trong hình dạng scanner đã công bố | 10 giá trị encoding/errors sai đều giet/own_signal=true. Chay thật giữ `review Đ ✓`; cp1252 làm sai chữ. Bốn giới hạn cú pháp vẫn khai riêng, không có call sai thuộc chúng trên HEAD. |

Không dùng tổng suite, việc đã áp HINT hoặc số 30 handler để tuyên bố đóng mọi trường hợp Python có thể tạo ra. Các biểu hiện cũ có phép đo được đóng; các hướng chưa đo được giữ riêng, không đổi thành pass hoặc finding đã xác lập.

## BANG NGHIEM THU

Lệnh dưới đây chạy từ thư mục review. `evidence/ab_run.py base` và `... head` chạy hai lệnh thật `python3 .claude/dev/launcher_test.py` và `python3 .claude/dev/launcher_test.py --dot-bien` trong clone tương ứng. Logs và JSON giữ nguyên sau cleanup.

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| N0 Windows trước vá, tái hiện → ghi message → vá | NOT_RUN: không có Windows/log job gốc offline | Source/comment nhắc run 41328709141; prompt chỉ cung cấp Windows pass trên fd1f82e. Không thay raw log N0 bằng lời khai | KHÔNG ĐO ĐƯỢC |
| N0' Linux base cùng rig | `ls -d /tmp/.git`; `python3 evidence/ab_run.py base` | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | ĐÃ ĐO NỀN, giữ rc đỏ |
| A1 assert/raise + AST khóa | `python3 evidence/inventory.py`; `python3 evidence/ast_edges.py`; `python3 evidence/mutation_probes.py` | 57 assert/11 ca, 8 raise/2 ca chuyển, mismatch=[]; assert/nested/raise Name/allowlist thừa hoặc mục dần đều bị đúng ca bắt | ĐẠT SPEC + mở rộng đã duyệt |
| A2 thông điệp 160 | `python3 evidence/guards.py`; `python3 evidence/routes.py`; `python3 evidence/mutation_probes.py` | TypeError(x*500) → loi, đúng 160 x; bỏ message/đổi trần bị chính khóa giết | ĐẠT |
| A3 Windows exact HEAD | NOT_RUN, không mạng/Windows/log exact HEAD | Windows 41333516059 được cung cấp thuộc fd1f82e, không thuộc 9d06bd10 | KHÔNG ĐO ĐƯỢC |
| A4 Linux HEAD/base | `python3 evidence/ab_run.py head`; `python3 evidence/summarize.py`; `python3 evidence/validate.py` | 331/354 ca DA CHAY QUA (tong 364, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 543/575 dat  (4 khong do duoc tren nen nay). Tập failed/skipped so theo tên trong ab-summary.json | ĐẠT điều khoản delta=0; validation.json xác nhận đủ catalog, không gọi N/N xanh |
| A5 bare Ruff F | `python3 evidence/audit.py` | Base/head cùng rc=1: 5 F841 launcher_test.py +12 F821 tl.py; chẩn đoán delta=0 | ĐẠT delta với Ruff 0.16.9; chưa đo bare lint bằng pin CI 0.15.15 |
| A5 doctrine | Cùng audit.py: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` trong clone HEAD | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 | ĐẠT |
| A5 whitespace | audit.py và `git -C cay-kho diff --check BASE HEAD` | .claude và toàn diff output rỗng, rc=0 | ĐẠT |
| A5 check-run ci.yml exact HEAD | NOT_RUN: không có receipt/check-run log cuối, cấm mạng | Không dùng kiểm tĩnh workflow/pin thay kết quả job | KHÔNG ĐO ĐƯỢC |
| A6 sau land | NOT_RUN, ngoài thời điểm/quyền reviewer | Chưa land | CHƯA ĐO ĐƯỢC theo SPEC |

## BANG DO

claims.py lấy mọi dòng thực thi thay đổi, comment bằng tokenize, docstring bằng AST và toàn bộ `git log --format=%B cccc5eb..HEAD`. Các entry catalog được tách khỏi vùng neo/thay như runner thật. Không có comment/docstring thay đổi trong diff lượt 8; có 21 dòng thêm không trắng, xóa 20 dòng trắng và thay một dòng gọi test.

| Khẳng định | Diff khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Khóa thứ tự formatter/map ở nhánh AssertionError | Subject commit 9d06bd10, callback/chốt journal | guards.py 12/12; order_mutations.py: cả late và early-map assertion chết đúng journal guard | Có |
| HINT lượt 8 áp nguyên văn | hint_provenance trong commit | claims.py: áp HINT.patch lượt 8 vào cccc5eb ở cây tạm, exact_hint_source=true cho TOÀN TỆP | Có |
| Chỉ TEST và 2 đột biến | Commit | claims.py: chay_bo_ca/cham_mot_ca/cham_lap_ca/main/mo_ta_loi không đổi AST; catalog harness 52→54; diff chỉ khối test và catalog | Có |
| Bỏ dòng trắng để giữ trần 450 | Commit | Diff từ lượt 8 +21/-21, bỏ đúng 20 dòng trắng; cumulative +450/-93 | Có |
| Callback chạy ca lồng khi format, luôn hạ cờ | 21 dòng mới | guards.py; đọc try/finally và guard dang_in. Hai fixture ordinary/signal cho inner loại ngược, map cuối giữ loại ngoài | Có |
| Nhật ký vẫn có loại và đúng 160 | Chốt cũ giữ, thân fixture gia cố | routes.py, cli_routes.py: 3 loại × 2 chế độ CLI, mọi journal/detail_exact=true và không x*161 | Có |
| Hai entry mới có neo duy nhất và đúng target | Catalog mới | claims.py: 54/54 neo unique/compile/target có mặt; mutation_probes.py 27/27 wp1122 own_signal; full --dot-bien đo đường child | Có trong phép đo |
| Không có read lại CHI_TIET_HONG / field message | Phạm vi chủ kho sau lượt 5 | inventory/scope_inventory: 0 identifier CHI_TIET_HONG; channel chỉ sáu trường; guards/extended không phát lại chi tiết cũ | Có |
| Mọi direct PY/py với literal text=True ghim utf-8/replace | Mở rộng đã duyệt, không mới từ lượt 8 | inventory.py: 21 call đều đúng, 22 call hệ thống giữ nguyên; scope_inventory: 12 direct Python khác dùng bytes/không text | Có trong hình dạng được nhận diện |
| Lời khai lịch sử 30 handler dựng chuỗi =18 ca +12 hạ tầng tại 93a9afe | Prompt yêu cầu kiểm lại, không có thay đổi claim này trong lượt 8 | scope_inventory.py: 93a9afe có 33 named handler/21 trong ca; predicate str/repr/type/mo_ta_loi/f-string công bố cho 28/17. HEAD 34/21 và 29/17. _CsSeam.f_kill chỉ append+raise, không format | Không tái lập số 30 dưới predicate này; thiếu script/predicate gốc nên không gán sai số cùng định nghĩa. Không dùng lời khai đó chứng minh đóng lớp |

## BANG TEST

| Bộ | N/M / kết quả | Bỏ qua/không đo | rc |
|---|---|---|---|
| base suite | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| base mutations | DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| head suite | 331/354 ca DA CHAY QUA (tong 364, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| head mutations | DOT BIEN: 543/575 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| Khóa r1122 HEAD | 12/12 qua | 0 | 0 |
| wp1122 mutant riêng | 27/27 giet đúng TinHieuChotCa của ca đích | 0 | 0 |
| Thứ tự, 4 mutant bổ sung | 4/4 bị đúng ca bắt; assertion 11/12 qua, ordinary 10/12 qua | 0 | 0 |
| AST nested/raise Name/allowlist mục dần | 4/4 giet own_signal=true | 0 | 0 |
| Encoding/errors sai | 10/10 giet own_signal=true | 0 | 0 |
| CLI suite/lặp với 3 loại lỗi | 6/6 có đúng detail160 và nhật ký, child rc=1 đúng kỳ vọng | 0 | 0 script |
| Ca tương thích cũ quanh nhật ký/provenance/headline | 7/7 qua | 0 | 0 |
| Fixture data/provenance ngoài @ca | 6 phép đo đạt | 0 | 0 |

## BANG SAN

Mỗi hướng dưới đây có lệnh và output THẬT đã lưu trong evidence. Nhãn KHÔNG PHẢI LỖI chỉ áp phạm vi phép đo; không biến NOT_RUN thành pass.

| Hướng độc lập | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| Tương đương chuyển assert/raise | `python3 evidence/inventory.py` | asserts=57, raises=8, mismatch=[] | KHÔNG PHẢI LỖI |
| AST lồng/raise Name/allowlist mục dần | `python3 evidence/ast_edges.py` | 4 giet/own_signal=true | KHÔNG PHẢI LỖI |
| Giá trị bảng mã/errors | `python3 evidence/encoding_edges.py` | 10 giá trị sai giet/own_signal=true; UTF-8 đúng, cp1252 sai chữ | KHÔNG PHẢI F02 còn mở |
| Giới hạn cú pháp scanner | Cùng encoding_edges.py | sys.executable, argv biến, text=1, universal_newlines đều qua khóa | KHÔNG PHẢI lỗi mới đã xác lập: giới hạn công bố từ lượt trước, không có call sai hiện tại; không khai phủ dataflow |
| Direct/suite/foreign/journal | `python3 evidence/routes.py` | foreign=loi; direct/suite/journal loại đúng, message160; message rỗng chỉ tên loại | KHÔNG PHẢI lỗi cũ còn mở |
| CLI mặc định và lặp | `python3 evidence/cli_routes.py` | 6/6 detail_exact=true, long_message_absent=true, journal_detail=true | KHÔNG PHẢI LỖI |
| Transport timeout/OSError/ValueError/JSON | `python3 evidence/routes.py` | Bốn kết quả loi, detail đúng mo_ta_loi | KHÔNG PHẢI LỖI |
| Product/hook/harness SAI | Cùng routes.py | Mỗi probe (1,0); product/neutral/hook TypeError +160; harness khac:TypeError | KHÔNG PHẢI LỖI reporter |
| Compiler thực | `python3 evidence/guards.py`; mutation_probes.py | Duplicate argument 500 tạo SyntaxError thực, output cắt160; mutant không cắt bị đúng khóa giết | KHÔNG PHẢI LỖI |
| Unicode console / setsid | guards.py; mutation_probes.py | Console ascii còn 160 ✓ và footer; setsid PermissionError160; mutant đúng own signal | KHÔNG PHẢI LỖI |
| Lượt qua/bỏ qua sau lỗi ngoài | `python3 evidence/extended.py`; guards.py | 4 follow-up đều khac:TypeError, hong=1; lượt qua không lỗi có loai=null | KHÔNG PHẢI LỖI |
| Thứ tự formatter/map cả hai handler | `python3 evidence/order_mutations.py` | late/early-map assertion đều bị journal guard giết; ordinary bị journal và channel guard giết; mọi own_signal=true | **P2 lượt 8 đã đóng** |
| Nhật ký I/O và lỗi điều khiển | `python3 evidence/extended.py` | open/write/fsync/final/close cắt, không traceback cho Exception; SystemExit rc7, KeyboardInterrupt rc-2 không bị nuốt | KHÔNG PHẢI LỖI |
| Fixture không phải reporter | `python3 evidence/fixture_routes.py` | _wp1077_llm raw_x=500 nhưng khi ra suite message_length=160; _CsNhan tương tự160; registry fixture qua; _CsSeam giữ nguyên object không format | KHÔNG PHẢI đường in chi tiết còn sót |
| Toàn vẹn lời khai diff/HINT | `python3 evidence/claims.py` | diff_equal=true, exact_hint_source=true, 54 unique/compile/target, producer_unchanged=true | KHÔNG PHẢI LỖI |
| Nền đầy đủ | ab_run.py base/head; summarize.py; validate.py | Failed/skipped so theo TẬP TÊN, không chỉ tổng; giữ lỗi nền | XEM validation.json |
| Windows/check run exact SHA | NOT_RUN | Không có native Windows/log cuối/receipt trong bundle, cấm mạng | KHÔNG ĐO ĐƯỢC |

## KIỂM KÊ ĐƯỜNG CHI TIẾT

AST toàn tệp lưu inventory.json (34 named handler, 21 trong @ca, 32 print site); detail-sites.txt lưu grep toàn tệp, không giới hạn khoảng dòng. scope-inventory.json/log kiểm LOAI_HONG, repr, traceback/excepthook và subprocess. Mọi print site đã được đọc cùng producer, không chỉ các except.

| Đường / dòng HEAD | Cách đo / kết quả |
|---|---|
| cham_mot_ca:209–214 → mo_ta_loi:193 | routes.py direct ordinary/assertion/foreign; own chỉ tên và giet. Dữ liệu ngoại lệ chuẩn type một lần và message160. |
| chay_bo_ca:15299–15310 → hong_ds → main thường:15491 / lặp:15472 | routes.py và cli_routes.py chạy cả hai CLI, 3 loại; giữ loại/message160. Hai handler mỗi handler format một lần trước map. |
| Hai handler → ket → NhatKyCa.ra:15220 → ghi/flush/fsync | Journal thật; guard seam tái nhập; 4 mutant thứ tự bị bắt, hai entry assertion mới qua runner thật. |
| NhatKyCa __init__/ghi/vao/ra/dong → biên CLI:15499–15501 | extended.py open/write/fsync/final/close, Exception được format/cắt; không nuốt BaseException điều khiển. |
| chay_dot_bien compiler:15048–15049 | Guard compiler thật với tham số trùng500; mutant bỏ cắt own signal. |
| Nhánh sản phẩm:15069/15073/15076 → ket_luan_mutant:218 | routes.py neutral và false-credit SAI, mỗi lỗi detail được format trước khi ghép, đúng160. |
| Nhánh hook:15106–15119 | routes.py hook TypeError500 → SAI, đúng160. TinHieu không in message lỗi thường ở nhánh này. |
| Nhánh harness:15167/15171/15174 → cham_lap_ca:15260–15269 | routes.py child thật chỉ khac:TypeError theo scope; 4 loại transport giữ message160. |
| Main --lap-ca:15464–15477 producer channel → cham_lap_ca consumer | guards/extended giữ loại lần hỏng ngoài, bỏ field message, lượt qua không phát lại loại cũ. Một read live LOAI_HONG vẫn ở15465, xem hướng chưa đo bên dưới. |
| _tu_tach_nhom_neu_can:2320–2321 → main:15422 | Guard setsid PermissionError500 giữ loại+160; mutant bỏ message/bỏ cắt chết đúng ca. |
| _cung_hoa_dau_ra_harness:15398 → main và chay_dot_bien | Guard child ascii giữ Unicode/footer; mutant mất UTF8 và đổi ASCII chết đúng ca. |
| Các nhánh trạng thái cố định, skip/headline, khai môi trường | Đã đọc toàn bộ32 print site. Các site này không tự format đối tượng lỗi; detail của skip/fixture là dữ liệu test, không tính là thêm reporter exception. |
| _wp1077_llm/_CsNhan/_review6_registry_raw/_CsSeam và các handler trong @ca | fixture_routes.py kiểm bốn helper; handler trong ca là logic fixture/chốt, không phải final reporter. Chi tiết được chốt của ca phát ra vẫn đi qua chay_bo_ca/cham_mot_ca ở trên. |
| repr(e), traceback.*, sys.excepthook/threading.excepthook | Chỉ có hai repr(e) trong logic registry test; không có lời gọi/install custom traceback formatter/excepthook trong AST. Không coi default Python hooks đã biến mất: KeyboardInterrupt còn traceback đúng như extended.py đo. |

## BẢNG LỚP VÀ FINDINGS

| Slug ổn định | Lịch sử / nguồn | Còn mở đã xác lập | Phép đóng / giới hạn |
|---|---|---|---|
| reporter-thong-diep (F01) | Lượt1–6: các reporter, Unicode, I/O, stale/live map và reentrancy; lượt8: thiếu khóa AssertionError | 0 biểu hiện P0/P1/P2/P3 mới được xác lập | Từng đường/chốt đã đo lại, 27 mutant own signal và 4 mutant thứ tự. Channel bỏ message theo authority. Các hướng cần lớp ngoại lệ mới chưa đo, không tự gọi pass. |
| khoa-encoding-chi-kiem-khoa (F02) | Lượt1: cp1252/None lọt | 0 biểu hiện mở trong hình dạng công bố | 10 giá trị sai bị đúng khóa giết, byte UTF8 thật đúng. Dataflow/cú pháp khác và Windows vẫn khai riêng. |

Không có finding mã mới nên không có patch sửa mã đề nghị. HINT.patch được để rỗng. Không vá dựa trên một giả thuyết chưa có phản chứng, không mở #1117 hoặc write set, không yêu cầu nâng_trần.

Để đổi sang approve toàn SPEC cần evidence của **chính SHA 9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651**: log job windows-latest cho suite hong0 và mutation M/M cùng các mục Windows/doctor bắt buộc; check run ci.yml cuối; và raw log N0 ở giai đoạn chỉ thông điệp xác nhận TypeError trước vá. Đó là nghĩa vụ nghiệm thu, không phải finding code/P2 bị suy ra từ việc reviewer không có Windows. A6 chỉ đo sau land, không yêu cầu làm trước review. Trần450 hiện vẫn giữ, không đề nghị thêm commit chỉ để đổi verdict.

## HƯỚNG CHỈ ĐỌC MÃ, CHƯA DỰNG PHẢN CHỨNG

Vẫn có read live LOAI_HONG ở main:15465 sau chay_bo_ca ghi map:15303/15309, kết thúc except, có thể ghi nhật ký:15312 rồi return:15313. Cache mo_ta_loi khóa callback __str__ đã biết, chưa tạo metadata thuộc invocation. Nếu callback khi lỗi được giải phóng ở cuối except chạy lồng cùng ca trước khi main đọc map, kết quả có thể đọc loại lần lồng. Phải chứng minh lifetime/callback thực và control direct/channel; không suy P1 chỉ từ thứ tự code. Hướng executor tự dựng: đối chiếu lỗi ngoài thường với chốt trong, đủ traceback/timing và journal/no-journal, không tự ghi map trong fixture. Hướng khác: formatter của lỗi thay đổi traceback/provenance trước chot_tu_ca_khac ở15303, trong khi cham_mot_ca kiểm trước formatter ở209–212. Nếu lỗi của chính __str__ thoát formatter, biên CLI cũng có thể gặp lỗi khi format lại. Đây là các hướng KHÔNG ĐO ĐƯỢC trong lượt này vì cần lớp ngoại lệ có hành vi đặc biệt mới mà prompt cấm reviewer soạn.

Nếu executor xác lập phản chứng, hướng vá hẹp là metadata thuộc kết quả invocation và chụp danh tính/provenance trước callback; cần guard cho producer/consumer và mỗi mutant chết bằng chốt của đúng ca. Đổi runner thuộc #1117 cần authority riêng. Chỉ mô tả hướng, không kèm patch producer authority.

Ngoài ra message có thể chứa dữ liệu người dùng trong160 ký tự đầu: cắt độ dài không phải redaction. Không soạn nội dung nhạy cảm/credential thật, không khai đã đo một vụ rò dữ liệu.

## TOÀN VẸN, GIỚI HẠN VÀ HIỆN VẬT

Các script/log/JSON nằm trong evidence/. Sau cleanup, dựng lại clone bằng `python3 evidence/setup.py` trước khi lặp các probe; chạy lại A/B bằng `python3 evidence/ab_run.py base` và `python3 evidence/ab_run.py head`. N/M, skipped và failed tách riêng; mọi child rc khác0 dùng làm phản chứng được giữ đúng ý nghĩa. Tên failed/skipped, danh sách catalog đầy đủ, hash/status và cleanup sẽ được chốt ở readback cuối sau khi hai writer kết thúc. Snapshot sạch chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Ruff pin/probe contract chỉ đọc tĩnh từ workflow, không thay bare lint 0.15.15 hay CI job cuối.

Readback cuối: source-initial.json/source-final.json băm 10459 tệp ngoài .git, gồm ignored/untracked; same_files=true, same_identity=true, initial_clean=true, clean=true; staged/unstaged diff rc=0, output rỗng. HEAD/tree đúng OID ở đầu tệp. Không có delta quan sát được giữa hai mốc.

validation.json: base đủ 552/552 dòng catalog đúng một lần (516 OK,32 SAI,4 không đo); HEAD đủ 579/579 (543 OK,32 SAI,4 không đo). Tập hỏng/bỏ qua suite và mutation trùng khít, delta=0; 27 entry wp1122 đều OK. Cả hai suite có23 ca hỏng: 10 đường run, 11 r484 và2 ca gốc tạm /var/tmp; các lỗi đều có sẵn trên base cùng rig. Danh sách tên trong ab-summary.json, output đầy đủ trong bốn log. Không gọi full suite xanh.

Đã dọn bốn cây copy-base/copy-head/tmp-base/tmp-head của riêng lượt này sau khi writer kết thúc; giữ script/log/JSON/VERDICT và HINT.patch rỗng. cleanup.json ghi đường dẫn và dung lượng đã dọn. Artifact-manifest.json lưu size/SHA-256 hiện vật, không tự băm chính nó.

Hoàn tất 2026-11-01T23:31:00.375477+00:00.
