### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Bản #456 chưa bia mộ vẫn giữ write set trước hạn

TỆP/DÒNG: `ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml:39` trên `origin/master`, blob `8b2103c06687546379a17f6deafc97f1fe0173fd`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:574` (A9); `ops/leases/gate-tach-job-cat-chi-phi-exec-1r3-claude-20260906.yaml:123`.

VẤN ĐỀ: Tại 09:56:25Z ngày 07-09-2026, snapshot có 89 cặp `(blob,path)`, trong đó #456 có hai blob: bản trên cây PR đã mang bia mộ, bản trên master chưa mang bia mộ và còn hạn tới 14:30:07Z. Registry có hai người giữ (#456 và exec-1r3), trái điều kiện bắt tay A9. Cả ba cạnh #456 → exec-1 → exec-1r2 → exec-1r3 trên cây PR đúng hai chiều; điều đó không thu hồi bản cũ trên ref khác. EVIDENCE đã tự khai đúng tình trạng này. Đây là finding còn mở về trạng thái, không cáo buộc executor đã bắt tay trái A9.

ĐÃ THỬ VÁ: Có, mô hình trong bộ nhớ đặt bia mộ trên mọi bản #456 làm registry 2 → 1; giữ nguyên các ref thật. Hướng xử lý: chờ hết hạn rồi fetch đủ ref và đo lại bằng `ai-dang-giu` trên cả hai đường write set, hoặc thu hồi sớm theo thủ tục có thẩm quyền ở mọi ref giữ bản cũ. Ca khóa: một bản mới có bia mộ cùng một bản cũ còn hạn vẫn phải đếm 2; mọi bản hết hạn/thu hồi thì còn 1. Rủi ro: chỉ cập nhật master nhưng còn bản cũ ở ref khác vẫn để hai writer. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review9/static_checks.py`, dùng `_quet_lease_toan_kho(..., doi_chieu_ref=False)`, `_phan_loai_lease`, `_bia_mo_doi_xung` và `_lease_cham_duong` thật. Đo registry=2, ci.yml=1; mô phỏng 14:30:06Z / 14:30:07Z / 14:30:08Z cho registry=2/1/1. `lease_publish.py check` r3 rc=0, nhưng lệnh này không thay phép kiểm chồng lấn. `static.json` giữ ref/blob/trạng thái và hai mô hình; đây chỉ là snapshot offline, chưa phải readback máy chủ sau hết hạn.

ĐỘ TIN: cao với snapshot và mô phỏng; GitHub trực tiếp KHÔNG ĐO ĐƯỢC.

### a2-neo-nen-cu-trai-write-set-hien-tai  [P2]  Bảng thứ tự vẫn xác nhận nền cũ cho A2 đã sửa

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:387`, đối chiếu mục revision `:10–12` và A2 `:460–471`.

VẤN ĐỀ: Phần nghiệm thu r3 đã sửa đúng lỗi P1: lấy dispatch trước tách tại `start_from_sha`, cùng nhánh/event/lane, và PR với YAML nền bằng byte. Nhưng hàng “số đo của GATE (A1/A2/A5)” trong bảng chọn thứ tự vẫn nói nền `34045664423`/`34048685345` “còn đúng”. Hai run đó đều có 39 bước, còn lease có 40; master còn khác lane. Cùng một spec vì vậy vừa rút, vừa xác nhận nền A2 cũ. Hạ mức từ P1 xuống P2 vì phép so nghiệm thu mới đã bác ca mất receipt-v2; không khai rằng bản r3 vẫn cho ca ấy qua.

ĐÃ THỬ VÁ: Có, thay duy nhất hàng :387 trong bản sao văn bản để A2 trỏ về nền mới theo r3; giữ hai run cũ làm nguồn ước lịch sử cho A1/A5. Ca khóa: tách đủ bước phải qua, bỏ receipt-v2 phải đỏ trên cả dispatch và PR; không còn hàng nào gọi nền lịch sử là nền hiện hành cho A2. Rủi ro: xóa cả số lịch sử sẽ làm mất nguồn của 43,20/21,03; sửa spec phải cập nhật revision/băm/lease và neo Issue theo quy trình. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `contract_checks.py` rc=0: mô hình lượt8 tái lập 86/88 bộ ba; nền cũ bác tách đủ nhưng nhận bản bỏ receipt. Phép so r3 trên dispatch nhánh giữ 88/88, bỏ hai bộ ba receipt thì đỏ; PR ubuntu giữ 44/44, bỏ một bộ ba receipt thì đỏ. Baseline PR trong dữ liệu đã lưu: run 34058508426/head 82e01a4, YAML bằng byte d28c4b1. Mô hình sai lane master/dispatch lệch 4 thêm/4 mất. `followup_checks.py` rc=0 xác nhận hàng stale có đúng một lần và hướng sửa loại nó. Không chạy CI mới; conclusion của mô hình dispatch được suy có giới hạn từ hai điều kiện LAND/WORKER thật trong YAML.

ĐỘ TIN: cao; lỗi còn lại là mâu thuẫn văn bản, không phải lỗ đã chứng minh trong phép so r3.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  Vẫn gọi chênh lệch khác lane là nhiễu runner đã đo

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:98–99`, `:107`, `:447–448`, `:531–533`; đối chiếu `:619–625` và Issue #463 `:33–36`.

VẤN ĐỀ: Hai câu gọi mẫu 11 run là master và lời nới theo biên 10,28 đã được sửa. Tuy nhiên :98–99 vẫn tuyên bố nhiễu runner 1–2,3 phút “là có thật” và mọi ngưỡng phải chừa biên; A1/A5 tiếp tục dùng “nhiễu … đo được” làm lý do cho biên. :107 còn gọi hai run ban đầu là hai lượt master. Tự đối chiếu nguồn cho thấy một run nhánh/dispatch và một master/push, cùng tree nhưng khác release-verify lane: 4 bộ ba thêm/4 mất. Chênh job không xác định được phần do runner. Điều này mâu thuẫn với nợ chưa tách nhiễu ở `chua_do_duoc` #3. A1 ≤ 25,00 và A5 ≤ 135,00 vẫn nguyên; không có cơ sở nới chúng.

ĐÃ THỬ VÁ: Có, sửa năm mỏ neo văn bản trong bản sao: gọi đúng mẫu hai run, ghi chênh lệch quan sát và biên thiết kế, giữ nợ đo nhiễu riêng. Ca khóa: metadata phải là 1 nhánh/dispatch + 1 master/push; không câu hiện hành nào gọi chênh khác lane là nhiễu đã tách; A1/A5 và các số nhánh 43,20/21,03 giữ nguyên. Rủi ro: đổi ngưỡng để hợp thức hóa lời giải thích, hoặc gộp số nhánh vào số master. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `measure_costs.py` và `followup_checks.py`, rc=0. Mẫu 11 run đúng 5 master/push + 6 nhánh, 1×39 + 10×40 bước; bảng hệ số khớp 28/28 ô và 12/12 đầu dải. `git diff --name-only 426bfc0 1b3caa1` rỗng nhưng hai tập conclusion 86/86 lệch 4 thêm/4 mất ở LAND/WORKER. Quét rồi đọc ngữ cảnh tìm năm vị trí khẳng định còn sai; thử sửa loại đủ năm và giữ ngưỡng. Các câu lịch sử được trích để phủ định không bị tính thành finding.

ĐỘ TIN: cao về mâu thuẫn và metadata; nguyên nhân/phương sai runner KHÔNG ĐO ĐƯỢC.

### quyet-dinh-tiep-h-con-bi-phu-dinh  [P2]  Phần mở đầu và hàng H vẫn nói chưa chọn

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:56–59`, `:157` (hàng “H — bản này”); đối chiếu quyết định `:254–260`, lease nháp `:119–125` và Issue #464 `:53`.

VẤN ĐỀ: Tiêu đề H và `ly_do_cap` đã sửa đúng theo lượt8. Nhưng phần mở đầu vẫn nói “không khai §12 đã xong”, H “chưa được chọn”; hàng H mang nhãn “bản này” còn ghi “ứng viên — chưa chọn”. Đây là các lời khai hiện hành, không được đánh dấu là trạng thái lịch sử trước quyết định 07-09. Chúng phủ định lựa chọn (1) đã ghi ở §12 và ba hồ sơ. Việc chọn thiết kế không đồng nghĩa cấp lease; năm ô null và Đ1–Đ5 đang được giữ đúng.

ĐÃ THỬ VÁ: Có, sửa khối mở đầu, trạng thái hàng H và tiêu đề bảng ở bản sao reviewer; ghi lựa chọn (1) đã có, lease chưa cấp, Đ1–Đ5 còn ràng buộc. Ca khóa: quét toàn văn cho cả “chưa được chọn” và “chưa chọn”, đọc ngữ cảnh để phân biệt selector regex với quyết định H; giữ URL và null của nháp. Rủi ro: thay “đã chọn” thành “đã cấp” hoặc “mọi điều kiện đã đạt” sẽ tạo lời khai authority/evidence không có. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `contract_checks.py` xác nhận URL 3/3, Đ1–Đ5 5/5, null 5/5 và hai câu đích lượt8 đã mất. Phép quét rộng trong `followup_checks.py` tìm hai phủ định khác tại :59/:157; sửa ba mỏ neo loại chúng, giữ nguyên hai khối Python của H và URL quyết định. Hai script rc=0. Đã sửa kết luận tạm trong VERDICT từ “đã vá” sang “vá hờ” sau khi đọc phần mở đầu/bảng; không dùng phép grep hai chuỗi đích làm bằng chứng hoàn tất.

ĐỘ TIN: cao về văn bản; quyền và nội dung comment chủ kho trực tiếp KHÔNG ĐO ĐƯỢC.

### manifest-luot8-liet-ke-hien-vat-khong-duoc-giao  [P2]  Gói lượt 8 thiếu 19 tệp mà manifest cam kết

TỆP/DÒNG: `ops/reviews/pr468-hoso-4-packet-review-8-codex/ARTIFACTS.sha256:48–66`; `ops/reviews/pr468-hoso-4-packet-review-8-codex-verdict.md:173`.

VẤN ĐỀ: Manifest liệt kê 69 tệp nhưng toàn bộ 19 đường `rig/` vắng trên cây và không có trong `git ls-files`: gồm corpus 1213 ca, bản H trích, đầu ra mutant, nguồn harness và stdout. `sha256sum --check ARTIFACTS.sha256` trả rc=1. Băm chính tệp verdict và receipt v2 vẫn đúng; cổng receipt không chứng nhận cây hiện vật bên cạnh. Đây là phần EVIDENCE không khai. Không nâng thành P1 mất bằng chứng H: cả 19 tệp có bản đúng từng byte tại gói lượt6 và phục dựng được.

ĐÃ THỬ VÁ: Có, trong `do-review9/artifact-repair/`, chép 50 tệp hiện có và điền đúng 19 đường thiếu bằng các tệp lượt6 có SHA-256 trùng manifest; manifest gốc được giữ nguyên. Executor có thể bổ sung chính các byte đã cam kết, hoặc ghi rõ cơ chế tham chiếu chéo và tạo manifest đúng cấu trúc lưu trữ. Ca khóa: mỗi dòng manifest phải trỏ tới tệp có thật và băm đúng; toàn bộ kiểm rc=0. Rủi ro: chỉ xóa dòng thiếu sẽ che mất phạm vi gói, còn dựng lại tên với byte khác thì làm sai chứng cứ lịch sử. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review9/artifact_checks.py` rc=0; bản PR kiểm manifest rc=1, có 50/69 và thiếu 19/69; xác minh 19/19 bản thay thế khớp byte; bản phục dựng kiểm rc=0, 69/69. `artifact-checks.json` lưu ánh xạ từng đường nguồn/đích và hash. Không sửa gói trong checkout, không khai đây là lần chạy lại suite H.

ĐỘ TIN: cao.
