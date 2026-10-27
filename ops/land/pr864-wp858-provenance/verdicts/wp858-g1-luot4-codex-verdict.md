verdict: changes_requested
reviewed_head: 93fd69fb958527ba738f882391956311972de60b
reviewed_sha: 93fd69fb958527ba738f882391956311972de60b
reviewed_tree: 0c2ead6f7c80324ed92f921da79b48e488084877
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_run: b31b149abcc3416a9fea16cbcc47b7cc

## Kết luận

**F858-03 CHƯA ĐÓNG lớp lỗi.** Biểu hiện không LF của lượt 3 đã được vá thật: phản chứng cũ nay rc=0, cả `rg`/`bash` DAT; đột biến bỏ LF đầu dòng canh bị chính ca N4 giết. Tuy nhiên, stdout của **tiến trình con installer ghi muộn**, sau khi hàm đã in `/dev/null`, vẫn được nhận thành `DICH`. Trên head nguyên vẹn, fixture này cho **rc=2, rg=DO, bash=DAT, 3/3 lần**; hai đối chứng độc lập đều **rc=0/DAT, 3/3**. Không thể kết luận đóng lớp bằng ranh giới LF khi stdout còn nhiều writer.

**F858-06 ĐÓNG trong phạm vi finding gốc — ĐÃ VÁ THẬT.** Mutant gắn `cygpath -u` với điều kiện ghi PATH bị ca Windows giết bằng `TinHieuChotCa`, không chỉ shape. **F858-01/02/04/05 không hồi quy trong phạm vi đã đóng**; diff là **6 tệp, 448 dòng thêm, 30 xoá**.

Có **F858-07, P2, về độ phủ test**: chiều mới đặt `GITHUB_PATH=""`, chưa đo biến **không tồn tại**. Mutant chỉ bỏ xử lý mặc định của biến này sống qua 6/6 ca liên quan và không thêm lỗi ở toàn suite; phép riêng không đặt biến phân biệt head rc=0/DAT với mutant rc=1. Đây không phải lỗi runtime của head nguyên vẹn. F858-06 giữ ID/trạng thái của phép chuyển đổi Windows đã sửa; F858-07 nhắm guard biến tuỳ chọn ở một nhánh khác, ảnh hưởng cả ba nền.

Không phát hiện P0/P1 trong phạm vi đã đo. Còn **2 finding P2 mở: F858-03 và F858-07**, không có quyết định chủ kho chấp nhận chúng trong nguồn được cấp. Áp điều kiện sensitive và lease M-1, chưa đủ để approve. Verdict này không cấp quyền merge/land/deploy.

## Neo và phạm vi đo

HEAD/tree như header; merge-base với `origin/master`: **637f78029f5a5fe56d35199dd0f75c50274f2c0f**. Spec đọc bằng `git show origin/ops/wp858-spec:ops/specs/wp858.md`, SHA-256 **5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54**, khớp assignment. Lease g2 đọc offline từ ref được cấp: generation 2, hết hạn **2026-10-24T04:32:00Z**, `nang_tran: []`, chỉ thị thu về ≤450. Base khởi đầu lease `3a3a3ca…` không bị dùng thay merge-base thực tế sau Q7. [HEAD/tree](evidence/head-tree.stdout), [merge-base](evidence/merge-base.stdout), [spec](evidence/spec.stdout), [lease](evidence/lease.stdout).

Đã tự `git show` **cả ba verdict trước, đều rc=0** trên `origin/ops/wp858-r1-g2-lease`. Bản lượt 3 bằng byte với `../VERDICT-luot3.md`, SHA-256 **79c5f24d9b73008f104bed2238dbc7a9838702f27455aef9faaf545a98a811ad**. Hạn chế provenance ở lượt 3 nay đã được giải quyết đối với ba tệp verdict trong ref cục bộ; không suy thành xác nhận trạng thái GitHub hiện tại. [Lượt 1](evidence/previous-1.stdout), [lượt 2](evidence/previous-2.stdout), [lượt 3](evidence/previous-3.stdout), [băm/đối chiếu](evidence/compression-audit.json).

Danh tính lấy từ [header đúng run](evidence/model-header.txt) và [metadata chọn trường](evidence/run-identity.json). Header chỉ chứng minh cấu hình CLI công bố, không chứng minh model phục vụ từng request. Đây là reviewer độc lập, có shell/tools, không tái dùng context executor; không suy identity từ actor đăng GitHub.

`kho/` chỉ đọc. Clone nền/head được dựng trong **cùng một lần** `python -B out/review.py setup`, không hardlink, cùng origin, local `core.abbrev=7`; mọi test, fixture, mutant nằm dưới `out/`. Môi trường Linux x86_64, Python **3.13.16**, PyYAML **6.0.3**, sandbox **workspace-write**, không phải mount toàn bộ `kho/` read-only. Dùng `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `TMPDIR=<out>/tmp`, auth fixture giả khi cần; không cài dependency qua mạng. Không gọi GitHub, push hoặc sửa sản phẩm. [Driver](review.py), [runtime](evidence/runtime.json).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn liền trước: lượt 3, reviewed SHA **8733f0ae7df5d9a1c704c31e6051e8cb5f439fe5**. Số liệu bên dưới được reviewer tự chạy lại; lời khai executor không được dùng làm pass.

| Finding trước | ĐÓNG / CHƯA ĐÓNG và phân loại | Lệnh → kết quả thật trên head hiện tại |
|---|---|---|
| **F858-01** — nuốt lỗi ghi PATH/`-w` | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `python -B out/probes.py direct`: git/shellcheck/bash × Linux/macOS/Windows mô phỏng đều rc=0/DAT, ghi đúng ứng viên, Windows có `W:`; đích ghi là thư mục đều **rc=1**; `-w` lỗi đều **rc=1**, không ghi PATH. `probes.py mutations`: bỏ trả lỗi ghi bị ca hành vi cả ba nền giết; bỏ trả lỗi `-w` bị ca Windows giết bằng **TinHieuChotCa**. |
| **F858-02** — fixture Windows không phân biệt đổi đường | **ĐÓNG phạm vi gốc — ĐÃ VÁ THẬT; không hồi quy** | `probes.py mutations`: control 6/6 PASS; bỏ `cygpath -u` bị ca Windows và shape giết bằng **TinHieuChotCa**. Ánh xạ `V:` còn buộc phải đổi. Hàm không tái đưa bộ lọc `-f/-x/.exe` cũ vào. Chưa suy kết quả này thành nghiệm thu native Windows. |
| **F858-03** — stdout installer thành kết quả chọn | **CHƯA ĐÓNG lớp — VÁ HỜ ở cấp lớp; biểu hiện không LF đã vá thật** | `probes.py batch`: shell lượt 3 + stdout bash không LF + thư mục `<prefix>/dev/null/rg` hỏng, thứ tự rg,bash ⇒ **rc=2/rg=DO**; head cùng phép ⇒ **rc=0/cả hai DAT**. Mutant bỏ LF đầu dòng canh bị **N4** giết bằng TinHieuChotCa. Nhưng `followup.py delayed`: stdout muộn trên head ⇒ **3/3 rc=2/rg=DO**, như finding bên dưới. |
| **F858-04** — thiếu ca âm cho lỗi `-u` | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `probes.py direct`: stub `-u` in đường đúng rồi thoát 37 ⇒ head **rc=1**, PATH file rỗng. `probes.py mutations`: chỉ bỏ `return 1` của handler ⇒ chính ca Windows ném **TinHieuChotCa**; shape cũng chết. |
| **F858-05** — vượt trần diff | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `git -C kho diff --numstat 637f78029f5a5fe56d35199dd0f75c50274f2c0f HEAD` ⇒ **6 tệp, 448 thêm/30 xoá**. `python -B out/audit.py`: không mất hàm/ca/assert; YAML và AST selftest không đổi so lượt 3; không bỏ mutant cũ. Không có nâng trần. |
| **F858-06** — chỉ đổi `-u` khi ghi PATH | **ĐÓNG phạm vi finding gốc — ĐÃ VÁ THẬT** | `probes.py mutations`: mutant `u-only-when-gp` bị **r858_cai_windows_chon_ban_chay_duoc** và shape giết bằng **TinHieuChotCa**. `probes.py direct` cũng đo head với cả biến rỗng và biến bị bỏ hẳn: **rc=0/DAT** trên ba công cụ Windows. Không gọi việc đóng mutant này là đầy đủ coverage biến tuỳ chọn: xem F858-07. |

Bằng chứng chi tiết: [edges](evidence/direct-edges.json), [ma trận stdout](evidence/stdout-edges.json), [đột biến độc lập](evidence/independent-mutations.json), [diff lượt 3→4](evidence/since-round3.stdout), [kiểm cấu trúc](evidence/compression-audit.json).

## Finding mới và biểu hiện còn mở

| ID | Mức | Tệp:dòng tại reviewed head | Lệnh → kết quả thật | Đề xuất |
|---|---|---|---|---|
| **F858-03 — biểu hiện tiếp, giữ ID/lớp** | **P2** | `ops/cai_cong_cu.sh:44`, tương tác reader `:120`–`:123`; fixture N4 `.claude/dev/launcher_test.py:8510`, `:8632` | `python -B out/followup.py delayed`: stub installer **bash** tạo một con giữ stdout, trả 0; con đợi 2 giây rồi in thư mục đầu PATH. Head nguyên vẹn: **3/3 rc=2, rg=DO,bash=DAT**. Trace có `/dev/null` trước, sau đó `DICH=<sân>/dau`, rồi `export PATH=<sân>/dau:…`. Cùng fixture, chỉ chuyển dòng muộn sang stderr: **3/3 rc=0/DAT**; chỉ cho stdout được ghi trước khi installer trả về: **3/3 rc=0/DAT**. [Driver](followup.py), [log](evidence/delayed-controls-run.log), [trace đầy đủ](evidence/delayed-controls.json). | Hợp đồng kết quả chọn phải phân biệt được log installer với kết quả ngay cả khi có writer giữ stdout sau khi installer cha trả về. Thêm ca N4 này và hai đối chứng; không chỉ thêm LF. Nếu phải tách kênh/đổi reader ngoài Q1 thì xin authority điều chỉnh phạm vi; hoặc cần quyết định chủ kho chấp nhận rõ giới hạn writer muộn. Đây là hướng bằng lời, không kèm patch runtime sensitive. |
| **F858-07** | **P2** | `.claude/dev/launcher_test.py:8535`, `:8573`; guard được bảo vệ `ops/cai_cong_cu.sh:54` | `python -B out/probes.py mutations`: mutant **gp-unset-nounset** thay duy nhất `if [ -n "${GITHUB_PATH:-}" ]; then` thành `if [ -n "$GITHUB_PATH" ]; then` ⇒ **6/6 ca r858 liên quan PASS**, kể cả shape. `python -B out/survivor.py`: control và mutant đều **221/234, 13 đỏ/10 bỏ qua, rc=1**, cùng đúng tập lỗi/bỏ qua, **delta lỗi=0**. `python -B out/followup.py unset`: biến rỗng ⇒ cả hai rc=0/DAT; **bỏ biến khỏi env** ⇒ head **rc=0/DAT**, mutant **rc=1**, báo `GITHUB_PATH: unbound variable`, trên Linux/macOS/Windows mô phỏng. [Mutant nguyên văn](mutants/gp-unset-nounset.sh), [6 ca](evidence/independent-mutations.json), [toàn suite](evidence/suite-delta.json), [đối chứng](evidence/unset-gp-controls.json). | Giữ chiều rỗng, thêm chiều thực sự loại biến khỏi env cho installer thật, ứng viên tốt/tên trần hỏng; đòi rc=0/DAT và không ghi PATH. Đăng ký mutant bỏ mặc định biến và đòi ca hành vi giết bằng TinHieuChotCa. Head hiện tại xử lý đúng; finding yêu cầu bổ sung test, không sửa runtime cho lỗi chỉ có trong mutant. |

**Cơ chế F858-03:** command substitution chờ EOF của pipe, gồm descriptor còn mở ở con installer. Hàm có thể đã in dòng canh nhưng con ấy vẫn ghi sau đó. `tail -1` nhận dòng muộn, `[ -d ]` chấp nhận thư mục fixture, và PATH bị đẩy về nơi có `rg` hỏng. Đây là một đường khác vào cùng lớp `stdout-installer-bi-nhan-lam-ket-qua-chon`, không phải một ID mới. Đã chạy bằng stub vô hại; **chưa chứng minh trình cài thật thường có hành vi này**. Các test hiện có chỉ cho installer ghi đồng bộ nên không đóng được hợp đồng rộng hơn ấy.

F858-06 và F858-07 không cùng nhánh sản phẩm: F858-06 kiểm việc **gọi `-u` ở dòng 48** độc lập với việc ghi PATH; F858-07 kiểm **đọc biến tuỳ chọn ở dòng 54 dưới `set -u`**. Ca dùng biến rỗng đã giết đúng mutant F858-06, nhưng không thể phân biệt hai cách đọc biến khi nó vắng. Giữ lịch sử liên quan này; không tái gọi F858-06 là chưa được sửa để che kết quả dương.

## Đánh giá phạm vi `rg` và các byte stdout

Đồng ý xếp **stdout không LF của installer `ripgrep` trong công thức `rg` riêng** là nợ có sẵn, ngoài phần vá helper của WP858: `audit.py` xác nhận toàn mục `cong_cu.rg` bằng nhau giữa merge-base và head; Q1 cho giữ công thức riêng, Q8 yêu cầu đo/ghi lỗi packet khác, không tự vá. `python -B out/followup.py rg` trên nền và head, cùng fixture: **LF đều rc=0/rg=DAT; không LF đều rc=2/rg=DO**. Nợ có bằng chứng, không được gọi là đã sửa; đề nghị handoff tiếp tục giữ tên `rg-installer-stdout-khong-LF`. [Phép đo](evidence/rg-scope-controls.json), [kiểm YAML](evidence/compression-audit.json).

Việc này **không** bao phủ F858-03 còn mở: trong phản chứng writer muộn, installer ripgrep **im lặng**; stdout gây lỗi chỉ đến từ installer bash đang đi qua helper mới.

| Phép thử stdout của installer bash | Head hiện tại | Đối chứng shell lượt 3 |
|---|---|---|
| LF; không LF với `<prefix>/dev/null/rg` hỏng | Cả hai thứ tự đều **rc=0/DAT** | Không LF, thứ tự rg,bash: **rc=2/rg=DO**; thêm LF: rc=0. |
| CR đơn cuối; CRLF cuối | Cả hai thứ tự đều **rc=0/DAT** | Đều rc=0 ở fixture này. |
| Tiền tố rồi NUL | Cả hai thứ tự đều **rc=0/DAT**; Bash cảnh báo bỏ NUL | Thứ tự rg,bash **rc=2/rg=DO**. |
| Chỉ in tiền tố ra stderr | Cả hai thứ tự đều **rc=0/DAT** | Đều rc=0. |
| Con installer ghi thư mục ra stdout sau khi cha trả về | Thứ tự rg,bash **rc=2/rg=DO**, kể cả ba lượt có trace | Cũng rc=2 ở phép ma trận; không phải lỗi mới do thêm LF. |

[Ma trận đầy đủ](evidence/stdout-edges.json). Đã kiểm cả nhánh chọn thư mục: `followup.py chosen`, installer git in tiền tố không LF ⇒ head **rc=0/git=DAT**; mutant chỉ bỏ LF đầu dòng in `$dich` ⇒ **rc=2/git=DO**; thêm LF vào log thì cả hai rc=0. Mutant ấy bị shape giết, **các ca hành vi hiện có không giết nó**; đây là giới hạn tín dụng hành vi, không báo thành mutant sống toàn suite. [Đối chứng](evidence/chosen-path-controls.json).

## Bảng lớp nguyên nhân

Giữ sáu slug của lượt 3; thêm một slug cho guard biến vắng. **7 lớp / 7 IDs; 2 lớp mở P2**. Phần native Windows chưa đo vẫn giữ giới hạn, không được biến thành xác nhận cả nền.

| Slug | IDs / nguồn | Trạng thái, mức cao nhất còn mở | Phép kiểm đóng lớp |
|---|---|---|---|
| `loi-ghi-path-bi-nuot-trong-command-substitution` | F858-01, lượt 1 `bfbd273…` | Đóng phạm vi gốc | Lỗi ghi/`-w` trả khác 0; control dương ghi đúng; mutant chết bằng ca hành vi. |
| `fixture-windows-khong-phan-biet-chuyen-doi-va-duoi-exe` | F858-02, lượt 1 | Đóng phạm vi gốc | Ánh xạ `V:` phân biệt phép đổi; không tái thêm bộ lọc cũ. Native còn chưa đo. |
| `stdout-installer-bi-nhan-lam-ket-qua-chon` | F858-03, lượt 1→4 | **Mở P2** | Cùng một cơ chế tách/nhận diện kết quả phải qua log đồng bộ, không LF, collision và writer muộn trong phạm vi helper; N4/control không làm PATH quay lại bản hỏng. `rg` riêng là nợ ngoài phạm vi Q1/Q8. |
| `cygpath-u-error-guard-khong-co-ca-am` | F858-04, lượt 2 | Đóng | Ca âm `-u` có stdout hợp lệ giết mutant bỏ trả lỗi bằng TinHieuChotCa. |
| `vuot-tran-diff-sensitive-chua-co-ngoai-le` | F858-05, lượt 2 | Đóng | ≤450 dòng thêm, ≤6 tệp, không mất chốt cũ; hiện 448/6. |
| `chuyen-doi-windows-gan-nham-voi-github-path` | F858-06, lượt 3 | Đóng phạm vi finding gốc | Windows DAT khi không ghi PATH; mutant gắn nhầm bị ca hành vi giết. |
| `fixture-luon-dat-github-path-bo-sot-unset` | F858-07, mới lượt 4; liên hệ coverage F858-06 | **Mở P2** | Biến vắng và biến rỗng đều DAT; mutant bỏ mặc định biến bị ca hành vi giết, control còn qua. |

## Thu gọn diff và đột biến

448 dòng thêm phân rã: **launcher_test 365 + manifest 11 + changelog 13 + shell 33 + YAML 15 + selftest 11**. `git diff --check` rc=0. So với lượt 3: **461 hàm → 461; 244 ca @ca → 244; 818 lời gọi bang → 819; 85 assert → 85**. Không mất tên hàm; các bảng mutant giữ mọi tên cũ, thêm đúng hai mutant mới. YAML parse bằng nhau; AST selftest bằng nhau. Bốn thân hàm test đổi đúng fixture installer/bash, chiều GITHUB_PATH rỗng, biến thể không LF của N4 và shape. Diff shell chỉ đổi hai lệnh in và chú thích; không nới reader. [Numstat](evidence/scope.stdout), [diff](evidence/since-round3.stdout), [audit AST/bảng mutant](evidence/compression-audit.json).

Fixture `cai_in` đã chuyển sang **chỉ installer bash**; ghi rõ sự thu hẹp này, không dùng nó để kết luận đã xử lý stdout installer rg. Phép `followup.py rg` ở trên đo nợ đó riêng trên cả nền/head.

`probes.py mutations` chạy **control + 8 mutant × 6 ca**. Control 6 PASS; bảy mutant bị giết ít nhất một ca, một mutant sống (`gp-unset-nounset`). Hai mutant mới đăng ký của lượt này bị giết đúng bởi **N4** và **ca Windows**, ngoài shape. Mutant bỏ LF đầu nhánh chọn thư mục chỉ bị shape giết; không cộng shape vào tín dụng ca hành vi. Không có lỗi setup được tính là kill trong bộ độc lập này. [Kết quả](evidence/independent-mutations.json), [các shell mutant](mutants/).

## Bảng lệnh → kết quả thật

Lệnh tính từ workspace trừ khi ghi cwd. Mỗi subprocess gate có argv/cwd/rc/thời lượng trong `evidence/<tên>.json`, stdout/stderr ở tệp cùng tên. Driver đo edge trả rc=0 để lưu cả kết quả dương/âm; rc driver không biến rc=2 trong finding thành pass.

| Lệnh / cwd | Kết quả thật |
|---|---|
| `python -B out/review.py setup` | **rc=0**; HEAD/tree/nền/spec đúng; ba verdict `git show` đều **rc=0**; hai clone cùng điều kiện. |
| `git -C kho diff --numstat <merge-base> HEAD`; `diff --check` | **6 tệp/448 thêm/30 xoá**, trong write set; check **rc=0**, rỗng. |
| `python -B out/audit.py` | **rc=0**; số ca/assert/mutant như trên; bản lượt 3 bằng byte; `rg` bằng nền. |
| `python -B out/review.py suites`: `python .claude/dev/launcher_test.py --nhat-ky <log>` ở mỗi clone, có/không auth giả | Driver **rc=0**, **bốn suite đều rc=1**; bảng bên dưới, không xác nhận headline executor 242/242 trong sandbox này. |
| `python -B out/probes.py direct`; `batch`; `mutations` | Mỗi driver cuối **rc=0**; các rc con và TinHieuChotCa như bảng finding. [Direct](evidence/direct-edges.json), [batch](evidence/stdout-edges.json), [mutations](evidence/independent-mutations.json). |
| `python -B out/followup.py delayed`; `unset`; `rg`; `chosen` | Đều **rc=0 driver**; A/B rc con **0/1/2** như trên, có trace. |
| `python -B out/survivor.py`: cặp control/mutant chạy toàn launcher suite cùng origin/config/env | Driver **rc=0**; cả hai suite **rc=1, 221/234**, cùng 13 lỗi/10 bỏ qua; mutant sống không tương đương. [Control](evidence/matched-control.stdout), [mutant](evidence/matched-mutant-unset-gp.stdout), [delta](evidence/suite-delta.json). |
| `python .claude/dev/launcher_test.py --dot-bien` ở `out/head` | **rc=0, 295/295 đạt, 4 không đo được**. Với ca gốc tạm, control đang lỗi môi trường nên không lấy dòng mutant “OK” làm chứng nhận native N5. [Log](evidence/launcher-mutations.stdout). |
| Hai `python scripts/tl.py --selftest` song song, env ký commit kế thừa | Cả hai **rc=1, 1729/1731**, đúng `r226` và `r268` đỏ; **edit_skill_assert_count_gate_dry qua cả hai**. Global `commit.gpgsign=true`, local clone false không truyền vào mini-repo của test. [Lượt 1](evidence/parallel-selftest-1.stdout), [lượt 2](evidence/parallel-selftest-2.stdout), [cấu hình](evidence/git-signing-config.stdout). |
| `python -B out/selftest_retry.py`: hai selftest song song, chỉ đặt `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=commit.gpgsign`, `GIT_CONFIG_VALUE_0=false` cho subprocess | **Cả hai rc=0, 1731/1731**; mục edit-skill qua cả hai. Không ghim abbrev bằng env, để r226 tự đổi config của fixture. Không sửa Git config toàn cục/cây review. [Lượt 1](evidence/parallel-selftest-nosign-1.stdout), [lượt 2](evidence/parallel-selftest-nosign-2.stdout), [env/rc](evidence/parallel-selftest-nosign-1.json). |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ở `out/head` | **rc=0, ok=true, expected=checked=190**, failed/extra/missing rỗng. [Log](evidence/release-verify.stdout). |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` ở `out/head` | **rc=0, 61 ca**, bỏ qua=0, tiền kiểm bỏ qua=0, cổng cây thật ĐẠT; **470 mutant giao job mảnh, không đo đủ bán kính trong lệnh này**. [Log](evidence/cong-cu-manh.stdout). |
| `python scripts/tl.py golden-test --json`; `doc-claims-check --strict --json` ở `out/head` | Đều **rc=0, ok=true**. [Golden](evidence/golden.stdout), [doc-claims](evidence/doc-claims.stdout). |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` ở `out/head` | **rc=0**, sạch. [Log](evidence/doctrine.stdout). |
| `bash -n ops/cai_cong_cu.sh`; `actionlint` ở `out/head` | Đều **rc=0**, stdout/stderr rỗng. [Bash](evidence/bash-syntax.json), [actionlint](evidence/actionlint.json). |
| `python -m ruff check --no-cache --select F scripts/tl.py scripts/tl_selftest.py .claude/dev/launcher_test.py` ở nền/head | Cả hai **rc=1, 4409 finding**, delta=0. **Bare lint có nợ nền**, không gọi là pass tuyệt đối. Ruff **0.17.1**. [Nền](evidence/ruff-base.stdout), [head](evidence/ruff-head.stdout), [version](evidence/ruff-version.stdout). |
| `python -B -c '<runpy ci_dang_ky_test.py; loi_ruff_ci()>'` ở `out/head`; argv nguyên văn trong JSON | **rc=0, RUFF_CONTRACT 3 []**. Đây là pin/probe contract của workflow, tách khỏi bare lint thật bằng Ruff 0.17.1 nêu trên. [Log](evidence/ruff-contract.stdout), [argv](evidence/ruff-contract.json). |
| `python -B out/review.py snapshot` | **rc=0**, snapshot trước/sau bằng nhau: HEAD/tree/status và hash **4899 tệp kể cả Git metadata**, tracked/untracked/ignored không delta. [Integrity](evidence/integrity.json). |

| Cây / auth | Passed | Skipped | Failed | Tổng | rc |
|---|---:|---:|---:|---:|---:|
| Nền / không giả | 214 | 10 | 12 | 236 | 1 |
| Nền / giả | 214 | 10 | 12 | 236 | 1 |
| Head / không giả | 221 | 10 | 13 | 244 | 1 |
| Head / giả | 221 | 10 | 13 | 244 | 1 |
| Head control cặp mutant | 221 | 10 | 13 | 244 | 1 |
| Mutant F858-07 | 221 | 10 | 13 | 244 | 1 |

**Delta thô nền→head là +1 ca đỏ**, đúng ca mới `r858_goc_tam_tranh_to_tien_co_git`. Trên head, nó và t86 chọn `/var/tmp` rồi **EROFS**; nền t86 bị Codex home nằm dưới tổ tiên `.git`. **11 lỗi r484** chung giữa nền/head. `/tmp/.git` có mount ro; `/dev/shm` cũng bị mount ro trong sandbox. Không đổi lỗi thành skipped, không sửa ca của packet khác để ép xanh, không tuyên bố delta lỗi bằng 0 cho cặp nền/head. Delta bằng 0 chỉ áp cho **cặp control/mutant F858-07**. [Tập lỗi/bỏ qua](evidence/suite-delta.json), [mountinfo](evidence/mounts.log).

## Không đo được

- **Native Windows/macOS, Git Bash/MSYS, `.exe`/PATHEXT và installer thật**: chưa có capability. Windows/macOS ở các fixture trên là mô phỏng trên Linux; chưa xác nhận Windows floor 70% hay N2 native.
- **N5 xanh end-to-end, hai launcher suite ×10**: không đo được vì tổ tiên `/tmp/.git` ro và gốc thay thế không ghi được. Không tháo mount/nới sandbox; không lặp phép lỗi để gọi là chứng nhận thành công.
- **10 ca launcher bỏ qua**: 8 cần venv/pip không dựng được offline và 2 liên quan Windows; giữ riêng trong evidence. 11 lỗi r484 vẫn là failed do môi trường, không cộng vào skipped/pass.
- **CI/GitHub/lease live**: theo yêu cầu không gọi GitHub; chưa xác nhận check-run ci.yml, workflow_dispatch Windows, thread resolution hoặc heartbeat hiện tại. Snapshot lease và verdict cục bộ không chứng minh trạng thái dịch vụ.
- **Handoff**: `git show origin/ops/wp858-r1-g2-lease:ops/handoff/wp858-g1-claude.md` **rc=128**; ref g1 không nằm trong bundle. Không xác nhận nội dung handoff ngoài nguồn đã cấp. [Lỗi đọc](evidence/handoff-g2.stderr). Khác với ba verdict trước: cả ba verdict đã đọc được.
- **470 mutant cong_cu_test**: chưa có kết quả job mảnh/gom; 61 ca và launcher 295/295 không thay phép đo bán kính ấy.
- **Python**: chỉ nghiệm thu phạm vi (a) chủ kho đã cấp trong assignment—rc=0, không in/ghi thư mục bản hỏng. Ca Python hiện qua; nợ **python-probe-khong-theo-PATH** còn nguyên, không khai đã probe đúng Python ứng viên theo PATH.
- Không thực hiện hướng cần tự soạn nội dung nhạy cảm; các khuyến nghị runtime chỉ mô tả bằng lời. Các stub đã chạy chỉ in đường dẫn fixture và mã phiên bản giả, không cài thật.

Sai sót giàn giáo reviewer được giữ riêng: lần đầu `direct` đụng `KeyError: env` vì interceptor cũng nhận lời gọi probe Bash không có tham số env; đã sửa chỉ xử lý khi có env rồi chạy lại đầy đủ, không tính lỗi đầu là finding/kill. Probe Ruff contract đầu lấy nhầm phần tử của tuple `(errors, count)` nên assert đỏ dù trả `([], 3)`; đã sửa đúng hợp đồng, kết quả cuối rc=0; giữ [log lỗi giàn giáo](evidence/ruff-contract-reviewer-assertion-error.stderr). Hai selftest kế thừa global signing đỏ được giữ cùng kết quả chạy lại có env cụ thể, không xoá bằng chứng ban đầu.

Snapshot sạch chỉ chứng minh không có delta quan sát được tại hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không có patch sản phẩm, commit, push hoặc liên lạc GitHub. Hash verdict, driver và evidence trong [SHA256SUMS](SHA256SUMS); các clone/fixture lớn không nằm trong danh mục băm này.
