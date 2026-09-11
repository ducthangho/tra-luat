verdict: changes_requested
reviewed_sha: c912945c0bcbec5e602ff931d2490d18c2a0d47d

Lượt 8: **0 P1 / 2 P2 / 0 P3**. Nội dung gốc §1/§2, chú thích `tong_hop` và manifest không phát hiện sai mới trong phần đo được. Hai P2 dưới đây thuộc biên nhận đã nhập và gói bằng chứng.

Reviewer: Codex/OpenAI, dùng công cụ shell trong sandbox; không xác thực model/session của các reviewer trước. Cây được review: `3e3c352131c5e29c14054a72929500ff3bc1b037`. Phạm vi Git là `c00c88a..c912945`; không chấm nội dung r363 hoặc hồ sơ PR492.

## BẢNG ĐO

Các lệnh chạy cổng dùng bản sao nguyên cây và `.git` trong thư mục tạm của sandbox. `TMPDIR`, cache và cấu hình Git phụ của phép thử đều đặt trong sandbox. Không cài công cụ, không gọi mạng, không sửa `cay-kho/`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact checkout | HEAD `c912945…`, tree `3e3c352…`, detached, đầy đủ | `git rev-parse HEAD HEAD^{tree}`, `symbolic-ref -q HEAD`, `rev-parse --is-shallow-repository`: đúng hai OID trên, detached, `false` | Có |
| Khối cấu hình gói | 9 trường trong EVIDENCE và `do-goi.txt` | Parse hai khối rồi so cấu hình thật: **9/9** khớp; origin trỏ `kho.git` trong sandbox, `core.abbrev=7` | Có |
| Số ref mirror | 325 = 324 + 1 giao hàng | `git -C kho.git for-each-ref … refs/heads`: **325**; bỏ đúng `refs/heads/pr497-head` còn **324** | Có |
| Tệp ref thô | 324 dòng, SHA-256 bắt đầu `51505d300d0a66c7` | **324 dòng / 26 116 byte**; SHA-256 `51505d300d0a66c72a00d94880809f01a61b1212709cd04eeae8527ca2b29a42` | Có về byte; xuất xứ và giờ chụp là ATTESTATION |
| Kết quả canh ref sau fetch | EVIDENCE thuật lại “mù = 0”, nhánh vừa bổ sung mang r364 | So hai hiện vật giao, đã bỏ ref giao hàng: **thiếu 1 / thừa 1 / khác OID 1**. Object đầu nhánh thiếu cũng không có | Gói chưa phản ánh kết quả ấy; P2 bên dưới |
| Quét r362 trên mirror | Hai ref, cùng nhánh công việc và bản sao lưu | Đọc `CHANGELOG.md` từ từng ref, loại ref giao hàng: đúng `claude/handoff-tra-luat-repo-2ak5th` và nhánh cùng tên có hậu tố `-wip` | Có; không suy thành quét GitHub |
| Diff được giao | 14 tệp, +2996/−5, 19 commit | `git diff --numstat c00c88a..HEAD`, `rev-list --count`: đúng; `diff.patch` và `numstat.txt` khớp byte với Git | Có |
| CHANGELOG sau merge | r363 → r362 → r361; không mất mục | Đúng thứ tự. Bỏ nguyên mục r362 khỏi HEAD khôi phục **đúng byte** `c00c88a:CHANGELOG.md` | Có |
| README sau merge | PR497: 5 mục lục + 2 cảnh báo; PR492: 4 + 6 | Đếm theo từng bảng: đúng **5+2 / 4+6**; toàn bộ hàng PR492 nguyên byte so base | Có; chỉ kiểm bảo toàn phía master |
| Dẫn vị trí r361 | Đã gọi tên r361 | Câu mở đầu gọi `r361`; “ngay trên” chỉ còn trong đoạn kể và bác bản cũ. Các dẫn vị trí còn lại trong r362 trỏ nội dung cùng mục | Có; không tìm thêm dẫn vị trí sai vì merge |
| §1 — merged | `8cee941`, hai cha `00e017a` + `01e7f77` | `git show -s --format='%H %P' 8cee941`: hai cha đầy đủ là `00e017af102bc8355e0c276d2d813e20620ddb42` và `01e7f77d707cb093b5ba6d9b9d8577f40d025488` | Có về đồ thị Git |
| §1 — quan hệ tổ tiên | Hai cha thuộc merge, merge đã vào cây | `merge-base --is-ancestor` cho từng cha → `8cee941`, rồi `8cee941` → HEAD: **rc=0 cả ba** | Có; không tự xác thực trạng thái PR trên GitHub |
| §1 — hậu-merge gate | Run `34391481045`, push/master, head `8cee941`, attempt 1, hai job success | **KHÔNG ĐO ĐƯỢC** kết quả hoặc metadata Actions: không có response/log run trong gói. Nhãn “thuật lại” đứng ngay trước bảng và quy tắc nguồn ở đầu r362 bao trùm CI | Nhãn nguồn đúng; không phải xác nhận CI độc lập |
| §1 — bảng CI | 41 bước; Ubuntu 37+4+0, Windows 35+6+0 | Hai phép cộng đều **41**. YAML tại `8cee941` và HEAD giống byte: **40 bước khai báo = 8 setup + 31 cổng + 1 upload**. Không đồng nhất số bước YAML với số bước runtime Actions | Số học khớp; số runtime vẫn THUẬT LẠI |
| §1 — skipped | Hình dạng lane LAND lặp trên ba lượt master | Cấu hình có điều kiện PR, Linux/Windows và LAND/WORKER phù hợp lời kể; không có log để đối chiếu từng bước hoặc ba lượt chạy | Cơ chế phù hợp; sự kiện KHÔNG ĐO ĐƯỢC |
| §1 — bookkeeping / landed | r359 ghi sổ thay tệp riêng; nay đủ ba vế | r359 có thật, ghi rõ cách bookkeeping thay thế. Quyết định chủ kho và hậu-merge CI là thuật lại. Kết luận `landed` dựa vào phần thuật lại ấy | Không thấy mâu thuẫn; reviewer không tự chứng nhận `landed` |
| §2 — A/B có shellcheck | Công cụ và canary DAT | PATH riêng có 7 executable cần dùng: tổng **DAT**, shellcheck **DAT**, actionlint **DAT**, canary **DAT**, `blocking`, lệnh **rc=0** | Có |
| §2 — A/B thiếu shellcheck | Canary bắt sự suy giảm | PATH thứ hai giống các mục còn lại, bỏ riêng shellcheck: actionlint **DAT**, shellcheck **KHONG_DO_DUOC**, canary **DO**, `blocking`, tổng **DO**, lệnh **rc=2** | Có; lời rút của r361 có phản chứng thật |
| §2 — `--chi` | Không chạy canary | Cả `--chi shellcheck` và `--chi actionlint`, trên cả hai PATH: `canary=[]`, tổng **DAT**, **rc=0**. Riêng shellcheck bị thiếu vẫn **KHONG_DO_DUOC** | Có |
| §2 — đường CI | Cài từng công cụ có `--chi`; G5 quét đầy đủ | Đọc `cai_cong_cu.sh`, YAML và `tong_hop`: đúng. G5 gọi `kiem-tra --json` không có `--chi`, sau bước cài rg | Có về mã; diễn biến Windows đỏ không được tái chạy |
| Chú thích `ops/cong_cu.py` | Mô tả cơ chế; CI cụ thể là thuật lại; không đổi runtime | `ast.dump(ast.parse(base)) == ast.dump(ast.parse(HEAD))` là **True**, không lấy thuộc tính vị trí. Diff chỉ thêm **23 dòng chú thích**; mô tả khớp A/B | Có |
| Các số Issue / #498 | Thuật lại tại chỗ | Các cụm 128, 101, bốn Issue và #498 có nhãn; `30/128 ≈ 23,44%` tính lại được, dữ liệu GitHub thì không | Nhãn đúng |
| Manifest kiểm kê | 180 → 180; chỉ CHANGELOG đổi | Tự đọc byte **180/180 đường dẫn duy nhất**, tính lại từng kích thước và SHA-256: **0 lệch**, tổng **8 172 715 byte**. So map hai manifest: chỉ entry `CHANGELOG.md` đổi, không thêm/bớt entry | Có |
| Manifest hash | Hash gói theo cây hiện tại | `CHANGELOG.md`: **878 393 byte**, SHA-256 `b53128882aed29b924c965e45248f7fd61d7c5b293f5c52f66803ade1ffc1f35`. Release verifier xác nhận cả hash tự thân và cây: `7033ea1d370df0330e8608ffd11097147a40c2983690b581ce3d56593a071716` | Có; tổng byte và hash tổng hợp cũng đổi theo entry ấy |
| Biên nhận 1–5 | Byte/hash, reviewed SHA, số P và neo blob | Tính lại: **5/5** khớp byte/hash/SHA/số P; **5/5** blob neo khớp verdict hiện tại và là tổ tiên HEAD. Số P1/P2/P3 lần lượt **0/1/1, 0/7/0, 0/6/0, 0/5/0, 0/8/0** | Có; không chứng thực runtime hoặc hành vi đọc |
| Vá lượt 7 | Bỏ “143 dòng”, giữ “dạng NGẮN” | Hàng biên nhận lượt 5 trong §3 đúng như bản vá; không còn lời khai tổng số dòng hiện hành tại hàng đó | Đã vá đúng chỗ |
| Quét hết lời khai số dòng biên nhận | Không còn lời khai số dòng PR497 | BN4 dòng 20 vẫn khai khối `nam_finding` **45 dòng**; đo phần năm mục ở dòng **67–116 = 50 dòng** | Không; P2 bên dưới. Các số được trích và bác hoặc ghim lịch sử không tính là lời khai hiện hành |
| `python3 ops/lease_publish_test.py` | 146/146; chạy 146, bỏ 0 | **rc=0; 146/146**, đã chạy=146, bỏ qua=0 | Có |
| `python3 ops/bien_nhan_v2.py --root .` | 57 v2, 11/11 legacy, 42 nợ; tổng 110 | **rc=0; 57 / 11 / 42**, tổng **110**, **0 vi phạm / 0 KHÔNG ĐO ĐƯỢC** | Có |
| `python3 ops/bien_nhan_v2_test.py` | 48/48 ca, 63/63 mutant, 2/2 tự kiểm | **rc=0; 48/48, 63/63 CÓ RĂNG, 2/2** | Có |
| `python3 ops/cong_cu.py kiem-tra --json` | Tổng DAT, canary DAT | **rc=0; DAT / DAT** trên môi trường có đủ công cụ | Có |
| `python3 ops/cong_cu_test.py` | 23 ca, 18 mutant, 0 lỗi mutant | **rc=0; 23/23**, bỏ qua=0; **18 mutant, 0 lỗi** | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | ok, 180=180 | **rc=0; ok=true; expected=checked=180**, failed/extra/missing đều rỗng | Có |
| `python3 scripts/tl.py golden-test --json` | ok | **rc=0; ok=true; 20 ca**; không truyền `--strict` | Có |
| `python3 scripts/tl.py determinism-audit --strict --json` | ok | **rc=0; ok=true; 15 checks**, `full=false` | Có, theo đúng lệnh đã khai |
| `python3 scripts/tl.py doc-claims-check --strict --json` | ok | **rc=0; ok=true; flags=[]**; 368 advisory được khai riêng | Có; không đồng nhất advisory với lỗi |
| `python3 scripts/tl.py workflow-audit --strict --json` | rc=0 | **rc=0; ok=true**, errors/warnings rỗng | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 | **rc=0**, quét 7 tệp, 0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc=0 | **rc=0**, 46 ADR / 46 dòng, khớp 1–1; ngoại lệ 0016 được công khai | Có |
| Phiên bản nền | actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0; chỉ hai được ghim | Probe đúng ba bản; YAML/CI ghim actionlint và jsonschema, shellcheck `ban_ghim: null`. Python 3.11.15, PyYAML 6.0.1 | Có |
| Đột biến tắt canary | t13 có răng | Trên bản sao, đổi điều kiện chạy canary thành luôn sai: gọi riêng `t13_actionlint_bien_mat_giua_probe_va_canary` cho **rc 0→1→0** khi nền/đột biến/khôi phục. CLI thiếu shellcheck lúc đột biến lại **rc=0, DAT** | Cổng test bắt; riêng CLI đã bị làm mất bảo vệ |
| Đột biến bỏ verdict lượt 5 | t26 cộng t27 mới đủ | Gọi riêng từng ca: nền **t26=0/t27=0**; bỏ verdict **t26=1/t27=0**; khôi phục **0/0** | Có cả chiều bắt và không bắt |
| Đột biến bỏ biên nhận / hàng mục lục / hàng cảnh báo | t27 bắt | Ba ca độc lập trên bản sao: **rc=1 / 1 / 1**; lỗi đúng hiện vật bị bỏ; khôi phục **rc=0** | Có |
| Đột biến văn xuôi CI | Hai cổng không bảo đảm ngữ nghĩa | Chỉ đổi hàng Ubuntu của r362 từ **37+4** sang **36+5**, vẫn tổng 41. Manifest cũ: release-verify **rc=2**, bắt hash CHANGELOG. Tái sinh bằng `release-manifest --root . --out RELEASE_MANIFEST.json --json`: release-verify **rc=0, ok=true** và doc-claims **rc=0, ok=true** | CÓ bắt tính toàn vẹn byte; KHÔNG bắt thay lời khai qua hai cổng này |
| Whitespace / giữ nguyên cây | Cây review sạch | `git diff --check c00c88a..HEAD`: **rc=0**. Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**; HEAD/tree không đổi | Có |

### so-dong-khoi-nam-finding-van-con-sai  [P2]  Biên nhận lượt 4 còn khai 45 dòng cho khối thực có 50 dòng

TỆP/DÒNG: `ops/reviews/pr497-review-4-codex-verdict.receipt.yaml:20`; phần được đếm ở dòng 67–116, khóa `nam_finding` ở dòng 66.

VẤN ĐỀ: Chú thích hiện hành viết “`nam_finding` chiếm **45** dòng cho 5 finding”. Đây không phải trích dẫn bản cũ hoặc kết quả ghim SHA. Parse YAML xác nhận năm object, nhưng phần nội dung từ object đầu đến dòng cuối của object thứ năm dài **50 dòng**; tính thêm dòng khóa là 51. Vì vậy bản vá lượt 7 đã bỏ đúng “143 dòng” ở §3, song khẳng định đã hết lời khai số dòng PR497 vẫn chưa đúng. Con số này nằm ngay trước đoạn giải thích vì sao phải xóa phép so số dòng.

ĐÃ THỬ VÁ: có — trên bản sao, thay cả câu bằng “`nam_finding` gồm năm object nhiều dòng. Bài học vẫn được ghi ở `CHANGELOG`.” Xóa con số, không thay bằng một số mới. `yaml.safe_load` trước và sau bằng nhau. Không sửa biên nhận thật hoặc verdict đã neo băm.

ĐÃ THỬ NGHIỆM: `nl -ba …receipt.yaml` đối chiếu với `yaml.compose`: khóa ở 66, mục đầu ở 67, nội dung cuối ở 116; **116−67+1=50**, năm object. Sau vá, gọi riêng `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi` và `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc` đều **rc=0**; `python3 ops/bien_nhan_v2.py --root .` **rc=0**, 57 v2 / tổng 110 / 0 vi phạm. Các cổng này cũng xanh trước vá: chúng không bắt lời khai số dòng trong chú thích. Không đề nghị xây cổng ngữ nghĩa.

ĐỘ TIN: cao

### goi-ref-chua-phan-anh-ket-qua-sau-fetch  [P2]  Gói giao vẫn thiếu đúng ref mà EVIDENCE thuật lại đã hết mù

TỆP/DÒNG: `EVIDENCE.md:33–36`, đối chiếu `ls-remote-may-chu.txt` với refs của `kho.git` và `cay-kho/`.

VẤN ĐỀ: Hồ sơ thuật lại phát hiện thiếu `claude/land-500-bookkeeping`, rồi “Sau fetch: mù = **0**”. Nhưng mirror được giao vẫn ở trạng thái lệch với chính tệp ref thô được giao. Sau khi loại ref giao hàng, hai tập cùng 324 tên nhưng:

- Thiếu `refs/heads/claude/land-500-bookkeeping`.
- Thừa `refs/heads/pr487-merge`.
- Ref chung `claude/pr491-land-va-findings-wip` còn khác OID: raw `9e78e19e5e3247d910c061a1171f4783ee0a3e10`, mirror `dd4a3ae8e551ea07445c79fa3274249285f15e42`.

Clone cũng thiếu ref đầu tiên và giữ hai ref cũ tương ứng. Object `dae1aedde87cf8b7b714061be21d476ab7e6a9c2` mà raw gán cho nhánh thiếu không có trong cả clone lẫn mirror. Do đó không tái đọc được r364 và không tái lập được kết quả sau-fetch từ gói hiện tại. Chín trường cấu hình vẫn khớp hoàn toàn: phép đếm đúng không phát hiện được độ lệch này.

Finding này là lệch giữa gói giao và kết quả sau-fetch được dùng trong hồ sơ, **không phải kết luận rằng máy điều phối chưa fetch hoặc lời kể về GitHub là sai**. Tiêu đề “chạy ở phía điều phối” phân loại đúng nguồn, nhưng chưa nói gói giao vẫn thiếu ref đó. Cần dựng lại gói từ bộ ref sau fetch, hoặc ghi rõ giới hạn này ngay cạnh kết quả sau-fetch để người nhận không dùng nó làm bằng chứng rằng mirror đã đủ.

ĐÃ THỬ VÁ: có — thử bổ sung vào bản sao `EVIDENCE.md` cảnh báo riêng cho gói lượt 8, ghi thiếu/thừa/khác OID như trên và tách kết quả sau-fetch của điều phối khỏi trạng thái mirror giao. Không tự thêm ref trỏ object chưa có, không sửa mirror thật. Phương án dựng lại mirror cần hiện vật bổ sung từ điều phối.

ĐÃ THỬ NGHIỆM: `git -C kho.git for-each-ref --format='%(objectname) %(refname)' refs/heads`; parse raw thành map tên→OID, bỏ đúng `refs/heads/pr497-head`, rồi lấy hai hiệu tập và so OID của giao: **324/324, thiếu 1, thừa 1, khác OID 1**. `git -C cay-kho for-each-ref … refs/remotes/origin` xác nhận cùng trạng thái tương ứng. `git -C kho.git cat-file -t dae1aedde87cf8b7b714061be21d476ab7e6a9c2` và cùng lệnh trên clone đều **rc=128**, không có object. Không gọi `ls-remote` ra mạng; không coi raw là xác thực GitHub.

ĐỘ TIN: cao về độ lệch hiện vật; vừa về thời điểm gói lệch so với thao tác fetch của điều phối.

## GIỚI HẠN

- **KHÔNG ĐO ĐƯỢC GitHub**: trạng thái PR/Issue, approval, actor, authority, thời điểm, run/job/bước CI, nguồn và giờ chụp raw. Đặc biệt không độc lập chứng nhận #490 `landed`, không xác nhận CI của `c912945` đã chạy hay chưa chạy.
- **KHÔNG ĐO ĐƯỢC hậu-fetch của kho điều phối** hoặc nội dung r364 trên nhánh đang thiếu. Độ lệch hai hiện vật giao là đo được; nguyên nhân và thời điểm tạo độ lệch thì không.
- Chạy trên Linux và công cụ sẵn có; không chạy runner Windows/macOS. A/B xác nhận cơ chế shellcheck/canary, không tái hiện sự kiện Windows được thuật lại.
- Đã chạy đúng **12 lệnh** được giao, không gọi đó là đủ 31 cổng CI. `determinism-audit --strict` báo `full=false`. Không chạy LIVE/deploy hoặc dùng cổng xanh để suy ra quyền land.
- Kết quả lịch sử của reviewer và mọi scalar runtime/identity/submitter vẫn là ATTESTATION; so byte/blob/OID chỉ xác nhận hiện vật, không xác nhận ai đã đọc hoặc model nào đã phục vụ.
- Đột biến văn xuôi chỉ chứng minh giới hạn của **hai cổng đã chạy**. Không suy sang mọi cổng, không yêu cầu cổng ngữ nghĩa mới. Lần thử văn xuôi đầu dừng ở assertion của giàn giáo do chuỗi có nhiều bản trong CHANGELOG; đã giới hạn đúng mục r362 rồi chạy đủ các lệnh và ghi kết quả ở bảng trên.
- Phần r363/PR492 chỉ được dùng để kiểm hợp nhất không làm mất phía master; không đưa nội dung của chúng thành finding.
