verdict: changes_requested
reviewed_sha: ba4a258d4e7d13ce8630c94023ae2cbeedb2fb3a

## BẢNG ĐO

Reviewer độc lập theo chỉ thị lượt 1; tự khai model GPT-6, provider OpenAI, bề mặt Codex/API có shell cục bộ, transport machine. Không có chứng thực độc lập model/build. Không truy cập mạng, không thao tác kho thật. Tree đã đo: `a80a73d6b0af958878e96187508a2edd614f22a2`. Mọi đường dẫn dưới đây tính từ thư mục làm việc; đường dẫn `ops/...`, `CHANGELOG.md` và `CLAUDE.md` trong finding tính trong `cay-kho/` nếu không nói khác.

“Khớp nguồn thuật lại” KHÔNG có nghĩa đã tái đo sự kiện lịch sử. Các số Git, byte, JSON, kết quả chạy cổng dưới đây được tự đo. Sự kiện GitHub không có response gốc được ghi KHÔNG ĐO ĐƯỢC. Timestamp commit không được dùng làm thời điểm push hay xác nhận thẩm quyền.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| SHA và phạm vi PR | head ba4a258, 2 tệp, không mã chạy được đổi | `git rev-parse HEAD`; `git diff --numstat c0a5cbe..HEAD`: CHANGELOG +112/−0, manifest +5/−5; đúng 2 tệp | Có |
| Tính toàn vẹn gói review | ARTIFACTS.sha256 | Python tự băm 3190 mục: 3190 khớp, 0 lệch, 0 đường dẫn resolve ngoài workspace | Có |
| Ref trong ảnh chụp | 316 nhánh | `for-each-ref refs/heads`: mirror 316, cây 316; so tập tên+OID với nguon-refs.tsv: 0/0 lệch | Có; không xác thực lại máy chủ |
| Tổng tệp chuỗi | 1016 | `git diff --shortstat b416830..c0a5cbe`: 1016 | Có |
| Tổng dòng thêm chuỗi | 247458 | Cùng lệnh: 247458 insertions, 0 deletions | Có |
| Thư mục cấp 1 | đúng một, ops | `git diff --name-only b416830..c0a5cbe` rồi lấy thành phần đầu: tập {ops}, cỡ 1 | Có |
| Lệnh in trong mục Phạm vi dòng 12 | lệnh không ghi khoảng SHA ⇒ ops | `git diff --name-only` trên exact head sạch trả chuỗi rỗng; thêm khoảng b416830..c0a5cbe mới ra ops | Không |
| Số PR trong chuỗi | “tám” | 7 mã PR khác nhau; `git rev-list --count --first-parent b416830..c0a5cbe` = 7 | Không |
| Merge #468 | 802fc01 | `git log -1 --oneline 802fc01`: Merge pull request #468 | Có |
| Merge #477 | 585c7d5 | Cùng phép đo: #477 | Có |
| Merge #478 | c87b067 | Cùng phép đo: #478 | Có |
| Merge #486 | da481f9 | Cùng phép đo: #486 | Có |
| Merge #480 | 7e69b8e | Cùng phép đo: #480; sau #486 trên first-parent | Có trong bảng; chuỗi mũi tên đặt ngược hai PR |
| Merge #487 | f4d74fe | Cùng phép đo: #487 | Có |
| Merge #489 | c0a5cbe | Cùng phép đo: #489 | Có |
| Bốn đặc tả của #468 | bốn | Diff b416830..802fc01 trong ops/specs có đúng 4 tệp; ops/issues có 4 tệp tương ứng #463–#466 | Có; trạng thái Mission #467 trên GitHub KHÔNG ĐO ĐƯỢC |
| Hiện vật năm lượt trong #487 | 5 lượt | Diff f4d74fe^1..f4d74fe thêm 5 verdict.md và 5 receipt tương ứng: #480×2, hậu kiểm #486×1, #487×2 | Có; không phải 5 lượt review riêng PR #487 |
| ops/land hiện tại | 6 tệp | Liệt kê tệp trực tiếp: plat-x8, pr468, pr477, pr478, pr480, pr487; đúng 6 | Có |
| Chuỗi đóng ở #490 | đã đóng | Có commit a48f576 ghi quyết định trong ops/land/pr489-land-evidence.yaml trên nhánh khác; HEAD chưa có tệp này. Quyết định/PR GitHub hiện tại KHÔNG ĐO ĐƯỢC offline | Chỉ có hồ sơ thuật lại |
| Không nâng VERSION | 1.36.68, từ r336 | VERSION tại 3dcdc6a, b416830, c0a5cbe, HEAD đều 1.36.68; `git log 3dcdc6a..HEAD -- VERSION` rỗng | Có |
| Tiền lệ ghi sổ | r354, r355, r356 | Có đủ ba mục ở CHANGELOG:846,208,113; nói về manifest, receipt v2, fixture dev-side | Có |
| Chuỗi chưa có mục ghi sổ | chưa có mục nào | CHANGELOG ở c0a5cbe không có mã #468/#477/#478/#480/#486/#487/#489; CHANGELOG không đổi trong b416830..c0a5cbe | Có trong phạm vi chuỗi đo |
| r357 đã được dùng, tiền lệ va chạm | #472; bc78656 | Nhánh claude/agents-ngoai-goi có d3aaba5 và 0e00d85 mang r357 trong commit; bc78656 đúng thông điệp đổi r355→r356. Liên kết PR #472 không có response để xác thực | Khớp phần Git; số PR KHÔNG ĐO ĐƯỢC |
| Kiểm kê gói | 180/180 | JSON manifest có 180 files; release-verify checked=180, expected=180 | Có |
| ops bị loại từ r336 | 0 mục | Manifest tại 3dcdc6a có 179 mục tổng, 0 ops; tại b416830/c0a5cbe/HEAD có 180 tổng, 0 ops | Có; không gán 180 ngược về r336 |
| Gói không đổi trong chuỗi b416830..c0a5cbe | không đổi | Hai manifest cùng blob `2c0dec66fcd12076c155842b1b80b8d5501c844a`; mọi thay đổi chỉ thuộc ops, 0 ops trong manifest | Có, chỉ cho chuỗi trước PR #491 |
| Gói thay đổi do chính PR #491 | hash bcde19d5… → 1513d58d… | Đọc manifest base/head khớp hai hash; total_bytes 8075509→8083189, tăng 7680; CHANGELOG 781187→788867, tăng đúng 7680 | Có |
| release-verify hiện tại | ok true, failed [], package_hash_match true | Chạy thật rc=0, ok=true, failed=[], package_hash_match=true, package_hash_self_match=true | Có |
| Các tập thiếu/thừa/lỗi | đều [] | extra_files=[], missing_from_current_manifest=[], required_missing=[], errors=[] | Có |
| Răng cổng kiểm kê | sửa CHANGELOG phải đỏ | Đổi một byte ASCII dev-side→dev-sidE, giữ nguyên kích thước 788867: rc=2, ok=false, failed có CHANGELOG, package_hash_match=false; khôi phục rc=0, ok=true | Có, đã giết đột biến |
| doc-claims-check --strict | rc=0, ok=true | Chạy thật rc=0, ok=true, 106 tệp, 367 advisory, flags=[] | Có |
| Cổng văn bản có kiểm số thống kê này không | PR chỉ khai xanh | Đột biến mọi 1016 trong mục mới thành 1017: doc-claims-check vẫn rc=0, ok=true | Không kiểm sự thật của số này; không coi đây là lỗi của release-verify |
| Bộ lease có actionlint | 121/121, chạy 121, bỏ 0, rc=0 | Chạy nguyên suite với thư mục actionlint có sẵn trên PATH và TMPDIR trong workspace: đúng toàn bộ, exit 0 | Có |
| Bộ lease cũ thiếu actionlint | 120/121, rc=1 | Hai nen/sau.lease.norm.out cũ đều ghi 120/121, chạy 121, bỏ 0; *.rc ghi 1. Không khôi phục được exit status lịch sử từ tiến trình cũ | Khớp log; lịch sử chỉ đọc hiện vật |
| t33 assertion trước subprocess | dòng 1359–1363 trước 1364 | Đọc AST/mã: đúng. Gọi nguyên t33, mock shutil.which=None và đếm subprocess.run: AssertionError, 0 lời gọi subprocess | Có, đã chạy phản chứng |
| Log lease lịch sử sau cài | 121/121 ở hai vế | Hai tệp nen/sau.lease-sau-cai-actionlint.out trong ops/reviews/log-t33-20260907 đều 8649 B, tổng kết 121/121, đã chạy 121, bỏ qua 0 | Có về byte/nội dung log; exit status lịch sử vẫn là thuật lại |
| Cài actionlint lịch sử bằng installer và băm | 1.7.7, kiểm băm | Binary hiện có tự báo 1.7.7; DO-T33-VA-GOI-REVIEW-20260907.md:34–37 nói thiếu log installer/băm archive. Quá trình cài lịch sử KHÔNG ĐO ĐƯỢC | Phiên bản khớp; provenance chưa xác thực |
| actionlint và shellcheck hiện tại | công cụ dùng được | Gọi actionlint tuyệt đối trên ops-publish-lease.yml và /usr/bin/shellcheck trên dung_goi_review.sh: cả hai rc=0 | Có |
| Cổng receipt v2 | 0 vi phạm, TỔNG ĐẠT | rc=0; 41 đạt v2 + 11 miễn trừ + 42 nợ = 94; 0 vi phạm, 0 không đo được | Có |
| “cài công cụ bằng bản ghim” | nói chung cho các công cụ | Script chỉ ghim actionlint=1.7.7; shellcheck/git/python3 lấy type -P và chạy --version, không so phiên bản ghim | Phạm vi khai quá rộng |
| AL_VER rỗng/sai, thiếu shellcheck | rc=4 | Mã có chốt; bảng lịch sử có lời thuật lại. Không chạy lại toàn quy trình vì cần clone/cài; không truy cập mạng | KHÔNG ĐO ĐƯỢC hành vi đầy đủ ở lượt này |
| Remote trùng git template | rc=5 | Mã có chốt rename/add; không có transcript thực thi đầy đủ được tái chạy tại lượt này | KHÔNG ĐO ĐƯỢC |
| Thay mirror bằng single-branch | rc=6, mirror=1, lệch 304/304 | Số lịch sử không được suy từ snapshot 316 nhánh hiện tại. Không tái dựng đúng nguồn lịch sử và phép thử cũ | KHÔNG ĐO ĐƯỢC; không đổi 304 thành 316 |
| cong-cu symlink, sentinel | rc=4, sentinel còn | Đọc được chốt -L; không tự soạn phép thử đường dẫn theo ràng buộc người dùng | KHÔNG ĐO ĐƯỢC động; chỉ kiểm mã |
| Tái dùng R đã dựng | rc=4, manifest còn nguyên | Chạy dung_goi_review.sh với chính thư mục gói đã có: rc=4, từ chối trước ls-remote; manifest đã băm khớp, không bị sửa | Có |
| actionlint giả 0.0.0-GIA, exit 42 | script rc=0, dùng 1.7.7 | Mã gọi binary cài theo đường tuyệt đối; không tái dựng probe lịch sử, không chạy installer qua mạng | KHÔNG ĐO ĐƯỢC động |
| Ba lượt sửa sót t33 | ba lượt liền | HEAD vẫn có câu “KHÔNG CHẠY” trong DO-T33…:9 và dung_goi_review.sh:33; bảng DO-T33 đã nói ĐỎ. Số đúng ba lượt cần verdict gốc #477, nguồn land khai thiếu lượt cuối | Đo được sót; đúng ba lượt KHÔNG ĐO ĐƯỢC |
| CLAUDE.md có hai endpoint/44 tool | dòng 583 | Mở đúng dòng 583–585 có /mcp/, 44 công cụ, /mcp/x/actions | Có nội dung dẫn; số công cụ máy chủ KHÔNG ĐO ĐƯỢC |
| CI Ubuntu của 585c7d5 | success, 44 bước, 0 hỏng, 26:46 | Hồ sơ pr477 ghi 01:22:44→01:49:30; tự trừ =1606s=26:46. Không có API response để đếm độc lập bước/status | Số học khớp; sự kiện KHÔNG ĐO ĐƯỢC |
| CI Windows của 585c7d5 | success, 44 bước, 0 hỏng, 48:15 | Hồ sơ ghi 01:22:45→02:11:00; tự trừ =2895s=48:15; status/số bước là thuật lại | Số học khớp; sự kiện KHÔNG ĐO ĐƯỢC |
| Trần và biên Windows | 60 phút, còn 11:45 | ci.yml:64 timeout=60; 3600−2895=705s=11:45 | Có số học trên thời lượng được khai |
| Issue #463 nhằm tách job, không tăng trần | đúng hướng này | Mở ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md: tiêu đề và phần mở đầu ghi đúng | Có nội dung nguồn |
| Cặp CI trước/sau | 43/1→44/6 | pr477-land-evidence.yaml:158–176 chỉ gọi là cặp thuật lại, thiếu response để kiểm cùng job/attempt. Tự tính delta: số bước +1, skipped +5 | Khớp phép trừ, KHÔNG ĐO ĐƯỢC số hạng lịch sử |
| Nguyên nhân mâu thuẫn 4/6 | vì đọc job in_progress | Nguồn pr477:167–179 và pr468:163–223 nói chưa xác định; cặp 43/1 thuộc run khác, không phải mẫu 43/4 đang tranh cãi | Không |
| _kiem_bia_mo vẫn any | any(...) | ops/lease_publish.py:605–610 còn đúng any; không có thay đổi mã này trong PR #491 | Có |
| Một bản sao có bia mộ đủ cho check | rc=0 | any bỏ qua bản sao khác cùng lease_id chưa bia mộ; đây chỉ là điều kiện vượt _kiem_bia_mo, không bảo đảm mọi kiểm tra khác của check đều qua | Khớp ở điều kiện hàm; rc toàn lệnh có điều kiện |
| Đặc tả thu hồi hiện tại | revision 6, packet_issue CHƯA CÓ | Ref đầy đủ trong gói tip bd32d114…: spec revision 9, packet_issue “neo ở Issue”; có hiện vật luot8-VERDICT nói hồ sơ Issue #488 | Không; trạng thái Issue GitHub vẫn KHÔNG ĐO ĐƯỢC |
| Review budget/bước kế của đặc tả | hết 6/6, chờ Rescue Checkpoint | Spec hiện hành ghi checkpoint reroute ngày 08-09; hiện vật lượt 8/lời gọi 9, 0 P1 và S11/P2. Trần 6/6 là mốc r6 tại 2aee80a, không phải hiện trạng | Không |
| Bốn lease A9 | bốn thời điểm nêu trong PR | Đọc YAML: 03:37:33, 07:50:35, 09:44:51, 10:17:12 ngày 07-09; cả 4 trước 14:30:07 cùng ngày trong lease tiền nhiệm #456 | Có |
| A9 revision/generation/spec_hash | revision 1/2/3/4; generation 1; 4 hash khác nhau | Safe-load 4 YAML: đúng 1/2/3/4, tập generation={1}, 4 hash khác nhau (8cca700c…, bda86f12…, 37800aa6…, 4c542f6b…) | Có |
| Đổi contract cần revision/generation mới | ADR-0034 | Đọc docs/adr/0034-governance-change-control-review-land-authority.md:7–8 có đúng “Packet đổi contract phải revision + generation mới”; nợ A9 còn được nguồn land ghi. Không xác thực quyết định xử lý mới trên GitHub | Khớp nội dung quy tắc; quyết định KHÔNG ĐO ĐƯỢC |
| Issue #463–#467 hiện open | 5 issue open | Snapshot mã không chứng minh trạng thái GitHub hiện tại; không gọi API theo ràng buộc | KHÔNG ĐO ĐƯỢC |
| PR #479 chưa merge | chưa merge | Có commit sửa b789e73, HEAD vẫn giữ phần cũ; không có response GitHub PR #479. Không suy trạng thái PR từ việc mã chưa vào HEAD | KHÔNG ĐO ĐƯỢC trạng thái GitHub |
| Hai P3 #479 đều về hợp đồng đầu vào | “hai P3 tự khai hợp đồng đầu vào” | Nguồn pr477:197–202 liệt kê 1 P3 về mở đầu t33, 1 P3 về giới hạn dựng gói; b789e73 sửa cả hai nội dung | Không đúng phân loại; số hai theo hồ sơ |
| Ba công cụ tin PATH, bản giả 9.9.9 | 3; rc=0 | Đếm vòng for: shellcheck, git, python3 đúng 3; không ghim. Phiên bản giả/rc là lời thuật lại trên b789e73, chưa chạy probe đó | Khớp mã, KHÔNG ĐO ĐƯỢC probe lịch sử |
| R chính nó không được kiểm; hai sentinel mất | 2 sentinel bị xóa | Đọc script có 2 lệnh xóa thư mục con, chỉ kiểm symlink các con; không có chốt R. Không tự dựng payload; không chạy ca xóa này | Khớp phạm vi mã; hậu quả động KHÔNG ĐO ĐƯỢC |
| Không đo macOS/Windows native | chưa có | Nguồn b789e73 ghi giới hạn Linux+Bash cho probe dựng gói; lượt này cũng chỉ Linux. Không thể chứng minh phủ định toàn lịch sử nền chạy | KHÔNG ĐO ĐƯỢC toàn cục; khớp tự khai có phạm vi |
| Hơn 20 finding | >20 | Chỉ 3 verdict pr487 lượt 1/2 + hậu kiểm pr486 đã có 33 tiêu đề, 28 slug khác nhau; không cần cộng lặp toàn chuỗi | Có cận dưới >20; “gần như tất cả” chưa có tiêu chí phân loại |
| Năm hình dạng lỗi | 5 | Mục mới có danh sách đánh số 1–5 | Có về danh sách, không phải phân loại độc lập toàn bộ finding |
| Bản vá sinh lỗi mới sáu lần | 6 lần | Đếm được 6 mục trong chuỗi kể; pr477-land-evidence:79 nói rõ không phải 6 lần tái hiện độc lập | Khớp số mục thuật lại; KHÔNG ĐO ĐƯỢC 6 sự kiện độc lập |
| Chỉ 1/6 stdout có thể tự đếm | 1/6 | Mỗi vế: doc JSON 70861 B nguyên vẹn; cidk chỉ 206 B tail, ploop 96 B tail, lease 8827 B đã normalize; doctrine/adr không có stdout. Đúng 1 loại nguyên vẹn trong 6 loại | Có trong phạm vi full-gate lịch sử |
| land_operator sai người so merged_by | ducthangho / notebyme88 | Có đính chính trong hồ sơ; Git không xác thực trường merged_by và không phân biệt UI/API | KHÔNG ĐO ĐƯỢC danh tính sự kiện độc lập |
| Một slug qua bốn lượt do sửa sót khung | 4 lượt | Hồ sơ kể lại, các bản giữ nợ và sửa khung còn có trong Git; chưa lập đủ chuỗi 4 verdict gốc #477 để xác thực số lần | KHÔNG ĐO ĐƯỢC đúng số 4 |
| Luật ít nhất HAI client | 2 | CLAUDE.md:580–581 đúng nguyên văn “thử ít nhất hai client…” | Có nội dung nguồn |
| run.json chỉ có ba trường | chuong_trinh, so_doi_so, van_tay | JSON lượt 14 và 15 đều có 35 khóa cấp cao; CHỈ object lenh có đúng 3 khóa đó; không có model ID trực tiếp | Không về cấu trúc; đúng việc không chứng minh model |

Các phép chạy dùng `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --deterministic --json`, `python3 -B scripts/tl.py doc-claims-check --strict --json`, `python3 -B ops/bien_nhan_v2.py` trong cay-kho. Suite lease chạy từ workspace với `TMPDIR="$PWD/review-tmp" PYTHONDONTWRITEBYTECODE=1 PATH="$PWD/cong-cu/actionlint.RIbENT:$PATH" python3 -B cay-kho/ops/lease_publish_test.py`. actionlint được gọi trực tiếp bằng đường tuyệt đối được giao khi lint riêng. Đã lấy mã thoát thật của suite: 0. Đột biến dùng try/finally khôi phục byte gốc; `git -C cay-kho status --short` cuối lượt rỗng.

Bộ lọc giữ dòng, không giữ mệnh đề. Không tính “không nâng VERSION”, “đúng một thư mục cấp 1”, “chưa có mục nào”, “tám PR” là bỏ sót: chúng đều nằm trên dòng có số và ĐÃ có trong bảng giao. Tương tự “ba lượt” dòng 59 lặp ý đã được giữ ở dòng 56. Các finding bỏ sót thực sự bên dưới dựa trên dòng thiếu và nội dung thiếu, không dựa đơn thuần vào chữ viết bằng chữ.

### chuoi-tam-pr-thuc-te-bay  [P1]  Câu mở đầu đếm sai số PR và đảo thứ tự hai merge
TỆP/DÒNG: CHANGELOG.md:3–4; than-pr-491.md:3.
VẤN ĐỀ: “tám PR” trái cả danh sách 7 mã lẫn Git first-parent 7 merge. Mũi tên còn đặt #480 trước #486, trong khi Git và chính bảng Chuỗi merge đặt #486 trước #480. Đây là số sự kiện sai trong một PR ghi sổ.
ĐÃ THỬ VÁ: không — đổi “tám” thành “bảy” ở cả hai nơi và thống nhất thứ tự #468→#477→#478→#486→#480→#487→#489. Không thêm #490 cho đủ tám: nó nằm ngoài khoảng đã đo.
ĐÃ THỬ NGHIỆM: `git -C cay-kho rev-list --count --first-parent b416830..c0a5cbe` = 7; `git log --first-parent --oneline` cùng khoảng cho đúng thứ tự trên. Sau vá kiểm lại cả mở đầu/bảng/thân PR; tái sinh manifest vì đổi CHANGELOG, tránh tự làm lệch băm gói.
ĐỘ TIN: cao

### no-thu-hoi-lease-dang-chep-trang-thai-cu  [P1]  Revision 6 và checkpoint 6/6 đã cũ trước khi PR được tạo
TỆP/DÒNG: CHANGELOG.md:80–81; phần Nợ trong than-pr-491.md.
VẤN ĐỀ: Lời khai hiện tại lấy mốc `2aee80a2ff6a088ff39a2a8bc882db978df64c75` (07-09). Nhưng ref `claude/spec-thu-hoi-lease-va-cap-lai-20260907` trong chính gói có tip `bd32d1145a4b890da695dc56196997b582c5be1e` (commit 09-09 11:23:01Z, trước head PR 16:10Z), spec revision 9. Spec:45–48 thuật lại checkpoint/reroute 08-09; `ops/reviews/thu-hoi-lease-va-cap-lai-spec/luot8-VERDICT.md` là lượt 8/lời gọi 9, 0 P1, còn S11/P2 về hồ sơ Issue #488. Nguồn hiện hành `ops/land/pr477-dung-goi-review-land-evidence.yaml:211–214` đã gọi r6 là MỐC LỊCH SỬ; r358 bỏ chính giới hạn đó. Câu cũ khiến người đọc chọn sai bước tiếp theo.
ĐÃ THỬ VÁ: không — đường ít rủi ro nhất là ghi rõ “tại 2aee80a ngày 07-09…” và bổ sung trạng thái theo snapshot bd32d114, tách lời thuật lại thẩm quyền khỏi Git đo được. Không tự khẳng định Issue đã ready/cấp lease hoặc r9 approved: verdict mới vẫn changes_requested vì P2.
ĐÃ THỬ NGHIỆM: `git show refs/heads/claude/spec-thu-hoi-lease-va-cap-lai-20260907:ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` trả revision 9, không còn packet_issue CHƯA CÓ; `git show bd32d114:ops/reviews/thu-hoi-lease-va-cap-lai-spec/luot8-VERDICT.md` xác nhận lượt/lời gọi và kết quả. Kiểm sau vá phải so từng số hạng revision/budget/bước kế ở cả CHANGELOG và thân PR; không chỉ kiểm any vẫn còn. Tái sinh manifest.
ĐỘ TIN: cao

### ci-gia-thuyet-bi-viet-thanh-nguyen-nhan  [P1]  R358 khôi phục kết luận nguyên nhân đã bị nguồn rút lại
TỆP/DÒNG: CHANGELOG.md:61,71–74; đoạn “Một phép đo SAI…” trong than-pr-491.md.
VẤN ĐỀ: R358 nói “Nguyên nhân” của mâu thuẫn 4/6 là job in_progress, rồi dùng cặp 43/1→44/6. Nguồn pr477-land-evidence.yaml:140–183 tách rõ (a) số thuật lại, (b) mẫu từ run KHÁC, (c) nguyên nhân cũ CHƯA BIẾT. Run tranh cãi là 34169756563 trên 802fc01; cặp trước/sau thuật lại thuộc 34176439015 trên 585c7d5. Số 1 không phải 4. Nguồn còn giữ đối thủ: đọc Ubuntu 44/4 rồi ghi nhầm 44 thành 43 cũng ra 43/4. Giữ quan hệ delta đúng không xác thực các số hạng, danh tính job hoặc nguyên nhân.
ĐÃ THỬ VÁ: không — đổi cả tiêu đề/câu dẫn thành “số đã đính chính, nguyên nhân chưa xác định”; gắn cặp trước/sau với run riêng và nhãn thuật lại. Giữ bài học chỉ chốt kết quả khi completed; không nói bài học ấy chứng minh sự kiện cũ. Nguy cơ vá: chỉ sửa thân rồi vẫn giữ khung “đã tự bắt được” như đã giải xong.
ĐÃ THỬ NGHIỆM: Mở pr477:140–183 và pr468-land-evidence:163–223; tính 44−43=1, 6−1=5 và (44,4)+(−1,0)=(43,4). Không có response trước/sau hoặc thời điểm gọi API cũ để chọn nguyên nhân: KHÔNG ĐO ĐƯỢC nguyên nhân lịch sử. Sau vá đối chiếu cả tiêu đề, câu mở, số run và thân PR; tái sinh manifest.
ĐỘ TIN: cao

### ghim-cong-cu-khai-rong-va-bi-bo-loc-bo-sot  [P2]  Phần giới thiệu nói ghim công cụ trong khi chỉ ghim actionlint
TỆP/DÒNG: CHANGELOG.md:37–38 so với :87–89; trich_khang_dinh.py, bộ lọc regex chữ số.
VẤN ĐỀ: “cài công cụ bằng bản ghim của kho” không giới hạn vào actionlint. Chính phần Nợ và script:167–179 cho thấy ba công cụ còn lại lấy từ PATH, không kiểm phiên bản ghim. Đây là lặp kiểu sửa thân nhưng giữ lời giới thiệu rộng hơn bằng chứng. Dòng 38 không có chữ số nên bảng giao bỏ hoàn toàn khẳng định này.
ĐÃ THỬ VÁ: không — sửa ngay câu giới thiệu thành “cài actionlint theo bản ghim; tìm và kiểm chạy được shellcheck/git/python3 trên PATH đầu vào”. Thêm dòng này vào bảng mệnh đề thủ công. Không biến “chạy được” thành “đúng phiên bản/nguồn gốc”.
ĐÃ THỬ NGHIỆM: Đọc vòng for ba tên và phép so phiên bản chỉ dành cho actionlint trong ops/dung_goi_review.sh. Chạy lại regex trên muc-r358.md xác nhận dòng 38 vắng. Kiểm sau vá đối chiếu ba vị trí: giới thiệu, Nợ, mã script; tái sinh manifest.
ĐỘ TIN: cao

### lenh-pham-vi-thieu-hai-moc  [P2]  Lệnh được trình bày như phép đo không tạo ra kết quả được ghi
TỆP/DÒNG: CHANGELOG.md:12; than-pr-491.md phần Phạm vi.
VẤN ĐỀ: `git diff --name-only` đo thay đổi chưa stage, không kế thừa khoảng SHA từ lệnh shortstat trước đó. Trên bản sao sạch nó trả rỗng, không phải ops. Dòng lệnh này còn bị bảng regex bỏ vì không có số; số thư mục ở dòng 15 vẫn được giữ, nên đây là bỏ phương pháp đo chứ không bỏ kết quả định lượng.
ĐÃ THỬ VÁ: không — thêm b416830..c0a5cbe vào đúng lệnh ở cả hai nơi. Không đổi khoảng theo HEAD vì chính PR #491 chạm CHANGELOG và manifest ở cấp gốc.
ĐÃ THỬ NGHIỆM: Chạy hai biến thể trên cây sạch: bản in nguyên văn trả chuỗi rỗng; bản có khoảng trả đúng tập {ops}. Sau vá chạy lại nguyên khối được in; tái sinh manifest.
ĐỘ TIN: cao

### run-json-ba-khoa-chi-dung-cho-lenh  [P2]  Đính chính việc dẫn nguồn lại mô tả sai cấu trúc chính nguồn đó
TỆP/DÒNG: CHANGELOG.md:109–111.
VẤN ĐỀ: Câu “run.json chỉ có chuong_trinh, so_doi_so, van_tay” sai. Cả run.json lượt 14 và 15 của PR468 có 35 khóa cấp cao, gồm provider, execution_surface, transport, head, trạng thái và các số stdout/stderr. Ba khóa được kể chỉ thuộc `lenh`. Điều đúng cần giữ: hiện vật đó không chứa argv/model ID để chứng minh cờ -m cụ thể.
ĐÃ THỬ VÁ: không — thay bằng “object lenh trong run.json chỉ lưu …, không lưu argv/model được yêu cầu”. Đừng nâng provider/transport tự khai thành chứng thực model độc lập; đó là rủi ro khi chữa câu này quá tay.
ĐÃ THỬ NGHIỆM: json.load hai tệp `ops/reviews/pr468-hoso-4-packet-review-{14,15}-codex/run.json`: len(d)=35; set(d['lenh']) đúng ba tên; không có khóa model cấp cao. Sau vá đối chiếu đúng object, tái sinh manifest.
ĐỘ TIN: cao

### hai-p3-khong-cung-la-hop-dong-dau-vao  [P2]  Tóm tắt gộp sai hai nội dung của PR479
TỆP/DÒNG: CHANGELOG.md:87; than-pr-491.md dòng cuối phần Nợ.
VẤN ĐỀ: Nguồn pr477-land-evidence.yaml:197–202 liệt kê hai slug: t33-khong-chay-van-con-o-mo-dau và gioi-han-dung-goi-chua-tu-khai. Một mục sửa lời mở đầu phủ nhận t33 đã chạy, một mục tự khai hợp đồng đầu vào. Không phải cả hai đều là “hai P3 tự khai hợp đồng đầu vào”.
ĐÃ THỬ VÁ: không — gọi tên hai nội dung riêng, giữ nhãn “theo hồ sơ điều phối” cho số hai vì thiếu verdict gốc lượt 6. Không tự xác nhận trạng thái PR479 trên GitHub bằng Git local.
ĐÃ THỬ NGHIỆM: `git show b789e73 --stat` cho 2 tệp +57/−5; đọc diff và nguồn land xác nhận sửa t33 và bổ sung hợp đồng. Verdict gốc #477 lượt 6 và trạng thái PR GitHub: KHÔNG ĐO ĐƯỢC từ nguồn đã có. Sau vá rà cả thân PR và CHANGELOG, tái sinh manifest.
ĐỘ TIN: cao

### so-lich-su-bi-mat-nhan-nguon  [P2]  Các số thuật lại được trình bày thành bằng chứng trực tiếp
TỆP/DÒNG: CHANGELOG.md:40–54,65–66,95,104–108.
VẤN ĐỀ: R358 bỏ các giới hạn nguồn đã có trong hồ sơ. DO-T33-VA-GOI-REVIEW-20260907.md:34–37 nói rõ thiếu transcript exit status, log installer, băm archive. pr477-land-evidence.yaml:79 nói SÁU MỤC được điều phối kể, không phải sáu lần tái hiện độc lập; phần :140–183 nói thiếu response CI. R358 lại dùng “được chứng minh CHẶN”, “Cài … đối chiếu băm ⇒”, “Merge commit … đo THEO JOB”, “SÁU lần” mà không giữ nhãn này. Chạy xanh hôm nay không khôi phục được sự kiện trước kia. Cận dưới >20 finding đo được, nhưng “gần như tất cả” chưa có tiêu chí phân loại.
ĐÃ THỬ VÁ: không — giữ số lịch sử, thêm nguồn/mốc/phạm vi cho từng nhóm: tự tái đo, nguyên liệu lưu đủ, hoặc điều phối thuật lại. Đổi “sáu lần” thành “sáu mục lỗi được hồ sơ kể lại”. Không thay số cũ bằng số mới 316 ref hay receipt 94: như vậy sẽ tự viết lại lịch sử.
ĐÃ THỬ NGHIỆM: Đã tái chạy lease 121/121, chốt tái dùng gói rc=4, lint rc=0; các probe lịch sử còn lại ghi KHÔNG ĐO ĐƯỢC ở bảng. Tự tính thời lượng từ timestamp chỉ kiểm số học, không kiểm event/job. Đếm 6 mục kể và 28 slug phân biệt trong 3 verdict làm cận dưới. Sau vá đối chiếu nhãn ở cả tiêu đề/bảng/thân PR; tái sinh manifest.
ĐỘ TIN: cao về việc mất giới hạn nguồn; vừa về khả năng còn hiện vật lịch sử chưa được định danh trong toàn bộ object store

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Bảng chữ số bỏ khẳng định độ phủ ref
TỆP/DÒNG: CHANGELOG.md:37; trich_khang_dinh.py.
VẤN ĐỀ: Dòng “clone mirror đủ mọi ref, vật chất hoá nhánh thành refs/heads/*” không được trích. Đây là định lượng “mọi”, cần kiểm tập hợp và namespace. Snapshot giao chỉ có số so heads; nó không tự chứng minh mọi tag/namespace phía máy chủ.
ĐÃ THỬ VÁ: không — bổ sung mệnh đề nguyên dòng vào bảng đo thủ công; giữ riêng “script dùng --mirror” và “ảnh chụp đã đối chiếu đủ heads”. Đừng đổi tuyên bố máy chủ thành chứng minh từ việc thấy đủ nhánh local.
ĐÃ THỬ NGHIỆM: Đọc script:85–99 có clone --mirror và update-ref; tự so set tên+OID: 316/316, 0 lệch ở mirror/cây với nguon-refs.tsv. Server refs ngoài heads KHÔNG ĐO ĐƯỢC vì không có ảnh chụp namespace khác, không mạng. Regex bỏ dòng 37 đúng như dự đoán. Không cần sửa mã sản phẩm.
ĐỘ TIN: cao

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Bảng bỏ lời hứa sinh bằng chứng và khai phần không đo
TỆP/DÒNG: CHANGELOG.md:38; trich_khang_dinh.py.
VẤN ĐỀ: Cùng dòng bị bỏ còn mệnh đề độc lập: script sinh EVIDENCE tự khai cách trích và phần bỏ sót, rồi lập manifest. Đây là lời hứa có đầu ra kiểm được, không phải số hiệu vô hại.
ĐÃ THỬ VÁ: không — thêm vào bảng mệnh đề với cột “đối chiếu đầu ra hiện có / chạy lại toàn builder”. Không sửa regex thành một bộ từ khóa rồi tuyên bố hết lớp bỏ sót.
ĐÃ THỬ NGHIỆM: Đọc EVIDENCE.md hiện có: có bảng phương pháp và PHAN BO SOT; ARTIFACTS có 3190/3190 mục khớp. Đọc phần sinh EVIDENCE của script. Không chạy lại toàn builder/cài công cụ: KHÔNG ĐO ĐƯỢC lần sinh mới ở lượt này; độ toàn vẹn đầu ra không chứng minh provenance lịch sử của việc sinh. Regex bỏ dòng 38. Đây là ghi nhận độ phủ bảng, không cáo buộc đầu ra sai.
ĐỘ TIN: cao

### bo-sot-pham-vi-nen-chua-do  [P3]  Phủ định về macOS/Windows native bị bảng bỏ
TỆP/DÒNG: CHANGELOG.md:91; trich_khang_dinh.py.
VẤN ĐỀ: “Mọi phép đo trên Linux+Bash; chưa có phép đo macOS/Windows native” hoàn toàn vắng trong bảng giao. Thiếu nó dễ làm người đọc nâng probe Linux thành kết quả đa nền. Phải hiểu trong phạm vi probe dựng gói; r358 còn thuật lại một job CI Windows ở đoạn khác.
ĐÃ THỬ VÁ: không — thêm dòng giới hạn vào bảng và ghi rõ “các probe dựng gói kể ở đây”. Không viết phủ định cho toàn kho/toàn lịch sử CI.
ĐÃ THỬ NGHIỆM: Đọc phần Nền đã đo của DO-T33… tại b789e73: đúng tự khai Linux+Bash; regex bỏ dòng 91. Lượt này chỉ chạy Linux. Không có máy macOS/Windows native để chạy: KHÔNG ĐO ĐƯỢC hai nền đó.
ĐỘ TIN: cao về bỏ sót, vừa về phủ định lịch sử

### bo-sot-nguong-hai-client  [P3]  Ngưỡng tối thiểu viết bằng chữ không được trích
TỆP/DÒNG: CHANGELOG.md:100–101; trich_khang_dinh.py.
VẤN ĐỀ: Mệnh đề nguồn “phải thử ít nhất HAI client…” bị mất cả hai dòng. Dòng 99 có số được giữ không chứa ngưỡng này. Đây là bỏ sót định lượng thật, dù nội dung dẫn là đúng.
ĐÃ THỬ VÁ: không — bổ sung mệnh đề và dẫn CLAUDE.md:580–581 trong bảng, không sửa nội dung nguồn. Giữ phạm vi đây là luật phương pháp kết luận đường mạng, không phải giấy phép bỏ ràng buộc không mạng của phiên review.
ĐÃ THỬ NGHIỆM: Mở CLAUDE.md:580–581: có đúng câu “thử ít nhất hai client trước khi gọi đó là chính sách”. Chạy regex trên dòng 100/101: cả hai bị bỏ. Không gọi client mạng nào.
ĐỘ TIN: cao

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng mất phần xác định đối tượng chưa được chặn và hậu quả đo
TỆP/DÒNG: CHANGELOG.md:89–91; trich_khang_dinh.py.
VẤN ĐỀ: Dòng 89 được giữ nhưng dừng ở “chốt symlink KHÔNG”; dòng 90 xác định R chính nó và “cả hai”, cùng dòng 91 xác nhận BỊ XOÁ, đều bị bỏ. Bảng không còn đủ mệnh đề để biết thiếu chốt nào và hai vật nào bị mất; không thể coi đã bao phủ vì còn token rm -rf ở dòng trước.
ĐÃ THỬ VÁ: không — thêm trọn ba dòng như một mệnh đề; giữ nhãn lời thuật lại cho hậu quả sentinel. Nếu cần phản chứng mới, phiên điều phối dựng một thư mục đầu ra qua liên kết tượng trưng, đặt dữ liệu đánh dấu trong hai thư mục con rồi quan sát việc giữ/xóa; reviewer không tự soạn chuỗi đường dẫn/payload đó.
ĐÃ THỬ NGHIỆM: Đọc script và bản b789e73: có hai lệnh xóa, chốt chỉ xét các thành phần con; nguồn nêu hai sentinel. Chạy bộ lọc xác nhận mất đuôi. KHÔNG ĐO ĐƯỢC hậu quả động ở lượt này vì không tự dựng phép thử đường dẫn bị ràng buộc; không gọi đây là không có vấn đề.
ĐỘ TIN: cao về bỏ sót và mã, vừa về hậu quả lịch sử

### cong-kiem-ke-co-rang-nhung-khong-kiem-su-that  [P3]  Đã kiểm hai chiều; gate xanh không chứng nhận các con số ghi sổ
TỆP/DÒNG: CHANGELOG.md:11,16–18; RELEASE_MANIFEST.json mục CHANGELOG.md; than-pr-491.md bảng cổng.
VẤN ĐỀ: Ghi nhận dương bắt buộc: release-verify thật sự chặn nội dung lệch manifest. Tuy nhiên doc-claims-check xanh không bắt được số thống kê 1016 bị đổi thành 1017. Đây là giới hạn cổng, không phải finding P1 “cổng kiểm kê vô nghĩa”.
ĐÃ THỬ VÁ: có — đột biến một byte giữ kích thước CHANGELOG để đo release-verify; riêng đột biến 1016→1017 để đo cổng claims. Cả hai đã khôi phục bằng byte gốc trong finally, không giữ bản vá sản phẩm.
ĐÃ THỬ NGHIỆM: Đột biến byte: release-verify rc=2, failed đúng CHANGELOG.md, package_hash_match=false, package_hash_self_match=true. Khôi phục: rc=0, ok=true. Đột biến số: doc-claims-check --strict rc=0, ok=true. Sau khôi phục cả hai cổng rc=0 và git status sạch. Cách chặn hồi quy lời khai ở lần sửa này là đo lại Git/JSON và nguồn, không thêm test khớp chuỗi chỉ để xanh; tái sinh manifest sau khi executor sửa nội dung.
ĐỘ TIN: cao
