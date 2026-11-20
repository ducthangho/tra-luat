Review wp1236 r9, đợt A, lượt 6: **changes_requested**. Còn **1 P2 và 2 P3**, thuộc **2 lớp mở**, với **27 biểu hiện** (25 mutant không tương đương, một fixture CLI thiếu, một mô tả lệch). Review class `sensitive` đòi đóng cả P3; chưa có miễn trừ neo SHA cho chúng.

`reviewed_sha: c2d606bb6fc230c288200b8f1dd79715462c172b`  
`tree: 9b78e9e0b1e1d445e19747e65ab4f65ea4016511`  
`spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8`  
Baseline `0f9aa2a2cc697129e1f5be72feddf60986286865`; spec nguồn `176feba3a09a4e86c6d8b06487f3e4224571be51`, revision 9/generation 1. Repo, lease và write set đều khớp; đúng 3 tệp, +1324/−0 ≤1400.

Lịch sử được dựng lại từ cả năm verdict đã giao; mỗi finding cũ thuộc đúng một lớp. Các probe cũ được tái dựng theo biến đổi/fixture mô tả trong verdict; không có các script scratch cũ trong gói đầu vào. Bằng chứng mới đều chạy trên HEAD này.

| Lớp | Finding cũ và lượt | Trạng thái trên HEAD | Bằng chứng độc lập |
|---|---|---|---|
| `yaml-ngoai-schema-bi-chan` | F01, lượt 1 | `DA_VA_THAT` | Năm dạng YAML ngoài schema giữ passed; m54 đỏ đúng a116. |
| `k2-mat-loi-doc` | F02/G01, lượt 1–2 | `DA_VA_THAT` | YAML/UTF-8 hỏng, symlink tệp/thư mục, lỗi scandir và 0/1/2 provenance chặn đúng; m55/m56/m59/m70 đỏ đúng ca. |
| `cli-vong-yaml-traceback` | F03/H02, lượt 1/3 | `DA_VA_THAT` | Vòng alias và stat tệp/thư mục quá dài đều rc2 không traceback; alias chia sẻ vẫn duyệt được; m57/m58/m65 đỏ đúng ca. |
| `test-thieu-chot` | F04/G02/H01/J01/J02/K01/K02, lượt 1–5 | `VA_MOT_PHAN` | 20 mutant đại diện biểu hiện cũ đã bị giết đúng ca; lớp còn các biểu hiện L01/L02. |

[prior_probes.json](prior_probes.json), [prior_replay_map.json](prior_replay_map.json), [audit_mutants.jsonl](audit_mutants.jsonl) và bảng nối đầy đủ trong [VERDICT.json](VERDICT.json) giữ nguồn từng lượt/SHA. Lớp test xuất hiện cả sáu lượt; hai chuyển tiếp 4→5 và 5→6 đều F/U=0/1. Lớp mới L03 không nằm trong mẫu số này. Cần trả bằng chứng về checkpoint §12 để xét tiếp cách làm; thay phương pháp quét không xoá lịch sử lớp.

**L01 · P2 · `test-thieu-chot`**, tại `ops/gate_output_doi_chieu_test.py:437,445,545,712`. Hai mươi mutant làm sai quyết định hoặc ném ngoại lệ đều qua đủ 36 ca với mã thoát từng ca bằng 0. Các nhóm đã quét:

- `is True` ở dạng gốc/packet và khối ngày đổi thành `== True`: số 1 bị coi là landed, sinh chặn oan.
- PHI_LOI_KHAI bị mở rộng theo chuỗi con hoặc ngừng duyệt bên trong metadata: bỏ sót lời khai phải kiểm.
- Bỏ chữ số khi chuẩn hoá khoá, mở TOKEN để nhận `pass`, nới phần run/đuôi tệp: nhận sai hoặc chặn oan theo đối chứng.
- Bỏ sáu dấu phân cách được phép: `—`, `-`, `(`, `,`, `.`, `;`. Mutant bỏ `:` đã bị a202 bắt và được tính GIẾT.
- Dòng miễn chỉ khớp tiền tố, bỏ strip, hoặc kiểm head bằng truthiness: nhận miễn sai hoặc từ chối dòng hợp lệ.
- Hai biến thể không giữ điều kiện bắt buộc có URL: một bản nhận hồ sơ landed chỉ khai owner_waived mà không có URL; bản kia ném TypeError qua kiem_ho_so. Mã gốc trả đúng vi phạm `waiver_khong_co_can_cu:url` và `landed_khong_loi_khai_gate_output`.

Đối chứng ở [independent_contrasts.json](independent_contrasts.json), [extra_contrasts.json](extra_contrasts.json), [real_waiver_matrix.json](real_waiver_matrix.json). Ma trận miễn cuối dùng bản sao readback thật pr1340, lưu hash nguồn; chỉ sửa bản sao. Cách vá chung: ma trận nghĩa độc lập từ spec cho tập giá trị, grammar, kiểu, 0/1/2 URL và đường đi qua consumer; giữ cặp dương/âm, thêm mutant tương ứng và phân loại riêng tương đương/lỗi vô can. Cần bảo vệ đầu vào hợp lệ khi bổ sung ca, không siết luật sản phẩm để làm oracle xanh.

**L02 · P3 · `test-thieu-chot`**, tại `ops/gate_output_doi_chieu_test.py:167,545,590`. Năm mutant sống chỉ đổi chẩn đoán: skipped v3 có hậu tố (`dong_la`→`co_job_skipped`) và bốn cặp ưu tiên miễn (`html_url`→`tac_gia`, `tac_gia`→`dong_mien`, `han`→`os`, `os`→`sha`). Chúng vẫn từ chối nhưng sai lý do cố định. A2-10 còn thiếu T-khong-prov: trace a210 là **5 fixture thật**, fixture thứ sáu gọi trực tiếp ra rc3 đúng. Bổ sung ca skipped v3, bảng lỗi đồng thời/các đối chứng đơn lỗi và đủ sáu fixture CLI; giữ thứ tự luật theo spec. [cli_acceptance.json](cli_acceptance.json) lưu lời gọi thực tế.

**L03 · P3 · `mo-ta-duong-dan-lech-hop-dong`**, tại `ops/gate_output_doi_chieu.py:224`. Docstring khai cấm `.`; `PurePosixPath` chuẩn hoá thành phần đó và `./tệp` được nhận. Đặc tả A chỉ cấm `..`, tuyệt đối và symlink. Sửa mô tả cho đúng, giữ hành vi A; chốt đóng bằng đối chứng `./tệp` đạt và các ca `../`/symlink tiếp tục bị chặn. [dotpath_probes.json](dotpath_probes.json). Đây là biểu hiện lệch đo được sau khi rà các docstring/mô tả ràng buộc của module.

Bộ quét được kiểm ở hai mức, không dùng tổng đột biến để suy đóng lớp:

| Phép đo | Kết quả |
|---|---|
| Tái sinh/chạy lại bộ AST tại 89fb99b, bộ ca tại chính mốc ấy | 381; 51 không có tín dụng GIẾT: 45 sống sạch, 6 lỗi vô can |
| Tái sinh/chạy lại bộ AST tại HEAD | 368; 362 GIẾT, 6 lỗi vô can; không còn bản sống sạch trong tập AST đó |
| Xác minh riêng | 362/362 chết đúng ca đích không patch/cache YAML; sáu bản còn lại chạy đủ 36 ca bằng SafeLoader có memo/deepcopy, không có tín dụng giết hợp lệ, có rc4; k339 chết tại a217 nhờ m124 |
| Thước độc lập mở rộng | **127 mutant: 93 GIẾT, 34 SỐNG** |
| Phân biệt 34 bản sống | **9 tương đương trong miền đầu vào; 25 làm khác hành vi** |
| Kiểm lại 25 bản làm khác hành vi | **36/36 ca rc0 cho từng bản**, không patch/cache YAML |

[all_independent_results.json](all_independent_results.json) liệt kê mọi toán tử và kết quả ca; nguồn bản sao ở `independent_mutants.jsonl`, `independent_corrected.jsonl`, `extra_mutants.jsonl` và `order_url_mutants.jsonl`, `reason_complete_mutants.jsonl`; [measurement_summary.json](measurement_summary.json) liệt kê đầy đủ 20 ID P2 và 5 ID P3; [semantic_native_full.jsonl](semantic_native_full.jsonl), [order_url_results.jsonl](order_url_results.jsonl) là kết quả không cache. Tập 102 ban đầu giữ SafeLoader và memo/deepcopy; hai lỗi của script đo riêng (trùng ID và sửa nhầm ngoặc regex) đã được loại, sửa và chạy lại. Quét bổ sung đủ 43 vị trí literal lý do cố định (kể cả append/comprehension/nhánh điều kiện), 20 bản bổ sung đều chết trên loader gốc không cache; xem `reason_census.json` và `reason_complete_results.jsonl`. Chín bản tương đương không tính thành finding; tám phép is/== trên giá trị parser/Path/regex chuẩn cùng một lookbehind dư được giải thích trong [equivalence.json](equivalence.json), với 20.736 đối chứng tên tệp không lệch. Hai phép is True không tương đương đã được giữ trong L01.

`quet/sinh.py` chỉ sinh phủ định/loại vế, thay số/bool và return; bỏ qua hằng chuỗi, regex, tập ở mức module, ưu tiên lỗi và thay is bằng ==. `chay_ca.py` dừng ở ca đầu rc3; `chay.py` không lưu child rc và không tự chứng minh baseline. C loader của scanner **đổi ngữ nghĩa**: tab sau colon/cuối dòng trong bản sao provenance bị SafeLoader từ chối nhưng CSafeLoader nhận; các escape Unicode cũng đổi kết quả/lớp ngoại lệ. [yaml_parity.json](yaml_parity.json). Vì vậy tín dụng của 362 bản đã được xác minh lại bằng tiến trình ca đích dùng loader sản phẩm. Sáu rc4 không phải SỐNG xanh và không được cấp tín dụng GIẾT.

| Kiểm bắt buộc / hợp đồng | Kết quả và giới hạn |
|---|---|
| Suite Python3.13.18/PyYAML6.0.3 | rc0; `CA: 36/36 dat`; `DOT BIEN: 124/124 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT` |
| Suite Python3.12.3/PyYAML6.0.1 | Cùng bốn dòng, rc0; cả hai stdout khớp regex đăng ký |
| Audit 124 mutant khai trong suite | 124/124 TinHieuChotCa ở đúng ca đích. Một số chỉ chứng minh chẩn đoán: m6→KeyError; m22/m23/m79 còn K2 symlink; m80→FileNotFoundError; m96–m100 kiểm tên lỗi kiểu. |
| Ruff bare, đúng ba tệp, --no-cache --select F | rc0, All checks passed; Ruff0.15.15 |
| ci_dang_ky_test.py | rc0;31/31;Ruff CI contract3/3;1226/1226 phản chứng |
| Corpus tại immutable base0f9aa2a |66 tệp=47/10/9;170 hồ sơ=25/56/39/50;94 landed,0 lệch;50 script=20/28/2 và đúng ba băm BO_SINH |
| Consumer độc lập |1 đối chứng dương+21 biến thể; không tìm thấy lời khai dương lọt ngoài giới hạn r9 |
| Bốn rút gọn so89fb99b |27 đối chứng khớp; xem [simplifications_probes.json](simplifications_probes.json) |
| K1–K8 và mọi API/hằng/tên lý do/CLI của Module mới | Đã đối chiếu; các counterexample đo trên HEAD xử lý đúng. L01/L02 thuộc bộ nghiệm thu; L03 thuộc mô tả helper. L8/D2b là đợt B/C. |
| Diff/check/trần |3 tệp,+1324/−0≤1400;diff --check rc0 |

Đối chiếu chi tiết mục *Module mới* (đọc mã và đặc tả, kết hợp probe độc lập với audit ca đích):

| Phần | Hành vi và tên lý do đã đối chiếu | Bằng chứng |
|---|---|---|
| Hằng | BO_SINH đúng ba SHA/nhãn; CHECK_BAT_BUOC_TEN đúng năm tên; PHI_LOI_KHAI đúng ba tên; TOKEN đúng bảy giá trị | corpus/producer_contrasts; a104/a109/a201/a202; quét thay/bỏ từng thành viên |
| doc_danh_gia/K1 | UTF-8, LF/CRLF; fullmatch header/job/skip/tổng; `khong_phai_utf8`, `xuong_dong_tron`, `cr_le`, `dau_tep_sai`, `dong_la`, `job_lap`, `thieu_moc`, `moc_lap`, `bo_sinh_la` | a103/a104/a118; các mutation lý do; skip v3 thiếu ca riêng ghi L02 |
| chon_provenance/K2 | schema và bộ ba run/attempt/head, số int nghiêm, không theo symlink; `symlink`, `provenance_0`, `provenance_nhieu` | prior, consumer_matrix, a108/a116/a117/a118 |
| K3 | push/ci.yml, cờ run/tập job/checkout khác rỗng, ngoại lệ checkout skipped đúng job; `khong_phai_run_land`, `provenance_chua_du` | consumer_matrix, a108/a114/a119 |
| K4 | ID trùng và tập job/skip chính xác; `job_id_trung_provenance`, `tap_job_lech`, `tap_skip_lech` | consumer_matrix, a107/a117 |
| K5 | name/conclusion/labels, kết luận tương thích trạng thái; `job_lech:<id>`, `ket_luan_lech:<id>` | consumer_matrix, a106/a113; rút gọn tương đương đại số |
| K6 | băm dòng khớp str(băm provenance); `log_sha_lech:<id>` | consumer_matrix, a105 |
| K7 | skip đúng phiên bản, tính ba thành phần tổng; `dong_skip_sai_phien_ban`, `moc_lech` | a110/a111/a119 và corpus |
| K8/kiem_tep | failed trước skipped/check; `co_job_skipped`, `check_bat_buoc:<tên>`; gom lỗi K3–7, ngoại lệ → not_measured/TênNgoạiLệ | a109/a112/a115, prior, audit 124 |
| loi_khai/_chuan | casefold, giữ chữ và số, mọi độ sâu/list; loại đúng tên nhưng vẫn duyệt con; vòng alias bị chặn | prior, a201/a214; L01 là lỗ hổng test, mã gốc đúng |
| token/tep_danh_gia | đúng regex đóng băng, casefold/tập token; trích mọi tên tệp, kể cả nhiều tệp | independent_contrasts, a202/a207; L01 là lỗ hổng test |
| la_landed | is True ở ba dạng; ưu tiên có khoá packet; fullmatch khối ngày | corpus 94/170 lệch 0, independent_contrasts, a212/a213/a215 |
| _tep_trong/kiem_ho_so | tương đối provenance, cấm tuyệt đối/../symlink; mọi tệp phải khớp trạng thái; token âm không tạo lời khai hợp lệ; `dinh_dang_loi_khai`, `duong_khong_tep_danh_gia`, `tep_danh_gia_khong_hop_le`, `danh_gia_khong_passed/failed`, `waiver_khong_co_can_cu`, `landed_khong_loi_khai_gate_output` | consumer_matrix, dotpath, a203–a208/a212/a215/a216; docstring sai ở L03 |
| kiem_mien | đúng một URL/readback/dòng strip+fullmatch; chủ kho/OWNER; ngày lịch, ubuntu, head khác None so trực tiếp; thứ tự `url, readback, doc_readback, html_url, tac_gia, dong_mien, han, os, sha` | real_waiver_matrix, a209/a215; thiếu ca biên/thứ tự ghi L01/L02 |
| CLI/main | kiem-tep 0/1/3, sai tham số 2; kiem-ho-so 0/1/2, nhiều hồ sơ giữ lỗi; help 0; không traceback | prior, a210/a214/a217; A2-10 thiếu fixture thứ sáu ghi L02 |

K5 rút gọn tương đương đại số: vế `tt==passed && conclusion!=success` đã nằm trong `conclusion!=success && tt!=failed`. `os.walk(followlinks=False)` vẫn không đi vào symlink khi bỏ lọc thu[:]. Các đối chứng glob trên thư mục vắng/tệp/symlink và body JSON falsy/chuỗi miễn hợp lệ đều giữ kết quả. Không thấy regression từ bốn rút gọn.

CI khai Python3.12, PyYAML6.0.3, fetch-depth0; các OID archive đều có trong ancestry đã cấp, symlink POSIX chạy được. Không thấy ca cần thứ vắng trong CI đã khai. `skipped`:0 trên Linux; `not_run`:Windows và CI từ xa/full release/land gate. Những phần log thật, provenance/readback sửa tay, danh tính người gõ và neo commit hồ sơ khác được giữ đúng giới hạn `chua_do_duoc`/`ngoai_pham_vi` của r9.

Reviewer `openai_codex / codex_cli / machine`, họ `openai` theo identity provider, run `887066e7bed94b84824ef0613a0acaf4`; model/effort phục vụ `KHONG_DO_DUOC`. Executor theo lease: `anthropic_claude / claude_code / machine/local`, phiên `session_015GtxrYsNDbfLo32S39f5uY`. Sandbox khai `workspace-write`; repository được giữ read-only bằng thao tác, không GitHub/mạng/commit/push. Hash 17,333 tệp đầu/cuối, kể cả ignored .codex, khớp; HEAD/tree và diff index không đổi. Snapshot không chứng minh lịch sử ghi rồi hoàn nguyên; repo nguồn ngoài checkout không được quan sát.

Các lệnh/script và output đầy đủ nằm cạnh báo cáo; stdout/stderr có mã thoát thật, phân biệt tín dụng GIẾT, SỐNG và lỗi vô can. JSON đã kiểm bằng `kiem_verdict_lop.py --vong 6`; kết quả lưu ở [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
