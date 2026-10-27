Reviewed commit: ba96fc6cfb2f0b21f4814fd6bf5e7431b727029b
Verdict: changes_requested — P0=0 P1=0 P2=3 P3=0

ĐÃ HOÀN TẤT. Gate xanh; kiểm toán độc lập còn **ba lớp P2**, gồm **32 đột biến sống trên 164/164 ca kg**. Chưa đạt ngưỡng Q6. Các finding là thiếu độ phủ của test, không phải lỗi trên mã sản phẩm nguyên vẹn.

## Định danh, vai trò và phạm vi

- KHO `/home/user/rv822`; detached HEAD đúng SHA trên, không shallow, working tree sạch đầu/cuối.
- Tree: `360df5be72d82e94108e4217a42b0cf94a42ca99`; base `f712205aa39e0b54d04a5bd8145fa69a84601fed`.
- Đặc tả trên base đã đọc trọn M1–M6, K01–K37, D1–D6, A1–A12 và điều kiện dừng. SHA256 khớp `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07`.
- Lease r1/g1 đã đọc từ ref chỉ định. Diff đúng một tệp `.claude/dev/packet_loop_test.py`, +450/−19; `packet_loop.py` không đổi.
- Reviewer Codex/OpenAI, shell cục bộ, offline; không dùng context executor, không gọi reviewer phụ. Lời gọi được giao 4/8. Phép đo code không tự chứng minh model build/session identity.
- Không sửa KHO, ref hoặc branch executor; không push/PR/đăng Issue. Scratch và bản chạy ở `/tmp/wp822-rv4/`; bằng chứng ở [evidence](evidence/). Python 3.13.16/Linux. [Định danh](evidence/repository-identity.json), [kiểm tra cuối](evidence/repository-final.json).

## Bảng lớp đã chốt sau quét rộng

Các neo thuộc `.claude/dev/packet_loop_test.py` trên SHA đang review. Tất cả mutant được báo SỐNG dưới đây đã chạy đủ 164 tên ca kg, mỗi tên đều có màu trong JSON.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `so-khop-tuyet-doi-chua-du` | P2 | `packet_loop_test.py:5961`, `:5963`, `:5971`, `:5973`, `:5978`, `:5979`, `:5980` | **28 mutant sống 164/164**: status 5, conclusion 5, danh tính name 4, danh tính head 6, so tên cảnh báo 5, so head trực tiếp 2, so name trực tiếp 1. 23 fixture rc12→0; 5 fixture cảnh báo giữ rc0 nhưng stderr đổi | Khóa phép bằng tại mọi vị trí bằng fixture chỉ sai một trường; bảng nối K16/K18/K26/K27/K32/K33/K34. HINT có cả các chiều đã được ca cũ khóa để giữ toàn lớp |
| `bao-loi-chi-do-mot-ten` | P2 | `packet_loop_test.py:5851`, `:5852`, `:5985` | Chỉ in cuối hoặc chỉ in đầu+cuối: **2 mutant sống 164/164**. Hai/ba tên đỏ giữ rc12, mất lý do đầu/giữa | Đòi đủ từng dòng, tổng đúng; fixture ba tên và mutant chọn đầu/chọn cuối/bỏ giữa. HINT |
| `canh-bao-chi-do-mot-id` | P2 | `packet_loop_test.py:5573`, `:5971` | Giữ ID đầu+cuối hoặc tên cảnh báo đầu+cuối: **2 mutant sống 164/164**. Ba ID/ba tên giữ rc0, mất phần tử giữa | Fixture ba ID phân biệt và ba tên bắt buộc, so toàn bộ danh sách/dòng stderr; hai mutant riêng. HINT |

### Mọi biểu hiện đã đo của lớp so khớp

- `status_{case,prefix,suffix,strip}` và `conclusion_{case,prefix,suffix,strip}`: tám phép nới điều kiện `completed`/`success`, tất cả SỐNG; mỗi fixture chỉ sai giá trị trường ấy, còn type/count/suite/head đúng.
- `identity_name_{case,strip,last}`: ba mutant SỐNG; khóa danh tính nhận nhầm tên chỉ khác hoa/thường, space hai đầu hoặc tiền tố. `identity_name_first` đã bị ca cũ giết (163/164 xanh), không được báo là mutant sống.
- `identity_head_sha_{case,strip,first,last}` và `identity_head_short`: năm mutant SỐNG; fixture dùng cùng id với head mâu thuẫn, thêm id mới hơn hợp lệ để phép cấp màu không chặn hộ.
- `warning_name_{case,suffix,strip_run,strip_arg}`: bốn mutant SỐNG; thay đúng phép so tên ở cảnh báo, giữ lọc tên quyết màu. `warning_name_prefix` đã bị ca cũ giết (163/164 xanh), không phải finding mới.

Các `audit-<tên>.json` giữ cặp tìm/thay, toàn bộ 164 tên/màu và fixture nền–mutant; `fast-r4.json` giữ thêm probe CLI trực tiếp. Tính sai này nằm ở độ phủ của test: sản phẩm nguyên vẹn từ chối/hiển thị đúng trên mọi fixture phân biệt đã chạy. Không gán lỗi sản phẩm cho kết quả dưới mutant.

- Quét cuối: `match_head_strip`, `match_head_nfkc`, `status_nfkc`, `conclusion_nfkc`, `match_name_nfc`, `identity_name_nfc`, `identity_head_nfkc`, `warning_name_nfc` đều SỐNG 164/164. Bảy fixture rc12→0, một fixture cảnh báo giữ rc0 nhưng stderr đổi. NFC dùng hai tên có cùng cách nhìn nhưng khác chuỗi codepoint; NFKC dùng chữ fullwidth thay chữ ASCII. Head/khóa danh tính vẫn cần so nguyên văn. `audit-unicode-summary.jsonl` và từng JSON giữ tên/màu/cặp tìm-thay/CLI thô.

### Mọi biểu hiện đã đo của hai lớp đầu ra bị cắt

`audit-red_last_name_only.json` và `audit-red_ends_only.json`: lý do tên đầu hoặc tên giữa biến mất; tổng vẫn đúng nên assertion tổng không phát hiện. HINT giữ fixture hai tên để khóa chiều ngược và thêm ba tên để khóa phần tử giữa.

`audit-warning_id_ends_only.json` và `audit-warning_name_ends_only.json`: số id `len(khac)` vẫn đúng, nhưng danh sách id thiếu phần tử giữa; hoặc thiếu cả dòng cảnh báo tên giữa. Fixture tên gần giống của lớp so khớp là phép đo riêng, không gộp nhầm với thiếu phần tử. HINT kiểm từng dòng/từng id và giữ đối chứng tên không bắt buộc, suite neo, bản ghi trùng có sẵn.

Không có finding `kiem-ke-bo-sot`: ba lớp đều là biến thể của K đã có, không tăng H2 từ 8 lên 9. Không cần đổi mã sản phẩm để đóng các finding.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nhãn đánh giá toàn lớp sau quét lại, không chỉ việc một phản chứng cũ đã đổi màu. Lượt 2 dở dang được giữ nguyên tính chất đó, không tự biến thành vòng canon đã chốt.

| lượt | lớp | nhãn | bằng chứng mới trên head này |
|---|---|---|---|
| 1 | `tin-dung-giet-sai` | **đã vá thật** | M6 có sẵn chạy xanh; rc ngoài bộ, hai kênh, các vỏ, cause/context/from None/BoQua/group được loại đúng; từng chốt tự kiểm có răng |
| 1 | `trung-id-chi-do-mot-chieu` | **đã vá thật** | Chọn bản đầu/chọn bản cuối bị hai chiều bản đỏ/xanh giết; baseline mọi ca giữ màu |
| 1 | `ten-trang-chi-khoa-space` | **đã vá thật** | TAB/NBSP khóa strip-space; space khóa bỏ strip; tên hợp lệ giữ xanh |
| 1 | `fixture-vi-pham-nhieu-chot` | **đã vá thật** | Bốn fixture sửa riêng trường đích đều rc0; ca conclusion cũ/D6 rc0; blacklist giữ kiểm status |
| 2 | `tin-dung-giet-sai` | **đã vá thật** | Các vỏ JSON/repr/log và escape có sẵn không được nhận GIẾT giả; marker/classifier đúng module nạp lại |
| 2 | `sha-chi-do-ngan-va-hoa` | **đã vá thật** | Các mutant nhận phi-hex, 39, 41 ký tự bị ca riêng giết; giữ đối chứng 7 ký tự và chữ hoa |
| 2 | `id-lon-nhat-chua-do-so-hoc` | **đã vá thật** | Max theo chuỗi bị cả hai chiều id9/id10 giết |
| 2 | `canh-bao-chi-do-mot-id` | **vá hờ** | Ca 2 ID/2 tên đã có răng với các mutant cũ, nhưng cắt phần tử giữa khi có 3 ID/3 tên vẫn sống 164/164 |
| 2 | `chi-kiem-kieu-trang-dau` | **đã vá thật** | Các mutant r2/r3 về schema, suite, bool run.id, bool suite.id, tc âm trang sau đều bị ca đích giết |
| 3 | `chi-kiem-kieu-trang-dau` | **đã vá thật** | Ba biến thể còn sót đã có fixture đơn chốt và mutant nối trực tiếp trong bảng |
| 3 | `khoa-trung-chua-phu-moi-tang` | **đã vá thật** | Hook thu hẹp tại suite.id hoặc extra root/object/array đều bị ca riêng giết |
| 3 | `so-khop-tuyet-doi-chua-du` | **vá hờ** | Name/head tại phép cấp màu đã vá; còn 28 mutant sống tại status/conclusion/khóa danh tính/tên cảnh báo/strip head/chuẩn hóa Unicode |
| 3 | `bao-loi-chi-do-mot-ten` | **vá hờ** | Chỉ in đầu bị giết nhưng chỉ in cuối hoặc bỏ giữa vẫn sống 164/164 |
| 3 | `tin-dung-giet-sai` | **đã vá thật** | Bỏ riêng cause làm ca cause-only ngoài except đỏ; bỏ riêng đối số làm ca banner chỉ đối số đỏ; bỏ context cũng đỏ |

Không gán nhãn “vá sinh lỗi mới”: không có phản chứng cho hồi quy phát sinh từ bản vá; A7 xác nhận toàn bộ ca base còn tên và giữ màu. Các khoảng trống mới trong bảng lớp là phần còn sót khi quét rộng cùng lớp.

## Kiểm kê độc lập và ca đích đúng chốt

Đã quét mọi điều kiện/so sánh/except trong `_doc_check_runs` và `cmd_kiem_gate`, đối chiếu **41 K, 103 mutant phân biệt**. K38–K40 bổ sung đúng hành vi hai hàm; K41 là help argparse ngoài hai hàm, giữ để kiểm M5(a). Không có dòng `tuong_duong`, nên không có lập luận tương đương nào được miễn phép thử. Không tìm thấy thành phần hoàn toàn vắng bảng và sống khi gỡ; không kích hoạt H2=9.

[Bảng độc lập](evidence/inventory-independent.md), [AST điều kiện](evidence/independent-predicates.json), [bảng/runtime mutant](evidence/inventory-runtime.json). Các finding là biến thể của K đã có; không nhầm sự hiện diện của K trong bảng với độ phủ đủ các biến thể.

D1–D6 khớp đúng một chỗ, đủ cặp nguyên văn. Mọi ca đích riêng CLI rc12→0, GIẾT thật và ba đối chứng khác họ xanh. D6 trên `kg_m2_thieu_conclusion` tên cũ và ca thay đều rc0, không THỪA id. [D1–D6](evidence/D1-D6.json). Bốn fixture từng sai nhiều chốt: sửa riêng trường đích đều rc0, [isolation](evidence/fixture-isolation.json).

M5(a)/(b)/(c) có răng riêng: thêm kg ngoài bảng chỉ làm (a) đỏ; thêm tên không tồn tại chỉ làm (b) đỏ; đổi tên K27 giữ nguyên toàn bộ ánh xạ chỉ làm (c) đỏ. Ba mutant t822 tương ứng cũng GIẾT, đối chứng xanh.

M6: chạy nguyên ca có sẵn (8 vỏ × 2 kênh, Unicode escape, rc ngoài bộ, help, cause/context/from None/BoQua/ExceptionGroup, banner trong fixture/đối số). Chín mutant chốt và mutant coi mọi ca đỏ là GIẾT đều làm tự kiểm đỏ. Bốn mutant độc lập bỏ cause/context/classifier except thường/chỉ đọc stdout cũng làm đỏ. Module nhắm test được nạp riêng: `_TinDungGia` khác danh tính và classifier dùng đúng module. [Tự kiểm và từng lỗi kỳ vọng](evidence/selfcheck-results.json). Không dùng một CLI sập làm bằng chứng giết thật.

Kiểm toán độc lập thêm **43 mutant × 164 ca kg = 7.052 màu**: 32 SỐNG thuộc ba lớp ở trên; 11 GIẾT thật, không TÍN_DỤNG_GIẢ. [Tổng kiểm toán](evidence/audit-all-summary.json), [danh sách sống](evidence/audit-survivors.md). Mỗi JSON ghi cặp tìm/thay, đủ tên ca/màu và CLI fixture phân biệt.

## Gate, A11 và nghiệm thu

Lệnh đã chạy trên bản sao nguyên vẹn:

```text
cp -a /home/user/rv822 /tmp/wp822-rv4/gate
PYTHONDONTWRITEBYTECODE=1 python3 -B /tmp/wp822-rv4/gate/.claude/dev/packet_loop_test.py
```

**rc0 · nền 614/614 đạt · BỎ QUA 1 · TỔNG: ĐẠT**. Có **357 mutant khai báo**, **356 GIẾT**, **1 BỎ QUA** (`luong_canonical_chay_that_dao_os_name`, Windows, ngoài họ kg); không khai đã giết tất cả 357. [Log đầy đủ](evidence/full-suite.log), [tập mutant/kết quả](evidence/full-suite-summary.json), [rc tiến trình](evidence/tool-run-results.json).

A11 hoàn tất **103/103 mutant × 166 tên ca = 17,098 dòng màu**; nền có **165 ca thực gọi CLI**, một ca M5 không gọi CLI. **20,875 lượt CLI dưới mutant**, cộng **206** lượt nền. Thiếu mutant/tên ca 0; lỗi mỏ neo/probe 0; ca đích khai báo nhận tín dụng crash 0. Ca ngoài đích đổi màu được liệt kê đủ trong [CSV A11](evidence/A11-colors.csv) và từng `matrix-<mutant>.json` (args, rc, stdout, stderr). [Tổng A11](evidence/A11-summary.json), [rc probe](evidence/matrix-tool-result.json).

Hai ca ngoài họ `stdout_cp1252`/`stdout_cp1258` chạy đầy đủ ở nền. Dưới mỗi mutant, replay đúng lệnh kiem-gate, fixture và encoding đã ghi của mỗi ca, giữ assertion rc0/stdout khác rỗng; không lặp các bước không liên quan. Tìm mọi cửa gọi xác nhận ngoài họ kg chỉ hai ca này. M6 được cô lập theo process vì tự kiểm thay CASES.

| tiêu chí | kết quả độc lập |
|---|---|
| A1–A3 | Đủ D1–D6 nguyên văn, GIẾT và đối chứng xanh; mọi đích rc12→0; ca conclusion cũ/ca thay đều rc0 |
| A4 | Ba vế M5 có răng độc lập |
| A5 | Không dòng tương đương; không K hoàn toàn vắng bảng. Độ phủ theo lớp còn ba finding P2 |
| A6 | Full gate rc0, nền 614/614, TỔNG ĐẠT; ghi riêng một mutant Windows bỏ qua |
| A7 | Base 554 xanh + 1 skip, head 614 xanh + 1 skip; đủ 555 tên base trong 615 tên head, thiếu/trùng/đổi màu 0 |
| A8 | Base/head doctrine-scan và adr-song đều rc0, có đầu ra dương |
| A9 | Head đúng một tệp +450/−19, không đổi sản phẩm |
| A10 | Base/head cùng hai F541, F401=F821=0, delta F=0; Ruff rc1 là lỗi có sẵn |
| A11 | Đủ 103 mutant và 166 tên ca; màu ngoài đích được ghi, không lỗi probe |
| A12 | Cặp crash/dự phòng xanh; gỡ loại crash và từng chốt đã đo làm tự kiểm đỏ |

[A7 từng tên/màu](evidence/A7-colors.csv), [nghiệm thu](evidence/acceptance-summary.json), [base/head gates và Ruff](evidence/baseline-gates.json). Các phần M5/M6 đạt trong phạm vi đã đo không xóa ba khoảng trống M1/M3 nêu trên.

## HINT.patch

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

[HINT.patch](HINT.patch) chỉ chạm `.claude/dev/packet_loop_test.py`. Đã apply thật vào bản sao pristine exact head, so bytes khớp bản dùng probe, diff-check sạch. [Biên nhận áp](evidence/hint-apply.json).

Tổng so base **+543/−19**, diff so head **+103/−10**: vượt trần ban đầu 93 dòng theo quyền vượt nếu cần đã nêu trong chỉ thị. A9 của head hiện tại vẫn +450/−19; không dùng số đó để khai cho HINT. Các dòng thêm khóa cả ba lớp; không xóa tên/assertion ca base hoặc đổi mã sản phẩm.

Trên HINT cuối: **190/190 ca xanh** (189 kg + chốt mỏ neo), **34/34 mutant mới GIẾT đúng ca đích**, ba đối chứng mỗi mutant xanh. Ruff cuối vẫn hai F541. [Kết quả HINT cuối](evidence/hint-results-last.json), [Ruff](evidence/ruff-hint-final.json). Các mutant chọn đầu/chọn cuối/bỏ giữa và đếm hằng cũng đã đo. Chưa chạy full suite trên HINT; gate đầy đủ ở trên chỉ thuộc head đang review.

HINT giữ hai chiều id trùng, các ca whitespace cũ, các fixture hai tên/hai id; thêm biến thể so chuỗi theo từng vị trí, ba tên đỏ/ba tên cảnh báo/ba id cảnh báo. Mọi fixture mới chỉ sai chốt đích; sửa test không cần sửa sản phẩm. Nguy cơ cần canh khi executor tái dẫn xuất: không để chốt count/danh tính khác chặn hộ; giữ phân loại theo module nạp lại; đo lại gate sau mọi thay đổi.

## Ngoài phạm vi, giới hạn và sự cố thao tác

Không sửa `packet_loop.py`, chứng minh nguồn gốc JSON/API, hoặc gán hạng cho ca ngoài họ kg. Ca Windows/PowerShell và mutant tương ứng bỏ qua trên Linux; không khai đã đo Windows. Không có push, PR, CI từ xa hoặc authority land sinh từ review này.

Đã tuân phân công M6: chỉ chạy fixture crash có sẵn và đột biến chốt bộ đo. Hướng cần payload mới chỉ mô tả: banner traceback thật F02 escape sâu hơn ba lớp, codec khác, hoặc fixture bị cấm banner đồng thời CLI trả rc ngoài bộ. Kỳ vọng không cấp GIẾT cho CLI sập. Những hướng này chưa chạy, không tính thành finding đã chứng minh; không suy kết quả fixture có sẵn thành chứng minh mọi codec/độ sâu. Không tự soạn mã in/giả/bọc traceback, payload sập, đường thoát cây, byte bất thường hoặc symlink.

Sai sót thao tác reviewer: gọi trực tiếp script isolation cũ đã ghi đè `/tmp/wp822-rv3/evidence/fixture-isolation.json`. Đã khôi phục **nội dung** bằng JSON từ log gốc lượt 3, đúng serialization script cũ; không thay đổi VERDICT/HINT cũ (checksum còn khớp). [Biên nhận khôi phục](evidence/incident-recovery.json). KHO không bị ghi. Các phép đo hiện tại dùng script và artifact riêng trong thư mục ra. [Nhật ký tăng dần](evidence/VERDICT.progress.md) lưu các số trung gian; số trong báo cáo cuối này là số chốt.

Ba lớp P2 còn mở nên **changes_requested** theo Q6. Không có K mới bị bỏ sót để tăng H2=9; không cần sửa sản phẩm. Ngân sách được giao là lời gọi 4/8; không gọi thêm reviewer hoặc tự mở vòng vá/đăng Issue.
