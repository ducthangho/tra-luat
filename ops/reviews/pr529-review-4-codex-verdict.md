verdict: blocked
reviewed_sha: a97d95c1763af30aa26750ef4d5246cfc4aa1206
so_p1: 0  so_p2: 9  so_p3: 0
so_the_hien: 18

Packet #523 `QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG`, revision 5, generation 4; PR #529; lượt 4. Executor Claude, reviewer OpenAI/Codex. `review_class=sensitive`: **không approve**. Cần điều phối xử lý S9/S10 và mâu thuẫn trong spec đóng băng; không được tự nới phép đo để chuyển sang xanh.

Bản vá sản phẩm duy nhất đã sửa đúng con trỏ severity sai. Sáu probe gốc đều rc=0, các số 201 dòng, 9/9, 3 tín dụng giả của oracle cũ đều tái lập được. Tuy nhiên, probe A9 lọc mất đường ngoài phạm vi; A17 nới tập chấp nhận; A18 nhận thiếu kết quả không đích; A20 chưa đóng hai lớp cũ; A19 chỉ dò từ khóa và đối chứng không chi phối kết luận. Đây là lỗi của **bằng chứng nghiệm thu**, không phải khẳng định các bảng thật đang mang dữ liệu đột biến.

Mức P2 của các lớp kế thừa được giữ; lớp mới dùng mức tương ứng với các lỗi nghiệm thu đã được lượt 3 xếp P2. Không tự định nghĩa lại P1/P2/P3 để lấp nợ của kho. Số đếm hiện hành chỉ gồm các thể hiện mở liệt kê dưới đây; ca dương, lớp sạch, giới hạn chưa đo và ca kiểm lại đã bị giết không cộng vào findings.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh ở mọi dòng chạy từ gốc sandbox; đặt `TMPDIR="$PWD/review-artifacts/tmp" PYTHONDONTWRITEBYTECODE=1`. Log đầy đủ trong `review-artifacts/`. Các phép kiểm lại ở mục này **không** cộng vào tám hướng săn.

| slug canonical | phán | phép đo tự chạy và phạm vi kết luận |
|---|---|---|
| `a9-bo-sot-delta-trong-merge` | **VÁ SINH LỖI MỚI** | `python3 probes/do_a9.py`: 201 ≤ 300; fixture resolution 305 bị bắt, lỗi cộng đôi/khoảng rỗng cũ đóng. Nhưng `python3 review-artifacts/facts4.py` tạo index tạm có `extra.txt`: phép lọc vẫn 62+139=201, đủ hai đường; full diff thấy đường thứ ba. Giữ slug cho lớp phép chọn delta không bao phủ nghĩa vụ; không nói số học endpoint còn bỏ sót resolution. |
| `a17-whitelist-bo-roi-m8` | **VÁ SINH LỖI MỚI** | `python3 probes/do_a17.py`: +62/−0, gỡ M8 làm 13 dòng ngoài whitelist. M8 thật đã được cho phép. `review4.py H1`: dòng ngoài nhóm đứng riêng ĐỎ, ghép vào khối hợp lệ ĐẠT; từ mới cho phép cũng nhận câu vô hại ngoài nhóm. Whitelist nay bỏ lọt theo chiều đối diện. |
| `dem-dot-bien-khong-theo-tieu-chi-dich` | **VÁ HỜ** | `kiem_a18.py` từ chối oracle cũ đúng 3 ca; `review4.py H3`: thiếu kết quả không đích vẫn 9/9, rc=0. Điều kiện 3 của A18 chưa được kiểm đủ. |
| `bo-doc-bang-vuot-ranh-gioi-muc` | **VÁ HỜ** | `review4.py canonical`: A1 qua `##` bị chặn đúng; bảng đơn vị A2 đặt dưới `## Phụ lục` vẫn `(True, 'ok')`. Guard vẫn bị tắt trên đường A2. |
| `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` | **VÁ HỜ** | `review4.py canonical`: đổi đơn vị so_the_hien bị bắt, nhưng lặp hàng sensitive vẫn True. `review4.py H5` mở thêm các chiều số cột/tên trường; H4 cho thấy cùng cơ chế dò từ tái phát ở A19. |
| `con-tro-dinh-nghia-phan-hang-sai-dich` | **ĐÃ VÁ THẬT** | `review4.py H6`: đúng một khối thay đổi, bỏ lời hứa sai, giữ con trỏ ngưỡng §12 và khai nợ; work-packet byte-identical. Đã đọc §12/3.2/8/13. Đây là kết luận về bản vá trong kho; mâu thuẫn A2 còn sót trong SPEC được xếp ở lớp nhất quán spec riêng bên dưới. |
| `bien-nhan-thieu-so-ci-da-chi` | **CHƯA VÁ** | `review4.py canonical` và H8: receipt lượt 4 `[]`. Không đo được hiện vật tương lai; không nhận lời hứa là đã vá. C1 của lượt 2 vẫn được giữ làm nợ lịch sử, không yêu cầu sửa biên nhận bất biến. |
| `phep-do-doctrine-khong-du-rang` | **CHƯA VÁ** | `python3 review-artifacts/gates4.py`: scanner gốc 0, câu trần ADR 0, §5.1 0, §12 6. Hai phản chứng còn sống; S4 không cho vá scanner. |

## BẢNG SĂN

Tám hướng độc lập theo bề mặt đo: phân loại khối; miền đường dẫn diff; hợp đồng kết quả oracle; kiểm con trỏ/đối chứng; lược đồ cột; bảo toàn nghĩa vụ qua patch; nhất quán spec/stop; biên nhận chưa tồn tại. H1–H5 là biến thể mới, không dùng nguyên các ca lượt 3 để đủ số hướng. `canonical` và sáu probe gốc nằm ngoài phép đếm tám hướng.

| hướng | giả thuyết, lệnh thật | output thật rút gọn | kết luận |
|---|---|---|---|
| H1 — phép nới A17 | `python3 review-artifacts/review4.py H1` | `separate block: (False, 0, [...])`; `attached ...: (True, 0, [])`; classifier `None`; keyword mới True, bỏ keyword False | **LỖI**: cả sửa theo khối lẫn mở từ khóa đều có mở rộng sai. Ba fixture cũ vẫn đỏ không chứng minh không nới. Hoán vị hai ô hành động M8 cũng True; riêng việc A17 không kiểm đúng nội dung M8 **không** bị đếm thêm, vì whitelist theo nhóm; M8 vẫn phải đọc riêng. |
| H2 — đường bị loại trước predicate | `python3 review-artifacts/review4.py H2`; `python3 review-artifacts/facts4.py` | full diff có `extra.txt`, filtered chỉ hai skill, 201 additions; hai tên skill sai cũng `(True, 'tong additions = 2 ...')`; 299/300 True, 301 False | **LỖI** miền quan sát A9, S10. **KHÔNG PHẢI LỖI** tại biên số học 300; chưa có phản chứng cho phép đếm net additions của đúng hai endpoint/đúng hai tệp. |
| H3 — oracle thiếu kết quả | `python3 review-artifacts/review4.py H3` | A2_stub rc1, 3/9; always_red rc2; both_red_on_change rc1, 0/9; missing_nontarget rc0, 9/9; fixture_only rc0, 9/9 | **LỖI** do missing non-target. Ba loại stub bị từ chối là **KHỚP**. Oracle tra đúng fixture được nhận là giới hạn của bộ hữu hạn, không tự tính thành lỗi hay đòi suite chứng minh mọi oracle. |
| H4 — con trỏ có từ mà không có hợp đồng | `python3 review-artifacts/review4.py H4` | bốn section chỉ có vocabulary: predicate cả bốn True; ép control thất bại: `LA?`, rc0 | **LỖI** phép đo A19 ở hai cơ chế. Đọc tay bốn đích thật thì lời hứa thật **KHỚP**; không phán con trỏ thật sai chỉ vì checker yếu. |
| H5 — schema cột và trường chưa đo | `python3 review-artifacts/review4.py H5` | A1 extra column=True; A2 thiếu so_p2/so_p3=True; đổi hai tên cột đầu=True; thêm cột đơn vị=True | **LỖI** A20: cardinality và danh tính trường chưa được khóa. Đây không phải lặp nguyên ca duplicate/đổi đơn vị lượt 3. |
| H6 — bản vá có mất M1–M15 không | `python3 review-artifacts/review4.py H6` | `changed blocks: 1`; work unchanged=True; removed lines đúng 2 dòng severity; recurrence pointer=True; debt=True | **KHÔNG PHẢI LỖI** của bản vá a97d95c: M1–M14 ngoài khối này nguyên byte; M15 cải thiện đúng. Không chứng minh tất cả nghĩa vụ lịch sử được thực thi chỉ từ byte. Nợ thiếu định nghĩa thuộc kho, không riêng packet. |
| H7 — nháp có miễn nghĩa vụ; S9–S11 và luật r5 | `python3 review-artifacts/review4.py H7` | draft=True; M6 prohibits=True; S9/S10/S11=True; stale formula vẫn có; A2 permits severity pointer=True, A19 removes=True | **KHÔNG PHẢI LỖI** vì nháp không phải cổng: không có câu miễn A20/M14. **LỖI** hai luật cũ còn hiệu lực văn bản trong spec r5. S9/S10 có trigger đo được; việc executor thực dừng và authority GitHub **KHÔNG ĐO ĐƯỢC**. S11 là cấm có thể đọc/audit, chưa là cổng máy. |
| H8 — khả năng thi hành A16 từ lượt 4 | `python3 review-artifacts/review4.py H8`; `python3 ops/bien_nhan_v2.py --root .` (cwd cay-kho) | schema source keys=False/False; receipt4=[]; applies-from-4=True; schema rc0, 117 đạt, tổng170 | **KHÔNG PHẢI LỖI MỚI** vì spec đã khai schema-pass ≠ A16-pass và là kỷ luật đọc. Nghĩa vụ có thể kiểm khi receipt tới; receipt tương lai **KHÔNG ĐO ĐƯỢC**, lớp C1 không được đóng. |

Các fixture mới dùng dữ liệu vô hại, thay cấu trúc bảng, đổi ô đã có hoặc stub kết quả. Không tự soạn payload tấn công. Hướng phủ định giới hạn dùng đúng ca do packet cung cấp trong `do_a17.py`; không tạo biến thể nội dung tấn công. Nếu muốn thử chỉ thị đối nghịch nằm trong khối M8/A2, điều phối cần đo hộ; review này chỉ mô tả hướng đó.

## BẢNG ĐO

Nguồn đầy đủ: `review-artifacts/do_*.log`, `dotbien.log`, `kiem_a18.log`, `H1.log`–`H8.log`, `canonical.log`, `controls4.log`, `facts4.log`, `gate-*.log`, `scanner-*.log`. Script tái lập là `review4.py`, `facts4.py`, `controls4.py`, `gates4.py`. Mọi đường artifact là tương đối với sandbox này.

| lời khai EVIDENCE | tự đo lại | phán / giới hạn |
|---|---|---|
| Exact SHA a97d95c… | rev-parse đúng 40 hex; tree `f7a591b3f006884a1153123179e70d237f1d6605` | **KHỚP** |
| SPEC hash 32859b68… đo từ blob | SHA-256 SPEC.md = `32859b68ecba880c26645f845b1d3611bd844dd01617339b89f01e0354209a95`; `git --git-dir kho.git show claude/spec-quy-trinh-r5-20260912:ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r5.md` cùng băm | **KHỚP** local blob/lease/file; ref không có trong clone working nhưng có trong bare. Không chứng thực authority comment. |
| Lượt 3 blocked, 8 lớp/11 thể hiện | đọc VERDICT-luot3.md, bảng lớp và thể hiện | **KHỚP hồ sơ**; sự kiện đăng GitHub là thuật lại |
| Giữ M8, một phép A9 do chủ kho chọn | SPEC/LEASE cùng khai; có comment IDs | **KHÔNG ĐO ĐƯỢC** authority trên GitHub, không giả làm đã readback |
| Ba lời khai đã rút | +55/−0 trên 6c26fe0 đo bằng numstat; fixture305 vs4; `controls4.py`: oracle cũ positive rc0, 7 ca đều rc1, luật cũ cho7/7 | **KHỚP việc bác**; không dùng +39/−0, “fail-closed” hay “0 tín dụng giả” cũ làm tiền đề |
| Bản vá r5 đúng một thay đổi | diff từ 6c26fe0 đúng một tệp/một khối; hai patch cung cấp và numstat khớp Git từng byte | **KHỚP** |
| Bỏ con trỏ sai, giữ ngưỡng §12 | H6 và đọc bốn section thật | **KHỚP**, lớp con trỏ sản phẩm đóng |
| Không nguồn có thẩm quyền định nghĩa cả ba; prompt không là doctrine | §8 có P1, thiếu P2/P3; §12 thiếu cả ba; đã đọc các section | **KHỚP** thiếu tại protocol. Mệnh đề tuyệt đối “duy nhất trong toàn kho”/thẩm quyền mọi tài liệu **chưa chứng minh toàn diện**; không nâng kết quả tìm chuỗi thành định nghĩa. Nợ khai ở cấp kho là đúng phạm vi. |
| A1'/A2' ĐẠT | `do_a1a2.py`: DAT/DAT | **KHỚP** đối chứng thật; không đủ chứng minh toàn acceptance, A2 probe không đọc work-packet (đã đọc tay nghĩa vụ ĐỌC BẢNG LỚP ở đó) |
| A9 201≤300, ba phép ĐỎ | +62/−0 và +139/−0; ba ca ĐỎ/BẮT ĐƯỢC, rc0 | **KHỚP ca cung cấp**; H2 bác độ phủ ngoài pathspec |
| Fixture resolution r4:4 vs305 | do_a9 chạy Git no-index ra305 trên2 đường, 4 là số hai delta r4 được khai trong fixture | **KHỚP fixture endpoint**; không phải tái tạo commit merge thật; không commit |
| A17 0 dòng xóa/ngoài nhóm | numstat +62/−0; checker ngoai=0 | **KHỚP output**; 0 “ngoài” là kết luận classifier yếu, không chứng minh semantic audit |
| Gỡ M8 làm13 dòng ra ngoài | do_a17:13 và ĐỎ | **KHỚP**; không nhầm13 với tổng18 dòng M8 có cả dòng trống |
| Phủ định giới hạn vẫn −0 và ĐỎ | ca2 do_a17:−0, ngoai=1, ĐỎ | **KHỚP đúng lý do ca ấy**, không chứng minh mọi vị trí đều bị bắt |
| Hai sửa A17 không nới vì ba ca vẫn ĐỎ | ba ca vẫn ĐỎ thật; H1 có False→True cho đầu vào không thuộc nhóm | **BỊ BÁC suy luận không nới**; sửa có thể cần để xử lý bó dòng, nhưng cách hiện tại mở sai tập chấp nhận |
| A18 thật 9/9, 0 tín dụng giả, rc0 | dotbien log có từng đích ĐỎ và không đích DAT; no-op guard, original untouched | **KHỚP cho chín ca thật**, không phải bảo đảm mọi oracle |
| Oracle cũ 6/9,3 giả,rc1; r4 cho7/7 | kiem_a18 và controls4 tái lập | **KHỚP**; H3 thiếu non-target vẫn được9/9 nên lớp chưa đóng |
| A20 hai ca mới bị giết | bỏ hàng và đổi đơn vị so_p1 đều A2 ĐỎ | **KHỚP**, nhưng duplicate A1 và đọc bảng A2 sang mục khác vẫn sống |
| A19 bốn con trỏ và đối chứng | do_a19 cả4 DAT; §12 chứa P2=False | **KHỚP quan sát và đọc tay**, chưa chứng minh phép đo ngữ nghĩa; đối chứng chỉ in, không ràng buộc exit |
| Sáu lỗi lịch sử bộ đo, lỗi chỉ lộ khi chạy | phiên bản hiện tại có regex cấp heading, gon, escaped pipe, casefold; log mới chạy được | **KHÔNG ĐO ĐƯỢC** trình tự sửa/động cơ/“không lỗi nào lộ bằng đọc code”: không có transcript, không nhận tự thuật là phép đo |
| Chín dòng bị A17 báo oan, hai dấu fence | hiện code và lời chú thích kể lại; việc cần hiểu đoạn bó dòng là có thật | **KHÔNG ĐO ĐƯỢC** chính xác lịch sử bản classifier bị sửa; không dùng con số ấy để cho phép cả khối tùy ý |
| Sandbox shallow=false, abbrev7, HTTPS origin, sạch | facts4 kiểm cả bốn | **KHỚP local**, URL không chứng minh truy cập được remote |
| Nguồn363/363; lần thiếu363/362; mirror thiếu0 thừa1 | bare hiện có364 head refs; working clone có1 local head | **KHÔNG ĐO ĐƯỢC** tập nguồn lúc clone và quan hệ tập;364 không chứng minh363+1 là superset |
| Bốn cổng nền↔sandbox cùng rc0 | sandbox doctrine/adr/idiom/doc-claims đều0 | **KHỚP một phía**; phía nguồn và parity môi trường **KHÔNG ĐO ĐƯỢC**, không suy tương đương |
| doctrine-scan rc0 | 7 tệp,0 chỗ,rc0 | **KHỚP**; phản chứng ADR/5.1 vẫn0 |
| adr-song rc0 | 48 ADR/48 hàng,rc0 | **KHỚP** |
| idiom-ba-ten rc0 | `python3 .claude/dev/idiom_py_test.py --kho .`:7/7,9 đột biến,7 tệp,bỏ qua0,rc0 | **KHỚP**;389 lời gọi ngoài phạm vi chỉ chẩn đoán |
| doc-claims-check --strict rc0 | ok=true,strict=true,108 files,376 advisories/claims flagged,flags=[],rc0 | **KHỚP**, không đánh đồng advisory với lỗi cứng |
| release-verify strict/json ok=true,180==180 | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`:ok=true,180/180,rc0 | **KHỚP**. Lần gọi đầu reviewer thiếu positional manifest nên argparse rc2; đã sửa lệnh, log lỗi giữ lại, không ghi thành finding. |
| bien_nhan_v2 rc0 |117 đạt +11 legacy +42 nợ =170;0 vi phạm,0 không đo được | **KHỚP**, không chứng thực A16 hay thực chi CI |
| git diff --check rc0 | working diff trống rc0; `git diff --check dc02c9b HEAD` rc2, whitespace tại verdict lượt1:117–118 | **CHỈ KHỚP không có mốc**. Không sửa hiện vật bất biến, không đếm lỗi whitespace lịch sử thêm lần nữa. |
| tl selftest/lease-publish sẽ đo trước commit receipt4 | NOT_RUN; chưa phải lời khai đã xanh | **KHÔNG ĐO ĐƯỢC** phép chạy tương lai. Không chạy full CI/suite có tạo commit hay cần mạng dưới cấm của lượt này. |
| gate/thu-hoi/Windows/CI gọi tay và N=0 | không gọi mạng/Actions/full CI; không có quan sát consumption ngoài Git | **KHÔNG ĐO ĐƯỢC**, không tự điền0 hay đổi session_run_id thành CI run_id |
| Doctrine chưa vá vì S4 | bản sao scanner0/0/0/6, phục hồi byte | **KHỚP**, giữ hai thể hiện mở |
| A9 không tách ai viết dòng nào | phép diff endpoint không có metadata tác giả từng dòng | **KHỚP giới hạn**, khác với lỗi bỏ đường H2 |
| ADAPTER… chưa đóng tổng quát | chín ca chỉ chứng minh chín ca, fixture-only oracle vẫn qua | **KHỚP giới hạn**, không đòi chứng minh tổng quát để tạo thêm finding |
| Probes là nháp, không commit | sáu tệp nằm ngoài cay-kho; không trong diff sản phẩm | **KHỚP trong bundle**; không miễn nghiệm thu A18/A20 |
| grep-i/tiếng Việt; “mọi phép đo dùng casefold + thu gọn khoảng trắng” | có casefold và NFC/gon ở các đường khác nhau; A17/A2 còn nhiều phép substring cục bộ | **KHÔNG ĐO ĐƯỢC** nguyên nhân lịch sử grep; không có một pipeline chuẩn hóa chung cho mọi phép đo, không suy rằng dùng Python là đủ đo nghĩa |

## CHẤM TIÊU CHÍ VÀ PHÉP ĐO

- **A18'**: yêu cầu đích và không đích riêng là đúng hướng; oracle cũ thực sự bị từ chối. **Bộ đo không đạt** vì không đích vắng bị coi là đúng. Đã thử chốt tập khóa chính xác trên bản sao: mutant thiếu không đích chuyển rc0→rc1,0/9; bộ thật vẫn rc0,9/9 (`controls4.log`). Oracle A2-stub/both-red/always-red đều bị từ chối đúng; oracle tra fixture là giới hạn hữu hạn, không phải một chứng minh oracle đúng.
- **A9'**: công thức một endpoint diff sửa đúng lỗi resolution/cộng đôi cũ, biên300 đúng. **Định nghĩa phép đo và probe chưa đủ phạm vi**: pathspec loại chính đường thứ ba cần bắt; predicate còn chỉ kiểm prefix thay hai tên exact. Ca cung cấp tự thêm một row mà collector thật không bao giờ trả, nên đỏ của ca đó không chứng minh pipeline có răng. S10 áp; không đề nghị executor tự đổi công thức lần nữa.
- **A17'**: whitelist gồm M8 giải quyết xung đột mục tiêu cũ. **Bộ đo bị nới thực tế**: một dấu hiệu ở bất kỳ dòng nào hợp thức hóa cả khối; hai từ mới cũng cho nhận câu chỉ nhắc từ ấy. Các đoạn nối dòng của head có thể cần gom theo câu, nhưng đó không phải căn cứ để nhận mọi câu trong khối. H1 là phản chứng trực tiếp cho cả hai sửa, S9 áp. Whitelist nhóm không tự thay nghiệm thu nội dung M8.
- **A19**: bốn đích thật được đọc tay và phù hợp; tiêu chí “không coi xuất hiện chuỗi là định nghĩa” đúng. **Probe không đạt tiêu chí đó** và control không chi phối kết luận. Đối chứng được gọi “dương” trong code thực chất là ca cố ý sai đích cần bị từ chối. Đã thử nối control vào kết luận trên bản sao: control sai đổi rc0→rc1. Không sửa protocol để tạo định nghĩa severity.

### a9-bo-sot-delta-trong-merge  [P2]  Phép đo delta mất miền đường dẫn cần kiểm

CƠ CHẾ SINH LỚP: Chọn một tập con diff rồi dùng nó làm toàn bộ miền nghiệm thu. r5 đã sửa trục thời gian, nhưng pathspec làm mất trục đường dẫn; giữ slug cũ cho cơ chế quan sát delta không phủ nghĩa vụ.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| G2 | SPEC.md:A9; probes/do_a9.py:14–24 | Index tạm từ HEAD thêm extra.txt: full diff thấy nó, filtered numstat vẫn62/139; a9 nhận. |
| G3 | probes/do_a9.py:21–23 | Hai đường .claude/skills/one.md và two.md được nhận, dù không phải hai skill exact trong A9. |

VẤN ĐỀ: Ca thêm row giả ngoài prefix đỏ đúng, nhưng không đi qua collector thật. Không khẳng định HEAD thật vi phạm write set: diff thật chỉ hai skill và ops/reviews. Vấn đề là không thể dùng phép đo hiện tại chứng nhận mọi cấu hình theo hợp đồng.

ĐÃ THỬ VÁ: Không sửa spec/lease. Điều phối cần thống nhất phép liệt kê phạm vi toàn diff và tập hai tên exact; giữ phép đếm endpoint đã được chọn, kèm phản chứng qua chính collector. S10 yêu cầu báo, không tự đổi acceptance.

ĐÃ THỬ NGHIỆM: `review4.py H2`, `facts4.py`; scratch GIT_INDEX_FILE/GIT_OBJECT_DIRECTORY đều trong review-artifacts, không tạo commit/ref, original status rỗng.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### a17-whitelist-bo-roi-m8  [P2]  Whitelist được mở theo khối và từ khóa ngoài nghĩa vụ

CƠ CHẾ SINH LỚP: Phân loại theo dấu hiệu tồn tại thay vì đòi mọi nội dung được thêm thuộc một nhóm được phép; một dòng nhận diện hợp thức hóa phần còn lại.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| W2 | probes/do_a17.py:80–86 | Cùng câu mô tả màu vô hại: đứng riêng False, kề khối A2 True, bản thân xep=None. |
| W3 | probes/do_a17.py:21–25, xep | Câu mô tả màu có từ vá lẻ: có hai từ mới thì True, bỏ hai từ mới thì False; không mô tả nghĩa vụ BẢNG LỚP. |

VẤN ĐỀ: A17 cấm cả dòng vô hại ngoài ba nhóm. Vì vậy không cần payload phủ định để chứng minh nới. Ba fixture cũ vẫn đỏ chỉ giữ ba điểm kiểm, không giữ tập chấp nhận. Không đếm riêng M8 đảo ô: A17 có thể phân nhóm đúng trong khi M8 sai nội dung.

ĐÃ THỬ VÁ: Không nới whitelist thêm. Cần audit từng câu/ô với nguồn nhóm và giữ ranh giới hunk, cho phép continuation chỉ khi cùng mệnh đề; chạy đối chứng ngoài nhóm ở trong lẫn ngoài đoạn. Đây là mô tả hướng, không áp patch vào skill.

ĐÃ THỬ NGHIỆM: `review4.py H1`; `do_a17.py` ba fixture vẫn ĐỎ. H1 dùng dữ liệu vô hại, không tự soạn chỉ thị tấn công.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### dem-dot-bien-khong-theo-tieu-chi-dich  [P2]  Thiếu kết quả không đích vẫn được cấp tín dụng

CƠ CHẾ SINH LỚP: Luật cấp tín dụng kiểm giá trị các kết quả đã trả về nhưng không kiểm sự có mặt của toàn bộ kết quả phải có. all trên tập rỗng là True.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| T2 | probes/dotbien.py:89–92 | Oracle trả hai DAT trên gốc, chỉ target=DO trên mỗi mutant: khac={},9/9 GIET THAT,rc0. |

VẤN ĐỀ: A18 bước3 buộc kiểm không đích đúng kỳ vọng. Không có quan sát không đích không tương đương DAT. Đây là biến thể mới cùng cơ chế cấp tín dụng thiếu bằng chứng; không đổi slug dù luật rc!=0 cũ đã được bỏ.

ĐÃ THỬ VÁ: Bản sao kiểm set(khac) bằng đúng tập tiêu chí trừ đích trước all: missing-nontarget rc1/0of9, oracle thật vẫn rc0/9of9. Không commit hay sửa probe được cấp.

ĐÃ THỬ NGHIỆM: `review4.py H3`; `controls4.py`; log giữ từng biến thể. A2_stub/both-red/always-red bị từ chối là kết quả sạch được giữ.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### bo-doc-bang-vuot-ranh-gioi-muc  [P2]  Đường đọc bảng đơn vị vẫn tắt khóa section

CƠ CHẾ SINH LỚP: Tìm marker trên toàn tài liệu và chủ động tắt guard ranh giới mục khi đọc bảng đơn vị, làm bảng của section khác bù cho bảng thiếu ở section đích.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| R2 | probes/do_a1a2.py:73 | Chèn ## Phụ lục trước bảng đơn vị: A2 vẫn True/ok; bảng không còn nằm trong BẢNG LỚP. |

VẤN ĐỀ: A20 yêu cầu cùng nguyên tắc cho cả hai bộ đọc. Đường A1 dừng đúng ## không bù được đường A2 tắt guard. Thể hiện R2 đã được lượt3 chỉ đúng mà chưa vá.

ĐÃ THỬ VÁ: Không sửa sản phẩm. Cần trích section BẢNG LỚP trước, chỉ parse bảng trong thân section; áp cardinality và phạm vi cho cả bảng chính lẫn đơn vị. Không chỉ đổi default bool.

ĐÃ THỬ NGHIỆM: `review4.py canonical`: A1 cross-heading=False; A2 unit-under-next-heading=True. Các ca canonical không cộng vào số hướng săn.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### bo-do-bang-chi-kiem-ten-khong-kiem-nghia  [P2]  Mất cấu trúc bảng và tái phát dò từ ở A19

CƠ CHẾ SINH LỚP: Chiếu tài liệu sang dict/substrings làm rơi số hàng, số cột, danh tính trường hoặc quan hệ khái niệm. Có tên không chứng minh đủ cấu trúc/nghĩa.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| N1 | probes/do_a1a2.py:A1 | Lặp sensitive thành bốn data rows: dict còn ba khóa, True. |
| N3 | probes/do_a1a2.py:A1 | Thêm cột vào routine vẫn True. |
| N4 | probes/do_a1a2.py:A2/doi | Bỏ so_p2/so_p3 khỏi hàng đơn vị, giữ so_p1: True. |
| N5 | probes/do_a1a2.py:A2/hd | Đổi hai tên cột đầu BẢNG LỚP thành alpha/beta: True. |
| N6 | probes/do_a1a2.py:A2/hang | Thêm cột vào findings_ids: True vì len>=2. |
| N7 | probes/do_a19.py:KIEM và vòng kiểm | Bốn section chỉ chứa bốn mảnh vocabulary, không có định nghĩa/hợp đồng: cả bốn predicate True. |

VẤN ĐỀ: Các ca đổi đơn vị được cấp nay bị giết thật; không nói bản vá không làm gì. Nhưng A20 cardinality áp cả hai bộ đọc, và A19 cấm chính phép có-chuỗi=khái-niệm. Giữ slug cũ vì cùng cơ chế, không tạo slug mới cho tái phát trong probe A19.

ĐÃ THỬ VÁ: Cần schema đóng: exact row/column count, không duplicate, đầy đủ so_p1/p2/p3, field→unit riêng. Với prose A19, kiểm mệnh đề/đoạn chứng minh lời hứa và đọc tay; không thêm vài keyword rồi khai đo nghĩa tổng quát.

ĐÃ THỬ NGHIỆM: `review4.py canonical`, H5 và H4. Bốn section protocol thật cũng đã được trích ra review-artifacts/section-*.md và đọc; chúng KHỚP lời hứa hiện tại.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### bien-nhan-thieu-so-ci-da-chi  [P2]  Lời hứa biên nhận lượt 4 chưa đóng được C1

CƠ CHẾ SINH LỚP: Không có khai consumption riêng ngân sách thì không phân biệt chưa chi với chưa ghi; schema v2 không cung cấp quan sát thay thế.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| C1 | cay-kho/ops/reviews/pr529-review-2-codex-verdict.receipt.yaml:191; nghĩa vụ A16' tương lai | Nợ lịch sử giữ nguyên. Receipt lượt4 không tồn tại trong cây/bundle tại lúc đo, nên chưa có hiện vật chứng minh cách xử mới. |

VẤN ĐỀ: Không phán receipt chưa tạo là một receipt sai schema, không bịa thể hiện mới của tương lai. C1 vẫn mở để truy vết. A16 r5 có hiệu lực từ lượt4; không hồi tố buộc sửa lượt1–2.

ĐÃ THỬ VÁ: Không sửa receipt bất biến. Khi nhận receipt4, kiểm ngân sách, số thực chi, danh sách run CI và bằng chứng; rỗng sau đo không chi, KHONG_DO_DUOC khi không biết. Không suy consumption từ số N.

ĐÃ THỬ NGHIỆM: `review4.py H8`, canonical; bien_nhan_v2 rc0/170 receipts vẫn không có receipt4.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### phep-do-doctrine-khong-du-rang  [P2]  Hai nhánh sao chép bắt buộc vẫn qua scanner

CƠ CHẾ SINH LỚP: Danh sách cụm cấm phân biệt cách viết, không bao phủ nghĩa vụ không sao chép doctrine; xanh ở danh sách không là xanh của nghiệm thu rộng.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| D1 | packet_loop.py:FORBIDDEN_DOCTRINE_PHRASES; A7/A13 kế thừa | Chép nguyên câu trần canon từ ADR-0043 vào cross skill bản sao:rc0. |
| D2 | cùng scanner; A7/A13 kế thừa | Chép nguyên §5.1 vào cross skill bản sao:rc0. |

VẤN ĐỀ: Gốc0 và §12 đỏ6 cho thấy scanner có chạy và có độ nhạy ở một phần miền. Hai ca phải đỏ khác vẫn sống. Lời khai nợ trong skill nay đúng nhưng không sửa cơ chế; S4 giữ lớp mở.

ĐÃ THỬ VÁ: Không sửa packet_loop.py ngoài write set. Điều phối quyết phạm vi/acceptance hoặc packet kế nhiệm; không coi khai nháp/nợ là bản vá.

ĐÃ THỬ NGHIỆM: `gates4.py`; scanner-base/adr/5.1/12.log cho0/0/0/6; finally phục hồi byte bản sao.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### doi-chung-a19-khong-chi-phoi-ket-luan  [P2]  Đối chứng A19 chỉ in, không làm tiêu chí đỏ

CƠ CHẾ SINH LỚP: Kết quả đối chứng được tính và hiển thị nhưng không được nối vào biến tổng hợp quyết định exit. Đây khác với dò nghĩa thiếu trong N7: dù control đã thấy sai, tiến trình vẫn xanh.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| C19 | probes/do_a19.py:64–66 | Bản sao buộc gia=True để mô phỏng control thất bại: in LA? nhưng rc0. |

VẤN ĐỀ: Một đối chứng mà hỏng không thể làm runner đỏ không bảo vệ lời khai A19 đạt. Ca supplied gốc False là đúng quan sát, nhưng không chứng minh chốt control có răng.

ĐÃ THỬ VÁ: Trên bản sao nối gia vào exit condition: cùng failure đổi rc0→rc1. Cần có cả positive baseline và negative control trong kết luận, không chỉ log.

ĐÃ THỬ NGHIỆM: `review4.py H4`; `controls4.py`: candidate control failure rc1. Tệp probes gốc nguyên byte.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

### dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi  [P2]  Spec đóng băng còn hai chỉ thị trái sửa đổi r5

CƠ CHẾ SINH LỚP: Sửa acceptance tại một mục nhưng giữ câu quy phạm cũ ở mục khác cùng spec; hai người đọc cùng revision có thể nhận hai nghĩa vụ loại trừ nhau.

BẢNG THỂ HIỆN:

| id | vị trí | bằng chứng |
|---|---|---|
| S9a | SPEC.md:96–97 so với A9' | Đoạn review_class vẫn gọi tổng hai khoảng là Phép đếm đúng, trong khi A9' chỉ cho một phép đo. |
| S15a | SPEC.md:170 so với ngoại phạm vi9/A19 | A2' vẫn cho phép trỏ §8/§12 cho định nghĩa P1/P2/P3, trong khi r5 cấm con trỏ sai và đòi bỏ nó. |

VẤN ĐỀ: Các câu này không được đánh dấu đã rút/hồ sơ. Có thể suy ưu tiên điều mới của r5 để thi hành, nhưng đó không sửa văn bản đóng băng mâu thuẫn, nhất là khi packet đang yêu cầu kiểm chính tiêu chí executor tự viết. Lớp này ở SPEC; không phủ nhận bản vá pointer trong kho đã đúng.

ĐÃ THỬ VÁ: Không sửa SPEC.md có băm. Điều phối cần revision/lease phù hợp và rà mọi chỗ dẫn xuất cũ, gồm S2 trong lease còn mô tả trước+sau merge. Không chỉ vá một câu rồi bỏ chỗ chiếu khác.

ĐÃ THỬ NGHIỆM: `review4.py H7` in cả hai cặp chỉ thị; hash vẫn khớp lease chứng minh không phải đọc nhầm revision. Đây là lý do blocked theo protocol §3.2, không chỉ changes_requested.

ĐỘ TIN: cao đối với cơ chế/quan sát cục bộ; không suy authority, CI thực chi hoặc hành vi executor ngoài sandbox.

## BẢNG LỚP

| lop_loi | các slug thuộc lớp | bản vá theo lớp hoặc lý do vá lẻ |
|---|---|---|
| `a9-bo-sot-delta-trong-merge` | `a9-bo-sot-delta-trong-merge` | Không sửa spec/lease. Điều phối cần thống nhất phép liệt kê phạm vi toàn diff và tập hai tên exact; giữ phép đếm endpoint đã được chọn, kèm phản chứng qua chính collector. S10 yêu cầu báo, không tự đổi acceptance. |
| `a17-whitelist-bo-roi-m8` | `a17-whitelist-bo-roi-m8` | Không nới whitelist thêm. Cần audit từng câu/ô với nguồn nhóm và giữ ranh giới hunk, cho phép continuation chỉ khi cùng mệnh đề; chạy đối chứng ngoài nhóm ở trong lẫn ngoài đoạn. Đây là mô tả hướng, không áp patch vào skill. |
| `dem-dot-bien-khong-theo-tieu-chi-dich` | `dem-dot-bien-khong-theo-tieu-chi-dich` | Bản sao kiểm set(khac) bằng đúng tập tiêu chí trừ đích trước all: missing-nontarget rc1/0of9, oracle thật vẫn rc0/9of9. Không commit hay sửa probe được cấp. |
| `bo-doc-bang-vuot-ranh-gioi-muc` | `bo-doc-bang-vuot-ranh-gioi-muc` | Không sửa sản phẩm. Cần trích section BẢNG LỚP trước, chỉ parse bảng trong thân section; áp cardinality và phạm vi cho cả bảng chính lẫn đơn vị. Không chỉ đổi default bool. |
| `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` | `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` | Cần schema đóng: exact row/column count, không duplicate, đầy đủ so_p1/p2/p3, field→unit riêng. Với prose A19, kiểm mệnh đề/đoạn chứng minh lời hứa và đọc tay; không thêm vài keyword rồi khai đo nghĩa tổng quát. |
| `bien-nhan-thieu-so-ci-da-chi` | `bien-nhan-thieu-so-ci-da-chi` | Không sửa receipt bất biến. Khi nhận receipt4, kiểm ngân sách, số thực chi, danh sách run CI và bằng chứng; rỗng sau đo không chi, KHONG_DO_DUOC khi không biết. Không suy consumption từ số N. |
| `phep-do-doctrine-khong-du-rang` | `phep-do-doctrine-khong-du-rang` | Không sửa packet_loop.py ngoài write set. Điều phối quyết phạm vi/acceptance hoặc packet kế nhiệm; không coi khai nháp/nợ là bản vá. |
| `doi-chung-a19-khong-chi-phoi-ket-luan` | `doi-chung-a19-khong-chi-phoi-ket-luan` | Trên bản sao nối gia vào exit condition: cùng failure đổi rc0→rc1. Cần có cả positive baseline và negative control trong kết luận, không chỉ log. |
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | Không sửa SPEC.md có băm. Điều phối cần revision/lease phù hợp và rà mọi chỗ dẫn xuất cũ, gồm S2 trong lease còn mô tả trước+sau merge. Không chỉ vá một câu rồi bỏ chỗ chiếu khác. |

findings_ids: [a9-bo-sot-delta-trong-merge, a17-whitelist-bo-roi-m8, dem-dot-bien-khong-theo-tieu-chi-dich, bo-doc-bang-vuot-ranh-gioi-muc, bo-do-bang-chi-kiem-ten-khong-kiem-nghia, bien-nhan-thieu-so-ci-da-chi, phep-do-doctrine-khong-du-rang, doi-chung-a19-khong-chi-phoi-ket-luan, dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi]

Đếm hiện hành: **9 LỚP P2, 18 THỂ HIỆN**, 0 P1, 0 P3. Mỗi thể hiện ở đúng một lớp. Lớp con trỏ sản phẩm đã vá thật không nằm trong findings_ids; mâu thuẫn SPEC là cơ chế khác được chỉ rõ, không đổi slug lớp con trỏ. Các tái phát A9/A17/A18/A20 giữ slug canonical, không tách slug theo từng bản probe.

## TÍNH TOÀN VẸN VÀ BÀN GIAO

VERDICT.md được tạo trước khi chạy probe; mỗi hướng/cổng đã bồi thêm kết quả. Bản ghi tăng dần lưu tại `review-artifacts/VERDICT-incremental.md`; bản hiện tại là bản hoàn chỉnh đã biên tập, không để câu cuối treo. Log sơ bộ H7/H8 từng có kết quả False do mẫu tìm của reviewer thiếu dấu backtick/khác vị trí xuống dòng; đã sửa mẫu, chạy lại và lưu output True. Không dùng hai False ấy làm finding.

original_files=2123; changed_or_missing=[]; added=[]; git_status=''

Tất cả đột biến/ứng viên sửa probe ở `review-artifacts/`, temporary files dưới `review-artifacts/tmp` (probes supplied có file tạm trong `probes/` và tự xóa). Scratch index/objects là bản riêng; không tạo commit, không push, không gọi mạng/GitHub, không sửa cây đang review. Hai diff sản phẩm và spec/lease được giữ nguyên. Không chạy full CI hoặc lane Windows.

Reviewer: **OpenAI (`openai_codex`) / Codex service qua API**; vai reviewer khác nền executor Claude; công cụ shell sandbox; vận chuyển **machine**, tệp cục bộ. Không tự chứng thực model ID, launcher run ID hoặc danh tính tài khoản đăng PR mà runtime không cung cấp. Không có subagent/thông điệp gửi bên ngoài.

Không tra được: PR/Actions hiện tại, comment authority và thời điểm đăng, consumption CI thực, tập ref nguồn lúc clone, parity cổng phía nguồn, transcript, lease #521 có thể đã bị xóa, biên nhận lượt4 tương lai. Sự kiện GitHub trong EVIDENCE/LEASE là **nguồn thuật lại**. Không đo được không có nghĩa là xanh hoặc không xảy ra.

**`VERDICT.md` là nguồn có thẩm quyền; comment trên PR chỉ là bản chiếu.** Verdict cuối là **blocked** trên đúng SHA đầu tệp. Không approve head này hay một head tương lai. Điều phối cần xử lý S9/S10 và revision/lease cho thiếu sót đặc tả; phần ngoài write set giữ nợ có tên. Review đã kết thúc, hiện vật hoàn chỉnh.
