---
verdict: blocked
reviewed_sha: abb79dfae7634da99a07a0c30095769973ed04d4
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

Reviewer độc lập: OpenAI / Codex, shell qua API, transport machine, trong sandbox được giao. Không dùng context executor, không suy model/effort thực thi từ receipt cũ hoặc danh tính người vận chuyển. Không mạng, push hay sửa cây executor. Verdict chỉ áp exact SHA trên, tree `ddfdc8180231a5633f2936400f28f38fff21c72e`.

Đã tạo VERDICT trước phép đo đầu tiên và bồi sau các phép đo. [Nhật ký tăng dần](review-artifacts/VERDICT-incremental.md) giữ cả output trước sửa thước. Lệnh trong các bảng chạy từ gốc sandbox, trừ sáu cổng chạy tại `cay/`. Script báo cáo thoát 0 chỉ nghĩa là xuất xong kết quả; phải đọc boolean và mã thoát tiến trình con.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Slug canonical | Phán duy nhất | Lệnh + output thật |
|---|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | **VÁ HỜ** | `python3 -B review-artifacts/measure.py semantic`: `appendix_heading_present=false`, không thấy sáu tiêu chí r5 được cấp lại; nhưng LEASE:130 vẫn “Luật chung nay là M17 của r8”, `accepted=false`. Đã đọc toàn 446 dòng spec/273 dòng lease. |
| `bien-nhan-thieu-so-ci-da-chi` | **VÁ HỜ** | `measure.py ledger`: `submitted_range_matches=true`, nhưng `stale_proven_claim` vẫn nói tập 253 phủ từ 06:16:03; hai khóa cùng hậu tố `trong_cua_so` dùng tập 283 và tập 253. `measure.py receipts`: lượt5 cả ba khóa `MISSING`, `supplement_named_candidates=[]`; lượt7/8 `0 / KHONG_DO_DUOC / []`. Ba thể hiện cũ đều chấm riêng bên dưới. |
| `phep-do-doctrine-khong-du-rang` | **CHƯA VÁ** | `python3 -B review-artifacts/measure.py doctrine`: gốc `rc=0`, thêm đoạn trần ADR0048 `rc=0`, thêm toàn §5.1 `rc=0`, đối chứng §12 `rc=6`; `unchanged_since_review8=true`. |
| `chu-giai-lease-neo-head-cu` | **ĐÃ VÁ THẬT** | `measure.py semantic`: hai neo máy đều `abb79dfae7634da99a07a0c30095769973ed04d4`, `current_head_prose_matches=true`. Câu hiện hành dùng abb79df; 00ac525 chỉ còn trong đoạn kể lỗi gen8. Không đếm lớp này vào số mở. |

Không nhận lời khai “đã sửa” thay phép đọc. Lớp thứ nhất đã bỏ lỗi bắt oan theo vùng và sửa con trỏ ở spec, nhưng còn đúng đường vận hành lease mà lượt8 đã chỉ ra; vì vậy là VÁ HỜ, không phải một cơ chế mới sinh thêm lỗi.

## NGHĨA VỤ N1–N8

| Nghĩa vụ | Thước độc lập và lệnh đã chạy | Output / phán |
|---|---|---|
| N1 | `python3 -B review-artifacts/measure.py oracles`: đọc bảng đúng mục; mỗi mutant có vector kỳ vọng đầy đủ, tập khóa chính xác, boolean đúng kiểu. | Bản gốc 7/7 quan sát true; 7 mutant có vector đúng kỳ vọng. `target_green=false`, `all_red=false`, `missing_non_target=false`, oracle đúng `true` về tín dụng. **ĐẠT** trong miền đã đo. |
| N2 | `measure.py audit`, `measure.py delta`; đọc từng câu/ô phần thêm, lưu nguyên văn ở [N2-units.json](review-artifacts/N2-units.json). Đưa cùng câu yêu cầu màu nền vào vị trí riêng/kề bảng, thêm ca chỉ chứa nhãn M8. | 201 dòng thêm, 149 dòng không trống; `unassigned_units=[]`. Ba ca ngoài nhóm đều `accepted=false`. Đảo hành động M8 vẫn đúng nhóm nhưng `content_correct=false`, giới hạn được khai. **ĐẠT**. |
| N3 | `python3 -B review-artifacts/measure.py delta`: liệt kê toàn endpoint base→head trước phân loại, kiểm cả đường không nằm trong patch nộp. | 21 đường; hai sản phẩm +62/+139, tổng201; `numstat_matches=true`, `cross_base_preserved_in_order=true`. Hai tooling ngoài write set bằng blob master d706abd, không đổi sau merge00ac525. **ĐẠT**. |
| N4 | `measure.py oracles`: đối chứng dương và từng đối chứng âm nằm trong cùng hàm kết luận với vector mutant. | `conclusion=true`, `broken_positive=false`, `broken_negative=false`. Đối chứng có khả năng đổi kết luận, không chỉ in log. **ĐẠT**. |
| N5 | `python3 -B review-artifacts/measure.py pointers`: trích đúng thân §3.2/5/8/12/13/20, đọc khái niệm con trỏ hứa. | Mọi witness cuối cùng true; con trỏ giả sang §12 cho schema review_class `false`; nợ severity có mặt. **ĐẠT** cho con trỏ adapter được thêm. |
| N6 | `measure.py ledger`; `measure.py receipts`; đọc JSON và đối chiếu hồ sơ Git, không lấy bảng kết quả executor làm oracle. | Đo được tập253/29 và lỗi lời khai; không đo được tổng CI loại(b)/run IDs trọn vòng đời. **KHÔNG ĐO ĐƯỢC**, không suy thành số0. |
| N7 | `python3 -B review-artifacts/measure.py n7n8` cùng thước N1–N6. | Sáu hợp đồng đo được dựng từ văn bản; `missing_text_prevents_measurement=[]`. **ĐẠT**: N6 thiếu dữ kiện, không thiếu mô tả để dựng thước. |
| N8 | `measure.py n7n8`; kiểm cả quy tắc và verdict này. | `all_pass_explicit=true`; N6 unknown, không đọc nghĩa, thiếu bảng săn, không approve tường minh đều trả `false`. **ĐẠT** vì đã thi hành chặn approve. |

Bảy đột biến N1: đổi ô sensitive; gộp routine/systemic; thay bảng dừng bằng con trỏ; bỏ cột phương án; bỏ bảng đơn vị; bỏ mỗi finding đúng một lớp; thay mục BẢNG LỚP bằng con trỏ. Các quan sát có thể đồng thời đỏ ở nhiều tiêu chí liên quan; tập đỏ kỳ vọng được khai trước, không giả “chỉ một boolean đỏ”. [Vector đầy đủ](review-artifacts/N1-N4.json) và `mut-*.md` là thước/hiện vật của reviewer.

N2 là phép đọc nghĩa trên tập hữu hạn: bản kê dòng ghi lại kết quả đọc, **không** dùng vị trí hay từ khóa làm giấy phép cho câu. Phần cross-review thuộc A1′/A2′/M8; work-packet thuộc M3–M10 và các giới hạn liên quan. Đã đối chiếu nghĩa vụ gốc từ blob r1/r2/r3/r4; phần severity của A2′ đọc theo việc r10 rút con trỏ sai. ĐẠT không chứng minh một oracle ngôn ngữ tổng quát, hay “dạng ngắn nhất” duy nhất.

Không thấy executor nộp probe nghiệm thu hay tự phán ĐẠT N1–N6 trong gói hiện hành. Các rc có sẵn được M16 cho phép; receipt thuật lại phán quyết reviewer cũ không phải executor tự cấp ĐẠT. Không dựng finding S11′ từ những hiện vật ấy.

## M17-GO VÀ LEDGER BẢN 4

**Gỡ M17/M17′ là đúng đối với hai thiết kế đã bị bác. Không cần M17″.** Cổng vị trí tên có thể báo một câu vận hành chứa tên cũ, nhưng cũng bắt câu lịch sử hợp lệ và không nhìn được khái niệm ngoài tập tên. Giữ nó làm chứng nhận “không còn luật cũ” không giải quyết nguyên nhân.

**Kết luận “phép đọc KHÔNG tự động hoá được, và đó là kết luận đo được” ở SPEC:183–184 quá rộng.** Ba ca và hai cổng hỏng không chứng minh bất khả tự động hóa. Chúng hỗ trợ quyết định bỏ hai cổng cụ thể, không chứng minh mọi phương pháp tự động đều bất khả, cũng không chứng minh reviewer có độ nhớ/độ phủ hoàn hảo. EVIDENCE đã tự khai giới hạn thống kê nhưng không làm câu tuyệt đối trong SPEC thành đúng. Nên phát biểu hẹp theo chứng cứ ấy.

Gỡ cổng có mất một **cảnh báo cú pháp tất định, dễ chạy lại**. Có ca cổng cũ bắt được: câu vận hành có tên cũ đặt ngoài vùng cho phép. Reviewer có thể bỏ sót câu đó nếu đọc thiếu; không có dữ kiện chứng minh xác suất bỏ sót bằng0. Ngược lại, đọc nghĩa đầy đủ sẽ bác câu ấy và không bắt oan lịch sử. Tìm kiếm vẫn có ích để hỗ trợ đọc, nhưng số0 của nó không mua được nghiệm thu.

Bắt buộc đọc một việc chưa có bộ đo tự động đáng tin **không tự mâu thuẫn**: thao tác đọc vẫn làm được, có người chịu trách nhiệm và có hậu quả không-approve khi bỏ. Đây là thiết kế phân công, không phải lời từ bỏ. Lỗ hiện tại là thu hồi chưa sạch, không phải nghĩa vụ đọc tự nó vô nghĩa.

**Đã thực sự đọc toàn thân spec và lease.** [Biên bản từng phần](review-artifacts/concept-read.md) tách lịch sử, nợ, quy phạm hiện hành và câu có vấn đề. Không thấy công thức cộng hai khoảng hoặc sáu tiêu chí r5 được cấp lại. Nhưng **LEASE:130 vẫn cấp M17 đã rút làm “Luật chung nay”**. `measure.py closure_controls` giữ bản sao chuyển câu ấy sang lịch sử rút hiệu lực: phán đọc nghĩa đổi reject→accept; không bắt tên M17 tự nó.

S12′ vẫn có câu “dựng lại phép quét”. Có cách đọc nhất quán là chặn khi executor chọn dùng một phép quét nội bộ yếu, không buộc phải có cổng. Vì vậy tôi không tự đếm nó thành lỗi khôi phục cổng chắc chắn. Tuy nhiên chủ kho nên nói rõ phạm vi điều kiện và cách sửa sau GO, tránh để người đọc phải tự hòa giải với việc gỡ cổng. Chuyện này được ghi cùng lớp canonical, không tách để tăng số.

**Ledger bản4 chưa đủ đóng N6 và chưa thu hồi hết lời khai sai.**

| Thể hiện / sửa đổi | Phép đo và kết quả |
|---|---|
| Cửa sổ được nộp mới | Min `08:15:01Z`, max `21:42:48Z`; khớp `cua_so_BAN_GHI_DUOC_NOP_utc`. MD đã giới hạn đúng. Đây là sửa thật. |
| Cửa sổ đã fetch | Khai rõ tập283 không nộp và không kiểm được từ tệp. Tách trường là đúng, nhưng đây chỉ là lời khai provenance. |
| Lời chứng minh cũ | JSON `pham_vi_khang_dinh.chung_minh_duoc[0]` vẫn: “Trong TAP 253… cua so 06:16:03Z… phu tu truoc moc lease”. Mệnh đề này vẫn sai đối với tập nộp. Đối chứng thay bằng min/max tập nộp đổi kiểm false→true. Thể hiện cửa sổ **VÁ HỜ**. |
| Khóa kết quả còn hai nghĩa | `run_TOAN_KHO_trong_cua_so=283`, còn tổng `workflow_CO_chay_TOAN_KHO_trong_cua_so=253`. Cùng tên phạm vi nhưng khác tập; các khóa `trong_vong_doi` vẫn còn. Thể hiện cấu trúc **CHƯA VÁ**. |
| Receipt lượt5 | Ba khóa ngân sách/thực chi/IDs đều thiếu; không tìm thấy bổ sung theo danh mục, không có đính chính cho lượt5 trong receipt kế tiếp đã đọc. EVIDENCE cũng khai chưa có. Thể hiện **CHƯA VÁ**. |
| Receipt lượt7/8 | Budget0 tách khỏi `KHONG_DO_DUOC`; lượt8 có đính chính lời khai0 của lượt6. Công nhận sửa thật, không biến receipt4/6 số0 thành đã được chứng minh. |

Min bản ghi **không phải** cận truy vấn lịch sử. Chênh một giây không chứng minh có hay không có CI ở giây thiếu. Tương tự, `as_of=2026-09-13T02:09:50Z` không kéo dài tập kết thúc tối12 đến thời điểm đó. Không cáo buộc executor chi CI trái phép.

Để đóng N6 cần: dữ liệu lịch sử đủ phạm vi từ mốc mở packet có thẩm quyền đến mốc chốt nghiệm thu; trang/raw response và thời điểm lấy đủ tái dựng truy vấn, lọc, phân trang; căn cứ phân loại từng lượt/attempt theo tự động, đo thủ công và thăm dò; các run_id/attempt tương ứng; và nguồn có khả năng giải quyết khoảng trống do run bị xóa. Nếu thiếu nguồn ấy thì tiếp tục ghi chưa đo được. Cần hiện vật bổ sung được chủ kho chấp nhận cho receipt5, neo receipt cũ; không sửa hiện vật bất biến. **Không thiếu số phút**: phút không phải đơn vị nghiệm thu N6.

## BẢNG SĂN

Sáu hướng bổ sung dưới đây không tính bảy mutant N1, phép canonical M17/ledger/receipt5/scanner hay kiểm neo chú giải lease. Chúng xét sáu quan hệ khác nhau, không lấy sáu biến thể của một regex làm sáu hướng. Lệnh: **`python3 -B review-artifacts/measure.py hunts`**; [output cuối](review-artifacts/hunts-final.out), kết quả từng H ở JSON cùng tên.

| Hướng | Đối tượng và phép thử | Output thật / phán |
|---|---|---|
| H1 — tính đúng của báo cáo lượt review | So ba khối receipt8 với verdict8, số runtime hiện hành và receipt6. Không đo khối CI của N6. | `hunt_ids_equal_receipt6=true`; receipt khai không lớp mới trong săn nhưng verdict có P3; anchor847,52s/538266B khác khối runtime807,77s/544140B; nhãn canonical lặp bị lệch. **Một lớp P3 mới**, ba thể hiện. |
| H2 — topology xuất bản hợp đồng | Tìm blob spec trên ref xuất bản, lease trên commit thêm tệp; so byte/băm với gói, rồi kiểm nó có ở product head không. | spec/lease `bytes_equal=true`, `spec_hash_matches_lease=true`, spec trong reviewed tree `false`. **SẠCH**: hợp đồng cấp riêng được gói chỉ định tường minh; không buộc nó nằm trong write set sản phẩm. |
| H3 — quyền chọn cách triển khai | Đọc câu ba điều kiện cho phương án khác; mutant bỏ tái dẫn xuất/tự đo để xem câu lịch sử có che thiếu nghĩa vụ không. | Bản gốc `true`, `blind_copy_mutation=false` sau sửa thước. **SẠCH** trong hợp đồng chữ: cách khác có đủ ba điều kiện được phép, vá lẻ vô cớ vòng3 bị cấm. |
| H4 — truy vết khi chuyển lớp sang nợ | Kiểm M6 còn đủ ba chiều lớp/phạm vi bị cắt/nợ tên; mutant chỉ khai tổng để thử mất liên kết. | `original=true`, `aggregate_only_mutation=false`. **SẠCH**: biết chính xác cái gì rời phạm vi; tổng sạch không cấp tín dụng vá thật. |
| H5 — ngoại lệ phát hiện lỗi sau quyết định merge | Đọc đủ ba mệnh đề M9; mutant bỏ ngoại lệ lỗi, giữ hai vế kia. | Gốc `[true,true,true,true]`; mutant `[true,true,false,true]`. **SẠCH**: đổi head đơn thuần không mở review mới, nhưng phát hiện lỗi mở vòng mới và khai lý do; CI hậu merge còn bắt buộc. |
| H6 — hạng của lớp có bị pha loãng | Đọc luật lấy hạng cao nhất; thử P2+P3 và P2+20P3; đổi “cao nhất” thành “thấp nhất”. | Cả hai nhóm trả `P2`; `lowest_mutation_rejected=true`. **SẠCH**: tăng thể hiện nhẹ không làm nhẹ lớp; slug giữ qua lượt. |

H3–H6 là phản chứng hợp đồng văn bản và mô hình hữu hạn reviewer dựng, **không** phải tuyên bố sản phẩm có cổng runtime cưỡng chế các quy tắc ấy. H2 không đo quyền cấp lease live; chỉ đo topology/băm trong mirror.

## BẢNG ĐO

| Khẳng định / đối tượng | Lệnh hoặc artifact output thật | Khớp? |
|---|---|---|
| SPEC băm/kích thước | `sha256sum goi/SPEC.md`, `wc -c`: `8bfa0a9e67c9fbef49227fa9688c842b3e9676ef82b5e2befb202634148a93cb`, 38191B | **KHỚP** |
| Cây và mirror | `inspect.py`: HEAD đúng; 410refs; shallow=false; core.abbrev7; tree như đầu verdict | **KHỚP** |
| Gói diff và numstat | `measure.py finalcheck`: diff không bằng toàn Git diff; [packet-diff-scope.json](review-artifacts/packet-diff-scope.json): patch bằng diff hai skill+reviews. Numstat toàn21 đường khớp. | **Có lọc patch**; N3 đã đo phần bỏ ngoài bằng Git, không kết luận vượt scope |
| Delta sản phẩm | `measure.py delta`: 2 tệp/+201/không xóa; hai tooling là blob master | **KHỚP**, dưới trần300 |
| Phụ lục A, cổng vùng tên | `measure.py semantic`: heading vắng, quy phạm M17′ đã gỡ | **Sửa thật** |
| Thu hồi hết M17 | LEASE:130 còn “Luật chung nay…” | **LỆCH** |
| Neo head trong chú giải | `current_head_prose_matches=true` | **Sửa thật** |
| Ledger số đếm hẹp | 253 ID duy nhất;29packet; push132/PR-target66/PR55;0dispatch;0windows packet;2ID attempt≠1 | **KHỚP** |
| Ledger câu chứng minh/các khóa kết quả | Câu cũ còn trong JSON;283 so tổng253 | **LỆCH** |
| Receipt8 schema so nội dung | Cổng122 ĐẠT nhưng ba khối dữ liệu lượt cũ còn trong receipt8 | **Schema-pass không bảo đảm nội dung** |
| `doctrine-scan --root .` | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`: rc0,7tệp,0cụm | **KHỚP rc executor**, chưa chứng minh sạch nghĩa |
| `adr-song --root .` | Cùng script: rc0,48ADR/48dòng§20 | **KHỚP** |
| `bien_nhan_v2` | `python3 -B ops/bien_nhan_v2.py --root .`: rc0,122ĐẠT,11/11miễn,42nợ,0vi phạm | **KHỚP**, không phải N6-pass |
| `doc-claims-check --strict` | `python3 -B scripts/tl.py doc-claims-check --strict --json`: rc0,ok=true,108tệp,flags=[],376advisory | **KHỚP** |
| `release-verify --strict` | `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: rc0,ok=true,180expected=180checked,hash_match=true | **KHỚP** |
| `git diff --check` | Trong cay: rc0 | **KHỚP đúng đầu vào worktree**, không khai đây là endpoint diff-check |
| Cây executor cuối lượt | `measure.py finalcheck`: status rc0,stdout rỗng | **Giữ sạch** |

[Sáu lệnh và output cổng](review-artifacts/gates.json) ghi cả mã thoát cuối của hai tiến trình chạy lâu. Output dài docclaims/release được công cụ cắt; các trường kết luận nêu trên hiện rõ, không nhận phần không thấy làm bằng chứng bổ sung. Không chạy full selftest hay CI live; con số1710 của executor không trở thành kết quả của reviewer.

## PHÁT HIỆN

### BẢNG LỚP

| `lop_loi` / slug | Hạng | Thể hiện mở | Bản vá theo lớp / lý do vá lẻ |
|---|---|---:|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | P2 | 1 | Thu hồi mọi câu đang trao hiệu lực hiện tại cho cơ chế đã gỡ; duy trì đọc nghĩa reviewer. |
| `bien-nhan-thieu-so-ci-da-chi` | P2 | 3 | Tách nhất quán tập quan sát/provenance/kết luận; cung cấp dữ kiện N6 và bổ sung receipt theo thẩm quyền. |
| `phep-do-doctrine-khong-du-rang` | P2 | 2 | Chủ kho quyết packet/scope riêng vì S4; không lấy khai nợ làm sửa cơ chế. |
| `bien-nhan-luot-8-lan-du-lieu-luot-6` | P3 | 3 | Đính chính đồng bộ các khối dẫn xuất của receipt8 từ đúng verdict8/run8; bảo toàn receipt cũ. |

Hạng giữ cách dùng của kho; không tự định nghĩa doctrine severity. Ba đoạn cùng gốc không thành ba lớp. Lớp P3 neo lease cũ đã đóng không nằm bảng mở.

### `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi`

**LEASE:130**, cuối `base_sha_ghi_chu`, còn dùng M17/r8 làm luật chung hiện tại. Đây không phải chỉ nhắc tên trong lịch sử: chữ “nay” trao vai trò vận hành, trái việc r10 gỡ cơ chế. Phần đầu khối nói N3 đúng không vô hiệu hóa câu cuối.

Vá ở các câu vận hành của spec/lease theo nghĩa vụ hiện hành, không thêm cổng tên lần ba. Ca khóa: người đọc độc lập bác câu cấp lại cơ chế cũ nhưng chấp nhận câu chỉ kể lịch sử đã rút; đã chạy đối chứng đọc trên bản sao. Rủi ro bản sửa là xóa cả lịch sử hữu ích hoặc để S12′ lại đòi dựng cổng đã gỡ; rà cả hai. Không tự sửa hợp đồng trong lượt review này.

### `bien-nhan-thieu-so-ci-da-chi`

Ba thể hiện: **receipt5 thiếu và chưa bổ sung**; **câu chứng minh cửa sổ vẫn sai trong JSON**; **các khóa kết quả cùng tên phạm vi nhưng dùng hai tập và còn mang nghĩa vòng đời**. Không đếm MD/JSON của cùng một câu hai lần. Đổi hai trường cửa sổ chưa sửa các consumer/lời khai còn lại.

Vá tại ledger và hiện vật bổ sung receipt, giữ số quan sát tách khỏi tổng thực chi chưa biết. Ca khóa: tính lại từng aggregate từ collection được chỉ tên; mỗi câu “chứng minh được” phải đúng trên collection ấy; receipt5 bổ sung có neo và phân biệt ngân sách/thực chi/IDs. Rủi ro: đổi tên khóa mà vẫn giữ câu cũ, hoặc dùng danh sách rỗng làm số0 khi chưa đủ dữ kiện. Số CI và bằng chứng còn thiếu đã nêu chính xác ở mục ledger; không dùng số phút làm rào cản mới.

### `phep-do-doctrine-khong-du-rang`

Hai loại sao chép còn lọt: đoạn trần ADR0048 và nguyên §5.1. Bản gốc và hai bản thêm đều rc0; thêm §12 rc6 cho đối chứng có răng. Scanner không đổi giữa a4451dd và abb79df. Đây là lớp cũ còn sống, không phải regression r10.

Vá cần chủ kho mở packet hoặc đổi scope; S4 cấm reviewer/executor sửa scanner trong packet này. Ca khóa là hai fixture đã lưu, cùng bản gốc và đối chứng dương. Rủi ro: mở rộng danh sách từ lại bắt oan lịch sử hoặc tiếp tục bỏ sót cách diễn đạt khác. Không yêu cầu dựng một máy hiểu nghĩa tổng quát để báo lớp này chưa đóng.

### `bien-nhan-luot-8-lan-du-lieu-luot-6`

Receipt8 là hiện vật mới trong delta được review. **Ba thể hiện cùng gốc dữ liệu lượt cũ còn sống trong bản mới:**

1. `doi_chieu_luot_truoc` ở dòng168–172 ghi lớp đặc tả **VÁ HỜ**, trong khi `findings_ids` và verdict8 ghi **VÁ SINH LỖI MỚI**. Hai nơi đưa ra hai nhãn cho cùng lớp/cùng lượt.
2. `bang_san` dòng225–238 chép nguyên sáu hướng lượt6 (`hunt_ids_equal_receipt6=true`), kể cả `khong_lop_moi_tu_sau_huong=true`; verdict8 thực có P3 mới từ bảng săn và sáu hướng khác.
3. `anchor.mo_ta` dòng259–262 gắn run8 nhưng ghi **847,52s/538266B**; khối `model_reviewer_identity` dòng205/210 cùng receipt khai **807,77s/544140B**. Đây là mâu thuẫn nội bộ đo được, không cần xác nhận runtime live để chỉ ra.

Không cáo buộc verdict gốc bị thay, model bị giả hoặc assurance đã được nâng sai: khối chính vẫn blocked và băm neo không phải vấn đề đang nêu. Hạng P3 cho lỗi độ tin cậy của metadata dẫn xuất. Khác lớp N6: đây là phán quyết, phạm vi săn và provenance review, không phải số chi CI; khác lớp neo lease đã đóng: đối tượng là receipt của lượt đã giao.

Vá bằng một đính chính có thẩm quyền, neo receipt8 bất biến, dựng các khối từ đúng nguồn lượt8. Ca khóa: nhãn canonical duy nhất khớp verdict; sáu hướng khớp bảng săn của đúng verdict; số runtime nhất quán giữa các khối, thiếu raw thì khai chưa xác thực. Rủi ro: sửa trực tiếp receipt cũ phá băm, hoặc chép template lượt mới rồi tiếp tục để trường trùng lệch nhau. Không đưa patch sửa hiện vật bất biến.

## KHÔNG ĐO ĐƯỢC

- N6: tổng lượt loại(b) và run IDs trọn vòng đời. Lịch sử nộp chưa đủ phạm vi/provenance/phân loại; không biến event dispatch0 thành loại(b)0.
- Quyền cấp lease, head GitHub live, metadata Issue mở chính xác, các run đã xóa và raw runtime review cũ không xác thực được offline. Gói hiện hành là thẩm quyền công việc được người dùng giao; không tra #521 theo chỉ thị cấm.
- Tính đầy đủ tuyệt đối của đọc nghĩa, khả năng tự động hóa tổng quát, và hành vi runtime của mọi agent không được các fixture hữu hạn chứng minh.
- Không tự soạn payload đường dẫn thoát cây hoặc dạng tương tự. Nếu điều phối muốn mở rộng: đo công cụ xử lý biểu diễn đường dẫn đặc biệt/thoát cây và việc chuẩn hóa về gốc trước phân loại; điều phối tự cung cấp/chạy payload. Hướng đó chưa chạy, không tính vào bảng săn.

**Tự khai lỗi thước:** N5 ban đầu tìm token `write_set` thay vì câu “Write set” ở §5; H2 ban đầu giả định lease nằm cùng ref với spec nên StopIteration; H3 ban đầu tìm toàn đoạn khiến từ trong câu phủ định/lịch sử che mutant. Đã giữ output sai, sửa nguồn/phạm vi đọc rồi chạy lại. Không dùng các output ấy làm finding. Lệnh đọc gộp quá dài bị cắt đã được bổ sung đọc riêng; không tự nhận đã thấy phần bị cắt.

## KẾT LUẬN

**blocked, không approve.** N1–N5 và N7/N8 ĐẠT trong miền phép đo đã khai; N6 KHÔNG ĐO ĐƯỢC tự chặn approve. Ba lớp P2 còn mở; lớp P3 neo lease đã vá thật, nhưng có một lớp P3 mới trong receipt8. Tổng **4 lớp mở / 9 thể hiện**.

Gỡ cổng tên là hướng đúng; chưa phải đóng lớp khi lease vẫn trao hiệu lực cho cơ chế đã gỡ. Tách cửa sổ ledger là sửa thật ở đúng hai trường mới, chưa sửa hết câu và aggregate cũ. Chủ kho cần quyết phần hợp đồng/nguồn CI/bổ sung receipt và scope scanner; reviewer không nới nghĩa vụ để đổi verdict thành xanh.
