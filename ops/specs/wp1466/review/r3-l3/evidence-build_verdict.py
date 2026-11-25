from pathlib import Path
O=Path(__file__).resolve().parent
old=[
('F02.a — câu cắt scope không là vá','neo-thieu-nghia-vu','ĐÃ VÁ THẬT','Xóa đúng câu cũ ⇒ rc 9, K03; `probes.log: old_scope_cut`.'),
('F02.b — bảng nối slug','neo-thieu-nghia-vu','ĐÃ VÁ THẬT','Xóa đúng câu cũ ⇒ rc 9, K03; `old_slug_map`.'),
('F02.c — hai chuyển tiếp dưới 50%','neo-thieu-nghia-vu','ĐÃ VÁ THẬT','Xóa đúng câu cũ ⇒ rc 9, K05; `old_two_transitions`. Băm độc lập 7/7 khớp.'),
('F03 — INV-20 thiếu nợ','cong-khong-do-bat-bien','ĐÃ VÁ THẬT','INV-20 có `INV-20-CHI-DO-CHEP-NGUYEN-VAN`; 15/15 ô cổng có nợ; 24/24 tên trỏ nằm trong 26 mục Nợ. Không còn lời khai scanner đọc diễn đạt lại.'),
('F04 — vế branch/worktree §1(2)','thieu-truy-vet-yeu-cau','ĐÃ VÁ THẬT','Tự tách §1: 10/10 mục bằng chữ của dòng INV tương ứng; INV-02 có branch/worktree và nợ riêng. Ngoài §1 chỉ khai có con trỏ.'),
('F05.a — bảng bị tách bằng dòng trống','kiem-chuoi-khong-doc-cau-truc','ĐÃ VÁ THẬT','`old_table_split` rc 9/K01; thêm khoảng trắng giữa ô vẫn rc 0. Biểu hiện cũ này đã hết, nhưng lớp có biểu hiện mới F05.d/e bên dưới.'),
('F05.b — khai báo ca theo AST','kiem-chuoi-khong-doc-cau-truc','CHƯA VÁ','R3 §0/§14 bỏ bộ đọc ca khỏi wp1466, giao #1469; 18 tham chiếu có mặt không phải nghiệm thu bộ đọc AST.'),
('F05.c — nợ phải thuộc mục Nợ','kiem-chuoi-khong-doc-cau-truc','CHƯA VÁ','Giao #1469 / `INV-BANG-DOI-CHIEU-NGU-NGHIA`; cổng r3 chỉ đọc protocol, không đọc ADR để kiểm vị trí mục Nợ.'),
('F06 — containment tệp ca/cổng/ADR','duong-dan-chua-khep-trong-goc','VÁ HỜ','Tệp protocol có G1: ca liên kết trong/ngoài và mutant bỏ containment đã chạy. Ba loại tệp cũ không được đọc trong wp1466 nữa; phần ấy là nợ #1469, chưa có cổng để đo.'),
('F07 — nghiệm thu cutover kế nhiệm','moc-chuyen-tiep-mau-thuan','CHƯA VÁ','Không còn hai vị từ mâu thuẫn trong r3, nhưng r2 đã chữa câu chữ ấy. R3 bỏ toàn bộ hợp đồng vị từ, giao #1470; không có bộ kiểm/các ô thời gian mới được nghiệm thu.'),
('F08 — pass ở cuối hàm cũ sát khối chèn','tieu-chi-dong-xoa-khong-do-hanh-vi','ĐÃ VÁ THẬT','`n8.log`: old_boundary_pass rc 1, chỉ ra `_doc_nguon_protocol` đổi byte. Lớp vẫn mở do N8 mới cho phép gán lại tên cũ trong một phép gán nhiều đích.'),
('F10 — identity v2 đủ provider/surface/family','schema-bo-sot-provider-hop-le','CHƯA VÁ','Bốn tệp nguyên mẫu không có schema v2/consumer identity mới; toàn bộ chuyển #1470 / `INV-12-CONG-VERDICT-THEO-LOP`.'),
('F11.a — chuẩn hóa, case-fold, resolve','tien-kiem-lease-chua-du','ĐÃ VÁ THẬT','3b dùng I2(Đ); đọc `_bieu_dien_duong`, `_dich_trong_cay`, `_giao`; prefix/case-fold/NFC trả True; hai ca r812 được chạy nguyên trạng (lease-cases.log).'),
('F11.b — closure trước kiểm giao','tien-kiem-lease-chua-du','CHƯA VÁ','`coordination.log`: I2_CLOSURE_READER False; policy §5 không có trong cây. I2 chỉ hợp write_set/effective_write_set đã khai, không tự tính hay xác minh closure.'),
('F13 — đối chứng cùng họ do tên r1466','doi-chung-khac-ho-chon-nham-doctrine','ĐÃ VÁ THẬT','24 tên doctrine_inv_ thực sự chạy doctrine-scan. 17 mutant đều chọn đúng ba ca máy trạng thái; vòng thật 17/17 ok và TỔNG: ĐẠT.'),
('F14.a — neo trong rào mã','ma-tran-dem-doi-loi-thay-doi-mau','ĐÃ VÁ THẬT','Ca thật `doctrine_inv_khoi_trong_rao_ma`: mutant bỏ mask giết assertion; có trong nhóm 3 ca đích của inv_bo_che_khong_render.'),
('F14.b — neo trong comment HTML','ma-tran-dem-doi-loi-thay-doi-mau','ĐÃ VÁ THẬT','Ca thật `doctrine_inv_khoi_trong_comment_html` bị giết trong cùng vòng thật; lý do khóa K05 mất, không chỉ đổi chuỗi tổng output.'),
('F14.c — bảng trong rào mã','ma-tran-dem-doi-loi-thay-doi-mau','ĐÃ VÁ THẬT','Tái dùng công thức fixture tác giả r2: baseline rc 9/assertion đạt; bỏ mask vẫn đạt (KHÔNG tính là giết); bỏ K01 rc 0/assertion đỏ. Cơ chế mới bảo vệ bằng khóa tiểu mục. `f14.log`; không khai ca này nằm trong 24 ca giao nộp.'),
('F14.d — rào không đóng','ma-tran-dem-doi-loi-thay-doi-mau','ĐÃ VÁ THẬT','Ca thật đòi lý do “không được đóng”; mutant bỏ mask làm assertion đỏ dù HTML vẫn có thể làm rc 9. Vòng thật xác nhận nhóm G2 giết 3 ca.'),
('F15 — chuỗi thiếu nhánh integration/base','tach-packet-bo-dieu-kien-integration','VÁ HỜ','R3 đã thêm first-parent master + base chứa merge trước và câu C5/E5. ADR-0044/0053 vẫn đòi integration; quyết định được cấp chỉ là tách 3 packet, chưa có ngoại lệ C5. Không suy authority từ đề xuất.'),
('F16 — khóa hiệu đúng 40 trái quyền thêm ca','nghiem-thu-khoa-so-ca-trai-quyen-them','ĐÃ VÁ THẬT','N6 dùng T thực, tập bắt buộc ⊆ T và hiệu số = |T|; N7 áp mọi mutant mới. Hai sổ đo 1582→1606 và 1581→1605, cùng +24. T đủ 24 hoặc thêm tên thứ 25 không bị ràng buộc số 24 loại bỏ.')]
classes=[
('neo-thieu-nghia-vu','ĐÃ VÁ THẬT','0','Giới hạn luật ngoài bảy đơn vị đã khai; không suy đã khóa toàn protocol.'),
('cong-khong-do-bat-bien','ĐÃ VÁ THẬT','0','Đóng lỗi khai quá mức; không chứng nhận 15 cổng đã phủ toàn bất biến.'),
('thieu-truy-vet-yeu-cau','ĐÃ VÁ THẬT','0','Ngoài §1 chưa hứa phủ từng vế; không biến con trỏ thành độ phủ.'),
('kiem-chuoi-khong-doc-cau-truc','VÁ SINH LỖI MỚI','4 nhóm: tab; hàng INV khác cách viết; AST ca; mục nợ','Hai nhóm cuối chuyển #1469 / INV-BANG-DOI-CHIEU-NGU-NGHIA.'),
('duong-dan-chua-khep-trong-goc','VÁ HỜ','1 nhóm containment tệp kế nhiệm','#1469 / INV-BANG-DOI-CHIEU-NGU-NGHIA; Windows chưa đo.'),
('moc-chuyen-tiep-mau-thuan','CHƯA VÁ','1 nhóm nghiệm thu cutover','#1470 / INV-12-CONG-VERDICT-THEO-LOP; không còn lỗi hai câu ngược nhau ở r3.'),
('tieu-chi-dong-xoa-khong-do-hanh-vi','VÁ SINH LỖI MỚI','1 nhóm kiểm đích gán của N8','Pass biên hàm cũ đã bị chặn, nhưng thước mới còn lỗ.'),
('schema-bo-sot-provider-hop-le','CHƯA VÁ','1 nhóm identity v2','#1470 / INV-12-CONG-VERDICT-THEO-LOP.'),
('tien-kiem-lease-chua-du','VÁ HỜ','2 nhóm: closure; vòng phụ thuộc cấp lease','Hai nợ ở INV-02 không ghi việc thiếu closure; chưa chạy admission trên GitHub.'),
('doi-chung-khac-ho-chon-nham-doctrine','ĐÃ VÁ THẬT','0','Không phải lách selector: phân họ đúng hành vi thực, đối chứng độc lập đã đo.'),
('ma-tran-dem-doi-loi-thay-doi-mau','ĐÃ VÁ THẬT','0','Đo assertion/vòng thật; không cho điểm giết giả khi chỉ thông báo đổi.'),
('tach-packet-bo-dieu-kien-integration','VÁ HỜ','1 nhóm ngoại lệ integration chưa có authority','C5/E5 là câu hỏi hợp lệ, chưa là quyết định; E2 tách không thay C5.'),
('nghiem-thu-khoa-so-ca-trai-quyen-them','ĐÃ VÁ THẬT','0','Giữ tập bắt buộc; cho thêm tên đã khai; không chỉ kiểm tổng ≥24.')]
openrows=[
('kiem-chuoi-khong-doc-cau-truc','F05.b/c/d/e; 4 nhóm','P2','r1 925f851 → r2 69bf087 → r3 b007995','Đọc cấu trúc Markdown/khai báo, không suy cấu trúc từ dạng chuỗi hẹp','Tab K04–K07 rc 0; hàng INV không dấu cách/backtick rc 0; AST/nợ chờ #1469'),
('duong-dan-chua-khep-trong-goc','F06; 1 nhóm','P2','r1 → r2 → r3','Một hợp đồng containment cho mọi tệp được đọc ở #1469','G1 protocol đạt; ba loại tệp kế nhiệm chưa đọc/nghiệm thu'),
('moc-chuyen-tiep-mau-thuan','F07; 1 nhóm','P2','r1 → r2 → r3','Một vị từ và bộ ca biên thời gian trong #1470','R3 đã cắt lời hứa; không tính chuyển đi là vá'),
('tieu-chi-dong-xoa-khong-do-hanh-vi','F08.b; 1 nhóm','P2','r1 → r2 → r3','Kiểm từng binding của AST mới, đối chiếu từng tên cũ','Gán nhiều đích cùng giá trị vẫn qua N8'),
('schema-bo-sot-provider-hop-le','F10; 1 nhóm','P2','r1 → r2 → r3','V2 và consumer đầy đủ trong #1470','Không có mã v2/các ca identity để đóng'),
('tien-kiem-lease-chua-du','F11.b/c; 2 nhóm','P2','r1 → r2 → r3','Tách kiểm trước cấp với nhập lease đã công bố; làm rõ closure/authority','Không gọi record-lease lên nguồn; kiểm mã/hàm thuần và ca r812'),
('tach-packet-bo-dieu-kien-integration','F15; 1 nhóm','P2','mới r2 → r3','Nhánh theo canon hoặc ngoại lệ E5 có quyết định bền, nêu rõ phạm vi B4','C5 đang mở, không coi lời đề nghị là quyết định'),
('khoa-khong-neo-vi-tri-va-duy-nhat','F17.a/b; 2 nhóm: dời vị trí, nhân bản','P1','mới r3 b007995','Nhận diện đơn vị bằng vị trí/cấu trúc và cardinality rồi so băm','Dời K01/K04–K07; nhân đôi K04: đều rc 0'),
('moc-dot-bien-tu-khop-trong-khai-bao','F18; 1 nhóm','P2','mới r3 b007995','Mốc nhắm đoạn thực thi duy nhất; chạy ca kiểm mốc cùng tập nghiệm thu','Nền marker đạt, nguyên mẫu marker đỏ: t1466… khớp 2 chỗ')]
s='''verdict: changes_requested
reviewed_sha: b0079956d230ccb09b1c1d48f5a2633aaf09a173
spec_sha256: 7b6457fda836f740e0d491bd0940532107fa9b4518c0eadf93522e4eb46ee454
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop: 9, so_bieu_hien: 14, P0: 0, P1: 1, P2: 8, P3: 0}
hoi_tu: {U: 13, F: 6, ty_le: "6/13 = 46,15%", lop_moi: 2, lop_tai_mo: 0, lop_lan_thu_ba: [kiem-chuoi-khong-doc-cau-truc, duong-dan-chua-khep-trong-goc, moc-chuyen-tiep-mau-thuan, tieu-chi-dong-xoa-khong-do-hanh-vi, schema-bo-sot-provider-hop-le, tien-kiem-lease-chua-du]}

Review ĐẶC TẢ r3, không phải approval mã thi hành. SHA-256 đã kiểm đầu tiên và khớp cả tệp local lẫn blob tại reviewed_sha. Tree của reviewed_sha: `adf0abe3ff1368437ca16dc62b9010badb6a293f`. Base đo: `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. Cây thử ở `out/prototype/` là clone riêng, checkout base rồi áp nguyên patch r3; không gọi HEAD nền là commit ứng viên đã nghiệm thu. Mọi ghi nằm dưới `out/`; không push, không sửa cây được review, không gọi API ghi.

Các số chính tái lập được: **368 dòng thêm / 4 tệp; 7/7 băm độc lập; 15/15 ô cổng có nợ; 26 mục Nợ; 156/156 ca; 17/17 mutant mới và 21/21 mutant cũ đều `ok`, `TỔNG: ĐẠT`.** Tuy nhiên N9 đỏ ở ca kiểm tính duy nhất của mốc mutant. Cổng toàn vẹn còn nhận cấu trúc/vị trí sai, N8 còn nhận phép gán lại tên cũ, và tiền kiểm lease chưa khép hợp đồng §5.

Số P đếm **lớp**, số biểu hiện đếm 14 **nhóm** trong BẢNG LỚP (không nhân bốn lần thụt tab thành bốn nhóm). Bảng giữ cả nợ lịch sử chuyển #1469/#1470; điều này không đòi kéo công việc ấy trở lại wp1466. Phần chuyển đi đã có authority E2 theo chỉ thị của lượt review, có Issue và tên nợ, nhưng chưa được tính là vá theo §8.3. `assurance` ở đầu là mức đề nghị cho cặp reviewer–executor, không phải một approval hoặc quyền thi công/merge.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

Bảng sau đối chiếu đủ **21 nhóm biểu hiện** của 13 lớp còn mở cuối lượt 2. Một biểu hiện cũ có thể đã vá trong khi nhãn tổng của lớp là VÁ SINH LỖI MỚI. Nguồn cũ là `ops/specs/wp1466/review/r2-l2/VERDICT.md` tại `69bf08715d9bd43643b72f5a6da0d8daac174e67`.

| finding lượt 2 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
'''
s+=''.join('| '+' | '.join(r)+' |\n' for r in old)
s+='''
### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | phần chưa đo / chuyển #1469/#1470 (nợ tên gì) |
|---|---|---|---|
'''+''.join('| '+' | '.join(r)+' |\n' for r in classes)
s+='''
**Hội tụ:** F gồm `neo-thieu-nghia-vu`, `cong-khong-do-bat-bien`, `thieu-truy-vet-yeu-cau`, `doi-chung-khac-ho-chon-nham-doctrine`, `ma-tran-dem-doi-loi-thay-doi-mau`, `nghiem-thu-khoa-so-ca-trai-quyen-them`: **6/13 = 46,15%**. Không cộng hai lớp mới vào tử số. Ba lớp đã đóng ở r2 (`neo-sai-don-vi-khop`, `dem-khong-khai-tap-ca`, `doi-diem-goi-cong-chua-du-yeu-cau`) vẫn đóng: 7/7 đơn vị khớp, sổ đăng ký/Linux phân biệt đúng, entrypoint thật gọi chốt mới. **0 lớp tái mở.**

Có sáu lớp còn mở đã xuất hiện cả r1, r2, r3, liệt kê ở `hoi_tu`. Ngoài ra, hai chuyển tiếp r1→r2 = 3/12 = 25% và r2→r3 = 6/13 = 46,15% đều dưới 50%. Cả hai điều kiện checkpoint của §12 đã đạt. Đây là dữ liệu để **phiên đang giữ việc dừng vá và xét lại cách làm**, ghi căn cứ vào revision/handoff; không tự phát sinh câu hỏi chủ kho. Việc ghi sổ `xet_lai_cach_lam` theo ADR-0067 do phiên có quyền ghi Issue thực hiện; reviewer này chỉ ghi verdict theo assignment.

Không tách/gộp hay đổi tên lớp cũ. F17 là lỗi **nhận diện vị trí/số lượng** của thiết kế khóa mới, khác F01 cũ (chọn sai đơn vị làm chính văn bản chuẩn không khớp). F18 là lỗi **tính duy nhất mốc** trong artifact, khác F14 (đếm thay đổi output thành assertion bị giết).

## BẢNG LỚP

Mọi lớp còn mở, gồm nợ kế nhiệm; cách xử lý theo phạm vi ghi riêng, không hợp thức hóa việc cắt scope thành đóng lớp.

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
'''+''.join('| '+' | '.join(r)+' |\n' for r in openrows)
s+='''
## BẢNG SĂN

Lệnh chạy từ thư mục làm việc của lượt review. `rc` trong log là của lệnh/ca được đo; `rc=0` của script tổng hợp không thay rc của từng phản chứng.

| hướng độc lập | lệnh | output thật | kết luận |
|---|---|---|---|
| 1. OID, băm, trần, drift master | `python -B out/measure.py` | HASH `7b6457…`; SHALLOW false; ABBREV 7; OPT_IN 0055/0053 `[0,128] True`; MASTER_COMMITS 14; MASTER_DIFF 4 tệp | Băm đúng; master không chạm tập đo; opt-in hợp lệ trong snapshot |
| 2. Ma trận INV/nguồn/nợ, băm độc lập | cùng lệnh; `out/blocks.log` từ script Python kiểm khối/AST | INV 28; GATES 15; WITH_DEBT 15; DEBTS 26; REFERENCED_DEBTS 24; 10 dòng INV_SOURCE True; LOCK K01…K07 mỗi cái 1 | Ba lớp khai quá mức/thiếu vế/neo thiếu nghĩa vụ cũ đã sửa |
| 3. Phản chứng cũ và vị trí khóa | `python -B out/probes.py` | old_scope_cut/slug_map/two_transitions rc 9; old_table_split rc 9; relocate_K01/K04–K07 rc 0; duplicate_K04 rc 0 | Câu cũ đã khóa; F17 mới |
| 4. Cấu trúc Markdown | cùng lệnh; `python -B out/rows_probe.py` | tab_indent_K04…K07 rc 0; canonical 9; no_space 0; plain_id 0 | F05 vẫn có hai nhóm mới |
| 5. Giới hạn sửa bằng AST/byte | `python -B out/n8_probe.py`; `python -B out/n8_matrix.py` | clean ma/test 0; old_boundary_pass 1; same_value_chained_binding 0; NEGATIVE_MATRIX 12 12; POSITIVE_MATRIX 2 2 | N8 dùng được nhưng chưa chứng minh toàn hợp đồng |
| 6. Vòng mutant mới thật | `python -B out/run_review.py new_mutants` | nền 26/26, BỎ QUA 0; 17 dòng ok; TỔNG: ĐẠT; process rc 0 | F13 và phép đo mới của F14 có bằng chứng thật |
| 7. Hồi quy họ doctrine | `python -B out/run_review.py cases`; `python -B out/run_review.py old_mutants` | CASES_RESULT 156 156 {}; nền 132/132; 21 dòng ok; TỔNG: ĐẠT; cả hai process rc 0 | S10/S11 đúng trong tập đã chạy |
| 8. Gate bị bỏ khỏi tập 156 | `python -B out/run_review.py adr_cases`; `python -B out/more_measure.py base` | nguyên mẫu 41 ca: 40 đạt, marker đỏ; nền marker None (đạt); mốc t1466… khớp 2 chỗ | F18; không đọc 156/156 thành N9 đạt |
| 9. Bốn biểu hiện F14 | `python -B out/f14_recheck.py` và log vòng mutant mới | table baseline 9/assertion True; without_mask 9/True; without_K01 0/False; G2 ba ca thật bị giết | Không cho điểm giết giả đối với bỏ mask của bảng; có mutant K01 làm assertion đỏ |
| 10. Lease toàn snapshot | `python -B out/leases.py` | LEASE_COUNTS 544 15 10 5; B4 wp1462-r8-g2-claude; POLICY_FILE_EXISTS False | B4 vẫn giữ hai .py; không phải bằng chứng được cấp lease wp1466 |
| 11. I2(Đ), closure và CI | `python -B out/coordination.py`; `python -B out/lease_cases.py` | I2_CLOSURE_READER False; PREFIX/CASE/NFC True; cả 4 CI_PR chay; CI_PUSH chay; hai ca r812 đạt | Chuẩn hóa có thật, closure chưa có; đường CI có consumer |
| 12. N6/N7, selector và target | `python -B out/more_measure.py prototype` | REGISTER 1606; LINUX 1605; TARGET_COVERAGE 24 24; mọi control là ba ca máy trạng thái; mutant mới 16 mốc một chỗ, 1 mốc hai chỗ | Đổi tiền tố đúng phân họ, không che việc test chạy doctrine; phát hiện riêng mốc trùng |

Log chính: [measure.log](measure.log), [blocks.log](blocks.log), [probes.log](probes.log), [rows-probe.log](rows-probe.log), [n8.log](n8.log), [n8-matrix.log](n8-matrix.log), [new-mutants.log](new-mutants.log), [old-mutants.log](old-mutants.log), [cases.log](cases.log), [adr-cases.log](adr-cases.log), [more-base.log](more-base.log), [more-prototype.log](more-prototype.log), [f14.log](f14.log), [leases.log](leases.log), [coordination.log](coordination.log), [lease-cases.log](lease-cases.log).

## BẢNG ĐO

Các phép đo chạy ngày 21-11-2026 UTC trên snapshot được giao. `measure.log` ghi mốc bắt đầu `2026-11-21T00:24:16.449729+00:00`. Số lịch sử cần GitHub/ảnh chụp tại thời điểm khác được tách khỏi số đo snapshot.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| r3 SHA-256 / commit / tree | chỉ thị đầu lượt | đúng đầu verdict; blob và local bằng byte | có |
| r2 verdict SHA-256 | 500fc4d9…55be16 | đúng đầy đủ băm trong spec | có |
| mirror / abbrev | đầy đủ / 7 | shallow false / 7 ở cây nguồn và clone riêng | có |
| ref snapshot | prompt 386; S1 lịch sử 384 tên nhánh | 386 ref origin **kể cả HEAD**, 385 nhánh không tính HEAD | khác đơn vị/thời điểm; không kết luận ảnh lịch sử sai |
| master so base | 010046f, 14 commit, 4 tệp ngoài tập đo | 14; `ops/ci_provenance_test.py` và ba hồ sơ `ops/reviews/pr1467-review-9-codex/{VERDICT.md,run.json,stdout.log}` | có |
| hai opt-in ADR | rc 0/128/0 mỗi OID | cat-file 0/128, OID có trong first-parent | có trong mirror; độ mới remote trực tiếp chưa đo |
| ADR nền / lớn nhất | 66 / 0067 | 66 / 0067 | có |
| ref có ADR ≥0068 | 0/384 thời điểm S3 | 0/385 nhánh snapshot | có về không tranh số trong snapshot |
| lease | 543 / 14 còn hạn / 9 tombstone / 5 hiệu lực | snapshot 544 / 15 / 10 / 5, phân hạn tại 00:11:44Z; có bản wp1236 r10 mới | không tái dựng được snapshot lịch sử; 5 hiệu lực và B4 vẫn đúng |
| B4 | wp1462-r8-g2-claude giữ hai .py | đúng; hạn 24-11 08:00Z; thêm prefix hồ sơ của chính B4 | có |
| người giữ bốn đường wp1466 | 0·0·1·1 theo phép định vị thô | như vậy; hai số 1 cùng B4 | có, không dùng làm admission |
| INV / phân loại | 28 = 15 + 12 + 1 | đúng | có |
| ô cổng có nợ | 15/15 | 15/15, gồm INV-20 | có |
| mục Nợ / tên được trỏ | 26 / 24 | 26 / 24, không tên trỏ nào vắng | có |
| tham chiếu ca | 18 | 18/18 có hàm/tên đăng ký trong AST | có về tồn tại; không nhận là phủ toàn vị từ |
| mười mục §1 chép nguyên văn | 10 | 10/10 bằng sau nối dòng/NFC | có |
| khóa | 7, gồm 5 khối + 2 tiểu mục | tự băm độc lập, mỗi băm khớp đúng một đơn vị ở bản nguyên vẹn | có; không chứng minh vị trí/cardinality trên bản sửa |
| sáu khối mới / hai khối cũ | mỗi mới 1, cũ 0 | mới base 0 → prototype 1; cũ 1 → 0; ba mốc N8 nền mỗi cái 1 | có |
| ADR / protocol / mã / test | 135; +46−2; +72−1; +115−1 | đúng từng tệp | có |
| tổng kích thước | 368 / 4 | 135+46+72+115=368; 4 tệp, tổng xóa 4 | có, dưới trần 6/450; không tính 704 dòng spec vào PR mã |
| tập ca mới | 24 = 17 rc9 + 1 rc6 + 3 KĐĐ + 3 xanh | đúng 24 tên; 24/24 đạt, không bỏ qua; được gọi trong tập 156 và nền vòng mutant 26 | có |
| tập mutant mới | 17 = 16 mã + 1 test | 17; 17 dòng ok; các số giết đúng G1–G7; 24/24 ca mới có target | có |
| số giết các mutant | 1,3,1; 1,3,2; 7×1 và16; 1;20,2 | từng tên và số đều khớp new-mutants.log | có |
| vòng mới | nền 26/26, 17/17 ok, TỔNG: ĐẠT | đúng, process rc 0; wrapper báo 16 lượt suite vì mutant test chạy tiến trình riêng | có; không nhầm số suite callback với số mutant |
| hồi quy họ doctrine | 132+24 =156/156 | 156/156 | có |
| mutant cũ | 21/21 ok | nền132/132; 21/21 ok, TỔNG: ĐẠT, process rc0 | có |
| adr_song và kiểm mốc N9 | 40 ca ADR + marker phải đạt | 40/40 ADR đạt; **marker đỏ** ở prototype, xanh ở base | **không** |
| N8 script | 47 dòng không trống, hai chế độ đạt | 47; cả hai đạt trên nguyên mẫu | có |
| N8 phản chứng | 12 ngoài phạm vi đỏ, 2 hợp lệ đạt | reviewer dựng 12 biến thể cùng loại: 12 đỏ; 2 đối chứng hợp lệ xanh; thêm phép gán nhiều đích ngoài hợp đồng vẫn xanh | con số đúng không đủ đóng lớp |
| sổ ca / Linux | 1582 /1581 nền | nền1582/1581; prototype1606/1605; lệch mỗi cây đúng wp1174_windows_claim_rejected | có |
| MUTANTS | nền1864, thêm17 | 1864→1881 | có |
| doctrine-scan / adr-song | prototype rc0 /67 ADR | nền rc0/12 tệp và66 ADR; prototype rc0/12 tệp và67 ADR | có |
| băm log tác giả | e5292f88…86bd;3674cd7d…56e | tệp được giao khớp băm; reviewer chạy lại bằng script riêng | có; không dùng băm làm thay phép chạy |
| các vector sáu vị trí | mọi dòng S5 và bảng đọc cổng | từng vector tái lập, in đầy đủ ở measure.log | có |
| INV-23 match | 1·2·8·6·1·0, 15 dòng sau chưa đọc | đúng vector; reviewer đọc cả 15: KeyboardInterrupt/label nội bộ/nhãn Windows CI, không thêm cổng nguồn authority | có về giới hạn |
| biên nhận | 352 /0 bang_lop | 352 /0 | có |
| call site doctrine | 4 adapter; 1 lệnh trong CI;21 chỗ CLI trong test | 4 tệp adapter, 1 CI command,21 dòng test | có |
| 4 tệp khác /14 dòng nhắc doctrine | 4 /14 | bốn tệp ops được xét:3+3+7+1=14; thêm idiom_py_test và tl_selftest chỉ chứa ví dụ/chú thích | đúng phạm vi định vị, không là inventory toàn repo |
| pre-push | full gate chỉ cho refs/heads/master | nhánh `if master_sha is not None and not run_full_gate(...)` đúng như khai | có |
| 23 điểm audit /16 lớp lịch sử | 23 /16 | ma trận A1–A3, B1–B15, C1–C5 đủ23; mục19 có16 slug | có về kiểm kê, không chứng nhận hết từng vấn đề audit |
| KN-0/KN-1 | #1469/#1470 có authority tách | theo chỉ thị và bản chép E2; không có lease hai packet trong mirror | authority được cấp làm tiền đề; không phải đã thi công |
| ruleset, Issue trạng thái, ls-remote lịch sử | sáu check, active/open, các số theo giờ | không có readback GitHub tương ứng trong mirror | KHÔNG ĐO ĐƯỢC |
| full suite, Ruff, Windows, CI H, hậu land | tiêu chí tương lai /chưa chạy | không chạy toàn suite; không có Ruff; không Windows/CI/live | KHÔNG ĐO ĐƯỢC, không phải passed |

### L3, L6 năm vế và khả năng nghiệm thu trên H

(a) dương mới/âm cũ; (b) nối dòng hoặc exact blob; (c) từng vị trí; (d) chữ/chữ số; (e) đủ sáu vị trí cổng.

| tiêu chí | L3 / phép đỏ | L6(a–e), kết luận |
|---|---|---|
| N1 | So byte ADR và sáu giá trị thay thế; đổi byte/số là đỏ | (a) có; (b) exact blob ghim băm; (c,e) sáu số riêng; (d) không regex lượng bằng chữ. Dòng Accepted phải có authority thật, khớp mẫu không tạo approval. |
| N2 | Sáu khối, vị trí, hai khối cũ và numstat | (a) mới1/cũ0 đã đo; (b) exact blob; (c) mỗi khối/mốc riêng; (d,e) không áp vì không đếm lượng văn xuôi/khai 0 cổng. |
| N3 | Bỏ dòng ADR §20 làm adr-song đỏ | Hai chiều66→67; không regex mới. Nợ lịch sử0016 vẫn được gate khai. |
| N4/N5 | Mất/sửa khóa làm rc9; băm tự tính lệch làm đỏ | (a) có nhưng chỉ với các biến thể đã xét; (b) NFC/nối dòng **làm mất nghĩa indentation tab**; (c) xét có mặt trong tập, **không định vị/đếm đúng một**; (d) băm toàn đơn vị không regex số; (e) không áp. F05/F17 chặn kết luận toàn vẹn. |
| N6 | Đủ tên bắt buộc, delta đúng T, không skip, tất cả đạt | (a,c) tập ID, không thay bằng N/N tổng; (b,d,e) không áp. T thêm tên thứ25 vẫn hợp lệ; một tên bắt buộc thiếu thì đỏ dù tổng đủ. Full suite/16 mảnh chưa chạy. |
| N7 | Vòng thật đòi target chết, control sống, không tín dụng giả | Đã chạy trên mã áp patch. 17/17 ok không bao gồm ca kiểm marker của N9; không đánh đồng hai tiêu chí. |
| N8 | Chạy script nhúng trên hai blob base/H | Có âm/dương và đo được trên mã thật. Counter các source segment chặn sửa thân cũ; kiểm tên gán nhiều đích bị sai (F08). Không phải số hunk nữa. |
| N9 | Ca cũ hoặc marker đỏ, mutant cũ sống là đỏ | **Đã đỏ** ở marker. 40 ADR/132 doctrine/21 mutant xanh không bù được marker. |
| N10 | Ruff F delta=0 | Không có Ruff trong môi trường, chưa đo; không suy từ import/test xanh. |
| N11 | Selftest N/N và diff --check | Diff --check đo riêng; full selftest chưa chạy. Là gate cũ, không phải lời hứa một regex mới. |
| N12 | 4 đường đúng, ≤450 dòng thêm | Đếm mỗi tệp và tổng thật368; ràng buộc spec4 tệp chặt hơn trần ADR6. Không lấy 368 dự đoán mã H sau B4. |
| N13/N14/N15 | Required jobs không thiếu/skipped; audit đúng H; kiem-merge không THIẾU | Đo được khi có H/CI/readback; hiện chưa có. Các vector grep không thay gate. Windows miễn phải có dòng chủ kho neo H. |
| N16 | Đọc log hậu land theo job và mutant mới | Người đo/thời điểm/nguồn đã khai. Classifier hiện tại trả chay trên push master; không thấy mâu thuẫn thiết kế kiểu job bị bỏ qua. Chưa land nên không khai đạt. |

L6(e) được làm trên đủ sáu tệp, từng số riêng; mọi lần dùng “0 cổng” còn phải đọc mã, không suy chỉ từ không khớp regex. Mười lăm dòng label/assignee/board mà người soạn chưa đọc đã được đọc trong lượt này. L6(d) không được dùng để yêu cầu khóa băm phải chịu thay nội dung bằng chữ số: đây là hợp đồng exact normalized unit, không một regex tìm lượng.

### Authority, L7, trần và phối hợp

- E2 tách ba packet là tiền đề đã được chủ kho cấp theo chỉ thị review. R3 **đã cắt** đúng hai hợp đồng rộng khỏi lời hứa wp1466, ghi rõ #1469/#1470 và hai nợ trong ADR. Mục19 không khai chuyển đi là vá. Đây là sửa scope có authority, không chứng cứ đóng F05.b/c, F06, F07, F10.
- C5 **đúng là việc chủ kho quyết**, và gắn E5 là phù hợp: nó đổi tuyến tích hợp/thẩm quyền so canon. Nhưng §5 cùng ADR-0044/0053 không tự sinh ngoại lệ “ngoài Mission thì dùng master”. R3 vẫn gọi đó là cách đọc của người soạn; C5 chưa được trả lời. B4 là packet thuộc Mission #1172, nên câu “cả chuỗi nằm ngoài Mission” cũng không đủ chính xác. Không nhập authority E2 tách vào authority E5 đổi tuyến.
- Không thấy điểm hỏi chủ kho mới ngoài E1–E5. C1/C4/C5 nằm trong phạm vi đổi luật/thẩm quyền E5; C3 và thiếu công cụ/trần là E2. Các điểm dừng kỹ thuật không được biến thành hỏi chủ kho nếu không thuộc mã E. Hai điều kiện checkpoint đã đạt ở lượt này, nhưng tự chúng không buộc hỏi.
- 4 tệp/+368 nằm dưới trần opt-in ADR-0053; không cần khối nâng trần cho nguyên mẫu này. ADR-0055 opt-in hợp lệ trong snapshot; không suy một ngân sách review spec độc lập chưa có quy tắc vào trần PR. Không dùng kích thước nhánh sổ sách làm kích thước PR mã.
- B4 r8/g2 còn giữ hai .py; wp1466 chưa được thi công. Base sau B4 phải đo lại sáu neo và ba mốc, diff cuối/numstat/các suite phải nghiệm thu lại. Chưa có diff B4 cuối thì không thể chứng nhận nguyên mẫu hiện tại áp nguyên vẹn lên base tương lai.
- #1460 snapshot là r7/B1a, không có lease. Bốn tệp dự kiến của nó gồm workflow full audit, ci_dang_ky_test.py và hai hiện vật hợp đồng: **không giao trực tiếp** bốn tệp wp1466. Nó thay đường full audit mà N14 tiêu thụ, nên evidence sau này phải theo workflow thật của đúng H. Hiện ci_dang_ky_test.py còn do wp1236 r10 giữ; không suy #1460 được chạy chỉ từ không giao wp1466.

'''
(O/'VERDICT.md').write_text(s)
print('WROTE',len(s.splitlines()),'lines; findings details next')
