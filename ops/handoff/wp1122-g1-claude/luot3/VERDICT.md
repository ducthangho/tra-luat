verdict: changes_requested
reviewed_sha: 4c6f9331e35331b41ca1c4b982ee6c088cad8898
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Packet #1122 r1/g1, lease `wp1122-r1-g1-claude`, review_class `sensitive`, lượt Codex 3/10. Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`; reviewed tree `055be1f2bfd152dcf42057b8daf28b7c8edbbd74`. Hai mở rộng được chủ kho duyệt (raise AssertionError và encoding con Python) được tính vào nghiệm thu. Diff `.claude/` khớp bundle: một tệp, +297/-91; trong trần kích thước đã khai. Chỉ đánh giá `.claude/`, không review lại nội dung ops/reviews của lần merge master.

Reviewer: Codex/OpenAI, GPT-6 theo cấu hình phiên; không có chứng cứ độc lập xác minh biến thể model/effort của từng request. Thực thi bằng shell trong sandbox Linux qua API, transport machine (bề mặt service, không tự nhận là ChatGPT Web hoặc Codex CLI). Run được giao ở `run/50169eba/prompt.snapshot`; executor là Claude theo packet. Không suy reviewer identity từ Git actor; verdict không cấp quyền merge/land.

Môi trường đo: Python 3.13.18, Ruff 0.16.9. `/tmp/.git` tồn tại, rỗng/read-only. Các suite, probe và mutant chạy trên bản sao ngoài `cay-kho/`, với `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`. Không mạng, không credential thật. Bare lint dùng `--no-cache`; doctrine chỉ đọc checkout. Sandbox cho phép ghi workspace; checkout được giữ chỉ đọc bằng cách chọn nơi thực thi, không nhận nó là mount read-only.

## DOI CHIEU LUOT TRUOC

Đã chạy lại inventory/probes/routes/transport_edges/encoding_edges/encoding_behavior/allowlist_edge của lượt trước trên bản sao HEAD; không dùng số executor thay phép đo. Script giữ nguyên phương pháp, chỉ cập nhật SHA/đường nguồn. `audit3.py` áp HINT lượt 2 lên blob `6cf0cc5` trong bản sao: rc=0 và khớp từng byte với HEAD; lời khai áp nguyên văn là đúng.

| Finding / nguồn | Trạng thái trên HEAD | Phép đo |
|---|---|---|
| F01 lượt 1, `30ee4ae`: suite, kênh lặp tên loại/cắt cả prefix, transport mất message | Các biểu hiện cũ **ĐÃ VÁ THẬT** | probes.py: suite/lap 160 x, loại một lần; transport_edges.py: OSError/TimeoutExpired/ValueError/JSONDecodeError còn loại + message, vẫn loi |
| F01 lượt 2, `6cf0cc5`: nhật ký hai nhánh, foreign direct, compiler SAI | Bốn biểu hiện cũ **ĐÃ VÁ THẬT**, lớp vẫn **VÁ HỜ** | routes.py: nhật ký TypeError/AssertionError/TinHieuChotCa đều 160 x; foreign direct vẫn loi, có loại + 160 x; SyntaxError thật có message đúng 160. Còn reporter main khi tách nhóm lỗi và renderer chết khi stdout không UTF-8: F01 dưới đây |
| F02 lượt 1: chỉ đòi keyword encoding | **ĐÃ VÁ THẬT trong hình dạng scanner đã giữ** | cp1252/None và bảy giá trị encoding/errors sai khác đều bị chính khóa giết; giới hạn cú pháp cũ không bị khai thành bao phủ mọi cách gọi Python tương lai |

Không thấy bản sửa lượt 3 làm mở lại bốn biểu hiện cũ hoặc đổi phân loại giết/loi trong các đường đã đo. Có biến thể do việc thêm message của packet: stdout không UTF-8 làm reporter ném UnicodeEncodeError trước tổng kết. Metadata mới do các ca khóa để lại được đo riêng, không suy từ tổng suite.

## BANG NGHIEM THU

Lệnh mặc định chạy từ thư mục review này. Setup probe: `python3 evidence/setup_probe.py`. Trong các lệnh Python đặt ba biến môi trường nêu trên. `run_ab.py` tạo hai clone local bằng `git clone --no-hardlinks --no-checkout`, checkout detached đúng BASE/HEAD, rồi chạy bốn bộ tuần tự với cùng command/env/kiểu clone. Mã thoát và thời điểm thật ở ab-jobs.json/ab-times.json.

| Tiêu chí | Lệnh chạy được | Output thật / bằng chứng | Đạt? |
|---|---|---|---|
| N0 Windows, tái hiện trước vá | Lệnh đọc khi có quyền mạng: `gh run view 41328709141 --repo ducthangho/tra-luat --log` — **chưa chạy** | Code/lượt trước nêu commit thông điệp 4423d18 và TypeError `the JSON object must be str, bytes or bytearray, not NoneType`; thiếu log gốc để tự kiểm cp1252/readerthread/thứ tự tái hiện → vá | KHÔNG ĐO ĐƯỢC độc lập |
| N0' Linux base cùng rig | `ls -d /tmp/.git`; `python3 evidence/run_ab.py` | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | Đã đo nền, giữ các lỗi nền |
| A1 chuyển assert/raise và khóa AST | `python3 evidence/inventory.py`; `python3 evidence/probes.py`; `python3 evidence/allowlist_edge.py` | 57 assert/11 ca chuyển, điều kiện/message có sẵn khớp; 8 raise/2 ca chuyển. Helper hàm cấp module: raw rỗng. Khóa xanh; assert/raise/tên thừa/tên hết raw đều chết bằng chính khóa | ĐẠT SPEC + mở rộng |
| A2 TypeError(x*500) và cắt 160 | `python3 evidence/probes.py` | Khóa qua; mutant bỏ message/đổi trần chết ở chính r1122_loi_mang_thong_diep_cat_160 | ĐẠT A2 |
| Mục tiêu 3, toàn bộ reporter | `python3 evidence/routes.py`; `python3 evidence/transport_edges.py`; `python3 evidence/edges3.py`; `python3 evidence/unicode_stdio3.py` | Đường cũ đúng trong UTF-8; main vẫn bỏ message setsid. Với stdout ASCII, base hoàn tất tổng kết, HEAD chết UnicodeEncodeError khi in message Unicode | CHƯA ĐẠT F01 |
| Mục tiêu 4, con Python | `python3 evidence/inventory.py`; `python3 evidence/encoding_edges.py`; `python3 evidence/encoding_behavior.py` | 17/17 call Python text=True hiện có dùng utf-8/replace; 14 chỗ thêm so base. 22 call hệ thống giữ nguyên. Khóa bắt giá trị sai trong hình dạng nhận diện | ĐẠT Linux/static; không thay N0 |
| A3 Windows exact HEAD | Lệnh đọc khi có log/run id của HEAD: `gh api repos/ducthangho/tra-luat/actions/runs --method GET -f head_sha=4c6f9331e35331b41ca1c4b982ee6c088cad8898` — **chưa chạy** | Packet chỉ cung cấp run 41333516059 trên fd1f82e: executor khai 446/446, không đo 118; suite 282/282, bỏ qua 74, hỏng 0. Đây là SHA cũ; lượt 4c6f933 còn đang đo theo prompt, không có log gốc trong bundle | KHÔNG ĐO ĐƯỢC độc lập |
| A4 Linux HEAD/base | `python3 evidence/run_ab.py`; `python3 evidence/summarize.py` | HEAD: 326/349 ca DA CHAY QUA (tong 359, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 532/564 dat  (4 khong do duoc tren nen nay). Tập tên ca/mutant đỏ và tập bỏ qua giống base: delta=0. | ĐẠT điều khoản delta=0; không gọi N/N xanh |
| A5 bare Ruff F delta | `python3 evidence/audit3.py` → `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` ở base/HEAD | Mỗi bên rc=1, 17 lỗi: 5 F841 ở launcher_test.py, 12 F821 ở tl.py; delta=0. Ruff 0.16.9 | ĐẠT delta với bản có sẵn; pin CI 0.15.15 CHƯA ĐO |
| A5 doctrine | Cwd cay-kho: `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 | ĐẠT |
| A5 whitespace | `git -C cay-kho diff --check c82047da4d6f9546ce1d68282c37acf9567b74bc 4c6f9331e35331b41ca1c4b982ee6c088cad8898` | Rỗng, rc=0 | ĐẠT |
| A5 ci.yml exact HEAD | `gh api repos/ducthangho/tra-luat/commits/4c6f9331e35331b41ca1c4b982ee6c088cad8898/check-runs` — **chưa chạy** | Không có check-run receipt hiện hành; không gọi mạng theo chỉ thị | KHÔNG ĐO ĐƯỢC |
| A6 sau land | Đọc job windows-latest của push master sau merge, chưa đến thời điểm đo | Không chạy | CHƯA ĐO ĐƯỢC theo SPEC |

## BANG DO

Đã đọc diff.patch, toàn bộ diff-tu-luot2.patch và `git log --format=%B 6cf0cc5..HEAD`. audit.json lưu mọi dòng thêm của diff mới; commits.txt giữ nguyên commit message. Bảng này đối chiếu cả code, docstring, comment và lời khai trong commit mới.

| Khẳng định | Diff / commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Foreign chốt có loại/message, vẫn loi | cham_mot_ca: thêm mo_ta_loi và suffix chốt ca khác; docstring ca mới | probes.py/routes.py/transport_edges.py: direct/child đều loi, TinHieuChotCa một lần, 160 x; mutant bỏ detail chết đúng ca | Có |
| Nhật ký giữ cùng loại/message khi stdout chưa tổng kết | Hai biến ket đổi sang mo_ta_loi; r1122_nhat_ky... | routes.py: đọc file NhatKyCa thật, TypeError/AssertionError/TinHieuChotCa có 160 x; build_hint3.py chạy lại t99. Hai mutant ket chết ở chính ca nhật ký | Có; không tự nhận đã đo crash hệ thống hoặc mất điện |
| Compiler reporter cũng có loại + 160 | Nhánh SyntaxError, docstring và ca duplicate parameter mới | routes.py REAL_SYNTAX_ERROR: compiler thật, message là 160 ký tự (141 x sau prefix duplicate argument). Mutant bỏ cắt chết đúng khóa compiler | Có |
| Ba ca mới có răng; bốn mục mutation mới | Ba @ca và bốn DOT_BIEN_HARNESS ở đầu diff | probes.py: 7/7 khóa HEAD qua; 16/16 mutant wp1122 chết bằng TinHieuChotCa của chính ca, gồm cả bốn mục mới | Có |
| Ba docstring mô tả nhật ký / foreign / compiler | Nội dung diff + tên/thông báo các chốt | Các phép đo trên gọi đúng đường; journal nhánh AssertionError trần được đo bổ sung ngoài ca khóa | Có trong phạm vi mô tả |
| Subject: nhật ký, chốt ca khác, lỗi biên dịch đều giữ loại + 160 | Commit 4c6f933 | routes.py kiểm cả ba nhóm, đúng giới hạn và phân loại | Có cho ba nhóm được nêu |
| HINT lượt 2 áp nguyên văn | hint_provenance của commit | audit3.py: patch rc=0 trên blob 6cf0cc5, byte equality với HEAD=true | Có; không chứng minh thao tác suy nghĩ/tự liệt kê của executor |
| Tự liệt kê MỌI đường in chi tiết lỗi trong tệp, trùng đúng bốn đường | Thân commit 4c6f933 / lời khai packet | `rg -n -e 'type\(e\)\.__name__' -e 'e\.msg' -e '\{e\}' -e 'str\(e\)' cay-kho/.claude/dev/launcher_test.py`; edges3.py: dòng 2321 cũng là reporter được main in, mất message | Không khớp phần bao phủ “mọi đường”: còn F01. Không đếm thành finding thứ hai |
| Thêm message vẫn cho reporter chạy đến tổng kết | Hành vi của các reporter đã đổi, không có khóa stdout không UTF-8 trong diff | unicode_stdio3.py: cùng ca TypeError("✓"*500), PYTHONIOENCODING=ascii; base has_summary=true/no UnicodeEncodeError, HEAD has_summary=false/UnicodeEncodeError=true | Có hồi quy F01; không suy đây là kết quả Windows native |
| Kế thừa A1/encoding không bị đổi ngoài ý muốn | Phần chung với lượt trước còn ràng buộc nghiệm thu | inventory.py: 57 chuyển assert khớp AST; 14 encoding thêm; allowlist bằng đúng tập ba ca cố ý. Giá trị sai bị khóa bắt; Unicode thật cp1252 làm sai chữ nhưng nay guard đỏ | Có trong hình dạng scanner đã ghi giới hạn |

## BANG TEST

| Bộ | N/M | Bỏ qua / không đo | rc |
|---|---|---|---|
| Base suite | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| HEAD suite | 326/349 ca DA CHAY QUA (tong 359, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| Base --dot-bien | DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| HEAD --dot-bien | DOT BIEN: 532/564 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| Bảy ca r1122 trên HEAD | 7/7 | 0 | 0 |
| Mười sáu mutant wp1122 trên HEAD | 16/16 chết đúng ca, own_signal=true | 0 | 0 |
| Giá trị encoding/errors sai bổ sung | 7/7 bị đúng khóa bắt | 0 | 0 |
| HEAD + hai khóa mới của hint, chưa sửa reporter | 2/2 đỏ đúng lý do, own_signal=true | 0 | 0 (script kiểm phản chứng) |
| HINT: chín khóa r1122 | 9/9 | 0 | 0 |
| HINT: 20 mutant wp1122 | 20/20 chết đúng ca, own_signal=true | 0 | 0 |
| HINT: tám ca tương thích cũ | 8/8 | 0 | 0 |
| HINT: bốn mutant mới qua runner/kênh child thật | 4/4 OK, giet 1/1 đúng ca | 0 | 0 |

Tập lỗi suite HEAD: r09_run_json_giu_ba_trang_thai_probe, r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh, r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe, r484_g2_doctor_doc_dung_home_da_materialize, r484_g2_hook_shell_scrub_truoc_probe, r484_g2_probe_isolated_marker_va_refresh, r484_g2_recovery_probe_rollback_va_snapshot_moi, r484_g2_schema_truoc_freshness_va_home_materialize, r484_g2_storage_kernel_guardrails, r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi, r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do, r484_g7_tu_choi_ghi_dung_ban_da_probe, r484_g8_hook_scrub_kin_voi_bash_env, r858_goc_tam_tranh_to_tien_co_git, r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC, r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat, r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m, r925_codex_qua_han_van_124_va_giu_khung_da_den, r925_rust_log_thua_ke_bi_GHI_DE_khong_noi, r926_dot_bien_tu_sinh_moi_thanh_phan_regex, r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC, r927_lenh_run_ghi_effort_va_sandbox_vao_run_json, t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac.

Có 23 ca suite đỏ sẵn: 10 đường launcher.py run thuộc ngoại phạm vi vá, 11 r484 vướng tổ tiên /tmp/.git/materializer, hai r858/t86 không ghi được /var/tmp trong sandbox. Mười bỏ qua: hai native Windows và tám fixture cần venv/pypdf không dựng được offline. Mỗi bên 32 mutant SAI đều do neutral đỏ; không gộp thành skipped. Bốn mutant không đo giống nhau: 124_khi_chau_con_song và ba mục native Windows. doctor_bo_do_bash là OK/giet 1/1 t73 ở cả hai bên. Giữ lỗi nền khi tính N/M; delta=0 nói về tên/trạng thái, không nói chi tiết text giống byte sau khi đổi kiểu ngoại lệ/thêm message. Lượt này không dùng số A/B do executor cung cấp thay các số vừa đo.

## BANG SAN

Mỗi hướng dưới đây có lệnh và output thật, giữ ở evidence/*.log. Nội dung mới chỉ là x, Unicode vô hại hoặc tên giả. Không soạn payload nhạy cảm.

| Hướng độc lập | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| Tương đương điều kiện/message khi chuyển assertion | `python3 evidence/inventory.py` | converted 57, cases 11, mismatches []; helper_raw [] (hàm cấp module) | KHÔNG PHẢI LỖI |
| Assert/raise trong hàm lồng, alias, đăng ký trực tiếp | `python3 evidence/probes.py` | nested assert/raise/raise_name bị khóa giết; alias/helper/unittest/direct append có thể lọt scanner nhưng target vẫn loi | KHÔNG PHẢI lỗi hiện hữu; giới hạn cú pháp đã khai từ lượt 1 |
| Allowlist mục dần | `python3 evidence/allowlist_edge.py`; `python3 evidence/probes.py` | Bỏ raw cuối của t119, thêm tên t73 hoặc chèn assert/raise đều giet, own_signal=true | KHÔNG PHẢI LỖI |
| Giá trị encoding/errors sai | `python3 evidence/probes.py`; `python3 evidence/encoding_edges.py` | cp1252/None/mất encoding + 7 giá trị khác chết đúng khóa | KHÔNG PHẢI F02 còn mở |
| Dạng argv/text-mode khác | Cùng hai lệnh trên | sys.executable, biến argv, universal_newlines, text=1, implicit text có thể lọt; không có lời gọi sai đang tồn tại kiểu ấy trên HEAD | Giới hạn đã giữ; KHÔNG PHẢI lỗi mới |
| Giải mã thật và replace che lỗi byte | `python3 evidence/encoding_behavior.py` | HEAD `review ✓`, cp1252 `review âœ“` nhưng guard nay giet; mutant đọc byte sai bị r926 bắt own_signal=true; t73 vẫn nhận note U+FFFD vì chỉ kiểm tên công cụ | KHÔNG PHẢI tín dụng giết giả đo được từ bản vá |
| Renderer dưới stdout không UTF-8 | `python3 evidence/unicode_stdio3.py` | Cùng một lỗi Unicode: base in được DOT BIEN: 0/1 dat; HEAD không có tổng kết, stderr UnicodeEncodeError, cả hai rc=1 | LỖI F01; rc giống nhau không chứng minh hành vi giống nhau |
| Suite/CLI/kênh, nhiều loại ngoại lệ | `python3 evidence/probes.py`; `python3 evidence/routes.py`; `python3 evidence/edges3.py` | TypeError/AssertionError/OSError/RuntimeError: direct loi, loại một lần, message 160 x; CLI rc=1, x=160 | KHÔNG PHẢI LỖI |
| Nhật ký file thật, empty và Unicode | `python3 evidence/routes.py` | TypeError/AssertionError/TinHieuChotCa 160 x; empty chỉ TypeError; Unicode đúng 160 ký tự | KHÔNG PHẢI F01 cũ còn mở |
| Transport, JSON và child | `python3 evidence/transport_edges.py` | OSError/TimeoutExpired/ValueError/JSONDecodeError đều loi có message; child Unicode 160; thiếu kênh vẫn loi | KHÔNG PHẢI LỖI |
| Dòng SAI launcher/hook/harness | `python3 evidence/routes.py` | Các dòng neutral/false-credit giữ TypeError + 160; harness real child SAI giet 0/1 | KHÔNG PHẢI LỖI |
| Compiler thật, không chỉ mock SyntaxError | Cùng lệnh routes.py | Duplicate parameter 500 ký tự: SyntaxError + message 160, không in đủ 500 x | KHÔNG PHẢI F01 cũ còn mở |
| Foreign signal và tên ca chứa dấu phân cách | `python3 evidence/transport_edges.py`; `python3 evidence/probes.py` | Foreign direct/child vẫn loi; TypeError có phẩy/ngoặc/newline vẫn SAI, so_chet=0/can_do=1 | KHÔNG PHẢI LỖI |
| Metadata cũ, ca hồi phục và lồng ca | `python3 evidence/routes.py`; `python3 evidence/edges3.py` | Sau fail→pass map còn TypeError/review-old; channel hong=0 còn metadata. Child thật vẫn qua; child skip vẫn bo_qua; outer có inner lỗi vẫn qua | KHÔNG PHẢI lỗi đổi điểm; chưa có bảo đảm tự sạch metadata |
| Tác dụng phụ của khóa mới lên toàn cục | `python3 evidence/edges3.py` | CA/launcher/subprocess/platform/env unchanged=true; thêm review_chot/review_loi/review_vo_can vào detail map, không trùng tên CA hiện tại | KHÔNG PHẢI lỗ mới đo được; ghi rõ phần map tồn lưu |
| Reporter tách nhóm và main | `python3 evidence/edges3.py` | GROUP_DIAGNOSTIC/GROUP_MAIN: `KHONG tach duoc (PermissionError)`, message_x=0 | LỖI F01 |
| Hint đủ răng và tương thích | `python3 evidence/build_hint3.py`; `python3 evidence/hint_channel3.py` | Hai guard mới làm HEAD đỏ đúng lý do; fixed 9/9; mutant 20/20 own signal; 47 neo duy nhất; compatible 8/8; runner 4/4 OK; fixed main có 160 x | KHÔNG PHẢI LỖI trong phạm vi đo hint |

## KIEM KE DUONG BAO LOI

AST inventory lưu 33 except có biến e và 31 print thực, không lẫn chuỗi mỏ neo trong bảng mutant. Đã đọc hai except của chay_dot_bien: SyntaxError:14911 và Exception nhánh hook:14969. Các đường chi tiết trực tiếp và consumer được liệt kê đầy đủ dưới đây; từng nhóm đã được gọi bằng probe, thay vì kết luận từ grep.

| Nguồn → nơi in/tiêu thụ | Phép đo | Kết quả |
|---|---|---|
| mo_ta_loi:193; cham_mot_ca:209/213 → ket_luan_mutant:219 | probes.py, edges3.py, transport_edges.py | Lỗi thường/foreign giữ loại + 160; own chốt là giet chỉ mang tên theo thiết kế |
| chay_bo_ca:15164/15171 → hong_ds → main:15324/15344 | routes.py, probes.py | Cả hai nhánh, suite và --lap-ca, loại một lần + 160 |
| Hai nhánh chay_bo_ca → ket → NhatKyCa.ra:15083 | routes.py | HONG/LOI đều giữ loại/message; flush/fsync không bị đổi |
| CHI_TIET_HONG:15165/15172 → main channel:15328–15331 → cham_lap_ca:15130 | routes.py, transport_edges.py, edges3.py | Tách loại/message đúng tại lỗi; hong=0 được consumer kiểm trước metadata cũ |
| cham_lap_ca except:15123 → loi → reporter harness:15034/15037 | transport_edges.py, routes.py | Transport/JSON có detail đúng; không đổi thành giet |
| cham_mot_ca → product neutral:14936 / SAI:14939 | routes.py | Neutral đỏ/false-credit message đúng giới hạn |
| Hook Exception:14969 → loi → print:14982 | routes.py | TypeError 160 x; except TinHieuChotCa không in exception vì đó là nhánh giết, không phải loi |
| cham_lap_ca → harness neutral:15034 / SAI:15037 | routes.py | Loại + 160; tên/key dùng chấm điểm vẫn độc lập chuỗi detail |
| SyntaxError:14911 → print:14912 | routes.py, probes.py | Compiler thật giữ loại/message 160 |
| _tu_tach_nhom_neu_can:2320 → return:2321 → main:15277 | edges3.py | Chỉ còn loại, mất message: F01 |
| Renderer stdout của chay_dot_bien:14939, khởi tạo main:15263 | unicode_stdio3.py | Message ✓*500 làm HEAD chết UnicodeEncodeError dưới stdout ASCII, trước footer. Base cùng probe vẫn có footer: F01 |

25 except có biến còn lại thuộc thân ca/helper kiểm thử: chúng phân loại sentinel, đọc exception để chấm hoặc chuyển nó thành thông điệp của chốt; danh sách đầy đủ và source từng handler ở exception-inventory.json. Chốt/loi cuối của ca đi qua các reporter trên. Không coi mọi phép bắt exception dùng làm điều kiện thử là reporter độc lập. Các print còn lại là trạng thái, đếm, mỏ neo thiếu, tên ca, BO QUA hoặc bản khai môi trường; chúng không chứa thông điệp ngoại lệ để áp trần 160. Print SID ở ca Windows chỉ in boolean. Không ép tên/đếm/lý do skip về 160; không thay lớp runner giả kênh #1117 đang ngoài phạm vi.

## BANG LOP

| Slug / nguồn | Biểu hiện đã đóng | Còn mở | Phép đóng lớp |
|---|---|---|---|
| reporter-thong-diep, F01 lượt 1/30ee4ae và lượt 2/6cf0cc5 | Suite, channel lặp loại, transport; nhật ký thường/assertion, foreign direct, compiler SAI trong môi trường UTF-8 | 2 biểu hiện: main bỏ message setsid; renderer chết trước footer khi stdout không UTF-8. P1, một finding | Cùng formatter cho các đường và chuẩn hóa luồng xuất; khóa/mutant từng biểu hiện phải chết đúng ca. Hint đã đo riêng |
| khoa-encoding-chi-kiem-khoa, F02 lượt 1/30ee4ae | cp1252/None và giá trị sai khác bị khóa chặn | Không còn biểu hiện mở trong hình dạng scanner đã giữ | HEAD qua, giá trị sai chết đúng khóa; giữ giới hạn argv/text-mode đã công bố |

## FINDINGS

### reporter-thong-diep [P1] F01 còn mất thông điệp và chết khi xuất Unicode lên console không UTF-8

TEP/DONG: `.claude/dev/launcher_test.py:14939`, khởi tạo `:15263`; `.claude/dev/launcher_test.py:2321`, consumer `:15277`. Khóa cũ t90 chỉ đòi tên PermissionError; các khóa reporter mới dùng x ASCII nên không bắt lỗi xuất Unicode.

VAN DE: Việc thêm str(e) đưa Unicode ra stdout, nhưng harness chưa chuẩn hóa stdout/stderr. Với stdout không UTF-8, một TypeError có message Unicode làm chính print của chay_dot_bien ném UnicodeEncodeError; mất cả dòng chi tiết lẫn tổng kết. Base cùng probe chỉ in tên TypeError nên hoàn tất. Đây là hồi quy đo được từ packet; không phải tín dụng giết giả hoặc lỗi neutral nền của bộ A/B mặc định. Cách ép PYTHONIOENCODING=ascii giống phép t47 hiện có để dựng lớp lỗi console trên Linux; chưa nhận đây là phép đo Windows native. Workflow launcher-windows.yml cố ý không ép PYTHONUTF8/PYTHONIOENCODING.

Biểu hiện thứ hai: `_tu_tach_nhom_neu_can()` bắt OSError nhưng trả `KHONG tach duoc (<Loại>) - ...`, rồi main in nguyên chuỗi. Message bị bỏ hoàn toàn. Đây là reporter trực tiếp còn sót theo Q3/mục tiêu 3 “ở cham_mot_ca và các reporter”, đã có trước bốn thay đổi lượt 3. Câu “MỌI đường ... trùng đúng bốn đường” của commit 4c6f933 chưa đúng cho toàn tệp. Hai biểu hiện cùng đơn vị nghĩa reporter phải giữ được chẩn đoán ngoại lệ; không tách lời khai thành finding khác.

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 python3 evidence/unicode_stdio3.py`, rc=0. Dựng cùng ca TypeError("✓"*500) trong bản sao base/HEAD, neutral qua, mutant loi, chạy CLI --dot-bien thật với PYTHONIOENCODING=ascii. Cả hai rc=1 như mong đợi cho mutant loi, nhưng base has_summary=true/unicode_encode_error=false; HEAD has_summary=false/unicode_encode_error=true tại print:14939. Không đánh đồng mã thoát giống nhau với kết quả tương đương. unicode-stdio.json/log giữ nguyên stdout/stderr cả hai.

`python3 evidence/edges3.py`, rc=0: PermissionError("x"*500) ở seam setsid, helper và main đều in thiếu message, message_x=0. Main với ca qua vẫn rc=0; không khai có đổi điểm hoặc đo sự cố setsid native trên Windows.

GOI Y VA: chuẩn hóa stdout/stderr sang UTF-8 ở entry main (sau parse đối số) và entry chay_dot_bien, tương tự launcher CLI; luồng thay bằng StringIO hoặc không reconfigure được giữ fallback như launcher. Đổi detail tại dòng 2321 sang mo_ta_loi(e). Một khóa gọi CLI child dưới PYTHONIOENCODING=ascii, đòi có footer và đúng 160 ✓; mutant bỏ chuẩn hóa/đổi ASCII phải chết đúng khóa. Khóa khác đòi PermissionError + đúng 160 x; mutant bỏ message/bỏ cắt phải chết đúng khóa. Hai cơ chế cần vá riêng vì formatter chỉ tạo str, còn renderer mới chọn cách xuất str ra byte.

HINT.patch (-p0 từ cay-kho) minh họa hai sửa đó, hai @ca và bốn mutant. build_hint3.py: HEAD + hai khóa đều đỏ bằng TinHieuChotCa của chính ca; bản sửa 9/9 khóa qua, 20/20 mutant liên quan chết đúng ca; 8 ca tương thích cũ qua, 47 neo harness duy nhất, Ruff vẫn 5 F841. hint_channel3.py: bốn mutant mới qua runner child thật đều OK/giet 1/1; khóa setsid qua khi thiếu thuộc tính và phục hồi đúng trạng thái; main bản sửa có 160 x/loại một lần.

TÁC ĐỘNG CẦN KIỂM: chuẩn hóa làm output byte là UTF-8, phù hợp decoder Python con hiện đã khai; consumer cố dùng codec khác cần cập nhật. Luồng custom không hỗ trợ reconfigure vẫn là giới hạn của gợi ý, chưa hứa xử lý mọi sink. Chuỗi setsid dài thêm tối đa 160 ký tự message; consumer so nguyên chuỗi cũ cần cập nhật. Giữ quyết định tách nhóm/nhãn cảnh báo và phân loại tín hiệu; cắt 160 không là redaction. Chưa chạy full suite/full --dot-bien của hint và chưa đo native Windows. Nhãn hint: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

DO TIN: cao về đường chạy và output, có phản chứng đúng nguyên nhân và own signal, cả main và child thật. Phạm vi kết luận là reporter exception trong chính tệp được giao; không xin mở write set, không sửa branch executor.

## TOAN VEN VA GIOI HAN

source-initial.json / source-final.json kiểm hash từng tệp ngoài .git, tracked/untracked/ignored, HEAD/tree và diff working tree/index. integrity.json: same_files=true, same_identity=true, clean=true. Không có delta quan sát được giữa hai mốc; snapshot không chứng minh chưa từng có ghi rồi hoàn nguyên. Các bản sao tạm của riêng lượt này được dọn, giữ script/log/JSON và HINT.patch; dựng lại bằng setup_probe.py/run_ab.py. Không push, không gọi mạng hoặc credential thật.

Chưa tự đọc Windows N0/A3, bare Ruff đúng pin CI và check-run exact HEAD. A6 sau land chưa đến. Các phần KHÔNG ĐO ĐƯỢC không biến thành pass hoặc finding suy đoán. Cắt 160 không che thông tin nhạy cảm; hướng kiểm exception từ API/subprocess có thể mang dữ liệu người dùng vào log chỉ được mô tả bằng lời, không soạn payload và không dùng credential thật. Không phát hiện P0/P2/P3 mới trong phạm vi đo. Verdict changes_requested vì F01 còn hai biểu hiện.
