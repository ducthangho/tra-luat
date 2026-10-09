# Cross-review độc lập — packet #668, lượt 5

Trạng thái lúc mở: dang_review; đã hoàn tất, kết luận ở cuối.
reviewed_sha: ef01112604ef47096daf99ee2470125c3ca0f0b3

Đột biến chỉ thực hiện trên bản sao `/tmp`. Các ca ký tự điều khiển/ẩn dùng nguyên bộ phản chứng có sẵn; không tự tạo payload mới.

HƯỚNG 1: Neo và môi trường review
  giả thuyết : Bundle đúng head/spec/write set được cấp.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; sha256sum SPEC.md; git status --porcelain=v1 --ignored; cat numstat.txt
  output     : HEAD ef01112604ef47096daf99ee2470125c3ca0f0b3; tree 3777b0b21b18723a04b3e0ae1be87e42b39a656b; spec dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; status rỗng; 5 tệp +1127/-31.
  kết luận   : KHÔNG PHẢI LỖI. Trần ~1.400 và quyền tiếp tục sau S3 lấy từ prompt hiện tại.

HƯỚNG 2: Phân biệt lỗi sandbox và lỗi packet
  giả thuyết : Repo-local commit.gpgsign=false đủ cho cả các kho git tạm do ca tạo.
  lệnh       : python evidence/env.py python .claude/dev/ci_dang_ky_test.py (cwd bản sao); probe git commit --allow-empty trong TemporaryDirectory.
  output     : registry lượt đầu rc=1: git commit rc=128; signing helper không nối được socket. t47 ở phép bán kính ban đầu bo_qua vì INDEX chỉ có stage 0.
  kết luận   : KHÔNG PHẢI LỖI sản phẩm. Kho con không thừa kế config repo cha. Harness reviewer thêm GIT_CONFIG_COUNT để đặt commit.gpgsign=false/core.abbrev=7 cho git con; giữ log lần đầu và đo lại. Lượt đầu không được tính là đủ 1/56 sạch.

HƯỚNG 3: Workflow F1/F3/F10 — ca sẵn có và gỡ chốt
  giả thuyết : Chốt toàn thân run đóng khác biệt tách dòng và nội suy, không chỉ vá từng payload.
  lệnh       : python evidence/env.py python -u evidence/workflow.py; python .claude/dev/ci_dang_ky_test.py trên bản sao (env.py).
  output     : control F1 20/20, F3 28/28, F10 7/7 đỏ đúng; registry 1020/1020, TỔNG ĐẠT. Gỡ F10 làm cả 7 F10 lọt; chỉ trả splitlines không làm ca F3 lọt vì chốt ký tự vẫn đứng trước. Gỡ cả hai được lưu trong workflow-summary.json. Gỡ bộ kiểm ngữ nghĩa làm 18/20 F1 lọt; hai ca workflow defaults/env vẫn bị chốt độc lập bắt.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi đã đo. Hai hàng rào độc lập cho F3 là hiệu quả thật. Không tự soạn payload ký tự ẩn/điều khiển.

HƯỚNG 4: Hồi quy ngoài lớp main
  giả thuyết : Các thay đổi không gây delta ở t152/lease subset/actionlint/Ruff F và probe công cụ.
  lệnh       : python evidence/env.py python -u evidence/regression.py
  output     : head/base đều t152 PASS; lease t24/t31/t35/t161/t162 PASS; actionlint rc=0; probe rc=0; Ruff bare F rc=1 cả hai (delta chi tiết = 0).
  kết luận   : KHÔNG PHẢI LỖI với các phép đã ghi. Không đồng nhất bare lint rc=1 với pass; sẽ chốt delta riêng. Lần đầu lease subset thiếu sys.path ops là lỗi harness, đã sửa và chạy lại đầy đủ.

HƯỚNG 5: MỚI — danh tính từng CA, không chỉ số lời gọi
  giả thuyết : Nhật ký nguyên vẹn phải phân biệt gọi đủ 56 ca với gọi một ca hai lần và bỏ một ca khác.
  lệnh       : python evidence/env.py python -u evidence/main_matrix.py; python evidence/env.py python evidence/wiring.py
  output     : ca_duplicate_middle thay vòng CA bằng CA[:3] + [CA[2]] + CA[4:]: t54 qua; bước đo ban đầu còn t47 bo_qua do sandbox, đo riêng t47 trên đúng mutant sau sửa env trả qua. wiring: control fourth_ca_red rc=1 calls=56 unique=56 case_3=1; mutant rc=0 calls=56 unique=55 case_3=0.
  kết luận   : LỖI (P2), F12, nối lớp F2/F5/F6/F7. `ca_gia` chỉ log "ca", rồi nén chuỗi và đếm; các lỗi giả chỉ kích hoạt đầu/nhì/cuối. Không quan sát danh tính ca giữa. Đây là lỗ bộ tự kiểm; không khẳng định head chưa đột biến đang bỏ ca.

HƯỚNG 6: MỚI — lỗi ở đầu luồng, kết quả cuối xanh
  giả thuyết : Tự kiểm main phải bắt mất lỗi đã tích luỹ khi đọc nhiều kết quả bán kính.
  lệnh       : python evidence/env.py python -u evidence/main_matrix.py; python evidence/env.py python evidence/wiring.py
  output     : đối chứng main thật với transport giả: chuỗi [lỗi=1, lỗi=0] control rc=1, mutant `loi_db = loi` rc=0; tự kiểm phân hạng đỏ + bán kính xanh cũng control rc=1, mutant rc=0. Kịch bản `du` hiện trả đúng một phần tử, lỗi tự kiểm riêng chỉ được kích thích ở gate. Đo đủ 56 CA: mutant sống, sau đo bù t47.
  kết luận   : LỖI (P2), cùng F12: mutant sống qua toàn bộ CA; bằng chứng dây nối chứng minh hậu quả.

HƯỚNG 7: Cửa thực thi CLI — F8 chưa bao hết __main__
  giả thuyết : Ca gọi `_main_gop()` trực tiếp có thể bỏ sót dây nối từ CLI vào helper.
  lệnh       : python evidence/env.py python -u evidence/entrypoint.py
  output     : RADIUS 56 {} (56/56 qua, không bỏ qua/tín dụng giả); thay duy nhất `sys.exit(_main_gop())` bằng `sys.exit(0)` trong bản sao. Chạy CLI thật `--gop <thư mục rỗng>`: control rc=1 có [G-rong]; mutant rc=0 stdout rỗng.
  kết luận   : LỖI (P2), F13 nối F8. Bốn đột biến f8_* gác helper nhưng không gác dispatcher mà workflow thực thi. Đã chứng minh với đúng CLI, không thêm cờ lạ và không cần payload.

HƯỚNG 8: Gom — phân hoạch và thứ tự độc lập tên tệp
  giả thuyết : Gom phải nhận bộ hợp lệ ở mọi N=2..16 khi đảo thứ tự bản ghi/đổi tên tệp, và từ chối đầu vào filesystem sai.
  lệnh       : python evidence/env.py python evidence/new_paths.py
  output     : 15/15 N có 281 bản ghi, rc helper=0; symlink rc=1 [G-tep]; đích ghi là directory ném IsADirectoryError (không xanh). Bản ghi giả với mọi ca ngoài đích bo_qua được gom nhận: lỗi đột biến=0.
  kết luận   : KHÔNG PHẢI LỖI mới của packet. Đây là fixture dữ liệu, không phải 281 đột biến đã đo thật. `bo_qua` ngoài đích là giới hạn của bộ kết luận kế thừa, cần đối chiếu baseline trước khi phân loại; không lấy nhãn bán kính 1/56 của bộ giả làm bằng chứng đã đo 56 ca.

HƯỚNG 9: MỚI — shell vắng không đồng nghĩa Bash trên Windows
  giả thuyết : `_loi_thuc_thi_g5` coi `b.get("shell", "bash")` là Bash, nhưng Windows dùng shell mặc định khác.
  lệnh       : python evidence/env.py python evidence/workflow_shell.py; registry trên clone /tmp/review668-r5-shell chỉ bỏ shell ở bước G5 mảnh.
  output     : Bỏ shell riêng từng bước G5 ở gate/mảnh/gom đều `loi_g5_workflow=[]`, actionlint rc=0. Không có pwsh trong sandbox; chưa thực thi PowerShell hoặc Windows runner.
  kết luận   : LỖI (P2), F14 nối lớp F1/F3/F10: miền ngữ nghĩa thực thi chưa đóng. Bước probe + selftest của gate/mảnh có hai chương trình native; không ghim Bash thì mất bảo đảm dừng ở lỗi chương trình đầu. Head hiện tại có shell:bash đúng, lỗ nằm ở validator chấp nhận hồi quy này.

  Căn cứ và giới hạn F14: GitHub quy định shell mặc định Windows là pwsh; phần bao PowerShell dùng mã thoát native cuối. Microsoft ghi `$PSNativeCommandUseErrorActionPreference` mặc định false. Do đó suy luận: probe trả khác 0 nhưng selftest sau trả 0 có thể che lỗi probe ở cấu hình mặc định. Đây là suy luận từ nguồn sơ cấp + phép đo validator/actionlint, không khai đã tái hiện runner. Không dùng bước gom một lệnh để khẳng định nuốt lỗi; hậu quả có ý nghĩa nằm ở hai bước hai lệnh gate/mảnh.
  Nguồn: [GitHub shell và exit codes](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell), [Microsoft native error preference](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables?view=powershell-7.5#psnativecommanduseerroractionpreference).

  Chốt HƯỚNG 9: registry THẬT trên clone bỏ duy nhất `shell: bash` ở G5 mảnh vẫn rc=0, PHẢN CHỨNG 1020/1020, TỔNG ĐẠT (`evidence/registry-shell.log`). F14 không chỉ lọt helper riêng.

  Chốt HƯỚNG 4: Ruff 0.15.15, `check --no-cache --select F` trên đúng W1/W3/W4: head/base đều 6 F841 (5 launcher, 1 cong_cu_test), khớp từng đường/tên biến/thông điệp; delta=0. Bare lint cả hai rc=1 do nợ nền. Actionlint 1.7.7 cả hai rc=0. F11 ĐÃ VÁ THẬT: workflow có đúng 5 dòng AL_VER, chú thích workflow:543 và hook:64 đều ghi 5; t152 chạy thật PASS trên cả hai cây.

  Chốt HƯỚNG 8: gọi `_ket_luan_ban_kinh` tại baseline f8a7829 với đích giet_that + mọi ca ngoài đích bo_qua cũng trả lỗi=0, "bán kính 1/53". Đây là giới hạn kế thừa, không phải đường mới do gom tự nới. Không báo thêm finding packet cho chính sách có từ baseline này.

HƯỚNG 10: Gate trọn chế độ giao mảnh, F8/F9 và toàn bộ bán kính mới
  giả thuyết : Gate vẫn chạy đủ CA/cổng cây thật/tự kiểm; 69 đột biến chính thức giết riêng đúng đích; mẫu cũ không lan sang 3 ca mới.
  lệnh       : python evidence/env.py bash -c 'cd /tmp/review668-r5 && CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py'; python evidence/env.py python -u evidence/radii.py new; ... radii.py old; ... complete_t47.py; ... summarize.py
  output     : gate-retry rc=0, 56/56, bỏ qua=0, tiền kiểm bỏ qua=0; CỔNG TRÊN CÂY THẬT ĐẠT; lỗi đột biến=0, 281 đột biến giao mảnh. Mẫu cũ TOTAL 9 ERRORS 0; mọi t52/t53/t54 đều qua. Đo 69 mới đã hoàn tất; kết quả và phép đo bù được chốt bên dưới.
  kết luận   : KHÔNG PHẢI LỖI ở gate và mẫu cũ đã đo. Phạm vi gate là chế độ M1 giao mảnh, không phải CLI mặc định chạy đủ 281 đột biến. Phép đo nguồn F9 và các mutant riêng sẽ được chốt theo kết quả đầy đủ bên dưới.

  Bổ sung HƯỚNG 6: `evidence/main-extra.log` có `full_first_only {}`: chỉ xét kết quả đầu của vòng bán kính vẫn qua 56/56. `wiring-more.py` đặt kết quả đầu xanh, kết quả cuối đỏ: control rc=1, mutant rc=0. Ca tự kiểm nhánh đủ đang trả một phần tử nên không phân biệt xét hết với cắt luồng. Đây là biểu hiện thứ ba có hậu quả trong F12, cùng cơ chế mô hình nhật ký làm mất thông tin.

  Bổ sung HƯỚNG 7/8: `cli_positive.py` chạy CLI thật trên bộ fixture 8 mảnh: rc=0, 281 dòng ok, GOM MẢNH 8/8. Thiếu/thừa đối số đều rc=2 [G-doi-so]. Không tính fixture này là A1 vì bản ghi do `_ban_ghi_du_gia` tạo.

  Bổ sung HƯỚNG 4: registry baseline rc=0, 938/938 phản chứng; head rc=0, 1020/1020. Chỉ định lượng phần registry tự kiểm, không chạy `--chay` toàn bộ registry suites (khác phạm vi gate G5).

Bảng kiểm độc lập các quyết định và dữ liệu của `main()`:

| Quyết định / dữ liệu truyền đi | Phép đổi trong ma trận | Điều quan sát |
|---|---|---|
| Cấu hình sai dừng trước CA | config_ignore | t54 giết |
| Cả hai tiền kiểm đúng hàm | batch_skip, alias_skip | t54 giết riêng |
| Gọi đủ CA; danh tính và thứ tự | ca_skip, ca_duplicate_middle, ca_reverse | Bỏ toàn bộ bị giết; thay một ca bằng ca lặp sống (F12); đảo thứ tự sống, chưa chứng minh hậu quả |
| Phân biệt AssertionError / Exception / BoQuaMoiTruong | assert_ignore, exception_ignore, skip_as_red | t54 giết |
| Bộ đếm đạt/bỏ qua | pass_counter, skip_counter | Sống; stdout không được kiểm, thuộc điểm mù quan sát F12 |
| Chọn nhánh mảnh | shard_never | t54 giết |
| Lấy k/N/đường ra và phân hoạch | shard_k, shard_n, shard_ra, partition | t54 giết |
| Nền đỏ HOẶC tiền kiểm bỏ qua | base_red_ignore, precheck_ignore | t54 giết |
| Dọn tệp khi nền đỏ, chuyển vân tay, trả lỗi | no_cleanup, cleanup_fp, bad_base_rc | t54 giết |
| Phóng con: tập tên, nền rỗng, worker | launch_names, launch_baseline, launch_workers | t54 giết |
| Nhận: nhóm, rc, stdout, nền rỗng | receiver_group, receiver_rc, receiver_output, receiver_baseline | Ba phép đầu bị giết; thay nền bằng tên không thuộc CA tương đương trên tập CA hợp lệ. Thay bằng tên CA thật bị t54 giết (`target-probe.log`) |
| Thực sự gọi bộ nhận | receiver_skip_call | t54 giết |
| Giữ lỗi nhóm, nhận hết nhóm | no_reason, break_on_error | Bỏ lỗi bị giết; break khi đã lỗi sống nhưng vẫn đỏ/không ghi, không lấy nó làm lỗi xanh sai |
| Hợp nhất đủ nhóm và giá trị | drop_group, drop_values | t54 giết |
| Gọi writer, truyền k/N/ra/tên/ket/ly/vân tay | writer_skip, writer_k/n/ra/names/ket/reason/fp | t54 giết |
| Lỗi writer → rc mảnh | writer_rc | t54 giết |
| Trình bày kết quả writer | print_writer_drop | Sống; stdout bị bỏ khỏi phép so nhật ký |
| Gọi cổng cây thật trên GOC | gate_skip, gate_root | t54 giết |
| Tự kiểm phân hạng, giàn giáo; cộng lỗi | classifier_skip, scaffold_skip, scaffold_reset | t54 giết |
| Tập nền đỏ và đầu vào báo cáo | baseline_empty, baseline_report_arg | t54 giết |
| Cộng lỗi nền, không xoá lỗi trước | baseline_errors, baseline_reset | Gỡ cộng riêng tương đương với vế hong cuối; gán đè bị giết |
| Tự kiểm song song, đầu vào, giữ lỗi cũ | parallel_skip, parallel_arg, parallel_reset | t54 giết |
| Gate không chạy bán kính | gate_run_full | t54 giết |
| Nhánh đủ truyền mọi tên/nền/worker | full_names, full_base, full_workers | t54 giết |
| Đọc hết kết quả, giữ lỗi qua nhiều kết quả | full_errors, full_reset, full_first_only, full_repeat_result | Bỏ mọi lỗi bị giết; gán đè/chỉ đọc đầu sống và làm xanh sai trong wiring (F12); lặp kết quả sống, sai số/báo cáo nhưng chưa chứng minh đổi xanh/đỏ |
| Trình bày bảng bán kính | print_full_drop | Sống; thiếu bảng không làm ca đỏ |
| Mã thoát đủ/gate dựa hong/loi_db/tiền kiểm/cổng | final_hong, final_db, final_precheck, final_gate | Vế hong dư với lỗi nền; ba vế khác bị giết |

Ma trận là danh sách biến đổi có giới hạn, không phải chứng minh toán học mọi chương trình đột biến. Các chuỗi chẩn đoán thuần văn phong không được coi là chốt riêng. Cặp neo/thay chính xác nằm trong `evidence/main-mutations.json` và `main-extra-mutations.json`; từng trạng thái 56 CA nằm trong JSON và `main-matrix.md`. Hai đột biến tương đương executor khai (`baseline_errors`, `final_hong`) vẫn được reviewer đo, không tính thành finding chỉ vì sống.

Chốt cuối các phép đo (ghi sau khi mọi lượt bắt buộc đã kết thúc):

- 69/69 `g668_*`/`f2_*`/`f5_*`/`f6_*`/`f7_*`/`f8_*`/`f9_*`: đúng đích, bán kính **1/56**, 3.795 `qua` + 69 `giet_that`, 0 `tin_dung_gia`, 0 `bo_qua`. `radii-new.log` kết thúc TOTAL 69 ERRORS 0. Kết quả đầy đủ đã đối chiếu ở `radii-new-corrected.json` và `summary.json`.
- Phép đo trên gồm 55 ca của lượt đầu cộng `t47` đo lại trên **đúng từng mutant** sau sửa cấu hình git con; không khai đó là một lượt chạy sạch duy nhất. Log gốc còn nguyên. `corrected/` chỉ thay trạng thái t47 bằng kết quả đã đo thật; các script và log `t47-retry*`/`t47-final.log` lưu dấu vết. Tương tự cho 62 mutant main ban đầu.
- 68/68 phép đổi độc lập tại `main`: 55 bị giết đúng t54, 13 sống **56/56 qua**, không bỏ qua/tín dụng giả sau phép đo bù. 13 survivor: `baseline_errors`, `break_on_error`, `ca_duplicate_middle`, `ca_reverse`, `final_hong`, `full_first_only`, `full_repeat_result`, `full_reset`, `pass_counter`, `print_full_drop`, `print_writer_drop`, `receiver_baseline`, `skip_counter`.
- Trong 13 survivor, ba phép có bằng chứng control đỏ / mutant xanh: **ca_duplicate_middle**, **full_reset**, **full_first_only** (F12). Năm phép làm sai/thiếu đầu ra hoặc bộ đếm: `full_repeat_result`, `pass_counter`, `skip_counter`, `print_full_drop`, `print_writer_drop` — điểm mù stdout cùng lớp, mức biểu hiện thấp hơn. Năm phép còn lại không dùng làm finding xanh sai: hai rào tương đương `baseline_errors`/`final_hong`; `break_on_error` vẫn giữ lỗi và dọn tệp; đảo CA chưa chứng minh hậu quả; `receiver_baseline` dùng tên không có trong CA nên không đổi tập. Probe bổ sung với tên CA thật bị t54 giết.
- Riêng dispatcher `--gop`: mutant F13 sống **56/56**, đã chạy CLI thật đối chứng/mutant; không nằm trong con số 68 main.
- 9 mutant cũ: lỗi bán kính=0; 27/27 trạng thái t52/t53/t54 đều `qua`. Toàn mẫu có 484 `qua`, 9 `giet_that`, **11 `bo_qua` ngoài ba ca mới**; giữ nguyên lý do ở `radii-old-corrected.json`. Không suy rằng đã đo đủ mọi ca cho mọi mutant cũ, cũng không suy thành đã đo toàn bộ 212 mutant cũ.
- Bốn f8_* giết đúng t52; hai f9_* giết đúng t53; 21 f7_* giết đúng t54. Vì thế các bản vá đã thêm răng thật, nhưng tập mutant chính thức chưa bao phủ toàn lớp (F12/F13).
- Bộ phản chứng workflow: control F1=20/20, F3=28/28, F10=7/7; gỡ F10 + trả `splitlines()` làm **27/28 F3** và **7/7 F10** lọt. Không tự tạo chuỗi mới thuộc loại bị phân công cấm. Sau chốt ký tự/nội suy, chưa thấy biến thể mới của chính loại ấy; F14 là thiếu ghim shell, không phải payload ẩn.

Giới hạn nghiệm thu và thông tin phiên:

- Không chạy GitHub CI; không sửa/commit/push mã sản phẩm hay đăng verdict lên GitHub. Các sửa đổi thử nghiệm nằm trong bản sao `/tmp` hoặc mã được nạp từ bản sao đó. Mã harness và kết quả nằm trong `evidence/` cạnh verdict.
- Reviewer: OpenAI Codex, họ GPT-6 theo cấu hình phiên; execution surface là dịch vụ Codex qua API và terminal tools, transport machine/local. Không có chứng cứ độc lập để khai model ID/effort thực tế hoặc tự nhận đây là Codex CLI gpt-6-astra. Không tạo human_audited hay quyền land.
- Linux, Python 3.11.15; actionlint 1.7.7; Ruff 0.15.15. Git core.abbrev=7 và không ký các commit của fixture. Checkout được giao có HEAD/tree/status/diff/index cuối giống đầu, cả untracked/ignored đều rỗng. Snapshot chứng minh không có delta quan sát được ở hai mốc, không phải audit mọi lần ghi trong lịch sử. Sandbox thực tế workspace-write, checkout được xử lý read-only theo vai trò.
- **Chưa đo** A1 8 mảnh thật đủ **281** mutant ở head này; CLI mặc định đủ 281; Windows/Actions runner; upload/download artifact thật; ruleset và A9. A1 executor khai ở c8f52b6 không thay được A1 của ef011126. Gate trọn đã chạy là chế độ giao mảnh, với đủ 56 CA, cổng cây thật và tự kiểm như mô tả HƯỚNG 10.
- F14 có phần validator/registry/actionlint đo được, phần hậu quả PowerShell suy luận từ tài liệu chính thức đã dẫn; chưa chạy pwsh. Không nâng thành P1 hay tuyên bố workflow hiện tại đang xanh sai trên Windows.
- Không xác nhận thêm mọi định lượng lịch sử trong spec. Các số dùng cho kết luận ở đây đều có lệnh và hiện vật tương ứng. Hai hướng mới tối thiểu đã đạt bằng danh tính CA và chuỗi kết quả nhiều phần tử, ngoài ra còn dispatcher CLI và shell mặc định Windows.

Bảng lớp finding — giữ nguyên slug nguồn qua các lượt:

| Slug lớp | Lịch sử / nguồn | Hiện trạng, mức cao nhất còn mở | Cách đóng lớp cần được kiểm |
|---|---|---|---|
| g5-main-thieu-ca-chon-vong-ban-kinh | F2@c8f52b6 → F5@c454ee9 → F6@2b501ef → F7@971e14c → F12@ef011126 | Mở, P2. Nhật ký mất danh tính ca và không đo tiêu thụ luồng kết quả | Quan sát đúng từng ca và từng kết quả; lỗi sớm/muộn và nhiều kết quả; đối chứng mutant thay ca, gán đè, cắt vòng đều phải chết đúng đích |
| g5-gom-cli-thieu-rang | F8@971e14c → F13@ef011126 | Mở, P2. Helper có răng, dispatcher chưa có | Kiểm qua cửa tiến trình CLI thực với bộ đạt/bộ sai; cắt lời gọi dispatcher phải làm ca đỏ |
| g5-shell-bo-qua-thuc-thi | F1@c8f52b6 → F3@c454ee9 → F10@971e14c → F14@ef011126 | Mở, P2. Biểu thức/ký tự đã chặn; vắng shell vẫn bị coi là Bash | Phân biệt shell vắng theo nền; ghim/kiểm ngữ nghĩa fail-fast cho bước G5 hai lệnh; ca bỏ shell phải đỏ và control hiện tại xanh |
| g5-nguon-van-tay-thieu-rang | F9@971e14c | Đóng trong phạm vi đo | t53 đổi bytes giữ HEAD, đổi HEAD, không Git; hai mutant nguồn chết đúng t53 |
| g5-chu-thich-dem-cu | F11@971e14c | Đóng | Số thật=5, hook/chú thích/ca t152 đồng bộ |

Có **3 lớp mở, 2 lớp đóng; 3 finding mới**. F12 gom 3 biểu hiện có hậu quả xanh sai và 5 điểm mù số liệu/đầu ra cùng nguyên nhân; F13 và F14 mỗi finding một biểu hiện chính. Không tạo finding cho 5 survivor chưa chứng minh sai/tương đương.

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F12 | P2 | ops/cong_cu_test.py:7236, :7260, :7295; t54 tại :6520 | Nhật ký "mọi lời gọi" mất danh tính CA, trả một kết quả giả cho vòng đủ và bỏ stdout; thay một CA bằng ca lặp, cắt vòng kết quả hoặc xoá lỗi trước vẫn sống | `main-ca_duplicate_middle.json`, `main-full_first_only.json`, `main-full_reset.json` + bản corrected; mỗi mutant 56/56 qua; `wiring-more.log`: control rc=1 → mutant rc=0 trong ba kịch bản khác nhau |
| F13 | P2 | ops/cong_cu_test.py:7570; giàn giáo CLI tại :7187 | F8 kiểm trực tiếp helper, không kiểm dây dispatcher gọi helper; bỏ gom thật không ca nào bắt | `entrypoint.py`: thay đúng `sys.exit(_main_gop())` → `sys.exit(0)`; 56/56 qua; CLI thư mục rỗng control=1, mutant=0/stdout rỗng |
| F14 | P2 | .claude/dev/ci_dang_ky_test.py:1120 | Vắng shell được mặc định là bash trong validator, khác Windows/pwsh; mất chốt fail-fast giữa probe và selftest | `workflow_shell.py`: ba trường hợp validator=[]/actionlint=0; clone bỏ shell G5 mảnh registry=1020/1020, rc=0. Hậu quả native exit-code là suy luận nguồn chính thức, chưa chạy Windows |

ĐỐI CHIẾU LƯỢT TRƯỚC — trạng thái và phần đã tự đo:

| Finding | Trạng thái | Đối chiếu độc lập |
|---|---|---|
| F1 | chưa đóng | Shell/keys/env/with cũ có răng; lớp ngữ nghĩa thực thi còn F14. Không lấy 20 ca cũ xanh làm chứng minh đóng lớp |
| F2 | chưa đóng lớp | Ba f2_* đúng 1/56; chọn chế độ đã vá, nhưng lớp main tiếp tục F12 |
| F3 | đóng biểu hiện | 28 ca nguyên cây chặn đúng; ablation hai hàng rào làm 27 lọt, chốt ký tự đóng cơ chế tách dòng cũ. Lớp workflow tổng thể còn F14 |
| F5 | chưa đóng lớp | Năm f5_* đúng 1/56; nhận/ghi/truyền lỗi được gọi tên đã vá, lớp main còn F12 |
| F6 | chưa đóng lớp | Bốn f6_* đúng 1/56; dữ liệu/vân tay/tiền kiểm/worker đã vá, lớp main còn F12 |
| F7 | chưa đóng — VÁ HỜ ở cấp lớp | 21 f7_* đều có răng và các lỗi cũ được kích thích riêng; tuyên bố nhật ký mọi lời gọi chưa đúng theo F12. Không gọi những răng mới là vô hiệu |
| F8 | chưa đóng — VÁ HỜ ở cấp lớp | Bốn f8_* chết đúng t52; dispatcher thật vẫn không được chốt (F13) |
| F9 | đóng — ĐÃ VÁ THẬT | t53 chạy kho git tạm, bytes/HEAD/no-Git; f9_sha_hang và f9_head_hang giết riêng đúng t53 |
| F10 | đóng biểu hiện — ĐÃ VÁ THẬT | Bảy ca sẵn có chặn đúng; gỡ chốt làm cả bảy lọt. Lớp workflow còn F14, không phải tái diễn nội suy |
| F11 | đóng — ĐÃ VÁ THẬT | 5 AL_VER thật; chú thích workflow/hook cùng 5; t152 PASS |

Ngưỡng áp dụng: 0 P1/P2/P3 theo chỉ thị packet. Còn 3 P2 nên không approve. Lớp main và workflow vẫn chưa đóng theo cấu trúc dù các bản vá riêng có hiệu quả; verdict trả executor/điều phối, không cấp quyền sửa/land hoặc tự quyết vòng review tiếp theo.

verdict: changes_requested
reviewed_sha: ef01112604ef47096daf99ee2470125c3ca0f0b3
