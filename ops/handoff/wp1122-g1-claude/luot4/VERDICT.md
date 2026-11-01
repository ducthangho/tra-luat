verdict: changes_requested
reviewed_sha: 93a9afe7bda76c55349bf72ba4fe77455758365d
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Packet #1122 r1/g1; lease `wp1122-r1-g1-claude`; review_class `sensitive`; lượt 4/10. Immutable base `c82047da4d6f9546ce1d68282c37acf9567b74bc`; reviewed tree `74c9409ecb2e71ebb3250c3600f1360be8aea117`. Hai mở rộng đã duyệt (raise AssertionError và encoding con Python) được tính. Diff `.claude/`: đúng một tệp, 348 thêm/92 xóa, khớp byte với bundle; merge master chỉ thay `ops/reviews/**`, không tính thành code cần review.

Reviewer: Codex/OpenAI, họ GPT-6 theo cấu hình phiên, shell trong sandbox Linux qua API, transport machine; run `0f89b394`. Không có phép đo độc lập biến thể model/effort trên từng request. Không dùng danh tính Git actor làm model identity, không tự nhận ChatGPT Web hay đã đo Windows. Chỉ thị trực tiếp của chủ kho là authority cho review offline này; verdict không cấp quyền merge/land.

Môi trường: Python 3.13.18; Ruff 0.16.9. `/tmp/.git` tồn tại; `/var/tmp` không ghi được trong rig này. Không xóa/chỉnh hai thư mục đó để làm xanh. Mọi suite/probe/mutant chạy trên bản sao ngoài `cay-kho/`; clone base và HEAD cùng cách dựng, cùng env `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`, bỏ `CODEX_AUTH_JSON` kế thừa. Không gọi mạng, không credential thật. Ruff `--no-cache` và doctrine-scan chỉ đọc checkout gốc. Các script và output thật ở `evidence/`; script cũ được chép từ lượt 3 rồi CHẠY LẠI trên HEAD, không tái dùng output cũ.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / lớp / nguồn | Phân loại trên HEAD | Bằng chứng tự đo |
|---|---|---|
| F01 `reporter-thong-diep`, lượt 1 `30ee4ae`, lượt 2 `6cf0cc5`, lượt 3 `4c6f933` | **VÁ HỜ ở cấp lớp**; các biểu hiện đã báo trước đều **ĐÃ VÁ THẬT** | `probes.py`, `routes.py`, `transport_edges.py`, `edges3.py`, `unicode_stdio3.py`: suite/CLI/channel/transport không lặp loại, giữ 160 ký tự; nhật ký hai nhánh, foreign chốt và compiler đều đúng. setsid nay có PermissionError + 160 x; stdout ASCII nay có footer + 160 ✓, không UnicodeEncodeError. Còn hai đường cùng lớp: metadata cũ phát vào kênh khi lượt qua; lỗi I/O nhật ký qua excepthook thô. |
| F02 `khoa-encoding-chi-kiem-khoa`, lượt 1 `30ee4ae` | **ĐÃ VÁ THẬT trong hình dạng AST đã công bố** | `probes.py`, `encoding_edges.py`, `encoding_behavior.py`: thiếu encoding, cp1252, None, ascii, rỗng, giá trị động, errors strict/ignore/None/thiếu đều bị chính khóa giết. Unicode giải mã thật đúng; giữ giới hạn argv/text-mode đã khai từ lượt 1. |

`audit4.py`: áp HINT lượt 3 vào blob `4c6f933` trong scratch bằng `patch --batch -p0` rc=0; kết quả khớp HEAD từng byte. Khai “áp nguyên văn” đúng. Đây không phải bằng chứng bản hint trước đủ độ phủ; phản chứng mới vẫn được tính.

## BANG NGHIEM THU

Các lệnh dưới đây chạy từ thư mục review, trừ chỗ ghi cwd. Các script Python dùng ba biến offline nêu trên. `run_ab.py` clone local `--no-hardlinks --no-checkout`, checkout detached exact OID, ghim `core.abbrev=7` và tắt hooks chỉ trong clone thử nghiệm. Log đầy đủ, rc và thời gian nằm ở `ab-jobs.json`; không thay số của reviewer bằng số executor.

| Tiêu chí | Lệnh | Output/bằng chứng | Đạt? |
|---|---|---|---|
| N0: tái hiện Windows trước vá | Chưa chạy: `gh run view 41328709141 --repo ducthangho/tra-luat --log` | Bundle lịch sử khai TypeError `the JSON object must be str, bytes or bytearray, not NoneType` trên 4423d18. Không có log job gốc để tự kiểm `_readerthread`/cp1252 và thứ tự tái hiện → vá. | KHÔNG ĐO ĐƯỢC độc lập; không giả Windows |
| N0': Linux base cùng rig | `ls -d /tmp/.git`; `python3 evidence/run_ab.py` | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay); cả hai rc=1 | Đã đo nền, giữ lỗi nền |
| A1: assert/raise + khóa AST | `python3 evidence/inventory.py`; `python3 evidence/probes.py`; `python3 evidence/allowlist_edge.py` | 57 assert/11 ca chuyển, mismatches=[]; 8 raise/2 ca chuyển; còn 1 Assert + 3 Raise trong đúng ba ca cố ý. Chèn assert/raise, nested, raise Name, thêm tên thừa và bỏ raw cuối của tên cho phép đều chết bằng TinHieuChotCa của chính khóa. | ĐẠT phạm vi cú pháp SPEC + mở rộng |
| A2: cham_mot_ca giữ đúng 160 | `python3 evidence/probes.py`; `python3 evidence/detail_edges.py` | TypeError 500 x vẫn `loi`, đúng TypeError + 160 x; rỗng chỉ tên loại; Unicode 160 ký tự. Bỏ thông điệp/đổi trần đều chết đúng khóa A2. | ĐẠT A2; mục tiêu 3 toàn lớp CHƯA ĐẠT F01 |
| Mục tiêu 3: mọi đường chẩn đoán | `python3 evidence/routes.py`; `python3 evidence/extended4.py`; `python3 evidence/inventory4.py` | Tám reporter trong except đều đã cắt; kênh hong=0 vẫn chứa review-old; lỗi --nhat-ky có thông điệp FileNotFoundError 350 ký tự + traceback thô. | CHƯA ĐẠT F01 |
| Mục tiêu 4: encoding con Python | `python3 evidence/inventory.py`; `python3 evidence/encoding_edges.py`; `python3 evidence/encoding_behavior.py` | 18 subprocess text-mode Python trên HEAD, tất cả utf-8/replace; 14 call cũ thêm encoding, một call mới ở khóa Unicode; 22 text-mode hệ thống không đổi. Các giá trị sai đã bị khóa bắt trong hình dạng nhận diện. | ĐẠT phép đo static/Linux; nguồn gốc Windows chưa đo độc lập |
| A3: Windows exact HEAD | Không chạy Windows và không gọi mạng | Prompt chỉ có số fd1f82e (446/446, 118 không đo; suite 282/282, bỏ qua 74) và 4c6f933 (450/450); 93a9afe đang đo. Không có log/check-run exact HEAD. | KHÔNG ĐO ĐƯỢC; không nâng số HEAD cũ thành check mới |
| A4: Linux HEAD/base | `python3 evidence/run_ab.py`; `python3 evidence/summarize.py` | 328/351 ca DA CHAY QUA (tong 361, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 536/568 dat  (4 khong do duoc tren nen nay); tập hỏng/bỏ qua suite và mutant trùng base, delta=0 | ĐẠT điều khoản delta=0; không gọi suite/mutation là N/N xanh |
| A5: bare Ruff F | `python3 evidence/audit4.py`: `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` ở HEAD/base | Cả hai rc=1, 17 lỗi: 5 F841 ở launcher_test.py, 12 F821 ở tl.py; delta=0. Ruff 0.16.9; chưa đo pin CI 0.15.15. | ĐẠT delta với tool hiện có, không phải bare lint xanh |
| A5: doctrine | `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` (cwd cay-kho) | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 | ĐẠT |
| A5: whitespace | `git -C cay-kho diff --check c82047da4d6f9546ce1d68282c37acf9567b74bc 93a9afe7bda76c55349bf72ba4fe77455758365d` | Rỗng, rc=0 | ĐẠT |
| A5: ci.yml exact HEAD | Chưa chạy: `gh api repos/ducthangho/tra-luat/commits/93a9afe7bda76c55349bf72ba4fe77455758365d/check-runs` | Không có receipt/check-run hiện hành trong bundle; không gọi mạng | KHÔNG ĐO ĐƯỢC |
| A6 sau land | Chưa land, ngoài quyền reviewer | Không chạy | CHƯA ĐO ĐƯỢC theo SPEC |

## BANG DO

Đã đọc diff toàn packet, diff từ lượt 3, code/caller/consumer tương ứng và toàn bộ `git log --format=%B 4c6f933..HEAD`. `audit4.py` lưu mọi dòng thêm trong `audit.json` và toàn bộ message trong `commits.txt`. Phép trích chỉ đánh dấu các dòng thêm; không đặt trần tìm finding ở code cũ hoặc đường mặc định của Python. Không nhận “8 reporter trong except” làm bằng chứng cho mọi đường xuất lỗi.

| Khẳng định | Diff/commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| setsid giữ loại và 160 message | mo_ta_loi thay type(e).__name__, docstring khóa mới | `edges3.py`: helper và main đều 160 x/loại một lần; `probes.py`: hai mutant mất message/bỏ cắt đều own_signal=true | Có |
| Unicode không làm reporter chết dưới console không UTF-8 | Docstring r1122_reporter_unicode_console_khong_utf8 | `unicode_stdio3.py`: cùng probe base có footer, HEAD có footer + 160 ✓, không UnicodeEncodeError; `probes.py`: bỏ chuẩn hóa/đổi ASCII đều chết đúng khóa | Có cho stdout chuẩn được reconfigure; không hứa mọi sink tùy biến |
| Chuẩn hóa stdout/stderr ở main và chay_dot_bien | Helper mới, hai callsite và subject commit | Code có hai entry; phép đo luồng chuẩn và StringIO/fallback ở `streams4.py`, các runner/probe dùng cả direct và CLI | Có trong phạm vi đã đo |
| Bốn mutant mới thật sự khóa hai biểu hiện cũ | Bốn mục đầu DOT_BIEN_HARNESS trong diff lượt 3 | `probes.py`: 4/4 chết bằng TinHieuChotCa của chính ca, thông báo đúng nguyên nhân; full catalog đều OK | Có |
| HINT lượt 3 áp nguyên văn | hint_provenance của 93a9afe | `audit4.py`: patch rc=0, byte equality=true | Có |
| Lời khai lượt 2 đã bỏ sót setsid | Đính chính trong commit 93a9afe | Đối chiếu blob 4c6f933 và VERDICT-LUOT3, phép đo setsid cũ và mới | Có; không đo được quá trình tự suy nghĩ của executor |
| “30 khối except dùng e dựng chuỗi; 18 trong @ca, 12 hạ tầng” | Thân commit và prompt | `inventory4.py`: tất cả handler có tên = 33, đều dùng biến; 21 trong ca/12 hạ tầng. Predicate công khai xét str/repr/type/mo_ta_loi và FormattedValue dùng biến bắt lỗi cho 28 = 17 + 11. Năm khối còn lại chỉ làm logic/return/identity/append. `_CsSeam` không dựng chuỗi. | Không tái lập được 30/18 dưới hai phép đếm này. Không có predicate gốc trong bundle; không tự đoán nó. Ghi trong cùng kiểm kê/giới hạn F01, không tạo finding số học riêng từ định nghĩa mơ hồ |
| 12 hạ tầng phân được 8 reporter + 4 fixture | Danh sách `_wp1077_llm`, `_CsNhan`, `_CsSeam`, `_review6_registry_raw_phai_tu_choi` | `inventory4.py`: grouping theo vai trò đúng 8 + 4; riêng `_CsSeam` là giữ exception rồi raise, không formatter | Đúng grouping; không chứng minh mọi đường ngoài except đã đóng |
| Các reporter của F01 trước đều giữ 160 và không lặp loại | Yêu cầu kế thừa + sửa trước | `routes.py`, `transport_edges.py`, `detail_edges.py`, `probes.py`: TypeError/AssertionError/TinHieuChotCa, empty/Unicode/foreign/compiler/transport đều đúng | Có cho các biểu hiện cũ; lớp còn mở F01 |
| Khóa encoding đủ đúng giá trị trong cú pháp hiện có | Điều kiện AST kế thừa | `encoding_edges.py` + `probes.py`: 10 giá trị/keyword sai bị bắt; các dạng argv/text khác còn lọt như đã khai | Có, giữ giới hạn từ lượt trước; không có call sai hiện hữu trên HEAD |
| Không đổi phai_chet/loi/giet | Mục tiêu 3 | `probes.py`: tên có dấu phân cách/newline vẫn SAI, 0/1; foreign direct/child vẫn loi; own vẫn giet; stale channel hiện vẫn được consumer trả qua vì hong=0 | Có về chấm điểm; stale detail vẫn là sai dữ liệu chẩn đoán |

## BANG TEST

| Bộ | N/M/output | Bỏ qua/không đo | rc |
|---|---|---|---|
| BASE suite | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| BASE --dot-bien | DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| HEAD suite | 328/351 ca DA CHAY QUA (tong 361, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| HEAD --dot-bien | DOT BIEN: 536/568 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| HEAD chín khóa r1122 | 9/9 | 0 | 0 |
| HEAD 20 mutant wp1122 độc lập, giữ nguyên catalog | 20/20 giet, own_signal=true | 0 | 0 |
| Giá trị encoding/errors sai | 10/10 giet, own_signal=true | 0 | 0 |
| HEAD + hai guard bổ sung | 2/2 đỏ đúng lý do, own_signal=true | 0 | 0 (script xác nhận phản chứng) |
| HINT: khóa r1122 | 11/11 qua | 0 | 0 |
| HINT: mutant wp1122 | 25/25 giet, own_signal=true | 0 | 0 |
| HINT: runner child thật | 6/6 OK, giet 1/1 đúng ca | 0 | 0 |
| HINT: tương thích cũ | 7/7 qua | 0 | 0 |
| HINT: controls aggregate/stop | 4/4 đúng kỳ vọng (2 aggregate + 2 stop) | 0 | 0 |

Tập 23 ca suite đỏ giống hệt base/HEAD: r09_run_json_giu_ba_trang_thai_probe, r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh, r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe, r484_g2_doctor_doc_dung_home_da_materialize, r484_g2_hook_shell_scrub_truoc_probe, r484_g2_probe_isolated_marker_va_refresh, r484_g2_recovery_probe_rollback_va_snapshot_moi, r484_g2_schema_truoc_freshness_va_home_materialize, r484_g2_storage_kernel_guardrails, r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi, r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do, r484_g7_tu_choi_ghi_dung_ban_da_probe, r484_g8_hook_scrub_kin_voi_bash_env, r858_goc_tam_tranh_to_tien_co_git, r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC, r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat, r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m, r925_codex_qua_han_van_124_va_giu_khung_da_den, r925_rust_log_thua_ke_bi_GHI_DE_khong_noi, r926_dot_bien_tu_sinh_moi_thanh_phan_regex, r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC, r927_lenh_run_ghi_effort_va_sandbox_vao_run_json, t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac.

10 ca đường launcher.py run đỏ nền; 11 r484 vướng /tmp/.git/materializer; r858 và t86 vướng /var/tmp read-only. Mười bỏ qua giống nhau: hai native Windows và tám fixture phụ thuộc venv/pypdf không dựng được offline. Mỗi bên 32 mutant SAI do neutral đỏ; không biến chúng thành skipped. Bốn mutant không đo: 124_khi_chau_con_song, g2_windows_directory_pin_access, g4_windows_LA_not_current_owner, g4_windows_sid_alias_not_normalized. doctor_bo_do_bash ở cả hai là OK, giet 1/1 t73. Catalog base 552, HEAD 572; mọi mục có output. Toàn bộ 20 mutant tăng thêm của packet đều OK. Delta=0 nói về tập tên/trạng thái lỗi và bỏ qua, không nói text lỗi giống byte sau đổi kiểu ngoại lệ/thêm message.

## BANG SAN

Mỗi hàng có lệnh/output thật, không chỉ ý tưởng thử; dùng các chuỗi inert `x`, `review-old`, ✓ hoặc đường dẫn giả. Các script dựng fixture, đo và ghi output; chỉ các ca/mutant mới dùng TinHieuChotCa để quyết đúng nguyên nhân.

| Hướng độc lập | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| Tương đương điều kiện khi đổi assert/raise | `python3 evidence/inventory.py` | converted 57, cases 11, mismatches=[]; helper_raw=[] (helper cấp module); raw còn đúng ba ca | KHÔNG PHẢI LỖI |
| Allowlist mục dần | `python3 evidence/allowlist_edge.py`; `python3 evidence/probes.py` | Bỏ raw cuối của t119, thêm t73, chèn raw assert/raise đều giet/own_signal=true | KHÔNG PHẢI LỖI |
| Helper/alias/unittest/đăng ký trực tiếp | `python3 evidence/probes.py` | nested raw bị bắt; helper/alias/unittest/direct CA có thể lọt scanner, nhưng target là loi, không được ghi tín dụng giết | KHÔNG PHẢI lỗi mới; giới hạn cú pháp đã công bố |
| Giá trị bảng mã và errors | `python3 evidence/encoding_edges.py` | strict/ignore/None/thiếu, ascii/rỗng/động đều bị chính khóa giết | KHÔNG PHẢI F02 còn mở |
| Các dạng nhận diện con Python khác | `python3 evidence/probes.py`; `python3 evidence/encoding_edges.py` | sys.executable, argv biến, universal_newlines, text=1, implicit text có thể lọt; check_output với [PY], text=True bị bắt | KHÔNG PHẢI lỗi hiện hữu; không nâng scanner thành phân tích dữ liệu tổng quát |
| Byte Unicode thật và decoder replace | `python3 evidence/encoding_behavior.py` | HEAD `review ✓`; cp1252 `review âœ“` nhưng guard giet. Mutant nhận byte model sai bị r926 bắt. t73 vẫn chấp nhận note có U+FFFD | KHÔNG PHẢI tín dụng giết giả từ bản vá |
| Suite/CLI/kênh và loại lỗi | `python3 evidence/probes.py`; `python3 evidence/transport_edges.py` | TypeError/AssertionError/OSError/RuntimeError vẫn loi, loại một lần, message 160; CLI rc=1; own signal vẫn giet | KHÔNG PHẢI LỖI |
| Nhánh hook và dòng SAI | `python3 evidence/routes.py` | launcher/hook/harness neutral và false-credit đều TypeError + 160; harness real child SAI, giet 0/1 | KHÔNG PHẢI F01 cũ còn mở |
| Compiler thật | `python3 evidence/routes.py` | duplicate argument dài 500: SyntaxError + message 160 (141 x sau prefix), không in cả 500 | KHÔNG PHẢI F01 cũ còn mở |
| Nhật ký lỗi ca, empty/Unicode | `python3 evidence/routes.py` | TypeError/AssertionError/TinHieuChotCa giữ 160; empty chỉ loại; Unicode đúng 160 | KHÔNG PHẢI F01 cũ còn mở |
| stdout/stderr và fallback | `python3 evidence/unicode_stdio3.py`; `python3 evidence/streams4.py` | HEAD có footer/160 ✓ dưới ASCII; stdout và stderr đều xuất đúng ✓ dưới ASCII; StringIO/ValueError/OSError fallback qua | KHÔNG PHẢI LỖI trên luồng đã đo |
| setsid không tách được | `python3 evidence/edges3.py` | GROUP_DIAGNOSTIC và GROUP_MAIN có PermissionError + 160 x | KHÔNG PHẢI F01 lượt 3 còn mở |
| Metadata qua→hỏng→qua, lồng ca cùng tên | `python3 evidence/routes.py`; `python3 evidence/extended4.py` | hong=0, qua=1, rc=0 nhưng channel có TypeError/review-old; cả prelude lỗi lẫn lồng cùng tên đều tái hiện | LỖI F01: sai vòng đời dữ liệu, không phải đổi điểm |
| Ngoại lệ không qua except của reporter | `python3 evidence/extended4.py` | CLI --nhat-ky thiếu parent: FileNotFoundError message_length=350, traceback=true, rc=1 | LỖI F01: đường mặc định sys.excepthook chưa cắt |
| Kiểm kê toàn AST thay grep khoảng dòng | `python3 evidence/inventory4.py` | 33 named handlers, 28 có string/type use theo predicate; 31 print, hai helper nhận exception | Có sai khác với 30/18; không dùng số đếm làm chứng minh đóng lớp |
| Traceback formatter/repr/thread hooks | `python3 evidence/extended4.py`; `python3 evidence/inventory4.py`; `rg -n 'threading|Thread\(|traceback|excepthook|format_exc|repr\(e\)' cay-kho/.claude/dev/launcher_test.py` | Không có format_exc/custom excepthook assignment; hai repr(e) là logic @ca và đi qua reporter khi ca hỏng. Thread target trực tiếp lambda:None là fixture không start; luồng đọc sản phẩm nằm ngoài tệp được sửa. Raw main I/O đã có phản chứng ở trên. | Không thấy reporter thread tùy biến còn sót; Windows _readerthread KHÔNG ĐO ĐƯỢC native |
| Hai guard mới của hint | `python3 evidence/build_hint4.py` | HEAD + guard: 2/2 giet/own_signal=true, đúng hai message lỗi. Bản gợi ý 11/11 khóa r1122 qua; 25/25 mutant đúng tín hiệu; 52 neo đều duy nhất | KHÔNG PHẢI LỖI trong phép đo hint |
| Chống vá làm mất lỗi thật hoặc nuốt yêu cầu dừng | `python3 evidence/hint_controls4.py` | fail→pass với --lan 2 vẫn hong=1 + 160, own/TypeError phân loại đúng; SystemExit rc=7, KeyboardInterrupt rc=-2; 7 ca cũ qua; runner child thật 6/6 OK, gồm 5 mutant mới và neo cũ đã đổi | KHÔNG PHẢI LỖI trong phép đo hint |

## KIỂM KÊ LUỒNG CHI TIẾT LỖI

`inventory4.json` ghi source từng handler và từng chỗ dùng e; `outputs4.json` ghi toàn bộ print thật, không tính chuỗi mỏ neo trong catalog. Phép đếm không phải call graph đầy đủ; dưới đây là đường nguồn → consumer được gọi bằng probe, gồm cả đường không nằm trong except.

| Nguồn và dòng trên reviewed SHA | Nơi nhận/in | Đo và kết quả |
|---|---|---|
| mo_ta_loi:193, exception argument | cham_mot_ca:209/213 | Lỗi thường/foreign có loại + 160, own signal chỉ trả tên để chấm; probes/transport_edges |
| chay_bo_ca:15204/15211 | hong_ds → main suite/lap:15372/15395 | AssertionError và Exception đều một loại + 160; routes/probes |
| Cùng hai nhánh → ket | NhatKyCa.ra:15123 → ghi UTF-8/flush/fsync | Cả HONG/LOI đúng 160; routes.py gọi file thật, không nhận đã đo mất điện |
| CHI_TIET_HONG/LOAI_HONG:15205/15212 | main channel:15378/15380/15381 → cham_lap_ca:15171 | Lúc hỏng mới: type/message đúng; lúc ca qua: vẫn xuất giá trị cũ. routes/extended4: F01 |
| cham_lap_ca:15163 | harness neutral/SAI:15074/15077 | OSError/TimeoutExpired/ValueError/JSONDecodeError đúng 160; transport_edges/routes |
| cham_mot_ca → ket_luan_mutant:219 | product neutral/SAI:14976/14979 | Đúng 160; không parse detail để khớp tên; probes/routes |
| chay_dot_bien except hook:15009 | print:15022 | TypeError + 160; routes |
| chay_dot_bien SyntaxError:14951 | print:14952 | Compiler thật, đúng 160; routes/probes |
| _tu_tach_nhom_neu_can:2320 | main print:15327 | PermissionError + 160; edges3 |
| _cung_hoa_dau_ra_harness:15303 | main + chay_dot_bien, stdout/stderr | Luồng chuẩn UTF-8, fallback StringIO không chết; unicode_stdio3/streams4 |
| NhatKyCa.__init__:15112; ghi/flush/fsync/close:15113–15128 | main tạo nhật ký:15353/15387 hoặc các call ra/đóng; root:15400 không có boundary | open thiếu parent → sys.excepthook mặc định, message 350 + stack; extended4: F01. Flush/close chưa gây lỗi native, cùng đường không có bộ cắt ở biên CLI |
| Traceback mặc định ngoài main / thread | Không có handler/formatter tùy biến trong tệp | Không tùy tiện thêm lỗi module/thread để nhận là lỗi hiện hữu; không hứa clamp KeyboardInterrupt/SystemExit, vốn cần giữ quyền dừng |

Bốn helper fixture được executor nêu không phải bốn reporter độc lập: `_wp1077_llm` trả kết quả phép đo, `_CsNhan` chuyển sentinel escaped thành chốt, `_review6_registry_raw_phai_tu_choi` phân loại ValueError để chấm; `_CsSeam` giữ exception rồi raise. Lỗi ca cuối cùng đi qua reporter suite/đột biến. Các string nội bộ trong @ca, repr(e), exception cause, e.ma, kết quả logic và message kiểm thử không tự là một kênh xuất riêng; không cắt chúng sớm rồi làm đổi điều kiện chấm. Không ép tên ca/số đếm/lý do skip về 160.

## BANG LOP

| Slug / lịch sử | Biểu hiện đã đóng | Còn mở | Phép đóng lớp |
|---|---|---|---|
| reporter-thong-diep / F01, lượt 1–3 | Suite/channel lặp loại/transport; nhật ký thường/assertion; foreign chốt; compiler; setsid; Unicode console chuẩn | Hai biểu hiện: channel hong=0 mang chẩn đoán cũ; I/O nhật ký qua formatter mặc định không cắt. Một lớp, P1 | Ràng buộc chi tiết với lỗi của lượt đang báo; đưa Exception hạ tầng CLI qua formatter chung; guard/mutant riêng từng đường; kiểm cả preserve lỗi thật + yêu cầu dừng |
| khoa-encoding-chi-kiem-khoa / F02 lượt 1 | Các giá trị encoding/errors sai trong hình dạng static đã công bố | Không phát hiện biểu hiện mở trên HEAD trong phạm vi ấy | Giữ kết quả guard + decode Unicode thật; không đổi giới hạn scanner thành lời hứa rộng hơn |

## FINDINGS

### reporter-thong-diep [P1] F01 còn phát lại lỗi cũ và để lỗi nhật ký thoát ra traceback không cắt

TEP/DONG: `.claude/dev/launcher_test.py:15380` và `:15381` (producer mới của packet), `:15205`/`:15212` (map tồn lưu); `.claude/dev/launcher_test.py:15112`, `:15353`, `:15387`, `:15400` (lỗi I/O nhật ký và biên CLI).

VAN DE: `CHI_TIET_HONG` chỉ được ghi khi ca hỏng, không được gắn với một lượt báo cáo. `main --lap-ca` đọc nó vô điều kiện ngay cả khi `hong_ds=[]`. Một ca từng hỏng ở prelude/cùng tiến trình rồi qua — hoặc ca lồng cùng tên hỏng nhưng ca ngoài qua — tạo kênh mới có `qua=1,hong=0` và vẫn `loai=khac:TypeError,ten_loai=TypeError,thong_diep=review-old`. Đây là chi tiết sai nguồn và phát lại dữ liệu cũ; **không** nhận là tín dụng giết giả: consumer hiện kiểm hong trước nên vẫn trả qua. Lượt 3 đã đo tồn lưu nhưng coi không đổi điểm là không có lỗi; kiểm lần này phân biệt đúng điểm với đúng dữ liệu chẩn đoán. `thong_diep` là trường mới của packet; rò nội dung lỗi cũ ra file kết quả là sai hành vi của producer, dù consumer chấm điểm biết bỏ qua.

Biểu hiện thứ hai không có `except ... as e` tại nơi báo nên phép quét 8 reporter bỏ sót: lỗi khởi tạo/ghi nhật ký không được `main` hay entrypoint xử lý, Python in traceback qua `sys.excepthook`. Chạy đúng cờ --nhat-ky với thư mục cha chưa tồn tại đã tạo FileNotFoundError có message 350 ký tự, rc=1; không đi qua mo_ta_loi. Đường này có trước packet; mục tiêu 3/Q3 mới yêu cầu các reporter giữ loại/thông điệp giới hạn, nên vẫn thuộc kiểm đóng lớp, không gọi nó là hồi quy mới. Không đòi nuốt lỗi hay làm suite xanh khi I/O hỏng.

DA THU NGHIEM: `python3 evidence/routes.py`, `python3 evidence/extended4.py`, rc=0. Output STALE_CHANNEL/NESTED_SAME_NAME_CHANNEL giữ nguyên JSON nêu trên; JOURNAL_UNCAUGHT giữ stderr và số đo 350. `python3 evidence/build_hint4.py`, rc=0: thêm riêng hai guard vào HEAD đều đỏ bằng TinHieuChotCa của CHÍNH ca, với lần lượt “kenh ca qua mang chi tiet loi cu: truoc” và “loi I/O nhat ky thoat ra traceback hoac khong cat dung 160”. Không dùng FileNotFoundError/setup error làm tín dụng giết.

GOI Y VA — ở đâu: producer channel trong main là biên có đủ `hong_ds` của lượt đang báo; không chữa bằng cách cắt tiếp ở consumer vì nội dung sai nguồn vẫn đã được ghi ra file. Biên CLI là chỗ đưa Exception hạ tầng từ mở/ghi/đóng nhật ký và các thao tác main khác qua formatter chung; không sửa từng lệnh open/fsync riêng. Hai biểu hiện cần hai cơ chế: vòng đời metadata và xử lý ngoại lệ chưa bắt.

GOI Y VA — thế nào: đường rẻ nhất là chỉ xuất loai/ten_loai/thong_diep khi lượt hiện tại có hong_ds; ca qua hoặc bỏ qua thì ba trường null. Giữ chi tiết khi bất kỳ lần lặp nào trong lượt hỏng. Thêm biên `Exception` tại entry CLI, báo qua mo_ta_loi và rc khác 0; giữ SystemExit/KeyboardInterrupt ra ngoài. Đường dài hơn là bỏ map dùng chung, trả metadata gắn từng kết quả/lượt, mua thêm cô lập khi API được gọi lồng; không bắt buộc đổi chữ ký để vá hai phản chứng này. Lời khai kiểm kê cần kèm đúng predicate và danh sách, phân biệt handler có biến, handler dựng chuỗi và đường interpreter mặc định; không dùng một con số thay quét consumer.

CA KHOA: hai guard và năm mutant mới trong HINT.patch. Ba mutant bỏ ràng buộc một trong ba trường của channel phải chết đúng guard đầu; mutant bỏ biên xử lý hoặc bỏ cắt phải chết đúng guard I/O. Cập nhật neo mutant cũ wp1122_reporter_lap_lay_ca_loai theo biểu thức mới; không để catalog đỏ do neo không khớp. `build_hint4.py`: 11/11 guard xanh, 25/25 mutant chết đúng ca; `hint_controls4.py`: sáu mutant qua runner/child thật đều OK, gồm năm mới và mutant cũ được đổi neo. `patch --batch -p0` trên bản sao HEAD rc=0, byte equality=true; 52 neo harness duy nhất; Ruff của hint vẫn 5 F841 như HEAD.

NGUY CO BAN VA: xóa map mỗi lần ca qua có thể làm mất lỗi của lần lặp trước trong cùng --lan; phép đo fail→pass với --lan 2 đã khóa giữ hong=1, đúng loại + 160. Biên bắt Exception có thể che stack hữu ích để debug; phải giữ loại/message và rc=1, không tuyên bố thành công, không bắt BaseException. Control flow đã đo SystemExit rc=7 và KeyboardInterrupt rc=-2. Không cài sys.excepthook/threading.excepthook toàn cục làm đổi ca/luồng ngoài scope. Luồng tùy biến đóng/hỏng vẫn là giới hạn; không hứa báo lỗi khi chính stderr vật lý không ghi được. Không đo native Windows của hint, không chạy full suite/full catalog của hint; chỉ HEAD được chạy full theo yêu cầu.

HINT.patch: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Chỉ là bằng chứng/gợi ý trên cây riêng; không commit/push/sửa checkout executor.

DO TIN: cao về hai đường chạy và output, có âm/dương, own signal, file kênh và CLI thật. Chỉ có một lớp F01 được tính; số kiểm kê không tái lập và giới hạn của lời khai nằm trong cùng audit lớp này, không cộng finding giả từ khác định nghĩa đếm. Không phát hiện P0/P2/P3 độc lập mới trong phạm vi đo.

## TOAN VEN VA GIOI HAN

`source-initial.json` / `source-final.json` và `integrity.json`: same_files=true, same_identity=true, initial_clean=true, clean=true; 10459 tệp được băm ngoài .git, bao gồm ignored/untracked. HEAD/tree trước–sau khớp exact OID ở đầu verdict, working tree/index sạch. Đây là không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên; sandbox thực tế cho phép ghi workspace, checkout được giữ chỉ đọc bằng cách chọn nơi chạy. Bản sao tạm do lượt này tạo đã dọn; giữ script, log, JSON, HINT và bảng hash trong evidence/artifact-manifest.json. Không push, không gọi mạng hoặc credential thật.

N0/A3/check-run ci.yml exact HEAD và Ruff pin CI chưa đo độc lập; A6 chưa đến thời điểm. Không đổi các mục đó thành pass, không lấy lời khai cũ thay log đúng job Windows/exact SHA. Hướng kiểm exception chứa dữ liệu nhạy cảm chỉ mô tả bằng lời: lỗi API/subprocess có thể chứa dữ liệu người dùng và cắt 160 không phải redaction; không soạn payload nhạy cảm, không dùng credential thật.

Đã sửa rig probe direct-mutant để chỉ loại catalog khỏi vùng TÌM/THAY rồi lắp lại catalog nguyên vẹn khi chạy. Bản đo ban đầu bỏ cả catalog có thể làm khóa compiler đỏ vì thiếu cấu trúc; log direct-mutant cuối đã chạy lại bằng rig sửa, neutral nguyên vẹn và own signal đều đạt. Full A/B dùng nguyên tệp nên không bị ảnh hưởng.
