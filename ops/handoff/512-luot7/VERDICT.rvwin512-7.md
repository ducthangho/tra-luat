verdict: changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: 13a2af8ca8cd1d4571590f0e46c751eb0d7e6964790a0d53cdd5e0058a591f84
  ops/chay_lease_publish_test.sh: 87c760294763c71a67cfaee50a440e62b31c439beb0abbfcb5e34076d32be693
model_tu_khai: GPT-6 / Codex; khác họ Claude theo lời khai tác giả; không xác minh backend độc lập
review_round: 7
so_p1: 1
so_p2: 0
so_p3: 0
so_the_hien: 38
hint_sha256:
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0

**changes_requested: còn một lớp F6 (công cụ/hồ sơ bằng chứng).** F2 và F7 đã vá thật theo đối chứng đột biến hai head. F6 còn cấp tín dụng giả cho ngoại lệ vô can `StopIteration`. Lời đính chính +1101/−27 và nguyên nhân của nó đều đúng.

**Cách đếm:** giữ nguyên lớp F6 của verdict vòng 6, không tách hồ sơ số thành lớp khác để nhân số P. 38 thể hiện mở = F6.5 (1 lỗ công cụ) + F6.6 (1 lời khai giao log không khớp gói) + F6.N01–N36 (36 số/đại lượng bảng EVIDENCE bỏ sót, tính riêng theo yêu cầu người dùng). Những số đo lại đúng vẫn được điểm danh và tính là thiếu bao phủ bảng; **38 không có nghĩa 38 lỗi thực thi**, và một lớp mang mức cao nhất P1 không có nghĩa mọi thể hiện trong nó đều P1. Không đếm các thể hiện cũ đã đóng.

Đã ghi tăng dần ngay khi phát hiện; bản nhật ký trước khi sắp lại báo cáo nằm ở `review-logs/VERDICT-journal.md`. Không nộp HINT.patch: việc còn yêu cầu sửa thuộc công cụ/hồ sơ ngoài write set. Không quyết định merge, không approve thay chủ kho, không cấp hay nâng trần.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp | Trạng thái canonical | Bằng chứng và giới hạn |
|---|---|---|
| F1 thu hồi cây | ĐÃ VÁ THẬT | Control t154 1/1; mutant giết PID, bỏ session, bỏ guard nhóm đều chết đúng chốt. Không thấy thoái lui trên POSIX trong phạm vi đo; chưa chứng nhận Windows. |
| F2 bằng chứng sống | ĐÃ VÁ THẬT | N10 sống ở t160 cũ, chết ở t160 hiện tại vì thiếu bốn tee. Control t157/t158 xanh; mutant trì hoãn tee, bỏ nhãn, bỏ flush đều chết đúng chốt. |
| F3 selector rỗng/không khớp | ĐÃ VÁ THẬT | Control t155 1/1; bỏ guard bị bắt vì selector không khớp trả 0 thay vì 3. Không thấy thoái lui. |
| F4 ngân sách tổng | ĐÃ VÁ THẬT | Control t156 1/1; các mutant cấp lại hạn, trả dở dang, hạ hạn ngoài, bỏ hạn chẩn đoán đều chết đúng chốt. N12 bị chặn tại consumer; không đếm lặp ở F4. |
| F5 tắt đệm con | ĐÃ VÁ THẬT | Control t158 1/1; M14 chết ở phép đo môi trường thực của hai vế. Không thấy thoái lui. |
| F6 công cụ/hồ sơ bằng chứng | VÁ HỜ | Regex đóng Exception/Error trần; control mới StopIteration vẫn được cấp GIET THAT. Còn thiếu log đã khai và bảng số chưa phủ các lời khai định lượng. |
| F7 classifier/consumer/phản chứng | ĐÃ VÁ THẬT | N01/N02/N12/N17/N18 cùng sống ở 353eae1, cùng chết đúng chốt ở 36f68c7; control t160 xanh. |

| Từng thể hiện cũ bắt buộc | Kết quả độc lập |
|---|---|
| F2.3 | Đã đóng. N10 thay danh sách luồng tee tại t125 bằng []: t160 hiện tại rc=1 với `consumer t125 phải nối đủ bốn tệp vào đúng tee: []`. Không tuyên t158 tự bắt N10. |
| F6.4 | Đã đóng thể hiện cũ. Control Exception trần: bản regex cũ cấp GIET THAT; bản mới trả TIN DUNG GIA. Error trần cũng được đóng. Cả lớp vẫn VÁ HỜ vì F6.5. |
| F7.2a | Đã đóng. N01 đảo đối số và N02 đảo biến nhận kết quả đều bị chốt tuple đúng nhãn không-actor/có-actor bắt. |
| F7.2b | Đã đóng. N17 bỏ so mẫu số chết ở chẩn đoán vế 1/2; N18 cố định mẫu số chết ở chốt tuple parser. |
| F7.2c | Đã đóng. N12 tái sinh retry từng tên ca lệch, cả hai môi trường, qua Popen/PIPE và timeout cấp lại, chết ở chốt cấm mở thêm run/Popen. |

Không có mã catalogue N của reviewer vòng 6 trong gói, nên đây là **tái dựng theo mô tả**, không tuyên byte giống bản cũ. Đã dùng cùng mỗi phép biến đổi trên cả hai nguồn Git: sáu mutant đều sống ở 353eae1 và chết ở 36f68c7, giúp xác nhận chúng nhắm đúng lỗ của lượt trước. Danh sách N01/N02/N10/N12/N17/N18 có **sáu** ID; không bỏ một ID để khớp chữ “năm” trong prompt. N09 không chạy lại, không tính finding.

## BẢNG ĐO

| Phép đo | Kết quả | Hiện vật |
|---|---|---|
| Neo Git | HEAD/base/merge-base đúng SHA đầu báo cáo; origin/master 2135 commit, is-shallow=false, core.abbrev=7 | metadata.json; final-hygiene.json trong review-logs |
| Diff được giao | Byte của diff.patch bằng git diff bb7013c 36f68c7 | final-hygiene.json |
| SPEC/HINT cũ | SHA256 đúng mỏ neo người dùng cung cấp | Băm trực tiếp; HINT được áp thử như hàng dưới |
| Numstat hiện tại | Hai tệp; Python +1095/−27, shell +6/−0; tổng +1101/−27 | metadata.json |
| Lời đính chính: số hạng | Trước HINT +1076 Python và +6 shell; sau HINT +1095 và +6. Delta thêm 19 | metadata.json |
| Lời đính chính: nguyên nhân | Đúng 13/13 dòng HINT xoá vốn là dòng thêm của PR. Patch +32/−13 ⇒ cột thêm tăng 19, không tăng 32 | metadata.json có từng số dòng parent |
| Merge 1db6af2 | Không đổi byte hai đường write set | git diff 1db6af2^ 1db6af2 trên hai đường rỗng |
| Áp nguyên HINT lượt 6 | Tại parent 1db6af2: patch -p0 --dry-run --fuzz=0 rc=0; áp thật bản sao rc=0; byte bằng HEAD | review-tmp/hint-verify; metadata.json |
| Wrapper độc lập, cwd=cay-kho | **KHÔNG ĐO ĐƯỢC** full suite. rc=4 tại installer, curl không kết nối được; không có actionlint/archive trong sandbox | suite-exact-cwd.log và .rc |
| Điều kiện môi trường | Linux; Python 3.11.15; shellcheck 0.9.0 có; actionlint chưa cài được | Lệnh version trực tiếp và log installer |
| Log suite tác giả | CHA/A/B đều có 155 tên đúng thứ tự với mã HEAD, không đỏ, mỗi vế 155/155; neo 1055/1060/1156 khớp | metadata.json đối chiếu do-cua-tac-gia/suite-36f68c7-linux.log |
| Thời gian CHA trong log tác giả | t125=55.445 s, t158=3.381 s, t160=0.066 s, đúng lời khai | Log tác giả dòng 1061/1146/1148 |
| Control không đột biến | t153/t154/t155/t156/t157/t158/t160: mỗi ca rc=0, 1/1, đã chạy=1, bỏ qua=0 | controls.json và control-t*.log |
| Catalogue tác giả | 16/16 chết đúng chốt; rc=0; đã kiểm nguyên log từng ca, không ngoại lệ vô can | catalogue.log; catalogue-full/; catalogue-full-audit.json |
| Tự kiểm bản mới | 4/4 đúng phân hạng; rc=0 | tukiem-moi.log và .rc |
| Tự kiểm bản cũ | 2/4 đúng phân hạng; rc=1; Exception/Error trần nhận tín dụng giả | tukiem-cu.log và .rc |
| Hai bộ đo | Khác đúng một dòng regex | metadata.json chứa diff |
| Control F6 mở rộng | StopIteration vô can vẫn GIET THAT; tự kiểm 3/4, rc=1 | tukiem-StopIteration.log và .rc |
| Sáu mutant lượt trước | SỐNG 6/6 ở 353eae1; CHẾT đúng chốt 6/6 ở 36f68c7 | comparative-mutants.json, log từng head-mutant |
| ci_dang_ky_test.py | rc=0; ĐĂNG KÝ 21/21; PHẢN CHỨNG 51/51; TỔNG ĐẠT | ci-dang-ky.log và .rc |
| review_rounds_used trong .py được phép đọc | 0 tệp, không suy có cổng canh trần vòng | counter-files.txt; loại thư mục skills bị cấm |
| Khối S2 tại 2d0ee53 | Object nay có; YAML khai ai_nang=ducthangho, 300→1500, đo tại 353eae1; không khai A5 đạt | lease-504-2d0ee53.yaml, sha256 0b77ab0cf7184fdaf7634ec7c3c8e4ff67914d2db8ca0768bd50d4a41328fb66 |
| A5 đóng băng | **KHÔNG ĐẠT** ngưỡng 300 vì 1101>300. 1101≤1500 chỉ khớp trần override được khai; không đổi đặc tả | SPEC.md và YAML S2 |

Các đường hiện vật ngắn trong bảng nằm dưới `review-logs/`. Bằng chứng dương của **lượt reviewer full wrapper chưa có**: không dùng rc=0 của script bọc ghi log, log suite tác giả, hay các control 1/1 để thay ba tổng kết CHA/A/B của lượt chạy độc lập. rc thực của wrapper được ghi riêng và là 4. Không gọi thiếu công cụ là hồi quy test.

## Findings theo lớp

### F6 — công cụ/hồ sơ bằng chứng; một lớp P1, 38 thể hiện mở

**F6.5 — P1, phân hạng ngoại lệ vô can còn cấp tín dụng giả.** `do-cua-tac-gia/dotbien512.py:179` chỉ loại tên có hậu tố Error/Exception. Tôi đổi đúng lệnh `raise Exception` của control có sẵn thành `raise StopIteration`, giữ thông điệp, ca đích, đáp án mong đợi và đường chạy catalogue. Bộ đo mới in `GIET THAT`, lý do `StopIteration: CONTROL vo can, khong lien quan A/B`; tự kiểm còn 3/4, rc=1.

Không có `except` chuyển ngoại lệ sang AssertionError, không giả mạo stdout, không cần nội dung đường dẫn đặc biệt. `main()` giữ nguyên kiểu ngoại lệ mà công cụ vẫn nhận sai. Vì vậy câu trong hồ sơ F6 rằng hướng sai còn lại chỉ là fail-close không đủ rộng. `4/4` kiểm đúng bốn control được chọn, không chứng minh đã loại mọi ngoại lệ vô can. Hiện vật tái lập: `review-logs/extra_f6.py`, `dotbien512_StopIteration.py`, `tukiem-StopIteration.log`.

Cần sửa bộ đo/hồ sơ riêng để phân biệt tín hiệu chốt với ngoại lệ không liên quan, thêm control không có hậu tố Error/Exception và giữ control dương. Không chỉ bổ sung danh sách một tên ngoại lệ nữa rồi tuyên đóng lớp. Nợ giả mạo tín hiệu đã khai vẫn là nợ; tôi không tự viết mã giả mạo để đo nó. Công cụ ngoài write set, không yêu cầu đưa đường thứ ba vào PR.

**F6.6 — lời khai giao cả hai log không khớp gói.** EVIDENCE nói log của cả lượt thiếu shellcheck (153/155) và lượt đủ công cụ (155/155) đều ở `do-cua-tac-gia/`. Bảy tệp được giao chỉ có một log suite, chứa ba tổng kết 155/155; không có log lượt 153/155. Không suy lượt đầu không từng xảy ra. Cần giao hiện vật còn thiếu hoặc đính chính rằng nó chưa nằm trong gói. Đây là thiếu hồ sơ, không hồi quy do shellcheck.

**F6.N01–F6.N36 — mỗi số/đại lượng bị bảng EVIDENCE bỏ sót được điểm danh riêng theo yêu cầu.** Đếm theo lời khai định lượng của packet, tách số hạng khi câu có quan hệ; không biến số ID commit/issue, số dòng dẫn chứng hoặc literal fixture thành lỗi thực thi. Các hàng ghi CÓ đã đo lại khớp vẫn là finding thiếu bao phủ bảng theo quy tắc người dùng. KHÔNG ĐO ĐƯỢC mốc lịch sử không đồng nghĩa mốc sai. Các mục ngoài write set chỉ cần bổ sung hồ sơ; không yêu cầu sửa lease/product/workflow trong PR.

| ID | Vị trí | Số/đại lượng bảng bỏ sót | Đo từng số hạng / giới hạn |
|---|---|---|---|
| F6.N01 | `ops/lease_publish_test.py:34` | AL_HAN_GIAY=180 s | CÓ: đọc hằng thật 180 |
| F6.N02 | `ops/lease_publish_test.py:35` | SC_HAN_TONG_GIAY=180 s | CÓ: đọc hằng thật 180 |
| F6.N03 | `ops/lease_publish_test.py:36` | CD_HAN_TONG_GIAY=120 s | CÓ: đọc hằng thật 120 |
| F6.N04 | `ops/lease_publish_test.py:38` | 2 thân run trong workflow | CÓ: YAML hiện tại có 2 thân; chỉ đọc dữ liệu workflow ngoài write set |
| F6.N05 | `ops/lease_publish_test.py:41` | T137_TRAN_GIAY=480 s | CÓ: giá trị chạy 480 = 180+180+120 |
| F6.N06 | `ops/lease_publish_test.py:53` | AB_SUITE_DO_DUOC_GIAY=350 s | CÓ: giá trị chạy 350; đây là cấu hình, cơ sở số đo Windows chưa có log |
| F6.N07 | `ops/lease_publish_test.py:53` | t125 Windows M4 lượt 4 = 344.438 s | KHÔNG ĐO ĐƯỢC: không có log Windows nguồn trong gói |
| F6.N08 | `ops/lease_publish_test.py:54` | AB_DU_PHONG_GIAY=120 s | CÓ: giá trị chạy 120 |
| F6.N09 | `ops/lease_publish_test.py:58` | AB_HAN_GIAY=950 s | CÓ: giá trị chạy 950 = 180+180+120+350+120; chưa chứng nhận hoàn tất Windows trong 900 s |
| F6.N10 | `ops/lease_publish_test.py:60` | AB_TRAN_CUNG_GIAY=1500 s | CÓ: giá trị chạy 1500; trần thời gian khác trần dòng thêm S2 |
| F6.N11 | `ops/lease_publish_test.py:4217` | M4 lượt 1: t125 chưa ra sau 1540 s | KHÔNG ĐO ĐƯỢC: thiếu log nguồn |
| F6.N12 | `ops/lease_publish_test.py:4231` | Windows lượt 4 tổng 526.866 s | KHÔNG ĐO ĐƯỢC: thiếu log nguồn; không suy số hạng từ hiệu |
| F6.N13 | `ops/lease_publish_test.py:4231` | Windows lượt 4: 15 ca ĐỎ | KHÔNG ĐO ĐƯỢC: thiếu log nguồn; không suy số hạng từ hiệu |
| F6.N14 | `ops/lease_publish_test.py:4231` | Windows lượt 4: 7 ca BỎ QUA | KHÔNG ĐO ĐƯỢC: thiếu log nguồn; không suy số hạng từ hiệu |
| F6.N15 | `ops/lease_publish_test.py:4231` | Windows lượt 4: 14 ca có chữ ký PATH | KHÔNG ĐO ĐƯỢC: thiếu log nguồn; không suy số hạng từ hiệu |
| F6.N16 | `ops/lease_publish_test.py:4232` | t150 chỉ giữ 200 ký tự cuối stderr | CÓ: t150 hiện tại dùng e[-200:] khi báo lỗi; chưa tái lập stderr Windows cũ |
| F6.N17 | `ops/lease_publish_test.py:4232` | Ubuntu lượt 4 = 114.528 s | KHÔNG ĐO ĐƯỢC: thiếu log của đúng lượt |
| F6.N18 | `ops/lease_publish_test.py:4232` | Ubuntu A2 lượt 1 = 141.023 s | KHÔNG ĐO ĐƯỢC: thiếu log của đúng lượt |
| F6.N19 | `ops/lease_publish_test.py:4233` | M4 lượt 3 t139 vào 17:24:51.969Z | KHÔNG ĐO ĐƯỢC mốc nguồn; chỉ có docstring tự khai |
| F6.N20 | `ops/lease_publish_test.py:4233` | M4 lượt 3 log huỷ 17:25:47.047Z | KHÔNG ĐO ĐƯỢC mốc nguồn; chỉ có docstring tự khai |
| F6.N21 | `ops/lease_publish_test.py:4233` | khoảng 55.077 s giữa hai mốc trên | CÓ phép trừ từ số hạng tự khai: 55.078 s; lệch 0.001 s. Có chữ khoảng nên không nâng sai số 1 ms thành lỗi chức năng |
| F6.N22 | `ops/lease_publish_test.py:4234` | f1b0b4f dòng thêm +102 | CÓ: Git so b98531e = +102 |
| F6.N23 | `ops/lease_publish_test.py:4234` | f1b0b4f dòng xoá −15 | CÓ: Git so b98531e = −15 |
| F6.N24 | `ops/lease_publish_test.py:4234` | 570209c dòng thêm +142 | CÓ: Git so b98531e = +142 |
| F6.N25 | `ops/lease_publish_test.py:4234` | 570209c dòng xoá −16 | CÓ: Git so b98531e = −16 |
| F6.N26 | `ops/lease_publish_test.py:4234` | dff28f6 dòng thêm +157 | CÓ: Git so b98531e = +157 |
| F6.N27 | `ops/lease_publish_test.py:4234` | dff28f6 dòng xoá −17 | CÓ: Git so b98531e = −17 |
| F6.N28 | `ops/lease_publish_test.py:4235` | +166 là tổng delta cộng cơ học | CÓ: 67+35+40+24=166; diff cuối thực +157, đã phân biệt đúng trong docstring |
| F6.N29 | `ops/lease_publish_test.py:4235` | −26 là tổng delta cộng cơ học | CÓ: 6+9+1+10=26; diff cuối thực −17, đã phân biệt đúng trong docstring |
| F6.N30 | `ops/lease_publish_test.py:5841` | M4 t153 = 0.250 s | KHÔNG ĐO ĐƯỢC: không có log Windows của mốc này |
| F6.N31 | `commit 36f68c7, subject` | 5 mutant sống ở vòng 6 | KHÔNG: chính body liệt kê N01,N02,N10,N12,N17,N18 = 6; đối chứng hai head cũng đủ sáu. Sai số của commit, không tính lỗi câu chữ của prompt |
| F6.N32 | `commit 36f68c7, numstat` | dư 386 so trần 1500 dòng | KHÔNG với số đính chính: 1500−1101=399; 386 chỉ đúng khi dùng 1114 đã thừa nhận sai. EVIDENCE đính chính tổng, chưa điểm danh số dư này |
| F6.N33 | `2d0ee53:ops/leases/windows-lease-suite-exec-1-claude-20260911.yaml:134` | 418 dòng dư tại head 353eae1 | CÓ: 1500−1082=418; đây là head cũ, không trộn với 399 tại head review |
| F6.N34 | `2d0ee53:ops/leases/windows-lease-suite-exec-1-claude-20260911.yaml:134` | 195 dòng thêm trước mốc vượt S2 | CÓ: diff b98531e..e0b5bf0 = 189+6=195 |
| F6.N35 | `2d0ee53:ops/leases/windows-lease-suite-exec-1-claude-20260911.yaml:134` | 746 dòng thêm tại mốc vượt S2 | CÓ: diff b98531e..8ffd062 = 740+6=746 |
| F6.N36 | `2d0ee53:ops/leases/windows-lease-suite-exec-1-claude-20260911.yaml:134` | mốc 8ffd062 là bốn vòng review trước lúc nâng | KHÔNG ĐO ĐƯỢC số vòng từ lịch sử commit; thiếu chuỗi biên nhận có định nghĩa vòng tương ứng |

N31 và N32 là hai lời khai số còn sai trong commit không được phần đính chính điểm danh đầy đủ: **6 mutant**, và **399 dòng dư** tại head hiện tại. N33 giữ đúng **418 dòng dư của head cũ**; không kéo nó sang head mới. N21 chỉ lệch 1 ms so phép trừ hai mốc tự khai và có chữ “khoảng”, nên không nâng sai số ấy thành lỗi chức năng.

## Mutant đã chạy

| Mutant tái dựng | t160 tại 353eae1 | t160 tại 36f68c7 | Lý do chết hiện tại |
|---|---|---|---|
| N01 đảo đối số classifier | SỐNG rc=0 | CHẾT rc=1 | Tuple phải gắn đúng nhãn A/B |
| N02 đảo biến kết quả A/B | SỐNG rc=0 | CHẾT rc=1 | Tuple phải gắn đúng nhãn A/B |
| N10 bỏ danh sách tee | SỐNG rc=0 | CHẾT rc=1 | Consumer thiếu bốn cặp tệp/nhãn tee |
| N12 retry Popen/PIPE khi lệch | SỐNG rc=0 | CHẾT rc=1 | Không được mở run/Popen ngoài hai vế A/B |
| N17 classifier bỏ mẫu số | SỐNG rc=0 | CHẾT rc=1 | Mất chẩn đoán vế 1/2 khi chỉ mẫu số lệch |
| N18 parser cố định mẫu số | SỐNG rc=0 | CHẾT rc=1 | Tuple parser khác tuple fixture được ghim |

Script `review-logs/compare_mutants.py` là phép đo chính cho sáu ID. `rebuild_mutants.py` là lượt sơ bộ: N12 ở đó chèn Popen vô điều kiện; đã thay bằng phép tái dựng retry có điều kiện và từng ca lệch để đối chứng đúng mô tả lượt 6. Không lấy lỗi runtime của một mutant sai hình dạng làm tín dụng.

| Catalogue tác giả, theo thứ tự | Ca đích | Kết quả kiểm log đầy đủ |
|---|---|---|
| giết chỉ PID | t154 | CHẾT: nhịp cháu 1→21 còn tăng |
| bỏ start_new_session | t154 | CHẾT: con không lãnh đạo nhóm riêng |
| bỏ guard selector | t155 | CHẾT: rc=0 thay vì 3 |
| AB_HAN_GIAY=420 | t156 | CHẾT: 420 nhỏ hơn 480+350 |
| tee chỉ in cuối | t157 | CHẾT: không thấy dòng trong 15 s |
| tee bỏ tiền tố | t157 | CHẾT: dòng không mang nhãn đầu dòng |
| cấp lại hạn tối thiểu | t156 | CHẾT: vượt ngân sách 0.6 s mà không dừng |
| M09 bỏ flush | t157 | CHẾT: không thấy dòng trong 15 s |
| M10 chỉ cấp lại khi cạn | t156 | CHẾT: không ném HetNganSachDay trước lệnh tiếp |
| M11 trả kết quả dở dang | t156 | CHẾT: thiếu tín hiệu hết ngân sách |
| M13 bỏ guard trưởng nhóm | t154 | CHẾT: chạm nhóm không được giết |
| M15 classifier trả KHỚP khi lệch | t160 | CHẾT: mất chẩn đoán đúng vế |
| M16 consumer bỏ classifier | t160 | CHẾT: classifier không nhận tuple |
| M17 consumer nhận CHƯA RÕ | t160 | CHẾT: mất chẩn đoán đúng vế |
| M14 bỏ PYTHONUNBUFFERED | t158 | CHẾT: môi trường thực hai vế thiếu biến |
| bỏ hạn chẩn đoán khỏi T137 | t156 | CHẾT: 360 khác 180+180+120 |

Đã tự chạy `--tu-kiem` cả hai bản trước khi dùng kết quả 16/16, rồi ghi lại nguyên stdout/stderr của 16 mutant để kiểm chốt và loại AttributeError vô can. Bản ghi đầy đủ ở `review-logs/catalogue-full/`. Việc 16 mutant này chết đúng là CÓ; việc bộ đo đã miễn nhiễm tín dụng giả là KHÔNG (F6.5). Không đánh đồng hai mệnh đề.

## chua_do_duoc

| Câu hỏi | Trạng thái | Giới hạn cụ thể |
|---|---|---|
| Reviewer có ba tổng kết CHA/A/B đầy đủ từ wrapper trên HEAD? | KHÔNG ĐO ĐƯỢC | Installer rc=4; thiếu actionlint và gói offline; đã yêu cầu vị trí gói trong sandbox, chưa nhận được. |
| Log tác giả có ba tổng kết dương 155/155? | có | Đã kiểm cả tên/thứ tự và 0 đỏ; chỉ chứng nhận nội dung hiện vật được giao. |
| Shellcheck có trong môi trường reviewer? | có | 0.9.0; không nhầm lỗi thiếu actionlint với hai cổng thiếu shellcheck t137/t159. |
| Các control và sáu mutant cũ có kết quả hoàn tất? | có | Bảng đo/log đã nêu; không thay full suite bằng selector. |
| Bộ đo mới đã loại được ngoại lệ vô can nói chung? | không | StopIteration được nhận GIET THAT, F6.5. |
| Hồi quy F1/F3/F4/F5 trong phạm vi POSIX đã đo? | không | Các control xanh và mutant chết đúng; không ngoại suy Windows. |
| Windows exact head, A2/A3/A4, ngưỡng 15 phút, chậm so Ubuntu ≤10%? | KHÔNG ĐO ĐƯỢC | Không chạy Windows/CI trong sandbox. Các thời gian Windows ở docstring thiếu log nguồn trong gói. |
| A5≤300? | không | +1101>300; không dùng override để đổi nhãn nghiệm thu đóng băng. |
| Hiện vật khối override 2d0ee53 tồn tại? | có | Nay đọc được YAML có băm; khác giới hạn snapshot vòng 6. |
| Nguồn chat/GitHub chứng thực độc lập khối override và metadata online? | KHÔNG ĐO ĐƯỢC | Không mạng; chỉ có lời thuật lại trong hiện vật. Không suy thiếu chứng thực là người dùng chưa cấp quyền. |
| doctrine-scan 7 tệp/0 chỗ và adr-song 47/47 tại HEAD? | KHÔNG ĐO ĐƯỢC | Không chạy phép đo đòi đọc CLAUDE.md/PROTOCOL/AGENTS/skills bị cấm. Không nhận lời khai làm sự thật. |
| Hai tập nguồn ref 356/356 trước clone, lệch đúng một tên nguồn/mirror? | KHÔNG ĐO ĐƯỢC | Không có hai danh sách nguồn trước clone trong gói. 398 ref checkout và 396 ref mirror hiện tại là namespace khác, không thay phép so nguồn; không dùng ls-remote thất bại để đếm. |
| Tần suất S8-bo-deadline, quan hệ nhân quả với GITHUB_ACTOR? | KHÔNG ĐO ĐƯỢC | Nợ khai ở ops/lease_publish.py ngoài write set; không suy control xanh đã loại trừ flake/actor. |
| Phần chống giả mạo tín hiệu của catalogue? | KHÔNG ĐO ĐƯỢC đầy đủ | Nợ tác giả đã khai; không tự soạn mã giả mạo. F6.5 đo ngoại lệ không có hậu tố, không phải phép giả mạo. |
| Backend mô hình và trạng thái GitHub trực tiếp? | KHÔNG ĐO ĐƯỢC | model_tu_khai là tự khai, không xác minh backend độc lập. |

Mọi mutation được viết trong `review-tmp/`, TMPDIR đặt trong sandbox và ngoài cây kho nguồn. Không đọc các tệp chỉ dẫn bị cấm để review; không soạn nội dung thoát cây hay mã tấn công. Các fixture con/cháu được chạy lại từ mã đã có. Không sửa `ops/lease_publish.py`, `.claude/dev/packet_loop.py` hoặc workflow: các phụ thuộc đọc/chạy phục vụ đo không mở write set.

Kiểm vệ sinh cuối: `git -C cay-kho status --porcelain` **RỖNG**; `git -C cay-kho log --oneline 36f68c7..HEAD` **RỖNG**. HEAD và băm cả hai tệp đúng khối đầu. Hiện vật: `review-logs/final-hygiene.json`. Không commit vào cây review, không để lại sửa đổi trong cay-kho.

XONG VERDICT
