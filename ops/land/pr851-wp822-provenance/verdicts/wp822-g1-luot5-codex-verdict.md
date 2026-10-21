Reviewed commit: c1f7fddc8adc16df025efa96e3ca2f59e7a6a9e0
Verdict: changes_requested — P0=0 P1=0 P2=7 P3=0

## Định danh và phạm vi

Reviewer độc lập: OpenAI, agent Codex/GPT-6 theo cấu hình phiên; thực thi qua shell, transport machine/local, offline. Không dùng context executor, không gọi reviewer khác, không ghi KHO, không push/PR/comment GitHub. Đây là lời gọi 5/8 được giao.

- HEAD `c1f7fddc8adc16df025efa96e3ca2f59e7a6a9e0`, tree `d6cd63d3593acf5b0c2bf50e11c16f9b3904194e`; kho đầy đủ, detached, sạch.
- Base `f712205aa39e0b54d04a5bd8145fa69a84601fed`. Đã đọc trọn đặc tả trên base; SHA-256 `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07` khớp. [Đặc tả](evidence/wp822-spec.md), [lease](evidence/wp822-lease.yaml).
- Write set và diff đúng một tệp `.claude/dev/packet_loop_test.py`, **+547/−19**; sản phẩm `packet_loop.py` không đổi. Vượt 450 đã được chủ kho cho phép, không tính finding.
- [Định danh](evidence/repository-identity.json), [kiểm cuối nguồn](evidence/source-final-check.json). Sandbox phiên chỉ cho ghi thư mục ra và `/tmp`. Snapshot chỉ chứng minh không có delta quan sát được ở các mốc, không chứng minh lịch sử không từng ghi rồi hoàn nguyên.

## Bảng lớp đã chốt

Mọi vị trí dưới đây thuộc `.claude/dev/packet_loop_test.py` trên **head được review**, không phải số dòng HINT. Mỗi mutant sống đã chạy đủ **173/173 ca kg xanh**, kèm fixture riêng có rc đổi và không crash. Có **44 mutant sống thuộc 7 lớp**, không phải 44 finding riêng.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `id-lon-nhat-chua-do-so-hoc` | P2 | `packet_loop_test.py:5818`, `:5986`, `:6073` | **3** mutant sống: lấy bản cuối, `key=abs`, `key=float`; thứ tự giảm, ID âm, hai số nguyên kề nhau trên 2^53 đều **rc12→0** | Sinh cặp ID × hai thứ tự × hai chiều màu; neo expected vào ID lớn hơn trong fixture; nối K30 |
| `kiem-tra-toan-bo-chua-phu-vi-tri` | P2 | `packet_loop_test.py:5430`, `:5550`, `:6058`, `:6060`, `:6066`, `:6072` | **7** mutant sống: chỉ kiểm tên đầu/cuối/hai đầu; chỉ kiểm danh tính hai bản đầu/hai đầu; chỉ ghi VẮNG cho tên đầu hoặc khi có run. Các fixture riêng **rc2/12→0** | Sinh vị trí và tập con: K24 mọi tên; K16–K18 mọi bản ghi/ID; K29 mọi tập tên vắng, cả 0 run và chỉ có suite khác |
| `sha-chi-do-ngan-va-hoa` | P2 | `packet_loop_test.py:5813`, `:5815`, `:6063` | **3** mutant sống: trim đối số, NFKC đối số, `[\da-f]` thay `[0-9a-f]`. SHA đệm trắng, fullwidth chữ, fullwidth chữ số đều **rc2→0** | Sinh dạng sai ở chính `--head`, đủ nhóm chữ/số hex; không lấy ca so head K34 thay kiểm dạng K21 |
| `check-suite-chua-phu-bien-chuoi` | P2 | `packet_loop_test.py:5498`, `:6064` | **2** mutant sống: `rstrip` hoặc NFKC trước regex. `1 ` và `１` đều **rc2→0** | Sinh whitespace hai phía và Unicode ở đối số suite, giữ K22 tách biệt fallback quá trần int K23 |
| `chi-kiem-kieu-trang-dau` | P2 | `packet_loop_test.py:5787`, `:5829`, `:6000`, `:6047` | **3** mutant sống: bỏ trang không-object phía sau, bỏ trang thiếu `check_runs` phía sau, nhận `check_runs` là string. Trang scalar/thiếu khóa/chuỗi rỗng sau trang hợp lệ đều **rc12→0** | Sinh mọi nhóm kiểu JSON của trang và check_runs, cả thiếu khóa, ở đầu/giữa/cuối; count toàn cục đúng; nối K05 |
| `trung-id-chi-do-mot-chieu` | P2 | `packet_loop_test.py:5464`, `:5808`, `:6074`, `:6075` | **1** mutant sống: chỉ kiểm status ở bản đầu. Cùng ID, bản đầu xanh/bản sau `in_progress`, conclusion đều success: **rc12→0** | Sinh riêng status/conclusion đỏ ở mọi vị trí trong ≥3 bản cùng ID; giữ danh tính nhất quán; nối K31/K32/K33 |
| `kiem-kieu-chi-do-mot-loai-sai` | P2 | `packet_loop_test.py:5790`, `:5791`, `:5793`, `:5820`, `:6051`, `:6057` | **25** mutant sống trong tích trường × kiểu JSON sai, tất cả fixture riêng **rc12→0**; chi tiết bên dưới | Sinh tập đóng null/bool/int/float/str/list/dict cho từng trường, vị trí và phân trang; nới riêng một kiểu của riêng trường; nối K09–K13/K15 |

[Toàn bộ cặp tìm/thay, từng tên ca/màu, rc và stdout/stderr](evidence/audit-all-summary.json), [danh sách kiểm toán](evidence/audit-survivors.md); từng `evidence/audit-<name>.json` là phản chứng chạy lại được. Không gán màu xanh của suite cho tính đầy đủ của các lớp.

### Đủ biểu hiện của lớp kiểu JSON

| trường | kiểu sai được nới mà vẫn sống 173/173 | số mutant sống |
|---|---|---:|
| id | null, float | 2 |
| name | null, bool, float, list, dict | 5 |
| head_sha | null, bool, float, list, dict | 5 |
| status | null, bool, float, list, dict | 5 |
| conclusion | bool, float, list, dict | 4 |
| check_suite.id | null, float, list, dict | 4 |

Đã thử **33** mutant kiểu riêng biệt: 25 sống, 8 bị ca cũ giết (id bool/string; name/head/status/conclusion int; suite.id bool/string). Mỗi fixture có một run bắt buộc hợp lệ và một run không bắt buộc chỉ sai trường đích, total_count đúng. Không dùng biến thể id list/dict để nhận GIẾT: nới riêng nó làm id không hash được và crash, trái M6; các fixture từ chối ấy vẫn có trong nền HINT.

### Cách vá và rủi ro cần giữ

1. **ID:** HINT sinh lo/hi, đảo thứ tự và đổi chiều đỏ/xanh. Expected lấy từ cặp fixture, không từ phép chọn ID của sản phẩm. Không chỉ thêm một cặp số dương tăng dần.
2. **Lượng từ:** HINT quay vị trí xung đột ở ID không phải ID đầu tiên, thử đủ tuple danh tính; đặt tên hỏng đầu/giữa/cuối; thử mọi tập con hiện diện của ba tên. Giữ count, suite và kiểu khác hợp lệ, tránh K20 hoặc schema chặn hộ.
3. **SHA:** giá trị `--head` và run.head_sha trùng nguyên văn để duy nhất kiểm dạng đối số quyết màu. Có cả đầu vào nền chữ và nền số; không chuẩn hóa expected để làm ca xanh.
4. **Suite:** tên/run/head còn lại hợp lệ. Các chuỗi sai dạng phải rc2; chuỗi ASCII 4301 chữ số đúng dạng vẫn VẮNG rc12 và không crash, không gom hai hợp đồng này.
5. **Trang:** tách không-object, thiếu khóa và check_runs sai kiểu. Các trang hợp lệ còn lại khai cùng count đúng; không sửa sản phẩm hoặc nuốt trang hỏng để làm fixture qua.
6. **Trùng ID:** HINT đặt một bản đỏ trong ba bản, riêng từng field, cùng mọi vị trí. Không dùng head khác để thử K31 vì K18 phải chặn mâu thuẫn danh tính trước đó.
7. **Kiểu:** HINT chạy mọi loại JSON sai ở đầu/giữa/cuối, trong một trang và nhiều trang. Run không bắt buộc tránh truy cập field hỏng sau khi nới kiểu. Mutant chỉ nới đúng một field/kiểu; luôn kiểm GIẾT và đối chứng, không nhận crash làm bằng chứng.

## Kiểm kê, ca đích và M5/M6

Đã tự kiểm kê hai hàm, gồm 45 nút AST điều kiện/so sánh/bool/except, đối chiếu **41 K / 161 mutant phân biệt**. K38–K40 là bổ sung đúng hành vi; K41 help argparse ngoài hai hàm được giữ cho M5(a). **Không có dòng tuong_duong**, không có miễn phép đo tương đương. Không tìm thấy thành phần hoàn toàn vắng bảng; các finding là thiếu phủ của K đã có, **không kích hoạt H2=9**. [Bảng độc lập](evidence/inventory-independent.md), [AST](evidence/independent-predicates.json), [runtime bảng và mutant](evidence/inventory-runtime.json).

D1–D6 đúng cặp nguyên văn, mỗi mỏ neo khớp một chỗ. Mọi ca đích riêng **rc12→0**, GIẾT thật, ba đối chứng khác họ xanh. D6 trên cả `kg_m2_thieu_conclusion` tên cũ và ca thay đều rc0, không THỪA id. Bốn fixture từng sai nhiều chốt: sửa riêng field đích đều rc0. [D1–D6](evidence/D1-D6.json), [surgical repair](evidence/fixture-isolation.json).

M5(a)/(b)/(c) có răng độc lập: thêm kg ngoài bảng, thêm tên không tồn tại, đổi tên K27 giữ toàn ánh xạ chỉ làm lần lượt (a)/(b)/(c) đỏ. Ba mutant t822 tương ứng cũng đỏ đúng vế.

M6 chạy nguyên phản chứng có sẵn: các vỏ × hai kênh, escape, rc ngoài bộ, help, cause/context/from None/BoQua/group và banner trong fixture/đối số. Chín guard t822_m6, classifier coi mọi đỏ là GIẾT và bốn guard độc lập (cause/context/except thường/chỉ stdout) đều làm tự kiểm đỏ, đối chứng xanh. Module nhắm test nạp riêng có marker khác danh tính; main/classifier dùng đúng module. [Tự kiểm](evidence/selfcheck-results.json). Không tự viết mã in/giả/bọc traceback hoặc payload gây sập.

## Gate và nghiệm thu

Lệnh gate chạy trên bản sao tạm nguyên vẹn, không trên KHO:

```text
cp -a /home/user/rv822 /tmp/wp822-rv5-gate
PYTHONDONTWRITEBYTECODE=1 python3 -B -u /tmp/wp822-rv5-gate/.claude/dev/packet_loop_test.py
```

**rc0 · nền 623/623 đạt · BỎ QUA 1 · TỔNG: ĐẠT.** Có 415 mutant: **414 GIẾT**, **1 BỎ QUA** (`luong_canonical_chay_that_dao_os_name`, Windows, ngoài họ kg). Không khai đã giết cả 415. [Log đầy đủ](evidence/gate.log), [tổng gate](evidence/full-suite-summary.json), [rc tiến trình](evidence/tool-run-results.json).

A11: **161/161 mutant × 175 tên = 28.175 màu**, **41.563 lượt CLI dưới mutant**, cộng **263** lượt nền. Đủ mọi tên, kể cả M5 không gọi CLI và M6 có nhiều lệnh. Hai ca cp1252/cp1258 chạy đầy đủ ở nền; dưới mỗi mutant phát lại đúng lệnh kiem-gate/fixture/encoding và assertion rc0/stdout có nội dung. Không lặp chuỗi lệnh ngoài phạm vi của hai ca này. Tất cả ca ngoài đích đổi màu được ghi, kể cả crash được phân loại tín dụng giả và không nhận GIẾT. [CSV từng màu](evidence/A11-colors.csv), [tổng A11](evidence/A11-summary.json).

Đối chiếu CLI độc lập cho **246 ca đích**: tất cả có rc hoặc nội dung CLI thực sự đổi sau khi loại đường dẫn tạm/địa chỉ bộ nhớ; không có target chết mà CLI không đổi. Từng cặp đầu ra tại [target deltas](evidence/target-cli-deltas.json), [tổng](evidence/target-cli-delta-summary.json). Không mỏ neo lỗi, target SỐNG hoặc tín dụng crash trong bảng.

| tiêu chí | kết quả |
|---|---|
| A1–A3 | D1–D6 đủ, GIẾT thật, mọi đích rc12→0; D6 tên cũ rc0; đối chứng xanh |
| A4 | ba vế M5 có răng riêng |
| A5 | không tuong_duong, không K hoàn toàn vắng; còn bảy lớp phủ thiếu được chứng minh |
| A6 | full gate rc0, 623/623, TỔNG ĐẠT; một skip Windows khai riêng |
| A7 | base checkout đúng SHA: 554 GREEN + 1 SKIP; head 623 GREEN + 1 SKIP; đủ 555 tên base trong 624 tên, thiếu/trùng/đổi màu 0 |
| A8 | doctrine-scan/adr-song base và head đều rc0, có đầu ra dương |
| A9 | một tệp +547/−19, được phép vượt 450; sản phẩm không đổi |
| A10 | Ruff 0.17.1 --select F: base/head cùng rc1 vì 2 F541, F401=F821=0, delta F=0 |
| A11 | đủ 161 mutant và 175 tên; không lỗi probe hoặc target tín dụng giả |
| A12 | tự kiểm M6 xanh; gỡ từng chốt đã thử làm tự kiểm đỏ |

[A7 từng tên](evidence/A7-colors.csv), [base/head thực đo](evidence/baseline-gates.json), [Ruff base](evidence/ruff-base.json), [Ruff head](evidence/ruff-head.json). Lần đo base đầu chỉ dùng nội dung base trong bản sao HEAD; đã thay bằng phép đo lại trên checkout thật f712205, giữ bản cũ riêng để không nhập nhằng.

Probe A11 có một lần ngắt chủ ý rc130 để tiếp tục 141 mutant còn lại với 8 worker thay vì 4; 20 kết quả hoàn tất giữ nguyên. Thư mục của mutant chưa xong được dựng lại sạch. Chỉ launcher.py bất biến được cache bytecode CHECKED_HASH đã đối chiếu source; product/test vẫn chạy từ source với -B. Không thay source mutant, fixture hoặc cắt tên ca. [Probe đầu](evidence/matrix_probe.py), [tiếp tục](evidence/matrix_resume.py), [cache](evidence/launcher-cache.json).

Kiểm toán bổ sung **63 mutant × 173 ca = 10.899 màu**: 44 SỐNG gây vi phạm trong bảy lớp; 13 bị ca cũ giết; 6 quan sát đổi chi tiết đầu ra giữ nguyên rc không được dùng làm finding. Sáu quan sát liên quan ID/head/thứ tự trên dòng xanh hoặc thứ tự ID cảnh báo: K36 chỉ chốt suite/tên xuất hiện một lần, K26 không chốt thứ tự liệt kê; không có lý do từ chối đổi. Không biến chúng thành lỗi sản phẩm chưa được đặc tả. Toàn bộ vẫn có biên nhận trong tổng kiểm toán.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| lượt | lớp | nhãn | bằng chứng trên head hiện tại |
|---|---|---|---|
| 1 | tin-dung-giet-sai | đã vá thật | nguyên fixture M6 và mọi guard đã thử có răng; classifier đúng module nạp lại |
| 1 | trung-id-chi-do-mot-chieu | vá hờ | chọn bản đầu/cuối cũ đã bị giết, nhưng chỉ kiểm status ở bản đầu vẫn sống 173/173 |
| 1 | ten-trang-chi-khoa-space | đã vá thật | TAB/NBSP giết strip-space, giữ các chiều tên hợp lệ; lượng từ nhiều tên là lớp riêng |
| 1 | fixture-vi-pham-nhieu-chot | đã vá thật | sửa riêng bốn fixture cũ ra rc0; blacklist giữ status; D6 tên cũ ra rc0 |
| 2 | tin-dung-giet-sai | đã vá thật | vỏ JSON/repr/log/escape có sẵn được loại đúng; không tín dụng giả từ marker khác module |
| 2 | sha-chi-do-ngan-va-hoa | vá hờ | phi-hex/39/41/hoa đã khóa; trim hoặc NFKC đối số head vẫn sống |
| 2 | id-lon-nhat-chua-do-so-hoc | vá hờ | key=str đã khóa nhưng thứ tự đầu vào, dấu âm và chính xác trên 2^53 chưa khóa |
| 2 | canh-bao-chi-do-mot-id | đã vá thật | ba tên, ba ID, bản lặp; cắt đầu/cuối/giữa đều bị ca r4 giết |
| 2 | chi-kiem-kieu-trang-dau | vá hờ | kiểu run/suite/count phía sau đã khóa, object của chính trang phía sau còn lọt |
| 3 | chi-kiem-kieu-trang-dau | vá hờ | bool run.id/suite.id và tc âm đã khóa; K05 phía sau còn sống |
| 3 | khoa-trung-chua-phu-moi-tang | đã vá thật | suite.id và extra root/object/array có ca đích cùng lý do khoá trùng |
| 3 | so-khop-tuyet-doi-chua-du | đã vá thật | cơ chế r4 bao các vị trí == chuỗi và chiều THA một phía; kiểm dạng đối số là hai lớp riêng |
| 3 | bao-loi-chi-do-mot-ten | đã vá thật | ba tên đỏ, các mutant đầu/cuối/bỏ giữa bị giết; số tên đỏ đúng |
| 3 | tin-dung-giet-sai | đã vá thật | bỏ cause-only/đối số riêng/context/group/nhánh BoQua đều làm tự kiểm đỏ |
| 4 | so-khop-tuyet-doi-chua-du | đã vá thật | đầy đủ họ r4 gần đúng và không chuẩn trùng nguyên văn; A11 đã hoàn tất đủ mọi mutant |
| 4 | bao-loi-chi-do-mot-ten | đã vá thật | kiểm đủ ba tên đỏ; mutant r4 chọn cuối/bỏ giữa chết |
| 4 | canh-bao-chi-do-mot-id | đã vá thật | ba ID và ba tên được so đủ, id phân biệt, đúng stderr |

Không có bằng chứng “vá sinh lỗi mới”; bảy lớp là khoảng trống phủ còn thiếu. Các slug cũ được giữ để không xóa lịch sử tái diễn. Quét kiểu JSON là lớp mới về tập loại sai, khác lỗi phạm vi trang; HINT thử cả tích kiểu và vị trí để không vá riêng một trục.

## HINT.patch

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

[HINT.patch](HINT.patch) chỉ sửa `.claude/dev/packet_loop_test.py`. Apply-check, apply thật trên bản sao pristine exact head, diff-check và so bytes đều đạt. Diff so head **+163/−18**, tổng so base **+692/−19**. [Biên nhận áp và hash](evidence/hint-apply-final.json).

HINT cuối: **187/187 nền xanh** (186 kg + chốt mỏ neo), **58/58 mutant mới GIẾT đúng ca đích**, **44/44 mutant kiểm toán sống được phát lại đều GIẾT**, mọi đối chứng khác họ xanh; không tín dụng giả. Bare Ruff vẫn chỉ hai F541 có sẵn. [Kết quả HINT đúng hash](evidence/hint-results-complete.json), [Ruff HINT](evidence/ruff-hint-final.json). Chưa chạy full suite trên HINT; full gate phía trên thuộc SHA đang review.

HINT dùng vòng theo cặp ID, vị trí, tập con, cấu trúc trang và tập kiểu JSON, không thêm một fixture riêng cho mỗi biến thể. Không sửa sản phẩm, không xóa tên/assertion ca base. Không có lớp phức tạp bị bỏ lại cho executor ngoài giới hạn payload dưới đây.

## Ngoài phạm vi và chưa đo

Không sửa packet_loop.py, chứng minh nguồn gốc JSON/API, hoặc quy hạng cho ca ngoài họ kg. Windows/PowerShell chưa đo; skip được giữ riêng. Không push/PR/comment/CI từ xa, không tạo quyền approve/land.

Theo phân công, các hướng cần payload mới chỉ mô tả, không chạy và không tính thành finding: traceback thật được escape sâu hơn ba lớp hoặc codec khác; fixture mang banner đồng thời CLI trả rc ngoài bộ; đường dẫn thoát cây, byte thô bất thường hoặc symlink. Kỳ vọng không cấp GIẾT cho crash và không gán tín dụng giả cho lỗi assertion đúng. Không suy các fixture có sẵn thành chứng minh mọi codec/độ sâu.

Bảy lớp P2 còn mở nên changes_requested theo Q6, dù gate hiện tại xanh. Không tự mở vòng vá hoặc lời gọi reviewer tiếp theo.
