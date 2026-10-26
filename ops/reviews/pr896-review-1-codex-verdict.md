verdict: changes_requested
reviewed_sha: 816f43988eb3012726120ad00166a989cc2b9af6
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

Review độc lập, chỉ đọc + đo, theo `runs/64761d8e/prompt.snapshot`; base `1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e`, reviewed_tree `3da0ce24590dfcf2e60805b2bef76687cdd64405`.

Reviewer `codex`; provider `openai_codex`; execution_surface `codex_cli`; transport `machine`. Run `64761d8e6164462d870c3d534d325dd2`; header CLI khai `gpt-6.1-sol`, effort `xhigh`, session `01a16ec6-03c0-72c0-ac25-dccfeef0cd62` (đọc `runs/64761d8e/run.json` và đầu `stderr.log`; header không chứng minh model phục vụ ở máy chủ). Không có GitHub submitter vì không đăng/push. Sandbox khai `workspace-write`; read-only đối với `cay-kho/` được giữ bằng phạm vi lệnh, bytecode bị tắt. Không gọi mạng, không dùng subagent, không sửa nguồn review.

P2 ở `CLAUDE.md:171–173`: t162 được mô tả rộng hơn phạm vi phép đo; `exclude:`/`if:` cấp job nằm ngoài ca đó. `HINT.patch` chỉ sửa lời văn. Các số/SHA/readback còn lại khớp trong phạm vi đo; những dữ kiện GitHub không có raw snapshot được đánh dấu rõ, không nâng thành pass.

## BẢNG ĐO

Quy ước: U = `ubuntu-latest`, W = `windows-latest`; Hn trỏ hướng đo có lệnh/output bên dưới. Các script nằm ngoài cây review và có thể chạy từ `cay-kho/` với `PYTHONDONTWRITEBYTECODE=1`. Tên nhánh không được dùng làm chuẩn.

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact head/tree/base và diff | 816f439… trên base 1ccc314…; 6 tệp | H1/H15: git rev-parse HEAD, HEAD^{tree}; git diff base head == ../diff.patch; tree=3da0ce24590dfcf2e60805b2bef76687cdd64405; +31/-34 CLAUDE, land +27/-0, sums +3/-0, readback +6/+436/+29 | Có |
| Ba lần tài liệu trôi khỏi CI | BA: #548, #878, #879 | H11: python3 ../review_evidence/history_probe.py; so YAML/CLAUDE ở d705623^, d705623, 5f288ea, 747f983, e63961f, 6ac385f | Có |
| #548 bỏ điều kiện master | CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND; chuan-bi | H11: git show d705623^:.github/workflows/ci.yml so d705623:…; biểu thức cũ có github.ref master, mới không có; thêm nguồn chung chuan-bi | Có (bỏ điều kiện khi đưa công thức về chuan-bi) |
| Sửa ở #870; cũ tiếp #878/#879; đo lại #889 | windows-only và một phần gate | H11: git show 5f288ea, 747f983, e63961f, 6ac385f; docs #870 giữ hai nền dispatch khi #878 đã có windows-only; #879 thêm exclude; #889 thêm cảnh báo | Có |
| Run 39354156843 | ci.yml; push 3a3a3ca lên master; 23 job Ubuntu | H11: đọc JSON readback-run/readback-jobs-39354156843; id=39354156843, event=push, head_branch=master, head_sha=3a3a3caca5de4934ff53851feb6994c2c7b84ad5, total_count=len=unique=23; 23 success, 23 labels=[ubuntu-latest], runner_id0=0 | Có |
| Biên bản cũ gây hiểu nhầm | 3f6c694: jobs: 23/23 success (gom windows) | H11: git show 3f6c694:ops/land/pr848-wp744-land-evidence.yaml; đúng chuỗi tại post_merge_checks | Có |
| Connector bắt P1 #859, r4323607674 | Tác giả/mức P1/comment cụ thể | H11: git show 4ae43f0 và merge #859/865; correction ghi connector P1 #859 r4323607674; không có raw comment để xác minh độc lập author/P1 | Một phần; raw comment KHÔNG ĐO ĐƯỢC offline |
| Sửa ở #865 | Đính chính 23/23 chỉ Ubuntu | H11: git show fa362fd (merge #865) và 4ae43f0; hunk thay gom windows bằng 23 job Ubuntu | Có |
| Nguồn dự kiến của từng gate* | outputs.os + exclude + job-if | H8: python3 ../review_evidence/workflow_probe.py; cả 8 job gate* lấy matrix.os từ chuan-bi; in riêng từng exclude/job-if | Có |
| t162 thực sự đánh giá biểu thức thật | push / PR thường / PR windows / từng runner_set | H2/H3/H4: --chi-ca=t162 1/1 đạt; AST 7985–8086; trace 13 lời gọi trên chính raw_expr; không chỉ so chuỗi tên ca | Có |
| Kỳ vọng được assert bởi t162 | push/PR thường Ubuntu; PR windows hai nền; dispatch theo runner_set | H4: so thân ca và trace: [U], [U], [U,W], dispatch absent/default [U,W], windows-only [W]; input windows-only không lọt sang 3 sự kiện không dispatch | Có |
| Răng của t162 đối với output os | Đổi hành vi được assert thì ca đỏ | H4: 4 mutant giá trị (master, nhãn windows, bỏ windows-only, windows-only trả hai nền) đều t162 FAIL; t161 PASS | Có, trong các nhánh được assert |
| t162 đại diện toàn bộ ma trận job | hành vi ấy được khoá; đọc ca ấy là đọc ma trận HIỆN HÀNH | H12: bỏ exclude Windows/mảnh1 hoặc bỏ job-if gom → t161 PASS/t162 PASS; checker riêng ci_dang_ky.loi_g5_workflow báo lỗi. t162 không đọc hai trường này | KHÔNG — P2 bên dưới |
| t161 chỉ khoá cấu trúc | Nguồn os chung; output không fromJSON; không evaluator | H4: AST 7927–7981, 0 lời gọi evaluator; độc lập job.os và output fromJSON làm t161 FAIL; đổi hành vi os vẫn PASS | Có |
| Trường nhãn và runner_id | Đọc labels của từng job, runner_id khác 0 | H11: 23 job đều Ubuntu/nonzero; readback-jobs-39745387589 có 22 job runner_id=0, 0 bước, failure. Đây là metadata nhận runner; không thay log/assertions của job | Có trong các readback; không suy nonzero là mọi bước đã đạt |
| Ảnh chụp 23-10 trên e63961f | push master/PR thường chỉ Ubuntu | H4: evaluator trên git show e63961f:.github/workflows/ci.yml và exact reviewed SHA đều [ubuntu-latest] cho hai context | Có; ngày người viết thực đo không xác minh độc lập |
| Ảnh chụp dispatch | hai nền; windows-only chỉ Windows | H4/H8: cả hai commit [U,W] khi input vắng/windows-and-ubuntu; [W] khi windows-only; input choice/default ở YAML khớp | Có cho matrix os; job chuan-bi vẫn cố định Ubuntu |
| Windows tự động trên push master | Chỉ launcher-windows.yml, có paths, lane launcher | H8: quét mọi workflow ở cả hai SHA; ci dispatch/nhãn mới có Windows, ci-dot-bien-du và ops-* chạy Ubuntu; launcher.push paths=[.claude/dev/**,.github/workflows/launcher-windows.yml], chỉ job launcher | Có |
| launcher PR có điều kiện | nhãn windows, types có labeled | H8: launcher.pull_request.types=[opened,synchronize,reopened,labeled], paths=.claude/dev/**; job-if kiểm nhãn; trigger/matrix in đầy đủ | Có (đây là workflow launcher, không phải ci.yml) |
| G5 Windows chỉ mảnh 0 từ #879 | gate-cong-cu duyệt ca nền rồi dừng | H8: expand matrix loại W/mảnh1..7, còn W/0; AST main 8880–8974, nhánh manh/nt return trước _phan_manh và vòng đột biến | Có |
| Ca thiếu năng lực bị loại mẫu số | so_ca = len(CA) - len(bo_qua) | H8: AST giả lập nt, 2 pass+1 skip → CA 2/2 tổng=3, rc=0; 1 failure → rc=1; all skipped → rc=1; precheck skip → rc=1 | Có |
| Gom không chạy Windows | gate-cong-cu-gop loại W; windows-only bị skipped theo if | H8: exclude=[{os:windows-latest}], job-if đòi Ubuntu trong outputs.os; matrix gom sau exclude chỉ [U] | Có về định nghĩa; skipped thực tế trên Actions KHÔNG ĐO ĐƯỢC |
| Nhiều bước if theo runner.os | Có job Windows chưa bảo đảm mọi bước chạy | H8: liệt kê đúng 6 bước có runner.os tại cả hai SHA (3 job); conditions Windows/Linux khác nhau | Có |
| Windows xanh không chứng minh bán kính | Chỉ ca không bỏ qua; lấy bán kính Ubuntu cùng head | H8: main nt không chạy vòng mutation; thông báo KHÔNG ĐO TRÊN WINDOWS; mô phỏng skip vẫn rc=0. Không có log Windows mới trong phiên này | Có, không khai đã chạy Windows thật |
| Dispatch trên ref để yêu cầu Windows | workflow_dispatch, xem runner_set để bỏ phút Ubuntu | H4/H8: workflow có dispatch và input choice; windows-only bỏ U khỏi matrix, chuan-bi vẫn U; không kiểm billing hay kích hoạt Actions offline | Có về cấu hình, không bảo đảm hạ tầng/job thực tế luôn thành công |
| Bẫy gắn nhãn của ci.yml (context giữ nguyên) | Không types; labeled không tự bắn | H8: ci.pull_request=None, launcher có types riêng; lịch sử #109 qua git log HEAD có 3736fc0/05170b4/9796f67 (H11) | Cấu hình có; mặc định Actions/raw finding P2 thứ hai không tái đo nền tảng offline |
| Bước EOL ở master (context giữ nguyên) | PR head contains required EOL base skipped | H8: if=${{ github.event_name == pull_request }} ở bước EOL, push không thoả; không suy lượt PR không có skipped khác | Có về điều kiện; không chạy job thật |
| Bổ sung sau landed, không sửa hồ sơ cũ | #891 head 0390130; comment 6366218495; chỉ thêm | H10: git show 8324567 ghi merge #891, cha2=0390130… và message dẫn comment; toàn bộ 146 dòng prefix bằng base và 0390130, thêm đúng 27 dòng | Có về Git/prefix; body comment owner không có raw readback |
| Ngày đo bổ sung | 2026-10-23 15:16Z / 15:16:09Z | H10: YAML khai đúng timestamp; readback/blob-file có ngày 23-10; không có transport receipt/đồng hồ độc lập của lần thu nhận | KHÔNG ĐO ĐƯỢC thời điểm thu nhận độc lập; không suy là sai |
| Yêu cầu review lại | 6366307732, ducthangho, 13:43:34Z, @codex review, sau #891 | H10: parse JSON đúng id/login/created_at/body; git merge #891 13:39:35Z < request 13:43:34Z; body nhắc 094e8d1 running | Có |
| Receipt không finding | 6366338141, connector, 13:45:03Z, Reviewed commit: 6ac385fdd7 | H10: parse JSON exact id/login/time/body; đúng Didn't find any major issues và short SHA | Có |
| Summary connector nay hoàn tất | 6360319005; 6ac385fdd7325f532ac4b4b6eb861292bfa7e970; completed; false; 13:45:05Z | H10: parse codex-review-state JSON: commit_sha/status/has_any_findings/has_unresolved_findings khớp; outer updated_at 13:45:05Z | Có |
| Reaction +1, không eyes | connector 13:45:08Z | H10: reactions mới đúng 1 phần tử, content=+1, login connector, created_at=13:45:08Z; cũ eyes 08:00:12Z | Có trong snapshot, không gọi GitHub sống |
| Connector sửa summary tại chỗ | Running 094e8d1 chỉ còn readback cũ | H10: cùng id/created_at, body/state đổi từ running 094e8d1 sang completed 6ac385f; new readback không còn trạng thái cũ | Có trong cặp snapshot; hiện trạng GitHub hôm nay KHÔNG ĐO ĐƯỢC |
| Đối chiếu CLAUDE.md | 094e8d1 và 6ac385f cùng blob 975cd94… | H10: git rev-parse 094e8d1:CLAUDE.md 6ac385f:CLAUDE.md; cả hai 975cd94ff851a3a0ee3aa0493e90184e5f81c874 | Có; không đồng nhất hai commit |
| Diff stat giữa head/merge cũ | Chỉ subagent_ghi_detect_test.py, land_evidence_nguon_test.py, thuộc #872/#877 | H10: git diff --stat 094e8d1 6ac385f: 2 files, 77 insertions(+), 5 deletions(-); tất cả dòng stat khớp readback; git show 9d4cb6a/daf8961 xác nhận PR | Có |
| Giới hạn và nợ mở | Chỉ bù về nội dung; không xoá chuyện merge trước review | H10: receipt/state gắn merge 6ac385f, không phải head 094e8d1; prefix/no_con_mo giữ nguyên; tệp bổ sung không tạo verdict cho head | Có; đây không phải re-review exact head 094e8d1 |
| Readback mới dùng tên mới; sum chỉ thêm | 3 tệp mới, không ghi đè cũ | H9/H10: 14/14 checksum OK; git diff base head -- ops/land/ không có dòng nội dung bị xoá; +3 SHA256SUMS, các tệp cũ prefix nguyên | Có |
| Validator hồ sơ và hai cổng bổ sung | land_evidence_nguon, doctrine-scan, doc-claims-check ok=true | H5/H6/H7: cả ba rc=0; doctrine sạch 10 tệp; doc-claims ok=true/flags=[]/381 advisory; land_evidence_nguon TỔNG: ĐẠT | Có |

## BẢNG SĂN

Các hướng được ghi tăng dần trong lúc đo. Hướng 14 lưu cả phép thử byte thô thất bại; hướng 15 giải thích và kiểm lại theo `.gitattributes`. Không che rc thất bại đó.

HƯỚNG 1: Neo đúng cây và phạm vi review
  giả thuyết : checkout lệch SHA, shallow hoặc có thay đổi trước khi đo.
  lệnh       : cd cay-kho && git rev-parse HEAD && git rev-parse --is-shallow-repository && git status --short; cat ../numstat.txt
  output     : HEAD=816f43988eb3012726120ad00166a989cc2b9af6; shallow=false; git status --short rỗng (rc=0). numstat: CLAUDE.md +31/-34; land-evidence.yaml +27/-0; SHA256SUMS.txt +3/-0; blob readback +6/-0; comments readback +436/-0; reactions readback +29/-0.
  kết luận   : KHÔNG PHẢI LỖI — cây đúng exact SHA, không sửa repository. Chỉ ghi báo cáo và scratch ngoài cay-kho/; không gọi mạng. Công cụ environment_status của skill runtime không có trong danh sách công cụ phiên này.

HƯỚNG 2: Chạy lại t161/t162 trên cây thật

  giả thuyết : Ca được viện dẫn chỉ tồn tại theo tên hoặc không assert ma trận thật.

  lệnh       : `cd cay-kho && python3 ops/lease_publish_test.py --chi-ca=t161` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
>>> vao t161_M3_chot_nguon_duy_nhat_ma_tran_ci 2026-10-24T16:38:55Z
<<< ra t161_M3_chot_nguon_duy_nhat_ma_tran_ci 0.089s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — cả hai selector chạy đúng một ca, đạt 1/1; các dòng KHÔNG ĐO ĐƯỢC nằm trong phản chứng fail-close có chủ đích của t162.

HƯỚNG 3: t162 thực thi evaluator và assert giá trị

  giả thuyết : t162 không đánh giá biểu thức thật hoặc không kiểm từng runner_set.

  lệnh       : `cd cay-kho && python3 ops/lease_publish_test.py --chi-ca=t162` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
>>> vao t162_M4_evaluator_toi_gian_chuan_bi 2026-10-24T16:38:55Z
KHÔNG ĐO ĐƯỢC: vế điều kiện không nằm trong tập tối giản hỗ trợ: "inputs.123 == 'x'"
KHÔNG ĐO ĐƯỢC: vế điều kiện không nằm trong tập tối giản hỗ trợ: ''
KHÔNG ĐO ĐƯỢC: literal/ngoặc không cân trong điều kiện: "github.ref == 'a"
KHÔNG ĐO ĐƯỢC: biểu thức không khớp hình chuẩn tối giản của chuan-bi: 'fromJSON(\'["ubuntu-latest"]\')'
<<< ra t162_M4_evaluator_toi_gian_chuan_bi 0.060s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — t162 thật chạy 1/1 đạt; hướng đột biến và trace tiếp theo đo độ phủ chi tiết.

HƯỚNG 4: Phản chứng ma trận và đo ảnh chụp hai commit

  giả thuyết : t162 chỉ khoá tên hoặc t161 cũng đánh giá biểu thức; ảnh chụp e63961f sai.

  lệnh       : `cd cay-kho && python3 ../review_evidence/matrix_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
<unknown>:2961: SyntaxWarning: invalid escape sequence '\s'
<unknown>:5104: SyntaxWarning: invalid escape sequence '\d'
t161_M3_chot_nguon_duy_nhat_ma_tran_ci: lines 7927-7981; direct evaluator calls=0; assertions bang=7
t162_M4_evaluator_toi_gian_chuan_bi: lines 7985-8086; direct evaluator calls=14; assertions bang=15
COMMIT e63961f expression=${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only') && '["windows-latest"]' || (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
  push master: ['ubuntu-latest']
  PR thường: ['ubuntu-latest']
  PR windows: ['ubuntu-latest', 'windows-latest']
  dispatch absent: ['ubuntu-latest', 'windows-latest']
  dispatch default: ['ubuntu-latest', 'windows-latest']
  dispatch windows-only: ['windows-latest']
COMMIT 816f43988eb3012726120ad00166a989cc2b9af6 expression=${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only') && '["windows-latest"]' || (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
  push master: ['ubuntu-latest']
  PR thường: ['ubuntu-latest']
  PR windows: ['ubuntu-latest', 'windows-latest']
  dispatch absent: ['ubuntu-latest', 'windows-latest']
  dispatch default: ['ubuntu-latest', 'windows-latest']
  dispatch windows-only: ['windows-latest']
TRACE t162 actual expression calls: 13
  {"event_name": "push", "labels": [], "ref": "refs/heads/master"} => ["ubuntu-latest"]
  {"event_name": "pull_request", "labels": ["docs"], "ref": "refs/pull/1/merge"} => ["ubuntu-latest"]
  {"event_name": "pull_request", "labels": ["windows"], "ref": "refs/pull/1/merge"} => ["ubuntu-latest", "windows-latest"]
  {"event_name": "workflow_dispatch", "labels": [], "ref": "refs/heads/master"} => ["ubuntu-latest", "windows-latest"]
  {"event_name": "workflow_dispatch", "inputs": {"runner_set": "windows-only"}, "labels": [], "ref": "refs/heads/master"} => ["windows-latest"]
  {"event_name": "workflow_dispatch", "inputs": {"runner_set": "windows-and-ubuntu"}, "labels": [], "ref": "refs/heads/master"} => ["ubuntu-latest", "windows-latest"]
  {"event_name": "workflow_dispatch", "inputs": {}, "labels": [], "ref": "refs/heads/master"} => ["ubuntu-latest", "windows-latest"]
  {"event_name": "push", "inputs": {"runner_set": "windows-only"}, "labels": [], "ref": "refs/heads/master"} => ["ubuntu-latest"]
  {"event_name": "push", "labels": [], "ref": "refs/heads/master"} => ["ubuntu-latest"]
  {"event_name": "pull_request", "inputs": {"runner_set": "windows-only"}, "labels": ["docs"], "ref": "refs/pull/1/merge"} => ["ubuntu-latest"]
  {"event_name": "pull_request", "labels": ["docs"], "ref": "refs/pull/1/merge"} => ["ubuntu-latest"]
  {"event_name": "pull_request", "inputs": {"runner_set": "windows-only"}, "labels": ["windows"], "ref": "refs/pull/1/merge"} => ["ubuntu-latest", "windows-latest"]
  {"event_name": "pull_request", "labels": ["windows"], "ref": "refs/pull/1/merge"} => ["ubuntu-latest", "windows-latest"]
MUTATION baseline: t161=PASS; t162=PASS
MUTATION push_master_gets_windows: t161=PASS; t162=FAIL AssertionError: push master phải chỉ chạy ubuntu-latest, nhận được: ['ubuntu-latest', 'windows-latest']
MUTATION remove_windows_only_branch: t161=PASS; t162=FAIL AssertionError: dispatch windows-only phải chỉ chạy windows-latest, nhận được: ['ubuntu-latest', 'windows-latest']
MUTATION PR_windows_becomes_linux: t161=PASS; t162=FAIL AssertionError: PR nhãn windows phải chạy hai nền, nhận được: ['ubuntu-latest']
MUTATION dispatch_windows_only_becomes_both: t161=PASS; t162=FAIL AssertionError: dispatch windows-only phải chỉ chạy windows-latest, nhận được: ['ubuntu-latest', 'windows-latest']
MUTATION output_wrapped_fromJSON: t161=FAIL AssertionError: ci.yml thật có output bọc fromJson: ['job \'chuan-bi\' output \'os\' bọc fromJson/fromJSON: \'${{ fromJSON(\\\'["ubuntu-latest"]\\\') }}\' (outputs chỉ nhận chuỗi)']; t162=FAIL ValueError: KHÔNG ĐO ĐƯỢC: biểu thức không khớp hình chuẩn tối giản của chuan-bi: 'fromJSON(\'["ubuntu-latest"]\')'
MUTATION independent_job_os: t161=FAIL AssertionError: ci.yml thật có job lén khai os: riêng: ["job 'gate' khai 'os:' riêng bằng danh sách tĩnh: ['ubuntu-latest'] (không tham chiếu needs.chuan-bi.outputs.os)"]; t162=PASS
MUTATION remove_Windows_shard1_exclusion: t161=PASS; t162=PASS
MUTATION remove_gop_if: t161=PASS; t162=PASS
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI với ma trận os: các đột biến giá trị đều làm t162 đỏ và t161 xanh; t161 bắt cấu trúc. t162 không khoá exclude/if mức job (hai đột biến cuối sống), cần đối chiếu chính xác phạm vi lời văn trước khi kết luận.

HƯỚNG 7: Validator hồ sơ land

  giả thuyết : Khối bổ sung làm hồ sơ không còn hợp lệ theo land_evidence_nguon.

  lệnh       : `cd cay-kho && python3 ops/land_evidence_nguon.py --root . --tep ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
ĐẠT ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml
land_evidence_nguon: 1 ĐẠT · 0/0 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1
TỔNG: ĐẠT
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — rc=0, 1 ĐẠT, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC, TỔNG: ĐẠT; vẫn đối chiếu nội dung riêng ở H10.

HƯỚNG 5: Cổng doctrine-scan

  giả thuyết : CLAUDE.md sửa chạm doctrine hoặc cổng bắt buộc không xanh.

  lệnh       : `cd cay-kho && python3 .claude/dev/packet_loop.py doctrine-scan --root .` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — rc=0; doctrine-scan sạch, 10 tệp, 0 chỗ chép doctrine.

HƯỚNG 6: Cổng doc-claims-check

  giả thuyết : SHA/tuyên bố tài liệu làm cổng kiểm claim đỏ hoặc ok khác true.

  lệnh       : `cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json`

  output     : trích các trường từ JSON thật; stdout đầy đủ giữ nguyên trong [review_evidence/6.log](review_evidence/6.log).

```json
{
  "ok": true,
  "files_scanned": 113,
  "flags": [],
  "advisory_count": 381,
  "layers_skipped": {}
}
```

  rc         : 0

  kết luận   : KHÔNG PHẢI LỖI — ok=true, flags=[], không có lớp bị bỏ; 381 advisory không làm gate fail. Cổng này không tự chứng minh claim nằm ngoài tập quy tắc.

HƯỚNG 8: Workflow, điều kiện kích hoạt, phần gate Windows và mẫu số bỏ qua

  giả thuyết : Ảnh chụp sai đường Windows; Windows xanh chứng minh mọi ca hoặc bán kính đột biến.

  lệnh       : `cd cay-kho && python3 ../review_evidence/workflow_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
COMMIT e63961f
ci triggers: {'push': {'branches': ['master']}, 'pull_request': None, 'workflow_dispatch': {'inputs': {'runner_set': {'description': 'windows-and-ubuntu (mặc định) hoặc windows-only (bỏ các job ma trận Ubuntu)', 'required': False, 'default': 'windows-and-ubuntu', 'type': 'choice', 'options': ['windows-and-ubuntu', 'windows-only']}}}}
gate* count: 8
  gate: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
  gate-cong-cu: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=[{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}]; job-if=None
  gate-cong-cu-gop: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=[{'os': 'windows-latest'}]; job-if=${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
  gate-ops: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
  gate-nhanh-manh: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
  gate-nhanh-gop: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=${{ !cancelled() }}
  gate-registry: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=${{ !cancelled() }}
  gate-packet-loop: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
expanded gate-cong-cu: [{'os': 'ubuntu-latest', 'manh': 0}, {'os': 'ubuntu-latest', 'manh': 1}, {'os': 'ubuntu-latest', 'manh': 2}, {'os': 'ubuntu-latest', 'manh': 3}, {'os': 'ubuntu-latest', 'manh': 4}, {'os': 'ubuntu-latest', 'manh': 5}, {'os': 'ubuntu-latest', 'manh': 6}, {'os': 'ubuntu-latest', 'manh': 7}, {'os': 'windows-latest', 'manh': 0}]
expanded gate-cong-cu-gop: [{'os': 'ubuntu-latest'}]
step conditions using runner.os: 6 [('gate', 'ci-phamvi selftest (phan chung — cong co rang)', "runner.os != 'Windows'"), ('gate-cong-cu', 'actions/upload-artifact@v4', "runner.os != 'Windows'"), ('gate-ops', 'ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)', "runner.os == 'Linux'"), ('gate-ops', 'don-nhanh selftest (chốt xoá nhánh)', "runner.os != 'Windows'"), ('gate-ops', 'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)', "${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"), ('gate-ops', 'gate lifecycle selftest (nen khong co cgroup)', "${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}")]
EOL step: ${{ github.event_name == 'pull_request' }}
launcher triggers: {'workflow_dispatch': {'inputs': {'runner_set': {'description': 'Nền cần đo trong lượt gọi tay', 'required': True, 'default': 'windows-only', 'type': 'choice', 'options': ['windows-only', 'windows-and-ubuntu']}}}, 'push': {'branches': ['master'], 'paths': ['.claude/dev/**', '.github/workflows/launcher-windows.yml']}, 'pull_request': {'types': ['opened', 'synchronize', 'reopened', 'labeled'], 'paths': ['.claude/dev/**']}}
launcher matrix: {'os': '${{ fromJSON(github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\' && \'["windows-latest"]\' || \'["windows-latest","ubuntu-latest"]\') }}'}
launcher if: github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'windows')
workflow .github/workflows/ci-dot-bien-du.yml: runs-on={'dot-bien-du': 'ubuntu-latest', 'dot-bien-manh': 'ubuntu-latest', 'dot-bien-gop': 'ubuntu-latest'}
workflow .github/workflows/ci.yml: runs-on={'chuan-bi': 'ubuntu-latest', 'gate': '${{ matrix.os }}', 'gate-cong-cu': '${{ matrix.os }}', 'gate-cong-cu-gop': '${{ matrix.os }}', 'gate-ops': '${{ matrix.os }}', 'gate-nhanh-manh': '${{ matrix.os }}', 'gate-nhanh-gop': '${{ matrix.os }}', 'gate-registry': '${{ matrix.os }}', 'gate-packet-loop': '${{ matrix.os }}'}
workflow .github/workflows/launcher-windows.yml: runs-on={'launcher': '${{ matrix.os }}'}
workflow .github/workflows/ops-don-ref.yml: runs-on={'don': 'ubuntu-latest'}
workflow .github/workflows/ops-open-pr.yml: runs-on={'mo': 'ubuntu-latest'}
workflow .github/workflows/ops-publish-lease.yml: runs-on={'dang': 'ubuntu-latest'}
workflow .github/workflows/ops-thu-hoi-admission.yml: runs-on={'thu-hoi': 'ubuntu-latest'}
COMMIT 816f43988eb3012726120ad00166a989cc2b9af6
ci triggers: {'push': {'branches': ['master']}, 'pull_request': None, 'workflow_dispatch': {'inputs': {'runner_set': {'description': 'windows-and-ubuntu (mặc định) hoặc windows-only (bỏ các job ma trận Ubuntu)', 'required': False, 'default': 'windows-and-ubuntu', 'type': 'choice', 'options': ['windows-and-ubuntu', 'windows-only']}}}}
gate* count: 8
  gate: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
  gate-cong-cu: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=[{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}]; job-if=None
  gate-cong-cu-gop: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=[{'os': 'windows-latest'}]; job-if=${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
  gate-ops: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
  gate-nhanh-manh: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
  gate-nhanh-gop: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=${{ !cancelled() }}
  gate-registry: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=${{ !cancelled() }}
  gate-packet-loop: os=${{ fromJson(needs.chuan-bi.outputs.os) }}; exclude=None; job-if=None
expanded gate-cong-cu: [{'os': 'ubuntu-latest', 'manh': 0}, {'os': 'ubuntu-latest', 'manh': 1}, {'os': 'ubuntu-latest', 'manh': 2}, {'os': 'ubuntu-latest', 'manh': 3}, {'os': 'ubuntu-latest', 'manh': 4}, {'os': 'ubuntu-latest', 'manh': 5}, {'os': 'ubuntu-latest', 'manh': 6}, {'os': 'ubuntu-latest', 'manh': 7}, {'os': 'windows-latest', 'manh': 0}]
expanded gate-cong-cu-gop: [{'os': 'ubuntu-latest'}]
step conditions using runner.os: 6 [('gate', 'ci-phamvi selftest (phan chung — cong co rang)', "runner.os != 'Windows'"), ('gate-cong-cu', 'actions/upload-artifact@v4', "runner.os != 'Windows'"), ('gate-ops', 'ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)', "runner.os == 'Linux'"), ('gate-ops', 'don-nhanh selftest (chốt xoá nhánh)', "runner.os != 'Windows'"), ('gate-ops', 'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)', "${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"), ('gate-ops', 'gate lifecycle selftest (nen khong co cgroup)', "${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}")]
EOL step: ${{ github.event_name == 'pull_request' }}
launcher triggers: {'workflow_dispatch': {'inputs': {'runner_set': {'description': 'Nền cần đo trong lượt gọi tay', 'required': True, 'default': 'windows-only', 'type': 'choice', 'options': ['windows-only', 'windows-and-ubuntu']}}}, 'push': {'branches': ['master'], 'paths': ['.claude/dev/**', '.github/workflows/launcher-windows.yml']}, 'pull_request': {'types': ['opened', 'synchronize', 'reopened', 'labeled'], 'paths': ['.claude/dev/**']}}
launcher matrix: {'os': '${{ fromJSON(github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\' && \'["windows-latest"]\' || \'["windows-latest","ubuntu-latest"]\') }}'}
launcher if: github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'windows')
workflow .github/workflows/ci-dot-bien-du.yml: runs-on={'dot-bien-du': 'ubuntu-latest', 'dot-bien-manh': 'ubuntu-latest', 'dot-bien-gop': 'ubuntu-latest'}
workflow .github/workflows/ci.yml: runs-on={'chuan-bi': 'ubuntu-latest', 'gate': '${{ matrix.os }}', 'gate-cong-cu': '${{ matrix.os }}', 'gate-cong-cu-gop': '${{ matrix.os }}', 'gate-ops': '${{ matrix.os }}', 'gate-nhanh-manh': '${{ matrix.os }}', 'gate-nhanh-gop': '${{ matrix.os }}', 'gate-registry': '${{ matrix.os }}', 'gate-packet-loop': '${{ matrix.os }}'}
workflow .github/workflows/launcher-windows.yml: runs-on={'launcher': '${{ matrix.os }}'}
workflow .github/workflows/ops-don-ref.yml: runs-on={'don': 'ubuntu-latest'}
workflow .github/workflows/ops-open-pr.yml: runs-on={'mo': 'ubuntu-latest'}
workflow .github/workflows/ops-publish-lease.yml: runs-on={'dang': 'ubuntu-latest'}
workflow .github/workflows/ops-thu-hoi-admission.yml: runs-on={'thu-hoi': 'ubuntu-latest'}
AST extracted: [('nen_bo_qua_dot_bien', 7900, 7902), ('dat_windows', 7905, 7911), ('dong_windows', 7914, 7918), ('main', 8880, 8974)]
MAIN Windows simulated two pass + one skip: rc=0; BỎ QUA skipped: fixture: missing capability |  | cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0 |  | TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
MAIN Windows simulated one failure: rc=1; BỎ QUA skipped: fixture: missing capability |   ĐỎ  bad: fixture: baseline failed |  | cong_cu_test: 1/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0 |  | TỔNG: CA 1/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
MAIN Windows simulated all skipped: rc=1; BỎ QUA skipped: fixture: missing capability |   BỎ QUA skipped: fixture: missing capability |  | cong_cu_test: 0/0 đạt; tổng=2, bỏ qua=2, tiền kiểm bỏ qua=0 |  | TỔNG: CA 0/0 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
MAIN Windows simulated precheck skip: rc=1; BỎ QUA (TIỀN KIỂM) batch: fixture: unavailable |  | cong_cu_test: 2/2 đạt; tổng=2, bỏ qua=0, tiền kiểm bỏ qua=1 |  | TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
nen_bo_qua_dot_bien: {'nt': True, 'posix': False, 'java': False}
Windows runner thật: KHÔNG ĐO ĐƯỢC (môi trường Linux, không gọi mạng).
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — điều kiện YAML và main AST tại exact SHA khớp lời văn; ca thiếu năng lực được loại mẫu số, đột biến không chạy trong nhánh mảnh Windows. Đây là mô phỏng nhánh nt trên Linux, không khai chạy Windows thật.

HƯỚNG 9: Toàn vẹn provenance bằng SHA-256

  giả thuyết : Readback thêm mới hoặc tệp cũ không khớp SHA256SUMS.

  lệnh       : `cd cay-kho && bash -c 'cd ops/land/pr889-claude-md-bai-hoc-c-provenance && sha256sum -c SHA256SUMS.txt'` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
readback-blob-claude-md-094e8d1-6ac385f.txt: OK
readback-check-runs-094e8d1.json: OK
readback-comments-889-sau-review-lai.json: OK
readback-comments-889.json: OK
readback-commit-6ac385f.json: OK
readback-jobs-39917653371.json: OK
readback-jobs-39921552473.json: OK
readback-pr-889.json: OK
readback-reactions-pr-889-sau-review-lai.json: OK
readback-reactions-pr-889.json: OK
readback-review-comments-889.json: OK
readback-reviews-889.json: OK
readback-run-39917653371.json: OK
readback-run-39921552473.json: OK
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — 14/14 tệp OK, rc=0; đây là toàn vẹn snapshot, không phải kiểm GitHub sống.

HƯỚNG 10: Đối chiếu từng lời khai measured, blob và chỉ-thêm

  giả thuyết : Sai comment/timestamp/trạng thái/reaction/blob/diff-stat hoặc khối cũ bị sửa.

  lệnh       : `cd cay-kho && python3 ../review_evidence/provenance_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
comment 6366307732: author=ducthangho; created_at=2026-10-23T13:43:34Z; updated_at=2026-10-23T13:43:34Z
comment 6366338141: author=chatgpt-codex-connector[bot]; created_at=2026-10-23T13:45:03Z; updated_at=2026-10-23T13:45:03Z
comment 6360319005: author=chatgpt-codex-connector[bot]; created_at=2026-10-23T08:00:09Z; updated_at=2026-10-23T13:45:05Z
request body: @codex review

Lượt connector trước trên head đã merge `094e8d1` (comment 6360319005) vẫn ở trạng thái `running` từ 08:00:05Z và chưa có kết quả. Nhờ chấm lại đúng `094e8d17ae4dfcf21dca63702c9262267bdc072c`. Hồ sơ land ghi khoảng trống này ở `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml` (`HEAD-MERGE-KHONG-CO-REVIEW-HOAN-TAT`).
receipt body: <!-- codex-review-receipt:v1 -->

Codex Review: Didn't find any major issues. Bravo.

**Reviewed commit:** `6ac385fdd7`
old summary: {"commit_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "has_any_findings": null, "has_unresolved_findings": null, "status": "running"}
new summary: {"commit_sha": "6ac385fdd7325f532ac4b4b6eb861292bfa7e970", "has_any_findings": false, "has_unresolved_findings": false, "status": "completed"}
readback-reactions-pr-889.json [('chatgpt-codex-connector[bot]', 'eyes', '2026-10-23T08:00:12Z')]
readback-reactions-pr-889-sau-review-lai.json [('chatgpt-codex-connector[bot]', '+1', '2026-10-23T13:45:08Z')]
PR #891 merge in committed history:
8324567788caab8dc332d45df458ef415fd305be
1d7e642092fb3dda15967be44d095f37bb22ac5f 0390130f57c8f6fdd3b69de79ae49e6618ef3d3c
2026-10-23T20:39:35+07:00
Merge pull request #891 from ducthangho/claude/gallant-fermat-34kgb9

ghi so(#870, #889): verdict cross-review #889 vao ops/reviews + ho so land cho #870 va #889

Chu kho duyet landed cho #870 va #889 tren head 0390130 (comment 6366218495, OWNER, 13:39:08Z sau commit cuoi 13:01:10Z).
Gate ci.yml run 39957796185 xanh tren 0390130; Codex connector review 0390130 khong co gop y.
request after #891 merge: True
CLAUDE.md blobs at 094e8d1 / 6ac385f: ['975cd94ff851a3a0ee3aa0493e90184e5f81c874', '975cd94ff851a3a0ee3aa0493e90184e5f81c874']
$ git diff --stat 094e8d1 6ac385f
 .claude/hooks/subagent_ghi_detect_test.py | 70 ++++++++++++++++++++++++++++++-
 ops/land_evidence_nguon_test.py           | 12 ++++--
 2 files changed, 77 insertions(+), 5 deletions(-)
blob readback stat byte-for-byte lines: True
master changes #872/#877:
9d4cb6a Merge pull request #872 from ducthangho/claude/wizardly-noether-zqqoae
daf8961 Merge pull request #877 from ducthangho/agent/wp854-g1-claude
land-evidence prefix unchanged from base and 0390130: True; old lines= 146 ; added lines= 27
$ git diff --numstat <base> <head> -- ops/land/
27	0	ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml
3	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/SHA256SUMS.txt
6	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-blob-claude-md-094e8d1-6ac385f.txt
436	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-comments-889-sau-review-lai.json
29	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-reactions-pr-889-sau-review-lai.json
land diff: removed content lines=0
6366218495 references available at reviewed SHA: ['816f43988eb3012726120ad00166a989cc2b9af6:ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml']
comment #891 6366218495 body/authorization and measurement timestamp 15:16:09Z: KHÔNG ĐO ĐƯỢC independently; no raw readback in this tree.
Current GitHub status: KHÔNG ĐO ĐƯỢC; observations limited to frozen before/after readbacks.
All measured fields with cited readback: matched.
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI với mọi measured có readback được trích — assertions đều đạt; body comment quyết định #891/đồng hồ thu nhận không có chứng cứ độc lập. Giữ giới hạn đó, không suy cùng SHA từ cùng blob.

HƯỚNG 11: Lịch sử ba lần trôi, run 23 job và runner chưa chạy

  giả thuyết : Các mốc #548/#870/#878/#879/#889 hoặc 23/23 Ubuntu/3f6c694/#865 không khớp Git và readback.

  lệnh       : `cd cay-kho && python3 ../review_evidence/history_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
HISTORY a612c70 2026-09-17T21:13:08+07:00 Merge pull request #549 — packet #546 MOI-TRUONG-CONG-CU-DO-DUOC r1/g1
before chuan-bi matrix: ${{ fromJSON( (github.event_name == 'workflow_dispatch' || github.ref == 'refs/heads/master' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]') }}
CLAUDE.md (c) first lines:   · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
  còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
gate-cong-cu.exclude: None
HISTORY d705623 2026-09-18T00:51:04+07:00 Merge pull request #550 — packet #548 CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND r2/g2
chuan-bi.outputs.os: ${{ (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
CLAUDE.md (c) first lines:   · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
  còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
gate-cong-cu.exclude: None
HISTORY 5f288ea 2026-10-22T16:05:33+07:00 Merge pull request #870 from ducthangho/claude/gallant-fermat-34kgb9
chuan-bi.outputs.os: ${{ (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
CLAUDE.md (c) first lines:   · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
  Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
  Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
  `github.ref == 'refs/heads/master'` khỏi output `os` của job `chuan-bi`). **Đo 22-10-2026** trên
  `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
  HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
gate-cong-cu.exclude: None
HISTORY 747f983 2026-10-23T08:19:34+07:00 Merge pull request #880 from ducthangho/agent/wp878-g1-claude
chuan-bi.outputs.os: ${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only') && '["windows-latest"]' || (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
CLAUDE.md (c) first lines:   · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
  Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
  Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
  `github.ref == 'refs/heads/master'` khỏi output `os` của job `chuan-bi`). **Đo 22-10-2026** trên
  `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
  HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
gate-cong-cu.exclude: None
HISTORY e63961f 2026-10-23T11:04:54+07:00 Merge pull request #883 from ducthangho/agent/wp879-g1-claude
chuan-bi.outputs.os: ${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only') && '["windows-latest"]' || (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
CLAUDE.md (c) first lines:   · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
  Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
  Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
  `github.ref == 'refs/heads/master'` khỏi output `os` của job `chuan-bi`). **Đo 22-10-2026** trên
  `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
  HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
gate-cong-cu.exclude: [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}]
HISTORY 6ac385f 2026-10-23T14:59:59+07:00 Merge pull request #889 from ducthangho/claude/gallant-fermat-34kgb9
chuan-bi.outputs.os: ${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only') && '["windows-latest"]' || (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
CLAUDE.md (c) first lines:   · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
  Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
  Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
  `github.ref == 'refs/heads/master'` khỏi output `os` của job `chuan-bi`). **Đo 22-10-2026** trên
  `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
  HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
gate-cong-cu.exclude: [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}]
three changes: #548 removed master; #878 added dispatch windows-only; #879 reduced Windows G5.
git history for correction #865:
fa362fd985b708190eb848bc0dbceeab44cfeb75
6ac385fdd7325f532ac4b4b6eb861292bfa7e970 a15d04ed44b13e8b87306faab259239d3f43dedf
Merge pull request #865 from ducthangho/claude/fix-859-ubuntu-only

land(#744): đính chính gate post-merge 3a3a3ca — chỉ Ubuntu (connector P1 #859)
correction 4ae43f0 relevant lines:
    land(#744): dinh chinh gate post-merge 3a3a3ca — chi ubuntu, khong gom windows (connector P1 #859)
-  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
+  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success, ca 23 job chi nhan ubuntu-latest (measured — readback-jobs-39354156843.json); Windows KHONG chay tren lan push nay', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
+  - 'launcher-windows/Windows KHONG chay cho push 3a3a3ca: ci.yml chi chon windows-latest cho workflow_dispatch hoac PR gan nhan windows; Windows khong phai dieu kien cua lease (M-3 chi doi ci.yml). Ban dau ho so ghi sai "gom windows" — connector P1 #859 r4323607674, dinh chinh o PR sau.'
3f6c694 original assertion:   - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
run 39354156843: {'id': 39354156843, 'path': '.github/workflows/ci.yml', 'event': 'push', 'head_branch': 'master', 'head_sha': '3a3a3caca5de4934ff53851feb6994c2c7b84ad5', 'status': 'completed', 'conclusion': 'success', 'created_at': '2026-10-20T01:34:09Z'}
jobs count: 23 23 unique ids= 23
labels: {('ubuntu-latest',): 23}
conclusions: {'success': 23} runner_id0= 0
readback-jobs-39745387589.json jobs= 46 runner_id0= 22 zero steps= Counter({0: 22}) zero conclusions= Counter({'failure': 22})
readback-jobs-39752735359.json jobs= 23 runner_id0= 0 zero steps= Counter() zero conclusions= Counter()
Raw GitHub comment r4323607674/P1 author: KHÔNG ĐO ĐƯỢC; committed correction attributes it, raw comment absent.
PR #109 historical second-P2 claim (unchanged context):
9796f67 Merge pull request #109 — ba lần đọc sai tín hiệu trong một phiên
3736fc0 docs: gắn nhãn windows KHÔNG đủ cho PR đang mở — phải có cò mới
05170b4 docs: nói CÓ ĐIỀU KIỆN câu về đo Windows — ma trận có nhãn windows và workflow_dispatch
Measurement dates 22/23-10 are author timing declarations; file behavior independently re-evaluated, actual local execution time then not recoverable.
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI với những mốc đo lại được; phân biệt raw GitHub comment r4323607674 và đồng hồ đo cũ là KHÔNG ĐO ĐƯỢC, không dùng lời khai cũ làm chứng minh độc lập.

HƯỚNG 12: Ranh giới bảo đảm của t162 với exclude và if

  giả thuyết : Lời văn hành vi ấy và đọc ca ấy là đọc ma trận hiện hành gán toàn bộ ma trận job cho t162.

  lệnh       : `cd cay-kho && python3 ../review_evidence/test_scope_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
baseline t161:PASS; t162:PASS ; ci_dang_ky.loi_g5_workflow= []
remove_windows_shard1_exclusion t161:PASS; t162:PASS ; ci_dang_ky.loi_g5_workflow= ["gate-cong-cu: matrix phải đúng os + manh [0, 1, 2, 3, 4, 5, 6, 7] + exclude [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}], thấy {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': [0, 1, 2, 3, 4, 5, 6, 7], 'exclude': [{'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}]}"]
remove_gop_if t161:PASS; t162:PASS ; ci_dang_ky.loi_g5_workflow= ['gate-cong-cu-gop: needs/if phải đúng [\'chuan-bi\', \'gate-cong-cu\']/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), \'ubuntu-latest\') }}", thấy [\'chuan-bi\', \'gate-cong-cu\']/None']
Scope: t162 validates chuan-bi.outputs.os; exclude/job-if are separately checked by ci_dang_ky_test.py, not t162.
No assertion that the complete gate remains green on these mutants.
rc=0
```

  kết luận   : LỖI — P2: t162 chỉ đánh giá outputs.os; exclude/if mức job phải đọc riêng và được checker khác kiểm. Hai đột biến đổi nền job đều qua t161/t162; loi_g5_workflow riêng bắt được. Không kết luận toàn bộ gate xanh.

HƯỚNG 13: Kiểm gợi ý vá patch -p0 trên scratch

  giả thuyết : HINT.patch sai đường dẫn, sai neo hoặc chạm tệp ngoài finding.

  lệnh       : `cd cay-kho && python3 ../review_evidence/hint_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
$ patch -p0 --dry-run -i /tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/HINT.patch
checking file CLAUDE.md
rc=0
$ patch -p0 -i /tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/HINT.patch
patching file CLAUDE.md
rc=0
patched scratch content matches intended wording; source CLAUDE.md unchanged: True
HINT.patch only changes CLAUDE.md; no workflow/test/runtime hunks.
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — dry-run và apply thật trên scratch đều rc=0, chỉ CLAUDE.md; chưa áp lên cây thật, executor tự áp/tự đo/tự chịu trách nhiệm commit.

HƯỚNG 14: Toàn vẹn cuối và đối chiếu diff đầu vào

  giả thuyết : Repo đã bị thay đổi, SHA/tree stale hoặc diff.patch không đúng phạm vi base/head.

  lệnh       : `cd cay-kho && python3 ../review_evidence/final_integrity_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
HEAD: 816f43988eb3012726120ad00166a989cc2b9af6
tree: 3da0ce24590dfcf2e60805b2bef76687cdd64405
git status --porcelain=v1 --untracked-files=all --ignored: rc=0; output=''; stderr=''
git diff --exit-code: rc=0; output=''; stderr=''
git diff --cached --exit-code: rc=0; output=''; stderr=''
tracked blob content compared to HEAD: 5203 ; mismatches= ['scripts/deploy-package.cmd', 'scripts/don-nhanh.cmd', 'tl-setup.cmd']
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr896.9C93/cay-kho/../review_evidence/final_integrity_probe.py", line 35, in <module>
    assert not failures
           ^^^^^^^^^^^^
AssertionError
rc=1
```

  kết luận   : KHÔNG PHẢI LỖI nguồn — phép kiểm byte thô rc=1 do ba checkout cmd có CRLF theo attributes. Lệnh ở đây là bản script trước khi thêm xử lý attributes; giữ output thật và giải quyết ở H15.

HƯỚNG 15: Phân biệt byte checkout CRLF với blob LF; hoàn tất toàn vẹn

  giả thuyết : Ba tệp cmd lệch byte thô ở hướng 14 là thay đổi nguồn do review.

  lệnh       : `cd cay-kho && python3 ../review_evidence/final_integrity_probe.py` (PYTHONDONTWRITEBYTECODE=1)

  output     :

```text
HEAD: 816f43988eb3012726120ad00166a989cc2b9af6
tree: 3da0ce24590dfcf2e60805b2bef76687cdd64405
git status --porcelain=v1 --untracked-files=all --ignored: rc=0; output=''; stderr=''
git diff --exit-code: rc=0; output=''; stderr=''
git diff --cached --exit-code: rc=0; output=''; stderr=''
tracked blob content compared to HEAD: 5203 ; mismatches= ['scripts/deploy-package.cmd', 'scripts/don-nhanh.cmd', 'tl-setup.cmd']
scripts/deploy-package.cmd: text: set
scripts/deploy-package.cmd: eol: crlf
scripts/deploy-package.cmd: filter: unspecified
scripts/deploy-package.cmd work CRLF= 59 blob CRLF= 0 normalize_CRLF_matches= True filtered_hash_matches= True
scripts/don-nhanh.cmd: text: set
scripts/don-nhanh.cmd: eol: crlf
scripts/don-nhanh.cmd: filter: unspecified
scripts/don-nhanh.cmd work CRLF= 72 blob CRLF= 0 normalize_CRLF_matches= True filtered_hash_matches= True
tl-setup.cmd: text: set
tl-setup.cmd: eol: crlf
tl-setup.cmd: filter: unspecified
tl-setup.cmd work CRLF= 6 blob CRLF= 0 normalize_CRLF_matches= True filtered_hash_matches= True
5200 raw matches + 3 declared CRLF checkout matches = 5203 correct files
provided diff.patch equals git diff base head: True
actual numstat:
31	34	CLAUDE.md
27	0	ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml
3	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/SHA256SUMS.txt
6	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-blob-claude-md-094e8d1-6ac385f.txt
436	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-comments-889-sau-review-lai.json
29	0	ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-reactions-pr-889-sau-review-lai.json
Reviewed source remains exact; only report/evidence/hint written outside cay-kho/.
Snapshot equality does not prove absence of temporary historical writes; commands were constrained to read-only source and external scratch.
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI — .gitattributes khai text/eol=crlf cho đúng ba tệp; normalize và git hash-object có clean-filter đều khớp HEAD. Hướng 14 thất bại vì phép kiểm byte thô chưa xét checkout attributes, không phải gate sản phẩm đỏ. HEAD/tree/status/index và diff đầu vào khớp.

### t162-khong-khoa-toan-bo-ma-tran-job [P2] Thu hẹp lời khẳng định về phạm vi của t162

TỆP/DÒNG: `CLAUDE.md:171–173` (tại reviewed_sha nêu đầu báo cáo).

VẤN ĐỀ: Gạch đầu dòng trước định nghĩa ma trận dự kiến là `outputs.os` cộng `exclude:` và `if:` cấp job. Gạch sau gọi **“hành vi ấy”** là thứ `t162` khoá, rồi kết luận **“đọc ca ấy là đọc ma trận HIỆN HÀNH”**. Nhưng `t162` chỉ lấy `jobs.chuan-bi.outputs.os` và assert các context của biểu thức đó; nó không đọc hai trường còn lại. Vì thế người chỉ đọc ca theo hướng dẫn vẫn bỏ sót phần quyết định Windows có chạy mảnh/gom hay không. Đây là khai rộng hơn phép đo (P2), không phải phát hiện gate tổng đang bỏ lọt cấu hình sai.

ĐÃ THỬ NGHIỆM: `cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review_evidence/test_scope_probe.py` (H12, rc=0). Baseline: t161 PASS, t162 PASS, `loi_g5_workflow=[]`. Trong bản sao YAML ngoài repository: bỏ duy nhất `{os: windows-latest, manh: 1}` khỏi exclude, hoặc bỏ `gate-cong-cu-gop.if`, đều t161 PASS/t162 PASS. Checker khác `ci_dang_ky_test.py:loi_g5_workflow` mới báo lỗi matrix/needs-if tương ứng. H4 cũng cho thấy các đột biến giá trị của output os thật đều làm t162 đỏ. Không nói toàn bộ gate còn xanh với các mutant exclude/if.

ĐỘ TIN: cao về phạm vi đọc/assert của ca và phản chứng; mức P2 do lời văn bao trùm quá phạm vi đó.

GỢI Ý VÁ: Sửa đúng `CLAUDE.md:171–173`, vì lỗi nằm ở hướng dẫn tìm nguồn. Nói rõ t162 khoá **riêng output os**, vẫn đọc exclude/job-if ở ci.yml; nếu muốn trỏ chốt G5 thì trỏ `loi_g5_workflow` trong `.claude/dev/ci_dang_ky_test.py` cho đúng hai job mảnh/gom. Không cần đổi mã test hay mở rộng ca t162 để vá lỗi tài liệu này. HINT kèm theo làm đúng phạm vi đó.

CA KHOÁ/PHẢN CHỨNG: Dùng H4/H12: mutant output os phải làm t162 đỏ; mutant exclude/if phải được checker đúng bắt, đồng thời chứng minh t162 không kiểm chúng. Sau chỉnh tài liệu, chạy hai cổng tài liệu bắt buộc và đọc đối chiếu lại source của từng con trỏ. Không thêm test chỉ so lại chính câu văn.

NGUY CƠ CỦA GỢI Ý: Con trỏ tới `loi_g5_workflow` có thể bị đọc quá rộng thành mọi gate*. Vì vậy HINT giới hạn rõ **phần mảnh/gom của gate-cong-cu***; ci.yml vẫn là nguồn phải đọc cho các job còn lại. Không sửa cấu hình gate hoặc hành vi chạy.

`HINT.patch`: định dạng `patch -p0` từ gốc `cay-kho/`, đã dry-run và áp thử trên scratch (H13, cả hai rc=0). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Executor dùng hint cần khai `hint_provenance` theo protocol; đây chỉ là artifact đề xuất của reviewer.

## CỔNG VÀ GIỚI HẠN

- `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **passed, rc=0**, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- `python3 scripts/tl.py doc-claims-check --json`: **passed, rc=0**, `"ok": true`, `flags=[]`, `layers_skipped={}`, 381 advisory; toàn bộ JSON ở `review_evidence/6.log`.
- `python3 ops/land_evidence_nguon.py --root . --tep ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml`: **passed, rc=0**, `TỔNG: ĐẠT` (1 ĐẠT, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC).
- `sha256sum -c SHA256SUMS.txt` trong provenance: **passed, rc=0**, 14/14 OK. `t161` và `t162` chạy riêng: **passed, rc=0**, mỗi selector 1/1 đạt.
- Chưa chạy full gate/bán kính, Windows thật hoặc GitHub Actions mới (**not_run**). Không có mạng để xác nhận raw comment `r4323607674`, raw owner decision `6366218495`, finding thứ hai #109 hoặc trạng thái GitHub hiện tại (**not_measured**); commit message/correction chỉ là dấu vết đã lưu, không là raw API. Ngày giờ tác giả thu readback không có transport receipt độc lập. Không coi các giới hạn này là pass hoặc tự suy thành lỗi.
- Hướng 14 là **failed probe** do chưa xét eol=crlf, đã giải quyết ở H15; không phải gate sản phẩm fail. Ba cmd có CRLF đúng attributes; 5.200 blob byte thô và 3 blob qua chuẩn hoá đều khớp HEAD. Trước/sau: HEAD/tree không đổi, tracked/index diff rc=0, untracked/ignored rỗng. Các snapshot này chứng minh không có delta quan sát được, không khẳng định lịch sử không từng có ghi-hoàn-nguyên. Không sửa `cay-kho/`, không push, không gọi mạng.
