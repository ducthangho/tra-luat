verdict: changes_requested
reviewed_sha: e27d839602e6691227181188886f07e2a446ff7d

## BẢNG ĐO

**Lượt 6: 0 P1 / 3 P2 / 0 P3.** Không phát hiện P1/P2 trong nội dung gốc §1, §2, khối chú thích mới của `ops/cong_cu.py` hoặc manifest. Hai P2 nằm trong hồ sơ review đã nhập kho; một P2 nằm trong lời khai chạy cổng của `EVIDENCE.md`. Không lấy kết quả cục bộ để tự chứng nhận trạng thái `landed` trên GitHub.

Reviewer: phiên Codex/OpenAI hiện tại, dùng công cụ thực thi cục bộ; không dùng danh tính tài khoản đăng GitHub làm danh tính reviewer. Cây được định danh bằng HEAD trên và tree `ac12c7b3f7f3b9c392d8d56bd471c87c77424efe`. Các lệnh có khả năng ghi và mọi đột biến chạy trên bản sao đầy đủ trong sandbox, với `TMPDIR` cũng nằm trong sandbox. Không cài công cụ, không gọi mạng.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Gói và cây được giao | Các trường trong `do-goi.txt`, chép vào `EVIDENCE.md` | Cả **10 trường** khớp cấu hình thật; khối nguyên văn trong EVIDENCE khớp do-goi; HEAD/tree đúng; không shallow; detached; `core.abbrev=7`; cây sạch | Có |
| Mirror | 324 = 323 nhánh + 1 ref giao hàng | `for-each-ref refs/heads` và `ls-remote --heads origin` cục bộ đều 324; loại **đích danh** `refs/heads/pr497-head` còn 323 | Có; đây là mirror, không phải GitHub |
| Số hiệu r362 | Chỉ nhánh PR này trong tập không có ref giao hàng | Đọc `CHANGELOG.md` của từng ref trong 323 ref, tìm tiêu đề r362: đúng một, `claude/handoff-tra-luat-repo-2ak5th` | Có với tập hiện có; không tái lập bộ đệm/máy chủ tại thời điểm cũ |
| Response máy chủ được giao | 322 dòng, SHA-256 bắt đầu `ec6ef20af4eb7f73` | 322 dòng; SHA-256 `ec6ef20af4eb7f734fcb0e321c86b93d0efbb34493630e968fcfb138b51b5ec8` | Byte/số học khớp; xuất xứ và giờ chụp là ATTESTATION |
| Phạm vi diff | `0721811..HEAD`: 14 tệp, +2968/−5, 15 commit | Đo bằng Git đúng cả bốn số; `diff.patch` và `numstat.txt` khớp output Git; `0721811` là tổ tiên HEAD | Có |
| §1 — vế merged | `8cee941`, hai cha `00e017a` + `01e7f77` | Hai cha đúng, đúng thứ tự; `8cee941` là tổ tiên của `origin/master` **cục bộ** tại `0721811` | Có về object/ancestry; trạng thái PR trên GitHub KHÔNG ĐO ĐƯỢC |
| §1 — hậu-merge gate | Run `34391481045`, push/master, head `8cee941`, attempt 1, hai job success | Không có response/log run này trong kho. Các lần xuất hiện ID chỉ ở CHANGELOG và verdict review. Nhãn **thuật lại** có trước bảng, cùng giới hạn nguồn ở đầu r362 | Nhãn nguồn phù hợp; kết quả CI KHÔNG ĐO ĐƯỢC |
| §1 — số bước và thời lượng CI | 41; Ubuntu 37+4+0; Windows 35+6+0; hai khoảng giờ trong bảng | Hai phép cộng đều 41. Hiệu giờ lần lượt **20m55s**, **53m32s**. Chỉ là số học trên đầu vào được kể | Không xác thực runtime |
| §1 — cấu hình hỗ trợ diễn biến CI | Các bước #7/#8/#9/#11/#22/#23/#38/#39 như mô tả | YAML ở `8cee941` và HEAD đều có **40 bước khai báo**; 8 setup + 1 upload + 31 bước còn lại. Các số bước kể trong PR phù hợp độ lệch +1 cho setup job; không coi đó là phép đếm 41 bước runtime | Cấu trúc khớp |
| §1 — skip trên master | Ubuntu 4, Windows 6; cùng hình dạng với hai run sau | Điều kiện YAML cho tập skip dự kiến Ubuntu **#11, #23, #28, #39**; Windows **#11, #21, #22, #28, #36, #39**, dùng cách đánh số của PR. Chuyện ba run thật có cùng kết quả vẫn là thuật lại | Khớp thiết kế; không xác minh ba run |
| §1 — bookkeeping | Mục r359 thay tệp land-evidence riêng theo quyết định chủ kho | Mục r359 thực sự ghi sổ #490, ba vế và nợ lúc đó (`CHANGELOG.md:756`, `:845–856`). Việc chủ kho cho phép thay thế hồ sơ là lời thuật lại trong kho | Đo được nội dung ghi sổ; không xác thực quyết định ngoài kho |
| §1 — kết luận landed | Cả ba vế ADR-0034 đạt | `docs/adr/0034-…md` đòi canonical + hậu-merge gate + bookkeeping. Bằng chứng cục bộ xác nhận lịch sử Git và mục ghi sổ; vế CI dựa trên attestation đã gắn nhãn | Không có phản chứng cục bộ; **không cấp chứng nhận landed độc lập** |
| §2 — có shellcheck, quét đầy đủ | Canary DAT, blocking | `rc=0`, tổng DAT, shellcheck DAT, canary DAT, chính sách blocking; bắt SC1003, actionlint trả rc=1 với fixture | Có |
| §2 — thiếu riêng shellcheck, quét đầy đủ | Canary DO, blocking, tổng không đạt | `rc=2`, tổng DO; shellcheck KHONG_DO_DUOC; canary DO với lý do SUY_GIAM, fixture trả rc=0; mọi công cụ bắt buộc khác vẫn DAT | Có; bác được câu r361 bị rút |
| §2 — `--chi` | Không chạy canary; bước shellcheck có thể xanh dù công cụ thiếu | Cả `--chi shellcheck` và `--chi actionlint`, với/không shellcheck, đều `rc=0`, tổng DAT, `canary=[]`. Khi thiếu shellcheck, bản ghi riêng của nó vẫn KHONG_DO_DUOC | Có |
| §2 — diễn biến Windows đỏ, các Issue 128/101/bốn Issue/#498 | Thuật lại; phân biệt cấu hình cho phép với sự kiện đã xảy ra | Đọc thấy nhãn nguồn và giới hạn. `cai_cong_cu.sh` gọi `--chi`; bước G5 quét đầy đủ; `rg` bắt buộc và bước cài đứng trước G5 | Cơ chế khớp; sự kiện GitHub KHÔNG ĐO ĐƯỢC |
| Chú thích mới `tong_hop` | Mô tả nợ mức bước; runtime không đổi | `git diff 0721811 HEAD -- ops/cong_cu.py`: +23/−0 dòng chú thích; `ast.dump(ast.parse(...))` hai bản **bằng nhau**, không tính thuộc tính vị trí | Có |
| Nhãn nguồn trong chú thích | Cơ chế đo được; run CI/#498 là thuật lại | Nhãn có ở `ops/cong_cu.py:209–229`; logic `chi is None`, optional shellcheck và nâng trạng thái canary phù hợp A/B | Có |
| Manifest | 180 mục; chỉ CHANGELOG đổi mục kiểm kê | Tự đọc đủ **180/180** tệp, 180 đường dẫn duy nhất; **0 lệch kích thước/SHA-256**, tổng **8 162 216 byte**; tập đường dẫn bằng bản `0721811`; chỉ mục `CHANGELOG.md` khác | Có |
| Hash tổng manifest | package_hash = content_hash | Tính độc lập từ các bản ghi thực: `65c33fc8c6d902c58a10704bab4dcbe5dae239345fc4e296e97748eef23b3b8f`, bằng cả hai trường | Có |
| Byte/hash CHANGELOG | 867894 byte, SHA-256 `a785c22e…` | **867894**, `a785c22e56f1ecd81dd1b42876b3c6625999e4629a9f12345d451df40c99b4d5`; tăng **51998 byte** so với bản nền | Có |
| Điều kiện công cụ | actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0; chỉ hai bản được ghim | Đúng ba bản ấy. YAML/CI ghim actionlint và jsonschema; shellcheck `ban_ghim: null`, câu gọi installer không truyền phiên bản | Có |
| Hồ sơ năm lượt | Verdict, receipt và mục lục khớp | Byte/dòng verdict: **28955/161; 43791/259; 48843/285; 51844/296; 42310/271**. Cả năm hash, số tiêu đề P1/P2/P3 và neo blob khớp; mỗi neo là commit thêm tệp duy nhất và là tổ tiên HEAD; 5 hàng mục lục, 2 hàng cảnh báo | Có; không chứng thực runtime reviewer |
| `lease_publish_test.py` | 146/146, chạy 146, bỏ qua 0 | **rc=0; 146/146; chạy 146; bỏ qua 0** | Có |
| `bien_nhan_v2.py --root .` | 53 v2, 11 legacy, 42 nợ, tổng 106; không vi phạm | **rc=0; 53 + 11 + 42 = 106; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC** | Có |
| Chuỗi bộ đếm biên nhận | 49/102 → 50/103 → 51/104 → 52/105 → 53/106 | Checkout trên bản sao và chạy validator tại **4d2a6f6, 4e6a2d5, 25974e7, f6ec9c0, e27d839**: đúng từng cặp, cả năm rc=0 | Có |
| `bien_nhan_v2_test.py` | 48/48 ca, 63/63 đột biến, 2/2 tự kiểm | **rc=0**, đúng cả ba số; output còn nêu **45/63** đột biến thường khai đối chứng | Có |
| `cong_cu_test.py` | ca=23, đột biến=18, lỗi đột biến=0 | **rc=0**, đúng ba số | Có |
| `release-verify RELEASE_MANIFEST.json --strict --json` | ok=true, expected=checked=180 | **rc=0**, ok=true, 180/180, `failed=[]` | Có |
| `golden-test --strict` trong EVIDENCE | ok=true; gọi chung ba lệnh là “đều --strict” | **rc=2**, lỗi `unrecognized arguments: --strict`. Lệnh hợp lệ `golden-test --json`: **rc=0, ok=true, 20/20 ca** | **Không — finding 1** |
| `determinism-audit --strict --json` | ok=true | **rc=0; ok=true; 15/15 checks đạt** | Có |
| `doc-claims-check --strict --json` | ok=true | **rc=0; ok=true**; quét 106 tệp, có **367 advisory** | Có; không đồng nghĩa mọi câu văn đúng |
| `workflow-audit --strict --json` | rc=0 | **rc=0; ok=true** | Có |
| `packet_loop.py doctrine-scan --root .` | rc=0 | **rc=0**, quét 7 tệp, 0 chỗ chép doctrine | Có |
| `packet_loop.py adr-song --root .` | rc=0 | **rc=0**, 46 ADR/46 dòng, có ngoại lệ thiếu trạng thái 0016 được khai rõ | Có |
| Biên nhận ngắn và bản vá lượt 5 | §4: 253/146, giảm 107, một dòng/finding, cả lớp rủi ro đã hết; BN4: 260/149, giảm 111, khối finding 45 dòng | HEAD: **BN3 273 dòng; BN4 165 dòng; chênh 108**; 5 mục finding chiếm khối **52 dòng**. Lời khẳng định hết rủi ro vẫn ở §4 | **Không — finding 2** |
| Bảng phân loại đã bị xoá | §4 và BN5 nói bỏ bảng sai | BN4 và hàng mục lục lượt 4 vẫn khai **0/2 · 5/7 · 4/6 · 5/5**. Đếm lại theo các dẫn chiếu đầy đủ và dẫn tắt: **0/2 · 7/7 · 6/6 · 5/5** | **Không — finding 3** |

**Lệnh và cách đo chính.** Các lệnh cổng trong bảng chạy bằng `python3`; ba lệnh `release-verify`, `golden-test`, các audit đi qua `scripts/tl.py`; hai lệnh doctrine/ADR đi qua `.claude/dev/packet_loop.py`. Bản chạy hợp lệ gồm 12 lệnh logic của EVIDENCE; lần gọi thêm `golden-test --strict --json` được giữ là kết quả lỗi, không tính thành pass.

Quan hệ cha đo bằng `git -C cay-kho show -s --format='%H %P' 8cee941`, trả:

```
8cee9410e958a6b9d956e080c11878fbd80d9f5f
cha 1: 00e017af102bc8355e0c276d2d813e20620ddb42
cha 2: 01e7f77d707cb093b5ba6d9b9d8577f40d025488
```

`git -C cay-kho merge-base --is-ancestor 8cee941 origin/master` trả **0**. `origin/master` được đọc ở đây là `072181157a27804e69deb35bb792a88c70ac31e3` trong clone được giao.

A/B dùng hai thư mục PATH riêng trong sandbox, cùng liên kết tới các executable có sẵn `python`, `python3`, `git`, `bash`, `rg`, `actionlint`; chỉ thư mục A có thêm `shellcheck`. Không dùng executable giả cho shellcheck trong phép A/B này. Từ cùng bản sao, chạy Python bằng đường dẫn executable tuyệt đối với môi trường PATH tương ứng:

```
python3 ops/cong_cu.py kiem-tra --json
python3 ops/cong_cu.py kiem-tra --json --chi shellcheck
python3 ops/cong_cu.py kiem-tra --json --chi actionlint
```

Cả sáu lần hoàn tất. Ngoài sự có mặt của shellcheck, các bản ghi công cụ trong hai phép quét đầy đủ giữ nguyên. Nền thực tế: Python **3.11.15**, PyYAML **6.0.1**, Git **2.43.0**, Bash **5.2.21**, rg **15.2.0**, cùng ba phiên bản đã nêu trong EVIDENCE; không giả đây là môi trường Windows/CI Python 3.12.

Phép kiểm manifest độc lập dùng `Path.read_bytes()` cho từng mục, so `len(data)` và `hashlib.sha256(data).hexdigest()` với hai trường tương ứng. Hash tổng tính từ các bản ghi **thực đo**, theo thứ tự manifest: nối path, size, sha256 bằng ký tự mã 0, rồi nối các bản ghi bằng ký tự xuống dòng và băm SHA-256. Không lấy `ok` của công cụ phát hành thay cho phép đọc từng tệp. Tập đường dẫn và từng bản ghi còn được so với `git show 0721811:RELEASE_MANIFEST.json`.

**Đột biến — báo cả chiều bị bắt và chiều sống sót.** Mỗi ca dưới đây bắt đầu từ bản sao nguyên vẹn; thay đúng phần nêu trong bảng rồi phục hồi. Các fixture và test có sẵn được dùng nguyên bản; không tự soạn nội dung tấn công.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Tắt vòng chạy canary trong `tong_hop` | Test canary có răng | Đổi điều kiện vòng canary thành luôn sai: quét đầy đủ khi thiếu shellcheck chuyển **rc=2 → 0**, canary rỗng. Gọi `t13_actionlint_bien_mat_giua_probe_va_canary`: **0 → 1 → 0** trước/đột biến/phục hồi | Cổng test bắt được mất canary |
| Bỏ fixture canary | Blocking khi không đo được | `kiem-tra --json`: **rc=3**, tổng và canary KHONG_DO_DUOC. Phục hồi: **rc=0**, DAT | Có răng; không báo oan sau phục hồi |
| Tăng riêng size CHANGELOG trong manifest một byte | Kiểm toàn vẹn phát hiện lệch | `release-verify … --strict --json`: **rc=2, ok=false**, chỉ đúng expected 867895/actual 867894; phục hồi **rc=0** | Có răng |
| Đổi bảng CI Ubuntu 37/4 thành 36/5, vẫn tổng 41 | Phân biệt hash với nghĩa câu | Giữ manifest cũ: release-verify **rc=2**, hash lệch dù kích thước bằng nhau. Tái sinh manifest: doc-claims và release-verify đều **rc=0, ok=true** | Bắt byte lệch; không bắt nghĩa ở hai cổng đã thử |
| Đổi cha thứ nhất trong §1 thành `0721811`, một commit thật | Cổng không được mặc nhiên coi là kiểm quan hệ cha | Sau tái sinh manifest, doc-claims và release-verify đều **rc=0, ok=true** | Đột biến sống ở hai cổng |
| Đổi riêng chữ blocking thành advisory trong lời văn §2 | Văn xuôi không phải cấu hình runtime | Sau tái sinh manifest, hai cổng trên đều **rc=0, ok=true** | Đột biến sống ở hai cổng |
| Đảo lời chú thích thành có `chi` thì mọi canary chạy | AST/runtime vẫn giữ nguyên | Hai cổng trên đều **rc=0, ok=true** | Đột biến sống ở hai cổng |
| Bỏ verdict lượt 5 | t26 cộng t27 bảo vệ hồ sơ | **t26 rc=1; t27 rc=0** | Đúng giới hạn từng ca |
| Bỏ receipt lượt 5 | t27 đòi receipt | **t26 rc=0; t27 rc=1** | Đúng giới hạn từng ca |
| Bỏ riêng hàng mục lục lượt 5 | t27 đòi hàng mục lục | **t27 rc=1**; phục hồi toàn bộ: **t26=t27=0** | Có răng |

Các ca trực tiếp gọi qua `python3 -c`, thêm `ops` vào `sys.path`, import module test rồi gọi đúng hàm: `cong_cu_test.t13_actionlint_bien_mat_giua_probe_va_canary`, `lease_publish_test.t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi`, `lease_publish_test.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc`. Tái sinh chỉ ở bản sao bằng `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json`.

**Bốn đột biến văn xuôi sống sót không tạo finding về thiếu cổng ngữ nghĩa.** Kết luận chỉ áp dụng cho `doc-claims-check` và `release-verify` ở những ca đã chạy; không suy ra mọi cổng trong kho đều không bắt được.

### evidence-gan-co-strict-cho-golden-test  [P2]  EVIDENCE khai thành công với một cờ mà golden-test không nhận

TỆP/DÒNG: `EVIDENCE.md:41`; đối chiếu dòng 29 về phép đo sau bước cuối và `cay-kho/.github/workflows/ci.yml` ở bước `golden-test`.

VẤN ĐỀ: Cụm “đều `--strict`” áp cho cả `golden-test`, nhưng lệnh đó không hỗ trợ cờ này. Vì vậy không tái lập được lời khai `ok=true` theo chính bảng lệnh. Đây là sai thông tin về phép chạy trong gói bằng chứng, không phải hồi quy của golden-test. User yêu cầu mọi lệch EVIDENCE/phép đo thành finding; mức P2 phù hợp lời khai kết quả sai.

ĐÃ THỬ VÁ: có — trên bản sao EVIDENCE trong sandbox, chỉ gắn `--strict` cho `determinism-audit` và `doc-claims-check`, giữ `golden-test` không cờ này. Không sửa bản EVIDENCE được giao.

ĐÃ THỬ NGHIỆM: từ bản sao HEAD, `python3 scripts/tl.py golden-test --strict --json` ⇒ **rc=2**, `unrecognized arguments: --strict`, stdout rỗng; `golden-test --help` không có cờ strict; `python3 scripts/tl.py golden-test --json` ⇒ **rc=0, ok=true, 20/20 ca**. Hai lệnh audit còn lại với strict đều rc=0.

ĐỘ TIN: cao

### bien-nhan-ngan-van-khai-sai-so-va-pham-vi  [P2]  Lời khai đã sửa số dòng và bỏ kết luận hết rủi ro vẫn không đúng trên HEAD giao cuối

TỆP/DÒNG: `cay-kho/CHANGELOG.md:559–567`; `cay-kho/ops/reviews/pr497-review-4-codex-verdict.receipt.yaml:14–21`; `cay-kho/ops/reviews/README.md:274`; đối chiếu `cay-kho/ops/reviews/pr497-review-5-codex-verdict.receipt.yaml:84–87`.

VẤN ĐỀ: §4 vẫn khai biên nhận chỉ còn trường đo được và “đúng một dòng mỗi finding”, số dòng 253/146, giảm 107, rồi khẳng định “Cả lớp rủi ro chết theo KIẾN TRÚC”. Hàng mục lục lượt 4 cũng còn “một dòng mỗi finding”. Trong khi đó, chú thích BN4 nói rõ vẫn có văn xuôi, finding là mục nhiều dòng và không được kết luận hết rủi ro. BN5 lại khai đã sửa ba số và bỏ chính kết luận ấy. Đây là mâu thuẫn giữa sản phẩm cuối và lời khai bản vá, không chỉ là trích lịch sử bất biến.

Ngay số mới ở chú thích BN4 cũng trôi: “tệp này 149 dòng”, BN3 260, chênh 111 và khối finding 45 dòng đều không có neo snapshot tại chỗ. Trên HEAD giao cuối, hai tệp là **165 và 273**, chênh **108**; `nam_finding` có năm object, khối từ khóa `nam_finding:` đến trước khóa cấp gốc kế tiếp là **52 dòng** (61–112, tính cả dòng trống). Chú thích vẫn đang mô tả hiện trạng bằng số của phiên bản trước. Không yêu cầu sửa các verdict lịch sử hoặc thông điệp commit bất biến.

ĐÃ THỬ VÁ: có — trên bản sao, thay đoạn kết §4 và phần tương ứng ở mục lục bằng mô tả hẹp: rút gọn văn xuôi, mỗi finding nhiều dòng, các trường tự thuật giữ nhãn ATTESTATION; không kết luận đã loại cả lớp rủi ro. Ghim cặp số 260/149/111 vào **3c82ae3** và bỏ số dòng biến động của khối finding trong chú thích BN4. Tái sinh manifest trên bản sao.

ĐÃ THỬ NGHIỆM: `wc -l cay-kho/ops/reviews/pr497-review-{3,4}-codex-verdict.receipt.yaml` ⇒ **273, 165**; parse YAML ⇒ **5 object** dưới `nam_finding`. Đọc từng blob bằng `git show <sha>:<path>` và đếm dòng cho kết quả:

| snapshot | BN3 | BN4 | chênh |
|---|---:|---:|---:|
| `f6ec9c0` | 253 | 149 | 104 |
| `3c82ae3` | 260 | 149 | 111 |
| `e27d839` | 273 | 165 | 108 |

Khối finding là 45 dòng tại hai snapshot trước, 52 tại HEAD. Bản thử vá: `doc-claims-check --strict --json` và `release-verify RELEASE_MANIFEST.json --strict --json` đều **rc=0, ok=true**; `bien_nhan_v2.py --root .` **rc=0, 53/106**, t26+t27 **rc=0**. Quét lại các đoạn được thay xác nhận không còn hai lời khai “đúng một dòng”/“cả lớp rủi ro chết” ở đó. Cổng xanh là kiểm tương thích cấu trúc; việc bỏ lời khai sai được kiểm trực tiếp bằng nội dung diff.

ĐỘ TIN: cao

### bang-phan-loai-da-xoa-van-con-o-hai-noi  [P2]  Hai bản sao vẫn dùng bảng 5/7 và 4/6 mà §4 đã bác và khai xoá

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-4-codex-verdict.receipt.yaml:6–10`; `cay-kho/ops/reviews/README.md:274`; đối chiếu `cay-kho/CHANGELOG.md:532–548` và `cay-kho/ops/reviews/pr497-review-5-codex-verdict.receipt.yaml:58–66`.

VẤN ĐỀ: Chú thích BN4 công bố quy tắc hỏi tập TỆP/DÒNG có chứa hiện vật sinh vì review, rồi vẫn cho **0/2 · 5/7 · 4/6 · 5/5**. Hàng mục lục lượt 4 lặp lại cùng bảng làm bằng chứng cho bản vá cấu trúc. §4 đã gọi chính bảng đó là sai và BN5 khai **XOÁ BẢNG**. Hai nơi còn sống không được ghi là số cũ đã rút, nên người đọc receipt/mục lục vẫn nhận kết luận đã bị bác ngay trong cùng PR.

ĐÃ THỬ VÁ: có — trên bản sao, bỏ bảng số ở đúng hai nơi còn sót; thay bằng nhận xét giới hạn ở các verdict lượt 2–4, không suy nội dung gốc sạch. Không tạo bảng mới hoặc cổng ngữ nghĩa mới.

ĐÃ THỬ NGHIỆM: đọc bốn verdict gốc, tách khối theo tiêu đề finding có `[P1]`, `[P2]`, `[P3]`; chỉ xét trường `TỆP/DÒNG`, nhận cả đường dẫn đầy đủ và dẫn tắt `receipt lượt N`/`verdict lượt N`. Kết quả **0/2, 7/7, 6/6, 5/5**, khớp đính chính §4, không khớp hai nơi nêu trên. Ví dụ bị bỏ sót ở lượt 2: `hai-cong-duoc-khai-thanh-moi-cong-trong-kho` dẫn “verdict lượt 1 dòng 100–113”; nó vẫn là dẫn chiếu hiện vật review. Sau bản thử vá kết hợp finding 2, các cổng doc-claims, release-verify, validator receipt và t26+t27 đều đạt như đã ghi; kiểm nội dung xác nhận bảng cũ đã mất ở hai đích. Đây là thử vá trên bản sao, không phải lời khai PR đã được sửa.

ĐỘ TIN: cao

## GIỚI HẠN

- Không mạng, không xác thực trạng thái PR/Issue, approval, actor, authority, số ref máy chủ tại thời điểm cũ hoặc các run GitHub. `ls-remote origin` chỉ đọc mirror trong sandbox. `ls-remote-may-chu.txt` chứng minh được byte của tệp được giao, không chứng minh nguồn gốc GitHub hay timestamp của lần chụp.
- Không có log Actions/run response để xác minh run `34391481045`, hai run so sánh, hay “lượt Windows đỏ”. Việc head này chưa chạy CI là attestation của điều phối. Chạy Linux cục bộ và đọc YAML không thay thế chạy Windows hoặc toàn bộ CI.
- Runtime, model đã phục vụ, prompt/stdout/stderr của năm phiên cũ, hành vi đọc cây, tuân thủ của reviewer và danh tính người đăng GitHub không được xác thực chỉ bằng receipt. Hash, byte, số tiêu đề và ancestry khớp không nâng những trường ấy thành phép đo sự kiện.
- Đã chạy 12 lệnh logic được liệt kê, sáu phép A/B, năm snapshot validator và các đột biến nêu cụ thể. Không chạy mọi cổng trong kho; không thực hiện LIVE/publish/merge/deploy. Đột biến bị bắt/sống chỉ có phạm vi như bảng; không đề nghị xây cổng hiểu nghĩa văn xuôi.
- Không tự soạn chuỗi tấn công, đồng tự Unicode hoặc đường dẫn thoát khỏi cây. Những hướng cần các đầu vào đó không được thử. Chỉ dùng suite/fixture sẵn có và thay số, chữ mô tả, điều kiện canary hoặc sự hiện diện của hiện vật trong bản sao.
- Các bản sao, script/log và bản vá thử đã được dọn. Chỉ giữ tệp kết quả **VERDICT.md** ở gốc sandbox. Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**; HEAD và tree vẫn đúng hai OID nêu trên.
