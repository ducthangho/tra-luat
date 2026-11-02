verdict: approve
reviewed_sha: 4a0d45d3c689600f749866f7b27e83b9d6039c00
spec_sha256: c34d506626e40a07fbfef41ccd39e138f74a2df3116f1b53cea704aaf6068d43
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

Review packet #1117 r2, lease `wp1117-r2-g2-claude`, lượt Codex 3/10, class `sensitive`. Áp ngưỡng hết P0/P1/P2/P3 theo chỉ thị; không áp ADR-0060. Hai trục đã xem: Spec và Standards/Security. Không tìm thấy finding mới trong phạm vi đã đo. F01/F02 giữ đóng và F03 đã đóng bằng cùng phép đo lượt 2; giới hạn gate được ghi riêng bên dưới.

Reviewer `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, run `5fb23c45`: nguồn là metadata cục bộ `run/5fb23c45/run.json`, không phải actor GitHub. Phiên này được giao vai Codex độc lập với executor Claude. Exact model/effort phục vụ từng request và session executor KHÔNG ĐO ĐƯỢC từ hiện vật được cấp; không tự cấp receipt/assurance của state machine. Không gọi mạng hoặc dùng credential thật.

HEAD/tree: `4a0d45d3c689600f749866f7b27e83b9d6039c00` / `7b54f030353f2fcfa664cb88bd5fb4839908e0de`; checkout detached, sạch khi bắt đầu. Base `c7174bfe03b3acd22cfa055b5fce176129d29542`. Spec r1 kế thừa có SHA-256 `48710a9b41cb744dd5b89df1d9f632fae51d08dcf22a0581088918832663598e`. Diff/numstat cấp trong packet khớp byte với phép đo Git; hai tệp, +326/-85, dưới trần +450. Nội dung hai hunk sửa từ L2 khớp nguyên `HINT-L2.patch`; chỉ tiêu đề hunk Git có thêm tên hàm/bảng.

## Đối chiếu các finding trước

| Slug lớp / nguồn | Kết luận trên HEAD | Phép đo và giới hạn |
|---|---|---|
| F01 `runner-stdin-khong-ghim-utf8` — L1 `b6fe8534d7498ebe88a1a222b49fbf36fe97cdf1` | ĐÃ VÁ THẬT các biểu hiện Linux đã báo, giữ đóng | `python3 -B evidence/probe_review.py`: base 6/6, L1 4/6, HEAD 6/6 với đường ASCII/có dấu × utf-8/ascii/cp1258. Mutation codec HEAD `OK giet 1/1` đúng `r1117_runner_stdin_utf8_khi_tmpdir_co_dau`. Windows thật chưa đo. |
| F02 `dot-bien-map-van-nham-ca-qua-runner` — L1 | ĐÃ VÁ THẬT, giữ đóng | Cùng script: hai mutation map base `(0,0)`, L1 `(2,0)`, HEAD `(0,0)`, mỗi cái `OK giet 1/1: r1122_nhat_ky_giu_loai_va_thong_diep_160`. |
| F03 `chot-kieu-record-chua-co-dot-bien-dung-tin-hieu` — L2 `b9f010b3e5ef521d2980f12a5a3d4317e1e78724` | ĐÃ VÁ THẬT | `python3 -B evidence/probe_f03.py`: neutral qua ở hai revision; cùng record bỏ guard dict trên L2 `SAI giet 0/1` do AttributeError, trên HEAD `OK giet 1/1` đúng ca `r1079_cham_lap_ca_doi_dung_TinHieuChotCa`. Cả nhóm 7 mutation HEAD `(0,0)`, 8/8 kết quả ca đích; L2 `(1,0)`. Đối chứng `probe_hint_negative.py` trên HEAD vẫn trả `loi` cho AttributeError vô can, `not_credited=true`. |

F03 chỉ sửa phép chốt của fixture JSON list và thêm record mutation; guard runtime/runner không đổi từ L2. Không mở catch thành mọi AttributeError: điều kiện giữ `k == danh_sach`, `e.name == get`, `e.obj` là list; lỗi không khớp vẫn raise. Không thấy hồi quy từ hai hunk trong các đối chứng đã chạy. Có 3 lớp lịch sử, không có lớp đang mở trong phạm vi đo.

## Phạm vi bằng chứng và giới hạn

Chỉ chạy ca/fixture/đột biến đã có trong cây hoặc sửa runtime trên bản sao ngoài `cay-kho/`. Không tự soạn payload giả kênh hay lớp ngoại lệ đặc biệt mới. Các script đo của L2 được đọc và tái dùng trong `evidence/`; negative probe chỉ đổi đường từ hint sang HEAD. Probe bổ sung đổi thứ tự đọc stdin trên bản sao runner, không thêm payload: chính ca phản chứng hiện có giết mutation bằng tín hiệu của nó.

`python3 -B evidence/run_ab.py` dựng hai clone exact SHA rồi chạy hai vế trong MỘT lệnh, cùng env/TMPDIR/công cụ; mỗi vế chạy suite, mutation, credential theo thứ tự. Python 3.13.18, Ruff 0.16.9. Lệnh con/cwd/UTC start-end/rc/thời lượng ghi ở `evidence/{base,head}-{suite,mutations,credentials}.json`, output nguyên văn ở `.log`. Mọi import đo dùng `-B`/dont_write_bytecode; Ruff dùng no-cache.

`/tmp/.git` hiện hữu. Quyền ghi chỉ gồm workspace và `/tmp`, nên điều kiện TMPDIR ngoài `/tmp` của Linux A/B theo spec KHÔNG ĐO ĐƯỢC. Các ca t86/r858 thực tế bị từ chối ghi `/var/tmp`, ghi nguyên lỗi trong log. Không xóa/che `.git` hay thay kiểm tổ tiên. Windows exact HEAD, CI PR/check-run và gate hậu land chưa có hiện vật; không gọi mạng để lấy. CRLF/codec trên Linux không thay phép đo Windows. Kết quả đỏ ở hai vế được giữ nguyên và so theo tập tên, không đổi thành pass.

Giới hạn `RUNNER-CUNG-TIEN-TRINH`, gồm cố ý sửa tệp trên đĩa, giữ đúng quyết định chủ kho. Không có tuyên bố cô lập hoàn toàn Python cùng tiến trình. Không tìm thấy cửa giả thụ động thứ tư trong mã và các phép đo đã chạy; không kích hoạt điều kiện dừng vì tái diễn nguồn #1079.

## BANG NGHIEM THU

| Tiêu chí | Lệnh / phép đo | Output thật | Đạt? |
|---|---|---|---|
| Exact SHA/spec/trần/write set | `git rev-parse HEAD`; `git diff --numstat BASE HEAD`; `sha256sum SPEC.md SPEC-R1.md` | Hash như đầu báo cáo; 2 tệp, +326/-85; diff/numstat khớp byte | Có |
| N0 trên base r2 | `python3 -B evidence/probe_review.py` | Hai ca phản chứng chép nguyên văn vào base đều rc=1, HONG TinHieuChotCa, thấy sai `('giet','review_target')` | Có |
| A1: chặn giả lúc module init | Cùng script; nhóm wp1117 trong full mutation | Hai ca HEAD qua; env/argv/ghi sớm bị đúng ca đích giết | Có trong phạm vi đo |
| A2: runner thật trong cây | `python3 -B evidence/probe_copy_and_cli.py` | Neutral qua; 6 biến thể runner méo có sẵn đều `OK giet 1/1: r1117_cay_harness_chep_runner_that`, accounting `(0,0)` | Có |
| A3: stdin/import/chấm/ghi | `nl -ba cay-kho/.claude/dev/launcher_test_runner.py`; `probe_contract.py`; `probe_order.py`; `probe_copy_and_cli.py` | Đọc byte :44, dup2 :48, gọi đọc :62 trước nạp :72; chấm :77 trước ghi :78–79. Mọi alias stdin EOF; main HEAD không tạo kênh, base tạo. Đảo đọc sau import `OK giet 1/1` đúng ca phản chứng | Có |
| A4: giữ #1079 | `probe_review.py`; `probe_f03.py` | Các ca liên quan qua; nonce, stdout, tên lớp, tiền tố đều OK đúng ca; F01/F02 không tái mở | Có |
| A7: giữ (a)(b)(c) #1122 qua runner | `probe_review.py`; mutation 3 record map/qua/chi tiết | Ca lồng cùng tên/`__str__`, chi tiết TypeError + 160, qua/bo_qua không mang lỗi cũ đều qua; 3 mutation OK đúng ca | Có |
| Chốt kiểu record có witness đúng tín hiệu | `python3 -B evidence/probe_f03.py`; `probe_hint_negative.py` | Bỏ guard → đúng TinHieuChotCa; lỗi vô can → loi | Có, đóng F03 |
| A5 full suite cục bộ | `python3 -B evidence/run_ab.py`; `suite_summary.py` | HEAD 343/366, base 339/362, cùng 23 lỗi và 2 skip, rc=1 | Delta lỗi 0; chưa N/N sạch |
| A5 full mutation cục bộ | Cùng lệnh; `summarize.py` | HEAD 552/584, base 543/575; cùng 32 SAI, 4 không đo; rc=1 | Delta SAI 0; chưa M/M sạch |
| A5 credential | Cùng lệnh | Cả hai 13/18 đạt, cùng 5 lỗi, TỔNG: ĐỎ, rc=1 | Delta lỗi 0; chưa đạt |
| A6/A8 tĩnh | `python3 -B evidence/static_checks.py` | Bare Ruff F rc=1 mỗi vế, cùng 5 F841 cũ; delta chuẩn hóa 0. Doctrine rc=0: 10 tệp/0 chỗ; diff-check rc=0 | Đạt tiêu chí delta/tĩnh |
| A5 r2 Windows / CI exact HEAD / hậu land | Kiểm hiện vật đã cấp, không gọi mạng | not_run; không có log exact HEAD để xác minh | KHÔNG ĐO ĐƯỢC |

A3 tiêu chí âm literal r1 nói LT_KENH chỉ còn trong ca/đột biến, trong khi mục 2 yêu cầu lọc LT_KENH trong env. Bộ lọc và docstring tại `launcher_test.py:15412`/`:15419` phục vụ chính mục 2; không tính là finding. Main đã bỏ toàn bộ kênh và `loai_luot`. Các điểm còn lại được liệt kê trong `evidence/channel-references.log`. Ruff ở đây chỉ là bare lint, không khai đã kiểm workflow pin/probe contract hay CI.

## BANG DO

| Khẳng định | Diff / lời khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Áp nguyên HINT-L2 cho F03 | `diff-tu-l2.patch`, `HINT-L2.patch` | `static-comparison.json`: nội dung hai hunk bằng nhau sau bỏ header hunk có tên hàm | Có |
| F03 neutral 1/1, 7 mutation accounting `(0,0)` | Prompt executor | `probe_f03.py` đo lại bằng `chay_dot_bien` thật | Có |
| Kênh không có trong env/argv | Runner/cham_lap_ca | `probe_review.py`: argv 4 mục, stdin 2 dòng, env_channel_keys=[], channel_in_argv=false; kênh cha không tồn tại | Có trong phép đo |
| Lỗi ngoài không bị map/ca lồng đổi thành giet | Mục 8(a) | Ca r1122 qua; mutation đọc map bị ca đích giết | Có |
| Chi tiết loi giữ loại + 160; qua/bo_qua sạch | Mục 8(b)(c) | Ca r1122 và mutation tương ứng qua đúng giao thức runner | Có |
| Runner thật của cây lồng không bị tráo mà A2 vẫn xanh | Lệch spec đã duyệt | `probe_copy_and_cli.py`: cả 6 biến thể méo đều bị A2 giết; bỏ copy trong full mutation cũng OK | Có trong biến thể đo |
| Danh sách wp1117/neo lại đủ khớp nguồn | Mục 9, bảng DOT_BIEN_HARNESS | AST toàn ba bảng + kiểm neo và ca đích; không giới hạn theo prefix | Có với universe trong cây; không suy bao phủ mọi mutation có thể nghĩ ra |
| Không hồi quy full A/B | Executor đang đo khi giao review | Cùng 23 tên lỗi suite, cùng 32 tên mutation SAI, cùng 5 lỗi credential; HEAD_ONLY_FAILED=[] ở cả suite/mutation | Chỉ kết luận delta cục bộ; Windows/CI riêng |

Kiểm kê độc lập: `python3 -B evidence/inventory.py` dùng AST/literal_eval của toàn bộ `DOT_BIEN`, `DOT_BIEN_HOOK`, `DOT_BIEN_HARNESS`, so cả record/cặp thay/ca đích với base và L1, không chỉ lọc wp1117. Product 446→446, hook 79→79 không đổi; harness 54→63 gồm 12 ID mới, đúng 3 ID bỏ theo spec và 5 ID đổi (`wp1079_bao_cao_theo_ten_lop`, `wp1079_bo_tien_to_khac`, `wp1079_lap_ca_bo_kiem_nonce`, `wp1079_lap_ca_tin_stdout`, `wp1122_dinh_dang_lai_sau_ghi_map`). Cả 63 neo khớp đúng một chỗ sau loại bảng khỏi vùng thay; không có ca đích vắng. Đây là kiểm kê record đã viết; việc đọc thêm các nhánh runtime và probe thứ tự/khung/EOF/kiểu record dùng để kiểm ngoài danh sách ấy.

## BANG TEST

| Bộ | N/M, rc | Bỏ qua / giới hạn |
|---|---|---|
| HEAD full launcher | 343/366 qua; tổng 368; rc=1 | 23 lỗi, 2 skip |
| BASE full launcher | 339/362 qua; tổng 364; rc=1 | Cùng 23 tên lỗi và 2 skip |
| HEAD full mutation | 552/584 đạt; tổng 588; rc=1 | 32 SAI, 4 không đo |
| BASE full mutation | 543/575 đạt; tổng 579; rc=1 | Cùng 32 tên SAI và 4 không đo |
| Credential HEAD/BASE | Cả hai 13/18 đạt, cùng 5 lỗi, TỔNG: ĐỎ, rc=1 | Nền đỏ; credential mutation không chạy theo chính gate của bộ này |
| Ca tập trung HEAD | 38/38 qua | r1079/r1117/r1122; 0 skip |
| N0 base + hai ca nguyên văn | Hai ca 0/1, rc=1 đúng phản chứng | Không viết payload mới |
| Encoding base/L1/HEAD | 6/6, 4/6, 6/6 | 18 tổ hợp; không Windows |
| F03 cùng guard deletion L2/HEAD | SAI 0/1 → OK 1/1 đúng ca | Neutral qua; nhóm 7 mutant HEAD 7/7, 8/8 kết quả đích |
| F03 lỗi AttributeError vô can | loi, not_credited=true | Không chuyển lỗi vô can thành TinHieuChotCa |
| Runner contract | 11/11 đúng kỳ vọng | 3 frame hợp lệ, 5 frame lỗi rc=2/no channel; thiếu/trùng ca → loi; EOF 4 alias, không pyc |
| Lỗi nạp module | 2/2 đúng kỳ vọng | File thiếu/lỗi cú pháp: rc=1, không tạo kênh |
| Mutation thứ tự đọc stdin ngoài bảng | OK giet 1/1, accounting `(0,0)` | Đúng `r1117_khoi_tao_module_gia_kenh_roi_thoat_la_loi`; không thêm payload |
| Bản runner méo trong cây lồng | 6/6 mutation OK đúng A2 | accounting `(0,0)` |

Hai skip suite: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity`. Tập 23 lỗi chung: 10 đường `launcher.py run` nợ đã khai, 11 ca `r484_*` trong điều kiện `/tmp/.git`, 2 ca t86/r858 bị cấm ghi `/var/tmp`; tên/output đủ trong `suite-comparison.json`. Bốn mutation không đo: `124_khi_chau_con_song`, `g2_windows_directory_pin_access`, `g4_windows_LA_not_current_owner`, `g4_windows_sid_alias_not_normalized`. Toàn bộ output SAI và kết quả 12 mutation mới/5 mutation đổi nằm trong `mutation-results.json`; cả 12 mới và 5 đổi đều OK đúng ca. Năm lỗi credential chung: `t15_home_chua_tao_la_KHONG_DO_DUOC`, `t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra(OSError)`, `t18_kiem_ghi_dung_ban_da_probe(OSError)`, `t6_khong_in_gia_tri_khi_khong_co_co(OSError)`, `t9_cmd_lay_GHI_tep_huong_dan_dan(OSError)`.

## BANG SAN

| Hướng độc lập | Lệnh đã chạy | Output thật | Kết luận |
|---|---|---|---|
| 1. Đường có dấu với stdin ASCII/cp1258 | `python3 -B evidence/probe_review.py` | Base 6/6, L1 4/6, HEAD 6/6; codec mutation OK 1/1 | KHÔNG PHẢI LỖI hiện tại; giữ đóng F01 |
| 2. Mutation map còn neo vào ca cũ | Cùng script, phần MUTANTS | Base `(0,0)`, L1 `(2,0)`, HEAD `(0,0)`; hai mutant HEAD OK đúng ca nhật ký | KHÔNG PHẢI LỖI; giữ đóng F02 |
| 3. Bỏ kiểu record chỉ gây AttributeError | `python3 -B evidence/probe_f03.py` | L2 SAI 0/1, HEAD OK 1/1 đúng TinHieuChotCa; nhóm 7 HEAD `(0,0)` | KHÔNG PHẢI LỖI; đóng F03 |
| 4. Catch F03 cấp tín dụng cho lỗi vô can | `python3 -B evidence/probe_hint_negative.py` | `('loi', '...AttributeError: review unrelated AttributeError')`, not_credited=true | KHÔNG PHẢI LỖI trong đối chứng |
| 5. Module initializer tự công bố kết quả/thoát | `python3 -B evidence/probe_review.py` | Hai N0 base rc=1/HONG/giet sai, hai HEAD qua; env/argv/ghi sớm bị ca đích giết | KHÔNG PHẢI LỖI hiện tại theo mô hình thụ động |
| 6. Env/argv rò dữ liệu hoặc kênh cha bị ghi | Cùng script, ENVELOPE | env_channel_keys=[], stdin 2 dòng, channel_in_argv=false, parent_channel_exists=false | KHÔNG PHẢI LỖI trong phép đo |
| 7. Stdin/fd0 còn byte hoặc khung lỗi vẫn nạp | `python3 -B evidence/probe_contract.py` | Text/buffer/original/fd0 EOF; 0/1/3 dòng, nonce rỗng, UTF-8 lỗi đều rc=2/no channel | KHÔNG PHẢI LỖI |
| 8. Đọc stdin sau import không bị ca bắt | `python3 -B evidence/probe_order.py` | review_stdin_doc_sau_import OK giet 1/1 đúng ca phản chứng | KHÔNG PHẢI LỖI của ca hiện có |
| 9. Thiếu/trùng ca bị chọn đại; nạp lỗi vẫn có kênh | `probe_contract.py`; `python3 -B evidence/probe_extra.py` | 0/2 match → loi; FileNotFoundError/SyntaxError rc=1/no channel | KHÔNG PHẢI LỖI trong phép đo |
| 10. Runner cây lồng lấy nguồn méo mà A2 xanh | `python3 -B evidence/probe_copy_and_cli.py` | 6/6 biến thể có sẵn OK giet 1/1 đúng A2 | KHÔNG PHẢI LỖI trong biến thể đã đo |
| 11. Ca lồng cùng tên/`__str__` thay loại hoặc thông điệp ngoài | `python3 -B evidence/probe_review.py` | r1122_kenh_loi_phai_thuoc_luot_ngoai qua, mutation đọc map OK đúng đích | KHÔNG PHẢI LỖI |
| 12. Qua/bo_qua mang lỗi cũ; chi tiết mất loại/cắt sai | Cùng script | Các ca r1122 qua, gồm TypeError + 160 và OSError transport; mutation qua/map/chi tiết OK | KHÔNG PHẢI LỖI |
| 13. Full A/B phát sinh lỗi mới ngoài tập nhắm | `python3 -B evidence/run_ab.py`; `suite_summary.py`; `summarize.py` | Cùng 23 tên lỗi suite, cùng 32 tên mutation SAI, cùng 5 lỗi credential; HEAD_ONLY_FAILED=[] ở cả suite/mutation | KHÔNG PHẢI LỖI hồi quy trong điều kiện A/B cục bộ; không suy gate xanh |
| 14. Windows/CI/hậu land exact HEAD | Không gọi mạng; kiểm bundle được cấp | Không có log Windows exact HEAD/check-run/hậu land | KHÔNG ĐO ĐƯỢC |

## Toàn vẹn và bàn giao

Snapshot đầu/cuối bao phủ 10,814 tệp ngoài `.git`, gồm tracked/untracked/ignored: không delta byte, HEAD/tree/status khớp, index khớp HEAD ở cả hai mốc. Xem `snapshot-comparison.json`. Snapshot chứng minh không có delta ở hai mốc, không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox là workspace-write; checkout được đối xử read-only theo vai review, không tuyên bố mount toàn cây nguồn chỉ đọc.

Không còn finding P0/P1/P2/P3 trong phạm vi đã review; F01/F02 giữ đóng, F03 được đóng trên exact SHA này. `approve` là kết luận review mã nguồn, không xác nhận các gate chưa đo đã đạt và không cấp quyền merge/land. Required Windows exact HEAD, CI/check-run và hậu land vẫn cần executor/điều phối đọc lại riêng theo spec. `HINT.patch` rỗng vì không có bản vá đề nghị mới. Không sửa `cay-kho/`, không push, không gọi mạng. Hiện vật đo giữ trong `evidence/`.
