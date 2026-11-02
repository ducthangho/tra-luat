verdict: changes_requested
reviewed_sha: aecdccd32b748fd5694231976193ade2e34ea10d
spec_sha256: 1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715
model/effort tự khai: GPT-6 theo cấu hình phiên; exact served model và effort KHÔNG ĐO ĐƯỢC
provider: openai_codex
execution_surface: API agent có shell cục bộ (không tự nhận Codex CLI/Desktop)
transport: machine, hiện vật cục bộ; không có GitHub submitter
reviewed_tree: f1e1128de9ca8233e768edbd30cdd456491682c7
base_sha: 1741e0a1ab7ebce4b26912aefadca56ddfcdc691
assurance: review nội dung độc lập; không tự cấp cross_approved hoặc land authority

Q1/Q2 và phần sửa A2/A5 có khả năng đóng va chạm ép kiểu trong phạm vi đã quyết. Tuy nhiên chưa thể dùng r2 làm hợp đồng thi hành: closure chưa được neo bằng hash, và công cụ A9 còn cho âm giả/thiếu bằng chứng. Áp ngưỡng của prompt: chỉ approve khi không còn lớp P1/P2/P3.

Đã đọc toàn bộ prompt.snapshot. Hai phép kiểm đầu tiên sau khi đọc chỉ thị:
```text
$ sha256sum SPEC.md
1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715  SPEC.md
$ git -C cay-kho rev-parse HEAD
aecdccd32b748fd5694231976193ade2e34ea10d
```
Mọi lệnh dưới đây chạy từ `$R` tuyệt đối đã giao. `goi/scratch-path` và `goi/hint-scratch-path` chứa các thư mục tạo bằng `mktemp -d -p "$R"`; code phản chứng, Git fixture, tempfile và bản sao áp patch đều nằm ở đó. Dùng `PYTHONDONTWRITEBYTECODE=1`, TMPDIR nằm trong scratch. Không sửa checkout hoặc mirror, không dùng mạng hay đăng GitHub. Lệnh gọi hàm sản phẩm và seam được ghi rõ, không coi mô hình tạm là mã PR.

Đã đọc AGENTS/CONTEXT, CLAUDE phần Bài học đắt giá, protocol §3.2/§4/§8/§13, skill soan-spec L1–L5 và bảng mục bắt buộc, mã thật và các helper/ca liên quan. Không cần thực hiện quy trình hỏi lại của skill soạn spec: đây là review được giao, Q1–Q4 đã được chủ kho xác nhận. Đọc skill để kiểm hợp đồng, không tự nhận quyền soạn/cấp lease.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã làm trước các hướng săn mới. Nguồn: `luot1/VERDICT.md`, `luot1/HINT.patch`, `r1-r2.diff`; đọc lại mã tại reviewed SHA. Mô hình chốt chỉ là thí nghiệm trên bản sao, không là implementation ứng viên.

| lớp lượt 1 | trạng thái | bằng chứng |
|---|---|---|
| tieu-chi-dot-bien-khong-phan-biet-chot | ĐÃ ĐÓNG | `PYTHONDONTWRITEBYTECODE=1 python goi/recheck.py`: A2 direct strict=8, restore_D2=RETURN, L_remove_D2=RETURN; cả ba probe=RETURN/GH=0. Đột biến L đúng định nghĩa t178 là gỡ chốt lease_id bên trong helper; ca trực tiếp có răng. A5 đã đóng: D5_self/D5_peer False→True, D6_self/D6_peer 8→RETURN, các đối chứng chuỗi giữ True/RETURN. |
| bo-quet-nghiem-thu-thieu-mien | CÒN MỞ | Cùng lệnh: Phụ lục A gọi qua `quet()` phân đúng good, int_yml, missing, list, parse, pointer_list, local_bool, broken_ref. `goi/hunts.py schema` cho các con trỏ trắng lọt; `ref_domain` cho ref thường topic/HEAD bị bỏ. Những nhánh lỗi cũ đã được bổ sung nhưng lớp miền hợp lệ vẫn chưa đóng. Cửa chạy và provenance ảnh được tách thành lớp mới vì cần cách chữa khác. |
| so-do-nen-khong-khop | ĐÃ ĐÓNG | Cùng lệnh: A6 có hai ref/path, `NGƯỜI_GIỮ 1: True`, rc=11, khớp bản sửa. `goi/measure.py`: 506 ref (505 remote + một local head), 560 blob/cặp, đều str; 506 so 507 do local head khác môi trường soạn. Suite rc=0, 187/187, bỏ qua=0 với shellcheck/actionlint đúng phiên bản. Không bác số lịch sử từ khác biệt snapshot. |
| hop-dong-dong-bang-thieu-neo | VÁ SINH LỖI MỚI | `sed -n '126,190p' cay-kho/docs/PROTOCOL_DA_PHIEN.md` nêu “Các trường này cùng nằm trong spec_hash”. `sed -n '1,34p' SPEC.md`: mission trống, băm chỉ bytes tệp rồi cho bổ sung closure vào lease hoặc khai vắng. Đã thêm environment/risk/công thức nhưng chưa đóng hợp đồng. |
| bang-duong-phan-loai-sai | ĐÃ ĐÓNG | `goi/recheck.log` mục SOURCE_D7_D9 xác nhận :2110/:2123 là D7, :2139/:2143 chỉ hiển thị; :1938/:1942 so thô, :1946 f-string, :1967 str rồi tra sổ. A7 đã tách hai CLI và bắt ca trực tiếp D8. |
| trang-thai-q3-chua-dong-bo | ĐÃ ĐÓNG | `goi/recheck.log` mục Q3: header, §3 và §10 đều ghi đã xác nhận; #678 comment 5885268193 được neo. Authority xác nhận Q1–Q4 có trong prompt; không đo live object GitHub. |

Log nguyên văn: `goi/recheck.log`. Lần dựng fixture đầu thất bại vì cấu hình ký commit kế thừa; đã tắt `commit.gpgsign` chỉ trong các repo tạm rồi chạy lại. Không nhận lỗi setup làm tín hiệu giết mutant.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện (vị trí trong SPEC) | phương án chung | phép kiểm / giới hạn |
|---|---|---|---|---|
| hop-dong-dong-bang-thieu-neo | P1 | header :10, :22–31; mission trống và cho closure nằm ngoài bytes băm | Đánh dấu chưa ready thi hành; điều phối hoàn tất hợp đồng/ngoại lệ trước revision/hash/lease mới | Hướng 5; không có authority để tự điền mission/closure |
| bo-quet-nghiem-thu-thieu-mien | P2 | A9 :212–225; Phụ lục A :303–304, :319–323 | Dẫn xuất miền ref và schema đầy đủ, thêm ca phần bù | Hướng 2/7; snapshot thật sạch, phản chứng ở kho tạm |
| bo-quet-chung-cu-khong-neo-anh | P2 | Phụ lục A :303–324; A9 :219–222; §8 :244–247 | Giữ map ref/OID và cặp/miền, đọc theo OID, báo đúng mẫu số | Hướng 3; race được dựng tại seam, không khai race đã xảy ra ở nguồn |
| bo-quet-khong-co-cua-chay | P2 | §8 :244; toàn khối Phụ lục A :295–325 và bảng tự kiểm :327–342 | Công bố entry point, JSON dương và quy tắc rc; tự kiểm qua subprocess | Hướng 1; không biết wrapper lịch sử của phiên soạn |
| objective-dong-nhat-cu-phap-voi-danh-tinh | P3 | objective :12 | Nói danh tính theo chuỗi sau safe_load; thu hẹp lời hứa về ép kiểu | Hướng 6; không đề nghị đổi Q1/loader |

Giữ nguyên slug hai lớp còn mở từ lượt trước; các lớp mới về cửa chạy và provenance không đếm lại cùng biểu hiện trong lớp miền. Những lớp cũ đã đóng không tính thành finding mới. Header closure được nâng từ P2 lên P1 vì r2 không chỉ thiếu trường: nó đã cho phép một cách đóng băng trái protocol, nên executor làm đúng vẫn không có hợp đồng đủ điều kiện thi hành.

## BẢNG SĂN

Các hướng bên dưới đo phần mới của r2. Không tính việc đọc tài liệu, kiểm băm, bảng đối chiếu lượt trước, hay chạy suite đơn thuần thành một hướng độc lập. Các phép CLI/miền/schema/provenance dùng phản chứng riêng; số lịch sử được tách khỏi số snapshot.

Ghi chú kiểm dụng cụ: lần nháp đã gỡ lời gọi helper và gán nhầm tên L. Đọc t178 :7717 xác nhận L gỡ chốt lease_id BÊN TRONG helper; đã sửa phép thử, chạy lại, hủy kết luận nháp. Không gán một mutant khác cho #677.

### HƯỚNG 1: Khối mã mới có thực thi phép quét khi chạy như script?
- Giả thuyết: trích và chạy khối mã Phụ lục A theo §8 có thể xanh mà không quét gì.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py entry` (khởi chạy nguyên `goi/appendix.py` ở các kho có đáp án biết trước).
- Output: good, int_yml, broken_ref và missing_repo đều `script_rc=0 stdout='' stderr=''`.
- Kết luận: LỖI. Khối mã chỉ định nghĩa hàm, không có caller/CLI/exit status. Bảng tự kiểm gọi `quet()` chứng minh hàm phát hiện lỗi nhưng không chứng minh các rc đã khai của script. Cần đóng gói lệnh gọi, xuất bằng chứng dương và ánh xạ lỗi sang rc. Không suy ra phiên soạn chưa hề gọi hàm bằng một wrapper ngoài tệp; wrapper ấy KHÔNG có trong công thức được công bố.

### HƯỚNG 2: Schema con trỏ chuỗi rỗng sau bản sửa phân biệt list/str
- Giả thuyết: sửa nhận đúng kiểu container vẫn cho lọt phần tử chuỗi mà schema sản phẩm bác.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py schema`.
- Output: empty_item và space_item đều `APP=(1,1,1,[])`, nhưng `_danh_sach_thay_the_cho` trả `None`; space_tombstone cũng `APP=(1,1,1,[])`, `_bia_mo_doi_xung=False`; đối chứng valid cho `['old']` và True, scanner sạch; empty_list hợp lệ.
- Kết luận: LỖI. A9 đòi schema sản phẩm, Phụ lục A mới chỉ kiểm str. Đây là phần còn mở của lớp bộ quét cũ. Bổ sung ca `thay_the_cho: [""]`, `["   "]`, `da_bi_thay_the: "   "` và đối chứng; không mở phạm vi sang sửa lịch sử lease.

### HƯỚNG 3: Bằng chứng của A9 có gắn với đúng OID và phân tách lịch sử?
- Giả thuyết: bộ quét mới bỏ OID sau khi liệt kê, đọc lại tên ref trôi; khử trùng blob làm mất thông tin miền/path.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py evidence`.
- Output: cùng bytes ở `ops/leases/live.yaml` và `ops/leases_retired/past.yaml` trả `(1,1,2,[])`; không có nhãn hai miền, số kiểu hay map ref/OID trong kết quả. Ca đổi ref tại seam sau `for-each-ref`: ref lúc liệt kê chứa `lease_id: 1000`, nhưng `SCAN_AFTER_MOVE=(1,1,1,[])` sau khi ref chuyển sang commit có chuỗi. OID cụ thể của hai commit nằm trong `goi/hunt-evidence.log`.
- Kết luận: LỖI. Chỉ ra phạm vi bằng chứng thiếu, không khẳng định repo thật đang có race. A9 đã đòi tập ref+OID nhưng công cụ bỏ chính OID vừa đọc; cần giữ map và `ls-tree` trên OID ấy, báo riêng từng miền/cặp và loại kiểu. Đây là lớp mới về provenance ảnh (`bo-quet-chung-cu-khong-neo-anh`), tách khỏi tập giá trị hợp lệ của bộ quét; không yêu cầu đổi scanner runtime.

### HƯỚNG 4: Truy nguyên phần tăng 559→560 được r2 khai chưa đo
- Giả thuyết: hai nhánh cùng thêm lease nhưng chỉ tăng một blob do lease của một nhánh đã xuất hiện ở ref khác.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/measure.py`; `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py counts`.
- Output: snapshot có 505 origin ref = 505 mirror head, bằng nhau cả tên/OID; một local head nên Phụ lục A trả `(506,560,560,[])`, phép quét độc lập ra str=560, errors=[]; hai nhánh mỗi nhánh có một blob độc quyền: 0492f6a2fb5da2f532301774f1be11b9d6d40bbf và 9ef27167168dae1abb89f894ee5a74e4aec515b8. Bỏ cả hai ref khỏi ảnh hiện tại còn 558 blob, không phải 559. Full output ở `goi/hunt-counts.log`.
- Kết luận: KHÔNG PHẢI LỖI chỉ vì 506≠507: clone review có ít hơn môi trường soạn một local head, 560 blob và cặp đều khớp. Không có ảnh ref/OID trước fetch 07:21Z nên chưa thể chứng minh lịch sử 559→560 bằng cách bỏ hai nhánh khỏi ảnh hiện tại. Không coi lời khai KHÔNG ĐO ĐƯỢC là số sai.

### HƯỚNG 5: Hash của hợp đồng header mới có bảo vệ closure?
- Giả thuyết: r2 cho đổi required_checks/closure trong lease mà hash đặc tả vẫn giữ nguyên.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py contract`; đọc protocol §3.2/§3.2.1/§13.
- Output: external_lease_closure `required_checks=['A']` và `['B']` đều cho `1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715`; header nói mission chưa cấp, cho closure nằm ngoài tệp; grep mission ở đặc tả #579 trả []. Các lease đọc tại snapshot có cả ID tên đọc được (xem log).
- Kết luận: LỖI. Tiền lệ bỏ mission không phải ngoại lệ protocol; closure bắt buộc cùng nằm trong spec_hash, thiếu closure còn bị §13 từ chối. environment=cloud nay đã tường minh; riêng việc chọn cloud không có phản chứng kỹ thuật. Hai nền bất biến/tiếp nối đúng §3.2.1. Chưa có bằng chứng để kết luận lease dùng tên đọc được đã gây lỗi runtime; cần giữ tên canonical trong hợp đồng, không đổi các lease lịch sử.

### HƯỚNG 6: Objective mới phân biệt giá trị hay cách viết YAML?
- Giả thuyết: mệnh đề mới “hai cách viết YAML khác nhau không bao giờ ra cùng một dấu đăng” rộng hơn Q1 đã được cấp.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py objective`.
- Output: `'yes'`/`!!str yes`, `'1.5'`/`!!str 1.5`, `fresh`/`"fr\u0065sh"` đều qua Q1 ở cả hai vế, cùng chuỗi và cùng dấu. Unicode tổ hợp/dựng sẵn, khoảng trắng đầu/cuối và newline bị regex loại; A/a cùng hợp lệ và khác nhau. Khóa YAML lặp cho giá trị cuối fresh.
- Kết luận: LỖI P3 ở lời khai objective mới, không là lỗ còn mở của Q1: chủ kho chọn danh tính sau safe_load, không chọn văn bản YAML gốc. Thu hẹp objective về va chạm do ép giá trị không phải chuỗi; giữ nguyên các biểu diễn ra cùng chuỗi là cùng danh tính.

### HƯỚNG 7: “Bỏ symbolic HEAD” có đúng bộ lọc suffix mới công bố?
- Giả thuyết: `endswith('/HEAD')` bỏ cả một ref thường có leaf HEAD mà Git cho phép, nên A9 không bao phủ đúng miền đã khai.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py ref_domain`.
- Output: `refs/heads/topic/HEAD` là ref thường (symref rỗng), chỉ nó mang `lease_id: on`; Phụ lục A trả `(1,1,1,[])`; runtime `_cac_ref_cuc_bo` cũng bỏ ref đó. OID/ref thật trong `goi/hunt-ref-domain.log`.
- Kết luận: LỖI ở phát biểu miền và thuật toán của công cụ A9: bỏ mọi suffix HEAD không tương đương bỏ symbolic HEAD. Runtime hiện cùng hạn chế, nên không khai bộ quét hẹp hơn runtime ở ca này. Đề nghị A9 quét tập bảo thủ bao trùm runtime, chỉ miễn đúng symbolic HEAD, test ref thường có hậu tố HEAD. Không tự giao sửa bộ liệt kê ref runtime ngoài mục tiêu packet.

### HƯỚNG 8: Phần A7 mới có thực sự tách được hai entry point?
- Giả thuyết: thêm D1 sẽ chặn luôn D8 ở cả hai CLI, khiến phần bổ sung A7 không có răng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`, mục A7; gọi CLI handler thật, seam Git offline và spy tại điểm vào D8.
- Output: nền `ai_dang_giu_D8_types=['int'] rc=11`, `check_D8_types=['int'] rc=0`; mô hình D1 strict: `ai_dang_giu_D8_types=['int'] rc=11`, `check_D8_types=[] rc=8`.
- Kết luận: KHÔNG PHẢI LỖI. Hai nhánh mới trong A7 cần thiết và khả thi; đường ai-dang-giu không được miễn nhờ D1. Mô hình này chưa cài D7/D8, không phải ứng viên. Không có bằng chứng bắt buộc sửa caller ngoài write set.

### HƯỚNG 9: Lời khai mới về workflow có đúng với Python thật và gh giữ trạng thái?
- Giả thuyết: §1 mới lấy kết quả từ stub của `_chay_buoc_dang`, khiến ca âm/dương cùng không đăng mà vẫn tưởng đã đo sản phẩm.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`, mục WORKFLOW; trích nguyên thân bước bằng `_buoc_workflow('đăng')`, không sửa workflow; gh giả trên PATH, mọi POST cập nhật state.json trong kho tạm.
- Output: base yes `rc=0 POST=0 calls=2`; base fresh-id `rc=0 POST=1 calls=4`; mô hình strict yes `rc=1 POST=0 calls=0`; strict fresh-id `rc=0 POST=1 calls=4`. Log riêng của mỗi lần nằm dưới scratch-path/workflow-*.
- Kết luận: KHÔNG PHẢI LỖI về kết quả rc/POST r2 mới công bố. Số calls không là tiêu chí A3; không dùng tổng số của lượt trước thay phép đo này. Harness cũ `_chay_buoc_dang` dùng stub, nên executor cần harness giữ Python thật như A3 đã yêu cầu; làm được trong test file.

## BẢNG ĐO

Thời điểm: `goi/recheck.log`, `goi/measure.log`, `goi/hunt-*.log` có UTC. Suite chạy từ khoảng 07:32Z đến 07:36Z 29-09-2026, xem timestamp từng ca trong `goi/suite.log`. Mọi số đo bên dưới lấy từ các script/log đã kèm; không lấy quan hệ đúng thay phép kiểm số hạng.

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| §1 bool true/yes/on/True | str True; D2=8, D1 qua | y hệt (`runtime.py`: SCALAR) | Có |
| §1 float 1.5/1.50 | str 1.5; D2=8, D1 qua | y hệt | Có |
| §1 hex/octal/underscore | 31/15/1000; D2/D1 qua | y hệt | Có |
| §1 date | 2026-09-29; D2=8, D1 qua | y hệt | Có |
| §1 chuỗi yes | str yes; D2/D1 qua | y hệt | Có |
| §1 va chạm | các cặp liệt kê rc=9; khác tên rc=0 | mọi cặp liệt kê 9; khac-lease/yes 0 | Có |
| §1 workflow mới | yes 0/0 POST; fresh-id 0/1 POST | y hệt, Python thật + gh trên PATH | Có |
| §2 D1/D2/D3/D4 | :861/:949/:668/:1070 | y hệt (`identity-paths.log`) | Có |
| §2 D5/D6 | :587/:592 và :609/:612 | y hệt | Có |
| §2 D7 | :2110/:2123 | đọc ID/lập khóa ở đúng hàm | Có |
| §2 D8 | :1938/:1942/:1946/:1967 | đúng vị trí và cơ chế như bảng r2 | Có |
| §2 D9 | :2074/:2089/:2139/:2143 | hiển thị, không so khóa danh tính | Có |
| §2 sổ thu hồi | :1192 đã đòi str | lấy ở 1192, kiểm str/regex/tên tệp ở 1193 | Có, mốc vùng mã |
| §2 packet_loop | :769–771 đã đòi str | vòng trường/đọc/kiểm tại các dòng ấy | Có |
| §2 workflows | không đọc lease_id | rg `lease_id` trên .github/workflows/*.yml không có dòng | Có |
| §8 ref remote | 505=505 | 505 origin=505 mirror, bằng tên+OID | Có ở snapshot; live KHÔNG ĐO ĐƯỢC |
| §8 ref tổng | 507=505 remote+2 local | 506=505 remote+1 local | Khác local head; không chứng minh số lịch sử sai |
| §8 blobs/cặp | 560/560 | 560/560 | Có |
| §8 kiểu ID/parse/schema | str 560/560, lỗi 0 | str 560/560, lỗi 0 qua phép quét độc lập | Có ở dữ liệu thật; không chứng minh scanner đủ miền |
| §8 hai nhánh sau fetch | mỗi nhánh thêm một lease | mỗi nhánh thêm một lease, blob riêng; ảnh hiện tại bỏ cả hai còn 558 | Có về số thêm; lịch sử tăng chỉ một KHÔNG ĐO ĐƯỢC |
| §8 người giữ .py / test | 0 / một t131 | 0 rc=0 / đúng t131 rc=11 | Có, seam máy chủ dùng tập mirror đã đối chiếu |
| §8 số dòng | 2206 / 10508 | 2206 / 10508; cả hai blob bằng base | Có |
| §8 số ca/max | 187 / t192 | len(CA)=187, max=192 | Có |
| A6 | nền rc=11; một người giữ True | rc=11, đúng hai ref/path và một khóa True | Có |
| A8/§8 suite hiện tại | 187/187; chạy=187, bỏ=0 | 187/187; chạy=187, bỏ=0; rc=0 | Có |
| A8 số lịch sử | 185/187 thiếu shellcheck | môi trường này có shellcheck 0.9.0/actionlint 1.7.7; không có log cũ | Không bác lịch sử |
| Ruff | KHÔNG ĐO ĐƯỢC | `python -m ruff --version` rc=1, No module named ruff | Có về giới hạn; chưa chạy lint F |
| Phụ lục A tự kiểm | good rc=0, âm rc=1/khác0 | gọi hàm nhận đúng lỗi cũ; script nguyên văn mọi ca rc=0/rỗng | Không ở cửa chạy công bố |
| mission của #579 | grep mission 0 dòng | [] (`hunts.py contract`) | Có, nhưng không tạo ngoại lệ protocol |

Lệnh kiểm bổ sung cho bảng đường: `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho|\.stem|name\[:-5\]' cay-kho/ops/lease_publish.py`; đọc flow D1–D9 và `kiem_ban_ghi_thu_hoi`. Không thấy đường quyết định lease_id chưa được liệt kê; tên tệp ở D8 đi từ sổ thu hồi, nơi validator đã kiểm str/regex/tên. Lệnh tìm caller Q3: `rg -n --hidden 'ai-dang-giu' cay-kho/.github cay-kho/.claude/skills cay-kho/ops --glob '*.py' --glob '*.sh' --glob '*.yml'`; kết quả vận hành thấy trong mã sản phẩm/test, các hồ sơ review cũ và chú thích dựng gói. Không có bằng chứng cần sửa workflow/skill ngoài write set do Q3. Không suy từ tìm chuỗi rằng đã kiểm mọi caller động.

## KHẢ NĂNG ĐỎ A1–A10 VÀ PHẦN NGOÀI HINT CŨ

| tiêu chí | kiểm trên r2 | giới hạn |
|---|---|---|
| A1 | `runtime.py` đọc văn bản YAML bằng _doc_yaml: nền qua, strict=8; quoted yes qua | Dùng kiem không tep và bỏ hạn như §1 để D6/neo không che D1 |
| A2 | `recheck.py`: direct int 8→RETURN khi trả D2 cũ hoặc gỡ chốt L; probe vẫn RETURN/0 GH | L đúng là gỡ chốt ID trong helper, không phải gỡ lời gọi cả helper |
| A3 | workflow 0/0→1/0 với bool; đối chứng 0/1 giữ nguyên; direct D3 nền 9→8 | Workflow chứng minh tích hợp; đơn vị đo D3 riêng tránh D1 che |
| A4 | dung_than trực tiếp bool: nền trả thân, strict=8 | Mô hình kiểm tra chốt, chưa có ca ứng viên |
| A5 | các toán hạng D5/D6 phân biệt được bằng fixture r2, giữ các chốt khác | Ca trong recheck là quan sát kết quả, chưa phải catalog TinHieuChotCa của executor |
| A6 | nền đã nonzero=11; nhãn/ref/path mới là tín hiệu có răng | Ca Q3 phải thu được cả hai lỗi, không dừng sau lease đầu |
| A7 | hai handler CLI đã đo riêng; direct D8 cần khi thêm validator ở D8 | Chưa có code D8 ứng viên để thử mutant cụ thể |
| A8 | suite nền thực chạy đủ | ứng viên chưa tồn tại; delta code và lint F KHÔNG ĐO ĐƯỢC |
| A9 | self-test hàm cũ phần nhiều đúng; ca mới chứng minh các lỗ miền/cửa chạy/provenance | snapshot sạch không cứu được công cụ nhận sai fixture |
| A10 | yêu cầu phân biệt đúng lớp ngoại lệ/đúng tên ca hợp lý, làm được bằng chot/TinHieuChotCa sẵn có | Chưa có catalog A1–A7 ứng viên để xác nhận actual kill matrix; không gọi mọi A đã đo trên ứng viên |

Đã áp nguyên `luot1/HINT.patch` lên bản sao r1 trong scratch bằng `patch -p0 --fuzz=0`, rc=0 (`goi/previous-hint-apply.log`), rồi `diff -u` với SPEC r2 ra `goi/beyond-previous-hint.diff`. Phần ngoài HINT gồm header/closure/objective, lời khai workflow, A2 về thứ tự #677, §8/§10, Phụ lục A; đều được xem riêng, không coi “đã áp HINT” là bằng chứng đúng.

A2 về #677: runtime/test nền định nghĩa L gỡ chốt lease_id của D2, nên cách đo trực tiếp mới là tương thích trong mô hình. Nhánh packet này land trước hay #677 land trước đều có thể sửa test trong write set; không có yêu cầu kỹ thuật bắt buộc sửa đặc tả #677. Nhưng toàn bộ Issue/revision0 và acceptance tương lai #677 không có trong snapshot: KHÔNG ĐO ĐƯỢC lời khai live ấy, không tự xác nhận nó. Trước cấp lease người điều phối vẫn phải chốt thứ tự và revision hợp đồng tương thích. §10 nói mới kiểm khả thi là giới hạn đúng, nhưng câu đó không chứng minh scanner A9 đầy đủ hay loại bỏ các finding mới.

## CHI TIẾT TỪNG LỚP

### hop-dong-dong-bang-thieu-neo [P1] Hợp đồng cho closure nằm ngoài băm đã đóng băng
VỊ TRÍ: SPEC :10, :22–31; protocol §3.2 :126–166 và §13 :1107–1112.

VẤN ĐỀ: r2 nói spec_hash là hash toàn bytes tệp và đã đóng băng, nhưng mission chưa cấp, closure lại được ghi riêng lúc cấp lease hoặc khai vắng. Protocol đòi mission tối thiểu, closure cùng nằm trong spec_hash, và từ chối làm khi closure thiếu. Thực hiện đúng r2 có thể nhận một lease với cùng băm nhưng required_checks/land_obligations khác; không tự kiểm được hợp đồng đầy đủ. Việc spec #579 cũng thiếu mission không cấp ngoại lệ cho packet này. Các trường environment/risk/công thức đã bổ sung là tiến bộ thật; chúng không đóng phần còn thiếu.

HINT: có — nhóm `hop-dong-dong-bang-thieu-neo`. Điều phối hoàn tất mission hoặc ngoại lệ có authority, và closure, trong revision mới trước ready/cấp lease. Bản gợi ý chỉ phân biệt hồ sơ review đóng băng với hợp đồng chưa ready; không bịa authority hay giao executor sửa ngoài write set.

ĐÃ THỬ: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py contract`: hai external closure khác required_checks vẫn cùng hash 1575fb3e…d5715; protocol đọc được yêu cầu ngược lại. Kiểm đóng lớp: hash revision đã đủ trường phải thay nếu bất kỳ trường hợp đồng/closure thay. Rủi ro vá: không nhúng hash tự tham chiếu; giá trị hash vẫn công bố bên ngoài. Mission/closure thực tế chưa được cấp là phần điều phối phải xử, không phải kết quả có thể tự suy từ sandbox.

ĐỘ TIN: cao về mâu thuẫn văn bản và phạm vi băm; authority GitHub ngoài prompt KHÔNG ĐO ĐƯỢC.

### bo-quet-nghiem-thu-thieu-mien [P2] Bộ lọc mới vẫn xấp xỉ miền schema/ref
VỊ TRÍ: A9 :212–225; Phụ lục A :303–304 và :319–323.

VẤN ĐỀ: all(isinstance(x,str)) nhận phần tử rỗng/trắng mà schema thay_the_cho trả None; bia mộ trắng cũng bị sản phẩm bác nhưng scanner sạch. Bộ lọc endswith('/HEAD') bỏ cả ref thường topic/HEAD. Cả hai là dùng đại diện gần đúng thay đúng miền đã khai; self-test cũ chỉ chạm vài đại diện âm, nên không kiểm được phần bù mới. Runtime cũng bỏ suffix HEAD, vì vậy đây là chênh miền A9 đã hứa, không khai scanner hẹp hơn runtime ở ca đó.

HINT: có — nhóm `bo-quet-nghiem-thu-thieu-mien`: dẫn xuất đầy đủ các điều kiện schema; chỉ loại symbolic HEAD và công bố miền nghiệm thu bảo thủ bao trùm runtime; thêm đối chứng list rỗng hợp lệ. Không sửa lease hay mở scope bộ liệt kê ref runtime.

ĐÃ THỬ: `hunts.py schema`, `hunts.py ref_domain`: mọi ca âm mới trả lỗi=[] trong nguyên bản; HINT áp trên bản sao rồi `check_hint.py` cho các ca ấy rc=1, good/empty_list/valid rc=0. Kiểm đóng lớp cần chạy cả ca âm và dương qua scanner executor. Rủi ro vá: không biến kiểm schema thành bắt mọi bia mộ lịch sử phải tìm được đối tác trong cùng ref; không gộp retired thành người giữ live.

ĐỘ TIN: cao; snapshot thật hiện không có những lease xấu này.

### bo-quet-chung-cu-khong-neo-anh [P2] Báo cáo không gắn với ảnh ref đã lấy
VỊ TRÍ: Phụ lục A :303–324, A9 :219–222, §8 :244–247.

VẤN ĐỀ: for-each-ref đã trả OID, nhưng công cụ vứt OID rồi ls-tree bằng tên ref. Nếu ref thay giữa hai lần đọc thì dữ liệu kiểm không phải ảnh đã liệt kê. Kết quả chỉ trả các số tổng và danh sách lỗi, không trả ref/OID, kiểu/mẫu số mapping hay nhóm live/retired như A9 yêu cầu. Cùng blob ở hai miền cho (1,1,2,[]) và mất nhãn lịch sử; “560 str” không tự dẫn xuất từ tuple ấy dù phép đo độc lập của review xác nhận nó đúng trên snapshot.

HINT: có — nhóm `bo-quet-chung-cu-khong-neo-anh`: giữ OID/map, đọc bằng OID, giữ cặp/path/ref và mẫu số theo đơn vị công bố, xuất nhóm lịch sử riêng. Cách chữa là làm chứng cứ của lần quét gắn với chính đầu vào đã đọc; không phải sửa ID sản phẩm.

ĐÃ THỬ: `hunts.py evidence`: ref liệt kê ở commit có int, bị chuyển sang commit chuỗi trước ls-tree, kết quả sạch. `check_hint.py`: bản gợi ý đọc OID cũ và báo int; cùng blob ở hai miền ra một blob/hai cặp/hai mapping str, từng miền một cặp. Kiểm đóng lớp phải đối chiếu nguồn ref đầy đủ; map của một cache tự nó chưa chứng minh đầy đủ nguồn live.

Rủi ro vá: không dùng “khớp OID đã chụp” để khai trạng thái máy chủ tại thời điểm land; trước công bố vẫn phải có lần đo mới. Không coi số blob và số cặp luôn bằng nhau.

ĐỘ TIN: cao cho phản chứng; không đo có race tại phiên soạn hay nguồn thật.

### bo-quet-khong-co-cua-chay [P2] Chạy nguyên khối tham chiếu không thực hiện phép đo
VỊ TRÍ: §8 :244; Phụ lục A :295–342.

VẤN ĐỀ: script được công bố chỉ định nghĩa git()/quet(), không gọi hàm, không in kết quả, không ánh xạ errors sang rc. Chạy nguyên khối trên kho có int, ref hỏng hay đường repo không tồn tại đều rc=0/stdout rỗng; bảng self-test rc không tái lập được bằng lệnh đã mô tả. Đây là lỗi cửa vào/phân loại tín hiệu, độc lập với bộ lọc có đúng hay không. Không kết luận người soạn chưa dùng wrapper ngoài tệp; chính sự thiếu wrapper làm công thức không tự đủ.

HINT: có — nhóm `bo-quet-khong-co-cua-chay`: thêm main, args, JSON dương/UTC, rc theo lỗi; ghim LC_ALL=C cho phép bắt cảnh báo Git và chỉ rõ lệnh chạy. Đặt bảng rc cũ dưới nhãn lịch sử chưa tái lập, bắt đo qua entry point trước công bố revision mới.

ĐÃ THỬ: `hunts.py entry`: good/int_yml/broken_ref/missing_repo đều 0/rỗng. `check_hint.py` dùng subprocess trên khối trích từ bản đã áp: good 0 + JSON, int 1 + JSON lỗi, broken/missing repo khác 0. Kiểm đóng lớp cần đòi cả schema/counts báo cáo, không tin rc đơn lẻ.

Rủi ro vá: mã báo cáo mới là công cụ soạn spec; executor vẫn chỉ thêm helper/selftest trong test file, không thêm script sản phẩm ngoài write set. Không nhận traceback không liên quan làm một phép giết mutant có ý nghĩa.

ĐỘ TIN: cao về artifact công bố; wrapper lịch sử KHÔNG ĐO ĐƯỢC.

### objective-dong-nhat-cu-phap-voi-danh-tinh [P3] Objective hứa phân biệt cả cú pháp YAML
VỊ TRÍ: header :12, đối chiếu Q1 :93–95.

VẤN ĐỀ: hai cách viết YAML khác nhau vẫn có thể cho cùng str hợp lệ; Q1 cố ý dùng giá trị sau safe_load nên không thể hứa mọi cách viết khác nhau cho dấu khác nhau. Đây là chính xác hóa lời khai mới; phần Q1 cụ thể đủ rõ, không đòi thay hành vi thi hành.

HINT: có — nhóm `objective-dong-nhat-cu-phap-voi-danh-tinh`: giới hạn lời hứa ở va chạm do ép non-str, ghi same string là same ID.

ĐÃ THỬ: `hunts.py objective`: các cặp tagged/quoted/escaped đã chọn cùng str/regex=True/dấu giống nhau. Ca khóa là ví dụ/documentation; không đòi xây bộ phân biệt cú pháp hay chặn khóa YAML lặp. Rủi ro vá: không mở rộng sang chuẩn hóa Unicode hoặc thay loader ngoài Q1.

ĐỘ TIN: cao.

## DRY-RUN HINT.patch

Nhãn bắt buộc: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. HINT chỉ nhắm `ops/specs/lease-id-ep-kieu-yaml-r2.md`; r1 bất khả xâm phạm. Điều phối dùng gợi ý để soạn revision kế tiếp, không sửa đè r2 đã công bố; không có patch mã sản phẩm.

Lệnh trên bản sao được tạo đúng mẫu yêu cầu:
```sh
hint_tmp=$(mktemp -d -p "$R")
cp -a "$R/cay-kho" "$hint_tmp/cay"
patch -d "$hint_tmp/cay" -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output đầy đủ của bản HINT cuối (`goi/hint-dry-run.log`):
```text
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: hop-dong-dong-bang-thieu-neo
|--- ops/specs/lease-id-ep-kieu-yaml-r2.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r2.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r2.md
Using Plan A...
Hunk #1 succeeded at 1.
Hunk #2 succeeded at 10.
Hunk #3 succeeded at 22.
Hunk #4 succeeded at 36.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|
|# lop: bo-quet-nghiem-thu-thieu-mien
|--- ops/specs/lease-id-ep-kieu-yaml-r2.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r2.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r2.md
Using Plan A...
Hunk #1 succeeded at 212.
Hunk #2 succeeded at 227.
Hunk #3 succeeded at 310.
Hunk #4 succeeded at 329.
Hunk #5 succeeded at 332.
Hunk #6 succeeded at 351.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|
|# lop: bo-quet-chung-cu-khong-neo-anh
|--- ops/specs/lease-id-ep-kieu-yaml-r2.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r2.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r2.md
Using Plan A...
Hunk #1 succeeded at 292.
Hunk #2 succeeded at 312.
Hunk #3 succeeded at 315.
Hunk #4 succeeded at 319.
Hunk #5 succeeded at 324.
Hunk #6 succeeded at 326.
Hunk #7 succeeded at 328.
Hunk #8 succeeded at 337.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|
|# lop: bo-quet-khong-co-cua-chay
|--- ops/specs/lease-id-ep-kieu-yaml-r2.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r2.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r2.md
Using Plan A...
Hunk #1 succeeded at 295.
Hunk #2 succeeded at 299.
Hunk #3 succeeded at 327.
Hunk #4 succeeded at 337.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|
|# lop: objective-dong-nhat-cu-phap-voi-danh-tinh
|--- ops/specs/lease-id-ep-kieu-yaml-r2.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r2.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r2.md
Using Plan A...
Hunk #1 succeeded at 12.
done
dry_run_rc=0
```
Áp thật tiếp trên cùng bản sao và cmp với nội dung dự kiến:
```text
apply_rc=0
expected_cmp_rc=0
```
Đã phát hiện và sửa lỗi dụng cụ sinh HINT: insertion hunk thiếu neo ban đầu được patch đặt sai vị trí dù rc=0. Bản cuối neo vào dòng nguyên văn duy nhất; apply thật + cmp byte-match đã qua. Không dùng riêng dry-run xanh làm bằng chứng.

Trích scanner từ bản đã áp và chạy `PYTHONDONTWRITEBYTECODE=1 python goi/check_hint.py`:
```text
good rc= 0 errors= [] positive_report= True
int_yml rc= 1 errors= [['ops/leases/a.yml', 'lease_id=1000']] positive_report= True
missing rc= 1 errors= [['ops/leases/a.yaml', 'thieu_lease_id']] positive_report= True
list rc= 1 errors= [['ops/leases/a.yaml', 'khong_phai_anh_xa']] positive_report= True
parse rc= 1 errors= [['ops/leases/a.yaml', 'parse']] positive_report= True
pointer_list rc= 1 errors= [['ops/leases/a.yaml', 'da_bi_thay_the']] positive_report= True
local_bool rc= 1 errors= [['ops/leases/a.yaml', 'lease_id=True']] positive_report= True
broken_ref rc= 1 errors= git/input error positive_report= False
empty_item rc= 1 errors= [['ops/leases/test.yaml', 'thay_the_cho']] positive_report= True
space_item rc= 1 errors= [['ops/leases/test.yaml', 'thay_the_cho']] positive_report= True
space_tombstone rc= 1 errors= [['ops/leases/test.yaml', 'da_bi_thay_the']] positive_report= True
empty_list rc= 0 errors= [] positive_report= True
valid rc= 0 errors= [] positive_report= True
ordinary_HEAD rc= 1 errors= [['ops/leases/good.yaml', 'lease_id=True']] positive_report= True
missing_repo rc= 1 errors= git/input error positive_report= False
same_blob= {'ref_count': 1, 'blob_count': 1, 'pair_count': 2, 'mapping_count_pairs': 2, 'id_count_pairs': 2, 'type_counts_pairs': {'str': 2}, 'areas': {'ops/leases': {'pairs': 1, 'blobs': 1}, 'ops/leases_retired': {'pairs': 1, 'blobs': 1}}, 'errors': []}
moving_ref uses_enumerated_oid= True errors= [('ops/leases/test.yaml', 'lease_id=1000')]
snapshot= {'ref_count': 506, 'blob_count': 560, 'pair_count': 560, 'mapping_count_pairs': 560, 'id_count_pairs': 560, 'type_counts_pairs': {'str': 560}, 'areas': {'ops/leases': {'pairs': 560, 'blobs': 560}, 'ops/leases_retired': {'pairs': 0, 'blobs': 0}}, 'errors': []}
hint_scanner_checks=PASS
```
Các kết quả này kiểm gợi ý trên cây riêng; chúng không tự đóng các finding của bytes r2 đang review. HINT không có quyền điền mission/closure chưa được cấp.

## TOÀN VẸN VÀ GIỚI HẠN CUỐI

Đã giữ cùng reviewed SHA/tree, không có ứng viên Python của PR. Không đo Windows, GitHub live, closure/mission authority hoặc acceptance tương lai #677; Ruff module không có nên lint F chưa chạy. Suite nền không thay được acceptance ứng viên. Tất cả bytecode/cache/tempfile từ script review nằm ngoài checkout qua cờ/env đã nêu.

Snapshot trước/sau băm mọi tệp regular và Git metadata trong cay-kho và kho.git. Đây là bằng chứng không có delta quan sát được ở hai mốc, không phải audit mọi syscall trong cả phiên. Sandbox cho phép ghi workspace; checkout read-only là ràng buộc công việc đã giữ, không tự khai có mount read-only.

Kiểm cuối: `PYTHONDONTWRITEBYTECODE=1 python goi/verify.py`:
```text
verdict=changes_requested
classes= 5 severity= {'P1': 1, 'P2': 3, 'P3': 1} hint_groups= 5
hunt_count= 9
source_files= 3004 source_delta= 0
HEAD/tree= ['aecdccd32b748fd5694231976193ade2e34ea10d', 'f1e1128de9ca8233e768edbd30cdd456491682c7']
r1_sha256= 578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c
spec_sha256= 1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715
dry_run_rc=0 apply_rc=0 expected_cmp_rc=0
suite_summary= lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0
```

Băm hai hiện vật bàn giao được ghi trong `goi/artifact-hashes.txt` bằng `sha256sum goi/VERDICT.md goi/HINT.patch`. Không nhúng băm tự tham chiếu của verdict vào chính verdict.
