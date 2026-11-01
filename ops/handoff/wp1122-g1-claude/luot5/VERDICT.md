verdict: changes_requested
reviewed_sha: 365c7511f2255129e7d05fa59bb26425e1e988c1
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Packet #1122 r1/g1, lease `wp1122-r1-g1-claude`, review_class `sensitive`, lượt 5/10. Ngưỡng của chủ kho: hết P1/P2/P3 mới approve. Chỉ đánh giá phần `.claude/`; thay đổi `ops/reviews/**` của merge master không được tính là code packet. Hai mở rộng đã được duyệt (raise AssertionError và encoding mọi con Python text-mode) được tính vào nghiệm thu.

Reviewer: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; không có đo độc lập biến thể model/effort của từng request. Execution surface: công cụ shell Linux cục bộ qua API trong sandbox, transport machine; không tự khai ChatGPT Web/human-mediated hay đã đo Windows. Executor Claude theo assignment. Không đăng GitHub, không push/merge/land, không gọi mạng hoặc credential thật. Verdict này không cấp authority tích hợp.

Immutable acceptance baseline: `c82047da4d6f9546ce1d68282c37acf9567b74bc`; candidate: `365c7511f2255129e7d05fa59bb26425e1e988c1`, tree `a6ec933b7691d38adb6a219ea95bc4fb4facd519`. Local SPEC.md khớp byte hash được assignment giao; nguồn authoritative ngoài bundle chưa thể đọc độc lập do chỉ thị offline. `diff.patch` và `diff-tu-luot4.patch` khớp byte với Git; numstat 408 thêm/93 xóa, một tệp. `claims.py` giữ lệnh và thân commit đầy đủ.

Môi trường Python 3.13.18, Ruff 0.16.9. `/tmp/.git` tồn tại, rỗng/read-only; `/var/tmp` read-only. Giữ nguyên hai điều kiện, không đổi permission để làm xanh. Suite và mutation chạy trên hai clone cục bộ `--no-hardlinks --no-checkout` cùng kiểu, checkout đúng BASE/HEAD, core.abbrev=7, TMPDIR riêng. Env `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`, bỏ CODEX_AUTH_JSON kế thừa. Tất cả probe/mutant chạy ngoài `cay-kho/`; Ruff --no-cache và doctrine-scan chỉ đọc checkout gốc.

Các lệnh dưới đây chạy từ thư mục review (cha của `cay-kho/`), trừ dòng ghi rõ cwd. `run_ab.py` dựng clone và chạy cả hai lệnh trên mỗi vế. Sau khi bản sao đã dọn, có thể dựng riêng bằng `python3 evidence/setup_copies.py` rồi chạy các probe; để chạy lại full A/B từ đầu, dùng run_ab.py khi chưa có hai copy đó. Không dùng output cũ làm kết quả lượt này. Mỗi script lưu log/JSON và kiểm các hậu điều được nêu; toàn bộ hiện vật ở evidence/.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / nguồn | Kết luận trên HEAD | Bằng chứng tự đo |
|---|---|---|
| F01 `reporter-thong-diep`, lượt 1–4 | **VÁ HỜ ở cấp lớp**; mọi biểu hiện cụ thể đã báo trước **ĐÃ VÁ THẬT**; còn một biến thể sai nguồn metadata | 11/11 khóa cũ qua; routes.py/extended.py: suite, lap, transport, nhật ký, compiler, hook, setsid, Unicode và I/O CLI đều đúng. Nhưng lượt có lỗi rồi qua/bỏ qua với ca lồng cùng tên vẫn lấy metadata của ca lồng. Xem finding bên dưới. |
| F02 `khoa-encoding-chi-kiem-khoa`, lượt 1 | **ĐÃ VÁ THẬT trong hình dạng AST đã công bố** | encoding_edges.py: thiếu/cp1252/None/ascii/rỗng/động; errors strict/ignore/None/thiếu đều bị chính khóa giết. Decode thật đúng chữ. Giới hạn syntax/dataflow được ghi riêng, không gọi scanner là chứng minh tổng quát. |

Lượt 4 sửa channel khi `hong_ds=[]` và thêm boundary Exception ở CLI. Cả hai phản chứng cũ nay xanh; không lấy việc áp hint làm bằng chứng đúng. Phép đo mở rộng lần này giữ `hong_ds` có lỗi thật, rồi gây nhiễu metadata bằng ca lồng ở lần qua sau đó. Đây vẫn cùng lớp F01, không tạo slug mới để mất lịch sử.

## BANG NGHIEM THU

| Tiêu chí | Lệnh / cách kiểm | Output thật / giới hạn | Đạt? |
|---|---|---|---|
| N0 Windows, trước vá | Đọc SPEC/prompt và Git history cục bộ; không có log job gốc | Lịch sử báo run 41328709141, TypeError do json.loads nhận None; không tự đọc runner/log/thứ tự tái hiện→vá | KHÔNG ĐO ĐƯỢC độc lập; không quy thành finding code |
| N0' Linux cùng rig | `ls -d /tmp/.git`; `python3 evidence/run_ab.py` | Base suite 319/342, tổng 352, bỏ qua 10, hỏng 23, rc=1; `DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay)`, rc=1 | Đã đo nền |
| A1 chuyển assert/raise, khóa AST | `python3 evidence/inventory.py`; `python3 evidence/mutation_probes.py`; `python3 evidence/ast_edges.py` | Đủ 57 assert/11 ca + 8 raise/2 ca; mismatches=[] cho điều kiện/message cũ. Còn 1 Assert + 3 Raise trong đúng ba ca cố ý. Chèn assert/raise, nested, raise Name, allowlist thừa/mục dần đều giet/own_signal=true | ĐẠT trong phạm vi SPEC + mở rộng |
| A2 chi tiết trực tiếp | `python3 evidence/guards.py`; `python3 evidence/mutation_probes.py`; `python3 evidence/routes.py` | TypeError 500 x vẫn loi; loại một lần + đúng 160 x; mutant bỏ message/đổi trần chết đúng ca. Empty và Unicode cũng đúng | ĐẠT A2; mục tiêu 3 toàn lớp chưa đạt F01 |
| Mục tiêu 3 mọi reporter | `python3 evidence/routes.py`; `python3 evidence/extended.py`; `python3 evidence/inventory.py` | Các đường cũ đã giữ 160; channel của lượt hỏng→qua có lỗi ca lồng lấy sai type/message | CHƯA ĐẠT F01 |
| Mục tiêu 4 encoding | `python3 evidence/inventory.py`; `python3 evidence/encoding_edges.py` | 20 call Python text=True đều utf-8/replace; 14 call cũ thêm encoding, 3 call mới so BASE; 22 call hệ thống không đổi. UTF-8 thật ra `review Đ ✓`, cp1252 ra chữ sai và bị khóa bắt | ĐẠT phép đo static/Linux; gốc Windows không tự đo |
| A3 Windows exact HEAD | Không chạy Windows, không gọi mạng theo chỉ thị | Bundle chỉ có lời khai Windows trên SHA cũ: 93a9afe run 41341295220, suite 287/287, mutation 454/454. Không có log/check-run độc lập cho 365c751 | KHÔNG ĐO ĐƯỢC; không nhận SHA cũ thay HEAD |
| A4 Linux HEAD/base | `python3 evidence/run_ab.py`; `python3 evidence/summarize.py` | HEAD 330/353, tổng 363, bỏ qua 10, hỏng 23, rc=1; `DOT BIEN: 541/573 dat  (4 khong do duoc tren nen nay)`, rc=1. Tập hỏng và tập bỏ qua suite/mutation trùng base | ĐẠT điều khoản delta=0; không gọi N/N xanh |
| A5 bare Ruff F | `python3 evidence/audit.py`: ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py trên HEAD/base | Cả hai rc=1: 5 F841 + 12 F821; cùng diagnostic theo file/code/message, delta=0. Tool 0.16.9 | ĐẠT delta tool hiện có; chưa đo pin CI 0.15.15 |
| A5 doctrine | Cùng audit.py, cwd cay-kho: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine; rc=0 | ĐẠT |
| A5 whitespace | Cùng audit.py: `git diff --check BASE HEAD -- .claude` | Output rỗng, rc=0 | ĐẠT |
| A5 ci.yml exact HEAD | Không có check-run/log offline | Không chạy API; không suy CI xanh từ trạng thái cục bộ | KHÔNG ĐO ĐƯỢC |
| A6 sau land | Chưa land trong phạm vi phiên | Không dùng review làm hậu-merge evidence | CHƯA ĐẾN THỜI ĐIỂM |

## BANG DO

| Khẳng định | Diff/commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Guard channel không mang lỗi cũ khi lượt qua | Hai fixture trước/lồng, --lan 1 | guards.py; mutation_probes.py: guard qua, ba mutant xuất live map đều chết đúng guard | Có cho hong=0; chưa đủ cho lượt có lỗi thật rồi bị nhiễu map |
| Ba field chỉ xuất khi có hong_ds | Ba điều kiện ở producer main; title commit | extended.py: control hong=0 trong guard cũ đúng; fail→pass/skip giữ lỗi; nested-error/signal lại sai nguồn | Đúng điều kiện tồn tại lỗi; không đủ đóng F01 |
| Lỗi I/O nhật ký không traceback dài | Guard mới thử mở parent thiếu; entry Exception | guards.py; extended.py: mở/ghi/fsync/final/đóng đều rc=1, loại + message 160, không traceback. SystemExit 7/KeyboardInterrupt -2 giữ quyền dừng | Có; ngoài lỗi mở, bốn vị trí còn lại được fault-injection, không khai lỗi filesystem native |
| Hai mutant bỏ boundary/bỏ cắt có răng | Hai entry DOT_BIEN_HARNESS mới | mutation_probes.py: từng entry chết bằng TinHieuChotCa của chính guard I/O, không phải setup error | Có |
| Neo wp1122_reporter_lap_lay_ca_loai đã cập nhật | Thay literal khớp producer mới | claims.py: toàn bộ 52 entry có neo duy nhất; mutation_probes.py: mutant cũ đó chết đúng ca | Có |
| Áp NGUYÊN VĂN HINT lượt 4 | Thân commit 365c751 | claims.py: diff khớp bundle và đúng cơ chế/guard/mutant mô tả trong VERDICT-LUOT4; HINT lượt 4 nguyên gốc không có trong bundle để áp lại rồi so byte | KHÔNG ĐO ĐƯỢC mức nguyên văn; không cáo buộc sai provenance |
| “30 except dựng chuỗi = 18 ca + 12 hạ tầng” | Lời khai lịch sử 93a9afe, được prompt yêu cầu kiểm lại | inventory.py predicate công khai: HEAD 34 named handler, đều dùng biến = 21 trong ca + 13 hạ tầng; string/type predicate 29 = 17 + 12. Boundary mới thêm 1; trừ nó cho số lượt 4 là 33/28. Không có predicate gốc để tái lập 30/18 | Không tái lập dưới predicate này; không coi sai khác định nghĩa đếm là finding số học độc lập |
| Chỉ còn chín handler reporter, bốn helper fixture | Kiểm lại lớp, không dựa grep khoảng dòng | inventory.json giữ source tất cả handler và 32 print; chín handler reporter gồm direct 2, setsid 1, lap transport 1, suite 2, compiler 1, hook 1, CLI 1; bốn helper không tự xuất độc lập | Phù hợp kiểm kê hiện tại; còn channel ngoài except được đo riêng |

Predicate string/type: có FormattedValue dùng biến bắt lỗi, hoặc gọi str/repr/type/mo_ta_loi dùng biến đó. `_CsSeam` giữ và ném lại exception, không dựng chuỗi; `_wp1077_llm`, `_CsNhan`, `_review6_registry_raw_phai_tu_choi` phục vụ logic fixture. Không cắt dữ liệu logic nội bộ để làm thay đổi điều kiện chấm. Hai repr(e) thật ở 10523/10671 là logic @ca. Không có format_exc/custom sys.excepthook/threading.excepthook trong AST; Thread trực tiếp tại 12613 là đối tượng fixture không start. Không tự chèn lỗi module/luồng ngoài đường hiện hữu rồi gọi đó là lỗi HEAD.

## BANG TEST

| Bộ | N/M | Bỏ qua / rc |
|---|---|---|
| BASE full suite | 319/342 đã chạy, tổng 352 | bỏ qua 10; hỏng 23; rc=1 |
| HEAD full suite | 330/353 đã chạy, tổng 363 | bỏ qua 10; hỏng 23; rc=1 |
| BASE --dot-bien | DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | rc=1 |
| HEAD --dot-bien | DOT BIEN: 541/573 dat  (4 khong do duoc tren nen nay) | rc=1 |
| HEAD khóa r1122 trực tiếp | 11/11 qua | 0 bỏ qua; rc=0 |
| HEAD wp1122 direct mutant | 25/25 chết đúng ca/own_signal=true | 0 bỏ qua; rc=0 |
| AST edges | 4/4 chết đúng khóa | 0 bỏ qua; rc=0 |
| Encoding giá trị sai | 10/10 chết đúng khóa | 0 bỏ qua; rc=0; thêm decode Unicode thật và bốn giới hạn syntax |
| HEAD + guard mới | 1/1 đỏ đúng lý do metadata lồng, own_signal=true | Không nhận lỗi hạ tầng là giết |
| HINT khóa r1122 | 12/12 qua | 0 bỏ qua; rc=0 |
| HINT wp1122 mutant | 27/27 đúng own signal | 0 bỏ qua; rc=0 |
| HINT runner/child thật | 6/6 entry OK, giet 1/1 | gồm 2 mới + 4 neo cũ đã đổi; rc=0 |
| HINT tương thích | 6/6 ca cũ qua | t90, t91, t99, t119, r1079 direct và neutral; rc=0 |

Hai vế full có đúng cùng 23 tên ca hỏng: 10 ca đường run đã biết, 11 r484 do tổ tiên có .git, hai ca liên quan /var/tmp read-only. Tên lỗi/skip đầy đủ và hai delta-set rỗng ở ab-summary.json. Không xóa /tmp/.git hay đổi /var/tmp để che nền. Message được thêm type/cắt là thay đổi mục tiêu packet nên không so text diagnostic thô của base/head; so tập ca/đột biến và trạng thái. Trên HEAD Linux: g4_windows_sid_alias_not_normalized và g4_windows_LA_not_current_owner KHÔNG ĐO ĐƯỢC (native SID conversion); g2_windows_directory_pin_access KHÔNG ĐO ĐƯỢC (native Windows share-delete pin); doctor_bo_do_bash OK, giet 1/1 bằng t73. Log Linux không chứng minh Windows A3.

## BANG SAN

| Hướng độc lập | Lệnh | Output thật | Kết luận |
|---|---|---|---|
| Bảo toàn điều kiện/message đổi assert | `python3 evidence/inventory.py` | 57 assert/11 ca, 8 raise/2 ca; mismatches=[] | KHÔNG PHẢI LỖI |
| Allowlist mục dần / nested / bare raise Name | `python3 evidence/ast_edges.py`; `python3 evidence/mutation_probes.py` | 4 edge và mutant thêm tên/chèn raw đều giet/own_signal=true | KHÔNG PHẢI LỖI |
| Giá trị encoding/errors sai | `python3 evidence/encoding_edges.py` | 10/10 bị guard bắt | KHÔNG PHẢI F02 còn mở |
| Decoder Unicode thật | Cùng encoding_edges.py | UTF-8 `review Đ ✓`; cp1252 chữ sai, guard bắt | KHÔNG PHẢI LỖI hiện hữu |
| Scope scanner syntax/dataflow | Cùng encoding_edges.py | sys.executable, argv biến, text=1, universal_newlines đều có thể lọt | GIỚI HẠN đã công bố, chưa có call sai như vậy trên HEAD |
| Direct/suite/journal, empty/Unicode/dấu câu | `python3 evidence/routes.py` | TypeError/AssertionError/TinHieuChotCa đúng loại + 160; foreign vẫn loi; own vẫn giet | KHÔNG PHẢI LỖI cũ còn mở |
| Transport OSError/timeout/JSON | Cùng routes.py | OSError, TimeoutExpired, ValueError, JSONDecodeError giữ đúng detail helper | KHÔNG PHẢI LỖI cũ còn mở |
| Các dòng SAI product/neutral/hook/harness | Cùng routes.py | mỗi đường SAI giữ TypeError + 160 x, không 161; harness qua child thật | KHÔNG PHẢI LỖI cũ còn mở |
| Compiler + setsid + console ASCII | `python3 evidence/guards.py`; `python3 evidence/mutation_probes.py` | khóa thật xanh; bỏ type/message/cắt/UTF-8 đều chết đúng khóa | KHÔNG PHẢI LỖI cũ còn mở |
| Kênh lượt qua / trước/lồng | Cùng guards.py | hong=0, qua=1, cả ba field null; mutant mỗi field chết đúng guard | KHÔNG PHẢI phản chứng lượt 4 còn mở |
| Lượt có lỗi thật rồi lồng ca ở lần qua | `python3 evidence/extended.py` | nested-error: channel RuntimeError/review-inner; nested-signal: channel TinHieuChotCa/review-inner; stdout lỗi ngoài TypeError/review-current | LỖI F01 |
| Nhật ký lỗi I/O và quyền dừng | Cùng extended.py | 5 vị trí rc=1/đúng 160/không traceback; SystemExit=7, KeyboardInterrupt=-2 | KHÔNG PHẢI LỖI boundary mới |
| Reporter ngoài except và hooks interpreter | `python3 evidence/inventory.py`; `python3 evidence/claims.py`; rg traceback/format_exc/excepthook/repr/Thread | 34 handler/32 print, hai repr logic, không custom hook/format_exc; kênh ngoài except ở finding | Không thấy đường reporter độc lập khác còn sót trong phạm vi đo; Windows readerthread KHÔNG ĐO ĐƯỢC native |
| Phản chứng của bản gợi ý | `python3 evidence/build_hint.py`; `python3 evidence/hint_controls.py` | HEAD+guard giet đúng lý do; hint 12/12; 27/27 own; runner child 6/6; 54 mục harness, mỗi neo đều duy nhất; patch áp khớp byte | KHÔNG PHẢI LỖI trong phạm vi đo hint |

## KIỂM KÊ ĐƯỜNG CHI TIẾT

| Nguồn → consumer trên HEAD | Đo |
|---|---|
| mo_ta_loi:193 → cham_mot_ca:209/213 → ket_luan_mutant → dòng neutral/SAI | routes; guards; 25 mutant riêng: đúng 160, foreign vẫn loi |
| chay_bo_ca:15259/15266 → hong_ds → main suite/lap | routes + guard CLI: type/message đúng, phân loại không dựa parse message |
| Cùng hai handler → ket → NhatKyCa.ra/ghi/flush/fsync | nhật ký thật của TypeError/AssertionError/chốt đều đúng |
| Cùng hai handler → CHI_TIET_HONG/LOAI_HONG → producer channel:15433–15436 → cham_lap_ca | hong=0 đã null; hong>0 bị ca lồng ở lần qua ghi đè map: F01 |
| cham_lap_ca:15218 → harness neutral/SAI | lỗi transport đã có mo_ta_loi; channel lỗi thường type một lần |
| chay_dot_bien:15064 → print nhánh hook | TypeError + 160, không mất message |
| chay_dot_bien:15006 → print lỗi compile | compiler thật duplicate argument dài: SyntaxError + 160 |
| _tu_tach_nhom_neu_can:2320 → main print | PermissionError + 160 |
| _cung_hoa_dau_ra_harness → stdout/stderr main và mutation | child PYTHONIOENCODING=ascii vẫn có tổng kết và đúng 160 ✓; StringIO phục vụ các probe không lỗi |
| Nhật ký __init__/vao/ghi/fsync/dong → boundary CLI:15457 | 5 vị trí đều cắt/không traceback; control flow BaseException được giữ |
| Import/thread interpreter ngoài main | Không có formatter riêng đang tồn tại; không nhận đã đo Windows/native hay mọi sink tùy biến |

## BANG LOP

| Slug / lịch sử | Đã đóng | Còn mở | Phép đóng lớp |
|---|---|---|---|
| reporter-thong-diep / F01 lượt 1–4 | Suite/channel lặp loại; transport; journal lỗi ca; foreign; compiler; setsid; Unicode; channel hong=0; CLI I/O | Một biểu hiện P1: hong>0 nhưng map bị ca lồng ở lần qua sau ghi đè | Metadata gắn với từng lỗi/lượt, kiểm qua/bỏ qua/lồng sau một lỗi thật và giữ phân loại lẫn message |
| khoa-encoding-chi-kiem-khoa / F02 lượt 1 | Mọi giá trị sai trong shape scanner công bố bị khóa bắt | Không có biểu hiện mở trong phạm vi ấy | Giữ literal utf-8/replace và mutant giá trị; không đổi giới hạn scanner thành lời hứa dataflow |

## FINDINGS

### reporter-thong-diep [P1] F01: kênh của lượt có lỗi vẫn đọc metadata bị ca lồng ghi đè

TEP/DONG: `.claude/dev/launcher_test.py:15418`, `:15433`, `:15435`, `:15436`; producer map `:15260`/`:15267`. Thay đổi mới `if hong_ds` chặn được dữ liệu cũ khi không có lỗi nhưng không gắn type/message với lỗi đang báo.

VAN DE: chạy `--lap-ca review_repeat --lan 2`. Lần 1 ngoài ném TypeError("review-current"). Lần 2 ngoài qua, nhưng gọi lồng chính ca; chay_bo_ca bên trong đã bắt RuntimeError("review-inner") và ghi vào map cùng tên. Lượt ngoài vẫn có một lỗi thật TypeError, stdout in đúng nó, nhưng JSON channel mang RuntimeError/review-inner. Cho lỗi lồng là TinHieuChotCa thì channel còn đổi `loai` sang TinHieuChotCa dù lỗi ngoài là TypeError. Đây là sai dữ liệu chẩn đoán của producer mới; không khẳng định đã tạo tín dụng giết giả trong cham_lap_ca hiện chỉ dùng --lan 1. Không đưa việc bỏ kênh của #1117 vào packet này.

DA THU NGHIEM: `python3 evidence/extended.py`, rc=0, giữ cả stdout/stderr/JSON. `pass` control: qua=1,hong=1, khac:TypeError/TypeError/review-current. `skip` control: bo_qua=1,hong=1, cùng chi tiết đúng. `nested-error`: qua=1,hong=1 nhưng khac:RuntimeError/RuntimeError/review-inner. `nested-signal`: qua=1,hong=1 nhưng TinHieuChotCa/TinHieuChotCa/review-inner. Không sửa map bằng tay; dữ liệu được ghi bởi chay_bo_ca thật và đọc từ child CLI thật.

VÁ Ở ĐÂU: ranh giới kết quả mỗi lần lặp trong main, nơi có h/q/b của chính lượt ngoài. Consumer cham_lap_ca chỉ thấy JSON sai nguồn nên cắt/đổi cách ghép bên consumer không chữa được nguyên nhân. Chỉ xóa map lúc ca qua cũng làm mất lỗi thật của lần trước trong cùng --lan.

VÁ THẾ NÀO: đường rẻ nhất là chụp loại và chi tiết ngay khi một lần lặp ngoài trả h khác rỗng; giữ snapshot cục bộ đó qua những lần ngoài qua/bỏ qua, rồi xuất snapshot. Không có lỗi ngoài thì khởi tạo ba trường null. Giữ chính sách hiện tại là lỗi ngoài cuối cùng khi có nhiều lần hỏng. Đường dài hơn: trả metadata có cấu trúc cùng từng kết quả, bỏ sự phụ thuộc vào map dùng chung; mua thêm cô lập cho caller lồng và nhiều consumer, cần cập nhật giao diện rộng hơn.

CA KHÓA VÀ ĐỘT BIẾN: HINT thêm `r1122_kenh_loi_phai_thuoc_luot_ngoai`, bốn tổ hợp: ngoài TypeError/lồng RuntimeError, ngoài TypeError/lồng chốt, ngoài chốt/lồng RuntimeError, ngoài TypeError rồi bỏ qua có lồng. Đòi cùng lỗi ngoài, đúng counter và message cắt 160. `build_hint.py`: HEAD + guard đỏ bằng TinHieuChotCa của CHÍNH guard với “kenh lay chi tiet ca long thay loi ngoai”; hint 12/12 guard qua, 27/27 mutant liên quan đúng own_signal. Hai mutant mới (chụp cả lần qua/bỏ qua; đọc lại live map) đều chết đúng guard mới. Bốn neo cũ của channel được cập nhật, không để lỗi neo thay tín dụng giết. `hint_controls.py`: 54 mục harness, mọi neo trong từng mục đều duy nhất, 6/6 entry qua runner/child thật; sáu ca cũ qua. Patch --batch -p0 trên cây riêng rc=0 và byte equality=true; Ruff hint giữ 5 F841.

NGUY CƠ BẢN VÁ: snapshot vô điều kiện hoặc clear lúc qua sẽ làm mất/đổi lỗi thật; khóa mới đo cả qua và bỏ qua sau lỗi. Cần giữ đúng ghép loại/message và phân loại chốt, không dùng chuỗi lỗi đã format để dựng message. Snapshot cục bộ không tự thay thế hoàn toàn vòng đời map ở API chay_bo_ca; không hứa xử lý callback nhật ký tùy biến hay caller đa luồng. Không nuốt SystemExit/KeyboardInterrupt. Không chạy full suite/full catalog trên hint và không đo native Windows; hint không thay required gate của executor.

HINT.patch: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Patch -p0 từ cay-kho/, chỉ là hiện vật gợi ý từ cây tạm; không sửa branch executor.

ĐỘ TIN: cao về lỗi dữ liệu, có control âm/dương, lỗi đúng lớp, own signal của guard mới và CLI/channel thật. Một lớp F01, một biểu hiện mở được tính; không có P0/P2/P3 độc lập khác trong phạm vi đã đo.

## TOÀN VẸN VÀ GIỚI HẠN

source-initial.json/source-final.json băm 10459 tệp ngoài .git, kể cả ignored/untracked. integrity.json: same_files=true, same_identity=true, clean=true. HEAD/tree trước–sau đúng các OID trên; không có delta quan sát được ở hai mốc. Đây không chứng minh chưa từng có ghi rồi hoàn nguyên. Sandbox thực tế workspace-write; chỉ đọc checkout bằng cách chọn nơi chạy, không tự nhận mount read-only. Các clone/tmp của riêng lượt này đã dọn; giữ script/log/JSON/patch và artifact-manifest.json.

N0/A3/check-run ci.yml exact HEAD và Ruff pin CI chưa đo độc lập; A6 chưa đến thời điểm. Những mục này không được gọi pass hay thay bằng lời khai cũ. Hướng kiểm nội dung nhạy cảm chỉ mô tả bằng lời: exception từ API/subprocess có thể chứa dữ liệu người dùng trong 160 ký tự đầu; cắt không phải redaction. Không soạn payload nhạy cảm và không dùng credential thật.

Đã sửa hai lỗi của rig riêng trước khi chốt: fixture harness ban đầu không đăng ký ca ở neutral (đã chạy lại qua child thật có ca neutral), và một tên ca tương thích t99 gõ sai (đã sửa, đòi tồn tại và chạy đủ 6/6). Output cuối giữ riêng ở routes/hint-controls; không dùng lỗi setup hay ca chưa chạy làm pass/kill. Không có hai sai sót này trong full A/B hoặc checkout được review.
