# Cross-review độc lập — packet #668 r1 g1 — lượt 2

verdict: changes_requested

Trạng thái lúc mở tệp: dang_review; đã ghi dần các phép đo dưới đây.
reviewed_sha: c454ee9984a287fe06b1446b827850cade261007

Mọi đột biến chạy trên bản sao trong /tmp. Không sửa mã sản phẩm.

HƯỚNG 1: MỚI — khác biệt bộ tách dòng Python/Bash (F1 chưa đóng lớp)
  giả thuyết : Danh sách lệnh nhìn đúng sau splitlines nhưng thực tế Bash không chạy lệnh gom.
  lệnh       : python3 evidence/env.py python3 evidence/workflow_probe.py
  output     : original []; vt-comment validator=[] actionlint=0; Bash chuẩn rc=0 stdout='' stderr=''.
               Đối chứng cùng --gop không bọc chú thích: rc=1 [G-thu-muc].
               cr-comment cũng validator=[]/Bash rc=0 nhưng actionlint=1, KHÔNG dùng CR làm chứng cứ CI xanh.
  kết luận   : LỖI (P1), F3 nối lớp F1. _dong_lenh dùng str.splitlines(), nhận VT làm dấu xuống dòng;
               Bash coi VT trong chú thích là ký tự thường, nên lệnh --gop nằm trọn trong chú thích.
               YAML dùng escape VT hợp lệ, qua actionlint 1.7.7. Phản chứng/log: evidence/workflow_probe.py,
               evidence/vt-comment.yml, evidence/vt-comment.lint, evidence/workflow.log.
               Chỉ chạy Bash/actionlint tại chỗ; không chạy GitHub Actions.

HƯỚNG 2: MỚI — chốt ngữ nghĩa từ chối cấu hình tương đương / metadata vô hại
  giả thuyết : Danh sách khoá mới khóa cả thay đổi hợp lệ không làm mất phép đo.
  lệnh       : python3 evidence/env.py python3 evidence/workflow_probe.py
  output     : registry-name: actionlint=0, validator=[gate-registry: khoá job ngoài danh sách cho phép: ['name']].
               registry-permissions(contents:read): actionlint=0, bị chặn khoá permissions.
               step-timeout=10, strategy.max-parallel=4, needs=['chuan-bi'], needs đảo thứ tự: actionlint=0, validator đỏ.
               exit 0 trước lệnh, env BASH_ENV/PATH, bước giữa mảnh/upload, bước sau upload đều bị validator bắt.
  kết luận   : KHÔNG PHẢI LỖI đã chứng minh trong hợp đồng hiện tại; ứng viên F4 thu hồi sau đối chiếu rộng.
               Chốt G5 mới rất chặt: từ chối cả job.name, max-parallel và needs tương đương. Tuy nhiên registry
               đã ghim hash toàn job gate-registry từ baseline; đổi name cũng bị loi_vung_thiet_lap bắt ở baseline.
               M6 yêu cầu hình dạng ghim/allowlist; chỉ actionlint xanh chưa chứng minh cấu hình mới được hợp đồng
               kho cho phép. Không nâng hạn chế mở rộng có chủ đích thành lỗi sản phẩm. Khi mở rộng workflow tương
               lai cần rà lại cả pin vùng và allowlist. Bằng chứng sửa kết luận: evidence/overstrict-delta.log.

HƯỚNG 3: MỚI — main bỏ dây ghi mảnh nhưng ca mới vẫn xanh
  giả thuyết : t54 chỉ nhìn tên đã chọn, chưa nhìn hậu điều ghi tệp và truyền lỗi của main.
  lệnh       : python3 evidence/env.py python3 -u evidence/main_mutants.py
  output     : review668_manh_no_write Counter({'qua': 56}), target=('qua', None), 33.2 s.
               Đối chứng review668_du_partial: 55 qua + 1 giet_that, chính t54;
               lý do: main chỉ đo 244 tên trong khi mong 245 (28.7 s).
  kết luận   : LỖI (P2), F5 nối lớp F2/M4: thay lời gọi _ket_thuc_manh trong main bằng ([], 0) vẫn qua 56/56.
               main không ghi tệp mảnh nữa; t52 chỉ kiểm writer trực tiếp, còn --tu-kiem-main thay writer bằng
               lambda không ghi nhận lời gọi. Không khẳng định mã ứng viên đang bỏ ghi; đây là thiếu răng test.
               Script lưu cặp neo/thay chạy được và toàn bộ trạng thái ở evidence/review668_manh_no_write.json.
               Đột biến CLI không ghi sẽ bị upload thiếu tệp bắt, nên finding ở P2, không suy thành CI xanh.

HƯỚNG 4: Hồi quy registry, actionlint, t152 và Ruff F
  giả thuyết : Bản vá r2 làm hỏng registry hoặc các hợp đồng kế thừa.
  lệnh       : python3 evidence/env.py python3 -u cay-kho/.claude/dev/ci_dang_ky_test.py
               python3 evidence/env.py python3 evidence/compat.py
  output     : Registry PHẢN CHỨNG: 985/985 đỏ đúng; TỔNG: ĐẠT.
               head/base: actionlint rc=0; t152 1/1 qua, 0 bỏ qua, 0 hỏng, rc=0.
               head/base: Ruff F rc=1, cùng 6 F841 (5 launcher, 1 cong_cu), delta=0 theo rule/file/message.
               actionlint 1.7.7; Ruff 0.15.8; Python 3.11.15.
  kết luận   : KHÔNG PHẢI LỖI trên các phép đã đo. Bare lint đỏ nền, KHÔNG gọi là Ruff passed.
               Dùng cùng bản Ruff cho hai SHA, chưa chạy bare lint bằng pin CI 0.15.15; registry kiểm pin/probe riêng.
               Môi trường tiến trình ghim commit.gpgsign=false + core.abbrev=7; không sửa Git config cây được giao.

HƯỚNG 5: MỚI — gỡ từng nhánh mới, đo phản chứng mất răng đúng nhánh
  giả thuyết : 20 phản chứng F1 có thể đỏ nhờ chốt khác, không kiểm được nhánh mới tương ứng.
  lệnh       : python3 evidence/env.py python3 evidence/branch_teeth.py
  output     : control 67/67 (trích nguyên khối phản chứng workflow trong phan_chung).
               gỡ job_keys: 3 ca nhận sai (job-defaults 2, container 1).
               gỡ job_env_strategy: 5 ca nhận sai (env 2, runs-on, matrix.os, fail-fast).
               gỡ step_keys_shell: 7 ca nhận sai (shell 5, working-directory 2).
               gỡ with: 2 ca nhận sai (checkout ref, python version).
               gỡ setup_env: 1 ca nhận sai (gate-thiet-lap-env-la).
  kết luận   : KHÔNG PHẢI LỖI tín dụng giả: cả 5 nhánh phát lỗi của _loi_thuc_thi_g5 đều có phản chứng riêng
               mất răng khi gỡ đúng nhánh. Đây là ablation trên AST trong bộ nhớ của bản sao, giữ nguyên cấu trúc
               if/elif và các nhánh khác; không sửa source được review. Không đồng nghĩa đã phủ mọi biểu thức con
               hay đã đóng ngữ nghĩa shell (F3). Chi tiết: evidence/branch-teeth.log.
  bổ sung HƯỚNG 3: review668_manh_ignore_error và review668_manh_no_receiver cũng sống, 56/56 qua,
               lần lượt 30.2/30.9 s. Đây là ba biểu hiện cùng lớp test main không kiểm dây nhận/ghi/truyền lỗi.

HƯỚNG 6: Gate đầy đủ trên ứng viên r2
  giả thuyết : t54 mới gây hồi quy ca hoặc N126.
  lệnh       : CONG_CU_TEST_BAN_KINH=manh python3 evidence/env.py python3 -u cay-kho/ops/cong_cu_test.py
  output     : cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0.
               TỰ KIỂM SONG SONG (N126): ĐẠT.
               SỐ LIỆU: ca=56 · đột biến=245 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT.
  kết luận   : KHÔNG PHẢI LỖI qua chế độ gate; log evidence/gate.log. Gate giữ tự kiểm song song,
               chỉ giao vòng bán kính đầy đủ cho job mảnh; không gọi gate pass là 245 đột biến đã đo.

  Bổ sung HƯỚNG 1: evidence/raw_yaml.py đo cả gate, gate-cong-cu và gate-cong-cu-gop:
               mỗi workflow VT validator=[] / actionlint=0, Bash rc=0, không stdout/stderr.
               Với thư mục manh có artifact hỏng thật: lệnh thường rc=1 [G-dau], bản VT rc=0.
               Không cần giả định download không có artifact mà vẫn xanh; bộ có tệp sai cũng bị bỏ kiểm.
               Mã nguồn runner ghi script UTF-8, chỉ chuẩn hóa CRLF trên Windows, không chuẩn hóa VT;
               đây là căn cứ suy rộng từ Bash local, KHÔNG phải lượt chạy CI:
               [ScriptHandler.cs](https://github.com/actions/runner/blob/main/src/Runner.Worker/Handlers/ScriptHandler.cs#L251-L266)

  Giới hạn read-only: t152 chạy hook session-start đã sinh đúng một tệp ignored
               cay-kho/.claude/.packet_state/session-start.ran (28 byte). So SHA-256 toàn cây không tính .git
               với bản sao đầu phiên xác nhận đó là delta duy nhất; đã dọn đúng tệp do phép đo tạo và thư mục rỗng.
               Không có mã sản phẩm thay đổi. Không khai checkout được mount read-only hay chưa từng ghi gì.
               Snapshot so sánh trước dọn lưu evidence/snapshot-compare.json.

HƯỚNG 7: YAML thô và sự kiện workflow — giới hạn validator dict
  giả thuyết : Khoá trùng, alias hoặc đổi sự kiện có thể được loi_g5_workflow nhận xanh.
  lệnh       : python3 evidence/env.py python3 evidence/raw_yaml.py
               python3 evidence/env.py python3 evidence/workflow_probe.py
  output     : duplicate-run validator=[] nhưng actionlint=1: key run is duplicated.
               anchors (env dùng chung bằng YAML alias) validator=[] nhưng actionlint=1: env is alias node.
               on chỉ workflow_dispatch: validator=[], actionlint=0.
  kết luận   : KHÔNG PHẢI LỖI CI xanh đã chứng minh ở khóa trùng/alias: actionlint đã chặn trong môi trường hiện có.
               Đổi on có thể ngừng tạo lượt PR; hàm G5 không gác sự kiện. Chưa đo required-check/ruleset trên GitHub,
               không suy thiếu lượt chạy thành check success; không thêm finding P1 chỉ từ dict xanh.
               Không khẳng định mọi YAML alias là sai trên GitHub: đây là hành vi actionlint 1.7.7 đã đo.

  Bổ sung HƯỚNG 3 (main thật với ca/transport giả, không phải bán kính thật):
               python3 evidence/env.py python3 evidence/main_wiring.py
               valid normal rc=0 exists=True; valid no_write rc=0 exists=False;
               valid no_receiver rc=1 exists=False, M-loi 31 lỗi;
               transport_error normal rc=1 M-con; ignore_error rc=0 dù vẫn in M-con.
               Giữ danh tính 56 CA nhưng thay thực thi CA bằng no-op, transport dựng BKCON hoặc rc=1 có chủ đích;
               chỉ dùng để xác minh hậu quả dây nối, không khai 31 tên ở phép này đã được đo bán kính.

  Bổ sung HƯỚNG 1 (toàn registry trên bản sao workflow VT):
               python3 evidence/env.py python3 -u /tmp/rv668-r2-workflow/.claude/dev/ci_dang_ky_test.py
               PHẢN CHỨNG: 985/985 đỏ đúng; TỔNG: ĐẠT. Chỉ đổi giá trị run của bước gom, giữ định dạng phần khác.
               Registry thật không chặn phản chứng này; log evidence/registry-vt.log.

Thông tin phiên và phạm vi:
- Người dùng cấp review độc lập, không sửa sản phẩm, không CI; không cần cấp lease viết mã mới.
- Baseline: f8a7829cc44f296c25faf1a6439b603ba840f70b; head r1: c8f52b6c89fcc62ed63b6e358892d7bbaf5be73b.
- Head r2: c454ee9984a287fe06b1446b827850cade261007; tree: 91143c95af35bdcb255950bbf308153b1f9b8a23.
- SPEC SHA-256: dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15, khớp.
- Diff: 5 tệp, +846/−28; áp trần ~1.100 dòng thêm được người dùng cấp trong prompt, không dùng trần cũ làm finding.
- Reviewer: OpenAI Codex, họ GPT-6 theo cấu hình phiên; execution_surface=codex_service (API + công cụ terminal),
  transport=machine/local tool execution. Không có runtime evidence độc lập cho model ID/effort; không tự khai
  Codex CLI/gpt-6-astra nếu không đo được. Verdict này không tự tạo human_audited hay quyền land.
- Linux / Python 3.11.15; Git config qua env tiến trình, PYTHONDONTWRITEBYTECODE=1, Ruff --no-cache.
- Không dùng bằng chứng A1 executor đang chạy trên SHA r1 để suy A1 đạt trên SHA r2. Chưa chạy 8 mảnh thật trọn 245
  đột biến + gom hay CLI mặc định đủ 245; lần này đo gate + 33 mới + mẫu cũ theo nhiệm vụ. Chưa đo runner Windows,
  GitHub upload/download thực, ruleset hay latency A9. Không chạy CI.
- Git và hash snapshot cuối chỉ chứng minh không còn delta quan sát được, không chứng minh lịch sử không từng ghi.

HƯỚNG 8: Mẫu có chủ đích trong 212 đột biến cũ — không giết thêm t52/t53/t54
  giả thuyết : Ca mới bám thuộc tính chung làm đột biến cũ tăng bán kính.
  lệnh       : python3 evidence/env.py python3 -u evidence/radii.py old
  output     : TOTAL 9 ERRORS 0 SECONDS 156.3; 9/9 bán kính 1/56, đúng ca đích.
               Mẫu = toàn bộ 5 bn_* nhắm TEP_TEST + t1_rc_gop, t6_day_g5_sau_py_compile,
               t13_mat_requiredness_khi_tool_bien_mat, t21_git_regex_cat_hau_to.
               t52/t53/t54: 27/27 trạng thái qua, không giết thêm; tổng trạng thái: qua=484, giet_that=9, bo_qua=11.
  kết luận   : KHÔNG PHẢI LỖI tăng bán kính trong mẫu. Không suy 9 tên đại diện thành đã chạy đủ 212 cũ.
               Có 11 trạng thái bo_qua ở các ca cũ, ghi nguyên lý do trong evidence/radii-old.json;
               các ca mới và ca đích của từng mutant đều thực chạy, không bo_qua/tin_dung_gia.
               Lần đầu script reviewer gọi sai arity _ket_luan_ban_ghi, rc=1; lần này đã sửa và chạy lại từ đầu,
               rc=0. Log lỗi giàn giáo giữ evidence/radii-old-harness-error.log, không tính là lỗi sản phẩm.

  Bổ sung HƯỚNG 2 (delta baseline): python3 evidence/env.py python3 evidence/overstrict_delta.py
               Chỉ thêm gate-registry.name: baseline validator=[], r2 validator đỏ khoá name.
               Tên job là nhãn hiển thị, độc lập job ID / needs / steps; xem GitHub Docs:
               [GitHub workflow syntax — job.name](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idname)

  Đính chính kết luận ứng viên F4: phép đo rộng thấy cả baseline và r2 đều chặn gate-registry.name qua
               loi_vung_thiet_lap (cùng băm 6478e49a…). Toàn registry r2 với metadata ấy rc=1 có HAI lý do:
               G5 allowlist mới và pin vùng đã có từ trước. Vì vậy F4 được thu hồi, không tính vào finding cuối.
               Đây là hạn chế mở rộng workflow cần biết, không đủ căn cứ gọi là hồi quy gate của packet.

  Căn cứ runtime bổ sung cho HƯỚNG 1: [ScriptHandlerHelpers.cs](https://github.com/actions/runner/blob/main/src/Runner.Worker/Handlers/ScriptHandlerHelpers.cs)
               ghim Bash thành --noprofile --norc -e -o pipefail {0}; FixUpScriptContents không sửa nội dung Bash.
               Lệnh Bash ở phản chứng dùng đúng argv này. Nguồn được đọc lúc review; không thay cho lượt runner thật.

HƯỚNG 9: Toàn bộ 33 g668_*/f2_* — bán kính thật trên 56 CA
  giả thuyết : Ca mới làm tăng bán kính, hoặc mutant chính thức không chết đúng ca đích.
  lệnh       : python3 evidence/env.py python3 -u evidence/radii.py new
               python3 evidence/summarize.py
  output     : TOTAL 33 ERRORS 0 SECONDS 447.2; rc=0; 33/33 dòng ok, bán kính 1/56.
  kết luận   : KHÔNG PHẢI LỖI trên 33 mutant đã đăng ký. Nhận bản ghi qua _nhan_ket_qua_con và kết luận bằng
               _ket_luan_ban_ghi của chính ứng viên, sau đó kiểm độc lập danh tính ca đích/trạng thái trong JSON.
               Log được tính: evidence/radii-new-fixed.log; dữ liệu đủ: evidence/radii-new.json.
               Lượt đầu cùng nhóm gặp lỗi arity trong script reviewer SAU khi con chạy; rc=1, không được tính pass.
               Lượt tính ở đây đã chạy lại toàn bộ sau sửa harness. Các mutant bổ sung F5 không nằm trong 33 tên này.

Bổ sung kiểm chứng cuối:
- 33 mới: 1.815 trạng thái qua, 33 giet_that, 0 bo_qua, 0 tin_dung_gia; mỗi bản ghi đủ 56 ca,
  đúng một ca giết và bằng ca đích. 3 f2_* đều giết chính t54. evidence/radii-summary.log.
- A7 bổ sung: `python3 evidence/env.py python3 evidence/lease_subset.py` rc=0,
  t24/t31/t35/t161/t162 PASS ở cả head và baseline. Dòng KHÔNG ĐO ĐƯỢC ở t162 là output
  của đối chứng cú pháp không hỗ trợ, không phải ca bị bỏ qua. Lần dựng harness đầu thiếu sys.path ops
  làm import bash_nen lỗi; đã sửa harness và chạy lại cả hai vế, không sửa sản phẩm.
- `python3 evidence/integrity.py`: HEAD/tree giữ nguyên; diff tracked/index rc=0;
  status gồm ignored rỗng; SHA-256 toàn bộ tệp ngoài .git bằng bản sao đầu phiên (delta=[]).
  Log evidence/final-integrity.log. Áp ngưỡng 0 P1/P2/P3 theo prompt, nên hai finding dưới chặn approve.

Bảng lớp finding — giữ slug kế thừa lượt 1 (2 lớp còn mở, 2 finding mới còn hiệu lực):

| slug lớp | lịch sử / biểu hiện | mức cao nhất còn mở | nguồn | cách sửa chung và phép đóng lớp |
|---|---|---|---|---|
| g5-shell-bo-qua-thuc-thi | F1 shell syntax-only được bắt; F3 run bị chú thích bằng VT vẫn lọt | P1 | r1 c8f52b6 → r2 c454ee9 | Kiểm ngữ nghĩa run theo đúng ranh giới dòng của shell, ràng buộc cả script chứ không chỉ danh sách sau splitlines. Đối chứng workflow chuẩn xanh; các biến thể không thực thi phải bị validator từ chối; bộ artifact hỏng phải gom đỏ. |
| g5-main-thieu-ca-chon-vong-ban-kinh | F2 bỏ vòng du được t54 bắt; F5 bỏ nhận/ghi/truyền lỗi mảnh còn sống | P2 | r1 c8f52b6 → r2 c454ee9 | Giữ slug để không xóa lịch sử; mở rộng phép đo dây nối main tới nhận bản ghi, gọi writer và truyền lỗi. Cần đầu vào con không rỗng/đỏ có chủ đích và ghi nhận hậu điều writer; từng mutant bị đúng ca giết, không tăng bán kính 212 cũ. |

F4 là ứng viên về chốt quá chặt đã thu hồi khi đối chiếu hợp đồng pin vùng baseline (HƯỚNG 2), không tính thành lớp/finding còn mở. Không đánh lại số F5 để giấu lịch sử ghi dần.

| Finding | mức | tệp:dòng | mô tả | phản chứng chạy được |
|---|---|---|---|---|
| F3 | P1 | .claude/dev/ci_dang_ky_test.py:1088 | `_dong_lenh` dùng `splitlines()` nên VT trong chú thích được coi là ranh giới lệnh; Bash không coi VT là newline. G5 gom có thể trả 0 mà chưa kiểm bộ sai. `loi_g5_workflow=[]`, actionlint=0, toàn registry vẫn 985/985 ĐẠT. Không khẳng định workflow gốc đang bỏ chạy. | `python3 evidence/env.py python3 evidence/workflow_probe.py`; `python3 evidence/env.py python3 evidence/raw_yaml.py`; evidence/vt-comment.yml; evidence/registry-vt.log |
| F5 | P2 | ops/cong_cu_test.py:7063 | Cửa t54 cho `_phong_con` trả rỗng và writer luôn thành công, không quan sát lời gọi/hậu điều. Bỏ receiver (main:7155), writer (:7160), hoặc truyền lỗi (:7163) đều sống qua 56/56. Đối chứng du thiếu một tên bị t54 giết. Đây là thiếu răng M4, không phải assertion mã gốc đang hỏng. | `python3 evidence/env.py python3 -u evidence/main_mutants.py`; `python3 evidence/env.py python3 evidence/main_wiring.py`; evidence/main-mutants.log và 4 JSON trạng thái |

| Finding lượt 1 | trạng thái | lý do và đối chiếu |
|---|---|---|
| F1 | chưa đóng | ĐÃ VÁ THẬT biểu hiện shell `bash -n`: có ca riêng và ablation đúng nhánh. CHƯA ĐÓNG LỚP ngữ nghĩa thực thi: F3 được validator, actionlint và registry nhận xanh nhưng Bash không chạy gom. |
| F2 | chưa đóng | ĐÃ VÁ THẬT biểu hiện du bỏ vòng; ba f2_* có răng. CHƯA ĐÓNG LỚP dây nối main/M4: ba đột biến F5 vẫn sống. Không gọi bản vá hiện tại vô tác dụng; nó đóng phần chọn danh sách nhưng bỏ phần nhận/ghi/truyền lỗi. |

Các phần không đo được: A1 đủ 8 mảnh và A5 CLI đủ 245 trên r2; Windows/GitHub Actions thực; ruleset và A9. Không nhận lời khai A1 ở SHA r1 làm bằng chứng r2. Không sửa mã sản phẩm, không commit/push/CI/đăng GitHub.

verdict: changes_requested
reviewed_sha: c454ee9984a287fe06b1446b827850cade261007
