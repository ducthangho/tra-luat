verdict: changes_requested
reviewed_sha: 6cf0cc5231adc6b4fd5bd63c4e97f6aeee30ecdb
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Packet #1122 r1/g1; lease `wp1122-r1-g1-claude`; review_class `sensitive`; lượt 2/10. Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`. Reviewed tree `4b792422b0f27498a5a8f66a5d648bb814614ae2`. Hai mở rộng đã được chủ kho duyệt (raise AssertionError và encoding của các con Python) được tính vào nghiệm thu. Diff `.claude/`: 1 tệp, 234 dòng thêm / 87 dòng xóa; khớp bundle và trần ADR-0053. Head detached, đúng OID ở đầu/cuối.

Reviewer: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; không có bằng chứng độc lập xác định biến thể model/effort của từng request. Shell cục bộ trong sandbox Linux qua API, transport machine; run `2f334acd7bf34ce6a6934b9da5548dda`. Executor là Claude theo packet. Không suy model identity từ Git actor. Không tự cấp quyền merge/land hay xác nhận CI/Windows chưa đọc.

Môi trường đo: Python 3.13.18, Ruff 0.16.9; `/tmp/.git` tồn tại, rỗng/read-only; `/var/tmp` read-only. Mọi chạy suite, probe và đột biến ở bản sao ngoài `cay-kho/`. Lint no-cache và doctrine-scan chỉ đọc checkout gốc. Không mạng, không credential thật. Các lệnh Python đặt `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`; bytecode của probe cũng bị tắt. Sandbox thực tế cho phép ghi workspace; tính chỉ đọc của checkout được giữ bằng cách chọn nơi chạy, không giả nhận mount read-only.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: VERDICT-LUOT1.md, reviewed_sha `30ee4ae1b62170c86b8c75e6b0c73663ab934d88`. Đã chạy lại đúng inventory/probes/encoding_behavior/detail_edges của lượt 1, chỉ đổi đường SOURCE sang bản sao của HEAD; không nhận báo cáo executor thay phép đo.

| Finding / lớp | Kết luận | Bằng chứng độc lập và giới hạn |
|---|---|---|
| F01 / reporter-thong-diep | **VÁ HỜ ở cấp lớp**; các biểu hiện đã báo lượt 1 **ĐÃ VÁ THẬT** | Suite, CLI và kênh TypeError/AssertionError đều còn đúng 160 x, loại một lần; transport OSError giữ message. Bốn mutant reporter đều bị chính khóa giết. Còn bốn biểu hiện cùng lớp: nhật ký lỗi thường, nhật ký assertion, lỗi chốt từ ca khác, lỗi biên dịch đột biến; xem finding duy nhất bên dưới. |
| F02 / khoa-encoding-chi-kiem-khoa | **ĐÃ VÁ THẬT** trong phạm vi nhận diện đã giữ ở hint lượt 1 | cp1252/None đều `giet`, own_signal=true; Unicode thực vẫn chứng minh cp1252 làm sai chữ, nhưng nay khóa bắt được. Bảy biến thể errors/encoding sai khác cũng bị chính khóa bắt. Các giới hạn argv/text-mode đã khai lượt 1 vẫn tồn tại; không có lời gọi sai đang tồn tại trên HEAD. |

Áp lại HINT.patch lượt 1 trên nội dung `30ee4ae` trong `evidence/provenance/` bằng `patch --batch -p0`: rc=0, kết quả khớp từng byte với HEAD. Lời khai `hint_provenance: ... ap nguyen van` là đúng. Việc này không chứng minh đủ độ phủ của chính hint cũ; phép quét lớp mở rộng dưới đây tìm thấy các biểu hiện còn sót.

## BANG NGHIEM THU

Lệnh trong bảng chạy từ thư mục review này, trừ lệnh ghi rõ cwd. `python3 evidence/setup_probe.py` dựng bản sao nguồn cho các probe; nó chỉ chép `.claude/` và `ops/bash_nen.py`. Các script/log đều được giữ lại. N0/A3/CI là những lệnh đọc khả dụng khi có mạng/Windows, **chưa chạy** trong phiên này; không gọi chúng là output đã đo.

| Tiêu chí | Lệnh | Output / bằng chứng | Đạt? |
|---|---|---|---|
| N0: tái hiện Windows trước vá | Chưa chạy: `gh run view 41328709141 --repo ducthangho/tra-luat --log` | Lượt 1/code ghi run trên commit thông điệp 4423d18, TypeError `the JSON object must be str, bytes or bytearray, not NoneType`. Không có log job gốc trong bundle để kiểm độc lập readerthread/cp1252/thứ tự tái hiện → vá. | KHÔNG ĐO ĐƯỢC độc lập; không thay bằng giả Windows |
| N0': Linux base cùng rig | `python3 evidence/run_ab.py` → clone local `--no-hardlinks --no-checkout`, checkout BASE; trong clone: `python3 .claude/dev/launcher_test.py` và cùng lệnh thêm `--dot-bien` | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay); cả hai rc=1 | Đã đo đầy đủ nền; giữ nguyên các lỗi nền |
| A1: đổi assert/raise và khóa AST | `python3 evidence/inventory.py`; `python3 evidence/probes.py`; `python3 evidence/allowlist_edge.py` | 57 assert/11 ca và 8 raise/2 ca chuyển; điều kiện/message có sẵn khớp AST. Chỉ còn 1 assert + 3 raise trong đúng ba ca cố ý. Khóa qua; chèn assert, chèn raise, thêm tên thừa, bỏ raw cuối của tên cho phép đều chết bằng chính khóa. | ĐẠT phạm vi SPEC + mở rộng |
| A2: lỗi trực tiếp còn đúng 160 | `python3 evidence/probes.py` | Khóa A2 qua; bỏ message/đổi trần đều bị chính r1122_loi_mang_thong_diep_cat_160 giết | ĐẠT A2; mục tiêu 3 toàn bộ đường chi tiết CHƯA ĐẠT: F01 |
| Mục tiêu 3: các đường reporter | `python3 evidence/routes.py`; `python3 evidence/transport_edges.py` | Suite/CLI/channel/hook và các dòng neutral/false-credit đã cắt; nhật ký còn 0/60 ký tự, foreign chốt mất message, compiler in 500 x | CHƯA ĐẠT F01 |
| Mục tiêu 4: encoding con Python | `python3 evidence/inventory.py`; `python3 evidence/encoding_edges.py`; `python3 evidence/encoding_behavior.py` | Cả 17 text-mode Python hiện có dùng utf-8/replace; 14 chỗ thêm so base, 22 call hệ thống giữ nguyên. Giá trị sai đã bị chặn trong hình dạng nhận diện. | ĐẠT phép đo Linux/static; nguồn gốc Windows giữ N0 chưa đo độc lập |
| A3: Windows head cuối | Chưa chạy: `gh run view 41333516059 --repo ducthangho/tra-luat --log` | Executor khai windows-latest/runner_id 1000033117 trên fd1f82e: 446/446 đột biến, 118 không đo; suite 282/282, bỏ qua 74, hỏng 0. `.claude` của fd1f82e = HEAD đo được, nhưng không có phép tự đọc log/check trên exact 6cf0cc5. | KHÔNG ĐO ĐƯỢC độc lập; không nâng code-tree bằng nhau thành check-run exact SHA |
| A4: Linux HEAD/base | `ls -d /tmp/.git`; `python3 evidence/run_ab.py`; `python3 evidence/summarize.py` | HEAD: 323/346 ca DA CHAY QUA (tong 356, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi; DOT BIEN: 528/560 dat  (4 khong do duoc tren nen nay). Tập tên lỗi và tập bỏ qua trùng base, delta=0 ở suite và mutation; cả bốn bộ rc=1. | ĐẠT điều khoản delta=0; không gọi các bộ này là N/N xanh |
| A5: bare Ruff F delta | `python3 evidence/audit.py` → `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` ở HEAD/base | Mỗi bên 17 lỗi: 5 F841 ở launcher_test.py, 12 F821 ở tl.py; rc=1, delta=0. Ruff 0.16.9; không cài pin CI 0.15.15 trong rig offline. | ĐẠT delta với Ruff hiện có; không khai bare lint xanh / pin contract đã chạy |
| A5: doctrine | `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` (cwd cay-kho) | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 | ĐẠT |
| A5: whitespace | `git -C cay-kho diff --check c82047da4d6f9546ce1d68282c37acf9567b74bc 6cf0cc5231adc6b4fd5bd63c4e97f6aeee30ecdb` | Rỗng, rc=0 | ĐẠT |
| A5: CI ci.yml exact HEAD | Chưa chạy: `gh api repos/ducthangho/tra-luat/commits/6cf0cc5231adc6b4fd5bd63c4e97f6aeee30ecdb/check-runs` | Không có check-run receipt hiện hành và không gọi mạng | KHÔNG ĐO ĐƯỢC |
| A6 sau land | Chưa land; ngoài quyền review | Không chạy | CHƯA ĐO ĐƯỢC theo SPEC |

## BANG DO

Đã đọc toàn bộ diff.patch, diff-tu-luot1.patch và `git log --format=%B 30ee4ae..HEAD`. `evidence/audit.py` lưu nguyên mọi dòng thêm của diff lượt 2 vào audit.json và mọi commit message vào commits.txt, rồi đo các mệnh đề dưới đây. Việc trích dòng không thay đọc nghĩa, không đặt trần tìm finding: nhánh cũ chưa được sửa nhưng trái yêu cầu mới vẫn được kiểm. Các commit ops/reviews do merge master được tách nguồn lịch sử khi đo, không xem là thay đổi mã launcher của executor.

| Khẳng định | Diff / commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Suite reporter giữ TypeError/TinHieuChotCa và đúng 160 message | Ca mới r1122_reporter...; hai nhánh chay_bo_ca đổi sang mo_ta_loi | probes.py: hai loại giữ 160; LOAI_HONG lần lượt khac:TypeError/TinHieuChotCa; routes.py đo cả AssertionError trần | Có cho các đường đã sửa |
| Transport giữ message | cham_lap_ca đổi nhánh except sang mo_ta_loi | detail_edges.py + transport_edges.py: OSError, TimeoutExpired, ValueError và JSONDecodeError vẫn loi, có loại/message giới hạn 160 | Có |
| Kênh không lấy prefix loại vào message | ten_loai/thong_diep riêng trong CHI_TIET_HONG và main; consumer dùng ten_loai | probes.py + routes.py: TypeError một lần + 160 x; channel JSON có tên loại riêng và message thuần. TinHieuChotCa riêng vẫn giet; foreign signal qua child vẫn loi. | Có |
| Metadata chứa loại thật/message cắt | CHI_TIET_HONG mới, cả hai except; comment ở main | routes.py: tuple TypeError/TinHieuChotCa + 160 x. Cũng đo được metadata không tự xóa khi ca sau qua; hong=0 vẫn có metadata cũ khi gọi main cùng tiến trình. | Có giá trị tại lỗi; không có bảo đảm vòng đời. Chưa thấy đổi điểm, xem giới hạn dưới |
| Khóa encoding đòi literal utf-8/replace | Điều kiện AST mới và thông báo lỗi mới | probes.py chặn cp1252/None/mất encoding; encoding_edges.py chặn errors strict/ignore/None/mất, ascii/rỗng/động. Tất cả own_signal=true, đúng lời thông báo. | Có trong hình dạng nhận diện |
| Bốn mutant reporter mới phát hiện lỗi tương ứng | DOT_BIEN_HARNESS: transport, assertion, exception, lap | probes.py chạy độc lập: 4/4 chết ở chính r1122_reporter..., đúng thông báo suite/transport/lap; không dùng ngoại lệ setup làm tín dụng | Có |
| Hai mutant bảng mã mới phát hiện giá trị sai | DOT_BIEN_HARNESS: cp1252, None | probes.py: 2/2 chết ở chính r1122_con_python_giai_ma_utf8, line 83 | Có |
| Ca mới đo reporter suite và lap, kể cả phân loại | Docstring mới | probes.py, routes.py, transport_edges.py: đã đo thật suite + child, phân loại own/foreign. Nó chưa đo nhật ký/foreign direct/compiler; ba khóa mới trong hint làm HEAD đỏ. | Đúng phạm vi docstring, không đủ để đóng toàn lớp F01 |
| “reporter cat dung 160 ky tu” | Subject commit fd1f82e, mục tiêu 3 | routes.py: journal 0/60; foreign direct mất message; SyntaxError thật với tên tham số trùng dài 500 in nguyên 500 x | Chưa đúng cho toàn bộ đường chi tiết: F01 |
| Áp nguyên văn HINT lượt 1, thêm ca reporter + sáu mutant | Commit fd1f82e / hint_provenance | audit.py áp HINT cũ vào 30ee4ae: rc=0, byte equality=true; probes.py đo đủ sáu mutant mới | Có |
| Master chỉ thêm ops/reviews, .claude/dev không đổi | Commit merge 6cf0cc5 | audit.py: 254 path BASE..180039c và fd1f82e..HEAD, tất cả dưới ops/reviews; OID cây .claude bằng nhau | Có |
| Bốn verdict approve 0/0/0/0; hiện vật, biên nhận và caveat được ghi sổ | Các commit ops/reviews được kéo vào qua master | `python3 evidence/merged_ops.py`: bốn verdict nguồn/flat khớp, đều approve; 59+45+45+92=241 entry SHA256SUMS khớp. Ba dòng cache bổ sung có mặt; DIFF.patch của cả hai lượt #1114 có mặt. README thêm 4 hàng mục lục/19 hàng caveat (3 sandbox, 2 không phải head cuối); cả bốn receipt có schema_version=2 và link blob ghim cf5acfa. Đã đo bằng merged_ops.py. | Nội dung/cấu trúc và băm nội bộ khớp. Nguồn sandbox gốc, danh tính từng phiên và byte của tệp bị omit không có để tự xác minh; không nhận các lời khai lịch sử ấy là đã đo |
| 57 assert/11 ca; 8 raise; 14 encoding thêm; allowance không mục | Các khẳng định kế thừa vẫn chi phối acceptance | inventory.py, probes.py, allowlist_edge.py: điều kiện/message chuyển khớp, helper raw rỗng, tên thừa và tên hết raw đều bị khóa giết | Có |

## BANG TEST

| Bộ | N/M | Bỏ qua / không đo | rc |
|---|---|---|---|
| Base suite | 319/342 ca DA CHAY QUA (tong 352, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| HEAD suite | 323/346 ca DA CHAY QUA (tong 356, bo qua 10, hong 23) - KHONG DU: 10 ca BO QUA, chua do gi | 10 | 1 |
| Base --dot-bien | DOT BIEN: 516/548 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| HEAD --dot-bien | DOT BIEN: 528/560 dat  (4 khong do duoc tren nen nay) | 4 | 1 |
| Bốn khóa r1122 trên HEAD | 4/4 | 0 | probes.py: 0 |
| 12 mutant #1122 trên HEAD | 12/12 chết đúng ca, own_signal=true | 0 | probes.py: 0 |
| Bảy biến thể giá trị encoding/errors sai bổ sung | 7/7 bị đúng khóa bắt | 0 | encoding_edges.py: 0 |
| HEAD + ba khóa mới của hint, chưa áp phần sửa | 3/3 đỏ đúng lý do, own_signal=true | 0 | build_hint.py: 0 (script kiểm phản chứng) |
| HINT: bảy khóa r1122 | 7/7 | 0 | build_hint.py: 0 |
| HINT: 16 mutant #1122 (12 cũ + 4 mới) | 16/16 chết đúng ca, own_signal=true | 0 | build_hint.py: 0 |
| HINT: sáu ca tương thích quanh nhật ký/chấm điểm/main | 6/6 | 0 | validate_hint.py: 0 |

Số liệu đầy đủ, tên ca/mutant và delta ở comparison.json; thời điểm bắt đầu, thời lượng và rc thật ở ab-jobs.json (UTC dễ đọc ở ab-times.json). Bốn bộ A/B chạy tuần tự cùng command/env/kiểu clone. Suite tăng bốn ca qua; mutation tăng 12 mục OK. Mỗi bên 23 ca suite đỏ và 32 mutant SAI. Tất cả mục SAI có neutral đỏ; không gộp chúng thành skipped để thu mẫu số. doctor_bo_do_bash ở cả hai là OK, giet 1/1 t73. Bốn mục không đo giống nhau: 124_khi_chau_con_song và ba mục Windows (g2 directory pin, g4 LA owner, g4 SID alias). Không dùng số 535/560 của executor thay số vừa đo.

23 ca suite đỏ giống base/HEAD: 10 đường launcher.py run đã được packet loại khỏi phạm vi vá, 11 ca r484 vướng tổ tiên /tmp/.git/materializer, và hai ca r858/t86 không ghi được /var/tmp. Mười bỏ qua gồm hai ca native Windows và tám ca cần venv/pypdf không dựng được offline. Việc head đổi AssertionError thành TinHieuChotCa và thêm message làm chi tiết lỗi khác base theo thiết kế; delta=0 ở đây là tập tên và trạng thái, không khai các dòng lỗi giống byte.

## BANG SAN

Mỗi hướng sau đã có lệnh/output thật; mọi nguồn biến thể nằm ngoài checkout. Các chuỗi mới là x, Unicode vô hại hoặc tên giả phục vụ chẩn đoán. Không soạn payload nhạy cảm.

| Hướng độc lập | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| Tương đương chuyển assertion/message | `python3 evidence/inventory.py` | converted 57, cases 11, mismatches []; helper_raw [] | KHÔNG PHẢI LỖI |
| Hai cú pháp assert/raise, hàm lồng | `python3 evidence/probes.py` | raise_name/nested_assert/nested_raise đều giet, own_signal=true | KHÔNG PHẢI LỖI |
| Allowlist thừa và tên hết raw | `python3 evidence/probes.py`; `python3 evidence/allowlist_edge.py` | Tên t73 thừa và t119 không còn raw đều bị chính khóa giết | KHÔNG PHẢI LỖI |
| Helper/alias/unittest/đăng ký trực tiếp | `python3 evidence/probes.py` | Các hình dạng này có thể lọt AST; target vẫn loi, không được cấp tín dụng. Inventory không có vi phạm đang tồn tại kiểu ấy | Giới hạn đã khai lượt 1; KHÔNG PHẢI lỗi hiện hữu |
| F02 giá trị bảng mã và errors | `python3 evidence/probes.py`; `python3 evidence/encoding_edges.py` | cp1252/None và bảy giá trị sai khác đều bị khóa giết đúng ca | KHÔNG PHẢI LỖI còn mở |
| Hình dạng con Python khác | `python3 evidence/probes.py`; `python3 evidence/encoding_edges.py` | sys.executable, biến argv, universal_newlines, text=1 hoặc implicit text có thể lọt; check_output([PY],text=True) thiếu encoding bị bắt | Giới hạn nhận diện, không phải lời gọi sai đang có trên HEAD |
| Unicode/replace có che lỗi không | `python3 evidence/encoding_behavior.py` | HEAD `review ✓`, cp1252 `review âœ“` nhưng khóa nay giet; mutant decode byte sai bị r926 bắt own_signal=true; t73 vẫn chấp nhận note có U+FFFD vì chỉ kiểm tên công cụ | Không đo thấy tín dụng giết giả từ thay đổi này; KHÔNG PHẢI LỖI |
| Suite và CLI in lỗi thông thường/assertion | `python3 evidence/probes.py`; `python3 evidence/routes.py` | suite_x=160, lap_x=160; cả hai CLI rc=1, loại chỉ một lần | KHÔNG PHẢI LỖI |
| Transport và child rỗng/Unicode/foreign | `python3 evidence/transport_edges.py` | Các except giữ loại/message; empty → TypeError; Unicode child 160 ký tự; foreign child vẫn loi | KHÔNG PHẢI LỖI |
| Nhật ký NhatKyCa thật và CLI --nhat-ky | `python3 evidence/routes.py` | TypeError: journal_x=0; AssertionError/TinHieuChotCa: journal_x=60, mất loại | LỖI F01 |
| Chốt của ca khác qua chấm trực tiếp | `python3 evidence/routes.py`; `python3 evidence/transport_edges.py` | `loi, review_chot_caller(chot cua ca khac)`; child cùng ca có loại/message | LỖI F01 ở chi tiết direct, không đổi điểm |
| Dòng SAI của launcher/hook/harness | `python3 evidence/routes.py` | Neutral và false-credit launcher/harness, lỗi hook đều giữ TypeError + 160 x, giet 0/1; không gộp lỗi thành giết | KHÔNG PHẢI LỖI |
| Lỗi compiler thực ở dòng SAI | `python3 evidence/routes.py` / REAL_SYNTAX_ERROR | Duplicate parameter 500 ký tự làm CPython ném SyntaxError; message_x_count=500 | LỖI F01 |
| Metadata cũ sau ca qua/lồng ca | `python3 evidence/routes.py` | second=[1,0,[]]; channel rc=0/hong=0 nhưng ten_loai=TypeError, thong_diep=review-old. Khóa reporter để lại review_vo_can/review_chot | KHÔNG PHẢI lỗi đổi điểm: consumer xét hong trước. Không có tên con trùng CA hiện tại; không khai trạng thái tự sạch |
| Dấu phân cách trong message và khớp tên ca | `python3 evidence/probes.py` / NAME_MATCH | SAI, so_chet=0, can_do=1 khi TypeError có dấu phẩy/ngoặc/newline | KHÔNG PHẢI LỖI: ket_luan_mutant dùng key/loai, không parse detail |
| Gợi ý có khóa đúng lỗi / không phá chốt cũ | `python3 evidence/build_hint.py`; `python3 evidence/validate_hint.py` | 3 khóa mới làm HEAD đỏ; fixed 7/7; mutant 16/16; compatible 6/6; 43 neo harness đều duy nhất; Ruff vẫn 5 F841 | KHÔNG PHẢI LỖI trong phép đo hint; chưa chạy full suite/mutation trên hint |

Các đường thông báo không có exception (thiếu mỏ neo, thiếu ca đích, thiếu kết quả kênh, bỏ qua và headline đếm) đã đọc/đối chiếu; chúng không phải message ngoại lệ nên không ép cắt tên/đếm về 160. F01 không được dùng để mở lại runner giả kênh #1117 đang ngoài phạm vi. Cắt 160 cũng không che bí mật: nếu dữ liệu nhạy cảm ở đầu message thì vẫn vào log. Hướng kiểm API/subprocess có thể đưa dữ liệu ấy vào exception chỉ được mô tả bằng lời; không tạo payload, không dùng credential thật, không nâng giả thuyết thành finding rò bí mật.

## BANG LOP

| Lớp / nguồn | Biểu hiện đã đóng | Còn mở / mức cao nhất | Phép kiểm đóng lớp |
|---|---|---|---|
| reporter-thong-diep / F01 lượt 1, 30ee4ae | Bốn biểu hiện cũ: suite assertion, suite exception, channel trộn loại/message, transport bỏ message | Bốn biểu hiện trong phạm vi mở rộng đã đo: journal thường, journal assertion, foreign direct, compiler SAI. P1, một finding | Mọi đường dùng loại thật + message đúng giới hạn; khóa tương ứng và mutant mỗi đường chết đúng ca. HINT có phép đo này trên bản sao; HEAD chưa có |
| khoa-encoding-chi-kiem-khoa / F02 lượt 1, 30ee4ae | cp1252/None đã bị chặn, giá trị utf-8/replace được kiểm | Không còn biểu hiện F02 mở trong hình dạng scanner đã thỏa thuận giữ. Giới hạn cú pháp không được khai thành bao phủ mọi cách gọi Python tương lai | HEAD qua; các giá trị sai bị đúng khóa bắt, không chỉ có keyword |

## FINDINGS

### reporter-thong-diep [P1] F01 chưa đóng toàn bộ đường báo chi tiết lỗi

TEP/DONG: `.claude/dev/launcher_test.py:15111`, `:15116`, `:212`, `:14853`.

VAN DE: Mục tiêu 3 yêu cầu loại và thông điệp giới hạn 160 ở các đường báo chi tiết. `chay_bo_ca` đã sửa hong_ds nhưng biến `ket` đưa vào NhatKyCa chưa sửa: lỗi thường chỉ còn `LOI TypeError`; lỗi assertion chỉ còn `HONG: <60 ký tự>`, mất loại. Khi tiến trình bị giết trước phần tổng kết, đúng kênh nhật ký được thiết kế để sống sót vẫn mất chẩn đoán. Nhánh foreign chốt của cham_mot_ca trả loi nhưng bỏ cả loại/thông điệp. Nhánh lỗi biên dịch của chay_dot_bien vẫn in nguyên e.msg; compiler thật có thể tạo message dài hơn 160. Đây là cùng lớp F01 còn sót ở các consumer cũ; không nhân bốn biểu hiện thành bốn finding. Các nhánh suite/channel/transport được sửa không làm sai phân loại giết/loi trong các phép đo.

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 evidence/routes.py` và `python3 evidence/transport_edges.py`, rc=0. Journal của TypeError(x*500) có 0 x; journal AssertionError/TinHieuChotCa có 60 x. Foreign direct trả `(loi, review_chot_caller(chot cua ca khac))`; channel cùng ca vẫn có loại + 160 x. Mutant chèn hàm có hai tham số trùng tên dài 500 ký tự vào bản sao launcher gây SyntaxError thật, message_x_count=500 ở dòng SAI. Không dùng payload nhạy cảm hay monkeypatch compiler làm bằng chứng duy nhất.

GOI Y VA: dùng mo_ta_loi ở hai nhánh đặt ket cho nhật ký, ở nhánh foreign direct (giữ nhãn chốt ca khác và loại loi), và ở reporter SyntaxError. HINT.patch (-p0 từ cay-kho) minh họa bốn thay đổi đó cùng ba ca khóa, bốn mutant riêng. `build_hint.py`: cả ba khóa mới làm HEAD chưa vá đỏ bằng TinHieuChotCa của chính khóa; bản sửa qua 7/7 khóa; 16/16 mutant liên quan chết đúng ca. `validate_hint.py`: sáu ca tương thích cũ qua, 43 mỏ neo harness vẫn duy nhất. Tác động cần giữ: loại/giới hạn message phải thống nhất, nhận diện foreign không được thành giet, nhật ký vẫn flush/fsync, tên/key dùng chấm điểm không đổi. Log có thể dài hơn trước (60 → 160); không hứa redaction. Chưa chạy full suite/full mutation trên hint.

DO TIN: cao, các đường đều được gọi và output được lưu; SyntaxError có phản chứng bằng compiler thật. Nhãn hint: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không áp hint vào checkout reviewer hay branch executor.

## TOÀN VẸN VÀ GIỚI HẠN

source-initial.json / source-final.json kiểm hash từng tệp ngoài .git, tracked/untracked/ignored, HEAD/tree, diff working tree và index. integrity.json: same_files=true, same_identity=true, clean=true. Không có delta quan sát được giữa hai mốc; snapshot không chứng minh chưa từng có ghi rồi hoàn nguyên. Các suite có thể tạo ignored marker trong clone riêng; không chạy chúng trên checkout gốc.

Các bản sao tạm của riêng lượt này đã dọn; giữ script, log, JSON đo và HINT.patch. Dựng lại probe bằng setup_probe.py, dựng lại đối chứng bằng run_ab.py. Chưa tự đọc Windows N0/A3, pin Ruff CI và check-run exact HEAD; A6 sau land chưa đến. Không thay những giới hạn này bằng số do executor cung cấp. Verdict changes_requested vì F01; không push, merge, land, gọi LIVE hay sửa mã nguồn cay-kho.
