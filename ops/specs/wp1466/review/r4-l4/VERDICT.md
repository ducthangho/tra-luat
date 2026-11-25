verdict: changes_requested
reviewed_sha: 937d135d903fe71a1660b138ebb2234cbc10bdbc
spec_sha256: d248c37823e4b07a89fcc652b79c345e375337beeb5f76e21db719f6f64d4b13
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: 3, so_bieu_hien_mo: 5, P0: 0, P1: 0, P2: 3, P3: 0, so_lop_no_ke_nhiem: 4}
hoi_tu: {U: 9, F: 3, ty_le: "3/9 = 33,33%", lop_moi: 0, lop_tai_mo: 0, lop_lan_thu_tu: [kiem-chuoi-khong-doc-cau-truc, duong-dan-chua-khep-trong-goc, moc-chuyen-tiep-mau-thuan, tieu-chi-dong-xoa-khong-do-hanh-vi, schema-bo-sot-provider-hop-le, tien-kiem-lease-chua-du]}

Review ĐẶC TẢ r4, không phải approval mã thi hành. Băm đã được kiểm **đầu tiên**, khớp tệp được giao; sau đó so tiếp với blob tại reviewed_sha, bằng byte. Tree: `005cba332fa093792eaecd6ff22678c3ecfe25ad`. Nguyên mẫu được tự dựng trong `out/prototype/`: clone mirror, checkout đúng `48d372e14f190dae83a75ccbca8ee9a0b25635c5`, `git apply -p1` patch r4. Không gọi HEAD của bản sao ấy là H giao nộp đã nghiệm thu.

**Các số chính khớp:** 395 dòng thêm/4 tệp; 31 ca mới/18 đột biến; 27 nợ ADR; 164/164 ca và 40/40 `adr_song_*`; nền vòng mới 34/34, 18/18 đột biến mới và 21/21 đột biến cũ `ok`, `TỔNG: ĐẠT`; ma trận N8 `ma` 12 đỏ + 1 đạt, `test` 6 đỏ + 1 đạt. Nhưng phản chứng độc lập ngoài ma trận cho thấy băm vẫn chuẩn hoá byte và N8 vẫn bỏ sót gán tên cũ. Nợ tiền kiểm lease chưa có Issue kế nhiệm để đủ điều kiện chuyển sang bảng (ii).

P0–P3 đếm **lớp trong bảng (i)**; 5 biểu hiện là 2 nhóm mất byte, 1 nhóm binding của N8, 2 nhóm tiền kiểm lease. Bảng (ii) có 4 slug/5 nhóm biểu hiện; một slug (`kiem-chuoi-khong-doc-cau-truc`) có các biểu hiện khác nhau trong cả hai bảng, không cộng trùng nó thành hai lớp trong lịch sử. Không tách, gộp hay đổi tên slug. Model/effort thực phục vụ và ID phiên không có bằng chứng runtime để đo: `KHONG_DO_DUOC`; không suy từ model yêu cầu trong đặc tả. Assurance ở đầu chỉ là mức đề nghị, không phải approval hay quyền thi công/merge.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

Đối chiếu trước khi kết luận: đủ **14 nhóm biểu hiện của 9 lớp** còn mở cuối r3, nguồn `b0079956d230ccb09b1c1d48f5a2633aaf09a173`. Băm verdict r3 tự tính lại: `c12b80e93a6bdc84787dfbc087006f967a119d1c8acba3eb90ae2535c3bb4a6d`. Nhãn một biểu hiện đã hết không có nghĩa cả lớp đã đóng.

| finding lượt 3 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
| F05.b — khai báo ca theo AST | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | R4 §0/§6/§14/§19 bỏ hợp đồng bộ đọc ca, nêu #1469 và tên nợ. Nguyên mẫu chỉ đọc protocol, không có bộ đọc AST ca. Đây là chuyển phạm vi, không phải vá. |
| F05.c — nợ phải ở mục Nợ | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Tự đếm 25/25 tên trỏ thuộc 27 nợ trong ADR; đó là đo dữ liệu hiện tại. Cổng không mở ADR để kiểm vị trí nợ; phần ấy chuyển #1469. |
| F05.d — thụt tab K04–K07 | kiem-chuoi-khong-doc-cau-truc | ĐÃ VÁ THẬT | `probes_r4.py`: thụt tab từng K01–K07 đều rc 9. Lớp còn biểu hiện mới F05.f/g về byte; xem finding. |
| F05.e — hàng INV không cách/backtick | kiem-chuoi-khong-doc-cau-truc | ĐÃ VÁ THẬT | `id_plain`, `id_compact`, `id_canonical` đều rc 9/nằm ngoài tiểu mục; đối chứng `id_debt` rc 0. Vòng thật: bỏ G8 giết 3; thu về dạng chuẩn giết 2. |
| F06 — containment tệp cổng/ca/ADR kế nhiệm | duong-dan-chua-khep-trong-goc | CHƯA VÁ | Ba loại tệp không được cổng wp1466 đọc; §0 và §19 giao rõ #1469. G1 của tệp protocol duy nhất: chạy lại hai ca liên kết sẵn có, đạt; mutant bỏ chốt giết 1. Không nhận phép đo G1 này là vá ba loại tệp đã chuyển đi. |
| F07 — nghiệm thu vị từ chuyển tiếp | moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Không có vị từ hay bộ ca cutover trong bốn tệp nguyên mẫu. §0/§14/§19 giao toàn bộ cho #1470. Bảng hiệu lực ADR chỉ định thời điểm, không còn hợp đồng vị từ kế nhiệm. |
| F08.b — gán nhiều đích có tên cũ | tieu-chi-dong-xoa-khong-do-hanh-vi | ĐÃ VÁ THẬT | N8 gán chuỗi, gán bộ, import đè tên đều rc 1; `pass` biên hàm cũ cũng rc 1. Phản chứng mới F08.c gán trong phần định nghĩa hàm/lớp vẫn rc 0. |
| F10 — lược đồ identity v2 | schema-bo-sot-provider-hop-le | CHƯA VÁ | Không có schema/consumer v2 mới trong patch; §0/§14/§19 bỏ lời hứa và giao #1470. Chưa có mã để nghiệm thu identity của packet ấy. |
| F11.b — closure trước cấp lease | tien-kiem-lease-chua-du | CHƯA VÁ | `coordination_r4.py`: `POLICY_EXISTS False`, `CLOSURE_READER False`; raw matcher trả False cho prefix, case và effective-only. R4 tự ghi chưa có packet nhận nợ. |
| F11.c — I2 đòi lease đã đăng | tien-kiem-lease-chua-du | VÁ HỜ | R4 đã bỏ gọi I2 làm tiền kiểm và khai đúng giới hạn `ai-dang-giu`. Đọc `_verify_lease_ref`: I2 vẫn cần lease/ref đã công bố; không có phép tiền kiểm tương đương trước công bố. Chuyển nghĩa vụ thành rủi ro người cấp lease chưa đóng biểu hiện. |
| F15 — thiếu authority đổi tuyến integration | tach-packet-bo-dieu-kien-integration | ĐÃ VÁ THẬT | Đối chiếu §0/§1/D8 với quyết định E5 được cung cấp: đúng ba Issue #1466/#1469/#1470, không gồm B4; first-parent master và base chứa merge trước được ghi đủ. B4 vẫn thuộc Mission #1172. |
| F17.a — dời khóa khỏi vị trí | khoa-khong-neo-vi-tri-va-duy-nhat | ĐÃ VÁ THẬT | Tự băm địa chỉ+đơn vị 7/7 khớp; dời K01 và K02/K04–K07 đều rc 9. Mutant bỏ địa chỉ giết ca đích, đối chứng sống. |
| F17.b — nhân bản khóa | khoa-khong-neo-vi-tri-va-duy-nhat | ĐÃ VÁ THẬT | Nhân K01 dưới cùng tổ tiên, nhân K02/K04–K07 ngoài vị trí đều rc 9; mutant bỏ duy nhất giết 1, mutant lệch số giết 3. Bản sao trong rào mã được ca xanh kiểm đúng ngoại lệ đã khai. |
| F18 — mốc tự khớp trong khai báo | moc-dot-bien-tu-khop-trong-khai-bao | ĐÃ VÁ THẬT | Tự đếm 18/18 mốc mới khớp đúng 1 nơi; marker test đạt trong 164 ca và trong nền 34/34. Mutant tệp test còn giết 2 ca, 3 đối chứng sống. |

### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | VÁ SINH LỖI MỚI | F05.f/g: mất CR và khoảng trắng cuối mục; F05.b/c: AST ca/mục nợ | (i) cho f/g vì wp1466 vẫn hứa băm byte; (ii) cho b/c vì có đủ cắt lời hứa, tên nợ, #1469. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ | Containment ba loại tệp kế nhiệm | (ii), đủ ba điều kiện; không tái mở G1 protocol đã đo. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Hợp đồng/bộ ca cutover | (ii), toàn bộ #1470; không yêu cầu wp1466 thi công thay. |
| tieu-chi-dong-xoa-khong-do-hanh-vi | VÁ SINH LỖI MỚI | F08.c: binding bị bỏ qua trong DEF | (i), N8 là tiêu chí wp1466. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ | Identity v2 và consumer | (ii), toàn bộ #1470. |
| tien-kiem-lease-chua-du | VÁ HỜ | F11.b/c: closure; tiền kiểm trước công bố | (i), chưa có Issue kế nhiệm/authority giao nợ; điều kiện cấp lease của chính wp1466 vẫn chạm tới việc này. |
| tach-packet-bo-dieu-kien-integration | ĐÃ VÁ THẬT | 0 | Đã có E5 đúng phạm vi; không ở bảng mở. |
| khoa-khong-neo-vi-tri-va-duy-nhat | ĐÃ VÁ THẬT | 0 | Địa chỉ và cardinality thật sự đổi màu; không ở bảng mở. |
| moc-dot-bien-tu-khop-trong-khai-bao | ĐÃ VÁ THẬT | 0 | Mốc duy nhất, ca marker đã vào tập nền; không ở bảng mở. |

**Hội tụ:** F = {`tach-packet-bo-dieu-kien-integration`, `khoa-khong-neo-vi-tri-va-duy-nhat`, `moc-dot-bien-tu-khop-trong-khai-bao`} ⇒ **3/9 = 33,33%**. Không cộng nợ kế nhiệm vào F. Không có slug mới hay lớp đã đóng bị tái mở; các biểu hiện mới thuộc hai lớp vẫn mở từ r3. Sáu slug đã có mặt cả bốn lượt nằm trong `hoi_tu`; việc chuyển packet không xóa lịch sử đó. Chuyển r2→r3 là 6/13, r3→r4 là 3/9, đều dưới 50%; checkpoint sau r3 đã được chỉ thị xác nhận, reviewer này không tự đăng sổ hay phát sinh câu hỏi chủ kho.

Chín lớp đã đóng trước r4 được soi lại và chưa thấy tái mở: bảy băm chuẩn và ba ca xóa câu cũ giữ `neo-sai-don-vi-khop`/`neo-thieu-nghia-vu`; bảng 15 ô cổng có nợ và 10 nguồn nguyên văn giữ `cong-khong-do-bat-bien`/`thieu-truy-vet-yeu-cau`; hai sổ đăng ký giữ `dem-khong-khai-tap-ca`; lời gọi CLI thực và mutant bỏ lời gọi giữ `doi-diem-goi-cong-chua-du-yeu-cau`; vòng mutant thật/đối chứng giữ `doi-chung-khac-ho-chon-nham-doctrine`/`ma-tran-dem-doi-loi-thay-doi-mau`; N6/N7 vẫn theo tập bắt buộc cộng tập thêm thực, giữ `nghiem-thu-khoa-so-ca-trai-quyen-them`.

**Cách đọc §8.3:** đồng ý tách lịch sử lỗi khỏi tập quyết định approval của packet như chỉ thị lượt này. Giữ nguyên bốn nhãn; không gọi chuyển phạm vi là vá. Chỉ chuyển biểu hiện sang (ii) khi đủ ba điều kiện đã giao. Chính vì vậy F11 không được đưa vào (ii): nợ có tên nhưng chưa có Issue nhận nợ. Không có finding phản đối cách đọc §8.3.

## BẢNG LỚP (i) — lớp MỞ của wp1466

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.f: universal-newline ở 7 khóa; F05.g: rstrip ở K01/K03 — 2 nhóm | P2 | r1 925f851 → r2 69bf087 → r3 b007995 → r4 937d135 | Bảo toàn biểu diễn byte khi định vị/băm; chỉ bỏ đúng các dòng biên được hợp đồng loại | 7 ca CRLF + 2 ca dấu cách vẫn rc 0; 7 ca xóa và 7 ca tab rc 9. |
| tieu-chi-dong-xoa-khong-do-hanh-vi | F08.c: thiếu binding thực thi khi định nghĩa hàm/lớp — 1 nhóm | P2 | r1 → r2 → r3 → r4 | Ngữ pháp nút mới đóng hoặc phân tích phạm vi thực thi đầy đủ, cùng một quy tắc cho hai chế độ | Default/decorator đều qua cả `ma` và `test`; lớp có global qua `ma`; compile và bytecode xác nhận binding. |
| tien-kiem-lease-chua-du | F11.b/c: closure; tiền kiểm trước công bố — 2 nhóm | P2 | r1 → r2 → r3 → r4 | Tiền kiểm thực hiện nghĩa vụ còn thiếu, hoặc successor có Issue và authority đúng phạm vi | Phép đo raw trung thực nhưng yếu hơn §5; chưa chạy admission/GitHub, chưa có packet nhận nợ. |

## BẢNG LỚP (ii) — nợ kế nhiệm có authority

| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c: đọc khai báo ca theo cấu trúc, vị trí mục nợ | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0 nêu đích danh rồi bỏ hợp đồng; §6 ngoài phạm vi; §14 không đặt thiết kế/tiêu chí; N1–N16 không kiểm consumer ngữ nghĩa này. |
| duong-dan-chua-khep-trong-goc | F06: containment tệp ca/cổng/ADR | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0/§19 chỉ giữ G1 cho protocol; hàm mới không mở ba loại tệp ấy. |
| moc-chuyen-tiep-mau-thuan | F07: vị từ và nghiệm thu cutover | #1470 | INV-12-CONG-VERDICT-THEO-LOP | §0/§14/§19 không kê vị từ chuyển tiếp; bảng hiệu lực giao việc định hình cho packet sau. |
| schema-bo-sot-provider-hop-le | F10: schema v2/identity | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Không schema v2/consumer identity trong patch hay các tiêu chí wp1466; §0/§19 ghi toàn bộ lớp thuộc kế nhiệm. |

Authority E2 của #1469/#1470 và E5 về nhánh nhận lấy từ bản chép quyết định trong chỉ thị và đặc tả. Không truy cập, không tự xác nhận nội dung URL từ GitHub. Bảng (ii) không có nghĩa nợ đã được sửa, cũng không tự cấp lease cho hai packet đó.

## BẢNG SĂN

Lệnh từ thư mục làm việc được giao. Các script ở ngay cạnh verdict; log là kết quả chạy của lượt này. Rc 0 của runner không thay rc riêng của phản chứng. Các thử nghiệm tự dựng dùng biến đổi định dạng và gán lại chính giá trị hiện hành, không tạo payload đường dẫn hay chuỗi độc hại; ca liên kết dùng nguyên ca tác giả cung cấp.

| hướng độc lập | LỆNH | OUTPUT THẬT | kết luận |
|---|---|---|---|
| 1. Băm/OID/ref/drift/trần | `python -B out/measure_r4.py` | `BLOB_EQUALS True`; `SHALLOW_ABBREV false 7`; `REFS_TOTAL 388`, `BRANCHES 387`; 17 commit/110 đường đổi; `MEASURED_PATHS_CHANGED []`; mỗi opt-in `0 128 True` | Không drift trên tập đo; trần đúng trong snapshot. |
| 2. Dữ liệu và đơn vị khóa, parser byte độc lập | cùng lệnh | `INV_COUNTS 28 15 15 12 1 18 DEBTS 27 REF_DEBTS 25 MISSING []`; 10 `INV_SOURCE True`; 7 `LOCK … MATCH True`; `PROTO_EXACT_RECONSTRUCTION True` | Băm chuẩn, nội dung bảng và sáu phép sửa tái lập được. |
| 3. Địa chỉ/cardinality và giá biên tập | `python -B out/probes_r4.py` | `relocate_K01` và mọi relocate/duplicate khối: rc 9; `duplicate_K01_same_ancestor` rc 9; `insert_block_before_K04/K05` rc 9; `append_unlocked_note` rc 0 | F17 đóng; giá thứ tự khối khai đúng và có thể chấp nhận trong phạm vi đã chọn. |
| 4. Băm byte và dạng bảng | cùng lệnh | `SUMMARY 48 MISMATCH` gồm 7 `crlf_inside_K*` và `trailing_space_K01/K03`, đều rc 0; tab/xóa/ba dạng ID đều rc 9, tên nợ rc 0 | F05 có biểu hiện còn mở; sự tương đương còn bị nhận ngoài lời khai. |
| 5. Thước N8 trên mã nguyên mẫu | `python -B out/n8_run.py` | `DECLARED_MATRIX ma RED 12 GREEN 1 EXPECTED_MATCH 13 13`; `test RED 6 GREEN 1 EXPECTED_MATCH 7 7`; clean cả hai rc 0 | Tái lập số tác giả; không đồng nghĩa N8 đủ. |
| 6. Binding lúc định nghĩa/decorator | cùng lệnh; `python -B out/extra_checks.py` | Default/decorator ở cả hai chế độ rc 0; class-global `ma` rc 0; `MODULE_OLD_STORES` tăng 1→2, class có `STORE_GLOBAL`; thêm decorator cho hàm cũ rc 1 | F08.c. Biến thể annotation compile lỗi nên không dùng làm bằng chứng bypass hành vi. |
| 7. Vòng đột biến mới và tính duy nhất mốc | `python -B out/auditor/run.py new_mutants`; `python -B out/auditor/markers.py` | nền 34/34/BỎ QUA 0; đủ 18 `ok`, `TỔNG: ĐẠT`, rc 0; mọi mốc `count=1` | F18 đóng; số giết G1–G9 khớp. |
| 8. Hồi quy ca và mutant cũ | `python -B out/auditor/run.py cases`; `… adr_cases`; `… old_mutants` | 164/164; 40/40; nền 132/132, 21 `ok`, `TỔNG: ĐẠT`; rc 0; 0 skip | Bộ đã chọn đạt, không khai full suite đạt. |
| 9. Lease/toàn ref và closure | `python -B out/coordination_r4.py` | `LEASE_COUNTS 545 15 11 4`; exact True, prefix/case/effective-only False; policy/closure False; B4 giữ hai `.py` | 3b trung thực nhưng F11 chưa đủ điều kiện chuyển nợ. |
| 10. Consumer CI và phối hợp | `python -B out/extra_checks.py` | 4 `CI_PR … chay`; `CI_PUSH … chay`; 4 adapter, 1 workflow call; #1460 write set 4 tệp không giao trực tiếp | Có consumer thật; B4 phải đi trước; #1460 ảnh hưởng evidence N14 về sau. |
| 11. Ruff F độc lập | `python -B out/ruff_delta.py` | `ruff 0.16.9`; nền/ứng viên mỗi bên 16 lỗi, rc1; `STABLE_DELTA_NEW []`, `STABLE_DELTA_REMOVED []` | N10 delta=0; so code/message/phạm vi hàm/dòng nguồn, loại riêng số dòng F811 bị dịch. |
| 12. Sáu vị trí cổng và phạm vi authority | `python -B out/measure_r4.py`; đọc §0/§1/§11/§12/§14/§17 cùng ADR-0034/0044/0053/0060/0062/0067 | 30 vector trong `measure.log`, từng vị trí riêng; `VECTOR_CANDIDATE_ADR [0,15,0,0,0,0]`; C5 chỉ 3 Issue, B4 loại rõ | Không mở rộng quyết định E5; luật đang hiệu lực là ADR-0060/0062. |

Log: [measure.log](measure.log), [probes.log](probes.log), [n8.log](n8.log), [coordination.log](coordination.log), [extra.log](extra.log), [new_mutants.log](auditor/new_mutants.log), [old_mutants.log](auditor/old_mutants.log), [cases.log](auditor/cases.log), [adr_cases.log](auditor/adr_cases.log), [counts.log](auditor/counts.log), [markers.log](auditor/markers.log). [results.json](auditor/results.json) ghi test IDs và băm log; probe Ruff trong đó chỉ là `python -m ruff`, phép đo CLI bổ sung ở [ruff-delta.log](ruff-delta.log). Phần output dài được giao `tl_auditor` chạy/tiêu hoá theo `CLAUDE.md` mục Quy trình sửa code (5); phiên chính đã đọc lại kết quả và log, tự làm phản chứng/đối chiếu và quyết verdict.

## BẢNG ĐO

Đo 21-11-2026 UTC. `measure.log` ghi giờ thực chạy; lease được phân hạn tại đúng 01:19:07Z mà S4 dùng. Không dùng snapshot để suy hiện trạng GitHub sau thời điểm chụp.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| Spec/blob/hash | r4/937d135/d248c378… | đầy đủ ở đầu verdict; local=blob | có |
| Verdict r3 | c12b80e9…4a6d, 9 lớp/P1 1/P2 8 | băm đúng, bảng mở 9 lớp | có |
| Lịch sử lớp | 18 | 18 slug trong §19; U lượt 3=9 | có |
| Audit nguồn / ma trận §15.2 | 62 dòng / 23 điểm | blob a8affd58 đọc rc0/62 dòng; 23 hàng A1–C5 trong ma trận, small-counts.log | có |
| Mirror/abbrev/ref | đầy đủ/7; S1 387 nhánh | không shallow/7; 388 ref origin kể cả HEAD, 387 nhánh | có; “388 nhánh” trong prompt khác đơn vị |
| Master so base | e02d748, không chạm tập đo | 17 commit/110 đường; giao tập đo rỗng | có |
| Opt-in 0055/0053 | 0/128/0 mỗi OID | cat-file 0/128, có trên first-parent | có offline; chưa đo độ mới server |
| ADR nền / số cao nhất / tranh số | 66/0067; 0/387 | 66/0067; 0/387 | có |
| Lease S4 | 545/15/11/4 | 545 blob-path/15 còn hạn/11 bia mộ hai chiều/4 hiệu lực | có |
| Write set wp1466 đang bị giữ | 0/0/1/1 | đúng, hai số 1 cùng wp1462-r8-g2-claude, hạn 24-11 08:00Z | có; chưa được thi công |
| Biên nhận nền | 352; 0 có bang_lop | 352; 0 | có |
| Vector §3/S5 và bảng cổng | số riêng 6 vị trí | toàn bộ vector đã chạy trong measure.log, khớp từng số | có |
| ADR / protocol / mã / test | 143; +46/−2; +74/−1; +132/−1 | đúng từng số, 4 tệp, tổng +395/−4 | có |
| Trần sensitive | ≤6 tệp/≤450 dòng thêm | 4/395, còn 55 dòng so trần | có cho nguyên mẫu, không cấp ngoại lệ H tương lai |
| Bảng INV | 28=15 cổng+12 kỷ luật+1 chưa đo; 18 trỏ ca | đúng; cả 15 ô cổng có nợ | có |
| Nợ | 27; 25 tên được bảng trỏ | 27/25, không tên trỏ thiếu | có |
| Nguồn §1 | 10 mục chép nguyên văn | 10/10 bằng sau nối dòng của chính mục | có |
| Bảy khóa | 7 bộ bốn, mỗi địa chỉ một mục | parser riêng ra 7/7 địa chỉ và băm byte khớp | có trên văn bản chuẩn; byte biến thể còn lỗi |
| Sáu khối protocol / ba mốc N8 | mỗi neo 1 | 6/6 neo một lần; ráp lại protocol bằng byte; 3/3 mốc một lần | có trên base đo |
| N8 script | 92 dòng không trống | 92; bằng byte tệp do_pham_vi.py kèm hồ sơ | có |
| CASES / Linux | nền 1582/1581, thêm 31 | 1582→1613 / 1581→1612; khác đúng wp1174_windows_claim_rejected | có |
| MUTANTS | nền 1864, thêm 18 | 1864→1882; không tuple cũ nào đổi | có |
| Tập bắt buộc | 31 ca, 18 mutants; 31 ca có đích giết | đủ tên; 31/31 được nhắm, không mất ca cũ | có |
| Vòng mới | nền34/34, 18/18 ok | 34/34; 0 skip; 18 ok/3 đối chứng sống mỗi mutant; TỔNG: ĐẠT/rc0 | có |
| Số ca giết từng mutant | G1–G9, K01–K07 | lần lượt 1,2,1,1,1,1,3,3,2,24; K=4,1,3,1,5,2,1; fixture=2 | có; JSON lưu từng tên |
| Vòng cũ | nền132/132, 21/21 ok | đúng, TỔNG: ĐẠT/rc0, 0 skip | có |
| Ca tổng chọn / ADR | 164/164; 40/40 | đúng, không missing/skip/fail | có |
| N8 ma/test | 12 đỏ+1 đạt / 6 đỏ+1 đạt | đúng, clean cả hai đạt | có với ma trận khai; ngoài ma trận còn lỗ |
| Mốc mutant | duy nhất | 18/18 đúng 1; ca kiểm mốc nằm trong nền | có |
| Băm log tác giả | mu:8c8a1a…; cu:8e719e… | khớp hồ sơ đã giao; số liệu được chạy lại độc lập | có |
| Caller doctrine-scan | 4 adapter/1 workflow/21 chuỗi CLI trong test | 4/1/21 | có |
| Gate thật | rc0; 67 ADR sau thay đổi | nguồn rc0/66; nguyên mẫu rc0/67; cùng quét 12 adapter | có |
| Cưỡng chế ADR ứng viên | N1–N6 điền trên H | nguyên mẫu đếm 0·15·0·0·0·0; tệp ADR thử còn điền 0 ở cả sáu dòng | chưa nghiệm thu N1; đây là placeholder cây thử, không lời khai H đã đạt |
| Ruff F | tác giả chưa đo nền | Ruff CLI 0.16.9: nền 16/ứng viên 16; F841=3, F401=8, F541=2, F811=3; delta ổn định 0 | có, N10 delta=0; bare lint cả hai rc1 vì nợ nền |
| Ruleset/sáu required checks/Issue open/remote cặp ref | các lần REST tại giờ nêu trong spec | không có readback server của lượt review | KHÔNG ĐO ĐƯỢC trực tiếp |

Wrapper vòng mới đếm 17 lượt gọi trong module gốc; mutant thứ 18 thay tệp test rồi nạp module riêng. Có đủ 18 dòng `ok`, gồm fixture giết 2; không lấy số callback 17 làm số mutant thực chạy.

### kiem-chuoi-khong-doc-cau-truc [P2] Lời hứa băm byte vẫn nhận hai dạng chuẩn hoá ngoài hợp đồng

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:393`, `:399`, `:401`, `:431`; nguyên mẫu `out/prototype/.claude/dev/packet_loop.py:1740` và `:1752`.

**VẤN ĐỀ:** R4 sửa tab và dạng hàng INV, nhưng vẫn mất thông tin trước khi băm. F05.f: `Path.read_text(encoding="utf-8")` dùng universal-newline; thêm CR trước một LF ở trong từng K01–K07 bị chuyển về LF, nên CLI vẫn rc 0. F05.g: `.rstrip()` trên TRỌN mục bỏ cả dấu cách cuối **dòng có nội dung**, không chỉ các dòng trống cuối mà hợp đồng cho bỏ; thêm một dấu cách cuối K01 hoặc K03 cũng rc 0. Đây là cùng cơ chế nhận dạng tương đương trước khi kiểm khóa của lớp F05, nên giữ slug cũ, không sinh lớp mới để reset lịch sử.

Điều này bác trực tiếp “mọi đơn vị là BYTE nguyên”, “đổi một byte là đỏ” và các hệ quả ở §8.3. Cổng EOL/diff-check khác có thể bắt một số biến thể nhưng không làm phép băm này đúng. Không cáo buộc thay đổi ngữ nghĩa luật đã qua toàn bộ pipeline: phản chứng chứng minh lời hứa toàn vẹn byte chưa được thực hiện.

**GỢI Ý VÁ:** dữ liệu gợi ý là giữ nguyên bytes/newline khi đọc và xác định lát cắt, chỉ loại đúng các dòng biên đã định nghĩa. Thêm ca cho byte ở giữa khối lẫn cuối dòng cuối mục; nếu chọn nới hợp đồng thì phải khai rõ giới hạn thay vì tiếp tục nói không chuẩn hoá.

**ĐÃ THỬ NGHIỆM:** `python -B out/probes_r4.py`: 48 phép thử, 9 lệch kỳ vọng gồm 7 CRLF và 2 dấu cách; mỗi biến thể thực sự đổi SHA-256 tệp. Đối chứng: xóa K01–K07 đỏ; thụt tab K01–K07 đỏ; dời/nhân bản đỏ; thêm ghi chú ngoài khóa xanh. Parser độc lập tính băm trên văn bản chuẩn khớp 7/7. Không sửa mã sản phẩm.

**ĐỘ TIN:** cao.

### tieu-chi-dong-xoa-khong-do-hanh-vi [P2] N8 bỏ sót binding của default và decorator khi gặp nút DEF

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:483`, `:492`, `:497`; khối được chép nguyên byte ra `out/n8_spec.py`.

**VẤN ĐỀ:** `gan(n)` trả ngay `{n.name}` cho FunctionDef/AsyncFunctionDef/ClassDef và không xét phần được thực thi lúc định nghĩa. Giá trị mặc định và decorator của hàm mới có thể gán tên cũ ngay ở module. Trong chế độ `ma`, một hàm `_inv_*` đặt đúng vị trí với phép gán lại `RC_ADR` ở default hoặc decorator vẫn được N8 in `ĐẠT`; trong chế độ `test`, tương tự với `ROOT`. Class mới tên `_inv_*` có binding `global` trong thân cũng qua `ma`, dù hợp đồng phần mới chỉ kê hằng và hàm. Việc thân các hàm cũ còn nguyên AST không bảo đảm các tên mà chúng tra còn được giữ nguyên.

Phản chứng chỉ gán lại **chính giá trị cũ**, không làm hỏng cổng hay thực thi module ứng viên. Compile/bytecode độc lập xác nhận hai dạng hàm hợp lệ và có thêm STORE_NAME của tên cũ ở module (1→2); class có STORE_GLOBAL trong code định nghĩa. Vì N8 không kiểm giá trị của binding bị bỏ qua, cùng đường cú pháp đó không được ràng buộc giữ giá trị; đây là giới hạn cấu trúc của thước, không phải đoán lỗi qua tên hàm.

**GỢI Ý VÁ:** giới hạn nút mới bằng danh sách dạng cú pháp được phép, hoặc duyệt đầy đủ các phần chạy trong phạm vi module lúc định nghĩa, kể cả decorator/default/class. Cùng một quy tắc áp vào hai chế độ. Không đề nghị một blacklist tên hay thêm từng ngoại lệ cho từng phản chứng.

**ĐÃ THỬ NGHIỆM:** `python -B out/n8_run.py` tái lập toàn bộ 13+7 biến thể khai trong §18, tất cả đúng màu; gán nhiều đích cũ bị chặn. Ngoài ma trận: default/decorator của hàm mới rc 0 ở cả `ma` và `test`, class-global rc 0 ở `ma`. Thêm decorator cho **hàm cũ** rc 1: không kết luận mọi decorator đều lọt. `python -B out/extra_checks.py` compile và kiểm bytecode, không thực thi. Biến thể annotation tuy N8 nhận nhưng compile lỗi vì future annotations, nên **loại khỏi bằng chứng bypass hành vi**; biến thể except bị chặn cũng không tính là finding.

**ĐỘ TIN:** cao.

### tien-kiem-lease-chua-du [P2] Thu hẹp lời khai chưa chuyển được nghĩa vụ tiền kiểm sang packet có authority

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:59` (3b), `:238` (nợ ADR), `:636` (đề xuất packet), `:742` (lịch sử); protocol §5 (`cay-kho/docs/PROTOCOL_DA_PHIEN.md:327`).

**VẤN ĐỀ:** 3b nay mô tả đúng năng lực `ai-dang-giu`: so đúng chuỗi khai trong `write_set`. Tôi không báo lại lỗi khai sai phép đo đã được sửa. Phần chưa vá là F11.b/c: closure/chuẩn hoá trước so giao và phép kiểm trước công bố lease. Protocol §5 vẫn đòi dispatcher tính effective write set rồi kiểm giao **trước cấp**; đọc tay write set rồi gánh rủi ro không mô tả cách hoàn tất các bước còn thiếu. Bốn điều kiện bắt đầu của chính wp1466 vẫn dùng phép tiền kiểm này.

R4 đặt tên `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE` nhưng ghi rõ **CHƯA có packet nào được giao**. Theo điều kiện phân bảng của chỉ thị lượt 4, thiếu Issue kế nhiệm thì biểu hiện ở bảng (i), không được coi đã vá hay nhập nhờ authority E2 của #1469/#1470. Đây không phải yêu cầu kéo nợ của hai packet đã được duyệt trở lại wp1466; nợ này chưa thuộc hai packet ấy.

**GỢI Ý VÁ:** hoặc có quy trình tiền kiểm đủ nghĩa vụ với bằng chứng/điều kiện fail-closed được nêu, hoặc định danh successor và authority chuyển phần này rõ ràng. Không suy ngoại lệ §5 từ việc thu hẹp lời khai. Phần đã chuyển hợp lệ có thể tiếp tục giữ nhãn CHƯA VÁ trong lịch sử, như bảng (ii).

**ĐÃ THỬ NGHIỆM:** `python -B out/coordination_r4.py` tái lập S4 chính xác 545/15/11/4; matcher exact=True, prefix/case/effective-only=False; policy closure không tồn tại và mã không đọc nó. Đọc `_verify_lease_ref` xác nhận I2 cần lease/ref đã công bố; không gọi lệnh cấp/nhập lease. Toàn bộ §0/§14/§19 đều không gán nợ này cho một Issue. Chưa đo admission GitHub, không cáo buộc đã cấp lease trái phép.

**ĐỘ TIN:** cao về mã, phạm vi và điều kiện chuyển nợ; quyết định authority có thể bổ sung chỉ thuộc phiên được giao việc đó.

## L3, L6, L7, trần và phối hợp

- **L1/L2/L4/L5:** số ca đăng ký và ca Linux tách đơn vị; bốn mục tiêu chiếu vào bốn tệp. Lịch sử 18 slug và U=9 không reset. Các số snapshot đã đo lại; số H sau B4, remote và hậu-land chưa có thì không gọi là đạt. Numstat H thực vẫn phải đo lại, không dùng 395 làm quota được cấp trước.
- **L3:** các G1–G9 và N4/N5/N7 có đối chứng/đột biến thật. N8 có ma trận thật nhưng còn mù ở F08.c; M3 còn mù ở F05.f/g. N1/N2 là đối chiếu byte/khối; protocol tự ráp khớp byte. N6 vẫn dùng T thực, tập bắt buộc là tập con, không khóa đúng 31 và cho phép thêm ca. N13–N16 là bằng chứng CI/merge/hậu-land tương lai, không dùng suite local thay thế.
- **L6(a):** có vế dương trên bảy khóa chuẩn và vế âm bằng xóa/dời/sửa; không coi chỉ vắng chữ cũ là đạt. **(b):** r4 chọn khóa blob bằng băm, chủ ý đỏ khi ngắt dòng lại; chính lựa chọn này cần bảo toàn byte và còn lỗi F05. **(c):** 7 địa chỉ được kiểm riêng, mỗi cái có cardinality; đã thử dời/nhân bản. **(d):** số dạng chữ không áp dụng cho grammar ID cố định `INV-NN` và băm; không có lời hứa bắt mọi diễn đạt ngôn ngữ tương đương. **(e):** đã đo riêng đủ sáu vị trí cổng; các số chỉ đo lần nhắc, không chứng minh đủ ngữ nghĩa. Nợ cổng được giữ rõ.
- **L7/authority:** không ngân sách mềm, không tự thêm mốc hỏi sau N lượt. Checkpoint là phiên tự xét lại theo ADR-0067. Các câu cần chủ kho quyết có E2/E5; `pham_vi_e` khai E5/không E4; không dùng uỷ quyền thường trực để tự freeze/merge packet này. ADR-0054 đã đóng băng; ADR-0060 theo ADR-0062 là luật merge. Các OID opt-in 0053/0055 hợp lệ trong mirror; quy tắc áp budget cho review đặc tả không gắn PR vẫn là giới hạn tác giả đã khai, không tự coi lượt này nâng/reset bộ đếm.
- **C5/B4:** quyết định E5 chép đúng và chỉ gồm #1466/#1469/#1470; B4 theo Mission #1172. Lease B4 đang giữ đúng hai tệp `.py`; điều kiện first-parent+base chứa merge trước giữ thứ tự. Sáu neo/ba mốc và toàn bộ counts/gates phải đo lại trên base thực sau B4; nguyên mẫu hiện tại không chứng minh khả năng áp nguyên vẹn trên diff B4 cuối.
- **#1460:** đọc trực tiếp spec r7/B1a từ ref snapshot `origin/ops/wp1460-r1`. Bốn tệp PR của nó không giao trực tiếp write set wp1466, nhưng thay `ci-dot-bien-du.yml` mà N14 tiêu thụ. Evidence sau này phải đọc theo workflow/job thật của đúng H; không dùng log cũ của một workflow khác. Snapshot không có lease #1460; `.claude/dev/ci_dang_ky_test.py` hiện do wp1236 r10 giữ.
- **Giá địa chỉ:** chèn đoạn trước K04/K05 thật sự đỏ; ngoài vùng khóa thêm ghi chú vẫn xanh. Đây là chi phí đã khai nhất quán trong ADR/§8.3/D3, không phải finding. Trần 395/450 còn chỗ nhưng không chứng minh mọi bản sửa tương lai đều nằm trong trần.

## Những gì KHÔNG đo được và giới hạn review

Không chạy Windows; không có waiver exact-H, full CI, `full_mutant_audit` từ GitHub, `kiem-merge`, canary N16 sau land hay mã giao nộp sau B4. Không chạy toàn bộ 1612 ca Linux hay `scripts/tl.py --selftest`; chỉ xác nhận các tập đã liệt kê. `python -m ruff` không có module, nhưng tìm được binary `ruff` trong PATH và đã đo N10: cả hai rc1/16 lỗi nền, delta=0. Không coi bare lint là rc0 và không khai đã kiểm pin/probe contract CI. Không kiểm ruleset live/bypass actors/branch protection, trạng thái Issue hay độ mới ref qua server. Các quyết định E2/E5/checkpoint là sự kiện được chỉ thị cung cấp, không phải dữ kiện remote tôi tự xác minh.

ADR nguyên mẫu cố ý `Proposed (cây thử, chưa duyệt)` và còn placeholder số cưỡng chế; chưa đạt N1 cho H, không được dùng nó làm Accepted hoặc chứng cứ đã có authority. 0·15·0·0·0·0 là số đo của cây nguyên mẫu, chưa phải giá trị cho H sau này. Hai lượt mutant là chọn tập, không là full mutant audit.

Mọi script, bản sao và output tạo trong lượt này nằm dưới `out/`; không push, không sửa nhánh nguồn, không dùng API GitHub ghi. `git status` nguồn đầu/cuối sạch đối với tracked/untracked; HEAD/tree và băm spec cuối khớp đầu. Nguồn có một file ignored `launcher.cpython-313.pyc` mtime 01:22:28Z; không có manifest ignored đầu lượt để chứng minh lịch sử toàn bộ workspace, nên không khai phép snapshot đầy đủ §8.2 đã đạt. Mọi lượt Python của review dùng `-B`/tắt bytecode; file ignored không bị dọn hay chỉnh. Sandbox thực là workspace-write với chỉ thị review chỉ ghi `out/`, không phải mount nguồn cưỡng chế read-only.

Lỗi setup của parser độc lập lần đầu (chưa che tiêu đề trong rào mã) đã sửa trong script scratch rồi chạy lại. Lỗi ấy không dùng làm finding hay bằng chứng đạt. Biến thể annotation không compile và warning escape có sẵn của test cũng không dùng để tính lỗi sản phẩm. Các giới hạn này không xóa ba finding P2 có bằng chứng nêu trên.
