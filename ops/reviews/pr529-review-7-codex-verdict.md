---
verdict: blocked
reviewed_sha: 6e7340312e01c39597f5c38df91538b022c945eb
so_p1: 0
so_p2: 3
so_p3: 0
so_the_hien: 8
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

Reviewer độc lập: OpenAI Codex, model theo môi trường phiên là GPT-6; bề mặt agent/API có shell, transport machine. Không suy danh tính từ tài khoản GitHub, không tự khai run ID chưa được cấp. Chỉ đọc cây `cay/` và mirror `mir/` trong sandbox; scratch và thước do reviewer viết ở `review-artifacts/`. Không mạng, push, sửa cây được review hay sửa receipt đã giao.

**Kết luận: blocked; KHÔNG approve.** Có 3 lớp P2, 8 thể hiện còn mở. N6 tự chặn approve theo N8. P2 giữ cách phân hạng canonical của ba lớp; không sáng tạo định nghĩa severity mới. Các ca đột biến của reviewer là chứng cứ về khả năng của thước và văn bản, không phải lời khai đã đo hành vi runtime của agent.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Mỗi slug đúng một nhãn. Lệnh dưới chạy từ gốc sandbox; JSON ghi cả argv Git/scanner và mã thoát thực.

| Slug canonical | Phán lượt 7 | Lệnh và output thật |
|---|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | **VÁ SINH LỖI MỚI** | `python review-artifacts/canonical.py`: đọc blob r7 và lease gen6 rc0; ba chỗ cũ đã viết lại. `python review-artifacts/m17.py`: baseline SPEC và LEASE đều `actual_violations=[]`; ca tên trần/nhãn sau/bullet khác bị bác, nhưng `label_laundering=true`, `table_laundering=true`, `valid_history=false`. `python review-artifacts/closure.py`: chốt hạ thành báo cáo ở spec `true`, lease `false`. |
| `bien-nhan-thieu-so-ci-da-chi` | **VÁ HỜ** | `python review-artifacts/ledger.py`: lease gốc đọc rc0, mốc 08:15Z khớp; 253 ID duy nhất, phân bố 132/66/55 khớp. Receipt5 ba trường đều `[]` trong kết quả regex, nghĩa là **không có trường**; receipt6 có ngân sách `0`, số chi `0`, run IDs `[]`, nhưng chưa đủ căn cứ cho số chi. |
| `phep-do-doctrine-khong-du-rang` | **CHƯA VÁ** | `python review-artifacts/canonical.py`: baseline `rc=0`, copy ADR `rc=0`, copy §5.1 `rc=0`, đối chứng copy §12 `rc=6`; diff scanner giữa base/head rỗng. |

[Log canonical](review-artifacts/canonical.json), [M17](review-artifacts/m17.json), [CI](review-artifacts/ledger.json), [chốt lease](review-artifacts/closure.json).

**Ba thể hiện đặc tả của lượt 6, xét riêng đều đã sửa thật:**

- SPEC r7:287–291 dùng A18 quyết phép đo/cách dừng; r8 mục `chua_do_duoc` số 5 dùng N1/N2, reviewer dựng thước, S7 quyết dừng. Không còn giao quyền cho A18 tại đây.
- LEASE gen6:121–125 dùng A17 làm căn cứ base; gen7:124–132 dùng N3 và một endpoint cố định.
- LEASE gen6:155–160 buộc bảy ca theo A18; gen7:162–170 giao phép đo cho reviewer và nói rõ executor không đặt số ca.

**Câu hỏi trực tiếp:** qua đọc toàn bộ SPEC/LEASE hiện hành và danh mục các đơn vị chứa tên, tôi **không tìm thấy một câu hiện hữu còn lấy A9/A16–A20, hoặc công thức cộng hai khoảng, làm nghĩa vụ vận hành** như ba câu trên. Kết luận này là kết quả đọc và đối chiếu khái niệm; không suy nó từ `actual_violations=[]`. Finding hiện hành là thiết kế thay thế cho phép tái đưa luật cũ vào, bắt oan lịch sử hợp lệ, và một chốt mới chưa được chiếu sang lease.

**Ba thể hiện CI của lượt 6:** thiếu receipt5 vẫn còn; lỗi mốc commit đã sửa thật thành lease; vấn đề suy luận từ tập quan sát vẫn chưa đóng. Receipt6 khôi phục **hình dạng** khối CI nhưng không chữa receipt5, đồng thời thêm một lời khai số chi không được chứng thực. Không đếm mỗi trường thiếu thành một thể hiện.

## NGHĨA VỤ N1–N8

Các thước đều do reviewer viết. `obligations.py` dùng bộ witness nội dung được chọn sau khi đọc adapter; `audit.py` ghi catalogue từng đơn vị đã đọc. Đây là phép đọc có thể làm đỏ trên văn bản cụ thể, không phải bộ hiểu mọi cách diễn đạt tiếng Việt.

| Nghĩa vụ | Thước độc lập, lệnh | Output thật và phán |
|---|---|---|
| N1 | `python review-artifacts/obligations.py`: quan sát riêng 10 chốt; cấp tín dụng chỉ khi tập quan sát bằng đúng tập kỳ vọng, giá trị là boolean, đích false và mọi không-đích đúng. | Baseline 10 chốt đều true; 10 đột biến bỏ nghĩa vụ đều đỏ đúng đích và có đủ không-đích. Oracle luôn xanh, tất cả đỏ, thiếu không-đích, sai đích, dư quan sát, giả boolean đều false; oracle đúng true. **ĐẠT** trong phạm vi adapter này. |
| N2 | `python review-artifacts/audit.py`: đọc 52 đơn vị thêm, gắn nhóm từng nội dung; không cấp quyền qua từ khóa hay đoạn lân cận. Catalogue và văn bản đầy đủ nằm ở `semantic-units.json`. | Thêm vô hại đứng riêng `[false]`, kề nhóm hợp lệ `[true,false]`, chỉ chứa từ khóa `[false]`; chuyển hai đơn vị hợp lệ `[true,true]`. Đổi nội dung hàng sensitive thành severity-only làm `stop=false`, các chốt khác true. Cross-review có 18+44 dòng insert; work-packet 139; không xóa byte master. **ĐẠT**. |
| N3 | `python review-artifacts/obligations.py`; `python review-artifacts/delta_mutation.py`; H5 của `hunts.py`. Liệt kê **toàn** endpoint trước phân loại nguồn. | 17 đường: 2 sản phẩm +201/−0; 13 review +3232/−0; 2 tooling +50/−5 nhập từ master. Hai tooling bằng blob `d706abd` (diff rc0 rỗng). Fixture merge xung đột rc1, viết 305 dòng khi giải xung đột ⇒ endpoint `305/1 product.md`, bị bác trần300; đường in-tree ngoài danh sách hiện trong full diff, vắng trong filtered diff. **ĐẠT**; không coi 2 tooling là tác giả lén ghi. |
| N4 | `python review-artifacts/obligations.py`: bốn nhóm đối chứng đi vào phép hội quyết kết luận. Lần lượt làm hỏng từng nhóm. | Baseline, mutations, reject-faults, accept-correct đều true; phá riêng từng nhóm cho kết luận false cả bốn. Đối chứng không chỉ được in ra. **ĐẠT**. |
| N5 | `python review-artifacts/obligations.py`: trích đúng thân §3.2, §5, §8, §12, §13, §20, kiểm lời hứa cụ thể; đọc nợ severity riêng. | 12 witness khái niệm đều true; §12 thiếu P2 và §8 thiếu P3 đúng như giới hạn được khai. Đích §8/13 có hợp đồng review/head; §12 có ngưỡng và lặp lớp; §20 có ADR/0 cổng. Không dùng con trỏ cho nguyên nhân head đổi hoặc định nghĩa severity mà đích không có. **ĐẠT**. |
| N6 | `python review-artifacts/ledger.py`; H1–H3 của `hunts.py`; đọc trực tiếp receipt4/5/6. | Tái đếm tập nộp được; không chứng minh tổng loại(b), tính đầy đủ lịch sử hoặc phần bổ sung receipt5. **KHÔNG ĐO ĐƯỢC**. Những lỗi khai số chi vẫn là finding, không biến thành ĐẠT vì schema xanh. |
| N7 | `python review-artifacts/obligations.py` và các thước trên: từ văn bản xác định đối tượng, kỳ vọng, dữ liệu cần cho N1–N6. | `N7_constructible` cả sáu true. Không có nghĩa vụ nào tôi phải đoán ý mới dựng được thước. N6 thiếu dữ liệu, không thiếu văn bản. **ĐẠT**. |
| N8 | `python review-artifacts/obligations.py`: bảng ba trạng thái; kiểm front matter verdict cuối bằng `verify_verdict.py`. | Chỉ ĐẠT cho phép qua; KHÔNG ĐẠT và KHÔNG ĐO ĐƯỢC đều false. N6 giữ trạng thái thứ ba; verdict blocked. **ĐẠT**. |

[Toàn bộ quan sát](review-artifacts/obligations.json), [audit từng đơn vị](review-artifacts/audit.json), [văn bản 52 đơn vị](review-artifacts/semantic-units.json), [fixture delta và argv thật](review-artifacts/delta_mutation.json).

Giới hạn N2 được giữ đúng: phân nhóm không tự chứng minh đúng nội dung. Tôi đọc các ô và câu trong 52 đơn vị, đồng thời đo nội dung bằng các chốt riêng; không dùng câu giới hạn để miễn sai nội dung. Catalogue hữu hạn sẽ cần reviewer đọc thêm khi có câu mới; nó không phải một cổng ngôn ngữ tổng quát.

## M17 VÀ LEDGER BẢN 2

### M17

Lệnh `python review-artifacts/m17.py`; đầu vào từng ca được lưu thành `review-artifacts/m17-*.md`. `allowed` nghĩa là phép diễn dịch đúng ba ngoại lệ cú pháp **cho qua**, không phải nội dung đã được reviewer approve.

| Ca | allowed thật | Đánh giá |
|---|---:|---|
| `A18 buộc BẢY ca.` | false | Có răng với câu vận hành trần. |
| Nhãn ĐÃ RÚT đứng sau tên trong cùng dòng | false | Có răng về thứ tự ký tự. |
| Bullet lịch sử sát bullet vận hành khác | false | Không che được đơn vị danh sách kế tiếp. |
| `[LỊCH SỬ] Tiêu chí A18 không còn hiệu lực kể từ r6.` | true | Đối chứng lịch sử có nhãn khớp. |
| `[LỊCH SỬ] Đoạn trước đã hết hiệu lực. Hiện nay A18 buộc BẢY ca.` | true | **Lọt** câu cấp nghĩa vụ trong cùng đơn vị. Vị trí nhãn không chứng minh phạm vi nghĩa của nhãn. |
| Hàng bảng có ô A17 quyết base hiện hành và ô khác ghi ĐÃ RÚT | true | **Lọt** do ngoại lệ hàng bảng, kể cả tên đứng trước nhãn. Luật hàng #1 còn tự làm yếu khẩu quyết “nhãn trước tên”. |
| `Tiêu chí A18 không còn hiệu lực kể từ r6.` | false | **Bắt oan theo hợp đồng ngữ nghĩa:** câu rút hiệu lực rõ ràng, không cấp nghĩa vụ nào. Đây là vi phạm cú pháp M17 có chủ đích, không phải lỗi parser; chính lựa chọn ép văn phong là đối tượng review. |
| `Phép đếm đúng phải cộng hai khoảng trước và sau merge.` | true | M17 riêng lẻ không phủ luật không tên. |

**Giới hạn không tên có phải miễn nghĩa vụ?** Không thể kết luận chỉ từ ca cuối rằng cả r8 cho phép công thức cũ: S12' vẫn bắt buộc quét khái niệm và N3 vẫn cấm cách đếm đó. Tôi không đếm ca này thành một finding độc lập. Tuy nhiên, nó bác việc dùng M17 riêng làm chứng minh “đóng cả lớp”. Hai ca **có tên** nhưng được nhãn/hàng bảng che còn bác thẳng tuyên bố ở SPEC:437–438 và LEASE phần đầu rằng phép tách không cần đọc ý nghĩa câu. Nhãn cú pháp chưa thay được kiểm nội dung.

**Không được dùng kết quả quét baseline sạch làm bằng chứng quy trình trước freeze:** không có raw cuộc thực thi freeze; lượt này chỉ đo văn bản và đột biến. S12' bản r8 thêm vế hạ thành báo cáo tại SPEC:423; LEASE:257–261 giữ bản r7. `python review-artifacts/closure.py` cho `spec=true / lease=false` với đúng vế mới. Trong tình huống quét theo khái niệm nhưng hạ một luật thành báo cáo, spec yêu cầu dừng, riêng danh sách lease không bắn. Spec vẫn là nguồn cao hơn; điều đó giảm rủi ro nhưng không làm lời hứa “lease chép đúng spec” thành đúng.

### Ledger bản 2: chấm năm phần sửa

| Phần sửa | Đo thực tế | Kết luận |
|---|---|---|
| Mốc | `ledger.py` đọc blob lease gen1 từ mirror rc0, `leased_at_utc=2026-09-12T08:15:00Z`. | **Sửa thật mốc đã biết**. Chưa chứng minh mốc mở Issue chính xác hoặc câu “lease sớm hơn Issue”. |
| Cửa sổ | Khai `06:16:03Z…21:42:48Z` ngày12; `as_of=2026-09-13T01:05:51Z`; chênh đuôi **12183 giây = 3:23:03**. | Phần đầu khai bao mốc lease; không có chứng cứ query tới as_of. Không suy có run bị bỏ sót từ khoảng trống, nhưng không thể chứng nhận cửa sổ đầy đủ. |
| Raw toàn kho | 253 records, 253 ID duy nhất; push132, pull_request_target66, pull_request55; dispatch0. | **Tái đếm được tập nộp**, tiến bộ thật so với 29. Chưa phải raw mọi page: 30 trong 283 ID khai duy nhất không được nộp. |
| run_attempt | Đủ trường cho 253/253; hai run có attempt2 đúng ID đã kê. | **Sửa thật trường thiếu**; snapshot attempt mới nhất không thay lịch sử attempts/jobs hay ý định gọi lại. |
| Provenance | 400 downloads − 283 unique =117 bản trùng là khả dĩ. Không có bốn response/page envelope, request đầy đủ, timestamp từng page hay 400 records gốc. | **Lời giải thích số học hợp lý**, chưa tái dựng/kiểm được union, thứ tự đơn điệu, ranh giới trang hoặc việc lấy đủ. |

**Số 0 chứng minh chính xác:** trong **253 bản ghi được nộp**, không bản nào có trường event bằng workflow_dispatch; 29 bản được gắn packet cũng không có. Nó không chứng minh mọi run trong toàn cửa sổ đã được nộp, không chứng minh số loại(b) là0, tổng attempts là0, không có run bị xóa, hoặc không có hoạt động sau21:42:48Z. Không cần phút billable để chấm nghĩa vụ đếm lượt này.

Bản2 tách dispatch khỏi tổng chi là đúng, nhưng chưa nhất quán xuyên hiện vật: receipt6:42–50 vẫn ghi số chi loại(b)=0 và dùng số dispatch để giải thích; MD:15–19 vẫn dùng “trong vòng đời” và “chưa từng chạy cho packet”. Đây là các khẳng định rộng hơn tập chứng minh được. Trong raw có **41 run trên nhánh spec/lease liên quan #523 bị để ngoài tập29**; không tự gán tất cả cho packet hay loại(b), nhưng cần giải thích quan hệ hỗ trợ thay vì coi nhánh thi công/PR529 là đầy đủ. Đặc biệt có run ops-publish-lease trên nhánh cấp lease522–523; “chưa từng” chỉ có thể giữ khi giới hạn rõ là tập29 đã chọn.

Mục KHÔNG ĐO ĐƯỢC của ledger vẫn im lặng về khoảng đuôi tới as_of, phần raw/trang chưa nộp, lịch sử attempts/jobs và độ bao phủ của quy tắc gắn packet. Đã nói rõ phân loại chi/run bị xóa là tốt, nhưng chưa đủ cho N6.

## BẢNG SĂN

**Sáu hướng độc lập**, không tính đột biến canonical vào số hướng. Cùng một lệnh `python review-artifacts/hunts.py` chạy cả sáu, output ở [hunts.json](review-artifacts/hunts.json). Đây là những trục khác nhau; các ca canonical M17/scanner ở phần trên không được đếm lại. H1 săn bảo toàn tập qua phân trang, không tính phép thử thiếu đầu/đuôi đơn thuần của lượt5 làm hướng mới.

| Hướng | N liên quan | Câu hỏi và output thật |
|---|---|---|
| H1 — bảo toàn tập qua bốn lần lấy | N6/N8 | 400/283/253 ⇒117 downloads trùng,30 unique không nộp; `page_envelopes_supplied=false`, không tái dựng union/đơn điệu được. Fixture có watermark đủ true; query watermark stale dù khai endpoint đủ false. Chưa có raw để phân biệt “không có run mới” với “chưa lấy trang mới”. |
| H2 — run hỗ trợ trên nhánh khác | N6 | `unassigned_support_runs=41`, log liệt kê từng nhánh và các ID publish lease. Tập29 không tự chứng minh tập chi của toàn packet; không cáo buộc 41 run là chi trái phép. |
| H3 — định danh attempt khác định danh run | N1/N6 | Fixture cùng ID với attempts1,2: unique_runs1 nhưng distinct_attempts2, dispatch0. Raw thật hai ID attempt2 nhưng không có history/jobs. Đếm ID hoặc dispatch không quyết được số lần thực thi loại(b). |
| H4 — biên50%, vòng không xác định, nhân thể hiện | N2/N4 | low–undefined–low=true; low–50%–low=false; 50%–50%=false; 0–0=true; toàn undefined=false. Tăng100 thể hiện vẫn tỉ lệ lớp1/3. Adapter có đủ witness miền xác định, ngưỡng nghiêm ngặt và slug duy nhất. Không thấy lỗi trên các chuỗi đã đo. |
| H5 — nguồn hai đường tooling trong endpoint | N3 | Diff từng tooling `d706abd..6e73403` rc0 rỗng; log master ghi commit nguồn. Không phải sửa sản phẩm của packet, không mất khỏi bảng đo. Đây là audit nguồn nhập qua merge, không lặp phép thử lọc đường trước predicate. |
| H6 — phối hợp ba điều kiện sau quyết merge | N2/N4 | Head đổi: new_review=false, ci_required=true, complete=false khi chưa CI; có lỗi: new_review=true dù CI có; có CI và không lỗi: complete=true. `clauses_in_adapter=true`; mutant kết thúc trước CI bị bác. Không thấy ba mệnh đề tự triệt tiêu. |

H4/H6 là mô hình hành vi được reviewer dẫn xuất từ văn bản và đối chiếu witness trong adapter, không phải chạy agent qua một vòng merge thật. Kết quả sạch có phạm vi đúng bằng các chuỗi đã kê.

## BẢNG ĐO

| Cái đo | Cái KHỚP | Cái LỆCH / giới hạn | Lệnh + output |
|---|---|---|---|
| Identity | SHA đúng; tree `76df7775d461d3f2dddcaa6cdca3d608f59453a8`; cây sạch | Không xác minh authority ngoài sandbox | `python review-artifacts/preflight.py`: head/tree rc0, status rỗng |
| Gói spec | SHA256 `e69d6a996306483a930bb3de7e9d267135535f43d8e7bea95375f51c879e0f75`,38107B | Không coi lease đã cấp là tự động chứng thực nội dung | cùng lệnh; [log](review-artifacts/preflight.json) |
| Mirror | 408 refs; shallow=false; abbrev7 | Không có remote fetch trong lượt này | cùng lệnh, rc0 |
| Product delta | 2 tệp,201 dòng thêm; giữ toàn byte nền ngoài insert | Endpoint còn2 tooling nhập master và13 review | obligations + hunts H5 |
| M16 | Gói chỉ dữ kiện/spec/lease/diff/ledger, không có probes; lời phán N cũ được dẫn lịch sử | Không dùng rc của executor làm phép nghiệm thu reviewer; không thấy S11' bị vi phạm ở lần nộp này | `closure.py` danh sách tệp + đọc EVIDENCE; các cổng dưới do reviewer chạy lại |
| M17 | 11 đơn vị có tên/nhóm tên qua cú pháp; baseline không vi phạm | Cú pháp có lỗ và bắt oan; chi tiết trên | `m17.py` |
| Doctrine | Đối chứng §12 đỏ6, baseline xanh0 | Hai mutant canonical sống0 | `canonical.py` |
| Sáu cổng cục bộ | doctrine0, adr0, doc_claims0, release0, receipt0, worktree_diff_check0 | Không thay review ngữ nghĩa hay chứng cứ CI | `python review-artifacts/gates.py`; [argv/output](review-artifacts/gates.json) |
| Bằng chứng dương cổng | ADR48/48; release `ok=true`, expected=checked=180; receipt120 ĐẠT v2,0 vi phạm | Schema xanh không xác thực N6 | `gate-adr.json`, `gate-release.json`, `gate-receipt.json` |
| Diff whitespace | Working-tree `git diff --check` rc0 | Endpoint base..head rc2:2 trailing spaces trong verdict lượt1 bất biến; khác phạm vi lệnh, không quy lỗi cho lời khai working-tree rc0 | preflight và gates; không mở lớp P3 cho hiện vật cũ |
| CI raw | 253 unique;132/66/55;29 gắn packet;2 attempt2 | Độ đầy đủ/phân loại chi chưa biết; receipt5 thiếu,receipt6 số0 chưa chứng minh | `ledger.py`, `hunts.py` |
| Cuối lượt | SHA không đổi, cây sạch | Không chạy CI live hoặc full selftest | `closure.py` |

Các mã thoát trong bảng cổng đều là reviewer chạy thật trên head yêu cầu. Không nhập số1710/1710 của executor thành kết quả của mình.

## PHÁT HIỆN

### BẢNG LỚP

| lop_loi | Slug lớp | Hạng / thể hiện mở | Bản vá theo lớp hoặc lý do chưa thể vá trong scope |
|---|---|---|---|
| Quy phạm cũ sống qua cơ chế thay thế thiếu kiểm nội dung | `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | P2 / 3 | Chủ kho sửa đặc tả để kiểm hiệu lực theo nội dung/phạm vi nhãn; giữ lịch sử hợp lệ; chiếu cùng chốt mới sang lease. Không thêm vài cụm rồi tuyên bố đóng toàn lớp. |
| Khẳng định CI thiếu liên kết giữa receipt và tập thực thi chứng minh được | `bien-nhan-thieu-so-ci-da-chi` | P2 / 3 | Một đường bổ sung bất biến cho receipt, có mốc và nguồn thô đầy đủ; thống nhất trạng thái số chi với mức chứng minh. |
| Scanner danh sách cụm không nhận diện đủ sao chép doctrine | `phep-do-doctrine-khong-du-rang` | P2 / 2 | Cần chủ kho mở packet hoặc đổi scope; S4 cấm sửa scanner tại đây. |

### `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi`

**Ba thể hiện hiện hành, không đếm từng fixture thành finding:**

1. **Ngoại lệ cú pháp hợp thức hóa câu đang cấp nghĩa vụ** — SPEC:150–159,437–438; nhãn đầu đoạn hoặc ô ĐÃ RÚT không quyết được nghĩa của câu/ô còn lại. Hai witness label/table trong `m17.json` đều được cho qua dù cấp A18/A17 quyền hiện hành. Lỗ không tên là giới hạn bổ sung của cùng phép quét, không cộng thêm thể hiện. Cách chữa cần kiểm phần nội dung được nhãn bao phủ, không chỉ vị trí xuất hiện nhãn.
2. **M17 bác lịch sử không cấp quyền** — SPEC:171–178. Witness `valid_history=false` trong khi câu chỉ rút hiệu lực. Không đổ cho việc người viết “vi phạm M17”: nhiệm vụ review chính là kiểm M17 có chọn tập chấp nhận sai không. Chủ kho có thể chọn chuẩn trình bày bắt buộc riêng, nhưng không được coi sai chuẩn trình bày là bằng chứng luật cũ đang vận hành.
3. **Bản chiếu lease giữ S12' đời trước** — LEASE:225–228 tiếp tục nói chép r7;257–261 thiếu vế mới SPEC:423. Fixture quét khái niệm nhưng hạ một luật thành báo cáo: spec dừng, riêng lease không dừng. Không đếm mỗi từ còn “r7” là một lỗi.

Ba đoạn cũ đã sửa, nên không phán CHƯA VÁ. Có lỗi mới trong cơ chế được dùng để chữa, nên phán canonical **VÁ SINH LỖI MỚI**.

### `bien-nhan-thieu-so-ci-da-chi`

**Ba thể hiện mở:**

1. Receipt lượt5 thiếu nguyên khối ngân sách/số chi/ID và chưa có bản bổ sung trong gói/cây. `ledger.json` chứng minh không có ba trường top-level; lời thuật lại verdict cũ không thay chúng.
2. Receipt lượt6:42–50 khôi phục trường nhưng ghi `da_chi_ci_loai_b: 0`, IDs rỗng, rồi viện dẫn dispatch0 và212 records. Chính phần giới hạn sau đó và ledger bản2 không chứng minh số loại(b). Phải là trạng thái chưa đo được khi thiếu bằng chứng; không sửa byte receipt đã giao, cần bản bổ sung được nhận theo hợp đồng.
3. Ledger bản2 còn kết luận vượt tập quan sát: “trong vòng đời/chưa từng”, raw và pagination chưa đủ kiểm, đuôi tới as_of chưa được chứng thực, tập29 chưa giải trình nhánh hỗ trợ. Gộp các thiếu hụt provenance/cửa sổ/phân loại thành **một thể hiện suy luận**, không mỗi ID, workflow hoặc trường một finding. Mốc08:15 đã sửa thật và không còn tính là thể hiện mở.

Không cáo buộc executor đã chi CI trái phép. Finding là số chi/lời khẳng định chưa có bằng chứng, không phải suy đoán về hành vi bị che.

### `phep-do-doctrine-khong-du-rang`

**Hai thể hiện:** chép nguyên đoạn nêu trần từ ADR0048 và chép nguyên §5.1 đều rc0. Cùng cây scratch, cùng scanner head hiện hành, thêm §12 cho rc6. Fixture và cả stdout/stderr ở `canonical.json` cùng `copy_*-fixture.md`.

Nợ được khai đúng; scanner không đổi. Khai giới hạn không vá cơ chế. S4 giải thích vì sao không sửa trong packet này, không phải căn cứ để chấm lớp là đóng.

## KHÔNG ĐO ĐƯỢC

**Để N6 đủ bằng chứng**, cần:

1. Metadata gốc xác định mốc mở/được cấp packet; đã có lease08:15Z, còn thiếu metadata Issue nếu nó sớm hơn. Không cần phủ nhận lease đúng để giữ phần chưa biết.
2. Các request/response trang run gốc và timestamp lấy, qua một `as_of` xác định: đủ4 lần/400 records nếu tiếp tục viện dẫn chúng; đủ283 unique để tái dựng khử trùng và cửa sổ, hoặc bộ lấy mới có chứng cứ tương đương. Watermark truy vấn phải phủ đuôi, không lấy timestamp run mới nhất thay chứng cứ “đã hỏi đến đâu”. Raw thử bộ lọc cần nộp nếu tiếp tục dùng lỗi bộ lọc làm căn cứ chọn tập.
3. Quy tắc gắn packet có chứng cứ nhánh/PR/head/generation, gồm nhánh spec/lease hỗ trợ và lý do loại chúng khỏi số chi nếu thích hợp; history attempts/jobs, actor/trigger và nhật ký mục đích gọi đủ phân biệt(a)/(b)/(c). Một field `run_attempt=2` chỉ nói snapshot hiện tại, không chứng minh mỗi lần đã dùng để làm gì.
4. Sổ thực thi/audit contemporaneous đối chiếu được với lịch sử còn lại, đủ xử lý run bị xóa/mất. Nếu chỉ có history còn tồn tại, phải giữ KHÔNG ĐO ĐƯỢC cho tổng thực chi. Phút billable không phải yêu cầu của phép đếm lượt.
5. Bản bổ sung receipt5 và receipt6 có neo hash đến bản bất biến, tách budget khỏi consumption, khai IDs hoặc KHONG_DO_DUOC theo đúng dữ kiện, cùng mốc as-of. Quyền nhận bổ sung thuộc chủ kho/điều phối nếu chưa có cơ chế. Bổ sung đủ hình dạng mà số chi vẫn chưa biết chưa tự làm N6 ĐẠT.

Ngoài N6: chưa đo runtime agent, hành vi thật trước freeze, CI live, full `tl.py --selftest` trên head này hoặc tính tối thiểu tổng quát của adapter. Các hạn chế ấy không được trình bày thành pass. Các cổng tài liệu/release/receipt liên quan đã được chạy riêng; không cần tự soạn nội dung nhạy cảm để hoàn thành các thước đã dùng.

Nếu điều phối muốn kiểm đầu vào đường dẫn có khả năng thoát cây hoặc dạng tương tự, reviewer chỉ đề nghị bằng lời: dùng fixture do điều phối quản lý, chạy trong môi trường kiểm soát, trả argv/rc/output và vị trí tác động. Lượt này không tự soạn loại payload đó, không tuyên bố đã đo nó.

**Tự sửa công khai lỗi thước:** lượt chạy M17 đầu chưa nhận ngoại lệ khối S12' ở YAML, báo nhầm LEASE:257. Đã sửa parser, chạy lại, baseline cuối không vi phạm. Output đầu còn trong nhật ký tăng dần và **không dùng làm finding**. Các thăm dò tên file/ref ban đầu không tìm thấy được thay bằng đọc đúng ref mirror; không dùng lỗi lookup thành finding. `cat cay/.git` báo đây là thư mục chỉ là thăm dò bố cục, không phải lỗi sản phẩm. Cổng endpoint whitespace và cổng working-tree được ghi riêng đúng phạm vi.

## KẾT LUẬN

**blocked, không approve.** Ba đoạn vận hành cũ đã sửa thật, nhiều chốt adapter đo được và các cổng hiện hành đều xanh. Những điều đó không đủ đóng lớp đặc tả vì M17 còn sai tập chấp nhận và lease chưa nhận đủ chốt mới. CI bản2 tiến bộ thật nhưng N6 vẫn KHÔNG ĐO ĐƯỢC; doctrine vẫn còn hai phản chứng sống.

Việc tiếp theo thuộc chủ kho/executor: quyết sửa thiết kế đặc tả và bản chiếu lease, cung cấp dữ kiện CI cùng đường bổ sung receipt bất biến, quyết scope riêng cho scanner. Không đổi slug, không nới N1–N8 để vừa kết quả, không sửa hiện vật đã giao.

Biên bản đã mở trước phép đo và được bồi bằng output sau từng bộ đo: [VERDICT-incremental.md](review-artifacts/VERDICT-incremental.md). Các scripts, fixture và JSON là hiện vật reviewer; `cay/` vẫn sạch và SHA không đổi.
