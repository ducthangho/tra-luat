Reviewed commit: 08aa09610b346edbe64dd2a397de6645e87f2276
Verdict: changes_requested — P0=0 P1=0 P2=4 P3=0

Trạng thái: ĐÃ HOÀN TẤT. Có bốn lớp P2, chưa đủ điều kiện approve theo Q6.

Đã xác minh exact HEAD, worktree sạch, spec SHA256 `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07`, lease r1/g1, base `f712205aa39e0b54d04a5bd8145fa69a84601fed`. Diff: đúng `.claude/dev/packet_loop_test.py`, +252/-14 (A9 đạt). Chỉ ghi thư mục ra và `/tmp`; không ghi kho gốc.

Provider: OpenAI; agent Codex, shell/tool cục bộ trong phiên này; không có bằng chứng máy độc lập về model/session identity. Review offline, không push/PR/LIVE.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| tin-dung-giet-sai | P2 | `.claude/dev/packet_loop_test.py:5358, 5373, 5572, 5632, 6950` | `fast_probe.py`: rc 3–11, traceback stdout, help rc1, BoQua cause/context đều được GIET; tên check hợp lệ có banner bị nhận nhầm crash | kiểm crash ở `run`, tập rc {0,2,12}, stdout/stderr, giữ dấu qua mọi nhánh except; HINT |
| trung-id-chi-do-mot-chieu | P2 | `.claude/dev/packet_loop_test.py:5436, 5776, 5868` | đột biến chỉ chọn bản cuối sống 125/125 kg; status/conclusion đỏ-trước-xanh-sau: rc12→0 | thêm cả thứ tự của bản đỏ/xanh, mutant chọn cuối, ánh xạ K31; HINT |
| ten-trang-chi-khoa-space | P2 | `.claude/dev/packet_loop_test.py:5774, 5818, 5860` | strip(" ") sống 125/125 kg; TAB/NBSP thuần: rc2→0 | thêm tên whitespace ngoài ASCII space, mutant strip hạn chế, ánh xạ K24; HINT |
| fixture-vi-pham-nhieu-chot | P2 | `.claude/dev/packet_loop_test.py:5408, 5409, 5411, 5647, 5681, 5767` | sửa riêng trường đích vẫn rc12: thiếu total_count/THỪA id; mutant blacklist chỉ sửa conclusion không giết được ca in_progress | làm total_count đúng, dùng run không bắt buộc cho trường thiếu, tách status/conclusion trong mutant blacklist; HINT |

Các phép đo chi tiết, CLI thô và màu từng ca được lưu trong `evidence/`.

## Finding đã xác nhận theo lớp

`tin-dung-giet-sai` (P2, M6/A12): probe thật `ValueError→TypeError` cho `TIN_DUNG_GIA`; bọc qua `AssertionError` bằng cause/context/from None vẫn đúng. Tuy nhiên bọc cùng crash qua `BoQua` (cause hoặc context) cho `GIET`, vì nhánh `except BoQua` không duyệt chuỗi crash. Ngoài ra đổi riêng chốt head từ `RC_ARG` sang `RC_STATE` cho rc 8 và được phân loại `GIET`; `_KG_RC_HOP_LE` đang nhận cả rc của các lệnh khác (0,2,3,…,12), thay vì {0,2,12} của `kiem-gate`. Bằng chứng: `evidence/fast_probe.py`, `evidence/fast-results.json`. Đã quét cửa gọi trực tiếp, stdout/stderr, wrapper và module nạp lại; chi tiết bên dưới.

M5: nền tự kiểm M5/M6 đều xanh; ba đột biến độc lập vào (a)/(b)/(c) đều làm đúng ca tự kiểm đỏ. Bốn đột biến `t822_*` nạp module mới đều giết ca đích như dự định; lớp `_TinDungGia` khác danh tính nhưng `main` dùng classifier của đúng module, chưa thấy tín dụng giả trên đường này.

Bổ sung lớp `tin-dung-giet-sai`: (1) nhánh F02 in traceback lên stdout rồi trả rc 12 vẫn được tính `GIET`; (2) đột biến `help="id suite…` → `help=1 or "id suite…` làm riêng `kiem-gate --help` sập rc 1 + traceback: cả `kg_n6_help` và `kg_m4_rc_gate_12` đều `GIET`, ba đối chứng khác họ đều xanh. Đầu đọc crash chỉ đặt trong `_kg`, nên các ca gọi `run()` trực tiếp đi vòng. Bằng chứng mới ở cùng `fast-results.json`.

A8: cả base/head `doctrine-scan` xanh (10 tệp), `adr-song` xanh (53 ADR / 53 dòng). A10: base và head cùng 2 F541, không F821/F401; delta F = 0. Biên nhận ở `evidence/doctrine-*.log`, `adr-*.log`, `ruff-*.json`.

## Hai lớp thiếu độ phủ đã đo

- `trung-id-chi-do-mot-chieu` (P2, K31/M1/M3): thay vòng mọi bản ghi id lớn nhất bằng chỉ bản cuối (`for r in [r for r in cung if r["id"] == id_max][-1:]:`) sống trên toàn bộ 125/125 ca `kg_*`. Hai fixture phân biệt, cùng id/suite/head, bản đỏ ở trước và bản xanh ở sau (riêng status hoặc conclusion), đều cho nền rc 12 → đột biến rc 0, không traceback. Ca hiện tại chỉ khoá trường hợp bản xanh trước/bản đỏ sau; ca hai bản đỏ chỉ đòi tổng 1/1. Xem `evidence/audit-newest_duplicate_last_wins.json`.
- `ten-trang-chi-khoa-space` (P2, K24/M1/M3): đổi `not t.strip()` thành `not t.strip(" ")` sống trên 125/125 ca `kg_*`. Tên chỉ TAB hoặc NBSP, run cùng đúng tên, cho nền rc 2 → đột biến rc 0. Ca mới hiện chỉ dùng một ASCII space; ca tab hợp lệ sẵn có là tab nằm giữa chữ. Xem `evidence/audit-blank_ascii_space_only.json`.

Hai lớp này là thiếu biến thể của các dòng K24/K31 đã có, chưa phải thành phần hoàn toàn vắng bảng; không tự tăng H2 từ 8 lên 9. Kiểm kê độc lập và gate đã hoàn tất.

Kiểm kê độc lập: xem `evidence/independent-inventory.md` và AST `evidence/independent-predicates.json`. Không dòng `tuong_duong`. Tập tên base 555 là tập con của head 576, thiếu 0; thêm 21 tên (biên nhận `evidence/case-names.json`).

A7 đo độc lập: base `nền: 554/554 đạt · BỎ QUA: 1`; head `nền: 575/575 đạt · BỎ QUA: 1`. Cùng ca Windows `luong_canonical_chay_that` bỏ qua. Tập tên không mất ca nào, nền không có ca đổi màu. Sau khi hoàn tất nền base, đã chủ động dừng vòng đột biến thừa của base (tiến trình rc 130; không khai toàn gate base ĐẠT). Gate đầy đủ của head sau đó kết thúc rc0, TỔNG: ĐẠT; số mutant bỏ qua được ghi ở kết luận cuối.

Quét thêm M6: rc 3–11 đều bị cấp `GIET` sai; rc 1,13 và SystemExit(-9) (rc tiến trình 247) được loại đúng. Tên check hợp lệ bằng `Traceback (most recent call last):`, có một run ở suite khác, cho CLI thật rc 0 và một cảnh báo hợp lệ; `_kg` lại ném `CliSapDo` vì dò substring trong cảnh báo. Đây là chiều nhận nhầm crash cùng lớp M6. `fast-results.json` lưu cả CLI thô và phân loại.

A1/A2/A3: mọi ca đích D1–D6 cho rc 0 và `GIET` đúng, gồm cả D5 thiếu status và D6 ca thay thiếu conclusion. Bảng riêng `evidence/d1-d6.md`; mọi CLI thô có trong các tệp `matrix-kg_d*.json`.

## Hướng vá theo lớp và phép khoá

### `tin-dung-giet-sai` — P2

Vá tại `run` và `chay_suite` trong tệp test: đây là hai biên nhận CLI/ngoại lệ của bộ đo; sửa mã sản phẩm không giải quyết được việc bộ đo cấp tín dụng sai. Chuyển kiểm rc/traceback về `run` cho mọi lời gọi `kiem-gate`, kể cả `--help`; chỉ nhận rc 0/2/12; xét cả hai kênh stdout/stderr. Nhánh `except BoQua` cũng phải gọi `_co_sap_do` trước khi chuyển ngoại lệ thành chuỗi hay skip.

Khoá bằng chính CLI sập thật: F02 ValueError→TypeError, traceback xuất stdout với rc12, traceback bọc repr, help formatter sập rc1, các wrapper AssertionError/BoQua dùng cause/context/from None; giữ cặp sống/giết thật `suite = 1`. Thêm đối chứng tên check chứa banner traceback nhưng chỉ sinh cảnh báo hợp lệ. Tất cả đường lỗi phải được nhận `TIN_DUNG_GIA`, riêng fallback xanh giả vẫn `GIET`; gỡ phép loại sập phải làm ca tự kiểm đỏ.

Nguy cơ vá: phân loại theo một substring lại nhận nhầm tên check hợp lệ; thiếu dò stdout/nhánh except lại mở cửa rửa tín dụng. HINT yêu cầu banner kèm frame, xử lý traceback thô và repr, có ca tên check chứa banner để canh chiều bắt oan. Đột biến cũ đổi RC_GATE 12→8 phải đổi thành 12→0 để tiếp tục đo mã thoát bằng một giá trị trong tập hợp lệ, thay vì cố giữ tín dụng cho rc8 trái M6. Các lớp ngoại lệ vẫn thuộc đúng module suite được nạp lại; không thay classifier trong `main` về module cha.

### `trung-id-chi-do-mot-chieu` — P2

Vá fixture K31 và `MUTANTS`/bảng K31. Thêm bản ghi cùng id/suite/head mà bản đỏ đứng trước bản xanh, riêng từng trường status và conclusion; giữ ca chiều ngược đã có. Thêm đột biến chỉ chọn bản cuối trong nhóm id lớn nhất. Fixture mới phải có total_count bằng số id phân biệt (1), tránh chốt danh tính hoặc N5 chặn hộ.

Khoá: nền rc12 đúng lý do status/conclusion, mutant chọn cuối rc0 và được `GIET`; mutant chọn đầu hiện có vẫn chết trên ca xanh trước/đỏ sau. Nguy cơ vá: dùng head khác nhau sẽ đo K18 thay K31; dùng id khác nhau sẽ đo K30; dùng cả hai bản đỏ không phân biệt được phép chọn một bản với đòi mọi bản. HINT giữ các trường danh tính đồng nhất.

### `ten-trang-chi-khoa-space` — P2

Vá fixture K24 và thêm đột biến thu hẹp strip sang ASCII space. Tên chỉ TAB hoặc NBSP được dùng cho cả `--bat-buoc` lẫn run để mọi chốt khác hợp lệ. Không cần tạo byte UTF-8 hỏng, đường dẫn đặc biệt hay symlink.

Khoá: nền rc2 kèm `không được rỗng`, mutant rc0; giữ các ca tên có tab giữa chữ và chuỗi backslash+n để bảo vệ chiều hợp lệ. Nguy cơ vá: dùng ký tự mà splitlines cắt sẽ bị chốt xuống dòng chặn hộ, không đo whitespace thuần; dùng run tên khác sẽ ra VẮNG. HINT dùng TAB/NBSP không bị splitlines cắt và run có đúng tên.

## HINT.patch

`HINT.patch` chỉ chạm `.claude/dev/packet_loop_test.py`; đã `git apply --check` trên bản sao exact head. Nhãn bắt buộc nằm trong tệp: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

Đã đo trên bản sao HINT: 129/129 ca kg xanh; các đột biến mới K24/K31 và mutant rc0 đều giết đúng ca; gỡ classifier TÍN_DỤNG_GIẢ làm tự kiểm M6 đỏ. Sau bổ sung nhận diện traceback repr và đối chứng tên check hợp lệ, chạy lại M5/M6 và chốt mỏ neo đúng-một-chỗ đều xanh (`hint-final-self.log`). Ruff HINT vẫn chỉ hai F541 như base/head. Tổng diff HINT so base +327/-19, đúng một tệp, dưới trần 450 dòng thêm. Chưa chạy gate đầy đủ trên HINT; đây là gợi ý test có thể áp, không phải ứng viên đã được review/approve.

## Đột biến kiểm toán bổ sung

`evidence/audit-summary.jsonl` và từng `audit-*.json` ghi toàn bộ tên ca/màu. Các đột biến gỡ kiểm thiếu total_count, chỉ đọc trang đầu, gỡ lọc id lớn nhất, đảo lý do thiếu/thừa đều bị giết; riêng đổi lý do không đổi rc vẫn làm ca đỏ như M1 yêu cầu. Hai đột biến sống làm xanh giả là hai finding K24/K31 ở trên.

Hai đột biến trình bày khác cũng sống: bỏ `sorted` danh sách id cảnh báo và đảo thứ tự tên bắt buộc. Ghi rõ giới hạn: không tìm được yêu cầu trong đặc tả buộc hai thứ tự ấy; các đột biến này không bỏ điều kiện cấp màu hay thay chính lý do từ chối. Vì vậy ghi nhận hiện trạng phép đo, không gán severity thêm hoặc tính H2.

## Ngoài phạm vi và giới hạn

Không sửa `packet_loop.py`; không xác minh nguồn gốc JSON/API; không gán finding cho ca ngoài họ kg. Hai ca codepage chỉ được đưa vào biên nhận A11 vì đặc tả yêu cầu. Các đầu vào cần tự soạn đường dẫn thoát cây/byte bất thường/symlink: không cần thêm hướng nào như vậy để chứng minh bốn finding; các fixture có sẵn trong suite được chạy nguyên trạng trong bản sao.

Không có PR/push/CI từ xa trong lượt này. Dữ liệu đây không tạo authority land hoặc receipt provenance. `HINT.patch` cần executor tái dẫn xuất và chạy gate trên head mới. A7 chỉ đo môi trường Linux/Python 3.13.16; ca Windows tiếp tục bỏ qua đúng như base, không khai đã đo trên Windows.

## `fixture-vi-pham-nhieu-chot` — P2 (M3)

M3 bắt buộc fixture ca từ chối chỉ vi phạm chính thành phần đang đo, mọi thứ khác hợp lệ, nêu rõ total_count phải khớp. Quét cùng lớp tìm được: hai ca sai/thiếu check_runs không khai total_count (`_kg_dem` bỏ qua trang có check_runs sai kiểu); ca mới `kg_k15_bo_qua_run_thieu_suite` có hai id nhưng cố khai 1; ca cũ `kg_m2_thieu_conclusion` cũng có hai id nhưng khai 1 và vẫn được dùng làm đích cho mutant bỏ phần tử thiếu trường. Probe `fixture_isolation.py` sửa riêng trường đích trên từng fixture: tất cả vẫn rc12 vì thiếu total_count hoặc THỪA id. Đây là vi phạm độc lập yêu cầu fixture M3; assertion lý do hiện tại vẫn có ích và không bị gọi nhầm là lỗi M6. Ca thay D6 mới đã đúng A3, không phủ định kết quả A3.

Cùng lớp trên K33: `kg_m3_in_progress` có cả status chưa completed lẫn conclusion null, nhưng nằm trong ca đích của `kg_danh_sach_cam` ánh xạ K33. Mutant hiện tại đồng thời bỏ điều kiện status và đổi luật conclusion thành blacklist. Giữ điều kiện status, chỉ đổi conclusion sang đúng blacklist ấy, ca này vẫn xanh (`blacklist-isolation.json`: SONG). Tín dụng của riêng ca này đến từ bỏ hai điều kiện. Các ca conclusion khác vẫn có ích; không kết luận toàn K33 mất phủ.

Vá tại fixture/mutant và ánh xạ ca đích trong tệp test, không ở sản phẩm: điền total_count cho trang sai check_runs; khai đúng 2 cho hai run; dùng run không bắt buộc cho conclusion thiếu để gỡ kiểm không KeyError. Giữ status trong mutant blacklist và bỏ ca sai cả hai trường khỏi phai_chet của mutant ấy; giữ tên ca trong CASES để A7 không mất tên.

Khoá: sau sửa riêng lỗi fixture, CLI phải không còn bị total_count từ chối; dưới mutant skip run, ca vẫn đỏ vì assertion đúng lý do (rc12 + lý do thiếu trang thay lý do trường đích là hợp lệ theo M1). D6 trên ca thiếu conclusion phải rc0; mutant conclusion đơn phải giết các ca chỉ sai conclusion, không gán tín dụng cho in_progress+null. Nguy cơ vá: ép mọi mutant skip run phải rc0 lại khiến người vá khai sai count; A2 chỉ buộc rc0 cho D1–D6. HINT giữ yêu cầu phân biệt lý do của các mutant còn lại và không sửa sản phẩm.

HINT sau khi đóng lớp fixture M3: `evidence/hint-final.json`/`.log` cho 130/130 ca nền (129 kg + chốt mỏ neo) xanh; cả 12 mutant chọn để khoá các phần thay đổi đều giết đúng ca đích và ba đối chứng khác họ xanh. Biên nhận này thay cho các phép đo HINT trung gian; không thay gate toàn suite trên head ứng viên mới.

Các fixture HINT đã được probe lại bằng đúng closure của ca test: sửa riêng trường đích cho bốn ca trong `hint-fixture-isolation.json` đều ra rc0 (trên head gốc cả bốn vẫn rc12 do total_count). Ruff HINT cuối vẫn 2 F541, delta 0.

A11 hoàn tất: 73/73 đột biến kiểm kê × 127 tên ca = 9.271 dòng màu, gồm 126 ca thực gọi kiem-gate và một ca tự kiểm bảng. CLI thật: 9.650 lần (xem `evidence/A11-summary.json`); không lỗi mỏ neo, không thiếu tên ca/cửa gọi. `evidence/A11-colors.csv` liệt kê từng tên và màu, `matrix-*.json` giữ rc/stdout/stderr từng lệnh. Hai ca codepage được dựng đầy đủ ở nền; dưới mỗi mutant, replay đúng lệnh kiem-gate/fixture/encoding của ca đó, không chạy lại các lệnh không liên quan trong kịch bản codepage. Không bỏ assertion rc0/stdout khác rỗng; hậu kiểm biên nhận xác nhận không có trường hợp replay bị đánh xanh sai.

A11 bắt được tín dụng sai ngay trên mutant khai báo: `kg_rc_gate_thanh_8` → `kg_m4_rc_gate_12`, CLI rc8, suite cấp GIET (`invalid_target_cli_kill_credit` trong A11-summary). Cùng lớp M6, crash CLI thật được nhét vào ExceptionGroup rồi ném sau khi thoát except (không có cause/context trực tiếp) vẫn GIET; fast-results ghi `group`. HINT duyệt cả ngoại lệ con của BaseExceptionGroup nếu Python hỗ trợ, ngoài cause/context và chống vòng.

## Gate và kết luận cuối

Gate head đầy đủ: `python3 -B /tmp/wp822-review-head/.claude/dev/packet_loop_test.py` **rc 0**, `nền: 575/575 đạt · BỎ QUA: 1`, **TỔNG: ĐẠT**. Có **318** mutant khai báo: bộ chạy báo giết **317**, bỏ qua **1** (`luong_canonical_chay_that_dao_os_name`) do ca Windows. Không khai đã giết đủ 318. Log nguyên văn `evidence/head-suite.log`; rc thật `evidence/run-results.json`. A11 còn chỉ ra một tín dụng giết sai ngay trong mutant được khai báo (`kg_rc_gate_thanh_8`), nên gate xanh không xoá finding M6.

| tiêu chí | kết quả đo |
|---|---|
| A1–A3 | D1–D6 đủ cặp nguyên văn; tám ca đích CLI rc12→0, GIET; đối chứng khác họ xanh; ca thay D6 không THỪA id |
| A4 | ba vế M5 có răng riêng; thêm mutant ngoài bảng / tên không tồn tại / xoá K14 đều làm tự kiểm đỏ |
| A5 | không có dòng tuong_duong; chưa tìm được thành phần hoàn toàn vắng bảng và sống khi gỡ; không tăng H2 |
| A6 | lệnh rc0, nền 575/575, 1 skip, TỔNG ĐẠT; yêu cầu mọi mutant bị giết chưa được chứng minh: 1 mutant Windows bỏ qua, 1 tín dụng giết trong bảng sai M6 |
| A7 | đủ 555 tên base trong 576 tên head; nền base 554/554, nền head 575/575; cùng một skip Windows |
| A8 | doctrine-scan và adr-song: base/head đều rc0 |
| A9 | đúng một tệp +252/-14, dưới trần 450 |
| A10 | base/head cùng 2 F541; F821/F401 đều 0; delta F = 0 |
| A11 | 73/73 mutant, 127 tên/126 ca thực gọi CLI; 9.271 màu và 9.650 lệnh; probe lỗi 0 |
| A12 | cặp tự kiểm hiện tại xanh, gỡ classifier làm đỏ; các đường crash chưa được tự kiểm đủ là finding M6 |

M1/M3/M6 vẫn chưa đạt theo bốn lớp P2 đã nêu. Ngưỡng approve là P0=P1=P2=P3=0; **changes_requested**. Không cần sửa mã sản phẩm để đóng các lớp này; không phát hiện điều kiện dừng H2=9. Mutant Windows nằm ngoài họ kg, chỉ ghi hạn chế gate, không cộng hạng theo quy định phạm vi.

HINT cuối: tổng diff đề xuất so base +327/-19; chỉ tệp test; apply-check rc0; 129/129 ca kg cộng chốt mỏ neo đều xanh, 12 mutant kiểm phần vá giết đúng ca đích/giữ đối chứng xanh. M6 đã gồm ExceptionGroup, traceback repr và đối chứng banner trong tên hợp lệ; Ruff vẫn 2 F541. Chưa chạy toàn suite trên HINT.

Kết thúc kiểm tra lại exact SHA và worktree gốc sạch (`repository-final.json`). Không sửa tệp hoặc ref nào trong KHO.
