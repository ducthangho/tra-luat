---
verdict: blocked
reviewed_sha: 00ac525df3f874cb0034622983c8c64f3b5ffc0a
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

Không approve. **3 LỚP P2 / 8 THỂ HIỆN**: hai lớp bắt buộc đối chiếu vẫn mở; lớp `bien-nhan-thieu-so-ci-da-chi` có thể hiện xác nhận thêm trong receipt lượt 5 và ledger mới. Giữ slug lịch sử, không gọi lỗi cũ bằng tên mới. N6 chưa chứng thực được số **thực đã chi**; riêng điều đó đã chặn approve.

Review độc lập với executor; provider OpenAI/Codex, thực thi bằng công cụ shell trong sandbox được giao. Không suy danh tính model/effort thực thi từ receipt cũ; không có header CLI/modelUsage của lượt này để xác thực model cụ thể. Không gọi mạng, push hoặc chạm kho thật. `cay/` giữ sạch; đột biến ở bộ nhớ và `review-artifacts/`. Các commit/tree thử chỉ nằm trong kho Git riêng của reviewer.

Đã tạo verdict trước phép đo đầu tiên, cập nhật sau từng phép. [Bản tăng dần](review-artifacts/VERDICT-incremental.md) giữ nhật ký đầy đủ; [script và JSON](review-artifacts/) cho phép chạy lại. Các lệnh dưới chạy từ gốc sandbox. Đây là bộ đọc văn bản có phạm vi đã khai và đối chứng, không phải chứng minh mọi agent tương lai sẽ tuân thủ.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Slug canonical | Phán duy nhất | Lệnh + output thật |
|---|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | **VÁ HỜ** | `python3 review-artifacts/probes.py canonical`: bốn mục `four_old_routes_closed` đều `true`; `remaining_live_old_references` còn SPEC:289–290, LEASE:123, LEASE:158. Hai dòng SPEC thuộc **một đoạn**, nên tổng **3 thể hiện** còn sống. |
| `phep-do-doctrine-khong-du-rang` | **CHƯA VÁ** | Cùng lệnh: scanner gốc `rc=0`; chép ADR `rc=0`; chép §5.1 `rc=0`; chép §12 `rc=6`. `S4` vẫn cấm packet vá scanner. |

**Bốn đường executor khai đã đóng có thật:** câu công thức vận hành ở mục `review_class` đã bỏ; danh sách dừng gen 6 có S9′/S10′/S11′ mới; không kế thừa công thức S2 gen 3; S8 gen 3 được rút rõ. H2/H4 kiểm thêm nội dung, không chỉ tên điều kiện.

**Có đường thứ năm:** `SPEC.md:287–291`, mục `chua_do_duoc` số 5, vẫn nói “A18 biến giả định ấy thành phép đo cho packet này” và đưa điều kiện “nếu A18 cho thấy…”. Nó chưa được chuyển sang nghĩa vụ/phép đo reviewer. Hai đường khác ở lease: `base_sha_ghi_chu:123–125` lấy A17 làm căn cứ vận hành; `recorder_xung_dot_loi_ich:158–160` còn nói A18 **buộc BẢY** phép chạy. Đây là cùng cơ chế để phần giải thích cũ tiếp tục cấp nghĩa vụ sau khi rút tiêu chí, không phải ba lớp mới.

Không dùng `S4` để miễn finding scanner, cũng không yêu cầu executor vi phạm `S4`. Cách xử lý cần quyết định chủ kho ngoài write set hiện tại.

## NGHĨA VỤ N1–N8

| Nghĩa vụ | Kết quả | Thước reviewer, lệnh + output thật |
|---|---|---|
| N1 | **ĐẠT** | `python3 review-artifacts/measure.py N1`: adapter gốc `{A1:true,A2:true}`; **8/8** đột biến đỏ đúng đích, không-đích vẫn true. Oracle đích luôn đạt / mọi tiêu chí đỏ / thiếu không-đích / sai đích / số nguyên thay bool đều **0/8** tín dụng; oracle đúng **8/8**. |
| N2 | **ĐẠT** | `python3 review-artifacts/measure.py N2`: 63 ô/dòng không rỗng có bản kê (kể cả Markdown cấu trúc), nhóm M8=17, A1=14, A2=32; xóa dòng gốc=0. Gốc true; câu vô hại riêng/kề khối/chứa từ khóa đều false. M8 gốc true, tráo ghép ô false dù vẫn cùng nhóm. |
| N3 | **ĐẠT** | `python3 review-artifacts/measure.py N3` và `python3 review-artifacts/probes.py delta_actual`: **15 đường** toàn diff; hai skill **62+139=201** dòng thêm. Hai đường tooling khớp blob master `d706abd`; không bỏ im lặng. Cây thật extra/tên sai/301 dòng/đổi blob tooling đều `accept=false`; gốc true. |
| N4 | **ĐẠT** | `python3 review-artifacts/measure.py N4`: `controls_observed=[true,true]`, kết luận gốc true; ép dương hỏng / âm hỏng / thiếu controls / thiếu results đều false. |
| N5 | **ĐẠT** | `python3 review-artifacts/probes.py N5`: đủ thân §3.2/5/8/12/13/20; mọi witness true. Đối chứng sai đích false, reflow true. §8 có P1, không P2/P3; §12 không cả ba; nợ severity có mặt. |
| N6 | **KHÔNG ĐO ĐƯỢC** | `python3 review-artifacts/measure.py N6`: chỉ 29 record, đủ 29 ID duy nhất; phân bố event 10/10/9, workflow 10/10/9 khớp. Không có raw toàn kho/dispatch. Lease đầu 08:15Z; cửa sổ 10:41:10Z; mốc ledger chọn 14:32:59Z. Receipt4 có ba trường; receipt5 vắng cả ba. `python3 review-artifacts/ci_controls.py ci_controls`: receipt4_shape=true; bỏ số chi / số chi không có ID / thiếu đầu hoặc đuôi cửa sổ đều false. |
| N7 | **ĐẠT** | `python3 review-artifacts/measure.py N7`: `missing_text_prevents_measurement=[]`. Dựng được thước cho cả sáu nghĩa vụ; N6 thiếu dữ kiện, không thiếu cách hiểu nghĩa vụ. |
| N8 | **ĐẠT** | `python3 review-artifacts/measure.py N8`: đủ sáu mục ĐẠT→true; N6 không đo được→false; thiếu N6→false. Verdict thực tế `blocked`; không tính N6 vào ĐẠT. |

**N1/N2/N4 — thẩm quyền và giới hạn:** reviewer tự viết bộ chấm. A1 đo ba quan hệ class→dừng; A2 đo bảng lớp, bảng đơn vị và nghĩa vụ bên đọc. Phép chấm đòi chính xác tập quan sát, kiểu bool, đích false và mọi không-đích true. Các đột biến gồm thay/gỡ bảng, gộp hàng, gỡ cột sửa lớp, gỡ đơn vị, gỡ nghĩa vụ một lớp, thay mục bằng con trỏ, bỏ nghĩa vụ đọc trước khi sửa.

N2 không lấy từ khóa hoặc hàng đầu đoạn để hợp thức hóa phần còn lại. [Bản kê](review-artifacts/N2-unit-manifest.json) lưu từng ô và từng dòng nối câu để đọc lại. Reviewer đã đọc nghĩa: M8 gồm hai nguyên nhân head đổi, hai hành động tương ứng, lệnh đo base và hai giới hạn; A1 gồm ba hàng và phân biệt approve; A2 gồm trách nhiệm phân lớp, sửa lớp, đơn vị, giữ slug, nợ severity và chống cắt tiêu chí. Replay exact đơn vị chỉ giữ bản đã audit; **không dùng việc tự khớp bản gốc làm bằng chứng ngữ nghĩa**. Khác cách diễn đạt có thể bị từ chối bảo thủ và cần đọc lại. Kiểm ghép ô M8 riêng chứng minh việc khai giới hạn phân nhóm không miễn nội dung M8.

**N3 — không giấu delta master:** EVIDENCE chỉ tóm hai nhóm skill/review; numstat đầy đủ còn `.claude/dev/chon_reviewer.py` +1/−1 và `chon_reviewer_test.py` +49/−4. Reviewer liệt kê cả hai, so blob với `d706abd` và xác nhận đúng phần master merge vào. Không gọi đó là executor tự viết ngoài phạm vi. Trần sản phẩm vẫn 201/300. Phép cây thật còn thử sửa chính một đường tooling đã được xác nhận: blob không còn khớp master thì bị từ chối; không có whitelist theo tên vĩnh viễn. Resolution tổng hợp 301 dòng là tree thử, không tự nhận đã xác định ai viết từng dòng trong merge thật. Nợ endpoint không tách tác giả/thời điểm vẫn còn.

**N5 — đã đọc quan hệ, không chỉ tìm từ:** §3.2 khai trục review_class và revision; §5 chứa write set/đổi phạm vi; §8 chứa assurance và approval neo SHA; §12 chứa stop, giữ finding IDs và xem lại cách làm; §13 chứa trigger/verdict/hoàn tất; §20 có đúng các hàng ADR và giới hạn cổng. Phần thêm không còn hứa §8/§12 định nghĩa severity. Không coi token search là chứng minh toàn kho không có cách diễn đạt tương đương.

**N6 — chấm chính ledger được nộp:**

- **Mốc mở sai loại sự kiện.** `git show -s --format='%H %aI %cI %s' 2c466ac` cho commit thi công r2 lúc `14:32:59Z`. Lease gen 1 từ blob mirror ghi **08:15:00Z**. Không cần biết chính xác Issue mở phút nào cũng đủ bác việc coi 14:32:59Z là lúc packet bắt đầu. Packet đã tồn tại **không muộn hơn 08:15Z**. Đầu cửa sổ ledger bỏ ít nhất **2 giờ 26 phút 10 giây** từ mốc đã biết đó. Mốc Issue mở chính xác chưa có raw để xác thực.
- **Có kê cả sáu workflow, chưa có bằng chứng phủ cả sáu.** Inventory khớp tree. Nhưng JSON chỉ có các record của ba workflow đã được chọn là thuộc packet. Danh sách ba workflow “chưa từng chạy” là kết luận sau lọc, không phải raw cho phép kiểm việc lọc có bỏ sót hay không. Không có `head_branch` trong 29 record để kiểm lại nhánh; ánh xạ `head_sha`/PR đã được chuẩn hóa từ trước.
- **Đếm event từng record là hướng đúng khi bộ lọc không đáng tin, nhưng raw cần thiết vắng.** Reviewer tái đếm được 0 dispatch **trong 29 record được cung cấp**. Không tái đếm được 0/127 toàn kho hoặc kiểm thứ tự/phân trang của 212 record; phương pháp nói hai trang ×100 mà tổng lại 212, chưa có lời giải thích tập hợp/khử trùng. Tính giảm dần trong tập đã lấy không tự chứng minh không có trang bị bỏ hay dữ liệu dịch giữa các lần lấy.
- **Thí nghiệm bộ lọc vẫn là thuật lại.** Không có nguyên request/response cho branch, workflow_id, event tại 21:25:14Z/21:43:38Z/21:44:07Z; cũng không có 100 record dispatch riêng. Vì vậy chưa kiểm được “100/100 đúng event” hay giả thuyết minimal_output. Ngay nếu thuật lại đúng, hai lần đều bỏ lọc chỉ bác cách giải thích đơn giản “đổi mỗi cờ này là đủ chữa”; chưa xác định nguyên nhân dịch vụ biến động theo thời gian. Reviewer không thay bằng một giả thuyết mới.
- **Thiếu dữ kiện phân biệt loại chi.** N6 đo CI loại (b) thực dùng làm nhạc cụ đo; adapter xếp `workflow_dispatch` vào ví dụ loại (c). Không có dispatch chưa phải là phép đồng nhất mọi loại chi với 0. Không có jobs/lane hoặc `run_attempt` trong cả 29 record. Workflow trong cây có dùng `github.run_attempt` và `run_attempt` ở artifact/job receipt, nên lịch sử attempt là một chiều dữ kiện thực sự cần đối chiếu; gói hiện tại không cho phân biệt các lần chạy lại hoặc chứng minh lane nào đã chạy. Không cáo buộc đã có chạy tay hay lane Windows.
- **Đuôi cửa sổ cũng chưa chứng thực:** metadata kết thúc `21:42:48Z`, đo lúc `21:45:27Z`. Có thể 21:42:48Z chỉ là timestamp run mới nhất, không phải lúc ngừng bao phủ. Muốn dùng cách hiểu đó phải có response chụp/phân trang và mốc as-of; gói chưa có. Không tự kết luận đã xảy ra một run trong khoảng trống này.
- **“Thứ còn lại trong lịch sử” không bằng “mọi lượt đã chi”.** Một run bị xóa hoặc lần thực thi không nằm trong bản chiếu vẫn có thể đã tiêu lượt. Ledger tự khai giới hạn xóa run là đúng; dùng lời khai ấy rồi vẫn kết luận “trọn vòng đời/mọi head/chưa từng một lần” là miễn nghĩa vụ. Ledger hiện chỉ chứng minh các phép đếm trên **tập 29 record đã nộp**, không chứng minh tổng tiêu hao bằng 0. Số phút billable không phải đơn vị N6; thiếu phút **không phải** lý do chính để chặn N6.

Các mục KHONG_DO_DUOC đã khai (phút, 185 run cũ, run bị xóa, conclusion vắng) **chưa đủ**: còn mốc packet sai, raw toàn kho/dispatch và thí nghiệm bộ lọc vắng, thiếu provenance của phân trang/chọn record, thiếu attempt/jobs, đuôi as-of chưa rõ, và receipt5 thiếu trường. Kết luận 185 run cũ “không ảnh hưởng” cũng chưa được reviewer tái lập vì 100 record và cơ sở thứ tự chưa có.

N6 toàn nghĩa vụ giữ **KHÔNG ĐO ĐƯỢC** theo chỉ thị lượt này. Điều đó không che subcheck đã **KHÔNG ĐẠT**: receipt5 thiếu trường trực tiếp nhìn thấy được. Không dùng schema receipt xanh để thay N6.

## BẢNG SĂN

Sáu hướng dưới khác các hướng r4/r5 đã cấm lặp. Chúng đo thay đổi quy trình đóng băng, bảo toàn ràng buộc khi bỏ kế thừa, cách biểu diễn số mục, parity hai bản stop, quan hệ thay thế lease và độ trung thực của delta revision. Không tính đột biến canonical hoặc phép N1–N8 thành hướng săn mới.

| Hướng độc lập | Lệnh | Output thật | Phán |
|---|---|---|---|
| H1 — S12′ là bắt buộc hay lời khuyên; có cổng đọc không | `PYTHONDONTWRITEBYTECODE=1 python3 review-artifacts/hunt.py H1` | `normative_S12_valid=true`; đổi DỪNG thành cân nhắc→false; `gate_mentions_S12=false`, `gate_reads_dieu_kien_dung=false`; trace trước freeze không có | S12′ có răng **ở nghĩa vụ đọc**, không có cổng máy đã chứng minh. Không thấy yêu cầu phải viết cổng mới. Không đo được executor thật sự quét thế nào trước freeze; không tự phán vi phạm S12′ từ kết quả sót chữ. |
| H2 — bỏ kế thừa có mất ràng buộc cũ không | `PYTHONDONTWRITEBYTECODE=1 python3 review-artifacts/hunt.py H2` | S1/S3/S4/S5/S6 giữ đúng nội dung; in cặp S2/S7/S8 cũ–mới; `replacement_no_revert_constraint=true` | S2 đổi có chủ đích theo N3; S7 giữ hành động; bỏ S8 không miễn chống hoàn nguyên vì ngoại phạm vi7/N2 vẫn giữ. Không thấy ràng buộc bị mất do thao tác này. |
| H3 — khoảng trống S8 và S12 ngoài bullet có làm mất mục | `PYTHONDONTWRITEBYTECODE=1 python3 review-artifacts/hunt.py H3` | YAML=12 mục, SPEC=12 ID; active=11; S8 bia mộ=true; S12 đoạn riêng=true; không thấy reader của trường stop trong hai cổng kiểm | Không thấy lỗi thực thi do đánh số. Bộ đọc tự dựng chỉ lấy bullet sẽ bỏ S12, nhưng chưa có bằng chứng kho dùng bộ đọc như vậy; không biến giả thuyết thành finding. |
| H4 — parity **từng điều kiện** spec r7/lease gen6 | `PYTHONDONTWRITEBYTECODE=1 python3 review-artifacts/hunt.py H4` | Cả 12 cặp spec/lease true; đổi 300→400 hoặc xóa DỪNG của S10′→false | Khớp trigger/hệ quả sau đọc nghĩa. Đây không phải so byte hay chỉ kiểm ID; các khác biệt định dạng không tạo finding. |
| H5 — hai chiều thay thế gen5↔gen6 và chốt đọc blob | `PYTHONDONTWRITEBYTECODE=1 python3 review-artifacts/hunt.py H5` | new→old / old→new khớp; `_kiem_bia_mo`: gốc **rc0**, xóa backlink **rc8**, backlink sai **rc8** | Lời khai hai chiều đúng, cổng có đối chứng dương và âm. Cây fixture Git riêng, không sửa lease thật. |
| H6 — r7 có lén đổi nghĩa vụ khi khai “giữ NGUYÊN VĂN” | `PYTHONDONTWRITEBYTECODE=1 python3 review-artifacts/hunt.py H6` | N1–N8 byte_identical đều true; M16=true; generation6/revision7/write_set_count3 | Lời khai giữ nguyên đúng. Đo sự trung thực của revision delta, không thay kết quả chấm từng nghĩa vụ. |

H1/H3 có giới hạn được khai; không coi những phần chưa đo được là bằng chứng sạch tuyệt đối. Không phát hiện lớp mới từ sáu hướng này. Bỏ kế thừa không phải bước sai đã được chứng minh; sai là tuyên bố đã đóng cả cơ chế trong khi còn prose vận hành ngoài danh sách đó.

## BẢNG ĐO

| Đối tượng | Kỳ vọng | Đo thực tế | Khớp/lệch |
|---|---|---|---|
| SPEC đóng băng | băm được giao, 30 999 B | `sha256sum goi/SPEC.md` = `19a4380499b3e66ea1b641cbe59ad6ca6ecc1a48dd16b511c0dbef9feafb0b6d`; `wc -c`=30999 | **KHỚP** |
| Blob spec/lease trên mirror | đúng gói | `python3 review-artifacts/collect.py`: cả hai matches=true | **KHỚP** |
| SHA/cây/mirror | exact SHA, đủ lịch sử | SHA `00ac525…`; tree `9dd4ef368206773c6788ca6aa78339a6d5d7c889`; shallow=false;407 ref | **KHỚP** |
| Bốn đường luật cũ được nêu | được đóng cả bốn | canonical: 4 true | **KHỚP** |
| Lớp luật cũ đóng toàn bộ | không còn cấp nghĩa vụ qua A17/A18 cũ | 3 đoạn vận hành còn sống | **LỆCH** |
| N1/N4 | đích và controls quyết kết luận | oracle sai0/8; controls hỏng đều false | **KHỚP** |
| N2/M8 | từng ô thuộc nhóm, cặp nguyên nhân–hành động đúng | không xóa byte #521; M8 gốc true/tráo false | **KHỚP** |
| Delta toàn bộ | không lọc mất đường | 15 đường = 2 skill + 11 review + 2 tooling từ master | **KHỚP sau đối chiếu provenance**; EVIDENCE tóm thiếu nhóm tooling |
| Trần hai skill | ≤300 dòng | 201; tree thử301 bị bác | **KHỚP** |
| Con trỏ thêm | có đúng hợp đồng đích | 6 section/witness đầy đủ, nợ severity có khai | **KHỚP** |
| Scanner nhận copy doctrine | các đối chứng âm đỏ | ADR0, §5.1=0, §12=6 | **LỆCH**, hai phản chứng sống |
| Ledger inventory | cả6 workflow | danh sách khớp tree | **KHỚP inventory**, chưa khớp bằng chứng bao phủ |
| Ledger record đã nộp | số đếm khớp nội dung | 29 ID duy nhất; event10/10/9, workflow10/10/9 | **KHỚP** |
| Ledger toàn kho | tái đếm212/127 và dispatch0 | không có raw tương ứng | **KHÔNG ĐO ĐƯỢC** |
| Vòng đời packet | phủ từ lúc packet mở | lease08:15Z, cửa sổ10:41Z, mốc khai14:32Z | **LỆCH** |
| Receipt4 | tách ngân sách/số chi/run | 0 / 0 / [] | **KHỚP cấu trúc**, số0 chưa chứng thực |
| Receipt5 | cùng nghĩa vụ từ lượt4 trở đi | vắng cả ba trường | **LỆCH** |
| Stop/S8/S12/thay thế/revision | như lời khai executor | H1–H6 như trên | các phần khớp được kê, giới hạn không giấu |
| Executor nộp probe nghiệm thu | không có | EVIDENCE là rc cổng, delta và mô tả; không có probes; các ĐẠT trong receipt cũ là thuật kết quả reviewer cũ | **Không xác nhận vi phạm S11′ mới** |
| Gate văn bản sản phẩm | diff sạch whitespace | `git -C cay diff --check dc02c9b..00ac525 -- .claude/skills/`: rc0, stdout rỗng | **KHỚP** |
| ADR routing | số trên đĩa/bảng khớp | `python3 -B cay/.claude/dev/packet_loop.py adr-song --root cay`: rc0,48/48, có ngoại lệ0016 trong output | **KHỚP trong phạm vi cổng** |
| Cây review không đổi | sạch | `git -C cay status --porcelain`: rc0,rỗng; diff skill từ f89f07d đến head rỗng | **KHỚP** |

`git diff --check` toàn endpoint báo hai trailing whitespace trong **verdict lượt1 bất biến**, không ở sản phẩm; không yêu cầu sửa hiện vật đã giao. Không dùng một `git diff --check` working tree rỗng để chứng minh endpoint sạch. Không chạy lại full selftest/release-verify hoặc truy cập CI live trong lượt này; các số 1710/1710 và CI success trong EVIDENCE không được biến thành kết quả reviewer tự chạy.

## PHÁT HIỆN

| `lop_loi` / slug giữ nguyên | Hạng | Thể hiện | Bản vá theo lớp / lý do cần chủ kho |
|---|---|---:|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | P2 | 3 | Rà toàn bộ prose đang cấp nghĩa vụ, kể cả chú thích lease và mục nợ; chuyển mệnh đề hiện hành sang N1/N3/N4 hoặc đánh dấu lịch sử đã rút ngay tại chỗ. Spec đóng băng nên chủ kho quyết revision/hash/generation. |
| `phep-do-doctrine-khong-du-rang` | P2 | 2 | Sửa cơ chế nhận diện doctrine trong packet được cấp quyền riêng; giữ hai phản chứng sống và đối chứng §12. S4 không cho vá tại đây. |
| `bien-nhan-thieu-so-ci-da-chi` | P2 | 3 | Một đường báo cáo CI đầy đủ cho mọi receipt áp dụng: ngân sách, chi thực, run/attempt và provenance/cửa sổ. Sửa bằng bản bổ sung liên kết biên nhận cũ và ledger đủ dữ kiện; không sửa receipt đã giao. |

Hạng P2 dùng theo tiền lệ canonical của chính các lớp này; không tự bổ sung định nghĩa severity vào doctrine.

### `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi`

**Ba thể hiện:** (1) SPEC:287–291, A18 vẫn quyết phép đo và cách dừng; (2) LEASE:121–125, A17 vẫn làm căn cứ cho base; (3) LEASE:155–160, A18 còn buộc bảy ca như chốt xung đột lợi ích. Bảng rút ở chỗ khác và đoạn phân công mới phía sau không xóa câu vận hành, chính cơ chế lượt5 đã bác.

Trigger: đọc riêng mục nợ hoặc lời giải thích lease để quyết phải đo gì. Kết quả: nhận một tiêu chí đã rút, số ca do mô hình cũ đặt ra, hoặc điểm neo thước không còn hiện hành. Hướng sửa theo lớp ở bảng trên phải bảo toàn nội dung nghĩa vụ, không xóa lịch sử vô tội vạ. Test khóa: trích từng đoạn quy phạm đang hoạt động và kiểm mục tiêu/đối tượng thẩm quyền hiện hành; đối chứng giữ nguyên trích dẫn lịch sử có nhãn đã rút. Rủi ro của sửa bằng regex toàn tệp là xóa hồ sơ lịch sử hoặc đổi nghĩa vụ đóng băng.

### `phep-do-doctrine-khong-du-rang`

**Hai thể hiện:** copy dòng `ADR-0043:5` dài101 ký tự; copy §5.1 dài2501 ký tự gồm heading, đều vào cross-review skill trên scan-tree. Gốc7 tệp sạch rc0; từng copy rc0; §12 rc6. [Các log](review-artifacts/canonical-baseline.log), [ADR](review-artifacts/canonical-copy_adr.log), [§5.1](review-artifacts/canonical-copy_5_1.log), [§12](review-artifacts/canonical-copy_12.log) ghi lệnh đầy đủ và mã thoát trực tiếp.

Giới hạn scanner được adapter khai đúng nhưng cơ chế chưa đổi. Không chấp nhận “đã khai nợ” thành “đã vá”. Hướng sửa cần kiểm cả cách nhận diện và false positive; mở rộng danh sách vài cụm có thể tiếp tục bỏ lọt cách viết khác hoặc bắt oan tài liệu đang mô tả giới hạn. Quyền mở packet/scope thuộc chủ kho.

### `bien-nhan-thieu-so-ci-da-chi`

Giữ slug đã có từ các lượt trước; đây không phải slug thứ ba trong mục đối chiếu bắt buộc **hai lớp** lượt5, mà là lớp lịch sử có thể hiện hiện hành được đo lại.

**Ba thể hiện, không tách mỗi trường thành một lỗi:**

1. Receipt lượt5 `cay/ops/reviews/pr529-review-5-codex-verdict.receipt.yaml` thiếu nguyên khối ngân sách/số đã chi/run. Nghĩa vụ áp từ receipt4 **trở đi**, không chỉ receipt4. Thuật lại verdict N6 KHÔNG ĐO ĐƯỢC không thay số chi/trạng thái số chi của chính receipt5.
2. Ledger `pham_vi`/mục Phạm vi chọn commit thi công làm lúc mở packet và khai cửa sổ phủ trọn, trái lease08:15Z. Đây là **lời khai sai đo được**, không chỉ thiếu dữ kiện.
3. Ledger dùng các tổng hợp không có raw kèm để khẳng định số0 và “chưa từng chạy”, dù tự giới hạn là lịch sử còn lại. Gộp raw thiếu, provenance chọn tập thiếu và kết luận vượt tập quan sát vào **một thể hiện suy luận**; không đếm mỗi workflow hay mỗi trường thiếu thành một finding.

Test khóa: receipt4 làm đối chứng hình dạng; xóa số chi hoặc khai chi1 nhưng ID[] phải bị bác; cửa sổ thiếu đầu/đuôi phải bị bác; đối chiếu nguồn toàn lịch sử trước khi chấp nhận0. Sửa cần bản bổ sung có neo receipt cũ và mốc as-of; không sửa các byte receipt bất biến hay gán ngân sách0 làm consumption0. Rủi ro chính của vá hời hợt là thêm đủ ba khóa rồi vẫn giữ số0 không có chứng cứ.

## KHÔNG ĐO ĐƯỢC

Để đóng N6, cần bổ sung chính xác:

1. Metadata thô có mốc mở Issue/packet được cấp quyền; đối chiếu lease đầu **08:15Z**. Lấy lịch sử từ mốc mở thật, không chỉ từ commit/PR đầu tiên.
2. Request/response đầy đủ các trang run của toàn kho qua mốc as-of rõ ràng, gồm cả workflow không thấy chạy; timestamps lấy trang, thông tin pagination, ID để khử trùng, quy tắc gắn packet bằng nhánh/PR/head và lịch sử các nhánh/generation. Cung cấp raw100 dispatch và raw các phép thử bộ lọc nếu tiếp tục dùng chúng làm căn cứ. Giải thích tổng212 so với hai trang100.
3. Lịch sử attempts/jobs và căn cứ phân loại (a)/(b)/(c) cho các lần thực thi liên quan; chứng minh số **lượt loại(b)**, không chỉ số event dispatch. Số phút chỉ cần nếu muốn tuyên bố về chi phí phút.
4. Chứng cứ bền về độ đầy đủ của lịch sử thực thi, gồm việc xóa/mất run nếu có: sổ ghi contemporaneous hoặc audit có thể đối chiếu. Nếu chỉ có lịch sử còn lại thì giữ kết luận giới hạn và **KHÔNG ĐO ĐƯỢC** cho tổng thực đã chi; không dùng lời khai giới hạn để miễn N6.
5. Bản bổ sung cho receipt5 tách ngân sách và số chi, khai run IDs hoặc `KHONG_DO_DUOC` đúng dữ kiện, có liên kết bất biến đến receipt5. Do cấm sửa receipt cũ, cơ chế bổ sung phải được chủ kho/điều phối chấp thuận nếu hợp đồng hiện hành chưa có đường đó.

Ngoài N6: chưa đo hành vi thực sự trước freeze đối với S12′; chưa đo sự tuân thủ runtime của agent; chưa tái chạy CI live/full selftest; không chứng minh mô hình adapter tối thiểu đúng tổng quát. Không cần tự soạn payload nhạy cảm để hoàn thành các phép trên; không có phép thử kiểu đó được tự soạn trong lượt này. Nếu điều phối muốn đo đầu vào thoát cây hoặc biến thể tương tự, hãy dùng fixture sẵn có và trả raw kết quả; reviewer không cần tạo nội dung ấy.

**Sai sót thước của reviewer đã sửa công khai:** N5 lần đầu tìm nhầm heading `3.2. `; H5 lần đầu thiếu Git rồi thiếu ref chứa blob. Các output đó nằm trong nhật ký, được đánh dấu không dùng làm finding. N5 cuối mọi witness true; H5 cuối rc0/8/8. Các dòng lệnh tự ghi trong nhật ký cũ dùng tên measure.py chung cho probes/hunt; bảng lệnh trong verdict này và tên script thật là đường chạy đúng.

## KẾT LUẬN

**blocked**, không có approve tường minh. Bản sửa r7 đóng thật bốn đường đã nêu và giữ đúng nhiều ràng buộc; nó chưa đóng toàn bộ lớp văn bản vận hành cũ. Scanner vẫn còn hai phản chứng sống. Ledger mới cải thiện khả năng tái đếm tập record được nộp, nhưng không chứng thực toàn vòng đời hoặc số CI thực đã chi, và receipt5 còn thiếu khối nghĩa vụ.

Chủ kho cần quyết sửa đặc tả và đường xử lý scanner ngoài scope; executor/điều phối cần cung cấp dữ kiện N6 cùng bản bổ sung receipt hợp lệ. Không đổi slug, không nới nghĩa vụ để vừa bản vá, không sửa hiện vật đã giao.
