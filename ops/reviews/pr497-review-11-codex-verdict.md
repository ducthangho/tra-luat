verdict: approve
reviewed_sha: 5271e997a22282d9f840ab8d54470022fc610f02

## BẢNG ĐO

Review độc lập lượt 11: **0 P1 / 0 P2 / 0 P3**. Không phát hiện lời khai sai mới trong phạm vi được giao. Finding lượt 10 đã được vá đúng. Đây là kết luận review offline trên SHA trên, không xác nhận trạng thái GitHub hay quyền land.

Base: `27c413c3e531800431cad9db4452d7236505a5a9`; tree: `acf0dc5d63300c32affa2b31cc3bdcd25c5b0fb0`. Reviewer: OpenAI Codex, thực thi lệnh cục bộ qua công cụ, transport machine; không suy danh tính model của các lượt trước từ biên nhận.

Mọi phép chạy dùng bản sao đầy đủ trong `tmp-review/` thuộc sandbox; `TMPDIR`, `TEMP`, `TMP` nằm trong đó, tắt ghi bytecode. Không cài công cụ, không gọi mạng, không sửa `cay-kho/`. Nền đo: Linux, Python 3.11.15, Git 2.43.0, PyYAML 6.0.1, actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0; `core.abbrev=7`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Cây giao review | Detached, đầy đủ, đúng SHA/tree, sạch | `rev-parse HEAD`, `HEAD^{tree}` đúng hai OID trên; `symbolic-ref -q HEAD` rc=1; `--is-shallow-repository=false`; status rỗng | Có |
| Cấu hình gói | `EVIDENCE.md` chép nguyên `do-goi.txt`; origin là mirror trong sandbox; abbrev 7 | Khối fenced bằng nguyên byte nội dung `do-goi.txt`; `git config --local` trả đúng đường `r11/kho.git` và 7 | Có |
| Ref mirror/raw | 326 = 325 + 1 giao hàng; raw 324; thiếu 0, thừa 1, lệch OID 0 | Đọc `for-each-ref refs/heads` trên mirror, bỏ riêng `pr497-head`: 325; so tập tên và OID với raw: thiếu 0, thừa đúng `pr487-merge`, lệch 0. Mọi OID raw đều có object trong clone | Có; không xác thực nguồn GitHub |
| Byte raw | 324 dòng, SHA-256 bắt đầu `89a9ff724c5d774e` | 324 dòng; SHA-256 `89a9ff724c5d774e6bbf97a90fd75920fe413bff991446e76d60894ebb540a07` | Có |
| Ref mang mục r362 | Hai ref, đều của nhánh này; loại ref giao hàng khi đếm | Đọc heading r362 trong `CHANGELOG.md` của đủ 325 head: đúng `claude/handoff-tra-luat-repo-2ak5th` và bản `-wip` | Có |
| CI của ref sao lưu | Push trực tiếp không khớp bộ lọc; số lượt CI không đo được | YAML khai `push.branches=[master]`, `pull_request`, `workflow_dispatch`. Không có cơ sở kết luận ref chưa từng chạy tay | Nhãn nguồn đúng |
| Phạm vi PR | 14 tệp, +3004/−5, 24 commit, base `27c413c` | `git diff --numstat 27c413c HEAD`, `rev-list --count 27c413c..HEAD`, `merge-base`: đúng; diff và numstat tái sinh khớp nguyên byte hai tệp giao kèm | Có |
| §1: merged | `8cee941`, cha `00e017a` + `01e7f77` | `git show -s --format='%H %P' 8cee941`: hai cha đúng thứ tự; merge là tổ tiên của base và HEAD | Có, từ object Git cục bộ |
| §1: bookkeeping | Mục r359 ghi sổ #490 | r359 có sẵn trong base, hiện ở `CHANGELOG.md:976`; phần bookkeeping tại dòng 1074–1075 nêu rõ dùng mục này thay hiện vật land riêng | Có về nội dung; chỉ thị chủ kho vẫn là thuật lại |
| §1: hậu-merge gate / landed | Run `34391481045`, push/master, head `8cee941`, attempt 1; cả hai job success | Không có response/log Actions để tái đo run, attempt, giờ chạy, kết luận job. §1:245–254 ghi “thuật lại”; giới hạn nguồn đầu r362 bao phủ run/job/bước CI | Nhãn đúng; KHÔNG ĐO ĐƯỢC sự kiện |
| Số học bảng CI | Ubuntu 37+4+0; Windows 35+6+0; mỗi nền 41 bước | Hai tổng đều 41. YAML tại `8cee941` có 40 bước khai báo; điều kiện trên master phù hợp 4 bước skip Ubuntu và 6 Windows. Điều này không chứng minh 41 bước của run đã thực sự chạy hay thành công | Khớp số học/cấu hình; kết quả run là thuật lại |
| Quy mô cổng CI | 31 bước cổng, phép chạy tại chỗ không đủ bộ | YAML có 37 bước `run`; trừ 6 bước chuẩn bị (LF và 5 bước cài) còn 31. Không đánh đồng số này với số ca test hoặc 41 bước trong bảng Actions | Có |
| §2, toàn bộ công cụ, CÓ shellcheck | Canary DAT, blocking | `python3 ops/cong_cu.py kiem-tra --json`: rc=0, tổng DAT; canary DAT, `chinh_sach=blocking`, bắt SC1003 với rc nội bộ 1 | Có |
| §2, toàn bộ công cụ, THIẾU shellcheck | Shellcheck KHONG_DO_DUOC; canary DO kéo tổng đỏ | Cùng lệnh, cùng cây, chỉ gỡ shellcheck khỏi PATH riêng: rc=2, tổng DO; canary DO, báo SUY_GIAM, rc actionlint nội bộ 0. Bảy probe khác giữ nguyên kết quả | Có; bác câu bị rút của r361 |
| `--chi` tắt canary | Không canary khi chọn một công cụ; shellcheck thiếu vẫn có tổng DAT | Chạy `kiem-tra --chi shellcheck --json` và `--chi actionlint --json`, mỗi lệnh có/không shellcheck: cả bốn rc=0, tổng DAT, `canary=[]`; shellcheck thiếu vẫn hiện KHONG_DO_DUOC | Có |
| Chú thích `tong_hop` | Chỉ chú thích mới, hành vi giữ nguyên | `ast.dump(ast.parse(...))` giữa base và HEAD bằng nhau, không gồm thuộc tính vị trí. Diff đúng +23 dòng comment; `if chi is None`, xử lý optional và blocking phù hợp phép A/B | Có |
| Nguồn diễn biến Windows / Issue | Cơ chế đo được; lượt CI đỏ, #498 và các số Issue là thuật lại | Đọc `cai_cong_cu.sh` thấy `--chi`; G5 gọi quét đầy đủ, đứng sau bước rg bắt buộc. §2 và comment mới đều phân biệt cấu hình cho phép với sự kiện đã xảy ra; số 128/101/bốn Issue/#498 có nhãn | Đúng phạm vi nguồn |
| Pin công cụ | Chỉ hai trong ba phiên bản được CI ghim | `ci.yml:93` ghim jsonschema 4.26.0; dòng 97 đặt AL_VER 1.7.7; shellcheck tại dòng 101 không nêu bản, YAML có `ban_ghim: null` | Có |
| Manifest từng tệp | 180 mục; chỉ CHANGELOG đổi hash | Tự đọc đủ 180 đường duy nhất, tính `len(bytes)` và SHA-256: 0 lệch, tổng 8.181.812 byte. So từng entry với base: chỉ CHANGELOG đổi; giao tập tệp diff với manifest cũng chỉ có CHANGELOG | Có |
| Manifest tổng hợp | Hash gói và content cùng `745b1a7f…` | Tính lại từ path/size/hash theo thứ tự manifest: `745b1a7f5c15e69de1111e074041fcf489c469c28de699c5cfd871005c3f54ba`, khớp cả hai trường | Có |
| CHANGELOG trong manifest | 887.490 byte, hash `fc27d449…` | 887.490 byte; SHA-256 `fc27d4490938bae9c61d33a7f1e4507d0807e9ccc843b1633eb4b1db5fbe5a8c` | Có |
| Vá lượt 10 | Chuỗi dừng ở `e27d839`, bỏ ô số “head hiện tại” | `git diff HEAD^ HEAD -- CHANGELOG.md` xác nhận bỏ ô cũ. Quét toàn CHANGELOG/EVIDENCE: cụm này còn ở CHANGELOG:598,601 và EVIDENCE:71, đều giải thích việc bỏ ô; không còn phép gán số cho nhãn đó | Đã vá |
| Chuỗi bộ đếm ghim SHA | 49/102 → 50/103 → 51/104 → 52/105 → 53/106 | Checkout lần lượt trong bản sao và chạy `python3 ops/bien_nhan_v2.py --root .`: đúng tại `4d2a6f6`, `4e6a2d5`, `25974e7`, `f6ec9c0`, `e27d839`; cả năm rc=0 | Có |
| Năm hồ sơ PR497 và mục lục | Năm verdict/receipt, 5 hàng mục lục + 2 cảnh báo của PR497 | Đếm đúng 5+5, 5+2; byte/dòng/hash từng verdict khớp; năm blob ghim khớp byte và đều là commit thêm tệp đầu tiên. P1/P2/P3 lần lượt 0/1/1, 0/7/0, 0/6/0, 0/5/0, 0/8/0 | Có |
| Đóng băng hồ sơ | Không có hồ sơ lượt 6 trở đi trong cây | Không có verdict/receipt PR497 cho lượt 6–11. Các hồ sơ master ngoài phạm vi không được chấm | Có |

Không thấy ô thứ tư cùng loại trong phần PR này thêm. Số `59/112` ở bảng cổng là phép đo cho cây được review, và EVIDENCE neo rõ `5271e99`; các cặp `57/110` và `59/112` trong đoạn giải thích là diễn biến lịch sử, không phải ô “head hiện tại” còn sống.

Các cổng đã chạy lại trên bản sao nguyên vẹn của SHA được review:

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| `python3 ops/lease_publish_test.py` | 146/146; chạy 146, bỏ qua 0 | rc=0; 146/146; chạy 146, bỏ qua 0 | Có |
| `python3 ops/bien_nhan_v2.py --root .` | 59 ĐẠT v2, 11 legacy, 42 nợ, tổng 112 | rc=0; 59 ĐẠT v2, 11/11 legacy, 42 nợ; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC; tổng 112 | Có |
| `python3 ops/cong_cu.py kiem-tra --json` | DAT, canary DAT | rc=0; DAT, canary DAT | Có |
| `python3 ops/cong_cu_test.py` | 23 ca, 18 đột biến, 0 lỗi đột biến | rc=0; 23/23, bỏ qua 0; 18 đột biến, 0 lỗi đột biến | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | ok; 180=180 | rc=0, ok=true, expected=checked=180, failed=[], extra_files=[] | Có |
| `python3 scripts/tl.py golden-test --json` | ok | rc=0, ok=true | Có |
| `python3 scripts/tl.py determinism-audit --strict --json` | ok | rc=0, ok=true | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` | ok | rc=0, ok=true | Có |
| `python3 scripts/tl.py workflow-audit --strict --json` | rc=0 | rc=0, ok=true, errors=[] | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 | rc=0; 7 tệp, 0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc=0 | rc=0; 46 ADR, 46 dòng, khớp 1–1 | Có |
| `python3 scripts/tl.py golden-test --strict --json` | Không nhận strict, rc=2 | rc=2, unrecognized arguments: --strict | Có; phép thử âm |

EVIDENCE liệt kê **11 lệnh trong bảng và một lệnh thử âm ngay dưới bảng**; 12 lệnh ở đây gồm cả phép thử âm, không phải 12 cổng đạt.

Đột biến trên bản sao riêng, từng ca phục hồi trước ca kế tiếp. Gọi ca có sẵn bằng `python3 -c "import runpy; d=runpy.run_path('ops/lease_publish_test.py'); d['<tên hàm>']()"`; tương tự với `ops/cong_cu_test.py`. Các hàm đích là `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi`, `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc`, `t13_actionlint_bien_mat_giua_probe_va_canary`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Tắt vòng canary: đổi điều kiện `if chi is None` thành `if False` | Có chốt chống mất canary | t13 nền rc=0 → mutant rc=1 với `TinHieuChotCa: canary mất executable bị nuốt`; tổng mutant DAT, canary rỗng. Phục hồi → rc=0 | Bắt đúng lý do |
| Xoá verdict lượt 5 | t26 đỏ, t27 xanh | t26 rc=1, “trỏ vào tệp không có”; t27 rc=0 | Có; t27 không bắt |
| Xoá receipt lượt 5 | t27 đỏ | t26 rc=0; t27 rc=1, “KHÔNG có biên nhận” | Có; t26 không bắt |
| Xoá hàng mục lục lượt 5 | t27 đỏ | t26 rc=0; t27 rc=1, thiếu verdict trong cột mục lục | Có; t26 không bắt |
| Phục hồi hồ sơ | Cả hai chốt xanh | t26 và t27 cùng rc=0 trước và sau ba ca xoá | Không báo oan ở đối chứng |
| Đổi riêng số Ubuntu tại §1 từ 37 success/4 skipped thành 36/5, giữ tổng 41; chưa tái sinh manifest | Manifest bắt lệch byte | release-verify strict rc=2, ok=false, failed chỉ CHANGELOG; kích thước vẫn 887.490, hash đã khác | Bắt tính toàn vẹn |
| Giữ đột biến số ấy, chạy `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --deterministic --json` | Hai cổng đã nêu không bảo đảm nghĩa lời khai | Tái sinh rc=0; release-verify strict rc=0, ok=true, 180=180; doc-claims-check strict rc=0, ok=true | Đột biến SỐNG ở cả hai cổng |

Không biến ca văn xuôi sống sót thành finding hay yêu cầu xây cổng ngữ nghĩa. Phép thử chỉ chứng minh giới hạn của **hai cổng đã chạy trên mutant đó**. Lần dựng mutant đầu tiên tự dừng ở assert vì neo văn bản không duy nhất trên toàn CHANGELOG; đã thu hẹp neo vào §1 r362 và chạy lại thành công. Lỗi giàn thử đó không được tính thành cổng giết mutant.

## GIỚI HẠN

- Không mạng: mọi trạng thái GitHub của #490/#497, CI run `34391481045`, so sánh với các run sau, các Issue và chỉ thị/approval đều KHÔNG ĐO ĐƯỢC. `landed` của #490 là kết luận có một vế hậu-merge gate dựa vào thuật lại; phép đo này chỉ xác nhận hai vế có hiện vật và nhãn nguồn của vế còn lại.
- Raw ref kiểm được byte, tập tên/OID và sự hiện diện của object; không xác thực được nó đến từ GitHub, thời điểm chụp, trình tự fetch/dựng gói, hay số ref mù lịch sử phía điều phối. Không lấy mirror cục bộ làm lần hỏi máy chủ độc lập.
- Chỉ chạy Linux và tập lệnh ghi trên; không chạy toàn bộ CI, không đo Windows thực, không xác nhận CI của head review đã hoặc chưa chạy. Cấu hình phù hợp câu chuyện CI không chứng minh câu chuyện đã xảy ra.
- Runtime, prompt/model/session identity, hành vi đọc và danh tính người vận chuyển của các lượt trước vẫn là attestation. Hash/tree khớp chỉ xác minh hiện vật và OID. Không tái dựng hồ sơ lượt 6–10 đã đóng băng.
- Không tự soạn nội dung tấn công; dùng fixture/ca có sẵn và các đột biến số, điều kiện, xoá tệp/hàng trong bản sao. Hướng cần chuỗi thoát, đồng tự Unicode hoặc đường dẫn thoát cây không được dựng mới.
- Kết thúc: `git -C cay-kho status --porcelain` rc=0, stdout rỗng; HEAD/tree giữ nguyên. Bản sao và log tạm đã được dọn; tệp kết quả duy nhất của lượt này là `VERDICT.md`.
