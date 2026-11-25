verdict: changes_requested
reviewed_sha: 69bf08715d9bd43643b72f5a6da0d8daac174e67
spec_sha256: d25a0c2445ebeff97d94381ed24d998d23d6a9e792ba4db2cdd23108a7a6f64c
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop: 13, so_bieu_hien: 21, P0: 0, P1: 4, P2: 9, P3: 0}
hoi_tu: {U: 12, F: 3, ty_le: 3/12 = 25%, lop_moi: 4, lop_tai_mo: 0}

Review ĐẶC TẢ r2, tiếp tục lần chạy bị ngắt; không phải review mã giao nộp. Băm được kiểm đầu tiên và khớp; HEAD/tree là `69bf08715d9bd43643b72f5a6da0d8daac174e67` / `36df108a0bee3af05d2d9cc2d434472f123dc9ab`; base `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. Chỉ ghi dưới `out/`, không sửa kho hoặc gọi API ghi. Phép đo lần chạy trước của chính reviewer được giữ và đối chiếu với script, không lấy lời khai người soạn làm kết quả. Các phép xác minh bổ sung của lần tiếp tục nằm trong `followup.log` và `remaining.log`.

Các số cấu trúc lớn tái lập được: 28 INV, 23 mục nợ, 14/14 neo khớp một đơn vị, protocol +46/−2, mã +79/−1, fixture +18/−1. Tuy nhiên còn lỗi độ phủ, phép kiểm hình dạng diff, và nghiệm thu đột biến. Một số phần r1 đã sửa hợp đồng nhưng chỉ còn trong đề xuất kế nhiệm, chưa đủ bằng chứng đóng lớp theo yêu cầu §8.3 của lượt này.

Số hạng P đếm lớp; số biểu hiện đếm các nhóm ở BẢNG LỚP, không nhân theo số lần câu lỗi xuất hiện. Không gộp/tách slug cũ. Lớp mới không vào F; hai lần chạy của cùng lượt 2 không thành hai lượt review. Tỷ lệ này chưa tạo hai chuyển tiếp <50% và chưa tự kích hoạt checkpoint ba lượt.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

| finding lượt 1 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
| F01 | neo-sai-don-vi-khop | ĐÃ VÁ THẬT | Tự tính băm và phân đơn vị trên cây áp nguyên mẫu: N01–N14 mỗi neo đúng 1 đơn vị; 14 băm khớp. Xóa từng neo rc 9, chỉ đúng nhãn tương ứng. Sáu neo sai đơn vị cũ đã được thay bằng hợp đồng khả thi. `measure.log`, `probes.log`. |
| F02 | neo-thieu-nghia-vu | VÁ HỜ | Bốn biểu hiện cũ đã có N04/N09/N11/N12, xóa riêng đều đỏ. Nhưng xóa riêng luật cắt scope không là vá, bảng nối slug, hoặc điều kiện hai chuyển tiếp <50% vẫn rc 0. Cùng cơ chế chọn thiếu nghĩa vụ. `coverage-probe.log`. |
| F03 | cong-khong-do-bat-bien | VÁ HỜ | Sáu ô cũ: INV-04/06/13/15/16 ghi nợ, INV-05 đổi sang survey. Quét cả 15 ô: INV-20 còn không có nợ dù bảng đọc cổng tự nhận chỉ n-gram/không đo diễn đạt lại; protocol §8.3 giữ nợ scanner. 18 tên ca có mặt không chứng minh 18 ca đo đủ vị từ. |
| F04 | thieu-truy-vet-yeu-cau | VÁ HỜ | Đủ 23 dòng A1–C5 và các nhóm thiếu cũ được ánh xạ. Tuy vậy §1(2) có HAI nghĩa vụ, INV-02 chỉ mang giao write set, bỏ branch/worktree riêng; ma trận 15.1 vẫn khai phủ mọi bất biến §1. `WORKTREE_IN_TABLE False`, `BRANCH_IN_INV02 False`. |
| F05 | kiem-chuoi-khong-doc-cau-truc | VÁ SINH LỖI MỚI | HTML được chặn KĐĐ; ca/nợ chuyển KN-0 có hợp đồng AST/mục Nợ. Cổng mới gom mọi dòng bắt đầu bằng `\|` trong tiểu mục: chèn dòng trống giữa từng hàng, bảng Markdown bị tách, nhưng rc 0 và băm giữ nguyên. `probes.log`. |
| F06 | duong-dan-chua-khep-trong-goc | VÁ HỜ | Resolve protocol đã có kiểm và nguyên mẫu có đối chứng trong/ngoài gốc. Tệp ca/cổng/ADR chỉ còn hợp đồng KN-0, chưa có ca nghiệm thu của packet được cấp; không tính chuyển phạm vi là đóng. |
| F07 | moc-chuyen-tiep-mau-thuan | VÁ HỜ | Mâu thuẫn câu chữ cũ đã hết: cả ADR và KN-1 chọn start ≥ T, bảng bốn ô F/F/T/T. Cổng/các ca cutover chuyển KN-1 chưa giao; các ca thiếu thời gian/T và mutant chưa có. Giữ mở phần chuyển kế nhiệm, không cáo buộc r2 còn hai vị từ. |
| F08 | tieu-chi-dong-xoa-khong-do-hanh-vi | VÁ HỜ | Thêm `pass` vô hại vào cuối hàm cũ liền trước khối chèn: AST hàm cũ đổi, số hunk vẫn 3→3, numstat +81/−1. `n8-counterexample.diff`, `probes.log`. |
| F09 | dem-khong-khai-tap-ca | ĐÃ VÁ THẬT | 1582 tên đăng ký duy nhất, 1581 Linux, lệch đúng `wp1174_windows_claim_rejected`; S8/N6 tách đúng hai tập; lỗi đơn vị r1 đã hết. Điều kiện khóa hiệu đúng 40 là mâu thuẫn mới, ghi F16 riêng. `measure.log`. |
| F10 | schema-bo-sot-provider-hop-le | VÁ HỜ | Đã bỏ “v1 cộng khóa”, yêu cầu enum đóng và AG trong KN-1. V2 theo đủ hợp đồng r2 chưa được giao; nguyên mẫu trong bundle không phải chứng cứ kiểm mọi provider/surface/family theo r2. Q4 rời ADR không được tính là vá. |
| F11 | tien-kiem-lease-chua-du | VÁ HỜ | 3a so cặp tên/SHA hai chiều; 3b có prefix. Tái lập 541/13/7/6 và B4 giữ hai tệp. Nhưng 3b thiếu case-fold và resolve/closure theo §5; phép giao chuỗi chưa chứng minh giao effective write set. `leases.log`, `probes.log`. |
| F12 | doi-diem-goi-cong-chua-du-yeu-cau | ĐÃ VÁ THẬT | Chính doctrine-scan bản nguyên vẹn rc 0; bỏ §8.3 rc 9 với 7 neo vắng. 132/132 ca họ doctrine trên nền và prototype đạt, 21 mutant cũ giữ phân hạng. Lỗi lựa chọn đối chứng mới ghi riêng vì cơ chế khác. |

### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | phần chưa đo / chuyển kế nhiệm (có nợ tên gì) |
|---|---|---|---|
| neo-sai-don-vi-khop | ĐÃ VÁ THẬT | 0 | Đóng lỗi thiết kế matcher, không chứng nhận implementation tương lai |
| neo-thieu-nghia-vu | VÁ HỜ | 3 nghĩa vụ chưa được neo | Các câu nói ngược là giới hạn khác đã khai, không dùng làm finding này |
| cong-khong-do-bat-bien | VÁ HỜ | INV-20 | Không có `còn nợ` tương ứng trong 23 mục nợ ADR |
| thieu-truy-vet-yeu-cau | VÁ HỜ | branch/worktree riêng của §1(2) | Không thấy nợ có tên cho phần này |
| kiem-chuoi-khong-doc-cau-truc | VÁ SINH LỖI MỚI | bảng bị tách; ca AST; nợ theo mục | Hai phần cuối: KN-0, `INV-BANG-DOI-CHIEU-NGU-NGHIA`; mới là đề xuất E5 |
| duong-dan-chua-khep-trong-goc | VÁ HỜ | containment tệp ca/cổng/ADR | KN-0, cùng nợ trên; authority triển khai chưa có; Windows chưa đo |
| moc-chuyen-tiep-mau-thuan | VÁ HỜ | nghiệm thu chuyển tiếp kế nhiệm | KN-1, `INV-12-CONG-VERDICT-THEO-LOP`; sửa hợp đồng có thực nhưng không tính phần chuyển đi đã đóng |
| tieu-chi-dong-xoa-khong-do-hanh-vi | VÁ HỜ | N8 không chứng minh giữ byte hàm cũ | Cả hai tệp cần kiểm phạm vi, không chỉ số hunk |
| dem-khong-khai-tap-ca | ĐÃ VÁ THẬT | 0 | Không đòi chạy ca Windows trên Linux |
| schema-bo-sot-provider-hop-le | VÁ HỜ | nghiệm thu identity v2 | KN-1, `INV-12-CONG-VERDICT-THEO-LOP`; chưa có v2 r2 hoàn chỉnh |
| tien-kiem-lease-chua-du | VÁ HỜ | chuẩn hóa và closure của 3b | Snapshot không chứng minh trạng thái khi cấp lease tương lai |
| doi-diem-goi-cong-chua-du-yeu-cau | ĐÃ VÁ THẬT | 0 | Đã nối entrypoint; độ phủ neo và phép đo đột biến là lớp khác |

Phân xử kế nhiệm: ghi tên KN-0/KN-1 và hai nợ trong ADR là tiến bộ thực, không phải bỏ việc không ghi nợ. Tuy nhiên §14 nói rõ “đề xuất, chưa phải việc được giao”; C1/C2 mới xin authority. Không coi chúng là packet đã được cấp hay evidence đóng lớp. Đặc biệt F07 đã sửa **mâu thuẫn thiết kế**, F10 đã sửa **hướng định nghĩa schema**; nhãn VÁ HỜ ở đây bảo toàn phần nghiệm thu chuyển đi theo chỉ thị lượt này, không có nghĩa bản r2 còn nguyên lỗi câu chữ r1.

## BẢNG LỚP

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| neo-thieu-nghia-vu | F02; 3 câu nghĩa vụ | P1 | r1 925f851 → r2 69bf087 | Ma trận nghĩa vụ đầy đủ, neo theo nghĩa vụ | Xóa từng câu vẫn rc 0 |
| cong-khong-do-bat-bien | F03; 1 ô INV-20 | P1 | r1 → r2 | Gắn đúng giới hạn/nợ vào ô | Đọc bảng, mã và nợ scanner hiện hành |
| thieu-truy-vet-yeu-cau | F04; 1 vế §1(2) | P1 | r1 → r2 | Đối chiếu từng vế nguồn | Không có branch/worktree trong bảng |
| kiem-chuoi-khong-doc-cau-truc | F05; 3 nhóm bảng/ca/nợ | P2 | r1 → r2 | Ràng buộc cấu trúc thật và giữ nợ kế nhiệm | Bảng tách rc 0; AST/nợ chưa nghiệm thu |
| duong-dan-chua-khep-trong-goc | F06; 1 nhóm đọc tệp kế nhiệm | P2 | r1 → r2 | Một hợp đồng containment cho mọi tệp | Không tự dựng payload đường dẫn |
| moc-chuyen-tiep-mau-thuan | F07; 1 nhóm cutover kế nhiệm | P2 | r1 → r2 | Giữ một vị từ, nghiệm thu cả bốn ô và KĐĐ | Chỉ đo hợp đồng, chưa đo cổng |
| tieu-chi-dong-xoa-khong-do-hanh-vi | F08; 1 thước N8 | P2 | r1 → r2 | Kiểm nguồn/AST ở vùng cũ cùng ngoại lệ rõ | AST đổi, vẫn ba hunk |
| schema-bo-sot-provider-hop-le | F10; 1 nhóm identity v2 | P2 | r1 → r2 | V2 độc lập, ca âm/dương đủ identity | Chưa có schema r2 nghiệm thu |
| tien-kiem-lease-chua-du | F11; 2 nhóm canonicalization/closure | P2 | r1 → r2 | Dùng đầy đủ §5 khi kiểm giao | Đối chiếu thủ tục 3b với §5 |
| doi-chung-khac-ho-chon-nham-doctrine | F13; 1 xung đột N7/N8 | P1 | mới r2 69bf087 | Phân họ đúng và cho phép sửa selector cần thiết | Mutant tách câu làm đỏ cả ba đối chứng |
| ma-tran-dem-doi-loi-thay-doi-mau | F14; 4 ca vùng render | P2 | mới r2 69bf087 | So assertion thật, không so cả chuỗi output | Mutant bỏ mask vẫn thỏa assertion của 4 ca |
| tach-packet-bo-dieu-kien-integration | F15; 1 đường nối tiếp chưa tuân ADR | P2 | mới r2 69bf087 | Ghi đường integration hoặc ngoại lệ có authority | ADR-0053 giữ nguyên điều kiện của ADR-0044 |
| nghiem-thu-khoa-so-ca-trai-quyen-them | F16; 1 mâu thuẫn N6/§8.3 | P2 | mới r2 69bf087 | Phân biệt sàn bắt buộc và tập ca thêm thực | Thêm 41 hợp §8.3 nhưng N6 từ chối |

## BẢNG SĂN

Các lệnh đã chạy trong lần trước của chính lượt 2, còn log/script tại đây; phép kiểm thêm được ghi tiếp cuối tệp. Không coi rc 0 của script đo là rc 0 của cổng: rc từng ca nằm trong output.

| hướng độc lập | lệnh | output thật | kết luận |
|---|---|---|---|
| 1. OID/băm/trần | `python -B out/measure.py` | `SHA256 d25a0c...`; `REFS 385`; `OPT_IN 0055 [0, 128] True`; `OPT_IN 0053 [0, 128] True` | OID hợp lệ trên mirror; lịch sử fetch chưa đo |
| 2. Khả thi matcher | cùng lệnh | `NEO_HASH 14 True`; `ANCHOR_MATCHES [('N01', 1), …, ('N14', 1)]` | F01 đóng |
| 3. Độ phủ nghĩa vụ | `python -B out/coverage_probe.py` | `REMOVAL scope_cut_not_fix (0,...)`; `convergence_stop (0,...)`; `slug_mapping (0,...)` | F02 còn mở |
| 4. Cấu trúc bảng | `python -B out/probes.py` | `TABLE_BLANK_LINE (0,...)`; `TABLE_BLANK_EVERY_ROW (0,...)`; `TABLE_DELETE (9,...)` | F05: chỉ băm các hàng, không kiểm chúng cùng một bảng |
| 5. Phạm vi N8 | cùng lệnh | `N8_OLD_FUNCTION_CHANGED True HUNKS 3 3 NUMSTAT 81 1` | F08 còn mở |
| 6. Lease/ADR toàn mirror | `python -B out/leases.py` | `RECORDS 541 LIVE 13 TOMBSTONED 7 ACTIVE 6`; `ADR_0068_PLUS 0 OF 385` | B4 đang giữ hai .py; chưa được thi công |
| 7. Hồi quy | `python -B out/run_selected.py base cases`; `python -B out/run_selected.py prototype cases`; tương tự với `mutants` | `selected-base.log`, `selected-prototype-repeat.log`: 132/132 PASS; JSON mutant nền/prototype bằng nhau | Không có hồi quy trong tập đã chạy |
| 8. Đối chứng đột biến | `python -B out/harness_probe.py` | `CLASSIFIED_DOCTRINE False`; mutant `inv_cau_khong_tach`: cả ba đối chứng `AssertionError`, rc 9 | F13 |
| 9. Răng assertion vùng render | `python -B out/replay_matrix.py`; `python -B out/matrix_summary.py` | Bốn ca: `BASE 9 MUTANT 9`, vẫn `N04 True` hoặc `BANG True`/`KDD True` | F14: output đổi không bằng assertion đổi màu |
| 10. Entry point | `python -B out/probes.py` | `REMOVE_8_3 (9,...)`; bản nguyên vẹn `(0, 'doctrine-scan: sạch …')` | F12 đóng |

## BẢNG ĐO

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| SHA-256 / HEAD / base | đầu chỉ thị | đúng các giá trị đầu verdict | có |
| mirror | full, abbrev 7 | shallow false, abbrev 7 | có |
| ref | 382 lúc 19:19Z | 385 trong snapshot reviewer | khác thời điểm, không phải bằng chứng số lịch sử sai |
| lease | 541 / 13 / 7 / 6 | đúng, tính tại 19:19Z | có |
| B4 | giữ 2 .py tới 24-11 08:00Z | `wp1462-r7-g1-claude`, đúng hai đường và hạn | có |
| ADR trống | 0/382 ref có ≥0068 | 0/385 | có về snapshot |
| ADR nền / lớn nhất | 66 / 0067 | 66 / 0067 | có |
| INV | 28 = 15 cổng + 12 kỷ luật + 1 chưa đo | đúng; 11/15 cổng có nợ | có về hình, chưa đủ về nghĩa |
| nợ / nợ được trỏ | 23 / 21 | 23 / 21 | có |
| tham chiếu ca | 18 | 18 AST nhận; tên bịa không nhận | có về tồn tại |
| neo | 14/14 mỗi neo một đơn vị | đúng; băm tự tính khớp | có |
| bảng | 30 dòng và băm a022ca… | đúng | có |
| ADR / protocol | 127 dòng / +46−2 | 127 / +46−2 | có |
| mã / fixture | +79−1 / +18−1 | đúng | có |
| 40 ca, 25 mutant mới | 30 đỏ + 3 KĐĐ + 3 xanh + 4 tự kiểm; 24+1 | danh sách đúng 40/25; prototype chưa đăng ký ca/mutant mới | chỉ danh sách |
| sổ ca | 1582 / 1581 Linux | đúng, sai khác đúng 1 tên | có |
| MUTANTS / adr_song / doctrine_scan / r1466 | 1864 / 40 / 17 / 0 | đúng | có |
| họ doctrine | 132/132 nền và prototype | đúng trong log chọn lọc | có |
| mutant cũ | 19/19 giữ hạng, 2 chưa đo | reviewer đo cả 21; 128 kết quả ca đích GIET mỗi cây, JSON bằng nhau | mạnh hơn số tác giả |
| adr-song | 66 nền, 67 prototype | rc 0 / rc 0 | có |
| doctrine-scan cây thật | 12 tệp, rc 0 | đúng trên nền/prototype | có |
| 35×24 ma trận | mỗi mutant giết ca, mỗi ca có mutant | 35 ca × 24 mutant, 4 rc 0 / 31 rc 9; tác giả so rc+cờ KĐĐ, assertion không đổi ở một số ca | không chứng minh N7 |
| nguyên mẫu KN-0 | 151 dòng, 0 lỗi, 15/11/12/1 | `bb2.py` đúng 151 dòng, 0 lỗi và đúng phân loại; `kn0/bb.py` là bản 77 dòng cũ | không phải mã giao nộp |
| biên nhận / bang_lop | 352 / 0 | 352 / 0 | có |
| schema v1 | 16 required, 3 provider, 4 assurance | đúng | có |
| SCHEMA_REVIEW | 9 dòng | 9 | có |
| pre-push | 392 dòng | 392 | có |
| workflow / kiem-merge / adr-song | 10 / 0 / 0 | đúng | có |
| tổng wp1466 | khoảng 387 / 4 tệp | 127+46+79+135=387; 135 chỉ mới đo 18 | ước lượng, không phải tổng diff đã có |
| tổng hai khối / KN-0 / KN-1 | 677 / 290 / 370 | 387+290=677; KN-0/1 vẫn ước | không xác minh như số triển khai |
| KN-1 tệp | 6; thêm ADR thành 7 | đếm đúng | chỗ vượt trần còn phải giải |
| ruleset / Issue / fetch lịch sử | REST theo thời điểm tác giả | không có readback tương ứng trong mirror | KHÔNG ĐO ĐƯỢC |
| full suite, Ruff, Windows, CI H, hậu land | chưa đo hoặc tiêu chí tương lai | chưa chạy | KHÔNG ĐO ĐƯỢC |

## ĐỐI CHIẾU NGHIỆM THU VÀ CÁC QUYẾT ĐỊNH

### N1–N8, L3 và năm vế L6

| tiêu chí | khả năng đo trên mã giao nộp | L3 / L6 và kết luận |
|---|---|---|
| N1 | So byte ADR H với khối từ blob spec đúng hash; thay đúng bảy placeholder bằng dữ kiện có nguồn | Có dương/âm (a), exact-byte trên blob ghim băm nên không hứa chịu reflow (b); sáu số phải đo riêng từng tệp (c,e). (d) không áp dụng vì không tìm lượng bằng chữ. Approval line vẫn cần authority thật, khớp dạng không tự tạo approval. |
| N2 | So đủ sáu khối và vị trí, hai khối cũ vắng, numstat nền..H | Có cả hai vế (a), so byte hợp đồng chứ không grep tiền tố (b); mỗi vị trí đúng một, không đếm tổng (c). (d,e) không áp dụng vì không tìm lượng/khai 0 cổng. Sáu mỏ neo nền đo được đều 1. |
| N3 | ADR-song trên H, số A nền+1 | Có phép âm bỏ P6 và số dương A/A; đã đo 66→67 trên cây thử. Không phải regex mới cần chịu cách viết chữ số. |
| N4 | Doctrine-scan thật trên H, xóa neo/hàng làm đỏ | Bản chuẩn rc 0, xóa 14 neo rc 9 đúng từng nhãn; nhưng phạm vi nghĩa vụ và cấu trúc bảng còn F02/F05. Màu suite không đóng hai lớp này. |
| N5 | Reviewer băm độc lập 14 neo và 30 dòng của blob H | Đã tính độc lập 14 băm và băm bảng, đúng. NFC/gộp khoảng trắng (b), từng neo riêng (c); không tìm cách viết số (d). Đây là toàn vẹn chữ trong đơn vị đã định nghĩa, không bằng chứng độ phủ ngữ nghĩa hay vị trí của mọi nghĩa vụ. |
| N6 | Tập tên đăng ký và tập Linux, trạng thái từng ca, CI 16 mảnh+gom | Đã chữa đơn vị; chưa có 40 ca sản phẩm. Phép kiểm còn mâu thuẫn quyền thêm (F16). Không được dùng ≥40 tên hay N/N tổng thay tập bắt buộc (c). |
| N7 | Bắt buộc chạy vòng đột biến thật trên H, target và control | Đây là yêu cầu đúng theo L3; số đo S10 không thay nó. Vòng thật đã chứng minh F13; ma trận rc+KĐĐ không chứng minh assertion đổi màu, F14. Không có 25 mutant sản phẩm để khai nghiệm thu đủ. |
| N8 | Đo trên diff H thật được, nhưng phép đo không chứng minh điều mình hứa | Phản chứng thêm ở biên hunk vẫn 3 hunk, AST hàm cũ đổi (F08). Cấm sửa hàm selector còn xung đột với N7. L6 yêu cầu kiểm thước đo: một ví dụ ra hunk thứ tư không đủ. |

L6(e): các vector sáu vị trí đã được đo, lưu `measure.log`; mẫu `refs/pull/` được sửa đúng ở script bổ sung (script cũ gõ nhầm `refs/pull:`), ra 0·1·1·0·0·0 như spec. Các số match chỉ định vị; không được suy từ 0 match một từ khóa ra 0 cổng. Đã đọc thêm 15 match `label|assignee|board` mà người soạn để chưa đọc: chúng là `KeyboardInterrupt`, nhãn sandbox/hồ sơ, biến thông báo hoặc label chọn Windows CI; không phải cổng từ chối chat/label làm nguồn authority. Không thấy thêm bằng chứng phủ INV-23 từ tập này.

### Trần, tách packet, authority và phối hợp

- Hai OID opt-in đúng; giới hạn áp cho PR **giao nộp**, không lấy 681 dòng spec hoặc bundle reviewer làm diff sản phẩm. Nguyên mẫu hiện có 127+46+79+18=270 dòng thêm; phần còn lại của 387 là 117 dòng ước lượng. 677=387+290 là tổng có hạng ước lượng; 370 của KN-1 cũng là ước lượng. Chưa có cơ sở nói ứng viên cuối chắc chắn trong trần. N12 đúng khi đòi đo trên H, dừng trước push/review nếu vượt.
- Tách luật/toàn vẹn/ngữ nghĩa/verdict có phần hữu ích độc lập; không sai chỉ vì có ba packet, không bắt buộc viết tất cả cổng trong cùng PR. Tuy nhiên đường nối tiếp vẫn phải giữ điều kiện ADR-0044/0053 (F15), và §8.3 không cho gọi phần chuyển đi đã vá. KN-1 tự khai thêm ADR thành 7 tệp: đây là điều phải giải trước khi đóng băng KN-1, không phải quyền nâng trần ngầm của wp1466.
- L7: không thấy ngân sách mềm hay điểm hỏi sau N lượt tự đặt. C1/C4 là thay luật/ngoại lệ bảng nên E5; C3 là quyền miễn Windows của cổng K6 nên E2. C2 có phần xin nâng trần thuộc E2 **nếu chọn gộp**, còn phương án tách trong trần không tự tạo một lần xin tài nguyên; nó nằm trong approval E5 của phạm vi. Một lựa chọn gộp vẫn cần `nang_tran` đủ bốn trường và lý do không tách được, không được lấy riêng câu trả lời C2 làm khối hợp lệ. Chưa thấy authority đã cấp cho lựa chọn nào trong mirror. Đây là phân định điều kiện, không phát sinh câu hỏi thêm cho chủ kho trong lượt review.
- ADR-0055 quy định trục lời gọi của PR; spec đã khai trung thực rằng áp cho review đặc tả không gắn PR chưa có luật rõ. Không tự xem “1/10” trong lời thuật là phép đo ngân sách; cũng không coi lần tiếp tục vì mạng lỗi là reset lịch sử hoặc miễn lời gọi.
- B4 #1462 r7 dự kiến chạm đúng hai .py của wp1466 và đang giữ chúng tới 24-11 08:00Z. R2 đòi B4 land trước, đo lại ref/lease/base và năm mốc N8; hướng phối hợp đó đúng. Chưa có diff B4 cuối để kết luận sau B4 vẫn +40, vẫn 132 ca, vẫn đúng vị trí chèn; nếu mốc lệch thì revision theo điều kiện bắt đầu 4.
- #1460 r7 dự kiến sửa `.claude/dev/ci_dang_ky_test.py`; lease đang giữ tệp là `wp1236-a-r9-g1-claude-20261120` tới 22-11 15:35Z. wp1466 thêm ca vào test file đã đăng ký, không thêm module test, nên không cần sửa registry này. Mã registry hiện nhận `packet_loop_test.py` qua `packet_loop_test_manh.py`, không ghim số 1582/1864. Không có giao write set trực tiếp với #1460, không có lý do tự mở tệp đó. Cả hai vẫn phải dùng CI/full-mutant trên H thật sau thay đổi nền.
- Bốn đường wp1466 được selector thật chọn `chay`. Bốn tệp ca ngoại vi của bảng chọn `bo_qua` khi chỉ riêng chúng đổi: nợ trigger KN-0 mục 7 là có thật, đã khai; không tính đó là một finding mới không ghi nợ. Băm bảng ở wp1466 chưa phát hiện ca bị đổi tên ở các tệp khác; câu này đã được nêu đúng là nợ, không gọi nó là cổng ngữ nghĩa đã giao.

### Bổ sung bảng đo và nguồn log

| khẳng định | đo độc lập bổ sung | kết luận |
|---|---|---|
| Hiện vật nguyên mẫu có checksum | 20/20 SHA256SUMS khớp; `git apply --check -p1` rc 0 | Bundle toàn vẹn |
| Cây dùng đo đúng patch | Áp lại vào `out/exact-patch`, rc 0; ba tệp protocol/mã/test bằng từng byte với `out/prototype` | Các log cũ dùng đúng nguyên mẫu được giao |
| Fixture cũ dưới cổng mới | 132 ca: 8 đạt, 124 đỏ; 122 lỗi có trực tiếp chuỗi “được rc=9”, hai ca gộp báo rc=9 trong các biến thể | Tái lập 124/132, không lấy lời khai S11 |
| 6 mỏ neo chèn / 5 mốc N8 | 1·1·1·1·1·1 / 1·1·1·1·1 | Đúng trên base snapshot, chưa phải base sau B4 |
| 23 audit / 62 dòng | 23 ID A1–A3, B1–B15, C1–C5; 62 dòng; ma trận 15.2 có đúng cùng tập 23 | Có phủ mã audit, chưa đồng nghĩa phủ mọi vế nghĩa vụ |
| R1→r2 | INV 21→28, nợ 9→23; danh sách neo 8→14, ca 44→40, mutant 33→25 | Không coi giảm số ca/mutant là regression tự thân: scope đã đổi và phải giữ lịch sử |
| 4 adapter / CLI trong test / 4 tệp ngoài | 1·1·1·1 lời gọi; 21 dòng gọi CLI trong test; 3+3+7+1=14 dòng ngoài | Khớp S9; CI có 2 dòng chứa tên lệnh: một lời gọi nhanh và tên của chính bước ấy |
| S13 run r1 | `provider: openai_codex`, `chup_workspace: false`, có `bat_dau_utc` | Khớp; không suy provider protocol bằng so chuỗi trực tiếp |
| Sáu số Cưỡng chế ADR trên nguyên mẫu | 0·18·0·0·0·0 (mẫu `ADR-0068\|INV_\|_inv_`) | Chỉ là số tại prototype; N1 vẫn phải đo trên H thật |
| Hash verdict r1 | `b2fc797949a75467843b06e15fdf31583e68ab276a0831456cdc196024d601b0` | Khớp dẫn nguồn r2 |
| Tiêu đề trùng sau bảng | Bản chuẩn rc 9 nêu 2 tiểu mục, mutant `inv_nhieu_tieu_muc` rc 0 | Bác nghi ngờ mutant thứ 24 còn sống trong ca đã sửa vị trí; fixture cũ trước bảng đúng là không giết |
| 11 mẫu đường dẫn KN-0 | Không tìm được tập 11 fixture đường dẫn tương ứng trong bundle; không tự soạn payload | KHÔNG ĐO ĐƯỢC con số 3 qua/8 từ chối như một tập 11; chỉ kiểm hợp đồng và các fixture đã được giao |
| Các mốc REST/fetch | Không có response lịch sử tên/SHA 382, ba ref lệch rồi hết lệch, Issue open/comment/time, sáu required check/bypass | KHÔNG ĐO ĐƯỢC; số ref snapshot 385 không thay response lịch sử |

Các log nguồn: `measure.log`, `probes.log`, `coverage-probe.log`, `leases.log`, `selected-base.log`, `selected-prototype.log`, `selected-prototype-repeat.log`, `mutants-base.json`, `mutants-prototype.json`, `harness-probe.log`, `matrix/raw-results.json`, `matrix/assertion-results.json`, `matrix-summary.log`, `followup.log`, `remaining.log`, `contracts.log`, `last-check.log`. Các script cùng tên nằm trong `out/`; không phải patch sản phẩm được đề nghị merge.

### neo-thieu-nghia-vu [P1] F02 — Băm 14 neo vẫn bỏ những luật quyết định có được đóng lớp hay không

TỆP/DÒNG: `ops/specs/wp1466.md:384–418`; protocol `§8.3`, `§12`.

VẤN ĐỀ: Các nghĩa vụ cũ đã được thêm neo, nhưng bỏ từng câu về (1) không tính cắt scope/chuyển biểu hiện là vá, (2) bảng nối khi tách/gộp slug, (3) dừng sau hai chuyển tiếp <50% vẫn rc 0. Đây là xóa luật hiện có, không phải thêm một câu nói ngược thuộc giới hạn đã khai. Ma trận Q1 đang chọn vài câu đại diện và không chứng minh §8.3/§12 được giữ đủ.

GỢI Ý VÁ: Ở ma trận 8.3, lập nghĩa vụ theo từng vế của nguồn rồi thêm neo/chốt cho các vế còn thiếu; ca bỏ riêng từng nghĩa vụ phải đỏ với lý do riêng, đối chứng biên tập vô hại xanh. Rủi ro cần tránh là lại giữ số 14 như một trần hoặc khóa cả đoạn không cần thiết.

ĐÃ THỬ NGHIỆM: `coverage_probe.py` trên bản sao protocol, ba phép xóa riêng đều rc 0; các neo hiện có vẫn đủ. Bốn biểu hiện r1 được kiểm bằng xóa neo, đều đỏ.

ĐỘ TIN: cao.

### cong-khong-do-bat-bien [P1] F03 — INV-20 còn quảng bá mạnh hơn phép đo và không mang nợ

TỆP/DÒNG: `ops/specs/wp1466.md:98,229–257,317`; protocol `§8.3` bảng nợ scanner.

VẤN ĐỀ: Ô INV-20 nói adapter/CLAUDE.md không chép doctrine và ghi có cổng đầy đủ. Bảng đọc cổng của chính r2 chỉ nhận n-gram, không phát hiện diễn đạt lại; protocol đã ghi `phep-do-doctrine-khong-du-rang`. Không có nợ tương ứng trong 23 mục Nợ, cũng không có `còn nợ` ở ô. Q2 đòi gắn nợ khi cổng chỉ đọc một phần; băm trọn bảng đang khóa một ô khai quá rộng.

GỢI Ý VÁ: Nêu phạm vi có máy của INV-20 và tên nợ cho phần không đo; đưa mục nợ vào đúng ADR, tính lại băm/bảng/số. Ca thật phải kiểm đúng tính chất được nhận, không dùng số tên ca tồn tại làm bằng chứng độ phủ. Không cần mở rộng scanner ngoài packet chỉ để hợp thức nhãn.

ĐÃ THỬ NGHIỆM: `coverage_probe.py` in nguyên ô và `INV20_KNOWN_DEBT_IN_ADR False`; đọc ngưỡng n-gram và bảng đọc cổng, đối chiếu toàn bộ 15 ô.

ĐỘ TIN: cao về sai nhãn; không tự tạo chuỗi độc hại để thử scanner.

### thieu-truy-vet-yeu-cau [P1] F04 — Ma trận khai phủ §1(2) nhưng bỏ branch/worktree riêng

TỆP/DÒNG: `ops/specs/wp1466.md:299–300,579–592`; protocol `:32`.

VẤN ĐỀ: §1(2) gồm branch/worktree riêng và loại trừ giao write set. INV-02 chỉ chứa vế thứ hai. INV-14 là quyền chỉ đọc, INV-26 là phân loại nhánh sổ sách; chúng không thay nghĩa vụ run riêng. Không có nợ cho phần thiếu dù 15.1 khai mọi bất biến §1 đã có dòng. Các điểm audit cũ được bổ sung không đóng biểu hiện cùng lớp này.

GỢI Ý VÁ: Ánh xạ ở mức từng vế, ghép vào INV thích hợp hoặc thêm dòng và nợ có tên; so ngược nguồn→INV để kiểm không mất nghĩa vụ. Giữ yêu cầu hữu ích, tránh chỉ thêm tên mục vào cột nguồn.

ĐÃ THỬ NGHIỆM: `WORKTREE_IN_TABLE False`, `BRANCH_IN_INV02 False`; đọc cả 28 phát biểu và toàn ma trận 23 điểm audit.

ĐỘ TIN: cao.

### kiem-chuoi-khong-doc-cau-truc [P2] F05 — Băm hàng rời không chứng minh còn một bảng Markdown

TỆP/DÒNG: `ops/specs/wp1466.md:380,422–434,540–541`.

VẤN ĐỀ: Thuật toán lấy MỌI dòng bắt đầu bằng `|` trong §1.1, bỏ qua dòng trống và nội dung xen giữa. Chèn dòng trống giữa từng hàng không đổi băm nhưng các hàng không còn thuộc một bảng render có header/separator. Đây là lỗi cấu trúc mới sinh khi thay G1 bằng băm bảng. Hai biểu hiện r1 về khai báo ca và vị trí nợ đã có hướng sửa AST/mục Nợ, nhưng chuyển KN-0 vẫn chưa nghiệm thu.

GỢI Ý VÁ: Ràng buộc một bảng liên tục, header/separator và số ô; nếu gặp cấu trúc ngoài tập hỗ trợ thì KĐĐ. Thử tách hàng bằng dòng trống (vô hại), đối chứng chỉ thêm khoảng trắng trong ô xanh; giữ các ca AST/nợ trong kế nhiệm có authority. Tránh nhầm “băm đủ hàng” với “đọc đúng cấu trúc”.

ĐÃ THỬ NGHIỆM: `TABLE_BLANK_LINE` và `TABLE_BLANK_EVERY_ROW` rc 0; bỏ một hàng rc 9. Không dựng payload HTML/chuỗi độc hại.

ĐỘ TIN: cao.

### duong-dan-chua-khep-trong-goc [P2] F06 — Containment của các tệp được trỏ vẫn là phần chuyển kế nhiệm

TỆP/DÒNG: `ops/specs/wp1466.md:401,538,675`.

VẤN ĐỀ: G1 nay bảo vệ protocol. Tuy nhiên lỗi r1 gắn với tệp ca, và nhóm tệp ca/cổng/ADR rời wp1466. KN-0 mục 2 đã có allowlist/resolve/regular-file/UTF-8 rõ, nhưng KN-0 là đề xuất chưa được cấp, chưa có bộ ca âm/dương cùng mutant để đóng nhóm ấy. Không khẳng định hợp đồng mới còn nguyên lỗ absolute/`..` cũ; finding còn mở về phần kế nhiệm chưa xác minh.

GỢI Ý VÁ: Giữ slug cùng nợ/authority kế nhiệm, nghiệm thu từng loại tệp bằng các fixture executor/điều phối cung cấp; kiểm đích trong/ngoài root mà nội dung đều hợp lệ. Không tuyên bố đóng chỉ từ regex; không dùng tệp vắng để giả phép containment đỏ.

ĐÃ THỬ NGHIỆM: Đọc hợp đồng; chạy lại hiện vật nguyên mẫu được cung cấp cho protocol. Không tự soạn payload đường dẫn. Chưa có evidence cho toàn bộ đường KN-0 theo hợp đồng r2 trên các nền.

ĐỘ TIN: cao về phần chưa đóng; không cáo buộc mã giao nộp chưa tồn tại.

### moc-chuyen-tiep-mau-thuan [P2] F07 — Hợp đồng cutover thống nhất nhưng phần nghiệm thu bị chuyển đi

TỆP/DÒNG: `ops/specs/wp1466.md:199–205,553–563,676`.

VẤN ĐỀ: Hai vị từ mâu thuẫn r1 đã được sửa thật ở văn bản. Tuy nhiên bốn ô cutover, ba trạng thái KĐĐ và mutant dùng sai thời điểm chỉ được hứa cho KN-1; không có mã/ca r2 để đo. Theo yêu cầu bảo toàn lớp của lượt này, phần chuyển phạm vi không vào F. Nợ chung có tên nhưng authority chỉ là đề xuất E5.

GỢI Ý VÁ: Giữ một vị từ này trong ADR/schema/consumer khi KN-1 được cấp; gắn bộ ca bốn ô, thiếu/sai `bat_dau_utc`, thiếu T và mutant vào acceptance của successor; ghi rõ đây là đóng thiết kế, chưa đóng nghiệm thu. Tránh coi ngày H là mốc thay thế.

ĐÃ THỬ NGHIỆM: Tự lập bảng start/H: F/F→miễn, F/T→miễn+cảnh báo, T/F→áp, T/T→áp; đối chiếu hai vị trí trong spec. Không chạy cổng cutover chưa có.

ĐỘ TIN: cao về văn bản; thực thi KHÔNG ĐO ĐƯỢC.

### tieu-chi-dong-xoa-khong-do-hanh-vi [P2] F08 — Ba hunk vẫn chứa được sửa hàm cũ

TỆP/DÒNG: `ops/specs/wp1466.md:119–120,436,460,632,654`.

VẤN ĐỀ: N8 dùng vị trí/số hunk để chứng minh mọi hàm cũ giữ từng byte. Hunk chèn ngay trước `cmd_doctrine_scan` có thể bắt đầu bằng một dòng thụt thuộc hàm cũ phía trước, rồi mới đến các hàm module mới. AST hàm cũ đổi, nhưng hunk vẫn thuần chèn, đúng vị trí và tổng vẫn −1. Một mẫu `pass` ở `cmd_adr_song` ra bốn hunk không chứng minh mọi vị trí khác.

GỢI Ý VÁ: Đối chiếu vùng nguồn/AST và phạm vi hàm trước/sau, ngoại lệ đúng khối chèn trong cmd_doctrine_scan và epilog; kiểm byte nếu hợp đồng đòi byte. Ca khóa cần cả vị trí sát khối chèn, giữa hàm cũ và tệp test; thêm hàm module hợp lệ phải qua. Tránh dùng kiểm AST đơn thuần để tuyên bố comment/byte bất biến.

ĐÃ THỬ NGHIỆM: `probes.py`: AST `_doc_nguon_protocol` đổi, `HUNKS 3 3`, numstat +81/−1; lưu `n8-counterexample.diff`, đã khôi phục prototype.

ĐỘ TIN: cao.

### schema-bo-sot-provider-hop-le [P2] F10 — V2 đã đổi hướng thiết kế nhưng chưa có bằng chứng đóng identity

TỆP/DÒNG: `ops/specs/wp1466.md:549,567,679`.

VẤN ĐỀ: KN-1 mục 1 sửa lỗi “v1 cộng khóa” và nêu năm chỗ cần thay. Nhưng nó vẫn giao một phần quyết định cho KN-1, và chưa có schema v2/consumer theo đầy đủ hợp đồng r2 cùng ca AG hợp lệ, sai surface và cùng model-family. Chuyển Q4 ra khỏi ADR không phải bằng chứng đóng lỗi provider của yêu cầu “mọi lượt review”.

GỢI Ý VÁ: Giữ slug/nợ kế nhiệm, khóa ma trận provider/family/surface/transport và human theo protocol ở base KN-1; đưa cả các ca dương/âm vào acceptance, không chỉ sửa enum provider. Rủi ro là mở enum tự do hoặc kiểm trực tiếp `openai_codex` như provider protocol.

ĐÃ THỬ NGHIỆM: V1 thực có 3 provider. `check_last.py` dùng schema prototype và mẫu JSON bình thường được giao: AG đúng family/surface có 0 lỗi, nhưng AG với `codex_cli` và Codex với family `claude` cũng có 0 lỗi. Đó là chứng cứ nguyên mẫu này chưa đáp ứng hợp đồng r2, không phải khẳng định thiết kế r2 cho phép hai trường hợp sai ấy. V2 giao nộp và ca K4 tương ứng chưa có.

ĐỘ TIN: vừa; phần mở là nghĩa vụ kế nhiệm, không nói v1 lịch sử phải được sửa tại wp1466.

### tien-kiem-lease-chua-du [P2] F11 — Tiền kiểm 3b chưa dùng effective write set chuẩn hóa của §5

TỆP/DÒNG: `ops/specs/wp1466.md:45–50`; protocol `:327–361`.

VẤN ĐỀ: 3b bổ sung prefix nhưng chỉ bỏ planned/separator/NFC/slash cuối. §5 còn đòi case-fold, resolve parent/symlink và closure từ canonical change-impact policy. Một kết luận “0 lease giao cả bốn đường” theo chuỗi thô chưa chứng minh điều kiện không giao effective write set. Snapshot hiện có B4 giữ đúng hai đường nên không cần dựng phản chứng gây hại để chứng minh sự thiếu thủ tục.

GỢI Ý VÁ: Dùng cùng canonicalization và closure của §5 hoặc ghi KĐĐ nếu không thể tái dựng; tiền kiểm đọc toàn ref và phân biệt lỗi quét với tập rỗng. Ca khóa khác kiểu chữ, prefix hai chiều và companion closure do điều phối cung cấp; không tự fetch/sửa mirror review để giả độ mới.

ĐÃ THỬ NGHIỆM: Quét 541 bản ghi, 6 active, B4 giữ hai .py; đọc 3b thấy thiếu case-fold, đối chiếu §5. Chưa đo collision thực ở thời điểm cấp lease tương lai.

ĐỘ TIN: cao về hợp đồng, không cáo buộc đã có hai writer.

### doi-chung-khac-ho-chon-nham-doctrine [P1] F13 — N7 chọn doctrine làm đối chứng cho mutant của doctrine, còn N8 cấm sửa selector

TỆP/DÒNG: `ops/specs/wp1466.md:119–120,425,439–445,459–460`; `packet_loop_test.py` hàm `_la_ho_doctrine`, `_doi_chung_khac_ho`.

VẤN ĐỀ: Tên bắt buộc `r1466_*` không được selector cũ nhận là họ doctrine. Đối chứng được chọn là `doctrine_scan_sach_xanh`, `ac18_nfkc_hai_cham_toan_rong`, `ac19_oan_claude_md_master`. Mutant bắt buộc `inv_cau_khong_tach` đổi chính phép tách neo mà cả ba đối chứng cần; cả ba đỏ rc 9. N7 yêu cầu đối chứng còn xanh, trong khi §6/N8 giữ nguyên byte các hàm cũ của test. Đây là xung đột acceptance thực, không phải hồi quy trên bản nguyên vẹn.

GỢI Ý VÁ: Cho phép cập nhật điểm phân họ với phạm vi rõ và dùng đối chứng thực sự độc lập; cập nhật N8 tương ứng. Khóa cả lựa chọn đối chứng và phân hạng bằng đúng `packet_loop_test_manh.chay`, trên mã giao nộp với mutant thật. Không dùng mẫu mutation giữ nguyên hành vi tách câu chỉ để làm đối chứng xanh.

ĐÃ THỬ NGHIỆM: `harness_probe.py`: `CLASSIFIED_DOCTRINE False`; chạy ba ca chọn bởi hàm thật trên mutant tác giả: cả ba `AssertionError`, rc 9, vắng 11 neo. Hai mutant kiểm soát khác giữ cả ba PASS. Phép gọi tích hợp đã đo bằng `verify_followup.py`: một ca bridge dùng fixture xanh cũ dưới tên `r1466_probe_control_selection`, đăng ký đúng mutant tác giả, gọi `manh.chay` thật. Nền 1/1, 0 bỏ qua; mutant bị báo giết cả ba đối chứng; `TỔNG: 3 lỗi`, kết quả `(1, ['r1466_probe_control_selection'], False, 1)`. Đây là phép đo selector/vòng đột biến, không phải bộ 40 ca giao nộp.

ĐỘ TIN: cao đối với selector và mutant nguyên mẫu; tên/shape implementation giao nộp còn chưa có.

### ma-tran-dem-doi-loi-thay-doi-mau [P2] F14 — Bỏ mask đổi thông báo nhưng bốn assertion vẫn xanh

TỆP/DÒNG: `ops/specs/wp1466.md:75–76,422,434,441–442,459`; nguyên mẫu `ma_tran.py`.

VẤN ĐỀ: Hàm `chay` của ma trận tác giả trả chuỗi ghép mã thoát với cờ `K` nếu stderr chứa `KHÔNG ĐO ĐƯỢC`; ma trận coi chuỗi ấy khác là “giết”. Với mutant `inv_bo_che_khong_render`, protocol thật có comment HTML; G3 làm KĐĐ ở các fixture có nguồn nguyên mẫu được đọc tới bước này. Ở bốn ca `neo_trong_rao_ma`, `neo_trong_comment_html`, `bang_trong_rao_ma`, `rao_khong_dong`, cả bản chuẩn lẫn mutant vẫn rc 9 và chứa nhãn/lý do mà §8.4 đòi. Thêm cờ KĐĐ vào một kết quả vốn đã đỏ không tương đương assertion đổi màu. Con số “→32” không chứng minh răng G2; nó còn đếm thất bại do chốt khác.

GỢI Ý VÁ: Đo bằng assertion/suite thực, giữ kết quả GIET/SONG/TIN_DUNG_GIA riêng, thiết kế fixture và đối chứng để mutant bỏ đúng chốt làm đổi tính chất cần đo. Nếu cần assertion lý do chính xác hoặc cấm lỗi khác, ghi nó trong hợp đồng và thử thật; tránh cho G3 che lỗi G2. Reviewer không tự soạn payload; executor/điều phối cung cấp ca nội dung.

ĐÃ THỬ NGHIỆM: Dùng lại fixture nguyên văn được giao, `replay_matrix.py` và `matrix_summary.py`; bốn dòng đều `BASE 9 MUTANT 9`, còn đúng `neo N04` hoặc `bảng bất biến`/`KHÔNG ĐO ĐƯỢC`. Có raw JSON để đối chiếu assertion.

ĐỘ TIN: cao về phép đo nguyên mẫu; chưa có bộ 40 ca sản phẩm để nghiệm thu N7.

### tach-packet-bo-dieu-kien-integration [P2] F15 — Tách ba packet nhưng chỉ ràng buộc thứ tự, bỏ điều kiện integration

TỆP/DÒNG: `ops/specs/wp1466.md:15–19,33,519,629`; `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md:16`; `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md:10–12`.

VẤN ĐỀ: wp1466/KN-0/KN-1 cùng sửa hai tệp .py. ADR-0053 chỉ thay cặp số, và nhắc lại rằng nối tiếp chỉ hợp lệ trên integration branch đã nhận slice trước. R2 tự quyết “không dựng Mission”; D8 đợi chủ kho nhận từ ba **packet kế nhiệm** trở lên mới dựng Mission, còn §14 chỉ hứa không mở song song. Điều này chưa bảo đảm điều kiện integration bắt buộc cho chuỗi đã chọn. E5 không được ủy quyền tự đóng băng/cấp lease không phải ngoại lệ của quy tắc integration. Chưa có PR thi công nên đây là lỗi hợp đồng điều phối, không cáo buộc đã merge sai.

GỢI Ý VÁ: Ở §1/§14/D8, nêu branch đích, base và điều kiện predecessor integrated của chuỗi theo ADR-0044; hoặc trình đúng delta quản trị/authority nếu muốn một tuyến khác. Ca kiểm hợp đồng: successor neo trước khi predecessor được nhận phải bị từ chối, base đúng sau integration được nhận; không chỉ kiểm thứ tự ngày hoặc “không song song”. Rủi ro là tạo hai PR chồng write set, hoặc tự suy ba lần land master thành ngoại lệ được duyệt.

ĐÃ THỬ NGHIỆM: Đối chiếu trực tiếp hai ADR và tất cả đoạn scope/dependency/D8; giao dự kiến chứa `.claude/dev/packet_loop.py` và `.claude/dev/packet_loop_test.py`; `coverage-probe.log` in `THREE_SPLIT_PATH_INTERSECTION` đúng hai tệp. Tìm `integration` trong spec chỉ thấy mẫu đo của INV-22, không có cam kết branch/base của chuỗi. Không cần tạo PR để kiểm sự thiếu điều kiện này.

ĐỘ TIN: cao về thiếu hợp đồng; authority cho ngoại lệ chưa có trong snapshot được giao.

### nghiem-thu-khoa-so-ca-trai-quyen-them [P2] F16 — Cho phép thêm ca nhưng N6 bắt hiệu luôn đúng 40

TỆP/DÒNG: `ops/specs/wp1466.md:434,458`.

VẤN ĐỀ: §8.3 xác định 40 tên tối thiểu và nói executor được thêm ca/đột biến. N6 lại buộc cả hiệu sổ đăng ký lẫn hiệu Linux bằng đúng 40, coi mọi hiệu khác 40 là đỏ. Một ca bổ sung để khóa finding mới là hợp đồng cho phép nhưng sẽ làm N6 thất bại. Đây không phải lỗi 1581/1582 cũ: hai đơn vị đã đúng; lỗi mới là giới hạn tập nghiệm thu trái quyền mở rộng ca.

GỢI Ý VÁ: Ở N6 và dòng đếm §8.3, chọn nhất quán “đúng tập đóng” hoặc “40 tên bắt buộc cộng tên bổ sung đã khai”; nếu giữ quyền thêm thì đo hiệu bằng tập thêm thực và kiểm đủ tập bắt buộc, tên duy nhất, không bỏ qua Ubuntu. Đối chứng 40 và 41 ca hợp lệ đều phải đúng luật đã chọn; thiếu một tên bắt buộc phải đỏ dù tổng đủ. Tránh nới thành chỉ ≥40 rồi cho tên thừa che tên thiếu.

ĐÃ THỬ NGHIỆM: `contracts.log`: nền 1582 +40→1622 được nhận, +41→1623 bị N6 từ chối; cùng kết quả với nền Linux 1581. Đọc nguyên văn hai điều khoản; không tạo thêm test sản phẩm chỉ để chứng minh phép cộng.

ĐỘ TIN: cao.

## CHƯA ĐO ĐƯỢC VÀ GIỚI HẠN

- Mã giao nộp H, 40 ca mới và 25 mutant chưa được đăng ký trong prototype; không khai đã chạy chúng.
- Lần đo đầu prototype (`selected-prototype.log`) có 131/132: `doctrine_scan_bom_cum_tu_do` gặp rc 1; test ấy không lưu stderr khi sai rc nên không xác định được nguyên nhân của lần đầu. Lần chạy lại cả tập đạt 132/132; kiểm riêng bổ sung 3/3 trên nền và 3/3 trên prototype đều đạt (`last-check.log`), không tái hiện rc 1. Giữ nguyên log thất bại, không quy thành lỗi hạ tầng đã chứng minh hay gọi đã loại hết flaky.
- Không chạy full selftest, toàn bộ packet-loop, Ruff, Windows hoặc CI. Không có approval/waiver/audit/land của H tương lai. N16 chưa đo.
- Số REST lịch sử, trạng thái server hiện tại, ruleset/bypass/branch-protection không thể suy từ mirror. Snapshot 385 ref không bác số 382 ở thời điểm tác giả.
- Hợp đồng KN-0/KN-1 được đọc và đối chiếu; chưa đóng lớp bằng lời hứa kế nhiệm. Không dùng prototype v1/v2 cũ làm v2 r2 đã nghiệm thu.
- Chỉ chạy fixture do người soạn cung cấp; hướng cần payload đường dẫn/chuỗi độc hại mới chỉ mô tả bằng lời. Phản chứng reviewer tự tạo chỉ xóa văn bản thường, tách bảng bằng dòng trống hoặc thêm `pass` vô hại trong scratch.
- Session ID/model/effort thực phục vụ chưa có nguồn đo riêng; không suy từ model yêu cầu trong spec. Assurance là đề nghị của assignment, không phải approval.

## KIỂM TRA CUỐI LƯỢT

`out/final-integrity.log`: HEAD/tree/base/băm đặc tả giữ đúng các giá trị đầu verdict; `git status --porcelain`, diff tracked và diff index đều rỗng. Có một tệp ignored `.claude/dev/__pycache__/launcher.cpython-313.pyc` đã được hồ sơ lượt 1 ghi nhận; lần tiếp tục này không có snapshot băm ignored đầu lượt nên không tuyên bố đã chứng minh toàn bộ lịch sử không ghi/hoàn nguyên. Lệnh Python dùng `-B`/`PYTHONDONTWRITEBYTECODE`, cache và test scratch đặt dưới `out/`.

Kiểm cấu trúc verdict: 12 hàng đối chiếu finding cũ; 13 slug còn mở khớp 13 mục finding; 4 P1 + 9 P2; 10 hướng săn có lệnh và output; mỗi finding đủ năm trường bắt buộc và gợi ý vá. Không có approval, API ghi, commit, push hoặc sửa checkout được review.
