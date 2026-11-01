verdict: changes_requested
reviewed_sha: 5d21d552ba8799fe9a4a01ea42d2dc4311a4cdb3
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Review lượt 6, packet #1122 r1/g1, lease `wp1122-r1-g1-claude`, class sensitive, PR #1130. **changes_requested vì F01 còn đọc loại từ map dùng chung tại thời điểm không còn thuộc lỗi ngoài.** Đã tái hiện tín dụng giết giả qua runner thật. Một lớp nguyên nhân, ba biểu hiện: sai loại lỗi, lỗi thường thành giết, chốt thật thành lỗi.

Baseline: `c82047da4d6f9546ce1d68282c37acf9567b74bc`; candidate tree: `80e155bcba92aee45f1605da29be774619462080`. SPEC bytes khớp băm trong prompt. Chỉ review `.claude/`; diff thực khớp `diff.patch`, diff từ `365c7511f2255129e7d05fa59bb26425e1e988c1` khớp `diff-tu-luot5.patch`. Phần merge `ops/reviews/**` nằm ngoài đối tượng. Numstat candidate: **446 thêm, 93 xóa, 1 tệp**, dưới trần 450 dòng thêm.

Reviewer: Codex/OpenAI, họ GPT-6 theo danh tính phiên được cung cấp; shell Linux trong sandbox qua API, transport machine. Không có phép đo độc lập biến thể model/effort của từng request; không suy identity từ Git actor. Executor là Claude theo packet; không kế thừa context Executor. Authority cho review offline và hai mở rộng phạm vi là prompt.snapshot do chủ kho giao. Không xuất bản verdict qua mạng, không cấp quyền merge/land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / nguồn | Kết luận trên HEAD | Bằng chứng tự chạy |
|---|---|---|
| F01 lượt 1: suite/CLI không cắt, transport mất message | Các đường đó ĐÃ VÁ THẬT | `routes.py`: TypeError/AssertionError/chốt đều đúng loại + 160 ký tự; transport OSError/timeout/JSON đúng helper. `guards.py`, `mutation_probes.py`: khóa thật qua, bỏ loại/message/cắt bị chính ca giết. |
| F01 lượt 1: channel lặp loại/cắt cả prefix | PHẠM VI ĐÃ ĐỔI, không gọi là vá thông điệp | Chủ kho đã duyệt bỏ toàn bộ message khỏi channel. Thật sự không còn CHI_TIET_HONG/ten_loai/thong_diep; chi tiết harness lỗi thường chỉ còn `review_loi_con(khac:TypeError)`. Không mở finding vì quyết định này. |
| F01 lượt 2: nhật ký hai nhánh, foreign chốt, lỗi compiler | ĐÃ VÁ THẬT các biểu hiện đó | `guards.py`, `routes.py`: journal thật giữ loại + 160; foreign vẫn loi; compiler duplicate argument thật giữ SyntaxError + 160. Các mutant tương ứng own_signal=true. |
| F01 lượt 3: Unicode console và setsid | ĐÃ VÁ THẬT các biểu hiện đó | Khóa chạy child với PYTHONIOENCODING=ascii vẫn có tổng kết và đúng 160 ✓; setsid PermissionError giữ 160. Bỏ UTF-8/đổi ASCII/mất message đều chết đúng ca. |
| F01 lượt 4: channel khi không hỏng, lỗi I/O nhật ký | ĐÃ VÁ THẬT các biểu hiện đó | Hai fixture lỗi cũ/trong ca lồng nhưng lượt ngoài qua: hong=0, loai=null; hai field message vắng. `extended.py`: open/write/fsync/final/close đều rc=1, chi tiết cắt, không traceback cho Exception. SystemExit/KeyboardInterrupt giữ quyền dừng. |
| F01 lượt 5: lỗi ngoài rồi ca lồng ở lượt qua/bỏ qua sau | ĐÃ VÁ THẬT phản chứng đó; **VÁ HỜ ở cấp lớp** | `extended.py`: pass/skip/nested-error/nested-signal đều giữ khac:TypeError của lần hỏng ngoài. `reentrant.py` + `runner_reentrant.py`: ca lồng chạy ngay trong formatter, trước snapshot, vẫn đổi loại và cấp tín dụng giả. Đây là đường trước chưa đo; không khai bản vá mới sinh ra cơ chế này. |
| F02 lượt 1: encoding=None/cp1252 vẫn được khóa chấp nhận | ĐÃ VÁ THẬT trong hình dạng AST đã công bố | `encoding_edges.py`: 10 giá trị encoding/errors sai đều giet/own_signal=true; decoder UTF-8 thật đúng. Bốn giới hạn syntax/dataflow cũ vẫn được khai, không có call sai thuộc các dạng đó đang hiện hữu. |

Lớp F01 chưa đóng. Không dùng tổng suite, việc đã áp hint, hoặc thay phạm vi message làm bằng chứng đóng lớp.

## BANG NGHIEM THU

Các lệnh `python3 evidence/...` chạy từ thư mục review này. Dựng lại probe bằng `python3 evidence/setup_copies.py`; `run_ab.py` tự dựng cả hai vế sạch trong cùng một lệnh. Không chạy lệnh mạng.

| Tiêu chí | Lệnh | Output / phép đo | Đạt? |
|---|---|---|---|
| N0 Windows trước vá | NOT_RUN: đọc log job windows-latest của run 41328709141 | Không có Windows/log job gốc trong gói để tự đo; không gọi mạng. Chỉ có lời khai lịch sử về TypeError/NoneType trên 4423d18. Không xác nhận độc lập thứ tự tái hiện → ghi message → vá. | KHÔNG ĐO ĐƯỢC |
| N0' Linux baseline cùng rig | `python3 evidence/run_ab.py`; `python3 evidence/summarize.py` | BASE suite 319/342 đã chạy, tổng 352, bỏ qua 10, hỏng 23; mutation 516/548, 4 không đo; cả hai rc=1. | ĐÃ ĐO NỀN |
| A1 đổi assert/raise và khóa AST | `python3 evidence/inventory.py`; `python3 evidence/ast_edges.py`; `python3 evidence/mutation_probes.py` | Đổi 57 assert/11 ca + 8 raise/2 ca; điều kiện/message cũ mismatches=[]. Còn đúng tập 3 ca cố ý. Assert/raise mới, tên allowlist thừa hoặc mục dần đều chết bằng chốt chính khóa. Hai mutant A1 bắt buộc có trong DOT_BIEN_HARNESS và chạy OK. | ĐẠT phạm vi đã duyệt |
| A2 chi tiết cham_mot_ca | `python3 evidence/guards.py`; `python3 evidence/routes.py`; `python3 evidence/mutation_probes.py` | TypeError 500 x vẫn loi, tên loại một lần + đúng 160 x. Mutant bỏ message/đổi trần chết đúng r1122_loi_mang_thong_diep_cat_160. Empty/Unicode cũng đúng. | ĐẠT A2; toàn lớp F01 chưa đạt |
| Mục tiêu 3 reporter và channel | `python3 evidence/routes.py`; `python3 evidence/extended.py`; `python3 evidence/reentrant.py`; `python3 evidence/runner_reentrant.py` | Reporter cũ đã cắt. Tuy nhiên ReviewError ngoài → channel TinHieuChotCa; harness mutant neutral qua được báo OK giet 1/1. | CHƯA ĐẠT F01 |
| Mục tiêu 4 encoding | `python3 evidence/inventory.py`; `python3 evidence/scope_inventory.py`; `python3 evidence/encoding_edges.py` | 21 call subprocess Python text=True đều utf-8/replace; 14 call cũ bổ sung codec, 4 call mới so BASE; 22 call text-mode hệ thống không đổi. Unicode thật `review Đ ✓`; cp1252 giải sai và bị khóa bắt. | ĐẠT static/Linux; gốc Windows giữ N0 |
| A3 Windows exact candidate | NOT_RUN: đọc job windows-latest + runner_id + suite/mutation trên 5d21d55 | Prompt chưa có log exact candidate, chỉ có bằng chứng do executor khai trên SHA cũ, trong đó 365c751/run 41347208963. Không thay số SHA cũ vào HEAD. | KHÔNG ĐO ĐƯỢC |
| A4 Linux HEAD/base | `python3 evidence/run_ab.py`; `python3 evidence/validate_evidence.py` | HEAD suite 331/354, tổng 364, bỏ qua 10, hỏng 23; mutation 540/572, 4 không đo; rc=1. Tập hỏng và tập bỏ qua hai vế trùng; 24 mutant tăng thêm OK. Đã kiểm /tmp/.git trước đo. | ĐẠT điều khoản delta=0; không gọi full suite xanh |
| A5 bare Ruff F | `python3 evidence/audit.py` | Ruff 0.16.9, `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py`: hai vế rc=1, cùng 5 F841 + 12 F821, cùng diagnostic, delta=0. | ĐẠT delta tool hiện có; pin CI 0.15.15 chưa đo |
| A5 doctrine | Cùng audit.py: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` (cwd cay-kho) | rc=0; sạch, quét 10 tệp, 0 chỗ chép doctrine. Bytecode tắt. | ĐẠT |
| A5 whitespace | Cùng audit.py: `git diff --check BASE HEAD -- .claude` | rc=0, output rỗng. | ĐẠT |
| A5 check-run ci.yml exact HEAD | NOT_RUN: đọc check runs của exact candidate | Không có check-run/log độc lập offline. Ruff delta/doctrine không thay CI evidence. | KHÔNG ĐO ĐƯỢC |
| A6 sau land | Chưa đến thời điểm | Không land trong phiên này. | CHƯA ĐO |

## BANG DO

| Khẳng định trong diff/comment/commit từ lượt 5 | Diff khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Bỏ message khỏi channel | Xóa CHI_TIET_HONG, ten_loai, thong_diep; consumer chỉ lấy loai | `inventory.py`, `claims.py`, `extended.py`: 0 identifier CHI_TIET_HONG, channel thật chỉ có nonce/ten/qua/bo_qua/hong/loai. Fixture lỗi thường ra review_loi_con(khac:TypeError). | CÓ, đúng quyết định phạm vi |
| Loai chụp sau mỗi lượt NGOÀI có hỏng | `if h`, gán từ map ở main:15460 | `scope_inventory.py`: đúng một `.get` map ngoài logic test tham gia chấm. `extended.py`: giữ đúng qua các lần qua/bỏ qua sau. | CÓ về vị trí gán/điều kiện |
| “ca lồng cùng tên không đổi được loại”, lỗi ngoài không thành giết | Commit và comment quanh snapshot/channel | `reentrant.py`: __str__ chạy lồng sau map assignment; stdout ReviewError nhưng channel TinHieuChotCa. `runner_reentrant.py`: HEAD rc=0, DOT BIEN: 1/1 dat cho lỗi thường. | KHÔNG: F01; không đếm thêm finding cho cùng lời khai |
| Khóa mới phủ ca lồng | Bốn tổ hợp TypeError/chốt/RuntimeError và bỏ qua | `guards.py`, `extended.py`: 4/4 tình huống gốc đúng; `build_hint.py`: thêm tình huống formatter làm chính khóa đỏ đúng lý do. | ĐÚNG bốn tình huống đã viết, chưa đủ cả thời điểm lồng |
| Hai mutant mới có răng | Chụp cả lần qua và đọc map lúc ghi | `mutation_probes.py`: cả hai chết đúng khóa; `claims.py`: 51/51 entry neo duy nhất, compile, đủ target. | CÓ; chưa đo snapshot tức thời bị nhiễu |
| Mutant assertion sửa neo sau bỏ map chi tiết | Xóa prefix CHI_TIET_HONG trong neo | `mutation_probes.py`: mutant thật chết bằng chính r1122_reporter_giu_loai_va_cat_dung_thong_diep, vì suite không cắt. | CÓ |
| Các neo channel cũ cập nhật, ba mutant message bỏ | ro_0 đổi sang loai_luot; bỏ ro_1/ro_2/lap_lay_ca_loai, thêm hai | `claims.py`: 51 entry hiện tại; toàn catalog 576 dòng output đủ. Hai mutant mới thay ba mutant xóa: tổng giảm 1 so lượt 5. | CÓ |
| Ca + hai mutant lấy từ HINT lượt 5, chỉ giữ phép đo loại | hint_provenance trong commit 5d21d55 | `provenance.py`: áp được HINT gốc ở ../cr1122-l5/HINT.patch lên 365c751; giữ bốn tổ hợp/fixture/counter. Thay message dài bằng review-current; bỏ hai field; mutant thứ nhất đổi comment neo, mutant thứ hai giữ đúng cặp loai trong ba cặp cũ. | CÓ tính dẫn xuất/điều chỉnh; không byte-identical và commit không khai nguyên văn |
| “30 except dựng chuỗi = 18 ca + 12 hạ tầng”, trong đó 8 reporter | Lời khai lịch sử 93a9afe, prompt yêu cầu đo lại | `scope_inventory.py`: tại 93a9afe có 33 named handler/21 trong ca; predicate string/type công khai ra 28/17. HEAD 34/21 và 29/17 do thêm boundary CLI. Hiện có 9 reporter + 4 helper hạ tầng. | KHÔNG tái lập 30/18 dưới predicate này; không dùng số ấy làm chứng minh đủ đường |

Predicate công khai: FormattedValue dùng biến bắt lỗi, hoặc gọi str/repr/type/mo_ta_loi dùng biến đó. Nó có thể bỏ qua luồng dữ liệu gián tiếp và có thể nhận type dùng thuần logic; vì vậy không xem con số này là chứng minh độ phủ. Source của mọi handler/print được giữ trong inventory.json để kiểm nghĩa. Khác định nghĩa đếm lịch sử không được nâng thành finding số học độc lập; lỗi hiện tại có phản chứng hành vi riêng.

## BANG TEST

| Bộ | N/M | Bỏ qua / không đo / rc |
|---|---|---|
| BASE full suite | 319/342 đã chạy; tổng 352 | bỏ qua 10, hỏng 23, rc=1 |
| HEAD full suite | 331/354 đã chạy; tổng 364 | bỏ qua 10, hỏng 23, rc=1 |
| BASE --dot-bien | 516/548 | 4 không đo; 32 SAI; rc=1 |
| HEAD --dot-bien | 540/572 | 4 không đo; 32 SAI; rc=1 |
| Catalog output coverage | BASE 552/552; HEAD 576/576 | không thiếu/trùng dòng; 24 mục tăng thêm đều OK |
| HEAD r1122 trực tiếp | 12/12 qua | 0 bỏ qua; script rc=0 |
| HEAD wp1122 mutant trực tiếp | 24/24 own_signal=true | 0 bỏ qua; không nhận setup error là giết |
| AST edge | 4/4 chết đúng khóa | nested assert, bare raise Name, nested raise, allowlist mục dần |
| Encoding sai | 10/10 chết đúng khóa | 2 decoder control và 4 giới hạn syntax đo riêng |
| Reentrant reporter | 6 tổ hợp đo qua CLI/channel/consumer thật | 5 sai loại; 2 lỗi thường thành giet; 1 chốt thật thành loi; control chốt→chốt đúng |
| HEAD + HINT TEST | khóa hiện có đỏ bằng chính TinHieuChotCa | tình huống 4 khac:RuntimeError; chạy riêng tình huống 5 TinHieuChotCa cũng đúng own signal |
| Scratch control metadata cục bộ | 12/12 khóa r1122 qua | chỉ là đối chứng ngoài kho; không phải candidate đã review hoặc full gate |
| Mutant quay snapshot về map live | đỏ đúng khóa, own_signal=true | RuntimeError và TinHieuChotCa được kiểm riêng |
| Runner thật đối nghịch | HEAD xanh giả 1/1; control đỏ 0/1; mutant xanh giả 1/1 | neutral đều qua; không giả nonce/channel hoặc gán map trực tiếp |
| HINT áp -p0 / Ruff | áp rc=0, byte_equal=true; 5 F841 như HEAD | test-only +448/-93 so BASE; không vá producer, không nhận hint suite xanh |

Hai vế A/B được dựng trong MỘT invocation của run_ab.py, clone local sạch --no-hardlinks/checkout exact SHA/core.abbrev=7, TMPDIR riêng nhưng cùng cấu trúc, Python 3.13.18, PIP_NO_INDEX=1 và tắt bytecode. Không chạy test trên checkout nguồn. Suite BASE mất 296.92s, HEAD 307.34s; mutation BASE 330.33s, HEAD 366.86s. Các số là phép đo Linux ngày 01-11-2026 UTC, không thay số Windows.

Cùng 23 ca hỏng: 10 đường launcher.py run đã biết; 11 r484 vướng tổ tiên /tmp/.git; hai t86/r858 gặp /var/tmp read-only. Cùng 10 ca bỏ qua: hai native Windows, tám fixture phụ thuộc venv/pypdf không dựng được offline. Cùng 32 mutant SAI, đều neutral đỏ; không chuyển chúng thành skipped. Danh sách đầy đủ và hai delta-set rỗng ở ab-summary.json. Không xóa /tmp/.git, không đổi /var/tmp để che nền.

Bốn mutant không đo: 124_khi_chau_con_song, g2_windows_directory_pin_access, g4_windows_LA_not_current_owner, g4_windows_sid_alias_not_normalized. doctor_bo_do_bash cả hai OK, giet 1/1 t73. Không đọc kết quả Linux thành bằng chứng native Windows.

## BANG SAN

| Hướng độc lập | Lệnh | OUTPUT thật | Kết luận |
|---|---|---|---|
| Bảo toàn phép đổi assertion | `python3 evidence/inventory.py` | 57 assert/11 ca + 8 raise/2 ca; mismatches=[] | KHÔNG PHẢI LỖI |
| AST/allowlist đủ răng | `python3 evidence/ast_edges.py`; `python3 evidence/mutation_probes.py` | 4 edge + mutant thêm tên/chèn raw đều giet/own_signal=true | KHÔNG PHẢI LỖI |
| Giá trị codec/errors | `python3 evidence/encoding_edges.py` | 10/10 sai bị chính khóa bắt | KHÔNG PHẢI F02 còn mở |
| Giải mã Unicode thật | Cùng encoding_edges.py | utf-8: review Đ ✓; cp1252: review Ä� âœ“ | KHÔNG PHẢI LỖI hiện hữu |
| Giới hạn syntax/dataflow encoding | Cùng encoding_edges.py | sys.executable, argv biến, text=1, universal_newlines đều qua khóa khi bị đổi codec | GIỚI HẠN cũ đã công bố; chưa có call sai như vậy trên HEAD |
| Direct/suite/journal/foreign | `python3 evidence/routes.py`; `python3 evidence/guards.py` | loại + 160 x, empty chỉ loại; own giet, foreign loi; nhật ký đúng | KHÔNG PHẢI biểu hiện cũ còn mở |
| Lỗi transport và JSON | Cùng routes.py | OSError, TimeoutExpired, ValueError, JSONDecodeError đều qua mo_ta_loi | KHÔNG PHẢI LỖI |
| SAI product/neutral/hook/harness | Cùng routes.py | ba đường đầu TypeError + 160 x; harness chỉ khac:TypeError đúng phạm vi mới | KHÔNG PHẢI LỖI cũ |
| Lỗi compiler thật | guards.py + mutant compiler | SyntaxError duplicate argument thật, message đúng 160; mutant mất cắt bị chính ca giết | KHÔNG PHẢI LỖI |
| Console ASCII/setsid | guards.py + mutation_probes.py | tổng kết còn, ✓ đúng 160; PermissionError + 160; các mutant chết đúng ca | KHÔNG PHẢI LỖI |
| Channel không có lỗi / ca lồng ở lần sau | `python3 evidence/extended.py`; guards.py | hong=0 loai=null; hong=1 rồi nested-signal vẫn khac:TypeError | KHÔNG PHẢI phản chứng cũ còn mở |
| Reentrancy ngay trong formatter | `python3 evidence/reentrant.py` | ngoài ReviewError, trong chốt: channel TinHieuChotCa, consumer giet; ngoài chốt/trong RuntimeError: consumer loi | LỖI F01 |
| Tín dụng qua runner thật | `python3 evidence/runner_reentrant.py` | HEAD và mutant rc=0, DOT BIEN: 1/1 dat; control rc=1, DOT BIEN: 0/1 dat | LỖI F01 |
| I/O nhật ký và quyền dừng | `python3 evidence/extended.py` | 5 vị trí rc=1/đúng 160/không traceback; SystemExit=7, KeyboardInterrupt=-2 | KHÔNG PHẢI LỖI boundary |
| Các sink ngoài except | `python3 evidence/scope_inventory.py`; inventory.py; reporters-rg.txt | không custom excepthook/format_exc; hai repr(e) là logic ca; Thread trực tiếp chỉ tạo fixture, không start | Không thấy sink riêng khác còn sót trong phạm vi đo; Windows readerthread KHÔNG ĐO ĐƯỢC native |
| Neo mutation/provenance | `python3 evidence/claims.py`; provenance.py | 51 entry neo duy nhất/compile/đủ target; hai mutant dẫn xuất đúng phần loại | KHÔNG PHẢI LỖI |
| Khóa hồi quy mới có răng | `python3 evidence/build_hint.py`; `python3 evidence/hint_signals.py` | HEAD+khóa đỏ đúng ca; control 12/12; mutant live map đỏ đúng lỗi 4 và 5 | KHÔNG PHẢI lỗi giàn |

## KIỂM KÊ ĐƯỜNG CHI TIẾT

| Nguồn → sink | Phép đo / kết quả |
|---|---|
| mo_ta_loi:193 nhận exception làm đối số → direct:209/213 | routes/guards/mutants: empty, Unicode, 500 x, foreign đều đúng; đây cũng là điểm có thể gọi __str__ tái nhập |
| chay_bo_ca:15296/15302 → hong_ds → hai nhánh main in HONG | suite/journal thật và khóa reporter: đúng loại + 160, không ghép lặp loại |
| Hai handler đó → ket → NhatKyCa.ra/ghi/flush/fsync | guards/routes: đúng 160; **mo_ta_loi(e) ở ket chạy sau ghi LOAI_HONG**, tạo cửa F01 |
| Hai handler đó → LOAI_HONG → snapshot main:15460 → channel:15474 → cham_lap_ca | scope_inventory: một read live tham gia điểm; reentrant: sai nguồn dù `if h` đúng; F01 |
| cham_lap_ca lỗi OS/subprocess/JSON:15257 → harness neutral/SAI | routes: detail helper đúng. Lỗi từ channel chỉ còn loại theo quyết định chủ kho |
| cham_mot_ca → ket_luan_mutant → SAI/neutral các dòng 15070/15073 | routes: giữ đúng 160; phai_chet vẫn khớp theo tên ca |
| hook except:15103 → loi → dòng 15116 | routes: đúng 160 cho TypeError; không mất message |
| compiler:15045 → SAI:15046 | compiler thật giữ SyntaxError + 160 |
| setsid:2320 → main:15417 | PermissionError + 160 |
| CLI boundary:15495 → stderr | 5 điểm I/O đều cắt; không nuốt BaseException điều khiển dừng |
| stdout/stderr reconfigure → các print trên | child ASCII thật vẫn footer/160 ✓; sink tùy biến và native Windows không được nhận đã đo |
| _wp1077_llm, _CsNhan, _CsSeam, _review6_registry_raw_phai_tu_choi | Bốn helper fixture, không phải bốn reporter độc lập: trả dữ liệu logic/ném lại/kiểm danh tính. _CsNhan dựng thông điệp chốt rồi được reporter cắt; _CsSeam không dựng chuỗi |
| repr và hooks interpreter | Hai repr(e) thuộc logic @ca; không format_exc/sys.excepthook/threading.excepthook riêng. Không chèn một lỗi import/luồng không tồn tại rồi gọi là lỗi hiện hữu |

Tất cả 34 named handler và 32 print site được lưu kèm source trong inventory.json. 13 handler hạ tầng hiện tại = 9 reporter + 4 fixture; 21 nằm trong @ca. Kiểm kê không lấy grep vùng dòng làm trần; đường channel ngoài except và lời gọi formatter đều đã được đo riêng.

## BANG LOP

| Slug / IDs | Đã đóng hoặc đổi phạm vi | Còn mở | Phép đóng lớp |
|---|---|---|---|
| reporter-thong-diep / F01 lượt 1–5 | Cắt ở direct/suite/journal/compiler/hook/transport/setsid; Unicode; I/O CLI; channel lượt qua; lồng ở lượt sau. Message channel được gỡ theo authority, không tính là sửa thông điệp | P1: snapshot đọc map sau reentrant formatter; ba biểu hiện sai loại/tín dụng giả/mất giết thật | Loại đi cùng kết quả của chính invocation ngoài, độc lập map global; kiểm lồng trước, trong, sau lỗi và qua/bỏ qua |
| khoa-encoding-chi-kiem-khoa / F02 lượt 1 | Giá trị utf-8/replace đã được kiểm; mutant sai giá trị bị chính khóa bắt | Không có biểu hiện mở trong shape scanner đã công bố | Giữ mutant giá trị và nêu giới hạn argv/text-mode, không khai là dataflow toàn diện |

## FINDINGS

### reporter-thong-diep [P1] F01: snapshot vẫn nhận loại do formatter lồng ghi đè, cấp tín dụng giả ngay --lan 1

TEP/DONG: `.claude/dev/launcher_test.py:15460` đọc LOAI_HONG; nhánh thường ghi map ở `:15304` rồi gọi lại mo_ta_loi ở `:15305`; nhánh assertion tương tự `:15299`/`:15301`. Consumer tin loại tại `:15264`–`:15267`. Comment `:15459` và `:15472` mô tả ảnh lỗi ngoài rộng hơn cơ chế bảo đảm.

VAN DE: chỉ dời `.get` từ lúc ghi JSON đến sau chay_bo_ca chưa gắn loại với kết quả trả về. chay_bo_ca bắt lỗi ngoài ReviewError(TypeError), thêm message vào hong_ds và ghi khac:ReviewError vào map; sau đó mo_ta_loi(e) cho biến ket gọi `str(e)` lần nữa. __str__ của lỗi gọi chay_bo_ca lồng cùng ca, bên trong ném TinHieuChotCa, đã bị handler lồng bắt và ghi map. Lời gọi ngoài trả h có lỗi ReviewError thật nhưng main đọc map thành TinHieuChotCa. Không có lỗi chốt nào thoát khỏi ca ngoài. Chỉ một lần lặp vẫn sai.

DA THU NGHIEM:

- `python3 evidence/reentrant.py`, script rc=0: 6 tổ hợp outer TypeError/AssertionError/TinHieuChotCa × inner RuntimeError/TinHieuChotCa. TypeError và AssertionError ngoài + chốt trong đều direct=loi nhưng channel TinHieuChotCa và cham_lap_ca=giet. Chốt ngoài + RuntimeError trong direct=giet nhưng cham_lap_ca=loi. Stdout vẫn báo đúng ReviewError: review-outer. Mỗi lần có qua=0, bo_qua=0, hong=1. Không gán map trực tiếp, không đọc nonce hoặc giả channel.
- `python3 evidence/runner_reentrant.py`, script rc=0: neutral cùng ca qua, mutant mới làm ca ngoài ném ReviewError có __str__ lồng. CLI --dot-bien HEAD báo `review_reentrant OK giet 1/1: review_repeat`, `DOT BIEN: 1/1 dat`, rc=0. Scratch control dùng loại thuộc kết quả cục bộ báo `SAI giet 0/1 ... [tin dung gia: review_repeat(khac:ReviewError)]`, `DOT BIEN: 0/1 dat`, rc=1. Quay riêng snapshot về map live lại xanh giả 1/1. Đây là điểm chấm thật, không chỉ JSON chẩn đoán sai.
- Khóa hiện có trên HEAD vẫn xanh vì bốn fixture chỉ lồng ở lần lặp sau. `build_hint.py` giữ bốn fixture đó, thêm hai callback __str__. HEAD + khóa tăng cường chết bằng TinHieuChotCa của chính r1122_kenh_loi_phai_thuoc_luot_ngoai: `...: 4 khac:RuntimeError`. `hint_signals.py` tách trường hợp chốt: `...: 5 TinHieuChotCa`, own_signal=true. Không nhận FileNotFoundError, lỗi setup hay chốt của ca khác làm giết.

VÁ Ở ĐÂU: dữ liệu kết quả của chay_bo_ca và ranh giới đọc kết quả ở main, không ở chuỗi hiển thị hoặc consumer JSON. Consumer không thể biết loại nhận được thuộc invocation nào. Việc gọi formatter là thực thi mã của exception nên không được để quyền phân loại phụ thuộc map sau bước đó.

VÁ THẾ NÀO: đường hẹp nhất là trả kèm loại đã tính từ ngoại lệ thật trong dữ liệu thuộc CHÍNH lời gọi chay_bo_ca; main lấy metadata của h vừa trả và giữ nó qua lượt qua/bỏ qua. Có thể giữ hình dạng tuple/list hiện có cho các caller nhưng kết quả phải sở hữu metadata riêng, không đọc lại LOAI_HONG để cấp điểm. Chụp loại trước các callback formatter/journal và không cho lời gọi lồng sửa metadata đó; không parse tên loại từ thông điệp format. Nếu có nhiều lỗi/lần lặp, giữ rõ chính sách lỗi ngoài cuối cùng như hiện tại. Bước rộng hơn là dùng kết quả cấu trúc cho mọi consumer và loại map toàn cục khỏi authority; không cần đưa việc thay toàn bộ --lap-ca của #1117 vào packet này.

CA KHÓA VÀ ĐỘT BIẾN: HINT.patch chỉ gia cố ca hiện có, thêm reentrancy TypeError→RuntimeError và TypeError→TinHieuChotCa, vẫn giữ bốn control lượt 5. Scratch control metadata cục bộ qua 12/12 khóa; mutant chỉ đổi snapshot cục bộ về `.get` map chết đúng khóa ở tình huống 4 và 5. Script/neo/thay thật nằm trong build_hint.py và hint_signals.py. Hai biến thể lớp assertion/chốt ngoài được đo thêm trong reentrant.py. Không tạo ca mới không có phản chứng.

NGUY CƠ BẢN VÁ: chỉ cache message một lần có thể chặn riêng callback __str__ này nhưng vẫn giữ quyền đọc global sau callback khác; không coi đó là đóng lớp. Không chụp vô điều kiện lúc qua/bỏ qua; không xóa lỗi thật của lượt trước; không đổi ngoại lệ lớp khác/cùng tên thành chốt; giữ own/foreign signal và quyền dừng SystemExit/KeyboardInterrupt. Caller/mutant dựa chữ ký, kiểu tuple hoặc neo literal có thể cần cập nhật; phải đo lại neo độc lập, không nhận lỗi neo là giết. Không tự mở scope #1117.

HINT.patch: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Patch -p0 từ cay-kho/, chỉ sửa TEST hiện có; HEAD+HINT cố ý đỏ để đặc tả lỗi, không phải bản vá producer. Hướng sửa producer được mô tả ở trên theo giới hạn patch-as-hint cho tooling tham gia authority của protocol §7–8. Đã áp thật trên cây bỏ được, byte-match với hint-tests-source.py; cumulative so BASE +448/-93, vẫn dưới 450. Scratch control +461/-102 chỉ là phản chứng khả thi, chưa tối ưu kích thước, không giao làm patch để áp hoặc xin nới trần. Không chạy full catalog/full suite trên control, không đo Windows.

ĐỘ TIN: cao. Có ngoại lệ thường/chốt thật, đối chứng direct, CLI/channel/consumer/runner thật, neutral qua, sửa riêng nguồn metadata đổi kết luận, mutant quay lại tái hiện. Một F01 P1; không có P0/P2/P3 độc lập khác trong phạm vi đã đo.

## TOÀN VẸN VÀ GIỚI HẠN

N0/A3 và ci.yml exact HEAD chưa tự đọc độc lập vì không có Windows và prompt cấm mạng. Pin Ruff CI chưa đo; bare Ruff 0.16.9 có delta=0 được khai riêng. A6 chưa đến thời điểm. Không thay các trạng thái ấy bằng lời khai executor hoặc kết quả Linux.

Hướng kiểm nội dung nhạy cảm chỉ mô tả bằng lời: exception của API/subprocess có thể mang dữ liệu người dùng ở đầu thông điệp; cắt 160 không là redaction. Không soạn payload nhạy cảm, không dùng credential thật. Không đổi cay-kho/, không push, không gọi mạng.

Hai sai sót của rig riêng đã sửa trước kết luận: fixture runner đầu có neo xuất hiện thêm trong literal catalog nên báo SAI neo (đã tách literal và chạy lại đủ 3 control); phép provenance ban đầu thử đòi byte-identical, trong khi commit chỉ khai dẫn xuất/giữ phần loại (đã đo riêng khác biệt và normalized pairs). Không dùng hai kết quả setup đó làm finding hoặc kill. Các log/JSON cuối giữ kết quả đã sửa.

Snapshot/cleanup và manifest cuối được ghi bên dưới sau khi mọi tiến trình đo đã kết thúc.

Final readback: source-initial.json/source-final.json băm 10459 tệp ngoài .git, kể cả ignored/untracked; same_files=true, same_identity=true, clean=true; staged/unstaged diff rc=0. HEAD/tree đúng các OID trên. Đây chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Sandbox thực tế workspace-write; không tự nhận mount read-only.

Đã dọn bốn thư mục copy-base/copy-head/tmp-base/tmp-head của riêng lượt này; giữ script/log/JSON/HINT và hai nguồn test/control phục vụ tái lập. Dựng lại bằng setup_copies.py cho probe hoặc run_ab.py cho cả A/B. Artifact-manifest.json chứa size/SHA-256 hiện vật, không tự băm chính nó. Hoàn tất 2026-11-01T22:42:54.759026+00:00.
