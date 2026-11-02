verdict: changes_requested
reviewed_sha: d58d649ff061ff125bc004414ed4a0787de8e5f3

Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

# Cross-review PR #1091

Đã hoàn tất độc lập trên cây mã cục bộ; chỉ đọc và đo, không gọi mạng, không sửa `cay-kho/`. Mọi đột biến và patch gợi ý được thực hiện trên bản sao bên ngoài cây mã. Windows native (icacls/NTFS) không có ở môi trường này: KHÔNG ĐO ĐƯỢC.

**changes_requested** vì một P2 trong mô hình/fixture reset: suite nguyên bản 116/116 nhưng bỏ `/T` reset, reset no-op, hoặc dời reset sau copy với điều kiện đã đếm trước đó vẫn xanh. Chưa đo được lỗi P0/P1 của sản phẩm HEAD. Gợi ý test thuần `HINT.patch` đạt 118/118 và bắt đúng ba đột biến trọng tâm trên bản sao Linux.

## Nhật ký tăng dần

### Hướng 0 — Tiếp nhận chỉ thị

- Giả thuyết: snapshot xác định đúng đối tượng và giới hạn phép đo.
- Lệnh: `cat runs/6fd13df4/prompt.snapshot`.
- Output: yêu cầu review SHA `d58d649ff061ff125bc004414ed4a0787de8e5f3`, chạy bộ PowerShell với `TL_TEST_PYTHON=python3`, xem ACL kế thừa/reset và kiểm tra sức phân biệt của đồ giả bằng đột biến trên bản sao.
- Kết luận: KHÔNG PHẢI LỖI; đã đọc chỉ thị và khởi tạo nhật ký ngay. Chưa kết luận approve.

### Hướng 1 — Mỏ neo, phạm vi và tính độc lập

- Giả thuyết: review nhầm HEAD/base hoặc snapshot/diff không khớp cây nguồn.
- Lệnh: các lệnh `git rev-parse HEAD origin/master HEAD^{tree}`, `git status --porcelain=v1 --untracked-files=all --ignored`, so byte `git diff origin/master...HEAD` với `diff.patch`; bằng chứng: `evidence/preflight.json`.
- Output: HEAD `d58d649ff061ff125bc004414ed4a0787de8e5f3`; base `90c101b8d1f8895b66607de8582a18c5e72d834c`; tree `78db0ce7aa198486b266a6e3d6eff7d822519109`; detached; shallow=false; core.abbrev=7; status rỗng; diff khớp byte; `PROMPT.md` = `prompt.snapshot`. Hai tệp đổi đúng phạm vi (+8/-1 và +33/-5).
- Kết luận: KHÔNG PHẢI LỖI. Authority là chỉ thị trực tiếp trong snapshot; review ngoại tuyến, không xét land/CI live. Reviewer Codex; provider `openai_codex`, model_family `openai`, execution_surface `codex_service` (API với công cụ shell), transport `machine`. Không nhận context executor, không đăng GitHub; model/effort phục vụ cụ thể KHÔNG ĐO ĐƯỢC bằng công cụ phiên này. Cây nguồn chỉ đọc theo quy tắc thao tác; sandbox thực tế cho phép ghi workspace nên read-only không phải bảo đảm cơ chế mount.

### Hướng 2 — Bộ test bắt buộc trên mã nguyên bản

- Giả thuyết: kết quả 116/116 của executor không tái lập được trên Linux tại exact SHA.
- Lệnh: `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/head-tests.log 2>&1`.
- Output: `cap-nhat-cong-cu tests: 116/116 ca QUA`; mã thoát thật 0 (`evidence/head-tests.rc`).
- Kết luận: KHÔNG PHẢI LỖI trong bộ test Linux. Không dùng lời khai 72/72 Windows hay lần chạy VM ở SHA khác làm bằng chứng cho HEAD này. Native icacls/NTFS/Scheduled Task Windows: KHÔNG ĐO ĐƯỢC.

### Hướng 3 — Luồng ACL, nguồn kế thừa và các biên Windows

- Giả thuyết: `/reset` lấy quyền từ Program Files hoặc mở lại quyền ghi cho Users; xử lý cây con/ẩn/khóa có thể bị bỏ qua.
- Lệnh: đọc có số dòng `ops/vm/cap-nhat-cong-cu.ps1:172–235,595–699`, `ops/vm/README.md`; đối chiếu diff và hợp đồng ở verdict lượt 16.
- Output phân tích tĩnh: `Assert-KhongReparse` quét tổ tiên, gốc và con (Recurse/Force, không đi theo liên kết), trước icacls. Thứ tự hiện hành là setowner toàn cây → đặt ACL gốc không `/T` → `Get-ChildItem -LiteralPath ... -Force` → reset `<gốc>/* /T /C /L /Q` nếu có con → chép ba tệp → setowner toàn cây → đo owner/bit ghi của gốc và ba tệp + băm → đăng ký tác vụ. Root tắt kế thừa; ba grant mang `(OI)(CI)` nên nguồn kế thừa của con là root vừa đặt, không phải trực tiếp Program Files. Users được RX, không có bit ghi trong grant mới.
- Điều kiện quan trọng: `/inheritance:r /grant:r` không phải thay thế toàn bộ DACL gốc; ACE explicit của danh tính khác có thể còn. Chốt `Test-AclChiAdminGhi` sau chép sẽ từ chối grant ghi không tin cậy ở root/ba tệp; không được diễn giải `/reset` là tự làm sạch mọi ACL gốc tùy ý. Guard này và giới hạn kiểm bốn nút là mã nền đã có, không phải delta mới. Không có phản chứng P0/P1 mới được đo từ đây.
- Phân tích biên: phép đếm chỉ cần biết có ít nhất một con trực tiếp; không cần đếm bằng số nút reset. `-Force` yêu cầu liệt kê cả hidden/system ở PowerShell. `/T` của icacls chịu trách nhiệm cây lồng; `/L` yêu cầu thao tác chính liên kết, `/C` tiếp tục nhưng `Invoke-Icacls` vẫn ném khi rc khác 0. Lỗi enumeration dưới `$ErrorActionPreference='Stop'` cũng đi vào catch đăng ký mã 6. Khóa chia sẻ, tên dài/ẩn/system thật và hành vi wildcard Win32 (kể cả không đuôi) không thể suy thành pass từ Linux.
- Kết luận: KHÔNG PHẢI LỖI về cấu trúc nguồn kế thừa và thứ tự ở HEAD khi phân tích tĩnh; KHÔNG ĐO ĐƯỢC về NTFS/icacls native, effective access, thứ tự truyền ACL native, khóa tệp Windows và race. Không lấy đồ giả làm chứng nhận các tính chất đó.

### Hướng 4 — Đột biến độc lập: có răng ở đâu, bỏ lọt ở đâu

- Giả thuyết: ca đăng ký lại chỉ kiểm tra hình dạng argv mà không quan sát hiệu ứng reset trên trạng thái thực sự cần sửa.
- Lệnh: `python3 -B probes/mutations.py > evidence/mutations-driver.log 2>&1` (12 đột biến + control, ba tiến trình độc lập, mỗi tiến trình một bản sao); `python3 -B probes/mutations.py reset_after_copy_cached_condition > evidence/mutations-extra-driver.log 2>&1`. Mỗi delta/log/băm được lưu ở `evidence/`; không sửa nguồn.
- Output ban đầu: control 116/116 rc0; trả `/T` không reset 114/116 rc1 (đúng hai ca executor khai); bỏ reset 115/116 rc1; bỏ `/L` của reset 115/116 rc1; reset trước grant 115/116 rc1; thêm lại `/T` nhưng giữ reset 115/116 rc1; reset gốc thay vì wildcard 115/116 rc1; bỏ setowner cuối hoặc Users=Modify đều 110/116 rc1. Không có ParserError.
- Phản chứng: bỏ `/T` riêng của reset **116/116 rc0**; biến hiệu ứng `/reset` của đồ giả thành no-op **116/116 rc0**. Fixture `ban-cu` cho cả ba tệp Administrators FullControl từ đầu; chỉ bỏ reset không tạo AccessDenied vì vẫn chép được vào chúng, ca đỏ vì thiếu lệnh reset. Mô hình mới chọn mọi hậu duệ khi thấy wildcard dù thiếu `/T`, và lấy ACL gốc cho mọi cấp thay vì cha trực tiếp. Đây là chỗ xanh nhờ đồ giả/fixture, khác với lỗi cũ đã được bắt.
- Kết luận: **LỖI P2 về sức phân biệt của test/reset model**; chưa có bằng chứng P1 ở mã sản phẩm HEAD. Đang đối chứng bằng fixture DACL rỗng, cây lồng và kiểm gợi ý test trên bản sao.

### Hướng 5 — Đối chứng trạng thái DACL rỗng và cây lồng

- Giả thuyết: hai đột biến sống sót được che bởi trạng thái đầu quá lành hoặc mô hình chọn sai phạm vi.
- Lệnh: `python3 -B probes/state-probes.py > evidence/state-probes-driver.log 2>&1`; harness PowerShell trích phần đăng ký và đồ giả của HEAD, thêm fixture ngoài cây nguồn. JSON từng phép đo ở `evidence/head_empty.json`, `no_reset_empty.json`, `after_copy_empty.json`, `head_nested.json`, `no_T_nested_original_model.json`, `no_T_nested_recursive_model.json`.
- Output: DACL ba tệp rỗng → HEAD đạt dấu dừng trước mật khẩu, tasks=1; bỏ reset hoặc reset sau copy → AccessDenied, tasks=0. Với cây chín nút (root, ba tệp cài, hai thư mục lồng, tệp dấu chấm và tệp không đuôi), HEAD theo mô hình giới hạn chọn đúng `/T` → 0 nút có grant ghi Users; mutant không `/T` dùng đồ giả nguyên bản → vẫn 0; cùng mutant dùng mô hình chọn con trực tiếp khi không `/T` → còn **3 nút** có grant Users Modify dù đã đến đăng ký tác vụ.
- Giới hạn: những trạng thái ACL này là dữ liệu mô hình, không phải Get-Acl/NTFS thật. Mô hình đối chứng coi DACL các nút độc lập/protected trước reset; không mô phỏng mọi tổ hợp inheritance flags hay effective access. Tệp/thư mục, hash và luồng Register-LichCapNhat là thật trên Linux. Không dùng con số ba nút để gọi lỗi native P1 của HEAD.
- Kết luận: **LỖI P2 được đối chứng**: fixture/mô hình hiện tại không đo được hai hậu điều chính của sửa chữa (hồi phục tệp DACL rỗng trước chép và phủ cây con theo `/T`). Mã sản phẩm HEAD vượt cả hai đối chứng mô hình.

### Hướng 6 — Wildcard qua native argv, enumeration và lỗi rc

- Giả thuyết: PowerShell nở `*` hoặc ký tự `[]` trước khi giao icacls; wrapper nuốt lỗi rc dưới `/C`; phép đếm bỏ qua tệp ẩn.
- Lệnh: `pwsh/pwsh -NoProfile -File probes/native-wrapper.ps1 -Product "$PWD/cay-kho/ops/vm/cap-nhat-cong-cu.ps1" -Evidence "$PWD/evidence"`; output lưu `evidence/native-wrapper.log`, JSON ở `evidence/native-wrapper.json`.
- Output: `Wrapper/argv: 3/3 PASS; enumeration Linux: 1/1 PASS; native Windows: KHONG_DO_DUOC`; rc0. Shim executable nhận nguyên một đối số `<install [x]>/*`, đủ `/reset /T /C /L /Q`; rc0 không ném, rc1 và rc5 đều ném. Enumeration thật Linux: không Force thấy 3 nút, Force thấy 4 gồm `.hidden`, `noextension`, `normal.txt`, `nested`.
- Kết luận: KHÔNG PHẢI LỖI về chuyển argv, phản ứng với rc và enumeration Linux trong phép đo. Windows wildcard hidden/system/không đuôi và sharing lock: **KHÔNG ĐO ĐƯỢC**. Shim là executable thật với argv/rc thật nhưng không phải icacls Windows.

### Hướng 7 — Kiểm gợi ý test và các đột biến sống sót

- Giả thuyết: có thể khóa thiếu sót bằng thay đổi test thuần, giữ nguyên sản phẩm và không tạo lỗi xanh/đỏ do setup.
- Lệnh: `python3 -B probes/validate-hint.py > evidence/hint-validation-driver.log 2>&1`. Bản control được tạo bằng `patch -p0 --batch --input <HINT.patch>` trong `copies/hint-control/`, rồi so byte với bản gợi ý. Đã chạy thực trên bản sao; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.
- Output: patch áp đúng một tệp `ops/vm/cap-nhat-cong-cu_test.ps1`, không fuzz/reject. Head + test gợi ý **118/118 rc0**. Mutant reset không `/T` **117/118 rc1**, đỏ đúng `dk_chay_reset_ca_cay_long_va_tep_an`; dời reset sau copy và cache điều kiện từ trước **117/118 rc1**, đỏ đúng `dk_chay_sua_tep_dacl_rong_truoc_khi_chep`; mô hình reset no-op **116/118 rc1**, đỏ cả hai ca mới. Tất cả không có ParserError. Logs và JSON ở `evidence/hint-*.log`, `evidence/hint-validation.json`.
- Đối chiếu quan trọng: mutant dời nguyên block reset sau copy (không cache) bị suite cũ bắt 115/116 do clean install nay cũng chạy reset; mutant cache điều kiện là **116/116 rc0** với suite nguyên bản (`evidence/mutations-extra.json`). Vì vậy phản chứng về thứ tự không dựa vào một mutant đã bị suite bắt, và oracle mới đo hành vi tệp DACL rỗng chứ không chỉ đếm lệnh.
- Kết luận: KHÔNG PHẢI LỖI trong thử nghiệm gợi ý trên Linux; hai ca mới và phạm vi chọn cây của mô hình bắt đúng ba đột biến trọng tâm trước đó xanh. Gợi ý chỉ là test thuần; không thay thế phép đo native Windows.

## Finding

### test-reset-thieu-trang-thai-va-pham-vi  [P2]

**TỆP/DÒNG:** `ops/vm/cap-nhat-cong-cu_test.ps1:948–952` (fixture), `:992–1008` (mô hình icacls), `:1064–1068` (ca đăng ký lại).

**VẤN ĐỀ:** Ca mới cho ba tệp sẵn có Administrators FullControl rồi chỉ đòi thành công và có một lệnh reset/wildcard/`/L`. Nó không cần hiệu ứng reset để chép thành công: đổi nhánh reset của đồ giả thành no-op vẫn 116/116. Đồng thời nhánh wildcard của đồ giả nhận mọi hậu duệ bất kể `/T`, và sao chép quyền root cho mọi cấp; mô hình còn dùng `$laCon` thay cho loại nút khi quyết định bỏ ACE `(OI)/(CI)`, nên cả thư mục con cũng bị coi như tệp. Thiếu fixture trạng thái DACL rỗng và cây lồng khiến các hồi quy trực tiếp của sửa chữa này xanh: bỏ `/T` reset hoặc dời reset sau chép (cache điều kiện trước chép) đều 116/116. Đây là thiếu sức phân biệt ở bằng chứng test mới, không phải kết luận bản vá sản phẩm HEAD đã sai trên Windows.

**ĐÃ THỬ NGHIỆM:** Các lệnh H4/H5/H7 và patch/log từng mutant ở `evidence/`. Suite nguyên bản 116/116; ba đột biến trọng tâm đều 116/116. Với fixture DACL rỗng, HEAD đạt dấu dừng trước mật khẩu còn reset sau copy gặp AccessDenied trước mọi tác vụ; với cây lồng, mô hình gốc che ba nút còn Users Modify khi thiếu `/T`. Gợi ý test cho HEAD 118/118, bắt đúng ba mutant bằng các assertion trạng thái/hành vi (117/118,117/118,116/118). Kết quả có đối chứng dương và âm, không chỉ kiểm chuỗi mã.

**ĐỘ TIN:** Cao cho thiếu sót của suite/mô hình (đã chạy PowerShell và đột biến trên bản sao). Hành vi NTFS/icacls native của mọi biên Windows: KHÔNG ĐO ĐƯỢC; không nâng thành P1 hoặc P0.

**GỢI Ý VÁ:** Vá riêng fixture và mô hình trong tệp test, vì sản phẩm HEAD đã có đúng thứ tự và `/T`. Thêm ca với ba tệp DACL rỗng để thành công phụ thuộc vào reset trước copy; thêm cây lồng có ACL xấu/protected giả lập và kiểm trạng thái mọi nút. Nhánh wildcard phải chọn con trực tiếp khi thiếu `/T`; reset từ cha trực tiếp theo thứ tự từ trên xuống; phân biệt tệp với thư mục khi xử lý `(OI)/(CI)`. `HINT.patch` là gợi ý test đã kiểm trên bản sao, áp bằng `patch -p0` từ gốc bản sao kho; executor phải tự tái dẫn xuất và đo. Các mutant bỏ `/T`, reset sau copy có cache, reset no-op phải chết. Rủi ro gợi ý: mở rộng đồ giả có thể tạo cảm giác đã mô phỏng NTFS đầy đủ; giữ nhãn mô hình giới hạn, và không nhận `.tep-an` Linux là phép đo thuộc tính Hidden/System Windows. Gợi ý chưa được chạy trên Windows.

## Bảng lớp và lịch sử

| Lớp | Biểu hiện | Mức còn mở | Nguồn | Cách đóng lớp |
| --- | --- | --- | --- | --- |
| `test-reset-thieu-trang-thai-va-pham-vi` | Thiếu trạng thái cần reset trước copy; wildcard luôn đệ quy và mô hình không phân biệt loại nút | P2 | Delta PR #1091 tại SHA đang review, đối chiếu H4/H5 | Fixture DACL rỗng + cây lồng; head xanh và ba mutant trọng tâm đỏ như H7 |

Một lớp, hai nhóm biểu hiện, một finding P2. Baseline `verdict-luot16.md` approve `210ab81c3f1af36243748458eb5e70180baeab71` là lịch sử hợp đồng, không dùng để chứng nhận code mới; không tái mở các hợp đồng phiên bản/băm đã chốt khi không có phản chứng liên quan diff. Lớp P2 hiện tại nằm ở fixture/mô hình reset mới. Chưa phát hiện P0/P1/P3 trong phạm vi review này.

### Hướng 8 — Kiểm cuối cây nguồn và hiện vật

- Giả thuyết: nguồn thay đổi sau đo, số đột biến sai, patch gợi ý lẫn mã sản phẩm hoặc các kết quả báo cáo không được oracle xác nhận.
- Lệnh: chạy thêm harness DACL rỗng cho mutant cache điều kiện (`probes/state-original-model.ps1`, output `evidence/after_copy_cached_empty.json`), rồi `python3 -B probes/final-audit.py > evidence/final-audit.log 2>&1`.
- Output: `Final audit: PASS; reviewed tree unchanged; exact head/base/diff and recorded oracles agree.`; rc0. HEAD/tree/base giữ nguyên; tracked/index/untracked/ignored snapshot đều rỗng. Cả năm tệp nguồn bằng Git blob và bằng băm preflight; diff vẫn khớp `diff.patch`; prompt khớp snapshot. Bộ bắt buộc 116/116 rc0; 13 mutant khác byte, 9 bị bắt và 4 xanh, không ParserError; test gợi ý 118/118 rc0, 3/3 mutant trọng tâm bị bắt; oracle kiểm 7/7 kết quả trạng thái; wrapper argv/rc 3/3 và enumeration Linux 1/1. HINT chỉ đổi một tệp test, băm SHA-256 `ca0c2ea4e81b3dfe86b8741360ef98d037408d9bfa5b9423e0db786ba212cfbe`.
- Phân loại mutant xanh: hai mutant sản phẩm (`reset_no_T`, `reset_after_copy_cached_condition`) và mất hiệu ứng reset của đồ giả là bằng chứng cho P2. Mutant thứ tư bỏ từ chối Copy-Item của đồ giả cũng xanh nhưng không được tính là finding riêng: với HEAD lành, bước reset đã chữa trạng thái trước copy nên không có nhánh từ chối cần chạy. Không coi mọi mutant sống sót tự động là lỗi sản phẩm.
- Kết luận: KHÔNG PHẢI LỖI về tính toàn vẹn phép đo và phạm vi patch gợi ý. Snapshot sạch chứng minh không có delta quan sát được tại đầu/cuối, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Trong các thao tác của reviewer, nguồn chỉ được đọc; không push/merge/gọi mạng. Native Windows, sharing lock và effective NTFS ACL vẫn KHÔNG ĐO ĐƯỢC. P2 còn mở nên kết luận cuối là **changes_requested** tại exact SHA trên.
