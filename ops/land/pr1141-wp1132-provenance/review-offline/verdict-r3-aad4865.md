verdict: approve
reviewed_sha: aad4865c734e7c146463b13ed1750a47e6a9cb8f
reviewed_tree: dce456c90ddffaef089140293e77de2cbb502c48
base_sha: 9091cf52cf20ac197c1a356d6a33cac6bab0b318
spec_sha256: 72b63a79e0b63193904aaa5378ffd266bce1eb0322cf8c4e425c5b7d9a58f7f8
windows: not_required (ghi nhận quyết định chủ kho tại đặc tả; không chạy Windows)
review_class: sensitive
provider: openai_codex
execution_surface: codex_service
transport: machine
model: GPT-6 theo mô tả phiên; model/effort thực phục vụ không có attestation độc lập
findings: []
lop_da_quet: [master-ref-pending-replacement, concurrency-contract-lock, concurrency-comment-permanent-gap]

Approve về nội dung trên exact SHA nêu trên: không phát hiện finding P0–P3 mở sau khi tự đọc toàn diff base..head và đối chiếu Spec cùng Standards/Security. Áp M1–M3 của ADR-0060 và protocol §8/§13; không có P3 cần miễn. Không kế thừa kết luận lượt 2. Đây là verdict review offline; receipt/assurance và quyền merge vẫn phải được bên nhận xác minh.

CHƯA ĐỦ ĐIỀU KIỆN MERGE trong phạm vi evidence đã xác minh: chưa readback A9 (full_mutant_audit trên head cuối và kiem-merge rc 0), A10 (CI PR, labels từng job), connector đúng Reviewed commit; kết quả dịch vụ của A5 chưa tự xác minh. A11 là hậu kiểm sau land. Không biến các mục chưa đo thành passed.

## Đối chiếu lượt trước

Lượt 2 cùng head có 0 finding; không có finding liền trước cần phân loại. Đã tự kiểm thêm F1 P3 lịch sử ở lượt 1, lớp `concurrency-comment-permanent-gap`: **ĐÃ VÁ THẬT** tại `.github/workflows/ci.yml:54–58`. Câu hiện tại nói mất lượt gate **tự động**, đồng thời ghi nhận chạy lại hoặc dispatch đúng SHA; không còn khẳng định vĩnh viễn “không bao giờ được gate”. Chú thích launcher ở dòng 39 cũng không có khẳng định đó. Đối chiếu bằng đọc nguyên văn và [comments.json](comments.json), không lấy tổng suite thay kiểm nghĩa. Lớp lịch sử: 1 lớp/1 biểu hiện đóng, 0 lớp/0 biểu hiện mở; không thấy biểu hiện mới do bản vá.

## Đối chiếu §2 và ngữ nghĩa sự kiện

§2.1: `.github/workflows/ci.yml:59` và `.github/workflows/launcher-windows.yml:40` khớp nguyên chuỗi group đóng băng; cancel ở dòng 60/41 giữ nguyên. Chú thích ci dòng 54–58 giải thích một pending mỗi group, vì sao chỉ giữ running là chưa đủ, có #1132. Chú thích cả hai không chứa ký hiệu mở biểu thức Actions; chúng ở cấp workflow, ngoài thân run. Không còn “phải chạy trọn” trong khối concurrency. Nội dung mới không hứa success, FIFO hay mọi dispatch đều chạy.

§2.2: `ops/ci_duong_nhanh_test.py:2705–2710` định nghĩa GROUP_CU/GROUP_MOI/HUY_CHUAN và cập nhật KHUNG_TOP. Ca mới dòng 2918–2927 đọc YAML cả hai workflow, so nguyên chuỗi group và cancel, không so chuỗi con. LW/_lw tại dòng 3571/3591 hỗ trợ workflow thứ hai. Hai mutation tại dòng 3754–3757 có đúng ca đích; mutation cũ dòng 3753 còn hoạt động. Loader nghiêm và runner phân biệt assertion rc 3 với lỗi vô can rc 4, không có nhánh skip trong hai ca.

Đặt W = tên workflow, N = số PR, S = github.sha, R = github.ref. Toán tử &&/|| short-circuit và trả **toán hạng**: khi ref là master, vế && trả chuỗi SHA truthy, không trả boolean true.

| Sự kiện được khai | Group cũ → mới | cancel | Kết quả |
|---|---|---|---|
| pull_request opened/synchronize/reopened, cả hai workflow | W-N → W-N | true | Giữ hành vi PR. |
| pull_request labeled, chỉ launcher | W-N → W-N | true | Giữ hành vi; labeled là activity của pull_request. |
| PR thiếu số, ref vẫn refs/pull/N/merge | W-R → W-R | true | Fallback không đổi. |
| push master tại S | W-refs/heads/master → W-S | false | Hai commit khác SHA tách group. |
| workflow_dispatch master tại S | W-refs/heads/master → W-S | false | Tách theo commit, như đặc tả. |
| workflow_dispatch nhánh khác master hoặc tag | W-R → W-R | true | Giữ hành vi cũ. |
| push nhánh khác master hoặc tag | Không tạo run | — | Cả hai workflow chỉ nhận push master. |

Không tìm thấy hai SHA khác nhau trên refs/heads/master cùng group, hoặc ca PR đổi hành vi trong các sự kiện khai báo. PR closed/merged không được khai nên không dùng context của sự kiện ấy làm phản ví dụ. Hai workflow có tên khác nhau nên không va group giữa chúng.

Hai lượt cùng SHA master, kể cả push + dispatch hoặc dispatch khác input, vẫn cùng W-S; pending thứ ba có thể thay pending thứ hai, đúng ngoại lệ §2.1. Launcher chỉ nhận push khi paths khớp và PR khi paths/nhãn phù hợp; diff không đổi các bộ lọc này. Đổi group cho phép các commit master tranh slot runner, không bảo đảm thời gian chờ hay kết quả job.

[semantics.json](semantics.json) ghi 44 context tự đối chiếu (hai SHA, từng activity PR, có/thiếu số PR, dispatch branch/tag), rc 0. Đây là mô hình scalar toán hạng để kiểm lập luận, **không phải** thực thi biểu thức trên máy chủ GitHub. actionlint bên dưới kiểm cú pháp/context biểu thức thật trong hai tệp.

## Đo răng và đột biến SỐNG

Chạy từ chính kho được giao, tắt bytecode:

- `PYTHONDONTWRITEBYTECODE=1 python ops/ci_duong_nhanh_test.py --mot-ca y13b_concurrency_master_theo_sha`: rc 0, stdout/stderr rỗng.
- `PYTHONDONTWRITEBYTECODE=1 python ops/ci_duong_nhanh_test.py --mot-ca y13_khoa_topology_cua_ci_yml_ngoai_than_run`: rc 0, stdout/stderr rỗng.

Ba mutation đăng ký được gọi qua chính `chay_mot_dot_bien`: baseline ca đích xanh, đột biến chết do assertion đúng ca. Kết quả [registered-mutants.json](registered-mutants.json):

| Mutation | Ca đích | Kết quả |
|---|---|---|
| yml_concurrency_luon_huy | y13 | GIET |
| yml_concurrency_group_ve_ref | y13 và y13b | GIET bởi cả hai |
| launcher_concurrency_group_ve_ref | y13b | GIET |

Thử độc lập từng workflow trên clone tạm; mỗi lần phục hồi trước mutation tiếp theo. GIET dưới đây là rc 3 với tiền tố `DO:<đúng tên ca>:`; SỐNG là rc 0, không phải traceback hay setup lỗi.

| Biến thể | ci: y13b / y13 | launcher: y13b / y13 |
|---|---|---|
| Group về bản cũ | GIET / GIET | GIET / **SỐNG** |
| cancel-in-progress: true | GIET / GIET | GIET / **SỐNG** |
| cancel-in-progress: false | GIET / GIET | GIET / **SỐNG** |
| Group tương đương khác byte: đảo hai toán hạng so sánh ref với chuỗi master | GIET / GIET | GIET / **SỐNG** |
| Thay riêng toàn bộ workflow bằng nội dung tại base | GIET / GIET | GIET / **SỐNG** |

Có **năm biến thể launcher sống trước y13 đơn lẻ** vì y13 chỉ khóa ci.yml. Không biến thể nào sống qua cả hai ca; y13b bù đúng phạm vi thiếu. Tổng 10 biến thể/20 phép gọi ca bổ sung, không gọi đây là full mutant audit. Log lệnh, rc và output: [mutants.json](mutants.json); script tái lập: [review_checks.py](review_checks.py), lệnh `python -B out/review_checks.py setup experiments` từ thư mục rv3.

A2 được tái lập bằng giữ test head và lần lượt thay mỗi workflow bằng `git show 9091cf52cf20ac197c1a356d6a33cac6bab0b318:.github/workflows/<tệp>` trong clone tạm. Cùng lệnh y13b, từng tệp độc lập trả rc 3:

```text
DO:y13b_concurrency_master_theo_sha:ci.yml: concurrency.group = '${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', phai = "${{ github.workflow }}-${{ github.event.pull_request.number || (github.ref == 'refs/heads/master' && github.sha) || github.ref }}"
DO:y13b_concurrency_master_theo_sha:launcher-windows.yml: concurrency.group = '${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', phai = "${{ github.workflow }}-${{ github.event.pull_request.number || (github.ref == 'refs/heads/master' && github.sha) || github.ref }}"
```

## M2 — quét theo lớp

Lớp nguyên nhân `master-ref-pending-replacement`: nhiều commit dùng một group cố định/theo ref, khiến pending cũ bị thay dù cancel-in-progress=false. Đã đọc YAML đủ **8 workflow**, cả concurrency cấp workflow và cấp job, đối chiếu trigger thật; [workflows.json](workflows.json).

| Workflow / dòng | Cùng cơ chế còn ngoài bản vá | Có thực sự gác master? |
|---|---|---|
| ci.yml:52; launcher-windows.yml:38 | Hai nơi mục tiêu đã dùng SHA | Có push master; launcher có paths filter, không chạy mọi commit. |
| ops-publish-lease.yml:52 | Group theo ref, cancel=false | Chỉ push ops/** và paths lease; đăng lease, không gác commit push master. |
| ops-open-pr.yml:23 | Group theo ref, cancel=true | Chỉ push claude/**, ops/**; mở PR, không nhận push master. |
| ops-don-ref.yml:65 | Group toàn cục ops-don-ref, cancel=false | Chỉ dispatch thao tác ref; không phải cổng kiểm code master. |
| ops-thu-hoi-admission.yml:41 | Group theo số PR, cancel=false | **Có gác tiếp nhận PR đích master**, qua pull_request_target; không gác từng commit sau push/land master. Group mỗi PR có chủ đích, không gộp các commit master sau merge. |
| ci-dot-bien-du.yml; ops-do-workflow-definition.yml | Không có concurrency | Không còn khối cùng lớp để vá. |

Không có concurrency cấp job trong cả tám tệp. Bốn khối ngoài bản vá vẫn có thể thay pending trong chính group của chúng; không phát hiện chỗ ngoài packet còn gộp các SHA khác nhau của push master vào một group gác phát hành. Lớp `concurrency-contract-lock`: cả hai mục tiêu đã khóa đủ bằng y13b và mutation. Lớp `concurrency-comment-permanent-gap`: đã kiểm cả hai chú thích như phần đối chiếu lịch sử.

## Đối chiếu A1–A11

| Mục | Kết quả tự đo và giới hạn |
|---|---|
| A1 | **Không chạy full suite** `python ops/ci_duong_nhanh_test.py` không đối số. Không có dòng CA:/DOT BIEN:/TONG: của lượt full để trích. Executor khai CA: 114/114, DOT BIEN: 421/421, TONG: DAT trong prompt; giữ là lời khai. Registry tự import base/head cho 113→114 ca, 419→421 mutation ([counts.json](counts.json)); số đếm không thay thực thi. |
| A2 | Workflow base của từng tệp làm y13b đỏ đúng assertion, rc 3 như trên. Không xác nhận trình tự executor đã đo trước khi sửa. |
| A3 | Hai mutation mới và mutation cũ đều GIET đúng ca đích qua harness thật; phép độc lập cũng bắt được. |
| A4 | actionlint **1.7.7** trên đúng hai workflow: base/head rc 0, output rỗng, delta 0. **shellcheck vắng**; không tuyên bố lint shell. |
| A5 | Đọc được cấu hình thử tại cả tám Git object, khớp hai vế; run/job, runner_id và timing push chưa readback độc lập. Chi tiết dưới. |
| A6 | Đúng bốn tệp write set, +131/-4: ci +6/-2; launcher +2/-1; test +28/-1; spec +95/0. Dưới trần 450 dòng thêm và 6 tệp; hash spec khớp. |
| A7 | Chú thích concurrency không còn “phải chạy trọn”; có “một lượt pending”, #1132; không có ký hiệu mở biểu thức Actions. Đã đọc nghĩa câu, không chỉ kiểm chuỗi. |
| A8 | doctrine-scan, adr-song, doc-claims-check strict đều rc 0 ở base và head; output từng cặp trùng byte. doctrine-scan 10 tệp/0 chỗ chép; adr-song 59 ADR/59 dòng; doc-claims-check ok=true, flags=[], 381 advisory nền, layers_skipped={}. |
| A9 | **khong_do_duoc** full_mutant_audit remote success trên head cuối và kiem-merge rc 0. Không dùng full suite cục bộ hoặc lời khai thay run bắt buộc. |
| A10 | **khong_do_duoc** CI PR, labels từng job và connector exact-head trong review offline. |
| A11 | **Chưa đo; chỉ sau land.** Executor/phiên land kiểm hai push master đầu có job thật/runner_id khác 0, không canceled vì concurrency; nếu sai mở lại #1132. |

## A5 — Git objects và lời khai runtime

Tự chạy `git rev-parse --verify <sha>^{commit}` và `git show <sha>:.github/workflows/thu-concurrency.yml` cho tám commit, tất cả rc 0; [a5-local-objects.json](a5-local-objects.json). Workflow chỉ nhận push đúng nhánh ops/thu-concurrency-1132, một job sleep 120, cancel expression dùng đúng ref nhánh thử. Bốn tệp vế cũ có hash SHA256 `a4a43c548876cc143aee7ae2f4608ba6256becb8ed0e260f917aaf19ffa8c879`; bốn tệp vế mới có hash `2b7ff43f82492ff9d5d520c239dd0e86f426b7d288d96a2d66248a82b002b3c5`. Vế mới đổi master thành ref thử đúng yêu cầu.

| Vế | SHA đầy đủ tự xác minh | Run/kết quả executor cung cấp; chưa readback |
|---|---|---|
| Cũ mồi | fce9580b04caccadd8ea3bd6a51e79785451c55b | 41373007029 success |
| Cũ 1 | d4991065b1707880ccae73b7d4290ba0a0f66e00 | 41373039944 cancelled, 0 job |
| Cũ 2 | 97cae433907953fb5407099f1e01b939c990bad5 | 41373042835 cancelled, 0 job |
| Cũ 3 | 4ae5bf680aaa49af977991da1dbb0fa4511154c8 | 41373045561; chưa có kết quả trong prompt |
| Mới mồi | aa67ee0083fee9015b419a17023abeab8abb0d3a | Chưa có run ID/kết quả trong prompt |
| Mới 1 | 790f794946faefa988195e6e4cd178260cca2a58 | Chưa có run ID/kết quả trong prompt |
| Mới 2 | 8d6adf69c158440f6cdc3a471fd4af47d8fba93e | Chưa có run ID/kết quả trong prompt |
| Mới 3 | f6ee8bead7e13337b07992960456a5cdb3a9087b | Chưa có run ID/kết quả trong prompt |

Không suy kết quả chạy từ sự tồn tại commit. Không có phép đo cho thấy vế cũ không tái hiện; cũng không ghi A5 passed khi thiếu readback dịch vụ. Không gọi mạng hay tạo run trong lượt offline này.

## Lệnh đã chạy và phạm vi bảo toàn

lenh_da_chay:

- `git -C kho rev-parse HEAD`: rc 0, khớp SHA chỉ định, đầu/cuối; `git -C kho rev-parse HEAD^{tree}`: rc 0, tree nêu trên; `git cat-file -t <base>`: rc 0, commit.
- `sha256sum kho/ops/specs/CI-CONCURRENCY-MASTER-r1.md`: rc 0, khớp hash đóng băng, đầu/cuối.
- `git -C kho status --short` và snapshot `status --porcelain=v1 --untracked-files=all --ignored`: rc 0, rỗng.
- `git -C kho diff <base> <head>`; `git diff --numstat <base> <head>`: rc 0, toàn bộ bốn tệp đã đối chiếu; `GIT_OPTIONAL_LOCKS=0 git -C kho diff --check <base> <head>`: rc 0, rỗng.
- Hai lệnh --mot-ca từ kho được giao: từng lệnh rc 0, như phần đo răng.
- `python -B out/review_checks.py before setup experiments`: rc 0; clone --shared --no-checkout từ kho local sang /tmp, checkout detached base/head, ghim core.abbrev=7, core.autocrlf=false, core.eol=lf. Ba registered mutation GIET; 20 phép --mot-ca trên clone: 15 rc 3 đúng assertion và 5 rc 0 như bảng; hai phép đếm registry rc 0. [commands-before-setup-experiments.json](commands-before-setup-experiments.json), [setup.json](setup.json).
- `python -B out/review_checks.py gates`: rc 0; từng lệnh trên **cả base và head** đều rc 0: `actionlint .github/workflows/ci.yml .github/workflows/launcher-windows.yml`; `python -B .claude/dev/packet_loop.py doctrine-scan --root .`; `python -B .claude/dev/packet_loop.py adr-song --root .`; `python -B scripts/tl.py doc-claims-check --strict --json`. [gates.json](gates.json).
- `actionlint -version`: rc 0, 1.7.7; probe `command -v shellcheck`: rc 1, vắng; probe Python shutil.which cũng trả None.
- `python -B out/review_inventory.py`: rc 0; tám workflow, chú thích, 44 context scalar và 16 lệnh Git kiểm A5 đều đạt phạm vi đã nêu. [review_inventory.py](review_inventory.py).
- `python -B out/review_checks.py after`: rc 0; `cmp out/before.json out/after.json`: rc 0. [before.json](before.json), [after.json](after.json) trùng byte.

khong_do_duoc:

- Full suite A1 **not_run**, full mutant audit A9 remote **not_measured**; không có CA:/DOT BIEN:/TONG: do reviewer full-run sinh ra.
- Kết quả runtime A5, timing push ≤15 giây, jobs/runner_id; CI PR/labels/connector A10; full_mutant_audit và kiem-merge A9: chưa xác minh độc lập offline.
- A11 sau land; giới hạn slot runner, thời gian chờ, chi phí thật chưa đo.
- Windows **not_run** theo not_required do chủ kho quyết, không phải reviewer tự miễn M3.
- Shellcheck vắng; bare Ruff không chạy vì ngoài phạm vi thay đổi. actionlint không thay shellcheck.
- Model/effort thực phục vụ, session attestation, launcher receipt/terminal state và assurance cuối chưa có nguồn runtime độc lập trong ngữ cảnh này; không suy từ tài khoản GitHub.

Kho được đối xử chỉ đọc: không commit, push, sửa code/workflow hay cấu hình Git nguồn. Bytecode tắt, cache/output ngoài kho, chỉ đột biến clone /tmp. Snapshot gồm HEAD/tree, diff/index, hash index và nội dung **10.815 tệp** tracked/untracked/ignored; trước/sau trùng byte. Snapshot đo trước các thí nghiệm trên clone và sau kiểm tra; trước đó chỉ có đọc và hai ca target, vốn không ghi bytecode. Nó chứng minh không có delta quan sát giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox thực tế là workspace-write; giới hạn chỉ đọc kho là chỉ thị tác vụ, không phải filesystem mount read-only. Phạm vi bảo toàn là checkout được giao, không bao gồm canonical ngoài môi trường.
