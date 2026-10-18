verdict: changes_requested
reviewed_sha: 75bcd43701652a2133bf1026be7f8ec9557de12a

F01/F02 đã đóng; các phép đo bắt buộc đã hoàn tất. Có F03 P2 mở: bộ chọn đổi Python khi thêm thư mục ứng viên vào PATH. Ngưỡng áp dụng: không còn P0/P1/P2 mới được approve.

Reviewer: Codex, họ OpenAI; công cụ shell chạy trực tiếp trong sandbox Linux, transport machine. Không có receipt để tự chứng nhận model variant/effort hay CLI/Desktop: **KHÔNG ĐO ĐƯỢC**. Không tự cấp assurance/transition/land authority. Đây là phiên reviewer độc lập theo assignment; executor được khai là Claude. Theo CLAUDE.md §Quy trình sửa code/5, subagent `tl_auditor` chỉ đọc và tiêu hoá log selftest, không chạy test hoặc ghi cây nguồn.

Neo đã tự đo: HEAD `75bcd43701652a2133bf1026be7f8ec9557de12a`; tree `018bf437fa0250e1154bc48f2c29473c82692fb2`; base/ref origin/master `1e69d2a0d3c708efe0dec86752fc13a0fe039aab`. SPEC-r1 sha256 `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888`; SPEC-r2 sha256 `3ab3aac4c68a7bbe87daf5dfee75c649ff46110697b2cd5b00b29586e4c253e7`. Cả ba tệp `diff.patch`, `numstat.txt`, `diff-tu-luot1.patch` khớp byte với Git ở đúng hai đầu mút. [preflight.json](preflight.json), [preflight.py](preflight.py).

## Đối chiếu finding lượt 1

| ID / slug giữ nguyên | Trạng thái | Phản chứng đã chạy và bằng chứng đóng |
|---|---|---|
| F01 P2 `chooser-checker-path-fallthrough` | **ĐÃ VÁ THẬT** trên Linux và macOS | `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_behavior.py`: ứng viên rg mode 0644, front rg tốt khác; head direct rc0, stdout cuối=front. Gỡ riêng `-x` ở mỗi công thức: rc0 nhưng stdout cuối=ứng viên 0644, tái hiện cơ chế cũ. Hai mutant ấy bị đúng r831 tương ứng bắt tại assertion dòng 8324, exception chính xác `TinHieuChotCa`. [behavior.json](behavior.json), [mutations.json](mutations.json). |
| F02 P2 `linux-candidate-set-drops-usrbin` | **ĐÃ VÁ THẬT** | Cùng script: seam vắng, `/usr/bin/rg` thật rc0/ripgrep; dpkg stub khai `/usr/bin/rg` tốt rồi đường khác hỏng. Head rc0, chọn `/usr/bin`, không gọi dpkg; recipe exact r1 từ Git `c3c790e` rc2. Đảo thứ tự hai dòng: head vẫn rc0, r1 rc0. Seam rỗng cũng chọn `/usr/bin`, không gọi dpkg. Gỡ ứng viên usrbin bị r831 Linux bắt tại dòng 8303. r2 đã ghi nhận seam, không còn sai Q1 bị phát hiện ở lượt 1. |

## Bảng săn — lệnh → kết quả thật → ý nghĩa

Lệnh dưới đây tính từ gốc rv2; lệnh gate nội bộ chạy với cwd `review-data/head` hoặc `review-data/base`, đúng SHA, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` nằm trong review-data. Installer chỉ là stub; không cài apt/brew thật. Windows/macOS dưới đây là recipe chạy trên Bash Linux, không phải chứng nhận native.

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| `python review-data/preflight.py` | rc0; 3/3 artifact byte-identical; spec hashes đúng; 7 tệp, **220 thêm / 17 xoá** | Đúng trần 7/450; không suy danh tính từ tên nhánh. |
| Đối chiếu AST base/head của `scripts/tl_selftest.py` | Đúng 2 giá trị Constant đổi 187→189, không đổi AST khác; text diff chỉ thêm/sửa chú thích slot | Đúng phạm vi r2 tại `_c291_docs_ngoai_goi` và `_c357_agents_ngoai_goi`; [static-checks.json](static-checks.json). |
| YAML parse + đối chiếu install prefix trước ` && ` đầu tiên | Linux, macOS, Windows đều byte-identical với base; source ca r802 parity byte-identical | N3 giữ nguyên install; kiểm riêng macOS vì r802 parity không đọc mục này. |
| `python review-data/probe_behavior.py` | rc0, **31/31 probe** đạt assertion | Hai nền: candidate tốt/có stderr, hỏng rc1, rc0-rỗng, token rác, candidate thiếu, 0644, symlink tốt/hỏng, fallback, prefix/repo/GITHUB_PATH có dấu cách, biến GITHUB_PATH vắng; wrapper thật và direct eval. [logs/behavior.log](logs/behavior.log). |
| Cùng probe, installer stub exit9 | Hai nền rc9, GITHUB_PATH rỗng | Không chọn tiếp khi install thất bại. |
| Cùng probe, âm rc1/rỗng/rác | Hai nền rc≠0, GITHUB_PATH rỗng | Không tính rc0 không parse được là rg đạt. |
| `python review-data/audit_mutations.py` | rc0; 18 exception đúng loại và có frame ca đích; 0 exception ngoài loại, 0 survival | 8/8 mutant bắt buộc giết bằng assertion hành vi. Một mutant bổ sung Linux-fallback bị chặn cấu trúc `dirname` trước khi đến phép đo hành vi; không cấp tín dụng hành vi cho kill đó. Chi tiết bảng dưới. |
| `python review-data/repro_python_path.py` | rc0 của script tái hiện; cả hai recipe **bare PY rc2**, **absolute PY rc0/in đúng candidate**, wrapper thật **rc2**; checker với Python ban đầu **rc0/DAT** | F03: thêm PATH đổi interpreter của checker, không phải rg hỏng. [python-path.json](python-path.json), [logs/python-path.log](logs/python-path.log). |
| `python review-data/check_signing_env.py` | rc0 của probe; Git commit trong mini-repo kế thừa global signing **rc128**, lỗi socket signer bị sandbox chặn; thêm `-c commit.gpgsign=false` **rc0** | Giải thích nghi can của hai fail selftest r226/r268; đây là cấu hình test Git, tách khỏi ratchet/F03. [signing-env.json](signing-env.json). |

## Bảng đột biến

L = `r831_cai_rg_linux_chon_ban_chay_duoc`; M = `r831_cai_rg_macos_chon_ban_chay_duoc`; W = `r802_cai_rg_windows_chon_ban_chay_duoc`. Script chỉ ghi YAML riêng trong `review-data/mutants/`, đổi con trỏ YAML_DANG_DUNG của module test bản sao. Không sửa YAML của source/head. Mỗi neo phải khớp đúng một lần. Tín dụng đòi **type(exception) chính xác là TinHieuChotCa**, traceback có function object của ca đích và `bang`; không coi rc khác 0/exception khác là kill.

| Chốt → mutant | Ca | Giết thật / tín dụng giả / sống sót; assertion thực sự |
|---|---|---|
| `-x` Linux → `linux_remove_x` | L | **Giết thật**, helper `_wp831_cai_rg_chon_ban_chay_duoc`:8324; in nhầm candidate 0644. |
| `-x` macOS → `macos_remove_x` | M | **Giết thật**, cùng assertion 8324. |
| `/usr/bin` Linux → `linux_remove_candidate` | L | **Giết thật**, :8303; wrapper rc2 thay vì DAT. |
| brew candidate → `macos_remove_candidate` | M | **Giết thật**, :8303; wrapper rc2. |
| checker Linux → chỉ đo `rg --version`, `linux_exitcode_selector` | L | **Giết thật**, :8311; rg rc0-rỗng bị chọn/ghi GITHUB_PATH rồi checker cuối từ chối. |
| checker macOS → chỉ đo `rg --version`, `macos_exitcode_selector` | M | **Giết thật**, :8311, cùng cơ chế. |
| điều kiện GITHUB_PATH Linux → ghi vô điều kiện | L | **Giết thật**, :8317; tên trần DAT nhưng file path vẫn bị ghi. |
| điều kiện GITHUB_PATH macOS → ghi vô điều kiện | M | **Giết thật**, :8317. |
| bỏ toàn bộ ghi path, mỗi nền | L/M | **2 giết thật**, :8306; GITHUB_PATH rỗng trong chiều phải persist. |
| bỏ fallback `command -v` macOS | M | **Giết thật**, :8324; candidate 0644 không còn fallback tốt, rc1. |
| bỏ fallback `command -v` Linux | L | `TinHieuChotCa` thật, **kill cấu trúc** tại `_wp802_rg_yaml`:8182 do không còn `dirname`; không gán kill này cho kiểm hành vi fallback. |
| Năm `stock_wp831_yaml_*` nguyên văn trong head | L/M theo khai báo | **5 giết thật**, neo mỗi cái=1: usrbin, brew, Linux checker, macOS -x, Linux điều kiện GITHUB_PATH. Không thất thoát mutant bởi sửa neo. |
| `stock_wp802_yaml_chon_ung_vien_chi_theo_ma_thoat` neo dài | W | **Giết thật**, neo=1, đúng exception/frame W; checker cuối từ chối candidate rỗng do bộ chọn sai. |

Tổng 18 mutant: 17 kill hành vi + 1 kill cấu trúc; 0 tín dụng từ exception ngoài loại, **không chốt bắt buộc nào sống sót**. Chỉ kết luận trong tập đã chạy, không nhận đây là `--dot-bien` toàn kho. Việc giảm xuống 5 stock wp831 đã kiểm từ bảng thật. Sàn `_dot_bien_du_san` ≥70% còn nguyên; con số Windows 197/281 và CI run do executor khai **KHÔNG ĐO ĐƯỢC** tại phiên này.

## Seam CONG_CU_GOC

`CONG_CU_GOC` là biến môi trường có tác dụng thật nếu được đặt, không được cưỡng chế chỉ trong test. Khi vắng hoặc rỗng, `${CONG_CU_GOC:-}/usr/bin` chính là `/usr/bin`; đã chạy cả hai. Khi có giá trị, nó đổi candidate đầu thành `<giá trị>/usr/bin`; phép test đường có khoảng trắng đã chạy được. `sudo apt-get install -y ripgrep` nằm trước và giữ nguyên; biến không thay package hay đích apt. Giá trị nằm trong dấu ngoặc kép và chỉ được khai triển thành dữ liệu đường dẫn, không được eval lại như mã shell.

Hướng lạm dụng (chỉ mô tả, **không soạn payload**): bên điều khiển được môi trường và thư mục prefix có thể đặt một chương trình giả rg trong candidate, cho nó khai phiên bản hợp lệ, để được thực thi ở quyền của tiến trình checker. Nếu rg tên trần vẫn hỏng và GITHUB_PATH được đặt, thư mục đó có thể được persist cho bước sau. Do đó không nên mô tả seam là hoàn toàn vô hiệu ngoài test. Tuy nhiên cùng actor đã có thể điều khiển PATH/rg/brew/Python của chính tiến trình; chưa thấy đường đưa dữ liệu từ actor ít quyền hơn vào biến này, không có đường sudo/apt nhận prefix, và chưa có bằng chứng mở biên đặc quyền mới. Không nâng thành finding an ninh độc lập chỉ từ khả năng tự đặt env. F03 bên dưới là lỗi đổi interpreter dưới môi trường hợp lệ, không cần payload tấn công.

## Finding mới mở

### F03 [P2] — chooser-path-reselects-python

**Tệp:dòng:** `ops/cong_cu.yaml:93` (Linux) và `ops/cong_cu.yaml:94` (macOS), đoạn `PATH="$RG_D:$PATH" "${PY[@]}" ops/cong_cu.py ...`. Caller thật đặt `PY=(python)` / `(python3)` / `(py -3)` bằng tên tại `ops/cai_cong_cu.sh:14`; :77 còn gọi lại cùng tên sau khi export PATH. Test direct F01 dùng `PY` absolute tại `.claude/dev/launcher_test.py:8289`, nên không canh được layout này.

**Cơ chế và hệ quả:** PATH tiền tố vốn để chọn rg cũng đổi executable Python khi `PY[0]` là tên trần. Nếu `/usr/bin` hay brew bin có Python khác (ví dụ thiếu PyYAML) trong khi Python ban đầu của môi trường đã đủ dependency, candidate rg tốt vẫn bị từ chối vì checker không chạy được bằng interpreter vừa được chọn lại. Khi front rg hỏng, không còn candidate được chọn: install thoát 2 dù rg candidate thực thi được và được chính checker ban đầu nhận DAT. Tình huống nhiều Python là cùng loại môi trường setup-python/system-python mà packet đã tránh ghi GITHUB_PATH vô điều kiện; điều kiện ghi mới không ngăn việc đổi Python ngay trong selector.

**Phản chứng đã chạy:** từ gốc rv2, `PYTHONDONTWRITEBYTECODE=1 python review-data/repro_python_path.py`. Dùng venv thật `venv.EnvBuilder(with_pip=False, symlinks=False)`, không cài gói/mạng; đặt rg stub hợp lệ cạnh Python venv chưa có yaml; front rg exit1; apt/brew stub rc0. Linux dùng seam r2 để mô phỏng candidate hệ thống, macOS lấy prefix từ brew stub. Python ban đầu import yaml rc0; cùng tên `python` sau prepend resolve vào venv và `ModuleNotFoundError: No module named 'yaml'`. Mỗi nền: direct recipe với **PY=(python) rc2**; chỉ đổi đầu vào PY sang đường tuyệt đối ban đầu, giữ nguyên recipe, **rc0/in đúng candidate**. **Wrapper thật rc2**. Checker thật gọi bằng đường tuyệt đối Python ban đầu với PATH đã prepend candidate **rc0/DAT**. Script rc0 nghĩa là tất cả assertion tái hiện/đối chứng đã đạt; [python-path.json](python-path.json) chứa command, stdout, stderr, đường dẫn và kết quả.

**Giới hạn nguồn gốc:** caller dùng tên Python và export PATH đã có ở base; không gán toàn bộ lỗi caller cho packet. Tuy nhiên hai selector POSIX mới thêm lời gọi checker dưới PATH đổi ở chính dòng sửa, và N1/N2 vẫn không đạt trên layout hợp lệ đã đo. Không suy rằng native macOS hay runner CI hiện có đúng layout này.

**Vá ở đâu / hướng vá:** giữ danh tính interpreter dùng để đọc YAML/checker từ trước khi prepend candidate, xuyên suốt selector và phép kiểm cuối. Chỗ cần xét là hai recipe và ranh giới caller `ops/cai_cong_cu.sh`, không sửa regex của rg. Ghim đường dẫn thực thi trước khi đổi PATH là hướng hẹp nhất; nếu cần sửa caller đang ngoài write set, điều phối phải cấp revision/phạm vi tương ứng. Chỉ ghim PY bên trong eval/subshell chưa chứng minh đã sửa :77 của caller sau export PATH; phải đo end-to-end, không chỉ control direct trong phản chứng này. Không giao patch runtime để áp mù.

**Ca khoá / đột biến:** thêm chiều nhiều interpreter vào cả r831: Python ban đầu có PyYAML, candidate directory có Python thật không có PyYAML và rg tốt, front rg hỏng; đòi wrapper thật rc0/DAT và đúng thư mục/GITHUB_PATH. Bỏ ghim interpreter phải làm chính ca đó đỏ bằng TinHieuChotCa. Giữ cả nhánh Python3 và mảng `py -3`/đường có khoảng trắng trong phạm vi giải pháp được cấp.

**Rủi ro của hướng vá:** mất argument của `py -3`, phá quoting/space/symlink, hoặc chỉ giữ interpreter trong command substitution nhưng phép đo cuối vẫn đổi Python. Persist cả candidate directory vẫn có thể đổi các công cụ khác ở bước kế khi bare rg hỏng; điều kiện GITHUB_PATH hiện tại chỉ xử lý nhánh bare rg đã tốt, không chứng minh cách ly mọi công cụ cùng thư mục.

Không phát hiện P0/P1; không lập P3 mới chỉ vì survival/CI chưa truy cập. F03 P2 còn mở nên verdict hiện tại là **changes_requested** dù F01/F02 đã đóng.

## Bảng săn gate — bổ sung kết quả đã hoàn tất

| Lệnh (cwd bản sao) | Kết quả thật | Ý nghĩa |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | Không auth và auth giả: đều rc0, **1/1 qua, 0 bỏ qua, 0 hỏng** | Chạy trong head exact SHA; log riêng theo tên ca dưới logs/. |
| `PYTHONDONTWRITEBYTECODE=1 python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_macos_chon_ban_chay_duoc --lan 1` | Không auth và auth giả: đều rc0, **1/1 qua, 0 bỏ qua, 0 hỏng** | Chạy trong head exact SHA; log riêng theo tên ca dưới logs/. |
| `PYTHONDONTWRITEBYTECODE=1 python .claude/dev/launcher_test.py --lap-ca r802_cai_rg_windows_chon_ban_chay_duoc --lan 1` | Không auth và auth giả: đều rc0, **1/1 qua, 0 bỏ qua, 0 hỏng** | Chạy trong head exact SHA; log riêng theo tên ca dưới logs/. |
| `PYTHONDONTWRITEBYTECODE=1 python .claude/dev/launcher_test.py --lap-ca r802_bang_cai_rg_khop_cong_cu_yaml --lan 1` | Không auth và auth giả: đều rc0, **1/1 qua, 0 bỏ qua, 0 hỏng** | Chạy trong head exact SHA; log riêng theo tên ca dưới logs/. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (core.abbrev=7) | Head rc0, **ok=true, expected=checked=189**, failed=[], extra_files=[]; base rc2, ok=false, 187/187, extra_files=[changelog.d/wp-802.md] | N5/L3 đạt; không sinh lại manifest để làm xanh. |
| `python scripts/tl.py doc-claims-check --strict` | Base/head rc0, ok=true | N4 doc-claims đạt. |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | Base/head rc0; 10 tệp, 0 chỗ | N4 doctrine đạt. |
| `python -m ruff check --no-cache --select F .claude/dev/launcher_test.py` | Base/head rc1; cùng 5 chẩn đoán, code+message multiset giống nhau | Delta 0, không gọi bare lint là sạch. |
| Cùng lệnh Ruff cho `scripts/tl_selftest.py` | Base/head rc1; cùng 4392 chẩn đoán, code+message multiset giống nhau | Delta 0 cả tệp mới được r2 cấp phép. |
| `python scripts/tl.py --selftest`, môi trường Git kế thừa | Base/head đều rc1, **1729/1731**, đúng hai FAIL r226/r268; r291/r357 đều OK | Delta 0, chưa gọi đây là N/N. Signer toàn cục lỗi socket đã có phản chứng riêng. Lượt cô lập signing và mutant được ghi trong mục kết quả cuối bên dưới. |

Bằng chứng có cấu trúc: [gates-summary.json](gates-summary.json); command/cwd/rc/thời gian và headline nằm trong từng `logs/*.result.json`.


## Selftest và ratchet — kết quả cuối

Mọi full selftest chạy **tuần tự**, cùng TMPDIR dưới review-data; không chồng ca dùng tệp tạm cố định. [run_checks.py](run_checks.py) chạy head, base, rồi hai mutant; [finish_checks.py](finish_checks.py) đợi kết quả mutant cuối và đợi bytes head được hoàn nguyên mới chạy head sạch với Git config cô lập.

| Phép đo | Kết quả thật | Kết luận |
|---|---|---|
| Head/base với cấu hình Git kế thừa | Cả hai rc1, 1729/1731; chỉ r226/r268 FAIL | Delta 0, không tính lỗi signer là lỗi packet. |
| `GIT_CONFIG_GLOBAL=<review-data/gitconfig-selftest> PYTHONDONTWRITEBYTECODE=1 python scripts/tl.py --selftest` trên head sạch | **rc0, tl 1731/1731**, transport 12/12; không FAIL | **N6 N/N đạt** sau khi cô lập Git signing của fixture. Config riêng include config cũ rồi đặt commit.gpgsign=false và core.abbrev=7; không sửa global/home hoặc mã nguồn để làm xanh. |
| Head mutant chỉ r291:189→187 | **rc1, 1728/1731**, `[FAIL] r291_docs_ngoai_goi`; r357 OK; còn đúng hai lỗi signer nền | **Giết thật r291**, delta FAIL={r291}; không nhận ba FAIL thành ba kill. |
| Head mutant chỉ r357:189→187 | **rc1, 1728/1731**, `[FAIL] r357_agents_ngoai_goi`; r291 OK; còn đúng hai lỗi signer nền | **Giết thật r357**, delta FAIL={r357}. |
| Trích nguyên hàm ratchet từ AST để chạy cô lập, có manifest 189 | Control cả hai True; chỉ đổi r291 thì chỉ r291 False; chỉ đổi r357 thì chỉ r357 False | Bổ sung xác nhận đúng ca, độc lập lỗi signer. Đây không được đếm là full selftest; hai mutant full ở trên mới là bằng chứng `[FAIL]` của harness thật. |

Log full: [head sạch N/N](logs/head-selftest-unsigned.log), [r291→187](logs/head-ratchet-291-187.log), [r357→187](logs/head-ratchet-357-187.log). [selftest-summary.json](selftest-summary.json) ghi command/cwd/rc/headline và delta; [ratchet-isolated.json](ratchet-isolated.json) ghi ma trận bổ sung. Không chạy lại full base trong config unsigned: so delta dùng hai lượt base/head cùng config kế thừa; không suy lượt base unsigned là đã chạy.

## Write set và toàn vẹn cuối

| Đường dẫn so base | Dòng thêm | Dòng xoá |
|---|---:|---:|
| `.claude/dev/launcher_test.py` | 102 | 1 |
| `RELEASE_MANIFEST.json` | 16 | 6 |
| `changelog.d/wp-831.md` | 13 | 0 |
| `docs/GOI_AGENT_DA_NEN.md` | 17 | 3 |
| `ops/cong_cu.yaml` | 10 | 2 |
| `ops/handoff/wp831-g1-claude.md` | 55 | 0 |
| `scripts/tl_selftest.py` | 7 | 5 |
| **Tổng** | **220** | **17** |

Đúng **7/7 đường dẫn** lease r2 nêu trong assignment, **220≤450 dòng thêm**. Git diff --check rc0. Không xác minh lease/CI live vì assignment cấm GitHub.

Nguồn cay-kho giữ nguyên **4355/4355 file/link kể cả .git** về hash/mode/đích symlink; HEAD/tree/base không đổi, status sạch. Hai bản sao cũng sạch sau khi hoàn nguyên các mutant. [integrity.json](integrity.json), [source-before.json](source-before.json), [source-after.json](source-after.json). Sandbox workspace-write không tự cưỡng chế cay-kho read-only; đây là kỷ luật không ghi và phép so đầu/cuối, không phải chứng minh không từng ghi rồi hoàn nguyên.

**KHÔNG ĐO ĐƯỢC:** native Windows/macOS, CI/check-run exact head, lease/receipt/assurance live và danh tính model/effort đo bằng receipt. `environment_status` không có trong tool catalog phiên này; không suy readiness credential/network. **not_run:** full launcher suite có/không auth và --dot-bien toàn kho; bằng chứng ở đây là 4 ca bắt buộc ×2 môi trường auth cùng tập mutant đã liệt kê, không lấy lời khai executor thay phép tự chạy. Không gọi GitHub, push, merge, land, deploy hay sửa cay-kho.

**Kết luận: changes_requested trên exact SHA ở dòng 2.** F01/F02 **ĐÃ VÁ THẬT**; các gate và ratchet được đo như trên; **F03 P2 chooser-path-reselects-python còn mở**, nên chưa đạt ngưỡng approve. Cần giải quyết danh tính Python xuyên suốt selector/caller và khoá bằng phép đo wrapper nhiều interpreter trong phạm vi được cấp.
