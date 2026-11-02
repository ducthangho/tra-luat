verdict: changes_requested
reviewed_sha: b6fe8534d7498ebe88a1a222b49fbf36fe97cdf1
spec_sha256: c34d506626e40a07fbfef41ccd39e138f74a2df3116f1b53cea704aaf6068d43
Ket qua: 0 P0, 2 P1, 0 P2, 0 P3.

HEAD có hai hồi quy đo được: runner đọc sai đường kênh Unicode khi stdin không dùng UTF-8; hai đột biến #1079 còn nhắm ca không còn đo map bị sửa. Chưa đủ điều kiện approval. HINT chỉ sửa test và ca đích đột biến; hướng sửa runner được mô tả bằng lời.

- Base: `c7174bfe03b3acd22cfa055b5fce176129d29542`.
- Reviewed tree: `c21c78108fd2f235f9d908ea64caf4d4871e4266`.
- SPEC-R1 SHA256: `48710a9b41cb744dd5b89df1d9f632fae51d08dcf22a0581088918832663598e`.
- Packet #1117, r2, generation 2, lease `wp1117-r2-g2-claude`, sensitive, lượt 1/10. Áp ngưỡng chủ kho: hết P1/P2/P3; không áp ADR-0060.
- Reviewer độc lập với executor Claude. `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, theo `run/186e1046/run.json`. Exact served model/effort không đo được trong các trường runtime hiện có; không suy từ tài khoản vận chuyển verdict.
- Linux, Python 3.13.18, Git 2.43.0, Ruff 0.16.9. Sandbox `workspace-write`; checkout được đối xử chỉ đọc, không đổi permission.

## Phạm vi, phương pháp và giới hạn

Đã đọc prompt snapshot, SPEC r2/R1, diff, hướng dẫn kho, phần protocol về review/gate, runner và các đường gọi liên quan. `diff.patch` khớp byte với `git diff BASE HEAD -- .claude`; toàn diff chỉ có hai tệp mã, +288/-83. Các clone phản chứng ở `evidence/`, ngoài `cay-kho/`, neo exact base/head, `core.abbrev=7`. Không push, không gọi mạng hoặc dùng credential thật. Chỉ chạy payload/ngoại lệ đặc biệt đã có trong kho; không soạn payload giả kênh hay lớp ngoại lệ đặc biệt mới.

Lệnh chạy từ thư mục workspace này trừ các lệnh được `evidence/run_ab.py` chạy với cwd `evidence/base` hoặc `evidence/head`. A/B full suite + mutation + credential được khởi chạy trong **một lệnh** `python3 -B evidence/run_ab.py`, hai vế cùng môi trường, TMPDIR và công cụ. Log có command, rc, mốc UTC và thời lượng ở `evidence/*-{suite,mutations,credentials}.json`; output nguyên văn ở tệp `.log` tương ứng.

`/tmp/.git` có mặt và chỉ đọc. Chỉ được ghi trong scratch dưới `/tmp`, còn `/var/tmp` bị từ chối; vì vậy điều kiện TMPDIR **ngoài `/tmp`** của Linux A/B không đo được. Không xóa hoặc che `.git`. So tập tên lỗi, không chỉ so tổng: full suite có cùng 23 tên hỏng; mutation có 32 tên SAI chung và đúng 2 tên SAI mới (F02). Không gọi các bộ đỏ là pass. Windows thật, check-run CI exact HEAD và gate sau land không đo do chỉ thị cấm mạng/không có hiện vật; không suy từ kiểm tra Linux.

Snapshot trước/sau của **10.814 tệp** (kể cả ignored/untracked ngoài `.git`) không có delta byte; HEAD/tree, status và danh sách index khớp. `git status --porcelain=v1 --untracked-files=all --ignored=matching` rỗng. Bằng chứng: `evidence/snapshot-{before,after,comparison}.json`. Snapshot chỉ chứng minh không có delta ở hai mốc.

## ĐỐI CHIẾU NGUỒN #1079

Đây là lượt đầu của #1117, không phải lượt kế của toàn bộ #1079. Finding nguồn `F04-kenh-ket-qua-gia-truoc-main` đã được kiểm lại bằng hai ca mục 5 có sẵn: trên exact base cả hai đỏ rc=1 với `('giet', 'review_target')`; trên HEAD cả hai xanh. Các đột biến env/argv/ghi kênh sớm đều bị đúng ca đích giết. Không tìm thấy cửa giả thụ động mới trong các phép đo này. Giới hạn `RUNNER-CUNG-TIEN-TRINH`, gồm can thiệp cố ý/ghi đè tệp, giữ nguyên theo quyết định chủ kho; không tính finding.

## BANG NGHIEM THU

| Tiêu chí | Lệnh/phép đo | Output thật | Đạt? |
|---|---|---|---|
| Exact head/spec/write set/trần | `sha256sum SPEC.md SPEC-R1.md`; `git -C cay-kho diff --numstat BASE HEAD` | Hash khớp; test +208/-83, runner +80/-0; 2 tệp, +288 ≤ 450 | Có |
| N0 r2 | `python3 -B evidence/probe_existing.py` — chép nguyên văn hai ca mục 5 vào clone base | Cả hai rc=1, `TinHieuChotCa`, nhận sai `('giet', 'review_target')` | Có, phản chứng tái hiện |
| A1: khởi tạo module không giả kênh | Cùng script + full `--dot-bien` | Hai ca HEAD 1/1; đột biến quay lại nguồn/env/argv/ghi sớm đều `OK giet 1/1` | Có trên các nguồn đã đo |
| A2: chép runner thật | `--lap-ca r1117_cay_harness_chep_runner_that --lan 1`; `wp1117_cay_khong_chep_runner` | 1/1 xanh; mutant `OK giet 1/1` | Có |
| A3: thứ tự và bỏ kênh trong main | `rg -n 'LT_KENH_' cay-kho/.claude/dev/launcher_test.py`; đọc runner theo số dòng | Đọc/bit stdin :42–46, gọi :58, nạp :68, chấm :73, ghi :74–75; main không đọc/ghi kênh | Đạt hành vi; xem lưu ý literal bên dưới |
| A4: giữ ca/đột biến #1079 | `python3 -B evidence/run_ab.py`; `python3 -B evidence/summarize.py` | Ca liên quan xanh; nonce `OK 1/1`, stdout `OK 2/2`; **hai mutant map SAI 0/1 chỉ trên HEAD** | **Không — F02** |
| A5: full suite | `python3 -B .claude/dev/launcher_test.py --nhat-ky <log>` trên hai clone | HEAD 342/365, tổng 367, bỏ 2, hỏng 23; base 339/362, tổng 364, bỏ 2, hỏng 23; rc=1 cả hai | Delta tập lỗi = 0; chưa đạt N/N sạch |
| A5: full mutation | `python3 -B .claude/dev/launcher_test.py --dot-bien` trên hai clone | HEAD **548/582**, SAI 34, bỏ 4; base **543/575**, SAI 32, bỏ 4; rc=1 cả hai | **Delta +2 SAI — F02** |
| A5: credential | `python3 -B .claude/dev/codex_cred_test.py` trên hai clone | 13/18, `TỔNG: ĐỎ`, cùng 5 tên lỗi; rc=1 | Delta = 0; mutation credential không chạy vì nền đỏ |
| A6/A8: cổng tĩnh | Ruff `check --no-cache --select F --output-format json` trên hai tệp; doctrine-scan; diff-check | Ruff base/head 5/5 lỗi F841 cũ, normalized delta rỗng; không còn `loai_luot`; doctrine rc=0, 10 tệp/0 chỗ; diff-check rc=0 | Đạt delta Ruff và cổng cục bộ, không gọi bare lint là xanh |
| A7/mục 8–9: kênh #1122 qua runner | `python3 -B evidence/probe_existing.py`; full mutation | 20/20 ca tập trung xanh; ba mutant map/qua/chi tiết mới đều `OK giet 1/1` | Có; vẫn còn F02 ngoài ba mutant này |
| Transport với tên đường Unicode | `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_transport.py` | Base 6/6 qua; HEAD 4/6 qua, 2 lỗi ở đường có dấu + ascii/cp1258 | **Không — F01** |
| Windows/CI/A6 sau land | Không gọi mạng | `not_run`/không có hiện vật Windows exact HEAD, CI hoặc sau land | KHÔNG ĐO ĐƯỢC |

Lưu ý A3: literal r1 “LT_KENH_ chỉ còn trong ca/đột biến” vẫn bắt bộ lọc bắt buộc của mục 2 ở :15387, cùng docstring :15380. Đây là chỗ tiêu chí chữ tự mâu thuẫn với yêu cầu lọc env; không coi việc giữ bộ lọc là lỗi mã. Các dòng còn lại: ca phản chứng :10510–10512, :10535–10537; bảng mutant :15070–15071, :15075. Main đã bỏ toàn bộ kênh cũ.

## BANG DO

| Khẳng định | Diff/lời khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| +288, hai tệp | `numstat.txt` | Git diff và so byte `diff.patch`: +288/-83, 2 tệp | Có |
| N0 base đỏ, HEAD xanh | Executor khai hai ca | `probe_existing.py`: base 0/1 cả hai; HEAD 1/1 cả hai | Có |
| Dữ liệu kênh không nằm trong env/argv | Runner/cham_lap_ca | `python3 -B evidence/probe_env.py`: argv 4 mục, stdin 2 dòng, env_LT_KENH_keys=[], channel_in_argv=false, parent_channel_exists=false | Có trong phép đo |
| Kết quả trực tiếp từ `cham_mot_ca` | Runner :73 | Hai ca kênh r1122 xanh; mutant đọc map làm ca ngoài đỏ bằng chốt của nó | Có |
| Chi tiết lỗi giữ loại + 160 ký tự | Mục 8(b) | `r1122_reporter_giu_loai_va_cat_dung_thong_diep` 1/1, cả lỗi transport và lỗi con | Có ở UTF-8; F01 là lỗi transport khác |
| Mọi mutant liên quan còn OK | Yêu cầu A4/mục 9 | Full A/B: `wp1079_bao_cao_theo_ten_lop`, `wp1079_bo_tien_to_khac` HEAD SAI/base OK | **Không — F02** |
| Runner hoạt động với stdio không UTF-8 | Chưa có phép đo executor riêng cho đường kênh có dấu | `probe_transport.py`: Unicode + ascii/cp1258 chỉ HEAD lỗi | **Không — F01** |
| Linux A/B và Windows còn đang đo | Prompt khai “ĐANG ĐO” | A/B cục bộ đã chạy xong với giới hạn TMPDIR; Windows không có evidence trong bundle | Không suy thành pass |

Kiểm kê độc lập dùng AST của **toàn bộ** bảng literal `DOT_BIEN`, `DOT_BIEN_HOOK`, `DOT_BIEN_HARNESS` trên base/head, rồi so từng ID/cặp thay/ca đích; không lọc riêng tiền tố `wp1117_`. Kết quả lưu `evidence/mutation-inventory.json`: 10 ID mới, 3 ID bỏ đúng mục 9, 3 ID đổi (`wp1079_lap_ca_bo_kiem_nonce`, `wp1079_lap_ca_tin_stdout`, `wp1122_dinh_dang_lai_sau_ghi_map`). Mọi neo của 61 mutant harness khớp đúng một chỗ khi bỏ bảng khỏi vùng thay. Cách này kiểm kê bảng hiện tại, không chứng minh mọi lỗi hành vi đều có mutant; đọc đường gọi và full A/B tìm ra hai ID cũ bị lệch nghĩa mà danh sách “mới/đổi” không bắt được.

Mười mutant mới đều đã in `OK giet 1/1` đúng ca đích: `runner_doc_map_toan_cuc`, `runner_map_de_ket_qua_qua`, `lap_ca_bo_chi_tiet_loi`, `runner_ve_lai_nguon_dot_bien`, `env_con_mang_kenh`, `runner_lo_kenh_qua_env`, `runner_lo_kenh_qua_argv`, `runner_ghi_kenh_truoc_khi_ca_chay`, `bo_kiem_loai`, `cay_khong_chep_runner` (đều có tiền tố `wp1117_`). Chi tiết từng record ở `evidence/mutation-results.json`.

## BANG TEST

| Bộ | N/M, rc | Bỏ qua / giới hạn |
|---|---|---|
| HEAD full launcher | 342/365 đã chạy qua; tổng 367; rc=1 | 2 skip, 23 hỏng |
| BASE full launcher | 339/362 đã chạy qua; tổng 364; rc=1 | Cùng 2 skip và cùng 23 tên hỏng |
| HEAD full mutation | 548/582 đạt; 586 tổng; rc=1 | 4 không đo được; 34 SAI |
| BASE full mutation | 543/575 đạt; 579 tổng; rc=1 | Cùng 4 không đo được; 32 SAI |
| Credential HEAD/BASE | Cả hai 13/18; rc=1 | Cùng 5 tên đỏ; dừng trước mutation do neutral đỏ |
| Ca tập trung HEAD | 20/20, mọi rc=0 | 0 skip; chọn AST: toàn bộ r1117/r1122 và r1079 có kenh/lap_ca/harness |
| N0 base + hai ca HEAD nguyên văn | 0/2 xanh; cả hai rc=1 đúng phản chứng | Không có sửa payload |
| Ma trận encoding A/B | BASE 6/6; HEAD 4/6 | ASCII/Unicode path × utf-8/ascii/cp1258 |
| Runner contract trực tiếp | 6/6 kết quả đúng kỳ vọng | Một ca bình thường, 0/2 match, stdin 0/1/3 dòng; không sinh .pyc |
| HINT F01 trên HEAD | 0/1, rc=1 đúng `TinHieuChotCa` của ca mới | Đỏ thật, không nhận lỗi hạ tầng làm kill |
| HINT F01 + sửa thử runner trên clone | 1/1, rc=0; chạy đủ 6 tổ hợp | Chưa sửa cây thật |
| Hồi quy sau sửa thử stdin | 5/5, mọi rc=0 | Hai ca khởi tạo module, nonce/schema, hai ca kênh r1122 |
| HINT F02, hai mutant | Trước `(2,0)`, mỗi mutant SAI 0/1; sau `(0,0)`, mỗi mutant OK 1/1 | Chạy `chay_dot_bien` thật, giữ tiêu chí chốt đúng ca |

Hai skip suite: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity`.

Bốn skip mutation: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song`.

23 tên lỗi suite bằng nhau ở `evidence/suite-comparison.json`: 10 đường `run` đã biết, 11 ca `r484_*`, và 2 lỗi bị từ chối ghi `/var/tmp` (`r858_goc_tam_tranh_to_tien_co_git`, `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`). 32 mutant SAI chung không được nhận là pass; tên/output đầy đủ và delta +2 ở `evidence/mutation-results.json`. Credential cùng 5 tên lỗi, xem `evidence/{base,head}-credentials.log`.

## BANG SAN

| Hướng độc lập / giả thuyết | Lệnh đã chạy | Output thật | Kết luận |
|---|---|---|---|
| 1. Encoding ống stdin khác bên gửi làm hỏng đường kênh | `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_transport.py` | Base 6 qua; HEAD 4 qua/2 loi; raw stderr: UnicodeDecodeError (ascii), FileNotFoundError (cp1258) | **LỖI — F01** |
| 2. Đổi kiến trúc làm mutant cũ không còn đo đúng đường | `python3 -B evidence/run_ab.py`; `python3 -B evidence/summarize.py` | SAI_HEAD_ONLY đúng hai mutant map; base OK 1/1, HEAD SAI 0/1 | **LỖI — F02** |
| 3. Env cha chứa nhiều khóa LT_KENH hoặc argv giữ dữ liệu kênh | `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_env.py` | Qua; env khóa kênh rỗng, channel_in_argv=false, kênh cha không được ghi | KHÔNG PHẢI LỖI trong phạm vi đo |
| 4. Khung stdin sai vẫn làm runner công bố kết quả | `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_contract.py` | 0/1/3 dòng đều rc=2, channel=null, không .pyc | KHÔNG PHẢI LỖI |
| 5. Tên ca khớp thiếu/nhiều làm chọn đại hoặc gọi main | Cùng `probe_contract.py` | 0 match → loi/khop 0; 2 match → loi/khop 2; đối chứng → qua; không .pyc | KHÔNG PHẢI LỖI |
| 6. Ca lồng cùng tên / __str__ đổi lỗi ngoài thành giet | `python3 -B evidence/probe_existing.py` — r1122_kenh_loi_phai_thuoc_luot_ngoai | 1/1; cả các nhánh cùng tên và __str__ có sẵn; mutant đọc map OK giet 1/1 | KHÔNG PHẢI LỖI hiện tại |
| 7. Lỗi cũ ở lúc import hoặc ca lồng làm bẩn kết quả qua | Cùng script — r1122_kenh_ca_qua_khong_mang_chi_tiet_cu | 1/1; mutant map đè qua OK giet 1/1 | KHÔNG PHẢI LỖI hiện tại |
| 8. Tin stdout, nonce sai, tên sai, JSON list hoặc loại lạ | Cùng script — r1079_cham_lap_ca_doi_dung_TinHieuChotCa và r1079_harness_duoi_stdout_gia_khong_cap_tin_dung | Cả hai 1/1; nonce mutant OK 1/1, stdout mutant OK 2/2 | KHÔNG PHẢI LỖI |
| 9. Neutral đỏ được nhận tín dụng do runner mới | Cùng script; full mutation | r1079_chay_dot_bien_noi_neutral_va_cham_theo_loai nằm trong full suite và xanh; các neutral đỏ có sẵn vẫn báo SAI | KHÔNG PHẢI LỖI trong phép đo |
| 10. Runner bản lồng bị lấy từ nguồn sai | Cùng script — r1117_cay_harness_chep_runner_that; full mutation | Ca bytes 1/1, bỏ copy → đúng chốt của ca; các mutant copy-runner méo có sẵn đều bị ca đích giết | KHÔNG PHẢI LỖI trong các biến thể có sẵn; ghi đè cố ý thuộc giới hạn đã duyệt |

## BANG LOP

| Slug | Finding/biểu hiện | Hạng mở | Nguồn | Cách vá chung / phép đóng |
|---|---|---|---|---|
| runner-stdin-khong-ghim-utf8 | F01: ASCII decode lỗi, cp1258 sai đường | P1 | Lượt #1117 này, exact HEAD | Ghim codec ở lần đọc đầu; ma trận 6 tổ hợp + hồi quy giả thụ động |
| dot-bien-map-van-nham-ca-qua-runner | F02: hai mutant map sống | P1 | A4/mục 9 r2, delta base→HEAD | Chuyển target sang ca đo map; neutral qua, từng mutant chết đúng TinHieuChotCa |

### runner-stdin-khong-ghim-utf8 [P1] F01 — Runner đọc sai đường kênh có dấu với stdin ASCII/cp1258

TEP/DONG: `.claude/dev/launcher_test_runner.py:42`; bên gửi `.claude/dev/launcher_test.py:15392`.

VAN DE: `subprocess.run(... input=..., encoding="utf-8")` gửi byte UTF-8, nhưng `sys.stdin.read()` trong runner dùng encoding mặc định của con. Khi TMPDIR có dấu, ASCII ném UnicodeDecodeError; cp1258 giải mã sang đường khác và không mở được kênh. Một ca neutral xanh thành `loi` dù bản gốc vẫn chạy được trong cùng môi trường. `open(0, encoding="utf-8")` ở :46 xảy ra **sau** lần đọc nên không sửa được lỗi này. Mọi ca dùng cùng transport có thể bị mất kết quả trong tổ hợp đó. Không liên quan giới hạn can thiệp cố ý cùng tiến trình.

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_transport.py` dùng nguyên ca `r1079_cham_mot_ca_chi_TinHieuChotCa_la_giet`, không thêm payload. Base 6/6 qua; HEAD chỉ hỏng Unicode path + ascii/cp1258. `evidence/transport-results.json` chứa từng tổ hợp; `evidence/transport-stderr.json` giữ hai stderr xác định nguyên nhân.

DA THU VA: có, trên `evidence/hint/`. HINT thêm ca `r1117_runner_stdin_utf8_khi_tmpdir_co_dau`. Trên HEAD ca đỏ rc=1 bằng chính `TinHieuChotCa` của nó (`evidence/hint-red.log`). Thử thay lần đọc đầu bằng `sys.stdin.buffer.read().decode("utf-8").splitlines()` trong clone: ca xanh rc=0, chạy đủ 6 tổ hợp (`evidence/hint-green.log`). Năm ca hồi quy về module init, nonce/schema, ca lồng/qua đều vẫn xanh (`evidence/hint-regression-results.json`). Không chạy full suite trên bản sửa thử, không khai đã sửa cây thật.

HUONG VA: đọc byte stdin/giải mã UTF-8 theo hợp đồng bên gửi, hoặc reconfigure stdin UTF-8 **trước** lần đọc đầu. Giữ đọc/bit fd 0 trước import. Thêm mutant quay lần đọc về codec môi trường nhắm ca mới. Không ép stdout/toàn env thành UTF-8 vì sẽ che ca console không UTF-8. Rủi ro cần kiểm: thứ tự đóng stdin, EOF ở cả sys.stdin/fd 0, framing hai dòng, Windows thật; sửa codec không thay bảo vệ env/argv. Chỉ cung cấp hunk test trong HINT do runner thuộc authority/gate sensitive.

DO TIN: cao trên Linux với PYTHONIOENCODING đặt tường minh. Chưa chạy Windows thật; không suy rằng toàn bộ Windows đều lỗi, hay một Windows gate với đường ASCII có thể loại trừ hồi quy này.

### dot-bien-map-van-nham-ca-qua-runner [P1] F02 — Hai mutant #1079 không còn làm đỏ ca đích

TEP/DONG: `.claude/dev/launcher_test.py:15000`/`:15006` (`wp1079_bao_cao_theo_ten_lop`), `:15025`/`:15029` (`wp1079_bo_tien_to_khac`); thay đổi đường chấm ở `:15391`.

VAN DE: Hai mutant sửa cách `chay_bo_ca` ghi LOAI_HONG. Ca đích cũ lại gọi `cham_lap_ca`, nay qua runner lấy kết quả từ `cham_mot_ca`, không đọc map. Vì vậy neutral và mutant đều qua; full gate có thêm đúng hai SAI so với base. Ca đích xanh riêng không chứng minh đột biến còn có tác dụng. Vi phạm A4/mục 9 r2; đây là lỗi gate đo được nên xếp P1 theo thang của prompt. Không phải một cửa giả tín hiệu mới và không kích hoạt điều kiện dừng vì tái diễn F04.

DA THU NGHIEM: `python3 -B evidence/run_ab.py` hoàn tất: base 543/575 (32 SAI), HEAD 548/582 (34 SAI), cùng 4 skip. `python3 -B evidence/summarize.py` trả SAI_HEAD_ONLY đúng hai ID. Log base mỗi ID `OK giet 1/1`; HEAD mỗi ID `SAI giet 0/1`. Neutral ca đích xanh trong full suite và phép đo riêng.

DA THU VA: có. `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_mutant_targets.py` chạy `chay_dot_bien` thật, chỉ chọn hai record có sẵn. HEAD nguyên `(2,0)`; clone đổi target cả hai sang `r1122_nhat_ky_giu_loai_va_thong_diep_160` trả `(0,0)`, mỗi ID `OK giet 1/1` đúng tên ca đó. Bộ chấm chỉ nhận `TinHieuChotCa` đúng ca, nên đây không phải kill do OSError/TypeError. Kết quả lưu `evidence/mutant-target-results.json`.

HUONG VA: HINT đổi target của hai mutant sang ca nhật ký hiện có, vì ca này thật sự gọi `chay_bo_ca` và kiểm map, loại cùng thông điệp. Có thể thay bằng bổ sung phép đo map trực tiếp vào ca cũ nếu executor muốn giữ liên kết cũ. Giữ các ca runner cũ để bảo vệ phân loại lớp; không xóa mutant hay hạ tiêu chí kill. Rủi ro: chỉ neo mới theo tên chưa đủ; phải duy trì neutral xanh, chốt của đúng ca và đo lại trên Windows cùng full mutation.

DO TIN: cao, có A/B exact SHA và phép thử sửa target bằng bộ chấm thật. HINT là gợi ý cho executor, không phải commit được duyệt.

## HINT và bàn giao

`HINT.patch` áp từ gốc cây bằng `patch -p0 --fuzz=0`. Dry-run trên bản sao HEAD rc=0; ba hunk chỉ thêm ca encoding và đổi hai target, không chứa sửa runner. Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit. Executor cần dẫn xuất sửa codec trong runner, nhận/test HINT, thêm mutant codec, rồi đo lại gate đúng điều kiện. Hai lớp vẫn mở trên reviewed_sha; không tự coi bản sửa thử trong scratch là đã đóng chúng.
