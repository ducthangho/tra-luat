verdict: changes_requested
reviewed_sha: df09f3eebf88a148f6bedfe5e5f5bf3ea8433519

## BẢNG ĐO

Kết quả: **0 P1 / 1 P2 / 0 P3**. Nội dung gốc §1/§2, chú thích mã và manifest không lộ sai lệch trong các phép đo dưới đây. Finding còn lại là một số dòng sai ở §3.

Reviewer: Codex/OpenAI, thực thi qua công cụ cục bộ trong sandbox; không có phép xác thực độc lập danh tính backend. Tree đã đối chiếu: `b00a40559cfdc14da6ce53a9538634842d120fac`. Các cổng chạy trên bản chép đầy đủ, cùng HEAD/config với `cay-kho/`; đột biến chạy trên bản chép riêng. `PYTHONDONTWRITEBYTECODE=1`; thư mục tạm của các tiến trình được đặt trong sandbox.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Gói giao, HEAD và tree | `do-goi.txt` và khối cấu hình `EVIDENCE.md` | Hai khối khớp nguyên văn; HEAD/tree đúng các OID trên; detached; không shallow; `core.abbrev=7`; origin trỏ đúng `kho.git` trong sandbox; worktree sạch | Có |
| Số head mirror | 324 = 323 + 1 ref giao hàng | `git --git-dir=kho.git for-each-ref refs/heads`: 324; đúng một `pr497-head`; `git -C cay-kho ls-remote --heads origin`: 324, chỉ đọc mirror | Có |
| Quét số r | Loại ref giao hàng và nói rõ đã loại | Đã loại `pr497-head`; đọc tiêu đề r đầu tiên trong `CHANGELOG.md` của 323 nhánh, không lỗi đọc; r362 ở `claude/handoff-tra-luat-repo-2ak5th`, r363 ở `claude/land-492-bookkeeping` | Có, đối với tập cục bộ này |
| Snapshot máy chủ | 322 dòng, SHA-256 bắt đầu `ec6ef20af4eb7f73` | 322 dòng, 322 tên duy nhất; SHA-256 `ec6ef20af4eb7f734fcb0e321c86b93d0efbb34493630e968fcfb138b51b5ec8`; so tập với mirror: mirror thêm `pr487-merge` và `pr497-head`, không thiếu tên, các OID chung khớp | Byte/số học khớp; xuất xứ GitHub KHÔNG ĐO ĐƯỢC |
| Phạm vi diff | `0721811..HEAD`: 14 tệp, +2991/−5, 16 commit | Tự chạy `git diff --numstat` và `git rev-list --count`; đúng các số trên; `diff.patch` và `numstat.txt` khớp nguyên byte với Git | Có |
| §1 — vế merged | `8cee941`, cha `00e017a` + `01e7f77` | Cha đúng thứ tự: `00e017af102bc8355e0c276d2d813e20620ddb42` và `01e7f77d707cb093b5ba6d9b9d8577f40d025488`. Hai phép kiểm cha là tổ tiên của `8cee941`, cùng phép `8cee941` là tổ tiên HEAD, đều rc=0 | Có về object/quan hệ Git; trạng thái PR trên GitHub KHÔNG ĐO ĐƯỢC |
| §1 — hậu-merge gate | Run `34391481045`, push/master, head `8cee941`, attempt 1; hai job success | Không có response Actions/log job của run này để kiểm. §1:42 đặt nhãn “thuật lại” trước bảng; giới hạn nguồn ở dòng 7–14 bao phủ số CI | Nhãn đúng; sự kiện KHÔNG ĐO ĐƯỢC |
| §1 — bảng CI | 41 bước; Ubuntu 37+4+0, Windows 35+6+0 | Hai tổng đều bằng 41. YAML có 40 bước khai báo; cộng bước khởi tạo job thành 41 theo cách đánh số được thuật lại. Phân loại YAML: 8 setup + 31 cổng + 1 upload. `ci.yml` không đổi từ `8cee941` tới HEAD | Số học/cấu hình khớp; kết quả thực chạy và thời gian KHÔNG ĐO ĐƯỢC |
| §1 — các bước skip | Cấu trúc lane LAND cho phép các bước được kể | Đọc điều kiện YAML: trên push/master, #11/#28/#39 không thuộc lane này; Ubuntu thêm #23; Windows thêm #21/#22/#36. Tương ứng 4 và 6. Chưa xác thực một lần chạy nào | Cấu hình phù hợp lời kể; không thay bằng chứng runtime |
| §1 — bookkeeping và landed | Mục r359 là ghi sổ thay hiện vật land riêng; ba vế đạt | r359 thực sự có khối ghi sổ và nêu lựa chọn đó tại `CHANGELOG.md:866`. ADR-0034 đòi vào canonical + hậu-merge gate + bookkeeping. Sự tồn tại/nội dung ghi sổ đo được; quyết định chủ kho và hậu-merge CI vẫn là thuật lại | Không tự chứng nhận `landed` từ sandbox; không thấy mâu thuẫn với nhãn nguồn đã khai |
| §2 — A/B có shellcheck | Tool/canary DAT | `python3 ops/cong_cu.py kiem-tra --json`: rc=0, tổng DAT, 8/8 tool DAT; canary blocking DAT, bắt SC1003, rc bên trong=1 | Có |
| §2 — A/B thiếu riêng shellcheck | Shellcheck KHONG_DO_DUOC, actionlint DAT, canary DO | Cùng cây và cùng thư mục PATH, chỉ bỏ liên kết `shellcheck`: rc=2, tổng DO; shellcheck KHONG_DO_DUOC; actionlint DAT; canary blocking DO, báo suy giảm lớp SC*, rc bên trong=0 | Có; lời rút của r361 có phản chứng thực chạy |
| §2 — `--chi` | Tắt canary; bước công cụ tùy chọn có thể xanh khi thiếu | Khi thiếu shellcheck, `kiem-tra --chi shellcheck --json`: rc=0, tổng DAT, tool KHONG_DO_DUOC, canary rỗng. `--chi actionlint`: rc=0, DAT, canary rỗng. Khi có shellcheck, `--chi shellcheck` cũng không chạy canary | Có |
| §2 — lời kể Windows đỏ | Chỉ cơ chế đo được; diễn biến CI thuật lại | `cai_cong_cu.sh:75` truyền `--chi`; bước #7/#8 gọi từng công cụ; #9 gọi quét đầy đủ và bộ test. Nhãn giới hạn có ở §2 và ngay đầu khối chú thích mới | Có về cơ chế/nhãn; Windows runtime KHÔNG ĐO ĐƯỢC |
| Chú thích `tong_hop` | Không đổi runtime; canary blocking kéo tổng lên | Diff `ops/cong_cu.py`: +23/−0, chỉ chú thích. `ast.dump(ast.parse(...))` của `0721811` và HEAD bằng nhau, không tính thuộc tính vị trí. Đọc vòng tổng hợp và A/B xác nhận mô tả | Có |
| Điều kiện công cụ | actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0; chỉ hai bản được CI ghim | Probe đúng ba bản; Python 3.11.15, PyYAML 6.0.1. YAML/CI ghim actionlint và jsonschema; shellcheck `ban_ghim: null`, lời gọi cài không ghi bản | Có |
| Manifest từng tệp | 180 mục; chỉ CHANGELOG đổi | Đọc byte riêng của đủ 180 đường dẫn: 180 tên duy nhất, 0 lệch size/SHA-256, tổng 8.162.753 byte. So manifest nền: 0 thêm, 0 bỏ, chỉ entry `CHANGELOG.md` đổi | Có |
| Manifest hash tổng | `package_hash = content_hash` | Tự tính lại từ các entry theo thứ tự đường dẫn: `9f6daaa51542a6c83762af76b4d9a18b20b85bb0db4e0f877e6d9582ed55f360`, khớp cả hai trường | Có |
| Hồ sơ lượt 1–5 | 5 verdict, 5 biên nhận, 5 hàng mục lục, 2 cảnh báo | Đếm đúng; hash/byte của 5 verdict khớp biên nhận và §3; blob ở 5 neo ghim nguyên byte; mỗi neo là đúng commit duy nhất thêm verdict. Đếm tiêu đề ra P1/P2/P3 lần lượt 0/1/1, 0/7/0, 0/6/0, 0/5/0, 0/8/0 | Có |
| Đóng băng từ lượt 6 | Hồ sơ lượt 6/7 không vào cây | Không có tệp `pr497-review-6-*` hay `pr497-review-7-*` | Có |
| Vá lượt 6 (a) | Bỏ cách gộp `golden-test` vào “đều --strict” | Bảng EVIDENCE ghi đúng từng lệnh. Chạy có `--strict`: rc=2, unrecognized arguments; không cờ: rc=0, 20/20 | Có |
| Vá lượt 6 (b) | Bỏ bảng phân loại sai còn sót ở chú thích BN4 và hàng mục lục | Hai chỗ nay thay bằng mệnh đề định tính; dãy số cũ còn được trích nhưng có nhãn bản cũ/sai, không còn là lời khai hiện hành | Có |
| Vá lượt 6 (c) | Bỏ phép so số dòng và câu “cả lớp rủi ro chết theo kiến trúc” | Các chỗ được sửa đã rút lời khẳng định; số cũ được dẫn như lịch sử có SHA. Tuy nhiên một số dòng khác vẫn còn sai ở §3:180 | Bản vá các chỗ nêu trên có hiệu lực; xem P2 dưới |
| §3 — độ dài biên nhận lượt 5 | 143 dòng | HEAD có 149 dòng; 143 là độ dài ở commit trước `e27d839` | **Không** |

**Chạy lại nguyên văn 12 cổng trong EVIDENCE.** Tất cả rc=0; không có lệch mới giữa EVIDENCE, `do-goi.txt` và các số đã đo.

| lệnh, chạy từ bản chép | bằng chứng dương |
|---|---|
| `python3 ops/lease_publish_test.py` | 146/146; đã chạy 146, bỏ qua 0 |
| `python3 ops/bien_nhan_v2.py --root .` | 53 v2 + 11 legacy + 42 nợ = 106; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC |
| `python3 ops/bien_nhan_v2_test.py` | 48/48 ca, 63/63 đột biến có răng, 2/2 tự kiểm |
| `python3 ops/cong_cu.py kiem-tra --json` | Tổng DAT, 8/8 tool DAT, canary DAT |
| `python3 ops/cong_cu_test.py` | 23/23, bỏ qua 0; 18 đột biến, 0 lỗi đột biến |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | ok=true; expected=checked=180; không thiếu/thừa/lệch |
| `python3 scripts/tl.py golden-test --json` | ok=true; 20/20 |
| `python3 scripts/tl.py determinism-audit --strict --json` | ok=true; 15/15; full=false |
| `python3 scripts/tl.py doc-claims-check --strict --json` | ok=true; 106 tệp; 0 flags, 367 advisory |
| `python3 scripts/tl.py workflow-audit --strict --json` | ok=true; 26 cards, 60 tasks; 0 lỗi/cảnh báo |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 7 tệp; 0 chỗ chép doctrine |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 46 ADR / 46 dòng; ADR 0016 được miễn kiểm trạng thái |

**Đột biến, cả hai chiều.** Mỗi ca dưới đây bắt đầu từ bản chép nguyên vẹn và được phục hồi trước ca tiếp theo. Chỉ thay số/văn xuôi thông thường, bỏ hiện vật hoặc đổi nhánh điều kiện; không tự soạn nội dung tấn công. Đối chứng ban đầu và sau phục hồi: `t26`, `t27`, `t13` đều rc=0.

Gọi ca riêng bằng `python3 -c 'import sys; sys.path.insert(0,"ops"); import lease_publish_test as m; getattr(m,next(n for n in dir(m) if n.startswith("t26_")))()'`; thay tiền tố bằng `t27_` cho t27, hoặc module `cong_cu_test` và tiền tố `t13_` cho t13. Các phép CLI dùng lệnh nguyên văn trong bảng cổng ở trên.

| thay đổi trên bản chép | kết quả đã chạy |
|---|---|
| Bỏ verdict lượt 1 | t26 rc=1, đúng lỗi “trỏ vào tệp không có”; **t27 vẫn rc=0** |
| Bỏ biên nhận lượt 1 | **t26 vẫn rc=0**; t27 rc=1 vì thiếu biên nhận |
| Bỏ hàng mục lục lượt 1 | t27 rc=1 vì thiếu ở đúng cột bảng |
| Bỏ hàng cảnh báo lượt 1, còn lời nhắc ở hàng khác | t27 rc=1 vì thiếu cảnh báo ở đúng hàng/cột |
| Thêm một câu thường vào verdict lượt 1, giữ biên nhận | t26 rc=1, LỆCH BĂM |
| Đổi `if chi is None` thành `if False` | t13 rc=1 tại chốt phát hiện canary bị nuốt; chính CLI quét đủ khi thiếu shellcheck lại **rc=0/DAT, canary rỗng** trên bản đột biến |
| Bỏ fixture canary có sẵn | `cong_cu.py kiem-tra --json`: rc=3, tổng/canary KHONG_DO_DUOC; không được tính là pass |
| Bảng CI 37 success/4 skipped thành 36/5, vẫn tổng 41 | doc-claims rc=0; release-verify rc=2 do băm CHANGELOG lệch; tái sinh manifest rồi release-verify **rc=0** |
| Đổi cha thứ nhất trong lời khai merge thành `0721811`, một commit có thật nhưng không phải cha | doc-claims rc=0; release-verify rc=2 do băm; tái sinh manifest rồi release-verify **rc=0** |

Hai đột biến văn xuôi đều sống qua **hai cổng được thử** sau khi tái sinh manifest bằng `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json`. Điều này đo giới hạn của hai cổng ấy; không suy thành giới hạn của mọi cổng và không yêu cầu xây cổng ngữ nghĩa mới. Chốt hồ sơ đúng là **t26 cộng t27**.

### so-dong-bien-nhan-luot-nam-con-neo-ban-cu  [P2]  §3 vẫn ghi 143 dòng cho biên nhận lượt 5 đã có 149 dòng

TỆP/DÒNG: `cay-kho/CHANGELOG.md:180`; đối chiếu `cay-kho/ops/reviews/pr497-review-5-codex-verdict.receipt.yaml:149`.

VẤN ĐỀ: Hàng kiểm kê ghi “biên nhận lượt 5, neo blob ghim `3c82ae3` — NGẮN, **143** dòng”. Tại reviewed_sha, tệp có **149** dòng. Số 143 đúng ở `e27d839`, trước khi commit cuối thêm sáu dòng. Neo `3c82ae3` là neo blob của **verdict**; tại commit đó biên nhận lượt 5 còn chưa tồn tại, nên neo này không biến 143 thành một phép đo hợp lệ của biên nhận hiện tại. Đây là lời khai số lượng sai còn sót, cùng hình dạng mà lượt 6 vừa yêu cầu bỏ; không phải lỗi runtime hay hash manifest.

ĐÃ THỬ VÁ: **có** — trên bản chép, bỏ riêng cụm số dòng (thay ` — NGẮN, **143** dòng |` bằng ` — NGẮN |`), giữ đường dẫn và neo verdict; tái sinh manifest. Diff bản thử chỉ gồm một dòng CHANGELOG và manifest. Không sửa `cay-kho/`. Rủi ro cần giữ khi áp: CHANGELOG nằm trong gói nên phải tái sinh manifest; không cần sửa biên nhận hay băm verdict. Kiểm khóa bản vá bằng việc đọc lại hàng kiểm kê và bảo đảm lời khai số dòng đã được bỏ, không thêm test ngữ nghĩa mới.

ĐÃ THỬ NGHIỆM: `wc -l cay-kho/ops/reviews/pr497-review-5-codex-verdict.receipt.yaml` ⇒ **149**. Đọc blob bằng `git -C cay-kho show e27d839:ops/reviews/pr497-review-5-codex-verdict.receipt.yaml` rồi đếm dòng ⇒ **143**; cùng phép ở `df09f3e` ⇒ **149**; ở `3c82ae3` ⇒ **rc=128**, tệp chưa tồn tại. Sau vá thử: `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json`, `python3 scripts/tl.py doc-claims-check --strict --json`, `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` đều **rc=0/ok=true**; cụm `**143** dòng` không còn. T26/t27/t13 sau phục hồi các đột biến đều rc=0.

ĐỘ TIN: **cao**.

## GIỚI HẠN

- Không mạng. Mọi trạng thái GitHub, quyết định/approval của chủ kho, nguồn gốc snapshot máy chủ, run/job/attempt/kết luận/thời gian CI, các Issue 128/101/bốn Issue/#498 và diễn biến Windows đều **KHÔNG ĐO ĐƯỢC** độc lập. Chỉ kiểm byte, nhãn nguồn, số học và cơ chế tại chỗ. Không tự xác nhận #490 đạt `landed`.
- Không chạy CI cho SHA này; không suy từ 12 lệnh xanh thành đủ 31 bước cổng. Chỉ chạy Linux và các fixture có sẵn; không đo Windows thật. Các advisory/miễn trừ nêu trong kết quả không bị chuyển thành phép đo đã đạt.
- Thông số runtime và danh tính thực của các lượt reviewer trước vẫn là attestation. Neo OID, băm và số tiêu đề khớp không chứng minh phiên cũ đã đọc/chạy đúng những gì nó kể.
- Phép A/B dùng một thư mục PATH có các liên kết tên `python`, `python3`, `git`, `bash`, `rg`, `actionlint`, `shellcheck`; nhánh B bỏ duy nhất liên kết `shellcheck`. Không cài công cụ. Không thực thi lệnh cài đặt của repository.
- Hướng thử cần nội dung tấn công mới không được triển khai. Bộ test/fixture có sẵn được dùng nguyên trạng; không soạn chuỗi thoát, đồng tự hay đường dẫn thoát cây.
- Đã dọn các bản chép và log tạm sau khi ghi kết quả. Hiện vật bàn giao duy nhất là `VERDICT.md`. Kiểm cuối `git -C cay-kho status --porcelain` trả rỗng.
