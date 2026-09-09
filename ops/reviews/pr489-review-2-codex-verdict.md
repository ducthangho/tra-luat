verdict: approve
reviewed_sha: 98ef1f1629a2ac786ff91e352dd02da9b693e81e
base_da_review_luot_truoc: 9a99dd8aa137ef118a00671482c29ea2438cbdbb
luot: 2
so_lan_luot_nay_bi_chet_va_phong_lai: 0

**0 finding P1 · 0 finding P2 · 4 finding P3.** Các điều kiện nội dung từng gây P1/P2 đã được sửa. `approve` áp cho exact SHA trên trong phạm vi review offline; không chứng nhận CI/API GitHub, không cấp quyền merge và không xóa các nợ P3. Đã ghi tệp này ngay khi có kết luận, rồi hoàn thiện bằng chứng trong cùng lượt.

Reviewer: Codex/OpenAI, bề mặt agent API có công cụ shell cục bộ, transport machine; độc lập với executor Claude theo nhiệm vụ được giao. Không suy danh tính model thực phục vụ từ tài khoản đăng GitHub hoặc metadata runtime do điều phối thuật lại. Quan sát **0 lần** chết/phóng lại reviewer.

Đơn vị: `luot` đếm lượt review; trường chết/phóng lại đếm lần. SHA/hash, số PR/ADR, số dòng nguồn, phiên bản schema, mã thoát và ID là định danh/giá trị kỹ thuật. Các số đếm dưới đây nêu đơn vị. Cặp bằng chứng dương `N/N` luôn có tử bằng mẫu. “Biên nhận phân loại” gồm biên nhận v2 đạt, legacy miễn trừ và nợ đóng băng; không đồng nghĩa tất cả đạt v2.

Tên ngắn: **L480/L487** = `ops/land/pr480-land-evidence.yaml` / `pr487-land-evidence.yaml`; **RH/VH** = `ops/reviews/pr487-hau-kiem-head-review-1-codex-verdict.receipt.yaml` / verdict `.md` tương ứng; **R2** = `ops/reviews/pr487-review-2-codex-verdict.receipt.yaml`; **RN/VN/JN** = các tệp mới `ops/reviews/pr489-review-1-codex-verdict.receipt.yaml`, `pr489-review-1-codex-verdict.md`, `pr489-review-1-do-cuc-bo.json`; **INDEX** = `ops/reviews/README.md`. Dòng nguồn thuộc reviewed SHA trừ khi ghi mốc khác.

## ĐỐI CHIẾU LƯỢT 1

- `ci-pr-khong-chung-minh-exact-head`: **VÁ SINH LỖI MỚI** — P1 đã đóng tại **2/2 mục CI** của L480:122–130 và L487:158–166: tên chỉ nhận CI được báo cho PR, có cảnh báo không chứng minh cây test là head. Workflow giữ nguyên byte, **1 bước checkout** không có `with.ref`. Nhưng RN:40–41 và INDEX:269 mới tóm tắt “chạy trên cây merge tổng hợp” thành sự kiện chắc chắn, bỏ giới hạn VN:132 “không tuyên đã quan sát runner”. Phần phát sinh chỉ là P3 về diễn giải nguồn, không tái mở P1 của tiền kiểm; giữ slug này ở finding dưới.
- `tien-kiem-bi-thay-bang-so-hau-kiem`: **ĐÃ VÁ THẬT** — **2/2 hàng** đặt tiền kiểm là `KHONG_DO_DUOC`, số mới nằm trong `do_lai_sau_merge`, có tested SHA và lời không hồi tố. Chạy lại cho **81/81 biên nhận** tại `5b96ddc` và **91/91 biên nhận** tại `3873173`; `ok: true`. Kết quả đúng vẫn được giữ, thời điểm lịch sử không bị chứng nhận thay.
- `no-hau-kiem-khong-dong-nghia-approve`: **ĐÃ VÁ THẬT** — **3/3 nguồn** L487:77–91, RH:33–41, INDEX:270 cùng nói đã đọc exact head, verdict `changes_requested`, chưa coi là `approve`. **5/5 tiêu đề finding** của VH khớp tổng; VH:7 xác nhận finding P2 nằm ở hồ sơ PR #489 tại `8911ea4`, ngoài head `3873173`.
- `ket-luan-bac-connector-vuot-phep-do-hau-kiem`: **ĐÃ VÁ THẬT** — **6/6 phép chạy lại** cổng trên commit đầy đủ khớp stdout cũ; **5/5 neo** đúng path/hash/ancestry trên head và merge thật. **2 object** tổng hợp vẫn không đọc được. L487:106–133,230–233; L480:183–211; RH:49–76; INDEX:270 giữ vế kho nông ở lớp attestation và giữ phạm vi connector chưa đo. Không còn suy “chỉ khác một biến” thành phép chứng minh độc lập.
- `trang-thai-477-ghep-ci-cua-480`: **ĐÃ VÁ THẬT** — L480:261–267 phân biệt **2/2 cặp PR–merge OID**: #477/`585c7d5`, #480/`7e69b8e`; trỏ đúng lời khai run `34176439015` ở evidence #477:111–117. CI #480 không còn làm căn cứ phủ định CI #477; `landed` không được chứng nhận offline.
- `dinh-chinh-van-giu-mau-thuan-da-rut`: **ĐÃ VÁ THẬT** — **2/2 khối** đối chứng đã đồng bộ: L480:252–253 chuyển mục chưa đo sang kho nông/log A/B gốc; RH:67–76 rút tiền đề master đỏ và giới hạn kết quả tại commit. Không còn giữ “nguyên nhân master đỏ” như câu hỏi đang mở.
- `khai-va-het-ba-loi-sai-commit`: **ĐÃ VÁ THẬT** — L487:55–59, R2:46–58, INDEX:271 cùng kể đúng **3/3 mốc commit**: `edb288e` sửa receipt, `3873173` sửa INDEX, `1455741` sửa manifest còn sót. RH:86 ghi `da_va: false` nhưng giới hạn rõ “tại reviewed head 9a99dd8”; đó là ảnh chụp trước bản vá, không phải trạng thái hiện tại bị mâu thuẫn. `git show` theo tệp xác nhận, không dựa commit message.
- `neo-verdict-khong-phai-commit-them-dau`: **ĐÃ VÁ THẬT** — RH neo `e1fd0a333109a555af4823fd2b830521d86fafbd`; lịch sử HEAD và `--all` đều cho **1/1 commit thêm** này, blob **37.900/37.900 byte** khớp. RN mới cũng đúng: **1/1 commit thêm** là `45bd80e08c5efdcb9d713e42fe0804f7d9fd3af1`, không mắc lại lỗi neo đầu tiên.
- `lich-su-land-evidence-bo-sot-nhanh-477`: **ĐÃ VÁ THẬT** — commit thêm L480 là `6db5b6c`, cha `7e69b8e`; `f4d74fe` không là tổ tiên commit thêm, được nhận ở `582a436`. Inventory khớp **4/4 tệp** tại `f4d74fe`, **6/6 tệp** tại head mới. L480:10–12,94–99,257–270 và L487:240–242 tách đúng tuyến #477→#480→#489, dùng số tệp thay thứ tự land.
- `dan-protocol-sai-o-cong`: **ĐÃ VÁ THẬT** — **2/2 lời dẫn** L480:7–8 và L487:5–6 đổi sang “có nhắc”; protocol:1136 thật sự ghi `lease_publish.py` **10 lần nhắc**, `packet_loop.py` **11 lần nhắc**. Chú giải protocol:1108–1110 nói đây là proxy, không chứng minh cưỡng chế nội dung.
- `bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon`: **CHƯA VÁ** — **526/526 lá YAML** đúng type/path/giá trị và không cắt; nhưng **2 tệp Markdown thay đổi**, **242 lá JSON** mới và **62 dòng comment YAML** hiện tại không có inventory trong bảng. Tái đo mốc cũ cho **67 dòng ứng viên = 66 comment YAML + 1 dòng prose**, đúng phép đo lượt trước. Bỏ bảng chú thích không đóng lỗi độ phủ; finding P3 giữ nguyên slug.

Tổng đối chiếu: **11/11 slug** — **9 slug ĐÃ VÁ THẬT**, **1 slug VÁ SINH LỖI MỚI**, **0 slug VÁ HỜ**, **1 slug CHƯA VÁ**. Đây là số trạng thái slug; severity còn lại được đếm riêng.

## BẢNG ĐO

Phép đo lưu ở `phep-do/`. `do-ho-so.py` kiểm Git/blob/biên nhận; `do-bang.py` so đầy đủ lá YAML, phân loại comment bằng span scalar và kiểm tham chiếu JSON. `do-cong.py` dựng phép chiếu receipt tại từng SHA, với HEAD riêng và object đọc từ gói, rồi gọi CLI `ops/bien_nhan_v2.py --root <phép-chiếu>` từ `cay-kho/`. Đây chỉ là đầu vào cho cổng receipt, không phải checkout đầy đủ để chạy các cổng khác. Mã cổng và các nguồn luật được đối chiếu nguyên byte tại **24/24 cặp SHA–tệp**. Mọi Git command đều chỉ đọc; metadata scratch nằm ngoài `cay-kho/`.

| khẳng định (tệp:key path) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| Gói: HEAD/base/tree/sạch/không nông | Exact SHA theo prompt | HEAD `98ef1f1629a2ac786ff91e352dd02da9b693e81e`; base `9a99dd8aa137ef118a00671482c29ea2438cbdbb`; tree `e7a5a80dea7a22fe1e240bced0366a1506746bfa`; detached; porcelain **0 byte**; shallow=false; **0 ref replace**; `preflight.json`, `ok: true` | ĐO ĐƯỢC | Có |
| Gói: ref nhánh | **314 ref nhánh**, không lệch snapshot | **314/314 cặp tên–OID** khớp cả snapshot cây, mirror và bản TSV được gọi là máy chủ; `refs.json`, `ok: true`. Không xác thực máy chủ hiện tại hoặc nguồn chụp | ĐO ĐƯỢC trong gói | Có, giới hạn snapshot |
| Gói: ARTIFACTS.sha256 | Toàn vẹn hiện vật | **3.176/3.176 tệp** khớp băm, **0 tệp lệch**; `manifest.json`, `ok: true`. Chứng minh khớp manifest được cấp, không chứng minh ai tạo hiện vật | ĐO ĐƯỢC | Có |
| PROMPT.md:11, tổng diff | **8 tệp**, thêm **560 dòng**, bớt **132 dòng** | Git và numstat cùng **8/8 tệp**, thêm **950 dòng**, bớt **132 dòng**; patch cung cấp khớp nguyên văn Git diff. Sai **390 dòng thêm** trong lời giới thiệu; `preflight.json` | ĐO ĐƯỢC+LỆCH | Không |
| RN:verdict_sha256,verdict_bytes | SHA-256 `74aa34c3f384148f3a17682f46da84f8aa52aa9001838a3db04ab68f131924ab`; **54.761 byte** | Băm trùng; **54.761/54.761 byte**; VN nguyên byte với `VERDICT-luot1.md`; `copies.json`, `receipts.json`, `ok: true` cho receipt | ĐO ĐƯỢC | Có |
| RN:so_p1/so_p2/so_p3,reviewed_sha,verdict | **1 finding P1**, **4 finding P2**, **6 finding P3**; `9a99dd8…`; `changes_requested` | Regex `^### … [P1/P2/P3]` đếm **11/11 tiêu đề finding**, đúng phân bố; SHA đầy đủ và verdict khớp thân VN. Không đổi reviewed SHA thành commit vận chuyển hoặc head lượt mới | ĐO ĐƯỢC | Có |
| RN:evidence_url,evidence_url_ghi_chu | `45bd80e` là commit đầu tiên thêm VN | HEAD và `--all` đều có **1/1 commit thêm**: `45bd80e08c5efdcb9d713e42fe0804f7d9fd3af1`; path/hash/byte/ancestry khớp. **8/8 đối chiếu receipt** đạt, `ok: true` | ĐO ĐƯỢC | Có |
| RH:evidence_url, ghi chú mốc cũ | Đổi `1455741` sang `e1fd0a3` | **1/1 commit thêm** là `e1fd0a333109a555af4823fd2b830521d86fafbd`; neo mới khớp blob và ancestry. `1455741` nằm sau và chỉ sửa hồ sơ khác; không phải commit thêm VH | ĐO ĐƯỢC | Có |
| L480:cross_review.hien_vat.ghi_chu_vi_tri | Thêm ở `6db5b6c`, cha `7e69b8e`; chưa nhận `f4d74fe` | `log --diff-filter=A` và cha commit khớp; phép hỏi ancestry trả false; `582a436` có `f4d74fe` là cha. `history.json` | ĐO ĐƯỢC | Có |
| L480/L487:bookkeeping, số land evidence | Base `f4d74fe` có **4 tệp**, head có **6 tệp** | `ls-tree -r --name-only`: **4/4 tệp** và **6/6 tệp**, có evidence #477 ở base; chênh **2 tệp** đúng hai land evidence của PR. Không biến inventory Git thành số lần land thành công | ĐO ĐƯỢC | Có |
| L480:7 / L487:5, dẫn §20 | ADR-0034 “có nhắc” | Protocol:1136 ghi **10 lần nhắc** ở lease_publish, **11 lần nhắc** ở packet_loop; **2/2 lời dẫn** đã sửa đúng ô. Đây là đọc hàng lịch sử trong protocol, không tái chứng minh độ bao phủ cổng hiện tại | ĐO ĐƯỢC | Có |
| RN:ba_loi_lich_su_git_dieu_phoi_tu_kiem_lai | Tên khóa gọi **3 lời khai**; danh sách là các kết quả mới | `safe_load` cho **4 phần tử**, các phép đối chứng lịch sử khớp **4/4 lời sửa**. Dữ liệu mới đúng; tên khối chưa theo số phần tử; RN:63–67 | ĐO ĐƯỢC+LỆCH | Sai tên khối, không sai kết quả |
| JN:toàn bộ byte | Hiện vật đo lượt trước đưa vào kho | Nguyên **10.443/10.443 byte** so với `do-cuc-bo-luot1.json`; SHA-256 `ddcfdde17f22f3d580234cbdd96e92dbb77ca1c3339238c4cdfd92e70e34ed40`; JSON parse cũng bằng nhau. Không dùng ký ức về phiên trước hoặc tên tác giả để thay phép so byte | ĐO ĐƯỢC | Có |
| JN:bien_nhan tại `c87b067` | **30 biên nhận v2 đạt**, **0 vi phạm**, tổng **83 biên nhận** | CLI tái chạy: **83/83 biên nhận** phân loại = **30 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; stdout nguyên văn khớp, `ok: true` | ĐO ĐƯỢC | Có |
| JN:bien_nhan tại `da481f9` | **33 biên nhận v2 đạt**, tổng **86 biên nhận** | **86/86 biên nhận** = **33 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; stdout khớp, `ok: true` | ĐO ĐƯỢC | Có |
| JN:bien_nhan tại `5b96ddc` | **28 biên nhận v2 đạt**, tổng **81 biên nhận** | **81/81 biên nhận** = **28 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; stdout khớp, `ok: true` | ĐO ĐƯỢC | Có |
| JN:bien_nhan tại `7e69b8e` | **33 biên nhận v2 đạt**, tổng **86 biên nhận** | **86/86 biên nhận** = **33 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; stdout khớp, `ok: true` | ĐO ĐƯỢC | Có |
| JN:bien_nhan tại `3873173` | **38 biên nhận v2 đạt**, tổng **91 biên nhận** | **91/91 biên nhận** = **38 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; stdout khớp, `ok: true` | ĐO ĐƯỢC | Có |
| JN:bien_nhan tại `f4d74fe` | **38 biên nhận v2 đạt**, tổng **91 biên nhận** | **91/91 biên nhận** = **38 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; stdout khớp, `ok: true` | ĐO ĐƯỢC | Có |
| JN:graph, số commit trong các cây | OID, cha, timestamp và số reachable commit | Tái hỏi Git cho **11/11 bản ghi commit**, tất cả khớp. Trường `ancestors` trong phần số đo cũ thực chất đếm commit reachable **kể cả HEAD**, như `commits_including_self`; không diễn giải thành số tổ tiên nghiêm ngặt. `graph-replay.json` | ĐO ĐƯỢC | Có |
| JN:five_anchors | Neo đúng path/hash và là tổ tiên head/merge thật | **5/5 bản ghi neo** tái đo trùng hoàn toàn; mỗi neo khớp cả `3873173` và `f4d74fe`; `anchors.json`, `ok: true` từng neo | ĐO ĐƯỢC | Có |
| JN:graph.synthetic_objects | Không có các object connector được dẫn | `cat-file -e <OID>^{commit}` vẫn không đọc được **2 object**: `a9b9edd014636dd49b208a5e2d37fbe5dfa0c01f`, `372bf9adb331218212619fc04763acbedfaa3f3f`. Không nói chúng bịa; không suy kết quả cổng từ cây khác | KHÔNG ĐO ĐƯỢC cổng trên object ấy | Khớp giới hạn |
| JN:đổi thư mục; RN:hien_vat_reviewer_vao_kho | `ops/land/` chuyển sang `ops/reviews/` | JSON không có đường dẫn tự trỏ thư mục cũ. **5/5 path receipt** và **7/7 path lệnh** vẫn tồn tại khi resolve từ gốc kho. `--root .` thuộc cwd chạy lệnh, không phải thư mục chứa JSON. RN:103–105 đã ghi ánh xạ đổi chỗ; `navigation.json`, `ok: true` | ĐO ĐƯỢC | Có |
| VN:150, đường dẫn gói gợi ý cũ | `cay/ops/land/pr489-review-1-do-cuc-bo.json` | Đây là địa chỉ trong gói vá lịch sử của lượt trước; không phải link repo hiện tại. Nó không tồn tại nguyên đường dẫn trong checkout mới. Địa chỉ hiện tại là `ops/reviews/pr489-review-1-do-cuc-bo.json`, được receipt và INDEX chỉ ra. Không sửa VN để tránh phá byte/hash lịch sử | ĐO ĐƯỢC | Không gãy tham chiếu JSON; cần đọc đúng ngữ cảnh gói |
| L480/L487:pre_merge_checks | Không chứng minh tiền kiểm receipt và CI exact head | **2/2 mục CI** giữ kết quả PR ở lớp attestation, ghi thiếu SHA/log cây test; **2/2 mục receipt** tách kết quả hậu kiểm. Không còn chỗ trong chính các mục tiền kiểm này chứng nhận cây test là head. `not_run` của review #487 là trước merge, phù hợp trạng thái hậu kiểm hiện tại | ĐO ĐƯỢC về phạm vi lời văn | Có |
| L487:no_review…; RH:tinh_trang_hau_kiem; INDEX:270 | Đã hậu kiểm, chờ đóng findings | **3/3 nguồn** cùng phạm vi, cùng verdict và phân bố **5/5 finding** của VH. Finding P2 ở hồ sơ viết sau không bị quy cho head đã merge | ĐO ĐƯỢC | Có |
| L480:trang_thai_cua_477 | #477 có lời khai CI riêng; chưa chứng nhận `landed` offline | Git khớp **2/2 cặp merge OID** và các khối văn bản phân biệt đúng PR. Run `34176439015` tồn tại dưới dạng lời khai ở evidence #477; không có API/run JSON để xác thực success | ĐO ĐƯỢC về liên kết; API KHÔNG ĐO ĐƯỢC | Có trong phạm vi offline |
| Các bản sửa: hạ xuống attestation | Kho nông/log cũ và nguồn API chưa đối chứng | Không thấy hạ quá tay băm blob, quan hệ tổ tiên hoặc số finding thành “không đo được”. Cơ chế mã và vế mirror nằm trong prose A/B nhưng được ghi rõ là đọc/tái đo được; **6/6 kết quả cổng**, **5/5 neo** và số finding còn nguyên. Lỗi mới là chiều ngược ở bản tóm tắt CI, xem P3 | ĐO ĐƯỢC về phân loại | Có, với P3 riêng |
| BANG-CAU-TRUC-DAY-DU.tsv | **526 lá**, **0 lá bị cắt** | **526/526 lá** khớp type/path/giá trị `safe_load` từ **5/5 tệp YAML**; **0 lá thiếu**, **0 lá dư**, **0 lá bị cắt**; `tables.json`, `ok: true`. Đây là giá trị sau parse, không phải byte YAML nguyên văn | ĐO ĐƯỢC | Có |
| Bảng: Markdown/JSON/comment | Tự nhận thiếu Markdown và không kèm bảng comment | Còn thiếu **2 tệp Markdown thay đổi**, toàn bộ **242 lá JSON** mới, **62 dòng comment YAML**. Không coi prose nằm nguyên trong scalar là bị mất chữ; vấn đề là chưa tách mệnh đề và thiếu nguồn đối chứng | ĐO ĐƯỢC+THIẾU PHỦ | Nợ chưa đóng |
| Phép đo comment tại base lượt trước | **67 dòng ứng viên = 66 comment + 1 prose** | `git show 9a99dd8:<path>` trên đúng **5 tệp YAML** cũ, `yaml.scan` cho đúng phép phân loại. Dòng prose là L480:97, thuộc folded scalar. `comments.json`, `old_replay_matches: true` | ĐO ĐƯỢC | Có |
| Comment ở đầu vào hiện tại | Bảng comment bị bỏ | Đo được **62/62 dòng comment YAML** hiện tại, tất cả là comment nguyên dòng; **0 comment cuối dòng** trong tập này. Đã ghi `BANG-CHU-THICH-DO-LAI.tsv`; không mang số của tập cũ sang tập mới | ĐO ĐƯỢC | Bổ sung phép đo mới |
| CLI trực tiếp tại reviewed head | Không có số head mới trong JSON lịch sử | **93/93 biên nhận** phân loại = **40 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`; `bien-nhan-head.json` | ĐO ĐƯỢC | Phép đo mới |
| doctrine-scan, adr-song tại head | Cổng ngắn được phép | **7/7 tệp** được quét, **0 chỗ chép doctrine**; **46/46 mục ADR** khớp, ngoại lệ thiếu trạng thái ADR-0016 được CLI khai rõ. Hai stdout lưu riêng | ĐO ĐƯỢC | Có |
| doc-claims-check --strict tại head | Cổng ngắn được phép | `ok: true`, **106 tệp quét**, **367 advisory**, **0 cờ cứng**. Roots không gồm `ops/`; kết quả này không xác thực prose trong land evidence/receipt/INDEX. `doc-claims-check.json` | ĐO ĐƯỢC | Có, đúng phạm vi cổng |
| ci.yml:checkout,timeout-minutes | Không thay workflow/timeout | **1/1 blob workflow** giữ nguyên so base và **2/2 head CI** lịch sử được dẫn; **1 bước checkout** không có `with.ref`; timeout **60 phút** giữ nguyên. Không chạy CI hoặc bộ test dài | ĐO ĐƯỢC về cấu hình | Có |
| RN/RH:runtime,model,session,API; A/B kho nông | Điều phối thuật lại | Không có runtime/log gốc, snapshot API hoặc kho nông để kiểm. Hash của verdict đo được không xác thực mọi scalar về phiên chạy; các URL GitHub chỉ được parse và đối chiếu Git cục bộ | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho) | Không kết luận về sự kiện ngoài gói |

**Bốn lời sửa lịch sử đều đúng — 4/4 phép đối chứng khớp.** Các tệp land evidence, RH và INDEX đã dùng đúng mốc mới. RN cũng ghi đủ kết quả đúng nhưng để tên khóa “ba lời khai”; lỗi tên khối được tách P3, không phủ nhận công sửa dữ liệu.

**Việc đổi thư mục JSON không làm hỏng nội dung hoặc các path bên trong.** VN giữ địa chỉ của gói gợi ý lịch sử, còn RN/INDEX dẫn vị trí đã nhập kho. Các tệp `phep-do/…` và `GOI-VA.md` được VN nhắc là hiện vật gói lượt trước, nhiều tệp không kèm lượt này; không nhận chúng là log đã kiểm lại. Những phép chạy lại của lượt này có đường dẫn riêng dưới `phep-do/` của gói hiện tại.

## KHẲNG ĐỊNH BẢNG BỎ SÓT

| vị trí | khẳng định | vì sao trượt | hệ quả |
|---|---|---|---|
| L480:7–12 | ADR-0034 thuộc ô “có nhắc”; tuyến #477→#480→#489 | Comment YAML không vào bảng lá; bảng comment bị bỏ | Bảng không cho kiểm chính lời dẫn đã từng bị bác dù ý tương tự có thể có trong scalar khác |
| L487:5–6 | Số lần nhắc không chứng minh cưỡng chế nội dung | Comment ngoài đầu vào | Bỏ giới hạn chống đọc quá rộng phần protocol |
| RN:5–8 | Nhiệm vụ của lượt trước là kiểm bản sửa sau phát hiện kho nông | Comment ngoài bảng | Bỏ một nơi điều phối tự thuật nguồn và phạm vi kết luận |
| VN:132 | Reviewer không tuyên đã quan sát runner checkout cây tổng hợp | Verdict Markdown ngoài bảng | RN/INDEX mới mất đúng giới hạn này; finding CI phát sinh mức P3 |
| VN:107 | **67 dòng ứng viên** thực chất gồm **66 comment YAML** và **1 dòng prose** | Verdict Markdown ngoài bảng | Không có nguồn kiểm lỗi parser ngay trong bảng tự nói về parser |
| VN:150 | Gói cũ đặt JSON ở `cay/ops/land/` | Verdict Markdown ngoài bảng | Không thấy đường dẫn lịch sử để đối chiếu với ánh xạ nhập kho trong RN |
| INDEX:269 | CI của PR “chạy trên cây merge tổng hợp” | INDEX ngoài bảng | Lời tóm tắt mới mạnh hơn phép quan sát được VN giới hạn |
| INDEX:270 | Hậu kiểm không thay `approve`; finding P2 ngoài head đã merge | INDEX ngoài bảng | Mất một trong các nguồn bắt buộc đối chiếu trạng thái; lần này nội dung đã sửa đúng |
| VH:7–9 | Phạm vi finding và việc hậu kiểm không hồi tố | Verdict nguồn ngoài bảng | Không thể kiểm sự trung thành của bản tóm tắt chỉ từ bảng YAML |
| JN:bien_nhan[*],five_anchors[*],graph | Stdout, SHA, băm/path/ancestry, topology và giới hạn phép đo | Đầu vào chỉ YAML, không nhận JSON mới; thiếu **242 lá JSON** | Bỏ hiện vật được đưa vào để người sau tái đo; đây là chỗ mù bổ sung ngoài các chỗ điều phối đã nêu |

`phep-do/bo-sot.json` lưu nguyên văn **9/9 vị trí nguồn** ở các hàng văn bản và **242/242 lá JSON** của hàng cuối. Đây là inventory, không tự nhận đã hiểu/tách hết mọi mệnh đề. Các vị trí cùng lớp độ phủ được gom dưới slug độ phủ; không nhân số finding chỉ vì có nhiều vị trí.

### ci-pr-khong-chung-minh-exact-head  [P3]  Bản tóm tắt mới biến cấu hình checkout dự kiến thành sự kiện runner đã quan sát

TỆP/DÒNG: RN:39–41; INDEX:269. Đối chứng VN:132 và `.github/workflows/ci.yml`:81–86,115.

VẤN ĐỀ: P1 cũ trong `pre_merge_checks` đã đóng. Tuy nhiên, RN và hàng INDEX mới nói lượt PR “chạy trên cây merge tổng hợp”, trong khi VN nói rõ không tuyên đã quan sát runner. Đọc workflow xác nhận cấu hình checkout dự kiến và lý do không được nhận CI ấy là bằng chứng head; nó không cung cấp log của run lịch sử. Tôi không khẳng định runner đã chạy cây khác với cấu hình. Lỗi là mất giới hạn nguồn khi thuật lại kết luận. Xếp P3 vì hai mục CI tiền kiểm đã cảnh báo đúng và câu mới không được dùng để cho qua gate/đóng trạng thái.

ĐÃ THỬ VÁ: Đổi cả hai tóm tắt thành “workflow dự kiến dùng cây merge tổng hợp; không có log checkout/run JSON để xác thực cây runner đã test”. Giữ kết luận P1 lịch sử, không sửa verdict gốc.

GÓI VÁ: **2 tệp đầy đủ** `cay/ops/reviews/pr489-review-1-codex-verdict.receipt.yaml` và `cay/ops/reviews/README.md`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: So câu nguồn VN với **2/2 vị trí** tóm tắt; YAML đọc được; giữ **12/12 trường** nhận dạng/verdict/neo/số finding đã chọn; INDEX chỉ đổi **1/1 dòng** dự kiến. `phep-do/hints.json`, `ok: true`. CI thực KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): cấm mạng/CI, không có log. Không thêm test mô phỏng runner để chứng nhận một sự kiện lịch sử.

ĐỘ TIN: cao về lệch phạm vi lời tóm tắt; không kết luận SHA runner thực đã checkout.

### bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon  [P3]  Giữ đủ lá YAML vẫn bỏ Markdown, comment và hiện vật JSON mới

TỆP/DÒNG: `BANG-CAU-TRUC-DAY-DU.tsv`:1–7; bảng bỏ sót ở trên; JN toàn tệp.

VẤN ĐỀ: **526/526 lá YAML** là phép đếm đúng, **0 lá bị cắt**. Nhưng bảng thiếu nguồn Markdown, comment và cả JSON mới, nên không đủ làm inventory khẳng định của toàn diff. Những mệnh đề trong scalar đã có chữ vẫn chưa được tách riêng; đó là giới hạn khác với bỏ nguồn. Chỉ ghi nợ hoặc bỏ bảng đã biết đếm sai không đóng lỗi này.

Bỏ bảng comment **làm độ phủ tra cứu kém hơn** giữ nguyên nội dung ứng viên với nhãn đúng và giới hạn rõ: từ tập cũ có thể tra các dòng sang không có bảng để tra. Tuy nhiên, tiếp tục gọi tất cả ứng viên là comment và báo đạt cũng sai. Cách sửa phù hợp là giữ dữ liệu, sửa phân loại; không chọn giữa bỏ dữ liệu và giữ kết luận sai. Lượt này dữ liệu nguồn còn nguyên, nên chưa mất bằng chứng không thể khôi phục.

ĐÃ THỬ VÁ: Dùng `yaml.scan` lấy span scalar, loại dấu `#` trong scalar khỏi comment; lập inventory comment và Markdown/JSON ngoài bảng. Tái đo mốc cũ xác định chính xác L480:97 là prose. Không viết một regex mới rồi tuyên bao phủ ngữ nghĩa văn xuôi.

GÓI VÁ: P3 không yêu cầu tệp sản phẩm; có `BANG-CHU-THICH-DO-LAI.tsv`, `phep-do/do-bang.py`, `phep-do/bo-sot.json`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Chưa tuyên đã hoàn thành công cụ trích toàn bộ khẳng định.

ĐÃ THỬ NGHIỆM: **526/526 lá** khớp; phân loại lại đúng **67 dòng ứng viên**, gồm **66 comment YAML** và **1 dòng prose** ở mốc cũ. Tập hiện tại cho **62/62 comment nguyên dòng**, **0 comment cuối dòng**; inventory bổ sung **9/9 vị trí văn bản** và **242/242 lá JSON**. Không dùng số comment cũ thay số của tập hiện tại. `tables.json`, `comments.json`, `bo-sot.json`.

ĐỘ TIN: cao về phần thiếu nguồn và phân loại; không tự chứng nhận đã tách hết mọi mệnh đề.

### ten-khoi-ba-loi-khong-khop-bon-phep-do  [P3]  Biên nhận mới giữ tên khối đếm ba nhưng liệt kê bốn lời sửa

TỆP/DÒNG: RN:63–67, khóa `ba_loi_lich_su_git_dieu_phoi_tu_kiem_lai`.

VẤN ĐỀ: Tên khối ghi **3 lời khai**, nhưng danh sách có **4 phần tử**, đúng với INDEX và chỉ thị chủ kho nói **4 lời khai**. Cả **4/4 kết quả** sửa đều khớp phép đo Git/nguồn protocol; lỗi chỉ ở tên gọi bị giữ lại sau khi mở rộng danh sách. Không trộn lỗi này vào số finding P1/P2/P3 của verdict, các số đó đều đúng.

ĐÃ THỬ VÁ: Đổi tên khóa sang `bon_loi_lich_su_git_dieu_phoi_tu_kiem_lai`, giữ nguyên các phần tử. Không đổi số mới hoặc hạ chúng thành attestation.

GÓI VÁ: Tệp đầy đủ RN trong `cay/ops/reviews/`, dùng chung với gợi ý CI. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `yaml.safe_load` đếm **4/4 phần tử** trước/sau, đối chiếu nội dung danh sách nguyên vẹn; **12/12 trường** đã chọn về identity/verdict/neo/số finding giữ nguyên. Không có yêu cầu thay schema cổng cho khóa prose này. `hints.json`, `ok: true`.

ĐỘ TIN: cao; tác động giới hạn ở nhất quán hồ sơ.

### tong-dong-diff-trong-prompt-khong-khop-numstat  [P3]  Lời giới thiệu gói đếm thiếu dòng thêm

TỆP/DÒNG: `PROMPT.md`:11; `numstat-luot1-den-luot2.txt` toàn tệp.

VẤN ĐỀ: Lời giới thiệu ghi thêm **560 dòng**, nhưng tổng trực tiếp từ Git và numstat là thêm **950 dòng**, bớt **132 dòng**, trên **8 tệp**. Thiếu **390 dòng thêm** trong lời khai quy mô. Không có hiện vật diff bị cắt: patch cung cấp và danh sách numstat vẫn đúng.

ĐÃ THỬ VÁ: Đưa con số đo được vào bảng đo của verdict và hướng dẫn sửa lời giới thiệu thành “**8 tệp, thêm 950 dòng, bớt 132 dòng**”. Không sửa prompt gốc của gói và không tạo một thay đổi sản phẩm chỉ để sửa lời giao việc.

GÓI VÁ: Không có tệp sản phẩm cho P3 thuộc prompt; đính chính cụ thể ở đây và `GOI-VA.md`. Nếu áp vào bản gói sau: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `git diff --numstat 9a99dd8… 98ef1f1…` khớp **8/8 hàng** của numstat; phép cộng cho **950 dòng thêm**, **132 dòng bớt**. Git diff khớp nguyên văn patch được cấp; `preflight.json`. Không suy số bị thiếu thuộc một tệp cụ thể khi không có bằng chứng cho cách người soạn cộng.

ĐỘ TIN: cao; không ảnh hưởng nội dung checkout được review.

## GIỚI HẠN VÀ HIỆN VẬT BÀN GIAO

**KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho):** GitHub API, trạng thái/checkout của CI thực, approval/merged_by, nội dung comment, lịch sử push; nguồn runtime/run.json/argv/stdout/stderr của phiên cũ; kho nông và log A/B gốc; môi trường connector và cổng trên object tổng hợp không có trong gói. Lý do là cấm mạng/CI, thiếu hiện vật hoặc cấm bộ test dài. Không xác nhận passed từ lời thuật API, `not_run`, `skipped` hoặc mã thoát trần.

Các phép ngắn được chạy đã nêu phạm vi và bằng chứng dương. Không chạy `lease_publish` suite để tạo số ca tiền kiểm, không dùng `lease_publish.py check` thay suite; không chạy actionlint/shellcheck lại cho các blob workflow/script không đổi trong diff này. Không cấp lease, đăng ra ngoài, commit, merge hoặc nâng timeout.

`GOI-VA.md` mô tả **2 tệp gợi ý đầy đủ** dưới `cay/`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không có P1/P2 cần gói vá bắt buộc; các gợi ý P3 không biến thành điều kiện ngầm của kết luận `approve` ở SHA đã review. Nếu executor sửa head, kết luận này không tự chuyển sang SHA mới.

Kiểm cuối: `cay-kho/` vẫn exact reviewed SHA, tree `e7a5a80dea7a22fe1e240bced0366a1506746bfa`, detached, không nông; **314/314 ref nhánh** nguyên trạng; `status --porcelain` **0 byte**. Đối chiếu đủ **11/11 slug**, đủ **4/4 tiêu đề finding P3** và các trường bắt buộc; `phep-do/final-integrity.json`, `ok: true`.
