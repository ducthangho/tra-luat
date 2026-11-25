verdict: approve
reviewed_sha: e215940d15286add6fe30947cfccda09a09d82c0
spec_sha256: 98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: 0, so_bieu_hien_mo: 0, P0: 0, P1: 0, P2: 0, P3: 0, so_lop_no_ke_nhiem: 5}
hoi_tu: {U: 1, F: 0, ty_le: "0/1 = 0%", lop_moi: 0, lop_tai_mo: 0, lop_lan_thu_tam: [kiem-chuoi-khong-doc-cau-truc, duong-dan-chua-khep-trong-goc, moc-chuyen-tiep-mau-thuan, tieu-chi-dong-xoa-khong-do-hanh-vi, schema-bo-sot-provider-hop-le, tien-kiem-lease-chua-du]}

Approve **đặc tả r8 trong phạm vi đã được chủ kho quyết định tách**. Không còn finding P0–P3 thuộc bảng (i). Lớp `tien-kiem-lease-chua-du` **CHƯA VÁ**, chuyển sang bảng (ii) của #1484; không tính vào F. Verdict này không cấp lease, không duyệt mã giao nộp, không miễn gate/audit/Windows và không cấp quyền merge. Phép đo hiện tại vẫn thấy lease B4 giữ hai tệp Python, nên wp1466 chưa đủ điều kiện bắt đầu.

Đã kiểm sha256 **đầu tiên**: khớp chỉ thị; tệp trên đĩa bằng blob tại reviewed SHA; tree `ad1e8b3d341a02b500631c44ec549290f171d978`. Băm verdict lượt 7 khớp `082db6d7c1cb824336268bff5c274990bea83bb783eefa2986a38df7ac8c8d54`. Mọi bản sao, script và log mới nằm dưới `out/`; không sửa kho nguồn, không push và không gọi API GitHub. Các liên kết hiện vật dưới đây tính từ thư mục chứa verdict.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

Đối chiếu các nhóm còn mở ở cả hai bảng của lượt 7 trước khi săn biểu hiện mới. Bốn nhãn §8 là **ĐÃ VÁ THẬT · VÁ HỜ · VÁ SINH LỖI MỚI · CHƯA VÁ**; không bắt buộc phải sử dụng cả bốn khi bằng chứng không phù hợp. Lượt này dùng CHƯA VÁ cho phần chuyển phạm vi, kể cả khi cách trình bày r8 đã sửa đúng. F11.f và F11.h là quan hệ nhóm/biểu hiện, không đếm thành hai lỗi độc lập.

| finding lượt 7 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
| F11.f — nguồn dependency chưa đóng hết | tien-kiem-lease-chua-du | CHƯA VÁ | Khối `tien-kiem` không còn; không còn bảng V/P. Mục 1 G5, mục 0/14/19 nhận phần còn lại vào #1484. `ops/lease_publish.py` không đổi; không có chốt import mới. [audit-text.log](audit-text.log), [r7-r8.diff](r7-r8.diff). |
| F11.g — danh tính lease được miễn sau đăng | tien-kiem-lease-chua-du | CHƯA VÁ | Đã bỏ cơ chế `--sau-dang` của khối cũ. 3e mới đòi output một ID và ref/tệp vừa đăng, nhưng G9 khai rõ không có liên kết máy tới packet/revision/spec hash. Ca bình thường đạt 3e; ca hai người giữ không đạt. Đây là thu hẹp hợp đồng, không phải vá xác thực danh tính. [hunt-steps.log](hunt-steps.log), H3/H7. |
| F11.h — import trong tiến trình cha trước isolated boundary | tien-kiem-lease-chua-du | CHƯA VÁ | Không còn lời hứa tự re-exec an toàn; G5 nói rõ đường nạp của công cụ hiện hữu. F11.h được nêu ở lịch sử và giao #1484. Không dựng module độc hại hay chạy lại phản chứng import vì r8 không còn nhận nghĩa vụ này. |
| F11.i — scanner bỏ tên Git bị quote | tien-kiem-lease-chua-du | CHƯA VÁ | Đọc lại `_quet_lease_toan_kho`: `ls-tree` không `-z`, kiểm hậu tố tại dòng 749/757; G6 khai đúng. Dùng tên Unicode **có sẵn** trong kho: output thường không khớp path/hậu tố; output NUL khớp cả hai. [hunt-steps.log](hunt-steps.log), H8. |
| F05.b — khai báo ca theo cấu trúc | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | 12 khối giữ lại và patch đều bằng byte r7; không thêm consumer ngữ nghĩa ca ↔ ô INV. Mục 0:21, ADR:255/314–315 và mục 14 giao #1469. |
| F05.c — nợ phải thuộc mục Nợ | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Parser reviewer đếm 25 tên được trỏ, đều có trong 27 mục Nợ; đây là kiểm tĩnh hiện trạng. Cổng mới không mở ADR để kiểm quan hệ này trong các lần thay đổi về sau. Nợ vẫn ở #1469. [check-prototype.log](check-prototype.log). |
| F06 — containment reader cổng/ca/ADR | duong-dan-chua-khep-trong-goc | CHƯA VÁ | Patch nguyên byte, chỉ có reader protocol; không thêm ba reader kế nhiệm. Mục 0:21 và mục 19 loại hợp đồng ấy; #1469 nhận nợ. G1 ở mục 8.3 vẫn chỉ bảo vệ nguồn protocol. |
| F07 — vị từ/nghiệm thu cutover | moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Mục 0:22, ADR:256 và mục 14 không đặt vị từ cutover của #1470 trong wp1466. Không có tiêu chí N1–N16 hay mã mới nhận lại phần đó. |
| F10 — schema identity v2 và consumer | schema-bo-sot-provider-hop-le | CHƯA VÁ | Không có schema/consumer v2 trong patch; mục 0:22 và mục 14 tiếp tục giao #1470. Việc khai identity của chính lượt review không phải triển khai schema ấy. |

### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
|---|---|---|---|
| tien-kiem-lease-chua-du | CHƯA VÁ | F11.f/g/h/i; hồ sơ #1484 còn nhận toàn bộ F11.b–i và G1–G10 | (ii): đã rút lời hứa closure; nợ có tên; Issue #1484 và quyết định E2 được nêu. |
| kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ đối với phần kế nhiệm | F05.b/c | (ii): đủ ba điều kiện với #1469. Phần khóa byte thuộc wp1466 giữ kết luận đã đóng của lượt trước. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ đối với reader kế nhiệm | F06 | (ii): đủ ba điều kiện với #1469; không mở rộng G1 của cổng protocol sang các reader khác. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ | F07 | (ii): đủ ba điều kiện với #1470. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ | F10 | (ii): đủ ba điều kiện với #1470. |

Không tách/gộp lớp và không đổi slug; không cần bảng nối mới. Sáu slug ở `lop_lan_thu_tam` tiếp tục danh sách lịch sử của lượt 7, **không** có nghĩa cả sáu còn mở trong wp1466. Bộ đếm severity và biểu hiện ở đầu verdict chỉ đếm bảng (i).

**Hội tụ:** U=1 đúng chỉ thị; F=0 vì không lớp nào trong U được vá thật. R7→r8 vẫn là 0/1, không lấy việc bảng (i) về 0 thành tỷ lệ vá 100%. Hai chuyển tiếp thấp liên tiếp và lịch sử lớp lặp vẫn còn trong hồ sơ §12. Quyết định E2 “Tách khối ra (Recommended)” là cách xử lý checkpoint được cung cấp cho lượt này; không reset ngân sách hay lịch sử, và không cần tự mở thêm vòng hỏi chủ kho để lặp lại quyết định ấy.

## BẢNG LỚP (i) — lớp MỞ của wp1466

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|

**0 lớp, 0 biểu hiện P0–P3.** Không có finding mới hoặc lớp đã đóng bị tái mở bởi phần thay đổi r7→r8. Các giới hạn tiền kiểm bên dưới thuộc bảng (ii), không bị đổi tên thành “đã vá”.

## BẢNG LỚP (ii) — nợ kế nhiệm có authority

| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | Mục 0:21 loại consumer ngữ nghĩa/khai báo ca/mục Nợ; ADR:255, 314–315; mục 14:743; N1–N16 chỉ kiểm phần wp1466. |
| duong-dan-chua-khep-trong-goc | F06 — ba reader kế nhiệm | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | Mục 0:21 loại toàn bộ ba reader và containment; mục 19:860 giới hạn rõ phần protocol. |
| moc-chuyen-tiep-mau-thuan | F07 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Mục 0:22; ADR:256 giao vị từ cho packet sau; mục 14:739/744; mục 19:861. |
| schema-bo-sot-provider-hop-le | F10 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Mục 0:22 loại schema/provider/consumer; mục 14:739/744; mục 19:864. |
| tien-kiem-lease-chua-du | F11.b–i, gồm phần còn mở F11.f/g/h/i; G1–G10 | #1484, depends_on [1466] | INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE | Mục 0:23/47–51; mục 1:74/81–96; mục 9:515; mục 14:745; D12/D17; mục 18:837/839; mục 19:865/878. Không có khối tiền kiểm hay tiêu chí nghiệm thu closure còn hiệu lực. |

Đã áp **cả ba điều kiện** cho từng hàng: (1) không còn lời hứa/tiêu chí về chính biểu hiện, (2) có tên nợ, (3) có Issue kế nhiệm. Hai tên nợ cũ có trong ADR ở dòng 291–292 và 314–315; tên nợ mới-kế-nhiệm đã tồn tại ở dòng 281–282 và ô INV-02 dòng 369. Patch bằng byte xác nhận không lén nhận lại mã của các packet kế nhiệm.

Authority #1469/#1470 là E2 “Duyệt tách 3 packet” ở comment 7053593553; authority #1484 là E2 ở comment 7058057029. Dùng các sự kiện do chỉ thị cung cấp cùng hồ sơ trong đặc tả, **không khai đã readback GitHub trực tiếp**. Dòng 745 còn lưu tên đề xuất ban đầu của #1484 và ánh xạ sang tên chốt hiện có; chỉ thị cũng xác nhận tên chốt ấy.

**Riêng D17 — liên kết #1484 không nằm trong ADR:** không làm hỏng điều kiện (2) hoặc (3). Điều kiện (2) cần nợ có tên: tên hiện diện trong chính mục Nợ của ADR, và INV-02 trỏ đúng tên. Điều kiện (3) cần nêu Issue kế nhiệm: các mục 0, 1, 14 và D17 nối đích danh tên ấy với #1484. Không có yêu cầu trong chỉ thị/§8.3 buộc hai dữ kiện phải nằm trên cùng dòng ADR. Đây là khác vị trí ghi liên kết so với #1469/#1470, **không phải finding P3**; không có liên kết chết hay đích kế nhiệm thiếu để buộc sửa. Thêm liên kết vào ADR mà giữ tên nợ cũng không tự buộc đổi K01; D17 chỉ gắn việc đổi K01 với phương án **đổi tên**. Không có mâu thuẫn kỹ thuật ở lý do ấy.

## RÀ TOÀN VĂN VÀ ĐIỀU KIỆN 3a–3e

Đọc toàn văn, không dùng tổng grep làm bằng chứng ngữ nghĩa. [scope-scan.log](scope-scan.log) lưu 66 dòng ứng viên từ phép tìm rộng; [audit-text.log](audit-text.log) và [followup.log](followup.log) tách cấu trúc, lịch sử và ảnh hưởng locale.

| nơi | kết quả đọc nghĩa |
|---|---|
| Mục 0 | Ba lời hứa hiện hành chỉ là ADR, protocol và cổng khóa văn bản. Đoạn r5/r6/r7 được gắn lịch sử; 47–51 rút khối và giao nợ. |
| Mục 1 | 3a–3e là điều kiện vận hành với công cụ hiện hữu; 74 và 81–96 bác rõ lời hứa closure. G1–G10 bao nguồn ref, write set/closure, mã, import, quote, race, cấu hình, danh tính và đồng hồ. |
| Mục 3, bảng INV | S1/S4/S16/S17 là số đo lịch sử theo dòng 107. S18 chỉ đo công cụ hiện hữu và vẫn bị B4 chặn. Dòng 135 thêm #1484; ô INV-02 giữ `còn nợ`, không tự nâng thành cổng đủ §5. |
| Mục 6–8 | Không bổ sung công cụ tiền kiểm vào write set hay M1–M4. Câu mục 6:173 về các **cổng mới** chưa được giao không đặt hợp đồng cho công cụ của Issue proposed #1484; mục 14 đã nêu rõ packet ấy cần đặc tả riêng. |
| Mục 9 | Đoạn đầu tách điều kiện cấp lease khỏi acceptance của H. Cả 16 hàng N1–N16 không nhận lại tiền kiểm. Những câu “khi không đo được thì đỏ” ở M3/G1–G9/N4 nói về reader/cổng protocol, không phải G1–G10 của tiền kiểm. |
| Mục 14 | Giao đúng tên nợ cho #1484, không đặt thiết kế hoặc nghiệm thu công cụ kế nhiệm. |
| Mục 16–17 | D12 nhận giới hạn, D17 chỉ giải thích liên kết. Không thêm câu hỏi, quyền cấp lease hay quyền merge. G1 trong C3 về Windows/resolve là G1 của **cổng protocol** ở mục 8.3, không phải lời hứa đóng G1 của bảng tiền kiểm. |
| Mục 18–19 | Những bộ 19/33/54 kịch bản và 3/14 đột biến tiền kiểm được ghi đã rút. Dòng 839 giữ trạng thái chưa đủ điều kiện thật. Dòng 878 không xin nhãn ĐÃ VÁ THẬT. |

**3a:** So cặp tên/OID hai chiều đúng hơn chỉ so số nhánh; ca cùng tên đổi OID làm hai tập lệch dù số lượng bằng nhau. Không shallow và timestamp vẫn cần cho việc cấp lease thật. Lệnh fetch được giữ từ r7 không có `--prune`: ca ref dư cho thấy fetch ấy chưa tự dọn được ref đã mất trên origin, còn `fetch --prune` như S18 thì dọn được. Điều kiện hai chiều bằng nhau vẫn chặn; không phải kết quả “không người giữ” giả. Không xếp đây thành lớp mới do r8 sinh ra, cũng không diễn giải câu fetch thành cam kết tự chữa mọi trạng thái clone.

**3b:** Lệnh NUL đo đúng cây master tại lúc chạy, gồm hai đường policy/schema canonical. Hiện policy: phải dừng; policy đã xuất hiện rồi bị rút giữa hai lần đo: endpoint không thấy lịch sử đó, đúng G3. Không còn lời hứa đọc lịch sử hay chứng minh closure rỗng suốt khoảng thời gian. Output danh sách rỗng ở bước kiểm vắng được phân biệt với lệnh hỏng bằng rc và phép ghi số 0; không lấy lỗi công cụ thành vắng policy.

**3c:** Công cụ thật trả đúng rc0/`NGƯỜI_GIỮ 0`, rc11 khi có người giữ, rc12 khi không xác định. Nó không tự chuẩn hóa, so prefix hoặc effective write set theo §5; fixture prefix cho rc0 như G2 khai. Chưa có bằng chứng cấp lease thật hợp lệ chỉ từ output ấy; r8 không hứa điều này. Việc chuẩn bị lại clone khi rc12 thuộc người cấp lease, không phải quyền reviewer sửa nguồn.

**3d:** Đã quét 394 ref origin: 0 ref có ADR từ 0068 trở lên. Số ADR trên master là 66. Nếu có cạnh tranh số ADR thì điều kiện này dừng/revision; không có giả định master là nơi duy nhất chứa ADR mới.

**3e:** Điều kiện có thể đạt với công cụ nguyên trạng: fixture mới có một lease trên ref đăng cho rc11, đúng ID/ref/tệp; thêm người giữ thứ hai làm vị từ không đạt; bia mộ hai chiều loại người cũ đúng nhãn. Kiểm riêng provenance cho thấy scanner khử trùng `(blob, path)`: nếu cùng lease còn trên nhánh local được đọc trước, nó chỉ in ref local, nên 3e không đạt dù tổng người giữ là 1. Đó là một trường hợp từ chối bảo thủ, không có căn cứ gọi là xanh giả; nó cũng cho thấy “dòng cuối 1” không thay được vế ref/tệp. Không đo CAS, xác thực danh tính hay quyền thu hồi thật; các giới hạn vẫn là G1/G7/G9.

**Protocol §4/§5 và C5:** R8 không biến thiếu cổng thành miễn các bất biến lease, generation, hạn, write set và authority. Câu dòng 96 nói về giới hạn **hợp đồng wp1466**, không tuyên bố lease sai thành hợp lệ theo protocol. E2 cho phép rút công cụ riêng và dùng phép đo hiện hữu; nó không cho executor tự cấp lease. Điều kiện 1 vẫn cần chủ kho duyệt băm, điều kiện 2 vẫn cần B4 trên first-parent master, điều kiện 4 vẫn đo neo trên base thật. Các bước 3a–3e là bộ kiểm vận hành đã được chấp thuận, **không phải chứng minh đầy đủ §5**.

Không mâu thuẫn với C5/quyết định E5 đi thẳng master: phép so ref/read lease không buộc tạo integration branch. Ngoại lệ chỉ bao #1466/#1469/#1470; không tự bao B4 hoặc #1484. `depends_on: [1466]` của #1484 không cấp cho nó đường merge riêng; packet ấy có đặc tả/quyền riêng theo mục 14.

## BẢNG SĂN

Tám hướng dưới độc lập về cơ chế. H1–H7 dùng Git thật và CLI scanner nguyên byte từ master, chỉ tạo dữ liệu lease bình thường trong fixture; các bản ghi đó **không phải lease đã được cấp quyền thật**. H8 chỉ đọc tên tệp có sẵn, không dựng tên tấn công. Lệnh chung `/usr/bin/python3 -B out/hunt_steps.py`; [hunt-commands.json](hunt-commands.json) giữ argv, cwd, rc, stdout, stderr của 192 lệnh. [hunt-steps.log](hunt-steps.log) là output tổng hợp thực chạy.

| hướng độc lập | LỆNH | OUTPUT THẬT | kết luận / giới hạn |
|---|---|---|---|
| H1 — stale OID và ref dư | `/usr/bin/python3 -B out/hunt_steps.py` (H1: `ls-remote --heads`, `for-each-ref`, fetch) | `SAME_NAMES True PAIRS_MISSING_EXTRA 1 1`; `FETCH_PAIR_EQUAL True`; `NO_PRUNE_EXTRA 1`; `PRUNE_EXTRA 0` | So cặp có răng; fetch không prune không tự xóa ref dư. Không phải proof server thật. |
| H2 — policy có mặt rồi rút | Cùng lệnh (H2: `ls-tree -r -z`, `log --all -- <policy>`) | `PRESENT 1`; `WITHDRAWN 0 HISTORY_COMMITS 2` | Xác nhận biên endpoint của G3; không còn cam kết closure lịch sử trong r8. |
| H3 — trước/sau đăng và cạnh tranh người giữ | Cùng lệnh (H3: CLI `ai-dang-giu`) | `BEFORE rc 0`; `AFTER rc 11`; `POST_PREDICATE True`; `TWO ... NGƯỜI_GIỮ 2`; `TWO_POST_PREDICATE False` | 3c/3e không tự mâu thuẫn và có trường hợp đạt/không đạt thật. |
| H4 — trạng thái bia mộ hai chiều | Cùng lệnh (H4: CLI trên cặp lease cũ/mới) | `ONE_SIDED rc 12`, lý do `bia mộ một chiều`; `TWO_SIDED rc 11`; `OLD_MARKED True NEW_POST True` | Không lấy rc12 thành không người giữ; vế loại nhãn ĐÃ_BỊ_THAY_THẾ của 3e phù hợp output thật. |
| H5 — dữ liệu không đọc được và hạn | Cùng lệnh (H5: sai kiểu ánh xạ, giờ không đọc được, lease hết hạn) | `wrong_shape rc 12`; `wrong_time rc 12`; `expired rc 0 ... NGƯỜI_GIỮ 0` | Phân biệt không xác định với hết hạn; không giả mạo clock hoặc payload mã. |
| H6 — ngữ nghĩa prefix của write set | Cùng lệnh (H6: lease giữ thư mục `.claude/dev/`, hỏi tệp con) | `PREFIX rc 0 ... NGƯỜI_GIỮ 0`; `DECLARED_G2 True` | G2 là thiếu hụt thật còn nguyên, chuyển nợ đúng; không được gọi đã vá. |
| H7 — provenance sau khử trùng blob/path | Cùng lệnh (H7: cùng blob hợp lệ ở nhánh local và ref origin) | `LOCAL_COPY rc 11 ... NGƯỜI_GIỮ 1`; `POST_PREDICATE False`; hàng chỉ trỏ `refs/heads/local-copy` | 3e có thể từ chối bảo thủ; tổng ID không đủ chứng minh ref đăng. Không nhận nó thành lỗi xác thực mới ngoài nợ đã khai. |
| H8 — giao thức tên Git gián tiếp | Cùng lệnh (H8: `ls-tree -r HEAD -- <tên Unicode có sẵn>` và đối chứng `-z`) | `DEFAULT PATH_EQUAL False SUFFIX_LOG False`; `NUL PATH_EQUAL True SUFFIX_LOG True` | G6/F11.i còn thật. Không dựng hay khai đã chạy ca bỏ lease YAML đầu-cuối. |

Ngoài tám hướng này, phép đọc nghĩa toàn văn, so byte, băm khóa, quét số ADR và trần là những kiểm bắt buộc riêng; không dùng chúng để làm tròn số hướng săn.

## BẢNG ĐO

Thời điểm reviewer: 21-11-2026 UTC, từ 05:52 đến 05:58 cho các phép trong bảng; timestamp cụ thể trong log. “Khớp snapshot” không xác minh lại máy chủ tại 05:41 của tác giả.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| SHA/băm | e215940… / 98790505… | HEAD, tree và blob khớp; băm đầy đủ ở đầu verdict | Có |
| Kích thước đặc tả | r7 1022 dòng/184992 byte; r8 882/158467 | Đúng cả bốn số | Có |
| Khối giữ lại | khóa, protocol, ADR, N8, sổ không đổi | 12/12 khối bằng byte; chỉ `tien-kiem` bị rút | Có |
| Nguyên mẫu | sha256 838bbccb…; 4 tệp +434 −4 | Băm đầy đủ `838bbccba7309c0989fb22b0433b7e33c683677129061bd0a9bef5b203123b55`; numstat 76/1, 163/1, 46/2, 149/0 | Có |
| Các ref origin S18 | 394; thiếu/thừa cặp 0/0; không shallow | 394/394; 0/0; false, origin là mirror cục bộ | Khớp snapshot; chưa đo server thật |
| Master S18 | 4e56f005785db1b04e043bb71fc694a674a8dc9f | Đúng OID | Có |
| Policy trên master | 0 đường dẫn chứa change-impact | 0 | Có |
| Số ADR | master 66; 0/394 ref có số ≥0068 | 66; 0/394 | Có |
| Người giữ hai tệp Python | B4 wp1462-r8-g2-claude, rc11 | Đúng ID, ref `origin/ops/wp1462-r1` và tệp lease, cả hai rc11 | Có |
| Người giữ protocol/ADR mới | 0/0, rc0 | 0/0, rc0 | Có |
| Bản ghi/hạn/bia mộ/còn hiệu lực | 551/17/12/5 | 551/17/12/5 tại giờ S18 và giờ đo reviewer | Có; dùng clock/ảnh snapshot |
| Năm lease còn hiệu lực | wp1236-a-r10-g1-claude-20261121; wp1448-r6-g6-claude; wp1462-r8-g2-claude; wp1475-r1-g1-claude; wp433-r9-g5-claude | Cùng tập năm ID | Có |
| Grep khối/bảng/marker cũ | tổng 3 | Khối 0; hàng V 0; marker lịch sử 3 ở dòng 114, 126, 127 | Có; ba marker không phải hợp đồng hiện hành |
| Grep trích đoạn của tác giả | log rà tại 05:47:03Z | `LC_ALL=C`: 58 kết quả, **bằng byte** log; `C.UTF-8`: 86 kết quả | Khớp khi cùng locale; không coi grep là proof ngữ nghĩa |
| Liên kết #1484 | tên nợ có sẵn, nối trong spec | 18 lần nhắc trên 16 dòng; tên có trong ADR/INV-02; ADR không có #1484 | Đúng D17 |
| Bảng INV/Nợ | 28; 15 cổng có nợ; 12 kỷ luật; 1 chưa đo; 18 trỏ ca; 25/27 tên nợ | Đúng từng số, thiếu tên 0 | Có |
| Khóa byte/địa chỉ | 7 bộ bốn | Cả 7 address/hash khớp; occurrence 1; hằng mã bằng kết quả độc lập | Có |
| Neo chèn/N8 | 6 neo và 3 mốc, mỗi cái 1 | [1,1,1,1,1,1], ba mốc đều 1 | Có trên nền hiện có, chưa thay base B4 tương lai |
| Vector cổng từng vị trí | số ở mục 3 trên sáu tệp | 29 mẫu, mọi vector khớp; không chỉ so tổng | Có |
| Cổng gốc/sandbox cùng SHA | cần parity | reviewed SHA: cả hai `doctrine-scan` sạch 12 tệp; `adr-song` 66/66, rc0 | Có |
| Cổng nguyên mẫu | doctrine sạch, ADR 67/67 | Cả hai rc0, `diff --cached --check` sạch | Có |
| Ca chọn lọc nguyên mẫu | 190, gồm 132 cũ +57 mới +1 mốc | `CHON 190 CHAY 190 DAT 190 KHONG DAT 0`, 58 giây | Có; không phải full suite |
| Hiện vật kèm r8/r5 | SHA256SUMS | 6/6 và 20/20 khớp | Có |

Nguồn: [setup-measure.log](setup-measure.log), [measure-snapshot.log](measure-snapshot.log), [audit-text.log](audit-text.log), [followup.log](followup.log), [check-prototype.log](check-prototype.log), [prototype-cases.log](prototype-cases.log). Bốn log `lease-path-0.log`…`lease-path-3.log` giữ output CLI đầy đủ.

Hai sai biệt harness được giữ rõ: bộ đếm nháp trong `setup-measure.log` bắt cả sáu bullet N1–N6 ngoài mục Nợ nên in 33; parser giới hạn đúng mục Nợ trong phép độc lập xác nhận **27**, không phải lỗi đặc tả. Lần tái lập grep đầu ở locale UTF-8 không bằng byte log; đối chứng C xác nhận log tác giả là phép khớp theo byte. Các mảnh UTF-8 bị cắt ở biên trích đoạn trong log C không chứng minh văn bản đặc tả hỏng.

## KHÔNG TÁI MỞ, L3, L6, L7 VÀ TRẦN

**Không tái mở:** [r7-r8.diff](r7-r8.diff) và phép trích khối xác nhận toàn mục 2, 4–8, 10–12, 15 giữ nguyên; mục 9 chỉ đổi phần giải thích điều kiện cấp lease, các tiêu chí và hai khối mã giữ nguyên. Patch sản phẩm bằng byte r7, phần mã của các cổng không đổi. Tự ráp sáu sửa protocol từ spec cho đúng byte nguyên mẫu; tự băm địa chỉ/raw cả bảy khóa; đối chiếu cả mười bất biến gốc sau nối dòng riêng từng mục; chạy lại 190 ca chọn lọc. Không chạy lại toàn bộ 167 biến thể hoặc 26/21 mutant của các lượt cũ, và không khai số cũ là kết quả mới của lượt này.

**L3:** Điều kiện 3a–3e có phép đo phân biệt đạt/không đạt trong phạm vi đã khai; H3/H4 có đối chứng dương và âm thật. R8 không dùng chúng để thay tiêu chí closure đã rút. N1–N16, ca và mutant của cổng protocol không đổi; giữ bằng chứng răng đã được review trước, bổ sung kiểm byte và ca hiện tại. N13–N16/Windows/land chưa có bằng chứng mới, không đánh dấu đạt.

**L6:** Grep `0 khối` hay tổng `3 marker` một mình không chứng minh hết lời hứa; đã đọc riêng các mục bắt buộc và phân loại lịch sử/giới hạn/cổng protocol. Locale làm regex trích đoạn khác số kết quả, nên không dùng số trích đoạn để đóng lớp. Phép khóa raw không chuẩn hóa xuống dòng để làm xanh; phép so mười bất biến gốc mới nối dòng trong biên từng mục. Các số cổng được so riêng sáu vị trí. Việc thấy tên cổng vẫn không chứng minh cổng cưỡng chế toàn bộ INV.

**L7/ADR-0067:** Không có ngân sách mềm hay điểm hỏi tự đặt ở lượt thứ N. Các điểm dừng tiếp tục dẫn protocol/ADR; câu hỏi C1/C4 mang E5, C3 mang E2. Quyết định tách tiền kiểm đã có authority do chỉ thị cung cấp; không hỏi lại. Duyệt băm, miễn Windows, audit exact-H và bấm merge vẫn là các quyền riêng chưa được verdict này cấp.

**ADR-0053/0055:** Mỗi opt-in có đúng một dòng hợp lệ; OID land của hai ADR đọc được tệp (`rc0`), parent thứ nhất chưa có (`rc128`), và OID nằm trên first-parent master của mirror. Không có opt-in 0052. Trần là **6 tệp/450 dòng thêm** và **10 lời gọi** theo các điều kiện đó. Nguyên mẫu 4 tệp/+434 còn 16 dòng tới trần, không bảo đảm mã giao nộp tương lai vẫn vừa. Lời gọi này **9/10 theo chỉ thị**; còn 1 nếu không có tiêu dùng khác chưa được giao. Không reset theo revision, provider hoặc việc chuyển sang #1484; không tự suy lịch sử API từ số verdict.

## HIỆN VẬT VÀ NHỮNG GÌ KHÔNG ĐO ĐƯỢC

- Chỉ đo Git cục bộ/mirror 394 nhánh; `ls-remote` trong các phép tái lập trỏ mirror hoặc fixture dưới `out/`. Không fetch GitHub, không readback Issue/comment/ruleset hiện tại; không xác thực lại máy chủ, transport, auth hay timestamp REST của tác giả.
- Không cấp/thu hồi lease thật. Dữ liệu trong các fixture chỉ đủ cho scanner đọc, không được khai là vượt cổng công bố/đã có authority. Không thử thực thi công cụ độc hại, traversal, tên lease đối kháng, can thiệp clock hay race trên server.
- Không đo đầy đủ G1–G10 và không biến sự vắng phản chứng thành an toàn. Giới hạn còn nguyên là lý do giữ lớp tiền kiểm ở bảng (ii), với nhãn CHƯA VÁ.
- Không chạy full selftest, full packet-loop suite, full mutant CI, Windows hoặc N16 sau land. Không có mã giao nộp dựa trên B4 cuối cùng; phải đo lại neo, base, số ADR, lease, gate và numstat khi triển khai thật.
- Họ reviewer lấy theo identity Codex/OpenAI; họ executor Claude theo chỉ thị. Model/effort backend và session ID được máy xác thực: **KHONG_DO_DUOC**; không suy từ model được yêu cầu trong spec. Assurance ở header là đề nghị cho nội dung review, còn receipt/identity validator bên điều phối phải nhận đúng hiện vật lượt này.
- Sandbox thực là `workspace-write`; tính chỉ đọc của nguồn được thực hiện bằng giới hạn thao tác và kiểm snapshot, không giả nhận toàn bộ nguồn bị kernel khóa. Snapshot nguồn trước phép thử và sau cùng kiểm cả file ignored/untracked, hash nội dung, size, mtime và symlink của `cay-kho`/`kho.git`; chỉ chứng minh không có delta giữa hai mốc, không chứng minh lịch sử không từng ghi rồi hoàn nguyên. Kết quả đóng gói ở [final-check.log](final-check.log), [SHA256SUMS](SHA256SUMS).

Kiểm cuối: **18.171 mục nguồn ở cả hai mốc, delta 0**; git status rỗng, HEAD/tree/spec hash giữ nguyên. Bảng (i) rỗng nhờ chuyển phạm vi có authority; năm lớp nợ kế nhiệm giữ nguyên slug và nhãn CHƯA VÁ.
