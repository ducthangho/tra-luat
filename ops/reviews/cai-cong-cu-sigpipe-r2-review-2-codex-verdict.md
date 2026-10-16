# Cross-review độc lập — packet #675 r2 g2 — lượt 2
verdict: changes_requested
reviewed_sha: 1ea9c1c16b4b731b457c8436c4c88c0eb69f4ce0
reviewed_tree: 681bd8ec9d083c09fb9bf096b263dee01c1d9555
baseline_sha: cd23c7dbc7833d64a8e87e8ffd94f194c18e0060

Reviewer độc lập, provider OpenAI; execution surface: Codex qua API với shell cục bộ; transport: machine/tool trực tiếp. Không sửa hai cây nguồn, không push, không đăng GitHub. Bản sao và phép đo nằm trong `tam/tmp.dcbYQp7XH2/`; log và mã tái lập được giữ làm bằng chứng, thư mục tạm do test sinh được dọn riêng.

HƯỚNG 1: Neo nguồn và phạm vi

- Giả thuyết: đúng HEAD, baseline, SPEC và W1–W5.
- Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}; git -C cay-nen rev-parse HEAD; sha256sum SPEC.md; git -C cay-kho diff --name-only 89fc4fa..HEAD; git -C cay-kho diff --numstat cd23c7d..HEAD -- ops/cai_cong_cu.sh ops/cai_actionlint.sh ops/dung_goi_review.sh ops/do_sigpipe.sh ops/don_ref_chot_test.sh; git -C cay-kho status --short; git -C cay-nen status --short`.
- Output: HEAD/tree/baseline như trên; SPEC `81fb6d533a892ec33c9b6b3f161dc1eca971579f4acfdb277c26521539be71cc`; chỉ W1–W5. Numstat thêm/xóa: W1 3/1, W2 2/1, W3 2/1, W4 221/0, W5 6/2; tổng 234 dòng thêm ≤300. Hai status rỗng, rc=0.
- Kết luận: KHÔNG PHẢI LỖI; đủ điều kiện tiếp tục đo. Diff sản phẩm lấy từ `89fc4fa`; baseline nghiệm thu vẫn là `cd23c7d`.

Model/effort: GPT-6 theo chỉ dẫn phiên; effort KHÔNG ĐO ĐƯỢC. Đây là tự khai, không có attestation runtime độc lập. Không suy danh tính model từ actor GitHub.

HƯỚNG 2: Chạy lại W4 và phản chứng quay về nền

- Giả thuyết: head xanh; từng W1–W3 nền đỏ đúng SIGPIPE; W5 nền bị khóa B1 bắt.
- Lệnh: `python tam/tmp.dcbYQp7XH2/measure.py mutations` (log `logs/mutations.jsonl`; từng stdout/stderr/argv/rc nằm trong `logs/`). Harness dùng `subprocess.Popen` với tín hiệu con mặc định, `TMPDIR` dưới scratch và cấu hình Git chỉ trong môi trường tiến trình (`commit.gpgsign=false`, `core.abbrev=7`).
- Output: head `57/57 DAT`, rc=0, 11,132 s; `--goc base` `50/57`, rc=1, 13,659 s. Ba điểm baseline đều `(b) rc0=0 rc141=10 khac=0`, `(d) rc=141` không sentinel; B1 explicit có hai dòng mỗi biến. Chỉ trả W1, W2 hoặc W3 về nền: từng bản sao `55/57`, rc=1, đúng điểm đó đỏ (b)/(d). Chỉ trả W5 về nền: `56/57`, rc=1, đúng (e) `khop-dau-tuong-minh` đỏ.
- Kết luận: KHÔNG PHẢI LỖI trên các phép đo này. 57 = 3 × (14 đầu vào + 4 phép b/c/d) + 3 ca B1; không lấy N/N làm bằng chứng vét cạn.

HƯỚNG 3: B1 và tính tương đương của W5

- Lệnh: `python tam/tmp.dcbYQp7XH2/extra.py b1_exact`; `python tam/tmp.dcbYQp7XH2/measure.py regressions`. Recorder `env()` giữ ranh giới đối số bằng NUL; script lấy nguyên hàm `lam()` từ mỗi cây, chạy dưới `set -uo pipefail` như lượt 1. Logs: `b1-exact.jsonl`, `b1-{head,base}-*.stdout`, `head-w5.stdout`, `base-w5.stdout`.
- Output: explicit ở đầu + 20.000 đối số đệm: head chỉ `GIA_REF_STATE=explicit`, `NEO_TEP=explicit`; baseline thêm cả hai fallback phía sau. Không match → cả hai sinh `refstate`/`neo_auto`. Rỗng, explicit rỗng, biến lặp, match chuỗi con, khoảng trắng/glob, chỉ ref hoặc chỉ neo: head/nền cùng hành vi sau chuẩn hóa đường dẫn tạm. Toàn bộ W5: head `105/105`, rc=0 (4,199 s); nền `105/105`, rc=0 (4,150 s).
- Có khác biệt ngoài payload lớn: với hai đối số hợp lệ `X=$'a\nGIA_REF_STATE=z'` và `Y=$'a\nNEO_TEP=z'`, baseline không nối mặc định vì grep khớp ĐẦU DÒNG nằm bên trong giá trị; head nối đủ hai mặc định vì không có ĐỐI SỐ nào bắt đầu bằng hai tên đó. KHÔNG PHẢI LỖI của r2: đúng quy tắc **đầu từng đối số** SPEC §4 yêu cầu. Vì thế không tuyên bố tương đương tuyệt đối trên mọi giá trị có LF.
- Kết luận: B1 hành vi W5 **ĐÃ VÁ THẬT** trong tập đo; SPEC r2 §2 đã đính chính đúng lời loại trừ sai. Độ dính của khóa (e) được đo riêng ở HƯỚNG 5.

HƯỚNG 4: F1 — phản chứng cũ và đường thứ ba sau điểm cắt

- Lệnh: `python tam/tmp.dcbYQp7XH2/measure.py mutations`; `python tam/tmp.dcbYQp7XH2/postcut.py` (log `mutations.jsonl`, `postcut.jsonl`).
- Đúng hai đột biến lượt 1, `unused() { <LENH>; }` không gọi và `: <<'REVIEW_COMMENT' ...`, nay đều W4 `56/57`, rc=1 ở (d); chạy toàn bộ W1 đều rc=1 `LENH: unbound variable`. Bọc `if false`, subshell, đặt `exit`/`return` trước dòng cũng đều bị (d) bắt. Với hàm/if/subshell, rc=2 của fixture là lỗi cú pháp do bị cắt trước dấu đóng; đó không phải bằng chứng đã chạy một script đầy đủ. Head không bị những lỗi này.
- Đường thứ ba: giữ nguyên dòng LENH, thêm ngay SAU đó `export LENH=false` → W4 **57/57, rc=0**, toàn bộ W1 **rc=1**, không probe. Thêm `exit 0` sau dòng → W4 **57/57, rc=0**, toàn bộ W1 rc=0 nhưng không chạy probe. Thêm phép gán pipeline cũ qua `eval` sau dòng → W4 **57/57**, trong khi script đầy đủ lại gặp SIGPIPE (xem log `whole-w1-pipeline-after`).
- Cơ chế: `ops/do_sigpipe.sh:122` dùng `head -n "$TRICH_SO"`, nối sentinel và `exit 0`, nên TOÀN BỘ mã sau phép gán bị bỏ khỏi phép (d). (a)/(b) cũng chỉ chạy dòng trích. Việc có một phép gán đúng phía trước không khóa được giá trị hoặc mã thoát tại điểm sử dụng thật.
- Kết luận: **G1 — P2, F1 còn mở ở cấp lớp lỗi (VÁ HỜ/đã chặn đúng hai phản chứng cũ)**. Đây là lỗi độ dính của phép đo W4, chưa phải P1 trong W1–W3 hiện hành.

Bổ sung HƯỚNG 4 — cùng đường lọt trên cả ba điểm, không cần `eval`:

- `postcut.py` nối ngay sau mỗi dòng vá nguyên phép gán nền với tiền tố `:; ` (ví dụ `:; LENH="$(printf '%s\n' "$DAU_RA" | head -1)"`). Đây là Bash hợp lệ, nhưng không khớp regex `^BIEN=` lần thứ hai.
- Output `w4-all-three-postcut.stdout`: **57/57 DAT, rc=0**. Chạy TOÀN BỘ từng script với fixture offline: head W1/W2/W3 **rc=0/0/0**, W1 có `PROBED`, W2 trả đường dẫn cài, W3 `GOI DU DE TAI DO: 1/1/1 ref, 0 lech`; ba bản đột biến **rc=141/141/141**. Logs `whole-postcut-{head,mutant}-{0,1,2}.{stdout,stderr,json}`. G1 không chỉ là mất một sentinel giả định: cả ba script thực đều có thể lại chết SIGPIPE mà W4 vẫn xanh.

HƯỚNG 5: Phép (e) có gọi đúng hàm W5 đang chạy?

- Giả thuyết: trích `sed -n '/^lam() {/,/^}/p'` có thể hồi sinh hàm nằm trong here-doc, bỏ qua hàm runtime.
- Lệnh: `python tam/tmp.dcbYQp7XH2/extra.py w5_runtime`. Đột biến bản sao W5: bọc nguyên hàm head trong `: <<'REVIEW_DEAD_LAM' ... REVIEW_DEAD_LAM`; đặt ngay sau đó nguyên hàm baseline với khai báo Bash hợp lệ `lam () {`. Không thay W4. Sau đó chạy toàn bộ W5 và nối một lời gọi stress với recorder trước khi shell thoát. Mã/nguồn mutant được giữ tại `extra.py`, `mutants/w5-dead-lam/`, `w5-runtime-{head,mutant}/`.
- Output: `w4-w5-dead-lam.stdout` **57/57 DAT, rc=0**. Cả hai W5 toàn bộ vẫn **105/105, rc=0**. Lời gọi stress cuối head ghi explicit mỗi biến một lần; mutant ghi explicit rồi **thêm `refstate` và `neo_auto`**, tức B1 đã tái xuất hiện trên đường chạy thật. Logs `whole-w5-{head,mutant}.stdout`.
- Kết luận: **G2 — P2**, `ops/do_sigpipe.sh:139–144`: (e) chỉ kiểm một bản hàm được trích theo văn bản, chưa neo vào hàm mà W5 thực thi. W5 hiện hành đã sửa B1, nhưng khóa hồi quy B1 có thể xanh khi bản vá chỉ còn trong mã chết.

HƯỚNG 6: Công cụ phụ, payload B1 và fixture offline

- Lệnh: `python tam/tmp.dcbYQp7XH2/extra.py dependencies`; `python tam/tmp.dcbYQp7XH2/extra.py safety`; chạy thêm W4 `--goc mutants/baseline-3` với PATH chứa `deps/seq-format`. Wrapper chỉ trả127 cho `seq -f`, mọi dạng `seq` khác chuyển tiếp binary thật.
- Output: git hỏng → rc=2; tar hỏng → rc=2 và KHÔNG ĐO ĐƯỢC; sha256sum hỏng → rc=127; toàn bộ seq hỏng → rc=1, `45/57`; không trường hợp nào trong bốn trường hợp ấy xanh. Nhưng riêng `seq -f` hỏng → **57/57, rc=0** trên head (`--lan 1`) VÀ **57/57, rc=0** trên W5 nền (`--lan 10`). stderr có `REVIEW_MISSING_TOOL seq`, stdout vẫn cấp N/N. Logs `deps-seq-format*.{stdout,stderr,json}`.
- Kết luận: **G3 — P2**, `ops/do_sigpipe.sh:145`: `mapfile -t PAD < <(seq -f ...)` không chuyển rc của producer tới shell cha, không kiểm `${#PAD[@]}`. Ba ca (e) chạy với payload rỗng, W5 cũ lại xanh. Phản chứng không còn ≥20.000 đối số như lời khai.
- Fixture offline: lượt trace đã sửa harness (`safety-w4-corrected`) **57/57, rc=0**; wrapper curl/wget/ssh không được gọi; mọi remote/clone Git ghi trong `safety/commands.log` đều là đường dẫn của kho giả dưới TMPDIR. `tmp_before=[]`, `tmp_after=[]`. Đọc xtrace của shell và nguồn W4 cho thấy gói tar tự tạo, AL_GOI/AL_DICH/sentinel/kho Git nằm trong thư mục tạm; không thấy đường tải mạng hoặc rác còn lại trong lần đo này.
- Giới hạn: lần trace đầu reviewer dùng PS4 tham chiếu BASH_SOURCE không có default, làm bash `-c` dưới `set -u` lỗi; đã sửa riêng harness `${BASH_SOURCE:-cmd}`, không sửa sản phẩm, rồi đo lại. `strace -f -e trace=network,file true` rc=1, `PTRACE_TRACEME: Operation not permitted`: **KHÔNG ĐO ĐƯỢC syscall audit toàn cục** về mọi ghi/connection ngoài cây. Không nâng wrapper/xtrace thành chứng minh syscall tuyệt đối.

HƯỚNG 7: F2, F3 và giới hạn corpus glob của lượt 1

- Lệnh: `python tam/tmp.dcbYQp7XH2/measure.py mutations`; các bản W4 đột biến giữ riêng tại `w4-score-function.sh`, `w4-score-callsite.sh`, `w4-no-glob.sh`.
- **F2 — ĐÃ VÁ THẬT:** xóa riêng W1/W2/W3/W5 đều rc=2, stderr `KHÔNG ĐO ĐƯỢC: thieu tep <đúng tên tệp>`, không có tổng kết xanh. Logs `w4-missing-{0,1,2,3}`. Preflight ở :69 và lỗi copy được chuyển thành `khong_do`.
- **Corpus glob — ĐÃ VÁ THẬT:** nối CHÍNH đột biến lượt 1 `; LENH="${LENH//\*/}"` vào dòng W1 → `54/57`, rc=1; đúng ba đầu vào glob mới đỏ. Gỡ ba đầu vào glob khỏi bản sao W4, giữ cùng mutant → `48/48 DAT`, rc=0. Khoá mới có răng, không chỉ tăng số N. Reviewer còn chạy lại `old_review_checks.py equivalence`: 604 đầu vào × 3 điểm × 3 chế độ = **5.436** so sánh, tất cả rc=0, `mismatches=[]` (log `equivalence.json`). KHÔNG PHẢI LỖI khai triển glob/CR trong W1–W3 hiện hành.
- **F3 — đóng nhánh trong helper, còn mở nhánh cấp điểm:** đổi điều kiện :101 của `cham_b` thành `if true; then KQ=DAT` → head `54/57`, rc=1, cả ba (c) đỏ với `cham ra DAT, rc141=10`. Điều này xác nhận bản vá dùng chung helper có tác dụng.
- Tuy nhiên, chạy lại đúng hình dạng đột biến lượt 1 tại nhánh thực sự CẤP ĐIỂM (b), nay ở :184: `if [ "$KQ" = DAT ]; then ghi 0` → `if true; then ghi 0`. Head vẫn **57/57, rc=0**; trên W1–W3,W5 nền **53/57, rc=1**, nhưng **KHÔNG có (b) đỏ và KHÔNG có (c) đỏ**. Chỉ (d) ba điểm và (e) B1 cứu tổng kết. Logs `w4-mut-score-callsite{,-base}`. Không tuyên bố bản mutant này làm cả baseline xanh; phản chứng là (c) vẫn không xác nhận đường cấp điểm (b) từ chối rc141.
- Kết luận: **G4 — P2 (F3 còn mở một phần)** ở `ops/do_sigpipe.sh:183–185,202–204`. Hai nơi dùng chung giá trị KQ nhưng (c) không đi qua nhánh tiêu thụ KQ để ghi điểm của (b); khoá “đổi nhánh chấm (b) luôn đúng ⇒ (c) ĐỎ” vẫn lọt tại nhánh đó. Đây là phép đột biến của chính hợp đồng F3, không phải sửa hàm tổng kết hoặc làm sai bộ đếm toàn suite.

HƯỚNG 8: Hồi quy và delta head/nền

Lệnh: `python tam/tmp.dcbYQp7XH2/measure.py regressions`; `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.dcbYQp7XH2/t5_repeat.py`. Các lệnh trong bảng chạy trên bản sao đầy đủ `head/`, `base/`, với TMPDIR riêng và chữ ký commit fixture tắt chỉ qua env; mọi subprocess khôi phục tín hiệu mặc định. ShellCheck là binary 0.11.0 đã có sẵn từ scratch lượt 1, sao chép vào `bin/`; không tải công cụ qua mạng. Logs `regressions.jsonl`, `t5-repeat.jsonl` và từng stdout/stderr.

| Phép đo | Head | Nền | Delta/kết luận |
|---|---|---|---|
| `bash ops/don_ref_chot_test.sh` | 105/105, rc0, 4,199s | 105/105, rc0, 4,150s | Cùng 105 tên ca, stdout 5.314 byte giống hệt |
| `python ops/bash_nen.py quet --root .` | DAT, rc0, 23,513s | DAT, rc0, 23,426s | stdout 41 byte giống hệt |
| `python .claude/dev/ci_dang_ky_test.py` | 938/938 phản chứng, rc0, 7,766s | 938/938, rc0, 7,269s | stdout 54.062 byte giống hệt |
| `actionlint .github/workflows/*.yml` có ShellCheck | rc1, 0,733s | rc1, 0,953s | Cùng SC1003 tại ops-don-ref.yml:117, stdout 224 byte giống hệt; lỗi nền, delta0 |
| `shellcheck --format=json W1 W2 W3 W5 [W4 trên head]` | rc1, 1,218s | rc1, 1,083s | Cùng SC1090 tại cai_cong_cu.sh:54; JSON 216 byte giống hệt; W4/W5 không thêm lỗi |
| t5: installer thật + gói offline 1.7.7, PATH có bản sai 9.9.9; lặp 200 lần | **200/200** rc0 và JSON DAT/1.7.7; rc141=0; 69,809s | **199/200**, rc141=1; 105,106s | Head đạt phần lặp A2; race nền tái hiện một lần. Không coi baseline đỏ này là lỗi mới |
| `python ops/cong_cu_test.py` đầy đủ | not_run | not_run | **KHÔNG ĐO ĐƯỢC**, không chạy hai suite ~40 phút/cây; không chứng nhận A2 toàn bộ |

Kết quả hoàn tất `lease_publish_test.py` được ghi dưới đây; không lấy các dòng QUA giữa chừng thay cho tổng kết toàn bộ.

Bổ sung kết quả hoàn tất A6:

- Lệnh: `python tam/tmp.dcbYQp7XH2/measure.py lease head` và `python tam/tmp.dcbYQp7XH2/measure.py lease base` (mỗi lệnh gọi đúng `python ops/lease_publish_test.py`, timeout ngoài1200s).
- Output: head **187/187 đạt; đã chạy=187, bỏ qua=0**, rc=0, **445,015s**; nền cùng **187/187**, rc=0, **445,969s**. Danh sách 187 tên ca và kết quả ở cấp suite ngoài giống nhau (`lease-outcomes-{head,base}.json`). Delta lỗi=0, kể cả bộ gọi W5. Hai cây có các chẩn đoán giả lập Windows ở stderr; không có ca bỏ qua và không biến chẩn đoán thành assertion lỗi. Không cần quy lỗi drift master cho packet.
- `bash -n` từng `ops/*.sh`: head8/8, nền7/7 rc0 (W4 là tệp mới). Môi trường đo: Linux x86_64, Bash5.2.21, Python3.11.15, Git2.43.0, actionlint1.7.7, ShellCheck0.11.0; lệnh `--version`/output lưu trong `logs/version-*`.

Bổ sung phép gỡ khóa:

- W4 bản sao `w4-disabled-d.sh`: đổi riêng điều kiện chấm (d) thành `if true`; chạy với hai mutant F1 cũ (`unused-function`, `heredoc`, `--lan 1`) đều **57/57, rc0**. Khi giữ khóa, cả hai **56/57, rc1** như trên. Điều này chứng minh chính (d) bắt hai ca cũ, không phải phép khác vô tình đỏ.
- W4 bản sao `w4-disabled-f2.sh`: gỡ preflight :69 và nhánh `|| khong_do` của cp :194, chạy với thiếu W2 → **rc1**, `cp: cannot stat`, không KHÔNG ĐO ĐƯỢC. Bản thật → rc2, đúng tên tệp. Logs `w4-disabled-*` chứa argv và output đầy đủ.

HƯỚNG 9: Commit, chú thích và giới hạn lời khai

- Lệnh: `git -C cay-kho log 89fc4fa..HEAD --format=fuller`; `sed -n '1,54p' ../review1/SPEC.md`; `nl -ba cay-kho/ops/do_sigpipe.sh`; đối chiếu các phép đo trên.
- Output: số **2/3000**, **0/3000**, “một write() mỗi dòng” trong commit r1/chú thích W1/W4 trùng bằng chứng **phiên điều phối** ghi tại SPEC r1 §2. Chú thích không ghi rõ nguồn; vật liệu chỉ định không cung cấp log executor đo lại 3000 lượt. Commit r2 nói rõ fixture cắt sau dòng, dùng chung `cham_b`, và trích `lam()`.
- Kết luận: **KHÔNG ĐO ĐƯỢC** nguồn gốc executor tự đo lại 3000 lượt và cơ chế syscall chính xác (strace bị chặn); không kết luận số liệu giả chỉ vì thiếu log, không thêm P3 về nghi ngờ đó. Nên ghi rõ nguồn SPEC r1 §2 nếu giữ số lịch sử. Số 10/10 SIGPIPE, head57/57, corpus glob, B1 và gate ở trên là số reviewer tự chạy lại. Các giới hạn của lời “đường chạy thật” và khóa chấm đã có finding G1/G2/G3/G4; không đếm trùng thành lỗi tài liệu riêng.

ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding lượt1 | Trạng thái lượt2 | Bằng chứng |
|---|---|---|
| F1 P2 | **VÁ HỜ ở cấp lớp lỗi; còn mở → G1** | Đúng hai ca cũ đỏ, nhưng thêm mã sau điểm cắt làm cả W1/W2/W3 rc141 mà W4 vẫn57/57 |
| F2 P3 | **ĐÃ VÁ THẬT, đã đóng** | Thiếu từng W1/W2/W3/W5 → rc2, đúng chẩn đoán; gỡ chốt → lỗi cũ rc1 |
| F3 P2 | **VÁ HỜ ở đường cấp điểm; còn mở → G4** | Chốt trong helper có răng; đổi nhánh ghi điểm (b) thành luôn đúng vẫn không làm (c) đỏ |
| B1 P2 | **ĐÃ VÁ THẬT trong W5**; khóa hồi quy mới có G2/G3 | 20.000 đối số giữ explicit trên head, nền thêm fallback;105/105 không mất ca |
| Giới hạn corpus HƯỚNG6 | **ĐÃ VÁ THẬT, đã đóng** | strip-star54/57; gỡ corpus mới48/48;5.436 so sánh độc lập xanh |

Bảng findings và hướng khắc phục (reviewer không sửa mã sản phẩm):

| ID | Hạng | Tệp:dòng | Lỗi đã đo | Đề xuất vá / ca khóa / rủi ro |
|---|---|---|---|---|
| G1 (tiếp F1) | P2 | `ops/do_sigpipe.sh:115–122` | Cắt mọi mã sau phép gán; ba pipeline cũ đặt sau dòng trích đều lọt57/57, script đầy đủ rc141. | **Ở đâu/cách:** phép(d) chạy script đầy đủ trong fixture offline và đo kết quả ở điểm sử dụng thật (W1 lệnh cài/probe; W2 kiểm bản và output; W3 gói/số liệu), hoặc từ chối cấu trúc chưa chứng minh được. **Khóa:** giữ dòng vá rồi nối `:; <phép gán nền>` sau dòng; mỗi W1–W3 phải đỏ; head và fixture thật phải xanh. Giữ cả unused/here-doc. **Rủi ro:** chạy phần còn lại có thể cài/tải thật nếu fixture thiếu; phải chặn đường mạng và đặt tất cả đích ghi trong cây tạm, không thay phần logic cần đo bằng stub. |
| G2 | P2 | `ops/do_sigpipe.sh:134–144` | (e) trích hàm đã sửa từ here-doc, bỏ qua `lam ()` cũ được runtime gọi; vẫn57/57 và suite W5 vẫn105/105 nhưng B1 tái xuất hiện. | **Ở đâu/cách:** kiểm tra qua chính W5 với đường nạp/chạy hàm thực tế và recorder tại biên env, hoặc một cơ chế kiểm cú pháp/ngữ cảnh từ chối hàm chết/tái định nghĩa không chứng minh được. **Khóa:** mutant here-doc + hàm runtime baseline của `extra.py` phải đỏ; cả match20.000 và no-match phải được gọi sau khi W5 thiết lập runtime. **Rủi ro:** không execute bước xoá ref thật; giữ gh/git/env giả, giữ ranh giới đối số và nguyên số ca cũ. |
| G3 | P2 | `ops/do_sigpipe.sh:145` | Producer `seq -f` lỗi bị process substitution nuốt; PAD rỗng, ngay W5 nền vẫn57/57. | **Ở đâu/cách:** bắt rc producer trực tiếp (tệp tạm/command substitution được kiểm) rồi kiểm số phần tử PAD đúng DONG_LON, hoặc tạo mảng bằng Bash và kiểm kích thước. Lỗi dựng payload phải `khong_do`. **Khóa:** wrapper chỉ làm `seq -f` trả127 hoặc trả0 nhưng không đủ dòng ⇒ rc2 + KHÔNG ĐO ĐƯỢC; W5 nền vẫn phải đỏ với payload thật. **Rủi ro:** tránh vượt ARG_MAX khi đổi nội dung đệm; không đưa lỗi dựng fixture vào số đo thành công. |
| G4 (tiếp F3) | P2 | `ops/do_sigpipe.sh:183–185,202–204` | (c) kiểm KQ của helper, không kiểm nhánh mà(b) dùng để cấp điểm; đột biến luôn-đúng tại :184 vẫn để(c) xanh. | **Ở đâu/cách:** gom toàn bộ quyết định cấp/khước từ điểm(b) vào một đường được self-check gọi thật, hoặc chạy chế độ con chỉ(b) và đòi rc/nhãn đỏ đúng141; tránh một lớp nhánh chấm độc lập sau helper. **Khóa:** cả đổi predicate :101 và đổi nhánh cấp điểm :184 thành luôn-đúng đều làm(c) đỏ; không nhờ(d)/(e) cứu tổng kết. **Rủi ro:** không đệ quy self-check, không cộng các lượt thử vào bộ đếm cha, phân biệt lỗi dựng fixture với141. |

HƯỚNG 10: Kết luận và điều kiện nghiệm thu

- **0 P1 / 4 P2 / 0 P3 trên diff packet**, tất cả P2 ở W4. G1/G4 là phần chưa đóng của F1/F3, không đếm thêm một lần nữa. W1–W3 hiện hành và bản vá W5 không phát hiện lỗi hành vi mới trong tập đo.
- A1 head/baseline và các điểm riêng đã đo; khóa F2/glob/B1 trực tiếp có tác dụng, nhưng yêu cầu khóa toàn lớp F1/F3 và độ dính B1 chưa đạt. A3/A4/A6 delta lỗi0. A2 phần t5 đạt; suite cong_cu_test đầy đủ **KHÔNG ĐO ĐƯỢC**. A5 chưa đạt ngưỡng0P1/P2/P3.
- Không approve theo ngưỡng của prompt/SPEC: **changes_requested**. Các ca not_run và syscall audit bị chặn không được ghi thành pass.
- Kiểm neo cuối: `git -C cay-kho diff 89fc4fa..HEAD --check` rc0; HEAD/tree/baseline và hash SPEC giữ nguyên như HƯỚNG1; `git status --porcelain --untracked-files=all --ignored` trên cả hai nguồn đều rỗng, rc0. Không sửa nguồn, không push, không đăng GitHub.

Hiện vật cuối: `tam/tmp.dcbYQp7XH2/logs/final-anchors.json` ghi lệnh/rc/output kiểm neo; `evidence.sha256` băm các script và log. Đã dọn 276 thư mục/tệp tạm do suite phụ sinh trong `temp/` (còn0); giữ bản sao, mutant và log để tái lập. Fixture riêng W4 đã tự dọn qua EXIT trap như HƯỚNG6.
