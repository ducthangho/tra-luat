verdict: changes_requested
reviewed_sha: feb0b773bfed9456e6862c8154a9711d8f11912d
spec_sha256: ac1593e6cfe22896de372cb601cec6198350dec0bef5077dc80f6b8a44646966
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, effort: high, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
dem: {so_lop_mo_wp1466: 2, so_bieu_hien_mo: 2, P0: 0, P1: 0, P2: 1, P3: 1, so_lop_no_ke_nhiem: 5}
hoi_tu: {U: 0, F: 0, lop_moi: 1, lop_tai_mo: 0}

Hai lớp cần sửa ở đặc tả: lời khẳng định cổng xanh/cấm ca đỏ vượt quá phần phép đếm đã chuyển nợ; và hợp đồng nâng trần cho vùng 451–500 dòng thiếu khối khai theo ADR-0053. Không phát hiện P0/P1. Không có trở ngại môi trường ngăn kết luận nên dùng `changes_requested`, không giữ `blocked` của bản ghi tạm.

## Phạm vi, danh tính và nguồn chứng cứ

Đây là review **đặc tả r10**, không phải chứng nhận mã giao nộp r10 hay cho phép merge. Băm được kiểm đầu tiên sau khi đọc PROMPT và kiểm lại cuối lượt: khớp giá trị giao. Blob đặc tả tại commit bằng tệp trên đĩa. Cây nguồn HEAD `feb0b773bfed9456e6862c8154a9711d8f11912d`, tree `1388f60cd87604170979515c91d0b5d37307d8cd`.

Đã đọc chỉ thị cross-review, soan-spec, CLAUDE, AGENTS, protocol §7/§8/§8.3/§12, ADR-0060 M1–M12, ADR-0062/0063 và ADR-0053/0055. Đối chiếu verdict đặc tả r9, verdict mã exact-H lượt 1 và hồ sơ r10/handoff liên quan. Không dùng danh sách executor làm trần tìm lỗi.

Chấp nhận Q3/E3, E2 nâng 500, E5 duyệt băm và lời gọi **12/13** theo chỉ thị chủ kho trong PROMPT. Không yêu cầu duyệt lại, không xác minh các comment trên mạng. Metadata reviewer ở đầu là danh tính/phân công theo assignment; không có biên nhận launcher chứng minh model thực phục vụ, effort thực phục vụ hay session ID, nên không tự cấp mức assurance tương ứng.

Các phép đo thực hiện ngày 26-11-2026 UTC; audit chính 23:47:48Z, kiểm kết thúc 23:54:12Z. Python 3.13.18, Git 2.43.0. Tất cả đường dẫn hiện vật bên dưới tính từ thư mục `out/`; lệnh ghi `out/...` chạy từ thư mục chứa PROMPT.

Hai cây thử `h/` và `candidate/` lấy H `da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd`, tree `84018dbd9db5edcb1397e63d81911fc0320247aa`, từ ref cục bộ `cay-kho/refs/exec/h`. `candidate/` chỉ áp phần thay đổi r9→r10 của khối `adr` vào ADR-0068 đang có: **1 tệp, +5/-1**; giữ các giá trị đã điền của H, kể cả Trạng thái cũ. Đây đúng cây tổng hợp phục vụ phép thử được giao, **chưa phải ADR được điền đạt N1 cho r10**. Không sửa mã executor hay protocol trong cây này. Các fixture và đột biến riêng đều dưới `out/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt đặc tả r9 có bảng (i) rỗng: U=0, F=0, tỷ lệ **N/A**, không phải 100%. Không phát hiện tái mở các lớp đã đóng trong phạm vi mà r9 đã kết luận. Có 1 lớp mới tại lượt này (`thieu-khoi-nang-tran-kich-thuoc`), cộng 1 lớp P2 kế thừa review mã giữa hai lượt. Không tính lớp P2 ấy thành slug mới, không gộp vào slug lịch sử. Năm lớp nợ cũ không được tính là vá.

Nếu lấy riêng **review mã H lượt 1** làm nguồn đối chiếu, U=2, F=0 đối với sản phẩm H: chuyển phạm vi không phải vá; các ca G8 do reviewer dựng thử không phải bản vá đã giao nộp. Không trộn mẫu số ấy vào chuỗi hội tụ của review đặc tả.

Trong bảng dưới, “giữ” nghĩa là đối chiếu diff r10 không thấy tái mở; không có nghĩa đã chạy lại toàn bộ bộ ca/mutant mà r9 từng chạy.

| slug | nhãn | bằng chứng tự đo/đối chiếu |
|---|---|---|
| neo-sai-don-vi-khop | Giữ ĐÃ VÁ THẬT trong phạm vi cũ | 7/7 khóa được parser độc lập băm lại; khối `khoa` bằng byte r9. |
| neo-thieu-nghia-vu | Giữ ĐÃ VÁ THẬT | Sáu khối protocol bằng byte; đổi byte tại mỗi khóa đều rc 9. |
| cong-khong-do-bat-bien | Giữ ĐÃ VÁ THẬT | Bảng protocol bằng byte; r10 không đổi nợ thành lời khai cưỡng chế ngữ nghĩa. |
| thieu-truy-vet-yeu-cau | Giữ ĐÃ VÁ THẬT | Các khối luật/bảng truy vết của protocol bằng byte, không có thay đổi r10 tại đây. |
| kiem-chuoi-khong-doc-cau-truc | Giữ phần đã vá; CHƯA VÁ F05.b/c | Khóa và mã không đổi; mục nợ ngữ nghĩa còn nguyên. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ, giữ nợ | Không thêm reader kế nhiệm; phạm vi #1469 không đổi. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ, giữ nợ | Diff ADR không đổi chuyển tiếp/consumer #1470. |
| tieu-chi-dong-xoa-khong-do-hanh-vi | Giữ ĐÃ VÁ THẬT trong N8 | `do-pham-vi` và `so-dang-ky` bằng byte; không tuyên bố chạy lại toàn N8. |
| dem-khong-khai-tap-ca | Giữ ĐÃ VÁ THẬT | N6 vẫn định nghĩa T và cho thêm ca; không đổi tổng tối thiểu thành tổng cố định. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ, giữ nợ | Không thêm schema/provider/consumer v2; #1470. |
| tien-kiem-lease-chua-du | CHƯA VÁ, giữ nợ | Không phục hồi công cụ đã rút; giới hạn và #1484 còn nguyên. |
| doi-diem-goi-cong-chua-du-yeu-cau | Giữ ĐÃ VÁ THẬT | CLI thật vẫn gọi chốt, bảy ca đổi byte đều rc 9; mã không đổi. |
| doi-chung-khac-ho-chon-nham-doctrine | Giữ ĐÃ VÁ THẬT | R10 không đổi quy tắc; mutant G8 thử mới có 3 đối chứng khác họ còn sống. |
| ma-tran-dem-doi-loi-thay-doi-mau | Giữ ĐÃ VÁ THẬT | G8 được thử qua vòng `packet_loop_test_manh.chay` thật, giết 30 ca đích. |
| tach-packet-bo-dieu-kien-integration | Giữ ĐÃ VÁ THẬT phần quyết định | Không có thay đổi điều kiện integration trong diff; authority theo hồ sơ được cấp. |
| nghiem-thu-khoa-so-ca-trai-quyen-them | Giữ ĐÃ VÁ THẬT | N6/N7 vẫn bao gồm phần thêm; G8 có thể bổ sung 30 ca mà không sửa các tập tối thiểu. |
| khoa-khong-neo-vi-tri-va-duy-nhat | Giữ kết luận trong định nghĩa đơn vị | 7 bản sao thành đơn vị đều đỏ; không mở rộng kết luận cũ sang mọi chuỗi con. Không gộp slug P2 của review mã vào đây. |
| moc-dot-bien-tu-khop-trong-khai-bao | Giữ ĐÃ VÁ THẬT | N7/N8 và khối sổ đăng ký không đổi; điểm thay regex G8 khớp đúng 1 lần. |
| con-tro-trong-backtick-bi-cong-khac-doc | Giữ ĐÃ VÁ THẬT | 236 span của 7 khối không có finding; hai full scan strict đều không flags. |
| phep-dem-ban-sao-khong-phu-ca-tep | **CHƯA VÁ; VÁ SINH LỖI MỚI ở lời hứa thu hẹp** | Authority và nợ có; điều kiện (1) để chuyển toàn lớp chưa đạt vì dòng 470 vẫn cam kết kết quả toàn cổng. K01 kèm đoạn nối/biên chỉ dấu cách cho rc 9 bởi chốt ID. Giữ hạng P2. |
| ca-id-chi-do-mot-gia-tri | Yêu cầu sửa ở đặc tả **đủ và đo được**; mã H CHƯA VÁ | Sáu ca cũ vẫn đạt trên mutant chỉ nhận 99. Thử thêm 30 ID thật/biên: nền 36/36 đạt, mutant bị giết bởi 30 ca. Không ghi ĐÃ VÁ THẬT cho mã chưa giao nộp. Giữ hạng lịch sử P3. |

### Ba điều kiện chuyển P2 sang bảng (ii)

1. **Chưa đạt hoàn toàn.** Quét toàn văn đặc tả và khối ADR, không chỉ diff: mục 0, M3, Q3 trong ADR và N4 đã thu hẹp phép (3) về đơn vị cùng loại. Các chữ “bất kỳ” còn lại nói về byte bên trong khóa hoặc vị trí của một đơn vị cùng loại, không còn là lời hứa đếm mọi chuỗi con. Tuy nhiên §8.3 dòng 470 mới suy ra “cổng xanh với nó” và “Không ca nào ... được đòi đỏ” cho toàn bộ dạng được chuyển. Đó vẫn là hợp đồng về các biểu hiện đã chuyển và xung đột với chốt ID.
2. **Đạt:** `INV-KHOA-BAN-SAO-DINH-CHU` có trong mục *Nợ* của khối `adr`, dòng 332–334; 28 tên thực, 28 tên duy nhất.
3. **Đạt:** Issue #1469 được nêu trong mục nợ và bảng phạm vi; authority Q3/E3 được PROMPT xác nhận.

Không yêu cầu khôi phục phép đếm ngoài phạm vi. Cần sửa đúng lời hứa mới để ba điều kiện đồng thời đúng; hiện chưa chuyển trọn lớp ra khỏi bảng (i).

## BẢNG LỚP (i): lớp MỞ của wp1466

| slug lớp | biểu hiện | hạng | phương án chung | phép kiểm/giới hạn |
|---|---|---|---|---|
| phep-dem-ban-sao-khong-phu-ca-tep | §8.3 dòng 470 biến giới hạn của phép (3) thành lời hứa toàn cổng xanh và cấm ca đỏ, dù chốt ID độc lập phải đỏ | P2 | Chỉ nói phép (3) không đếm các bản ấy; giữ hiệu lực các chốt khác; không cấm ca đỏ vì ID/băm/địa chỉ | Hai biến thể K01 rc 9 vì ID; K02–K07 cùng kiểu rc 0. Không cần đổi mã phép (3). |
| thieu-khoi-nang-tran-kich-thuoc | N12/mục 10 nhận vùng 451–500 dòng nhưng không cung cấp khối nâng trần đủ trường theo ADR-0053 | P3 | Ghi khối dựa trên E2 đã duyệt, kèm căn cứ/số đo, và yêu cầu chép lease | Bốn trường đều 0 lần trong đặc tả. Cây tổng hợp hiện +447, chưa chứng minh đã vượt 450; lỗi nằm ở hợp đồng cho phần nới. |

Đếm **2 lớp, 2 biểu hiện hợp đồng**. Hai mệnh đề của dòng 470 là cùng một sai lầm suy từ phép đếm sang cả cổng; các fixture không bị đếm thành finding riêng. Không đổi hạng hay miễn P3.

## BẢNG LỚP (ii): nợ kế nhiệm có authority

| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì cho phần ấy |
|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c: khai báo ca theo cấu trúc, consumer kiểm mục Nợ | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | Mục 0/14/19 giữ loại trừ, diff không đưa consumer trở lại. |
| duong-dan-chua-khep-trong-goc | F06: ba reader kế nhiệm | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | Wp1466 tiếp tục chỉ nhận reader protocol; không thêm reader cổng/ca/ADR. |
| moc-chuyen-tiep-mau-thuan | F07: vị từ chuyển tiếp | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Không có yêu cầu mới nhận lại consumer chuyển tiếp. |
| schema-bo-sot-provider-hop-le | F10: schema/provider/consumer v2 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Diff ADR không đổi phần schema/nợ, không có mã consumer trong thay đổi r10. |
| tien-kiem-lease-chua-du | F11.b–i và G1–G10 | #1484 | INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE | Giới hạn và việc rút tiền kiểm ở mục 0/1/14 giữ nguyên. |

Authority kế thừa verdict r9: comment 7053593553 cho #1469/#1470, comment 7058057029 cho #1484; không xác thực online trong lượt này. Tất cả **CHƯA VÁ** phần nợ.

Có thêm **một tên nợ đã được chủ kho cho phép**: `phep-dem-ban-sao-khong-phu-ca-tep` → #1469, `INV-KHOA-BAN-SAO-DINH-CHU`, Q3/E3 comment 7201538748. Nhưng điều kiện (1) chưa hoàn tất như phân tích trên, nên chưa tính thành lớp thứ sáu đủ điều kiện rời bảng (i). Số 28 mục Nợ của ADR khác với số lớp bảng (ii); không trộn hai đơn vị đếm. Đây không phải reviewer bác việc chuyển phạm vi hay tự đặt nợ mới.

## BẢNG SĂN — hướng độc lập, lệnh và output thật

Mỗi hàng là một giả thuyết/cơ chế cần bác riêng, không phải mỗi biến thể đầu vào được đếm thành một hướng. Các probe dùng văn bản Markdown vô hại. Hướng liên quan nội dung tấn công chỉ được xét bằng mô tả: chuỗi trong backtick có thể bị consumer hiểu như đường dẫn/lệnh/con trỏ ca; không dựng nội dung tấn công.

| hướng | lệnh đã chạy | output thật / kết quả |
|---|---|---|
| 1. Phép đếm bản sao và chốt ID độc lập có thể trái lời hứa xanh | `python3 -B out/probes.py` | `K01/attached-after rc 9`, `K01/space-separator rc 9`; stderr `ID bất biến trên dòng bảng nằm ngoài tiểu mục §1.1`; `K02/attached-after rc 0` đến K07 cùng rc 0. Phát hiện P2. |
| 2. Biên trọn mục và biên khối có cùng ý nghĩa sau đoạn nối không | Cùng `out/probes.py`, nhóm `blank-separator` và `standalone` | `K03/blank-separator rc 0`; `K04/blank-separator rc 9`, stderr `có 2 bản hiển thị ... phải đúng 1`; cả 7 `standalone` rc 9. Xác nhận giới hạn theo loại đơn vị. |
| 3. Bản sao không hiển thị có làm đếm nhầm | Cùng `out/probes.py`, nhóm `fenced-copy` | K01–K07 đều `rc 0 expected 0`. Không thấy hồi quy trong ca rào mã vô hại. |
| 4. Thu hẹp đếm bản sao có vô tình bỏ băm bản gốc | Cùng `out/probes.py`, nhóm `change-original`; `python3 -B out/hash_independent.py` | K01–K07 đổi byte đều `rc 9 expected 9`; `INDEPENDENT_HASH 7/7 PASS`. |
| 5. Sáu ca G8 hiện tại có phân biệt miền ID ngoài 99 | `python3 -B out/stock99.py`; `python3 -B out/g8.py` | Sau hoàn chỉnh phụ thuộc: `STOCK_ONLY99 6 / 6 ERRORS {}`. Vòng mutant thật: `nền: 36/36 đạt · BỎ QUA: 0`, `ok  rv_g8_only99 → giết 30 ca đích · 3 đối chứng khác họ còn sống`, `TỔNG: ĐẠT`. G8 mới đo được. |
| 6. Ranh giới regex có nhầm tên nợ/ID dài với ID trần | `python3 -B out/probes.py`, nhóm `id-boundary` | `debt`, `three-digits`, `suffix-letter`, `suffix-hyphen` đều rc 0; `punctuation` rc 9. Chốt hậu tố không bị yêu cầu G8 mới làm mất. |
| 7. Chuẩn hóa hiển thị có phụ thuộc riêng ID99 | Cùng `out/probes.py`, nhóm `id-normalize` dùng ID01 | `fullwidth rc 9`, `cf rc 9`, `soft-hyphen rc 9`. Không thấy giới hạn chỉ-99 trong mã nền. |
| 8. Consumer tài liệu có đọc nhầm backtick mới | `python3 -B out/spans.py`; `python3 -B out/gates.py` | `adr SPANS 103 FINDINGS []`; tổng 236 span, không finding. Full strict `ok:true`, `flags:[]`, `layers_skipped:{}` trên H và candidate. |
| 9. Tên nợ/số đếm hoặc template có trôi khi sửa prose | `python3 -B out/audit.py`; kiểm dựng lại trong `out/final-audit.log` | `DEBTS 28 UNIQUE 28`; 9 khối bắt buộc bằng byte; `REBUILD_EQUAL True`; Trạng thái 8.1 lấy revision của chính tệp được duyệt. |
| 10. Nâng trần có đủ hợp đồng của ADR, không chỉ có con số | `python3 -B out/audit.py`; `python3 -B out/final_audit.py` | `NANG_TRAN_FIELDS {'ai_nang': 0, 'can_cu': 0, 'tran_cu': 0, 'tran_moi': 0}`; N12 và mục 10 cùng 500; H + ADR là +447. Phát hiện P3 ở hợp đồng cho phần nới. |

Log tổng probe: **`TOTAL 113 MATCHED 113 DOMAIN_VALUES 31`**. “MATCHED” là khớp dự đoán từng probe, kể cả dự đoán màu trái lời hứa §8.3; **không** có nghĩa đặc tả đạt 113 tiêu chí. Các fixture cô lập chỉ chứa protocol nên dòng scanner chung nói “quét 0 tệp”; chốt protocol chạy trước và đã trả đúng lỗi đo được. Hai full scan trên cây đầy đủ quét 12 tệp, ghi riêng bên dưới.

## BẢNG ĐO

| phép đo | kết quả và giới hạn |
|---|---|
| Băm đầu/cuối, blob Git | `ac1593e6cfe22896de372cb601cec6198350dec0bef5077dc80f6b8a44646966`; `BLOB_EQUAL True`; đúng commit giao. |
| Diff r9→r10 | Lưu `spec.diff`; script dựng r10 của hồ sơ chạy trên r9 cho byte đúng tệp review (`REBUILD_EQUAL True`). |
| Khối không được đổi | `p1-moi`…`p6-moi`, `khoa`, `do-pham-vi`, `so-dang-ky`: **9/9 bằng byte**. Cả `p4-cu`/`p5-cu` cũng bằng byte. Trong 12 khối có tên, chỉ `adr` đổi. |
| Số mục Nợ | 28 mục, 28 tên duy nhất; thêm đúng `INV-KHOA-BAN-SAO-DINH-CHU`. M1 và C1 đều khai 28. |
| Trạng thái 8.1 | Dòng 206 yêu cầu hash của chính tệp đã duyệt và N từ `revision:`; do đó phải là r10 và hash được giao. Không có literal r9 bắt buộc trong template. Ngày/comment E5 chính xác chưa được cung cấp để điền; cây tổng hợp giữ dòng H theo thiết kế phép thử. |
| H: ba cổng | `doc-claims-check --strict --json`: rc 0, `ok:true`, 132 tệp, flags 0, advisory 392. `doctrine-scan`: rc 0, 12 tệp, 0 chỗ. `adr-song`: rc 0, 67 ADR/67 dòng, khớp 1–1, ngoại lệ cũ ADR0016. |
| H + diff ADR: ba cổng | Cùng các số trên, cả ba rc 0. `layers_skipped:{}`; không đọc advisory thành finding nghiêm trọng. |
| Khóa | 7/7 địa chỉ, thứ tự, băm byte thô khớp bảng; mỗi khóa có 1 bản theo định nghĩa đơn vị. Script parser của reviewer r9 được đọc và tái dùng, độc lập với parser executor; không nhận là parser mới tự viết. |
| G8 | 31 giá trị phân biệt: 00,01…28,98,99. Mã nền rc 9 cho 31; mutant chỉ99 lọt 30 giá trị còn lại. Thử nghiệm harness thêm 30 ca, giữ 6 ca cũ; nền 36/36, mutant giết 30, 3 đối chứng sống. Đây là bằng chứng khả thi của yêu cầu, không phải commit thực thi. |
| Kích thước | Nền `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70` → H: đúng 4 tệp, +443/-4. Cây H + diff ADR: +447/-4. Chưa có thêm mã ca G8 vào file, chưa có H-r10 cuối để chứng minh ≤500. |
| Trần 500 | Mục 0, N12 dòng 550 và mục 10 dòng 717 nhất quán. “434, còn 16” được gắn rõ là nguyên mẫu r5; 450 là trần chung trước ngoại lệ, không phải trần r10 còn hiệu lực song song. Thiếu khối formal là finding riêng. |
| Opt-in ADR0053/0055 | Mỗi OID có tệp tại OID (rc 0), không có tại cha thứ nhất (rc 128), nằm trên first-parent `origin/master`; clone không shallow. Đây là kiểm snapshot cục bộ, không chứng minh ref vừa fetch từ máy chủ. Không có lý do phủ nhận authority 12/13 đã được PROMPT cấp. |
| Không sửa nguồn | Snapshot bao gồm cả `.git`: `cay-kho` 19.083 tệp, `kho.git` 22 tệp; **0 thêm, 0 mất, 0 thay đổi** cả nội dung và size/mtime. `git status --porcelain` nguồn rỗng. Chỉ ghi `out/`, không push/ghi API GitHub. |

### Các lớp L1–L12 của consumer backtick

Khối ADR mới có 3 occurrence backtick thêm vào: `INV-KHOA-BAN-SAO-DINH-CHU` hai lần, `doctrine-scan` một lần; 2 giá trị phân biệt. Quét cả khối tại đúng đường dẫn ADR, không đưa snippet vào một tệp có ngữ cảnh sai.

| lớp | đối chiếu |
|---|---|
| L1 | Hai token mới không phải đường dẫn file; 0 finding khi quét cả ADR. |
| L2 | Không phải SHA; full scan chạy trên phần văn bản tương ứng, 0 cờ. |
| L3 | Không có cú pháp link mới trong các token này; 0 cờ. |
| L4 | Không phải placeholder/TODO; ADR thử đã giữ giá trị điền từ H. |
| L5 | Không phải version được consumer nhận; 0 cờ. |
| L6 | Không thêm số đợt; 0 cờ. |
| L7 | Không có con trỏ `.py:<dòng>` mới; 0 cờ. |
| L8 | `doctrine-scan` đứng riêng không bị nhận thành khai lệnh CLI cần resolve; thực đo 0 cờ. |
| L9 | Full scan chạy, không skip; 0 cờ. |
| L10/L11 | Không có scanner đang bật: `basis.layers_bac` ghi L10 đã bác vì kho cố ý chỉ giữ 6 bản GAS, L11 đã bác vì số hiệu chính thức bare là đúng. Không ghi hai lớp này là “đã chạy xanh”. Token mới cũng không mang hai dạng ấy. |
| L12 | Không phải con trỏ tên ca selftest; resolver trên cả 7 khối không báo cờ. |

### L1–L7 của soan-spec và M1–M12

| luật | kết luận trong phần r10 đổi |
|---|---|
| L1 — đơn vị đếm | 28 là mục Nợ, 7 là khóa; 500 là dòng thêm; N6/N7 vẫn khai tập. Không trộn số ca thử của reviewer với số ca sản phẩm. |
| L2 — write set | Thay prose vào ADR-0068, thêm G8/mutant vào tệp test đã có trong write set; không phát sinh đường dẫn sản phẩm thứ năm. |
| L3 — phép đo làm đỏ | G8 định rõ mutant chỉ99 và ID thật/biên, đã thử đo được; câu cấm đỏ ở §8.3 lại trái chốt ID → P2. |
| L4 — hình dạng kế thừa | Mục 0/19 ghi hai slug/hạng của review mã, 23/43 và 6 ca99. Không tự đổi hạng hay coi chuyển nợ là vá. Các số 23/43 là số được kế thừa, không nhận là đã tái chạy đủ 43. |
| L5 — thời điểm/số đo | R10 ghi ngày và nguồn review H; các số nguyên mẫu có nhãn lịch sử. Đã đo lại hash, khối, nợ và numstat ở lượt này; final H-r10 chưa đo được. |
| L6 — kiểm thước đo | Tái băm 7 khóa; đối chứng theo loại biên; chạy mutant thật G8. Phép (3) đúng phạm vi đơn vị, không chứng minh toàn cổng xanh. |
| L7 — authority/điểm dừng | E2/E3/E5 đã được giao; không thêm điểm hỏi chủ kho. Thực hiện lượt12/13, không suy trần10 chung phủ nhận ngoại lệ đã cấp. Phần formal nâng kích thước cần hoàn thiện theo ADR0053. |

Đã đối chiếu ADR0060 M1–M12 cùng ADR0062/0063: các cổng tài liệu đang xanh không thay thế lease/spec_hash, bằng chứng ca/mutant trên H cuối, CI, Windows hoặc merge gates. R10 không cho phép bỏ các điều kiện đó. Lượt này không có dữ liệu để chứng nhận chúng hoàn tất.

## Chi tiết finding

### phep-dem-ban-sao-khong-phu-ca-tep [P2] Thu hẹp phép đếm nhưng lại cam kết sai kết quả toàn cổng

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:470` (đoạn mới của r10); đối chiếu chốt ID dòng 486, M3 dòng 197, G8 dòng 515, N4. Lớp kế thừa review mã exact-H lượt 1, giữ nguyên slug và P2.

**VẤN ĐỀ:** “không bị đếm” chỉ đúng với phép (3). Suy ra “nên cổng xanh với nó” rồi cấm mọi ca đòi đỏ trên các dạng ấy là sai. Một bản sao nguyên byte K01 dưới mục khác, kèm một đoạn văn vô hại sau nó, không còn là trọn đơn vị K01. Phép đếm không bắt bản này nhưng các hàng `INV-01`… của bản sao vẫn nằm ngoài khoảng K01 chính; chốt ID trả rc9. Bản sao có một dòng chỉ dấu cách trước đoạn nối cũng vậy. R10 tự mâu thuẫn giữa ngoại lệ mới và nghĩa vụ ID còn giữ. Nếu executor tuân câu cấm đỏ, họ có thể bỏ một ca hồi quy hợp lệ hoặc yếu hóa chốt ID.

Đã rà cả 7 khóa với các kiểu ranh giới, các câu hứa trong toàn văn (53 dòng được bộ tìm từ khóa chọn, sau đó đọc ngữ cảnh), mục 0/M3/Q3/N4/8.3/19. Chưa thấy một lời hứa đếm mọi bản sao khác cần mở thêm slug. Mục Nợ của ADR chỉ nói **không bị đếm**, vốn là cách diễn đạt đúng hơn.

**GỢI Ý VÁ:** Giữ quyết định chuyển #1469 và giữ mã phép (3). Thay kết luận bằng ý: “phép (3) không phát hiện các bản sao này; không yêu cầu wp1466 đỏ chỉ vì có bản sao ngoài đơn vị; các điều kiện địa chỉ, băm, hiển thị, ID và không đo được vẫn áp dụng”. Bỏ lệnh cấm mọi ca đỏ. Sau sửa, rà lại toàn bộ lời hứa để hoàn tất điều kiện (1) chuyển lớp; không ghi phần chuyển là ĐÃ VÁ THẬT.

**ĐÃ THỬ NGHIỆM:** `probes.json`, `probes.log`, `final-audit.log`. `K01/attached-after` và `K01/space-separator`: rc9, chỉ nêu lỗi ID ngoài §1.1, không báo có hai bản theo phép (3). K02–K07 cùng hai biến thể: rc0. Bản sao đứng thành đơn vị: cả7 đỏ. Không sửa sản phẩm để tạo kết quả.

**ĐỘ TIN:** Cao; mâu thuẫn câu chữ được CLI thật tái hiện, có đối chứng âm/dương theo từng loại khóa. Không chứng minh mọi cách đính nội dung đều cho cùng màu; đó chính là lý do không được hứa toàn cổng xanh.

### thieu-khoi-nang-tran-kich-thuoc [P3] Hợp đồng phần nới trần chưa có khối khai bắt buộc

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:64`, `:550`, `:717`; chuẩn đối chiếu `cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md:34`–`:37`, soan-spec §3.

**VẤN ĐỀ:** R10 gọi việc nâng 500 là `nang_tran` và N12 coi chỉ lớn hơn 500 mới phải dừng. Nhưng đặc tả không có khối gồm `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`; cả bốn tên trường đều vắng. ADR0053 yêu cầu khối này trong đặc tả và bản chép trong lease khi vượt 450, với căn cứ vì sao không tách được và số đo numstat. Chỉ trỏ E2 chưa cung cấp hiện vật mà hợp đồng ấy yêu cầu. Vùng ứng viên +451…+500 được N12 mới cho qua sẽ vẫn thiếu hồ sơ này.

**Giới hạn quan trọng:** Quyền nâng trần đã có, không phải finding thiếu quyền. H hiện +443 và cây tổng hợp +447, chưa vượt 450; không cáo buộc hai cây này đã vi phạm ngưỡng. Nếu sản phẩm cuối luôn ≤450 thì ADR0053 không bắt khối. Finding P3 ở việc đặc tả đang tuyên bố áp dụng phần nới mà chưa quy định/điền hồ sơ bắt buộc khi dùng phần đó, không phải suy đoán kích thước H-r10.

**GỢI Ý VÁ:** Bổ sung khối dựa trên **E2 đã duyệt**, xác định người nâng và comment, căn cứ cần giữ phần sửa G8 trong packet, số đo có nền/H/thời điểm và nghĩa vụ cập nhật, cặp cũ 6 tệp/450 dòng thêm → cặp mới 6 tệp/500 dòng thêm; write set wp1466 vẫn đúng 4 tệp. Quy định chép vào lease khi dùng ngoại lệ. Có thể ghi rõ điều kiện chỉ cần khối khi vượt 450; không cần xin lại quyền đã có. Không tự bịa số đo final H.

**ĐÃ THỬ NGHIỆM:** `audit.log` và `final-audit.log`: bốn trường đều 0; N12 và mục 10 cùng 500; numstat độc lập 4 tệp/+443 và tổng hợp+447. Ba cổng xanh không phủ nhận finding vì ADR0053 khai rõ kiểm khối này bằng tay, chưa có cổng.

**ĐỘ TIN:** Cao về thiếu khối và văn bản chuẩn; điều kiện kích hoạt là ứng viên cuối vượt450, chưa đo được trên H-r10. Hạng P3 phản ánh thiếu hợp đồng/hồ sơ formal, không phải lỗi thuật toán hay thẩm quyền.

## Hiện vật, lỗi dựng phép thử và giới hạn

- `audit.py`, `audit.log`, `spec.diff`, `adr-r9-r10.diff`: byte/hash/nợ/diff/trần; `promise-sweep.txt`: danh sách hỗ trợ rà lời hứa, không thay thế đọc toàn văn.
- `gates.py`, `gates.log`, `h-*.json`, `candidate-*.json`: argv/cwd/rc/stdout/stderr đầy đủ của sáu lần chạy cổng.
- `hash_independent.py`, `hash.log`, `keys.json`, `K01.raw`…`K07.raw`: phép băm riêng. Script tái dùng từ bằng chứng reviewer r9 đã đọc.
- `spans.py`, `spans.log`, `spans.json`: backtick/context/lớp đang bật.
- `probes.py`, `probes.json`, `probes.log`: 113 quan sát; `g8.py`, `g8.log`, `g8-summary.json`, `stock99.py`, `stock99.log`: thử miền ID và mutant thật.
- `finish_setup.py`, `finish-setup.json`, `final_audit.py`, `final-audit.log`, `*-before.json`, `*-integrity.json`: dựng cây và kiểm nguồn không đổi.

Lần dựng đầu lấy H từ mirror thất bại vì mirror không có ref executor; sau đó fetch **cục bộ vào cây thử** từ ref đã được cấp trong `cay-kho`. Lần gọi mutant riêng đầu tiên thiếu module `launcher` nên rc1; log được giữ ở `probes-setup-error.log`, và phần `stock` của `g8-summary.json`/đầu `g8.log` còn ghi lỗi dựng ấy. Sau bổ sung các module phụ thuộc vào `out/id99/`, bộ probe chạy đủ113/113 và chạy lại sáu ca cũ cho **6/6** tại `stock99.log`. Kết quả vòng mutant thật trong `g8.log` đã tự dựng đủ module và đạt36/36 từ lần đó. Không dùng rc1 hay exception thiết lập làm finding sản phẩm hoặc làm bằng chứng giết mutant.

Chưa đo: mã r10 cuối có G8 đã đăng ký/commit, N1 sau điền duyệt r10, toàn suite/selftest/mutant cũ trên sản phẩm r10, CI/ruleset server, lease hiện hành, Windows, K7, N15/merge-ready; ngày/URL chính xác của comment E5; độ mới ref máy chủ; model/effort thực phục vụ. Không gửi review GitHub, không merge. Hướng cần nội dung tấn công không được dựng. Kết luận chỉ áp cho đặc tả/hash ghi đầu tệp và các phép đo được mô tả.
