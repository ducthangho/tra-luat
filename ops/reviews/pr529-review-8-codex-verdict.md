---
verdict: blocked
reviewed_sha: a4451ddb634da481581eea339282c1fe01c851b5
so_p1: 0
so_p2: 3
so_p3: 1
so_the_hien: 9
nghia_vu:
  N1: ĐẠT
  N2: ĐẠT
  N3: ĐẠT
  N4: ĐẠT
  N5: ĐẠT
  N6: KHÔNG ĐO ĐƯỢC
  N7: ĐẠT
  N8: ĐẠT
---

Reviewer độc lập: Codex / OpenAI, công cụ shell qua API trong sandbox được giao; không suy danh tính từ người sẽ vận chuyển biên bản. Không có header lượt gọi độc lập để chứng thực model chi tiết, nên không khai model/effort cụ thể. Không mạng, không push, không sửa `cay/` hay `mir/`. Các script, bản sao đột biến và log ở `review-artifacts/`.

Đã kiểm trước khi tin: `sha256sum goi/SPEC.md` → `507191dff0f8aee9734dfbea2bbe7c54a8d8f02cbf8224e37a132e168d10b229`; `wc -c` → `39554`; `git -C cay rev-parse HEAD` → SHA trên. Tree `06de906bea4255a66957a5995be94334b583bad6`; mirror 409 ref, shallow `false`. Các kết luận về repo chỉ áp cho snapshot này.

Đã tạo VERDICT trước phép đo đầu tiên. Nhật ký tăng dần, gồm output trước/sau sửa thước, ở [VERDICT-incremental.md](review-artifacts/VERDICT-incremental.md). Lệnh dưới chạy từ gốc sandbox. Script thoát 0 nghĩa là đã xuất báo cáo; boolean/rc con mới là kết quả phép đo, không đồng nhất rc script với nghĩa vụ ĐẠT.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Slug canonical | Phán duy nhất | Lệnh và output thật |
|---|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | **VÁ SINH LỖI MỚI** | `python3 -B review-artifacts/measure.py m17`: `clean_control=true`, `bad_body_rejected=true`, `bad_lease_rejected=true`, nhưng `valid_history_body_rejected=true`; lease:243 vẫn chứa A17. `python3 -B review-artifacts/finalchecks.py closure`: hai vế S12 spec/lease đều `true`. `python3 -B review-artifacts/extended.py pointers`: còn SPEC:26/439 và LEASE:129 viện dẫn M17. |
| `bien-nhan-thieu-so-ci-da-chi` | **VÁ HỜ** | `python3 -B review-artifacts/measure.py receipts`: lượt7 `ngan_sach=0`, `da_chi=KHONG_DO_DUOC`, IDs `[]`; lượt5 cả ba khóa `ABSENT`, `supplement_candidates=[]`. `python3 -B review-artifacts/measure.py ledger`: 253 dòng, min `08:15:01Z`, khác min khai `06:16:03Z`; hai khóa kết quả vẫn mang `trong_vong_doi`. |
| `phep-do-doctrine-khong-du-rang` | **CHƯA VÁ** | `python3 -B review-artifacts/extended.py doctrine`: baseline `rc=0`, chép đoạn trần ADR0048 `rc=0`, chép toàn §5.1 `rc=0`, đối chứng chép §12 `rc=6`; `scanner_unchanged_since_review7=true`. |

Hai sửa thật trong lớp CI được công nhận riêng: receipt7 không còn tự khẳng định chi 0; các phép đếm 0 dispatch/0 windows trong tập packet đúng. Chúng chưa đóng cả lớp. Receipt6 là lịch sử còn ghi 0; receipt7 không viết lại nó và cũng không chứng thực hồi tố giá trị ấy. Không yêu cầu sửa biên nhận bất biến.

## NGHĨA VỤ N1–N8

Thước do reviewer dựng. Phần đọc nghĩa là phán độc lập có neo văn bản; script không được mô tả thành bộ hiểu mọi văn bản tiếng Việt.

| Nghĩa vụ | Thước, lệnh | Output thật và phán |
|---|---|---|
| N1 | `python3 -B review-artifacts/measure.py oracles`. Vector đầy đủ `stop/class/count/drift`; tập khóa phải bằng, giá trị phải là bool, đích false và từng mục còn lại đúng kỳ vọng. | Gốc cả bốn `true`. Cả 7 đột biến A1'/A2' nhận tín dụng đúng vector. Oracle đúng `true`; all-green/all-red/missing/null/numeric/string/extra/wrong-target đều `false`. **ĐẠT** trong miền nghĩa vụ adapter này. |
| N2 | `python3 -B review-artifacts/extended.py units`; đọc từng câu/ô trong [N2-units-audit.tsv](review-artifacts/N2-units-audit.tsv); `python3 -B review-artifacts/more.py n2`. | 62 dòng thêm ở cross-review, 45 không trống, 18 M8 + 13 A1' + 31 A2', không đơn vị ngoài nhóm. Câu thời tiết ở ba vị trí đều bị reviewer bác. Đảo trình tự trong ô M8 vẫn đúng nhóm nhưng `drift: true → false`. **ĐẠT**; phân nhóm không tự miễn kiểm nội dung. |
| N3 | `python3 -B review-artifacts/measure.py delta`. Liệt kê toàn endpoint rồi mới phân loại; đọc toàn diff, không chỉ hai path sản phẩm. | `numstat_matches_packet=true`, hai sản phẩm +201, cross-review −0, `cross_base_lines_preserved=true`. Hai path tooling đều bằng blob master `d706abd`, không có delta sau merge `00ac525`. **ĐẠT**; đã thấy và giải trình đường ngoài write set, không giấu bằng lọc trước. |
| N4 | Cùng lệnh `oracles`, hàm kết luận nhận cả đối chứng dương và âm; đổi từng đối chứng vào cùng hàm đó. | `conclusion=true`; `force_positive_failure_conclusion=false`; `force_negative_failure_conclusion=false`. **ĐẠT**. |
| N5 | `python3 -B review-artifacts/extended.py pointers`, đọc thân §3.2/8/12/13/20 đã trích thành các tệp `section-*.md`; `python3 -B review-artifacts/more.py H6b`. | Mọi witness được liệt kê `true`; đọc nghĩa xác nhận trục review_class ở §3.2, assurance/exact head ở §8/13, lặp lớp ở §12, nợ/cổng ADR ở §20. Nợ severity khai rõ. **ĐẠT** cho con trỏ adapter được thêm, không phải chứng nhận mọi con trỏ trong SPEC/LEASE. |
| N6 | `python3 -B review-artifacts/measure.py receipts`; `python3 -B review-artifacts/measure.py ledger`; `python3 -B review-artifacts/extended.py hunts`; `python3 -B review-artifacts/more.py H4`. | Receipt7 dùng trạng thái đúng, nhưng receipt5 thiếu; ledger 253 ID duy nhất, 29 gắn packet, không chứng minh lịch sử đủ hay phân loại b. **KHÔNG ĐO ĐƯỢC** về tổng thực chi. Phần lời khai sai đã đo được được ghi thành finding, không làm tổng chi trở thành đo được. |
| N7 | `python3 -B review-artifacts/more.py n8` và các thước N1–N6 ở trên. | `N7_constructible` liệt kê đủ sáu hợp đồng thước. **ĐẠT**: không có nghĩa vụ nào phải đoán ý từ văn bản N1–N6. Thiếu CI là thiếu quan sát. |
| N8 | `python3 -B review-artifacts/more.py n8`. Chấm đầy đủ N1–N8, ≥6 hướng và approve tường minh. | `all_pass_explicit_approve=true`; `N6_unknown_approve=false`, `N7_missing_approve=false`, `clean_without_explicit_approve=false`, `missing_hunt_table=false`. **ĐẠT**; chính verdict này blocked vì N6 chưa đo được. |

Bảy đột biến bắt buộc đã chạy: đổi ô sensitive; gộp hai hàng; thay bảng dừng bằng con trỏ; bỏ cột phương án; bỏ bảng đơn vị đếm; bỏ nghĩa vụ mỗi finding một lớp; thay mục BẢNG LỚP bằng con trỏ. Vector quan sát và kỳ vọng đầy đủ ở [oracles.json](review-artifacts/oracles.json), bản đột biến ở `mut-*.md`. Không đếm chúng vào bảng săn.

Đối với N2, đánh số dòng theo nhóm chỉ ghi lại việc reviewer đã đọc; không có quy tắc “nằm trong vùng thì được chấp nhận”. Đã đọc toàn phần work-packet +139 theo các nghĩa vụ vòng lặp, M4–M6, hậu merge, CI và khai giới hạn; không thấy phần #521 bị xóa hay phần mới không có nguồn nhiệm vụ. `N3` không tách tác giả từng dòng resolution; giữ giới hạn đã chọn, không phục hồi công thức cộng hai khoảng.

Không thấy probe executor nộp làm bằng chứng nghiệm thu N1–N6. Các rc của cổng có sẵn và lời kể kết quả reviewer cũ nằm trong loại dữ kiện được M16 cho phép; không dùng chúng để tự cấp ĐẠT. Việc lease khai “ZERO” tên cũ sai là lời khai bị phép reviewer bác, chưa phải bằng chứng executor nộp một probe cấm.

## M17' VÀ LEDGER BẢN 3

### M17'

Thước lấy tập 10 tên từ dòng “Tập tên đầy đủ”, xác định đúng heading `## PHỤ LỤC A` ở đầu dòng, kiểm phần trước heading và toàn lease. Đối chứng trên bản sạch cô lập rồi thêm câu vận hành có tên: đỏ ở cả thân và lease. Cùng câu lịch sử chỉ rút hiệu lực, đặt ngoài phụ lục bị bác, đặt trong phụ lục được nhận. Không có payload nhạy cảm.

**Có răng về vị trí tên. Không đóng lỗi bắt oan về nghĩa.** Câu thật tại LEASE:243–245 nói S8/A17 đã rút và không được dùng tiếp. Nó hợp lệ về nghĩa, nhưng luật mới cấm nó trên toàn lease. Câu đột biến “A17 đã rút ở r6; không được dùng làm nghĩa vụ hiện hành.” xác nhận không cần dựa vào cách ghi YAML để tái hiện. Đây chính là lịch sử hợp lệ mà luật vị trí tiếp tục loại, chỉ chuyển yêu cầu miễn trừ từ nhãn sang vùng.

Không phán laundering khi văn bản nằm trong Phụ lục A: cả vùng đó phi quy phạm nên một câu ở đó không tự có quyền cấp nghĩa vụ. Hai cửa laundering theo nhãn/ô cũ đã đóng theo định nghĩa vùng. Đó là phần sửa thật.

Giá văn phong đã có điểm cụ thể: SPEC:26 đòi đọc “M17 bên dưới” nhưng không còn mục M17; SPEC:439–440 tiếp tục giới thiệu M17 như lối ra cuối mục dừng. Người đọc phải tự hòa giải với mục M17' ở trên. Không cần tìm câu vô nghĩa để công nhận đây là con trỏ khó tra trong chính hợp đồng đang dùng.

Phép quét theo ranh giới từ còn bắt `A9` trong slug nợ SPEC:368. Thước theo nguyên identifier không bắt nó: [closure.json](review-artifacts/closure.json) cho thân `[]`, còn LEASE:243 vẫn bị bắt. **Không lấy ca slug này làm finding chắc chắn**, vì nghĩa “chứa tên” với tên ghép chưa được quy định rõ. Phản chứng lịch sử lease không phụ thuộc lựa chọn đó.

**Đã đọc toàn bộ SPEC và LEASE theo khái niệm**, không chỉ chạy regex; biên bản từng phần ở [concept-read.md](review-artifacts/concept-read.md). Không tìm thấy câu cấp lại sáu tiêu chí đã rút để quyết delta, whitelist, số bảy ca hay định nghĩa severity. Các đoạn ba lượt trước đã sửa về nội dung vẫn sạch. Tuy nhiên, câu trả lời cho “còn luật cũ đang cấp nghĩa vụ không?” trên toàn hợp đồng là **có ở cấp cơ chế M17**: LEASE:129 vẫn viết “Luật chung nay là M17 của r8”; SPEC:439–440 vẫn giới thiệu nó làm lối ra. M17 đã bị r9 thay, và không thuộc tập tên mà M17' quét.

Giới hạn chỉ phủ TÊN không được văn bản N1–N8 dùng để miễn đọc nghĩa: SPEC:179–183 buộc reviewer đọc mỗi lượt. Tôi đã thực hiện nó và để kết quả chi phối blocked. `S12'` chiếu đầy đủ **ĐÃ VÁ THẬT**: cả spec và lease có vế hạ luật xuống báo cáo. Lease thêm S13'; spec không có ID S13' riêng nhưng đã có cùng nghĩa vụ cấm tên ở M17', nên không tự tạo finding chỉ vì khác số nhãn.

**Phán thiết kế:** bỏ cả M17/M17' khỏi vai trò cổng nghiệm thu. Có thể giữ phụ lục lịch sử như cách tổ chức tài liệu, nhưng không lấy vị trí một tên làm chứng nhận không còn luật cũ. Phép đọc khái niệm độc lập phải tiếp tục có thẩm quyền và fail-closed theo N7/N8. Chủ kho cần sửa đồng bộ những câu vận hành còn gọi M17 và điều kiện dừng liên quan; không vá regex hay thêm ngoại lệ lần ba. Đây là đề nghị về lớp, không phải patch executor phải chép.

### Ledger

`python3 -B review-artifacts/measure.py ledger` tái đếm độc lập JSON, không lấy bảng kết quả làm oracle.

| Mệnh đề | Kết quả |
|---|---|
| 253 bản ghi, 253 ID duy nhất; 29 bản ghi gắn packet | **KHỚP** trong tập đã nộp. |
| 0 event dispatch toàn tập; 0 dispatch và 0 windows trong 29 packet | **KHỚP**, đúng cột chứng minh được khi giới hạn trên tập. |
| Hai bản ghi attempt khác 1, không gắn packet | **KHỚP**, IDs 34689095386 và 34707637324. |
| Cửa sổ của tập 253 là 06:16:03–21:42:48, phủ từ trước lease | **KHÔNG KHỚP**: min thực 08:15:01, 0 bản ghi trước lease 08:15:00. Câu này bị xếp sai vào “chứng minh được” ở cả MD và JSON. |
| Tổng thực chi=0, loại b=0, workflow chưa từng chạy, tập đầy đủ | **Đúng cột KHÔNG chứng minh được**. Không biến các câu ấy thành khẳng định dương. |
| Đã gỡ hết kết luận/khóa đọc rộng hơn tập | **CHƯA**: `run_TOAN_KHO_trong_vong_doi_packet`, `phan_bo_event_TOAN_KHO_trong_vong_doi` còn nguyên; tên collection cũng còn `trong_vong_doi`. |

Ngoài hai cột, `sua_gi_so_ban_1` còn kể “Ban 2 nop TOAN BO ban ghi trong cua so”, và provenance khai 283 bản ghi duy nhất nhưng chỉ nộp 253. Không thể tái dựng 30 bản ghi trước lease hoặc bốn trang ban đầu từ gói này. Không kết luận 30 bản ghi bị cố ý giấu; chỉ nói mệnh đề đủ/cửa sổ trước lease chưa có chứng cứ trong hiện vật.

Min của tập không chứng minh rằng không có run trước min. Vì thế cũng không lấy sai lệch một giây ở đầu tập làm chứng cứ packet đã chi trái phép. `as_of` 01:38:55 ngày13 không tự lấp phần sau 21:42:48 ngày12; còn thiếu lịch sử đến thời điểm chốt nghiệm thu.

## BẢNG SĂN

Sáu hướng dưới độc lập về kiểu lỗi đang săn. Không tính phép canonical M17, receipt5/7, scanner hay bảy đột biến adapter vào sáu hướng này.

| # | Hướng mới / nghĩa vụ | Lệnh đã chạy | Output thật và phán |
|---|---|---|---|
| H1 | N1/N4: giá trị sai kiểu vẫn truthy hoặc thừa khóa có mua tín dụng không? Khác ca thiếu quan sát cũ. | `python3 -B review-artifacts/measure.py oracles` | `null=false`, `numeric=false`, `string=false`, `extra=false`, correct `true`. **SẠCH** trong schema reviewer; không ép kiểu 1 hay chuỗi thành bool. |
| H2 | N7/N8: miền biên M5 ở đúng 50%, vòng undefined chen giữa, vòng xác định ngắt chuỗi. | `python3 -B review-artifacts/extended.py hunts` | exact_half `false`; undefined_gap `true`; reset_defined `false`; empty_only `false`; just_below `true`. Cả 5 khớp kỳ vọng từ văn bản. **SẠCH**; phép mô hình hóa luật chữ, không khai cổng sản phẩm cưỡng chế M5. |
| H3 | N6: run ID và attempt có cùng đơn vị không? | Cùng lệnh `extended.py hunts` | 2 ID attempt=2, suy ra 4 attempt theo bộ đếm nhưng chỉ 2 bản ghi trạng thái hiện tại; packet_rerun_records=0. **Không thấy lỗi gắn packet trong tập**; lịch sử attempt riêng còn cần nếu đếm tổng lượt. Không lặp phép đếm dispatch=0. |
| H4 | N6: trường `thuoc_packet_qua` có tự gắn sai bản ghi không? Đối chiếu khóa PR/branch độc lập và Git ancestry. | `python3 -B review-artifacts/more.py H4` | attached=29; known_ancestry=29; `attribution_mismatches=[]`. **SẠCH** với hai khóa quan sát; ancestry không tự biến mọi run master thành chi phí packet. |
| H5 | N7: chú giải trường neo hiện tại có còn gọi giá trị generation trước không? | `python3 -B review-artifacts/extended.py hunts` | raw start/required đều a4451dd; prose 00ac525; `prose_matches_field=false`. **LỖI P3**, chú giải trôi; không gọi SHA máy là sai. |
| H6 | N5: đi qua §20 có nhận ra ADR0043 bị thay một phần bởi ADR0048, hay áp mù tiêu đề trần cũ? | `python3 -B review-artifacts/more.py H6b` | superseded marker `true`; successor chỉ đổi trục vòng `true`; cả hai ô registry 0 cổng `true`. **SẠCH**; r9 ngày13 sau mốc ngày12, không suy đổi trục call/attempt từ trần vòng. |

H1 kiểm kiểu kết quả; H2 kiểm chuỗi thời gian hội tụ; H3 kiểm đơn vị đếm sự kiện; H4 kiểm quy thuộc đối tượng; H5 kiểm tính nhất quán neo/chú giải; H6 kiểm hiệu lực nguồn thay thế. Không dùng sáu biến thể của cùng một regex làm sáu hướng.

## BẢNG ĐO

| Khẳng định / đối tượng | Đo thật | Khớp? |
|---|---|---|
| Băm SPEC, số byte, SHA | đúng băm yêu cầu / 39554 / a4451dd đầy đủ | Có |
| Mirror | 409 refs, shallow false | Có trong sandbox; chưa đối chiếu nguồn live |
| Delta sản phẩm | 2 tệp, +201, không xóa cross-review nền | Có |
| Hai tooling ngoài danh sách | hai blob bằng d706abd, không đổi sau merge | Có nguồn; không cáo buộc vượt scope |
| M16 dữ kiện executor | không có probe nghiệm thu trong gói; cổng có sẵn được phép | Không thấy vi phạm S11' |
| Bảy chốt A1'/A2' | 7 vector làm đỏ đúng đích, đầy đủ không-đích | Có trong miền đã đo |
| S12' hai vế | cả spec/lease true | Đã vá thật |
| Lease khai không tên đã rút | LEASE:243 vẫn A17 | Không |
| M17' không bắt oan | câu chỉ rút hiệu lực vẫn đỏ ngoài phụ lục | Không |
| Nội dung sáu tiêu chí cũ | không thấy nghĩa vụ vận hành tái cấp | Sạch khi đọc nghĩa |
| M17 đã được thay hết ở câu vận hành | spec còn lối ra M17, lease còn “Luật chung nay” | Không |
| Ledger số hẹp | 253/29/0 dispatch/2 rerun khớp | Có |
| Ledger cửa sổ trước lease của 253 | thực từ 08:15:01 | Không |
| Receipt7 phân biệt budget/chi chưa biết | 0 / KHONG_DO_DUOC | Có |
| Receipt5 bổ sung | không tìm thấy trong danh mục, EVIDENCE cũng khai chưa có | Chưa |
| Doctrine trên cây thật | `finalchecks.py gates`: rc0, 7 tệp, 0 cụm | Có, không chứng nhận không chép nghĩa |
| ADR registry | rc0, 48 ADR/48 dòng §20 | Có |
| `git diff --check` worktree | `scope-check.json`: rc0 | Khớp lệnh EVIDENCE |
| Endpoint sản phẩm diff-check | rc0 | Sạch |
| Endpoint toàn gói diff-check | rc2, whitespace ở verdict lượt1:117–118 | Có lệch với worktree do **khác đầu vào**, không cáo buộc lời khai rc sai, không đòi sửa hiện vật bất biến |
| `git status --porcelain` của cay | rc0, stdout rỗng | Reviewer giữ cây sạch |

Không chạy lại `doc-claims-check`, `release-verify`, `bien_nhan_v2`, `tl.py --selftest` hoặc CI live; những rc do EVIDENCE khai không trở thành kết quả reviewer. Các cổng đã chạy ở [gates.json](review-artifacts/gates.json); giới hạn diff-check ở [scope-check.json](review-artifacts/scope-check.json).

## PHÁT HIỆN

Mỗi slug là một lớp; severity giữ cách dùng của kho, không tự dựng định nghĩa doctrine P1/P2/P3. `so_the_hien` đếm phản chứng/mệnh đề vận hành, không đếm mỗi token lặp hoặc mỗi bản MD/JSON của cùng một khẳng định.

| Lớp / slug | Hạng | Thể hiện | Bản vá theo lớp / lý do |
|---|---|---:|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | P2 | 3 | Bỏ cổng phân vùng tên; thu hồi nhất quán cơ chế cũ trong spec và lease; reviewer đọc nghĩa có quyền chặn. |
| `bien-nhan-thieu-so-ci-da-chi` | P2 | 3 | Khai đúng tập quan sát, nộp nguồn CI đủ và bổ sung lịch sử bằng hiện vật mới được chủ kho cho phép; không sửa receipt cũ. |
| `phep-do-doctrine-khong-du-rang` | P2 | 2 | Chủ kho quyết packet/scope riêng; S4 cấm vá scanner tại đây. |
| `chu-giai-lease-neo-head-cu` | P3 | 1 | Đồng bộ chú giải với hai giá trị neo máy hiện tại, ghi rõ đoạn cũ chỉ là lịch sử nếu giữ. |

### `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi`

Ba thể hiện: (1) M17' bắt oan lịch sử hợp lệ — câu S8 trong LEASE:243 là ca thật, đồng thời chứng minh lời khai ZERO sai; (2) SPEC:26/439–440 còn dẫn cơ chế M17 đã thay, một đường đọc spec cũ; (3) LEASE:129 tiếp tục trao nó tư cách “Luật chung nay”, đường vận hành lease cũ. Không tách thành các slug mới để tăng số lớp. Không đếm thêm ca A9 nằm trong slug vì ranh giới tên còn hai cách đọc.

Tác động: thay kiến trúc chưa loại được cơ chế đọc sai; cổng vị trí còn tạo lý do dừng với câu hợp lệ, trong khi không phát hiện việc văn xuôi cấp lại M17. Hai hướng đo khác nhau — bắt oan và bỏ sót cơ chế cũ — cùng cho thấy đây chưa phải bản đóng lớp. Việc sửa thuộc chủ kho vì cần quyết cơ chế, không phải reviewer sửa SPEC.

### `bien-nhan-thieu-so-ci-da-chi`

Ba thể hiện: (1) receipt5 không có bộ ba CI và chưa có bổ sung; (2) ledger mô tả tập 253 phủ từ trước lease nhưng dữ liệu không chứa phần ấy; (3) các khóa/bản khai đầy đủ vẫn đọc như kết luận vòng đời, trái cột giới hạn mới. Một mệnh đề cửa sổ được in ở cả MD và JSON chỉ đếm một lần; các tên khóa cùng tuyên phạm vi toàn thể là một thể hiện cấu trúc.

Tác động: người đọc vẫn có thể nhận một cận quan sát làm chứng minh vòng đời. Receipt7 đã sửa thật; không phủ nhận sửa đó và không cáo buộc executor gọi CI trái phép.

### `phep-do-doctrine-khong-du-rang`

Hai thể hiện là hai loại sao chép nghĩa chưa bị bắt: đoạn trần ADR0048 và toàn §5.1. Bản gốc/ADR/§5.1 rc0, §12 rc6 trên các bản sao độc lập cùng scanner. Các tệp fixture và log được giữ. S4 giải thích không vá trong packet; không biến nợ thành đã đóng.

### `chu-giai-lease-neo-head-cu`

LEASE:133–136: `start_from_sha` và `reviewed_sha_required` đều là a4451dd đầy đủ, nhưng trường chú giải tiếp theo viết “BẰNG start_from_sha (00ac525), tức head TẠI LÚC CẤP”. `H5.json` cho `prose_matches_field=false`. Đây là lời giải thích hiện tại sai, không phải yêu cầu đổi hai neo đúng. Chú giải có thể làm bàn giao lạnh chọn nhầm mốc; hạng P3 vì trường máy và SHA giao reviewer vẫn đúng. Khác lớp tiêu chí cũ: dữ liệu định danh bị trôi, không phải cơ chế nghiệm thu bị phục hồi.

## KHÔNG ĐO ĐƯỢC

- **N6 tổng CI thực chi và run IDs loại b:** cần lịch sử từ mốc mở packet có thẩm quyền đến mốc chốt hiện tại; các trang/raw response có thời gian lấy, provenance và dữ liệu đủ tái dựng phạm vi; nguồn phân loại từng run/attempt theo tự động, đo thủ công, thăm dò (event đơn lẻ không đủ); run ID và attempt cho lượt chạy lại; dấu vết bền xử lý khả năng run bị xóa. Không bắt buộc số phút để đóng N6. Nếu không có chứng cứ đủ thì giữ KHONG_DO_DUOC, không thay bằng danh sách rỗng được diễn giải là không chi.
- Cần một hiện vật bổ sung cho receipt5 theo hợp đồng được chủ kho chấp nhận, neo đến biên nhận cũ. Không tự dựng thẩm quyền cập nhật lịch sử và không sửa receipt bất biến. Receipt6 số0 cũng không được hồi tố thành đã chứng minh chỉ nhờ receipt7 dùng trạng thái đúng.
- Không truy cập GitHub nên không xác minh trực tiếp head live, dispatch history, dữ liệu đã xóa, model thực thi cũ hoặc quyền cấp lease. Không suy các thiếu hụt ấy thành vi phạm đã xảy ra.
- Không chứng minh scanner tổng quát hay một oracle ngôn ngữ tổng quát. Phạm vi ĐẠT N1–N5 là nghĩa vụ và câu/ô adapter của packet đã đọc và đột biến, không phải mọi cách diễn đạt có thể có.
- Không soạn đường dẫn thoát cây hay payload nhạy cảm. Hướng cần điều phối đo hộ nếu muốn mở rộng: kiểm phân loại đường dẫn với tên biểu diễn đặc biệt/thoát cây, kiểm công cụ có chuẩn hóa về đúng gốc trước khi quyết phạm vi. Hướng này chưa chạy và không tính trong bảng săn.

Hai sửa thước công khai: lần đầu m17 bắt nhầm chuỗi nhắc heading, thoát1, đã đổi sang heading neo dòng; lần đầu doctrine chọn đoạn ADR0043 chứa cụm cấm khác nên rc6, không phải canonical ADR0048, đã đo lại đúng fixture. Giữ log cũ và không dùng chúng làm finding. Sau kiểm thứ hai, không dùng ca slug A9 làm finding vì phụ thuộc ranh giới token. Không giấu output bất lợi cho thước.

## KẾT LUẬN

**blocked, không approve.** N1–N5 và N7/N8 đo được ĐẠT trong phạm vi nêu trên; N6 KHÔNG ĐO ĐƯỢC tự chặn approve. Ba lớp P2 còn mở, cộng một lớp P3 chú giải neo: tổng bốn lớp / chín thể hiện.

S12' chiếu lease đã vá thật, receipt7 dùng KHONG_DO_DUOC đã vá thật, các số hẹp ledger khớp, và phần nội dung sáu tiêu chí cũ không còn cấp nghĩa vụ. Nhưng M17' không phải cơ chế đáng vá lần ba: đề nghị bỏ nó khỏi cổng nghiệm thu, giữ phép đọc khái niệm reviewer có thẩm quyền. Chủ kho quyết sửa hợp đồng và đường bổ sung CI/scanner; reviewer không sửa repo hay nới nghĩa vụ để đóng lượt.
