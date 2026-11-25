Review đặc tả wp1236 r10 bản sửa 1, vòng 6: **changes_requested** — **1 P2, 1 lớp mở**. V01 `VA_MOT_PHAN`; V02 `DA_VA_THAT`. Hội tụ vòng 5→6: **1/2**. Lịch sử lớp tái diễn và hai lớp mã r9 còn `VA_MOT_PHAN` được giữ trong JSON.

`reviewed_sha: 19fd74ac8a69c4912b5f9484630a607c5dd11184`  
`reviewed_tree: 3ed01155a390a06fe339573e710e2c338c44710e`  
`spec_sha256: 2a1e3cb870c20491af3efb7efdd900f0d372c01a78411e80087ff231999a884e`

| Finding | Kết luận và bằng chứng |
|---|---|
| **W01 · P2** — `nghiem-thu-khong-co-lap-chot-dich` | Resume chỉ khoá theo ID. Đưa nguồn gốc lành (native **36/36**) vào ID từng bị giết vẫn báo **GIẾT 1/1** từ kết quả cũ, hash không khớp. Test vắng: child rc1 nhưng tool rc0 và `SONG_SACH 1`. Thiếu baseline/marker hoàn tất và ledger ca đích. [Phép đo](runner_audit.json); scanner:227–278. |

Phần sửa đã được xác nhận bằng phép đo:

- **800 mutant**, sinh hai lần **giống hệt byte**; **127/127** cặp áp được và khớp băm nguồn tái dựng từ các generator ma6. Năm raw JSONL cũ không có trong bundle này; không nhận đã đọc chúng.
- Toàn bộ **927 ID/hash** khớp pilot. Chạy lại **66** mẫu có chủ đích: **22 GIẾT / 34 sống sạch / 10 lỗi vô can**, khớp từng kết quả. Có đủ **25/25** survivor không tương đương và **9** tương đương. Chạy riêng **22/22** ca giết không cache YAML: rc3 với đúng `DO:<ca>`. Không nhận đã chạy lại toàn bộ927. [Đối chiếu](pilot_comparison.json).
- Luật4 route đúng: `kiem_ho_so` chỉ `head=None`; `head!=None` qua helper A và D2b C. Đây là sửa hợp đồng có thật. Harness B/C hiện dùng giao thức khác runner; các test mới phải nối adapter trong write set và chứng minh đúng module/consumer khi review mã B/C. Chưa có test mới nên không lấy khác biệt của harness cũ làm finding P2 riêng về đặc tả.
- V02: **30 ca A, 5 luật, 3 finding mã / 2 lớp**; **1324 dòng / 3 tệp** thuộc r9. Census chạy lại trùng byte bản ghim: **66=47/10/9**, **170=25/56/39/50**, **50 script=20/28/2**. [Số đo](reference_census.json).

Luật5 giữ được hồi quy cũ, nhưng **97/127 neo là cả tệp**. Bản chỉ đổi định dạng, giữ nguyên AST, cho **124 KHONG_AP_DUNG**; điều đó không xoá124 nghĩa vụ. Cần ledger ID/invariant → replacement/ca đích hoặc chứng minh tương đương, được kiểm trên head mới. [Phép đo](regression_portability.json). Không dùng danh sách tương đương của head cũ hoặc lỗi vô can làm miễn tự động.

Có phép biến đổi lượt6 mà generator không sinh: bỏ đệ quy chọn lọc dưới metadata, `head is not None` thành truthiness, đổi nhãn bộ sinh trong dict module, đổi thứ tự qua `try`. Chúng vẫn có trong kho127. `h2` thêm `~them~` vào TOKEN là tương đương vì regex không thể trả giá trị ấy; không thay cho ca `pass`. Audit đủ24 mã nằm trong JSON; có hai mô tả cần làm rõ: `a2` còn xoá điều kiện comprehension; `i5` trong lớp ký tự tạo dấu chấm literal, không phải wildcard.

**1700 là đề nghị, chưa là khả năng đã đo hay quyền đã cấp.** Nền1324 và số mutant có phép đo; +200–300 dòng để đóng lớp chỉ là ước lượng. 34 bản sống của kho đã nằm trong153 sống sạch, không phải34 nghĩa vụ bổ sung độc lập. Phải đo numstat r10 thực trước review mã; không land A1 chưa đạt luật3 rồi coi A2 là phần sửa sau.

Hướng sửa chung cho W01: neo run bằng hash nguồn/test/manifest, kiểm baseline/completion và tín dụng đúng ca. Khi thi công, giữ ledger hồi quy qua đổi head và kiểm adapter từng consumer. **Chưa kết luận E1**, vì các phần tái lập đã có bằng chứng và hướng sửa còn có ca đóng hữu hạn; **cách hiện tại vẫn chưa đủ để công nhận đóng lớp**. Checkpoint §12 về lớp lặp phải giữ, không tiếp tục chỉ thêm từng ca survivor.

Provider/surface/transport: `openai_codex / codex_cli / machine`, run `8157832c863a4be0910f08b0d051f9d7` theo launcher run.json; model/effort phục vụ `KHONG_DO_DUOC`. Chỉ review offline đặc tả; không mạng, không sửa/commit/push hai kho, không chứng nhận code r10/Windows/CI/merge. JSON có15 dòng lịch sử lớp và bảng nối alias.

Đối chứng resume bổ sung dùng manifest sinh thật từ thay đổi chỉ ở docstring: **800 ID giữ nguyên / 800 hash thay đổi**, tool vẫn nhận một kết quả cũ sai hash. [Bằng chứng](resume_real_manifest.json).

Snapshot cuối: repo **17.387** tệp, mã r9 **17.333** tệp, **0 delta** nội dung/mode/HEAD/tree/index/status so đầu. Validator rc0: **`HOP_LE (§8.3): 1 finding, 1 lop`** ([kết quả](kiem_verdict.txt)).

KET_LUAN: changes_requested
