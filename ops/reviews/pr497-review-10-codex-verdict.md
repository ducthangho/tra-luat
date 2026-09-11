verdict: changes_requested
reviewed_sha: a6dcdbe57e823da297cc7d38f89a95c569190d27

## BẢNG ĐO

**0 P1 / 1 P2 / 0 P3.** Hai finding lượt 9 đã được sửa trong phạm vi kiểm được. Finding mới là một câu còn sót sau merge thứ ba; chưa thấy sai mới trong nội dung gốc §1/§2, chú thích `tong_hop` hoặc manifest.

Reviewer: Codex/OpenAI, bề mặt API có công cụ shell, transport machine. Tree tự đo: `6f841f69861e50798e6b92c7566358d16f746cec`. Mọi phép chạy và đột biến thực hiện trên bản sao trong sandbox; `cay-kho/` chỉ đọc. Môi trường chạy: Linux, Python 3.11.15, PyYAML 6.0.1, actionlint 1.7.7, shellcheck 0.9.0, jsonschema 4.26.0. Không cài thêm công cụ.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Cây giao review | HEAD `a6dcdbe`, tree như trên; detached, không shallow, abbrev 7, sạch | `rev-parse`, `symbolic-ref`, `config --local`, `status --porcelain`: đúng; `symbolic-ref` rc=1 do detached | Có |
| Base và diff | `27c413c..HEAD`; 14 tệp, +2.999/−5, 23 commit | Git cho đúng các số này. `diff.patch` và `numstat.txt` trùng byte với kết quả Git; 23 khối trong `commit-messages.txt` có tiêu đề khớp lịch sử | Có |
| Ba lần merge master | `0721811`, `c00c88a`, `27c413c` | Lịch sử first-parent có merge `1e75335`, `865adbd`, `6924295`, lần lượt nhận ba mốc ấy | Có |
| Thứ tự CHANGELOG sau merge | r364 → r363 → r362 → r361; không mất mục | Đúng thứ tự; nội dung các mục r364, r363 và r361 khớp base khi bỏ khoảng trắng phân cách | Có |
| Mục lục hợp nhất | PR497: 5; PR492: 4; PR500: 2 | Đếm đúng cột trong phần “Mục lục”: 5/4/2. Phần PR497 có 2 hàng cảnh báo. Chỉ kiểm việc giữ hàng của PR khác, không chấm nội dung chúng | Có |
| Bỏ số README của PR khác khỏi §3 | Chỉ còn 5 mục lục + 2 cảnh báo của PR497 | Dòng mô tả README ở §3 đúng phạm vi này. Dòng 597 vẫn nêu 4 biên nhận r363 và gắn số 57/110 với “head hiện tại”; xem finding | Một chỗ sót |
| Cấu hình gói | EVIDENCE chép nguyên `do-goi.txt`; origin trỏ mirror sandbox | Khối cấu hình trùng nội dung `do-goi.txt`; URL origin trỏ đúng `kho.git` trong sandbox | Có |
| Mirror và raw | 326 = 325 + 1 giao hàng; raw 324; thiếu 0, thừa 1, lệch OID 0 | So tập tên và OID: đúng; phần thừa là `pr487-merge`. Raw có 324 dòng, 26.116 byte, SHA-256 `06d030af79dbab01304558279374a430237230d76bd53b231177508bef67ae9c` | Có về hiện vật cục bộ |
| Ref mang r362 | Hai ref của nhánh này | Quét tiêu đề CHANGELOG trên 325 head **sau khi loại rõ ref giao hàng `pr497-head`**: đúng nhánh `claude/handoff-tra-luat-repo-2ak5th` và nhánh có hậu tố `-wip` | Có |
| Bản vá lượt 9 về CI ref sao lưu | Chỉ kết luận push trực tiếp không khớp bộ lọc; số lượt CI không đo được | YAML khai `push` với `branches: [master]`, `pull_request`, `workflow_dispatch`. EVIDENCE:34–39 phân biệt đúng cấu hình với lịch sử chạy; không thấy lời kết luận hiện hành khác rằng ref này có 0 lượt CI trong phần thay đổi đã quét | Đã sửa |
| §1: vế merged của ADR-0034 | `8cee941`, hai cha `00e017a` + `01e7f77` | `git show -s --format='%H %P' 8cee941` trả merge `8cee9410e958a6b9d956e080c11878fbd80d9f5f`, cha `00e017af102bc8355e0c276d2d813e20620ddb42` và `01e7f77d707cb093b5ba6d9b9d8577f40d025488`; là tổ tiên của base master trong clone | Có về Git cục bộ |
| §1: vế hậu-merge gate | Run `34391481045`, push/master, attempt 1; hai job success | **KHÔNG ĐO ĐƯỢC**: không có response/log job gốc. Bảng CI có nhãn thuật lại, phù hợp phần giới hạn nguồn của r362 | Đúng nhãn; chưa xác thực sự kiện |
| §1: bảng 41 bước | Ubuntu 37+4+0; Windows 35+6+0 | Hai phép cộng đều bằng 41. Trạng thái từng bước, giờ chạy, số attempt và so sánh ba run chỉ là thuật lại. YAML ở `8cee941`, `7693852`, `28ba133` giống HEAD; điều đó không xác thực các kết quả run | Khớp số học, không đo được lịch sử CI |
| §1: vế bookkeeping và kết luận landed | Bookkeeping là mục r359; #490 nay landed | Mục r359 có trong cây. Chỉ thị đóng chuỗi land-evidence và trạng thái GitHub là thuật lại. Vì hậu-merge gate chưa kiểm độc lập được, kết luận landed là kết luận dựa trên lời khai điều phối, không phải cả ba vế đều đã đo offline | Đúng giới hạn nguồn |
| §2: A/B đầy đủ, có shellcheck | Canary DAT, blocking | PATH dựng riêng trong sandbox: các tool DAT, canary bắt SC1003 với rc nội bộ 1; tổng DAT, lệnh rc=0 | Có |
| §2: A/B đầy đủ, thiếu shellcheck | Canary DO, blocking, báo suy giảm | Giữ nguyên PATH chung, chỉ bỏ thư mục chứa lệnh shellcheck: shellcheck KHONG_DO_DUOC, actionlint DAT, canary DO với thông báo thiếu shellcheck; tổng DO, lệnh rc=2 | Có; bác câu r361 bị rút |
| §2: `--chi` | Không chạy canary; có thể tổng DAT khi thiếu shellcheck | Thử `--chi shellcheck` và `--chi actionlint`, mỗi lệnh cả có/không shellcheck: cả bốn lần canary `[]`, rc=0. Riêng thiếu shellcheck với `--chi shellcheck`: tool KHONG_DO_DUOC nhưng tổng DAT | Có |
| Chú thích mới `tong_hop` | Mô tả cơ chế, không sửa runtime; diễn biến CI là thuật lại | `ast.dump(ast.parse(...))` của base và HEAD bằng nhau; diff chỉ thêm 23 dòng chú thích. Đọc `cai_cong_cu.sh`, YAML và chạy A/B xác nhận cơ chế; chú thích tách nhãn cho lượt Windows đỏ và Issue #498 | Có |
| Điều kiện phiên bản | Chỉ 2 trong 3 bản actionlint/shellcheck/jsonschema được CI ghim | actionlint 1.7.7 và jsonschema 4.26.0 được ghim; shellcheck có `ban_ghim: null`, lệnh cài CI không chỉ định phiên bản | Có |
| Manifest | 180 mục; chỉ CHANGELOG đổi hash | Tự đọc byte **từng tệp**: đủ 180 kích thước và SHA-256 khớp, tổng 8.181.382 byte. So hai manifest: tập đường dẫn không đổi; chỉ entry CHANGELOG đổi, từ 833.465 lên 887.060 byte | Có |
| Các verdict đã nhập | Các số dòng, byte, băm và severity trong §3 | Năm tệp lần lượt: 161/28.955; 259/43.791; 285/48.843; 296/51.844; 271/42.310 (dòng/byte). Băm khớp receipt; đếm tiêu đề được 0/1/1, 0/7/0, 0/6/0, 0/5/0, 0/8/0 (P1/P2/P3) | Có |
| Bản vá lượt 9 về số dòng receipt | Không còn gán độ dài hiện tại cho khối `nam_finding` | Quét số với `\d+`, không giới hạn số chữ số; đọc chú thích và parse YAML, gộp scalar gấp dòng. Khối có đúng 5 object; không còn lời khai độ dài hiện tại ấy. Những cặp số còn lại là đính chính lịch sử; ba mốc f6ec9c0, 3c82ae3, e27d839 tái đếm được 253/149, 260/149, 273/165 | Đã sửa |
| Bộ đếm hiện tại | EVIDENCE và bảng §3: 59/112; câu trước bảng: **57/110** | Validator trả **59 ĐẠT v2, tổng 112**; câu trước bảng sai, dù commit cuối khai đã sửa cả chuỗi | **Không — P2 dưới đây** |

Các lệnh sau chạy từ gốc bản sao sạch của exact HEAD; mọi thư mục tạm được đặt trong sandbox. EVIDENCE liệt kê 11 lệnh trong bảng và thêm một phép thử cờ sai bên dưới; không coi phép thử âm đó là cổng xanh thứ 12.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| `python3 ops/lease_publish_test.py` | 146/146, bỏ qua 0 | rc=0; 146/146, đã chạy 146, bỏ qua 0 | Có |
| `python3 ops/bien_nhan_v2.py --root .` | 59 v2, 11 legacy, 42 nợ; tổng 112 | rc=0; đúng các số trên, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC | Có |
| `python3 ops/cong_cu.py kiem-tra --json` | Tổng và canary DAT | rc=0; cả hai DAT | Có |
| `python3 ops/cong_cu_test.py` | 23 ca, 18 đột biến, lỗi đột biến 0 | rc=0; 23/23, bỏ qua 0; 18 đột biến giết đúng ca đích, lỗi 0 | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | ok, expected=checked=180 | rc=0, ok=true, 180=180; failed và extra_files rỗng; package hash khớp `a16dafb3978e0bb605fb04232b0dddb5275ff84f73e41c19d2b7709fffbd4606` | Có |
| `python3 scripts/tl.py golden-test --json` | ok=true | rc=0, ok=true, 20 ca | Có |
| `python3 scripts/tl.py determinism-audit --strict --json` | ok=true | rc=0, ok=true | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` | ok=true | rc=0, ok=true; có 368 advisory, không suy thành không còn lời khai sai | Có |
| `python3 scripts/tl.py workflow-audit --strict --json` | rc=0 | rc=0, ok=true | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 | rc=0; quét 7 tệp, 0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc=0 | rc=0; 46 ADR/46 dòng, giữ ngoại lệ trạng thái 0016 có sẵn | Có |
| `python3 scripts/tl.py golden-test --strict --json` | Không nhận `--strict`, rc=2 | rc=2, parser từ chối cờ | Có |
| Phạm vi CI | 31 bước cổng; các lệnh trên chưa đủ bộ | YAML có 40 step, 37 step có `run`; bỏ 6 step cấu hình/cài đặt còn 31. Không lấy số step YAML làm số bước thực thi của một run GitHub | Có với cách đếm này |

Đột biến chủ động, mỗi ca độc lập và khôi phục bản gốc trước ca kế tiếp. `t26`, `t27`, `t13` được gọi trực tiếp từ module test sẵn có bằng `runpy.run_path`; nền cả ba rc=0. Ví dụ lệnh dùng cho `t26`:

```sh
python3 -c "import runpy; d=runpy.run_path('ops/lease_publish_test.py'); next(v for k,v in d.items() if k.startswith('t26_') and callable(v))()"
```

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Bỏ tệp verdict lượt 1, giữ receipt và mục lục | t26 đỏ, t27 xanh | t26 rc=1, đúng lỗi tệp không tồn tại; **t27 rc=0** | Có; t27 không bắt ca này |
| Bỏ receipt lượt 1 | t27 đỏ | t27 rc=1, đúng lỗi thiếu receipt; **t26 rc=0** | Có; t26 không bắt ca này |
| Bỏ hàng mục lục lượt 1 | t27 đỏ | t27 rc=1, đúng lỗi thiếu tên trong cột mục lục; t26 rc=0 | Có |
| Bỏ hàng cảnh báo lượt 1 | t27 đỏ | t27 rc=1, đúng lỗi caveat thiếu trong cột id; t26 rc=0 | Có |
| Đổi điều kiện chạy canary thành `if False` | Cơ chế có test bảo vệ | t13 rc=1 tại chốt nghiệp vụ “canary mất executable bị nuốt”, không phải lỗi import/parse. Lệnh đầy đủ khi thiếu shellcheck bị đột biến đổi từ rc=2 thành **rc=0, canary=[]** | Có răng ở test đích |
| Đổi hàng Ubuntu của §1 từ 37 success/4 skipped thành 36/5, giữ tổng 41 | Không khai cổng hiểu nghĩa văn xuôi | Với manifest cũ: release-verify **rc=2**, chỉ CHANGELOG lệch hash, kích thước vẫn bằng nhau. Sau `release-manifest --out RELEASE_MANIFEST.json --json`: release-verify, doc-claims-check, bien_nhan_v2, doctrine-scan và adr-song **đều rc=0** | Năm cổng đã thử không bắt sai nghĩa sau tái sinh manifest |

Một lần dựng phép thử văn xuôi dừng vì chuỗi neo xuất hiện ở nhiều mục; đã giới hạn neo vào §1 và chạy lại. Không tính lỗi giàn giáo đó là bằng chứng giết đột biến. Sự sống sót của đột biến văn xuôi **không** được dùng để yêu cầu xây cổng ngữ nghĩa mới.

### chuoi-bo-dem-van-khai-57-110-cho-head-sau-merge-thu-ba  [P2]  Câu trước bảng vẫn gán bộ đếm cũ cho head hiện tại

TỆP/DÒNG: `cay-kho/CHANGELOG.md:597`; đối chiếu dòng 602, `EVIDENCE.md:68–70` và thông điệp commit `a6dcdbe` trong `commit-messages.txt`.

VẤN ĐỀ: Dòng 597 vẫn ghi “head hiện tại ⇒ **57/110** — nhảy **4** vì merge `c00c88a`…”. Trên exact HEAD được giao, validator trả **59/112**, đúng như dòng 602 và EVIDENCE. Vì vậy hai câu cùng §3 tự mâu thuẫn sau merge `27c413c`. Đây không phải số lịch sử được ghim: câu gọi rõ “head hiện tại”. Commit cuối còn khai “Bảng cổng §3 và chuỗi ghim SHA nay ghi head hiện tại 59…” nhưng `git diff HEAD^ HEAD -- CHANGELOG.md` cho thấy chỉ dòng bảng đổi 57→59 và 110→112, chuỗi phía trên không được sửa. Phần giải thích chỉ một lần tăng 4 cũng đã cũ đối với head sau merge thứ ba.

ĐÃ THỬ VÁ: có — trong bản sao tạm, bỏ đoạn dùng “head hiện tại ⇒ 57/110” và phép liệt kê biên nhận của PR khác; giữ chuỗi số lịch sử đã ghim, ghi rõ bảng dưới là số đo trên `a6dcdbe`, bộ đếm bao gồm mọi biên nhận trong kho và có thể đổi khi merge master. Tái sinh manifest bằng cổng có sẵn. Bản vá thử chỉ đổi CHANGELOG và manifest; không áp vào `cay-kho/`.

ĐÃ THỬ NGHIỆM: `python3 ops/bien_nhan_v2.py --root .` trước và sau vá đều rc=0, **59 ĐẠT v2 / tổng 112**. `git diff HEAD^ HEAD -- CHANGELOG.md` xác nhận phạm vi vá thiếu như trên. Sau bản vá thử, `python3 scripts/tl.py doc-claims-check --strict --json` và `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` đều rc=0, ok=true; tự đọc lại đủ 180 kích thước và SHA-256 đều khớp. Kiểm câu 57/110 không còn gắn với head hiện tại. Khi áp bản vá thật, kiểm lại đúng đoạn này với đầu ra validator; không cần thêm test sản phẩm cho văn xuôi. Rủi ro cần tránh: thay bằng một số “head hiện tại” khác lại tiếp tục trôi; sửa CHANGELOG mà không tái sinh manifest sẽ làm cổng kiểm hash đỏ.

ĐỘ TIN: cao

## GIỚI HẠN

- Không mạng: **mọi trạng thái GitHub đều KHÔNG ĐO ĐƯỢC**, gồm #490 landed, CI `34391481045`, các lượt Windows được kể, CI của head review/ref sao lưu, Issue, approval, submitter và chỉ thị trên GitHub. Nhãn thuật lại đúng không biến chúng thành phép đo độc lập.
- Raw `ls-remote` chỉ được kiểm byte, số học, tập tên và OID với mirror được giao. Không xác minh được nguồn GitHub, giờ chụp, thứ tự fetch/dựng gói hay lần chạy script của điều phối.
- Không có runtime transcript gốc của chín lượt review trước trong gói. Không xác thực model, session, việc đọc tệp hay tuân thủ sandbox của họ từ các scalar tự khai; băm/OID trùng chỉ chứng minh quan hệ giữa hiện vật. Model ID chi tiết của phiên này cũng không có phép đối chiếu độc lập.
- Chạy các lệnh đã nêu trên Linux; không chạy toàn bộ CI hay xác nhận hành vi trên máy Windows thật. Kết luận đột biến chỉ áp cho các ca/cổng đã liệt kê.
- Không chấm nội dung hồ sơ `pr492-*`, `pr500-*`, r363, r364; chỉ kiểm chúng được giữ sau merge. Không tự soạn chuỗi tấn công; các hướng cần chuỗi thoát, đồng tự hoặc đường dẫn vượt cây không được dựng mới. Các suite sẵn có được chạy nguyên bản.
- Kiểm cuối: `git -C cay-kho status --porcelain` rc=0, stdout **rỗng**; HEAD vẫn `a6dcdbe57e823da297cc7d38f89a95c569190d27`.
