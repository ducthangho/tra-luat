reviewed_sha: aad4865c734e7c146463b13ed1750a47e6a9cb8f
reviewed_tree: dce456c90ddffaef089140293e77de2cbb502c48
base_sha: 9091cf52cf20ac197c1a356d6a33cac6bab0b318
spec_sha256: 72b63a79e0b63193904aaa5378ffd266bce1eb0322cf8c4e425c5b7d9a58f7f8
windows: not_required (ghi nhận quyết định chủ kho tại đặc tả; không chạy Windows)
review_class: sensitive
provider: openai_codex
model: GPT-6 theo cấu hình phiên; không xác minh độc lập model/effort đã phục vụ
execution_surface: codex_service (agent gọi shell trực tiếp, không qua lệnh codex hoặc Desktop)
transport: machine
findings: []

Kết luận nội dung: approve trên đúng SHA nêu trên. Không phát hiện P0–P3 mở sau khi review lại toàn bộ diff base..head, theo hai trục Spec và Standards/Security. M1 không cần waiver P3. Không tự nâng assurance hoặc cấp quyền merge từ tệp này; identity/receipt của lượt chạy do bên nhận xác minh.

CHƯA ĐỦ ĐIỀU KIỆN MERGE trong phạm vi bằng chứng tôi xác minh được: thiếu readback A9 (full_mutant_audit tại head cuối và kiem-merge rc 0), A10 (CI PR tại head cuối, labels từng job), connector Reviewed commit đúng SHA, và xác minh độc lập kết quả chạy GitHub A5. A1 full suite không chạy trong lượt review này theo chỉ thị; executor chạy riêng. Các mục thiếu quan sát không được ghi là pass. A11 là hậu kiểm sau land, không phải finding trước land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / lớp | Nguồn | Kết quả tự kiểm trên head này | Bằng chứng |
|---|---|---|---|
| F1 P3 / concurrency-comment-permanent-gap | Lượt 1, 024212c1f565858788edc0b3e48fdf8a356ac8b4; VERDICT-luot1.md là bản ghi dở | **ĐÃ VÁ THẬT** | `git show aad4865` và `.github/workflows/ci.yml:54–58`: bỏ “không bao giờ được gate”, thay bằng mất lượt gate **tự động**, ghi nhận chạy lại hoặc dispatch đúng SHA. `comments.json` xác nhận câu cũ vắng, câu mới có mặt, không có cú pháp mở biểu thức Actions trong chú thích. |

Đã đối chiếu thêm chú thích launcher tại `.github/workflows/launcher-windows.yml:39`: nói về lượt pending bị thay chỗ, không tuyên bố commit vĩnh viễn không thể gate. Không phát hiện biểu hiện cùng lớp còn mở hoặc do bản vá sinh ra. Bảng lớp kế thừa: 1 lớp / 1 biểu hiện đã đóng; 0 lớp / 0 biểu hiện mở. Phép đo đóng lớp là nội dung chú thích hiện tại và lint; không mượn kết quả suite để đóng lỗi nghĩa của câu.

## Đối chiếu từng mục §2

- §2.1: cả `.github/workflows/ci.yml:59` và `.github/workflows/launcher-windows.yml:40` chứa đúng từng byte chuỗi group đóng băng. `cancel-in-progress` ở dòng 60/41 giữ nguyên biểu thức cũ. Các chú thích mới giải thích pending/group theo SHA, có #1132, không chứa nội suy Actions.
- §2.2: `ops/ci_duong_nhanh_test.py:2705–2710` định nghĩa GROUP_CU/GROUP_MOI/HUY_CHUAN; KHUNG_TOP dùng GROUP_MOI đúng đặc tả. Ca `y13b` ở dòng 2918–2927 đọc YAML **cả hai** workflow, so toàn chuỗi group và cancel, không so chuỗi con. `_lw` và LW thêm đích đột biến cho launcher; bảng ở dòng 3754–3757 có hai đột biến mới, đúng ca đích. Đột biến cũ `yml_concurrency_luon_huy` vẫn hoạt động.

## Ngữ nghĩa trên mọi sự kiện khai báo

Đặt W = tên workflow (`gate` hoặc `launcher (Windows that)`), N = số PR, S = github.sha, R = github.ref. `&&`/`||` trả **giá trị toán hạng** qua short-circuit: vế master trả chuỗi SHA có giá trị truthy, không trả boolean `true`. Đối chiếu mã chính thức [And.cs](https://raw.githubusercontent.com/actions/runner/main/src/Sdk/DTExpressions2/Expressions2/Sdk/Operators/And.cs) và [Or.cs](https://raw.githubusercontent.com/actions/runner/main/src/Sdk/DTExpressions2/Expressions2/Sdk/Operators/Or.cs). Các context này được phép tại concurrency; [GitHub contexts](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts) mô tả ref/SHA và thuộc tính không tồn tại trả chuỗi rỗng.

| Sự kiện | Group cũ → mới | cancel-in-progress | Đối chiếu |
|---|---|---|---|
| pull_request opened, synchronize, reopened, cả hai workflow | W-N → W-N | true | Không đổi; PR mới cùng N hủy lượt cũ. |
| pull_request labeled, chỉ launcher | W-N → W-N | true | Không đổi; lọc paths và `if` nhãn windows của job cũng giữ nguyên. |
| PR thiếu số trong context nhưng ref vẫn refs/pull/N/merge | W-R → W-R | true | Vế master không đúng, fallback giống cũ; không suy rằng thiếu số làm mọi PR chung group. |
| push master tại SHA S | W-refs/heads/master → W-S | false | Hai SHA khác nhau tách group. Launcher chỉ phát run khi paths đã khai khớp; patch không mở rộng trigger. |
| workflow_dispatch master tại SHA S | W-refs/heads/master → W-S | false | Tách theo commit, giữ lượt đang chạy. |
| workflow_dispatch nhánh khác master hoặc tag | W-R → W-R | true | Giữ hành vi cũ. |
| push nhánh khác master hoặc tag | Không tạo run ở hai workflow này | — | Bộ lọc push chỉ nhận master; nếu xét riêng công thức trên ref khác thì vẫn W-R như cũ. |

Các loại PR mặc định và ref của dispatch đối chiếu [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows). `labeled` là activity của pull_request, không phải event riêng. Hai workflow có tên khác nhau, không va group giữa chúng.

Không tìm thấy cặp **khác SHA** trên refs/heads/master rơi chung group trong các sự kiện hợp lệ đã khai, cũng không tìm thấy PR đổi hành vi concurrency. Các workflow không khai sự kiện PR closed/merged nên không áp context của sự kiện ấy để tạo phản ví dụ.

Hai run cùng SHA master, kể cả push + dispatch hoặc hai bộ input dispatch khác nhau, vẫn chung W-S; lượt pending thứ ba có thể thay lượt pending trước, đúng ngoại lệ §2.1. Đây không phải cam kết mọi lần dispatch đều chạy. Việc tách group cho phép master tranh slot runner và không bảo đảm success hoặc FIFO toàn master. Với mặc định queue của hai tệp, `cancel-in-progress: false` bảo vệ running nhưng không bảo vệ pending cũ; đối chiếu [GitHub concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency). Chú thích mới được đọc trong phạm vi nguyên nhân hủy do concurrency; không còn khẳng định vĩnh viễn của F1.

Phép đối chiếu scalar độc lập `python -B out/review_checks.py semantics`: rc 0, 44 context (hai SHA cho push/dispatch master, PR từng activity có/thiếu số, dispatch nhánh/tag). Kết quả trong `semantics.json`. Đây là mô hình toán hạng kiểm lại lập luận, **không** phải thực thi biểu thức trên máy chủ GitHub.

## Đo răng test và các đột biến SỐNG

Hai lệnh bắt buộc chạy từ chính `kho`, PYTHONDONTWRITEBYTECODE=1:

- `python ops/ci_duong_nhanh_test.py --mot-ca y13b_concurrency_master_theo_sha`: rc 0, stdout/stderr rỗng.
- `python ops/ci_duong_nhanh_test.py --mot-ca y13_khoa_topology_cua_ci_yml_ngoai_than_run`: rc 0, stdout/stderr rỗng.

Đã đọc registry CA và `main`: hai ca tồn tại, được gọi trực tiếp; ca không có nhánh skip. Đối chứng mutation cho thấy ca thực sự thất bại bằng TinHieuChotCa, không dựa riêng vào output rỗng/rc 0.

Ba đột biến trong bảng được gọi qua chính `chay_mot_dot_bien`: baseline từng ca phải xanh, neo thay duy nhất, sau đó đúng ca trả `DO:<tên>:`/rc 3. Kết quả `registered-mutants.json`:

| Đột biến đăng ký | Ca đích | Kết quả |
|---|---|---|
| yml_concurrency_luon_huy | y13 | GIET |
| yml_concurrency_group_ve_ref | y13 và y13b | GIET bởi cả hai |
| launcher_concurrency_group_ve_ref | y13b | GIET |

Thử thêm trên hai clone tạm ngoài kho; mỗi lần chỉ đổi một workflow, rồi phục hồi trước lần kế tiếp:

| Biến thể | ci: y13b / y13 | launcher: y13b / y13 |
|---|---|---|
| Đưa group về bản cũ | GIET / GIET | GIET / **SỐNG** |
| cancel-in-progress: true | GIET / GIET | GIET / **SỐNG** |
| cancel-in-progress: false | GIET / GIET | GIET / **SỐNG** |
| Group tương đương nhưng khác byte: đảo hai toán hạng phép so ref với chuỗi master | GIET / GIET | GIET / **SỐNG** |
| Thay workflow bằng toàn bộ nội dung workflow tại base, từng tệp riêng | GIET / GIET | GIET / **SỐNG** |

Tất cả GIET ở bảng trên là rc 3 và đúng tiền tố `DO:<ca>:`; mọi SỐNG là rc 0. **Có năm biến thể launcher SỐNG trước y13 đơn lẻ**, vì y13 chỉ khóa ci.yml. Không có biến thể nào sống qua cả hai ca; y13b bù đúng chỗ thiếu ấy. Có 8 biến thể tự thử, cộng 2 phép đo workflow base; không gọi đây là full mutant audit. Chuỗi tương đương khác byte bị bắt đúng yêu cầu khóa nguyên văn, không phải lỗi của test.

Phản chứng A2 (giữ tệp test head; thay từng workflow bằng `git show <base>:.github/workflows/<tệp>` trên clone tạm). Cùng lệnh y13b ở trên, rc 3 ở cả hai phép độc lập:

```text
DO:y13b_concurrency_master_theo_sha:ci.yml: concurrency.group = '${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', phai = "${{ github.workflow }}-${{ github.event.pull_request.number || (github.ref == 'refs/heads/master' && github.sha) || github.ref }}"
DO:y13b_concurrency_master_theo_sha:launcher-windows.yml: concurrency.group = '${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', phai = "${{ github.workflow }}-${{ github.event.pull_request.number || (github.ref == 'refs/heads/master' && github.sha) || github.ref }}"
```

Bằng chứng đầy đủ và lệnh con nằm trong `targets.json`, `registered-mutants.json`, `custom-mutants.json`; script tái lập `review_checks.py`.

## M2 — quét theo lớp

lop_da_quet:
- master-ref-group-pending-replacement: group dùng chung một ref làm pending của commit trước bị thay chỗ; quét mọi concurrency cấp workflow/job trong cả 8 tệp YAML. Chỉ hai gate push master có biểu hiện cần vá, và cả hai đã vá.
- pr-concurrency-behavior-drift: xét mọi activity khai báo, ref và toán hạng PR; không thấy biểu hiện mới.
- concurrency-exact-string-test-coverage: cả hai tệp, group, cancel, đột biến đăng ký và biến thể tương đương khác byte; không còn thiếu coverage mà §2 yêu cầu.
- concurrency-comment-permanent-gap: lớp F1 kế thừa đã đóng; quét chú thích mới của cả hai tệp.

| Vị trí cùng họ cố định/theo ref, không được packet vá | Concurrency / trigger | Có thật sự gác master? |
|---|---|---|
| ops-don-ref.yml:65–67 | group cố định `ops-don-ref`, cancel=false; chỉ workflow_dispatch | Không. Vận hành dọn ref, không gate từng push master. |
| ops-open-pr.yml:23–25 | group theo github.ref, cancel=true; push claude/** hoặc ops/** | Không. Tạo PR; không nhận push master. |
| ops-publish-lease.yml:52–54 | group theo github.ref, cancel=false; push ops/**, lọc paths lease | Không. Đăng lease; có khả năng thay pending cùng ref về cơ chế chung, nhưng không phải gate phát hành mỗi commit master. |
| ops-thu-hoi-admission.yml:41–43 | group theo số PR, cancel=false; pull_request_target nhắm master | Là admission PR vào master; **không** phải gate push master hay group chung cho mọi commit master. |
| ci-dot-bien-du.yml | Không có concurrency ở workflow hoặc job; schedule/dispatch | Là full_mutant_audit theo yêu cầu vận hành; không có cơ chế thay pending cùng group trong lớp này. |
| ops-do-workflow-definition.yml | Không có concurrency; chỉ dispatch | Đo provenance, không gate từng push master. |

`ci.yml` push master không lọc paths; `launcher-windows.yml` push master có lọc paths như trước. Không báo launcher không chạy trên commit ngoài paths là regression. Không có concurrency cấp job ở cả tám tệp. Inventory YAML được lưu ở `workflows.json` và đã đối chiếu trigger nguyên văn; không chỉ tìm chuỗi “master”.

## Đối chiếu A1–A11

| Tiêu chí | Kết quả của lượt này |
|---|---|
| A1 | **not_run full suite.** Không chạy `python ops/ci_duong_nhanh_test.py` không đối số; không có dòng CA:/DOT BIEN:/TONG: để trích. Theo chỉ thị, executor chạy riêng. Registry đo bằng import base/head: 113→114 ca (+1), 419→421 đột biến (+2); không dùng số này thay kết quả thực thi. |
| A2 | Đối chứng workflow base đỏ ở từng tệp, đúng assertion y13b như trên. Đây là tái lập độc lập hiện tại, không xác nhận trình tự executor đã chạy trước khi sửa. |
| A3 | Hai mutation mới và mutation cũ đều GIET đúng ca; các phép thử thêm cũng bắt được. |
| A4 | actionlint 1.7.7 trên **đúng hai workflow**: base rc 0, head rc 0, cả stdout/stderr rỗng, delta 0. shellcheck **vắng**, không tuyên bố đã lint shell. |
| A5 | **Chỉ xác minh được cấu hình thí nghiệm qua Git objects**, chưa xác minh được run/job GitHub. Chi tiết dưới đây. |
| A6 | Đạt: đúng bốn tệp trong write set, +131/-4; spec +95/0; dưới trần 450 dòng thêm. Đặc tả khớp hash đóng băng. |
| A7 | Đạt phép đo chữ: `rg -n -F 'phải chạy trọn' .github/workflows/ci.yml` rc 1, rỗng; nối chú thích concurrency có “một lượt pending” và #1132, không có ký hiệu mở biểu thức Actions. Đã đọc nghĩa để đóng F1, không chỉ dựa rg. |
| A8 | doctrine-scan, adr-song, doc-claims-check strict: base và head đều rc 0; từng cặp stdout/stderr trùng byte. doctrine-scan: 10 tệp/0 chỗ chép; adr-song: 59 ADR/59 dòng; doc-claims-check: ok=true, flags=[], advisory_count=381 giống nền, không có layer skip. |
| A9 | **khong_do_duoc** success full_mutant_audit trên aad4865... và kiem-merge/readback. Không dùng run trên 024212c... thay head cuối. |
| A10 | **khong_do_duoc** CI PR/labels jobs/connector trên exact head; không kế thừa trạng thái queued của lượt trước thành kết quả. |
| A11 | **Chưa đo, chỉ sau land**: executor/phiên land cần kiểm hai push master đầu sau merge, có job runner_id khác 0, không canceled do concurrency; nếu thất bại mở lại #1132. Không merge hay push thử trong review read-only. |

## A5 — bằng chứng phân biệt với lời khai

Đọc được `git rev-parse --verify <sha>^{commit}` và `git show <sha>:.github/workflows/thu-concurrency.yml` cho cả 8 commit; mỗi lệnh rc 0. Nội dung cả 4 workflow vế cũ đồng nhất hash SHA-256 `a4a43c548876cc143aee7ae2f4608ba6256becb8ed0e260f917aaf19ffa8c879`; cả 4 vế mới đồng nhất `2b7ff43f82492ff9d5d520c239dd0e86f426b7d288d96a2d66248a82b002b3c5`. Tệp chỉ nhận push đúng nhánh thử, một job ubuntu sleep 120, cancel expression dùng đúng ref nhánh thử. Vế mới thay master bằng ref nhánh thử đúng đặc tả. Dữ liệu: `a5-local-objects.json`.

| Vế | SHA đầy đủ tự đọc từ kho | Run ID / kết quả do prompt cung cấp, **chưa readback độc lập** |
|---|---|---|
| Cũ mồi | fce9580b04caccadd8ea3bd6a51e79785451c55b | 41373007029 success |
| Cũ 1 | d4991065b1707880ccae73b7d4290ba0a0f66e00 | 41373039944 cancelled, 0 job |
| Cũ 2 | 97cae433907953fb5407099f1e01b939c990bad5 | 41373042835 cancelled, 0 job |
| Cũ 3 | 4ae5bf680aaa49af977991da1dbb0fa4511154c8 | 41373045561; prompt không chốt kết quả |
| Mới mồi | aa67ee0083fee9015b419a17023abeab8abb0d3a | Run ID/kết quả chưa đọc được |
| Mới 1 | 790f794946faefa988195e6e4cd178260cca2a58 | Run ID/kết quả chưa đọc được |
| Mới 2 | 8d6adf69c158440f6cdc3a471fd4af47d8fba93e | Run ID/kết quả chưa đọc được |
| Mới 3 | f6ee8bead7e13337b07992960456a5cdb3a9087b | Run ID/kết quả chưa đọc được |

VERDICT-luot1.md khai đã đọc 8 run và vế mới 4 success; tôi giữ đó là lời khai lịch sử, không khai tự đo lại. Chưa xác minh được timing push ≤15 giây, jobs/runner_id hoặc kết quả A5 qua dịch vụ. Không có phép đo cho thấy vế cũ không tái hiện; cũng không coi thiếu kết nối là A5 pass hoặc fail hành vi.

`gh api repos/ducthangho/tra-luat/actions/runs/41373039944 --jq '{id,head_sha,status,conclusion,event,head_branch,run_attempt}'`: rc 1, output:

```text
Get "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/41373039944": proxyconnect tcp: dial tcp 127.0.0.1:38717: socket: operation not permitted
```

Thử đọc public bằng web tool cho API trên và PR #1141 cũng không lấy được nội dung (not accessible / cache miss). Không đổi proxy, không xin quyền vượt sandbox, không tạo workflow/run hay gửi thông điệp GitHub.

## Lệnh và giới hạn phép đo

lenh_da_chay:
- `git -C kho rev-parse HEAD`: rc 0, đúng SHA chỉ định, đo đầu và cuối.
- `git -C kho rev-parse HEAD^{tree}`: rc 0, dce456c90ddffaef089140293e77de2cbb502c48.
- `git -C kho rev-parse --verify 9091cf52cf20ac197c1a356d6a33cac6bab0b318^{commit}`: rc 0.
- `sha256sum kho/ops/specs/CI-CONCURRENCY-MASTER-r1.md`: rc 0, đúng hash, đo đầu và cuối.
- `git -C kho status --porcelain=v1`: rc 0, rỗng; snapshot chi tiết chạy với GIT_OPTIONAL_LOCKS=0.
- `git -C kho diff <base> <head>` và `git -C kho show aad4865 --`: rc 0; đã đối chiếu lại toàn diff, không chỉ delta sửa F1.
- `git -C kho diff --numstat <base> <head>`: rc 0, ci +6/-2; launcher +2/-1; test +28/-1; spec +95/0.
- `GIT_OPTIONAL_LOCKS=0 git -C kho diff --check <base> <head>`: rc 0, rỗng.
- Hai lệnh --mot-ca nêu trên: từng lệnh rc 0; log gốc trong targets.json.
- `python -B out/review_checks.py before targets setup experiments`: rc 0. Clone bằng git clone --no-hardlinks --no-checkout rồi checkout detached base/head ngoài kho; core.abbrev=7, autocrlf=false, eol=lf. Mutation chạy trên bản sao tạm.
- `python -B out/review_checks.py gates`: rc 0; mỗi lệnh sau chạy trên base VÀ head, từng lệnh rc 0: `actionlint .github/workflows/ci.yml .github/workflows/launcher-windows.yml`; `python .claude/dev/packet_loop.py doctrine-scan --root .`; `python .claude/dev/packet_loop.py adr-song --root .`; `python scripts/tl.py doc-claims-check --strict --json`. Log đầy đủ trong gates.json.
- `actionlint --version`: rc 0, 1.7.7; `python --version`: rc 0, 3.13.18; probe shellcheck không tìm thấy executable.
- `python -B out/review_checks.py semantics`: rc 0, 44 context mô hình qua.
- `rg -n -F 'phải chạy trọn' .github/workflows/ci.yml` (cwd kho): rc 1, rỗng — bằng chứng âm mong muốn.
- Đọc YAML 8 workflow và kiểm chú thích bằng Python: rc 0; workflows.json, comments.json.
- Tám cặp `git rev-parse --verify <sha>^{commit}` / `git show <sha>:.github/workflows/thu-concurrency.yml`: từng lệnh rc 0, xem A5.
- `gh api .../actions/runs/41373039944 ...`: rc 1, sandbox không cho socket; xem nguyên văn ở trên.
- `python -B out/review_checks.py after` và `cmp out/before.json out/after.json`: rc 0. Hai snapshot trùng byte.

khong_do_duoc:
- Full suite A1 và full mutant audit A9 không chạy trong lượt này; không có CA:/DOT BIEN:/TONG: của full suite để báo. Không tuyên bố tổng suite xanh.
- Kết quả remote A5/A9/A10, labels jobs, connector exact-head, kiem-merge và live lease projection hiện thời chưa xác minh độc lập do kết nối không khả dụng. Bản ghi cũ không thay readback của head cuối.
- A11 sau land; số slot runner, chi phí thực và thời gian tranh runner chưa đo.
- Windows không chạy: ghi nhận not_required do chủ kho quyết ở spec, không phải reviewer tự hạ mức M3.
- Shellcheck vắng; actionlint không chứng minh shell lint.
- Model/effort/session served và receipt assurance chưa có runtime attestation độc lập trong ngữ cảnh này. Provider/surface/transport khai theo công cụ thực tế, không suy từ tài khoản đăng GitHub.

Sandbox thực tế là workspace-write; read-only với `kho` là giới hạn tác vụ, không phải tuyên bố sandbox toàn bộ read-only. Không commit/push/sửa workflow hoặc mã trong kho. Cache Python tắt; đầu ra đặt ở out và clone/đột biến trong /tmp. Snapshot trước/sau gồm HEAD/tree, diff/index (kể hash index), tracked và mọi tệp untracked/ignored, hash nội dung: cùng 10.815 tệp và status rỗng. Hai snapshot trùng byte chỉ chứng minh không có delta quan sát ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Phạm vi snapshot là checkout `kho` được giao, không phải canonical ngoài môi trường.

verdict: approve
