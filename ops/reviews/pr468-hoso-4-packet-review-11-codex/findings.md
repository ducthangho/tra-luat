### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Bản #456 trên ref khác vẫn giữ write set trước hạn

TỆP/DÒNG: `ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml:39` trên `origin/master`, blob `8b2103c06687546379a17f6deafc97f1fe0173fd`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:579` (A9); lease r4 `:125` (`thay_the_cho`).

VẤN ĐỀ: Tại 2026-09-07T11:37:58.336896Z, quét snapshot bằng công cụ thật có 90 cặp `(blob,path)`. #456 có hai blob: một đã mang bia mộ trên cây PR, một chưa mang bia mộ vẫn có trên `origin/master` và ref khác. Registry có hai người giữ (#456 và exec-1r4), trái A9 phải còn đúng một. Bốn cạnh #456 → exec-1 → r2 → r3 → r4 đều đúng hai chiều trên cây PR, nhưng không thu hồi bản cũ trên ref khác. `check` r4 vẫn rc=0. EVIDENCE tự khai đúng việc này; đây là finding trạng thái chưa được đóng, không phải cáo buộc executor đã bắt tay trái A9.

ĐÃ THỬ VÁ: Có, mô hình trong bộ nhớ đặt bia mộ #456 → exec-1 cho mọi bản #456, giữ nguyên chuỗi r1/r2/r3/r4: registry từ 2 về 1. Hướng sửa trên kho thật: chủ kho hoàn tất thu hồi/cập nhật mọi ref còn blob cũ rồi fetch/readback, hoặc đo lại sau 14:30:07Z khi #456 hết hạn. Ca khóa: trên cả hai đường write set, công cụ chỉ còn một người giữ là lease r4 và không còn bản #456 CÒN_HẠN chưa bia mộ. Rủi ro: chỉ sửa master hoặc chỉ đọc cây PR bỏ sót ref khác; không đổi bừa tên người kế nhiệm làm gãy chuỗi; mô phỏng hết hạn không thay được readback thật. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/static_checks.py` rc=0, gọi `_quet_lease_toan_kho(..., doi_chieu_ref=False)` rồi dùng `_phan_loai_lease`, `_bia_mo_doi_xung`, `_lease_cham_duong` của công cụ thật. Mốc 14:30:06Z/07Z/08Z cho registry 2/1/1, ci.yml 1/1/1. Mô hình thu hồi mọi bản cho 1/1 ở thời điểm đo. `python3 -B ops/lease_publish.py check ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml` trong `cay-kho/`: rc=0, ĐĂNG ĐƯỢC. Dữ liệu và các ref/blob nằm trong `do-review10/snapshot.json`; lệnh check có stdout/metadata riêng. Không gọi `ai-dang-giu` CLI vì đường ấy đối chiếu mạng; phép quét ở đây chỉ chứng nhận snapshot offline.

ĐỘ TIN: cao về snapshot và mô hình thời gian; trạng thái máy chủ trực tiếp, kể cả sau 14:30:07Z, KHÔNG ĐO ĐƯỢC.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  Lease r4 còn gọi đối chiếu khác lane là đối chiếu nhiễu

TỆP/DÒNG: `ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml:162–164`; đối chiếu spec r4 `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:11–14`, `:103–107`, `:455–457`, `:540–542`, `:628–634`.

VẤN ĐỀ: Toàn văn spec r4 và Issue #463 đã sửa đúng các câu của lượt9: mẫu được gọi đúng 5 master + 6 nhánh, hai run lịch sử khác event/lane, biên A1/A5 là thiết kế, không còn cho nới theo nhiễu được cho là đã đo. Nhưng lease r4 MỚI CẤP vẫn giao việc tính billing với “lượt master 34048685345 = 111,08 để đối chiếu nhiễu”. Câu này là một phần của `viec_trong_lease`, không phải chú thích lịch sử. Nó tiếp tục gán ý nghĩa nhiễu cho phép so mà chính spec r4 đã bác. Giữ P2 vì A1 ≤ 25,00 và A5 ≤ 135,00 không bị nới; đây là sai nghĩa và mâu thuẫn giữa hai phần hợp đồng. EVIDENCE bỏ sót câu này.

ĐÃ THỬ VÁ: Có, thử thay đúng một mỏ neo trong bản sao văn bản ngoài checkout: gọi run master là đối chiếu lịch sử, nói rõ cùng tree nhưng khác event/lane và chưa tách phần runner. Chỉ một mục `viec_trong_lease` đổi; ngưỡng 135,00, băm spec/write set, authority, mốc và chuỗi thay thế đều giữ nguyên trong thử nghiệm. Ca khóa: parse YAML rồi kiểm mục billing không còn “đối chiếu nhiễu”; quét và đọc ngữ cảnh toàn spec/Issue/lease hiện hành, xác nhận hai ngưỡng giữ nguyên. Rủi ro: chỉ xóa chữ ở spec lại sót lease; không sửa các lease r1/r2/r3 đã thành lịch sử để che dấu lời khai cũ. Executor tự quyết và ghi audit phù hợp cho thay đổi lease đã cấp. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/prose_checks.py` rc=0. Dữ liệu lưu trong kho cho `426bfc0`/`1b3caa1`: tree bằng nhau, 0 path đổi; một run `workflow_dispatch` trên nhánh, một `push` trên master. Hai tập đều 86 bộ ba nhưng có 4 thêm/4 mất ở release-verify WORKER/LAND. Chênh job Windows 0,916667 phút và ubuntu 2,266667 phút khớp số làm tròn, không xác định được thành phần do runner. Mô hình sửa có 1 neo duy nhất và 1 mục YAML đổi. Hiện vật: `do-review10/prose-checks.json`, `gate-prose-scan.txt`, `prose-experiment/`. Không chạy hay tạo bản vá workflow/gate.

ĐỘ TIN: cao về câu lease và sự khác event/lane; nhiễu runner riêng KHÔNG ĐO ĐƯỢC từ mẫu này.

### manifest-luot8-liet-ke-hien-vat-khong-duoc-giao  [P2]  Lượt8 đã đủ nhưng gói lượt9 lại thiếu 19 tệp đã phục dựng

TỆP/DÒNG: `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/ARTIFACTS.sha256:48–66`; `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-checks.json:2–7`; `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact_checks.py:10–17`; `EVIDENCE.md:12` của bundle giao reviewer.

VẤN ĐỀ: Gói lượt8 hiện kiểm đủ 69/69, nhưng phần `artifact-repair/` do reviewer lượt9 tạo lại mất cả 19 tệp `rig/do-review/` và `rig/source/` khi được chép vào gói lượt9. Manifest con vẫn cam kết những tệp ấy; script và kết quả lịch sử xác nhận reviewer đã phục dựng và chạy rc=0. Chạy trên gói đã giao nay rc=1, chỉ 50/69. Con số “111 tệp” trong EVIDENCE đúng số tệp hiện có nhưng không chứng minh chép đủ: ít nhất 19 tệp đã tạo còn thiếu. Giữ nguyên slug vì cùng lỗi bàn giao theo manifest tái phát trong gói kế tiếp. Không nâng P1 mất bằng chứng H: toàn bộ 19 tệp có bản đúng hash ở gói lượt8 đã sửa.

ĐÃ THỬ VÁ: Có, dựng lại gói con ngoài checkout trong `do-review10/artifact9-repair/`: giữ nguyên 50 tệp có sẵn và manifest, bổ sung 19 tệp thường có hash khớp từ gói lượt8. Executor có thể bổ sung đúng byte đã cam kết vào gói lượt9. Ca khóa: `sha256sum -c ARTIFACTS.sha256` phải rc=0 cho cả gói lượt8 và manifest con gói lượt9; so tập đường dẫn trước/sau sao chép, loại tmp/symlink theo thành phần đường dẫn tương đối, không bỏ cả thư mục `rig/`. Rủi ro: chỉ xóa dòng manifest sẽ làm mất chứng cứ lịch sử; chép theo tên mà không so hash có thể trộn các lượt khác nhau. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/artifact_checks.py` rc=0; chương trình gọi `sha256sum -c ARTIFACTS.sha256` thật ở từng gói. Lượt6: 62/62 rc=0; lượt7: 66/66 rc=0; lượt8: 69/69 rc=0; lượt9/artifact-repair: 50/69 rc=1. Gói lượt9 có 111 tệp thường và 0 symlink. Tìm được 19/19 nguồn đúng hash trong lượt8; bản sao phục dựng kiểm 69/69 rc=0. Ánh xạ từng đường và hash nằm trong `do-review10/artifact-checks.json`; stdout/stderr của mỗi phép kiểm được lưu. Không sửa checkout và không khai đã chạy lại suite H.

ĐỘ TIN: cao.
