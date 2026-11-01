verdict: changes_requested
reviewed_sha: cccc5eb31425f78c23a7dadf826034715831fcf5
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 0 P1, 1 P2, 0 P3.

Packet #1122 r1/g1, lease `wp1122-r1-g1-claude`, sensitive, PR #1130, lượt gọi Codex 8/10. **changes_requested vì F01 còn thiếu khóa hồi quy cho nhánh AssertionError**: đưa lỗi thứ tự formatter trở lại nhánh này mà 12/12 khóa r1122 vẫn qua. Chưa có phản chứng mới chứng minh HEAD cấp tín dụng giả trong giới hạn phép thử của lượt này; không nâng khoảng trống kiểm thử thành P1.

Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`; HEAD tree `c68fec48b962eb9bfb3e5f404c643eb3ca84e4a6`. SPEC được băm lại; diff thực khớp diff.patch và diff từ 5d21d55 khớp diff-tu-luot6.patch. Chỉ review `.claude/`, một tệp +450/-93; phần ops/reviews ngoài đối tượng. Trần 450 vẫn giữ được với HINT bên dưới. Ngưỡng chủ kho là hết P1/P2/P3; không tự miễn P2.

Reviewer: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; không đo độc lập biến thể model/effort từng request. Công cụ thực thi shell Linux sandbox qua API; `codex_service` theo định nghĩa provider của kho, transport machine. Không tự nhận ChatGPT Web, model từ Git actor, hoặc đã đo Windows. Executor Claude theo packet; không kế thừa context executor. Verdict không cấp quyền merge/land.

Python 3.13.18, Ruff 0.16.9. Sandbox thực tế workspace-write; giữ cay-kho chỉ đọc bằng nơi chạy, không tự nhận mount read-only. Snapshot đầu băm 10459 tệp kể cả ignored/untracked và status sạch. Mọi suite/probe/mutant chạy trên bản sao ngoài cay-kho. Hai vế A/B cùng clone cục bộ, core.abbrev=7, TMPDIR riêng; `/tmp/.git` tồn tại, không chỉnh/xóa nó để làm xanh. Đặt PYTHONDONTWRITEBYTECODE=1, PIP_NO_INDEX=1, PIP_DISABLE_PIP_VERSION_CHECK=1; bỏ CODEX_AUTH_JSON kế thừa. Không mạng, credential thật hoặc push.

Theo giới hạn lượt 8: chỉ chạy lớp ngoại lệ đặc biệt ĐÃ CÓ trong test của HEAD; không soạn lớp mới. Các script routes/extended/encoding/AST được chép từ lượt 6, đọc rồi CHẠY LẠI trên HEAD này; không tái dùng output cũ. HINT mới dùng TypeError/TinHieuChotCa bình thường và callback ở seam mo_ta_loi, không định nghĩa lớp ngoại lệ đặc biệt. Hướng cần lớp như vậy được mô tả bằng lời ở cuối.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / nguồn | Trạng thái trên HEAD | Bằng chứng tự đo |
|---|---|---|
| F01 lượt 1: suite/CLI không cắt, transport mất message | ĐÃ VÁ THẬT các biểu hiện đó | routes.py: direct TypeError/AssertionError/chốt, suite và nhật ký giữ loại + 160; OSError/TimeoutExpired/ValueError/JSONDecodeError qua formatter. guards.py + mutation_probes.py: khóa qua, bỏ message/cắt bị chính ca giết. |
| F01 lượt 1: channel lặp loại/cắt cả prefix | PHẠM VI ĐÃ ĐỔI theo chủ kho, không gọi là vá message | CHI_TIET_HONG không còn identifier; producer có sáu trường nonce/ten/qua/bo_qua/hong/loai. Lỗi harness thường chỉ còn review_child(khac:TypeError), đúng quyết định bỏ message sau lượt 5. |
| F01 lượt 2: ket nhật ký, foreign chốt, compiler | ĐÃ VÁ THẬT các biểu hiện đó | Journal LOI/HONG đúng loại + 160; foreign vẫn loi; compiler duplicate argument thật ra SyntaxError + 160. Mutant từng đường đều own_signal=true. |
| F01 lượt 3: Unicode console, setsid | ĐÃ VÁ THẬT trong luồng chuẩn đã đo | Child với PYTHONIOENCODING=ascii vẫn có footer và đúng 160 ✓; setsid PermissionError + 160. Bỏ UTF-8/đổi ASCII/bỏ message bị chính khóa bắt. |
| F01 lượt 4: message cũ khi lượt qua; I/O nhật ký | ĐÃ VÁ THẬT các biểu hiện đó | guards.py: hai fixture prelude/lồng với hong=0 có loai=null, không field message; extended.py: open/write/fsync/final/close đều cắt, không traceback cho Exception. |
| F01 lượt 5: ca lồng ở lượt qua/bỏ qua sau lỗi ngoài | ĐÃ VÁ THẬT các fixture đó | extended.py pass/skip/nested-error/nested-signal đều giữ khac:TypeError và hong=1. Mutant đọc lại map/chụp cả lượt qua bị chính khóa bắt. |
| F01 lượt 6: formatter lồng sau ghi map | ĐÃ VÁ THẬT sáu fixture hiện có; VÁ HỜ ở phần khóa của cả lớp | guards.py qua sáu tổ hợp hiện có; late-exception/early-map-exception bị chính khóa giết. Nhưng late-assertion/early-map-assertion đều qua 12/12 khóa: P2 dưới đây. Các tổ hợp lớp ngoại lệ đặc biệt khác của script lượt 6 không được dựng lại do ràng buộc lượt 8; không khai đã đo lại chúng. |
| F02 lượt 1: cp1252/None vẫn được khóa chấp nhận | ĐÃ VÁ THẬT trong hình dạng scanner đã công bố | encoding_edges.py: 10 giá trị sai đều giet/own_signal=true; chay thật giải mã review Đ ✓ đúng. Bốn giới hạn cú pháp cũ vẫn được khai riêng. |

Không thấy bản vá producer sinh hồi quy trong các đường được chạy. F01 chưa được tuyên bố đóng lớp bằng tổng suite hoặc việc đã áp HINT; còn P2 về khóa và các hướng chưa đo được nêu rõ.

## BANG NGHIEM THU

Lệnh evidence chạy từ thư mục review này. Sau khi dọn cây tạm, run_ab.py tự dựng A/B sạch; setup_copies.py dựng lại hai cây cho các probe. common.py tự đặt env offline/không bytecode. Trong từng clone, hai lệnh thật là `python3 .claude/dev/launcher_test.py` và cùng lệnh thêm `--dot-bien`.

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| N0 Windows tái hiện trước vá | NOT_RUN; không có log job gốc để đọc offline | Chỉ có lời khai lịch sử run 41328709141 về TypeError/NoneType; không tự xác nhận thứ tự tái hiện → ghi message → vá | KHÔNG ĐO ĐƯỢC |
| N0' Linux base cùng rig | `ls -d /tmp/.git`; `python3 evidence/run_ab.py` | Base 319/342 đã chạy, tổng 352, bỏ qua 10, hỏng 23; mutation: DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | ĐÃ ĐO NỀN, giữ rc=1 |
| A1 assert/raise + khóa AST | `python3 evidence/inventory.py`; `python3 evidence/ast_edges.py`; `python3 evidence/mutation_probes.py` | 57 assert/11 ca và 8 raise/2 ca chuyển, mismatches=[]; assert/nested/raise Name/tên allowlist thừa hoặc mục dần đều chết đúng khóa | ĐẠT phạm vi SPEC + mở rộng |
| A2 thông điệp 160 | `python3 evidence/guards.py`; `python3 evidence/routes.py`; `python3 evidence/mutation_probes.py` | TypeError(x*500) → loi + đúng 160 x; Unicode/empty đúng; bỏ message/đổi trần bị chính ca giết | ĐẠT A2; khóa lớp F01 còn P2 |
| A3 Windows exact HEAD | NOT_RUN, prompt cấm mạng | Run 41333516059 được cung cấp là trên fd1f82e, không phải cccc5eb; không dùng thay log exact HEAD | KHÔNG ĐO ĐƯỢC |
| A4 Linux HEAD/base | `python3 evidence/run_ab.py`; `python3 evidence/summarize.py` | HEAD 331/354 đã chạy, tổng 364, bỏ qua 10, hỏng 23; mutation: DOT BIEN: 541/573 dat  (4 khong do duoc tren nen nay). Tập hỏng/bỏ qua đối chiếu trong ab-summary.json | ĐẠT điều khoản delta=0: tập hỏng/bỏ qua trùng; không gọi N/N xanh |
| A5 bare Ruff F | `python3 evidence/audit.py` | Base và HEAD đều rc=1: 5 F841 launcher_test.py + 12 F821 tl.py, chẩn đoán delta=0 | ĐẠT delta với Ruff 0.16.9; chưa đo pin CI 0.15.15 |
| A5 doctrine | Cùng audit.py: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` từ cay-kho | Sạch, quét 10 tệp, 0 chỗ chép doctrine, rc=0 | ĐẠT |
| A5 whitespace | `git -C cay-kho diff --check BASE HEAD` (OID ở đầu tệp); audit.py đo riêng .claude | Cả toàn diff và .claude output rỗng, rc=0 | ĐẠT |
| A5 ci.yml exact HEAD | NOT_RUN: không có check-run receipt cuối, không mạng | Workflow khai pin Ruff đúng là kiểm tĩnh, không chứng minh job đã xanh | KHÔNG ĐO ĐƯỢC |
| A6 sau land | NOT_RUN, ngoài thời điểm/quyền reviewer | Chưa land | CHƯA ĐO ĐƯỢC theo SPEC |

## BANG DO

claims.py lấy toàn bộ dòng thực thi thay đổi, comment qua tokenize, docstring qua AST từ 5d21d55..HEAD và toàn bộ commit message, lưu claims.json/commit-messages.txt. Đây là kiểm kê văn bản, không phải bộ nhận diện đầy đủ khẳng định ngữ nghĩa và không đặt trần review; vẫn đọc caller/consumer, dòng xóa và đường ngoài except. Mọi khẳng định bỏ sót vẫn thuộc phạm vi tìm finding.

| Khẳng định | Diff/commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Chạy formatter một lần trước map | Comment :15300 và commit cccc5eb | inventory.py đọc hai handler: mỗi handler một mo_ta_loi trước phép gán; guards.py 12/12, routes.py giữ output | Đúng code HEAD; khóa riêng nhánh assertion chưa đủ, F01/P2 |
| Giữ tin cho hong_ds và ket ở cả hai nhánh | Diff producer | routes.py: TypeError/AssertionError/chốt có cùng nội dung journal và hong_ds, loại một lần + 160 x | Có trong phép đo |
| Áp nguyên văn TEST HINT lượt 6 | Commit hint_provenance | claims.py áp HINT lượt 6 lên 5d21d55 trong cây tạm: exact_hint_test=true | Có, byte-equal toàn hàm test |
| Fixture đo lồng ở lượt sau và trong str | Docstring mới + sáu tuple | guards.py qua; đọc sáu tuple: bốn lượt-sau và hai TypeError/str. order_mutations.py: chỉ nhánh Exception có răng trước reentrancy | Có cho sáu fixture; không chứng minh mọi nhánh, P2 |
| Mutant mới khôi phục định dạng sau map | Entry wp1122_dinh_dang_lai_sau_ghi_map | mutation_probes.py: neo duy nhất, own_signal=true; lỗi `4 khac:RuntimeError` | Có; chỉ khôi phục nhánh LOI |
| Neo cũ đổi theo biến tin vẫn đúng tác dụng | Bốn entry journal/reporter trong diff từ lượt 6 | claims.py: 52 entry neo duy nhất/compile/đủ target; mutation_probes.py: 25 wp1122 đúng own_signal | Có |
| Channel không mang message, giữ loại lỗi ngoài | Hai comment mới tại producer | scope_inventory.py: một read live ở main:15465; guards/extended kiểm sáu trường, hong=0 và lỗi rồi qua/bỏ qua | Đúng các fixture đã đo; chưa là ownership độc lập global |
| Trần diff 450 | numstat.txt | git diff --numstat BASE HEAD -- .claude → 450/93, diff_equal=true | Có |
| Toàn bộ call Python text=True được ghim | Phạm vi mở rộng encoding | inventory.py: 21 call direct PY/py text=True đều utf-8/replace; 14 call cũ thêm encoding; 22 call hệ thống không đổi. scope_inventory.py: 12 direct Python khác dùng byte/không text | Có trong hình dạng được nhận diện; không khai dataflow toàn diện |
| 30 handler dựng chuỗi = 18 ca + 12 hạ tầng ở 93a9afe | Lời khai lịch sử được prompt yêu cầu kiểm lại | inventory/scope_inventory: 93a9afe có 33 named handler/21 trong ca; predicate công khai str/repr/type/mo_ta_loi/f-string là 28/17. HEAD có 34/21 và 29/17 | Không tái lập 30/18 dưới predicate này; không có script/predicate gốc để quy thành sai số cùng định nghĩa. Không dùng số đó chứng minh đóng lớp |

## BANG TEST

| Bộ | N/M / kết quả | Bỏ qua/không đo | rc |
|---|---|---|---|
| Base suite | 319/342 đã chạy, tổng 352, hỏng 23 | 10 | 1 |
| HEAD suite | 331/354 đã chạy, tổng 364, hỏng 23 | 10 | 1 |
| Base --dot-bien | DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | 4 không đo được; 32 neutral đỏ tính hỏng | 1 |
| HEAD --dot-bien | DOT BIEN: 541/573 dat  (4 khong do duoc tren nen nay) | 4 không đo được; 32 neutral đỏ tính hỏng | 1 |
| Khóa r1122 trên HEAD | 12/12 qua | 0 | 0 |
| Mutant wp1122 hiện có, chạy riêng | 25/25 chết đúng chính ca | 0 | 0 |
| AST bổ sung | 4/4 chết đúng chính ca | 0 | 0 |
| Giá trị encoding/errors sai | 10/10 chết đúng chính khóa | 0 | 0 |
| HINT: khóa r1122 | 12/12 qua | 0 | 0 |
| HINT: mutant wp1122 | 27/27 chết đúng chính ca | 0 | 0 |
| HINT: hai entry mới qua runner/child thật | 2/2 OK, mỗi entry giet 1/1 | 0 | 0 |
| HINT: ca tương thích cũ | 7/7 qua; bare Ruff delta=0 | 0 | 0 (lint vẫn rc=1 với 5 F841 nền) |

## BANG SAN

Các dòng độc lập dưới đây có lệnh và output thật trong evidence, không dùng giả thuyết thay phép đo.

| Hướng | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| Tương đương assert/raise | `python3 evidence/inventory.py` | asserts=57, raises=8, mismatch=[] | KHÔNG PHẢI LỖI |
| Khóa AST/nested/allowlist mục dần | `python3 evidence/ast_edges.py` | Bốn biến thể giet/own_signal=true | KHÔNG PHẢI LỖI |
| Giá trị encoding/errors | `python3 evidence/encoding_edges.py` | 10 giá trị sai giet/own_signal=true; UTF-8 review Đ ✓; cp1252 sai byte | KHÔNG PHẢI F02 mở |
| Hình dạng scanner khác | Cùng encoding_edges.py | sys.executable, argv biến, text=1, universal_newlines đều qua khóa | KHÔNG PHẢI lỗi mới: giới hạn syntax đã công bố, chưa có call sai trên HEAD |
| Direct/suite/journal/foreign | `python3 evidence/routes.py` | direct foreign=loi; TypeError/AssertionError/chốt giữ 160; empty chỉ loại | KHÔNG PHẢI lỗi cũ còn mở |
| Transport/JSON/timeout | Cùng routes.py | Bốn loại exception đều detail đúng helper, vẫn loi | KHÔNG PHẢI LỖI |
| Product/hook/harness SAI | Cùng routes.py | Mỗi probe (1,0); product/neutral/hook TypeError + 160; harness khac:TypeError theo phạm vi đã duyệt | KHÔNG PHẢI LỖI reporter |
| Compiler thật | `python3 evidence/guards.py`; mutation_probes.py | SyntaxError duplicate argument dài được cắt; mutant bị chính khóa giết | KHÔNG PHẢI LỖI |
| Unicode console/setsid | Cùng guards.py và mutation_probes.py | Footer + đúng 160 ✓ dưới ASCII; PermissionError + 160 | KHÔNG PHẢI LỖI |
| Vòng đời channel, lỗi rồi qua/bỏ qua | `python3 evidence/extended.py`; guards.py | Bốn follow-up giữ hong=1, loai=khac:TypeError; fixture không hỏng loai=null | KHÔNG PHẢI phản chứng cũ còn mở |
| I/O nhật ký/quyền dừng | `python3 evidence/extended.py` | 5 điểm I/O rc=1, message cắt, không traceback; SystemExit=7, KeyboardInterrupt=-2 | KHÔNG PHẢI LỖI |
| Thứ tự formatter/map ở hai nhánh | `python3 evidence/order_mutations.py` | late-/early-map-assertion: 12/12 qua; Exception tương ứng: 11/12, đúng khóa chết | LỖI F01/P2 về khóa |
| Kiểm kê sink ngoài except | `python3 evidence/scope_inventory.py`; inventory.py | CUSTOM_EXCEP_HOOKS=[]; 34 handler/32 print; 0 CHI_TIET_HONG; một read live LOAI_HONG ở main | Không thấy sink formatter riêng bỏ sót; callback cleanup chưa đo, mô tả dưới |
| Provenance/neo | `python3 evidence/claims.py` | exact_hint_test=true; 52 entry duy nhất, compile, target có mặt | KHÔNG PHẢI LỖI |
| HINT thực sự bắt nhánh assertion | `python3 evidence/build_hint.py`; hint_controls.py | 27/27 own_signal, hai entry runner thật OK 1/1; cumulative +450/-93 | KHÔNG PHẢI lỗi setup hoặc tín dụng giả của giàn đo |

## KIỂM KÊ TOÀN BỘ ĐƯỜNG CHI TIẾT

| Nguồn → sink | Phép đo / kết quả |
|---|---|
| mo_ta_loi:193 nhận exception; cham_mot_ca:209/213 → ket_luan_mutant → product neutral/SAI:15073/15076 | routes/guards/mutants: loại + 160, empty/Unicode đúng; own=giết chỉ tên theo thiết kế, foreign=loi. Không parse detail để khớp phai_chet |
| chay_bo_ca:15299/15306 → hong_ds → hai print HONG main:15472/15491 | routes: đúng loại/160 cho ba loại lỗi; lấy cùng tin cho nhật ký |
| Hai handler đó → ket → NhatKyCa.ra:15218 → ghi/flush/fsync | Journal thật qua cả LOI/HONG. Hai lần gọi formatter sau map cũ đã được bỏ; khóa hồi quy cho assertion còn thiếu (P2) |
| Hai handler → LOAI_HONG:15303/15309 → main live read:15465 → channel:15473 → cham_lap_ca:15266 | Đúng sáu fixture hiện có và lỗi-rồi-qua/bỏ qua. Vẫn một read từ map toàn cục; không gọi đó là metadata sở hữu bởi kết quả |
| cham_lap_ca:15260 → detail transport/JSON → harness neutral/SAI:15171/15174 | routes: bốn loại lỗi có loại + 160. Detail từ channel chỉ còn loại theo quyết định chủ kho |
| Hook except:15106 → loi → print:15119 | routes: TypeError + 160; không lặp loại. Nhánh giết không hiển thị exception theo thiết kế |
| Compiler except:15048 → SAI:15049 | Compiler thật + khóa/mutant: SyntaxError và đúng 160 message |
| setsid:2320 → main:15422 | PermissionError + 160 qua khóa hiện có |
| NhatKyCa open/vao/ghi/fsync/dong → root boundary:15499/15500 | extended: 5 điểm đều cắt; BaseException yêu cầu dừng vẫn thoát |
| stdout/stderr reconfigure:15398 → main/chay_dot_bien prints | Child ASCII của khóa qua; không nhận đã đo mọi stream tùy biến hoặc Windows native |
| _wp1077_llm, _CsNhan.goi, _CsSeam.f_kill, _review6_registry_raw_phai_tu_choi | Bốn helper fixture, không phải reporter độc lập. Trả logic hoặc ném chốt để qua formatter cuối. _CsSeam không dựng chuỗi |
| repr(e), sys/threading hooks và traceback formatter | Hai repr(e) thuộc logic @ca; không có custom excepthook/format_exc/format_exception. Thread trực tiếp target=lambda:None chỉ dựng fixture, không start. _readerthread Windows native không đo được |

inventory.json lưu source của mọi 34 named handler và 32 print, không đếm chuỗi catalog như code. 21 handler trong @ca; 13 hạ tầng = 9 reporter + 4 helper fixture. Các print còn lại là trạng thái/đếm/tên ca/skip/bản khai môi trường, không chứa detail exception độc lập; không ép tên hay lý do skip về 160. CHI_TIET_HONG không còn đường đọc/ghi; map loại vẫn có thể giữ mục cũ nhưng producer không phát nó khi hong=0 trong các fixture đã đo.

## BANG LOP

| Slug / IDs | Đã đóng hoặc đổi phạm vi | Còn mở | Phép đóng lớp |
|---|---|---|---|
| reporter-thong-diep / F01 lượt 1–6 | Các đường message, Unicode, I/O và fixture map/str hiện có đều được chạy lại đạt. Message channel được bỏ theo authority | 1 biểu hiện P2: khóa không bắt nhánh AssertionError tái định dạng sau map hoặc ghi map sớm. Hướng callback cleanup/provenance khác chưa đo | Gia cố nhánh assertion, mỗi mutant chết đúng ca; giữ meta thuộc invocation nếu cần xử lý callback khác. Không dùng tổng suite thay phép đo ownership |
| khoa-encoding-chi-kiem-khoa / F02 lượt 1 | Giá trị sai trong hình dạng literal PY/py + text=True bị khóa bắt | Không có biểu hiện mở trong shape đã công bố; giới hạn dataflow và Windows vẫn khai riêng | Giữ UTF-8/replace và mutant sai giá trị; khi mở shape cần thêm phép đo tương ứng |

## FINDINGS

### reporter-thong-diep [P2] F01: khóa hồi quy formatter/map bỏ sót nhánh AssertionError

TEP/DONG: `.claude/dev/launcher_test.py:9998`–`:10019` (tuple/fixture callback chỉ dùng TypeError), `:14830` (mutant mới chỉ thay LOI), nhánh tương ứng cần bảo vệ `:15299`–`:15305`.

VAN DE: sửa producer áp dụng invariant formatter trước map cho hai handler, nhưng phép thử reentrancy mới chỉ tác động handler Exception. Đổi riêng `ket = f"HONG: {tin}"` thành gọi lại mo_ta_loi, hoặc dời phép gán LOAI_HONG của AssertionError lên trước lần format, vẫn được toàn bộ 12 khóa r1122 chấp nhận. Đó chính là hai cách quay lại lỗi thứ tự được sửa ở lượt 6, ở nhánh còn lại. Các khóa journal hiện chỉ so văn bản, nên format lại cùng text vẫn qua. P2 là thiếu răng kiểm thử đã đo được; không tuyên bố HEAD đang có P1 tín dụng giả.

DA THU NGHIEM: `python3 evidence/order_mutations.py`, rc=0: late-assertion 12/12 qua; early-map-assertion 12/12 qua; hai control Exception tương ứng đều 11/12 qua và r1122_kenh_loi_phai_thuoc_luot_ngoai chết own_signal=true, lỗi `4 khac:RuntimeError`. Không đổi fixture hoặc viết lớp ngoại lệ mới cho phép đo này. Cặp neo/thay late assertion nguyên văn nằm trong order_mutations.py và HINT.patch; early-map lấy nguyên block AST, chỉ dời phép gán. Neo vùng executable được đòi duy nhất, loại catalog khỏi vùng thay như runner thật.

VÁ Ở ĐÂU: ca r1122_nhat_ky_giu_loai_va_thong_diep_160 hoặc ca ownership hiện có, cùng DOT_BIEN_HARNESS. Producer HEAD giữ được thứ tự đúng trong các phép đo này; không có lý do sửa producer chỉ để đóng P2.

VÁ THẾ NÀO: đo tái nhập formatter cho cả hai nhánh và đòi loại cuối vẫn thuộc lỗi ngoài, đồng thời giữ nguyên chốt text/160/journal cũ. HINT mô phỏng ở seam mo_ta_loi: khi đang format thì chạy lồng CHÍNH fixture với loại ngược lại; dùng hai ngoại lệ chuẩn đã có, không subclass đặc biệt. Thêm hai mutant assertion (format lại sau map; ghi map trước formatter). Đây là bằng chứng khóa invariant, không phải lời khai đã tái hiện một lớp __str__ mới trên HEAD.

CA KHÓA VÀ ĐỘT BIẾN: `python3 evidence/build_hint.py`, rc=0: HINT 12/12 khóa qua, 27/27 mutant wp1122 chết bằng TinHieuChotCa của chính ca. Cả hai mutant mới báo `formatter long doi loai loi ngoai: TinHieuChotCa`, own_signal=true. `python3 evidence/hint_controls.py`, rc=0: hai entry qua chay_dot_bien thật/child thật đều OK giet 1/1; bảy ca tương thích qua; bare Ruff giữ 5 F841. 54 entry harness đều neo duy nhất/compile/target có mặt. Đã patch -p0 trên cây tạm và byte-compare với nguồn đã đo.

NGUY CƠ BẢN VÁ: callback seam phải có cờ chống đệ quy, luôn hoàn nguyên formatter và vẫn giữ chốt nhật ký/loại/160. Không biến TinHieuChotCa của helper khác hoặc lỗi setup thành kill. HINT đo LOAI_HONG vì đó là authority hiện tại; nếu executor chuyển sang metadata thuộc kết quả thì nên đo kết quả/channel tương ứng và cập nhật mutant/neo, không giữ một ràng buộc global lỗi thời. Không nuốt SystemExit/KeyboardInterrupt, xóa lỗi của lần trước, hoặc mở việc thay runner #1117.

HINT.patch: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Chỉ gia cố TEST/catalog, không viết producer authority. Cumulative so BASE +450/-93: bỏ 20 dòng trắng trong khối test MỚI của packet để bù phần gia cố khóa; không bỏ test/chốt/comment/docstring. Không cần nâng_trần. Không chạy full suite/full catalog trên HINT hoặc Windows.

ĐỘ TIN: cao cho lỗ khóa và đối chứng sửa khóa. Không dùng lỗi runtime/setup làm tín dụng giết. Một lớp F01, một biểu hiện P2; không có P0/P1/P3 mới được xác lập trong các phép đo được phép.

## HƯỚNG CHỈ ĐỌC MÃ, CHƯA DỰNG PHẢN CHỨNG

Vẫn còn read live `LOAI_HONG.get` ở main:15465, sau khi chay_bo_ca ghi map (:15303/:15309), kết thúc handler, có thể gọi nk.ra (:15312), rồi return (:15313). Cache str chỉ khóa vị trí formatter đã biết, chưa tạo ownership cho kết quả. Một hướng executor cần tự dựng là callback khi exception được giải phóng ở cuối handler (ví dụ cơ chế hủy đối tượng) chạy lồng cùng ca trước lúc main đọc map. Hướng khác là formatter làm thay đổi traceback/provenance trước chot_tu_ca_khac trong nhánh assertion (:15303), trong khi cham_mot_ca kiểm provenance trước format (:209–:212). Cần chứng minh reachability, thời điểm callback thật và control trực tiếp/channel, không suy từ code order rằng P1 đã xảy ra. Reviewer không viết lớp ngoại lệ có hành vi đó theo chỉ thị lượt 8; đánh dấu KHÔNG ĐO ĐƯỢC, không gọi pass hoặc thêm finding P1 suy đoán. Nếu phản chứng đúng, hướng vá hẹp vẫn là metadata thuộc kết quả invocation và snapshot danh tính/provenance trước callback; không cần giả kênh hoặc dùng credential.

Hướng nội dung nhạy cảm cũng chỉ mô tả: exception API/subprocess có thể mang dữ liệu người dùng trong 160 ký tự đầu; cắt độ dài không phải redaction. Không soạn payload nhạy cảm hoặc thử credential thật, không ghi nhận rò bí mật khi chưa có phép đo.

## TOÀN VẸN VÀ GIỚI HẠN

N0/A3 và check run ci.yml exact HEAD chưa đo độc lập vì không có Windows/log offline và cấm mạng; pin Ruff CI chưa chạy; A6 chưa đến thời điểm. Các trạng thái đó không được biến thành pass. Không có test nào được tính qua từ output rỗng hoặc rc=0 đơn độc. Kết quả full A/B và readback/cleanup được chốt dưới đây sau khi các writer kết thúc.

Readback cuối: source-initial.json/source-final.json băm 10459 tệp ngoài .git, kể cả ignored/untracked; same_files=true, same_identity=true, initial_clean=true, clean=true; staged/unstaged diff rc=0, output rỗng. HEAD/tree đúng OID ở đầu tệp. Đây chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng có ghi rồi hoàn nguyên.

validation.json: base có đủ 552/552 dòng catalog đúng một lần (516 OK, 32 SAI, 4 không đo); HEAD đủ 577/577 (541 OK, 32 SAI, 4 không đo). Tập hỏng/bỏ qua suite và mutation giống nhau, delta=0; 25 mục wp1122 mới đều OK. 23 ca suite đỏ gồm 10 ca đường run đã biết, 11 ca r484 và hai ca thử gốc tạm /var/tmp trong sandbox; giữ nguyên lỗi nền, không sửa rig để làm xanh. Danh sách tên và output đầy đủ ở ab-summary.json cùng hai log mỗi vế.

Đã dọn bốn cây copy-base/copy-head/tmp-base/tmp-head của riêng lượt này sau khi mọi writer hoàn tất; giữ script, log, JSON, HINT và nguồn test đã đo. Artifact-manifest.json lưu size/SHA-256 hiện vật, không tự băm chính nó. Không sửa cay-kho, push hoặc gọi mạng.

Hoàn tất 2026-11-01T23:05:22.176746+00:00.
