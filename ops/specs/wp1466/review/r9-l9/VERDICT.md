verdict: approve
reviewed_sha: b9416b93e5a9dce7f8d245e2fb35d685594cdf07
spec_sha256: 28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, effort: high, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: 0, so_bieu_hien_mo: 0, P0: 0, P1: 0, P2: 0, P3: 0, so_lop_no_ke_nhiem: 5}
hoi_tu: {U: 0, F: 0, lop_moi: 0, lop_tai_mo: 0}

**Approve đặc tả r9:** bảng (i) có 0 finding P0–P3 sau các phép đo dưới đây. Năm lớp nợ kế nhiệm giữ nguyên, không được tính là đã vá.

Phạm vi là **đặc tả r9**, không phải phê duyệt mã giao nộp hoặc quyền merge. Băm đã kiểm đầu tiên, đúng giá trị trên; tệp trên đĩa bằng blob ở reviewed SHA, tree `1502b179ae88163c5ece49a299cee6d75685d96a`. Mọi ghi mới nằm dưới `out/`. Không sửa `cay-kho/` hoặc `kho.git`, không push, không gọi API GitHub.

Cây thử `candidate/` = H `96e44721a149b363c83af4fcabe3599232f6512b` cộng đúng hai thay đổi: thay `p2-moi` trong protocol và thay băm K01 trong mã. Nền là `1fac6ced8e5a8c76fdb2699edac779a4251f6149`; Git ghim `core.abbrev=7`. Cây này chưa phải một commit r9 giao nộp. Các đường dẫn hiện vật dưới đây tính từ thư mục chứa verdict.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 8: `cay-kho/ops/specs/wp1466/review/r8-l8/VERDICT.md`, trên r8 `e215940`; bảng (i) rỗng. Đối chiếu byte với r8 đã land tại `434846a`. Không có lớp mở của bảng (i) để tính vá: U=0, F=0, tỷ lệ **N/A**, không phải 100%. Năm lớp bảng (ii) tiếp tục CHƯA VÁ, không tính thành F.

| slug | nhãn | bằng chứng tự đo |
|---|---|---|
| neo-sai-don-vi-khop | ĐÃ VÁ THẬT, giữ kết luận trong phạm vi đã đo | Parser riêng băm trọn 7 đơn vị; hằng mã khớp 7/7; vòng đột biến mới giết các mutant bỏ từng khóa. |
| neo-thieu-nghia-vu | ĐÃ VÁ THẬT, giữ | K02–K07 và năm khối protocol bằng byte; ba ca xoá câu nằm trong lượt nền đạt và vòng đột biến thật. |
| cong-khong-do-bat-bien | ĐÃ VÁ THẬT, giữ | 15/15 ô có cổng đều còn nợ; 12 ô kỷ luật, 1 chưa đo; không nâng lời khai thành cưỡng chế đầy đủ. |
| thieu-truy-vet-yeu-cau | ĐÃ VÁ THẬT, giữ | Đối chiếu riêng 10 bất biến của §1 sau nối dòng trong từng mục: 10/10 bằng nội dung bảng. |
| kiem-chuoi-khong-doc-cau-truc | ĐÃ VÁ THẬT phần khóa byte; CHƯA VÁ F05.b/c | Ca và mutant byte thô/biên/che/ID đều chạy; 25 tên nợ đều có trong 27 mục Nợ chỉ là kiểm tĩnh; consumer ngữ nghĩa vẫn giao #1469. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ phần kế nhiệm | G1 hiện có được ca/mutant kiểm; không thêm reader cổng/ca/ADR. Khối ADR và phạm vi kế nhiệm giữ nguyên. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Không nhận lại vị từ cutover của #1470; ADR bằng byte. |
| tieu-chi-dong-xoa-khong-do-hanh-vi | ĐÃ VÁ THẬT trong phạm vi N8, giữ | `do-pham-vi` bằng byte; hai chế độ mã/test đều ĐẠT; `so-dang-ky` ĐẠT. Không coi AST là chứng minh mọi tác dụng phụ lúc chạy. |
| dem-khong-khai-tap-ca | ĐÃ VÁ THẬT, giữ | Đo riêng đăng ký 1804→1864 và Linux 1803→1863, hai hiệu đều 60. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ | Không thêm schema/consumer v2; tiếp tục #1470. |
| tien-kiem-lease-chua-du | CHƯA VÁ | R9 không phục hồi khối tiền kiểm đã rút; mục 0/1/14 giữ G1–G10 và nợ của #1484. Không tuyên bố chạy lại tiền kiểm lease thật. |
| doi-diem-goi-cong-chua-du-yeu-cau | ĐÃ VÁ THẬT, giữ | CLI `doctrine-scan` chạy chốt; mutant bỏ lời gọi giết 54 ca đích, 3 đối chứng còn sống. |
| doi-chung-khac-ho-chon-nham-doctrine | ĐÃ VÁ THẬT, giữ | Mọi dòng của 29 mutant mới đều có 3 đối chứng khác họ còn sống. |
| ma-tran-dem-doi-loi-thay-doi-mau | ĐÃ VÁ THẬT, giữ | Dùng `packet_loop_test_manh.chay` thật: nền 63/63, 29 dòng giết mutant, `TỔNG: ĐẠT`. |
| tach-packet-bo-dieu-kien-integration | ĐÃ VÁ THẬT, giữ phần quyết định | Mục 0 giữ nguyên E5 cho #1466/#1469/#1470; r9 không mở rộng sang #1484/B4. Authority lấy từ chỉ thị và hồ sơ, không xác thực online. |
| nghiem-thu-khoa-so-ca-trai-quyen-them | ĐÃ VÁ THẬT, giữ | N6/N7 vẫn là tập bắt buộc cộng phần thêm thực; T=60, mutant mới=29 được nhận và chạy. |
| khoa-khong-neo-vi-tri-va-duy-nhat | ĐÃ VÁ THẬT trong định nghĩa đơn vị; đã kiểm thêm phần đầu tệp | Các bản sao đứng thành khối trước tiêu đề bị đếm; dời khỏi địa chỉ vẫn đỏ; hai loại đơn vị được phân biệt. Xem 73 probe và phân tích bên dưới. |
| moc-dot-bien-tu-khop-trong-khai-bao | ĐÃ VÁ THẬT, giữ | Ca `moc_dot_bien_phai_khop_DUNG_MOT_CHO` có mặt trong lượt nền mới và lượt ca cũ, đạt; N8 và sổ cũ giữ nguyên. |
| con-tro-trong-backtick-bi-cong-khac-doc | ĐÃ VÁ THẬT đối với nội dung r9 đưa vào kho | Cùng scanner/context: p2 r8 có 3 cờ L12; p2 r9 không cờ. Quét đủ 233 span của 7 khối và full CLI không còn cờ L1–L9/L12. Đây là lớp executor phát hiện sau lượt 8, không phải finding mở của lượt 8. |

Không gộp hoặc đổi slug. Cơ chế executor gọi `phep-dem-ban-sao-khong-phu-ca-tep` được đối chiếu trong lớp lịch sử `khoa-khong-neo-vi-tri-va-duy-nhat`, không đếm thêm thành một lớp mới.

## BẢNG LỚP (i) — lớp MỞ của wp1466

| slug lớp | biểu hiện | hạng | phương án chung | phép kiểm/giới hạn |
|---|---|---|---|---|

**0 lớp, 0 biểu hiện P0–P3.** Không có finding mở để lập mục chi tiết P0–P3. Các giới hạn nêu dưới đây không được biến thành lời khai đã kiểm chứng ngoài phạm vi.

## BẢNG LỚP (ii) — nợ kế nhiệm có authority

| slug lớp | biểu hiện giữ nguyên | packet và tên nợ | authority/phạm vi |
|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c: khai báo ca theo cấu trúc, consumer kiểm mục Nợ | #1469 · INV-BANG-DOI-CHIEU-NGU-NGHIA | E2 tách 3 packet; mục 0, 14, 19 và ADR. |
| duong-dan-chua-khep-trong-goc | F06: ba reader kế nhiệm | #1469 · INV-BANG-DOI-CHIEU-NGU-NGHIA | Cùng E2; wp1466 chỉ nhận reader protocol. |
| moc-chuyen-tiep-mau-thuan | F07: vị từ chuyển tiếp | #1470 · INV-12-CONG-VERDICT-THEO-LOP | Cùng E2; không có tiêu chí wp1466 nhận lại nghĩa vụ. |
| schema-bo-sot-provider-hop-le | F10: schema/provider/consumer v2 | #1470 · INV-12-CONG-VERDICT-THEO-LOP | Cùng E2; ADR không đổi. |
| tien-kiem-lease-chua-du | F11.b–i và G1–G10 | #1484 · INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE | E2 tách tiền kiểm; mục 0/1/14/19 tiếp tục khai nợ. |

Authority được kế thừa từ lượt 8: comment 7053593553 cho #1469/#1470; comment 7058057029 cho #1484. Chỉ thị hiện tại cung cấp Q0/E3 và Q2/E5 cho r9. Không tự suy rằng đề xuất Q3 trong HANDOFF đã được duyệt: **không thêm nợ kế nhiệm mới** cho giới hạn tìm chuỗi con hay HTML giữa dòng.

## BẢNG SĂN

Mọi lệnh dưới chạy từ thư mục giao việc, trừ khi ghi cwd riêng. `run.py` ghi argv, cwd, rc và output nguyên văn. Các hướng độc lập theo cơ chế: consumer tài liệu, miền đếm, che hiển thị, địa chỉ, số bản, nhận dạng byte/biên và sổ nghiệm thu. Không lấy số biến thể của một hướng làm số hướng.

| hướng | LỆNH | OUTPUT THẬT | kết luận/giới hạn |
|---|---|---|---|
| 1. Consumer khác diễn giải backtick | `python -B out/run.py spans . python -B out/spans.py`; cwd `out/candidate`: `python -B scripts/tl.py doc-claims-check --strict --json` | `TOTAL_SPANS 233 LAYER_FINDINGS {}`; p2 r8 có 3 `TEST_ID_UNKNOWN`; r9 `ok: true`, flags 0, advisory 392 | Quét mọi span trong sáu khối protocol và ADR, không chỉ L12; L9 được full scan chạy. |
| 2. Miền đếm trước tiêu đề và biên khối | `python -B out/run.py probes . python -B out/probes.py` | Với K02/K04/K05/K06/K07, `first`, `adjacent-heading`, `later-block`, `leading-blanks`: rc9, `có 2 bản`, tất cả PASS | 20 phép bao đầu tệp, sau khối khác, sát tiêu đề và dòng rỗng đầu. |
| 3. Bản che và cách tìm tiêu đề đầu | Cùng lệnh probe; `python -B out/run.py prefix-mask . python -B out/prefix_mask.py` | 10 bản sao trong fence/comment: rc0; 10 bản sao nằm sau tiêu đề giả đã che: rc9; `MASKED_HEADING_BOUNDARY 10/10 PASS` | Không lấy tiêu đề thô nằm trong vùng che làm biên phần đầu. Chỉ dùng Markdown/comment bình thường, không nội dung thực thi. |
| 4. Địa chỉ không được phép đếm cứu | Lệnh probe trên, nhánh `move-before`, `whole-section-before`, `no-headings` | 5 lần dời khối lên đầu: rc9 `không còn nguyên ... đúng địa chỉ`; K01/K03 chép trước: rc9; không tiêu đề: rc9 `thấy 0` | Phép (1)/(2) không bị phần đầu tệp thay thế; trọn mục tự tạo tiêu đề nên khác loại khối. |
| 5. Duy nhất là đúng một, không phải có ít nhất một | Lệnh probe, nhánh `two-copies`; vòng `db-moi` dưới | 5 đầu vào có hai bản sao thêm: rc9 `có 3 bản`; `inv_duy_nhat_lech_so → giết 6 ca đích` | Không dùng số lượng case tổng để suy tính đúng của ngưỡng. |
| 6. Byte thô và biên đơn vị so với chuỗi con | Lệnh probe, `attached-before/after/space-line`; `python -B out/run.py mutants-new . python -B exec-out/sc/chay_ca.py out/candidate out/baseline out/tmp/tests db-moi` | 15 bản sao dính đoạn khác: rc0; mutant `inv_doc_qua_text` giết 9, `inv_tach_dong_splitlines` giết 8, `inv_cat_cuoi_muc` giết 5, `inv_dong_trang_la_khoang_trang` giết 2 | Phân biệt giới hạn định nghĩa với lỗi chuẩn hóa byte; không tuyên bố bắt mọi dãy byte con. |
| 7. Răng của ba đường sửa phần đầu | Cùng vòng `db-moi` | nền `63/63 đạt · BỎ QUA: 0`; ba mutant mới lần lượt giết `2`, `1`, `1` ca; mỗi dòng 3 đối chứng còn sống; `TỔNG: ĐẠT` | Đo bằng bộ chạy thật, không chỉ thấy tên ca/đột biến trong mã. |
| 8. Tập bắt buộc, phần thêm và sổ cũ | `python -B out/run.py registry . python -B out/so-dang-ky.txt out/baseline out/candidate`; hai lần `out/do-pham-vi.txt ma/test ...` | T=60; đăng ký 1804→1864, Linux 1803→1863; `mutants_cu_doi: []`; `SỔ ĐĂNG KÝ: ĐẠT`; `PHẠM VI [ma]: ĐẠT`, `[test]: ĐẠT` | Không bỏ ca cũ hoặc ghi đè mutant để vừa các tổng số. |

[probes.log](probes.log) có **63/63** phép đúng kỳ vọng; [prefix-mask.log](prefix-mask.log) thêm **10/10**. Các probe CLI với root tối thiểu in “quét 0 tệp” vì không có adapter: ở các phép này đối tượng là chốt protocol chạy trước vòng quét adapter. Cổng trên cây đầy đủ chạy riêng và in quét **12 tệp**; không tráo hai bằng chứng.

## BẢNG ĐO

Các phép đo mới chạy ngày **26-11-2026 UTC** trên snapshot được giao; [measure.log](measure.log) ghi mốc `2026-11-26T12:40:57Z`. Không xác nhận máy chủ tại thời điểm ấy.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| Hash/commit | reviewed SHA và sha256 trong chỉ thị | Khớp blob, cây làm việc và HEAD | Có |
| Khối r8→r9 | ADR, N8, sổ và 5 khối protocol không đổi | 10/12 khối bằng byte, gồm cả hai khối `p4-cu/p5-cu`; chỉ p2 và khoa đổi | Có |
| K02–K07 | 6 bộ bốn giữ nguyên | 6/6 bằng byte; tự băm 7/7 và so hằng mã 7/7 | Có |
| K01 mới | `987f9527…381c5` | `987f952747e26847a5a8e39dd82bf09da72d508dd3e03cef3bfdd42db4e381c5` | Có |
| Sáu khối protocol | Mỗi khối mới đúng 1 lần; khối cũ 0 | 6×1, p4-cu/p5-cu 0; protocol +46/−2 | Có |
| Bảng bất biến | 28 hàng; 18 trỏ ca không backtick | 28; 18; 0 trỏ ca thật có backtick | Có |
| Cổng/ngữ nghĩa nguồn | 15 cổng đều có nợ; 10 câu từ §1 | 15/15; 10/10 sau nối dòng riêng mỗi mục | Có |
| Nợ bảng | Các tên có trong mục Nợ | 25 tên được trỏ, 27 tên đăng ký, thiếu 0 | Có, chỉ kiểm tĩnh |
| doc-claims nền/r9 | Cùng 392, rc0 | Cả hai `ok=true`, 0 flags, 392 advisories, `layers_skipped={}` | Có; 392 không phải cờ chặn |
| doctrine/ADR r9 | rc0 | sạch 12 tệp; ADR 67/67, rc0 | Có |
| N6/N7 tập thực tế | Được thêm ngoài 57/26 | T=60; mutant mới=29; 63 ca nền vòng đột biến đều đạt | Có |
| Răng mutant mới | Mọi mutant mới giết ca đích | 29 dòng `ok ... giết`; mỗi dòng 3 đối chứng sống; `TỔNG: ĐẠT`, rc0 | Có |
| N8/sổ cũ | Cấu trúc giới hạn và sổ được bảo toàn | Cả 3 phép ĐẠT | Có |
| Ca cũ | 132 doctrine + mốc; 40 ADR | 133/133 và 40/40, bỏ qua 0 | Có |
| Mutant cũ | 21 mutant có ca đích trong họ doctrine | nền 132/132, 21 dòng giết mutant, đối chứng sống; TỔNG: ĐẠT, rc0 | Có |
| Tập bắt buộc nguyên mẫu | 57 ca, 26 mutant giữ tên và cặp tìm/thay | Dựng nguyên mẫu từ 48d372e: thiếu 0/0, cặp đổi 0; hai danh sách đích chỉ thêm 52→54 và 5→6 | Có |
| Numstat H, H+r9 | H +443; trần 450, 4 tệp | Cả hai: mã +78/−1, test +170/−1, protocol +46/−2, ADR +149/−0 = +443/−4 | Có; còn 7 dòng |
| ADR sáu số | Đo trên ứng viên | 0·11·0·0·0·0; thân ADR bằng template sau điền | Có; trạng thái vẫn là r8 của H |
| Opt-in 0053/0055 | OID land hợp lệ | Tệp tại OID rc0; tại cha rc128; đều first-parent master; không shallow | Khớp snapshot |

### Quét các lớp L1–L12 của doc-claims-check

Nguồn phân tích: `scripts/tl_core/workflow.py:1203–1538` và các hàm mask/context. [spans.json](spans.json) giữ đủ **233** span: p1=3, p2=118, p3=2, p4=1, p5=4, p6=5, ADR=100. Quét dùng đường dẫn tài liệu đích thật, ADR đã điền chỗ trống; không quét cả spec trong fence rồi nhận sự im lặng thành bằng chứng.

| lớp | cơ chế liên quan | kết quả trên phần sẽ đưa vào kho |
|---|---|---|
| L1 | Token đường dẫn trong span, kể cả `.claude/`, `.github/` | 0 cờ/0 advisory trong 7 khối; các đích được nhắc tồn tại trong cây thử. |
| L2 | SHA trên văn bản đã che span | Span không bị đọc thành SHA; full scan vẫn chạy phần văn xuôi, 0 cờ. |
| L3 | Link Markdown trên bản chưa che span | Có thể đọc cú pháp link cả trong backtick; 7 khối không sinh cờ. |
| L4 | Placeholder/TODO trên văn bản đã che span | Đã điền ADR, không coi template `{{…}}` chưa dựng là sản phẩm; 0 cờ. |
| L5 | Version trên bản đã che span | 0 cờ. |
| L6 | Số đợt trên bản đã che span | Bỏ backtick quanh con trỏ ca không tạo cờ L6; 0 cờ. |
| L7 | Con trỏ `.py:<số dòng>` trên bản chưa che span | Con trỏ `::tên_ca` không phải vị trí dòng; 0 cờ. |
| L8 | Phân tích lệnh bắt đầu span bằng `tl` hoặc đường tl.py | 0 cờ; câu dẫn r9 không còn dạng lệnh nháp bị đọc sai. Không dựng lại câu nháp không có blob được giao. |
| L9 | Tài liệu mồ côi, phụ thuộc tập tài liệu được quét | Full CLI nền và r9 chạy lớp này, không skipped, 0 cờ; không suy từ quét riêng 7 khối. |
| L10/L11 | Hai đề xuất đã bị bác, không nằm trong `_DOC_CLAIMS_LAYERS` | Không có bộ kiểm thực thi để báo đạt. `basis.layers_bac` ghi rõ lý do; không gọi chúng là lớp đã chạy xanh. |
| L12 | Resolver ca selftest dùng chung, chỉ đọc span | P2 r8 sinh đúng `r812_nguoi_giu_khac`, `r812_nguoi_giu_prefix_giao_nhau`, `r1252_ghi_trong_git`; r9 bỏ backtick cả 18 trỏ ca thật nên 0 cờ. |

Bảng advisories toàn kho không chặn. `claims_flagged` là tổng phát hiện gồm advisory, không đồng nghĩa `len(flags)`. Không sửa runtime scanner hay nới phân loại để đạt rc0.

### Luật phần đầu tệp và tính nhất quán mục 0/8.3/19

`_inv_muc` tại H thêm phần tử cuối cho đoạn trước **tiêu đề hiển thị đầu tiên**. Các mục thật vẫn được tạo như cũ; phần tử thêm có khóa địa chỉ rỗng và đơn vị trọn-mục giả với băm rỗng. Bảy địa chỉ/băm thật đều khác rỗng. Do đó phần tử này chỉ đóng góp các khối vào phép (3); không tạo thêm địa chỉ khớp ở phép (1), không thay đơn vị của phép (2), không tạo bản sao trọn-mục hợp lệ. Khi không có tiêu đề, các khóa đều báo thiếu mục, rc9, không sập CLI.

Miền dòng nay phủ hết tệp: phần đầu cộng các mục từ tiêu đề này tới tiêu đề kế tiếp. Đã kiểm 5 khóa dạng khối ở mọi biên mà bản vá nhắm tới, kể cả hai bản sao thêm, đoạn dẫn khác trước chúng và tiêu đề giả trong vùng che. K01/K03 là trọn-mục: đặt chúng trước tệp tự tạo mục mới, nên không thuộc phần đầu theo định nghĩa. Không tìm thấy một đoạn dòng nào cùng cơ chế bị bỏ ngoài hợp miền này.

Giới hạn còn nguyên: phép (3) đếm **đơn vị cùng loại**, không tìm mọi dãy byte con. Một bản sao dính dòng văn bản khác, hoặc tách bằng dòng chứa dấu cách, thành khối lớn hơn và rc0; 15 phép độc lập xác nhận điều này với cả 5 khóa dạng khối. Câu “bản hiển thị trong cả tệp” ở mục 0/Q3 phải đọc cùng định nghĩa đơn vị tại 8.3. R9 mở miền sang phần đầu tệp, không đổi từ so đơn vị sang tìm chuỗi con. Đây không phải lớp mới do r9 sinh ra, và chưa có authority để tuyên bố nó đã chuyển thành nợ kế nhiệm mới. HTML giữa dòng được HANDOFF nêu là giới hạn; không tự dựng payload mới để thử hay tuyên bố đã đóng toàn bộ ngữ nghĩa Markdown.

Ba ca mới tại H thật sự chạy, không chỉ được đăng ký. Ba mutant nhắm phần đầu có kết quả riêng 2/1/1; ca đầu tệp K04 và ca khối thứ hai sát tiêu đề K02 phân biệt các biên. Ca chữ lạ ở phần đầu là đối chứng xanh; mutant đổi số lượng duy nhất giết nó cùng các ca xanh khác. Lượt nền 63/63 không bỏ qua, và đối chứng khác họ vẫn sống.

**“Các số của N6, N7 không đổi”** được đọc là không đổi **57 tên ca bắt buộc và 26 tên mutant bắt buộc**, không phải tổng thực tế giữ 57/26 hoặc số ca bị giết giữ nguyên. N6 định nghĩa T theo hiệu tập, N7 bao mọi mutant mới. T thực tế 60, mutant mới 29; `inv_doctrine_scan_bo_goi` giết 54 thay vì 52, `inv_duy_nhat_lech_so` giết 6 thay vì 5. Bảng “Chín chốt” đã ghi cột cuối là số đo trên **nguyên mẫu S10**, nên không dùng những số cũ ấy để nghiệm thu H. Các số nền 1582/1581 cũng thuộc nền lịch sử của đặc tả; phép sổ lấy nền lease thật ra 1804/1803. Không thấy tiêu chí nào buộc bỏ ba ca/mutant thêm để làm tổng quay về số cũ.

Mục 19 tiếp tục giữ lịch sử 18 lớp review và bổ sung lớp do executor phát hiện; không tuyên bố các lớp kế nhiệm đã vá. Việc duyệt băm r9 và nâng trần đã được PROMPT cung cấp, nên không yêu cầu hỏi lại. Những câu `proposed`, “chưa duyệt”, B4 chưa có của các mốc cũ không được dùng làm trạng thái LIVE mới. Bản thử theo README còn nguyên dòng trạng thái ADR r8 của H; sản phẩm r9 sau này phải điền lại metadata theo 8.1 trên băm/quyết định r9. Lượt này không chứng nhận N1 hoàn chỉnh cho một H-r9 chưa tồn tại.

### Trần và phạm vi bằng chứng

H và bản dựng r9 đều +443/−4 trên đúng 4 tệp. R9 bỏ backtick và thêm câu trên một dòng hiện có nên không làm tăng số dòng protocol; băm K01 cũng thay trên dòng có sẵn. Còn **7 dòng** tới trần 450; không có ngoại lệ kích thước được suy thêm. Con số +434 ở mục 10 được ghi rõ là nguyên mẫu lịch sử, không phải lời khai về H.

Lượt gọi này là **10/13 theo PROMPT** và quyết định nâng trần được cung cấp. Hai dòng opt-in của đặc tả được kiểm ở snapshot; riêng lịch sử API/lời gọi, comment nâng trần và mọi CI hiện thời chưa được đọc từ máy chủ. Không reset bộ đếm theo revision.

## NHỮNG GÌ KHÔNG ĐO ĐƯỢC

- Không chạy full `packet_loop_test.py` một tiến trình, 16 mảnh đầy đủ, full 2106-mutant audit, `tl.py --selftest`, Ruff hoặc Windows. Các kết quả chọn lọc chỉ chứng minh đúng tập đã nêu; không gán lại kết quả HANDOFF thành kết quả của reviewer.
- Không đo CI PR N13, full CI N14/K7, `kiem-merge` N15, hậu land N16, authority cấp lease thật hoặc readback GitHub. Không approve mã H, không cấp quyền push/merge/land.
- Không tạo phản chứng đường dẫn hoặc chuỗi thực thi độc hại mới. Các ca đường dẫn có sẵn được chạy nguyên qua bộ test; các hướng cần payload mới chỉ nằm ở phần giới hạn/mô tả.
- Các phép prefix dùng Markdown/comment thường và định nghĩa mask của cổng; không chứng minh renderer Markdown hoàn chỉnh, mọi HTML, race filesystem, hay toàn bộ containment trên Windows.
- Provider/họ reviewer theo identity Codex/OpenAI; executor họ Claude theo chỉ thị. `effort: high` là mức assignment của lượt này; model/effort backend thực phục vụ và session ID được máy xác thực: **KHONG_DO_DUOC**. Không suy model đã phục vụ từ model được yêu cầu trong spec. Assurance trong header là đề nghị nội dung, chưa thay receipt validator của điều phối.
- Sandbox thực là `workspace-write`, nguồn được giữ chỉ đọc bằng phạm vi thao tác; không khai kernel khóa riêng hai kho. Snapshot đầu/cuối gồm nội dung, kích thước, mtime, symlink, cả ignored/untracked; chỉ chứng minh không có delta giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

## HIỆN VẬT VÀ LỖI CÔNG CỤ ĐO ĐÃ PHÂN BIỆT

[setup.log](setup.log), [finish-setup.log](finish-setup.log), [spec.diff](spec.diff), [hash-independent.log](hash-independent.log), [content.log](content.log), [spans.log](spans.log), [measure.log](measure.log), [registry.log](registry.log), [scope-code.log](scope-code.log), [scope-test.log](scope-test.log), [mutants-new.log](mutants-new.log), [old-cases.log](old-cases.log), [adr-cases.log](adr-cases.log), [required-sets.log](required-sets.log), [old-mutants.log](old-mutants.log).

Các lỗi nháp của reviewer đã được sửa trước khi dùng số: fetch abbreviated OID không được Git nhận (dựng nền bằng OID đầy đủ đã có); bytes literal tiếng Việt không hợp lệ trong script probe; hằng regex scanner nằm ở module workflow; phép đếm con trỏ phải giới hạn hàng bảng, không tính ví dụ đoạn dẫn; placeholder trạng thái ADR là cả dòng; dòng nối của bất biến một chữ số thụt 3 dấu cách. Không lỗi nào trong số đó được báo thành finding của đặc tả. Bản script cuối và output chạy lại là bằng chứng dùng trong verdict. Trường `lượt đột biến=28` trong kết quả hàm của vòng mới đếm mutant mã; log còn nhánh mutant tệp test `t1466_fixture_ve_trung_tinh`, nên tổng bằng chứng là 29 dòng giết mutant, không phải 28 hoặc toàn bộ 2106.


Kiểm cuối: `SNAPSHOT 18950 18950 DELTA 0`; git status rỗng, HEAD/tree và băm đặc tả giữ nguyên. Python 3.13.18, git version 2.43.0. Không có tiến trình đo bắt buộc còn dang dở. [SHA256SUMS](SHA256SUMS) neo các script, log và verdict của lượt này.
