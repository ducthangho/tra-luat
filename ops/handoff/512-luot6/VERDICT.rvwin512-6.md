verdict: changes_requested
reviewed_sha: 353eae10120da2a1788dcaf7a906fe46261bd71b
reviewed_base: 015ffcc09d76fbc9cdfbc3d2ee0735c3ead8d364
reviewed_files_sha256:
  ops/lease_publish_test.py: 8bcc22934e5d1eca808674cd8d9ecbc88a01bcbfd5bda7fdb6cd5478757635ea
  ops/chay_lease_publish_test.sh: 87c760294763c71a67cfaee50a440e62b31c439beb0abbfcb5e34076d32be693
model_tu_khai: GPT-6 / Codex; khác họ Claude Opus 5 của tác giả theo EVIDENCE.md; không xác minh backend độc lập
review_round: 6
so_p1: 3
so_p2: 0
so_p3: 0
so_the_hien: 5
hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0
previous_hint_sha256: 9087726521c621617de5dc9fc40eab5e0f302f928662d23a8c62d47e81b47cdc

**changes_requested — ba lớp F2/F6/F7 còn thiếu răng, tổng năm thể hiện.** Bản kết luận dùng các phép đo đã lưu trước những lần gián đoạn hạ tầng; các phần không hoàn tất được khai riêng. Không xem việc container chết là lỗi của PR. Không có quyền nâng trần hoặc quyết định merge được suy từ review này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp | Trạng thái canonical tại HEAD | Căn cứ đã đo |
|---|---|---|
| F1 thu hồi cây | ĐÃ VÁ THẬT | Retry cũ đã xoá; consumer thật với hạn 0.5s thu hồi hai cháu, nhịp 13→13 và 12→12; catalogue t154 bắt PID-only, mất session và mất guard |
| F2 bằng chứng sống | VÁ HỜ | Retry giữ kín log cũ đã xoá; nhưng N10 ngắt tee tại t125 sống ở t158 và full wrapper 155/155. HEAD thật vẫn tee đúng |
| F3 selector rỗng/không khớp | ĐÃ VÁ THẬT | Catalogue bỏ guard bị t155 giết đúng chốt; wrapper thật đủ 155 tên |
| F4 ngân sách tổng | ĐÃ VÁ THẬT | Không còn vòng retry nhận hạn mới; catalogue các nhánh ngân sách chết đúng chốt. N12 có thể tái sinh đường ấy được tính vào F7 wiring, không đếm lặp ở F1/F4 |
| F5 tắt đệm con | ĐÃ VÁ THẬT | Hai môi trường thực có PYTHONUNBUFFERED=1; M14 chết tại t158 |
| F6 công cụ/hồ sơ bằng chứng | VÁ HỜ | Neo log và bảng S2 khớp; catalogue lại cấp tín dụng GIẾT THẬT cho Exception vô can (control RuntimeError bị loại đúng) |
| F7 classifier/consumer/phản chứng | VÁ HỜ | Nhãn chưa rõ giữ dấu lỗi; M15/M16/M17 chết thật. N01/N02 đảo nhãn, N17/N18 bỏ mẫu số và N12 hồi sinh retry qua Popen còn sống |

| Thể hiện lượt 5 | Đối chiếu độc lập đã lưu |
|---|---|
| F1.4 | Đã xoá đường retry không nhóm; behavior.json: hai lượt A/B qua helper; timeout thật làm cả hai cháu ngừng nhịp |
| F2.2 | Đã xoá đường retry không tee; behavior.json: nhánh lệch giữ lý do S8 và seam trong log [B], đúng bốn tee; không run/Popen phụ |
| F4.4 | Đã xoá vòng nhân ngân sách; nhánh khớp/lệch chỉ sinh hai vế; các mutant cấp lại hạn bị t156 giết |
| F7.1 | Không còn kết luận loại trừ actor/chập chờn; giữ rc, số đếm, tên ca và hướng đọc log gốc |
| F7.2 | Vá một phần: chặn ba mutant đã khai và parser hằng; còn các lỗ wiring N01/N02/N12/N17/N18 |

## BẢNG ĐO

| Đối tượng | Kết quả trước gián đoạn | Hiện vật |
|---|---|---|
| HEAD/base/hash hai tệp | Khớp SHA đầy đủ đầu báo cáo | review-logs/metadata.json |
| Diff PR ba chấm | 2 tệp, +1082/−27 | metadata.json |
| HINT lượt 5 | Áp fuzz=0 lên c3bcfa1; bytes hai tệp bằng HEAD; 3 hunk +78/−107 Python | metadata.json |
| Merge a15f302→353eae1 | Chỉ ops/dung_goi_review.sh và ops/reviews/DO-T33-VA-GOI-REVIEW-20260907.md, không write set | metadata.json |
| Log tác giả dòng 1055 | [B] 155/155, đã chạy155, bỏ qua0 | nguon/suite-luot6-linux.log |
| Dòng 1060 | [A] 155/155, đã chạy155, bỏ qua0 | cùng log |
| Dòng 1156 | CHA 155/155, đã chạy155, bỏ qua0 | cùng log |
| Dòng 1061 | t125 CHA 72.143s QUA | cùng log |
| Dòng 1148 | t160 CHA 0.038s QUA | cùng log |
| Tên ca log tác giả | Đúng 155 tên/thứ tự ở CHA/A/B, không đỏ | metadata.json |
| Gói actionlint | SHA256 đúng 023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757, bằng băm ghim installer | Đã băm trực tiếp |
| Wrapper nguyên dạng | rc=5 do tar không nhận UID1001/GID996 của archive trong sandbox | wrapper-exact.log |
| Wrapper bản sao chọn lọc, TAR_OPTIONS=--no-same-owner | rc=0; CHA/A/B 155/155 | wrapper.log |
| Lượt harness đặt TMPDIR bên trong cây | Tự sao chép đệ quy ở t82, đã hủy; lỗi harness, không tính finding | wrapper-bad-tmp.log |
| Catalogue của tác giả | 16/16 chết đúng ca/chốt, đã giữ stdout đầy đủ từng mutant | catalog-original.txt; catalog-original/ |
| Hai control catalogue | RuntimeError→TIN DUNG GIA; Exception trần→GIET THAT sai | catalog-known.txt; catalog-known/ |
| Ngân sách/thu hồi HEAD thật | Hai con nhóm riêng, timeout 0.5s, nhịp cháu13→13 và12→12 | behavior.json |
| Khớp/lệch tại consumer thật | Hai spawn qua helper, bốn tee, run0/Popen phụ0 | behavior.json |
| N10 full wrapper | CHA155/155, không dòng tee A/B; audit vẫn có hai lượt toàn suite | full-N10.log; full-N10-spawns.jsonl |
| N12 full wrapper | CHA/A/B155/155, retry qua Popen không bị t160 bắt | full-N12.log |
| N12 probe thu nhỏ | 4 lần cấp đủ0.04s, tổng0.2261s; PIPE giữ marker; cả4 con cùng nhóm runner | impact.json |
| S2 bảng cũ từ b98531e | 27463d4=67; e0b5bf0=195;8ffd062=746;59a0ed4=914;1df4729=991;353eae1=1082 | metadata.json |
| Base lease thật | b98531e256ea91e20f31b74ac6b9046e8fac8eed trên ref origin/ops/cap-lease-504 cũ | lease504.yaml, SHA256 a4b5bebe0f7d7ca821f2901067282672f6bdb4e405a7c83a5a7e249af4033317 |
| S2 nâng trần mới | git show2d0ee53 rc=128, object không có; +1082≤1500 đúng theo trần người dùng cung cấp; nội dung khối KHÔNG ĐO ĐƯỢC | review-logs/s2-final.json |
| HINT kiểm ca/mutant | t160 control xanh; catalogue16/16 chết thật; N01–N18 có17 chết đúng chốt, N09 tương đương sống | hint-new-mutants.txt; hint-more-mutants.txt; hint-catalog-original.txt |
| HINT full wrapper | Hai lượt bị hạ tầng ngắt, chưa có tổng kết CHA; không khai xanh | hint-wrapper.log; hint-wrapper-resume.log |
| HINT áp dụng | Dry-run rc=0,3 hunk/1 tệp; compile thành công | review-logs/hint-final.json |

## Findings theo lớp

**Chốt: 3 lớp P1, 0 lớp P2, 0 lớp P3; 5 thể hiện.** F2 có 1 thể hiện (F2.3: ngắt tee tại caller); F6 có 1 (F6.4: catalogue cấp tín dụng giả); F7 có 3 (F7.2a: đảo nhãn, F7.2b: bỏ mẫu số, F7.2c: hồi sinh retry qua Popen). F7 được xếp P1 theo tiêu chí phản chứng có mutant không tương đương sống và có đường nhận lệch làm khớp. Không đếm N09 tương đương; không đếm lặp tác động N12 vào F1/F4.

**F2.3 — consumer có thể bỏ toàn bộ tee mà suite vẫn xanh (P1 theo tiêu chí mutant sống).** `ops/lease_publish_test.py:4290`; N10 thay danh sách luồng ở t125 bằng []: t158 xanh, full wrapper CHA155/155, không dòng A/B. Probe có lỗi giữ lại thông điệp chung nhưng làm mất mọi lý do từng ca trong stdout. Đây là lỗ phản chứng ở caller; HEAD chưa đột biến vẫn tee bình thường. Không tính retry cũ F2.2 còn tồn tại.

**F6.4 — bộ đo cấp tín dụng giả (P1).** cong-cu/dotbien512.py:123 chỉ nhận một số tên ngoại lệ kết thúc Error/Exception có tiền tố. Control t160 ném Exception('CONTROL unrelated to A/B') bị tính GIET THAT, trong khi RuntimeError bị loại. Không suy 16 mutant tác giả là giả: 16 log thực đã có đúng chốt. Sửa công cụ ngoài write set bằng hồ sơ riêng; không lén đưa nó vào HINT.

**F7 — P1, phản chứng nối dây còn ba thể hiện.** **F7.2a** (`ops/lease_publish_test.py:4310`, `:4312`, `:6247`): N01/N02 đảo nhãn A/B nhưng t160 vẫn qua vì chỉ kiểm chuỗi không gắn nhãn; impact.json ghi sai vế có actor. **F7.2b** (`ops/lease_publish_test.py:4272`, `:6239`): N17/N18 bỏ mẫu số: t160 qua, consumer thật nhận A1/2 và B1/3 như khớp. **F7.2c** (`ops/lease_publish_test.py:6233`): N12 đưa retry về bằng Popen/PIPE, không nhóm/tee/ngân sách tổng: t160 và full wrapper vẫn xanh. N11 cùng đường dùng run bị giết đúng. Các lỗi phát hiện là thiếu răng ở HEAD; không khẳng định HEAD thật đang chạy retry. N09 chỉ đổi consumer sang kiểm thông điệp khớp là mutant tương đương tại HEAD, không tính finding.

## Mutant đã chạy

| Mutant HEAD | Kết quả đã lưu |
|---|---|
| Catalogue 16 mutant, gồm M15/M16/M17 | 16 chết thật, đúng ca, không ngoại lệ vô can trong log thực |
| N01 đổi thứ tự đối số classifier | SỐNG t160 |
| N02 đảo nhãn kết quả trước classifier | SỐNG t160 |
| N03 consumer dùng truthiness thông điệp | CHẾT t160 |
| N04 parser trả tuple hằng | CHẾT t160 |
| N05 fixture luôn dùng cap[0] | CHẾT t160 |
| N06 parser bỏ rc | CHẾT t160 |
| N07 classifier bỏ tập đỏ/skip | CHẾT t160 |
| N08 consumer từ chối cả hai cùng đỏ | CHẾT t160 |
| N09 consumer dùng thông điệp thay enum | SỐNG, tương đương ở hợp đồng hiện tại; không finding |
| N10 consumer bỏ luồng tee | SỐNG t158 và full wrapper |
| N11 khôi phục retry run | CHẾT đúng chốt không chạy thêm |
| N12 khôi phục retry Popen | SỐNG t160 và full wrapper |
| N13 thông điệp loại trừ actor | CHẾT t160 |
| N14 parser bỏ skip | CHẾT t160 |
| N15 parser bỏ tên đỏ | CHẾT t160 |
| N16 parser lấy tử làm mẫu | CHẾT t160 |
| N17 classifier bỏ so mẫu số | SỐNG t160; consumer thật xanh khi chỉ mẫu số lệch |
| N18 parser hằng mẫu số | SỐNG t160; consumer thật xanh khi chỉ mẫu số lệch |
| HINT chạy lại N01–N18 | 17 chết đúng chốt; N09 tương đương sống. N10 được chốt mới ở t160, không khai t158 tự bắt nó |

### Tầng chạy lại đã đi thật đến đâu

Ở HEAD chưa đột biến, phép chạy consumer thật với hai log khớp, hai log lệch và hai vế cùng đỏ đều ghi đúng **2 spawn qua `_mo_con_nhom_rieng`, 4 tee, 0 `run` và 0 `Popen` phụ** (`review-logs/behavior.json`). Probe timeout dùng nguyên fixture con/cháu t154: nhóm của hai con khác runner; hai cháu ngừng nhịp. Bằng chứng dương của HEAD là hành vi này, không phải chỉ việc diff mất callback.

A/B vẫn là hai lượt toàn suite. Các subprocess ở t153/t155 chạy selector; `_chay_day_lenh_trong_ngan_sach` dùng cho dãy lint ở t137, không phải bộ sinh A/B. A/B có deadline mỗi con từ lúc start và waiter đồng thời. Vì thế không đòi mọi lời gọi suite phải đi qua bộ chạy dãy lint. `subprocess.run` của taskkill ở nhánh thu hồi Windows cũng không phải một lượt suite. Trong các đường đã kiểm, không còn một lượt suite phụ không selector chạy bằng run/PIPE.

Nói chính xác về tầng đã xoá: callback tại c3bcfa1 thêm `CO_CHI_CA + ten_ca`, tức chạy lại **từng ca lệch** sau A/B toàn suite. N12 tái sinh đúng loại tầng ấy qua Popen; không khai N12 sinh thêm một lượt toàn suite không selector. Nó vẫn qua toàn suite155/155×3, trong khi probe độc lập ghi4 tiến trình phụ cùng nhóm runner, stdout/stderrPIPE, mỗi lần được cấp lại0.04s, marker chỉ ở output bị giữ. Do đó việc XOÁ đã đóng đường lỗi thực tế cũ F1.4/F2.2/F4.4; sự vắng mặt của tầng ấy **chưa được phản chứng khóa đầy đủ**. Lỗ canh hồi quy này được tính một lần tại F7.2c, không tính lại ba lỗi đang tồn tại ở HEAD.

### Đánh đổi về chẩn đoán

**(i) Trạng thái chưa rõ không làm mất dấu lỗi thật trong HEAD đã đo.** Consumer giữ rc/số đếm hai vế, tên ca đỏ/skip lệch và trỏ log[A]/[B]. Probe đưa đúng lý do S8 vào vếB: stdout teed vẫn chứa `S8-bo-deadline`, `thực SONG` và seam `KhoObject._con_thoi_gian`. Người đọc tìm được ca và lỗi gốc; thông điệp không còn phủ nhận actor khi chưa loại trừ nó. Không gán P1 cho chính nhãn “chưa rõ”. N10 là một lỗi phản chứng riêng có thể làm mất chi tiết log, được ghi ở F2.3.

**(ii) Ba nguyên nhân nêu trong thân không phải danh sách đầy đủ.** Ví dụ thêm được: khác biệt dữ liệu/tên thư mục tạm giữa hai lượt hoặc lỗi I/O nhất thời của công cụ. Đây là những khả năng chưa loại trừ, chưa được tái hiện thành lỗi HEAD trong lượt này. Câu “không kết luận nguyên nhân từ riêng hai kết quả” không đóng danh sách ở actor/thứ tự/tải và không phủ nhận các khả năng khác. Không có căn cứ nâng sự không liệt kê mọi nguyên nhân thành finding; có thể thêm chữ “ví dụ” nếu muốn rõ hơn, nhưng không cần thêm P3 để kéo dài review.

**(iii) Ca chập chờn làm hai vế lệch khiến t125 đỏ là fail-close đối với phép đo bất biến.** Lượt ấy chưa chứng minh bất biến; tự nhận xanh hoặc quy chắc cho actor đều vượt phép đo. Nó có chi phí điều tra/chạy lại CI, nhưng chưa có chứng cứ để gọi là cổng đỏ oan. Không ước tần suất từ một trích log lỗi và sáu lần không tái hiện do tác giả kể: mẫu ấy không xác lập tần suất CI. Tần suất đỏ do flake **KHÔNG ĐO ĐƯỢC**, không phải0. Chẩn đoán “chưa rõ” giữ nợ đó lộ ra; nó không sửa nợ S8. Lý do CI đỏ e6feddb là mutantS8 sống ở seam sản phẩm, tách riêng ngoài write set/S3; HINT không chữa mã sản phẩm.

### S2 — phép đo và giới hạn của override

Lease thật trong snapshot cũ neo `base_sha=b98531e256ea91e20f31b74ac6b9046e8fac8eed`; bảng67/195/746/914/991/1082 tái lập từ chính base ấy. Base→origin/master không đổi hai đường write set, nên số+1082 cũng khớp diff PR ba chấm. Không thấy nhánh sửa ngưỡng S2 trong write set; việc mã vượt300 không tự chứng minh một hành động nâng trần. Phần lời khai đã quét mọi PR/Issue và comment thông báo không được xác minh online trong lượt offline này.

Theo cập nhật của người dùng, trần S2 mới là1500 và **1082≤1500**. Tuy nhiên, lệnh đọc exact commit`2d0ee53` trả **rc=128: invalid object name**; ref offline `origin/ops/cap-lease-504` còn ở `87b833e039a941629930007fa97b7e3e14acccdc`. Không suy từ thiếu object rằng khối sai hoặc người dùng chưa cấp quyền.

`ops/specs/WINDOWS-LEASE-SUITE.md:132` vẫn ghi A5≤300, `:161` ghi S2>300. Vì **1082>300**, không thể dùng bất đẳng thức1082≤1500 để tuyên “A5 đạt” theo văn bản đóng băng. Cách phân biệt **OVERRIDE thay cho A5 đạt** trong yêu cầu là nhất quán về phép đo; nội dung khối mới có thật sự tự khai đúng như vậy hay không **KHÔNG ĐO ĐƯỢC từ snapshot này**. Đây là giới hạn đầu vào, không thêm một finding suy đoán hay phán xử thẩm quyền nâng trần.

### HINT đã nộp

`HINT.patch` có **3 hunk, 1 tệp**: `ops/lease_publish_test.py`, nằm trong hai đường write set. Dry-run `patch -p0 --dry-run --fuzz=0` từ gốc `cay-kho/` **rc=0**. SHA256 `e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0`.

Patch gia cố t160 bằng tuple đúng nhãn, đầy đủ thành phần, hai hướng A/B, bốn đường tee tại consumer, và chốt không mở thêm run/Popen ngoài biên tiến trình giả. Control t160 xanh;17 mutant không tương đương đều chết đúng chốt; N09 tương đương còn xanh. Catalogue gốc16/16 cũng chết thật trên bản HINT. Hai lượt full wrapper HINT bị hạ tầng cắt: lượt đầu đang chạy t113 trong A/B; lượt nối lại đã tới t158 ở CHA lúc10:41Z nhưng không có tổng kết CHA. **Không khai HINT đã qua full wrapper.**

F6.4 nằm trong công cụ ngoài write set nên không có bản vá catalogue trong HINT. Việc cần làm riêng: sửa cách nhận tín hiệu “chết đúng chốt”, chạy control ngoại lệ vô can trước khi tính tín dụng, và giữ log đầy đủ để phân biệt chốt mục tiêu với lỗi runner. Không dùng con số16/16 đơn độc để chứng minh bộ phân hạng miễn nhiễm ngoại lệ.

## chua_do_duoc

- **Khối nâng trần S2 tại2d0ee53:** object không có trong snapshot; đã thử đọc exact commit và ghi rc128. Đã kiểm số+1082 và bất đẳng thức với1500; chưa chứng nhận lời khai OVERRIDE trong khối chưa đọc được.
- **Full wrapper trên HINT:** hai lượt bị hạ tầng ngắt, thiếu tổng kết CHA; chỉ công nhận control/các mutant/dry-run/compile đã hoàn tất. Full wrapper HEAD và hai mutant N10/N12 đã hoàn tất như bảng đo; không đánh đồng các cây.
- **Windows exact HEAD/A3/A4:** không chạy theo chỉ thị chủ kho. Linux155/155 không chứng nhận thời gian Windows≤15 phút hay gate sau merge.
- **S8 trên CI e6feddb:** trích log xác định mutant/seam, chưa đo tần suất và chưa chữa gốc ngoài write set/S3. Không đề xuất sửa sản phẩm trong HINT.
- **Nguyên nhân và tần suất chập chờn:** chưa có phép đo phân biệt nhân quả hay mẫu đại diện CI; không gọi “chưa rõ” là đã loại trừ actor, cũng không tự xếp P1 đỏ oan.
- **Cổng hồ sơ7/47 và metadata online:** các số doctrine-scan/adr-song trong EVIDENCE không được đo lại trong lượt này; không đọc tệp chỉ dẫn bị cấm để xác minh. Không mạng/GitHub/comment; không xác minh toàn bộ PR/Issue, sự kiện nâng trần online hoặc backend mô hình độc lập.

Kiểm vệ sinh cuối: HEAD vẫn353eae10120da2a1788dcaf7a906fe46261bd71b; hash hai tệp không đổi; `git -C cay-kho status --porcelain` **RỖNG** và `git -C cay-kho log --oneline 353eae1..HEAD` **RỖNG**. Không commit, không sửa cây git được review.
