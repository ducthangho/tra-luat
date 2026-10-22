verdict: changes_requested
reviewed_head: 521efebab226fe3a92b2ccce4a59c27dd638edff
reviewed_sha: 521efebab226fe3a92b2ccce4a59c27dd638edff
reviewed_tree: 9fc05c9986f711d1961e040dc7345850d0133294
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_run: 0265f9641e964cbe82b29d14a9813fc7
review_round: 5/5

## Kết luận

**F858-07 ĐÓNG — ĐÃ VÁ THẬT.** Head chạy đúng khi `GITHUB_PATH` rỗng hoặc vắng; mutant bỏ `:-` bị chính ca Linux giết bằng `TinHieuChotCa` tại chiều biến vắng, đồng thời bị ca macOS, Windows mô phỏng và shape giết. **F858-01/02/04/05/06 không hồi quy trong phạm vi finding gốc.** Diff đúng **6 tệp, 450 dòng thêm, 30 xoá**, không vượt trần/write set.

**F858-03/writer muộn: mở có quyết định chủ kho**, nợ `cai-stdout-writer-muon`. Các đường đã vá — dòng trống, log đường dẫn đồng bộ, trùng tên canh, không LF — đều qua phép kiểm độc lập. Writer muộn vẫn gây **rc=2/rg=DO, bash=DAT, 3/3 lần**; hai đối chứng mỗi loại **3/3 rc=0/DAT**. Giữ nguyên ID/lớp và quyết định chọn A; finding này **không phải lý do chặn** lượt này.

**Có F858-08 mới, P2 về độ phủ vòng duyệt ứng viên**, khác lớp stdout: hai mutant không tương đương vẫn sống qua 7/7 ca `r858_*` liên quan và toàn launcher suite không thêm lỗi. Phản chứng Windows chỉ có ứng viên thứ ba chạy được phân biệt **head rc=0/DAT** với mutant chỉ duyệt hai ứng viên đầu **rc=1**. Đây là thiếu chốt test, **không phải lỗi runtime trên head nguyên vẹn**. Không có quyết định chủ kho chấp nhận F858-08 trong nguồn được giao; theo chỉ thị lượt 5 và M-1, **changes_requested**. Không phát hiện P0/P1 trong phạm vi đã đo.

## Neo, authority và môi trường

Merge-base thực tế với `origin/master`: **637f78029f5a5fe56d35199dd0f75c50274f2c0f**. Spec đọc offline từ `origin/ops/wp858-spec:ops/specs/wp858.md`, SHA-256 **5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54**, đúng assignment. Lease g2 đọc từ ref được cấp, hạn **2026-10-24T04:32:00Z**, không nâng trần. Cả bốn verdict cũ đọc bằng `git show` **rc=0**; lượt 4 bằng byte với `../VERDICT-luot4.md`. [Neo](evidence/before-ids.stdout), [spec](evidence/spec.stdout), [lease](evidence/lease.stdout), [audit](evidence/scope-audit.json).

Áp dụng authority được **prompt snapshot chép lại**, không tự chứng thực GitHub live:

- [Python phương án (a)](https://github.com/ducthangho/tra-luat/issues/858#issuecomment-6312034981): giữ phạm vi rc=0, không in/ghi thư mục bản hỏng; nợ `python-probe-khong-theo-PATH`.
- [Lease g2, không nâng trần](https://github.com/ducthangho/tra-luat/issues/858#issuecomment-6332689060): tối đa 450 dòng thêm.
- [Chọn A cho F858-03](https://github.com/ducthangho/tra-luat/issues/858#issuecomment-6333879879): writer muộn được mở có quyết định; gốc stdout chung và `rg-installer-stdout-khong-LF` chuyển packet riêng. Không áp quyết định này sang F858-08.

Reviewer độc lập dùng shell/tools; [header đúng run](evidence/model-header.txt) công bố Codex **0.163.0**, model/effort như header verdict; [run identity chọn trường](evidence/run-identity.json) neo đúng prompt/head. Header chỉ chứng minh cấu hình CLI công bố, không chứng minh model phục vụ từng request. Không lấy actor GitHub làm danh tính model.

Linux x86_64, Python **3.13.16**, PyYAML **6.0.3**, jsonschema **4.26.0**, Ruff **0.17.1**. Sandbox thật `workspace-write`; `kho/` được đối xử chỉ đọc. Hai clone không hardlink dựng trong **một lệnh** `python -B out/review.py setup`, cùng origin và local `core.abbrev=7`. Mọi phép thử/đột biến ở `out/`; `TMPDIR=out/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`; không dùng auth thật trong suite. Selftest có command-env `commit.gpgsign=false`, không đổi cấu hình nguồn/toàn cục. [Runtime](evidence/runtime.json), [dependency probe](evidence/dependency-probe.stdout), [driver](review.py).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn liền trước: **93fd69fb958527ba738f882391956311972de60b**. Kết quả sau đây do reviewer tự chạy trên head hiện tại.

| Finding | Trạng thái/phân loại | Lệnh → kết quả thật |
|---|---|---|
| **F858-01** — nuốt lỗi ghi PATH/`-w` | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `python -B out/probes.py direct`: git/shellcheck/bash × ba nền mô phỏng chọn đúng ứng viên; đích GITHUB_PATH là thư mục ⇒ **rc=1**; Windows `-w` lỗi ⇒ **rc=1**, không ghi PATH. `probes.py mutations`: mutant nuốt lỗi ghi và `-w` bị đúng ca hành vi giết bằng **TinHieuChotCa**. |
| **F858-02** — fixture Windows không phân biệt đổi đường | **ĐÓNG phạm vi gốc — ĐÃ VÁ THẬT; không hồi quy** | `probes.py mutations`: bỏ `cygpath -u` bị ca Windows và shape giết; fixture giữ ánh xạ `V:` khác đường Unix. `direct`: đường GITHUB_PATH qua `W:` đúng. Không suy thành đã đo native Windows/PATHEXT. |
| **F858-03** — stdout installer thành kết quả chọn | **Đường đã vá vẫn ĐÓNG; lớp còn mở có quyết định chủ kho — CHƯA VÁ writer muộn** | `python -B out/probes.py stdout`: **8/8** tổ hợp (hai thứ tự rg/bash × dòng trống, log đường dẫn có LF, trùng tên canh, không LF) đều **rc=0, rg/bash DAT**. Mutant bỏ dòng canh/đổi về tên thư mục/bỏ LF bị N4 giết. Writer muộn **3/3 rc=2/rg=DO**; chuyển sang stderr hoặc ghi đồng bộ trước return ⇒ mỗi loại **3/3 rc=0/DAT**. Không gọi lớp này là đã vá thật toàn bộ. |
| **F858-04** — thiếu ca âm lỗi `-u` | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `direct`: `-u` vẫn in đường đúng nhưng thoát 37 ⇒ installer **rc=1**, PATH file rỗng, cả ba công cụ Windows. Mutant chỉ bỏ `return 1` bị ca Windows giết bằng **TinHieuChotCa**. |
| **F858-05** — vượt trần diff | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `git -C kho diff --numstat 637f780… HEAD` ⇒ **6 tệp, 450 thêm/30 xoá**; `diff --check` **rc=0**. `out/audit.py`: không mất hàm/ca/assert/mutant; đúng write set; Q3 giữ cả 12 tiền tố cài. |
| **F858-06** — đổi `-u` bị gắn với ghi PATH | **ĐÓNG phạm vi gốc — ĐÃ VÁ THẬT; không hồi quy** | `direct`: Windows git/shellcheck/bash đều **rc=0/DAT** với GITHUB_PATH rỗng và vắng. Mutant chỉ gọi `-u` khi ghi PATH bị ca Windows giết bằng **TinHieuChotCa**. |
| **F858-07** — fixture không đo biến GITHUB_PATH vắng | **ĐÓNG — ĐÃ VÁ THẬT** | `probes.py direct`: **18/18** tổ hợp ba công cụ × ba nền × rỗng/vắng đều **rc=0/DAT**, không ghi PATH. `probes.py mutations`: `wp858_sh_github_path_vang_khong_mac_dinh` chết ở **Linux/git: GITHUB_PATH=None, rc=1**, cùng lỗi đúng chiều trên macOS/Windows và lỗi shape; control **7/7 PASS**. `launcher_test.py --dot-bien` cũng ghi mutant này giết **2/2**, gồm ca Linux. |

Bằng chứng: [42 direct edges](evidence/direct-edges.json), [stdout và đối chứng](evidence/stdout-edges.json), [18 mutant đăng ký được chạy độc lập](evidence/independent-mutations.json), [diff lượt 4→5](evidence/since-round4.stdout), [audit cấu trúc](evidence/scope-audit.json).

## Finding mới

| ID / mức / lớp | Vị trí ở reviewed head | Bằng chứng | Hướng xử lý |
|---|---|---|---|
| **F858-08 — P2**; `fixture-khong-khoa-vong-duyet-ung-vien` | `.claude/dev/launcher_test.py:8474`, `:8550`, `:8667`; hợp đồng cần bảo vệ ở `ops/cai_cong_cu.sh:46`–`:51`, danh sách Windows trong `ops/cong_cu.yaml` | Mutant **first-two-only** chỉ duyệt hai phần tử đầu của danh sách; **no-break** bỏ dừng sau ứng viên đầu DAT. Cả hai **7/7 ca r858 liên quan PASS**, kể cả shape. Chạy toàn suite bằng cùng driver/cwd/env: control và hai mutant đều **221/234, 13 failed, 10 skipped, rc=1**, cùng tập lỗi/bỏ qua, **delta lỗi=0**. Fixture Windows git **và bash** chỉ có `Git/usr/bin` (ứng viên thứ ba) tốt: head **rc=0/DAT**, first-two-only **rc=1**. Hai thư mục ứng viên cùng tốt: head chọn thư mục đầu hợp lệ, no-break **rc=0 nhưng ghi thư mục tốt phía sau**, sai thứ tự chọn. | Bổ sung chiều chỉ ứng viên thứ ba DAT và chiều nhiều ứng viên cùng DAT; đòi đúng rc/trạng thái/thư mục, giữ control qua và giết mutant bằng **TinHieuChotCa**. Đăng ký mutant bảo vệ vòng duyệt, cân đối trong trần 450 và giữ các chốt cũ. Chỉ cần sửa test cho finding này; không có bằng chứng cần sửa runtime head nguyên vẹn. |

**Vì sao đây là mutant không tương đương:** Q2 giao cả danh sách ứng viên, gồm Windows `Git/{cmd,bin,usr/bin}`, và công thức giữ thứ tự nơi cài rồi fallback. Fixture hiện tại có một thư mục tốt: git ở `cmd`, bash ở `bin`; không đo chiều hai vị trí này đều hỏng mà `usr/bin` tốt. Shape buộc các đối số vẫn hiện diện trong YAML nhưng không chứng minh helper duyệt đến chúng. Do đó cắt vòng lặp sau hai phần tử vẫn qua mọi ca; phép riêng cho thấy nó từ chối một ứng viên được Q2 cho phép. Mutant bỏ `break` bổ sung bằng chứng thiếu chốt ưu tiên ứng viên đầu, vốn được comment sản phẩm mô tả rõ. Hai biểu hiện gom vào **một** finding/lớp độ phủ vòng duyệt.

Các phép này dùng installer im lặng, không LF bất thường, không writer nền; độc lập hoàn toàn với `stdout-installer-bi-nhan-lam-ket-qua-chon`. F858-02 vẫn đóng chốt chuyển đổi Windows; F858-08 bảo vệ việc duyệt danh sách sau chuyển đổi, không đổi tên để tái mở finding ấy.

| Fixture độc lập, Windows mô phỏng | Head/control | first-two-only | no-break |
|---|---|---|---|
| git: chỉ ứng viên thứ ba tốt | **rc=0/DAT**, ghi `W:<…>/Git/usr/bin` | **rc=1**, không ghi PATH | rc=0, đúng thư mục |
| bash: chỉ ứng viên thứ ba tốt | **rc=0/DAT**, ghi `W:<…>/Git/usr/bin` | **rc=1**, không ghi PATH | rc=0, đúng thư mục |
| git: cmd và usr/bin cùng tốt | **rc=0**, chọn cmd | rc=0, chọn cmd | **rc=0**, chọn usr/bin sai ưu tiên |
| bash: bin và usr/bin cùng tốt | **rc=0**, chọn bin | rc=0, chọn bin | **rc=0**, chọn usr/bin sai ưu tiên |

[Driver tái lập](explore.py), [mutant chỉ hai ứng viên](mutants/first-two-only.sh), [mutant bỏ break](mutants/no-break.sh), [7 ca mỗi biến thể](evidence/exploratory-targeted.json), [A/B mở rộng với stdout/stderr thật](evidence/candidate-witnesses-expanded.json), [delta toàn suite](evidence/suite-delta.json). Đây là các bản cố ý làm hỏng phục vụ phép đo, không phải patch khắc phục runtime sensitive; hướng khắc phục ở trên chỉ mô tả bằng lời.

## Bảng lớp và lịch sử

**8 lớp / 8 finding IDs; 2 lớp mở P2:** F858-03 có quyết định chủ kho; F858-08 chưa có. Tập mở cuối lượt 4 là F858-03/F858-07, lượt này xác minh vá thật một lớp ⇒ **1/2 = 50%**; chấp nhận nợ F858-03 không được tính là vá. F858-08 là lớp mới, không cộng vào tử số.

| Slug giữ ổn định | ID / nguồn | Trạng thái và phép kiểm |
|---|---|---|
| `loi-ghi-path-bi-nuot-trong-command-substitution` | F858-01, lượt 1 | Đóng phạm vi gốc; lỗi ghi/`-w` trả khác 0, mutant chết đúng ca hành vi. |
| `fixture-windows-khong-phan-biet-chuyen-doi-va-duoi-exe` | F858-02, lượt 1 | Đóng phạm vi gốc; ánh xạ V: phân biệt `-u`, không tái thêm bộ lọc `-f/-x/.exe`. Native còn chưa đo. |
| `stdout-installer-bi-nhan-lam-ket-qua-chon` | F858-03, lượt 1→5 | **Mở P2 có quyết định chủ kho**; đường đồng bộ/LF/collision đã vá; writer muộn chưa vá, giao packet riêng theo chọn A. |
| `cygpath-u-error-guard-khong-co-ca-am` | F858-04, lượt 2 | Đóng; ca `-u` stdout hợp lệ/rc37 giết mutant bỏ return. |
| `vuot-tran-diff-sensitive-chua-co-ngoai-le` | F858-05, lượt 2 | Đóng; đúng 450/6, không mất chốt cũ, không nâng trần. |
| `chuyen-doi-windows-gan-nham-voi-github-path` | F858-06, lượt 3 | Đóng phạm vi gốc; Windows DAT khi không ghi PATH, mutant chết bằng ca hành vi. |
| `fixture-luon-dat-github-path-bo-sot-unset` | F858-07, lượt 4 | **Đóng**; thật sự bỏ biến, control DAT, mutant chết đúng chiều biến vắng. |
| `fixture-khong-khoa-vong-duyet-ung-vien` | F858-08, mới lượt 5 | **Mở P2**; cần phép chỉ ứng viên cuối tốt và nhiều ứng viên tốt, head qua/mutant bị đúng assertion giết. |

## Bảng lệnh → kết quả thật

Cwd mặc định là workspace; lệnh con chạy trong `out/head` hoặc `out/base` như metadata. Mỗi gate có `evidence/<tên>.json` ghi argv/cwd/rc/thời lượng và stdout/stderr riêng; [gate summary](evidence/gate-summary.json). Driver phản chứng trả 0 khi ghi nhận đúng cả ca dương lẫn ca âm; không dùng rc driver để đổi lỗi con thành pass.

| Lệnh / cwd | Kết quả thật |
|---|---|
| `python -B out/review.py setup` | **rc=0**; dựng nền/head cùng lần; kiểm đúng SHA/spec/lease, bốn verdict cũ đọc **rc=0**. |
| `git -C kho diff --numstat <merge-base> HEAD`; `git -C kho diff --check <merge-base> HEAD` | **6 tệp/450 thêm/30 xoá**; check **rc=0**, không output. |
| `python -B out/audit.py` | **rc=0**; lượt 4→5: **461→461 hàm, 244→244 ca @ca, 819→819 bang, 85→85 assert**, không mất mutant; thêm đúng mutant F858-07. Shell/YAML/selftest bằng byte với lượt 4; YAML chỉ đổi các khối cai được giao so nền; rg nguyên vẹn, Q3 đủ 12/12. |
| `python -B out/review.py suites` → `python -B .claude/dev/launcher_test.py --nhat-ky <log>` × nền/head × có/không auth giả | Driver **rc=0**; bốn suite **rc=1**, số liệu bên dưới. Không tái xác nhận headline executor 242/242 trong sandbox này. |
| `python -B out/probes.py direct`; `mutations` | Cả hai **rc=0 driver**; **42** phép direct; control **7/7 PASS**, **18/18** mutant đăng ký bị giết ít nhất một chốt, không dùng lỗi setup làm kill. |
| `python -B out/probes.py stdout` | **rc=0 driver**; 8/8 đường đã vá rc=0/DAT; writer muộn 3/3 rc=2; hai đối chứng mỗi loại 3/3 rc=0. |
| `python -B out/explore.py targeted`; `witnesses` | Đều **rc=0 driver**; control và hai mutant đều **7/7 PASS**; 12 phép A/B git/bash xác nhận hai mutant không tương đương. |
| `python -B out/explore.py full` → `explore.py suite {control,first-two-only,no-break}` | Driver **rc=0**; cả ba suite **rc=1**, cùng **221/234, failed=13, skipped=10**, delta lỗi mutant/control=0; 7 ca r858 liên quan đều qua. |
| `python -B .claude/dev/launcher_test.py --dot-bien`, cwd `out/head` | **rc=0, 296/296 đạt, 4 không đo được** trên Linux. Không lấy dòng mutant gốc tạm “OK” làm chứng nhận N5 vì control của ca ấy đang lỗi môi trường. |
| Hai `python -B scripts/tl.py --selftest` song song, cwd `out/head`, command-env tắt ký Git | **Cả hai rc=0, 1731/1731**; `edit_skill_assert_count_gate_dry` **OK cả hai**. [Lượt 1](evidence/selftest-1.stdout), [lượt 2](evidence/selftest-2.stdout). |
| `python -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, cwd `out/head` | **rc=0, ok=true, expected=checked=190**, failed/extra/missing rỗng. |
| `CONG_CU_TEST_BAN_KINH=manh python -B ops/cong_cu_test.py`, cwd `out/head` | **rc=0, 61 ca, tiền kiểm bỏ qua=0, cổng cây thật ĐẠT**; **470 mutant giao job mảnh/gom**, không đo đủ bán kính trong lệnh này. |
| `python -B scripts/tl.py golden-test --json`; `doc-claims-check --strict --json`, cwd `out/head` | Đều **rc=0, ok=true**. |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .`, cwd `out/head` | **rc=0**, sạch. |
| `bash -n ops/cai_cong_cu.sh`; `actionlint`, cwd `out/head` | Đều **rc=0**, output rỗng. ShellCheck thật vắng trong PATH, không nhận kết quả actionlint này là đã đo lớp SC*. |
| `python -B -m ruff check --no-cache --select F scripts/tl.py scripts/tl_selftest.py .claude/dev/launcher_test.py`, nền/head | Cả hai **rc=1, 4409 finding**, **delta=0**; bare lint còn nợ nền. Ruff **0.17.1**. |
| `python -B -c '<runpy ci_dang_ky_test.py; loi_ruff_ci()>'`, cwd `out/head`; argv đầy đủ trong JSON | **rc=0, RUFF_CONTRACT 3 []**; pin/probe contract, tách khỏi bare lint ở hàng trên. |
| `python -B out/summarize.py` | **rc=0**; đối chiếu tên lỗi/bỏ qua và số liệu các suite trong [suite-delta](evidence/suite-delta.json). |
| `python -B out/review.py snapshot` | **rc=0**, HEAD/tree/status và hash **4904 tệp, gồm Git metadata**, bằng mốc đầu. [Integrity](evidence/integrity.json). |

| Cây / phép đo | Passed | Failed | Skipped | Tổng | rc |
|---|---:|---:|---:|---:|---:|
| Nền / không auth giả | 214 | 12 | 10 | 236 | 1 |
| Nền / auth giả | 214 | 12 | 10 | 236 | 1 |
| Head / không auth giả | 221 | 13 | 10 | 244 | 1 |
| Head / auth giả | 221 | 13 | 10 | 244 | 1 |
| Control cùng driver với mutant mới | 221 | 13 | 10 | 244 | 1 |
| first-two-only | 221 | 13 | 10 | 244 | 1 |
| no-break | 221 | 13 | 10 | 244 | 1 |

**Delta thô nền→head là +1 failed**, đúng `r858_goc_tam_tranh_to_tien_co_git` mới. Head: ca ấy và t86 đều **EROFS tại `/var/tmp`**; nền t86 không thể materialize home dưới tổ tiên `.git`. **11 lỗi r484** chung giữa nền/head, liên quan repository ancestor/credential guard. `/tmp/.git` và lớp mount `/dev/shm` là ro. Không sửa mount/quyền hoặc đổi lỗi thành skipped. **Delta=0 chỉ áp cho Ruff và cặp control/mutant**, không dùng cho tổng failed nền→head. [Tập lỗi](evidence/suite-delta.json), [mounts](evidence/mounts.log), [head stdout](evidence/launcher-head-none.stdout).

## Không đo được

- **Native Windows/macOS, Git Bash/MSYS, `.exe`/PATHEXT và installer thật**: các phép Windows/macOS ở đây mô phỏng trên Linux bằng stub vô hại. Chưa chứng nhận sàn đột biến native Windows hay N2 trên runner thật.
- **N5/t86 xanh end-to-end, hai launcher suite song song ×10**: không nghiệm thu được vì tổ tiên `/tmp/.git` ro và gốc thay thế `/var/tmp` không ghi được. Giữ failed thật, không tính lỗi môi trường là kill có giá trị của chốt chọn gốc tạm.
- **10 ca launcher skipped**: 8 cần venv/pip không dựng được offline, 2 đặc thù Windows; danh sách riêng trong suite-delta. Không trộn skipped vào passed.
- **GitHub/CI/heartbeat/lease live, check-run `ci.yml`, dispatch `launcher-windows.yml`, thread resolution**: không gọi mạng/GitHub theo assignment. Snapshot lease và authority chép lại không xác nhận các trạng thái live này. Chưa chứng nhận M-2/M-3 hoặc quyền merge/land/deploy.
- **470 mutant cong_cu_test**: chưa có kết quả job mảnh/gom; 61 ca và launcher 296/296 không thay phép đo ấy. **ShellCheck thật** vắng; actionlint rc0 không chứng minh lớp SC*.
- **Python**: chỉ nghiệm thu phạm vi (a) được chủ kho giao; ca hiện qua, nợ `python-probe-khong-theo-PATH` còn nguyên. **rg riêng** không đổi so nền theo audit; nợ `rg-installer-stdout-khong-LF` giữ theo quyết định chủ kho, không tuyên bố đã vá hay đã chạy lại phản chứng rg riêng của lượt 4.
- Runtime plugin không có tool `environment_status` trong danh sách tool khả dụng; môi trường được đo trực tiếp bằng shell/dependency probe/mountinfo. Không suy readiness mạng/credential từ đó.

Không có patch sản phẩm, commit, push hay liên lạc GitHub. Snapshot sạch chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Hai clone test cũng có status tracked/untracked sạch sau chạy. Các driver, verdict và evidence có băm ở [SHA256SUMS](SHA256SUMS); clone/fixture lớn không nằm trong danh mục ấy. Đây là lời gọi Codex cuối **5/5**, không tự mở thêm vòng review.
