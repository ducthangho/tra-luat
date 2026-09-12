verdict: changes_requested
reviewed_sha: 8de21bee0460bfe89b13ece2bafaa3a113593441

## BẢNG ĐO

Lượt 9: **0 P1 / 2 P2 / 0 P3**. Không phát hiện sai mới trong phần đo được của §1, §2, chú thích `tong_hop` và manifest. Hai finding nằm ở lời khai đã xoá số trong biên nhận lượt 4 và phạm vi kết luận về CI trong `EVIDENCE.md`.

Tree đo được: `3e8189607e5d59decb0da1cb1ee3fd9485bf9052`. Các lệnh có khả năng ghi và mọi đột biến chạy trên bản chép đầy đủ trong `tam-review-r9/`, với thư mục tạm cũng nằm tại đó; không chạy chúng trên `cay-kho/`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Cấu hình gói | HEAD/tree, clone đầy đủ, origin cục bộ, abbrev 7, cây sạch | `rev-parse`, `remote get-url`, `config`, `status --porcelain` khớp từng trường; `is-shallow-repository=false`. Khối cấu hình trong EVIDENCE bằng nguyên văn `do-goi.txt` | Có |
| Mirror và raw | 326 heads; 1 ref giao hàng; raw 324; thiếu/thừa/lệch OID = 0/1/0 | `for-each-ref` trên `kho.git`: 326; loại đúng `pr497-head` còn 325. So map tên → OID với raw: thiếu `[]`, thừa `[pr487-merge]`, lệch OID `[]` | Có; lỗi giao ref của lượt 8 đã hết trong gói này |
| Byte raw | 324 dòng; SHA-256 bắt đầu `92f19bcba422aa39` | 324 dòng; SHA-256 `92f19bcba422aa392d4885c372a34d6e3e3cd00d0bbe6bccc1d0d4518b7771d3`. Tệp thời điểm ghi `2026-09-11T01:54:54Z` | Có về byte; xuất xứ/thời điểm GitHub là thuật lại |
| Quét `r362` trên mirror | Hai ref, không tính ref giao hàng | Quét tiêu đề CHANGELOG trên từng head, **đã loại `pr497-head`**: đúng `claude/handoff-tra-luat-repo-2ak5th` và `claude/handoff-tra-luat-repo-2ak5th-wip` | Có |
| Ref sao lưu không kích hoạt CI | Suy từ cấu hình `ci.yml` | Cấu hình còn `workflow_dispatch`; chỉ chứng minh được push trực tiếp vào ref này không khớp bộ lọc push | Không; finding bên dưới |
| Phạm vi PR | `c00c88a..HEAD`: 14 tệp, +2 998/−5, 20 commit | `git diff --numstat`, `rev-list --count` khớp; `diff.patch` và `numstat.txt` bằng kết quả Git. Hồ sơ #492 thuộc phần merge từ master | Có |
| §1: `merged` của #490 | `8cee941`, hai cha `00e017a` và `01e7f77` | `git show -s --format='%H %P' 8cee941` trả đúng hai cha. Hai cha là tổ tiên của merge; merge là tổ tiên của HEAD và `origin/master`, tất cả `merge-base --is-ancestor` rc=0 | Có về DAG cục bộ; trạng thái GitHub không đo được |
| §1: `bookkeeping` | Mục r359 là nơi ghi sổ thay land-evidence riêng | Mục r359 hiện diện và mô tả đúng lựa chọn đó (`CHANGELOG.md:963–973`); đọc được nội dung, không xác thực được quyết định của chủ kho chỉ bằng nội dung ấy | Có về hiện vật; authority là thuật lại |
| §1: hậu-merge gate / `landed` | Run `34391481045`, push/master, SHA `8cee941`, attempt 1; hai job success | **KHÔNG ĐO ĐƯỢC** run/job/attempt/event/kết luận GitHub. §1 có nhãn “thuật lại” tại dòng 149, cùng quy tắc nguồn ở dòng 114–121. Không lấy cổng chạy hôm nay làm bằng chứng cho run cũ | Nhãn phù hợp; không chứng thực độc lập `landed` |
| Bảng CI | 41 bước; Ubuntu 37+4+0, Windows 35+6+0 | Hai tổng đều 41. YAML tại `8cee941` và HEAD đều có 40 khai báo step; đó không phải bản ghi 41 bước runtime của Actions. Đọc được các điều kiện skip, không đọc được kết quả từng bước của run | Đúng số học; kết quả CI vẫn là thuật lại |
| §2: A/B chỉ khác shellcheck | Có: canary DAT; thiếu: canary DO, blocking | PATH riêng gồm các liên kết tới công cụ có sẵn; chỉ bỏ liên kết `shellcheck` giữa A/B. Có: tổng DAT/rc=0, canary DAT, bắt SC1003/rc=1. Thiếu: actionlint DAT, shellcheck KHONG_DO_DUOC, canary DO/blocking với thông báo SUY_GIAM, tổng DO/rc=2 | Có; câu r361 bị rút thực sự sai |
| `--chi` | Không chạy canary; thiếu shellcheck vẫn có thể tổng DAT | Với cả hai PATH, thử riêng `--chi shellcheck`, `--chi actionlint`, `--chi rg`: đều `canary=[]`, tổng DAT/rc=0. Trường shellcheck ở nhánh thiếu vẫn KHONG_DO_DUOC | Có; nợ hẹp đã được mô tả đúng |
| Chú thích `tong_hop` | Chỉ giải thích cơ chế, không sửa runtime; CI cụ thể là thuật lại | `ast.dump(ast.parse(...))` của toàn tệp tại base `c00c88a` và HEAD bằng nhau. `if chi is None`, vòng tổng hợp canary, YAML blocking, lệnh G5 đầy đủ và lệnh cài dùng `--chi` khớp chú thích | Có |
| Manifest | 180 mục; chỉ CHANGELOG đổi trong kiểm kê | Đọc và băm **từng tệp**: 180 đường dẫn duy nhất, 0 sai size/hash, tổng 8 172 715 byte. So map manifest base/head: chỉ `CHANGELOG.md` đổi; hiện 878 393 byte, SHA-256 `b53128882aed29b924c965e45248f7fd61d7c5b293f5c52f66803ade1ffc1f35` | Có |
| Băm toàn manifest | package_hash = content_hash | Tính lại theo công thức path/size/SHA-256 của mã: cùng `7033ea1d370df0330e8608ffd11097147a40c2983690b581ce3d56593a071716` | Có |
| Lượt 8 bỏ số dòng biên nhận | “Bỏ số, không thay số mới” | Chú thích BN4 vẫn viết “khối dài **50** dòng”. HEAD có khoá ở 68, nội dung 69–118: đúng 50 dòng, 5 object | Số hiện đúng; lời khai đã bỏ số không đúng |
| Số dòng/byte verdict bất biến | 161/28 955; 259/43 791; 285/48 843; 296/51 844; 271/42 310 | Đếm byte/dòng cả năm verdict, băm và đọc blob tại từng `evidence_url` ghim commit: đều khớp. Đếm tiêu đề P1/P2/P3: 0/1/1, 0/7/0, 0/6/0, 0/5/0, 0/8/0 | Có |
| Mục lục PR497 | 5 mục lục + 2 cảnh báo | README có đúng 5 hàng mục lục ở 281–285 và 2 hàng cảnh báo ở 19–20 | Có |
| Chuỗi bộ đếm biên nhận | 49/102 → 50/103 → 51/104 → 52/105 → 53/106 → 57/110 | Checkout từng SHA trên bản chép rồi chạy validator: khớp tại `4d2a6f6`, `4e6a2d5`, `25974e7`, `f6ec9c0`, `e27d839`, `8de21be`; mỗi lần rc=0, 0 vi phạm. Diff merge `865adbd` mang đúng bốn receipt #492 | Có |
| Phiên bản công cụ | actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0; chỉ hai được ghim | Probe thực khớp; YAML ghim actionlint/jsonschema, shellcheck `ban_ghim: null`; lệnh cài CI không chỉ định phiên bản shellcheck | Có |

**Cổng chạy lại trên bản chép nguyên vẹn.** Bảng EVIDENCE có 11 lệnh; ngoài bảng còn phép thử `golden-test --strict --json` dự kiến rc=2. Đã chạy cả 12 cách gọi này; không tính lệnh bị từ chối là cổng đạt và không kết luận đã chạy đủ CI.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| `python3 ops/lease_publish_test.py` | 146/146, bỏ qua 0 | rc=0; 146/146 đạt, đã chạy 146, bỏ qua 0 | Có |
| `python3 ops/bien_nhan_v2.py --root .` | 57 v2, 11 legacy, 42 nợ, tổng 110 | rc=0; đúng các bộ đếm; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC | Có |
| `python3 ops/cong_cu.py kiem-tra --json` | DAT, canary DAT | rc=0; tổng DAT, canary DAT | Có |
| `python3 ops/cong_cu_test.py` | 23 ca, 18 đột biến, lỗi đột biến 0 | rc=0; 23/23 đạt, bỏ qua 0; 18 đột biến, lỗi đột biến 0 | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | ok, 180/180 | rc=0; ok=true, expected=checked=180, failed/extra_files/errors rỗng, package_hash_match=true | Có |
| `python3 scripts/tl.py golden-test --json` | ok | rc=0, ok=true | Có |
| `python3 scripts/tl.py determinism-audit --strict --json` | ok | rc=0, ok=true | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` | ok | rc=0, ok=true | Có |
| `python3 scripts/tl.py workflow-audit --strict --json` | rc=0 | rc=0, ok=true, errors rỗng | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 | rc=0; 7 tệp, 0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc=0 | rc=0; 46 ADR/46 hàng, ngoại lệ trạng thái 0016 được khai rõ | Có |
| `python3 scripts/tl.py golden-test --strict --json` | Không nhận cờ; rc=2 | rc=2, `unrecognized arguments: --strict` | Có; phép thử âm |

**Đột biến — báo cả hai chiều.** Chỉ dùng fixture có sẵn và thay đổi vô hại về số, điều kiện, sự có mặt của hiện vật. Mỗi ca dưới bắt đầu từ bản đã phục hồi; các kiểm tra nền tương ứng xanh trước khi đột biến và xanh sau khi phục hồi.

| đột biến trên bản chép | cổng / phép đo | kết quả |
|---|---|---|
| Đổi điều kiện chạy canary thành `if False` | Gọi riêng `t13_actionlint_bien_mat_giua_probe_va_canary` | rc=0 → **1** → 0; assertion đúng về canary bị nuốt. Chạy bản đột biến khi thiếu shellcheck cho tổng DAT/rc=0, xác nhận canary là phần đang chặn ở bản thật |
| Lần lượt bỏ verdict của từng lượt 1–5 | Gọi riêng t26 và t27 | **5/5** bị t26 chặn, rc=1; **5/5 vẫn qua t27**, rc=0. Phạm vi bảo vệ phải là t26 + t27 |
| Lần lượt bỏ receipt của từng lượt 1–5 | t27 | **5/5** bị chặn, rc=1 |
| Lần lượt bỏ đúng hàng mục lục của từng lượt 1–5, giữ hàng cảnh báo | t27 | **5/5** bị chặn, rc=1 |
| Đổi Ubuntu 37 success/4 skipped thành 36/5, vẫn tổng 41 | release-verify strict trước/sau tái sinh manifest; doc-claims-check strict | Manifest cũ: **rc=2**, sai băm CHANGELOG. Sau `release-manifest --out RELEASE_MANIFEST.json`: **cả hai cổng rc=0**, lời khai sai sống |
| Đổi cha thứ nhất ở bảng §1 từ `00e017a` thành commit có thật `c00c88a` | Cùng hai cổng và trình tự trên | Manifest cũ: **rc=2**. Tái sinh: **cả hai rc=0**; phép kiểm DAG riêng xác định đó không phải cha thật |
| Đổi “khối dài 50 dòng” thành “51 dòng” trong chú thích BN4 | t26, t27, bien_nhan_v2, doc-claims-check strict, release-verify strict | **Cả năm rc=0**; validator vẫn 57/110. Văn xuôi sai sống qua đúng các cổng đã thử |

Các lệnh gọi riêng ca test, thực hiện **từ gốc bản chép**:

```sh
python3 -c "import sys; sys.path.insert(0,'ops'); import cong_cu_test as t; t.t13_actionlint_bien_mat_giua_probe_va_canary()"
python3 -c "import sys; sys.path.insert(0,'ops'); import lease_publish_test as t; t.t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()"
python3 -c "import sys; sys.path.insert(0,'ops'); import lease_publish_test as t; t.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()"
```

Sự sống sót của văn xuôi chỉ xác định giới hạn những cổng vừa chạy, **không** chứng minh mọi cổng đều mù và **không** tạo yêu cầu xây cổng ngữ nghĩa mới. Suite lease còn tự báo catalog A0 có 34/37 đột biến bị giết, 3 sống có chủ đích, tín dụng giả 0; không đổi báo cáo đó thành “mọi đột biến đều bị giết”, cũng không review lại phần #492 ngoài diff.

### van-giu-so-dong-trong-chu-thich-khai-da-bo-so  [P2]  Bản vá lượt 8 vẫn thay số dòng ngay trong câu khai không thay số mới

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-4-codex-verdict.receipt.yaml:21–22`; `commit-messages.txt:6–9`.

VẤN ĐỀ: Chú thích vẫn ghi “khối dài **50** dòng”, rồi ngay dòng kế kết luận “Bỏ số, không thay số mới.” Thông điệp commit cũng khai đã bỏ số. **50 hiện đúng**, nên đây không phải cáo buộc đếm sai 50: sai là lời khai đã loại phép đếm khỏi chú thích trong khi lại đưa một số thay thế vào đó. Nó cũng chưa thực hiện yêu cầu cụ thể của lượt này là bỏ số dòng của biên nhận có thể đổi. Cụm 45 được trích như lỗi lịch sử không làm biến mất mệnh đề thay thế 50, vốn không neo snapshot.

ĐÃ THỬ VÁ: có — trên bản chép, xoá trọn hai dòng chú thích 21–22, giữ mô tả “NĂM OBJECT nhiều dòng”. Không sửa verdict bất biến, không thay 50 bằng số khác, không sửa lịch sử commit hay cây gốc.

ĐÃ THỬ NGHIỆM: Quét các receipt bằng mẫu `[0-9]+`, không giới hạn chữ số; đọc cả chú thích và scalar YAML đã nối khoảng trắng, đồng thời rà phần r362/README. Đo `nam_finding` tại HEAD: khoá dòng 68, nội dung 69–118, **50 dòng / 5 object**. Các cặp số lịch sử có neo `f6ec9c0`, `3c82ae3`, `e27d839` được đọc lại và khớp; các số verdict ghim băm cũng khớp, không bị gộp vào finding này. Sau bản vá xoá hai dòng: hai lệnh gọi t26/t27 ở trên, `python3 ops/bien_nhan_v2.py --root .` và `python3 scripts/tl.py doc-claims-check --strict --json` đều **rc=0**; validator 57/110, 0 vi phạm. Đột biến 50 thành 51 vẫn xanh ở năm cổng như bảng trên, nên cổng xanh không chứng minh chú thích đã đúng.

ĐỘ TIN: cao

### ket-luan-ref-sao-luu-khong-co-ci-vuot-cau-hinh  [P2]  EVIDENCE bỏ sót workflow_dispatch khi kết luận không có lượt CI nào

TỆP/DÒNG: `EVIDENCE.md:31–34`; đối chiếu `cay-kho/.github/workflows/ci.yml:10–20` và `:43–47`.

VẤN ĐỀ: EVIDENCE gắn nhãn “đo được” cho suy luận `ci.yml` chỉ bắn push trên master và pull_request, nên ref sao lưu “không kích hoạt lượt CI nào”. YAML còn khai **`workflow_dispatch`**; ma trận cũng xử lý event này tường minh. Đọc cấu hình chỉ chứng minh push trực tiếp lên ref sao lưu không khớp bộ lọc `push.branches`. Nó không chứng minh ref ấy chưa từng được chạy tay hay có số lượt CI bằng 0. Đây là lời khai rộng hơn phép đo trong gói; không phải bằng chứng rằng một lượt CI trên ref ấy đã thực sự xảy ra.

ĐÃ THỬ VÁ: có — trên bản chép EVIDENCE, thay câu bao trùm bằng: push trực tiếp vào ref sao lưu không khớp cò push; workflow còn `pull_request` và `workflow_dispatch`; có lượt CI thực nào trên ref là KHÔNG ĐO ĐƯỢC từ gói. Không đổi workflow và không gọi CI.

ĐÃ THỬ NGHIỆM: Parse YAML bằng `yaml.safe_load`, đọc khoá `on` (PyYAML còn có thể biểu diễn khoá này là boolean `True`): **ba** event `push`, `pull_request`, `workflow_dispatch`; `push.branches=['master']`. Đối chiếu tên `claude/handoff-tra-luat-repo-2ak5th-wip` với bộ lọc: không khớp. Đọc trực tiếp `git --git-dir=kho.git show refs/heads/claude/handoff-tra-luat-repo-2ak5th-wip:.github/workflows/ci.yml` cũng thấy cùng ba event. Bản vá văn bản được đối chiếu lại với cấu hình, đạt. Lịch sử run GitHub **KHÔNG ĐO ĐƯỢC** vì không mạng và không có response/log tương ứng trong gói.

ĐỘ TIN: cao

## GIỚI HẠN

- Không truy cập mạng. Raw `ls-remote` là attestation về máy chủ; so raw/mirror chứng minh tính nhất quán của hai hiện vật được giao, không xác thực raw đến từ GitHub. Script `dung-goi-review.sh` không có trong gói/cây: không kiểm được trình tự fetch, thao tác chụp, hay nhánh dừng rc=3 của script; chỉ kiểm được kết quả ref cuối cùng.
- Không xác thực run `34391481045`, lịch sử CI khác, PR/Issue/review/actor/authorization, quyết định không đốt CI hay quyết định đóng chuỗi land-evidence. §1 có bằng chứng Git/bookkeeping cục bộ, nhưng vế hậu-merge gate và do đó kết luận `landed` vẫn dựa vào thuật lại. Các số Issue 128/101/bốn Issue/#498 và diễn biến Windows đỏ có nhãn nguồn phù hợp; không được nâng thành phép đo hôm nay.
- Không có runtime artifact của tám lượt cũ. Byte/hash/OID/số tiêu đề có thể đo lại; việc reviewer cũ đã đọc/chạy gì, model nào phục vụ, các scalar runtime và identity GitHub không thể xác thực từ lời khai receipt.
- Đã chạy các lệnh nêu trong bảng, A/B và các đột biến nêu rõ; không chạy toàn bộ workflow CI, Windows thật, LIVE, publish, merge hay deploy. Phép đối chiếu nền/head của runtime dùng AST toàn tệp; không suy từ đó rằng mọi môi trường thực thi đã được kiểm.
- Không tự soạn nội dung tấn công. Những hướng cần chuỗi thoát, đồng tự Unicode hoặc đường dẫn vượt cây không được thử. Các fixture nhạy cảm nếu có trong suite là hiện vật sẵn có của kho.
- Phiên review dùng công cụ thực thi cục bộ OpenAI/Codex; không dùng danh tính người vận chuyển verdict để suy danh tính model của phiên cũ. Một assertion nháp của giàn tổng kết đoán sai số lượt gọi lệnh đột biến đã được bỏ và đếm lại từ kết quả; không tính lỗi giàn đo đó thành lỗi PR hay phép thử đạt.
- Đã dọn các bản chép, script và log tạm do lượt này tạo; chỉ để lại `VERDICT.md` ở gốc sandbox. Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**; HEAD vẫn `8de21bee0460bfe89b13ece2bafaa3a113593441`.
