verdict: changes_requested
reviewed_sha: b9f010b3e5ef521d2980f12a5a3d4317e1e78724
spec_sha256: c34d506626e40a07fbfef41ccd39e138f74a2df3116f1b53cea704aaf6068d43
Ket qua: 0 P0, 0 P1, 1 P2, 0 P3.

F01/F02 lượt 1 đã được vá trong phạm vi phép đo Linux của lượt trước. Còn F03 P2: chốt kiểu record mới chưa có đột biến được giết bằng TinHieuChotCa của chính ca đích, theo yêu cầu mục 4 prompt snapshot. HEAD hiện xử lý JSON list đúng; finding này là thiếu chứng cứ mutation đúng tín hiệu, không phải một cửa giả kênh mới. Chưa đạt ngưỡng chủ kho yêu cầu hết P1/P2/P3.

- Base: `c7174bfe03b3acd22cfa055b5fce176129d29542`.
- Reviewed tree: `84992282576bc674f1e521eba9ee2da8e9de4c3b`.
- SHA lượt 1: `b6fe8534d7498ebe88a1a222b49fbf36fe97cdf1`.
- SPEC-R1 SHA256: `48710a9b41cb744dd5b89df1d9f632fae51d08dcf22a0581088918832663598e`.
- Packet #1117, r2, generation 2, lease được prompt giao `wp1117-r2-g2-claude`, sensitive, lượt 2/10; không áp ADR-0060.
- Reviewer độc lập với executor Claude. `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, theo `run/510b309c/run.json`; run ID `510b309c99c64c0282ba5ae98acf56c4`. Exact served model/effort không đo được trong metadata runtime được cấp. Không suy identity từ actor vận chuyển verdict.
- Linux, Python 3.13.18, Git 2.43.0, Ruff 0.16.9. Sandbox workspace-write; checkout được đối xử chỉ đọc.

## Phạm vi, phương pháp và giới hạn

Đã đọc toàn bộ prompt snapshot, SPEC r2/R1, diff đầy đủ, sửa đổi từ lượt 1, verdict/hint lượt trước, finding nguồn F04 của #1079, hướng dẫn kho và các phần protocol liên quan review/gate. Đọc trực tiếp runner và đường gọi/bộ chấm/test liên quan. `diff.patch` khớp byte với `git diff BASE HEAD -- .claude`; full numstat có đúng hai tệp: launcher_test +232/-85, runner +84/-0, tổng +316/-85, trong trần +450.

Bản sao đo nằm ở `evidence/{base,head,previous,n0,hint}`, ngoài `cay-kho/`. Clone local, không mạng, `core.abbrev=7`. Hai clone A/B neo exact base/head; clone previous neo exact SHA lượt 1. Clone n0 chỉ thêm nguyên văn hai ca đã có ở HEAD vào base. Clone hint chỉ sửa test/bảng mutation. Không sửa checkout được review, push hay dùng credential thật; môi trường đo gỡ các biến credential/token thừa hưởng. Payload giả kênh, fake runner và ngoại lệ có hành vi đặc biệt đều lấy từ ca đã có, không soạn payload/lớp đặc biệt mới. Phép đột biến bổ sung F03 chỉ bỏ kiểm tra kiểu trong bản sao, tái dùng fixture JSON list có sẵn.

Full A/B được dựng/chạy trong **một lệnh** `python3 -B evidence/run_ab.py`; mỗi vế lần lượt chạy full launcher suite, full mutation và credential suite, hai vế cùng TMPDIR/env/công cụ. Command, cwd, UTC start/end, rc và thời lượng nằm ở `evidence/{base,head}-{suite,mutations,credentials}.json`; stdout/stderr nguyên văn trong `.log`. HEAD suite chạy 01:08:11–01:13:29 UTC, mutation 01:13:29–01:20:08 UTC ngày 02-11-2026.

`/tmp/.git` hiện diện. Sandbox chỉ cho ghi workspace và `/tmp`, nên không dựng được TMPDIR ngoài `/tmp` đúng điều kiện Linux A/B của SPEC; không xóa/che `.git` hoặc lách kiểm tổ tiên. Kết quả có cùng 23 ca lỗi, cùng 32 mutation SAI, cùng 5 ca credential lỗi. Đây là delta tập tên bằng 0, **không phải gate xanh**. Windows thật trên exact HEAD, CI PR/check-run và hậu land không đo được vì cấm mạng/không có hiện vật; không suy từ CRLF hay codec trên Linux.

Snapshot đầu/cuối bao phủ **10.814 tệp**, kể cả ignored/untracked ngoài `.git`: không delta byte, HEAD/tree/index/status khớp; status gồm ignored rỗng. Xem `evidence/snapshot-{before,after,comparison}.json`. Snapshot chứng minh không có delta tại hai mốc, không chứng minh lịch sử mọi lần ghi rồi hoàn nguyên.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding/lớp nguồn | Phân loại | Phép đo đóng / giới hạn |
|---|---|---|
| F01 `runner-stdin-khong-ghim-utf8` | **ĐÃ VÁ THẬT** đối với hai biểu hiện Linux đã báo | `python3 -B evidence/probe_review.py`: đường ASCII/có dấu × utf-8/ascii/cp1258: base 6/6, lượt 1 4/6, HEAD 6/6. Mutant codec mới `OK giet 1/1` đúng `r1117_runner_stdin_utf8_khi_tmpdir_co_dau`. `probe_contract.py` xác nhận EOF và frame lỗi sau sửa. Windows vẫn chưa đo, không tuyên bố đã nghiệm thu Windows. |
| F02 `dot-bien-map-van-nham-ca-qua-runner` | **ĐÃ VÁ THẬT** | Cùng script: hai mutant base `(0,0)`, lượt 1 `(2,0)`, HEAD `(0,0)`; HEAD từng ID `OK giet 1/1: r1122_nhat_ky_giu_loai_va_thong_diep_160`. Full A/B cũng không còn hai SAI mới của lượt 1: 32 SAI bằng nhau theo tên. |

Không thấy lỗi mới do hai hunk sửa F01/F02 trong các phép đo này. F03 thuộc phần chốt schema đã thêm ở lượt trước, được tìm thêm khi đột biến ngoài danh sách executor; không tái mở hai lớp trên. Tỷ lệ hai lớp nguồn được vá trong phạm vi đã báo: 2/2; tỷ lệ này không thay finding mới hay cổng chưa đo.

## ĐỐI CHIẾU NGUỒN #1079 VÀ RANH GIỚI RUNNER

N0 trên exact base cộng hai ca HEAD nguyên văn: cả hai rc=1 bằng TinHieuChotCa, thấy sai `('giet', 'review_target')`. Trên HEAD cả hai ca qua. Các mutant env/argv/ghi kênh sớm đều được ca đích giết. Không tìm thấy cửa giả thụ động mới trong nguồn và phép đo đã chạy; không kích hoạt điều kiện cửa giả thứ tư.

Runner ngoài do `_dung_cay_harness` thật chép trước khi import module bị đột biến. `_dung_cay_harness` trong module bị đột biến có thể làm runner của **cây lồng** méo để đo runner: đây là cơ chế đã được r2 duyệt. Sáu biến thể méo runner có sẵn, khi đổi sang ca đích A2 hiện có, đều bị `r1117_cay_harness_chep_runner_that` giết bằng chốt của ca. Không thấy trường hợp lấy sai runner mà ca A2 vẫn xanh trong các biến thể ấy. Cố ý sửa `__file__`, monkeypatch hay ghi đè runner trên đĩa thuộc `RUNNER-CUNG-TIEN-TRINH` đã chấp nhận, không tính finding và không tuyên bố đã cô lập hoàn toàn.

## BANG NGHIEM THU

| Tiêu chí | Lệnh / phép đo | Output thật | Đạt? |
|---|---|---|---|
| Exact SHA/spec/write set/trần | `sha256sum SPEC.md SPEC-R1.md`; Git diff/numstat; snapshot | Hash đúng; hai tệp, +316/-85; HEAD/tree không đổi | Có |
| N0 r2 | `python3 -B evidence/probe_review.py` | Hai ca chép nguyên văn vào base đều rc=1, HONG TinHieuChotCa, nhận sai giet | Có |
| A1: module init không tự giả kết quả | Cùng script; full mutation | Hai ca HEAD qua; các mutant quay nguồn/env/argv/ghi sớm đều OK đúng đích | Có trong phạm vi đo |
| A2: chép runner thật | Ca `r1117_cay_harness_chep_runner_that`; `python3 -B evidence/probe_copy_and_cli.py` | Neutral qua; bỏ copy OK 1/1; sáu biến thể méo runner đều OK giet 1/1 với ca A2 | Có |
| A3: thứ tự stdin/import/chấm/ghi và bỏ kênh main | `nl -ba` runner; `probe_contract.py`; `probe_copy_and_cli.py`; `rg -n 'LT_KENH_'` | Đọc byte :44, bit fd :47–50, gọi :62, import test :72, chấm :77, ghi :78–79. Main HEAD rc=0, không tạo kênh dù có LT env; base tạo | Có về hành vi |
| A4: ca/đột biến #1079 giữ nghĩa | `probe_review.py`; full mutation | 38/38 ca tập trung qua; hai mutant map, nonce và stdout đều OK | Có |
| A5 full launcher Linux | `python3 -B evidence/run_ab.py` | HEAD 343/366, tổng 368; base 339/362, tổng 364; cùng 23 lỗi, cùng 2 skip; rc=1 | Delta lỗi 0; chưa N/N sạch |
| A5 full mutation Linux | Cùng lệnh | HEAD 551/583; base 543/575; cùng 32 SAI, cùng 4 không đo; rc=1 | Delta SAI 0; chưa M/M sạch |
| A5 credential | Cùng lệnh | Cả hai 13/18, cùng 5 lỗi, TỔNG: ĐỎ; rc=1 | Delta lỗi 0; chưa đạt |
| A7 / mục 8(a)(b)(c) | `probe_review.py`; full mutation | Ca lồng/cùng tên/định dạng lỗi, lỗi cũ, chi tiết 160 đều qua; ba mutant map/qua/chi tiết mới đều OK giet 1/1 | Có |
| Mỗi chốt mới có mutation đúng TinHieuChotCa | AST toàn bảng + `python3 -B evidence/probe_guard_teeth.py` | Không có mutant kiểm kiểu record; bỏ riêng guard → SAI 0/1 do AttributeError, không tới chốt | **Không — F03 P2** |
| A6/A8 tĩnh | Ruff F no-cache JSON trên hai tệp; doctrine-scan; git diff --check | Ruff base/head rc=1, 5/5 F841 cũ, delta chuẩn hóa rỗng; không còn loai_luot; doctrine rc=0, 10 tệp/0 chỗ; diff-check rc=0 | Có về delta và hai cổng cục bộ |
| A5 Windows / CI exact HEAD / hậu land | Không gọi mạng | not_run / không có hiện vật để đọc lại | KHÔNG ĐO ĐƯỢC |

A3 literal r1 nói LT_KENH chỉ còn trong ca/đột biến, nhưng mục 2 đồng thời bắt buộc lọc LT_KENH trong env. Giữ bộ lọc ở :15409 và docstring :15402 là đúng mục 2, không phải finding. Các chỗ khác là ca :10510–10512, :10535–10537; bảng mutant :15088–15089, :15093. Main không còn phần kênh. Ruff ở đây là bare lint với command/rule/scope đã ghi; không đo pin/probe contract workflow và không gọi bare lint rc=1 là passed.

## BANG DO

| Khẳng định | Diff / lời khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Diff hai tệp, +316 | numstat.txt, prompt | So byte diff.patch với Git, full numstat | Có |
| F01 byte stdin/UTF-8 | diff-tu-l1.patch | `probe_review.py`: HEAD 6/6; `probe_contract.py`: byte lỗi rc=2, EOF mọi alias | Có trên Linux |
| F02 neo lại hai mutant | diff-tu-l1.patch, executor khai OK 1/1 | `probe_review.py`: b6fe853 SAI 0/1 từng ID, HEAD OK 1/1; full A/B không thêm SAI | Có |
| Kênh không còn trong env/argv | Runner/cham_lap_ca | `probe_review.py`: argv 4 mục, stdin 2 dòng, env_channel_keys=[], channel_in_argv=false, parent_channel_exists=false | Có trong phép đo |
| Kết quả lấy từ lời gọi ngoài, không từ map | SPEC mục 8 | Các ca r1122 xanh; các mutant map làm đúng ca đích giet | Có |
| Lỗi mang loại + 160 ký tự | SPEC mục 8(b), sửa reporter | `r1122_reporter_giu_loai_va_cat_dung_thong_diep` qua cả OSError transport và TypeError con | Có |
| Mọi mutant mới/đổi được chỉ định đều OK | Bảng DOT_BIEN_HARNESS | `summarize.py`: 11 ID mới đều OK; năm ID đổi đều OK trong full log | Có với danh sách đó; không bao phủ chốt còn thiếu F03 |
| A/B và Windows còn đang đo khi giao review | Prompt | A/B cục bộ đã xong, điều kiện TMPDIR không đáp ứng; Windows/CI không có evidence | Không suy thành pass |

Kiểm kê độc lập: `python3 -B evidence/inventory.py` dùng AST/literal_eval của **toàn bộ** ba bảng `DOT_BIEN`, `DOT_BIEN_HOOK`, `DOT_BIEN_HARNESS`, so cả record/cặp thay/ca đích trên base, lượt 1 và HEAD; không chỉ lọc wp1117. Product 446→446 và hook 79→79 không đổi. Harness 54→62: 11 ID mới, 3 bỏ đúng mục 9, 5 đổi (`wp1079_bao_cao_theo_ten_lop`, `wp1079_bo_tien_to_khac`, `wp1079_lap_ca_bo_kiem_nonce`, `wp1079_lap_ca_tin_stdout`, `wp1122_dinh_dang_lai_sau_ghi_map`). Cả 62 neo khớp đúng một chỗ sau khi bỏ bảng khỏi vùng thay; không ca đích vắng.

Cách kiểm kê đó chỉ thấy mutation đã được viết, **không chứng minh mọi chốt đã có mutation**. Vì vậy đã đọc thêm các nhánh kiểm tra mới và thử bỏ guard kiểu record bằng bộ chấm thật: tìm ra F03 ngoài danh sách executor và ngoài danh sách kiểm kê. Mục bị bỏ sót được tính finding như prompt yêu cầu. Chi tiết ở `evidence/mutation-inventory.json`, `mutation-results.json`, `guard-teeth-result.json`.

## BANG TEST

| Bộ | N/M, rc | Bỏ qua / giới hạn |
|---|---|---|
| HEAD full launcher | 343/366 qua; tổng 368; rc=1 | 23 lỗi, 2 skip |
| BASE full launcher | 339/362 qua; tổng 364; rc=1 | Cùng 23 tên lỗi, cùng 2 skip |
| HEAD full mutation | 551/583 đạt; tổng 587; rc=1 | 32 SAI, 4 không đo |
| BASE full mutation | 543/575 đạt; tổng 579; rc=1 | Cùng 32 tên SAI, cùng 4 không đo |
| Credential HEAD/BASE | 13/18 mỗi vế; rc=1 | Cùng 5 lỗi; credential mutation không chạy vì neutral đỏ |
| Ca tập trung HEAD | 38/38 qua | Toàn bộ r1079/r1117/r1122, 0 skip; kết quả chi tiết trong review-probes.json |
| N0 base + hai ca HEAD nguyên văn | Cả hai 0/1, rc=1 đúng phản chứng | Không viết payload mới |
| Encoding base / lượt 1 / HEAD | 6/6 / 4/6 / 6/6 | 18 tổ hợp tổng cộng, không Windows |
| Runner contract | 11/11 đúng kết quả mong đợi | 3 khung hợp lệ; 5 khung lỗi rc=2; 0/2 match trả loi; EOF text/buffer/original/fd0; không .pyc |
| Phép bỏ guard trên HEAD | Neutral qua, mutant SAI 0/1, accounting (1,0) | Đỏ do AttributeError, **không** nhận là giết đúng chốt |
| Hint thử trên clone | Neutral 1/1; 4/4 mutant OK, tổng 5/5 kill theo ca; accounting (0,0) | Có nonce, stdout, kiểu record và loại hợp lệ; không chạy full suite trên hint |
| Hint đối chứng lỗi vô can | Trả loi, không được tín dụng; script rc=0 | AttributeError không mang .get/list metadata không bị chuyển thành chốt |

Hai skip suite: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity`.

Bốn skip mutation: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song`.

23 tên lỗi suite bằng nhau trong `evidence/suite-comparison.json`: 10 đường run đã biết, 11 r484 báo Codex home inside repository, và 2 ca không ghi được /var/tmp (`r858_goc_tam_tranh_to_tien_co_git`, `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`). Toàn bộ 32 mutation SAI chung và output ở `evidence/mutation-results.json`; không đổi chúng thành pass. Credential cùng 5 tên đỏ: t15, t16, t18, t6, t9, xem log nguyên văn.

## BANG SAN

| Hướng độc lập / giả thuyết | Lệnh đã chạy | Output thật | Kết luận |
|---|---|---|---|
| 1. Đường kênh có dấu hỏng khi stdin ASCII/cp1258 | `python3 -B evidence/probe_review.py` | Base 6/6, lượt 1 4/6, HEAD 6/6; codec mutant OK 1/1 | KHÔNG PHẢI LỖI hiện tại; F01 đã vá trong phạm vi đã đo |
| 2. Stdin/fd 0 còn dữ liệu hoặc khung hỏng vẫn import/chạy | `python3 -B evidence/probe_contract.py` | Cả bốn alias EOF; 0/1/3 dòng, nonce rỗng và UTF-8 lỗi rc=2/no channel | KHÔNG PHẢI LỖI trong phép đo |
| 3. Dữ liệu kênh lọt env/argv, hoặc kênh cha bị ghi | `probe_review.py`, đoạn ENVELOPE | env_channel_keys=[], argv không mang kênh/nonce, parent_channel_exists=false; target qua | KHÔNG PHẢI LỖI |
| 4. Tên ca thiếu/trùng khiến chọn đại | `probe_contract.py` | Không khớp → loi/khop 0; trùng → loi/khop 2; đối chứng qua | KHÔNG PHẢI LỖI |
| 5. Module initializer tự công bố kết quả rồi thoát | `probe_review.py`, hai ca N0/HEAD; full mutation | Base cả hai HONG/giet sai; HEAD cả hai qua; mutant env/argv/ghi sớm đều OK 1/1 | KHÔNG PHẢI LỖI hiện tại trong mô hình thụ động |
| 6. Cây lồng lấy runner méo mà A2 vẫn xanh | `python3 -B evidence/probe_copy_and_cli.py` | Sáu biến thể runner có sẵn đều OK giet 1/1: r1117_cay_harness_chep_runner_that; neutral qua | KHÔNG PHẢI LỖI trong biến thể đã đo; ghi đè cố ý ngoài phạm vi |
| 7. Ca lồng cùng tên / __str__ đổi loi ngoài thành giet | `probe_review.py` — r1122_kenh_loi_phai_thuoc_luot_ngoai; full mutation | Ca qua; runner_doc_map_toan_cuc OK giet 1/1 đúng đích | KHÔNG PHẢI LỖI |
| 8. Kết quả qua/bo_qua mang chi tiết lỗi cũ | `probe_review.py` — hai ca r1122_kenh_*; full mutation | Qua cả nhánh lỗi khi import, ca lồng và bo_qua; map_de_ket_qua_qua OK 1/1 | KHÔNG PHẢI LỖI |
| 9. Reporter mất loại hoặc cắt sai 160 | `probe_review.py` — r1122_reporter_giu_loai_va_cat_dung_thong_diep | qua, gồm OSError transport và TypeError con; lap_ca_bo_chi_tiet_loi OK 1/1 | KHÔNG PHẢI LỖI |
| 10. Stdout giả, nonce/tên sai, loại lạ được nhận | `probe_review.py` — r1079_cham_lap_ca_doi_dung_TinHieuChotCa, r1079_harness_duoi_stdout_gia_khong_cap_tin_dung | Hai ca qua; nonce mutant OK 1/1, stdout OK 2/2, bo_kiem_loai OK 1/1 | KHÔNG PHẢI LỖI hiện tại |
| 11. Neo mới F02 vẫn không đo map | `probe_review.py`; `run_ab.py`; `summarize.py` | Hai mutant HEAD OK 1/1; HEAD_ONLY_FAILED=[] | KHÔNG PHẢI LỖI; F02 đã vá |
| 12. Chốt kiểu record mới thiếu witness đúng tín hiệu | `python3 -B evidence/probe_guard_teeth.py` | SAI giet 0/1, tin dung gia: AttributeError list.get; không có record tương ứng trong cả ba bảng | **LỖI — F03 P2** |
| 13. Windows, CI exact HEAD, hậu land | Không gọi mạng; chỉ kiểm hiện vật được cấp | not_run / không có log Windows exact HEAD hay check-run để xác minh | KHÔNG ĐO ĐƯỢC |

## BANG LOP

| Slug lớp | Biểu hiện / nguồn | Hạng còn mở | Vá chung / phép đóng |
|---|---|---|---|
| runner-stdin-khong-ghim-utf8 | F01 lượt 1, b6fe853; ASCII decode và cp1258 sai đường | Không còn trong phạm vi Linux đã báo | HEAD ma trận 6/6, codec mutant đúng chốt, EOF/frame hồi quy; Windows ghi riêng chưa đo |
| dot-bien-map-van-nham-ca-qua-runner | F02 lượt 1, hai mutant map không giết ca cũ | Không còn | Đã đổi cả hai đích sang ca nhật ký; targeted + full A/B xác nhận |
| chot-kieu-record-chua-co-dot-bien-dung-tin-hieu | F03 mới, thiếu mutant bỏ guard dict; fixture list chưa tới bang khi bỏ guard | **P2** | Thêm mutant và chốt đúng lỗi schema tại ca hiện có; neutral qua, mutant chết bằng chính ca; giữ đối chứng lỗi vô can |

### chot-kieu-record-chua-co-dot-bien-dung-tin-hieu [P2] F03 — Chốt kiểu record mới thiếu mutation được giết bằng chốt ca

TEP/DONG: `.claude/dev/launcher_test.py:10329` trong `r1079_cham_lap_ca_doi_dung_TinHieuChotCa`; guard runtime ở `:15421`; bảng mutation bắt đầu `:14926`.

VAN DE: HEAD đã thêm `not isinstance(kq, dict)` trước `.get` và fixture `danh_sach` hiện trả loi đúng. Nhưng toàn bộ ba bảng không có mutation bỏ riêng chốt này. Hơn nữa, ca gọi helper thẳng ở :10329; nếu bỏ guard, AttributeError văng trước assertion tổng ở :10330. Vì vậy chỉ thêm record mutant chưa đủ đáp ứng yêu cầu mục 4 prompt snapshot: mỗi chốt mới phải có mutant làm đúng ca đích đỏ bằng TinHieuChotCa. Đây là thiếu witness đúng tín hiệu. Việc bỏ guard vẫn làm suite đỏ bằng lỗi thường; không khai guard hoàn toàn không có coverage, không khai HEAD đang nhận JSON list là giet, và không coi đây là cửa giả thứ tư của #1117.

DA THU NGHIEM: `python3 -B evidence/probe_guard_teeth.py` dùng bộ chấm `chay_dot_bien` thật, neutral nguyên HEAD qua, chỉ bỏ `not isinstance(kq, dict) or` trong bản sao. Payload JSON list lấy nguyên từ ca hiện có. Kết quả:

```text
review_bo_kiem_kieu_record   SAI  giet 0/1: (khong ca nao chet) [tin dung gia: r1079_cham_lap_ca_doi_dung_TinHieuChotCa(AttributeError: 'list' object has no attribute 'get')]
accounting: (1, 0)
```

HUONG VA: Sửa ngay phép gọi trong vòng `runner_gia` của ca hiện có, vì đây là nơi fixture JSON list đi qua hợp đồng helper. Khóa đúng AttributeError do `.get` trên list của nhánh `danh_sach`, rồi `bang(False, ...)`; mọi ngoại lệ/nguồn khác giữ nguyên. Thêm mutant `wp1117_lap_ca_bo_kiem_kieu_record` bỏ riêng guard, nhắm ca này. Không đổi guard runtime, không hạ tiêu chuẩn kill và không xóa fixture đối chứng.

DA THU VA: Có, chỉ trên `evidence/hint/`. `python3 -B evidence/try_hint.py`: neutral qua; mutant mới `OK giet 1/1: r1079_cham_lap_ca_doi_dung_TinHieuChotCa`, accounting cả nhóm `(0,0)`. Mutant nonce vẫn OK 1/1, stdout OK 2/2, loại hợp lệ OK 1/1. Chấm trực tiếp target trên bản bỏ guard sau sửa test trả `('giet', <đúng tên ca>)`. `python3 -B evidence/probe_hint_negative.py`: AttributeError vô can tại cùng nhánh vẫn trả loi, không được tín dụng. Ruff vẫn 5 lỗi nền; patch dry-run `--fuzz=0 -p0` rc=0. Không chạy full suite/mutation trên hint, không sửa cây thật.

RUI RO: Không mở catch thành Exception hay mọi AttributeError; sẽ biến lỗi vô can thành tín dụng giả, đúng bệnh của #1079. Hint chỉ nhận `k == "danh_sach"`, `e.name == "get"`, `e.obj` là list; phải giữ đối chứng lỗi vô can, runner_dung/nonce_sai/ten_sai và đo lại full mutation, Windows thật. Catch này là assertion hợp đồng schema của fixture đã biết, không phải đổi mọi lỗi hạ tầng thành kill.

DO TIN: cao trên Linux với phép bỏ guard, neutral, chốt đúng tên và đối chứng âm đã đo. P2 theo yêu cầu witness của prompt; không phải P1 hành vi runtime hay finding do thiếu Windows.

## HINT và bàn giao

`HINT.patch` gồm hai hunk thuần test/bảng mutation, áp từ gốc bằng `patch -p0 --fuzz=0`; dry-run trên clone exact HEAD rc=0. Không có hunk sửa runner hay guard runtime. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Dùng hint thì khai hint_provenance theo protocol.

F03 vẫn mở trên reviewed_sha. Bản sửa thử trong scratch không đóng finding của cây được review. Executor cần tái dẫn xuất test/mutant, giữ các đối chứng, đo gate trên SHA mới; Windows/CI exact HEAD và điều kiện TMPDIR vẫn cần bằng chứng riêng, không được nhận các bộ đỏ có delta 0 là gate xanh.
