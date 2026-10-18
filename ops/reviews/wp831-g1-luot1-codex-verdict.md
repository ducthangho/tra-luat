verdict: changes_requested
reviewed_sha: c3c790e0ae19fabb27e2ea9daa16591d03859ed3

Kết luận lượt 1: **2 lớp finding P2 mở** — F01 `chooser-checker-path-fallthrough` (Linux/macOS) và F02 `linux-candidate-set-drops-usrbin` (Linux/Q1). Không đủ ngưỡng approve của assignment (không P0/P1/P2 mở). Các ca stock qua và manifest đạt không đóng hai phản chứng dưới đây.

Reviewer OpenAI Codex; provider `openai_codex`, execution surface `codex_service` theo định nghĩa kho (API agent có shell, không tự nhận đang chạy qua Codex CLI), transport `machine`. Family OpenAI và vai reviewer từ assignment; executor Claude là thông tin được giao, không phải receipt reviewer tự xác minh. Model ID/effort/session ID/launcher receipt và assurance runtime độc lập: **KHÔNG ĐO ĐƯỢC**. Không tự cấp assurance, quyền merge/land hoặc trạng thái Packet.

Đã đọc toàn bộ prompt.snapshot và SPEC.md; AGENTS, CONTEXT, các phần Quy trình sửa code/Bài học đắt giá của CLAUDE.md, protocol §8/§13, adapter cross-review Codex, kế hoạch provider, wrapper/checker/YAML rg, các helper/ca/mutation/runner được yêu cầu. Mẫu wp802 chỉ dùng định dạng. Kiểm cả trục Spec và Standards/Security. Không gọi GitHub, không push/merge/land, không sửa `cay-kho/`; không tự soạn payload thoát cây. Các bản sao và thử nghiệm đều dưới `review-data/`.

## Neo và môi trường

| Phép đo | Kết quả |
|---|---|
| HEAD / tree | `c3c790e0ae19fabb27e2ea9daa16591d03859ed3` / `64b665d8f5a7ccbd2340db6eb90f1a6fcd7ac0a4` |
| Base refs/remotes/origin/master | `1e69d2a0d3c708efe0dec86752fc13a0fe039aab` |
| SPEC.md SHA-256 | `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888`, khớp assignment |
| Bundle diff/numstat | So byte với `git diff <base> <head>` và `git diff --numstat <base> <head>`: cả hai bằng nhau; preflight.json, git-diff.patch, git-numstat.txt |
| Phạm vi | 6 tệp, 165 dòng thêm / 10 dòng xóa; đúng 6 path write set, dưới trần 450 dòng thêm. Chỉ hai công thức rg Linux/macOS đổi trong YAML |
| Cách dựng | `PYTHONDONTWRITEBYTECODE=1 python review-data/bootstrap.py`: base/head clone `--no-hardlinks --no-checkout`, detached SHA, cùng một vòng lệnh; `core.abbrev=7`, `core.autocrlf=false`, origin đặt về URL thật, không fetch mạng |
| Runtime | Linux x86_64, Python 3.13.16, GNU Bash 5.2.21, mawk 1.3.4, Ruff 0.17.1, host `/usr/bin/rg` 14.1.0; environment.json |
| Cache/scratch | Python tắt bytecode; TMPDIR dưới review-data/tmp cho stock test/mutation; Ruff --no-cache; fixture tự dựng có path chứa dấu cách |

## Phán riêng Q1 và N4

**Q1 — KHÔNG CHẤP NHẬN NGUYÊN TRẠNG.** Đã đo phần lời khai có thể đo ở local: `/usr/bin/rg --version` rc 0, ripgrep 14.1.0. Trong YAML bản sao, chỉ thay ứng viên đầu thành `/usr/bin` như spec; giữ nguyên helper stock. Bốn thân rg ở thư mục fixture (phiên bản hợp lệ, exit 1, exit 0 rỗng, phiên bản rác) đều cho wrapper rc 0/DAT và GITHUB_PATH=/usr/bin. Ca r831 Linux ĐỎ bằng `TinHieuChotCa` vì GITHUB_PATH khác thư mục fixture. Xem q1.json, mutations.json mục q1_hard_usrbin.

Điều này chứng minh fixture hiện tại không dựng được tiền đề “không ứng viên nào chạy được” khi `/usr/bin/rg` thật vẫn tốt; không chứng minh mọi cách viết test cho chuỗi cứng đều bất khả thi. Phải phân biệt recipe không thể trả lỗi trong tiền đề ấy với assertion âm: assertion âm đòi rc khác 0 sẽ ĐỎ. Khả năng ghi `/usr/bin` của executor và trạng thái rg trên runner CI: **KHÔNG ĐO ĐƯỢC**; không thử ghi hệ thống ngoài write set, không gọi GitHub.

Việc đọc metadata có thể là một nguồn bổ sung, nhưng thay thế hẳn `/usr/bin` bằng dòng khớp CUỐI của dpkg làm mất ứng viên bắt buộc. F02 đo được head từ chối dù `/usr/bin/rg` tốt; biến thể đúng Q1 lại qua trên cùng layout. Lý do thuận tiện cho test không đủ để chấp nhận mất bảo đảm này. Không kết luận có đường thực thi mã ngoài những binary vốn được phép trong PATH; đây là lỗi chọn ứng viên và tính sẵn sàng.

**N4 — CHẤP NHẬN về đúng/an toàn.** Bảng tài liệu đúng với mã thật; danh sách “git, python, rg” trong spec không liệt kê hết tập bắt buộc của launcher. Đã gọi chính `_bat_buoc` trên từng phần tử CONG_CU với môi trường trống, remote, GITHUB_ACTIONS=true, CI=true và CI+remote; doc-matrix.json:

| Công cụ | User | Remote=true | CI=true hoặc GITHUB_ACTIONS=true |
|---|---|---|---|
| git, python, rg, bash | Bắt buộc | Bắt buộc | Bắt buộc |
| claude, codex | Bắt buộc | Bắt buộc | Tùy chọn |
| gh | Bắt buộc | Tùy chọn | Tùy chọn |
| npm, node, llm, agy, actionlint, shellcheck | Tùy chọn | Tùy chọn | Tùy chọn |

CI được ưu tiên khi đồng thời có dấu remote. `_bat_buoc` chỉ nhận các biến trên bằng chuỗi `true`; không suy diễn mọi giá trị truthy. Tài liệu `docs/GOI_AGENT_DA_NEN.md:32`, `:39`, `:43`, `:440` khớp `CONG_CU`, `_bat_buoc` và nhánh thieu_bat_buoc trong lenh_doctor: công cụ bắt buộc thiếu/hỏng, xác thực đo được sai, hoặc rg/git BI_CHE dẫn tới mã 12. `_AP_DUNG_BI_CHE` đúng là git và rg. Bốn ca doctor bổ sung (rg bị che, rg tốt, git bị che, bash ngoài phạm vi) đều 1/1 qua, 0 bỏ qua, rc 0. Không biến kết quả fixture thành lời khai đã chạy doctor với credential thật hoặc đã đo mạng.

## Ca bắt buộc và cổng

Các lệnh chạy trong review-data/head, với `PYTHONDONTWRITEBYTECODE=1`, TMPDIR trong review-data; rc và toàn bộ stdout/stderr nằm trong các log JSON tương ứng.

| Lệnh | Kết quả thật | Đánh giá |
|---|---|---|
| `python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | rc 0; 1/1 qua, 0 bỏ qua, 0 hỏng | N1/N3 stock qua |
| Tương tự `r831_cai_rg_macos_chon_ban_chay_duoc` | rc 0; 1/1, 0 bỏ qua | N2/N3 stock qua; công thức macOS chạy trên Bash/Linux |
| Tương tự `r802_cai_rg_windows_chon_ban_chay_duoc` | rc 0; 1/1, 0 bỏ qua | Không hồi quy fixture Windows chạy trên POSIX |
| Tương tự `r802_bang_cai_rg_khop_cong_cu_yaml` | rc 0; 1/1, 0 bỏ qua | Parity mà ca này thực đo là Linux/Windows; macOS kiểm độc lập bên dưới |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | Base rc 2, ok=false, 187/187, extra_files=[changelog.d/wp-802.md]; head rc 0, **ok=true, expected=189, checked=189**, failed=[], extra_files=[] | N5/L3 đạt trên bản sao exact head, gồm wp-831; không sinh lại manifest để làm xanh |
| `python scripts/tl.py doc-claims-check --strict` | Base/head rc 0, ok=true | Cổng N4 đạt; không thay phép đối chiếu ngữ nghĩa |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | Base/head rc 0, 10 tệp / 0 chỗ | Cổng N4 đạt |
| `python -m ruff check --no-cache --select F .claude/dev/launcher_test.py` | Base/head rc 1, cùng 5 F841 | Bare lint đỏ sẵn, delta 0; không gọi là lint sạch |
| `git diff --check <base> <head>` | rc 0, output rỗng | Không lỗi whitespace |
| Full launcher suite, có/không auth giả; --dot-bien toàn kho | **not_run**, assignment cho tùy chọn | Không xác nhận N/N toàn bộ hoặc delta full suite từ lời khai executor |
| Ruff pin/probe contract | **not_run** | Bare lint trên không thay phép kiểm contract |
| CI ci.yml / launcher-windows.yml exact head, native Windows/macOS BSD | **KHÔNG ĐO ĐƯỢC** | Không gọi GitHub; không nhận evidence native/CI chưa được cấp |

N3: phần trước ` && ` đầu tiên bằng BYTE của chuỗi đã parse YAML giữa base/head: Linux `sudo apt-get install -y ripgrep`; macOS `brew install ripgrep`. Windows cũng giữ nguyên. Đã kiểm riêng cả macOS vì r802 parity không đọc mục này. `cong_cu.py kiem-tra --chi rg` đúng là checker dùng chung trong cả hai vòng chọn. L2 về tập bắt buộc/mã 12/BI_CHE đúng như phần N4.

## Bảng săn hành vi — lệnh → kết quả thật → ý nghĩa

Lệnh chính từ gốc rv1: `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_behavior.py` (40 trial; behavior.json, behavior-summary.log). Mỗi trial lưu command wrapper/direct, cwd, PATH, stub và stdout/stderr thực; installer đều là stub, không cài thật. Các tên dưới đây là khóa `name` trong JSON. Các probe bổ sung có lệnh riêng.

| Hướng / lệnh hoặc trial | Kết quả thật | Ý nghĩa / giới hạn |
|---|---|---|
| linux/macos_direct_pfFalse/True × good/bad/empty | Mỗi nền: good rc 0/in đúng candidate; exit 1 và exit 0 rỗng đều rc 2, không GITHUB_PATH. Cả bật/tắt pipefail | Không thấy việc bỏ pipefail làm lọt hai chiều âm này |
| linux/macos_wrapper_spaces | rc 0/DAT, GITHUB_PATH đúng prefix có dấu cách | Đường repository, prefix và GITHUB_PATH có khoảng trắng đều đi qua wrapper thật |
| linux/macos_no_github | rc 0/DAT khi gỡ hẳn GITHUB_PATH | Không lỗi nounset từ biến vắng |
| linux/macos_stale_bad | Thừa kế RG_DICH trỏ thư mục tốt khác; cả hai candidate đang thử hỏng ⇒ rc 2, GITHUB_PATH rỗng | Head không lấy stale RG_DICH làm thành công |
| linux/macos_inherit_good / inherit_bad | Bash -O inherit_errexit: good rc 0/đúng candidate; bad rc 2 | Kiểm thêm ảnh hưởng `set -e` trong `$(eval ...)`; không chỉ đọc mã |
| linux/macos_install_fails | apt-get/brew stub exit 9 ⇒ wrapper rc 9, không GITHUB_PATH, không tiếp tục chọn | Chuỗi `&&` không nuốt lỗi installer, kể cả có RG_DICH tốt thừa kế |
| linux/macos_fallback | Candidate hỏng, rg đầu PATH tốt ⇒ rc 0, chọn front | Vòng for đi tiếp khi candidate đầu bị checker từ chối; không thoát sớm vì errexit |
| linux/macos_candidate_missing | Không file rg ở prefix, PATH đầu tốt ⇒ rc 0, chọn front | Fileguard hiện có chặn được thư mục thiếu file |
| linux/macos_candidate_nonexec; `python review-data/repro_f01.py` | File rg 0644 ở prefix, PATH đầu tốt ⇒ head rc 0/DAT nhưng chọn prefix; chính file đó rc 126/Permission denied. Bước shell tiếp theo chỉ nhận thư mục đã persist cũng rc 126 | **F01**: checker đã chạy rg khác; thêm -x trong biến thể thử ⇒ chọn front, probe trực tiếp/bước sau đều rc 0 |
| linux_dpkg_absent / fail_empty / empty_success | Cả ba rc 0, chọn /usr/bin, bản host thật được checker nhận | Nhánh fallback hoạt động trên host này. Không dùng host rg tốt để chứng minh âm “không có ứng viên” |
| linux_dpkg_fail_output | dpkg in đường tốt rồi exit 7 ⇒ wrapper rc 0, chọn đường được in | Exit pipeline bị bọc bởi dirname nên không quyết định kết quả chọn. “Không đọc được ⇒ /usr/bin” trong comment chỉ đúng khi không thu được dòng khớp, không phải mọi rc khác 0 |
| linux_dpkg_multi_bad_last / multi_good_last | Đường tốt rồi đường hỏng ⇒ rc 2; đảo thứ tự ⇒ rc 0/chọn tốt | awk giữ một dòng CUỐI; không thử tất cả thư mục dpkg khai |
| `python review-data/repro_f02.py` | dpkg rc 0 in /usr/bin/rg tốt rồi fixture/bin/rg hỏng: head rc 2; chỉ đổi ứng viên về /usr/bin như Q1 ⇒ rc 0/DAT, GITHUB_PATH=/usr/bin | **F02**, bằng chứng mất ứng viên thật. dpkg native hiện chỉ có một dòng /usr/bin/rg; nhiều dòng là fixture được giao săn |
| macos_brew_fail_empty | brew --prefix exit 7/rỗng ⇒ ứng viên thành /bin; host /bin/rg tốt nên rc 0, chọn /bin | Lỗi lấy prefix không tự fail-close; ở layout này vẫn chọn binary qua checker. Không suy rằng macOS thật luôn có /bin/rg |
| macos_brew_fail_output | brew in prefix tốt rồi exit 7 ⇒ rc 0, chọn prefix | Không lấy rc của command substitution làm bằng chứng prefix đáng tin; quyết định cuối vẫn qua checker |
| dirname/awk BSD native | **KHÔNG ĐO ĐƯỢC**; chỉ đo dirname GNU và mawk trên Linux | Biểu thức awk dùng tính năng POSIX qua đọc mã; điều đó không thay phép chạy BSD/macOS thật |
| `python review-data/probe_extra.py` — bỏ init hoặc guard, stale RG_DICH + candidate hỏng | 4 layout, đều rc 2, không GITHUB_PATH | Trong layout đã đo, for thất bại làm chuỗi && dừng trước guard/echo; survival init/guard chưa chứng minh lỗi stale ở head |
| Cùng script — gỡ fallback với prefix hỏng/PATH tốt | Cả hai mutant rc 2; control ở probe_behavior rc 0/chọn front | Survival của chốt fallback có ý nghĩa hành vi; head hiện vẫn xử lý đúng |
| Gỡ fileguard, prefix vắng/PATH tốt | Mutant rc 0 nhưng ghi prefix không có rg; control chọn front | Chốt có ý nghĩa nhưng stock không canh; head còn F01 do chỉ kiểm -f, chưa kiểm khả năng thực thi |
| Cùng script — công thức base trên layout nonexec/PATH tốt | Linux/macOS rc 0, stdout là front tốt | Hồi quy chọn nhầm thư mục của F01 được tạo ở head, không phải hành vi base trên layout đó |

Các thử nghiệm shell chọn binary/phiên bản trong PATH; không khẳng định đã chạy nội dung tra cứu thật của mọi binary rg hoặc thử mọi race/filesystem. Không có thử nghiệm thay đổi file trong lúc checker chạy.

## Bảng đột biến — giết đúng assertion và survival

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python review-data/audit_mutations.py`, `... python review-data/audit_more.py`. Mutation chỉ ghi YAML riêng dưới review-data/mutants rồi đổi con trỏ YAML_DANG_DUNG của module test; wrapper/checker thật được copy vào từng fixture. Đếm chỉ exception **TinHieuChotCa** có frame đúng ca đích; traceback và tên ca đầy đủ trong mutations.json / more-mutations.json. Ngoại lệ khác không được cấp kill.

Ký hiệu L = r831_cai_rg_linux_chon_ban_chay_duoc, M = r831_cai_rg_macos_chon_ban_chay_duoc, W = r802_cai_rg_windows_chon_ban_chay_duoc, P = r802_bang_cai_rg_khop_cong_cu_yaml.

| Chốt / mutant | Ca | Kết quả thật / phạm vi |
|---|---|---|
| wp831_yaml_linux_bo_ung_vien_dpkg (N1) | L | **Giết thật**: GITHUB_PATH=/usr/bin khác thư mục fixture tốt; không gán kill này cho nhánh âm |
| wp831_yaml_linux_quay_ve_command_v (N1) | L | **Giết thật**: wrapper không DAT khi rg hỏng đứng đầu PATH |
| wp831_yaml_linux_chi_theo_ma_thoat (N3) | L | **Giết thật**: rg exit 0 rỗng bị chọn/ghi GITHUB_PATH trước khi checker cuối từ chối |
| wp831_yaml_linux_khong_ghi_github_path | L | **Giết thật**: GITHUB_PATH rỗng thay vì prefix tốt |
| wp831_yaml_macos_bo_ung_vien_brew (N2) | M | **Giết thật**: không DAT khi bản hỏng đầu PATH |
| wp831_yaml_macos_chi_theo_ma_thoat (N3) | M | **Giết thật**: chọn/ghi candidate rỗng |
| wp831_yaml_macos_khong_ghi_github_path | M | **Giết thật**: GITHUB_PATH rỗng |
| wp802_yaml_chon_ung_vien_chi_theo_ma_thoat, neo dài mới | W | **Giết thật**, neo khớp đúng một lần; không mất mutant Windows sau khi có thêm hai checker |
| linux/macos_remove_select_path | L / M tương ứng | **Giết thật**: checker lại đo rg hỏng của PATH cũ |
| linux_wrong_install_prefix | P (L/M/W vẫn qua) | **Giết thật** bằng parity Linux; stub apt không tự phát hiện sai package |
| macos_wrong_install_prefix | L/M/W/P | **Sống sót**: đổi thành brew install other-package không ca nào bắt; r802 parity bỏ mục macOS, stub brew chấp nhận mọi lệnh install |
| linux/macos_remove_fileguard | L/M/W/P | **Sống sót** cả hai. Probe độc lập chứng minh tác dụng fileguard khi candidate vắng; chưa canh file không thực thi được (F01) |
| linux/macos_remove_init | L/M/W/P | **Sống sót** cả hai; phản chứng stale bổ sung vẫn rc 2, không nhận là lỗi head |
| linux/macos_remove_guard | L/M/W/P | **Sống sót** cả hai; for-return/&& đã fail trong các layout âm đo được |
| linux/macos_remove_fallback | L/M/W/P | **Sống sót** cả hai; probe fallback độc lập làm mutant rc 2 trong khi control rc 0 |
| linux/macos_reverse_order | L/M/W/P | **Sống sót** cả hai; fixture chỉ có một candidate tốt nên không canh ưu tiên giữa hai bản tốt |
| q1_hard_usrbin — đối chứng giữ đúng Q1 | L | Có TinHieuChotCa vì fixture yêu cầu đúng prefix tạm. **Không cộng vào bằng chứng giết lỗi sản phẩm**: /usr/bin là ứng viên spec yêu cầu |

22 biến thể gỡ/đổi chốt (không tính đối chứng Q1): **11 giết thật / 0 tín dụng giả / 11 sống sót**. Với từng survivor còn chạy thêm hai consumer YAML còn lại của module: r802_hook_windows_khong_cai_in_dung_lenh và r802_runner_tra_lai_con_tro_nguoi_goi; tất cả vẫn qua, survivor-consumers.json. Đối chiếu source consumer YAML không thấy thêm ca đọc hai công thức này. Không suy từ đây rằng đã chạy full suite hoặc mọi mutant toàn kho.

Các chốt **chưa có ca bắt trong tập consumer đó**: fileguard, init, guard cuối, command-v fallback, ưu tiên candidate, tiền tố install macOS. Survival là giới hạn độ phủ; không lập thêm finding sản phẩm chỉ vì survival. N1/N2/N3 đều có ít nhất một mutant bị đúng r831 tương ứng bắt, nhưng điều đó không chứng minh bao phủ hết mỗi tiêu chí.

## Finding mở

### F01 [P2] — chooser-checker-path-fallthrough

**Tệp:dòng:** ops/cong_cu.yaml:89 (Linux), ops/cong_cu.yaml:90 (macOS); consumer ops/cai_cong_cu.sh:72; phép chạy checker ops/cong_cu.py:127.

**Vấn đề:** `[ -f "$RG_D/rg" ]` chỉ kiểm tồn tại. Nếu file rg không executable, subprocess tra tên `rg` qua PATH bỏ qua file ấy và chạy bản tốt ở thư mục khác. Checker trả DAT nhưng RG_DICH vẫn được gán thư mục vừa bị bỏ qua. Head in/persist một thư mục không có rg chạy được, trái L1 và cam kết của chooser.

**Tái hiện đã chạy:** từ gốc rv1, `PYTHONDONTWRITEBYTECODE=1 python review-data/repro_f01.py`. Mỗi nền: prefix có rg mode 0644, PATH trước cài có rg executable tốt, installer stub rc 0. Wrapper head rc 0, JSON DAT, GITHUB_PATH=prefix. Chạy chính prefix/rg và shell bước sau chỉ nhận GITHUB_PATH+tools đều rc **126**, stderr **Permission denied**. Công thức base trên cùng loại layout in front tốt (extra.json). Biến thể thử chỉ thêm kiểm -x chọn front, hai probe sau rc 0; f01.json và f01-summary.log. Probe có assertion xác nhận cả lỗi và đối chứng, rc 0 của script nghĩa là tái hiện thành công.

**Hệ quả:** bước hiện tại báo thành công nhờ một rg khác; nếu rg tốt chỉ có trong export PATH của bước trước và không được persist, bước kế tiếp nhận sai thư mục rồi thất bại. Layout bước kế này được mô phỏng rõ bằng PATH trong f01.json; không tuyên bố đã có CI incident thật. Lỗi thư mục chọn sai đã có ngay trước mô phỏng bước kế.

**Hướng vá / khóa / rủi ro:** sửa hai công thức trong YAML để candidate phải thực thi được và checker thực sự đo binary thuộc thư mục ấy; tối thiểu thêm -x vào fileguard trước checker dùng chung trên POSIX đã đóng phản chứng này trong bản sao. Giữ nguyên một chuẩn parse của cong_cu.py, quoting, phần install đầu và GITHUB_PATH. Bổ sung fixture PATH đã tốt + candidate tồn tại nhưng không executable, đòi thư mục bản tốt, rồi gỡ chốt mới phải làm đúng r831 ĐỎ. Kiểm thêm candidate vắng, thực thi nhưng rc 1/rỗng/rác, symlink và đường có dấu cách. Rủi ro còn lại là sự thay đổi file giữa -x và probe; phép thử hiện tại không chứng minh loại race. Không giao bản vá runtime để áp mù; executor tự dẫn xuất và kiểm trong write set.

### F02 [P2] — linux-candidate-set-drops-usrbin

**Tệp:dòng:** ops/cong_cu.yaml:89, phần `awk ... {p = $0} END ...` và danh sách for; liên quan Q1, handoff ops/handoff/wp831-g1-claude.md:20.

**Vấn đề:** mỗi dòng dpkg khớp đè p; có một dòng khớp là `/usr/bin` không còn được thử riêng. Khi dpkg trả nhiều đường, một dòng cuối hỏng có thể che mất `/usr/bin/rg` tốt. Đây là sai khác hành vi với ứng viên cố định mà Q1 chốt, không chỉ sai khác chữ.

**Tái hiện đã chạy:** `PYTHONDONTWRITEBYTECODE=1 python review-data/repro_f02.py`. `/usr/bin/rg --version` thật rc 0/ripgrep 14.1.0. dpkg stub rc 0, stdout hai dòng: `/usr/bin/rg` rồi `<fixture>/other prefix/bin/rg` (exit 1); rg đầu PATH cũng exit 1. Head wrapper **rc 2**, GITHUB_PATH rỗng; chỉ thay candidate đầu về `/usr/bin` trên bản sao ⇒ **rc 0/DAT**, GITHUB_PATH=/usr/bin. f02.json ghi stdout dpkg, PATH, stdout/stderr wrapper và hai command; f02-summary.log. Script có assertion cho A/B. Probe nhiều dòng tốt/hỏng đảo thứ tự cũng cho rc 2 → rc 0 (behavior.json).

**Giới hạn:** dpkg thật trên host hiện chỉ khai `/usr/bin/rg`; không tuyên bố package Debian hiện tại có hai executable hoặc đã có sự cố production. Đây là biên nhiều dòng được assignment yêu cầu thử, trên đó hệ thống vẫn có chính candidate tốt Q1 yêu cầu mà head bỏ qua.

**Hướng vá / khóa / rủi ro:** giữ `/usr/bin` trong tập ứng viên theo thứ tự spec, thay vì dùng độ thuận tiện của fixture để bỏ nó. Nếu muốn dùng metadata bổ sung, cần xử lý nhiều dòng theo chính sách rõ ràng, không chỉ lấy dòng cuối, và không đánh mất candidate tốt đã được spec bảo đảm. Khóa bằng ca dpkg nhiều dòng với /usr/bin tốt/dòng cuối hỏng và đảo thứ tự, cộng các ca dpkg vắng/lỗi/rỗng. Giải quyết cách ly `/usr/bin` trong môi trường test hoặc seam đo có kiểm soát; nếu cần đổi hợp đồng/phạm vi thì điều phối cấp revision, không âm thầm đổi runtime để test xanh. Rủi ro: khi phục hồi candidate hệ thống, fixture hiện tại sẽ bị ảnh hưởng bởi rg có sẵn; phép đo q1.json đã chứng minh điều này. Không thêm fallback rộng hơn ngoài quyết định spec.

| Lớp | Biểu hiện / nguồn | Mức cao nhất mở | Điều kiện đóng |
|---|---|---|---|
| chooser-checker-path-fallthrough | F01 Linux + macOS tại reviewed_sha, cùng cơ chế PATH bỏ file nonexec | P2 | Cả hai công thức chọn đúng executable, tái chạy phản chứng và mutation gỡ chốt mới |
| linux-candidate-set-drops-usrbin | F02, sai khác Q1 và dpkg nhiều dòng tại reviewed_sha | P2 | Không mất /usr/bin tốt trong A/B; chính sách và test ứng viên phù hợp spec/revision được chốt |

Hai lớp, ba biểu hiện theo nền; không đếm Linux/macOS của F01 thành hai finding độc lập. Không P0/P1 phát hiện; không lập P3 mới chỉ từ survival. Đây là lượt 1 packet wp831; mẫu verdict wp802 không được dùng như bằng chứng đã đóng các lớp mới này.

## Giới hạn và toàn vẹn

Không đo native macOS/BSD dirname/awk, native Windows, CI/check-run exact head, lease live, receipt assurance hoặc quyền hệ thống của executor. Không có dữ liệu các phần đó thì ghi **KHÔNG ĐO ĐƯỢC**, không đọc thành pass. Full suite và mutation toàn kho chủ động not_run theo quyền tùy chọn của assignment. Kết quả updater/handoff được phân biệt với phép tự chạy; không dùng con số executor thay cho delta full suite tự đo.

VERDICT.md được ghi sớm và cập nhật sau các phần; lịch sử trước khi chốt giữ ở VERDICT-progress.md. source-before.json và source-after.json bao gồm hash/mode/symlink của checkout nguồn và .git; integrity.json ghi đối chiếu hai mốc, HEAD/tree/status/diff/index. Sandbox thực tế workspace-write; read-only với cay-kho là kỷ luật và phép so hai mốc, không tự nhận sandbox cưỡng chế hoặc chứng minh không từng ghi rồi hoàn nguyên. artifact-manifest.json neo path/size/SHA-256 các hiện vật chính sau khi writer kết thúc.

Đối chiếu cuối đã đạt: **4355/4355 file/link nguồn kể cả .git không đổi hash/mode/đích symlink**; HEAD/tree đúng neo; status tracked/untracked/ignored, diff và index đều rỗng. Bản sao head cũng sạch và giữ đúng SHA. Xem integrity.json.

**Quyết định cuối: changes_requested trên exact reviewed_sha nêu ở dòng 2.** Cần đóng F01/F02 rồi review SHA mới trong ngân sách được điều phối cấp; không tự mở thêm lượt, không tự đăng GitHub hoặc quyết định land.
