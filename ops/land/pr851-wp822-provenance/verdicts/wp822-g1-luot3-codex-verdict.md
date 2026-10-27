Reviewed commit: ee853d32e2e55592a1d7caf4c5f16714cd25dad2
Verdict: changes_requested — P0=0 P1=0 P2=5 P3=0

Review đã hoàn tất. Gate xanh, nhưng còn **5 lớp P2 về độ phủ và răng của test**. Không sửa KHO; không push, tạo PR hoặc gọi mạng. Reviewer: Codex/OpenAI, dùng công cụ shell cục bộ; không tái sử dụng context executor. Model build/effort và authority nhận biên nhận không được chứng minh độc lập bởi phép đo code này.

## Định danh và phạm vi

- KHO `/home/user/rv822`, detached HEAD đúng SHA trên; kho không shallow, working tree sạch đầu/cuối lượt.
- Tree: `37f9c4a2f591df0df532cacac0672b8348cdd931`.
- Base: `f712205aa39e0b54d04a5bd8145fa69a84601fed`.
- Đặc tả trên base đã đọc trọn M1–M6, K01–K37, D1–D6, A1–A12, điều kiện dừng; SHA-256 đúng `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07`.
- Đã đọc lease `origin/ops/wp822-spec:ops/leases/wp822-r1-g1-claude.yaml`, chỉ cho tệp test. Diff thực chỉ `.claude/dev/packet_loop_test.py`, **+428/-19**; sản phẩm không đổi.
- Đã đọc verdict/evidence hai lượt trước và diff từ `08aa096`, `cffd44e`. Đây là lời gọi được giao **3/8**; không gọi reviewer phụ.
- Bản chạy/đột biến nằm trong `/tmp`; kết quả và script tái lập ở [evidence](evidence/). Định danh/môi trường: [repository-identity.json](evidence/repository-identity.json).

## Bảng lớp

Các neo dưới đây thuộc `.claude/dev/packet_loop_test.py` trên exact head. Mỗi mutant logic được chạy qua **đủ 147 ca kg**; không suy kết quả từ grep hoặc lời khai executor.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `chi-kiem-kieu-trang-dau` | P2 | `packet_loop_test.py:5816`, `:5823`, `:5906` | Ba mutant cho phép bool run.id / bool suite.id ở trang sau, hoặc chỉ kiểm tc âm ở trang đầu, đều sống **147/147**. Hai fixture bool rc12→0; tc âm giữ rc12 nhưng đổi lý do. | Fixture và mutant riêng cho từng vế; nối K07/K14/K15. HINT có đủ ba biến thể. |
| `khoa-trung-chua-phu-moi-tang` | P2 | `packet_loop_test.py:5464`, `:5470`, `:5925` | Bỏ kiểm trùng tại object suite chỉ có id, hoặc chỉ kiểm các khóa schema đã biết: cả hai sống **147/147**. Suite.id trùng và extra trùng tại root/object lồng/object trong array đều rc12→0. | Bốn fixture chỉ sai khóa trùng; hai mutant thu hẹp hook, nối K02. HINT có đủ bốn fixture. |
| `so-khop-tuyet-doi-chua-du` | P2 | `packet_loop_test.py:5450`, `:5711`, `:5957` | **Tám** mutant sống **147/147**: head theo prefix/suffix/casefold/7 ký tự; tên theo suffix/casefold/strip run/strip đối số tại phép so. Bảy phản chứng rc12→0; strip đối số làm đầu vào đúng rc0→12. | Đo các biên của phép bằng tuyệt đối K27/K34, tách khỏi kiểm dạng đối số K21. HINT có đủ tám biến thể. |
| `bao-loi-chi-do-mot-ten` | P2 | `packet_loop_test.py:5809`, `:5890`, `:5965` | Chỉ in `do[:1]`, hoặc báo số tên đỏ bằng hằng 1: cả hai sống **147/147**. Hai tên đỏ giữ rc12 nhưng mất lý do tên thứ hai hoặc sai `1/2` thay `2/2`. | Đòi dòng lý do thứ hai cùng tổng `2/2`; hai mutant K39/K40. HINT có cả hai. |
| `tin-dung-giet-sai` | P2 | `packet_loop_test.py:5352`, `:5371`, `:6041`, `:6067` | Bỏ riêng duyệt cause hoặc bỏ riêng quét đối số đều để tự kiểm M6 **SONG**, ba đối chứng xanh. Context chặn hộ cause; tệp chặn hộ đối số. | Tách cause-only cho AssertionError/BoQua và banner chỉ ở đối số. HINT đóng phần đối số bằng fixture có sẵn; phần cause-only phải do executor viết theo lệnh cấm của prompt. |

### Bằng chứng và giới hạn từng lớp

**Trang sau.** [audit-later_page_run_bool.json](evidence/audit-later_page_run_bool.json), [audit-later_page_suite_bool.json](evidence/audit-later_page_suite_bool.json), [audit-later_page_negative_count.json](evidence/audit-later_page_negative_count.json) giữ cặp tìm/thay, tên/màu đủ 147 ca và stdout/stderr của cặp nền–mutant. Run.id bool được đặt cạnh id khác để không bị trùng danh tính chặn hộ. Tc âm đổi lý do từ `trang 1: total_count không phải số nguyên ≥ 0` sang các trang khai count khác nhau; đây không phải tương đương hành vi theo M1. Lớp lượt 2 còn sót ba biểu hiện này.

**JSON trùng.** [audit-nested_suite_duplicates_ignored.json](evidence/audit-nested_suite_duplicates_ignored.json), [audit-extra_key_duplicates_ignored.json](evidence/audit-extra_key_duplicates_ignored.json). Các fixture còn lại đúng count, kiểu, suite, head và trạng thái. Hook hiện tại đúng; các ca test chưa khóa yêu cầu “mọi khóa, mọi tầng” của K02. Không gọi đó là lỗi sản phẩm.

**So khớp.** Các tệp `audit-head_prefix`, `head_suffix`, `head_casefold`, `head_first7`, `name_suffix`, `name_casefold`, `name_strip_run`, `name_strip_arg` trong evidence giữ tám phản chứng. Tên có khoảng trắng ở hai đầu vẫn là tên hợp lệ và phải được giữ nguyên. Mutant chuẩn hóa đối số *trước* kiểm xuống dòng đã bị ca cũ giết; mutant sống chỉ strip tại phép so, sau kiểm đối số. Mutant dùng phép chứa chuỗi bị ca cũ giết, không bị báo như khoảng trống mới. K34 so head khác K21 kiểm dạng `--head`.

**Nhiều tên đỏ.** [audit-red_first_name_only.json](evidence/audit-red_first_name_only.json), [audit-red_count_constant.json](evidence/audit-red_count_constant.json) giữ cả hai dòng lý do và tổng đúng của nền. Đây là thiếu phủ lý do/đầu ra K39/K40; D2/K35 về một tên đỏ cạnh một tên xanh đã đạt.

**M6.** [selfcheck-results.json](evidence/selfcheck-results.json), mục `own_no_cause`: chỉ đổi `cho += [ex.__cause__, ex.__context__]` thành `cho += [ex.__context__]` vẫn SONG. Nhánh tên “cause” ném ngay trong except, nên ngoại lệ ấy đồng thời nằm trong context. [M6-no-arg-scan.json](evidence/M6-no-arg-scan.json): đổi dòng dựng `vao` từ đối số thành `vao = []` vẫn SONG vì fixture đồng thời mang banner trong JSON. Đây là **hai chốt tự kiểm chưa có răng**, không khẳng định classifier nguyên vẹn của head đang phân loại sai hai đầu vào ấy.

Đã chạy nguyên ca M6 có sẵn: traceback thật 6 vỏ × 2 kênh, banner không frame, rc ngoài bộ, help, cause/context/from None, BoQua, ExceptionGroup, banner thô/giải mã JSON. Tám mutant M6 khai báo đều bị giết. Mutant riêng bỏ context, bỏ classifier ở except thường, hoặc chỉ đọc stdout cũng làm tự kiểm đỏ. Module test được nạp riêng và phân loại bằng đúng lớp của module đó; danh tính `_TinDungGia` khác nhau được ghi trong evidence.

Theo lệnh cấm rõ trong prompt, reviewer **không tự viết mã in/giả/bọc traceback hoặc payload gây sập**. Executor cần tái dùng crash F02 có sẵn, tạo ngoại lệ ngoài except sao cho chỉ cause còn giữ tín hiệu, context không giữ; đo cả AssertionError và BoQua. Kỳ vọng nền TIN_DUNG_GIA, bỏ duyệt cause phải làm tự kiểm đỏ. Hướng bổ sung chưa chạy vì cùng giới hạn: giữ traceback F02 nhưng trình bày các chữ của banner bằng escape Unicode và rc12; kiểm rằng không được cấp GIẾT chỉ vì mất bytes banner literal. Không dùng hướng chưa đo làm finding riêng.

## Kiểm kê độc lập và phép đo bắt buộc

[Bảng kiểm kê độc lập](evidence/inventory-independent.md) đối chiếu từng điều kiện của `_doc_check_runs` và `cmd_kiem_gate` với bảng test: **41 K, 88 mutant phân biệt**. K41 là help argparse, giữ vì M5(a), ngoài hai hàm. Không có dòng `tuong_duong`. Không tìm thấy thành phần hoàn toàn vắng bảng và sống khi gỡ: **không có finding `kiem-ke-bo-sot`, không kích hoạt H2=9**. Các finding trên là biến thể của K đã có hoặc tự kiểm M6.

A11: chạy lại nền rồi **88/88 mutant × 149 tên ca = 13.112 dòng màu**, gồm **148 ca thực gọi CLI** và một ca tự kiểm bảng; **15.731 lượt CLI dưới mutant**. Không thiếu mutant/tên ca, lỗi mỏ neo hoặc tín dụng crash ở ca đích được khai báo. Ca ngoài đích đổi màu được liệt kê đầy đủ. [A11-summary.json](evidence/A11-summary.json), [A11-colors.csv](evidence/A11-colors.csv), các `matrix-*.json` giữ lệnh/rc/stdout/stderr.

Hai ca codepage được chạy đầy đủ ở nền; dưới mỗi mutant, replay đúng lệnh kiem-gate, fixture và encoding của từng ca, giữ assertion rc0 và stdout khác rỗng. Không chạy lại những bước không liên quan trong kịch bản codepage. Tìm tĩnh mọi cửa gọi xác nhận ngoài họ kg chỉ có hai ca này; report kiểm không mất assertion khi replay. M6 được cô lập bằng process vì tự kiểm thay CASES.

D1–D6 có đủ cặp tìm/thay nguyên văn, khớp một chỗ. Tất cả tám ca đích riêng đều rc12→0 và GIẾT; ba đối chứng khác họ xanh. D6 trên cả tên cũ `kg_m2_thieu_conclusion` và ca thay đều rc0, không THỪA id. [D1-D6.json](evidence/D1-D6.json). Bốn fixture từng sai nhiều chốt, sau khi chỉ sửa trường đích, đều rc0: [fixture-isolation.json](evidence/fixture-isolation.json).

M5(a)/(b)/(c) có răng riêng. Hai thay đổi độc lập thêm mutant ngoài bảng / tên không tồn tại đều làm đúng vế đỏ. Riêng (c), đổi K09 thành K09_copy nhưng giữ nguyên toàn bộ ánh xạ: (a), (b) vẫn đúng, chỉ (c) đỏ: [M5-c-only.json](evidence/M5-c-only.json). Ba mutant t822 tương ứng cũng bị giết và đối chứng xanh.

## Gate và nghiệm thu

Lệnh full gate: `cp -a /home/user/rv822 /tmp/wp822-rv3-head` rồi `python3 -B /tmp/wp822-rv3-head/.claude/dev/packet_loop_test.py`.

**rc0 · nền 597/597 đạt · BỎ QUA 1 · TỔNG: ĐẠT**. Trong **340 mutant**, **339 GIẾT**, **1 BỎ QUA** (`luong_canonical_chay_that_dao_os_name`, Windows, ngoài họ kg); không thiếu tên mutant. Không khai 340/340 bị giết. [full-suite.log](evidence/full-suite.log), [full-suite-summary.json](evidence/full-suite-summary.json), [final-run-results.json](evidence/final-run-results.json).

| tiêu chí | kết quả |
|---|---|
| A1–A3 | D1–D6 đủ nguyên văn, GIẾT/đối chứng xanh, rc12→0; D6 không bị count chặn hộ |
| A4 | ba vế M5 được phá độc lập, tự kiểm đều đỏ đúng vế |
| A5 | không có tuong_duong; kiểm kê không có K hoàn toàn vắng bảng; độ phủ còn các lớp ở trên |
| A6 | full gate rc0, nền 597/597, TỔNG ĐẠT; ghi riêng một mutant Windows bỏ qua |
| A7 | base **554/554 + 1 skip** đo lại cùng container; đủ 555 tên base trong 598 tên head, không trùng tên, không đổi màu; cùng một skip Windows |
| A8 | doctrine-scan và adr-song trên base/head đều rc0, có đầu ra dương |
| A9 | đúng một tệp +428/-19, không đổi packet_loop.py |
| A10 | Ruff base/head cùng rc1 vì 2 F541; F821=F401=0; delta F=0 |
| A11 | 88/88 mutant, 149 tên ca, 13.112 màu, 15.731 CLI; lỗi probe 0 |
| A12 | cặp crash/dự phòng và bỏ toàn classifier đã có răng; quét từng chốt còn hai biểu hiện M6 nêu trên |

Bằng chứng nền/tên/màu: [baseline-gates.json](evidence/baseline-gates.json), [A7-colors.csv](evidence/A7-colors.csv), [acceptance-summary.json](evidence/acceptance-summary.json). Ruff dùng `--no-cache --select F --output-format json`; không lấy rc1 có sẵn làm regression. Mọi exit code công cụ đã thu trong `run-results.json` và `final-run-results.json`.

Kiểm toán độc lập thêm **26 mutant logic**: 15 sống là bốn lớp logic ở bảng, 10 bị GIẾT thật; mutant `suite_first_run_only` làm hai ca sập và được phân loại **TIN_DUNG_GIA**, không được tính GIẾT. [audit-all-summary.json](evidence/audit-all-summary.json) giữ toàn bộ tên/màu và phản chứng. Không dùng lỗi probe hay crash làm bằng chứng giết.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| lượt | lớp | nhãn | tự đo trên head này |
|---|---|---|---|
| 1 | tin-dung-giet-sai | **vá hờ** | Các biểu hiện cũ đã vá thật; tự kiểm còn thiếu cause-only và đối số độc lập. |
| 1 | trung-id-chi-do-mot-chieu | **đã vá thật** | Cả status đỏ trước/conclusion đỏ trước đều giết chọn bản cuối; chiều đỏ sau giữ xanh nền. |
| 1 | ten-trang-chi-khoa-space | **đã vá thật** | Tab và nbsp giết strip-space; toàn space giết bỏ strip. |
| 1 | fixture-vi-pham-nhieu-chot | **đã vá thật** | Bốn ca sửa riêng trường đích đều rc0; D6 tên cũ/ca thay rc0; mutant blacklist giữ status, bỏ ca sai hai vế khỏi tín dụng K33. |
| 2 | tin-dung-giet-sai | **vá hờ** | Vỏ JSON/repr/log và các đường crash có sẵn đều được loại đúng; lớp tự kiểm còn hai biểu hiện trên. |
| 2 | sha-chi-do-ngan-va-hoa | **đã vá thật** | Phi-hex/39/41 đều bị ca mới giết, giữ ca 7 ký tự/chữ hoa; không đánh đồng với K34 so head. |
| 2 | id-lon-nhat-chua-do-so-hoc | **đã vá thật** | Max theo chuỗi bị cả hai chiều id9/id10 giết. |
| 2 | canh-bao-chi-do-mot-id | **đã vá thật** | Hằng count=1, chỉ id đầu, chỉ tên đầu đều bị giết; đếm phân biệt, bản lặp, stderr đúng. |
| 2 | chi-kiem-kieu-trang-dau | **vá hờ** | Các mutant r2 bị giết nhưng bool run.id, bool suite.id và tc âm trang sau vẫn sống 147/147. |

Không có lớp nào được gán “vá sinh lỗi mới” khi chưa có phản chứng cho nhãn ấy. Lớp mới: khóa trùng mọi tầng, so khớp tuyệt đối, báo lỗi nhiều tên. Lượt 2 dở dang không tự tạo một vòng canon đã chốt. Slug M6 có mặt cả ba lời gọi; dispatcher cần đối chiếu tín hiệu xem lại cách làm tại checkpoint theo protocol, không reset lịch sử hoặc tự cấp thêm lời gọi. Review này không ghi state/Issue/PR.

## HINT và phần executor cần làm

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

[HINT.patch](HINT.patch) áp được bằng git apply trên bản sao exact head; chỉ tệp test. Đã áp thật trong `/tmp/wp822-rv3-hint-git`, `git diff --check` sạch, nội dung trùng bản dùng probe. **Git đo so base +449/-19**, còn một dòng dưới trần 450. Diff gợi ý +28/-7: bỏ bảy dòng comment trùng ý, không xóa assertion hoặc tên ca base.

- 17 fixture mới, 15 mutant sản phẩm đóng đủ bốn lớp logic. Nền HINT ban đầu **164/164 kg xanh**; mỗi mutant mới GIẾT đúng ca đích, ba đối chứng xanh. Hai sửa đổi sau được đo delta riêng: ca strip đối số và M5, rồi M6/M5/chốt mỏ neo. Không khai đã chạy lại toàn bộ 164 ca trên HINT cuối.
- M6 thêm biến thể chỉ đối số chứa banner, tái dùng `_KG_1` và banner đã có; không thêm mã in/bọc traceback hoặc payload sập. Mutant `t822_m6_bo_doi_so` GIẾT đúng tự kiểm, ba đối chứng xanh.
- M5, M6 và chốt mọi mỏ neo khớp đúng một chỗ đều xanh trên HINT cuối; Ruff vẫn 2 F541, delta 0.
- **Cause-only chưa được HINT đóng**, đúng giới hạn cấm reviewer tự viết mã bọc traceback. Executor phải tự thêm fixture và mutant riêng như mô tả M6, đồng thời tạo thêm chỗ dưới trần. Không giả vờ diff hiện tại là bản vá hoàn tất mọi lớp.

Biên nhận: [hint-build.json](evidence/hint-build.json), [hint-results.json](evidence/hint-results.json), [hint-amendment.json](evidence/hint-amendment.json), [hint-M6-final.json](evidence/hint-M6-final.json), [ruff-hint-final.json](evidence/ruff-hint-final.json). HINT cuối vẫn cho mutant bỏ cause SONG, được ghi rõ trong biên nhận. Chưa chạy full suite trên HINT; gate đầy đủ ở trên là trên head đang review.

## Ngoài phạm vi và chưa đo

Không sửa sản phẩm, chứng minh nguồn gốc JSON/API, hoặc gán hạng cho ca ngoài họ kg. Hai ca codepage chỉ tham gia A11; ca Windows/PowerShell và mutant tương ứng không được đo trên Linux. Không tự soạn đường dẫn thoát cây, byte bất thường, symlink hoặc payload crash; các fixture có sẵn được chạy nguyên trạng trong bản sao. Hướng M6 cần nội dung mới được mô tả bằng lời ở trên, không báo thành đã chạy.

Không phát hiện điều kiện dừng H2=9, nhu cầu sửa sản phẩm hoặc hết ngân sách trong phạm vi review này. Năm lớp P2 còn mở nên không đạt ngưỡng approve P0=P1=P2=P3=0.
